from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from playwright.sync_api import Page, sync_playwright


FEATURE_ROOT = Path(__file__).resolve().parents[1]
HTML = FEATURE_ROOT / "01_HTML" / "TaxCode.html"
SHOTS = Path(__file__).resolve().parent / "e2e_shots"
SHOTS.mkdir(parents=True, exist_ok=True)


class RoundResult:
    def __init__(self, name: str):
        self.name = name
        self.started = time.time()
        self.checks: list[dict] = []
        self.page_errors: list[str] = []
        self.console_errors: list[str] = []

    def check(self, condition: bool, label: str, actual=None):
        passed = bool(condition)
        self.checks.append({"name": label, "passed": passed, "actual": actual})
        if not passed:
            raise AssertionError(f"{label}: actual={actual!r}")

    def finish(self):
        return {
            "round": self.name,
            "status": "PASS",
            "duration_seconds": round(time.time() - self.started, 2),
            "checks": self.checks,
            "page_errors": self.page_errors,
            "console_errors": self.console_errors,
        }


def boot(page: Page, result: RoundResult):
    page.on("pageerror", lambda exc: result.page_errors.append(str(exc)))
    page.on(
        "console",
        lambda msg: result.console_errors.append(msg.text) if msg.type == "error" else None,
    )
    page.goto(HTML.resolve().as_uri())
    page.locator(".ph-actions").wait_for(state="visible", timeout=12_000)
    result.check(
        page.evaluate("location.hash") == "#/accounting/setup/tax-codes",
        "production hash route initialized",
        page.evaluate("location.hash"),
    )


def choose_combo(page: Page, key: str, index: int = 0):
    page.locator(f"#ss-input-{key}").click()
    options = page.locator(f"#ss-list-{key} .ss-opt")
    options.first.wait_for(state="visible")
    if options.count() <= index:
        raise AssertionError(f"combobox {key} has only {options.count()} options")
    options.nth(index).click()


def open_create(page: Page):
    page.locator(".ph-actions .btn-primary").click()
    page.locator("#drawer.is-open .dw-title").wait_for(state="visible")


def click_rerender(page: Page, selector: str):
    """Dispatch click for controls whose handler intentionally replaces its own DOM node."""
    page.locator(selector).dispatch_event("click")


def fill_common(page: Page, code: str, name: str):
    text_inputs = page.locator('#drawer input[type="text"]:not(.ss-input)')
    text_inputs.nth(0).fill(code)
    text_inputs.nth(1).fill(name)


