# Self-Certification Declaration

<!-- 5230 §3.6.1.1, 18974 §4.4.1.1 -->

---

## Declaration

**Company name**: {company name}
**Declaring Program Manager**: {name}, {title}
**Declaration date**: YYYY-MM-DD
**Validity expires**: YYYY-MM-DD (declaration date + 18 months)
**Re-declaration due**: YYYY-MM-DD

---

## Standards being declared

- [x] ISO/IEC 5230:2020 (OpenChain License Compliance)
- [x] ISO/IEC 18974:2023 (OpenChain Security Assurance)

_Check only the ones that apply._

---

## Scope

<!-- §3.1.4, §4.1.4 -->

This declaration applies to the software and products below:

- **Target product or software**: {product or service name}
- **Version range**: {version X and above / all}
- **Distribution methods**: {SaaS / app store / embedded / internal use}
- **Exclusions**: {none / specific exclusions}

---

## ISO/IEC 5230:2020 checklist confirmation

<!-- Confirm the 25 pieces of evidence per standard by clause ID, the same scheme as gap-analysis.md.
     docs/00-overview/checklist-mapping.md is the authoritative map of the G items (G1 to G4). -->

Confirm whether the 25 pieces of evidence below are satisfied. If anything is still only partially satisfied (🔶), either complete it before declaring, or declare with only the time-based items (18974 §4.1.2.5, §4.1.2.6, §4.1.4.3) left in the planned state.

| Item ID | Content                                                          | Satisfied | Deliverable                                                  |
| ------- | ---------------------------------------------------------------- | :-------: | ------------------------------------------------------------ |
| 3.1.1.1 | Documented open source policy                                    |   ✅/🔶   | output/policy/oss-policy.md                                  |
| 3.1.1.2 | Policy dissemination procedure                                   |   ✅/🔶   | oss-policy.md §7, training/curriculum.md                     |
| 3.1.2.1 | List of roles and responsibilities                               |   ✅/🔶   | organization/role-definition.md                              |
| 3.1.2.2 | Documented competencies per role                                 |   ✅/🔶   | role-definition.md §2                                        |
| 3.1.2.3 | Evidence of competency assessment                                |   ✅/🔶   | training/completion-tracker.md                               |
| 3.1.3.1 | Evidence of participant awareness assessment                     |   ✅/🔶   | training/curriculum.md and completion-tracker.md             |
| 3.1.4.1 | Document defining the program scope                              |   ✅/🔶   | oss-policy.md §1                                             |
| 3.1.5.1 | Procedure for reviewing license obligations                      |   ✅/🔶   | process/usage-approval.md §4, policy/license-allowlist.md    |
| 3.2.1.1 | Public channel for external inquiries                            |   ✅/🔶   | role-definition.md §3                                        |
| 3.2.1.2 | Internal procedure for handling external inquiries               |   ✅/🔶   | role-definition.md §3                                        |
| 3.2.2.1 | Document naming the people holding each role                     |   ✅/🔶   | organization/raci-matrix.md (real names being entered)       |
| 3.2.2.2 | Confirmation of role staffing and budget                         |   ✅/🔶   | raci-matrix.md §Budget allocation status                     |
| 3.2.2.3 | Access to legal advice                                           |   ✅/🔶   | role-definition.md §4                                        |
| 3.2.2.4 | Internal responsibility assignment procedure                     |   ✅/🔶   | raci-matrix.md §Internal responsibility assignment procedure |
| 3.2.2.5 | Procedure for reviewing and correcting non-compliance            |   ✅/🔶   | raci-matrix.md §Non-compliance case review procedure         |
| 3.3.1.1 | SBOM management procedure                                        |   ✅/🔶   | sbom/sbom-management-plan.md                                 |
| 3.3.1.2 | Component record (SBOM file)                                     |   ✅/🔶   | sbom/[project].cdx.json                                      |
| 3.3.2.1 | Procedure for handling license use cases                         |   ✅/🔶   | sbom/license-report.md, process/usage-approval.md            |
| 3.4.1.1 | Procedure for preparing and distributing compliance deliverables |   ✅/🔶   | process/distribution-checklist.md                            |
| 3.4.1.2 | Procedure for retaining compliance deliverables                  |   ✅/🔶   | distribution-checklist.md §5                                 |
| 3.5.1.1 | Open source contribution policy                                  |   ✅/🔶   | oss-policy.md §5                                             |
| 3.5.1.2 | Open source contribution management procedure                    |   ✅/🔶   | oss-policy.md §5                                             |
| 3.5.1.3 | Procedure for awareness of the contribution policy               |   ✅/🔶   | oss-policy.md §7                                             |
| 3.6.1.1 | Document confirming all requirements are met                     |   ✅/🔶   | conformance/gap-analysis.md                                  |
| 3.6.2.1 | Confirmation that requirements were met within 18 months         |   ✅/🔶   | This document (declaration-draft.md)                         |

