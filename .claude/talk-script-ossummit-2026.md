# 슬라이드 구성안 + 발표 스크립트 — OSS Summit Korea 2026

**세션**: 2026-08-12(수) 13:35~14:15, Rose · 실질 35분(발표 30분 + Q&A 5분)
**형식**: 한국어 발표 + 영문 슬라이드
**구성 근거**: `.claude/talk-ossummit-korea-2026.md`

스크립트는 축자 대본이 아니다. **첫 문장·전환 문장·닫는 문장은 그대로 말할 수 있게** 적었고,
나머지는 말할 요점을 문장으로 적었다. 읽지 말고 눈으로 훑은 뒤 자기 말로 하는 것을 전제로 한다.

슬라이드 20장. 괄호 안 시간은 누적이 아니라 해당 구간의 길이다.

---

## 1. 타이틀 (0:00)

```
AI-Powered Open Source Risk Management
ISO Self-Certification Kit and 5-Level AI Coding Governance

Haksung Jang
SK Telecom · OpenChain Korea Work Group
```

인사와 소속을 한 문장으로 끝낸다. 소속 설명에 시간을 쓰지 않는다.

---

## 2. 문제 제기 ①: 사고는 계속 일어난다 (0:20 / 1분)

```
The supply chain keeps breaking

XZ Utils (2024)     backdoor planted in an upstream project
Log4Shell (2021)    one library, hundreds of millions of systems
```

점심 직후라 목차로 열지 않는다. 사례로 바로 들어간다.

말할 것:

- 두 사건 모두 "우리가 직접 만들지 않은 코드"가 원인이었다
- 공통점은 무엇이 들어 있는지 몰랐다는 것
- 그래서 규제가 SBOM을 요구하기 시작했다 — 다음 슬라이드로 넘어가는 다리

---

## 3. 문제 제기 ②: 요구 수준이 올라갔다 (1:20 / 1분)

```
The bar moved — twice, this year

EU CRA        reporting obligations start 2026-09-11
              full application 2027-12-11

CISA 2026     published 2026-07-29, replaces NTIA 2021
Minimum       + component hash      (was recommended)
Elements      + component license   (was optional)
              + SBOM tool name, generation context
              scope now includes AI software and SaaS
```

말할 것:

- 유럽연합 사이버 복원력법 보고 의무가 **한 달 뒤** 시작된다
- CISA 2026 최소 요소는 **2주 전** 발표됐다. NTIA 2021을 대체한다
- 컴포넌트 해시와 라이선스가 권고에서 필수로 올라갔다. 기존에 만들던 SBOM으로는 부족해진다

한 줄 덧붙임: 이 가이드는 CISA 2026 기준을 이미 반영했다.
(주의 — **가이드가 반영했다는 뜻이다.** 도구 구현 여부와 섞지 않는다.)

---

## 4. 문제 제기 ③: 그런데 만들지를 못한다 (2:20 / 1분)

```
But most suppliers still can't produce one

no source          binaries and firmware are what gets delivered
air-gapped         can't upload to a hosted service
no verdict         "does this meet the minimum elements?" — unanswered

Requirements went up. The means didn't.
```

**이 슬라이드가 발표 전체의 문제 정의다.** 천천히 말한다.

말할 것:

- 요구는 올라가는데 만들 수단이 따라가지 못한다
- 소스가 없는 납품물, 외부 서비스를 쓸 수 없는 폐쇄망, 충족 여부를 판정할 방법의 부재
- 여기에 AI 코딩이 위험을 하나 더 얹는다. 사람이 검토하지 않은 의존성이 들어온다

전환 문장:

```
이 두 문제 — 만들지 못하는 문제와 AI가 더한 위험 — 을 함께 다루는 것이
오늘 이야기입니다.
```

---

## 5. 전체 지도 (3:20 / 2분)

```
Trusted OSS — the map

  [ Governance ]        ISO/IEC 5230 & 18974 self-certification
                        9 agents → 24 artifacts → declaration

  [ AI Coding ]         5-level maturity model
                        rules → CI gates → AI defense → auto-remediation

  [ DevSecOps ]         (level 3 of the model above)

  ──────────────────────────────────────────────
  [ TRUSCA ]            what runs after the declaration

  CC BY 4.0 · trustedoss.github.io
```

말할 것:

- 이후 모든 슬라이드는 이 지도 위 어딘가다
- DevSecOps는 따로 떼어 설명하지 않는다. 5단계 모델의 3단계가 곧 DevSecOps다
- 아래 칸(TRUSCA)은 마지막에 다룬다. 왜 거기 있는지는 그때 설명한다

