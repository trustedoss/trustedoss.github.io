#!/usr/bin/env bash
# deck/index.html 을 웹사이트 공개 경로로 복사한다.
# 슬라이드를 고친 뒤에는 이 스크립트를 돌려야 공개본이 최신이 된다.
#
# 공개본에서는 발표자 노트(.notes-src)를 걷어낸다. 슬라이드 본문은 영어지만
# 노트는 한국어 발표용 원고라, 그대로 두면 한국어와 영어 사이트 어느 쪽에서도
# 방문자가 한국어 원고를 읽게 된다. 원본 index.html 은 노트를 그대로 유지한다.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
src="$here/index.html"
dest="$here/../website/static/reference/talks/oss-summit-korea-2026/slides.html"

mkdir -p "$(dirname "$dest")"

python3 - "$src" "$dest" <<'PY'
import re
import sys

src, dest = sys.argv[1], sys.argv[2]
html = open(src, encoding="utf-8").read()

# 노트 블록에는 중첩 div 가 없으므로 첫 </div> 까지 잘라내면 된다.
html, removed = re.subn(
    r'[ \t]*<div class="notes-src">.*?</div>\n', "", html, flags=re.S
)

# 노트를 걷어냈으니 S 키도 막는다. 그대로 두면 빈 발표자 패널이 열린다.
html, keys = re.subn(
    r'notes\.classList\.toggle\("open"\);',
    "/* presenter notes are not published */",
    html,
)
if removed and not keys:
    sys.exit("S 키 핸들러를 찾지 못했다. 슬라이드 구조가 바뀌었는지 확인하라.")

left = re.findall(r"[가-힣]", html)
if left:
    sys.exit(f"공개본에 한글이 {len(left)}자 남았다. 노트 밖에 한국어가 있는지 확인하라.")

open(dest, "w", encoding="utf-8").write(html)
print(f"발표자 노트 {removed}개 블록 제거")
PY

echo "published: deck/index.html -> website/static/reference/talks/oss-summit-korea-2026/slides.html"
