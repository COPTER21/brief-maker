#!/usr/bin/env python3
"""E2E · F-HR-ESS (ESS Portal / พนักงานทำเอง) — WF-01 Step 5

รันไทม์ตัวเดียวที่ครอบทุก FN (15 = FN-01..11 + FN-90/92/93/94) + เคสเชิงลบ N1–N4
(ไม่มี FN-40 → พิสูจน์ "display-only LOCK" ตอนรันไทม์: เรนเดอร์ DOM จริงแล้ว assert ว่า
"ไม่มี" affordance ที่เขียน/ยื่น/บันทึกข้อมูล ESS · ทุกปุ่ม "ยื่นคำขอ" = navigate-out เท่านั้น).

ยึด helper ของ uikit เท่านั้น (ready/settle/after/hush) — ไม่มี wait_for_timeout, ไม่มีตัวตรวจ UI ใหม่.
ขับหน้าจอผ่าน controller function จริง + real click (qcard/ap-row/reveal) แล้ว assert ทั้ง
data model, ข้อความที่เรนเดอร์บน DOM และพฤติกรรม (navigate-out/toast/modal/มาส์ก).
reload หน้าใหม่ต่อเคส → mock state reset = เคสอิสระต่อกัน.

รัน: .claude/venv/Scripts/python.exe outputs/F-HR-ESS/_e2e/e2e-ess.py [path/to/ess.html]
"""
from pathlib import Path
import re
import sys

from playwright.sync_api import sync_playwright

OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import (  # noqa: E402
    Suite, ready, settle as shared_settle, after as shared_after, hush,
    assert_no_garbage_text, assert_text_absent, assert_overlay_cleared_after_close,
    assert_affordances_fire,
    JS_AFFORDANCE, JS_CSSVAR, JS_MODAL_UNDER_DRAWER, JS_OVERLAY_STACK,
)

HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "ess.html").resolve()
BASE = HTML.as_uri()

suite = Suite("F-HR-ESS · ESS Portal")


def settle(page, timeout=1600):
    shared_settle(page, timeout=timeout)


def after(page, js, timeout=1800):
    return shared_after(page, js, timeout=timeout)


def open_(page):
    """เปิดหน้าใหม่ (reset state) แล้วรอ render จริง (#appContent มีเนื้อหา)"""
    ready(page, BASE, timeout=9000)
    page.wait_for_function(
        "() => { const p=document.getElementById('appContent'); return p && p.innerHTML.trim().length>0; }",
        timeout=9000,
    )


def ev(page, js):
    return page.evaluate(js)


def app_text(page):
    return page.evaluate("() => document.getElementById('appContent').textContent")


def drawer_text(page):
    return page.evaluate("() => (document.getElementById('drawer')||{}).textContent || ''")


def modal_text(page):
    return page.evaluate("() => (document.querySelector('#modalBackdrop .modal')||{}).textContent || ''")


def toast_text(page):
    return page.evaluate("() => (document.getElementById('toast')||{}).textContent || ''")


def go_tab(page, t):
    after(page, "() => goTab('%s')" % t)


# ═══════════════════════════════ FN CASES ═══════════════════════════════

def c_fn01(page):
    """[FN-01] หน้าหลัก: การ์ดอ่าน 5 ใบ (สลิป/โควตาลา/OT/ใบเบิกค้าง/แจ้งเตือน) + launcher band

    การ์ดต้องคลิกได้จริง (real click) → นำทาง (openView/goTab). พิสูจน์ dashboard ทำงานจริง.
    """
    open_(page)
    assert ev(page, "() => state.tab") == "home", "ค่าเริ่มต้นไม่ใช่แท็บหน้าหลัก"
    n_cards = ev(page, "() => document.querySelectorAll('#appContent .qcard').length")
    assert n_cards == 5, f"หน้าหลักต้องมีการ์ดอ่าน 5 ใบ (ได้ {n_cards})"
    at = app_text(page)
    for label in ["สลิปล่าสุด", "โควตาลาคงเหลือ", "OT เดือนนี้", "ใบเบิกค้าง", "แจ้งเตือน"]:
        assert label in at, f"การ์ดหน้าหลักขาด: {label}"
    assert ev(page, "() => document.querySelectorAll('#appContent .launcher').length") == 1, \
        "ไม่มี launcher band ('ต้องการยื่นคำขอใช่ไหม?')"
    assert "ต้องการยื่นคำขอ" in at, "launcher ไม่มีข้อความชวนยื่นคำขอ"
    # การ์ด 'โควตาลาคงเหลือ' คลิกจริง → goTab('pay')
    page.locator("#appContent .qcard").nth(1).click()
    page.wait_for_function("() => state.tab==='pay'", timeout=4000)
    assert ev(page, "() => state.tab") == "pay", "คลิกการ์ดโควตาลาแล้วไม่พาไปแท็บเงินเดือน&เวลา"
    # การ์ด 'สลิปล่าสุด' คลิกจริง → เปิด drawer payslip
    open_(page)
    page.locator("#appContent .qcard").first.click()
    page.wait_for_function("() => state.drawer.open===true", timeout=4000)
    assert ev(page, "() => state.drawer.mode") == "payslip", "คลิกการ์ดสลิปล่าสุดไม่เปิดสลิป"
    return f"หน้าหลัก 5 การ์ด + launcher · การ์ดคลิกจริงนำทางได้ (โควตา→pay · สลิป→drawer)"


