# trustedoss

ISO/IEC 5230 (라이선스 컴플라이언스)과 ISO/IEC 18974 (보안 보증) 자체 인증을 위한 실전 키트.
챕터·Agent·산출물 전체 목록은 README.md 참조.

## 작업 범위

이 프로젝트는 콘텐츠 작업만 한다.
디자인과 동작 방식은 수정하지 않는다.

| 작업 대상 (O) | 작업 금지 (X) |
|-------------|-------------|
| `docs/`      | `website/src/` (아래 예외 제외) |
| `agents/`    | `website/static/` |
| `templates/` | `*.ts`, `*.tsx`, `*.js` |
| `.claude/`   | `*.css`, `*.scss` (아래 예외 제외) |
| `CLAUDE.md`  | 설정 파일 전체 |

**예외 — 아래 목적에 한해 허용:**
- `website/src/css/customTheme.scss` — sidebar 계층 구분 CSS 추가, 또는 테이블 가독성 개선 CSS 추가 목적에 한해 수정 가능

콘텐츠 작업 중 디자인/코드 수정이 필요해 보이는 상황이 생기면 작업을 멈추고 사용자에게 확인하라.

## 디렉토리 구조
| 경로 | 역할 |
|---|---|
| `docs/` | 챕터별 가이드 문서 |
| `agents/` | 산출물 자동 생성 agent |
| `templates/` | 문서 템플릿 |
| `samples/` | 실습용 샘플 프로젝트 |
| `workshop/` | 강의 키트 |
| `output/` | 생성된 산출물 (gitignore) |
| `.claude/skills/` | 재사용 skill 정의 |

## 독자 상태 감지 — 다음 단계 안내

"어디서 시작해야 해?" 또는 "다음에 뭘 해야 해?" 질문 시 `output/` 폴더를 스캔하고 아래 표로 안내한다.

| output/ 상태 | 안내 |
|---|---|
| 비어있음 | "시작하기 전에: 두 표준과 이 키트의 소개"(`docs/00-overview/index.md`) 및 "소프트웨어 공급망 보안: 왜 지금 중요한가"(`docs/00-overview/supply-chain.md`) 읽기 → 현재 Claude 세션 종료 후 `cd agents/02-organization-designer && claude` 실행 |
| organization/ 있음, policy/ 없음 | 현재 Claude 세션 종료 후 `cd agents/03-policy-generator && claude` 실행 |
| policy/ 있음, process/ 없음 | 현재 Claude 세션 종료 후 `cd agents/04-process-designer && claude` 실행 |
| process/ 있음, sbom/ 없음 | 현재 Claude 세션 종료 후 `cd agents/05-sbom-guide && claude` 실행 |
| sbom/ 있음, vulnerability/ 없음 | 현재 Claude 세션 종료 후 `cd agents/05-sbom-analyst && claude` 실행 → 완료 후 `cd agents/05-vulnerability-analyst && claude` 실행 |
| vulnerability/ 있음, training/ 없음 | 현재 Claude 세션 종료 후 `cd agents/05-sbom-management && claude` 실행 → 완료 후 `cd agents/06-training-manager && claude` 실행 |
| training/ 있음, conformance/ 없음 | 현재 Claude 세션 종료 후 `cd agents/07-conformance-preparer && claude` 실행 |
| conformance/ 있음 | 완성 축하 → OpenChain 자체 인증 등록: https://www.openchainproject.org/conformance |

## 사용 경로
- **셀프스터디**: `docs/` 챕터를 00부터 순서대로 진행

## Skills — 언제 쓰는가

| 파일 | 트리거 조건 |
|---|---|
| `.claude/skills/create-doc.md` | `docs/` 하위 문서를 새로 작성하거나 수정할 때 |
| `.claude/skills/validate-checklist.md` | `agents/07-conformance-preparer` 또는 output/ 전체 완료 여부 점검 시 |
| `.claude/skills/generate-report.md` | SBOM 분석·취약점 분석·갭 분석 리포트를 생성할 때 |

