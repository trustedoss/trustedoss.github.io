---
id: checklist-mapping
title: Requirements Checklist Integrated Mapping
sidebar_label: Checklist Mapping
sidebar_position: 2
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: Full (mapping reference document)'
  - 'ISO/IEC 18974: Full (mapping reference document)'
self_study_time: 1 hour
---

# Requirements Checklist Integrated Mapping

## Purpose of this document

This document brings the self-certification checklist items of **ISO/IEC 5230** (license compliance) and **ISO/IEC 18974** (security assurance) together into a single mapping table. It serves as a compass for the whole project.

Every agent's CLAUDE.md refers to this document to produce output that meets specific standard requirements, so you can see at a glance which module produces what.

### How to read this document

1. **Comparison of the two standards** → first understand the purpose and scope of each standard
2. **Integrated mapping** → for each G1-G4 group, check the evidence, output files, and responsible agent in each item block
3. **Tags** → quickly grasp the nature of each item from `[Common]` `[5230]` `[18974]` `[Supply Chain]` `[Regulation]`
4. **Summary statistics** → see the overall status in numbers at the bottom of the document

---

## Compare two standards

| Item                              | ISO/IEC 5230                                                                                                | ISO/IEC 18974                                                                                            |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Official name**                 | OpenChain License Compliance                                                                                | OpenChain Security Assurance                                                                             |
| **Latest version**                | 2.1 (2023)                                                                                                  | 1.0 (2023)                                                                                               |
| **Purpose**                       | Establishment of an open source license compliance system                                                   | Establishment of an open source security vulnerability assurance system                                  |
| **Focus**                         | Fulfill license obligations, manage BOM, create notices                                                     | Identifying, tracking and responding to known CVEs, SBOM based security                                  |
| **Key Requirements**              | Policy, Organization, Process, BOM, Compliance Deliverables, Contribution Policy, Declaration of Compliance | Policy, Organization, SBOM, CVE Scan, vulnerability Tracking/Scoring/Response, Declaration of Compliance |
| **Authentication Method**         | OpenChain Website self-declaration                                                                          | OpenChain Website self-declaration                                                                       |
| **Validity Period**               | 18 months                                                                                                   | 18 months                                                                                                |
| **Related regulations/standards** | SPDX, REUSE, EU CRA (licensing aspect)                                                                      | EO 14028, NTIA SBOM, EU CRA, NVD/CVSS                                                                    |
| **Complementarity**               | Share common base (policy, organization, SBOM), add license-specific requirements                           | Share common base, add security-specific requirements                                                    |

> **Key Insights:** The two standards share common ground in the areas of policy, organization, education, and SBOM.
> Building one automatically fulfills half of the other.

---

## Tag notation rules

| Tag              | Meaning                                                                 |
| ---------------- | ----------------------------------------------------------------------- |
| `[Common]`       | Required by both standards                                              |
| `[5230]`         | ISO/IEC 5230 only                                                       |
| `[18974]`        | ISO/IEC 18974 only (security-specific)                                  |
| `[Supply Chain]` | Related to software supply chain security                               |
| `[Regulation]`   | Items linked to international regulations (EO 14028, EU CRA, NTIA SBOM) |

---

## Integrated mapping

### G1: Program-based

---

#### G1.1 — Establishing and documenting open source policies `[Common]`

> ISO/IEC 5230 §3.1.1 · ISO/IEC 18974 §4.1.1

Without a policy you cannot establish systematic compliance; it is the basis for every activity.

| Proof ID                       | Content                        | output file                     |
| ------------------------------ | ------------------------------ | ------------------------------- |
| 5230 §3.1.1.1 · 18974 §4.1.1.1 | Documented open source policy  | `output/policy/oss-policy.md`   |
| 5230 §3.1.1.2 · 18974 §4.1.1.2 | Policy dissemination procedure | `output/training/curriculum.md` |

- **Agent in Charge**: `03-policy-generator`

---

#### G1.2 — Establish a review process for security assurance policies `[18974]`

