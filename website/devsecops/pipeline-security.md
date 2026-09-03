---
id: pipeline-security
title: 파이프라인 자체 보안과 빌드 출처
sidebar_label: 파이프라인 자체 보안
sidebar_position: 10
---

# 파이프라인 자체 보안과 빌드 출처

이 가이드의 다른 페이지는 파이프라인이 무엇을 검사하는지를 다룹니다. 이 페이지는 그 파이프라인 자체를 어떻게 지키는지를 다룹니다.
SAST, SCA, 시크릿 스캔을 아무리 촘촘하게 걸어도 그 검사를 실행하는 워크플로가 공격자의 코드를 실행하고 있으면 결과는 신뢰할 수 없습니다.

:::tip 아래 설정은 예시입니다. 작동하는 전체 구현은 참조 저장소에
이 페이지의 YAML과 명령은 핵심을 보여주는 예시입니다. 복사해 바로 쓸 수 있는 전체 파이프라인(정책 파일, 샘플 앱 포함)은 [Best Practice 저장소](/ai-coding/best-practice-repo)에서 확인하세요.
:::

## 왜 파이프라인 자체가 표적이 되는가

CI 러너는 저장소 시크릿, 클라우드 자격증명, 배포 권한을 한자리에 모아 둔 실행 환경입니다.
애플리케이션 코드를 뚫는 것보다 그 코드를 빌드하는 워크플로를 뚫는 쪽이 얻는 것이 훨씬 많습니다.

:::info 워크플로가 참조하는 태그는 언제든 다른 커밋을 가리킬 수 있습니다
`uses: owner/repo@v45` 는 "v45 라는 이름표가 지금 가리키는 커밋"을 실행하라는 뜻입니다.
그 이름표는 저장소 소유자가 아무 때나 다른 커밋으로 옮길 수 있습니다.
:::

**tj-actions/changed-files (2025-03, CVE-2025-30066).** 널리 쓰이던 GitHub Action의 태그가 악성 커밋
`0e58ed86` 로 재지정됐습니다. `v1.0.0`, `v35.7.7-sec`, `v44.5.1` 을 포함한 여러 태그가 같은 커밋을
가리키게 바뀌었고, 그 커밋의 스크립트가 러너 워커 프로세스 메모리에서 시크릿을 추출해 워크플로 로그에
평문으로 출력했습니다. 로그가 공개된 저장소에서는 API 키, 클라우드 자격증명, SSH 키가 그대로 노출됐습니다.
영향받은 저장소는 2만 3천 개가 넘습니다. 애플리케이션 코드는 한 줄도 바뀌지 않았습니다.

**Trivy Action 컴포지트 액션 스크립트 인젝션 (2026-02-18, GHSA-9p44-j4g5-cfx5).** 널리 쓰이는
보안 스캐너 Action 자체에서도 취약점이 나왔습니다. 컴포지트 액션이 환경 파일을 `source`로
불러오는 방식이라, 그 파일 내용을 제어할 수 있는 공격자가 임의 명령을 실행할 수 있었습니다.
보안 스캔을 위해 넣은 워크플로 단계 자체가 검증 대상에서 빠지면 그 자체가 침투 경로가 됩니다.

**Trivy 생태계 공급망 침해 (2026-03-19, GHSA-69fq-xp46-6x23).** 같은 Action이 한 달 뒤 전혀 다른
방식으로 다시 뚫렸습니다. 공격자가 탈취한 자격증명으로 `aquasecurity/trivy-action`의 태그 77개 중
76개를 악성 커밋으로 강제 재지정했고, `aquasecurity/setup-trivy`의 태그 7개는 전부 교체했으며,
악성 Trivy v0.69.4 릴리스를 배포했습니다. trivy-action의 노출 창은 2026-03-19 17:43부터
2026-03-20 05:40까지 약 12시간이었습니다(UTC 기준). 앞의 스크립트 인젝션과는 별개의 사건입니다.

세 사건이 보여주는 공통 교훈은, 워크플로가 실행하는 참조와 입력값 모두 검증 대상이라는
것입니다. tj-actions와 2026-03 Trivy 침해는 내용이 고정되지 않은 태그 참조가, 2026-02 Trivy
Action 취약점은 검증 없이 신뢰한 입력값이 문제였습니다. 한 저장소가 두 경로 모두로 뚫릴 수
있다는 점도 함께 보아야 합니다. 도구가 보안 도구라는 사실은 면제 사유가 되지 않습니다.

---

## 커밋 SHA 고정

가변 태그 대신 40자리 커밋 SHA로 참조하면 태그를 재지정해도 실행되는 코드가 바뀌지 않습니다.
사람이 읽을 수 있도록 원래 버전은 주석으로 남깁니다.

