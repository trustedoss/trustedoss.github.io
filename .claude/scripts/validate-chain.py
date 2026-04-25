#!/usr/bin/env python3
"""
validate-chain.py — agent 체인 전제 조건 연결 검증

output/ 또는 output-sample/ 디렉토리를 대상으로 각 agent 전환 지점의
전제 조건 파일이 실제로 존재하는지 확인한다.

사용법:
  python3 .claude/scripts/validate-chain.py                  # output-sample/ 검증
  python3 .claude/scripts/validate-chain.py --dir output/    # output/ 검증
  python3 .claude/scripts/validate-chain.py --agent 05-sbom-analyst
"""

import argparse
import glob
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 체인 스펙: 각 agent가 의존하는 전제 조건 파일
# OpenWave 프로필 기준 (기여 계획 있음 → contribution-process.md 포함)
CHAIN_SPEC = [
    {
        "agent": "02-organization-designer",
        "inputs": [],
        "outputs": [
            "organization/role-definition.md",
            "organization/raci-matrix.md",
            "organization/appointment-template.md",
        ],
        "conditional_outputs": [],
    },
    {
        "agent": "03-policy-generator",
        "inputs": [
            "organization/role-definition.md",
        ],
        "outputs": [
            "policy/oss-policy.md",
            "policy/license-allowlist.md",
        ],
        "conditional_outputs": [],
    },
    {
        "agent": "04-process-designer",
        "inputs": [
            "policy/oss-policy.md",
            "organization/role-definition.md",
        ],
        "outputs": [
            "process/usage-approval.md",
            "process/distribution-checklist.md",
            "process/vulnerability-response.md",
            "process/inquiry-response.md",
            "process/process-diagram.md",
        ],
        "conditional_outputs": [
            {
                "file": "process/contribution-process.md",
                "condition": "기여 계획 있음 (Q5=예) — 없으면 WARNING",
            }
        ],
    },
    {
        "agent": "05-sbom-guide",
        "inputs": [],
        "glob_outputs": ["sbom/*.cdx.json"],
        "outputs": [],
        "conditional_outputs": [],
    },
    {
        "agent": "05-sbom-analyst",
        "inputs": [],
        "glob_inputs": ["sbom/*.cdx.json"],
        "outputs": [
            "sbom/license-report.md",
            "sbom/copyleft-risk.md",
        ],
        "conditional_outputs": [],
    },
    {
        "agent": "05-sbom-management",
        "inputs": [
            "sbom/license-report.md",
        ],
        "glob_inputs": ["sbom/*.cdx.json"],
        "outputs": [
            "sbom/sbom-management-plan.md",
            "sbom/sbom-sharing-template.md",
        ],
        "conditional_outputs": [],
    },
    {
        "agent": "05-vulnerability-analyst",
        "inputs": [
            "sbom/sbom-management-plan.md",
        ],
        "glob_inputs": ["sbom/*.cdx.json"],
        "outputs": [
            "vulnerability/cve-report.md",
            "vulnerability/remediation-plan.md",
        ],
        "conditional_outputs": [],
    },
    {
        "agent": "06-training-manager",
        "inputs": [
            "policy/oss-policy.md",
            "organization/role-definition.md",
        ],
        "outputs": [
            "training/curriculum.md",
            "training/completion-tracker.md",
            "training/resources.md",
        ],
        "conditional_outputs": [],
    },
    {
        "agent": "07-conformance-preparer",
        "inputs": [
            "organization/role-definition.md",
            "organization/raci-matrix.md",
            "organization/appointment-template.md",
            "policy/oss-policy.md",
            "policy/license-allowlist.md",
            "process/usage-approval.md",
            "process/distribution-checklist.md",
            "process/vulnerability-response.md",
            "process/inquiry-response.md",
            "process/process-diagram.md",
            "sbom/sbom-management-plan.md",
            "sbom/license-report.md",
            "sbom/copyleft-risk.md",
            "sbom/sbom-sharing-template.md",
            "vulnerability/cve-report.md",
            "vulnerability/remediation-plan.md",
            "training/curriculum.md",
            "training/completion-tracker.md",
        ],
        "glob_inputs": ["sbom/*.cdx.json"],
        "outputs": [
            "conformance/gap-analysis.md",
            "conformance/declaration-draft.md",
            "conformance/submission-guide.md",
        ],
        "conditional_outputs": [],
    },
]


