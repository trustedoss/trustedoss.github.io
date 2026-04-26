---
id: checklist-mapping
title: Requirements Checklist Integrated Mapping
sidebar_label: Checklist Mapping
sidebar_position: 2
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: 전체 (매핑 기준 문서)'
  - 'ISO/IEC 18974: 전체 (매핑 기준 문서)'
self_study_time: 1 hour
---

# Requirements Checklist Integrated Mapping

## Purpose of this document

This document complies with **ISO/IEC 5230** (license compliance) and **ISO/IEC 18974** (security assurance).
It is a compass for the entire project that integrates self-certification checklist items from both standards into one mapping table.

Every agent's CLAUDE.md refers to this document and produces output that meets certain standard requirements.
Find out which module creates it.

### How to read this document

1. **Comparison table of two standards** → First understand the purpose and scope of each standard
2. **Integrated mapping** → Check the proving materials, output, and agent in charge in the item block for each G1~G4 group.
3. **Tag** → Quickly understand the nature of each item with `[Common]` `[5230]` `[18974]` `[Supply Chain]` `[Regulation]`
4. **Summary statistics** → Check the overall status in numbers at the bottom of the document

---

## Compare two standards

| Item                              | ISO/IEC 5230                                                                                                | ISO/IEC 18974                                                                                            |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Official name**                 | OpenChain License Compliance                                                                                | OpenChain Security Assurance                                                                             |
| **Latest version**                | 2.1 (2023)                                                                                                  | 1.0 (2023)                                                                                               |
| **Purpose**                       | Establishment of an open source license compliance system                                                   | Establishment of an open source security vulnerability assurance system                                  |
| **Focus**                         | Fulfill license obligations, manage BOM, create notices                                                     | Identifying, tracking and responding to known CVEs, SBOM based security                                  |
| **Key Requirements**              | Policy, Organization, Process, BOM, Compliance Deliverables, Contribution Policy, Declaration of Compliance | Policy, Organization, SBOM, CVE Scan, Vulnerability Tracking/Scoring/Response, Declaration of Compliance |
| **Authentication Method**         | OpenChain Website self-declaration                                                                          | OpenChain Website self-declaration                                                                       |
| **Validity Period**               | 18 months                                                                                                   | 18 months                                                                                                |
| **Related regulations/standards** | SPDX, REUSE, EU CRA (licensing aspect)                                                                      | EO 14028, NTIA SBOM, EU CRA, NVD/CVSS                                                                    |
| **Complementarity**               | Share common base (policy, organization, SBOM), add license-specific requirements                           | Share common base, add security-specific requirements                                                    |

> **Key Insights:** The two standards share common ground in the areas of policy, organization, education, and SBOM.
> Building one automatically fulfills half of the other.

---

## Remarks Column notation rules

| Tags             | meaning                                                              |
| ---------------- | -------------------------------------------------------------------- |
| `[Common]`       | Required by both standards                                           |
| `[5230]`         | ISO/IEC 5230 only                                                    |
| `[18974]`        | ISO/IEC 18974 only (security specialized)                            |
| `[Supply Chain]` | Software supply chain security related                               |
| `[Regulation]`   | International regulatory linkage items (EO 14028, EU CRA, NTIA SBOM) |

---

## Integrated mapping

### G1: Program-based

---

#### G1.1 — Establishing and documenting open source policies `[Common]`

> ISO/IEC 5230 §3.1.1 · ISO/IEC 18974 §4.1.1

Systematic compliance cannot be established without policy; The basis for all activities

| Proof ID                       | Content                        | output file                     |
| ------------------------------ | ------------------------------ | ------------------------------- |
| 5230 §3.1.1.1 · 18974 §4.1.1.1 | Documented open source policy  | `output/policy/oss-policy.md`   |
| 5230 §3.1.1.2 · 18974 §4.1.1.2 | Policy dissemination procedure | `output/training/curriculum.md` |

- **Agent in Charge**: `03-policy-generator`

---

#### G1.2 — Establish a review process for security assurance policies `[18974]`

> ISO/IEC 18974 §4.1.1

18974 further requires a regular review process to ensure policies and methods of communication are always up to date.

