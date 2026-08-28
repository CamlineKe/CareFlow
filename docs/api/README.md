# CareFlow HTTP API reference (`docs/api/`)

Human-oriented documentation for the REST surface registered in **`backend/<route-registry>`**. It explains **query contracts**, **pagination models**, **auth scopes**, and **error envelopes** that are easy to misread from OpenAPI alone.

**Machine-readable contract:** `backend/openapi/openapi.yaml` plus tests—not this prose.

**Related material**

- [Conventions](conventions.md) — prefix, auth, money and time, errors.
- [Pagination, sorting, and query keys](pagination-sorting-and-query-keys.md) — cursor vs offset lists, master table.
- [AGENTS.md](AGENTS.md) — authoring contract for agents writing or refreshing domain chapters.
- Domain chapters (add below as you document each area).

## Route map

All routes use the **`/v1`** prefix unless noted. Replace path templates with your router's param syntax (`{id}`, `:id`, etc.).

| Method | Path template | Chapter |
|--------|---------------|---------|
| | | *(add rows as domains are documented)* |

## Maintaining this documentation

Use this section when changing the HTTP surface or refreshing OpenAPI.

**Precedence when sources disagree**

1. **Runtime contract** — Handler code, schemas, status codes, and serializers define what clients receive.
2. **JSON field names** — Schema definitions and response helpers.
3. **Generated OpenAPI** — Must match the above; fix handlers/schemas first, regenerate, then update prose here.

**Same-PR discipline**

Any change that alters routes, query contracts, sort tokens, bodies, or status codes should, in the **same PR**: regenerate OpenAPI when applicable, run `echo 'Set TEST_COMMAND in docs/testing-reference.md'`, and **edit the relevant `docs/api/*.md`** (route map row if needed, query tables, pagination master table, endpoint notes).

**Parity checklist before merge**

- Every shipped route appears in the route map above (or a linked chapter covers it explicitly).
- List handlers: documented query keys match validation in code.
- New pagination or sort behaviour appears in [pagination-sorting-and-query-keys.md](pagination-sorting-and-query-keys.md).
- Document intentional JSON quirks so they are not "corrected" away.

**What not to do**

- Do not hand-edit generated OpenAPI without updating source schemas or JSDoc.
- Do not treat this prose as authoritative for machine consumers—OpenAPI and tests are.

**Authoring:** follow [AGENTS.md](AGENTS.md). For large new surfaces, delegate chapter work to a documentation subagent per that file.
