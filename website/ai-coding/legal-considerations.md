---
id: legal-considerations
title: 'AI 생성 코드의 법적 고려'
sidebar_label: 'AI 생성 코드의 법적 고려'
---

# AI 생성 코드의 법적 고려

Rules와 CI 게이트가 라이선스·보안 위험을 다룬다면, 이 페이지는 남은 세 가지 법무 관점 질문에 답합니다.
AI가 생성한 코드의 저작권은 누구 것인가, 침해 분쟁이 나면 누가 방어하는가, AI 사용 사실은 어디에 표시해야 하는가.

:::note 법률 자문이 아닙니다
이 페이지는 2026-07 기준 공개 자료를 정리한 실무 안내입니다. 구체적 사안은 법무팀 또는 변호사와 상의하세요.
:::

## 1. 저작권 귀속: 사람이 얼마나 기여했는가

미국 저작권청(US Copyright Office)은 보고서 "Copyright and Artificial Intelligence" Part 2:
Copyrightability(2025-01 확정)에서 판단 기준을 정리했습니다. 연방대법원이 Thaler v. Perlmutter
상고를 기각(2025)하면서 "AI 자체는 저작자가 될 수 없다"는 원칙도 확정됐습니다.

| 시나리오                                        | 인간 저작자성 | 저작권 보호                              |
| ----------------------------------------------- | ------------- | ---------------------------------------- |
| 프롬프트만 입력하고 출력을 그대로 사용          | 인정되지 않음 | 보호 불가 — 회사 저작물로 등록할 수 없음 |
| AI 초안에 인간이 창작적으로 수정·배열           | 인정됨        | 인간 기여 부분에 한해 보호 가능          |
| AI를 보조 도구로 쓰고 인간이 설계와 통합을 결정 | 인정됨        | 전체 작품의 보호가 부정되지 않음         |

변경 비율 같은 정량 기준은 없습니다. "인간의 창작적 기여가 표현 요소를 결정했는가"를 사안별로 판단합니다.

**실행 규칙** — 나중에 귀속을 입증할 수 있도록 개발 시점에 기록을 남깁니다.

- 커밋 메시지에 AI 도구 사용을 명시합니다. 예: `feat: 주문 API 핸들러 구현 (Claude Code 보조)`
- AI 초안을 수정해 사용한 경우, PR 본문에 어떤 설계·수정 결정을 사람이 했는지 한두 줄 기록합니다.
- 출력을 그대로 사용한 코드는 외부 공개 전에 저작권 표기 방식을 법무팀과 검토합니다.

## 2. 공급자 IP 보증: 침해 분쟁이 나면 누가 방어하는가

주요 공급자는 유료 상용 플랜 사용자에게 IP 보증(indemnification — 제3자가 저작권 침해를
주장하면 공급자가 방어와 배상을 부담)을 제공합니다. 2026-07 기준 현황입니다.

| 공급자                     | 제도와 근거                                                                       | 적용 대상                                           | 유의 조건                                                                                       |
| -------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Microsoft (GitHub Copilot) | Customer Copyright Commitment — GitHub Generative AI Services Terms(2026-03 교체) | Copilot Business, Enterprise                        | 개인용 Free와 Pro 는 제외. 공개 코드 매칭 차단 필터는 2026-04부터 보증 조건에서 제외(선택 기능) |
| OpenAI                     | Copyright Shield(발표명) — Business Terms 의 배상 조항                            | ChatGPT Enterprise, API                             | 무료·개인 플랜 제외. 고객이 콘텐츠를 변경하거나 타사 기술과 결합한 경우 등은 제외               |
| Anthropic                  | Commercial Terms of Service Section K(Indemnification)                            | 유료 상용 고객                                      | 승인된 사용과 그 Output 에 한함. 침해임을 알 수 있었던 사용 등은 제외                           |
| Google Cloud               | Generative AI indemnification — 훈련 데이터와 생성 출력 이중 보장                 | Gemini for Google Cloud(Gemini Code Assist 포함) 등 | 대상 서비스 목록을 Google 이 수시 갱신 — 공식 목록 페이지 확인 필수                             |

**도입 전 체크리스트**

- [ ] 사용할 도구의 플랜이 보증 적용 대상인가 (개인 무료 계정은 대부분 제외)
- [ ] 보증 조건(승인된 사용, 필터 설정, 콘텐츠 변경 금지 등)을 충족하도록 사내 설정을 표준화했는가
- [ ] 약관은 수시로 바뀐다 — 도입 시점의 약관 원문을 확인하고 연 1회 재점검 일정을 잡았는가

