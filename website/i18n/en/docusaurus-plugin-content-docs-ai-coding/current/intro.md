---
id: intro
title: AI Coding Governance
sidebar_label: Introduction
sidebar_position: 1
slug: intro
---

# AI Coding Governance

AI coding tools (Claude Code, Cursor, GitHub Copilot, Devin Desktop, OpenAI Codex, Gemini CLI, and
others) are now standard tools in development organizations. Whether the organization uses them under
the same rules has become a bigger question than whether to use them at all. This section covers how
to set those rules and run them.

Surveys point the same way. In Deloitte's State of AI in the Enterprise 2026 (2026-01, 3,235 leaders in
24 countries), 74% of companies planned to deploy agentic AI within two years, but only 21% said their
agent governance was mature. By governance Deloitte means clear boundaries for agent autonomy,
real-time monitoring, and audit trails covering the full chain of agent actions. In 2025-06 Gartner
predicted that over 40% of agentic AI projects will be canceled by the end of 2027 because of rising
costs, unclear business value, or inadequate risk controls. The tools are already in place; the rules
have not kept up.

AI coding governance does not end with preventing risk. DORA's 2025 report calls AI an amplifier: it
magnifies the strengths of high-performing organizations and the dysfunctions of struggling ones. With
the same tools, if review, testing, and collaboration do not keep up, the extra volume of change comes
back as bottlenecks and incidents.

## The four areas this section covers

AI coding governance covers both preventing risk and getting results. This section is organized into
four areas.

| Area | Question | Pages |
| --- | --- | --- |
| Governance foundations | Which tools are allowed, what data may be sent, and who is accountable? Who owns the copyright of AI-written code? | [AI Coding Tool Usage Policy](./usage-policy), [Legal Considerations for AI-Generated Code](./legal-considerations), [AI System Compliance](./iso42001) |
| Security and compliance controls | How do you block risks in AI-written code and in the tools agents call? | [5-Stage Strategy](./strategy), [Common Rules Template](./rules-template), [Quick CI/CD](./cicd-quick), [AI Security Code Review](./ai-security-review), [AI Fuzzing](./ai-fuzzing), [Agent & MCP Tool Governance](./agent-governance) |
| Productivity and collaboration | What must change so the extra changes do not get stuck in review and integration? | [Productivity and Collaboration in AI Coding](./collaboration) |
| Testing | How do you confirm that an AI-written change is correct? | [Testing for AI-Written Code](./testing) |

Tool setup is on the [Claude Code](./tools/claude-code), [Cursor](./tools/cursor),
[GitHub Copilot](./tools/copilot), [OpenAI Codex](./tools/codex), [Devin Desktop](./tools/windsurf),
and [Cline / Aider](./tools/cline-aider) pages, ordered by how widely each tool is used at work. In
JetBrains' Developer Ecosystem Survey 2026 (15,509 professional developers, published 2026-08), work
usage was Claude Code 39%, GitHub Copilot 21%, Codex 16%, and Cursor 12%.

The [Best Practice Repository](./best-practice-repo) is a reference implementation that collects the
settings and workflows for all four areas in one repository. Which ISO/IEC 5230 and 18974 requirements
each item strengthens is summarized in [Standard Coverage](./iso-mapping).

## Where to start

Expand only after confirming one step.

1. **Set the usage rules first.** Use the copy-paste block in the
   [AI Coding Tool Usage Policy](./usage-policy) to decide allowed tools and plans, data that must not be
   sent, and who is responsible. If you configure tools before setting rules, personal accounts and
   unapproved extensions stay in use.
2. **Add rules and gates.** Put a rules file in the repository ([Common Rules Template](./rules-template))
   and add secret, SAST, and SCA gates to CI ([Quick CI/CD](./cicd-quick)). Rules are advice; gates are
   what actually block.
3. **Make tests the verification standard.** Add core behavior tests and the test-weakening check
   ([Testing](./testing)). The scope you can hand to agents equals the scope your tests check.
4. **Pilot one task and measure.** Pick one repeated task, record current lead time and review wait time
   as a baseline, and hand it to an agent with a human approval point
   ([Productivity and Collaboration](./collaboration)).
5. **Expand based on results.** Set approval points, permission scope, cost limits, and a PR size
   guideline, then expand to other tasks and teams, adding Stages 4 and 5 of the
   [5-Stage Strategy](./strategy) and [MCP tool controls](./agent-governance).

## Relation to the Build Your System guide

If ISO/IEC 5230 and 18974 Self-Certification is your only goal, finish the [Build Your System](/en/docs)
track first. The policy, SBOM, and vulnerability-response deliverables the standards require are made
there. This section applies that policy to AI coding tools and CI so it holds at development time, and
extends it to productivity, collaboration, and testing, which the standards do not cover. Advanced
CI/CD pipeline design and organization-wide security strategy are covered in the
[DevSecOps guide](/en/devsecops/intro).
