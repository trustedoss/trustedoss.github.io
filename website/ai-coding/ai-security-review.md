---
id: ai-security-review
title: AI 보안 코드 리뷰
sidebar_label: AI 보안 리뷰
sidebar_position: 7
---

# AI 보안 코드 리뷰

## 기존 도구와의 역할 분담

Gitleaks · grype · Semgrep 등 기존 CI/CD 도구는 **알려진 패턴**을 기계적으로 탐지합니다.
AI 코드 리뷰는 이 도구들이 놓치는 **의미론적 취약점**을 보완하는 선택 옵션입니다.

| 도구             | 탐지 방식        | 강점                | 한계                      |
| ---------------- | ---------------- | ------------------- | ------------------------- |
| Gitleaks         | 정규식 패턴 매칭 | 하드코딩 시크릿     | 변수에 담긴 시크릿 미탐지 |
| grype            | CVE DB 대조      | 알려진 취약점       | 0-day·논리 버그 탐지 불가 |
| Semgrep          | 코드 패턴 규칙   | 일반적 취약 패턴    | 비즈니스 로직 맥락 무시   |
| **AI 코드 리뷰** | 자연어 추론      | 논리 흐름·맥락 이해 | FP율 높음, 비용 발생      |

:::warning 빌드 차단보다 리포트 용도로 사용하세요
AI 리뷰는 FP(오탐)율이 높습니다. 빌드를 강제로 실패시키는 용도보다
PR 코멘트 또는 리포트 생성 용도로 운영하는 것이 현실적입니다.
:::

---

## GitHub Actions 구성 예시

PR diff를 Claude API에 전달해 보안 검토 결과를 PR 코멘트로 게시하는 워크플로우입니다.

````yaml
# .github/workflows/ai-security-review.yml
name: AI Security Review

on:
  pull_request:
    branches: [main, develop]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get PR diff
        id: diff
        run: |
          git diff origin/${{ github.base_ref }}...HEAD \
            -- '*.py' '*.js' '*.ts' '*.go' '*.java' '*.rb' \
            | head -c 8000 > diff.txt
          echo "size=$(wc -c < diff.txt)" >> $GITHUB_OUTPUT

      - name: AI Security Review
        if: steps.diff.outputs.size > 0
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          pip install anthropic -q
          python3 << 'EOF'
          import anthropic, pathlib, os

          diff = pathlib.Path("diff.txt").read_text()
          client = anthropic.Anthropic()

          response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=1024,
            messages=[{
              "role": "user",
              "content": (
                "아래 코드 변경에서 보안 취약점을 검토하라.\n"
                "탐지 대상: SQL 인젝션, 인증·인가 우회, 민감 정보 노출, "
                "입력값 검증 누락, 안전하지 않은 역직렬화.\n"
                "발견 시: 파일명·라인·위험도(High/Medium)·설명 형식으로 출력.\n"
                "발견 없으면: 'PASS' 한 줄만 출력.\n\n"
                f"```diff\n{diff}\n```"
              )
            }]
          )

          result = response.content[0].text
          pathlib.Path("review_result.txt").write_text(result)
          print(result)
          EOF

      - name: Post PR comment
        if: steps.diff.outputs.size > 0
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const result = fs.readFileSync('review_result.txt', 'utf8');
            if (result.trim() === 'PASS') return;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🔍 AI 보안 코드 리뷰\n\n${result}\n\n> 이 리뷰는 AI가 생성했습니다. 오탐 가능성이 있으니 맥락을 고려해 판단하세요.`
            });
````

---

## 주의사항

**FP율과 비용**

LLM 기반 코드 리뷰는 오탐(False Positive)이 잦습니다. 팀 규모와 PR 빈도에 따라 월 API 비용을 사전에 추산하고, `head -c 8000` 같은 토큰 절약 장치를 반드시 적용하세요.

**민감 코드의 외부 전송**

PR diff가 Anthropic 서버로 전송됩니다. 사내 보안 정책상 외부 API 전송이 제한된 경우 도입 전 정책 검토가 필요합니다. 온프레미스 LLM(Ollama 등)으로 대체하는 방안도 고려할 수 있습니다.

**컨텍스트 창 한계**

파일 전체가 아닌 PR diff 단위로만 분석합니다. 여러 파일에 걸친 복잡한 취약점 흐름은 탐지하기 어렵습니다.

---

## 더 알아보기

- [DevSecOps — SAST](/devsecops/sast) — 규칙 기반 정적 분석 (Semgrep · CodeQL)
- [DevSecOps — 전사 파이프라인 설계](/devsecops/pipeline-design)
