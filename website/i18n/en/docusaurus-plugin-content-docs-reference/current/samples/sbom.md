---
sidebar_label: SBOM Output
sidebar_position: 4
---

# SBOM Output Best Practice

These are examples of the SBOM-related deliverables generated in the [05 Tools chapter](/docs/tools/sbom-generation).
They show actual output produced from the sample project (`java-vulnerable`, which includes Log4Shell CVE-2021-44228).

:::tip Download the Sample SBOM
We provide a sample SBOM (CycloneDX format, containing a GPL-2.0 copyleft component plus a vulnerable version) so you can try the analysis yourself. Download it and feed it into the [SCA analyzer](/devsecops/sca) or a local tool such as grype.

<a href="/samples/fixture-sample.cdx.json" download>Download fixture-sample.cdx.json</a>

Each code block below can be copied as-is with the copy button in its top-right corner.
:::

---

**Deliverables on this page**

- SBOM License Analysis Report
- Copyleft Risk Report
- SBOM Management Plan
- SBOM Submission Cover Letter (template for customer delivery)

## SBOM License Analysis Report

:::info
**Generating agent**: `05-sbom-analyst` | **Save path**: `output/sbom/license-report.md`
:::

---

Report type: SBOM License Analysis
Created: 2026-03-23 07:11
Target project: vulnerable-java-app
Tool used: syft 1.42.3

---

### 1. Summary

- Analyzed SBOM: `java-vulnerable.cdx.json` (CycloneDX 1.6)
- **3** software components in total (excluding file entries)
- License fields in the SBOM are empty → licenses were supplemented and classified from external sources
- Apache Log4j 2.14.1 is classified as **Apache 2.0 (Permissive)**
- The internal application (`vulnerable-java-app`) has no license information → **Unknown**
- **0** copyleft components (no immediate compliance action required)
- ⚠️ License information is missing from the SBOM; re-running the tool or supplementing manually is recommended

### 2. License Details per Component

| Component           | Version | Group                    | License    | Category   | Source                       |
| ------------------- | ------- | ------------------------ | ---------- | ---------- | ---------------------------- |
| log4j-api           | 2.14.1  | org.apache.logging.log4j | Apache-2.0 | Permissive | Maven Central (supplemented) |
| log4j-core          | 2.14.1  | org.apache.logging.log4j | Apache-2.0 | Permissive | Maven Central (supplemented) |
| vulnerable-java-app | 1.0.0   | com.example              | Unknown    | Unknown    | Not stated in SBOM           |

:::info[Note]
No license information was included when the SBOM was generated. When re-running syft, check the `--source-name` option and whether Maven Central metadata is enabled, or use the `cdxgen` tool in parallel to supplement the license fields.
:::

### 3. License Classification Summary

| Category        | Component count | Components            |
| --------------- | --------------- | --------------------- |
| Permissive      | 2               | log4j-api, log4j-core |
| Weak Copyleft   | 0               | —                     |
| Strong Copyleft | 0               | —                     |
| Unknown         | 1               | vulnerable-java-app   |

### 4. Actions

#### Info — Supplement SBOM license information

- **Target:** All components (especially `vulnerable-java-app`)
- **Action:** Enable license metadata when re-running syft or cdxgen

  ```bash
  # syft: include Maven POM license info
  syft /path/to/project --output cyclonedx-json

  # cdxgen: auto-collect license information
  cdxgen -t java /path/to/project -o sbom.cdx.json
  ```

- **Estimated time:** 30 minutes

#### Info — Declare the internal application license

- **Target:** `vulnerable-java-app@1.0.0`
- **Action:** Declare an internal license or Proprietary in the `<licenses>` section of `pom.xml`
  ```xml
  <licenses>
    <license>
      <name>Proprietary</name>
      <url>https://example.com/license</url>
    </license>
  </licenses>
  ```
- **Estimated time:** 15 minutes

### 5. Compliance Obligation Summary

| License             | Obligations                                                                         |
| ------------------- | ----------------------------------------------------------------------------------- |
| Apache-2.0          | Retain copyright notices, include the NOTICE file, distribute a copy of the license |
| Permissive (common) | Include the original license text when redistributing                               |

> Apache-2.0 has no source code disclosure obligation, making it friendly to binary distribution.
> Verify that your distribution package includes the `LICENSE` and `NOTICE` files.

---

