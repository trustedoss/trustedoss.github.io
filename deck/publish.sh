#!/usr/bin/env bash
# deck/index.html 을 웹사이트 공개 경로로 복사한다.
# 슬라이드를 고친 뒤에는 이 스크립트를 돌려야 공개본이 최신이 된다.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
src="$here/index.html"
dest="$here/../website/static/reference/talks/oss-summit-korea-2026/slides.html"

mkdir -p "$(dirname "$dest")"
cp "$src" "$dest"

echo "published: deck/index.html -> website/static/reference/talks/oss-summit-korea-2026/slides.html"
