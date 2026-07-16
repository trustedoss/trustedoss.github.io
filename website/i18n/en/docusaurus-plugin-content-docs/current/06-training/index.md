---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: G1.4 (3.1.2), G1.7 (3.1.3), G2.3 (3.1.3)'
  - 'ISO/IEC 18974: G1.4 (4.1.2), G1.7 (4.1.3), G2.3 (4.1.3)'
self_study_time: 1 hour
---

# Training Program: Raise open source awareness across your organization

<Prerequisite items={[{label: '3. Open Source Policy', href: '/docs/policy'}]} />

## 1. What we do in this chapter

We establish a training curriculum for each job group, build a completion tracking system, and gather training resources you can use for free. Completing this chapter gives all relevant members of your organization a foundation for understanding and applying your open source policies and processes.

Both standards require proof that program managers and relevant members have completed training. No matter how good your policy documents and process procedures are, real compliance cannot be achieved if members do not know their contents.

## 2. Background knowledge: Why training is a standard requirement

### Why policies and processes alone are not enough

Even when policies and processes exist, they will not work if people do not know about them. ISO/IEC 5230 and 18974 do not simply check whether a document exists. They also check whether members actually know the document, understand it, and are able to follow it. Training completion records are one of the key pieces of evidence for self-certification.

### Training requirements of ISO/IEC 5230 and 18974

**ISO/IEC 5230 (License Compliance)**

- **3.1.2 (G1.4)**: Ensure that program participants have the competence needed for their roles, with documented evidence such as completed training.
- **3.1.3 (G2.3)**: Ensure that program participants understand the policy goals, their contributions, and their relevant roles.

**ISO/IEC 18974 (Security Assurance)**

- **4.1.2 (G1.4)**: Ensure that program participants have the competence needed for their security assurance roles, with documented evidence.
- **4.1.3 (G2.3)**: Ensure that program participants understand the goals of the security assurance policy and their roles.

> This step meets the requirements of ISO/IEC 5230 G1.4 (3.1.2), G1.7 (3.1.3), G2.3 (3.1.3) and ISO/IEC 18974 G1.4 (4.1.2), G1.7 (4.1.3), G2.3 (4.1.3).

**Training completion records serve as evidence for self-certification.** During a certification review, you must have records showing "who received what training, and when." The completion tracking sheet you create in this chapter is that evidence document.

## 3. Required training content by job group

:::tip
Unfamiliar acronyms such as SBOM and CVSS are explained in plain language in the [Glossary](/reference/glossary).
:::

| Job group           | Required training content                                                                           | Recommended time |
| ------------------- | --------------------------------------------------------------------------------------------------- | ---------------- |
| Developer           | Open source license basics, usage approval process, SBOM concepts, vulnerability response procedure | 4 hours          |
| Manager/Team Leader | Open source policy overview, understanding legal risks, role in the approval process                | 2 hours          |
| Legal/Purchasing    | Detailed license obligations, open source clauses in contracts                                      | 3 hours          |
| Security Manager    | Vulnerability identification and response, interpreting CVSS scores, 18974 requirements             | 3 hours          |

:::tip
For real corporate training examples (SKT, Kakao, NCSOFT, etc.) and training materials, see [KWG Open Source Guide — Training](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/5-training/).
:::

## 4. List of free training resources

