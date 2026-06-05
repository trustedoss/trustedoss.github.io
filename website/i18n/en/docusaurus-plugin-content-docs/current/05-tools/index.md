---
date: 2026-06-05
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 5 minutes
sidebar_position: 0
sidebar_label: Tools overview
---

# Tools: SBOM and vulnerability management

This chapter covers the tools that automatically identify the open source included in your product (SBOM), manage it, and find and respond to vulnerabilities. It proceeds in the three-step flow below.

## The flow

1. **SBOM creation** — Create a bill of materials (SBOM) of which open source is included in your product. The tools are syft and cdxgen. Go to [SBOM creation](./sbom-generation/index.md).
2. **SBOM management** — Update and store the SBOM you created, and share it with your supply chain. Go to [SBOM management](./sbom-management/index.md).
3. **Vulnerability analysis and response** — Based on the SBOM, find and respond to known vulnerabilities (CVEs). The tools are grype and OSV. Go to [Vulnerability management](./vulnerability/index.md).

## Try it right away (no install, no API key)

Check SBOM analysis results right in your browser first, with no installation.

- [SBOM analyzer sample experience](pathname:///tools/sbom-sample-demo.html)

## Automatic generation with AI agents

The outputs of each step can be generated automatically with agents. For the full mapping, see [Create outputs with AI agents](../00-overview/agents.md).

- SBOM creation: `05-sbom-guide`, `05-sbom-analyst`
- SBOM management: `05-sbom-management`
- Vulnerability analysis: `05-vulnerability-analyst`

## Extend to automation

The SBOM creation and vulnerability scanning you learn here can be put into your CI pipeline for continuous automation. The [DevSecOps](/devsecops/intro) guide provides workflows you can copy and use.
