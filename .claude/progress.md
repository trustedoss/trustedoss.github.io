# 프로젝트 진행 상황

이 파일은 CLAUDE.md를 경량화하면서 분리된 진행 상태 정보를 담는다.
장기 계획, 완료된 지시, 다음 작업, 실습 구조 정의를 포함한다.

---

## 장기 로드맵

| Phase | 이름 | 상태 |
|---|---|---|
| 0 | 플랫폼 기반 구축 (Docusaurus, CI/CD, 기본 구조) | ✅ 완료 |
| 1 | 핵심 콘텐츠 작성 (docs 챕터 00~07) | 🔄 진행 중 |
| 2 | Agent 구축 (산출물 자동 생성 파이프라인) | ⏳ 대기 |
| 3 | 검증 시스템 강화 (verify.sh, CI 통합) | ⏳ 대기 |
| 4 | 워크숍 키트 완성 (핸드아웃, 진행자 가이드) | ⏳ 대기 |
| 5 | 출시 및 배포 (퍼블리시, OpenChain 등록 안내) | ⏳ 대기 |

---

## 완료된 지시

| ID | 내용 | 커밋 |
|---|---|---|
| A | 프로젝트 플랫폼 재초기화 (Docusaurus + Yarn 4) | `d86e55b` |
| B | CI 빌드 수정 (Yarn 4 corepack, immutable flag) | `b1ef129`, `aa32bb6`, `bc907fc`, `6b4ba2f` |
| C | baseURL 및 내부 링크 수정 (Hero, CallToAction, 홈) | `65f89b6`, `e93e92f`, `a0cb0a7`, `94fc7e1` |
| D | self check 스크립트 업데이트 | `91213b1` |

---

## 다음 작업

### 지시 E (완료)
- [x] CLAUDE.md 재작성 — 토큰 최소화, 표 압축, 스킬 트리거 명시
- [x] `.claude/progress.md` 생성 — 진행 상태 정보 분리 보관

### 지시 F (완료)
- [x] `.claudeignore` 보강 — Docusaurus 소스/설정/CSS 추가
- [x] CLAUDE.md 작업 범위 섹션 추가

### 지시 G (완료)
- [x] docs/ 파일 크기 분석 (`wc -l`)

### 지시 H (완료)
- [x] 모든 챕터 디렉토리에 `_category_.json` 생성 (숫자 접두사 제거)
- [x] `website/sidebars.ts` 업데이트
- [x] `docs/00b-supply-chain/` → `docs/00-overview/supply-chain.md` + `sbom-101.md` 이동 및 삭제
- [x] 관련 CLAUDE.md 병합, intro.md 링크 수정
- [x] 대형 챕터 분리:
  - `08-developer-guide/index.md` → 4개 method 파일 추출
  - `05-tools/vulnerability/index.md` → `tools-setup.md` 추출
  - `05-tools/sbom-generation/index.md` → `docker-cicd.md` 추출
- [x] 내부 링크 수정 (verify.sh 10개 broken link 전부 해결)
- [x] verify.sh 5/5 PASS 확인

### 지시 I (완료)
- [x] `docs/00-overview/checklist-mapping.md` 전면 개편
  - 10컬럼 테이블 → 항목별 `####` 섹션 + 입증자료 소형 테이블
  - 산출물 파일 매핑 추가 (입증자료 ID → output/ 파일)
  - 스펙 번호 오류 전수 수정 (G1.7, G3L.5, G3L.6, G3B.2, G4.2~G4.4)
- [x] ISO/IEC 5230/18974 전문을 `.claude/reference/` 에 저장 (나침반)
- [x] ISO/IEC 18974 섹션 번호 체계 일괄 정정 (§3.x.x → §4.x.x)
  - agents/ CLAUDE.md 7개 파일
  - docs/ CLAUDE.md 7개 파일
  - docs/ index.md 4개 파일
- [x] verify.sh [6/6] 체크 추가 (18974 §3.x.x 오표기 탐지)
- [x] CLAUDE.md 스펙 섹션 번호 표기 규칙 추가
- [x] 기존 broken link 수정 (docs/01-setup/method1-claude-md.md)
- [x] verify.sh 6/6 PASS 확인

### 지시 J (완료)
- [x] 가이드 기준 충족 여부 검토 (표준 설명/이유/방법/입증자료)
- [x] 워크숍 경로 섹션 전체 제거 (9개 챕터 index.md)
  - 00-overview, 02-organization, 03-policy, 04-process
  - 05-sbom-generation, 05-sbom-management, 05-vulnerability
  - 06-training, 07-conformance
- [x] front matter `워크숍 소요시간` 줄 전체 제거
- [x] "막혔을 때" 주요 내용 셀프스터디 섹션에 통합 (04, 05-sbom-gen, 05-sbom-management)
- [x] 06-training/index.md 18974 섹션 번호 수정 (3.1.2→4.1.2, 3.1.3→4.1.3)
- [x] 03-policy/index.md :::info 블록 내 18974 번호 수정 (3.1.1→4.1.1, 3.1.4→4.1.4)
- [x] 03-policy/index.md 중복 ✅ 완료 확인 섹션 제거
- [x] docs/.claude/settings.local.json git 추적 해제 + .gitignore 추가
- [x] verify.sh 6/6 PASS 확인

