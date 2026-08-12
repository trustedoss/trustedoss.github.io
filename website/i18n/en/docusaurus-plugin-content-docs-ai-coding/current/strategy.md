---
id: strategy
title: 5-Stage Strategy by Assurance Level
sidebar_label: 5-Stage Strategy
sidebar_position: 2
---

# 5-Stage Strategy by Assurance Level

## Overview

| Stage   | Name                                     | Core Method                                           | Assurance Level | Recommended For         |
| ------- | ---------------------------------------- | ----------------------------------------------------- | --------------- | ----------------------- |
| Stage 1 | Prompt Dependency                        | None (personal memory)                                | Low             | Individual experiments  |
| Stage 2 | AI Rule Internalization                  | CLAUDE.md, .cursor/rules, AGENTS.md, etc.             | Medium          | Team collaboration      |
| Stage 3 | CI/CD Auto Blocking                      | Gitleaks · Semgrep · CodeQL · grype · Trivy · Checkov | High            | Teams and organizations |
| Stage 4 | AI Defense Layer                         | findings-driven AI review · AI fuzzing                | High+           | Teams and organizations |
| Stage 5 | Continuous Monitoring & Auto-remediation | Dependabot · Renovate · DAST                          | Very high       | Organization-wide       |

Stage 1 can be started immediately, but true DevSecOps gatekeeping begins at Stage 3.
**Stage 4 is a defense layer that counters AI-driven attacks with AI.**

---

## Stage 1: Prompt Dependency (Manual / Ad-hoc)

:::info Where this stage stands
It is the easiest to adopt but also the most unstable.
:::

This approach enforces license or security policies by entering prompts directly into AI tools, such as "Use only MIT-licensed code." It can be started immediately without tools or settings, but everything depends entirely on each developer's memory and skill. There is always a risk that AI hallucination introduces GPL code unintentionally or recommends package versions with known vulnerabilities. It may be sufficient for individual learning or experiments, but it is hard to guarantee consistency in team collaboration.

---

## Stage 2: AI Rule Internalization (Tool-level Context Injection)

:::tip Team-level adoption starts here
:::

This approach places common rule files such as CLAUDE.md, .cursor/rules, and AGENTS.md in the repository so AI automatically recognizes policies while writing code. The whole team shares the same rules, and AI can be expected to check licenses or suggest the latest stable versions when adding external libraries. However, AI treats rules as guidance, so 100% enforced hard blocking is not possible. If you want to start rule-based collaboration right away, refer to the links below.

- [Common Rules Template](./rules-template)
- [Tool-specific Setup](./tools/claude-code)

If your agents call external tools over MCP, rule internalization needs tool-side controls alongside it — see [Agent and MCP Tool Governance](./agent-governance).

---

## Stage 3: CI/CD Pipeline Auto Blocking (Pipeline Enforcement)

:::warning True hard blocking starts at this stage
:::

At this stage, the pipeline mechanically verifies the five areas below before PR or merge. It can block policy-violating code at the source regardless of mistakes by developers or AI, and this is where true gatekeeping begins.

| Area               | Representative Tools | Pipeline Position | Detection Target                                       |
| ------------------ | -------------------- | ----------------- | ------------------------------------------------------ |
| Secret Detection   | Gitleaks             | pre-commit · PR   | Hardcoded API keys, tokens, passwords                  |
| SAST               | Semgrep · CodeQL     | PR                | SQL injection, logic bugs, vulnerable patterns         |
| SCA                | syft · grype         | PR · Build        | Known CVEs, prohibited licenses                        |
| Container Security | Trivy                | Build             | Image vulnerabilities (when using containers)          |
| IaC Security       | Checkov              | PR                | Cloud infrastructure misconfiguration (when using IaC) |

AI coding tools frequently insert hardcoded values into code, so **secret detection is mandatory from day one of Stage 3**. Rather than introducing all areas at once, it is recommended to stabilize in this order: secret detection → SAST → SCA, then move on.

