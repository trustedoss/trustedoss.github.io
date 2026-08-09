# 슬라이드 구성안 + 발표 스크립트 — OSS Summit Korea 2026

**세션**: 2026-08-12(수) 13:35~14:15, Rose · 실질 35분(발표 30분 + Q&A 5분)
**형식**: 한국어 발표 · 슬라이드는 한국어 문장 + 영어 키워드
**영문 전용 슬라이드**: 별도 판으로 만들어 따로 배포한다(이 문서의 구성을 그대로 옮기면 된다)
**구성 근거**: `.claude/talk-ossummit-korea-2026.md`

스크립트는 축자 대본이 아니다. **첫 문장·전환 문장·닫는 문장은 그대로 말할 수 있게** 적었고,
나머지는 말할 요점을 문장으로 적었다. 낭독하지 않고 발표자의 표현으로 전달하는 것을 전제로 한다.

도구명·표준명·기술 용어(SBOM, CVE, SAST, MCP, CI/CD 등)는 영어 그대로 두고, 설명 문장만
한국어로 쓴다. 슬라이드 20장. 괄호 안 시간은 누적이 아니라 해당 구간의 길이다.

링크는 두 종류로 구분했다. **[화면]** 은 슬라이드에 실제로 띄우는 것이고, **[참조]** 는
발표자가 필요할 때 열거나 질문에 답할 때 쓰는 것이다. 전체 목록은 문서 맨 끝에 모아 두었다.
모든 링크는 2026-08-09 에 응답을 확인했다.

---

## 1. 타이틀 (0:00)

```
AI로 여는 오픈소스 리스크 관리
ISO 자체 인증 키트와 AI 코딩 거버넌스 5단계

장학성
SK텔레콤 · OpenChain Korea Work Group
```

인사와 소속을 한 문장으로 끝낸다. 소속 설명에 시간을 쓰지 않는다.

---

## 2. 문제 제기 ①: 오픈소스 공급망 위험 (0:20 / 1분)

```
오픈소스 공급망 침해는 반복되고 있습니다

XZ Utils (2024)      upstream 프로젝트에 삽입된 backdoor
Log4Shell (2021)     라이브러리 하나, 수억 개 시스템

공통점 — 무엇이 포함되어 있는지 파악하지 못했습니다
```

점심 직후 시간대이므로 목차로 시작하지 않는다. 사례부터 제시한다.

말할 것:

- 두 사건 모두 직접 작성하지 않은 코드가 원인이었다
- 구성 요소를 파악하지 못한 상태에서는 영향 범위조차 판단할 수 없다
- 이것이 기존에 알려진 문제다. 다음 슬라이드에서 AI 코딩이 이 조건을 어떻게 바꾸는지 다룬다

링크:

- **[참조]** 사건 정리 — https://trustedoss.github.io/docs/overview/supply-chain

---

## 3. 문제 제기 ②: AI 코딩이 조건을 바꿨습니다 (1:20 / 1분)

```
AI 코딩 도구는 세 가지를 바꿉니다

의존성 유입    AI 가 제안한 패키지가 사람의 검토를 거치지 않고 반입됩니다
코드 패턴      AI 가 생성한 코드는 기존 rule 에 없는 형태를 만듭니다
도구 호출      agent 가 MCP 로 외부 tool 을 호출하면
               그 tool 의 설명과 동작 자체가 공급망 입력이 됩니다

기존 통제는 사람이 코드를 작성한다는 전제 위에 설계되었습니다
```

**이 슬라이드가 세션 제목의 절반을 설명한다.** 축 B 전체(11~15번)의 근거가 여기서 나온다.

말할 것:

- 첫 번째는 반입 경로의 문제다. 사람이 라이브러리를 고를 때는 검토 절차가 작동하지만,
  AI 가 제안하고 에이전트가 설치하면 그 절차를 건너뛴다
