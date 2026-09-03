---
id: agent-governance
title: 'Agent and MCP Tool Governance'
sidebar_label: 'Agent & MCP Tool Governance'
sidebar_position: 7
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

| Plane                                   | Threat                                                                                         | Defense                                                                                            |
| --------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Input (prompts and rules files)         | Indirect prompt injection — instructions planted in content the agent reads and in rules files | Minimize untrusted content access, review rules files in PRs, human approval for high-risk actions |
| Tools (MCP servers, skills, extensions) | Tool poisoning, tool shadowing, chained tool calls, malicious package installs                 | Server allowlist, pre-adoption scanning and egress review, version pinning, provenance checks      |
| Artifact (code)                         | Tainted generated code, vulnerable or forbidden-license dependencies                           | Existing CI hard blocks (secrets, SAST, SCA) — the last line of defense                            |

The point is that the three planes are complementary: if input and tool controls are bypassed, the
artifact gate remains, and behavior that never lands in code (data exfiltration through a tool) is
caught by tool controls, not the CI gate.

Rules files are called out separately on the input plane for a reason. They are easy to treat as
human-authored configuration, but to an agent they are instructions read in every session, and
anything planted there influences every code suggestion that follows. The Rules File Backdoor
(Pillar Security, 2025-03-18) hides instructions in a rules file using zero-width joiners and
Unicode Tags. The characters do not render in a PR diff, so a change arriving from a fork passes
review. The AIShellJack study (arXiv:2509.22040) evaluated GitHub Copilot and Cursor with 314
payloads covering 70 MITRE ATT&CK techniques and reported attack success rates of 41% to 84%, the
highest being 83.4% for Cursor in auto-approve mode on TypeScript scenarios. The check procedure is
in the [Common Rules Template](./rules-template).

Configuration files sit on the same plane. An MCP configuration file looks like a declaration
listing servers, but what it actually holds is an execution command. Research published by Ox
Security on 2026-04-15 reported that the STDIO transport in all four official MCP SDKs (Python,
TypeScript, Java, Rust) passes values taken from configuration to a shell without validation. From
more than 150 million cumulative downloads and more than 7,000 externally exposed servers, the
researchers estimated an impact of up to 200,000 instances, and ten critical or high severity CVEs
were issued. Anthropic answered that the behavior is by design and that sanitizing input is the
developer's responsibility, so the protocol was not changed. The MCP specification's security best
practices document covers the same risk under local server compromise, listing a malicious startup
command planted in a client configuration as the first attack scenario. The defense therefore stays
with the adopting organization: an MCP configuration file has to be treated as an execution path
for code, not as configuration. The concrete handling is in section 3 below.

## 3. Nine working controls

Translating the Microsoft Incident Response guidance (2026-06) and the MCP spec's security
principles into working rules gives five; two more are drawn from actual incidents, making seven.
Two more follow from the authorization changes in the specification and from the transport research
above, making nine.

National agency guidance points the same way. "Careful adoption of agentic AI services", published
jointly at the end of April 2026 by five agencies (the Canadian Centre for Cyber Security,
Australia's ACSC, the United States CISA and NSA, New Zealand's NCSC, and the United Kingdom's
NCSC), recommends layered defence and strict access controls to reduce the likelihood of
compromise, and organizes its guidance into four areas: designing and developing secure agents,
deploying agentic AI securely, operating it securely, and defending against future risks. It is a
government document you can cite when an internal policy needs approval.

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

### Tool and extension supply chain

The six controls above govern how an approved tool is used. The seventh looks at where the tool came
from. MCP servers, agent skills, and IDE extensions are all third-party packages that execute code
with developer privileges, so they belong in the same procedure as any dependency. Yet none of them
appear in a lockfile, so existing SCA results never show them.

The evidence runs in three strands.

- Agent skills. Snyk's ToxicSkills research (2026-02) examined 3,984 skills and found 13.4% (534)
  carrying at least one critical-level issue. Of the 76 malicious payloads confirmed by hand, 91%
  also used prompt injection techniques.
