#!/usr/bin/env bash
# samples/ 실습을 문서에 적힌 그대로 끝까지 돌려 본다 (L4).
#
# 앞 계층은 예시가 문법적으로 성립하는지만 본다. 실제로 도구를 실행해 기대한 결과가
# 나오는지는 여기서 확인한다. 2026-09 진단에서 syft·grype 버전이 어긋나 생성한 SBOM 을
# 스캔 단계가 읽지 못하는 조합이 있었는데, 문법 검사로는 잡히지 않는 종류였다.
#
# 단언은 종료 코드가 아니라 값이다. 이유가 있다. macOS 의 Docker 는 공유 목록에 없는
# 호스트 경로를 마운트하면 오류 대신 빈 디렉터리를 붙인다. 그러면 syft 는 종료 코드 0 으로
# 유효하지만 컴포넌트가 하나도 없는 SBOM 을 내놓는다. 종료 코드만 보는 검사는 이걸 통과시킨다.
# 그래서 컴포넌트 수와 특정 취약점 ID 를 직접 확인한다.
#
# 사용법:
#   bash .claude/scripts/example-e2e.sh              # 전체
#   bash .claude/scripts/example-e2e.sh --selftest   # 단언이 실제로 검출하는지 확인
#   bash .claude/scripts/example-e2e.sh --no-network # 네트워크가 필요한 항목을 건너뛴다

set -uo pipefail

# 이미지는 태그를 고정한다. latest 는 언제든 다른 것을 가리킬 수 있고,
# 이 검사는 "지금 문서대로 하면 되는가" 를 보는 것이라 재현 가능해야 한다.
SYFT_IMAGE="anchore/syft:v1.51.1"
GRYPE_IMAGE="anchore/grype:v0.118.0"
NODE_IMAGE="node:22-bookworm-slim"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

RAN=()
SKIPPED=()
FAILED=()

ok()   { RAN+=("$1"); printf '  OK   %s\n' "$1"; }
fail() { FAILED+=("$1"); printf '  FAIL %s\n' "$1"; }
skip() { SKIPPED+=("$1"); printf '  건너뜀 %s\n' "$1"; }

syft() { docker run --rm -v "$1":/project "$SYFT_IMAGE" /project "${@:2}"; }

# grype 취약점 DB 는 내려받는 데 몇 분이 걸린다. CI 에서 캐시 디렉터리를 넘겨 주면
# 컨테이너 안 DB 경로에 붙여 재사용한다. 비어 있으면 매번 새로 받는다(로컬 기본값).
grype_scan() {
  local args=(--rm -i)
  if [ -n "${GRYPE_DB_CACHE:-}" ]; then
    mkdir -p "$GRYPE_DB_CACHE"
    args+=(-v "$GRYPE_DB_CACHE":/grype-db -e GRYPE_DB_CACHE_DIR=/grype-db)
  fi
  docker run "${args[@]}" "$GRYPE_IMAGE" "$@"
}

# SBOM 의 컴포넌트 수를 센다. 파일 자체가 없거나 JSON 이 아니면 -1 을 돌려
# "0개 탐지" 와 "생성 실패" 를 구분한다.
components() {
  [ -s "$1" ] || { echo -1; return; }
  jq -r '.components | length' "$1" 2>/dev/null || echo -1
}

require_tools() {
  local missing=0
  for t in docker jq; do
    command -v "$t" >/dev/null 2>&1 || { printf '  필요한 도구가 없다: %s\n' "$t"; missing=1; }
  done
  docker info >/dev/null 2>&1 || { printf '  docker 데몬이 돌지 않는다\n'; missing=1; }
  return $missing
}

# 샘플 하나에 대해 SBOM 을 만들고 컴포넌트 수가 기준 이상인지 본다.
# 만든 경로는 SBOM_PATH 로 돌려준다. 명령 치환으로 받으면 ok() 출력까지 섞인다.
SBOM_PATH=""
check_sbom() {
  local name="$1" min="$2" out="$WORK/$1.cdx.json"
  SBOM_PATH=""
  syft "$ROOT/samples/$name" --output cyclonedx-json > "$out" 2>/dev/null
  local n; n=$(components "$out")
  if [ "$n" -lt 0 ]; then
    fail "$name SBOM 생성 (파일이 비었거나 JSON 이 아니다)"
    return 1
  fi
  if [ "$n" -lt "$min" ]; then
    # 빈 디렉터리를 마운트했을 때 정확히 이 모양이 된다. 위 주석 참조.
    fail "$name 컴포넌트 $n 개 (기대 $min 개 이상). 마운트가 비었는지 확인하라"
    return 1
  fi
  ok "$name 컴포넌트 $n 개 (기대 $min 개 이상)"
  SBOM_PATH="$out"
}

