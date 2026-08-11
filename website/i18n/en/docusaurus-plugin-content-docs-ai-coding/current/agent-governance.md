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

This is **stage 4c** of the [five-stage model](./strategy). 4a re-judges what the scanners flagged
and 4b searches what they never flagged; both read code the AI wrote. 4c covers what the AI calls,
which no pull request ever shows.

:::note Scope of this page

This page covers **agents used during development**. The goal is securing the development
environment and confirming code provenance; the target is developer workstations, so the work is
closer to continuous monitoring than to producing deliverables.

**Agents embedded in shipped products** have different requirements. They are components of a
service delivered to customers, so each release needs deliverables, and MCP servers become runtime
dependencies that must be listed in the product SBOM (section 6 below). For regulatory obligations
see [Legal Considerations](./legal-considerations); for managing the AI system itself see
[ISO/IEC 42001](./iso42001).

:::

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

| Plane               | Threat                                                                      | Defense                                                                    |
| ------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Input (prompts)     | Indirect prompt injection — instructions planted in content the agent reads | Minimize untrusted content access, human approval for high-risk actions    |
| Tools (MCP servers) | Tool poisoning, tool shadowing, chained tool calls                          | Server allowlist, pre-adoption scanning and egress review, version pinning |
| Artifact (code)     | Tainted generated code, vulnerable or forbidden-license dependencies        | Existing CI hard blocks (secrets, SAST, SCA) — the last line of defense    |

The point is that the three planes are complementary: if input and tool controls are bypassed, the
artifact gate remains, and behavior that never lands in code (data exfiltration through a tool) is
caught by tool controls, not the CI gate.

## 3. Six working controls

Translating the Microsoft Incident Response guidance (2026-06) and the MCP spec's security
principles into working rules gives five; a sixth is drawn from an actual incident.

How strictly each applies depends on where the server comes from. Only the first row needs
across-the-board review; the rest ride on existing procedures or are handled at another stage.

| Source                    | Example                                       | Handling                                                           |
| ------------------------- | --------------------------------------------- | ------------------------------------------------------------------ |
| Public community releases | npm/PyPI public packages                      | Review and approve every server; pin versions and track changes    |
| Vendor official servers   | GitHub, Atlassian, etc. for their own service | Light review focused on permission scope and egress paths          |
| In-house servers          | Internal repos, issue trackers, databases     | Design review, not approval — decide privileges and exposure early |
| Bundled with a tool       | Shipped with a commercial coding agent        | Review as part of tool selection                                   |

If servers are adopted through a hosting platform, the platform itself is in scope. A path traversal
vulnerability in the MCP hosting platform Smithery left more than 3,000 hosted servers open to
arbitrary code execution (a researcher found and reported it, and it was fixed; no exploitation was
observed). Reviewing individual servers does not help when the hosting path is a single point of
failure.

### MCP server allowlist

Use only approved servers and disable "allow all"-style settings. New servers pass the scanning
in section 4 before registration.

### Least privilege

Limit the agent's file, network, and command-execution scope to what is needed.

### Description review

Tool descriptions from untrusted sources are review targets, both at adoption and on updates
(descriptions can change when a server updates).

### Version pinning

Pin agents and MCP servers like any dependency and track changes. The npm package `postmark-mcp`
was clean through 1.0.15, then later versions (believed to start at 1.0.16) added a hidden BCC
copying every outgoing email to an external address. Approving once at adoption cannot catch this.

### Human approval and audit logs

Never auto-approve high-risk actions — file deletion, external transmission, deployment — and keep
tool-call history.

### Egress path review

Before adoption, determine which external endpoints the server talks to and whether internal data
can leave through them. `postmark-mcp` above is exactly the kind of case this catches. Record the
result in the SBOM as described in section 6.

## 4. Automation tools

| Control point             | Main                                        | Alternative                                            |
| ------------------------- | ------------------------------------------- | ------------------------------------------------------ |
| Pre-adoption scanning     | Snyk agent-scan (Apache-2.0)                | Cisco mcp-scanner (Apache-2.0)                         |
| Centralized operation     | ToolHive (Stacklok, Apache-2.0)             | MCP Gateway & Registry (agentic-community, Apache-2.0) |
| Unified agent traffic     | agentgateway (Linux Foundation, Apache-2.0) | —                                                      |
| Developer-endpoint policy | Tool built-in controls (section 5)          | —                                                      |

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

