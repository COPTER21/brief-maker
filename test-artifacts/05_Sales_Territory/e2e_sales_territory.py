from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from playwright.sync_api import Page, sync_playwright


ROOT = Path(__file__).resolve().parent
WORKSPACE = Path(__file__).resolve().parents[2]
HTML = WORKSPACE / "outputs" / "05_Sales_Territory" / "sales-territory.html"
EVIDENCE = ROOT / "_e2e_evidence"
RESULTS = ROOT / "_e2e_results.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_round(browser_type, round_no: int, width: int, height: int) -> dict:
    shot_dir = EVIDENCE / f"run-{round_no}"
    shot_dir.mkdir(parents=True, exist_ok=True)
    browser = browser_type.launch(headless=True)
    context = browser.new_context(viewport={"width": width, "height": height})
    page = context.new_page()
    page.set_default_timeout(3000)
    console_errors: list[str] = []
    font_resource_errors: list[str] = []
    page_errors: list[str] = []
    def on_console(msg) -> None:
        if msg.type != "error":
            return
        location = msg.location or {}
        url = location.get("url", "")
        entry = f"{msg.text} [{url}]"
        if any(host in url for host in ("fonts.googleapis.com", "fonts.gstatic.com", "api.fontshare.com")):
            font_resource_errors.append(entry)
        else:
            console_errors.append(entry)
    page.on("console", on_console)
    page.on("pageerror", lambda exc: page_errors.append(str(exc)))
    cases: list[dict] = []

    def case(case_id: str, name: str, action: Callable[[], None]) -> None:
        try:
            action()
            cases.append({"id": case_id, "name": name, "status": "PASS", "error": ""})
            print(f"run {round_no} {case_id} PASS", flush=True)
        except Exception as exc:  # evidence runner must continue and report every case
            cases.append({"id": case_id, "name": name, "status": "FAIL", "error": str(exc)})
            print(f"run {round_no} {case_id} FAIL: {exc}", flush=True)

    def shot(name: str) -> None:
        page.screenshot(path=str(shot_dir / f"{name}.png"), full_page=False)

    def wait_render() -> None:
        page.wait_for_timeout(80)

    page.goto(HTML.as_uri(), wait_until="load")
    page.wait_for_selector("#page-content .ph-title")
    province_count_before = int(page.locator(".stat").nth(1).locator(".stat-value").inner_text())

    case("TC-01", "Initial load, title and canonical hash route", lambda: (
        require(page.url.endswith("#/sales-territory"), f"unexpected route: {page.url}"),
        require(page.locator(".ph-title").inner_text() == "ผังเขตขาย", "page title missing"),
        require(page.locator(".stat").count() == 4, "expected four summary stats"),
    ))
    shot("01-initial")

    case("TC-02", "Initial runtime has no page/console errors", lambda: (
        require(not page_errors, f"page errors: {page_errors}"),
        require(not console_errors, f"console errors: {console_errors}"),
    ))

    def workload() -> None:
        page.get_by_role("tab").nth(1).click()
        wait_render()
        require(page.get_by_text("capacity", exact=False).count() > 0, "workload content not rendered")
        require(page.get_by_role("tab").nth(1).get_attribute("aria-selected") == "true", "workload tab not selected")
    case("TC-03", "Navigate to workload tab", workload)
    shot("02-workload")

    def map_tab() -> None:
        page.get_by_role("tab").nth(2).click()
        wait_render()
        require(page.locator(".map-wrap").count() == 1, "map layout not rendered")
        require(page.locator("#mapTip").count() == 1, "map tooltip host missing")
        page.locator(".mchip").nth(1).click()
        require("is-on" in (page.locator(".mchip").nth(1).get_attribute("class") or ""), "region map filter not selected")
        page.locator(".mchip").first.click()
    case("TC-04", "Navigate to interactive map tab", map_tab)
    shot("03-map")

    def structure_tab() -> None:
        page.get_by_role("tab").nth(0).click()
        wait_render()
        require(page.locator("#qInput").count() == 1, "structure search missing")
    case("TC-05", "Return to structure tab", structure_tab)

    def search_result() -> None:
        page.locator("#qInput").fill("R-CM-01")
        wait_render()
        require(page.locator("tbody tr").filter(has_text="R-CM-01").count() == 1, "expected route not found")
    case("TC-06", "Search by Route code", search_result)

    def empty_search() -> None:
        page.locator("#qInput").fill("NO-SUCH-ROUTE-999")
        wait_render()
        require(page.locator(".empty").is_visible(), "empty state not visible")
        require(page.locator(".empty button").is_visible(), "empty-state reset action missing")
    case("TC-07", "Search empty state has recovery action", empty_search)
    shot("04-empty-search")

    def reset_search() -> None:
        page.locator(".empty button").click()
        wait_render()
        require(page.locator("#qInput").input_value() == "", "search was not reset")
        require(page.locator("tbody tr").count() > 1, "table did not recover")
    case("TC-08", "Reset search/filter from empty state", reset_search)

    def archived_filter() -> None:
        page.locator(".filter-bar select").select_option("archived")
        wait_render()
        require(page.locator("tbody tr").filter(has_text="B2B-S-01").count() == 1, "seed archived route missing")
    case("TC-09", "Status filter: archived", archived_filter)

    def all_filter() -> None:
        page.locator(".filter-bar select").select_option("all")
        wait_render()
        require(page.locator("tbody tr").filter(has_text="B2B-S-01").count() == 1, "all filter omitted archived route")
        page.locator(".filter-bar select").select_option("active")
        wait_render()
    case("TC-10", "Status filter: all then active", all_filter)

    def open_view() -> None:
        page.locator("tbody tr").filter(has_text="R-CM-01").click()
        wait_render()
        require(page.locator("#drawerEl").get_attribute("class").find("is-open") >= 0, "view drawer not open")
        require(page.locator("#drawerEl .drawer-title").inner_text().find("R-CM-01") >= 0, "route identity missing")
    case("TC-11", "Row click opens view-first detail drawer", open_view)
    shot("05-view-drawer")

    def future_customer() -> None:
        before = page.url
        page.locator("#drawerEl .related-actions button").nth(0).click()
        require(page.locator("#toastWrap .toast").last.is_visible(), "future-hook warning toast missing")
        require("ยังไม่พร้อม" in page.locator("#toastWrap .toast").last.inner_text(), "future hook not labeled unavailable")
        require(page.url == before, "future hook navigated unexpectedly")
    case("TC-12", "Customer future hook remains non-functional and labeled", future_customer)

    def future_visit() -> None:
        before = page.url
        page.locator("#drawerEl .related-actions button").nth(1).click()
        require("ยังไม่พร้อม" in page.locator("#toastWrap .toast").last.inner_text(), "Visit hook not labeled unavailable")
        require(page.url == before, "Visit hook navigated unexpectedly")
    case("TC-13", "Visit future hook remains non-functional and labeled", future_visit)

    def drawer_esc() -> None:
        page.keyboard.press("Escape")
        wait_render()
        require("is-open" not in (page.locator("#drawerEl").get_attribute("class") or ""), "Esc did not close view drawer")
    case("TC-14", "Esc closes view drawer", drawer_esc)

    def create_focus_geometry() -> None:
        page.locator(".ph-actions .btn-primary").click()
        wait_render()
        require(page.locator("#drawerEl").is_visible(), "create drawer not visible")
        require(page.evaluate("document.activeElement === document.querySelector('#fld-code input')"), "first create field not focused")
        box = page.locator("#drawerEl").bounding_box()
        require(box is not None and box["width"] <= width and box["height"] <= height, "drawer exceeds viewport")
    case("TC-15", "Create drawer opens, focuses first field, fits viewport", create_focus_geometry)

    def blank_validation() -> None:
        page.locator("#btn-save").click()
        wait_render()
        require(page.locator(".field.is-error").count() == 3, "blank form should flag code, name and salesperson")
        require(page.locator("#toastWrap .toast").last.is_visible(), "validation toast missing")
    case("TC-16", "Blank create validation and error state", blank_validation)
    shot("06-create-validation")

    def duplicate_validation() -> None:
        page.locator("#fld-code input").fill("R-CM-01")
        page.locator("#fld-name input").fill(f"E2E Route {round_no}")
        page.locator("#cbi-rep").click()
        page.locator("#dd-portal .cb-item").first.click()
        page.locator("#btn-save").click()
        wait_render()
        require("is-error" in (page.locator("#fld-code").get_attribute("class") or ""), "duplicate code was not blocked")
        require(page.locator("#drawerEl").is_visible(), "drawer closed despite duplicate code")
    case("TC-17", "Duplicate Route code is blocked", duplicate_validation)

    def combo_empty_esc() -> None:
        page.locator("#cbi-rep").click()
        page.locator("#cbi-rep").fill("__missing_salesperson__")
        wait_render()
        require(page.locator("#dd-portal .cb-empty").is_visible(), "combobox empty row missing")
        require("Sales Team / Salesperson" in page.locator("#dd-portal .cb-empty").inner_text(), "empty row lacks future master label")
        shot("07-combobox-empty")
        page.keyboard.press("Escape")
        wait_render()
        require(page.locator("#dd-portal .cb-menu").count() == 0, "Esc did not close combobox")
        require(page.locator("#drawerEl").is_visible(), "Esc incorrectly closed drawer before combobox")
    case("TC-18", "Master combobox empty state and Esc chain", combo_empty_esc)

    code = f"E2E-R{round_no}"

    def valid_create_loading() -> None:
        page.locator("#fld-code input").fill(code)
        page.locator("#fld-name input").fill(f"E2E Route {round_no}")
        page.locator("#universeInput").fill("37")
        require(page.locator("#universeInput").input_value() == "37", "create universe input rejected typing")
        page.locator("#cbi-rep").click()
        page.locator("#dd-portal .cb-item").first.click()
        page.locator("#btn-save").click()
        require(page.locator("#btn-save").is_disabled(), "save button not disabled during submit")
        require("กำลังบันทึก" in page.locator("#btn-save").inner_text(), "loading copy missing")
        page.wait_for_timeout(600)
        require(page.locator("tbody tr").filter(has_text=code).count() == 1, "created route not in table")
    case("TC-19", "Valid create, loading/disabled state, created row", valid_create_loading)

    def edit_locked_save() -> None:
        page.locator("tbody tr").filter(has_text=code).click()
        page.locator("#drawerEl .drawer-hactions .btn-secondary").click()
        require(page.locator("#fld-code input").is_disabled(), "Route code is editable in edit mode")
        page.locator("#fld-name input").fill(f"E2E Updated {round_no}")
        page.locator("#universeInput").fill("41")
        require(page.locator("#universeInput").input_value() == "41", "edit universe input rejected typing")
        page.locator("#btn-save").click()
        require(page.locator("#btn-save").is_disabled(), "edit save not disabled during submit")
        page.wait_for_timeout(600)
        require(page.locator("#drawerEl").inner_text().find(f"E2E Updated {round_no}") >= 0, "updated name not shown in view")
        page.keyboard.press("Escape")
    case("TC-20", "Edit flow keeps code locked and saves updated detail", edit_locked_save)

    def drawer_backdrop() -> None:
        page.locator("tbody tr").filter(has_text=code).click()
        page.locator("#drawerBackdrop").click(position={"x": 8, "y": 8})
        wait_render()
        require("is-open" not in (page.locator("#drawerEl").get_attribute("class") or ""), "drawer backdrop did not close")
    case("TC-21", "Drawer closes from backdrop", drawer_backdrop)

    def open_archive() -> None:
        page.locator("tbody tr").filter(has_text=code).click()
        page.locator("#drawerEl .drawer-hactions .btn-danger").click()
        wait_render()
        require(page.locator("#modalCard").is_visible(), "archive confirm modal missing")

    def modal_esc() -> None:
        open_archive()
        page.keyboard.press("Escape")
        wait_render()
        require(not page.locator("#modalCard").is_visible(), "Esc did not close modal")
        require(page.locator("#drawerEl").is_visible(), "Esc closed drawer before modal")
    case("TC-22", "Destructive modal opens and Esc closes it first", modal_esc)
    shot("08-after-modal-esc")

    def modal_backdrop() -> None:
        page.locator("#drawerEl .drawer-hactions .btn-danger").click()
        page.locator("#modalBackdrop").click(position={"x": 8, "y": 8})
        wait_render()
        require(not page.locator("#modalCard").is_visible(), "modal backdrop did not close")
        require(page.locator("#drawerEl").is_visible(), "modal backdrop closed drawer")
    case("TC-23", "Modal closes from backdrop without closing drawer", modal_backdrop)

    def archive_restore() -> None:
        page.locator("#drawerEl .drawer-hactions .btn-danger").click()
        shot("09-archive-modal")
        page.locator("#modalCard .btn-danger").click()
        require(page.locator("#modalCard .btn-danger").is_disabled(), "archive action not disabled during submit")
        require("กำลังบันทึก" in page.locator("#modalCard .btn-danger").inner_text(), "archive loading copy missing")
        page.wait_for_timeout(600)
        page.keyboard.press("Escape")
        page.locator(".filter-bar select").select_option("archived")
        wait_render()
        require(page.locator("tbody tr").filter(has_text=code).count() == 1, "archived route not visible in archived filter")
        page.locator("tbody tr").filter(has_text=code).locator('[title="กู้คืน"]').click()
        wait_render()
        require(page.locator("tbody tr").filter(has_text=code).count() == 0, "restored route remained in archived filter")
        page.locator(".filter-bar select").select_option("active")
        wait_render()
        require(page.locator("tbody tr").filter(has_text=code).count() == 1, "restored route missing from active filter")
    case("TC-24", "Archive loading, archived filter and restore lifecycle", archive_restore)

    def geometry() -> None:
        require(page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), "page has horizontal overflow")
        require(page.locator(".main").bounding_box() is not None, "main content has no geometry")
        page.locator("tbody tr").filter(has_text=code).click()
        footer = page.locator("#drawerEl .drawer-footer").bounding_box()
        require(footer is not None and footer["y"] + footer["height"] <= height + 1, "drawer footer is outside viewport")
        page.keyboard.press("Escape")
    case("TC-25", f"Responsive geometry at {width}x{height}", geometry)

    def final_runtime() -> None:
        require(not page_errors, f"page errors: {page_errors}")
        require(not console_errors, f"console errors: {console_errors}")
    case("TC-26", "Final runtime has no page/console errors", final_runtime)

    def font_stack() -> None:
        stack = page.evaluate("getComputedStyle(document.body).fontFamily")
        require(stack.startswith('"Noto Sans Thai", Satoshi') or stack.startswith("'Noto Sans Thai', 'Satoshi'"), f"source font stack not restored: {stack}")
        links = page.eval_on_selector_all("link[rel=stylesheet]", "els => els.map(e => e.href)")
        require(any("fonts.googleapis.com/css2?family=Noto+Sans+Thai" in x for x in links), "source Noto Sans Thai import missing")
        require(any("api.fontshare.com/v2/css?f[]=satoshi" in x for x in links), "source Satoshi import missing")
    case("TC-27", "Font imports and declaration match source HTML", font_stack)

    def unspecified_province_not_counted() -> None:
        count = int(page.locator(".stat").nth(1).locator(".stat-value").inner_text())
        require(count == province_count_before, f"blank province changed province stat: {province_count_before} -> {count}")
    case("TC-28", "Create with unspecified province does not increment province stat", unspecified_province_not_counted)

    def map_hover_clears() -> None:
        page.get_by_role("tab").nth(2).click()
        page.evaluate("""() => {
          window.__mapBoundaryCalls={hover:0,tip:0,select:0};
          const hover=window.mapHover, tip=window.updateTip, select=window.mapSelect;
          window.mapHover=(...args)=>{window.__mapBoundaryCalls.hover++;return hover(...args);};
          window.updateTip=(...args)=>{window.__mapBoundaryCalls.tip++;return tip(...args);};
          window.mapSelect=(...args)=>{window.__mapBoundaryCalls.select++;return select(...args);};
        }""")
        frame = page.locator(".map-canvas")
        frame_box = frame.bounding_box()
        pin = page.locator(".th-map g[data-pin]:visible").first
        pin.scroll_into_view_if_needed()
        frame_box = frame.bounding_box()
        pin_box = pin.bounding_box()
        require(frame_box is not None and pin_box is not None, "map frame/pin geometry unavailable")
        inside = (pin_box["x"] + pin_box["width"] / 2, pin_box["y"] + pin_box["height"] / 2)
        page.mouse.move(*inside)
        page.wait_for_timeout(40)
        require(page.evaluate("state.mapHover !== null"), "map hover did not activate")
        x, y, w, h = frame_box["x"], frame_box["y"], frame_box["width"], frame_box["height"]
        clamp_x = lambda value: max(1, min(width - 2, value))
        clamp_y = lambda value: max(1, min(height - 2, value))
        outside = [
            (clamp_x(x - 6), clamp_y(y + h / 2)),
            (clamp_x(x + w + 6), clamp_y(y + h / 2)),
            (clamp_x(x + w / 2), clamp_y(y - 6)),
            (clamp_x(x + w / 2), clamp_y(y + h + 6)),
            (clamp_x(x - 6), clamp_y(y - 6)),
            (clamp_x(x + w + 6), clamp_y(y - 6)),
            (clamp_x(x - 6), clamp_y(y + h + 6)),
            (clamp_x(x + w + 6), clamp_y(y + h + 6)),
        ]
        page.mouse.move(*inside)
        page.wait_for_timeout(35)
        require(page.evaluate("state.mapHover !== null"), "positive inside control failed")
        page.mouse.move(*outside[0])
        page.wait_for_timeout(55)
        require(page.evaluate("state.mapHover === null"), "first outside exit did not clear hover")
        baseline = page.evaluate("""() => ({calls:{...window.__mapBoundaryCalls},hover:state.mapHover,sel:state.mapSel,region:state.mapRegion,tip:getComputedStyle(document.querySelector('#mapTip')).display})""")
        for index, point in enumerate(outside[1:], start=1):
            page.mouse.move(*point)
            page.wait_for_timeout(35)
            current = page.evaluate("""() => ({calls:{...window.__mapBoundaryCalls},hover:state.mapHover,sel:state.mapSel,region:state.mapRegion,tip:getComputedStyle(document.querySelector('#mapTip')).display})""")
            require(current == baseline, f"outside sample {index} caused call/state change: {baseline} -> {current}")
        heat = page.locator(".mp-heat-row").first
        if heat.count():
            heat.hover()
            page.wait_for_timeout(50)
            current = page.evaluate("""() => ({calls:{...window.__mapBoundaryCalls},hover:state.mapHover,sel:state.mapSel,region:state.mapRegion,tip:getComputedStyle(document.querySelector('#mapTip')).display})""")
            require(current == baseline, f"map-side list outside frame caused call/state change: {baseline} -> {current}")
        page.get_by_role("tab").nth(0).click()
    case("TC-29", "Map boundary: positive inside control and negative coordinates on all sides/corners", map_hover_clears)

    def searchable_dropdown_scroll() -> None:
        page.locator(".ph-actions .btn-primary").click()
        for key in ("prov", "rep"):
            field = page.locator(f"#cbi-{key}")
            field.click()
            menu = page.locator("#dd-portal .cb-menu")
            require(menu.evaluate("el => el.scrollHeight > el.clientHeight"), f"{key} menu is not scrollable")
            menu.hover()
            page.mouse.wheel(0, 420)
            page.wait_for_timeout(80)
            require(menu.evaluate("el => el.scrollTop > 0"), f"{key} wheel scroll was reset")
            page.keyboard.press("Escape")
            field.click()
            for _ in range(6):
                page.keyboard.press("ArrowDown")
            visible = page.evaluate("""() => { const m=document.querySelector('#dd-portal .cb-menu'), h=m?.querySelector('.cb-item.is-hi'); if(!m||!h)return false; const a=m.getBoundingClientRect(), b=h.getBoundingClientRect(); return b.top>=a.top && b.bottom<=a.bottom; }""")
            require(visible, f"{key} keyboard highlight is outside scroll viewport")
            page.keyboard.press("Escape")
        page.keyboard.press("Escape")
    case("TC-30", "Every searchable dropdown supports wheel and keyboard scrolling", searchable_dropdown_scroll)

    def universe_contract() -> None:
        page.locator("tbody tr").filter(has_text=code).click()
        page.locator("#drawerEl .drawer-hactions .btn-secondary").click()
        require(page.locator("#universeInput").is_editable(), "edit universe control is not editable")
        require(page.locator("#fld-universe .field-help").inner_text().find("เว้นว่างได้") >= 0, "universe optional/editable affordance missing")
        page.keyboard.press("Escape")
    case("TC-31", "Universe remains editable in edit drawer with explicit optional affordance", universe_contract)

    def central_area_route() -> None:
        page.locator("#qInput").fill("R-BK-01")
        wait_render()
        row = page.locator("tbody tr").filter(has_text="R-BK-01")
        require(row.count() == 1, "central Area Route mock missing from structure list")
        require("กรุงเทพมหานคร" in row.inner_text() and "เอก ทวีสุข" in row.inner_text(), "central mock anchors drifted")
        require(page.locator("tbody .region-row").filter(has_text="ภาคกลาง").count() == 1, "ภาคกลาง group heading missing")
        page.locator("#qInput").fill("")
        wait_render()
    case("TC-32", "Central Area Route mock is visible under ภาคกลาง", central_area_route)

    def structure_document_scroll() -> None:
        metrics = page.evaluate("""() => {
          const pick=s=>getComputedStyle(document.querySelector(s)).overflowY;
          return {doc:document.documentElement.scrollHeight,viewport:innerHeight,body:getComputedStyle(document.body).overflowY,content:pick('.content'),card:pick('.card'),table:pick('.table-wrap')};
        }""")
        require(metrics["doc"] > metrics["viewport"], f"document does not extend beyond viewport: {metrics}")
        require(metrics["body"] in ("auto", "visible"), f"body is not outer scroller: {metrics}")
        for key in ("content", "card", "table"):
            require(metrics[key] not in ("auto", "scroll"), f"nested vertical scroller remains on {key}: {metrics}")
        last = page.locator("tbody tr:not(.region-row)").last
        last.scroll_into_view_if_needed()
        page.wait_for_timeout(80)
        require(page.evaluate("window.scrollY > 0"), "browser/document did not scroll to final row")
        box = last.bounding_box()
        require(box is not None and box["y"] >= 0 and box["y"] + box["height"] <= height + 1, "final row not reachable in browser viewport")
        require(page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), "structure page has horizontal overflow")
        page.evaluate("window.scrollTo(0,0)")
    case("TC-33", "Structure uses document scrollbar and browser reaches final row", structure_document_scroll)
    shot("10-final")

    context.close()
    browser.close()
    passed = sum(1 for item in cases if item["status"] == "PASS")
    return {
        "round": round_no,
        "viewport": f"{width}x{height}",
        "fresh_browser": True,
        "fresh_context": True,
        "passed": passed,
        "failed": len(cases) - passed,
        "cases": cases,
        "console_errors": console_errors,
        "font_resource_errors": font_resource_errors,
        "page_errors": page_errors,
        "screenshots": sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in shot_dir.glob("*.png")),
    }


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        rounds = [
            run_round(playwright.chromium, 1, 1440, 900),
            run_round(playwright.chromium, 2, 1024, 768),
        ]
    payload = {
        "html": str(HTML.relative_to(WORKSPACE)).replace("\\", "/"),
        "rounds": rounds,
        "passed": sum(r["passed"] for r in rounds),
        "failed": sum(r["failed"] for r in rounds),
    }
    RESULTS.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 1 if payload["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
