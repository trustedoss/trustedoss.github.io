#!/usr/bin/env bash
# sync-output-samples.sh
# output/ → output-sample/ 동기화
# *.md 파일만 복사. .json/.sh/.DS_Store 등 제외.
# 기존 파일은 덮어쓰기만 하며 삭제는 하지 않음.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$ROOT/output"
DST="$ROOT/output-sample"

echo "===== output-sample 동기화 시작 ====="
echo "  from: $SRC"
echo "  to:   $DST"
echo ""

rsync -av \
  --include="*/" \
  --include="*.md" \
  --exclude="*" \
  "$SRC/" "$DST/"

echo ""
echo "✅ output-sample/ 동기화 완료"
echo "   다음 단계: /update-reference-samples 스킬을 실행하여 website/reference/samples/ 를 갱신하세요."
