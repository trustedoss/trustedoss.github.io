# AI SBOM 가이드 동기화 + AI 생성 코드 법적 고려 보강 계획 (2026-07-09)

> 근거: `summit-review-findings.md` P0-6 후속, `STATUS.md` "KWG 갭 분석 — 검토 후 결정" 1번(동기화 범위 확장),
> 5번(AI 코딩 3주제 보강), 7번(guide_mappings 사각지대). 승인 후 실행한다.

## Context

Part A. 상류 KWG 에 AI SBOM 컴플라이언스 가이드(`content/ko/guide/ai-sbom_guide/`)가 신설됐으나
우리 동기화 스크립트는 3개 경로(opensource_for_enterprise, templates, tools)만 가져온다.
상류 구조(실측): 5개 파트, 하위 페이지 13개 —
프로그램 기반 4(정책, 역량, 인식, 범위), AI 확장 3(라이선스 의무, 투명성 의무, AI SBOM),
관련 업무 2(접근성, 리소스), 거버넌스 1, 도구 3(OWASP AIBOM Generator, cdxgen, 스캐너).

Part B. 상류 7-ai-compliance §5 가 신설한 세 주제가 우리 AI 코딩 가이드에 없다
(grep 실측: website/ai-coding 에 "저작권 귀속", "indemnif", "AI Act" 0건).

1. AI 생성 코드의 저작권 귀속 — 인간 저작자성 3-시나리오 판단 기준 (US Copyright Office AI 가이드)
2. 공급자 IP 보증(indemnification) — Microsoft, OpenAI, Anthropic, Google 4사의 보증 제도와 적용 조건
3. AI 사용 표시 의무 — EU AI Act §50, 한국 AI 기본법의 AI 생성 콘텐츠 표시 의무

우리 `templates/policy/oss-policy.md` §5(AI 생성 코드 정책, 102~116행)는 검토 의무와
출처 추적, 약관 확인 3원칙만 담고 있어 위 세 주제(귀속 판단, 보증 조건, 표시 규칙)가 비어 있다.

## 원칙

- POSITIONING §7 준수: KWG 가 "무엇을·왜", 우리는 "어떻게, 자동으로". KWG 본문 전재 금지
  (iso42001.md 전재 문제의 재발 방지). 요약 + 실행 자산(복붙 블록, 체크리스트) + 원문 링크 + CC BY 4.0 표기.
- 사실 검증 선행: KWG 서술도 그대로 믿지 않고 1차 출처로 재검증한다. 특히 공급자 보증 제도의
  정확한 명칭과 조건, 규제 시행 일정은 변화가 빠르다.
- 실행 규약: STATUS 선커밋, 청크별 DoD(수정 + en 쌍 + verify.sh 12/12, 빌드는 커밋 게이트가 강제),
  최종 gate-verifier 역순 독립 판정.

## Part A — ai-sbom_guide 동기화 (규모: 소)

### 청크 A1 — 동기화 범위 확장

- `.claude/scripts/sync-kwg-reference.sh` 45~47행 대상 배열에 `${BASE_CONTENT_PATH}/ai-sbom_guide` 추가.
  파일 상단 주석(6~8행)과 말미 대상 표(159~161행)도 갱신.
- 스크립트 실행으로 `.claude/reference/kwg/content/ko/guide/ai-sbom_guide/` 동기화 후 커밋.

### 청크 A2 — drift 하네스 정합

- 동기화 직후 `check-kwg-drift.py` 실행 — 신규 파일의 alert 블록에서 수집되는 섹션 번호를 확인하고,
  `kwg-mapping.yaml` 에 다음을 반영한다.
  - guide_mappings 에 ai-sbom_guide 항목 추가 (our_coverage 는 당장 "참조 전용" — 대응 문서가 생기면 갱신)
  - 갭 분석 7번 함께 처리: guide_mappings 에 0-openchain 과 7-ai-compliance 항목 추가
    (7-ai-compliance 는 website/ai-coding/ 대응 — Part B 신규 페이지 포함)
  - ISO/IEC 42001 조항 번호 등 5230/18974 가 아닌 번호는 오탐 방지 목적으로 등재 (기존 패턴 재사용)
- drift 클린 확인 후 `--reset` 으로 기준점 재설정, 커밋.

### 청크 A3 — 독자 대면 최소 연결

전면 챕터화는 이번 범위 밖(아래 "범위 밖" 참조). KWG 링크 정책(일관된 위치에만 링크)에 따라 두 곳만 연결한다.

- `docs/00-overview/sbom-101.md` — "AI SBOM" 짧은 절 신설(3~4문단): 왜 일반 SBOM 으로 부족한가,
  SPDX 3.0 AI Profile 과 CycloneDX ML-BOM 이 담는 것(모델, 데이터셋, 하이퍼파라미터),
  상세는 KWG ai-sbom_guide 원문 링크로 위임.
- `website/ai-coding/iso42001.md` — 기존 AI SBOM 언급부에 KWG ai-sbom_guide 링크 추가.
  (이 페이지의 전재 축약은 보고서 P1-11 로 별도 진행 — 이번에는 링크만.)
