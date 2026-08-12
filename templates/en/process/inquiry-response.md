# External Inquiry Response Procedure

<!-- 5230 §3.2.1.2 (G2.2) -->

**Company name**: {company name}
**Date written**: YYYY-MM-DD
**Owner**: {Open Source Program Manager}

This process document is based on the OpenChain KWG process guide (the external inquiry response process) and on ISO/IEC 5230 and 18974. The KWG guide is licensed under CC BY 4.0.

---

## 1. External inquiry channels

<!-- 5230 §3.2.1.1, §3.2.1.2 -->

| Inquiry type                   | Channel                     | Owner            |
| ------------------------------ | --------------------------- | ---------------- |
| License compliance inquiries   | opensource@{company domain} | OSPM             |
| Security vulnerability reports | security@{company domain}   | Security Manager |
| Copyright infringement claims  | legal@{company domain}      | Legal team       |
| Other open source inquiries    | opensource@{company domain} | OSPM             |

The channels have to be publicly reachable (stated on the website, in product notices, and similar).

---

## 2. Inquiry classification

<!-- 5230 §3.2.1.2 - inquiry handling procedure -->

Classify received inquiries into the types below and handle them accordingly:

| Code  | Type                          | Examples                                                                  |
| ----- | ----------------------------- | ------------------------------------------------------------------------- |
| INQ-L | License inquiry               | Request for GPL source code, notice that a copyright statement is missing |
| INQ-S | Security vulnerability report | A report of a CVE-related security vulnerability                          |
| INQ-C | Copyright infringement claim  | Claim of unauthorised use, DMCA notice                                    |
| INQ-G | General inquiry               | Request for an SBOM, request to confirm a license                         |

---

## 3. Response SLA per inquiry type

<!-- 5230 §3.2.1.2 -->

| Classification       | Acknowledgement        | Investigation complete  | Final handling                             |
| -------------------- | ---------------------- | ----------------------- | ------------------------------------------ |
| INQ-L (license)      | Within 2 business days | Within 10 business days | Within 30 business days                    |
| INQ-S (security)     | Within 1 business day  | Within 5 business days  | Per the `vulnerability response procedure` |
| INQ-C (infringement) | Within 1 business day  | Within 5 business days  | Decided after consulting the legal team    |
| INQ-G (general)      | Within 3 business days | Within 15 business days | Within 30 business days                    |

---

## 4. Response procedure (8 steps)

<!-- 5230 §3.2.1.2 - external inquiry handling flow -->

1. **Receipt notice**: Send an automatic reply or an acknowledgement email as soon as the inquiry arrives. Register it in the internal issue tracker ({Jira, GitHub Issues, and so on})
2. **Investigation notice**: Send a reply stating that the investigation has started within the SLA
3. **Internal investigation**: Check the SBOM and distribution history, and review the relevant license and copyright information
4. **Report to the requester**: Communicate the investigation result and the response plan
5. **Remediation**: Carry out corrective action immediately if a license obligation was not fulfilled
6. **Resolution notice**: Notify the requester once the correction is complete or the inquiry is satisfied
7. **Process improvement**: Review preventive measures through the OSRB (Open Source Review Board) or an OSPM review
8. **Record retention**: Retain for at least 3 years from closure (per [5. Inquiry history retention])

---

## 5. Escalation criteria

<!-- 5230 §3.2.1.2 -->

Escalate immediately to the legal team and management when:

- The inquiry contains the threat of a copyright infringement lawsuit
- The same inquiry recurs, or arrives from multiple external organizations
- Handling within the SLA is impossible
- The inquiry arrives through the press or a public channel

Escalation path: OSPM → legal team → {C-level owner}

---

## 6. Inquiry history retention

<!-- 5230 §3.2.1.2 - inquiry handling records -->

Retain records of every external inquiry and the response for **at least 3 years**, including the information below:

| Retained item          | Content                                |
| ---------------------- | -------------------------------------- |
| Receipt date           | YYYY-MM-DD                             |
| Inquiry type           | INQ-L / INQ-S / INQ-C / INQ-G          |
| Summary of the inquiry | The core request                       |
| Investigation result   | What was established as fact           |
| Action taken           | The correction made or the reply given |
| Closure date           | YYYY-MM-DD                             |
| Owner                  | {name}                                 |

Retention location: {internal wiki / shared drive / issue tracker}
Retention period: **at least 3 years from closure**
