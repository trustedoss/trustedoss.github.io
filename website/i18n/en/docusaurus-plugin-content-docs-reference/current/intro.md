---
id: intro
title: Reference
slug: intro
description: 'Reference materials: deliverable best practices, canonical concept pages (license classification, vulnerability response deadlines), a glossary, and an agent selection guide.'
sidebar_position: 1
---

# Reference

This section collects the reference materials you need to build an open source management system.

## Deliverable Best Practices

Completed examples of the deliverables each stage's agent generates (based on a fictional company).
Compare them with the results in your own `output/` folder to spot missing items.
The per-stage list of deliverable files is canonical in the deliverables table of [Overview: the two standards and the whole journey](/en/docs).

| Stage         | Link                                                  |
| ------------- | ----------------------------------------------------- |
| Organization  | [Organization deliverables](./samples/organization)   |
| Policy        | [Policy deliverables](./samples/policy)               |
| Process       | [Process deliverables](./samples/process)             |
| SBOM          | [SBOM deliverables](./samples/sbom)                   |
| Vulnerability | [Vulnerability deliverables](./samples/vulnerability) |
| Training      | [Training deliverables](./samples/training)           |
| Conformance   | [Conformance deliverables](./samples/conformance)     |

## Concepts in Depth

Canonical concept pages linked from the main guide. The policy, process, and tools chapters treat these pages as the source of truth.

| Document                                                                      | Contents                                                                                  |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [License Classification](./concepts/license-classification)                   | Classification criteria, impact by distribution method, distribution channel allow matrix |
| [Vulnerability Response Deadlines and VEX](./concepts/vulnerability-response) | Response deadlines by CVSS severity (KWG baseline and organizational SLA), VEX            |
| [Glossary](./glossary)                                                        | Plain-language definitions of license, SBOM, security, and organization terms             |
| [Talks](./talks)                                                              | Where Trusted OSS has been presented, and the slides                                      |

## Agent Selection Guide

[Create deliverables with AI agents](./agents) covers which agent to use in which situation. The nine program-building agents map one-to-one to chapters and deliverables, and the seven automation agents write CI and developer-tool configuration or analyze scanner output.

## More on Tools and Regulations

| Topic                                   | Link                                                                                                                                                     |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SBOM generation tools in depth          | [SBOM Generation](/en/docs/tools/sbom-generation) (syft, cdxgen)                                                                                         |
| Vulnerability management tools in depth | [Vulnerability Analysis and Response](/en/docs/tools/vulnerability) (grype, OSV)                                                                         |
| KWG ecosystem tools                     | [KWG Open Source Guide — Tools](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/4-tool/) (FOSSLight, SW360, FOSSology) |
| Regulatory trends                       | [Software Supply Chain Security](/en/docs/overview/supply-chain) (EU CRA, EO 14028, Korean SBOM trends)                                                  |
| SKT Open Source Guide                   | [Link](https://sktelecom.github.io)                                                                                                                      |
