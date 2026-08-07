# Payment gateways — Admin app

Enable PSPs and methods checkout / wallet top-ups call. Start with the methods you actually use (usually **Stripe** and **PayPal**), then regional providers.

## Steps

1. Open **Gateways** (`/api/gateways`).
2. Enable only credentialed methods; disable the rest.
3. Open each gateway form: capabilities, logo, provider keys (Stripe publishable/secret/webhook; PayPal client id/secret + sandbox/live).
4. Test checkout + wallet top-up ([customer wallet](../customer-app/wallet.md)).

Stripe secrets: [backend getting started](../my-backend/getting-started.md).

Online screenshots: list + Stripe + PayPal forms on the public docs page.
