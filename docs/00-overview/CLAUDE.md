# 챕터 00 — 전체 개요

## 현재 위치: 전체 여정의 시작점 (0/7단계)

이 챕터는 모든 여정의 출발점이다. 실제 산출물을 생성하지는 않지만,
전체 키트의 목적과 구조를 이해하는 데 필수적이다.

## 이 챕터의 목표

ISO/IEC 5230 (라이선스 컴플라이언스)과 ISO/IEC 18974 (보안 보증) 두 표준의 핵심 개념을 파악하고,
전체 여정에서 무엇을 달성하게 되는지, 어떤 순서로 진행해야 하는지 이해한다.

두 표준은 상호 보완적이다. 공통 기반(정책·조직·교육·SBOM)을 공유하므로
하나를 구축하면 다른 하나의 절반이 자동으로 충족된다.

## 충족되는 체크리스트 항목

이 챕터 자체는 체크리스트 항목을 직접 충족하지 않는다 (개요 챕터).
그러나 `checklist-mapping.md` 를 통해 전체 25개 항목의 지도를 파악한다.

## 체크리스트 매핑 문서 보는 방법

`docs/00-overview/checklist-mapping.md` 를 열어 아래 순서로 읽는다:

1. **두 표준 비교 표** → 각 표준의 목적과 범위 파악
2. **통합 매핑 테이블** → G1~G4 그룹별로 담당 Agent와 산출물 확인
3. **비고 컬럼 태그** → `[공통]` `[5230]` `[18974]` `[공급망]` `[규제]` 로 항목 성격 파악
4. **요약 통계** → 전체 25개 항목 현황 숫자로 확인

## 전체 산출물 목록 미리보기

이 키트를 완료하면 아래 산출물이 생성된다:

| 단계 | 산출물 |
|------|--------|
| 조직 | role-definition.md, raci-matrix.md, appointment-template.md |
| 정책 | oss-policy.md, license-allowlist.md |
| 프로세스 | usage-approval.md, distribution-checklist.md, vulnerability-response.md, process-diagram.md |
| SBOM | [project].cdx.json, sbom-commands.sh, license-report.md, copyleft-risk.md |
| SBOM 관리 | sbom-management-plan.md, sbom-sharing-template.md |
| 취약점 | cve-report.md, remediation-plan.md |
| 교육 | curriculum.md, completion-tracker.md, resources.md |
| 인증 | gap-analysis.md, declaration-draft.md, submission-guide.md |

## 전제 조건

없음. 이 챕터가 시작점이다.

## 완료 기준

- [ ] 두 표준의 차이점과 공통점을 설명할 수 있다
- [ ] checklist-mapping.md 의 전체 구조를 파악했다
- [ ] 다음 단계(챕터 00b 또는 챕터 01)로 이동할 준비가 되었다

## 셀프스터디 경로

:::info 셀프스터디 모드 (약 1시간)
충분한 시간을 갖고 각 문서를 이해하며 진행합니다.
:::

1. `docs/00-overview/index.md` 읽기 — 전체 여정 개요 파악
2. `docs/00-overview/checklist-mapping.md` 읽기 — 전체 체크리스트 25개 항목 파악
3. `docs/00b-supply-chain/` 으로 이동하여 배경 지식 습득


## 자주 발생하는 문제

**Q: 두 표준 중 어느 것을 먼저 해야 하나요?**
A: 동시에 진행한다. 공통 기반이 크기 때문에 별도로 진행하면 중복 작업이 발생한다.

**Q: 두 표준 모두 해야 하나요?**
A: 선택이다. 라이선스 컴플라이언스만 필요하면 5230만, 보안 보증도 필요하면 18974 추가.
이 키트는 두 표준을 동시에 달성하도록 설계되었다.

**Q: 자체 인증과 제3자 인증의 차이는?**
A: 두 표준 모두 자체 인증(Self-Certification) 방식이다. 외부 심사 없이 OpenChain 웹사이트에서 직접 선언한다.

## 다음 단계

- **셀프스터디**: `supply-chain.md` 읽기 (배경 지식) → `sbom-101.md` 읽기 → `docs/01-setup/` 실습
- **바로 시작**: `cd agents/02-organization-designer && claude`

---

## 공급망 보안 배경 지식 (supply-chain.md, sbom-101.md)

이 챕터에는 공급망 보안 배경 지식 문서 2개가 포함되어 있다.

### supply-chain.md
소프트웨어 공급망 보안의 현실을 실제 사고 사례를 통해 이해하는 문서.

**주요 사고 사례:**
- **SolarWinds (2020)**: 빌드 파이프라인 침해로 18,000개 조직 영향
- **Log4Shell (2021)**: Log4j 취약점으로 수억 개 시스템 위협
- **XZ Utils (2024)**: 오픈소스 프로젝트 내 악의적 백도어 삽입

**주요 규제 동향:**
| 규제/표준 | 내용 | SBOM 요구 |
|----------|------|---------|
| EO 14028 (미국, 2021) | 연방 조달 소프트웨어 보안 강화 | SBOM 필수 |
| EU CRA (2024) | EU 시장 출시 디지털 제품 보안 의무 | SBOM 권고 |
| NTIA SBOM 지침 | SBOM 최소 요소 정의 | SBOM 표준화 |

### sbom-101.md
SBOM의 기술적 세부사항을 다루는 문서:
- NTIA 7가지 최소 요소
- CycloneDX vs SPDX 포맷 비교
- SBOM 생태계 (생성 → 관리 → 분석 → 공유)
- 생성 도구 개요 (syft, cdxgen)
