#!/usr/bin/env bash
# sync-kwg-reference.sh
# OpenChain KWG 한국어 가이드 원본을 .claude/reference/kwg/ 에 동기화한다.
#
# 대상:
#   - content/ko/guide/opensource_for_enterprise/ (기업 오픈소스 관리 가이드)
#   - content/ko/guide/templates/                (정책·프로세스 템플릿)
#   - content/ko/guide/tools/                   (도구 가이드)
#
# 규칙:
#   - .md 파일만 다운로드 (PNG 등 이미지는 Claude 컨텍스트에 불필요)
#   - 원본 디렉토리 구조 유지
#   - 기존 파일이 있으면 덮어쓰기 (최신 유지)
#   - GitHub API rate limit: unauthenticated 60 req/hour
#     → GITHUB_TOKEN 환경변수 설정 시 5000 req/hour
#
# 사용:
#   bash .claude/scripts/sync-kwg-reference.sh
#   GITHUB_TOKEN=ghp_xxx bash .claude/scripts/sync-kwg-reference.sh

set -euo pipefail

OWNER="OpenChain-Project"
REPO="OpenChain-KWG"
BRANCH="master"
BASE_CONTENT_PATH="content/ko/guide"
TARGET_DIR=".claude/reference/kwg"

API_BASE="https://api.github.com/repos/${OWNER}/${REPO}/contents"
RAW_BASE="https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}"

# GitHub API 헤더 (토큰 있으면 포함)
AUTH_HEADER=""
if [ -n "${GITHUB_TOKEN:-}" ]; then
  AUTH_HEADER="-H \"Authorization: Bearer ${GITHUB_TOKEN}\""
  echo "✅ GITHUB_TOKEN 사용 (rate limit: 5000 req/hour)"
else
  echo "ℹ️  GITHUB_TOKEN 없음 (rate limit: 60 req/hour)"
  echo "   대량 실행 시 GITHUB_TOKEN=ghp_xxx bash $0 권장"
fi
echo ""

# 동기화 대상 디렉토리 목록
declare -a SYNC_DIRS=(
  "${BASE_CONTENT_PATH}/opensource_for_enterprise"
  "${BASE_CONTENT_PATH}/templates"
  "${BASE_CONTENT_PATH}/tools"
)

# 통계
DOWNLOADED=0
SKIPPED=0
ERRORS=0

# GitHub API 호출 함수
api_get() {
  local url="$1"
  if [ -n "${GITHUB_TOKEN:-}" ]; then
    curl -sf -H "Authorization: Bearer ${GITHUB_TOKEN}" \
         -H "Accept: application/vnd.github.v3+json" \
         "$url"
  else
    curl -sf -H "Accept: application/vnd.github.v3+json" "$url"
  fi
}

