#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib/paths.sh
source "$SCRIPT_DIR/lib/paths.sh"

usage() {
  echo "Usage: $(basename "$0") INPUT.svg OUTPUT.pdf [--landscape]"
  echo
  pdf_show_help
}

LANDSCAPE=0
POSITIONAL=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --landscape)
      LANDSCAPE=1
      shift
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

set -- "${POSITIONAL[@]}"

pdf_resolve_repo_root
pdf_validate_io_paths "${1:?input.svg}" "${2:?output.pdf}"

SVG_ARGS=("$SCRIPT_DIR/render-svg.mjs" "$INPUT" "$OUTPUT")
if [[ "$LANDSCAPE" -eq 1 ]]; then
  SVG_ARGS+=(--landscape)
fi

node "${SVG_ARGS[@]}"
