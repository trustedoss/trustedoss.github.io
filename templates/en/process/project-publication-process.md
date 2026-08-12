# Internal Project Open Source Release Procedure

<!-- 5230 §3.5.1 (community participation) -->

**Company name**: {company name}
**Date written**: YYYY-MM-DD
**Owner**: {Open Source Program Manager}

This process document is based on the OpenChain KWG process guide (the internal project release process) and on ISO/IEC 5230 and 18974. The KWG guide is licensed under CC BY 4.0.

---

## 1. Review before release

<!-- 5230 §3.5.1 - open source community participation policy -->

Check the following before releasing an internal project as open source:

| Item to check                                                    | How to check              | Owner            |
| ---------------------------------------------------------------- | ------------------------- | ---------------- |
| Whether company IP (patents, trade secrets) is included          | Complete the IP checklist | Legal            |
| License compatibility of third-party libraries                   | SBOM analysis             | OSPM             |
| Whether personal data or internal system information is included | Code review               | Development team |
| Prior security vulnerability check                               | Run static analysis tools | Security Manager |
| Purpose of the release and its strategic soundness               | Management review         | Manager          |

Information to submit with a release review request:

- Project name and repository URL (internal)
- Purpose of the release and the expected benefit
- License to be used (including the reason for choosing it)
- List of third-party libraries

---

## 2. License selection criteria

<!-- 5230 §3.5.1 -->

| Purpose of the release              | Recommended license | Reason                                        |
| ----------------------------------- | ------------------- | --------------------------------------------- |
| Maximum adoption                    | MIT, Apache 2.0     | No restriction on commercial use              |
| Encouraging community contributions | GPL v2/v3, AGPL     | Copyleft obligations bring contributions back |
| Patent protection needed            | Apache 2.0          | Includes an explicit patent grant             |
| Releasing a library                 | LGPL, MPL           | Usable independently, weak copyleft           |

The final license choice is a joint decision by the OSPM and the legal team.

---

## 3. Preparing for release

<!-- 5230 §3.5.1 - release preparation procedure -->

Preparing the repository after release approval:

- [ ] Remove sensitive information (API keys, passwords, internal URLs, and so on)
- [ ] Configure `.gitignore` and `.gitattributes`
- [ ] Add a `LICENSE` file (the full text of the chosen license)
- [ ] Write `README.md` (installation, usage, how to contribute)
- [ ] Write `CONTRIBUTING.md` (contribution guidelines, whether a CLA applies)
- [ ] Write `SECURITY.md` (how to report vulnerabilities)
- [ ] Check the copyright statement: `Copyright (c) {year} {company name}`
- [ ] Confirm the commit history contains no sensitive information

---

## 4. Approval stages

| Stage                    | Approver         | Approval criteria                           |
| ------------------------ | ---------------- | ------------------------------------------- |
| 1st: technical review    | Development lead | Code quality, no security vulnerabilities   |
| 2nd: IP and legal review | Legal team       | No infringement of patents or trade secrets |
| 3rd: final approval      | OSPM             | License choice, strategic fit               |

---

## 5. Maintenance plan after release

Carry out the following continuously after the release:

- **Pull request and issue review**: {owner} reviews new pull requests and issues within {N business days}
- **Vulnerability response**: Handle reported vulnerabilities per the `vulnerability response procedure`
- **Release management**: Tag and write release notes for significant changes
- **Continued license obligation fulfilment**: Re-check license compatibility whenever a dependency is added

Criteria for discontinuing maintenance: the business purpose no longer exists, or management decides to stop. Notify the community in advance before stopping.

---

## 6. Release record retention

Retain the record of every released open source project for **at least 3 years**, including the information below:

| Retained item    | Content                   |
| ---------------- | ------------------------- |
| Project name     | {project name}            |
| Release date     | YYYY-MM-DD                |
| Chosen license   | {license name}            |
| Approved by      | {name and title}          |
| IP review result | Checked / nothing of note |
| Repository URL   | {public repository URL}   |

Retention location: {internal wiki / shared drive}
Retention period: **at least 3 years from the release date**
