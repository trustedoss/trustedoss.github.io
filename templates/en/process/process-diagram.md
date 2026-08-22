# Open Source Process Flow Diagram

<!-- 5230 §3.1.5.1, §3.3.2.1 · 18974 §4.1.5.1 -->

**Company name**: {company name}
**Date written**: YYYY-MM-DD
**Owner**: {Open Source Program Manager name}

> This document visualizes, as Mermaid flowcharts, the procedures already defined in prose in
> `usage-approval.md`, `distribution-checklist.md`, and `vulnerability-response.md`. For the
> rationale and exception handling behind each procedure, follow those documents; use this one as
> a quick-reference overview of the overall flow.

---

## 1. Open source usage approval flow

<!-- Must match the procedure in usage-approval.md -->

```mermaid
graph TD
    A[Open source usage request] --> B{On the allowed license list?}
    B -->|Yes| C[Vulnerability scan: no Critical/High findings]
    B -->|No| D[Legal review]
    D -->|Approved| C
    D -->|Rejected| E[Review alternative components]
    C -->|Clear| F[Owner approval]
    C -->|Critical/High found| G[Check for a patch or review an alternative]
    F --> H[Update the SBOM]
```

## 2. Pre-distribution checklist flow

<!-- Must match the procedure in distribution-checklist.md -->

```mermaid
graph TD
    A[Prepare for distribution] --> B[Confirm the SBOM is current]
    B --> C[Generate and verify notices]
    C --> D[Confirm copyleft obligations are fulfilled]
    D --> E[Final approval]
    E --> F[Distribute]
    F --> G[Post-distribution final check]
```

## 3. Vulnerability response flow

<!-- Must match the procedure in vulnerability-response.md -->

```mermaid
graph TD
    A[CVE detected] --> B{Classify severity}
    B -->|Critical| C[Address within 1 week]
    B -->|High| D[Address within 4 weeks]
    B -->|Medium| E[Address within 1 month]
    B -->|Low| F[Include in the next release]
    C --> G[Patch or apply a mitigation]
    D --> G
    E --> G
    F --> G
    G --> H[Record in remediation-plan.md]
```

---

## 4. Notes

- For the detailed conditions and exception handling of each flow, follow the corresponding process document referenced in §1.
- When a process changes, update this document together with the corresponding process document.