- MCP servers. Besides `postmark-mcp` under version pinning above,
  `@lanyer640/mcp-runcommand-server` shipped with a double backdoor on 2025-09-30. The official MCP
  Registry has stayed in preview since its 2025-09-08 launch, and it moderates listings reactively
  on community reports rather than certifying the safety of listed code. Being in the registry does
  not mean a listing passed review.
- IDE extensions. GlassWorm spread through the Open VSX marketplace in 2025-10 with 35,800 installs
  and returned in a second wave in 2025-11. In 2026-03 a variant delivered through transitive
  dependencies affected 72 extensions, including ones impersonating Claude Code and Codex. On the VS
  Code marketplace, MaliciousCorgi affected roughly 1.5 million developers in 2026-01, and 15
  malicious AI plugins were confirmed on the JetBrains marketplace in 2026-06.

Four working controls follow.

- Check provenance before installing. Look at the publisher, the linked repository, recent commits,
  and any sudden jump in download counts. A marketplace or registry listing is not evidence of
  review.
- Run an allowlist. Permit only approved MCP servers, skills, and extensions, and stop individuals
  from adding their own. Claude Code enforces this through the managed settings in section 5; VS
  Code and JetBrains each offer an extension allowlist in their organization policies.
- Audit on a schedule. Re-check the installed list periodically. What the cases above have in common
  is a package that was clean at approval and changed in a later version. Snyk agent-scan in
  section 4 covers agent configurations and skills, not just MCP servers.
- Isolate execution. With isolation off, Claude Code runs file tools, MCP servers, and hooks
  directly on the host. The built-in sandbox isolates Bash subprocesses only, and Read, Edit, and
  Write go through the permission system instead, so putting MCP servers and hooks inside the
  boundary means isolating the whole process. That isolation is opt-in: choose
  `@anthropic-ai/sandbox-runtime`, a dev container, a virtual machine, or Claude Code on the web.
  Even before turning it on, adding configuration paths such as `.claude/settings.json` and
  `.mcp.json` to `permissions.deny` (deny always wins over allow) blocks the specific path an
  agent would use to change its own privileges. Write the rule as `Edit(./.mcp.json)`. The
  documentation states that file permissions are checked against `Edit(path)` and `Read(path)`
  rules only, so a path rule written as `Write(...)` or `MultiEdit(...)` is accepted, never
  consulted, and only warned about at startup. Get the form wrong and the path you believed was
  blocked is open.

Bringing IDE extensions into scanning scope continues in
[Software Composition Analysis (SCA)](/devsecops/sca).

### The authorization layer

After the seven controls above settled, the MCP specification changed authorization substantially.
The 2025-11-25 revision added OAuth Client ID Metadata Documents as the recommended client
registration mechanism and introduced authorization server discovery based on OpenID Connect
Discovery. The 2026-07-28 revision removed the initialization handshake to make the protocol
stateless, and at the same time it requires clients to validate the `iss` value in an authorization
response against the issuer they recorded (RFC 9207) and to key client credentials by the issuing
authorization server so they are never reused with another one. This blocks mix-up attacks, where
an attacker-controlled authorization server gets the client to send it a code issued by an honest
one; the specification notes that PKCE alone does not prevent this. The same revision deprecated
OAuth Dynamic Client Registration (RFC 7591) in favor of Client ID Metadata Documents, keeping it
only for backward compatibility with authorization servers that do not support them.

For organization-wide adoption, the official Enterprise-Managed Authorization extension applies
directly. Instead of each user approving each server, the corporate IdP decides which servers may
be reached and under what conditions, and granting and revoking access on joining and leaving
happens in one place. Three working rules follow.

- Confirm which revision the clients and servers you use implement. The move to a stateless
  protocol is a breaking change, so record the version combination in place at adoption.
- Have newly adopted clients use Client ID Metadata Documents rather than Dynamic Client
  Registration.
- Where a corporate IdP exists, route access through Enterprise-Managed Authorization instead of
  per-server approvals. The extension is never on by default, so check first that the intended
  client supports it.

### Treating configuration files as execution paths

The STDIO transport flaw in section 2 will not be fixed in the protocol, so it has to be contained
in operations. Files that carry server startup commands, such as `.mcp.json` and an IDE's MCP
settings, deserve the same treatment as source code.