---

## ISO/IEC 18974:2023 checklist confirmation

| Item ID | Content                                                  | Satisfied | Deliverable                                                  |
| ------- | -------------------------------------------------------- | :-------: | ------------------------------------------------------------ |
| 4.1.1.1 | Documented security assurance policy                     |   ✅/🔶   | oss-policy.md §4                                             |
| 4.1.1.2 | Policy dissemination procedure                           |   ✅/🔶   | oss-policy.md §7, training/curriculum.md                     |
| 4.1.2.1 | List of roles and responsibilities                       |   ✅/🔶   | organization/role-definition.md §1                           |
| 4.1.2.2 | Documented competencies per role                         |   ✅/🔶   | role-definition.md §2                                        |
| 4.1.2.3 | List of participants and their roles                     |   ✅/🔶   | raci-matrix.md (real names being entered)                    |
| 4.1.2.4 | Evidence of competency assessment                        |   ✅/🔶   | training/completion-tracker.md                               |
| 4.1.2.5 | Evidence of periodic review and change                   |   ✅/🔶   | role-definition.md §6                                        |
| 4.1.2.6 | Owner verifying conformance to internal best practice    |   ✅/🔶   | role-definition.md §6                                        |
| 4.1.3.1 | Evidence of participant awareness assessment             |   ✅/🔶   | training/curriculum.md and completion-tracker.md             |
| 4.1.4.1 | Document defining the program scope                      |   ✅/🔶   | oss-policy.md §1                                             |
| 4.1.4.2 | Performance metrics                                      |   ✅/🔶   | oss-policy.md §3 (5 KPI items)                               |
| 4.1.4.3 | Evidence of continuous improvement (audit history)       |   ✅/🔶   | conformance/gap-analysis.md (audit round 1)                  |
| 4.1.5.1 | Standard vulnerability response procedure                |   ✅/🔶   | process/vulnerability-response.md                            |
| 4.2.1.1 | Public channel for external vulnerability inquiries      |   ✅/🔶   | role-definition.md §3 (security@{company domain})            |
| 4.2.1.2 | Internal procedure for handling external inquiries       |   ✅/🔶   | vulnerability-response.md §7                                 |
| 4.2.2.1 | Document naming the people holding each role             |   ✅/🔶   | raci-matrix.md (real names being entered)                    |
| 4.2.2.2 | Confirmation of role staffing and budget                 |   ✅/🔶   | raci-matrix.md §Budget allocation status                     |
| 4.2.2.3 | Stated expertise for remediating vulnerabilities         |   ✅/🔶   | role-definition.md §5                                        |
| 4.2.2.4 | Internal responsibility assignment procedure             |   ✅/🔶   | raci-matrix.md §Internal responsibility assignment procedure |
| 4.3.1.1 | Procedure for keeping SBOM records across the lifecycle  |   ✅/🔶   | sbom/sbom-management-plan.md                                 |
| 4.3.1.2 | Component record (SBOM file)                             |   ✅/🔶   | sbom/[project].cdx.json                                      |
| 4.3.2.1 | Procedure for detecting and resolving vulnerabilities    |   ✅/🔶   | vulnerability-response.md and remediation-plan.md            |
| 4.3.2.2 | Records of vulnerabilities and the actions taken         |   ✅/🔶   | vulnerability/cve-report.md and remediation-plan.md          |
| 4.4.1.1 | Document confirming all requirements are met             |   ✅/🔶   | conformance/gap-analysis.md                                  |
| 4.4.2.1 | Confirmation that requirements were met within 18 months |   ✅/🔶   | This document (declaration-draft.md)                         |

---

## Signature

This declaration confirms that all requirements of the standards above are met.

- **Declared by**: {name}, {title}
- **Declaration date**: YYYY-MM-DD
- **Next re-confirmation date**: YYYY-MM-DD
