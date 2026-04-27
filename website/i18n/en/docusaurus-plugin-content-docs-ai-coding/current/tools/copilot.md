---
id: copilot
title: GitHub Copilot
sidebar_label: GitHub Copilot
sidebar_position: 3
---

# GitHub Copilot

## Overview

GitHub Copilot reads `.github/copilot-instructions.md` as custom instructions applied across the entire repository. It applies consistently in all environments where Copilot is enabled, such as VS Code, JetBrains, and GitHub.com. The scope is repository-level.

If open source policy is written in this file, Copilot automatically recognizes license and security policy while suggesting code, regardless of which editor team members use. Since most repositories already have a `.github/` directory, it can be applied immediately without creating additional directories. It is recommended to copy a base template including this file whenever creating a new repository.

## Configuration File Location

- `.github/copilot-instructions.md` (single file, applied to whole repository)

## How to Apply

1. If `.github/` does not exist, create it and add `copilot-instructions.md`.
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
Common instructions at the organization level are not supported separately, so `.github/copilot-instructions.md` must be copied into each repository. If you manage multiple repositories, maintain this file as a shared template and sync updates across all repositories to prevent policy drift. It applies to both Copilot Chat and code completion, though there may be a short delay after changes.
:::
