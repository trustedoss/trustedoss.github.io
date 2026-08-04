---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: G4.1 (3.6.1), G4.3 (3.6.2), G4.4 (3.6.2)'
  - 'ISO/IEC 18974: G4.2 (4.4.1), G4.3 (4.4.2), G4.4 (4.4.2)'
self_study_time: 2 hours
---

# Self-Certification Declaration: The Final Step

<Prerequisite>All deliverables from steps 2–6 (the entire `output/` folder)</Prerequisite>

## 1. What we do in this chapter

Congratulations on making it this far. You have now completed all the key areas of an open source management system: organizational structure, policy creation, process design, SBOM generation and management, vulnerability analysis, and the training program.

Let's review the full list of deliverables created so far. If you have all of these in place, you are ready to declare your self-certification:

| Folder                  | Deliverables                                                                                                                                                                             |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `output/organization/`  | role-definition.md, raci-matrix.md, appointment-template.md                                                                                                                              |
| `output/policy/`        | oss-policy.md, license-allowlist.md                                                                                                                                                      |
| `output/process/`       | usage-approval.md, distribution-checklist.md, vulnerability-response.md, inquiry-response.md, process-diagram.md (+ contribution-process.md, project-publication-process.md conditional) |
| `output/sbom/`          | [project].cdx.json, sbom-commands.sh, license-report.md, copyleft-risk.md, sbom-management-plan.md, sbom-sharing-template.md                                                             |
| `output/vulnerability/` | cve-report.md, remediation-plan.md                                                                                                                                                       |
| `output/training/`      | curriculum.md, completion-tracker.md, resources.md                                                                                                                                       |

In this chapter, we perform a gap analysis based on these deliverables, complete the self-certification declaration, and finish the official OpenChain registration.

---

## 2. Background knowledge: What is self-certification?

OpenChain Self-Certification is a way for an organization to declare that it meets the standard requirements without a third-party audit. Its key features are:

- **Self-declaration method**: The organization checks and declares the checklist itself, without an external audit agency.
- **Official recognition**: By registering on the OpenChain website, you receive official recognition from the OpenChain project.
- **Not legally binding**: Although it is not a legal obligation, it serves as a trust signal to supply chain partners.
- **Validity period of 18 months**: Per OpenChain guidance, rechecking every 18 months is recommended.

ISO/IEC 5230 (License Compliance) and ISO/IEC 18974 (Security Assurance) both provide a self-certification path, and simultaneous certification is also possible.

---

## 3. Final review before self-certification (self-study)

:::info Self-study mode (about 2 hours)
Additional work may be required depending on the results of the gap analysis. The conformance-preparer agent automatically scans the entire output/ folder to identify unmet items.
:::

Proceed in the following order:

1. Read this document until the end.
2. Run the conformance-preparer agent:

   :::tip Check before execution
   Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
   :::

   ```bash
   cd agents/07-conformance-preparer && claude
   ```

   The agent automatically scans the entire `output/` folder and generates a gap analysis report.

3. Open the generated `output/conformance/gap-analysis.md` and check for unmet items.
4. If any items are not met, return to the relevant chapter and supplement them.
5. Review and edit the `output/conformance/declaration-draft.md` declaration.
6. Register your self-certification on the OpenChain website, referring to `output/conformance/submission-guide.md`.

---

## 4. Understanding the gap analysis report

`output/conformance/gap-analysis.md` is created with the following structure:

| Section                   | Content                                                                           |
| ------------------------- | --------------------------------------------------------------------------------- |
| List of satisfied items   | Items that fully meet requirements and their supporting deliverables              |
| Partially satisfied items | Items that are partially met but need supplementation, and how to supplement them |
| Unmet items               | Items not yet met and links to their chapters                                     |
| Overall progress          | Ratio of satisfied / partially satisfied / unmet items (%)                        |

There is no need to panic if your gap analysis reveals unmet items. Each entry includes a link to the chapter you should return to. Partially satisfied items can often be converted to satisfied with only minor changes.

**§4.1.4.3 — How to handle continuous improvement audit evidence (initial certification):**

ISO/IEC 18974 §4.1.4.3 requires "audit evidence demonstrating continuous improvement." During initial certification, there is no history yet, so proceed as follows.

- **Initial certification**: The `gap-analysis.md` generated by the conformance-preparer agent is itself the first audit record. If this is stated in gap-analysis.md, the item is treated as partially satisfied and does not block the certification declaration.
- **Renewal certification (18 months later)**: Once you have two or more gap analysis records, the item becomes fully satisfied (✅).

**How to handle the two remaining time-based items (initial certification):**

For the same reason, the two items below are normally only partially satisfied at first certification, and this does not block the certification declaration.

- **§4.1.2.5 Evidence of periodic review**: Record the "next scheduled review date" in `gap-analysis.md` and the item is treated as partially satisfied. On renewal, one or more actual review records convert it to satisfied.
- **§4.1.2.6 Person responsible for verifying alignment with internal best practices**: Assign the verification owner in `role-definition.md` and the item is treated as partially satisfied. On renewal, one or more recorded review results convert it to satisfied.

**G4.5 — Confirming vulnerability remediation before distribution (18974 §4.3.2.2 · §4.4.1.1):**

ISO/IEC 18974 does not require zero known vulnerabilities. It requires a record of the action taken for each identified vulnerability — including a decision that no action is needed (§4.3.2.2) — plus documented evidence that the program meets the requirements (§4.4.1.1). If a vulnerability exists, handle it as follows:

