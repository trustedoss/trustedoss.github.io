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

## Isolation and Sandboxing

### Why it matters

Rules files steer the direction in which the agent writes code, but they do not limit what the agent is able to do. By default, Claude Code runs file tools, MCP servers, and hooks directly on the host. If an attacker plants instructions in content the agent reads (an issue, a web page, a code comment), that indirect prompt injection can rewrite the hook configuration in `.claude/settings.json` or `.mcp.json` so that it runs automatically from the next session onward. The broader threat model is covered in [Agent & MCP Tool Governance](../agent-governance).

### Choosing an isolation scope

Isolation is opt-in. If you do not turn it on, nothing is restricted.

| Approach                        | Isolation scope                                                | Requirement    |
| ------------------------------- | -------------------------------------------------------------- | -------------- |
| Sandboxed Bash tool (built in)  | Bash commands and their child processes                        | None           |
| Sandbox runtime                 | The whole Claude Code process (file tools, MCP servers, hooks) | Node           |
| Dev container, custom container | The whole development environment                              | Docker         |
| Virtual machine                 | The whole operating system                                     | Virtualization |
| Claude Code on the web          | The whole operating system (operated by Anthropic)             | None           |

The built-in sandboxed Bash tool restricts Bash commands only. MCP servers and hooks are separate processes and still run unconstrained on the host. To isolate MCP servers and hooks as well, one of the other four approaches must put the entire Claude Code process inside the isolation boundary.

The sandbox runtime is a beta research preview. Run it with `npx @anthropic-ai/sandbox-runtime claude`; it denies writes to the project's `.git/hooks`, `.mcp.json`, `.claude/commands`, `.claude/agents`, and shell startup files by default.

### How to turn it on

Running `/sandbox` in a session opens a panel for choosing the mode and its exceptions, and the choices are saved to `.claude/settings.local.json`. To apply it to every project, write it directly in `~/.claude/settings.json`.

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": {"allowWrite": ["~/.kube", "/tmp/build"]},
    "network": {"allowedDomains": ["github.com", "*.npmjs.org"]}
  }
}
```

No domains are pre-allowed by default. A domain that is not on the list triggers an approval prompt, and turning on `sandbox.network.strictAllowlist` denies it without prompting. macOS uses the built-in Seatbelt; Linux and WSL2 need `bubblewrap` and `socat`. Native Windows is not supported, so run it under WSL2. If the sandbox fails to start, the default behavior is to warn and keep running without it, so set `sandbox.failIfUnavailable` to `true` to stop instead.

To enforce this organization-wide, put the same keys in managed settings (`managed-settings.json`). Individual settings cannot override them.

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  }
}
```

### Blocking writes to configuration paths only

Before adopting full isolation, permission rules can at least block tampering with configuration files. Rules are evaluated in the order deny, ask, allow, and the first match decides the outcome, so a path placed in deny cannot be revived by an allow rule.

```json
{
  "permissions": {
    "deny": [
      "Edit(./.claude/**)",
      "Edit(./.mcp.json)",
      "Edit(./.git/hooks/**)"
    ]
  }
}
```

Path rules are checked against the `Edit` and `Read` matchers only. Writing the same path as `Write(...)` registers the rule but it is never consulted, and Claude Code only warns at startup.

## Notes

:::warning Limits of AI rules
Because `CLAUDE.md` consumes prompt tokens, overly long content reduces context efficiency. Also, Claude Code treats rules as guidance and does not hard-block policy-violating code. If practical blocking is required, it must be paired with a CI/CD pipeline. The pipeline should serve as the real gatekeeper, while `CLAUDE.md` supports AI in generating code in the right direction.
:::
