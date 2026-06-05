# TrustedOSS 개편 — 실행 현황 (resume용)

> 목적: 긴 세션에서 히스토리가 유실돼도 이 파일만 보면 즉시 재개 가능. 매 task 후 갱신·커밋한다.
> 최종 갱신: 2026-06-05

## 재개 방법

1. `git checkout feat/ia-kwg-revamp`
2. 계획 정독: `docs/_plan/improvement-plan.md` (승인본). 실행 규약은 그 파일 "실행 규약" 절.
3. KWG 커버리지 근거: `.claude/reference/kwg-coverage-matrix.md`
4. 아래 "다음 작업"부터 이어서 진행. 매 task는 완료 정의(DoD) 통과 시에만 완료 처리.

## 작업 브랜치

`feat/ia-kwg-revamp` (main에서 분기, task별 커밋, Co-Authored-By 트레일러 금지)

## 완료 정의(DoD) 요약

task 고유 수용 기준 + `cd website && npm run build`(ko/en) + `verify.sh` 12/12 + (UI면) 헤드리스 캡처 + (KWG면) 커버리지 100%. KO(주 로케일) 빌드는 broken link 0이어야 함.

## 진행 상태

| #   | 작업                                             | 상태     |
| --- | ------------------------------------------------ | -------- |
| 12  | 메뉴 라벨(오픈소스 관리, AI 코딩 거버넌스)       | 완료     |
| 13  | KWG 커버리지 매트릭스                            | 완료     |
| 14  | 정책 템플릿 KWG 정렬(용어 정의·사내 공개·추적성) | 완료     |
| 15  | 온보딩: 5분 빠른 시작 + 내게 맞는 시작 경로      | 완료     |
| 16  | AI 에이전트 허브 페이지                          | 완료     |
| 17  | 05-tools 통합 인덱스 + 세 기둥 cross-link        | 완료     |
| 18  | P1: 단일 출처, 검색, 매핑 정본                   | 완료     |
| 19  | 도구(onot/sbom-tools) + POSITIONING 차별화       | **다음** |

