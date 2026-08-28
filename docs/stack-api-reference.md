# API reference documentation pack

Optional overlay from cursor-scaffold (**`api-docs`** module, OFF by default).

## What gets installed

| Path | Purpose |
|------|---------|
| `docs/api/README.md` | Route map + maintainer checklist |
| `docs/api/AGENTS.md` | Authoring contract for humans and agents |
| `docs/api/conventions.md` | Cross-cutting API contract (customize) |
| `docs/api/pagination-sorting-and-query-keys.md` | List-endpoint master table (customize) |
| `.cursor/rules/docs-api-reference.mdc` | Opt-in rule (`alwaysApply: false`) |

## After init

1. Set paths in `docs/api/AGENTS.md` placeholders (or re-run init with vars) — `API_ROUTES_PATH`, `HANDLER_ROOT`, `SCHEMA_ROOT`, `OPENAPI_PATH`, `REFERENCE_CHAPTER`.
2. Customize [docs/api/conventions.md](api/conventions.md) for auth, prefix, and errors.
3. Add domain chapters (e.g. `docs/api/listings.md`) using [docs/api/AGENTS.md](api/AGENTS.md) as the outline.
4. Attach `@.cursor/rules/docs-api-reference.mdc` when refreshing API prose.

## Reference implementations

- [Finance backend `docs/api/`](~/Documents/Projects/Finance/backend/docs/api/) — Go + chi + Swag
- [PropertyKenya backend `docs/api/`](~/Documents/Projects/PropertyKenya-Backend/docs/api/) — TypeScript + Fastify + JSDoc OpenAPI

## Testing

Run your project's test command after contract-impacting doc+code changes (`echo 'Set TEST_COMMAND in docs/testing-reference.md'`).