## 3. AI 사용 표시: 법적 의무와 모범 관행의 구분

두 규제 모두 표시 의무의 주체는 **AI 시스템이나 생성형 AI 서비스를 제공하는 사업자**입니다.
AI 코딩 도구를 사내 개발에 쓰는 것만으로 코드에 표시할 법적 의무가 생기지는 않습니다.
다만 아래 표의 모범 관행은 저작권 귀속 입증(1절)과 추적성을 위해 권장합니다.

| 규제                  | 핵심 의무                                                                | 시점                                                            |
| --------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------- |
| EU AI Act 제50조      | 제공자의 합성 콘텐츠 머신리더블 마킹, 배포자의 딥페이크·공익 텍스트 고지 | 2026-08-02 적용 (기존 출시 시스템의 마킹은 2026-12-02까지 유예) |
| 한국 AI 기본법 제31조 | 생성형 AI 제품·서비스 제공 사실 고지와 결과물 표시                       | 2026-01-22 시행 (계도기간 운영 중)                              |

**모범 관행** — 법적 의무가 아니어도 다음을 권장합니다.

- 사내 커밋 메시지와 PR 에 AI 도구 사용 명시 (1절의 실행 규칙과 동일)
- 외부 공개 저장소는 README 또는 CONTRIBUTING 에 AI 도구 활용 사실을 한 줄 고지
- 제품에 생성형 AI 기능을 넣어 이용자에게 제공한다면 그때는 위 규제의 직접 대상이 되므로 법무 검토 필수

## 4. 복붙 자산: AI 코딩 도구 사용 정책

아래 블록을 오픈소스 정책 문서(챕터 03 산출물)의 AI 생성 코드 절에 추가하거나 별도 정책으로 사용하세요.

```markdown
## AI 코딩 도구 사용 정책

### 사용 허용 도구

- 공급자 IP 보증이 적용되는 유료 상용 플랜만 사용한다.
  (예: GitHub Copilot Business, ChatGPT Enterprise, Claude 유료 상용 플랜, Gemini Code Assist)
- 개인 무료 계정은 사내 코드에 사용을 금지한다.

### 저작권 귀속 기록

- AI 출력을 그대로 사용한 경우 커밋 메시지에 명시한다.
- AI 초안을 수정한 경우 사람이 내린 설계·수정 결정을 PR 본문에 기록한다.
- AI 출력 그대로인 코드를 외부 공개할 때는 저작권 표기를 법무팀과 검토한다.

### 라이선스 위험 차단

- AI 가 제안한 코드가 카피레프트 라이선스 코드와 유사한지 검증한다 (SCANOSS 등 매칭 도구 활용).
- AI 가 제안한 의존성도 일반 오픈소스와 동일하게 SBOM 과 취약점 관리 대상에 포함한다.
- 의심 사례는 법무팀으로 에스컬레이션한다.
```

정책 문서 전체 구조는 [체계구축 3. 오픈소스 정책](/docs/policy)에서, 도구별 Rules 적용은
[공통 Rules 템플릿](./rules-template)에서 다룹니다.

## 5. 표준 연계와 출처

이 페이지는 OpenChain KWG [AI 컴플라이언스 가이드](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/7-ai-compliance/)
§5(CC BY 4.0)를 기반으로, 아래 1차 출처로 사실을 재확인해 재구성했습니다.

- US Copyright Office, [Copyright and Artificial Intelligence](https://www.copyright.gov/ai/) — Part 2 Copyrightability (2025-01)
- Microsoft, [Customer Copyright Commitment 필수 완화 조치](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/customer-copyright-commitment) / GitHub, [Generative AI Services Terms](https://github.com/customer-terms/github-generative-ai-services-terms)
- OpenAI, [Business Terms](https://openai.com/policies/business-terms/)
- Anthropic, [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) — Section K
- Google Cloud, [Generative AI indemnified services](https://cloud.google.com/terms/generative-ai-indemnified-services)
- EU AI Act, [Article 50](https://artificialintelligenceact.eu/article/50/) / 한국, [인공지능 발전과 신뢰 기반 조성 등에 관한 기본법](https://www.law.go.kr/lsInfoP.do?lsiSeq=268543) 제31조

ISO/IEC 표준과의 연계는 [ISO 표준 연계](./iso-mapping)를, AI 시스템 자체의 컴플라이언스는
[AI 시스템 컴플라이언스 (ISO 42001)](./iso42001)를 참조하세요.
