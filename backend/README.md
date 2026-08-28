# Backend (`backend/`)

API, domain logic, and persistence for CareFlow. **Persistence is locked:** PostgreSQL + pgvector ([D-001](../research/decision-log.md), [ADR](../docs/research/postgresql-primary-store.md)). Application code is still a placeholder until FastAPI lands per [plans/kenya-pretriage.md](../plans/kenya-pretriage.md).

## Key files

| File | Role |
|------|------|
| [../plans/product-schema.md](../plans/product-schema.md) | Product DDL — first Alembic revision when FastAPI lands |
| *(app package)* | Add a row when the first package, OpenAPI spec, or entrypoint exists |

## Related

- [docs/api/](../docs/api/) — human + agent HTTP reference (stubs; customize after the API exists)
- [research/ops/](../research/ops/) — stack and vendor research
- [Repository root](../README.md)
- [ONBOARDING.md](../ONBOARDING.md)
