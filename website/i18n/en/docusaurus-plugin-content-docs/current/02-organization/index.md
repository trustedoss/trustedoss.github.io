---
id: index
title: Organizational Structure
sidebar_label: Organizational Structure
sidebar_position: 1
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: G1.3 (3.1.2), G2.1 (3.2.2), G2.2 (3.2.1)'
  - 'ISO/IEC 18974: G1.3 (4.1.2), G2.1 (4.2.2), G2.2 (4.2.1)'
self_study_time: 1 hour
---

# Organizational structure: Designating open source personnel and defining roles

<Prerequisite items={[{label: '0. Overview', href: '/docs/'}]}>This chapter is the first deliverable step.</Prerequisite>

## 1. What we do in this chapter

This chapter designates the people responsible for open source management and documents their roles and responsibilities.
When you run the `organization-designer` agent, the three deliverables below are generated automatically.

- `output/organization/role-definition.md` — Role definition for each program manager
- `output/organization/raci-matrix.md` — Responsibility matrix by activity
- `output/organization/appointment-template.md` — Appointment letter template for the program manager

> This step meets the ISO/IEC 5230 G1.3 (3.1.2), G2.1 (3.2.2), and G2.2 (3.2.1) requirements, and the equivalent ISO/IEC 18974 items.

---

## 2. Why designating a program manager comes first

Open source management is an activity that requires decision-making. "Can we use this library?" "How do we respond to this vulnerability?" — someone has to answer these questions. Without clear responsibility, neither the policy nor the process actually works.

That is also why the standards require designating a program manager first. Without an organization in place, every activity that follows falls apart.

In real-world open source disputes, the consequences of having no one in charge are concrete.

- **GPL license violation**: With no one to respond, you carry the litigation risk as is. Because no one has decided who will release the source code or who will handle the legal response, the critical window for action is lost.
- **CVE vulnerability disclosure**: Response is delayed by weeks because you cannot identify which components in your products are affected. Without an SBOM and a program manager, you become aware of the issue late.
- **SBOM requested by a customer**: A growing number of contracts include clauses requiring SBOM submission. Without a program manager and a process, submission itself is impossible, and the contract stalls.

---

## 3. Roles required by the standards

ISO/IEC 5230 and ISO/IEC 18974 both require the following two things.

1. **Designate a program manager** (G1.3 / 3.1.2): The person or group responsible for managing the open source program must be clearly identified.
2. **Channel for receiving external inquiries** (G2.2 / 3.2.1): There must be an official channel to receive license obligation requests and vulnerability reports.

To meet both standards, you commonly need an OSPM (Open Source Program Manager), a legal role, a security role, and a development representative.

:::tip
Detailed responsibilities and required competencies for each role are defined in the [KWG Open Source Guide — Organization](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/1-teams/). This chapter's structure and requirement descriptions are reworked from that KWG guide (CC BY 4.0).
:::

### Channel for receiving external inquiries (G2.2 requirement)

You must designate an official email address or channel to receive license obligation requests and vulnerability reports. This is an explicit requirement of the standards, and it is as important as designating a program manager.

Examples:

- `opensource@company.com` — External inquiries regarding licensing
- `security@company.com` — Receiving vulnerability reports

Combining the two channels and operating them under a single address is also a realistic option for small organizations.

### Contribution and project disclosure contact (G3L.6 / §3.5.1)

If you plan to contribute to an external open source project or release an internal project as open source, you need to add the roles below to your RACI matrix.

| Activity                                                    | Primary owner                  | Approver           |
| ----------------------------------------------------------- | ------------------------------ | ------------------ |
| Carrying out open source contribution activities            | Development representative (R) | OSPM (A)           |
| Disclosure review of internal projects                      | Development representative (R) | OSPM and Legal (A) |
| Overall response to external license and security inquiries | OSPM (R)                       | —                  |

### Gather evidence for periodic review (ISO/IEC 18974 §4.1.2.5, §4.1.2.6)

ISO/IEC 18974 requires evidence of **periodic review** of the open source program and **verification of conformance with internal best practices**. For initial certification, partial fulfillment through establishing a review plan is permitted; at renewal certification (18 months later), it must be fully satisfied with an actual review history.

`role-definition.md` must contain the following:

- The designated reviewer
- The review cycle (annually is recommended)
- A review history table (initially written with blank rows, filled in at renewal)

---

## 4. Realistic structures by company size

| Scale                              | Structure                                                          | Minimum headcount | Recommendation                  |
| ---------------------------------- | ------------------------------------------------------------------ | ----------------- | ------------------------------- |
| Startup / small (10 devs or fewer) | One person can hold the OSPM, Legal, and Security roles            | 1 person          | CTO or a senior developer leads |
| Small business (10–100 people)     | One person dedicated to OSPM; Legal and Security held concurrently | 2–3 people        | Use external counsel for legal  |
| Mid-size / large enterprise (100+) | Form a dedicated team; separate the roles                          | 4 or more people  | Establish a formal OSPO         |

**Important**: It is fine for roles to overlap in a small organization. What matters is being clear about who is responsible.

### Assign people by name — the per-team champion model

The standards' evidence requires the responsible person's **name**, so a department name or
"everyone" in the role table does not satisfy the requirement. For roles that involve entire
business units, we recommend designating a **per-team champion** — one person in each development
team who acts as the open source contact — and recording their name.

Also, designating an **internal best-practice verification owner** who periodically checks that
the role list and processes match actual best practice naturally accumulates the review evidence
required at renewal certification. In small organizations the open source program manager can hold
this role concurrently.

