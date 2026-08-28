# Model selection guide — PDF generation

Maps **task phases** to model tiers, not specific SKU names that may rotate.

## Phase matrix

| Phase | What the model must do | Evaluation criteria | **Default** | **Budget mode** |
|-------|------------------------|---------------------|-------------|-----------------|
| **Requirements / layout design** | Page structure, branding, section hierarchy, pick pipeline tier | Reasoning, instruction following | Claude Sonnet / GPT-5 medium+ / Opus for complex briefs | Composer 2.x Fast |
| **HTML/CSS generation** | Print CSS (`@page`, breaks, margins, `-webkit-print-color-adjust`) | Front-end quality, spec compliance | Sonnet / GPT-5 / Composer (strong coding) | Composer Fast + `reference/print.css` template |
| **LaTeX / Pandoc markup** | Long-form academic layouts, citations, TOC | Syntax accuracy, fewer compile errors | Sonnet / Opus (avoid unnecessary LaTeX — prefer MD→HTML chain) | Composer + validate with `pandoc --dry-run` |
| **Python / Node PDF code** | ReportLab Platypus, pdfkit, Playwright helper scripts | API correctness, library knowledge | Composer / GPT-5 Codex class | Composer Fast |
| **Data → chart → PDF** | matplotlib → PNG → embed in HTML or ReportLab | Tool use, visual clarity | Sonnet + code execution | Composer |
| **Review / QA** | Compare rendered PDF to intent; spot overflow/clipping | Multimodal vision | **Claude Sonnet/Opus, GPT-5, or Gemini Flash/Pro with image input** | *No budget substitute* — skip QA = accept layout risk |
| **Iteration after render failure** | Parse stderr (LaTeX log, Chromium, Playwright traces) | Log comprehension, targeted fixes | Sonnet / Opus | Composer (max 2 retries then escalate) |

## Escalation rules

Escalate from **Budget → Default → Frontier** when:

1. **Second consecutive render failure** on same document
2. **Multi-column**, **running headers**, or **custom @page** (odd/even pages)
3. **LaTeX** explicitly requested (consider discouraging — use HTML tier instead)
4. **Brand-critical** deliverable (executive summary, client-facing)
5. **QA multimodal** flags clipping, orphan headings, or wrong page count

Do **not** escalate for: simple one-page letters, boilerplate tables via ReportLab, or SVG→PDF with existing gantt output.

## Multimodal QA workflow

Required before marking PDF tasks complete on branded/research deliverables:

1. Export page 1 (and last page if multi-page) as PNG — `pdftoppm -png doc.pdf /tmp/page` or Preview screenshot
2. Attach to chat; ask multimodal model: margins OK? text clipped? page count correct?
3. If fail → fix CSS/source → re-render → re-QA (max 2 loops)

## Anti-patterns

| Avoid | Why |
|-------|-----|
| Fast model for complex print CSS from scratch | High iteration cost; start from `reference/print.css` |
| Skipping multimodal QA on research PDFs | Silent margin/clipping bugs |
| LaTeX model on macOS without engine installed | Guaranteed failure |
| Same model for codegen + visual QA | Vision-capable models may be weaker at shell debugging — split phases |

## Budget mode summary

Use **Composer Fast** (or equivalent) for: scripted renders, SVG conversion, ReportLab from template, smoke tests.

Always use **multimodal frontier** for: final QA on anything committed to `deliverables/` or sent externally.

When in doubt, **HTML primary + Composer render + one vision check** beats **LaTeX + frontier codegen** on macOS agent setups.
