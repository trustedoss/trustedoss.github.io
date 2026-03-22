---
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - "ISO/IEC 5230: []"
  - "ISO/IEC 18974: []"
셀프스터디 소요시간: 1시간
워크숍 소요시간: 30분 (M0 모듈)
---

# 시작하기 전에: 두 표준과 이 키트의 소개

## 1. 이 챕터에서 하는 일

오늘 처음 오픈소스 담당자가 됐어도 이 키트를 따라가면 ISO/IEC 5230과 ISO/IEC 18974 자체 인증 선언까지 완성할 수 있다. 이 챕터에서는 전체 여정의 목적과 구조를 파악하고, 셀프스터디 또는 워크숍 경로 중 하나를 선택한다.

### 완성 시 갖게 되는 산출물

| 단계 | 산출물 파일 | 관련 표준 |
|------|------------|----------|
| 조직 | `role-definition.md`, `raci-matrix.md`, `appointment-template.md` | [공통] |
| 정책 | `oss-policy.md`, `license-allowlist.md` | [공통] |
| 프로세스 | `usage-approval.md`, `distribution-checklist.md`, `vulnerability-response.md`, `process-diagram.md` | [공통] |
| SBOM 생성 | `[project].cdx.json`, `sbom-commands.sh`, `license-report.md`, `copyleft-risk.md` | [공통] |
| SBOM 관리 | `sbom-management-plan.md`, `sbom-sharing-template.md` | [공급망] |
| 취약점 | `cve-report.md`, `remediation-plan.md` | [18974] |
| 교육 | `curriculum.md`, `completion-tracker.md`, `resources.md` | [공통] |
| 인증 | `gap-analysis.md`, `declaration-draft.md`, `submission-guide.md` | [공통] |

---

## 2. 배경 지식

### 두 표준 비교

| 항목 | ISO/IEC 5230 | ISO/IEC 18974 |
|------|-------------|---------------|
| 정식 명칭 | OpenChain License Compliance | OpenChain Security Assurance |
| 최신 버전 | 2.1 (2023) | 1.0 (2023) |
| 목적 | 오픈소스 라이선스 컴플라이언스 체계 수립 | 오픈소스 보안 취약점 보증 체계 수립 |
| 초점 | 라이선스 의무사항 이행, BOM 관리 | 알려진 CVE 식별·추적·대응, SBOM 기반 보안 |
| 핵심 요구사항 | 정책·조직·프로세스·BOM·컴플라이언스 산출물·기여 정책·준수 선언 | 정책·조직·SBOM·CVE 스캔·취약점 추적·대응·준수 선언 |
| 인증 방식 | OpenChain 웹사이트 자체 선언 | OpenChain 웹사이트 자체 선언 |
| 제정 배경 | 오픈소스 라이선스 분쟁 급증 대응 | SolarWinds·Log4Shell 등 공급망 보안 사고 대응 |

> 유효 기간·관련 규제·상호 보완성 등 항목별 상세 비교는 [`checklist-mapping.md`](./checklist-mapping.md) 참조.

### 자체 인증이란 무엇인가

두 표준 모두 **자체 인증(Self-Certification)** 방식이다. 외부 심사 기관의 감사 없이 OpenChain 웹사이트에서 직접 선언한다.

- **제3자 인증과의 차이**: 외부 심사 비용과 일정이 없으며, 조직 스스로 요구사항 충족을 선언한다.
- **법적·실무적 의미**: 공급망 파트너에게 오픈소스 관리 수준을 투명하게 제공하며, 납품 시 컴플라이언스 증빙 자료로 활용 가능하다.
- **인증 후 할 수 있는 것**: OpenChain 인증 로고 사용, 공급망 투명성 증명, 고객사 감사 대응 시 신뢰도 향상.

### 이 키트의 두 가지 사용 경로

| 경로 | 대상 | 소요 시간 | 진행 방식 |
|------|------|----------|----------|
| 셀프스터디 | 혼자 진행하는 담당자 | 3~5일, 총 12시간 | `docs/` 챕터를 시작부터 순서대로 진행 |
| 워크숍 | 팀 전체 참여 | 하루 6~7시간 | `workshop/student-handout.md` 기준 M0~M6 모듈 |

### `checklist-mapping.md` 보는 방법

`docs/00-overview/checklist-mapping.md` 는 두 표준의 전체 25개 요구사항을 한 표로 정리한 지도다.

**항목 ID 체계:**

| 접두사 | 의미 |
|--------|------|
| G1 | 프로그램 기반 (정책·조직·교육) |
| G2 | 관련 업무 정의 (역할·채널·인식) |
| G3-L | 라이선스 컴플라이언스 (ISO/IEC 5230 중심) |
| G3-S | 보안 보증 (ISO/IEC 18974 중심) |
| G3-B | SBOM 및 공급망 (공통) |
| G4 | 준수 선언 및 유지 |

**핵심 인사이트:** 전체 25개 항목 중 공통 항목이 10개다. 공통 항목 10개를 먼저 완성하면 두 표준을 동시에 40% 충족하므로, 중복 작업을 약 40% 절감할 수 있다. 이 키트는 공통 항목을 우선 처리하도록 설계되어 있다.

---

## 3. 셀프스터디 경로

:::info 셀프스터디 모드 (약 1시간)
혼자서 충분한 시간을 갖고 각 문서를 이해하며 진행합니다. 전체 키트 완료까지 3~5일을 권장합니다.
:::

1. 이 문서(`index.md`) 읽기 — 전체 여정 개요 파악
2. `checklist-mapping.md` 읽기 — 전체 25개 항목 구조 파악
3. `supply-chain.md` 읽기 — 소프트웨어 공급망 보안 배경 지식 습득
4. `docs/01-setup/` 으로 이동 — 환경 준비 시작

---

## 4. 워크숍 경로

:::tip 워크숍 모드 (M0 - 30분)
전체 팀과 함께 이 문서를 리뷰하고 담당자를 사전 지정합니다. `workshop/student-handout.md` 를 함께 펼쳐 두세요.
:::

1. **(10분)** 두 표준 비교 표를 팀 전체가 함께 리뷰하고 질문을 공유
2. **(10분)** `checklist-mapping.md` 의 워크숍 모듈 매핑 확인 — M1~M6 일정 조율
3. **(10분)** 역할 분담 사전 논의 — M1 모듈(조직 설계) 준비

---

## 5. 완료 확인 체크리스트

- [ ] 두 표준(ISO/IEC 5230, ISO/IEC 18974)의 차이점과 공통점을 설명할 수 있다
- [ ] `checklist-mapping.md` 의 G1~G4 항목 ID 체계를 파악했다
- [ ] 공통 항목 10개가 두 표준을 동시에 충족한다는 점을 이해했다
- [ ] 셀프스터디 또는 워크숍 경로를 선택했다
- [ ] 다음 단계(공급망 보안 학습 또는 챕터 `01`)로 이동할 준비가 됐다

---

## 6. 다음 단계 안내

**배경 지식이 필요하다면:**
→ `supply-chain.md` 와 `sbom-101.md` 를 읽어 소프트웨어 공급망 보안과 SBOM 개념을 먼저 학습한다.

**바로 환경 준비를 시작하려면:**
→ `docs/01-setup/` 으로 이동하여 도구 설치와 환경 설정을 진행한다.

**워크숍 참가자라면:**
→ `workshop/student-handout.md` 를 열어 M0 완료를 표시하고 M1 모듈로 이동한다.
