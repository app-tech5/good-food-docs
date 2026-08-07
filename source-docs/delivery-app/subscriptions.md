# Priority plans — Driver app

Driver subscription tiers (`target = driver`). Priority members get first look at new jobs and a wider batch radius.

## What you configure (Admin → Subscriptions)

| Field / flag | Effect |
|---|---|
| **Price / billing cycle** | What the driver pays |
| **Benefits** (display tags) | Copy on the plan card |
| **`prioritySupport`** | First look at new pending jobs (~90s lead), plus wider batch-suggestion radius |
| **`platformAccess`** | Marks the plan as access/SaaS-style |
| **`is_active`** | Plan purchasable or hidden |

## Try it

1. Admin: active plan with `target = driver` and `prioritySupport` on.
2. Driver → **Subscriptions** → subscribe.
3. Go online — new pending jobs appear for the priority driver before non-members.
4. On an active delivery, request batch suggestions — search radius is wider for priority members.

## Related

- [Job board & batching](./deliveries.md)
- [Backend subscriptions](../my-backend/subscriptions-engine.md) · Admin [subscriptions](../admin-app/subscriptions.md)