| Proof ID       | Content                                                         | output file                          |
| -------------- | --------------------------------------------------------------- | ------------------------------------ |
| 18974 §4.1.1.1 | Documented security assurance policy (including review process) | `output/policy/oss-policy.md`        |
| 18974 §4.1.2.5 | Periodic review and evidence of change                          | `output/conformance/gap-analysis.md` |

- **Agent in Charge**: `03-policy-generator`

---

#### G1.3 — Designation of open source contact persons and organizations `[Common]`

> ISO/IEC 5230 §3.1.2 · ISO/IEC 18974 §4.1.2

Without a clear sense of responsibility, a decision-making vacuum arises.

| Proof ID                       | Content                                            | output file                              |
| ------------------------------ | -------------------------------------------------- | ---------------------------------------- |
| 5230 §3.1.2.1 · 18974 §4.1.2.1 | List of Roles and Responsibilities                 | `output/organization/raci-matrix.md`     |
| 5230 §3.1.2.2 · 18974 §4.1.2.2 | Competency technical documentation for each role   | `output/organization/role-definition.md` |
| 18974 §4.1.2.3                 | Participant list and roles                         | `output/organization/role-definition.md` |
| 5230 §3.1.2.3 · 18974 §4.1.2.4 | Competency Assessment Evidence                     | `output/training/completion-tracker.md`  |
| 18974 §4.1.2.5                 | Periodic review and evidence of process changes ⚠️ | `output/conformance/gap-analysis.md`     |
| 18974 §4.1.2.6                 | Internal best practice alignment verification ⚠️   | `output/conformance/gap-analysis.md`     |

> ⚠️ **§4.1.2.5 · §4.1.2.6 Processing upon initial certification**: At first certification, there is no review history, so it is processed as partially satisfied (🔶).
> Record “review cycle plan” and “designation of person in charge” in gap-analysis.md and meet with actual history upon renewal after 18 months.

- **Agent in Charge**: `02-organization-designer`

---

#### G1.4 — Establishing a training program `[Common]`

> ISO/IEC 5230 §3.1.2 · ISO/IEC 18974 §4.1.2 (education and training aspects)

Securing and continuously maintaining staff capacity; All standards require proof of training completion

| Proof ID                       | Content                            | output file                             |
| ------------------------------ | ---------------------------------- | --------------------------------------- |
| 5230 §3.1.2.1 · 18974 §4.1.2.1 | List of Roles and Responsibilities | `output/organization/raci-matrix.md`    |
| 5230 §3.1.2.3 · 18974 §4.1.2.4 | Competency Assessment Evidence     | `output/training/completion-tracker.md` |

- **Agent in Charge**: `06-training-manager`

---

#### G1.5 — Program scope definition `[Common]`

> ISO/IEC 5230 §3.1.4 · ISO/IEC 18974 §4.1.4

Efficient resource allocation possible by clarifying target software/products

| Proof ID                       | Content                                | output file                          |
| ------------------------------ | -------------------------------------- | ------------------------------------ |
| 5230 §3.1.4.1 · 18974 §4.1.4.1 | Program Scope and Limitations Document | `output/policy/oss-policy.md`        |
| 18974 §4.1.4.2                 | Performance Metrics                    | `output/policy/oss-policy.md`        |
| 18974 §4.1.4.3                 | Evidence of continuous improvement ⚠️  | `output/conformance/gap-analysis.md` |

> ⚠️ **§4.1.4.3 Processing upon initial certification**: There is no history of improvement upon first certification. The initial gap analysis execution itself is recorded in gap-analysis.md as a one-time audit history, and when renewed after 18 months, the history is satisfied at least twice.

- **Agent in Charge**: `03-policy-generator`

---

#### G1.6 — Establish procedures for review of license obligations `[5230]`

> ISO/IEC 5230 §3.1.5

Prevent license violations before distribution; Copyleft Source code disclosure obligation, etc.

| Proof ID      | Content                                                                                                  | output file                        |
| ------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| 5230 §3.1.5.1 | Procedures for reviewing and recording obligations, restrictions, and rights for each identified license | `output/process/usage-approval.md` |

- **Agent in charge**: `04-process-designer`

---

#### G1.7 — Program Participant Recognition Record `[Common]`

> ISO/IEC 5230 §3.1.3 · ISO/IEC 18974 §4.1.3

Individually document whether each person in each role understands the policies, goals, and ways to contribute; Key supporting information during audits

