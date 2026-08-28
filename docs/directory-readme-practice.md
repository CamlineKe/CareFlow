# Directory README practice

Human and agent reference for **top-level** repository documentation. Installed by default from the cursor-scaffold meta-repo (`directory-readmes` module).

**Rule (always on):** `.cursor/rules/directory-readmes.mdc`

## Why

New contributors and remote agents should orient from the repo root without opening every folder. Finance backend/frontend and PropertyKenya orchestration repos use this pattern; PropertyKenya-Backend goes further (README per route/package) — **that depth is opt-in here**, not the default.

## Two-layer root docs

| File | Audience | Content |
|------|----------|---------|
| [`README.md`](../README.md) | Production scan, architects | Purpose, topology, polyrepo table, directory map → top-level READMEs |
| [`ONBOARDING.md`](../ONBOARDING.md) | Local first-time setup | Prerequisites, clone, env, run, verify, directory map |

Split keeps root README readable in GitHub and avoids mixing prod hostnames with `localhost:8090` matrices.

## Top-level directory README template

Use for every committed top-level directory **except** `.cursor/`, `.claude/`, and hidden/tool dirs.

```markdown
# Title (`dirname/`)

One or two sentences: role of this directory.

## Key files

| File | Role |
|------|------|
| `example.sh` | What it does |

## Related

- [Repository root](../README.md)
- [ONBOARDING.md](../ONBOARDING.md) — if scripts or setup live here
```

### Good examples (external)

| Repo | Path | Notes |
|------|------|-------|
| Finance backend | `docs/README.md`, `scripts/README.md` | Index + script table; depth in linked docs |
| Finance frontend | `docs/README.md` | Short index table |
| PropertyKenya-Dev (target) | `caddy/README.md`, `scripts/README.md` | Infra dirs at top level only |

### Avoid by default

- README in every `src/routes/*` or `packages/*` subtree (PropertyKenya-Backend style)
- Duplicating `docs/testing-reference.md` inside `tests/README.md` — link instead

## Directory map (maintain in root README + ONBOARDING)

When you add a top-level folder, add a row to **both** maps:

| Directory | README | Topics |
|-----------|--------|--------|
| `docs/` | [docs/README.md](README.md) | Agent SOPs, testing reference |
| `plans/` | [plans/README.md](../plans/README.md) | Committed specs, wave template |

## Polyrepo links

When documenting sibling repositories:

1. **GitHub URL** — clone source of truth
2. **Default local path** — convention when checked out side-by-side
3. **Env var** — how compose or build resolves the path (if applicable)

Do not document siblings using only relative `../` paths.

## Nested READMEs (explicit request only)

Create `README.md` below the top level when the user asks — for example:

- A large standalone package (`packages/api/`) needing its own agent boundary
- A design subtree with multiple versioned mockups
- API reference chapters under `docs/api/` (separate `api-docs` module)

Otherwise, one paragraph in the parent top-level README or a link to `docs/` is enough.

## Verification

```bash
# Top-level dirs with content but no README (customize SKIP list)
for d in */; do
  base="${d%/}"
  case "$base" in .cursor|.claude|node_modules) continue ;; esac
  [[ -f "$d/README.md" ]] || echo "MISSING: $d/README.md"
done
```
