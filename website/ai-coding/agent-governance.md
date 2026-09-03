---
id: agent-governance
title: '에이전트와 MCP 도구 거버넌스'
sidebar_label: '에이전트·MCP 도구 거버넌스'
sidebar_position: 7
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

| 면                        | 위협                                                                    | 방어선                                                                      |
| ------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 입력 (프롬프트·규칙 파일) | 간접 프롬프트 인젝션 — 에이전트가 읽는 콘텐츠와 규칙 파일에 심어진 지시 | 신뢰할 수 없는 콘텐츠 접근 최소화, 규칙 파일 PR 리뷰, 고위험 작업 사람 승인 |
| 도구 (MCP 서버·스킬·확장) | tool poisoning, 도구 가장(shadowing), 도구 연쇄 호출, 악성 패키지 설치  | 서버 allowlist, 도입 전 스캔·반출 경로 판정, 버전 고정, 출처 확인           |
| 산출물 (코드)             | 오염된 생성 코드, 취약·금지 라이선스 의존성                             | 기존 CI Hard Block(시크릿, SAST, SCA) — 최후 방어선                         |

핵심은 세 면이 상보적이라는 점입니다. 입력·도구 통제가 뚫려도 산출물 게이트가 남고,
산출물 게이트가 놓치는 행위(데이터 유출 등)는 도구 통제가 막습니다.

입력 면에서 규칙 파일을 따로 적어 둔 이유가 있습니다. 규칙 파일은 사람이 쓴 설정으로 취급하기
쉬우나 에이전트에게는 매 세션 읽히는 지시문이고, 여기에 심어진 문장은 이후 생성되는 모든 코드
제안에 영향을 줍니다. Rules File Backdoor(Pillar Security, 2025-03-18)는 zero-width joiner 와
Unicode Tags 로 규칙 파일에 보이지 않는 지시를 심는 기법입니다. 숨긴 문자가 PR diff 에 표시되지
않아 포크에서 온 변경도 리뷰를 통과합니다. AIShellJack 연구(arXiv:2509.22040)는 MITRE ATT&CK
70개 기법을 반영한 페이로드 314개로 GitHub Copilot 과 Cursor 를 평가해 공격 성공률 41~84% 를
보고했고, Cursor 를 auto-approve 모드로 쓴 TypeScript 시나리오가 83.4% 로 가장 높았습니다.
점검 방법은 [공통 Rules 템플릿](./rules-template)에 정리해 두었습니다.

설정 파일도 같은 면에 있습니다. MCP 설정 파일은 서버 목록을 적어 둔 선언 파일로 보이지만
실제로 담고 있는 것은 실행 명령입니다. Ox Security 가 2026-04-15 공개한 연구는 공식 MCP SDK
네 종(Python, TypeScript, Java, Rust)의 STDIO 전송이 설정에서 받은 값을 검증 없이 셸로
넘긴다고 보고했습니다. 연구진은 누적 내려받기 1억 5천만 건 이상, 외부에 노출된 서버
7,000개 이상을 근거로 영향 범위를 최대 20만 인스턴스로 추산했고, 중대·높음 등급 CVE 10건이
발급됐습니다. Anthropic 은 이 동작이 의도된 설계이며 입력 정제는 개발자 책임이라고 답해
프로토콜을 바꾸지 않았습니다. MCP 스펙의 보안 모범사례 문서도 같은 위험을 로컬 서버 침해
항목으로 다루며, 클라이언트 설정에 악성 실행 명령을 심는 것을 첫 번째 공격 시나리오로
적어 두었습니다. 방어가 도입 조직 쪽에 남는다는 뜻이므로, MCP 설정 파일은 설정이 아니라
코드 실행 경로로 다뤄야 합니다. 구체적인 처리는 아래 3절에 있습니다.

## 3. 실행 통제 아홉 가지

Microsoft Incident Response 의 권고(2026-06)와 MCP 스펙의 보안 원칙을 실무 규칙으로 옮기면
다섯 가지가 되고, 실제 사건에서 도출한 두 가지를 더하면 일곱 가지입니다. 여기에 명세가 바뀐
인가 계층과 위 전송 계층 연구에서 나온 설정 파일 통제를 더해 아홉 가지입니다.

