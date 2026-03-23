# 무료 교육 리소스 목록
<!-- 5230 §3.1.2, §3.1.3, 18974 §4.1.2, §4.1.3 -->

**회사명**: 테크유니콘
**버전**: 1.0
**작성일**: 2026-03-23

---

## 권장 활용 방식

- 온라인 자율 학습 모듈(A·B·C 과정)에 아래 무료 리소스를 연계 활용
- 수료증 발급 과정은 OpenChain 인증 증빙으로 직접 제출 가능

---

## 1. OpenChain 공식 교육 자료

| 리소스 | 대상 | 형태 | 수료증 | 링크 |
|--------|------|------|--------|------|
| OpenChain e-Learning | 전 직군 | 온라인 자율 | 없음 | https://www.openchainproject.org/resources |
| OpenChain Curriculum | 개발자·관리자 | 슬라이드/문서 | 없음 | https://github.com/OpenChain-Project/curriculum |
| OpenChain Reference Materials | 관리자 | 문서 | 없음 | https://www.openchainproject.org/resources |

**커리큘럼 연계**: 개발자 M1·M2, 관리자 M1·M2 보조 자료

---

## 2. Linux Foundation 강좌

| 과정명 | 과정 코드 | 대상 | 시간 | 수료증 | 링크 |
|--------|---------|------|------|--------|------|
| Open Source Compliance in the Enterprise | LFC193 | 개발자·관리자 | ~3h | 있음 (무료) | https://training.linuxfoundation.org/training/open-source-compliance-in-the-enterprise/ |
| Open Source Licensing Basics for Software Developers | LFD106x | 개발자 | ~3h | 있음 (무료) | https://training.linuxfoundation.org/training/open-source-licensing-basics-for-software-developers/ |
| Secure Software Development Fundamentals | LFD121 | 개발자 | ~12h | 있음 (무료) | https://training.linuxfoundation.org/training/developing-secure-software-lfd121/ |
| Kubernetes and Cloud Native Security Associate | — | 운영 | — | 유료 | — |

**커리큘럼 연계**:
- LFC193 → 개발자 M2, 관리자 M1·M2 핵심 자료
- LFD106x → 개발자 M1 핵심 자료
- LFD121 → 개발자 M4 보조 자료

> **수료증 활용**: LFC193·LFD106x 수료증은 OpenChain 자체 인증 제출 증빙으로 사용 가능

---

## 3. SPDX 교육

| 리소스 | 대상 | 형태 | 링크 |
|--------|------|------|------|
| SPDX Specification 공식 문서 | 개발자 | 문서 | https://spdx.github.io/spdx-spec/ |
| SPDX 입문 가이드 | 개발자 | 문서 | https://spdx.dev/learn/ |
| SPDX Tools 사용법 | 개발자 | 문서·도구 | https://tools.spdx.org/ |

**커리큘럼 연계**: 개발자 M3 (SBOM 생성 실습) 참고 자료

---

## 4. 오픈소스 취약점 관련 리소스

| 리소스 | 대상 | 링크 |
|--------|------|------|
| NVD (National Vulnerability Database) | 개발자·관리자 | https://nvd.nist.gov/ |
| OSV (Open Source Vulnerabilities) | 개발자 | https://osv.dev/ |
| CISA Known Exploited Vulnerabilities | 관리자 | https://www.cisa.gov/known-exploited-vulnerabilities-catalog |

**커리큘럼 연계**: 개발자 M4, 관리자 M4

---

## 5. 도구 및 실습 자료

| 도구/자료 | 용도 | 링크 |
|----------|------|------|
| Syft (Anchore) | SBOM 생성 실습 | https://github.com/anchore/syft |
| Grype (Anchore) | 취약점 스캔 실습 | https://github.com/anchore/grype |
| CycloneDX 공식 사이트 | SBOM 표준 이해 | https://cyclonedx.org/ |
| FOSSA 블로그 | 라이선스 컴플라이언스 사례 | https://fossa.com/blog/ |
| REUSE 스펙 | 소스코드 라이선스 표기법 | https://reuse.software/ |

**커리큘럼 연계**: 개발자 M3·M4 실습 도구

---

## 6. ISO/IEC 5230 · 18974 참고 자료

| 리소스 | 설명 | 링크 |
|--------|------|------|
| OpenChain ISO/IEC 5230 사양 | 라이선스 컴플라이언스 표준 | https://www.openchainproject.org/license-compliance |
| OpenChain ISO/IEC 18974 사양 | 보안 보증 표준 | https://www.openchainproject.org/security-assurance |
| OpenChain 자체 인증 체크리스트 | 인증 준비 | https://www.openchainproject.org/conformance |

**커리큘럼 연계**: 관리자 M3 핵심 자료

---

## 리소스 선택 가이드

| 직군 | 최우선 리소스 | 수료증 활용 |
|------|------------|-----------|
| 개발자 | LFD106x → LFC193 → Syft 실습 | LFD106x + LFC193 수료증 제출 |
| 관리자 | LFC193 → OpenChain Curriculum → ISO 5230/18974 사양 | LFC193 수료증 제출 |
| 운영 | OpenChain e-Learning | 이수 기록으로 대체 |
