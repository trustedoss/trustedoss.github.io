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

This chapter covers the tools that automatically identify the open source in your product (SBOM), manage it, and find and respond to vulnerabilities. It follows the three-step flow below.

## The flow

1. **SBOM creation** — Create a bill of materials (SBOM) that captures which open source is included in your product. The tools are syft and cdxgen. Go to [SBOM creation](./sbom-generation/index.md).
2. **SBOM management** — Update and store the SBOM you created, and share it across your supply chain. Go to [SBOM management](./sbom-management/index.md).
3. **Vulnerability analysis and response** — Use the SBOM to find and respond to known vulnerabilities (CVEs). The tools are the OSV API and Dependency-Track. Go to [Vulnerability management](./vulnerability/index.md).
4. **AI SBOM (optional)** — Organizations working with AI systems extend the SBOM scope to models and datasets. The tool is BomLens. Go to [AI SBOM](./ai-sbom/index.md).

## Try it right away (no install, no API key)

See SBOM analysis results right in your browser first, with no installation.

- [SBOM analyzer sample experience](pathname:///tools/sbom-sample-demo.html)

## Automatic generation with AI agents

The outputs of each step can be generated automatically with AI agents. For the full mapping, see [Create outputs with AI agents](../00-overview/agents.md).

- SBOM creation: `05-sbom-guide`, `05-sbom-analyst`
- SBOM management: `05-sbom-management`
- Vulnerability analysis: `05-vulnerability-analyst`

## Extend to automation

The SBOM creation and vulnerability scanning you learn here can be wired into your CI pipeline for continuous automation. The [DevSecOps](/devsecops/intro) guide provides workflows you can copy and use.
