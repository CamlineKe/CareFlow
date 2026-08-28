# API conventions

Cross-cutting behaviour for JSON routes registered in **`backend/<route-registry>`**. This chapter is the **shared contract** for frontend agents and maintainers; domain-specific routes, filters, and auth tables live in the chapters linked below.

**Machine-readable contract:** handler code, schema types, generated OpenAPI, and integration tests—not this prose. When sources disagree, see **Precedence** in [README](README.md).

**Authoring standard for domain chapters:** [AGENTS.md](AGENTS.md) (reference depth: **`<first-domain-chapter>.md`** once written).

---

## Path prefix

| Concept | Detail |
|---------|--------|
| **Prefix** | Product REST routes use **`/v1`** (customize this table for your mount). |
| **Health / probes** | Document non-prefixed routes here if your stack exposes them (e.g. `GET /health`). |
| **Path params** | Brace names must match route modules (customize examples for your router). |

---

## Authentication and authorisation

<!-- Customize: auth provider, header shape, middleware names, scope tables, 401/403 behaviour -->

| Topic | Detail |
|-------|--------|
| **Credentials** | *(e.g. `Authorization: Bearer <jwt>`, API keys, session cookies)* |
| **Validation** | *(JWKS URL, audience, TTL)* |
| **Route guards** | *(named hooks or middleware)* |
| **Admin / scoped routes** | *(scope claim names, capability tables)* |

---

## Money, time, and identifiers

<!-- Customize: currency units, epoch vs RFC3339, UUID vs integer ids -->

---

## Errors

<!-- Customize: envelope shape (`error.code`, `message`, `requestId`), link to codes catalogue -->

---

## Related chapters

Add links to domain chapters as they are created under `docs/api/`.
