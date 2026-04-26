---
id: strategy
title: DevSecOps Introduction Strategy
sidebar_label: Introduction Strategy
sidebar_position: 2
---

# DevSecOps Introduction Strategy

## What is DevSecOps?

It is a culture and methodology that integrates development (Dev), security (Sec), and operations (Ops) to internalize security throughout the software development life cycle. The key is to block threats early with automated inspection from the time code is written, rather than “security comes later.”

---

## Shift Left — Why faster is better

:::info The cost of fixing a vulnerability varies dozens of times depending on when it is discovered.
:::

As vulnerabilities are discovered at the code writing stage, the cost and time to fix them decreases exponentially.

| When discovered               | relative cost of correction | Contact person          |
| ----------------------------- | --------------------------- | ----------------------- |
| Writing code (IDE·pre-commit) | 1x                          | Developer himself       |
| PR/Code Review (CI)           | 10x                         | Developer/Reviewer      |
| Staging·QA                    | 25x                         | QA/DevOps               |
| After production deployment   | 100x                        | All Teams/Security Team |

The goal of DevSecOps is to move as many checks to the left (code writing phase) as possible.

---

## Maturity Model — Stage 4

| steps  | level           | Features                                    | Main tools              |
| ------ | --------------- | ------------------------------------------- | ----------------------- |
| Step 1 | None            | Security check manual or absent             | —                       |
| Step 2 | Basic           | Key Areas CI Automation                     | Gitleaks, grype         |
| Step 3 | Systematization | Full-area pipeline integration              | Semgrep, Trivy, Checkov |
| Step 4 | Optimization    | Automatic calibration/continuous monitoring | Dependabot + AI         |

For most teams, it is realistic to start in Stage 2 and move to Stage 3 over 6 to 12 months.

---

## Step-by-step introduction roadmap

:::tip Don’t try to introduce everything at once
Stabilizing one area at a time and then moving on to the next is a sustainable way to avoid team fatigue.
:::

1. **Start Immediately (1-2 Weeks)**
   Secret detection (Gitleaks) + SCA is applied starting from basic (grype). The setup is simple and the effects are immediate. Blocks secret leaks and critical vulnerabilities in the existing code base.

2. **Improvement of code quality (1 month)**
   Add SAST(Semgrep). Choose a ruleset that matches the language your team uses, and initially print only a warning, then switch to block builds after 2-4 weeks.

3. **Build/Infrastructure Security (2~3 months)**
   Add container security (Trivy) + IaC security (Checkov). Applies to teams that use container/cloud environments.

4. **Completion of dynamic analysis and automation (3-6 months)**
   Add DAST(OWASP ZAP). After integrating all areas of the pipeline, a monitoring and automatic correction system is established.

---

## Location in the pipeline

| area               | pre-commit | PR/CI | build | After Deployment |
| ------------------ | ---------- | ----- | ----- | ---------------- |
| Secret Detection   | ✓          | ✓     | —     | —                |
| SAST               | —          | ✓     | —     | —                |
| SCA                | —          | ✓     | ✓     | ✓                |
| Container Security | —          | —     | ✓     | ✓                |
| IaC security       | —          | ✓     | —     | —                |
| DAST               | —          | —     | —     | ✓                |

---

## Self-study — step-by-step agent

:::tip Automate each step with Claude Code agent
If you run the agents below in order,
You can actually implement steps 1-4 on the strategy page.
:::

**Prerequisite**: Requires clone of [Trusted OSS repository](https://github.com/trustedoss/trustedoss.github.io)

| steps                             | agent                | command                                               |
| --------------------------------- | -------------------- | ----------------------------------------------------- |
| Step 2 — Internalize the AI rules | ai-coding-setup      | `cd agents/ai-coding-setup && claude`                 |
| Step 3 — CI/CD Pipeline           | devsecops-setup      | `cd agents/devsecops-setup && claude`                 |
| Step 3 — PR Auto Comment          | level2-pr-comment    | `cd agents/level2-automation/pr-comment && claude`    |
| Step 4 — Continuous monitoring    | level2-issue-tracker | `cd agents/level2-automation/issue-tracker && claude` |

---

## Next steps

- To start immediately: [Secret Detection](./secret-detection), [SCA](./sca)
- From code security: [SAST](./sast)
- Entire pipeline design: [Pipeline design](./pipeline-design)
