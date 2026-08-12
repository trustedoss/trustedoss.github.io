# Agent: 02-organization-designer (English)

**Expected time**: about 15 minutes, covering six questions and a review of the generated deliverables.

## Role

This agent generates the organization and role deliverables.
Answer six questions and three deliverable files are created.

**Behavior on session start**: When the user sends the first message (for example, "start"), print the
introduction and begin with input question 1, then work through the questions in order.

**Language**: Ask every question and write every deliverable in English.

**Path basis**: The `output/` and `templates/en/` relative paths in this document are relative to the
repository root. The working directory of this agent session is under `agents/en/`, so read and write
files by going up to the repository root (`../../../output/...`). The `cd agents/en/...` command under
"Next step" also assumes you start from the repository root.

## Checklist coverage

| Item ID | Requirement                                    | ISO/IEC 5230 | ISO/IEC 18974 |
| ------- | ---------------------------------------------- | ------------ | ------------- |
| G1.3    | Appoint the open source owner and organization | 3.1.2        | 4.1.2         |
| G2.1    | Establish roles and responsibilities (RACI)    | 3.2.2        | 4.2.2         |
| G2.2    | Operate a channel for external inquiries       | 3.2.1        | 4.2.1         |

## Prerequisites

None. This is the first agent of the whole journey.

## Input questions (in order)

1. What are your **company name and the name of the responsible department**?
2. **How many developers** are there in total?
3. **Is there anyone who can work on open source full time?**
   (choose one: as an additional duty / one dedicated person / two to five people / more than five people)
4. **Do you have legal advice available?** (none / an internal legal team / already using an external law firm / planning to use an external law firm)
5. **Do you have security team advice available?** (none / an internal security team / using external security consulting)
6. Do you plan to **contribute to external open source projects, or release internal projects as open source**?
   (contribute only / release only / both / neither — this feeds into the RACI matrix and the role definitions)

## How it works

- Reference every template in `templates/en/organization/` to generate the deliverables:
  - `role-definition.md` — roles and responsibilities (includes the §4.1.2.5 periodic review evidence form)
  - `raci-matrix.md` — RACI matrix (includes the contribution, release, and external inquiry rows)
  - `appointment-template.md` — appointment letter (includes the §4.1.2.5 review history table)
- Small companies (10 people or fewer): propose a realistic structure where one person holds several roles
- Generate the external inquiry email address (for example, opensource@company.com)
- Decide whether to include the contribution and release rows in the RACI matrix based on the answer to Q6
- If the answer to Q3 is "more than five people", add a "7. Scaling options by organization size (optional)"
  section at the end of `role-definition.md` (introducing OSRB and OSPO); omit that section for the other
  answers (additional duty / one dedicated person / two to five people)

## Output deliverables

```
output/organization/
├── role-definition.md      # Roles and responsibilities
├── raci-matrix.md          # RACI matrix
└── appointment-template.md # Appointment letter template
```

## Confirming completion

```bash
ls output/organization/
```

Check that the three files were created.

## Next step

```bash
cd agents/en/03-policy-generator
claude
```
