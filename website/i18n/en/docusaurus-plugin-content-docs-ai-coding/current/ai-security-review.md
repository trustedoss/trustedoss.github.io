---
id: ai-security-review
title: AI Security Code Review
sidebar_label: AI Security Review
sidebar_position: 7
---

# AI Security Code Review (Stage 4)

## Why Findings-Driven?

Sending the entire codebase to AI causes high token costs and excessive noise.
It is more efficient for **Stage 3 tools (Semgrep and grype) to narrow candidates first, and AI to focus only on those results**.

```
[Step 3] Semgrep · grype → findings.json
                                ↓
[Step 4] AI: code context + findings → validation, deep interpretation, and related finding discovery
                                ↓
                       PR comment (does not block build)
```

| Tool             | Detection Method           | Strengths                                                   | Limitations                               |
| ---------------- | -------------------------- | ----------------------------------------------------------- | ----------------------------------------- |
| Gitleaks         | Regex pattern matching     | Hardcoded secrets                                           | Cannot detect secrets hidden in variables |
| grype            | CVE DB matching            | Known vulnerabilities                                       | Cannot detect 0-day or logic bugs         |
| Semgrep          | Code pattern rules         | Common vulnerability patterns                               | Ignores business logic context            |
| **AI (Stage 4)** | Natural language reasoning | FP classification, context understanding, related discovery | High FP rate, API costs                   |

:::warning Operate as reporting, not build blocking
AI review has a high FP (false positive) rate. Use it only for PR comments or Security tab reporting,
and avoid using it to force build failures.
:::

---

## GitHub Actions Configuration Example

This workflow collects findings from Stage 3 tools, then has AI analyze them with code context.

