# TrustedOSS 개편 — 실행 현황 (resume용)

> 목적: 긴 세션에서 히스토리가 유실돼도 이 파일만 보면 즉시 재개 가능. 매 task 후 갱신·커밋한다.
> 최종 갱신: 2026-07-09

## 후속 작업 (followup-plan, 2026-07-09) — 진행 중

> 계획 승인본: docs/\_plan/followup-plan.md. 재개 시 미체크 청크부터.
> DoD = 수정 + en 쌍 + verify 12/12(커밋 게이트), 순위 종료마다 gate-verifier 역순 판정.

- [ ] 1순위 S1: 고아 페이지 2건 삭제 (docs/intro, 01-setup/method1 + en 쌍)
- [ ] 1순위 S2: iso42001.md 전재 축약 (60~80행 재구성 + CC BY)
- [ ] 1순위 S3: devsecops mdx 4종 섹션 순서 (분석기를 설정 직후로)
- [ ] 1순위 S4: SLA·VEX 정본 참조 (sca 강화안 명시 + concepts 링크)
- [ ] 1순위 게이트
- [ ] 2순위 B1~B3: BomLens 소개 (sbom-generation, glossary, sbom-101, en)
- [ ] 3순위 K1: 취약점 템플릿 상향 + 다운스트림 재생성
- [ ] 3순위 K2: 정책 용어 부록 (본문 단일 표기 유지)
- [ ] 3순위 K3: 조직 챔피언 모델·검증 담당 역할
- [ ] 2·3순위 게이트
- [ ] 4순위 P2-a~d: minor 일괄 (도구 명령 / 구조·문체 / en / Rules 단일화·하네스)
- [ ] 최종 게이트 + STATUS 마감

## Summit P1 수정 작업 (2026-07-09) — 완료

> 근거: summit-review-findings.md P1 절. 범위: 동작·정확성 계열 13건 + Node20 액션 일괄.
> 구조 다듬기 4건(고아 페이지, iso42001 축약, mdx 순서, SLA 정본 참조)과 P2, KWG 잔여 4건은 발표 후 후속.

- [x] 청크 1: AI 코딩 도구 지형 5건 — agent 산출물 .cursor/rules 와 .windsurf/rules, CONVENTIONS.md 로 전환,
      Copilot 조직 지침·경로 한정 지침·AGENTS.md 반영, Windsurf 소속 정정(Cognition), AGENTS.md 공통 트랙,
      ISO 42001 조항 A.6/A.7/A.10 정정 — `29813b7`
- [x] 청크 2: EO 14028 재서술(EO 14306, OMB M-26-05, 위험 기반 전환) + CRA 2026-09-11 보고 의무 — `9ffcc57`
- [x] 청크 3: ISO 인용 3곳(3.3.2 사용 사례 처리, 교육 역량 문구, en 4.x 표기) + Artifex 소각하 기각·합의,
      Log4Shell 약 80만 건, XZ 개발·베타 한정 — `7728772`
- [x] 청크 4: reference 프로필 허위 안내 삭제, sbom-101 링크화, 04-process 6번째 프로세스 신설,
      verify 12/12 표기 일괄, README 시간·메뉴·산출물 표 정합(23문서+SBOM), KWG 출처와 CC BY 표기 — `3bf349a`
- [x] 청크 5: Node20 액션 일괄 상향(checkout v7, upload-artifact v7, gitleaks v3, codeql v4 + build-mode,
      scan-action v7 + outputs 경로) — `4703d83`
- [x] 최종 게이트: gate-verifier 역순 판정 **전 청크 PASS** + verify.sh 12/12

## AI SBOM 동기화 + 법적 고려 보강 (2026-07-09) — 완료

> 계획 승인본: `docs/_plan/ai-compliance-sync-plan.md`.

- [x] 청크 A1: sync-kwg-reference.sh 에 ai-sbom_guide 추가 + 19파일 동기화 — `31ffc42`
- [x] 청크 A2: kwg-mapping.yaml guide_mappings 3건 + drift 기준점 — `206d383`.
      게이트가 발견한 결함 2건 후속 수정: 스냅샷이 삭제 상태로 커밋돼 콜드 스타트 감지 불능(`8abd64e`
      복구), drift 스크립트가 매 실행 기준선을 재기록해 drift 은폐와 트리 오염 유발(`6ee0fa5` 읽기 전용화)
