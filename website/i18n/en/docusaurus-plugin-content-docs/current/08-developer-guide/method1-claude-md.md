---
sidebar_position: 2
sidebar_label: 'Method 1:CLAUDE.md policy'
---

# Method 1:Adding policy to CLAUDE.md

:::info Self-study mode(About 15 minutes)
If you add a policy to your project root CLAUDE.md, Claude Code will recognize it immediately.
:::

Add the section below to `CLAUDE.md` in the project root.

```markdown
## Open Source Policy (automatic compliance)

### Allowed Licenses

Only the following licenses are allowed for new packages:

- MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
- See full list: output/policy/license-allowlist.md

### Prohibited Licenses

The following licenses cannot be added without prior approval:

- GPL-2.0, GPL-3.0, AGPL-3.0 (Copyleft - Source code disclosure obligation)
- LGPL-2.0, LGPL-2.1, LGPL-3.0 (Weak Copyleft - dynamic linking review required)
- CC-BY-SA (not suitable for software)
- all licenses with non-commercial use restrictions

### vulnerability policy

- CVSS 7.0 or later(High/Critical) packages with these vulnerabilities are prohibited
- Upgrade versions with known vulnerabilities to patched versions

### Checks when adding packages

When adding a new package, follow this sequence:

1. License check: `license-checker` or `/oss-policy-check` skill run
2. vulnerability check: OSV API or `grype` run
3. Allowlist comparison: output/policy/license-allowlist.md compare
4. On violation: request usage approval from the Program Manager (output/process/usage-approval.md refer to)
```

**effect:** When Claude Code helps you add packages, it automatically references this policy to alert you.

**margin:** If the developer directly executes `npm install` in the terminal, Claude Code will not be able to intervene.

---

→ next: [Method 2:Define Skill](./method2-skill.md)
