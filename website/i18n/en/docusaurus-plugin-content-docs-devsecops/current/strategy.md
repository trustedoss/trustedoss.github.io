---
id: strategy
title: DevSecOps Introduction Strategy
sidebar_label: Introduction Strategy
sidebar_position: 2
---

# DevSecOps Introduction Strategy

## What is DevSecOps?

A culture and methodology that integrates development (Dev), security (Sec), and operations (Ops) to build security into the entire software development lifecycle. The core idea is to block threats early with automated checks from the moment code is written, rather than treating security as something to handle later.

---

## Shift Left — Why faster is better

:::info The cost of fixing a vulnerability can vary by orders of magnitude depending on when it is discovered.
:::

The earlier a vulnerability is found in the code-writing stage, the more the cost and time to fix it drop exponentially.

| When discovered               | Relative fix cost | Responsible               |
| ----------------------------- | ----------------- | ------------------------- |
| Writing code (IDE·pre-commit) | 1x                | The developer             |
| PR · code review (CI)         | 10x               | Developer · reviewer      |
| Staging · QA                  | 25x               | QA · DevOps               |
| After production deployment   | 100x              | All teams · security team |

The goal of DevSecOps is to shift as many checks as possible to the left (the code-writing stage).

---

## Maturity Model — Stage 4

| Stage   | Level        | Characteristics                          | Main tools              |
| ------- | ------------ | ---------------------------------------- | ----------------------- |
| Stage 1 | None         | Security checks manual or absent         | —                       |
| Stage 2 | Basic        | CI automation in key areas               | Gitleaks, grype         |
| Stage 3 | Systematized | Pipeline integration across all areas    | Semgrep, Trivy, Checkov |
| Stage 4 | Optimized    | Auto-remediation · continuous monitoring | Dependabot + AI         |

For most teams, it is realistic to start at Stage 2 and move to Stage 3 over 6 to 12 months.

---

## Step-by-step introduction roadmap

:::tip Don't try to adopt everything at once
Stabilizing one area at a time before moving to the next is the sustainable way to avoid team fatigue.
:::

1. **Start immediately (1-2 weeks)**
   Begin with secret detection (Gitleaks) and basic SCA (grype). The setup is simple and the effect is immediate. This blocks secret leaks and critical vulnerabilities in the existing codebase.

2. **Strengthen code quality (1 month)**
   Add SAST (Semgrep). Choose a ruleset that matches the languages your team uses; initially emit warnings only, then switch to blocking builds after 2-4 weeks.

3. **Build and infrastructure security (2-3 months)**
   Add container security (Trivy) and IaC security (Checkov). This applies to teams that use container or cloud environments.

4. **Complete dynamic analysis and automation (3-6 months)**
   Add DAST (OWASP ZAP). After integrating all areas of the pipeline, establish a monitoring and auto-remediation system.

---

## Location in the pipeline

| Area               | pre-commit | PR/CI | Build | After deployment |
| ------------------ | ---------- | ----- | ----- | ---------------- |
| Secret Detection   | ✓          | ✓     | —     | —                |
| SAST               | —          | ✓     | —     | —                |
| SCA                | —          | ✓     | ✓     | ✓                |
| Container Security | —          | —     | ✓     | ✓                |
| IaC Security       | —          | ✓     | —     | —                |
| DAST               | —          | —     | —     | ✓                |

---

## Self-study — step-by-step agent

:::tip Automate each stage with a Claude Code agent
Run the agents below in order to actually implement
Stages 1-4 from the strategy page.
:::

**Prerequisite**: Clone the [Trusted OSS repository](https://github.com/trustedoss/trustedoss-agents)

| Stage                              | agent                | Command                                               |
| ---------------------------------- | -------------------- | ----------------------------------------------------- |
| Stage 2 — Internalize the AI rules | ai-coding-setup      | `cd agents/ai-coding-setup && claude`                 |
| Stage 3 — CI/CD pipeline           | devsecops-setup      | `cd agents/devsecops-setup && claude`                 |
| Stage 3 — PR auto-comment          | level2-pr-comment    | `cd agents/level2-automation/pr-comment && claude`    |
| Stage 5 — Continuous monitoring    | level2-issue-tracker | `cd agents/level2-automation/issue-tracker && claude` |

---

## Next steps

- To start immediately: [Secret Detection](./secret-detection), [SCA](./sca)
- From code security: [SAST](./sast)
- Entire pipeline design: [Pipeline design](./pipeline-design)
