---
date: 2026-03-20
version: '1.0'
checklist:
  - 'ISO/IEC 5230: G1.4 (3.1.2), G2.3 (3.1.3)'
  - 'ISO/IEC 18974: G1.4 (4.1.2), G2.3 (4.1.3)'
self_study_time: 1 hour
---

# education system:Raise open source awareness throughout your organization

## 1. What we do in this chapter

Establish training curriculum for each occupation,Creating a completion tracking system,We organize educational resources that you can use for free. Completing this chapter will provide a foundation for all relevant members of your organization to understand and implement open source policies and processes.

Both standards require proof that personnel and relevant members have completed training. No matter how well you have policy documents and process procedures,,If members do not know the contents, actual compliance cannot be achieved.

## 2. Background knowledge:Why training is a standard requirement

### Why policies and processes alone are not enough

Even if there are policies and processes, they won’t work if people don’t know about them. ISO/IEC 5230 and 18974 do not simply check whether a document exists. actually know the document,understand,We check together to see if there are any members who can follow. Training completion records are one of the key pieces of evidence for self-certification.

### Training requirements of ISO/IEC 5230 and 18974

**ISO/IEC 5230 (License Compliance)**

- **3.1.2 (G1.4)**:Ensure that program participants are aware of the existence of policies regarding open source license compliance.
- **3.1.3 (G2.3)**:Program participants have policy goals,Make sure they understand their contributions and relevant roles.

**ISO/IEC 18974 (security assurance)**

- **3.1.2 (G1.4)**:Ensure that program participants are aware of the existence of a security assurance policy.
- **3.1.3 (G2.3)**:Ensure that program participants understand the goals of the security assurance policy and their roles.

> This step is ISO/IEC 5230 G1.4(3.1.2), G2.3 (3.1.3)and ISO/IEC 18974 G1.4(4.1.2), G2.3 (4.1.3)Meets your requirements.

**Records of training completion serve as evidence of self-certification.** When reviewing certification, “Who,when,You must have records showing “what kind of training you received.” The completion tracking sheet you create in this chapter will be the proof document.

## 3. Required training content for each job group

| Occupation          | Required training content                                                                           | Recommended Time |
| ------------------- | --------------------------------------------------------------------------------------------------- | ---------------- |
| Developer           | Open source licensing basics,Approval Process for Use,SBOM concept,vulnerability Response Procedure | 4 hours          |
| Manager/Team Leader | Open source policy overview,Understanding legal risks,Role in the Approval Process                  | 2 hours          |
| Legal/Purchasing    | License Detailed Obligations,Contract Open Source Terms                                             | 3 hours          |
| Security Manager    | vulnerability identification and response,Interpreting CVSS scores,18974 Requirements               | 3 hours          |

> Real corporate training examples(SKT,cacao,NC Soft, etc.)and educational materials [KWG Open Source Guide — Education](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/5-training/)See .

## 4. List of free educational resources

| Resources                             | Provided by organization | level                 | language | Link                                                                                          |
| ------------------------------------- | ------------------------ | --------------------- | -------- | --------------------------------------------------------------------------------------------- |
| OpenChain Training Materials          | OpenChain Project        | Beginner~Intermediate | English  | https://www.openchainproject.org/resources                                                    |
| Open Source Licensing Basics (LFC193) | Linux Foundation         | Beginner              | English  | LFC193 Course(Linux Foundation Training)                                                      |
| NIPA Open Source License Guide        | NIPA                     | Beginner~Intermediate | Korean   | NIPA open SW portal                                                                           |
| OpenChain KWG Training Materials      | OpenChain KWG            | Intermediate          | Korean   | https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/5-training/ |
| SPDX official documentation           | SPDX Community           | Intermediate          | English  | SPDX Official Site(spdx.dev)                                                                  |
| CycloneDX official documentation      | CycloneDX Community      | Intermediate          | English  | CycloneDX Official Site(cyclonedx.org)                                                        |

## 5. How to manage training completion records

Training completion records can be easily managed using a spreadsheet or markdown file without any additional tools. What is important is not the format but the record itself.

> ⚠️ **completion-tracker.md is a document filled in after training.**
> When you run the agent, it is normal for an empty template to be created.
> After completing the training, please add your completion record in the format below.
> This file is ISO/IEC 5230 §3.1.2.3(Competency assessment evidence)and 18974 §4.1.2.4.

`output/training/completion-tracker.md` format example:

