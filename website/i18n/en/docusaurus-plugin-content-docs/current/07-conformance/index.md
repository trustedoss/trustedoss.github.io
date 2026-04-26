---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: G4.1 (3.6.1), G4.3 (3.6.2), G4.4 (3.6.2)'
  - 'ISO/IEC 18974: G4.2 (4.4.1), G4.3 (4.4.2), G4.4 (4.4.2)'
self_study_time: 2 hours
---

# Self-certification declaration:final step

## 1. What we do in this chapter

Congratulations on making it this far. Organization structure so far,policy making,process design,SBOM creation and management,Vulnerability Analysis,All key areas of the open source management system, including the establishment of an education system, have been completed.

Let's look at the full list of artifacts created so far. If you have all of this in place, you are ready to declare your self-certification.:

| folder                  | output                                                                                                                                                                                  |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `output/organization/`  | role-definition.md, raci-matrix.md, appointment-template.md                                                                                                                             |
| `output/policy/`        | oss-policy.md, license-allowlist.md                                                                                                                                                     |
| `output/process/`       | usage-approval.md, distribution-checklist.md, vulnerability-response.md, inquiry-response.md, process-diagram.md (+ contribution-process.md,project-publication-process.md conditional) |
| `output/sbom/`          | [project].cdx.json, sbom-commands.sh, license-report.md, copyleft-risk.md, sbom-management-plan.md, sbom-sharing-template.md                                                            |
| `output/vulnerability/` | cve-report.md, remediation-plan.md                                                                                                                                                      |
| `output/training/`      | curriculum.md, completion-tracker.md, resources.md                                                                                                                                      |

In this chapter, we perform gap analysis based on these outputs and,Complete the self-certification declaration and complete OpenChain official registration.

---

## 2. Background knowledge:What is self-certification?

OpenChain Self-authentication(Self-Certification)is a way for an organization to declare that it meets the standard requirements without a third-party audit. Key features include::

- **Self-declaration method**:The organization itself checks and declares the checklist without an external audit agency.
- **Official recognition**:By registering on the OpenChain website, you receive official recognition from the OpenChain project.
- **Not legally binding**:Although it is not a legal obligation,It serves as a trust signal to supply chain partners.
- **Validity period: 18 months**:Rechecking is recommended every 18 months as per OpenChain advisory.

ISO/IEC 5230(License Compliance)and ISO/IEC 18974(security assurance)Both standards provide their own certification paths and,Simultaneous authentication is also possible.

---

## 3. Final inspection before self-certification(self study)

:::info Self-study mode(About 2 hours)
Additional work may be required depending on the results of the gap analysis. The conformance-preparer agent automatically scans the entire output/ folder to identify non-conformance items.
:::

Proceed in the following order:

1. Read this document until the end.
2. Run conformance-preparer agent:

   :::tip Check before execution
   Terminate the current Claude session first(`/exit` or `Ctrl+C`)After doing it,Run the command below in a new terminal.
   :::

   ```bash
   cd agents/07-conformance-preparer && claude
   ```

   The agent automatically scans the entire `output/` and generates a gap analysis report.

3. Open the generated `output/conformance/gap-analysis.md` and check for unmet items.
4. If any items are not met, go back to the relevant chapter and supplement them.
5. Review and edit the `output/conformance/declaration-draft.md` declaration.
6. Register your self-certification on the OpenChain website, referring to `output/conformance/submission-guide.md`.

---

## 4. Understanding the gap analysis report

`output/conformance/gap-analysis.md` is created with the following configuration::

| section                   | Content                                                                          |
| ------------------------- | -------------------------------------------------------------------------------- |
| List of meeting items     | Items and supporting deliverables that fully meet requirements                   |
| Partially satisfied items | Items that are partially met but need supplementation and how to supplement them |
| Items not met             | Items not yet met and their chapter links                                        |
| Overall progress          | Satisfied/Partially Satisfied/Not Satisfied Ratio(%)                             |

There is no need to panic if your gap analysis reveals unmet items. Each entry includes a link to return to which chapter. Partially satisfied items can often be converted to satisfied with only minor modifications.

**§4.1.4.3 — How to handle continuous improvement audit evidence(initial authentication):**

ISO/IEC 18974 §4.1.4.3 requires “audit evidence demonstrating continuous improvement.” During initial authentication, there is no history yet, so proceed as follows.

- **Initial Certification**:The `gap-analysis.md` itself generated by the conformance-preparer agent is the first audit trail. Partially satisfied if this fact is specified in gap-analysis.md(🔶)It is processed and does not prevent authentication declarations.
- **Renewal Certification(18 months later)**:Fully satisfied if two or more gap analysis records are obtained.(✅)This happens.

**G4.5 — Verify that distributed software has no known vulnerabilities(18974 §4.4.1.1)Processing method:**

This item is a requirement to “verify and declare that the distributed software has no known vulnerabilities.” If there is a vulnerability, handle it as follows::

