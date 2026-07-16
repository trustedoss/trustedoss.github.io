---
id: 08-developer-guide
title: 'Developer Guide: Automatic Open Source Policy Compliance in Claude Code'
sidebar_label: Developer Guide (Optional)
sidebar_position: 8
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: (Optional chapter - no mandatory items, supports G1.6 operational reinforcement)'
  - 'ISO/IEC 18974: (Optional chapter - no mandatory items, supports G3S.1 operational reinforcement)'
self_study_time: 2 hours
---

# Developer Guide: Automatic Open Source Policy Compliance in Claude Code

## 1. What we do in this chapter

With chapters 01–07, your open source management system is complete.
The remaining task is **making sure the policy is followed automatically in day-to-day development**.

Having the program manager review every PR is not sustainable.
This chapter explains four ways to use Claude Code so that **developers comply with the policy without thinking about it**.

:::info Goal
Claude Code keeps the policy for you, even when the program manager does not review every change — reaching this state is the goal of this chapter.
:::

:::note This chapter vs. the AI coding Rules template
This chapter shows four ways to automatically apply **the organizational policy you built earlier** (`output/policy/`) to daily development.
If you have not created a policy yet and just want a quick Rules file for AI coding tools, use the [Common Rules Template](/ai-coding/rules-template).
:::

## 2. Background: Why automation is needed

:::tip
If SBOM and license terminology is unfamiliar, see the [Glossary](/reference/glossary).
:::

### Problems that actually happen

**Scenario 1: A GPL package is added without thinking**
A developer finds a convenient utility library.
They run `npm install some-gpl-utility` and open a PR.
Until the program manager reviews it, the risk of GPL contamination remains hidden.
If it is discovered after distribution, a source code disclosure obligation may arise.

**Scenario 2: A vulnerable version stays in use**
An old version keeps being used without dependency updates.
A Critical vulnerability with CVSS 9.0 is disclosed, but the team is unaware of it.
When a security incident occurs, "we didn't know" is not an acceptable excuse.

**Scenario 3: A policy violation the program manager never sees**
A package with a license not on the approved license list (`license-allowlist.md`) is added.
It is distributed without going through the usage approval process (`usage-approval.md`).
The violation is only discovered at certification renewal time.

### Guiding principle

Do not rely on developers' **memory and willpower** for policy compliance.
Make tools and automation the **default**.

## 3. Overview of the four methods

Apply a combination of the four methods below. The higher the level of assurance, the higher the implementation complexity.

| Method                          | Description                                                              | Assurance level | Implementation difficulty |
| ------------------------------- | ------------------------------------------------------------------------ | --------------- | ------------------------- |
| **Policy in CLAUDE.md**         | Tell Claude Code directly which policies to follow                       | 70%             | Very easy                 |
| **Skill definition**            | Turn the license and vulnerability check procedure into a reusable skill | 80%             | Easy                      |
| **Automatic checks with Hooks** | Automatically raise a warning whenever a dependency file changes         | 90%             | Moderate                  |
| **CI/CD pipeline**              | Automatic checks on every PR; merges are blocked on violations           | 99%             | Somewhat complex          |

:::info[Core principle]
For complete assurance, apply all four methods. Each method works independently, but the more you combine them, the lower the risk of anything slipping through.
:::

## 4. Detailed guide to each method

We recommend starting with the easiest method 1 and reinforcing it with methods 3 and 4. Below is a summary of the key examples; the full explanation is in each linked document.

### Method 1 — State the policy in CLAUDE.md (70% assurance, very easy)

Write the allowed and prohibited licenses and the package addition procedure in the project root `CLAUDE.md`, and Claude Code will automatically consult this policy whenever it helps add a package.

```markdown
## Open Source Policy (automatic compliance)

### Prohibited licenses

- GPL-2.0, GPL-3.0, AGPL-3.0 (Copyleft — source code disclosure obligation)
- Full allowlist: see output/policy/license-allowlist.md
```

- Effect: Claude Code is aware of the policy and warns you on violations.
- Limitation: if a developer runs `npm install` directly in the terminal, Claude Code cannot intervene.

