---
id: checklist-mapping
title: 요구사항 체크리스트 통합 매핑
sidebar_label: 체크리스트 매핑
sidebar_position: 2
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - "ISO/IEC 5230: 전체 (매핑 기준 문서)"
  - "ISO/IEC 18974: 전체 (매핑 기준 문서)"
셀프스터디 소요시간: 1시간
워크숍 소요시간: 30분 (M0 모듈)
---

# 요구사항 체크리스트 통합 매핑

## 이 문서의 목적

이 문서는 **ISO/IEC 5230** (라이선스 컴플라이언스)과 **ISO/IEC 18974** (보안 보증)
두 표준의 자체인증 체크리스트 항목을 **하나의 매핑 테이블로 통합**한 프로젝트 전체의 나침반이다.

모든 agent의 CLAUDE.md는 이 문서를 참조하여 어떤 표준 요구사항을 충족하는 산출물을
어느 모듈에서 생성하는지 파악한다.

### 이 문서를 읽는 방법

1. **두 표준 비교 표** → 각 표준의 목적과 범위를 먼저 파악한다
2. **통합 매핑 테이블** → 그룹별로 어떤 agent와 산출물이 어느 요구사항을 충족하는지 확인한다
3. **비고 컬럼** → `[공통]` `[5230]` `[18974]` `[공급망]` `[규제]` 태그로 항목 성격을 빠르게 파악한다
4. **요약 통계** → 문서 하단에서 전체 현황을 숫자로 확인한다

---

## 두 표준 비교

| 항목 | ISO/IEC 5230 | ISO/IEC 18974 |
|------|-------------|--------------|
| **정식 명칭** | OpenChain License Compliance | OpenChain Security Assurance |
| **최신 버전** | 2.1 (2023) | 1.0 (2023) |
| **목적** | 오픈소스 라이선스 컴플라이언스 체계 수립 | 오픈소스 보안 취약점 보증 체계 수립 |
| **초점** | 라이선스 의무사항 이행, BOM 관리, 고지문 생성 | 알려진 CVE 식별·추적·대응, SBOM 기반 보안 |
| **주요 요구사항** | 정책, 조직, 프로세스, BOM, 컴플라이언스 산출물, 기여 정책, 준수 선언 | 정책, 조직, SBOM, CVE 스캔, 취약점 추적·점수화·대응, 준수 선언 |
| **인증 방식** | OpenChain 웹사이트 자체 선언 | OpenChain 웹사이트 자체 선언 |
| **유효 기간** | 18개월 | 18개월 |
| **관련 규제·표준** | SPDX, REUSE, EU CRA (라이선스 측면) | EO 14028, NTIA SBOM, EU CRA, NVD/CVSS |
| **상호 보완성** | 공통 기반(정책·조직·SBOM) 공유, 라이선스 특화 요구사항 추가 | 공통 기반 공유, 보안 특화 요구사항 추가 |

> **핵심 통찰:** 두 표준은 정책·조직·교육·SBOM 영역에서 공통 기반을 공유한다.
> 하나를 구축하면 다른 하나의 절반이 자동으로 충족된다.

---

## 비고 컬럼 표기 규칙

| 태그 | 의미 |
|------|------|
| `[공통]` | 두 표준 모두 요구 |
| `[5230]` | ISO/IEC 5230 전용 |
| `[18974]` | ISO/IEC 18974 전용 (보안 특화) |
| `[공급망]` | 소프트웨어 공급망 보안 관련 |
| `[규제]` | 국제 규제 연계 항목 (EO 14028, EU CRA, NTIA SBOM) |

---

## 통합 매핑 테이블

### G1: 프로그램 기반

