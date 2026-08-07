# Languages & RTL — Admin app

The catalogue of languages available across every client app, and which one is the marketplace default. Migrations seed English, French, Spanish, and Arabic.

## What you configure

| Field | Meaning | Effect when set |
|---|---|---|
| **Code** | ISO language code (`en`, `fr`, `es`, `ar`) | Must match the locale files each app ships (`lang/`/`locales/` per repo) — an unmatched code has nothing to render |
| **Name** | Display name shown in language pickers | What users see in the picker, not the code itself |
| **Is Default** (`isDefault`) | Marks this language as the marketplace default | Turning this on for one language automatically becomes the fallback for clients that haven't picked a language yet, and updates the platform's default language setting |

Arabic (`ar`) also needs its RTL flag/handling honored on the client side — it's a layout concern in each app, not a field on this record, but don't remove Arabic from the catalogue if any client still ships RTL support for it.

## How to set it up

1. Open **Languages** after running migrations — you should already see `en`, `fr`, `es`, `ar`.
2. Add any language you support that isn't listed: set **Code** and **Name**.
3. Set **Is Default** on exactly one language — the one new users without a saved preference should see.
4. Confirm each client's locale files actually contain that language code (customer, driver, restaurant, admin all keep their own `lang/` / `locales/` JSON — adding a row here does not create the translations, it just exposes the option).
5. To customize wording: copy `en.json`, translate **values only**, register the locale in that app’s i18n entry — see [customer languages](../customer-app/languages-rtl.md) for the in-app picker story.

## Verify

| Check | Expect |
|---|---|
| Open Languages after migrations | `en`, `fr`, `es`, `ar` present |
| One language marked `isDefault` | Exactly one row — new sessions without a saved preference use it |
| Switch language picker in each mobile app | [customer](../customer-app/languages-rtl.md), [driver](../delivery-app/languages.md), [restaurant](../restaurant-app/languages.md) all reflect the same codes |
| Select Arabic on a client that supports RTL | Layout mirrors correctly |

## Related

- [Market index](./market.md) · [Backend market data](../my-backend/market-data.md)
