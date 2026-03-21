# docs/ — 공통 규칙 및 안내

## docs/ 전체에 적용되는 공통 규칙

이 디렉토리는 trustedoss의 모든 챕터 문서가 위치하는 곳이다.
각 챕터는 독립적인 하위 디렉토리로 구성되며, 00번부터 07번까지 순서대로 진행한다.

## create-doc skill 적용

docs/ 하위 모든 문서는 `.claude/skills/create-doc.md` 에 정의된 표준을 따른다.

- 문서 상단에 메타 블록 포함 (작성일, 버전, 충족 체크리스트, 소요시간)
- 섹션 순서 준수: 이 챕터에서 하는 일 → 배경 지식 → 셀프스터디 경로 → 워크숍 경로 → 완료 확인 → 다음 단계
- 체크리스트 항목 참조 시 `> 이 단계는 ISO/IEC 5230 [항목ID] 요구사항을 충족합니다.` 형식 사용

## 두 가지 사용 경로

### 셀프스터디 경로
- docs/ 챕터를 00부터 순서대로 읽고 실습한다
- 각 챕터마다 충분한 시간을 갖고 배경 지식을 이해하며 진행한다
- 예상 전체 소요시간: 8~12시간 (모든 챕터 합산)

### 워크숍 경로
- `workshop/student-handout.md` 를 따라 진행한다
- M0~M6 모듈로 구성되며 총 약 6시간 소요
- 각 모듈은 시간 제한이 있으므로 핵심 단계에 집중한다

## 산출물 저장 위치

모든 실습 산출물은 `output/` 디렉토리에 저장된다.
`output/` 는 .gitignore 에 포함되어 있어 버전 관리 대상이 아니다.

```
output/
├── organization/   # 02-organization 챕터 산출물
├── policy/         # 03-policy 챕터 산출물
├── process/        # 04-process 챕터 산출물
├── sbom/           # 05-tools 챕터 산출물
├── vulnerability/  # 05-tools/vulnerability 산출물
├── training/       # 06-training 챕터 산출물
├── conformance/    # 07-conformance 챕터 산출물
└── progress.md     # 전체 진행 상황 추적
```

## 막혔을 때

각 챕터 디렉토리로 이동하면 해당 폴더의 CLAUDE.md 가 세부 맥락을 제공한다.
Agent를 활용하면 산출물을 자동으로 생성할 수 있다.

```bash
# 예시: 조직 설계 agent 실행
cd agents/02-organization-designer
claude
```
