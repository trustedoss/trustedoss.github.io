#!/usr/bin/env python3
"""한국어 원본과 영어 로케일의 문서 파일 목록 패리티를 검사한다.

내용 수준의 번역 품질은 검사하지 않는다. 한쪽에만 있는 파일(번역 누락 또는
원본이 사라진 고아 번역)만 잡는다. 영어 드리프트가 이 저장소에서 가장 자주
재발한 결함이라, 파일 단위 누락만이라도 자동으로 막는 것이 목적이다.

사용법:
    python3 .claude/scripts/check-i18n-parity.py [-v]
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
I18N = ROOT / "website" / "i18n" / "en"

# (한국어 원본 디렉토리, 영어 로케일 디렉토리, 원본 기준 제외 경로)
PAIRS = [
    ("docs", "docusaurus-plugin-content-docs/current", {"_plan"}),
    ("website/ai-coding", "docusaurus-plugin-content-docs-ai-coding/current", set()),
    ("website/devsecops", "docusaurus-plugin-content-docs-devsecops/current", set()),
    ("website/reference", "docusaurus-plugin-content-docs-reference/current", set()),
]

EXTS = {".md", ".mdx"}
# 번역 대상이 아닌 파일 (Claude 컨텍스트 파일 등)
SKIP_NAMES = {"CLAUDE.md"}


def collect(base: Path, excludes: set) -> set:
    if not base.is_dir():
        return set()
    found = set()
    for p in base.rglob("*"):
        if p.suffix not in EXTS or p.name in SKIP_NAMES:
            continue
        rel = p.relative_to(base)
        if rel.parts and rel.parts[0] in excludes:
            continue
        found.add(rel.as_posix())
    return found


def main() -> int:
    verbose = "-v" in sys.argv
    missing_total = 0
    orphan_total = 0

    for ko_dir, en_dir, excludes in PAIRS:
        ko_base = ROOT / ko_dir
        en_base = I18N / en_dir
        ko_files = collect(ko_base, excludes)
        en_files = collect(en_base, excludes)

        missing = sorted(ko_files - en_files)
        orphans = sorted(en_files - ko_files)
        missing_total += len(missing)
        orphan_total += len(orphans)

        for rel in missing:
            print(f"  번역 누락: {en_dir}/{rel} (원본 {ko_dir}/{rel})")
        for rel in orphans:
            print(f"  고아 번역: {en_dir}/{rel} (원본 {ko_dir}/{rel} 없음)")
        if verbose:
            print(f"  [{ko_dir}] ko {len(ko_files)}개 / en {len(en_files)}개")

    if missing_total or orphan_total:
        print(f"  누락 {missing_total}건, 고아 {orphan_total}건")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
