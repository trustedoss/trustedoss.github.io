---
id: windsurf
title: Devin Desktop (formerly Windsurf)
sidebar_label: Devin Desktop
sidebar_position: 4
---

# Devin Desktop (formerly Windsurf)

## Overview

Windsurf was renamed Devin Desktop on 2026-06-02. The IDE and its features are unchanged; the brand was unified under Devin. The coding agent also changed from Cascade to Devin Local (Cascade remained available only through 2026-07).

Rules files live at the project level, and global rules are configured separately in the app settings (UI). It is efficient to manage rules in layers: put organization-wide policy in Global Rules and project-specific exceptions or additional rules in the project rules directory. Committing the rules directory to the repository applies the same policy across the team. If global and project rules conflict, project rules take precedence.

## Configuration File Location

- Project (recommended): `.devin/rules/` directory — the new standard path, which takes precedence over the others
- Project (backward compatible): `.windsurf/rules/` directory and the legacy single-file `.windsurfrules`. Existing setups keep working as-is
- Common format: `AGENTS.md` is supported, and `.cursor/rules` can be imported
- Global: Global Rules in the app settings

There is a 12,000-character limit per file.

## How to Apply

1. Create `.devin/rules/oss-policy.md` in the project.
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
Following Cognition's (the maker of Devin) 2025 acquisition, the rebrand to Devin Desktop completed on 2026-06-02, and the official docs moved to docs.devin.ai. Existing `.windsurf/rules/` and `.windsurfrules` are still recognized, so there is no need to migrate immediately, but use `.devin/rules/` for anything new. Larger rule files can increase response latency (12,000-character limit per file), so trim the full template down to only the essential team policies.
:::