> ISO/IEC 18974 §4.1.1

18974 additionally requires a regular review process to keep the policy and its communication channels current.

| Proof ID       | Content                                                         | output file                          |
| -------------- | --------------------------------------------------------------- | ------------------------------------ |
| 18974 §4.1.1.1 | Documented security assurance policy (including review process) | `output/policy/oss-policy.md`        |
| 18974 §4.1.2.5 | Periodic review and evidence of change                          | `output/conformance/gap-analysis.md` |

- **Agent in Charge**: `03-policy-generator`

---

#### G1.3 — Designation of open source contact persons and organizations `[Common]`

> ISO/IEC 5230 §3.1.2 · ISO/IEC 18974 §4.1.2

Without clear ownership, decision-making stalls.

| Proof ID                       | Content                                            | output file                              |
| ------------------------------ | -------------------------------------------------- | ---------------------------------------- |
| 5230 §3.1.2.1 · 18974 §4.1.2.1 | List of Roles and Responsibilities                 | `output/organization/raci-matrix.md`     |
| 5230 §3.1.2.2 · 18974 §4.1.2.2 | Competency technical documentation for each role   | `output/organization/role-definition.md` |
| 18974 §4.1.2.3                 | Participant list and roles                         | `output/organization/role-definition.md` |
| 5230 §3.1.2.3 · 18974 §4.1.2.4 | Competency Assessment Evidence                     | `output/training/completion-tracker.md`  |
| 18974 §4.1.2.5                 | Periodic review and evidence of process changes ⚠️ | `output/conformance/gap-analysis.md`     |
| 18974 §4.1.2.6                 | Internal best practice alignment verification ⚠️   | `output/conformance/gap-analysis.md`     |

> ⚠️ **§4.1.2.5 · §4.1.2.6 at initial certification**: at first certification there is no review history, so these are treated as partially satisfied (🔶).
> Record the "review-cycle plan" and "owner assignment" in gap-analysis.md, and satisfy them with actual history at the 18-month renewal.

- **Agent in Charge**: `02-organization-designer`

---

#### G1.4 — Establishing a training program `[Common]`

> ISO/IEC 5230 §3.1.2 · ISO/IEC 18974 §4.1.2 (education and training aspects)

Building and continuously maintaining staff competency; both standards require evidence of training completion.

| Proof ID                       | Content                            | output file                             |
| ------------------------------ | ---------------------------------- | --------------------------------------- |
| 5230 §3.1.2.1 · 18974 §4.1.2.1 | List of Roles and Responsibilities | `output/organization/raci-matrix.md`    |
| 5230 §3.1.2.3 · 18974 §4.1.2.4 | Competency Assessment Evidence     | `output/training/completion-tracker.md` |

- **Agent in Charge**: `06-training-manager`

---

#### G1.5 — Program scope definition `[Common]`

> ISO/IEC 5230 §3.1.4 · ISO/IEC 18974 §4.1.4

Clarifying the target software and products enables efficient resource allocation.

| Proof ID                       | Content                                | output file                          |
| ------------------------------ | -------------------------------------- | ------------------------------------ |
| 5230 §3.1.4.1 · 18974 §4.1.4.1 | Program Scope and Limitations Document | `output/policy/oss-policy.md`        |
| 18974 §4.1.4.2                 | Performance Metrics                    | `output/policy/oss-policy.md`        |
| 18974 §4.1.4.3                 | Evidence of continuous improvement ⚠️  | `output/conformance/gap-analysis.md` |

> ⚠️ **§4.1.4.3 at initial certification**: there is no improvement history at first certification. Record the initial gap analysis itself in gap-analysis.md as a one-time audit record; by the 18-month renewal you will have at least two such records to satisfy this item.

- **Agent in Charge**: `03-policy-generator`

---

#### G1.6 — Establish procedures for review of license obligations `[5230]`

> ISO/IEC 5230 §3.1.5

Prevent license violations before distribution; covers obligations such as copyleft source-code disclosure.

