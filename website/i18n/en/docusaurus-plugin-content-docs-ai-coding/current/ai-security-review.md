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
[Stage 3] Semgrep · grype → findings.json
                                ↓
[Stage 4] AI: code context + findings → validation, deep interpretation, and related finding discovery
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
    runs-on: ubuntu-latest
    # The secrets context is not available in a job-level if; move it to env and check per step.
    env:
      HAS_ANTHROPIC_KEY: ${{ secrets.ANTHROPIC_API_KEY != '' }}
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0

      # Collect Stage 3 tool results (light rerun) — skipped entirely when the key is missing
      - name: Run Semgrep (SARIF)
        if: env.HAS_ANTHROPIC_KEY == 'true'
        run: |
          pip install semgrep -q
          semgrep --config=auto --sarif-output=semgrep.sarif \
            --include='*.py' --include='*.js' --include='*.ts' \
            --include='*.go' --include='*.java' || true

      - name: Run grype (JSON)
        if: env.HAS_ANTHROPIC_KEY == 'true'
        run: |
          curl -sSfL https://get.anchore.io/grype \
            | sh -s -- -b /usr/local/bin
          grype dir:. -o json > grype.json || true

      # AI: findings + code context → validation and interpretation
      - name: AI Findings Analysis
        if: env.HAS_ANTHROPIC_KEY == 'true'
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

          # grype CVE findings parse (High/Critical only)
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

          # assemble prompt (limited to top 13 — 8 Semgrep + 5 grype)
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
- If TP: add a one-line real exploit scenario
- For grype CVEs, determine whether the package is used in actual runtime paths

---
{semgrep_block}

{grype_block}
---

If there are no detected items, output PASS."""

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
        if: env.HAS_ANTHROPIC_KEY == 'true'
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
                '> AI validates and interprets the detection results from Stage 3 tools (Semgrep·grype).',
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
  ├─ [Stage 3] Semgrep → semgrep.sarif  ─┐
  └─ [Stage 3] grype   → grype.json     ─┤
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

## What Actually Goes Over the Wire

Here is one run of the workflow above, showing what goes in and what comes back.
The values below are illustrative; real ones vary per project.

### 1. Raw tool output

Semgrep emits SARIF and grype emits JSON. Neither is suitable to send as-is — both are large and
carry fields the model does not need.

```json
// semgrep.sarif (excerpt) — the real file also carries rule definitions, tags, and fix suggestions
{
  "runs": [
    {
      "results": [
        {
          "ruleId": "python.lang.security.audit.formatted-sql-query.formatted-sql-query",
          "message": {
            "text": "Detected possible formatted SQL query. Use parameterized queries instead."
          },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {"uri": "app/db.py"},
                "region": {"startLine": 42}
              }
            }
          ]
        }
      ]
    }
  ]
}
```

```json
// grype.json (excerpt)
{
  "matches": [
    {
      "vulnerability": {
        "id": "CVE-2021-44228",
        "severity": "Critical",
        "fix": {"versions": ["2.15.0"]}
      },
      "artifact": {"name": "log4j-core", "version": "2.14.1"}
    }
  ]
}
```

### 2. The prompt sent to the Claude API

The parsing step pulls just the fields it needs and reads ±5 lines around each hit for context.
This is the entire payload.

```text
The following are findings from a static analysis tool (Semgrep) and an SCA tool (grype).
Judge each item in the format below.

Format:
- **[item]** true positive (TP) or false positive (FP) | risk: High/Medium/Low | 1-2 sentences of reasoning
- If TP: add a one-line exploitation scenario
- For grype CVEs, judge whether the package is actually reachable in the execution path

---
[Semgrep #1] python.lang.security.audit.formatted-sql-query.formatted-sql-query @ app/db.py:42
Message: Detected possible formatted SQL query. Use parameterized queries instead.
Code:
38:     def find_user(keyword):
39:         conn = get_connection()
40:         cur = conn.cursor()
41:         # the search term goes straight into the string
42:         cur.execute(f"SELECT * FROM users WHERE name LIKE '%{keyword}%'")
43:         return cur.fetchall()

[Semgrep #2] python.lang.security.audit.subprocess-shell-true.subprocess-shell-true @ scripts/deploy.py:18
Message: Detected subprocess function with shell=True.
Code:
16:     RELEASE_DIR = "/opt/app/release"
17:
18:     subprocess.run(f"tar -xzf {RELEASE_DIR}/build.tar.gz", shell=True)

[grype] CVE-2021-44228 — log4j-core@2.14.1 (Critical) → fixed in: ['2.15.0']
---

Output PASS if there are no findings.
```

Not the repository — **only the three flagged items and a few lines around each**. That is the
core of the findings-driven approach.

### 3. What Claude returns

```text
- **[Semgrep #1]** true positive (TP) | risk: High | The user-supplied keyword is interpolated
  directly into SQL via an f-string. With no parameter binding, an input that closes the quote can
  change the query structure.
  Exploitation: searching for `%' OR '1'='1` returns every user record.

- **[Semgrep #2]** false positive (FP) | risk: Low | shell=True is used, but the only value in the
  command string is the module constant RELEASE_DIR, which no external input reaches. Should that
  path ever become an argument it would turn into an injection point, so shell=False with list
  arguments is still the safer form.

- **[grype CVE-2021-44228]** true positive (TP) | risk: High | log4j-core 2.14.1 is within the
  Log4Shell affected range; if user input reaches a logging call, this leads to remote code
  execution. Upgrade to 2.15.0 or later. Even when the application never calls the package
  directly, frameworks often use it internally, so ruling it out requires checking the execution
  path.
```

This is where level 4 diverges from level 3. Semgrep flagged both findings at the same strength;
the model separated one as real and one as a false positive, and still attached a conditional
improvement to the false positive.

### 4. How it appears as a PR comment

The judgment becomes the comment body verbatim.

```markdown
## 🔍 AI Security Review (Findings-Driven)

The AI verified and interpreted the level 3 tool findings (Semgrep, grype).
False positives are possible, so weigh the context. This is not a build gate.

- **[Semgrep #1]** true positive (TP) | risk: High | ...
```

The build does not fail. A developer reads the comment and decides.

---

## How to Enable

1. Add `ANTHROPIC_API_KEY` to GitHub Secrets
2. The workflow moves the key check to `env` and gates each step, so registering the key enables it automatically (steps are skipped when the key is missing)

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