| 그룹 | 항목ID | 요구사항 요약 | 왜 필요한가 | ISO/IEC 5230 | ISO/IEC 18974 | 담당 Agent | 산출물 파일 | 워크숍 모듈 | 비고 |
|------|--------|------------|-----------|-------------|--------------|-----------|------------|------------|------|
| G1 | G1.1 | 오픈소스 정책 수립 및 문서화 | 정책 없이 체계적 컴플라이언스 구축 불가; 모든 활동의 근거 | 3.1.1 | 3.1.1 | 03-policy-generator | output/policy/oss-policy.md | M1 | [공통] |
| G1 | G1.2 | 보안 보증 정책 수립 | 알려진 취약점 대응 체계의 공식 근거; 18974 특화 보안 정책 요소 포함 | — | 3.1.1 | 03-policy-generator | output/policy/oss-policy.md | M1 | [18974] |
| G1 | G1.3 | 오픈소스 담당자 및 조직 지정 | 명확한 책임 소재 없이는 의사결정 공백 발생 | 3.1.2 | 3.1.2 | 02-organization-designer | output/organization/role-definition.md | M1 | [공통] |
| G1 | G1.4 | 교육 프로그램 수립 | 담당자 역량 확보 및 지속적 유지; 표준 모두 교육 이수 증빙 요구 | 3.1.2 | 3.1.2 | 06-training-manager | output/training/curriculum.md | M6 | [공통] |
| G1 | G1.5 | 프로그램 범위 정의 | 대상 소프트웨어·제품 명확화로 효율적 자원 배분 가능 | 3.1.4 | 3.1.4 | 03-policy-generator | output/policy/oss-policy.md | M1 | [공통] |
| G1 | G1.6 | 라이선스 의무사항 검토 절차 수립 | 배포 전 라이선스 위반 방지; Copyleft 소스코드 공개 의무 등 | 3.1.5 | — | 04-process-designer | output/process/usage-approval.md | M2 | [5230] |

### G2: 관련 업무 정의 및 지원

| 그룹 | 항목ID | 요구사항 요약 | 왜 필요한가 | ISO/IEC 5230 | ISO/IEC 18974 | 담당 Agent | 산출물 파일 | 워크숍 모듈 | 비고 |
|------|--------|------------|-----------|-------------|--------------|-----------|------------|------------|------|
| G2 | G2.1 | 역할과 책임 (RACI) 수립 | 오픈소스 활동 주체·승인·검토 체계 명확화; 업무 공백 방지 | 3.2.2 | 3.2.2 | 02-organization-designer | output/organization/raci-matrix.md | M1 | [공통] |
| G2 | G2.2 | 외부 문의 수신 채널 운영 | 라이선스 의무사항 이행 요청 및 보안 취약점 신고 공식 채널 의무 | 3.2.1 | 3.2.1 | 02-organization-designer | output/organization/role-definition.md | M1 | [공통] |
| G2 | G2.3 | 인식 제고 프로그램 운영 | 전체 구성원이 정책을 알고 준수해야 컴플라이언스 실효성 보장 | 3.1.3 | 3.1.3 | 06-training-manager | output/training/resources.md | M6 | [공통] |

### G3-L: 라이선스 컴플라이언스 (ISO/IEC 5230 중심)

| 그룹 | 항목ID | 요구사항 요약 | 왜 필요한가 | ISO/IEC 5230 | ISO/IEC 18974 | 담당 Agent | 산출물 파일 | 워크숍 모듈 | 비고 |
|------|--------|------------|-----------|-------------|--------------|-----------|------------|------------|------|
| G3-L | G3L.1 | 라이선스 식별 및 분류 | SBOM 기반 컴포넌트별 라이선스 현황 파악; Copyleft 위험 식별 | 3.3.2 | — | 05-sbom-analyst | output/sbom/license-report.md, output/sbom/copyleft-risk.md | M3 | [5230] |
| G3-L | G3L.2 | 라이선스 의무사항 이행 | GPL·LGPL·AGPL 등 Copyleft 라이선스 의무 이행; 허용 라이선스 목록 관리 | 3.3.2 | — | 04-process-designer | output/process/distribution-checklist.md, output/policy/license-allowlist.md | M2 | [5230] |
| G3-L | G3L.3 | 컴플라이언스 산출물 생성 | 배포 시 고지문·소스코드 등 법적 의무 이행 증빙 파일 제공 의무 | 3.4.1 | — | 05-sbom-analyst | output/sbom/license-report.md | M3 | [5230] |
| G3-L | G3L.4 | 오픈소스 기여 정책 수립 | 업스트림 기여 시 IP 유출·라이선스 오염 위험 사전 방지 | 3.5.1 | — | 03-policy-generator | output/policy/oss-policy.md | M1 | [5230] |

