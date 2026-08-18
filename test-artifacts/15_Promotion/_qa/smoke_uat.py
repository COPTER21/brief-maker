from pathlib import Path
from playwright.sync_api import sync_playwright


target = Path(__file__).resolve().parents[1] / "testcase-F-SALES-PROMO.html"
errors = []
failed_requests = []
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
    page.on("console", lambda msg: errors.append(f"console-error: {msg.text}") if msg.type == "error" else None)
    page.on("requestfailed", lambda req: failed_requests.append(req.url))
    page.goto(target.as_uri(), wait_until="load")
    page.wait_for_timeout(500)
    body = page.locator("body").inner_text()
    assert "แบบทดสอบโปรโมชัน" in body
    assert "TC-L01" in body
    assert page.locator("button").count() >= 10
    assert page.locator("img").count() >= 1
    assert page.locator("text=พิมพ์ผลทดสอบ").count() >= 1
    page.get_by_text("สิทธิ์และขอบเขตฟีเจอร์", exact=True).click()
    page.wait_for_timeout(150)
    assert "TC-P04" in page.locator("body").inner_text()
    hard_errors = [item for item in errors if "ERR_NETWORK_ACCESS_DENIED" not in item]
    assert not hard_errors, hard_errors
    print(f"PASS title=1 first_case=1 last_case=1 buttons={page.locator('button').count()} images={page.locator('img').count()} hard_errors=0 blocked_requests={len(failed_requests)}")
    if failed_requests:
        print("BLOCKED " + " | ".join(failed_requests))
    browser.close()
