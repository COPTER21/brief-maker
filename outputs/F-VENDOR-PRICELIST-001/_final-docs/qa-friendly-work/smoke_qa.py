import json
from pathlib import Path
from playwright.sync_api import sync_playwright

WORK = Path(__file__).resolve().parent
HTML = WORK.parent / "testcase-vendor-price-list.html"
SHOT = WORK / "smoke-main.png"

errors = []
result = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000}, accept_downloads=True)
    page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
    page.on("console", lambda msg: errors.append(f"console {msg.type}: {msg.text}") if msg.type == "error" else None)
    page.goto(HTML.as_uri(), wait_until="domcontentloaded")
    page.locator("#grpNav .gn").first.wait_for(state="visible", timeout=10000)

    result["groups"] = page.locator("#grpNav .gn").count()
    result["cases"] = page.locator("section.case").count()
    result["steps"] = page.locator("table.steps tbody tr").count()
    result["sys_cases"] = page.locator("section.case[data-sys='1']").count()
    result["user_cases"] = result["cases"] - result["sys_cases"]

    page.locator("#case-TC-NAV-01 .eyebtn:not(.empty)").first.click()
    page.locator("#lb.show #lbImg").wait_for(state="visible")
    result["image_viewer"] = page.locator("#lbImg").get_attribute("src").startswith("data:image/")
    page.locator("#lb").click(position={"x": 5, "y": 5})

    page.locator("#gn-g-b").click()
    page.wait_for_function("location.hash === '#g-b'")
    page.locator("#case-TC-CRT-01 .dprev").first.click()
    page.locator("#dpop.show .dpop-inner").wait_for(state="visible")
    result["data_sample_rows"] = page.locator("#dpop.show tbody tr").count()
    page.keyboard.press("Escape")

    page.locator("#case-TC-CRT-01 .qpass").click()
    result["pass_count_after_mark"] = int(page.locator("#ovPass").inner_text())
    result["saved_locally"] = page.evaluate("Object.keys(localStorage).some(k => k.startsWith('qa_F-VENDOR-PRICELIST-001'))")

    page.get_by_role("button", name="พิมพ์ผลทดสอบ (Test Result)").click()
    page.locator("#preview.show #pvPaper").wait_for(state="visible")
    result["report_preview"] = "รายงานผลการทดสอบ" in page.locator("#pvPaper").inner_text()
    result["pdf_button"] = page.locator("#dlPdfBtn").is_enabled()
    with page.expect_download(timeout=30000) as download_info:
        page.locator("#dlPdfBtn").click()
    download = download_info.value
    download_path = download.path()
    result["pdf_download_bytes"] = download_path.stat().st_size if download_path else 0
    page.locator("#preview .acts button", has_text="ปิด").click()

    page.screenshot(path=str(SHOT), full_page=False)
    browser.close()

expected = {"groups": 8, "cases": 62, "steps": 303, "sys_cases": 34, "user_cases": 28}
for key, value in expected.items():
    if result.get(key) != value:
        errors.append(f"{key}: expected {value}, got {result.get(key)}")
for key in ["image_viewer", "saved_locally", "report_preview", "pdf_button"]:
    if result.get(key) is not True:
        errors.append(f"{key}: expected true, got {result.get(key)}")
if result.get("data_sample_rows", 0) < 1:
    errors.append("data_sample_rows: expected at least 1")
if result.get("pass_count_after_mark") != 1:
    errors.append(f"pass_count_after_mark: expected 1, got {result.get('pass_count_after_mark')}")
if result.get("pdf_download_bytes", 0) < 10000:
    errors.append(f"pdf_download_bytes: expected >=10000, got {result.get('pdf_download_bytes')}")

print(json.dumps({"result": result, "errors": errors, "screenshot": str(SHOT)}, ensure_ascii=False))
raise SystemExit(1 if errors else 0)
