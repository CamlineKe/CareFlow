#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUT_DIR="$SCRIPT_DIR/.smoke-out"
mkdir -p "$OUT_DIR"

pass=0
skip=0

echo "=== 1. HTML → PDF ==="
"$SCRIPT_DIR/render-html.sh" "$SCRIPT_DIR/fixtures/sample.html" "$OUT_DIR/html.pdf"
test -s "$OUT_DIR/html.pdf"
echo "OK: $OUT_DIR/html.pdf"
pass=$((pass + 1))

echo
echo "=== 2. Markdown → PDF ==="
if command -v pandoc >/dev/null 2>&1; then
  "$SCRIPT_DIR/render-markdown.sh" "$SCRIPT_DIR/fixtures/sample.md" "$OUT_DIR/markdown.pdf"
  test -s "$OUT_DIR/markdown.pdf"
  echo "OK: $OUT_DIR/markdown.pdf"
  pass=$((pass + 1))
else
  echo "SKIP: pandoc not installed (brew install pandoc)"
  skip=$((skip + 1))
fi

echo
echo "=== 3. SVG → PDF (landscape) ==="
"$SCRIPT_DIR/render-svg.sh" "$SCRIPT_DIR/fixtures/sample.svg" "$OUT_DIR/svg-landscape.pdf" --landscape
test -s "$OUT_DIR/svg-landscape.pdf"
echo "OK: $OUT_DIR/svg-landscape.pdf"
pass=$((pass + 1))

echo
echo "=== 4. ReportLab (tertiary, optional) ==="
if [[ -x "$SCRIPT_DIR/.venv/bin/python" ]]; then
  "$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/fixtures/reportlab-sample.py" "$OUT_DIR/reportlab.pdf"
  test -s "$OUT_DIR/reportlab.pdf"
  echo "OK: $OUT_DIR/reportlab.pdf"
  pass=$((pass + 1))
else
  echo "SKIP: no .venv — tertiary ReportLab pipeline available with:"
  echo "  python3 -m venv $SCRIPT_DIR/.venv && $SCRIPT_DIR/.venv/bin/pip install reportlab"
  skip=$((skip + 1))
fi

echo
echo "Smoke test complete: $pass passed, $skip skipped"
echo "Outputs in $OUT_DIR"

# Global skill install: verify arbitrary absolute I/O (global mode contract)
if [[ "$SCRIPT_DIR" == "$HOME/.cursor/skills/pdf-generation/scripts" ]]; then
  echo
  echo "=== 5. Global mode — absolute /tmp output ==="
  TMP_PDF="$(mktemp /tmp/pdf-global-smoke-XXXXXX.pdf)"
  "$SCRIPT_DIR/render-html.sh" "$SCRIPT_DIR/fixtures/sample.html" "$TMP_PDF"
  test -s "$TMP_PDF"
  echo "OK: $TMP_PDF"
  rm -f "$TMP_PDF"
  pass=$((pass + 1))
fi
