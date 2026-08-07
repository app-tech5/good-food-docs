# Languages & RTL — Driver app

EN / FR / ES / AR strings switchable from driver Settings (RTL for Arabic). This app has its own `lang/` files independent of the customer/restaurant apps — translating one does not translate the others.

## What drives this

- **App Settings → `defaultLanguage`** (Admin) sets the language a fresh driver session starts in; it doesn't override a driver who already picked a language.
- **`lang/en.json` / `fr.json` / `es.json` / `ar.json` + `i18n.js`** hold this app's actual copy — job board, active-delivery, and POD strings all come from here.
- **RTL** is applied automatically for Arabic by the app's i18n layer — useful to demo mid-shift screens (job board, active job) since drivers rely on quick scanning, not just readable text direction.

## Try it

1. Driver → **Settings** → language.
2. Confirm Deliveries / Active job strings update immediately.
3. Try Arabic RTL on the job board and confirm layout mirrors, not just text.

## Related

- [Customer languages](../customer-app/languages-rtl.md) · [Admin languages](../admin-app/languages.md)
