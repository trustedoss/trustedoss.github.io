---
title: '개발자 가이드: Claude Code에서 오픈소스 정책 자동 준수'
sidebar_position: 8
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - 'ISO/IEC 5230: (선택 챕터 - 필수 항목 없음, G1.6 운영 강화 지원)'
  - 'ISO/IEC 18974: (선택 챕터 - 필수 항목 없음, G3S.1 운영 강화 지원)'
셀프스터디 소요시간: 2시간
---

<!-- STYLEGUIDE.md §1 의 200~350줄 권장을 넘는다. 방법 1~4 를 개별 페이지로 두면
     독자가 네 번 이동해야 하고 절끼리 중복이 생겨 한 페이지로 합쳤다. SKILL.md 전문과
     워크플로 전문은 <details> 로 접어 본문 흐름에서 뺐다.
     방법 1 의 라이선스 목록은 독자가 붙여넣는 산출물이라 전문을 유지한다. 등급이 바뀌면
     세 곳을 함께 고쳐야 한다. 정본(reference/concepts/license-classification),
     ai-coding/rules-template, 그리고 이 문서다. -->

# 개발자 가이드: Claude Code에서 오픈소스 정책 자동 준수

## 1. 이 챕터에서 하는 일

01~07챕터로 오픈소스 관리 체계 구축이 완료되었습니다.
이제 남은 과제는 **일상적인 개발 과정에서 정책이 자동으로 지켜지게 하는 것**입니다.

담당자가 매번 모든 PR을 검토하는 방식은 지속 가능하지 않습니다.
이 챕터는 Claude Code를 활용하여 **개발자가 무의식적으로 정책을 준수**하게 만드는 4가지 방법을 설명합니다.

:::info 목표
담당자가 매번 검토하지 않아도 Claude Code가 정책을 지켜준다 — 이 상태를 만드는 것이 이 챕터의 목표입니다.
:::

:::note 이 챕터 vs AI코딩 Rules 템플릿
이 챕터는 **앞서 구축한 우리 조직 정책**(`output/policy/`)을 개발 일상에 자동 적용하는 4가지 방법입니다.
정책을 아직 안 세웠고 AI 코딩 도구용 Rules 파일만 빠르게 만들려면 [공통 Rules 템플릿](/ai-coding/rules-template)을 쓰세요.
:::

## 2. 배경: 왜 자동화가 필요한가

:::tip
SBOM·라이선스 관련 용어가 낯설면 [용어집](/reference/glossary)을 참고하세요.
:::

### 실제 발생하는 문제 상황

**시나리오 1: GPL 패키지 무심코 추가**
개발자가 편리한 유틸리티 라이브러리를 발견합니다.
`npm install some-gpl-utility`를 실행하고 PR을 올립니다.
담당자가 검토하기 전까지 GPL 오염 위험이 잠재됩니다.
배포 후에 발견되면 소스코드 공개 의무가 발생할 수 있습니다.

**시나리오 2: 취약한 버전 그대로 사용**
의존성 업데이트 없이 오래된 버전을 계속 사용합니다.
CVSS 9.0의 Critical 취약점이 공개되었지만 팀이 인지하지 못합니다.
보안 사고가 나면 "몰랐다"는 변명은 통하지 않습니다.

**시나리오 3: 담당자 모르게 정책 위반**
허용 라이선스 목록(`license-allowlist.md`)에 없는 라이선스를 가진 패키지가 추가됩니다.
사용 승인 절차(`usage-approval.md`)를 거치지 않고 배포됩니다.
인증 갱신 시점에서야 위반이 발견됩니다.

### 해결 원칙

정책 준수를 개발자의 **기억과 의지**에 맡기지 않습니다.
도구와 자동화가 **기본값**이 되게 합니다.

## 3. 해결 방법 개요

아래 4가지 방법을 조합하여 적용합니다. 보장 수준이 높을수록 구현 복잡도도 높아집니다.

