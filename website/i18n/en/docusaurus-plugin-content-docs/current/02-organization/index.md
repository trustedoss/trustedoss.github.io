---
id: index
title: organizational structure
sidebar_label: organizational structure
sidebar_position: 1
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: [G1.3, G2.1, G2.2]'
  - 'ISO/IEC 18974: [G1.3, G2.1, G2.2]'
self_study_time: 1 hour
---

# organizational structure:Designating open source personnel and defining roles

## 1. What we do in this chapter

This chapter designates open source management personnel and,Document roles and responsibilities.
When you run `organization-designer` agent, the three outputs below are automatically generated.

- `output/organization/role-definition.md` — Role definition for each person in charge
- `output/organization/raci-matrix.md` — Activity-specific responsibility matrix
- `output/organization/appointment-template.md` — Contact person appointment template

> This step is ISO/IEC 5230 G1.3(3.1.2), G2.1 (3.2.2), G2.2 (3.2.1)and ISO/IEC 18974 equivalent requirements.

---

## 2. Why designating a person in charge comes first

Open source management is an activity that requires decision making. “Can I use this library?”,“How do we respond to this vulnerability?” — Somebody has to answer these questions. If there is no responsibility, there is no policy,The process doesn't actually work either.

That's why the standard requires designation of a contact person in the first place. Without organization, all subsequent activities fall into disarray.

In actual open source dispute cases, the consequences of the absence of a person in charge are specific.

- **In case of violation of GPL license**:Since there is no one to respond to, you are left with the risk of litigation. Who will release the source code?,Golden time is lost because it has not been decided who will take legal action.
- **Upon announcement of a CVE vulnerability**:Responses are delayed by weeks due to the inability to identify components affected by their products. If there is no SBOM and no person in charge, the issue will be recognized late.
- **Delivery destination SBOM upon request**:There is an increasing number of cases where SBOM submission clauses are included in contracts. Without a person in charge and a process, submission itself is impossible, resulting in contract disruption.

---

## 3. Roles required by the standard

ISO/IEC 5230 and ISO/IEC 18974 have two things in common:

1. **Designate a person in charge**(G1.3 / 3.1.2):The person or group responsible for managing the open source program must be clearly identified.
2. **External inquiry receiving channel**(G2.2 / 3.2.1):There must be a formal channel to receive requests for fulfillment of license obligations and reports of vulnerabilities.

OSPM in common to meet both standards(Open Source Program Manager),legal affairs,security officer,A Development Representative role is required.

> Detailed responsibilities and required competencies for each role are defined in [KWG Open Source Guide — Organization].(https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/1-teams/)See .

### External inquiry receiving channel(G2.2 Requirements)

You must specify an official email or channel to receive requests for fulfillment of license obligations and vulnerability reports. This is an explicit requirement of the standard and,It is as important as designating a person in charge.

example:

- `opensource@company.com` — External inquiries regarding licensing
- `security@company.com` — Receive vulnerability reports

Integrating the two channels and operating them under a single address is also a realistic option for small organizations.

### Contribution and Project Disclosure Contact Person(G3L.6 / §3.5.1)

If you plan to contribute to an external open source project or release an internal project as open source,You need to add the roles below to your RACI matrix:

| Activities                                                        | Primary Contact               | Approver              |
| ----------------------------------------------------------------- | ----------------------------- | --------------------- |
| Executing open source contribution activities                     | development representative(R) | OSPM (A)              |
| Public review of in-house projects                                | development representative(R) | OSPM·Legal Affairs(A) |
| Comprehensive response to external license and security inquiries | OSPM(R)                       | —                     |

### Gather evidence for periodic review(ISO/IEC 18974 §4.1.2.5·§4.1.2.6)

ISO/IEC 18974 requires **periodic review** and **evidence of internal best practice conformance** of open source programs. During initial certification, partial fulfillment is permitted by establishing a review plan;,renewal certification(18 months later)Fully satisfied with actual review history.

`role-definition.md` must contain the following:

- Designate a reviewer
- review cycle(Recommended once a year)
- Review history table(Initially written as a blank row,Fill upon renewal)

---

## 4. Realistic composition plan by company size

| scale                                       | Structure plan                                                                | Minimum number of people | Recommended                       |
| ------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------ | --------------------------------- |
| Startup/Small(Less than 10 developers)      | One person can hold OSPM + Legal + Security positions                         | 1 person                 | CTO or senior developer in charge |
| small business(10~100 people)               | 1 person dedicated to OSPM,Concurrent positions in legal affairs and security | 2~3 people               | Legal affairs use external advice |
| Medium/Large Enterprise(100 or more people) | Recommend forming a dedicated team,Separation by role                         | 4 or more people         | OSPO officially established       |

**importance**:It is okay for roles to overlap in a small organization. The important thing is to be clear about who is responsible.

---

## 5. Self-study

:::info Self-study mode(About 1 hour)
It interacts with agents and creates organizational artifacts.
:::

1. Read this article — Understand the concept of roles
2. Decide on a configuration plan that suits your company’s size and situation(See section 4)
3. run agent:

   :::tip Check before execution
   Terminate the current Claude session first(`/exit` or `Ctrl+C`)After doing it,Run the command below in a new terminal.
   :::

   ```bash
   cd agents/02-organization-designer
   claude
   ```

