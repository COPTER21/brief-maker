"""Tax Code screen walk for the project-wide :mod:`uikit` auditor."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from uikit import Audit  # noqa: E402


FEATURE_ROOT = Path(__file__).resolve().parents[1]
HTML = FEATURE_ROOT / "01_HTML" / "TaxCode.html"
OUTPUT = Path(__file__).resolve().parent


def wait_ready(page: Page) -> None:
    page.locator(".ph-actions").wait_for(state="visible")
    page.wait_for_function("typeof state !== 'undefined' && typeof render === 'function'")


def wait_overlay(page: Page, selector: str, opened: bool = True) -> None:
    page.wait_for_function(
        "([selector, opened]) => document.querySelector(selector)?.classList.contains('is-open') === opened",
        arg=[selector, opened],
    )


def wait_state_closed(page: Page, kind: str) -> None:
    page.wait_for_function("kind => !state[kind].open", arg=kind)


def close_modal(page: Page) -> None:
    if page.locator("#modalBackdrop.is-open").count():
        page.keyboard.press("Escape")
        wait_overlay(page, "#modalBackdrop", False)
        wait_state_closed(page, "modal")


def close_drawer(page: Page) -> None:
    if page.locator("#drawer.is-open").count():
        page.keyboard.press("Escape")
        wait_overlay(page, "#drawer", False)
        wait_state_closed(page, "drawer")


def open_create(page: Page) -> None:
    page.locator(".ph-actions .btn-primary").click()
    wait_overlay(page, "#drawer", True)
    page.locator("#drawer .dw-title").wait_for(state="visible")


def choose_combo(page: Page, key: str, index: int = 0) -> None:
    page.locator(f"#ss-input-{key}").click()
    options = page.locator(f"#ss-list-{key} .ss-opt")
    options.first.wait_for(state="visible")
    options.nth(index).click()


def fill_common(page: Page, code: str, name: str) -> None:
    inputs = page.locator('#drawer input[type="text"]:not(.ss-input)')
    inputs.nth(0).fill(code)
    inputs.nth(1).fill(name)


def click_rerender(page: Page, selector: str) -> None:
    page.locator(selector).dispatch_event("click")


def walk_layout(a: Audit, pg: Page, tag: str) -> None:
    """Open every materially different Tax Code scene and scan rendered pixels."""
    a.open(pg)
    wait_ready(pg)
    a.scan(pg, f"{tag}-01-vat-list")

    pg.locator(".drawer-tabs .drawer-tab").nth(1).click()
    a.scan(pg, f"{tag}-02-wht-list")

    # Picker modal exercises a centered overlay plus dense result rows.
    pg.locator(".ph-actions .btn-secondary").click()
    wait_overlay(pg, "#modalBackdrop", True)
    a.scan(pg, f"{tag}-03-picker-modal")
    close_modal(pg)

    # View drawer and a confirmation modal stacked above it.
    pg.evaluate("state.tab='VAT'; state.filters={search:'VAT7',status:'all'}; render()")
    pg.locator("tbody tr").first.click()
    wait_overlay(pg, "#drawer", True)
    a.scan(pg, f"{tag}-04-view-drawer")
    pg.locator("#drawer .drawer-header-actions .btn-danger").click()
    wait_overlay(pg, "#modalBackdrop", True)
    a.scan(pg, f"{tag}-05-confirm-over-drawer")
    close_modal(pg)
    close_drawer(pg)

    # Create drawer, conditional WHT fields, and an expanded master combobox.
    pg.evaluate("state.filters={search:'',status:'all'}; render()")
    open_create(pg)
    a.scan(pg, f"{tag}-06-create-vat")
    pg.locator("#drawer select").first.select_option("WHT")
    pg.locator("#ss-input-glWht").click()
    pg.locator("#ss-list-glWht:not(.hidden)").wait_for(state="visible")
    a.scan(pg, f"{tag}-07-create-wht-gl-menu")


def walk_behavior(a: Audit, pg: Page) -> None:
    """Exercise keyboard, submission, overlay, refresh, and invalid-route flows."""
    a.open(pg)
    wait_ready(pg)
    a.check(
        pg.evaluate("location.hash") == "#/accounting/setup/tax-codes",
        "production route initializes correctly",
        measured=pg.evaluate("location.hash"),
        expected="#/accounting/setup/tax-codes",
    )

    # Tabs must support both Enter and Space like pointer activation.
    tabs = pg.locator(".drawer-tabs .drawer-tab")
    tabs.nth(1).focus()
    pg.keyboard.press("Enter")
    a.check(pg.evaluate("state.tab") == "WHT", "WHT tab works with Enter", measured=pg.evaluate("state.tab"), expected="WHT")
    tabs = pg.locator(".drawer-tabs .drawer-tab")
    tabs.nth(0).focus()
    pg.keyboard.press("Space")
    a.check(pg.evaluate("state.tab") == "VAT", "VAT tab works with Space", measured=pg.evaluate("state.tab"), expected="VAT")

    user_chip = pg.locator(".user-chip")
    user_chip.focus()
    pg.keyboard.press("Enter")
    a.check(pg.locator("#userMenu.is-open").count() == 1, "user menu works with Enter")
    pg.evaluate("document.getElementById('userMenu').classList.remove('is-open')")

    first_stat = pg.locator(".stat.is-clickable").nth(1)
    first_stat.focus()
    pg.keyboard.press("Space")
    a.check(pg.evaluate("state.filters.status") == "pickable", "KPI filter works with Space", measured=pg.evaluate("state.filters.status"), expected="pickable")
    a.check(bool(pg.locator("#notifBtn").get_attribute("aria-label")), "notification button has an accessible name", measured=pg.locator("#notifBtn").get_attribute("aria-label"), expected="non-empty aria-label")

    # Open and close each top-level overlay twice.
    for attempt in (1, 2):
        pg.locator(".ph-actions .btn-secondary").click()
        wait_overlay(pg, "#modalBackdrop", True)
        pg.keyboard.press("Escape")
        wait_overlay(pg, "#modalBackdrop", False)
        wait_state_closed(pg, "modal")
        a.check(pg.locator("#modalBackdrop.is-open").count() == 0, f"picker closes with Esc (attempt {attempt})")

    for attempt in (1, 2):
        open_create(pg)
        pg.keyboard.press("Escape")
        wait_overlay(pg, "#drawer", False)
        wait_state_closed(pg, "drawer")
        a.check(pg.locator("#drawer.is-open").count() == 0, f"create drawer closes with Esc (attempt {attempt})")

    # Submit VAT validation and then a valid VAT form.
    open_create(pg)
    click_rerender(pg, "#drawer .dw-footer .btn-primary")
    vat_errors = pg.evaluate("Object.keys(state.formErrors).sort()")
    a.check(
        vat_errors == ["code", "glPurchase", "glSale", "name"],
        "VAT form exposes all required-field errors",
        measured=vat_errors,
        expected=["code", "glPurchase", "glSale", "name"],
    )
    fill_common(pg, "VAT-UI", "VAT UI audit")
    choose_combo(pg, "glSale", 0)
    choose_combo(pg, "glPurchase", 3)
    click_rerender(pg, "#drawer .dw-footer .btn-primary")
    wait_state_closed(pg, "drawer")
    vat = pg.evaluate("state.records.find(r=>r.code==='VAT-UI')")
    a.check(bool(vat and vat["status"] == "active"), "valid VAT form submits", measured=vat, expected="active record")

    # Submit WHT validation and then a valid WHT form.
    open_create(pg)
    pg.locator("#drawer select").first.select_option("WHT")
    click_rerender(pg, "#drawer .dw-footer .btn-primary")
    wht_errors = pg.evaluate("Object.keys(state.formErrors).sort()")
    a.check(
        wht_errors == ["code", "glWht", "incomeType", "name"],
        "WHT form exposes all required-field errors",
        measured=wht_errors,
        expected=["code", "glWht", "incomeType", "name"],
    )
    fill_common(pg, "WHT-UI", "WHT UI audit")
    choose_combo(pg, "incomeType", 2)
    choose_combo(pg, "glWht", 5)
    click_rerender(pg, "#drawer .dw-footer .btn-primary")
    wait_state_closed(pg, "drawer")
    wht = pg.evaluate("state.records.find(r=>r.code==='WHT-UI')")
    a.check(bool(wht and wht["status"] == "active"), "valid WHT form submits", measured=wht, expected="active record")

    # Critical regression: close stacked modal and drawer with consecutive Esc.
    pg.evaluate("state.tab='VAT'; state.filters={search:'VAT7',status:'all'}; render()")
    pg.locator("tbody tr").first.click()
    wait_overlay(pg, "#drawer", True)
    pg.locator("#drawer .drawer-header-actions .btn-danger").click()
    wait_overlay(pg, "#modalBackdrop", True)
    pg.keyboard.press("Escape")
    pg.keyboard.press("Escape")
    try:
        pg.wait_for_function(
            "!state.modal.open && !state.drawer.open && !document.querySelector('#modalBackdrop').classList.contains('is-open') && !document.querySelector('#drawer').classList.contains('is-open')",
            timeout=800,
        )
    except PlaywrightTimeoutError:
        pass
    stacked_state = pg.evaluate("({modal:state.modal.open,drawer:state.drawer.open,modalClass:document.querySelector('#modalBackdrop').classList.contains('is-open'),drawerClass:document.querySelector('#drawer').classList.contains('is-open')})")
    a.check(
        not any(stacked_state.values()),
        "consecutive Esc closes modal then drawer without stale backdrop",
        measured=stacked_state,
        expected={"modal": False, "drawer": False, "modalClass": False, "drawerClass": False},
    )
    if stacked_state["modal"] or stacked_state["drawer"]:
        pg.evaluate("state.modal={open:false,type:null,data:null}; state.drawer={open:false,mode:null,recordId:null,step:1}; document.querySelector('#modalBackdrop').classList.remove('is-open'); document.querySelector('#drawerBackdrop').classList.remove('is-open'); render()")

    # Refresh the valid production route and a route that does not exist.
    pg.evaluate("location.hash='#/accounting/setup/tax-codes'")
    pg.reload(wait_until="load")
    wait_ready(pg)
    a.check(pg.locator("h1").is_visible(), "valid route survives refresh", measured=pg.evaluate("location.hash"))

    pg.evaluate("location.hash='#/this-route-does-not-exist'")
    pg.reload(wait_until="load")
    wait_ready(pg)
    invalid = {"hash": pg.evaluate("location.hash"), "headingVisible": pg.locator("h1").is_visible()}
    a.check(
        invalid["headingVisible"],
        "invalid route does not produce a blank screen",
        measured=invalid,
        expected={"headingVisible": True},
        severity="WARN",
    )


def main() -> int:
    audit = Audit(
        HTML,
        OUTPUT,
        widths=(1280, 1440, 1920, 2560),
        browsers=("chromium",),
        deterministic_screenshots=True,
    )
    report = audit.run(walk_layout, walk_behavior)
    print(json.dumps({"status": report["status"], "summary": report["summary"]}, ensure_ascii=False, indent=2))
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
