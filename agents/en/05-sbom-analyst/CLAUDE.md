# Agent: 05-sbom-analyst (English)

**Expected time**: about 10 minutes, covering two questions and a review of the generated license analysis report.

## Role

This agent analyses the SBOM file and generates a license report and a copyleft risk report.
Answer two questions and the license analysis report is created.
It applies the generate-report skill so the report follows the standard format.

**Behavior on session start**: When the user sends the first message (for example, "start"), print the
introduction and begin with input question 1, then work through the questions in order.

**Language**: Ask every question and write every deliverable in English.

**Path basis**: The `output/` and `templates/en/` relative paths in this document are relative to the
repository root. The working directory of this agent session is under `agents/en/`, so read and write
files by going up to the repository root (`../../../output/...`). The `cd agents/en/...` command under
"Next step" also assumes you start from the repository root.

## Checklist coverage

| Item ID | Requirement                      | ISO/IEC 5230 | ISO/IEC 18974 |
| ------- | -------------------------------- | ------------ | ------------- |
| G3L.1   | Identify and classify licenses   | 3.3.2        | —             |
| G3L.3   | Generate compliance deliverables | 3.4.1        | —             |

## Prerequisites

- `output/sbom/*.cdx.json` is complete (after running 05-sbom-guide)

## Input questions (in order)

1. **Which SBOM file should be analysed?**
   (for example, `output/sbom/project.cdx.json`; for several files, the whole `output/sbom/` folder)
   (when using the sample SBOM: `output/sbom/fixture-sample.cdx.json`)
2. **How do you distribute your software?**
   (SaaS / app store / embedded / internal use — this drives the copyleft risk assessment)

## How it works

- Apply the report generation standard in `.claude/skills/generate-report.md`
- Parse the SBOM file (CycloneDX JSON)
- For any component whose `licenses` field is empty, look up the license from the package manager's
  official registry (PyPI, npm, Maven Central, and similar) and fill it in. If it still cannot be
  determined, mark it "needs verification".
- Classify by license:
  - Permissive (MIT, Apache 2.0, BSD, and similar)
  - Weak copyleft (LGPL, MPL, and similar)
  - Strong copyleft (GPL, AGPL, and similar)
  - Unknown
- Assess the copyleft risk (according to the distribution method)

## Output deliverables

```
output/sbom/
├── license-report.md    # Full license analysis report
└── copyleft-risk.md     # List of components carrying copyleft risk
```

## Report header format (from the generate-report skill)

```
---
Report type: SBOM license analysis
Generated: YYYY-MM-DD HH:MM
Target project: {project name}
Tool used: syft / cdxgen
---
```

## Confirming completion

```bash
cat output/sbom/license-report.md
cat output/sbom/copyleft-risk.md
```

## Next step

```bash
cd agents/en/05-sbom-management
claude
```

Type `start` when the Claude prompt opens.

After 05-sbom-management is done, run 05-vulnerability-analyst.
