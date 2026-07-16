---
id: checklist-mapping
title: Integrated Requirements Checklist Mapping
sidebar_label: Standard requirements at a glance
sidebar_position: 2
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: Full (mapping reference document)'
  - 'ISO/IEC 18974: Full (mapping reference document)'
self_study_time: 1 hour
---

# Integrated Requirements Checklist Mapping

## Purpose of this document

This document brings the self-certification checklist items of ISO/IEC 5230 (license compliance) and ISO/IEC 18974 (security assurance) together into **a single mapping table**. It serves as a compass for the whole project.

Every agent's CLAUDE.md refers to this document to determine which module generates the deliverables that satisfy which standard requirements.

**Source basis**: for the original-text commentary and templates behind each item, see the OpenChain
KWG (CC BY 4.0) [Enterprise Open Source Guide](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/)
and [Policy and Process Templates](https://openchain-project.github.io/OpenChain-KWG/guide/templates/).
The chapter and deliverable structure of this mapping is reworked from those guides.

### How to read this document

1. **Comparison of the two standards** → first understand the purpose and scope of each standard
2. **Integrated mapping** → for each G1-G4 group, check the evidence, deliverable files, and responsible agent in each item block
3. **Tags** → quickly grasp the nature of each item from `[Common]` `[5230]` `[18974]` `[Supply Chain]` `[Regulation]`
4. **Summary statistics** → see the overall status in numbers at the bottom of the document

---

## Comparing the two standards

| Item                              | ISO/IEC 5230                                                                                                | ISO/IEC 18974                                                                                            |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Official name**                 | OpenChain License Compliance                                                                                | OpenChain Security Assurance                                                                             |
| **Latest version**                | 2.1 (2020)                                                                                                  | 1.0 (2023)                                                                                               |
| **Purpose**                       | Establish an open source license compliance system                                                          | Establish an open source security vulnerability assurance system                                         |
| **Focus**                         | Fulfilling license obligations, BOM management, attribution notice creation                                 | Identifying, tracking, and responding to known CVEs; SBOM-based security                                 |
| **Key requirements**              | Policy, organization, process, BOM, compliance deliverables, contribution policy, declaration of compliance | Policy, organization, SBOM, CVE scan, vulnerability tracking/scoring/response, declaration of compliance |
| **Certification method**          | Self-declaration on the OpenChain website                                                                   | Self-declaration on the OpenChain website                                                                |
| **Validity period**               | 18 months                                                                                                   | 18 months                                                                                                |
| **Related regulations/standards** | SPDX, REUSE, EU CRA (licensing aspect)                                                                      | EO 14028, NTIA SBOM, EU CRA, NVD/CVSS                                                                    |
| **Complementarity**               | Shares the common foundation (policy, organization, SBOM); adds license-specific requirements               | Shares the common foundation; adds security-specific requirements                                        |

:::info[Key insight]
The two standards share a common foundation in the areas of policy, organization, training, and SBOM. Building one automatically fulfills half of the other.
:::

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

### G1: Program foundation

---

#### G1.1 — Establishing and documenting an open source policy `[Common]`

> ISO/IEC 5230 §3.1.1 · ISO/IEC 18974 §4.1.1

Without a policy you cannot establish systematic compliance; it is the basis for every activity.

| Evidence ID                    | Content                        | Deliverable file                |
| ------------------------------ | ------------------------------ | ------------------------------- |
| 5230 §3.1.1.1 · 18974 §4.1.1.1 | Documented open source policy  | `output/policy/oss-policy.md`   |
| 5230 §3.1.1.2 · 18974 §4.1.1.2 | Policy dissemination procedure | `output/training/curriculum.md` |

- **Agent in charge**: `03-policy-generator`

---

#### G1.2 — Establishing a review process for the security assurance policy `[18974]`

> ISO/IEC 18974 §4.1.1

18974 additionally requires a regular review process to keep the policy and its communication methods current.

| Evidence ID    | Content                                                         | Deliverable file                     |
| -------------- | --------------------------------------------------------------- | ------------------------------------ |
| 18974 §4.1.1.1 | Documented security assurance policy (including review process) | `output/policy/oss-policy.md`        |
| 18974 §4.1.2.5 | Evidence of periodic review and change                          | `output/conformance/gap-analysis.md` |

- **Agent in charge**: `03-policy-generator`

---

#### G1.3 — Designating the open source Program Manager and organization `[Common]`

> ISO/IEC 5230 §3.1.2 · ISO/IEC 18974 §4.1.2

Without clear ownership, decision-making stalls.

| Evidence ID                    | Content                                                   | Deliverable file                         |
| ------------------------------ | --------------------------------------------------------- | ---------------------------------------- |
| 5230 §3.1.2.1 · 18974 §4.1.2.1 | List of roles and responsibilities                        | `output/organization/raci-matrix.md`     |
| 5230 §3.1.2.2 · 18974 §4.1.2.2 | Document describing the competencies of each role         | `output/organization/role-definition.md` |
| 18974 §4.1.2.3                 | Participant list and roles                                | `output/organization/role-definition.md` |
| 5230 §3.1.2.3 · 18974 §4.1.2.4 | Evidence of competency assessment                         | `output/training/completion-tracker.md`  |
| 18974 §4.1.2.5                 | Evidence of periodic review and process changes ⚠️        | `output/conformance/gap-analysis.md`     |
| 18974 §4.1.2.6                 | Verification of alignment with internal best practices ⚠️ | `output/conformance/gap-analysis.md`     |

:::info[§4.1.2.5 · §4.1.2.6 at initial certification]
At first certification there is no review history, so these are treated as partially satisfied. Record the review-cycle plan and owner assignment in gap-analysis.md, and satisfy them with actual history at the 18-month renewal.
:::

- **Agent in charge**: `02-organization-designer`

---

#### G1.4 — Establishing a training program `[Common]`

> ISO/IEC 5230 §3.1.2 · ISO/IEC 18974 §4.1.2 (education and training aspects)

Build and continuously maintain staff competency; both standards require evidence of training completion.

| Evidence ID                    | Content                            | Deliverable file                        |
| ------------------------------ | ---------------------------------- | --------------------------------------- |
| 5230 §3.1.2.1 · 18974 §4.1.2.1 | List of roles and responsibilities | `output/organization/raci-matrix.md`    |
| 5230 §3.1.2.3 · 18974 §4.1.2.4 | Evidence of competency assessment  | `output/training/completion-tracker.md` |

- **Agent in charge**: `06-training-manager`

---

#### G1.5 — Defining the program scope `[Common]`

> ISO/IEC 5230 §3.1.4 · ISO/IEC 18974 §4.1.4

Clarifying the target software and products enables efficient resource allocation.

| Evidence ID                    | Content                                | Deliverable file                     |
| ------------------------------ | -------------------------------------- | ------------------------------------ |
| 5230 §3.1.4.1 · 18974 §4.1.4.1 | Program scope and limitations document | `output/policy/oss-policy.md`        |
| 18974 §4.1.4.2                 | Performance metrics                    | `output/policy/oss-policy.md`        |
| 18974 §4.1.4.3                 | Evidence of continuous improvement ⚠️  | `output/conformance/gap-analysis.md` |

:::info[§4.1.4.3 at initial certification]
There is no improvement history at first certification. Record the initial gap analysis run itself in gap-analysis.md as one audit record; at the 18-month renewal, two or more records will satisfy this item.
:::

- **Agent in charge**: `03-policy-generator`

---

#### G1.6 — Establishing procedures to review license obligations `[5230]`

> ISO/IEC 5230 §3.1.5

Prevent license violations before distribution; covers obligations such as copyleft source-code disclosure.

| Evidence ID   | Content                                                                                                     | Deliverable file                   |
| ------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| 5230 §3.1.5.1 | Procedures for reviewing and recording the obligations, restrictions, and rights of each identified license | `output/process/usage-approval.md` |

- **Agent in charge**: `04-process-designer`

---

#### G1.7 — Program participant awareness records `[Common]`

> ISO/IEC 5230 §3.1.3 · ISO/IEC 18974 §4.1.3

Document, per person and role, that each participant understands the policy, the goals, and how to contribute; this is key evidence during an audit.

| Evidence ID                    | Content                                                                                                         | Deliverable file                        |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| 5230 §3.1.3.1 · 18974 §4.1.3.1 | Evidence assessing participant awareness of the program goals, ways to contribute, and impact of non-compliance | `output/training/completion-tracker.md` |

- **Agent in charge**: `06-training-manager`

---

### G2: Defining and supporting related tasks

---

#### G2.1 — Establishing roles and responsibilities (RACI) `[Common]`

> ISO/IEC 5230 §3.2.2 · ISO/IEC 18974 §4.2.2

Clarify who performs, approves, and reviews open source activities; prevent gaps in ownership.

| Evidence ID                    | Content                                                              | Deliverable file                                                               |
| ------------------------------ | -------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 5230 §3.2.2.1 · 18974 §4.2.2.1 | Document naming the owner/group/job title for each role              | `output/organization/raci-matrix.md`                                           |
| 5230 §3.2.2.2 · 18974 §4.2.2.2 | Confirmation of adequate role staffing and budget                    | `output/organization/raci-matrix.md`                                           |
| 5230 §3.2.2.3                  | Method for accessing legal counsel on license compliance             | `output/organization/role-definition.md`                                       |
| 5230 §3.2.2.4 · 18974 §4.2.2.4 | Internal responsibility assignment procedure                         | `output/organization/raci-matrix.md`                                           |
| 5230 §3.2.2.5                  | Procedure for reviewing and correcting license non-compliance cases  | `output/process/usage-approval.md`, `output/process/distribution-checklist.md` |
| 18974 §4.2.2.3                 | Identification of the expertise available to resolve vulnerabilities | `output/organization/role-definition.md`                                       |

- **Agent in charge**: `02-organization-designer`

---

#### G2.2 — Operating channels for receiving external inquiries `[Common]`

> ISO/IEC 5230 §3.2.1 · ISO/IEC 18974 §4.2.1

An official channel is required so third parties can request fulfillment of license obligations and report security vulnerabilities.

| Evidence ID                    | Content                                                | Deliverable file                                                                 |
| ------------------------------ | ------------------------------------------------------ | -------------------------------------------------------------------------------- |
| 5230 §3.2.1.1 · 18974 §4.2.1.1 | Public channel through which third parties can inquire | `output/organization/role-definition.md`                                         |
| 5230 §3.2.1.2 · 18974 §4.2.1.2 | Internal response procedure for third-party inquiries  | `output/process/inquiry-response.md`, `output/process/vulnerability-response.md` |

- **Agent in charge**: `02-organization-designer`, `04-process-designer`

---

#### G2.3 — Operating an awareness program `[Common]`

> ISO/IEC 5230 §3.1.3 · ISO/IEC 18974 §4.1.3

Compliance is only effective when every member knows and follows the policy.

| Evidence ID                    | Content                                                                                                    | Deliverable file                                                        |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 5230 §3.1.3.1 · 18974 §4.1.3.1 | Evidence of participant awareness assessment (including goals, contribution, and impact of non-compliance) | `output/training/resources.md`, `output/training/completion-tracker.md` |

- **Agent in charge**: `06-training-manager`

---

### G3-L: License compliance (ISO/IEC 5230 focus)

---

#### G3L.1 — License identification and classification `[5230]`

> ISO/IEC 5230 §3.3.1 · §3.3.2

Identify the license status of each component from the SBOM; flag copyleft risk.

| Evidence ID   | Content                                                                           | Deliverable file                                                |
| ------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 5230 §3.3.1.1 | Procedure for identifying, tracking, reviewing, approving, and archiving the SBOM | `output/process/usage-approval.md`                              |
| 5230 §3.3.1.2 | Component records (evidence of procedural compliance)                             | `output/sbom/[project].cdx.json`                                |
| 5230 §3.3.2.1 | Procedure for handling license use cases                                          | `output/sbom/license-report.md`, `output/sbom/copyleft-risk.md` |

- **Agent in charge**: `05-sbom-analyst`

---

#### G3L.2 — Fulfilling license obligations `[5230]`

> ISO/IEC 5230 §3.3.2

Fulfill copyleft license obligations such as GPL, LGPL, and AGPL; maintain an Approved License List.

| Evidence ID   | Content                                                                    | Deliverable file                                                                 |
| ------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| 5230 §3.3.2.1 | Procedure for handling the license use cases of each open source component | `output/process/distribution-checklist.md`, `output/policy/license-allowlist.md` |

- **Agent in charge**: `04-process-designer`

---

#### G3L.3 — Generating compliance artifacts `[5230]`

> ISO/IEC 5230 §3.4.1

Obligation to provide, at distribution time, the files that demonstrate fulfillment of legal obligations, such as attribution notices and source code.

| Evidence ID   | Content                                                                 | Deliverable file                |
| ------------- | ----------------------------------------------------------------------- | ------------------------------- |
| 5230 §3.4.1.1 | Procedure for preparing and distributing compliance artifacts           | `output/sbom/license-report.md` |
| 5230 §3.4.1.2 | Procedure for archiving compliance artifacts and records of fulfillment | `output/sbom/license-report.md` |

- **Agent in charge**: `05-sbom-analyst`

---

#### G3L.4 — Establishing an open source contribution policy `[5230]`

> ISO/IEC 5230 §3.5.1

Prevents IP leakage and license-contamination risk when contributing upstream.

| Evidence ID   | Content                                 | Deliverable file                |
| ------------- | --------------------------------------- | ------------------------------- |
| 5230 §3.5.1.1 | Open source contribution policy         | `output/policy/oss-policy.md`   |
| 5230 §3.5.1.3 | Contribution policy awareness procedure | `output/training/curriculum.md` |

- **Agent in charge**: `03-policy-generator`

---

#### G3L.5 — Process for verifying that license obligations are met `[5230]`

> ISO/IEC 5230 §3.4.1

Verify before distribution that all license obligations (source-code disclosure, inclusion of attribution notices, and so on) have actually been met; acts as a release approval gate.

| Evidence ID   | Content                                                                 | Deliverable file                           |
| ------------- | ----------------------------------------------------------------------- | ------------------------------------------ |
| 5230 §3.4.1.1 | Procedure for preparing and distributing compliance artifacts           | `output/process/distribution-checklist.md` |
| 5230 §3.4.1.2 | Procedure for archiving compliance artifacts and records of fulfillment | `output/process/distribution-checklist.md` |

- **Agent in charge**: `04-process-designer`

---

#### G3L.6 — Operating an open source contribution process `[5230]`

> ISO/IEC 5230 §3.5.1

Concrete procedures for implementing the policy (G3L.4): the contribution review, approval, and submission workflow. Policy alone cannot govern actual contributions.

| Evidence ID   | Content                                       | Deliverable file                                                                      |
| ------------- | --------------------------------------------- | ------------------------------------------------------------------------------------- |
| 5230 §3.5.1.2 | Open source contribution management procedure | `output/policy/oss-policy.md`, `output/process/contribution-process.md` (conditional) |

- **Agent in charge**: `03-policy-generator`, `04-process-designer` (conditional)

---

### G3-S: Security assurance (ISO/IEC 18974 focus)

---

#### G3S.1 — Identifying known vulnerabilities (CVE scan) `[18974]`

> ISO/IEC 18974 §4.3.2 · §4.1.5

Failing to identify CVEs invites security incidents and legal liability; this is an EO 14028 requirement.

| Evidence ID    | Content                                                                              | Deliverable file                           |
| -------------- | ------------------------------------------------------------------------------------ | ------------------------------------------ |
| 18974 §4.1.5.1 | Standard vulnerability response procedure, including vulnerability detection methods | `output/process/vulnerability-response.md` |
| 18974 §4.3.2.1 | Vulnerability detection and resolution procedure                                     | `output/vulnerability/cve-report.md`       |
| 18974 §4.3.2.2 | Record of vulnerabilities and actions taken                                          | `output/vulnerability/cve-report.md`       |

- **Agent in charge**: `05-vulnerability-analyst`

---

#### G3S.2 — Vulnerability tracking and status management `[18974]`

> ISO/IEC 18974 §4.3.2 · §4.1.5

Continuously track identified vulnerabilities until remediation is complete; prevent items from being missed or left unattended.

| Evidence ID    | Content                                                                    | Deliverable file                           |
| -------------- | -------------------------------------------------------------------------- | ------------------------------------------ |
| 18974 §4.1.5.1 | Standard response procedure, including how to follow up on vulnerabilities | `output/process/vulnerability-response.md` |
| 18974 §4.3.2.1 | Vulnerability detection and resolution procedure                           | `output/vulnerability/cve-report.md`       |
| 18974 §4.3.2.2 | Record of vulnerabilities and actions taken                                | `output/vulnerability/cve-report.md`       |

- **Agent in charge**: `05-vulnerability-analyst`

---

#### G3S.3 — CVE risk scoring (CVSS) `[18974]`

> ISO/IEC 18974 §4.3.2

Prioritize by CVSS score; allocate resources efficiently.

| Evidence ID    | Content                                                                  | Deliverable file                     |
| -------------- | ------------------------------------------------------------------------ | ------------------------------------ |
| 18974 §4.3.2.1 | Vulnerability handling procedure, including risk/impact score assignment | `output/vulnerability/cve-report.md` |
| 18974 §4.3.2.2 | Record of identified vulnerabilities and risk scores                     | `output/vulnerability/cve-report.md` |

- **Agent in charge**: `05-vulnerability-analyst`

---

#### G3S.4 — Vulnerability response and patching procedures `[18974]`

> ISO/IEC 18974 §4.3.2 · §4.1.5

A system for rapidly patching, upgrading, or mitigating discovered vulnerabilities.

| Evidence ID    | Content                                                                               | Deliverable file                           |
| -------------- | ------------------------------------------------------------------------------------- | ------------------------------------------ |
| 18974 §4.1.5.1 | Standard response procedure, including appropriate action methods for each risk level | `output/vulnerability/remediation-plan.md` |
| 18974 §4.3.2.1 | Vulnerability resolution procedure                                                    | `output/vulnerability/remediation-plan.md` |
| 18974 §4.3.2.2 | Record of actions taken                                                               | `output/vulnerability/remediation-plan.md` |

- **Agent in charge**: `05-vulnerability-analyst`

---

#### G3S.5 — Security artifact delivery process `[18974, Supply Chain]`

> ISO/IEC 18974 §4.3.1

Formal procedures for delivering security deliverables such as the SBOM and CVE reports to supply chain partners and customers; addresses the EO 14028 and EU CRA disclosure obligations.

| Evidence ID    | Content                                                                                   | Deliverable file                       |
| -------------- | ----------------------------------------------------------------------------------------- | -------------------------------------- |
| 18974 §4.3.1.1 | Procedure for continuously recording the SBOM throughout the supplied software life cycle | `output/sbom/sbom-sharing-template.md` |
| 18974 §4.3.1.2 | Component records (evidence of procedural compliance)                                     | `output/sbom/[project].cdx.json`       |

- **Agent in charge**: `05-sbom-management`

---

#### G3S.6 — Process for verifying that security obligations are met `[18974]`

> ISO/IEC 18974 §4.3.2

Procedure to verify that the response, patch, and mitigation actions for identified and tracked vulnerabilities were actually completed; confirms real implementation rather than a mere declaration.

| Evidence ID    | Content                                                                    | Deliverable file                           |
| -------------- | -------------------------------------------------------------------------- | ------------------------------------------ |
| 18974 §4.3.2.1 | Procedure including verification that vulnerability resolution is complete | `output/vulnerability/remediation-plan.md` |
| 18974 §4.3.2.2 | Record of completed actions                                                | `output/vulnerability/remediation-plan.md` |

- **Agent in charge**: `05-vulnerability-analyst`

---

### G3-B: SBOM and supply chain (common)

---

#### G3B.1 — Creating an SBOM (CycloneDX/SPDX) `[Common, Supply Chain]`

> ISO/IEC 5230 §3.3.1 · ISO/IEC 18974 §4.3.1

The starting point for component transparency; the input for both license and security analysis.

| Evidence ID                    | Content                                                                           | Deliverable file                 |
| ------------------------------ | --------------------------------------------------------------------------------- | -------------------------------- |
| 5230 §3.3.1.1 · 18974 §4.3.1.1 | Procedure for identifying, tracking, reviewing, approving, and archiving the SBOM | `output/sbom/sbom-commands.sh`   |
| 5230 §3.3.1.2 · 18974 §4.3.1.2 | Component records (evidence of procedural compliance)                             | `output/sbom/[project].cdx.json` |

- **Agent in charge**: `05-sbom-guide`

---

#### G3B.2 — SBOM management and maintenance `[Common, Supply Chain]`

> ISO/IEC 5230 §3.3.1 · ISO/IEC 18974 §4.3.1

Keep the SBOM current on every release and update; integrate it with configuration management.

| Evidence ID                    | Content                              | Deliverable file                      |
| ------------------------------ | ------------------------------------ | ------------------------------------- |
| 5230 §3.3.1.1 · 18974 §4.3.1.1 | SBOM life cycle management procedure | `output/sbom/sbom-management-plan.md` |
| 5230 §3.3.1.2 · 18974 §4.3.1.2 | Up-to-date component records         | `output/sbom/[project].cdx.json`      |

- **Agent in charge**: `05-sbom-management`

---

#### G3B.3 — Sharing the SBOM (with supply chain partners) `[Supply Chain, Regulation]`

> ISO/IEC 18974 §4.3.1

Pass transparency down the supply chain; addresses the NTIA and EU CRA supply chain disclosure obligations.

| Evidence ID    | Content                                                                               | Deliverable file                       |
| -------------- | ------------------------------------------------------------------------------------- | -------------------------------------- |
| 18974 §4.3.1.1 | Life cycle recording procedure, including sharing the SBOM with supply chain partners | `output/sbom/sbom-sharing-template.md` |
| 18974 §4.3.1.2 | Component records                                                                     | `output/sbom/[project].cdx.json`       |

- **Agent in charge**: `05-sbom-management`

---

#### G3B.4 — Continuous monitoring of supply chain vulnerabilities `[Supply Chain]`

> ISO/IEC 18974 §4.3.2

When a new CVE is disclosed, immediately identify which supply chain components are affected.

| Evidence ID    | Content                                                                               | Deliverable file                      |
| -------------- | ------------------------------------------------------------------------------------- | ------------------------------------- |
| 18974 §4.3.2.1 | Response procedure, including methods for analyzing new vulnerabilities after release | `output/sbom/sbom-management-plan.md` |
| 18974 §4.3.2.2 | Record of vulnerabilities and actions taken                                           | `output/sbom/sbom-management-plan.md` |

- **Agent in charge**: `05-sbom-management`

---

### G4: Declaring and maintaining compliance

---

#### G4.1 — ISO/IEC 5230 self-certification declaration `[5230]`

> ISO/IEC 5230 §3.6.1

Official declaration of license compliance capability; earns the trust of supply chain partners.

| Evidence ID   | Content                                                                                     | Deliverable file                          |
| ------------- | ------------------------------------------------------------------------------------------- | ----------------------------------------- |
| 5230 §3.6.1.1 | Document confirming that the program in §3.1.4 meets all requirements of this specification | `output/conformance/declaration-draft.md` |

- **Agent in charge**: `07-conformance-preparer`

---

#### G4.2 — ISO/IEC 18974 self-certification declaration `[18974]`

> ISO/IEC 18974 §4.4.1

Official declaration of security assurance capability; evidence for EO 14028 and EU CRA compliance.

| Evidence ID    | Content                                                                                     | Deliverable file                          |
| -------------- | ------------------------------------------------------------------------------------------- | ----------------------------------------- |
| 18974 §4.4.1.1 | Document confirming that the program in §4.1.4 meets all requirements of this specification | `output/conformance/declaration-draft.md` |

- **Agent in charge**: `07-conformance-preparer`

---

#### G4.3 — Managing the certification validity period (18 months) `[Common]`

> ISO/IEC 5230 §3.6.2 · ISO/IEC 18974 §4.4.2

Both standards require re-declaration every 18 months; this avoids automatic expiration.

| Evidence ID                    | Content                                                                                           | Deliverable file                         |
| ------------------------------ | ------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| 5230 §3.6.2.1 · 18974 §4.4.2.1 | Document confirming that all requirements have been met within 18 months of obtaining conformance | `output/conformance/submission-guide.md` |

- **Agent in charge**: `07-conformance-preparer`

---

#### G4.4 — Regular gap analysis and policy updates `[Common]`

> ISO/IEC 5230 §3.6.2 · ISO/IEC 18974 §4.4.2

Evolve the system as the technical and regulatory environment changes; required before a renewal declaration.

| Evidence ID                    | Content                                                           | Deliverable file                     |
| ------------------------------ | ----------------------------------------------------------------- | ------------------------------------ |
| 5230 §3.6.2.1 · 18974 §4.4.2.1 | Document confirming re-satisfaction of requirements after renewal | `output/conformance/gap-analysis.md` |

- **Agent in charge**: `07-conformance-preparer`

---

#### G4.5 — Confirming distributed software has no known vulnerabilities `[18974]`

> ISO/IEC 18974 §4.4.1 · §4.3.2

Before distribution, verify and declare that externally distributed software has no known vulnerabilities; a practical prerequisite for the certification declaration.

| Evidence ID    | Content                                                                    | Deliverable file                          |
| -------------- | -------------------------------------------------------------------------- | ----------------------------------------- |
| 18974 §4.4.1.1 | Document confirming that distributed software fully meets the requirements | `output/conformance/declaration-draft.md` |
| 18974 §4.3.2.2 | Record of completed vulnerability actions                                  | `output/vulnerability/cve-report.md`      |

- **Agent in charge**: `07-conformance-preparer`

---

## Summary statistics

| Category                                          | Number of items |
| ------------------------------------------------- | --------------- |
| ISO/IEC 5230 mapped items                         | 20              |
| ISO/IEC 18974 mapped items                        | 23              |
| Items common to both standards                    | 12              |
| Supply chain related items (`[Supply Chain]` tag) | 5               |
| Regulation-linked items (`[Regulation]` tag)      | 1               |
| **Total number of items**                         | **31**          |

:::info[Note]
The common items (12) are counted in both the 5230 total (20) and the 18974 total (23). Preparing both standards at once lets you handle the common items only once, saving roughly 39% (12/31).
:::

---

## Next steps

:::info Self-study mode (about 1 hour)
Once you understand this mapping document, start producing the actual deliverables.
If the `output/` folder is empty, begin with the steps below.
:::

1. **Organization design** → `cd agents/02-organization-designer && claude`
2. **Create policy** → `cd agents/03-policy-generator && claude`
3. **Process design** → `cd agents/04-process-designer && claude`
4. **Create SBOM** → `cd agents/05-sbom-guide && claude`
5. **License analysis** → `cd agents/05-sbom-analyst && claude`
6. **SBOM management plan** → `cd agents/05-sbom-management && claude`
7. **Vulnerability analysis** → `cd agents/05-vulnerability-analyst && claude`
8. **Training program** → `cd agents/06-training-manager && claude`
9. **Certification declaration** → `cd agents/07-conformance-preparer && claude`

:::info Status of this document
This document is the project's canonical mapping reference for the **full** ISO/IEC 5230 and the **full** ISO/IEC 18974 requirements.
Each agent's CLAUDE.md refers to this file.
:::
