import json
import pathlib
import sys

from playwright.sync_api import sync_playwright


report = pathlib.Path(sys.argv[1]).resolve()
viewport_widths = (1280, 390)
results = []

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    for width in viewport_widths:
        page_errors = []
        page = browser.new_page(viewport={"width": width, "height": 900})
        page.on("pageerror", lambda error, errors=page_errors: errors.append(str(error)))
        page.goto(report.as_uri(), wait_until="load")
        page.wait_for_load_state("domcontentloaded")
        metrics = page.evaluate(
            """() => ({
                scrollWidth: document.documentElement.scrollWidth,
                clientWidth: document.documentElement.clientWidth,
                bodyScrollWidth: document.body.scrollWidth
            })"""
        )
        results.append(
            {
                "viewport": width,
                "page_errors": page_errors,
                "horizontal_overflow": max(metrics["scrollWidth"], metrics["bodyScrollWidth"])
                > metrics["clientWidth"],
                "metrics": metrics,
            }
        )
        page.close()
    browser.close()

print(json.dumps(results, ensure_ascii=False))
if any(result["page_errors"] or result["horizontal_overflow"] for result in results):
    raise SystemExit(1)
