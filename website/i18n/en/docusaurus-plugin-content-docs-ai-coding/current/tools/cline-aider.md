---
id: cline-aider
title: Cline / Aider Setup
sidebar_label: Cline / Aider
sidebar_position: 6
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

<!-- Copy the allowed / review-required / prohibited license lists and the rest of the rules from the Common Rules Template -->
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

<!-- Copy the allowed / review-required / prohibited license lists and the rest of the rules from the Common Rules Template -->
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

## Isolation and Sandboxing

### Why it matters

Both tools run directly on the developer's machine and provide no operating-system-level isolation. If instructions are planted in an issue or a document the agent reads (indirect prompt injection), they can turn directly into command execution, and human approval is the only thing standing in the way. If you use these tools, run them inside a container or a virtual machine and grant credentials and write access only within it. The broader threat model is covered in [Agent & MCP Tool Governance](../agent-governance).

### Cline

Cline's control is human approval. The official documentation states that it offers a human-in-the-loop interface rather than a separate sandbox. Auto-approve is split into reading and editing files, running commands, using the browser, and using MCP servers, so turn on only what is needed. YOLO mode, which disables every safety check, should not be used outside an isolated environment.

Per-command allow and deny lists are set as JSON in the `CLINE_COMMAND_PERMISSIONS` environment variable (`allow`, `deny`, `allowRedirects`). There is no matching entry in the editor settings file.

### Aider

Aider has no sandbox option. The confirmation prompt shown before each shell command is the only line of defense, so use `--yes-always`, which skips it, only inside an isolated environment. `.aider.conf.yml` has no entry corresponding to a per-command allow or deny list either.

An official Docker image (`paulgauthier/aider`) exists, but the documentation presents it as an installation method rather than a security boundary. To use it for isolation, restrict the mounted paths and network access yourself.

## Notes

:::info Good to know
Both Cline and Aider treat rules as soft guidance rather than hard blocking. To fully block policy-violating packages, configure a CI/CD pipeline in parallel. Since Aider is CLI-based, if `.aider.conf.yml` does not exist, you can point to the policy document directly on each run with `aider --read CONVENTIONS.md`. For automated CI/CD gate setup, refer to [Quick CI/CD](../cicd-quick).
:::