main_run() {
  printf '[예제 E2E] syft %s / grype %s\n' "$SYFT_IMAGE" "$GRYPE_IMAGE"

  # 1. java: 컴포넌트와 Log4Shell 탐지
  local java_sbom
  if check_sbom java-vulnerable 4; then
    java_sbom="$SBOM_PATH"
    # 생성한 SBOM 을 스캔 도구가 실제로 읽는지 본다. 버전이 어긋나면
    # "sbom format not recognized" 로 여기서 걸린다.
    local scan="$WORK/java.scan.json"
    if grype_scan -o json < "$java_sbom" > "$scan" 2>/dev/null \
       && [ -s "$scan" ]; then
      ok "java SBOM 을 grype 가 파싱함"
      if jq -e '[.matches[].vulnerability.id] | index("GHSA-jfh8-c2jp-5v3q")' \
           "$scan" >/dev/null 2>&1; then
        ok "java 스캔에 Log4Shell(GHSA-jfh8-c2jp-5v3q) 포함"
      else
        fail "java 스캔에 Log4Shell(GHSA-jfh8-c2jp-5v3q) 없음"
      fi
    else
      fail "java SBOM 을 grype 가 읽지 못함 (버전 조합 확인)"
    fi
  fi

  # 2. python: 컴포넌트만 본다. 라이선스 필드는 비어 있는 것이 정상이고
  #    README 도 그렇게 적고 있다.
  check_sbom python-mixed-license 5

  # 3. nodejs: README 가 npm install 선행을 요구한다. 설치 전에는 컴포넌트가 0 이므로
  #    설치까지 해야 이 샘플의 실습이 재현된다.
  if [ "${NO_NETWORK:-0}" = "1" ]; then
    skip "nodejs 실습 (--no-network)"
  else
    local proj="$WORK/nodejs"
    cp -R "$ROOT/samples/nodejs-unlicensed" "$proj"
    if docker run --rm -v "$proj":/app -w /app "$NODE_IMAGE" \
         npm install --no-audit --no-fund >/dev/null 2>&1; then
      ok "nodejs 의존성 설치"
      local out="$WORK/nodejs.cdx.json"
      syft "$proj" --output cyclonedx-json > "$out" 2>/dev/null
      local n; n=$(components "$out")
      if [ "$n" -gt 0 ]; then
        ok "nodejs 컴포넌트 $n 개 (설치 후)"
      else
        fail "nodejs 컴포넌트 $n 개 (설치 후 0 개는 실습이 성립하지 않는다)"
      fi
      # 이 샘플의 학습 지점. 로컬 vendor 패키지에 license 필드가 없어야 한다.
      if jq -e '.license == null' "$proj/vendor/legacy-parser/package.json" >/dev/null 2>&1; then
        ok "vendor/legacy-parser 에 license 필드 없음 (README 전제와 일치)"
      else
        fail "vendor/legacy-parser 에 license 필드가 생겼다. README 전제가 깨진다"
      fi
    else
      fail "nodejs 의존성 설치 실패"
    fi
  fi
}

# 단언이 정말 검출하는지 확인한다. 빈 디렉터리를 스캔해 "컴포넌트 0" 이 실패로
# 판정되는지 본다. 이걸 통과시키면 마운트가 비어도 초록이 나온다는 뜻이다.
selftest() {
  printf '[셀프테스트] 빈 입력이 실패로 판정되는지 확인한다\n'
  local empty="$WORK/empty"; mkdir -p "$empty"
  local out="$WORK/empty.cdx.json"
  syft "$empty" --output cyclonedx-json > "$out" 2>/dev/null
  local n; n=$(components "$out")
  if [ "$n" -le 0 ]; then
    printf '  OK   빈 디렉터리 -> 컴포넌트 %s 개로 집계됨 (단언이 걸러낸다)\n' "$n"
  else
    printf '  FAIL 빈 디렉터리에서 컴포넌트 %s 개가 나왔다. 집계가 잘못됐다\n' "$n"
    return 1
  fi
  # 없는 파일에 대해 -1 을 돌려 "생성 실패" 와 "0개 탐지" 를 구분하는지
  local missing; missing=$(components "$WORK/does-not-exist.json")
  if [ "$missing" -eq -1 ]; then
    printf '  OK   파일 없음 -> -1 (생성 실패와 0개 탐지를 구분한다)\n'
  else
    printf '  FAIL 파일이 없는데 %s 를 돌려줬다\n' "$missing"
    return 1
  fi
  return 0
}

NO_NETWORK=0
MODE=run
for arg in "$@"; do
  case "$arg" in
    --selftest) MODE=selftest ;;
    --no-network) NO_NETWORK=1 ;;
    *) printf '알 수 없는 인자: %s\n' "$arg"; exit 2 ;;
  esac
done
export NO_NETWORK

if ! require_tools; then
  printf 'FAIL: 필요한 도구를 갖추지 못해 아무것도 확인하지 못했다\n'
  exit 1
fi

if [ "$MODE" = selftest ]; then
  selftest; exit $?
fi

main_run

printf '\n[결과] 통과 %d / 실패 %d / 건너뜀 %d\n' \
  "${#RAN[@]}" "${#FAILED[@]}" "${#SKIPPED[@]}"
for s in "${SKIPPED[@]:-}"; do [ -n "$s" ] && printf '  건너뜀: %s\n' "$s"; done
for f in "${FAILED[@]:-}"; do [ -n "$f" ] && printf '  실패: %s\n' "$f"; done

# 아무것도 돌리지 못했으면 통과로 세지 않는다. K18 에서 겪은 실패 유형이다.
if [ "${#RAN[@]}" -eq 0 ]; then
  printf 'FAIL: 확인한 항목이 하나도 없다\n'
  exit 1
fi
[ "${#FAILED[@]}" -eq 0 ] || exit 1
printf 'PASS: 문서대로 실습이 재현된다\n'
