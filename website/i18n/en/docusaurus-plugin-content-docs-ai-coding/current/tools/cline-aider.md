---
id: cline-aider
title: Cline / Aider Setup
sidebar_label: Cline / Aider
sidebar_position: 5
---

# Cline / Aider Setup

## Overview

Cline reads `.clinerules` files (a single root file or `.clinerules/` folder) as project instructions and applies them to AI behavior. Aider includes a policy document (conventionally `CONVENTIONS.md`) in every session's context via the `--read` option or the `read` field in `.aider.conf.yml`. Both tools apply rules at the project level.

Cline is an agent-style AI tool running as a VS Code extension, while Aider is a terminal-based CLI tool. Both are open source and run locally, so they are often preferred by teams that avoid sending code to external servers. If open source policy is written in each configuration file, AI automatically considers it when adding packages or generating code.

---

## Cline Setup

### Configuration File Location

- `.clinerules` (single root file, recommended)
- `.clinerules/` (folder, allows split files)

### How to Apply

1. Create `.clinerules` in the project root.
2. Paste content from the [Common Rules Template](../rules-template).
3. Update the allow/deny license list to match internal policy.

### Configuration Example

```markdown
## Open Source Policy

### License Management

**Allowed Licenses**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**Review Required Licenses** (legal review required): LGPL, MPL

**Prohibited Licenses** (cannot be used without prior approval): GPL, AGPL, SSPL, Commons Clause

<!-- Copy the full rules (including the Security, SBOM, and Copyright sections) from the Common Rules Template -->
```

Copy the full text from the [Common Rules Template](../rules-template). When the allow/deny lists change, update only the canonical template and paste it into each tool file again.

---

## Aider Setup

### Configuration File Location

- `CONVENTIONS.md` (root; the file name is free — this is the convention in Aider's official docs)
- `read` field in `.aider.conf.yml` (registers the file so it loads automatically)

### How to Apply

1. Create `CONVENTIONS.md` in the project root.
2. Paste content from the [Common Rules Template](../rules-template).
3. Add `read: CONVENTIONS.md` to `.aider.conf.yml` so it loads on every run.
   (For a one-off run, use `aider --read CONVENTIONS.md`.)

### Configuration Example

**CONVENTIONS.md** — This file holds the Common Rules Template content. Below is an excerpt.

```markdown
## Open Source Policy

### License Management

**Allowed Licenses**: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC

**Review Required Licenses** (legal review required): LGPL, MPL

**Prohibited Licenses** (cannot be used without prior approval): GPL, AGPL, SSPL, Commons Clause

<!-- Copy the full rules (including the Security, SBOM, and Copyright sections) from the Common Rules Template -->
```

Copy the full text from the [Common Rules Template](../rules-template). When the allow/deny lists change, update only the canonical template and paste it into each tool file again.

**.aider.conf.yml** — Always loads the policy document as read-only context.

```yaml
# Load the policy document as read-only context at session start
read: CONVENTIONS.md
```

---

## Verifying the Rules Are Applied

To check whether the rules are applied, ask the tool.

"Can I add a GPL-3.0 licensed package to this project?"

If the rules are recognized, the tool answers that it is a prohibited license and suggests an alternative. If it does not recognize the rules, re-check the configuration file location and how to apply the rules. For linkage to the standard requirements, see [ISO Standards Linkage](../iso-mapping).

## Notes

:::info Good to know
Both Cline and Aider treat rules as soft guidance rather than hard blocking. To fully block policy-violating packages, configure a CI/CD pipeline in parallel. Since Aider is CLI-based, if `.aider.conf.yml` does not exist, you can point to the policy document directly on each run with `aider --read CONVENTIONS.md`. For automated CI/CD gate setup, refer to [Quick CI/CD](../cicd-quick).
:::