**Unified agent traffic — agentgateway**: an open-source proxy built by solo.io and contributed to
the Linux Foundation in August 2025. It handles large language model API calls, MCP, Agent-to-Agent
(A2A), and HTTP in a single data plane. Where ToolHive focuses on a trusted catalog of MCP servers
and isolated execution, agentgateway concentrates all agent traffic — including model API calls —
at one point. It is not a substitute but a different scope of control.

Start with logs before policy. Blocking rules work from the moment you add them, but logs for a
period already past cannot be reconstructed. Begin recording even before the scope of control is
settled. From there, move up in stages: observe only, then warn, then block. Blocking first creates
workarounds, and once workarounds become routine the control itself stops working.

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

## 6. Listing MCP servers in the SBOM

Once an MCP server becomes a runtime dependency, it belongs in the SBOM. Alongside `components`,
CycloneDX defines a `services` element that describes external services an application calls —
endpoint URIs, authentication requirements, whether a trust boundary is crossed, and data
classification and flow direction.

- **Remote MCP servers** — list under `services`, using `endpoints`, `authenticated`,
  `x-trust-boundary`, `trustZone`, and `data` (`flow` direction and `classification`).
- **Locally executed MCP server packages** — list under `components` and treat them like any other
  dependency.

Being able to state data flow direction connects directly to control 6 in section 3 (egress path
review): the result of determining what a server sends to which external endpoint goes straight
into the document.

Know the limits as well. The `component.type` enumeration in CycloneDX 1.7 has no type specific to
MCP servers, and there is no field for MCP-specific risks such as tool poisoning. For now the
approach is to list them as ordinary services and add organization-defined `properties`. Those
definitions carry no meaning outside your organization, so they are hard to require of suppliers
and need separate explanation when used for regulatory filings.

No standards body guidance on representing MCP servers in an SBOM has been identified. The mapping
above interprets the existing specification and is not a standardized practice. For hands-on SBOM
generation, see [SBOM Generation](/docs/tools/sbom-generation).

## 7. Relationship to the existing gates

Even if every control on this page is bypassed, the [stage 3 CI hard block](/devsecops/intro)
mechanically stops secrets, vulnerabilities, and forbidden licenses at the artifact stage.
Conversely, the CI gate cannot see behavior that never lands in code (such as data exfiltration
through a tool), so tool controls and artifact gates are complementary — neither substitutes for
the other. [Stage 4 findings-driven review](./ai-security-review) adds reachability judgment in
between.

## 8. Standards linkage and sources

For linkage to the ISO/IEC standards, see [ISO Standards Linkage](./iso-mapping); for copyright
and regulation of AI-generated code, see [Legal Considerations](./legal-considerations). The OpenChain
KWG guide does not yet cover this topic; this page is based on the primary sources below (as of
2026-08).

- MCP specification — [Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) and the Security and Trust & Safety section
- Microsoft Security Blog, [Securing AI agents: When AI tools move from reading to acting](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) (2026-06-30)
- OWASP GenAI Security Project, [LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) / [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) (Incubator stage)
- Hasan et al., [Model Context Protocol (MCP) at First Glance](https://arxiv.org/abs/2506.13538) — a study of 1,899 servers (5.5% tool poisoning)
- Invariant Labs, [MCP Security Notification: Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) (2025-04-01) — the first public disclosure of the technique
- Snyk, [Malicious MCP Server on npm: postmark-mcp Harvests Emails](https://snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails/) (2025-09-25) — the malicious versions are believed to start at 1.0.16, and no link to the ActiveCampaign/Postmark repository was confirmed
- GitGuardian, [From Path Traversal to Supply Chain Compromise: Breaking MCP Server Hosting](https://blog.gitguardian.com/breaking-mcp-server-hosting/) (2025-10-15) — a responsibly disclosed and fixed vulnerability, not a breach
- OWASP CycloneDX, [Specification Overview](https://cyclonedx.org/specification/overview/) / [JSON Schema 1.7](https://cyclonedx.org/schema/bom-1.7.schema.json) — `service` object fields and the `component.type` enumeration
- [Snyk agent-scan](https://github.com/snyk/agent-scan) / [Cisco mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner) / [ToolHive](https://github.com/stacklok/toolhive) / [MCP Gateway & Registry](https://github.com/agentic-community/mcp-gateway-registry) / [agentgateway](https://agentgateway.dev/)
- [Claude Code settings documentation](https://code.claude.com/docs/en/settings) (managed settings, MCP allowlist)
