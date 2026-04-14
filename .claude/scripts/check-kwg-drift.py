#!/usr/bin/env python3
"""
check-kwg-drift.py
KWG 원본 파일의 구조적 변경을 감지하고 스냅샷과 비교한다.

4개 차원 감지:
  차원 1: KWG 가이드 헤딩 변경 → 우리 docs/ 챕터 영향
  차원 2: KWG 템플릿 ISO 항목 변경 → 우리 templates/ 영향
  차원 3: KWG 도구 수 변경 → 우리 docs/05-tools/ 영향
  차원 4: 매핑 테이블 미반영 ISO 섹션 → checklist-mapping.md 영향

실행:
  python3 .claude/scripts/check-kwg-drift.py
  python3 .claude/scripts/check-kwg-drift.py --reset   # 스냅샷 초기화
  python3 .claude/scripts/check-kwg-drift.py --verbose  # 상세 출력

출력:
  변경 없음 → "싱크 OK" 출력 후 종료 (exit 0)
  변경 있음 → 변경 내용 출력 후 /kwg-check 실행 안내 (exit 1)
"""

import sys
import os
import re
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("⚠️  PyYAML 없음. 설치: pip3 install pyyaml")
    sys.exit(2)

# ── 경로 설정 ──────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
KWG_ROOT     = PROJECT_ROOT / ".claude/reference/kwg"
SNAPSHOT_DIR = KWG_ROOT / ".sync-snapshot"
MAPPING_FILE = PROJECT_ROOT / ".claude/reference/kwg-mapping.yaml"

SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

HEADINGS_SNAP = SNAPSHOT_DIR / "headings.json"
ISO_SNAP      = SNAPSHOT_DIR / "iso_sections.json"
TOOLS_SNAP    = SNAPSHOT_DIR / "tools.json"
HASH_SNAP     = SNAPSHOT_DIR / "file_hashes.json"

# ── 유틸 ───────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def file_hash(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.md5(path.read_bytes()).hexdigest()

def extract_headings(path: Path) -> list[str]:
    """마크다운 파일에서 ## 헤딩 목록 추출 (Hugo shortcode 제외)."""
    if not path.exists():
        return []
    headings = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## ") or line.startswith("### "):
            # Hugo shortcode, 빈 줄 제거
            h = re.sub(r'\{[{%].*?[%}]\}', '', line).strip()
            h = re.sub(r'\s+', ' ', h)
            if h:
                headings.append(h)
    return headings

def extract_iso_sections(path: Path) -> list[str]:
    """KWG 파일에서 ISO 섹션 번호 패턴 추출 (예: 3.1.1.1)."""
    if not path.exists():
        return []
    pattern = re.compile(r'\b(\d+\.\d+\.\d+(?:\.\d+)?)\b')
    text = path.read_text(encoding="utf-8")
    # alert 블록 내용만 추출
    alert_blocks = re.findall(r'\{{% alert.*?%\}\}(.*?)\{{% /alert %\}\}', text, re.DOTALL)
    sections = set()
    for block in alert_blocks:
        for m in pattern.finditer(block):
            sections.add(m.group(1))
    return sorted(sections)

def count_tool_dirs(tools_dir: Path) -> list[str]:
    """tools/ 하위 번호 디렉토리 목록 반환."""
    if not tools_dir.exists():
        return []
    dirs = [d.name for d in sorted(tools_dir.iterdir())
            if d.is_dir() and re.match(r'^\d+', d.name)]
    return dirs

# ── 메인 로직 ──────────────────────────────────────────────

