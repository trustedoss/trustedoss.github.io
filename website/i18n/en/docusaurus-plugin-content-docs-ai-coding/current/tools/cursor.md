---
id: cursor
title: Cursor
sidebar_label: Cursor
sidebar_position: 2
---

# Cursor

## Overview

Cursor recognizes `.mdc` files under `.cursor/rules/` as rules and applies them to AI behavior. You can set scope (glob patterns) per file, so rules can be split and managed by language or folder. The scope is project-level.

If the open source policy is separated into `.cursor/rules/oss-policy.mdc`, it can be managed independently from other development guidelines and disabled easily when needed. Limiting target files with `globs` reduces unnecessary context usage. Committing it to the repository automatically applies the same policy across the team. If there are multiple rule files, clear purpose-based filenames make maintenance easier.

## Configuration File Location

- `.cursor/rules/oss-policy.mdc` (recommended)
- `.cursorrules` (single root file, legacy)

## How to Apply

1. Create `.cursor/rules/oss-policy.mdc`.
2. Paste content from the [Common Rules Template](../rules-template).
3. Update the allow/deny license list to match internal policy.

## Configuration Example

```markdown
---
description: Open source license and security policy
globs: ['**/*.{js,ts,py,go,java}']
alwaysApply: true
---

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
When `alwaysApply: true` is set, rules apply to all files and token usage may increase. For policies that must always apply, use `alwaysApply: true`; for rules needed only for specific languages or folders, limit scope with `globs` for efficiency. If both `.cursorrules` (legacy) and `.cursor/rules/` are used, `.cursor/rules/` takes precedence, so `.cursor/rules/` is recommended for new projects.
:::