---

## 6. 축 A ①: 무엇을 만들어야 하는가 (5:20 / 1분)

```
What conformance actually requires

5230  policy · organization · process · BOM · notices · contribution
18974 policy · organization · SBOM · CVE tracking · response · records

Shared foundation is large.
Build one, and half of the other is already done.
```

말할 것:

- 두 표준은 별개가 아니다. 정책·조직·교육·SBOM이 공통 기반이다
- 따로 진행하면 같은 일을 두 번 한다

---

## 7. 축 A ②: Agent가 만든다 (6:20 / 1분)

```
9 agents → 24 artifacts

02 organization    role definition, RACI, appointment letter
03 policy          OSS policy, license allowlist
04 process         approval, distribution, vulnerability response, inquiry
05 SBOM            CycloneDX SBOM, license report, copyleft risk
05 vulnerability   CVE report, remediation plan
06 training        curriculum, completion tracker
07 conformance     gap analysis, declaration draft
```

산출물을 하나씩 읽지 않는다. 화면으로 넘기고 말로는 흐름만 말한다.

말할 것:

- 각 Agent가 회사 상황을 묻고 그 답으로 문서를 만든다. 템플릿을 채우는 게 아니라 답변에 따라 내용이 달라진다
- 마지막 Agent가 앞선 산출물을 전부 읽어 갭 분석과 선언문 초안을 만든다

---

## 8. 축 A ③: SBOM 생성의 간극 (7:20 / 1.5분)

```
The gap in the middle

source available   →  syft, cdxgen            ✓ solved
binary / firmware  →  ?
air-gapped         →  ?

BomLens (Apache-2.0)
  in    source · container · binary · firmware
  out   CycloneDX SBOM · NOTICE · risk report · ML-BOM
  runs  locally
```

4번 슬라이드에서 던진 문제를 여기서 받는다. **이 연결을 말로 명시한다.**

말할 것:

```
앞에서 공급사가 SBOM을 만들지 못한다고 했습니다. 그 이유가 여기 있습니다.
```

- 소스가 있는 프로젝트는 이미 해결돼 있다. syft와 cdxgen으로 된다
- 문제는 소스 없이 바이너리나 펌웨어만 있는 경우, 그리고 폐쇄망이다
- BomLens는 로컬에서 돌고 펌웨어와 바이너리를 입력으로 받는다. Apache-2.0으로 공개돼 있다
- 고지문과 위험 리포트까지 한 번에 나온다

**말하지 않을 것**: "최적의 도구". 비교 평가 없이 단정하면 근거를 요구받는다.
능력을 구체적으로 말하는 것으로 충분하다.

---

## 9. 축 A ④: 데모 (8:50 / 4.5분)

```
[ recorded demo ]
agents/03-policy-generator → output/policy/oss-policy.md
```

녹화본을 2배속으로 재생하고 말로 해설한다. 라이브 실행하지 않는다.

해설할 지점:

- Agent가 던지는 질문 — 회사 규모, 배포 여부, 라이선스 정책 수준
- 답변에 따라 결과가 달라지는 부분
- 생성된 정책 문서에 표준 조항 번호가 붙어 있다는 점
- 이 문서가 다음 Agent의 입력이 된다는 점

시간이 밀리면 여기서 조절한다. 재생을 멈추고 결과 화면으로 건너뛴다.

---

## 10. 축 A ⑤: 그래서 어떻게 선언하는가 (13:20 / 1분)

```
Declaring conformance

1  download the checklist   OpenChain-Project/Reference-Material
2  self-assess              yes/no against each item
3  apply for listing        openchainproject.org/get-started

No audit. No fee.
```

말할 것:

- 자체 인증이므로 외부 심사가 없다
- 체크리스트를 받아 스스로 점검하고 신청 폼을 낸다
- 앞에서 만든 갭 분석과 선언문 초안이 이 점검의 근거가 된다

---

## 11. 축 B ①: 자가진단 (14:20 / 4분)

```
Where is your team right now?

L1  prompt-dependent      policy lives in someone's memory
L2  rules internalized    CLAUDE.md, .cursor/rules, AGENTS.md
L3  CI/CD hard block      gitleaks · semgrep · grype · trivy · checkov
L4  AI-augmented defense  findings-driven review · AI fuzzing
L5  continuous            dependabot · renovate · DAST

                          entry cost:  L2 = 10 minutes
```

