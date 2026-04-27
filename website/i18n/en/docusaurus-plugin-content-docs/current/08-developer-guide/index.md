---
id: 08-developer-guide
title: 'Developer Guide:Automatic compliance with open source policies in Claude Code'
sidebar_label: Developer Guide(select)
sidebar_position: 8
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: (Optional chapter - no mandatory items, supports G1.6 operational enhancement)'
  - 'ISO/IEC 18974: (Optional chapter - no mandatory items, supports G3S.1 operational enhancement)'
self_study_time: 2 hours
---

# Developer Guide:Automatic compliance with open source policies in Claude Code

## 1. What we do in this chapter

The establishment of the open source management system was completed in Chapters 01 to 07.
The remaining task is **ensuring that the policy is automatically followed during the day-to-day development process**.

It is not sustainable for a person in charge to review every PR every time.
This chapter describes four ways to leverage the Claude Code to force developers into unconscious policy compliance.

> target:“Claude Code protects policies even if the person in charge doesn’t have to review them every time.”

## 2. Background:Why do you need automation?

### Problem situations that actually occur

**Scenario 1:Adding GPL package inadvertently**
Developers find the utility library handy.
Run `npm install some-gpl-utility` and,Raise your PR.
There is a potential risk of GPL contamination until it is reviewed by a responsible person.
If discovered after distribution, source code disclosure obligations may arise.

**Scenario 2:Use the vulnerable version as is**
Continuing to use older versions without updating dependencies.
A critical vulnerability in CVSS 9.0 has been disclosed, but the team is not aware of it.
When a security incident occurs, the excuse “I didn’t know” does not work.

**Scenario 3:Policy violation without the knowledge of the person in charge**
Allowed License List(`license-allowlist.md`)Packages with licenses that are not in are added.
Approval Process for Use(`usage-approval.md`)It is distributed without going through .
It is only at the time of certification renewal that the violation is discovered.

### Solving Principles

Policy compliance is not left to the **memory and will** of the developer.
Make tools and automation the **default**.

## 3. Solution overview

Apply a combination of the four methods below. The higher the level of coverage, the higher the complexity of implementation.

| method                           | Description                                                          | Coverage Level | Implementation Difficulty |
| -------------------------------- | -------------------------------------------------------------------- | -------------- | ------------------------- |
| **CLAUDE.md Policy Statement**   | Directly inform Claude Code of the policies to be followed           | 70%            | Very Easy                 |
| **Skill Definition**             | Make the license/vulnerability verification process a reusable skill | 80%            | Easy                      |
| **Hooks automatic verification** | Automatically generates a warning when changing dependency files     | 90%            | Normal                    |
| **CI/CD Pipeline**               | Automatic check during PR,Merge blocked in case of violation         | 99%            | somewhat complicated      |

> **Core Principles:** All four must be applied for complete coverage.
> Each method works independently, but,The more you combine, the lower the risk of omission.

## 4. Detailed guide to each method

Each method is explained in detail on its own independent page. You can select and apply only the method you need.

| method                        | document                                    |
| ----------------------------- | ------------------------------------------- |
| Method 1:Add CLAUDE.md policy | [method1-claude-md](./method1-claude-md.md) |
| Method 2:Skill definition     | [method2-skill](./method2-skill.md)         |
| Method 3:Hooks settings       | [method3-hooks](./method3-hooks.md)         |
| Method 4:CI/CD Pipeline       | [method4-cicd](./method4-cicd.md)           |

## 5. Detailed implementation guidance

:::info For detailed implementation, refer to separate project.
Actual implementation examples of each method,Troubleshooting,Settings for various languages ​​and build systems
It will be provided by the **claude-oss-policy-guard** project.
(preparing)
:::

This chapter presents concepts and basic examples.
Apply to actual production environment,Exception handling,Complex monorepo configuration, etc.
Please refer to the detailed guide of the `claude-oss-policy-guard` project.

## 6. Confirm completion

:::info Self-study mode(About 2 hours)
Take your time and understand each step.
:::

Completing all of the items below will complete this chapter.

- [ ] Completed adding open source policy section to project `CLAUDE.md`
- [ ] `.claude/skills/oss-policy-check.md` creation completed
- [ ] Run `/oss-policy-check` to check operation
- [ ] `.claude/settings.json` Hook setup complete
- [ ] Check warning message output when modifying dependency files
- [ ] `.github/workflows/oss-policy-check.yml` creation completed
- [ ] Confirm automatic execution of license/vulnerability check by uploading a test PR

## 7. Next steps

If you have completed this chapter,The open source management system has been completed beyond **construction to operation**.

**Maintenance Recommendation:**

- OpenChain self-certification renewal every 18 months([Self-certification declaration:final step](../07-conformance/index.md)reference)
- Review and update `license-allowlist.md` quarterly
- rescan grype when a new CVE occurs

**Go further:**

- claude-oss-policy-guard project(preparing)
- [OpenChain Community](https://www.openchainproject.org/)participation
- Share SBOM with supply chain partners(`output/sbom/sbom-sharing-template.md` Utilization)
