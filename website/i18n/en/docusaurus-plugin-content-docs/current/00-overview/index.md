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

If you take on this responsibility without a management system, problems will arise. Product distribution is halted due to missing the GPL license, incidents like Log4Shell where the scope of impact cannot even be identified without SBOM, or situations in which SBOM cannot be submitted to customers in response to regulations such as the EU Cyber ​​Resilience Act and US EO 14028 occur.

This kit is designed to help **persons with no open source management experience** build a system from start to finish. Claude Code Agent directly asks about the company's situation and automatically creates policy, organization, process, SBOM, training, and certification outputs. ISO/IEC 5230 (license compliance) and ISO/IEC 18974 (security assurance) establish a common foundation for both standards, reducing duplicate work by 40%.

---

## 1. What we do in this chapter

Even if you become an open source representative for the first time today, you can complete ISO/IEC 5230 and ISO/IEC 18974 self-certification declarations by following this kit. This chapter identifies the purpose and structure of the entire journey.

- Agent automatically creates **23 deliverables** that fit the company’s situation.
- **Achieve both standards simultaneously** (40% savings on common basis)

### quick start

```bash
git clone https://github.com/trustedoss/trustedoss.github.io.git
cd trustedoss.github.io && claude
# "어디서 시작해야 해?" 입력
```

### full chapter

| Chapter                                              | Content                                                                                                                                                                            |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [00 Getting started](./index.md)                     | Background, Checklist Mapping, Software Supply Chain Security + SBOM Concepts                                                                                                      |
| [01 Environment preparation](../01-setup/index.md)   | Install Docker, Git, Claude Code                                                                                                                                                   |
| [02 Organization](../02-organization/index.md)       | Organizational structure and designation of personnel                                                                                                                              |
| [03 policy](../03-policy/index.md)                   | Establishment of open source policy                                                                                                                                                |
| [04 Process](../04-process/index.md)                 | Open source process design                                                                                                                                                         |
| 05 Tools                                             | · [Create SBOM](../05-tools/sbom-generation/index.md) <br /> · [SBOM Management](../05-tools/sbom-management/index.md) <br />· [vulnerability](../05-tools/vulnerability/index.md) |
| [06 Education](../06-training/index.md)              | Building an education system                                                                                                                                                       |
| [07 Certification](../07-conformance/index.md)       | Self-certification declaration                                                                                                                                                     |
| [08 Developer Guide](../08-developer-guide/index.md) | Automatic policy compliance with Claude Code (optional)                                                                                                                            |

### Deliverables upon completion

| steps           | output file                                                                                                                                     | Related standards |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| organization    | `role-definition.md`, `raci-matrix.md`, `appointment-template.md` — [See example](/reference/samples/organization)                              | [Common]          |
| policy          | `oss-policy.md`, `license-allowlist.md` — [See example](/reference/samples/policy)                                                              | [Common]          |
| process         | `usage-approval.md`, `distribution-checklist.md`, `vulnerability-response.md`, `process-diagram.md` — [See example](/reference/samples/process) | [Common]          |
| create SBOM     | `[project].cdx.json`, `sbom-commands.sh`, `license-report.md`, `copyleft-risk.md` — [See example](/reference/samples/sbom)                      | [Common]          |
| SBOM Management | `sbom-management-plan.md`, `sbom-sharing-template.md` — [See example](/reference/samples/sbom)                                                  | [Supply Chain]    |
| vulnerability   | `cve-report.md`, `remediation-plan.md` — [See example](/reference/samples/vulnerability)                                                        | [18974]           |
| Education       | `curriculum.md`, `completion-tracker.md`, `resources.md` — [See example](/reference/samples/training)                                           | [Common]          |
| Certification   | `gap-analysis.md`, `declaration-draft.md`, `submission-guide.md` — [See example](/reference/samples/conformance)                                | [Common]          |

---

## 2. Background knowledge

### Compare two standards