| 방법                    | 설명                                                     | 보장 수준 | 구현 난이도 |
| ----------------------- | -------------------------------------------------------- | --------- | ----------- |
| **CLAUDE.md 정책 명시** | Claude Code에게 지켜야 할 정책을 직접 알린다             | 70%       | 매우 쉬움   |
| **Skill 정의**          | 라이선스·취약점 확인 절차를 재사용 가능한 skill로 만든다 | 80%       | 쉬움        |
| **Hooks 자동 검증**     | 의존성 파일 변경 시 자동으로 경고를 발생시킨다           | 90%       | 보통        |
| **CI/CD 파이프라인**    | PR 시 자동 체크, 위반 시 머지 차단                       | 99%       | 다소 복잡   |

:::info[핵심 원칙]
완벽한 보장을 위해서는 4가지를 모두 적용해야 합니다. 각 방법은 독립적으로 작동하지만, 조합할수록 누락 위험이 줄어듭니다.
:::

## 4. 각 방법 상세 가이드

가장 쉬운 방법 1부터 시작해 3·4로 보강하는 순서를 권장합니다.

### 방법 1 — CLAUDE.md에 정책 명시 (보장 70%, 쉬움) {#method-1}

프로젝트 루트의 `CLAUDE.md`에 아래 섹션을 추가하면, Claude Code가 패키지 추가를 도울 때 이 정책을 자동으로 참조합니다. 등급 구분은 [라이선스 분류](/reference/concepts/license-classification) 기준을 따릅니다. 실제 회사 정책의 허용 목록은 03 정책 챕터에서 생성한 `output/policy/license-allowlist.md`이므로, 아래 예시를 붙여넣은 뒤 그 파일 내용에 맞게 조정하세요.

```markdown
## 오픈소스 정책 (자동 준수)

### 허용 라이선스

아래 라이선스는 별도 승인 없이 신규 패키지에 사용 가능하다:

- MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
- 전체 목록: output/policy/license-allowlist.md 참조

### 조건부 허용 라이선스

아래 라이선스는 담당자 사전 검토와 승인 후 사용 가능하다:

- LGPL, MPL (Weak Copyleft - 사용 방식에 따라 소스 공개 의무 발생, 법무 검토 필요)
- CC-BY-SA (콘텐츠용 라이선스라 소프트웨어 적용 시 별도 검토 필요)
- 조건과 예외는 output/policy/license-allowlist.md 참조

### 금지 라이선스

아래 라이선스는 사전 승인 없이 추가 금지:

- GPL, AGPL (Copyleft - 배포 시 소스코드 공개 의무)
- SSPL, Commons Clause (오픈소스 정의를 충족하지 않는 사용 제한 조항)
- 상업적 사용 금지 조항이 있는 모든 라이선스

### 취약점 정책

- CVSS 7.0 이상(High/Critical) 취약점이 있는 패키지 사용 금지
- 알려진 취약점이 있는 버전은 패치 버전으로 업그레이드

### 패키지 추가 시 확인 절차

새 패키지를 추가할 때는 반드시 아래 순서로 확인한다:

1. 라이선스 확인: `license-checker` 또는 `/oss-policy-check` skill 실행
2. 취약점 확인: OSV API 또는 `grype` 실행
3. 허용 목록 비교: output/policy/license-allowlist.md 대조
4. 위반 시: 담당자에게 사용 승인 요청 (output/process/usage-approval.md 참조)
```

:::note 등급 기준의 정본
허용·조건부·금지 세 등급의 판단 기준은 [라이선스 분류](/reference/concepts/license-classification)가
정본입니다. 위 예시는 그 기준을 CLAUDE.md 형식으로 옮긴 것이므로, 등급이 바뀌면 정본을 먼저
확인하세요. AI 코딩 도구별 설정 파일에 넣을 규칙 전문은
[공통 Rules 템플릿](/ai-coding/rules-template)에 있습니다.
:::

