---
작성일: 2026-03-20
버전: 1.0
충족 체크리스트:
  - 'ISO/IEC 5230: [3.3.1, 3.3.2, 3.4.1]'
  - 'ISO/IEC 18974: [4.3.1]'
셀프스터디 소요시간: 1.5시간
---

# SBOM 생성: syft와 cdxgen으로 소프트웨어 구성 명세 만들기

## 1. 이 챕터에서 하는 일

이 챕터에서는 syft와 cdxgen을 사용해 프로젝트의 CycloneDX 형식 SBOM(Software Bill of Materials)을 생성합니다. 두 도구 모두 Docker로 실행하므로 별도 설치가 필요 없으며, 명령어 몇 줄로 프로젝트의 전체 의존성 목록을 JSON 파일로 만들 수 있습니다.

생성된 SBOM은 이후 라이선스 분석(05-sbom-analyst)과 취약점 스캔(05-vulnerability-analyst)의 기반이 됩니다. SBOM이 정확할수록 컴플라이언스 리스크와 보안 취약점을 빠짐없이 파악할 수 있습니다.

---

## 2. 배경 지식

### SBOM이란?

SBOM(Software Bill of Materials)은 소프트웨어에 포함된 모든 구성 요소의 목록입니다. 식품 영양성분표처럼, 소프트웨어에 어떤 오픈소스가 어떤 버전으로 들어있는지 명시합니다. ISO/IEC 5230과 18974 모두 SBOM 생성을 핵심 요구사항으로 규정합니다 (G3B.1).

SBOM이 중요한 이유:

- 어떤 오픈소스 라이선스가 포함되어 있는지 파악 (컴플라이언스)
- 취약한 버전의 라이브러리가 있는지 확인 (보안)
- 제품 배포 시 고객 또는 규제 기관에 소프트웨어 구성 정보 제공

### 사용 도구 소개

SBOM 생성에는 두 가지 접근 방식이 있습니다. **Dependency 분석**은 패키지 매니저 파일(pom.xml, package-lock.json 등)을 기반으로 선언된 의존성을 파악하고, **소스 코드 스캔**은 코드 내에 직접 내장된 오픈소스를 파일 레벨에서 탐지합니다. 두 방식을 병행하면 패키지 선언 없이 복사·삽입된 코드 조각까지 포함한 더 완전한 SBOM을 만들 수 있습니다.

**Dependency 분석 도구** (이 챕터에서 실습)

| 도구   | 제작사    | 특징                                           | 적합한 상황                           |
| ------ | --------- | ---------------------------------------------- | ------------------------------------- |
| syft   | Anchore   | 빠르고 가볍다, 단일 바이너리, 다양한 언어 지원 | Python, Node.js, Go                   |
| cdxgen | CycloneDX | CycloneDX 전용, 언어별 정밀 분석               | Java(Maven/Gradle), 정밀 분석 필요 시 |

두 도구 모두 CycloneDX JSON 형식으로 출력할 수 있으며, 이 챕터에서는 CycloneDX를 표준 포맷으로 사용합니다.

**소스 코드 스캔 도구** (선택 사항)

| 도구    | 운영주체 | 특징                                                            | 적합한 상황                                    |
| ------- | -------- | --------------------------------------------------------------- | ---------------------------------------------- |
| SCANOSS | SCANOSS  | 파일 단위 스니펫 스캔, 클라우드+온프레미스, API 통합, SBOM 생성 | 소스 코드 직접 임베딩 탐지, 정밀 라이선스 식별 |

