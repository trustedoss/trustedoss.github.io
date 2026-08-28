---
id: cursor
title: Cursor
sidebar_label: Cursor
sidebar_position: 2
---

# Cursor

## 개요

Cursor는 `.cursor/rules/` 폴더 내 `.mdc` 파일을 규칙으로 인식해 AI 동작에 반영합니다. 파일별로 적용 범위(glob 패턴)를 지정할 수 있어 언어·폴더별로 규칙을 분리 관리할 수 있습니다. 적용 범위는 프로젝트 단위입니다.

오픈소스 정책 규칙 파일을 `.cursor/rules/oss-policy.mdc`로 별도 분리해 두면, 다른 개발 가이드라인과 독립적으로 관리하고 필요 시 쉽게 비활성화할 수 있습니다. `globs` 패턴으로 적용 대상 파일을 한정하면 불필요한 컨텍스트 소비를 줄일 수 있습니다. 저장소에 커밋해 두면 팀 전체에 동일한 정책이 자동으로 적용됩니다. 규칙 파일이 여러 개인 경우 목적별로 파일명을 명확히 구분해 관리하면 유지보수가 쉬워집니다.

## 설정 파일 위치

- `.cursor/rules/oss-policy.mdc` (권장)
- `.cursorrules` (루트 단일 파일, 레거시)
- `AGENTS.md` (루트와 하위 디렉토리 중첩 지원 — 공통 규칙 파일 대안)

## 적용 방법

1. `.cursor/rules/oss-policy.mdc` 파일을 생성합니다.
2. [공통 Rules 템플릿](../rules-template)의 내용을 붙여넣습니다.
3. 허용·금지 라이선스 목록을 사내 정책에 맞게 수정합니다.

## 설정 예시

```markdown
---
description: 오픈소스 라이선스 및 보안 정책
globs: ['**/*.{js,ts,py,go,java}']
alwaysApply: true
---

## 오픈소스 정책

### 라이선스 관리

**허용 라이선스**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**주의 라이선스** (법무 검토 필요): LGPL, MPL

**금지 라이선스** (사전 승인 없이 사용 불가): GPL, AGPL, SSPL, Commons Clause

<!-- 전체 규칙(보안, SBOM, 저작권 절 포함)은 공통 Rules 템플릿에서 복사 -->
```

전문은 [공통 Rules 템플릿](../rules-template)에서 복사하세요. 허용·금지 목록이 바뀌면 정본만 갱신하고 각 도구 파일에 다시 붙여넣으면 됩니다.

## 적용 확인

규칙이 적용됐는지 확인하려면 도구에 물어보세요.

"이 프로젝트에 GPL-3.0 라이선스 패키지를 추가해도 돼?"

규칙이 인식되면 금지 라이선스라는 답과 함께 대안을 제시합니다. 인식하지 못하면 설정 파일 위치와 적용 방법을 다시 확인하세요. 표준 항목과의 연계는 [ISO 표준 연계](../iso-mapping)를 참조하세요.

## 격리와 샌드박싱

### 왜 필요한가

규칙 파일은 에이전트가 어떤 코드를 만들지 유도할 뿐, 에이전트가 실행할 수 있는 명령과 접근할 수 있는 경로를 제한하지 않습니다. 에이전트가 읽는 이슈나 문서에 공격자가 지시를 심어 두면(간접 프롬프트 인젝션) 그 지시가 터미널 명령 실행으로 이어질 수 있습니다. 위협 모델 전반은 [에이전트·MCP 도구 거버넌스](../agent-governance)에서 다룹니다.

### 두 계층으로 나뉩니다

Cursor 의 통제는 실행 승인과 샌드박스 두 계층입니다.

- 실행 승인(Run Mode): Auto-review, Allowlist, Run Everything 세 가지 중 하나를 고릅니다. Allowlist 는 미리 등록한 명령만 자동 실행합니다.
- 샌드박스: 승인 계층 위에 얹히는 운영체제 수준 격리입니다. macOS 는 Seatbelt(`sandbox-exec`)를, Linux 는 Landlock 으로 파일시스템을, seccomp 로 위험한 시스템 호출을 제한합니다. Linux 는 커널 6.2 이상과 Landlock v3, unprivileged user namespace 가 필요하고, 조건이 맞지 않으면 명령 실행 전에 승인을 묻는 방식으로 되돌아갑니다. Windows 는 WSL2 안에서 Linux 샌드박스를 실행합니다.

### 어떻게 켜는가

`Settings > Agents > Approvals & Execution` 에서 Run Mode 와 샌드박스를 지정합니다. 샌드박스의 네트워크 정책은 세 가지입니다. `sandbox.json Only` 는 직접 적은 목록만 허용하고, 기본값인 `sandbox.json + Defaults` 는 내장 허용 목록(약 110개 도메인)을 함께 적용하며, `Allow All` 은 제한을 두지 않습니다. 기본 정책은 거부이므로 목록에 없는 도메인은 막힙니다.

설정은 파일로도 남습니다. `~/.cursor/permissions.json` 이 명령·MCP 서버 허용 목록(`terminalAllowlist`, `mcpAllowlist`, `autoRun`)을, `~/.cursor/sandbox.json` 이 샌드박스 유형과 네트워크 정책(`networkPolicy`, `additionalReadwritePaths`)을 담습니다. 조직 정책은 Enterprise 대시보드의 Auto Run Configuration 과 Cloud Agent 의 Lock Network Access Policy 로 강제하며, 팀 관리자 설정이 개인의 `permissions.json` 과 편집기 설정보다 우선합니다.

명령 단위로 확실히 막아야 한다면 `.cursor/hooks.json` 의 `beforeShellExecution` 훅을 씁니다. 훅이 종료 코드 2 를 반환하면 해당 명령은 실행되지 않습니다.

## 주의사항

:::info 알아두세요
`alwaysApply: true`로 설정하면 모든 파일에 규칙이 적용되어 토큰 사용량이 증가할 수 있습니다. 정책 규칙처럼 항상 적용이 필요한 경우에는 `alwaysApply: true`를, 특정 언어나 폴더에만 필요한 규칙은 `globs` 패턴으로 범위를 한정하는 것이 효율적입니다. `.cursorrules`(레거시)와 `.cursor/rules/`를 동시에 사용하는 경우 `.cursor/rules/`가 우선 적용되므로, 신규 프로젝트에서는 `.cursor/rules/` 방식을 권장합니다.
:::
