---
id: cline-aider
title: Cline / Aider 설정
sidebar_label: Cline / Aider
sidebar_position: 5
---

# Cline / Aider 설정

## 개요

Cline은 `.clinerules` 파일(루트 단일 파일 또는 `.clinerules/` 폴더)을 프로젝트 지침으로 읽어 AI 동작에 반영합니다. Aider는 `AGENTS.md` 또는 `.aider.conf.yml`의 `system_prompt` 항목을 통해 시스템 프롬프트를 보강할 수 있습니다. 두 도구 모두 프로젝트 단위로 규칙을 적용합니다.

Cline은 VS Code 확장으로 동작하는 에이전트형 AI 도구이며, Aider는 터미널 기반 CLI 도구입니다. 두 도구 모두 오픈소스이며 로컬 환경에서 실행되므로, 코드를 외부 서버에 전송하는 것을 꺼리는 팀에서 선호합니다. 오픈소스 정책을 각 설정 파일에 작성해 두면 AI가 패키지를 추가하거나 코드를 생성할 때 자동으로 정책을 고려합니다.

---

## Cline 설정

### 설정 파일 위치

- `.clinerules` (루트 단일 파일, 권장)
- `.clinerules/` (폴더, 여러 파일 분리 가능)

### 적용 방법

1. 프로젝트 루트에 `.clinerules` 파일을 생성합니다.
2. [공통 Rules 템플릿](../rules-template)의 내용을 붙여넣습니다.
3. 허용·금지 라이선스 목록을 사내 정책에 맞게 수정합니다.

### 설정 예시

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

## Aider 설정

### 설정 파일 위치

- `AGENTS.md` (루트, OpenAI Codex 에이전트 규격 호환)
- `.aider.conf.yml` 의 `system_prompt` 항목

### 적용 방법

1. 프로젝트 루트에 `AGENTS.md` 파일을 생성합니다.
2. [공통 Rules 템플릿](../rules-template)의 내용을 붙여넣습니다.
3. 간결한 설정을 원한다면 `.aider.conf.yml`의 `system_prompt`에 핵심 내용만 요약해 작성합니다.

### 설정 예시

**AGENTS.md** — 공통 Rules 템플릿 전체를 그대로 포함합니다.

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

**.aider.conf.yml** — 핵심 내용만 요약해 사용합니다.

```yaml
system_prompt: |
  ## 오픈소스 정책
  허용 라이선스: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
  주의 라이선스 (법무 검토 필요): LGPL, MPL
  금지 라이선스: GPL, AGPL, SSPL, Commons Clause
  CVE 취약점 버전 사용 금지. 의존성 추가 후 audit 실행 권장.
```

---

## 주의사항

:::info 알아두세요
Cline과 Aider 모두 규칙을 Hard Block이 아닌 소프트 가이드라인으로 처리합니다. 정책 위반 패키지를 완전히 차단하려면 CI/CD 파이프라인을 함께 구성해야 합니다. Aider는 CLI 기반으로 동작하므로, `.aider.conf.yml`이 없으면 매 실행 시 `--system-prompt` 플래그로 정책 내용을 직접 전달할 수도 있습니다. 자동화된 CI/CD 게이트 구성 방법은 [Quick CI/CD](../cicd-quick)를 참고하세요.
:::