def resolve(base_dir: str, rel: str) -> str:
    return os.path.join(base_dir, rel)


def check_agent(spec: dict, base_dir: str, verbose: bool = True) -> tuple[int, int, int]:
    """(passes, fails, warns) 반환."""
    agent = spec["agent"]
    passes, fails, warns = 0, 0, 0

    # 전제 조건 (inputs) 확인
    for f in spec.get("inputs", []):
        path = resolve(base_dir, f)
        if os.path.exists(path):
            passes += 1
            if verbose:
                print(f"    전제조건 존재: {f}")
        else:
            fails += 1
            print(f"    FAIL 전제조건 누락: {f}")

    # glob 전제 조건
    for pattern in spec.get("glob_inputs", []):
        matches = glob.glob(resolve(base_dir, pattern))
        if matches:
            passes += 1
            if verbose:
                print(f"    전제조건 존재 (glob): {pattern} → {len(matches)}개")
        else:
            fails += 1
            print(f"    FAIL 전제조건 누락 (glob): {pattern}")

    # 출력 파일 확인
    for f in spec.get("outputs", []):
        path = resolve(base_dir, f)
        if os.path.exists(path):
            passes += 1
            if verbose:
                print(f"    출력 존재: {f}")
        else:
            fails += 1
            print(f"    FAIL 출력 누락: {f}")

    # glob 출력 파일
    for pattern in spec.get("glob_outputs", []):
        matches = glob.glob(resolve(base_dir, pattern))
        if matches:
            passes += 1
            if verbose:
                print(f"    출력 존재 (glob): {pattern} → {len(matches)}개")
        else:
            fails += 1
            print(f"    FAIL 출력 누락 (glob): {pattern}")

    # 조건부 출력 (WARNING)
    for cond in spec.get("conditional_outputs", []):
        path = resolve(base_dir, cond["file"])
        if os.path.exists(path):
            passes += 1
            if verbose:
                print(f"    조건부 출력 존재: {cond['file']}")
        else:
            warns += 1
            print(f"    WARN 조건부 출력 없음: {cond['file']} ({cond['condition']})")

    return passes, fails, warns


def run(base_dir: str, agent_filter: str = None, verbose: bool = True) -> bool:
    print(f"[체인 연결 검증] 대상: {base_dir}")
    print()

    total_pass = total_fail = total_warn = 0
    specs = [s for s in CHAIN_SPEC if agent_filter is None or s["agent"] == agent_filter]

    if not specs:
        print(f"  ERROR: agent '{agent_filter}' 를 찾을 수 없습니다.")
        return False

    for spec in specs:
        agent = spec["agent"]
        p, f, w = check_agent(spec, base_dir, verbose)
        total_pass += p
        total_fail += f
        total_warn += w

        status = "PASS" if f == 0 else "FAIL"
        warn_note = f" (경고 {w}개)" if w else ""
        print(f"  [{status}] {agent}: {p}개 통과, {f}개 실패{warn_note}")
        print()

    print("─" * 50)
    if total_fail == 0:
        warn_note = f" (경고 {total_warn}개)" if total_warn else ""
        print(f"  PASS: 체인 연결 이상 없음{warn_note}")
        return True
    else:
        print(f"  FAIL: {total_fail}개 체인 연결 이슈 발견")
        return False


def main():
    parser = argparse.ArgumentParser(description="agent 체인 전제 조건 연결 검증")
    parser.add_argument(
        "--dir",
        default="output-sample",
        help="검증할 output 디렉토리 (기본값: output-sample)",
    )
    parser.add_argument("--agent", help="특정 agent만 검증 (예: 05-sbom-analyst)")
    parser.add_argument("-v", "--verbose", action="store_true", help="상세 출력")
    args = parser.parse_args()

    base_dir = os.path.join(PROJECT_ROOT, args.dir)
    if not os.path.isdir(base_dir):
        print(f"ERROR: 디렉토리 없음: {base_dir}")
        sys.exit(1)

    ok = run(base_dir, agent_filter=args.agent, verbose=args.verbose)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
