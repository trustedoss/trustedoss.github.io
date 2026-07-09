# TRUSCA 로드맵 제안 — OSSRA 2026 웨비나 수요 기반 (2026-07-09)

> 목적: Black Duck x KMS Technology "2026 OSSRA Report" 웨비나 질문 약 90건을 분석해,
> TRUSCA(github.com/trustedoss/trusca, Apache-2.0 self-hosted SCA)가 그 수요를 어디까지 지금 충족하고
> 무엇을 더하면 시장 공백을 메우는지 정리한다. 이 문서는 trustedoss.github.io 사이트가 아니라 TRUSCA
> 저장소로 전달할 제안서 성격이다(로드맵 소관은 TRUSCA repo).

## 배경 — 왜 이 질문들이 곧 TRUSCA의 타깃인가

웨비나 질문의 큰 축은 두 가지였다. (1) AI 코딩·에이전트 환경의 오픈소스 통제, (2) 상용 SCA 도입 장벽
(예산과 인력 부족, 폐쇄망, 구축 공수). TRUSCA 는 (2)의 구조적 대안이므로(무료이고 self-hosted 이며
Black Duck/Snyk 급 기능), 이 질문 리스트는 사실상 TRUSCA 잠재 고객의 목소리다.

TRUSCA 현재 기능(README 실측 2026-07-09): 컴포넌트 탐지(cdxgen, 30+ 생태계, direct/transitive),
컨테이너 스캔(Trivy), SBOM 수입(CycloneDX/SPDX, 적합성 채점), 취약점(Trivy 통합 DB = NVD+OSV+GHSA
+EPSS+KEV, 주간 갱신), EPSS/KEV 컬럼·정렬·정책 임계값, VEX 수출입 + 7단계 triage, 라이선스 3계층 정책

- forbidden 빌드 차단 + NOTICE 자동 생성, CI 게이트(GitHub/GitLab/Jenkins), 컴포넌트 승인 워크플로,
  RBAC·감사 로그, Compose/Helm 배포.

## 수요 대비 갭 — 우선순위별 제안

### P1 — 최다 요구, 시장 차별화 큼

**1. Reachability(도달 가능성) 분석**

- 수요: 우선순위 클러스터에서 단일 기능으로 가장 많이 요구됨. "NVD CVE 가 우리 앱에서 도달 불가능한
  Path 에 있는 경우가 많다"(신유진), "CVSS 뿐 아니라 실행 경로까지"(곽원기), "런타임 호출 가능한
  위험만 우선순위화"(오상진). Black Duck 도 이걸 답으로 내세움.
- 현재: TRUSCA 는 EPSS/KEV 로 악용 "확률"은 반영하나 "우리 코드에서의 도달 여부"는 없음.
- 제안: call-graph 기반 정적 reachability(최소한 direct import 여부 → 함수 수준). 완전한 분석이 어렵다면
  1차로 "취약 함수가 우리 의존성 그래프에서 실제 참조되는가" 수준부터. VEX 자동 초안 생성과 연결하면
  triage 부담이 크게 준다.
- 가치/난이도: 가치 최상 / 난이도 상. 언어별 편차 커서 단계적.

**2. 에이전트 시점 검증 — TRUSCA 정책 조회 MCP 서버 / pre-flight API**

- 수요: AI 클러스터의 핵심 미충족. "AI Agent 가 선택한 오픈소스를 자동 검증·승인/차단하는 Agent 기반
  거버넌스"(신유진), "AI 코딩 환경에서 오픈소스 유입 자동 탐지·통제"(곽원기), "사내 리포지토리·프록시
  단계 베스트 프랙티스"(김광덕). 벤더도 원론 수준으로만 답함.
- 현재: TRUSCA 는 빌드 후 게이트(exit 1)까지는 있으나, 코드 생성 "시점"의 사전 질의가 없음.
- 제안: 정책 조회 pre-flight 엔드포인트(`POST /v1/policy/check` — 패키지·버전·라이선스 입력 →
  allow/conditional/forbidden + 이유 반환)를 만들고, 이를 감싸는 **MCP 서버**를 제공. 에이전트가 패키지를
  추가하기 전에 TRUSCA 정책을 질의해 스스로 차단·대안 제시. 사이트의 agent-governance 페이지와
  결합하면 "AI 에이전트 오픈소스 거버넌스"의 실행 도구로 시장에 없는 조합이 된다.
- 가치/난이도: 가치 최상(차별화) / 난이도 중. 정책 엔진은 이미 있어 API+MCP 래퍼 중심.

### P2 — 반복 요구, 경쟁 대응

**3. Operational Risk 점수 (프로젝트 건강도)**

- 수요: EOL·좀비 컴포넌트 클러스터(9건). "유지보수 중단 프로젝트도 식별"(오준배), "CVE 점수보다 활성도·
  Release 주기·Commit 빈도"(신유진). Black Duck 이 Operational Risk 를 차별점으로 답함.
- 현재: TRUSCA 에 없음(최신성 대비 버전 수는 있음).
- 제안: deps.dev / OpenSSF Scorecard / ecosyste.ms 같은 공개 데이터로 컴포넌트별 활성도(마지막 릴리스,
  커밋 빈도, 아카이브 여부)를 점수화해 별도 리스크 축으로 노출. 교체 우선순위 산정에 활용.
