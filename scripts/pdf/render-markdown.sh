#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib/paths.sh
source "$SCRIPT_DIR/lib/paths.sh"

usage() {
  echo "Usage: $(basename "$0") INPUT.md OUTPUT.pdf"
  echo
  pdf_show_help
}

case "${1:-}" in
  -h|--help)
    usage
    exit 0
    ;;
esac

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pdf: pandoc not found — install with: brew install pandoc" >&2
  exit 1
fi

pdf_resolve_repo_root
pdf_validate_io_paths "${1:?input.md}" "${2:?output.pdf}"

PANDOC_CSS="$SCRIPT_DIR/fixtures/pandoc-print.css"
TMP_HTML="$(mktemp "${TMPDIR:-/tmp}/pdf-render.XXXXXX.html")"
trap 'rm -f "$TMP_HTML"' EXIT

pandoc "$INPUT" -o "$TMP_HTML" --standalone --css="$PANDOC_CSS"
node "$SCRIPT_DIR/render-html.mjs" "$TMP_HTML" "$OUTPUT"
