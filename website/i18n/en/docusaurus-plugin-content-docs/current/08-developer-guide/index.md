---
title: 'Developer Guide: Automatic Open Source Policy Compliance in Claude Code'
sidebar_label: Developer Guide (Optional)
sidebar_position: 8
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: (Optional chapter - no mandatory items, supports G1.6 operational reinforcement)'
  - 'ISO/IEC 18974: (Optional chapter - no mandatory items, supports G3S.1 operational reinforcement)'
self_study_time: 2 hours
---

<!-- This exceeds the 200-350 line guidance in STYLEGUIDE.md section 1. Keeping methods 1-4
     as separate pages made the reader navigate four times and duplicated text between
     sections, so they were merged into one page. The full SKILL.md and the full workflow
     are folded into <details> to keep them out of the reading flow.
     The license list in method 1 stays complete because readers paste it into their own
     CLAUDE.md. When a category changes, three places must be updated together: the canonical
     page (reference/concepts/license-classification), ai-coding/rules-template, and this file. -->

# Developer Guide: Automatic Open Source Policy Compliance in Claude Code

## 1. What we do in this chapter

With chapters 01–07, your open source management system is complete.
The remaining task is **making sure the policy is followed automatically in day-to-day development**.

Having the program manager review every PR is not sustainable.
This chapter explains four ways to use Claude Code so that **developers comply with the policy without thinking about it**.

:::info Goal
Claude Code keeps the policy for you, even when the program manager does not review every change — reaching this state is the goal of this chapter.
:::

:::note This chapter vs. the AI coding Rules template
This chapter shows four ways to automatically apply **the organizational policy you built earlier** (`output/policy/`) to daily development.
If you have not created a policy yet and just want a quick Rules file for AI coding tools, use the [Common Rules Template](/ai-coding/rules-template).
:::

## 2. Background: Why automation is needed

:::tip
If SBOM and license terminology is unfamiliar, see the [Glossary](/reference/glossary).
:::

### Problems that actually happen

**Scenario 1: A GPL package is added without thinking**
A developer finds a convenient utility library.
They run `npm install some-gpl-utility` and open a PR.
Until the program manager reviews it, the risk of GPL contamination remains hidden.
If it is discovered after distribution, a source code disclosure obligation may arise.

**Scenario 2: A vulnerable version stays in use**
An old version keeps being used without dependency updates.
A Critical vulnerability with CVSS 9.0 is disclosed, but the team is unaware of it.
When a security incident occurs, "we didn't know" is not an acceptable excuse.

**Scenario 3: A policy violation the program manager never sees**
A package with a license not on the approved license list (`license-allowlist.md`) is added.
It is distributed without going through the usage approval process (`usage-approval.md`).
The violation is only discovered at certification renewal time.

### Guiding principle

Do not rely on developers' **memory and willpower** for policy compliance.
Make tools and automation the **default**.

## 3. Overview of the four methods

Apply a combination of the four methods below. The higher the level of assurance, the higher the implementation complexity.

| Method                          | Description                                                              | Assurance level | Implementation difficulty |
| ------------------------------- | ------------------------------------------------------------------------ | --------------- | ------------------------- |
| **Policy in CLAUDE.md**         | Tell Claude Code directly which policies to follow                       | 70%             | Very easy                 |
| **Skill definition**            | Turn the license and vulnerability check procedure into a reusable skill | 80%             | Easy                      |
| **Automatic checks with Hooks** | Automatically raise a warning whenever a dependency file changes         | 90%             | Moderate                  |
| **CI/CD pipeline**              | Automatic checks on every PR; merges are blocked on violations           | 99%             | Somewhat complex          |

:::info[Core principle]
For complete assurance, apply all four methods. Each method works independently, but the more you combine them, the lower the risk of anything slipping through.
:::

## 4. Detailed guide to each method

We recommend starting with the easiest method 1 and reinforcing it with 3 and 4.

### Method 1 — State the policy in CLAUDE.md (70% assurance, very easy) {#method-1}

Add the section below to `CLAUDE.md` in the project root and Claude Code will reference this policy automatically when it helps you add a package. The categories follow [License Classification](/reference/concepts/license-classification). The allowlist that actually governs your company is `output/policy/license-allowlist.md`, generated in the 03 Policy chapter, so adjust the example to match that file after pasting it.

```markdown
## Open Source Policy (automatic compliance)

### Allowed licenses

The following licenses may be used for new packages without separate approval:

- MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
- Full list: see output/policy/license-allowlist.md

### Conditionally allowed licenses

The following licenses may be used after review and approval by the program manager:

- LGPL, MPL (Weak Copyleft - source disclosure obligation depending on usage, legal review required)
- CC-BY-SA (a content license, so applying it to software requires separate review)
- Conditions and exceptions: see output/policy/license-allowlist.md

### Prohibited licenses

The following licenses must not be added without prior approval:

- GPL, AGPL (Copyleft - source code disclosure obligation on distribution)
- SSPL, Commons Clause (use restrictions that do not meet the Open Source Definition)
- Any license with a clause prohibiting commercial use

### Vulnerability policy

- Do not use packages with vulnerabilities of CVSS 7.0 or higher (High/Critical)
- Upgrade versions with known vulnerabilities to a patched version

### Checks when adding a package

When adding a new package, always check in this order:

1. License check: run `license-checker` or the `/oss-policy-check` skill
2. Vulnerability check: run the OSV API or `grype`
3. Allowlist comparison: compare against output/policy/license-allowlist.md
4. On violation: request usage approval from the program manager (see output/process/usage-approval.md)
```

