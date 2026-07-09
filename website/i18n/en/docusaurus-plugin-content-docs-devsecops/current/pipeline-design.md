---
id: pipeline-design
title: Enterprise-wide Pipeline Design
sidebar_label: Pipeline Design
sidebar_position: 9
---

# Enterprise-wide pipeline design

This page walks through how to integrate the six areas — SAST, SCA, secret detection, container security, IaC security, and DAST — into a single pipeline.
It focuses on how to combine the individual configurations covered on each area page to fit your actual operating environment.

## Pipeline design principles

**Parallel execution**: Run independent scans in parallel to minimize overall pipeline time. SAST, SCA, and secret detection have no dependencies on each other, so they can run simultaneously.

**Staged gating**: Place fast scans (secret/SAST) at the front and slow scans (DAST) at the back. If an earlier stage fails, later stages don't need to run, which reduces wasted resources.

**Separate failure policies**: Clearly distinguish hard fail from warning-only (soft fail). Starting at a tolerable level and tightening gradually increases the success rate of real-world adoption.

**Result retention**: Keep all scan results as artifacts. Retaining them for a defined period is important for audit response, trend analysis, and reproduction.

---

## Overall pipeline structure

| Stage | Checks                      | When to run | Failure policy | Time required |
| ----- | --------------------------- | ----------- | -------------- | ------------- |
| 1     | Secret detection (Gitleaks) | PR          | Hard Fail      | ~1 minute     |
| 2     | SAST (Semgrep)              | PR          | Hard Fail      | 2~5 minutes   |
| 2     | SCA (syft+grype)            | PR          | Hard Fail      | 2~3 minutes   |
| 2     | IaC Security (Checkov)      | PR          | Hard Fail      | 1-2 minutes   |
| 3     | Container Security (Trivy)  | Push/Merge  | Hard Fail      | 3~5 minutes   |
| 4     | DAST (ZAP Baseline)         | Push/Merge  | Soft Fail→Hard | 5-10 minutes  |

The stage-2 scans can run in parallel to keep the overall time within 5 minutes.

---

## GitHub Actions integrated workflow

### PR phase (parallel execution)

```yaml
# .github/workflows/devsecops-pr.yml

name: DevSecOps — PR Check

on:
  pull_request:
    branches: [main, develop]

jobs:
  # Step 1: secret detection (first)
  secret-detection:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v3
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # Step 2: run in parallel
  sast:
    runs-on: ubuntu-latest
    needs: secret-detection
    container:
      image: semgrep/semgrep
    steps:
      - uses: actions/checkout@v7
      - run: semgrep ci
        env:
          SEMGREP_RULES: p/owasp-top-ten p/security-audit

  sca:
    runs-on: ubuntu-latest
    needs: secret-detection
    steps:
      - uses: actions/checkout@v7
      - uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cdx.json
      - uses: anchore/scan-action@v7
        with:
          sbom: sbom.cdx.json
          fail-build: true
          severity-cutoff: high
          config: .grype.yaml
      - uses: actions/upload-artifact@v7
        with:
          name: sbom-${{ github.sha }}
          path: sbom.cdx.json

  iac:
    runs-on: ubuntu-latest
    needs: secret-detection
    steps:
      - uses: actions/checkout@v7
      - uses: bridgecrewio/checkov-action@master
        with:
          directory: .
          framework: terraform,kubernetes,dockerfile
          soft_fail: false
```

### Push/Merge stage (Container, DAST)

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
      - uses: actions/checkout@v7
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
      - uses: actions/checkout@v7
      - name: Start application
        run: |
          docker compose up -d
          sleep 15
      - uses: zaproxy/action-baseline@v0.12.0
        with:
          target: http://localhost:8080
          fail_action: false # Soft Fail during initial adoption
      - uses: actions/upload-artifact@v7
        if: always()
        with:
          name: zap-report-${{ github.sha }}
          path: report_html.html
```

---

## GitLab CI integration pipeline

```yaml
# .gitlab-ci.yml (full integration)

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
      -r zap-report.html -I # -I: continue on failure (Soft Fail)
  artifacts:
    paths: [zap-report.html]
    expire_in: 30 days
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

---

## Cross-repository policy consistency

:::tip Manage policies centrally with reusable workflows
:::

**GitHub Actions reusable workflows**: Keep common workflows in a dedicated repository (e.g. `your-org/security-workflows`) and reference them from each project as `uses: your-org/security-workflows/.github/workflows/devsecops-pr.yml@main`. A policy change made in one place is immediately reflected across every repository.

**GitLab CI templates**: Reference a CI template in a central repository with the `include:` keyword. Project-specific overrides can be handled with `extends:`, allowing exceptions while keeping the default policy intact.

**Policy file synchronization**: Keep policy files such as `.grype.yaml`·`.gitleaks.toml`·`.trivyignore.yaml` in a dedicated repository and distribute them to each project via git submodule or a file-copy script. Preserving the version history of policy files is advantageous for audit response.

---

## Developer guidance when a build fails

:::warning Build failure messages should let developers act immediately
Simply reporting "vulnerability found" leaves developers unsure what to do.
:::

**Clear cause of failure**: State which CVE, in which package, on which line of which file. Failures with unclear causes erode developer trust and lead to ignored alerts.

**How to fix**: Where possible, include a concrete action in the message, such as "upgrade to this version." Grype automatically shows the fixed version, providing remediation guidance with no extra effort.

**Exception path**: When an immediate fix isn't possible, the build failure message should include how to request an exception (owner and document link). Without an exception path, developers feel stuck or try to bypass the security checks.

---

## Next steps

- Continuous monitoring and automated patching after deployment: [Monitoring and Automated Remediation](./monitoring)
- ISO/IEC 18974 requirements mapping: [ISO Standard Linkage](./iso-mapping)