- [30-Minute Quick CI/CD](./cicd-quick) — Minimal starting point focused on SCA
- [DevSecOps — Secret Detection](/devsecops/secret-detection) · [SAST](/devsecops/sast) · [SCA](/devsecops/sca) · [Container Security](/devsecops/container-security) · [IaC Security](/devsecops/iac-security)
- [Organization-wide Pipeline Design](/devsecops/pipeline-design)

**In practice — TRUSCA**: an Apache-2.0 open source SCA project runs this level today. The
workflow files are open to read.

| Area             | Workflow                                                                                            | How it runs                                           |
| ---------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Secret detection | [secret-scan.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/secret-scan.yml) | Gitleaks, hard fail on any leak                       |
| SAST             | [sast.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sast.yml)               | bandit (High) + semgrep (ERROR), hard fail            |
| SAST             | [codeql.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/codeql.yml)           | CodeQL static analysis                                |
| SCA              | [sca-self.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sca-self.yml)       | cdxgen SBOM then Trivy scan, daily                    |
| Container        | [ci.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/ci.yml)                   | image-scan job, Trivy, hard fail on HIGH and CRITICAL |

Hard-failing on secrets and SAST, pinning tool versions, and verifying checksums are what a mature
form of this level looks like.

---

## Stage 4: AI Defense Layer (AI-Augmented Defense)

:::info Closing the stage 3 blind spot with AI
Stage 3 tools detect **known patterns** accurately. What a rule does not define, they do not catch:
business logic flaws, missing authorization checks, and broken state transitions. That limit of
static analysis predates AI coding.

What AI coding changed is **the volume of code landing in that blind spot**. Output multiplies while
review headcount does not, and AI-generated code reads cleanly enough that reviewers rarely stop on
it. Attackers can also use AI to generate rule-evading variants.

4a and 4b close that blind spot with AI. 4c runs the other way: it covers what the AI itself
reaches for, since an agent calling outside tools pulls in input no pull request ever shows.
:::

Stage 3 tools first narrow down candidates through pattern matching, and AI then focuses on those results to perform **semantic judgment** and **active exploration**.

### 4a. Findings-Driven AI Review

Instead of sending all code to AI, only **code snippets flagged by Stage 3 tools** are sent. This saves tokens while focusing on areas that require AI judgment.

| AI Role                 | Input                                        | Output                                                       |
| ----------------------- | -------------------------------------------- | ------------------------------------------------------------ |
| **Validation**          | Semgrep/CodeQL results + related code        | FP/TP classification, exploitability assessment              |
| **Deep Interpretation** | grype CVE + usage locations of the component | "Is this CVE actually reachable in our execution path?"      |
| **Related Discovery**   | Flagged pattern + adjacent code blocks       | Neighboring vulnerabilities of the same type missed by tools |

When multiple tools flag the same location, AI raises priority and alerts developers. AI review results are **posted as PR comments**, and the build is not force-failed (because FP rates are high).

- [AI Security Code Review](./ai-security-review) — Findings-driven implementation guide and GitHub Actions example

**In practice — TRUSCA**: [ai-review.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/ai-review.yml) runs this level (added 2026-08).
Three design decisions are worth borrowing.

- **It blocks nothing.** A comment in the file states it must never be added to branch protection —
  the principle that a model's verdict cannot gate a build, written into the workflow itself
- **It scans only what the PR changed**, not the whole repository, which cuts cost and noise together
- **It skips entirely without a key.** Forks and early adopters see the job succeed rather than fail

The file also explains why it re-runs the stage 3 tools: a job running at a blocking threshold
produces either nothing or a build that has already failed, leaving no input to triage.

### 4b. AI Fuzzing

AI **actively explores** areas untouched by Stage 3 tools, such as business logic and edge-case input handling. LLMs like Claude analyze endpoint signatures, generate boundary and abnormal inputs automatically, and execute them directly against the app to detect 5xx errors and abnormal behavior. For low-level C/C++ and Rust code, OSS-Fuzz integration is recommended.

