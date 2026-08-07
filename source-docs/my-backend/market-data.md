# Languages & market data — Backend API

Locales (EN/FR/ES/AR + RTL metadata), currencies, and taxes served to every client.

## After migrations

Confirm language documents and market defaults exist (`migrate:status` / admin lists).

## Operator steps

1. Admin → **Languages** — default + Arabic RTL flag ([admin languages](../admin-app/languages.md)).
2. **Currencies** + App Settings main currency ([currencies & taxes](../admin-app/currencies-taxes.md)).
3. **Taxes** — rates used at checkout.
4. Mobile Settings language pickers: [customer](../customer-app/languages-rtl.md), [driver](../delivery-app/languages.md), [restaurant](../restaurant-app/languages.md).

Older hub: [admin market.md](../admin-app/market.md).

## Verify

- Symbol matches on menu, cart, wallet, earnings.
- Arabic mirrors layout on at least one mobile app.

## Related

- [Environment config](../environment-config.md) — editing locale JSON
