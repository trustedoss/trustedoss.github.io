---
id: claude-code
title: Claude Code
sidebar_label: Claude Code
sidebar_position: 1
---

# Claude Code

## 개요

Claude Code는 프로젝트 루트의 `CLAUDE.md`를 세션 시작 시 자동으로 읽어 모든 작업에 컨텍스트로 활용합니다. 하위 폴더에도 `CLAUDE.md`를 둘 수 있으며, 해당 폴더에서 작업할 때 추가로 로드됩니다. 적용 범위는 프로젝트 단위이며, `~/.claude/CLAUDE.md`를 통해 글로벌 설정도 가능합니다.

오픈소스 정책을 `CLAUDE.md`에 작성해 두면, 개발자가 명시적으로 요청하지 않아도 Claude Code가 새 패키지를 추가하거나 코드를 생성할 때 라이선스·보안 정책을 자동으로 고려합니다. 팀 전체가 동일한 저장소를 사용하는 경우 `CLAUDE.md`를 커밋해 두면 모든 팀원에게 일관된 정책이 적용됩니다.

## 설정 파일 위치

- 프로젝트 루트: `CLAUDE.md` (권장)
- 하위 폴더별: `{폴더명}/CLAUDE.md` (보조)
- 글로벌: `~/.claude/CLAUDE.md` (모든 프로젝트 공통)

## 적용 방법

1. 프로젝트 루트에 `CLAUDE.md` 파일을 생성하거나 기존 파일을 엽니다.
2. [공통 Rules 템플릿](../rules-template)의 내용을 붙여넣습니다.
3. 허용·금지 라이선스 목록을 사내 정책에 맞게 수정합니다.

## 설정 예시

```markdown
# 프로젝트 가이드

(기존 프로젝트 지침 내용)

---

## 오픈소스 정책

### 라이선스 관리

**허용 라이선스**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**주의 라이선스** (법무 검토 필요): LGPL, MPL

**금지 라이선스** (사전 승인 없이 사용 불가): GPL, AGPL, SSPL, Commons Clause

<!-- 전체 규칙(보안, SBOM, 저작권 절 포함)은 공통 Rules 템플릿에서 복사 -->

---
```

전문은 [공통 Rules 템플릿](../rules-template)에서 복사하세요. 허용·금지 목록이 바뀌면 정본만 갱신하고 각 도구 파일에 다시 붙여넣으면 됩니다.

## 적용 확인

규칙이 적용됐는지 확인하려면 도구에 물어보세요.

"이 프로젝트에 GPL-3.0 라이선스 패키지를 추가해도 돼?"

규칙이 인식되면 금지 라이선스라는 답과 함께 대안을 제시합니다. 인식하지 못하면 설정 파일 위치와 적용 방법을 다시 확인하세요. 표준 항목과의 연계는 [ISO 표준 연계](../iso-mapping)를 참조하세요.

## 격리와 샌드박싱

### 왜 필요한가

규칙 파일은 에이전트가 어떤 방향으로 코드를 만들지 유도할 뿐, 에이전트가 무엇을 할 수 있는지는 제한하지 않습니다. Claude Code 는 기본 상태에서 파일 도구, MCP 서버, 훅을 모두 호스트에서 그대로 실행합니다. 에이전트가 읽는 이슈, 웹 페이지, 코드 주석에 공격자가 지시를 심어 두면(간접 프롬프트 인젝션) 그 지시가 `.claude/settings.json` 의 훅 설정이나 `.mcp.json` 을 고쳐 다음 세션부터 자동 실행되는 상태를 만들 수 있습니다. 위협 모델 전반은 [에이전트·MCP 도구 거버넌스](../agent-governance)에서 다룹니다.

### 격리 범위 고르기

격리는 켜야 동작하는 선택 기능입니다. 켜지 않으면 아무 제한도 걸리지 않습니다.