def check_drift(mapping: dict, verbose: bool) -> list[dict]:
    """4개 차원 드리프트 감지. 변경 항목 리스트 반환."""
    changes = []

    prev_headings = load_json(HEADINGS_SNAP)
    prev_iso      = load_json(ISO_SNAP)
    prev_tools    = load_json(TOOLS_SNAP)
    prev_hashes   = load_json(HASH_SNAP)

    curr_headings = {}
    curr_iso      = {}
    curr_hashes   = {}

    # ── 차원 1: 가이드 헤딩 변경 ──
    print("\n[차원 1] KWG 가이드 헤딩 변경 감지...")
    for entry in mapping.get("guide_mappings", []):
        kwg_rel = entry["kwg_file"]
        kwg_abs = KWG_ROOT / kwg_rel
        curr_hash = file_hash(kwg_abs)
        curr_hashes[kwg_rel] = curr_hash

        headings = extract_headings(kwg_abs)
        curr_headings[kwg_rel] = headings

        prev_h = set(prev_headings.get(kwg_rel, []))
        curr_h = set(headings)

        added   = curr_h - prev_h
        removed = prev_h - curr_h

        if added or removed:
            change = {
                "dimension": 1,
                "kwg_file": kwg_rel,
                "our_files": entry["our_files"],
                "description": entry["description"],
                "watch_for": entry.get("watch_for", []),
                "added_headings": sorted(added),
                "removed_headings": sorted(removed),
            }
            changes.append(change)
            print(f"  ⚠️  변경: {kwg_rel}")
            if verbose:
                for h in sorted(added):
                    print(f"       + {h}")
                for h in sorted(removed):
                    print(f"       - {h}")
        else:
            if verbose:
                print(f"  ✅ 동일: {kwg_rel}")

    # ── 차원 2: 템플릿 ISO 항목 변경 ──
    print("\n[차원 2] KWG 템플릿 ISO 항목 변경 감지...")
    for entry in mapping.get("template_mappings", []):
        kwg_rel = entry["kwg_file"]
        kwg_abs = KWG_ROOT / kwg_rel
        curr_hash = file_hash(kwg_abs)
        curr_hashes[kwg_rel] = curr_hash

        iso_sections = extract_iso_sections(kwg_abs)
        curr_iso[kwg_rel] = iso_sections

        prev_s = set(prev_iso.get(kwg_rel, []))
        curr_s = set(iso_sections)

        added   = curr_s - prev_s
        removed = prev_s - curr_s

        # 헤딩 변경도 감지
        headings = extract_headings(kwg_abs)
        curr_headings[kwg_rel] = headings
        prev_h = set(prev_headings.get(kwg_rel, []))
        curr_h = set(headings)
        added_h   = curr_h - prev_h
        removed_h = prev_h - curr_h

        if added or removed or added_h or removed_h:
            change = {
                "dimension": 2,
                "kwg_file": kwg_rel,
                "our_files": entry["our_files"],
                "description": entry["description"],
                "watch_for": entry.get("watch_for", []),
                "added_iso": sorted(added),
                "removed_iso": sorted(removed),
                "added_headings": sorted(added_h),
                "removed_headings": sorted(removed_h),
            }
            changes.append(change)
            print(f"  ⚠️  변경: {kwg_rel}")
            if verbose and (added or removed):
                for s in sorted(added):
                    print(f"       + ISO §{s}")
                for s in sorted(removed):
                    print(f"       - ISO §{s}")
        else:
            if verbose:
                print(f"  ✅ 동일: {kwg_rel}")

    # ── 차원 3: 도구 수 변경 ──
    print("\n[차원 3] KWG 도구 목록 변경 감지...")
    tools_dim  = mapping.get("tools_dimension", {})
    tools_dir  = KWG_ROOT / tools_dim.get("kwg_tools_dir", "content/ko/guide/tools")
    curr_tools = count_tool_dirs(tools_dir)
    expected   = tools_dim.get("expected_tool_count", 0)
    known      = [t["dir"] for t in tools_dim.get("known_tools", [])]

    prev_tools_list = prev_tools.get("dirs", known)
    curr_tools_set  = set(curr_tools)
    prev_tools_set  = set(prev_tools_list)

    new_tools     = curr_tools_set - prev_tools_set
    removed_tools = prev_tools_set - curr_tools_set

    if new_tools or removed_tools:
        changes.append({
            "dimension": 3,
            "kwg_file": str(tools_dir.relative_to(KWG_ROOT)),
            "our_files": [tools_dim.get("our_tools_doc", "docs/05-tools/index.md")],
            "description": "KWG 도구 목록 변경",
            "watch_for": ["새 도구 추가 시 docs/05-tools/ 반영 필요"],
            "new_tools": sorted(new_tools),
            "removed_tools": sorted(removed_tools),
            "current_count": len(curr_tools),
            "expected_count": expected,
        })
        print(f"  ⚠️  도구 수 변경: {len(prev_tools_list)}개 → {len(curr_tools)}개")
        if verbose:
            for t in sorted(new_tools):
                print(f"       + {t}")
            for t in sorted(removed_tools):
                print(f"       - {t}")
    else:
        if verbose:
            print(f"  ✅ 동일: {len(curr_tools)}개 도구")

    # ── 차원 4: 매핑 미반영 ISO 섹션 ──
    print("\n[차원 4] ISO 섹션 매핑 누락 감지...")
    mapped_sections = set()
    for entry in mapping.get("iso_section_mapping", []):
        for s in entry.get("kwg_sections", []):
            mapped_sections.add(s)

    # KWG 가이드 파일 전체에서 ISO 섹션 번호 수집
    all_kwg_files = list(KWG_ROOT.rglob("*.md"))
    found_sections = set()
    pattern = re.compile(r'\b(\d+\.\d+(?:\.\d+)?)\b')
    for kwg_file in all_kwg_files:
        text = kwg_file.read_text(encoding="utf-8")
        # alert 블록 내용만
        alert_blocks = re.findall(r'\{{% alert.*?%\}\}(.*?)\{{% /alert %\}\}', text, re.DOTALL)
        for block in alert_blocks:
            for m in pattern.finditer(block):
                s = m.group(1)
                # 최소 3자리 섹션 번호 (3.1.1 이상)
                parts = s.split(".")
                if len(parts) >= 3:
                    # 상위 섹션 (3.x.x)만 추적
                    found_sections.add(".".join(parts[:3]))

    unmapped = found_sections - mapped_sections
    if unmapped:
        changes.append({
            "dimension": 4,
            "kwg_file": "(전체 KWG 파일)",
            "our_files": ["docs/00-overview/checklist-mapping.md"],
            "description": "kwg-mapping.yaml에 없는 ISO 섹션 번호 발견",
            "watch_for": ["새 ISO 요구사항이 우리 G항목 체계에 없을 수 있음"],
            "unmapped_sections": sorted(unmapped),
        })
        print(f"  ⚠️  매핑 누락 ISO 섹션: {sorted(unmapped)}")
    else:
        if verbose:
            print(f"  ✅ 모든 ISO 섹션 매핑됨 ({len(found_sections)}개)")

    # ── 스냅샷 갱신 ──
    save_json(HEADINGS_SNAP, curr_headings)
    save_json(ISO_SNAP, curr_iso)
    save_json(TOOLS_SNAP, {"dirs": curr_tools, "updated": datetime.utcnow().isoformat()})
    save_json(HASH_SNAP, curr_hashes)

    return changes