띄우고 **3초 침묵**한다. 거수를 요구하지 않는다. 스스로 찾게 둔다.

말할 것:

- 1단계는 정책이 개인의 기억에만 있는 상태다. 담당자가 바뀌면 사라진다
- 2단계는 그 정책을 파일로 저장소에 넣는 것이다. 비용이 들지 않고 10분이면 된다
- 3단계부터 진짜 차단이다. 규칙은 부탁이지 강제가 아니기 때문이다
- 시크릿 탐지를 첫날 넣고 SAST, SCA 순으로 올린다. 한꺼번에 넣으면 실패한다

전환 문장:

```
앞의 세 단계가 위험을 만들지 않게 하는 쪽이라면,
4단계부터는 이미 만들어진 위험을 찾아내는 쪽입니다.
```

---

## 12. 축 B ②: 4단계는 왜 필요한가 (18:20 / 1.5분)

```
Level 3 catches known patterns.
AI writes new ones.

  attacker with AI  →  novel pattern  →  no rule matches  →  passes

Level 4: answer AI with AI
```

말할 것:

- 3단계 도구는 알려진 패턴을 정확하게 잡는다. 그게 강점이자 한계다
- 공격자도 AI를 쓴다. 룰셋에 없는 형태가 나오면 통과한다
- 전체 코드를 AI에게 보내는 방식은 비용이 크고 노이즈가 많다. 그래서 findings-driven이다

---

## 13. 축 B ③: 무엇이 오가는가 (19:50 / 1.5분)

```
What actually goes to the model

  semgrep.sarif ─┐
  grype.json    ─┴→  parse  →  3 flagged items + ±5 lines each
                                        ↓
                              TP / FP · risk · exploit path
                                        ↓
                                   PR comment (not a gate)
```

이 페이지는 사이트에 실제 입출력 예시가 들어 있으니, 시간이 되면 화면으로 보여준다.

말할 것:

- 저장소 전체가 아니라 플래그된 항목과 주변 몇 줄만 나간다
- 같은 강도로 플래그된 두 건을 AI가 하나는 실제 취약점으로, 하나는 오탐으로 가른다. 이게 3단계와 갈리는 지점이다
- 빌드는 실패시키지 않는다. 오탐 비율이 높기 때문이다. PR 코멘트로만 남긴다

---

## 14. 축 B ④: 에이전트가 도구를 부른다 (21:20 / 1.5분)

```
Agents call tools. Tools are supply chain inputs.

npm postmark-mcp
  1.0.15   clean
  1.0.16+  hidden BCC — every outgoing mail copied to an external address
           (start version is the researcher's estimate)

Approving once at adoption does not catch this.
```

말할 것:

- MCP는 에이전트가 외부 도구를 호출하는 규약이다
- 이 패키지는 처음엔 정상이었다가 나중 버전에서 악성으로 바뀌었다
- 최초 승인만으로는 막지 못한다. 버전 고정과 변경 추적이 필요한 이유다

**사실 경계 주의**: 악성 시작 버전은 추정이고, 공식 저장소와의 연관은 확인되지 않았다.
단정해서 말하지 않는다.

---

## 15. 축 B ⑤: 여섯 가지 통제 (22:50 / 1.5분)

```
Six controls for agent tooling

1  server allowlist          5  human approval + audit log
2  least privilege           6  egress path review   ← new
3  description review
4  version pinning

Source tiers: public releases need full review.
              vendor and in-house servers do not.
```

말할 것:

- 여섯 번째가 앞의 사례에서 나온 것이다. 도입 전에 어떤 외부 엔드포인트로 무엇이 나가는지 판정한다
- 모든 서버를 같은 강도로 심사하면 운영이 안 된다. 출처에 따라 나눈다
- 호스팅 플랫폼을 경유한다면 그 플랫폼도 심사 대상이다

전환 문장:

```
여기까지가 체계를 세우고 위험을 막는 이야기입니다.
그런데 선언하고 나면 끝일까요?
```

---

## 16. TRUSCA ①: 선언 다음에 오는 것 (24:20 / 2분)

```
The declaration is not the finish line

18974 asks for continuous operation
  · vulnerability DB refreshed weekly
  · VEX judgments kept current
  · license policy enforced on every build

This is where most teams stop — at the price of a commercial SCA.
```

말할 것:

- 키트는 체계와 산출물까지 만들어 준다. 거기까지다
- 18974가 요구하는 것은 지속 운영이다. CVE는 계속 나오고 SBOM은 계속 낡는다
- 대부분의 팀이 여기서 멈춘다. 예산 때문이다

