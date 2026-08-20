# Hybrid order channels — Backend API

What actually happens when you flip **Web Ordering**, **WhatsApp**, or **USSD** on in Admin App Settings — not a list of webhook routes.

## The idea

An order can reach the kitchen from four doors — the native app, a browser, WhatsApp, or a feature-phone USSD menu — and all four land in the **same** `Order` document, tagged with one field: `orderSource` (`app` / `whatsapp` / `ussd` / `web` / `admin`). There is no separate "WhatsApp order queue" or "USSD kitchen" — restaurant and driver apps just see another ticket with a different source tag.

Each channel is gated by its own flags on the **one** `AppSetting` document. The backend checks those flags before it will touch Meta's API or accept a USSD session; nothing fires by default.

## What each toggle configures

| App Settings field | Type | Effect when enabled |
|---|---|---|
| `webOrderingEnabled` | boolean (default **on**) | Lets an authenticated browser/web client place an order via the channel intake path. Off → that path refuses new orders. |
| `whatsappEnabled` | boolean (default **off**) | Turns on WhatsApp Cloud API messaging: outbound order-status notifications and, if your build wires the webhook, inbound catalog ordering. |
| `whatsappPhoneNumberId` | string | Meta phone number ID the messages are sent from. Can also come from `.env` `WHATSAPP_PHONE_NUMBER_ID`. |
| `whatsappAccessToken` | string | Meta access token used to call `graph.facebook.com`. Can also come from `.env` `WHATSAPP_ACCESS_TOKEN`. |
| `whatsappVerifyToken` | string | Verify token used by Meta's webhook challenge. Falls back to `.env` `WHATSAPP_VERIFY_TOKEN`. |
| `whatsappTemplateLang` | string | Default template language (for template sends) — e.g. `en`, `fr`, `es`. |
| `whatsappNotifyOnStatus` | boolean (default **on**) | When a WhatsApp-eligible order changes status, the customer's phone gets a WhatsApp message automatically. Independent of `whatsappEnabled` being used for intake — this is the outbound leg. |
| `ussdEnabled` | boolean (default **off**) | Turns on the USSD session handler (feature-phone dial codes, e.g. `*123#`, via an aggregator like Africa's Talking). |
| `ussdShortCode` | string | The short code customers dial — must match what you configured with your aggregator. |
| `ussdApiKey` | string | Aggregator API key, used to validate/sign sessions. |

**Precedence / safety net:** every send checks its own flag first, then whether the credentials look real. App Settings values win; if they are empty, the backend can fall back to `.env` (`WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_VERIFY_TOKEN`, `WHATSAPP_TEMPLATE_LANG`). If a token or key still contains the word "demo", the backend silently skips the external call instead of erroring — WhatsApp sends and USSD ordering just won't happen until you replace those values. `whatsappNotifyOnStatus` only fires messages for orders where the customer has a phone number on file.

Credential fields (`whatsappAccessToken`, `ussdApiKey`) are the kind of thing you don't want sitting in a form screenshot — your build may hide or mask them in the Admin UI. Set real values via a migration/seed edit or a small secure-config step rather than typing them into a shared screen.

## Where the enforcement lives

- **Admin App Settings** is where an operator flips these flags — see [order channels](../admin-app/order-channels.md).
- The backend (`channelService`) is what actually reads `AppSetting` before calling Meta or answering a USSD session — the Admin toggle isn't cosmetic, it's the switch the code checks.
- Every channel order still goes through the one order pipeline: restaurant accept/prepare/ready, driver assignment, delivery — see [order lifecycle](./order-lifecycle.md).

Small "where it lives" note, not the focus of this doc: the intake surfaces are exposed under `/api/channels` (config + USSD session + channel order creation). The WhatsApp webhook verify challenge is `GET /api/channels/whatsapp`; inbound/status callbacks are `POST /api/channels/whatsapp`. Outbound sends now return Meta `messageId` when accepted so operators can correlate status callbacks.

## Smoke test

| Step | Expect |
|------|--------|
| All three flags off | Only native-app orders can be created; `orderSource` is always `app` |
| Enable `webOrderingEnabled` | Authenticated web client can place an order; order shows `orderSource: "web"` |
| Enable `whatsappEnabled` with real phone number ID + token | A status change on a customer's order arrives as a WhatsApp message |
| Enable `whatsappEnabled` with placeholder/demo token | Message send is skipped (no error, no message) — replace credentials |
| Enable `ussdEnabled` + short code + key | Dialing the configured session flow returns menu text instead of "Service unavailable" |
| Any channel order | Same restaurant/driver pipeline picks it up; admin **Orders** shows the correct `orderSource` |

## Related

- [Admin order channels](../admin-app/order-channels.md)
- [Order lifecycle](./order-lifecycle.md)
- [Kitchen Display](../restaurant-app/kitchen-display.md)
