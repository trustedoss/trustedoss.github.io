---
리포트 유형: Copyleft 위험도 분석
생성일: 2026-03-23 07:11
대상 프로젝트: vulnerable-java-app
사용 도구: syft 1.42.3
---

# Copyleft 위험도 리포트

## 1. 요약

- 분석 대상: `java-vulnerable.cdx.json` (CycloneDX 1.6, 컴포넌트 3개)
- **Strong Copyleft (GPL/AGPL) 컴포넌트: 0개**
- **Weak Copyleft (LGPL/MPL) 컴포넌트: 0개**
- 식별된 컴포넌트 2개는 모두 **Apache-2.0 (Permissive)** 으로 Copyleft 위험 없음
- 1개 컴포넌트는 라이선스 **Unknown** — 별도 확인 필요
- ⚠️ SBOM 내 라이선스 메타데이터 누락으로 잠재적 미확인 Copyleft 위험 존재 가능

## 2. Copyleft 위험 컴포넌트 목록

| 컴포넌트 | 버전 | 라이선스 | Copyleft 등급 | 위험도 | 조치 |
|---------|------|---------|-------------|------|------|
| log4j-api | 2.14.1 | Apache-2.0 | 없음 | 🟢 Low | 불필요 |
| log4j-core | 2.14.1 | Apache-2.0 | 없음 | 🟢 Low | 불필요 |
| vulnerable-java-app | 1.0.0 | Unknown | 미확인 | 🟡 Medium | 라이선스 확인 필요 |

## 3. Copyleft 등급 기준

| 등급 | 해당 라이선스 | 배포 시 의무 |
|------|------------|-----------|
| Strong Copyleft | GPL-2.0, GPL-3.0, AGPL-3.0 | 전체 소스코드 공개 의무 |
| Weak Copyleft | LGPL-2.1, LGPL-3.0, MPL-2.0 | 해당 컴포넌트 수정본 소스코드 공개 |
| Permissive | Apache-2.0, MIT, BSD | 저작권 표시만 유지 |
| Unknown | — | 확인 전까지 Copyleft로 보수적 처리 권고 |

## 4. 위험도 평가

### 현재 배포 방식 기준

| 배포 방식 | Copyleft 위험 |
|---------|-------------|
| 소스코드 비공개 바이너리 배포 | 🟢 위험 없음 (Apache-2.0만 사용 시) |
| SaaS / 네트워크 서비스 | 🟢 위험 없음 (AGPL 컴포넌트 없음) |
| 오픈소스 재배포 | 🟢 위험 없음 (Strong Copyleft 없음) |

> **결론:** 현재 식별된 오픈소스 컴포넌트(log4j-api, log4j-core)는 모두 Apache-2.0으로
> 어떤 배포 방식에서도 소스코드 공개 의무가 발생하지 않습니다.

## 5. 조치사항

### 🟡 Medium — Unknown 라이선스 컴포넌트 확인

- **대상:** `vulnerable-java-app@1.0.0` (내부 개발 애플리케이션)
- **위험:** 라이선스 미명시 상태에서 외부 배포 시 컴플라이언스 불명확
- **조치:** `pom.xml`에 라이선스 정보 명시 또는 내부 IP 정책 문서화
- **예상 소요시간:** 15분

### ⚪ Info — SBOM 라이선스 정보 보완

- **대상:** 전체 컴포넌트
- **위험:** 라이선스 필드 공백으로 추가 의존성 추가 시 Copyleft 누락 가능
- **조치:** SBOM 생성 도구에서 라이선스 메타데이터 활성화 후 재생성
- **예상 소요시간:** 30분

## 6. 향후 모니터링 권고

- 새 의존성 추가 시 SBOM 재생성 및 이 리포트 업데이트
- GPL/AGPL 컴포넌트 도입 시 법무팀 검토 필수
- 분기별 SBOM 라이선스 현황 점검 일정 수립

---

*이 리포트는 ISO/IEC 5230 §3.3.2(라이선스 식별) 요구사항을 충족하기 위해 생성되었습니다.*