---

## 17. TRUSCA ②: 무엇인가 (26:20 / 2분)

```
TRUSCA — Apache-2.0, self-hosted SCA

  detect    cdxgen, 30+ ecosystems
  match     Trivy unified DB (NVD · OSV · GHSA · EPSS · KEV)
  judge     VEX import/export, 7-stage triage
  enforce   3-tier license policy, CI gate, NOTICE generation
  operate   RBAC, audit log, Compose/Helm

  runs in your own network
```

**말하는 방식 주의**: 상용 도구와 기능을 나열해 비교하지 않는다.
"상용보다 낫다"가 아니라 "제약이 있는 팀에게 선택지가 하나 더 있다"로 말한다.

말할 것:

- 자체 호스팅이므로 폐쇄망에서 돌아간다. 이게 한국 기업 상당수에 결정적이다
- 규제 크로스워크 데이터는 BomLens에서 가져다 쓴다. 오픈소스 프로젝트끼리 데이터를 주고받은 결과다

---

## 18. TRUSCA ③: 그리고 다음 단계 (28:20 / 1분)

```
On the roadmap

  reachability analysis      is this CVE actually on our execution path?
  agent pre-flight policy    an MCP server the agent queries
                             before it adds a package
```

**발표를 닫는 슬라이드다.**

닫는 문장:

```
AI 에이전트를 통제하는 이야기로 시작해서,
그 에이전트가 스스로 정책을 조회하게 만드는 지점에서 두 축이 만납니다.

규칙으로 부탁하는 2단계도, CI에서 사후에 막는 3단계도 아닙니다.
넣기 전에 묻는 것입니다. 5단계 모델이 아직 담지 못한 자리입니다.
```

---

## 19. 시작하기 (29:20 / 1분)

```
Start today

  guide      trustedoss.github.io          CC BY 4.0
  agents     git clone → cd agents → claude
  browser    API key only, no local setup

  [ QR ]

  Built with the OpenChain Korea Work Group
```

말할 것:

- 전부 공개돼 있고 포크해서 회사에 맞게 고쳐 쓸 수 있다
- 브라우저 도구는 설치 없이 API 키만으로 바로 쓸 수 있다

---

## 20. Q&A (30:20 / 5분)

```
Questions

trustedoss.github.io
github.com/trustedoss
```

시간이 없으면 세션 후 개별 대응으로 넘긴다.

---

## 예상 질문과 답변 준비

**"이 가이드를 만든 저장소는 3~5단계를 적용했나?"**
현재 trustedoss 저장소에는 시크릿 탐지·SAST·SCA·Dependabot이 없다. 사실대로 말하고,
문서에서 링크한 실제 운영 사례는 TRUSCA임을 밝힌다. 적용 계획을 덧붙이면 자연스럽다.

**"AI가 만든 코드의 저작권은?"**
미국 저작권청 기준과 Thaler v. Perlmutter 상고 기각(2026-03)으로 AI 자체는 저작자가 될 수
없다는 원칙이 확정됐다. 사이트의 "AI 생성 코드의 법적 고려" 페이지로 안내한다.

**"CISA 2026을 도구가 지원하나?"**
공개 저장소에서 확인되지 않았다. **발표 전에 확인해 답을 정해 둔다.**
확인 못 했으면 "가이드는 반영했고 도구 대응은 진행 중"으로 답한다.

**"4단계 API 비용은?"**
findings 수를 제한해 통제한다. 정확한 수치는 팀 규모와 PR 빈도에 따라 다르므로
사전 추산을 권한다고 답한다. 실측치를 지어내지 않는다.

**"온프레미스 LLM으로 4단계를 할 수 있나?"**
가능하다. 사내 정책상 외부 API 전송이 막힌 경우의 대안으로 사이트에도 적어 두었다.

---

## 리허설 체크

- [ ] 전체 30분 안에 들어가는지 실측 (Q&A 제외)
- [ ] 데모 구간이 4.5분에 맞는지 — 넘치면 재생 속도를 올린다
- [ ] 11번 슬라이드에서 3초 침묵을 실제로 지키는지
- [ ] 4번 → 8번 연결(문제와 답)을 말로 명시했는지
- [ ] 18번 닫는 문장을 보지 않고 말할 수 있는지

시간이 밀릴 때 줄이는 순서: Q&A → 18번 로드맵 → 12~13번 4단계.
9번 데모와 11번 자가진단, 8번 SBOM 간극은 마지막까지 지킨다.
