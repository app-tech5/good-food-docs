# Languages & RTL — Restaurant app

EN / FR / ES / AR strings switchable from restaurant Settings (RTL for Arabic). This app has its own `lang/` files — separate from the customer, driver, and admin apps.

## What drives this

- **App Settings → `defaultLanguage`** (Admin) sets the language a fresh restaurant session starts in; it doesn't override a staff member who already picked a language.
- **`lang/en.json` / `fr.json` / `es.json` / `ar.json` + `i18n.js`** hold this app's copy — Orders, Menu, Kitchen Display, and drawer strings all pull from here.
- **RTL** mirrors navigation and text direction automatically for Arabic — worth testing on the Orders list and Kitchen Display since those are the highest-traffic screens during service.

## Try it

1. Restaurant → **Settings** → language.
2. Confirm Orders / Menu / drawer strings update.
3. Try Arabic RTL during a quiet moment (not mid-rush) and confirm layout — not just text — mirrors.

## Related

- [Customer languages](../customer-app/languages-rtl.md)