다만 고정은 고정한 참조까지만 보호합니다. 2026-03 Trivy 침해 권고는 SHA로 고정했더라도 그 시점의
trivy-action이 자신이 호출하는 액션을 고정해 두지 않았다면 악성 `setup-trivy`를 그대로 끌어왔다고
밝혔습니다. 고정한 액션이 내부에서 무엇을 다시 호출하는지까지 봐야 합니다.

```yaml
# .github/workflows/ci.yml

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # 권장하지 않음. 태그는 다른 커밋으로 재지정될 수 있습니다
      - uses: actions/checkout@v7

      # 권장. 내용이 고정됩니다
      - uses: actions/checkout@<40자리 커밋 SHA> # v7
      - uses: aquasecurity/trivy-action@<40자리 커밋 SHA> # v0.36.0
```

태그에 대응하는 SHA는 아래처럼 확인합니다.

```bash
# 특정 태그가 현재 가리키는 커밋 SHA 조회
gh api repos/actions/checkout/git/ref/tags/v7 --jq '.object.sha'

# 저장소 전체 워크플로에서 태그 참조를 한 번에 찾기
grep -rn "uses: .*@v[0-9]" .github/workflows/
```

### 고정한 SHA를 낡은 채로 두지 않기

SHA를 고정하면 보안 패치도 함께 멈춥니다. 이 문제는 자동 갱신 도구로 해결합니다.
Dependabot과 Renovate 둘 다 SHA 고정 참조를 인식해서 새 릴리스의 SHA로 올리는 PR을 만들고,
주석의 버전 표기도 함께 갱신합니다.

```yaml
# .github/dependabot.yml

version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

Renovate를 쓴다면 `helpers:pinGitHubActionDigests` 프리셋으로 기존 태그 참조를 SHA 고정으로
한 번에 바꾸고, 이후 갱신도 같은 형태로 유지할 수 있습니다.

```json
// renovate.json

{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    "helpers:pinGitHubActionDigests"
  ]
}
```

두 도구의 차이는 [모니터링과 자동 교정](./monitoring) 페이지의 비교표를 참고하세요.

---

## 워크플로 권한 최소화

GitHub Actions의 `GITHUB_TOKEN` 은 워크플로 실행마다 자동으로 발급됩니다.
저장소 설정에 따라 이 토큰에 쓰기 권한이 있으면, 침해된 액션 하나가 저장소 내용을 고칠 수 있습니다.

워크플로 최상단에서 전체를 읽기 전용으로 내리고, 쓰기가 필요한 job에만 필요한 범위를 개별로 부여합니다.

```yaml
# .github/workflows/ci.yml

name: CI

on:
  pull_request:
    branches: [main]

# 워크플로 전체 기본값. 명시하지 않은 권한은 모두 none 이 됩니다
permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    # 상속받은 contents: read 만 사용합니다
    steps:
      - uses: actions/checkout@<40자리 커밋 SHA> # v7
        with:
          # 이후 단계가 토큰을 재사용하지 못하게 합니다
          persist-credentials: false
      - run: npm ci && npm test

  sast:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      # SARIF 업로드에만 필요한 권한을 이 job 에서만 엽니다
      security-events: write
    steps:
      - uses: actions/checkout@<40자리 커밋 SHA> # v7
```

`permissions: {}` 로 시작해 필요한 것만 더하는 방식이 더 엄격합니다.
저장소 설정에서도 Settings의 Actions 메뉴에서 `GITHUB_TOKEN` 기본 권한을 읽기 전용으로 바꿔 두세요.

### pull_request_target 을 쓸 때의 주의

`pull_request` 이벤트는 포크에서 온 PR을 시크릿 없는 읽기 전용 환경에서 실행합니다.
`pull_request_target` 은 반대로 대상 저장소의 시크릿과 쓰기 권한을 가진 채로 실행됩니다.
여기서 PR 브랜치의 코드를 체크아웃해 실행하면, 외부인이 보낸 코드가 저장소 시크릿을 쥐고 돌아갑니다.

```yaml
# 위험한 조합. 이렇게 쓰지 마세요
on: pull_request_target

jobs:
  build:
    steps:
      - uses: actions/checkout@<40자리 커밋 SHA> # v7
        with:
          # 포크의 코드를 시크릿이 있는 환경에서 체크아웃합니다
          ref: ${{ github.event.pull_request.head.sha }}
      - run: npm ci # 포크가 넣은 install 훅이 여기서 실행됩니다
