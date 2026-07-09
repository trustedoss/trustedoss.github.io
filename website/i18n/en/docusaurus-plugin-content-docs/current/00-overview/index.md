---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 1 hour
slug: /
---

# Before you start

70-80% of modern software is open source. Using open source means taking on three responsibilities: fulfilling licensing obligations, tracking security vulnerabilities, and ensuring supply chain transparency.

Taking on this responsibility without a management system invites trouble: product shipments halted by a missed GPL obligation, incidents like Log4Shell where you cannot even determine the scope of impact without an SBOM, or being unable to deliver an SBOM as required by the EU Cyber Resilience Act or customer procurement contracts.

This kit is designed to help **people with no open source management experience** build a system from start to finish. A Claude Code agent asks about your company's situation and automatically generates the policy, organization, process, SBOM, training, and certification outputs. ISO/IEC 5230 (license compliance) and ISO/IEC 18974 (security assurance) share a common foundation, so building both at once cuts duplicate work by about 35%.

---

## 1. What this chapter covers

Even if today is your first day as an open source lead, you can complete the ISO/IEC 5230 and ISO/IEC 18974 self-certification declarations by following this kit. This chapter lays out the purpose and structure of the entire journey.

- The agent automatically generates **23 deliverables** tailored to your company's situation.
- **Achieve both standards at once** (about 35% savings from the shared foundation)

### Quick start

```bash
git clone https://github.com/trustedoss/trustedoss.github.io.git
cd trustedoss.github.io && claude
# Type "Where should I start?"
```

### Full chapter list

| Chapter                                              | Content                                                                                                                                                                            |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [00 Getting started](./index.md)                     | Background, checklist mapping, software supply chain security, and SBOM concepts                                                                                                   |
| [01 Environment preparation](../01-setup/index.md)   | Install Docker, Git, and Claude Code                                                                                                                                               |
| [02 Organization](../02-organization/index.md)       | Organizational structure and personnel assignment                                                                                                                                  |
| [03 Policy](../03-policy/index.md)                   | Establish an open source policy                                                                                                                                                    |
| [04 Process](../04-process/index.md)                 | Design open source processes                                                                                                                                                       |
| 05 Tools                                             | · [Create SBOM](../05-tools/sbom-generation/index.md) <br /> · [SBOM management](../05-tools/sbom-management/index.md) <br />· [Vulnerability](../05-tools/vulnerability/index.md) |
| [06 Training](../06-training/index.md)               | Build a training program                                                                                                                                                           |
| [07 Certification](../07-conformance/index.md)       | Self-certification declaration                                                                                                                                                     |
| [08 Developer Guide](../08-developer-guide/index.md) | Automatic policy compliance with Claude Code (optional)                                                                                                                            |

### Deliverables upon completion

| Step            | Output file                                                                                                                                     | Related standards |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| organization    | `role-definition.md`, `raci-matrix.md`, `appointment-template.md` — [See example](/reference/samples/organization)                              | [Common]          |
| policy          | `oss-policy.md`, `license-allowlist.md` — [See example](/reference/samples/policy)                                                              | [Common]          |
| process         | `usage-approval.md`, `distribution-checklist.md`, `vulnerability-response.md`, `process-diagram.md` — [See example](/reference/samples/process) | [Common]          |
| create SBOM     | `[project].cdx.json`, `sbom-commands.sh`, `license-report.md`, `copyleft-risk.md` — [See example](/reference/samples/sbom)                      | [Common]          |
| SBOM management | `sbom-management-plan.md`, `sbom-sharing-template.md` — [See example](/reference/samples/sbom)                                                  | [Supply Chain]    |
| vulnerability   | `cve-report.md`, `remediation-plan.md` — [See example](/reference/samples/vulnerability)                                                        | [18974]           |
| Training        | `curriculum.md`, `completion-tracker.md`, `resources.md` — [See example](/reference/samples/training)                                           | [Common]          |
| Certification   | `gap-analysis.md`, `declaration-draft.md`, `submission-guide.md` — [See example](/reference/samples/conformance)                                | [Common]          |

---

## 2. Background knowledge

### Comparing the two standards

| Item          | ISO/IEC 5230                                               | ISO/IEC 18974                                                            |
| ------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------ |
| Official name | OpenChain License Compliance                               | OpenChain Security Assurance                                             |
| Purpose       | Establish an open source license compliance system         | Establish an open source security vulnerability assurance system         |
| Origin        | Response to the rapid rise in open source license disputes | Response to supply chain security incidents such as SolarWinds·Log4Shell |

:::tip
The full comparison — including version, focus, core requirements, authentication method, validity period, related regulations, and mutual complementarity — is canonical in [Standard requirements at a glance](./checklist-mapping.md).
:::

### What is self-certification?

Both standards use **self-certification**. You make the declaration directly on the OpenChain website, with no audit by an external review body.

- **Difference from third-party certification**: There is no external audit cost or schedule; the organization itself declares that it meets the requirements.
- **Legal and practical implications**: Your open source management maturity is shared transparently with supply chain partners and can serve as evidence of compliance at delivery time.
- **What you can do after certification**: Use the OpenChain certification logo, demonstrate supply chain transparency, and respond to customer audits with greater credibility.

### How to read `checklist-mapping.md`

`docs/00-overview/checklist-mapping.md` is a map that organizes all 31 requirements of the two standards into a single table.

**Item ID scheme:**

| Prefix | Meaning                                             |
| ------ | --------------------------------------------------- |
| G1     | Program foundation (policy, organization, training) |
| G2     | Defining related tasks (roles, channels, awareness) |
| G3-L   | License compliance (ISO/IEC 5230 focus)             |
| G3-S   | Security assurance (ISO/IEC 18974 focus)            |
| G3-B   | SBOM and supply chain (common)                      |
| G4     | Declaring and maintaining compliance                |

**Key insight:** Of the 31 items, 11 are common to both standards. By completing those 11 common items first, you satisfy a large share of both standards at once and save roughly 35% of the duplicate work. The kit is designed to prioritize the common items.

---

## 3. Self-study

:::info Self-study mode (about 1 hour)
Take your time to understand and work through each document on your own. We recommend 3-5 days to complete the entire kit.
:::

1. Read this page (`index.md`) — get an overview of the whole journey
2. Read `checklist-mapping.md` — understand the structure of all 31 items
3. Read `supply-chain.md` — build background on software supply chain security
4. Go to `docs/01-setup/` — start preparing your environment

---

## 4. Completion checklist

- [ ] I can explain the differences and similarities between the two standards (ISO/IEC 5230 and ISO/IEC 18974)
- [ ] I understand the G1-G4 item ID system in `checklist-mapping.md`
- [ ] I understand that the 10 common items satisfy both standards at once
- [ ] I have confirmed my self-study route
- [ ] I am ready to move to the next step (learn supply chain security, or go to chapter `01`)

---

## 5. Next steps

**If you want some background first:**
→ Learn the basics of software supply chain security and SBOM by reading [Software Supply Chain Security: Why It Matters Now](./supply-chain.md) and [SBOM Basics: Introduction to Software Composition Specifications](./sbom-101.md).

**If you want to start preparing your environment right away:**
→ Go to [Prepare the environment: install the tools needed for the labs](../01-setup/index.md) to install the tools and set things up.

---

## Related links

- [OpenChain KWG](https://openchain-project.github.io/OpenChain-KWG/)
- [ISO/IEC 5230](https://www.iso.org/standard/81039.html)
- [ISO/IEC 18974](https://www.iso.org/standard/86450.html)
- [OpenChain self-certification registration](https://www.openchainproject.org/conformance)