- 가치/난이도: 가치 상 / 난이도 중(외부 데이터 연동).

**4. 라이선스 비호환 자동 감지 + 대체 추천**

- 수요: 라이선스 클러스터(10건). "서로 호환되지 않는 라이선스가 얽혔을 때 자동 감지·대체 추천"(김광덕),
  "GPL 계열 실수 포함 예방"(방성현). SSPL·BSL 등 신규 라이선스 추적(신유진).
- 현재: TRUSCA 는 3계층 분류·차단은 하나, 컴포넌트 간 라이선스 조합 비호환(예: Apache-2.0 vs GPL-2.0)
  자동 감지는 없음.
- 제안: 라이선스 호환성 매트릭스로 프로젝트 내 조합 충돌을 플래그. 동적 카탈로그로 SSPL/BSL 등 신규
  라이선스 반영(로드맵의 per-team 정책 편집과 함께).
- 가치/난이도: 가치 상 / 난이도 중.

**5. 반입 단계 공급망 공격 검사 (typosquatting / dependency confusion)**

- 수요: 공급망 클러스터(8건). "Dependency Confusion·Typosquatting 탐지"(신유진), "악성 패키지 반입 차단
  프록시 베스트 프랙티스"(김광덕). 사이트는 04-process 에 반입 게이트 패턴을 문서화했으나 탐지 도구는 없음.
- 현재: TRUSCA 컴포넌트 승인 워크플로가 반입 승인에 부분 대응.
- 제안: 반입(ingest) 시 패키지명 유사도(typosquatting), 내부/공개 네임스페이스 충돌(dependency
  confusion), 신규·저평판 패키지 플래그. 사이트 agent-governance·04-process 반입 게이트와 짝을 이룸.
- 가치/난이도: 가치 상 / 난이도 중.

### P3 — 운영 성숙, 자산 연계

**6. AI/ML 모델 SBOM(ML-BOM) 수입 — BomLens 연계**

- 수요: "조직 49%가 AI/ML 모델을 직접 포함하나 매니페스트에 없어 기존 도구로 가시성 어렵다"(김광덕),
  "AI SBOM 가시성"(류원옥 ETRI). 사이트는 5.4 AI SBOM 챕터 + BomLens 로 생성은 커버.
- 제안: BomLens 가 만든 CycloneDX ML-BOM 을 TRUSCA 가 수입해 모델 라이선스·정보 공백을 리스크로 표시.
  생성(BomLens) → 관리(TRUSCA) 파이프라인 완성.
- 가치/난이도: 가치 중상 / 난이도 중(수입 파이프라인은 이미 있음, 모델 컴포넌트 타입 처리 추가).

**7. KPI 대시보드 (거버넌스 정량 지표)**

- 수요: "정량 평가 지표 — 취약점 조치율, MTTR, SBOM 커버리지, 라이선스 위반"(곽원기), 성숙도 로드맵.
- 현재: 프로젝트 리스크 롤업은 있으나 시계열 KPI 는 없음.
- 제안: MTTR, 조치율, SBOM 커버리지, 라이선스 위반 추이 대시보드. 사이트의 성숙도 모델과 연결.
- 가치/난이도: 가치 중 / 난이도 중.

**8. 폐쇄망 오프라인 운영 가이드 + DB 미러**

- 수요: "폐쇄망/사설망 인프라 선결 조건"(박선희), 금융·공공(신유진). 벤더가 "오픈소스 DB 는 SaaS 연결
  필요"라 답한 지점에서 TRUSCA 의 self-hosted 가 구조적 우위.
- 현재: self-hosted 이나 Trivy DB 주간 갱신이 네트워크 전제. 폐쇄망 오프라인 미러 절차 문서 필요.
- 제안: Trivy DB 오프라인 미러 + 정기 반입 절차를 문서화(기능보다 운영 가이드). 사이트에서 이 가이드로 링크.
- 가치/난이도: 가치 중(세그먼트 결정적) / 난이도 하(주로 문서).

## 이미 TRUSCA 로드맵에 있는 것 (참고)

Excel·컴플라이언스 PDF 리포트, 동적 per-team 정책 편집, Hosted read-only demo. 위 4번(라이선스)·7번
(KPI)이 이들과 묶여 진행되면 효율적이다.

## 요약 — 권장 착수 순서

1. 에이전트 pre-flight 정책 API + MCP 서버 (P1-2) — 난이도 중, 차별화 최상, 사이트 자산과 즉시 결합
2. Reachability 1차(의존성 그래프 참조 여부) (P1-1) — 가치 최상, 단계적
3. Operational Risk 점수 (P2-3) — 공개 데이터 연동으로 경쟁 대응
4. 반입 공급망 공격 검사 (P2-5), 라이선스 비호환 감지 (P2-4)
5. 폐쇄망 가이드(P3-8, 문서), BomLens ML-BOM 수입(P3-6), KPI 대시보드(P3-7)

각 항목은 웨비나 실제 질문을 근거로 하며, 1·5는 trustedoss.github.io 의 agent-governance / 5.4 AI SBOM /
04-process 콘텐츠와 직접 연동되어 "가이드 + 도구"의 통합 스토리를 만든다.
