#!/usr/bin/env python3
"""
ISO/IEC 5230 + 18974 커버리지 검증 스크립트

셀프가이드를 따라 agent를 실행했을 때 모든 ISO 입증자료가
생성 가능한지를 정적(static) 분석으로 검증합니다.

검증 항목:
  [A] checklist-mapping.md: 모든 G-항목에 담당 Agent 할당 여부
  [B] checklist-mapping.md: 모든 G-항목에 output/ 파일 할당 여부
  [C] mapping ↔ validate-checklist 일관성 (누락 파일 탐지)
  [D] agents/ CLAUDE.md가 참조하는 templates/ 파일 존재 여부

실행:
  python3 .claude/scripts/test-coverage.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MAPPING_FILE = ROOT / "docs/00-overview/checklist-mapping.md"
VALIDATE_FILE = ROOT / ".claude/skills/validate-checklist.md"
AGENTS_DIR = ROOT / "agents"

PASS_COUNT = 0
FAIL_COUNT = 0
failures = []


def record(label: str, ok: bool, detail: str = ""):
    global PASS_COUNT, FAIL_COUNT
    if ok:
        print(f"  PASS  {label}")
        PASS_COUNT += 1
    else:
        msg = f"  FAIL  {label}" + (f"\n        → {detail}" if detail else "")
        print(msg)
        FAIL_COUNT += 1
        failures.append((label, detail))


# ─── 파서 ────────────────────────────────────────────────────────────────────

def parse_mapping() -> list[dict]:
    """checklist-mapping.md에서 G-항목 데이터 파싱"""
    text = MAPPING_FILE.read_text(encoding="utf-8")
    items = []

    # G항목 블록 분리 (#### G...)
    blocks = re.split(r"(?=^#### G)", text, flags=re.MULTILINE)

    for block in blocks:
        header_match = re.match(r"#### (G[\w.]+)\s*—\s*([^\n`[]+)", block)
        if not header_match:
            continue

        g_id = header_match.group(1).strip()
        g_name = header_match.group(2).strip()

        # 산출물 파일 추출 (`output/...` 패턴)
        output_files = re.findall(r"`(output/[^`]+)`", block)

        # 담당 Agent 추출
        agent_match = re.search(r"- \*\*담당 Agent\*\*:\s*`([^`]+)`", block)
        agent = agent_match.group(1).strip() if agent_match else ""

        items.append({
            "id": g_id,
            "name": g_name,
            "output_files": output_files,
            "agent": agent,
        })

    return items


def parse_validate_files() -> list[str]:
    """validate-checklist.md에서 output/ 파일 목록 파싱"""
    text = VALIDATE_FILE.read_text(encoding="utf-8")
    # "N. output/..." 패턴 — 백슬래시 이스케이프 처리(\* → *)
    raw = re.findall(r"\d+\.\s+(output/[^\s—]+)", text)
    return [f.replace("\\*", "*").rstrip(".") for f in raw]


# ─── 테스트 A: G-항목 Agent 할당 ─────────────────────────────────────────────

def test_a(items: list[dict]):
    print("\n[A] G-항목 담당 Agent 할당 확인")

    record(
        f"G-항목 수 ≥ 25 (발견: {len(items)}개)",
        len(items) >= 25,
        f"checklist-mapping.md에서 {len(items)}개 파싱됨",
    )

    unassigned = [it["id"] for it in items if not it["agent"]]
    record(
        "모든 G-항목에 담당 Agent 할당",
        len(unassigned) == 0,
        f"미할당: {unassigned}" if unassigned else "",
    )

    # 담당 Agent 디렉토리 실제 존재 확인
    agent_dirs = {d.name for d in AGENTS_DIR.iterdir() if d.is_dir()}
    missing_agents = []
    for it in items:
        if it["agent"] and it["agent"] not in agent_dirs:
            missing_agents.append(f"{it['id']} → {it['agent']}")
    record(
        "모든 담당 Agent 디렉토리 존재",
        len(missing_agents) == 0,
        "; ".join(missing_agents) if missing_agents else "",
    )


# ─── 테스트 B: G-항목 output 파일 할당 ────────────────────────────────────────

def test_b(items: list[dict]):
    print("\n[B] G-항목 output 파일 할당 확인")

    no_output = [it["id"] for it in items if not it["output_files"]]
    record(
        "모든 G-항목에 output 파일 할당",
        len(no_output) == 0,
        f"output 없음: {no_output}" if no_output else "",
    )


# ─── 테스트 C: mapping ↔ validate-checklist 일관성 ───────────────────────────

def test_c(items: list[dict], validate_files: list[str]):
    print("\n[C] checklist-mapping ↔ validate-checklist 일관성 확인")

    # mapping의 모든 .md output 파일 수집
    mapping_md_files: set[str] = set()
    for it in items:
        for f in it["output_files"]:
            if f.endswith(".md"):
                mapping_md_files.add(f)

    # validate의 파일 집합
    validate_set = set(validate_files)

    # validate에 있지만 mapping에 없는 파일 (validate 추가분 — 누락 위험)
    not_in_mapping = sorted(
        vf for vf in validate_set
        if "*" not in vf and vf not in mapping_md_files
    )
    record(
        "validate-checklist의 모든 파일이 checklist-mapping에 커버됨",
        len(not_in_mapping) == 0,
        "매핑 누락: " + ", ".join(not_in_mapping) if not_in_mapping else "",
    )

    # mapping에 있지만 validate에 없는 파일 (validate 체크 누락 가능성)
    not_in_validate = sorted(
        mf for mf in mapping_md_files
        if mf not in validate_set
        # sbom-commands.sh 등 비-md 제외 이미 됨; conformance/ 하위는 별도 확인
        and "conformance/" not in mf  # conformance 파일은 07 agent가 생성 — 별도 처리
    )
    if not_in_validate:
        # 정보성 출력 (FAIL이 아님 — conformance/ 외 파일만 필수)
        print(f"  INFO  mapping에는 있으나 validate에 없는 파일: {', '.join(not_in_validate)}")


# ─── 테스트 D: templates/ 파일 존재 확인 ─────────────────────────────────────

def test_d():
    print("\n[D] Agent CLAUDE.md 참조 templates/ 파일 존재 확인")

    missing = []
    for agent_dir in sorted(AGENTS_DIR.iterdir()):
        claude_md = agent_dir / "CLAUDE.md"
        if not claude_md.exists():
            continue
        text = claude_md.read_text(encoding="utf-8")
        refs = re.findall(r"`(templates/[^`]+\.md)`", text)
        for ref in refs:
            path = ROOT / ref
            if not path.exists():
                missing.append(f"{agent_dir.name}/CLAUDE.md → {ref}")

    record(
        "모든 참조 templates/ 파일 존재",
        len(missing) == 0,
        "; ".join(missing) if missing else "",
    )


# ─── 실행 ─────────────────────────────────────────────────────────────────────

print("=" * 55)
print("  ISO/IEC 5230 + 18974 커버리지 검증")
print("=" * 55)

if not MAPPING_FILE.exists():
    print(f"ERROR: {MAPPING_FILE} 없음")
    sys.exit(2)
if not VALIDATE_FILE.exists():
    print(f"ERROR: {VALIDATE_FILE} 없음")
    sys.exit(2)

items = parse_mapping()
validate_files = parse_validate_files()

test_a(items)
test_b(items)
test_c(items, validate_files)
test_d()

print()
print("=" * 55)
print(f"  PASS: {PASS_COUNT}  /  FAIL: {FAIL_COUNT}")
print("=" * 55)

if failures:
    print("\n조치 필요 항목:")
    for label, detail in failures:
        print(f"  • {label}")
        if detail:
            print(f"    {detail}")

if FAIL_COUNT == 0:
    print("\n모든 커버리지 검증 통과.")
    sys.exit(0)
else:
    print(f"\n{FAIL_COUNT}개 항목 실패. 수정 후 재실행하세요.")
    sys.exit(1)
