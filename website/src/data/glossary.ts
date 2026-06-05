/**
 * 용어 호버 툴팁용 정의 맵 — 용어집(reference/glossary)의 핵심 항목과 동기화.
 * <Term k="sbom">SBOM</Term> 형태로 본문에서 사용한다.
 */

export const GLOSSARY: Record<string, string> = {
  sbom: '소프트웨어 부품 명세서 — 제품에 들어간 모든 오픈소스 구성요소와 버전·라이선스 목록.',
  spdx: 'SBOM·라이선스 표준 포맷 (Linux Foundation).',
  cyclonedx: 'SBOM 표준 포맷의 하나 (OWASP).',
  copyleft:
    '카피레프트 — 파생물도 같은 라이선스로 공개하도록 요구하는 라이선스 유형 (GPL, AGPL 등).',
  permissive:
    '허용적 라이선스 — 고지 위주로 제약이 적은 유형 (MIT, Apache-2.0, BSD).',
  cve: '공개 취약점 식별번호 — 알려진 취약점에 부여되는 고유 번호.',
  cvss: '취약점 심각도 점수 — 0~10으로 위험도를 표시.',
  vex: '취약점 영향 알림 — 해당 취약점이 우리 제품에 실제 영향을 주는지 표기.',
  sca: '소프트웨어 구성 분석 — 오픈소스 구성요소의 취약점·라이선스를 점검.',
  openchain: '오픈소스 컴플라이언스 국제표준 프로젝트 (ISO/IEC 5230·18974).',
  'self-certification':
    '외부 심사 없이 OpenChain 요구사항 충족을 스스로 선언하는 방식.',
};