```

`pull_request_target` 은 PR 라벨링이나 코멘트처럼 PR 코드를 실행하지 않는 작업에만 쓰고,
포크 코드를 빌드해야 한다면 `pull_request` 를 쓰거나 승인된 실행(Approval required)을 거치게 하세요.

---

## zizmor로 워크플로를 검사하기

[zizmor](https://github.com/zizmorcore/zizmor)는 GitHub Actions 워크플로 YAML을 정적 분석하는 도구입니다.
Rust로 작성됐고 MIT 라이선스이며, 위에서 다룬 문제를 자동으로 찾아냅니다.

| 탐지 항목        | 내용                                                       |
| ---------------- | ---------------------------------------------------------- |
| 템플릿 인젝션    | `${{ }}` 로 받은 값이 셸 명령에 그대로 들어가는 경로       |
| 자격증명 잔존    | 체크아웃 토큰이 이후 단계에 남아 재사용될 수 있는 설정     |
| 과도한 권한      | job 이 실제로 쓰지 않는 쓰기 권한까지 부여받은 경우        |
| 위장 커밋과 참조 | 포크에서 밀어 넣은 커밋을 정상 참조로 착각하게 만드는 형태 |

`.github/workflows/` 를 대상으로 실행하며 SARIF로 결과를 내보내면 GitHub Security 탭에 집계됩니다.

```bash
# 로컬 실행
zizmor .github/workflows/

# SARIF 출력
zizmor --format=sarif .github/workflows/ > zizmor.sarif
```

CI에는 공식 액션으로 붙입니다. 자기 자신도 SHA 고정과 최소 권한을 지키는 형태입니다.

```yaml
# .github/workflows/zizmor.yml

name: Workflow Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: ['**']

permissions: {}

jobs:
  zizmor:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      actions: read
      security-events: write
    steps:
      - uses: actions/checkout@<40자리 커밋 SHA> # v7
        with:
          persist-credentials: false

      - uses: zizmorcore/zizmor-action@<40자리 커밋 SHA> # v0.2.0
```

zizmor는 심각도에 따라 종료 코드를 다르게 반환하므로, 처음에는 결과만 보고 넘기다가
기존 지적 사항을 정리한 뒤 차단 게이트로 올리는 순서를 권합니다.

---

## 빌드 출처와 서명

앞의 세 절은 파이프라인이 침해되지 않도록 막는 예방입니다.
빌드 출처(provenance)와 서명은 그다음 질문에 답합니다. 지금 손에 든 이 아티팩트가 정말 그 파이프라인에서 나온 것인가.

| 계층           | 무엇을 해결하는가                                                                                             | 대표 구현                     |
| -------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| 빌드 출처 증명 | 이 아티팩트가 어느 저장소의 어느 커밋에서 어떤 빌드 과정을 거쳐 나왔는지를 기계가 확인 가능한 형태로 남깁니다 | SLSA provenance, in-toto 증명 |
| 게시 인증      | 장기 유효 토큰을 없애 토큰 탈취로 패키지를 게시하는 경로를 차단합니다                                         | npm trusted publishing (OIDC) |
| 아티팩트 서명  | 배포된 이미지나 파일이 게시 이후 바뀌지 않았음을 검증합니다                                                   | Sigstore, cosign              |

### SLSA 빌드 트랙

[SLSA](https://slsa.dev/spec/)는 빌드 과정의 신뢰 수준을 단계로 정의한 프레임워크입니다.
현행 사양은 v1.2이고, 빌드 트랙은 세 단계로 되어 있습니다.

| 레벨     | 요구사항                                                                                                    |
| -------- | ----------------------------------------------------------------------------------------------------------- |
| Build L1 | 빌드 과정을 일관되게 유지하고 출처 증명을 함께 배포합니다                                                   |
| Build L2 | 호스팅된 빌드 플랫폼이 증명을 직접 생성하고 서명합니다. 소비자는 서명을 검증합니다                          |
| Build L3 | 빌드 실행끼리 서로 영향을 주지 못하도록 격리하고, 서명 키를 사용자 정의 빌드 단계에서 접근할 수 없게 합니다 |

v1.2에는 빌드 트랙 외에 소스 트랙이 추가돼 소스 저장소 자체의 통제 수준도 다룹니다.

### npm trusted publishing

npm은 GitHub Actions, GitLab CI/CD, CircleCI에서 OIDC로 인증해 패키지를 게시하는 방식을 지원합니다.
저장소 시크릿에 장기 유효 npm 토큰을 두지 않아도 되므로, 토큰이 유출돼 악성 버전이 게시되는 경로가 사라집니다.
GitHub Actions와 GitLab CI/CD에서 게시하면 출처 증명이 자동으로 함께 게시됩니다.
다만 자체 호스팅 러너는 아직 지원 대상이 아닙니다.

### Sigstore와 cosign

Sigstore는 키를 직접 보관하지 않고 서명하는 체계입니다.
Fulcio가 OIDC 신원을 확인해 단기 인증서를 발급하고, 서명 기록은 Rekor 투명성 로그에 남습니다.
서명자가 개인 키를 장기 보관할 필요가 없고, 누가 언제 무엇에 서명했는지 공개 로그로 확인할 수 있습니다.
컨테이너 이미지에는 cosign으로 서명과 검증을 붙입니다.

```bash
# 키리스 서명. 실행 환경의 OIDC 신원으로 서명합니다
cosign sign ghcr.io/myorg/myapp@sha256:<다이제스트>

