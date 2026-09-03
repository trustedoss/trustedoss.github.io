[🇰🇷 한국어](#한국어) | [🇺🇸 English](#english)

---

<a id="한국어"></a>

# nodejs-unlicensed — 라이선스 미명시 패키지 리스크 시연

| 항목      | 내용                                                    |
| --------- | ------------------------------------------------------- |
| 학습 목표 | 라이선스 미명시(NOASSERTION) 패키지의 법적 리스크 처리  |
| 예상 시간 | 약 25분 (npm install 포함)                              |
| 난이도    | 중급                                                    |
| 선행 조건 | Docker Desktop 실행, Node.js·npm 설치(npm install 필요) |
| 관련 챕터 | 05 SBOM 생성·라이선스 분석, 03 정책(license-allowlist)  |

## 실습 목적

이 샘플은 **라이선스가 명시되지 않은 패키지를 포함**할 때의
법적 리스크를 시연합니다.

라이선스 미명시 패키지는 `vendor/legacy-parser`라는 저장소 내 로컬 패키지로
재현합니다. 실제 npm 레지스트리 패키지는 배포자가 나중에 라이선스를 추가하면
실습 결과가 달라질 수 있어, license 필드가 없는 가짜 패키지를 저장소에 두어
언제 실행해도 같은 결과가 나오게 했습니다.

## 포함된 패키지 현황

| 패키지        | 버전                        | 라이선스 | 상태                        |
| ------------- | --------------------------- | -------- | --------------------------- |
| express       | ^4.18.2                     | MIT      | 명확 — 상업적 사용 가능     |
| lodash        | ^4.17.21                    | MIT      | 명확 — 상업적 사용 가능     |
| legacy-parser | file:./vendor/legacy-parser | (없음)   | **위험 — 사용 권한 불명확** |

> **참고:** 이 프로젝트(package.json) 자체에도 license 필드가 없습니다.
> SBOM 생성 시 NOASSERTION으로 표시됩니다.

## 예상 실습 결과

### SBOM 생성 시

- `legacy-parser` 패키지의 라이선스 정보: 비어 있음(CycloneDX) 또는 `NOASSERTION`(SPDX)
- 프로젝트 자체 라이선스: `NOASSERTION`

### 라이선스 분석 시

- **라이선스 확인 필요 항목 표시**
- 상업적 사용 위험 표시

## 강의 포인트

1. **라이선스 미명시 = 기본적으로 All Rights Reserved**
   저작권법상 명시적 허가 없이는 사용 권한이 없습니다
2. **npm 생태계의 라이선스 불확실성 문제**
   package.json 의 license 필드가 없거나 신뢰하기 어려운 경우가 실제로 존재합니다
3. **라이선스 확인 없이 사용하면 법적 리스크**
   특히 상업적 배포 시 위험합니다

## 실제 조치 방법

1. **패키지의 출처(저장소, 배포 페이지)에서 라이선스 직접 확인**

   ```bash
   # npm 레지스트리 패키지라면 라이선스 정보 확인
   npm view <패키지명> license

   # 이 샘플의 로컬 패키지라면 package.json을 직접 확인
   cat vendor/legacy-parser/package.json
   ```

2. **확인 불가 시 해당 패키지 사용 금지**
   같은 기능을 하는 라이선스가 명확한 대안 패키지를 검토하고,
   사내에서 만든 출처 불명 코드라면 작성자를 찾아 라이선스를 명시합니다.

3. **license-allowlist.md 에 검토 결과 기록**
   ```
   output/policy/license-allowlist.md
   ```

## SBOM 생성 명령어

```bash
# npm install 먼저 실행
npm install

# 출력 디렉토리 생성 (fresh clone 직후에는 없음)
mkdir -p ../../output/sbom

docker run --rm -v "$(pwd)":/project \
  anchore/syft:latest \
  /project --output cyclonedx-json \
  > ../../output/sbom/nodejs-unlicensed.cdx.json
```

스캔 단계에서 `sbom format not recognized` 가 나오면 grype 가 낡은 것입니다.
`anchore/syft:latest` 는 CycloneDX 1.7 을 내는데 grype 는 0.118 이상에서만 읽습니다.
`grype version` 으로 확인하고 올리세요.

## 프로젝트 구조

```
nodejs-unlicensed/
├── package.json              # 의존성 목록 (license 필드 없음)
├── index.js                  # 메인 스크립트
├── vendor/legacy-parser/     # 라이선스 미명시 로컬 패키지 (실습용)
└── README.md                 # 이 파일
```

---

<a id="english"></a>

# nodejs-unlicensed — the risk of a package with no declared license

| Item         | Detail                                                                    |
| ------------ | ------------------------------------------------------------------------- |
| Goal         | Handle the legal risk of a package with no declared license (NOASSERTION) |
| Time         | About 25 minutes (including the dependency install)                       |
| Level        | Intermediate                                                              |
| Prerequisite | Docker Desktop running, Node.js and npm installed                         |
| Related      | 05 SBOM generation and license analysis, 03 policy (license-allowlist)    |

## What this is for

This sample demonstrates the legal risk of **including a package that declares no license**.

The unlicensed package is reproduced as a local package in the repository,
`vendor/legacy-parser`. A real npm registry package could have a license added later by
its publisher, which would change what you see, so a fake package with no license field
lives in the repository to keep the exercise reproducible.

## The packages in play

| Package       | Version                     | License | Status                              |
| ------------- | --------------------------- | ------- | ----------------------------------- |
| express       | ^4.18.2                     | MIT     | Clear, commercial use is fine       |
| lodash        | ^4.17.21                    | MIT     | Clear, commercial use is fine       |
| legacy-parser | file:./vendor/legacy-parser | (none)  | **Risky, no clear right to use it** |

**Note:** this project's own package.json has no license field either.
It shows up as NOASSERTION when you generate the SBOM.

## What you should see

### When generating the SBOM

- License information for `legacy-parser`: empty (CycloneDX) or `NOASSERTION` (SPDX)
- The project's own license: `NOASSERTION`

### When analysing licenses

- **The item is flagged as needing a license check**
- Commercial use is flagged as risky

## Points worth making

1. **No declared license means all rights reserved by default.**
   Under copyright law you have no right to use it without explicit permission
2. **License uncertainty is real in the npm ecosystem.**
   A missing or untrustworthy license field in package.json does happen
3. **Using it without checking is a legal risk**, especially when you distribute commercially

## How to handle it for real

1. **Check the license at the source (repository, distribution page)**

   ```bash
   # For a package on the npm registry
   npm view <package-name> license

   # For the local package in this sample, read package.json directly
   cat vendor/legacy-parser/package.json
   ```

2. **If you cannot confirm it, do not use the package.**
   Look for an alternative with a clear license, and if the code came from inside your
   company with no clear provenance, find the author and get the license stated.

3. **Record the outcome in license-allowlist.md**

   ```
   output/policy/license-allowlist.md
   ```

## SBOM generation commands

```bash
# Install the dependencies first, the same command as in the Korean section above
npm ci

# Create the output directory (it does not exist in a fresh clone)
mkdir -p ../../output/sbom

docker run --rm -v "$(pwd)":/project \
  anchore/syft:latest \
  /project --output cyclonedx-json \
  > ../../output/sbom/nodejs-unlicensed.cdx.json
```

If the scan step reports `sbom format not recognized`, grype is too old.
`anchore/syft:latest` emits CycloneDX 1.7, which grype only reads from 0.118 onwards.
Check with `grype version` and upgrade.

## Project layout

```
nodejs-unlicensed/
├── package.json              # the dependency list (no license field)
├── index.js                  # the main script
├── vendor/legacy-parser/     # the unlicensed local package (for the exercise)
└── README.md                 # this file
```