| Proof ID      | Content                                                                                                  | output file                        |
| ------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| 5230 §3.1.5.1 | Procedures for reviewing and recording obligations, restrictions, and rights for each identified license | `output/process/usage-approval.md` |

- **Agent in charge**: `04-process-designer`

---

#### G1.7 — Program Participant Recognition Record `[Common]`

> ISO/IEC 5230 §3.1.3 · ISO/IEC 18974 §4.1.3

Document, per role, whether each person understands the policy, the goals, and how to contribute; this is key evidence during an audit.

| Proof ID                       | Content                                                                                                       | output file                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| 5230 §3.1.3.1 · 18974 §4.1.3.1 | Evidence assessing participant perceptions of program goals, ways to contribute, and impact of non-compliance | `output/training/completion-tracker.md` |

- **Agent in charge**: `06-training-manager`

---

### G2: Define and support relevant tasks

---

#### G2.1 — Establishing Roles and Responsibilities (RACI) `[Common]`

> ISO/IEC 5230 §3.2.2 · ISO/IEC 18974 §4.2.2

Clarify who performs, approves, and reviews open source activities; prevent gaps in ownership.

| Proof ID                       | Content                                                     | output file                                                                    |
| ------------------------------ | ----------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 5230 §3.2.2.1 · 18974 §4.2.2.1 | Role Owner/Group/Job Name Document                          | `output/organization/raci-matrix.md`                                           |
| 5230 §3.2.2.2 · 18974 §4.2.2.2 | Ensure role placement and budget adequacy                   | `output/organization/raci-matrix.md`                                           |
| 5230 §3.2.2.3                  | How to Approach License Compliance Legal Advice             | `output/organization/role-definition.md`                                       |
| 5230 §3.2.2.4 · 18974 §4.2.2.4 | Internal Responsibility Assignment Process                  | `output/organization/raci-matrix.md`                                           |
| 5230 §3.2.2.5                  | License Non-Compliance Case Review and Correction Procedure | `output/process/usage-approval.md`, `output/process/distribution-checklist.md` |
| 18974 §4.2.2.3                 | Specify available expertise to address vulnerabilities      | `output/organization/role-definition.md`                                       |

- **Agent in charge**: `02-organization-designer`

---

#### G2.2 — Operation of channels for receiving external inquiries `[Common]`

> ISO/IEC 5230 §3.2.1 · ISO/IEC 18974 §4.2.1

An official channel is required so third parties can request fulfillment of license obligations and report security vulnerabilities.

| Proof ID                       | Content                                                | output file                                                                      |
| ------------------------------ | ------------------------------------------------------ | -------------------------------------------------------------------------------- |
| 5230 §3.2.1.1 · 18974 §4.2.1.1 | Public channel for third parties to make inquiries     | `output/organization/role-definition.md`                                         |
| 5230 §3.2.1.2 · 18974 §4.2.1.2 | Internal response procedures for third party inquiries | `output/process/inquiry-response.md`, `output/process/vulnerability-response.md` |

- **Agent in charge**: `02-organization-designer`

---

#### G2.3 — Operating awareness-raising programs `[Common]`

> ISO/IEC 5230 §3.1.3 · ISO/IEC 18974 §4.1.3

Compliance is only effective when every member knows and follows the policy.

| Proof ID                       | Content                                                                                                     | output file                                                             |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 5230 §3.1.3.1 · 18974 §4.1.3.1 | Evidence of participant perception assessment (including goals, contributions and impact of non-compliance) | `output/training/resources.md`, `output/training/completion-tracker.md` |

- **Agent in charge**: `06-training-manager`

---

### G3-L: License compliance (ISO/IEC 5230 focused)

---

#### G3L.1 — License Identification and Classification `[5230]`

> ISO/IEC 5230 §3.3.1 · §3.3.2

Identify the license of each component from the SBOM; flag copyleft risk.

