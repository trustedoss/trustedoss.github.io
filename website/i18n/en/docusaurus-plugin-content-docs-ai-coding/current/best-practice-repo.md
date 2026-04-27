---
id: best-practice-repo
title: Best Practice Repository
sidebar_label: Best Practice Repository
sidebar_position: 8
---

# Best Practice Repository

This is a reference GitHub repository that implements all Stages 1-5 from the [5-Stage Strategy](./strategy).
You can fork it for immediate use or copy configuration files into an existing project.

:::info Repository
**[github.com/trustedoss/ai-coding-best-practice](http://github.com/trustedoss/ai-coding-best-practice)**
:::

---

## Repository Structure

```
ai-coding-best-practice/
├── README.md                          # badges + step-by-step explanation + guide links
├── src/
│   └── app.py                         # sample Python web app (with dependencies)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml                 # app startup for DAST/AI fuzzing
│
├── CLAUDE.md                          # Step 2: Embed AI rules
├── .cursorrules                       # Step 2: Cursor rules
│
├── .gitleaks.toml                     # Step 3: secret detection settings
├── .grype.yaml                        # Step 3: SCA threshold settings
├── .semgrep.yml                       # Step 3: SAST ruleset
│
├── renovate.json                      # Step 4: Renovate auto-updates
│
├── k8s/
│   └── deployment.yaml                # sample target for IaC security scan (Checkov)
│
├── scripts/
│   └── ai-fuzz.py                     # AI fuzzing run script
│
└── .github/
    ├── dependabot.yml                 # Step 4: Dependabot settings
    └── workflows/
        ├── secret-detection.yml       # Step 3: Gitleaks
        ├── sast.yml                   # Step 3: Semgrep
        ├── codeql.yml                 # Step 3: CodeQL (PR + weekly)
        ├── oss-policy.yml             # Step 3: syft + grype + licenses
        ├── iac-security.yml           # Step 3: Checkov (Dockerfile/K8s)
        ├── container-security.yml     # Step 3: Trivy
        ├── ai-review.yml              # Step 4: findings-driven AI review (ANTHROPIC_API_KEY auto-enabled when configured)
        ├── ai-fuzzing.yml             # Step 4: AI fuzzing (weekly + push)
        └── dast.yml                   # Step 5: OWASP ZAP (Push to main)
```

---

## Stage-by-stage Implementation

### Stage 3 — CI/CD Auto Blocking

| Area               | Implementation File      | Description                                                  |
| ------------------ | ------------------------ | ------------------------------------------------------------ |
| Secret Detection   | `secret-detection.yml`   | Gitleaks — Detects hardcoded API keys/tokens in every PR     |
| SAST               | `sast.yml`               | Semgrep — OWASP Top 10 ruleset + custom rules                |
| SAST (Deep)        | `codeql.yml`             | CodeQL — Static analysis on PRs and weekly schedule          |
| SCA                | `oss-policy.yml`         | syft + grype — SBOM generation, CVE scan, and license checks |
| IaC Security       | `iac-security.yml`       | Checkov — Detects Dockerfile/Kubernetes configuration issues |
| Container Security | `container-security.yml` | Trivy — Docker image vulnerability scan                      |

### Stage 4 — AI Defense Layer

| Item                | Implementation File | Description                                                                     |
| ------------------- | ------------------- | ------------------------------------------------------------------------------- |
| AI Code Review (4a) | `ai-review.yml`     | Semgrep/grype findings → Claude validation and deep interpretation → PR comment |
| AI Fuzzing (4b)     | `ai-fuzzing.yml`    | Claude generates edge cases → runs app → detects 5xx errors (Push to main)      |

### Stage 5 — Continuous Monitoring & Auto-remediation

| Item                         | Implementation File | Description                                              |
| ---------------------------- | ------------------- | -------------------------------------------------------- |
| Automatic Dependency Updates | `dependabot.yml`    | Automatically creates weekly dependency update PRs       |
| Automatic Patch Merge        | `renovate.json`     | Auto-merges Critical patches, notifies for Major updates |
| DAST                         | `dast.yml`          | OWASP ZAP Baseline — dynamic scan on Push to main        |

---

## Getting Started

**1. Fork the repository**

```bash
git clone https://github.com/YOUR-ORG/ai-coding-best-practice.git
cd ai-coding-best-practice
```

**2. Add GitHub Secrets**

| Secret Name         | Usage                      | Required |
| ------------------- | -------------------------- | -------- |
| `ANTHROPIC_API_KEY` | AI code review, AI fuzzing | Optional |

**3. Open a PR to verify pipelines**

```bash
git checkout -b test/pipeline-check
echo "# test" >> README.md
git commit -am "test: pipeline check"
git push origin test/pipeline-check
```

When a PR is created, six Stage 3 workflows run automatically.
Stage 4 AI review is enabled automatically when `ANTHROPIC_API_KEY` is configured.
AI fuzzing and DAST run on Push to main or weekly schedules.

---

## Customization Points

| File             | What to Customize                                                |
| ---------------- | ---------------------------------------------------------------- |
| `CLAUDE.md`      | Reflect team license policy and prohibited package list          |
| `.grype.yaml`    | Adjust vulnerability thresholds (`high` ↔ `critical`)            |
| `.gitleaks.toml` | Add internal organization pattern exceptions                     |
| `.semgrep.yml`   | Add language/framework-specific rulesets                         |
| `renovate.json`  | Adjust auto-merge scope and update cadence                       |
| `dast.yml`       | After stabilization, change to `fail_action: true` for hard fail |

---

## Related Guides

- [5-Stage Strategy](./strategy) — Purpose and adoption sequence of each stage
- [30-Minute Quick CI/CD](./cicd-quick) — Minimal starting point focused on SCA
- [AI Security Code Review](./ai-security-review) — Semantic vulnerability detection with AI
- [DevSecOps — Organization-wide Pipeline Design](/devsecops/pipeline-design) — Multi-repository policy governance
