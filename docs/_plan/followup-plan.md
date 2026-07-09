# 후속 작업 계획 — P1 잔여 + BomLens + KWG 잔여 + P2 (2026-07-09)

> 근거: summit-review-findings.md 의 P1 구조 4건과 P2, STATUS.md 의 KWG 갭 잔여 항목, 사용자 지시.
> 사용자 지시 반영: (1) "KWG 동기화 범위 추가 확장"(금융권 가이드, 표준별 가이드 3종)은 후속 과제에서 제외.
> (2) SBOM 생성 도구로 BomLens 를 소개.

## BomLens 사실 확인 결과 (2026-07-09 실측)

BomLens 는 SK텔레콤 `sbom-tools` 저장소(github.com/sktelecom/sbom-tools)의 제품명이다.
우리 사이트는 이미 구명칭 "SK텔레콤 sbom-tools"로 소개 중이므로(docs/05-tools/sbom-generation/index.md:62-63,
glossary), 신규 추가가 아니라 명칭 갱신 + 기능 확장 소개다.

- 성격: local-first SBOM 생성기 + 오픈소스 위험 평가기. Docker 기반으로 전부 로컬 실행(SaaS 없음)
- 입력: 다중 언어 소스(Java, Python, Node.js, Go, Rust 등), 컨테이너 이미지, 바이너리와 RootFS, 펌웨어,
  기존 SBOM 재평가, HuggingFace AI 모델(ML-BOM 생성)
- 출력: CycloneDX SBOM(bom.json), 고지문(NOTICE.txt/html), 위험 리포트(risk-report), Trivy 보안 데이터
- 인터페이스: CLI, 웹 UI, 데스크톱 설치본(Windows/macOS)
- 엔진: syft, cdxgen, trivy 래핑. 라이선스 Apache-2.0. 최신 v1.7.0(2026-07)
- 이미지: `ghcr.io/sktelecom/bomlens`

도구 선정 정책(improvement-plan)과의 정합: 메인 도구는 syft 유지, BomLens 는 국내 큐레이션 계층의
통합 옵션으로 소개. ML-BOM 지원은 sbom-101 의 AI SBOM 절과 자연스럽게 연결된다.

## 실행 규약 (공통)

STATUS 선커밋, 청크별 DoD(수정 + en 쌍 + verify.sh 12/12 — 빌드는 커밋 게이트 강제),
우선순위 그룹이 끝날 때마다 gate-verifier 역순 독립 판정.

## 1순위 — P1 구조 잔여 4건 (근거: summit-review-findings P1 10~15)

- 청크 S1 — 고아 중복 페이지 2건 삭제: `docs/intro.md`(고유분인 소요 시간 비교는 start-path.md 에 흡수 검토),
  `docs/01-setup/method1-claude-md.md`. en 쌍 파일도 함께 삭제. 삭제 후 인바운드 링크 0건 재확인.
- 청크 S2 — iso42001.md 전재 축약: KWG 7-ai-compliance 와 동일한 표 5종을 걷어내고
  "경계 정의(코딩 도구 거버넌스 vs AI 시스템 컴플라이언스) + 5230/18974 운영 기업의 재활용 포인트 +
  A.6/A.7/A.10 교차표(요약) + KWG 원문 링크(CC BY 4.0 표기)"로 재구성. legal-considerations 와 상호 링크.
  분량 목표 60~80행. en 쌍 재작성.
- 청크 S3 — devsecops mdx 4종 섹션 순서: sast, sca, secret-detection, iac-security 에서
  분석기(샘플 미리보기 포함)를 설정 절 직후로 올리고 셀프 스터디를 그 뒤로. "위 분석기" 문구 정합.
  cicd-quick 의 배치가 선례. ko/en 8파일.
- 청크 S4 — SLA·VEX 정본 참조: sca.mdx 의 SLA 표를 "조직 강화안(KWG 기준선은 정본 참조)"으로 명시하고
  reference/concepts/vulnerability-response 링크, VEX 상세는 정본 위임. devsecops·ai-coding 의
  용어 첫 등장에 용어집 링크 표본 추가(과도한 링크는 피하고 페이지당 1~2개). ko/en.

## 2순위 — BomLens 소개 (사용자 지시)

