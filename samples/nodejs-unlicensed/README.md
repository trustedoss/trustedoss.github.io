# nodejs-unlicensed — 라이선스 미명시 패키지 리스크 시연

## 실습 목적

이 샘플은 **라이선스가 명시되지 않은 패키지를 포함**할 때의
법적 리스크를 시연합니다.

## 포함된 패키지 현황

| 패키지 | 버전 | 라이선스 | 상태 |
|--------|------|---------|------|
| express | ^4.18.2 | MIT | 명확 — 상업적 사용 가능 |
| lodash | ^4.17.21 | MIT | 명확 — 상업적 사용 가능 |
| nightmare | ^3.0.2 | UNLICENSED | **위험 — 사용 권한 불명확** |

> **참고:** 이 프로젝트(package.json) 자체에도 license 필드가 없습니다.
> SBOM 생성 시 NOASSERTION으로 표시됩니다.

## 예상 실습 결과

### SBOM 생성 시
- `nightmare` 패키지의 라이선스 필드: `UNLICENSED` 또는 `NOASSERTION`
- 프로젝트 자체 라이선스: `NOASSERTION`

### 라이선스 분석 시
- **라이선스 확인 필요 항목 표시**
- 상업적 사용 위험 표시

## 강의 포인트

1. **라이선스 미명시 = 기본적으로 All Rights Reserved**
   저작권법상 명시적 허가 없이는 사용 권한이 없다
2. **npm 생태계의 라이선스 불확실성 문제**
   package.json 의 license 필드를 신뢰하기 어려운 경우도 있음
3. **라이선스 확인 없이 사용하면 법적 리스크**
   특히 상업적 배포 시 위험

## 실제 조치 방법

1. **패키지 저장소(GitHub)에서 라이선스 직접 확인**
   ```bash
   # npm 패키지 라이선스 정보 확인
   npm view nightmare license
   ```

2. **확인 불가 시 해당 패키지 사용 금지**
   대안 패키지 검토:
   | 현재 (불명확) | 대안 | 라이선스 |
   |-------------|------|---------|
   | nightmare | puppeteer | Apache-2.0 |
   | nightmare | playwright | Apache-2.0 |

3. **license-allowlist.md 에 검토 결과 기록**
   ```
   output/policy/license-allowlist.md
   ```

## SBOM 생성 명령어

```bash
# npm install 먼저 실행
npm install

docker run --rm -v $(pwd):/project \
  anchore/syft:latest \
  /project --output cyclonedx-json \
  > ../../output/sbom/nodejs-unlicensed.cdx.json
```

## 프로젝트 구조

```
nodejs-unlicensed/
├── package.json    # 의존성 목록 (license 필드 없음)
├── index.js        # 메인 스크립트
└── README.md       # 이 파일
```
