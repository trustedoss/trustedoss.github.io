# Skill: QA 오케스트레이터 (qa-loop)

## 호출 방법

```
/qa [대상]
```

| 대상               | 의미                                 |
| ------------------ | ------------------------------------ |
| `changed` (기본값) | git으로 추적된 변경 파일만 검사      |
| `all`              | docs/, agents/, templates/ 전체 검사 |
| 파일 경로          | 특정 파일 1개 검사                   |
| 챕터 번호          | 해당 챕터 문서 감사 (03, 05 등)      |

## 실행 순서

### Step 1 — 변경 범위 계산 (diff-scope)

`changed` 또는 기본값 호출 시:

```bash
git diff --name-only HEAD
git diff --name-only HEAD~1 2>/dev/null | head -20
```

결과를 기반으로 처리 대상 파일 목록 결정.
`all` 호출 시 Step 1 건너뜀.

---

### Step 2 — 품질 이슈 탐지 (qa-reviewer)

`@qa-reviewer` 에이전트를 호출한다.

전달 내용:

- Step 1에서 계산한 파일 목록 (또는 `all`)
- 검사할 파일 유형: docs/, agents/, templates/

qa-reviewer가 이슈 리포트를 반환할 때까지 대기.

이슈가 **0건**이면:

```
✅ QA 완료 — 이슈 없음 (N개 파일 검사)
verify.sh는 변경 사항이 없으므로 생략합니다.
```

→ 종료.

---

### Step 3 — 자동 수정 (doc-fixer)

이슈가 1건 이상이면 `@doc-fixer` 에이전트를 호출한다.

전달 내용:

- qa-reviewer의 이슈 리포트 전체

doc-fixer가 수정 완료 리포트를 반환할 때까지 대기.

---

### Step 4 — 검증 (verify.sh)

```bash
bash .claude/scripts/verify.sh
```

결과 해석:

- 8/8 PASS → Step 5로
- FAIL 항목 존재 → 해당 항목을 최종 보고에 포함

---

### Step 5 — 최종 보고

```
## /qa 완료 보고
대상: [파일 수]개 파일
탐지된 이슈: N건
자동 수정: M건
verify.sh: 8/8 PASS

### 수동 처리 필요 항목
(qa-reviewer의 "수동 처리 필요" 목록 + verify.sh FAIL 항목)
| 파일 | 유형 | 상세 |
|------|------|------|
| ... | BROKEN_LINK | ... |
```

수동 처리 항목이 없으면 "수동 처리 항목 없음" 출력.

---

## 사용 시나리오

### 일상적인 파일 수정 후

```bash
# 파일 수정 완료 후 세션 내에서 한 번만 호출
/qa changed
```

→ 변경된 파일만 검사하므로 토큰 최소화.

### 챕터 완성도 점검

```bash
/qa 03
```

→ `@content-auditor`를 대신 호출하여 챕터 감사 리포트 출력.

### ISO 산출물 정합성 검증

```bash
/qa iso
```

→ `@iso-verifier`를 호출하여 output/ 파일 검증.

---

## 에이전트 호출 분기

| 호출 패턴                                       | 실행 에이전트                                    |
| ----------------------------------------------- | ------------------------------------------------ |
| `/qa`, `/qa changed`, `/qa all`, `/qa 파일경로` | diff-scope → qa-reviewer → doc-fixer → verify.sh |
| `/qa 00`~`/qa 08`, `/qa all-chapters`           | content-auditor                                  |
| `/qa iso`, `/qa iso changed`                    | iso-verifier                                     |

---

## 주의사항

- doc-fixer는 자동 수정 불가 항목(BROKEN_LINK, SECTION_ORDER)을 건드리지 않는다
- verify.sh FAIL이 doc-fixer 수정으로 인해 발생한 경우, 수정을 되돌리고 수동 처리 목록에 추가
- `/qa all`은 파일 수가 많아 토큰 소비가 크므로 전체 리팩토링 후에만 사용
