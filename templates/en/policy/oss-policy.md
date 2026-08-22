# Open Source Policy

<!-- 5230 §3.1.1.1, §3.1.4.1, §3.1.5.1, §3.5.1.1·§3.5.1.2 -->
<!-- 18974 §4.1.1.1, §4.1.4.1·§4.1.4.2 -->

**Company name**: {company name}
**Version**: 1.0
**Date written**: YYYY-MM-DD
**Author**: {Open Source Program Manager name}
**Approved by**: {name of the approver}
**Next review date**: YYYY-MM-DD (date written + 1 year)

This policy document is based on the OpenChain KWG open source policy template (§1 to §11) and on ISO/IEC 5230 and 18974. The KWG guide is licensed under CC BY 4.0.

---

## 1. Purpose and scope

<!-- 5230 §3.1.1.1, 18974 §4.1.1.1 -->

This policy sets out how {company name} (hereafter "the company") uses open source software correctly while developing and distributing software, fulfils license obligations, and manages security vulnerabilities.

### Scope of application

<!-- 5230 §3.1.4.1, 18974 §4.1.4.1 -->

This policy applies to the following:

- **Target software**: {product or service name} — {version, or "all products"}
- **Distribution methods**: {SaaS / app store distribution / embedded / internal use}
- **Applicable personnel**: All members involved in open source use, including developers, managers, and purchasing or procurement staff
- **Exclusions**: {none / specific exclusions}

---

## 2. Open source usage principles

<!-- 5230 §3.1.5.1 license obligation review, 18974 §4.1.1.1 security assurance -->

### Mandatory review before use

Review all of the following before adopting new open source or changing the version of existing open source:

1. **License check**: Compare against the allowed license list in `output/policy/license-allowlist.md`
2. **License obligation fulfilment plan**: For copyleft licenses, decide how obligations such as publishing source code will be met
3. **Known vulnerability check**: Generate an SBOM and run a CVE scan to confirm there are no Critical or High vulnerabilities
4. **Owner approval**: Approve according to the `output/process/usage-approval.md` procedure

### License classification criteria

| Classification   | Examples             | Obligations when distributing                    |
| ---------------- | -------------------- | ------------------------------------------------ |
| Permissive       | MIT, Apache-2.0, BSD | Copyright notice, license notice                 |
| Weak Copyleft    | LGPL, MPL            | Publish the source code of modified files        |
| Strong Copyleft  | GPL-2.0, GPL-3.0     | Publish the full source code (when distributing) |
| Network Copyleft | AGPL-3.0             | Publish source code including for network use    |

### SBOM submission obligation to customers (conditional)

<!-- Include this subsection only when 03-policy-generator Q4 (do you deliver software to external
     customers or clients) is answered "yes". If "no", omit this subsection entirely and keep a single
     line instead: "SBOMs are kept in output/sbom/ for internal management purposes." -->

When delivering software to external customers or clients, follow the SBOM (Software Bill of Materials) submission procedure below.

