# Getting started — Backend API

Goal: install the Node API, connect MongoDB, apply migrations, and confirm the server answers on port **5000** (or the `PORT` you chose) before any client starts.

## Prerequisites

- Node.js LTS (20+ recommended)
- A reachable MongoDB instance (local or Docker)
- Terminal open in the `my-backend` project root (where `package.json` lives)

Boot order reminder: **Mongo running → `.env` → `npm install` → migrations → `npm start`**.

## 1. Install dependencies

```bash
cd my-backend
npm install
```

Wait for a clean finish. The API does not embed a database engine; MongoDB must already be reachable.

## 2. Create `.env`

Copy the example and edit values:

```bash
cp .env.example .env
```

### Required day-one keys

| Variable | Purpose | Example |
|----------|---------|---------|
| `MONGO_URI` | Full Mongo connection string | `mongodb://127.0.0.1:27017/your-database-name` |
| `JWT_SECRET` | Signs auth tokens — **change before production** | long random string |
| `PORT` | HTTP listen port | `5000` |
| `CORS_ORIGINS` | Comma-separated browser origins allowed to call the API | `http://localhost:3000` |
| `NODE_ENV` | Runtime mode | `development` |

Clients will call `http://<host>:<PORT>/api/...`. Keep that base URL identical in customer, driver, restaurant, and admin configs.

### Optional Mongo split vars

`.env.example` also documents `MONGODB_HOST`, `MONGODB_PORT`, `MONGODB_DATABASE`, and `MONGO_DOCKER_CONTAINER`. These help local helper scripts. The server path you must get right first is still **`MONGO_URI`**.

### Stripe (when you enable card / Connect flows)

| Variable | Purpose |
|----------|---------|
| `STRIPE_SECRET_KEY` | Server Stripe secret (`sk_test_...` locally) |
| `STRIPE_CONNECT_COUNTRY` | Connect country code (example: `FR`) |
| `STRIPE_CONNECT_RETURN_URL` | Driver Connect return deep link |
| `STRIPE_CONNECT_REFRESH_URL` | Driver Connect refresh deep link |

You can leave Stripe empty for pure demo / cash flows; set these before live card charging or Connect onboarding.

### Firebase (push from the API)

| Variable | Purpose |
|----------|---------|
| `FIREBASE_SERVICE_ACCOUNT_JSON` | Single-line JSON string of the Firebase Admin service account |

Auth and orders live in **this API + MongoDB**, not in Firestore. Firebase here is for **FCM push** only. Skip it until you need device notifications.

### VPS sync helpers (optional)

Vars such as `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`, `VPS_MONGO_URI`, `VPS_PM2_NAME` support `npm run sync:mongo:vps`. Ignore them for a local first run.

## 3. Verify MongoDB

```bash
npm run test:db
```

Fix connection errors before migrating. Common issues: Mongo not running, wrong port in `MONGO_URI`, or Docker container name/port mismatch.

## 4. Run migrations

Migrations create collections and seed baseline marketplace data (settings, languages, demo accounts, subscription tiers, sponsored samples, kitchen tickets, wallet defaults, and related monetization / market seeds).

```bash
npm run migrate:up
npm run migrate:status
```

Useful companions:

| Script | What it does |
|--------|----------------|
| `npm run migrate:up` | Apply pending migrations |
| `npm run migrate:status` | Show applied vs pending |
| `npm run migrate:down` | Roll back one step (use carefully) |
| `npm run migrate:create` | Scaffold a new migration file |

On a fresh database, always run **`migrate:up` once** before opening the apps, or lists will look empty and demo logins may fail.

## 5. Start the API

Production-style process:

```bash
npm start
```

(`prestart` may ensure a local Mongo helper is up — still keep your own Mongo healthy.)

Auto-reload during development:

```bash
npm run dev
```

## 6. Verify it is alive

1. Confirm the process is listening on `PORT` (default **5000**).
2. From the same machine, request the API base (for example open or `curl` `http://localhost:5000/api` / a documented login route).
3. Attempt an admin or demo user login from the admin app or a mobile client.
4. If browsers call the API, ensure `CORS_ORIGINS` includes that origin and restart the server after editing `.env`.

### Changing the port

If you set `PORT=6000`, update **every** client:

- Mobiles: `EXPO_PUBLIC_API_URL=http://<host>:6000/api`
- Admin: `REACT_APP_API_URL=http://<host>:6000/api` and `REACT_APP_SERVER_URL=http://<host>:6000/`

## Security notes

- Never commit `.env`.
- Rotate `JWT_SECRET` and Stripe keys for production.
- Restrict `CORS_ORIGINS` to real admin (and any web) origins — not `*`.

## Stack & where things live (for launch)

The API is **Node.js + Express** with **MongoDB** (Mongoose), JWT auth, file uploads, i18n, and **migrate-mongo** for schema/seed evolution. Real-time channels (for example live tracking) are available when enabled in your deploy.

| You want to… | Look here |
|--------------|-----------|
| Install & run | `npm install`, then `npm run migrate:up`, then `npm start` / `npm run dev` |
| Secrets & DB | `.env` from `.env.example` (`MONGO_URI`, `JWT_SECRET`, `PORT`, `CORS_ORIGINS`, …) |
| Evolve data | `migrations/` + `migrate-mongo-config.js` |
| HTTP entry | `src/server.js` mounts routes under `/api` |
| Auth / roles | Auth middleware + role checks on routes |
| Manual API exploration | `postman_collection.json` when present |
| Connectivity check | `npm run test:db` (if scripted in `package.json`) |

Default HTTP port is **5000** when `PORT` is unset — every mobile/admin client must use the same host:port (and `/api` where required).

Version baseline is typically `1.0.0` in `package.json`.

## Project name & port (operators)

### Optional rename

Update `package.json` `"name"` / `"version"` if you rename the backend folder for your own tooling. This does not change mobile branding.

### Changing `PORT`

If you set e.g. `PORT=6000` in `.env`:

1. Restart the API.
2. Update **every** client API URL to the new host:port (and keep `/api` where required):
   - Mobiles: `EXPO_PUBLIC_API_URL`
   - Admin: `REACT_APP_API_URL` / `REACT_APP_SERVER_URL`
3. Ensure `CORS_ORIGINS` still lists your admin (and any web) origins.

Mismatched ports are the most common “apps look broken” false alarm after a backend tweak.

## Next steps

- [Launch the whole suite](../00-launch-suite.md) for boot order and smoke test.
- [Environment & branding](../environment-config.md) for reachability, FCM, and production checklist.
- Backend feature HOW-TOs: [order lifecycle](./order-lifecycle.md) · [payments & wallet](./payments-wallet.md) · [AI & pricing](./intelligence-engine.md) · [logistics](./logistics-engine.md) · [channels](./channels-api.md) — full list in [README](../README.md).
