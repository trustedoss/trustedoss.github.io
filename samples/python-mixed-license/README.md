# python-mixed-license — GPL + Permissive 라이선스 혼재 시연

## 실습 목적

이 샘플은 **GPL 라이선스와 Permissive 라이선스가 혼재**할 때 발생하는
라이선스 리스크를 시연합니다.

## 포함된 라이선스 현황

| 패키지 | 버전 | 라이선스 | 배포 시 의무사항 |
|--------|------|---------|----------------|
| PyYAML | 6.0.1 | MIT | 저작권 고지 |
| requests | 2.31.0 | Apache-2.0 | 저작권 고지, NOTICE 파일 |
| celery | 5.3.4 | BSD | 저작권 고지 |
| mysql-connector-python | 8.1.0 | GPL-2.0 | **소스코드 공개 의무** |

## 예상 실습 결과

### SBOM 생성 시
- `mysql-connector-python` GPL-2.0 컴포넌트 탐지

### 라이선스 분석 시
- **Copyleft 위험 항목 표시** (GPL-2.0)
- 소스코드 공개 의무 검토 필요 표시

## 강의 포인트

1. **GPL 컴포넌트를 포함하면** 배포 방식에 따라 전체 소스 공개 의무가 생길 수 있다
2. **라이선스 allowlist 정책**이 왜 필요한가 (policy/license-allowlist.md)
3. **도입 전 라이선스 확인**의 중요성

## GPL 라이선스 리스크 상세 설명

GPL-2.0 의 "카피레프트(Copyleft)" 특성:
- GPL 라이선스 코드를 포함하여 배포 시, 전체 소프트웨어의 소스코드를 공개해야 할 수 있다
- 상업용 소프트웨어에 GPL 컴포넌트를 포함하는 것은 법적 검토 필수
- LGPL은 라이브러리 형태로 링크 시 소스공개 의무가 완화됨

## 실제 조치 방법

GPL 컴포넌트를 동등한 기능의 Permissive 라이선스 패키지로 교체 검토:

| 현재 (GPL) | 대안 (Permissive) | 라이선스 |
|-----------|-----------------|---------|
| mysql-connector-python (GPL-2.0) | PyMySQL | MIT |
| mysql-connector-python (GPL-2.0) | aiomysql | MIT |

또는 법무 검토 후 소스코드 공개 준비.

## SBOM 생성 명령어

```bash
docker run --rm -v $(pwd):/project \
  anchore/syft:latest \
  /project --output cyclonedx-json \
  > ../../output/sbom/python-mixed.cdx.json
```

## 프로젝트 구조

```
python-mixed-license/
├── requirements.txt    # 의존성 목록 (GPL 포함)
├── main.py             # 메인 스크립트
└── README.md           # 이 파일
```
