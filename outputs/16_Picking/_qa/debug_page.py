from pathlib import Path
from playwright.sync_api import sync_playwright


page_path = Path(__file__).parents[1] / "f-wh-picking.html"
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1024, "height": 900})
    errors = []
    page.on("console", lambda msg: errors.append(f"console {msg.type}: {msg.text}"))
    page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
    page.goto(page_path.resolve().as_uri(), wait_until="load")
    page.wait_for_load_state("domcontentloaded")
    print("\n".join(errors) if errors else "no browser errors")
    print("page-content:", page.locator("#page-content").inner_text()[:500])
    browser.close()
