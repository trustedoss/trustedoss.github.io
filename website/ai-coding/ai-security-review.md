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
    runs-on: ubuntu-latest
    # job 수준 if 에서는 secrets 컨텍스트를 쓸 수 없어 env 로 옮겨 step 에서 검사합니다.
    env:
      HAS_ANTHROPIC_KEY: ${{ secrets.ANTHROPIC_API_KEY != '' }}
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0

      # 3단계 도구 결과 수집 (경량 재실행) — 키가 없으면 전체 건너뜀
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

      # AI: findings + 코드 컨텍스트 → 검증·해석
      - name: AI Findings Analysis
        if: env.HAS_ANTHROPIC_KEY == 'true'
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

          # 프롬프트 조립 (상위 13개로 제한 — Semgrep 8개 + grype 5개)
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

## 실제로 오가는 데이터

위 워크플로우에서 무엇이 입력되고 무엇이 나오는지 한 번의 실행을 따라가 봅니다.
아래는 이해를 돕기 위한 예시이며, 실제 값은 프로젝트마다 다릅니다.

### 1. 도구가 낸 원본

Semgrep은 SARIF로, grype는 JSON으로 결과를 냅니다. 둘 다 그대로는 AI에게 보내기에 크고
불필요한 필드가 많습니다.

```json
// semgrep.sarif (발췌) — 실제로는 룰 정의·태그·수정 제안까지 포함돼 훨씬 깁니다
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
// grype.json (발췌)
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

### 2. Claude API 로 전달되는 프롬프트

파싱 단계가 위 원본에서 필요한 필드만 뽑고, 해당 파일에서 ±5줄을 읽어 컨텍스트로 붙입니다.
실제로 전송되는 것은 이만큼입니다.

```text
아래는 정적 분석 도구(Semgrep)와 SCA 도구(grype)의 탐지 결과다.
각 항목에 대해 아래 형식으로 판정하라.

판정 형식:
- **[항목번호]** 실제취약점(TP) 또는 오탐(FP) | 위험도: High/Medium/Low | 판정 근거 1~2문장
- TP일 경우: 실제 익스플로잇 시나리오 1줄 추가
- grype CVE는 해당 패키지가 실제 코드 실행 경로에서 사용되는지 판단

---
[Semgrep #1] python.lang.security.audit.formatted-sql-query.formatted-sql-query @ app/db.py:42
메시지: Detected possible formatted SQL query. Use parameterized queries instead.
코드:
38:     def find_user(keyword):
39:         conn = get_connection()
40:         cur = conn.cursor()
41:         # 검색어를 그대로 문자열에 넣는다
42:         cur.execute(f"SELECT * FROM users WHERE name LIKE '%{keyword}%'")
43:         return cur.fetchall()

[Semgrep #2] python.lang.security.audit.subprocess-shell-true.subprocess-shell-true @ scripts/deploy.py:18
메시지: Detected subprocess function with shell=True.
코드:
16:     RELEASE_DIR = "/opt/app/release"
17:
18:     subprocess.run(f"tar -xzf {RELEASE_DIR}/build.tar.gz", shell=True)

[grype] CVE-2021-44228 — log4j-core@2.14.1 (Critical) → 수정버전: ['2.15.0']
---

탐지 항목이 없으면 PASS를 출력하라.
```

전체 저장소가 아니라 **플래그된 3건과 그 주변 몇 줄만** 나갑니다. 이것이 findings-driven 방식의
핵심입니다.

### 3. Claude 가 낸 판정

```text
- **[Semgrep #1]** 실제취약점(TP) | 위험도: High | 사용자 입력 keyword 가 f-string 으로 SQL 에
  직접 삽입됩니다. 파라미터 바인딩이 없어 인용부호를 닫는 입력으로 쿼리 구조를 바꿀 수 있습니다.
  익스플로잇: 검색어에 `%' OR '1'='1` 를 넣으면 전체 사용자 목록이 반환됩니다.

- **[Semgrep #2]** 오탐(FP) | 위험도: Low | shell=True 가 쓰였지만 명령 문자열에 들어가는 값이
  모듈 상수 RELEASE_DIR 뿐이고 외부 입력이 닿지 않습니다. 다만 이 경로가 향후 인자로 바뀌면
  주입 지점이 되므로 shell=False 와 리스트 인자로 바꾸는 편이 안전합니다.

- **[grype CVE-2021-44228]** 실제취약점(TP) | 위험도: High | log4j-core 2.14.1 은 Log4Shell 영향
  버전이며, 로깅 호출에 사용자 입력이 들어가는 경로가 있으면 원격 코드 실행으로 이어집니다.
  2.15.0 이상으로 올리십시오. 애플리케이션이 이 패키지를 직접 호출하지 않더라도 프레임워크가
  내부적으로 사용하는 경우가 많아 배제 판정에는 실행 경로 확인이 필요합니다.
```

여기서 4단계가 3단계와 갈리는 지점이 드러납니다. Semgrep 은 두 건을 같은 강도로 플래그했지만
AI 는 하나를 실제 취약점으로, 다른 하나를 오탐으로 갈랐고, 오탐에도 조건부 개선안을 붙였습니다.

### 4. PR 코멘트로 게시되는 모습

위 판정이 그대로 코멘트 본문이 됩니다.

```markdown
## 🔍 AI 보안 리뷰 (Findings-Driven)

3단계 도구(Semgrep·grype) 탐지 결과를 AI가 검증·해석한 결과입니다.
오탐 가능성이 있으니 맥락을 고려해 판단하세요. 빌드 차단 기준이 아닙니다.

- **[Semgrep #1]** 실제취약점(TP) | 위험도: High | ...
```

빌드는 실패하지 않습니다. 개발자가 코멘트를 읽고 판단합니다.

---

## 활성화 방법

1. `ANTHROPIC_API_KEY`를 GitHub Secrets에 등록
2. 워크플로우가 키 존재 여부를 `env`로 옮겨 각 단계에서 확인하므로, 키를 등록하면 자동으로 활성화 (키가 없으면 각 단계를 건너뜀)

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
