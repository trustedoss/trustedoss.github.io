---
id: agent-governance
title: '에이전트와 MCP 도구 거버넌스'
sidebar_label: '에이전트·MCP 도구 거버넌스'
---

# 에이전트와 MCP 도구 거버넌스

Rules(2단계)가 AI가 **무엇을 쓰는지**를, CI 게이트(3단계)가 **산출물**을 통제한다면, 이 페이지는
남은 면을 다룹니다: 에이전트가 **어떤 도구를 호출하고 어떤 입력을 읽는지**입니다. 에이전트가
MCP(Model Context Protocol)로 외부 도구를 연쇄 호출하는 개발 환경에서는, 도구와 프롬프트 자체가
공급망의 입력이 됩니다.

## 1. 왜 필요한가

- **도구 설명이 곧 지시입니다.** MCP 도구의 설명(메타데이터)은 에이전트의 컨텍스트로 들어가므로,
  악성 지시를 숨긴 도구 설명(tool poisoning)은 시스템 프롬프트를 바꾼 것과 같은 효과를 냅니다.
  1,899개 오픈소스 MCP 서버를 조사한 연구에서 5.5%가 MCP 고유의 tool poisoning 을 보였습니다.
- **심어진 프롬프트가 빌드를 조종할 수 있습니다.** 에이전트가 읽는 위치(이슈, 웹 페이지, 코드
  주석)에 공격자가 지시를 심으면 생성되는 코드와 도입되는 패키지가 바뀔 수 있습니다
  (간접 프롬프트 인젝션, OWASP LLM01:2025).
- **에이전트가 수용하는 의존성은 사람의 위협 모델을 거치지 않습니다.** AI 가 제안하고 에이전트가
  설치하는 패키지는 검토 없이 공급망에 들어옵니다.

MCP 스펙 자체도 "도구 설명은 신뢰된 서버에서 온 것이 아니면 신뢰하지 말 것"과 사용자 동의
원칙을 명시하지만, 프로토콜 수준에서 강제할 수 없어 구현자(도입 조직)의 책임이라고 밝히고 있습니다.

## 2. 위협 모델: 세 개의 면과 방어선

| 면              | 위협                                                        | 방어선                                                   |
| --------------- | ----------------------------------------------------------- | -------------------------------------------------------- |
| 입력 (프롬프트) | 간접 프롬프트 인젝션 — 에이전트가 읽는 콘텐츠에 심어진 지시 | 신뢰할 수 없는 콘텐츠 접근 최소화, 고위험 작업 사람 승인 |
| 도구 (MCP 서버) | tool poisoning, 도구 가장(shadowing), 도구 연쇄 호출        | 서버 allowlist, 도입 전 스캔, 도구 설명 검토, 버전 고정  |
| 산출물 (코드)   | 오염된 생성 코드, 취약·금지 라이선스 의존성                 | 기존 CI Hard Block(시크릿, SAST, SCA) — 최후 방어선      |

핵심은 세 면이 상보적이라는 점입니다. 입력·도구 통제가 뚫려도 산출물 게이트가 남고,
산출물 게이트가 놓치는 행위(데이터 유출 등)는 도구 통제가 막습니다.

## 3. 실행 통제 다섯 가지

Microsoft Incident Response 의 권고(2026-06)와 MCP 스펙의 보안 원칙을 실무 규칙으로 옮기면
다음 다섯 가지입니다.

1. **MCP 서버 allowlist** — 승인된 서버만 사용하고 "모두 허용"류 설정을 끕니다. 신규 서버는
   아래 4절의 스캔을 거쳐 등록합니다.
2. **최소 권한** — 에이전트의 파일·네트워크·명령 실행 범위를 필요한 만큼만 허용합니다.
3. **도구 설명 검토** — 도구 설명은 신뢰된 서버 출처가 아니면 검토 대상입니다. 도입 시점과
   갱신 시점 모두 확인합니다(설명은 서버 업데이트로 바뀔 수 있습니다).
4. **버전 고정** — 에이전트와 MCP 서버도 의존성처럼 버전을 고정하고 변경을 추적합니다.
5. **고위험 작업 사람 승인과 감사 로그** — 파일 삭제, 외부 전송, 배포 같은 작업은 자동 승인하지
   않고, 도구 호출 이력을 남깁니다.

## 4. 자동화 도구

| 통제 지점        | 메인                            | 대안                                                   |
| ---------------- | ------------------------------- | ------------------------------------------------------ |
| 도입 전 스캔     | Snyk agent-scan (Apache-2.0)    | Cisco mcp-scanner (Apache-2.0)                         |
| 운영 중앙 통제   | ToolHive (Stacklok, Apache-2.0) | MCP Gateway & Registry (agentic-community, Apache-2.0) |
| 개발자 단말 정책 | 도구 내장 통제 (아래 5절)       | —                                                      |

