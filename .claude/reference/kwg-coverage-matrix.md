# KWG 템플릿 ↔ TrustedOSS 산출물 커버리지 매트릭스

작성일: 2026-06-05 · 근거: `.claude/reference/kwg/content/ko/guide/templates/` 동기화본과 `output-sample/` 실제 산출물 직접 대조.

목적: KWG 공식 정책/프로세스 템플릿의 모든 절을 우리가 생성하는 산출물 어디에서 충족하는지 1:1로 확인하고, 실제 누락을 식별한다. (P0-0)

## 핵심 결론

- 우리는 KWG의 통합 정책+프로세스 템플릿을 **모듈형 산출물 세트**(조직, 정책, 프로세스, SBOM, 취약점, 교육, 인증)로 분산 생성한다.
- **산출물 세트 전체 기준으로는 KWG 정책 11절과 프로세스 6대 프로세스가 거의 모두 커버된다.** 단일 `oss-policy.md`만 보면 누락처럼 보이는 항목 다수가 실제로는 다른 산출물 파일에서 충족된다.
- 실제 갭은 좁다(아래 "갭" 참조). P0-0 #2(템플릿 정렬)는 대규모 재구조화가 아니라 **좁은 보강 + 추적성 표면화**로 충분하다.

## 정책 템플릿(11절) 커버리지

| KWG 정책 템플릿 절                  | 우리 산출물 위치                                                                                  | 상태                     |
| ----------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------ |
| 1. 목적 및 적용 범위                | `policy/oss-policy.md` §1                                                                         | 충족                     |
| 2. 정의(용어)                       | (산출물에 없음. `website/reference/glossary`는 가이드용 페이지)                                   | **갭**                   |
| 3. 역할 및 책임                     | `organization/role-definition.md` §1~7 + `raci-matrix.md`                                         | 충족(조직 산출물로 분리) |
| 4. 라이선스 컴플라이언스            | `oss-policy.md` §2 + `process/usage-approval.md` + `process/distribution-checklist.md` + `sbom/*` | 충족(분산)               |
| 4.1 식별·의무 검토                  | `usage-approval.md` §1,§4                                                                         | 충족                     |
| 4.2 설계·사용 사례별 처리           | `oss-policy.md` §2 + `policy/license-allowlist.md`                                                | 충족                     |
| 4.3 산출물 생성·관리                | `distribution-checklist.md` §3,§5 + `sbom/*`                                                      | 충족                     |
| 4.4 SBOM 생성·관리                  | `sbom/*` + `distribution-checklist.md` §1                                                         | 충족                     |
| 4.5 컴플라이언스 이슈 대응          | `distribution-checklist.md` §6 + `usage-approval.md`                                              | 충족                     |
| 5. 보안 보증                        | `oss-policy.md` §4 + `process/vulnerability-response.md`                                          | 충족                     |
| 6. 교육 및 인식 제고(평가·기록 3년) | `oss-policy.md` §7 + `training/curriculum.md`·`completion-tracker.md`                             | 충족                     |
| 7. 외부 오픈소스 기여               | `oss-policy.md` §5 + `process/contribution-process.md`                                            | 충족                     |
| 8. 사내 프로젝트 공개               | `process/project-publication-process.md` (조건부 생성)                                            | **부분**(조건부)         |
| 9. 외부 문의 대응                   | `process/inquiry-response.md` (전체 파일, §1~6)                                                   | 충족                     |
| 10. 프로그램 효과성 측정·개선(KPI)  | `oss-policy.md` §3                                                                                | 충족                     |
| 11. ISO 표준 준수 선언              | `conformance/declaration-draft.md`                                                                | 충족                     |

## 프로세스 템플릿(6대 프로세스) 커버리지

| KWG 프로세스 템플릿                        | 우리 산출물 위치                                                                                | 상태             |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------- | ---------------- |
| 1. 오픈소스 프로세스 11단계(식별~모니터링) | `process/usage-approval.md`(도입~승인) + `process/distribution-checklist.md`(고지~배포~배포 후) | 충족(2파일 분산) |
| 2. 보안 취약점 관리 프로세스               | `process/vulnerability-response.md` §1~8(탐지·평가·해결·모니터링·통지·외부신고·출시전테스트)    | 충족             |
| 3. 외부 문의 대응 프로세스(8단계)          | `process/inquiry-response.md` §4(대응 절차 8단계)                                               | 충족             |
| 4. 오픈소스 기여 프로세스                  | `process/contribution-process.md`                                                               | 충족             |
| 5. 사내 프로젝트 공개 프로세스             | `process/project-publication-process.md` (조건부 생성)                                          | **부분**(조건부) |
| 6. 교육·평가 실행 프로세스                 | `training/curriculum.md` + `completion-tracker.md`                                              | 충족             |

## 식별된 갭과 권장 조치 (→ P0-0 #2 입력)

1. **용어 정의 누락**(정책 §2): 생성 산출물에 표준 용어 정의 절이 없다.
   - 조치: `templates/policy/oss-policy.md`에 "정의(용어)" 절을 추가하고, 가이드의 `reference/glossary`와 교차 링크. (작은 추가)
2. **사내 공개(정책 §8 / 프로세스 §5)가 조건부 생성**: 기본 산출물에서 빠질 수 있다.
   - 조치: 최소한 정책 본문에 "사내 공개 시 절차는 `project-publication-process.md` 참조" 요약 절을 항상 포함. 또는 조건부 유지하되 커버리지 문서에 명시.
3. **추적성 표면화**: KWG 절 번호 매핑이 현재 HTML 주석에만 있음.
   - 조치: 각 산출물 상단 또는 절에 "KWG 정책/프로세스 템플릿 ○절 기준"을 가시 표기(권위 신호).

## 재평가 메모

이전 계획 P0-0 서술("공식 템플릿과 구조가 상당히 다르다 / 다수 누락")은 **단일 `oss-policy.md` 기준**의 관찰이었다. 산출물 세트 전체로 보면 커버리지는 강하며, 실제 갭은 위 3가지로 좁다. 따라서 P0-0 #2는 대규모 재구조화가 아니라 좁은 보강과 추적성 표면화로 수행한다.