| Item                  | ISO/IEC 5230                                                                                 | ISO/IEC 18974                                                                            |
| --------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Official name         | OpenChain License Compliance                                                                 | OpenChain Security Assurance                                                             |
| Latest version        | 2.1 (2023)                                                                                   | 1.0 (2023)                                                                               |
| Purpose               | Establishment of an open source license compliance system                                    | Establishment of an open source security vulnerability assurance system                  |
| focus                 | Fulfillment of license obligations, BOM management                                           | Identifying, tracking and responding to known CVEs, SBOM based security                  |
| Core Requirements     | Policy·Organization·Process·BOM·Compliance Output·Contribution Policy·Compliance Declaration | Policy·Organization·SBOM·CVE Scan·vulnerability Tracking·Response·Compliance Declaration |
| Authentication method | OpenChain Website self-declaration                                                           | OpenChain Website self-declaration                                                       |
| enactment background  | Response to rapid increase in open source licensing disputes                                 | Response to supply chain security incidents such as SolarWinds·Log4Shell                 |

> For detailed comparison of items such as validity period, related regulations, and mutual complementarity, refer to [`checklist-mapping.md`](./checklist-mapping.md).

### What is self-certification?

Both standards are **Self-Certification**. The declaration is made directly on the OpenChain website without any audit by an external review body.

- **Difference from third-party certification**: There is no external audit cost or schedule, and the organization itself declares that it meets the requirements.
- **Legal and practical implications**: Open source management level is transparently provided to supply chain partners, and can be used as evidence of compliance when delivering.
- **What you can do after certification**: OpenChain Use the certification logo, prove supply chain transparency, and improve reliability when responding to customer audits.

### How to view `checklist-mapping.md`

`docs/00-overview/checklist-mapping.md` is a map that organizes all 25 requirements of the two standards in one table.

**Item ID Scheme:**

| prefix | meaning                                                  |
| ------ | -------------------------------------------------------- |
| G1     | Program-based (policy, organization, education)          |
| G2     | Definition of related tasks (role, channel, recognition) |
| G3-L   | License compliance (ISO/IEC 5230 focused)                |
| G3-S   | Security assurance (ISO/IEC 18974 focused)               |
| G3-B   | SBOM and supply chain (common)                           |
| G4     | Declaration of Compliance and Maintenance                |

**Key Insight:** Among the 25 items, 10 are common. Completing the 10 common items first will meet 40% of both standards simultaneously, saving approximately 40% of duplicate work. The kit is designed to prioritize common items.

---

## 3. Self-study

:::info Self-study mode (about 1 hour)
Take enough time on your own to understand and proceed with each document. We recommend 3-5 days to complete the entire kit.
:::

1. Read this article (`index.md`) — Get an overview of your entire journey
2. Reading `checklist-mapping.md` — Understand the structure of all 25 items
3. Read `supply-chain.md` — Gain background in software supply chain security.
4. Go to `docs/01-setup/` — Start preparing your environment

---

## 4. Completion Confirmation Checklist

- [ ] Can explain the differences and similarities between the two standards (ISO/IEC 5230, ISO/IEC 18974)
- [ ] I figured out the G1~G4 item ID system of `checklist-mapping.md`
- [ ] It was understood that the 10 common items meet both standards simultaneously
- [ ] Confirmed the self-study route
- [ ] You are ready to move to the next step (Learn Supply Chain Security or Chapter `01`)

---

## 5. Next steps guidance

**If you need some background:**
→ First learn software supply chain security and SBOM concepts by reading [Software Supply Chain Security: Why It Matters Now](./supply-chain.md) and [SBOM Basics: Introduction to Software Composition Specifications](./sbom-101.md).

**To start preparing your environment right away:**
→ Go to [Prepare the environment: Install the tools needed for the lab](../01-setup/index.md) to install tools and set up the environment.

---

## Related Links

- [OpenChain KWG](https://openchain-project.github.io/OpenChain-KWG/)
- [ISO/IEC 5230](https://www.iso.org/standard/81039.html)
- [ISO/IEC 18974](https://www.iso.org/standard/86450.html)
- [OpenChain self-authentication registration](https://www.openchainproject.org/conformance)
