# Environment & branding configuration

Technical HOW-TO for buyers with the ZIP: **toolchain commands**, **`.env` tables**, reachability matrix, branding files, FCM, maps keys, CORS, and a production checklist.

The online [Environment setup](../environment-setup.html) page is the soft product story (currency UI, languages, push, Places) — it does **not** repeat Admin captures for App Settings, gateways, or channels. Those live on their own guides (linked below). This markdown is where the install/config detail belongs.

## Boot order (short)

1. MongoDB up → `my-backend` `.env` → `migrate:up` → `npm start`
2. Admin `.env` → `npm start` → sign in
3. Point every mobile `EXPO_PUBLIC_API_URL` at the same `/api` base the device can reach
4. In Admin, configure marketplace behaviour on the dedicated screens (do not look for those walkthroughs on the online Environment page):
   - [App settings](./admin-app/app-settings.md)
   - [Order channels](./admin-app/order-channels.md)
   - [Gateways](./admin-app/gateways.md)
   - [Subscriptions](./admin-app/subscriptions.md)
   - [Currencies & taxes](./admin-app/currencies-taxes.md) · [Languages](./admin-app/languages.md)

Full sequence: [Launch the suite](./00-launch-suite.md).

---

## API reachability

| Client runs on | Backend on your laptop | Suggested API base |
|----------------|------------------------|--------------------|
| Same laptop browser (admin) | `localhost:5000` | `http://localhost:5000/api` |
| iOS Simulator | laptop | `http://localhost:5000/api` |
| Android emulator | laptop | `http://10.0.2.2:5000/api` |
| Physical phone | laptop Wi‑Fi | `http://<LAN-IP>:5000/api` |
| Any client | VPS / domain | `https://your-domain.com/api` |

**Effects:** wrong host → login/order calls fail; phone `localhost` means the phone, not your PC. After changing `EXPO_PUBLIC_*`, restart Metro. Keep **protocol + host + port + `/api`** identical across customer, driver, restaurant, and admin.

`CORS_ORIGINS` must list browser origins (admin `http://localhost:3000` and production admin URLs).

---

## Backend env (`my-backend`)

| Variable | What it configures | Effect when set |
|----------|--------------------|-----------------|
| `MONGO_URI` | Database connection | API cannot start without a reachable Mongo |
| `JWT_SECRET` | Auth token signing | Sessions / protected routes; use a long unique secret in production |
| `PORT` | HTTP listen port (default `5000`) | Clients must use this port in their API URL |
| `NODE_ENV` | Runtime mode | `production` vs `development` logging/behaviour |
| `CORS_ORIGINS` | Allowed browser origins | Admin SPA can call the API; omit a origin → browser blocks |
| `STRIPE_SECRET_KEY` | Server-side Stripe | Card intents + Connect; needs real `sk_` for live charges |
| `STRIPE_CONNECT_COUNTRY` | Connect onboarding country | e.g. `FR` |
| `STRIPE_CONNECT_RETURN_URL` / `REFRESH_URL` | Driver Connect deep links | Return/refresh after Stripe Connect |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | FCM Admin SDK | API can push to devices (single-line JSON) |
| `WHATSAPP_VERIFY_TOKEN` | Meta webhook verify token | WhatsApp Cloud API handshake (default `goodfood_whatsapp_verify` if unset) |
| `PUBLIC_APP_URL` | Public web origin | PayPal return/cancel fallbacks when no callback passed |
| `DEMO_MODE` | Demo safety | Blocks destructive writes when `true` |
| `LOGISTICS_BATCH_RADIUS_KM` | Default batch search radius | Nearby job suggestions for drivers |
| `LOGISTICS_MAX_BATCH_SIZE` | Max orders in one batch | Caps multi-drop accepts |
| `LOGISTICS_POD_GEOFENCE_M` | POD distance check (metres) | Proof-of-delivery distance recorded vs dropoff |
| `LOGISTICS_POD_GEOFENCE_SOFT` | Soft vs hard geofence | Default soft (`true`); set `false` to block out-of-range POD |
| `LOGISTICS_PRIORITY_JOB_LEAD_S` | Priority-plan first-look window (seconds) | Non-members wait this long before seeing brand-new pending jobs |
| `LOGISTICS_PRIORITY_BATCH_BONUS_KM` | Extra batch radius for priority drivers | Wider multi-drop search for subscribed drivers |
| `INTELLIGENCE_HTTP_TIMEOUT_MS` | Weather/routing timeout | Fallback heuristics if Open-Meteo/OSRM slow |
| `OPEN_METEO_BASE_URL` / `OSRM_BASE_URL` | Optional self-hosted weather/routing | Defaults to public endpoints |
| `IMGBB_API_KEY` / `CLOUDINARY_*` | Image upload providers | Optional media hosting for uploads |
| `MONGODB_*` / `VPS_*` | Tooling / backup scripts | Optional; not required for `npm start` |

Day-one scripts: `migrate:up`, `migrate:status`, `npm start` / `npm run dev`, `npm run test:db`.

---

## After the API is up — configure in Admin

Env keys unlock the stack. **Marketplace behaviour** is configured in Admin (not only `.env`):

### App Settings (singleton)

| Setting | Effect |
|---------|--------|
| App name, support email, timezone, default language | Branding + reports + fallback locale |
| **Commission Rate** | Baseline platform cut on restaurant sales |
| **Stripe Enabled** / **Cash On Delivery Enabled** | Turn card/COD on or off (stays in sync with Gateways → Active) |
| Delivery fee, free threshold, max distance | Checkout defaults when a restaurant has no override |
| Wallet cashback % / instant refund | Auto ledger credits on delivered / cancelled paid orders |
| Web Ordering / WhatsApp / USSD | Intake outside native apps — see [order channels](./admin-app/order-channels.md) |

