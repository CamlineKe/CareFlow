---
name: pdf-generation
description: >-
  Generate publication-quality A4 PDFs from HTML, Markdown, SVG, or Python
  ReportLab. Use when the user asks for a PDF, printable report, export to PDF,
  download document, or print-ready deliverable.
---

# PDF generation

## When to use

- User asks for PDF, printable report, or export
- Research deliverable needs committed `deliverables/*.pdf`
- After regenerating Gantt SVGs — automate PDF step
- Executive summary or branded layout from HTML/CSS

## Dual script resolution (critical for Home workspace)

Render scripts live in the **project repo** when scaffolded (`scripts/pdf/`). In a Home workspace or before project init, fall back to the global skill copy or cursor-scaffold templates.

Resolve `PDF_BIN` once per shell session before any render:

```bash
if [[ -x scripts/pdf/render-html.sh ]]; then
  PDF_BIN=scripts/pdf
elif [[ -x "$HOME/.cursor/skills/pdf-generation/scripts/render-html.sh" ]]; then
  PDF_BIN="$HOME/.cursor/skills/pdf-generation/scripts"
else
  SCAFFOLD_ROOT="${CURSOR_SCAFFOLD_ROOT:-$HOME/Documents/Projects/cursor-scaffold}"
  PDF_BIN="$SCAFFOLD_ROOT/templates/scripts/pdf"
fi
```

Use `"$PDF_BIN/render-html.sh"`, `"$PDF_BIN/render-markdown.sh"`, and `"$PDF_BIN/render-svg.sh"` in all examples below.

## Pipeline selection

| Input | Pipeline | Script |
|-------|----------|--------|
| HTML (+ optional print CSS) | **Primary** — Playwright | `$PDF_BIN/render-html.sh` |
| Markdown (`.md`) | **Secondary** — Pandoc → HTML → Playwright | `$PDF_BIN/render-markdown.sh` |
| Tabular / invoice / data-heavy | **Tertiary** — ReportLab Python | Agent writes script; run in `.venv` |
| SVG (Gantt, diagram) | **Escape** — Playwright landscape | `$PDF_BIN/render-svg.sh` |

Default to **Primary** unless the source is already Markdown or pure tabular data.

## Prerequisites (macOS)

One-time setup — run if smoke test fails.

| Prerequisite | Skill documents | Cross-link target |
|--------------|-----------------|-------------------|
| Chromium / Playwright | Prefer project hook when present; fallback commands | [`scripts/ensure-playwright-browsers.mjs`](../../../scripts/ensure-playwright-browsers.mjs), [`.cursor/hooks.json`](../../hooks.json) sessionStart hook |
| Playwright npm dep | Pin `playwright@1.52.0` | [`scripts/pdf/package.json`](../../../scripts/pdf/package.json) |
| Pandoc | `brew install pandoc` | Evaluation report §7 install runbook (ops research deliverable when present) |
| ReportLab | PEP 668 safe `.venv` only | Failure handling — `ImportError` row below |
| Smoke verification | Post-setup check | [`scripts/pdf/smoke-test.sh`](../../../scripts/pdf/smoke-test.sh) |

**Chromium / Playwright:** If `.cursor/hooks.json` includes the Playwright sessionStart hook, Chromium installs on first Cursor session; otherwise run `node scripts/ensure-playwright-browsers.mjs` or `cd scripts/pdf && npx playwright install chromium`.

Pin Playwright version in commits; do not use floating `@latest` in CI.

```bash
brew install pandoc
python3 -m venv .venv && .venv/bin/pip install reportlab
```

## Global mode

Render scripts enter **global mode** when either:

1. The script tree is the **global skill install** (`~/.cursor/skills/pdf-generation/scripts`), or
2. The script tree is **not** inside a git repository (`git -C "$PDF_BIN"` finds no root)

In global mode:

- **Reject** any path containing a `..` segment (unchanged)
- **Allow** absolute paths for input and output
- **Skip** the “must stay under `REPO_ROOT`” check

When using **project** `scripts/pdf/` inside a git repo, resolved paths must stay under that repo’s root. Do not use `..` in any mode.

## Workflow — HTML (primary)