def round_1(browser):
    result = RoundResult("1 — smoke, list, filters, picker")
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    boot(page, result)

    result.check(page.locator("h1").is_visible(), "Tax Code heading visible")
    result.check(page.locator("tbody tr").count() == 4, "VAT tab has 4 rows", page.locator("tbody tr").count())

    page.locator(".drawer-tabs .drawer-tab").nth(1).click()
    result.check(page.locator("tbody tr").count() == 5, "WHT tab has 5 rows", page.locator("tbody tr").count())

    search = page.locator(".input-search input")
    search.fill("WHT3")
    result.check(page.locator("tbody tr").count() == 2, "search narrows WHT3 variants", page.locator("tbody tr").count())
    search.fill("")

    page.locator(".filter-status").select_option("draft")
    result.check(page.locator("tbody tr").count() == 1, "draft lifecycle filter", page.locator("tbody tr").count())
    page.locator(".filter-status").select_option("all")

    first_before = page.locator("tbody tr .tc-code").first.inner_text()
    page.locator("thead .sort-btn").first.click()
    first_desc = page.locator("tbody tr .tc-code").first.inner_text()
    result.check(first_before != first_desc, "code sort toggles direction", {"before": first_before, "after": first_desc})
    page.locator("thead .sort-btn").first.click()

    page.locator(".drawer-tabs .drawer-tab").first.click()
    page.locator(".stats .stat").nth(1).click()
    result.check(page.locator("tbody tr").count() == 3, "pickable KPI filter matches VAT rows", page.locator("tbody tr").count())
    page.locator(".stats .stat").first.click()

    page.locator(".ph-actions .btn-secondary").click()
    modal = page.locator("#modalBackdrop.is-open")
    modal.wait_for(state="visible")
    result.check(modal.locator(".pick-row").count() == 3, "sales context exposes 3 VAT codes", modal.locator(".pick-row").count())

    modal.locator("select").select_option("PURCHASE")
    result.check(modal.locator(".pick-row").count() == 5, "purchase context exposes VAT + WHT suggestions", modal.locator(".pick-row").count())
    result.check(modal.locator(".pill-warning").count() == 4, "purchase WHT rows are suggestions", modal.locator(".pill-warning").count())

    modal.locator("select").select_option("PAYMENT")
    result.check(modal.locator(".pick-row").count() == 4, "payment context exposes 4 WHT codes", modal.locator(".pick-row").count())

    date_input = modal.locator('input[type="date"]')
    date_input.fill("2000-01-01")
    date_input.press("Tab")
    result.check(modal.locator(".pick-row").count() == 0, "effective start excludes pre-2017 document", modal.locator(".pick-row").count())
    date_input = modal.locator('input[type="date"]')
    date_input.fill("2026-08-05")
    date_input.press("Tab")
    result.check(modal.locator(".pick-row").count() == 4, "effective date restores current WHT", modal.locator(".pick-row").count())

    modal.locator(".pick-row .btn").first.click()
    result.check(modal.locator(".snapshot-card").is_visible(), "document snapshot rendered")
    result.check(
        page.evaluate("state.pickerSnapshot.consumerContext") == "PAYMENT",
        "snapshot keeps payment consumer context",
        page.evaluate("state.pickerSnapshot.consumerContext"),
    )
    page.screenshot(path=str(SHOTS / "round1_picker_payment_snapshot.png"))

    page.keyboard.press("Escape")
    result.check(page.locator("#modalBackdrop.is-open").count() == 0, "Esc closes picker modal")
    page.wait_for_timeout(300)
    open_create(page)
    result.check(page.evaluate("document.activeElement.closest('#drawer') !== null"), "create drawer focuses first field")
    page.keyboard.press("Escape")
    page.wait_for_timeout(350)
    result.check(page.locator("#drawer.is-open").count() == 0, "Esc closes create drawer")

    result.check(len(result.page_errors) == 0, "no browser page errors", result.page_errors)
    page.close()
    return result.finish()


