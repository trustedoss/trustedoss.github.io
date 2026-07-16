---
id: iso-mapping
title: 'ISO Standards Linkage (AI Coding)'
sidebar_label: 'ISO Standards Linkage'
sidebar_position: 12
---

# ISO/IEC 5230 · 18974 Linkage (AI Coding)

This page shows which requirements of the two standards the AI coding guide's implementations **operate and strengthen at the development stage**.

:::note The Build Your System guide is the authority for meeting the standards
The deliverables that **formally satisfy** the standard requirements (policy, SBOM, vulnerability reports, etc.) are produced in the [Build Your System](/docs) track.
The [Checklist Mapping](/docs/overview/checklist-mapping) is the authoritative integrated mapping of all requirements.
The AI coding guide is a means of **automatically applying that policy to daily development** to strengthen execution.
:::

## What does it strengthen?

The policy you created in Build Your System exists as a document. The problem is that developers do not remember it every time they write code.
The AI coding guide internalizes that policy into **AI tool Rules and CI gates**, so it is enforced automatically at code-generation and commit time.

## Requirement mapping

| AI coding implementation                                                     | Standard requirement strengthened                    | How                                                 |
| ---------------------------------------------------------------------------- | ---------------------------------------------------- | --------------------------------------------------- |
| Internalize open source policy in Rules ([Rules Template](./rules-template)) | 5230 §3.1.1 Policy operation & communication         | AI recognizes the policy at code-generation time    |
| Allowed/forbidden license lists in Rules                                     | 5230 §3.1.5 License obligation identification        | AI avoids or warns about forbidden-license packages |
| CI license gate ([Quick CI/CD](./cicd-quick))                                | 5230 §3.3.2 License compliance                       | Build is blocked when forbidden licenses are found  |
| SBOM refresh on dependency change                                            | 5230 §3.3.1 · 18974 §4.3.1 SBOM                      | SBOM generated automatically with cdxgen/syft       |
| SCA and CVE scanning in CI ([AI Security Review](./ai-security-review))      | 18974 §4.3.2 Vulnerability identification & tracking | PRs blocked with npm audit, trivy, and grype        |
| Continuous post-deployment monitoring (Stage 5)                              | 18974 §4.3.2 Vulnerability response                  | New CVEs tracked with Dependabot and Renovate       |

:::note
The AI coding guide **automates the execution** of the items above, but the self-certification declaration and evidence deliverables are completed in the [Build Your System](/docs) track.
:::

## Next steps

- To build the standards system from scratch → [Build Your System guide](/docs)
- For organization-wide pipeline-level security enforcement → [DevSecOps guide](/devsecops/intro)
