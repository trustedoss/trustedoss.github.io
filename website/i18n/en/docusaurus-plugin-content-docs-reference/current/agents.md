---
id: agents
title: Create deliverables with AI agents
sidebar_label: Agent selection guide
sidebar_position: 4
description: 'How agents map to chapters and deliverables, and which one to pick. Covers all nine program-building agents and seven automation agents.'
---

# Create deliverables with AI agents

What makes Trusted OSS different is that an AI agent asks about your company and then generates deliverables that meet the OpenChain standards. Instead of filling in blank templates, you answer questions and get policy, process, and organization documents written for your company. This page shows which agent produces what.

Agents come in two groups. Program-building agents produce the deliverables you need for self-certification. Automation agents apply that policy to your CI and developer tools, or analyze scanner output.

## Program-building agents

Each maps to one chapter of the [Open Source Management](/docs) track. If self-certification is your goal, run them in the order below.

| Chapter         | Agent (`agents/…`)                 | Deliverables                                                                                                                                        |
| --------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2 Organization  | `02-organization-designer`         | role-definition, raci-matrix, appointment-template                                                                                                  |
| 3 Policy        | `03-policy-generator`              | oss-policy, license-allowlist                                                                                                                       |
| 4 Process       | `04-process-designer`              | usage-approval, distribution-checklist, vulnerability-response, inquiry-response, process-diagram, (conditional) contribution / project-publication |
| 5 SBOM creation | `05-sbom-guide`, `05-sbom-analyst` | SBOM (cdx.json), sbom-commands, license-report, copyleft-risk                                                                                       |
| 5 SBOM managing | `05-sbom-management`               | sbom-management-plan, sbom-sharing-template                                                                                                         |
| 5 Vulnerability | `05-vulnerability-analyst`         | cve-report, remediation-plan                                                                                                                        |
| 6 Training      | `06-training-manager`              | curriculum, completion-tracker, resources                                                                                                           |
| 7 Certification | `07-conformance-preparer`          | gap-analysis, declaration-draft, submission-guide                                                                                                   |

To see what the output actually looks like, read [Policy deliverables best practice](./samples/policy).

## Automation agents

Use these once policy exists, in the [DevSecOps](/devsecops/intro) and [AI Coding Governance](/ai-coding/intro) tracks. Setup agents analyze your project and write configuration files. Analysis agents take a scanner's output file and turn it into a response report.

| Group    | Agent (`agents/…`)  | What it does                                                                                            | Deliverables                                                                                               |
| -------- | ------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Setup    | `ai-coding-setup`   | Analyzes your project and writes rules files for AI coding tools                                        | Per-tool rules under `output/ai-coding/` (CLAUDE.md, Cursor, Copilot, Devin Desktop)                       |
| Setup    | `devsecops-setup`   | Analyzes your project and writes CI/CD workflow and policy files                                        | devsecops-pr.yml, devsecops-merge.yml, devsecops-schedule.yml, .gitlab-ci.yml, .gitleaks.toml, .grype.yaml |
| Setup    | `level2-automation` | Writes workflows that file scan results as issues (`issue-tracker`) or post them on a PR (`pr-comment`) | GitHub Actions and GitLab CI workflows                                                                     |
| Analysis | `sast-analyst`      | Reads Semgrep or CodeQL SARIF output and gives priorities and fix code                                  | sast-report.md                                                                                             |
| Analysis | `sbom-vuln-analyst` | Reads an SBOM file or grype scan output and organizes the vulnerability response                        | sbom-vuln-report.md, .grype.yaml suppression examples                                                      |
| Analysis | `secret-analyst`    | Reads Gitleaks output and gives immediate response steps per secret type                                | secret-response-report.md, .gitleaks.toml suppression examples                                             |
| Analysis | `iac-fixer`         | Reads Checkov output and writes corrected IaC code for each violation                                   | iac-fix-report.md                                                                                          |

:::warning If a secret really was exposed
Revoke and reissue that credential before you run `secret-analyst`. Analysis comes second.
:::

## Which agent for which situation

- **If self-certification is the goal**, run 2 Organization → 3 Policy → 4 Process → 5 Tools → 6 Training → 7 Certification in order. This path is required.
- **If you only need a policy quickly**, you can start at `03-policy-generator`.
- **If you only want to check SBOM and vulnerabilities**, use the chapter 5 agents (`05-sbom-*`, `05-vulnerability-analyst`) alone.
- **If you need contribution or internal-release procedures**, answer "yes" to the matching question while running the chapter 4 agent and the conditional deliverables are generated too.
- **To apply policy to developer tools**, use `ai-coding-setup` for rules files and `devsecops-setup` for CI workflows.
- **If you already run scanners**, pick the analysis agent that matches your output file: SARIF goes to `sast-analyst`, SBOM and grype results to `sbom-vuln-analyst`, Gitleaks results to `secret-analyst`, and Checkov results to `iac-fixer`.

## How to run any agent

Every agent runs the same way.

:::tip Before you run this
Exit the current Claude session first (`/exit` or `Ctrl+C`), then run the command below in a new terminal. Replace `XX-agent-name` with an agent name from the tables above.
:::

```bash
cd agents/XX-agent-name
claude
```

When the prompt opens, type `start` and answer the agent's questions. Generated deliverables are saved under `output/`.

`level2-automation` holds two agents, `issue-tracker` and `pr-comment`, so it takes one more level.

:::tip Before you run this
Exit the current Claude session first.
:::

```bash
cd agents/level2-automation/issue-tracker
claude
```

## Next steps

- If you have not set up your environment yet, start with the [Environment setup](/docs/setup) chapter.
- To decide what to do first, see the next-steps section of [Overview: the two standards and the whole journey](/docs).
