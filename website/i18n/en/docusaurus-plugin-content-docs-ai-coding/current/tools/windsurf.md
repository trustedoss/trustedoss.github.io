---
id: windsurf
title: Windsurf
sidebar_label: Windsurf
sidebar_position: 4
---

# Windsurf

## Overview

Windsurf reads `.windsurfrules` in the project root and uses it as behavior instructions for the Cascade AI agent. Global rules can be configured separately in the Windsurf app settings (UI). The scope is project-level, and global and project settings can be used together.

It is efficient to manage rules in layers: put organization-wide policy in Global Rules and project-specific exceptions or additional rules in `.windsurfrules`. Committing `.windsurfrules` to the repository applies the same policy across the team. If global and project rules conflict, project rules take precedence.

## Configuration File Location

- Project: `.windsurfrules` (root, recommended)
- Global: Windsurf app settings > Global Rules

## How to Apply

1. Create `.windsurfrules` in the project root.
2. Paste content from the [Common Rules Template](../rules-template).
3. Update the allow/deny license list to match internal policy.

## Configuration Example

```markdown
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
`.windsurfrules` is only for the Cascade agent and does not apply to standard code completion (Autocomplete). Keep in mind that policy applies only to agent actions (file creation/modification, package additions, etc.), and extra caution is needed when using plain completion. Larger files can increase response latency, so keep only essential team policies concise from the full template.
:::