Full example: [Method 1: Adding the Policy to CLAUDE.md](./method1-claude-md.md)

### Method 2 — Standardize checks with a Skill (80% assurance, easy)

Turn the license and vulnerability check procedure into an `/oss-policy-check` skill so anyone can run the same check with a single command.

```bash
npx license-checker --summary    # Collect licenses
grype dir:. --fail-on high       # Check vulnerabilities (fail on High or above)
```

- Effect: the check procedure is standardized into one reusable command.
- Limitation: if developers forget to run it, nothing is checked.

Full example: [Method 2: Defining a Skill](./method2-skill.md)

### Method 3 — Automatic reminders with Hooks (90% assurance, moderate)

With a Hook configured in `.claude/settings.json`, a warning is displayed automatically whenever a dependency file changes.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "... print a warning when a dependency file changes ..."
          }
        ]
      }
    ]
  }
}
```

- Effect: changes to `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, and similar files trigger an automatic reminder.
- Limitation: files modified outside Claude Code are not detected, so complement this with CI/CD.

Full example: [Method 3: Setting Up Hooks](./method3-hooks.md)

### Method 4 — Block merges with CI/CD (99% assurance, somewhat complex)

Automatically check every PR with syft and grype, and block the merge on policy violations. This guards the last gate regardless of what people or tools miss.

```yaml
on:
  pull_request:
    paths: [package.json, requirements.txt, pom.xml, go.mod]
# Generate SBOM with syft → block High or above vulnerabilities with grype --fail-on high
```

- Effect: every PR is checked, regardless of the development environment.
- Limitation: initial setup and exception management take some effort.

Full example: [Method 4: Adding a CI/CD Pipeline](./method4-cicd.md)

### Recommended combinations by situation

You do not need to adopt all four at once. Start with the combination that fits your situation.

| Situation                                      | Recommended combination | Reason                                                             |
| ---------------------------------------------- | ----------------------- | ------------------------------------------------------------------ |
| Small team of 1–2 / quick start                | Methods 1 + 3           | Lightweight setup with immediate reminders inside Claude Code      |
| Officially shipped product / external delivery | Methods 1 + 3 + 4       | CI/CD merge blocking enforces checks with nothing slipping through |
| Making the check procedure a team standard     | Above + Method 2        | Everyone runs the same check with the same command                 |

We recommend a phased rollout: apply method 1 in five minutes first to see the effect, then add enforcement with method 4 as your release frequency grows.

## 5. Detailed implementation guidance

:::info See the separate project for detailed implementation
Real implementation examples for each method, troubleshooting, and settings for various languages and build systems
will be provided in the **claude-oss-policy-guard** project.
(In preparation)
:::

This chapter provides the concepts and basic examples.
For real production deployment, exception handling, complex monorepo setups, and more,
refer to the detailed guide in the `claude-oss-policy-guard` project.

## 6. Completion check

:::info Self-study mode (about 2 hours)
Take your time and work through each step until you understand it.
:::

This chapter is complete when all items below are done.

- [ ] Open source policy section added to the project `CLAUDE.md`
- [ ] `.claude/skills/oss-policy-check/SKILL.md` created
- [ ] `/oss-policy-check` run and confirmed working
- [ ] Hook configured in `.claude/settings.json`
- [ ] Warning message confirmed when a dependency file is modified
- [ ] `.github/workflows/oss-policy-check.yml` created
- [ ] Test PR opened and the license and vulnerability checks confirmed to run automatically

## 7. Next steps

If you have completed this chapter, your open source management system has moved **beyond being built into daily operation**.

**Maintenance recommendations:**

- Renew OpenChain self-certification every 18 months (see [Self-Certification Declaration: The Final Step](../07-conformance/index.md))
- Review and update `license-allowlist.md` quarterly
- Re-scan with grype when new CVEs are published

**Going further:**

- claude-oss-policy-guard project (in preparation)
- Join the [OpenChain community](https://www.openchainproject.org/)
- Share SBOMs with supply chain partners (using `output/sbom/sbom-sharing-template.md`)