1. Write or reuse HTML with print stylesheet (`@page { size: A4; margin: 20mm; }`).
2. Use `reference/print.css` from this skill or link an equivalent.
3. Validate paths (no `..`; under repo root when in a git repo).
4. Render:

```bash
"$PDF_BIN/render-html.sh" path/to/input.html path/to/output.pdf
```

5. **QA:** Open PDF or attach page-1 screenshot; use multimodal model to check margins, clipping, page breaks.
6. Commit PDF only when user expects it in git (research deliverables yes; scratch use `tmp/pdf/`).

## Workflow — Markdown (secondary)

1. Prefer Pandoc metadata (title, date) in YAML frontmatter.
2. Optional: pass [`reference/pandoc-defaults.yaml`](reference/pandoc-defaults.yaml) for standalone HTML defaults.
3. Render:

```bash
"$PDF_BIN/render-markdown.sh" path/to/input.md path/to/output.pdf
```

Internally: Pandoc → standalone HTML with print CSS → Playwright. **Do not** call `pandoc -o file.pdf` without `--pdf-engine` unless tectonic/weasyprint is confirmed installed.

## Workflow — ReportLab (tertiary)

1. Create `.venv` if missing.
2. Generate Python using Platypus (`SimpleDocTemplate`, `Paragraph`, `Table`).
3. Run: `.venv/bin/python script.py -o output.pdf`
4. Coordinate origin is bottom-left — do not mix with top-left HTML mental model.

## Workflow — SVG / Gantt integration

After `gantt-roadmap` skill runs `scripts/roadmap/generate-gantt.sh`:

```bash
"$PDF_BIN/render-svg.sh" docs/project-management/roadmaps/initial-roadmap.svg \
  docs/project-management/roadmaps/initial-roadmap-gantt.pdf --landscape
```

Replaces manual Preview Print-to-PDF step from gantt-roadmap skill.

## Workflow — Stakeholder roadmap PDF

After editing a file in `docs/project-management/roadmaps/`:

```bash
"$PDF_BIN/render-markdown.sh" docs/project-management/roadmaps/initial-roadmap.md \
  docs/project-management/roadmaps/initial-roadmap.pdf
```

Output PDF uses the **same basename** as the source markdown in `roadmaps/` (not a separate `pdf-formatted/` folder). Regenerate when narrative or embedded Gantt changes.

## Script contracts

All `$PDF_BIN/*.sh` wrappers must:

- Exit non-zero on failure; print stderr hint
- Accept absolute or repo-relative paths
- Reject paths containing `..`
- Inside a git repo, reject paths outside `$REPO_ROOT`
- Be idempotent (overwrite output)
- Use Playwright with `printBackground: true` for HTML/SVG

## Security

- Never fetch remote HTML for render unless user explicitly provided URL
- Disable JS in Playwright for untrusted content
- Do not embed env vars, API keys, or tokens in PDF metadata
- No `curl | bash` from document bodies

## Failure handling

| Error | Fix |
|-------|-----|
| `Executable doesn't exist` (Chromium) | `npx playwright install chromium` or `node scripts/ensure-playwright-browsers.mjs` |
| `pandoc: command not found` | `brew install pandoc` |
| `ImportError` (ReportLab) | Use `.venv/bin/pip`, not system pip (PEP 668) |
| Layout wrong | Fix CSS `@page` / `page-break-before`; re-render; escalate model for CSS |
| Still wrong after 2 tries | Suggest user Cmd+P from browser on the HTML file |

## Model hints

See [`reference/model-selection-guide.md`](reference/model-selection-guide.md) for phase matrix, escalation rules, and multimodal QA.

- HTML/CSS layout → frontier or Sonnet-class
- ReportLab code → Composer / Codex
- Render log debugging → Sonnet
- Final QA → multimodal (screenshot page 1)

## Related skills

| Skill / module | Link |
|----------------|------|
| Playwright browser install (hooks module) | [`scripts/ensure-playwright-browsers.mjs`](../../../scripts/ensure-playwright-browsers.mjs), [`.cursor/hooks.json`](../../hooks.json) |
| Gantt SVG source | `gantt-roadmap` (project skill, when present) |
| Project init | `~/.cursor/skills/project-init/SKILL.md` — pdf-generation default ON |