### 지시 K (완료)
- [x] verify.sh [6/6] 정규식 이중 패턴 적용 (false positive 수정)
  - 패턴 1: `18974[^(0-9]*3\.[1-9]\.[0-9]` — 본문 텍스트 §3.x.x 탐지
  - 패턴 2: `18974[^)]*[\[(]3\.[1-9]` — 괄호/대괄호 형식 `G?.? (3.x.x)` 탐지
- [x] `.claude/skills/create-doc.md` 업데이트 — 워크숍 제거, 품질 기준 추가
- [x] `docs/CLAUDE.md` 업데이트 — 워크숍 규칙 명시
- [x] verify.sh 6/6 PASS 확인

### 지시 L (완료)
- [x] 가이드 완전성 검증 (입증자료 50개 커버리지 분석)
- [x] validate-checklist.md 13항목 → 17항목으로 보완 (distribution-checklist.md, remediation-plan.md, sbom-sharing-template.md, copyleft-risk.md 추가)
- [x] §4.1.2.5·§4.1.2.6·§4.1.4.3 시간 기반 항목 안내 추가 (checklist-mapping.md, 07-conformance-preparer)
- [x] §3.2.2.5 라이선스 미준수 절차 매핑 수정 (vulnerability-response.md → usage-approval.md + distribution-checklist.md)
- [x] 05-sbom-management 실행 순서 명확화 (agents/CLAUDE.md, checklist-mapping.md 다음 단계 9단계로 수정)
- [x] verify.sh 6/6 PASS 확인

### 지시 M (완료)
- [x] templates/ 핵심 산출물 5개 섹션 구조 정의 (role-definition, raci-matrix, distribution-checklist, vulnerability-response, completion-tracker, gap-analysis, declaration-draft)
- [x] docs/06-training/index.md — completion-tracker.md 빈 템플릿 처리 안내 추가 (⚠️ 블록)
- [x] docs/05-tools/sbom-generation/index.md — 3개 샘플 프로젝트 비교 표 추가
- [x] docs/07-conformance/index.md — G4.5 취약점 있을 때 인증 선언 처리 방법 표 추가
- [x] docs/05-tools/sbom-generation/CLAUDE.md — 잘못된 samples 경로 수정 (java-app → java-vulnerable 등)
- [x] verify.sh 6/6 PASS 확인

### 다음 작업 (예정)
- templates/ 나머지 산출물 (policy/oss-policy, process/usage-approval, training/curriculum, conformance/submission-guide) 구조 정의
- docs/ 챕터별 실습 블록 보강 (Phase 1 콘텐츠 완성)

---

## 챕터-실습 매핑 표

| 챕터 | 셀프스터디 실습 | 워크숍 실습 | 연동 Agent |
|---|---|---|---|
| 00-overview | 두 표준 체크리스트 비교 | 개요 강의 (15분) | — |
| 00-overview/supply-chain | SBOM 개념 정리 | 공급망 위협 시나리오 (20분) | — |
| 01-setup | 도구 설치 및 환경 확인 | 환경 세팅 (15분) | — |
| 02-organization | 역할 정의 + RACI 작성 | 역할 지정 워크 (30분) | 02-organization-designer |
| 03-policy | 오픈소스 정책 문서 작성 | 정책 초안 리뷰 (30분) | 03-policy-generator |
| 04-process | 프로세스 흐름도 설계 | 흐름도 그리기 (30분) | 04-process-designer |
| 05-tools/sbom-generation | SBOM 생성 명령어 실습 | 생성 실습 (20분) | 05-sbom-guide |
| 05-tools/sbom-management | SBOM 공유 계획 작성 | 공유 템플릿 작성 (20분) | 05-sbom-management |
| 05-tools/vulnerability | CVE 스캔 및 대응 계획 | 취약점 트리아지 (30분) | 05-sbom-analyst, 05-vulnerability-analyst |
| 06-training | 교육 커리큘럼 설계 | 커리큘럼 템플릿 작성 (20분) | 06-training-manager |
| 07-conformance | 갭 분석 + 선언문 작성 | 자체 인증 체크 (30분) | 07-conformance-preparer |

---

## Phase 1 실습 블록 형식 정의

Phase 1 (docs 챕터 작성) 에서 사용하는 실습 블록은 3가지 형식이 있다.

### 형식 1 — 명령어 실행형
CLI 명령어를 직접 실행하고 결과를 확인하는 실습.

```
:::info 셀프스터디 — 명령어 실행형
**목표**: {무엇을 확인하는가}

1. 아래 명령어를 실행한다.
   ```bash
   {명령어}
   ```
2. 예상 결과: {결과 설명}
3. 결과가 다르면 {대처 방법}.
:::
```

### 형식 2 — 문서 작성형
템플릿을 채워서 산출물 문서를 작성하는 실습.

```
:::info 셀프스터디 — 문서 작성형
**목표**: {어떤 문서를 작성하는가}

1. `templates/{파일명}` 을 열고 {} 자리에 내용을 채운다.
2. 작성 완료 후 `output/{경로}` 에 저장한다.
3. 완료 기준: {체크 항목}.
:::
```

### 형식 3 — Agent 실행형
`agents/` 폴더의 agent를 실행하여 산출물을 자동 생성하는 실습.

```
:::info 셀프스터디 — Agent 실행형
**목표**: {어떤 산출물을 생성하는가}

1. 아래 경로로 이동하고 Claude를 실행한다.
   ```bash
   cd agents/{agent명}
   claude
   ```
2. Agent의 질문에 답하면 `output/{경로}` 에 파일이 생성된다.
3. 생성된 파일을 열어 내용을 검토한다.
:::
```
