# 슬라이드 구성안 + 발표 스크립트 — OSS Summit Korea 2026

**세션**: 2026-08-12(수) 13:35~14:15, Rose · 실질 35분(발표 30분 + Q&A 5분)
**형식**: 한국어 발표 · 슬라이드는 한국어 문장 + 영어 키워드
**영문 전용 슬라이드**: 별도 판으로 만들어 따로 배포한다(이 문서의 구성을 그대로 옮기면 된다)
**구성 근거**: `.claude/talk-ossummit-korea-2026.md`

각 슬라이드 제목에 **시작 시각**과 **길이**를 함께 적었다. `시작 6:20 · 길이 1분` 은
발표 시작 후 6분 20초에 이 슬라이드로 넘어가고 1분간 머문다는 뜻이다.

말할 내용은 그 길이를 실제로 채우는 분량으로 적었다. 한국어 발표는 1분에 300자 안팎이므로
1분 슬라이드는 300자, 2분 슬라이드는 600자 정도가 기준이다. 축자 대본은 아니다.
**첫 문장·전환 문장·닫는 문장만 그대로 말할 수 있게** 적었고 나머지는 말할 내용을 문장으로 적었다.
낭독하지 않고 발표자의 표현으로 전달하는 것을 전제로 한다.

도구명·표준명·기술 용어(SBOM, CVE, SAST, MCP, CI/CD 등)는 영어 그대로 두고, 설명 문장만
한국어로 쓴다. 슬라이드 20장.

링크는 두 종류로 구분했다. **[화면]** 은 슬라이드에 실제로 띄우는 것이고, **[참조]** 는
발표자가 필요할 때 열거나 질문에 답할 때 쓰는 것이다. 전체 목록은 문서 맨 끝에 모아 두었다.
모든 링크는 2026-08-09 에 응답을 확인했다.

---

## 1. 타이틀 · 시작 0:00 · 길이 20초

```
AI로 여는 오픈소스 리스크 관리
ISO 자체 인증 키트와 AI 코딩 거버넌스 5단계

장학성
SK텔레콤 · OpenChain Korea Work Group
```

첫 문장:

```
안녕하십니까. SK텔레콤에서 오픈소스 관리를 맡고 있고,
OpenChain Korea Work Group 을 이끌고 있는 장학성입니다.

오늘은 오픈소스 컴플라이언스 체계를 AI 로 만드는 방법과,
그 AI 자체를 어떻게 통제할 것인가를 함께 말씀드리겠습니다.
```

소속 설명에 시간을 쓰지 않는다. 두 문장으로 끝내고 바로 다음 슬라이드로 넘어간다.

---

## 2. 문제 제기 ①: 오픈소스 공급망 위험 · 시작 0:20 · 길이 1분

```
오픈소스 공급망 침해는 계속 일어나고 있습니다

XZ Utils (2024)      upstream 프로젝트에 삽입된 backdoor
Log4Shell (2021)     라이브러리 하나, 수억 개 시스템

공통점 — 무엇이 들어 있는지 몰랐습니다
```

점심 직후 시간대이므로 목차로 시작하지 않는다. 사례부터 제시한다.

말할 것:

- XZ Utils 사건을 먼저 든다. 공격자가 2년 넘게 프로젝트에 기여하면서 신뢰를 쌓았고,
  메인테이너 권한을 얻은 뒤 압축 라이브러리에 backdoor 를 넣었다. 리눅스 배포판 대부분이
  의존하는 라이브러리였다. 우연히 성능 이상을 발견한 엔지니어가 없었다면 훨씬 넓게 퍼졌을 것이다
- Log4Shell 은 반대 경우다. 악의가 없었고 오래된 기능이 취약점으로 드러났을 뿐인데,
  Java 를 쓰는 거의 모든 조직이 영향을 받았다
- 두 사건의 원인은 다르지만 대응할 때의 문제는 같았다. **어느 제품에 그 라이브러리가
  들어 있는지 아무도 몰랐다.** 영향 범위를 파악하는 데만 며칠이 걸렸다
- 그래서 규제가 SBOM 을 요구하기 시작했다. 무엇이 들어 있는지부터 알자는 것이다

전환 문장:

```
여기까지가 이미 알려진 문제입니다.
그런데 AI 코딩이 여기에 새로운 조건을 더했습니다.
```

링크:

- **[참조]** 사건 정리 — https://trustedoss.github.io/docs/overview/supply-chain

---

## 3. 문제 제기 ②: AI 코딩이 조건을 바꿨습니다 · 시작 1:20 · 길이 1분

```
AI 코딩 도구는 세 가지를 바꿉니다

의존성 유입    AI 가 제안한 패키지가 사람의 검토를 거치지 않고 반입됩니다

검토 밀도      rule 이 탐지하지 못하는 영역 — 비즈니스 로직, 권한 검사,
               상태 전이 — 의 코드는 생산량만큼 늘지만
               리뷰 인원은 그대로입니다

도구 호출      MCP tool 의 description 은 agent 의 context 로 들어갑니다.
               사람이 읽지 않고 저장소에도 없으며 서버가 언제든 변경합니다

기존 통제는 사람이 코드를 쓰고 사람이 검토한다는 전제로 만들어졌습니다
```

**이 슬라이드가 세션 제목의 절반을 설명한다.** 2부 전체(11~15번)의 근거가 여기서 나온다.

말할 것:

- 첫 번째는 반입 경로 문제다. 예전에는 개발자가 라이브러리를 고를 때 최소한 검색은 했고,
  조직에 따라 승인 절차도 있었다. 지금은 AI 가 제안하고 에이전트가 설치까지 한다.
  사람이 그 이름을 처음 보는 시점이 이미 코드에 들어간 뒤다
