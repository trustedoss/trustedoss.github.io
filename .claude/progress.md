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

### 지시 E (현재 작업)
- [x] CLAUDE.md 재작성 — 토큰 최소화, 표 압축, 스킬 트리거 명시
- [x] `.claude/progress.md` 생성 — 진행 상태 정보 분리 보관

### 지시 F 이후 계획 (예정)
- docs/ 챕터별 실습 블록 작성 (Phase 1 콘텐츠)
- agents/ CLAUDE.md 정비 — 각 agent 실행 맥락 명확화
- verify.sh 검증 항목 확장 (Phase 3)
- workshop/student-handout.md 초안 작성 (Phase 4)

---

## 챕터-실습 매핑 표

| 챕터 | 셀프스터디 실습 | 워크숍 실습 | 연동 Agent |
|---|---|---|---|
| 00-overview | 두 표준 체크리스트 비교 | 개요 강의 (15분) | — |
| 00b-supply-chain | SBOM 개념 정리 | 공급망 위협 시나리오 (20분) | — |
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
