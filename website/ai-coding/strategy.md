---
id: strategy
title: 보장 수준별 5단계 전략
sidebar_label: 5단계 전략
sidebar_position: 2
---

# 보장 수준별 5단계 전략

## 개요

| 단계  | 이름                      | 핵심 수단                                             | 보장 수준 | 권장 대상   |
| ----- | ------------------------- | ----------------------------------------------------- | --------- | ----------- |
| 1단계 | 프롬프트 의존             | 없음 (개인 기억)                                      | 낮음      | 개인 실험   |
| 2단계 | AI 규칙 내재화            | CLAUDE.md, .cursor/rules, AGENTS.md 등                | 중간      | 팀 공동작업 |
| 3단계 | CI/CD 자동 차단           | Gitleaks · Semgrep · CodeQL · grype · Trivy · Checkov | 높음      | 팀·조직     |
| 4단계 | AI 방어 레이어            | findings-driven AI 리뷰 · AI 퍼징                     | 높음+     | 팀·조직     |
| 5단계 | 지속적 모니터링·자동 교정 | Dependabot · Renovate · DAST                          | 매우 높음 | 조직·전사   |

1단계는 지금 당장 시작할 수 있지만, 3단계부터 진정한 DevSecOps 게이트키퍼 역할을 합니다.
**4단계는 AI 공격에 AI로 맞대응하는 방어 레이어**입니다.

---

## 1단계: 프롬프트 의존 (Manual / Ad-hoc)

:::info 이 단계의 위치
가장 도입이 쉽지만 가장 불안정합니다.
:::

AI 도구에 직접 "MIT 라이선스만 써줘"와 같은 프롬프트를 입력해 라이선스나 보안 정책을 지키는 방식입니다. 도구나 설정 없이 바로 시작할 수 있다는 장점이 있지만, 모든 것이 개발자 개인의 역량과 기억에 전적으로 의존합니다. AI 환각(Hallucination)으로 인해 GPL 코드가 무심코 혼입되거나, 알려진 취약점이 있는 패키지 버전이 추천될 위험이 항상 존재합니다. 개인 실험이나 학습 수준에서는 충분하지만, 팀 협업 환경에서는 일관성을 보장하기 어렵습니다.

---

## 2단계: AI 규칙 내재화 (Tool-level Context Injection)

:::tip 이 단계부터 팀 단위 적용 가능
:::

CLAUDE.md, .cursor/rules, AGENTS.md 같은 공통 규칙 파일을 저장소에 두어 AI가 코드를 작성할 때 자동으로 정책을 인지하도록 하는 방식입니다. 팀 전체가 동일한 규칙을 공유하고, 외부 라이브러리를 추가할 때 AI가 스스로 라이선스를 검토하거나 최신 안정 버전을 제안하는 효과를 기대할 수 있습니다. 다만 AI는 규칙을 어디까지나 "권장사항"으로 이해할 뿐, 100% 강제 차단(Hard Block)은 불가능합니다. 규칙 기반 공동작업을 바로 시작하고 싶다면 아래 링크를 참고하세요.

- [공통 Rules 템플릿](./rules-template)
- [도구별 설정](./tools/claude-code)

에이전트가 MCP 로 외부 도구를 호출하는 환경이라면, 규칙 내재화와 함께 도구 측 통제도 필요합니다 — [에이전트와 MCP 도구 거버넌스](./agent-governance)를 참조하세요.

---

## 3단계: CI/CD 파이프라인 자동 차단 (Pipeline Enforcement)

:::warning 이 단계부터 진정한 Hard Block
:::

PR 또는 Merge 전 파이프라인에서 아래 5개 영역을 기계적으로 검증하는 방식입니다. 개발자나 AI의 실수와 무관하게 정책 위반 코드를 원천 차단할 수 있으며, 이 시점부터 진정한 의미의 게이트키퍼가 작동합니다.

| 영역          | 대표 도구        | 파이프라인 위치 | 탐지 대상                               |
| ------------- | ---------------- | --------------- | --------------------------------------- |
| 시크릿 탐지   | Gitleaks         | pre-commit · PR | API 키·토큰·비밀번호 하드코딩           |
| SAST          | Semgrep · CodeQL | PR              | SQL 인젝션·논리 버그·취약 패턴          |
| SCA           | syft · grype     | PR · 빌드       | 알려진 CVE·금지 라이선스                |
| 컨테이너 보안 | Trivy            | 빌드            | 이미지 취약점 (컨테이너 사용 시)        |
| IaC 보안      | Checkov          | PR              | 클라우드 인프라 설정 오류 (IaC 사용 시) |

