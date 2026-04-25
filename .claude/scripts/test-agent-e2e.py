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

환경변수:
  ANTHROPIC_API_KEY  (필수)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic 패키지가 없습니다. 'pip install anthropic' 후 재실행하세요.")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"
OUTPUT_SAMPLE_DIR = PROJECT_ROOT / "output-sample"
AGENTS_DIR = PROJECT_ROOT / "agents"


# ---------------------------------------------------------------------------
# 픽스처 로드
# ---------------------------------------------------------------------------

def load_fixture(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def find_fixture(agent_name: str) -> Path:
    """agent 이름으로 첫 번째 매칭 fixture 반환."""
    # exact name match
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
    # 절대 경로지만 output/ 포함
    if "/output/" in p:
        idx = p.index("/output/")
        return output_dir / p[idx + len("/output/"):]
    # 그 외: output_dir 아래로
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

        # 검색 순서: output_dir → project root (templates 등)
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

        # cp 명령: output-sample/ → output/ 복사 처리
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

        # chmod 명령: 권한 설정 mock (항상 성공)
        if stripped.startswith("chmod "):
            return "권한 설정 완료"

        # 출력 확인용 ls / mkdir / echo 등만 허용
        safe_prefixes = ("ls ", "ls\n", "ls", "mkdir", "echo ", "cat ", "pwd")
        if any(stripped.startswith(p) for p in safe_prefixes):
            # output/ 경로를 실제 output_dir로 치환
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
        # 안전하지 않은 명령은 dry-run
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
) -> None:
    """Anthropic API 멀티턴 대화 실행."""
    client = anthropic.Anthropic()
    messages = []
    input_index = 0
    max_turns = 80

    # 첫 번째 메시지: agent가 세션 시작 시 자동으로 질문을 시작하도록 유도
    messages.append({"role": "user", "content": "시작해주세요."})

    for turn in range(1, max_turns + 1):
        if verbose:
            print(f"  [turn {turn}] API 호출 중... (input_index={input_index}/{len(inputs)})")

        response = client.messages.create(
            model=model,
            max_tokens=8192,
            system=system_prompt,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )

        # assistant 응답 저장
        messages.append({"role": "assistant", "content": response.content})

        # 도구 호출 처리
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
            continue  # 도구 결과 후 다시 응답 대기

        # 텍스트 응답 — 다음 입력 제공 또는 종료
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
            # max_tokens 등 예외적 stop_reason
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
            continue  # MISSING은 이미 위에서 기록
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

def run_fixture(fixture: dict, verbose: bool = False) -> bool:
    """단일 fixture 실행. 성공 시 True."""
    agent_name = fixture["agent"]
    model = fixture.get("model", "claude-sonnet-4-6")
    inputs = fixture.get("inputs", [])
    desc = fixture.get("description", "")

    print(f"\n{'='*60}")
    print(f"Agent  : {agent_name}")
    if desc:
        print(f"설명   : {desc}")
    print(f"모델   : {model}  입력수: {len(inputs)}")
    print(f"{'='*60}")

    system_prompt = load_system_prompt(agent_name)
    tmpdir = setup_tmpdir(fixture)

    try:
        run_conversation(system_prompt, model, inputs, tmpdir, verbose)
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
        description="Layer 3 E2E 테스트 — Anthropic API 기반 agent 대화 시뮬레이션",
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
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY 환경변수를 설정하세요.")
        sys.exit(1)

    # fixture 목록 수집
    fixture_paths: list[Path] = []
    if args.fixture:
        fixture_paths.append(Path(args.fixture))
    elif args.agent:
        fixture_paths.append(find_fixture(args.agent))
    else:  # --all
        fixture_paths = sorted(FIXTURES_DIR.glob("*.json"))

    if not fixture_paths:
        print("ERROR: 실행할 fixture가 없습니다.")
        sys.exit(1)

    results: list[tuple[str, bool]] = []
    for fp in fixture_paths:
        fixture = load_fixture(fp)
        passed = run_fixture(fixture, verbose=args.verbose)
        results.append((fp.name, passed))

    print(f"\n{'='*60}")
    total = len(results)
    passed_count = sum(1 for _, p in results if p)
    print(f"최종 결과: {passed_count}/{total} PASS")
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}")

    sys.exit(0 if passed_count == total else 1)


if __name__ == "__main__":
    main()