- 두 파일 모두 en 쌍 동일 수정.

## Part B — AI 생성 코드 법적 고려 3주제 보강 (규모: 중)

### 배치 결정

신규 페이지 `website/ai-coding/legal-considerations.md` — "AI 생성 코드의 법적 고려".
사이드바 "실전 적용" 카테고리의 ai-security-review 다음에 배치.

iso42001.md 확장안은 기각한다: 그 페이지는 축약 대상(전재 문제)인 데다, 세 주제는 42001(경영시스템)이
아니라 저작권과 계약, 규제 대응이므로 별도 페이지가 주제 정합적이다.

### 청크 B0 — 사실 검증 (WebSearch, 1차 출처만)

작성 전에 아래를 확인하고, KWG 원문과 다른 점이 있으면 확인된 사실을 따른다.

| 확인 대상                              | 확인 포인트                                                               |
| -------------------------------------- | ------------------------------------------------------------------------- |
| US Copyright Office AI 가이드          | 2024 가이드 이후 갱신(2025 보고서 Part 2 등) 여부, 3-시나리오 표의 정확성 |
| Microsoft Copilot Copyright Commitment | 적용 대상(Business/Enterprise), 조건(필터 활성화 등)                      |
| OpenAI Copyright Shield                | 적용 대상 플랜, 현행 명칭 유지 여부                                       |
| Anthropic 보증 제도                    | KWG 표기 "Customer Protection"의 정확한 현행 명칭과 조건                  |
| Google Cloud 생성형 AI indemnification | 적용 서비스 범위                                                          |
| EU AI Act §50                          | 투명성 의무 적용 시점(2026-08 전후)과 코드 생성에의 적용 범위             |
| 한국 AI 기본법                         | 표시 의무 조항 번호, 시행일, 하위 법령 상태                               |

### 청크 B1 — 페이지 작성

구성(각 절은 요약 + 실행 지침 중심, 근거는 링크):

1. 왜 필요한가 — AI 코딩 도구 도입 시 법무 관점 위험 3가지 (3~5줄)
2. 저작권 귀속 판단 — 3-시나리오 표 + 우리식 실행 규칙(commit 메시지, PR 본문 기록 예시)
3. 공급자 IP 보증 — 4사 비교 표 + 도입 전 체크리스트(개인 무료 계정 사내 사용 금지 등)
4. AI 사용 표시 의무 — 두 규제 요약 + 사내 commit, 외부 공개 README, AI 출력물 라벨링 예시
5. 복붙 자산 — "AI 코딩 도구 사용 정책" 블록(KWG §5-4 기반, 우리 정책 템플릿 §5와 용어 정합)
6. 표준 연계와 출처 — KWG 7-ai-compliance §5 원문 링크 + CC BY 4.0 출처 표기 + 1차 출처 목록

분량 목표 120~160행. ko-style 준수(표 밖 가운뎃점 나열 금지, 이모지 금지 — KWG 원문 표의 체크 이모지는
텍스트로 치환).

### 청크 B2 — 결선(연결)

- `website/sidebarsAiCoding.ts` — 실전 적용 카테고리에 legal-considerations 등록.
- `website/ai-coding/intro.md` — 섹션 개요 표에 행 추가 (P2 지적이던 표 누락 2건도 이때 함께 보완 검토).
- `website/ai-coding/strategy.md` — 도입 단계 안내에서 법적 고려 페이지 링크 1줄.
- `templates/policy/oss-policy.md` §5 보강 — 갭 분석 4-5 대응: 귀속 결정 기록 규칙,
  IP 보증 조건 확인, AI 사용 표시 3항목을 원칙 목록에 추가 (agent 산출물 정합은 verify 커버리지로 확인).
- rules-template 공통 템플릿에는 이번에 손대지 않는다 — 동일 블록이 사이트에 7회 중복 수록돼 있어
  (P2 단일화 선행 과제) 지금 수정하면 7곳 동시 수정이 필요하다. 페이지 내 안내로 갈음.

### 청크 B3 — en 쌍

신규 페이지 번역 + B2 에서 변경된 ko 파일들의 en 쌍 동일 수정.

## 최종 게이트

- verify.sh 12/12 (커밋 게이트가 ko/en 빌드 포함 매 커밋 강제)
- gate-verifier 역순 독립 판정: B3 → B2 → B1 → B0(출처 표기 실재) → A3 → A2(drift 클린 실측) → A1
- STATUS 마감 갱신 + 커밋

## 범위 밖 (후속 후보)

- AI SBOM 독자 대면 전용 챕터(실습 포함: cdxgen ML-BOM 생성 실측) — 수요 확인 후 별도 계획
- iso42001.md 전재 축약(보고서 P1-11), rules-template 7곳 중복 단일화(P2)
- 갭 분석 2번(vulnerability-response 템플릿 상향), 3번(정책 용어 정의), 4번(조직 챔피언 모델)

## 예상 작업량

Part A 청크 3개(스크립트 1줄 + 매핑 + 연결 2파일), Part B 청크 4개(신규 페이지 1 + 연결 4파일 + en 쌍).
커밋 6~7개 예상.
