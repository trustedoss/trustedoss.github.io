---
id: 08-developer-guide
title: "개발자 가이드: Claude Code에서 오픈소스 정책 자동 준수"
sidebar_label: 08. 개발자 가이드 (선택)
sidebar_position: 8
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - "ISO/IEC 5230: (선택 챕터 - 필수 항목 없음, G1.6 운영 강화 지원)"
  - "ISO/IEC 18974: (선택 챕터 - 필수 항목 없음, G3S.1 운영 강화 지원)"
셀프스터디 소요시간: 2시간
워크숍 소요시간: 해당 없음 (선택 챕터)
---

# 개발자 가이드: Claude Code에서 오픈소스 정책 자동 준수

## 1. 이 챕터에서 하는 일

01~07챕터로 오픈소스 관리 체계 구축이 완료되었다.
이제 남은 과제는 **일상적인 개발 과정에서 정책이 자동으로 지켜지게 하는 것**이다.

담당자가 매번 모든 PR을 검토하는 방식은 지속 가능하지 않다.
이 챕터는 Claude Code를 활용하여 **개발자가 무의식적으로 정책을 준수**하게 만드는 4가지 방법을 설명한다.

> 목표: "담당자가 매번 검토하지 않아도 Claude Code가 정책을 지켜준다"

## 2. 배경: 왜 자동화가 필요한가

### 실제 발생하는 문제 상황

**시나리오 1: GPL 패키지 무심코 추가**
개발자가 편리한 유틸리티 라이브러리를 발견한다.
`npm install some-gpl-utility`를 실행하고, PR을 올린다.
담당자가 검토하기 전까지 GPL 오염 위험이 잠재된다.
배포 후에 발견되면 소스코드 공개 의무가 발생할 수 있다.

**시나리오 2: 취약한 버전 그대로 사용**
의존성 업데이트 없이 오래된 버전을 계속 사용한다.
CVSS 9.0의 Critical 취약점이 공개되었지만 팀이 인지하지 못한다.
보안 사고 발생 시 "몰랐다"는 변명은 통하지 않는다.

**시나리오 3: 담당자 모르게 정책 위반**
허용 라이선스 목록(`license-allowlist.md`)에 없는 라이선스를 가진 패키지가 추가된다.
사용 승인 절차(`usage-approval.md`)를 거치지 않고 배포된다.
인증 갱신 시점에서야 위반이 발견된다.

### 해결 원칙

정책 준수를 개발자의 **기억과 의지**에 맡기지 않는다.
도구와 자동화가 **기본값**이 되게 한다.

## 3. 해결 방법 개요

아래 4가지 방법을 조합하여 적용한다. 보장 수준이 높을수록 구현 복잡도도 높아진다.

| 방법 | 설명 | 보장 수준 | 구현 난이도 |
|------|------|----------|-----------|
| **CLAUDE.md 정책 명시** | Claude Code에게 지켜야 할 정책을 직접 알린다 | 70% | 매우 쉬움 |
| **Skill 정의** | 라이선스·취약점 확인 절차를 재사용 가능한 skill로 만든다 | 80% | 쉬움 |
| **Hooks 자동 검증** | 의존성 파일 변경 시 자동으로 경고를 발생시킨다 | 90% | 보통 |
| **CI/CD 파이프라인** | PR 시 자동 체크, 위반 시 머지 차단 | 99% | 다소 복잡 |

> **핵심 원칙:** 완벽한 보장을 위해서는 4가지를 모두 적용해야 한다.
> 각 방법은 독립적으로 작동하지만, 조합할수록 누락 위험이 줄어든다.

## 4. 방법 1: CLAUDE.md에 정책 추가하기

:::info 셀프스터디 모드 (약 15분)
프로젝트 루트 CLAUDE.md에 정책을 추가하면 Claude Code가 즉시 인식한다.
:::

