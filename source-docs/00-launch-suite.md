# Launch the whole suite

This guide is the big-picture bootstrap for buyers who just unzipped the source pack. Follow it once to get MongoDB, the API, the admin dashboard, and the three mobile apps talking to each other — then run a full order smoke test.

If you only need one app later, jump to that app’s getting-started page. On first install, start here.

## What you are launching

| Piece | Role | Default local URL |
|-------|------|-------------------|
| MongoDB | Data store | `mongodb://127.0.0.1:27017/<database>` |
| Backend API (`my-backend`) | Auth, orders, payments, logistics, settings | `http://localhost:5000` (JSON under `/api`) |
| Admin web app | Operator console | `http://localhost:3000` (CRA default) |
| Customer app | Ordering | Expo Metro + device/emulator |
| Restaurant app | Accept / KDS / partner tools | Expo Metro + device/emulator |
| Driver app | Deliveries + POD | Expo Metro + device/emulator |

All clients must share **one** API base that ends with `/api`, for example `http://localhost:5000/api` or `http://192.168.x.x:5000/api` on a phone.

## Prerequisites (install once)

1. **Node.js LTS** — prefer **20+** (mobile apps expect modern Expo tooling). Verify with `node -v` and `npm -v`.
2. **MongoDB** — local install or Docker (`mongo:7` on port `27017` is the usual pattern).
3. **Expo / native tooling** for the mobiles:
   - Android Studio (emulator or USB device), and/or
   - Xcode on macOS (iOS Simulator / device).
4. A code editor for `.env` files (plain text — no smart quotes).

These apps use **development builds** (`expo-dev-client`), not Expo Go. Plan on `npm run android` or `npm run ios` once per mobile project so a native client is installed.

## Boot order (do not skip steps)

Run each step until it succeeds before starting the next.

### 1. Start MongoDB

Confirm the database process is listening. If you use Docker:

```bash
docker ps
```

Your connection string (later put in the backend `.env` as `MONGO_URI`) should look like:

```env
MONGO_URI=mongodb://127.0.0.1:27017/your-database-name
```

Optional split vars (`MONGODB_HOST`, `MONGODB_PORT`, `MONGODB_DATABASE`) appear in `.env.example` for tooling; the server path that matters for day-one launch is a valid `MONGO_URI`.

### 2. Configure and migrate the API

In the backend project:

```bash
cd my-backend
cp .env.example .env
# edit MONGO_URI, JWT_SECRET, PORT, CORS_ORIGINS
npm install
npm run test:db          # optional connectivity check
npm run migrate:up
npm run migrate:status
npm start                # or: npm run dev
```

You should see the API listening on **`PORT`** (default **5000**). Migrations seed languages, app settings, demo users, subscription tiers, sponsored samples, kitchen demo tickets, and related marketplace defaults — so the apps look alive on first open.

Details: [Backend getting started](./my-backend/getting-started.md).

### 3. Start the admin dashboard

```bash
cd admin-app
npm install
# set REACT_APP_SERVER_URL / REACT_APP_API_URL if not using localhost defaults
npm start
```

Sign in with an admin account that exists after migrations (demo presets often use `admin@example.com` / `admin123` — replace these before production). Confirm lists and **App Settings** load.

Details: [Admin getting started](./admin-app/getting-started.md).

### 4. Start the mobile apps

Point each app’s `EXPO_PUBLIC_API_URL` at the **same** `/api` base the admin uses.

| App | Typical start |
|-----|----------------|
| Customer | `npm start` (or `npm run android` / `ios` for first native install) |
| Driver | same pattern in `delivery-app` |
| Restaurant | prefer `npm run start:demo` or `npm run start:live` (see restaurant guide) |

On a **physical phone**, replace `localhost` with your computer’s LAN IP. On Android emulator, `10.0.2.2` often reaches the host machine’s `localhost`.

Details: [customer](./customer-app/getting-started.md) · [driver](./delivery-app/getting-started.md) · [restaurant](./restaurant-app/getting-started.md).

## Shared API URL checklist

Before you debug “login failed” on three apps at once, verify:

1. Backend responds: open `http://<host>:5000/api` (or hit a known health/login endpoint) from the **same machine** that will run clients.
2. Every mobile `.env` has `EXPO_PUBLIC_API_URL=http://<host>:5000/api`.
3. Admin uses `REACT_APP_API_URL=http://<host>:5000/api` (and `REACT_APP_SERVER_URL=http://<host>:5000/` for sockets if you override defaults).
4. Backend `CORS_ORIGINS` includes the admin origin (for example `http://localhost:3000`).
5. After changing any `EXPO_PUBLIC_*` value, **restart Metro** so Expo reinlines env vars.

## Smoke test checklist (order → accept → deliver)

Use this once everything is up. It proves money, kitchen, and courier paths without reading feature docs yet.

1. **Customer** — Sign in (demo: `demo@customer.com` / `demo123` if seeded). Place a delivery order to a restaurant that exists in the catalog.
2. **Restaurant** — Sign in (`demo@restaurant.com` / `password123` typical demo). Accept the new order. Optionally open **Kitchen Display** and advance the ticket.
3. **Driver** — Sign in (`driver@demo.com` / `driver123` typical demo). Go online, accept the job (or a suggested batch if offered), navigate to drop-off.
4. **Complete with POD** — Finish delivery with **photo and/or signature** when the app asks for proof.
5. **Admin** — Refresh orders / earnings views and confirm the order appears with a sensible platform vs restaurant split.
6. **Customer** — Confirm the order reaches a delivered state and tracking looked live during the trip.

If any hop fails, check API URL + JWT login first, then role permissions, then that migrations actually ran (`npm run migrate:status`).

## Demo vs live

| Mode | Purpose | What to expect |
|------|---------|----------------|
| **Demo** | Investor walkthroughs, product demos, offline-friendly UI demos | Login fields may prefill; some restaurant flows use demo handlers; seeded tickets and campaigns appear after `migrate:up` |
| **Live** | Real API traffic against your Mongo data | Prefill off; every action hits `/api`; payment keys and FCM matter for full flows |

**Restaurant app:** do **not** set `EXPO_PUBLIC_DEMO_MODE` by hand in `.env`. Use:

- `npm run start:demo` / `npm run start:demo:localhost`
- `npm run start:live` / `npm run start:live:localhost`

**Customer & driver:** `EXPO_PUBLIC_DEMO_MODE=true|false` plus demo email/password in `.env` (see each `.env.example`).

For a first successful smoke test, **demo mode + migrated seed data** is the fastest path. Switch to live when you are ready to exercise Stripe keys, real push, and empty (or production-like) data.

## What to read next

- Deeper env / branding / production: [environment-config.md](./environment-config.md)
- Turn on commissions, plans, ads, wallet: [Monetization](./admin-app/monetization.md)
- Languages, currency, channels: [Market adaptability](./admin-app/market.md)
- KDS, logistics POD, intelligence demos: [03](./restaurant-app/kitchen-display.md) · [04](./delivery-app/logistics.md) · [05](./customer-app/intelligence.md)
