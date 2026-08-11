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

이 페이지가 [5단계 모델](./strategy)의 **4c** 입니다. 4a 는 스캐너가 걸러 낸 것을 다시
판정하고 4b 는 걸러 내지 못한 영역을 탐색합니다. 둘 다 AI 가 쓴 코드를 봅니다. 4c 는 AI 가
호출하는 것을 보며, 이 경로는 pull request 에 드러나지 않습니다.

:::note 이 페이지의 범위

여기서 다루는 대상은 **개발 과정에서 쓰는 에이전트**입니다. 관리 목적이 개발 환경 보안과 코드
유래 확인이고, 대상이 개발자 워크스테이션이라 상시 감시에 가깝습니다.

**제품에 내장해 출하하는 에이전트**는 요구사항이 다릅니다. 고객에게 나가는 서비스의 구성요소이므로
릴리스마다 산출물을 만들어야 하고, MCP 서버가 런타임 의존성이 되어 제품 SBOM에 등재해야 합니다
(아래 6절). 규제 대응은 [AI 생성 코드의 법적 고려](./legal-considerations)를, AI 시스템 자체의
관리체계는 [ISO/IEC 42001](./iso42001)을 참조하세요.

:::

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
| 도구 (MCP 서버) | tool poisoning, 도구 가장(shadowing), 도구 연쇄 호출        | 서버 allowlist, 도입 전 스캔·반출 경로 판정, 버전 고정   |
| 산출물 (코드)   | 오염된 생성 코드, 취약·금지 라이선스 의존성                 | 기존 CI Hard Block(시크릿, SAST, SCA) — 최후 방어선      |

핵심은 세 면이 상보적이라는 점입니다. 입력·도구 통제가 뚫려도 산출물 게이트가 남고,
산출물 게이트가 놓치는 행위(데이터 유출 등)는 도구 통제가 막습니다.

## 3. 실행 통제 여섯 가지

Microsoft Incident Response 의 권고(2026-06)와 MCP 스펙의 보안 원칙을 실무 규칙으로 옮기면
다섯 가지가 되고, 실제 사건에서 도출한 한 가지를 더해 여섯 가지입니다.

적용 강도는 서버 출처에 따라 나눕니다. 전수 심사가 필요한 것은 첫 행이고, 나머지는 기존 절차에
얹거나 다른 단계에서 처리됩니다.

| 출처                 | 예                                        | 처리                                                        |
| -------------------- | ----------------------------------------- | ----------------------------------------------------------- |
| 외부 커뮤니티 배포판 | npm·PyPI 공개 패키지                      | 전수 승인 심사, 버전 고정과 변경 추적                       |
| 벤더 공식 서버       | GitHub, Atlassian 등 자사 서비스용        | 권한 범위와 반출 경로 확인 중심의 간이 심사                 |
| 사내 자체 개발 서버  | 사내 저장소·이슈 트래커·데이터베이스 연동 | 승인이 아니라 설계 검토 — 권한·노출 범위를 개발 시점에 결정 |
| 개발 도구 번들       | 상용 코딩 에이전트 기본 탑재              | 도구 선정 단계에서 함께 검토                                |

호스팅 플랫폼을 경유해 서버를 도입한다면 플랫폼 자체도 심사 대상입니다. MCP 호스팅 플랫폼
Smithery 에서 경로 순회 취약점이 발견되어 3,000개 이상의 호스팅 서버에 임의 코드 실행이 가능한
상태였던 사례가 있습니다(연구자가 발견해 제보했고 수정됐습니다. 악용 정황은 확인되지 않았습니다).
개별 서버를 심사해도 호스팅 경로가 단일 실패 지점이 될 수 있습니다.

### MCP 서버 allowlist

승인된 서버만 사용하고 "모두 허용"류 설정을 끕니다. 신규 서버는 아래 4절의 스캔을 거쳐
등록합니다.

### 최소 권한

에이전트의 파일·네트워크·명령 실행 범위를 필요한 만큼만 허용합니다.

