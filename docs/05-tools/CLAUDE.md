# 챕터 05 — 도구 실습 (공통)

## 현재 위치: 5단계 - 도구 실습 (5/7단계)

## 이 챕터의 목표

무료 오픈소스 도구만을 사용하여 SBOM을 생성하고, 라이선스를 분석하며,
취약점을 스캔하는 실전 실습을 진행한다.

이 단계에서 모든 도구는 Docker 기반으로 실행되므로 로컬 환경에 영향을 주지 않는다.

## 하위 3개 챕터 진행 순서

아래 순서로 진행해야 한다. 각 단계의 산출물이 다음 단계의 입력값이 된다.

```
sbom-generation → sbom-management → vulnerability
```

| 순서 | 챕터 | 주요 산출물 |
|------|------|-----------|
| 5-1 | docs/05-tools/sbom-generation/ | [project].cdx.json |
| 5-2 | docs/05-tools/sbom-management/ | sbom-management-plan.md |
| 5-3 | docs/05-tools/vulnerability/ | cve-report.md |

## 공통 전제 조건

- Docker Desktop이 실행 중인 상태 (`docker ps` 오류 없이 실행되어야 함)
- `output/process/` 산출물 완료 (챕터 04)

## 도구 목록

| 도구 | 역할 | 실행 방식 |
|------|------|---------|
| syft | SBOM 생성 (Anchore) | Docker |
| cdxgen | CycloneDX SBOM 생성 | Docker |
| Dependency Track | 취약점 스캔 및 추적 | Docker Compose |
| OSV API | 취약점 조회 (대안) | HTTP API (Docker 불필요) |

## Docker 실행 확인

```bash
docker ps
# 오류가 없으면 Docker Desktop이 정상 실행 중
```

## 셀프스터디 경로

:::info 셀프스터디 모드 (약 3~4시간, 3개 챕터 합산)
각 챕터마다 실제 프로젝트 또는 samples/ 를 대상으로 실습합니다.
:::

1. `docs/05-tools/sbom-generation/` 진행 (1시간 30분)
2. `docs/05-tools/sbom-management/` 진행 (45분)
3. `docs/05-tools/vulnerability/` 진행 (45분)

## 워크숍 경로

:::tip 워크숍 모드 (M3~M5 - 총 3시간)
Docker Desktop을 강의 전에 미리 시작해두세요. 이미지 풀링에 시간이 필요합니다.
:::

각 모듈은 독립적으로 진행 가능하지만, sbom-generation 이 먼저여야 한다.

## 자주 발생하는 문제

**Q: Docker Desktop이 느려요.**
A: 최소 8GB RAM 권장. 다른 무거운 앱을 종료하고 진행.

**Q: 실습할 프로젝트가 없어요.**
A: `samples/` 디렉토리에 Java, Python, Node.js 샘플 프로젝트가 있다.

## 다음 단계

`docs/05-tools/sbom-generation/` 으로 이동하여 시작.
