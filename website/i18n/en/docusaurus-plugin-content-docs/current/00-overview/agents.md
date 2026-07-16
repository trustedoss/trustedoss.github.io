---
description: 'AI agents automatically generate company-tailored open source deliverables. See the mapping of agents, chapters, and deliverables at a glance.'
date: 2026-06-05
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 10 minutes
sidebar_position: 7
sidebar_label: Create deliverables with AI agents
---

# Create deliverables with AI agents

The core of TrustedOSS is that **an AI agent asks about your company's situation and automatically creates deliverables that conform to the OpenChain standards**. Instead of filling in blank templates yourself, you answer questions and the policy, process, and organization documents tailored to your company are generated. This page shows at a glance which agent creates what.

## Agents at a glance

| Chapter           | Agent (`agents/…`)                 | Generated deliverables                                                                                                                              |
| ----------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2 Organization    | `02-organization-designer`         | role-definition, raci-matrix, appointment-template                                                                                                  |
| 3 Policy          | `03-policy-generator`              | oss-policy, license-allowlist                                                                                                                       |
| 4 Process         | `04-process-designer`              | usage-approval, distribution-checklist, vulnerability-response, inquiry-response, process-diagram, (conditional) contribution / project-publication |
| 5 SBOM creation   | `05-sbom-guide`, `05-sbom-analyst` | SBOM(cdx.json), sbom-commands, license-report, copyleft-risk                                                                                        |
| 5 SBOM management | `05-sbom-management`               | sbom-management-plan, sbom-sharing-template                                                                                                         |
| 5 Vulnerability   | `05-vulnerability-analyst`         | cve-report, remediation-plan                                                                                                                        |
| 6 Training        | `06-training-manager`              | curriculum, completion-tracker, resources                                                                                                           |
| 7 Certification   | `07-conformance-preparer`          | gap-analysis, declaration-draft, submission-guide                                                                                                   |

You can see the actual form of the generated deliverables in the [Policy Deliverable Best Practices](/reference/samples/policy).

## Which agent for which situation

- **If your goal is self-certification**, run each agent in the order 2 Organization → 3 Policy → 4 Process → 5 Tools → 6 Training → 7 Certification. This is the required path.
- **If you only need a policy quickly**, you can start from `03-policy-generator`.
- **If you only want to check SBOM and vulnerabilities**, use only the 5 Tools agents (`05-sbom-*`, `05-vulnerability-analyst`).
- **If you need contribution or internal publication procedures**, answer "yes" to the relevant question while running the 4 Process agent, and the conditional deliverables are generated together.

## Common way to run

All agents are run in the same way.

:::tip Check before running
First exit the current Claude session (`/exit` or `Ctrl+C`), then run the command below in a new terminal. Put the agent name from the table above in place of `XX-agent-name`.
:::

```bash
cd agents/XX-agent-name
claude
```

When the prompt opens, type `start` and answer the agent's questions. The generated deliverables are saved in the `output/` folder.

## Next steps

- If you have not set up your environment yet, start from the [Environment preparation](../01-setup/index.md) chapter.
- To choose where to begin, see [The start path that fits you](./start-path.md).