| Proof ID                       | Content                                                                                                       | output file                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| 5230 §3.1.3.1 · 18974 §4.1.3.1 | Evidence assessing participant perceptions of program goals, ways to contribute, and impact of non-compliance | `output/training/completion-tracker.md` |

- **Agent in charge**: `06-training-manager`

---

### G2: Define and support relevant tasks

---

#### G2.1 — Establishing Roles and Responsibilities (RACI) `[Common]`

> ISO/IEC 5230 §3.2.2 · ISO/IEC 18974 §4.2.2

Clarification of open source activity subject, approval, and review system; Prevent work gaps

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

Official channel obligations to request fulfillment of license obligations and report security vulnerabilities

| Proof ID                       | Content                                                | output file                                                                      |
| ------------------------------ | ------------------------------------------------------ | -------------------------------------------------------------------------------- |
| 5230 §3.2.1.1 · 18974 §4.2.1.1 | Public channel for third parties to make inquiries     | `output/organization/role-definition.md`                                         |
| 5230 §3.2.1.2 · 18974 §4.2.1.2 | Internal response procedures for third party inquiries | `output/process/inquiry-response.md`, `output/process/vulnerability-response.md` |

- **Agent in charge**: `02-organization-designer`

---

#### G2.3 — Operating awareness-raising programs `[Common]`

> ISO/IEC 5230 §3.1.3 · ISO/IEC 18974 §4.1.3

Effectiveness of compliance is ensured when all members know and follow the policy.

| Proof ID                       | Content                                                                                                     | output file                                                             |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 5230 §3.1.3.1 · 18974 §4.1.3.1 | Evidence of participant perception assessment (including goals, contributions and impact of non-compliance) | `output/training/resources.md`, `output/training/completion-tracker.md` |

- **Agent in charge**: `06-training-manager`

---

### G3-L: License compliance (ISO/IEC 5230 focused)

---

#### G3L.1 — License Identification and Classification `[5230]`

> ISO/IEC 5230 §3.3.1 · §3.3.2

Identify license status for each SBOM-based component; Copyleft risk identification

| Proof ID      | Content                                                                 | output file                                                     |
| ------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------- |
| 5230 §3.3.1.1 | SBOM Identification, tracking, review, approval, and storage procedures | `output/process/usage-approval.md`                              |
| 5230 §3.3.1.2 | Component Records (Proof of Procedural Compliance)                      | `output/sbom/[project].cdx.json`                                |
| 5230 §3.3.2.1 | Licensing Use Case Processing Procedure                                 | `output/sbom/license-report.md`, `output/sbom/copyleft-risk.md` |

- **Agent in Charge**: `05-sbom-analyst`

---

#### G3L.2 — Fulfillment of License Obligations `[5230]`

> ISO/IEC 5230 §3.3.2

Fulfillment of copyleft license obligations such as GPL, LGPL, AGPL, etc.; Manage permitted license list

| Proof ID      | Content                                                            | output file                                                                      |
| ------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| 5230 §3.3.2.1 | License use case handling procedure for each open source component | `output/process/distribution-checklist.md`, `output/policy/license-allowlist.md` |

- **Agent in Charge**: `04-process-designer`

---

#### G3L.3 — Generate compliance artifacts `[5230]`

> ISO/IEC 5230 §3.4.1

Obligation to provide files proving the fulfillment of legal obligations, such as notices and source codes, when distributing

| Proof ID      | Content                                                           | output file                     |
| ------------- | ----------------------------------------------------------------- | ------------------------------- |
| 5230 §3.4.1.1 | Compliance deliverable preparation and distribution procedures    | `output/sbom/license-report.md` |
| 5230 §3.4.1.2 | Compliance deliverable storage procedures and performance records | `output/sbom/license-report.md` |

- **Agent in Charge**: `05-sbom-analyst`

---

#### G3L.4 — Establishing an open source contribution policy `[5230]`

> ISO/IEC 5230 §3.5.1

Prevents IP leakage and license contamination risks when contributing upstream

| Proof ID      | Content                                   | output file                     |
| ------------- | ----------------------------------------- | ------------------------------- |
| 5230 §3.5.1.1 | Open source contribution policy           | `output/policy/oss-policy.md`   |
| 5230 §3.5.1.3 | Contribution Policy Recognition Procedure | `output/training/curriculum.md` |