| Proof ID      | Content                                                                 | output file                                                     |
| ------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------- |
| 5230 §3.3.1.1 | SBOM Identification, tracking, review, approval, and storage procedures | `output/process/usage-approval.md`                              |
| 5230 §3.3.1.2 | Component Records (Proof of Procedural Compliance)                      | `output/sbom/[project].cdx.json`                                |
| 5230 §3.3.2.1 | Licensing Use Case Processing Procedure                                 | `output/sbom/license-report.md`, `output/sbom/copyleft-risk.md` |

- **Agent in Charge**: `05-sbom-analyst`

---

#### G3L.2 — Fulfillment of License Obligations `[5230]`

> ISO/IEC 5230 §3.3.2

Fulfill copyleft license obligations such as GPL, LGPL, and AGPL; maintain an allowlist of permitted licenses.

| Proof ID      | Content                                                            | output file                                                                      |
| ------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| 5230 §3.3.2.1 | License use case handling procedure for each open source component | `output/process/distribution-checklist.md`, `output/policy/license-allowlist.md` |

- **Agent in Charge**: `04-process-designer`

---

#### G3L.3 — Generate compliance artifacts `[5230]`

> ISO/IEC 5230 §3.4.1

Obligation to provide, at distribution time, the files that demonstrate fulfillment of legal obligations, such as notices and source code.

| Proof ID      | Content                                                           | output file                     |
| ------------- | ----------------------------------------------------------------- | ------------------------------- |
| 5230 §3.4.1.1 | Compliance deliverable preparation and distribution procedures    | `output/sbom/license-report.md` |
| 5230 §3.4.1.2 | Compliance deliverable storage procedures and performance records | `output/sbom/license-report.md` |

- **Agent in Charge**: `05-sbom-analyst`

---

#### G3L.4 — Establishing an open source contribution policy `[5230]`

> ISO/IEC 5230 §3.5.1

Prevents IP leakage and license-contamination risk when contributing upstream.

| Proof ID      | Content                                   | output file                     |
| ------------- | ----------------------------------------- | ------------------------------- |
| 5230 §3.5.1.1 | Open source contribution policy           | `output/policy/oss-policy.md`   |
| 5230 §3.5.1.3 | Contribution Policy Recognition Procedure | `output/training/curriculum.md` |

- **Agent in Charge**: `03-policy-generator`

---

#### G3L.5 — Process for Verifying Satisfaction of License Obligations `[5230]`

> ISO/IEC 5230 §3.4.1

Verify before distribution that all license obligations (source-code disclosure, inclusion of notices, and so on) have actually been met; acts as a release approval gate.

| Proof ID      | Content                                                           | output file                                |
| ------------- | ----------------------------------------------------------------- | ------------------------------------------ |
| 5230 §3.4.1.1 | Compliance deliverable preparation and distribution procedures    | `output/process/distribution-checklist.md` |
| 5230 §3.4.1.2 | Compliance deliverable storage procedures and performance records | `output/process/distribution-checklist.md` |

- **Agent in Charge**: `04-process-designer`

---

#### G3L.6 — Open source contribution process operation `[5230]`

> ISO/IEC 5230 §3.5.1

Concrete procedures for implementing the policy (G3L.4): the contribution review, approval, and submission workflow. Policy alone cannot govern actual contributions.

| Proof ID      | Content                                     | output file                                                                           |
| ------------- | ------------------------------------------- | ------------------------------------------------------------------------------------- |
| 5230 §3.5.1.2 | Open source contribution management process | `output/policy/oss-policy.md`, `output/process/contribution-process.md` (conditional) |

- **Agent in charge**: `03-policy-generator`, `04-process-designer` (conditional)

---

### G3-S: Security assurance (ISO/IEC 18974 focus)

---

#### G3S.1 — Identification of known vulnerabilities (CVE scan) `[18974]`

> ISO/IEC 18974 §4.3.2 · §4.1.5

Failing to identify CVEs invites security incidents and legal liability; this is an EO 14028 requirement.

