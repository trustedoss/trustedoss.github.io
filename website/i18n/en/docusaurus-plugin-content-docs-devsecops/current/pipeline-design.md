---
id: pipeline-design
title: Transcription Pipeline Design
sidebar_label: pipeline design
sidebar_position: 9
---

# Transcription pipeline design

We guide you through a design method that integrates the six areas of SAST, SCA, secret detection, container security, IaC security, and DAST into one pipeline.
We focus on how to combine the individual settings covered on each area page to suit your actual operating environment.

## Pipeline design principles

**Parallel execution**: Independent tests run in parallel to minimize overall pipeline time. SAST, SCA, and Secret detection do not depend on each other, so they can run simultaneously.

**Step-by-step gate**: Place fast tests (Secret/SAST) at the front and slow tests (DAST) at the back. If the previous step fails, the later step does not need to be executed, thus reducing unnecessary resource consumption.

**Separation of failure policies**: Clear distinction between hard fail and warning only (soft fail). Starting at an acceptable level and gradually strengthening the team increases the success rate of actual adoption.

**Result Retention**: All test results are kept as artifacts. It is important to maintain it for a certain period of time for audit response, trend analysis, and reproduction.

---

## Pipeline overall structure

| steps | Inspection items            | When to run | failure policy | Time required |
| ----- | --------------------------- | ----------- | -------------- | ------------- |
| 1     | Secret detection (Gitleaks) | PR          | Hard Fail      | ~1 minute     |
| 2     | SAST (Semgrep)              | PR          | Hard Fail      | 2~5 minutes   |
| 2     | SCA (syft+grype)            | PR          | Hard Fail      | 2~3 minutes   |
| 2     | IaC Security (Checkov)      | PR          | Hard Fail      | 1-2 minutes   |
| 3     | Container Security (Trivy)  | Push/Merge  | Hard Fail      | 3~5 minutes   |
| 4     | DAST (ZAP Baseline)         | Push/Merge  | Soft Fail→Hard | 5-10 minutes  |

Two-stage tests can be run in parallel to keep the overall time within 5 minutes.

---

## GitHub Actions Integrated Workflow

### PR phase (parallel execution)

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

### Push/Merge stage (Container·DAST)

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

## GitLab CI integration pipeline

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

## Multi-store policy consistency

:::tip Centrally manage policies with reusable workflows
:::

**GitHub Actions Reusable Workflow**: Manage common workflows in a separate repository (e.g. `your-org/security-workflows`) and reference them as `uses: your-org/security-workflows/.github/workflows/devsecops-pr.yml@main` in each project. When a policy change is made in just one location, it is immediately reflected in the entire repository.

**GitLab CI Template**: References a CI template in the central repository with the `include:` keyword. Project-specific overrides can be handled with `extends:` to allow exceptions while maintaining the default policy.

**Policy file synchronization**: Manage policy files such as `.grype.yaml`·`.gitleaks.toml`·`.trivyignore.yaml` in a separate repository and distribute them to each project using git submodule or file copy script. The version history of the policy file is preserved, which is advantageous for audit response.

---

## Developer guidance when build fails

:::warning Build failure messages should allow developers to act immediately
All you have to do is report a “vulnerability found” and developers won’t know what to do.
:::

**Clear cause of failure**: Include in the message which CVE in which package and which line in which file. Failures with unclear causes lead to developer distrust and ignoring notifications.

**How ​​to Fix**: If possible, include a specific action in your message, such as “Upgrade to this version.” grype automatically displays the fix version, providing guidance on fixing it without any additional work.

**Exception handling path**: If immediate correction is not possible, instructions on how to apply for an exception (person in charge/document link) will be provided in the build failure message. The absence of exception paths leaves developers feeling helpless or attempting to bypass security checks.

---

## Next steps

- Continuous monitoring/automatic patching after deployment: [Monitoring/automatic correction](./monitoring)
- ISO/IEC 18974 Requirements Mapping: [ISO Standard Linkage](./iso-mapping)