| Tool Combination  | Detection Target                                | Execution Cycle           |
| ----------------- | ----------------------------------------------- | ------------------------- |
| Claude + requests | Web API edge cases and abnormal responses       | Push to main              |
| Claude + AFL++    | Low-level binary crashes                        | Weekly schedule           |
| Claude + OSS-Fuzz | Parser vulnerabilities in open source libraries | Per-project configuration |

- [AI Fuzzing](./ai-fuzzing) — the workflow, the script, and what to watch when adopting it

**In practice — ai-coding-best-practice**:
[ai-fuzzing.yml](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/workflows/ai-fuzzing.yml)
and [scripts/ai-fuzz.py](https://github.com/trustedoss/ai-coding-best-practice/blob/main/scripts/ai-fuzz.py)
run this stage on pushes to main and every Sunday. The app is started and health-checked, the
model's edge cases go out as real requests, and 5xx responses are recorded as findings. Results are
kept as `fuzz-report.json` for 30 days. Without `ANTHROPIC_API_KEY` the job skips rather than fails.

**TRUSCA does not run this stage.** It is an SCA product, so fuzzing a web application does not
apply. The working example for 4b is the reference repository above.

### 4c. Agent and MCP Tool Governance

4a and 4b both look at code the AI wrote. This one looks at what the AI _calls_. An agent that
reaches outside the repository over MCP (Model Context Protocol) pulls in tool descriptions and
tool output that never pass through a pull request, so neither the stage 2 rule file nor the stage 3
gate ever sees them. A study of 1,899 open-source MCP servers found 5.5% carrying tool poisoning,
and the npm package `postmark-mcp` was clean through 1.0.15 before later versions added a hidden BCC
on every outgoing mail.

The control set is a server allowlist, least privilege, description review, version pinning, human
approval with audit logs, and egress path review, backed by pre-adoption scanning.

- [Agent and MCP Tool Governance](./agent-governance) — the six controls, the scanners, and a
  copy-paste organization policy

---

## Stage 5: Continuous Monitoring & Auto-remediation (Continuous & Auto-remediation)

At this stage, SBOM is continuously scanned even after deployment, and patch PRs are generated automatically when new CVEs are discovered. Integration with Dependabot and Renovate maintains centralized supply chain security compliance (ISO/IEC 18974). Human intervention for policy compliance is minimized, creating a virtuous cycle that continuously controls AI-induced risk through automation.

- [Continuous Monitoring & Auto-remediation](/devsecops/monitoring)
- [DAST — Dynamic Analysis](/devsecops/dast)

**In practice — TRUSCA**:

| Component          | File                                                                                                  | What it does                                                    |
| ------------------ | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Dependency updates | [dependabot.yml](https://github.com/trustedoss/trusca/blob/main/.github/dependabot.yml)               | npm, pip, docker, github-actions — four ecosystems, six entries |
| Scheduled scanning | [sca-self.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sca-self.yml)         | Regenerates the SBOM and rescans daily at 07:00 UTC             |
| Dogfooding         | [dogfood-scan.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/dogfood-scan.yml) | Scans its own repository with its own SCA; advisory by default  |

`dogfood-scan.yml` defaults to non-blocking and turns blocking on through a `fail_on_gate` input —
the same observe, then warn, then block progression this guide recommends.

---

## Where should our team start?

:::tip Stage selection guide
:::

If you are developing alone or running a small-scale experiment, starting from Stage 2 is recommended. Setup can be completed within 10 minutes at no extra cost.

If your team already uses GitHub Actions, try Stage 3 Quick CI/CD first. You can build a basic security gate in 30 minutes.

If you are operating Stage 3 stably, add the Stage 4 AI defense layer. A single `ANTHROPIC_API_KEY` can activate both findings-driven review and AI fuzzing.

If you already operate up to Stage 4 and have a dedicated security team, review Stage 5 and the full DevSecOps guide to raise organization-wide supply chain security maturity.

Regardless of stage, adopting an AI coding tool requires three legal decisions: copyright attribution, vendor IP indemnification, and AI-use disclosure. Review [Legal Considerations for AI-Generated Code](./legal-considerations) alongside your rollout.
