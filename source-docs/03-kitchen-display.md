# Kitchen Display / KDS (developer)

Paperless kitchen tickets in the restaurant app, backed by order documents and demo seeds.

## UI

- Screen: `restaurant-app/screens/KitchenDisplayScreen.js`
- Registered in restaurant drawer / settings stack navigation (`navigation/DrawerNavigator.js`, `SettingsStackNavigator.js`, `screens/index.js`)
- Order cards / hooks: restaurant order hooks and shared order card components as used by live order lists

## Data flow

1. Customer places order  
2. Restaurant accepts  
3. KDS shows kitchen-oriented ticket  
4. Kitchen advances status  
5. Driver pickup  

Same `Order` documents power admin earnings and driver logistics.

## Demo seed

- `my-backend/migrations/41-orders-seed-kds-demo-tickets.js` — kitchen-oriented demo tickets for screenshots / first-run denseness

## Related

- Restaurant subscriptions & sponsored listings (monetization) sit alongside KDS in the partner app
- Run `npm run migrate:up` in `my-backend` after install so demo tickets exist
