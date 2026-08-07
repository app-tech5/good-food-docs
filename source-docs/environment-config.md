# Environment & branding configuration

Deeper reference for buyers who finished the getting-started guides and need a single place for **API reachability**, **env tables**, **branding**, **i18n edits**, **FCM**, **maps keys**, **CORS**, and a **production checklist**.

Keep this next to the repos from the ZIP; it complements (but does not replace) the public online Environment setup HTML.

## API reachability matrix

Every mobile and admin client must use a host **that device can route to**.

| Client runs on | Backend on your laptop | Suggested API base |
|----------------|------------------------|--------------------|
| Same laptop browser (admin) | `localhost:5000` | `http://localhost:5000/api` |
| iOS Simulator | laptop | `http://localhost:5000/api` often works |
| Android emulator | laptop | `http://10.0.2.2:5000/api` (host loopback alias) |
| Physical phone / tablet | laptop on Wi‑Fi | `http://<LAN-IP>:5000/api` |
| Any client | VPS / domain | `https://your-domain.com/api` |

Rules of thumb:

1. On a phone, `localhost` means the phone — not your computer.
2. Guest Wi‑Fi with client isolation breaks LAN demos.
3. After changing `EXPO_PUBLIC_*`, restart Metro so values reinline.
4. Match **protocol + host + port + `/api`** across customer, driver, restaurant, and admin.

Backend `CORS_ORIGINS` must include browser origins (admin on `http://localhost:3000`, plus production admin URLs).

---

## Backend env table (`my-backend`)

| Variable | Required | Notes |
|----------|----------|-------|
| `MONGO_URI` | Yes | e.g. `mongodb://127.0.0.1:27017/your-database-name` |
| `JWT_SECRET` | Yes | Long random string; rotate for production |
| `PORT` | Yes | Default `5000` |
| `NODE_ENV` | Recommended | `development` / `production` |
| `CORS_ORIGINS` | Yes for browsers | Comma-separated origins |
| `STRIPE_SECRET_KEY` | For card / Connect | `sk_test_...` locally |
| `STRIPE_CONNECT_COUNTRY` | For Connect | e.g. `FR` |
| `STRIPE_CONNECT_RETURN_URL` | For Connect | Driver return deep link |
| `STRIPE_CONNECT_REFRESH_URL` | For Connect | Driver refresh deep link |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | For FCM send | Single-line service account JSON |
| `MONGODB_HOST` / `PORT` / `DATABASE` | Optional | Helper scripts |
| `VPS_*` / `LOCAL_BACKUP_BASE` | Optional | `npm run sync:mongo:vps` |

Scripts you will use constantly: `npm run migrate:up`, `migrate:status`, `npm start`, `npm run dev`, `npm run test:db`.

---

## Customer app env

| Variable | Notes |
|----------|-------|
| `EXPO_PUBLIC_API_URL` | Must end with `/api` |
| `EXPO_PUBLIC_DEMO_MODE` | `true` / `false` |
| `EXPO_PUBLIC_DEMO_EMAIL` | Default demo `demo@customer.com` |
| `EXPO_PUBLIC_DEMO_PASSWORD` | Default demo `demo123` |
| `EXPO_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Optional card checkout |
| `EXPO_PUBLIC_MAPTILER_API_KEY` | Optional maps / tiles |

Start: `npm start`, first native install `npm run android` / `npm run ios`.

---

## Driver app env

| Variable | Notes |
|----------|-------|
| `EXPO_PUBLIC_API_URL` | Same `/api` base as other apps |
| `EXPO_PUBLIC_DEMO_MODE` | Prefill login when true |
| `EXPO_PUBLIC_DEMO_EMAIL` | Default `driver@demo.com` |
| `EXPO_PUBLIC_DEMO_PASSWORD` | Default `driver123` |
| `EXPO_PUBLIC_GOOGLE_MAPS_API_KEY` | Optional / production Android needs |

Driver maps are MapLibre-oriented by default; still configure Google keys when your production Android build requires Maps SDK entries in Expo config.

---

## Restaurant app env

| Variable | Notes |
|----------|-------|
| `EXPO_PUBLIC_API_URL` | Shared `/api` base |
| `EXPO_PUBLIC_DEMO_EMAIL` | Default `demo@restaurant.com` |
| `EXPO_PUBLIC_DEMO_PASSWORD` | Default `password123` |

**Do not** set `EXPO_PUBLIC_DEMO_MODE` by hand. Use:

- `npm run start:demo` / `start:demo:localhost`
- `npm run start:live` / `start:live:localhost`

---

## Admin app env

| Variable | Notes |
|----------|-------|
| `REACT_APP_API_URL` | REST base, e.g. `http://localhost:5000/api` |
| `REACT_APP_SERVER_URL` | Server origin for sockets, e.g. `http://localhost:5000/` |

