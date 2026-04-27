---
sidebar_label: SBOM output
sidebar_position: 4
---

# SBOM Output Best Practice

[05 Tools Chapter] This is an example of SBOM-related output generated from (/docs/tools/sbom-generation).
You can check actual output examples based on sample projects (including `java-vulnerable`, Log4Shell CVE-2021-44228).

---

## SBOM License Analysis Report

> **generating agent**: `05-sbom-analyst` | **Save Path**: `output/sbom/license-report.md`

---

Report Type: SBOM License Analysis
Created Date: 2026-03-23 ​​07:11
Target project: vulnerable-java-app
Tool used: syft 1.42.3

---

### 1. Summary

- Analysis object SBOM: `java-vulnerable.cdx.json` (CycloneDX 1.6)
- Total of **3** software components (excluding file items)
- SBOM My license field is empty → License supplementation classification based on external information
- Apache Log4j 2.14.1 is classified as **Apache 2.0 (Permissive)**
- Internal application (`vulnerable-java-app`) has no license information → **Unknown**
- **0 Copyleft components** (no immediate compliance action required)
- ⚠️ License information is missing in SBOM, so re-running the tool or manual supplementation is recommended.

### 2. License details for each component

| component           | version | group                    | License    | Category   | Source                        |
| ------------------- | ------- | ------------------------ | ---------- | ---------- | ----------------------------- |
| log4j-api           | 2.14.1  | org.apache.logging.log4j | Apache-2.0 | Permissive | Maven Central (complementary) |
| log4j-core          | 2.14.1  | org.apache.logging.log4j | Apache-2.0 | Permissive | Maven Central (complementary) |
| vulnerable-java-app | 1.0.0   | com.example              | Unknown    | Unknown    | SBOM Not stated               |

> **Note:** No license information was included when generating SBOM.
> When re-running syft, check whether `--source-name` or Maven Central metadata is activated or
> We recommend using the `cdxgen` tool in parallel to supplement the license field.

### 3. License classification summary

| Category        | Number of components | Component List        |
| --------------- | -------------------- | --------------------- |
| Permissive      | 2                    | log4j-api, log4j-core |
| Weak Copyleft   | 0                    | —                     |
| Strong Copyleft | 0                    | —                     |
| Unknown         | 1                    | vulnerable-java-app   |

### 4. Measures

#### ⚪ Info — SBOM Supplementary license information

- **Target:** All components (especially `vulnerable-java-app`)
- **Action:** Enable license metadata when rerunning syft or cdxgen.

  ```bash
  # syft: include Maven POM license info
  syft /path/to/project --output cyclonedx-json

  # cdxgen: auto-collect license information
  cdxgen -t java /path/to/project -o sbom.cdx.json
  ```

- **Estimated time:** 30 minutes

#### ⚪ Info — Specifies internal application license

- **Target:** `vulnerable-java-app@1.0.0`
- **Action:** Specify Internal License or Proprietary in `<licenses>` section of `pom.xml`
  ```xml
  <licenses>
    <license>
      <name>Proprietary</name>
      <url>https://example.com/license</url>
    </license>
  </licenses>
  ```
- **Estimated time:** 15 minutes

### 5. Summary of compliance obligations

| License           | Obligations                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| Apache-2.0        | Retain copyright notice, include NOTICE file, distribute licensed copies |
| Permissive common | Secondary distribution includes original license text                    |

> Apache-2.0 is friendly to binary distribution as there is no obligation to disclose source code.
> Make sure your deployment package includes `LICENSE`, `NOTICE` files.

---

_This report was created to meet requirements ISO/IEC 5230 §3.3.2 (License Identification) and §3.4.1 (Compliance Deliverables)._

---

## Copyleft Risk Report

> **generating agent**: `05-sbom-analyst` | **Save Path**: `output/sbom/copyleft-risk.md`

---

Report Type: Copyleft Risk Analysis
Created Date: 2026-03-23 ​​07:11
Target project: vulnerable-java-app
Tool used: syft 1.42.3