:::note The canonical source for the categories
The criteria behind the allowed, conditional, and prohibited categories are owned by
[License Classification](/reference/concepts/license-classification). The example above restates
those criteria in CLAUDE.md form, so check the canonical page first if a category changes. The full
rule set for AI coding tool configuration files is in the
[Common Rules Template](/ai-coding/rules-template).
:::

- Effect: Claude Code is aware of the policy and warns you on violations.
- Limitation: if a developer runs `npm install` directly in the terminal, Claude Code cannot intervene.

### Method 2 — Standardize checks with a Skill (80% assurance, easy) {#method-2}

Turn the license and vulnerability check procedure into an `/oss-policy-check` skill so anyone can run the same check with a single command. Skills are defined per directory, and the frontmatter (name, description) at the top of the file is required for the skill to be recognized.

```bash
mkdir -p .claude/skills/oss-policy-check
```

You can invoke it anywhere in this project with `/oss-policy-check`. To use it in every project, put the same content in `~/.claude/skills/`.

<details>
<summary>Full <code>.claude/skills/oss-policy-check/SKILL.md</code></summary>

````markdown
---
name: oss-policy-check
description: Open source policy compliance check. Run when a developer requests /oss-policy-check or asks to "check the open source policy".
---

# OSS Policy Compliance Check

## Execution steps

### Step 1: License check

Node.js project:

```bash
npx license-checker --summary --excludePrivatePackages
```

Python project:

```bash
pip-licenses --format=markdown --with-urls
```

Java/Maven project:

```bash
mvn license:aggregate-third-party-report
```

### Step 2: Allowlist comparison

Compare against the allowed licenses in output/policy/license-allowlist.md.
If a license not on the list is found, issue a warning immediately.

### Step 3: Vulnerability lookup (OSV API)

Look up vulnerabilities for the discovered packages via the OSV API:

```bash
# Use grype (recommended)
grype dir:. --fail-on high

# Or use OSV-Scanner
osv-scanner --recursive .
```

### Step 4: Report format

Report the check results in the following format:

---

## OSS Policy Check Results

**Check date:** YYYY-MM-DD
**Target project:** [project name]

### License status

| License    | Package count | Status       |
| ---------- | ------------- | ------------ |
| MIT        | 45            | ✅ Allowed   |
| Apache-2.0 | 12            | ✅ Allowed   |
| GPL-3.0    | 1             | ❌ Violation |

### Vulnerability status

| CVE           | CVSS | Package        | Status                 |
| ------------- | ---- | -------------- | ---------------------- |
| CVE-2024-XXXX | 9.1  | lodash@4.17.15 | ❌ Urgent patch needed |

### Recommendations

- [ ] Replace the GPL-3.0 package or request usage approval
- [ ] Upgrade lodash to 4.17.21 or later
````

</details>

- Effect: the check procedure is standardized into one reusable command.
- Limitation: if developers forget to run it, nothing is checked.

### Method 3 — Automatic reminders with Hooks (90% assurance, moderate) {#method-3}

With the Hook below configured in `.claude/settings.json`, a warning is displayed automatically whenever a dependency file changes.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "node -e \"\nlet raw = '';\nprocess.stdin.on('data', (c) => (raw += c));\nprocess.stdin.on('end', () => {\n  const hook = JSON.parse(raw);\n  const file = (hook.tool_input && hook.tool_input.file_path) || '';\n  const depFiles = ['package.json', 'requirements.txt', 'pom.xml', 'go.mod', 'Cargo.toml'];\n  if (depFiles.some((f) => file.endsWith(f))) {\n    console.error('[OSS Policy Warning] A dependency file was changed.');\n    console.error('Always check the licenses and vulnerabilities of new packages.');\n    console.error('How to check: run /oss-policy-check');\n    process.exit(2);\n  }\n});\n\""
          }
        ]
      }
    ]
  }
}
```

The hook command receives JSON on standard input describing the tool call (`tool_name`, `tool_input`, `tool_response`). The example decides whether the file is a dependency file from `tool_input.file_path` and, if so, exits with code 2 so the warning reaches Claude. This Hook serves as an automatic reminder of the package addition approval procedure defined in `output/process/usage-approval.md`.

- Effect: changes to `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, `Cargo.toml`, and similar files trigger an automatic reminder.
- Stronger control: to block the edit itself, register the same script as a `PreToolUse` Hook. In PreToolUse, exit code 2 blocks the tool call before it runs.
- Limitation: files modified outside Claude Code are not detected, so complement this with CI/CD.

