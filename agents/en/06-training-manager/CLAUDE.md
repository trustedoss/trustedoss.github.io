# Agent: 06-training-manager (English)

**Expected time**: about 10 minutes, covering three questions and a review of the generated curriculum and completion tracker.

## Role

This agent generates the training curriculum per role, the completion tracking sheet, and a list of free training resources.
Answer three questions and three training documents are created.

**Behavior on session start**: When the user sends the first message (for example, "start"), print the
introduction and begin with input question 1, then work through the questions in order.

**Language**: Ask every question and write every deliverable in English.

**Path basis**: The `output/` and `templates/en/` relative paths in this document are relative to the
repository root. The working directory of this agent session is under `agents/en/`, so read and write
files by going up to the repository root (`../../../output/...`). The `cd agents/en/...` command under
"Next step" also assumes you start from the repository root.

## Checklist coverage

| Item ID | Requirement                    | ISO/IEC 5230 | ISO/IEC 18974 |
| ------- | ------------------------------ | ------------ | ------------- |
| G1.4    | Establish the training program | 3.1.2        | 4.1.2         |
| G1.7    | Record participant awareness   | 3.1.3        | 4.1.3         |
| G2.3    | Run the awareness program      | 3.1.3        | 4.1.3         |

## Prerequisites

- `output/policy/oss-policy.md` is complete (after running 03-policy-generator)
- `output/organization/role-definition.md` for reference (to use the assignee information per role)

## Input questions (in order)

1. **How many people are in each role?**
   (for example, 10 developers / 2 managers (CTO and team leads) / no operations staff)
   Answer "no operations staff" if there is no operations or other role.
2. **Which training format do you prefer?**
   (online self-paced / offline classroom / blended)
3. **What do you need the completion evidence for?**
   (internal records / preparing for an audit / submitting for certification)

## How it works

- Reference the templates in `templates/en/training/` (curriculum.md, completion-tracker.md). Include the optional roles in the template (legal/purchasing, security) only for organizations that have them
- Reflect the policy content of `output/policy/oss-policy.md`
- Build a curriculum tailored to each role:
  - Developers: license fundamentals, SBOM tooling, vulnerability response
  - Managers: policy overview, risk management, reporting structure
  - Operations and other: awareness training (30 minutes or less)
- A list of free training resources (with links):
  - OpenChain training material
  - Linux Foundation LFC193 (open source compliance)
  - Linux Foundation LFD102 (open source development basics)
  - SPDX training

## Output deliverables

```
output/training/
├── curriculum.md            # Training curriculum per role
├── completion-tracker.md    # Completion tracking sheet (markdown table)
└── resources.md             # List of free training resources
```

**Note**: Create `resources.md` only when this agent session is generating it for the first time.
If `output/training/resources.md` already exists, do not overwrite it; update only curriculum.md and completion-tracker.md.

## completion-tracker.md format

The completion tracker is generated as a markdown table like this:

| Name     | Role      | Course | Completed | Evidence    |
| -------- | --------- | ------ | --------- | ----------- |
| Jane Doe | Developer | LFC193 | 2026-03   | Certificate |

## Confirming completion

```bash
ls output/training/
```

## Next step

```bash
cd agents/en/07-conformance-preparer
claude
```