| Proof ID       | Content                                                                               | output file                                |
| -------------- | ------------------------------------------------------------------------------------- | ------------------------------------------ |
| 18974 §4.1.5.1 | Standard vulnerability response procedures, including vulnerability detection methods | `output/process/vulnerability-response.md` |
| 18974 §4.3.2.1 | vulnerability detection and resolution procedures                                     | `output/vulnerability/cve-report.md`       |
| 18974 §4.3.2.2 | Record of vulnerabilities and actions taken                                           | `output/vulnerability/cve-report.md`       |

- **Agent in Charge**: `05-vulnerability-analyst`

---

#### G3S.2 — Vulnerability tracking and status management `[18974]`

> ISO/IEC 18974 §4.3.2 · §4.1.5

Continuously track identified vulnerabilities until remediation is complete; prevent items from being missed or left unattended.

| Proof ID       | Content                                                                     | output file                                |
| -------------- | --------------------------------------------------------------------------- | ------------------------------------------ |
| 18974 §4.1.5.1 | Standard response procedures, including how to follow up on vulnerabilities | `output/process/vulnerability-response.md` |
| 18974 §4.3.2.1 | vulnerability detection and resolution procedures                           | `output/vulnerability/cve-report.md`       |
| 18974 §4.3.2.2 | Record of vulnerabilities and actions taken                                 | `output/vulnerability/cve-report.md`       |

- **Agent in Charge**: `05-vulnerability-analyst`

---

#### G3S.3 — CVE Risk Score Assessment (CVSS) `[18974]`

> ISO/IEC 18974 §4.3.2

Prioritize by CVSS score; allocate resources efficiently.

| Proof ID       | Content                                                                   | output file                          |
| -------------- | ------------------------------------------------------------------------- | ------------------------------------ |
| 18974 §4.3.2.1 | vulnerability handling procedures, including risk/impact score assignment | `output/vulnerability/cve-report.md` |
| 18974 §4.3.2.2 | Record identified vulnerabilities and risk scores                         | `output/vulnerability/cve-report.md` |

- **Agent in Charge**: `05-vulnerability-analyst`

---

#### G3S.4 — Vulnerability response and patching procedures `[18974]`

> ISO/IEC 18974 §4.3.2 · §4.1.5

A system for rapidly patching, upgrading, or mitigating discovered vulnerabilities.

| Proof ID       | Content                                                                                | output file                                |
| -------------- | -------------------------------------------------------------------------------------- | ------------------------------------------ |
| 18974 §4.1.5.1 | Standard response procedures, including appropriate action methods for each risk level | `output/vulnerability/remediation-plan.md` |
| 18974 §4.3.2.1 | vulnerability remediation procedures                                                   | `output/vulnerability/remediation-plan.md` |
| 18974 §4.3.2.2 | Records of actions taken                                                               | `output/vulnerability/remediation-plan.md` |

- **Agent in Charge**: `05-vulnerability-analyst`

---

#### G3S.5 — Security artifact delivery process `[18974,supply chain]`

> ISO/IEC 18974 §4.3.1

Formal procedures for delivering security outputs such as the SBOM and CVE reports to supply chain partners and customers; addresses the EO 14028 and EU CRA disclosure obligations.

| Proof ID       | Content                                                                          | output file                            |
| -------------- | -------------------------------------------------------------------------------- | -------------------------------------- |
| 18974 §4.3.1.1 | SBOM Continuous recording procedures throughout the supplied software life cycle | `output/sbom/sbom-sharing-template.md` |
| 18974 §4.3.1.2 | Component Records (Proof of Procedural Compliance)                               | `output/sbom/[project].cdx.json`       |

- **Agent in Charge**: `05-sbom-management`

---

#### G3S.6 — Process for ensuring security obligations are met `[18974]`

> ISO/IEC 18974 §4.3.2

Procedures to verify that the response, patch, and mitigation actions for identified and tracked vulnerabilities were actually completed; confirms real implementation rather than a mere declaration.