def round_2(browser):
    result = RoundResult("2 — validation, create, replacement, lifecycle")
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    boot(page, result)

    open_create(page)
    click_rerender(page, "#drawer .dw-footer .btn-primary")
    errors = page.evaluate("Object.keys(state.formErrors).sort()")
    result.check(errors == ["code", "glPurchase", "glSale", "name"], "required VAT validation", errors)

    fill_common(page, "VAT-E2E", "VAT E2E active")
    choose_combo(page, "glSale", 0)
    choose_combo(page, "glPurchase", 3)
    click_rerender(page, "#drawer .dw-footer .btn-primary")
    page.locator("#drawer.is-open").wait_for(state="detached", timeout=4_000)
    created = page.evaluate("state.records.find(r=>r.code==='VAT-E2E')")
    result.check(created and created["status"] == "active", "create active VAT record", created)

    open_create(page)
    fill_common(page, "vat-e2e", "Duplicate code")
    click_rerender(page, "#drawer .dw-footer .btn-primary")
    duplicate_error = page.evaluate("state.formErrors.code")
    result.check(bool(duplicate_error), "duplicate code blocked case-insensitively", duplicate_error)
    page.keyboard.press("Escape")
    page.wait_for_timeout(350)

    open_create(page)
    page.locator("#drawer select").first.select_option("WHT")
    fill_common(page, "WHT-E2E", "WHT E2E active")
    choose_combo(page, "incomeType", 2)
    choose_combo(page, "glWht", 5)
    click_rerender(page, "#drawer .dw-footer .btn-primary")
    page.locator("#drawer.is-open").wait_for(state="detached", timeout=4_000)
    wht = page.evaluate("state.records.find(r=>r.code==='WHT-E2E')")
    result.check(wht and wht["status"] == "active" and wht["incomeCategoryCode"] == "SERVICE", "create active WHT with income mapping", wht)

    open_create(page)
    page.locator("#drawer select").first.select_option("WHT")
    fill_common(page, "DRAFT-E2E", "Draft E2E")
    click_rerender(page, "#drawer .dw-footer .btn-secondary")
    page.wait_for_timeout(500)
    draft = page.evaluate("state.records.find(r=>r.code==='DRAFT-E2E')")
    result.check(draft and draft["status"] == "draft", "save incomplete WHT as draft", draft)

    page.evaluate("state.tab='WHT'; state.filters={search:'DRAFT-E2E',status:'all'}; render()")
    page.locator("tbody tr").first.click()
    page.locator("#drawer .drawer-header-actions .btn-danger").click()
    page.locator("#modalBackdrop .btn-danger").click()
    page.wait_for_timeout(350)
    result.check(page.evaluate("state.records.find(r=>r.code==='DRAFT-E2E').status") == "archived", "archive draft without hard delete")

    page.evaluate("state.tab='VAT'; state.filters={search:'VAT7',status:'all'}; render()")
    page.locator("tbody tr").filter(has_text="VAT7").first.click()
    page.locator("#drawer .drawer-header-actions .btn-secondary").click()
    rate_input = page.locator('#drawer input[type="number"]')
    result.check(rate_input.is_disabled(), "used VAT rate is immutable")
    click_rerender(page, "#drawer .tc-alert .btn-secondary")
    rate_input = page.locator('#drawer input[type="number"]')
    result.check(not rate_input.is_disabled(), "replacement rate is editable")
    rate_input.fill("10")
    page.locator('#drawer input[type="date"]').first.fill("2027-01-01")
    click_rerender(page, "#drawer .dw-footer .btn-primary")
    page.locator("#drawer.is-open").wait_for(state="detached", timeout=4_000)
    replacement = page.evaluate("state.records.find(r=>r.code==='VAT7-N')")
    old = page.evaluate("state.records.find(r=>r.id==='TX-01')")
    result.check(replacement and replacement["replacesTaxCodeId"] == "TX-01", "replacement points to old code", replacement)
    result.check(old["replacedByTaxCodeId"] == replacement["id"] and old["effEnd"] == "2026-12-31", "old code closes before replacement", old)

    page.evaluate("state.filters={search:'VAT7-N',status:'all'}; render()")
    replacement_row = page.locator("tbody tr").first
    replacement_row.locator(".ra-btn.is-danger").click()
    page.locator("#modalBackdrop .btn-danger").click()
    page.wait_for_timeout(350)
    result.check(page.evaluate("state.records.find(r=>r.code==='VAT7-N').status") == "inactive", "deactivate replacement through confirmation")

    result.check(page.evaluate("typeof doDelete === 'undefined'"), "hard-delete function does not exist")
    result.check(page.locator('[data-lucide="trash-2"]').count() == 0, "no trash action exists")
    page.screenshot(path=str(SHOTS / "round2_lifecycle_complete.png"))
    result.check(len(result.page_errors) == 0, "no browser page errors", result.page_errors)
    page.close()
    return result.finish()