| 방식                           | 격리 범위                                         | 준비물      |
| ------------------------------ | ------------------------------------------------- | ----------- |
| 샌드박스 Bash 도구 (내장)      | Bash 명령과 그 자식 프로세스                      | 없음        |
| sandbox runtime                | Claude Code 프로세스 전체 (파일 도구·MCP 서버·훅) | Node 실행   |
| 개발 컨테이너, 커스텀 컨테이너 | 개발 환경 전체                                    | Docker      |
| 가상 머신                      | 운영체제 전체                                     | 가상화 도구 |
| 웹의 Claude Code               | 운영체제 전체 (Anthropic 이 운영)                 | 없음        |

내장 샌드박스 Bash 도구는 Bash 명령만 제한합니다. MCP 서버와 훅은 별도 프로세스라 호스트에서 제한 없이 실행됩니다. MCP 서버와 훅까지 격리하려면 나머지 네 방식 중 하나로 Claude Code 프로세스 전체를 격리 경계 안에 넣어야 합니다.

sandbox runtime 은 베타 연구 프리뷰 단계입니다. `npx @anthropic-ai/sandbox-runtime claude` 로 실행하며, 프로젝트의 `.git/hooks`, `.mcp.json`, `.claude/commands`, `.claude/agents` 와 셸 시작 파일에 대한 쓰기를 기본으로 거부합니다.

### 어떻게 켜는가

세션에서 `/sandbox` 를 실행하면 모드와 예외를 고르는 패널이 열리고, 선택한 값은 `.claude/settings.local.json` 에 저장됩니다. 모든 프로젝트에 적용하려면 `~/.claude/settings.json` 에 직접 씁니다.

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": {"allowWrite": ["~/.kube", "/tmp/build"]},
    "network": {"allowedDomains": ["github.com", "*.npmjs.org"]}
  }
}
```

사전 허용 도메인은 없는 상태가 기본입니다. 목록에 없는 도메인은 그때 승인을 묻고, `sandbox.network.strictAllowlist` 를 켜면 묻지 않고 거부합니다. macOS 는 내장 Seatbelt 를, Linux 와 WSL2 는 `bubblewrap` 과 `socat` 을 사용합니다. Windows 는 네이티브 실행을 지원하지 않으므로 WSL2 에서 실행합니다. 샌드박스를 시작하지 못하면 기본 동작은 경고만 내고 샌드박스 없이 계속 실행하는 것이므로, 실패 시 중단하려면 `sandbox.failIfUnavailable` 을 `true` 로 둡니다.

조직 단위로 강제하려면 관리 설정(`managed-settings.json`)에 같은 키를 넣습니다. 개인 설정으로 덮어쓸 수 없습니다.

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  }
}
```

### 설정 경로 쓰기만 따로 막기

전체 격리를 도입하기 전이라면 권한 규칙으로 설정 파일 변조만 먼저 막을 수 있습니다. 규칙은 deny, ask, allow 순으로 평가되고 먼저 걸린 규칙이 결과를 정하므로, deny 에 넣은 경로는 allow 규칙으로 되살아나지 않습니다.

```json
{
  "permissions": {
    "deny": [
      "Edit(./.claude/**)",
      "Edit(./.mcp.json)",
      "Edit(./.git/hooks/**)"
    ]
  }
}
```

경로 규칙은 `Edit` 과 `Read` 매처만 확인합니다. 같은 경로를 `Write(...)` 로 적으면 규칙이 등록은 되지만 참조되지 않고 시작할 때 경고만 나옵니다.

## 주의사항

:::warning AI 규칙의 한계
`CLAUDE.md`는 프롬프트 토큰으로 소비되므로 내용이 너무 길면 컨텍스트 효율이 저하됩니다. 또한 Claude Code는 규칙을 "권장사항"으로 처리할 뿐, 정책 위반 코드를 Hard Block하지는 않습니다. 실질적인 차단이 필요하다면 CI/CD 파이프라인과 반드시 병행해야 합니다. 실제 게이트키퍼 역할은 파이프라인이 담당하고, `CLAUDE.md`는 AI가 올바른 방향으로 코드를 생성하도록 돕는 보조 수단으로 활용하세요.
:::
