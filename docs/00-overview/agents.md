---
description: 'AI 에이전트가 회사 맞춤 오픈소스 산출물을 자동 생성합니다. 에이전트와 챕터, 산출물 매핑을 한눈에 봅니다.'
작성일: 2026-06-05
버전: 1.0
충족 체크리스트:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
셀프스터디 소요시간: 10분
sidebar_position: 7
sidebar_label: AI 에이전트로 산출물 만들기
---

# AI 에이전트로 산출물 만들기

TrustedOSS의 핵심은 **AI 에이전트가 회사 상황을 묻고, OpenChain 표준에 맞는 산출물을 자동으로 만들어 준다**는 점입니다. 빈 템플릿을 직접 채울 필요 없이, 질문에 답하면 우리 회사용 정책·프로세스·조직 문서가 생성됩니다. 이 페이지는 어떤 에이전트가 무엇을 만드는지 한눈에 보여줍니다.

## 에이전트 한눈에 보기

| 챕터        | 에이전트 (`agents/…`)              | 생성 산출물                                                                                                                   |
| ----------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 2 조직      | `02-organization-designer`         | role-definition, raci-matrix, appointment-template                                                                            |
| 3 정책      | `03-policy-generator`              | oss-policy, license-allowlist                                                                                                 |
| 4 프로세스  | `04-process-designer`              | usage-approval, distribution-checklist, vulnerability-response, inquiry-response, (조건부) contribution / project-publication |
| 5 SBOM 생성 | `05-sbom-guide`, `05-sbom-analyst` | SBOM(cdx.json), sbom-commands, license-report, copyleft-risk                                                                  |
| 5 SBOM 관리 | `05-sbom-management`               | sbom-management-plan, sbom-sharing-template                                                                                   |
| 5 취약점    | `05-vulnerability-analyst`         | cve-report, remediation-plan                                                                                                  |
| 6 교육      | `06-training-manager`              | curriculum, completion-tracker, resources                                                                                     |
| 7 인증      | `07-conformance-preparer`          | gap-analysis, declaration-draft, submission-guide                                                                             |

생성된 산출물의 실제 형태는 [정책 산출물 Best Practice](/reference/samples/policy)에서 확인할 수 있습니다.

## 어느 상황에 어느 에이전트

- **자체 인증이 목표라면** 2 조직 → 3 정책 → 4 프로세스 → 5 도구 → 6 교육 → 7 인증 순서로 각 에이전트를 실행합니다. 필수 경로입니다.
- **정책만 빠르게 필요하면** `03-policy-generator`부터 실행해도 됩니다.
- **SBOM·취약점만 점검하려면** 5 도구의 에이전트(`05-sbom-*`, `05-vulnerability-analyst`)만 사용합니다.
- **기여·사내 공개 절차가 필요하면** 4 프로세스 에이전트 실행 중 해당 질문에 "예"로 답하면 조건부 산출물이 함께 생성됩니다.

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

## 다음 단계

- 아직 환경 설정 전이라면 [환경 준비](../01-setup/index.md) 챕터부터 진행하세요.
- 무엇부터 할지 고르려면 [내게 맞는 시작 경로](./start-path.md)를 보세요.