4. When the Claude prompt opens, type **`시작`**. The agent asks the six questions in order.

   <details>
   <summary>Agent conversation example(Click to expand)</summary>

   Below is an example of a conversation flow with an actual agent. When the user enters `시작`, the process goes like this.

   **Agent guidance message:**

   > hello! This is an agent that creates organization/personnel output.
   > If you answer 6 questions, 3 deliverable files will be automatically created.

   ***

   **Question 1/5** — Please tell us your company name and department name.

   `Sample answer: (main)Tech start,Development Team`

   **Question 2/5** — How many developers are there in total?

   `Sample answer:50 people

   **Question 3/5** — Is there a dedicated staff member dedicated to open source work?(Concurrent duties / 1 person in charge / 2 to 5 people / 5 or more people)

   `Sample answer:Concurrent duties`

   **Question 4/5** — Do you have legal advice?(None / Own legal team / Utilization of external legal firm)

   `Sample answer:Utilization of an external legal firm`

   **Question 5/5** — Do you have any security team advice?(None / Own security team / Utilization of external security consulting)

   `Sample answer:None`

   **Question 6/6** — Do you plan to contribute to external open source projects or release internal projects as open source?(Contribution only / Public only / Both / None)

   `Sample answer:None`

   ***

   **Example of output upon completion of creation:**

   | file                                          | Content                                                      |
   | --------------------------------------------- | ------------------------------------------------------------ |
   | `output/organization/role-definition.md`      | Defining Roles and Responsibilities,External Inquiry Channel |
   | `output/organization/raci-matrix.md`          | RACI Matrix,Person in charge by role                         |
   | `output/organization/appointment-template.md` | Officer Appointment Letter Template                          |

   **Items that require manual entry:**
   - Contact person's actual name
   - Development team representative email
   - Open source tools and education budget status

   </details>

5. Answer 6 questions from agent:
   - Company name and department name
   - Total number of developers
   - Dedicated staff size(Concurrent duties / 1 person in charge / 2 to 5 people / 5 or more people)
   - Legal advice available(None / Own legal team / Utilization of external legal firm)
   - Security team consultation(None / Own security team / Utilization of external security consulting)
   - Whether there is a plan to contribute/disclose
6. Confirm creation of `output/organization/`

:::tip expected result
Upon completing the exercise, the three files below will be created.

**Created file:**

- `output/organization/role-definition.md`
- `output/organization/raci-matrix.md`
- `output/organization/appointment-template.md`

**Items that must be included in the file:**

- Open source contact name and contact information
- Responsibilities by role(R/A/C/I)definition
- External license inquiry and vulnerability reporting channel(email)

In the generated files, make sure placeholders such as `{assignee name}` and `{email address}` are filled with actual values.
:::

:::info Standard requirements met
Completing this lab will meet the requirements below:

**ISO/IEC 5230**

| Item ID | Requirements                       | Self-certification checklist                                                         |
| ------- | ---------------------------------- | ------------------------------------------------------------------------------------ |
| 3.1.2   | Defining Contact Persons and Roles | Do you have documented roles and responsibilities for your open source program?      |
| 3.2.1   | External inquiry reception channel | Do you have a publicly visible contact method for open source compliance inquiries?  |
| 3.2.2   | Role/Responsibility Matrix         | Do you have a process for reviewing and remediating open source license obligations? |

**ISO/IEC 18974**

| Item ID | Requirements                             | Self-certification checklist                                                                            |
| ------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| 4.1.2   | Define security personnel and roles      | Do you have documented roles and responsibilities for your open source security assurance program?      |
| 4.2.1   | External vulnerability reporting channel | Do you have a publicly visible contact method for open source vulnerability reporting?                  |
| 4.2.2   | Security Role/Responsibility Matrix      | Do you have a process for assigning responsibilities for handling open source security vulnerabilities? |

:::

---

## 6. Example of generated output

### role-definition.md sample

```markdown
## 오픈소스 프로그램 관리자 (OSPM)

**담당자**: 홍길동 (개발팀 시니어 엔지니어)
**연락처**: opensource@example.com

### 주요 책임

- 오픈소스 사용 승인 및 검토
- 정책 문서 유지 관리
- 외부 문의 수신 및 대응
```

### raci-matrix.md sample

| Activities                      | OSPM | Legal | Security | development |
| ------------------------------- | ---- | ----- | -------- | ----------- |
| Approved for use of open source | R, A | C     | C        | I           |
| License Review                  | A    | R     | I        | C           |
| Response to CVE vulnerabilities | A    | I     | R        | C           |
| create SBOM                     | A    | I     | C        | R           |

_(R=Run,A=Final responsibility,C=negotiation,I=Information sharing)_

---

## 7. Completion Confirmation Checklist

- [ ] `output/organization/role-definition.md` created
- [ ] `output/organization/raci-matrix.md` created
- [ ] `output/organization/appointment-template.md` created
- [ ] Open source contact name and contact information defined
- [ ] External inquiry email/channel specified

> 📋 **Example of output**: [Organizational Output Best Practices](/reference/samples/organization)You can check the actual format of the generated file at .

---

## 8. Next steps

Once you've completed organizing your organization, move on to establishing open source policies.

:::tip Check before execution
Terminate the current Claude session first(`/exit` or `Ctrl+C`)After doing it,Run the command below in a new terminal.
:::

```bash
cd agents/03-policy-generator
claude
```

or [Establishment of open source policy:The first step to legal protection](../03-policy/index.md)You can go to and read the policy chapter first before proceeding.