| Resource                              | Provided by         | Level                 | Language | Link                                                                                                                             |
| ------------------------------------- | ------------------- | --------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------- |
| OpenChain Training Materials          | OpenChain Project   | Beginner–Intermediate | English  | https://www.openchainproject.org/resources                                                                                       |
| Open Source Licensing Basics (LFC193) | Linux Foundation    | Beginner              | English  | [LFC193 course](https://training.linuxfoundation.org/training/introduction-to-open-source-license-compliance-management-lfc193/) |
| NIPA Open Source License Guide        | NIPA                | Beginner–Intermediate | Korean   | [NIPA Open SW Portal](https://www.oss.kr)                                                                                        |
| OpenChain KWG Training Materials      | OpenChain KWG       | Intermediate          | Korean   | https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/5-training/                                    |
| SPDX Official Documentation           | SPDX Community      | Intermediate          | English  | [SPDX official site](https://spdx.dev)                                                                                           |
| CycloneDX Official Documentation      | CycloneDX Community | Intermediate          | English  | [CycloneDX official site](https://cyclonedx.org)                                                                                 |

## 5. How to manage training completion records

Training completion records can be managed easily with a spreadsheet or markdown file, without any additional tools. What matters is not the format but the record itself.

:::info[About completion-tracker.md]
completion-tracker.md is a document you fill in after training takes place. When you run the agent, it is normal for an empty template to be created. After conducting the training, add completion records in the format below.
:::

This file serves as evidence for ISO/IEC 5230 §3.1.2.3 (competency assessment evidence) and 18974 §4.1.2.4.

`output/training/completion-tracker.md` format example:

| Name          | Job group | Training name               | Completion date | Confirmed by                |
| ------------- | --------- | --------------------------- | --------------- | --------------------------- |
| Hong Gil-dong | Developer | Open source license basics  | 2026-03-20      | Open source program manager |
| Kim Cheol-su  | Manager   | Open source policy overview | 2026-03-21      | Open source program manager |

**Using completion-tracker.md for self-certification:**

- On first certification, if training has not yet been completed, mark the item as partially satisfied ("curriculum complete, training pending").
- After training is complete, fill in the records and convert it to fully satisfied.
- Requiring training completion when onboarding new employees helps maintain continuous compliance.

## 6. Self-study

:::info Self-study mode (about 1 hour)
Take your time and work through each step until you understand it.
:::

1. Read this document from beginning to end.
2. Run the training-manager agent with the command below:

   :::tip Check before execution
   Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
   :::

   ```bash
   cd agents/06-training-manager && claude
   ```

3. When the Claude prompt opens, type **`시작`** (start).

   <details>
   <summary>Agent conversation example (click to expand)</summary>

   Below is an example of how a conversation with the actual agent flows when you run it.

   **Agent guidance message:**

   ```text
   Hello! This is the agent that creates training program deliverables.
   Answer 3 questions and 3 training documents will be created automatically.
   ```

   ***

   **Question 1/3** — How many people are in each job group? (N developers / N managers / N operations)

   `Sample answer: 40 developers, 5 managers, 5 in operations`

   **Question 2/3** — What is your preferred training format? (Online self-paced / In-person classroom / Blended)

   `Sample answer: Online self-paced`

   **Question 3/3** — Do you need proof of training completion? (For internal records / for audit preparation / for certification submission)

   `Sample answer: For certification submission`

   ***

   **Example output on completion:**

   | File                                    | Content                                                                 |
   | --------------------------------------- | ----------------------------------------------------------------------- |
   | `output/training/curriculum.md`         | Training curriculum and recommended time for each job group             |
   | `output/training/completion-tracker.md` | Completion tracking sheet (blank form, fill in directly after training) |
   | `output/training/resources.md`          | List of free training resources                                         |

   **Items that require manual entry:**
   - Training schedule (annual plan)
   - How to prove completion (certificate of completion / confirmation email / signature)

   </details>

4. Answer the agent's three questions (see the conversation example above).
5. After the agent generates the deliverables, check the results in the `output/training/` folder.

:::tip Expected result
When you complete this lab, the three files below will be created.

**Created files:**

- `output/training/curriculum.md`
- `output/training/completion-tracker.md`
- `output/training/resources.md`

**Items that must be included in the files:**

- Training items and recommended times for each job group
- How to prove completion (certificate of completion / signature / email confirmation)
- Regular training schedule (at least once a year)

`completion-tracker.md` is created as an empty form. You must fill it in yourself after completing the actual training.
:::

:::info Standard requirements met
Completing this lab meets the requirements below.

**ISO/IEC 5230**

| Item ID | Requirement          | Self-certification checklist                                                                         |
| ------- | -------------------- | ---------------------------------------------------------------------------------------------------- |
| 3.1.2   | Proof of competency  | Do you have documented evidence that each program participant has completed the necessary training?  |
| 3.1.3   | Awareness assessment | Do you have documented evidence that your program participants are aware of your open source policy? |

**ISO/IEC 18974**

| Item ID | Requirement                   | Self-certification checklist                                                                                            |
| ------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 4.1.2   | Proof of security competency  | Do you have documented evidence that each program participant has the necessary competence for security assurance?      |
| 4.1.3   | Security awareness assessment | Do you have documented evidence that your program participants are aware of your open source security assurance policy? |

:::

## 7. Generated deliverables

When you complete this chapter, the following files will be created in the `output/training/` folder:

- **curriculum.md**: Training curriculum by job group (training items, recommended time, priority)
- **completion-tracker.md**: Training completion tracking sheet (self-certification evidence document)
- **resources.md**: List of free training resources (select according to your organization's situation)

## 8. Completion checklist

- [ ] `output/training/curriculum.md` created
- [ ] `output/training/completion-tracker.md` created
- [ ] `output/training/resources.md` created
- [ ] Training items are defined for each job group
- [ ] Method of proving completion has been decided

:::tip Example deliverables
You can see the actual format of the generated files in [Training Deliverables Best Practice](/reference/samples/training).
:::

## 9. Next steps

Once you have built your training program, it is time to prepare your self-certification declaration.

Move on to the final chapter, or run the agent right away.

To read the chapter document first, go to [Self-Certification Declaration: The Final Step](../07-conformance/index.md).

:::tip Check before execution
Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/07-conformance-preparer && claude
```