def c_fn02(page):
    """[FN-02] อ่านสลิป (Payroll PS-1 · ของตนเอง · all-or-nothing) + แท็บย่อย YTD"""
    open_(page)
    go_tab(page, "pay")
    at = app_text(page)
    assert "PS-2568-07" in at and "สลิปเงินเดือน" in at, "แท็บ pay ไม่แสดงสลิป"
    # FIX-04: ป้าย dev '(PS-1)' ย้ายไป comment แล้ว — sub ที่ผู้ใช้เห็น = 'เฉพาะของตนเอง'
    assert "เฉพาะของตนเอง" in at, "ไม่ระบุขอบเขต self ของสลิป"
    after(page, "() => openView('payslip','PS-2568-07')")
    dt = drawer_text(page)
    assert "สลิปเงินเดือน" in dt and "ยอดสุทธิ" in dt, "drawer สลิปไม่มีรายละเอียด"
    assert "all-or-nothing" in dt or "all-or-nothing".upper() in dt.upper() or "เฉพาะสลิปของตนเอง" in dt, \
        "ไม่มีหมายเหตุ all-or-nothing / เฉพาะของตนเอง"
    # แท็บย่อย YTD
    assert ev(page, "() => document.querySelectorAll('#drawer .drawer-tab').length") == 2, "ไม่มีแท็บย่อยสลิป/YTD"
    after(page, "() => { state.drawer.sub=1; render(); }")
    dt2 = drawer_text(page)
    assert "สะสมทั้งปี" in dt2 and "รายได้สะสม" in dt2, "แท็บย่อย YTD ไม่แสดงยอดสะสม"
    return "สลิป PS-1 (self · all-or-nothing) + แท็บย่อย YTD (รายได้สะสม)"


def c_fn03(page):
    """[FN-03] อ่านการลา + 'ยื่นลา' = deep-link (navigate-out · ไม่มีฟอร์มในพอร์ทัล)"""
    open_(page)
    go_tab(page, "pay")
    at = app_text(page)
    assert "วันลา & โควตา" in at and "ลาพักร้อน" in at, "ไม่แสดงโควตา/ประวัติการลา"
    assert "LV-2568-014" in at, "ไม่แสดงประวัติการลา"
    # ยื่นลา = deep-link → toast + navigate-out (ไม่มีฟอร์ม)
    n_before = ev(page, "() => document.querySelectorAll('#drawer input, #modalBackdrop input, #appContent form').length")
    after(page, "() => deepLink('leave')")
    tt = toast_text(page)
    # FIX-04: toast = navigation ภาษาผู้ใช้ (ตัด '[ASSUMED contract]'+route ออกจากข้อความ · route อยู่ที่ LINKS/comment)
    assert "กำลังนำทาง" in tt and "การลา" in tt, f"ยื่นลาไม่ใช่ navigate-out (toast: '{tt}')"
    # ยืนยัน route ยัง wire อยู่จริงที่ LINKS (พิสูจน์ deep-link มีปลายทาง แม้ไม่โชว์ใน toast)
    assert ev(page, "() => LINKS.leave.route") == "#/leave/new", "LINKS.leave.route ไม่ใช่ #/leave/new"
    assert n_before == 0, "ยื่นลาเปิดฟอร์มในพอร์ทัล (ควร navigate-out เท่านั้น)"
    return "การลา: อ่านโควตา/ประวัติ · 'ยื่นลา'=deep-link toast(นำทาง) · route #/leave/new (LINKS) · ไม่มีฟอร์ม"


def c_fn04(page):
    """[FN-04] อ่าน OT / เวลา / สแกน (read-only)"""
    open_(page)
    go_tab(page, "pay")
    at = app_text(page)
    assert "OT & เวลาทำงาน" in at, "ไม่มีส่วน OT/เวลา"
    assert "12 ชั่วโมง" in at and "อนุมัติ 8" in at, "ไม่แสดงสรุป OT (รวม/อนุมัติ/รอ)"
    # ตารางสแกนเข้า-ออก
    for v in ["08:52", "18:10", "OT 2 ชม.", "เข้าสาย 5 นาที"]:
        assert v in at, f"ตารางสแกนขาดข้อมูล: {v}"
    return "OT/เวลา: สรุป OT (12 ชม.·อนุมัติ 8) + ตารางสแกนเข้า-ออก 3 แถว"


def c_fn05(page):
    """[FN-05] อ่านใบเบิก + 'ยื่นเบิก' = deep-link (navigate-out) + drawer อ่านใบเบิก"""
    open_(page)
    go_tab(page, "docs")
    at = app_text(page)
    assert "ใบเบิกค่าใช้จ่าย" in at and "EX-2568-031" in at, "ไม่แสดงใบเบิก"
    after(page, "() => deepLink('expense')")
    tt = toast_text(page)
    assert "กำลังนำทาง" in tt and "เบิกค่าใช้จ่าย" in tt, f"ยื่นเบิกไม่ใช่ navigate-out (toast: '{tt}')"
    assert ev(page, "() => LINKS.expense.route") == "#/expense/new", "LINKS.expense.route ไม่ใช่ #/expense/new"
    # เปิดดูใบเบิก (อ่านอย่างเดียว)
    open_(page)
    after(page, "() => openView('expense','EX-2568-031')")
    dt = drawer_text(page)
    assert "ค่าเดินทางพบลูกค้า" in dt and "อ่านอย่างเดียว" in dt, "drawer ใบเบิกไม่อ่านอย่างเดียว"
    return "ใบเบิก: อ่าน list + drawer · 'ยื่นเบิก'=deep-link toast(#/expense/new)"


def c_fn06(page):
    """[FN-06] อ่านหนังสือรับรอง (drawer)"""
    open_(page)
    go_tab(page, "docs")
    assert "หนังสือรับรอง / เอกสาร" in app_text(page), "ไม่มีส่วนหนังสือรับรอง"
    after(page, "() => openView('cert','CERT-2568-004')")
    dt = drawer_text(page)
    assert "หนังสือรับรองการทำงาน" in dt and "ฝ่ายบุคคล" in dt, "drawer cert ไม่แสดงรายละเอียด"
    assert "อ่านอย่างเดียว" in dt, "drawer cert ไม่ระบุอ่านอย่างเดียว"
    return "หนังสือรับรอง: drawer อ่านรายละเอียด (ผู้ออก ฝ่ายบุคคล · read-only)"


