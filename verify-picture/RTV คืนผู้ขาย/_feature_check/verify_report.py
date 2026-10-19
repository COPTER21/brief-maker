from pathlib import Path
from playwright.sync_api import sync_playwright


report = (
    Path(__file__).resolve().parents[1]
    / "FR_F-PUR-RTV-001_R1_20261016.html"
)
errors: list[str] = []

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(report.as_uri(), wait_until="networkidle")
    metrics = page.evaluate(
        """() => ({
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth,
          title: document.title
        })"""
    )
    page.screenshot(path=str(Path(__file__).with_name("report-preview.png")), full_page=True)
    browser.close()

horizontal_scroll = metrics["scrollWidth"] > metrics["clientWidth"]
print(
    {
        "title": metrics["title"],
        "pageerror_count": len(errors),
        "pageerrors": errors,
        "horizontal_scroll": horizontal_scroll,
        "scroll_width": metrics["scrollWidth"],
        "client_width": metrics["clientWidth"],
    }
)

if errors or horizontal_scroll:
    raise SystemExit(1)
