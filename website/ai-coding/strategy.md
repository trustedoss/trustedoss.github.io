---
id: strategy
title: 보장 수준별 4단계 전략
sidebar_label: 4단계 전략
sidebar_position: 2
---

# 보장 수준별 4단계 전략

## 개요

| 단계  | 이름                      | 핵심 수단                                           | 보장 수준 | 권장 대상   |
| ----- | ------------------------- | --------------------------------------------------- | --------- | ----------- |
| 1단계 | 프롬프트 의존             | 없음 (개인 기억)                                    | 낮음      | 개인 실험   |
| 2단계 | AI 규칙 내재화            | CLAUDE.md · .cursorrules 등                         | 중간      | 팀 공동작업 |
| 3단계 | CI/CD 자동 차단           | Gitleaks · Semgrep · syft · grype · Trivy · Checkov | 높음      | 팀·조직     |
| 4단계 | 지속적 모니터링·자동 교정 | Dependabot · Renovate · OSS-Fuzz + AI               | 매우 높음 | 조직·전사   |

1단계는 지금 당장 시작할 수 있지만, 3단계부터 진정한 DevSecOps 게이트키퍼 역할을 합니다.

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

CLAUDE.md · .cursorrules · .clinerules 등 공통 규칙 파일을 저장소에 두어 AI가 코드를 작성할 때 자동으로 정책을 인지하도록 하는 방식입니다. 팀 전체가 동일한 규칙을 공유하고, 외부 라이브러리를 추가할 때 AI가 스스로 라이선스를 검토하거나 최신 안정 버전을 제안하는 효과를 기대할 수 있습니다. 다만 AI는 규칙을 어디까지나 "권장사항"으로 이해할 뿐, 100% 강제 차단(Hard Block)은 불가능합니다. 규칙 기반 공동작업을 바로 시작하고 싶다면 아래 링크를 참고하세요.

- [공통 Rules 템플릿](./rules-template)
- [도구별 설정](./tools/claude-code)

---

## 3단계: CI/CD 파이프라인 자동 차단 (Pipeline Enforcement)

:::warning 이 단계부터 진정한 Hard Block
:::

PR 또는 Merge 전 파이프라인에서 아래 6개 영역을 기계적으로 검증하는 방식입니다. 개발자나 AI의 실수와 무관하게 정책 위반 코드를 원천 차단할 수 있으며, 이 시점부터 진정한 의미의 게이트키퍼가 작동합니다.

| 영역          | 대표 도구           | 파이프라인 위치 | 탐지 대상                               |
| ------------- | ------------------- | --------------- | --------------------------------------- |
| 시크릿 탐지   | Gitleaks            | pre-commit · PR | API 키·토큰·비밀번호 하드코딩           |
| SAST          | Semgrep · CodeQL    | PR              | SQL 인젝션·논리 버그·취약 패턴          |
| SCA           | syft · grype        | PR · 빌드       | 알려진 CVE·금지 라이선스                |
| 컨테이너 보안 | Trivy               | 빌드            | 이미지 취약점 (컨테이너 사용 시)        |
| IaC 보안      | Checkov             | PR              | 클라우드 인프라 설정 오류 (IaC 사용 시) |
| AI 코드 리뷰  | Claude · Semgrep AI | PR              | 의미론적 취약점 (선택 옵션)             |

AI 코딩 도구는 하드코딩된 값을 코드에 삽입하는 경우가 잦으므로, **시크릿 탐지는 3단계 도입 첫날부터 필수**입니다. 모든 영역을 한꺼번에 도입하기보다 시크릿 탐지 → SAST → SCA 순서로 안정화한 뒤 다음으로 넘어가는 방식을 권장합니다.

- [30분 완성 Quick CI/CD](./cicd-quick) — SCA 중심 최소 시작점
- [AI 코드 리뷰 확장](./ai-security-review) — AI를 활용한 의미론적 취약점 탐지 (선택 옵션)
- [DevSecOps — 시크릿 탐지](/devsecops/secret-detection) · [SAST](/devsecops/sast) · [SCA](/devsecops/sca) · [컨테이너 보안](/devsecops/container-security) · [IaC 보안](/devsecops/iac-security)
- [전사 파이프라인 설계](/devsecops/pipeline-design)

---

## 4단계: 지속적 모니터링·자동 교정 (Continuous & Auto-remediation)

배포 이후에도 SBOM을 지속적으로 스캔하고, 신규 CVE가 발견되면 AI Agent가 자동으로 패치 PR을 생성하는 단계입니다. Dependabot · Renovate와 연동해 중앙 집중식으로 공급망 보안(ISO/IEC 18974) 준수를 유지합니다. 정책 준수에 들어가는 인간의 개입이 최소화되고, AI가 유발한 위험을 AI와 자동화로 통제하는 선순환 구조가 완성됩니다.

AI 퍼징(Fuzz Testing) 또한 4단계의 확장 영역입니다. Claude 등 LLM에게 함수 시그니처를 분석시켜 fuzz target 코드를 자동 생성한 뒤, AFL++ · libFuzzer · OSS-Fuzz 인프라에서 실제 퍼징을 실행하는 방식입니다. C/C++ · Rust 등 저수준 언어나 파서·프로토콜 구현부에서 효과가 크며, Python · JS 웹 애플리케이션은 DAST([동적 분석](/devsecops/dast))로 대체합니다.

- [지속적 모니터링·자동 교정](/devsecops/monitoring)
- [DAST — 동적 분석](/devsecops/dast)

---

## 우리 팀은 어디서 시작해야 할까?

:::tip 단계 선택 가이드
:::

혼자 개발하거나 소규모 실험 중이라면 2단계부터 시작하는 것을 권장합니다. 별도 비용 없이 10분 이내에 설정을 완료할 수 있습니다.

팀이 이미 GitHub Actions를 사용하고 있다면 3단계 Quick CI/CD부터 도전해 보세요. 30분이면 기본 보안 게이트를 구성할 수 있습니다.

이미 3단계를 운영 중이고 전담 보안팀이 있다면 4단계와 DevSecOps 가이드 전체를 검토해 조직 전체의 공급망 보안 수준을 높이세요.
