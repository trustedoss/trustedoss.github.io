---
id: cicd-quick
title: CI/CD 자동화
sidebar_label: CI/CD 자동화
sidebar_position: 5
---

# CI/CD 자동화

## AI 규칙만으로는 부족한 이유

:::warning Hard Block은 CI/CD에서만 가능합니다
:::

`CLAUDE.md`나 `.cursorrules` 같은 AI 규칙 파일은 어디까지나 "권장사항"입니다. 개발자가 의도적으로 무시하거나 AI가 실수로 규칙을 따르지 않아도 아무것도 막아주지 않습니다.

규칙 파일만 운영하는 환경에서는 PR이 병합되는 순간 정책 위반 코드가 프로덕션으로 그대로 흘러들어갈 수 있습니다. AI 도구가 빠르게 코드를 생성할수록 이 위험은 커집니다.

CI/CD 게이트는 사람과 AI의 실수에 관계없이 기계적으로 정책 위반을 차단하는 유일한 안전망입니다. 3단계 전략([4단계 전략](./strategy) 참고)부터 진정한 Hard Block이 작동합니다.

---

## 최소 3종 조합

| 역할 | 도구 | 하는 일 |
|------|------|---------|
| SBOM 생성 | syft | 의존성 전체를 CycloneDX/SPDX 형식으로 추출 |
| 취약점 차단 | grype | SBOM 기반으로 CVE 스캔, 임계값 초과 시 빌드 실패 |
| 라이선스 차단 | syft + 스크립트 | SBOM에서 금지 라이선스 검출 시 빌드 실패 |

세 도구 모두 무료 오픈소스이며, 설치 없이 GitHub Actions / GitLab CI에서 바로 사용 가능합니다.

---

## GitHub Actions

### 전체 워크플로우

```yaml
# .github/workflows/oss-policy.yml
name: OSS Policy Check

on:
  pull_request:
    branches: [main, develop]

jobs:
  oss-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      # 1. SBOM 생성
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cdx.json

      # 2. 취약점 스캔 — High 이상 발견 시 빌드 실패
      - name: Scan vulnerabilities
        uses: anchore/scan-action@v3
        with:
          sbom: sbom.cdx.json
          fail-build: true
          severity-cutoff: high

      # 3. 금지 라이선스 검사
      - name: Check licenses
        run: |
          FORBIDDEN="GPL AGPL SSPL"
          FOUND=""
          for license in $FORBIDDEN; do
            if grep -qi "\"$license" sbom.cdx.json; then
              FOUND="$FOUND $license"
            fi
          done
          if [ -n "$FOUND" ]; then
            echo "금지 라이선스 발견:$FOUND"
            exit 1
          fi
          echo "라이선스 검사 통과"

      # 4. SBOM 아티팩트 보관
      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.cdx.json
```

---

### 단계별 설명

**1. SBOM 생성 (anchore/sbom-action)**

소스코드와 매니페스트 파일(package.json, requirements.txt 등)을 분석해 CycloneDX JSON 형식의 SBOM 파일을 생성합니다. GitHub Actions 마켓플레이스에서 바로 사용할 수 있으며, 별도 설치가 필요하지 않습니다.

**2. 취약점 스캔 (anchore/scan-action)**

생성된 SBOM을 기반으로 CVE 데이터베이스와 대조해 취약점을 검사합니다. `severity-cutoff: high` 설정으로 High·Critical CVE가 발견되면 빌드가 자동으로 실패합니다. Medium 이하는 경고만 출력되고 빌드는 계속 진행됩니다. 처음 도입하는 경우 `critical`로 완화해 운영하다가 점진적으로 `high`로 강화하는 방식을 권장합니다.

**3. 금지 라이선스 검사 (셸 스크립트)**

SBOM JSON에서 GPL·AGPL·SSPL 문자열을 검색합니다. 금지 라이선스가 발견되면 `exit 1`로 빌드를 실패시킵니다. `FORBIDDEN` 변수를 수정해 [공통 Rules 템플릿](./rules-template)의 금지 목록과 동기화하거나 팀 정책에 맞게 커스터마이징할 수 있습니다.

**4. SBOM 아티팩트 보관**

생성된 SBOM을 Actions 아티팩트로 저장합니다. 감사(Audit) 대응 자료로 활용하거나 ISO/IEC 18974 증적으로 보관할 수 있습니다.

---

## GitLab CI

:::info GitHub Actions와 도구는 동일합니다
runner 문법만 다를 뿐, syft·grype를 그대로 사용합니다.
:::

### 전체 파이프라인

```yaml
# .gitlab-ci.yml (oss-check 잡 부분)
oss-check:
  stage: test
  image: ubuntu:22.04
  script:
    # 도구 설치
    - curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
    - curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

    # 1. SBOM 생성
    - syft . -o cyclonedx-json=sbom.cdx.json

    # 2. 취약점 스캔 — High 이상 빌드 실패
    - grype sbom:sbom.cdx.json --fail-on high

    # 3. 금지 라이선스 검사
    - |
      FORBIDDEN="GPL AGPL SSPL"
      FOUND=""
      for license in $FORBIDDEN; do
        if grep -qi "\"$license" sbom.cdx.json; then
          FOUND="$FOUND $license"
        fi
      done
      if [ -n "$FOUND" ]; then
        echo "금지 라이선스 발견:$FOUND"
        exit 1
      fi

  artifacts:
    paths:
      - sbom.cdx.json
    expire_in: 30 days

  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---

### GitHub Actions와의 차이점

| 항목 | GitHub Actions | GitLab CI |
|------|---------------|-----------|
| SBOM 생성 | anchore/sbom-action (Action) | syft 직접 설치·실행 |
| 취약점 스캔 | anchore/scan-action (Action) | grype 직접 설치·실행 |
| 트리거 조건 | pull_request | merge_request_event |
| 아티팩트 보관 | upload-artifact | artifacts.paths |

---

## 정책 커스터마이징

:::tip 최소한 이 두 가지는 팀 정책에 맞게 수정하세요
:::

**취약점 임계값**

`severity-cutoff`(GitHub Actions) 또는 `--fail-on`(GitLab CI) 값을 기본값인 `high`에서 `critical`로 완화하거나 `medium`으로 강화할 수 있습니다. 처음 파이프라인을 도입할 때는 `critical`부터 시작해 빌드 실패 빈도를 파악한 뒤 점진적으로 강화하는 방식을 권장합니다.

**금지 라이선스 목록**

`FORBIDDEN` 변수를 [공통 Rules 템플릿](./rules-template)의 금지 라이선스 목록과 동기화해 두세요. LGPL·MPL 등 주의 라이선스는 빌드를 실패시키는 대신 경고 메시지만 출력하는 별도 로직을 추가해 법무 검토 흐름과 연결하는 방식도 가능합니다.

---

## 다음 단계

멀티 저장소·정책 거버넌스·ORT 연동 등 전사 수준의 파이프라인 설계가 필요하다면 DevSecOps 가이드를 참고하세요.

- [DevSecOps — 전사 파이프라인 설계](/devsecops/pipeline-design)
- [DevSecOps — 지속적 모니터링·자동 교정](/devsecops/monitoring)
