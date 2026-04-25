#!/usr/bin/env bash
# dry-run/run-dryrun.sh
#
# OpenWave 스타트업 프로필 기준 agent 체인 드라이런.
# Anthropic API를 사용해 각 agent를 실제 실행하고 출력을 검증한다.
#
# 사용법:
#   bash dry-run/run-dryrun.sh              # 전체 실행 (OpenWave 프로필)
#   bash dry-run/run-dryrun.sh --chain-only # 체인 연결 검증만 (API 호출 없음)
#   bash dry-run/run-dryrun.sh --agent 05-sbom-guide  # 특정 agent만
#
# 환경변수:
#   ANTHROPIC_API_KEY  (--chain-only 제외 시 필수)

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FIXTURES_DIR="$REPO_ROOT/tests/fixtures"
SCRIPTS_DIR="$REPO_ROOT/.claude/scripts"

# OpenWave 프로필 기준 fixture 파일 매핑
# 형식: "agent이름:fixture파일명"
FIXTURE_PAIRS=(
  "02-organization-designer:02-organization-designer.json"
  "03-policy-generator:03-policy-generator.json"
  "04-process-designer:04-process-designer-openwave.json"
  "05-sbom-guide:05-sbom-guide.json"
  "05-sbom-analyst:05-sbom-analyst.json"
  "05-sbom-management:05-sbom-management-openwave.json"
  "05-vulnerability-analyst:05-vulnerability-analyst.json"
  "06-training-manager:06-training-manager.json"
  "07-conformance-preparer:07-conformance-preparer.json"
)

AGENT_ORDER=(
  "02-organization-designer"
  "03-policy-generator"
  "04-process-designer"
  "05-sbom-guide"
  "05-sbom-analyst"
  "05-sbom-management"
  "05-vulnerability-analyst"
  "06-training-manager"
  "07-conformance-preparer"
)

# agent 이름으로 fixture 파일명 조회
get_fixture() {
  local agent="$1"
  for pair in "${FIXTURE_PAIRS[@]}"; do
    local key="${pair%%:*}"
    local val="${pair##*:}"
    if [[ "$key" == "$agent" ]]; then
      echo "$val"
      return
    fi
  done
}

# ── 인수 파싱 ─────────────────────────────────────────────
CHAIN_ONLY=false
AGENT_FILTER=""
VERBOSE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --chain-only) CHAIN_ONLY=true ;;
    --agent) AGENT_FILTER="$2"; shift ;;
    -v|--verbose) VERBOSE="-v" ;;
    *) echo "알 수 없는 옵션: $1"; exit 1 ;;
  esac
  shift
done

# ── 체인 연결 검증만 실행 ──────────────────────────────────
if [[ "$CHAIN_ONLY" == "true" ]]; then
  echo "===== 체인 연결 검증 (output-sample/ 기준) ====="
  python3 "$SCRIPTS_DIR/validate-chain.py" --dir output-sample $VERBOSE
  exit $?
fi

# ── API 키 확인 ───────────────────────────────────────────
if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "ERROR: ANTHROPIC_API_KEY 환경변수를 설정하세요."
  echo "  export ANTHROPIC_API_KEY=sk-..."
  echo ""
  echo "API 호출 없이 체인 연결만 검증하려면:"
  echo "  bash dry-run/run-dryrun.sh --chain-only"
  exit 1
fi

# ── 실행 대상 결정 ────────────────────────────────────────
if [[ -n "$AGENT_FILTER" ]]; then
  TARGETS=("$AGENT_FILTER")
else
  TARGETS=("${AGENT_ORDER[@]}")
fi

# ── 드라이런 실행 ─────────────────────────────────────────
echo "===== OpenWave 드라이런 ====="
echo "프로필: 오픈웨이브(OpenWave) SaaS · Python/pip · GitHub Actions · 2주 배포"
echo "대상  : ${TARGETS[*]}"
echo ""

PASS=0
FAIL=0
RESULTS=()

for agent in "${TARGETS[@]}"; do
  fixture_file="$(get_fixture "$agent")"
  if [[ -z "$fixture_file" ]]; then
    echo "  SKIP: $agent (fixture 없음)"
    continue
  fi

  fixture_path="$FIXTURES_DIR/$fixture_file"
  if [[ ! -f "$fixture_path" ]]; then
    echo "  SKIP: $agent (fixture 파일 없음: $fixture_file)"
    continue
  fi

  echo "──────────────────────────────────────────"
  echo "  실행: $agent"
  echo "  fixture: $fixture_file"

  if python3 "$SCRIPTS_DIR/test-agent-e2e.py" \
       --fixture "$fixture_path" $VERBOSE; then
    PASS=$((PASS + 1))
    RESULTS+=("PASS: $agent ($fixture_file)")
  else
    FAIL=$((FAIL + 1))
    RESULTS+=("FAIL: $agent ($fixture_file)")
  fi
  echo ""
done

# ── 체인 연결 추가 검증 ───────────────────────────────────
echo "──────────────────────────────────────────"
echo "  체인 연결 검증 (output-sample/ 기준)"
if python3 "$SCRIPTS_DIR/validate-chain.py" --dir output-sample $VERBOSE; then
  RESULTS+=("PASS: 체인 연결 검증")
else
  FAIL=$((FAIL + 1))
  RESULTS+=("FAIL: 체인 연결 검증")
fi

# ── 결과 요약 ─────────────────────────────────────────────
echo ""
echo "=========================================="
echo "===== 드라이런 결과 ====="
for r in "${RESULTS[@]}"; do
  echo "  $r"
done
echo ""
echo "PASS: $PASS  /  FAIL: $FAIL"
echo "=========================================="

[[ $FAIL -eq 0 ]]
