# Skill: 리포트 생성 표준 (generate-report)

## 적용 대상
agents/05-sbom-analyst
agents/05-vulnerability-analyst
agents/07-conformance-preparer

## 리포트 헤더 형식
---
리포트 유형: {유형명}
생성일: YYYY-MM-DD HH:MM
대상 프로젝트: {프로젝트명}
사용 도구: {도구명 및 버전}
---

## 3단 구조
### 1. 요약
- 전체 현황을 3-5줄로 요약
- 즉시 조치 필요 항목 수 강조

### 2. 상세
- 표 형식 사용
- 컬럼: 컴포넌트 | 버전 | 항목 | 심각도 | 조치

### 3. 조치사항
- 심각도 순서로 정렬 (Critical → High → Medium → Low)
- 각 항목마다 구체적인 조치 방법 명시
- 예상 조치 소요시간 포함

## 심각도 표기
| 심각도 | 표기 | 기준 |
|---|---|---|
| Critical | 🔴 Critical | 즉시 조치 필요 |
| High | 🟠 High | 1주일 내 조치 |
| Medium | 🟡 Medium | 1개월 내 조치 |
| Low | 🟢 Low | 다음 릴리즈 시 조치 |
| Info | ⚪ Info | 참고용 |
