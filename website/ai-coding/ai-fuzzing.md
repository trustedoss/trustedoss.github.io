---
id: ai-fuzzing
title: AI 퍼징
sidebar_label: AI 퍼징
sidebar_position: 8
---

# AI 퍼징 (4b 단계)

3단계 도구는 룰에 정의된 패턴을 찾습니다. 룰이 묘사하지 않은 것 — 비즈니스 로직 결함,
엣지케이스 입력 처리 — 은 정의상 걸리지 않습니다. 4b 는 그 영역을 **모델이 직접 탐색**해서
메웁니다. [4a](./ai-security-review) 가 이미 플래그된 것을 다시 판정한다면, 4b 는 아무도
플래그하지 않은 곳을 찾습니다.

:::info 이 단계만 앱을 실제로 실행합니다

1~3단계와 4a 는 코드를 읽습니다. 4b 는 앱을 띄우고 요청을 보내 응답을 봅니다. 정적 분석이
도달하지 못하는 결함이 여기서 나오는 이유이고, 매 커밋이 아니라 주기로 도는 이유이기도
합니다.

:::

## 무엇을 어떻게 하는가

| 단계 | 하는 일                                                     |
| ---- | ----------------------------------------------------------- |
| 읽기 | 앱 코드를 모델에 넘겨 엔드포인트와 파라미터를 파악합니다    |
| 생성 | 엔드포인트마다 경계값과 이상 입력을 만듭니다                |
| 실행 | 기동한 앱에 실제로 요청을 보냅니다                          |
| 관찰 | 5xx 응답, 비정상 응답, 어긋나는 상태를 결함 후보로 남깁니다 |

무작위 바이트를 넣는 전통적 퍼징과 다릅니다. 모델이 엔드포인트 시그니처를 읽고 **의미 있는
경계값**을 만듭니다. 문자열 길이 제한 근처, 음수, 빈 값, 타입이 어긋나는 값, 경로 탐색
문자열 같은 것들입니다.

## 대상별 도구 조합

| 도구 조합         | 탐지 대상                       | 실행 주기       |
| ----------------- | ------------------------------- | --------------- |
| Claude + requests | 웹 API 엣지케이스·비정상 응답   | Push to main    |
| Claude + AFL++    | 저수준 바이너리 크래시          | 주 1회 스케줄   |
| Claude + OSS-Fuzz | 오픈소스 라이브러리 파서 취약점 | 프로젝트별 설정 |

C/C++ 나 Rust 같은 저수준 코드는 모델이 입력을 만들더라도 실행 커버리지를 추적하는 쪽이
효과적입니다. 이 경우 OSS-Fuzz 연동을 권장합니다.

## 실전 적용 사례 — ai-coding-best-practice

[ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice) 저장소가 이
단계를 매주 돌립니다. 파일 두 개로 되어 있습니다.

### 워크플로

[ai-fuzzing.yml](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/workflows/ai-fuzzing.yml)
이 main 푸시와 매주 일요일에 실행됩니다.

```yaml
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 4 * * 0'
```

앱을 기동하고 헬스체크로 준비를 확인한 뒤 스크립트를 실행합니다. 결과 파일은 artifact 로
30일 보관합니다.

```yaml
- name: Start app
  run: |
    python src/app.py &
    sleep 5
    curl -sf http://localhost:8080/health || (echo "앱 기동 실패" && exit 1)
```

**키가 없으면 건너뜁니다.** `ANTHROPIC_API_KEY` 가 없는 fork 나 도입 초기에도 job 이
실패하지 않습니다. 4a 워크플로와 같은 설계입니다.

```yaml
if [ -z "$ANTHROPIC_API_KEY" ]; then
echo "::warning::ANTHROPIC_API_KEY가 설정되지 않아 AI 퍼징을 건너뜁니다."
exit 0
fi
```

### 스크립트

[scripts/ai-fuzz.py](https://github.com/trustedoss/ai-coding-best-practice/blob/main/scripts/ai-fuzz.py)
가 세 가지를 합니다.

- `generate_fuzz_cases()` — 앱 코드를 모델에 넘겨 엔드포인트별 케이스를 JSON 배열로 받습니다.
  최소 20건을 요구하고, 인젝션·경로 탐색·비정상 입력을 탐지 목표로 지정합니다
- `run_fuzz_cases()` — 각 케이스를 실제 요청으로 보냅니다. 상태 코드가 500 미만이면 통과,
  그 이상이거나 예외가 나면 실패로 기록하고 응답 앞부분을 함께 남깁니다
- 결과를 `fuzz-report.json` 으로 씁니다

## 도입할 때 주의할 것

**차단 게이트로 쓰지 않습니다.** 모델이 만든 입력이므로 오탐이 섞이고, 실패 하나로 배포를
막으면 곧 꺼지게 됩니다. 4a 와 같은 원칙입니다.

**격리된 환경에서 돌립니다.** 실제 요청을 보내므로 운영 환경을 대상으로 하면 안 됩니다.
CI 안에서 앱을 새로 띄우고 그 인스턴스만 대상으로 합니다.

**비용을 주기로 조절합니다.** 매 커밋마다 20건 이상을 생성·실행하면 토큰과 시간이 함께
듭니다. 위 사례는 main 푸시와 주 1회로 제한합니다.

## 셀프 스터디

- 위 저장소를 fork 한 뒤 `ANTHROPIC_API_KEY` 를 등록하고 워크플로를 수동 실행해 보세요.
  키가 없을 때 job 이 어떻게 끝나는지 먼저 확인하면 도입 부담을 가늠할 수 있습니다
- `fuzz-report.json` 을 열어 실패한 케이스의 `description` 을 읽어 보세요. 모델이 무엇을
  노렸는지가 적혀 있습니다
- 여러분의 앱에 적용한다면 `BASE_URL` 과 기동 명령만 바꾸면 됩니다

## 다음 단계

- [AI 보안 코드 리뷰](./ai-security-review) — 4a, 이미 플래그된 것을 다시 판정합니다
- [에이전트와 MCP 도구 거버넌스](./agent-governance) — 4c, AI 가 호출하는 도구를 통제합니다
- [5단계 전략](./strategy) — 전체 모델에서 이 단계의 위치
