---
id: glossary
title: Glossary
sidebar_label: Glossary
sidebar_position: 2
---

# Glossary

If you are new to open source management, many of these abbreviations will be unfamiliar. This page collects plain-language definitions of the technical terms used throughout the guide. The parenthetical explanations given when an abbreviation first appears in a document are also based on this table.

## Licenses

| Term                        | Plain-language definition                                                                               |
| --------------------------- | ------------------------------------------------------------------------------------------------------- |
| Permissive                  | Permissive license — loose redistribution conditions (MIT, Apache, BSD). An attribution notice suffices |
| Copyleft                    | Copyleft — requires derivative works to be released under the same license (GPL, etc.)                  |
| Weak Copyleft               | Weak copyleft — only modified files must be disclosed (LGPL, MPL)                                       |
| Strong Copyleft             | Strong copyleft — distributing a combined work triggers a full disclosure obligation (GPL)              |
| Network Copyleft            | Network copyleft — disclosure obligation even when only serving over a network as SaaS (AGPL)           |
| Attribution Notice (NOTICE) | The file included at distribution that lists open source copyrights and license notices                 |

## SBOM · Standards

| Term               | Plain-language definition                                                                                           |
| ------------------ | ------------------------------------------------------------------------------------------------------------------- |
| SBOM               | Software Bill of Materials — a list of every component that goes into a piece of software                           |
| CycloneDX          | One of the standard SBOM formats (OWASP)                                                                            |
| SPDX               | A standard format for SBOMs and licenses (Linux Foundation)                                                         |
| PURL               | Package URL — a standard notation that uniquely identifies a package                                                |
| NTIA               | U.S. National Telecommunications and Information Administration — the agency that defined the SBOM minimum elements |
| OpenChain          | The international standards project for open source compliance (ISO/IEC 5230, 18974)                                |
| KWG                | The OpenChain Korea Work Group                                                                                      |
| ISO/IEC 5230       | The OpenChain international standard for license compliance                                                         |
| ISO/IEC 18974      | The OpenChain international standard for security assurance (vulnerability management)                              |
| Self-Certification | Declaring on your own that you meet the OpenChain requirements, without an external audit                           |

## Security · Vulnerabilities

| Term | Plain-language definition                                                                                   |
| ---- | ----------------------------------------------------------------------------------------------------------- |
| SCA  | Software Composition Analysis — checking open source components for vulnerabilities and licenses            |
| SAST | Static Application Security Testing — analyzing source code without executing it                            |
| DAST | Dynamic Application Security Testing — analyzing a running application                                      |
| CVE  | Common Vulnerabilities and Exposures — the unique identifier assigned to a known vulnerability              |
| CVSS | Common Vulnerability Scoring System — expresses risk on a scale of 0 to 10                                  |
| EPSS | Exploit Prediction Scoring System — estimates the probability a vulnerability is used in real attacks       |
| KEV  | Known Exploited Vulnerabilities — a catalog of vulnerabilities confirmed to be exploited in the wild        |
| VEX  | Vulnerability Exploitability eXchange — states whether a vulnerability actually affects your product        |
| CVD  | Coordinated Vulnerability Disclosure — the process for responsibly receiving and disclosing vulnerabilities |

## Organization · Roles

| Term        | Plain-language definition                                                                                               |
| ----------- | ----------------------------------------------------------------------------------------------------------------------- |
| RACI        | Responsibility assignment matrix — divides roles into Responsible (R), Accountable (A), Consulted (C), and Informed (I) |
| OSPO / OSPM | Open Source Program Office / Open Source Program Manager                                                                |

## Tools

| Tool     | Plain-language definition                                                                                           |
| -------- | ------------------------------------------------------------------------------------------------------------------- |
| Syft     | SBOM generation tool                                                                                                |
| cdxgen   | CycloneDX SBOM generation tool (precise per-language analysis)                                                      |
| Grype    | Vulnerability scanning tool                                                                                         |
| OSV      | Open source vulnerability lookup API and database                                                                   |
| Trivy    | Integrated vulnerability and SBOM scanning tool                                                                     |
| Gitleaks | Secret (private key, token) detection tool                                                                          |
| Checkov  | IaC (Infrastructure as Code) security scanning tool                                                                 |
| onot     | Automatically generates OSS attribution notices from SPDX documents (Kakao and SK Telecom)                          |
| BomLens  | SK Telecom's local-first integrated SBOM generation and risk assessment tool (source, containers, firmware, ML-BOM) |

<!-- Maintenance rule: if a new term not in this table is needed, add it to the STYLEGUIDE.md abbreviation table first, then sync this page. -->
