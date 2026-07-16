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
# Project Guide

(existing project guidance content)

---

## Open Source Policy

### License Management

**Allowed Licenses**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**Review Required Licenses** (legal review required): LGPL, MPL

**Prohibited Licenses** (cannot be used without prior approval): GPL, AGPL, SSPL, Commons Clause

<!-- Copy the full rules (including the Security, SBOM, and Copyright sections) from the Common Rules Template -->

---
```

Copy the full text from the [Common Rules Template](../rules-template). When the allow/deny lists change, update only the canonical template and paste it into each tool file again.

## Verifying the Rules Are Applied

To check whether the rules are applied, ask the tool.

"Can I add a GPL-3.0 licensed package to this project?"

If the rules are recognized, the tool answers that it is a prohibited license and suggests an alternative. If it does not recognize the rules, re-check the configuration file location and how to apply the rules. For linkage to the standard requirements, see [ISO Standards Linkage](../iso-mapping).

## Notes

:::warning Limits of AI rules
Because `CLAUDE.md` consumes prompt tokens, overly long content reduces context efficiency. Also, Claude Code treats rules as guidance and does not hard-block policy-violating code. If practical blocking is required, it must be paired with a CI/CD pipeline. The pipeline should serve as the real gatekeeper, while `CLAUDE.md` supports AI in generating code in the right direction.
:::