- 청크 B1 — 본문 갱신: docs/05-tools/sbom-generation/index.md 의 tip 블록을 "BomLens (SK텔레콤)"로
  갱신 — 명칭, 입력 확대(펌웨어, 기존 SBOM, HuggingFace 모델), 출력(SBOM + 고지문 + 위험 리포트),
  인터페이스(CLI, 웹 UI, 데스크톱), local-first 특성, ghcr 이미지. 메인은 syft 유지 문구 보존.
- 청크 B2 — 연결: glossary 의 sbom-tools 항목을 BomLens 로 갱신, sbom-101 AI SBOM 절에
  "HuggingFace 모델의 ML-BOM 을 로컬에서 생성하는 도구로 BomLens" 한 문장,
  04-process 의 고지문(onot) 부근에 BomLens 고지문 생성 대안 여부 검토(중복이면 생략).
- 청크 B3 — en 쌍 동일 반영.

## 3순위 — KWG 갭 잔여 (동기화 범위 확장 제외)

- 청크 K1 — 취약점 대응 템플릿 상향(방향 명확, 바로 실행): templates/process/vulnerability-response.md 에
  CVSS v3.1/v4.0 병기(더 높은 점수 기준), EPSS 와 CISA KEV 보조 지표, KISA KNVD 소스 추가,
  VEX 4가지 상태값 통지 형식. 다운스트림 정합: output-sample/process/vulnerability-response.md,
  reference/samples/process 재생성(/update-reference-samples), 05-tools/vulnerability 본문과 모순 없는지 확인.
- 청크 K2 — 정책 템플릿 용어 정의(방향 제안 포함 실행): 본문의 "오픈소스 담당자" 단일 표기는 유지하되,
  부록 A(용어 정의)에 OSPO, OSPM, OSRB 를 "업계 통용 명칭" 참고로 추가하고 KWG 용어 표와 대응 관계 한 줄.
  초심자 우선 원칙과 KWG 정렬을 동시에 만족하는 절충.
- 청크 K3 — 조직 챕터 보강(방향 제안 포함 실행): 02-organization 배경에 팀별 1인 챔피언 모델과
  실명 지정 권고("전원" 표기는 요건 미충족)를 한 절로 추가, role-definition 템플릿에
  "내부 모범 사례 검증 담당" 역할(§4.1.2.6 수행 주체)을 선택 역할로 추가. 다운스트림 정합 확인.

## 4순위 — P2 일괄 (주제별 4묶음)

- 청크 P2-a — 도구 명령 소소한 낡음 일괄: gitleaks detect 를 git/dir 로, 이미지 ghcr 통일,
  trivy-action 고정 태그(+공급망 사고 각주), ZAP 액션 2종 상향, tfsec 이관 단서, Semgrep Community Edition
  표기, GHAS 분리 표기, syft 예시 버전, get.anchore.io 설치 경로, docker-compose version 키.
  전체 목록은 summit-review-details.md 의 Agent A 절.
- 청크 P2-b — docs/website 구조·문체: 사이드바 잔여(개요 라벨, 챕터 1~7 카테고리, 05-tools 종속 표현),
  문체 혼용 정리, ko-style S2 35건, 단계 번호 잔재, intro 표·라벨 불일치, 초장문 샘플 상단 목차.
- 청크 P2-c — en 품질: intro 재번역, 볼드 공백 아티팩트 일괄, 02-organization title 대문자화.
- 청크 P2-d — Rules 템플릿 7곳 중복 단일화(발췌 + 정본 링크 또는 MDX partial) + 도구 페이지 공통 구조
  보완("적용 확인" 절) + 하네스 개선(verify.sh 단계별 실패 원인 기록).

## 보류 (별도 결정 대기)

- KWG 동기화 범위 추가 확장 — 사용자 지시로 제외 (2026-07-09)
- AI SBOM 독자 전용 실습 챕터 — 수요 확인 후
- rules-template 생성기의 키 없는 미리보기 추가 등 데모 UX 통일 — P2-d 진행 시 범위 재평가

## 예상 규모

1순위 청크 4개(반나절), 2순위 청크 3개(2~3시간), 3순위 청크 3개(하루), 4순위 청크 4개(하루 이상).
각 순위 종료 시 역순 독립 검증 후 다음 순위로 진행.
