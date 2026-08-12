#!/usr/bin/env python3
"""
test-agent-specs.py — Agent CLAUDE.md 스펙 구조 검증 (Layer 1)

각 셀프스터디 agent의 CLAUDE.md를 파싱하여:
1. 필수 섹션 존재 여부 확인 (세션 시작 동작, 입력 질문, 출력 산출물)
2. 출력 산출물 선언과 validate-output.py 필수 파일 목록 정합성 확인
3. 참조된 templates/ 파일 실제 존재 여부 확인 (WARNING 처리)
4. 한국어 트리(agents/)와 영어 트리(agents/en/)의 파일 패리티 확인

한국어 트리와 영어 트리를 같은 기준으로 검사한다. 섹션 헤더 문자열만 트리마다
다르므로 TREES 에서 언어별 문구를 정의한다.

verify.sh [10/13]에서 호출되며, 독립 실행도 가능.
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

# 체인 밖 독립 도구 agent 목록 (DevSecOps·AI 코딩 트랙)
# 출력 산출물이 선택 조합에 따라 달라지므로 필수 섹션 존재 여부만 검증한다.
TOOL_AGENTS = [
    "ai-coding-setup",
    "devsecops-setup",
    "iac-fixer",
    "sast-analyst",
    "sbom-vuln-analyst",
    "secret-analyst",
    "level2-automation/issue-tracker",
    "level2-automation/pr-comment",
]

# 언어 트리 정의. prefix 는 agents/ 하위 경로, tpl_prefix 는 레포 루트 기준 템플릿 경로.
TREES = [
    {
        "name": "ko",
        "prefix": "",
        "tpl_prefix": "templates/",
        "phrases": [
            "세션 시작 시 동작",  # 자동 시작 행동 선언
            "## 입력 질문",  # 질문 섹션
            "## 출력 산출물",  # 출력 파일 선언
        ],
        "output_heading": "## 출력 산출물",
    },
    {
        "name": "en",
        "prefix": "en/",
        "tpl_prefix": "templates/en/",
        "phrases": [
            "Behavior on session start",
            "## Input questions",
            "## Output deliverables",
        ],
        "output_heading": "## Output deliverables",
    },
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
# 경로는 카테고리부터 적는다. 트리별 접두사(templates/ 또는 templates/en/)를 앞에 붙인다.
AGENT_TEMPLATE_FILES = {
    "02-organization-designer": [
        "organization/role-definition.md",
        "organization/raci-matrix.md",
        "organization/appointment-template.md",
    ],
    "03-policy-generator": [
        "policy/oss-policy.md",
        "policy/license-allowlist.md",
    ],
    "04-process-designer": [
        "process/usage-approval.md",
        "process/distribution-checklist.md",
        "process/vulnerability-response.md",
        "process/inquiry-response.md",
        "process/contribution-process.md",
        "process/project-publication-process.md",
    ],
    "05-sbom-guide": [],
    "05-sbom-analyst": [],
    "05-sbom-management": [],
    "05-vulnerability-analyst": [],
    "06-training-manager": [
        "training/curriculum.md",
        "training/completion-tracker.md",
    ],
    "07-conformance-preparer": [
        "conformance/gap-analysis.md",
        "conformance/declaration-draft.md",
        "conformance/submission-guide.md",
    ],
}


def extract_declared_output_files(content, heading):
    """
    CLAUDE.md의 출력 산출물 섹션 코드블록에서 파일명 목록 추출.
    트리 구조(├── *.md, └── *.md)와 일반 파일 경로 모두 처리.
    """
    output_section = re.search(
        rf"{re.escape(heading)}(.*?)(?=\n## |\Z)", content, re.DOTALL
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


def check_agent(agent_name, tree):
    """단일 agent 검증. (passes, fails, warns) 반환."""
    rel_dir = os.path.join("agents", tree["prefix"] + agent_name)
    claude_md = os.path.join(PROJECT_ROOT, rel_dir, "CLAUDE.md")

    passes = []
    fails = []
    warns = []

    # 검증 1: CLAUDE.md 존재
    if not os.path.isfile(claude_md):
        fails.append(f"CLAUDE.md 없음: {rel_dir}/CLAUDE.md")
        return passes, fails, warns

    with open(claude_md, encoding="utf-8") as f:
        content = f.read()

    # 검증 2: 필수 구문 존재 여부
    for phrase in tree["phrases"]:
        if phrase in content:
            passes.append(f"필수 구문 확인: '{phrase}'")
        else:
            fails.append(f"필수 구문 누락: '{phrase}'")

    # 검증 3: 출력 산출물 선언 정합성
    declared_files = extract_declared_output_files(content, tree["output_heading"])
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
        tpl_path = os.path.join(PROJECT_ROOT, tree["tpl_prefix"] + tpl_rel)
        if os.path.isfile(tpl_path):
            passes.append(f"템플릿 존재: {tree['tpl_prefix'] + tpl_rel}")
        else:
            warns.append(
                f"템플릿 파일 없음 (agent가 동적 생성할 수 있음): {tree['tpl_prefix'] + tpl_rel}"
            )

    return passes, fails, warns


def check_tool_agent(agent_name, tree):
    """체인 밖 도구 agent 검증 — 필수 섹션 구문만 확인. (passes, fails, warns) 반환."""
    rel_dir = os.path.join("agents", tree["prefix"] + agent_name)
    claude_md = os.path.join(PROJECT_ROOT, rel_dir, "CLAUDE.md")

    passes = []
    fails = []
    warns = []

    if not os.path.isfile(claude_md):
        fails.append(f"CLAUDE.md 없음: {rel_dir}/CLAUDE.md")
        return passes, fails, warns

    with open(claude_md, encoding="utf-8") as f:
        content = f.read()

    for phrase in tree["phrases"]:
        if phrase in content:
            passes.append(f"필수 구문 확인: '{phrase}'")
        else:
            fails.append(f"필수 구문 누락: '{phrase}'")

    return passes, fails, warns


def collect_md(base_rel, skip_dirs):
    """base_rel 하위 .md 파일을 base 기준 상대 경로 집합으로 수집."""
    base = os.path.join(PROJECT_ROOT, base_rel)
    found = set()
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for name in files:
            if not name.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, name), base)
            found.add(rel)
    return found


def check_tree_parity():
    """한국어 트리와 영어 트리의 파일 목록 패리티 확인. (fails,) 반환."""
    fails = []
    for base in ("agents", "templates"):
        ko = collect_md(base, skip_dirs={"en"})
        en = collect_md(os.path.join(base, "en"), skip_dirs=set())
        for missing in sorted(ko - en):
            fails.append(f"영문 누락: {base}/en/{missing}")
        for orphan in sorted(en - ko):
            fails.append(f"고아 영문 파일 (원본 {base}/{orphan} 없음): {base}/en/{orphan}")
    return fails


def main():
    print("[Agent 스펙 구조 검증]")

    total_pass = 0
    total_fail = 0
    total_warn = 0

    for tree in TREES:
        for agent in AGENTS + TOOL_AGENTS:
            if agent in TOOL_AGENTS:
                passes, fails, warns = check_tool_agent(agent, tree)
            else:
                passes, fails, warns = check_agent(agent, tree)
            total_pass += len(passes)
            total_fail += len(fails)
            total_warn += len(warns)

            label = f"[{tree['name']}] {agent}"
            if not fails and not warns:
                print(f"  [PASS] {label}: {len(passes)}개 항목 통과")
            elif not fails:
                print(f"  [WARN] {label}: {len(passes)}개 통과, 경고 {len(warns)}개")
                for w in warns:
                    print(f"         ⚠ {w}")
            else:
                print(f"  [FAIL] {label}: {len(passes)}개 통과, 실패 {len(fails)}개")
                for f in fails:
                    print(f"         ✗ {f}")
                for w in warns:
                    print(f"         ⚠ {w}")

    parity_fails = check_tree_parity()
    total_fail += len(parity_fails)
    if parity_fails:
        print(f"  [FAIL] ko/en 트리 패리티: 불일치 {len(parity_fails)}개")
        for f in parity_fails:
            print(f"         ✗ {f}")
    else:
        print("  [PASS] ko/en 트리 패리티: agents·templates 파일 목록 일치")

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
