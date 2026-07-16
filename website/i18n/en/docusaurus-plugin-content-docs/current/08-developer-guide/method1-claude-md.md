---
sidebar_position: 2
sidebar_label: 'Method 1: CLAUDE.md Policy'
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 15 minutes
---

# Method 1: Adding the Policy to CLAUDE.md

:::info Self-study mode (about 15 minutes)
Add the policy to the project root CLAUDE.md and Claude Code recognizes it immediately.
:::

Add the section below to `CLAUDE.md` in the project root.

```markdown
## Open Source Policy (automatic compliance)

### Allowed licenses

Only the following licenses may be used for new packages:

- MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
- Full list: see output/policy/license-allowlist.md

### Prohibited licenses

The following licenses must not be added without prior approval:

- GPL-2.0, GPL-3.0, AGPL-3.0 (Copyleft - source code disclosure obligation)
- LGPL-2.0, LGPL-2.1, LGPL-3.0 (Weak Copyleft - dynamic linking review required)
- CC-BY-SA (not suitable for software)
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

**Effect:** When Claude Code helps you add a package, it automatically consults this policy and warns you.

**Limitation:** If a developer runs `npm install` directly in the terminal, Claude Code cannot intervene.

---

→ Next: [Method 2: Defining a Skill](./method2-skill.md)
