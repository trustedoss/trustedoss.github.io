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
| Stage 2 | AI Rule Internalization                  | CLAUDE.md, .cursorrules, etc.                         | Medium          | Team collaboration      |
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

This approach places common rule files such as CLAUDE.md, .cursorrules, and .clinerules in the repository so AI automatically recognizes policies while writing code. The whole team shares the same rules, and AI can be expected to check licenses or suggest the latest stable versions when adding external libraries. However, AI treats rules as guidance, so 100% enforced hard blocking is not possible. If you want to start rule-based collaboration right away, refer to the links below.

- [Common Rules Template](./rules-template)
- [Tool-specific Setup](./tools/claude-code)

---

## Stage 3: CI/CD Pipeline Auto Blocking (Pipeline Enforcement)

:::warning True hard blocking starts at this stage
:::

At this stage, the pipeline mechanically verifies the six areas below before PR or merge. It can block policy-violating code at the source regardless of mistakes by developers or AI, and this is where true gatekeeping begins.

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

---

## Stage 4: AI Defense Layer (AI-Augmented Defense)

:::info Use AI defense against AI attacks
Attackers also use AI to generate new vulnerability patterns and automatically produce code that bypasses existing rule sets.
Stage 3 tools catch **known patterns** accurately, but novel AI-generated patterns can pass because they are not in the rule set.
Stage 4 uses AI to defend this blind spot.
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

### 4b. AI Fuzzing

AI **actively explores** areas untouched by Stage 3 tools, such as business logic and edge-case input handling. LLMs like Claude analyze endpoint signatures, generate boundary and abnormal inputs automatically, and execute them directly against the app to detect 5xx errors and abnormal behavior. For low-level C/C++ and Rust code, OSS-Fuzz integration is recommended.

| Tool Combination  | Detection Target                                | Execution Cycle           |
| ----------------- | ----------------------------------------------- | ------------------------- |
| Claude + requests | Web API edge cases and abnormal responses       | Push to main              |
| Claude + AFL++    | Low-level binary crashes                        | Weekly schedule           |
| Claude + OSS-Fuzz | Parser vulnerabilities in open source libraries | Per-project configuration |

- [AI Security Code Review](./ai-security-review) — Findings-driven implementation guide and GitHub Actions example

---

## Stage 5: Continuous Monitoring & Auto-remediation (Continuous & Auto-remediation)

At this stage, SBOM is continuously scanned even after deployment, and patch PRs are generated automatically when new CVEs are discovered. Integration with Dependabot and Renovate maintains centralized supply chain security compliance (ISO/IEC 18974). Human intervention for policy compliance is minimized, creating a virtuous cycle that continuously controls AI-induced risk through automation.

- [Continuous Monitoring & Auto-remediation](/devsecops/monitoring)
- [DAST — Dynamic Analysis](/devsecops/dast)

---

## Where should our team start?

:::tip Stage selection guide
:::

If you are developing alone or running a small-scale experiment, starting from Stage 2 is recommended. Setup can be completed within 10 minutes at no extra cost.

If your team already uses GitHub Actions, try Stage 3 Quick CI/CD first. You can build a basic security gate in 30 minutes.

If you are operating Stage 3 stably, add the Stage 4 AI defense layer. A single `ANTHROPIC_API_KEY` can activate both findings-driven review and AI fuzzing.

If you already operate up to Stage 4 and have a dedicated security team, review Stage 5 and the full DevSecOps guide to raise organization-wide supply chain security maturity.
