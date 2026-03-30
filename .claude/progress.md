# 프로젝트 진행 상황

## 로드맵

| Phase | 이름                                                  | 상태              |
| ----- | ----------------------------------------------------- | ----------------- |
| 0     | 플랫폼 기반 구축 (Docusaurus, CI/CD, 기본 구조)       | ✅ 완료           |
| 1     | 핵심 콘텐츠 작성 (docs 챕터 00~07, templates, agents) | ✅ 완료 (2026-03) |
| 2     | Agent 구축 (산출물 자동 생성 파이프라인)              | ⏳ 대기           |
| 3     | 검증 시스템 강화 (verify.sh, CI 통합)                 | ⏳ 대기           |
| 4     | 출시 및 배포 (퍼블리시, OpenChain 등록 안내)          | ⏳ 대기           |

---

## 현재 단계 — 사용자 테스트 & 버그 리포트 대응

사용자가 가이드를 직접 따라가며 실습 동작을 검증하는 단계.
오류·개선 포인트 발견 시 알려주면 즉시 수정한다.

**수정 시 체크리스트:**

1. 파일 수정 후 `bash .claude/scripts/verify.sh` — 8/8 PASS 확인
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
  - 전체 챕터(00~07) 완료 확인 섹션 및 산출물 테이블에 /reference/samples/\* 링크 추가
  - verify.sh: 절대경로 링크(/로 시작) 및 settings.local.json 예외 처리 추가
- **KWG 동등성 갭 해소** (2026-03-29, Phase 0~7):
  - Phase 0: agents/ 실행 순서 수정 (sbom-analyst→sbom-management→vulnerability)
  - Phase 1: templates 신규 4종 (contribution-process, inquiry-response, project-publication-process, appointment-template)
  - Phase 2: templates 기존 6개 수정 (3년 보관 조항, CVD §8, RACI 기여·공개·문의 행, role-definition §6 검토이력)
  - Phase 3: verify.sh 필수파일 5개 추가, validate-checklist.md 18항목화, settings.json hook 확장
  - Phase 4: agents/ 8개 CLAUDE.md 수정 (입력질문 신설·보강, 산출물 목록 확장, 연결고리 수정)
  - Phase 5: docs/ 4개 수정 (02-organization, 03-policy, 04-process, 07-conformance)
  - Phase 6: update-reference-samples.md process.md 매핑 3종 추가, website/reference/samples/process.md 3섹션 추가
  - Phase 7: verify.sh 7/7 PASS, 갭 해소 확인 완료
- **ISO 커버리지 테스트 추가** (2026-03-30):
  - `.claude/scripts/test-coverage.py` 신규 작성 — 4가지 정적 검증 (G-항목 Agent할당, output 파일 할당, mapping↔checklist 일관성, templates 파일 존재)
  - `docs/00-overview/checklist-mapping.md` G2.2·G3L.6 테이블 보완 (inquiry-response.md, contribution-process.md 누락 추가)
  - `verify.sh` 8번 항목 추가 (ISO 커버리지 정합성), 번호 표기 [1/8]~[8/8] 통일
  - 8/8 PASS 확인