### Method 4 — Block merges with CI/CD (99% assurance, somewhat complex) {#method-4}

Automatically check every PR with syft and grype, and block the merge on policy violations. This guards the last gate regardless of what people or tools miss. The example below uses free open source tools only ([syft](https://github.com/anchore/syft) and [grype](https://github.com/anchore/grype) are both Apache-2.0).

Put only licenses in the prohibited category of [License Classification](/reference/concepts/license-classification) into the block list. Conditionally allowed licenses such as LGPL and MPL go to program manager review rather than failing the build, which is what the canonical page specifies.

<details>
<summary>Full <code>.github/workflows/oss-policy-check.yml</code></summary>

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
    name: License policy check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: Generate SBOM with syft
        uses: anchore/sbom-action@v0
        with:
          format: cyclonedx-json
          output-file: sbom.cdx.json

      - name: Extract licenses and check policy
        run: |
          # Extract the license list from the SBOM (sbom.cdx.json) generated in the previous step
          jq -r '.components[]?.licenses[]? | (.license.id // .license.name // .expression) // empty' sbom.cdx.json | sort -u > detected-licenses.txt

          echo "=== Detected licenses ==="
          cat detected-licenses.txt

          # Check for prohibited licenses (grep -E extended regex; -only/-or-later variants also match partially)
          # \b is a word boundary, so LGPL does not match. LGPL and MPL are conditionally
          # allowed rather than prohibited, so they go to manager review instead of a block.
          # Requires GNU grep.
          FORBIDDEN='\b(GPL-2\.0|GPL-3\.0|AGPL-3\.0|SSPL-1\.0|Commons-Clause)'
          if grep -qE "$FORBIDDEN" detected-licenses.txt; then
            echo "::error::Prohibited licenses detected. Obtain program manager approval or use an alternative package."
            grep -E "$FORBIDDEN" detected-licenses.txt
            exit 1
          fi

          echo "✅ License check passed"

  vulnerability-check:
    name: Vulnerability check (block High or above)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: Scan vulnerabilities with grype
        id: scan
        uses: anchore/scan-action@v7
        with:
          path: '.'
          fail-build: true
          severity-cutoff: high # Block the merge when a High / Critical vulnerability is found
          output-format: sarif # The result file path is referenced below via outputs

      - name: Upload vulnerability report
        if: always()
        uses: actions/upload-artifact@v7
        with:
          name: vulnerability-report
          # Since v6 the result file is written to a temp path; reference it via outputs.
          path: ${{ steps.scan.outputs.sarif }}
```

</details>

:::note
This step supports the automated, continuous verification of the ISO/IEC 18974 G3S.1 requirement (identifying known vulnerabilities).
:::

- Effect: every PR is checked regardless of the development environment, and merges are blocked when a prohibited license or a High or above vulnerability is found. Results appear directly on the PR.
- Limitation: initial setup and exception management take some effort.

How to put the same checks into an organization-wide pipeline, and the per-tool settings, are covered in [Software Composition Analysis (SCA)](/devsecops/sca).

### Recommended combinations by situation

You do not need to adopt all four at once. Start with the combination that fits your situation.

| Situation                                      | Recommended combination | Reason                                                             |
| ---------------------------------------------- | ----------------------- | ------------------------------------------------------------------ |
| Small team of 1–2 / quick start                | Methods 1 + 3           | Lightweight setup with immediate reminders inside Claude Code      |
| Officially shipped product / external delivery | Methods 1 + 3 + 4       | CI/CD merge blocking enforces checks with nothing slipping through |
| Making the check procedure a team standard     | Above + Method 2        | Everyone runs the same check with the same command                 |

We recommend a phased rollout: apply method 1 in five minutes first to see the effect, then add enforcement with method 4 as your release frequency grows.

## 5. Completion check

:::info Self-study mode (about 2 hours)
Take your time and work through each step until you understand it.
:::

This chapter is complete when all items below are done.

- [ ] Open source policy section added to the project `CLAUDE.md`
- [ ] `.claude/skills/oss-policy-check/SKILL.md` created
- [ ] `/oss-policy-check` run and confirmed working
- [ ] Hook configured in `.claude/settings.json`
- [ ] Warning message confirmed when a dependency file is modified
- [ ] `.github/workflows/oss-policy-check.yml` created
- [ ] Test PR opened and the license and vulnerability checks confirmed to run automatically

## 6. Next steps

If you have completed this chapter, your open source management system has moved **beyond being built into daily operation**.

**Maintenance recommendations:**

- Renew OpenChain self-certification every 18 months (see [Self-Certification Declaration: The Final Step](../07-conformance/index.md))
- Review and update `license-allowlist.md` quarterly
- Re-scan with grype when new CVEs are published

**Going further:**

- Join the [OpenChain community](https://www.openchainproject.org/)
- Share SBOMs with supply chain partners (using `output/sbom/sbom-sharing-template.md`)
