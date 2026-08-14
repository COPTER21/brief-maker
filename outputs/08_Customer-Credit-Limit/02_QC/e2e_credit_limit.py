from pathlib import Path
import re
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "01_HTML" / "f-credit-limit.html"
SHOTS = ROOT / "02_QC" / "_e2e_shots"
SHOTS.mkdir(exist_ok=True)


def snap(page, name):
    page.screenshot(path=str(SHOTS / f"{name}.png"), full_page=True)


def open_customer(page, customer_code):
    page.locator("tbody tr").filter(has_text=customer_code).click()
    expect(page.locator("#drawerEl")).to_have_class(re.compile(r"\bis-open\b"))


def round_one(browser):
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(HTML.as_uri())
    expect(page.locator("tbody tr")).to_have_count(8)
    snap(page, "r1_01_list")

    open_customer(page, "CUST-2026-0033")
    expect(page.get_by_text("ภาพรวม", exact=True)).to_be_visible()
    page.get_by_role("button", name="ทบทวน").click()
    expect(page.locator("#toastWrap")).to_contain_text("บันทึกการทบทวนเครดิตแล้ว")

    page.get_by_role("button", name="ระงับเครดิต", exact=True).click()
    expect(page.get_by_role("button", name="ยืนยันระงับ")).to_be_disabled()
    page.locator("#modalCard textarea").fill("ทดสอบ E2E: ระงับชั่วคราว")
    page.get_by_role("button", name="ยืนยันระงับ").click()
    expect(page.locator("#toastWrap")).to_contain_text("ระงับเครดิตแล้ว")
    snap(page, "r1_02_hold")

    page.get_by_role("button", name="ปลดระงับ", exact=True).click()
    page.locator("#modalCard textarea").fill("ทดสอบ E2E: ปลดระงับแล้ว")
    page.get_by_role("button", name="ยืนยันปลดระงับ").click()
    expect(page.locator("#toastWrap")).to_contain_text("ปลดระงับเครดิตแล้ว")
    page.keyboard.press("Escape")
    expect(page.locator("#drawerEl")).not_to_have_class(re.compile(r"\bis-open\b"))
    page.close()


def round_two(browser):
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(HTML.as_uri())
    search = page.locator("#credit-search")
    search.click()
    search.press_sequentially("CUST-2026-0058")
    expect(search).to_be_focused()
    expect(page.locator("tbody tr")).to_have_count(1)
    search.fill("ไม่มีข้อมูล-E2E")
    expect(page.get_by_text("ไม่พบข้อมูลตามเงื่อนไข")).to_be_visible()
    page.get_by_role("button", name="ล้างตัวกรอง").first.click()
    expect(page.locator("tbody tr")).to_have_count(8)

    open_customer(page, "CUST-2026-0033")
    page.get_by_role("button", name="ปรับวงเงิน").click()
    expect(page.locator("#chg-submit")).to_be_disabled()
    page.locator("#chg-amt").fill("1100000")
    page.locator("#chg-reason").fill("ทดสอบ E2E: ปรับวงเงินตาม DOA")
    expect(page.locator("#chg-submit")).to_be_enabled()
    page.locator("#chg-amt").fill("1200000")
    expect(page.locator("#chg-submit")).to_be_disabled()
    page.locator("#chg-amt").fill("1100000")
    expect(page.locator("#chg-submit")).to_be_enabled()
    page.get_by_role("button", name="บันทึกคำขอ").click()
    expect(page.locator("#drawerEl").get_by_text("รอส่งอนุมัติ", exact=True)).to_be_visible()
    page.get_by_role("button", name="ส่งอนุมัติ", exact=True).click()
    expect(page.locator("#drawerEl").get_by_text("รออนุมัติ", exact=True)).to_be_visible()
    expect(page.locator(".sec-t").filter(has_text="คำขอปรับวงเงิน")).to_be_visible()
    snap(page, "r2_01_pending")

    while page.get_by_role("button", name="อนุมัติขั้น", exact=False).count():
        page.get_by_role("button", name="อนุมัติขั้น", exact=False).click()
    expect(page.get_by_text("ไม่มีคำขอค้างอนุมัติ", exact=False)).to_be_visible()
    page.locator(".drawer-tabs").get_by_role("button", name="ประวัติ", exact=False).click()
    expect(page.get_by_text("อนุมัติครบสาย", exact=False).first).to_be_visible()
    snap(page, "r2_02_approved_history")
    page.close()


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            round_one(browser)
            round_two(browser)
        finally:
            browser.close()
    print("E2E PASS: 2 rounds completed")


if __name__ == "__main__":
    main()
