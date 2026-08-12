# Open Source RACI Matrix

<!-- 5230 §3.2.2.1·§3.2.2.2·§3.2.2.4, 18974 §4.2.2.1·§4.2.2.2·§4.2.2.4 -->

**Company name**: {company name}
**Date written**: YYYY-MM-DD

R=Responsible (does the work), A=Accountable (approves), C=Consulted (advises), I=Informed (is notified)

---

## RACI matrix

| Task                                                            | Open Source Program Manager | Development team | Security team | Legal | Management |
| --------------------------------------------------------------- | :-------------------------: | :--------------: | :-----------: | :---: | :--------: |
| Open source usage review and approval                           |              A              |        R         |       C       |   C   |     I      |
| License compliance review                                       |              R              |        C         |       I       |   C   |     I      |
| SBOM generation and management                                  |              A              |        R         |       I       |   I   |     I      |
| Vulnerability scanning and response                             |              C              |        R         |       R       |   I   |     I      |
| Policy establishment and update                                 |              R              |        C         |       C       |   C   |     A      |
| Running the training program                                    |              R              |        I         |       I       |   I   |     I      |
| Responding to external license inquiries                        |              R              |        C         |       I       |   C   |     I      |
| Responding to external vulnerability reports                    |              C              |        I         |       R       |   I   |     I      |
| Self-certification declaration                                  |              R              |        I         |       C       |   C   |     A      |
| **Approving open source contribution activity**                 |              A              |        R         |       I       |   C   |     I      |
| **Reviewing the release of internal projects**                  |              A              |        R         |       C       |   A   |     I      |
| **Overall response to external license and security inquiries** |              R              |        I         |       C       |   C   |     I      |

---

## Assignees per role

<!-- 5230 §3.2.2.1·§3.2.2.2 -->

| Role                            | Assignee name       | Department              | Email   | Dedicated / additional duty   |
| ------------------------------- | ------------------- | ----------------------- | ------- | ----------------------------- |
| Open Source Program Manager     | {name}              | {department}            | {email} | {dedicated / additional duty} |
| Development team representative | {name}              | {department}            | {email} | additional duty               |
| Security Manager                | {name / department} | {department}            | {email} | {dedicated / additional duty} |
| Legal Affairs                   | {name / external}   | {department / external} | {email} | {standing / on request}       |

---

## Budget allocation status

<!-- 5230 §3.2.2.2, 18974 §4.2.2.2 -->

| Item                       | Status                                        |
| -------------------------- | --------------------------------------------- |
| Dedicated staffing         | {N dedicated / N holding it as an extra duty} |
| Open source tooling budget | {yes / no / {amount} per year}                |
| Legal advice budget        | {yes / no / billed when needed}               |
| External training budget   | {yes / no / {amount} per year}                |

---

## Non-compliance case review procedure

<!-- 5230 §3.2.2.5 -->

When a license non-compliance case occurs:

1. The Program Manager establishes and records what was not complied with
2. Legal advice is used to assess how serious the violation is
3. A corrective action plan is drawn up (replacing the license, publishing source code, and so on)
4. The case is re-reviewed under the `output/process/usage-approval.md` process
5. The policy and processes are strengthened to prevent recurrence

---

## Internal responsibility assignment procedure

<!-- 5230 §3.2.2.4, 18974 §4.2.2.4 -->

When new open source related work arises:

1. The Open Source Program Manager defines the work
2. Assignees are allocated according to the RACI matrix
3. role-definition.md and this document are updated
