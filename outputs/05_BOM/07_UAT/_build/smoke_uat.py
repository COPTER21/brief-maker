import json
from pathlib import Path
from playwright.sync_api import sync_playwright

target = Path(__file__).resolve().parents[1] / "testcase-F-BOM.html"
result = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(target.as_uri(), wait_until="load")
    result["title"] = page.title()
    result["case_count"] = page.locator(".case").count()
    result["group_count"] = page.locator(".gn").count()
    result["eye_buttons"] = page.locator("button.eyebtn:not(.empty)").count()
    result["step_results"] = page.locator(".resgrp").count()
    page.locator(".gn").nth(1).click()
    result["navigation_visible_cases"] = page.locator(".case:visible").count()
    page.locator("#page-g-create button.eyebtn:not(.empty)").first.click()
    result["image_modal_visible"] = page.locator("#lb.show").count() == 1
    page.locator("#lb").click(position={"x": 5, "y": 5})
    page.locator("#page-g-create .resgrp .pass").first.click()
    result["local_storage_written"] = page.evaluate("localStorage.length > 0")
    page.get_by_role("button", name="พิมพ์ผลทดสอบ (Test Result)").click()
    result["preview_visible"] = page.locator("#preview.show").count() == 1
    result["page_errors"] = errors
    browser.close()

print(json.dumps(result, ensure_ascii=False))
