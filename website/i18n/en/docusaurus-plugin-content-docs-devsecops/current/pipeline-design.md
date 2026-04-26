---
id: pipeline-design
title: 전사 파이프라인 설계
sidebar_label: 파이프라인 설계
sidebar_position: 9
---

# 전사 파이프라인 설계

SAST·SCA·시크릿 탐지·컨테이너 보안·IaC 보안·DAST 6개 영역을 하나의 파이프라인으로 통합하는 설계 방법을 안내합니다.
각 영역 페이지에서 다룬 개별 설정을 실제 운영 환경에 맞게 조합하는 방법에 집중합니다.

## 파이프라인 설계 원칙

**병렬 실행**: 독립적인 검사는 병렬로 실행해 전체 파이프라인 소요 시간을 최소화합니다. SAST·SCA·시크릿 탐지는 서로 의존성이 없으므로 동시에 실행할 수 있습니다.

**단계별 게이트**: 빠른 검사(시크릿·SAST)를 앞에 두고 느린 검사(DAST)를 뒤에 배치합니다. 앞 단계가 실패하면 뒤 단계를 실행할 필요가 없으므로 불필요한 자원 소비를 줄입니다.

**실패 정책 분리**: 즉시 차단(Hard Fail)과 경고만(Soft Fail)을 명확히 구분합니다. 팀이 수용 가능한 수준에서 시작해 점진적으로 강화하는 방식이 실제 도입 성공률을 높입니다.

**결과 보존**: 모든 검사 결과를 아티팩트로 보관합니다. 감사 대응·트렌드 분석·재현을 위해 일정 기간 유지하는 것이 중요합니다.

---

## 파이프라인 전체 구조

| 단계 | 검사 항목              | 실행 시점  | 실패 정책      | 소요 시간 |
| ---- | ---------------------- | ---------- | -------------- | --------- |
| 1    | 시크릿 탐지 (Gitleaks) | PR         | Hard Fail      | ~1분      |
| 2    | SAST (Semgrep)         | PR         | Hard Fail      | 2~5분     |
| 2    | SCA (syft+grype)       | PR         | Hard Fail      | 2~3분     |
| 2    | IaC 보안 (Checkov)     | PR         | Hard Fail      | 1~2분     |
| 3    | 컨테이너 보안 (Trivy)  | Push/Merge | Hard Fail      | 3~5분     |
| 4    | DAST (ZAP Baseline)    | Push/Merge | Soft Fail→Hard | 5~10분    |

2단계 검사들은 병렬 실행으로 전체 소요 시간을 5분 내로 유지할 수 있습니다.

---

## GitHub Actions 통합 워크플로우

### PR 단계 (병렬 실행)

```yaml
# .github/workflows/devsecops-pr.yml

name: DevSecOps — PR Check

on:
  pull_request:
    branches: [main, develop]

jobs:
  # 1단계: 시크릿 탐지 (가장 먼저)
  secret-detection:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # 2단계: 병렬 실행
  sast:
    runs-on: ubuntu-latest
    needs: secret-detection
    steps:
      - uses: actions/checkout@v4
      - uses: semgrep/semgrep-action@v1
        with:
          config: p/owasp-top-ten p/security-audit

  sca:
    runs-on: ubuntu-latest
    needs: secret-detection
    steps:
      - uses: actions/checkout@v4
      - uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cdx.json
      - uses: anchore/scan-action@v3
        with:
          sbom: sbom.cdx.json
          fail-build: true
          severity-cutoff: high
          config: .grype.yaml
      - uses: actions/upload-artifact@v4
        with:
          name: sbom-${{ github.sha }}
          path: sbom.cdx.json

  iac:
    runs-on: ubuntu-latest
    needs: secret-detection
    steps:
      - uses: actions/checkout@v4
      - uses: bridgecrewio/checkov-action@master
        with:
          directory: .
          framework: terraform,kubernetes,dockerfile
          soft_fail: false
```

### Push/Merge 단계 (컨테이너·DAST)

```yaml
# .github/workflows/devsecops-merge.yml

name: DevSecOps — Post Merge

on:
  push:
    branches: [main]

jobs:
  container-security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          exit-code: 1
          severity: HIGH,CRITICAL
          ignore-unfixed: true

  dast:
    runs-on: ubuntu-latest
    needs: container-security
    steps:
      - uses: actions/checkout@v4
      - name: Start application
        run: |
          docker compose up -d
          sleep 15
      - uses: zaproxy/action-baseline@v0.12.0
        with:
          target: http://localhost:8080
          fail_action: false # 초기 도입 시 Soft Fail
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: zap-report-${{ github.sha }}
          path: report_html.html
```

