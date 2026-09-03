---
id: license-classification
title: License Classification
sidebar_label: License Classification
sidebar_position: 1
---

# License Classification

> This page is the **canonical reference** for open source license classification. When the policy, process, or SBOM chapters cover license classification, they use this table as the baseline and link here.

Open source licenses fall into four broad categories by the strength of their obligations. Because the application criteria for each category depend on your company's distribution method, understand them before writing a policy.

## Classification Table

| Category         | Representative licenses | Core obligation                                       | Distribution caution                                         |
| ---------------- | ----------------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| Permissive       | MIT, Apache-2.0, BSD    | Copyright and license notice                          | Safe in almost every distribution method                     |
| Weak Copyleft    | LGPL, MPL               | Disclose source only for modified files and libraries | Mostly safe with dynamic linking                             |
| Strong Copyleft  | GPL-2.0, GPL-3.0        | Disclose the full source of derivative works          | No obligation for SaaS; arises on binary distribution        |
| Network Copyleft | AGPL-3.0                | Disclose source even for network provision (SaaS)     | Obligation arises even for SaaS — review required before use |

:::info[Key insight]
For the same code, whether an obligation arises depends on the **distribution method**. In particular, GPL does not treat server execution (SaaS) as "distribution," so no obligation arises, whereas AGPL imposes an obligation even for network provision.
:::

## CC-BY-SA: Using a Content License for Software

CC-BY-SA (Creative Commons Attribution-ShareAlike) is handled separately rather than placed in the four categories above. It was built for content such as text, images, and video, and Creative Commons itself recommends using a dedicated software license instead of a CC license for software. **Its category is conditionally allowed**, and applying it to code requires review by the program manager plus legal confirmation.

The problem is not a commercial-use restriction. Unlike CC-BY-NC, CC-BY-SA does not restrict commercial use. The real problem is that how far the ShareAlike clause propagates is undefined for software.

- **The boundary of a derivative work is unclear.** ShareAlike requires an adaptation of the original work to carry the same license. But the license does not define which of linking, bundling, or embedding counts as an adaptation in software, in contrast to the GPL family, which spells out the scope of a derivative work.
- **There is no notion of source code.** The GPL requires source to be provided in "the preferred form for making modifications," while CC licenses have no such provision. Even if you decide an obligation applies, there is no defined way to satisfy it.
- **There is no patent clause.** CC-BY-SA 4.0 states explicitly that it grants no patent rights. For a project that needs an explicit patent grant such as the one in Apache-2.0, that gap is a risk.

One path is defined. Creative Commons declared CC BY-SA 4.0 one-way compatible with GPL-3.0. You can bring CC BY-SA 4.0 material into a GPL-3.0 project, but not the reverse.

In practice the rule is to keep it out of code. You will still meet CC-BY-SA often in content assets bundled with software such as fonts, icons, documentation, and training data. In those cases the program manager confirms whether the asset ships with the distribution and how the attribution obligation is satisfied.

This is also why CC-BY-SA is the only row in the matrix below whose SaaS column is conditional. The GPL text itself supports the judgment that server execution is not distribution; CC-BY-SA offers no such basis for the judgment.

## Impact by Distribution Method

Distribution method is the key factor that determines whether a license obligation arises.

- **SaaS (server-provided)**: Running GPL code on a server does not count as "distribution," so GPL obligations do not arise. However, AGPL-3.0 imposes a source-disclosure obligation even when providing a service over a network, so caution is required.
- **App store distribution (mobile/desktop)**: Because the software is distributed to users as a binary, copyleft obligations arise. Including a GPL component may create a full source-disclosure obligation.
- **Embedded (firmware/hardware)**: The strictest case. Binary distribution triggers GPL obligations, and because software embedded in hardware is hard to modify and reinstall, GPL compliance is more demanding.

## Distribution Channel × License Allow Matrix

A matrix to consult when deciding which categories to allow per channel. The actual allow list for your company policy is generated by the `policy-generator` agent to match your distribution method.

| License    | Category         | Internal use | SaaS distribution | App distribution | Embedded       |
| ---------- | ---------------- | ------------ | ----------------- | ---------------- | -------------- |
| MIT        | Permissive       | ✅ Allowed   | ✅ Allowed        | ✅ Allowed       | ✅ Allowed     |
| Apache-2.0 | Permissive       | ✅ Allowed   | ✅ Allowed        | ✅ Allowed       | ✅ Allowed     |
| LGPL-2.1   | Weak Copyleft    | ✅ Allowed   | ✅ Allowed        | ⚠️ Conditional   | ⚠️ Conditional |
| GPL-2.0    | Strong Copyleft  | ✅ Allowed   | ✅ Allowed        | ❌ Prohibited    | ❌ Prohibited  |
| AGPL-3.0   | Network Copyleft | ✅ Allowed   | ❌ Prohibited     | ❌ Prohibited    | ❌ Prohibited  |
| CC-BY-SA   | Content license  | ✅ Allowed   | ⚠️ Conditional    | ⚠️ Conditional   | ⚠️ Conditional |

The symbols follow the same three-level notation as the [Policy Deliverable Best Practices](/en/reference/samples/policy).

| Symbol         | Meaning                                                                                   |
| -------------- | ----------------------------------------------------------------------------------------- |
| ✅ Allowed     | Usable without separate approval                                                          |
| ⚠️ Conditional | Usable after prior review and approval by the open source Program Manager                 |
| ❌ Prohibited  | Prohibited in principle (exceptions require review by the Program Manager and legal team) |

:::info
This classification is foundational knowledge for ISO/IEC 5230 3.1.4 (program scope definition), 3.1.5 (identifying and reviewing license obligations), and 3.3.2 (handling license use cases).
:::

## Related Documents

- [Open Source Policy chapter guide](/en/docs/policy) — turn this classification into an allow list tailored to your company's distribution method
- [Policy Deliverable Best Practices](/en/reference/samples/policy) — a completed example reflecting per-channel allow principles
- [Glossary](/en/reference/glossary) — definitions of Copyleft, Permissive, and other terms