```yaml
# .github/workflows/ai-review.yml
name: AI Security Review (Findings-Driven)

on:
  pull_request:
    branches: [main]

permissions:
  pull-requests: write

jobs:
  ai-review:
    if: ${{ secrets.ANTHROPIC_API_KEY != '' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # Step 3 Tools collect results (light rerun)
      - name: Run Semgrep (SARIF)
        run: |
          pip install semgrep -q
          semgrep --config=auto --sarif-output=semgrep.sarif \
            --include='*.py' --include='*.js' --include='*.ts' \
            --include='*.go' --include='*.java' || true

      - name: Run grype (JSON)
        run: |
          curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh \
            | sh -s -- -b /usr/local/bin
          grype dir:. -o json > grype.json || true

      # AI: findings + code context → validation and interpretation
      - name: AI Findings Analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          pip install anthropic -q
          python3 << 'PYEOF'
          import json, pathlib, anthropic, sys

          # Semgrep findings parse
          semgrep_issues = []
          try:
              sarif = json.loads(pathlib.Path("semgrep.sarif").read_text())
              for run in sarif.get("runs", []):
                  for result in run.get("results", []):
                      loc = result.get("locations", [{}])[0]
                      region = loc.get("physicalLocation", {}).get("region", {})
                      uri = loc.get("physicalLocation", {}).get("artifactLocation", {}).get("uri", "")
                      line = region.get("startLine", 0)
                      rule_id = result.get("ruleId", "")
                      msg = result.get("message", {}).get("text", "")
                      # extract line context (±5 lines)
                      ctx = ""
                      try:
                          lines = pathlib.Path(uri).read_text().splitlines()
                          start = max(0, line - 6)
                          end = min(len(lines), line + 5)
                          ctx = "\n".join(f"{i+1}: {l}" for i, l in enumerate(lines[start:end], start=start))
                      except Exception:
                          pass
                      semgrep_issues.append({"rule": rule_id, "file": uri, "line": line, "msg": msg, "ctx": ctx})
          except Exception:
              pass

          # grype CVE findings parse (High/Criticalonly)
          grype_issues = []
          try:
              grype = json.loads(pathlib.Path("grype.json").read_text())
              for match in grype.get("matches", []):
                  sev = match.get("vulnerability", {}).get("severity", "")
                  if sev in ("High", "Critical"):
                      grype_issues.append({
                          "cve": match["vulnerability"]["id"],
                          "pkg": match["artifact"]["name"],
                          "ver": match["artifact"]["version"],
                          "severity": sev,
                          "fixed": match["vulnerability"].get("fix", {}).get("versions", []),
                      })
          except Exception:
              pass

          if not semgrep_issues and not grype_issues:
              pathlib.Path("review_result.txt").write_text("PASS")
              print("No detected findings — skip AI analysis")
              sys.exit(0)

          # assemble prompt (limited to top 10)
          semgrep_block = "\n".join(
              f"[Semgrep #{i+1}] {x['rule']} @ {x['file']}:{x['line']}\nMessage: {x['msg']}\nCode:\n{x['ctx']}"
              for i, x in enumerate(semgrep_issues[:8])
          )
          grype_block = "\n".join(
              f"[grype] {x['cve']} — {x['pkg']}@{x['ver']} ({x['severity']}) → Fixed version: {x['fixed']}"
              for x in grype_issues[:5]
          )

          prompt = f"""Below are detected results from static analysis tools (Semgrep) and SCA tools (grype).
Assess each item using the format below.

Assessment format:
- **[Item number]** Real vulnerability (TP) or false positive (FP) | Risk: High/Medium/Low | 1-2 sentence rationale
- TPif TP: add one-line real exploit scenario
- For grype CVEs, determine whether the package is used in actual runtime paths

---
{semgrep_block}

{grype_block}
---

detected If there are no findings, output PASS."""

          client = anthropic.Anthropic()
          response = client.messages.create(
              model="claude-opus-4-7",
              max_tokens=1500,
              messages=[{"role": "user", "content": prompt}]
          )
          result = response.content[0].text
          pathlib.Path("review_result.txt").write_text(result)
          print(result)
          PYEOF

      - name: Post PR comment
        uses: actions/github-script@v9
        with:
          script: |
            const fs = require('fs');
            let result;
            try { result = fs.readFileSync('review_result.txt', 'utf8'); }
            catch { result = 'PASS'; }
            if (result.trim() === 'PASS') return;
            const total = (result.match(/\[Semgrep|grype/g) || []).length;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: [
                '## 🔍 AI Security Review (Findings-Driven)',
                '',
                '> Step 3 Tools(Semgrep·grype) detected Results validated and interpreted by AI.',
                '> False positives are possible; evaluate with context. This is not a build-blocking criterion.',
                '',
                result
              ].join('\n')
            });
```

---

## Workflow Execution Flow

```
PR opened
  │
  ├─ [Step 3] Semgrep → semgrep.sarif  ─┐
  └─ [Step 3] grype   → grype.json     ─┤
                                        ↓
                            findings parse + code context extract
                                        ↓
                            Claude API (top 13 findings only)
                                        ↓
                            PR comment: TP/FP assessment + risk level
```

**Token-saving points:**

- Send only the top 8 Semgrep findings with ±5 lines of context each
- Include only grype Critical/High findings (exclude Medium/Low)
- Skip API calls entirely when there are no findings

---

## How to Enable

1. Add `ANTHROPIC_API_KEY` to GitHub Secrets
2. The workflow condition `if: ${{ secrets.ANTHROPIC_API_KEY != '' }}` is enabled automatically

---

## Notes

**External transfer of sensitive code**

Code snippets flagged by Semgrep are sent to Anthropic servers. If internal security policy restricts external API transfer, policy review is required before adoption. Replacing with an on-prem LLM (such as Ollama) can also be considered.

**FP rate and cost**

LLM-based judgments frequently produce false positives. Control cost by limiting findings (`[:8]`, `[:5]`) and estimate monthly API usage in advance based on team size and PR frequency.

---

## Learn More

- [5-Stage Strategy](./strategy) — Full stage structure and AI defense layer positioning
- [DevSecOps — SAST](/devsecops/sast) — Rule-based static analysis (Semgrep · CodeQL)
- [DevSecOps — Organization-wide Pipeline Design](/devsecops/pipeline-design)
