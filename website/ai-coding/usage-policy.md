---
id: usage-policy
title: 'AI 코딩 도구 사용 정책'
sidebar_label: 'AI 코딩 도구 사용 정책'
description: 조직이 허용할 AI 코딩 도구와 승인 기준, 보내도 되는 데이터, 역할과 책임, 교육 항목을 정하는 사용 정책 작성법을 설명합니다.
sidebar_position: 2
---

# AI 코딩 도구 사용 정책

:::info 이 페이지에서 정하는 것

- 허용할 도구와 플랜, 그 승인 기준
- 도구에 보내도 되는 데이터와 막아야 할 데이터
- 역할과 책임, 교육 항목
- 비용 한도와 정기 점검

대상은 정책 담당, 도구 관리자, 보안·법무 담당입니다. 개발자는 2절(데이터 취급)과 템플릿의 "작업 방식과 검증" 항목을 먼저 보면 됩니다.
:::

AI 코딩 도구를 쓰는 조직이 먼저 정해야 할 것은 도구 설정이 아니라 사용 기준입니다. 어떤 도구를
허용하는지, 어떤 코드와 데이터를 도구에 보내도 되는지, 누가 승인하고 누가 책임지는지, 사람들에게
무엇을 가르치는지, 비용을 어디까지 쓰는지입니다. 이 기준이 없으면 개인이 각자 고른 도구와 계정으로
일하게 되고, 이 섹션의 다른 통제인 Rules, CI(지속적 통합) 게이트, MCP(Model Context Protocol) 통제는 적용 대상부터 흔들립니다.

이 페이지는 그 기준을 한 문서로 묶습니다. 마지막 절의 정책 템플릿을 [오픈소스 정책](/docs/policy)에
추가하거나 별도 정책으로 채택할 수 있습니다.

:::note 법률 자문이 아닙니다
공급자 약관과 데이터 처리 조건은 2026-11 기준 공개 문서를 정리한 것입니다. 약관은 자주 바뀌므로
도입 시점에 원문을 다시 확인하세요.
:::

## 1. 도구 승인

### 승인 기준

도구를 허용 목록에 올리기 전에 아래 항목을 확인합니다. 같은 제품도 플랜에 따라 조건이 다르므로
제품이 아니라 "제품과 플랜" 단위로 승인합니다.

