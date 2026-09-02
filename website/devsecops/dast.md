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

:::tip 아래 설정은 예시입니다 — 작동하는 전체 구현은 참조 저장소에
이 페이지의 YAML·명령은 핵심을 보여주는 예시입니다. 복사해 바로 쓸 수 있는 전체 파이프라인(정책 파일·샘플 앱 포함)은 [Best Practice 저장소](/ai-coding/best-practice-repo)에서 확인하세요.
:::

:::note 예시의 태그 표기와 실제 운영 설정
아래 예시는 읽기 쉽도록 `@v7` 같은 태그를 그대로 썼습니다. 태그는 나중에 다른 커밋을 가리키도록 바뀔 수 있으므로, 실제 운영 워크플로에서는 액션을 커밋 SHA로 고정하고 `permissions:` 로 잡마다 필요한 권한만 부여하세요. 이유와 방법은 [파이프라인 자체 보안](/devsecops/pipeline-security)에서 다룹니다.
:::

**정의:** 실행 중인 애플리케이션에 실제 HTTP 요청을 보내 SQL 인젝션, XSS, 인증 우회, 민감 정보 노출 같은 런타임 취약점을 탐지합니다.

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
    permissions:
      contents: read
      issues: write # ZAP 액션이 결과를 이슈로 등록합니다
    steps:
      - uses: actions/checkout@v7

      # 앱 실행 (예: Docker Compose)
      - name: Start application
        run: |
          docker compose up -d
          sleep 10  # 앱 기동 대기

      # ZAP Baseline 스캔 (수동 개입 없이 기본 취약점 탐지)
      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.15.0
        with:
          target: http://localhost:8080
          rules_file_name: zap-rules.tsv
          fail_action: true

      # ZAP API 스캔 (OpenAPI 명세 기반)
      - name: ZAP API Scan
        uses: zaproxy/action-api-scan@v0.10.0
        with:
          target: http://localhost:8080/api/openapi.json
          format: openapi
          fail_action: true

      - name: Upload ZAP report
        uses: actions/upload-artifact@v7
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

PR 단계에는 Baseline, 릴리즈 전에는 Full Scan을 실행하는 이중 전략을 권장합니다. 다만 Full Scan은 **무엇을 대상으로 삼는지**가 정해진 다음에 붙여야 합니다. 아래 차이 때문입니다.

### Baseline과 Full은 무엇이 다른가

두 스캔의 차이는 시간이 아니라 대상에 무엇을 보내느냐입니다.

| 구분             | Baseline                                                | Full Scan                                                   |
| ---------------- | ------------------------------------------------------- | ----------------------------------------------------------- |
| 동작             | 스파이더로 훑고 오가는 트래픽을 관찰                    | 발견한 모든 파라미터에 공격 페이로드 전송                   |
| 보내는 요청      | 일반적인 조회 요청                                      | SQL 인젝션, 경로 탐색, 명령 인젝션 등 실제 공격 문자열      |
| 찾는 것          | 응답에 드러나는 문제(헤더 누락, 쿠키 플래그, 정보 노출) | 실제로 취약점이 성립하는지                                  |
| 대상에 남는 흔적 | 조회 로그                                               | 공격 시도 로그, 새로 생기거나 바뀐 데이터, 실패한 인증 시도 |

Baseline은 공격 페이로드를 보내지 않습니다. 그래서 데모나 스테이징처럼 사람이 쓰고 있는 환경에 걸어도 무리가 없습니다. 프로덕션은 이 페이지 아래 주의사항대로 여전히 대상에서 제외합니다. 대신 응답에 드러나는 것만 봅니다.

### 운영 중인 대상에 Full Scan을 걸 때

Full Scan은 성격이 다릅니다. 아래 셋 중 앞의 둘은 대상이 읽기 전용이어도 그대로 성립합니다.

- **자원 고갈.** 발견한 파라미터마다 수십에서 수백 건의 변형 요청을 보냅니다. 검색이나 목록 조회처럼 무거운 경로에 이것이 걸리면 정상 사용자가 체감할 만큼 느려집니다.
- **계정 잠금.** 로그인 경로를 발견하면 인증 우회를 시도하며 반복 요청을 보냅니다. 잠금 정책이 있는 시스템에서는 스캔이 끝난 뒤 실제 계정이 잠겨 있을 수 있습니다.
- **데이터 오염.** 쓰기가 막혀 있어도 예외적으로 열린 경로가 있으면 그쪽으로 요청을 보냅니다. 스캔 결과 업로드나 웹훅 수신처럼 외부 입력을 받도록 설계된 경로가 대표적입니다.

