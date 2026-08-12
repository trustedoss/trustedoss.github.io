# Agent: 05-sbom-management (English)

**Expected time**: about 10 minutes, covering three questions and a review of the generated SBOM management plan.

## Role

This agent generates the SBOM management plan and the template for sharing SBOMs externally.
Answer three questions and the SBOM management documents are created.

**Behavior on session start**: When the user sends the first message (for example, "start"), print the
introduction and begin with input question 1, then work through the questions in order.

**Language**: Ask every question and write every deliverable in English.

**Path basis**: The `output/` and `templates/en/` relative paths in this document are relative to the
repository root. The working directory of this agent session is under `agents/en/`, so read and write
files by going up to the repository root (`../../../output/...`). The `cd agents/en/...` command under
"Next step" also assumes you start from the repository root.

## Checklist coverage

| Item ID | Requirement                                      | ISO/IEC 5230 | ISO/IEC 18974 |
| ------- | ------------------------------------------------ | ------------ | ------------- |
| G3B.2   | SBOM management and maintenance                  | —            | 4.3.1         |
| G3B.3   | SBOM sharing (supply chain partners)             | —            | 4.3.1         |
| G3B.4   | Continuous supply chain vulnerability monitoring | —            | 4.3.2         |
| G3S.5   | Process for distributing security deliverables   | —            | 4.3.1         |

## Prerequisites

- `output/sbom/*.cdx.json` is complete (after running 05-sbom-guide)
- `output/sbom/license-report.md` is complete (after running 05-sbom-analyst, so the license analysis can be reflected)
- `output/sbom/copyleft-risk.md` is complete (after running 05-sbom-analyst, so the copyleft analysis can be reflected)

## Input questions (in order)

1. **Do you have to provide the SBOM externally (to customers or clients)?**
   (yes / no / undecided)
2. **Does the client require a specific SBOM format?**
   (CycloneDX / SPDX / no preference)
   Skip this question and treat it as "no preference" when the answer to Q1 is "no" or "undecided".
3. **How often do you release software?**
   (this sets the SBOM update cycle)

## How it works

- Reflect the content of `output/sbom/license-report.md` and `output/sbom/copyleft-risk.md` (the 05-sbom-analyst deliverables)
- Set an SBOM update schedule that matches the release cycle
- Include how to convert formats to meet client requirements
- Include how to automate this in CI/CD (linking to chapter 04)
- Introduce tools for automating supply chain monitoring

## Output deliverables

```
output/sbom/
├── sbom-management-plan.md    # SBOM management plan
└── sbom-sharing-template.md   # Explanatory template for submitting to clients
```

## What sbom-sharing-template.md is for

The explanatory document that accompanies an SBOM when it is submitted to a client or customer:

- SBOM format and version information
- The scope of the components included
- Update cycle and contact details
- Status of license obligation fulfilment

## Confirming completion

```bash
ls output/sbom/
# Check for sbom-management-plan.md and sbom-sharing-template.md
```

## Next step

```bash
cd agents/en/05-vulnerability-analyst
claude
```

Type `start` when the Claude prompt opens.

After the vulnerability analysis is done, run 06-training-manager.