---

## 5. Self-study

:::info Self-study mode (about 1 hour)
You interact with the agent and create the organizational deliverables.
:::

1. Read this chapter to understand the concept of the roles.
2. Decide on a structure that suits your company's size and situation (see section 4).
3. Run the agent:

   :::tip Check before running
   First terminate the current Claude session (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
   :::

   ```bash
   cd agents/02-organization-designer
   claude
   ```

4. When the Claude prompt opens, type **`시작`** ("start"). The agent walks through the six questions in order.

   <details>
   <summary>Agent conversation example (click to expand)</summary>

   Below is an example of a conversation flow with the actual agent. When the user enters `시작`, it proceeds like this.

   **Agent guidance message:**

   ```text
   Hello! This is the agent that creates the organization and personnel deliverables.
   Answer 6 questions and 3 deliverable files will be created automatically.
   ```

   ***

   **Question 1/6** — Tell us your company name and department name.

   `Sample answer: TechStart Inc., Development Team`

   **Question 2/6** — How many developers do you have in total?

   `Sample answer: 50 people`

   **Question 3/6** — Do you have anyone who can be dedicated to open source work? (Concurrent role / 1 dedicated person / 2–5 people / 5 or more people)

   `Sample answer: Concurrent role`

   **Question 4/6** — Do you have legal counsel? (None / In-house legal team / Currently using an external law firm / Planning to use an external law firm)

   `Sample answer: Currently using an external law firm`

   **Question 5/6** — Do you have security team support? (None / In-house security team / External security consulting)

   `Sample answer: None`

   **Question 6/6** — Do you plan to contribute to external open source projects or release internal projects as open source? (Contribution only / Disclosure only / Both / Neither)

   `Sample answer: Neither`

   ***

   **Example output on completion:**

   | File                                          | Content                                              |
   | --------------------------------------------- | ---------------------------------------------------- |
   | `output/organization/role-definition.md`      | Roles and responsibilities, external inquiry channel |
   | `output/organization/raci-matrix.md`          | RACI matrix, person assigned to each role            |
   | `output/organization/appointment-template.md` | Appointment letter template for the program manager  |

   **Items you must fill in manually:**
   - The program manager's actual name
   - The development team's representative email
   - The status of open source tooling and the training budget

   </details>

5. Answer the six questions from the conversation example above according to your company's situation.
6. Confirm that `output/organization/` was created.

:::tip Expected result
When the exercise is complete, the three files below will be created.

**Created files:**

- `output/organization/role-definition.md`
- `output/organization/raci-matrix.md`
- `output/organization/appointment-template.md`

**Items the files must include:**

- Open source program manager's name and contact details
- Responsibility definitions by role (R/A/C/I)
- Channel (email) for external license inquiries and vulnerability reports

In the generated files, make sure placeholders such as `{assignee name}` and `{email address}` are filled in with actual values.
:::

:::info Standard requirements met
Completing this exercise meets the requirements below.

**ISO/IEC 5230**

| Item ID | Requirement                         | Self-certification checklist                                                                      |
| ------- | ----------------------------------- | ------------------------------------------------------------------------------------------------- |
| 3.1.2   | Defining program managers and roles | Do you have documented roles and responsibilities for your open source program?                   |
| 3.2.1   | External inquiry receiving channel  | Do you have a publicly visible contact method for open source compliance inquiries?               |
| 3.2.2   | Role/responsibility matrix          | Do you have a documented list of roles and responsibilities with personnel assigned to each role? |

**ISO/IEC 18974**

| Item ID | Requirement                              | Self-certification checklist                                                                            |
| ------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| 4.1.2   | Define security personnel and roles      | Do you have documented roles and responsibilities for your open source security assurance program?      |
| 4.2.1   | External vulnerability reporting channel | Do you have a publicly visible contact method for open source vulnerability reporting?                  |
| 4.2.2   | Security role/responsibility matrix      | Do you have a process for assigning responsibilities for handling open source security vulnerabilities? |

:::

---

## 6. Examples of generated deliverables

### role-definition.md sample

```markdown
## Open Source Program Manager (OSPM)

**Program Manager**: Hong Gil-dong (Senior Engineer, Development Team)
**Contact**: opensource@example.com

### Key Responsibilities

- Approve and review open source usage
- Maintain policy documents
- Receive and respond to external inquiries
```

### raci-matrix.md sample

| Activity                       | OSPM | Legal | Security | Development |
| ------------------------------ | ---- | ----- | -------- | ----------- |
| Approve open source usage      | R, A | C     | C        | I           |
| License review                 | A    | R     | I        | C           |
| Respond to CVE vulnerabilities | A    | I     | R        | C           |
| Create SBOM                    | A    | I     | C        | R           |

_(R = Responsible, A = Accountable, C = Consulted, I = Informed)_

---

## 7. Completion checklist

- [ ] `output/organization/role-definition.md` created
- [ ] `output/organization/raci-matrix.md` created
- [ ] `output/organization/appointment-template.md` created
- [ ] Open source program manager's name and contact details defined
- [ ] External inquiry email/channel designated

:::tip Example deliverables
See the actual format of the generated files in [Organization deliverables best practice](/reference/samples/organization).
:::

---

## 8. Next steps

Once the organizational structure is complete, move on to establishing your open source policy.

:::tip Check before running
First terminate the current Claude session (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/03-policy-generator
claude
```

Or go to [Establishing an open source policy: The first step to legal protection](../03-policy/index.md) to read the policy chapter first before proceeding.
