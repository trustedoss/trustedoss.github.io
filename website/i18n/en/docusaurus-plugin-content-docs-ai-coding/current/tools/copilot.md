---
id: copilot
title: GitHub Copilot
sidebar_label: GitHub Copilot
sidebar_position: 3
---

# GitHub Copilot

## Overview

GitHub Copilot reads `.github/copilot-instructions.md` as custom instructions applied across the entire repository. It applies consistently in all environments where Copilot is enabled, such as VS Code, JetBrains, and GitHub.com. The scope is repository-level.

If open source policy is written in this file, Copilot automatically recognizes license and security policy while suggesting code, regardless of which editor team members use. Since most repositories already have a `.github/` directory, it can be applied immediately without creating additional directories. It is recommended to copy a base template including this file whenever creating a new repository.

## Configuration File Location

- `.github/copilot-instructions.md` (single file, applied to whole repository)

## How to Apply

1. If `.github/` does not exist, create it and add `copilot-instructions.md`.
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
Common instructions at the organization level are not supported separately, so `.github/copilot-instructions.md` must be copied into each repository. If you manage multiple repositories, maintain this file as a shared template and sync updates across all repositories to prevent policy drift. It applies to both Copilot Chat and code completion, though there may be a short delay after changes.
:::
