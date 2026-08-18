from pathlib import Path
import sys

from playwright.sync_api import sync_playwright


OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import ready, settle, hush  # noqa: E402


html = Path(__file__).parents[1] / "f-wh-picking.html"
shots = Path(__file__).parent / "ux-evidence"
shots.mkdir(exist_ok=True)

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    ready(page, html.resolve().as_uri() + "#/create/SO-2026-0207")
    hush(page)
    page.screenshot(path=shots / "create-step2.png", full_page=True)
    page.locator("#cbi-wiz-asg").focus()
    settle(page)
    page.screenshot(path=shots / "assignee-combobox.png", full_page=True)
    page.locator("#combo-pop button").first.click()
    settle(page)
    page.screenshot(path=shots / "assignee-selected.png", full_page=True)

    ready(page, html.resolve().as_uri() + "#/view/PICK-2026-0891")
    tabs = page.locator("#view-drawer .drawer-tab")
    for index, name in enumerate(("lines", "detail", "pdf", "history")):
        tabs.nth(index).click()
        settle(page)
        hush(page)
        page.screenshot(path=shots / f"view-{name}.png", full_page=True)

    page.locator("#view-drawer .drawer-tab").nth(0).click()
    settle(page)
    page.get_by_role("button", name="บันทึกหยิบ").first.click()
    settle(page)
    hush(page)
    page.screenshot(path=shots / "pick-line-modal.png", full_page=True)
    page.keyboard.press("Escape")
    settle(page)
    browser.close()

print(f"captured 8 UX evidence files in {shots}")