- **Agent in Charge**: `03-policy-generator`

---

#### G3L.5 — Process for Verifying Satisfaction of License Obligations `[5230]`

> ISO/IEC 5230 §3.4.1

Verification that all license obligations (source code disclosure, inclusion of notices, etc.) have actually been fulfilled prior to distribution; Acts as a deployment approval gateway

| Proof ID      | Content                                                           | output file                                |
| ------------- | ----------------------------------------------------------------- | ------------------------------------------ |
| 5230 §3.4.1.1 | Compliance deliverable preparation and distribution procedures    | `output/process/distribution-checklist.md` |
| 5230 §3.4.1.2 | Compliance deliverable storage procedures and performance records | `output/process/distribution-checklist.md` |

- **Agent in Charge**: `04-process-designer`

---

#### G3L.6 — Open source contribution process operation `[5230]`

> ISO/IEC 5230 §3.5.1

Specific procedures for implementing the policy (G3L.4); Contribution review, approval, and submission workflow; Policy alone cannot control actual contributions

| Proof ID      | Content                                     | output file                                                                           |
| ------------- | ------------------------------------------- | ------------------------------------------------------------------------------------- |
| 5230 §3.5.1.2 | Open source contribution management process | `output/policy/oss-policy.md`, `output/process/contribution-process.md` (conditional) |

- **Agent in charge**: `03-policy-generator`, `04-process-designer` (conditional)

---

### G3-S: Security assurance (based on ISO/IEC 18974)

---

#### G3S.1 — Identification of known vulnerabilities (CVE scan) `[18974]`

> ISO/IEC 18974 §4.3.2 · §4.1.5

Risk of security incidents and legal liability if CVE vulnerabilities are not identified; EO 14028 Requirements

| Proof ID       | Content                                                                               | output file                                |
| -------------- | ------------------------------------------------------------------------------------- | ------------------------------------------ |
| 18974 §4.1.5.1 | Standard vulnerability response procedures, including vulnerability detection methods | `output/process/vulnerability-response.md` |
| 18974 §4.3.2.1 | Vulnerability detection and resolution procedures                                     | `output/vulnerability/cve-report.md`       |
| 18974 §4.3.2.2 | Record of vulnerabilities and actions taken                                           | `output/vulnerability/cve-report.md`       |

- **Agent in Charge**: `05-vulnerability-analyst`

---

#### G3S.2 — Vulnerability Tracking and Health Management `[18974]`

> ISO/IEC 18974 §4.3.2 · §4.1.5

Continuous tracking of identified vulnerabilities until response is completed; Prevention of omission and neglect

| Proof ID       | Content                                                                     | output file                                |
| -------------- | --------------------------------------------------------------------------- | ------------------------------------------ |
| 18974 §4.1.5.1 | Standard response procedures, including how to follow up on vulnerabilities | `output/process/vulnerability-response.md` |
| 18974 §4.3.2.1 | Vulnerability detection and resolution procedures                           | `output/vulnerability/cve-report.md`       |
| 18974 §4.3.2.2 | Record of vulnerabilities and actions taken                                 | `output/vulnerability/cve-report.md`       |

- **Agent in Charge**: `05-vulnerability-analyst`

---

#### G3S.3 — CVE Risk Score Assessment (CVSS) `[18974]`

> ISO/IEC 18974 §4.3.2

CVSS score-based prioritization; Efficient resource allocation

| Proof ID       | Content                                                                   | output file                          |
| -------------- | ------------------------------------------------------------------------- | ------------------------------------ |
| 18974 §4.3.2.1 | Vulnerability handling procedures, including risk/impact score assignment | `output/vulnerability/cve-report.md` |
| 18974 §4.3.2.2 | Record identified vulnerabilities and risk scores                         | `output/vulnerability/cve-report.md` |

- **Agent in Charge**: `05-vulnerability-analyst`

---

#### G3S.4 — Vulnerability response and patching procedures `[18974]`

> ISO/IEC 18974 §4.3.2 · §4.1.5

Rapid patch, upgrade, and mitigation action system for discovered vulnerabilities

