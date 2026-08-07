# Payouts & history — Driver app

Transaction trail (every `delivery_fee`, adjustment, or payout line for this driver) and the bank/Connect setup that turns accrued earnings into an actual bank deposit.

## What drives this

- **Transaction list** — each row is a `Transaction` document scoped to this driver (`driver_payout`, `delivery_fee`, `adjustment`, etc.) — the same records support and admin use to resolve a dispute, so what the driver sees here matches what admin sees on their side.
- **Payout methods** — backed by `PaymentMethod.stripeConnectAccountId` when Stripe Connect is configured on the backend, or manual bank details (`bankDetails`) otherwise. Whether Connect onboarding is offered at all depends on the backend having Stripe Connect environment keys configured — see [backend getting started](../my-backend/getting-started.md).
- **"Ready for settlement"** in this build simply reflects whether a payout method exists and is complete/verified; actual bank transfer timing depends on your Stripe Connect account, not on anything inside this app.

## Try it

1. Open **Transactions** — use these rows for support disputes (they should match what admin sees for the same driver).
2. Open **Payout methods** — add bank details or complete Stripe Connect onboarding if enabled.
3. Confirm the method shows as ready before expecting a real bank settlement.

## Related

- [Shift earnings](./earnings.md) · [Backend getting started](../my-backend/getting-started.md) (Stripe Connect env)
