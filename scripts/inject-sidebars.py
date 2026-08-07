#!/usr/bin/env python3
"""Inject shared sidebar — structure by app (no Platform features menu)."""
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

    def link(href: str, label: str, active: bool = False) -> str:
        cls = ' class="active"' if active else ""
        return f'          <a{cls} href="{href}">{label}</a>'

    def section(label: str, items: list[tuple[str, str, bool]]) -> list[str]:
        out = [f'        <p class="sidebar-label">{label}</p>', '        <nav class="nav">']
        for href, text, active in items:
            out.append(link(href, text, active))
        out.append("        </nav>")
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

    is_drv_ov = rel == "delivery-app/index.html"
    is_drv_gs = rel == "delivery-app/getting-started.html"
    is_drv_del = rel == "delivery-app/deliveries.html"
    is_drv_act = rel == "delivery-app/active-delivery.html"
    is_drv_pod = rel == "delivery-app/proof-of-delivery.html"
    is_drv_earn = rel == "delivery-app/earnings.html"
    is_drv_tx = rel == "delivery-app/transactions-payouts.html"
    is_drv_sub = rel == "delivery-app/subscriptions.html"

    is_res_ov = rel == "restaurant-app/index.html"
    is_res_gs = rel == "restaurant-app/getting-started.html"
    is_res_ord = rel == "restaurant-app/orders.html"
    is_res_menu = rel == "restaurant-app/menu.html"
    is_res_hrs = rel == "restaurant-app/hours.html"
    is_res_an = rel == "restaurant-app/analytics.html"
    is_res_kds = rel == "restaurant-app/kitchen-display.html"
    is_res_sub = rel == "restaurant-app/subscriptions.html"
    is_res_spon = rel == "restaurant-app/sponsored.html"

    is_adm_ov = rel == "admin-app/index.html"
    is_adm_gs = rel == "admin-app/getting-started.html"
    is_adm_ord = rel == "admin-app/orders.html"
    is_adm_part = rel == "admin-app/partners.html"
    is_adm_cat = rel == "admin-app/catalog.html"
    is_adm_earn = rel == "admin-app/earnings.html"
    is_adm_sub = rel == "admin-app/subscriptions.html"
    is_adm_gw = rel == "admin-app/gateways.html"
    is_adm_promo = rel == "admin-app/promotions.html"
    is_adm_coup = rel == "admin-app/coupons.html"
    is_adm_lang = rel == "admin-app/languages.html"
    is_adm_cur = rel == "admin-app/currencies-taxes.html"
    is_adm_app = rel == "admin-app/app-settings.html"
    is_adm_spon = rel == "admin-app/sponsored.html"
    is_adm_sales = rel == "admin-app/sales-reports.html"
    is_adm_prep = rel == "admin-app/partner-reports.html"
    is_adm_tx = rel == "admin-app/transactions.html"

    is_be_ov = rel == "my-backend/index.html"
    is_be_gs = rel == "my-backend/getting-started.html"

    cust_ov = f"{prefix}index.html" if not is_cust_ov else "#overview"
    drv_ov = f"{prefix}delivery-app/index.html" if not is_drv_ov else "#overview"
    res_ov = f"{prefix}restaurant-app/index.html" if not is_res_ov else "#overview"
    adm_ov = f"{prefix}admin-app/index.html" if not is_adm_ov else "#overview"
    be_ov = f"{prefix}my-backend/index.html" if not is_be_ov else "#overview"

    lines = [
        f'        <a class="brand-link" href="{prefix}index.html" aria-label="Good Food Pro Docs home">',
        '          <span class="brand-dot" aria-hidden="true"></span>',
        '          <span class="brand-title">Good Food Pro Docs</span>',
        "        </a>",
        *section(
            "All apps",
            [
                (f"{prefix}environment-setup.html", "Environment setup", is_env),
                (f"{prefix}downloads/index.html", "Android downloads", is_dl and rel == "downloads/index.html"),
            ],
        ),
        *section(
            "Customer app",
            [
                (cust_ov, "Overview", is_cust_ov),
                (f"{prefix}getting-started.html", "Getting Started", is_cust_gs),
                (f"{prefix}discovery.html", "Discovery", is_cust_disc),
                (f"{prefix}restaurant-page.html", "Restaurant page", is_cust_resto),
                (f"{prefix}menu-cart.html", "Menu & cart", is_cust_menu),
                (f"{prefix}checkout.html", "Checkout & offers", is_cust_check),
                (f"{prefix}order-history.html", "Order history", is_cust_hist),
                (f"{prefix}order-tracking.html", "Order tracking", is_cust_track),
                (f"{prefix}wallet.html", "Wallet & payments", is_cust_wallet),
                (f"{prefix}subscriptions.html", "Subscriptions", is_cust_sub),
                (f"{prefix}recommendations.html", "Recommendations", is_cust_reco),
                (f"{prefix}smart-eta.html", "Smart ETA", is_cust_eta),
                (f"{prefix}delivery-fee.html", "Delivery fee", is_cust_fee),
            ],
        ),
        *section(
            "Delivery app (driver)",
            [
                (drv_ov, "Overview", is_drv_ov),
                (f"{prefix}delivery-app/getting-started.html", "Getting Started", is_drv_gs),
                (f"{prefix}delivery-app/deliveries.html", "Deliveries", is_drv_del),
                (f"{prefix}delivery-app/active-delivery.html", "Active delivery", is_drv_act),
                (f"{prefix}delivery-app/proof-of-delivery.html", "Proof of delivery", is_drv_pod),
                (f"{prefix}delivery-app/earnings.html", "Earnings", is_drv_earn),
                (f"{prefix}delivery-app/transactions-payouts.html", "Transactions & payouts", is_drv_tx),
                (f"{prefix}delivery-app/subscriptions.html", "Subscriptions", is_drv_sub),
            ],
        ),
        *section(
            "Restaurant app",
            [
                (res_ov, "Overview", is_res_ov),
                (f"{prefix}restaurant-app/getting-started.html", "Getting Started", is_res_gs),
                (f"{prefix}restaurant-app/orders.html", "Live orders", is_res_ord),
                (f"{prefix}restaurant-app/menu.html", "Menu", is_res_menu),
                (f"{prefix}restaurant-app/hours.html", "Hours & delivery", is_res_hrs),
                (f"{prefix}restaurant-app/analytics.html", "Analytics", is_res_an),
                (f"{prefix}restaurant-app/kitchen-display.html", "Kitchen Display (KDS)", is_res_kds),
                (f"{prefix}restaurant-app/subscriptions.html", "Subscriptions", is_res_sub),
                (f"{prefix}restaurant-app/sponsored.html", "Sponsored listings", is_res_spon),
            ],
        ),
        *section(
            "Admin app (web)",
            [
                (adm_ov, "Overview", is_adm_ov),
                (f"{prefix}admin-app/getting-started.html", "Getting Started", is_adm_gs),
                (f"{prefix}admin-app/orders.html", "Orders", is_adm_ord),
                (f"{prefix}admin-app/partners.html", "Partners", is_adm_part),
                (f"{prefix}admin-app/catalog.html", "Catalog", is_adm_cat),
                (f"{prefix}admin-app/earnings.html", "Earnings", is_adm_earn),
                (f"{prefix}admin-app/subscriptions.html", "Subscriptions", is_adm_sub),
                (f"{prefix}admin-app/gateways.html", "Payment gateways", is_adm_gw),
                (f"{prefix}admin-app/promotions.html", "Promotions", is_adm_promo),
                (f"{prefix}admin-app/coupons.html", "Coupons", is_adm_coup),
                (f"{prefix}admin-app/languages.html", "Languages", is_adm_lang),
                (f"{prefix}admin-app/currencies-taxes.html", "Currencies & taxes", is_adm_cur),
                (f"{prefix}admin-app/app-settings.html", "App settings", is_adm_app),
                (f"{prefix}admin-app/sponsored.html", "Sponsored listings", is_adm_spon),
                (f"{prefix}admin-app/sales-reports.html", "Sales reports", is_adm_sales),
                (f"{prefix}admin-app/partner-reports.html", "Partner reports", is_adm_prep),
                (f"{prefix}admin-app/transactions.html", "Transactions", is_adm_tx),
            ],
        ),
        *section(
            "Backend (API)",
            [
                (be_ov, "Overview", is_be_ov),
                (f"{prefix}my-backend/getting-started.html", "Getting Started", is_be_gs),
            ],
        ),
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