_This report was generated to satisfy ISO/IEC 5230 §3.1.5 (identifying and reviewing license obligations), §3.3.2 (handling license use cases), and §3.4.1 (compliance deliverables)._

---

## Copyleft Risk Report

:::info
**Generating agent**: `05-sbom-analyst` | **Save path**: `output/sbom/copyleft-risk.md`
:::

---

Report type: Copyleft Risk Analysis
Created: 2026-03-23 07:11
Target project: vulnerable-java-app
Tool used: syft 1.42.3

---

### 1. Summary

- Analysis target: `java-vulnerable.cdx.json` (CycloneDX 1.6, 3 components)
- **Strong Copyleft (GPL/AGPL) components: 0**
- **Weak Copyleft (LGPL/MPL) components: 0**
- Both identified components are **Apache-2.0 (Permissive)**, so there is no copyleft risk
- 1 component has an **Unknown** license — needs separate confirmation
- ⚠️ Missing license metadata in the SBOM means potential unidentified copyleft risk may exist

### 2. Copyleft Risk Component List

| Component           | Version | License    | Copyleft grade | Risk      | Action                        |
| ------------------- | ------- | ---------- | -------------- | --------- | ----------------------------- |
| log4j-api           | 2.14.1  | Apache-2.0 | None           | 🟢 Low    | Not needed                    |
| log4j-core          | 2.14.1  | Apache-2.0 | None           | 🟢 Low    | Not needed                    |
| vulnerable-java-app | 1.0.0   | Unknown    | Unconfirmed    | 🟡 Medium | License verification required |

### 3. Copyleft Grade Criteria

| Grade           | Licenses                    | Obligations upon distribution                               |
| --------------- | --------------------------- | ----------------------------------------------------------- |
| Strong Copyleft | GPL-2.0, GPL-3.0, AGPL-3.0  | Obligation to disclose the full source code                 |
| Weak Copyleft   | LGPL-2.1, LGPL-3.0, MPL-2.0 | Disclose the source code of modifications to that component |
| Permissive      | Apache-2.0, MIT, BSD        | Retain copyright notices only                               |
| Unknown         | —                           | Treat conservatively as copyleft until confirmed            |

### 4. Risk Assessment

#### Based on the current distribution model

| Distribution model                | Copyleft risk                           |
| --------------------------------- | --------------------------------------- |
| Closed-source binary distribution | 🟢 No risk (when using Apache-2.0 only) |
| SaaS / network service            | 🟢 No risk (no AGPL components)         |
| Open source redistribution        | 🟢 No risk (no Strong Copyleft)         |

> **Conclusion:** All currently identified open source components (log4j-api, log4j-core) are Apache-2.0,
> so no source code disclosure obligation arises under any distribution model.

### 5. Actions

#### Medium — Confirm the Unknown-licensed component

- **Target:** `vulnerable-java-app@1.0.0` (internally developed application)
- **Risk:** Compliance status is unclear if distributed externally without a declared license
- **Action:** Declare license information in `pom.xml` or document the internal IP policy
- **Estimated time:** 15 minutes

#### Info — Supplement SBOM license information

- **Target:** All components
- **Risk:** With empty license fields, copyleft could be missed when new dependencies are added
- **Action:** Enable license metadata in the SBOM generation tool and regenerate
- **Estimated time:** 30 minutes

### 6. Ongoing Monitoring Recommendations

- Regenerate the SBOM and update this report whenever new dependencies are added
- Legal team review is mandatory before introducing GPL/AGPL components
- Establish a quarterly SBOM license status review schedule

---

_This report was generated to satisfy ISO/IEC 5230 §3.1.5 (identifying and reviewing license obligations) and §3.3.2 (handling license use cases)._

---

## SBOM Management Plan

:::info
**Generating agent**: `05-sbom-management` | **Save path**: `output/sbom/sbom-management-plan.md`
:::

---

### Overview

This document defines the SBOM management and maintenance plan to satisfy ISO/IEC 18974 requirements 4.3.1 and 4.3.2.

| Item                | Content                                                          |
| ------------------- | ---------------------------------------------------------------- |
| Provided externally | Yes (provided on customer/recipient request)                     |
| Supported formats   | CycloneDX, SPDX (provided selectively per recipient requirement) |
| Update cycle        | On feature completion, as needed (per release)                   |

---

### 1. SBOM Generation Principles

#### 1.1 When to generate