- 효과: Claude Code가 정책을 인지하고 위반 시 경고합니다.
- 한계: 개발자가 터미널에서 직접 `npm install`을 실행하면 개입하지 못합니다.

### 방법 2 — Skill로 검사 절차 표준화 (보장 80%, 쉬움) {#method-2}

라이선스·취약점 확인 절차를 `/oss-policy-check` skill로 만들어, 누구나 한 명령으로 같은 검사를 실행합니다. Skill은 디렉토리 단위로 정의하며, 파일 상단의 frontmatter(name, description)가 있어야 인식됩니다.

```bash
mkdir -p .claude/skills/oss-policy-check
```

이 프로젝트 어디서나 `/oss-policy-check`으로 호출할 수 있습니다. 모든 프로젝트에서 쓰려면 같은 내용을 `~/.claude/skills/`에 두면 됩니다.

<details>
<summary><code>.claude/skills/oss-policy-check/SKILL.md</code> 전문</summary>

````markdown
---
name: oss-policy-check
description: 오픈소스 정책 준수 검사. 개발자가 /oss-policy-check 또는 "오픈소스 정책 확인"을 요청할 때 실행한다.
---

# OSS 정책 준수 검사

## 실행 절차

### 1단계: 라이선스 확인

Node.js 프로젝트:

```bash
npx license-checker --summary --excludePrivatePackages
```

Python 프로젝트:

```bash
pip-licenses --format=markdown --with-urls
```

Java/Maven 프로젝트:

```bash
mvn license:aggregate-third-party-report
```

### 2단계: 허용 목록 대조

output/policy/license-allowlist.md 의 허용 라이선스와 비교한다.
목록에 없는 라이선스가 발견되면 즉시 경고한다.

### 3단계: 취약점 조회 (OSV API)

발견된 패키지에 대해 OSV API로 취약점을 조회한다:

```bash
# grype 사용 (권장)
grype dir:. --fail-on high

# 또는 OSV-Scanner 사용
osv-scanner --recursive .
```

### 4단계: 결과 보고 형식

검사 결과를 아래 형식으로 보고한다:

## OSS 정책 검사 결과

**검사 일시:** YYYY-MM-DD
**대상 프로젝트:** [프로젝트명]

### 라이선스 현황

| 라이선스   | 패키지 수 | 상태    |
| ---------- | --------- | ------- |
| MIT        | 45        | ✅ 허용 |
| Apache-2.0 | 12        | ✅ 허용 |
| GPL-3.0    | 1         | ❌ 위반 |

### 취약점 현황

| CVE           | CVSS | 패키지         | 상태              |
| ------------- | ---- | -------------- | ----------------- |
| CVE-2024-XXXX | 9.1  | lodash@4.17.15 | ❌ 긴급 패치 필요 |

### 권고사항

- [ ] GPL-3.0 패키지 대체 또는 사용 승인 요청
- [ ] lodash 4.17.21 이상으로 업그레이드
````

</details>

- 효과: 검사 절차가 재사용 가능한 한 명령으로 표준화됩니다.
- 한계: 개발자가 실행을 잊으면 검사되지 않습니다.

### 방법 3 — Hooks로 자동 환기 (보장 90%, 보통) {#method-3}