- **Submission format**: CycloneDX or SPDX (follow the customer's required format when specified)
- **Submission timing**: at initial delivery and whenever an updated SBOM is needed after a component change
- **Required license information**: per-component license, version, and known vulnerability status
- **Customer license requirements**: reflect any license restrictions from the delivery contract (for example, a ban on bringing in copyleft components) in `output/policy/license-allowlist.md`

---

## 3. Program scope and performance metrics

<!-- 18974 §4.1.4.1, §4.1.4.2 -->

### Performance metrics (KPI)

The targets this program has to meet:

| Metric                      | Target                                                                                          |
| --------------------------- | ----------------------------------------------------------------------------------------------- |
| SBOM freshness              | An up-to-date SBOM attached to every release                                                    |
| License compliance rate     | 100% of newly adopted components reviewed in advance                                            |
| CVE scan cycle              | Every release, plus a regular monthly scan                                                      |
| Vulnerability response time | Critical: 1 week, High: 4 weeks, Medium: within 1 month                                         |
| Vulnerability response rate | 90% or more resolved within the deadline (document the reason and mitigation plan for the rest) |
| Training completion rate    | 100% completion per year for roles that touch open source                                       |
| Renewal cycle               | Re-confirm the self-certification every 18 months                                               |

**Note**: These vulnerability deadlines are the OpenChain KWG guide baseline. Depending on the risk profile and capability of the organization, a stricter internal SLA such as 24 hours for Critical and one week for High can be applied.

### Measuring and improving program effectiveness

- **Regular evaluation cycle**: Evaluate KPI achievement and process compliance at least once a year.
- **Evaluation reporting**: Report evaluation results to management; for unmet items, include the cause and an improvement plan.
- **Continuous improvement**: Update the policy and processes based on evaluation results, internal best practices, and industry trends (see the policy review and update section for the update cycle).
- **Resource sufficiency review**: Once a year, assess whether open source management staffing and tool budgets are sufficient, and recommend adjustments if necessary.

---

## 4. Security assurance policy

<!-- 18974 §4.1.1.1 -->

The company systematically identifies, tracks, and responds to known vulnerabilities (CVEs) in the software it distributes:

- Run an SBOM-based vulnerability scan before every release
- Critical and High vulnerabilities must be resolved before distribution, or have a mitigation plan
- When a new vulnerability is found after distribution, respond according to `output/process/vulnerability-response.md`
- Operate an external vulnerability reporting channel: security@{company domain}

---

## 5. AI-generated code policy

<!-- Recommended by the KWG open source guide -->
<!-- Always included in the default output of 03-policy-generator. If the organization does not use AI
     coding tools, state that explicitly in "Permitted and restricted uses" below.
     Because section numbering can still shift between generated documents, refer to sections of this policy by name rather than by number in other documents. -->

When AI code generation tools such as GitHub Copilot or ChatGPT are used, open source license obligations may still apply to the generated code, so the following criteria apply.

### Principles for using AI-generated code

1. **Review obligation**: When AI-generated code is included in a product, review it for open source license compliance exactly as ordinary open source is reviewed.
2. **Recognising that provenance cannot be traced**: The origin of the training data behind AI-generated code is hard to pin down, so verification with a source code scanning tool (such as SCANOSS) is recommended.
3. **Checking each tool's terms of service**: Check and comply with the copyright and license conditions for generated code in the terms of service of the AI coding tool in use.
4. **Meeting IP indemnification conditions**: Use paid commercial plans that carry supplier IP indemnification, and standardise settings so the indemnification conditions (such as the approved scope of use) are met. Personal free accounts are not used on company code.
5. **Recording copyright attribution**: State it in the commit message when AI output is used as is, and record the design and modification decisions a person made in the pull request body when an AI draft was edited.
6. **Disclosing AI use**: Disclose the use of AI tools in README or CONTRIBUTING for externally published repositories. When generative AI features are provided to users as part of a product, review the disclosure obligations of the applicable regulations (EU AI Act Article 50, Korea AI Framework Act Article 31) with the legal team.

### Permission and restrictions

- {Allowed: use after review / Restricted: specific tools prohibited / Allowed: internal AI tools only}

---

## 6. Open source contribution policy

<!-- 5230 §3.5.1.1 documented contribution policy, §3.5.1.2 contribution management procedure -->

### Whether contributions are allowed

- {Contributions allowed / contributions prohibited / allowed after prior approval}

### Requirements when contributing (if allowed)

1. **Prior approval**: Approved after review by the Open Source Program Manager and the legal team
2. **IP check**: Check whether the contribution contains company confidential information or third-party IP
3. **License agreement**: Check whether a CLA (Contributor License Agreement) has to be signed
4. **Record keeping**: Record the contribution following the retention location and period set in §9 (Record management)

---

## 7. Policy dissemination and training

<!-- 5230 §3.1.1.2, 18974 §4.1.1.2 -->

This policy is disseminated to everyone taking part in the program by:

- Including it in new-hire onboarding training
- Training (or a notice) for all members once a year
- Publishing it on the internal wiki or shared drive and sharing the link
- Training completion records: `output/training/completion-tracker.md`

---

## 8. Handling non-compliance

<!-- 5230 §3.2.2.5 -->

When this policy is violated:

1. Report to the Open Source Program Manager immediately
2. Establish what was violated and how far the impact reaches
3. Draw up and carry out a corrective action plan
4. Strengthen the policy or process to prevent recurrence

---

## 9. Records management

<!-- 5230 §3.4.1.2, 18974 §4.3.2.2 -->

All records related to running the open source program are retained for the periods below:

| Record type                                        | Retention period                                 | Location              |
| -------------------------------------------------- | ------------------------------------------------ | --------------------- |
| Compliance deliverables (SBOM, attribution notice) | At least 3 years from the distribution date      | {internal repository} |
| Vulnerability response history                     | At least 3 years from the last distribution date | {internal repository} |
| External inquiry response records                  | At least 3 years from closure                    | {internal repository} |
| Training completion records                        | At least 3 years from completion                 | {internal repository} |
| Open source contribution history                   | At least 3 years from the contribution date      | {internal repository} |
| Internal project release records                   | At least 3 years from the release date           | {internal repository} |
| Policy and approval documents                      | At least 3 years from the last revision date     | {internal repository} |

Before a retention period expires, the Open Source Program Manager reviews whether the record is still needed and decides whether to extend or dispose of it.

---

## 10. Policy review and update

<!-- 18974 §4.1.1.1 review process (G1.2) -->

This policy is reviewed and updated on the cycle below, or when one of the listed triggers occurs:

- **Regular review**: Once a year (next review date: YYYY-MM-DD)
- **Ad hoc review triggers**: Standard revisions, regulatory changes, major incidents, change of the Program Manager
- **Review owner**: {Open Source Program Manager}, with legal team confirmation
- **Review history**:

| Version | Review date | Main changes  | Approved by |
| ------- | ----------- | ------------- | ----------- |
| 1.0     | YYYY-MM-DD  | Initial entry | {name}      |

---

## 11. Policy change requests and operation

<!-- 18974 §4.1.1.1 operation (G1.2), 5230 §3.1.5.1 -->

Where §10 sets out _when_ the policy is reviewed, this section sets out how _anyone can request a change_ during operation and how such requests are handled.

### Change request flow

1. **Request**: A member who needs a change to the policy or to the allowed license list requests it from the Open Source Program Manager (for example, adding a new license or making an exception to a prohibited license).
2. **Assessment**: The Open Source Program Manager reviews the license obligations and the security and business impact, and obtains legal confirmation where necessary.
3. **Approval**: {The approver} approves. An approved exception is recorded together with its validity period and conditions.
4. **Application**: On approval, update the policy or `output/policy/license-allowlist.md` and leave an entry in the §10 review history.
5. **Notification**: Disseminate the change to everyone taking part in the program (using the channels in §7).

### Monitoring regulatory and standards change

- **Owner**: {The Open Source Program Manager} reviews relevant regulatory and standards developments (EU CRA, national SBOM mandates, ISO revisions, and so on) at least once a quarter.
- **Application**: When a change affects the policy, update it through the change request procedure above.

---

## Appendix A. Definitions

<!-- Corresponds to KWG policy template §2 (definitions) -->

The main terms used in this policy are as follows.

| Term                     | Definition                                                                                                                                                                              |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SBOM                     | Software Bill of Materials. The list of open source components, versions, and licenses contained in a product (SPDX or CycloneDX format).                                               |
| License obligation       | Conditions that have to be met when using open source, such as notices, copyright statements, and publishing source code.                                                               |
| Copyleft                 | A license type that requires derivative works to be published under the same license (GPL, AGPL, and similar).                                                                          |
| Permissive               | A license type with few restrictions, mainly notice obligations (MIT, Apache-2.0, BSD, and similar).                                                                                    |
| Vulnerability (CVE)      | A publicly identified security defect. Severity is expressed as a CVSS score.                                                                                                           |
| Distribution participant | A member involved in providing the company's software to external parties.                                                                                                              |
| Self-certification       | The procedure for declaring on your own that OpenChain (ISO/IEC 5230 and 18974) requirements are met.                                                                                   |
| OSPO                     | Open Source Program Office. The industry term for an organization dedicated to open source management. Corresponds to the "open source organization" in this policy.                    |
| OSPM                     | Open Source Program Manager. The industry term for the manager of an open source program. Corresponds to the "Open Source Program Manager" in this policy.                              |
| OSRB                     | Open Source Review Board. The industry term for the review board that deliberates on open source use and release. Smaller organizations can substitute a review by the Program Manager. |

The body of this policy uses a single term, "Open Source Program Manager", so that beginners can follow it.
Use the mapping above when comparing this policy with external documents or the KWG template.

## Appendix B. Releasing internal projects

<!-- Corresponds to KWG policy template §8 (releasing internal projects as open source) -->

Releasing internally developed software as open source goes through prior approval, intellectual property and security review, license selection, notice preparation, and post-release management. Follow `output/process/project-publication-process.md` (a process deliverable) for the detailed procedure. If that deliverable does not exist, generate it with the `process-designer` agent.
