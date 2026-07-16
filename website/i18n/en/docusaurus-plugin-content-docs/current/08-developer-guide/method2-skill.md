---
sidebar_position: 3
sidebar_label: 'Method 2: Skill Definition'
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 20 minutes
---

# Method 2: Defining a Skill

:::info Self-study mode (about 20 minutes)
Define it once and you can invoke it instantly anywhere in this project with `/oss-policy-check`. To use it in every project, put the same content in `~/.claude/skills/`.
:::

Create the file `.claude/skills/oss-policy-check/SKILL.md`.
Skills are defined per directory, and the frontmatter (name, description) at the top of the file is required for the skill to be recognized.

```bash
mkdir -p .claude/skills/oss-policy-check
```

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

**Effect:** Any team member can get the current status instantly with the `/oss-policy-check` command.

---

→ Next: [Method 3: Setting Up Hooks](./method3-hooks.md)