# md 파일 다운로드 함수 (재귀)
download_dir() {
  local remote_path="$1"
  local local_path="${TARGET_DIR}/${remote_path}"

  mkdir -p "$local_path"

  # GitHub API로 디렉토리 내 파일 목록 조회
  local api_url="${API_BASE}/${remote_path}"
  local response
  if ! response=$(api_get "$api_url" 2>/dev/null); then
    echo "  ⚠️  API 오류: ${remote_path} (rate limit 또는 경로 오류)"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # Python3으로 JSON 파싱
  local items
  items=$(python3 -c "
import sys, json
try:
    items = json.loads(sys.stdin.read())
    if not isinstance(items, list):
        sys.exit(0)
    for item in items:
        t = item.get('type', '')
        n = item.get('name', '')
        p = item.get('path', '')
        if t == 'file' and n.endswith('.md'):
            print('FILE:' + p)
        elif t == 'dir':
            print('DIR:' + p)
except Exception as e:
    sys.stderr.write(str(e))
" <<< "$response")

  while IFS= read -r line; do
    if [[ "$line" == FILE:* ]]; then
      local file_path="${line#FILE:}"
      local file_name
      file_name=$(basename "$file_path")
      local target_file="${TARGET_DIR}/${file_path}"

      # raw 콘텐츠 다운로드
      local raw_url="${RAW_BASE}/${file_path}"
      if curl -sf "$raw_url" -o "$target_file" 2>/dev/null; then
        echo "  ✅ ${file_path}"
        DOWNLOADED=$((DOWNLOADED + 1))
      else
        echo "  ❌ 실패: ${file_path}"
        ERRORS=$((ERRORS + 1))
      fi

    elif [[ "$line" == DIR:* ]]; then
      local sub_path="${line#DIR:}"
      echo "  📂 ${sub_path}/"
      download_dir "$sub_path"
    fi
  done <<< "$items"
}

# 메인 실행
echo "===== KWG 원본 가이드 동기화 시작 ====="
echo "대상: ${#SYNC_DIRS[@]}개 디렉토리"
echo "저장: ${TARGET_DIR}/"
echo ""

mkdir -p "$TARGET_DIR"

# README 생성 (첫 실행 또는 업데이트)
cat > "${TARGET_DIR}/README.md" << 'EOF'
# KWG 원본 가이드 (자동 동기화)

OpenChain Korea Work Group의 한국어 가이드 원본.
**이 폴더는 자동 생성됩니다. 직접 편집하지 마세요.**

## 갱신 방법

```bash
bash .claude/scripts/sync-kwg-reference.sh
```

## 출처

- 저장소: https://github.com/OpenChain-Project/OpenChain-KWG
- 라이선스: CC BY 4.0
- 원본 경로: content/ko/guide/

## 포함 내용

| 폴더 | 내용 |
|------|------|
| `opensource_for_enterprise/` | ISO 표준 기반 기업 오픈소스 관리 가이드 |
| `templates/` | 오픈소스 정책·프로세스 문서 템플릿 |
| `tools/` | SBOM 도구, 취약점 분석 도구 가이드 |
EOF

for dir in "${SYNC_DIRS[@]}"; do
  echo "📥 ${dir}"
  download_dir "$dir"
  echo ""
done

# 동기화 날짜 기록
echo "sync_date: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" > "${TARGET_DIR}/.sync-meta"
echo "branch: ${BRANCH}" >> "${TARGET_DIR}/.sync-meta"

echo "===== 동기화 완료 ====="
echo "다운로드: ${DOWNLOADED}개 파일"
echo "오류: ${ERRORS}건"
echo "저장 위치: ${TARGET_DIR}/"
echo ""

if [ "$ERRORS" -gt 0 ]; then
  echo "⚠️  일부 파일 다운로드 실패. rate limit일 수 있습니다."
  echo "   잠시 후 재시도하거나 GITHUB_TOKEN을 설정하세요."
  exit 1
fi
echo "✅ 완료. .claude/reference/kwg/ 에서 KWG 원본 가이드를 참조할 수 있습니다."

# ── 드리프트 감지 자동 실행 ──────────────────────────────
echo ""
echo "===== KWG 드리프트 감지 시작 ====="
if command -v python3 &>/dev/null && [ -f ".claude/scripts/check-kwg-drift.py" ]; then
  if python3 .claude/scripts/check-kwg-drift.py; then
    echo "✅ KWG 싱크 이상 없음."
  else
    EXIT_CODE=$?
    if [ "$EXIT_CODE" -eq 1 ]; then
      echo ""
      echo "┌──────────────────────────────────────────────────┐"
      echo "│  KWG 변경 감지됨. 다음 단계를 실행하세요:        │"
      echo "│                                                  │"
      echo "│  Claude Code 세션에서:                           │"
      echo "│    /kwg-check                                    │"
      echo "│                                                  │"
      echo "│  (의미론적 갭 분석 후 반영 권고사항 출력)         │"
      echo "└──────────────────────────────────────────────────┘"
    fi
  fi
else
  echo "ℹ️  python3 없음. check-kwg-drift.py 건너뜀."
  echo "   설치 후 수동 실행: python3 .claude/scripts/check-kwg-drift.py"
fi
