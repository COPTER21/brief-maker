from pathlib import Path

from playwright.sync_api import sync_playwright


report = Path(__file__).resolve().parents[1] / "FR_F-BOM-001_R1_20261020.html"
preview = Path(__file__).with_name("report-preview.png")
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
    page.screenshot(path=str(preview), full_page=True)
    browser.close()

horizontal_overflow = metrics["scrollWidth"] > metrics["clientWidth"]
print(
    {
        "pageerrors": errors,
        "pageerror_count": len(errors),
        "horizontal_overflow": horizontal_overflow,
        "metrics": metrics,
        "preview": str(preview),
    }
)

if errors or horizontal_overflow:
    raise SystemExit(1)
