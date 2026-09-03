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

<!-- Copy the allowed / review-required / prohibited license lists and the rest of the rules from the Common Rules Template -->
```

Copy the full text from the [Common Rules Template](../rules-template). When the allow/deny lists change, update only the canonical template and paste it into each tool file again.

## Verifying the Rules Are Applied

To check whether the rules are applied, ask the tool.

"Can I add a GPL-3.0 licensed package to this project?"

If the rules are recognized, the tool answers that it is a prohibited license and suggests an alternative. If it does not recognize the rules, re-check the configuration file location and how to apply the rules. For linkage to the standard requirements, see [ISO Standards Linkage](../iso-mapping).

## Isolation and Sandboxing

### Why it matters

Rules files steer what code the agent writes, but they do not limit which commands it can run or which paths it can reach. If an attacker plants instructions in an issue or a document the agent reads (indirect prompt injection), those instructions can turn into terminal command execution. The broader threat model is covered in [Agent & MCP Tool Governance](../agent-governance).

### Two separate layers

Cursor's controls come in two layers: execution approval and the sandbox.

- Execution approval (Run Mode): choose one of Auto-review, Allowlist, or Run Everything. Allowlist auto-runs only the commands registered in advance.
- Sandbox: operating-system-level isolation layered on top of approval. macOS uses Seatbelt (`sandbox-exec`); Linux restricts the filesystem with Landlock and blocks risky syscalls with seccomp. Linux requires kernel 6.2 or later, Landlock v3, and unprivileged user namespaces; when those are unavailable it falls back to asking for approval before each command. On Windows, the Linux sandbox runs inside WSL2.

### How to turn it on

Set the Run Mode and the sandbox under `Settings > Agents > Approvals & Execution`. The sandbox network policy has three options: `sandbox.json Only` allows only the list you write, the default `sandbox.json + Defaults` also applies the built-in allowlist (about 110 domains), and `Allow All` applies no restriction. The default policy is deny, so domains outside the list are blocked.

The settings are also backed by files. `~/.cursor/permissions.json` holds the command and MCP server allowlists (`terminalAllowlist`, `mcpAllowlist`, `autoRun`), and `~/.cursor/sandbox.json` holds the sandbox type and network policy (`networkPolicy`, `additionalReadwritePaths`). Organization policy is enforced through Auto Run Configuration and the Cloud Agent's Lock Network Access Policy in the Enterprise dashboard, and team admin settings take precedence over a user's `permissions.json` and editor settings.

To block specific commands with certainty, use the `beforeShellExecution` hook in `.cursor/hooks.json`. When the hook returns exit code 2, the command does not run.

## Notes

:::info Good to know
When `alwaysApply: true` is set, rules apply to all files and token usage may increase. For policies that must always apply, use `alwaysApply: true`; for rules needed only for specific languages or folders, limit scope with `globs` for efficiency. If both `.cursorrules` (legacy) and `.cursor/rules/` are used, `.cursor/rules/` takes precedence, so `.cursor/rules/` is recommended for new projects.
:::