- 두 번째는 탐지가 아니라 **분량** 문제다. 정적 분석이 비즈니스 로직 결함이나 권한 검사 누락을
  잡지 못하는 것은 원래부터 그랬다. 달라진 것은 그 영역에 들어가는 코드의 양이다.
  생산량이 몇 배가 되어도 리뷰 인원은 그대로다. 게다가 AI 가 쓴 코드는 문법이 정연하고
  주석까지 있어서 리뷰에서 문제로 인식되지 않는다.
  **"AI 가 신종 취약점 패턴을 만든다"고 말하지 않는다** — 근거를 요구받으면 답하기 어렵다
- 세 번째가 가장 최근에 생긴 문제다. MCP 도구 설명(description 필드)은 에이전트의 컨텍스트로
  들어가므로 **악성 지시를 숨긴 설명은 시스템 프롬프트를 바꾼 것과 같은 효과**를 낸다.
  문제는 이 설명이 세 가지 통제 어디에도 걸리지 않는다는 점이다. 사람은 읽지 않고(에이전트만 읽는다),
  저장소에 없으니 코드 리뷰 대상도 아니며, 서버가 내용을 바꿔도 알아채기 어렵다.
  1,899개 오픈소스 MCP 서버 조사에서 5.5% 가 이 유형을 보였다

링크:

- **[참조]** 에이전트·MCP 거버넌스 — https://trustedoss.github.io/ai-coding/agent-governance

---

## 4. 문제 제기 ③: 규제 요구와 SBOM 품질의 격차 · 시작 2:20 · 길이 1분

```
규제는 강해졌는데 만들 수단은 그대로입니다

EU CRA        보고 의무 2026-09-11 · 전면 적용 2027-12-11
CISA 2026     2026-07-29 발표, NTIA 2021 대체
              component hash 와 license 가 필수가 됨
              적용 범위가 AI software 와 SaaS 까지 넓어짐

그러나 납품되는 SBOM 은 요구 수준에 미치지 못합니다

  설명 없는 요구     왜 필요한지 공유되지 않은 채 제출 기한부터 통보됩니다
  안내의 한계        절차를 알려줘도 도구 선택과 환경 구성에서 막힙니다
  도입 비용          상용 도구는 조직 규모에 따라 부담이 큽니다
  결과의 정확도      무료 도구로 만든 SBOM 에 transitive dependency 가 빠지거나
                     PURL 이 없어 최소 요소를 충족하지 못합니다
```

말할 것:

- 위쪽 절반은 규제다. 유럽연합 사이버 복원력법 보고 의무가 **한 달 뒤** 시작된다.
  CISA 2026 최소 요소는 **2주 전에** 나왔고 NTIA 2021 기준을 대체했다.
  component hash 와 license 가 권고에서 필수가 됐다. 기준이 올라간 만큼 기존 방식으로 만든
  SBOM 은 더 자주 반려된다
- 아래쪽 절반이 오늘 말씀드리려는 현실이다. **문제의 핵심은 "만들지 못한다"가 아니라
  "만들어도 요구 수준에 못 미친다"이다.** 공급사 입장에서 보면 SBOM 은 왜 필요한지 공유되지
  않은 채 제출 기한부터 오는 요구다. 절차를 안내받아도 도구 선택과 환경 구성에서 막히고,
  상용 도구는 조직 규모에 따라 부담이 크다. 무료 도구로 생성해도 transitive dependency 누락,
  PURL 누락 같은 결함으로 최소 요소를 채우지 못한다. 원인은 8번 슬라이드에서 다룬다
- **공급사를 탓하는 어조가 되지 않게 한다.** 이것은 역량의 문제가 아니라 요구만 내려가고
  수단은 함께 가지 않은 구조의 문제다. 발표 자리에 해당 조직의 담당자가 있을 수 있다
- **폐쇄망과 "소스 없음"을 문제로 들지 않는다.** syft·cdxgen 은 로컬에서 실행되고, 공급사는
  대체로 자기가 개발한 소프트웨어의 소스를 가지고 있다. 실제 병목은 정확도다

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

## 5. 전체 지도 · 시작 3:20 · 길이 2분

```
Trusted OSS 전체 지도

  [ 체계 구축 ]         ISO/IEC 5230 & 18974 자체 인증
                        agent 9종 → 산출물 24종 → 선언

  [ AI 코딩 거버넌스 ]  5단계 성숙도 모델
                        rules → CI gate → AI 방어 → 자동 교정
                        3단계·5단계의 구현 상세는 DevSecOps 가이드

  ──────────────────────────────────────────────
  [ TRUSCA ]            선언한 뒤의 지속 운영

  trustedoss.github.io · CC BY 4.0
```

말할 것:

- Trusted OSS 는 CC BY 4.0 으로 공개된 실전 키트다. 누구나 가져다 회사에 맞게 고쳐 쓸 수 있다
- 위 칸이 첫 번째 영역이다. ISO/IEC 5230 은 라이선스 컴플라이언스, 18974 는 보안 보증 표준이다.
  둘 다 자체 인증 방식이라 외부 심사 없이 스스로 선언한다. 이 체계를 세우는 데 필요한 산출물
  24종을 agent 9종이 만든다. 오늘 앞부분에서 이걸 다룬다
- 아래 칸이 두 번째 영역이다. AI 코딩 도구를 쓰는 팀이 지금 어느 수준인지 판단하는 5단계
  모델이다. 오늘 뒷부분에서 다룬다. 각 단계를 실제로 구현하는 방법은 사이트의 DevSecOps
  가이드에 영역별로 정리돼 있다
- **DevSecOps 를 별도 상자로 그리지 않은 이유를 짚는다.** 5단계 모델이 성숙도를 판단하는 틀이고
  DevSecOps 가이드는 그 3단계와 5단계를 구현하는 방법이다. 층이 아니라 같은 것의 다른 면이다
