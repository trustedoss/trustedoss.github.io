---
id: copilot
title: GitHub Copilot
sidebar_label: GitHub Copilot
description: Explains the scope of the .github/copilot-instructions.md file read by GitHub Copilot, an example open source policy, and how to verify it is applied.
sidebar_position: 3
---

# GitHub Copilot

## Overview

GitHub Copilot reads `.github/copilot-instructions.md` as custom instructions applied across the entire repository. It applies consistently in all environments where Copilot is enabled, such as VS Code, JetBrains, and GitHub.com. The scope is repository-level.

If open source policy is written in this file, Copilot automatically recognizes license and security policy while suggesting code, regardless of which editor team members use. Since most repositories already have a `.github/` directory, it can be applied immediately without creating additional directories. It is recommended to copy a base template including this file whenever creating a new repository.

## Configuration File Location

- `.github/copilot-instructions.md`: single file, applied to the whole repository
- `.github/instructions/*.instructions.md`: path-scoped via the `applyTo` frontmatter pattern (good for per-language or per-folder rules)
- `AGENTS.md`: common rules file. It can sit in any folder of the repository, and the file nearest to the working location wins

## How to Apply

1. If `.github/` does not exist, create it and add `copilot-instructions.md`.
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

Copilot runs in three different places, each with a different level of isolation. The cloud agent reads issue bodies and pull request descriptions verbatim, so instructions planted there can turn into command execution and outbound traffic, while the local tools run directly on the developer's machine. The broader threat model is covered in [Agent & MCP Tool Governance](../agent-governance).

### Cloud agent

The Copilot cloud agent runs in an ephemeral GitHub Actions environment. Its firewall is on by default, and the recommended allowlist is applied by default as well. The settings live under `Settings > Code, planning, and automation > Copilot > Internet access` for the organization or the repository.

| Setting                       | Role                                                             |
| ----------------------------- | ---------------------------------------------------------------- |
| Enable firewall               | Whether the firewall is used; the org default defers to the repo |
| Recommended allowlist         | The default set of allowed domains provided by GitHub            |
| Allow repository custom rules | Whether a repository may add its own allow rules                 |
| Custom allowlist              | Additional allowed domains set by the organization or repository |

Note the limit: this firewall applies only to processes started by the Bash tool, not to MCP servers or setup steps.

### Copilot CLI

Local sandboxing became generally available on 2026-10-07. Turn it on in a session with `/sandbox enable`, or start with `--sandbox` (`--no-sandbox` to turn it off); to keep it on, set `sandbox.enabled` in `~/.copilot/settings.json`. Organizations can require sandboxing through enterprise-managed settings. The isolation is at the process and filesystem level, not a virtual machine or a container. macOS uses Seatbelt, Linux uses bubblewrap 0.5.0 or later with slirp4netns, and Windows works on Windows 11 25H2 (KB5124010 or later) or 26H1.

Tool approvals are set with the `--allow-tool` and `--deny-tool` flags. Approved tools and paths are stored in `~/.copilot/permissions-config.json`, and allowed URLs in `allowedUrls` in `~/.copilot/settings.json`. `--allow-all-tools` and `--yolo` skip every approval, so do not use them outside an isolated environment.

### VS Code agent mode

Terminal command auto-approval is enabled with `chat.tools.terminal.enableAutoApprove`, and the target commands are listed in `chat.tools.terminal.autoApprove`. Auto-approval across tools is `chat.tools.global.autoApprove` (it replaced `chat.tools.autoApprove` in 1.104, with no automatic migration).

The sandbox is turned on with `chat.agent.sandbox.enabled`. It supports macOS, Linux, and WSL2, and Windows 11 as an experimental feature. Network access is adjusted with `chat.agent.sandbox.network.allowNetwork` (formerly `chat.agent.sandbox.allowNetwork`), `network.allowedDomains` and `network.deniedDomains`, and the filesystem with `chat.agent.sandbox.fileSystem.userConfiguredPaths` (`fileSystem.mac` and `fileSystem.linux` are deprecated). Watch two defaults: `network.allowNetwork` defaults to `true`, so the network is open, and `allowUnsandboxedCommands` also defaults to `true`, so commands can run outside the sandbox. Set both to `false` if your policy requires it.

## Notes

:::info Good to know
Organization settings support organization-wide custom instructions. Their scope is limited to Copilot Chat, code review, and the coding agent on GitHub.com, so to stay consistent across IDEs, also manage per-repository instruction files from a shared template. Custom instructions apply to Chat, code review, and the coding agent; application to inline code completion is not guaranteed. There may be a short delay after changes.
:::