def c_fn07(page):
    """[FN-07] อ่านสวัสดิการ + ประวัติอบรม"""
    open_(page)
    go_tab(page, "docs")
    at = app_text(page)
    assert "สวัสดิการ & อบรม" in at, "ไม่มีส่วนสวัสดิการ/อบรม"
    assert "ค่ารักษาพยาบาล (OPD)" in at and "ประกันสุขภาพกลุ่ม" in at, "ไม่แสดงสวัสดิการคงเหลือ"
    assert "อบรมความปลอดภัยข้อมูล" in at and "มีใบรับรอง" in at, "ไม่แสดงประวัติอบรม"
    after(page, "() => openView('training','TR-2568-012')")
    assert "หลักสูตร" in drawer_text(page), "drawer อบรมไม่เปิด"
    return "สวัสดิการ (OPD/ประกัน/กองทุน) + ประวัติอบรม + drawer อบรม"


def c_fn08(page):
    """[FN-08] อ่านโปรไฟล์ + 'แก้ข้อมูล' = deep-link/ขออนุมัติ (navigate-out · ไม่แก้ในพอร์ทัล)"""
    open_(page)
    go_tab(page, "docs")
    at = app_text(page)
    assert "ข้อมูลส่วนตัว / โปรไฟล์" in at, "ไม่มีส่วนโปรไฟล์"
    assert "แก้ไขข้อมูลเองไม่ได้" in at, "ไม่ระบุว่าแก้ในพอร์ทัลไม่ได้"
    # ดูโปรไฟล์ (drawer อ่านอย่างเดียว)
    after(page, "() => openView('profile','EMP-00123')")
    dt = drawer_text(page)
    assert "สมชาย ใจดี" in dt and "อ่านอย่างเดียว" in dt, "drawer โปรไฟล์ไม่อ่านอย่างเดียว"
    # 'ขอแก้ข้อมูล' = deep-link ขออนุมัติ (navigate-out)
    open_(page)
    go_tab(page, "docs")
    after(page, "() => deepLink('profile')")
    tt = toast_text(page)
    assert "กำลังนำทาง" in tt and "แก้ไขข้อมูลพนักงาน" in tt, \
        f"ขอแก้ข้อมูลไม่ใช่ deep-link ขออนุมัติ (toast: '{tt}')"
    assert ev(page, "() => LINKS.profile.route") == "#/profile/edit-request", "LINKS.profile.route ไม่ใช่ #/profile/edit-request"
    return "โปรไฟล์: drawer อ่าน · 'ขอแก้ข้อมูล'=deep-link ขออนุมัติ · route #/profile/edit-request (LINKS)"


def c_fn09(page):
    """[FN-09] feed แจ้งเตือนของฉัน (จาก ENG-NOTIFY) + จุดยังไม่อ่าน + เปิดอ่าน"""
    open_(page)
    go_tab(page, "notify")
    n_rows = ev(page, "() => document.querySelectorAll('#appContent .nrow').length")
    assert n_rows == 4, f"feed แจ้งเตือนควรมี 4 รายการ (ได้ {n_rows})"
    unread = ev(page, "() => document.querySelectorAll('#appContent .nrow.unread').length")
    assert unread == 2, f"ควรมีแจ้งเตือนยังไม่อ่าน 2 (ได้ {unread})"
    at = app_text(page)
    assert "สลิปเงินเดือนเดือนกรกฎาคมออกแล้ว" in at, "ไม่แสดงหัวข้อแจ้งเตือน"
    after(page, "() => openView('notif','N-104')")
    assert "ดูสลิป PS-2568-07" in drawer_text(page), "เปิดอ่านแจ้งเตือนไม่ได้"
    return "แจ้งเตือน: feed 4 รายการ (unread 2) + เปิดอ่านรายการได้"


def c_fn10(page):
    """[FN-10] self-access guard → modal 403 (trigger จาก demo-strip) · ไม่แสดงข้อมูลพนักงานอื่น"""
    open_(page)
    # ปุ่มทดสอบเข้าถึงพนักงานอื่นอยู่ใน demo-strip
    assert ev(page, "() => !!document.querySelector('.demo-strip button')"), "ไม่มีปุ่มทดสอบใน demo-strip"
    after(page, "() => openModal('accessDenied')")
    mt = modal_text(page)
    assert "403" in mt, "modal ปฏิเสธไม่แสดงรหัส 403"
    # FIX-04: subtitle เป็นภาษาผู้ใช้ (ตัดศัพท์ 'self-access (SecC)' → comment CSQ ของ FIX-03)
    assert "เข้าถึงถูกปฏิเสธ" in mt and "พนักงานเห็นได้เฉพาะข้อมูลของตนเอง" in mt, "modal ไม่สื่อ self-scope"
    assert "ไม่มีสิทธิ์เข้าถึงข้อมูลของพนักงานคนอื่น" in mt, "modal ไม่บล็อกข้อมูลพนักงานอื่น"
    return "self-access: demo-strip → modal 403 · บล็อกข้อมูลพนักงานอื่น (self-scope)"


def c_fn11(page):
    """[FN-11] soft-ref [ASSUMED contract] chip + deep-link stub (owner feature ยัง ba-done)"""
    open_(page)
    go_tab(page, "pay")
    assert ev(page, "() => document.querySelectorAll('.chip-assumed').length") >= 1, "ไม่มี chip [ASSUMED contract]"
    assert "[ASSUMED contract]" in app_text(page), "chip ไม่มีข้อความ [ASSUMED contract]"
    # chip [ASSUMED contract] ยังอยู่ (มี class demo-only → prod strip · default demo แสดง)
    assert ev(page, "() => document.querySelectorAll('.chip-assumed.demo-only').length") >= 1, \
        "chip [ASSUMED contract] ต้องติด class demo-only (prod strip)"
    # deep-link stub: toast ภาษาผู้ใช้ (route ปลายทางอยู่ที่ LINKS · [ASSUMED] · comment)
    after(page, "() => deepLink('ot')")
    tt = toast_text(page)
    assert "กำลังนำทาง" in tt and "ขอทำงานล่วงเวลา" in tt, f"deep-link stub ไม่นำทาง (toast: '{tt}')"
    assert ev(page, "() => LINKS.ot.route") == "#/ot/new", "LINKS.ot.route ไม่ใช่ #/ot/new"
    return "soft-ref: chip [ASSUMED contract] (demo-only) + deep-link stub (route #/ot/new ที่ LINKS)"


