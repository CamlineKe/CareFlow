# Product map (`camlinedev/product-map/`)

Visual domain map of CareFlow **before** high-level system design. Two sides: care-seeker and hospital. One shared object: the booking. This folder explains how the product works to the end, why queues matter, and what the written plans still leave open.

| Field | Value |
|-------|-------|
| Document type | Product domain map index |
| Version | 0.1 |
| Status | Draft |
| Owner | camline |
| Last updated | 2026-08-28 |
| Related documents | [../README.md](../README.md), [../01-problem.md](../01-problem.md), [../../plans/user-journeys.md](../../plans/user-journeys.md) |
| Prerequisites | [../01-problem.md](../01-problem.md) |
| Revision summary | First map: language, two sides, loop, queue vs booking, invariants, scenarios |

This is not stack, APIs, modules, or a high-level architecture. Those wait until this map is challenged and the open wait-count / appointment questions are answered.

## Reading order

| File | Role |
|------|------|
| [01-language.md](01-language.md) | Canonical words. Read this first |
| [02-two-sides.md](02-two-sides.md) | Care-seeker side, hospital side, how they connect |
| [03-end-to-end.md](03-end-to-end.md) | Full loop, visuals, why each step exists |
| [04-queue-and-bookings.md](04-queue-and-bookings.md) | Walk-ins already there, wait_count, appointments, cancel, no-show |
| [05-invariants.md](05-invariants.md) | Rules that must stay true |
| [06-scenarios.md](06-scenarios.md) | Happy paths, edges, failures |

## Related

- [camlinedev index](../README.md)
- [Draft FRs](../03-functional-requirements.md)
- [Grill me questions](../05-open-questions.md)
