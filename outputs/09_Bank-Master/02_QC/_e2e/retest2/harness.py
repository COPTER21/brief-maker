import os, sys, json, traceback
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(r"C:/Users/Admin/Desktop/Work/brief-maker/outputs/09_Bank-Master")
HTML = BASE / "01_HTML" / "BankMaster.html"
OUT  = BASE / "02_QC" / "_e2e" / "retest2"
OUT.mkdir(parents=True, exist_ok=True)
PROG = BASE / "02_QC" / "_retest2_progress.txt"
RESULTS = OUT / "results.json"

results = []
progress_lines = []

def log(msg):
    print(msg, flush=True)
    progress_lines.append(msg)
    PROG.write_text("\n".join(progress_lines), encoding="utf-8")

def rec(name, status, detail=""):
    results.append({"check": name, "status": status, "detail": detail})
    RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"[{status}] {name} :: {detail}")

console_errors = []
page_errors = []

with sync_playwright() as p:
    exe = r"C:/Users/Admin/Desktop/Work/brief-maker/.tools/ms-playwright/chromium-1228/chrome-win64/chrome.exe"
    browser = p.chromium.launch(executable_path=exe)
    page = browser.new_page()
    page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: page_errors.append(str(e)))
    page.goto(HTML.as_uri())
    page.wait_for_timeout(600)
    log("PAGE LOADED")

    def zidx(sel):
        return page.evaluate("""(s)=>{const e=document.querySelector(s);return e?getComputedStyle(e).zIndex:null;}""", sel)

    # ---------- PRIORITY 1: Deactivate from drawer (Bug C) ----------
    try:
        # Round 1: open active account BA-003 view drawer
        page.evaluate("openView('BA-003')")
        page.wait_for_timeout(500)
        drawer_open = page.evaluate("document.getElementById('drawer').classList.contains('is-open')")
        # click header ปิดใช้งาน button inside drawer
        page.locator("#drawer button:has-text('ปิดใช้งาน')").first.click()
        page.wait_for_timeout(500)
        modal_open = page.evaluate("document.getElementById('modalBackdrop').classList.contains('is-open')")
        z_modal = zidx(".modal-backdrop")
        z_drawer = zidx(".drawer")
        # elementFromPoint at confirm button center
        hit = page.evaluate("""()=>{
            const btns=[...document.querySelectorAll('.modal-footer .btn-danger')];
            const b=btns[btns.length-1]; const r=b.getBoundingClientRect();
            const el=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
            return {inModal: !!el.closest('.modal'), inDrawerBody: !!el.closest('.drawer-body'), tag: el.tagName};
        }""")
        above = int(z_modal) > int(z_drawer)
        rec("BugC-Deactivate-R1-modal-above-drawer",
            "PASS" if (drawer_open and modal_open and above and hit['inModal'] and not hit['inDrawerBody']) else "FAIL",
            f"drawer_open={drawer_open} modal_open={modal_open} z_modal={z_modal} z_drawer={z_drawer} above={above} hit={hit}")
        # screenshot proof (modal over drawer)
        page.screenshot(path=str(OUT / "modal-over-drawer.png"))
        log("screenshot modal-over-drawer.png written")
        # click confirm
        page.locator(".modal-footer .btn-danger").last.click()
        page.wait_for_timeout(500)
        new_status = page.evaluate("accounts.find(a=>a.id==='BA-003').status")
        rec("BugC-Deactivate-R1-confirm-sets-inactive",
            "PASS" if new_status == "inactive" else "FAIL", f"BA-003 status={new_status}")
    except Exception as e:
        rec("BugC-Deactivate-R1", "ERROR", repr(e) + " | " + traceback.format_exc().splitlines()[-1])

    # Round 2: Cancel path on another active account (BA-001)
    try:
        page.evaluate("closeDrawer(); closeModal();"); page.wait_for_timeout(300)
        page.evaluate("openView('BA-001')"); page.wait_for_timeout(400)
        page.locator("#drawer button:has-text('ปิดใช้งาน')").first.click(); page.wait_for_timeout(400)
        # click ยกเลิก (cancel/ghost)
        page.locator(".modal-footer .btn-ghost").last.click(); page.wait_for_timeout(400)
        modal_open = page.evaluate("document.getElementById('modalBackdrop').classList.contains('is-open')")
        status_after = page.evaluate("accounts.find(a=>a.id==='BA-001').status")
        rec("BugC-Deactivate-R2-cancel-path",
            "PASS" if (not modal_open and status_after == "active") else "FAIL",
            f"modal_open_after_cancel={modal_open} BA-001 status={status_after}")
    except Exception as e:
        rec("BugC-Deactivate-R2-cancel", "ERROR", repr(e))

    # ---------- PRIORITY 2: Archive from drawer (Bug C / FN-06) ----------
    try:
        page.evaluate("closeDrawer(); closeModal();"); page.wait_for_timeout(300)
        page.evaluate("openView('BA-002')"); page.wait_for_timeout(400)  # active account
        page.locator("#drawer button:has-text('เก็บถาวร')").first.click(); page.wait_for_timeout(500)
        modal_open = page.evaluate("document.getElementById('modalBackdrop').classList.contains('is-open')")
        z_modal = zidx(".modal-backdrop"); z_drawer = zidx(".drawer")
        hit = page.evaluate("""()=>{
            const b=[...document.querySelectorAll('.modal-footer .btn-danger')].pop();
            const r=b.getBoundingClientRect();
            const el=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
            return {inModal: !!el.closest('.modal'), inDrawerBody: !!el.closest('.drawer-body')};
        }""")
        above = int(z_modal) > int(z_drawer)
        rec("BugC-Archive-modal-above-drawer",
            "PASS" if (modal_open and above and hit['inModal'] and not hit['inDrawerBody']) else "FAIL",
            f"modal_open={modal_open} z_modal={z_modal} z_drawer={z_drawer} above={above} hit={hit}")
        page.locator(".modal-footer .btn-danger").last.click(); page.wait_for_timeout(500)
        st = page.evaluate("accounts.find(a=>a.id==='BA-002').status")
        rec("BugC-Archive-confirm-sets-archived", "PASS" if st == "archived" else "FAIL", f"BA-002 status={st}")
    except Exception as e:
        rec("BugC-Archive", "ERROR", repr(e))

    # ---------- SMOKE: Bug A still holds (default tab keeps drawer on-screen) ----------
    try:
        page.evaluate("closeDrawer(); closeModal();"); page.wait_for_timeout(300)
        page.evaluate("openView('BA-001')"); page.wait_for_timeout(400)
        page.locator("#drawer .drawer-tab:has-text('ค่าเริ่มต้น')").click(); page.wait_for_timeout(400)
        onscreen = page.evaluate("""()=>{const d=document.getElementById('drawer');
            const r=d.getBoundingClientRect(); return {open:d.classList.contains('is-open'), right:r.right, left:r.left, vw:window.innerWidth};}""")
        # drawer visible if left < viewport width (not translated off-screen)
        visible = onscreen['open'] and onscreen['left'] < onscreen['vw']
        rec("Smoke-BugA-drawer-stays-on-defaulttab", "PASS" if visible else "FAIL", f"{onscreen}")
    except Exception as e:
        rec("Smoke-BugA", "ERROR", repr(e))

    # ---------- SMOKE: Doc picker opens/closes (uses same modal-backdrop) ----------
    try:
        page.evaluate("closeDrawer(); closeModal();"); page.wait_for_timeout(300)
        page.evaluate("openDocPicker()"); page.wait_for_timeout(400)
        dp_open = page.evaluate("document.getElementById('modalBackdrop').classList.contains('is-open')")
        z_modal = zidx(".modal-backdrop")
        page.evaluate("closeModal()"); page.wait_for_timeout(400)
        dp_closed = not page.evaluate("document.getElementById('modalBackdrop').classList.contains('is-open')")
        rec("Smoke-DocPicker-open-close", "PASS" if (dp_open and dp_closed) else "FAIL",
            f"opened={dp_open} z_modal={z_modal} closed={dp_closed}")
    except Exception as e:
        rec("Smoke-DocPicker", "ERROR", repr(e))

    # ---------- SMOKE: mask/reveal ----------
    try:
        page.evaluate("closeDrawer(); closeModal();"); page.wait_for_timeout(300)
        page.evaluate("revealAccNo('BA-003')"); page.wait_for_timeout(300)
        revealed = page.evaluate("state.revealed.has('BA-003')")
        page.evaluate("hideAccNo('BA-003')"); page.wait_for_timeout(200)
        hidden = not page.evaluate("state.revealed.has('BA-003')")
        rec("Smoke-mask-reveal", "PASS" if (revealed and hidden) else "FAIL", f"revealed={revealed} hidden={hidden}")
    except Exception as e:
        rec("Smoke-mask-reveal", "ERROR", repr(e))

    # ---------- SMOKE: Esc chain (modal then drawer) ----------
    try:
        page.evaluate("closeDrawer(); closeModal();"); page.wait_for_timeout(300)
        page.evaluate("openView('BA-001')"); page.wait_for_timeout(300)
        page.evaluate("openDeactivate('BA-001')"); page.wait_for_timeout(300)
        page.keyboard.press("Escape"); page.wait_for_timeout(400)
        modal_after = page.evaluate("document.getElementById('modalBackdrop').classList.contains('is-open')")
        drawer_after1 = page.evaluate("document.getElementById('drawer').classList.contains('is-open')")
        page.keyboard.press("Escape"); page.wait_for_timeout(400)
        drawer_after2 = page.evaluate("document.getElementById('drawer').classList.contains('is-open')")
        # Esc1 should close modal but keep drawer; Esc2 closes drawer
        ok = (not modal_after) and drawer_after1 and (not drawer_after2)
        rec("Smoke-Esc-chain", "PASS" if ok else "WARN",
            f"esc1: modal_open={modal_after} drawer_open={drawer_after1}; esc2: drawer_open={drawer_after2}")
    except Exception as e:
        rec("Smoke-Esc-chain", "ERROR", repr(e))

    # ---------- SMOKE: W1 delete guard (used>0 disabled / used=0 deletes) ----------
    try:
        page.evaluate("closeDrawer(); closeModal();"); page.wait_for_timeout(300)
        # inspect archive modal note behavior via usedInDoc. Use edit/delete path if exists.
        # BA-001 usedInDoc true -> cannot hard delete; BA-003 usedInDoc false (but we deactivated it, still usedInDoc false)
        has_delete = page.evaluate("typeof openDelete === 'function' || typeof confirmDelete === 'function'")
        rec("Smoke-W1-delete-guard-fn-present", "INFO", f"delete fn present={has_delete}")
    except Exception as e:
        rec("Smoke-W1-delete-guard", "ERROR", repr(e))

    # ---------- SMOKE: create account (I-06a) ----------
    try:
        page.evaluate("closeDrawer(); closeModal();"); page.wait_for_timeout(300)
        before = page.evaluate("accounts.filter(a=>a.company===state.currentCompany).length")
        # open create drawer
        opened = page.evaluate("typeof openCreate === 'function'")
        if opened:
            page.evaluate("openCreate()"); page.wait_for_timeout(400)
            create_drawer_open = page.evaluate("document.getElementById('drawer').classList.contains('is-open')")
            rec("Smoke-CreateAccount-drawer-opens", "PASS" if create_drawer_open else "FAIL", f"before_count={before}")
        else:
            rec("Smoke-CreateAccount", "WARN", "openCreate fn not found")
    except Exception as e:
        rec("Smoke-CreateAccount", "ERROR", repr(e))

    # ---------- console/page error tally ----------
    app_console = [e for e in console_errors if "fontshare" not in e.lower()]
    rec("Console-errors", "PASS" if len(app_console)==0 else "FAIL",
        f"app_console_errors={len(app_console)} (raw_console={len(console_errors)}) sample={app_console[:3]}")
    rec("Page-errors", "PASS" if len(page_errors)==0 else "FAIL",
        f"page_errors={len(page_errors)} sample={page_errors[:3]}")

    browser.close()

log("HARNESS DONE")
print(json.dumps(results, ensure_ascii=False))