**도입 전 스캔 — Snyk agent-scan**: MCP 서버, 에이전트 설정, agent skill 에서 prompt injection,
tool poisoning, tool shadowing 등을 탐지합니다(Invariant Labs mcp-scan 의 후속). Snyk API 토큰이
필요하고, 검사 과정에서 MCP 서버를 실제 실행한다는 점에 유의하세요(격리 환경에서 실행 권장).

```bash
# 예: VS Code 의 MCP 설정 검사 (SNYK_TOKEN 필요)
uvx snyk-agent-scan@latest ~/.vscode/mcp.json
```

대안인 Cisco mcp-scanner 는 YARA 규칙, LLM 판정, Cisco AI Defense API 세 엔진을 조합합니다.

```bash
uv tool install --python 3.13 cisco-ai-mcp-scanner
mcp-scanner --scan-known-configs --analyzers yara --format summary
```

**운영 중앙 통제 — ToolHive**: 승인된 MCP 서버의 신뢰 카탈로그를 만들고, 접근 정책과 OIDC/OAuth
인증, 컨테이너 격리 실행(Docker/Podman, Kubernetes Operator), OpenTelemetry 기반 감사를
제공합니다. 조직 규모에서 allowlist 를 사람 손이 아니라 플랫폼으로 관리할 때 도입합니다.
대규모 IdP 연동(Keycloak, Entra ID 등)이 필요하면 MCP Gateway & Registry 를 검토하세요.

## 5. 복붙 자산: Claude Code 조직 정책

Claude Code 는 조직이 배포하는 관리 설정(`managed-settings.json` — macOS
`/Library/Application Support/ClaudeCode/`, Linux `/etc/claude-code/`)으로 개인이 덮어쓸 수 없는
정책을 강제할 수 있습니다. 아래는 MCP allowlist 와 최소 권한의 시작점입니다(현행 공식 문서 기준).

```json
{
  "allowedMcpServers": [
    {"serverName": "github"},
    {"serverName": "sentry"}
  ],
  "allowManagedMcpServersOnly": true,
  "permissions": {
    "deny": ["Bash(curl:*)", "Read(./.env)", "Read(./secrets/**)"]
  },
  "allowManagedHooksOnly": true
}
```

- `allowedMcpServers` 에 없는 서버는 사용할 수 없습니다(빈 배열이면 전면 잠금,
  `deniedMcpServers` 가 우선).
- 도구 호출 단위의 결정적 차단은 PreToolUse hook 으로 구현합니다 —
  [방법 3: Hooks 설정하기](/docs/developer-guide/method3-hooks) 의 스크립트를 그대로 확장할 수 있습니다.
- 다른 도구도 관리자 정책을 제공합니다(예: 도구별 조직 설정에서 MCP 사용 제한). 각 도구의
  관리자 문서를 확인하세요.

## 6. 기존 게이트와의 관계

이 페이지의 통제가 모두 뚫려도, [3단계 CI Hard Block](/devsecops/intro)이 산출물 단계에서
시크릿, 취약점, 금지 라이선스를 기계적으로 차단합니다. 반대로 CI 게이트는 "코드로 남지 않는
행위"(도구를 통한 데이터 유출 등)를 보지 못하므로, 도구 통제와 산출물 게이트는 어느 한쪽으로
대체할 수 없는 상보 관계입니다. [4단계 findings-driven 리뷰](./ai-security-review)는 그 사이에서
도달 가능성 판단을 보탭니다.

## 7. 표준 연계와 출처

ISO/IEC 표준과의 연계는 [ISO 표준 연계](./iso-mapping)를 참조하세요. 이 주제는 OpenChain KWG
가이드가 아직 다루지 않는 영역으로, 아래 1차 출처를 기반으로 작성했습니다(2026-07 기준).

- MCP 스펙 — [Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) 및 본문의 Security and Trust & Safety 절
- Microsoft Security Blog, [Securing AI agents: When AI tools move from reading to acting](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) (2026-06-30)
- OWASP GenAI Security Project, [LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) / [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) (Incubator 단계)
- Hasan et al., [Model Context Protocol (MCP) at First Glance](https://arxiv.org/abs/2506.13538) — 1,899개 서버 조사(tool poisoning 5.5%)
- [Snyk agent-scan](https://github.com/snyk/agent-scan) / [Cisco mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner) / [ToolHive](https://github.com/stacklok/toolhive) / [MCP Gateway & Registry](https://github.com/agentic-community/mcp-gateway-registry)
- [Claude Code 설정 문서](https://code.claude.com/docs/en/settings) (managed settings, MCP allowlist)
