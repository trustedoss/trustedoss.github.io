---
sidebar_position: 1
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

Add the section below to `CLAUDE.md` in the project root. The categories follow
[License Classification](/reference/concepts/license-classification). The allowlist that
actually governs your company is `output/policy/license-allowlist.md`, generated in the
03 Policy chapter, so adjust the example to match that file after pasting it.

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

**Effect:** When Claude Code helps you add a package, it automatically consults this policy and warns you.

**Limitation:** If a developer runs `npm install` directly in the terminal, Claude Code cannot intervene.

:::note Canonical source for the categories
[License Classification](/reference/concepts/license-classification) is the canonical source
for the allowed, conditional, and prohibited categories. The example above restates those
criteria in CLAUDE.md form, so check the canonical page first whenever a category changes.
The full rule set for AI coding tool config files is in the
[Common Rules Template](/ai-coding/rules-template).
:::

---

→ Next: [Method 2: Defining a Skill](./method2-skill.md)
