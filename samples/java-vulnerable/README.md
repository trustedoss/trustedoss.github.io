# java-vulnerable — Log4Shell 취약점 탐지 실습

## 실습 목적

이 샘플 프로젝트는 **Log4Shell 취약점 (CVE-2021-44228) 탐지 실습용**입니다.
SBOM 생성 도구와 취약점 분석 도구가 어떻게 Critical 취약점을 탐지하는지 직접 확인합니다.

## 의도적으로 포함된 취약점

| CVE | 컴포넌트 | 버전 | CVSS | 심각도 |
|-----|---------|------|------|--------|
| CVE-2021-44228 | log4j-core | 2.14.1 | 10.0 | Critical |

**Log4Shell 취약점이란?**
Apache Log4j 2의 JNDI 조회 기능을 악용하여 원격 코드 실행(RCE)이 가능한 취약점.
2021년 12월 공개 직후 전 세계적으로 광범위하게 악용되었다.

## 예상 실습 결과

### SBOM 생성 시
- `log4j-core 2.14.1` 컴포넌트 탐지

### 취약점 분석 시
- **CVE-2021-44228 Critical 탐지**
- 즉시 조치 권고 (2.15.0 이상으로 업그레이드)

## 강의 포인트

1. **단 하나의 취약한 의존성**이 전체 시스템을 위험에 빠뜨릴 수 있다
2. **SBOM이 없으면** 이런 컴포넌트를 추적하기 어렵다
3. **취약점 공개 즉시 업그레이드**가 필요한 이유

## 실제 조치 방법

`pom.xml` 에서 log4j-core 버전을 **2.17.1 이상**으로 변경:

```xml
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-core</artifactId>
    <version>2.17.1</version>  <!-- 취약점 수정 버전 -->
</dependency>
```

## SBOM 생성 명령어

```bash
docker run --rm -v $(pwd):/project \
  anchore/syft:latest \
  /project --output cyclonedx-json \
  > ../../output/sbom/java-vulnerable.cdx.json
```

## 프로젝트 구조

```
java-vulnerable/
├── pom.xml                          # Maven 빌드 파일 (취약한 log4j 포함)
├── README.md                        # 이 파일
└── src/
    └── main/
        └── java/
            └── com/
                └── example/
                    └── App.java     # 메인 애플리케이션
```