- [x] 청크 A3: sbom-101 "AI SBOM" 절 + iso42001 링크, en 쌍 — `3ca635f`
- [x] 청크 B0: 사실 검증 — KWG 원문 대비 정정 4건 확인(정량 귀속 기준 없음, Anthropic 제도명은
      Commercial ToS Section K, Microsoft 필터 조건 2026-04 제외, 표시 의무 주체는 제공 사업자)
- [x] 청크 B1+B2: legal-considerations.md 신설 + 사이드바, intro 표(누락 2행 보완), strategy 링크,
      templates/policy §5 원칙 4~6 추가 — `b46210b`
- [x] 청크 B3: en 쌍 — `8dbda10`
- [x] 최종 게이트: gate-verifier 역순 판정 1차 미통과(A2) 후 수정, **재판정 통과** + verify.sh 12/12

잔여 후속(선택): 상류 finance-oss-guide 와 iso 표준별 가이드 3종의 동기화 여부, AI SBOM 독자
전용 챕터(실습 포함), verify.sh 가 단계별 stderr 를 버려 실패 원인을 남기지 않는 문제 개선.

## Summit P0 수정 작업 (2026-07-09) — 완료

> 재개 방법: 아래 미체크 청크부터. DoD = 해당 수정 + en 쌍 동기화 + verify.sh 12/12,
> 전 청크 완료 후 ko/en 빌드 + gate-verifier 역순 판정. 근거는 summit-review-findings.md P0 절.

- [x] 청크 1 (P0-1): static/tools 6종 모델 ID 교체 (claude-sonnet-5) — `18e986d`
- [x] 청크 2 (P0-2): devsecops/iso-mapping.md 18974 표 재작성 + en 쌍 — `df27f07`
- [x] 청크 3 (P0-3): 동작 불능 안내 9건 교정 + en 쌍 6파일 — `c0f89f2`
- [x] 청크 4 (P0-4): og:image 도메인 교체 — `b1f3192`
- [x] 청크 5 (P0-5): en navbar 키, `__ISO13__` 4건, Hero Translate — `5a6af66`
- [x] 청크 6 (P0-6): KWG 재동기화(`8ba6b83`) + 의미론적 갭 분석 + 즉시 반영 2건 + 스냅샷 reset.
      즉시 반영: (a) kwg-mapping.yaml — 도구 10종과 18974 §4.x.x 매핑 추가,
      드리프트 오탐 2건(정책 템플릿 자체 절 번호, ISO 42001 조항)을 제외 목적으로 등재,
      (b) 통합 매핑 항목 수 표기 정정 25→31, 공통 10→11, 40%→약 35%
      (00-overview index+CLAUDE, intro, 07-conformance index+CLAUDE, en 쌍 3파일).
      표준별 입증자료 25개 표기(samples/conformance, 07 agent)는 상류 공식 집계와 일치해 유지.
- [x] 최종 게이트: gate-verifier 역순 독립 판정 **청크 1~6 전 항목 PASS** + verify.sh 12/12
      (ko/en 빌드는 커밋 게이트가 매 커밋 강제 — 전 커밋 통과). P0 종료.
      다음 작업: 보고서 P1 17건 (사용자 지시 대기), 위 "KWG 갭 분석 — 검토 후 결정" 7건.

### KWG 갭 분석 — 검토 후 결정 항목 (후속, 사용자 방향 필요)

> 갱신(2026-07-09): 아래 1번(동기화 범위 확장)은 사용자 지시로 후속 과제에서 제외.
> 나머지의 실행 계획은 docs/\_plan/followup-plan.md 참조 (BomLens 소개 과제 추가됨).

1. 동기화 범위 확장: 상류 신규 가이드 5종(ai-sbom_guide, finance-oss-guide, iso5230/18974/42001_guide)이
   sync-kwg-reference.sh 범위 밖. 최소 ai-sbom_guide 추가 권고(발표 주제 직결).
2. templates/process/vulnerability-response.md — CVSS v3.1/v4.0 병기, EPSS와 CISA KEV 보조 지표,
   KISA KNVD, VEX 통지 형식 (상류 요구 상향 반영).
