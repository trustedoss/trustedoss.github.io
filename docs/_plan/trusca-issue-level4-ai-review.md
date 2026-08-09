# TRUSCA 전달 이슈 — 4단계(AI 방어 레이어) 추가 제안

**상태**: 초안 — TRUSCA 저장소(github.com/trustedoss/trusca)에 이슈로 등록할 내용
**작성**: 2026-08-09
**근거**: trustedoss.github.io 의 AI 코딩 거버넌스 5단계 모델과 TRUSCA 현행 워크플로우 대조

---

## 배경 (전달자용 메모)

가이드의 5단계 모델을 기준으로 TRUSCA 저장소를 확인한 결과, **3단계와 5단계는 갖춰져 있고
4단계만 비어 있다.**

| 단계                  | 상태            | 근거                                                                                                     |
| --------------------- | --------------- | -------------------------------------------------------------------------------------------------------- |
| 3단계 CI/CD 자동 차단 | 다섯 영역 중 넷 | secret-scan(gitleaks) · sast(bandit·semgrep) · codeql · sca-self(cdxgen+Trivy) · ci 의 image-scan(Trivy) |
| 4단계 AI 방어 레이어  | **없음**        | AI 리뷰 워크플로우 부재                                                                                  |
| 5단계 지속 모니터링   | 갖춤            | dependabot(5개 생태계) · sca-self(매일 07:00) · dogfood-scan · demo-health-canary(30분). DAST 없음       |

가이드 사이트는 3단계와 5단계의 실전 사례로 TRUSCA 워크플로우를 링크하고 있다. 4단계만
링크할 곳이 없어 "공개 사례가 드물다"고 적어 두었다.

핵심 요구사항은 **Anthropic API 키가 준비되지 않아도 저장소에 들어갈 수 있어야 한다**는 것이다.
아래 본문에 그 방법을 두 가지로 정리했고 첫 번째를 권장했다.

**전달 방법**: 아래 구분선 사이의 내용을 그대로 복사해 이슈 본문에 붙여넣는다.
라벨은 `enhancement` 와 보안 관련 라벨이 맞다.

---

<!-- ===== 여기서부터 이슈 본문 ===== -->

## Add a level 4 findings-driven AI review workflow

### Context

Measured against the five-level AI coding governance model published at
https://trustedoss.github.io/ai-coding/strategy, this repository already runs
levels 3 and 5:

- **Level 3** — `secret-scan.yml` (gitleaks), `sast.yml` (bandit + semgrep),
  `codeql.yml`, `sca-self.yml` (cdxgen + Trivy), and the `image-scan` job in
  `ci.yml` (Trivy). Four of the five areas; IaC has nothing to scan here.
- **Level 5** — `dependabot.yml` across five ecosystems, `sca-self.yml` nightly,
  `dogfood-scan.yml`, and `demo-health-canary.yml` every 30 minutes.

Level 4 is the gap. The guide site links this repository as the working example
for levels 3 and 5, and notes that public examples of level 4 are rare — which
is precisely why adding one here would be useful.

### What level 4 adds

Level 3 tools match known patterns accurately. Code written by an AI can produce
shapes no rule covers, and those pass. Level 4 answers that with a
findings-driven review: the level 3 tools narrow the candidates first, and a
model judges only what they flagged.

Concretely, for each PR:

1. Parse `semgrep.sarif` and `grype.json` (already produced by existing jobs)
2. Send only the flagged findings plus ±5 lines of surrounding code
3. Get back per-finding verdicts — true positive or false positive, risk level,
   and an exploitation path when real
4. Post the result as a PR comment

**This must not gate the build.** LLM verdicts carry a high false positive rate;
the value is in triage, not enforcement. `secret-scan` and `sast` should remain
the blocking checks.

A working implementation — the full workflow file, the parsing code, and a
worked example of what goes to the model and what comes back — is at
https://trustedoss.github.io/ai-coding/ai-security-review

### Handling the API key

The workflow needs `ANTHROPIC_API_KEY` in repository secrets. If that is not
available yet, there are two ways to land this without breaking anything.

**Option A — merge the workflow with a key guard (recommended).**

The secrets context is not available in a job-level `if`, so move the check to
`env` and gate each step. In outline:

    jobs:
      ai-review:
        runs-on: ubuntu-latest
        env:
          HAS_ANTHROPIC_KEY: ${{ secrets.ANTHROPIC_API_KEY != '' }}
        steps:
          - uses: actions/checkout@v4
          - name: Run semgrep
            if: env.HAS_ANTHROPIC_KEY == 'true'
            ...

With no key present every step is skipped, so the job succeeds and costs
nothing. Registering the secret later turns it on with no code change.

This is preferable to commenting the file out: the YAML stays valid and is
checked by every workflow lint, so a syntax error surfaces now rather than on
the day someone enables it.

**Option B — commit it commented out.**

If policy requires that no workflow referencing an external API exists in the
tree at all, commit the file fully commented, with a header stating what needs
to happen to enable it:

    # Level 4 — findings-driven AI review.
    # Disabled pending an ANTHROPIC_API_KEY repository secret.
    #
    # To enable:
    #   1. Add ANTHROPIC_API_KEY to repository secrets
    #   2. Uncomment everything below
    #   3. Confirm the first run posts a PR comment and does not fail the build
    #
    # name: AI Security Review (Findings-Driven)
    # ...

Either way the prerequisite is the same and worth tracking separately: the API
key needs to be provisioned and a cost owner agreed.

### Cost control

Cost scales with findings volume, not repository size. The reference
implementation caps it:

- Top 8 semgrep findings, ±5 lines of context each
- grype Critical and High only
- No findings means no API call at all

Measuring the false positive rate over the first few weeks before deciding
whether to keep it is the sensible order.

### Alternative for restricted environments

Where sending code to an external API is not acceptable, the same design works
against a self-hosted model (Ollama and similar) — only the client call changes.
Worth noting since air-gapped deployment is a stated use case for this project.

### Suggested acceptance criteria

- [ ] `ai-review.yml` present and valid, skipping cleanly when no key is set
- [ ] With a key set: posts a PR comment, never fails the build
- [ ] Findings caps in place (8 semgrep / 5 grype)
- [ ] README or docs note that level 4 is now covered

<!-- ===== 이슈 본문 끝 ===== -->

---

## 반영 후 할 일

이 제안이 받아들여지면 가이드의 4단계에도 실전 사례 링크를 붙일 수 있다. 현재
`website/ai-coding/strategy.md` 4단계 절에는 "공개 사례가 드물다"고 적혀 있고,
영어판도 같은 문구다. 두 곳을 함께 고쳐야 한다.
