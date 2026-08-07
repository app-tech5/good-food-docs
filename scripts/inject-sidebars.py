#!/usr/bin/env python3
"""Inject shared sidebar — collapsible app groups (StackFood / GitBook style)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/nass/Documents/good-food-docs")


def rel_prefix(html_path: Path) -> str:
    depth = len(html_path.relative_to(ROOT).parts) - 1
    if depth <= 0:
        return "./"
    return "../" * depth


def build_sidebar(html_path: Path) -> str:
    prefix = rel_prefix(html_path)
    rel = html_path.relative_to(ROOT).as_posix()

    def link(href: str, label: str, active: bool = False, *, indent: int = 12) -> str:
        pad = " " * indent
        cls = ' class="active"' if active else ""
        return f'{pad}<a{cls} href="{href}"><span class="nav-link-text">{label}</span></a>'

    def item_is_active(item) -> bool:
        if isinstance(item, tuple) and len(item) >= 3 and item[0] == "__nested__":
            return any(active for _, _, active in item[2])
        return bool(item[2])

    def nested_subgroup(label: str, items: list[tuple[str, str, bool]], *, force_open: bool = False) -> list[str]:
        any_active = any(active for _, _, active in items)
        open_attr = " open" if (force_open or any_active) else ""
        active_cls = " is-current" if any_active else ""
        out = [
            f'            <details class="nav-nested{active_cls}"{open_attr}>',
            '              <summary class="nav-nested-summary">',
            f'                <span class="nav-nested-title">{label}</span>',
            f'                <span class="nav-count">{len(items)}</span>',
            "              </summary>",
            f'              <nav class="nav nav-nested-links" aria-label="{label}">',
        ]
        for href, text, active in items:
            out.append(link(href, text, active, indent=16))
        out.append("              </nav>")
        out.append("            </details>")
        return out

    def section(label: str, items: list, *, force_open: bool = False) -> list[str]:
        any_active = any(item_is_active(it) for it in items)
        open_attr = " open" if (force_open or any_active) else ""
        active_cls = " is-current" if any_active else ""
        out = [
            f'        <details class="nav-group{active_cls}"{open_attr}>',
            '          <summary class="nav-group-summary">',
            f'            <span class="nav-group-title">{label}</span>',
            f'            <span class="nav-count">{len(items)}</span>',
            "          </summary>",
            '          <nav class="nav" aria-label="' + label + '">',
        ]
        for it in items:
            if isinstance(it, tuple) and len(it) >= 3 and it[0] == "__nested__":
                out.extend(nested_subgroup(it[1], it[2], force_open=False))
            else:
                href, text, active = it
                out.append(link(href, text, active))
        out.append("          </nav>")
        out.append("        </details>")
        return out

    is_env = rel == "environment-setup.html"
    is_dl = rel.startswith("downloads/")

    is_cust_ov = rel == "index.html"
    is_cust_gs = rel == "getting-started.html"
    is_cust_disc = rel == "discovery.html"
    is_cust_resto = rel == "restaurant-page.html"
    is_cust_menu = rel == "menu-cart.html"
    is_cust_check = rel == "checkout.html"
    is_cust_hist = rel == "order-history.html"
    is_cust_track = rel == "order-tracking.html"
    is_cust_wallet = rel == "wallet.html"
    is_cust_sub = rel == "subscriptions.html"
    is_cust_reco = rel == "recommendations.html"
    is_cust_eta = rel == "smart-eta.html"
    is_cust_fee = rel == "delivery-fee.html"
    is_cust_lang = rel == "languages-rtl.html"
    # Redirect stubs still under customer root
    is_cust_redirect = rel in ("ordering.html", "intelligence.html")

    is_drv_ov = rel == "delivery-app/index.html"
    is_drv_gs = rel == "delivery-app/getting-started.html"
    is_drv_del = rel == "delivery-app/deliveries.html"
    is_drv_act = rel == "delivery-app/active-delivery.html"
    is_drv_pod = rel == "delivery-app/proof-of-delivery.html"
    is_drv_earn = rel == "delivery-app/earnings.html"
    is_drv_tx = rel == "delivery-app/transactions-payouts.html"
    is_drv_sub = rel == "delivery-app/subscriptions.html"
    is_drv_lang = rel == "delivery-app/languages.html"
    is_drv_redirect = rel == "delivery-app/logistics.html"

    is_res_ov = rel == "restaurant-app/index.html"
    is_res_gs = rel == "restaurant-app/getting-started.html"
    is_res_ord = rel == "restaurant-app/orders.html"
    is_res_menu = rel == "restaurant-app/menu.html"
    is_res_hrs = rel == "restaurant-app/hours.html"
    is_res_an = rel == "restaurant-app/analytics.html"
    is_res_kds = rel == "restaurant-app/kitchen-display.html"
    is_res_sub = rel == "restaurant-app/subscriptions.html"
    is_res_spon = rel == "restaurant-app/sponsored.html"
    is_res_lang = rel == "restaurant-app/languages.html"
    is_res_redirect = rel == "restaurant-app/operations.html"

    is_adm_ov = rel == "admin-app/index.html"
    is_adm_gs = rel == "admin-app/getting-started.html"
    is_adm_ord = rel == "admin-app/orders.html"
    is_adm_part = rel == "admin-app/partners.html"
    is_adm_cat = rel == "admin-app/catalog.html"
    is_adm_earn = rel == "admin-app/earnings.html"
    is_adm_sub = rel == "admin-app/subscriptions.html"
    is_adm_gw = rel == "admin-app/gateways.html"
    is_adm_gw_stripe = rel == "admin-app/gateway-stripe.html"
    is_adm_gw_paypal = rel == "admin-app/gateway-paypal.html"
    is_adm_gw_flutterwave = rel == "admin-app/gateway-flutterwave.html"
    is_adm_gw_paystack = rel == "admin-app/gateway-paystack.html"
    is_adm_gw_orange = rel == "admin-app/gateway-orangepay.html"
    is_adm_gw_razorpay = rel == "admin-app/gateway-razorpay.html"
    is_adm_gw_cod = rel == "admin-app/gateway-cod.html"
    is_adm_gw_wallet = rel == "admin-app/gateway-wallet.html"
    is_adm_gw_crypto = rel == "admin-app/gateway-crypto.html"
    is_adm_gw_any = (
        is_adm_gw
        or is_adm_gw_stripe
        or is_adm_gw_paypal
        or is_adm_gw_flutterwave
        or is_adm_gw_paystack
        or is_adm_gw_orange
        or is_adm_gw_razorpay
        or is_adm_gw_cod
        or is_adm_gw_wallet
        or is_adm_gw_crypto
    )
    is_adm_promo = rel == "admin-app/promotions.html"
    is_adm_coup = rel == "admin-app/coupons.html"
    is_adm_lang = rel == "admin-app/languages.html"
    is_adm_cur = rel == "admin-app/currencies-taxes.html"
    is_adm_app = rel == "admin-app/app-settings.html"
    is_adm_ch = rel == "admin-app/order-channels.html"
    is_adm_spon = rel == "admin-app/sponsored.html"
    is_adm_sales = rel == "admin-app/sales-reports.html"
    is_adm_prep = rel == "admin-app/partner-reports.html"
    is_adm_tx = rel == "admin-app/transactions.html"
    is_adm_redirect = rel in (
        "admin-app/operations.html",
        "admin-app/monetization.html",
        "admin-app/market.html",
        "admin-app/reports.html",
    )

    is_be_ov = rel == "my-backend/index.html"
    is_be_gs = rel == "my-backend/getting-started.html"
    is_be_ord = rel == "my-backend/order-lifecycle.html"
    is_be_live = rel == "my-backend/live-updates.html"
    is_be_pay = rel == "my-backend/payments-wallet.html"
    is_be_com = rel == "my-backend/commission-engine.html"
    is_be_sub = rel == "my-backend/subscriptions-engine.html"
    is_be_ai = rel == "my-backend/intelligence-engine.html"
    is_be_log = rel == "my-backend/logistics-engine.html"
    is_be_ch = rel == "my-backend/channels-api.html"
    is_be_mkt = rel == "my-backend/market-data.html"
    is_be_cat = rel == "my-backend/catalog-api.html"

    cust_ov = f"{prefix}index.html" if not is_cust_ov else "#overview"
    drv_ov = f"{prefix}delivery-app/index.html" if not is_drv_ov else "#overview"
    res_ov = f"{prefix}restaurant-app/index.html" if not is_res_ov else "#overview"
    adm_ov = f"{prefix}admin-app/index.html" if not is_adm_ov else "#overview"
    be_ov = f"{prefix}my-backend/index.html" if not is_be_ov else "#overview"

    # Which product owns this page (redirect stubs count too)
    in_cust = (
        is_cust_ov
        or is_cust_gs
        or is_cust_disc
        or is_cust_resto
        or is_cust_menu
        or is_cust_check
        or is_cust_hist
        or is_cust_track
        or is_cust_wallet
        or is_cust_sub
        or is_cust_reco
        or is_cust_eta
        or is_cust_fee
        or is_cust_lang
        or is_cust_redirect
    )
    in_drv = rel.startswith("delivery-app/")
    in_res = rel.startswith("restaurant-app/")
    in_adm = rel.startswith("admin-app/")
    in_be = rel.startswith("my-backend/")
    in_suite = is_env or is_dl

    lines = [
        '        <div class="sidebar-head">',
        f'          <a class="brand-link" href="{prefix}index.html" aria-label="Good Food Pro Docs home">',
        '            <span class="brand-mark" aria-hidden="true">GF</span>',
        '            <span class="brand-text">',
        '              <span class="brand-title">Good Food Pro</span>',
        '              <span class="brand-tagline">Marketplace docs</span>',
        "            </span>",
        "          </a>",
        '          <button type="button" class="sidebar-close" aria-label="Close navigation" hidden>&times;</button>',
        "        </div>",
        '        <div class="sidebar-body">',
        *section(
            "Suite",
            [
                (f"{prefix}environment-setup.html", "Environment setup", is_env),
                (f"{prefix}downloads/index.html", "Android downloads", is_dl and rel == "downloads/index.html"),
            ],
            force_open=in_suite or not (in_cust or in_drv or in_res or in_adm or in_be),
        ),
        *section(
            "Customer app",
            [
                (cust_ov, "Overview", is_cust_ov),
                (f"{prefix}getting-started.html", "Getting Started", is_cust_gs),
                (f"{prefix}discovery.html", "Browse & discover", is_cust_disc),
                (f"{prefix}restaurant-page.html", "Restaurant details", is_cust_resto),
                (f"{prefix}menu-cart.html", "Menu & basket", is_cust_menu),
                (f"{prefix}checkout.html", "Checkout & vouchers", is_cust_check),
                (f"{prefix}order-history.html", "Order history", is_cust_hist),
                (f"{prefix}order-tracking.html", "Live tracking", is_cust_track),
                (f"{prefix}wallet.html", "Wallet & cashback", is_cust_wallet),
                (f"{prefix}subscriptions.html", "Membership plans", is_cust_sub),
                (f"{prefix}recommendations.html", "AI recommendations", is_cust_reco),
                (f"{prefix}smart-eta.html", "Smart delivery ETA", is_cust_eta),
                (f"{prefix}delivery-fee.html", "Surge pricing", is_cust_fee),
                (f"{prefix}languages-rtl.html", "Languages & RTL", is_cust_lang),
            ],
            force_open=in_cust,
        ),
        *section(
            "Delivery app",
            [
                (drv_ov, "Overview", is_drv_ov),
                (f"{prefix}delivery-app/getting-started.html", "Getting Started", is_drv_gs),
                (f"{prefix}delivery-app/deliveries.html", "Job board & batching", is_drv_del),
                (f"{prefix}delivery-app/active-delivery.html", "On the road", is_drv_act),
                (f"{prefix}delivery-app/proof-of-delivery.html", "Photo & signature POD", is_drv_pod),
                (f"{prefix}delivery-app/earnings.html", "Shift earnings", is_drv_earn),
                (f"{prefix}delivery-app/transactions-payouts.html", "Payouts & history", is_drv_tx),
                (f"{prefix}delivery-app/subscriptions.html", "Priority plans", is_drv_sub),
                (f"{prefix}delivery-app/languages.html", "Languages & RTL", is_drv_lang),
            ],
            force_open=in_drv or is_drv_redirect,
        ),
        *section(
            "Restaurant app",
            [
                (res_ov, "Overview", is_res_ov),
                (f"{prefix}restaurant-app/getting-started.html", "Getting Started", is_res_gs),
                (f"{prefix}restaurant-app/orders.html", "Incoming orders", is_res_ord),
                (f"{prefix}restaurant-app/menu.html", "Menu management", is_res_menu),
                (f"{prefix}restaurant-app/hours.html", "Hours & delivery zone", is_res_hrs),
                (f"{prefix}restaurant-app/analytics.html", "Performance", is_res_an),
                (f"{prefix}restaurant-app/kitchen-display.html", "Kitchen Display (KDS)", is_res_kds),
                (f"{prefix}restaurant-app/subscriptions.html", "Partner plans", is_res_sub),
                (f"{prefix}restaurant-app/sponsored.html", "Sponsored visibility", is_res_spon),
                (f"{prefix}restaurant-app/languages.html", "Languages & RTL", is_res_lang),
            ],
            force_open=in_res or is_res_redirect,
        ),
        *section(
            "Admin app",
            [
                (adm_ov, "Overview", is_adm_ov),
                (f"{prefix}admin-app/getting-started.html", "Getting Started", is_adm_gs),
                (f"{prefix}admin-app/orders.html", "Orders & support", is_adm_ord),
                (f"{prefix}admin-app/partners.html", "Partners & users", is_adm_part),
                (f"{prefix}admin-app/catalog.html", "Menus & catalog", is_adm_cat),
                (f"{prefix}admin-app/earnings.html", "Commissions & earnings", is_adm_earn),
                (f"{prefix}admin-app/subscriptions.html", "Subscription plans", is_adm_sub),
                (
                    "__nested__",
                    "Payment gateways",
                    [
                        (f"{prefix}admin-app/gateways.html", "Overview", is_adm_gw),
                        (f"{prefix}admin-app/gateway-stripe.html", "Stripe", is_adm_gw_stripe),
                        (f"{prefix}admin-app/gateway-paypal.html", "PayPal", is_adm_gw_paypal),
                        (f"{prefix}admin-app/gateway-flutterwave.html", "Flutterwave", is_adm_gw_flutterwave),
                        (f"{prefix}admin-app/gateway-paystack.html", "Paystack", is_adm_gw_paystack),
                        (f"{prefix}admin-app/gateway-orangepay.html", "OrangePay", is_adm_gw_orange),
                        (f"{prefix}admin-app/gateway-razorpay.html", "Razorpay", is_adm_gw_razorpay),
                        (f"{prefix}admin-app/gateway-cod.html", "Cash on Delivery", is_adm_gw_cod),
                        (f"{prefix}admin-app/gateway-wallet.html", "Internal Wallet", is_adm_gw_wallet),
                        (f"{prefix}admin-app/gateway-crypto.html", "Crypto (Commerce)", is_adm_gw_crypto),
                    ],
                ),
                (f"{prefix}admin-app/promotions.html", "Promo campaigns", is_adm_promo),
                (f"{prefix}admin-app/coupons.html", "Coupon codes", is_adm_coup),
                (f"{prefix}admin-app/languages.html", "Languages & RTL", is_adm_lang),
                (f"{prefix}admin-app/currencies-taxes.html", "Currencies & taxes", is_adm_cur),
                (f"{prefix}admin-app/app-settings.html", "Marketplace settings", is_adm_app),
                (f"{prefix}admin-app/order-channels.html", "Order channels", is_adm_ch),
                (f"{prefix}admin-app/sponsored.html", "Sponsored inventory", is_adm_spon),
                (f"{prefix}admin-app/sales-reports.html", "Sales analytics", is_adm_sales),
                (f"{prefix}admin-app/partner-reports.html", "Partner scorecards", is_adm_prep),
                (f"{prefix}admin-app/transactions.html", "Money ledger", is_adm_tx),
            ],
            force_open=in_adm or is_adm_redirect,
        ),
        *section(
            "Backend API",
            [
                (be_ov, "Overview", is_be_ov),
                (f"{prefix}my-backend/getting-started.html", "Getting Started", is_be_gs),
                (f"{prefix}my-backend/order-lifecycle.html", "Order lifecycle", is_be_ord),
                (f"{prefix}my-backend/live-updates.html", "Live status sync", is_be_live),
                (f"{prefix}my-backend/payments-wallet.html", "Payments & wallet", is_be_pay),
                (f"{prefix}my-backend/commission-engine.html", "Commission engine", is_be_com),
                (f"{prefix}my-backend/subscriptions-engine.html", "Subscriptions engine", is_be_sub),
                (f"{prefix}my-backend/intelligence-engine.html", "AI & pricing brain", is_be_ai),
                (f"{prefix}my-backend/logistics-engine.html", "Logistics engine", is_be_log),
                (f"{prefix}my-backend/channels-api.html", "Hybrid channels", is_be_ch),
                (f"{prefix}my-backend/market-data.html", "Languages & market data", is_be_mkt),
                (f"{prefix}my-backend/catalog-api.html", "Catalog & partners", is_be_cat),
            ],
            force_open=in_be,
        ),
        "        </div>",
    ]
    return "\n".join(lines)


SIDEBAR_RE = re.compile(
    r'<aside class="sidebar" data-docs-sidebar>.*?</aside>',
    re.DOTALL,
)


def inject(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'data-docs-sidebar' not in text:
        print("NO SIDEBAR", path)
        return False
    new_aside = f'<aside class="sidebar" data-docs-sidebar>\n{build_sidebar(path)}\n      </aside>'
    updated, n = SIDEBAR_RE.subn(new_aside, text, count=1)
    if n != 1:
        print("REPLACE FAIL", path, n)
        return False
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        print("updated", path.relative_to(ROOT))
        return True
    return False


def main():
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "node_modules" in path.parts:
            continue
        if inject(path):
            changed += 1
    print(f"done, changed={changed}")


if __name__ == "__main__":
    main()