| Situation                                                         | Processing method                                                                                                        |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| If the vulnerability is in the **actual distributed software**    | Declared after patch completion before distribution. Log action completion in `output/vulnerability/remediation-plan.md` |
| If a vulnerability exists but **mitigations have been completed** | Mitigation measures and remaining risks can be documented in `remediation-plan.md` and conditionally declared            |
| In case of vulnerability in **Practice sample**                   | Samples are not actual distributed software.,Judgment based on actual distribution target product                        |

> Self-certification is a declaration of specific software “scope”. range(§3.1.4 / §4.1.4)By clearly defining , you can make the declaration about actual products rather than practice samples.

---

## 5. OpenChain Self-certification declaration procedure

If the gap analysis is completed and there are no unmet items or a resolution plan has been prepared, proceed with official registration through the following procedures.:

**Step 1**:`output/conformance/declaration-draft.md` Final review and confirmation of contents.

**Step 2**:https in browser:Access //www.openchainproject.org/conformance.

**Step 3**:Select the standard you want to certify to: ISO/IEC 5230 or ISO/IEC 18974.(Or choose both standards)

**Step 4**:Complete and submit the online self-certification checklist. You can complete it quickly by referring to the contents of `declaration-draft.md`.

**Step 5**:Once registration is complete, you can use the OpenChain logo.,Listed on the list of officially recognized companies.

> This step is ISO/IEC 5230 G4.1(3.6.1)and ISO/IEC 18974 G4.2(4.4.1)Meets your requirements.

:::info Standard requirements met
Completing this lab will meet the requirements below:

**ISO/IEC 5230**

| Item ID | Requirements                             | Self-certification checklist                                                                       |
| ------- | ---------------------------------------- | -------------------------------------------------------------------------------------------------- |
| 3.6.1   | Self-certification declaration           | Do you confirm that your program meets all the requirements of this specification?                 |
| 3.6.2   | Certification validity period management | Do you have a process to confirm the program meets the requirements at least once every 18 months? |

**ISO/IEC 18974**

| Item ID | Requirements                                       | Self-certification checklist                                                                                          |
| ------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 4.4.1   | Self-certification declaration(security)           | Do you confirm that your security assurance program meets all the requirements of this specification?                 |
| 4.4.2   | Security authentication validity period management | Do you have a process to confirm the security assurance program meets the requirements at least once every 18 months? |

:::

---

## 6. Two standards simultaneous authentication strategy

ISO/IEC 5230 and ISO/IEC 18974 share many requirements. If simultaneous authentication is the goal, the following strategy is efficient::

- **10 common items**:Items shared by both standards are met simultaneously in one operation.
- **6 for 5230 only**:Additional requirements specific to license compliance are met.
- **18974 only 9**:It additionally satisfies special security assurance requirements.

Recommended Order of Action:Complete common items first → ISO/IEC 5230 only items → By proceeding with ISO/IEC 18974-specific items, you can achieve approximately **40% work savings**. The organization of the chapters in this kit itself is designed to follow this order.

---

## 7. Post-certification maintenance

Self-certification does not end once. Requires ongoing maintenance:

- **Policy review once a year**:Review `output/policy/oss-policy.md` and `output/policy/license-allowlist.md` once a year and keep them up to date.
- **Handover when person in charge changes**:Follow a systematic handover process using the RACI matrix and appointment letter template.
- **Response when new version standard is released**:We will re-perform the gap analysis when revisions to ISO/IEC 5230 and ISO/IEC 18974 are released.
- **Recheck every 18 months**:OpenChain As recommended, we reconfirm our own certification every 18 months and declare renewal when necessary.

> This step is ISO/IEC 5230 G4.3(3.6.2)and ISO/IEC 18974 G4.3(4.4.2)Meets your requirements.

---

## 8. Completion Confirmation Checklist

Check all items below before finishing this chapter:

- [ ] `output/conformance/gap-analysis.md` created
- [ ] `output/conformance/declaration-draft.md` created
- [ ] `output/conformance/submission-guide.md` created
- [ ] There are no unmet items in the gap analysis or there are plans to resolve them.
- [ ] Self-certification declaration completed

> 📋 **Example of output**: [Self-certified output Best Practice](/reference/samples/conformance)You can check the actual format of the generated file at .

---

## 9. Celebrate completion and next steps

Your open source management system is now complete.

From organizational structure to policy,process, SBOM,Vulnerability Management,education,And even the self-certification declaration — all elements required by ISO/IEC 5230 and ISO/IEC 18974 were systematically met. This achievement will be a strong signal of confidence to your supply chain partners and customers that demonstrates your open source management maturity.

Ways to grow with the open source ecosystem even after certification:

- **OpenChain KWG Community Participation**:We share our experiences with other companies in the domestic OpenChain community.
  https://openchain-project.github.io/OpenChain-KWG
- **Establishment of an in-house open source contribution policy**:From consumption to contribution — Establish policies that contribute to the open source community.
- **OSPO(Open Source Program Office)Establishment review**:Strengthen long-term capabilities by formalizing an organization dedicated to open source management.