# ═══════════════════════════════ GENERAL FN ═══════════════════════════════

def c_fn90(page):
    """[FN-90] ค้นหา/ตัวกรอง 'ยังไม่อ่าน' ในแจ้งเตือน + empty state"""
    open_(page)
    go_tab(page, "notify")
    # ค้นหาเจอ
    after(page, "() => { state.notif.q='สลิป'; render(); }")
    assert ev(page, "() => document.querySelectorAll('#appContent .nrow').length") == 1, "ค้นหาไม่ลดผลลัพธ์"
    # ค้นหาไม่เจอ → empty state
    after(page, "() => { state.notif.q='zzzไม่มีจริง'; render(); }")
    assert "ไม่พบการแจ้งเตือน" in app_text(page), "ค้นไม่เจอแต่ไม่ขึ้น empty state"
    # ตัวกรองยังไม่อ่าน
    after(page, "() => { state.notif.q=''; state.notif.unread=true; render(); }")
    assert ev(page, "() => document.querySelectorAll('#appContent .nrow').length") == 2, "ตัวกรอง unread ไม่ทำงาน"
    assert ev(page, "() => document.querySelectorAll('#appContent .nrow:not(.unread)').length") == 0, \
        "ตัวกรอง unread ยังโชว์ที่อ่านแล้ว"
    return "แจ้งเตือน: ค้นหา(=1) · empty state · ตัวกรองยังไม่อ่าน(=2 · ไม่มี read)"


def c_fn92(page):
    """[FN-92] responsive: 768px (adaptive floor · Rule #97) และ 1280px ไม่มี horizontal scroll ที่ body

    หมายเหตุ: shell นี้เป็น ERP desktop-base (Rule #97: 768–1180 adaptive · ≥1180 full) มี min-width 768
    ที่ .main — ต่ำกว่า 768px อยู่นอก envelope ที่ออกแบบ (ไม่ใช่ข้อบกพร่อง). วัดที่ขอบล่าง 768 + desktop 1280.
    """
    results = []
    for w in (768, 1280):
        page.set_viewport_size({"width": w, "height": 900})
        open_(page)
        # เดินทุกแท็บ + เปิด drawer เพื่อวัดจริง
        for t in ("home", "pay", "docs", "notify"):
            go_tab(page, t)
            over = ev(page, "() => document.body.scrollWidth - window.innerWidth")
            assert over <= 2, f"[{w}px · {t}] body ล้นแนวนอน {over}px"
        after(page, "() => openView('profile','EMP-00123')")
        over_d = ev(page, "() => document.body.scrollWidth - window.innerWidth")
        assert over_d <= 2, f"[{w}px · drawer] body ล้นแนวนอน {over_d}px"
        results.append(f"{w}px OK")
    page.set_viewport_size({"width": 1280, "height": 900})
    return "responsive ไม่มี hscroll: " + " · ".join(results)


def c_fn93(page):
    """[FN-93] ประวัติการเข้าถึงข้อมูล append-only (แก้/ลบไม่ได้)"""
    open_(page)
    after(page, "() => openView('profile','EMP-00123')")
    dt = drawer_text(page)
    assert "ประวัติการเข้าถึงข้อมูลของฉัน" in dt and "append-only" in dt, "ไม่มีบล็อกประวัติเข้าถึง append-only"
    n_audit = ev(page, "() => document.querySelectorAll('#drawer .audit-row').length")
    assert n_audit == 3, f"ควรมีรายการ audit 3 (ได้ {n_audit})"
    assert "แก้/ลบไม่ได้" in dt, "ไม่ระบุว่าแก้/ลบไม่ได้ (append-only)"
    # ไม่มีปุ่มลบ/แก้ในบล็อก audit
    mut = ev(page, "() => [...document.querySelectorAll('#drawer .audit-row button, #drawer .audit-row [onclick]')].length")
    assert mut == 0, "บล็อก audit มีปุ่มแก้/ลบ (ต้อง append-only)"
    return "audit append-only: 3 รายการ · ระบุแก้/ลบไม่ได้ · ไม่มีปุ่มแก้/ลบ"


def c_fn94(page):
    """[FN-94] มาส์ก RESTRICTED (nationalId/บัญชี) + ปุ่ม reveal สลับ แสดง/ซ่อน (real click)"""
    open_(page)
    after(page, "() => openView('profile','EMP-00123')")
    dt0 = drawer_text(page)
    assert "X-XXXX-XXXXX-56-7" in dt0, "เลขบัตร ปชช. ไม่ถูกมาส์กตอนเริ่ม"
    assert "1-2345-67890-56-7" not in dt0, "เลขเต็มโผล่ทั้งที่ยังไม่กดแสดง (มาส์กพัง)"
    assert ev(page, "() => state.drawer.reveal") is False, "ค่าเริ่ม reveal ควร false"
    # กดปุ่มแสดงจริง → เผยเลขเต็ม
    page.locator("#drawer .reveal-btn").click()
    page.wait_for_function("() => state.drawer.reveal===true", timeout=4000)
    dt1 = drawer_text(page)
    assert "1-2345-67890-56-7" in dt1, "กดแสดงแล้วไม่เผยเลขบัตรเต็ม"
    # กดซ่อนกลับ → มาส์กอีกครั้ง
    page.locator("#drawer .reveal-btn").click()
    page.wait_for_function("() => state.drawer.reveal===false", timeout=4000)
    dt2 = drawer_text(page)
    assert "1-2345-67890-56-7" not in dt2 and "X-XXXX-XXXXX-56-7" in dt2, "กดซ่อนแล้วเลขเต็มไม่ถูกมาส์กกลับ"
    return "มาส์ก RESTRICTED: เริ่มมาส์ก · reveal→เลขเต็ม · ซ่อน→มาส์กกลับ (real click toggle)"


# ═══════════════════ NEGATIVE (display-only LOCK, rendered → absent) ═══════════════════

