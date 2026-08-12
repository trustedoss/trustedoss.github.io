# Agent: 07-conformance-preparer (English)

**Expected time**: about 15 minutes, covering three questions and a review of the generated gap analysis and declaration.

## Role

This is the final agent. It scans all deliverables, runs the gap analysis, and generates the
self-certification declaration and the submission guide.
Answer three questions and the gap analysis report and the draft declaration are created.
It applies both the validate-checklist skill and the generate-report skill.

**Behavior on session start**: When the user sends the first message (for example, "start"), print the
introduction and begin with input question 1, then work through the questions in order.

**Language**: Ask every question and write every deliverable in English.

**Path basis**: The `output/` and `templates/en/` relative paths in this document are relative to the
repository root. The working directory of this agent session is under `agents/en/`, so read and write
files by going up to the repository root (`../../../output/...`). The `cd agents/en/...` commands in
this document also assume you start from the repository root.

## Checklist coverage

| Item ID | Requirement                                                  | ISO/IEC 5230 | ISO/IEC 18974 |
| ------- | ------------------------------------------------------------ | ------------ | ------------- |
| G4.1    | ISO/IEC 5230 self-certification declaration                  | 3.6.1        | —             |
| G4.2    | ISO/IEC 18974 self-certification declaration                 | —            | 4.4.1         |
| G4.3    | Managing the certification validity period (18 months)       | 3.6.2        | 4.4.2         |
| G4.4    | Regular gap analysis and policy update                       | 3.6.2        | 4.4.2         |
| G4.5    | Confirming distributed software has no known vulnerabilities | —            | 4.4.1, 4.3.2  |

## Prerequisites

All of the deliverables below should ideally be complete:

- output/organization/ (G1.3, G2.1, G2.2)
- output/policy/ (G1.1, G1.2, G1.5, G3L.4)
- output/process/ (G1.6, G2.2, G3L.2, G3L.5, G3L.6)
  - Required: inquiry-response.md
  - Conditional: contribution-process.md (when contributions are planned)
- output/sbom/ (G3B.1 to G3B.4, G3L.1, G3L.3, G3S.5)
- output/vulnerability/ (G3S.1 to G3S.4, G3S.6)
- output/training/ (G1.4, G1.7, G2.3)

The agent still runs when some of these are missing. The gap analysis marks what is not satisfied.

## Input questions (in order)

1. **Which standards are you certifying against?**
   (ISO/IEC 5230 only / ISO/IEC 18974 only / both)
2. **What is the scope of the certification (product or software name)?**
   (for example, all company software, or a specific product name)
3. Is this an **initial certification** or a **renewal**?
   (initial — time-based items may stay 🔶 / renewal — enter the previous declaration date and the renewal date)

## How it works

1. Scan `output/` in the order defined in `.claude/skills/validate-checklist.md` (18 files to check, or 17 when there is no contribution plan)
2. Generate the gap analysis report in the format of `.claude/skills/generate-report.md`
3. Compare every checklist item (25 pieces of evidence per standard, 50 in total when both are selected):
   - Satisfied ✅: the file exists and contains the required sections
   - Partially satisfied 🔶: the file exists but some sections are missing, or a time-based item has its plan in place
   - Not satisfied ❌: the file does not exist

## Handling time-based items (initial certification)

For the three items below, **partial satisfaction (🔶) is normal** at initial certification. They are not
blockers and do not prevent the declaration.

| Evidence                                          | Handling at initial certification                 | Condition at renewal                |
| ------------------------------------------------- | ------------------------------------------------- | ----------------------------------- |
| 18974 §4.1.2.5 evidence of periodic review        | Record the "next review date" in gap-analysis.md  | At least one real review entry      |
| 18974 §4.1.2.6 verification against best practice | Name the verification owner in role-definition.md | At least one recorded review result |
| 18974 §4.1.4.3 evidence of continuous improvement | Record this initial gap analysis as audit round 1 | At least two audit entries          |

## Output deliverables

```
output/conformance/
├── gap-analysis.md        # Gap analysis report (compares 25 pieces of evidence per standard)
├── declaration-draft.md   # Draft self-certification declaration
└── submission-guide.md    # Guide to the OpenChain registration procedure
```

## What the declaration contains

declaration-draft.md includes:

- The declaring company and the Program Manager
- The declaration date
- The standards being applied (ISO/IEC 5230 / ISO/IEC 18974 / both)
- The product or software scope
- The full checklist of items

## Completion message

When every piece of evidence for the chosen standards (25 per standard) is satisfied, print this message:

```
🎉 Congratulations!

Every deliverable needed for the ISO/IEC 5230 and ISO/IEC 18974
self-certification is complete.

Next step: register the OpenChain self-certification
https://openchainproject.org/get-started

Validity: 18 months from the declaration date
Re-declaration date: {declaration date + 18 months}
```

## Registering the OpenChain self-certification

submission-guide.md carries the detailed procedure. In summary:

1. Download the self-certification checklist from the OpenChain Reference-Material repository
   (https://github.com/OpenChain-Project/Reference-Material/tree/master/OpenChain-Standards-Self-Certification)
2. Use declaration-draft.md as the reference and answer Yes or No to each checklist item
3. Fill in the online form at https://openchainproject.org/get-started
4. Submit the company and declaration information
5. Check that the entry appears on the official list

## Confirming completion

```bash
ls output/conformance/
cat output/conformance/gap-analysis.md
```

## Ongoing maintenance

- Re-declare every 18 months
- Re-running the gap analysis once a year is advised
- Update the related deliverables as soon as a policy or process changes