Start: `npm start`. Production: `npm run build` and host static files over HTTPS.

Demo login presets often include `admin@example.com` / `admin123` — change before sharing the dashboard.

---

## Branding (name, logo, colors)

### Mobile apps (Expo)

1. Update the visible **name**, **slug**, and store identifiers in each app’s Expo config (`app.json` / app config).
2. Update any in-app `APP_NAME` (or equivalent) config label so splash/about screens match the store name.
3. Replace logo / icon image assets **keeping the same filenames** when the project references fixed asset names — then rebuild the development client if native icons changed.
4. Adjust theme colors through the app’s existing global theme / palette entries rather than one-off hardcoding on every screen.

### Admin web

1. Set `<title>` and meta description in `public/index.html`.
2. Update `public/manifest.json` `name` / `short_name` for PWA labelling.
3. Replace the public logo asset the header imports.
4. Tune global CSS variables / theme sparingly so lists and forms stay consistent.

### Backend

The API has no consumer-facing brand chrome. Optionally rename the npm `package.json` `name` for your org; always keep client API URLs in sync if you change `PORT`.

---

## i18n edit approach

Shipped locales: **EN, FR, ES, AR** (Arabic RTL).

1. Copy the English locale file structure for the language you edit.
2. Translate **values only** — keep keys identical.
3. Register a brand-new locale the same way existing locales are registered in that app’s i18n entry.
4. In admin **Languages**, upsert code / name / default / `rtl` so the API and clients agree.
5. Restart Metro or the admin dev server after edits.

Customers can switch language in Settings; device locale may auto-select when a pack exists.

---

## Firebase Cloud Messaging (FCM)

Auth and database remain **JWT + Mongo via your API**. Firebase is for **push**.

1. Create a Firebase project; register Android/iOS apps for customer, driver, and restaurant as needed.
2. Download `google-services.json` / iOS plist into each mobile app per Expo / native setup for that repo.
3. Enable Cloud Messaging only — you do not need Firebase Auth or Firestore for the core suite.
4. Put the Admin SDK service account JSON into backend `FIREBASE_SERVICE_ACCOUNT_JSON` (single line).
5. Send a test order event and confirm a device notification.

---

## Maps keys

1. **Google Cloud** — enable Places and/or Maps SDK for Android/iOS depending on which apps need them; create an API key; restrict by app / API where possible.
2. **Expo Android** — when required, set `expo.android.config.googleMaps.apiKey` in app config and rebuild.
3. **Customer** — MapTiler via `EXPO_PUBLIC_MAPTILER_API_KEY` when used; Places autocomplete needs a Google key + billing on the Google project.
4. **Driver** — MapLibre default; add Google key when your production checklist says the Android build needs it.
5. Rebuild native binaries after key changes for store/dev clients that embed keys at build time.

---

## CORS

On the API:

```env
CORS_ORIGINS=http://localhost:3000,https://admin.your-domain.com
```

Restart the API after changes. Mobile apps calling JSON over HTTP(S) are not browser CORS clients, but the **admin** SPA is.

---

## Production checklist

1. **Secrets** — unique `JWT_SECRET`; live Stripe keys only on the server; no `.env` in git.
2. **HTTPS** — API and admin behind TLS; mobiles use `https://.../api`.
3. **Mongo** — authenticated, backed up, not exposed publicly without firewall rules.
4. **CORS** — explicit origins only.
5. **Demo mode** — off on store builds; demo passwords rotated or removed.
6. **Migrations** — `migrate:status` clean on the production database before release.
7. **FCM + maps** — production keys and restricted API credentials.
8. **Smoke test** — customer order → restaurant accept → driver POD on production-like data.
9. **Monitoring** — process manager (e.g. PM2) for the API; log rotation; error tracking as you prefer.
10. **Legal / store** — privacy policy URLs, package IDs, and branding finalized before submission.

## Related guides

- [Launch the suite](./00-launch-suite.md)  
- [Backend](./my-backend/getting-started.md) · [Customer](./customer-app/getting-started.md) · [Driver](./delivery-app/getting-started.md) · [Restaurant](./restaurant-app/getting-started.md) · [Admin](./admin-app/getting-started.md)  
- Feature HOW-TOs: [Monetization](./admin-app/monetization.md) · [Market](./admin-app/market.md) · [KDS](./restaurant-app/kitchen-display.md) · [Logistics](./delivery-app/logistics.md) · [Intelligence](./customer-app/intelligence.md)
