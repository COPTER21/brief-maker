from pathlib import Path
from playwright.sync_api import sync_playwright

target = Path(__file__).with_name("testcase-warehouse-bin.html").resolve().as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1360, "height": 900})
    page.goto(target)
    page.wait_for_timeout(1200)
    title = page.title()
    text = page.locator("body").inner_text()
    assert "แบบทดสอบ Warehouse & Bin" in title
    assert "TC-A01" in text
    assert "พิมพ์ผลทดสอบ" in text
    page.screenshot(path=str(Path(__file__).with_name("_uat_render_check.png")), full_page=False)
    buttons = page.locator("button")
    assert buttons.count() > 10
    group_button = page.get_by_text("ข้อตกลงและจุดต้องแก้", exact=True)
    assert group_button.count() == 1
    group_button.click()
    page.wait_for_timeout(250)
    assert "TC-I03" in page.locator("body").inner_text()
    assert page.locator("input[type=checkbox], button").count() > 10
    print(f"UAT RENDER: PASS | title={title!r}")
    browser.close()
