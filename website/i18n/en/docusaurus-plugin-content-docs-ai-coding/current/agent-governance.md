---
id: agent-governance
title: 'Agent and MCP Tool Governance'
sidebar_label: 'Agent & MCP Tool Governance'
---

# Agent and MCP Tool Governance

Rules (stage 2) govern **what the AI writes** and CI gates (stage 3) govern **the artifact**. This
page covers the remaining plane: **which tools the agent calls and which inputs it reads**. In a
development environment where agents chain external tools over MCP (Model Context Protocol), the
tools and prompts themselves become supply chain inputs.

## 1. Why this matters

- **Tool descriptions are instructions.** An MCP tool's description (metadata) enters the agent's
  context, so a description with hidden malicious instructions (tool poisoning) is as effective as
  changing the system prompt. A study of 1,899 open-source MCP servers found 5.5% exhibiting
  MCP-specific tool poisoning.
- **Planted prompts can steer the build.** If an attacker plants instructions where the agent will
  read them (issues, web pages, code comments), the generated code and pulled-in packages can
  change (indirect prompt injection, OWASP LLM01:2025).
- **Agent-accepted dependencies bypass human threat models.** Packages the AI suggests and the
  agent installs enter the supply chain without review.

The MCP specification itself states that tool descriptions should be considered untrusted unless
obtained from a trusted server and requires explicit user consent — while noting the protocol
cannot enforce these principles, leaving them to implementers (adopting organizations).

## 2. Threat model: three planes and their defenses

| Plane               | Threat                                                                      | Defense                                                                      |
| ------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Input (prompts)     | Indirect prompt injection — instructions planted in content the agent reads | Minimize untrusted content access, human approval for high-risk actions      |
| Tools (MCP servers) | Tool poisoning, tool shadowing, chained tool calls                          | Server allowlist, pre-adoption scanning, description review, version pinning |
| Artifact (code)     | Tainted generated code, vulnerable or forbidden-license dependencies        | Existing CI hard blocks (secrets, SAST, SCA) — the last line of defense      |

The point is that the three planes are complementary: if input and tool controls are bypassed, the
artifact gate remains, and behavior that never lands in code (data exfiltration through a tool) is
caught by tool controls, not the CI gate.

## 3. Five working controls

Translating the Microsoft Incident Response guidance (2026-06) and the MCP spec's security
principles into working rules:

1. **MCP server allowlist** — use only approved servers and disable "allow all"-style settings.
   New servers pass the scanning in section 4 before registration.
2. **Least privilege** — limit the agent's file, network, and command-execution scope to what is
   needed.
3. **Description review** — tool descriptions from untrusted sources are review targets, both at
   adoption and on updates (descriptions can change when a server updates).
4. **Version pinning** — pin agents and MCP servers like any dependency and track changes.
5. **Human approval and audit logs for high-risk actions** — never auto-approve file deletion,
   external transmission, or deployment, and keep tool-call history.

## 4. Automation tools

| Control point             | Main                               | Alternative                                            |
| ------------------------- | ---------------------------------- | ------------------------------------------------------ |
| Pre-adoption scanning     | Snyk agent-scan (Apache-2.0)       | Cisco mcp-scanner (Apache-2.0)                         |
| Centralized operation     | ToolHive (Stacklok, Apache-2.0)    | MCP Gateway & Registry (agentic-community, Apache-2.0) |
| Developer-endpoint policy | Tool built-in controls (section 5) | —                                                      |

**Pre-adoption scanning — Snyk agent-scan**: detects prompt injection, tool poisoning, and tool
shadowing in MCP servers, agent configurations, and agent skills (the successor of Invariant Labs
mcp-scan). Note that it requires a Snyk API token and actually executes MCP servers during the
scan (run it in an isolated environment).

```bash
# Example: scan the VS Code MCP configuration (SNYK_TOKEN required)
uvx snyk-agent-scan@latest ~/.vscode/mcp.json
```

The alternative, Cisco mcp-scanner, combines three engines: YARA rules, LLM-as-a-judge, and the
Cisco AI Defense API.

```bash
uv tool install --python 3.13 cisco-ai-mcp-scanner
mcp-scanner --scan-known-configs --analyzers yara --format summary
```

**Centralized operation — ToolHive**: builds a trusted catalog of approved MCP servers with access
policies, OIDC/OAuth authentication, isolated container execution (Docker/Podman, a Kubernetes
Operator), and OpenTelemetry-based auditing. Adopt it when the allowlist should be managed by a
platform rather than by hand. If you need large-scale IdP integration (Keycloak, Entra ID, etc.),
consider MCP Gateway & Registry.

## 5. Copy-paste asset: a Claude Code organization policy

Claude Code enforces organization-deployed managed settings (`managed-settings.json` — macOS
`/Library/Application Support/ClaudeCode/`, Linux `/etc/claude-code/`) that individuals cannot
override. The following is a starting point for an MCP allowlist and least privilege (per the
current official docs).

```json
{
  "allowedMcpServers": [
    {"serverName": "github"},
    {"serverName": "sentry"}
  ],
  "allowManagedMcpServersOnly": true,
  "permissions": {
    "deny": ["Bash(curl:*)", "Read(./.env)", "Read(./secrets/**)"]
  },
  "allowManagedHooksOnly": true
}
```

- Servers not in `allowedMcpServers` cannot be used (an empty array locks MCP down entirely;
  `deniedMcpServers` takes precedence).
- Deterministic per-tool-call blocking is implemented with a PreToolUse hook — you can extend the
  script from [Method 3: Setting up hooks](/docs/developer-guide/method3-hooks) directly.
- Other tools offer admin policies as well (e.g., restricting MCP use in per-tool organization
  settings); check each tool's admin documentation.

## 6. Relationship to the existing gates

Even if every control on this page is bypassed, the [stage 3 CI hard block](/devsecops/intro)
mechanically stops secrets, vulnerabilities, and forbidden licenses at the artifact stage.
Conversely, the CI gate cannot see behavior that never lands in code (such as data exfiltration
through a tool), so tool controls and artifact gates are complementary — neither substitutes for
the other. [Stage 4 findings-driven review](./ai-security-review) adds reachability judgment in
between.

## 7. Standards linkage and sources

For linkage to the ISO/IEC standards, see [ISO Standards Linkage](./iso-mapping). The OpenChain
KWG guide does not yet cover this topic; this page is based on the primary sources below (as of
2026-07).

- MCP specification — [Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) and the Security and Trust & Safety section
- Microsoft Security Blog, [Securing AI agents: When AI tools move from reading to acting](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) (2026-06-30)
- OWASP GenAI Security Project, [LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) / [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) (Incubator stage)
- Hasan et al., [Model Context Protocol (MCP) at First Glance](https://arxiv.org/abs/2506.13538) — a study of 1,899 servers (5.5% tool poisoning)
- [Snyk agent-scan](https://github.com/snyk/agent-scan) / [Cisco mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner) / [ToolHive](https://github.com/stacklok/toolhive) / [MCP Gateway & Registry](https://github.com/agentic-community/mcp-gateway-registry)
- [Claude Code settings documentation](https://code.claude.com/docs/en/settings) (managed settings, MCP allowlist)