# เก็บ affordance จริงจากทุก surface (ทุกแท็บ + ทุก drawer + ทุก modal) แล้วตรวจว่า onclick
# ทุกตัวอยู่ใน ALLOWLIST ของฟังก์ชัน "ดู/นำทาง" เท่านั้น — ไม่มีตัวเขียน/บันทึก/ยื่นข้อมูล ESS.
NEG_SWEEP_JS = r"""
() => {
  const html = [];
  // ทุกแท็บ (page)
  ['home','pay','docs','notify'].forEach(t=>{ state.tab=t; html.push(renderPage()); });
  // ทุก drawer (view mode)
  [['payslip','PS-2568-07'],['profile','EMP-00123'],['leave','LV-2568-014'],
   ['expense','EX-2568-031'],['cert','CERT-2568-004'],['training','TR-2568-012'],
   ['notif','N-104']].forEach(d=>{
     state.drawer={open:true,mode:d[0],recordId:d[1],step:1,sub:0,reveal:false}; html.push(renderDrawer());
   });
  // payslip YTD sub-tab ด้วย
  state.drawer={open:true,mode:'payslip',recordId:'PS-2568-07',step:1,sub:1,reveal:false}; html.push(renderDrawer());
  // profile reveal=true (เผยเลข) ด้วย — กันมี affordance โผล่เฉพาะ state นี้
  state.drawer={open:true,mode:'profile',recordId:'EMP-00123',step:1,sub:0,reveal:true}; html.push(renderDrawer());
  // ทุก modal
  state.modal={open:true,type:'actionPicker',data:null}; html.push(renderModal());
  state.modal={open:true,type:'accessDenied',data:null}; html.push(renderModal());
  const box=document.createElement('div'); box.innerHTML=html.join('');
  const acts=[...box.querySelectorAll('button,a[href],[onclick]')].map(el=>({
    tag: el.tagName,
    txt:(el.textContent||'').replace(/\s+/g,' ').trim(),
    on:(el.getAttribute('onclick')||''),
    href:(el.getAttribute('href')||''),
  }));
  return {
    acts,
    forms: box.querySelectorAll('form').length,
    // input ทั้งหมดยกเว้นช่องค้นหาแจ้งเตือน (filter · placeholder ค้นหา) = ห้ามมี input ป้อนข้อมูล
    dataInputs: [...box.querySelectorAll('input,textarea,select')]
      .filter(e => (e.getAttribute('placeholder')||'').indexOf('ค้นหา') < 0).length,
    fileInputs: box.querySelectorAll('input[type=file]').length,
  };
}
"""

# onclick ที่อนุญาต = ดู/นำทาง/สลับ view-state เท่านั้น (ไม่แตะข้อมูลธุรกิจ ESS)
#   สองสาขา: (ก) เรียกฟังก์ชันดู/นำทาง (มี \b ท้ายชื่อ) · (ข) กำหนดค่า view-state (state.notif/drawer.*=)
#   แยก \b ให้อยู่เฉพาะสาขาชื่อฟังก์ชัน — สาขา assignment จบที่ '=' (กัน reveal=!... ที่ = ตามด้วย !)
ALLOW_ONCLICK = re.compile(
    r"^\s*(?:(?:openView|goTab|openModal|closeModal|closeDrawer|deepLink|navigate|toggleModule|"
    r"render|event\.stopPropagation)\b|state\.(?:notif|drawer)\.[\w.]+\s*=)"
)
# ชื่อ 'ฟังก์ชัน' ที่บ่งชี้การเขียน/ยื่น/บันทึก/อนุมัติ/จ่ายข้อมูล — ต้องไม่มีเป็นตัวลงมือ
#   จับเฉพาะ identifier ที่ตามด้วย '(' (การเรียกฟังก์ชัน) เพื่อไม่ไปชนสตริงพารามิเตอร์ เช่น goTab('pay')
MUTATE_ONCLICK = re.compile(
    r"\b(?:submit\w*|save\w*|create\w*|delete\w*|remove\w*|approve\w*|reject\w*|pay[A-Z]\w*|"
    r"payout|disburse\w*|post[A-Z]\w*|doArchive\w*|doCancel\w*|doApprove\w*|doReject\w*|"
    r"updateRecord|writeData)\s*\(", re.I)


def c_neg1_no_mutation(page):
    """[N1] ไม่มี affordance เขียนข้อมูล: ไม่มี <form>, ไม่มี input ป้อนข้อมูล, onclick ทุกตัว=ดู/นำทางเท่านั้น"""
    open_(page)
    r = ev(page, NEG_SWEEP_JS)
    acts = r["acts"]
    assert len(acts) > 15, f"เก็บ affordance ได้น้อยผิดปกติ ({len(acts)}) — surface อาจไม่เรนเดอร์"
    assert r["forms"] == 0, "[N1] พบ <form> ในพอร์ทัล (display-only ห้ามมีฟอร์ม)"
    assert r["dataInputs"] == 0, f"[N1] พบช่องป้อนข้อมูล {r['dataInputs']} (อนุญาตเฉพาะช่องค้นหาแจ้งเตือน)"
    assert r["fileInputs"] == 0, "[N1] พบช่องอัปโหลดไฟล์ (display-only ห้ามมี)"
    # ทุก onclick ต้องอยู่ allowlist และต้องไม่ตรงคำ mutate
    bad_allow = [a for a in acts if a["on"] and not ALLOW_ONCLICK.search(a["on"])]
    assert not bad_allow, f"[N1] พบ onclick นอก allowlist (อาจเขียนข้อมูล): {[a['on'][:50] for a in bad_allow][:4]}"
    bad_mut = [a for a in acts if MUTATE_ONCLICK.search(a["on"])]
    assert not bad_mut, f"[N1] พบ onclick ที่เขียน/ยื่น/อนุมัติข้อมูล ESS: {[a['on'][:50] for a in bad_mut][:4]}"
    return f"display-only lock: 0 form · 0 data-input · {len(acts)} affordance ทั้งหมด=ดู/นำทาง (ไม่มีตัวเขียนข้อมูล)"


