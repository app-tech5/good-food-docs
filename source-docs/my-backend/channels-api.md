# Hybrid channels — Backend API

WhatsApp / USSD / web intake with `orderSource` tagging (`/api/channels` and related webhooks).

## Operator steps

1. Admin → **App Settings** / channel fields — enable only channels you have credentials for.
2. WhatsApp: Meta phone number ID + token; verify webhook path your build documents.
3. USSD: aggregator CON/END webhook as seeded / configured.
4. Web intake: authenticated place-order with `orderSource` = `web` (or similar).
5. Place one test order per enabled channel; confirm source on the order in admin.

Channels must land in the **same** kitchen and driver pipeline — not a second system.

## Related

- [Admin order channels](../admin-app/order-channels.md)
- [Order lifecycle](./order-lifecycle.md)
- [Kitchen Display](../restaurant-app/kitchen-display.md)
