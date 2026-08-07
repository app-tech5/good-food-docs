# Getting started — Customer app

Goal: point the customer mobile app at your running API, start Expo with a development build, and complete a first login so you can browse restaurants and place an order.

## Before you start

1. Backend is up with migrations applied — see [Backend getting started](../my-backend/getting-started.md).
2. Node.js **20+** and Android Studio and/or Xcode are installed.
3. You understand that **Expo Go is not supported**. Install a **development build** once with `npm run android` or `npm run ios`.

## 1. Install

```bash
cd customer-app
npm install
```

## 2. Configure the API URL

Copy the example env and edit it:

```bash
cp .env.example .env
```

The critical variable:

```env
EXPO_PUBLIC_API_URL=http://localhost:5000/api
```

| Situation | What to put in `EXPO_PUBLIC_API_URL` |
|-----------|--------------------------------------|
| iOS Simulator / same-machine tooling that can reach host localhost | `http://localhost:5000/api` |
| Android emulator | Often `http://10.0.2.2:5000/api` (emulator alias for host loopback) |
| Physical phone on Wi‑Fi | `http://<your-LAN-IP>:5000/api` (never `localhost` — that is the phone itself) |
| Deployed API | `https://your-domain.com/api` |

Expo inlines `EXPO_PUBLIC_*` at Metro start. **Restart Metro** after every env change.

### Demo login helpers (optional)

```env
EXPO_PUBLIC_DEMO_MODE=true
EXPO_PUBLIC_DEMO_EMAIL=demo@customer.com
EXPO_PUBLIC_DEMO_PASSWORD=demo123
```

With demo mode on, the login screen can prefill those credentials (they must exist in Mongo after `migrate:up`).

### Optional keys

| Variable | When you need it |
|----------|------------------|
| `EXPO_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Card checkout against Stripe |
| `EXPO_PUBLIC_MAPTILER_API_KEY` | Map tiles / map features that expect MapTiler |

## 3. Run Expo

First time on a device/emulator (builds + installs the native client):

```bash
npm run android
# or
npm run ios
```

Later sessions:

```bash
npm start
# optional: npm run start:localhost
```

Then open the already-installed development client (or press `a` / `i` in the Expo terminal when it resolves your device).

## 4. LAN vs localhost (the usual first bug)

If login spins forever or network errors appear:

1. Confirm the API answers from the **same network path** the phone uses (browser or `curl` to that host).
2. Fix `EXPO_PUBLIC_API_URL` — physical devices need the LAN IP.
3. Ensure phone and computer share Wi‑Fi (guest networks that isolate clients break LAN access).
4. Restart Metro after editing `.env`.
5. For USB Android debugging of Metro, `adb reverse tcp:8081 tcp:8081` can help the packager; the **API port** still needs a reachable host in `EXPO_PUBLIC_API_URL`.

More detail: [environment-config.md](../environment-config.md) → API reachability.

## 5. First customer login

1. Open the app → sign-in screen.
2. Use seeded demo credentials (`demo@customer.com` / `demo123`) or an account you created.
3. You should land on home / restaurant discovery fed by the API.
4. Place a small delivery order as a smoke test (restaurant + driver guides complete the loop).

If auth fails with a reachable API, re-check migrations and that the user role is a **customer** account.

## What to try after login

- Browse restaurants and open a menu.
- Add to cart and checkout (cash / wallet / card depending on keys and admin gateway settings).
- Watch live tracking once a driver is assigned.
- Open **Subscriptions** / wallet screens if you are following the [monetization guide](../admin-app/monetization.md).
- Switch language in Settings (EN / FR / ES / AR) — see [market adaptability](../admin-app/market.md).


## Stack & where things live (for launch)

The customer app is **React Native + Expo** (Android & iOS from one codebase). It talks to your HTTP API; it does not store the marketplace database on the phone.

| You want to… | Look here |
|--------------|-----------|
| Point the app at your API | `.env` → `EXPO_PUBLIC_API_URL` (restart Metro after changes) |
| Demo login helpers | `.env` → `EXPO_PUBLIC_DEMO_*` |
| Stripe / maps publishable keys | `.env` → `EXPO_PUBLIC_STRIPE_*`, `EXPO_PUBLIC_MAPTILER_*` |
| Change copy / languages | `lang/` (EN / FR / ES / AR) |
| Find a screen while debugging UX | `screens/` (Home, cart, tracking, wallet, …) |
| Follow an API call | `api/` (auth, restaurants, orders, …) |

You do **not** need a full source-tree map to launch. Configure `.env`, start the API, then `npm run android` / `npm run ios` as above.

**Baseline version** in `package.json` is typically `1.0.0` — bump it when you ship your own builds.

## Branding & personalization

Prefer `.env` for API and demo flags (see above). Runtime labels also appear in `config/index.js` (or equivalent) as `APP_NAME` / `VERSION`.

### Change the public app name

1. Update Expo metadata in `app.json` / `app.config.*`: `expo.name`, `slug`, and store identifiers (`ios.bundleIdentifier`, `android.package`).
2. Update the in-app label in config (`APP_NAME`).
3. If native folders already exist (prebuild), also update:
   - iOS: `Info.plist` → `CFBundleDisplayName`
   - Android: `android/app/src/main/res/values/strings.xml` → `app_name`
4. Restart Metro (`npm start`) so bundler caches clear.

### Logo

Replace the logo file under `assets/images` and **keep the exact same filename** so you do not chase path changes. Restart the app afterward.

### Theme / colors

Shared colors and theme tokens live under `global/` (and related asset config). Adjust there for brand colors.

### Auth note

Customer login hits the suite auth endpoints on your API (same host/port as every other client). Keep `/api` consistent with the backend.

## Next

- Full suite smoke test: [00-launch-suite.md](../00-launch-suite.md)
- Branding & production env: [environment-config.md](../environment-config.md)
- Feature HOW-TOs (same topics as the online sidebar): [discovery](./discovery.md) · [checkout](./checkout.md) · [tracking](./order-tracking.md) · [wallet](./wallet.md) · [recommendations](./recommendations.md) · [languages](./languages-rtl.md) — see [README index](../README.md)