- 두 번째는 탐지의 문제다. 정적 분석 도구는 알려진 패턴을 기준으로 판정하므로,
  학습된 규칙에 없는 형태는 통과한다
- 세 번째가 가장 최근에 생긴 축이다. 에이전트가 외부 도구를 호출하는 구조에서는
  도구의 메타데이터가 에이전트의 판단에 직접 개입한다

링크:

- **[참조]** 에이전트·MCP 거버넌스 — https://trustedoss.github.io/ai-coding/agent-governance

---

## 4. 문제 제기 ③: 규제 요구와 대응 수단의 격차 (2:20 / 1분)

```
규제 요구사항은 강화되었으나 대응 수단은 부족합니다

EU CRA        보고 의무 2026-09-11 · 전면 적용 2027-12-11
CISA 2026     2026-07-29 발표, NTIA 2021 대체
              component hash 와 license 가 필수 항목으로 변경
              적용 범위에 AI software 와 SaaS 포함

그러나 다수의 공급사는 SBOM 을 생성하지 못합니다
  소스 없음 (binary · firmware 납품)
  폐쇄망 (외부 서비스 업로드 불가)
  충족 여부 판정 방법 없음
```

말할 것:

- 유럽연합 사이버 복원력법(EU CRA) 보고 의무가 한 달 뒤 시작된다
- CISA 2026 최소 요소는 2주 전 발표되었고 NTIA 2021 기준을 대체한다.
  컴포넌트 해시와 라이선스가 권고에서 필수로 변경되었다
- 요구 수준은 상향되었으나 생성 수단은 그대로다. 이 격차를 8번 슬라이드에서 다시 다룬다

한 줄 덧붙임: 이 가이드는 CISA 2026 기준을 이미 반영했다.
(주의 — **가이드가 반영했다는 뜻이다.** 도구 구현 여부와 혼동하지 않는다.)

전환 문장:

```
AI 가 만들어내는 위험과, 그 관리 체계를 문서로 증명해야 하는 요구.
이 두 가지를 함께 다루는 방법이 오늘 주제입니다.
```

링크:

- **[화면]** CISA 원문 — https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom
- **[참조]** 우리 가이드의 반영 결과 — https://trustedoss.github.io/docs/overview/sbom-101
- **[참조]** 사건 정리와 규제 동향 — https://trustedoss.github.io/docs/overview/supply-chain

---

## 5. 전체 지도 (3:20 / 2분)

```
Trusted OSS 전체 지도

  [ 체계 구축 ]        ISO/IEC 5230 & 18974 자체 인증
                       agent 9종 → 산출물 24종 → 선언

  [ AI 코딩 ]          거버넌스 5단계 성숙도 모델
                       rules → CI gate → AI 방어 → 자동 교정

  [ DevSecOps ]        (위 모델의 3단계에 해당)

  ─────────────────────────────────────────────
  [ TRUSCA ]           선언 이후에 계속 도는 층

  trustedoss.github.io · CC BY 4.0
```

말할 것:

- 이후 모든 슬라이드는 이 지도 위의 한 지점에 해당한다
- DevSecOps 는 별도로 설명하지 않는다. 5단계 모델의 3단계가 DevSecOps 에 해당한다
- 하단의 TRUSCA 는 마지막에 다룬다. 배치 이유는 그 시점에 설명한다

링크:

