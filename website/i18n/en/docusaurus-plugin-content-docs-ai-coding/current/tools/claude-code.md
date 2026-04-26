---
id: claude-code
title: Claude Code
sidebar_label: Claude Code
sidebar_position: 1
---

# Claude Code

## Overview

Claude Code automatically reads `CLAUDE.md` in the project root at session start and uses it as context for all work. You can also place `CLAUDE.md` in subfolders, and it is additionally loaded when working in those folders. The scope is project-level, and global settings are also possible through `~/.claude/CLAUDE.md`.

If open source policies are written in `CLAUDE.md`, Claude Code automatically considers license and security policies when adding new packages or generating code, even without explicit developer prompts. If the team uses the same repository, committing `CLAUDE.md` applies consistent policy to all team members.

## Configuration File Location

- Project root: `CLAUDE.md` (recommended)
- Per subfolder: `{folder_name}/CLAUDE.md` (supplementary)
- Global: `~/.claude/CLAUDE.md` (shared across all projects)

## How to Apply

1. Create `CLAUDE.md` in the project root, or open the existing file.
2. Paste content from the [Common Rules Template](../rules-template).
3. Update the allow/deny license list to match internal policy.

## Configuration Example

```markdown
# 프로젝트 가이드

(기존 프로젝트 지침 내용)

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

---
```

## Notes

:::warning Limits of AI rules
Because `CLAUDE.md` consumes prompt tokens, overly long content reduces context efficiency. Also, Claude Code treats rules as guidance and does not hard-block policy-violating code. If practical blocking is required, it must be paired with a CI/CD pipeline. The pipeline should serve as the real gatekeeper, while `CLAUDE.md` supports AI in generating code in the right direction.
:::
