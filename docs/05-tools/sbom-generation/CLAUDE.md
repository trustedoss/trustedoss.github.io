# 챕터 05-1 — SBOM 생성

## 현재 위치: 5-1단계 - SBOM 생성 (5.1/7단계)

## 이 챕터의 목표

syft 또는 cdxgen 도구를 사용하여 실제 프로젝트의 SBOM을 CycloneDX JSON 형식으로 생성한다.
생성된 SBOM은 이후 라이선스 분석과 취약점 스캔의 기반이 된다.

## 충족되는 체크리스트 항목

| 항목ID | 요구사항 | ISO/IEC 5230 | ISO/IEC 18974 |
|--------|---------|-------------|--------------|
| G3B.1 | SBOM 생성 (CycloneDX/SPDX) | 3.3.1 | 3.3.1 |
| G3L.1 | 라이선스 식별 및 분류 | 3.3.2 | — |
| G3L.3 | 컴플라이언스 산출물 생성 | 3.4.1 | — |

> 이 단계는 ISO/IEC 5230 3.3.1, 3.3.2, 3.4.1 및 ISO/IEC 18974 3.3.1 요구사항을 충족합니다.

## 전제 조건

- Docker Desktop 실행 중
- `output/process/` 산출물 완료 (챕터 04)
- 분석할 프로젝트 경로 (없으면 `samples/` 중 선택)

## 언어별 분기 안내

| 언어 | 패키지 매니저 | 권장 도구 | samples/ 프로젝트 |
|------|------------|---------|----------------|
| Java | Maven/Gradle | cdxgen | samples/java-app |
| Python | pip/poetry | syft | samples/python-app |
| Node.js | npm/yarn | syft | samples/node-app |
| Go | go mod | syft | — |

## samples/ 프로젝트 활용

실습할 프로젝트가 없다면:
```bash
ls samples/
# java-app, python-app, node-app 중 선택
```

## agent 실행 안내

```bash
cd agents/05-sbom-guide
claude
```

agent가 아래 질문을 순서대로 한다:
1. 분석할 프로젝트 경로
2. 주요 개발 언어
3. 패키지 매니저

agent가 언어에 맞는 syft/cdxgen 명령어와 실행 스크립트를 생성한다.

이후 라이선스 분석:
```bash
cd agents/05-sbom-analyst
claude
```

## 완료 기준

- [ ] `output/sbom/[project-name].cdx.json` 생성됨
- [ ] `output/sbom/sbom-commands.sh` 생성됨
- [ ] `output/sbom/license-report.md` 생성됨
- [ ] `output/sbom/copyleft-risk.md` 생성됨

## 셀프스터디 경로

:::info 셀프스터디 모드 (약 1시간 30분)
처음 실행 시 Docker 이미지 풀링으로 10-15분 추가 소요될 수 있습니다.
:::

1. `docs/05-tools/sbom-generation/index.md` 읽기
2. `cd agents/05-sbom-guide && claude` 실행
3. SBOM 생성 명령어 실행 및 확인
4. `cd agents/05-sbom-analyst && claude` 실행
5. `output/sbom/` 산출물 확인

## 워크숍 경로

:::tip 워크숍 모드 (M3 - 1시간 30분)
Docker 이미지를 강의 전에 미리 pull 해두세요.
docker pull anchore/syft
:::

1. (15분) SBOM 개념 및 도구 소개
2. (45분) syft/cdxgen 실행, SBOM 생성
3. (30분) 라이선스 분석 리포트 생성

## 자주 발생하는 문제

**Q: syft 실행 시 "no packages discovered" 가 나와요.**
A: 프로젝트 디렉토리에 lock 파일이 있는지 확인. (package-lock.json, requirements.txt 등)

**Q: CycloneDX JSON 이 너무 큰데 정상인가요?**
A: 의존성이 많은 프로젝트는 수MB가 될 수 있다. 정상이다.

**Q: cdxgen과 syft 중 어느 것을 써야 하나요?**
A: Java/Maven 프로젝트는 cdxgen, 나머지는 syft가 더 안정적이다.

## 다음 단계

완료 후:
```bash
cd agents/05-sbom-management
claude
```
또는 `docs/05-tools/sbom-management/` 로 이동.
