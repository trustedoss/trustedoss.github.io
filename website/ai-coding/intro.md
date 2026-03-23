---
id: intro
title: AI 코딩 도구 소개
sidebar_label: 소개
sidebar_position: 1
slug: intro
---

# AI 코딩 도구와 오픈소스 컴플라이언스

AI 코딩 도구(Claude Code, Cursor, GitHub Copilot, Windsurf 등)는 개발 생산성을 크게 높여줍니다.
하지만 AI가 생성한 코드에도 오픈소스 라이선스 컴플라이언스와 보안 취약점 관리가 필요합니다.

## 왜 AI 코딩 도구에서 오픈소스 관리가 중요한가?

- **AI는 오픈소스 코드를 학습하여 유사한 코드를 생성합니다** — 저작권 및 라이선스 이슈가 발생할 수 있습니다.
- **AI가 제안하는 의존성 패키지**도 SBOM 및 취약점 관리 대상입니다.
- **Rules/Prompt 설정**으로 오픈소스 컴플라이언스 요구사항을 AI에게 사전 안내할 수 있습니다.

## 이 섹션에서 다루는 내용

| 도구 | 설명 |
|------|------|
| [Claude Code](./tools/claude-code) | Anthropic의 CLI 기반 AI 코딩 에이전트 |
| [Cursor](./tools/cursor) | AI 기반 코드 편집기 |
| [GitHub Copilot](./tools/copilot) | GitHub의 AI 페어 프로그래머 |
| [Windsurf](./tools/windsurf) | Codeium의 AI 코딩 에이전트 |
| [공통 Rules 템플릿](./rules-template) | 오픈소스 컴플라이언스를 위한 공통 Rules 예시 |
| [CI/CD 자동화](./cicd-quick) | AI 코딩과 SBOM/보안 스캔 자동화 통합 |

## 빠른 시작

오픈소스 컴플라이언스 관점에서 AI 코딩 도구를 설정하려면 [공통 Rules 템플릿](./rules-template)부터 시작하세요.
