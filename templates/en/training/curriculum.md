# Open Source Training Curriculum

<!-- 5230 §3.1.1.2 (policy dissemination procedure), §3.1.2.2 (competencies per role), 18974 §4.1.1.2 -->

**Company name**: {company name}
**Version**: 1.0
**Date written**: YYYY-MM-DD
**Owner**: {Open Source Program Manager name}

---

## 1. Training overview

This curriculum defines the training that gives everyone taking part in the open source policy and security assurance program the competencies they need. Because the knowledge and hands-on work each role needs differs, separate courses run per role.

---

## 2. Courses per role

<!-- 06-training-manager always generates the three base roles (developers, managers, all members).
     The optional roles (legal/purchasing, security) are included only for organizations that have them. -->

### Developer course (required, 4 hours)

| No. | Content                                                 | Duration | Format         |
| --- | ------------------------------------------------------- | -------- | -------------- |
| 1   | Open source license fundamentals (MIT vs Apache vs GPL) | 1 hour   | Online lecture |
| 2   | Hands-on with the open source usage approval process    | 1 hour   | Hands-on       |
| 3   | Hands-on with SBOM generation tools (syft, cdxgen)      | 1 hour   | Hands-on       |
| 4   | Vulnerability scanning and response                     | 1 hour   | Hands-on       |

### Manager and team lead course (required, 2 hours)

| No. | Content                                                  | Duration | Format          |
| --- | -------------------------------------------------------- | -------- | --------------- |
| 1   | Open source policy overview and understanding legal risk | 1 hour   | Online lecture  |
| 2   | The manager's role in the approval procedure             | 1 hour   | Lecture and Q&A |

### Legal and purchasing course (optional, for organizations with these roles, 3 hours)

| No. | Content                                                | Duration  | Format        |
| --- | ------------------------------------------------------ | --------- | ------------- |
| 1   | License obligations in detail (copyleft and similar)   | 1.5 hours | Lecture       |
| 2   | How to review open source clauses in contracts         | 1 hour    | Case study    |
| 3   | Non-compliance cases and how they were handled legally | 0.5 hours | Case briefing |

### Security course (optional, for organizations with this role, 3 hours)

| No. | Content                                           | Duration | Format   |
| --- | ------------------------------------------------- | -------- | -------- |
| 1   | Identifying vulnerabilities (CVE and CVSS basics) | 1 hour   | Lecture  |
| 2   | Hands-on with vulnerability scanning tools        | 1 hour   | Hands-on |
| 3   | Overview of ISO/IEC 18974 requirements            | 1 hour   | Lecture  |

### Awareness course for all members (required, 30 minutes)

| No. | Content                                                 | Duration | Format                        |
| --- | ------------------------------------------------------- | -------- | ----------------------------- |
| 1   | That an open source policy exists, and what it is for   | 15 min   | Video or distributed material |
| 2   | The impact of non-compliance and the reporting channels | 15 min   | Video or distributed material |

---

## 3. Onboarding training (new hires)

- **Audience**: everyone, within 30 days of joining
- **Content**: the awareness course for all members, plus the required course for their role
- **Owner**: {Open Source Program Manager}

---

## 4. Regular training schedule

| Training                         | Cycle       | Audience                | Next scheduled               |
| -------------------------------- | ----------- | ----------------------- | ---------------------------- |
| Awareness course for all members | Once a year | All employees           | YYYY-MM                      |
| Developer course                 | Once a year | Developers              | YYYY-MM                      |
| Manager course                   | Once a year | Managers and team leads | YYYY-MM                      |
| Briefing when the policy changes | As needed   | Affected roles          | Within 1 month of the change |

---

## 5. Free external training resources

| Resource                                             | Provider          | Level                    | Duration   |
| ---------------------------------------------------- | ----------------- | ------------------------ | ---------- |
| OpenChain training material                          | OpenChain Project | Beginner to intermediate | Self-paced |
| LFC193 Open Source License Compliance                | Linux Foundation  | Beginner                 | 3 hours    |
| LFD102 A Beginner's Guide to Open Source Development | Linux Foundation  | Beginner                 | Self-paced |
| OpenChain KWG training material                      | OpenChain KWG     | Intermediate             | Self-paced |
| Official SPDX documentation                          | SPDX Community    | Intermediate             | Self-paced |

---

## 6. Evidence of training completion

| Method                 | When it applies                            |
| ---------------------- | ------------------------------------------ |
| Attach the certificate | External courses (LFC193 and similar)      |
| Signature of the owner | Internal classroom training                |
| Email confirmation     | Training delivered as distributed material |
| Test result            | When comprehension has to be confirmed     |

Record completion in `output/training/completion-tracker.md`.

---

## 7. Training record retention

<!-- 5230 §3.1.2.3, 18974 §4.1.2.4 -->

Retain all training completion records as follows:

| Retained item                                      | Retention period                                | Location                             |
| -------------------------------------------------- | ----------------------------------------------- | ------------------------------------ |
| Training completion record (completion-tracker.md) | At least 3 years from completion                | {internal repository / shared drive} |
| Certificates or other completion evidence          | At least 3 years from completion                | {internal repository / shared drive} |
| Training material (slides, videos)                 | At least 3 years from the last time it was used | {internal repository}                |

The three-year retention meets the evidence requirements of ISO/IEC 5230 §3.1.2.3 (evidence of competency assessment) and ISO/IEC 18974 §4.1.2.4.
