---
date: 2026-06-05
version: '1.0'
checklist:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
self_study_time: 5 minutes
sidebar_position: 1
sidebar_label: 5-minute quick start
---

# 5-minute quick start

TrustedOSS uses AI agents to automatically generate company-tailored OpenChain 2026 (ISO/IEC 5230 and 18974) enterprise open source management outputs, helping you reach a self-certification declaration as fast as possible. Even if this is your first time taking on open source management, you can follow along step by step.

## When to use this

- When you are taking on enterprise open source management for the first time and are not sure where to start
- When you need to quickly create outputs required for self-certification, such as policy, process, and SBOM
- When you want to automatically apply the policy you created to your CI pipeline and AI coding tools

## Try it now

### 1. See the results first (no install, no API key)

Check SBOM analysis results right in your browser, with no installation.

- [Open the SBOM sample experience](pathname:///tools/sbom-sample-demo.html)

If you are curious about the actual form of the generated outputs, also see [Policy Output Best Practices](/reference/samples/policy).

### 2. Create your own outputs (AI agent)

The first output you create is the definition of your organization's roles and responsibilities. The agent asks questions and generates documents tailored to your company.

:::tip Check before running
First terminate the current Claude session (`/exit` or `Ctrl+C`), then run the command below in a new terminal.
:::

```bash
cd agents/02-organization-designer
claude
```

## Next steps

- To choose a path that fits your situation, see [The start path that fits you](./start-path.md).
- To see the full journey, go to [Overview: the two standards and the full journey](./index.md).
- To prepare your environment first, go to the [Environment preparation](../01-setup/index.md) chapter.
