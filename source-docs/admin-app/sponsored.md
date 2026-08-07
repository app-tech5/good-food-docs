# Sponsored listings — Admin app

Paid placement campaigns that restaurants create from their own app ([restaurant sponsored](../restaurant-app/sponsored.md)) to appear higher in search or on the home banner. This admin screen is oversight, not creation — you review, intervene, and pull down anything that shouldn't stay live.

## What you configure

| Field | Meaning | Effect when set |
|---|---|---|
| **Restaurant** | Who's running the campaign | Read-only link back to the restaurant record |
| **Name / Headline / Image** | Campaign creative | What shows in the sponsored slot |
| **Placement** | `search`, `home_banner`, or `both` | Where the listing can appear |
| **Status** | `draft`, `pending_payment`, `active`, `paused`, `ended` | Only `active` campaigns actually show to customers; use **Paused** to pull a creative without deleting the campaign |
| **Bid Amount / Currency** | What the restaurant pays for placement | Higher bids rank higher against other sponsored listings for the same placement/slot |
| **Priority** (0–100) | Server-side tie-break/ranking weight | Higher priority wins ranking ties independent of bid, when your ranking logic considers it |
| **Start At / End At** | Campaign run window | Listing only serves between these dates, even if status is `active` |
| **Impressions / Clicks** | Read-only performance counters | Use to judge whether a campaign is working before a restaurant renews |
| **Daily Budget** | Optional spend cap per day | Caps how much of the bid gets spent per day, if your billing logic enforces it |

## How to set it up

1. Open **Sponsored listings**.
2. Review active/past campaigns: restaurant, placement, status, date window.
3. **View** a row for full detail — creative, bid, impressions/clicks — before intervening.
4. Set **Status** to `paused` (not deleted) if a creative shouldn't stay live but the restaurant might resume it; use `ended` once it's genuinely over.
5. Cross-check what customers actually see: [restaurant sponsored](../restaurant-app/sponsored.md) and the customer discovery feed.

## Verify

| Check | Expect |
|---|---|
| Campaign with status `active`, inside its date window | Shows in the customer feed at its configured placement |
| Pause a campaign | Disappears from customer feed immediately; row and stats remain |
| Campaign past `endAt` | No longer serves even if status still says `active` |
| Compare impressions/clicks over time | Numbers increase as the listing serves and gets tapped |

## Related

- [Monetization index](./monetization.md) · [Restaurant sponsored](../restaurant-app/sponsored.md)
