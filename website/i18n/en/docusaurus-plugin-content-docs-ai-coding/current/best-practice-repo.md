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
├── README.md                          # 배지 + 단계별 설명 + 가이드 링크
├── src/
│   └── app.py                         # 샘플 Python 웹 앱 (의존성 포함)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml                 # DAST·AI 퍼징용 앱 기동
│
├── CLAUDE.md                          # 2단계: AI 규칙 내재화
├── .cursorrules                       # 2단계: Cursor 규칙
│
├── .gitleaks.toml                     # 3단계: 시크릿 탐지 설정
├── .grype.yaml                        # 3단계: SCA 임계값 설정
├── .semgrep.yml                       # 3단계: SAST 룰셋
│
├── renovate.json                      # 4단계: Renovate 자동 업데이트
│
├── k8s/
│   └── deployment.yaml                # IaC 보안 스캔 대상 샘플 (Checkov)
│
├── scripts/
│   └── ai-fuzz.py                     # AI 퍼징 실행 스크립트
│
└── .github/
    ├── dependabot.yml                 # 4단계: Dependabot 설정
    └── workflows/
        ├── secret-detection.yml       # 3단계: Gitleaks
        ├── sast.yml                   # 3단계: Semgrep
        ├── codeql.yml                 # 3단계: CodeQL (PR + 주 1회)
        ├── oss-policy.yml             # 3단계: syft + grype + 라이선스
        ├── iac-security.yml           # 3단계: Checkov (Dockerfile·K8s)
        ├── container-security.yml     # 3단계: Trivy
        ├── ai-review.yml              # 4단계: findings-driven AI 리뷰 (ANTHROPIC_API_KEY 등록 시 자동 활성화)
        ├── ai-fuzzing.yml             # 4단계: AI 퍼징 (주 1회 + Push)
        └── dast.yml                   # 5단계: OWASP ZAP (Push to main)
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
