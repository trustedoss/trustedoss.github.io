---
id: monitoring
title: Continuous monitoring and automatic correction
sidebar_label: Monitoring and automatic correction
sidebar_position: 10
---

# Continuous monitoring and automatic correction

The CI/CD gate checks the code state at the time of deployment, but cannot respond to new vulnerabilities that occur after deployment.
Dependabot·Renovate·The combination of regular scans allows you to continuously detect vulnerabilities in your production environment and automatically generate patch PRs.

## Why post-deployment monitoring is necessary

:::info The CI/CD gate only checks snapshots at the time of deployment
The new CVE discovered after distribution is
The pipeline cannot detect it.
:::

**Characteristics of the new CVE**: Code deployed today may be vulnerable to the new CVE tomorrow. A representative example is Log4Shell, where a library that has been used for years becomes a Critical vulnerability overnight. Scan results at the time of distribution lose meaning over time.

**Limitations of a pipeline without monitoring**: Even code that passes the PR stage may have vulnerabilities after 30 days. Without continuous scanning, your service will operate without awareness of risks in your production environment.

**Need for automation**: Manually tracking hundreds of dependencies is not realistically possible. The key is to minimize human intervention and speed up patching with automated tools like Dependabot·Renovate.

---

## Dependabot settings

###Default settings

Adding `.github/dependabot.yml` to the GitHub repository automatically creates a dependency update/security patch PR.

```yaml
# .github/dependabot.yml

version: 2
updates:
  # npm 의존성
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
      day: monday
      time: '09:00'
    open-pull-requests-limit: 10
    groups:
      # 마이너·패치 업데이트는 그룹으로 묶어 PR 수 감소
      minor-and-patch:
        update-types:
          - minor
          - patch

  # Python 의존성
  - package-ecosystem: pip
    directory: /
    schedule:
      interval: weekly
    ignore:
      # 메이저 업데이트는 수동 검토
      - dependency-name: django
        update-types: [version-update:semver-major]

  # Docker 베이스 이미지
  - package-ecosystem: docker
    directory: /
    schedule:
      interval: weekly

  # GitHub Actions 자체 업데이트
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

### Automatically enable security notifications

Dependabot Security Alerts on GitHub work automatically when you enable them in your repository settings.
Without separate settings, a PR is immediately created when a Critical or High vulnerability is discovered based on the GitHub Advisory Database.

---

## Renovate settings

Renovate allows more detailed policy settings than Dependabot, and supports all GitHub·GitLab·Bitbucket.
The same can be used in GitLab in a self-hosted manner.

```json
// renovate.json

{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:base"],
  "schedule": ["every weekend"],
  "vulnerabilityAlerts": {
    "enabled": true,
    "schedule": ["at any time"],
    "automerge": true,
    "automergeType": "pr"
  },
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true,
      "automergeType": "pr"
    },
    {
      "matchUpdateTypes": ["major"],
      "enabled": true,
      "automerge": false,
      "addLabels": ["major-update", "needs-review"]
    }
  ]
}
```

| Item             | Dependabot  | Renovate                          |
| ---------------- | ----------- | --------------------------------- |
| platform         | GitHub only | GitHub·GitLab·Bitbucket           |
| Setup complexity | low         | High (high flexibility)           |
| Auto Merge       | LIMITED     | Detailed policy settings possible |
| Group PR         | possible    | Possible (more detailed)          |
| cost             | Free        | Free (self-hosted)                |

---

## Automate regular scans

In addition to the PR phase, we separately operate a scheduled workflow that periodically scans distributed code.

```yaml
# .github/workflows/scheduled-scan.yml

name: Scheduled Security Scan

on:
  schedule:
    - cron: '0 2 * * *' # 매일 새벽 2시
  workflow_dispatch: # 수동 실행 가능

jobs:
  sca-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cdx.json

      - name: Scan for new CVEs
        uses: anchore/scan-action@v3
        with:
          sbom: sbom.cdx.json
          fail-build: true
          severity-cutoff: critical

      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom-scheduled-${{ github.run_id }}
          path: sbom.cdx.json
          retention-days: 365 # 연간 보관

  container-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Scan production image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ vars.PROD_IMAGE }}
          exit-code: 1
          severity: CRITICAL
          ignore-unfixed: true
```

---

## Notification and response system

:::tip Notifications must be delivered to the person in charge immediately
:::

**GitHub Utilize the Security tab**: Dependabot·Code scan results are automatically aggregated to the repository Security tab. When a critical finding is made, response time can be greatly shortened by linking email and Slack notifications to the person in charge.

**Automatically create issues**: When a new vulnerability is discovered in a schedule scan, an issue is automatically created with GitHub Actions to enable assigning a person in charge and tracking SLA. Once vulnerabilities are managed as issues, patch progress can be shared with the entire team.

**SBOM Archive by Year**: Permanently archive SBOM generated from regular scans by release version. ISO/IEC 18974 Can be used as an audit response trace, and is also useful for reproducing the dependency status at a specific point in time.

---

## Self-Study — Level 2 Automation

:::tip Create automation workflow with Claude Code
The agents below work in conjunction with the CI/CD pipeline.
Create workflow files to fully automate security analysis.
:::

**Prerequisite**: Requires clone of [Trusted OSS repository](https://github.com/trustedoss/trustedoss.github.io)

### PR Security Analysis Automatic Comments

Every time a PR is created, Claude analyzes the security scan results and
Automatically post comments to PR.

```bash
cd agents/level2-automation/pr-comment
claude
```

Generated output:

- `.github/workflows/pr-security-comment.yml` (GitHub Actions)
- `gitlab-pr-comment.yml` (GitLab CI conversion version)

### Automatic issue registration + Dependabot analysis

Automatically creates issues when High/Critical vulnerabilities are found in regular scans
Dependabot Automatically publish impact analysis comments to PR.

```bash
cd agents/level2-automation/issue-tracker
claude
```

Generated output:

- `.github/workflows/scheduled-security-scan.yml`
- `.github/workflows/dependabot-analysis.yml`
- `gitlab-scheduled-scan.yml` (GitLab CI conversion version)

:::info GitHub Actions vs GitLab CI
GitHub Actions provides YAML that has been verified to actually work.
GitLab CI contains conversion patterns and annotations for the same function.
Both platforms require ANTHROPIC_API_KEY to be registered as Secret/Variable.
:::

---

## Next steps

- ISO/IEC 18974 Requirements and implementation mapping: [ISO standard linkage](./iso-mapping)