마일스톤: **P0-0(#13, #14) 완료, P0(#15, #16, #17) 완료, P1(#18) 완료**. 남음: 마무리(#19 + 최종 end-to-end 검증).

## 후속(미완) 항목

- 정책 부록 A/B·추적성 헤더 다운스트림 반영은 **#18에서 완료**(output-sample/policy, reference/samples/policy). 남은 것: 프로세스 소스 템플릿(templates/process/\*)에 가시적 추적성 헤더 note 표면화(현재 HTML 주석만). reference/samples/process는 §10 등 구버전 drift도 함께 있어 sync 워크플로로 일괄 재생성 권장.
- `00-overview/index.md` 본문 축약 보류 — 온보딩 진입은 quick-start + 랜딩 CTA + 에이전트 허브로 달성.
- **en 로케일 i18n quirk(기존)**: en 브로큰링크 체커가 상대 `.md` 링크를 slug 무시하고 경로로 해석해 false-positive 경고(현재 4건). 런타임 정상, KO 0 broken, verify 12/12. en 정합은 별도 과제.
- 기존 ko-style 잔재(07-conformance, checklist-mapping, devsecops/intro의 이모지와 가운뎃점)는 내가 건드린 라인이 아니라서 보류한다. 필요하면 별도로 정리한다.

## 다음 작업 (#19 마무리: 도구 큐레이션 + POSITIONING 차별화 + 최종 end-to-end)

1. 도구 3계층 큐레이션 반영(계획 §도구 선정): onot(고지문, distribution-checklist §3) + SKT sbom-tools(5.1 SBOM 생성 보완), KWG 생태계(FOSSLight/SW360/FOSSology) 배치. 작업별 "메인 1개 + 대안" 큐레이션.
2. `POSITIONING.md` 차별화 명문화 + 랜딩 "왜 KWG와 함께 TrustedOSS인가" 노출(계획 §차별화).
3. 최종 end-to-end 검증: 전 페이지 빌드(ko 0 broken), 내부 링크, 온보딩 클릭 테스트, 완전성 비평 1회(실행 규약 §9).

### #18에서 완료한 것 (참고)

- 단일 출처화: `reference/concepts/license-classification`, `reference/concepts/vulnerability-response` 정본 신설(사이드바 "개념 심화" 등록). 03-policy·04-process·05-tools/vulnerability 본문은 표 제거 후 정본 링크. 00-overview/index 비교표는 핵심 3행으로 축약 + checklist-mapping 정본 링크.
- 검색: `@easyops-cn/docusaurus-search-local` 테마 추가(language ko/en, docs와 devsecops, ai-coding, reference 인스턴스 인덱싱). ko/en search-index 생성과 navbar 검색창 렌더 확인.
- 매핑 정본: devsecops/ai-coding iso-mapping이 이미 checklist-mapping을 정본 참조 중(추가 작업 불필요).
- 정책 부록 A/B + 추적성 헤더를 output-sample/policy, reference/samples/policy에 반영.

## 핵심 결정 (drift 방지용 고정값)

- 미션: AI·도구로 OpenChain 2026(5230·18974) 관리를 쉽고 정확하게 + DevSecOps 자동화 + AI 코딩 거버넌스. 1차 대상=처음 맡은 담당자.
- 포지셔닝: KWG의 실행·자동화 레이어(경쟁 아님). CC BY 4.0 출처 표기, KWG 연계 명시.
- 상단 메뉴: 오픈소스 관리 / DevSecOps / AI 코딩 거버넌스 / 레퍼런스(유지) + 검색.
- 확정 라벨: 내게 맞는 시작 경로, 표준 요구사항 한눈에, (DevSecOps)표준 연계(18974), (AI)실전 적용.
- 디자인: 이미 구현된 Gemini 문서 look&feel 위에서. 신규 페이지/컴포넌트도 동일 시스템.
- 콘텐츠 패턴: 모든 주제 보기(무API키 데모/샘플) → 해보기(에이전트/도구 복붙) → 자동화(CI/Rules).
- 정적 데모 링크는 `pathname:///tools/<file>.html`(verify.sh가 pathname: 스킵하도록 수정됨).
- 정책/프로세스는 KWG 절 구조에 정렬 + 가치 항목은 확장으로 구분.
- 도구: 국제(syft/grype/trivy/cdxgen/OSV/Dependency-Track) + KWG생태계(FOSSLight/SW360/FOSSology) + 국내(onot 고지문, SKT sbom-tools).

## 핵심 발견·결정 로그

- #13: 산출물 세트 전체로는 KWG 거의 전 절 충족. 실제 갭 3개(용어 정의, 사내 공개 조건부, 추적성).
- #14: 정책 소스 템플릿에 부록 A(용어), 부록 B(사내 공개), 추적성 헤더 추가로 갭 해소(소스 기준).
- #15: 정적 데모는 `pathname://` 링크 + verify.sh가 이를 스킵하도록 수정. en i18n quirk 확인(ko 무관).
- #16: AI 에이전트 허브(`docs/00-overview/agents.md`) 신설.
- #17: `docs/05-tools/index.md` 신설(카테고리 link로 연결). 07-conformance에 "자동화로 확장" 분기, devsecops→AI코딩 상호 링크, checklist-mapping 라벨 "표준 요구사항 한눈에".
- #18: 단일 출처화 핵심 발견 — CVSS 대응 기한표가 04-process(KWG 기준선 Critical 1주)와 05-tools/vulnerability(운영 SLA Critical 24h)에서 값이 **달랐음**. 정본 페이지에서 "기준선 + 조직 SLA 강화안"으로 통합해 불일치 해소. 매핑 정본(#8)은 이미 두 iso-mapping이 checklist-mapping을 정본 참조 중이라 추가 작업 불필요였음. Diátaxis(#6)는 단일 출처용 reference 개념 페이지 신설로 부분 달성(개념=reference, 본문=링크).
