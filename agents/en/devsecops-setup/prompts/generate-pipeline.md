# generate-pipeline prompt

## Purpose

Generate the DevSecOps CI/CD pipeline files and policy files, based on the user's answers and the
project analysis.

## Input variables

- PROJECT_PATH: path of the project to analyse
- PLATFORM: github / gitlab / both
- DOMAINS: the selected security areas
- VULN_THRESHOLD: critical / high / medium
- IAC_TOOLS: terraform / kubernetes / cloudformation
- SCHEDULE: daily / weekly / none
- DETECTED_LANGS: detected languages (automatic)
- HAS_DOCKERFILE: true / false (automatic)
- HAS_IAC: true / false (automatic)
- HAS_EXISTING_WORKFLOW: true / false (automatic)

## Pipeline design principles

1. Parallel execution: put independent checks in the same stage
2. Gates per stage: secret detection → code analysis → build analysis
3. Failure policy:
   - Secrets, SAST, SCA, IaC: hard fail (block the pull request)
   - DAST: soft fail while it is being introduced (fail_action: false)
4. Artifact retention: 90 days for SBOMs, 30 days for reports

## Action version reference (must be followed)

Use the owners and tags in the table below verbatim in `uses:`. Do not invent versions from memory.
Do not use moving references (`@master`, `@main`). A supply chain compromise can replace a whole tag,
so pinning the version is the real defence (see the trivy-action tag poisoning case of 2026-03).

| Purpose                 | uses value                                                                                                |
| ----------------------- | --------------------------------------------------------------------------------------------------------- |
| Checkout                | `actions/checkout@v7`                                                                                     |
| Artifact upload         | `actions/upload-artifact@v7`                                                                              |
| SBOM generation         | `anchore/sbom-action@v0`                                                                                  |
| SBOM vulnerability scan | `anchore/scan-action@v7`                                                                                  |
| Container scan          | `aquasecurity/trivy-action@0.36.0`                                                                        |
| Secret detection        | `gitleaks/gitleaks-action@v3`                                                                             |
| IaC check               | `bridgecrewio/checkov-action@v12`                                                                         |
| Terraform check         | `aquasecurity/tfsec-action@v1.0.3`                                                                        |
| SAST                    | `github/codeql-action/init@v4`, `github/codeql-action/analyze@v4`, `github/codeql-action/upload-sarif@v4` |
| DAST                    | `zaproxy/action-baseline@v0.15.0`, `zaproxy/action-api-scan@v0.10.0`                                      |

`anchore/scan-action` falls back to `medium` when `severity-cutoff` is omitted.
Always state the threshold you intend.

When `.trivyignore.yaml` is generated alongside, the Trivy run has to point at it with `--ignorefile`
for it to take effect.

## GitHub Actions generation rules

devsecops-pr.yml:

- on: pull_request (branches: [main, develop])
- parallel jobs:
  - secret-detection (always first, no needs)
  - sast (needs: secret-detection, when SAST is selected)
  - sca (needs: secret-detection, when SCA is selected)
  - iac (needs: secret-detection, when IaC is selected)
- Each job: runs-on ubuntu-latest
- checkout: fetch-depth: 0 (full history for secret detection)
- SBOM artifact: retention-days: 90

devsecops-merge.yml (when container security or DAST is selected):

- on: push (branches: [main])
- job order:
  - container-security (Trivy, when container security is selected)
  - dast (needs: container-security, when DAST is selected)
- DAST: fail_action: false (soft fail at first)

devsecops-schedule.yml (when a schedule is selected):

- on: schedule (cron) plus workflow_dispatch
- jobs: sca-scan and container-scan (only the selected areas)
- Artifacts: retention-days: 365 (kept for a year)

## GitLab CI generation rules

stages: [secret-scan, code-scan, build-scan, dast]
Place each domain in its stage:

- secret-detection → secret-scan stage
- sast, sca, iac → code-scan stage (in parallel)
- container → build-scan stage
- dast → dast stage
  rules: merge_request_event (jobs of the PR stage)
  CI_COMMIT_BRANCH == "main" (jobs of the merge stage)

## Policy file generation rules

.grype.yaml (when SCA is selected):

- fail-on-severity: the VULN_THRESHOLD value
- Include one ignore example (with a comment explaining how to use it)

.gitleaks.toml (when secret detection is selected):

- useDefault: true
- allowlists: exceptions for test file paths
- Detect the test folders under PROJECT_PATH automatically and include those paths

.trivyignore.yaml (when container security is selected):

- Include one example ignore rule

## PIPELINE-SUMMARY.md generation rules

Always generated. It contains:

- A table of the selected security areas and the tools used
- The pipeline execution flow, stage by stage
- Expected duration per area
- The list of generated files

## APPLY-GUIDE.md generation rules

Always generated. It contains:

- Where each file goes
- How to avoid conflicts with existing workflows
  (emphasised when HAS_EXISTING_WORKFLOW is true)
- What to check after the first run
- A roadmap for tightening in stages
  (start with soft fail, move to hard fail once it is stable)

## Cautions

- Do not write files outside output/devsecops/
- Only read the existing files at PROJECT_PATH; never modify them
- Do not expose local absolute paths in the deliverables
- Write the comments in every generated file in English
