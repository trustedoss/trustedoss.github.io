---
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - "ISO/IEC 5230: G4.1 (3.6.1), G4.3 (3.6.2), G4.4 (3.6.2)"
  - "ISO/IEC 18974: G4.2 (4.4.1), G4.3 (4.4.2), G4.4 (4.4.2)"
셀프스터디 소요시간: 2시간
---

# 자체 인증 선언: 마지막 단계

## 1. 이 챕터에서 하는 일

여기까지 온 것을 축하한다. 지금까지 조직 구성, 정책 수립, 프로세스 설계, SBOM 생성 및 관리, 취약점 분석, 교육 체계 구축까지 오픈소스 관리 체계의 모든 핵심 영역을 완성했다.

지금까지 생성한 산출물 전체 목록을 보자. 이 모든 것이 갖춰졌다면 자체 인증 선언 준비가 된 것이다:

| 폴더 | 산출물 |
|------|--------|
| `output/organization/` | role-definition.md, raci-matrix.md, appointment-template.md |
| `output/policy/` | oss-policy.md, license-allowlist.md |
| `output/process/` | usage-approval.md, distribution-checklist.md, vulnerability-response.md, process-diagram.md |
| `output/sbom/` | [project].cdx.json, sbom-commands.sh, license-report.md, copyleft-risk.md, sbom-management-plan.md, sbom-sharing-template.md |
| `output/vulnerability/` | cve-report.md, remediation-plan.md |
| `output/training/` | curriculum.md, completion-tracker.md, resources.md |

이번 챕터에서는 이 산출물들을 바탕으로 갭 분석을 수행하고, 자체 인증 선언문을 완성하여 OpenChain 공식 등록까지 마무리한다.

---

## 2. 배경 지식: 자체 인증이란 무엇인가

OpenChain 자체 인증(Self-Certification)은 제3자 감사 없이 조직 스스로 표준 요구사항을 충족함을 선언하는 방식이다. 주요 특징은 다음과 같다:

- **자기 선언 방식**: 외부 감사 기관 없이 조직이 직접 체크리스트를 점검하고 선언한다.
- **공식 인정**: OpenChain 웹사이트에 등록하면 OpenChain 프로젝트로부터 공식 인정을 받는다.
- **법적 구속력 없음**: 법적 의무는 아니지만, 공급망 파트너에게 신뢰 신호로 활용된다.
- **유효기간 18개월**: OpenChain 권고에 따라 18개월마다 재확인이 권장된다.

ISO/IEC 5230(라이선스 컴플라이언스)과 ISO/IEC 18974(보안 보증) 두 표준 모두 자체 인증 경로를 제공하며, 동시 인증도 가능하다.

---

## 3. 자체 인증 전 최종 점검 (셀프스터디 경로)

:::info 셀프스터디 모드 (약 2시간)
갭 분석 결과에 따라 추가 작업이 필요할 수 있습니다. conformance-preparer agent가 자동으로 전체 output/ 폴더를 스캔하여 미충족 항목을 식별해 줍니다.
:::

다음 순서로 진행한다:

1. 이 문서를 끝까지 읽는다.
2. conformance-preparer agent를 실행한다:
   ```bash
   cd agents/07-conformance-preparer && claude
   ```
   agent가 자동으로 `output/` 전체를 스캔하여 갭 분석 리포트를 생성한다.
3. 생성된 `output/conformance/gap-analysis.md`를 열어 미충족 항목을 확인한다.
4. 미충족 항목이 있다면 해당 챕터로 돌아가 보완한다.
5. `output/conformance/declaration-draft.md` 선언문을 검토하고 수정한다.
6. `output/conformance/submission-guide.md`를 참고하여 OpenChain 웹사이트에 자체 인증을 등록한다.

---

## 4. 갭 분석 리포트 이해하기

`output/conformance/gap-analysis.md`는 다음 구성으로 생성된다:

| 섹션 | 내용 |
|------|------|
| 충족 항목 목록 | 요구사항을 완전히 충족한 항목과 근거 산출물 |
| 부분충족 항목 | 일부 충족되었으나 보완이 필요한 항목과 보완 방법 |
| 미충족 항목 | 아직 충족되지 않은 항목과 해당 챕터 링크 |
| 전체 진행률 | 충족/부분충족/미충족 비율 (%) |

갭 분析에서 미충족 항목이 나왔다고 당황하지 않아도 된다. 각 항목에는 어느 챕터로 돌아가면 되는지 링크가 포함되어 있다. 부분충족 항목은 작은 수정만으로도 충족으로 전환할 수 있는 경우가 많다.

**G4.5 — 배포 소프트웨어 알려진 취약점 없음 확인 (18974 §4.4.1.1) 처리 방법:**

이 항목은 "배포 소프트웨어에 알려진 취약점이 없음을 검증·선언"하는 요구사항이다. 취약점이 있는 경우 다음과 같이 처리한다:

| 상황 | 처리 방법 |
|------|---------|
| 취약점이 **실제 배포 소프트웨어**에 있는 경우 | 배포 전 패치 완료 후 선언. `output/vulnerability/remediation-plan.md`에 조치 완료 기록 |
| 취약점이 있지만 **완화 조치가 완료**된 경우 | 완화 조치 내용과 잔존 리스크를 `remediation-plan.md`에 문서화하고 조건부 선언 가능 |
| **실습용 샘플**의 취약점인 경우 | 샘플은 실제 배포 소프트웨어가 아니므로, 실제 배포 대상 제품 기준으로 판단 |