### 도구 설명 검토

도구 설명은 신뢰된 서버 출처가 아니면 검토 대상입니다. 도입 시점과 갱신 시점 모두 확인합니다
(설명은 서버 업데이트로 바뀔 수 있습니다).

### 버전 고정

에이전트와 MCP 서버도 의존성처럼 버전을 고정하고 변경을 추적합니다. npm `postmark-mcp` 는
1.0.15 까지 정상이던 패키지가 이후 버전(1.0.16부터로 추정)에서 숨은 BCC 로 모든 발신 메일을
외부 주소에 복사했습니다. 최초 승인만으로는 막을 수 없는 유형입니다.

### 고위험 작업 사람 승인과 감사 로그

파일 삭제, 외부 전송, 배포 같은 작업은 자동 승인하지 않고, 도구 호출 이력을 남깁니다.

### 데이터 반출 경로 판정

서버가 어떤 외부 엔드포인트와 통신하는지, 사내 데이터가 그 경로로 나갈 수 있는지를 도입 전에
판정합니다. 위 `postmark-mcp` 는 정확히 이 항목에서 걸릴 수 있었던 유형입니다. 판정 결과는
아래 6절의 방식으로 SBOM 에 기록합니다.

## 4. 자동화 도구

| 통제 지점            | 메인                                        | 대안                                                   |
| -------------------- | ------------------------------------------- | ------------------------------------------------------ |
| 도입 전 스캔         | Snyk agent-scan (Apache-2.0)                | Cisco mcp-scanner (Apache-2.0)                         |
| 운영 중앙 통제       | ToolHive (Stacklok, Apache-2.0)             | MCP Gateway & Registry (agentic-community, Apache-2.0) |
| 에이전트 트래픽 통합 | agentgateway (Linux Foundation, Apache-2.0) | —                                                      |
| 개발자 단말 정책     | 도구 내장 통제 (아래 5절)                   | —                                                      |

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

**에이전트 트래픽 통합 — agentgateway**: solo.io 가 만들어 2025년 8월 Linux Foundation 에 기부한
오픈소스 프록시입니다. 대규모 언어 모델 API 호출, MCP, 에이전트 간 프로토콜(Agent-to-Agent, A2A),
HTTP 를 하나의 데이터 플레인에서 처리합니다. ToolHive 가 MCP 서버의 신뢰 카탈로그와 격리 실행에
초점을 둔다면, agentgateway 는 모델 API 호출까지 포함한 에이전트 트래픽 전체를 한 지점에 모읍니다.
대체재가 아니라 통제 범위가 다른 선택지입니다.

도입 순서는 로그가 먼저입니다. 차단 정책은 나중에 붙여도 그 시점부터 작동하지만, 지나간 기간의
로그는 소급해 만들 수 없습니다. 통제 범위를 확정하기 전이라도 기록부터 시작하세요. 이후 관측만
하는 단계, 경고를 내는 단계, 차단하는 단계로 나누어 올립니다. 차단부터 걸면 우회 경로가 생기고,
우회가 일상이 되면 통제 자체가 무력해집니다.

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

## 6. MCP 서버를 SBOM 에 등재하기

MCP 서버가 런타임 의존성이 되면 SBOM 에 담아야 합니다. CycloneDX 는 `components` 와 별도로
`services` 요소를 두고, 애플리케이션이 호출하는 외부 서비스를 엔드포인트 URI, 인증 요구사항,
신뢰 경계 통과 여부, 데이터 분류와 흐름 방향까지 기술할 수 있게 합니다.

- **원격 MCP 서버** — `services` 에 등재합니다. `endpoints`, `authenticated`,
  `x-trust-boundary`, `trustZone`, `data`(`flow` 방향과 `classification`) 필드를 사용합니다.
- **로컬에서 실행되는 MCP 서버 패키지** — `components` 에 등재하고 일반 의존성과 동일하게 다룹니다.

