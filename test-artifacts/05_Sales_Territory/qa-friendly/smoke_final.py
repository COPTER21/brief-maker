import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
HTML = ROOT / "outputs" / "05_Sales_Territory" / "testcase-sales-territory.html"
REPORT = Path(__file__).with_name("ui-smoke-report.json")

checks = {}

def check(name, condition, detail=""):
    checks[name] = {"status": "pass" if condition else "fail", "detail": detail}
    if not condition:
        raise AssertionError(f"{name}: {detail}")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(HTML.as_uri(), wait_until="domcontentloaded")
    page.wait_for_timeout(600)

    check("group_nav", page.locator("#grpNav .gn").count() == 6, "expected 6 groups")
    check("case_count", page.locator("section.case").count() == 35, "expected 35 cases")

    page.locator("#grpNav .gn").nth(1).click()
    page.wait_for_timeout(150)
    check("nav_switch", page.url.endswith("#g2") and page.locator("#page-g2.active").count() == 1)

    eye = page.locator("#page-g2 .eyebtn:not(.empty)").first
    eye.click()
    check("eye_modal", page.locator("#lb.show").count() == 1 and page.locator("#lbImg").get_attribute("src", timeout=3000).startswith("data:image/"))
    page.locator("#lb").click(position={"x": 5, "y": 5})

    data_btn = page.locator("#page-g2 .dprev").first
    data_btn.click()
    check("data_sample", page.locator("#dpop.show").count() == 1 and page.locator("#dpop .cpy").count() > 0)
    page.locator("#dpop .x").click()

    first_result = page.locator("#page-g2 .resgrp").first
    first_result.locator("button.pass").click()
    check("pass_click", first_result.locator("button.pass.on").count() == 1)
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(300)
    page.locator("#grpNav .gn").nth(1).click()
    persisted = page.locator("#page-g2 .resgrp").first
    check("persistence", persisted.locator("button.pass.on").count() == 1 and page.evaluate("localStorage.length") > 0)
    persisted.locator("button.fail").click()
    check("fail_click", persisted.locator("button.fail.on").count() == 1)

    page.get_by_role("button", name="พิมพ์ผลทดสอบ (Test Result)").click()
    check("print_preview", page.locator("#preview.show").count() == 1 and page.locator("#pvPaper .rep").count() == 1)
    check("pdf_button", page.locator("#dlPdfBtn").is_visible())
    page.get_by_role("button", name="ปิด").first.click()

    browser.close()

REPORT.write_text(json.dumps({"summary": {"pass": sum(v["status"] == "pass" for v in checks.values()), "fail": sum(v["status"] == "fail" for v in checks.values())}, "checks": checks}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"UI_SMOKE PASS {len(checks)}/{len(checks)} -> {REPORT}")
