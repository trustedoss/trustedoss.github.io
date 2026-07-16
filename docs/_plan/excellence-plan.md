# 전 영역 완성도 상향 계획 (2026-07-16)

> 근거: 멀티 에이전트 전수 감사 결과 `full-audit-findings-2026-07.md` (finder 22유닛 + P0/P1
> 적대적 검증, 총 160 에이전트). 발견 252건 중 반박 4건 제외, 확정 P0 24 / 확정 P1 110 /
> 미검증 P1 13 / P2 101건을 수정 대상으로 한다.
> 사용자 결정(2026-07-16 인터뷰): 목적은 전 영역 균형 상향, 대상은 docs, agents, website, en 전부,
> 일정 제약 없음.

## 운영 원칙

- DoD(청크 공통): 수정 + `bash .claude/scripts/verify.sh` 12/12 PASS + 영어 커밋. ko 콘텐츠 수정 시
  en 영향 여부를 STATUS 작업 로그에 기록해 6순위에서 회수한다.
- 순위(Phase) 종료마다 gate-verifier 역순 판정. 판정 근거는 파일 실물·스크립트 실행 결과만 인정.
- 착수 전 이 계획과 STATUS 갱신을 먼저 커밋한다(세션 유실 대비).
- 미검증 P1 13건은 해당 청크 착수 시 파일을 열어 실재 확인 후 수정한다(확인 실패 시 발견 문서에 반박 기록).
- en 동기화는 ko 수정이 모두 끝난 뒤 마지막에 한다(이중 작업 방지).

## 1순위 — P0: 따라 하면 실패·사실 오류·실기업 정보 (24건)

- [ ] A1: docs P0 6건 — checklist-mapping 5230 연도(2020), `claude login`→올바른 로그인 안내,
      sbom-management 주간 스캔 워크플로(syft·grype 설치 + mkdir), method2-skill 코드펜스 조기 종료,
      method4-cicd grep ERE 패턴 + syft 미설치 2건
- [ ] A2: CI 예시 P0 8건 (devsecops·ai-coding, 패턴 반복이라 일괄) — GitLab ubuntu 이미지 curl 부재
      4곳(sca.mdx, cicd-quick.mdx, pipeline-design ×2), trivy/zap 이미지 docker CLI 부재 3곳
      (pipeline-design ×2, container-security), gitleaks `--source` 제거, Checkov ID 2건
      (CKV_AWS_25→24, CKV_K8S_35 설명)
- [ ] A3: agents P0 3건 + settings.local.json 정리 — LFD106x→LFD102, gitleaks `--report-path` 추가,
      커밋된 settings.local.json 전부(02~05 계열 6개+) `git rm --cached` + .gitignore + 필요 권한만
      settings.json으로 이전(사용자명 경로 제거)
- [ ] A4: 실기업 정보·집계·인프라 — output-sample 전반의 sktelecom.com 도메인을 가상 도메인으로 일괄
      교체 후 reference/samples 재생성(/update-reference-samples), conformance 갭 분석 집계(18/7)
      정정, docusaurus editUrl 함수형 전환
- [ ] A5: nodejs-unlicensed 샘플 재구성 — nightmare는 MIT라 실습 전제 불성립. license 필드 없는
      로컬 의존성 방식으로 재구성 + 연동 문서(samples/README, sbom-generation 143행, docker-cicd 90행) 갱신
- [ ] A6: en P0 2건 — tools-setup 깨진 curl 명령 복원, reference sbom 링크 문법 복원
- [ ] 게이트 1: gate-verifier 역순 판정(A6→A1)

## 2순위 — 정본 정합성 클러스터 (연동 수치·매핑, P1 핵심)

숫자·매핑이 여러 파일에 연동된 결함은 개별 수정하면 다시 어긋난다. 정본을 먼저 확정하고 일괄 전파한다.

- [ ] B1: G항목 정본 확정·전파 — 공통 항목 수(12), 필수 산출물 수(24, inquiry-response 포함),
      담당 Agent 매핑(G1.7→06, G3S.5→05-management, G3S.6→05-vulnerability, G4.5→07, G2.2 복수 기재)
      을 checklist-mapping.md에서 확정한 뒤 index.md(108, 129행), agents.md, 06과 07 챕터의
      frontmatter와 본문, 해당 agents CLAUDE.md 충족 표, validate-output.py까지 일괄 동기화.
      07의 25/31 표기 구분,
      다음 단계 순서(management→vulnerability) 정정 포함
- [ ] B2: templates↔output-sample↔agent 스펙 정합 — gap-analysis·declaration 체크리스트 체계
      단일화(G항목 31개 권장), curriculum 템플릿 표류 해소(06 agent 참조 명시 + 3직군 정렬),
      oss-policy AI 생성 코드 절 정본 결정 + 절 번호 참조를 이름 기준으로, vulnerability-response
      샘플 CVD 절 추가, appointment 샘플 검토 이력 추가
- [ ] B3: 문서 내부 정합 — 04-process 조건부 산출물 생성 조건 모순(정본 하나로), 4~7개→5~7개,
      SBOM 파일명 [project].cdx.json 통일, 18974 4.3.1 체크리스트 문구 단일화, 05-vulnerability
      frontmatter 4.1.5, 도구 개수 문구, 3-6 섹션 위치, 02 질문 번호 6/6 등
