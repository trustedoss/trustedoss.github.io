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
| 17  | 05-tools 통합 인덱스 + 세 기둥 cross-link        | **다음** |
| 18  | P1: 단일출처·Diátaxis·검색·매핑정본              | 대기     |
| 19  | 도구(onot/sbom-tools) + POSITIONING 차별화       | 대기     |

마일스톤: **P0-0(#13+#14) 완료** / P0 = #15·#16 완료, #17 남음 / P1 = #18 / 마무리 = #19 + 최종 end-to-end 검증.

## 후속(미완) 항목

- 정책 템플릿(#14) 부록 A/B·추적성 헤더를 다운스트림 샘플(`output-sample/policy`, `website/reference/samples/policy`)에 반영 + 프로세스 템플릿 추적성 헤더. (#18 또는 sync 시)
- `00-overview/index.md` 본문 축약 보류 — 온보딩 진입은 quick-start + 랜딩 CTA + 에이전트 허브로 달성. index 축약은 별도 콘텐츠 작업.
- **en 로케일 i18n quirk(기존)**: en 브로큰링크 체커가 상대 `.md` 링크를 slug 무시하고 경로로 해석해 false-positive 경고(현재 3건). 런타임은 정상, KO 0 broken, verify 12/12. en 정합은 별도 과제.
- checklist-mapping 사이드바 라벨을 "표준 요구사항 한눈에"로 변경(#17 사이드바 정리 시).

## 다음 작업 (#17 05-tools 통합 + 세 기둥 cross-link)

1. `docs/05-tools/index.md` 신설: SBOM 생성 → 관리 → 취약점 흐름 + 통합 에이전트 안내. 사이드바 5번 카테고리에 index 추가.
2. `docs/07-conformance/index.md` 끝에 "다음: 자동화로 확장(DevSecOps / AI 코딩 거버넌스)" 분기 추가.
3. DevSecOps↔AI코딩 상호 링크 보강(현재 고립). checklist-mapping 사이드바 라벨 "표준 요구사항 한눈에"로.
4. build(ko 0 broken)/verify 12/12/캡처.

## 핵심 결정 (drift 방지용 고정값)

- 미션: AI·도구로 OpenChain 2026(5230·18974) 관리를 쉽고 정확하게 + DevSecOps 자동화 + AI 코딩 거버넌스. 1차 대상=처음 맡은 담당자.
- 포지셔닝: KWG의 실행·자동화 레이어(경쟁 아님). CC BY 4.0 출처 표기, KWG 연계 명시.
- 상단 메뉴: 오픈소스 관리 / DevSecOps / AI 코딩 거버넌스 / 레퍼런스(유지) + 검색.
- 확정 라벨: 내게 맞는 시작 경로, 표준 요구사항 한눈에, (DevSecOps)표준 연계(18974), (AI)실전 적용.
- 디자인: 이미 구현된 Gemini 문서 look&feel 위에서. 신규 페이지/컴포넌트도 동일 시스템.
- 콘텐츠 패턴: 모든 주제 보기(무API키 데모/샘플) → 해보기(에이전트/도구 복붙) → 자동화(CI/Rules).
- 정적 데모 링크는 `pathname:///tools/<file>.html` 형식(verify.sh가 pathname: 스킵하도록 수정됨).
- 정책/프로세스는 KWG 절 구조에 정렬 + 가치 항목은 확장으로 구분.
- 도구: 국제(syft/grype/trivy/cdxgen/OSV/Dependency-Track) + KWG생태계(FOSSLight/SW360/FOSSology) + 국내(onot 고지문, SKT sbom-tools).

## 핵심 발견·결정 로그

- #13: 산출물 세트 전체로는 KWG 거의 전 절 충족. 실제 갭 3개(용어 정의, 사내 공개 조건부, 추적성).
- #14: 정책 소스 템플릿에 부록 A(용어), 부록 B(사내 공개), 추적성 헤더 추가로 갭 해소(소스 기준).
- #15: 정적 데모는 `pathname://` 링크 + verify.sh가 이를 스킵하도록 수정. en i18n quirk 확인(ko 무관).
- #16: AI 에이전트 허브(`docs/00-overview/agents.md`) 신설 — 에이전트↔챕터↔산출물 매핑 한 페이지.