---

### 1. Summary

- Analysis target: `java-vulnerable.cdx.json` (CycloneDX 1.6, 3 components)
- **Strong Copyleft (GPL/AGPL) Components: 0**
- **Weak Copyleft (LGPL/MPL) Component: 0**
- Both identified components are **Apache-2.0 (Permissive)**, so there is no risk of copyleft.
- 1 component is licensed **Unknown** — needs to be confirmed separately
- ⚠️ SBOM Potential unconfirmed copyleft risk exists due to missing license metadata

### 2. List of Copyleft Risk Components

| component           | version | License    | Copyleft rating | Risk      | action                        |
| ------------------- | ------- | ---------- | --------------- | --------- | ----------------------------- |
| log4j-api           | 2.14.1  | Apache-2.0 | None            | 🟢Low     | Not necessary                 |
| log4j-core          | 2.14.1  | Apache-2.0 | None            | 🟢Low     | Not necessary                 |
| vulnerable-java-app | 1.0.0   | Unknown    | Unconfirmed     | 🟡 Medium | License verification required |

### 3. Copyleft rating criteria

| Rating          | Applicable License          | Obligations upon distribution                                      |
| --------------- | --------------------------- | ------------------------------------------------------------------ |
| Strong Copyleft | GPL-2.0, GPL-3.0, AGPL-3.0  | Obligation to disclose full source code                            |
| Weak Copyleft   | LGPL-2.1, LGPL-3.0, MPL-2.0 | Disclosure of source code of the modified version of the component |
| Permissive      | Apache-2.0, MIT, BSD        | Keep only copyright notice                                         |
| Unknown         | —                           | Recommend conservative handling with copyleft until confirmation   |

### 4. Risk assessment

#### Based on current distribution method

| Distribution method                     | Copyleft risk                           |
| --------------------------------------- | --------------------------------------- |
| Source code private binary distribution | 🟢 No risk (only when using Apache-2.0) |
| SaaS/Network Services                   | 🟢 Risk-Free (No AGPL Components)       |
| Open source redistribution              | 🟢 No Risk (No Strong Copyleft)         |

> **Conclusion:** All currently identified open source components (log4j-api, log4j-core) have been converted to Apache-2.0.
> There is no obligation to disclose source code in any distribution method.

### 5. Measures

#### 🟡 Medium — Check Unknown licensed components

- **Target:** `vulnerable-java-app@1.0.0` (internally developed application)
- **Risk:** Compliance is unclear when distributed externally without specifying a license.
- **Action:** Specify license information in `pom.xml` or document internal IP policy
- **Estimated time:** 15 minutes

#### ⚪ Info — SBOM Supplementary license information

- **Target:** All components
- **Risk:** Copyleft may be missed when adding additional dependencies with a blank license field.
- **Action:** Activate and regenerate the license metadata in the SBOM generation tool.
- **Estimated time:** 30 minutes

### 6. Future monitoring recommendations

- Regenerate SBOM and update this report when new dependencies are added.
- Legal team review required when introducing GPL/AGPL components
- Establish quarterly SBOM license status inspection schedule

---

_This report was created to meet requirement ISO/IEC 5230 §3.3.2 (License Identification)._

---

## SBOM Management Plan

> **generating agent**: `05-sbom-management` | **Save Path**: `output/sbom/sbom-management-plan.md`

---

This document defines the SBOM management and maintenance plan to meet ISO/IEC 18974 4.3.1 and 4.3.2 requirements.

| Item                        | Content                                                             |
| --------------------------- | ------------------------------------------------------------------- |
| Whether provided externally | Yes (available upon customer/delivery request)                      |
| Supported Formats           | CycloneDX, SPDX (selected depending on the request of the supplier) |
| Update cycle                | Frequently upon feature completion (unit of release)                |

---

### 1. SBOM Creation Principle

#### 1.1 Creation time

