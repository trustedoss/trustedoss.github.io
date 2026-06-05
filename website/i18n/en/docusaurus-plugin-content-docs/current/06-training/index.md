---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: G1.4 (3.1.2), G2.3 (3.1.3)'
  - 'ISO/IEC 18974: G1.4 (4.1.2), G2.3 (4.1.3)'
self_study_time: 1 hour
---

# Training Program: Raise open source awareness across your organization

## 1. What we do in this chapter

We establish a training curriculum for each job group, build a completion tracking system, and gather training resources you can use for free. Completing this chapter gives all relevant members of your organization a foundation for understanding and applying your open source policies and processes.

Both standards require proof that personnel and relevant members have completed training. No matter how good your policy documents and process procedures are, real compliance cannot be achieved if members do not know their contents.

## 2. Background knowledge: Why training is a standard requirement

### Why policies and processes alone are not enough

Even when policies and processes exist, they will not work if people do not know about them. ISO/IEC 5230 and 18974 do not simply check whether a document exists. They check whether members actually know the document, understand it, and are able to follow it. Training completion records are one of the key pieces of evidence for self-certification.

### Training requirements of ISO/IEC 5230 and 18974

**ISO/IEC 5230 (License Compliance)**

- **3.1.2 (G1.4)**: Ensure that program participants are aware of the existence of the open source license compliance policy.
- **3.1.3 (G2.3)**: Ensure that program participants understand the policy goals, their contributions, and their relevant roles.

**ISO/IEC 18974 (Security Assurance)**

- **3.1.2 (G1.4)**: Ensure that program participants are aware of the existence of a security assurance policy.
- **3.1.3 (G2.3)**: Ensure that program participants understand the goals of the security assurance policy and their roles.

> This step meets the requirements of ISO/IEC 5230 G1.4 (3.1.2), G2.3 (3.1.3) and ISO/IEC 18974 G1.4 (4.1.2), G2.3 (4.1.3).

**Training completion records serve as evidence for self-certification.** During a certification review, you must have records showing "who received what training, and when." The completion tracking sheet you create in this chapter is that evidence document.

## 3. Required training content by job group

| Job group           | Required training content                                                                           | Recommended time |
| ------------------- | --------------------------------------------------------------------------------------------------- | ---------------- |
| Developer           | Open source license basics, usage approval process, SBOM concepts, vulnerability response procedure | 4 hours          |
| Manager/Team Leader | Open source policy overview, understanding legal risks, role in the approval process                | 2 hours          |
| Legal/Purchasing    | Detailed license obligations, open source clauses in contracts                                      | 3 hours          |
| Security Manager    | Vulnerability identification and response, interpreting CVSS scores, 18974 requirements             | 3 hours          |

> For real corporate training examples (SKT, Kakao, NCSOFT, etc.) and training materials, see [KWG Open Source Guide — Training](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/5-training/).

## 4. List of free training resources

| Resource                              | Provided by         | Level                 | Language | Link                                                                                          |
| ------------------------------------- | ------------------- | --------------------- | -------- | --------------------------------------------------------------------------------------------- |
| OpenChain Training Materials          | OpenChain Project   | Beginner–Intermediate | English  | https://www.openchainproject.org/resources                                                    |
| Open Source Licensing Basics (LFC193) | Linux Foundation    | Beginner              | English  | LFC193 Course (Linux Foundation Training)                                                     |
| NIPA Open Source License Guide        | NIPA                | Beginner–Intermediate | Korean   | NIPA Open SW Portal                                                                           |
| OpenChain KWG Training Materials      | OpenChain KWG       | Intermediate          | Korean   | https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/5-training/ |
| SPDX Official Documentation           | SPDX Community      | Intermediate          | English  | SPDX Official Site (spdx.dev)                                                                 |
| CycloneDX Official Documentation      | CycloneDX Community | Intermediate          | English  | CycloneDX Official Site (cyclonedx.org)                                                       |

## 5. How to manage training completion records

Training completion records can be managed easily with a spreadsheet or markdown file, without any additional tools. What matters is not the format but the record itself.

> ⚠️ **completion-tracker.md is a document you fill in after training.**
> When you run the agent, it is normal for an empty template to be created.
> After completing the training, add your completion records in the format below.
> This file serves as evidence for ISO/IEC 5230 §3.1.2.3 (competency assessment evidence) and 18974 §4.1.2.4.

`output/training/completion-tracker.md` format example:

| Name          | Job group | Training name               | Completion date | Confirmed by               |
| ------------- | --------- | --------------------------- | --------------- | -------------------------- |
| Hong Gil-dong | Developer | Open source license basics  | 2026-03-20      | Open source representative |
| Kim Cheol-su  | Manager   | Open source policy overview | 2026-03-21      | Open source representative |

**Using completion-tracker.md for self-certification:**

- On first certification, if training has not yet been completed, mark the item as partially satisfied ("curriculum complete, training pending").
- After training is complete, fill in the records and convert it to fully satisfied.
- Requiring training completion when onboarding new employees helps maintain continuous compliance.

## 6. Self-study

:::info Self-study mode (about 1 hour)
Take your time and understand each step.
:::

1. Read this document from beginning to end.
2. Run the training-manager agent with the command below:

   :::tip Check before execution
   Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
   :::

   ```bash
   cd agents/06-training-manager && claude
   ```

3. When the Claude prompt opens, type **`시작`**.

   <details>
   <summary>Agent conversation example (click to expand)</summary>

   Below is an example of how a conversation with the actual agent flows when you run it.

   **Agent guidance message:**

   > Hello! This is the agent that creates training program outputs.
   > Answer 3 questions and 3 training documents will be created automatically.

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

4. The agent asks three questions in order:
   - Number of people by job group (N developers / N managers / N operations)
   - Preferred training format (Online self-paced / In-person classroom / Blended)
   - Purpose of training completion proof (For internal records / for audit preparation / for certification submission)
5. After the agent generates the outputs, check the results in the `output/training/` folder.

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

> `completion-tracker.md` is created as an empty form. You must fill it in yourself after completing the actual training.
> :::

:::info Standard requirements met
Completing this lab meets the requirements below:

**ISO/IEC 5230**

| Item ID | Requirements         | Self-certification checklist                                                                         |
| ------- | -------------------- | ---------------------------------------------------------------------------------------------------- |
| 3.1.2   | Proof of competency  | Do you have documented evidence that each program participant has completed the necessary training?  |
| 3.1.3   | Awareness Assessment | Do you have documented evidence that your program participants are aware of your open source policy? |

**ISO/IEC 18974**

| Item ID | Requirements                  | Self-certification checklist                                                                                            |
| ------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 4.1.2   | Proof of security competency  | Do you have documented evidence that each program participant has the necessary competence for security assurance?      |
| 4.1.3   | Security Awareness Assessment | Do you have documented evidence that your program participants are aware of your open source security assurance policy? |

:::

## 7. Generated outputs

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

> 📋 **Example output**: You can see the actual format of the generated files in [Training Output Best Practices](/reference/samples/training).

## 9. Next steps

Once you have built your training program, it is time to prepare your self-certification declaration.

Go to the final chapter or run the agent right away.

To read the chapter document first, go to [Self-certification declaration: final step](../07-conformance/index.md).

:::tip Check before execution
Terminate the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/07-conformance-preparer && claude
```
