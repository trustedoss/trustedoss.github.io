#!/usr/bin/env python3
"""
Layer 3 E2E Test Runner

Anthropic API를 사용해 각 셀프스터디 agent의 실제 대화 흐름을 시뮬레이션하고
기대 파일 생성 여부 및 내용 패턴을 검증한다.

사용법:
  python3 .claude/scripts/test-agent-e2e.py --agent 02-organization-designer
  python3 .claude/scripts/test-agent-e2e.py --fixture tests/fixtures/04-process-designer-branch-A.json
  python3 .claude/scripts/test-agent-e2e.py --all
  python3 .claude/scripts/test-agent-e2e.py --all -v

  # 카세트 녹화 (ANTHROPIC_API_KEY 필요)
  python3 .claude/scripts/test-agent-e2e.py --all --record

  # 카세트 재생 (API 키 불필요)
  python3 .claude/scripts/test-agent-e2e.py --all

환경변수:
  ANTHROPIC_API_KEY  (--record 모드에서만 필수)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic 패키지가 없습니다. 'pip install anthropic' 후 재실행하세요.")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"
CASSETTES_DIR = PROJECT_ROOT / "tests" / "cassettes"
OUTPUT_SAMPLE_DIR = PROJECT_ROOT / "output-sample"
AGENTS_DIR = PROJECT_ROOT / "agents"


# ---------------------------------------------------------------------------
# 카세트 재생용 Mock 응답 객체
# ---------------------------------------------------------------------------

@dataclass
class _TextBlock:
    text: str
    type: str = "text"


@dataclass
class _ToolUseBlock:
    id: str
    name: str
    input: dict
    type: str = "tool_use"


@dataclass
class _MockResponse:
    content: list
    stop_reason: str


# ---------------------------------------------------------------------------
# 카세트 — 녹화/재생
# ---------------------------------------------------------------------------

class Cassette:
    """API 응답을 JSON 파일로 녹화하고 재생한다."""

    def __init__(self, path: Path, record: bool = False):
        self.path = path
        self._record = record
        self._turns: list[dict] = []
        self._index = 0
        self.mode = "off"

        if record:
            if path.exists():
                self.mode = "done"  # 이미 녹화됨 — 덮어쓰지 않음
            else:
                self.mode = "record"
        elif path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            self._turns = data.get("turns", [])
            self.mode = "replay"
        else:
            self.mode = "skip"

    @property
    def available(self) -> bool:
        return self.mode in ("record", "replay")

    def call(self, client, **kwargs):
        if self.mode == "record":
            for attempt in range(5):
                try:
                    response = client.messages.create(**kwargs)
                    self._turns.append(self._serialize(response))
                    return response
                except anthropic.RateLimitError:
                    wait = 60 * (attempt + 1)
                    print(f"\n  [rate limit] {wait}초 대기 후 재시도 ({attempt + 1}/5)...")
                    time.sleep(wait)
            raise RuntimeError("Rate limit 재시도 5회 소진 — 나중에 다시 시도하세요.")
        elif self.mode == "replay":
            if self._index >= len(self._turns):
                raise RuntimeError(
                    f"카세트 응답 소진 — turn {self._index + 1}번째 응답이 없습니다. "
                    f"'--record'로 재녹화하세요."
                )
            turn = self._turns[self._index]
            self._index += 1
            return self._deserialize(turn)
        raise RuntimeError(f"Cassette.call() called in mode={self.mode}")

    def save(self):
        if self.mode != "record":
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {"turn_count": len(self._turns), "turns": self._turns}
        self.path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def _serialize(self, response) -> dict:
        blocks = []
        for b in response.content:
            if b.type == "text":
                blocks.append({"type": "text", "text": b.text})
            elif b.type == "tool_use":
                blocks.append(
                    {"type": "tool_use", "id": b.id, "name": b.name, "input": b.input}
                )
        return {"content": blocks, "stop_reason": response.stop_reason}

    def _deserialize(self, data: dict) -> _MockResponse:
        blocks = []
        for b in data["content"]:
            if b["type"] == "text":
                blocks.append(_TextBlock(text=b["text"]))
            elif b["type"] == "tool_use":
                blocks.append(
                    _ToolUseBlock(id=b["id"], name=b["name"], input=b["input"])
                )
        return _MockResponse(content=blocks, stop_reason=data["stop_reason"])


# ---------------------------------------------------------------------------
# 픽스처 로드
# ---------------------------------------------------------------------------

def load_fixture(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def find_fixture(agent_name: str) -> Path:
    """agent 이름으로 첫 번째 매칭 fixture 반환."""
    exact = FIXTURES_DIR / f"{agent_name}.json"
    if exact.exists():
        return exact
    matches = sorted(FIXTURES_DIR.glob(f"{agent_name}*.json"))
    if matches:
        return matches[0]
    raise FileNotFoundError(f"fixture를 찾을 수 없습니다: {agent_name}")


def load_system_prompt(agent_name: str) -> str:
    claude_md = AGENTS_DIR / agent_name / "CLAUDE.md"
    if not claude_md.exists():
        raise FileNotFoundError(f"CLAUDE.md 없음: {claude_md}")
    return claude_md.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# tmpdir 준비
# ---------------------------------------------------------------------------

def setup_tmpdir(fixture: dict) -> Path:
    """tmpdir 생성 및 prerequisite_files 복사."""
    tmpdir = Path(tempfile.mkdtemp(prefix="trustedoss-e2e-"))
    output_dir = tmpdir / "output"
    output_dir.mkdir()

    for rel_path, value in fixture.get("prerequisite_files", {}).items():
        dst = output_dir / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        if value == "__COPY_FROM_OUTPUT_SAMPLE__":
            src = OUTPUT_SAMPLE_DIR / rel_path
            if src.exists():
                shutil.copy2(src, dst)
            else:
                print(f"  WARN: prerequisite 없음: {src}")
        else:
            dst.write_text(str(value), encoding="utf-8")

    return tmpdir


# ---------------------------------------------------------------------------
# Mock 도구 정의
# ---------------------------------------------------------------------------

TOOL_SCHEMAS = [
    {
        "name": "Write",
        "description": "파일을 생성하거나 덮어씁니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "작성할 파일 경로"},
                "content": {"type": "string", "description": "파일 내용"}
            },
            "required": ["file_path", "content"]
        }
    },
    {
        "name": "Read",
        "description": "파일을 읽습니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "읽을 파일 경로"},
                "limit": {"type": "integer"},
                "offset": {"type": "integer"}
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "Edit",
        "description": "파일의 특정 문자열을 교체합니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"},
                "old_string": {"type": "string"},
                "new_string": {"type": "string"}
            },
            "required": ["file_path", "old_string", "new_string"]
        }
    },
    {
        "name": "Bash",
        "description": "셸 명령을 실행합니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "실행할 명령"}
            },
            "required": ["command"]
        }
    },
    {
        "name": "Glob",
        "description": "파일 패턴으로 파일을 검색합니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string"},
                "path": {"type": "string"}
            },
            "required": ["pattern"]
        }
    },
    {
        "name": "Grep",
        "description": "파일 내용을 검색합니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string"},
                "path": {"type": "string"},
                "glob": {"type": "string"}
            },
            "required": ["pattern"]
        }
    }
]


def resolve_output_path(file_path: str, output_dir: Path) -> Path:
    """file_path를 output_dir 기준으로 해석."""
    p = file_path.strip()
    if p.startswith("output/"):
        return output_dir / p[len("output/"):]
    if p.startswith("./output/"):
        return output_dir / p[len("./output/"):]
    if "/output/" in p:
        idx = p.index("/output/")
        return output_dir / p[idx + len("/output/"):]
    return output_dir / p


def execute_tool(name: str, tool_input: dict, tmpdir: Path, verbose: bool) -> str:
    """Mock 도구 실행 — 파일은 tmpdir/output/ 에 저장."""
    output_dir = tmpdir / "output"

    if name == "Write":
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "")
        dst = resolve_output_path(file_path, output_dir)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(content, encoding="utf-8")
        if verbose:
            print(f"    Write → {dst.relative_to(tmpdir)}")
        return f"파일 작성 완료: {file_path}"

    elif name == "Read":
        file_path = tool_input.get("file_path", "")
        limit = tool_input.get("limit")
        offset = tool_input.get("offset", 0)

        candidates = [
            resolve_output_path(file_path, output_dir),
            PROJECT_ROOT / file_path.lstrip("/"),
            PROJECT_ROOT / file_path,
        ]
        for c in candidates:
            if c.exists() and c.is_file():
                text = c.read_text(encoding="utf-8")
                lines = text.splitlines(keepends=True)
                if offset:
                    lines = lines[offset:]
                if limit:
                    lines = lines[:limit]
                return "".join(lines)
        return f"(파일 없음: {file_path})"

    elif name == "Edit":
        file_path = tool_input.get("file_path", "")
        old_string = tool_input.get("old_string", "")
        new_string = tool_input.get("new_string", "")
        dst = resolve_output_path(file_path, output_dir)
        if dst.exists():
            text = dst.read_text(encoding="utf-8")
            new_text = text.replace(old_string, new_string, 1)
            dst.write_text(new_text, encoding="utf-8")
            return "편집 완료"
        return f"(파일 없음: {file_path})"

    elif name == "Bash":
        command = tool_input.get("command", "")
        stripped = command.strip()

        if stripped.startswith("cp "):
            parts = stripped.split()
            if len(parts) >= 3:
                src_rel, dst_rel = parts[1], parts[2]
                if src_rel.startswith("output-sample/"):
                    src_path = PROJECT_ROOT / src_rel
                elif src_rel.startswith("output/"):
                    src_path = output_dir / src_rel[len("output/"):]
                else:
                    src_path = PROJECT_ROOT / src_rel
                dst_path = resolve_output_path(dst_rel, output_dir)
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                if src_path.exists():
                    shutil.copy2(src_path, dst_path)
                    if verbose:
                        print(f"    cp {src_rel} → {dst_path.relative_to(tmpdir)}")
                    return f"복사 완료: {src_rel} → {dst_rel}"
                return f"(cp 오류: {src_rel} 없음)"
            return "(cp: 인수 부족)"

        if stripped.startswith("chmod "):
            return "권한 설정 완료"

        safe_prefixes = ("ls ", "ls\n", "ls", "mkdir", "echo ", "cat ", "pwd")
        if any(stripped.startswith(p) for p in safe_prefixes):
            safe_cmd = command.replace(" output/", f" {output_dir}/")
            safe_cmd = safe_cmd.replace('"output/', f'"{output_dir}/')
            safe_cmd = safe_cmd.replace(">output/", f">{output_dir}/")
            safe_cmd = safe_cmd.replace(">>output/", f">>{output_dir}/")
            try:
                result = subprocess.run(
                    safe_cmd, shell=True, capture_output=True, text=True,
                    timeout=5, cwd=str(tmpdir)
                )
                return (result.stdout + result.stderr).strip() or "(no output)"
            except subprocess.TimeoutExpired:
                return "(timeout)"
            except Exception as e:
                return f"(오류: {e})"
        return f"(mock-bash: {command[:80]})"

    elif name == "Glob":
        pattern = tool_input.get("pattern", "")
        search_path_str = tool_input.get("path", "")
        if not search_path_str or search_path_str in (".", "output", "output/"):
            search_path = output_dir
        elif search_path_str.startswith("output/"):
            search_path = output_dir / search_path_str[len("output/"):]
        else:
            search_path = PROJECT_ROOT / search_path_str
        try:
            matches = sorted(search_path.glob(pattern))
            return "\n".join(str(m.relative_to(tmpdir)) for m in matches) or "(no matches)"
        except Exception as e:
            return f"(glob error: {e})"

    elif name == "Grep":
        pattern = tool_input.get("pattern", "")
        path_str = tool_input.get("path", "output")
        if path_str.startswith("output"):
            search_path = output_dir
        else:
            search_path = PROJECT_ROOT / path_str
        try:
            import re
            results = []
            glob_pat = tool_input.get("glob", "**/*")
            for f in search_path.glob(glob_pat):
                if f.is_file():
                    try:
                        text = f.read_text(encoding="utf-8")
                        for i, line in enumerate(text.splitlines(), 1):
                            if re.search(pattern, line):
                                results.append(f"{f.relative_to(tmpdir)}:{i}: {line}")
                    except Exception:
                        pass
            return "\n".join(results[:50]) or "(no matches)"
        except Exception as e:
            return f"(grep error: {e})"

    return f"(unknown tool: {name})"


# ---------------------------------------------------------------------------
# E2E 대화 루프
# ---------------------------------------------------------------------------

def run_conversation(
    system_prompt: str,
    model: str,
    inputs: list,
    tmpdir: Path,
    verbose: bool,
    cassette: Cassette,
) -> None:
    """멀티턴 대화 실행 — 카세트가 있으면 재생, 없으면 실제 API 호출."""
    client = anthropic.Anthropic() if cassette.mode == "record" else None
    messages = []
    input_index = 0
    max_turns = 80

    messages.append({"role": "user", "content": "시작해주세요."})

    for turn in range(1, max_turns + 1):
        if verbose:
            mode_label = f"[{cassette.mode}]"
            print(f"  [turn {turn}] {mode_label} (input_index={input_index}/{len(inputs)})")

        response = cassette.call(
            client,
            model=model,
            max_tokens=8192,
            system=system_prompt,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
        if tool_use_blocks:
            tool_results = []
            for block in tool_use_blocks:
                result = execute_tool(block.name, block.input, tmpdir, verbose)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })
            messages.append({"role": "user", "content": tool_results})
            continue

        if response.stop_reason == "end_turn":
            if input_index < len(inputs):
                answer = inputs[input_index]
                input_index += 1
                if verbose:
                    print(f"  → 입력 [{input_index}/{len(inputs)}]: {answer!r}")
                messages.append({"role": "user", "content": answer})
            else:
                if verbose:
                    print("  모든 입력 소진 → 대화 종료")
                break
        else:
            if verbose:
                print(f"  stop_reason={response.stop_reason} → 종료")
            break
    else:
        print(f"  WARN: max_turns({max_turns}) 초과")


# ---------------------------------------------------------------------------
# 검증
# ---------------------------------------------------------------------------

def verify_output(fixture: dict, tmpdir: Path, verbose: bool) -> list:
    """기대 파일·패턴 검증. 오류 목록 반환."""
    output_dir = tmpdir / "output"
    errors = []

    for rel_path in fixture.get("expected_files", []):
        fpath = output_dir / rel_path
        if fpath.exists():
            if verbose:
                print(f"  ✓ {rel_path}")
        else:
            errors.append(f"MISSING: {rel_path}")

    for rel_path in fixture.get("expected_absent", []):
        fpath = output_dir / rel_path
        if fpath.exists():
            errors.append(f"SHOULD_NOT_EXIST: {rel_path}")
        elif verbose:
            print(f"  ✓ ABSENT: {rel_path}")

    for rel_path, patterns in fixture.get("content_patterns", {}).items():
        fpath = output_dir / rel_path
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding="utf-8")
        for pattern in patterns:
            if pattern not in content:
                errors.append(f"PATTERN_NOT_FOUND in {rel_path}: '{pattern}'")
            elif verbose:
                print(f"  ✓ '{pattern}' in {rel_path}")

    return errors


# ---------------------------------------------------------------------------
# 단일 fixture 실행
# ---------------------------------------------------------------------------

def run_fixture(fixture: dict, fixture_path: Path, verbose: bool = False, record: bool = False) -> Optional[bool]:
    """단일 fixture 실행. PASS→True / FAIL→False / SKIP→None."""
    agent_name = fixture["agent"]
    model = fixture.get("model", "claude-sonnet-4-6")
    inputs = fixture.get("inputs", [])
    desc = fixture.get("description", "")

    # 카세트 이름: fixture 파일 stem 기준 — 동일 agent의 복수 fixture를 분리
    cassette_path = CASSETTES_DIR / f"{fixture_path.stem}.json"
    cassette = Cassette(cassette_path, record=record)

    print(f"\n{'='*60}")
    print(f"Agent  : {agent_name}  (fixture: {fixture_path.name})")
    if desc:
        print(f"설명   : {desc}")
    print(f"모델   : {model}  입력수: {len(inputs)}  카세트: [{cassette.mode}]")
    print(f"{'='*60}")

    if cassette.mode == "skip":
        print("SKIP — 카세트 없음 (녹화하려면 --record 플래그 사용)")
        return None

    if cassette.mode == "done":
        print("SKIP — 이미 녹화됨")
        return None

    system_prompt = load_system_prompt(agent_name)
    tmpdir = setup_tmpdir(fixture)

    try:
        run_conversation(system_prompt, model, inputs, tmpdir, verbose, cassette)

        if record:
            cassette.save()
            if verbose:
                print(f"  카세트 저장 → {cassette_path.relative_to(PROJECT_ROOT)}")

        errors = verify_output(fixture, tmpdir, verbose)

        if errors:
            print(f"\nFAIL — {len(errors)}개 오류:")
            for e in errors:
                print(f"  ✗ {e}")
            return False
        else:
            n = len(fixture.get("expected_files", []))
            print(f"\nPASS — {n}개 파일 생성 확인")
            return True
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Layer 3 E2E 테스트 — 카세트 재생(무료) 또는 실제 API 호출",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--agent", metavar="NAME",
                       help="agent 이름 (예: 02-organization-designer)")
    group.add_argument("--fixture", metavar="PATH",
                       help="fixture JSON 경로")
    group.add_argument("--all", action="store_true",
                       help="tests/fixtures/ 내 모든 fixture 실행")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="상세 출력 (도구 호출, 입력 흐름 등)")
    parser.add_argument("--record", action="store_true",
                        help="실제 API를 호출하여 카세트를 녹화/갱신 (ANTHROPIC_API_KEY 필요)")
    args = parser.parse_args()

    if args.record:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("ERROR: --record 모드는 ANTHROPIC_API_KEY가 필요합니다.")
            sys.exit(1)
    else:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("INFO: ANTHROPIC_API_KEY 없음 — 카세트 재생 모드로 실행합니다.")

    fixture_paths: list[Path] = []
    if args.fixture:
        fixture_paths.append(Path(args.fixture))
    elif args.agent:
        fixture_paths.append(find_fixture(args.agent))
    else:
        fixture_paths = sorted(FIXTURES_DIR.glob("*.json"))

    if not fixture_paths:
        print("ERROR: 실행할 fixture가 없습니다.")
        sys.exit(1)

    results: list = []
    for fp in fixture_paths:
        fixture = load_fixture(fp)
        result = run_fixture(fixture, fixture_path=fp, verbose=args.verbose, record=args.record)
        results.append((fp.name, result))

    total = len(results)
    passed = sum(1 for _, r in results if r is True)
    failed = sum(1 for _, r in results if r is False)
    skipped = sum(1 for _, r in results if r is None)

    print(f"\n{'='*60}")
    print(f"최종 결과: {passed} PASS / {failed} FAIL / {skipped} SKIP  (총 {total})")
    for name, result in results:
        if result is True:
            status = "PASS"
        elif result is False:
            status = "FAIL"
        else:
            status = "SKIP"
        print(f"  [{status}] {name}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