- Generate SBOM at each release build after completion of feature development
- Immediate regeneration when dependency changes (addition/deletion/version update) occur
- Check the latest SBOM regeneration during regular security checks (once a month)

#### 1.2 Generation Tool

| Build environment | tools                      | creation format  |
| ----------------- | -------------------------- | ---------------- |
| Java/Maven        | `cyclonedx-maven-plugin`   | CycloneDX JSON   |
| Java/Gradle       | `cyclonedx-gradle-plugin`  | CycloneDX JSON   |
| Node.js           | `@cyclonedx/cyclonedx-npm` | CycloneDX JSON   |
| Python            | `cyclonedx-bom`            | CycloneDX JSON   |
| Format Conversion | `cdxgen`, `spdx-tools`     | CycloneDX ↔ SPDX |

#### 1.3 format conversion

If the supplier requests SPDX, CycloneDX → SPDX conversion is performed.

```bash
# CycloneDX → SPDX convert (cdxgen Use)
cdxgen -o sbom.cdx.json --format json .
# SPDX for conversion, use separate tools (spdx-tools) or customer-designated tools
```

---

### 2. SBOM Renewal Procedure

#### 2.1 Update per release (main procedure)

```
1. Feature development complete and code freeze
2. Finalize dependency list (package.json / pom.xml / requirements.txt etc.)
3. SBOM automatic generation (CI/CD pipeline integration)
4. License review (copyleft check whether new items are included)
5. vulnerability scan (OSV-Scanner / Grype)
6. Tag and store SBOM file version
7. When customer submission is required sbom-sharing-template.md attach and deliver
```

#### 2.2 Emergency update (in case of security vulnerability)

Immediate update regardless of release cycle when Critical/High CVE occurs:

1. Patch or replace vulnerable components
2. Regenerate SBOM
3. Resubmit renewal SBOM to the supplier (if necessary)

---

### 3. CI/CD integration automation

#### 3.1 Pipeline Configuration (Example: GitHub Actions)

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
      - uses: actions/checkout@v4

      - name: Generate SBOM (CycloneDX)
        run: |
          # replace with commands for your project build environment
          npx @cyclonedx/cyclonedx-npm --output-file sbom.cdx.json

      - name: vulnerability scan
        run: |
          curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
          grype sbom:sbom.cdx.json

      - name: Store SBOM
        uses: actions/upload-artifact@v4
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

### 4. Supply chain monitoring (ISO/IEC 18974 4.3.2)

#### 4.1 Regular monitoring items

| Item                     | cycle                          | tools                  |
| ------------------------ | ------------------------------ | ---------------------- |
| New CVE Scan             | Once a month (or upon release) | OSV-Scanner, Grype     |
| License change detection | Upon release                   | ort, scancode-toolkit  |
| Track dependency updates | continuous                     | Dependabot, Renovate   |
| SBOM Validation          | Upon release                   | cyclonedx-cli validate |

#### 4.2 Monitoring automation settings

