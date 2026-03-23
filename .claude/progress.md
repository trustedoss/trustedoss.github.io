# 프로젝트 진행 상황

## 로드맵

| Phase | 이름 | 상태 |
|---|---|---|
| 0 | 플랫폼 기반 구축 (Docusaurus, CI/CD, 기본 구조) | ✅ 완료 |
| 1 | 핵심 콘텐츠 작성 (docs 챕터 00~07, templates, agents) | ✅ 완료 (2026-03) |
| 2 | Agent 구축 (산출물 자동 생성 파이프라인) | ⏳ 대기 |
| 3 | 검증 시스템 강화 (verify.sh, CI 통합) | ⏳ 대기 |
| 4 | 출시 및 배포 (퍼블리시, OpenChain 등록 안내) | ⏳ 대기 |

---

## 현재 단계 — 사용자 테스트 & 버그 리포트 대응

사용자가 가이드를 직접 따라가며 실습 동작을 검증하는 단계.
오류·개선 포인트 발견 시 알려주면 즉시 수정한다.

**수정 시 체크리스트:**
1. 파일 수정 후 `bash .claude/scripts/verify.sh` — 6/6 PASS 확인
2. `git commit`

---

## 완료된 주요 작업 이력 (요약)

- **Phase 0** (지시 A~D): Docusaurus + Yarn 4 플랫폼, CI/CD, self check 스크립트
- **Phase 1** (지시 E~O):
  - docs 챕터 00~07 콘텐츠 완성 (배경지식, 실습 블록, 완료 체크리스트)
  - agents/ 9개 CLAUDE.md 작성
  - templates/ 11개 산출물 템플릿 작성
  - validate-checklist skill (17항목), verify.sh 6항목 체크
  - 입증자료 50개 전체 checklist-mapping.md 매핑
  - 챕터별 :::info 충족되는 표준 요구사항 블록 추가 (03-policy 기준)
  - README.md 저장소 구조 안내 추가
  - docs 챕터 02/03/04/06 셀프스터디 경로에 `:::details` Agent 대화 예시 블록 추가
  - website/reference/samples/ 산출물 Best Practice 5종 생성 (organization, policy, process, training, conformance) — 규모별 3 프로필 (스타트업/중소기업/대기업)
  - website/reference/intro.md 및 sidebarsReference.ts 업데이트
  - docs/intro.md 챕터 05 테이블 3행 → 1행("05 도구") 병합
  - 전체 챕터 "셀프스터디 경로" 섹션 제목 → "셀프 스터디"로 통일 (11개 파일)
  - docs/06-training: `시작` 입력 안내를 bash block 직후로 이동
  - docs/05-tools/vulnerability + agents/05-vulnerability-analyst: 다음 단계 `시작` 안내 추가
  - website/reference/samples/sbom.md, vulnerability.md 신규 생성 (Best Practice, 렌더링 마크다운)
  - sidebarsReference.ts에 sbom, vulnerability 항목 추가
  - 전체 챕터(00~07) 완료 확인 섹션 및 산출물 테이블에 /reference/samples/* 링크 추가
  - verify.sh: 절대경로 링크(/로 시작) 및 settings.local.json 예외 처리 추가
