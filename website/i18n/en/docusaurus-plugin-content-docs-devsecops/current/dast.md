---
id: dast
title: 동적 분석 (DAST)
sidebar_label: DAST
sidebar_position: 8
---

# 동적 분석 (DAST)

## DAST란

:::info DAST는 SAST의 대체가 아닌 보완입니다
SAST는 코드를 보고 DAST는 실행 중인 앱을 봅니다. 두 가지를 함께 적용해야 사각지대를 줄일 수 있습니다.
:::

**정의:** 실행 중인 애플리케이션에 실제 HTTP 요청을 보내 SQL 인젝션·XSS·인증 우회·민감 정보 노출 등 런타임 취약점을 탐지합니다.

**SAST와의 차이:** SAST는 코드 작성 단계에서 빠르게 탐지하지만 런타임 동작은 확인할 수 없습니다. DAST는 배포 후 실제 동작을 검증하므로 SAST가 놓친 취약점을 발견할 수 있습니다.

---

## 도구 비교

| 도구      | 특징                           | 주요 용도               | 라이선스   |
| --------- | ------------------------------ | ----------------------- | ---------- |
| OWASP ZAP | 업계 표준·GUI·자동화 모두 지원 | 웹앱·API 전체 스캔      | Apache-2.0 |
| Nuclei    | 템플릿 기반·빠른 속도·경량     | 알려진 취약점 패턴 스캔 | MIT        |

심층 웹앱 스캔에는 OWASP ZAP, 알려진 CVE·미설정 취약점 빠른 검사에는 Nuclei를 권장합니다.

---

## OWASP ZAP 설정

### GitHub Actions

```yaml
# .github/workflows/dast-zap.yml

name: DAST — OWASP ZAP

on:
  push:
    branches: [main]

jobs:
  zap:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # 앱 실행 (예: Docker Compose)
      - name: Start application
        run: |
          docker compose up -d
          sleep 10  # 앱 기동 대기

      # ZAP Baseline 스캔 (수동 개입 없이 기본 취약점 탐지)
      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.12.0
        with:
          target: http://localhost:8080
          rules_file_name: zap-rules.tsv
          fail_action: true

      # ZAP API 스캔 (OpenAPI 명세 기반)
      - name: ZAP API Scan
        uses: zaproxy/action-api-scan@v0.7.0
        with:
          target: http://localhost:8080/api/openapi.json
          format: openapi
          fail_action: true

      - name: Upload ZAP report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: zap-report
          path: report_html.html
```

### 스캔 유형 선택

| 스캔 유형 | Action           | 소요 시간 | 권장 상황            |
| --------- | ---------------- | --------- | -------------------- |
| Baseline  | action-baseline  | 2~5분     | PR마다 기본 검사     |
| API Scan  | action-api-scan  | 5~15분    | OpenAPI 명세 있을 때 |
| Full Scan | action-full-scan | 20분+     | 릴리즈 전 심층 검사  |

PR 단계에는 Baseline, 릴리즈 전에는 Full Scan을 실행하는 이중 전략을 권장합니다.

### 규칙 파일 설정

특정 알림을 무시하거나 실패로 처리할 규칙은 `zap-rules.tsv` 파일로 관리합니다.

```
# zap-rules.tsv
10016	IGNORE	(웹 브라우저 XSS 보호 헤더 — 레거시 브라우저 대응 불필요)
10020	WARN	(X-Frame-Options 헤더 미설정)
10021	FAIL	(Anti-CSRF 토큰 미설정)
```

`IGNORE`·`WARN`·`FAIL` 세 가지 수준으로 항목별 처리 방식을 지정할 수 있습니다.

---

## Nuclei 설정

### GitHub Actions

```yaml
# .github/workflows/dast-nuclei.yml

name: DAST — Nuclei

on:
  push:
    branches: [main]

jobs:
  nuclei:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Start application
        run: |
          docker compose up -d
          sleep 10

      - name: Run Nuclei
        uses: projectdiscovery/nuclei-action@main
        with:
          target: http://localhost:8080
          templates: cves,misconfiguration,exposures
          severity: medium,high,critical
          fail-on-severity: high

      - name: Upload Nuclei report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: nuclei-report
          path: nuclei.log
```

### 주요 템플릿 카테고리

| 카테고리         | 설명                   |
| ---------------- | ---------------------- |
| cves             | 알려진 CVE 취약점 패턴 |
| misconfiguration | 보안 설정 오류         |
| exposures        | 민감 정보·파일 노출    |
| default-logins   | 기본 계정·패스워드     |
| takeovers        | 서브도메인 탈취 가능성 |

---

## DAST 도입 시 주의사항

:::warning DAST는 반드시 격리된 테스트 환경에서 실행하세요
:::

**환경 분리:** DAST는 실제 HTTP 요청을 보내므로 프로덕션 환경에서 실행하면 데이터 오염·서비스 장애가 발생할 수 있습니다. 반드시 스테이징·테스트 환경에서만 실행합니다.

**인증 설정:** 인증이 필요한 엔드포인트는 ZAP의 인증 설정 또는 Nuclei의 헤더 옵션으로 토큰을 전달해야 커버리지가 확보됩니다.

**오탐 관리:** DAST는 SAST보다 오탐 비율이 높습니다. 처음에는 `WARN`으로 시작해 결과를 검토한 뒤 `FAIL`로 전환하는 단계적 접근을 권장합니다.

---

## 다음 단계

- 전체 보안 파이프라인 통합: [파이프라인 설계](./pipeline-design)
- 배포 후 지속적 보안 모니터링: [모니터링·자동 교정](./monitoring)
