#!/usr/bin/env python3
"""
test-agent-specs.py — Agent CLAUDE.md 스펙 구조 검증 (Layer 1)

각 셀프스터디 agent의 CLAUDE.md를 파싱하여:
1. 필수 섹션 존재 여부 확인 (세션 시작 동작, 입력 질문, 출력 산출물)
2. 출력 산출물 선언과 validate-output.py 필수 파일 목록 정합성 확인
3. 참조된 templates/ 파일 실제 존재 여부 확인 (WARNING 처리)

verify.sh [10/11]에서 호출되며, 독립 실행도 가능.
"""

import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

# 검증 대상 셀프스터디 agent 목록 (순서 유지)
AGENTS = [
    "02-organization-designer",
    "03-policy-generator",
    "04-process-designer",
    "05-sbom-guide",
    "05-sbom-analyst",
    "05-sbom-management",
    "05-vulnerability-analyst",
    "06-training-manager",
    "07-conformance-preparer",
]

# 각 agent의 CLAUDE.md에 선언되어야 할 필수 output 파일명
# validate-output.py CHAPTER_FILES + agent 선언 파일 기반
AGENT_REQUIRED_OUTPUTS = {
    "02-organization-designer": [
        "role-definition.md",
        "raci-matrix.md",
        "appointment-template.md",
    ],
    "03-policy-generator": [
        "oss-policy.md",
        "license-allowlist.md",
    ],
    "04-process-designer": [
        "usage-approval.md",
        "distribution-checklist.md",
        "vulnerability-response.md",
        "inquiry-response.md",
        "process-diagram.md",
    ],
    "05-sbom-guide": [],  # .cdx.json은 동적 파일명 — 별도 확인
    "05-sbom-analyst": [
        "license-report.md",
        "copyleft-risk.md",
    ],
    "05-sbom-management": [
        "sbom-management-plan.md",
        "sbom-sharing-template.md",
    ],
    "05-vulnerability-analyst": [
        "cve-report.md",
        "remediation-plan.md",
    ],
    "06-training-manager": [
        "curriculum.md",
        "completion-tracker.md",
    ],
    "07-conformance-preparer": [
        "gap-analysis.md",
        "declaration-draft.md",
        "submission-guide.md",
    ],
}

# 각 agent가 참조하는 template 파일 목록 (미존재 시 WARNING)
AGENT_TEMPLATE_FILES = {
    "02-organization-designer": [
        "templates/organization/role-definition.md",
        "templates/organization/raci-matrix.md",
        "templates/organization/appointment-template.md",
    ],
    "03-policy-generator": [
        "templates/policy/oss-policy.md",
        "templates/policy/license-allowlist.md",
    ],
    "04-process-designer": [
        "templates/process/usage-approval.md",
        "templates/process/distribution-checklist.md",
        "templates/process/vulnerability-response.md",
        "templates/process/inquiry-response.md",
        "templates/process/contribution-process.md",
        "templates/process/project-publication-process.md",
    ],
    "05-sbom-guide": [],
    "05-sbom-analyst": [],
    "05-sbom-management": [],
    "05-vulnerability-analyst": [],
    "06-training-manager": [
        "templates/training/curriculum.md",
        "templates/training/completion-tracker.md",
    ],
    "07-conformance-preparer": [
        "templates/conformance/gap-analysis.md",
        "templates/conformance/declaration-draft.md",
        "templates/conformance/submission-guide.md",
    ],
}

# 각 agent CLAUDE.md에 반드시 포함되어야 할 구문
REQUIRED_PHRASES = [
    "세션 시작 시 동작",  # 자동 시작 행동 선언
    "## 입력 질문",       # 질문 섹션
    "## 출력 산출물",     # 출력 파일 선언
]


