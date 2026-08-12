# Agent: 03-policy-generator (English)

**Expected time**: about 15 minutes, covering five questions and a review of the generated policy documents.

## Role

This agent generates open source policy documents tailored to the company.
Answer five questions and two policy documents are created.

**Behavior on session start**: When the user sends the first message (for example, "start"), print the
introduction and begin with input question 1, then work through the questions in order.

**Language**: Ask every question and write every deliverable in English.

**Path basis**: The `output/` and `templates/en/` relative paths in this document are relative to the
repository root. The working directory of this agent session is under `agents/en/`, so read and write
files by going up to the repository root (`../../../output/...`). The `cd agents/en/...` command under
"Next step" also assumes you start from the repository root.

## Checklist coverage

| Item ID | Requirement                                   | ISO/IEC 5230 | ISO/IEC 18974 |
| ------- | --------------------------------------------- | ------------ | ------------- |
| G1.1    | Establish and document the open source policy | 3.1.1        | 4.1.1         |
| G1.2    | Establish the security assurance policy       | —            | 4.1.1         |
| G1.5    | Define the program scope                      | 3.1.4        | 4.1.4         |
| G3L.4   | Establish the open source contribution policy | 3.5.1        | —             |

## Prerequisites

- `output/organization/role-definition.md` is complete (after running 02-organization-designer)

## Input questions (in order)

1. **How do you distribute your software?**
   (SaaS / app store / embedded / internal use / a mix)
2. **Which programming languages and package managers do you mainly use?**
3. **Do you plan to contribute to open source projects?**
4. **Do you deliver software to external customers or clients?**
5. **Do you have a license review procedure today?**
   (yes / no / informally)

## How it works

- Reference every template in `templates/en/policy/`:
  - `oss-policy.md` — the body of the open source policy
  - `license-allowlist.md` — the allowed license list per distribution method
- Use the assignee information from `output/organization/role-definition.md`
- Build the allowed license list differently depending on the distribution method
  - SaaS: watch AGPL closely, GPL is relatively free
  - Embedded or distributed: restrict GPL strictly, avoiding copyleft is advised
- If the answer to Q3 is that contributions are planned: state that `contribution-process.md` has to be
  generated in 04-process-designer
- Handling Q4:
  - "Yes" (there are clients): add sections on the SBOM submission obligation and on client license requirements
  - "No" (SaaS and similar, no delivery): omit the SBOM submission obligation section and mention SBOMs for internal management instead
- Generate the vulnerability response times in the `oss-policy.md` KPI table as `Critical: 1 week, High: 4 weeks, Medium: within 1 month`, and include a note below the table saying stricter deadlines can be applied
- Always include the "Measuring and improving program effectiveness" subsection immediately below the "Performance metrics (KPI)" subsection (regular evaluation cycle, evaluation reporting, continuous improvement, resource sufficiency review)
- Always include the "Policy change requests and operation" section at the end of `oss-policy.md` (refer to it by name rather than by number, because the numbering shifts depending on which conditional sections are included). It covers the five-step change request flow and monitoring of regulatory and standards change. Reflect the current procedure according to the answer to Q5

## Output deliverables

```
output/policy/
├── oss-policy.md          # Open source policy document
└── license-allowlist.md   # Allowed license list
```

## Confirming completion

```bash
ls output/policy/
```

## Next step

```bash
cd agents/en/04-process-designer
claude
```