AI 코딩 도구는 하드코딩된 값을 코드에 삽입하는 경우가 잦으므로, **시크릿 탐지는 3단계 도입 첫날부터 필수**입니다. 모든 영역을 한꺼번에 도입하기보다 시크릿 탐지 → SAST → SCA 순서로 안정화한 뒤 다음으로 넘어가는 방식을 권장합니다.

- [30분 완성 Quick CI/CD](./cicd-quick) — SCA 중심 최소 시작점
- [DevSecOps — 시크릿 탐지](/devsecops/secret-detection) · [SAST](/devsecops/sast) · [SCA](/devsecops/sca) · [컨테이너 보안](/devsecops/container-security) · [IaC 보안](/devsecops/iac-security)
- [전사 파이프라인 설계](/devsecops/pipeline-design)

**실전 적용 사례 — TRUSCA**: Apache-2.0 오픈소스 SCA 프로젝트가 이 단계를 실제로 운영합니다.
워크플로우 파일을 그대로 열어 볼 수 있습니다.

| 영역        | 워크플로우                                                                                          | 운영 방식                                 |
| ----------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| 시크릿 탐지 | [secret-scan.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/secret-scan.yml) | Gitleaks, 유출 발견 시 Hard Fail          |
| SAST        | [sast.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sast.yml)               | bandit(High) + semgrep(ERROR) Hard Fail   |
| SAST        | [codeql.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/codeql.yml)           | CodeQL 정적 분석                          |
| SCA         | [sca-self.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sca-self.yml)       | cdxgen SBOM 생성 후 Trivy 스캔, 매일 실행 |

시크릿과 SAST 를 Hard Fail 로 걸어 둔 점, 도구 버전을 고정하고 체크섬을 확인하는 점이 이 단계의
성숙한 형태를 보여줍니다.

---

## 4단계: AI 방어 레이어 (AI-Augmented Defense)

:::info 3단계의 사각지대를 AI로 보완합니다
3단계 도구는 **알려진 패턴**을 정확하게 탐지합니다. 반대로 룰에 정의되지 않은 것은 잡지 못합니다.
비즈니스 로직 결함, 권한 검사 누락, 상태 전이 오류가 여기에 해당하며, 이는 AI 코딩 이전부터
정적 분석의 한계였습니다.

AI 코딩이 바꾼 것은 **그 사각지대에 놓이는 코드의 양**입니다. 생산량이 몇 배로 늘어도 리뷰
인원은 그대로이고, AI가 생성한 코드는 문법적으로 정연해 리뷰에서 걸러지기 어렵습니다. 또한
공격자도 AI로 룰 우회 변형을 자동 생성할 수 있습니다.

4단계는 이 사각지대를 AI로 보완합니다.
:::

3단계 도구들이 먼저 패턴 매칭으로 후보를 추려내고, AI는 그 결과물에 집중해 **의미론적 판단**과 **능동적 탐색**을 수행합니다.

### 4a. Findings-Driven AI 리뷰

전체 코드를 AI에게 보내는 대신, **3단계 도구가 플래그한 코드 조각**만 AI에게 전달합니다. 토큰을 절약하면서도 AI 판단이 필요한 영역에 집중할 수 있습니다.

| AI 역할       | 입력                             | 출력                                                    |
| ------------- | -------------------------------- | ------------------------------------------------------- |
| **검증**      | Semgrep·CodeQL 결과 + 해당 코드  | FP/TP 판정, 실제 익스플로잇 가능성 평가                 |
| **심층 해석** | grype CVE + 해당 컴포넌트 사용처 | "이 CVE가 우리 코드 실행 경로에서 실제로 도달 가능한가" |
| **연관 발견** | 플래그된 패턴 + 인접 코드 블록   | 도구가 놓친 동일 유형의 인접 취약점                     |

여러 도구가 동일 위치를 동시에 플래그하면 AI가 높은 우선순위로 상향 조정해 개발자에게 경보를 냅니다. AI 리뷰 결과는 **PR 코멘트로 게시**하며, 빌드를 강제로 실패시키지 않습니다(FP율이 높기 때문).

### 4b. AI 퍼징

