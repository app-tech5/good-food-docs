# Order channels — Admin app

Configure intake **outside** the native mobile apps: browser web ordering, WhatsApp (Meta Cloud API), and USSD dial codes for feature phones. Every ticket still lands in the same kitchen + driver pipeline, tagged with `orderSource` (`app` / `whatsapp` / `ussd` / `web` / `admin`).

These toggles live on the same **App Settings** form as commission and wallet — scroll past money flags to the channel block. Full field glossary: [App settings](./app-settings.md). Backend behaviour: [Hybrid channels](../my-backend/channels-api.md).

## What you configure

| Field | Meaning | Effect when set |
|---|---|---|
| **Web Ordering Enabled** | Allow authenticated browser / web clients to place orders | Off → web intake refuses new orders. On → new orders can be tagged `orderSource: web` |
| **Whatsapp Enabled** | Turn on WhatsApp Cloud API for this marketplace | Off → no Meta calls. On → needs phone number ID + access token below |
| **Whatsapp Phone Number Id** | Meta phone number ID messages are sent from | Required with the token before WhatsApp does anything real |
| **Whatsapp Access Token** | Meta access token | Often hidden/masked in the UI — set via seed/secure config if the form hides it. Placeholder/"demo" tokens are skipped silently by the backend |
| **Whatsapp Notify On Status** | Push order status updates over WhatsApp | On → eligible orders with a customer phone get WhatsApp status messages |
| **Ussd Enabled** | Turn on feature-phone dial-code intake | Off → USSD sessions get "unavailable". On → needs short code + aggregator API key |
| **Ussd Short Code** | Code customers dial (e.g. `*123#`) | Must match what you registered with the aggregator |
| **Ussd Api Key** | Aggregator key | Validates sessions; demo placeholders are skipped until replaced |

**Do not confuse** these with **Wallet Cashback** / **Commission Rate** on the same screen — those are money settings, not channels.

## How to set it up

1. **Settings → App Settings** → open the active app record.
2. Scroll to **Web Ordering / WhatsApp / USSD** (below wallet cashback).
3. Enable **only** channels you have real credentials for.
4. Save.
5. Place one test order per enabled channel; in **Orders**, confirm `orderSource`.
6. For WhatsApp: change an order status and confirm a message fan-out when notify-on-status is on (real credentials only).

## Verify

| Check | Expect |
|---|---|
| All channel flags off | Only native-app orders; `orderSource` stays `app` |
| Web Ordering on | Web/authenticated intake creates `orderSource: web` |
| WhatsApp on + real Meta credentials | Status notify reaches the customer phone |
| WhatsApp on + demo token | No crash — send is skipped until you replace credentials |
| USSD on + short code + key | Dial session returns menu text, not "unavailable" |
| Any channel order | Same restaurant accept → kitchen → driver path as app orders |

## Related

- [App settings](./app-settings.md) · [Orders](./orders.md)
- Backend: [Hybrid channels](../my-backend/channels-api.md)