def c_neg2_picker_link_only(page):
    """[N2] 'ยื่นคำขอ' link-only: ทุกแถว action-picker = deepLink navigate-out (ไม่เปิดฟอร์มในพอร์ทัล)"""
    open_(page)
    after(page, "() => openModal('actionPicker')")
    rows = ev(page, "() => [...document.querySelectorAll('#modalBackdrop .ap-row')].map(r=>r.getAttribute('onclick'))")
    # FIX-01: เพิ่ม 'ขอหนังสือรับรอง' → launcher = 5 แถว
    assert len(rows) == 5, f"action-picker ควรมี 5 แถว (ได้ {len(rows)})"
    assert all(o and o.strip().startswith("deepLink(") for o in rows), \
        f"มีแถวที่ไม่ใช่ deepLink navigate-out: {rows}"
    # คลิกจริงแถวแรก → toast navigate-out + modal ปิด + ไม่มีฟอร์มเปิด
    page.locator("#modalBackdrop .ap-row").first.click()
    page.wait_for_function("() => state.modal.open===false", timeout=4000)
    tt = toast_text(page)
    assert "กำลังนำทาง" in tt, f"คลิกแถวแล้วไม่ navigate-out (toast: '{tt}')"
    assert ev(page, "() => document.querySelectorAll('#drawer input, #appContent form, #modalBackdrop input').length") == 0, \
        "คลิกยื่นคำขอแล้วเปิดฟอร์มในพอร์ทัล"
    return "action-picker 5 แถว = deepLink navigate-out ทั้งหมด · คลิกจริง→toast นำทาง · ไม่มีฟอร์ม"


def c_neg3_self_access(page):
    """[N3] self-access: ทดสอบเข้าถึงพนักงานอื่น → 403 บล็อก · ไม่มีข้อมูลพนักงานอื่นเรนเดอร์"""
    open_(page)
    # trigger จาก demo-strip (คลิกจริง)
    page.locator(".demo-strip button").click()
    page.wait_for_function("() => state.modal.open===true && state.modal.type==='accessDenied'", timeout=4000)
    mt = modal_text(page)
    assert "403" in mt and "เข้าถึงถูกปฏิเสธ" in mt, "ไม่ขึ้น 403 หลังทดสอบเข้าถึงพนักงานอื่น"
    # ยืนยันไม่มี "ข้อมูล" พนักงานอื่นโผล่ (ชื่อ/รหัสของคนอื่น) — ไม่ใช่ป้าย UI เช่น "พนักงานอื่น"
    assert_text_absent(page, ["EMP-00124", "EMP-00200", "สมหญิง", "วิชัย", "สุนิสา"], scope="#appContent")
    assert ev(page, "() => (document.getElementById('appContent').textContent.match(/EMP-\\d+/g)||[]).every(x=>x==='EMP-00123')"), \
        "พบรหัสพนักงานอื่นนอกเหนือ EMP-00123 บนหน้า"
    return "self-access: demo→403 บล็อก · หน้าไม่มีข้อมูล/รหัสพนักงานอื่น (self เท่านั้น)"


def c_neg4_ap_row_stacked(page):
    """[N4 · UX-01 regression] ap-row: .ap-title / .ap-sub = display:block และเรนเดอร์คนละบรรทัด (stacked)"""
    open_(page)
    after(page, "() => openModal('actionPicker')")
    r = ev(page, r"""() => {
      const rows=[...document.querySelectorAll('#modalBackdrop .ap-row')];
      return rows.map(row=>{
        const t=row.querySelector('.ap-title'), s=row.querySelector('.ap-sub');
        if(!t||!s) return {ok:false, why:'missing'};
        const tc=getComputedStyle(t).display, sc=getComputedStyle(s).display;
        const tr=t.getBoundingClientRect(), sr=s.getBoundingClientRect();
        return {tDisp:tc, sDisp:sc, tBottom:Math.round(tr.bottom), sTop:Math.round(sr.top),
                stacked: tr.bottom <= sr.top + 1};
      });
    }""")
    assert len(r) == 5, f"ควรมี 5 ap-row (ได้ {len(r)})"
    for i, row in enumerate(r):
        assert row.get("tDisp") == "block" and row.get("sDisp") == "block", \
            f"[N4] แถว {i}: title/sub ไม่ใช่ display:block ({row})"
        assert row.get("stacked"), \
            f"[N4] แถว {i}: title+sub ยุบเป็นบรรทัดเดียว (title.bottom {row.get('tBottom')} > sub.top {row.get('sTop')})"
    return "ap-row: title/sub = display:block และซ้อนคนละบรรทัด (stacked) ครบ 5 แถว (UX-01 กันถอย)"


def c_esc_chain(page):
    """[Esc · DSP-01] modal เปิดทับ drawer → Esc ครั้งเดียวปิด modal · drawer ยังอยู่"""
    open_(page)
    after(page, "() => openView('profile','EMP-00123')")
    assert ev(page, "() => state.drawer.open") is True, "เปิด drawer โปรไฟล์ไม่สำเร็จ"
    after(page, "() => openModal('actionPicker')")
    assert ev(page, "() => state.modal.open") is True and ev(page, "() => state.drawer.open") is True, \
        "modal เปิดทับ drawer ไม่สำเร็จ"
    # z-order: modal ต้องอยู่เหนือ drawer (DSP-01)
    under = ev(page, JS_MODAL_UNDER_DRAWER)
    assert not under, f"[DSP-01] modal จมใต้ drawer: {under}"
    # Esc ครั้งเดียว → ปิด modal, drawer ยังอยู่
    page.keyboard.press("Escape")
    page.wait_for_function("() => state.modal.open===false", timeout=4000)
    settle(page)
    assert ev(page, "() => state.drawer.open") is True, "[DSP-01] Esc ปิด modal แล้ว drawer หลุดปิดตาม (ควรอยู่)"
    # Esc อีกครั้ง → ปิด drawer
    page.keyboard.press("Escape")
    page.wait_for_function("() => state.drawer.open===false", timeout=4000)
    settle(page)
    assert_overlay_cleared_after_close(page, note="หลังปิด drawer ด้วย Esc")
    return "Esc chain: modal เหนือ drawer · Esc#1 ปิด modal (drawer อยู่) · Esc#2 ปิด drawer · overlay เคลียร์"


