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

- `.github/copilot-instructions.md` — single file, applied to the whole repository
- `.github/instructions/*.instructions.md` — path-scoped via the `applyTo` frontmatter pattern (good for per-language or per-folder rules)
- `AGENTS.md` — common rules file at the root (nearest file wins)

## How to Apply

1. If `.github/` does not exist, create it and add `copilot-instructions.md`.
2. Paste content from the [Common Rules Template](../rules-template).
3. Update the allow/deny license list to match internal policy.

## Configuration Example

```markdown
## Open Source Policy

### License Management

**Allowed Licenses**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**Review Required Licenses** (legal review required): LGPL, MPL

**Prohibited Licenses** (cannot be used without prior approval): GPL, AGPL, SSPL, Commons Clause

<!-- Copy the full rules (including the Security, SBOM, and Copyright sections) from the Common Rules Template -->
```

Copy the full text from the [Common Rules Template](../rules-template). When the allow/deny lists change, update only the canonical template and paste it into each tool file again.

## Verifying the Rules Are Applied

To check whether the rules are applied, ask the tool.

"Can I add a GPL-3.0 licensed package to this project?"

If the rules are recognized, the tool answers that it is a prohibited license and suggests an alternative. If it does not recognize the rules, re-check the configuration file location and how to apply the rules. For linkage to the standard requirements, see [ISO Standards Linkage](../iso-mapping).

## Notes

:::info Good to know
Organization settings support organization-wide custom instructions. Their scope is limited to Copilot Chat, code review, and the coding agent on GitHub.com, so to stay consistent across IDEs, also manage per-repository instruction files from a shared template. Custom instructions apply to Chat, code review, and the coding agent; application to inline code completion is not guaranteed. There may be a short delay after changes.
:::
