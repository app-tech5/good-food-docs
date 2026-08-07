# Job board & batching — Driver app

Go online, work today’s list, and accept nearby batch suggestions.

## Prerequisites

- Driver approved / can go online ([getting started](./getting-started.md))
- Assignment radius sensible ([admin / restaurant delivery settings](../restaurant-app/hours.md))

## Steps

1. Driver goes **online**.
2. Open **Deliveries** — pending / on the way / completed.
3. Accept or start the next job.
4. For batching: two nearby ready orders → review **batch suggestions** → accept batch.
5. Continue to [on the road](./active-delivery.md).

API: **`/api/logistics`** batch-suggestions / accept-batch (used by the app).

## Related

- [Logistics index](./logistics.md) · [Backend logistics engine](../my-backend/logistics-engine.md)
