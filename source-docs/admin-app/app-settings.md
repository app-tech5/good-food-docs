# App Settings — Admin app

This is the single record (`AppSetting`) that holds platform-wide defaults: branding, commission baseline, delivery defaults, notification toggles, wallet cashback, and the alternate order-intake channels (WhatsApp / USSD / Web). Every restaurant and order in the marketplace inherits these defaults unless a screen says otherwise.

## What you configure

### Platform basics

| Field | Meaning | Effect when set |
|---|---|---|
| **App Name** (`appName`) | Brand name shown in emails, receipts, and some UI copy | Changes the name customers/restaurants see in system-generated text |
| **Support Email** (`supportEmail`) | Contact address surfaced to customers | Used as the reply-to / help address in emails and support links |
| **Default Language** (`defaultLanguage`) | Fallback locale when a client doesn't send one | New sessions without a saved preference render in this language |
| **Timezone** (`timezone`) | Reference timezone for reports and scheduling | Report date ranges and "today" boundaries use this timezone |
| **Maintenance Mode** (`isMaintenance`) | Global kill switch | When **on**, treat the marketplace as closed for maintenance — stop onboarding new orders before flipping this |

### Commission & payments

| Field | Meaning | Effect when set |
|---|---|---|
| **Commission Rate** (`commissionRate`, 0–100) | Marketplace baseline commission % taken from restaurant sales | Applies to every restaurant that doesn't have its own `commission_rate` override and isn't on a subscription that waives/reduces commission (see [subscriptions](./subscriptions.md)) |
| **Stripe Enabled** (`stripeEnabled`) | Turns Stripe card payments on for the marketplace | On → Stripe can take cards (and syncs the Stripe row **Active** under Gateways). Off → card checkout and payment intents are refused |
| **Cash On Delivery Enabled** (`cashOnDeliveryEnabled`) | Turns cash-on-delivery on for the marketplace | On → customers can pay on delivery (and syncs the COD gateway **Active**). Off → COD orders and COD payment methods are refused |

### Delivery defaults

| Field | Meaning | Effect when set |
|---|---|---|
| **Delivery Fee** (`deliveryFee`) | Flat fee charged when no per-restaurant/zone fee applies | Added to every delivery order's total as the baseline delivery charge |
| **Free Delivery Threshold** (`freeDeliveryThreshold`) | Cart subtotal above which delivery is free | Orders at or above this amount drop the delivery fee automatically |
| **Max Delivery Distance** (`maxDeliveryDistance`, km/mi per your locale) | Radius drivers/restaurants will serve | Customers outside this distance from a restaurant can't check out for delivery from it |

### Notifications

| Field | Meaning | Effect when set |
|---|---|---|
| **Send Order Emails** (`sendOrderEmails`) | Email receipts/status updates | When **on**, customers get emails at key order milestones |
| **Send SMS Notifications** (`sendSMSNotifications`) | SMS status updates via Twilio | Requires `twilioSID` below; when **on**, key order events also fire an SMS |

### Integration keys

| Field | Meaning | Effect when set |
|---|---|---|
| **Google Maps Api Key** (`googleMapsApiKey`) | Key used for geocoding/distance/maps features | Leaving this blank breaks map previews and distance-based delivery checks |
| **Twilio Sid** (`twilioSID`) | Twilio account SID for SMS | Required for `sendSMSNotifications` to actually send anything |

### Wallet cashback & refunds

| Field | Meaning | Effect when set |
|---|---|---|
| **Wallet Cashback Enabled** (`walletCashbackEnabled`) | Turns on automatic cashback to customer wallets | When **on**, a delivered order credits `walletCashbackPercent` of its value back to the customer's wallet |
| **Wallet Cashback Percent** (`walletCashbackPercent`, 0–100) | Cashback rate | Only matters while cashback is enabled; higher = more margin given back per order |
| **Wallet Instant Refund Enabled** (`walletInstantRefundEnabled`) | Auto-refund to wallet on cancellation | When **on** (default), a cancelled order refunds instantly to the customer's wallet instead of waiting on a manual/gateway refund |

### Alternate order channels

These control intake **outside** the native mobile apps. See [order channels](./order-channels.md) for the full walkthrough — summary here:

| Field | Meaning | Effect when set |
|---|---|---|
| **Whatsapp Enabled** (`whatsappEnabled`) | Lets customers order via WhatsApp | Requires `whatsappPhoneNumberId` + `whatsappAccessToken` below; orders created this way are tagged `orderSource: whatsapp` |
| **Whatsapp Phone Number Id** / **Whatsapp Access Token** | Meta WhatsApp Cloud API credentials | Both required for WhatsApp intake to authenticate — leave WhatsApp off until both are filled in |
| **Whatsapp Notify On Status** (`whatsappNotifyOnStatus`) | Sends order status updates back over WhatsApp | When **on**, customers who ordered via WhatsApp get status pings on the same channel |
| **Ussd Enabled** (`ussdEnabled`) | Lets feature-phone customers order via a USSD dial code | Requires `ussdShortCode` + `ussdApiKey` |
| **Ussd Short Code** / **Ussd Api Key** | The dial code (e.g. `*123#`) and your aggregator's API key | Both required before USSD intake will work |
| **Web Ordering Enabled** (`webOrderingEnabled`) | Lets customers order from a browser client | When **on**, web checkout is accepted; orders are tagged `orderSource: web` |

## How to set it up

1. Sign in to Admin → **Settings → App Settings**.
2. Open the single app record (there is only one — it's a singleton, not a list you add rows to).
3. Update the fields you need, grouped as above. Save often — this form covers a lot of ground.
4. For commission overrides per restaurant, use [Partners](./partners.md) instead of this screen.
5. For other payment providers (Paystack, Flutterwave, …), use [Gateways](./gateways.md). Stripe and COD also appear there and stay in sync with the App Settings toggles above.
6. For the WhatsApp/USSD/Web toggles specifically, follow [order channels](./order-channels.md) for the credential setup and test flow.

## Verify

| Check | Expect |
|---|---|
| Open App Settings | All fields load with current values (no blank/error state) |
| Save a harmless change | Toast/confirmation; value persists on reload |
| Place a test order at/above `freeDeliveryThreshold` | Delivery fee is waived |
| Cancel a test order with wallet refund on | Customer wallet balance increases immediately |
| Toggle a channel on with credentials filled | Test order from that channel succeeds and shows the right `orderSource` |

## Related

- [Order channels](./order-channels.md) · [Gateways](./gateways.md) · [Subscriptions](./subscriptions.md)
- [Market index](./market.md) · [Monetization index](./monetization.md)
