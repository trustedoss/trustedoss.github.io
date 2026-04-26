---
id: intro
title: DevSecOps
slug: intro
---

# DevSecOps

## What this guide covers

AI Covers how to enforce at the pipeline level that code produced by coding tools does not violate your organization's open source policies. This is a practical guide to building a company-wide DevSecOps system, including SBOM creation, vulnerability management, license governance, and continuous monitoring. It also explains how to link with the ISO/IEC 5230 (license compliance) and ISO/IEC 18974 (security assurance) standard requirements.

---

## AI Relationship to coding guide

:::info If you applied Quick CI/CD first, learn more here
The Quick CI/CD of the AI Coding Guide aims to help developers create a basic gate in 30 minutes. This DevSecOps guide covers enterprise policy design, multi-repository management, and audit response. The two guides can be used independently, but we recommend reading them in the following order: [AI Coding — 4-Step Strategy](/ai-coding/strategy) → [Quick CI/CD](/ai-coding/cicd-quick) → DevSecOps.
:::

---

## Structure of this menu

| Page                                            | Contents covered                                      | Recommended Readers  |
| ----------------------------------------------- | ----------------------------------------------------- | -------------------- |
| [Introduction Strategy](./strategy)             | Maturity model/step-by-step roadmap                   | Team Lead/Architect  |
| [SAST](./sast)                                  | Static analysis — CodeQL·Semgrep                      | Developer·DevOps     |
| [SCA](./sca)                                    | Dependency Analysis — syft·grype·SBOM                 | DevOps·Security Team |
| [Secret Detection](./secret-detection)          | Prevent key/token leakage — Gitleaks                  | Developer·DevOps     |
| [Container Security](./container-security)      | Image vulnerability — Trivy                           | DevOps·Security Team |
| [IaC Security](./iac-security)                  | Infrastructure Code Inspection — Checkov              | DevOps·SRE           |
| [DAST](./dast)                                  | Dynamic Analysis — OWASP ZAP·Nuclei                   | Security Team·QA     |
| [Pipeline Design](./pipeline-design)            | Full Integrated Design·GitHub Actions                 | DevOps Engineer      |
| [Monitoring·Automatic Correction](./monitoring) | Continuous scanning and automatic PR after deployment | DevOps·Security Team |
| [ISO standard linkage](./iso-mapping)           | ISO/IEC 18974 Requirements Mapping                    | Compliance Manager   |

---

## Where to start?

:::tip Starting point for each role

- DevSecOps is the first
  → From [Introduction Strategy](./strategy)
- I want to catch code quality and security vulnerabilities at the code stage.
  → From [SAST](./sast)
- I am concerned about open source dependency vulnerabilities.
  → From [SCA](./sca)
- API Key/Token has been exposed to code
  → From [Secret Detection](./secret-detection)
- Running a container environment
  → From [Container Security](./container-security)
- ISO/IEC 18974 Preparing for certification
  → From [ISO standard linkage](./iso-mapping)
  (However, we recommend reading the SCA page first)
  :::