| Proof ID       | Content                                                                                | output file                                |
| -------------- | -------------------------------------------------------------------------------------- | ------------------------------------------ |
| 18974 §4.1.5.1 | Standard response procedures, including appropriate action methods for each risk level | `output/vulnerability/remediation-plan.md` |
| 18974 §4.3.2.1 | Vulnerability remediation procedures                                                   | `output/vulnerability/remediation-plan.md` |
| 18974 §4.3.2.2 | Records of actions taken                                                               | `output/vulnerability/remediation-plan.md` |

- **Agent in Charge**: `05-vulnerability-analyst`

---

#### G3S.5 — Security Artifact Deployment Process `[18974,supply chain]`

> ISO/IEC 18974 §4.3.1

SBOM·Formal procedures for delivering security outputs such as CVE reports to supply chain partners and customers; Response to EO 14028·EU CRA disclosure obligation

| Proof ID       | Content                                                                          | output file                            |
| -------------- | -------------------------------------------------------------------------------- | -------------------------------------- |
| 18974 §4.3.1.1 | SBOM Continuous recording procedures throughout the supplied software life cycle | `output/sbom/sbom-sharing-template.md` |
| 18974 §4.3.1.2 | Component Records (Proof of Procedural Compliance)                               | `output/sbom/[project].cdx.json`       |

- **Agent in Charge**: `05-sbom-management`

---

#### G3S.6 — Process for ensuring security obligations are met `[18974]`

> ISO/IEC 18974 §4.3.2

Procedures to verify that response, patch, and mitigation measures for identified and tracked vulnerabilities have actually been completed; Confirmation of actual implementation rather than formal declaration

| Proof ID       | Content                                                                     | output file                                |
| -------------- | --------------------------------------------------------------------------- | ------------------------------------------ |
| 18974 §4.3.2.1 | Procedures including verification of completion of vulnerability resolution | `output/vulnerability/remediation-plan.md` |
| 18974 §4.3.2.2 | Action Completion Record                                                    | `output/vulnerability/remediation-plan.md` |

- **Agent in charge**: `05-vulnerability-analyst`

---

### G3-B: SBOM and supply chain (common)

---

#### G3B.1 — create SBOM (CycloneDX/SPDX)`[Common,supply chain]`

> ISO/IEC 5230 §3.3.1 · ISO/IEC 18974 §4.3.1

Starting point for ensuring component transparency; Inputs for both license and security analysis

| Proof ID                       | Content                                                                 | output file                      |
| ------------------------------ | ----------------------------------------------------------------------- | -------------------------------- |
| 5230 §3.3.1.1 · 18974 §4.3.1.1 | SBOM Identification, tracking, review, approval, and storage procedures | `output/sbom/sbom-commands.sh`   |
| 5230 §3.3.1.2 · 18974 §4.3.1.2 | Component Records (Proof of Procedural Compliance)                      | `output/sbom/[project].cdx.json` |

- **Agent in Charge**: `05-sbom-guide`

---

#### G3B.2 — SBOM Management and Maintenance `[Common,supply chain]`

> ISO/IEC 5230 §3.3.1 · ISO/IEC 18974 §4.3.1

Maintain SBOM up-to-date when released/updated; Configuration management integration

| Proof ID                       | Content                              | output file                           |
| ------------------------------ | ------------------------------------ | ------------------------------------- |
| 5230 §3.3.1.1 · 18974 §4.3.1.1 | SBOM Life Cycle Management Procedure | `output/sbom/sbom-management-plan.md` |
| 5230 §3.3.1.2 · 18974 §4.3.1.2 | Latest component history             | `output/sbom/[project].cdx.json`      |

- **Agent in charge**: `05-sbom-management`

---

#### G3B.3 — SBOM Share (Supply Chain Partner)`[Supply chain,regulation]`

> ISO/IEC 18974 §4.3.1

Transparency down the supply chain; NTIA·Response to EU CRA supply chain disclosure obligation

| Proof ID       | Content                                                                            | output file                            |
| -------------- | ---------------------------------------------------------------------------------- | -------------------------------------- |
| 18974 §4.3.1.1 | Life cycle recording procedures, including sharing SBOM with supply chain partners | `output/sbom/sbom-sharing-template.md` |
| 18974 §4.3.1.2 | Component History                                                                  | `output/sbom/[project].cdx.json`       |

- **Agent in charge**: `05-sbom-management`

---

#### G3B.4 — Continuous monitoring of supply chain vulnerabilities `[Supply Chain]`

> ISO/IEC 18974 §4.3.2

