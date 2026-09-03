---
id: agents
title: AI 에이전트로 산출물 만들기
sidebar_label: 에이전트 선택 가이드
sidebar_position: 4
description: '에이전트와 챕터, 산출물의 매핑과 상황별 선택 기준. 체계 구축 에이전트 9종과 자동화 에이전트 7종을 모두 다룹니다.'
---

# AI 에이전트로 산출물 만들기

Trusted OSS의 핵심은 AI 에이전트가 회사 상황을 묻고, OpenChain 표준에 맞는 산출물을 자동으로 만들어 준다는 점입니다. 빈 템플릿을 직접 채울 필요 없이, 질문에 답하면 우리 회사용 정책·프로세스·조직 문서가 생성됩니다. 이 페이지는 어떤 에이전트가 무엇을 만드는지 한눈에 보여줍니다.

에이전트는 두 갈래입니다. 체계 구축 에이전트는 자체 인증에 필요한 산출물을 만들고, 자동화 에이전트는 CI와 개발 도구에 정책을 적용하거나 스캔 결과를 분석합니다.

## 체계 구축 에이전트

[오픈소스 관리](/docs) 트랙의 챕터와 하나씩 대응합니다. 자체 인증이 목표라면 이 표의 순서대로 실행합니다.

| 챕터        | 에이전트 (`agents/…`)              | 생성 산출물                                                                                                                                    |
| ----------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| 2 조직      | `02-organization-designer`         | role-definition, raci-matrix, appointment-template                                                                                             |
| 3 정책      | `03-policy-generator`              | oss-policy, license-allowlist                                                                                                                  |
| 4 프로세스  | `04-process-designer`              | usage-approval, distribution-checklist, vulnerability-response, inquiry-response, process-diagram, (조건부) contribution / project-publication |
| 5 SBOM 생성 | `05-sbom-guide`, `05-sbom-analyst` | SBOM(cdx.json), sbom-commands, license-report, copyleft-risk                                                                                   |
| 5 SBOM 관리 | `05-sbom-management`               | sbom-management-plan, sbom-sharing-template                                                                                                    |
| 5 취약점    | `05-vulnerability-analyst`         | cve-report, remediation-plan                                                                                                                   |
| 6 교육      | `06-training-manager`              | curriculum, completion-tracker, resources                                                                                                      |
| 7 인증      | `07-conformance-preparer`          | gap-analysis, declaration-draft, submission-guide                                                                                              |

생성된 산출물의 실제 형태는 [정책 산출물 Best Practice](./samples/policy)에서 확인할 수 있습니다.

## 자동화 에이전트

정책을 세운 뒤 [DevSecOps](/devsecops/intro)와 [AI 코딩 거버넌스](/ai-coding/intro) 트랙에서 사용합니다. 설정 생성 에이전트는 프로젝트를 분석해 설정 파일을 만들고, 결과 분석 에이전트는 스캔 도구의 출력 파일을 받아 대응 리포트를 만듭니다.

| 갈래      | 에이전트 (`agents/…`) | 하는 일                                                                                         | 생성 산출물                                                                                                |
| --------- | --------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 설정 생성 | `ai-coding-setup`     | 프로젝트를 분석해 AI 코딩 도구용 Rules 파일 생성                                                | `output/ai-coding/` 아래 도구별 규칙 파일(CLAUDE.md, Cursor, Copilot, Devin Desktop)                       |
| 설정 생성 | `devsecops-setup`     | 프로젝트를 분석해 CI/CD 파이프라인 워크플로와 정책 파일 생성                                    | devsecops-pr.yml, devsecops-merge.yml, devsecops-schedule.yml, .gitlab-ci.yml, .gitleaks.toml, .grype.yaml |
| 설정 생성 | `level2-automation`   | 스캔 결과를 이슈로 등록(`issue-tracker`)하거나 PR 코멘트로 게시(`pr-comment`)하는 워크플로 생성 | GitHub Actions · GitLab CI 워크플로                                                                        |
| 결과 분석 | `sast-analyst`        | Semgrep·CodeQL SARIF 결과를 분석해 우선순위와 수정 코드 제시                                    | sast-report.md                                                                                             |
| 결과 분석 | `sbom-vuln-analyst`   | SBOM 파일이나 grype 스캔 결과를 분석해 취약점 대응 정리                                         | sbom-vuln-report.md, .grype.yaml 예외 처리 예시                                                            |
| 결과 분석 | `secret-analyst`      | Gitleaks 결과를 분석해 시크릿 유형별 즉시 대응 절차 제시                                        | secret-response-report.md, .gitleaks.toml 예외 처리 예시                                                   |
| 결과 분석 | `iac-fixer`           | Checkov 결과를 분석해 위반 항목별 수정된 IaC 코드 생성                                          | iac-fix-report.md                                                                                          |

:::warning 시크릿이 실제로 노출됐다면
`secret-analyst`로 분석하기 전에 해당 자격증명을 먼저 폐기하고 재발급하세요. 분석은 그다음입니다.
:::

## 어느 상황에 어느 에이전트

- **자체 인증이 목표라면** 2 조직 → 3 정책 → 4 프로세스 → 5 도구 → 6 교육 → 7 인증 순서로 각 에이전트를 실행합니다. 필수 경로입니다.
- **정책만 빠르게 필요하면** `03-policy-generator`부터 실행해도 됩니다.
- **SBOM·취약점만 점검하려면** 5 도구의 에이전트(`05-sbom-*`, `05-vulnerability-analyst`)만 사용합니다.
- **기여·사내 공개 절차가 필요하면** 4 프로세스 에이전트 실행 중 해당 질문에 "예"로 답하면 조건부 산출물이 함께 생성됩니다.
- **정책을 개발 도구에 적용하려면** `ai-coding-setup`으로 Rules 파일을, `devsecops-setup`으로 CI 워크플로를 만듭니다.
- **스캔은 이미 돌리고 있다면** 결과 파일 종류에 맞는 분석 에이전트를 씁니다. SARIF는 `sast-analyst`, SBOM과 grype 결과는 `sbom-vuln-analyst`, Gitleaks 결과는 `secret-analyst`, Checkov 결과는 `iac-fixer`입니다.

## 공통 실행 방법

모든 에이전트는 같은 방식으로 실행합니다.

:::tip 실행 전 확인
현재 Claude 세션을 먼저 종료(`/exit` 또는 `Ctrl+C`)한 뒤, 새 터미널에서 아래 명령을 실행하세요. `XX-agent-name` 자리에 위 표의 에이전트 이름을 넣습니다.
:::

```bash
cd agents/XX-agent-name
claude
```

프롬프트가 열리면 `시작`을 입력하고, 에이전트의 질문에 답하면 됩니다. 생성된 산출물은 `output/` 폴더에 저장됩니다.

`level2-automation`은 하위에 `issue-tracker`와 `pr-comment` 두 에이전트가 있으므로 한 단계 더 들어갑니다.

:::tip 실행 전 확인
현재 Claude 세션을 먼저 종료한 뒤 실행하세요.
:::

```bash
cd agents/level2-automation/issue-tracker
claude
```

## 다음 단계

- 아직 환경 설정 전이라면 [환경 준비](/docs/setup) 챕터부터 진행하세요.
- 무엇부터 할지 고르려면 [개요: 두 표준과 전체 여정](/docs)의 다음 단계 안내를 보세요.