### G3-S: 보안 보증 (ISO/IEC 18974 중심)

| 그룹 | 항목ID | 요구사항 요약 | 왜 필요한가 | ISO/IEC 5230 | ISO/IEC 18974 | 담당 Agent | 산출물 파일 | 워크숍 모듈 | 비고 |
|------|--------|------------|-----------|-------------|--------------|-----------|------------|------------|------|
| G3-S | G3S.1 | 알려진 취약점 식별 (CVE 스캔) | CVE 취약점 미파악 시 보안 사고·법적 책임 위험; EO 14028 요구사항 | — | 3.3.2 | 05-vulnerability-analyst | output/vulnerability/cve-report.md | M5 | [18974] |
| G3-S | G3S.2 | 취약점 추적 및 상태 관리 | 식별된 취약점을 대응 완료까지 지속 추적; 누락·방치 방지 | — | 3.3.3 | 05-vulnerability-analyst | output/vulnerability/cve-report.md | M5 | [18974] |
| G3-S | G3S.3 | CVE 위험 점수 평가 (CVSS) | CVSS 점수 기반 우선순위 결정; 자원 배분 효율화 | — | 3.3.4 | 05-vulnerability-analyst | output/vulnerability/cve-report.md | M5 | [18974] |
| G3-S | G3S.4 | 취약점 대응 및 패치 절차 | 발견된 취약점 신속 패치·업그레이드·완화 조치 체계 | — | 3.3.5 | 05-vulnerability-analyst | output/vulnerability/remediation-plan.md | M5 | [18974] |

### G3-B: SBOM 및 공급망 (공통)

| 그룹 | 항목ID | 요구사항 요약 | 왜 필요한가 | ISO/IEC 5230 | ISO/IEC 18974 | 담당 Agent | 산출물 파일 | 워크숍 모듈 | 비고 |
|------|--------|------------|-----------|-------------|--------------|-----------|------------|------------|------|
| G3-B | G3B.1 | SBOM 생성 (CycloneDX/SPDX) | 구성 요소 투명성 확보의 출발점; 라이선스·보안 분석 모두의 입력값 | 3.3.1 | 3.3.1 | 05-sbom-guide | output/sbom/[project].cdx.json, output/sbom/sbom-commands.sh | M3 | [공통, 공급망] |
| G3-B | G3B.2 | SBOM 관리 및 유지보수 | 릴리즈·업데이트 시 SBOM 최신 상태 유지; 형상 관리 통합 | — | 3.3.1 | 05-sbom-management | output/sbom/sbom-management-plan.md | M4 | [공급망] |
| G3-B | G3B.3 | SBOM 공유 (공급망 파트너) | 하위 공급망으로 투명성 전달; NTIA·EU CRA 공급망 공개 의무 대응 | — | 3.3.1 | 05-sbom-management | output/sbom/sbom-sharing-template.md | M4 | [공급망, 규제] |
| G3-B | G3B.4 | 공급망 취약점 지속 모니터링 | 신규 CVE 공개 시 영향받는 공급망 컴포넌트 즉시 파악 | — | 3.3.3 | 05-sbom-management | output/sbom/sbom-management-plan.md | M4 | [공급망] |

### G4: 준수 선언 및 유지

