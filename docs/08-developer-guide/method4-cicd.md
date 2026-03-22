---
sidebar_position: 5
sidebar_label: "방법 4: CI/CD 파이프라인"
---

# 방법 4: CI/CD 파이프라인 추가하기

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