방향은 국가기관 지침과도 일치합니다. 캐나다 사이버보안센터, 호주 ACSC, 미국 CISA 와 NSA,
뉴질랜드 NCSC, 영국 NCSC 5개국 기관이 2026년 4월 말 공동 발표한
"Careful adoption of agentic AI services" 는 계층 방어와 엄격한 접근 통제로 침해 가능성을
줄이라고 권고하고, 안전한 에이전트 설계와 개발, 안전한 배포, 안전한 운영, 향후 위험 대비
네 영역으로 나누어 지침을 제시합니다. 사내 정책 승인 근거가 필요할 때 인용할 수 있는
국가기관 문서입니다.

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

### 도구·확장 공급망

앞의 여섯 가지는 승인한 도구를 어떻게 쓰는지에 관한 통제입니다. 일곱 번째는 그 도구가 어디서
왔는지를 봅니다. 에이전트가 쓰는 MCP 서버, 에이전트 스킬, IDE 확장은 모두 개발자 권한으로 코드를
실행하는 서드파티 패키지이므로 의존성과 같은 절차로 다뤄야 합니다. 그런데 이들은 lockfile 에
나타나지 않아 기존 SCA 결과에 잡히지 않습니다.

근거는 세 갈래입니다.

- 에이전트 스킬. Snyk 이 스킬 3,984개를 조사한 ToxicSkills 연구(2026-02)에서 13.4%(534개)가
  critical 등급 이슈를 하나 이상 포함했습니다. 사람이 직접 확인한 악성 페이로드 76개 중 91%가
  프롬프트 인젝션 기법을 함께 썼습니다.
- MCP 서버. 위 버전 고정 항목의 `postmark-mcp` 외에 `@lanyer640/mcp-runcommand-server` 가
  2025-09-30 이중 백도어를 담은 채 배포됐습니다. 공식 MCP Registry 는 2025-09-08 공개 이후 여전히
  프리뷰 상태이고, 등재 후 커뮤니티 신고를 받아 처리하는 사후 방식이라 등재된 코드의 안전성을
  인증하지 않습니다. 레지스트리에 있다는 사실은 심사를 통과했다는 뜻이 아닙니다.
- IDE 확장. GlassWorm 은 2025-10 Open VSX 마켓플레이스에서 확산해 설치 3만 5,800건을 기록했고
  2025-11 에 2차로 재발했습니다. 2026-03 에는 전이 의존성을 통한 변형으로 확장 72개가 영향을
  받았고 여기에 Claude Code 와 Codex 를 사칭한 확장이 포함됐습니다. VS Code 마켓플레이스에서는
  MaliciousCorgi 가 2026-01 약 150만 개발자에게 영향을 줬고, JetBrains 마켓플레이스에서도 악성
  AI 플러그인 15개가 2026-06 확인됐습니다.

실무 통제는 네 가지입니다.

- 설치 전 출처 확인. 게시자, 연결된 저장소, 최근 커밋, 다운로드 수의 급증 여부를 봅니다.
  마켓플레이스나 레지스트리 등재는 심사 근거가 아닙니다.
- allowlist 운용. 승인한 MCP 서버·스킬·확장만 쓰게 하고 개인이 임의로 추가하지 못하게 합니다.
  Claude Code 는 아래 5절의 관리 설정으로, VS Code 와 JetBrains 는 각 제품의 조직 정책에서
  확장 allowlist 로 강제할 수 있습니다.
- 정기 감사. 설치된 목록을 주기적으로 다시 확인합니다. 승인 시점에 정상이던 패키지가 나중
  버전에서 바뀌는 것이 위 사례들의 공통점입니다. 4절의 Snyk agent-scan 은 MCP 서버뿐 아니라
  에이전트 설정과 스킬도 검사 대상으로 삼습니다.
- 격리 실행. 격리를 켜지 않은 기본 상태의 Claude Code 는 파일 도구와 MCP 서버, 훅이 호스트에서
  직접 실행됩니다. 내장 샌드박스는 Bash 하위 프로세스만 격리하고 Read·Edit·Write 는 권한 시스템이
  따로 처리하므로, MCP 서버와 훅까지 격리 경계 안에 넣으려면 프로세스 전체를 격리해야 합니다.
  이 격리는 opt-in 이며 `@anthropic-ai/sandbox-runtime`, 개발 컨테이너, 가상 머신, 웹에서 실행하는
  Claude Code 중 하나를 골라 켜야 합니다. 격리를 켜기 전이라도 `permissions.deny` 에
  `.claude/settings.json`·`.mcp.json` 같은 설정 경로를 넣어 두면(deny 가 allow 보다
  우선합니다) 에이전트가 자기 권한을 바꾸는 경로는 개별적으로 막을 수 있습니다.
  이때 규칙은 `Edit(./.mcp.json)` 처럼 `Edit` 으로 적어야 합니다. 공식 문서는 파일 권한을
  `Edit(path)` 와 `Read(path)` 규칙으로만 검사한다고 밝히고 있어, `Write(...)` 나
  `MultiEdit(...)` 로 적은 경로 규칙은 받아들여지되 조회되지 않고 시작 시 경고만 남습니다.
  막았다고 생각한 경로가 실제로는 열려 있는 상태가 되므로 표기를 틀리면 통제가 없는 것과 같습니다.

