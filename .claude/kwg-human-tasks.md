# KWG 싱크 유지 — 사람이 해야 할 일

> 이 문서는 KWG 원본과 trustedoss 콘텐츠의 싱크를 유지하기 위해
> **사람이 직접 판단하고 수행해야 하는 작업**을 정리한 것입니다.
> 자동화 도구가 처리하는 부분은 포함하지 않습니다.

---

## 목차

1. [정기 작업 — 분기별](#1-정기-작업--분기별)
2. [이벤트 기반 작업 — KWG 업데이트 시](#2-이벤트-기반-작업--kwg-업데이트-시)
3. [갭 분석 후 반영 판단 기준](#3-갭-분석-후-반영-판단-기준)
4. [kwg-mapping.yaml 유지보수](#4-kwg-mappingyaml-유지보수)
5. [초기 설정 (최초 1회)](#5-초기-설정-최초-1회)
6. [체크리스트 — 분기별 싱크 작업](#6-체크리스트--분기별-싱크-작업)

---

## 1. 정기 작업 — 분기별

**주기**: 분기 1회 (1월, 4월, 7월, 10월 첫째 주)

**목적**: KWG 원본이 업데이트됐는지 확인하고, 변경이 있으면 우리 콘텐츠에 반영한다.

### 실행 순서

```bash
# Step 1: KWG 원본 파일 갱신
bash .claude/scripts/sync-kwg-reference.sh
# → 자동으로 check-kwg-drift.py 실행됨
# → 변경 없으면: "KWG 싱크 이상 없음" → 분기 작업 완료
# → 변경 있으면: "/kwg-check 실행하세요" 안내 출력
```

```
# Step 2: 변경 있을 때만
# (Claude Code 세션에서 실행)
/kwg-check
```

```bash
# Step 3: 갭 분석 후 반영 작업 완료 후
python3 .claude/scripts/check-kwg-drift.py --reset
bash .claude/scripts/verify.sh   # 8/8 PASS 확인
git commit -m "chore: KWG 싱크 반영 YYYY-QN"
```

### 소요 시간 예상

| 상황              | 소요 시간     |
| ----------------- | ------------- |
| 변경 없음         | 5분 이내      |
| 🟢 낮음 항목만    | 30분 이내     |
| 🟡 중간 항목 포함 | 1~2시간       |
| 🔴 높음 항목 포함 | 반나절 ~ 하루 |

---

## 2. 이벤트 기반 작업 — KWG 업데이트 시

KWG 공식 업데이트 알림을 받았을 때 즉시 실행한다.

### KWG 업데이트 모니터링 방법

아래 중 하나 이상 설정:

- [ ] **GitHub Watch**: https://github.com/OpenChain-Project/OpenChain-KWG → Watch → "Releases only" 또는 "All Activity"
- [ ] **RSS**: GitHub 저장소의 releases.atom 피드 구독
- [ ] **OpenChain KWG 메일링 리스트**: https://lists.openchainproject.org/g/korea-wg 가입

### 업데이트 알림 수신 후 절차

```bash
# 즉시 실행
bash .claude/scripts/sync-kwg-reference.sh
/kwg-check
```

---

## 3. 갭 분석 후 반영 판단 기준

`/kwg-check` 실행 후 출력된 갭 분석 리포트를 보고 **사람이 직접 판단**해야 하는 항목들.

### 🔴 높음 — 즉시 반영 필요

아래 경우에 해당하면 지체 없이 반영한다.

| 상황                            | 반영 방법                                |
| ------------------------------- | ---------------------------------------- |
| KWG에 새 ISO 요구사항 섹션 추가 | 해당 docs/ 챕터 + templates/ 업데이트    |
| 기존 ISO 요구사항 내용 변경     | 우리 파일의 해당 항목 수정               |
| 새 도구 추가 (KWG tools/)       | docs/05-tools/index.md 에 도구 소개 추가 |

**반영 후 반드시**:

```bash
/qa changed                       # 자동 품질 검증
bash .claude/scripts/verify.sh   # 8/8 PASS
python3 .claude/scripts/check-kwg-drift.py --reset
git commit
```

---

### 🟡 중간 — 검토 후 결정

에이전트가 "검토 필요"로 분류한 항목. **사람이 맥락을 보고 결정**한다.

#### 판단 질문

1. **이것이 ISO 자체 인증에 영향을 주는가?**
   - Yes → 반영
   - No → 건너뜀

2. **KWG가 권고 수준인가 vs 필수 수준인가?**
   - KWG 원본 파일 직접 확인: `.claude/reference/kwg/content/ko/guide/...`
   - "해야 합니다" / "shall" → 필수 → 반영
   - "권장합니다" / "should" → 선택 → 상황에 따라 결정

3. **우리 프로젝트 규모/맥락에 맞는가?**
   - 대기업 전용 항목인지 중소기업도 해당하는지 확인
   - 우리 타겟 독자(중소기업 중심)에게 맞으면 반영, 아니면 "선택 사항" 주석 추가

#### 자주 발생하는 🟡 상황

| 상황                                       | 권장 판단                             |
| ------------------------------------------ | ------------------------------------- |
| KWG 예시 추가 (우리 파일은 다른 예시 사용) | 건너뜀 (예시는 교체 불필요)           |
| KWG 도구 버전 업데이트 언급                | docs/05-tools/ 버전 정보 업데이트     |
| KWG에 새 대기업 전용 항목 추가             | "선택 사항" 주석으로 우리 파일에 추가 |
| KWG ISO 섹션 번호 재조정 (내용은 동일)     | kwg-mapping.yaml만 업데이트           |

---

### 🟢 낮음 — 대부분 건너뜀 가능

에이전트가 "표현 변경" 또는 "이미 반영됨"으로 분류한 항목.
특별한 이유가 없으면 반영하지 않는다.

---

## 4. kwg-mapping.yaml 유지보수

`.claude/reference/kwg-mapping.yaml` 은 자동 업데이트되지 않는다.
아래 상황에서 **사람이 직접** 수정해야 한다.

### 수정 필요 상황 1: KWG에 새 가이드 파일 추가

예: `opensource_for_enterprise/7-ai-policy/` 추가됨

```yaml
# kwg-mapping.yaml의 guide_mappings에 추가
- id: guide-ai-policy
  kwg_file: 'content/ko/guide/opensource_for_enterprise/7-ai-policy/_index.md'
  our_files:
    - 'docs/09-ai-policy/index.md' # 또는 기존 챕터에 통합
  description: 'AI 코드 생성 오픈소스 정책'
  watch_for:
    - 'AI 생성 코드 라이선스 처리 방법 변경'
```

### 수정 필요 상황 2: KWG에 새 도구 추가

예: `tools/8-grype/` 추가됨

```yaml
# kwg-mapping.yaml의 tools_dimension 수정
tools_dimension:
  expected_tool_count: 8 # 7 → 8 로 변경
  known_tools:
    # ... 기존 7개 유지 ...
    - dir: '8-grype'
      name: 'Grype'
      our_coverage: 'docs/05-tools/index.md'
```

### 수정 필요 상황 3: 새 ISO 섹션 번호 발견

예: KWG 파일에서 `3.7.1` 발견됨

```yaml
# kwg-mapping.yaml의 iso_section_mapping에 추가
- kwg_sections: ['3.7']
  our_g_items: ['G5.1'] # 우리 G항목 체계 확장 필요 시
  standard: '5230'
  description: '새 요구사항 설명'
```

**이 경우 추가로 필요한 작업**:

- `docs/00-overview/checklist-mapping.md` 에 새 G항목 추가
- `agents/07-conformance-preparer/CLAUDE.md` 업데이트
- `.claude/skills/validate-checklist.md` 업데이트
- `bash .claude/scripts/verify.sh` 재실행

### 수정이 필요하지 않은 상황

| 상황                             | 이유                                        |
| -------------------------------- | ------------------------------------------- |
| KWG 파일 내용만 수정 (구조 동일) | check-kwg-drift.py가 헤딩/ISO 섹션으로 감지 |
| KWG 이미지 파일 추가             | 이미지는 동기화 대상 아님                   |
| KWG 오타 수정                    | 낮은 우선순위, 건너뜀                       |

---

## 5. 초기 설정 (최초 1회)

처음 이 시스템을 셋업할 때 한 번만 수행하는 작업.

```bash
# 1. KWG 파일 다운로드
bash .claude/scripts/sync-kwg-reference.sh
# → 첫 실행이므로 "기준 스냅샷 저장 완료" 출력

# 2. 스냅샷 기준점 확인
ls .claude/reference/kwg/.sync-snapshot/
# headings.json, iso_sections.json, tools.json, file_hashes.json 생성됨 확인

# 3. PyYAML 설치 여부 확인
python3 -c "import yaml; print('OK')"
# 없으면: pip3 install pyyaml
```

**초기 설정 완료 기준**:

- `.claude/reference/kwg/` 에 20개 md 파일 존재
- `.claude/reference/kwg/.sync-snapshot/` 에 스냅샷 파일 4개 존재
- `python3 .claude/scripts/check-kwg-drift.py` 실행 시 "싱크 OK" 출력

---

## 6. 체크리스트 — 분기별 싱크 작업

매 분기 이 체크리스트를 복사해서 사용한다.

```
분기: YYYY-QN (예: 2026-Q2)
실행일: YYYY-MM-DD
담당자:

[ ] sync-kwg-reference.sh 실행
    결과: 다운로드 __개, 오류 __건

[ ] 드리프트 감지 결과 확인
    [ ] 변경 없음 → 완료 (아래 항목 건너뜀)
    [ ] 변경 있음 → /kwg-check 실행

[ ] /kwg-check 갭 분석 결과
    🔴 높음 항목: __건
    🟡 중간 항목: __건
    🟢 낮음 항목: __건

[ ] 🔴 항목 반영 완료
    반영한 파일:
    -
    -

[ ] 🟡 항목 판단 및 처리
    반영:
    건너뜀:

[ ] kwg-mapping.yaml 업데이트 (해당 시)
    수정 내용:

[ ] /qa changed 실행 → 자동 품질 검증
[ ] bash .claude/scripts/verify.sh → 8/8 PASS
[ ] python3 .claude/scripts/check-kwg-drift.py --reset → 기준점 재설정
[ ] git commit -m "chore: KWG 싱크 반영 YYYY-QN"

완료 시각:
특이사항:
```

---

## 빠른 참조

| 작업               | 명령                                                 |
| ------------------ | ---------------------------------------------------- |
| KWG 파일 갱신      | `bash .claude/scripts/sync-kwg-reference.sh`         |
| 드리프트 감지만    | `python3 .claude/scripts/check-kwg-drift.py`         |
| 갭 분석            | `/kwg-check` (Claude 세션에서)                       |
| 전체 강제 분석     | `/kwg-check full`                                    |
| 기준점 재설정      | `python3 .claude/scripts/check-kwg-drift.py --reset` |
| 품질 검증          | `bash .claude/scripts/verify.sh`                     |
| KWG 원본 직접 보기 | `.claude/reference/kwg/content/ko/guide/`            |
| 매핑 테이블 수정   | `.claude/reference/kwg-mapping.yaml`                 |
