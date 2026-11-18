import json
from pathlib import Path

from playwright.sync_api import sync_playwright


report = (
    Path(__file__).resolve().parent.parent
    / "FR_F-TMP-001_R1_20261117.html"
)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page_errors = []
    page.on("pageerror", lambda error: page_errors.append(str(error)))
    page.goto(report.as_uri(), wait_until="networkidle")
    dimensions = page.evaluate(
        """() => ({
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth
        })"""
    )
    result = {
        "report": str(report),
        "page_errors": page_errors,
        "horizontal_overflow": dimensions["scrollWidth"] > dimensions["clientWidth"],
        "dimensions": dimensions,
    }
    print(json.dumps(result, ensure_ascii=False))
    browser.close()

if result["page_errors"] or result["horizontal_overflow"]:
    raise SystemExit(1)