- [ ] 게이트 2: 역순 판정

## 3순위 — 검증 하네스 강화 (P1 harness 6건 + 드러나는 위반 해소)

하네스를 먼저 강화하면 이후 순위의 회귀를 자동으로 잡는다.

- [ ] H1: verify.sh — [5/12] Windows 경로 패턴 + py/js/mdx/tsx/scss 확장자, [6/12] 5230↔4.x.x
      역방향 검사 + templates/·output-sample/·website 범위 확장, [2/12] website md 링크 검사
      (또는 onBrokenLinks: 'throw')
- [ ] H2: validate-output.py 누락 4파일(process-diagram, resources, declaration-draft,
      submission-guide) 추가, check-admonition.js stdin JSON 파싱 전환, sync-kwg-reference.sh
      경로 절대화
- [ ] H3: 강화된 검사가 새로 잡아내는 기존 위반 일괄 해소(수량은 실행 시 확정)
- [ ] 게이트 3: 역순 판정 + 강화 전후 검출 수 비교 기록

## 4순위 — 영역별 P1 잔여

- [ ] C1: docs P1 — 인용(>) → admonition/코드펜스 전환, macOS 전용 `open` 교체, SPDX/CycloneDX
      버전 표기, 06-training 174행 렌더링 깨짐, 02 frontmatter 형식, onot 입력 형식 등
- [ ] C2: agents P1 — 경로 기준 문장(레포 루트 기준 명시) 전 agent 공통 추가, `cd agents/...` 다음
      단계 표기 정리, 05-sbom-guide Q2 Go·기타 분기, 07 표기 구분
- [ ] C3: website 콘텐츠 P1 — reference/samples 원본 어긋남(process 외부 문의·SLA 충돌,
      organization 산출물 수, intro 표) → 원본 수정 후 /update-reference-samples 재생성,
      ISO 조항 라벨 정정(3.3.2 vs 3.1.5, iso-mapping 라벨), cdxgen 변환 주석·pyspdxtools 사용법,
      monitoring·iac-security의 agent 스펙 불일치, gitleaks allowlists 버전, checkov soft-fail,
      CKV_K8S_6→23, sast GitLab 소절 위치, conformance 부분충족 제출 안내
- [ ] C4: 디자인·UX P1 — docs 플러그인 `exclude: ['**/CLAUDE.md']`, gtag 플레이스홀더 처리,
      Showcase 5230 목차 매핑, FinalCTA 무설치·무비용 과장 완화, quick-start 5분 범위·경로·
      OpenChain 표기, about.md 인용 제거
- [ ] 게이트 4: 역순 판정

## 5순위 — P2 스타일·일관성 일괄 (101건, 패턴별 sweep)

- [ ] S1: 존댓말 평서형 통일 sweep (supply-chain, 06-training, tools-setup, 01-setup 등)
- [ ] S2: 인용(>) → admonition 전환 sweep (P1 외 잔여)
- [ ] S3: 표기 정본화 — cron UTC 병기, BomLens 새 URL, STYLEGUIDE 정본 용어(NTIA, SBOM 풀이),
      admonition 제목 문법, '셀프스터디 경로' 제목 통일, front matter 필수 필드(method1~4,
      docker-cicd — 또는 하위 문서 예외를 STYLEGUIDE에 명문화)
- [ ] S4: 잔여 P2 개별 건 (findings 문서 기준, 실행 시 ko-style 린트 병행)
- [ ] 게이트 5: 역순 판정

## 6순위 — en 패리티 전면 동기화 (ko 확정 후)

- [ ] D1: en 누락 페이지 신규 번역 — ai-coding/iso-mapping, reference/glossary
- [ ] D2: 기계번역 품질 미달 4파일 재번역 — docs 05 docker-cicd, 05 vulnerability/tools-setup,
      08-developer-guide index(최신 ko 구조 반영), reference intro
- [ ] D3: 구조 동기화 일괄 — Prerequisite 배너(02~07), JourneyProgress, tip/note admonition
      누락분, 데모 iframe·API 키 안내(devsecops 4+1페이지), rules-template 3블록,
      trustedoss-agents URL(en 7+2파일), supply-chain 6절, 04-process frontmatter와 도입부,
      policy 샘플 §10, 1~5순위에서 STATUS에 기록한 ko 변경분 회수
- [ ] D4: 번역 리소스 — footer.json 키 2추가·1제거, reference current.json 카테고리 키,
      sidebar_label 통일(SBOM Basics, Output 계열), intro.md H1 공백
- [ ] 게이트 6: 역순 판정 + `cd website && npm run build` (en 로케일 포함)

## 마무리

- [ ] 최종 검증: verify 12/12 + 빌드 + 콜드스타트 페르소나 walkthrough 1회(선행 사례: 2026-06-10)
- [ ] STATUS.md·progress.md 결산, CLAUDE.md 반영 사항 확인(하네스 변경 시 harness-guide 갱신)

## 계획 외 소재 (이번 범위 아님)

- TRUSCA 로드맵 실행은 trusca 저장소 소관(`trusca-roadmap.md` 전달로 완료)
- STATUS 미착수 잔여 2건(supply-chain Shai-Hulud 사례, CI 게이트 프롬프트 인젝션 프레임 한 줄)은
  사용자 승인 시 5순위에 편입 가능
