---
id: monitoring
title: Continuous Monitoring and Automated Remediation
sidebar_label: Monitoring and Automated Remediation
sidebar_position: 10
---

# Continuous monitoring and automated remediation

A CI/CD gate checks the state of the code at deployment time but cannot respond to new vulnerabilities that emerge afterward.
Combining Dependabot·Renovate with scheduled scans lets you continuously detect vulnerabilities in production and automatically generate patch PRs.

:::tip The configuration below is an example — a fully working implementation lives in the reference repository
The YAML and commands on this page are examples that show the essentials. For a complete, copy-and-run pipeline (including policy files and a sample app), see the [Best Practice repository](/ai-coding/best-practice-repo).
:::

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

GitHub's Dependabot has two separate settings to enable. **Security Alerts** notify you of vulnerable
dependencies based on the GitHub Advisory Database; to have fix PRs opened automatically as well, you
must additionally enable **Dependabot security updates**. Both are enabled in the Code security menu
of the repository Settings.

---

## Renovate setup

Renovate allows finer-grained policy configuration than Dependabot and supports GitHub·GitLab·Bitbucket alike.
It can also be run self-hosted on GitLab.

```json
// renovate.json

{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
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

## What neither tool sees

Dependabot and Renovate update packages declared in a manifest. A name has to appear in
`requirements.txt`, `package.json` or `go.mod` to be in scope. Anything undeclared is outside
their view.

A runtime environment carries undeclared packages too: what the base image already had
installed, and what an installed tool bundles inside itself.

**A real case.** The container scan in the
[ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice) repository failed
on two HIGH findings.

| Package    | Vulnerability       | Installed | Fixed  |
| ---------- | ------------------- | --------- | ------ |
| msgpack    | GHSA-6v7p-g79w-8964 | 1.1.2     | 1.2.1  |
| setuptools | CVE-2025-47273      | 70.3.0    | 78.1.1 |

Neither was in `requirements.txt`. Both sat under `site-packages/pip/_vendor/`, inside pip itself.
Dependabot and Renovate never saw them, and the gate stayed red for over three months.

The repository had registered the docker ecosystem with Dependabot, which did not help. That
ecosystem updates the tag in `FROM`. A tag like `python:3.14-slim` pins no patch version, so there
is nothing to bump, and packages installed inside the image are never in scope either way.

### How to cover it

| Measure                 | What it does                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------- |
| Gate on the image       | Scanning the built image rather than the manifest is what makes this layer visible (Trivy, grype) |
| Run on a schedule       | On PRs only, a newly disclosed vulnerability waits until the next PR to surface                   |
| Drop tools from runtime | With no package manager in the container, the tree it bundles goes with it                        |
| Suppress with evidence  | Suppression is not the problem; unexplained suppression is (see below)                            |

The case above was resolved by removing pip right after `pip install`. A runtime container does not
need a package manager. The same applies to build tools, compilers and shell utilities.

### When a suppression file is the right answer

Sometimes upstream has not shipped a fix, or the vulnerable code path is never called. Excluding
such an entry in `.trivyignore` is legitimate. What makes it illegitimate is leaving no record of
what was excluded and why, at which point it is indistinguishable from switching the gate off.

The `.trivyignore` in [TRUSCA](https://github.com/trustedoss/trusca) requires each entry to carry:

- The CVE identifier, the artifact it came from, and the path the scanner reported
- Upstream fix status: unpatched, or patched but not yet in the bundled release
- A reach analysis, naming the code location that shows the vulnerable entry point is never invoked

A vulnerability that is reachable does not belong there and blocks the merge until it is fixed.
Every entry is re-judged after 180 days, or sooner if the tool cuts a new release. At that point the
file records decisions rather than hiding findings.

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
      - uses: actions/checkout@v7

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cdx.json

      - name: Scan for new CVEs
        uses: anchore/scan-action@v7
        with:
          sbom: sbom.cdx.json
          fail-build: true
          severity-cutoff: critical

      - name: Upload SBOM
        uses: actions/upload-artifact@v7
        with:
          name: sbom-scheduled-${{ github.run_id }}
          path: sbom.cdx.json
          retention-days: 365 # retain yearly

  container-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Scan production image
        uses: aquasecurity/trivy-action@0.36.0
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

## In Practice

TRUSCA runs this layer three ways.

- [dependabot.yml](https://github.com/trustedoss/trusca/blob/main/.github/dependabot.yml) — covers npm, pip, docker and github-actions — four ecosystems, six entries
- [sca-self.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sca-self.yml) — regenerates the SBOM and rescans daily at 07:00 UTC
- [dogfood-scan.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/dogfood-scan.yml) — scans its own repository with its own SCA

That last workflow defaults to advisory and turns blocking on through a `fail_on_gate` input — the
observe-first, block-later progression implemented literally.

## Self-Study — Level 2 Automation

:::tip Build automation workflows with Claude Code
The agents below work in conjunction with the CI/CD pipeline.
They generate workflow files that fully automate security analysis.
:::

**Prerequisite**: Clone the [Trusted OSS Agent repository](https://github.com/trustedoss/trustedoss-agents)

### Automated PR security-analysis comments

Each time a PR is opened, Claude analyzes the security scan results and
automatically posts a comment on the PR.

```bash
cd agents/en/level2-automation/pr-comment
claude
```

Generated output:

- `.github/workflows/pr-security-comment.yml` (GitHub Actions)
- `gitlab-pr-comment.yml` (GitLab CI conversion version)

### Automatic issue creation + Dependabot analysis

Generates a workflow that automatically registers findings from security scan results
(grype, Semgrep, license violations) at or above a configured severity as GitHub or GitLab Issues.
It includes deduplication logic keyed by CVE ID.

```bash
cd agents/en/level2-automation/issue-tracker
claude
```

Generated output:

- `.github/workflows/security-issue-tracker.yml`
- `gitlab-issue-tracker.yml` (GitLab CI conversion version)
- `ISSUE-TRACKER-SETUP.md` (guide to token permissions, labels, and cost settings)

:::info GitHub Actions vs GitLab CI
GitHub Actions provides YAML verified to actually work.
GitLab CI provides conversion patterns and annotations for the same functionality.
Both platforms require ANTHROPIC_API_KEY to be registered as a Secret/Variable.
:::

---

## Next steps

- Mapping ISO/IEC 18974 requirements to implementation: [ISO Standard Mapping](./iso-mapping)