| 항목                | 확인할 내용                                                                                                                                     |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 데이터 처리         | 입력한 코드와 프롬프트를 모델 학습에 쓰지 않는가, 보존 기간은 얼마인가                                                                          |
| IP(지식재산권) 보증 | 생성물에 대한 저작권 침해 주장을 공급자가 방어하는가. [법적 고려 2절](./legal-considerations#2-공급자-ip-보증-침해-분쟁이-나면-누가-방어하는가) |
| 관리자 통제         | 조직 관리자가 설정을 강제할 수 있는가(개인이 덮어쓸 수 없는 정책)                                                                               |
| 기록                | 사용 기록과 감사 로그를 조직이 볼 수 있는가                                                                                                     |
| 비용 통제           | 조직 단위 사용량 한도와 알림을 걸 수 있는가                                                                                                     |
| 확장                | MCP 서버, 플러그인, 외부 연결을 관리자가 제한할 수 있는가. [에이전트와 MCP 도구 거버넌스](./agent-governance)                                   |

### 공급자별 데이터 처리 조건

아래는 업무용 플랜 기준입니다. 같은 공급자라도 개인 플랜은 조건이 다릅니다. 예를 들어 GitHub 는
2026-04-24부터 Copilot Free·Pro·Pro+ 사용자의 상호작용 데이터를 학습에 쓰며(사용자가 거부 가능),
Business 와 Enterprise 는 이 변경에서 제외됩니다.

| 도구                                      | 학습 사용               | 보존                                  | 관리자 강제            |
| ----------------------------------------- | ----------------------- | ------------------------------------- | ---------------------- |
| GitHub Copilot Business·Enterprise        | 안 함                   | github.com 채팅: 계정 유지 기간(주 1) | 정책 강제, 콘텐츠 제외 |
| Anthropic (Team·Enterprise·API)           | 안 함(주 2)             | 30일, ZDR 개별 적용                   | 관리 설정(주 2)        |
| OpenAI (ChatGPT Business·Enterprise, API) | 안 함                   | API 로그 최대 30일, ZDR 사전 승인     | 워크스페이스 설정      |
| Cursor (Teams·Enterprise)                 | Privacy Mode 에서 안 함 | Privacy Mode 에서 ZDR(주 3)           | Privacy Mode 강제      |
| Gemini Code Assist                        | 안 함                   | 명시 없음                             | 확인하지 못함          |

ZDR(Zero Data Retention)은 공급자가 입력과 출력을 저장하지 않는 무보존 옵션입니다. 표의 주는 다음과 같습니다.

1. 2026-09-28부터 바뀐 조건이며 이전에는 28일이었습니다. 엔터프라이즈 정책은 조직이 덮어쓸 수 없고,
   콘텐츠 제외는 저장소·경로 단위로 겁니다.
2. 고객이 별도 프로그램에 참여한 경우는 학습에 쓰일 수 있습니다. Claude Code 는 관리 설정
   (`managed-settings.json`)의 키를 사용자 설정으로 덮어쓸 수 없습니다.
3. 모델 공급자와 무보존 계약을 맺었지만 일부 모델은 예외입니다. 관리자가 Privacy Mode 를 켜면 구성원이
   끌 수 없습니다.

두 가지를 주의합니다. 첫째, GitHub 의 콘텐츠 제외는 에이전트가 파일을 간접적으로 읽는 경우를 놓칠 수
있고 운영체제 권한을 대신하지 않는다고 공식 문서가 밝힙니다. 둘째, Copilot 의 공개 코드 매칭 차단
정책은 Copilot CLI 에 적용되지 않고 클라우드 에이전트에서는 표시 모드로만 동작합니다. 도구를 승인할
때는 IDE(통합 개발 환경) 기능뿐 아니라 CLI(명령줄 인터페이스)와 에이전트 기능의 조건을 따로 확인해야 합니다.

### 승인되지 않은 도구

개인 계정이나 승인되지 않은 확장을 업무에 쓰는 것(섀도 AI)은 금지만으로 막기 어렵습니다. 승인된
도구가 없거나 쓰기 불편하면 사람들은 개인 계정으로 돌아갑니다. 승인 절차를 짧게 유지하고, 승인된
도구를 먼저 제공하는 편이 효과가 큽니다. 기술적으로는 사내 네트워크에서 승인되지 않은 AI 서비스
도메인을 막거나, IDE 확장 허용 목록을 관리하는 방법이 있습니다.

## 2. 데이터 취급

도구에 무엇을 보내도 되는지는 데이터 분류로 정합니다. 승인된 도구라도 보내지 말아야 할 데이터가
있습니다.

| 분류 | 예                                | 승인된 도구에 보내기                             |
| ---- | --------------------------------- | ------------------------------------------------ |
| 공개 | 공개 저장소 코드, 공개 문서       | 허용                                             |
| 사내 | 사내 저장소 코드, 설계 문서, 이슈 | 학습에 쓰지 않는 플랜이면 허용                   |
| 제한 | 고객 데이터, 개인정보, 운영 로그  | 원칙적으로 금지. 필요하면 가명 처리 후 별도 승인 |
| 비밀 | API 키, 토큰, 인증서, 비밀번호    | 금지. 에이전트 설정에서 읽기 자체를 차단         |

에이전트형 도구는 사람이 붙여 넣지 않아도 파일을 직접 읽습니다. 그래서 "보내지 않는다"는 규칙은
"읽지 못하게 한다"는 설정으로 옮겨야 지켜집니다. Claude Code 의 `permissions.deny` 로 `.env` 와
`secrets/` 읽기를 막는 예가 [ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.claude/settings.json)
에 있고, GitHub Copilot 은 저장소나 경로 단위의 콘텐츠 제외 설정을 제공합니다.

외부 문서와 시스템을 에이전트에 연결할 때도 같은 기준이 적용됩니다. 에이전트는 연결한 사람의 권한으로
읽으므로, 너무 넓게 공유된 문서는 에이전트도 그만큼 찾아냅니다. 연결하기 전에 공유 범위부터
정리합니다.

## 3. 역할과 책임

| 역할        | 맡는 일                                                                   |
| ----------- | ------------------------------------------------------------------------- |
| 정책 담당   | 사용 정책 작성·개정, 승인 목록 관리, 연 1회 재점검                        |
| 도구 관리자 | 관리자 설정 배포(관리 설정, 조직 정책), 계정과 라이선스, 비용 한도와 알림 |
| 보안 담당   | 도구·MCP 서버 도입 심사, 데이터 분류 판단, 사고 대응                      |
| 법무        | 공급자 약관과 IP 보증 검토, 저작권 귀속 판단, 외부 공개 전 검토           |
| 개발 팀장   | 팀 규칙 파일 담당, PR(pull request) 리뷰 기준과 승인 지점 운영            |
| 개발자      | 승인된 도구만 사용, AI 사용 기록, 생성된 코드에 대한 최종 책임            |

작은 조직은 한 사람이 여러 역할을 맡아도 됩니다. 다만 도구를 승인하는 사람과 그 도구로 만든 코드를
승인하는 사람이 같은 경우에는 리뷰 기록을 남겨 판단 근거가 보이게 합니다. 조직 설계에서 AI 코딩 도구
정책 담당을 어디에 두는지는 [조직 구성](/docs/organization)에서 다룹니다.

마지막 줄이 중요합니다. AI가 만든 코드라도 병합한 사람이 책임집니다. Linux 커널이 AI 에이전트의
`Signed-off-by` 를 금지하고 사람만 DCO(Developer Certificate of Origin, 기여자 출처 확인서)를 인증하게
한 것도 같은 원칙입니다([법적 고려 4절](./legal-considerations#4-상류-오픈소스-프로젝트의-ai-기여-정책)).

## 4. 교육과 인식

도구를 허용하는 것과 사람들이 그 도구를 안전하게 쓰는 것은 다릅니다. 신규 입사자 온보딩과 정기 교육에
아래 항목을 넣습니다.

- 승인된 도구와 플랜, 개인 계정 금지 이유
- 데이터 분류와 보내면 안 되는 데이터
- AI가 만든 코드의 흔한 결함: 취약한 패턴, 존재하지 않는 패키지 제안, 라이선스가 맞지 않는 코드
- 테스트를 먼저 정하고 구현을 맡기는 작업 방식([테스트 환경](./testing))
- AI 사용 기록 방법(커밋 메시지, PR 템플릿)
- 외부 오픈소스에 기여할 때 상류 프로젝트의 AI 정책 확인

EU 에서 AI 시스템을 제공하거나 업무에 쓰는 조직에는 교육이 법적 의무이기도 합니다. EU AI Act 제4조(AI
리터러시)는 2025-02-02부터 제공자와 배포자에게 적용됐습니다. Digital Omnibus on AI(Regulation (EU)
2026/1744, 2026-07-27 발효)가 이 조항을 고쳐, 제공자와 배포자는 직원의 AI 리터러시 향상을 지원하는
조치를 취해야 하되 특정 개인의 수준을 보장할 의무는 없다고 명시했습니다. 의무가 완화됐을 뿐 없어진
것은 아니므로, 교육 계획과 이수 기록은 그대로 근거로 쓰입니다.

교육 기록은 오픈소스 교육 기록과 같은 방식으로 남깁니다. [교육과 역량](/docs/training) 챕터의
산출물에 AI 코딩 항목을 추가하면 별도 체계를 만들 필요가 없습니다.

## 5. 비용 한도

에이전트형 도구는 사용량에 따라 비용이 크게 달라집니다. 에이전트 하나가 긴 작업을 반복하면 대화형
사용보다 훨씬 많은 토큰을 씁니다. 비용 한도를 정하지 않으면 청구서를 받은 뒤에야 사용 실태를 알게
됩니다.

- 조직 단위 월 한도와 사용자 또는 팀 단위 한도를 정합니다.
- 한도의 일정 비율(예: 80%, 100%)에서 알림이 가게 하고, 알림 받는 사람이 실제로 조치할 사람인지
  확인합니다.
- CI 에서 돌리는 AI 작업(AI 리뷰, AI 퍼징)은 전용 키를 쓰고 키마다 한도를 겁니다.

주요 도구의 비용 통제 기능은 다음과 같습니다(2026-11 확인).

| 도구                     | 한도 단위                                  | 확인할 점                                           |
| ------------------------ | ------------------------------------------ | --------------------------------------------------- |
| Claude (Team·Enterprise) | 조직, 그룹, 구성원                         | 사용 크레딧을 켜야 좌석 기본량을 넘어 계속 사용     |
| Claude API (Console)     | 워크스페이스                               | Claude Code 전용 워크스페이스가 따로 생김           |
| GitHub Copilot           | 사용자, 조직, 비용 센터, 엔터프라이즈      | 사용자 외 단위는 한도에서 멈추는 옵션이 기본값 꺼짐 |
| Cursor                   | 팀(고정 또는 좌석당), Enterprise 는 구성원 | 한도 적용에 지연이 있음                             |

GitHub Copilot 은 2026-06-01부터 premium request 대신 GitHub AI Credits 로 과금합니다. Claude Code 에서는
`/usage` 로 사용량을 확인합니다.

GitHub Copilot 의 기본값은 특히 확인이 필요합니다. 조직 예산을 만들어도 사용 중지 옵션을 켜지 않으면
한도를 넘어 계속 과금됩니다.

## 6. 예외와 재점검

- 승인 목록에 없는 도구가 필요하면 보안 담당과 법무 검토를 거쳐 기간을 정한 예외로 승인합니다.
- 공급자 약관, 데이터 처리 조건, 플랜 구성은 자주 바뀝니다. 연 1회, 그리고 주요 약관 변경 공지가 있을
  때 승인 목록을 다시 점검합니다.
- 사고(비밀 유출, 라이선스 위반 코드 병합, 에이전트의 의도하지 않은 작업)가 생기면 정책에 반영할 점이
  있는지 검토합니다.

## 7. 정책 템플릿

1~6절을 정책 문서 형태로 옮긴 템플릿이
[templates/policy/ai-coding-usage-policy.md](https://github.com/trustedoss/trustedoss.github.io/blob/main/templates/policy/ai-coding-usage-policy.md)에 있습니다. 오픈소스 정책(챕터 03 산출물)의
AI 생성 코드 절에 붙이거나 별도 정책으로 채택하고, 중괄호 안의 값을 조직에 맞게 바꿉니다.

| 템플릿 절                  | 이 가이드의 근거                                                                |
| -------------------------- | ------------------------------------------------------------------------------- |
| 적용 범위, 도구 승인       | 1절                                                                             |
| 데이터 취급                | 2절                                                                             |
| 작업 방식과 검증           | [테스트 환경](./testing), [생산성과 협업](./collaboration)                      |
| 저작권 귀속과 기록         | [법적 고려 1절](./legal-considerations#1-저작권-귀속-사람이-얼마나-기여했는가)  |
| 라이선스 위험 차단         | [공통 Rules 템플릿](./rules-template), [Quick CI/CD](./cicd-quick)              |
| 외부 오픈소스 기여         | [법적 고려 4절](./legal-considerations#4-상류-오픈소스-프로젝트의-ai-기여-정책) |
| 비용                       | 5절                                                                             |
| 책임과 교육, 예외와 재점검 | 3절, 4절, 6절                                                                   |

## 8. 표준 연계와 출처

| 이 페이지의 항목 | 연결되는 표준 요구사항                                   |
| ---------------- | -------------------------------------------------------- |
| 정책 문서와 전파 | ISO/IEC 5230 §3.1.1, ISO/IEC 18974 §4.1.1                |
| 역할과 역량      | ISO/IEC 5230 §3.1.2, ISO/IEC 18974 §4.1.2                |
| 교육과 인식      | ISO/IEC 5230 §3.1.3, ISO/IEC 18974 §4.1.3                |
| AI 정책          | ISO/IEC 42001 §5.2. [AI 시스템 컴플라이언스](./iso42001) |

- GitHub, [Updates to GitHub Copilot interaction data usage policy](https://github.blog/news-insights/company-news/updates-to-github-copilot-interaction-data-usage-policy/) (2026-03-25), [Upcoming changes to GitHub Copilot policies and billing](https://github.blog/changelog/2026-08-28-upcoming-changes-to-github-copilot-policies-and-billing/) (2026-08-28)
- GitHub Docs, [Excluding content from GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot), [Managing policies for Copilot in your organization](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/manage-policies), [Budgets for usage-based billing](https://docs.github.com/en/copilot/concepts/billing/budgets-for-usage-based-billing)
- GitHub, [GitHub Copilot is moving to usage-based billing](https://github.blog/news-insights/github-copilot-is-moving-to-usage-based-billing/)
- Anthropic, [Claude Code data usage](https://code.claude.com/docs/en/data-usage), [Zero data retention](https://code.claude.com/docs/en/zero-data-retention), [Managed settings](https://code.claude.com/docs/en/managed-settings), [Manage costs](https://code.claude.com/docs/en/costs)
- OpenAI, [Enterprise privacy](https://openai.com/enterprise-privacy/), [Your data (API)](https://developers.openai.com/api/docs/guides/your-data)
- Cursor, [Data use](https://cursor.com/data-use), [Privacy and data governance](https://cursor.com/docs/enterprise/privacy-and-data-governance), [Spend limits](https://cursor.com/help/account-and-billing/spend-limits)
- Google Cloud, [Gemini for Google Cloud data governance](https://docs.cloud.google.com/gemini/docs/discover/data-governance)
- EU, [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng) (Digital Omnibus on AI, 제4조 개정)

모든 출처는 2026-11-12에 확인했습니다.

## 다음 단계

- [AI 생성 코드의 법적 고려](./legal-considerations): 템플릿의 저작권·IP 보증 항목 배경
- [에이전트와 MCP 도구 거버넌스](./agent-governance): MCP 서버 도입 심사와 관리 설정
- [AI 코딩의 생산성과 협업](./collaboration): 정책을 팀의 작업 방식으로 옮기기
- [AI가 만든 코드의 테스트 환경](./testing): 템플릿의 "작업 방식과 검증" 항목 구현
