#!/usr/bin/env python3
"""
test-output-fixtures.py — 골든 픽스처 회귀 테스트 (Layer 2)

output-sample/을 임시 디렉토리에 복사하여 validate-output.py가 PASS하는지 검증한다.
output-sample/이 실제로 유효한 골든 픽스처임을 보장하며,
향후 agent 출력 변경 시 회귀를 탐지한다.

verify.sh [11/11]에서 호출되며, 독립 실행도 가능.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
OUTPUT_SAMPLE_DIR = os.path.join(PROJECT_ROOT, "output-sample")
VALIDATE_SCRIPT = os.path.join(SCRIPT_DIR, "validate-output.py")


def prepare_fixture(tmpdir):
    """
    output-sample/ → tmpdir/output/ 복사 후 자동 검증 불가 파일 보완.
    validate-output.py가 실제로 검사하는 파일만 보완한다.
    """
    output_dir = os.path.join(tmpdir, "output")

    if not os.path.isdir(OUTPUT_SAMPLE_DIR):
        print("  FAIL: output-sample/ 디렉토리 없음")
        return None

    shutil.copytree(OUTPUT_SAMPLE_DIR, output_dir)

    # sbom/*.cdx.json: validate-output.py가 존재 여부 확인
    # output-sample/에 실제 SBOM 파일이 없으면 최소 픽스처 생성
    sbom_dir = os.path.join(output_dir, "sbom")
    if os.path.isdir(sbom_dir):
        cdx_files = [f for f in os.listdir(sbom_dir) if f.endswith(".cdx.json")]
        if not cdx_files:
            mock_cdx = os.path.join(sbom_dir, "fixture-sample.cdx.json")
            with open(mock_cdx, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "bomFormat": "CycloneDX",
                        "specVersion": "1.4",
                        "version": 1,
                        "metadata": {"component": {"name": "fixture-sample"}},
                        "components": [],
                    },
                    f,
                    indent=2,
                )

    return output_dir


def run_validate(output_dir):
    """validate-output.py를 output_dir 대상으로 실행."""
    env = {**os.environ, "TRUSTEDOSS_OUTPUT_DIR": output_dir}
    result = subprocess.run(
        [sys.executable, VALIDATE_SCRIPT],
        env=env,
        capture_output=True,
        text=True,
    )
    return result


def check_fixture_completeness():
    """
    output-sample/의 파일이 각 챕터별 예상 파일을 포함하는지 확인.
    validate-output.py CHAPTER_FILES 기준.
    """
    CHAPTER_FILES = {
        "organization": [
            "role-definition.md",
            "raci-matrix.md",
            "appointment-template.md",
        ],
        "policy": ["oss-policy.md", "license-allowlist.md"],
        "process": [
            "usage-approval.md",
            "distribution-checklist.md",
            "vulnerability-response.md",
            "inquiry-response.md",
        ],
        "sbom": ["sbom-management-plan.md"],
        "vulnerability": ["cve-report.md", "remediation-plan.md"],
        "training": ["curriculum.md", "completion-tracker.md"],
        "conformance": ["gap-analysis.md"],
    }

    issues = []
    for chapter, files in CHAPTER_FILES.items():
        chapter_dir = os.path.join(OUTPUT_SAMPLE_DIR, chapter)
        if not os.path.isdir(chapter_dir):
            issues.append(f"output-sample/{chapter}/ 디렉토리 없음")
            continue
        for fname in files:
            fpath = os.path.join(chapter_dir, fname)
            if not os.path.isfile(fpath):
                issues.append(f"output-sample/{chapter}/{fname} 없음")
            elif os.path.getsize(fpath) == 0:
                issues.append(f"output-sample/{chapter}/{fname} 빈 파일")

    return issues


def main():
    print("[골든 픽스처 회귀 테스트]")

    # 1단계: output-sample/ 완전성 사전 확인
    print("  output-sample/ 완전성 확인 중...")
    completeness_issues = check_fixture_completeness()
    if completeness_issues:
        print(f"  [FAIL] output-sample/ 불완전 — {len(completeness_issues)}개 파일 누락:")
        for issue in completeness_issues:
            print(f"         ✗ {issue}")
        sys.exit(1)
    print("  output-sample/ 완전성 확인 완료")

    # 2단계: 임시 디렉토리에 픽스처 구성
    tmpdir = tempfile.mkdtemp(prefix="trustedoss-fixture-test-")
    try:
        output_dir = prepare_fixture(tmpdir)
        if output_dir is None:
            sys.exit(1)

        # 3단계: validate-output.py 실행
        print("  validate-output.py 실행 중...")
        result = run_validate(output_dir)

        # 결과 출력 (들여쓰기 보정)
        for line in result.stdout.strip().splitlines():
            print(f"  {line}")
        if result.stderr.strip():
            for line in result.stderr.strip().splitlines():
                print(f"  ERR: {line}")

        if result.returncode == 0:
            print()
            print("  PASS: output-sample/ 골든 픽스처 유효")
            sys.exit(0)
        else:
            print()
            print("  FAIL: output-sample/ 골든 픽스처 검증 실패")
            print("        output-sample/ 에 누락된 파일을 추가하거나")
            print("        validate-output.py CHAPTER_FILES를 확인하세요.")
            sys.exit(1)

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
