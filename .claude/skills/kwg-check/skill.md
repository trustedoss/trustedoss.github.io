# Skill: KWG 싱크 체크 (kwg-check)

## 호출 방법

```
/kwg-check [모드]
```

| 모드     | 의미                                           |
| -------- | ---------------------------------------------- |
| _(없음)_ | check-kwg-drift.py 실행 후 변경 있으면 갭 분석 |
| `full`   | 변경 여부 무관하게 전체 갭 분석 강제 실행      |
| `reset`  | 스냅샷 초기화 (sync 직후 기준점 재설정 시)     |

---

## 실행 순서

### Step 1 — 구조적 변경 감지

```bash
python3 .claude/scripts/check-kwg-drift.py
```

결과 해석:

- **exit 0 + "싱크 OK"** → 구조적 변경 없음. Step 2 건너뜀.

  ```
  ✅ 싱크 OK — 마지막 동기화 대비 구조적 변경 없음
  ```

  → 종료. "KWG 싱크 이상 없음" 출력.

- **exit 1 + 변경 목록** → 변경 감지됨. Step 2 실행.

- **`full` 모드** → Step 1 결과 무관하게 Step 2 실행.

---

### Step 2 — 의미론적 갭 분석

`@kwg-drift-checker` 에이전트 호출.

전달 내용:

- Step 1의 드리프트 리포트 전체
- 분석 모드: changed (변경 파일만) 또는 full (전체)

에이전트가 갭 분석 리포트를 반환할 때까지 대기.

---

### Step 3 — 최종 보고

갭 분석 리포트를 그대로 출력 후:

```
## 다음 행동 요약

🔴 즉시 반영 필요:
  1. [항목] → [파일] 수정 방법

🟡 검토 후 결정:
  1. [항목] → [판단 기준]

완료 후:
  /qa changed           # 품질 검증
  bash .claude/scripts/verify.sh  # 8/8 PASS 확인
  python3 .claude/scripts/check-kwg-drift.py --reset  # 기준점 재설정
```

---

## 사용 시나리오

### 분기별 정기 싱크 확인

```bash
# 1. KWG 원본 갱신
bash .claude/scripts/sync-kwg-reference.sh

# 2. 변경 있으면 자동으로 /kwg-check 실행 제안이 뜸
#    직접 실행:
/kwg-check

# 3. 반영 완료 후 기준점 재설정
python3 .claude/scripts/check-kwg-drift.py --reset
```

### KWG 업데이트 알림 받은 후 즉시 확인

```bash
bash .claude/scripts/sync-kwg-reference.sh
/kwg-check
```

### 전체 갭 현황 파악 (변경 없어도)

```bash
/kwg-check full
```

---

## `reset` 모드 사용 시점

아래 상황에서 `python3 .claude/scripts/check-kwg-drift.py --reset` 실행:

1. 갭 분석 후 반영 작업을 모두 완료했을 때
2. 처음 sync-kwg-reference.sh 실행 직후 (초기 기준점 설정)
3. kwg-mapping.yaml을 대규모 수정한 후

**주의**: reset 전에 갭 분석에서 🔴 항목을 모두 반영했는지 확인.
미반영 상태로 reset하면 다음 sync 때 해당 변경이 감지되지 않는다.
