from pathlib import Path
import sys

from playwright.sync_api import sync_playwright


outputs = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(outputs / "_SHARED" / "_e2e"))
from uikit import JS_LAYOUT, ready, settle  # noqa: E402


html = Path(__file__).parents[1] / "f-wh-picking.html"
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.route("https://**", lambda route: route.abort())
    ready(page, html.resolve().as_uri() + "?stack-proof=1#/create/SO-2026-0207", timeout=1200)
    page.locator("#cbi-wiz-asg").focus()
    settle(page, timeout=900)
    result = page.evaluate(JS_LAYOUT)
    covered = [row for row in result["menuCovered"] if "combo-pop" in row["menu"]]
    crowded = result["optionCrowded"]
    page.locator("#combo-pop button").first.click()
    settle(page, timeout=900)
    selection_crowded = page.evaluate(JS_LAYOUT)["selectionCrowded"]
    issues = {"covered": covered, "crowded": crowded, "selectionCrowded": selection_crowded}
    print("combo layout:", "FAIL" if covered or crowded or selection_crowded else "PASS", issues)
    browser.close()
sys.exit(1 if covered or crowded or selection_crowded else 0)