- Keep configuration files in the repository so changes surface as a PR. The reason for committing
  `.mcp.json` in section 5 applies here as well.
- Never place user input or externally supplied strings into configuration values. Preventing the
  agent from writing its own configuration file belongs to the same control; blocking writes to
  configuration paths through `permissions.deny` is described under isolated execution above.
- Launch servers by passing the executable and its arguments separately rather than through a
  shell.
- Check which SDK version you use and move to at least the release that fixes the related CVEs. The
  same applies to servers you build yourself.

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

### The repository-scoped version

Where you cannot deploy managed settings, checked-in repository config is a place to start. The
[ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice) repository carries
that shape.

| File                                                                                                           | Control it carries                                                             |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [.mcp.json](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.mcp.json)                         | Declares approved servers; currently empty                                     |
| [.claude/settings.json](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.claude/settings.json) | No server auto-approved, secret reads blocked, approval for egress and deploys |
| [CLAUDE.md](https://github.com/trustedoss/ai-coding-best-practice/blob/main/CLAUDE.md)                         | Tool-description review, egress judgement, how to add a server                 |

One difference matters. Some of the managed-settings example above carries over to repository
config and some does not. Per the settings reference, `allowedMcpServers`, `deniedMcpServers`,
`enabledMcpjsonServers`, `disabledMcpjsonServers`, `enableAllProjectMcpServers` and
`disableClaudeAiConnectors` all apply from user and project settings files, not only managed ones.
The key that works in managed settings alone is `allowManagedMcpServersOnly`, which is ignored in
repository config. What managed settings buy you is the part an individual cannot override, so
treat repository settings as the place that sets a default rather than the place that closes a
bypass.

Leave `enableAllProjectMcpServers` at its default of `false`: it approves every server in
`.mcp.json` with no prompt. Keeping `.mcp.json` in the repository is what makes adding a server
show up as a PR diff instead of in someone's personal config.

Three of the nine controls do not reduce to a file: reviewing tool descriptions, judging the egress
path, and checking the provenance of tools and extensions. They stay written rules whose results
belong in the PR.

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

Discussion on the standards side is under way. A proposal for an Agent Bill of Materials, covering
the MCP servers, tool definitions, models, and identity credentials an agent uses, was opened in the
CycloneDX specification repository (issue #895, opened 2026-03-26). It was closed as a duplicate on
2026-04-29, with a maintainer noting that agentic AI is being addressed in the ongoing work of the
Blueprints and Threat Modeling working groups. The need is on the table, but whether a dedicated
component type will be added or the information expressed some other way is not settled.

No standards body guidance on representing MCP servers in an SBOM has been identified. The mapping
above interprets the existing specification and is not a standardized practice. Until that settles,
keep the mapping above; even when you use organization-defined properties, recording which item you
captured under which name makes it easier to move to a standard representation later. For hands-on
SBOM generation, see [SBOM Generation](/docs/tools/sbom-generation).

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

Two more framework deliverables are now worth consulting. The OWASP Top 10 for Agentic Applications
2026 (published 2025-12-09) organizes risks such as agent goal hijacking, tool misuse, identity and
privilege abuse, memory poisoning, insecure inter-agent communication, cascading failures, trust
exploitation, and rogue agents, which overlaps the threat model in section 2. OWASP AISVS 1.0
(published 2026-06) is a different kind of document: not an awareness list but a catalogue of
verifiable requirements. Of its twelve chapters, chapter 9 covers orchestration and agentic action
and chapter 10 covers MCP security. Each requirement carries a verification level from 1 to 3, so an
organization can pick a target level and carry the requirements straight into a self-certification
checklist. Chapter 10, for instance, requires that MCP components be obtained only from trusted
sources and cryptographically verified (level 1), that only allow-listed servers be permitted
(level 2), and that locally launched servers run in a least-privilege sandbox (level 2), which maps
directly onto the controls in section 3.

- MCP specification — [Security Best Practices](https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices) and the Security and Trust & Safety section. The current revision is 2026-07-28; the authorization changes are in the [2025-11-25 changelog](https://modelcontextprotocol.io/specification/2025-11-25/changelog) and the [2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- MCP official extension — [Enterprise-Managed Authorization](https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization) (stable) — a corporate IdP deciding MCP server access centrally
- Ox Security, [The Mother of All AI Supply Chains](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/) (2026-04-15) — the STDIO transport flaw across four official SDKs, ten CVEs, an estimate of up to 200,000 instances
- Canadian Centre for Cyber Security et al., [Careful adoption of agentic AI services](https://www.cyber.gc.ca/en/news-events/joint-guidance-careful-adoption-agentic-artificial-intelligence-services) (posted 2026-05-01) — joint guidance from agencies in Canada, Australia, the United States, New Zealand, and the United Kingdom
- Microsoft Security Blog, [Securing AI agents: When AI tools move from reading to acting](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/) (2026-06-30)
- OWASP GenAI Security Project, [Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) (2025-12-09) / [LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) (2026-08-03, the revision succeeding the LLM01:2025 entry cited above) / [LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) / [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) (Incubator stage)
- OWASP, [AISVS 1.0](https://github.com/OWASP/AISVS) (2026-06) — chapter 9 on orchestration and agentic action, chapter 10 on MCP security, verification levels 1 to 3
- CycloneDX, [Proposal: Agent Bill of Materials](https://github.com/CycloneDX/specification/issues/895) (opened 2026-03-26, closed as duplicate 2026-04-29) — the state of the agent-specific BOM discussion
- Hasan et al., [Model Context Protocol (MCP) at First Glance](https://arxiv.org/abs/2506.13538) — a study of 1,899 servers (5.5% tool poisoning)
- Invariant Labs, [MCP Security Notification: Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) (2025-04-01) — the first public disclosure of the technique
- Snyk, [Malicious MCP Server on npm: postmark-mcp Harvests Emails](https://snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails/) (2025-09-25) — the malicious versions are believed to start at 1.0.16, and no link to the ActiveCampaign/Postmark repository was confirmed
- GitGuardian, [From Path Traversal to Supply Chain Compromise: Breaking MCP Server Hosting](https://blog.gitguardian.com/breaking-mcp-server-hosting/) (2025-10-15) — a responsibly disclosed and fixed vulnerability, not a breach
- OWASP CycloneDX, [Specification Overview](https://cyclonedx.org/specification/overview/) / [JSON Schema 1.7](https://cyclonedx.org/schema/bom-1.7.schema.json) — `service` object fields and the `component.type` enumeration
- Pillar Security, [New Vulnerability in GitHub Copilot and Cursor: How Hackers Can Weaponize Code Agents](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents) (2025-03-18) — the Rules File Backdoor
- Liu et al., ["Your AI, My Shell": Demystifying Prompt Injection Attacks on Agentic AI Coding Editors](https://arxiv.org/abs/2509.22040) — AIShellJack, 314 payloads, 41–84% success rates
- Snyk, [ToxicSkills: Malicious AI Agent Skills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) (2026-02) — 13.4% of 3,984 skills carried a critical-level issue
- Model Context Protocol Blog, [Introducing the MCP Registry](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/) (2025-09-08) — preview status and report-driven moderation
- Koi Security, [GlassWorm: First Self-Propagating Worm Using Invisible Code Hits OpenVSX Marketplace](https://www.koi.ai/blog/glassworm-first-self-propagating-worm-using-invisible-code-hits-openvsx-marketplace) (2025-10-18) / [MaliciousCorgi](https://www.koi.ai/blog/maliciouscorgi-the-cute-looking-ai-extensions-leaking-code-from-1-5-million-developers) (2026-01-22)
- [Snyk agent-scan](https://github.com/snyk/agent-scan) / [Cisco mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner) / [ToolHive](https://github.com/stacklok/toolhive) / [MCP Gateway & Registry](https://github.com/agentic-community/mcp-gateway-registry) / [agentgateway](https://agentgateway.dev/)
- [Claude Code settings documentation](https://code.claude.com/docs/en/settings) (managed settings, MCP allowlist) / [Sandboxing](https://code.claude.com/docs/en/sandboxing) / [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments) — isolation scope and its opt-in nature
