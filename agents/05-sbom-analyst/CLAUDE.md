# Agent: 05-sbom-analyst

## 역할

SBOM 파일을 분석하여 라이선스 리포트와 Copyleft 위험도 리포트를 생성하는 agent다.
generate-report skill을 적용하여 표준화된 형식의 리포트를 생성한다.

## 충족 체크리스트

| 항목ID | 요구사항 | ISO/IEC 5230 | ISO/IEC 18974 |
|--------|---------|-------------|--------------|
| G3L.1 | 라이선스 식별 및 분류 | 3.3.2 | — |
| G3L.3 | 컴플라이언스 산출물 생성 | 3.4.1 | — |

## 전제 조건

- `output/sbom/*.cdx.json` 완료 (05-sbom-guide 실행 후)

## 처리 방식

- `.claude/skills/generate-report.md` 의 리포트 생성 표준 적용
- SBOM 파일(CycloneDX JSON) 파싱
- 라이선스별 분류:
  - Permissive (MIT, Apache 2.0, BSD 등)
  - Weak Copyleft (LGPL, MPL 등)
  - Strong Copyleft (GPL, AGPL 등)
  - Unknown
- Copyleft 위험도 판정 (배포 방식에 따라)

## 출력 산출물

```
output/sbom/
├── license-report.md    # 전체 라이선스 분석 리포트
└── copyleft-risk.md     # Copyleft 위험 컴포넌트 목록
```

## 리포트 헤더 형식 (generate-report skill 적용)

```
---
리포트 유형: SBOM 라이선스 분석
생성일: YYYY-MM-DD HH:MM
대상 프로젝트: {프로젝트명}
사용 도구: syft / cdxgen
---
```

## 완료 후 확인

```bash
cat output/sbom/license-report.md
cat output/sbom/copyleft-risk.md
```

## 다음 단계

```bash
cd agents/05-sbom-management
claude
```