> 자체 인증은 특정 소프트웨어 "범위"에 대한 선언이다. 범위(§3.1.4 / §4.1.4)를 명확히 정의하면 실습 샘플이 아닌 실제 제품에 대해 선언할 수 있다.

---

## 5. OpenChain 자체 인증 선언 절차

갭 분석이 완료되고 미충족 항목이 없거나 해소 계획이 마련되었다면 다음 절차로 공식 등록을 진행한다:

**1단계**: `output/conformance/declaration-draft.md` 내용을 최종 검토하고 확정한다.

**2단계**: 브라우저에서 https://www.openchainproject.org/conformance 에 접속한다.

**3단계**: ISO/IEC 5230 또는 ISO/IEC 18974 중 인증할 표준을 선택한다. (또는 두 표준 모두 선택)

**4단계**: 온라인 자체 인증 체크리스트를 작성하고 제출한다. `declaration-draft.md`의 내용을 참고하면 빠르게 완성할 수 있다.

**5단계**: 등록이 완료되면 OpenChain 로고 사용이 가능하며, 공식 인정 기업 목록에 등재된다.

> 이 단계는 ISO/IEC 5230 G4.1 (3.6.1) 및 ISO/IEC 18974 G4.2 (4.4.1) 요구사항을 충족합니다.

:::info 충족되는 표준 요구사항
이 실습을 완료하면 아래 요구사항이 충족됩니다.

**ISO/IEC 5230**

| 항목 ID | 요구사항 | 자체인증 체크리스트 |
|---|---|---|
| 3.6.1 | 자체 인증 선언 | Do you confirm that your program meets all the requirements of this specification? |
| 3.6.2 | 인증 유효기간 관리 | Do you have a process to confirm the program meets the requirements at least once every 18 months? |

**ISO/IEC 18974**

| 항목 ID | 요구사항 | 자체인증 체크리스트 |
|---|---|---|
| 4.4.1 | 자체 인증 선언 (보안) | Do you confirm that your security assurance program meets all the requirements of this specification? |
| 4.4.2 | 보안 인증 유효기간 관리 | Do you have a process to confirm the security assurance program meets the requirements at least once every 18 months? |
:::

---

## 6. 두 표준 동시 인증 전략

ISO/IEC 5230과 ISO/IEC 18974는 많은 요구사항을 공유한다. 동시 인증을 목표로 한다면 다음 전략이 효율적이다:

- **공통 항목 10개**: 두 표준이 공유하는 항목은 한 번의 작업으로 동시에 충족된다.
- **5230 전용 6개**: 라이선스 컴플라이언스에 특화된 항목을 추가로 충족한다.
- **18974 전용 9개**: 보안 보증에 특화된 항목을 추가로 충족한다.

권장 작업 순서: 공통 항목 먼저 완료 → ISO/IEC 5230 전용 항목 → ISO/IEC 18974 전용 항목 순으로 진행하면 약 **40% 작업 절감** 효과를 얻을 수 있다. 이 키트의 챕터 구성 자체가 이 순서를 따르도록 설계되어 있다.

---

## 7. 인증 후 유지 관리

자체 인증은 한 번으로 끝나지 않는다. 지속적인 유지 관리가 필요하다:

- **연 1회 정책 검토**: `output/policy/oss-policy.md`와 `output/policy/license-allowlist.md`를 연 1회 검토하고 최신 상태로 유지한다.
- **담당자 변경 시 인수인계**: RACI 매트릭스와 임명장 템플릿을 활용하여 체계적인 인수인계 절차를 밟는다.
- **새 버전 표준 출시 시 대응**: ISO/IEC 5230과 ISO/IEC 18974의 개정판이 출시되면 갭 분석을 재수행한다.
- **18개월마다 재확인**: OpenChain 권고에 따라 18개월 주기로 자체 인증을 재확인하고 필요 시 갱신 선언을 한다.

> 이 단계는 ISO/IEC 5230 G4.3 (3.6.2) 및 ISO/IEC 18974 G4.3 (4.4.2) 요구사항을 충족합니다.

---

## 8. 완료 확인 체크리스트

이 챕터를 마치기 전에 아래 항목을 모두 확인한다:

- [ ] `output/conformance/gap-analysis.md` 생성됨
- [ ] `output/conformance/declaration-draft.md` 생성됨
- [ ] `output/conformance/submission-guide.md` 생성됨
- [ ] 갭 분석에서 미충족 항목이 없거나 해소 계획이 있음
- [ ] 자체 인증 선언문이 완성됨

---

## 9. 완료 축하 및 다음 단계

이제 귀사의 오픈소스 관리 체계가 완성되었다.

조직 구성부터 정책, 프로세스, SBOM, 취약점 관리, 교육, 그리고 자체 인증 선언까지 — ISO/IEC 5230과 ISO/IEC 18974가 요구하는 모든 요소를 체계적으로 갖추었다. 이 성과는 공급망 파트너와 고객에게 귀사의 오픈소스 관리 성숙도를 증명하는 강력한 신뢰 신호가 될 것이다.

인증 이후에도 오픈소스 생태계와 함께 성장할 수 있는 방법들:

- **OpenChain KWG 커뮤니티 참여**: 국내 OpenChain 커뮤니티에서 다른 기업들과 경험을 공유한다.
  https://openchain-project.github.io/OpenChain-KWG
- **사내 오픈소스 기여 정책 수립**: 소비에서 기여로 — 오픈소스 커뮤니티에 기여하는 정책을 수립한다.
- **OSPO(Open Source Program Office) 설립 검토**: 오픈소스 관리를 전담하는 조직을 공식화하여 장기적인 역량을 강화한다.
