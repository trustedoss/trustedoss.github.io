---
description: 'An overview of the full journey: build an enterprise open source management system based on ISO/IEC 5230 and 18974 step by step with AI agents, all the way to self-certification.'
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 1 hour
sidebar_label: 'Overview: the two standards and the full journey'
sidebar_position: 1
slug: /
---

# Before you start

70-80% of modern software is open source. Using open source means taking on three responsibilities: fulfilling licensing obligations, tracking security vulnerabilities, and ensuring supply chain transparency.

Taking on this responsibility without a management system invites trouble: product shipments halted by a missed GPL obligation, incidents like Log4Shell where you cannot even determine the scope of impact without an SBOM, or being unable to deliver an SBOM as required by the EU Cyber Resilience Act or customer procurement contracts.

This kit is designed to help **people with no open source management experience** build a system from start to finish. A Claude Code agent asks about your company's situation and automatically generates the policy, organization, process, <Term k="sbom">SBOM</Term>, training, and certification outputs. ISO/IEC 5230 (license compliance) and ISO/IEC 18974 (security assurance) share a common foundation, so building both at once cuts duplicate work by about 39%.

---

## 1. What this chapter covers

Even if today is your first day as an open source lead, you can complete the ISO/IEC 5230 and ISO/IEC 18974 self-certification declarations by following this kit. This chapter lays out the purpose and structure of the entire journey.

- The agent automatically generates **24 deliverables** tailored to your company's situation.
- **Achieve both standards at once** (about 39% savings from the shared foundation)

### Quick start

The labs need three things: a terminal, git, and Claude Code. Installing them and
downloading the repository is covered in one place, in
[Environment preparation: install the tools needed for the labs](../01-setup/index.md).
You can follow it from opening a terminal for the first time.

Once you are set up, run `claude` from the repository root and ask "Where should I start?".
It reads your current progress and points you to the next step.

If you would rather see the output before deciding, go to the [5-minute quick start](./quick-start.md).

### Full chapter list

| Chapter                                              | Content                                                                                                                                                                                                                                       |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [00 Getting started](./index.md)                     | Background, checklist mapping, software supply chain security, and SBOM concepts                                                                                                                                                              |
| [01 Environment preparation](../01-setup/index.md)   | Install Docker, Git, and Claude Code                                                                                                                                                                                                          |
| [02 Organization](../02-organization/index.md)       | Organizational structure and program manager assignment                                                                                                                                                                                       |
| [03 Policy](../03-policy/index.md)                   | Establish an Open Source Policy                                                                                                                                                                                                               |
| [04 Process](../04-process/index.md)                 | Design Open Source Processes                                                                                                                                                                                                                  |
| 05 Tools                                             | · [Create SBOM](../05-tools/sbom-generation/index.md) <br /> · [SBOM management](../05-tools/sbom-management/index.md) <br />· [Vulnerability](../05-tools/vulnerability/index.md) <br />· [AI SBOM](../05-tools/ai-sbom/index.md) (optional) |
| [06 Training](../06-training/index.md)               | Build a training program                                                                                                                                                                                                                      |
| [07 Certification](../07-conformance/index.md)       | Self-certification declaration                                                                                                                                                                                                                |
| [08 Developer Guide](../08-developer-guide/index.md) | Automatic policy compliance with Claude Code (optional)                                                                                                                                                                                       |

### Deliverables upon completion

| Step            | Deliverable files                                                                                                                                                      | Related standards |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| Organization    | `role-definition.md`, `raci-matrix.md`, `appointment-template.md` — [See example](/reference/samples/organization)                                                     | [Common]          |
| Policy          | `oss-policy.md`, `license-allowlist.md` — [See example](/reference/samples/policy)                                                                                     | [Common]          |
| Process         | `usage-approval.md`, `distribution-checklist.md`, `vulnerability-response.md`, `inquiry-response.md`, `process-diagram.md` — [See example](/reference/samples/process) | [Common]          |
| Create SBOM     | `[project].cdx.json`, `sbom-commands.sh`, `license-report.md`, `copyleft-risk.md` — [See example](/reference/samples/sbom)                                             | [Common]          |
| SBOM management | `sbom-management-plan.md`, `sbom-sharing-template.md` — [See example](/reference/samples/sbom)                                                                         | [Supply Chain]    |
| Vulnerability   | `cve-report.md`, `remediation-plan.md` — [See example](/reference/samples/vulnerability)                                                                               | [18974]           |
| Training        | `curriculum.md`, `completion-tracker.md`, `resources.md` — [See example](/reference/samples/training)                                                                  | [Common]          |
| Certification   | `gap-analysis.md`, `declaration-draft.md`, `submission-guide.md` — [See example](/reference/samples/conformance)                                                       | [Common]          |

