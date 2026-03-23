---
id: intro
title: DevSecOps
slug: intro
---

# DevSecOps

## 이 가이드에서 다루는 것

AI 코딩 도구가 생성한 코드가 조직의 오픈소스 정책을 위반하지 않도록 파이프라인 수준에서 강제하는 방법을 다룹니다. SBOM 생성·취약점 관리·라이선스 거버넌스·지속적 모니터링까지 전사 DevSecOps 체계를 구축하는 실전 가이드입니다. ISO/IEC 5230(라이선스 컴플라이언스)과 ISO/IEC 18974(보안 보증) 표준 요구사항과의 연계 방법도 함께 설명합니다.

---

## AI 코딩 가이드와의 관계

:::info Quick CI/CD를 먼저 적용했다면 여기서 심화하세요
AI 코딩 가이드의 Quick CI/CD는 개발자가 30분 안에 기본 게이트를 만드는 것이 목적입니다. 이 DevSecOps 가이드는 그 위에서 전사 정책 설계·멀티 저장소 관리·감사 대응까지 다룹니다. 두 가이드는 독립적으로 사용 가능하지만, [AI 코딩 — Quick CI/CD](/ai-coding/cicd-quick) → DevSecOps 순서로 읽는 것을 권장합니다.
:::

---

## 이 메뉴의 구성

| 페이지 | 다루는 내용 | 권장 독자 |
|--------|------------|-----------|
| [도입 전략](./strategy) | 성숙도 모델·단계별 로드맵 | 팀 리드·아키텍트 |
| [SAST](./sast) | 정적 분석 — CodeQL·Semgrep | 개발자·DevOps |
| [SCA](./sca) | 의존성 분석 — syft·grype·SBOM | DevOps·보안팀 |
| [시크릿 탐지](./secret-detection) | 키·토큰 누출 방지 — Gitleaks | 개발자·DevOps |
| [컨테이너 보안](./container-security) | 이미지 취약점 — Trivy | DevOps·보안팀 |
| [IaC 보안](./iac-security) | 인프라 코드 검사 — Checkov | DevOps·SRE |
| [DAST](./dast) | 동적 분석 — OWASP ZAP·Nuclei | 보안팀·QA |
| [파이프라인 설계](./pipeline-design) | 전체 통합 설계·GitHub Actions | DevOps 엔지니어 |
| [모니터링·자동 교정](./monitoring) | 배포 후 지속 스캔·자동 PR | DevOps·보안팀 |
| [ISO 표준 연계](./iso-mapping) | ISO/IEC 18974 요구사항 매핑 | 컴플라이언스 담당 |

---

## 어디서 시작할까?

:::tip 역할별 시작점

- DevSecOps가 처음이다
  → [도입 전략](./strategy)부터
- 코드 품질·보안 취약점을 코드 단계에서 잡고 싶다
  → [SAST](./sast)부터
- 오픈소스 의존성 취약점이 걱정된다
  → [SCA](./sca)부터
- API Key·토큰이 코드에 노출된 적 있다
  → [시크릿 탐지](./secret-detection)부터
- 컨테이너 환경을 운영 중이다
  → [컨테이너 보안](./container-security)부터
- ISO/IEC 18974 인증을 준비 중이다
  → [ISO 표준 연계](./iso-mapping)부터
  (단, SCA 페이지를 먼저 읽을 것을 권장)
:::
