#!/usr/bin/env bash
# Path resolution for PDF render scripts. Source from wrappers; do not execute directly.

pdf_script_dir() {
  local src="${BASH_SOURCE[1]:-${BASH_SOURCE[0]}}"
  cd "$(dirname "$src")/.." && pwd
}

pdf_show_help() {
  cat <<'EOF'
PDF render scripts — shared path rules

  - Accept absolute paths or paths relative to the current working directory
  - Reject any path containing a ".." segment
  - Inside a git repository (project scripts/pdf/), resolved paths must stay under REPO_ROOT
  - Global skill install or scripts outside git: global mode — absolute paths allowed

Wrappers:
  render-html.sh     INPUT.html OUTPUT.pdf
  render-markdown.sh INPUT.md   OUTPUT.pdf
  render-svg.sh      INPUT.svg  OUTPUT.pdf [--landscape]
EOF
}

pdf_resolve_repo_root() {
  local pdf_bin
  pdf_bin="$(pdf_script_dir)"

  # Global skill install — always global mode (arbitrary absolute I/O; still reject ..)
  if [[ "$pdf_bin" == "$HOME/.cursor/skills/pdf-generation/scripts" ]]; then
    REPO_ROOT=""
    PDF_GLOBAL_MODE=1
    export REPO_ROOT PDF_GLOBAL_MODE
    return
  fi

  if REPO_ROOT="$(git -C "$pdf_bin" rev-parse --show-toplevel 2>/dev/null)"; then
    PDF_GLOBAL_MODE=0
    REPO_ROOT="$(cd "$REPO_ROOT" && pwd)"
  else
    REPO_ROOT=""
    PDF_GLOBAL_MODE=1
  fi
  export REPO_ROOT PDF_GLOBAL_MODE
}

pdf_reject_dotdot() {
  local raw="$1"
  local part
  IFS='/' read -ra parts <<< "${raw#./}"
  for part in "${parts[@]}"; do
    if [[ "$part" == ".." ]]; then
      echo "pdf: path must not contain '..' segment: $raw" >&2
      return 1
    fi
  done
}

pdf_to_absolute() {
  local raw="$1"
  if [[ "$raw" = /* ]]; then
    printf '%s\n' "$raw"
    return 0
  fi
  local dir base
  dir="$(dirname "$raw")"
  base="$(basename "$raw")"
  if [[ "$dir" == "." ]]; then
    printf '%s/%s\n' "$(pwd)" "$base"
  else
    printf '%s/%s\n' "$(cd "$dir" && pwd)" "$base"
  fi
}

pdf_validate_under_repo() {
  local abs="$1"
  local label="$2"
  if [[ "$PDF_GLOBAL_MODE" -eq 1 ]]; then
    return 0
  fi
  case "$abs" in
    "$REPO_ROOT"|"$REPO_ROOT"/*) return 0 ;;
    *)
      echo "pdf: $label outside REPO_ROOT ($REPO_ROOT): $abs" >&2
      return 1
      ;;
  esac
}

# Validate input/output paths; export INPUT and OUTPUT as absolute paths.
pdf_validate_io_paths() {
  local input_raw="$1"
  local output_raw="$2"

  pdf_reject_dotdot "$input_raw" || return 1
  pdf_reject_dotdot "$output_raw" || return 1

  local input_abs output_abs output_dir
  input_abs="$(pdf_to_absolute "$input_raw")"
  output_abs="$(pdf_to_absolute "$output_raw")"

  pdf_validate_under_repo "$input_abs" "input" || return 1
  pdf_validate_under_repo "$output_abs" "output" || return 1

  if [[ ! -f "$input_abs" ]]; then
    echo "pdf: input file not found: $input_abs" >&2
    return 1
  fi

  output_dir="$(dirname "$output_abs")"
  if [[ ! -d "$output_dir" ]]; then
    mkdir -p "$output_dir"
  fi

  export INPUT="$input_abs"
  export OUTPUT="$output_abs"
}
