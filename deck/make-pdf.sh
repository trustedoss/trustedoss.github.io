#!/usr/bin/env bash
# Render the deck to PDF. Chrome lays out the print stylesheet, which puts
# every slide on its own 1280x720 page.
#
# index.pdf    the deck itself, 1280x720 per page
# handout.pdf  the rehearsal print: A4 portrait, one slide per sheet with
#              the script underneath
set -euo pipefail
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
HERE="$(cd "$(dirname "$0")" && pwd)"

"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=5000 \
  --print-to-pdf="$HERE/index.pdf" "file://$HERE/index.html" 2>/dev/null
echo "index.pdf written"

"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=6000 \
  --print-to-pdf="$HERE/handout.pdf" "file://$HERE/index.html?handout" 2>/dev/null
echo "handout.pdf written"
