# Source documentation (CodeCanyon pack)

Technical HOW-TO guides that ship with the source ZIP. Same **app split** as the online HTML docs (customer, driver, restaurant, admin, backend) — but written for buyers who already unzipped the suite and need commands, `.env`, and smoke tests.

| | Online HTML docs | This `source-docs/` pack |
|---|---|---|
| Audience | Shoppers & evaluators | Buyers with the ZIP |
| Tone | Soft product stories | Step-by-step launch & configuration |
| Layout | Pages under each app | **Same folders by app** |

## Folder map (mirrors the online site)

```
source-docs/
  README.md                 ← you are here
  00-launch-suite.md        ← boot the whole suite once
  environment-config.md     ← shared env / branding / production checklist
  my-backend/
    getting-started.md
  customer-app/
    getting-started.md
    intelligence.md
  delivery-app/
    getting-started.md
    logistics.md
  restaurant-app/
    getting-started.md
    kitchen-display.md
  admin-app/
    getting-started.md
    monetization.md
    market.md
```

## Recommended read order

1. **[Launch the whole suite](./00-launch-suite.md)**
2. **[Backend](./my-backend/getting-started.md)**
3. Per app (any order after the API is up):
   - [Customer](./customer-app/getting-started.md)
   - [Driver](./delivery-app/getting-started.md)
   - [Restaurant](./restaurant-app/getting-started.md)
   - [Admin](./admin-app/getting-started.md)
4. **[Environment & branding](./environment-config.md)**
5. Feature HOW-TOs under the owning app:
   - [Customer — Intelligence](./customer-app/intelligence.md)
   - [Driver — Logistics & POD](./delivery-app/logistics.md)
   - [Restaurant — Kitchen Display](./restaurant-app/kitchen-display.md)
   - [Admin — Monetization](./admin-app/monetization.md)
   - [Admin — Market](./admin-app/market.md)

## Index by app

### Shared
| Guide | Path |
|-------|------|
| Launch the suite | [00-launch-suite.md](./00-launch-suite.md) |
| Environment & branding | [environment-config.md](./environment-config.md) |

### Backend (API)
| Guide | Path |
|-------|------|
| Getting started | [my-backend/getting-started.md](./my-backend/getting-started.md) |

### Customer app
| Guide | Path |
|-------|------|
| Getting started | [customer-app/getting-started.md](./customer-app/getting-started.md) |
| AI intelligence | [customer-app/intelligence.md](./customer-app/intelligence.md) |

### Delivery app (driver)
| Guide | Path |
|-------|------|
| Getting started | [delivery-app/getting-started.md](./delivery-app/getting-started.md) |
| Logistics & POD | [delivery-app/logistics.md](./delivery-app/logistics.md) |

### Restaurant app
| Guide | Path |
|-------|------|
| Getting started | [restaurant-app/getting-started.md](./restaurant-app/getting-started.md) |
| Kitchen Display | [restaurant-app/kitchen-display.md](./restaurant-app/kitchen-display.md) |

### Admin app
| Guide | Path |
|-------|------|
| Getting started | [admin-app/getting-started.md](./admin-app/getting-started.md) |
| Monetization | [admin-app/monetization.md](./admin-app/monetization.md) |
| Market & languages | [admin-app/market.md](./admin-app/market.md) |

## Conventions

- **“The suite”** = backend API + customer + driver + restaurant + admin.
- Commands assume you are inside the matching project folder (`my-backend`, `customer-app`, `delivery-app`, `restaurant-app`, `admin-app`).
- Demo credentials come from each app’s `.env.example` after migrations. Change them before any public deploy.
- Keep the **same API base URL** (including `/api`) across every client.