| Proof ID       | Content                                                                     | output file                                |
| -------------- | --------------------------------------------------------------------------- | ------------------------------------------ |
| 18974 §4.3.2.1 | Procedures including verification of completion of vulnerability resolution | `output/vulnerability/remediation-plan.md` |
| 18974 §4.3.2.2 | Action Completion Record                                                    | `output/vulnerability/remediation-plan.md` |

- **Agent in charge**: `05-vulnerability-analyst`

---

### G3-B: SBOM and supply chain (common)

---

#### G3B.1 — Create an SBOM (CycloneDX/SPDX) `[Common,supply chain]`

> ISO/IEC 5230 §3.3.1 · ISO/IEC 18974 §4.3.1

The starting point for component transparency; the input for both license and security analysis.

| Proof ID                       | Content                                                                 | output file                      |
| ------------------------------ | ----------------------------------------------------------------------- | -------------------------------- |
| 5230 §3.3.1.1 · 18974 §4.3.1.1 | SBOM Identification, tracking, review, approval, and storage procedures | `output/sbom/sbom-commands.sh`   |
| 5230 §3.3.1.2 · 18974 §4.3.1.2 | Component Records (Proof of Procedural Compliance)                      | `output/sbom/[project].cdx.json` |

- **Agent in Charge**: `05-sbom-guide`

---

#### G3B.2 — SBOM management and maintenance `[Common,supply chain]`

> ISO/IEC 5230 §3.3.1 · ISO/IEC 18974 §4.3.1

Keep the SBOM current on every release and update; integrate it with configuration management.

| Proof ID                       | Content                              | output file                           |
| ------------------------------ | ------------------------------------ | ------------------------------------- |
| 5230 §3.3.1.1 · 18974 §4.3.1.1 | SBOM Life Cycle Management Procedure | `output/sbom/sbom-management-plan.md` |
| 5230 §3.3.1.2 · 18974 §4.3.1.2 | Latest component history             | `output/sbom/[project].cdx.json`      |

- **Agent in charge**: `05-sbom-management`

---

#### G3B.3 — Share the SBOM (with supply chain partners) `[Supply chain,regulation]`

> ISO/IEC 18974 §4.3.1

Transparency down the supply chain; addresses the NTIA and EU CRA supply chain disclosure obligations.

| Proof ID       | Content                                                                            | output file                            |
| -------------- | ---------------------------------------------------------------------------------- | -------------------------------------- |
| 18974 §4.3.1.1 | Life cycle recording procedures, including sharing SBOM with supply chain partners | `output/sbom/sbom-sharing-template.md` |
| 18974 §4.3.1.2 | Component History                                                                  | `output/sbom/[project].cdx.json`       |

- **Agent in charge**: `05-sbom-management`

---

#### G3B.4 — Continuous monitoring of supply chain vulnerabilities `[Supply Chain]`

> ISO/IEC 18974 §4.3.2

When a new CVE is disclosed, immediately identify which supply chain components are affected.

| Proof ID       | Content                                                                        | output file                           |
| -------------- | ------------------------------------------------------------------------------ | ------------------------------------- |
| 18974 §4.3.2.1 | Response procedures including new vulnerability analysis methods after release | `output/sbom/sbom-management-plan.md` |
| 18974 §4.3.2.2 | vulnerability and Action Log                                                   | `output/sbom/sbom-management-plan.md` |

- **Agent in Charge**: `05-sbom-management`

---

### G4: Declaring and maintaining compliance

---

#### G4.1 — ISO/IEC 5230 self-certification declaration `[5230]`

> ISO/IEC 5230 §3.6.1

Official declaration of license compliance capability; earns the trust of supply chain partners.

| Proof ID      | Content                                                                              | output file                               |
| ------------- | ------------------------------------------------------------------------------------ | ----------------------------------------- |
| 5230 §3.6.1.1 | Confirmation that the program in §3.1.4 meets all requirements of this specification | `output/conformance/declaration-draft.md` |

- **Agent in charge**: `07-conformance-preparer`

---

#### G4.2 — ISO/IEC 18974 self-certification declaration `[18974]`

> ISO/IEC 18974 §4.4.1

