---
id: cursor
title: Cursor
sidebar_label: Cursor
sidebar_position: 2
---

# Cursor

## Overview

Cursor recognizes `.mdc` files under `.cursor/rules/` as rules and applies them to AI behavior. You can set scope (glob patterns) per file, so rules can be split and managed by language or folder. The scope is project-level.

If the open source policy is separated into `.cursor/rules/oss-policy.mdc`, it can be managed independently from other development guidelines and disabled easily when needed. Limiting target files with `globs` reduces unnecessary context usage. Committing it to the repository automatically applies the same policy across the team. If there are multiple rule files, clear purpose-based filenames make maintenance easier.

## Configuration File Location

- `.cursor/rules/oss-policy.mdc` (recommended)
- `.cursorrules` (single root file, legacy)

## How to Apply

1. Create `.cursor/rules/oss-policy.mdc`.
2. Paste content from the [Common Rules Template](../rules-template).
3. Update the allow/deny license list to match internal policy.

## Configuration Example

```markdown
---
description: 오픈소스 라이선스 및 보안 정책
globs: ['**/*.{js,ts,py,go,java}']
alwaysApply: true
---

## 오픈소스 정책

### 라이선스 관리

새로운 외부 패키지·라이브러리 추가 시 반드시 라이선스를 확인하고 명시할 것.

**허용 라이선스**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**주의 라이선스** (법무 검토 필요): LGPL, MPL

**금지 라이선스** (사전 승인 없이 사용 불가): GPL, AGPL, SSPL, Commons Clause

### 보안 관리

- 알려진 CVE 취약점이 있는 패키지 버전 사용 금지
- 의존성 추가 후 아래 명령어 중 하나를 실행할 것:
  - npm: `npm audit`
  - Python: `pip-audit`
  - 컨테이너·범용: `trivy fs .`
- 패키지 버전은 가능한 최신 안정 버전(Latest Stable) 사용

### SBOM 관리

- 의존성 변경 시 SBOM 업데이트 필요
- 생성 도구: cdxgen, syft, trivy
- 권장 포맷: CycloneDX (차선: SPDX)

### 저작권

- 기존 코드의 저작권 헤더 유지
- 새 파일 생성 시 프로젝트 라이선스 헤더 포함
- 타 프로젝트 코드 복사 시 출처 및 라이선스 명시
```

## Notes

:::info Good to know
When `alwaysApply: true` is set, rules apply to all files and token usage may increase. For policies that must always apply, use `alwaysApply: true`; for rules needed only for specific languages or folders, limit scope with `globs` for efficiency. If both `.cursorrules` (legacy) and `.cursor/rules/` are used, `.cursor/rules/` takes precedence, so `.cursor/rules/` is recommended for new projects.
:::
