from pathlib import Path
import json
from playwright.sync_api import sync_playwright

workspace = Path(__file__).resolve().parents[3]
source = workspace / "outputs" / "05_Sales_Territory" / "FEATURE_TLDR_F-05.html"
screenshot = Path(__file__).with_name("FEATURE_TLDR_F-05.png")
report = Path(__file__).with_name("render-report.json")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1080})
    page.goto(source.as_uri(), wait_until="load")
    metrics = page.evaluate(
        """() => ({
          title: document.title,
          height: document.documentElement.scrollHeight,
          sections: document.querySelectorAll('section').length,
          externalResources: [...document.querySelectorAll('[src],[href]')]
            .map(el => el.src || el.href)
            .filter(url => /^https?:/i.test(url)),
          visibleTextLength: document.body.innerText.trim().length
        })"""
    )
    metrics["screensAt1440x1080"] = round(metrics["height"] / 1080, 2)
    metrics["horizontalOverflow"] = page.evaluate(
        "document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )
    page.screenshot(path=str(screenshot), full_page=True)
    browser.close()

report.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(metrics, ensure_ascii=False))
