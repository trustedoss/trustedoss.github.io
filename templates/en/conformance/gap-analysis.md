# Gap Analysis Report

<!-- 5230 §3.6.1.1, §3.6.2.1 · 18974 §4.4.1.1, §4.4.2.1, §4.1.2.5, §4.1.2.6, §4.1.4.3 -->
<!-- This template has the same structure as the gap analysis 07-conformance-preparer generates:
     25 pieces of evidence per standard (50 in total when both are selected), compared by clause ID.
     docs/00-overview/checklist-mapping.md is the authoritative map of the G items (G1 to G4). -->

---

Report type: gap analysis ({ISO/IEC 5230 / ISO/IEC 18974 / both})
Generated: YYYY-MM-DD
Target project: {company name} open source program
Tool used: trustedoss agents/en/07-conformance-preparer

---

## 1. Summary

- Scope of the analysis: ISO/IEC 5230:2020 (25 items) plus ISO/IEC 18974:2023 (25 items) = 50 pieces of evidence
- **ISO/IEC 5230**: satisfied ✅ {N} / partially satisfied 🔶 {N} / not satisfied ❌ {N}
- **ISO/IEC 18974**: satisfied ✅ {N} / partially satisfied 🔶 {N} / not satisfied ❌ {N}
- ❌ Not satisfied (blocks certification): {none → the self-certification declaration can proceed / N items → see the actions below}
- The three time-based 🔶 items are normal at initial certification (they are satisfied at the 18-month renewal)

---

## 2. ISO/IEC 5230:2020 status by item

| Item ID | Summary                                                          | Verdict  | Supporting deliverable                                                 |
| ------- | ---------------------------------------------------------------- | :------: | ---------------------------------------------------------------------- |
| 3.1.1.1 | Documented open source policy                                    | ✅/🔶/❌ | output/policy/oss-policy.md                                            |
| 3.1.1.2 | Policy dissemination procedure                                   | ✅/🔶/❌ | oss-policy.md §7, curriculum.md                                        |
| 3.1.2.1 | List of roles and responsibilities                               | ✅/🔶/❌ | role-definition.md §1                                                  |
| 3.1.2.2 | Documented competencies per role                                 | ✅/🔶/❌ | role-definition.md §2                                                  |
| 3.1.2.3 | Evidence of competency assessment                                | ✅/🔶/❌ | completion-tracker.md                                                  |
| 3.1.3.1 | Evidence of participant awareness assessment                     | ✅/🔶/❌ | curriculum.md and completion-tracker.md                                |
| 3.1.4.1 | Scope of the program                                             | ✅/🔶/❌ | oss-policy.md §1                                                       |
| 3.1.5.1 | Procedure for reviewing license obligations                      | ✅/🔶/❌ | usage-approval.md §4, license-allowlist.md                             |
| 3.2.1.1 | Public channel for external inquiries                            | ✅/🔶/❌ | role-definition.md §3                                                  |
| 3.2.1.2 | Internal procedure for handling external inquiries               | ✅/🔶/❌ | role-definition.md §3, usage-approval.md                               |
| 3.2.2.1 | Document naming the people holding each role                     | ✅/🔶/❌ | raci-matrix.md                                                         |
| 3.2.2.2 | Confirmation of role staffing and budget                         | ✅/🔶/❌ | raci-matrix.md §Budget allocation status                               |
| 3.2.2.3 | Access to legal advice                                           | ✅/🔶/❌ | role-definition.md §4                                                  |
| 3.2.2.4 | Internal responsibility assignment procedure                     | ✅/🔶/❌ | raci-matrix.md §Internal responsibility assignment procedure           |
| 3.2.2.5 | Procedure for reviewing and correcting non-compliance            | ✅/🔶/❌ | raci-matrix.md §Non-compliance case review procedure, oss-policy.md §8 |
| 3.3.1.1 | SBOM management procedure                                        | ✅/🔶/❌ | sbom-management-plan.md, usage-approval.md §6                          |
| 3.3.1.2 | Component record (SBOM file)                                     | ✅/🔶/❌ | output/sbom/[project].cdx.json                                         |
| 3.3.2.1 | Procedure for handling license use cases                         | ✅/🔶/❌ | license-report.md, copyleft-risk.md, usage-approval.md                 |
| 3.4.1.1 | Procedure for preparing and distributing compliance deliverables | ✅/🔶/❌ | distribution-checklist.md                                              |
| 3.4.1.2 | Procedure for retaining compliance deliverables                  | ✅/🔶/❌ | distribution-checklist.md §5                                           |
| 3.5.1.1 | Open source contribution policy                                  | ✅/🔶/❌ | oss-policy.md §5                                                       |
| 3.5.1.2 | Open source contribution management procedure                    | ✅/🔶/❌ | oss-policy.md §5                                                       |
| 3.5.1.3 | Procedure for awareness of the contribution policy               | ✅/🔶/❌ | oss-policy.md §7                                                       |
| 3.6.1.1 | Document confirming all requirements are met                     | ✅/🔶/❌ | gap-analysis.md (this document)                                        |
| 3.6.2.1 | Document confirming requirements were met within 18 months       | ✅/🔶/❌ | declaration-draft.md                                                   |

**ISO/IEC 5230 subtotal: ✅ {N} / 🔶 {N} / ❌ {N}**

---

## 3. ISO/IEC 18974:2023 status by item