- Generate an SBOM at every release build after feature development is complete
- Regenerate immediately when dependencies change (addition/removal/version update)
- Confirm the SBOM is up to date during regular security checks (once a month)

#### 1.2 Generation tools

| Build environment | Tool                          | Output format    |
| ----------------- | ----------------------------- | ---------------- |
| Java/Maven        | `cyclonedx-maven-plugin`      | CycloneDX JSON   |
| Java/Gradle       | `cyclonedx-gradle-plugin`     | CycloneDX JSON   |
| Node.js           | `@cyclonedx/cyclonedx-npm`    | CycloneDX JSON   |
| Python            | `cyclonedx-bom`               | CycloneDX JSON   |
| Format conversion | `cyclonedx-cli`, `spdx-tools` | CycloneDX ↔ SPDX |

#### 1.3 Format conversion

If the recipient requires SPDX, perform a CycloneDX → SPDX conversion.

```bash
# CycloneDX → SPDX conversion (using cyclonedx-cli)
cyclonedx convert --input-file sbom.cdx.json \
  --output-file sbom.spdx.json --output-format spdxjson
```

cdxgen is an SBOM generation tool and has no format conversion capability, so use cyclonedx-cli
(`docker run --rm -v $(pwd):/data cyclonedx/cyclonedx-cli convert ...`) or the tool designated by the recipient for conversion.

---

### 2. SBOM Update Procedure

#### 2.1 Per-release update (main procedure)

```
1. Complete feature development and freeze the code
2. Finalize the dependency list (package.json / pom.xml / requirements.txt, etc.)
3. Generate the SBOM automatically (integrated into the CI/CD pipeline)
4. Review licenses (check whether any new copyleft is included)
5. Scan for vulnerabilities (OSV-Scanner / Grype)
6. Tag the SBOM file version and store it
7. If submission to a recipient is required, attach sbom-sharing-template.md and deliver
```

#### 2.2 Emergency update (when a security vulnerability occurs)

When a Critical/High CVE occurs, update immediately regardless of the release cycle:

1. Patch or replace the vulnerable component
2. Regenerate the SBOM
3. Resubmit the updated SBOM to the recipient (if needed)

---

### 3. CI/CD Integration and Automation

#### 3.1 Pipeline configuration (example: GitHub Actions)

```yaml
# .github/workflows/sbom.yml
name: Generate SBOM

on:
  push:
    branches: [main, release/*]
  workflow_dispatch:

jobs:
  generate-sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: Generate SBOM (CycloneDX)
        run: |
          # Replace with the command for your project's build environment
          npx @cyclonedx/cyclonedx-npm --output-file sbom.cdx.json

      - name: Vulnerability scan
        run: |
          curl -sSfL https://get.anchore.io/grype | sh -s -- -b /usr/local/bin
          grype sbom:sbom.cdx.json

      - name: Store SBOM
        uses: actions/upload-artifact@v7
        with:
          name: sbom-${{ github.sha }}
          path: sbom.cdx.json
```

#### 3.2 Local storage path rules

```
output/sbom/
├── {project-name}-{version}.cdx.json    # CycloneDX format
├── {project-name}-{version}.spdx.json   # SPDX format (when converted)
├── sbom-management-plan.md
└── sbom-sharing-template.md
```

---

### 4. Supply Chain Monitoring (ISO/IEC 18974 4.3.2)

#### 4.1 Regular monitoring items

| Item                       | Cycle                         | Tool                   |
| -------------------------- | ----------------------------- | ---------------------- |
| New CVE scan               | Once a month (or per release) | OSV-Scanner, Grype     |
| License change detection   | Per release                   | ort, scancode-toolkit  |
| Dependency update tracking | Continuous                    | Dependabot, Renovate   |
| SBOM validation            | Per release                   | cyclonedx-cli validate |

#### 4.2 Monitoring automation setup

