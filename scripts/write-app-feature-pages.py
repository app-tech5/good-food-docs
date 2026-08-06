#!/usr/bin/env python3
"""Write feature pages under each app — real documentation, not caption+screenshot cards."""
from __future__ import annotations

import html
import subprocess
from pathlib import Path

ROOT = Path("/Users/nass/Documents/good-food-docs")
A = "assets/images"
SS = Path("/Users/nass/Documents/good-foods-description/img/pro/screenshots")


def esc(s: str) -> str:
    """Escape unless the string already contains intentional HTML tags we author."""
    if "<a " in s or "<code>" in s or "<strong>" in s or "<em>" in s:
        return s
    return html.escape(s)


def render_shots(shots, img_prefix: str) -> str:
    if not shots:
        return ""
    phones = [s for s in shots if s[0] == "phone"]
    wides = [s for s in shots if s[0] == "wide"]
    parts: list[str] = []
    if phones:
        parts.append('            <div class="shot-grid phones">')
        for _, src, alt, cap in phones:
            parts.append(
                f"""              <div class="shot phone">
                <img src="{img_prefix}{src}" alt="{html.escape(alt)}" />
                <p>{html.escape(cap)}</p>
              </div>"""
            )
        parts.append("            </div>")
    if wides:
        style = ' style="margin-top: 16px;"' if phones else ""
        parts.append(f'            <div class="shot-grid"{style}>')
        for _, src, alt, cap in wides:
            parts.append(
                f"""              <div class="shot wide">
                <img src="{img_prefix}{src}" alt="{html.escape(alt)}" />
                <p>{html.escape(cap)}</p>
              </div>"""
            )
        parts.append("            </div>")
    return "\n".join(parts)


def render_section(sec: dict, img_prefix: str) -> str:
    """
    sec keys:
      h2: str
      paras: list[str]  (optional lead paragraphs)
      blocks: list[{h3, paras?, steps?}]
      shots: list after explanation
      after: list[str] optional closing paras
    """
    lines = [f'          <section class="section-block">', f"            <h2>{esc(sec['h2'])}</h2>"]
    for i, p in enumerate(sec.get("paras") or []):
        cls = "" if i == 0 else ' class="section-subtext"'
        lines.append(f"            <p{cls}>\n              {esc(p)}\n            </p>")
    for block in sec.get("blocks") or []:
        if block.get("h3"):
            lines.append(f"            <h3>{esc(block['h3'])}</h3>")
        for p in block.get("paras") or []:
            lines.append(f'            <p class="section-subtext">\n              {esc(p)}\n            </p>')
        steps = block.get("steps") or []
        if steps:
            lines.append("            <ol class=\"doc-steps\">")
            for step in steps:
                lines.append(f"              <li>{esc(step)}</li>")
            lines.append("            </ol>")
    if sec.get("shots"):
        lines.append(render_shots(sec["shots"], img_prefix))
    for p in sec.get("after") or []:
        lines.append(f'            <p class="section-subtext">\n              {esc(p)}\n            </p>')
    lines.append("          </section>")
    return "\n".join(lines)


def page(title, h1, subtitle, pills, sections, css_href, js_href, img_prefix):
    pills_html = "\n".join(f'            <span class="meta-pill">{html.escape(p)}</span>' for p in pills)
    body = "\n".join(render_section(s, img_prefix) for s in sections)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(title)}</title>
    <link rel="stylesheet" href="{css_href}" />
  </head>
  <body>
    <script src="{js_href}"></script>
    <main class="layout">
      <aside class="sidebar" data-docs-sidebar></aside>
      <section class="content">
        <header id="top" class="hero">
          <h1>{html.escape(h1)}</h1>
          <p class="subtitle">
            {esc(subtitle)}
          </p>
          <div class="meta-strip">
{pills_html}
          </div>
        </header>

        <section class="overview">
{body}
        </section>
      </section>
    </main>
  </body>