def round_3(browser):
    result = RoundResult("3 — permissions, snapshot immutability, overlay resilience")
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    boot(page, result)

    gl_contract = page.evaluate(
        "GL_ACCOUNTS.every(a=>a.companyId===CURRENT_COMPANY.id && a.status==='active' && a.postingAllowed)"
    )
    result.check(gl_contract, "GL lookup contains only current-company active posting accounts")
    result.check(page.evaluate("!isPickable({...state.records[0],effStart:'2030-01-01'}, '2026-08-05')"), "future effective start is excluded")
    result.check(page.evaluate("!isPickable({...state.records[0],effEnd:'2020-01-01'}, '2026-08-05')"), "expired code is excluded")

    page.evaluate("CURRENT_PERMISSIONS.delete('tax_code.create'); render()")
    result.check(page.locator(".ph-actions .btn-primary").count() == 0, "create action hidden without permission")
    page.evaluate("CURRENT_PERMISSIONS.add('tax_code.create'); CURRENT_PERMISSIONS.delete('tax_code.update'); render()")
    result.check(page.locator("tbody .ra-btn:not(.is-danger)").count() == 0, "edit actions hidden without update permission")
    page.evaluate("CURRENT_PERMISSIONS.add('tax_code.update'); render()")

    page.locator(".ph-actions .btn-secondary").click()
    modal = page.locator("#modalBackdrop.is-open")
    modal.locator(".pick-row .btn").first.click()
    snapshot_before = page.evaluate("JSON.stringify(state.pickerSnapshot)")
    page.evaluate("state.records.find(r=>r.id==='TX-01').name='MUTATED MASTER'; state.records.find(r=>r.id==='TX-01').rate=99; render()")
    snapshot_after = page.evaluate("JSON.stringify(state.pickerSnapshot)")
    result.check(snapshot_before == snapshot_after, "document snapshot is immutable when master changes", {"before": snapshot_before, "after": snapshot_after})
    page.screenshot(path=str(SHOTS / "round3_snapshot_immutable.png"))
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    page.evaluate("state.filters={search:'VAT7',status:'all'}; render()")
    page.locator("tbody tr").first.click()
    page.locator("#drawer .drawer-header-actions .btn-danger").click()
    page.wait_for_function("document.querySelector('#modalBackdrop').classList.contains('is-open')")
    overlay_z = page.evaluate("({modal:Number(getComputedStyle(document.querySelector('#modalBackdrop')).zIndex),drawer:Number(getComputedStyle(document.querySelector('#drawer')).zIndex)})")
    result.check(
        page.locator("#modalBackdrop.is-open").count() == 1
        and page.locator("#drawer.is-open").count() == 1
        and overlay_z["modal"] > overlay_z["drawer"],
        "modal stacks above view drawer",
        overlay_z,
    )
    page.keyboard.press("Escape")
    page.wait_for_timeout(250)
    result.check(page.locator("#modalBackdrop.is-open").count() == 0 and page.locator("#drawer.is-open").count() == 1, "first Esc closes top modal only")
    page.keyboard.press("Escape")
    page.wait_for_timeout(350)
    result.check(page.locator("#drawer.is-open").count() == 0, "second Esc closes drawer")

    open_create(page)
    page.locator("#drawer .drawer-body").evaluate("e=>e.scrollTop=e.scrollHeight")
    page.locator("#ss-input-glPurchase").click()
    dropdown = page.locator("#ss-list-glPurchase:not(.hidden)")
    result.check(dropdown.evaluate("e=>e.classList.contains('drop-up')"), "bottom-edge GL dropdown flips upward")
    page.locator("#drawer .drawer-body").click(position={"x": 20, "y": 20})
    result.check(page.locator("#ss-list-glPurchase:not(.hidden)").count() == 0, "outside click closes GL dropdown")
    page.keyboard.press("Escape")

    result.check(len(result.page_errors) == 0, "no browser page errors", result.page_errors)
    page.close()
    return result.finish()


def main():
    report = {
        "html": str(HTML),
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "rounds": [],
        "environment_notes": [
            "Network is restricted in the test sandbox; font/Lucide CDN resource errors are classified separately from page errors.",
            "Each round uses a fresh browser page, so in-memory mock state cannot leak between rounds.",
        ],
    }
    exit_code = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for fn in (round_1, round_2, round_3):
            try:
                report["rounds"].append(fn(browser))
            except Exception as exc:
                exit_code = 1
                report["rounds"].append({"round": fn.__name__, "status": "FAIL", "error": repr(exc)})
                break
        browser.close()

    report["status"] = "PASS" if exit_code == 0 and len(report["rounds"]) == 3 else "FAIL"
    report["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    output = Path(__file__).resolve().parent / "E2E_3_ROUNDS_RESULT.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