```bash
# Enable GitHub Dependabot (.github/dependabot.yml)
version: 2
updates:
  - package-ecosystem: "npm"   # or maven, pip, etc.
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

#### 4.3 Vulnerability response criteria

| Severity | Response deadline               | Action                                   |
| -------- | ------------------------------- | ---------------------------------------- |
| Critical | Immediately (within 24 hours)   | Apply a patch or a replacement component |
| High     | Within 7 days                   | Establish and apply a patch plan         |
| Medium   | Within 30 days                  | Include in the next release              |
| Low      | Within 90 days or next planning | Review whether to accept the risk        |

---

### 5. Owners and Contacts

| Role             | Responsibilities                                  |
| ---------------- | ------------------------------------------------- |
| SBOM manager     | Overall SBOM generation, update, and distribution |
| Security officer | Review and respond to vulnerability scan results  |
| Legal/Compliance | License review and coordination with recipients   |

> For contact details, see the `output/organization/` deliverables

---

### 6. Governing Standards

| Standard      | Requirement                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------- |
| ISO/IEC 18974 | 4.3.1 — Continuously record the lifecycle of open source components (SBOM management and maintenance) |
| ISO/IEC 18974 | 4.3.2 — Continuously monitor supply chain vulnerabilities                                             |

---

## SBOM Submission Cover Letter (template for customer delivery)

:::info
**Generating agent**: `05-sbom-management` | **Save path**: `output/sbom/sbom-sharing-template.md`
:::

---

> **How to use**: Deliver this document to the recipient/customer along with the SBOM file.
> Fill in the `[ ]` items with actual information before submitting.

---

To: [ Recipient/Customer name ]
From: [ Your company name ]
Document title: SBOM (Software Bill of Materials) Submission Notice
Date: [ YYYY-MM-DD ]

---

### 1. Submitted File Information

| Item         | Content                                |
| ------------ | -------------------------------------- |
| Product name | [ Product or software name ]           |
| Version      | [ v0.0.0 ]                             |
| Build date   | [ YYYY-MM-DD HH:MM ]                   |
| SBOM format  | [ CycloneDX 1.6 JSON / SPDX 2.3 JSON ] |
| File name    | [ e.g., myproduct-v1.0.0.cdx.json ]    |
| SHA-256 hash | [ file hash value ]                    |

---

### 2. SBOM Format Details

#### When submitting in CycloneDX format

- Standard: CycloneDX Specification 1.6
- Encoding: JSON
- Generation tool: [ tool name and version used ]
- Validation: `cyclonedx-cli validate --input-file <filename>`

#### When submitting in SPDX format

- Standard: SPDX 2.3
- Encoding: JSON
- Generation tool: [ tool name and version used ]
- Validation: `pyspdxtools -i <filename>` (spdx-tools)

---

### 3. Coverage

| Item                 | Content                                                       |
| -------------------- | ------------------------------------------------------------- |
| Included components  | All direct and transitive dependencies                        |
| Included information | Component name, version, license, PURL, hash                  |
| Exclusions           | Build-only tools (devDependencies, etc., not part of runtime) |
| Analysis scope       | [ e.g., backend service / frontend app / all ]                |

---

### 4. License Obligation Fulfillment Status

| License type               | Included                  | Fulfillment action                                    |
| -------------------------- | ------------------------- | ----------------------------------------------------- |
| MIT, Apache-2.0, BSD       | Included                  | Copyright notices included                            |
| LGPL-2.1, LGPL-3.0         | [ Included/Not included ] | Dynamic linking used; source ready to be provided     |
| GPL-2.0, GPL-3.0           | [ Included/Not included ] | Source code disclosure/provision obligations reviewed |
| Other proprietary licenses | [ Included/Not included ] | Individual license agreements confirmed               |

> For the detailed license analysis, see `output/sbom/license-report.md`

---

### 5. Update Policy

| Item             | Content                                                             |
| ---------------- | ------------------------------------------------------------------- |
| Update cycle     | On feature completion, as needed (per release)                      |
| Emergency update | Regenerate and resubmit immediately when a Critical/High CVE occurs |
| Version control  | Maintain an SBOM archive for each release version                   |
| Delivery method  | [ Email / secure portal / method designated by the recipient ]      |

---

### 6. Contacts

For SBOM-related inquiries or additional requests, contact the following.

| Role             | Contact  | Email     |
| ---------------- | -------- | --------- |
| SBOM manager     | [ Name ] | [ Email ] |
| Security officer | [ Name ] | [ Email ] |
| Legal/Compliance | [ Name ] | [ Email ] |

---

### 7. Additional Materials Available

The following materials can be provided upon request:

- [ ] Open source attribution notice (NOTICES.txt / ATTRIBUTION.md)
- [ ] Vulnerability analysis report
- [ ] Detailed license analysis report
- [ ] Source code (for applicable LGPL/GPL components)

---

_This document was prepared in accordance with ISO/IEC 18974 requirement 4.3.1._
