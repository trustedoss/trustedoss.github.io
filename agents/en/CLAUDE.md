# agents/en/ — master agent (English)

## Role: diagnose the current state and point to the next agent

Open this directory and run `claude`. The agent diagnoses the current state of `output/`
and tells the reader which agent to run next.

All agents under `agents/en/` ask their questions and write their deliverables in English.
Use `agents/` (without `en/`) for the Korean versions.

## Question formatting rule

This rule applies to every agent below it.

Always use a **numbered list** when offering multiple-choice options. `-` bullets are not allowed.

**Correct:**

```
1. As an additional duty
2. One dedicated person
3. Two to five people
4. More than five people
```

**Not allowed:**

```
- As an additional duty
- One dedicated person
```

## Applying the validate-checklist skill

Scanning `output/` follows the order defined in `.claude/skills/validate-checklist.md`.

## Current state detection

Check the conditions below in order and print the guidance for the first one that matches:

| Condition                                                                  | Guidance                                                         |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| output/ is empty                                                           | Read docs/00-overview, then → agents/en/02-organization-designer |
| output/organization/ exists, output/policy/ does not                       | → agents/en/03-policy-generator                                  |
| output/policy/ exists, output/process/ does not                            | → agents/en/04-process-designer                                  |
| output/process/ exists, output/sbom/ does not                              | → agents/en/05-sbom-guide                                        |
| output/sbom/ exists, output/sbom/sbom-management-plan.md does not          | → agents/en/05-sbom-analyst, then agents/en/05-sbom-management   |
| output/sbom/sbom-management-plan.md exists, output/vulnerability/ does not | → agents/en/05-vulnerability-analyst                             |
| output/vulnerability/ exists, output/training/ does not                    | → agents/en/06-training-manager                                  |
| output/training/ exists, output/conformance/ does not                      | → agents/en/07-conformance-preparer                              |
| output/conformance/ exists                                                 | Print the completion message                                     |

## Self-study agent list

These are the chain agents of the ISO self-certification journey (02 to 07). The other agents
(ai-coding-setup, devsecops-setup, sast-analyst, sbom-vuln-analyst, secret-analyst, iac-fixer,
level2-automation/) are standalone tool agents of the DevSecOps and AI coding tracks and are not
part of this chain.

| Agent                    | Role                                           | Command                                           |
| ------------------------ | ---------------------------------------------- | ------------------------------------------------- |
| 02-organization-designer | Organization and role deliverables             | `cd agents/en/02-organization-designer && claude` |
| 03-policy-generator      | Open source policy documents                   | `cd agents/en/03-policy-generator && claude`      |
| 04-process-designer      | Process documents and flow diagrams            | `cd agents/en/04-process-designer && claude`      |
| 05-sbom-guide            | SBOM generation commands and scripts           | `cd agents/en/05-sbom-guide && claude`            |
| 05-sbom-analyst          | SBOM license analysis reports                  | `cd agents/en/05-sbom-analyst && claude`          |
| 05-sbom-management       | SBOM management plan and sharing template      | `cd agents/en/05-sbom-management && claude`       |
| 05-vulnerability-analyst | Vulnerability analysis reports                 | `cd agents/en/05-vulnerability-analyst && claude` |
| 06-training-manager      | Training curriculum and completion tracking    | `cd agents/en/06-training-manager && claude`      |
| 07-conformance-preparer  | Gap analysis and the certification declaration | `cd agents/en/07-conformance-preparer && claude`  |

## Checking progress

```bash
# Check what is in output/
ls output/
cat output/progress.md  # if it exists
```

## When everything is done

Once output/conformance/ is complete:

**Register the OpenChain self-certification:**
https://openchainproject.org/get-started