데이터 흐름 방향을 기술할 수 있다는 점이 3절 6번(데이터 반출 경로 판정)과 직접 연결됩니다.
서버가 어떤 외부 엔드포인트로 무엇을 내보내는지 판정한 결과를 그대로 담을 수 있습니다.

한계도 함께 알아두세요. CycloneDX 1.7 의 `component.type` 열거값에는 MCP 서버 전용 유형이 없고,
도구 오염 같은 MCP 고유 위험을 표현할 필드도 없습니다. 현재로서는 일반 서비스로 등재한 뒤
`properties` 에 조직 자체 정의를 얹는 방식이 됩니다. 자체 정의는 조직 밖에서 통용되지 않으므로
협력사에 요구하기 어렵고, 규제 대응 문서로 쓸 때 설명이 따로 필요합니다.

MCP 서버를 SBOM 에 표현하는 방법에 대한 표준 기구의 공식 지침은 아직 확인되지 않습니다. 위 배치는
기존 명세를 해석해 적용한 것이며 표준화된 관례가 아닙니다. SBOM 생성 실습은
[SBOM 생성](/docs/tools/sbom-generation)에서 진행할 수 있습니다.

## 7. 기존 게이트와의 관계

이 페이지의 통제가 모두 뚫려도, [3단계 CI Hard Block](/devsecops/intro)이 산출물 단계에서
시크릿, 취약점, 금지 라이선스를 기계적으로 차단합니다. 반대로 CI 게이트는 "코드로 남지 않는
행위"(도구를 통한 데이터 유출 등)를 보지 못하므로, 도구 통제와 산출물 게이트는 어느 한쪽으로
대체할 수 없는 상보 관계입니다. [4단계 findings-driven 리뷰](./ai-security-review)는 그 사이에서
도달 가능성 판단을 보탭니다.

## 8. 표준 연계와 출처

ISO/IEC 표준과의 연계는 [ISO 표준 연계](./iso-mapping)를, AI 생성 코드의 저작권과 규제는
[AI 생성 코드의 법적 고려](./legal-considerations)를 참조하세요. 이 주제는 OpenChain KWG
가이드가 아직 다루지 않는 영역으로, 아래 1차 출처를 기반으로 작성했습니다(2026-08 기준).

- MCP 스펙 — [Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) 및 본문의 Security and Trust & Safety 절
- Microsoft Security Blog, [Securing AI agents: When AI tools move from reading to acting](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) (2026-06-30)
- OWASP GenAI Security Project, [LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) / [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) (Incubator 단계)
- Hasan et al., [Model Context Protocol (MCP) at First Glance](https://arxiv.org/abs/2506.13538) — 1,899개 서버 조사(tool poisoning 5.5%)
- Invariant Labs, [MCP Security Notification: Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) (2025-04-01) — 도구 오염 기법 최초 공개
- Snyk, [Malicious MCP Server on npm: postmark-mcp Harvests Emails](https://snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails/) (2025-09-25) — 악성 버전은 1.0.16부터로 추정이며, ActiveCampaign/Postmark 저장소와의 연관은 확인되지 않았습니다
- GitGuardian, [From Path Traversal to Supply Chain Compromise: Breaking MCP Server Hosting](https://blog.gitguardian.com/breaking-mcp-server-hosting/) (2025-10-15) — 침해 사고가 아니라 연구자가 제보해 수정된 취약점
- OWASP CycloneDX, [Specification Overview](https://cyclonedx.org/specification/overview/) / [JSON Schema 1.7](https://cyclonedx.org/schema/bom-1.7.schema.json) — `service` 객체 필드와 `component.type` 열거값
- [Snyk agent-scan](https://github.com/snyk/agent-scan) / [Cisco mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner) / [ToolHive](https://github.com/stacklok/toolhive) / [MCP Gateway & Registry](https://github.com/agentic-community/mcp-gateway-registry) / [agentgateway](https://agentgateway.dev/)
- [Claude Code 설정 문서](https://code.claude.com/docs/en/settings) (managed settings, MCP allowlist)
