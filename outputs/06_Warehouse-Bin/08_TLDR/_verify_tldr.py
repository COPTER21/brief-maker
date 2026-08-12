from pathlib import Path
from playwright.sync_api import sync_playwright

target = Path(__file__).with_name("tldr-warehouse-bin.html").resolve().as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1360, "height": 900})
    page.goto(target)
    page.wait_for_timeout(700)
    text = page.locator("body").inner_text()
    assert page.title() == "สรุปฟีเจอร์ · Warehouse & Bin"
    for phrase in ("ทำอะไรได้ · ทำอะไรไม่ได้", "มี 9 มุมที่ต้องรู้", "กฎสำคัญ · ห้ามพลาด", "จุดที่ต้องเช็กตอนรับงาน"):
        assert phrase in text
    assert page.locator("section").count() == 6
    page.screenshot(path=str(Path(__file__).with_name("_tldr_render_check.png")), full_page=True)
    print("TLDR RENDER: PASS | sections=6")
    browser.close()
