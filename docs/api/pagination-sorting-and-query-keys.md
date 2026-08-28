# Pagination, sorting, and query keys

Master reference for **list endpoints** on the CareFlow API. Domain chapters should link here instead of duplicating pagination rules.

**Machine-readable contract:** handler validation and OpenAPI—not this prose.

---

## Models in use

<!-- Document which endpoints use cursor vs offset vs unpaginated arrays -->

| Model | Used by | Notes |
|-------|---------|-------|
| Cursor | | |
| Offset (`limit` / `offset` or `page`) | | |
| Unpaginated | | |

---

## Endpoint master table

| Method | Path | Pagination | Sort allowlist | Filter notes |
|--------|------|--------------|----------------|--------------|
| | | | | *(add rows as list endpoints are documented)* |

---

## Query key conventions

<!-- Global rules: snake_case query keys, unknown key behaviour, default limits, max limits -->

---

## Maintenance

When a list contract changes, update this file and the domain chapter in the **same PR**. See [AGENTS.md](AGENTS.md).
