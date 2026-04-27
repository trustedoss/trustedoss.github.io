---
id: iso-mapping
title: 'ISO/IEC 18974 Linkage'
sidebar_label: 'ISO/IEC 18974 Linkage'
sidebar_position: 11
---

# ISO/IEC 5230 · 18974 Linkage

This page focuses on **ISO/IEC 18974 (Open Source Security Assurance)**.
You can check which of the standard requirements your implementation meets in this DevSecOps guide.
The license compliance standard ISO/IEC 5230 is outside the scope of this guide.

## What is ISO/IEC 18974?

:::info ISO/IEC 18974 is an international standard for open source security assurance
Hosted by OpenChain Project
Through self-certification
Anyone can authenticate for free.
:::

**Purpose**: Define the minimum core requirements to identify, track, and respond to known security vulnerabilities (CVE, etc.) in open source software. We focus on minimum standards so organizations of all sizes can adopt without burden.

**Organization**: Consists of four sections: Program establishment, definition of related tasks, compliance assurance, and data provision. Each requirement is numbered in the format 4.x.x.

**Authentication Method**: Complete and submit a self-certification checklist on the OpenChain official site. Since the organization declares itself without external audit, the procedure is simple and there is no cost.

---

## DevSecOps Implementation and requirements mapping

The table below shows how the DevSecOps pipeline implemented in this guide meets the key requirements of ISO/IEC 18974.

| Requirement Number | Requirements (Summary)                | Implementation method                                           | Related Pages                        |
| ------------------ | ------------------------------------- | --------------------------------------------------------------- | ------------------------------------ |
| 4.1.1              | Documenting Security Assurance Policy | DevSecOps Strategy/SLA Policy Document                          | [Introduction Strategy](./strategy)  |
| 4.1.2              | Policy awareness and education        | Guidance and documentation of pipeline failures within the team | [Pipeline Design](./pipeline-design) |
| 4.2.1              | Open source component identification  | syft SBOM auto-generated                                        | [SCA](./sca)                         |
| 4.2.2              | Check for known vulnerabilities       | grype CVE Scan/PR blocking                                      | [SCA](./sca)                         |
| 4.2.3              | vulnerability Response Procedure      | SLA definition/exception handling process                       | [SCA](./sca)                         |
| 4.3.1              | Compliance assurance activities       | Regular Scan·SBOM Artifact Storage                              | [Monitoring](./monitoring)           |
| 4.3.2              | Data Preservation                     | SBOM Permanent storage by release                               | [Monitoring](./monitoring)           |
| 4.4.1              | External Inquiry Response Procedure   | vulnerability Response SLA·VEX Document                         | [SCA](./sca)                         |

---

## Self-certification preparation checklist

:::tip Prepare a trace file that satisfies each item in advance
OpenChain Self-certification is a declaration method, but
You must be able to provide evidence when an audit is requested.
:::

1. **Security Policy Document**

- DevSecOps Introduction Strategy Document (based on strategy.md)
- SLA definition document by vulnerability severity
- Exception handling approval process document

2. **SBOM Accumulation**

- SBOM files automatically generated from CI/CD (kept by release version)
- SBOM Creation tool/format/cycle specification document

3. **vulnerability management evidence**

- grype scan result artifacts
- Exception handled CVE list and approval records (including .grype.yaml comments)
- vulnerability discovery → Modification history (GitHub Issues·PR)

4. **Continuous monitoring evidence**

- Regular scan workflow execution log
- Dependabot·Renovate PR history
- New CVE Notification → Response Timeline

---

## Certification registration process

1. **Self-Assessment**: Self-assess ISO/IEC 18974 items from the OpenChain official checklist and ensure that all requirements are met.
2. **Declaration**: After confirming that all requirements are met, declare that OpenChain has an eligible program. It is also recommended that this be stated in organizational policy documents.
3. **Registration**: Register the organization name in OpenChain Community of Conformance. Although optional, it helps improve supply chain reliability.

---

## Limitations and precautions

**DevSecOps Scope**: This guide's implementation of DevSecOps focuses on the open source security assurances of ISO/IEC 18974. Additional areas such as SAST, DAST, and IaC security are security enhancement activities that go beyond standard requirements and are optional improvements beyond the scope of certification.

**ISO/IEC 5230 Separate preparation required**: The license compliance standard, ISO/IEC 5230, is outside the scope of this guide. Please refer to Trusted OSS’s Enterprise Open Source Governance Guide.
