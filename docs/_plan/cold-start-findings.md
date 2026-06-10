# 콜드스타트 시뮬레이션 발견 보고서 — 실사용자 검증

> 실행일: 2026-06-10. 상태: 13건 전부 수정 완료, push 후 M1·M2 최종 확인만 남음. 빌드 비대상(`_plan/`).

## 처리 결과 (2026-06-10)

| 구분  | 처리                                                                                          | 커밋      |
| ----- | --------------------------------------------------------------------------------------------- | --------- |
| M1·M2 | sync-agents.yml에 samples/, output-sample/ 동기화 추가                                        | `6131729` |
| M3·M4 | quick-start 클론 안내 추가, OSV Maven 패키지명 수정 (curl 실측 재검: Log4Shell 포함 7건 반환) | `b956107` |
| m1~m9 | ko·en 쌍 수정 (cdxgen 폴백은 Docker 실측 재검: output/sbom/에 생성, components 2)             | `56da54e` |

독립 게이트(quality-gate:gate-verifier) 판정: **13/13 PASS** — ko·en 반영 여부를 항목별 grep으로
확인, OSV curl 실제 호출 확인, verify.sh 12/12, ko/en 클론 URL 불일치 잔존 0건.
M1·M2는 push 후 sync 워크플로우 완료 시점에 trustedoss-agents 새 클론으로 최종 확인한다.

게이트 검증 중 범위 밖 기존 결함 1건 발견 (후속 후보로 등록): en sbom-101.md에 번역
플레이스홀더 `__ISO13__` 4건 잔존 (2026-04-26 커밋 052d283 유입).

## 1. 방법론

사전 지식을 차단한 LLM 에이전트 2개가 실제 신규 사용자의 경로만으로 가이드를 따라갔다.
시작점은 공개 사이트 `https://trustedoss.github.io/` 하나이며, 로컬 개발 저장소 접근은
금지했다. 문서가 지시한 명령은 격리된 임시 작업 공간에서 실제로 실행했다.

| 프로필 | 설정                                          | 경로                            | 결과                 |
| ------ | --------------------------------------------- | ------------------------------- | -------------------- |
| P1     | 스타트업 담당자, OSS 경험 0, Docker 사용 불가 | 빠른 시작 + 05 Docker-없이 분기 | 완주 (우회 2회 필요) |
| P2     | 중견기업 담당자, Docker 사용 가능             | 풀코스 00→07 + 05 Docker 실경로 | 완주 (우회 2회 필요) |

agent 체인 연결은 `dry-run/run-dryrun.sh --chain-only`로 별도 검증했다 — 9개 agent 전부 PASS.

**한계**: LLM 에이전트는 사람보다 문서를 성실히 읽으므로 인지 부하·이탈 지점은 잡지
못한다. 소요 시간 약속(1~2h 등)은 검증하지 않았다. `claude` 대화형 agent의 실제 대화
품질은 범위 외다(Layer 3 E2E, API 키 필요). 이 결과는 실제 사람 테스트를 대체하지 않고,
사람 테스터에게 보여주기 전에 거를 결함을 먼저 거른 것이다.

## 2. 핵심 발견 — major 4건

두 프로필 모두 완주는 했지만, 4곳에서 문서 그대로는 진행이 막혀 우회가 필요했다.
모두 메인 루프에서 직접 재현해 확정했다.

### M1. 공개 클론 저장소에 `samples/` 미포함 — 05 실습이 조용히 빈 결과를 냄

문서(01-setup, 05-sbom-generation)가 클론하라고 안내하는 `trustedoss-agents.git`의
git 추적 경로는 `.claude, agents/, CLAUDE.md, README.md, templates/` 뿐이다.
`samples/java-vulnerable/` 등 3개 샘플 프로젝트가 없다.

- 문서 그대로 `docker run ... -v $(pwd)/samples/java-vulnerable:/project anchore/syft:latest`를
  실행하면 빈 디렉토리가 마운트되어 **에러 없이 `components: 0`인 빈 SBOM**이 생성된다.
  문서가 약속한 결과(log4j-core 2.14.1 탐지)는 재현되지 않고, 사용자는 실패 사실조차
  알기 어렵다.
- 샘플은 `trustedoss/trustedoss.github.io` 저장소에만 존재한다. P2는 README의 동기화
  출처 문구를 단서로 GitHub tarball에서 직접 받아오는 우회를 했다.

**권고**: trustedoss-agents 저장소에 samples/를 포함(동기화 스크립트 확장)하거나,
05 문서에 샘플 입수 명령(별도 클론 또는 다운로드)을 명시한다.

### M2. 공개 클론 저장소에 `output-sample/` 미포함 — Docker-없이 대체 경로가 막힘

05-sbom-generation의 "Docker 없이 진행하는 경우" 분기가 지시하는
`cp output-sample/sbom/fixture-sample.cdx.json output/sbom/`이
`No such file or directory`로 실패한다. Docker를 못 쓰는 독자를 위한 공식 대체 경로
자체가 막혀 있다. P1은 사이트를 뒤져 `/samples/fixture-sample.cdx.json` 다운로드
링크(정상 200, 유효한 CycloneDX, 컴포넌트 5개)를 찾아 우회했지만, 이 링크는 해당
분기에서 연결되지 않는다.