Below is the 7-step journey from zero to self-certification. Check off each step as you complete it to track your progress (saved only in this browser).

<JourneyProgress />

---

## 2. Background knowledge

### Comparing the two standards

| Item          | ISO/IEC 5230                                               | ISO/IEC 18974                                                                |
| ------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Official name | OpenChain License Compliance                               | OpenChain Security Assurance                                                 |
| Purpose       | Establish an open source license compliance system         | Establish an open source security vulnerability assurance system             |
| Origin        | Response to the rapid rise in open source license disputes | Response to supply chain security incidents such as SolarWinds and Log4Shell |

:::tip
The full comparison — including version, focus, core requirements, certification method, validity period, related regulations, and mutual complementarity — is canonical in [Standard requirements at a glance](./checklist-mapping.md).
:::

### What is self-certification?

Both standards use **Self-Certification**. You make the declaration directly on the OpenChain website, with no audit by an external review body.

- **Difference from third-party certification**: There is no external audit cost or schedule; the organization itself declares that it meets the requirements.
- **Legal and practical implications**: Your open source management maturity is shared transparently with supply chain partners and can serve as evidence of compliance at delivery time.
- **What you can do after certification**: Use the OpenChain certification logo, demonstrate supply chain transparency, and respond to customer audits with greater credibility.

### How to read the requirements map

The 31 requirements across the two standards fall into six groups: program foundation (G1), defining related tasks (G2), license compliance (G3-L), security assurance (G3-S), SBOM and supply chain (G3-B), and declaring and maintaining compliance (G4). Twelve of them are common to both standards, so working through them in order saves roughly 39% of the duplicate work.

Which chapter fills which group is laid out in [Standard requirements at a glance](./checklist-mapping.md). The point where you need the certification question and verification material for each individual item is [07 Conformance](../07-conformance/index.md); that is when you open the [Requirements Detail Matrix](/reference/requirements-matrix).

---

## 3. Self-study

:::info Self-study mode (about 1 hour)
Take your time to understand and work through each document on your own. We recommend 3-5 days to complete the entire kit.
:::

1. Read this page — grasp the purpose and structure of the whole journey
2. Read [Standard requirements at a glance](./checklist-mapping.md) — grasp what the two standards require on a single screen
3. Read [Software Supply Chain Security: Why It Matters Now](./supply-chain.md) — build the background
4. Go to [Environment preparation: install the tools needed for the labs](../01-setup/index.md) — install the tools and clone the repository

---

## 4. Completion checklist

- [ ] I can explain the differences and similarities between the two standards (ISO/IEC 5230 and ISO/IEC 18974)
- [ ] I understand the G1-G4 item ID system in the requirements map
- [ ] I understand that the 12 common items satisfy both standards at once
- [ ] I have confirmed my self-study route
- [ ] I am ready to move to the next step (learn supply chain security, or go to chapter `01`)

---

## 5. Next steps

The fastest route differs depending on your goal. Choose the case closest to you below.

### Just get to self-certification quickly

This is the path of building a standards-based management system from scratch all the way to an OpenChain self-certification declaration.

Proceed in order starting from [Environment preparation](../01-setup/index.md). The core deliverables are the [Open Source Policy](../03-policy/index.md) and the [Self-certification declaration](../07-conformance/index.md). The full course takes about 12-14 hours; if you are short on time, a condensed 1-2 hour course covers just this overview, chapter 02 (organization), and chapter 03 (policy).

### All the way to automation with your dev team

This is for when you want to set up a policy and then automatically apply it to daily development and CI.

First create the [Open Source Policy](../03-policy/index.md), apply the policy to your development tools with [AI coding governance](/ai-coding/intro), and then enforce it in your CI pipeline with [DevSecOps](/devsecops/intro).

### When you already have a policy

This is for when you already have a management system in place and want to strengthen automation first.

Start from [DevSecOps adoption strategy](/devsecops/strategy) and build pipeline security gates. If you use AI coding tools, also see [AI coding governance](/ai-coding/intro).

### If you are not sure where to go

If none of the three routes obviously matches your situation, try the results first with the [5-minute quick start](./quick-start.md) and then decide. It shows you the actual shape of the deliverables with nothing to install.

If you would rather build background first, read [Software Supply Chain Security: Why It Matters Now](./supply-chain.md) and [SBOM Basics: An Introduction to the Software Bill of Materials](./sbom-101.md). Either one helps whichever route you pick.

---

## Related links

- [OpenChain KWG](https://openchain-project.github.io/OpenChain-KWG/)
- [ISO/IEC 5230](https://www.iso.org/standard/81039.html)
- [ISO/IEC 18974](https://www.iso.org/standard/86450.html)
- [OpenChain self-certification registration](https://openchainproject.org/get-started)