## 작업 완료 후 필수 규칙

### 1. 검증 실행
파일 생성·수정 후 반드시 실행하라.

```bash
bash .claude/scripts/verify.sh
```

검증 항목: Docusaurus 빌드 / 내부 링크 / front matter YAML / 필수 파일 / 로컬 경로 노출 / **18974 섹션 번호 형식** / **agent 실행 admonition 누락**
모든 항목 PASS 후에만 push 가능.

### 2. 경로 규칙

| 구분 | 패턴 | 예시 |
|---|---|---|
| **금지** | 사용자명 포함 절대경로 | `~username/...`, `C:\Users\사용자명\...` |
| **허용** | 상대 경로 | `./docs/...` |
| **허용** | 홈 디렉토리 약칭 | `~/` |
| **허용** | 일반화 예시 경로 | `/path/to/trustedoss` |

명령어 예시·스크립트·에러 인용·README 설치 가이드 모두 동일 규칙 적용.

#### docs/ → reference/ 크로스 인스턴스 링크

`docs/` 문서에서 `website/reference/` 페이지를 참조할 때는 Docusaurus 절대 경로를 사용한다.

| 구분 | 형식 | 예시 |
|---|---|---|
| **올바름** | `/reference/samples/{name}` | `/reference/samples/sbom` |
| **금지** | 상대 경로로 reference/ 접근 | `../../website/reference/...` |

`verify.sh` 링크 체크는 `/`로 시작하는 절대 경로를 자동으로 건너뛴다 (Docusaurus 라우팅 경로로 처리).

### 3. 스펙 섹션 번호 표기 규칙

ISO/IEC 5230과 18974는 섹션 번호 체계가 다르다. 혼용하면 verify.sh [6/6] 항목이 FAIL을 낸다.

| 표준 | 섹션 번호 체계 | 올바른 예 | 잘못된 예 |
|------|------------|---------|---------|
| ISO/IEC 5230 | `3.x.x` | `3.1.1`, `3.3.2`, `3.6.1` | — |
| ISO/IEC 18974 | `4.x.x` | `4.1.1`, `4.3.2`, `4.4.1` | ~~`3.1.1`, `3.3.2`~~ |

**스펙 전문은** `.claude/reference/iso-5230.md` 및 `.claude/reference/iso-18974.md` 참조.

### 4. settings 파일 규칙

| 파일 | 용도 | 로컬 경로 | 커밋 |
|---|---|---|---|
| `settings.json` | 프로젝트 공통 | 절대 금지 | 가능 |
| `settings.local.json` | 로컬 전용 | 사용 가능 | 금지 |

로컬에서만 필요한 설정은 반드시 `settings.local.json` 에 작성하라.

## 막혔을 때
해당 `docs/` 챕터 폴더로 이동하면 그 폴더의 `CLAUDE.md` 가 맥락을 제공한다.

## 진행 상황
`.claude/progress.md` 참조

## CLAUDE.md 업데이트 규칙

아래 상황 발생 시 CLAUDE.md를 즉시 업데이트하라.

| 상황 | 업데이트 항목 |
|------|-------------|
| 새 챕터/Agent 추가 | 독자 상태 감지 테이블 |
| 새 스킬 파일 추가 | 스킬 트리거 테이블 |
| 디렉토리 구조 변경 | 핵심 경로 섹션 |
| 새 규칙/제약 발견 | 해당 규칙 섹션 |

업데이트 후 변경 내용을 커밋 메시지에 명시하라.
예: "docs: update CLAUDE.md - add devsecops agent trigger"

## 세션 종료 전 체크리스트

매 작업 세션 종료 전 아래를 순서대로 실행하라.
- [ ] bash .claude/scripts/verify.sh 실행 후 모두 PASS 확인
- [ ] .claude/progress.md 업데이트
      (완료 항목 체크, 다음 작업 갱신)
- [ ] 이번 세션에서 구조 변경이 있었으면 CLAUDE.md도 업데이트
- [ ] git commit