[SCANOSS](https://www.scanoss.com/)는 패키지 선언 없이 직접 복사·삽입된 오픈소스 코드 조각을 파일 레벨에서 탐지하는 데 강점이 있습니다. syft/cdxgen과 역할이 보완적이므로, 소스 레벨 정밀도가 필요한 경우 병행 사용을 권장합니다.

> FOSSLight, SW360, FOSSology 등 SCA·컴플라이언스 도구의 도입 및 활용 가이드는 [KWG 오픈소스 가이드 — 도구](https://openchain-project.github.io/OpenChain-KWG/guide/opensource_for_enterprise/4-tool/)를 참조하세요.

실제 Docker 실행 명령어, GitHub Actions CI/CD 설정, 샘플 프로젝트 실습은 [Docker·CI/CD 실행 가이드](./docker-cicd.md) 페이지를 참조합니다.

### CycloneDX JSON 형식 주요 필드

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "metadata": {
    "component": {
      "name": "my-app",
      "version": "1.0.0",
      "type": "application"
    }
  },
  "components": [
    {
      "name": "log4j-core",
      "version": "2.14.1",
      "purl": "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1",
      "licenses": [{"license": {"id": "Apache-2.0"}}]
    }
  ]
}
```

주요 필드 설명:

- `bomFormat`, `specVersion`: CycloneDX 포맷 식별자
- `metadata.component`: 분석 대상 소프트웨어 정보
- `components[]`: 의존성 목록 (라이선스, PURL 포함)
- `vulnerabilities[]`: 취약점 정보 (있을 경우)

---

## 3. 셀프 스터디

:::info 셀프스터디 모드 (약 1시간 30분)
처음 실행 시 Docker 이미지 풀링으로 10-15분 추가 소요될 수 있습니다.
:::

단계별 실습:

**단계 1** — Docker Desktop 실행 확인

```bash
docker ps
```

오류 없이 실행되면 Docker가 준비된 것입니다.

**단계 2** — 분석할 프로젝트 선택

본인의 프로젝트를 사용할 수도 있고, 샘플을 사용할 수도 있습니다.

처음이라면 아래 샘플 중 하나를 선택한다:

| 샘플 경로                       | 언어          | 특징                           | 학습 포인트                 |
| ------------------------------- | ------------- | ------------------------------ | --------------------------- |
| `samples/java-vulnerable/`      | Java (Maven)  | Log4Shell(CVE-2021-44228) 포함 | Critical 취약점 탐지 실습   |
| `samples/python-mixed-license/` | Python (pip)  | GPL + MIT 혼용                 | Copyleft 라이선스 충돌 실습 |
| `samples/nodejs-unlicensed/`    | Node.js (npm) | 라이선스 미표기 패키지         | 라이선스 미식별 처리 실습   |

> **권장**: `samples/java-vulnerable/` — Log4Shell 취약점을 직접 탐지하며 SBOM의 가치를 체감할 수 있습니다.

**단계 3** — 출력 폴더 생성

```bash
mkdir -p output/sbom
```

**단계 4** — sbom-guide agent 실행

:::tip 실행 전 확인
현재 Claude 세션을 먼저 종료(`/exit` 또는 `Ctrl+C`)한 뒤, 새 터미널에서 아래 명령을 실행하세요.
:::

```bash
cd agents/05-sbom-guide
claude
```

agent가 프로젝트 정보를 묻는 3가지 질문을 한다:

- 프로젝트 경로 (예: `samples/java-vulnerable`)
- 주 언어 (예: `Java`)
- 패키지 매니저 (예: `Maven`)

**단계 5** — 생성된 스크립트 실행

agent가 `output/sbom/sbom-commands.sh`를 생성하면 실행한다:

```bash
bash output/sbom/sbom-commands.sh
```

**단계 6** — SBOM 파일 존재 확인

```bash
ls -lh output/sbom/*.cdx.json
```

파일이 존재하고 크기가 0보다 크면 정상입니다. 파일을 열어 `components` 배열이 비어있지 않은지 확인합니다.

**단계 7** — 라이선스 분석 실행

:::tip 실행 전 확인
현재 Claude 세션을 먼저 종료(`/exit` 또는 `Ctrl+C`)한 뒤, 새 터미널에서 아래 명령을 실행하세요.
:::

```bash
cd agents/05-sbom-analyst
claude
```

**단계 8** — 분석 결과 확인

```bash
ls output/sbom/license-report.md output/sbom/copyleft-risk.md
```

**막혔을 때:**

`output/sbom/sbom.cdx.json`이 비어있으면 lock 파일 존재 여부를 먼저 확인합니다 (`package-lock.json`, `requirements.txt`, `pom.xml` 등). lock 파일이 없으면 cdxgen으로 전환하여 재시도합니다.

```bash
docker run --rm \
  -v $(pwd)/samples/java-vulnerable:/app \
  -w /app \
  ghcr.io/cyclonedx/cdxgen:latest \
  -r /app \
  -o /app/output/sbom/java-vulnerable-cdxgen.cdx.json
```

**각 단계 예상 결과:**

| 단계 완료 후        | 예상 결과                                                              |
| ------------------- | ---------------------------------------------------------------------- |
| 4번 (sbom-guide)    | `output/sbom/sbom-commands.sh` 생성됨                                  |
| 5번 (스크립트 실행) | `output/sbom/sbom.cdx.json` 생성됨 (`components` 항목 있어야 정상)     |
| 7번 (sbom-analyst)  | `output/sbom/license-report.md`, `output/sbom/copyleft-risk.md` 생성됨 |

:::info 충족되는 표준 요구사항
이 실습을 완료하면 아래 요구사항이 충족됩니다.

**ISO/IEC 5230**

| 항목 ID | 요구사항                 | 자체인증 체크리스트                                                                                   |
| ------- | ------------------------ | ----------------------------------------------------------------------------------------------------- |
| 3.3.1   | SBOM 생성 및 관리        | Do you have a process for creating and managing a bill of materials for each supply software release? |
| 3.3.2   | 라이선스 식별 및 분류    | Do you have a process for identifying the licenses applicable to supply software?                     |
| 3.4.1   | 컴플라이언스 산출물 준비 | Do you have a process for creating the necessary compliance artifacts?                                |

**ISO/IEC 18974**

| 항목 ID | 요구사항             | 자체인증 체크리스트                                                            |
| ------- | -------------------- | ------------------------------------------------------------------------------ |
| 4.3.1   | 공급 소프트웨어 SBOM | Do you have a process for creating and maintaining a SBOM for supply software? |

:::

---

## 4. 완료 확인 체크리스트

아래 항목을 모두 확인한 후 다음 단계로 넘어간다.

- [ ] `output/sbom/[project].cdx.json` 생성됨
- [ ] SBOM 파일에 `components` 배열이 비어있지 않음
- [ ] `output/sbom/sbom-commands.sh` 생성됨
- [ ] `output/sbom/license-report.md` 생성됨
- [ ] `output/sbom/copyleft-risk.md` 생성됨

**java-vulnerable 샘플 실습 시 예상 결과:**

- log4j-core 2.14.1 컴포넌트 탐지
- Apache-2.0 라이선스 식별
- CVE-2021-44228 (Log4Shell) 취약점 플래그 예상

> 이 단계는 ISO/IEC 5230 3.3.1, 3.3.2, 3.4.1 및 ISO/IEC 18974 4.3.1 요구사항을 충족합니다.

> 📋 **산출물 예시**: [SBOM 산출물 Best Practice](/reference/samples/sbom)에서 생성된 파일의 실제 형식을 확인할 수 있습니다.

---

## 5. 다음 단계

SBOM 생성과 라이선스 분석이 완료되면, SBOM 관리 체계를 수립하는 단계로 넘어간다.

:::tip 실행 전 확인
현재 Claude 세션을 먼저 종료(`/exit` 또는 `Ctrl+C`)한 뒤, 새 터미널에서 아래 명령을 실행하세요.
:::

```bash
cd agents/05-sbom-management
claude
```

또는 [SBOM 관리: 만들고 끝이 아니라 관리가 시작이다](../sbom-management/index.md)로 이동하여 가이드를 확인합니다.

취약점 분석을 먼저 진행하려면:

:::tip 실행 전 확인
현재 Claude 세션을 먼저 종료(`/exit` 또는 `Ctrl+C`)한 뒤, 새 터미널에서 아래 명령을 실행하세요.
:::

```bash
cd agents/05-vulnerability-analyst
claude
```

완료 후 `output/progress.md`를 업데이트하여 진행 상황을 기록합니다.
