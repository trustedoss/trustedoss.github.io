#!/usr/bin/env python3
"""
validate-output.py — output/ 산출물 완전성 검증

output/이 없거나 비어있으면 SKIP (아직 진행 전)
output/에 파일이 존재하면 각 챕터의 필수 파일 완성도 검증

verify.sh [9/9]에서 호출되며, 독립 실행도 가능.
"""

import os
import sys
import glob

# 프로젝트 루트 기준 output/ 경로
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# 챕터별 필수 파일 목록
CHAPTER_FILES = {
    "organization": [
        "role-definition.md",
        "raci-matrix.md",
        "appointment-template.md",
    ],
    "policy": [
        "oss-policy.md",
        "license-allowlist.md",
    ],
    "process": [
        "usage-approval.md",
        "distribution-checklist.md",
        "vulnerability-response.md",
        "inquiry-response.md",
    ],
    "sbom": [
        "sbom-management-plan.md",
    ],
    "vulnerability": [
        "cve-report.md",
        "remediation-plan.md",
    ],
    "training": [
        "curriculum.md",
        "completion-tracker.md",
    ],
    "conformance": [
        "gap-analysis.md",
    ],
}


def is_output_empty():
    """output/ 디렉토리가 없거나 실질적으로 비어있는지 확인."""
    if not os.path.isdir(OUTPUT_DIR):
        return True
    # progress.md만 있거나 완전히 비어있으면 아직 시작 전으로 간주
    entries = [
        e for e in os.listdir(OUTPUT_DIR)
        if e != "progress.md" and not e.startswith(".")
    ]
    return len(entries) == 0


def check_chapter(chapter, files):
    """
    챕터 디렉토리를 검사하여 (존재하는 파일 수, 전체 파일 수, 누락 목록) 반환.
    챕터 디렉토리 자체가 없으면 None 반환 (아직 진행 전).
    """
    chapter_dir = os.path.join(OUTPUT_DIR, chapter)
    if not os.path.isdir(chapter_dir):
        return None  # 아직 진행하지 않은 챕터

    missing = []
    empty = []
    for f in files:
        path = os.path.join(chapter_dir, f)
        if not os.path.isfile(path):
            missing.append(f)
        elif os.path.getsize(path) == 0:
            empty.append(f)

    present = len(files) - len(missing)
    issues = missing + empty
    return present, len(files), issues


def check_sbom_cdx():
    """output/sbom/에 *.cdx.json 파일이 하나 이상 있는지 확인."""
    sbom_dir = os.path.join(OUTPUT_DIR, "sbom")
    if not os.path.isdir(sbom_dir):
        return None  # sbom 챕터 자체가 없음
    cdx_files = glob.glob(os.path.join(sbom_dir, "*.cdx.json"))
    return len(cdx_files)


def main():
    print("[output 산출물 검증]")

    if is_output_empty():
        print("  SKIP: output/ 디렉토리가 없거나 비어있음 (아직 진행 전 — 정상)")
        sys.exit(0)

    fail_count = 0
    checked_count = 0

    for chapter, files in CHAPTER_FILES.items():
        result = check_chapter(chapter, files)
        if result is None:
            # 아직 해당 챕터 진행 안 함 → 검증 대상 아님
            continue

        present, total, issues = result
        checked_count += 1

        if not issues:
            print(f"  {chapter}/: 완료 ({present}/{total})")
        else:
            missing_files = [f for f in issues if not os.path.isfile(
                os.path.join(OUTPUT_DIR, chapter, f)
            )]
            empty_files = [f for f in issues if f not in missing_files]

            status_parts = []
            if missing_files:
                status_parts.append("누락: " + ", ".join(missing_files))
            if empty_files:
                status_parts.append("빈 파일: " + ", ".join(empty_files))

            print(f"  {chapter}/: 부분 완료 ({present}/{total}) — {'; '.join(status_parts)}")
            fail_count += 1

    # sbom CDX 파일 별도 확인
    cdx_count = check_sbom_cdx()
    if cdx_count is not None:
        if cdx_count == 0:
            print("  sbom/*.cdx.json: FAIL — .cdx.json 파일 없음 (SBOM 생성 필요)")
            fail_count += 1
        else:
            print(f"  sbom/*.cdx.json: 완료 ({cdx_count}개 발견)")

    if checked_count == 0:
        print("  SKIP: 검증할 챕터 산출물 없음 (정상)")
        sys.exit(0)

    if fail_count == 0:
        print(f"  PASS: 모든 챕터 산출물 완전")
        sys.exit(0)
    else:
        print(f"  FAIL: {fail_count}개 챕터 산출물 미완료")
        sys.exit(1)


if __name__ == "__main__":
    main()
