# OpenChain 자체 인증 등록 절차 안내

---

## 개요

테크유니콘은 ISO/IEC 5230:2020 (라이선스 컴플라이언스)과 ISO/IEC 18974:2023 (보안 보증) 자체 인증을
OpenChain 프로젝트 공식 사이트에 등록하여 공개적으로 선언한다.

| 항목        | 내용                                     |
| ----------- | ---------------------------------------- |
| 등록 사이트 | https://openchainproject.org/get-started |
| 선언 유형   | 자체 인증 (Self Certification)           |
| 적용 표준   | ISO/IEC 5230:2020 + ISO/IEC 18974:2023   |
| 유효 기간   | 18개월 (2026-03-23 ~ 2027-09-23)         |

---

## 등록 전 사전 준비

아래 항목을 완료한 후 등록 절차를 진행한다.

### 필수 조치 (등록 전 완료 권고)

- [ ] `output/organization/raci-matrix.md` §역할별 담당자 — 실명 기입 완료
- [ ] `output/organization/appointment-template.md` — 발령문 서명 완료
- [ ] 교육 이수 시작 — 관리자 과정(2026-06) 최소 착수

### 산출물 최종 확인

- [ ] `output/conformance/gap-analysis.md` 존재 확인
- [ ] `output/conformance/declaration-draft.md` 존재 확인
- [ ] 모든 산출물 최신 상태 확인

---

## 등록 절차 (단계별)

### 1단계 — 자체 인증 체크리스트 내려받기

1. [OpenChain Reference-Material 저장소](https://github.com/OpenChain-Project/Reference-Material/tree/master/OpenChain-Standards-Self-Certification) 접속
2. `Checklist/ISO-IEC-5230` 및 `Checklist/ISO-IEC-18974` 아래에서 언어별 파일을 내려받는다

### 2단계 — 선언할 표준 결정

- **ISO/IEC 5230** (라이선스 컴플라이언스)
- **ISO/IEC 18974** (보안 보증)
- 두 표준 모두 선언 가능하며, 표준마다 체크리스트가 따로 있다

### 3단계 — 등재 신청 정보 준비

| 입력 항목   | 입력 내용                       |
| ----------- | ------------------------------- |
| 회사명      | 테크유니콘                      |
| 담당자 이름 | DevOps팀 오픈소스 담당자 실명   |
| 이메일      | opensource@techunicorn.example  |
| 국가        | Korea (South)                   |
| 웹사이트    | https://www.techunicorn.example |

### 4단계 — 체크리스트 자체 점검

`output/conformance/declaration-draft.md`를 참조하여 각 항목을 Yes/No 로 판정한다.

**ISO/IEC 5230 체크리스트 (25개 항목)**:

- 3.1.1.1부터 3.6.2.1까지 모든 항목에 체크
- 🔶 항목(3.1.2.3, 3.1.3.1, 3.2.2.1)은 가능하면 충족(교육 이수 개시, 실명 기입)으로 전환한 뒤 제출하고, 전환 전이라면 계획 수립 완료 상태임을 인지하고 체크

**ISO/IEC 18974 체크리스트 (25개 항목)**:

- 4.1.1.1부터 4.4.2.1까지 모든 항목에 체크
- 🔶 항목 중 시간 기반 3개(4.1.2.5, 4.1.2.6, 4.1.4.3)는 초기 인증 시 허용 범위이고, 나머지는 가능하면 충족으로 전환한 뒤 제출

### 5단계 — 등재 신청 및 확인

1. [OpenChain 시작하기 페이지](https://openchainproject.org/get-started)의 온라인 신청 폼 작성
2. 3단계에서 준비한 회사 정보를 입력하고 제출
3. OpenChain 공식 등재 목록에 테크유니콘이 오르는지 확인 (문의: support@openchainproject.org)

---

## 등록 완료 후 조치

### 공개 발표

등록 완료 후 아래 채널에 공지를 권장한다:

- 사내 위키/인트라넷에 등록 인증 현황 게시
- 회사 보안/컴플라이언스 페이지에 OpenChain 인증 배너 추가
- 주요 납품처/고객사에 인증 획득 사실 통보 (신뢰도 제고)

### 산출물 보관

OpenChain 등록 후 아래 증거를 보관한다:

- 등록 확인 이메일 사본
- 등록 시점 스크린샷 (`output/conformance/` 폴더 보관)
- `declaration-draft.md` 서명본 (담당자 및 팀장 서명)

---

## 유지 관리 일정

### 18개월 재선언 주기

| 시점                        | 작업                                      |
| --------------------------- | ----------------------------------------- |
| 2026-09-23 (선언 6개월 후)  | 중간 점검 — 부분충족 항목 이행 확인       |
| 2027-03-23 (선언 12개월 후) | 연간 갭 분석 재실행, gap-analysis.md 갱신 |
| 2027-09-23 (선언 18개월 후) | 재선언 — OpenChain 사이트 재등록          |

### 수시 갱신 트리거

아래 상황 발생 시 즉시 산출물 갱신 후 갭 分析 재실행:

| 트리거                   | 갱신 대상 산출물                    |
| ------------------------ | ----------------------------------- |
| 오픈소스 정책 변경       | oss-policy.md, gap-analysis.md      |
| 담당자 변경              | role-definition.md, raci-matrix.md  |
| 새로운 Critical CVE 발생 | cve-report.md, remediation-plan.md  |
| 신규 제품/서비스 출시    | sbom/\*, distribution-checklist.md  |
| 배포 채널 추가           | license-allowlist.md, oss-policy.md |

---

## 문의처

| 유형                       | 연락처                           |
| -------------------------- | -------------------------------- |
| 라이선스 컴플라이언스 문의 | opensource@techunicorn.example   |
| 보안 취약점 신고           | security@techunicorn.example     |
| OpenChain 프로젝트 공식    | https://www.openchainproject.org |

---

_본 문서는 ISO/IEC 5230 §3.6.1 및 ISO/IEC 18974 §4.4.1 요구사항 이행을 위해 작성되었습니다._