def reset_snapshot():
    """스냅샷 초기화 (다음 실행 시 현재 상태를 기준점으로 재설정)."""
    for f in [HEADINGS_SNAP, ISO_SNAP, TOOLS_SNAP, HASH_SNAP]:
        if f.exists():
            f.unlink()
    print("✅ 스냅샷 초기화 완료. 다음 실행 시 현재 상태를 기준점으로 사용합니다.")

def print_report(changes: list[dict]):
    """드리프트 리포트 출력."""
    print("\n" + "="*60)
    print("  KWG 드리프트 감지 결과")
    print("="*60)

    if not changes:
        print("\n✅ 싱크 OK — 마지막 동기화 대비 구조적 변경 없음")
        print(f"   (스냅샷 기준: {SNAPSHOT_DIR})")
        return

    print(f"\n⚠️  변경 감지: {len(changes)}개 항목\n")
    for c in changes:
        dim = c["dimension"]
        print(f"[차원 {dim}] {c['description']}")
        print(f"  KWG 파일  : {c['kwg_file']}")
        print(f"  영향 파일 : {', '.join(c['our_files'])}")

        if c.get("added_headings"):
            print(f"  추가 헤딩 : {c['added_headings']}")
        if c.get("removed_headings"):
            print(f"  삭제 헤딩 : {c['removed_headings']}")
        if c.get("added_iso"):
            print(f"  추가 ISO  : {c['added_iso']}")
        if c.get("removed_iso"):
            print(f"  삭제 ISO  : {c['removed_iso']}")
        if c.get("new_tools"):
            print(f"  추가 도구 : {c['new_tools']}")
        if c.get("removed_tools"):
            print(f"  삭제 도구 : {c['removed_tools']}")
        if c.get("unmapped_sections"):
            print(f"  미매핑 섹션: {c['unmapped_sections']}")

        if c.get("watch_for"):
            print(f"  확인 사항 :")
            for w in c["watch_for"]:
                print(f"    - {w}")
        print()

    print("─"*60)
    print("👉 다음 단계: /kwg-check 를 실행하여 의미론적 갭 분석 시작")
    print("   또는 직접 확인 후 kwg-mapping.yaml 및 관련 파일 업데이트")
    print("─"*60)

def main():
    parser = argparse.ArgumentParser(description="KWG 원본 드리프트 감지")
    parser.add_argument("--reset",   action="store_true", help="스냅샷 초기화")
    parser.add_argument("--verbose", action="store_true", help="상세 출력")
    args = parser.parse_args()

    if args.reset:
        reset_snapshot()
        return

    if not MAPPING_FILE.exists():
        print(f"❌ kwg-mapping.yaml 없음: {MAPPING_FILE}")
        sys.exit(2)

    if not KWG_ROOT.exists():
        print("❌ .claude/reference/kwg/ 없음. sync-kwg-reference.sh 먼저 실행하세요.")
        sys.exit(2)

    # 스냅샷 없으면 초기 기준점 설정
    is_first_run = not HEADINGS_SNAP.exists()
    if is_first_run:
        print("ℹ️  첫 실행 — 현재 상태를 기준 스냅샷으로 설정합니다.")
        print("   다음 sync-kwg-reference.sh 실행 시부터 변경 감지가 활성화됩니다.\n")

    mapping = load_yaml(MAPPING_FILE)
    changes = check_drift(mapping, args.verbose)
    print_report(changes)

    if is_first_run:
        print("\nℹ️  기준 스냅샷 저장 완료.")
        sys.exit(0)

    sys.exit(1 if changes else 0)

if __name__ == "__main__":
    main()
