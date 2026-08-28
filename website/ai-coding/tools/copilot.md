---
id: copilot
title: GitHub Copilot
sidebar_label: GitHub Copilot
sidebar_position: 3
---

# GitHub Copilot

## 개요

GitHub Copilot은 `.github/copilot-instructions.md` 파일을 저장소 전체에 적용되는 커스텀 지침으로 읽습니다. VS Code, JetBrains, GitHub.com 등 Copilot이 활성화된 모든 환경에 동일하게 적용됩니다. 적용 범위는 저장소 단위입니다.

오픈소스 정책을 이 파일에 작성해 두면, 팀원들이 어떤 편집기를 사용하든 Copilot이 코드를 제안할 때 자동으로 라이선스와 보안 정책을 인지합니다. `.github/` 폴더는 이미 대부분의 저장소에 존재하므로 별도 디렉토리 생성 없이 바로 적용할 수 있다는 장점이 있습니다. 신규 저장소를 생성할 때마다 이 파일을 포함한 기본 템플릿을 함께 복사하는 것을 권장합니다.

## 설정 파일 위치

- `.github/copilot-instructions.md` — 단일 파일, 저장소 전체 적용
- `.github/instructions/*.instructions.md` — frontmatter 의 `applyTo` 패턴으로 경로 한정 적용 (언어·폴더별 규칙 분리에 적합)
- `AGENTS.md` — 루트 공통 규칙 파일 (가장 가까운 파일 우선)

## 적용 방법

1. `.github/` 폴더가 없으면 생성 후 `copilot-instructions.md` 파일을 만듭니다.
2. [공통 Rules 템플릿](../rules-template)의 내용을 붙여넣습니다.
3. 허용·금지 라이선스 목록을 사내 정책에 맞게 수정합니다.

## 설정 예시

```markdown
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

Copilot 은 실행 위치가 셋으로 나뉘고 격리 수준도 각각 다릅니다. 클라우드 에이전트는 이슈 본문이나 PR 설명을 그대로 읽으므로 거기 심어진 지시가 명령 실행과 외부 통신으로 이어질 수 있고, 로컬 도구는 개발자 단말에서 직접 실행됩니다. 위협 모델 전반은 [에이전트·MCP 도구 거버넌스](../agent-governance)에서 다룹니다.

### 클라우드 에이전트

Copilot 클라우드 에이전트는 GitHub Actions 기반 임시 환경에서 실행되고, 방화벽이 기본으로 켜져 있으며 권장 허용 목록도 기본 적용됩니다. 설정 위치는 조직 또는 저장소의 `Settings > Code, planning, and automation > Copilot > Internet access` 입니다.

| 설정                          | 역할                                               |
| ----------------------------- | -------------------------------------------------- |
| Enable firewall               | 방화벽 사용 여부. 조직 기본값은 저장소 판단에 맡김 |
| Recommended allowlist         | GitHub 가 제공하는 기본 허용 도메인 묶음           |
| Allow repository custom rules | 저장소가 자체 허용 규칙을 추가할 수 있는지 여부    |
| Custom allowlist              | 조직 또는 저장소가 직접 추가하는 허용 도메인       |

한계도 함께 알아두세요. 이 방화벽은 Bash 도구가 실행하는 프로세스에만 적용되고, MCP 서버와 설정 단계(setup steps)에는 적용되지 않습니다.

### Copilot CLI

로컬 샌드박스가 있지만 기본으로 꺼져 있는 실험 기능입니다. `--experimental` 로 실행한 뒤 `/sandbox enable` 로 켭니다. 격리는 프로세스와 파일시스템 수준이며 가상 머신이나 컨테이너가 아닙니다. macOS 는 Seatbelt, Linux 는 bubblewrap 을 사용하고, Windows 는 Insiders 빌드에서만 동작합니다.

도구 승인은 `--allow-tool`, `--deny-tool` 플래그로 지정하고, 승인된 도구와 경로는 `~/.copilot/permissions-config.json` 에, 허용 URL 은 `~/.copilot/settings.json` 의 `allowedUrls` 에 남습니다. `--allow-all-tools` 와 `--yolo` 는 모든 승인을 건너뛰므로 격리 환경 밖에서는 쓰지 마세요.

### VS Code 에이전트 모드

터미널 명령 자동 승인은 `chat.tools.terminal.enableAutoApprove` 로 켜고 `chat.tools.terminal.autoApprove` 에 대상 명령을 적습니다. 도구 전반의 자동 승인은 `chat.tools.global.autoApprove` 입니다(1.104 에서 `chat.tools.autoApprove` 를 대체했고 자동 이전은 없습니다).

샌드박스는 미리보기 기능으로 `chat.agent.sandbox.enabled` 에서 켭니다. macOS, Linux, WSL2 를 지원하고, 네트워크는 `chat.agent.sandbox.allowNetwork`, 파일시스템은 `chat.agent.sandbox.fileSystem.mac` 과 `chat.agent.sandbox.fileSystem.linux` 로 조정합니다.

## 주의사항

:::info 알아두세요
조직(Organization) 설정에서 조직 전체 공통 지침(Custom instructions)을 지원합니다. 다만 적용 범위가 GitHub.com 의 Copilot Chat, 코드 리뷰, 코딩 에이전트에 한정되므로, IDE 전반에 일관 적용하려면 저장소별 지침 파일을 공통 템플릿으로 함께 관리하는 것이 좋습니다. 커스텀 지침은 Chat, 코드 리뷰, 코딩 에이전트에 적용되며 인라인 코드 완성에의 적용은 보장되지 않습니다. 설정 변경 후 반영까지 약간의 지연이 발생할 수 있습니다.
:::
