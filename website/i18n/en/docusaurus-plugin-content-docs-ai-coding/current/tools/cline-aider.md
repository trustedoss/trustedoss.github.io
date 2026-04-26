---
id: cline-aider
title: Cline / Aider Setup
sidebar_label: Cline / Aider
sidebar_position: 5
---

# Cline / Aider Setup

## Overview

Cline reads `.clinerules` files (a single root file or `.clinerules/` folder) as project instructions and applies them to AI behavior. Aider can augment the system prompt through `AGENTS.md` or the `system_prompt` field in `.aider.conf.yml`. Both tools apply rules at the project level.

Cline is an agent-style AI tool running as a VS Code extension, while Aider is a terminal-based CLI tool. Both are open source and run locally, so they are often preferred by teams that avoid sending code to external servers. If open source policy is written in each configuration file, AI automatically considers it when adding packages or generating code.

---

## Cline Setup

### Configuration File Location

- `.clinerules` (single root file, recommended)
- `.clinerules/` (folder, allows split files)

### How to Apply

1. Create `.clinerules` in the project root.
2. Paste content from the [Common Rules Template](../rules-template).
3. Update the allow/deny license list to match internal policy.

### Configuration Example

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

---

## Aider Setup

### Configuration File Location

- `AGENTS.md` (root, compatible with OpenAI Codex agent spec)
- `system_prompt` field in `.aider.conf.yml`

### How to Apply

1. Create `AGENTS.md` in the project root.
2. Paste content from the [Common Rules Template](../rules-template).
3. If you prefer concise setup, summarize only key policy points in `.aider.conf.yml` under `system_prompt`.

### Configuration Example

**AGENTS.md** — Include the entire Common Rules Template as-is.

```markdown
## 오픈소스 정책

### 라이선스 관리

새로운 외부 패키지·라이브러리 추가 시 반드시 라이선스를 확인하고 명시할 것.

**허용 라이선스**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**주의 라이선스** (법무 검토 필요): LGPL, MPL

**금지 라이선스** (사전 승인 없이 사용 불가): GPL, AGPL, SSPL, Commons Clause

### 보안 관리

- 알려진 CVE 취약점이 있는 패키지 버전 사용 금지
- 패키지 버전은 가능한 최신 안정 버전(Latest Stable) 사용

### SBOM 관리

- 의존성 변경 시 SBOM 업데이트 필요 (도구: cdxgen, syft)
```

**.aider.conf.yml** — Use a concise summary of key items only.

```yaml
system_prompt: |
  ## 오픈소스 정책
  허용 라이선스: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
  주의 라이선스 (법무 검토 필요): LGPL, MPL
  금지 라이선스: GPL, AGPL, SSPL, Commons Clause
  CVE 취약점 버전 사용 금지. 의존성 추가 후 audit 실행 권장.
```

---

## Notes

:::info Good to know
Both Cline and Aider treat rules as soft guidance rather than hard blocking. To fully block policy-violating packages, configure a CI/CD pipeline in parallel. Since Aider is CLI-based, if `.aider.conf.yml` does not exist, you can pass policy directly on each run with `--system-prompt`. For automated CI/CD gate setup, refer to [Quick CI/CD](../cicd-quick).
:::
