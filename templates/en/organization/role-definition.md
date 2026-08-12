# Open Source Roles and Responsibilities Definition

<!-- 5230 §3.1.2.1·§3.1.2.2, 18974 §4.1.2.1·§4.1.2.2·§4.1.2.3 -->

**Company name**: {company name}
**Date written**: YYYY-MM-DD
**Author**: {author name}

---

## 1. Open source program role list

| Role                                       | Owner / department        | Key responsibilities                                                                                                               |
| ------------------------------------------ | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Open Source Program Manager                | {name}                    | Policy establishment, license review, external inquiry response                                                                    |
| Security Manager                           | {name / department}       | CVE scanning, vulnerability response                                                                                               |
| Legal Affairs                              | {name / external counsel} | License disputes, legal advice                                                                                                     |
| Development team representative            | {name}                    | Process compliance, SBOM updates                                                                                                   |
| Team champions (optional)                  | {team: name, ...}         | Open source contact point for each development team, policy dissemination. Name one person per team rather than writing "everyone" |
| Internal best practice reviewer (optional) | {name}                    | Periodic review of whether roles and processes match internal best practice, and recording the review evidence                     |

---

## 2. Required competencies per role

| Role                            | Required competencies                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------ |
| Open Source Program Manager     | Open source license fundamentals, SBOM tooling, understanding of OpenChain standards |
| Security Manager                | Understanding of CVE/CVSS, vulnerability analysis tooling, patch management          |
| Legal Affairs                   | Legal obligations of open source licenses, contract review                           |
| Development team representative | Usage approval process, basics of SBOM generation tooling                            |

---

## 3. External inquiry channels

<!-- 5230 §3.2.1.1, 18974 §4.2.1.1 -->

- **License compliance inquiries**: opensource@{company domain}
- **Security vulnerability reports**: security@{company domain}
- **Response owner**: {Open Source Program Manager name}
- **Target response time**: within {N business days}

---

## 4. Access to legal advice

<!-- 5230 §3.2.2.3 -->

- **Internal legal team**: {Yes / No}
- **Use of external legal counsel**: {law firm name / open source legal support service}

---

## 5. Vulnerability remediation expertise

<!-- 18974 §4.2.2.3 -->

- **Responsible organization**: {Security Team / name of the person holding this as an additional duty}
- **Available external resources**: {security consulting / national CERT support and similar}

---

## 6. Best practice conformance verification and periodic review

<!-- 18974 §4.1.2.5, §4.1.2.6 -->

### Verification owner

- **Verification owner**: {name / title}
- **Review cycle**: {once a year / twice a year}
- **First scheduled review date**: YYYY-MM-DD

### Periodic review method

<!-- 18974 §4.1.2.5 - evidence of periodic review of the role list and participants -->

Review the role definitions and the list of participants as follows:

1. The reviewer compares the current role list against the people actually holding each role
2. Identify changes such as a replaced owner or an added or removed role
3. If anything changed, update this document and reissue the appointment letter (appointment-template.md)
4. Record the completed review in the review history table below

### Review history

<!-- 18974 §4.1.2.5 - evidence of periodic review -->

| Review no.        | Review date | Reviewer | Summary of changes      | Notes |
| ----------------- | ----------- | -------- | ----------------------- | ----- |
| 1 (initial entry) | YYYY-MM-DD  | {name}   | Initial role definition |       |
| 2                 |             |          |                         |       |
| 3                 |             |          |                         |       |

---

## 7. Scaling options by organization size (optional)

As the organization grows and open source management becomes more complex, consider adding the governance structures below.

- **OSRB (Open Source Review Board)**: A committee that handles license, security, contribution, and release approvals. It is composed of the Open Source Program Manager and legal, security, and development representatives, and convenes once a month or when an issue arises.
- **OSPO (Open Source Program Office)**: An organization dedicated to open source strategy and governance. Consider formalizing it once there are three or more dedicated staff members.