| 그룹 | 항목ID | 요구사항 요약 | 왜 필요한가 | ISO/IEC 5230 | ISO/IEC 18974 | 담당 Agent | 산출물 파일 | 워크숍 모듈 | 비고 |
|------|--------|------------|-----------|-------------|--------------|-----------|------------|------------|------|
| G4 | G4.1 | ISO/IEC 5230 자체 인증 선언 | 라이선스 컴플라이언스 능력 공식 선언; 공급망 파트너 신뢰 확보 | 3.6.1 | — | 07-conformance-preparer | output/conformance/declaration-draft.md | M6 | [5230] |
| G4 | G4.2 | ISO/IEC 18974 자체 인증 선언 | 보안 보증 능력 공식 선언; EO 14028 및 EU CRA 대응 증빙 | — | 3.4.1 | 07-conformance-preparer | output/conformance/declaration-draft.md | M6 | [18974] |
| G4 | G4.3 | 인증 유효기간 관리 (18개월) | 두 표준 모두 18개월마다 재선언 의무; 자동 만료 방지 | 3.6.2 | 3.4.2 | 07-conformance-preparer | output/conformance/submission-guide.md | M6 | [공통] |
| G4 | G4.4 | 정기 갭 분석 및 정책 갱신 | 기술·규제 환경 변화에 따른 체계 현행화; 갱신 선언 전 필수 | 3.6.2 | 3.4.2 | 07-conformance-preparer | output/conformance/gap-analysis.md | M6 | [공통] |

---

## 워크숍 모듈 매핑

| 모듈 | 명칭 | 포함 항목 | 관련 챕터 |
|------|------|---------|---------|
| M0 | 공급망 보안 개요 | 두 표준 소개, 이 매핑 문서 리뷰 | docs/00-overview, docs/00b-supply-chain |
| M1 | 조직 + 정책 | G1.1~G1.5, G2.1~G2.3, G3L.4 | docs/02-organization, docs/03-policy |
| M2 | 프로세스 | G1.6, G3L.2 | docs/04-process |
| M3 | SBOM 생성 + 라이선스 분석 | G3B.1, G3L.1, G3L.3 | docs/05-tools/sbom-generation |
| M4 | SBOM 관리 + 공유 | G3B.2, G3B.3, G3B.4 | docs/05-tools/sbom-management |
| M5 | 취약점 분석 | G3S.1~G3S.4 | docs/05-tools/vulnerability |
| M6 | 교육 + 인증 선언 | G1.2(교육), G1.4, G2.3, G4.1~G4.4 | docs/06-training, docs/07-conformance |

---

## 요약 통계

| 구분 | 항목 수 |
|------|--------|
| ISO/IEC 5230 매핑 항목 수 | 16 |
| ISO/IEC 18974 매핑 항목 수 | 19 |
| 두 표준 공통 항목 수 | 10 |
| 공급망 관련 항목 수 (`[공급망]` 태그) | 4 |
| 규제 연계 항목 수 (`[규제]` 태그) | 1 |
| **전체 항목 수** | **25** |

> **참고:** 공통 항목(10개)은 5230(16개)과 18974(19개) 양쪽에 모두 계산된다.
> 두 표준을 동시에 준비하면 공통 항목을 한 번만 작업하여 약 40%를 절약할 수 있다.

---

## 다음 단계

:::info 셀프스터디 모드 (약 1시간)
이 매핑 문서를 파악했으면 실제 산출물 생성을 시작하라.
`output/` 폴더가 비어있다면 아래 순서로 시작한다.
:::

1. **조직 설계** → `cd agents/02-organization-designer && claude`
2. **정책 생성** → `cd agents/03-policy-generator && claude`
3. **프로세스 설계** → `cd agents/04-process-designer && claude`
4. **SBOM 생성** → `cd agents/05-sbom-guide && claude`
5. **취약점 분석** → `cd agents/05-vulnerability-analyst && claude`
6. **교육 체계** → `cd agents/06-training-manager && claude`
7. **인증 선언** → `cd agents/07-conformance-preparer && claude`

:::tip 워크숍 모드 (M0 - 30분)
이 문서를 전체 팀과 함께 리뷰하고 담당자를 사전 지정한 뒤 M1으로 넘어간다.
:::

> 이 문서는 ISO/IEC 5230 **전체** 및 ISO/IEC 18974 **전체** 요구사항의
> 프로젝트 내 매핑 기준 문서입니다.
> 각 agent의 CLAUDE.md에서 이 파일을 참조합니다.
