# OrangePay — how to configure (Admin)

## What this gateway does

- Identifier: `orange-pay`
- Targets Orange Money / Orange Pay style merchant checkout (mobile-money heavy markets)
- Credentials: **merchantId**, **apiKey**, **clientId**, **clientSecret**
- Seed capabilities often: webhooks on; refunds / withdrawals / subscriptions off

## Prerequisites

1. Orange developer / merchant enrollment for the countries you sell in.
2. Backend + admin; `orange-pay` row from seed.
3. Clear ops plan for async mobile-money confirmation (not instant card auth).

## Admin steps

1. **Gateways** → **OrangePay**.
2. Fill all four credential fields from the Orange portal.
3. Enable only capabilities your merchant account actually has.
4. Set fees to your commercial terms (seed may show ~1% / 0 fixed).
5. **Active** only after a successful test payment in a supported country/currency.

## Smoke test

| Step | Expect |
|------|--------|
| Active with empty/demo merchant fields | Checkout/init fails or stays non-production |
| Real merchant credentials + test pay | Payment pending → confirmed via Orange callback/webhook |
| Card-only city with OrangePay Active | Customers may see a method they cannot complete — deactivate per market |

## Differs from others

- Four merchant/OAuth-style fields — not Stripe publishable/secret, not Paystack public/secret pair alone.
- UX is wallet/USSD confirmation; support scripts differ from card chargebacks.

## Related

- [gateways.md](./gateways.md) · [payments-wallet.md](../my-backend/payments-wallet.md)
