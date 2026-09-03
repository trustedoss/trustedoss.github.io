---
id: codex
title: OpenAI Codex
sidebar_label: OpenAI Codex
sidebar_position: 4
---

# OpenAI Codex

## 개요

Codex 는 `AGENTS.md` 를 지침 파일로 읽습니다. 전역 파일(`~/.codex/AGENTS.md`)을 먼저 읽고, 이어서 Git 저장소 루트부터 현재 작업 디렉터리까지 각 단계의 파일을 순서대로 이어 붙입니다. 현재 디렉터리에 가까운 파일이 뒤에 놓이므로 앞선 지침을 덮습니다. 같은 위치에 `AGENTS.override.md` 가 있으면 그 파일이 `AGENTS.md` 보다 우선합니다.

`AGENTS.md` 는 Cursor, GitHub Copilot, Devin Desktop, Cline 도 지원하는 공통 규격입니다. 오픈소스 정책을 `AGENTS.md` 한 벌로 두면 여러 도구에 같은 규칙이 적용되고, 도구별 파일에는 차이점만 남길 수 있습니다.

## 설정 파일 위치

- `AGENTS.md` (프로젝트 루트, 권장)
- `{하위 디렉터리}/AGENTS.md` (해당 디렉터리에서 작업할 때 추가로 적용)
- `AGENTS.override.md` (같은 위치에서 `AGENTS.md` 보다 우선)
- `~/.codex/AGENTS.md` (전역, 가장 먼저 읽히므로 우선순위는 가장 낮음)

`~/.codex/config.toml` 의 `project_doc_fallback_filenames` 로 `AGENTS.md` 가 없을 때 찾을 파일명을 추가할 수 있고, `project_doc_max_bytes` 로 읽어 들일 최대 크기를 정합니다.

## 적용 방법

1. 프로젝트 루트에 `AGENTS.md` 파일을 생성하거나 기존 파일을 엽니다.
2. [공통 Rules 템플릿](../rules-template)의 내용을 붙여넣습니다.
3. 허용·금지 라이선스 목록을 사내 정책에 맞게 수정합니다.

## 설정 예시

```markdown
## 오픈소스 정책

### 라이선스 관리

<!-- 허용·주의·금지 라이선스 목록과 나머지 규칙 전문은 공통 Rules 템플릿에서 복사 -->
```

전문은 [공통 Rules 템플릿](../rules-template)에서 복사하세요. 허용·금지 목록이 바뀌면 정본만 갱신하고 각 도구 파일에 다시 붙여넣으면 됩니다.

## 적용 확인

규칙이 적용됐는지 확인하려면 도구에 물어보세요.

"이 프로젝트에 GPL-3.0 라이선스 패키지를 추가해도 돼?"

규칙이 인식되면 금지 라이선스라는 답과 함께 대안을 제시합니다. 인식하지 못하면 설정 파일 위치와 적용 방법을 다시 확인하세요. 표준 항목과의 연계는 [ISO 표준 연계](../iso-mapping)를 참조하세요.

## 격리와 샌드박싱

### 왜 필요한가

Codex 는 터미널 명령을 직접 실행하므로, 에이전트가 읽은 콘텐츠에 심어진 지시(간접 프롬프트 인젝션)가 그대로 명령 실행으로 이어질 수 있습니다. 규칙 파일은 이 경로를 막지 못합니다. Codex 는 실행 범위를 `sandbox_mode` 로, 사람이 개입하는 시점을 `approval_policy` 로 나눠 정합니다. 위협 모델 전반은 [에이전트·MCP 도구 거버넌스](../agent-governance)에서 다룹니다.

### 어떻게 켜는가

`~/.codex/config.toml` 에 두 값을 지정합니다.

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = false
writable_roots = ["/tmp/build"]
```

`sandbox_mode` 값은 세 가지입니다. `read-only` 는 읽기만 허용하고, `workspace-write` 는 작업 공간과 `writable_roots` 에 적은 경로에만 쓰기를 허용하며, `danger-full-access` 는 제한을 두지 않습니다. `network_access` 를 `false` 로 두면 샌드박스 안에서 외부 통신이 막힙니다.

`approval_policy` 값은 `untrusted`, `on-request`, `never` 입니다. 구버전의 `on-failure` 는 폐기됐습니다. 대화형 실행에는 `on-request` 를 씁니다. 비대화형 실행에서는 승인을 물을 상대가 없어 `never` 를 쓰게 되는데, 이때는 샌드박스가 유일한 방어선이므로 `sandbox_mode` 를 함께 낮춰 두어야 합니다.

일회성으로 바꾸려면 `--sandbox workspace-write`, `--ask-for-approval on-request` 플래그를 씁니다.

운영체제별 구현은 다릅니다. macOS 는 내장 Seatbelt 를, Linux 와 WSL2 는 `bubblewrap` 을 사용합니다. Windows 는 PowerShell 에서 실행하면 Windows Sandbox 를, WSL2 에서 실행하면 Linux 구현을 사용합니다.

### 관리 대상 기기에서 강제하기

조직이 배포하는 요구사항 파일을 두면 사용자 설정보다 우선합니다. 경로는 Unix 계열이 `/etc/codex/requirements.toml`, Windows 가 `%ProgramData%\OpenAI\Codex\requirements.toml` 입니다. `allowed_sandbox_modes` 로 허용할 샌드박스 강도를, `allowed_approval_policies` 로 허용할 승인 정책을 제한하고, MCP 서버 허용 목록과 플러그인 출처도 함께 잠글 수 있습니다. 사용자 설정이 요구사항과 충돌하면 Codex 가 호환되는 값으로 낮춰 실행하고 사용자에게 알립니다.

## 주의사항

:::info 알아두세요
`AGENTS.md` 는 이어 붙이는 방식이라 하위 디렉터리 파일이 상위 지침을 덮을 수 있습니다. 조직 공통 정책을 반드시 지켜야 한다면 전역 `AGENTS.md` 가 아니라 위의 요구사항 파일로 강제하세요. 규칙 파일은 Hard Block 이 아니므로 CI/CD 게이트와 병행해야 합니다. 구성 방법은 [Quick CI/CD](../cicd-quick)를 참고하세요. 공식 문서 위치는 learn.chatgpt.com/docs 로 이전됐습니다(2026-08 확인).
:::
