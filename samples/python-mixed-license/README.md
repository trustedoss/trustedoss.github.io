[🇰🇷 한국어](#한국어) | [🇺🇸 English](#english)

---

<a id="한국어"></a>

# python-mixed-license — GPL + Permissive 라이선스 혼재 시연

| 항목      | 내용                                                                     |
| --------- | ------------------------------------------------------------------------ |
| 학습 목표 | GPL과 Permissive 라이선스가 혼재할 때의 Copyleft 리스크를 식별           |
| 예상 시간 | 약 20분                                                                  |
| 난이도    | 입문                                                                     |
| 선행 조건 | Docker Desktop 실행 (없으면 docs 05 챕터의 "Docker 없이 진행" 경로 사용) |
| 관련 챕터 | 05 SBOM 생성·라이선스 분석, 03 정책(license-allowlist)                   |

## 실습 목적

이 샘플은 **GPL 라이선스와 Permissive 라이선스가 혼재**할 때 발생하는
라이선스 리스크를 시연합니다.

## 포함된 라이선스 현황

| 패키지                 | 버전   | 라이선스   | 배포 시 의무사항         |
| ---------------------- | ------ | ---------- | ------------------------ |
| PyYAML                 | 6.0.1  | MIT        | 저작권 고지              |
| requests               | 2.31.0 | Apache-2.0 | 저작권 고지, NOTICE 파일 |
| celery                 | 5.3.4  | BSD        | 저작권 고지              |
| mysql-connector-python | 8.1.0  | GPL-2.0    | **소스코드 공개 의무**   |

## 예상 실습 결과

### SBOM 생성 시

- `mysql-connector-python 8.1.0` 컴포넌트 탐지 (syft 출력의 라이선스 필드는 비어 있음)

### 라이선스 분석 시

- **GPL-2.0 라이선스 식별** 및 Copyleft 위험 항목 표시
- 소스코드 공개 의무 검토 필요 표시

## 강의 포인트

1. **GPL 컴포넌트를 포함하면** 배포 방식에 따라 전체 소스 공개 의무가 생길 수 있습니다
2. **라이선스 allowlist 정책**이 왜 필요한지 확인합니다 (policy/license-allowlist.md)
3. **도입 전 라이선스 확인**의 중요성을 확인합니다

## GPL 라이선스 리스크 상세 설명

GPL-2.0 의 "카피레프트(Copyleft)" 특성은 다음과 같습니다:

- GPL 라이선스 코드를 포함하여 배포 시, 전체 소프트웨어의 소스코드를 공개해야 할 수 있습니다
- 상업용 소프트웨어에 GPL 컴포넌트를 포함하는 것은 법적 검토가 필수입니다
- LGPL은 라이브러리 형태로 링크 시 소스공개 의무가 완화됩니다

## 실제 조치 방법

GPL 컴포넌트를 동등한 기능의 Permissive 라이선스 패키지로 교체 검토:

| 현재 (GPL)                       | 대안 (Permissive) | 라이선스 |
| -------------------------------- | ----------------- | -------- |
| mysql-connector-python (GPL-2.0) | PyMySQL           | MIT      |
| mysql-connector-python (GPL-2.0) | aiomysql          | MIT      |

또는 법무 검토 후 소스코드 공개 준비.

## SBOM 생성 명령어

```bash
# 출력 디렉토리 생성 (fresh clone 직후에는 없음)
mkdir -p ../../output/sbom

docker run --rm -v "$(pwd)":/project \
  anchore/syft:latest \
  /project --output cyclonedx-json \
  > ../../output/sbom/python-mixed.cdx.json
```

스캔 단계에서 `sbom format not recognized` 가 나오면 grype 가 낡은 것입니다.
`anchore/syft:latest` 는 CycloneDX 1.7 을 내는데 grype 는 0.118 이상에서만 읽습니다.
`grype version` 으로 확인하고 올리세요.

## 프로젝트 구조

```
python-mixed-license/
├── requirements.txt    # 의존성 목록 (GPL 포함)
├── main.py             # 메인 스크립트
└── README.md           # 이 파일
```

---

<a id="english"></a>

# python-mixed-license — GPL and permissive licenses side by side

| Item         | Detail                                                                          |
| ------------ | ------------------------------------------------------------------------------- |
| Goal         | Identify the copyleft risk when GPL and permissive licenses are mixed           |
| Time         | About 20 minutes                                                                |
| Level        | Beginner                                                                        |
| Prerequisite | Docker Desktop running (or use the "working without Docker" path in chapter 05) |
| Related      | 05 SBOM generation and license analysis, 03 policy (license-allowlist)          |

## What this is for

This sample demonstrates the license risk that appears when **GPL and permissive
licenses sit in the same project**.

## The licenses in play

| Package                | Version | License    | Obligation when distributing     |
| ---------------------- | ------- | ---------- | -------------------------------- |
| PyYAML                 | 6.0.1   | MIT        | Copyright notice                 |
| requests               | 2.31.0  | Apache-2.0 | Copyright notice, NOTICE file    |
| celery                 | 5.3.4   | BSD        | Copyright notice                 |
| mysql-connector-python | 8.1.0   | GPL-2.0    | **Obligation to publish source** |

## What you should see

### When generating the SBOM

- The `mysql-connector-python 8.1.0` component is detected (the license field in the syft output is empty)

### When analysing licenses

- **GPL-2.0 is identified** and flagged as a copyleft risk
- The report says the source publication obligation needs review

## Points worth making

1. **Including a GPL component** can create an obligation to publish your full source, depending on how you distribute
2. It shows why a **license allowlist policy** is needed (policy/license-allowlist.md)
3. It shows why **checking the license before adoption** matters

## The GPL risk in more detail

The copyleft nature of GPL-2.0 works like this:

- If you distribute software that includes GPL code, you may have to publish the source of the whole thing
- Including a GPL component in commercial software requires legal review
- LGPL relaxes the obligation when the library is linked rather than modified

## How to fix it for real

Consider replacing the GPL component with a permissive one of equivalent function:

| Current (GPL)                    | Alternative (permissive) | License |
| -------------------------------- | ------------------------ | ------- |
| mysql-connector-python (GPL-2.0) | PyMySQL                  | MIT     |
| mysql-connector-python (GPL-2.0) | aiomysql                 | MIT     |

Or get legal review and prepare to publish the source.

## SBOM generation commands

```bash
# Create the output directory (it does not exist in a fresh clone)
mkdir -p ../../output/sbom

docker run --rm -v "$(pwd)":/project \
  anchore/syft:latest \
  /project --output cyclonedx-json \
  > ../../output/sbom/python-mixed.cdx.json
```

If the scan step reports `sbom format not recognized`, grype is too old.
`anchore/syft:latest` emits CycloneDX 1.7, which grype only reads from 0.118 onwards.
Check with `grype version` and upgrade.

## Project layout

```
python-mixed-license/
├── requirements.txt    # the dependency list (includes GPL)
├── main.py             # the main script
└── README.md           # this file
```
