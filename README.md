[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![OpenChain](https://img.shields.io/badge/OpenChain-ISO%2FIEC%205230%20%26%2018974-blue)](https://www.openchainproject.org/conformance)

# trustedoss

소프트웨어 공급망 보안과 오픈소스 관리 체계를 처음부터 완성까지 — ISO/IEC 5230 & 18974 실전 키트

오픈소스 관리 경험이 전혀 없는 신규 담당자도 이 키트를 따라가면 ISO/IEC 5230과 18974 자체 인증 선언까지 완성할 수 있습니다. Agent가 회사 상황에 맞는 산출물을 자동 생성하며, 셀프스터디 방식으로 활용할 수 있습니다.

---

## 빠른 시작

```bash
# 1. 저장소 클론
git clone https://github.com/haksungjang/trustedoss.git

# 2. 프로젝트 진입 및 Claude Code 실행
cd trustedoss && claude

# 3. 시작 안내 요청
# "어디서 시작해야 해?" 입력
```

---

## 저장소 구조

```
trustedoss/
├── docs/          # 챕터별 가이드 문서 (핵심)
├── agents/        # 산출물 자동 생성 Agent
├── templates/     # 문서 템플릿
├── samples/       # 실습용 샘플 프로젝트 (Log4Shell 등)
├── output/        # 생성된 산출물 (.gitignore, 직접 편집)
├── .claude/       # Claude Code 설정 및 skills
└── website/       # 문서 웹사이트 소스 (Docusaurus — 체계 구축과 무관)
```

> `website/`는 이 문서를 웹사이트로 배포하기 위한 코드입니다. 체계 구축 작업과 무관하며,
> `claude` 실행 시 자동으로 제외됩니다 (`.claudeignore` 적용).

---

## 전체 챕터 목록

| 챕터 | 내용 | 셀프스터디 |
|------|------|---------|
| 00-overview | 두 표준 개요 및 체크리스트 매핑 | 1시간 | 
| 00-overview/supply-chain | 소프트웨어 공급망 보안 + SBOM 개념 | 1시간 |
| 01-setup | 환경 준비 (Docker, Git, Claude Code) | 30분 |
| 02-organization | 조직 구성 및 담당자 지정 | 1시간 |
| 03-policy | 오픈소스 정책 수립 | 1시간 |
| 04-process | 오픈소스 프로세스 설계 | 1시간 |
| 05-tools/sbom-generation | SBOM 생성 | 1시간 |
| 05-tools/sbom-management | SBOM 관리 및 공유 | 1시간 |
| 05-tools/vulnerability | 취약점 분석 및 대응 | 1시간 |
| 06-training | 교육 체계 구축 | 30분 | 
| 07-conformance | 자체 인증 선언 | 30분 |

---

## 최종 산출물 목록

| 파일 | 설명 | 충족 표준 |
|------|------|---------|
| `output/organization/role-definition.md` | 오픈소스 담당자 역할 정의 | 5230 + 18974 |
| `output/organization/raci-matrix.md` | 역할·책임 매트릭스 | 5230 + 18974 |
| `output/organization/appointment-template.md` | 담당자 지정 공문 템플릿 | 5230 + 18974 |
| `output/policy/oss-policy.md` | 오픈소스 정책 문서 | 5230 + 18974 |
| `output/policy/license-allowlist.md` | 허용 라이선스 목록 | 5230 |
| `output/process/usage-approval.md` | 오픈소스 사용 승인 절차 | 5230 |
| `output/process/distribution-checklist.md` | 배포 전 체크리스트 | 5230 |
| `output/process/vulnerability-response.md` | 취약점 대응 절차 | 18974 |
| `output/process/process-diagram.md` | 전체 프로세스 다이어그램 | 5230 + 18974 |
| `output/sbom/[project].cdx.json` | SBOM (CycloneDX 형식) | 5230 + 18974 |
| `output/sbom/sbom-commands.sh` | SBOM 생성 명령어 스크립트 | 5230 + 18974 |
| `output/sbom/license-report.md` | 라이선스 분석 리포트 | 5230 |
| `output/sbom/copyleft-risk.md` | Copyleft 위험 분석 | 5230 |
| `output/sbom/sbom-management-plan.md` | SBOM 관리 계획 | 18974 |
| `output/sbom/sbom-sharing-template.md` | SBOM 공유 템플릿 | 18974 |
| `output/vulnerability/cve-report.md` | CVE 취약점 분석 리포트 | 18974 |
| `output/vulnerability/remediation-plan.md` | 취약점 대응 계획 | 18974 |
| `output/training/curriculum.md` | 교육 커리큘럼 | 5230 + 18974 |
| `output/training/completion-tracker.md` | 교육 이수 추적표 | 5230 + 18974 |
| `output/training/resources.md` | 교육 자료 목록 | 5230 + 18974 |
| `output/conformance/gap-analysis.md` | 갭 분석 보고서 | 5230 + 18974 |
| `output/conformance/declaration-draft.md` | 자체 인증 선언문 초안 | 5230 + 18974 |
| `output/conformance/submission-guide.md` | 인증 등록 안내 | 5230 + 18974 |

---

## Agent 목록

| Agent | 역할 | 생성 산출물 |
|-------|------|---------|
| `agents/02-organization-designer` | 조직/담당자 산출물 생성 | role-definition, raci-matrix, appointment-template |
| `agents/03-policy-generator` | 오픈소스 정책 문서 생성 | oss-policy, license-allowlist |
| `agents/04-process-designer` | 프로세스 문서 및 흐름도 생성 | usage-approval, distribution-checklist, vulnerability-response, process-diagram |
| `agents/05-sbom-guide` | SBOM 생성 명령어 및 스크립트 | [project].cdx.json, sbom-commands.sh |
| `agents/05-sbom-analyst` | SBOM 라이선스 분석 리포트 | license-report, copyleft-risk |
| `agents/05-sbom-management` | SBOM 관리 계획 및 공유 템플릿 | sbom-management-plan, sbom-sharing-template |
| `agents/05-vulnerability-analyst` | 취약점 분석 리포트 | cve-report, remediation-plan |
| `agents/06-training-manager` | 교육 커리큘럼 및 이수 추적 | curriculum, completion-tracker, resources |
| `agents/07-conformance-preparer` | 갭 분석 및 인증 선언문 | gap-analysis, declaration-draft, submission-guide |

---

## 관련 링크

- [OpenChain KWG](https://openchain-project.github.io/OpenChain-KWG/)
- [ISO/IEC 5230](https://www.iso.org/standard/81039.html)
- [ISO/IEC 18974](https://www.iso.org/standard/86450.html)
- [OpenChain 자체 인증 등록](https://www.openchainproject.org/conformance)

---

## 기여 방법

OpenChain KWG 커뮤니티와 연계하여 운영됩니다. PR과 이슈 제출을 환영합니다.

---

## 라이선스

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
