# Open Source License Allowlist

**Company name**: {company name}
**Distribution method**: {distribution method}
**Date written**: YYYY-MM-DD
**Owner**: {Open Source Program Manager}

Review and update this list regularly. A license that is not on the list can be used after the Program Manager reviews it.

---

## 1. Allowed licenses (Permissive)

Licenses with minimal obligations. Usable without separate approval.

| License                    | SPDX identifier | Main obligations                                          | Notes                 |
| -------------------------- | --------------- | --------------------------------------------------------- | --------------------- |
| MIT License                | MIT             | Copyright notice, include the license                     | The most widely used  |
| Apache License 2.0         | Apache-2.0      | Copyright notice, include the NOTICE file                 | Includes patent terms |
| BSD 2-Clause               | BSD-2-Clause    | Copyright notice, include the license                     |                       |
| BSD 3-Clause               | BSD-3-Clause    | Copyright notice, include the license, no use of the name |                       |
| ISC License                | ISC             | Copyright notice, include the license                     |                       |
| Boost Software License 1.0 | BSL-1.0         | Include the license when distributing source code         |                       |
| The Unlicense              | Unlicense       | None                                                      | Public domain         |

---

## 2. Conditionally allowed licenses (Weak Copyleft)

Licenses whose obligations depend on the scope of the derivative work. Use after review by the Program Manager.

| License                                     | SPDX identifier | Main obligations                                   | Applies to {distribution method} |
| ------------------------------------------- | --------------- | -------------------------------------------------- | -------------------------------- |
| GNU Lesser GPL v2.1                         | LGPL-2.1        | Publish source when the library itself is modified | {condition}                      |
| GNU Lesser GPL v3.0                         | LGPL-3.0        | Publish source when the library itself is modified | {condition}                      |
| Mozilla Public License 2.0                  | MPL-2.0         | Publish the source of modified files               | {condition}                      |
| Eclipse Public License 2.0                  | EPL-2.0         | Publish the source of modified files               | {condition}                      |
| Common Development and Distribution License | CDDL-1.0        | Publish the source of modified files               | {condition}                      |

---

## 3. Restricted licenses (Strong Copyleft)

<!-- Adjust the content below according to {distribution method} -->

Licenses that require the same license to apply to the whole derivative work. Legal review is mandatory.

| License       | SPDX identifier | Main obligations                                      | Applies to {distribution method} |
| ------------- | --------------- | ----------------------------------------------------- | -------------------------------- |
| GNU GPL v2.0  | GPL-2.0         | Obligation to publish the full source code            | {condition}                      |
| GNU GPL v3.0  | GPL-3.0         | Obligation to publish the full source code            | {condition}                      |
| GNU AGPL v3.0 | AGPL-3.0        | Publish source even when offered as a network service | {condition}                      |

---

## 4. Licenses that are not allowed

The licenses below cannot be used without separate legal approval:

- Creative Commons (including NC): CC-BY-NC-_, CC-BY-SA-_ — restrict commercial use or impose strong copyleft
- Server Side Public License (SSPL): requires the source of the whole service to be published
- Business Source License (BUSL): includes conditions that restrict commercial use
- Other custom licenses: prior review by the legal team is mandatory

---

## 5. License review request procedure

When a license that is not on the list is needed:

1. Create a license review request ticket in GitHub Issues
2. The OSPM reviews it and consults the legal team where necessary
3. Reflect the approval result in this document and commit it

---

## 6. License taxonomy: when copyleft is triggered

Even among "copyleft" licenses, _when_ the obligation to publish source arises differs. The two variables that matter are **whether you distribute** and **how you combine the code**.

| Type             | Representative | When the obligation triggers                         | Practical point                                                                     |
| ---------------- | -------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Permissive       | MIT, Apache    | (effectively never)                                  | A copyright and license notice is enough                                            |
| Weak Copyleft    | LGPL, MPL      | When you modify the library itself and distribute it | If you only link without modifying, your own code stays closed                      |
| Strong Copyleft  | GPL            | When you **distribute** the combined result          | Linking and distributing means publishing everything. Pure SaaS does not trigger it |
| Network Copyleft | AGPL           | Even when you only **serve** it over a network       | SaaS also has to publish source, which SaaS companies must watch most closely       |

Two things matter most:

- **If you do not distribute (pure SaaS), GPL obligations usually do not trigger.** AGPL is the exception, because it treats network use like distribution.
- **For LGPL the test is whether you modified the library.** If you link it unmodified, you do not have to open your own source.

When the judgement is unclear, request a legal review through the §5 procedure.

---

## 7. Approved exceptions

Record exceptions approved through the §5 review here. An exception is not permanent and is reviewed again on its expiry date.

| Component and license  | Reason for approval | Conditions and scope | Approved by | Approval date | Expiry / re-review date |
| ---------------------- | ------------------- | -------------------- | ----------- | ------------- | ----------------------- |
| {e.g. lib-x / GPL-3.0} | {no alternative}    | {internal use only}  | {approver}  | YYYY-MM-DD    | YYYY-MM-DD              |

- An exception past its expiry date is treated as void until it is reviewed again.
- Registering and renewing exceptions follows the policy §11 procedure (policy change requests and operation).

---

## Change history

| Date       | Change        | Owner   |
| ---------- | ------------- | ------- |
| YYYY-MM-DD | Initial entry | {owner} |