def c_overlay_clear(page):
    """[overlay] ปิด drawer/modal แล้วไม่มี overlay ค้างดักคลิกกลางจอ (BUG-6 guard)"""
    open_(page)
    after(page, "() => openView('payslip','PS-2568-07')")
    after(page, "() => closeDrawer()")
    assert_overlay_cleared_after_close(page, note="หลังปิด drawer สลิป")
    after(page, "() => openModal('actionPicker')")
    after(page, "() => closeModal()")
    assert_overlay_cleared_after_close(page, note="หลังปิด modal action-picker")
    # ไม่มี element อื่นวาดทับ overlay ที่เปิดอยู่ (BASE-KIT z-order invariant)
    after(page, "() => openView('profile','EMP-00123')")
    stack = ev(page, JS_OVERLAY_STACK)
    assert not stack, f"มี element วาดทับ overlay ผิดปกติ: {stack}"
    return "overlay เคลียร์หลังปิด (drawer+modal) · ไม่มีของทับ overlay ที่เปิดอยู่"


def c_no_garbage(page):
    """[polish] ไม่มีข้อความ mock/undefined/[object Object] หลุดบนจอ (ทุกแท็บ)"""
    open_(page)
    for t in ("home", "pay", "docs", "notify"):
        go_tab(page, t)
        assert_no_garbage_text(page, scope="#appContent")
    after(page, "() => openView('profile','EMP-00123')")
    assert_no_garbage_text(page, scope="#drawer")
    return "ไม่มีข้อความขยะ (undefined/NaN/[object Object]) ทุกแท็บ + drawer"


def c_affordances_fire(page):
    """[FIRE · C3.8] ปุ่มหลัก (qcard/ap-row) ยิง handler จริงเมื่อคลิก — จับ capture-phase ที่กลืนคลิกทั้งหน้า

    บั๊กจริง F-HR-ESS ที่ qc-ux มองไม่เห็น: listener 'click' ระดับ document แบบ capture-phase
    (}, true) เรียก stopPropagation → onclick ของทุกการ์ด/ทุกแถวตายเงียบ (real click ไม่เกิดอะไร)
    ทั้งที่ markup/cursor/keyboard ผ่านหมด. เปิด action-picker ให้ .ap-row เรนเดอร์คู่ .qcard แล้ว
    คลิกจริงที่ target → assert ว่า event ถึง target (ตัววัดใหม่ assert_affordances_fire ใน uikit).
    """
    open_(page)
    after(page, "() => openModal('actionPicker')")
    r = assert_affordances_fire(
        page, ['.qcard', '.ap-row'],
        note="ปุ่มหลัก dashboard+action-picker (capture-phase swallow guard)")
    return f"ปุ่มหลักยิง handler จริงทุกตัว (capture-phase ไม่กลืนคลิก) · tested={r['tested']}"


# ═══════════════════════════ FIX RE-GATE (F059 short round) ═══════════════════════════

def c_cert_link(page):
    """[FIX-01] launcher = 5 แถว รวม 'ขอหนังสือรับรอง' + section FN-06 ปุ่ม 'ขอหนังสือ' = deep-link (navigate-out · ไม่มีฟอร์ม)"""
    open_(page)
    after(page, "() => openModal('actionPicker')")
    rows = ev(page, "() => [...document.querySelectorAll('#modalBackdrop .ap-row')].map(r=>({on:r.getAttribute('onclick'),txt:r.textContent}))")
    assert len(rows) == 5, f"action-picker ควรมี 5 แถว (ได้ {len(rows)})"
    assert any("ขอหนังสือรับรอง" in r["txt"] for r in rows), "action-picker ไม่มีแถว 'ขอหนังสือรับรอง'"
    cert_row = [r for r in rows if "ขอหนังสือรับรอง" in r["txt"]][0]
    assert cert_row["on"].strip().startswith("deepLink('cert')"), f"แถวขอหนังสือไม่ใช่ deepLink('cert'): {cert_row['on']}"
    # LINKS.cert wire ปลายทาง #/cert/new
    assert ev(page, "() => LINKS.cert && LINKS.cert.route") == "#/cert/new", "LINKS.cert.route ไม่ใช่ #/cert/new"
    # section FN-06 (แท็บเอกสาร) มีปุ่ม 'ขอหนังสือ' → deepLink('cert')
    open_(page)
    go_tab(page, "docs")
    has_btn = ev(page, "() => [...document.querySelectorAll('#appContent button')].some(b=>/ขอหนังสือ/.test(b.textContent) && (b.getAttribute('onclick')||'').indexOf(\"deepLink('cert')\")>=0)")
    assert has_btn, "section หนังสือรับรอง (FN-06) ไม่มีปุ่ม 'ขอหนังสือ' = deepLink('cert')"
    # คลิก deepLink('cert') → toast นำทาง + ไม่มีฟอร์ม
    n_form = ev(page, "() => document.querySelectorAll('#appContent form, #appContent input, #modalBackdrop input').length")
    after(page, "() => deepLink('cert')")
    tt = toast_text(page)
    assert "กำลังนำทาง" in tt and "หนังสือรับรอง" in tt, f"deepLink('cert') ไม่นำทาง (toast: '{tt}')"
    assert n_form == 0, "หน้าเอกสารมีฟอร์ม/ช่องป้อน (display-only ต้องไม่มี)"
    return "cert: launcher 5 แถว(+ขอหนังสือรับรอง) · FN-06 ปุ่มขอหนังสือ=deepLink('cert') · toast นำทาง · route #/cert/new · ไม่มีฟอร์ม"


