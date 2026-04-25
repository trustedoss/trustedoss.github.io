---
id: ai-security-review
title: AI 보안 코드 리뷰
sidebar_label: AI 보안 리뷰
sidebar_position: 7
---

# AI 보안 코드 리뷰 (4단계)

## 왜 Findings-Driven인가

전체 코드를 AI에게 보내는 방식은 토큰 비용이 크고 노이즈가 많습니다.
**3단계 도구(Semgrep·grype)가 먼저 후보를 추리고, AI는 그 결과에만 집중**하는 방식이 효율적입니다.

```
[3단계] Semgrep · grype → findings.json
                                ↓
[4단계] AI: 코드 컨텍스트 + findings → 검증·심층 해석·연관 발견
                                ↓
                       PR 코멘트 (빌드 차단 아님)
```

| 도구           | 탐지 방식        | 강점                        | 한계                      |
| -------------- | ---------------- | --------------------------- | ------------------------- |
| Gitleaks       | 정규식 패턴 매칭 | 하드코딩 시크릿             | 변수에 담긴 시크릿 미탐지 |
| grype          | CVE DB 대조      | 알려진 취약점               | 0-day·논리 버그 탐지 불가 |
| Semgrep        | 코드 패턴 규칙   | 일반적 취약 패턴            | 비즈니스 로직 맥락 무시   |
| **AI (4단계)** | 자연어 추론      | FP 판정·맥락 이해·연관 발견 | FP율 높음, API 비용 발생  |

:::warning 빌드 차단이 아닌 리포트 용도로 운영하세요
AI 리뷰는 FP(오탐)율이 높습니다. PR 코멘트 또는 Security 탭 리포트 생성 용도로만 사용하고,
빌드를 강제로 실패시키는 용도로는 쓰지 않는 것을 권장합니다.
:::

---

## GitHub Actions 구성 예시

3단계 도구의 findings를 수집한 뒤, AI가 코드 컨텍스트와 함께 분석하는 워크플로우입니다.

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

## 워크플로우 동작 원리

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

**토큰 절약 포인트:**

- Semgrep findings 상위 8개 + 각 ±5줄 컨텍스트만 전송
- grype Critical/High만 (Medium·Low 제외)
- findings 없으면 API 호출 자체를 건너뜀

---

## 활성화 방법

1. `ANTHROPIC_API_KEY`를 GitHub Secrets에 등록
2. 워크플로우의 `if: ${{ secrets.ANTHROPIC_API_KEY != '' }}` 조건이 자동으로 활성화

---

## 주의사항

**민감 코드의 외부 전송**

Semgrep이 플래그한 코드 조각이 Anthropic 서버로 전송됩니다. 사내 보안 정책상 외부 API 전송이 제한된 경우 도입 전 정책 검토가 필요합니다. 온프레미스 LLM(Ollama 등)으로 대체하는 방안도 고려할 수 있습니다.

**FP율과 비용**

LLM 기반 판정은 오탐이 잦습니다. findings 수를 제한(`[:8]`, `[:5]`)해 비용을 통제하고, 팀 규모와 PR 빈도에 따라 월 API 비용을 사전에 추산하세요.

---

## 더 알아보기

- [5단계 전략](./strategy) — 전체 단계 구조와 AI 방어 레이어 포지셔닝
- [DevSecOps — SAST](/devsecops/sast) — 규칙 기반 정적 분석 (Semgrep · CodeQL)
- [DevSecOps — 전사 파이프라인 설계](/devsecops/pipeline-design)