Official declaration of security assurance capability; evidence of EO 14028 and EU CRA compliance.

| Proof ID       | Content                                                                              | output file                               |
| -------------- | ------------------------------------------------------------------------------------ | ----------------------------------------- |
| 18974 §4.4.1.1 | Confirmation that the program in §4.1.4 meets all requirements of this specification | `output/conformance/declaration-draft.md` |

- **Agent in charge**: `07-conformance-preparer`

---

#### G4.3 — Management of certification validity period (18 months) `[Common]`

> ISO/IEC 5230 §3.6.2 · ISO/IEC 18974 §4.4.2

Both standards require re-declaration every 18 months; this avoids automatic expiration.

| Proof ID                       | Content                                                                                               | output file                              |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| 5230 §3.6.2.1 · 18974 §4.4.2.1 | Documentation confirming that all requirements have been met within 18 months of obtaining conformity | `output/conformance/submission-guide.md` |

- **Agent in charge**: `07-conformance-preparer`

---

#### G4.4 — Regular gap analysis and policy updates `[Common]`

> ISO/IEC 5230 §3.6.2 · ISO/IEC 18974 §4.4.2

Evolve the system as the technical and regulatory environment changes; required before a renewal declaration.

| Proof ID                       | Content                                                           | output file                          |
| ------------------------------ | ----------------------------------------------------------------- | ------------------------------------ |
| 5230 §3.6.2.1 · 18974 §4.4.2.1 | Document confirming re-satisfaction of requirements after renewal | `output/conformance/gap-analysis.md` |

- **Agent in Charge**: `07-conformance-preparer`

---

#### G4.5 — Verify that distributed software has no known vulnerabilities `[18974]`

> ISO/IEC 18974 §4.4.1 · §4.3.2

Before distribution, verify and declare that externally distributed software has no known vulnerabilities; a practical prerequisite for the certification declaration.

| Proof ID       | Content                                                          | output file                               |
| -------------- | ---------------------------------------------------------------- | ----------------------------------------- |
| 18974 §4.4.1.1 | Confirmation that deployment software requirements are fully met | `output/conformance/declaration-draft.md` |
| 18974 §4.3.2.2 | Record of vulnerability action completion                        | `output/vulnerability/cve-report.md`      |

- **Agent in charge**: `07-conformance-preparer`

---

## Summary Statistics

| Category                                                    | number of items |
| ----------------------------------------------------------- | --------------- |
| ISO/IEC 5230 mapping entries                                | 20              |
| ISO/IEC 18974 mapping entries                               | 23              |
| Number of items common to both standards                    | 11              |
| Number of supply chain related items (`[Supply Chain]` tag) | 5               |
| Number of regulatory linkage items (`[Regulation]` tag)     | 1               |
| **Total number of items**                                   | **31**          |

> **Note:** the common entries (11) are counted in both the 5230 total (20) and the 18974 total (23).
> Preparing both standards at once saves roughly 35% by handling the common items only once.

---

## Next steps

:::info Self-study mode (about 1 hour)
Once you understand this mapping document, start producing the actual outputs.
If the `output/` folder is empty, begin with the steps below.
:::

1. **Organization design** → `cd agents/02-organization-designer && claude`
2. **Create policy** → `cd agents/03-policy-generator && claude`
3. **Process design** → `cd agents/04-process-designer && claude`
4. **Create SBOM** → `cd agents/05-sbom-guide && claude`
5. **License analysis** → `cd agents/05-sbom-analyst && claude`
6. **Vulnerability analysis** → `cd agents/05-vulnerability-analyst && claude`
7. **SBOM management plan** → `cd agents/05-sbom-management && claude`
8. **Training program** → `cd agents/06-training-manager && claude`
9. **Certification declaration** → `cd agents/07-conformance-preparer && claude`

> This document covers the **full** ISO/IEC 5230 and **full** ISO/IEC 18974 requirements.
> It is the canonical mapping reference within the project, and each agent's CLAUDE.md refers to it.
