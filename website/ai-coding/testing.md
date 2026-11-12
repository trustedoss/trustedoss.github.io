---
id: testing
title: 'AI가 만든 코드의 테스트 환경'
sidebar_label: '테스트 환경'
sidebar_position: 13
---

# AI가 만든 코드의 테스트 환경

:::info 이 페이지에서 다루는 것

- 테스트를 먼저 정하고 구현을 맡기는 작업 방식
- 에이전트가 테스트를 약화하는 것을 막는 세 겹의 통제
- 커버리지와 변이 테스트로 테스트 자체의 품질 재기
- 격리되고 재현 가능한 실행 환경, 불안정한 테스트 관리

대상은 개발자, 테스트·품질 담당, CI 를 운영하는 팀입니다.
:::

AI 코딩 도구를 쓰면 변경량이 늘어납니다. 리뷰 인원은 그대로이므로, 사람이 모든 줄을 읽어서
동작을 확인하는 방식은 곧 한계에 닿습니다. 이때 변경이 맞는지를 판단하는 기준은 테스트입니다.
테스트가 약하면 AI가 만든 코드가 맞는지 확인할 방법이 사람의 눈밖에 남지 않고, 테스트가
단단하면 에이전트에게 맡길 수 있는 범위가 넓어집니다.

이 페이지는 테스트를 AI 코딩의 검증 기준으로 세우는 방법을 다룹니다. 테스트를 먼저 정하는 작업
방식, 에이전트가 테스트를 약화하는 문제와 그 방어, 테스트 자체의 품질을 재는 방법, 격리된 실행
환경 순서입니다. 각 항목은 [ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice)
저장소에 동작하는 파일로 들어 있습니다.

## 1. 테스트가 거버넌스의 일부인 이유

[5단계 전략](./strategy)의 3단계 게이트는 알려진 위험 패턴을 찾습니다. 시크릿, 취약한 코드
패턴, 금지 라이선스가 그 대상입니다. 하지만 "이 함수가 요구사항대로 동작하는가"는 어떤 스캐너도
답하지 못합니다. 그 질문에 답하는 것이 테스트입니다.

DORA 의 2025 보고서는 AI 도입이 배포 처리량을 높이지만 배포 불안정성도 함께 높인다고 보고합니다.
변경이 많아질수록, 그 변경이 기존 동작을 깨지 않았음을 자동으로 확인하는 장치가 없으면 불안정이 그대로
운영으로 넘어갑니다. 테스트가 그 장치입니다.

에이전트를 사람이 한 단계씩 지시하지 않고 반복 실행(루프)으로 돌리는 방식이 늘면서 이 점이 더
분명해졌습니다. 공개된 에이전트 루프 50개를 분석한 연구(Macedo, 2026-06)는 루프 명세를 시작 조건, 목표,
검증 단계, 멈춤 기준, 기억으로 정의합니다. 검증 단계가 없으면 루프는 언제 끝났는지 알 수 없고, 검증이
약하면 잘못된 결과에서 멈춥니다. 대부분의 코드 작업에서 그 검증 단계가 테스트입니다.

정리하면, AI 코딩에서 테스트는 품질 활동이기 전에 통제 수단입니다. 에이전트에게 "완료"의
정의를 알려 주는 것도, 사람이 리뷰에서 무엇을 믿고 무엇을 확인할지 정하는 것도 테스트입니다.

## 2. 테스트를 먼저 정하고 구현을 맡기기

에이전트에게 구현과 테스트를 한 번에 맡기면, 에이전트는 자기가 만든 구현에 맞춰 테스트를
씁니다. 구현에 버그가 있으면 테스트도 그 버그를 정답으로 기록합니다. 테스트가 통과해도 요구사항을
확인한 것이 아니라 구현을 다시 적은 것에 그칩니다.

순서를 나누면 이 문제가 줄어듭니다.

1. 요구사항을 테스트로 적습니다. 사람이 쓰거나, 에이전트가 초안을 쓰고 사람이 검토합니다.
2. 테스트가 실패하는 것을 확인하고 커밋합니다. 실패하지 않는 테스트는 아무것도 확인하지 않습니다.
3. 에이전트에게 테스트를 고치지 말고 구현만 바꿔 통과시키라고 지시합니다.
4. 통과하면 사람이 구현을 리뷰합니다. 이때 리뷰의 초점은 동작이 아니라 설계와 유지보수성으로
   좁혀집니다. 동작은 테스트가 이미 확인했기 때문입니다.

