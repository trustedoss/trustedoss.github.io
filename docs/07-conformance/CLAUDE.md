# 챕터 07 — 자체 인증 선언 (최종)

## 현재 위치: 7단계 - 자체 인증 선언 (7/7단계, 최종!)

## 이 챕터의 목표

지금까지 생성한 모든 산출물을 검토하고, 갭 분석을 통해 미완료 항목을 파악하며,
ISO/IEC 5230과 ISO/IEC 18974 자체 인증 선언문을 완성한다.

이 챕터가 완료되면 OpenChain 프로젝트 웹사이트에 자체 인증을 등록할 수 있다.

## 충족되는 체크리스트 항목

| 항목ID | 요구사항 | ISO/IEC 5230 | ISO/IEC 18974 |
|--------|---------|-------------|--------------|
| G4.1 | ISO/IEC 5230 자체 인증 선언 | 3.6.1 | — |
| G4.2 | ISO/IEC 18974 자체 인증 선언 | — | 4.4.1 |
| G4.3 | 인증 유효기간 관리 (18개월) | 3.6.2 | 4.4.2 |
| G4.4 | 정기 갭 분析 및 정책 갱신 | 3.6.2 | 4.4.2 |

> 이 단계는 ISO/IEC 5230 3.6.1, 3.6.2 및 ISO/IEC 18974 4.4.1, 4.4.2 전체 요구사항을 충족합니다.

## 전제 조건

`output/` 전체 산출물이 완료된 상태:
- [ ] output/organization/ (챕터 02)
- [ ] output/policy/ (챕터 03)
- [ ] output/process/ (챕터 04)
- [ ] output/sbom/ (챕터 05-1, 05-2)
- [ ] output/vulnerability/ (챕터 05-3)
- [ ] output/training/ (챕터 06)

## 완료 기준

- [ ] `output/conformance/gap-analysis.md` 생성됨
- [ ] `output/conformance/declaration-draft.md` 생성됨
- [ ] `output/conformance/submission-guide.md` 생성됨
- [ ] 갭 분석에서 미충족 항목이 없거나 해소 계획이 있음
- [ ] 자체 인증 선언문이 완성됨

## agent 실행 안내

```bash
cd agents/07-conformance-preparer
claude
```

agent가 output/ 전체를 스캔하고 25개 체크리스트 항목과 대조하여 갭 분석을 실행한다.

## 자체 인증 등록 절차

선언문 완성 후 아래 링크에서 자체 인증을 등록한다:

**ISO/IEC 5230 (라이선스 컴플라이언스):**
https://www.openchainproject.org/conformance

**ISO/IEC 18974 (보안 보증):**
https://www.openchainproject.org/conformance

등록 시 필요한 정보:
- 회사명 및 담당자 이름
- 선언 날짜
- 적용 제품/소프트웨어 범위

## 유지 관리 주기

- **18개월마다**: 재선언 의무 (두 표준 모두 동일)
- **연 1회 권장**: 갭 분석 재실행 및 정책 검토
- **릴리즈마다**: SBOM 갱신 및 취약점 재스캔

## 셀프스터디 경로

:::info 셀프스터디 모드 (약 2시간)
갭 분석 결과에 따라 추가 작업이 필요할 수 있습니다.
:::

1. `docs/07-conformance/index.md` 읽기
2. `cd agents/07-conformance-preparer && claude` 실행
3. 갭 분석 결과 확인 및 미충족 항목 보완
4. 선언문 검토 및 수정
5. OpenChain 웹사이트 자체 인증 등록

## 자주 발생하는 문제

**Q: 갭 분석에서 미충족 항목이 나왔어요. 어떻게 하나요?**
A: 해당 챕터의 agent를 다시 실행하거나, 직접 문서를 보완한다.
agent가 구체적인 해소 방법을 안내한다.

**Q: 자체 인증 선언은 법적 구속력이 있나요?**
A: 법적 구속력은 없지만, 허위 선언 시 신뢰 손상 및 공급망 파트너와의 관계에 영향을 줄 수 있다.

**Q: 인증 유효기간이 지나면 어떻게 되나요?**
A: 자동으로 만료된다. OpenChain 웹사이트에서 재선언이 필요하다.
submission-guide.md 에 리마인더 설정 방법이 포함된다.

## 완료 축하

모든 산출물을 완성하고 자체 인증을 선언하면, 당신의 조직은:
- ISO/IEC 5230 준수 선언 조직이 된다 (라이선스 컴플라이언스)
- ISO/IEC 18974 준수 선언 조직이 된다 (보안 보증)
- 공급망 파트너에게 신뢰할 수 있는 오픈소스 관리 체계를 증명할 수 있다

**OpenChain 자체 인증 등록:**
https://www.openchainproject.org/conformance