# 검증. 어느 저장소의 어느 워크플로가 서명했는지까지 확인합니다
cosign verify ghcr.io/myorg/myapp@sha256:<다이제스트> \
  --certificate-identity-regexp '^https://github.com/myorg/myapp/' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

AI 모델 아티팩트에도 같은 체계를 적용하는 OpenSSF Model Signing v1.0(2025-04)이 나와 있습니다.

---

## 서명과 증명이 막지 못하는 것

증명과 서명을 만능으로 소개하는 자료가 많습니다. 실제로는 그렇지 않습니다.

:::warning 유효한 SLSA 증명을 달고 배포된 악성 패키지가 있습니다
2026-05 npm을 노린 Mini Shai-Hulud 공격에서 악성 패키지 84개가 유효한 SLSA Build Level 3 출처 증명을
붙인 채 배포됐습니다. 증명은 위조되지 않았습니다. 침해된 파이프라인이 정상적으로 증명을 발급한 것입니다.
:::

SLSA 증명이 보증하는 것은 "이 아티팩트가 선언된 파이프라인에서 나왔다"입니다.
"그 파이프라인이 침해되지 않았다"는 보증하지 않습니다. 공격자가 워크플로를 장악하면
그 워크플로가 만드는 증명도 정상 절차로 발급됩니다. 검증하는 쪽에서는 구분되지 않습니다.

그래서 순서가 있습니다.

| 순서 | 무엇을                             | 왜 먼저인가                                              |
| ---- | ---------------------------------- | -------------------------------------------------------- |
| 1    | 커밋 SHA 고정과 자동 갱신          | 태그 재지정 공격을 직접 차단합니다. 비용이 가장 낮습니다 |
| 2    | 워크플로 권한 최소화               | 침해가 일어나도 얻어 갈 수 있는 것을 줄입니다            |
| 3    | zizmor 등으로 워크플로 자체를 검사 | 1과 2가 지켜지는지 자동으로 확인합니다                   |
| 4    | 빌드 출처 증명과 아티팩트 서명     | 1에서 3이 갖춰진 파이프라인에서만 의미가 생깁니다        |

4번을 먼저 도입해도 손해는 아니지만, 1번에서 3번이 비어 있으면 4번은 침해된 파이프라인의 결과물에
정품 표시를 붙여 주는 역할을 합니다.

에이전트가 호출하는 도구와 IDE 확장도 같은 구조의 공급망입니다. 도구 자체를 어떻게 통제할지는
[에이전트와 MCP 도구 거버넌스](/ai-coding/agent-governance)를 참고하세요.

---

## 셀프 점검

저장소 하나를 골라 아래 여섯 가지를 확인해 보세요.

- `.github/workflows/` 안에 `@v` 로 시작하는 태그 참조가 몇 개인가
- 워크플로 최상단에 `permissions:` 블록이 있는가. 없다면 저장소 기본값은 무엇인가
- `pull_request_target` 을 쓰는 워크플로가 있는가. 있다면 PR 브랜치 코드를 실행하는가
- `actions/checkout` 에 `persist-credentials: false` 가 붙어 있는가
- `.github/dependabot.yml` 에 `github-actions` 생태계가 등록돼 있는가
- 릴리스 아티팩트에 출처 증명이나 서명이 붙어 있는가

zizmor를 한 번 돌려 보면 앞의 네 가지는 자동으로 확인됩니다.

## 참고 자료

- [SLSA 사양](https://slsa.dev/spec/)
- [zizmor 문서](https://docs.zizmor.sh/)
- [Sigstore cosign](https://docs.sigstore.dev/cosign/signing/overview/)
- [npm trusted publishing 문서](https://docs.npmjs.com/trusted-publishers)
- [GitHub Actions 보안 강화 가이드](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)

## 다음 단계

- 전체 파이프라인 구성: [파이프라인 설계](./pipeline-design)
- 배포 후 지속 탐지: [모니터링과 자동 교정](./monitoring)
- ISO/IEC 18974 요구사항과 구현 매핑: [ISO 표준 연계](./iso-mapping)
