---
description: 'Start enterprise open source management in 5 minutes. See the results first with a no-install demo, then create your first deliverable with an AI agent.'
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

TrustedOSS uses AI agents to automatically generate company-tailored <Term k="openchain">OpenChain</Term> (ISO/IEC 5230 and 18974) enterprise open source management deliverables, helping you reach a <Term k="self-certification">Self-Certification</Term> declaration as fast as possible. Even if this is your first time taking on open source management, you can follow along step by step.

## When to use this

- When you are taking on enterprise open source management for the first time and are not sure where to start
- When you need to quickly create the deliverables required for self-certification, such as the policy, processes, and <Term k="sbom">SBOM</Term>
- When you want to automatically apply the policy you created to your CI pipeline and AI coding tools

## Try it now

### 1. See the results first (no install, no API key, 5 minutes)

Check SBOM analysis results right in your browser, with no installation.

- [Open the SBOM sample demo](pathname:///tools/sbom-sample-demo.html)

If you are curious about the actual form of the generated deliverables, also see the [Policy Deliverable Best Practices](/reference/samples/policy).

### 2. Create your own deliverables (AI agent, about 15 minutes)

The first deliverable you create is the definition of your organization's roles and responsibilities. The agent asks questions and generates documents tailored to your company.

If you have not cloned the repository yet, get it first. Skip this step if you have already completed [Environment preparation: install the tools needed for the labs](../01-setup/index.md).

```bash
git clone https://github.com/trustedoss/trustedoss-agents.git
cd trustedoss-agents
```

:::tip Check before running
If a Claude session is open, exit it first (`/exit` or `Ctrl+C`). Run the command below from the root of the `trustedoss-agents` repository you moved into above. (If you opened a new terminal, run `cd trustedoss-agents` first.)
:::

```bash
cd agents/02-organization-designer
claude
```

After the agent finishes, return to the repo root (`cd ../..`) and check the deliverables: `ls output/organization/` — three files mean success.

## Next steps

- To choose a path that fits your situation, see [The start path that fits you](./start-path.md).
- To see the full journey, go to [Overview: the two standards and the full journey](./index.md).
- To prepare your environment first, go to the [Environment preparation](../01-setup/index.md) chapter.