---

## GitLab CI 통합 파이프라인

```yaml
# .gitlab-ci.yml (전체 통합)

stages:
  - secret-scan
  - code-scan
  - build-scan
  - dast

variables:
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

secret-detection:
  stage: secret-scan
  image: zricethezav/gitleaks:latest
  script:
    - gitleaks detect --source . --exit-code 1
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

sast:
  stage: code-scan
  image: semgrep/semgrep:latest
  script:
    - semgrep ci --config p/owasp-top-ten --error
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

sca:
  stage: code-scan
  image: ubuntu:22.04
  script:
    - curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh
      | sh -s -- -b /usr/local/bin
    - curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh
      | sh -s -- -b /usr/local/bin
    - syft . -o cyclonedx-json=sbom.cdx.json
    - grype sbom:sbom.cdx.json --fail-on high --config .grype.yaml
  artifacts:
    paths: [sbom.cdx.json]
    expire_in: 90 days
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

iac-security:
  stage: code-scan
  image: bridgecrew/checkov:latest
  script:
    - checkov -d . --framework terraform,kubernetes,dockerfile
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

container-security:
  stage: build-scan
  image: aquasec/trivy:latest
  script:
    - docker build -t $IMAGE_TAG .
    - trivy image --severity HIGH,CRITICAL
      --exit-code 1 --ignore-unfixed $IMAGE_TAG
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

dast:
  stage: dast
  image: ghcr.io/zaproxy/zaproxy:stable
  script:
    - docker compose up -d && sleep 15
    - zap-baseline.py -t http://localhost:8080
      -r zap-report.html -I # -I: 실패해도 계속 (Soft Fail)
  artifacts:
    paths: [zap-report.html]
    expire_in: 30 days
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

---

## 멀티 저장소 정책 일관성

:::tip 재사용 가능한 워크플로우로 정책을 중앙 관리하세요
:::

**GitHub Actions Reusable Workflow**: 공통 워크플로우를 별도 저장소(예: `your-org/security-workflows`)에 관리하고 각 프로젝트에서 `uses: your-org/security-workflows/.github/workflows/devsecops-pr.yml@main`으로 참조합니다. 정책 변경 시 한 곳만 수정하면 전체 저장소에 즉시 반영됩니다.

**GitLab CI 템플릿**: `include:` 키워드로 중앙 저장소의 CI 템플릿을 참조합니다. 프로젝트별 오버라이드는 `extends:`로 처리하면 기본 정책을 유지하면서 예외를 허용할 수 있습니다.

**정책 파일 동기화**: `.grype.yaml`·`.gitleaks.toml`·`.trivyignore.yaml` 등 정책 파일을 별도 저장소에서 관리하고 각 프로젝트에 git submodule 또는 파일 복사 스크립트로 배포합니다. 정책 파일의 버전 이력이 보존되어 감사 대응에 유리합니다.

---

## 빌드 실패 시 개발자 안내

:::warning 빌드 실패 메시지는 개발자가 즉시 행동할 수 있어야 합니다
"취약점 발견"만 알리면 개발자가 무엇을 해야 할지 모릅니다.
:::

**명확한 실패 원인**: 어떤 패키지의 어떤 CVE인지, 어떤 파일의 어떤 라인인지 메시지에 포함합니다. 원인이 불분명한 실패는 개발자의 불신과 알림 무시로 이어집니다.

**수정 방법 안내**: 가능하면 "이 버전으로 업그레이드하세요" 같은 구체적 조치를 메시지에 포함합니다. grype는 fix 버전을 자동으로 표시하므로 별도 작업 없이 수정 안내가 제공됩니다.

**예외 처리 경로**: 즉시 수정이 불가능한 경우 예외 신청 방법(담당자·문서 링크)을 빌드 실패 메시지에 안내합니다. 예외 경로가 없으면 개발자가 무력감을 느끼거나 보안 검사를 우회하려는 시도가 발생합니다.

---

## 다음 단계

- 배포 후 지속적 모니터링·자동 패치: [모니터링·자동 교정](./monitoring)
- ISO/IEC 18974 요구사항 매핑: [ISO 표준 연계](./iso-mapping)
