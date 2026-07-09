---
id: intro
title: AI 코딩 거버넌스
sidebar_label: 소개
sidebar_position: 1
slug: intro
---

# AI 코딩 거버넌스 — 도구와 오픈소스 컴플라이언스

:::note 선택 단계 — 개발팀이 있다면
이 섹션은 [체계구축](/docs)으로 만든 정책을 **AI 코딩 도구·CI에 자동 적용**하는 선택 단계입니다.
표준 자체 인증이 목표라면 체계구축(거버넌스)을 먼저 끝내세요. 개발자가 AI 도구를 쓴다면 여기서 정책을 코드 생성 시점에 강제합니다.
:::

AI 코딩 도구(Claude Code, Cursor, GitHub Copilot, Windsurf, OpenAI Codex, Gemini CLI 등)는 개발 생산성을 크게 높여줍니다.
하지만 AI가 생성한 코드에도 오픈소스 라이선스 컴플라이언스와 보안 취약점 관리가 필요합니다.

## 왜 AI 코딩 도구에서 오픈소스 관리가 중요한가?

- **AI는 오픈소스 코드를 학습하여 유사한 코드를 생성합니다** — 저작권 및 라이선스 이슈가 발생할 수 있습니다.
- **AI가 제안하는 의존성 패키지**도 SBOM 및 취약점 관리 대상입니다.
- **Rules/Prompt 설정**으로 오픈소스 컴플라이언스 요구사항을 AI에게 사전 안내할 수 있습니다.

## 이 섹션에서 다루는 내용

| 페이지                                             | 설명                                                             |
| -------------------------------------------------- | ---------------------------------------------------------------- |
| [보장 수준별 5단계 전략](./strategy)               | 프롬프트 의존 → AI 규칙 내재화 → CI/CD 차단 → AI 방어 → 모니터링 |
| [공통 Rules 템플릿](./rules-template)              | 오픈소스 컴플라이언스를 위한 공통 Rules 예시                     |
| [Claude Code](./tools/claude-code)                 | Anthropic의 CLI 기반 AI 코딩 에이전트                            |
| [Cursor](./tools/cursor)                           | AI 기반 코드 편집기                                              |
| [GitHub Copilot](./tools/copilot)                  | GitHub의 AI 페어 프로그래머                                      |
| [Windsurf](./tools/windsurf)                       | Cognition의 AI 코딩 에이전트 (구 Codeium, Devin Desktop 통합 중) |
| [Cline / Aider](./tools/cline-aider)               | 오픈소스 CLI/VS Code 기반 AI 에이전트                            |
| [30분 완성 Quick CI/CD](./cicd-quick)              | SCA·라이선스 중심 CI/CD 최소 시작점                              |
| [AI 보안 코드 리뷰](./ai-security-review)          | 4단계 — findings-driven AI 검증·심층 해석                        |
| [AI 생성 코드의 법적 고려](./legal-considerations) | 저작권 귀속, 공급자 IP 보증, AI 사용 표시                        |
| [AI 시스템 컴플라이언스](./iso42001)               | ISO/IEC 42001과 오픈소스의 교차점                                |
| [Best Practice 저장소](./best-practice-repo)       | 1~5단계 모두 구현한 참조 GitHub 저장소                           |
| [ISO 표준 연계](./iso-mapping)                     | AI 코딩 구현이 강화하는 표준 항목 매핑                           |

## 빠른 시작

오픈소스 컴플라이언스 관점에서 AI 코딩 도구를 설정하려면 [공통 Rules 템플릿](./rules-template)부터 시작하세요.

CI/CD 파이프라인 심화 설계와 전사 보안 전략은 [DevSecOps 가이드](/devsecops/intro)에서 다룹니다.