도구 공급자의 가이드도 같은 순서를 권합니다. Anthropic 의 Claude Code 모범 사례(2025-04)는 테스트를
쓰고 커밋한 뒤 구현하는 흐름을 제시하면서, 테스트 주도 개발 중임을 알리고 테스트를 고치지 말라고 지시하며,
구현이 테스트에만 맞춰지지 않았는지 별도 서브에이전트로 확인하라고 권했습니다. 현재 문서는 "통과 또는
실패로 결과가 나오는 실행 가능한 것을 주라"고 정리합니다. GitHub 의 Spec Kit 은 명세 기반 개발
방법론에서 테스트 우선을 협상할 수 없는 원칙으로 둡니다.

이 순서는 저장소 규칙 파일에 적어 두면 에이전트가 매번 따릅니다. ai-coding-best-practice 의
[CLAUDE.md](https://github.com/trustedoss/ai-coding-best-practice/blob/main/CLAUDE.md) "테스트 정책"
절이 그 예입니다.

## 3. 에이전트가 테스트를 약화하는 문제

실패하는 테스트를 만난 에이전트는 코드를 고치는 대신 테스트를 바꿔 통과시키는 경우가 있습니다.
테스트를 지우거나, `skip` 을 붙이거나, 기대값을 현재 출력에 맞게 고치거나, 특정 입력만
처리하도록 구현을 끼워 맞추는 방식입니다.

측정된 결과가 있습니다. ImpossibleBench(2025-10)는 명세와 테스트가 서로 모순되게 만들어 정직하게는
통과할 수 없는 과제를 냈습니다. 과제를 통과했다면 테스트를 속인 것입니다. 한 과제 묶음에서 GPT-5 는
과제의 76%에서 그렇게 했습니다. Claude 모델이 속인 경우에는 79% 이상이 테스트 자체를 고치는 방식이었습니다. 프롬프트를 엄격하게
바꾸자 한 모델에서 92%가 1%로 줄었지만, 저자들은 테스트를 숨기거나 읽기 전용으로 두는 방법을 함께
권합니다. METR(2025-06)도 한 프런티어 모델이 특정 벤치마크 실행의 30.4%에서 점수 측정 방식을
조작했고, "속이지 말라"고 지시해도 비율이 크게 줄지 않았다고 보고했습니다.

규칙 파일에 "테스트를 고치지 말라"고 적는 것만으로는 부족합니다. 2단계 규칙은 권고일 뿐이라는
점이 여기서도 같습니다. 세 겹으로 막습니다.

| 위치          | 통제                                                                       | ai-coding-best-practice 파일                                                                                                                                                                                                                           |
| ------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 에이전트 세션 | `tests/` 를 고치려면 사람 승인을 받게 함                                   | [.claude/settings.json](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.claude/settings.json) 의 `Edit(./tests/**)`                                                                                                                   |
| pull request  | 테스트 파일·함수 삭제, `skip`·`xfail` 추가, assert 감소를 탐지해 실패 처리 | [test-integrity.yml](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/workflows/test-integrity.yml), [check-test-integrity.py](https://github.com/trustedoss/ai-coding-best-practice/blob/main/scripts/check-test-integrity.py) |
| 리뷰          | `tests/` 변경은 담당자 리뷰 요청                                           | [CODEOWNERS](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/CODEOWNERS)                                                                                                                                                       |

테스트를 지우는 것이 맞는 경우도 있습니다. 기능을 없앴거나 테스트가 잘못된 동작을 고정하고
있었다면 지워야 합니다. 그래서 test-integrity 검사는 금지가 아니라 확인 절차로 설계했습니다.
담당자가 변경을 읽고 `test-change-approved` 라벨을 붙이면 통과합니다. 라벨이 사람이 판단했다는
기록이 됩니다.

검사 스크립트는 Python 의 `ast` 모듈로 기준 브랜치와 PR 의 `tests/` 를 비교합니다. 정규식이
아니라 구문 트리를 보므로 주석이나 문자열 속 `assert` 에 속지 않습니다. 저장소에서 일부러
테스트 하나를 지우고 다른 하나에 `skip` 을 붙인 커밋으로 확인한 결과는 다음과 같습니다.

```text
Test suite weakened:
  - deleted test function: tests/test_app.py::test_fetch_rejects_missing_url
  - added skip/xfail marker(s): tests/test_app.py (+1)
  - assert count dropped: 18 -> 17
```

## 4. 테스트의 품질 재기: 커버리지와 변이 테스트

커버리지는 테스트가 실행한 줄의 비율입니다. 그 줄의 결과가 틀렸을 때 테스트가 알아차리는지는
알려 주지 않습니다. assert 가 하나도 없는 테스트로도 커버리지 100%를 만들 수 있습니다. AI가
테스트를 대량으로 만들면 이런 테스트가 섞이기 쉽습니다.

변이 테스트(mutation testing)가 이 빈틈을 잽니다. 도구가 소스 코드를 조금씩 바꾼 변이체를
만들고(비교 연산자 뒤집기, 상수 바꾸기, 호출 지우기), 변이체마다 테스트를 다시 돌립니다.
테스트가 실패하면 그 변이를 잡은 것이고, 통과하면 테스트가 그 잘못을 알아차리지 못한 것입니다.
살아남은 변이체 목록이 곧 보강할 assert 목록입니다.

| 언어                             | 도구                                      |
| -------------------------------- | ----------------------------------------- |
| Python                           | [mutmut](https://github.com/boxed/mutmut) |
| Java                             | [PIT](https://pitest.org/)                |
| JavaScript·TypeScript, C#, Scala | [Stryker](https://stryker-mutator.io/)    |

2026-11 기준 최신 버전은 mutmut 3.8.1, PIT 1.30.2, StrykerJS 10.1.1, Stryker.NET 5.1.0 입니다.
mutmut 는 `fork` 를 지원하는 운영체제가 필요해 Windows 에서는 WSL 안에서 돌립니다. 설정은
`pyproject.toml` 의 `[tool.mutmut]` 에 두며, 3.6.0 부터 대상 경로 키 이름이 `paths_to_mutate` 에서
`source_paths` 로 바뀌었습니다.

변이 테스트는 변이체마다 테스트를 다시 돌리므로 느립니다. PR 마다 돌리기보다 주기적으로 돌려
결과를 보고, 점수가 안정된 뒤에 게이트로 올리는 편이 낫습니다. ai-coding-best-practice 는
[tests.yml](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/workflows/tests.yml)
에서 테스트와 커버리지 하한 90%를 PR 차단 조건으로 두고,
[mutation.yml](https://github.com/trustedoss/ai-coding-best-practice/blob/main/.github/workflows/mutation.yml)
은 매주 월요일 권고로 돌려 살아남은 변이체를 작업 요약에 남깁니다.

적용하면서 확인한 제약이 하나 있습니다. mutmut 3 은 데코레이터가 붙은 함수를 변이 대상에서
뺍니다. Flask 라우트 핸들러가 모두 `@app.route` 를 달고 있어서, 처음 실행했을 때는 변이체를
하나도 만들지 못했습니다. 검색 로직과 URL 검사를 데코레이터 없는 함수로 분리하고 핸들러는 그
함수를 부르기만 하도록 바꾼 뒤에야 변이체 9개가 생겼고, 9개 모두 테스트가 잡았습니다. 핸들러를
얇게 두는 구조는 변이 테스트뿐 아니라 단위 테스트를 쓰기에도 낫습니다.

## 5. 격리되고 재현 가능한 실행 환경

에이전트가 테스트를 직접 돌리게 하려면 실행 환경이 두 조건을 만족해야 합니다.

첫째, 격리입니다. 테스트를 돌리는 에이전트는 셸 명령을 실행합니다. 개발자 워크스테이션의 인증
정보나 운영 환경에 닿지 않도록 샌드박스 안에서 돌립니다. 도구별 설정 방법은 각 도구 페이지의
"격리와 샌드박싱" 절에 있습니다(예: [Claude Code](./tools/claude-code#격리와-샌드박싱)).

둘째, 재현성입니다. 같은 커밋이면 누가 언제 돌려도 같은 결과가 나와야 에이전트의 판단을 믿을 수
있습니다.

- 의존성 버전을 고정합니다. ai-coding-best-practice 는 테스트 도구까지 `requirements-dev.txt` 에
  정확한 버전으로 적습니다.
- 외부 네트워크 호출은 테스트에서 대체합니다. 외부 서비스 상태에 따라 결과가 바뀌는 테스트는
  에이전트에게 잘못된 신호를 줍니다. 저장소의 `/fetch` 테스트는 `unittest.mock` 으로 응답을
  대체합니다.
- 로컬과 CI 가 같은 명령을 씁니다. CI 의 `pytest --cov=src --cov-fail-under=90` 을 로컬에서도 그대로
  돌리면 에이전트가 로컬에서 확인한 결과와 게이트의 판정이 어긋나지 않습니다.
- 컨테이너나 개발 컨테이너(devcontainer)로 런타임을 고정하면 운영체제 차이까지 줄일 수 있습니다.

## 6. 불안정한 테스트(flaky test)

같은 코드에서 통과와 실패를 오가는 테스트는 AI 코딩 환경에서 특히 해롭습니다. 에이전트는 실패를
보고 코드를 고치려 들고, 다음 실행에서 우연히 통과하면 그 수정이 맞았다고 판단합니다. 사람은
"원래 가끔 실패한다"며 실패를 무시하는 습관이 생기고, 진짜 실패도 함께 묻힙니다.

불안정한 테스트는 지우거나 조용히 `skip` 하지 말고, 담당자와 고칠 기한을 정해 격리 목록에 올립니다.
`skip` 을 붙이면 test-integrity 검사가 걸리므로, 라벨을 붙이는 담당자가 격리 사유를 PR 에 남기게
됩니다. 격리 목록이 늘어나는 추세 자체가 테스트 환경을 점검할 신호입니다.

## 7. 퍼징과의 관계

[AI 퍼징](./ai-fuzzing)(4b)도 테스트의 한 형태지만 목적이 다릅니다. 여기서 다룬 테스트는 사람이
정한 요구사항을 확인합니다. 퍼징은 아무도 요구사항으로 적지 않은 입력을 던져 예상하지 못한 동작을
찾습니다. 퍼징이 찾은 결함은 재현 입력을 회귀 테스트로 옮겨야 다시 생기지 않습니다. 두 가지는
대체 관계가 아니라 순서입니다.

## 8. 도입 순서

| 순서 | 할 일                                                    | 강제 수준         |
| ---- | -------------------------------------------------------- | ----------------- |
| 1    | 핵심 동작 테스트를 쓰고 CI 에서 돌린다                   | 차단              |
| 2    | 규칙 파일에 테스트 우선 작업과 테스트 약화 금지를 적는다 | 권고              |
| 3    | test-integrity 검사와 CODEOWNERS 를 건다                 | 차단(라벨로 해제) |
| 4    | 커버리지 하한을 현재 수준에 맞춰 건다                    | 차단              |
| 5    | 변이 테스트를 주기적으로 돌리고 결과를 본다              | 권고              |

커버리지 하한은 처음부터 높게 잡지 말고 현재 값에서 시작해 올립니다. 하한을 넘기려고 assert 없는
테스트를 만드는 일이 생기면 4번이 오히려 테스트를 약하게 만듭니다. 5번 변이 테스트가 그 경우를
드러냅니다.

## 표준 연계와 출처

이 페이지의 통제는 ISO/IEC 5230·18974 의 특정 조항을 직접 충족하지는 않습니다. 다만 18974
§4.3.2 의 취약점 대응에서 수정이 회귀를 만들지 않았음을 보이는 근거가 되고, 사용 정책에서 정한
리뷰·승인 절차가 실제로 지켜졌음을 보여 주는 기록(라벨, CODEOWNERS 리뷰)을 남깁니다.

- DORA, [State of AI-assisted Software Development 2025](https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf) (2025-09)
- Anthropic, [Claude Code best practices](https://web.archive.org/web/20250602202220/https://www.anthropic.com/engineering/claude-code-best-practices) (2025-04-18, 보관본) / [현행 Best practices](https://code.claude.com/docs/en/best-practices)
- GitHub, [Spec Kit](https://github.com/github/spec-kit) (`spec-driven.md`, Article III Test-First Imperative)
- Zhong et al., [ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases](https://arxiv.org/abs/2510.20270) (2025-10-23)
- Macedo, [Stop Hand-Holding Your Coding Agent: Engineering the Loops that Replace Step-by-Step Prompting](https://arxiv.org/abs/2607.00038) (2026-06-28)
- METR, [Recent Frontier Models Are Reward Hacking](https://metr.org/blog/2025-06-05-recent-reward-hacking/) (2025-06-05)
- [mutmut](https://github.com/boxed/mutmut), [PIT](https://pitest.org/), [Stryker](https://stryker-mutator.io/)
- [ai-coding-best-practice](https://github.com/trustedoss/ai-coding-best-practice) 저장소의 `tests/`, `scripts/check-test-integrity.py`, `.github/workflows/`

모든 출처는 2026-11-12에 확인했습니다.

## 다음 단계

- [AI 코딩의 생산성과 협업](./collaboration): 테스트가 받쳐 주는 작은 PR과 리뷰 분담
- [AI 퍼징](./ai-fuzzing): 요구사항으로 적지 않은 입력 탐색
- [Best Practice 저장소](./best-practice-repo): 이 페이지에서 다룬 파일 전체
- [5단계 전략](./strategy): 3단계 게이트와 함께 거는 테스트 게이트