def extract_declared_output_files(content):
    """
    CLAUDE.md의 '## 출력 산출물' 코드블록에서 파일명 목록 추출.
    트리 구조(├── *.md, └── *.md)와 일반 파일 경로 모두 처리.
    """
    output_section = re.search(
        r"## 출력 산출물(.*?)(?=\n## |\Z)", content, re.DOTALL
    )
    if not output_section:
        return []

    section_text = output_section.group(1)

    # 코드 블록 안에서만 탐색
    code_block = re.search(r"```(.*?)```", section_text, re.DOTALL)
    if not code_block:
        return []

    block_text = code_block.group(1)

    # 파일명 패턴: .md, .json, .sh 확장자를 가진 파일
    filenames = re.findall(r"[\w\[\]-]+\.(?:md|json|sh)", block_text)
    return filenames


def check_agent(agent_name):
    """단일 agent 검증. (passes, fails, warns) 반환."""
    agent_dir = os.path.join(PROJECT_ROOT, "agents", agent_name)
    claude_md = os.path.join(agent_dir, "CLAUDE.md")

    passes = []
    fails = []
    warns = []

    # 검증 1: CLAUDE.md 존재
    if not os.path.isfile(claude_md):
        fails.append(f"CLAUDE.md 없음: agents/{agent_name}/CLAUDE.md")
        return passes, fails, warns

    with open(claude_md, encoding="utf-8") as f:
        content = f.read()

    # 검증 2: 필수 구문 존재 여부
    for phrase in REQUIRED_PHRASES:
        if phrase in content:
            passes.append(f"필수 구문 확인: '{phrase}'")
        else:
            fails.append(f"필수 구문 누락: '{phrase}'")

    # 검증 3: 출력 산출물 선언 정합성
    declared_files = extract_declared_output_files(content)
    declared_lower = [f.lower() for f in declared_files]

    required_files = AGENT_REQUIRED_OUTPUTS.get(agent_name, [])
    if not required_files:
        passes.append("출력 파일 선언 검사 SKIP (동적 파일명)")
    else:
        for req_file in required_files:
            if req_file.lower() in declared_lower:
                passes.append(f"출력 선언 확인: {req_file}")
            else:
                fails.append(f"출력 산출물 미선언: {req_file}")

    # 검증 4: template 파일 실제 존재 여부 (WARNING)
    for tpl_rel in AGENT_TEMPLATE_FILES.get(agent_name, []):
        tpl_path = os.path.join(PROJECT_ROOT, tpl_rel)
        if os.path.isfile(tpl_path):
            passes.append(f"템플릿 존재: {tpl_rel}")
        else:
            warns.append(f"템플릿 파일 없음 (agent가 동적 생성할 수 있음): {tpl_rel}")

    return passes, fails, warns


def main():
    print("[Agent 스펙 구조 검증]")

    total_pass = 0
    total_fail = 0
    total_warn = 0

    for agent in AGENTS:
        passes, fails, warns = check_agent(agent)
        total_pass += len(passes)
        total_fail += len(fails)
        total_warn += len(warns)

        if not fails and not warns:
            print(f"  [PASS] {agent}: {len(passes)}개 항목 통과")
        elif not fails:
            print(f"  [WARN] {agent}: {len(passes)}개 통과, 경고 {len(warns)}개")
            for w in warns:
                print(f"         ⚠ {w}")
        else:
            print(f"  [FAIL] {agent}: {len(passes)}개 통과, 실패 {len(fails)}개")
            for f in fails:
                print(f"         ✗ {f}")
            for w in warns:
                print(f"         ⚠ {w}")

    print()
    if total_fail == 0:
        if total_warn > 0:
            print(
                f"  PASS: 모든 Agent 스펙 구조 유효 (경고 {total_warn}개 — 확인 권장)"
            )
        else:
            print("  PASS: 모든 Agent 스펙 구조 유효")
        sys.exit(0)
    else:
        print(f"  FAIL: {total_fail}개 구조 오류 발견")
        sys.exit(1)


if __name__ == "__main__":
    main()
