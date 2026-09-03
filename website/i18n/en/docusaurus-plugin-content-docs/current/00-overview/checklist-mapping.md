---
id: checklist-mapping
title: Integrated Requirements Checklist Mapping
sidebar_label: Standard requirements at a glance
sidebar_position: 3
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: Full (mapping reference document)'
  - 'ISO/IEC 18974: Full (mapping reference document)'
self_study_time: 15 minutes
---

# Integrated Requirements Checklist Mapping

This document summarizes **what ISO/IEC 5230 (license compliance) and ISO/IEC 18974 (security assurance) require, on a single screen**. The self-certification question, verification material, and deliverable file for each individual item live in the [Requirements Detail Matrix](/reference/requirements-matrix). You use that matrix at the [self-certification](../07-conformance/index.md) stage to check gap analysis results; for now the three sections below are all you need.

## Comparing the two standards

| Item                     | ISO/IEC 5230                                                                               | ISO/IEC 18974                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| **Official name**        | OpenChain License Compliance                                                               | OpenChain Security Assurance                                                              |
| **Current edition**      | ISO/IEC 5230:2020 (OpenChain spec 2.1)                                                     | ISO/IEC 18974:2023                                                                        |
| **Purpose**              | Establish an open source license compliance program                                        | Establish an open source security vulnerability assurance program                         |
| **Focus**                | Meeting license obligations, BOM management, notice generation                             | Identifying, tracking, and responding to known CVEs; SBOM-based security                  |
| **Main requirements**    | Policy, organization, process, BOM, compliance artifacts, contribution policy, declaration | Policy, organization, SBOM, CVE scanning, vulnerability tracking and scoring, declaration |
| **Certification method** | Self-declaration on the OpenChain website                                                  | Self-declaration on the OpenChain website                                                 |
| **Validity period**      | 18 months                                                                                  | 18 months                                                                                 |
| **Related regulations**  | SPDX, REUSE, EU CRA (license side)                                                         | EO 14028, CISA SBOM minimum elements, EU CRA, NVD/CVSS                                    |
| **Complementarity**      | Shares the common base (policy, organization, SBOM) and adds license-specific items        | Shares the common base and adds security-specific items                                   |

:::info[Key insight]
The two standards share a common base across policy, organization, training, and SBOM. Building one automatically satisfies about half of the other.
:::

## The four groups of requirements

All 31 requirements fall into the groups below. Each group has a chapter that fills it, so working through the chapters in order fills the requirements along the way.

| Group    | What it covers                             | Chapters that fill it                                                                                                                |
| -------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| **G1**   | Program foundation (policy, org, training) | [02 Organization](../02-organization/index.md), [03 Policy](../03-policy/index.md), [06 Training](../06-training/index.md)           |
| **G2**   | Scoped tasks (roles, channels, awareness)  | [02 Organization](../02-organization/index.md), [04 Process](../04-process/index.md)                                                 |
| **G3-L** | License compliance (5230 focused)          | [03 Policy](../03-policy/index.md), [04 Process](../04-process/index.md), [05 SBOM generation](../05-tools/sbom-generation/index.md) |
| **G3-S** | Security assurance (18974 focused)         | [04 Process](../04-process/index.md), [05 Vulnerability](../05-tools/vulnerability/index.md)                                         |
| **G3-B** | SBOM and supply chain (common)             | [05 SBOM generation](../05-tools/sbom-generation/index.md), [05 SBOM management](../05-tools/sbom-management/index.md)               |
| **G4**   | Conformance declaration and maintenance    | [07 Conformance](../07-conformance/index.md)                                                                                         |

## Why do both standards together

| Category                   | Number of items |
| -------------------------- | --------------- |
| ISO/IEC 5230 mapped items  | 20              |
| ISO/IEC 18974 mapped items | 23              |
| Items common to both       | 12              |
| **Total number of items**  | **31**          |

The 12 common items are counted in both the 5230 total (20) and the 18974 total (23). Preparing both standards at once means doing those 12 only once, saving roughly 39% (12/31). That is why this kit's chapter order handles the common items first.

**Source basis**: For the original standard commentary and templates behind each item, see the OpenChain KWG (CC BY 4.0)
[Enterprise Open Source Guide](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/)
and [policy and process templates](https://openchain-project.github.io/OpenChain-KWG/guide/templates/).
This mapping's chapter and deliverable structure is reworked from that guide.

## Next steps

Once you have this much, move on to [Environment setup](../01-setup/index.md) to install the tools, then start producing deliverables from [Organization structure](../02-organization/index.md).

The point where you need the per-item certification questions and verification material is the [self-certification](../07-conformance/index.md) chapter. At that point, open the [Requirements Detail Matrix](/reference/requirements-matrix) and check it against your gap analysis results.
