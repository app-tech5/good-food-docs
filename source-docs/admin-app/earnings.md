# Commissions & earnings — Admin app

Review platform vs restaurant (and delivery/tax) splits by period.

## Prerequisites

1. Backend migrated; demo or real completed orders that produce earnings rows.
2. Default commission set in [App Settings](./app-settings.md).
3. Admin signed in against the same API.

## Steps

1. Complete a test order end-to-end (customer → restaurant accept → complete / paid).
2. Open **Earnings** (`/earnings`) — list periods and totals.
3. **View** a row → **Earnings details**:
   - Summary: period range, reference, total earnings
   - Split cards: platform commission, restaurant earnings, delivery earnings, taxes
   - **Transactions** table for that period
   - **Payouts** (pending/completed) when money is owed out
4. If the split looks wrong, re-check App Settings commission and the related orders; restaurant subscription benefits can soften the platform cut ([subscriptions](./subscriptions.md)).

## Smoke test

| Step | Expect |
|------|--------|
| List after completed orders | Rows with period totals |
| View detail | Summary + four split cards + transactions |
| Payout pending | Restaurant earnings amount appears under Payouts when applicable |
| Change commission then new order | New earning rows reflect the new rate |

## Related

- [monetization index](./monetization.md)
- [backend commission engine](../my-backend/commission-engine.md)
- [transactions / money ledger](./transactions.md)
