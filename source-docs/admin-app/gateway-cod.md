# Cash on Delivery — how to configure (Admin)

Technical HOW-TO. Online HTML: `admin-app/gateway-cod.html`.

## What this gateway does

- Identifier: `cash-on-delivery`
- **No card PSP** — checkout marks the order as COD; courier collects cash
- Credentials are minimal (seed uses an `enabled`-style flag)
- Capabilities typically: no refunds / withdrawals / webhooks / subscriptions at the PSP layer
- Fees usually `0` / `0` — cost is ops risk, not interchange

## Prerequisites

1. Markets where you allow cash collection.
2. Driver / POD process that records cash collected ([delivery POD](../delivery-app/proof-of-delivery.md)).
3. Support playbook: COD disputes ≠ Stripe chargebacks.

## Admin steps

1. **Gateways** → **Cash on Delivery**.
2. Confirm the method is the one you intend (name/identifier).
3. Set **Active** only for cities/modes that allow COD (disable for prepaid-only campaigns).
4. Save. No Stripe/Paystack secrets belong on this form.

## Smoke test

| Step | Expect |
|------|--------|
| COD Active | Customer checkout can select cash |
| Place COD order | Order created without PSP authorize URL |
| Driver completes delivery | Cash collection / POD consistent with restaurant + admin ledger |
| COD Inactive | Checkout hides or rejects cash method |

## Differs from others

- No `/api/gateways/initialize` hosted session. Failures are operational (customer not home, wrong change), not `card_declined`.

## Related

- [gateways.md](./gateways.md) · [proof-of-delivery.md](../delivery-app/proof-of-delivery.md) · [orders.md](./orders.md)