| Situation                                                      | How to handle                                                                                                                      |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| The vulnerability is in the **actual distributed software**    | Declare after completing the patch before distribution. Record the completed action in `output/vulnerability/remediation-plan.md`. |
| A vulnerability exists but **mitigations have been completed** | Document the mitigation measures and remaining risks in `remediation-plan.md`; a conditional declaration is possible.              |
| The vulnerability is in a **practice sample**                  | Samples are not actual distributed software. Judge based on your actual distribution target product.                               |

:::info Declaration scope
Self-certification is a declaration about a specific software "scope." By clearly defining the scope (§3.1.4 / §4.1.4), you can make the declaration about actual products rather than practice samples.
:::

---

## 5. OpenChain self-certification declaration procedure

Once the gap analysis is complete and there are no unmet items (or a resolution plan is in place), proceed with official registration using the following steps:

**Step 1**: Do a final review of the contents of `output/conformance/declaration-draft.md` and confirm them.

**Step 2**: Download the self-certification checklist. The [OpenChain Reference-Material repository](https://github.com/OpenChain-Project/Reference-Material/tree/master/OpenChain-Standards-Self-Certification) hosts language-specific files under `Checklist/ISO-IEC-5230` and `Checklist/ISO-IEC-18974`. Download each one you intend to declare against.

**Step 3**: Answer each checklist item Yes/No as a self-assessment. The per-item verdicts in `declaration-draft.md` map directly onto it.

**Step 4**: Complete the online application form on the [OpenChain get-started page](https://openchainproject.org/get-started) to request listing. You do not upload the checklist itself; you submit company details on the premise that the self-assessment is done.

**Step 5**: Once listed, you appear among officially recognized companies and can use the OpenChain logo.

> This step meets the requirements of ISO/IEC 5230 G4.1 (3.6.1) and ISO/IEC 18974 G4.2 (4.4.1).

:::info Standard requirements met
Completing this lab meets the requirements below.

**ISO/IEC 5230**

| Item ID | Requirement                              | Self-certification checklist                                                                       |
| ------- | ---------------------------------------- | -------------------------------------------------------------------------------------------------- |
| 3.6.1   | Self-certification declaration           | Do you confirm that your program meets all the requirements of this specification?                 |
| 3.6.2   | Certification validity period management | Do you have a process to confirm the program meets the requirements at least once every 18 months? |

**ISO/IEC 18974**

| Item ID | Requirement                                       | Self-certification checklist                                                                                          |
| ------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 4.4.1   | Self-certification declaration (security)         | Do you confirm that your security assurance program meets all the requirements of this specification?                 |
| 4.4.2   | Security certification validity period management | Do you have a process to confirm the security assurance program meets the requirements at least once every 18 months? |

:::

---

## 6. Strategy for certifying both standards at once

ISO/IEC 5230 and ISO/IEC 18974 share many requirements. If simultaneous certification is your goal, the following strategy is efficient:

- **12 common items**: Items shared by both standards are met simultaneously in a single effort.
- **8 items for 5230 only**: Additional requirements specific to license compliance are met.
- **11 items for 18974 only**: Additional requirements specific to security assurance are met.

Recommended order of work: complete the common items first → then the ISO/IEC 5230-only items → then the ISO/IEC 18974-only items. This can save roughly **39% of the work**. The way the chapters in this kit are organized is designed to follow this order.

---

## 7. Post-certification maintenance

Self-certification is not a one-time event. It requires ongoing maintenance:

- **Annual policy review**: Review `output/policy/oss-policy.md` and `output/policy/license-allowlist.md` once a year and keep them up to date.
- **Handover when the program manager changes**: Follow a systematic handover process using the RACI matrix and the appointment letter template.
- **Response when a new version of a standard is released**: Re-run the gap analysis when revisions of ISO/IEC 5230 and ISO/IEC 18974 are released.
- **Recheck every 18 months**: As OpenChain recommends, reconfirm your self-certification every 18 months and declare a renewal when necessary.

> This step meets the requirements of ISO/IEC 5230 G4.3 (3.6.2) and ISO/IEC 18974 G4.3 (4.4.2).

---

## 8. Completion checklist

Check all items below before finishing this chapter:

- [ ] `output/conformance/gap-analysis.md` created
- [ ] `output/conformance/declaration-draft.md` created
- [ ] `output/conformance/submission-guide.md` created
- [ ] There are no unmet items in the gap analysis, or there are plans to resolve them
- [ ] Self-certification declaration completed

:::tip Example deliverables
You can see the actual format of the generated files in [Self-Certification Deliverables Best Practice](/reference/samples/conformance).
:::

---

## 9. Celebrate completion and next steps

Your organization's open source management system is now complete.

From organizational structure to policy, process, SBOM, vulnerability management, training, and the self-certification declaration — every element required by ISO/IEC 5230 and ISO/IEC 18974 has been systematically put in place. This achievement is a strong trust signal to your supply chain partners and customers, demonstrating the maturity of your open source management.

Ways to keep growing with the open source ecosystem after certification:

- **Participate in the OpenChain KWG community**: Share your experience with other companies in the Korean OpenChain community.
  https://openchain-project.github.io/OpenChain-KWG
- **Establish an in-house open source contribution policy**: Move from consumption to contribution — set up a policy for contributing to open source communities.
- **Consider establishing an OSPO (Open Source Program Office)**: Strengthen long-term capability by formalizing a team dedicated to open source management.

### Next: Scale with automation

Now that certification has defined what to do, the next step is enforcing it automatically in daily development.

- [AI Coding Tools and Open Source Compliance](/ai-coding/intro): Use Rules to keep AI coding tools such as Cursor, Copilot, and Claude Code within your policy.
- [DevSecOps](/devsecops/intro): Turn SBOM generation and vulnerability scanning into CI pipeline gates that automatically block policy violations.
