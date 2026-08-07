# Partner reports — Admin app

Complaint/incident records filed against drivers or restaurants — not performance dashboards, but a queue of specific issues you triage and resolve. Two separate lists: driver reports and restaurant reports.

## What you configure

### Driver reports

| Field | Meaning | Effect when set |
|---|---|---|
| **Report Type** | `late_delivery`, `rude_behavior`, `unprofessional`, `wrong_order`, `safety_concern`, `driving_issues`, `other` | Categorizes the complaint |
| **Severity** | `low`, `medium`, `high`, `critical` | Use to prioritize your review queue |
| **Status** | `pending`, `under_review`, `resolved`, `dismissed`, `requires_action` | Drives what shows in an open-issues queue vs. history |
| **Admin Notes** | Internal timestamped notes, tied to the admin who wrote them | Not visible to the driver — use for investigation trail |
| **Resolution** | `warning_issued`, `driver_suspended`, `driver_terminated`, `compensation_issued`, `no_action` | Required once you set Status to `resolved` — this is the actual outcome |
| **Resolution Details** | Free text explaining the resolution | Required alongside Resolution |
| **Processing Time** | Read-only: time from creation to resolution | Use to track how fast the team clears reports |

### Restaurant reports

| Field | Meaning | Effect when set |
|---|---|---|
| **Report Type** | `hygiene`, `food_quality`, `service_quality`, `fake_menu`, `price_issue`, `delivery_issue`, `false_advertising`, `other` | Categorizes the complaint |
| **Severity** | `low`, `medium`, `high`, `critical` | Prioritization signal |
| **Status** | `pending`, `under_review`, `resolved`, `rejected` | Drives your queue view |
| **Evidence Photos** | Up to 5 supporting images | Attached by whoever filed the report |
| **Admin Notes** | Internal notes with author + timestamp | Investigation trail, not shown to the restaurant |
| **Resolved By / Resolution Details** | Who closed it and how | Set when moving Status to `resolved` or `rejected` |
| **Days Pending** | Read-only: age of the report while still `pending` | Use to catch reports going stale |

## How to set it up

1. Open **Driver reports** — sort by **Severity**/**Status**; open `critical`/`pending` items first.
2. Read the description, order link (if any), and any attached images/videos.
3. Add an **Admin Note** as you investigate.
4. When done, set **Status** to `resolved` (or `dismissed`), then fill **Resolution** + **Resolution Details**.
5. Repeat for **Restaurant reports** — same triage pattern, using **Evidence Photos** and **Order Reference** for context.
6. Act on the outcome from [Partners](./partners.md) — e.g. suspend a driver (`isApproved` off) or deactivate a restaurant if the resolution calls for it.

## Verify

| Check | Expect |
|---|---|
| Open a `pending` report | Full description, reporter, evidence, and related order (if any) |
| Add an admin note | Appears with your name and timestamp, not visible to the reported party |
| Resolve a report | Status becomes `resolved`; Resolution + Resolution Details required and saved; Processing Time / Days Pending stop accumulating |
| Suspend a driver after a `driver_suspended` resolution | Reflected on that driver's record in [Partners](./partners.md) |

## Related

- [Partners](./partners.md) · [Sales reports](./sales-reports.md)
