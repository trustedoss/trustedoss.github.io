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
- `AGENTS.md` (supported at the root and nested in subdirectories — a common-rules-file alternative)

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
When `alwaysApply: true` is set, rules apply to all files and token usage may increase. For policies that must always apply, use `alwaysApply: true`; for rules needed only for specific languages or folders, limit scope with `globs` for efficiency. If both `.cursorrules` (legacy) and `.cursor/rules/` are used, `.cursor/rules/` takes precedence, so `.cursor/rules/` is recommended for new projects.
:::