- **[화면]** https://trustedoss.github.io
- **[참조]** 네 메뉴 — [체계 구축](https://trustedoss.github.io/docs) ·
  [AI 코딩](https://trustedoss.github.io/ai-coding/intro) ·
  [DevSecOps](https://trustedoss.github.io/devsecops/intro) ·
  [레퍼런스](https://trustedoss.github.io/reference/intro)

---

## 6. 축 A ①: 무엇을 만들어야 하는가 (5:20 / 1분)

```
두 표준이 실제로 요구하는 것

5230    정책 · 조직 · 프로세스 · BOM · 고지문 · 기여
18974   정책 · 조직 · SBOM · CVE 추적 · 대응 · 기록

공통 기반의 비중이 큽니다.
하나를 구축하면 나머지의 절반이 함께 충족됩니다.
```

말할 것:

- 두 표준은 독립적이지 않다. 정책·조직·교육·SBOM 이 공통 기반이다
- 개별 진행하면 동일한 작업을 중복 수행하게 된다

링크:

- **[참조]** 표준 요구사항 한눈에 —
  https://trustedoss.github.io/docs/overview/checklist-mapping

---

## 7. 축 A ②: Agent가 만든다 (6:20 / 1분)

```
agent 9종 → 산출물 24종

02 조직        역할 정의, RACI, 임명 공문
03 정책        오픈소스 정책, 허용 license 목록
04 프로세스    사용 승인, 배포 전 점검, 취약점 대응, 외부 문의
05 SBOM        CycloneDX SBOM, license 리포트, copyleft 위험
05 취약점      CVE 리포트, 조치 계획
06 교육        커리큘럼, 이수 추적
07 인증        gap 분석, 선언문 초안

github.com/trustedoss/trustedoss-agents
```

산출물을 하나씩 낭독하지 않는다. 화면으로 제시하고 구두로는 흐름만 설명한다.

말할 것:

- 각 agent 가 조직 상황을 질문하고 그 답변으로 문서를 생성한다. 템플릿을 채우는 방식이 아니라 답변에 따라 내용이 달라진다
- 마지막 agent 가 앞선 산출물을 모두 읽어 갭 분석과 선언문 초안을 생성한다

링크:

- **[화면]** agent 저장소 — https://github.com/trustedoss/trustedoss-agents
- **[참조]** 산출물 완성 예시 — https://trustedoss.github.io/reference/samples/policy

---

## 8. 축 A ③: SBOM 생성이 불가능한 구간 (7:20 / 1.5분)

```
SBOM 을 생성할 수 없는 구간

소스가 있는 경우    →  syft, cdxgen              해결됨
binary / firmware   →  ?
폐쇄망              →  ?

BomLens (Apache-2.0)
  입력   소스 · container · binary · firmware
  출력   CycloneDX SBOM · NOTICE · 위험 리포트 · ML-BOM
  실행   로컬에서 동작

github.com/sktelecom/bomlens
```

4번 슬라이드에서 제시한 격차를 여기서 해소한다. **이 연결을 말로 명시한다.**

말할 것:

```
앞에서 다수의 공급사가 SBOM 을 생성하지 못한다고 말씀드렸습니다.
그 원인이 여기에 있습니다.
```

- 소스가 있는 프로젝트는 syft 와 cdxgen 으로 해결된다
- 미해결 구간은 소스 없이 바이너리나 펌웨어만 존재하는 경우, 그리고 폐쇄망이다
- BomLens 는 로컬에서 실행되며 펌웨어와 바이너리를 입력으로 받는다. Apache-2.0 으로 공개되어 있다
- 고지문과 위험 리포트를 함께 생성한다

**사용하지 않을 표현**: "최적의 도구". 비교 평가 없이 단정하면 근거를 요구받는다.
지원 범위를 구체적으로 제시하는 것으로 충분하다.

링크:

- **[화면]** https://github.com/sktelecom/bomlens
- **[참조]** SBOM 생성 실습 — https://trustedoss.github.io/docs/tools/sbom-generation
- **[참조]** ML-BOM 실습(BomLens 실측) — https://trustedoss.github.io/docs/tools/ai-sbom

---

## 9. 축 A ④: 데모 (8:50 / 4.5분)

```
[ 녹화 데모 ]
agents/03-policy-generator → output/policy/oss-policy.md
```

녹화본을 2배속으로 재생하고 말로 해설한다. 라이브 실행하지 않는다.

해설할 지점:

- Agent가 던지는 질문 — 회사 규모, 배포 여부, 라이선스 정책 수준
- 답변에 따라 결과가 달라지는 부분
- 생성된 정책 문서에 표준 조항 번호가 붙어 있다는 점
- 이 문서가 다음 Agent의 입력이 된다는 점

시간이 지연되면 이 구간에서 조절한다. 재생을 중단하고 결과 화면으로 이동한다.

링크:

- **[참조]** 데모가 만든 것과 같은 산출물 —
  https://trustedoss.github.io/reference/samples/policy

---

## 10. 축 A ⑤: 그래서 어떻게 선언하는가 (13:20 / 1분)

```
자체 인증 선언 절차

1  체크리스트 내려받기     OpenChain-Project/Reference-Material
2  스스로 점검             각 항목에 yes / no
3  등재 신청               openchainproject.org/get-started

외부 심사 없음. 비용 없음.
```

말할 것:

- 자체 인증 방식이므로 외부 심사가 없다
- 체크리스트를 내려받아 자체 점검한 뒤 신청 폼을 제출한다
- 앞에서 생성한 갭 분석과 선언문 초안이 이 점검의 근거가 된다

링크:

- **[화면]** 체크리스트 —
  https://github.com/OpenChain-Project/Reference-Material/tree/master/OpenChain-Standards-Self-Certification
- **[화면]** 등재 신청 — https://openchainproject.org/get-started
- **[참조]** 07 인증 챕터 — https://trustedoss.github.io/docs/conformance

---

## 11. 축 B ①: 자가진단 (14:20 / 4분)

```
지금 우리 팀은 몇 단계입니까?

L1  프롬프트 의존       정책이 개인의 기억에만 있다
L2  규칙 내재화         CLAUDE.md, .cursor/rules, AGENTS.md
L3  CI/CD 자동 차단     gitleaks · semgrep · grype · trivy · checkov
L4  AI 방어 레이어      findings-driven 리뷰 · AI fuzzing
L5  지속 모니터링       dependabot · renovate · DAST

                        진입 비용:  L2 는 10분

trustedoss.github.io/ai-coding/strategy
```

띄우고 **3초 침묵**한다. 거수를 요구하지 않는다. 스스로 찾게 둔다.

말할 것:

- 1단계는 정책이 개인의 기억에만 존재하는 상태다. 담당자가 변경되면 유실된다
- 2단계는 그 정책을 규칙 파일로 저장소에 두는 단계다. 별도 비용 없이 10분이면 적용된다
- 3단계부터 실질적인 차단이 작동한다. 규칙은 권고이지 강제가 아니기 때문이다
- 시크릿 탐지를 먼저 적용하고 SAST, SCA 순으로 확대한다. 동시 도입은 실패 확률이 높다

3단계를 실제로 돌리는 곳이 있느냐는 질문이 나오면 아래 워크플로우를 연다.

전환 문장:

```
앞의 세 단계가 위험의 발생을 억제하는 통제라면,
4단계부터는 이미 발생한 위험을 탐지하는 통제입니다.
```

링크:

- **[화면]** 5단계 전략 — https://trustedoss.github.io/ai-coding/strategy
- **[참조]** 3단계 실제 운영 — TRUSCA. 다섯 영역 중 넷을 덮는다

  | 영역          | 도구                  | 워크플로우                                                                                            |
  | ------------- | --------------------- | ----------------------------------------------------------------------------------------------------- |
  | 시크릿 탐지   | gitleaks              | [secret-scan.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/secret-scan.yml)   |
  | SAST          | bandit · semgrep      | [sast.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sast.yml)                 |
  | SAST          | CodeQL                | [codeql.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/codeql.yml)             |
  | SCA           | cdxgen 12.3.3 + Trivy | [sca-self.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sca-self.yml)         |
  | 컨테이너 보안 | Trivy (image scan)    | [ci.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/ci.yml) 의 `image-scan` job |
  | IaC 보안      | —                     | 없음 (대상 IaC 가 없다)                                                                               |

- **[참조]** 5단계 실제 운영 — TRUSCA
  [dependabot.yml](https://github.com/trustedoss/trusca/blob/main/.github/dependabot.yml) (npm · pip · docker · github-actions) ·
  [sca-self.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sca-self.yml) (매일 07:00) ·
  [dogfood-scan.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/dogfood-scan.yml) (advisory 기본) ·
  [demo-health-canary.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/demo-health-canary.yml) (30분 주기).
  DAST 는 없다
- **[참조]** 4단계는 TRUSCA 에도 없다. 공개 저장소에서 findings-driven 리뷰를 상시 운영하는
  사례가 드물다는 점을 그대로 말하면 된다 — 이 단계가 앞서 있다는 뜻이 된다

---

## 12. 축 B ②: 4단계는 왜 필요한가 (18:20 / 1.5분)

```
3단계는 알려진 pattern 을 탐지합니다.
AI 는 알려지지 않은 pattern 을 생성합니다.

  AI 를 사용하는 공격자  →  신종 pattern  →  rule 미등록  →  통과

4단계 — AI 공격에는 AI 방어로
```

말할 것:

- 3단계 도구는 알려진 패턴을 정확하게 탐지한다. 이것이 강점이자 한계다
- 공격자도 AI 를 사용한다. 룰셋에 등록되지 않은 형태는 통과한다
- 전체 코드를 모델에 전달하는 방식은 비용이 크고 노이즈가 많다. 그래서 findings-driven 방식을 사용한다

---

## 13. 축 B ③: 무엇이 오가는가 (19:50 / 1.5분)

```
모델에 실제로 전달되는 것

  semgrep.sarif ─┐
  grype.json    ─┴→  파싱  →  플래그된 3건 + 각 ±5줄
                                       ↓
                             TP / FP · 위험도 · 익스플로잇 경로
                                       ↓
                                 PR 코멘트 (빌드 차단 아님)

trustedoss.github.io/ai-coding/ai-security-review
```

사이트에 실제 입출력 예시(SARIF 원본 → 프롬프트 → 판정 → PR 코멘트)가 들어 있으니,
시간이 되면 화면으로 보여준다.

말할 것:

- 저장소 전체가 아니라 플래그된 항목과 주변 코드만 전송된다
- 동일한 심각도로 플래그된 두 건을 모델이 실제 취약점과 오탐으로 구분한다. 3단계와 구분되는 지점이다
- 빌드는 실패시키지 않는다. 오탐 비율이 높기 때문에 PR 코멘트로만 남긴다

링크:

- **[화면]** https://trustedoss.github.io/ai-coding/ai-security-review

---

## 14. 축 B ④: 에이전트가 도구를 부른다 (21:20 / 1.5분)

```
agent 가 호출하는 tool 도 공급망 입력입니다

npm postmark-mcp
  1.0.15    정상
  1.0.16+   숨은 BCC — 모든 발신 메일을 외부 주소로 복사
            (시작 버전은 연구자의 추정)

도입 시점의 승인만으로는 통제되지 않습니다.
```

말할 것:

- MCP 는 에이전트가 외부 도구를 호출하는 규약이다
- 이 패키지는 초기 버전에서는 정상이었고 이후 버전에서 악성 코드가 포함되었다
- 도입 시점의 승인만으로는 통제되지 않는다. 버전 고정과 변경 추적이 필요한 근거다

**사실 경계 주의**: 악성 코드가 포함된 시작 버전은 추정이며, 공식 저장소와의 연관은
확인되지 않았다. 단정적으로 서술하지 않는다.

링크:

- **[화면]** 출처 — Snyk, https://snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails/

---

## 15. 축 B ⑤: 여섯 가지 통제 (22:50 / 1.5분)

```
Agent tool 통제 여섯 가지

1  서버 allowlist            5  사람 승인 + 감사 로그
2  최소 권한                 6  데이터 반출 경로 판정   ← 신규
3  도구 설명 검토
4  버전 고정

출처별 분기: 외부 커뮤니티 배포판만 전수 심사.
             벤더 공식 서버와 사내 개발 서버는 다른 절차로.

trustedoss.github.io/ai-coding/agent-governance
```

말할 것:

- 여섯 번째 항목이 앞의 사례에서 도출된 것이다. 도입 전에 외부 엔드포인트와 전송 데이터를 판정한다
- 모든 서버를 동일한 강도로 심사하면 운영이 지속되지 않는다. 출처에 따라 구분한다
- 호스팅 플랫폼을 경유하는 경우 해당 플랫폼도 심사 대상이다

전환 문장:

```
여기까지가 체계를 수립하고 위험을 통제하는 방법입니다.
그렇다면 자체 인증을 선언한 이후에는 무엇이 남습니까?
```

링크:

- **[화면]** https://trustedoss.github.io/ai-coding/agent-governance

---

## 16. TRUSCA ①: 선언 다음에 오는 것 (24:20 / 2분)

```
자체 인증 선언 이후에도 관리는 계속됩니다

18974 가 요구하는 것은 지속 운영입니다
  · 취약점 DB 주간 갱신
  · VEX 판정 최신 유지
  · 모든 빌드에서 license policy 적용

상용 SCA 도입 비용에서 중단되는 경우가 많습니다.
```

말할 것:

- 키트가 제공하는 범위는 체계 수립과 산출물 생성까지다
- 18974 가 요구하는 것은 지속 운영이다. CVE 는 계속 공개되고 SBOM 은 시간이 지나면 실제 구성과 어긋난다
- 이 지점에서 상용 도구 비용 때문에 중단되는 경우가 많다

---

## 17. TRUSCA ②: 무엇인가 (26:20 / 2분)

```
TRUSCA — Apache-2.0, self-hosted SCA

  탐지    cdxgen, 30개 이상 생태계
  대조    Trivy 통합 DB (NVD · OSV · GHSA · EPSS · KEV)
  판정    VEX 수출입, 7단계 triage
  차단    3계층 license policy, CI gate, NOTICE 생성
  운영    RBAC, 감사 로그, Compose / Helm

  사내망에서 실행됩니다

github.com/trustedoss/trusca
```

**서술 방식 주의**: 상용 도구와 기능을 나열해 비교하지 않는다.
"상용 대비 우위"가 아니라 "제약이 있는 조직의 선택지"로 제시한다.

말할 것:

- 자체 호스팅 방식이므로 폐쇄망에서 실행된다. 국내 기업 상당수에 중요한 조건이다
- 규제 크로스워크 데이터는 BomLens 에서 가져온 것이다. 오픈소스 프로젝트 간 데이터 재사용 사례다

공개된 운영 자산을 함께 제시한다. 문서상의 절차가 아니라 실제로 운영 중임을 확인할 수 있다.

링크:

- **[화면]** https://github.com/trustedoss/trusca · https://trustedoss.github.io/trusca/
- **[참조]** 릴리스마다 첨부되는 CycloneDX SBOM —
  https://github.com/trustedoss/trusca/releases/latest
- **[참조]** 취약점 신고 창구(5230 §3.2.1 · 18974 §4.2.1) —
  https://github.com/trustedoss/trusca/blob/main/SECURITY.md
- **[참조]** 고지문(5230 §3.4.1) —
  [NOTICE](https://github.com/trustedoss/trusca/blob/main/NOTICE) ·
  [THIRD_PARTY_NOTICES.md](https://github.com/trustedoss/trusca/blob/main/THIRD_PARTY_NOTICES.md)

---

## 18. TRUSCA ③: 그리고 다음 단계 (28:20 / 1분)

```
로드맵

  reachability 분석       이 CVE 가 우리 실행 경로에 실제로 있는가
  agent pre-flight 정책   패키지를 넣기 전에 agent 가 조회하는
                          MCP 서버
```

**발표를 닫는 슬라이드다.**

닫는 문장:

```
AI 에이전트를 통제하는 문제에서 출발해,
그 에이전트가 정책을 직접 조회하는 지점에서 두 축이 만납니다.

규칙으로 권고하는 2단계도, CI 에서 사후 차단하는 3단계도 아닙니다.
반입 이전에 조회하는 방식이며, 5단계 모델이 아직 포함하지 못한 영역입니다.
```

---

## 19. 시작하기 (29:20 / 1분)

```
오늘 바로 시작하기

  가이드      trustedoss.github.io            CC BY 4.0
  agent       git clone → cd agents → claude
  브라우저    API key 만으로 설치 없이 사용

  [ QR ]  →  trustedoss.github.io

  OpenChain Korea Work Group 과 함께 만들었습니다
```

말할 것:

- 전부 공개되어 있으며 포크해서 조직에 맞게 수정할 수 있다
- 브라우저 도구는 설치 없이 API 키만으로 사용할 수 있다

링크:

- **[화면]** QR 대상 — https://trustedoss.github.io
- **[화면]** https://github.com/trustedoss
- **[참조]** 브라우저 도구 —
  [Rules 생성기](https://trustedoss.github.io/ai-coding/rules-template) ·
  [Quick CI/CD](https://trustedoss.github.io/ai-coding/cicd-quick) ·
  [SBOM 분석기](https://trustedoss.github.io/devsecops/sca)

---

## 20. Q&A (30:20 / 5분)

```
질문

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
없다는 원칙이 확정됐다. → https://trustedoss.github.io/ai-coding/legal-considerations

**"CISA 2026을 도구가 지원하나?"**
공개 저장소에서 확인되지 않았다. **발표 전에 확인해 답을 정해 둔다.**
확인 못 했으면 "가이드는 반영했고 도구 대응은 진행 중"으로 답한다.

**"4단계 API 비용은?"**
findings 수를 제한해 통제한다. 정확한 수치는 팀 규모와 PR 빈도에 따라 다르므로
사전 추산을 권한다고 답한다. 실측치를 지어내지 않는다.

**"온프레미스 LLM으로 4단계를 할 수 있나?"**
가능하다. 사내 정책상 외부 API 전송이 막힌 경우의 대안으로 사이트에도 적어 두었다.
→ https://trustedoss.github.io/ai-coding/ai-security-review

**"ISO/IEC 42001(AI 경영시스템)과는 어떤 관계인가?"**
→ https://trustedoss.github.io/ai-coding/iso42001

---

## 전체 링크 목록

슬라이드 제작과 QR 준비에 쓴다. 2026-08-09 기준 전부 응답 확인.

### 사이트

| 대상                  | URL                                                         |
| --------------------- | ----------------------------------------------------------- |
| 메인                  | https://trustedoss.github.io                                |
| 체계 구축             | https://trustedoss.github.io/docs                           |
| AI 코딩               | https://trustedoss.github.io/ai-coding/intro                |
| DevSecOps             | https://trustedoss.github.io/devsecops/intro                |
| 레퍼런스              | https://trustedoss.github.io/reference/intro                |
| 5단계 전략            | https://trustedoss.github.io/ai-coding/strategy             |
| AI 보안 리뷰(4단계)   | https://trustedoss.github.io/ai-coding/ai-security-review   |
| 에이전트·MCP 거버넌스 | https://trustedoss.github.io/ai-coding/agent-governance     |
| 법적 고려             | https://trustedoss.github.io/ai-coding/legal-considerations |
| ISO/IEC 42001         | https://trustedoss.github.io/ai-coding/iso42001             |
| 파이프라인 설계       | https://trustedoss.github.io/devsecops/pipeline-design      |
| SBOM 생성 실습        | https://trustedoss.github.io/docs/tools/sbom-generation     |
| AI SBOM 실습          | https://trustedoss.github.io/docs/tools/ai-sbom             |
| 자체 인증 챕터        | https://trustedoss.github.io/docs/conformance               |
| 산출물 예시(정책)     | https://trustedoss.github.io/reference/samples/policy       |

### 저장소

| 대상          | URL                                             |
| ------------- | ----------------------------------------------- |
| 조직          | https://github.com/trustedoss                   |
| agent 저장소  | https://github.com/trustedoss/trustedoss-agents |
| TRUSCA        | https://github.com/trustedoss/trusca            |
| TRUSCA 사이트 | https://trustedoss.github.io/trusca/            |
| BomLens       | https://github.com/sktelecom/bomlens            |

### TRUSCA 실제 운영 사례

| 대상                     | URL                                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| 시크릿 탐지 (3단계)      | https://github.com/trustedoss/trusca/blob/main/.github/workflows/secret-scan.yml           |
| SAST — bandit·semgrep    | https://github.com/trustedoss/trusca/blob/main/.github/workflows/sast.yml                  |
| SAST — CodeQL            | https://github.com/trustedoss/trusca/blob/main/.github/workflows/codeql.yml                |
| SCA 정기 스캔 (3·5단계)  | https://github.com/trustedoss/trusca/blob/main/.github/workflows/sca-self.yml              |
| 컨테이너 이미지 스캔     | https://github.com/trustedoss/trusca/blob/main/.github/workflows/ci.yml (`image-scan` job) |
| 의존성 자동 갱신 (5단계) | https://github.com/trustedoss/trusca/blob/main/.github/dependabot.yml                      |
| 자기 적용 검증 (5단계)   | https://github.com/trustedoss/trusca/blob/main/.github/workflows/dogfood-scan.yml          |
| 운영 감시 (5단계)        | https://github.com/trustedoss/trusca/blob/main/.github/workflows/demo-health-canary.yml    |
| 릴리스 SBOM              | https://github.com/trustedoss/trusca/releases/latest                                       |
| 취약점 신고 창구         | https://github.com/trustedoss/trusca/blob/main/SECURITY.md                                 |
| 고지문                   | https://github.com/trustedoss/trusca/blob/main/NOTICE                                      |
| 서드파티 고지            | https://github.com/trustedoss/trusca/blob/main/THIRD_PARTY_NOTICES.md                      |

### 외부 표준·출처

| 대상                     | URL                                                                                                        |
| ------------------------ | ---------------------------------------------------------------------------------------------------------- |
| CISA 2026 최소 요소      | https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom          |
| OpenChain 등재 신청      | https://openchainproject.org/get-started                                                                   |
| 자체 인증 체크리스트     | https://github.com/OpenChain-Project/Reference-Material/tree/master/OpenChain-Standards-Self-Certification |
| postmark-mcp 사례 (Snyk) | https://snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails/                             |

---

## 리허설 체크

- [ ] 전체 30분 안에 들어가는지 실측 (Q&A 제외)
- [ ] 데모 구간이 4.5분에 맞는지 — 넘치면 재생 속도를 올린다
- [ ] 11번 슬라이드에서 3초 침묵을 실제로 지키는지
- [ ] 3번(AI 코딩이 바꾼 조건) → 축 B, 4번(생성 수단 부재) → 8번 연결을 말로 명시했는지
- [ ] 18번 닫는 문장을 보지 않고 말할 수 있는지
- [ ] 화면에 띄우는 URL 이 뒷자리에서 읽히는 크기인지

시간이 지연될 때 축소 순서: Q&A → 18번 로드맵 → 12~13번 4단계.
9번 데모, 11번 자가진단, 8번 SBOM 생성 구간은 마지막까지 유지한다.