- 선 아래 TRUSCA 는 이 프로젝트 바깥이다. 왜 여기 있는지는 마지막에 설명한다.
  지금은 "선언하고 끝이 아니다"라는 표시로만 봐 두면 된다

링크:

- **[화면]** https://trustedoss.github.io
- **[참조]** 네 메뉴 — [체계 구축](https://trustedoss.github.io/docs) ·
  [AI 코딩](https://trustedoss.github.io/ai-coding/intro) ·
  [DevSecOps](https://trustedoss.github.io/devsecops/intro) ·
  [레퍼런스](https://trustedoss.github.io/reference/intro)

---

## 6. 1부 ①: 두 표준이 요구하는 것 · 시작 5:20 · 길이 1분

```
두 표준이 실제로 요구하는 것

5230    정책 · 조직 · 프로세스 · BOM · 고지문 · 기여
18974   정책 · 조직 · SBOM · CVE 추적 · 대응 · 기록

공통 기반이 큽니다.
하나를 세우면 나머지 절반이 함께 충족됩니다.
```

말할 것:

- 두 표준을 별개 프로젝트로 진행하는 조직이 많은데, 실제로 열어 보면 공통 기반이 크다
- 문서화된 정책이 있어야 하고, 역할과 책임이 정해져 있어야 하고, 담당자가 교육을 받아야 하고,
  무엇을 쓰는지 목록이 있어야 한다. 여기까지가 양쪽 공통이다
- 갈라지는 지점은 그다음이다. 5230 은 라이선스 의무 이행과 고지문, 기여 정책을 요구하고,
  18974 는 취약점 탐지·점수화·조치와 그 기록을 요구한다
- 그래서 따로 진행하면 같은 작업을 두 번 하게 된다. 이 키트는 처음부터 두 표준을 함께
  충족하도록 설계돼 있다

링크:

- **[참조]** 표준 요구사항 한눈에 —
  https://trustedoss.github.io/docs/overview/checklist-mapping

---

## 7. 1부 ②: agent 가 산출물을 만든다 · 시작 6:20 · 길이 1분

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

산출물을 하나씩 낭독하지 않는다. 화면으로 제시하고 구두로는 아래 네 가지만 말한다.

말할 것:

- 왼쪽 번호가 진행 순서다. 조직을 정하고, 정책을 쓰고, 프로세스를 설계하고, SBOM 을 만들고,
  취약점을 분석하고, 교육 체계를 세우고, 마지막에 인증을 준비한다. 순서대로 가면 된다
- **각 agent 는 템플릿을 채우는 방식이 아니다.** 회사 상황을 묻고 그 답에 따라 내용이 달라진다.
  예를 들어 정책 agent 는 배포 여부, 라이선스 정책 수준, 법무 조직 유무를 묻고,
  그 답에 따라 허용 라이선스 목록과 승인 절차의 강도가 달라진다
- 앞 단계 산출물이 다음 단계의 입력이 된다. 조직에서 정한 담당자가 프로세스 문서의 승인자로
  들어가고, SBOM 분석 결과가 취약점 리포트의 입력이 된다. 그래서 순서가 중요하다
- 마지막 agent 는 질문을 하지 않는다. 앞서 만든 산출물을 전부 읽어서 표준 요구사항과 대조하고,
  충족·부분충족·미충족을 판정한 gap 분석과 선언문 초안을 만든다

전환 문장:

```
그런데 이 흐름에서 공급사가 가장 많이 막히는 지점이 하나 있습니다.
SBOM 입니다.
```

링크:

- **[화면]** agent 저장소 — https://github.com/trustedoss/trustedoss-agents
- **[참조]** 산출물 완성 예시 — https://trustedoss.github.io/reference/samples/policy

---

## 8. 1부 ③: 정확한 SBOM 을 만드는 문제 · 시작 7:20 · 길이 1분 30초

```
SBOM 은 만드는 것보다 정확하게 만드는 것이 어렵습니다

왜 빠지는가
  의존성 트리는 빌드해야 확정됩니다
  로컬에 Java · Maven · Node · Python 버전이 프로젝트와 맞지 않으면
  도구가 조용히 부분 결과만 냅니다
  → transitive dependency 누락 · PURL 없음 · license 미확인
  → 최소 요소 미충족 → 납품처 반려 → 재작업

BomLens (Apache-2.0)
  빌드 환경을 Docker image 하나로 제공합니다
  Java · Python · Node.js · Ruby · PHP · Rust · Go · .NET · Swift · C/C++
  공급사가 환경을 구성할 필요가 없습니다

  받는 쪽도 씁니다 — 납품된 SBOM 을 형식 요건 대비로 점검 (--analyze)
```

4번 슬라이드에서 제시한 문제에 여기서 답한다. **이 연결을 말로 명시한다.**

말할 것:

```
앞에서 납품되는 SBOM 이 요구 수준에 미치지 못한다고 말씀드렸습니다.
왜 그런지 원인부터 보겠습니다.
```

- 의존성 트리는 매니페스트만 읽어서는 확정되지 않는다. Maven 이든 npm 이든 빌드 도구가 실제로
  의존성을 해결해야 전이 의존성이 확인된다. 직접 선언한 라이브러리는 열 개인데 실제로 함께
  포함되는 것은 수백 개인 경우가 흔하다
- 그래서 로컬 환경이 프로젝트와 맞지 않으면 문제가 생긴다. Java 버전이 다르거나 빌드 도구가
  없으면 **도구가 실패하지 않고 부분 결과만 낸다.** 파일이 나왔으니 정상으로 보이고 그대로
  납품된다. 문제는 반려된 뒤에야 드러나는데, 원인이 환경 불일치라는 것을 알기 어려워
  같은 작업이 반복된다
- PURL 이 빠지면 더 곤란하다. 컴포넌트 식별자가 없으면 취약점 데이터베이스와 대조할 수 없다.
  SBOM 이 있어도 쓸 수 없는 문서가 된다
- BomLens 는 이 지점을 **빌드 환경을 Docker image 하나로 제공**해서 해결한다. 열 개 언어의
  런타임과 빌드 도구가 이미지 안에 들어 있으므로 공급사가 환경을 맞출 필요가 없다
- 설치 프로그램과 웹 UI 가 있어 명령줄을 쓰지 않아도 되고, Apache-2.0 이라 도입 비용이 없다.
  앞 슬라이드의 네 가지에 각각 대응한다
- 받는 쪽에서도 쓸 수 있다. 협력사가 보낸 SBOM 을 형식 요건 대비로 점검하는 기능이 있어서,
  반려할지 판단할 근거가 생긴다

**사용하지 않을 표현**: "최적의 도구". 비교 평가 없이 단정하면 근거를 요구받는다.
빌드 환경을 이미지로 제공한다는 구조적 차이를 말하는 것으로 충분하다.

링크:

- **[화면]** https://github.com/sktelecom/bomlens
- **[참조]** 설치 없이 결과만 보는 데모 — https://sktelecom.github.io/bomlens/demo/
  (소스·컨테이너 이미지·펌웨어·AI 모델·협력사 SBOM 점검 결과가 각각 하나씩 있다)
- **[참조]** SBOM 생성 실습 — https://trustedoss.github.io/docs/tools/sbom-generation
- **[참조]** ML-BOM 실습(BomLens 실측) — https://trustedoss.github.io/docs/tools/ai-sbom

---

## 9. 1부 ④: 데모 · 시작 8:50 · 길이 4분 30초

```
[ 녹화 데모 ]
agents/03-policy-generator → output/policy/oss-policy.md
```

녹화본을 2배속으로 재생하고 말로 해설한다. 라이브 실행하지 않는다.
아래는 재생 구간별 해설 순서다.

**0:00~1:00 — 실행과 첫 질문**

```
지금 보시는 것은 정책 생성 agent 입니다.
저장소를 클론하고 해당 폴더에서 claude 를 실행한 화면입니다.
```

- 사용자가 입력한 것은 명령 한 줄뿐이다. 나머지는 agent 가 묻는다
- 첫 질문이 회사 규모다. 규모에 따라 전담 조직을 둘지 겸무로 갈지가 달라진다

**1:00~2:30 — 질문에 답하는 과정**

- 배포 여부를 묻는다. 사내에서만 쓰는 소프트웨어와 고객에게 배포하는 소프트웨어는
  라이선스 의무가 완전히 다르다. 여기서 답이 갈리면 뒤 문서의 절 구성이 달라진다
- 라이선스 정책 수준을 묻는다. 엄격·표준·유연 셋 중 하나다. 이 답이 허용 라이선스 목록에
  그대로 반영된다
- **여기서 강조한다.** 질문이 다섯 개 남짓인데, 답에 따라 결과 문서의 내용이 실제로 달라진다.
  같은 템플릿에 회사 이름만 바꿔 넣는 방식이 아니다

**2:30~4:00 — 생성된 문서 확인**

- 생성된 `oss-policy.md` 를 연다. 목차부터 본다
- 각 절 옆에 표준 조항 번호가 붙어 있다. 5230 §3.1.1 처럼 어느 요구사항을 충족하는지가
  문서에 기재돼 있다. 나중에 gap 분석 agent 가 이 표기를 읽어서 대조한다
- 허용 라이선스 목록을 보여준다. 앞에서 선택한 정책 수준이 여기 반영돼 있다

**4:00~4:30 — 다음 단계로의 연결**

```
이 문서가 다음 agent 의 입력이 됩니다.
프로세스 설계 agent 는 이 정책을 읽어서 승인 절차를 만듭니다.
```

- 24개 산출물이 이렇게 이어진다. 각각 독립된 문서가 아니라 하나의 체계다

시간이 지연되면 이 구간에서 조절한다. 2:30 지점으로 건너뛰어 결과 문서만 보여준다.

링크:

- **[참조]** 데모가 만든 것과 같은 산출물 —
  https://trustedoss.github.io/reference/samples/policy

---

## 10. 1부 ⑤: 자체 인증 선언 절차 · 시작 13:20 · 길이 1분

```
자체 인증 선언 절차

1  checklist 내려받기      OpenChain-Project/Reference-Material
2  self-assessment         각 항목에 yes / no
3  등재 신청               openchainproject.org/get-started

외부 심사 없음. 비용 없음.
```

말할 것:

- 인증이라고 하면 심사기관과 비용을 먼저 떠올리는데, OpenChain 자체 인증은 그렇지 않다.
  외부 심사가 없고 비용도 들지 않는다
- 절차는 세 단계다. GitHub 에서 체크리스트를 내려받고, 각 항목에 yes 또는 no 로 스스로
  점검하고, 신청 폼을 제출한다. 5230 과 18974 각각 25개 항목이다
- **앞에서 만든 gap 분석이 이 점검의 근거가 된다.** 항목마다 어느 산출물이 그것을 충족하는지
  이미 대조돼 있으므로, 체크리스트를 채우는 작업이 확인 작업으로 바뀐다
- 유효 기간은 18개월이다. 그 안에 다시 점검하고 재선언한다

전환 문장:

```
여기까지가 체계를 세우는 이야기입니다.
이제 그 체계 안에서 AI 코딩을 어떻게 다룰지로 넘어가겠습니다.
```

링크:

- **[화면]** 체크리스트 —
  https://github.com/OpenChain-Project/Reference-Material/tree/master/OpenChain-Standards-Self-Certification
- **[화면]** 등재 신청 — https://openchainproject.org/get-started
- **[참조]** 07 인증 챕터 — https://trustedoss.github.io/docs/conformance

---

## 11. 2부 ①: 자가진단 · 시작 14:20 · 길이 4분

```
지금 우리 팀은 몇 단계입니까?

L1  프롬프트 의존       정책이 개인의 기억에만 있다
L2  AI 규칙 내재화      CLAUDE.md, .cursor/rules, AGENTS.md
L3  CI/CD 자동 차단     gitleaks · semgrep · grype · trivy · checkov
L4  AI 방어 레이어      findings-driven 리뷰 · AI fuzzing
L5  지속 모니터링       dependabot · renovate · DAST

                        진입 비용:  L2 는 10분

trustedoss.github.io/ai-coding/strategy
```

띄우고 **3초 침묵**한다. 거수를 요구하지 않는다. 스스로 찾게 둔다.

첫 문장:

```
이 표를 3초만 보시고, 지금 우리 팀이 어디에 있는지 찾아보십시오.
```

말할 것:

- **1단계**는 정책이 개인의 기억에만 있는 상태다. 개발자가 프롬프트에 "GPL 은 쓰지 마"라고
  매번 적는다. 그 사람이 팀을 떠나면 사라지고, 새로 온 사람은 알 방법이 없다.
  대부분의 팀이 여기서 시작한다
- **2단계**는 그 정책을 규칙 파일로 저장소에 두는 단계다. CLAUDE.md, .cursor/rules, AGENTS.md
  같은 파일이다. 저장소에 커밋하면 팀 전체에 같은 정책이 적용되고, 새로 합류한 사람에게도
  자동으로 전달된다. **별도 비용 없이 10분이면 적용된다.** 혼자 개발하더라도 여기서
  시작하시기를 권한다
- **3단계**부터 실질적인 차단이 작동한다. 앞의 두 단계는 AI 에게 권고하는 것이지 강제가 아니다.
  AI 가 규칙을 무시해도 막을 방법이 없다. 파이프라인이 기계적으로 막아야 한다.
  다섯 영역이 있는데 순서가 중요하다. **secret detection 을 먼저 적용한다.** AI 코딩 도구는
  값을 하드코딩하는 일이 잦고, 시크릿은 한 번 노출되면 되돌릴 수 없다.
  그다음 SAST, SCA 순으로 확대한다. 동시에 다 넣으면 오탐이 쏟아져서 팀이 게이트를 꺼 버린다
- **4단계와 5단계**는 뒤에서 따로 다룬다. 지금은 4단계가 AI 로 방어하는 층,
  5단계가 배포 이후에도 계속 실행되는 통제라는 것만 봐 두시면 된다
- 각 단계의 진입 비용을 함께 봐야 한다. 2단계는 10분이고, 3단계는 도구마다 반나절 정도다.
  4단계부터는 담당자가 필요하다. **자기 팀이 지금 할 수 있는 다음 단계를 정하는 것이
  이 표의 목적이다.** 한 번에 5단계까지 가려는 계획은 대부분 실패한다

3단계를 실제로 돌리는 곳이 있느냐는 질문이 나오면 아래 워크플로우를 연다.

전환 문장:

```
앞의 세 단계가 위험의 발생을 억제하는 통제라면,
4단계부터는 이미 발생한 위험을 탐지하는 통제입니다.
```

링크:

- **[화면]** 5단계 전략 — https://trustedoss.github.io/ai-coding/strategy
- **[참조]** 3단계 실제 운영 — TRUSCA. 다섯 영역 중 넷을 덮는다

  | 영역             | 도구                  | 워크플로우                                                                                            |
  | ---------------- | --------------------- | ----------------------------------------------------------------------------------------------------- |
  | secret detection | gitleaks              | [secret-scan.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/secret-scan.yml)   |
  | SAST             | bandit · semgrep      | [sast.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sast.yml)                 |
  | SAST             | CodeQL                | [codeql.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/codeql.yml)             |
  | SCA              | cdxgen 12.3.3 + Trivy | [sca-self.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sca-self.yml)         |
  | container 보안   | Trivy (image scan)    | [ci.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/ci.yml) 의 `image-scan` job |
  | IaC 보안         | —                     | 없음 (대상 IaC 가 없다)                                                                               |

- **[참조]** 5단계 실제 운영 — TRUSCA
  [dependabot.yml](https://github.com/trustedoss/trusca/blob/main/.github/dependabot.yml) (npm · pip · docker · github-actions) ·
  [sca-self.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/sca-self.yml) (매일 07:00) ·
  [dogfood-scan.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/dogfood-scan.yml) (advisory 기본) ·
  [demo-health-canary.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/demo-health-canary.yml) (30분 주기).
  DAST 는 없다
- **[참조]** 4단계는 TRUSCA 에도 없다. 공개 저장소에서 findings-driven 리뷰를 상시 운영하는
  사례가 드물다는 점을 그대로 말하면 된다 — 이 단계가 앞서 있다는 뜻이 된다

---

## 12. 2부 ②: 4단계가 필요한 이유 · 시작 18:20 · 길이 1분 30초

```
3단계는 알려진 pattern 을 탐지합니다.
AI 는 알려지지 않은 pattern 을 생성합니다.

  AI 를 사용하는 공격자  →  신종 pattern  →  rule 미등록  →  통과

4단계 — AI 공격에는 AI 방어로
```

말할 것:

- 3단계 도구는 알려진 패턴을 정확하게 탐지한다. Semgrep 룰이든 CodeQL 쿼리든 "이런 형태는
  위험하다"를 미리 정의해 둔 것이다. 정확하다는 것이 강점이고, 정의되지 않은 것은 못 잡는다는
  것이 한계다
- 이 한계는 원래부터 있었다. 비즈니스 로직 결함, 권한 검사 누락, 상태 전이 오류는 룰로 표현하기
  어렵다. 앞에서 말씀드린 대로 AI 코딩은 그 영역에 들어가는 코드의 양을 늘린다
- 여기에 공격자 측면이 하나 더 있다. 공격자도 AI 를 쓴다. 기존 룰을 우회하는 변형을 자동으로
  만들어 볼 수 있다
- 그래서 4단계는 AI 로 이 사각지대를 보완한다. **다만 전체 코드를 모델에 보내는 방식은 안 된다.**
  비용이 크고, 노이즈가 많아서 정작 중요한 항목이 드러나지 않는다
- findings-driven 방식은 순서를 바꾼다. 3단계 도구가 먼저 후보를 추리고, 모델은 그 결과에만
  집중한다. 다음 슬라이드에서 실제로 무엇이 오가는지 보여드리겠다

---

## 13. 2부 ③: 모델에 무엇이 전달되는가 · 시작 19:50 · 길이 1분 30초

```
모델에 실제로 전달되는 것

  semgrep.sarif ─┐
  grype.json    ─┴→  파싱  →  플래그된 3건 + 각 ±5줄
                                       ↓
                             TP / FP · risk · exploit path
                                       ↓
                                 PR 코멘트 (빌드 차단 아님)

trustedoss.github.io/ai-coding/ai-security-review
```

사이트에 실제 입출력 예시(SARIF 원본 → 프롬프트 → 판정 → PR 코멘트)가 들어 있으니,
시간이 되면 화면으로 보여준다.

말할 것:

- 왼쪽이 3단계 도구의 출력이다. Semgrep 은 SARIF 로, grype 는 JSON 으로 결과를 낸다.
  그대로는 크고 불필요한 필드가 많다
- 파싱 단계에서 필요한 것만 뽑는다. 플래그된 항목과 그 주변 다섯 줄이다.
  **저장소 전체가 아니라 이만큼만 나간다.** 토큰 비용이 통제되는 이유다
- 모델은 항목마다 세 가지를 판정한다. 실제 취약점인지 오탐인지, 위험도가 어느 정도인지,
  실제 취약점이라면 어떤 경로로 공격이 가능한지
- **여기가 3단계와 구분되는 지점이다.** 예를 들어 SQL 문자열 조합과 `shell=True` 두 건이 같은
  심각도로 플래그됐다고 하자. 앞의 것은 사용자 입력이 그대로 들어가니 실제 취약점이고,
  뒤의 것은 명령 문자열에 상수만 들어가니 오탐이다. 룰은 이 차이를 모르지만 모델은 구분한다
- 결과는 PR 코멘트로만 남긴다. **빌드는 실패시키지 않는다.** 오탐 비율이 높기 때문이다.
  4단계는 차단이 아니라 판단을 돕는 층이다

링크:

- **[화면]** https://trustedoss.github.io/ai-coding/ai-security-review

---

## 14. 2부 ④: agent 가 호출하는 tool · 시작 21:20 · 길이 1분 30초

```
agent 가 호출하는 tool 도 공급망 입력입니다

npm postmark-mcp
  1.0.15    정상
  1.0.16+   숨은 BCC — 모든 발신 메일을 외부 주소로 복사
            (시작 버전은 연구자의 추정)

도입 시점의 승인만으로는 통제되지 않습니다.
```

말할 것:

- MCP 는 에이전트가 외부 도구를 호출하는 규약이다. 지금은 개발 환경에서 널리 쓰인다.
  GitHub 을 읽고, 데이터베이스를 조회하고, 메일을 보내는 도구들이 이 방식으로 연결된다
- 이 패키지는 메일 발송 도구다. 처음에는 정상이었다. 그런데 이후 버전에 숨은 BCC 가 들어가서,
  이 도구로 보낸 **모든 메일이 외부 주소로 복사**됐다
- 도입할 때 심사했다면 통과했을 것이다. 그 시점에는 정상이었기 때문이다.
  **한 번 승인하는 것으로는 막지 못한다**는 것이 이 사례의 요점이고, 버전 고정과 변경 추적이
  필요한 이유다
- 이름이 실제 서비스와 같아서 공식 패키지로 오인하기 쉬웠다는 점도 있다. 게시 계정과 운영
  주체를 대조하는 확인이 필요한 이유다

**사실 경계 주의**: 악성 코드가 포함된 시작 버전은 추정이며, 공식 저장소와의 연관은
확인되지 않았다. 단정적으로 서술하지 않는다. 2차 보도의 다운로드 수와 영향 조직 수는
원문에 없는 수치이므로 쓰지 않는다.

링크:

- **[화면]** 출처 — Snyk, https://snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails/

---

## 15. 2부 ⑤: agent tool 통제 여섯 가지 · 시작 22:50 · 길이 1분 30초

```
agent tool 통제 여섯 가지

1  서버 allowlist            5  사람 승인 + 감사 로그
2  최소 권한                 6  데이터 반출 경로 판정   ← 신규
3  도구 설명 검토
4  버전 고정

출처별 분기: 외부 커뮤니티 배포판만 전수 심사.
             벤더 공식 서버와 사내 개발 서버는 다른 절차로.

trustedoss.github.io/ai-coding/agent-governance
```

말할 것:

- 앞의 다섯 가지는 Microsoft Incident Response 권고와 MCP 스펙의 보안 원칙을 실무 규칙으로
  옮긴 것이다. 승인된 서버만 쓰고, 권한을 최소로 주고, 도구 설명을 검토하고, 버전을 고정하고,
  고위험 작업은 사람이 승인한다
- **여섯 번째가 앞의 사례에서 나온 것이다.** 도입 전에 그 서버가 어떤 외부 endpoint 와
  통신하는지, 사내 데이터가 그 경로로 나갈 수 있는지 판정한다. postmark-mcp 사례가 정확히
  이 항목에서 탐지될 수 있었던 유형이다
- 실무에서 중요한 것은 아래쪽이다. **모든 서버를 같은 강도로 심사하면 운영이 이어지지 않는다.**
  전수 심사가 필요한 것은 npm 이나 PyPI 에서 받는 외부 커뮤니티 배포판이다.
  GitHub 이나 Atlassian 이 자기 서비스용으로 내는 공식 서버는 권한 범위와 반출 경로 확인
  중심의 간이 심사로 충분하고, 사내에서 직접 만드는 서버는 심사가 아니라 설계 검토의 문제다
- 하나 덧붙이면, 호스팅 플랫폼을 경유해 서버를 도입한다면 그 플랫폼도 심사 대상이다.
  개별 서버를 아무리 심사해도 호스팅 경로가 단일 실패 지점이 될 수 있다

전환 문장:

```
여기까지가 체계를 수립하고 위험을 통제하는 방법입니다.
그렇다면 자체 인증을 선언한 이후에는 무엇이 남습니까?
```

링크:

- **[화면]** https://trustedoss.github.io/ai-coding/agent-governance

---

## 16. TRUSCA ①: 선언 이후에 남는 것 · 시작 24:20 · 길이 2분

```
자체 인증을 선언한 뒤에도 관리는 계속됩니다

18974 가 요구하는 것은 지속 운영입니다
  · vulnerability DB 주간 갱신
  · VEX 판정 최신 유지
  · 모든 build 에서 license policy 적용

상용 SCA 비용 때문에 여기서 멈추는 경우가 많습니다.
```

말할 것:

- 지금까지 말씀드린 키트가 해 주는 것은 체계를 세우고 산출물을 만드는 데까지다.
  선언문 초안이 나오면 거기서 끝난다
- 그런데 18974 를 다시 읽어 보면 요구하는 것이 지속 운영이다. 취약점 데이터베이스는 계속
  갱신되고, 새 CVE 가 나오면 우리 제품에 영향이 있는지 판정해야 하고, 그 판정 결과를
  VEX 로 관리해야 한다. 라이선스 정책도 빌드마다 적용돼야 한다
- SBOM 은 만든 순간부터 실제 구성과 달라지기 시작한다. 6개월 전 SBOM 을 믿고 있다가 그 사이 추가된 라이브러리의
  취약점을 놓치는 경우가 실제로 있다. 고객이 먼저 발견하면 신뢰 문제가 된다
- 이걸 사람이 손으로 하기는 어렵다. 도구가 필요한데, 상용 SCA 는 조직 규모에 따라 도입 부담이
  크다. **선언은 했는데 운영이 이어지지 않는 상태**가 여기서 생긴다
- 도입 여력이 크지 않은 조직과, 외부 서비스를 쓸 수 없는 폐쇄망 환경에서 특히 그렇다

---

## 17. TRUSCA ②: 무엇인가 · 시작 26:20 · 길이 2분

```
TRUSCA — Apache-2.0, self-hosted SCA

  detect     cdxgen, 30개 이상 ecosystem
  match      Trivy 통합 DB (NVD · OSV · GHSA · EPSS · KEV)
  triage     VEX import / export, 7단계 triage
  enforce    3계층 license policy, CI gate, NOTICE 생성
  operate    RBAC, audit log, Compose / Helm

  사내망에서 실행됩니다

github.com/trustedoss/trusca
```

**서술 방식 주의**: 상용 도구와 기능을 나열해 비교하지 않는다.
"상용 대비 우위"가 아니라 "제약이 있는 조직의 선택지"로 제시한다.

말할 것:

- TRUSCA 는 Apache-2.0 으로 공개된 self-hosted SCA 다. 앞 슬라이드에서 말씀드린 지속 운영을
  맡는 층이다
- 컴포넌트 탐지는 cdxgen 으로 30개 이상 생태계를 덮는다. 취약점 대조는 Trivy 통합 데이터베이스를
  쓰는데, NVD 와 OSV 뿐 아니라 EPSS 와 KEV 까지 들어 있다. 악용 확률과 실제 악용 여부까지
  보고 우선순위를 정할 수 있다는 뜻이다
- VEX 를 수출입할 수 있고 7단계 triage 를 지원한다. "이 CVE 는 우리 실행 경로에 없다"는 판정을
  기록하고 협력사와 주고받을 수 있다. 18974 가 요구하는 조치 기록이 이 형태로 남는다
- 라이선스 정책은 3계층으로 두고 금지 라이선스는 빌드를 차단한다. 고지문도 자동 생성된다
- **자체 호스팅이라는 점이 핵심이다.** 사내망 안에서 돌기 때문에 코드나 SBOM 이 외부로 나가지
  않는다. 국내 기업 상당수에 중요한 조건이다
- 규제 크로스워크 데이터는 BomLens 에서 가져온 것이다. 앞에서 말씀드린 SBOM 생성 도구와 같은
  데이터를 공유한다. **오픈소스 프로젝트끼리 실제로 데이터를 주고받은 사례다**

공개된 운영 자산을 함께 제시한다. 문서상의 절차가 아니라 실제로 운영 중임을 확인할 수 있다.

링크:

- **[화면]** https://github.com/trustedoss/trusca · https://trustedoss.github.io/trusca/
- **[참조]** release asset 으로 첨부되는 CycloneDX SBOM —
  https://github.com/trustedoss/trusca/releases/latest
- **[참조]** vulnerability 신고 창구(5230 §3.2.1 · 18974 §4.2.1) —
  https://github.com/trustedoss/trusca/blob/main/SECURITY.md
- **[참조]** NOTICE 와 third-party notices(5230 §3.4.1) —
  [NOTICE](https://github.com/trustedoss/trusca/blob/main/NOTICE) ·
  [THIRD_PARTY_NOTICES.md](https://github.com/trustedoss/trusca/blob/main/THIRD_PARTY_NOTICES.md)

---

## 18. TRUSCA ③: 로드맵 · 시작 28:20 · 길이 1분

```
로드맵

  reachability 분석       이 CVE 가 실제 execution path 상에 있는가
  agent pre-flight 정책   패키지를 넣기 전에 agent 가 조회하는
                          MCP 서버
```

**발표를 닫는 슬라이드다.**

말할 것:

- 두 가지가 진행 중이다. 첫 번째는 도달 가능성 분석이다. CVE 가 있어도 우리 코드에서 그 함수를
  부르지 않으면 실제 위험은 없다. 이걸 판정할 수 있으면 triage 부담이 크게 준다
- 두 번째가 오늘 이야기와 이어진다. **에이전트가 패키지를 넣기 전에 정책을 조회하는 MCP 서버다**

닫는 문장:

```
AI 에이전트를 통제하는 문제에서 출발해,
그 에이전트가 정책을 직접 조회하는 지점에서 1부와 2부가 만납니다.

규칙으로 권고하는 2단계도, CI 에서 사후 차단하는 3단계도 아닙니다.
반입 이전에 조회하는 방식이며, 5단계 모델이 아직 포함하지 못한 영역입니다.
```

---

## 19. 시작하기 · 시작 29:20 · 길이 1분

```
오늘 바로 시작하기

  guide       trustedoss.github.io           CC BY 4.0
  agent       git clone → cd agents → claude
  browser     API key 만으로 설치 없이 사용

  [ QR ]  →  trustedoss.github.io

  OpenChain KWG 와 연계해 운영합니다
```

말할 것:

- 전부 공개돼 있고 fork 해서 조직에 맞게 고칠 수 있다. CC BY 4.0 이므로 출처만 밝히면 된다
- agent 를 쓰려면 저장소를 클론하고 해당 폴더에서 claude 를 실행하면 된다.
  "어디서 시작해야 해?"라고 물으면 현재 상태를 진단하고 다음 단계를 안내한다
- Claude Code 없이 브라우저에서 바로 쓸 수 있는 도구도 있다. API key 만 있으면 되고
  설치가 필요 없다. Rules 생성기, CI/CD 워크플로 생성기, SBOM·SAST·시크릿·IaC 분석기다
- 사이트 메뉴는 네 개다 — 오픈소스 관리, AI 코딩 거버넌스, DevSecOps, 레퍼런스.
  오늘 다루지 않은 DevSecOps 에는 영역별(secret detection · SAST · SCA · container · IaC · DAST)
  구현 가이드와 전사 pipeline 설계가 들어 있다
- 기여를 환영한다. OpenChain KWG 커뮤니티와 연계해 운영하고 있다

링크:

- **[화면]** QR 대상 — https://trustedoss.github.io
- **[화면]** https://github.com/trustedoss
- **[참조]** 브라우저 도구 —
  [Rules 생성기](https://trustedoss.github.io/ai-coding/rules-template) ·
  [Quick CI/CD](https://trustedoss.github.io/ai-coding/cicd-quick) ·
  [SBOM 분석기](https://trustedoss.github.io/devsecops/sca)

---

## 20. Q&A · 시작 30:20 · 길이 5분

```
질문

trustedoss.github.io
github.com/trustedoss
```

시간이 없으면 세션 후 개별 대응으로 넘긴다. 아래 예상 질문을 미리 준비해 둔다.

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

| 대상                      | URL                                                                                        |
| ------------------------- | ------------------------------------------------------------------------------------------ |
| secret detection (3단계)  | https://github.com/trustedoss/trusca/blob/main/.github/workflows/secret-scan.yml           |
| SAST — bandit·semgrep     | https://github.com/trustedoss/trusca/blob/main/.github/workflows/sast.yml                  |
| SAST — CodeQL             | https://github.com/trustedoss/trusca/blob/main/.github/workflows/codeql.yml                |
| SCA scheduled scan        | https://github.com/trustedoss/trusca/blob/main/.github/workflows/sca-self.yml              |
| container image scan      | https://github.com/trustedoss/trusca/blob/main/.github/workflows/ci.yml (`image-scan` job) |
| dependency update (5단계) | https://github.com/trustedoss/trusca/blob/main/.github/dependabot.yml                      |
| dogfooding (5단계)        | https://github.com/trustedoss/trusca/blob/main/.github/workflows/dogfood-scan.yml          |
| health canary (5단계)     | https://github.com/trustedoss/trusca/blob/main/.github/workflows/demo-health-canary.yml    |
| release SBOM              | https://github.com/trustedoss/trusca/releases/latest                                       |
| vulnerability 신고 창구   | https://github.com/trustedoss/trusca/blob/main/SECURITY.md                                 |
| NOTICE                    | https://github.com/trustedoss/trusca/blob/main/NOTICE                                      |
| third-party notices       | https://github.com/trustedoss/trusca/blob/main/THIRD_PARTY_NOTICES.md                      |

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
- [ ] 3번(AI 코딩이 바꾼 조건) → 2부, 4번(SBOM 품질 격차) → 8번 연결을 말로 명시했는지
- [ ] 18번 닫는 문장을 보지 않고 말할 수 있는지
- [ ] 화면에 띄우는 URL 이 뒷자리에서 읽히는 크기인지
- [ ] 각 슬라이드가 표기된 길이 안에 들어가는지 — 넘치는 구간을 먼저 찾아 줄인다

시간이 지연될 때 축소 순서: Q&A → 18번 로드맵 → 12~13번 4단계.
9번 데모, 11번 자가진단, 8번 SBOM 정확도 구간은 마지막까지 유지한다.