`.claude/settings.json`에 아래 Hook을 걸어 두면, 의존성 파일이 변경될 때마다 자동으로 경고가 표시됩니다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "node -e \"\nlet raw = '';\nprocess.stdin.on('data', (c) => (raw += c));\nprocess.stdin.on('end', () => {\n  const hook = JSON.parse(raw);\n  const file = (hook.tool_input && hook.tool_input.file_path) || '';\n  const depFiles = ['package.json', 'requirements.txt', 'pom.xml', 'go.mod', 'Cargo.toml'];\n  if (depFiles.some((f) => file.endsWith(f))) {\n    console.error('[OSS Policy Warning] 의존성 파일이 변경되었습니다.');\n    console.error('신규 패키지의 라이선스와 취약점을 반드시 확인하세요.');\n    console.error('확인 방법: /oss-policy-check 실행');\n    process.exit(2);\n  }\n});\n\""
          }
        ]
      }
    ]
  }
}
```

Hook 커맨드는 표준 입력(stdin)으로 도구 호출 정보가 담긴 JSON(`tool_name`, `tool_input`, `tool_response`)을 받습니다. 위 예시는 `tool_input.file_path`로 의존성 파일 여부를 판단하고, 해당하면 exit code 2로 종료해 경고 메시지가 Claude에게 전달되도록 합니다. 이 Hook은 `output/process/usage-approval.md`에 정의된 패키지 추가 승인 절차를 자동으로 환기시킵니다.

- 효과: `package.json`·`requirements.txt`·`pom.xml`·`go.mod`·`Cargo.toml` 등 변경 시 자동으로 환기됩니다.
- 더 강한 통제: 수정 자체를 차단하려면 같은 스크립트를 `PreToolUse` Hook으로 등록하세요. PreToolUse에서 exit code 2는 도구 호출을 실행 전에 차단합니다.
- 한계: Claude Code 외부에서 파일을 수정하면 감지하지 못하므로 CI/CD로 보완합니다.

### 방법 4 — CI/CD로 머지 차단 (보장 99%, 다소 복잡) {#method-4}

PR에서 syft·grype로 자동 검사하고, 정책 위반 시 머지를 차단합니다. 사람이나 도구의 누락과 무관하게 마지막 관문을 지킵니다. 아래 예시는 무료 오픈소스 도구만 사용합니다([syft](https://github.com/anchore/syft), [grype](https://github.com/anchore/grype) 모두 Apache-2.0).

차단 목록에는 [라이선스 분류](/reference/concepts/license-classification)에서 금지 등급인 라이선스만 넣습니다. LGPL·MPL 같은 조건부 허용 라이선스는 빌드를 실패시키는 대신 담당자 검토로 넘기는 것이 정본 기준입니다.

<details>
<summary><code>.github/workflows/oss-policy-check.yml</code> 전문</summary>

```yaml
name: OSS Policy Check

on:
  pull_request:
    branches: [main, master]
    paths:
      - 'package.json'
      - 'package-lock.json'
      - 'requirements.txt'
      - 'pom.xml'
      - 'go.mod'
      - 'Cargo.toml'

jobs:
  license-check:
    name: 라이선스 정책 검사
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: syft로 SBOM 생성
        uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cdx.json

      - name: 라이선스 추출 및 정책 검사
        run: |
          # 앞 단계에서 생성한 SBOM(sbom.cdx.json)에서 라이선스 목록 추출
          jq -r '.components[]?.licenses[]? | (.license.id // .license.name // .expression) // empty' sbom.cdx.json | sort -u > detected-licenses.txt

          echo "=== 감지된 라이선스 ==="
          cat detected-licenses.txt

          # 금지 라이선스 확인 (grep -E 확장 정규식, -only/-or-later 변형도 부분 일치로 감지)
          # \b 는 단어 경계라 LGPL 은 걸리지 않습니다. LGPL·MPL 은 금지가 아니라 조건부
          # 허용이므로 차단 대신 담당자 검토 대상입니다. GNU grep 기준입니다.
          FORBIDDEN='\b(GPL-2\.0|GPL-3\.0|AGPL-3\.0|SSPL-1\.0|Commons-Clause)'
          if grep -qE "$FORBIDDEN" detected-licenses.txt; then
            echo "::error::금지된 라이선스가 감지되었습니다. 담당자의 승인을 받거나 대체 패키지를 사용하세요."
            grep -E "$FORBIDDEN" detected-licenses.txt
            exit 1
          fi

          echo "✅ 라이선스 검사 통과"

  vulnerability-check:
    name: 취약점 검사 (High 이상 차단)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: grype로 취약점 스캔
        id: scan
        uses: anchore/scan-action@v7
        with:
          path: '.'
          fail-build: true
          severity-cutoff: high # High / Critical 취약점 발견 시 머지 차단
          output-format: sarif # 결과 파일 경로는 아래에서 outputs 로 참조

      - name: 취약점 보고서 업로드
        if: always()
        uses: actions/upload-artifact@v7
        with:
          name: vulnerability-report
          # v6부터 결과 파일이 임시 경로에 생성되어 outputs 로 참조합니다.
          path: ${{ steps.scan.outputs.sarif }}