프로젝트 루트의 `CLAUDE.md`에 아래 섹션을 추가한다.

```markdown
## 오픈소스 정책 (자동 준수)

### 허용 라이선스
아래 라이선스만 신규 패키지에 사용 가능하다:
- MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
- 전체 목록: output/policy/license-allowlist.md 참조

### 금지 라이선스
아래 라이선스는 사전 승인 없이 추가 금지:
- GPL-2.0, GPL-3.0, AGPL-3.0 (Copyleft - 소스코드 공개 의무)
- LGPL-2.0, LGPL-2.1, LGPL-3.0 (Weak Copyleft - 동적 링킹 검토 필요)
- CC-BY-SA (소프트웨어에 부적합)
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

**효과:** Claude Code가 패키지 추가를 도울 때 이 정책을 자동으로 참조하여 경고한다.

**한계:** 개발자가 직접 터미널에서 `npm install`을 실행하면 Claude Code가 개입하지 못한다.

## 5. 방법 2: Skill 정의하기

:::info 셀프스터디 모드 (약 20분)
한 번 정의하면 모든 프로젝트에서 `/oss-policy-check`으로 즉시 호출할 수 있다.
:::

`.claude/skills/oss-policy-check.md` 파일을 생성한다.

```markdown
# Skill: OSS 정책 준수 검사 (oss-policy-check)

## 트리거
개발자가 `/oss-policy-check` 또는 "오픈소스 정책 확인" 요청 시 실행

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

---
## OSS 정책 검사 결과

**검사 일시:** YYYY-MM-DD
**대상 프로젝트:** [프로젝트명]

### 라이선스 현황
| 라이선스 | 패키지 수 | 상태 |
|---------|---------|------|
| MIT | 45 | ✅ 허용 |
| Apache-2.0 | 12 | ✅ 허용 |
| GPL-3.0 | 1 | ❌ 위반 |

### 취약점 현황
| CVE | CVSS | 패키지 | 상태 |
|-----|------|--------|------|
| CVE-2024-XXXX | 9.1 | lodash@4.17.15 | ❌ 긴급 패치 필요 |

### 권고사항
- [ ] GPL-3.0 패키지 대체 또는 사용 승인 요청
- [ ] lodash 4.17.21 이상으로 업그레이드
---
```

**효과:** 팀원 누구나 `/oss-policy-check` 명령으로 즉시 현황을 파악할 수 있다.

## 6. 방법 3: Hooks 설정하기

:::info 셀프스터디 모드 (약 30분)
의존성 파일이 변경될 때마다 자동으로 경고가 발생한다.
:::

`.claude/settings.json`에 아래 Hook을 추가한다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "node -e \"\nconst fs = require('fs');\nconst result = process.env.CLAUDE_TOOL_RESULT || '';\nconst changedFiles = ['package.json', 'requirements.txt', 'pom.xml', 'go.mod', 'Cargo.toml'];\nconst hasDepChange = changedFiles.some(f => result.includes(f));\nif (hasDepChange) {\n  console.error('[OSS Policy Warning] 의존성 파일이 변경되었습니다.');\n  console.error('신규 패키지의 라이선스와 취약점을 반드시 확인하세요.');\n  console.error('확인 방법: /oss-policy-check 실행');\n}\n\""
          }
        ]
      }
    ]
  }
}
```

> 이 단계는 `output/process/usage-approval.md`에 정의된 패키지 추가 승인 절차를 자동으로 환기시킵니다.

