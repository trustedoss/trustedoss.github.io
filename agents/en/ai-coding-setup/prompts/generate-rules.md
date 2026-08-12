# generate-rules prompt

## Purpose

Generate the open source policy rules files for each AI coding tool, based on the user's answers
and the project analysis.

## Input variables

These variables are collected through the questions in CLAUDE.md.

- PROJECT_PATH: path of the project to analyse
- TOOLS: the selected AI coding tools
- LICENSE_LEVEL: strict / standard / flexible
- VULN_THRESHOLD: critical / high / medium
- OPTIONS: additional rules (sbom / copyright / cicd)
- DETECTED_LANGS: detected languages (automatic)
- DETECTED_PKGS: detected packages (automatic)
- RISK_PKGS: packages under prohibited licenses (automatic)

## License policy mapping

Include the following in the rules according to LICENSE_LEVEL.

Strict:
Allowed: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
Prohibited: LGPL, MPL, GPL, AGPL, SSPL, Commons Clause

Standard:
Allowed: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
Caution (legal review required): LGPL, MPL
Prohibited: GPL, AGPL, SSPL, Commons Clause

Flexible:
Allowed: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, LGPL, MPL
Caution (legal review required): GPL, AGPL
Prohibited: SSPL, Commons Clause

## Vulnerability policy mapping

Include the following according to VULN_THRESHOLD.

critical: block only Critical CVEs immediately; warn on High and below.
high: block when a High or Critical CVE is found; warn on Medium and below.
medium: block when a Medium, High, or Critical CVE is found.

## Audit commands per language

Add only the languages present in DETECTED_LANGS to the rules.

javascript / typescript: npm audit or yarn audit
python: pip-audit
java: dependency-check
go: govulncheck ./...
rust: cargo audit
ruby: bundle audit

## File generation rules per tool

Generate the file below for each tool in TOOLS.
Every output path sits under output/ai-coding/.

Claude Code:
File: CLAUDE.md
Format: instructions organised under ## section headers
Note: if the file already exists at PROJECT_PATH, add only the ## Open source policy section (keep the existing content)

Cursor:
File: .cursor/rules/oss-policy.mdc
Format: frontmatter (description, alwaysApply: true) plus a concise rule list
Note: do not generate the legacy single .cursorrules file

GitHub Copilot:
File: .github/copilot-instructions.md
Format: markdown instructions

Devin Desktop (formerly Windsurf):
File: .devin/rules/oss-policy.md
Format: a concise rule list (do not generate the legacy .windsurfrules or .windsurf/rules/)

Cline:
File: .clinerules
Format: a list of project instructions

Aider:
File: CONVENTIONS.md
Format: a list of project instructions (include a note on registering `read: CONVENTIONS.md` in .aider.conf.yml)

## Rules for LICENSE-RISK-REPORT.md

Generate it only when RISK_PKGS is non-empty.
Omit it otherwise.

What it contains:

- The list of packages found under prohibited or caution licenses
- The license type of each package
- Recommended alternative packages, where they exist
- Whether legal review is advised

## Rules for SETUP-SUMMARY.md

Always generate it.

What it contains:

- The list of generated files and where each one goes
- Example copy commands per project path
- A summary of the license risks found, where there are any
- The next step (the devsecops-setup agent)

## Execution order

1. Read the dependency files at PROJECT_PATH
   → detect languages and packages automatically
   → search for packages under prohibited licenses

2. If RISK_PKGS is non-empty, report it to the user and confirm whether to continue

3. Once every answer is collected, start generating files
   → generate the per-tool files in the order of the TOOLS list
   → LICENSE-RISK-REPORT.md (when RISK_PKGS is non-empty)
   → SETUP-SUMMARY.md

4. After generation, print the "Message when finished" from CLAUDE.md

## Cautions

- Do not write files outside output/ai-coding/
- Only read the existing files at PROJECT_PATH; never modify them
- Do not expose local absolute paths in the deliverables
  (use the ./project-name form in the path examples of SETUP-SUMMARY.md)
- Write every generated file in English