```

</details>

:::note
이 단계는 ISO/IEC 18974 G3S.1 (알려진 취약점 식별) 요구사항의 자동화된 지속 검증을 지원합니다.
:::

- 효과: 개발 환경과 무관하게 모든 PR을 강제로 검사하고, 금지 라이선스나 High 이상 취약점 발견 시 머지를 차단합니다. 검사 결과는 PR 화면에 직접 표시됩니다.
- 한계: 초기 설정과 예외 관리에 약간의 노력이 필요합니다.

같은 검사를 전사 파이프라인에 넣는 방법과 도구별 상세 설정은 [소프트웨어 구성 분석 (SCA)](/devsecops/sca)에서 다룹니다.

### 상황별 적용 조합 권장

네 가지를 한 번에 도입할 필요는 없습니다. 상황에 맞는 조합부터 시작하세요.

| 상황                       | 권장 조합        | 이유                                       |
| -------------------------- | ---------------- | ------------------------------------------ |
| 1~2인 소규모 / 빠른 시작   | 방법 1 + 3       | 설정이 가볍고 Claude Code 안에서 즉시 환기 |
| 정식 배포 제품 / 외부 납품 | 방법 1 + 3 + 4   | CI/CD 머지 차단으로 누락 없이 강제 검사    |
| 검사 절차를 팀 표준으로    | 위 조합 + 방법 2 | 누구나 같은 명령으로 동일한 검사 수행      |

처음에는 방법 1을 5분 만에 적용해 효과를 확인하고, 배포 빈도가 높아지면 방법 4로 강제력을 더하는 단계적 도입을 권장합니다.

## 5. 완료 확인

:::info 셀프스터디 모드 (약 2시간)
충분한 시간을 갖고 각 단계를 이해하며 진행합니다.
:::

아래 항목을 모두 완료하면 이 챕터가 완성됩니다.

- [ ] 프로젝트 `CLAUDE.md`에 오픈소스 정책 섹션 추가 완료
- [ ] `.claude/skills/oss-policy-check/SKILL.md` 생성 완료
- [ ] `/oss-policy-check` 실행하여 동작 확인
- [ ] `.claude/settings.json` Hook 설정 완료
- [ ] 의존성 파일 수정 시 경고 메시지 출력 확인
- [ ] `.github/workflows/oss-policy-check.yml` 생성 완료
- [ ] 테스트 PR을 올려 라이선스·취약점 검사 자동 실행 확인

## 6. 다음 단계

이 챕터까지 완료했다면, 오픈소스 관리 체계가 **구축을 넘어 운영**까지 완성된 것입니다.

**유지 관리 권고:**

- 18개월마다 OpenChain 자체 인증 갱신 ([자체 인증 선언: 마지막 단계](../07-conformance/index.md) 참조)
- 분기마다 `license-allowlist.md` 검토 및 갱신
- 신규 CVE 발생 시 grype 재스캔

**더 나아가기:**

- [OpenChain 커뮤니티](https://www.openchainproject.org/) 참여
- 공급망 파트너와 SBOM 공유 (`output/sbom/sbom-sharing-template.md` 활용)