| Name          | Occupation    | Education name               | Soo-il Lee | Confirmer                  |
| ------------- | ------------- | ---------------------------- | ---------- | -------------------------- |
| Hong Gil-dong | Developer     | Open source licensing basics | 2026-03-20 | Open source representative |
| Cheolsu Kim   | Administrator | Open source policy overview  | 2026-03-21 | Open source representative |

**Use completion-tracker.md when self-authenticating:**

- When first authenticating, if training has not been completed, “training curriculum is complete”,Partially satisfied as “to be completed”
- After completing training, fill in the record and convert to fully satisfied
- Continuous compliance can be maintained by requiring training completion when onboarding new employees.

## 6. Self-study

:::info Self-study mode(About 1 hour)
Take your time and understand each step.
:::

1. Read this document from beginning to end.
2. Run the training-manager agent with the command below::

   :::tip Check before execution
   Terminate the current Claude session first(`/exit` or `Ctrl+C`)After doing it,Run the command below in a new terminal.
   :::

   ```bash
   cd agents/06-training-manager && claude
   ```

3. When the Claude prompt opens, type **`시작`**.

   <details>
   <summary>Agent conversation example(Click to expand)</summary>

   Below is an example of a conversation flow with an actual agent. When running, it goes like this.

   **Agent guidance message:**

   > hello! It is an agent that creates education system output.
   > Answer 3 questions and 3 training documents will be automatically created.

   ***

   **Question 1/3** — Please tell us the number of people in each job group.(N developers / N managers / N operations)

   `Sample answer:40 developers,5 managers,5 people in operation

   **Question 2/3** — What is your preferred form of education?(Online Autonomous / Offline Aggregation / Mixed)

   `Sample answer:Online autonomy`

   **Question 3/3** — Do I need proof of training completion?(For internal records / for audit preparation / for certification submission)

   `Sample answer:For certification submission`

   ***

   **Example of output upon completion of creation:**

   | file                                    | Content                                                                |
   | --------------------------------------- | ---------------------------------------------------------------------- |
   | `output/training/curriculum.md`         | Training curriculum and recommended time for each occupation           |
   | `output/training/completion-tracker.md` | Completion Tracking Sheet(blank form,Fill out directly after training) |
   | `output/training/resources.md`          | List of Free Educational Resources                                     |

   **Items that require manual entry:**
   - Training implementation schedule(annual plan)
   - Deciding how to prove completion(Certificate of Completion / Confirm Email / Signature)

   </details>

4. The agent asks three questions in order.:
   - Number of people by occupation(N developers / N managers / N operations)
   - preferred form of education(Online Autonomous / Offline Aggregation / Mixed)
   - Purpose of proof of training completion(For internal records / for audit preparation / for certification submission)
5. After the agent generates the output, check the results in the `output/training/` folder.

:::tip expected result
Upon completing the exercise, the three files below will be created.

**Created file:**

- `output/training/curriculum.md`
- `output/training/completion-tracker.md`
- `output/training/resources.md`

**Items that must be included in the file:**

- Training items and recommended times for each job type
- How to prove completion(Certificate of Completion / Signature / Email Confirmation)
- Regular training schedule(More than once a year)

> `completion-tracker.md` is created as an empty form. You must fill it out yourself after completing the actual training.
> :::

:::info Standard requirements met
Completing this lab will meet the requirements below:

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

## 7. Output generated

When you complete this chapter, the following files will be created in the `output/training/` folder.:

- **curriculum.md**:Training curriculum by occupation(educational items,recommended time,Includes priority)
- **completion-tracker.md**:Training Completion Tracking Sheet(Self-certified evidence document)
- **resources.md**:List of Free Educational Resources(Select according to organizational situation)

## 8. Completion Confirmation Checklist

- [ ] `output/training/curriculum.md` created
- [ ] `output/training/completion-tracker.md` created
- [ ] `output/training/resources.md` created
- [ ] Training items are defined for each job group
- [ ] Method of proof of completion has been decided

> 📋 **Example of output**: [Educational Output Best Practices](/reference/samples/training)You can check the actual format of the generated file at .

## 9. Next steps

If you have completed building an education system,Now it’s time to prepare your self-certification declaration.

Go to the last chapter or run the agent immediately:

To read the chapter document first, go to [Self-certification declaration]:final step](../07-conformance/index.md)Go to .

:::tip Check before execution
Terminate the current Claude session first(`/exit` or `Ctrl+C`)After doing it,Run the command below in a new terminal.
:::

```bash
cd agents/07-conformance-preparer && claude
```
