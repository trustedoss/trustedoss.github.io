---
id: iso-mapping
title: 'ISO Standards Linkage (AI Coding)'
sidebar_label: 'ISO Standards Linkage'
description: Shows in a mapping table which ISO/IEC 5230 and 18974 requirements the implementation in the AI coding guide reinforces at the development stage.
sidebar_position: 11
---

# ISO/IEC 5230 · 18974 Linkage (AI Coding)

This page shows which requirements of the two standards the AI coding guide's implementations **operate and strengthen at the development stage**.

:::note The Open Source Management guide is the authority for meeting the standards
The deliverables that **formally satisfy** the standard requirements (policy, SBOM, vulnerability reports, etc.) are produced in the [Open Source Management](/en/docs) guide.
The [Requirements Detail Matrix](/en/reference/requirements-matrix) is the canonical per-item mapping of certification questions and verification material.
The AI coding guide is a means of **automatically applying that policy to daily development** to strengthen execution.
:::

## What does it strengthen?

The policy you created in the Open Source Management guide exists as a document. The problem is that developers do not remember it every time they write code.
The AI coding guide internalizes that policy into **AI tool Rules and CI gates**, so it is enforced automatically at code-generation and commit time.

## Requirement mapping

| AI coding implementation                                                     | Standard requirement strengthened                    | How                                                                           |
| ---------------------------------------------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------- |
| Internalize open source policy in Rules ([Rules Template](./rules-template)) | 5230 §3.1.1 Policy operation & communication         | AI recognizes the policy at code-generation time                              |
| Allowed/forbidden license lists in Rules                                     | 5230 §3.1.5 License obligation identification        | AI avoids or warns about forbidden-license packages                           |
| CI license gate ([Quick CI/CD](./cicd-quick))                                | 5230 §3.3.2 License compliance                       | Build is blocked when forbidden licenses are found                            |
| SBOM refresh on dependency change                                            | 5230 §3.3.1 · 18974 §4.3.1 SBOM                      | SBOM generated automatically with cdxgen/syft                                 |
| SCA and CVE scanning in CI ([AI Security Review](./ai-security-review))      | 18974 §4.3.2 Vulnerability identification & tracking | PRs blocked with npm audit, trivy, and grype                                  |
| Continuous post-deployment monitoring (Stage 5)                              | 18974 §4.3.2 Vulnerability response                  | New CVEs tracked with Dependabot and Renovate                                 |
| AI coding tool usage policy ([Usage Policy](./usage-policy))                 | 5230 §3.1.1 · 18974 §4.1.1 Policy                    | Tool approval, data handling, and accountability adopted as a policy document |
| Roles and responsibilities ([Usage Policy](./usage-policy))                  | 5230 §3.1.2 · 18974 §4.1.2 Competence                | Policy owner, tool administrator, security, and legal roles assigned          |
| AI coding training and records ([Usage Policy](./usage-policy))              | 5230 §3.1.3 · 18974 §4.1.3 Awareness                 | AI coding items in onboarding and regular training                            |
| MCP server review and SBOM entry ([4c](./agent-governance))                  | 5230 §3.3.1 · 18974 §4.3.1 SBOM                      | Servers agents call recorded as `services`                                    |
| Test gate and test-weakening check ([Testing](./testing))                    | 18974 §4.3.2 Vulnerability response                  | Confirms a fix did not introduce a regression                                 |

:::note
The AI coding guide **automates the execution** of the items above, but the self-certification declaration and evidence deliverables are completed in the [Open Source Management](/en/docs) guide.
:::

## Next steps

- To build the standards system from scratch, see the [Open Source Management guide](/en/docs)
- For organization-wide pipeline-level security enforcement, see the [DevSecOps guide](/en/devsecops/intro)
