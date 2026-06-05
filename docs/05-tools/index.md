---
description: '무료 오픈소스 도구로 SBOM을 만들고 취약점에 대응합니다. syft, grype, OSV 실습 통합 인덱스.'
작성일: 2026-06-05
버전: 1.0
충족 체크리스트:
  - 'ISO/IEC 5230: []'
  - 'ISO/IEC 18974: []'
셀프스터디 소요시간: 5분
sidebar_position: 0
sidebar_label: 도구 개요
---

# 도구: SBOM과 취약점 관리

<Prerequisite items={[{label: '4. 오픈소스 프로세스', href: '/docs/process'}]}>+ Docker 실행 환경</Prerequisite>

이 챕터는 제품에 포함된 오픈소스를 자동으로 파악하고(SBOM), 관리하고, 취약점을 찾아 대응하는 도구를 다룹니다. 아래 세 단계 흐름으로 진행합니다.

## 진행 흐름

1. **SBOM 생성** — 제품에 어떤 오픈소스가 들어 있는지 명세서(SBOM)를 만듭니다. 도구는 syft와 cdxgen입니다. [SBOM 생성](./sbom-generation/index.md)으로 이동하세요.
2. **SBOM 관리** — 생성한 SBOM을 갱신·보관하고 공급망과 공유합니다. [SBOM 관리](./sbom-management/index.md)로 이동하세요.
3. **취약점 분석과 대응** — SBOM을 기반으로 알려진 취약점(CVE)을 찾아 대응합니다. 도구는 grype와 OSV입니다. [취약점 관리](./vulnerability/index.md)로 이동하세요.

## 바로 체험 (무설치·무API키)

설치 없이 브라우저에서 SBOM 분석 결과를 먼저 확인해 보세요.

- [SBOM 분석기 샘플 체험](pathname:///tools/sbom-sample-demo.html)

## AI 에이전트로 자동 생성

각 단계의 산출물은 에이전트로 자동 생성할 수 있습니다. 전체 매핑은 [AI 에이전트로 산출물 만들기](../00-overview/agents.md)를 참고하세요.

- SBOM 생성: `05-sbom-guide`, `05-sbom-analyst`
- SBOM 관리: `05-sbom-management`
- 취약점 분석: `05-vulnerability-analyst`

## 자동화로 확장

여기서 익힌 SBOM 생성과 취약점 스캔은 CI 파이프라인에 넣어 상시 자동화할 수 있습니다. [DevSecOps](/devsecops/intro) 가이드에서 복사해 쓸 수 있는 워크플로를 제공합니다.