```bash
# GitHub Dependabot enable (.github/dependabot.yml)
version: 2
updates:
  - package-ecosystem: "npm"   # or maven, pip, etc.
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

#### 4.3 vulnerability response standards

| Severity | Response Deadline             | action                                    |
| -------- | ----------------------------- | ----------------------------------------- |
| Critical | Immediately (within 24 hours) | Applying a patch or replacement component |
| High     | within 7 days                 | Establish and apply patch plan            |
| Medium   | Within 30 days                | Reflected in next release                 |
| Low      | Plan within 90 days or next   | Review whether to accept risk             |

---

### 5. Person in charge and contact information

| Role                | Responsibilities                                   |
| ------------------- | -------------------------------------------------- |
| SBOM Contact person | SBOM Creation, update, and distribution management |
| Security Officer    | Review and respond to vulnerability scan results   |
| Legal/Compliance    | License review and supplier consultation           |

> Refer to `output/organization/` output for contact information

---

### 6. Governing standards

| standard      | Requirements                                                  |
| ------------- | ------------------------------------------------------------- |
| ISO/IEC 18974 | 4.3.1 — SBOM Care and Maintenance                             |
| ISO/IEC 18974 | 4.3.1 — SBOM Share (Supply Chain Partner)                     |
| ISO/IEC 18974 | 4.3.2 — Continuous monitoring of supply chain vulnerabilities |

---

## SBOM Submission notice (template for submission to delivery address)

> **generating agent**: `05-sbom-management` | **Save Path**: `output/sbom/sbom-sharing-template.md`

---

> **How ​​to use**: Deliver this document along with the SBOM file to the supplier/customer.
> Fill out the `[ ]` item with actual information and submit.

---

Recipient: [Supplier/Customer Name]
From: [your company name]
Document Title: SBOM (Software Bill of Materials) Submission Instructions
Created on: [ YYYY-MM-DD ]

---

### 1. Submission file information

| Item         | Content                                |
| ------------ | -------------------------------------- |
| Product name | [Product name or software name]        |
| version      | [ v0.0.0 ]                             |
| Build date   | [ YYYY-MM-DD HH:MM ]                   |
| SBOM format  | [ CycloneDX 1.5 JSON / SPDX 2.3 JSON ] |
| file name    | [Example: myproduct-v1.0.0.cdx.json ]  |
| SHA-256 hash | [file hash value]                      |

---

### 2. SBOM format information

#### When submitting in CycloneDX format

- Standard: CycloneDX Specification 1.5
- Encoding: JSON
- Creation tool: [Tool name and version used]
- Verification: `cyclonedx-cli validate --input-file <filename>`

#### When submitting in SPDX format

- Standard: SPDX 2.3
- Encoding: JSON
- Creation tool: [Tool name and version used]
- Verification: `pyspdxtools validate <filename>`

---

### 3. Coverage

| Item                 | Content                                                        |
| -------------------- | -------------------------------------------------------------- |
| Included Components  | All direct and transitive dependencies                         |
| Included information | Component name, version, license, PURL, hash                   |
| Exclusions           | Build-only tools (devDependencies, etc., runtime not included) |
| Analysis scope       | [Example: Backend service / Frontend app / All ]               |

---

### 4. Status of fulfillment of license obligations

| License Type             | Included or not           | Implementation Action                                                   |
| ------------------------ | ------------------------- | ----------------------------------------------------------------------- |
| MIT, Apache-2.0, BSD     | Included                  | Complete with copyright notice                                          |
| LGPL-2.1, LGPL-3.0       | [ Included/Not Included ] | Using dynamic linking method, ready to provide source                   |
| GPL-2.0, GPL-3.0         | [ Included/Not Included ] | Completion of review of source code disclosure or provision obligations |
| Other Exclusive Licenses | [ Included/Not Included ] | Individual license agreement confirmed                                  |

> For detailed license analysis results, see `output/sbom/license-report.md`

---

### 5. Renewal Policy

| Item            | Content                                                            |
| --------------- | ------------------------------------------------------------------ |
| Update cycle    | Frequently upon feature completion (unit of release)               |
| Urgent update   | Regenerate and resubmit immediately when Critical/High CVE occurs  |
| Version Control | Maintain SBOM archive for each release version                     |
| Delivery method | [Email / Secure Portal / Method of Designating a Delivery Address] |

---

### 6. Contact information

SBOM For related inquiries or additional requests, please contact below.

| Role                | Contact person | Contact Us |
| ------------------- | -------------- | ---------- |
| SBOM Contact person | [Name]         | [Email]    |
| Security Officer    | [Name]         | [Email]    |
| Legal/Compliance    | [Name]         | [Email]    |

---

### 7. Additional available materials

The following materials can be provided upon request:

- [ ] Open source notice (NOTICES.txt / ATTRIBUTION.md)
- [ ] vulnerability analysis report
- [ ] License detailed analysis report
- [ ] Source code (LGPL/GPL components)

---

_This document has been prepared in accordance with the requirements ISO/IEC 18974 4.3.1._
