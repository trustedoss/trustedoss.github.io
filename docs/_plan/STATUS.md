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

task 고유 수용 기준 + `cd website && npm run build`(ko/en) + `verify.sh` 12/12 + (UI면) 헤드리스 캡처 + (KWG면) 커버리지 100%. 단계 종료 전 독립 검증(quality-gate/code-review/doc-qa).

## 진행 상태

| #   | 작업                                             | 상태     |
| --- | ------------------------------------------------ | -------- |
| 12  | 메뉴 라벨(오픈소스 관리, AI 코딩 거버넌스)       | 완료     |
| 13  | KWG 커버리지 매트릭스                            | 완료     |
| 14  | 정책 템플릿 KWG 정렬(용어 정의·사내 공개·추적성) | 완료     |
| 15  | 온보딩: 5분 빠른 시작 + 내게 맞는 시작 경로      | **다음** |
| 16  | AI 에이전트 허브 페이지                          | 대기     |
| 17  | 05-tools 통합 인덱스 + 세 기둥 cross-link        | 대기     |
| 18  | P1: 단일출처·Diátaxis·검색·매핑정본              | 대기     |
| 19  | 도구(onot/sbom-tools) + POSITIONING 차별화       | 대기     |

마일스톤: **P0-0(#13+#14) 완료** / P0 = #15~#17 / P1 = #18 / 마무리 = #19 + 최종 end-to-end 검증.

## 후속(미완) 항목

- 정책 템플릿(#14)에 추가한 부록 A(용어 정의)·부록 B(사내 공개)·추적성 헤더를 **다운스트림 샘플에 반영**: `output-sample/policy/oss-policy.md`와 `website/reference/samples/policy.md`. (소스 템플릿만 우선 반영함. 샘플은 `update-reference-samples`/sync 워크플로로 재생성 예정 — #18 또는 별도 동기화 시.)
- 프로세스 템플릿(04-process)도 같은 추적성 헤더 적용 검토(#14 후속).

## 다음 작업 (#15 온보딩)

1. `docs/00-overview/quick-start.md` 신설(5분: 이게 뭔가 / 언제 / 지금 해보기 + "지금 체험"=무API키 데모, "내 것 만들기"=첫 에이전트).
2. "내게 맞는 시작 경로" 진입(3분기: 인증만 / 개발팀과 함께 / 이미 정책 있음).
3. `00-overview/index.md` 본문 축약, `sidebars.ts` "시작하기"에 신규 항목 추가.
4. 랜딩 1차 CTA "처음이세요? 5분 시작". build/verify/캡처.

## 핵심 결정 (drift 방지용 고정값)

- 미션: AI·도구로 OpenChain 2026(5230·18974) 관리를 쉽고 정확하게 + DevSecOps 자동화 + AI 코딩 거버넌스. 1차 대상=처음 맡은 담당자.
- 포지셔닝: KWG의 실행·자동화 레이어(경쟁 아님). CC BY 4.0 출처 표기, KWG 연계 명시.
- 상단 메뉴: 오픈소스 관리 / DevSecOps / AI 코딩 거버넌스 / 레퍼런스(유지) + 검색.
- 확정 라벨: 내게 맞는 시작 경로, 표준 요구사항 한눈에, (DevSecOps)표준 연계(18974), (AI)실전 적용.
- 디자인: 이미 구현된 Gemini 문서 look&feel 위에서. 신규 페이지/컴포넌트도 동일 시스템.
- 콘텐츠 패턴: 모든 주제 보기(무API키 데모/샘플) → 해보기(에이전트/도구 복붙) → 자동화(CI/Rules).
- 정책/프로세스는 KWG 절 구조에 정렬 + 가치 항목은 확장으로 구분.
- 도구: 국제(syft/grype/trivy/cdxgen/OSV/Dependency-Track) + KWG생태계(FOSSLight/SW360/FOSSology) + 국내(onot 고지문, SKT sbom-tools).

## 핵심 발견

- #13: 산출물 세트 전체로는 KWG 거의 전 절 충족. 실제 갭 3개(용어 정의, 사내 공개 조건부, 추적성).
- #14: 정책 소스 템플릿에 용어 정의(부록 A), 사내 공개(부록 B), "KWG 정책 템플릿 §1~11 기준" 추적성 헤더 추가로 갭 해소(소스 기준). 샘플 반영은 후속.
