---
id: monitoring
title: Continuous Monitoring and Automated Remediation
sidebar_label: Monitoring and Automated Remediation
sidebar_position: 10
---

# Continuous monitoring and automated remediation

A CI/CD gate checks the state of the code at deployment time but cannot respond to new vulnerabilities that emerge afterward.
Combining Dependabot·Renovate with scheduled scans lets you continuously detect vulnerabilities in production and automatically generate patch PRs.

## Why post-deployment monitoring is necessary

:::info A CI/CD gate only checks a snapshot taken at deployment time
The pipeline cannot detect a new CVE
discovered after deployment.
:::

**Nature of new CVEs**: Code deployed today may become vulnerable to a new CVE tomorrow. Log4Shell is a classic example, where a library used for years turned into a Critical vulnerability overnight. Scan results taken at deployment time lose their meaning over time.

**Limits of a pipeline without monitoring**: Even code that passed the PR stage may have vulnerabilities 30 days later. Without continuous scanning, your service runs unaware of the risks in production.

**Need for automation**: Manually tracking hundreds of dependencies is not realistic. The key is to minimize human intervention and accelerate patching with automated tools like Dependabot·Renovate.

---

## Dependabot setup

### Basic configuration

Adding `.github/dependabot.yml` to a GitHub repository automatically opens dependency-update and security-patch PRs.

```yaml
# .github/dependabot.yml

version: 2
updates:
  # npm dependencies
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
      day: monday
      time: '09:00'
    open-pull-requests-limit: 10
    groups:
      # Group minor/patch updates to reduce PR count
      minor-and-patch:
        update-types:
          - minor
          - patch

  # Python dependencies
  - package-ecosystem: pip
    directory: /
    schedule:
      interval: weekly
    ignore:
      # major updates require manual review
      - dependency-name: django
        update-types: [version-update:semver-major]

  # Docker base images
  - package-ecosystem: docker
    directory: /
    schedule:
      interval: weekly

  # GitHub Actions self-updates
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

### Enable security alerts

Dependabot security alerts on GitHub work automatically once you enable them in your repository settings.
With no further configuration, a PR is opened immediately when a Critical or High vulnerability is found based on the GitHub Advisory Database.

---

## Renovate setup

Renovate allows finer-grained policy configuration than Dependabot and supports GitHub·GitLab·Bitbucket alike.
It can also be run self-hosted on GitLab.

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
| Platform         | GitHub only | GitHub·GitLab·Bitbucket           |
| Setup complexity | Low         | High (very flexible)              |
| Auto-merge       | Limited     | Configurable with detailed policy |
| Grouped PRs      | Supported   | Supported (more granular)         |
| Cost             | Free        | Free (self-hosted)                |

---

## Automate scheduled scans

Beyond the PR phase, run a separate scheduled workflow that periodically scans deployed code.

```yaml
# .github/workflows/scheduled-scan.yml

name: Scheduled Security Scan

on:
  schedule:
    - cron: '0 2 * * *' # daily 2 AM
  workflow_dispatch: # manual run available

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
          retention-days: 365 # retain yearly

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

:::tip Alerts must reach the responsible owner immediately
:::

**Use the GitHub Security tab**: Dependabot and code-scan results are automatically aggregated in the repository's Security tab. For critical findings, wiring email and Slack notifications to the owner can greatly shorten response time.

**Create issues automatically**: When a scheduled scan finds a new vulnerability, automatically open an issue via GitHub Actions so you can assign an owner and track the SLA. Once vulnerabilities are managed as issues, patch progress can be shared across the whole team.

**Archive SBOMs by year**: Permanently archive the SBOMs produced by scheduled scans, organized by release version. These serve as an audit-response trail for ISO/IEC 18974 and are also useful for reproducing the dependency state at a specific point in time.

---

## Self-Study — Level 2 Automation

:::tip Build automation workflows with Claude Code
The agents below work in conjunction with the CI/CD pipeline.
They generate workflow files that fully automate security analysis.
:::

**Prerequisite**: Clone the [Trusted OSS repository](https://github.com/trustedoss/trustedoss.github.io)

### Automated PR security-analysis comments

Each time a PR is opened, Claude analyzes the security scan results and
automatically posts a comment on the PR.

```bash
cd agents/level2-automation/pr-comment
claude
```

Generated output:

- `.github/workflows/pr-security-comment.yml` (GitHub Actions)
- `gitlab-pr-comment.yml` (GitLab CI conversion version)

### Automatic issue creation + Dependabot analysis

Automatically opens issues when scheduled scans find High/Critical vulnerabilities,
and automatically posts impact-analysis comments on Dependabot PRs.

```bash
cd agents/level2-automation/issue-tracker
claude
```

Generated output:

- `.github/workflows/scheduled-security-scan.yml`
- `.github/workflows/dependabot-analysis.yml`
- `gitlab-scheduled-scan.yml` (GitLab CI conversion version)

:::info GitHub Actions vs GitLab CI
GitHub Actions provides YAML verified to actually work.
GitLab CI provides conversion patterns and annotations for the same functionality.
Both platforms require ANTHROPIC_API_KEY to be registered as a Secret/Variable.
:::

---

## Next steps

- Mapping ISO/IEC 18974 requirements to implementation: [ISO Standard Linkage](./iso-mapping)