IDE 확장을 스캔 범위에 넣는 이야기는 [소프트웨어 구성 분석 (SCA)](/devsecops/sca)에서 이어집니다.

### 인가 계층

앞의 일곱 가지가 정리된 뒤 MCP 명세 자체가 인가 방식을 크게 바꿨습니다. 2025-11-25
개정은 OAuth Client ID Metadata Document 를 권장 클라이언트 등록 방식으로 추가하고
OpenID Connect Discovery 기반 인가 서버 탐색을 도입했습니다. 2026-07-28 개정은 초기화
핸드셰이크를 없애 프로토콜을 무상태로 바꾸면서, 인가 응답의 `iss` 값을 기록해 둔 발급자와
대조하도록 요구하고(RFC 9207) 클라이언트 자격증명을 발급 인가 서버 단위로 보관해 다른
서버에 재사용하지 못하게 했습니다. 공격자가 통제하는 인가 서버로 정직한 서버의 인가 코드를
보내게 만드는 혼동 공격(mix-up)을 막는 장치이고, 스펙은 PKCE 만으로는 이 공격을 막을 수
없다고 명시합니다. 같은 개정에서 Dynamic Client Registration(RFC 7591)은 Client ID Metadata
Document 로 대체하는 방향으로 deprecated 처리됐고, 이를 지원하지 않는 인가 서버와의 하위
호환용으로만 남습니다.

조직 단위 도입에는 공식 확장인 Enterprise-Managed Authorization 이 직접 쓰입니다. 사용자가
서버마다 개별 승인하는 대신 사내 IdP 가 접근 대상 서버와 조건을 결정하고, 입사와 퇴사에
따른 권한 부여와 회수를 한 곳에서 처리합니다. 실무 규칙은 세 가지입니다.

- 쓰는 클라이언트와 서버가 어느 개정을 구현하는지 확인합니다. 무상태 전환은 하위 호환이
  깨지는 변경이라 도입 시점의 버전 조합을 기록해 두어야 합니다.
- 새로 도입하는 클라이언트는 Dynamic Client Registration 대신 Client ID Metadata Document
  를 쓰게 합니다.
- 사내 IdP 가 있으면 서버별 개별 승인 대신 Enterprise-Managed Authorization 경로로 모읍니다.
  확장은 기본으로 켜지지 않으므로 쓰려는 클라이언트가 지원하는지 먼저 확인해야 합니다.

### 설정 파일을 코드 실행 경로로 다루기

2절의 STDIO 전송 결함은 프로토콜이 고쳐 주지 않으므로 운영에서 막아야 합니다. `.mcp.json`
과 IDE 의 MCP 설정처럼 서버 실행 명령을 담은 파일은 소스 코드와 같은 취급을 받아야 합니다.

- 설정 파일을 저장소에 두고 변경을 PR 로 드러냅니다. 5절에서 `.mcp.json` 을 커밋하라고 한
  이유가 여기에도 그대로 적용됩니다.
- 설정 값에 사용자 입력이나 외부에서 받은 문자열을 넣지 않습니다. 에이전트가 자기 설정
  파일을 쓰지 못하게 막는 것도 같은 항목입니다. `permissions.deny` 로 설정 경로 쓰기를
  차단하는 방법은 위 격리 실행 항목에 있습니다.
- 서버를 셸을 거쳐 띄우지 않고 실행 파일과 인자를 분리해 넘기는 형태를 씁니다.
- 쓰는 SDK 버전을 확인하고 관련 CVE 수정본 이상으로 올립니다. 서버를 직접 만드는 경우에도
  같습니다.

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

### 저장소 수준으로 줄인 형태

관리 설정을 배포할 수 없는 상황에서는 저장소에 커밋하는 설정만으로 시작할 수 있습니다.
[ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice) 저장소가
그 형태를 담고 있습니다.