| Item ID | Summary                                                    | Verdict  | Supporting deliverable                                                  |
| ------- | ---------------------------------------------------------- | :------: | ----------------------------------------------------------------------- |
| 4.1.1.1 | Security assurance policy                                  | ✅/🔶/❌ | oss-policy.md §4                                                        |
| 4.1.1.2 | Policy dissemination procedure                             | ✅/🔶/❌ | oss-policy.md §7, curriculum.md                                         |
| 4.1.2.1 | List of roles and responsibilities                         | ✅/🔶/❌ | role-definition.md §1                                                   |
| 4.1.2.2 | Documented competencies per role                           | ✅/🔶/❌ | role-definition.md §2                                                   |
| 4.1.2.3 | List of participants and their roles                       | ✅/🔶/❌ | raci-matrix.md §Assignees per role                                      |
| 4.1.2.4 | Evidence of competency assessment                          | ✅/🔶/❌ | completion-tracker.md                                                   |
| 4.1.2.5 | Evidence of periodic review and change                     | ✅/🔶/❌ | oss-policy.md §9 (review plan in place, no history yet) — time-based    |
| 4.1.2.6 | Owner verifying conformance to internal best practice      | ✅/🔶/❌ | role-definition.md §6 (owner named, review due 2026-12-31) — time-based |
| 4.1.3.1 | Evidence of participant awareness assessment               | ✅/🔶/❌ | curriculum.md and completion-tracker.md                                 |
| 4.1.4.1 | Document defining the program scope                        | ✅/🔶/❌ | oss-policy.md §1                                                        |
| 4.1.4.2 | Performance metrics                                        | ✅/🔶/❌ | oss-policy.md §3 (5 KPI items)                                          |
| 4.1.4.3 | Evidence of continuous improvement (audit history)         | ✅/🔶/❌ | This gap analysis is audit round 1 — time-based                         |
| 4.1.5.1 | Standard vulnerability response procedure                  | ✅/🔶/❌ | vulnerability-response.md (covers all eight methods)                    |
| 4.2.1.1 | Public channel for external vulnerability inquiries        | ✅/🔶/❌ | role-definition.md §3 (security@techunicorn.example)                    |
| 4.2.1.2 | Internal procedure for handling external inquiries         | ✅/🔶/❌ | vulnerability-response.md §7                                            |
| 4.2.2.1 | Document naming the people holding each role               | ✅/🔶/❌ | raci-matrix.md                                                          |
| 4.2.2.2 | Confirmation of role staffing and budget                   | ✅/🔶/❌ | raci-matrix.md §Budget allocation status                                |
| 4.2.2.3 | Stated expertise for remediating vulnerabilities           | ✅/🔶/❌ | role-definition.md §5 (security team, national CERT support)            |
| 4.2.2.4 | Internal responsibility assignment procedure               | ✅/🔶/❌ | raci-matrix.md §Internal responsibility assignment procedure            |
| 4.3.1.1 | Procedure for keeping SBOM records across the lifecycle    | ✅/🔶/❌ | sbom-management-plan.md                                                 |
| 4.3.1.2 | Component record (SBOM file)                               | ✅/🔶/❌ | output/sbom/[project].cdx.json                                          |
| 4.3.2.1 | Procedure for detecting and resolving vulnerabilities      | ✅/🔶/❌ | vulnerability-response.md and remediation-plan.md                       |
| 4.3.2.2 | Records of vulnerabilities and the actions taken           | ✅/🔶/❌ | cve-report.md (5 CVEs recorded) and remediation-plan.md                 |
| 4.4.1.1 | Document confirming all requirements are met               | ✅/🔶/❌ | gap-analysis.md (this document)                                         |
| 4.4.2.1 | Document confirming requirements were met within 18 months | ✅/🔶/❌ | declaration-draft.md                                                    |

**ISO/IEC 18974 subtotal: ✅ {N} / 🔶 {N} / ❌ {N}**

---

## 4. Actions (plan for closing what is not satisfied or only partially satisfied)

| Item ID | How to close it                                     | Owner  | Target date |
| ------- | --------------------------------------------------- | ------ | ----------- |
| {item}  | {re-run the relevant agent, or complete it by hand} | {name} | YYYY-MM-DD  |

---

## 5. Handling time-based items (normal at initial certification)

<!-- Items where partial satisfaction is normal at initial certification -->

| Item                                                       | Plan                               | Next review date        |
| ---------------------------------------------------------- | ---------------------------------- | ----------------------- |
| 18974 §4.1.2.5 evidence of periodic review                 | {review cycle and owner}           | YYYY-MM-DD              |
| 18974 §4.1.2.6 verification against internal best practice | {name the verification owner}      | YYYY-MM-DD              |
| 18974 §4.1.4.3 evidence of continuous improvement          | This gap analysis is audit round 1 | At renewal (YYYY-MM-DD) |

---

## 6. Renewal schedule and audit history

<!-- 18974 §4.1.4.3 evidence of continuous improvement -->

| Round       | Date       | Owner  | Main findings                 | Follow-up                                  |
| ----------- | ---------- | ------ | ----------------------------- | ------------------------------------------ |
| 1 (initial) | YYYY-MM-DD | {name} | Initial gap analysis complete | Closing the unsatisfied items is under way |

- Self-certification validity: 18 months from the declaration date
- Re-declaration (renewal) date: YYYY-MM-DD
