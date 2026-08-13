from pathlib import Path
from playwright.sync_api import sync_playwright

WORKSPACE = Path(__file__).resolve().parents[2]
HTML = WORKSPACE / "outputs" / "05_Sales_Territory" / "sales-territory.html"


def require(value, message):
    if not value:
        raise AssertionError(message)


def run(browser_type, width, height):
    browser = browser_type.launch(headless=True)
    context = browser.new_context(viewport={"width": width, "height": height})
    page = context.new_page()
    page.goto(HTML.as_uri(), wait_until="load")
    stack = page.evaluate("getComputedStyle(document.body).fontFamily")
    require("Noto Sans Thai" in stack and "Satoshi" in stack, f"source font stack missing: {stack}")
    links = page.eval_on_selector_all("link[rel=stylesheet]", "els => els.map(e => e.href)")
    require(any("fonts.googleapis.com/css2?family=Noto+Sans+Thai" in x for x in links), "Noto import missing")
    require(any("api.fontshare.com/v2/css?f[]=satoshi" in x for x in links), "Satoshi import missing")

    page.get_by_role("tab").nth(2).click()
    page.evaluate("""() => {
      window.__mapBoundaryCalls={hover:0,tip:0,select:0};
      const hover=window.mapHover, tip=window.updateTip, select=window.mapSelect;
      window.mapHover=(...args)=>{window.__mapBoundaryCalls.hover++;return hover(...args);};
      window.updateTip=(...args)=>{window.__mapBoundaryCalls.tip++;return tip(...args);};
      window.mapSelect=(...args)=>{window.__mapBoundaryCalls.select++;return select(...args);};
    }""")
    frame = page.locator(".map-canvas")
    pin = page.locator(".th-map g[data-pin]:visible").first
    pin.scroll_into_view_if_needed()
    frame_box, pin_box = frame.bounding_box(), pin.bounding_box()
    require(frame_box and pin_box, "map geometry missing")
    inside = (pin_box["x"] + pin_box["width"] / 2, pin_box["y"] + pin_box["height"] / 2)
    x, y, w, h = frame_box["x"], frame_box["y"], frame_box["width"], frame_box["height"]
    cx = lambda n: max(1, min(width - 2, n))
    cy = lambda n: max(1, min(height - 2, n))
    outside = [
        (cx(x - 6), cy(y + h / 2)), (cx(x + w + 6), cy(y + h / 2)),
        (cx(x + w / 2), cy(y - 6)), (cx(x + w / 2), cy(y + h + 6)),
        (cx(x - 6), cy(y - 6)), (cx(x + w + 6), cy(y - 6)),
        (cx(x - 6), cy(y + h + 6)), (cx(x + w + 6), cy(y + h + 6)),
    ]
    page.mouse.move(*inside)
    page.wait_for_timeout(35)
    require(page.evaluate("state.mapHover !== null"), "inside positive control failed")
    page.mouse.move(*outside[0])
    page.wait_for_timeout(55)
    require(page.evaluate("state.mapHover === null"), "first outside exit did not clear hover")
    baseline = page.evaluate("""() => ({calls:{...window.__mapBoundaryCalls},hover:state.mapHover,sel:state.mapSel,region:state.mapRegion,tip:getComputedStyle(document.querySelector('#mapTip')).display})""")
    for index, point in enumerate(outside[1:], start=1):
        page.mouse.move(*point)
        page.wait_for_timeout(35)
        current = page.evaluate("""() => ({calls:{...window.__mapBoundaryCalls},hover:state.mapHover,sel:state.mapSel,region:state.mapRegion,tip:getComputedStyle(document.querySelector('#mapTip')).display})""")
        require(current == baseline, f"outside coordinate caused call/state change {index}: {point}; {baseline} -> {current}")
    page.locator(".mp-heat-row").first.hover()
    page.wait_for_timeout(55)
    current = page.evaluate("""() => ({calls:{...window.__mapBoundaryCalls},hover:state.mapHover,sel:state.mapSel,region:state.mapRegion,tip:getComputedStyle(document.querySelector('#mapTip')).display})""")
    require(current == baseline, f"outside map-side row caused call/state change: {baseline} -> {current}")
    context.close()
    browser.close()
    print(f"FOCUSED PASS {width}x{height}: font source match + map inside/outside 8 coordinates + side panel")


with sync_playwright() as playwright:
    run(playwright.chromium, 1440, 900)
    run(playwright.chromium, 1024, 768)