그래서 Full Scan은 스캔 전용 인스턴스에 겁니다. 데이터를 지우고 다시 만들 수 있고, 계정이 잠겨도 실제 사용자가 없고, 부하가 튀어도 아무도 불편하지 않은 환경이어야 합니다.

### TRUSCA에 붙인 방식

[TRUSCA](https://github.com/trustedoss/trusca)에는 Baseline만 먼저 붙였습니다. 워크플로는 [dast-baseline.yml](https://github.com/trustedoss/trusca/blob/main/.github/workflows/dast-baseline.yml)이고 매주 월요일에 돕니다. 대상 URL을 저장소 변수로 두어, 설정하지 않으면 아무것도 스캔하지 않고 통과합니다.

데모 호스트가 `DEMO_READ_ONLY` 로 GET과 HEAD, OPTIONS 외의 요청을 거부하고 있어 쓰기 위험은 대부분 막혀 있었습니다. 그런데도 Full을 미룬 이유는 앞의 두 가지가 읽기 전용과 무관하게 남기 때문입니다. 조회만 해도 자원은 소모되고, 인증 시도는 잠금 정책을 건드립니다. 세 번째인 데이터 오염도 완전히 사라지지는 않습니다. 샌드박스 스캔을 허용하는 설정을 켜면 스캔 결과를 받아들이는(ingest) 경로가 열리기 때문입니다. Full은 스캔 전용 인스턴스가 생긴 뒤로 미뤘습니다.

Baseline에도 상한을 걸었습니다. 스파이더 2분, 전체 실행 6분입니다. 실행 시간을 줄이려는 것이 아닙니다. 데모가 저비용으로 운영되고 있어 메모리 상한이 걸려 있고, 제한 없는 스파이더의 조회 부하 자체가 그 규모에 부담이 되기 때문입니다. 실제로 한 번 돌려 응답 시간이 흔들리지 않는 것을 확인한 뒤에 늘리는 편이 안전합니다.

대상 URL은 워크플로에 직접 쓰지 않고 저장소 변수로 두었습니다. 변수가 비어 있으면 잡이 "아무것도 스캔하지 않았다"는 메시지를 남기고 성공으로 끝납니다. 워크플로를 머지하는 것과 특정 호스트를 대상으로 지정하는 것은 다른 결정이고, 후자가 전자의 부수 효과로 일어나면 안 되기 때문입니다.

다만 이 구조에는 짝이 되는 위험이 있습니다. 변수를 설정하지 않은 채로 두면 워크플로는 계속 초록이고, 초록만 보는 사람은 DAST가 돌고 있다고 생각합니다. 그래서 잡 요약에 위험도별 건수와 함께 **몇 개의 서로 다른 URL을 훑었는지**를 찍고, 그 값이 0이면 깨끗한 스캔이 아니라 실패한 스캔이라고 명시했습니다. 껐다는 사실이 로그에 남아야 껐다는 것을 압니다.

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
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v7

      - name: Start application
        run: |
          docker compose up -d
          sleep 10

      - name: Run Nuclei
        uses: projectdiscovery/nuclei-action@v3
        with:
          target: http://localhost:8080
          # v3부터 templates·severity 같은 개별 input이 제거되어
          # flags 로 nuclei CLI 플래그를 직접 전달합니다.
          flags: '-t cves/ -t misconfiguration/ -t exposures/ -severity medium,high,critical -o nuclei.log'

      - name: Upload Nuclei report
        uses: actions/upload-artifact@v7
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

:::note
SCA, SAST, 시크릿, IaC 페이지가 제공하는 브라우저 결과 분석기는 이 주제에는 아직 없습니다.
ZAP 리포트(zap-report.html)는 우선순위가 표기되어 있어 그대로 검토하면 됩니다.
:::

## 다음 단계

- 전체 보안 파이프라인 통합: [파이프라인 설계](./pipeline-design)
- 배포 후 지속적 보안 모니터링: [모니터링·자동 교정](./monitoring)
