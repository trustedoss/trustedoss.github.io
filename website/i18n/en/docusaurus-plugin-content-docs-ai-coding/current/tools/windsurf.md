---
id: windsurf
title: Windsurf
sidebar_label: Windsurf
sidebar_position: 4
---

# Windsurf

## Overview

Windsurf reads workspace rules from the `.windsurf/rules/` directory (the legacy single-file `.windsurfrules` is still recognized) and uses them as behavior instructions for the Cascade AI agent. Global rules can be configured separately in the Windsurf app settings (UI). The scope is project-level, and global and project settings can be used together.

It is efficient to manage rules in layers: put organization-wide policy in Global Rules and project-specific exceptions or additional rules in `.windsurf/rules/`. Committing the rules directory to the repository applies the same policy across the team. If global and project rules conflict, project rules take precedence.

## Configuration File Location

- Project: `.windsurf/rules/` directory (recommended — 12,000-character limit per file; the legacy single-file `.windsurfrules` is still recognized). `AGENTS.md` is also supported
- Global: `~/.codeium/windsurf/memories/global_rules.md` (6,000-character limit)

## How to Apply

1. Create `.windsurf/rules/oss-policy.md` in the project.
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
Windsurf has been merging into Devin Desktop since Cognition (the maker of Devin) acquired it in 2025, and the official docs moved to docs.devin.ai. Newer docs recommend the `.devin/rules/` directory first, so check for rule-path changes when the tool updates. Larger rule files can increase response latency (12,000-character limit per file), so trim the full template down to only the essential team policies.
:::