Full glossary: [App settings](./admin-app/app-settings.md).

### Gateways

| What you set | Effect |
|--------------|--------|
| Each provider **Active** | Method appears / initializes at checkout |
| Provider credentials | Real charges once demo placeholders are replaced |
| Stripe / COD Active | Mirrors App Settings Stripe/COD toggles |

Index: [gateways](./admin-app/gateways.md).

### Currencies, taxes, languages

| Screen | Effect |
|--------|--------|
| **Currencies** + main currency in settings | Symbol and amounts clients display |
| **Taxes** | Rates applied on cart lines |
| **Languages** (+ RTL for `ar`) | Catalogue the apps and API agree on |

See [currencies & taxes](./admin-app/currencies-taxes.md) · [languages](./admin-app/languages.md).

### Subscriptions (benefit flags)

Configure plans so membership **does** change money and logistics: restaurant commission reduce/waive, customer free delivery + discount %, driver priority job lead. See [subscriptions](./admin-app/subscriptions.md).

---

## Customer app env

| Variable | What it configures | Effect |
|----------|--------------------|--------|
| `EXPO_PUBLIC_API_URL` | API base (must end `/api`) | All REST/auth traffic |
| `EXPO_PUBLIC_DEMO_MODE` | Demo login prefill | `true` / `false` |
| `EXPO_PUBLIC_DEMO_EMAIL` / `PASSWORD` | Demo credentials | Default `demo@customer.com` / `demo123` |
| `EXPO_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Client Stripe | Card UI when Stripe is enabled server-side |
| `EXPO_PUBLIC_MAPTILER_API_KEY` | Map tiles | Map surfaces that use MapTiler |

Start: `npm start`; first native install `npm run android` / `npm run ios` (dev client, not Expo Go).

---

## Driver app env

| Variable | What it configures | Effect |
|----------|--------------------|--------|
| `EXPO_PUBLIC_API_URL` | Same `/api` base | Jobs, POD, earnings |
| `EXPO_PUBLIC_DEMO_MODE` / email / password | Demo login | Default `driver@demo.com` / `driver123` |
| `EXPO_PUBLIC_GOOGLE_MAPS_API_KEY` | Optional Google Maps | When production Android config needs Maps SDK |

Maps default to MapLibre; add Google when your store build embeds the SDK key.

---

## Restaurant app env

| Variable | What it configures | Effect |
|----------|--------------------|--------|
| `EXPO_PUBLIC_API_URL` | Shared `/api` | Orders, menu, KDS |
| `EXPO_PUBLIC_DEMO_EMAIL` / `PASSWORD` | Demo login | Default `demo@restaurant.com` / `password123` |

Use `npm run start:demo` / `start:live` (and `:localhost` variants) — do not set demo mode by hand.

---

## Admin app env

| Variable | What it configures | Effect |
|----------|--------------------|--------|
| `REACT_APP_API_URL` | REST base | CRUD + forms |
| `REACT_APP_SERVER_URL` | Origin for sockets | Live updates |

Start: `npm start`. Production: `npm run build` behind HTTPS.

---

## Branding, languages, currency, push, maps

Do **not** duplicate those walkthroughs here — configure them where they belong:

| Topic | Guide |
|-------|--------|
| Currency & taxes | [admin currencies-taxes](./admin-app/currencies-taxes.md) |
| Language catalogue | [admin languages](./admin-app/languages.md) |
| Customer language picker / RTL / locale files | [customer languages](./customer-app/languages-rtl.md) |
| Driver / restaurant languages | [delivery languages](./delivery-app/languages.md) · [restaurant languages](./restaurant-app/languages.md) |
| Push (FCM) — API service account + mobile config files | [backend getting started](./my-backend/getting-started.md) (and each mobile getting-started Branding / Android notes if present) |
| Places autocomplete | [checkout](./customer-app/checkout.md) |
| Driver maps | [delivery getting started](./delivery-app/getting-started.md) |
| App name / logo / theme | Each app’s getting-started → Branding section |

---

## CORS

```env
CORS_ORIGINS=http://localhost:3000,https://admin.your-domain.com
```

Restart the API after changes. The admin SPA needs an explicit origin; native apps are not browser CORS clients.

---

## Production checklist

1. Unique `JWT_SECRET`; live PSP secrets only on the server; no `.env` in git.
2. HTTPS for API + admin; mobiles use `https://…/api`.
3. Mongo authenticated, backed up, firewalled.
4. Explicit `CORS_ORIGINS` only.
5. Demo mode off on store builds; demo passwords rotated.
6. `migrate:status` clean before release.
7. FCM + maps production keys restricted (per app getting-started).
8. Smoke: customer order → restaurant accept → driver POD.
9. App Settings + Gateways as you intend to sell.
10. Process manager + logs for the API.
11. Privacy policy / package IDs / branding finalized for stores.

## Related

- [Launch the suite](./00-launch-suite.md)
- [Backend](./my-backend/getting-started.md) · [Customer](./customer-app/getting-started.md) · [Driver](./delivery-app/getting-started.md) · [Restaurant](./restaurant-app/getting-started.md) · [Admin](./admin-app/getting-started.md)
- [App settings](./admin-app/app-settings.md) · [Gateways](./admin-app/gateways.md) · [Currencies](./admin-app/currencies-taxes.md) · [Order channels](./admin-app/order-channels.md)
