---
sidebar_position: 5
sidebar_label: '방법 4: CI/CD 파이프라인'
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
셀프스터디 소요시간: 45분
---

# 방법 4: CI/CD 파이프라인 추가하기

:::info 셀프스터디 모드 (약 45분)
PR 단계에서 자동으로 차단하면 위반이 메인 브랜치에 들어오지 못합니다.
:::

`.github/workflows/oss-policy-check.yml`을 생성합니다.
아래 예시는 **무료 오픈소스 도구만** 사용합니다 (syft, grype 모두 오픈소스).

차단 목록에는 [라이선스 분류](/reference/concepts/license-classification)에서 금지 등급인
라이선스만 넣습니다. LGPL·MPL 같은 조건부 허용 라이선스는 빌드를 실패시키는 대신 담당자
검토로 넘기는 것이 정본 기준입니다.

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

> 이 단계는 ISO/IEC 18974 G3S.1 (알려진 취약점 식별) 요구사항의 **자동화된 지속 검증**을 지원합니다.

**효과:**

- 모든 PR에서 자동으로 라이선스 검사 실행
- GPL·AGPL 등 금지 라이선스 발견 시 PR 머지 차단
- CVSS High(7.0) 이상 취약점 발견 시 머지 차단
- 검사 결과가 PR 화면에 직접 표시됨

**무료 도구 정보:**

- [syft](https://github.com/anchore/syft): SBOM 생성 도구 (Apache-2.0)
- [grype](https://github.com/anchore/grype): 취약점 스캐너 (Apache-2.0)

---

→ 다음: [완료 확인](./index.md#6-완료-확인)
