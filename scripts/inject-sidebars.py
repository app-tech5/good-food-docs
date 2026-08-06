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
    is_cust_ord = rel == "ordering.html"
    is_cust_wallet = rel == "wallet.html"
    is_cust_sub = rel == "subscriptions.html"
    is_cust_ai = rel == "intelligence.html"
    is_cust_track = rel == "order-tracking.html"

    is_drv_ov = rel == "delivery-app/index.html"
    is_drv_gs = rel == "delivery-app/getting-started.html"
    is_drv_log = rel == "delivery-app/logistics.html"
    is_drv_earn = rel == "delivery-app/earnings.html"
    is_drv_sub = rel == "delivery-app/subscriptions.html"

    is_res_ov = rel == "restaurant-app/index.html"
    is_res_gs = rel == "restaurant-app/getting-started.html"
    is_res_ops = rel == "restaurant-app/operations.html"
    is_res_kds = rel == "restaurant-app/kitchen-display.html"
    is_res_sub = rel == "restaurant-app/subscriptions.html"
    is_res_spon = rel == "restaurant-app/sponsored.html"

    is_adm_ov = rel == "admin-app/index.html"
    is_adm_gs = rel == "admin-app/getting-started.html"
    is_adm_ops = rel == "admin-app/operations.html"
    is_adm_mon = rel == "admin-app/monetization.html"
    is_adm_promo = rel == "admin-app/promotions.html"
    is_adm_mkt = rel == "admin-app/market.html"
    is_adm_spon = rel == "admin-app/sponsored.html"
    is_adm_rep = rel == "admin-app/reports.html"

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
                (f"{prefix}ordering.html", "Ordering & discovery", is_cust_ord),
                (f"{prefix}wallet.html", "Wallet & payments", is_cust_wallet),
                (f"{prefix}subscriptions.html", "Subscriptions", is_cust_sub),
                (f"{prefix}intelligence.html", "AI intelligence", is_cust_ai),
                (f"{prefix}order-tracking.html", "Order tracking", is_cust_track),
            ],
        ),
        *section(
            "Delivery app (driver)",
            [
                (drv_ov, "Overview", is_drv_ov),
                (f"{prefix}delivery-app/getting-started.html", "Getting Started", is_drv_gs),
                (f"{prefix}delivery-app/logistics.html", "Logistics & POD", is_drv_log),
                (f"{prefix}delivery-app/earnings.html", "Earnings & payouts", is_drv_earn),
                (f"{prefix}delivery-app/subscriptions.html", "Subscriptions", is_drv_sub),
            ],
        ),
        *section(
            "Restaurant app",
            [
                (res_ov, "Overview", is_res_ov),
                (f"{prefix}restaurant-app/getting-started.html", "Getting Started", is_res_gs),
                (f"{prefix}restaurant-app/operations.html", "Orders & menu", is_res_ops),
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
                (f"{prefix}admin-app/operations.html", "Operations", is_adm_ops),
                (f"{prefix}admin-app/monetization.html", "Monetization", is_adm_mon),
                (f"{prefix}admin-app/promotions.html", "Promotions & coupons", is_adm_promo),
                (f"{prefix}admin-app/market.html", "Market & languages", is_adm_mkt),
                (f"{prefix}admin-app/sponsored.html", "Sponsored listings", is_adm_spon),
                (f"{prefix}admin-app/reports.html", "Reports & analytics", is_adm_rep),
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
