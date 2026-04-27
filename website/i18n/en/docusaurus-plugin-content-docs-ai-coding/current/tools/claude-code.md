---
id: claude-code
title: Claude Code
sidebar_label: Claude Code
sidebar_position: 1
---

# Claude Code

## Overview

Claude Code automatically reads `CLAUDE.md` in the project root at session start and uses it as context for all work. You can also place `CLAUDE.md` in subfolders, and it is additionally loaded when working in those folders. The scope is project-level, and global settings are also possible through `~/.claude/CLAUDE.md`.

If open source policies are written in `CLAUDE.md`, Claude Code automatically considers license and security policies when adding new packages or generating code, even without explicit developer prompts. If the team uses the same repository, committing `CLAUDE.md` applies consistent policy to all team members.

## Configuration File Location

- Project root: `CLAUDE.md` (recommended)
- Per subfolder: `{folder_name}/CLAUDE.md` (supplementary)
- Global: `~/.claude/CLAUDE.md` (shared across all projects)

## How to Apply

1. Create `CLAUDE.md` in the project root, or open the existing file.
2. Paste content from the [Common Rules Template](../rules-template).
3. Update the allow/deny license list to match internal policy.

## Configuration Example

```markdown
# project Guides

(existing project guidance content)

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

---
```

## Notes

:::warning Limits of AI rules
Because `CLAUDE.md` consumes prompt tokens, overly long content reduces context efficiency. Also, Claude Code treats rules as guidance and does not hard-block policy-violating code. If practical blocking is required, it must be paired with a CI/CD pipeline. The pipeline should serve as the real gatekeeper, while `CLAUDE.md` supports AI in generating code in the right direction.
:::