Immediately identify affected supply chain components when a new CVE is disclosed

| Proof ID       | Content                                                                        | output file                           |
| -------------- | ------------------------------------------------------------------------------ | ------------------------------------- |
| 18974 §4.3.2.1 | Response procedures including new vulnerability analysis methods after release | `output/sbom/sbom-management-plan.md` |
| 18974 §4.3.2.2 | Vulnerability and Action Log                                                   | `output/sbom/sbom-management-plan.md` |

- **Agent in Charge**: `05-sbom-management`

---

### G4: Declaring and maintaining compliance

---

#### G4.1 — ISO/IEC 5230 self-certification declaration `[5230]`

> ISO/IEC 5230 §3.6.1

Official declaration of license compliance capability; Secure supply chain partner trust

| Proof ID      | Content                                                                              | output file                               |
| ------------- | ------------------------------------------------------------------------------------ | ----------------------------------------- |
| 5230 §3.6.1.1 | Confirmation that the program in §3.1.4 meets all requirements of this specification | `output/conformance/declaration-draft.md` |

- **Agent in charge**: `07-conformance-preparer`

---

#### G4.2 — ISO/IEC 18974 self-certification declaration `[18974]`

> ISO/IEC 18974 §4.4.1

Official declaration of security assurance capability; Proof of EO 14028 and EU CRA response

| Proof ID       | Content                                                                              | output file                               |
| -------------- | ------------------------------------------------------------------------------------ | ----------------------------------------- |
| 18974 §4.4.1.1 | Confirmation that the program in §4.1.4 meets all requirements of this specification | `output/conformance/declaration-draft.md` |

- **Agent in charge**: `07-conformance-preparer`

---

#### G4.3 — Management of certification validity period (18 months) `[Common]`

> ISO/IEC 5230 §3.6.2 · ISO/IEC 18974 §4.4.2

Both standards require redeclaration every 18 months; Avoid automatic expiration

| Proof ID                       | Content                                                                                               | output file                              |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| 5230 §3.6.2.1 · 18974 §4.4.2.1 | Documentation confirming that all requirements have been met within 18 months of obtaining conformity | `output/conformance/submission-guide.md` |

- **Agent in charge**: `07-conformance-preparer`

---

#### G4.4 — Regular gap analysis and policy updates `[Common]`

> ISO/IEC 5230 §3.6.2 · ISO/IEC 18974 §4.4.2

Implementation of the system according to changes in the technological and regulatory environment; Required before renewal declaration

| Proof ID                       | Content                                                           | output file                          |
| ------------------------------ | ----------------------------------------------------------------- | ------------------------------------ |
| 5230 §3.6.2.1 · 18974 §4.4.2.1 | Document confirming re-satisfaction of requirements after renewal | `output/conformance/gap-analysis.md` |

- **Agent in Charge**: `07-conformance-preparer`

---

#### G4.5 — Verify that distributed software has no known vulnerabilities `[18974]`

> ISO/IEC 18974 §4.4.1 · §4.3.2

Verify and declare before distribution that there are no known vulnerabilities in externally distributed software; Practical prerequisites for declaration of certification

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

> **Note:** Common entries (11) are counted in both 5230 (20) and 18974 (23).
> Preparing both standards simultaneously saves approximately 35% by working on common items only once.

---

## next steps

:::info Self-study mode (about 1 hour)
Once you have this mapping document figured out, start creating the actual output.
If the `output/` folder is empty, start with the steps below.
:::

1. **Organizational Design** → `cd agents/02-organization-designer && claude`
2. **Create Policy** → `cd agents/03-policy-generator && claude`
3. **Process Design** → `cd agents/04-process-designer && claude`
4. **SBOM creation** → `cd agents/05-sbom-guide && claude`
5. **License Analysis** → `cd agents/05-sbom-analyst && claude`
6. **Vulnerability Analysis** → `cd agents/05-vulnerability-analyst && claude`
7. **SBOM Management Plan** → `cd agents/05-sbom-management && claude`
8. **Education System** → `cd agents/06-training-manager && claude`
9. **Certification Declaration** → `cd agents/07-conformance-preparer && claude`

> This document contains the ISO/IEC 5230 **Full** and ISO/IEC 18974 **Full** requirements.
> This is the mapping standard document within the project.
> This file is referenced in each agent's CLAUDE.md.