3단계 도구가 전혀 건드리지 않은 영역 — 비즈니스 로직, 엣지케이스 입력 처리 — 을 **AI가 능동적으로 탐색**합니다. Claude 등 LLM이 엔드포인트 시그니처를 분석해 경계값과 이상 입력을 자동 생성하고, 앱에 직접 실행해 5xx 오류와 비정상 동작을 탐지합니다. C/C++, Rust 같은 저수준 코드는 OSS-Fuzz 연동을 권장합니다.

| 도구 조합         | 탐지 대상                       | 실행 주기       |
| ----------------- | ------------------------------- | --------------- |
| Claude + requests | 웹 API 엣지케이스·비정상 응답   | Push to main    |
| Claude + AFL++    | 저수준 바이너리 크래시          | 주 1회 스케줄   |
| Claude + OSS-Fuzz | 오픈소스 라이브러리 파서 취약점 | 프로젝트별 설정 |

- [AI 보안 코드 리뷰](./ai-security-review) — Findings-driven 구현 가이드 및 GitHub Actions 예시

**실전 적용 사례**: 3단계와 5단계는 공개 사례를 찾기 쉽지만, 4단계를 상시 운영하는 공개 저장소는
아직 드뭅니다. 이 단계는 도구 지형이 막 형성되는 중이라 참고할 선례가 적습니다. 위 구현 가이드의
워크플로우를 그대로 복사해 먼저 리포트 전용으로 돌려 보고, 오탐 비율을 확인한 뒤 운영 방식을
정하는 편이 현실적입니다.

---

## 5단계: 지속적 모니터링·자동 교정 (Continuous & Auto-remediation)

배포 이후에도 SBOM을 지속적으로 스캔하고, 신규 CVE가 발견되면 자동으로 패치 PR을 생성하는 단계입니다. Dependabot · Renovate와 연동해 중앙 집중식으로 공급망 보안(ISO/IEC 18974) 준수를 유지합니다. 정책 준수에 들어가는 인간의 개입이 최소화되고, AI가 유발한 위험을 자동화로 지속 통제하는 선순환 구조가 완성됩니다.

- [지속적 모니터링·자동 교정](/devsecops/monitoring)
- [DAST — 동적 분석](/devsecops/dast)

**실전 적용 사례 — TRUSCA**:

| 구성 요소        | 파일                                                                                                  | 내용                                                     |
| ---------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 의존성 자동 갱신 | [dependabot.yml](https://github.com/trustedoss/trusca/blob/main/.github/dependabot.yml)               | npm·pip·docker·github-actions 6개 항목                   |
| 정기 스캔        | [sca-self.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sca-self.yml)         | 매일 07:00 UTC SBOM 재생성 + 취약점 스캔                 |
| 자기 적용 검증   | [dogfood-scan.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/dogfood-scan.yml) | 자사 SCA 로 자기 저장소를 스캔(수동 실행, advisory 기본) |

`dogfood-scan.yml` 이 기본값을 비차단으로 두고 `fail_on_gate` 옵션으로 차단을 켜게 설계한 점은,
이 가이드가 권하는 관측 → 경고 → 차단 순서와 같은 접근입니다.

---

## 우리 팀은 어디서 시작해야 할까?

:::tip 단계 선택 가이드
:::

혼자 개발하거나 소규모 실험 중이라면 2단계부터 시작하는 것을 권장합니다. 별도 비용 없이 10분 이내에 설정을 완료할 수 있습니다.

팀이 이미 GitHub Actions를 사용하고 있다면 3단계 Quick CI/CD부터 도전해 보세요. 30분이면 기본 보안 게이트를 구성할 수 있습니다.

3단계를 안정적으로 운영 중이라면 4단계 AI 방어 레이어를 추가하세요. ANTHROPIC_API_KEY 하나로 findings-driven 리뷰와 AI 퍼징을 모두 활성화할 수 있습니다.

이미 4단계까지 운영 중이고 전담 보안팀이 있다면 5단계와 DevSecOps 가이드 전체를 검토해 조직 전체의 공급망 보안 수준을 높이세요.

단계와 무관하게 AI 코딩 도구를 도입하는 시점에는 저작권 귀속, 공급자 IP 보증, AI 사용 표시 세 가지 법무 관점 결정이 필요합니다. [AI 생성 코드의 법적 고려](./legal-considerations)를 함께 확인하세요.
