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
[3단계] Semgrep · grype → findings.json
                                ↓
[4단계] AI: 코드 컨텍스트 + findings → 검증·심층 해석·연관 발견
                                ↓
                       PR 코멘트 (빌드 차단 아님)
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

      # 3단계 도구 결과 수집 (경량 재실행)
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

      # AI: findings + 코드 컨텍스트 → 검증·해석
      - name: AI Findings Analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          pip install anthropic -q
          python3 << 'PYEOF'
          import json, pathlib, anthropic, sys

          # Semgrep findings 파싱
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
                      # 해당 라인 컨텍스트 추출 (±5줄)
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

          # grype CVE findings 파싱 (High/Critical만)
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
              print("탐지된 findings 없음 — AI 분석 건너뜀")
              sys.exit(0)

          # 프롬프트 조립 (상위 10개로 제한)
          semgrep_block = "\n".join(
              f"[Semgrep #{i+1}] {x['rule']} @ {x['file']}:{x['line']}\n메시지: {x['msg']}\n코드:\n{x['ctx']}"
              for i, x in enumerate(semgrep_issues[:8])
          )
          grype_block = "\n".join(
              f"[grype] {x['cve']} — {x['pkg']}@{x['ver']} ({x['severity']}) → 수정버전: {x['fixed']}"
              for x in grype_issues[:5]
          )

          prompt = f"""아래는 정적 분석 도구(Semgrep)와 SCA 도구(grype)의 탐지 결과다.
각 항목에 대해 아래 형식으로 판정하라.

판정 형식:
- **[항목번호]** 실제취약점(TP) 또는 오탐(FP) | 위험도: High/Medium/Low | 판정 근거 1~2문장
- TP일 경우: 실제 익스플로잇 시나리오 1줄 추가
- grype CVE는 해당 패키지가 실제 코드 실행 경로에서 사용되는지 판단

---
{semgrep_block}

{grype_block}
---

탐지 항목이 없으면 PASS를 출력하라."""

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
                '## 🔍 AI 보안 리뷰 (Findings-Driven)',
                '',
                '> 3단계 도구(Semgrep·grype) 탐지 결과를 AI가 검증·해석한 결과입니다.',
                '> 오탐 가능성이 있으니 맥락을 고려해 판단하세요. 빌드 차단 기준이 아닙니다.',
                '',
                result
              ].join('\n')
            });
```

---

## Workflow Execution Flow

```
PR 오픈
  │
  ├─ [3단계] Semgrep → semgrep.sarif  ─┐
  └─ [3단계] grype   → grype.json     ─┤
                                        ↓
                            findings 파싱 + 코드 컨텍스트 추출
                                        ↓
                            Claude API (상위 13개 findings만)
                                        ↓
                            PR 코멘트: TP/FP 판정 + 위험도
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