**효과:** Claude Code가 `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, `Cargo.toml` 등을 수정할 때마다 자동으로 경고 메시지가 표시된다.

**한계:** Claude Code 외부에서 파일을 수정하면 Hook이 실행되지 않는다. CI/CD로 보완한다.

## 7. 방법 4: CI/CD 파이프라인 추가하기

:::info 셀프스터디 모드 (약 45분)
PR 단계에서 자동으로 차단하면 위반이 메인 브랜치에 들어오지 못한다.
:::

`.github/workflows/oss-policy-check.yml`을 생성한다.
아래 예시는 **무료 오픈소스 도구만** 사용한다 (syft, grype 모두 오픈소스).

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
      - uses: actions/checkout@v4

      - name: syft로 SBOM 생성
        uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cdx.json

      - name: 라이선스 추출 및 정책 검사
        run: |
          # syft로 라이선스 목록 추출
          syft . -o json | jq -r '.artifacts[].licenses[].value' | sort -u > detected-licenses.txt

          echo "=== 감지된 라이선스 ==="
          cat detected-licenses.txt

          # 금지 라이선스 확인
          FORBIDDEN="GPL-2.0\|GPL-3.0\|AGPL-3.0\|LGPL-2.0"
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
      - uses: actions/checkout@v4

      - name: grype로 취약점 스캔
        uses: anchore/scan-action@v3
        with:
          path: '.'
          fail-build: true
          severity-cutoff: high   # High / Critical 취약점 발견 시 머지 차단
          output-format: table

      - name: 취약점 보고서 업로드
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: vulnerability-report
          path: results.sarif
```

> 이 단계는 ISO/IEC 18974 G3S.1 (알려진 취약점 식별) 요구사항의 **자동화된 지속 검증**을 지원합니다.

**효과:**
- 모든 PR에서 자동으로 라이선스 검사 실행
- GPL 등 금지 라이선스 발견 시 PR 머지 차단
- CVSS High(7.0) 이상 취약점 발견 시 머지 차단
- 검사 결과가 PR 화면에 직접 표시됨

**무료 도구 정보:**
- [syft](https://github.com/anchore/syft): SBOM 생성 도구 (Apache-2.0)
- [grype](https://github.com/anchore/grype): 취약점 스캐너 (Apache-2.0)

## 8. 상세 구현 안내

:::info 상세 구현은 별도 프로젝트를 참조
각 방법의 실제 구현 예시, 트러블슈팅, 다양한 언어·빌드 시스템별 설정을
**claude-oss-policy-guard** 프로젝트에서 제공할 예정입니다.
(준비 중)
:::

이 챕터는 개념과 기본 예시를 제공한다.
실제 프로덕션 환경 적용, 예외 처리, 복잡한 모노레포 구성 등은
`claude-oss-policy-guard` 프로젝트의 상세 가이드를 참조한다.

## 9. 완료 확인

:::info 셀프스터디 모드 (약 2시간)
충분한 시간을 갖고 각 단계를 이해하며 진행합니다.
:::

아래 항목을 모두 완료하면 이 챕터가 완성된다.

- [ ] 프로젝트 `CLAUDE.md`에 오픈소스 정책 섹션 추가 완료
- [ ] `.claude/skills/oss-policy-check.md` 생성 완료
- [ ] `/oss-policy-check` 실행하여 동작 확인
- [ ] `.claude/settings.json` Hook 설정 완료
- [ ] 의존성 파일 수정 시 경고 메시지 출력 확인
- [ ] `.github/workflows/oss-policy-check.yml` 생성 완료
- [ ] 테스트 PR을 올려 라이선스·취약점 검사 자동 실행 확인

## 10. 다음 단계

이 챕터까지 완료했다면, 오픈소스 관리 체계가 **구축을 넘어 운영**까지 완성된 것이다.

**유지 관리 권고:**
- 18개월마다 OpenChain 자체 인증 갱신 (`docs/07-conformance/` 참조)
- 분기마다 `license-allowlist.md` 검토 및 갱신
- 신규 CVE 발생 시 grype 재스캔

**더 나아가기:**
- claude-oss-policy-guard 프로젝트 (준비 중)
- [OpenChain 커뮤니티](https://www.openchainproject.org/) 참여
- 공급망 파트너와 SBOM 공유 (`output/sbom/sbom-sharing-template.md` 활용)
