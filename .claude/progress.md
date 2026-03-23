# 프로젝트 진행 상황

## 로드맵

| Phase | 이름 | 상태 |
|---|---|---|
| 0 | 플랫폼 기반 구축 (Docusaurus, CI/CD, 기본 구조) | ✅ 완료 |
| 1 | 핵심 콘텐츠 작성 (docs 챕터 00~07, templates, agents) | ✅ 완료 (2026-03) |
| 2 | Agent 구축 (산출물 자동 생성 파이프라인) | ⏳ 대기 |
| 3 | 검증 시스템 강화 (verify.sh, CI 통합) | ⏳ 대기 |
| 4 | 워크숍 키트 완성 (핸드아웃, 진행자 가이드) | ⏳ 대기 |
| 5 | 출시 및 배포 (퍼블리시, OpenChain 등록 안내) | ⏳ 대기 |

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
