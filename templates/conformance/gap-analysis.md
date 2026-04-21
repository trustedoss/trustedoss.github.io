# 갭 분석 리포트

<!-- 5230 §3.6.2.1, 18974 §4.4.2.1, §4.1.2.5, §4.1.2.6, §4.1.4.3 -->

---

리포트 유형: 갭 분석
생성일: YYYY-MM-DD HH:MM
분석 대상: output/ 전체 산출물
표준: ISO/IEC 5230 + ISO/IEC 18974

---

## 요약

| 구분            | 항목 수  |
| --------------- | -------- |
| ✅ 충족         | {N}개    |
| 🔶 부분충족     | {N}개    |
| ❌ 미충족       | {N}개    |
| **전체 진행률** | **{N}%** |

---

## 항목별 상세

### G1: 프로그램 기반

| 항목                              | 상태     | 산출물                                | 비고 |
| --------------------------------- | -------- | ------------------------------------- | ---- |
| G1.1 오픈소스 정책 수립           | ✅/🔶/❌ | output/policy/oss-policy.md           |      |
| G1.2 보안 보증 정책 검토 프로세스 | ✅/🔶/❌ | output/policy/oss-policy.md           |      |
| G1.3 담당자 및 조직 지정          | ✅/🔶/❌ | output/organization/                  |      |
| G1.4 교육 프로그램 수립           | ✅/🔶/❌ | output/training/curriculum.md         |      |
| G1.5 프로그램 범위 정의           | ✅/🔶/❌ | output/policy/oss-policy.md           |      |
| G1.6 라이선스 의무사항 검토 절차  | ✅/🔶/❌ | output/process/usage-approval.md      |      |
| G1.7 참여자 인식 기록             | ✅/🔶/❌ | output/training/completion-tracker.md |      |

### G2: 관련 업무 정의

| 항목                     | 상태     | 산출물                                 | 비고 |
| ------------------------ | -------- | -------------------------------------- | ---- |
| G2.1 역할과 책임 (RACI)  | ✅/🔶/❌ | output/organization/raci-matrix.md     |      |
| G2.2 외부 문의 수신 채널 | ✅/🔶/❌ | output/organization/role-definition.md |      |
| G2.3 인식 제고 프로그램  | ✅/🔶/❌ | output/training/                       |      |

### G3-L: 라이선스 컴플라이언스

| 항목                              | 상태     | 산출물                                   | 비고 |
| --------------------------------- | -------- | ---------------------------------------- | ---- |
| G3L.1 라이선스 식별 및 분류       | ✅/🔶/❌ | output/sbom/license-report.md            |      |
| G3L.2 라이선스 의무사항 이행      | ✅/🔶/❌ | output/process/distribution-checklist.md |      |
| G3L.3 컴플라이언스 산출물 생성    | ✅/🔶/❌ | output/sbom/license-report.md            |      |
| G3L.4 오픈소스 기여 정책          | ✅/🔶/❌ | output/policy/oss-policy.md              |      |
| G3L.5 라이선스 의무사항 충족 확인 | ✅/🔶/❌ | output/process/distribution-checklist.md |      |
| G3L.6 오픈소스 기여 프로세스      | ✅/🔶/❌ | output/policy/oss-policy.md              |      |

### G3-S: 보안 보증

| 항목                                | 상태     | 산출물                                   | 비고 |
| ----------------------------------- | -------- | ---------------------------------------- | ---- |
| G3S.1 알려진 취약점 식별 (CVE 스캔) | ✅/🔶/❌ | output/vulnerability/cve-report.md       |      |
| G3S.2 취약점 추적 및 상태 관리      | ✅/🔶/❌ | output/vulnerability/cve-report.md       |      |
| G3S.3 CVE 위험 점수 평가 (CVSS)     | ✅/🔶/❌ | output/vulnerability/cve-report.md       |      |
| G3S.4 취약점 대응 및 패치 절차      | ✅/🔶/❌ | output/vulnerability/remediation-plan.md |      |
| G3S.5 보안 산출물 배포 프로세스     | ✅/🔶/❌ | output/sbom/sbom-sharing-template.md     |      |
| G3S.6 보안 의무사항 충족 확인       | ✅/🔶/❌ | output/vulnerability/remediation-plan.md |      |

### G3-B: SBOM 및 공급망

| 항목                              | 상태     | 산출물                               | 비고 |
| --------------------------------- | -------- | ------------------------------------ | ---- |
| G3B.1 SBOM 생성                   | ✅/🔶/❌ | output/sbom/\*.cdx.json              |      |
| G3B.2 SBOM 관리 및 유지보수       | ✅/🔶/❌ | output/sbom/sbom-management-plan.md  |      |
| G3B.3 SBOM 공유 (공급망 파트너)   | ✅/🔶/❌ | output/sbom/sbom-sharing-template.md |      |
| G3B.4 공급망 취약점 지속 모니터링 | ✅/🔶/❌ | output/sbom/sbom-management-plan.md  |      |

### G4: 준수 선언

| 항목                                    | 상태     | 산출물                                  | 비고 |
| --------------------------------------- | -------- | --------------------------------------- | ---- |
| G4.1 ISO/IEC 5230 자체 인증 선언        | ✅/🔶/❌ | output/conformance/declaration-draft.md |      |
| G4.2 ISO/IEC 18974 자체 인증 선언       | ✅/🔶/❌ | output/conformance/declaration-draft.md |      |
| G4.3 인증 유효기간 관리 (18개월)        | ✅/🔶/❌ | output/conformance/submission-guide.md  |      |
| G4.4 정기 갭 분석 및 정책 갱신          | ✅/🔶/❌ | 이 파일                                 |      |
| G4.5 배포 소프트웨어 알려진 취약점 없음 | ✅/🔶/❌ | output/vulnerability/cve-report.md      |      |

---

## 시간 기반 항목 처리 현황

<!-- 초기 인증 시 부분충족이 정상인 항목 -->

| 항목                               | 계획                       | 다음 검토 예정일     |
| ---------------------------------- | -------------------------- | -------------------- |
| 18974 §4.1.2.5 주기적 검토 증거    | {검토 주기 및 담당자}      | YYYY-MM-DD           |
| 18974 §4.1.2.6 모범 사례 일치 검증 | {검증 담당자 지정}         | YYYY-MM-DD           |
| 18974 §4.1.4.3 지속적 개선 증거    | 이 갭 분석이 1회 감사 이력 | 갱신 시 (YYYY-MM-DD) |

---

## 미충족 항목 해소 계획

| 항목          | 해소 방법                          | 담당자 | 목표일     |
| ------------- | ---------------------------------- | ------ | ---------- |
| {미충족 항목} | {해당 agent 재실행 또는 수동 보완} | {이름} | YYYY-MM-DD |

---

## 감사 이력

<!-- 18974 §4.1.4.3 지속적 개선 증거 -->

| 회차       | 실시일     | 담당자 | 주요 발견사항     | 후속 조치             |
| ---------- | ---------- | ------ | ----------------- | --------------------- |
| 1회 (최초) | YYYY-MM-DD | {이름} | 초기 갭 분석 완료 | 미충족 항목 보완 진행 |
