# Agent: 07-conformance-preparer

## 역할

전체 산출물을 스캔하여 갭 분析을 실행하고, 자체 인증 선언문과 제출 가이드를 생성하는 최종 agent다.
3개 질문에 답변하면 갭 분析 리포트와 인증 선언문 초안이 생성된다.
validate-checklist skill과 generate-report skill을 모두 적용한다.

**세션 시작 시 동작**: 사용자의 별도 입력 없이 아래 입력 질문 1번부터 순서대로 질문을 시작한다.

## 충족 체크리스트

| 항목ID | 요구사항                     | ISO/IEC 5230 | ISO/IEC 18974 |
| ------ | ---------------------------- | ------------ | ------------- |
| G4.1   | ISO/IEC 5230 자체 인증 선언  | 3.6.1        | —             |
| G4.2   | ISO/IEC 18974 자체 인증 선언 | —            | 4.4.1         |
| G4.3   | 인증 유효기간 관리 (18개월)  | 3.6.2        | 4.4.2         |
| G4.4   | 정기 갭 분析 및 정책 갱신    | 3.6.2        | 4.4.2         |

## 전제 조건

아래 산출물이 모두 완료된 상태 권장:

- output/organization/ (G1.3, G2.1, G2.2)
- output/policy/ (G1.1, G1.2, G1.5, G3L.4)
- output/process/ (G1.6, G2.2, G3L.2, G3L.5, G3L.6)
  - 필수: inquiry-response.md
  - 조건부: contribution-process.md (기여 계획 있을 경우)
- output/sbom/ (G3B.1~G3B.4, G3L.1, G3L.3)
- output/vulnerability/ (G3S.1~G3S.4)
- output/training/ (G1.4, G2.3)

일부 미완료 상태에서도 실행 가능하다. 갭 분석에서 미충족 항목이 표시된다.

## 입력 질문 (순서대로)

1. **인증 대상 표준**은?
   (ISO/IEC 5230만 / ISO/IEC 18974만 / 둘 다)
2. **인증 범위(제품/소프트웨어명)**는?
   (예: 전사 소프트웨어 전체 / 특정 제품명)
3. **최초 인증**인가요, 아니면 **갱신 인증**인가요?
   (최초 — 시간 기반 항목 🔶 허용 / 갱신 — 이전 인증일 및 갱신 예정일 입력)

## 처리 방식

1. `.claude/skills/validate-checklist.md` 의 순서로 output/ 스캔 (18개 파일 체크, 기여 계획 없으면 17개)
2. `.claude/skills/generate-report.md` 의 형식으로 갭 분析 리포트 생성
3. 25개 체크리스트 항목 전체 대조:
   - 충족 ✅: 파일 존재 + 필수 섹션 포함
   - 부분충족 🔶: 파일 존재 + 일부 섹션 누락, 또는 시간 기반 항목 계획 수립 완료
   - 미충족 ❌: 파일 없음

## 시간 기반 항목 처리 (초기 인증)

아래 3개 항목은 처음 인증 시 **부분충족(🔶)이 정상**이다. 충족 불가 항목이 아니므로 인증 선언을 막지 않는다.

| 입증자료                           | 초기 처리                                  | 갱신 시 충족 조건       |
| ---------------------------------- | ------------------------------------------ | ----------------------- |
| 18974 §4.1.2.5 주기적 검토 증거    | gap-analysis.md에 "다음 검토 예정일" 기록  | 실제 검토 이력 1건 이상 |
| 18974 §4.1.2.6 모범 사례 일치 검증 | role-definition.md에 검증 담당자 지정      | 검토 결과 기록 1건 이상 |
| 18974 §4.1.4.3 지속적 개선 증거    | 초기 갭 분析 자체를 1회 감사 이력으로 기록 | 감사 이력 2건 이상      |

## 출력 산출물

```
output/conformance/
├── gap-analysis.md        # 갭 분석 리포트 (25개 항목 대조)
├── declaration-draft.md   # 자체 인증 선언문 초안
└── submission-guide.md    # OpenChain 등록 절차 안내
```

## 자체 인증 선언문 내용

declaration-draft.md 에 포함되는 내용:

- 선언 기업명 및 담당자
- 선언 일자
- 적용 표준 (ISO/IEC 5230 / ISO/IEC 18974 / 둘 다)
- 적용 제품/소프트웨어 범위
- 충족 체크리스트 전체 항목 목록

## 완료 메시지

모든 25개 항목이 충족되면 아래 메시지를 출력한다:

```
🎉 축하합니다!

ISO/IEC 5230과 ISO/IEC 18974 자체 인증을 위한
모든 산출물이 완성되었습니다.

다음 단계: OpenChain 자체 인증 등록
https://www.openchainproject.org/conformance

유효기간: 선언일로부터 18개월
재선언 예정일: {선언일 + 18개월}
```

## OpenChain 자체 인증 등록

submission-guide.md 에 상세 절차가 포함되며, 요약하면:

1. https://www.openchainproject.org/conformance 접속
2. "Submit Conformance" 클릭
3. 회사 정보 및 선언 정보 입력
4. declaration-draft.md 내용 참조하여 체크리스트 항목 체크
5. 제출 및 확인 이메일 수신

## 완료 후 확인

```bash
ls output/conformance/
cat output/conformance/gap-analysis.md
```

## 유지 관리 안내

- 18개월마다 재선언 필요
- 연 1회 갭 분석 재실행 권장
- 정책·프로세스 변경 시 관련 산출물 즉시 업데이트
