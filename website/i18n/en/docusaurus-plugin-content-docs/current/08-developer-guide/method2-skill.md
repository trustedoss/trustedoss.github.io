---
sidebar_position: 3
sidebar_label: 'Method 2:Skill definition'
---

# Method 2:Define Skill

:::info Self-study mode(About 20 minutes)
Define it once and you can immediately call it as `/oss-policy-check` from any project.
:::

Create a `.claude/skills/oss-policy-check.md` file.

````markdown
# Skill: OSS policy compliance check (oss-policy-check)

## Trigger

Run when developers request `/oss-policy-check` or "check Open Source Policy".

## Execution Steps

### Step 1: License check

Node.js project:

```bash
npx license-checker --summary --excludePrivatePackages
```
````

Python project:

```bash
pip-licenses --format=markdown --with-urls
```

Java/Maven project:

```bash
mvn license:aggregate-third-party-report
```

### Step 2:Whitelist matching

Compare with the allowed license in output/policy/license-allowlist.md.
If a license that is not in the list is found, an immediate alert is issued.

### Step 3:vulnerability inquiry(OSV API)

Search for vulnerabilities in discovered packages using OSV API:

```bash
# use grype (recommended)
grype dir:. --fail-on high

# or use OSV-Scanner
osv-scanner --recursive .
```

### Step 4:Results reporting format

Report the test results in the format below.:

---

## OSS Policy check result

**Inspection date and time:** YYYY-MM-DD
**Target project:** [Project Name]

### License Status

| License    | number of packages | status       |
| ---------- | ------------------ | ------------ |
| MIT        | 45                 | ✅ Allowed   |
| Apache-2.0 | 12                 | ✅ Allowed   |
| GPL-3.0    | 1                  | ❌ Violation |

### vulnerability Status

| CVE           | CVSS | package        | status                 |
| ------------- | ---- | -------------- | ---------------------- |
| CVE-2024-XXXX | 9.1  | lodash@4.17.15 | ❌ Urgent patch needed |

### Recommendation

- [ ] Request for approval to replace or use GPL-3.0 package
- [ ] Upgrade to lodash 4.17.21 or higher

---

```

**Impact:** Any team member can quickly check status with `/oss-policy-check`.

---

→ Next: [Method 3: Set up Hooks](./method3-hooks.md)
```
