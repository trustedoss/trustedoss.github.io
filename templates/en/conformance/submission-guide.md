# OpenChain Self-Certification Registration Guide

<!-- 5230 §3.6.2.1, 18974 §4.4.2.1 (18-month maintenance) -->

**Company name**: {company name}
**Date written**: YYYY-MM-DD
**Owner**: {Open Source Program Manager name}

---

## 1. Self-certification registration procedure

### Step 1 — Pre-checks

Confirm the following before registering:

- [ ] `output/conformance/gap-analysis.md` is complete, with nothing unsatisfied or with a plan to close it
- [ ] `output/conformance/declaration-draft.md` has had its final review
- [ ] The scope of the declaration (the software or products it covers) is clearly defined
- [ ] The approver (management or the responsible executive) has agreed in advance

### Step 2 — Download the self-certification checklist

https://github.com/OpenChain-Project/Reference-Material/tree/master/OpenChain-Standards-Self-Certification

Files per language sit under `Checklist/ISO-IEC-5230` and `Checklist/ISO-IEC-18974`.

### Step 3 — Choose the standard and self-assess

| Standard to certify against        | Choice |
| ---------------------------------- | ------ |
| ISO/IEC 5230 (license compliance)  | ☐      |
| ISO/IEC 18974 (security assurance) | ☐      |
| Both standards                     | ☐      |

Use `output/conformance/declaration-draft.md` as the reference when answering Yes or No to each checklist item.

### Step 4 — Apply for listing

Fill in and submit the online form at https://openchainproject.org/get-started.
You do not upload the checklist itself; you submit company information on the basis that the self-assessment is done.

### Step 5 — Confirm the certification

Once registration is complete:

- The company appears on the official OpenChain conformant list
- The OpenChain logo can be used (check the usage conditions)

---

## 2. Managing the certification validity period

<!-- 5230 §3.6.2.1, 18974 §4.4.2.1 -->

| Item                    | Content                                         |
| ----------------------- | ----------------------------------------------- |
| **Validity period**     | 18 months from the declaration date             |
| **Declaration date**    | YYYY-MM-DD                                      |
| **Expiry date**         | YYYY-MM-DD                                      |
| **Re-declaration date** | YYYY-MM-DD (one month before expiry is advised) |
| **Reminder owner**      | {Open Source Program Manager name}              |

### Setting the reminder

Set a notice one month before expiry, using one of these:

- Add an "OpenChain re-declaration preparation" entry to the owner's calendar
- Set up a recurring reminder bot in the team channel (Slack, Teams, and so on)

---

## 3. Preparing to re-declare (after 18 months)

When the re-declaration date approaches, prepare in this order:

1. Re-run `agents/en/07-conformance-preparer` to update the gap analysis
2. Check whether changed policies and processes are reflected
3. Review the vulnerability response history and training history of the past 18 months
4. Update `output/conformance/declaration-draft.md` (dates, any change of scope)
5. Register the re-declaration on the OpenChain website

---

## 4. Certification history

| Round       | Declaration date | Expiry date | Standards applied     | Owner  |
| ----------- | ---------------- | ----------- | --------------------- | ------ |
| 1 (initial) | YYYY-MM-DD       | YYYY-MM-DD  | {5230 / 18974 / both} | {name} |