</html>
"""


def ensure_admin_sponsored():
    dest = ROOT / "assets/images/features/admin-sponsored.jpg"
    src = SS / "admin/46-sponsored-listings.jpg"
    if dest.exists() and dest.stat().st_size > 2000:
        return
    if src.exists():
        subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "78", str(src), "--out", str(dest)],
            check=False,
            capture_output=True,
        )
        subprocess.run(["sips", "-Z", "1400", str(dest)], check=False, capture_output=True)


def main():
    ensure_admin_sponsored()

    ROOT.joinpath("wallet.html").write_text(
        page(
            "Wallet & payments — Customer app",
            "Wallet & payments",
            "How the in-app balance works for customers, how they top up, and what you configure so checkout and refunds stay coherent.",
            ["Balance", "Top up", "Payment methods"],
            [
                {
                    "h2": "What the wallet is for",
                    "paras": [
                        "The wallet is a prepaid balance inside the customer app. Instead of entering a card on every order, the customer can pay from money already on the account. That shortens checkout, reduces failed payments at the door of the kitchen, and gives you a place to land refunds or promotions as credit.",
                        "On the Wallet screen the customer sees the current balance, actions to add or send money (depending on what you enable), and the list of saved payment methods (card brands, Google Pay, PayPal, cash, and similar).",
                    ],
                    "blocks": [
                        {
                            "h3": "How a customer uses it",
                            "steps": [
                                "Open the drawer or account area and choose <strong>Wallet</strong>.",
                                "Check the balance. Use the refresh control if the amount looks stale after a payment.",
                                "Tap <strong>Add Money</strong>, choose an amount (or a quick chip such as $10 / $20 / $50), select a payment method, then confirm <strong>Add to balance</strong>.",
                                "At checkout, choose the wallet as the payment method when the balance covers the order (or the part your rules allow).",
                            ],
                        },
                        {
                            "h3": "What you configure as operator",
                            "paras": [
                                'Payment gateways and marketplace payment behaviour are managed in the admin app — see <a href="./admin-app/monetization.html">Monetization</a>. Enable the gateways you actually use in each market before expecting top-ups to succeed in production.',
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/wallet.jpg", "Customer wallet", "Balance and saved payment methods"),
                        ("phone", f"{A}/features/wallet-topup.jpg", "Add money", "Choose amount and pay into the wallet"),
                    ],
                },
            ],
            "./site.css",
            "./js/sidebar-scroll.js",
            "./",
        ),
        encoding="utf-8",
    )

    ROOT.joinpath("subscriptions.html").write_text(
        page(
            "Subscriptions — Customer app",
            "Subscriptions",
            "How membership plans appear to customers, what benefits they unlock, and how those plans are created in admin.",
            ["Plans", "Benefits", "Subscribe"],
            [
                {
                    "h2": "Membership in the customer app",
                    "paras": [
                        "Customer subscriptions are recurring plans (for example monthly) that unlock benefits such as free delivery, a food discount, member-only deals, or priority support. The customer app shows only plans whose target is <strong>customer</strong>.",
                        "Each plan card lists the name, price and billing cycle, the benefit bullets, and a Subscribe action. After a successful purchase path (via your configured gateways), the membership stays attached to that account until it expires or is cancelled under your rules.",
                    ],
                    "blocks": [
                        {
                            "h3": "How a customer subscribes",
                            "steps": [
                                "Sign in with a customer account.",
                                "Open the Subscriptions / membership screen from account or settings (label depends on your translations).",
                                "Compare the listed plans and tap <strong>Subscribe</strong> on the one you want.",
                                "Complete payment with an enabled gateway. Confirm the plan shows as active afterward.",
                            ],
                        },
                        {
                            "h3": "Where plans are defined",
                            "paras": [
                                'You create and edit tiers in the admin app under Subscriptions (name, price, billing cycle, benefits, active flag, target = customer). Details and earnings impact are covered in <a href="./admin-app/monetization.html">admin monetization</a>.',
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/sub-customer.jpg", "Customer plans", "Plan cards with benefits and Subscribe"),
                    ],
                },
            ],
            "./site.css",
            "./js/sidebar-scroll.js",
            "./",
        ),
        encoding="utf-8",
    )

    ROOT.joinpath("intelligence.html").write_text(
        page(
            "AI intelligence — Customer app",
            "AI intelligence",
            "Three customer-facing helpers: personalized recommendations, smarter arrival times, and delivery fees that can rise when demand spikes.",
            ["Recommendations", "Smart ETA", "Surge"],
            [
                {
                    "h2": "Recommendations that grow the basket",
                    "paras": [
                        "On restaurant and discovery surfaces, a <strong>Recommended for you</strong> block can suggest dishes that fit the customer’s history, time of day, and context such as weather. Each card shows a short reason line so the suggestion feels explained rather than random.",
                        "The goal is a natural add-to-cart moment (sides, drinks, extras) that raises average order value without forcing a separate upsell screen.",
                    ],
                    "blocks": [
                        {
                            "h3": "What the customer sees",
                            "paras": [
                                "A horizontal row of recommended items with title, price, and a short match reason. Tapping a card follows your normal product / add-to-cart path.",
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/ai-reco.jpg", "Recommendations", "Recommended for you on the restaurant screen"),
                    ],
                },
                {
                    "h2": "Arrival times customers can trust",
                    "paras": [
                        "Smart ETA estimates how long food will take, using kitchen load and travel time where your backend intelligence stack is enabled. On restaurant cards and detail screens the estimate appears as a clear badge (for example “ETA 26–36 min”) next to fee information.",
                        "Clearer arrivals reduce “where is my food?” support load and set expectations before the customer commits to checkout.",
                    ],
                    "shots": [
                        ("phone", f"{A}/features/ai-eta.jpg", "ETA badge", "ETA shown on the restaurant detail"),
                    ],
                },
                {
                    "h2": "Surge when the city is busy",
                    "paras": [
                        "When demand is high and courier capacity is tight, delivery pricing can show a surge multiplier (for example “Surge 1.45x”) beside the ETA. Quiet periods keep standard fees; peaks stay explicit so the customer understands the change before paying.",
                        "Surge is a marketplace lever: it protects delivery reliability when everyone orders at once, instead of silently missing SLAs.",
                    ],
                    "shots": [
                        ("phone", f"{A}/features/ai-surge.jpg", "Surge badge", "Surge multiplier on restaurant detail"),
                    ],
                },
            ],
            "./site.css",
            "./js/sidebar-scroll.js",
            "./",
        ),
        encoding="utf-8",
    )

    ROOT.joinpath("order-tracking.html").write_text(
        page(
            "Order tracking — Customer app",
            "Order tracking",
            "How customers follow an order from acceptance to delivery, and how that ties to the map and the driver app.",
            ["Status steps", "ETA", "Map"],
            [
                {
                    "h2": "Follow the order without calling support",
                    "paras": [
                        "After checkout, the customer opens Track Order (from order history or the post-order flow). The screen shows the order id, timestamp, and a vertical status timeline: pending → preparing → out for delivery → delivered. Active steps are highlighted; later steps stay muted until they happen.",
                        "Restaurant contact details appear on the same screen so the customer can call if something is wrong with the meal itself — while delivery progress stays visible without opening a separate chat.",
                    ],
                    "blocks": [
                        {
                            "h3": "Typical customer path",
                            "steps": [
                                "Place an order and wait for the restaurant to accept it.",
                                "Open <strong>Order history</strong>, select the order, then <strong>Track order</strong> (or the equivalent deep link after payment).",
                                "Watch the timeline advance as kitchen and driver statuses change on the shared order record.",
                                "When the driver is en route, ETA copy updates when your logistics / intelligence data provides it.",
                            ],
                        },
                        {
                            "h3": "Map before and during the order",
                            "paras": [
                                'The nearby map helps customers discover restaurants around them. Live courier movement on the customer map depends on your deployment; driver-side job handling and proof of delivery are documented under <a href="./delivery-app/logistics.html">Logistics &amp; POD</a>.',
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/tracking.jpg", "Track order", "Status timeline for a live order"),
                        ("phone", f"{A}/features/map-nearby.jpg", "Map nearby", "Map of nearby restaurants"),
                    ],
                },
            ],
            "./site.css",
            "./js/sidebar-scroll.js",
            "./",
        ),
        encoding="utf-8",
    )

    (ROOT / "delivery-app/logistics.html").write_text(
        page(
            "Logistics & POD — Driver app",
            "Logistics & proof of delivery",
            "How drivers work a shift: today’s jobs, an active delivery, customer details, and proof at the door.",
            ["Deliveries", "Active job", "Proof of delivery"],
            [
                {
                    "h2": "Today’s deliveries and assignment radius",
                    "paras": [
                        "The driver app centres on a clear list of jobs for the shift — pending, on the way, and completed. Batching nearby drops reduces empty miles at lunch peak: one courier can stack orders in the same neighbourhood instead of zigzagging across the city.",
                        "How far a restaurant (or the marketplace) is willing to send couriers is controlled with delivery settings such as radius and preparation time. Those settings live with the restaurant / marketplace configuration; drivers experience the result as which jobs appear and how far they run.",
                    ],
                    "blocks": [
                        {
                            "h3": "Driver checklist for the list",
                            "steps": [
                                "Go online / available so new assignments can reach you.",
                                "Open <strong>Deliveries</strong> (or Home’s active list) and scan statuses.",
                                "Accept or start the next job according to your marketplace rules.",
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/driver-deliveries.jpg", "Deliveries", "Today’s delivery list"),
                        ("phone", f"{A}/features/delivery-settings.jpg", "Delivery settings", "Radius and prep time (restaurant side)"),
                    ],
                },
                {
                    "h2": "On the road",
                    "paras": [
                        "An active delivery screen keeps the current order, status, and primary actions in one place. From details, the driver sees customer information needed for the drop-off and can open navigation toward the address.",
                        'Customers follow the same order on <a href="../order-tracking.html">order tracking</a> — there is one order record, not a separate “driver copy”.',
                    ],
                    "shots": [
                        ("phone", f"{A}/features/driver-active.jpg", "Active delivery", "Current job while on delivery"),
                        ("phone", f"{A}/features/driver-details.jpg", "Delivery details", "Customer and order details"),
                    ],
                },
                {
                    "h2": "Proof of delivery at the door",
                    "paras": [
                        "When the driver marks the order delivered, a proof-of-delivery flow can require a photo and a signature — especially useful for contactless drop-off and cash-on-delivery disputes. The modal explains contactless rules (for example staying within a short distance of the address) and offers Clear on the signature pad before Complete delivery.",
                    ],
                    "blocks": [
                        {
                            "h3": "Complete with evidence",
                            "steps": [
                                "Arrive at the drop-off and open <strong>Mark as Delivered</strong> (or the equivalent action).",
                                "If contactless is on, capture the required photo.",
                                "Collect a signature on the pad (or clear and retry).",
                                "Confirm <strong>Complete delivery</strong>. The order status becomes delivered for customer, restaurant, and admin.",
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/driver-pod.jpg", "Proof of delivery", "Photo + signature before complete"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "delivery-app/subscriptions.html").write_text(
        page(
            "Subscriptions — Driver app",
            "Subscriptions",
            "How courier membership plans appear in the driver app and how you define those tiers in admin.",
            ["Driver plans", "Benefits", "Subscribe"],
            [
                {
                    "h2": "Plans for couriers",
                    "paras": [
                        "Driver subscriptions are tiers targeted at <strong>driver</strong> accounts. Typical benefits include access perks, support priority, or other marketplace rules you attach to the plan. The driver app lists those plans with price, cycle, and a Subscribe action — the same pattern customers and restaurants see for their own targets.",
                    ],
                    "blocks": [
                        {
                            "h3": "Driver steps",
                            "steps": [
                                "Sign in with a driver account.",
                                "Open Subscriptions from the driver menu / settings.",
                                "Choose a plan and complete Subscribe through an enabled payment path.",
                                "Confirm the plan shows as active and that any access benefits apply on the next shift.",
                            ],
                        },
                        {
                            "h3": "Operator setup",
                            "paras": [
                                'Create and edit driver tiers in admin → Subscriptions (target = driver). See <a href="../admin-app/monetization.html">Monetization</a> for the full money picture.',
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/sub-driver.jpg", "Driver plans", "Driver subscription plans"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "restaurant-app/kitchen-display.html").write_text(
        page(
            "Kitchen Display — Restaurant app",
            "Kitchen Display (KDS)",
            "How the paperless kitchen board works: where tickets come from, how staff advance them, and how to run it on a tablet at the pass.",
            ["Tickets", "Columns", "Orders"],
            [
                {
                    "h2": "What the Kitchen Display does",
                    "paras": [
                        "The Kitchen Display is a board inside the restaurant app for cooks and the pass. After an order is accepted, it appears as a ticket with items, timing cues, and actions to move it through prep. The idea is simple: stop hunting paper slips; keep one shared order story with the customer, the driver, and admin.",
                        "Columns such as <strong>New</strong>, <strong>Preparing</strong>, and <strong>Ready</strong> group tickets. Staff accept new work, start preparation, then mark food ready for pickup or courier handoff. Age on the ticket helps the line see what is burning.",
                    ],
                    "blocks": [
                        {
                            "h3": "Happy path on a busy service",
                            "steps": [
                                "A customer places a delivery or pickup order.",
                                "Restaurant staff accept it on the normal <strong>Orders</strong> list (or via your auto-accept rules).",
                                "Open <strong>Kitchen Display</strong> from the drawer / navigation — preferably on a tablet in landscape.",
                                "Advance each ticket: accept → prepare → ready.",
                                "When food is ready, the driver (or the customer for pickup) completes the handoff; admin still sees the same order for support and earnings.",
                            ],
                        },
                        {
                            "h3": "Tablet tips",
                            "paras": [
                                "Mount the device at eye level on the pass, keep brightness high, and disable auto-lock during service. Prefer a stable Wi‑Fi path to your API — a flaky network looks like “KDS is broken”.",
                                "Demo databases can include kitchen-oriented sample tickets so you can train staff or screenshot the board before the first real rush.",
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/kds.jpg", "Kitchen Display", "Tickets across New / Preparing / Ready"),
                    ],
                },
                {
                    "h2": "Tied to the live orders list",
                    "paras": [
                        "Orders still land in the restaurant orders UI first. The Kitchen Display is the kitchen-oriented view of that same pipeline — not a second database. If a ticket is missing, refresh the board and confirm the order exists and was accepted for this restaurant account.",
                    ],
                    "shots": [
                        ("phone", f"{A}/features/resto-orders.jpg", "Orders", "Live restaurant orders"),
                        ("phone", f"{A}/features/resto-drawer.jpg", "Drawer", "Open Kitchen Display from the menu"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "restaurant-app/subscriptions.html").write_text(
        page(
            "Subscriptions — Restaurant app",
            "Subscriptions",
            "How restaurant partners subscribe to plans that change commission, visibility, or SaaS-style access.",
            ["Restaurant plans", "Benefits", "Subscribe"],
            [
                {
                    "h2": "Plans partners buy from their app",
                    "paras": [
                        "Restaurant subscriptions are tiers with target <strong>restaurant</strong>. Benefits often include a lower platform commission, eligibility for sponsored placement, better support, or tool access you attach to the plan. Partners see those plans inside the restaurant app and subscribe without leaving their day-to-day workspace.",
                    ],
                    "blocks": [
                        {
                            "h3": "Restaurant steps",
                            "steps": [
                                "Sign in as the restaurant user.",
                                "Open <strong>Subscriptions</strong> from the drawer or settings.",
                                "Review price, cycle, and benefits; tap Subscribe on the chosen plan.",
                                "After activation, confirm commission / feature changes on the next orders (and in admin earnings if you are verifying).",
                            ],
                        },
                        {
                            "h3": "Where you edit tiers",
                            "paras": [
                                'Admin → Subscriptions, target = restaurant. Full monetization context: <a href="../admin-app/monetization.html">Monetization</a>.',
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/sub-restaurant.jpg", "Restaurant plans", "Restaurant subscription screen"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "restaurant-app/sponsored.html").write_text(
        page(
            "Sponsored listings — Restaurant app",
            "Sponsored listings",
            "How a restaurant launches a paid placement campaign (search, home banner, or both) from its own app.",
            ["Campaign", "Bid", "Placement"],
            [
                {
                    "h2": "Buy attention in the customer feed",
                    "paras": [
                        "Sponsored listings let a restaurant pay for better visibility: top of search, a home banner slot, or both. The restaurant fills a short campaign form — headline, daily bid, placement — then launches. Active campaigns can appear in the customer experience without looking like a bolted-on ad unit.",
                        "Admin keeps oversight of what is live so paid placement stays controlled marketplace-wide.",
                    ],
                    "blocks": [
                        {
                            "h3": "Launch a campaign",
                            "steps": [
                                "Sign in to the restaurant app (live API mode recommended for real campaigns).",
                                "Open <strong>Sponsored listings</strong>.",
                                "Under New campaign, set a headline customers will recognize.",
                                "Enter a daily bid amount and choose placement (search top, home banner, or search + banner).",
                                "Tap <strong>Launch campaign</strong>, then confirm the campaign appears under My campaigns.",
                                'Optionally verify in the customer app that the placement shows, and in <a href="../admin-app/sponsored.html">admin sponsored listings</a> that the campaign is visible to operators.',
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/sponsored.jpg", "Sponsored form", "Headline, bid, and placement"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "admin-app/monetization.html").write_text(
        page(
            "Monetization — Admin app",
            "Monetization",
            "How operators set the platform cut, subscription tiers, earnings views, and payment gateways that power wallets and checkout.",
            ["Earnings", "Subscriptions", "Gateways"],
            [
                {
                    "h2": "Commissions and earnings",
                    "paras": [
                        "Every completed order splits value between the marketplace and the restaurant (and related parties under your rules). The baseline platform commission is configured in marketplace / app settings; restaurant subscription benefits can soften that cut when an active plan says so.",
                        "The Earnings area in admin is where you review periods and totals — what the platform kept versus what restaurants earned — before you run payouts or investigations.",
                    ],
                    "blocks": [
                        {
                            "h3": "Operator checklist",
                            "steps": [
                                "Set or review the default commission rate in App Settings.",
                                "Place a test order end-to-end (customer → restaurant accept → complete).",
                                "Open <strong>Earnings</strong> and confirm the platform vs restaurant split matches your rate and any active restaurant plan benefits.",
                                "Use View on a row when you need the detail behind a period.",
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", f"{A}/features/earnings.jpg", "Earnings", "Earnings list — periods and totals"),
                    ],
                },
                {
                    "h2": "Subscription tiers for every role",
                    "paras": [
                        "Subscriptions in admin are the source of truth for plans sold in the three mobile apps. Each plan has a <strong>target</strong>: customer, driver, or restaurant — plus price, billing cycle, active flag, and benefit text / flags.",
                        "Seeded demos usually include sample tiers so lists are not empty after migrations. Edit those to match your pricing story before go-live.",
                    ],
                    "blocks": [
                        {
                            "h3": "Create or edit a plan",
                            "steps": [
                                "Open <strong>Subscriptions</strong> in the admin sidebar.",
                                "Review existing rows (name, target, price, cycle, active).",
                                "Add New or View to edit: set target audience, price, billing cycle, and benefits.",
                                "Save, then open the matching mobile app and confirm the plan appears on that role’s subscription screen.",
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", f"{A}/features/admin-subscriptions.jpg", "Subscriptions", "Admin subscription tiers"),
                    ],
                    "after": [
                        'Customer, driver, and restaurant subscribe UIs: <a href="../subscriptions.html">customer</a>, <a href="../delivery-app/subscriptions.html">driver</a>, <a href="../restaurant-app/subscriptions.html">restaurant</a>.',
                    ],
                },
                {
                    "h2": "Payment gateways",
                    "paras": [
                        "Gateways tell the platform which PSPs and local methods are available (cards, wallets, cash on delivery, regional providers, and the internal wallet). Each row typically shows fees, name, and whether it is active.",
                        "Turn on only what you have credentials and compliance for. Checkout and wallet top-ups will fail in production if the customer’s method points at a disabled or misconfigured gateway.",
                    ],
                    "blocks": [
                        {
                            "h3": "Configure for a market",
                            "steps": [
                                "Open <strong>Gateways</strong> in admin.",
                                "Enable the methods you support; disable the rest.",
                                "Enter provider credentials / fees as your form requires (View on a row).",
                                'Verify a test checkout and a wallet top-up from the <a href="../wallet.html">customer wallet</a> docs path.',
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", f"{A}/features/gateways.jpg", "Gateways", "Active payment gateways and fees"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "admin-app/market.html").write_text(
        page(
            "Market & languages — Admin app",
            "Market & languages",
            "How to make the marketplace feel local: languages (including RTL), currencies, and app-level marketplace settings.",
            ["Languages", "Currencies", "App settings"],
            [
                {
                    "h2": "Languages",
                    "paras": [
                        "Admin maintains the language catalogue (code, name, default flag). Mobile apps and the admin UI follow the active / default language. Arabic and similar locales can reverse layout (RTL) when the selected language requires it.",
                        "Customers change language from their settings screen; the admin list is where you decide which languages exist and which one is the marketplace default for new users.",
                    ],
                    "blocks": [
                        {
                            "h3": "Operator steps",
                            "steps": [
                                "Open <strong>Settings → Languages</strong> (or Languages in the sidebar, depending on your build).",
                                "Ensure the languages you sell in are present; mark one as default.",
                                "In a customer (or driver / restaurant) app, open Settings and switch language to verify strings and layout.",
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", f"{A}/features/languages.jpg", "Languages", "Admin language list"),
                        ("phone", f"{A}/features/lang-picker.jpg", "Customer settings", "Language shown in customer settings"),
                    ],
                },
                {
                    "h2": "Currencies",
                    "paras": [
                        "Menus, carts, wallets, subscriptions, and reports should speak one money language per market. The Currencies list is where you define codes and defaults; changing the active currency without a plan will confuse prices already shown to users, so treat it as a go-live decision.",
                    ],
                    "shots": [
                        ("wide", f"{A}/features/currencies.jpg", "Currencies", "Admin currencies"),
                    ],
                },
                {
                    "h2": "Taxes",
                    "paras": [
                        "Local tax rules (VAT, GST, sales tax, and similar) belong in the Taxes catalogue so carts and reports collect the right amounts for your jurisdiction. Configure rates before go-live and verify on a test checkout that tax lines match finance expectations.",
                    ],
                    "shots": [
                        ("wide", f"{A}/features/admin-taxes.jpg", "Taxes", "Admin tax settings"),
                    ],
                },
                {
                    "h2": "Marketplace app settings",
                    "paras": [
                        "App Settings hold cross-cutting marketplace behaviour: default language, timezone, cash-on-delivery, delivery fee defaults, maximum delivery distance, and related flags. Commission baselines and channel hooks (WhatsApp / USSD / web ordering when enabled) often live here too — review this screen when you enter a new city.",
                    ],
                    "blocks": [
                        {
                            "h3": "Before launch in a city",
                            "steps": [
                                "Open <strong>Settings → App Settings</strong> and View the active app record.",
                                "Set timezone, default language, delivery fee / distance, and COD according to local rules.",
                                "Align currency, taxes, and gateways with that same market.",
                                "Enable only the order channels you will actually operate.",
                                "Run one full order in that configuration before inviting real restaurants.",
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", f"{A}/features/app-settings.jpg", "App settings", "Marketplace app settings"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    # --- Pages covering CodeCanyon / Pro feature gaps ---

    ROOT.joinpath("ordering.html").write_text(
        page(
            "Ordering & discovery — Customer app",
            "Ordering & discovery",
            "How customers find restaurants, build a cart, apply offers, and place an order — the core marketplace journey.",
            ["Home", "Search", "Cart", "Checkout", "Offers"],
            [
                {
                    "h2": "Find food in a multi-restaurant marketplace",
                    "paras": [
                        "The customer app is a multi-store marketplace: one install, many restaurants. Home mixes delivery / pickup, search, categories, banners, and featured places. Nearby map views help when the customer wants “what’s close”, and restaurant pages carry hours, fees, ratings, offers, and the menu.",
                    ],
                    "blocks": [
                        {
                            "h3": "Discovery path",
                            "steps": [
                                "Open the app and choose <strong>Delivery</strong> or <strong>Pickup</strong> when both are available.",
                                "Browse the homepage (categories, offers, restaurants) or open <strong>Search</strong> for a keyword.",
                                "Optionally use the map / nearby view to pick a place geographically.",
                                "Open a restaurant: check status, ETA / fee cues, offers, then browse the menu and add items (with variants when priced).",
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/ordering-home.jpg", "Home", "Homepage — delivery/pickup, categories, offers"),
                        ("phone", f"{A}/features/ordering-search.jpg", "Search", "Search restaurants and dishes"),
                        ("phone", f"{A}/features/ordering-menu.jpg", "Menu", "Restaurant menu and add to cart"),
                    ],
                },
                {
                    "h2": "Cart, offers, and checkout",
                    "paras": [
                        "The cart stays synced with the backend. Customers can manage items, apply a promo / coupon when you run campaigns, choose delivery or pickup, pick an address, and pay with an enabled method (card, cash on delivery, wallet, and other gateways you activate).",
                        "Offers and coupons are how you grow volume: percentage or fixed discounts, free delivery, and similar campaign types configured in admin. The customer sees them on home / restaurant surfaces and can enter a code at checkout when the campaign allows.",
                    ],
                    "blocks": [
                        {
                            "h3": "Place an order",
                            "steps": [
                                "Review the cart (quantities, extras, totals).",
                                "Apply a coupon or claim a listed offer when available.",
                                "Confirm fulfillment (delivery vs pickup), address, and payment method.",
                                "Place the order, then follow it in order history / <a href=\"./order-tracking.html\">tracking</a>.",
                            ],
                        },
                        {
                            "h3": "Where offers are configured",
                            "paras": [
                                'Coupons and promotions are managed in the admin app — see <a href="./admin-app/promotions.html">Promotions &amp; coupons</a>. Payment methods and wallet top-ups: <a href="./wallet.html">Wallet &amp; payments</a> and <a href="./admin-app/monetization.html">Monetization</a>.',
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/ordering-cart.jpg", "Cart", "Cart before checkout"),
                        ("phone", f"{A}/features/ordering-checkout.jpg", "Checkout", "Summary, payment, place order"),
                        ("phone", f"{A}/features/ordering-offers.jpg", "Offers", "Offers / vouchers surface"),
                    ],
                },
                {
                    "h2": "Order history",
                    "paras": [
                        "After checkout, orders appear in the order list with status and detail. From there customers reopen tracking, contact the restaurant when needed, and later leave reviews when your flow enables them.",
                    ],
                    "shots": [
                        ("phone", f"{A}/features/ordering-history.jpg", "Orders", "Order history list"),
                    ],
                },
            ],
            "./site.css",
            "./js/sidebar-scroll.js",
            "./",
        ),
        encoding="utf-8",
    )

    (ROOT / "delivery-app/earnings.html").write_text(
        page(
            "Earnings & payouts — Driver app",
            "Earnings & payouts",
            "How drivers see today’s money, delivery history, transactions, and where payouts are sent.",
            ["Earnings", "Transactions", "Payouts"],
            [
                {
                    "h2": "Know what a shift paid",
                    "paras": [
                        "Couriers need a clear money picture: what they earned today, what sits in history, and how cash reaches their bank. The driver app exposes earnings summaries, transaction history, and payout method setup (including Connect-style onboarding when you enable it).",
                        "Job handling, batching, and proof of delivery stay on the logistics screens; this page is the money side of the same role.",
                    ],
                    "blocks": [
                        {
                            "h3": "Driver checklist",
                            "steps": [
                                "Complete deliveries for the shift (see <a href=\"./logistics.html\">Logistics &amp; POD</a>).",
                                "Open <strong>Earnings</strong> to review today’s totals and periods your build shows.",
                                "Open transactions when you need a line-by-line trail.",
                                "Add or update <strong>Payout methods</strong> so admin / Connect can settle the driver.",
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/driver-earnings.jpg", "Earnings", "Driver earnings overview"),
                        ("phone", f"{A}/features/driver-transactions.jpg", "Transactions", "Driver transaction history"),
                        ("phone", f"{A}/features/driver-payouts.jpg", "Payouts", "Payout methods"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "restaurant-app/operations.html").write_text(
        page(
            "Orders & menu — Restaurant app",
            "Orders & menu",
            "Day-to-day partner ops: accept or reject orders, manage the menu, set hours, and read analytics — before or beside the Kitchen Display.",
            ["Orders", "Menu", "Hours", "Analytics"],
            [
                {
                    "h2": "Live orders: accept and reject",
                    "paras": [
                        "Incoming orders land in the restaurant orders list in real time. Operators accept or reject, then move the meal through prepare / ready so the driver (or pickup customer) can collect it. New-order alerts can deep-link back to the order so nobody misses a ticket during rush.",
                        'For a paperless board on the pass, use the <a href="./kitchen-display.html">Kitchen Display (KDS)</a> — it shares the same order pipeline.',
                    ],
                    "blocks": [
                        {
                            "h3": "Service loop",
                            "steps": [
                                "Keep the restaurant <strong>open</strong> when you can fulfill orders.",
                                "Watch the orders list; accept what you can cook, reject with a clear reason when you cannot.",
                                "Advance status as food progresses; mark ready for courier or pickup.",
                                "Use order history when you need past tickets or disputes.",
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/resto-ops-orders.jpg", "Orders", "Live restaurant orders"),
                    ],
                },
                {
                    "h2": "Menu, hours, and analytics",
                    "paras": [
                        "Partners manage categories, dishes, prices, photos, variants, and availability from the restaurant app — without waiting on admin for every price tweak. Opening hours and delivery / pickup controls (radius, prep time) define when and how far you sell.",
                        "Dashboard KPIs and analytics (periods, bestsellers, peaks) help owners see what is working. Reviews appear for reputation; reply flows depend on your build.",
                    ],
                    "blocks": [
                        {
                            "h3": "Keep the catalog honest",
                            "steps": [
                                "Open <strong>Menu</strong>: add or edit categories and items, set prices and photos, toggle availability when an item is 86’d.",
                                "Edit <strong>Opening hours</strong> and delivery settings so the customer app shows accurate open/closed and radius.",
                                "Check analytics after a few service days to spot bestsellers and quiet slots.",
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/resto-ops-menu.jpg", "Menu", "Restaurant menu management"),
                        ("phone", f"{A}/features/resto-ops-menu-edit.jpg", "Edit item", "Add / edit a menu item"),
                        ("phone", f"{A}/features/resto-ops-hours.jpg", "Hours", "Opening hours"),
                        ("phone", f"{A}/features/resto-ops-analytics.jpg", "Analytics", "Restaurant analytics"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "admin-app/operations.html").write_text(
        page(
            "Operations — Admin app",
            "Operations",
            "The day-to-day control room: orders, restaurants, customers, drivers, and the food catalog that powers every mobile app.",
            ["Orders", "Partners", "Catalog", "Users"],
            [
                {
                    "h2": "Orders and partners",
                    "paras": [
                        "Admin is the marketplace command center. The orders list shows payment state, customer, restaurant, driver, totals, and fulfillment status — with View into full detail (line items, delivery, timeline). From here support can investigate without asking three apps for screenshots.",
                        "Restaurant and driver management cover onboarding and ongoing control: activate or close restaurants, approve drivers before they go online, and keep profiles consistent with what mobile apps display.",
                    ],
                    "blocks": [
                        {
                            "h3": "Operator habits",
                            "steps": [
                                "Start on the dashboard KPIs when you open admin.",
                                "Use <strong>Orders</strong> for live incidents (failed payment, stuck status, missing driver).",
                                "Use <strong>Restaurants</strong> / <strong>Drivers</strong> / <strong>Users</strong> to approve, edit, or suspend accounts.",
                                "Open a row’s View when you need the full record.",
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", f"{A}/features/admin-ops-orders.jpg", "Orders", "Admin orders list"),
                        ("wide", f"{A}/features/admin-ops-restaurants.jpg", "Restaurants", "Restaurant management"),
                        ("wide", f"{A}/features/admin-ops-drivers.jpg", "Drivers", "Driver management"),
                        ("wide", f"{A}/features/admin-ops-users.jpg", "Users", "Customer users"),
                    ],
                },
                {
                    "h2": "Menus and catalog",
                    "paras": [
                        "Categories, menus, products, and variants can be curated centrally when partners need help — or when you seed a new city. What you publish here is what customers browse and what restaurants edit on mobile when you allow dual management.",
                    ],
                    "shots": [
                        ("wide", f"{A}/features/admin-ops-menus.jpg", "Menus", "Admin menus / catalog"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "admin-app/promotions.html").write_text(
        page(
            "Promotions & coupons — Admin app",
            "Promotions & coupons",
            "How operators run growth campaigns: promotion types, scoping, and coupon codes customers redeem at checkout.",
            ["Promotions", "Coupons", "Campaigns"],
            [
                {
                    "h2": "Grow volume with real campaigns",
                    "paras": [
                        "The promotion engine supports the campaign styles buyers expect from a modern marketplace: percentage or fixed discounts, free delivery, Buy X Get Y / combos, flash sales, happy hours, and similar types your build exposes. Scope a campaign to the whole platform or to a restaurant, category, or item — and target audiences such as all, new, existing, or VIP customers when those flags exist.",
                        "Coupon codes add constrained redemptions: minimum order, max uses, per-user limits, first-order-only, and expiry. Customers enter codes in the cart / checkout path documented under <a href=\"../ordering.html\">Ordering &amp; discovery</a>.",
                    ],
                    "blocks": [
                        {
                            "h3": "Launch a campaign safely",
                            "steps": [
                                "Open <strong>Promotions</strong> and create or edit a campaign (type, discount, schedule, scope).",
                                "Open <strong>Coupons</strong> when you need a redeemable code with usage limits.",
                                "Activate only what you can afford on margin; test with a demo customer order.",
                                "Confirm the offer appears on customer home / restaurant surfaces and that checkout applies the code.",
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", f"{A}/features/admin-promotions.jpg", "Promotions", "Admin promotions list"),
                        ("wide", f"{A}/features/admin-coupons.jpg", "Coupons", "Admin coupon codes"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "admin-app/reports.html").write_text(
        page(
            "Reports & analytics — Admin app",
            "Reports & analytics",
            "Sales, restaurant, and driver reports so you can prove performance — not guess from a single dashboard card.",
            ["Sales", "Restaurants", "Drivers", "Ledger"],
            [
                {
                    "h2": "Prove what the marketplace earned",
                    "paras": [
                        "Reports turn operational noise into decisions: sales with AOV, delivery fees, taxes collected, and category breakdowns; restaurant and driver performance for partner conversations; and the money ledger (transactions) when you need fee-level transparency on payments, payouts, refunds, tips, and wallet movements.",
                        "Use earnings under <a href=\"./monetization.html\">Monetization</a> for commission splits; use reports when you need period analytics and partner scorecards.",
                    ],
                    "blocks": [
                        {
                            "h3": "Weekly operator rhythm",
                            "steps": [
                                "Open <strong>Sales reports</strong> for the period you care about.",
                                "Check restaurant and driver reports for outliers (late deliveries, weak acceptance, top performers).",
                                "Spot-check <strong>Transactions</strong> when a payout or refund is disputed.",
                                "Export or screenshot what your finance process needs (depending on your deployment tools).",
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", f"{A}/features/admin-sales-reports.jpg", "Sales reports", "Sales reporting"),
                        ("wide", f"{A}/features/admin-resto-reports.jpg", "Restaurant reports", "Restaurant performance"),
                        ("wide", f"{A}/features/admin-driver-reports.jpg", "Driver reports", "Driver performance"),
                        ("wide", f"{A}/features/admin-transactions.jpg", "Transactions", "Money ledger / transactions"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    spon_img = "assets/images/features/admin-sponsored.jpg"
    if not (ROOT / spon_img).exists():
        spon_img = "assets/images/features/sponsored.jpg"

    (ROOT / "admin-app/sponsored.html").write_text(
        page(
            "Sponsored listings — Admin app",
            "Sponsored listings",
            "How operators oversee paid placement campaigns that restaurants create from their app.",
            ["Oversight", "Campaigns", "Marketplace"],
            [
                {
                    "h2": "Keep paid placement under control",
                    "paras": [
                        "Restaurants create and launch campaigns from the restaurant app. Admin Sponsored listings is the operator view: which campaigns exist, their state, and enough context to intervene if something should not stay live on the customer feed.",
                        "Use this screen together with the restaurant flow — partners self-serve the creative and bid; you keep marketplace hygiene.",
                    ],
                    "blocks": [
                        {
                            "h3": "Operator workflow",
                            "steps": [
                                "Open <strong>Sponsored listings</strong> in admin.",
                                "Review active and past campaigns (restaurant, placement, status).",
                                "Open View when you need campaign detail or to take an admin action your build exposes.",
                                'Cross-check the customer home / search experience and the <a href="../restaurant-app/sponsored.html">restaurant sponsored</a> form so creative and bid match what you expect.',
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", spon_img, "Admin sponsored", "Sponsored listings in admin"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    print("OK")


if __name__ == "__main__":
    main()