**권고**: 분기 명령을 `curl -o output/sbom/fixture-sample.cdx.json https://trustedoss.github.io/samples/fixture-sample.cdx.json`
류로 교체하거나, output-sample/을 agents 저장소에 포함한다.

### M3. 빠른 시작이 클론 안내 없이 `cd agents/...` 제시

quick-start §2가 `cd agents/02-organization-designer && claude`를 제시하지만, 이
페이지에는 저장소 클론 안내가 없다. 콜드스타트 사용자가 그대로 실행하면
`No such file or directory`. 클론 안내는 "다음 단계"의 환경 준비 링크를 따라가야 나온다.

**권고**: 명령 직전에 클론 선행 안내 한 줄(또는 클론 명령 자체)을 추가한다.

### M4. OSV API 예시 명령이 빈 결과를 반환 — Maven 패키지명 형식 오류

05-tools/vulnerability/tools-setup의 curl 예시가 `"name": "log4j-core"`를 쓰는데,
OSV의 Maven 생태계는 `groupId:artifactId` 형식이 필요하다. 문서 명령 그대로는 응답이
`{}`(취약점 0건)이고, `org.apache.logging.log4j:log4j-core`로 바꾸면 Log4Shell 포함
7건이 반환된다 (메인 루프에서 재현 확정).

**권고**: 예시의 name을 `org.apache.logging.log4j:log4j-core`로 수정한다.

## 3. minor 9건 — 혼란 유발

| #   | 위치                                 | 내용                                                                                                                         | 권고                                                                       |
| --- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| m1  | 01-setup 도구 표                     | Docker가 "필수"로 표기되나 바로 아래 콜아웃은 "05에서만 사용, 대체 경로 있음"                                                | 표를 "챕터 05만 필요(대체 경로 있음)"로 일치                               |
| m2  | 01-setup 완료 체크리스트             | 첫 항목 `docker --version`에 Docker 미사용 경로 예외 단서 없음 — 해당 독자는 영구 미완료로 인식                              | "(Docker 미사용 시 생략)" 단서                                             |
| m3  | quick-start 첫 문단                  | "OpenChain 2026", "자체 인증 선언"이 풀이 없이 등장 (SBOM은 풀이 있음)                                                       | 인라인 풀이 또는 용어집 링크                                               |
| m4  | 05-sbom-generation 예상 결과         | "Apache-2.0 라이선스 식별" 약속하나 syft/cdxgen 실제 출력의 licenses 필드는 빈 값 (샘플 pom.xml에 license 선언 없음)         | 라이선스 식별이 분석 agent 단계 몫임을 명시하거나 샘플에 license 선언 추가 |
| m5  | 05-tools/vulnerability 예시 로그     | "컴포넌트 12개 발견" 예시 vs 동일 샘플 실제 2~4개                                                                            | 예시 수치를 실측과 일치                                                    |
| m6  | 05-sbom-generation cdxgen 폴백       | 폴백 출력이 샘플 폴더 내부에 생성되어 완료 확인 `ls output/sbom/*.cdx.json`과 불일치                                         | 출력 경로 통일 또는 위치 차이 안내                                         |
| m7  | docker-cicd 트러블슈팅               | 파일 공유 제한 환경(colima 등)에서 빈 마운트 → 에러 없는 빈 SBOM. 기존 표("lock 파일 없음")가 원인을 잘못 짚게 함            | "마운트가 비어 보일 때 파일 공유 설정 확인" 항목 추가                      |
| m8  | 05-tools 개요                        | 취약점 도구로 grype 언급하나 챕터 내 grype 실행 명령 없음 (실제는 OSV·Dependency Track)                                      | 개요 도구 목록을 실습 도구와 일치                                          |
| m9  | quick-start·01-setup의 02 agent 지점 | 웹 문서가 "끝나면 무엇을 확인하는지"(output/organization/ 3개 파일)를 안 알려줌 — 그 정보는 클론 후 agent CLAUDE.md에만 있음 | 완료 확인 한 줄(ls 명령) 추가                                              |

## 4. 잘 작동한 것

- 클론 URL이 정확해 두 프로필 모두 한 번에 클론에 성공했다. agents/ 9개 폴더의
  CLAUDE.md가 예상 소요 시간, 질문 목록, 산출물 파일명, 완료 확인 명령까지 제공한다.
- 챕터 구조가 일관적("하는 일 → 배경 → 셀프스터디 → 완료 확인 → 다음 단계")이라
  콜드스타트 독자도 다음 행동을 헤매지 않았다. "현재 Claude 세션 종료 후 실행" 안내가
  매번 반복되어 함정을 방지한다.
- 무설치 데모, 샘플 SBOM 다운로드, Best Practice 샘플 5종, OpenChain 등록 URL이 모두
  정상(200)이고 내용도 약속과 일치했다.
- agent 체인 연결 검증(dry-run --chain-only) 9/9 PASS.

## 5. 후속 권고 우선순위

1. **M1·M2 (클론 저장소 구성)** — 05 챕터의 실습 두 경로(Docker 실경로, Docker-없이)가
   모두 문서 그대로는 실패한다. 가장 영향이 크고, trustedoss-agents 동기화 범위 결정이
   필요하다.
2. **M3·M4 (문서 한 줄 수정)** — 비용이 작고 효과가 분명하다.
3. **minor 9건** — 대부분 문서 한 줄 수정. m4·m5는 실측 수치 기준으로 고친다.
