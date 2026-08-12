# Open Source Contribution Procedure

<!-- 5230 §3.5.1.2 (G3L.6) -->

**Company name**: {company name}
**Date written**: YYYY-MM-DD
**Owner**: {Open Source Program Manager}

This process document is based on the OpenChain KWG process guide (the open source contribution process) and on ISO/IEC 5230 and 18974. The KWG guide is licensed under CC BY 4.0.

---

## 1. Review before contributing

<!-- 5230 §3.5.1.2 - contribution management procedure -->

Check the following before contributing to an external open source project:

| Item to check                                             | How to check                       | Owner       |
| --------------------------------------------------------- | ---------------------------------- | ----------- |
| License of the target project                             | Read the LICENSE file              | Contributor |
| Whether company IP (patents, trade secrets) is included   | Complete the IP checklist          | Legal       |
| Whether a CLA (Contributor License Agreement) is required | Check the project CONTRIBUTING.md  | Contributor |
| Whether the contribution relates to company work          | Confirmation by the direct manager | Manager     |

Information to submit with a contribution request:

- Name and repository URL of the target project
- Summary of the contribution (bug fix / new feature / documentation, and so on)
- Whether patent-related technology is included (yes/no)
- Whether third-party libraries are included (yes/no)

---

## 2. Approval criteria per contribution type

<!-- 5230 §3.5.1.2 - managing open source contributions -->

| Contribution type                       | Approval steps required     | Criteria                          |
| --------------------------------------- | --------------------------- | --------------------------------- |
| Typo and documentation fixes            | Manager approval            | Confirm no company IP is included |
| Bug fixes                               | OSPM review                 | Confirm license compatibility     |
| New features                            | OSPM and legal review       | Review IP and patent impact       |
| Starting to contribute to a new project | OSPM, legal, and management | Includes a strategic review       |

---

## 3. CLA handling procedure

<!-- 5230 §3.5.1.2 - contribution procedure -->

When contributing to a project that requires a CLA:

1. **Review the CLA**: The legal team reviews the CLA clauses to see whether any are unfavourable to the company
2. **Approve signing**: The OSPM gives final approval on whether to sign the CLA
3. **How to sign**: Individual signature or corporate CLA signature (according to the project's policy)
4. **Record retention**: Retain a copy of the signed CLA per [5. Contribution history retention]

Grounds for refusing to sign a CLA:

- The CLA contains a clause requiring the contributor to give up company IP
- The CLA contains a clause that affects the company's patents

---

## 4. Requirements while contributing

<!-- 5230 §3.5.1.2 -->

What to comply with when contributing after approval:

- [ ] Copyright statement: `Copyright (c) {year} {company name}`
- [ ] State the SPDX license identifier (according to the project's policy)
- [ ] Use the company email address: `{name}@{company domain}`
- [ ] Do not include trade secrets or internal system information
- [ ] Confirm that the contribution stays within the approved scope

---

## 5. Contribution history retention

<!-- 5230 §3.5.1.2 - recording contribution history -->

Record the information below for every open source contribution and retain it for **at least 3 years**:

| Retained item               | Example                          |
| --------------------------- | -------------------------------- |
| Contribution date           | 2025-03-01                       |
| Project and repository URL  | github.com/project/repo          |
| Summary of the contribution | Bug fix #1234                    |
| Approved by                 | {OSPM name}                      |
| Whether a CLA was signed    | Yes / No                         |
| Pull request URL            | github.com/project/repo/pull/456 |

Retention location: {internal wiki / shared drive / Git repository}
Retention period: **at least 3 years from the contribution date**