| 파일                                                                                                           | 담은 통제                                                       |
| -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [.mcp.json](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.mcp.json)                         | 승인한 서버 선언. 현재 비어 있음                                |
| [.claude/settings.json](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.claude/settings.json) | 서버 자동 승인 차단, 시크릿 읽기 차단, 외부 통신·배포 명령 승인 |
| [CLAUDE.md](https://github.com/trustedoss/ai-coding-best-practice/blob/main/CLAUDE.md)                         | 도구 설명 검토와 반출 경로 판정 절차, 서버 추가 방법            |

주의할 차이가 있습니다. 위 관리 설정 예시에서 저장소 설정으로 옮겨도 그대로 동작하는 것과
그렇지 않은 것이 갈립니다. 공식 설정 문서 기준으로 `allowedMcpServers`·`deniedMcpServers`,
`enabledMcpjsonServers`·`disabledMcpjsonServers`, `enableAllProjectMcpServers`,
`disableClaudeAiConnectors` 는 모두 관리 설정뿐 아니라 사용자·프로젝트 설정 파일에서도
적용됩니다. 관리 설정에서만 동작하는 것은 `allowManagedMcpServersOnly` 이며, 이것을 저장소
설정에 넣으면 무시됩니다. 개인이 덮어쓸 수 없게 만드는 강제력은 관리 설정에서 나오므로,
저장소 설정은 기본값을 세우는 자리이지 우회를 막는 자리가 아닙니다.

`enableAllProjectMcpServers` 는 `.mcp.json` 의 모든 서버를 프롬프트 없이 승인하는 설정이라
기본값 `false` 를 그대로 두는 편이 낫습니다. `.mcp.json` 을 저장소에 두는 이유는 서버 추가가
개인 설정이 아니라 PR diff 로 드러나게 하기 위해서입니다.

아홉 통제 가운데 도구 설명 검토, 데이터 반출 경로 판정, 도구·확장의 출처 확인은 파일로
표현되지 않습니다. 사람이 판단하는 절차이므로 규칙으로 적어 두고 결과를 PR 에 남기는 방식으로
다룹니다.

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

표준 쪽 논의는 진행 중입니다. CycloneDX 사양 저장소에 에이전트가 쓰는 MCP 서버, 도구 정의,
모델, 신원 자격증명을 함께 담는 Agent Bill of Materials 제안이 올라왔습니다(이슈 #895,
2026-03-26 개설). 이 이슈는 2026-04-29 중복으로 닫혔고, 유지관리자는 에이전틱 AI 를
Blueprints 와 위협 모델링 워킹그룹의 진행 중인 작업에서 다루고 있다고 밝혔습니다. 필요성은
논의 대상이 됐으나 전용 컴포넌트 타입을 새로 만들지, 다른 방식으로 표현할지는 아직 정해지지
않았습니다.

MCP 서버를 SBOM 에 표현하는 방법에 대한 표준 기구의 공식 지침은 아직 확인되지 않습니다. 위 배치는
기존 명세를 해석해 적용한 것이며 표준화된 관례가 아닙니다. 결론이 나오기 전까지는 위 배치를
유지하되, 조직 자체 정의를 쓰더라도 어떤 항목을 무엇으로 기록했는지 남겨 두면 나중에 표준
표현으로 옮기기 쉽습니다. SBOM 생성 실습은
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

프레임워크 쪽에서 참고할 산출물이 둘 늘었습니다. OWASP Top 10 for Agentic Applications
2026(2025-12-09 공개)은 에이전트 목표 탈취, 도구 오용, 신원과 권한 남용, 메모리 오염,
안전하지 않은 에이전트 간 통신, 연쇄 실패, 신뢰 악용, 통제를 벗어난 에이전트를 위험 범주로
정리해 위 2절의 위협 모델과 겹칩니다. OWASP AISVS 1.0(2026-06 공개)은 성격이 다릅니다.
인식 목록이 아니라 검증 가능한 요구사항 카탈로그이고, 12개 장 가운데 9장이 오케스트레이션과
에이전틱 액션, 10장이 MCP 보안입니다. 각 요구사항에 1에서 3까지 검증 레벨이 붙어 있어
조직이 목표 레벨을 정하고 그대로 자체 인증 체크리스트로 옮길 수 있습니다. 예를 들어 10장은
MCP 구성요소를 신뢰할 수 있는 출처에서만 받아 암호학적으로 검증할 것(레벨 1), allowlist 된
서버만 허용할 것(레벨 2), 로컬에서 띄우는 서버를 최소 권한 샌드박스에서 실행할 것(레벨 2)을
요구하는데, 위 3절의 통제와 그대로 대응합니다.

- MCP 스펙 — [Security Best Practices](https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices) 및 본문의 Security and Trust & Safety 절. 현행 개정은 2026-07-28 이며 인가 관련 변경은 [2025-11-25 변경 목록](https://modelcontextprotocol.io/specification/2025-11-25/changelog)과 [2026-07-28 변경 목록](https://modelcontextprotocol.io/specification/2026-07-28/changelog)에 있습니다
- MCP 공식 확장 — [Enterprise-Managed Authorization](https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization) (stable) — 사내 IdP 가 MCP 서버 접근을 중앙에서 결정하는 방식
- Ox Security, [The Mother of All AI Supply Chains](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/) (2026-04-15) — 공식 SDK 네 종의 STDIO 전송 결함, CVE 10건, 최대 20만 인스턴스 추산
- Canadian Centre for Cyber Security 외, [Careful adoption of agentic AI services](https://www.cyber.gc.ca/en/news-events/joint-guidance-careful-adoption-agentic-artificial-intelligence-services) (2026-05-01 게시) — 캐나다, 호주, 미국, 뉴질랜드, 영국 5개국 기관의 공동 지침
- Microsoft Security Blog, [Securing AI agents: When AI tools move from reading to acting](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) (2026-06-30)
- OWASP GenAI Security Project, [Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) (2025-12-09) / [LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) (2026-08-03, 본문에서 인용한 LLM01:2025 를 잇는 개정판) / [LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) / [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) (Incubator 단계)
- OWASP, [AISVS 1.0](https://github.com/OWASP/AISVS) (2026-06) — 9장 오케스트레이션과 에이전틱 액션, 10장 MCP 보안, 검증 레벨 1~3
- CycloneDX, [Proposal: Agent Bill of Materials](https://github.com/CycloneDX/specification/issues/895) (2026-03-26 개설, 2026-04-29 중복 처리) — 에이전트 전용 BOM 논의 경과
- Hasan et al., [Model Context Protocol (MCP) at First Glance](https://arxiv.org/abs/2506.13538) — 1,899개 서버 조사(tool poisoning 5.5%)
- Invariant Labs, [MCP Security Notification: Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) (2025-04-01) — 도구 오염 기법 최초 공개
- Snyk, [Malicious MCP Server on npm: postmark-mcp Harvests Emails](https://snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails/) (2025-09-25) — 악성 버전은 1.0.16부터로 추정이며, ActiveCampaign/Postmark 저장소와의 연관은 확인되지 않았습니다
- GitGuardian, [From Path Traversal to Supply Chain Compromise: Breaking MCP Server Hosting](https://blog.gitguardian.com/breaking-mcp-server-hosting/) (2025-10-15) — 침해 사고가 아니라 연구자가 제보해 수정된 취약점
- OWASP CycloneDX, [Specification Overview](https://cyclonedx.org/specification/overview/) / [JSON Schema 1.7](https://cyclonedx.org/schema/bom-1.7.schema.json) — `service` 객체 필드와 `component.type` 열거값
- Pillar Security, [New Vulnerability in GitHub Copilot and Cursor: How Hackers Can Weaponize Code Agents](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents) (2025-03-18) — Rules File Backdoor
- Liu et al., ["Your AI, My Shell": Demystifying Prompt Injection Attacks on Agentic AI Coding Editors](https://arxiv.org/abs/2509.22040) — AIShellJack, 페이로드 314개, 성공률 41~84%
- Snyk, [ToxicSkills: Malicious AI Agent Skills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) (2026-02) — 스킬 3,984개 중 13.4%가 critical 등급 이슈
- Model Context Protocol Blog, [Introducing the MCP Registry](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/) (2025-09-08) — 프리뷰 공개와 신고 기반 사후 조치 방식
- Koi Security, [GlassWorm: First Self-Propagating Worm Using Invisible Code Hits OpenVSX Marketplace](https://www.koi.ai/blog/glassworm-first-self-propagating-worm-using-invisible-code-hits-openvsx-marketplace) (2025-10-18) / [MaliciousCorgi](https://www.koi.ai/blog/maliciouscorgi-the-cute-looking-ai-extensions-leaking-code-from-1-5-million-developers) (2026-01-22)
- [Snyk agent-scan](https://github.com/snyk/agent-scan) / [Cisco mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner) / [ToolHive](https://github.com/stacklok/toolhive) / [MCP Gateway & Registry](https://github.com/agentic-community/mcp-gateway-registry) / [agentgateway](https://agentgateway.dev/)
- [Claude Code 설정 문서](https://code.claude.com/docs/en/settings) (managed settings, MCP allowlist) / [샌드박스 문서](https://code.claude.com/docs/en/sandboxing) / [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments) — 격리 범위와 opt-in 방식
