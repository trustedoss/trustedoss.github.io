---
id: intro
title: Reference
slug: intro
description: 'Reference materials: deliverable best practices, canonical concept pages (license classification, vulnerability response deadlines), a glossary, and an agent selection guide.'
---

# Reference

This section collects the reference materials you need to build an open source management system.

## Deliverable Best Practices

Completed examples of the deliverables each stage's agent generates (based on a fictional company).
Compare them with the results in your own `output/` folder to spot missing items.

| Deliverable                                                                                                 | Agent                          | Link                                                  |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------ | ----------------------------------------------------- |
| Organization (role-definition, raci-matrix, appointment-template)                                           | organization-designer          | [Organization deliverables](./samples/organization)   |
| Policy (oss-policy, license-allowlist)                                                                      | policy-generator               | [Policy deliverables](./samples/policy)               |
| Process (usage-approval, distribution-checklist, vulnerability-response, inquiry-response, process-diagram) | process-designer               | [Process deliverables](./samples/process)             |
| SBOM (license-report, copyleft-risk, sbom-management-plan, sbom-sharing-template)                           | sbom-analyst / sbom-management | [SBOM deliverables](./samples/sbom)                   |
| Vulnerability (cve-report, remediation-plan)                                                                | vulnerability-analyst          | [Vulnerability deliverables](./samples/vulnerability) |
| Training (curriculum, completion-tracker, resources)                                                        | training-manager               | [Training deliverables](./samples/training)           |
| Conformance (gap-analysis, declaration-draft, submission-guide)                                             | conformance-preparer           | [Conformance deliverables](./samples/conformance)     |

## Concepts in Depth

Canonical concept pages linked from the main guide. The policy, process, and tools chapters treat these pages as the source of truth.

| Document                                                                      | Contents                                                                                  |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [License Classification](./concepts/license-classification)                   | Classification criteria, impact by distribution method, distribution channel allow matrix |
| [Vulnerability Response Deadlines and VEX](./concepts/vulnerability-response) | Response deadlines by CVSS severity (KWG baseline and organizational SLA), VEX            |
| [Glossary](./glossary)                                                        | Plain-language definitions of license, SBOM, security, and organization terms             |

## Agent Selection Guide

Which agent to use in which situation, and how agents map to chapters and deliverables, is covered in [Creating Deliverables with AI Agents](/docs/overview/agents).

## More on Tools and Regulations

| Topic                                   | Link                                                                                                                                                     |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SBOM generation tools in depth          | [SBOM Generation](/docs/tools/sbom-generation) (syft, cdxgen)                                                                                            |
| Vulnerability management tools in depth | [Vulnerability Analysis and Response](/docs/tools/vulnerability) (grype, OSV)                                                                            |
| KWG ecosystem tools                     | [KWG Open Source Guide — Tools](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/4-tool/) (FOSSLight, SW360, FOSSology) |
| Regulatory trends                       | [Software Supply Chain Security](/docs/overview/supply-chain) (EU CRA, EO 14028, Korean SBOM trends)                                                     |
| SKT Open Source Guide                   | [Link](https://sktelecom.github.io)                                                                                                                      |