def c_shift(page):
    """[FIX-02] section 'ตารางกะของฉัน' เรนเดอร์ 7 วัน (อ่านอย่างเดียว · ไม่มีปุ่ม mutation)"""
    open_(page)
    go_tab(page, "pay")
    at = app_text(page)
    assert "ตารางกะของฉัน" in at, "แท็บเงินเดือน&เวลา ไม่มี section ตารางกะ"
    # นับแถวกะจาก DATA.shifts + เรนเดอร์จริง
    assert ev(page, "() => DATA.shifts.length") == 7, "DATA.shifts ไม่ใช่ 7 วัน"
    # หา section ที่มีหัว 'ตารางกะของฉัน' แล้วนับ tbody tr = 7
    n_rows = ev(page, r"""() => {
      const secs=[...document.querySelectorAll('#appContent .ess-sec')];
      const s=secs.find(x=>/ตารางกะของฉัน/.test((x.querySelector('h3')||{}).textContent||''));
      if(!s) return -1;
      return s.querySelectorAll('table tbody tr').length;
    }""")
    assert n_rows == 7, f"ตารางกะควรมี 7 แถว (ได้ {n_rows})"
    # ค่าจาก mock ต้องปรากฏจริง (กะเช้า/บ่าย/หยุด)
    for v in ["เช้า 08:00–17:00", "บ่าย 13:00–22:00", "หยุด"]:
        assert v in at, f"ตารางกะขาดค่ากะ: {v}"
    # ไม่มีปุ่ม/affordance แก้กะใน section นี้
    n_mut = ev(page, r"""() => {
      const secs=[...document.querySelectorAll('#appContent .ess-sec')];
      const s=secs.find(x=>/ตารางกะของฉัน/.test((x.querySelector('h3')||{}).textContent||''));
      if(!s) return -1;
      // ปุ่มใน section (ไม่นับ chip demo-only ที่เป็น span) — ต้องไม่มีปุ่ม action ใด ๆ
      return s.querySelectorAll('button, input, [onclick], a[href]').length;
    }""")
    assert n_mut == 0, f"section ตารางกะมี affordance ({n_mut}) — ต้องอ่านอย่างเดียว ไม่มีแก้กะ"
    return "ตารางกะของฉัน: 7 วัน (เช้า/บ่าย/หยุด) เรนเดอร์จริง · อ่านอย่างเดียว (0 ปุ่ม/ช่องป้อน)"


def c_demo_guard(page):
    """[FIX-04] prod strip: ซ่อน .demo-only แล้วจอไม่เหลือศัพท์ dev/contract + layout ไม่พัง

    inject .demo-only{display:none} แล้ว sweep innerText (เฉพาะที่มองเห็น — ไม่รวม display:none)
    ของทุกแท็บ: ต้องไม่พบ '[ASSUMED' · 'SecC' · 'self-access' · 'PS-1' · 'ตัวอย่าง (persona)'.
    """
    open_(page)
    assert ev(page, "() => document.querySelectorAll('.demo-only').length") >= 1, "ไม่มี element .demo-only ในไฟล์"
    page.add_style_tag(content=".demo-only{display:none !important}")
    banned = ["[ASSUMED", "SecC", "self-access", "PS-1", "ตัวอย่าง (persona)"]
    for t in ("home", "pay", "docs", "notify"):
        go_tab(page, t)
        vis = ev(page, "() => (document.getElementById('appContent').innerText || '')")
        hit = [b for b in banned if b in vis]
        assert not hit, f"[FIX-04] แท็บ {t}: ยังเห็นศัพท์ dev/contract หลังซ่อน demo-only: {hit}"
    # demo-strip ถูกซ่อนจริง · self-banner (ภาษาผู้ใช้) ยังอยู่
    assert ev(page, "() => { const el=document.querySelector('.demo-strip'); return !el || getComputedStyle(el).display==='none'; }"), \
        "demo-strip ยังแสดงหลังซ่อน demo-only"
    assert "คุณกำลังดูข้อมูลของตนเอง" in ev(page, "() => document.querySelector('.self-banner').innerText"), \
        "self-banner (ภาษาผู้ใช้) หาย"
    # layout ไม่พัง (ไม่มี hscroll)
    over = ev(page, "() => document.body.scrollWidth - window.innerWidth")
    assert over <= 2, f"layout พังหลังซ่อน demo-only (hscroll {over}px)"
    # Esc chain ยังทำงาน (drawer เปิด/ปิดด้วย Esc)
    after(page, "() => openView('profile','EMP-00123')")
    assert ev(page, "() => state.drawer.open") is True, "เปิด drawer ไม่ได้หลังซ่อน demo-only"
    page.keyboard.press("Escape")
    page.wait_for_function("() => state.drawer.open===false", timeout=4000)
    return "prod strip: ซ่อน .demo-only → 4 แท็บไม่เหลือ [ASSUMED]/SecC/self-access/PS-1/persona · self-banner คงอยู่ · layout ปกติ · Esc ทำงาน"


# ═══════════════════════════════ RUN ═══════════════════════════════

CASES = [
    ("E01", c_fn01),   ("E02", c_fn02),   ("E03", c_fn03),   ("E04", c_fn04),
    ("E05", c_fn05),   ("E06", c_fn06),   ("E07", c_fn07),   ("E08", c_fn08),
    ("E09", c_fn09),   ("E10", c_fn10),   ("E11", c_fn11),
    ("E90", c_fn90),   ("E92", c_fn92),   ("E93", c_fn93),   ("E94", c_fn94),
    ("N1", c_neg1_no_mutation), ("N2", c_neg2_picker_link_only),
    ("N3", c_neg3_self_access), ("N4", c_neg4_ap_row_stacked),
    ("ESC", c_esc_chain), ("OVL", c_overlay_clear), ("GBG", c_no_garbage),
    ("FIRE", c_affordances_fire),
    # FIX re-gate (F059 short round)
    ("F01", c_cert_link), ("F02", c_shift), ("F04", c_demo_guard),
]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        suite.watch(page)
        for tid, fn in CASES:
            suite.check(tid, fn.__doc__.strip().splitlines()[0], lambda fn=fn: fn(page))
        browser.close()

    ok = suite.report(exit_on_fail=False)
    total = len(suite.results)
    # FN coverage tally (15 FN · N-cases แยกนับ)
    fn_covered = 15
    print()
    print(f"FN ครอบ {fn_covered}/15 · เคสรวม {total} · ผ่าน {ok}/{total}")
    sys.exit(0 if ok == total and not suite.console_errors else 1)


if __name__ == "__main__":
    main()
