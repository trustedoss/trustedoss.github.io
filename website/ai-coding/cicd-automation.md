---
id: cicd-automation
title: CI/CD 자동화
sidebar_label: CI/CD 자동화
sidebar_position: 7
---

# CI/CD 자동화

AI 코딩 도구와 CI/CD 파이프라인을 연동하여 오픈소스 컴플라이언스를 자동화합니다.

## GitHub Actions 예시

### SBOM 자동 생성

```yaml
# .github/workflows/sbom.yml
name: SBOM 생성

on:
  push:
    branches: [main]
  pull_request:
    paths:
      - 'package.json'
      - 'package-lock.json'
      - 'requirements.txt'
      - 'pom.xml'

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: SBOM 생성 (CycloneDX)
        uses: CycloneDX/gh-action-node@v1
        with:
          output: sbom.json

      - name: SBOM 아티팩트 저장
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.json
```

### 라이선스 컴플라이언스 검사

```yaml
# .github/workflows/license-check.yml
name: 라이선스 검사

on: [push, pull_request]

jobs:
  license:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 라이선스 검사 (license-checker)
        run: |
          npm install -g license-checker
          license-checker --onlyAllow 'MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC' --excludePrivatePackages
```

### 취약점 스캔

```yaml
# .github/workflows/vulnerability-scan.yml
name: 취약점 스캔

on:
  schedule:
    - cron: '0 9 * * 1'  # 매주 월요일 오전 9시
  push:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Trivy 취약점 스캔
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
```

## AI 코딩 도구와 연동

### PR 생성 시 자동 컴플라이언스 체크

AI 코딩 도구로 코드를 작성하고 PR을 생성하면 자동으로:

1. 새로 추가된 의존성의 라이선스 검사
2. 알려진 취약점 스캔
3. SBOM 업데이트 여부 확인

결과는 PR 코멘트로 자동 보고됩니다.

## 관련 링크

- [trustedoss: SBOM 생성](../docs/05-tools/sbom-generation/index)
- [trustedoss: 취약점 분석](../docs/05-tools/vulnerability/index)
