# Languages & RTL — Customer app

EN / FR / ES / AR strings, switchable from in-app Settings; Arabic mirrors the layout (RTL). Every client app (customer, driver, restaurant, admin) ships the same four locale files independently — translating one app does not translate the others.

## What drives this

- **App Settings → `defaultLanguage`** (Admin) sets the language a *fresh* install/session starts in; it does not force-override a customer who has already picked a language in their own Settings.
- **Per-app locale files** (`lang/en.json`, `lang/fr.json`, `lang/es.json`, `lang/ar.json` + `i18n.js`) hold the actual copy for this app — edit these to change wording, not the backend.
- **RTL** is applied automatically by the app's i18n layer when Arabic is selected — navigation direction and text alignment mirror; this is a layout behaviour, not a separate setting.
- **Currency/number formatting** is separate from language — see [market adaptability](../admin-app/market.md) for currency/timezone, which is driven by App Settings **`timezone`** and the currency configured per market, not by `defaultLanguage`.

## Try it

1. Confirm the Admin languages catalogue is populated ([admin languages](../admin-app/languages.md)).
2. Customer → **Settings** → pick a language.
3. Confirm home / menu / cart strings update immediately (no restart needed).
4. Select Arabic — navigation and text direction should mirror (RTL).

Editing copy: edit that app’s locale JSON (copy English keys, translate values only). Register a new language the same way EN/FR/ES/AR are registered, then expose the code in Admin → Languages.

## Related

- [Backend market data](../my-backend/market-data.md) · Driver / restaurant language guides under those apps
