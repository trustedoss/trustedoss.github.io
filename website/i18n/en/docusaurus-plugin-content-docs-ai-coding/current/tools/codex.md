---
id: codex
title: OpenAI Codex
sidebar_label: OpenAI Codex
sidebar_position: 4
---

# OpenAI Codex

## Overview

Codex reads `AGENTS.md` as its instruction file. It reads the global file (`~/.codex/AGENTS.md`) first, then concatenates the file at each level from the Git repository root down to the current working directory. Files closer to the current directory appear later, so they override earlier guidance. If `AGENTS.override.md` exists in the same location, it takes precedence over `AGENTS.md`.

`AGENTS.md` is a shared format that Cursor, GitHub Copilot, Devin Desktop, and Cline also support. Keeping the open source policy in a single `AGENTS.md` applies the same rules across several tools and leaves only the differences in tool-specific files.

## Configuration File Location

- `AGENTS.md` (project root, recommended)
- `{subdirectory}/AGENTS.md` (additionally applied when working in that directory)
- `AGENTS.override.md` (takes precedence over `AGENTS.md` in the same location)
- `~/.codex/AGENTS.md` (global; read first, so it has the lowest precedence)

In `~/.codex/config.toml`, `project_doc_fallback_filenames` adds file names to look for when `AGENTS.md` is absent, and `project_doc_max_bytes` sets the maximum size that is read.

## How to Apply

1. Create `AGENTS.md` in the project root, or open the existing file.
2. Paste content from the [Common Rules Template](../rules-template).
3. Update the allow/deny license list to match internal policy.

## Configuration Example

```markdown
## Open Source Policy

### License Management

<!-- Copy the allowed / review-required / prohibited license lists and the rest of the rules from the Common Rules Template -->
```

Copy the full text from the [Common Rules Template](../rules-template). When the allow/deny lists change, update only the canonical template and paste it into each tool file again.

## Verifying the Rules Are Applied

To check whether the rules are applied, ask the tool.

"Can I add a GPL-3.0 licensed package to this project?"

If the rules are recognized, the tool answers that it is a prohibited license and suggests an alternative. If it does not recognize the rules, re-check the configuration file location and how to apply the rules. For linkage to the standard requirements, see [ISO Standards Linkage](../iso-mapping).

## Isolation and Sandboxing

### Why it matters

Codex runs terminal commands directly, so instructions planted in content the agent reads (indirect prompt injection) can turn into command execution. Rules files cannot close that path. Codex separates the execution scope, set by `sandbox_mode`, from the point at which a human steps in, set by `approval_policy`. The broader threat model is covered in [Agent & MCP Tool Governance](../agent-governance).

### How to turn it on

Set both values in `~/.codex/config.toml`.

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = false
writable_roots = ["/tmp/build"]
```

`sandbox_mode` has three values. `read-only` allows reads only, `workspace-write` allows writes to the workspace and the paths listed in `writable_roots`, and `danger-full-access` applies no restriction. Setting `network_access` to `false` blocks outbound traffic inside the sandbox.

`approval_policy` takes `untrusted`, `on-request`, or `never`. The older `on-failure` value is deprecated. Use `on-request` for interactive runs. Non-interactive runs have nobody to ask, so they end up on `never`, and in that case the sandbox is the only line of defense, so lower `sandbox_mode` at the same time.

For a one-off change, use the `--sandbox workspace-write` and `--ask-for-approval on-request` flags.

The implementation differs per operating system. macOS uses the built-in Seatbelt, while Linux and WSL2 use `bubblewrap`. On Windows, running from PowerShell uses Windows Sandbox and running under WSL2 uses the Linux implementation.

### Enforcing it on managed devices

A requirements file distributed by the organization takes precedence over user settings. The path is `/etc/codex/requirements.toml` on Unix-like systems and `%ProgramData%\OpenAI\Codex\requirements.toml` on Windows. `allowed_sandbox_modes` limits which sandbox levels are permitted and `allowed_approval_policies` limits which approval policies are permitted; MCP server allowlists and plugin sources can be locked as well. When a user setting conflicts with the requirements, Codex falls back to a compatible value and notifies the user.

## Notes

:::info Good to know
Because `AGENTS.md` is concatenated, a file in a subdirectory can override guidance from above. If organization-wide policy must hold, enforce it through the requirements file above rather than a global `AGENTS.md`. Rules files are not a hard block, so pair them with a CI/CD gate; see [Quick CI/CD](../cicd-quick) for setup. The official documentation has moved to learn.chatgpt.com/docs (confirmed 2026-08).
:::
