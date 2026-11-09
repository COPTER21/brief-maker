import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


target = Path(sys.argv[1]).resolve().as_uri()
errors = []

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(target, wait_until="load")
    dimensions = page.evaluate(
        """() => ({
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth
        })"""
    )
    browser.close()

print(json.dumps({"pageerrors": errors, "horizontal_overflow": dimensions["scrollWidth"] > dimensions["clientWidth"], **dimensions}, ensure_ascii=False))
