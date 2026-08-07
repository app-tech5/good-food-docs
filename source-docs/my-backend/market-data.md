# Languages & market data — Backend API

What gets seeded automatically vs. what an operator has to set — not a route list.

## Three separate documents, easy to conflate

| Model | What it holds | Who edits it |
|---|---|---|
| `Language` | The catalogue of available locales (`code`, `name`, `isDefault`) — migrations seed `en`/`fr`/`es`/`ar`. | Admin → **Languages**. |
| `Currency` | Currency catalogue (`code`, `name`, `symbol`, `exchangeRate`) — seeded with common currencies. | Admin → **Currencies**. |
| `Setting` (singular, one document) | The marketplace's **active** branding: `appName`, `logoUrl`, one `currency` reference, and the embedded default-`language` object. | Admin App Settings (main currency picker) + whichever screen sets the default language. |
| `Tax` | Named tax rates (`location`, `name`, `rate`) attached per-restaurant. | Admin → **Taxes**; also auto-assigned to a new restaurant from the oldest `Tax` record if none is set. |

The distinction that trips people up: **`Language.isDefault`** flips which language is the marketplace default (setting it on one language automatically clears the flag on the rest and syncs `Setting.language`), while **`Setting.currency`** is the one "main currency" used across menu/cart/wallet/earnings displays — editing `Currency` rows alone doesn't change what's "active" until `Setting.currency` points at one.

## RTL, honestly

There's no separate "RTL flag" field in the database — Arabic renders right-to-left because the client apps special-case the `ar` language code, not because of a backend setting. Setting `ar` as `Language.isDefault` only changes the default locale; RTL layout is a client concern (customer/driver/restaurant Settings screens each read the language code and flip layout direction themselves).

## Taxes at checkout

A restaurant's `tax.rate` is set once (defaulting to the oldest seeded `Tax` record) and stored inline on the restaurant document — changing a `Tax` row later does not retroactively change restaurants that already copied a rate. Reassign the restaurant's tax explicitly if you need it to pick up a new rate.

## Configure market data for a launch city

1. Admin → **Languages** — confirm `en`/`fr`/`es`/`ar` exist; set the one you want as default ([admin languages](../admin-app/languages.md)).
2. Admin → **Currencies** + App Settings main currency ([currencies & taxes](../admin-app/currencies-taxes.md)) — this is what actually displays across the apps, not just the `Currency` catalogue.
3. Admin → **Taxes** — add the rate(s) for your market, then assign to each restaurant (or let new restaurants pick up the oldest seeded rate by default).
4. Mobile Settings language pickers read the same `Language` catalogue: [customer](../customer-app/languages-rtl.md), [driver](../delivery-app/languages.md), [restaurant](../restaurant-app/languages.md).

## Verify

- Symbol matches on menu, cart, wallet, earnings — all should reflect `Setting.currency`, not just the `Currency` list.
- Changing `Language.isDefault` updates `Setting.language` (check the App Settings/Setting record after saving).
- Arabic mirrors layout on at least one mobile app once selected — confirms the client-side RTL logic, not a backend flag.

## Related

- [Environment config](../environment-config.md) — editing locale JSON
- [Hybrid order channels](./channels-api.md) — `defaultLanguage`/`timezone` also live on `AppSetting`, separate from `Setting`
