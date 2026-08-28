#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib/paths.sh
source "$SCRIPT_DIR/lib/paths.sh"

usage() {
  echo "Usage: $(basename "$0") INPUT.html OUTPUT.pdf"
  echo
  pdf_show_help
}

case "${1:-}" in
  -h|--help)
    usage
    exit 0
    ;;
esac

pdf_resolve_repo_root
pdf_validate_io_paths "${1:?input.html}" "${2:?output.pdf}"

node "$SCRIPT_DIR/render-html.mjs" "$INPUT" "$OUTPUT"
