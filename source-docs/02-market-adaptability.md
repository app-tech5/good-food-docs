# Market adaptability — languages, currency, channels, regional money

Food delivery is local. This guide shows how to enable the shipped locales, switch currency, understand hybrid channels, and verify wallet / regional payment flags — after the backend migrations that seed market defaults.

Run **`npm run migrate:up`** in the API project first. Market-adaptability migrations upsert Spanish and Arabic language documents (Arabic marked RTL), keep English/French RTL off, and prepare wallet / channel / gateway defaults.

## 1. Enable languages (EN / FR / ES / AR)

The suite ships UI strings for **English, French, Spanish, and Arabic**. Arabic uses **right-to-left (RTL)** layout in the mobile and admin experiences when that language is active.

### In admin

1. Open **Languages**.
2. Confirm `en`, `fr`, `es`, and `ar` exist after migrations.
3. Set the **default** language for your primary market.
4. Leave Arabic’s RTL flag on — the clients rely on that metadata plus their own locale packs.

### In each app

1. Open **Settings** (or the language picker) in customer, driver, restaurant, and admin.
2. Switch between EN / FR / ES / AR.
3. For Arabic, confirm layout mirrors (navigation, text alignment, icons that should flip).
4. Restart the app if a cached language sticks after an admin default change.

Mobile apps can also follow the device locale when a matching pack exists; users can still override in Settings.

### Editing copy

Translate by editing the locale JSON for each app (same keys as English, translated values only), then restart Metro / the admin dev server. Register any brand-new language the same way the four shipped locales are registered, and optionally add a languages document in Mongo via admin. Practical detail: [environment-config.md](./environment-config.md).

## 2. Change currency

You do **not** hard-code currency in every mobile binary for normal market changes. Configure it in admin:

1. Open **Currencies**.
2. Create (or edit) the currency: code, name, symbol, exchange rate as required.
3. Open **App Settings** and set that currency as the **main** / default platform currency.
4. Save.
5. Force clients to reload settings: pull to refresh where available, restart the app, or sign out and back in if a cached symbol remains.

### Verify

- Customer menu prices, cart, and wallet show the new symbol.
- Restaurant and driver totals match.
- Admin reports / earnings use the same currency story.

## 3. Hybrid channels (overview)

Not every order starts in your branded mobile app. **Channels** describe how demand can enter (counter, phone, partner, and similar ideas) while still landing in the **same** order pipeline for kitchen status, earnings, and logistics.

### How to think about them

1. In admin, review channel-related fields / configuration exposed on settings or channel entities after migrations.
2. Keep one kitchen and one courier flow — channels should not become a second disconnected system.
3. Place a test order from the normal customer app first; then explore alternate channel entry only once the core accept → deliver path is solid.

API surface: **`/api/channels`**. Pair with [Kitchen Display](./03-kitchen-display.md) and [Logistics](./04-logistics.md) so every entry mode still ends in tickets and drivers.

## 4. Regional payments & wallet flags

Feeling “local” also means payment brands and wallet habits people already trust.

### Gateways

1. Open admin **Gateways** (backed by **`/api/gateways`**).
2. Enable Stripe and/or regional PSP options your deployment supports (for example Paystack, Flutterwave, Razorpay slots).
3. Align mobile publishable keys and backend secrets — see [01-monetization.md](./01-monetization.md) and [environment-config.md](./environment-config.md).

### Wallet behaviour

1. In **App Settings**, review cashback-style and instant-refund (or similar) wallet flags seeded for market adaptability.
2. Toggle what you want for the launch city.
3. In the customer app, top up and complete a refund/cashback scenario that matches the flags you enabled.

Stripe Connect remains available for marketplace-style payouts where you turn it on with backend env vars.

## 5. End-to-end verification checklist

1. Admin default language = your launch language; Arabic RTL checked on a device.
2. Main currency updated; all three mobile apps show the symbol after refresh.
3. Customer can check out with the gateway you enabled.
4. Wallet flags behave as configured.
5. A normal app order still reaches restaurant accept and driver complete.

## Related

- [Monetization](./01-monetization.md) — commissions, plans, ads, Stripe env  
- [Environment config](./environment-config.md) — i18n edit approach and production checklist
