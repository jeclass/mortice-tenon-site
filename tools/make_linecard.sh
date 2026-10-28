#!/usr/bin/env bash
# Print tools/linecard.html to docs/downloads/mortice-and-tenon-line-card.pdf (one Letter page),
# then recompress the product thumbnails as JPEG (needs a Python with pymupdf; see README).
set -euo pipefail
cd "$(dirname "$0")/.."
out=docs/downloads/mortice-and-tenon-line-card.pdf
py=${PYTHON:-$HOME/.local/share/mtsite-venv/bin/python}
google-chrome --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=5000 --print-to-pdf="$out.tmp" "file://$PWD/tools/linecard.html" 2>/dev/null
"$py" -W ignore - "$out.tmp" "$out" <<'PY'
import sys, pymupdf
d = pymupdf.open(sys.argv[1])
d.rewrite_images(dpi_threshold=None, quality=82, lossy=True, lossless=True, bitonal=False, color=True, gray=True, set_to_gray=False)
d.set_metadata({"title": "Mortice & Tenon line card", "author": "Mortice & Tenon", "subject": "Line card, updated 2026-10-27"})
d.save(sys.argv[2], garbage=4, deflate=True)
PY
rm -f "$out.tmp"
echo "wrote $out ($(stat -c %s "$out") bytes)"
