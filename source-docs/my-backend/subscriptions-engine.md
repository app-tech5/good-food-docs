# Subscriptions engine — Backend API

Recurring plans for **customer**, **driver**, and **restaurant** targets — stored and enforced server-side.

## Operator steps

1. Admin → **Subscriptions** (`/api/subscriptions`).
2. Review seeded tiers; edit price, cycle, benefits, `target`, active flag.
3. Align currency with [market data](./market-data.md).

## App smoke tests

| App | Path |
|-----|------|
| Customer | [Membership plans](../customer-app/subscriptions.md) |
| Driver | [Priority plans](../delivery-app/subscriptions.md) |
| Restaurant | [Partner plans](../restaurant-app/subscriptions.md) |

Empty lists → `migrate:status`, admin CRUD, and that the signed-in role matches the plan `target`.

## Related

- [Commission engine](./commission-engine.md) — restaurant plan benefits
- Admin: [subscriptions](../admin-app/subscriptions.md)
