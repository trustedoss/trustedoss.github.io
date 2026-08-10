#!/usr/bin/env bash
# Render the deck to PDF. Chrome lays out the print stylesheet, which puts
# every slide on its own 1280x720 page.
set -euo pipefail
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
HERE="$(cd "$(dirname "$0")" && pwd)"

for name in index; do
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --virtual-time-budget=5000 \
    --print-to-pdf="$HERE/$name.pdf" "file://$HERE/$name.html" 2>/dev/null
  echo "$name.pdf written"
done