3. templates/policy/oss-policy.md — OSPO/OSPM/OSRB 용어 정의 (coverage-matrix 갭 #1과 묶어 처리).
4. 02-organization — §4.1.2.6 검증 담당 역할, 팀별 1인 챔피언, 실명 표기 권고.
5. website/ai-coding — AI 생성 코드 저작권 귀속, 공급자 IP 보증, EU AI Act §50/한국 AI 기본법
   표시 의무 3주제 보강 (현재 미커버, 상류 7-ai-compliance §5 신설 대응).
6. docs/05-tools — 상류 신규 도구 가이드 3종(cdxgen-dt, scanoss, onot) 외부 링크 추가.
7. kwg-mapping.yaml guide_mappings 에 0-openchain, 7-ai-compliance 항목 추가(감시 사각지대 해소).

## Summit 대비 사이트 개선 검토 (2026-07-09) — 보고 완료, 수정 진행 중 (위 작업 로그)

Open Source Summit Korea 발표 대비 전수 검토. 결과: `docs/_plan/summit-review-findings.md`.
방법: 로컬 하네스 점검 + 독립 검토 에이전트 7개(최신성 3, 구조 2, 가치 1, 일관성 1) + gate-verifier 교차 검증.

- **P0 6묶음 (발표 전 필수)**: 브라우저 도구 6종이 은퇴 모델(claude-sonnet-4-20250514, 2026-06-15 retired)
  하드코딩으로 불능 추정 / devsecops iso-mapping 의 18974 매핑 표 스펙 불일치(존재하지 않는 §4.2.3 포함) /
  따라 하면 동작 안 하는 안내 7건(Aider, hooks, Skill 형식, semgrep-action, nuclei-action, secrets-if, cdxgen 이미지) /
  og:image 가 미해석 도메인(trustedoss.dev) / en navbar 한국어 노출 + `__ISO13__` 4건 /
  KWG 동기화 2026-04-15 정지(이후 70커밋, AI SBOM 가이드 등 미반영)
- **P1 17건**: AI 코딩 도구 지형(AGENTS.md 표준화, Cursor 형식, Copilot 조직 지침, Windsurf 소속),
  EO 14028 낡음, Node20 액션 일괄, ISO 인용 오매핑 3건, 법적 사례 서술, 고아 페이지 2건,
  iso42001 KWG 전재 + 출처 미표기, 수치 불일치(verify.sh 11/11 표기 등), CC BY 표기 미완
- **P2 40여 건**: 도구 명령 소소한 낡음, docs/website 구조 다듬기, en 품질, ko-style 잔여(S2 35, S3 78)
- 잘 유지되는 것: 61페이지 중 53페이지 고유 가치 명확, ISO 존재하지 않는 조항 인용 0건, verify.sh 12/12

다음 작업: 보고서 승인 후 "권고 실행 순서"(보고서 말미) 1번부터 — 즉시 항목은 모델 ID 교체,
og:image 도메인, en navbar 키, 18974 매핑 표, `__ISO13__` 4건.

## 콜드스타트 발견 수정 작업 (2026-06-10) — 완료

> **재개 방법**: 아래 미체크 청크부터 진행. DoD = 해당 항목 수정 + en 쌍 동기화 +
> `verify.sh` 12/12 + (glossary/Term 변경 시 `cd website && npm run build`) 통과 후 커밋.
> 발견 상세·근거는 `docs/_plan/cold-start-findings.md` (M1~M4, m1~m9).

### 청크 체크리스트

- [x] **청크 0**: 이 작업 로그 신설 + 커밋
- [x] **청크 1 (M1·M2)**: `.github/workflows/sync-agents.yml`에 samples/, output-sample/
      추가 (on.push.paths + rsync 2줄, 기존 패턴 그대로). `.github/agents-repo/README.md`가
      구조를 나열하면 두 디렉토리 항목 추가
- [x] **청크 2 (M3·M4)**: quick-start.md §2 `:::tip` 직전에 클론 선행 안내+명령 추가 /
      OSV Maven name을 `org.apache.logging.log4j:log4j-core`로 수정
      (tools-setup.md 74·88행, vulnerability/CLAUDE.md 65행, en tools-setup.md 74·88행).
      주의: sbom-generation index·sbom-101의 `log4j-core`는 SBOM name 필드라 수정 금지
- [x] **청크 3 (m1~m9)**: 01-setup 도구 표 Docker "필수"→"챕터 05만 사용(대체 경로 있음)"(m1),
      체크리스트 docker 항목 생략 단서(m2), quick-start Term 풀이 openchain·자체인증(m3,
      필요 시 `website/src/data/glossary.ts` 키 추가), sbom-generation licenses 빈 값
      주의문(m4), vulnerability 예시 "12개"→"4개"(m5), docker-cicd cdxgen 폴백 출력 경로
      output/sbom/ 일치(m6, 수정 후 Docker 실측), 트러블슈팅 파일 공유 행 추가(m7),
      05-tools index grype→OSV·Dependency-Track(m8), agent 완료 확인 `ls output/organization/`
      한 줄(quick-start·01-setup, m9). **전부 en 쌍 동일 수정**
- [x] **청크 4 (최종 게이트)**: gate-verifier 독립 판정 **13/13 PASS** (역순 검사, OSV curl
      실호출 확인, verify.sh 12/12). M4 curl 실측(7건 반환)·m6 cdxgen 실측(output/sbom/ 생성,
      components 2) 완료. cold-start-findings.md에 처리 결과 기록.
      게이트가 발견한 범위 밖 기존 결함: en sbom-101.md `__ISO13__` 플레이스홀더 4건
      (커밋 052d283 유입) — 후속 후보로 등록
- [x] **push 후 검증**: sync 워크플로우(run 27249199927) success → trustedoss-agents 새 클론에
      samples/와 output-sample/ 추적 파일 37개 확인, 샘플 3종 존재, 문서 명령
      `cp output-sample/sbom/fixture-sample.cdx.json output/sbom/` 성공(components 5) — M1·M2 최종 확정

## 콜드스타트 실사용자 검증 (2026-06-10) — 발견 보고 완료, 수정은 후속

사전 지식 차단 에이전트 2개(P1 스타트업/Docker 불가, P2 중견기업/풀코스)가 공개 사이트만
보고 00→07을 따라가며 명령을 실제 실행. 결과: `docs/_plan/cold-start-findings.md`.

- **major 4건**: 공개 클론 저장소(trustedoss-agents)에 samples/ 부재(M1, 빈 SBOM 조용한 실패),
  output-sample/ 부재(M2, Docker-없이 분기 막힘), quick-start 클론 안내 누락(M3),
  OSV Maven 패키지명 형식 오류(M4, 문서 명령이 `{}` 반환)
- minor 9건 (문서 한 줄 수정 수준), 잘 작동한 것 4건, 체인 검증 9/9 PASS
- **다음 작업(후속)**: M1·M2는 trustedoss-agents 동기화 범위 결정 필요. M3·M4는 문서 한 줄 수정.

## 재개 방법

1. `git checkout feat/ia-kwg-revamp`
2. 계획 정독: `docs/_plan/improvement-plan.md` (승인본). 실행 규약은 그 파일 "실행 규약" 절.
3. KWG 커버리지 근거: `.claude/reference/kwg-coverage-matrix.md`
4. 아래 "다음 작업"부터 이어서 진행. 매 task는 완료 정의(DoD) 통과 시에만 완료 처리.

## 작업 브랜치

`feat/ia-kwg-revamp` (main에서 분기, task별 커밋, Co-Authored-By 트레일러 금지)

## 완료 정의(DoD) 요약

task 고유 수용 기준 + `cd website && npm run build`(ko/en) + `verify.sh` 12/12 + (UI면) 헤드리스 캡처 + (KWG면) 커버리지 100%. KO(주 로케일) 빌드는 broken link 0이어야 함.

## 진행 상태

| #   | 작업                                             | 상태 |
| --- | ------------------------------------------------ | ---- |
| 12  | 메뉴 라벨(오픈소스 관리, AI 코딩 거버넌스)       | 완료 |
| 13  | KWG 커버리지 매트릭스                            | 완료 |
| 14  | 정책 템플릿 KWG 정렬(용어 정의·사내 공개·추적성) | 완료 |
| 15  | 온보딩: 5분 빠른 시작 + 내게 맞는 시작 경로      | 완료 |
| 16  | AI 에이전트 허브 페이지                          | 완료 |
| 17  | 05-tools 통합 인덱스 + 세 기둥 cross-link        | 완료 |
| 18  | P1: 단일 출처, 검색, 매핑 정본                   | 완료 |
| 19  | 도구(onot/sbom-tools) + POSITIONING 차별화       | 완료 |

마일스톤: **P0-0(#13, #14), P0(#15, #16, #17), P1(#18), 마무리(#19), P2 완성도(#9·#10·#11) + 브랜드 수렴 전부 완료.**

## P2 완성도 + 브랜드 (브랜치 feat/p2-completeness)

- DevSecOps/AI코딩 사이드바 대칭화(P2 #11, `6c25e52`): 양쪽 4카테고리 정합 + AI코딩 orphan 3페이지 편입.
- 진행 가시화(P2 #10, `003c521`): JourneyProgress(7단계 진행률, localStorage) + Prerequisite(전제조건 배지). MDXComponents 전역 등록.
- 레퍼런스 정합(P2 #9, `0c46ca0`): Best Practice 표 보완, "준비 중" 8곳 실제 링크화, 에이전트 가이드 링크, 용어집 보강.
- 브랜드 토큰(`56cc53a`): 수렴은 이미 코드에 적용돼 있었음(주색 Material/Google 블루 #1a73e8, 폰트 Roboto). POSITIONING §6 기록만 실제와 일치시킴. 색 변경 없음. 포털 측 수렴은 별도 과제.
- 검증: verify.sh 12/12, ko/en 빌드 0 broken.

## 후속(미완) 항목 — 전부 처리 완료

- 프로세스 템플릿 추적성 헤더: **완료**(`4f4cbb4`). templates/process/\* 6개 + output-sample/process 5개 + reference/samples/process에 KWG 6대 프로세스 정렬 헤더 표면화.
- 정책 샘플 §10 drift: **완료**(`4f4cbb4`). reference/samples/policy에 §10(정책 변경 요청·운영) 보강.
- en 패리티: **완료**(`7ed96f7`). 정본 2페이지 EN 번역, 본문 4개 단일출처 동기화, 온보딩 4페이지 번역. en i18n quirk(4건)는 미번역 폴백이 원인이었고 번역 추가로 해소 — 이제 **ko/en 모두 broken link 0**.
- ko-style 잔재: **완료**(`9739f49`). 가운뎃점 나열 S2 7건 정리(checklist-mapping, devsecops/intro, POSITIONING §1~3). 07-conformance §감사이력의 부분충족 표시 기호(다이아몬드 이모지)는 gap-analysis 산출물의 상태 범례(충족/부분충족/미충족)와 일치하는 의미 기호라 보존. S3 화살표 장식 25건은 권고 수준이라 보류.
- `00-overview/index.md` 본문 축약 보류 — 온보딩 진입은 quick-start + 랜딩 CTA + 에이전트 허브로 달성.

## 다음 작업 (계획 전 범위 + 후속 종료)

계획의 P0-0부터 마무리(#19)까지, 그리고 위 후속 4건까지 전부 완료. 추가 지시 없으면 작업 없음. 잔여 후보(선택): S3 화살표(→) 산문 정리, en 본문의 산발적 미번역 코드주석.

### 후속에서 완료한 것 (참고)

- #10 프로세스 템플릿 추적성 헤더, #11 정책 샘플 §10, #12 en 패리티(quirk 해소 포함), #13 ko-style 가운뎃점 정리.

### #19에서 완료한 것 (참고)

- 도구 큐레이션: onot(04-process 배포 전 고지문, SPDX 입력 OSS 고지문 생성, github.com/sktelecom/onot), SKT sbom-tools(05-tools/sbom-generation 보완, cdxgen·syft 파이프라인+Trivy, 메인은 syft 유지). FOSSLight/SW360/FOSSology는 기존 KWG tools 링크로 이미 연결됨.
- POSITIONING.md §7 "OpenChain KWG와의 관계(보완 레이어)" 신설 — KWG=무엇을·왜 / TrustedOSS=어떻게·자동으로, 차별점 5축 표.
- 랜딩 WhyKwg 섹션 신설(`website/src/components/Home/WhyKwg`, Showcase와 FinalCTA 사이). 중립 Infima 토큰(POSITIONING §5), en code.json 번역 추가. ko/en 홈에서 렌더 확인.
- 독립 검수(doc-qa): high 0. med 1건(03-policy 샘플 AGPL Strong→Network Copyleft) 즉시 수정.
- 최종: build ko/en SUCCESS, KO 0 broken, verify 12/12.

### #18에서 완료한 것 (참고)

- 단일 출처화: `reference/concepts/license-classification`, `reference/concepts/vulnerability-response` 정본 신설(사이드바 "개념 심화" 등록). 03-policy·04-process·05-tools/vulnerability 본문은 표 제거 후 정본 링크. 00-overview/index 비교표는 핵심 3행으로 축약 + checklist-mapping 정본 링크.
- 검색: `@easyops-cn/docusaurus-search-local` 테마 추가(language ko/en, docs와 devsecops, ai-coding, reference 인스턴스 인덱싱). ko/en search-index 생성과 navbar 검색창 렌더 확인.
- 매핑 정본: devsecops/ai-coding iso-mapping이 이미 checklist-mapping을 정본 참조 중(추가 작업 불필요).
- 정책 부록 A/B + 추적성 헤더를 output-sample/policy, reference/samples/policy에 반영.

## 핵심 결정 (drift 방지용 고정값)

- 미션: AI·도구로 OpenChain 2026(5230·18974) 관리를 쉽고 정확하게 + DevSecOps 자동화 + AI 코딩 거버넌스. 1차 대상=처음 맡은 담당자.
- 포지셔닝: KWG의 실행·자동화 레이어(경쟁 아님). CC BY 4.0 출처 표기, KWG 연계 명시.
- 상단 메뉴: 오픈소스 관리 / DevSecOps / AI 코딩 거버넌스 / 레퍼런스(유지) + 검색.
- 확정 라벨: 내게 맞는 시작 경로, 표준 요구사항 한눈에, (DevSecOps)표준 연계(18974), (AI)실전 적용.
- 디자인: 이미 구현된 Gemini 문서 look&feel 위에서. 신규 페이지/컴포넌트도 동일 시스템.
- 콘텐츠 패턴: 모든 주제 보기(무API키 데모/샘플) → 해보기(에이전트/도구 복붙) → 자동화(CI/Rules).
- 정적 데모 링크는 `pathname:///tools/<file>.html`(verify.sh가 pathname: 스킵하도록 수정됨).
- 정책/프로세스는 KWG 절 구조에 정렬 + 가치 항목은 확장으로 구분.
- 도구: 국제(syft/grype/trivy/cdxgen/OSV/Dependency-Track) + KWG생태계(FOSSLight/SW360/FOSSology) + 국내(onot 고지문, SKT sbom-tools).

## 핵심 발견·결정 로그

- #13: 산출물 세트 전체로는 KWG 거의 전 절 충족. 실제 갭 3개(용어 정의, 사내 공개 조건부, 추적성).
- #14: 정책 소스 템플릿에 부록 A(용어), 부록 B(사내 공개), 추적성 헤더 추가로 갭 해소(소스 기준).
- #15: 정적 데모는 `pathname://` 링크 + verify.sh가 이를 스킵하도록 수정. en i18n quirk 확인(ko 무관).
- #16: AI 에이전트 허브(`docs/00-overview/agents.md`) 신설.
- #17: `docs/05-tools/index.md` 신설(카테고리 link로 연결). 07-conformance에 "자동화로 확장" 분기, devsecops→AI코딩 상호 링크, checklist-mapping 라벨 "표준 요구사항 한눈에".
- #19: 도구 사실 확인(WebSearch/WebFetch) — onot은 github.com/sktelecom/onot(SPDX 입력으로 OSS 고지문 생성, Kakao와 SKT 공동), sbom-tools는 github.com/sktelecom/sbom-tools(내부 cdxgen과 syft 파이프라인에 Trivy, CycloneDX 1.6, 소스/Docker/바이너리/RootFS 분석, Apache-2.0). 계획의 "syft, cdxgen 래핑" 주장 사실 확인됨. FOSSLight, SW360, FOSSology는 이미 KWG tools 링크로 연결돼 추가 불필요. POSITIONING은 가이드 대 포털(SCA 제품) 축이라 KWG 차별화는 별도 §7로 신설. yarn과 corepack, playwright가 없어 락 immutable과 픽셀 캡처는 직접 검증 못 함(빌드 HTML로 UI 확인, yarn.lock은 정상 포맷으로 판단).
- #18: 단일 출처화 핵심 발견 — CVSS 대응 기한표가 04-process(KWG 기준선 Critical 1주)와 05-tools/vulnerability(운영 SLA Critical 24h)에서 값이 **달랐음**. 정본 페이지에서 "기준선 + 조직 SLA 강화안"으로 통합해 불일치 해소. 매핑 정본(#8)은 이미 두 iso-mapping이 checklist-mapping을 정본 참조 중이라 추가 작업 불필요였음. Diátaxis(#6)는 단일 출처용 reference 개념 페이지 신설로 부분 달성(개념=reference, 본문=링크).
