---
id: windsurf
title: Windsurf
sidebar_label: Windsurf
sidebar_position: 4
---

# Windsurf

## Overview

Windsurf reads `.windsurfrules` in the project root and uses it as behavior instructions for the Cascade AI agent. Global rules can be configured separately in the Windsurf app settings (UI). The scope is project-level, and global and project settings can be used together.

It is efficient to manage rules in layers: put organization-wide policy in Global Rules and project-specific exceptions or additional rules in `.windsurfrules`. Committing `.windsurfrules` to the repository applies the same policy across the team. If global and project rules conflict, project rules take precedence.

## Configuration File Location

- Project: `.windsurfrules` (root, recommended)
- Global: Windsurf app settings > Global Rules

## How to Apply

1. Create `.windsurfrules` in the project root.
2. Paste content from the [Common Rules Template](../rules-template).
3. Update the allow/deny license list to match internal policy.

## Configuration Example

```markdown
## Open Source Policy

### License Management

When adding new external packages/libraries, always verify and document the license.

**Allowed Licenses**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**Review Required Licenses** (legal review required): LGPL, MPL

**Prohibited Licenses** (cannot be used without prior approval): GPL, AGPL, SSPL, Commons Clause

### Security Management

- Do not use package versions with known CVEs
- After adding dependencies, run one of the following commands:
  - npm: `npm audit`
  - Python: `pip-audit`
  - Container/General: `trivy fs .`
- Use the latest stable package version whenever possible

### SBOM Management

- SBOM update required when dependencies change
- Generation tools: cdxgen, syft, trivy
- Recommended format: CycloneDX (alternative: SPDX)

### Copyright

- Keep existing code copyright headers
- Include project license header when creating new files
- When copying code from another project, include source and license
```

## Notes

:::info Good to know
`.windsurfrules` is only for the Cascade agent and does not apply to standard code completion (Autocomplete). Keep in mind that policy applies only to agent actions (file creation/modification, package additions, etc.), and extra caution is needed when using plain completion. Larger files can increase response latency, so keep only essential team policies concise from the full template.
:::
