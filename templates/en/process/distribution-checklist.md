# Pre-Distribution License Compliance Checklist

<!-- 5230 §3.4.1.1·§3.4.1.2 (G3L.5) -->

**Project name**: {project name}
**Version**: {version}
**Planned release date**: YYYY-MM-DD
**Reviewer**: {name}

This process document is based on the OpenChain KWG process guide (the pre-distribution check and notice stages of the open source management process) and on ISO/IEC 5230 and 18974. The KWG guide is licensed under CC BY 4.0.

---

## 1. SBOM freshness check

<!-- 5230 §3.3.1.2 -->

- [ ] Is the SBOM up to date for this release?
- [ ] Was `output/sbom/sbom-commands.sh` run to regenerate the SBOM?
- [ ] Are newly added dependencies reflected in the SBOM?

---

## 2. License obligation fulfilment check

<!-- 5230 §3.3.2.1, §3.1.5.1 -->

- [ ] Have all licenses in `output/sbom/license-report.md` been checked?
- [ ] Is there no license included that is missing from `output/policy/license-allowlist.md`?
- [ ] When a copyleft license is used, are the items below satisfied:

| License | Obligations                                        | Fulfilled                 |
| ------- | -------------------------------------------------- | ------------------------- |
| GPL-2.0 | Publish source code, include the notice            | ☐ not applicable / ☐ done |
| GPL-3.0 | Publish source code, include the notice            | ☐ not applicable / ☐ done |
| LGPL    | Publish source code or guarantee dynamic linking   | ☐ not applicable / ☐ done |
| AGPL    | Publish source code including for network services | ☐ not applicable / ☐ done |
| MPL     | Publish the source code of modified files          | ☐ not applicable / ☐ done |

---

## 3. Attribution notice generation and check

<!-- 5230 §3.4.1.1 -->

### 3-1. Generating the notice

- Example tools: use whichever of `syft`, `scancode-toolkit`, or `tern` fits the environment.
- Include a `NOTICE` or `OPEN_SOURCE_LICENSES.txt` file in the build output.
- What to include: component name, version, license SPDX ID, copyright statement, and the full license text or a license URL.
- For binary distribution (embedded, apps): provide at least one of an enclosed file, an About screen, or a QR code or URL.

### 3-2. Checking the notice

- [ ] Is the `NOTICE` or `OPEN_SOURCE_LICENSES.txt` file included in the distribution package?
- [ ] Does the notice carry the copyright statement and license text for every open source component?
- [ ] For binary distribution, is there a way for users to reach the license notice?

---

## 4. Retaining compliance deliverables

<!-- 5230 §3.4.1.2 -->

- [ ] Has a copy of this release's SBOM been retained? (path: `output/sbom/{project}-{version}.cdx.json`)
- [ ] Has a copy of the notice been retained?
- [ ] Are the retention criteria below met?

| Retained item                    | Location                                     | Retention period                                |
| -------------------------------- | -------------------------------------------- | ----------------------------------------------- |
| SBOM ({version}.cdx.json)        | {internal repository / cloud storage}        | **At least 3 years from the distribution date** |
| Notice (NOTICE file)             | {internal repository / cloud storage}        | **At least 3 years from the distribution date** |
| Completed copy of this checklist | output/process/distribution-checklist.md     | **At least 3 years from the distribution date** |
| Previous version checklists      | {archive path: archive/checklist/{version}/} | **At least 3 years from the distribution date** |

The OSPM checks whether retention needs to be extended before the period expires.

---

## 5. License non-compliance check

<!-- 5230 §3.2.2.5 -->

- [ ] Is this release free of license non-compliance cases?
- [ ] If there was a non-compliance case, has the corrective action been completed?

---

## 6. Final approval

| Party                          | Name   | Signature / date |
| ------------------------------ | ------ | ---------------- |
| Open Source Program Manager    | {name} | YYYY-MM-DD       |
| Legal review (where necessary) | {name} | YYYY-MM-DD       |
| Release approver               | {name} | YYYY-MM-DD       |

---

## 7. Final check after release

Immediately after the release, check the following and record it in the fulfilment record.

- [ ] Visually confirm that the released artifact really contains the NOTICE file or a way to reach it
- [ ] Confirm that the SBOM for the released version is archived in `output/sbom/`
- [ ] Confirm that monitoring for new CVEs has started after the release (see vulnerability-response.md section 5)
- [ ] Confirm that the release record (version, date and time, approver, channel) is in the fulfilment record

---

## Fulfilment record

<!-- 5230 §3.4.1.2 requirement to record fulfilment -->

Once this checklist is complete, retain it in `output/process/distribution-checklist.md` together with the date.
Release history: record the completion date per version at the bottom of this file.

| Version   | Release date | Checklist complete | Owner  |
| --------- | ------------ | ------------------ | ------ |
| {version} | YYYY-MM-DD   | ✅                 | {name} |
