#!/usr/bin/env python3
"""uikit — เครื่องมือกลางสำหรับตรวจคุณภาพ UI และรัน E2E ของต้นแบบ CUBE

ใช้ร่วมกันทุก feature — ไฟล์ของแต่ละ feature เขียนแค่ "ลำดับการเดินจอ" เท่านั้น

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / '_SHARED' / '_e2e'))
    from uikit import Audit, Suite

ตรวจ 6 ด้าน
  1 Layout      getBoundingClientRect: clipping · scroll แนวนอน · สูงไม่เท่า · ข้อความล้น · ซ้อนทับ
                · คำอธิบายที่เด้งตอนชี้ ⓘ ถูกกล่องแม่ตัด/ล้นออกนอกจอ
  2 Responsive  ระบุด้วย --widths (ค่าเริ่มต้น 1024/1280/1920 · --quick = 1024/1280)
                ยึด "โหมด" ของ v8 Rule #97: 768–1180 adaptive · ≥1180 เต็มรูป
                เดิม 1280/1440/1920/2560 = ตัวอย่างของโหมดเดียวกันทั้ง 4 ตัว
  3 Browser     ค่าเริ่มต้น Chromium อย่างเดียว — เปิดด้วย --browsers=chromium,firefox,webkit
  4 Behavior    ลำดับการเดินจอที่ feature เขียนเอง
  5 Runtime     console error/warning/pageerror + resource ที่โหลดไม่ได้ (แยก CDN ภายนอกออกให้)
  6 A11y        keyboard reachable · tab order · focus ที่มองเห็น · contrast WCAG AA

────────────────────────────────────────────────────────────────────────────
⚠️ ปรับตาม html-generator-v8 เมื่อ 2026-08-10 — 3 จุดยังรอยืนยันกับไฟล์ v8 จริง

ตอนแก้ ทั้งโปรเจกต์ยังไม่มีไฟล์ v8 สักตัว (ทุกไฟล์ใน _final-docs เป็น v7 —
grep portalMenu/menu-fixed/page-fill/table-wrap ได้ 0 ทั้ง 8 ไฟล์) จึงยืนยันได้แค่
กับหน้าทดสอบสังเคราะห์ที่คัด CSS มาจาก file-skeleton.template.html ของ v8

  ✅ ยืนยันกับไฟล์จริงแล้ว  ตัวกรองของค้าง (5/5) · ไม่ regress (Layout 27 นิ่ง 2 รอบ) · เวลา −18%
  ⏳ รอไฟล์ v8 ตัวแรก      (ก) .menu-fixed ใน SEL_OK  (ข) .page-fill/.table-wrap ใน hscroll
                          (ค) ความกว้าง 1024 ให้ผลที่มีความหมายกับจอที่ออกแบบตาม #97

→ feature v8 ตัวแรกที่รัน step 5 = จุดที่ 3 ข้อนี้จะถูกแตะจริง **ให้ตรวจผลตรงนั้นด้วย**
  ถ้า .menu-fixed ยังโดนฟ้องว่าทับลิ้นชัก = แพตช์ยังไม่พอ ต้องแก้ต่อ

────────────────────────────────────────────────────────────────────────────
สัญญาณหลอกที่พิสูจน์แล้วว่าไม่ใช่ข้อบกพร่อง — กันไว้ในตัวตรวจนี้แล้ว ห้ามไปไล่ซ้ำ
  1 กล่องที่ scroll ได้ ไม่ใช่ "ตัด" — เลื่อนไปดูได้ · ตัดจริงเมื่อ overflow:hidden
    หรือเป็นเมนูลอย (absolute/fixed) ที่ตกอยู่ในกล่อง scroll
  2 element ที่ display:inline คืน clientWidth = 0 ตามสเปก — วัดข้อความล้นไม่ได้ (Firefox รายงานผิด 344 จุด)
  3 พื้นไล่สี (gradient) อ่านค่าสีพื้นไม่ได้ — ข้าม contrast
  4 onclick="event.stopPropagation()" ไม่ใช่ปุ่ม — ไม่ต้องโฟกัสได้
  5 ฉากหลัง overlay (backdrop) ไม่ต้องโฟกัสได้ — ปิดด้วย Esc/ปุ่ม X อยู่แล้ว
  6 ข้อความ "Failed to load resource" ไม่มี URL — ต้องดูจาก event ของ request จริง
  7 ตัวเลือกในเมนูที่กางอยู่ ไม่ใช่ control ในแถว
  8 ปุ่มล้างตัวกรองเป็น btn-sm ตามสเปกโซนกรอง (Rule #78.3) — สูงต่างจาก input ได้
  9 กล่องที่คลิกได้ซึ่งมี control โฟกัสได้อยู่ข้างในและเรียกฟังก์ชันเดียวกัน (ชื่อตรงเป๊ะ)
    = คีย์บอร์ดไปถึงผ่าน control นั้นแล้ว เช่น แถวตารางคลิกกาง + ปุ่มลูกศรในแถวเดียวกัน
 10 แถวที่เป็น "แผงกางออก" (เซลล์เดียว colspan หลายช่อง) ข้างในเป็น grid หลายบรรทัด
    → ไม่ตรวจ "ขอบบนตรงแนว"
 11 ไอคอนลอยที่จัดกึ่งกลางอยู่ "ใน" ช่องกรอก (ปุ่มล้าง/ลูกศรของช่องค้นหา) ไม่ใช่ control ของแถว
 12 ในแผงกางออก เทียบความสูง "ทีละบรรทัดที่เห็นจริง" (จับกลุ่มด้วยขอบบน) ไม่ใช่ทั้งแถวรวด
    — การ์ดตัวเลือกคนละบรรทัดกับลิงก์ปิด สูงต่างกันได้ตามดีไซน์
    แต่ของที่อยู่บรรทัดเดียวกันยังต้องสูงเท่ากัน (พิสูจน์แล้วด้วยการย้อนโค้ดให้พัง)
────────────────────────────────────────────────────────────────────────────
เพิ่มเมื่อ 2026-07-31 — ผู้ใช้เจอเองสองจุดที่ตัววัดมองไม่เห็น จึงเพิ่มการตรวจ:
  · เนื้อหาในเซลล์ตารางล้นออกนอกคอลัมน์ (min-width ของ div ข้างในชนะความกว้างคอลัมน์)
  · ช่องกรอกในแถวตารางเดียวกันขอบบนไม่ตรงกัน (เซลล์ที่มีป้ายใต้ช่องดันช่องขึ้น)

เพิ่มเมื่อ 2026-08-03 — ผู้ใช้เจอคำอธิบายตอนชี้ ⓘ ถูกขอบลิ้นชักตัดหายไปครึ่งประโยค:
  · เดิมข้อ 1 ใส่ .info-tip ไว้แล้ว แต่วัดได้แค่ "ตัวไอคอน 14px" ไม่ใช่ "กล่องคำอธิบาย"
    เพราะ BASE-KIT วาดกล่องด้วย ::after ซึ่ง querySelectorAll หาไม่เจอและไม่มี rect
  · ตัวตรวจใหม่อยู่ที่ JS_TIP — ก๊อป computed style ของ pseudo ลง element ชั่วคราวแล้ววัด
    ส่วนแบบที่วาดด้วย JS ตอน hover จะยิง pointerover ให้โผล่ก่อนวัด

เพิ่มเมื่อ 2026-08-05 — เจอตอนทำ F-GLPG-001 ว่า F-COA-001 ที่ส่งไปแล้วมีของพังเงียบ ๆ:
  · การ์ดสรุปเขียนเป็น '<div class="stat" '+(onclick?'class="cell-click" onclick=...':'')+'>'
    → 1 แท็กมี class= สองครั้ง เบราว์เซอร์เก็บอันแรกทิ้งอันหลัง · onclick ติด (กดได้จริง)
    แต่ cell-click หลุด → ไม่มี cursor:pointer = กรองได้แต่ผู้ใช้ไม่มีทางรู้ (วัดได้ 3 ใน 5 ใบ)
  · ตัววัดเดิมมองไม่เห็นทั้ง 3 ทาง: JS_A11Y_REACH ถามแค่ "คีย์บอร์ดไปถึงมั้ย" ·
    JS_GHOST_CLASS ถามว่า class มีนิยามใน CSS มั้ย (cell-click มี แค่ไม่ได้ติดกับ element) ·
    self_audit เทียบข้อความ ไม่ได้ประกอบ DOM จึงไม่เห็น attribute ที่ถูกทิ้ง
  · ตัวตรวจใหม่อยู่ที่ JS_AFFORDANCE — ถามตรง ๆ ว่า "ของที่มี onclick มี cursor:pointer มั้ย"
    ครอบทุกสาเหตุที่ทำให้ class หลุด · พิสูจน์แล้วกับ F-COA-001 ตัวจริง (จับได้ 3 ใบ)
    กันสัญญาณหลอกไว้ 2 ชั้น: backdrop (ข้อ 5) และ onclick ที่เป็น stopPropagation ล้วน (ข้อ 4)
────────────────────────────────────────────────────────────────────────────
"""
import sys, pathlib, json
from playwright.sync_api import sync_playwright

# ═══════════════════════ JS probes ═══════════════════════
JS_LAYOUT = """
() => {
  const out = { clipped: [], hscroll: [], rowMix: [], textOverflow: [], overlap: [], cellOverflow: [], rowTopMix: [], ghostCtl: [], menuCovered: [], optionCrowded: [], selectionCrowded: [], headMisplaced: [], deadStyle: [], iconFlush: [], stackFlush: [] };
  const vis = el => { const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden'; };

  // 1) ถูกกล่องแม่ตัด — FP#1: กล่องที่ scroll ได้ + เนื้อหาปกติ = เลื่อนไปดูได้ ไม่นับ
  //    v8 (#95): .menu-fixed = เมนูที่ portalMenu() ย้ายไป #overlay-root — ต้องตรวจด้วย
  document.querySelectorAll('.ss-list:not(.hidden), .menu-fixed, .combo-pop, .user-menu.open, .info-tip, .src, .conv-tag, .rev-tag').forEach(el => {
    if (!vis(el)) return;
    const r = el.getBoundingClientRect();
    const pos = getComputedStyle(el).position;
    const isPopup = pos === 'absolute' || pos === 'fixed';
    let p = el.parentElement;
    while (p && p !== document.body) {
      const cs = getComputedStyle(p);
      const hasHidden = [cs.overflow, cs.overflowX, cs.overflowY].includes('hidden');
      const hasScroll = ['auto','scroll'].some(v => [cs.overflow, cs.overflowX, cs.overflowY].includes(v));
      if (hasHidden || (hasScroll && isPopup)) {
        const pr = p.getBoundingClientRect();
        const worst = Math.max(r.bottom - pr.bottom, r.right - pr.right, pr.top - r.top, pr.left - r.left);
        if (worst > 2) out.clipped.push({ el: el.className, by: p.className || p.tagName, cut: Math.round(worst) });
      }
      p = p.parentElement;
    }
  });

  // 1b) ตัวควบคุมที่ผู้ใช้ต้องกด แต่ไม่มีกล่องให้เห็น
  //     ที่มา: F-PO-001 ใช้ class .toggle/.toggle-row/.toggle-slider ซึ่ง "ไม่มีอยู่ใน BASE-KIT เลย"
  //     → markup ถูกทุกอย่าง แต่ไม่มี CSS สวิตช์จึงสูง 0px กดไม่ได้ มองไม่เห็น
  //     audit.sh · self_audit.py · ตัววัดเดิมทั้งหมดผ่านหมด เพราะไม่มีข้อไหนถามว่า
  //     "class ที่ใช้มีนิยามจริงมั้ย" · จับได้ตอนคนเปิด screenshot ดูเท่านั้น (2026-08-04)
  document.querySelectorAll('[role=switch], [role=checkbox], [role=radio], .toggle, .toggle-slider, .cb, .mode-sw button').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;   // ซ่อนตั้งใจ ไม่นับ
    const r = el.getBoundingClientRect();
    if (r.width < 8 || r.height < 8)
      out.ghostCtl.push({ el: (el.className || el.tagName).toString().slice(0, 34),
                          w: Math.round(r.width), h: Math.round(r.height) });
  });

  // 1c) เมนูที่กางอยู่ถูก element อื่นวาดทับ
  //     ที่มา: F-PO-001 ให้ z-index เท่ากันทุก combobox ในตาราง → ช่องค้นหาของแถวล่าง
  //     (มาทีหลังใน DOM) วาดทับเมนูของแถวบน · ผู้ใช้เจอเอง 2026-08-04
  //     ตัววัดเดิมไม่เจอ เพราะข้อ "ถูกกล่องแม่ตัด" ตรวจแค่ overflow ของบรรพบุรุษ ไม่ได้ถามว่า
  //     "จุดบนเมนูนี้ คลิกแล้วโดนเมนูจริงมั้ย" · ต้องมี ≥2 แถวถึงจะเห็น
  document.querySelectorAll('.ss-list:not(.hidden), .menu-fixed, .combo-pop, [data-overlay].open').forEach(menu => {
    const r = menu.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) return;
    // สุ่มเป็นตาราง ทุก 16px ตามแนวตั้ง × 3 คอลัมน์ — สุ่มหยาบไปจะพลาดของที่ทับเป็นแถบบาง ๆ
    // (เจอตอนพิสูจน์: ช่องค้นหาของแถวล่างทับอยู่ระหว่างตัวเลือกที่ 1 กับ 2 พอดี 2026-08-04)
    const pts = [];
    for (let y = r.top + 6; y < r.bottom - 4; y += 16)
      for (const x of [r.left + 8, r.left + r.width / 2, r.right - 8]) pts.push([x, y]);
    for (const [x, y] of pts) {
      if (x < 0 || y < 0 || x > innerWidth || y > innerHeight) continue;
      const hit = document.elementFromPoint(Math.round(x), Math.round(y));
      if (!hit || hit === menu || menu.contains(hit)) continue;
      out.menuCovered.push({ menu: (menu.className || menu.id).toString().slice(0, 30),
                             by: (hit.className || hit.tagName).toString().slice(0, 34) });
      break;
    }
  });

  // 1d) option แบบสองบรรทัดต้องมีพื้นที่หายใจแนวตั้งพอ ไม่ชิดเส้นแบ่งรายการ
  document.querySelectorAll('.combo-pop button').forEach(option => {
    if (!vis(option)) return;
    const cs = getComputedStyle(option);
    const pt = parseFloat(cs.paddingTop) || 0;
    const pb = parseFloat(cs.paddingBottom) || 0;
    if (pt < 14 || pb < 14)
      out.optionCrowded.push({ el: option.className || option.tagName,
                               top: Math.round(pt), bottom: Math.round(pb) });
  });

  // 1e) ค่าที่เลือกแล้วแบบสองบรรทัดต้องไม่ถูกบีบติดขอบ control
  document.querySelectorAll('.combo-selection').forEach(selection => {
    if (!vis(selection)) return;
    const cs = getComputedStyle(selection);
    const pt = parseFloat(cs.paddingTop) || 0;
    const pb = parseFloat(cs.paddingBottom) || 0;
    if (pt < 8 || pb < 8)
      out.selectionCrowded.push({ el: selection.className,
                                  top: Math.round(pt), bottom: Math.round(pb) });
  });

  // 2) scroll แนวนอนที่ไม่ตั้งใจ
  // v8: .page-fill (#96 หน้าเต็มความสูง) · .table-wrap (#96 ตาราง scroll ภายใน) — จุดที่ล้นแนวนอนได้ง่ายสุด
  document.querySelectorAll('body, .content, .page-fill, .table-wrap, .drawer-body, .modal-body, .lt-wrap, .card, .drawer, .modal, .fgrid, .dgrid, .exp-in, .line-expand-panel-inner, .lx-grid, .bud-grid').forEach(el => {
    const over = el.scrollWidth - el.clientWidth;
    if (over > 2) out.hscroll.push({ el: el.className || el.tagName, over: Math.round(over), w: el.clientWidth });
  });

  // 3) ปุ่ม/ช่องกรอกในแถวเดียวกันสูงไม่เท่ากัน — FP#7 ตัวเลือกในเมนู · FP#8 btn-sm ในโซนกรอง
  //    FP#11 ไอคอนลอยที่จัดกึ่งกลางอยู่ "ใน" ช่องกรอก (ปุ่มล้าง/ลูกศรของช่องค้นหา) ไม่ใช่ control ของแถว
  //    FP#12 แถวแผงกางออกเป็น grid หลายบรรทัด — เทียบเฉพาะช่องกรอกด้วยกัน (การ์ด/ลิงก์สูงต่างได้)
  const adorn = e => getComputedStyle(e).position === 'absolute' && !!e.closest('.search-select');
  const panelRow = row => row.tagName === 'TR' && row.cells && row.cells.length === 1 && (row.cells[0].colSpan || 1) > 1;
  document.querySelectorAll('.filter-bar, .ph-actions, .dw-footer, .dw-footer-right, .modal-footer, .drawer-header-actions, .bulk-bar, .lt tbody tr, .file-row, .table-footer, .qty-cell').forEach(row => {
    const c = [...row.querySelectorAll('input:not([type=hidden]), select, button')]
      .filter(vis)
      .filter(e => !e.closest('.ss-list'))
      .filter(e => !adorn(e))
      .filter(e => !(row.classList.contains('filter-bar') && e.classList.contains('btn-sm')));
    // แผงกางออกเป็น grid หลายบรรทัด → เทียบทีละบรรทัดที่เห็นจริง (จับกลุ่มด้วยขอบบน)
    // แถวปกติทุกอย่างอยู่บรรทัดเดียว → เทียบทั้งแถวเหมือนเดิม
    const groups = new Map();
    c.forEach(e => {
      const k = panelRow(row) ? Math.round(e.getBoundingClientRect().top / 8) : 0;
      if (!groups.has(k)) groups.set(k, []);
      groups.get(k).push(e);
    });
    groups.forEach(g => {
      const hs = g.map(e => Math.round(e.getBoundingClientRect().height));
      if (new Set(hs).size > 1)
        out.rowMix.push({ row: row.className, heights: g.map((e, j) => (e.className || e.tagName) + '=' + hs[j]) });
    });
  });

  // 4) ข้อความล้นกล่อง — FP#2: inline element คืน clientWidth = 0 ตามสเปก
  document.querySelectorAll('.dg-v, .prod-name, .file-n, .bud-name, .appr-n, .stat-value, .idno, .btn, .sum-row, .flow-step, .pill, .conv-tag, .src, .stepper-label').forEach(el => {
    if (!vis(el)) return;
    const cs = getComputedStyle(el);
    if (cs.overflow !== 'visible' || cs.textOverflow === 'ellipsis') return;
    if (cs.display === 'inline') return;
    const over = el.scrollWidth - el.clientWidth;
    if (over > 2) out.textOverflow.push({ el: el.className, txt: el.textContent.trim().slice(0, 24), over: Math.round(over) });
  });

  // 5) เนื้อหาในเซลล์ตารางล้นออกนอกคอลัมน์ (ไปทับคอลัมน์ข้าง ๆ)
  document.querySelectorAll('td, th').forEach(cell => {
    const cr = cell.getBoundingClientRect();
    if (cr.width < 1) return;
    cell.querySelectorAll('*').forEach(el => {
      if (getComputedStyle(el).position === 'absolute') return;   // เมนูลอย วัดแยกในข้อ 1
      if (el.closest('.ss-list')) return;
      const r = el.getBoundingClientRect();
      if (r.width < 1) return;
      const over = Math.max(r.right - cr.right, cr.left - r.left);
      if (over > 2) out.cellOverflow.push({ cell: cell.className || cell.cellIndex,
        el: (el.className || el.tagName).toString().slice(0, 26),
        over: Math.round(over), cellW: Math.round(cr.width), elW: Math.round(r.width) });
    });
  });

  // 6) ช่องกรอกในแถวตารางเดียวกันไม่อยู่แนวเดียวกัน (ขอบบนไม่ตรง)
  //    FP#10: แถวที่เป็น "แผงกางออก" (เซลล์เดียว colspan หลายช่อง) ข้างในเป็น grid หลายบรรทัด
  //    ช่องคนละบรรทัดไม่ต้องตรงแนวกัน — แต่ยังตรวจ "สูงเท่ากัน" ในข้อ 3 ตามปกติ
  const isPanelRow = tr => tr.cells.length === 1 && (tr.cells[0].colSpan || 1) > 1;
  document.querySelectorAll('.lt tbody tr, .table tbody tr').forEach(tr => {
    if (isPanelRow(tr)) return;
    const c = [...tr.querySelectorAll('input:not([type=hidden]), select, button')]
      .filter(vis).filter(e => !e.closest('.ss-list')).filter(e => !adorn(e));
    // FP#11 (2026-08-04 F-COA-001): ปุ่มคนละ <td> ที่ "สูงไม่เท่ากัน" แต่จัดกึ่งกลางแนวตั้งถูกต้อง
    //   จะมีขอบบนต่างกันเสมอ — tree-toggle 20px vs ra-btn 28px ได้ top ต่าง 4px แต่ center ตรงกันเป๊ะ
    //   ตาคนเห็นว่า "ตรงแนว" เพราะมองที่กึ่งกลาง ไม่ใช่ขอบบน → เทียบ center เมื่ออยู่คนละเซลล์
    //   (เดิมรายงาน 248 จุดใน F-COA ซึ่งไม่มีจุดไหนเพี้ยนจริงเลยสักจุด)
    const rects = c.map(e => e.getBoundingClientRect());
    const sameCell = c.length > 1 && c.every(e => e.closest('td') === c[0].closest('td'));
    const key = sameCell ? rects.map(r => Math.round(r.top))
                         : rects.map(r => Math.round(r.top + r.height / 2));
    if (new Set(key).size > 1)
      out.rowTopMix.push({ row: tr.className || 'tr',
        items: c.map((e, j) => (e.className || e.tagName).toString().slice(0, 20) + '@' + key[j]) });
  });

  // 7) ลูกโดยตรงของ flex/grid ซ้อนทับกัน
  document.querySelectorAll('.fgrid, .dgrid, .bud-grid, .stats, .ph, .filter-bar, .dw-footer, .modal-footer').forEach(box => {
    const kids = [...box.children].filter(vis);
    for (let i = 0; i < kids.length; i++) for (let j = i + 1; j < kids.length; j++) {
      const a = kids[i].getBoundingClientRect(), b = kids[j].getBoundingClientRect();
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left);
      const oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ox > 2 && oy > 2)
        out.overlap.push({ box: box.className, a: kids[i].className || kids[i].tagName,
                           b: kids[j].className || kids[j].tagName, ox: Math.round(ox), oy: Math.round(oy) });
    }
  });
  // 8) ค่าที่ CSS ตั้งไว้แต่ไม่มีผลเพราะ element เป็น inline (margin/padding แนวตั้ง · width/height)
  //    ใบเปรียบเทียบราคา 2026-08-04: .win-m ใช้เป็น <span> ซึ่งเป็น inline → margin-top:2px ไม่ทำงาน
  //    ข้อความชื่อผู้ขายกับรหัสจึงไหลต่อกันบรรทัดเดียว ("บจก. สยามออฟฟิศ ซัพพลายV-006")
  //    ตัววัดเดิมมองไม่เห็นเพราะไม่ล้น ไม่ทับ ไม่เกินกรอบ — แค่ "ติดกัน" ซึ่งไม่มีข้อไหนถาม
  document.querySelectorAll('[class]').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display !== 'inline') return;
    const dead = [];
    if (cs.marginTop !== '0px') dead.push('margin-top:' + cs.marginTop);
    if (cs.marginBottom !== '0px') dead.push('margin-bottom:' + cs.marginBottom);
    if (cs.width !== 'auto' && cs.width !== '') dead.push('width:' + cs.width);
    if (cs.height !== 'auto' && cs.height !== '') dead.push('height:' + cs.height);
    if (!dead.length) return;
    const r = el.getBoundingClientRect();
    if (r.width < 1 && r.height < 1) return;
    out.deadStyle.push({ el: (el.className || el.tagName).toString().slice(0, 30),
                         props: dead.join(' · '), txt: (el.textContent || '').trim().slice(0, 24) });
  });

  // 9) หัวลิ้นชัก/หน้าต่าง: ปุ่มปิดต้องอยู่ขวาสุดของแถวเดียวกับหัวข้อ (Rule #31.4 · #46.4)
  //    ผู้ใช้เจอเอง 2026-08-04: ลืมห่อ .dw-head-row → ปุ่มปิดตกไปอยู่ใต้หัวข้อ หัวกินแค่มุมซ้ายบน
  //    ตัววัดเดิมมองไม่เห็นเพราะ .dw-head ไม่ใช่ flex จึงไม่ถูกนับเป็น "แถว" และไม่อยู่ในรายการกล่องที่ตรวจซ้อนทับ
  document.querySelectorAll('.dw-head, .drawer-header, .modal-header').forEach(head => {
    const hr = head.getBoundingClientRect();
    if (hr.width < 10 || hr.height < 10) return;
    const btns = [...head.querySelectorAll('.top-icon-btn, .icon-btn')].filter(vis);
    if (!btns.length) return;
    const close = btns[btns.length - 1];               // ปุ่มปิดอยู่ขวาสุดเสมอตาม contract
    const br = close.getBoundingClientRect();
    // ก) ตกบรรทัด — ปุ่มอยู่ต่ำกว่าครึ่งล่างของหัว ทั้งที่ควรอยู่แถวบนสุดร่วมกับหัวข้อ
    const title = head.querySelector('.dw-title, .drawer-title, .modal-title, .idno');
    if (title) {
      const tr = title.getBoundingClientRect();
      if (br.top >= tr.bottom - 2)
        out.headMisplaced.push({ head: head.className || 'head', kind: 'ตกไปอยู่ใต้หัวข้อ',
                                 detail: 'ปุ่มปิดขอบบน ' + Math.round(br.top) + ' · หัวข้อขอบล่าง ' + Math.round(tr.bottom) });
    }
    // ข) ไม่ชิดขวา — หัวข้อกับปุ่มไม่ได้ถูกดันออกจากกัน (มักเกิดจากไม่มีตัวจัดแนวครอบ)
    const gap = hr.right - br.right;
    if (gap > 48)
      out.headMisplaced.push({ head: head.className || 'head', kind: 'ปุ่มปิดไม่ชิดขวาของหัว',
                               detail: 'ห่างขอบขวา ' + Math.round(gap) + 'px' });
  });

  // ═══ ไอคอนชนตัวอักษรในปุ่ม/แท็บ/ป้าย ═══
  // ผู้ใช้ทักเอง 2026-08-06 (F-SCFG-001): แท็บระดับหน้าใช้ .drawer-tab ของ BASE-KIT ซึ่งเป็น
  // display:block และ markup วาง <i><span> ติดกันไม่มีช่องว่าง → ไอคอนชนตัวอักษร 0px ทั้ง 3 แท็บ
  // ตัววัดเดิมมองไม่เห็นเพราะ "ซ้อนทับ" เทียบเฉพาะพี่น้องใน flex/grid box (แท็บนี้ไม่ใช่ flex)
  // และ 0px ไม่ถือว่าซ้อนทับอยู่แล้ว — มันคือ "ชิดเกินไป" ซึ่งไม่มีใครวัด
  // ลวงตาที่ทำให้คนไม่ทันสังเกต: บาง glyph (sliders-horizontal) มีที่ว่างในกรอบ 16px ของตัวเอง
  // จึงดูเหมือนมีช่องไฟ ทั้งที่ CSS ไม่ได้เว้นให้ → ช่องไฟไม่สม่ำเสมอระหว่างแท็บ
  document.querySelectorAll('button, a, .drawer-tab, .sec-t, .pill, .badge, .chip, label').forEach(el => {
    if (!vis(el)) return;
    const ic = el.querySelector(':scope > svg, :scope > [data-lucide]');
    if (!ic) return;
    let tx = null;
    for (const n of el.childNodes) {                       // ข้อความตัวแรกที่ตามหลังไอคอน
      if (n.nodeType === 3 && n.textContent.trim()) {
        const rg = document.createRange(); rg.selectNodeContents(n); tx = rg.getBoundingClientRect(); break;
      }
      if (n.nodeType === 1 && n !== ic && n.textContent.trim() && !n.querySelector('svg')) {
        tx = n.getBoundingClientRect(); break;
      }
    }
    if (!tx || !tx.width) return;
    const a = ic.getBoundingClientRect();
    if (!a.width) return;
    if (a.bottom < tx.top || tx.bottom < a.top) return;     // คนละบรรทัด = ไม่เกี่ยวกัน
    const g = tx.left - a.right;
    if (g >= 0 && g < 4)                                    // ติดลบ = ซ้อนทับ มีตัวนับอื่นจับอยู่แล้ว
      out.iconFlush.push({ el: el.className || el.tagName, txt: (el.textContent || '').trim().slice(0, 24),
                           gap: Math.round(g * 10) / 10 });
  });

  // ═══ ก้อนเนื้อหาระดับหน้าติดกัน (ไม่มีจังหวะแนวตั้ง) ═══
  // ผู้ใช้ทักเอง 2026-08-06 (F-SCFG-001): .card ของ BASE-KIT ไม่มี margin — ถูกแล้ว เพราะ kit
  // ไม่ควรเดาบริบทที่ตัวเองถูกวาง · แต่แปลว่า "หน้าที่ตั้งจังหวะเป็นของ page CSS" ซึ่งลืมได้ง่ายมาก
  // ผลคือ card→card · card→nbar ติดกัน 0px เห็นเป็นเส้นคู่ อ่านเหมือนกล่องเดียวที่ขาด
  // ตรวจเฉพาะ "กองบล็อกระดับหน้า" (.content / .drawer-body / .modal-body) ไม่ลงไปในกล่อง
  // เพราะส่วนย่อยในกล่องเดียวกัน (filter-bar → ตาราง → footer) ตั้งใจให้ชิดกันแล้วคั่นด้วยเส้น
  // FP#10 — แถวในลิสต์ที่คั่นด้วยเส้นอยู่แล้ว (.diff-row) ตั้งใจให้ชิดกัน ไม่ใช่ของพัง
  // ตัวแยก: border-radius · กล่องมุมมนคือกล่องเอกเทศ สองใบชนกันอ่านเป็นกล่องเดียวที่ขาด
  // ส่วนแถวในลิสต์ radius 0 → ต้องมีอย่างน้อยหนึ่งฝั่งเป็นกล่องมุมมนถึงจะนับ
  const rounded = el => parseFloat(getComputedStyle(el).borderTopLeftRadius) >= 4;
  document.querySelectorAll('.content, .drawer-body, .modal-body').forEach(stack => {
    const kids = [...stack.children].filter(e => {
      const r = e.getBoundingClientRect();
      return r.width > 0 && r.height > 0 && getComputedStyle(e).position === 'static';
    });
    for (let i = 1; i < kids.length; i++) {
      const pr = kids[i-1].getBoundingClientRect(), cr = kids[i].getBoundingClientRect();
      if (cr.top < pr.bottom - 1) continue;                 // ซ้อน/คนละคอลัมน์ — มีตัวนับอื่นดูแล
      if (!rounded(kids[i-1]) && !rounded(kids[i])) continue;
      const g = Math.round(cr.top - pr.bottom);
      if (g < 8) out.stackFlush.push({ stack: stack.className.toString().slice(0,20) || 'content',
          a: kids[i-1].className.toString().slice(0,26) || kids[i-1].tagName,
          b: kids[i].className.toString().slice(0,26) || kids[i].tagName, gap: g });
    }
  });

  return out;
}
"""

# ═══════ class ที่ใช้ใน markup แต่ไม่มีนิยามใน CSS ═══════
# รากเดียวกับ defect 2 ตัวที่เจอจริง:
#   · ใบสั่งซื้อ 2026-08-04 — .toggle/.toggle-slider ไม่มีใน BASE-KIT → สวิตช์สูง 0px มองไม่เห็น
#   · ใบเปรียบเทียบราคา 2026-08-04 — .drawer.wide ไม่ได้ประกาศ → ลิ้นชักตกกลับไปใช้ค่าฐาน 920px
#     ทั้งที่ทั้งโค้ด คอมเมนต์ และเทสเขียนว่า 1290 (เทสเช็คแค่ว่ามี class มั้ย ไม่ได้วัด px)
# ตัวนับเดิม ghostCtl จับได้เฉพาะตอนที่ element เล็กจนเกือบหาย — เคส .wide ขนาดปกติจึงรอด
JS_GHOST_CLASS = r"""
() => {
  // ต้องรองรับจุดที่ escape ไว้ใน selector (.w-3\.5) ไม่งั้นจะอ่านว่าไม่มีนิยาม
  const defined = new Set();
  for (const sheet of document.styleSheets) {
    let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
    if (!rules) continue;
    const walk = rs => { for (const r of rs) {
      if (r.selectorText)
        (r.selectorText.match(/\.(?:[-\w]|\\.)+/g) || []).forEach(c => defined.add(c.slice(1).split('\\').join('')));
      if (r.cssRules) walk(r.cssRules);
    }};
    walk(rules);
  }
  const used = new Map();
  document.querySelectorAll('*').forEach(el => {
    if (!el.classList || !el.classList.length) return;
    el.classList.forEach(c => { if (!used.has(c)) used.set(c, (el.tagName || '').toLowerCase()); });
  });
  const ghost = [];
  used.forEach((tag, c) => {
    if (defined.has(c)) return;
    if (/^lucide/.test(c)) return;     // ไลบรารีไอคอนใส่ให้ svg เอง ไม่ใช่ class ที่เราเขียน
    ghost.push({ cls: c, tag: tag });
  });
  return ghost;
}
"""

# ═══════ คำอธิบายที่เด้งตอนชี้ (tooltip) ถูกตัด / ล้นออกนอกจอ ═══════
# ต้องแยกออกมาจาก JS_LAYOUT เพราะวัดตรง ๆ ไม่ได้ 2 เหตุ:
#   1) BASE-KIT วาดด้วย ::after ซึ่งเป็น pseudo — querySelectorAll หาไม่เจอ และไม่มี getBoundingClientRect
#      → ก๊อป computed style ของ pseudo ใส่ element ชั่วคราวที่ host แล้ววัดแทน (ตกที่เดิมเป๊ะ)
#   2) แบบที่วาดด้วย JS จะเกิดตอน hover เท่านั้น → ต้องยิง pointerover ให้มันโผล่ก่อนวัด
# กล่องที่ scroll ได้ "ตัด" คำอธิบายจริง (ต่างจาก FP#1) เพราะ tooltip ไม่ใช่เนื้อหาที่เลื่อนไปดูได้
JS_TIP = """
() => {
  const out = [];
  const vis = el => { const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden'; };
  const clippers = node => { const list = []; let p = node.parentElement;
    while (p && p !== document.body) {
      const cs = getComputedStyle(p);
      if ([cs.overflow, cs.overflowX, cs.overflowY].some(v => v !== 'visible')) list.push(p);
      p = p.parentElement; }
    return list; };

  document.querySelectorAll('.info-tip, [data-tip]').forEach(host => {
    if (!vis(host)) return;
    const cs = getComputedStyle(host, '::after');
    let rect = null, pos = '', node = host;

    if (cs && cs.content && cs.content !== 'none' && cs.content !== 'normal') {
      const probe = document.createElement('span');
      for (const p of cs) probe.style.setProperty(p, cs.getPropertyValue(p));
      probe.textContent = cs.content.replace(/^["']|["']$/g, '');
      probe.style.setProperty('content', 'normal');
      probe.style.setProperty('opacity', '0');
      probe.style.setProperty('pointer-events', 'none');
      host.appendChild(probe);
      rect = probe.getBoundingClientRect(); pos = cs.position;
      probe.remove();
    } else {
      host.dispatchEvent(new PointerEvent('pointerover', { bubbles: true }));
      const live = [...document.querySelectorAll('.tip-pop, [role=tooltip]')].filter(vis);
      if (live.length) { node = live[0]; rect = node.getBoundingClientRect(); pos = getComputedStyle(node).position; }
      document.body.dispatchEvent(new PointerEvent('pointerover', { bubbles: true }));
    }
    const txt = (host.getAttribute('data-tip') || '').slice(0, 26);
    // ไม่มีกล่องให้วัด = ชี้แล้วไม่มีอะไรโผล่ — ต้องฟ้อง ไม่งั้น "ตรวจผ่าน" เพราะไม่มีของให้ตรวจ
    if (!rect || rect.width < 1) {
      if (txt) out.push({ txt, kind: 'missing', by: '—', px: 0, w: 0 });
      return;
    }

    // position:fixed ที่เกาะ body ไม่ถูกกล่องแม่ตัด — เหลือแค่ตรวจว่าอยู่ในจอ
    if (pos !== 'fixed') clippers(node).forEach(p => {
      const pr = p.getBoundingClientRect();
      const cut = Math.max(pr.left - rect.left, rect.right - pr.right, pr.top - rect.top, rect.bottom - pr.bottom);
      if (cut > 2) out.push({ txt, kind: 'cut', by: (p.className || p.tagName).toString().slice(0, 26),
                              px: Math.round(cut), w: Math.round(rect.width) });
    });
    const off = Math.max(-rect.left, rect.right - innerWidth, -rect.top, rect.bottom - innerHeight);
    if (off > 2) out.push({ txt, kind: 'viewport', by: 'จอ', px: Math.round(off), w: Math.round(rect.width) });
  });
  return out;
}
"""

# FP#4 stopPropagation ไม่ใช่ปุ่ม · FP#5 ฉากหลัง overlay ไม่ต้องโฟกัสได้
JS_A11Y_REACH = """
() => {
  const FOCUSABLE = 'a[href],button,input,select,textarea,[tabindex]';
  const out = [];
  document.querySelectorAll('[onclick]').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;
    if (el.matches(FOCUSABLE)) return;
    const h = (el.getAttribute('onclick') || '').replace(/\\s/g, '');
    // FP#4 — handler ที่ทำหน้าที่ "หยุด event ไม่ให้ทะลุไปแถวแม่" อย่างเดียว ไม่ใช่ปุ่ม
    //   ครอบทั้งแบบเขียนสด event.stopPropagation() และแบบเรียกผ่านตัวช่วยกลาง เช่น stopEvt(event)
    //   (ตัวช่วยกลางจำเป็นเพราะ self_audit.py นับ stopPropagation ดิบเกิน 3 จุด = "เหมา" — Rule #68)
    //   เจอ 2026-08-05 ที่ F-DOC-001: <td> 4 จุดถูกฟ้องว่า "คลิกได้แต่คีย์บอร์ดไปไม่ถึง" ทั้งที่ไม่ใช่ปุ่ม
    if (/^(event\\.stopPropagation\\(\\)|stopEvt\\(event\\))$/.test(h)) return;
    if (/backdrop/.test(el.className || '')) return;
    if (el.closest('[onclick]') !== el && el.parentElement.closest('[onclick]')) return;
    // FP#9 กล่องที่คลิกได้ ถ้ามี control โฟกัสได้อยู่ข้างในซึ่งเรียก "ฟังก์ชันเดียวกัน"
    //      แปลว่าคีย์บอร์ดทำสิ่งเดียวกันได้ผ่าน control นั้นแล้ว (เช่น แถวตารางคลิกกาง + ปุ่มลูกศรในแถว)
    //      เทียบชื่อฟังก์ชันเป๊ะ ๆ เท่านั้น — control ที่ทำคนละเรื่องไม่นับ
    const fname = s => ((s || '').match(/([A-Za-z_$][\\w$]*)\\s*\\(/) || [])[1];
    const mine = fname(h);
    if (mine && [...el.querySelectorAll(FOCUSABLE)]
          .some(c => fname(c.getAttribute('onclick')) === mine)) return;
    out.push({ tag: el.tagName, cls: (el.className || '').slice(0, 40), txt: el.textContent.trim().slice(0, 24) });
  });
  return out;
}
"""

# FP#3 พื้นไล่สีอ่านค่าสีไม่ได้ — ข้าม
JS_CONTRAST = """
() => {
  const lum = c => { const s = c.map(v => { v /= 255; return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4); });
    return .2126*s[0] + .7152*s[1] + .0722*s[2]; };
  const parse = s => { const m = s.match(/rgba?\\(([^)]+)\\)/); if (!m) return null;
    const p = m[1].split(',').map(x => parseFloat(x)); return { rgb: p.slice(0,3), a: p.length > 3 ? p[3] : 1 }; };
  const bgOf = el => { let p = el;
    while (p) { const cs = getComputedStyle(p);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return null;
      const c = parse(cs.backgroundColor);
      if (c && c.a > 0.5) return c.rgb; p = p.parentElement; } return [255,255,255]; };
  const out = [];
  document.querySelectorAll('*').forEach(el => {
    if (el.children.length > 0) return;
    const t = el.textContent.trim(); if (!t) return;
    const r = el.getBoundingClientRect(); if (r.width < 4 || r.height < 4) return;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.opacity === '0') return;
    const fg = parse(cs.color); if (!fg) return;
    const bg = bgOf(el); if (!bg) return;
    const l1 = lum(fg.rgb), l2 = lum(bg);
    const ratio = (Math.max(l1,l2) + .05) / (Math.min(l1,l2) + .05);
    const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700;
    const need = (size >= 24 || (bold && size >= 18.66)) ? 3 : 4.5;
    if (ratio < need)
      out.push({ cls: (el.className || el.tagName).toString().slice(0, 34), txt: t.slice(0, 20),
                 ratio: Math.round(ratio*100)/100, need, size, color: cs.color });
  });
  const seen = new Set(), uniq = [];
  out.forEach(o => { const k = o.cls + '|' + o.ratio; if (!seen.has(k)) { seen.add(k); uniq.push(o); } });
  return uniq;
}
"""

JS_FOCUS_RING = """
async () => {
  // FP#11 (2026-08-06 · F-SCFG-001): BASE-KIT ให้กรอบโฟกัสผ่าน box-shadow ที่มี transition 0.12s
  //   ของเดิมอ่าน computed style "ทันที" หลัง el.focus() → ได้ค่าตั้งต้นที่ยังโปร่งใส
  //   → ฟ้องว่า "ไม่มีกรอบโฟกัส" ทั้งที่มี และฟ้องไม่ครบทุกครั้ง (ผลแกว่งตามจังหวะเครื่อง)
  //   วัดแล้ว: ทันทีที่โฟกัส = rgba(0,0,0,0) · รอ 400ms = rgba(255,59,48,0.1) 0 0 0 3px
  //   แก้ด้วยการรอให้ transition จบก่อนอ่าน — ตัววัดที่แกว่งแย่กว่าตัววัดที่ช้า
  const settleFocus = el => new Promise(res => {
    const t = getComputedStyle(el).transitionDuration.split(',')
      .reduce((m, v) => Math.max(m, parseFloat(v) || 0), 0);
    setTimeout(res, Math.min(Math.round(t * 1000) + 60, 400));
  });
  // FP#9 (2026-08-06 · F-SCFG-001): ตัวควบคุมที่ถูกปิดอยู่ (disabled) รับโฟกัสไม่ได้ตามสเปก
  //   el.focus() จึงไม่เกิดอะไร → computed style ก่อน/หลังเท่ากันเสมอ → ถูกฟ้องว่า "ไม่มีกรอบโฟกัส"
  //   ทั้งที่ถูกต้องแล้ว (ของที่กดไม่ได้ ไม่ควรมีกรอบโฟกัส) — ตัดออกก่อนวัด
  const els = [...document.querySelectorAll('a[href],button,input,select,textarea,[tabindex]:not([tabindex="-1"])')]
    .filter(e => !e.disabled && e.getAttribute('aria-disabled') !== 'true')
    .filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
  const bad = [];
  for (const el of els) {
    const b0 = getComputedStyle(el);
    const b = { o: b0.outlineStyle + b0.outlineWidth, s: b0.boxShadow, bc: b0.borderColor };
    el.focus();
    await settleFocus(el);
    const a = getComputedStyle(el);
    if ((a.outlineStyle + a.outlineWidth) === b.o && a.boxShadow === b.s && a.borderColor === b.bc)
      bad.push({ tag: el.tagName, cls: (el.className || '').toString().slice(0, 34), txt: el.textContent.trim().slice(0, 20) });
    el.blur();
  }
  return bad;
}
"""

# ⭐ เพิ่ม 2026-08-04 (F-COA-001) — ผู้ใช้เจอหัวตารางพาดผ่านลิ้นชักที่ตัววัดเดิมมองไม่เห็น
#
# สาเหตุจริง: BASE-KIT ของ html-generator-v7 เขียน `z-index: var(--z-drawer)` ไว้ทุก overlay
# แต่ template ไม่เคยประกาศค่า --z-* ใน :root → computed เป็น `auto` ทั้งหมด
# → sticky thead (z-index:3) ชนะ drawer ทุกกรณี
#
# ทำไมของเดิมมองไม่เห็น: "element ซ้อนทับกัน" ใน JS_LAYOUT เทียบพี่น้องใน flex/grid box เดียวกัน
# — หัวตารางกับลิ้นชักอยู่คนละ subtree จึงไม่เคยถูกจับคู่ · ส่วน "เมนูที่กางอยู่ถูกวาดทับ" ดูเฉพาะ
# .ss-list/dropdown ไม่ครอบ overlay ใหญ่ · uikit ทั้งไฟล์ไม่มีคำว่า sticky เลยสักครั้ง
JS_OVERLAY_STACK = """
() => {
  const SEL = '.drawer, .modal, .modal-backdrop, .drawer-backdrop, [role="dialog"]';
  // ของที่ "อยู่เหนือ overlay ได้อย่างถูกต้อง" — ไม่นับเป็นข้อบกพร่อง
  //   .toast      = สูงสุดเสมอ (--z-toast 90)
  //   .menu-fixed = v8 Rule #95 portalMenu() ย้ายเมนูไป #overlay-root แล้วให้ --z-portal 60 > drawer 55
  //                 → กางจากในลิ้นชักแล้วต้องอยู่บน ไม่งั้นเมนูจม (ซึ่งคือบั๊กที่ #95 มาแก้)
  //   ⚠️ พิสูจน์แล้ว 2026-08-10: ไม่มี .menu-fixed ในลิสต์นี้ → รายงาน "opt ทับ drawer" 2 จุด
  //      ทุก feature ที่มี combobox ในลิ้นชัก (= เกือบทุกตัว ตาม Rule #94)
  const SEL_OK = SEL + ', .toast, .menu-fixed, #overlay-root';
  const out = [], overlays = [...document.querySelectorAll(SEL)].filter(o => {
    const r = o.getBoundingClientRect(), cs = getComputedStyle(o);
    return r.width > 40 && r.height > 40 && cs.visibility !== 'hidden' &&
           parseFloat(cs.opacity) > 0.05 && cs.pointerEvents !== 'none';
  });
  if (!overlays.length) return out;
  const seen = new Set();
  overlays.forEach(ov => {
    const r = ov.getBoundingClientRect();
    // ยิงเป็นตารางทุก 32px แนวตั้ง × 3 คอลัมน์ — ของที่โผล่เหนือ overlay ต้องอยู่ใน SEL_OK เท่านั้น
    // ⚠️ เดิมยิงแค่ 8 จุดที่สัดส่วนคงที่ (.06/.3/.6/.94) → แถวห่างกัน ~228px บนลิ้นชักเต็มจอ
    //    พิสูจน์แล้ว 2026-08-10: เมนูสูง 116px หลุดทั้งตัวเพราะตกในช่องว่างระหว่างแถวพอดี
    //    (บทเรียนเดียวกับข้อ 1c ที่ยิงทุก 16px — สุ่มหยาบไปพลาดของที่ทับเป็นแถบบาง ๆ)
    const pts = [];
    for (let y = r.top + 6; y < r.bottom - 4; y += 32)
      for (const x of [r.left + r.width*0.2, r.left + r.width*0.5, r.left + r.width*0.8]) pts.push([x, y]);
    pts.forEach(([x, y]) => {
      if (x < 1 || y < 1 || x > innerWidth-1 || y > innerHeight-1) return;
      const top = document.elementFromPoint(x, y);
      if (!top || top === ov || ov.contains(top)) return;
      if (top.closest(SEL_OK)) return;
      const cs = getComputedStyle(top);
      const key = (top.className || top.tagName).toString().slice(0,30) + '|' +
                  (ov.className || ov.tagName).toString().slice(0,20);
      if (seen.has(key)) return; seen.add(key);
      out.push({ over: (ov.className||ov.tagName).toString().slice(0,24),
                 ovz: getComputedStyle(ov).zIndex,
                 by: (top.className||top.tagName).toString().slice(0,30),
                 pos: cs.position, z: cs.zIndex });
    });
  });
  return out;
}
"""

# ⭐ เพิ่ม 2026-09-02 (F-HR-RECRUIT) — ผู้ใช้เจอ modal โดน drawer ทับ "ทุกอัน"
#
# สาเหตุจริง: BASE-KIT ให้ .modal-backdrop = var(--z-backdrop) 50 แต่ .drawer = var(--z-drawer) 55
# → เปิด modal จากในลิ้นชัก (confirm/reason/interview/DOA) modal จมใต้ drawer ทุกครั้ง
#
# ทำไม JS_OVERLAY_STACK เดิมมองไม่เห็น: มันใส่ overlay "ทุกชนิด" ไว้ใน SEL_OK (drawer/modal/backdrop)
# เพื่อกัน false-positive ของ menu-fixed → ผลคือ "drawer วาดทับ modal" ถูกนับว่า OK เงียบ ๆ
# ตัวนี้จึงตรวจ invariant เฉพาะ: ถ้า modal + drawer เปิดพร้อมกัน → modal z ต้อง > drawer z เสมอ
JS_MODAL_UNDER_DRAWER = """
() => {
  const vis = el => { const r=el.getBoundingClientRect(), cs=getComputedStyle(el);
    return r.width>40 && r.height>40 && cs.visibility!=='hidden' &&
           parseFloat(cs.opacity)>0.05 && cs.pointerEvents!=='none'; };
  const zi = el => { const z=parseInt(getComputedStyle(el).zIndex,10); return isNaN(z)?0:z; };
  const drawers = [...document.querySelectorAll('.drawer')].filter(vis);
  const modals  = [...document.querySelectorAll('.modal-backdrop')].filter(vis);
  if(!drawers.length || !modals.length) return [];
  const dzMax = Math.max(...drawers.map(zi));
  const topDrawer = drawers.find(d=>zi(d)===dzMax) || drawers[0];
  const out=[];
  modals.forEach(mc=>{
    const mz = zi(mc);
    if(mz <= dzMax){
      const r = mc.getBoundingClientRect();
      const hit = document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
      out.push({ mz:String(mz), dz:String(dzMax),
        modal:(mc.className||mc.tagName).toString().slice(0,24),
        drawer:(topDrawer.className||topDrawer.tagName).toString().slice(0,20),
        centerHit: hit ? (hit.className||hit.tagName).toString().slice(0,30) : 'none' });
    }
  });
  return out;
}
"""

# CSS var ที่ใช้แต่ไม่มีใครประกาศ — ต้นตอชั้นลึกของเคสข้างบน
# ตรวจแบบ static จับได้ทุกตัวแปร ไม่ใช่แค่ z-index (สี/ระยะ/ฟอนต์ก็หายเงียบแบบเดียวกันได้)
JS_CSSVAR = """
() => {
  const css = [...document.querySelectorAll('style')].map(s => s.textContent).join('\\n');
  const declared = new Set([...css.matchAll(/(--[\\w-]+)\\s*:/g)].map(m => m[1]));
  const used = new Set([...css.matchAll(/var\\((--[\\w-]+)/g)].map(m => m[1]));
  return [...used].filter(v => !declared.has(v));
}
"""

# ⭐ กดได้แต่ไม่มีอะไรบอกว่ากดได้ (เพิ่ม 2026-08-05)
#
# ที่มา: F-COA-001 เขียนการ์ดสรุปเป็น
#   '<div class="stat" '+(onclick?'class="cell-click" onclick="..."':'')+'>'
# → ใน 1 แท็กมี class= สองครั้ง เบราว์เซอร์เก็บอันแรกทิ้งอันหลังเงียบ ๆ
#   ผลคือ onclick ติด (กดได้จริง) แต่ cell-click หลุด → ไม่มี cursor:pointer
#   = การ์ดกรองได้แต่ผู้ใช้ไม่มีทางรู้ · วัดแล้ว 3 ใน 5 ใบเป็นแบบนี้
#
# ทำไมตัววัดเดิมมองไม่เห็น:
#   · JS_A11Y_REACH ถามว่า "กดได้แต่คีย์บอร์ดไปถึงมั้ย" — การ์ดนี้ตอบว่าไปไม่ถึง (จับได้)
#     แต่ถ้าเผลอใส่ tabindex ให้ ก็จะเงียบทันทีทั้งที่ยังมองไม่ออกว่ากดได้
#   · JS_GHOST_CLASS ถามว่า "class ที่ใช้มีนิยามใน CSS มั้ย" — cell-click มีนิยาม
#     แค่ไม่เคยติดกับ element จริง จึงไม่ถูกจับ
#   · self_audit เทียบข้อความ ไม่ได้ประกอบ DOM จึงไม่เห็น attribute ที่ถูกทิ้ง
# ข้อนี้ถามตรง ๆ ว่า "ของที่มี onclick มี cursor:pointer มั้ย" — ครอบทุกสาเหตุ
JS_AFFORDANCE = """
() => {
  const NATIVE = new Set(['BUTTON', 'A', 'INPUT', 'SELECT', 'TEXTAREA', 'LABEL', 'SUMMARY', 'OPTION']);
  const OK = new Set(['pointer', 'help', 'text', 'not-allowed', 'grab', 'grabbing', 'move']);
  const out = [];
  document.querySelectorAll('[onclick]').forEach(el => {
    if (NATIVE.has(el.tagName)) return;
    if (el.closest('button, a, label')) return;
    // FP#5 เดิม — ฉากหลัง overlay (backdrop) เป็นพื้นที่กดปิด ไม่ใช่ปุ่มที่ต้องมีสัญญาณ
    if (/backdrop|overlay-bg|scrim/.test(el.className || '')) return;
    // FP#4 เดิม — onclick ที่เป็น "ตัวกันคลิกทะลุ" ล้วน ๆ ไม่ใช่ action ของผู้ใช้
    //   ครอบทั้งแบบเขียนสด และแบบเรียกผ่านตัวช่วยกลาง stopEvt(event) ซึ่งจำเป็นต้องมี
    //   เพราะ self_audit.py นับ stopPropagation ดิบเกิน 3 จุด = "เหมา" (Rule #68)
    //   — ต้องแก้คู่กับ JS_A11Y_REACH เสมอ ไม่งั้นไฟล์ที่ทำถูกจะถูกฟ้องซ้ำ (2026-08-05)
    const h = (el.getAttribute('onclick') || '').replace(/\\s|;/g, '');
    if (/^(event\\.stopPropagation\\(\\)|e\\.stopPropagation\\(\\)|stopEvt\\(event\\))$/.test(h)) return;
    const r = el.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) return;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') return;
    if (OK.has(cs.cursor)) return;
    out.push({
      tag: el.tagName.toLowerCase(),
      cls: (el.className || '').toString().slice(0, 40),
      cursor: cs.cursor,
      txt: (el.innerText || '').trim().replace(/\\s+/g, ' ').slice(0, 34)
    });
  });
  return out.slice(0, 12);
}
"""

# FP#6 ข้อความจาก CDN ภายนอก — ไม่ใช่ข้อบกพร่องของไฟล์
EXTERNAL = ('fontshare', 'googleapis', 'gstatic', 'downloadable font',
            'unpkg', 'jsdelivr', 'cdnjs', 'failed to load resource')


def is_external(txt):
    """ข้อความ console ที่มาจาก CDN ภายนอก ไม่ใช่โค้ดในไฟล์

    `Suite` กับ `Audit` แยกของพวกนี้ออกอยู่แล้ว แต่ `render-gate.py` ของแต่ละ feature
    นับรวมหมดแล้ว exit 1 — พอ Google Fonts/Fontshare ตอบ 500 ชั่วคราว (เกิดจริง 2026-08-06)
    ด่านจะแดงทั้งที่ไฟล์ไม่ได้พัง · เปิดให้ render-gate เรียกใช้ตัวเดียวกันได้
    """
    return any(k in str(txt).lower() for k in EXTERNAL)


class Audit:
    """ตัวตรวจกลาง — feature เขียนแค่ walk_layout / walk_behavior แล้วส่งเข้ามา"""

    def __init__(self, html_path, argv=None):
        argv = argv if argv is not None else sys.argv
        self.html = pathlib.Path(html_path).resolve().as_uri()
        quick = '--quick' in argv

        def arg(name, default):
            for a in argv:
                if a.startswith(name + '='):
                    return a.split('=', 1)[1].split(',')
            return default

        # ความกว้าง (ปรับ 2026-08-10 ตาม html-generator-v8 Rule #97)
        #   v8 มี 2 โหมด: 768–1180 adaptive (sidebar off-canvas) · ≥1180 เต็มรูป
        #   เดิม 1280/1440/1920/2560 = ตัวอย่างของ "เต็มรูป" ทั้ง 4 ตัว → โหมด adaptive ไม่เคยถูกแตะ
        #   ใหม่: 1024 (adaptive) · 1280 (เต็มรูปที่คับที่สุด — ของล้นเกิดตรงนี้) · 1920 (จอกว้าง)
        #   ตัด 2560 (เหนือ 1180 ได้แค่ที่ว่างเพิ่ม) และ 1440 (โหมดเดียวกับ 1280 แต่หลวมกว่า)
        self.widths = [int(x) for x in arg('--widths', ['1024', '1280'] if quick else ['1024', '1280', '1920'])]
        self.browsers = arg('--browsers', ['chromium'])
        self.layout_only = '--layout-only' in argv
        self.issues, self.notes, self.runtime = [], [], []

    # ── บันทึกผล ──
    def add(self, dim, scene, kind, detail):
        self.issues.append({'dim': dim, 'scene': scene, 'kind': kind, 'detail': detail})

    # ── ของที่ลงทะเบียนไว้แล้วในทะเบียน design system ──
    @staticmethod
    def _known_rules():
        """อ่านบล็อก ```known-findings จาก _SHARED/DESIGN_SYSTEM_PENDING.md

        คืน [(dim, kind_sub, [detail_sub, …]), …] · ไม่มีไฟล์/ไม่มีบล็อก = ไม่กรองอะไรเลย
        ทะเบียนเป็น source of truth ตัวเดียว — ห้าม hardcode รายการไว้ในไฟล์นี้

        ช่อง detail คั่นด้วย `&&` ได้ = ต้องเจอทุกชิ้น (ใช้ตอนชิ้นเดียวกว้างเกินไป
        เช่น ขาว rgb(255,255,255) ต้องพ่วง ratio ด้วย ไม่งั้นกลืนของจริงที่ไม่เกี่ยว)
        """
        f = pathlib.Path(__file__).resolve().parent.parent / 'DESIGN_SYSTEM_PENDING.md'
        if not f.exists():
            return []
        rules, inside = [], False
        for ln in f.read_text(encoding='utf-8').splitlines():
            s = ln.strip()
            if s.startswith('```known-findings'):
                inside = True; continue
            if inside and s.startswith('```'):
                break
            if not inside or not s or s.startswith('#'):
                continue
            parts = [p.strip() for p in s.split('|')]
            if len(parts) == 3 and all(parts):
                subs = [x.strip() for x in parts[2].split('&&') if x.strip()]
                rules.append((parts[0], parts[1], subs))
        return rules

    def _split_known(self):
        """แยก issues เป็น (ของใหม่, ที่ลงทะเบียนแล้ว)"""
        rules = self._known_rules()
        if not rules:
            return self.issues, []
        fresh, known = [], []
        for i in self.issues:
            hit = any(d == i['dim'] and k in i['kind'] and all(t in i['detail'] for t in subs)
                      for d, k, subs in rules)
            (known if hit else fresh).append(i)
        return fresh, known

    # ── ตัวช่วยที่ walk เรียกใช้ ──
    def scan(self, pg, scene):
        """วัดเรขาคณิตของฉากปัจจุบัน"""
        try:
            r = pg.evaluate(JS_LAYOUT)
        except Exception as e:
            self.add('1 Layout', scene, 'ตรวจไม่สำเร็จ', str(e)[:90]); return
        # ⭐ ของที่วาดทับ overlay ที่เปิดอยู่ (sticky header / shell bar ทะลุลิ้นชัก)
        try:
            for x in pg.evaluate(JS_OVERLAY_STACK):
                self.add('1 Layout', scene, 'ของอื่นวาดทับลิ้นชัก/หน้าต่างที่เปิดอยู่',
                         f"{x['by']} (position:{x['pos']} z:{x['z']}) ทับ {x['over']} (z:{x['ovz']})")
        except Exception as e:
            self.add('1 Layout', scene, 'ตรวจการซ้อนของ overlay ไม่สำเร็จ', str(e)[:90])
        # ⭐ modal เปิดพร้อม drawer → modal ต้องเหนือ drawer (F-HR-RECRUIT 2026-09-02)
        try:
            for x in pg.evaluate(JS_MODAL_UNDER_DRAWER):
                self.add('1 Layout', scene, 'modal เปิดอยู่แต่จมใต้ลิ้นชัก (z ≤ drawer)',
                         f"modal {x['modal']} (z:{x['mz']}) ≤ drawer {x['drawer']} (z:{x['dz']}) · จุดกลางโดน {x['centerHit']}")
        except Exception as e:
            self.add('1 Layout', scene, 'ตรวจ modal เหนือลิ้นชักไม่สำเร็จ', str(e)[:90])
        # ⭐ CSS var ที่ใช้แต่ไม่ประกาศ — ตรวจครั้งเดียวพอ (เป็นคุณสมบัติของไฟล์ ไม่ใช่ของฉาก)
        if not getattr(self, '_cssvar_done', False):
            self._cssvar_done = True
            try:
                miss = pg.evaluate(JS_CSSVAR)
                if miss:
                    self.add('1 Layout', 'ทั้งไฟล์', 'CSS var ที่ใช้แต่ไม่มีใครประกาศค่า (คุณสมบัติเงียบหาย)',
                             ' · '.join(miss[:12]))
            except Exception as e:
                self.add('1 Layout', 'ทั้งไฟล์', 'ตรวจ CSS var ไม่สำเร็จ', str(e)[:90])
        for x in r['clipped']:
            self.add('1 Layout', scene, 'ถูกกล่องแม่ตัด', f"{x['el']} ถูก {x['by']} ตัด {x['cut']}px")
        for x in r['hscroll']:
            self.add('1 Layout', scene, 'scroll แนวนอนไม่ตั้งใจ', f"{x['el']} เนื้อหาเกินกล่อง {x['over']}px (กล่อง {x['w']}px)")
        for x in r['rowMix']:
            self.add('1 Layout', scene, 'สูงไม่เท่ากันในแถวเดียว', f"{x['row']} → {' · '.join(x['heights'])}")
        for x in r['textOverflow']:
            self.add('1 Layout', scene, 'ข้อความล้นกล่อง', f"{x['el']} “{x['txt']}” ล้น {x['over']}px")
        for x in r['overlap']:
            self.add('1 Layout', scene, 'element ซ้อนทับกัน', f"{x['box']}: {x['a']} ทับ {x['b']} {x['ox']}×{x['oy']}px")
        for x in r.get('cellOverflow', []):
            self.add('1 Layout', scene, 'เนื้อหาล้นออกนอกเซลล์ตาราง',
                     f"{x['el']} กว้าง {x['elW']}px ในเซลล์ {x['cellW']}px → ล้น {x['over']}px")
        for x in r.get('rowTopMix', []):
            self.add('1 Layout', scene, 'ช่องกรอกในแถวไม่อยู่แนวเดียวกัน', ' · '.join(x['items']))
        for x in r.get('menuCovered', []):
            self.add('1 Layout', scene, 'เมนูที่กางอยู่ถูกของอื่นวาดทับ', f"{x['menu']} ถูก {x['by']} ทับ")
        for x in r.get('deadStyle', []):
            self.add('1 Layout', scene, 'ค่าที่ตั้งใน CSS ไม่มีผลเพราะ element เป็น inline',
                     f"{x['el']} → {x['props']} · “{x['txt']}”")
        for x in r.get('iconFlush', []):
            self.add('1 Layout', scene, 'ไอคอนชนตัวอักษร (ไม่มีช่องไฟ)',
                     f"{x['el']} “{x['txt']}” ห่างแค่ {x['gap']}px")
        for x in r.get('stackFlush', []):
            self.add('1 Layout', scene, 'ก้อนเนื้อหาติดกันในแนวตั้ง (ไม่มีจังหวะ)',
                     f"[{x['stack']}] {x['a']} → {x['b']} ห่างแค่ {x['gap']}px")
        for x in r.get('headMisplaced', []):
            self.add('1 Layout', scene, 'หัวลิ้นชัก/หน้าต่าง: ปุ่มปิดไม่อยู่ขวาสุดแถวเดียวกับหัวข้อ',
                     f"{x['head']} → {x['kind']} ({x['detail']})")
        for x in r.get('ghostCtl', []):
            self.add('1 Layout', scene, 'ตัวควบคุมมองไม่เห็น (มักเกิดจากใช้ class ที่ไม่มีนิยามใน CSS)',
                     f"{x['el']} ขนาด {x['w']}×{x['h']}px")
        # ⭐ กดได้แต่ไม่มีสัญญาณว่ากดได้ — มัก
        # เกิดจาก class หลุด (เช่นเขียน class= ซ้ำในแท็กเดียว เบราว์เซอร์ทิ้งอันหลัง)
        try:
            for x in pg.evaluate(JS_AFFORDANCE):
                self.add('1 Layout', scene, 'กดได้แต่ไม่มีอะไรบอกว่ากดได้ (cursor ไม่ใช่ pointer)',
                         f"<{x['tag']} class=\"{x['cls']}\"> cursor:{x['cursor']} · “{x['txt']}”")
        except Exception as e:
            self.add('1 Layout', scene, 'ตรวจสัญญาณว่ากดได้ไม่สำเร็จ', str(e)[:90])
        try:
            for x in pg.evaluate(JS_GHOST_CLASS):
                self.add('1 Layout', scene, 'ใช้ class ที่ไม่มีนิยามใน CSS (สไตล์ไม่ถูกใช้จริง)',
                         f"<{x['tag']}> class=\"{x['cls']}\"")
        except Exception as e:
            self.add('1 Layout', scene, 'ตรวจ class ไม่สำเร็จ', str(e)[:90])
        try:
            tips = pg.evaluate(JS_TIP)
        except Exception as e:
            self.add('1 Layout', scene, 'ตรวจคำอธิบายไม่สำเร็จ', str(e)[:90]); return
        for x in tips:
            what = f"“{x['txt']}” (กว้าง {x['w']}px)"
            if x['kind'] == 'cut':
                self.add('1 Layout', scene, 'คำอธิบายตอนชี้ถูกกล่องแม่ตัด',
                         f"{what} ถูก {x['by']} ตัด {x['px']}px — เลื่อนไปดูไม่ได้")
            elif x['kind'] == 'missing':
                self.add('1 Layout', scene, 'ชี้ ⓘ แล้วไม่มีคำอธิบายโผล่', f"“{x['txt']}” มีข้อความแต่ไม่มีกล่องให้เห็น")
            else:
                self.add('1 Layout', scene, 'คำอธิบายตอนชี้ล้นออกนอกจอ', f"{what} ล้น {x['px']}px")

    def closes_cleanly(self, pg, open_modal_js, scene='ลำดับการปิด'):
        """ปิดหน้าต่างยืนยันแล้วปิดลิ้นชักติดกัน — ทั้งคู่ต้องหายจริง

        ชุดพื้นฐานหน่วง 200-280ms ก่อนตั้งสถานะว่าปิดแล้ว ถ้ามีอะไรสั่งวาดจอในช่วงนั้น
        จอจะอ่านว่า "ยังเปิดอยู่" แล้ววาดกลับมาค้างถาวร กดอะไรไม่ได้ทั้งจอ
        เจอจริงกับใบเปรียบเทียบราคา 2026-08-04 (การปิดลิ้นชักสั่งวาดจอทันทีเพื่อคืนเส้นทาง)
        ตัววัดเดิมจับได้แค่ทางอ้อม — ฉากถัดไป click timeout ซึ่งไม่บอกว่าอะไรบัง
        """
        pg.evaluate(open_modal_js); pg.wait_for_timeout(550)
        if not pg.eval_on_selector('#modalBackdrop', "e => e.classList.contains('is-open')"):
            self.add('4 Behavior', scene, 'สั่งเปิดหน้าต่างยืนยันแล้วไม่เปิด', open_modal_js[:50]); return
        pg.evaluate("closeModal(); closeDrawer()"); pg.wait_for_timeout(700)
        stuck = pg.evaluate("""(function(){
          var out = [], vw = window.innerWidth, vh = window.innerHeight;
          ['modalBackdrop', 'drawerBackdrop', 'drawer'].forEach(function(id){
            var el = document.getElementById(id); if (!el) return;
            var cs = getComputedStyle(el), r = el.getBoundingClientRect();
            if (cs.visibility === 'hidden' || cs.display === 'none') return;
            if (parseFloat(cs.opacity || '1') < 0.05) return;
            if (cs.pointerEvents === 'none') return;
            if (r.left >= vw || r.top >= vh || r.right <= 0 || r.bottom <= 0) return;  // เลื่อนออกนอกจอแล้ว
            out.push(id + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
          });
          return out;
        })()""")
        for x in stuck:
            self.add('4 Behavior', scene,
                     'ปิดหน้าต่างยืนยันแล้วปิดลิ้นชักติดกัน → ของค้างทับจอ กดอะไรไม่ได้', x)

    def rows_same_height(self, pg, selector, scene, label):
        """ตรวจความสูงของ control ในแถวที่ระบุเอง"""
        for r in pg.evaluate(JS_LAYOUT)['rowMix']:
            self.add('1 Layout', scene, label, json.dumps(r['heights'], ensure_ascii=False))

    @staticmethod
    def pick(pg, key, query, idx=0):
        """เลือกค่าในช่องค้นหาแบบ search-select ของ kit"""
        pg.click(f"#ss-input-{key}", timeout=8000); pg.wait_for_timeout(200)
        pg.fill(f"#ss-input-{key}", query); pg.wait_for_timeout(300)
        pg.query_selector_all(f"#ss-list-{key} .ss-opt")[idx].click(); pg.wait_for_timeout(400)

    def combobox_sweep(self, pg, scene, keys=None):
        """เลือกค่าในเมนูค้นหาทุกช่องที่เห็นอยู่ แล้ววัดว่า "ค่าติดจริง" มั้ย

        เกณฑ์ผ่าน 3 ข้อ: เปิดแล้วเมนูกาง · เลือกแล้วช่องแสดงค่า · เลือกแล้วเมนูปิด

        ⭐ ที่มา (ผู้ใช้เจอเอง 2026-08-05 · F-GLPG-001):
        onSelect ของ combobox ในหน้าต่างเรียก render() ซึ่งวาด overlay ใหม่ทั้งก้อน →
        restoreRenderState คืนโฟกัสให้ช่องเดิม (Rule #29) → การ focus() ยิง onfocus
        → ssOpen() ล้าง query แล้วกางเมนูซ้ำ · ค่าเข้า state แล้วแต่ช่องกลับเป็นว่าง
        ผู้ใช้อ่านว่า "กดแล้วไม่ trigger" ทั้งที่ค่าถูกบันทึกไปแล้ว

        ทำไมตัววัดเดิมมองไม่เห็น: ทุกด้านวัด "ฉากนิ่ง" — scan() ถ่ายภาพเรขาคณิต ณ
        ขณะนั้น · JS_A11Y_REACH ถามว่าโฟกัสได้มั้ย · ไม่มีข้อไหน "เลือกค่าแล้ววัดผล
        หลังเลือก" จึงไม่มีทางเห็น interaction ที่ล้างตัวเองทิ้ง
        """
        # เก็บเฉพาะช่องที่ "กดได้จริง" — overlay ที่ปิดแล้วยังค้างใน DOM (opacity 0 +
        # pointer-events:none) แต่ยังมี rect อยู่ ถ้าไม่กรองจะไปคลิกของที่กดไม่ได้จนหมดเวลา
        found = keys or pg.evaluate("""() => [...document.querySelectorAll('.search-select')]
            .filter(e => {
              const r = e.getBoundingClientRect();
              if (r.width <= 4 || r.height <= 4) return false;
              for (let p = e; p && p !== document.body; p = p.parentElement) {
                const cs = getComputedStyle(p);
                if (cs.display === 'none' || cs.visibility === 'hidden') return false;
                if (cs.pointerEvents === 'none') return false;
                if (parseFloat(cs.opacity || '1') < 0.05) return false;
              }
              return true;
            })
            .map(e => (e.id || '').replace(/^ss-/, '')).filter(Boolean)""")
        for key in found:
            try:
                inp = pg.query_selector(f"#ss-input-{key}")
                if not inp:
                    self.add('4 Behavior', scene, 'ไม่พบช่องค้นหาของเมนูที่ประกาศไว้', key); continue

                def is_open():
                    return pg.eval_on_selector(f"#ss-list-{key}", "e => !e.classList.contains('hidden')")

                def open_menu(why):
                    """คลิกช่องให้เมนูกาง — เผื่อกรณีช่องยังโฟกัสค้างอยู่ (onfocus จะไม่ยิงซ้ำ)"""
                    pg.click(f"#ss-input-{key}", timeout=5000); pg.wait_for_timeout(350)
                    if not is_open():
                        self.add('4 Behavior', scene, 'คลิกช่องค้นหาแล้วเมนูไม่กาง', f'{key} ({why})')
                        return []
                    return pg.query_selector_all(f"#ss-list-{key} .ss-opt")

                opts = open_menu('เปิดครั้งแรก')
                if not opts: continue

                # ⭐ ต้องปิดได้ด้วยการคลิกที่อื่น (Rule #65 ปิดได้ 4 ทาง · Rule #68)
                # ที่มา: overlay ที่กันคลิกทั้งใบด้วย stopPropagation ทำให้ตัวปิดเมนูของ kit
                # (global click) ไม่เห็นคลิกเลย — เมนูเปิดแล้วปิดไม่ได้นอกจากเลือก
                # ผู้ใช้เจอเอง 2026-08-05 · ตัววัดเดิมทดสอบแค่ "เลือกแล้วปิดมั้ย" จึงมองไม่เห็น
                spot = pg.evaluate("""(key) => {
                  const w = document.getElementById('ss-' + key); if (!w) return null;
                  const host = w.closest('.modal, .drawer, .drawer-panel'); if (!host) return null;
                  const t = host.querySelector('.modal-title, .dw-title, .drawer-title'); if (!t) return null;
                  const r = t.getBoundingClientRect();
                  return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2) };
                }""", key)
                if spot:
                    pg.mouse.click(spot['x'], spot['y']); pg.wait_for_timeout(400)
                    if is_open():
                        self.add('4 Behavior', scene,
                                 'เปิดเมนูค้นหาแล้วคลิกที่อื่นไม่ปิด (ปิดได้ทางเดียวคือต้องเลือก)',
                                 f"{key} — มักเกิดจาก stopPropagation เหมาบนกล่อง overlay บัง global click ของ kit")
                    opts = open_menu('เปิดซ้ำหลังคลิกที่อื่น')
                    if not opts: continue

                # ปิดด้วย Esc แล้วต้องเปิดใหม่ได้ (Rule #94 ข้อ 3 + #65)
                pg.keyboard.press('Escape'); pg.wait_for_timeout(350)
                if is_open():
                    self.add('4 Behavior', scene, 'กด Esc แล้วเมนูค้นหาไม่ปิด', key)
                opts = open_menu('เปิดซ้ำหลังกด Esc — ช่องยังโฟกัสค้าง')
                if not opts: continue

                opts[0].click(timeout=5000); pg.wait_for_timeout(450)
                val = pg.eval_on_selector(f"#ss-input-{key}", "e => e.value")
                still_open = pg.eval_on_selector(f"#ss-list-{key}", "e => !e.classList.contains('hidden')")
                if not val:
                    self.add('4 Behavior', scene,
                             'เลือกค่าในเมนูค้นหาแล้วค่าไม่ติด (ช่องยังว่าง)',
                             f"{key} — มักเกิดจาก onSelect วาด overlay ใหม่แล้วโฟกัสเด้งกลับไปเปิดเมนูซ้ำ")
                if still_open:
                    self.add('4 Behavior', scene,
                             'เลือกค่าแล้วเมนูเด้งกางใหม่ (ควรปิดหลังเลือก)', key)
            except Exception as e:
                self.add('4 Behavior', scene, 'ทดสอบเมนูค้นหาไม่สำเร็จ', f'{key}: {str(e).splitlines()[0][:70]}')

        # ⭐ Esc ครั้งที่ 2 ต้องปิด "กล่องแม่" ได้ (เจอที่ F-SCFG-001 · 2026-08-06)
        #
        # ที่มา: `ssOnKey` ของ BASE-KIT เรียก `e.stopPropagation()` ทุกครั้งที่กด Esc ในช่องค้นหา
        # โดยไม่ดูว่าเมนูกางอยู่หรือเปล่า — เจตนาคือกัน Esc ทะลุไปปิดลิ้นชัก (Rule #94 ข้อ 3)
        # แต่ผลข้างเคียงคือ **ตราบใดที่โฟกัสยังค้างอยู่ในช่องค้นหา Esc ครั้งถัดไปก็ถูกกลืนไปด้วย**
        # กล่องแม่จึงปิดด้วยคีย์บอร์ดไม่ได้อีกเลย ต้องเอื้อมไปคลิกปุ่ม X หรือฉากหลังแทน
        #
        # ทำไมตัววัดเดิมมองไม่เห็น: ข้างบนกด Esc **ครั้งเดียว** แล้วเช็คแค่ว่าเมนูปิดมั้ย
        # ซึ่งผ่านเสมอ — อาการจริงเริ่มที่ครั้งที่ 2 · ทำกับ key สุดท้ายตัวเดียวเพราะการทดสอบนี้
        # ปิดกล่องแม่ทิ้ง (ช่องอื่นในกล่องเดียวกันจะหายไปด้วย)
        if found:
            key = found[-1]
            try:
                host = pg.evaluate("""(key) => {
                  const w = document.getElementById('ss-' + key); if (!w) return null;
                  if (w.closest('.modal')) return 'modal';
                  if (w.closest('.drawer')) return 'drawer';
                  return null;
                }""", key)
                sel = {'modal': '#modalBackdrop', 'drawer': '#drawer'}.get(host)
                if sel and pg.query_selector(f"#ss-input-{key}"):
                    pg.click(f"#ss-input-{key}", timeout=5000); pg.wait_for_timeout(350)
                    pg.keyboard.press('Escape'); pg.wait_for_timeout(350)   # ชั้นที่ 1 — ปิดเมนู
                    pg.keyboard.press('Escape'); pg.wait_for_timeout(450)   # ชั้นที่ 2 — ต้องปิดกล่องแม่
                    if pg.eval_on_selector(sel, "e => e.classList.contains('is-open')"):
                        self.add('4 Behavior', scene,
                                 'กด Esc ซ้ำแล้วปิดกล่องแม่ไม่ได้ (คีย์บอร์ดตันอยู่ในช่องค้นหา)',
                                 f"{key} — ssOnKey เรียก stopPropagation ทุกครั้งแม้เมนูปิดแล้ว "
                                 f"ต้องดัก Esc แบบ capture ที่ระดับ feature หรือแก้ให้ stopPropagation เฉพาะตอนเมนูกาง")
            except Exception as e:
                self.add('4 Behavior', scene, 'ทดสอบ Esc ซ้ำไม่สำเร็จ', f'{key}: {str(e).splitlines()[0][:70]}')

    # ── ด้าน 6: เข้าถึงด้วยคีย์บอร์ด · โฟกัส · contrast ──
    def a11y(self, pg, scene='หน้ารายการ', tab_presses=45):
        pg.goto(self.html); pg.wait_for_timeout(1800)
        for el in pg.evaluate(JS_A11Y_REACH):
            self.add('6 A11y', scene, 'คลิกได้แต่คีย์บอร์ดไปไม่ถึง',
                     f"<{el['tag'].lower()} class=\"{el['cls']}\"> “{el['txt']}”")
        seq = []
        for _ in range(tab_presses):
            pg.keyboard.press('Tab'); pg.wait_for_timeout(45)
            seq.append(pg.evaluate("() => { const a = document.activeElement; return a ? a.tagName + '|' + (a.className||'').toString().slice(0,26) : 'none'; }"))
        if len(set(seq)) < 8:
            self.add('6 A11y', scene, 'Tab เดินได้น้อยเกินไป', f"กด Tab {tab_presses} ครั้ง ไปได้ {len(set(seq))} จุด")
        for el in pg.evaluate(JS_FOCUS_RING):
            self.add('6 A11y', scene, 'โฟกัสแล้วไม่เห็นกรอบ',
                     f"<{el['tag'].lower()} class=\"{el['cls']}\"> “{el['txt']}”")
        for c in pg.evaluate(JS_CONTRAST):
            self.add('6 A11y', scene, 'contrast ต่ำกว่า WCAG AA',
                     f"{c['cls']} “{c['txt']}” = {c['ratio']}:1 (ต้อง ≥ {c['need']}) · {c['size']}px {c['color']}")

    # ── เดินทุกเบราว์เซอร์ × ทุกความกว้าง ──
    def run(self, walk_layout, walk_behavior=None, deep=('chromium', 1280)):
        # behavior + a11y รันครั้งเดียวที่คู่ (browser, width) นี้
        # กันพลาด: ถ้าความกว้างของ deep ไม่อยู่ใน self.widths (เช่นผู้ใช้ส่ง --widths เอง)
        # จะไม่มีรอบไหนตรงเลย → walk_behavior/a11y ไม่ถูกเรียกแบบเงียบ ๆ · ตกลงมาที่ตัวกว้างสุดแทน
        if deep[1] not in self.widths and self.widths:
            deep = (deep[0], max(self.widths))
        if deep[0] not in self.browsers and self.browsers:
            deep = (self.browsers[0], deep[1])
        with sync_playwright() as pw:
            for bname in self.browsers:
                try:
                    browser = getattr(pw, bname).launch()
                except Exception as e:
                    self.notes.append(f'{bname}: เปิดไม่ได้ — {str(e).splitlines()[0][:70]}')
                    continue
                for w in self.widths:
                    pg = browser.new_page(viewport={'width': w, 'height': 950})
                    pg.on("console", lambda m, b=bname, w=w: self.runtime.append((b, w, m.type, m.text)) if m.type in ('error', 'warning') else None)
                    pg.on("pageerror", lambda e, b=bname, w=w: self.runtime.append((b, w, 'pageerror', str(e))))
                    pg.on("response", lambda r, b=bname, w=w: self.runtime.append((b, w, 'http' + str(r.status), r.url)) if r.status >= 400 else None)
                    pg.on("requestfailed", lambda r, b=bname, w=w: self.runtime.append((b, w, 'requestfailed', r.url)))
                    pg.goto(self.html); pg.wait_for_timeout(2200)
                    tag = f'{bname} {w}'
                    try:
                        walk_layout(self, pg, tag)
                    except Exception as e:
                        self.add('1 Layout', tag, 'เดินฉากไม่จบ', f'{type(e).__name__}: {str(e).splitlines()[0][:90]}')
                    if (bname, w) == deep and not self.layout_only:
                        if walk_behavior:
                            try:
                                walk_behavior(self, pg)
                            except Exception as e:
                                self.add('4 Behavior', tag, 'เดิน flow ไม่จบ', f'{type(e).__name__}: {str(e).splitlines()[0][:90]}')
                        try:
                            self.a11y(pg)
                        except Exception as e:
                            self.add('6 A11y', tag, 'ตรวจไม่จบ', f'{type(e).__name__}: {str(e).splitlines()[0][:90]}')
                    pg.close()
                browser.close()
        self._fold_runtime()
        return self

    def _fold_runtime(self):
        ext = {}
        for b, w, kind, txt in self.runtime:
            if any(k in txt.lower() for k in EXTERNAL):
                ext[txt[:70]] = ext.get(txt[:70], 0) + 1
                continue
            self.add('5 Runtime', f'{b} {w}', kind, txt[:130])
        for txt, n in list(ext.items())[:4]:
            self.notes.append(f'จาก CDN ภายนอก (ไม่ใช่โค้ดในไฟล์) ×{n}: {txt}')
        if len(ext) > 4:
            self.notes.append(f'… ข้อความจาก CDN ภายนอกอีก {len(ext)-4} แบบ')

    # ── รายงาน ──
    def report(self, exit_on_issue=True, per_kind=12):
        line = '=' * 84
        print(line)
        print(f"เบราว์เซอร์: {', '.join(self.browsers)}  ·  ความกว้าง: {', '.join(map(str, self.widths))}")
        if self.browsers == ['chromium']:
            print("  (cross-browser ปิดอยู่ — เปิดด้วย --browsers=chromium,firefox,webkit)")
        for n in self.notes:
            print('  ! ' + n)
        print(line)
        fresh, known = self._split_known()
        if not fresh:
            print('จุดใหม่ = 0')
        else:
            for dim in sorted({i['dim'] for i in fresh}):
                rows = [i for i in fresh if i['dim'] == dim]
                print(f'\n█ {dim} — {len(rows)} จุด')
                by_kind = {}
                for r in rows:
                    by_kind.setdefault(r['kind'], []).append(r)
                for kind, lst in by_kind.items():
                    print(f'  ✗ {kind} ({len(lst)})')
                    seen = set()
                    for r in lst:
                        if r['detail'] in seen: continue
                        seen.add(r['detail'])
                        if len(seen) > per_kind:
                            print(f'      … อีก {len(lst) - per_kind} รายการ'); break
                        print(f"      [{r['scene']}] {r['detail']}")
        # ของที่ลงทะเบียนใน _SHARED/DESIGN_SYSTEM_PENDING.md แล้ว — แสดงแค่จำนวน ไม่ปนกับของใหม่
        if known:
            kinds = sorted({k['kind'] for k in known})
            print(f'\n▨ ลงทะเบียนแล้ว (ข้าม) — {len(known)} จุด · {", ".join(kinds)}')
            print('   ดู _SHARED/DESIGN_SYSTEM_PENDING.md — รอเจ้าของ design system เคาะ')
        print(line)
        print(f'จุดใหม่ {len(fresh)} จุด' + (f'  ·  ลงทะเบียนแล้ว {len(known)} จุด' if known else ''))
        self.issues = fresh          # exit code + ตัวนับข้างล่างยึด "ของใหม่" เท่านั้น
        if exit_on_issue:
            sys.exit(1 if self.issues else 0)
        return len(self.issues)


class Suite:
    """ตัวรัน E2E — feature เขียนแค่เคสทดสอบ"""

    def __init__(self, title=''):
        self.title = title
        self.results = []
        self.console_errors = []
        self.external = []          # FP#6 — ข้อความจาก CDN ภายนอก ไม่ใช่ข้อบกพร่องของไฟล์

    def _log(self, txt):
        (self.external if any(k in txt.lower() for k in EXTERNAL) else self.console_errors).append(txt)

    def watch(self, pg):
        pg.on("console", lambda m: self._log(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: self._log("pageerror: " + str(e)))

    def check(self, tid, name, fn):
        try:
            self.results.append((tid, name, 'PASS', fn() or ''))
        except AssertionError as e:
            self.results.append((tid, name, 'FAIL', str(e)))
        except Exception as e:
            self.results.append((tid, name, 'ERROR', f'{type(e).__name__}: {e}'.replace('\n', ' ')[:170]))

    def report(self, exit_on_fail=True):
        print('=' * 74)
        for t in self.results:
            print(f"{t[2]:<5} {t[0]}  {t[1]}")
            if t[3]:
                print(f"        {t[3]}")
        ok = sum(1 for t in self.results if t[2] == 'PASS')
        print('=' * 74)
        print(f"ผ่าน {ok}/{len(self.results)} · console errors = {len(self.console_errors)}")
        for e in self.console_errors[:5]:
            print("  !", e)
        if self.external:
            print(f"  (ข้ามข้อความจาก CDN ภายนอก {len(self.external)} รายการ — ไม่ใช่โค้ดในไฟล์)")
        if exit_on_fail:
            sys.exit(0 if ok == len(self.results) and not self.console_errors else 1)
        return ok


# ── รอ "จอนิ่งจริง" แทนการเดาเวลา (เพิ่ม 2026-08-06) ──────────────────────
# เดิมทั้งโปรเจกต์ใช้ wait_for_timeout() 1,231 จุด และ "ไม่มี wait_for_selector เลยสักตัว"
# ทุกจังหวะจึงต้องเผื่อเวลาแบบ worst case → วัดได้ว่า CPU ว่าง ~80% ระหว่างตรวจ
# helper ชุดนี้รอ "เงื่อนไขจริง" แล้วไปต่อทันทีที่พร้อม — ได้ผลเท่าเดิม แต่ไม่นั่งรอเวลาที่เผื่อไว้
#
# ⚠️ ต้องกรอง animation ที่วนไม่รู้จบออก (BASE-KIT มี `pulse 2s infinite` + `spin .8s infinite`)
#    ไม่กรอง = getAnimations() ไม่มีวันว่าง → รอจนหมดเวลาทุกครั้ง ช้ากว่า sleep เดิมอีก

# ⚠️ ข้อที่สอง (สำคัญกว่า): จอหน่วงด้วย **JS timer** ไม่ใช่แค่แอนิเมชัน
#    เช่น setTimeout(finalizeForm, 600) ตอนบันทึก · ตัวปิดลิ้นชัก/หน้าต่างที่เลื่อนเคลียร์ state
#    getAnimations() มองไม่เห็นพวกนี้เลย → ถ้ารอแค่แอนิเมชัน เทสจะอ่านค่าก่อนงานจบ
#    จึงต้อง "นับ timer ที่ค้างอยู่" ด้วย โดย**นับเฉพาะตัวสั้น** (≤ SHORT_TIMER_MS)
#    ตัวยาวคือของที่ตั้งใจให้ค้าง (toast ซ่อนตัวเองที่ 5s) — ไม่ใช่สิ่งที่เทสรอ

SHORT_TIMER_MS = 1500

_JS_PATCH_TIMERS = """
(() => {
  if (window.__uikitTimerPatch) return;
  window.__uikitTimerPatch = true;
  window.__uikitPending = 0;
  const orig = window.setTimeout;
  window.setTimeout = function (fn, ms) {
    const rest = Array.prototype.slice.call(arguments, 2);
    const track = typeof fn === 'function' && (typeof ms !== 'number' || ms <= %d);
    if (track) window.__uikitPending++;
    return orig.apply(window, [function () {
      try { fn.apply(this, arguments); }
      finally { if (track) window.__uikitPending--; }
    }, ms].concat(rest));
  };
})();
""" % SHORT_TIMER_MS

# C3.8 (F-WH-STKADJ 2026-09-14): ดัก native confirm/alert/prompt — ห้ามใช้ ต้องเป็น modal ของแอป (Pattern D)
# บันทึกการเรียกไว้ (ไม่ throw กันไม่ให้ flow ของ feature พังกลางคัน) แล้วให้ assert_no_native_dialog ตัดสิน
_JS_TRAP_NATIVE_DIALOGS = """
(() => {
  if (window.__uikitDialogTrap) return;
  window.__uikitDialogTrap = true;
  window.__NATIVE_DIALOGS = [];
  ['confirm','alert','prompt'].forEach(k => {
    const ret = k === 'confirm' ? true : (k === 'prompt' ? '' : undefined);
    window[k] = function (msg) {
      window.__NATIVE_DIALOGS.push({ kind: k, msg: String(msg == null ? '' : msg).slice(0, 120) });
      return ret;
    };
  });
})();
"""

_JS_ANIM_DONE = """() => {
    if (window.__uikitPending) return false;
    if (!document.getAnimations) return true;
    return document.getAnimations().filter(a => {
        try { return a.effect.getComputedTiming().iterations !== Infinity; }
        catch (e) { return true; }
    }).every(a => a.playState !== 'running');
}"""

_JS_TWO_FRAMES = ("() => new Promise(r => requestAnimationFrame("
                  "() => requestAnimationFrame(r)))")


def settle(pg, timeout=4000):
    """รอจน timer สั้นเดินจบ + แอนิเมชันที่มีวันจบ จบครบ + วาดอีก 2 เฟรม

    ใช้แทน `wait_for_timeout(200–900)` ที่ตามหลังการสั่งอะไรก็ตามที่ทำให้จอขยับ
    """
    try:
        pg.wait_for_function(_JS_ANIM_DONE, timeout=timeout)
    except Exception:
        pass                      # จอไม่นิ่งภายในเวลา — ปล่อยให้ assertion ข้างนอกตัดสิน
    pg.evaluate(_JS_TWO_FRAMES)


# ⚠️ ข้อที่สาม: `document.fonts.ready` **ไม่ได้แปลว่าจัดหน้าเสร็จ**
#    ฟอนต์ไทยมาจาก Google Fonts CDN (ดู CLAUDE.md "ฟอนต์ไทย") — พอไฟล์มาถึง เบราว์เซอร์
#    จัดหน้าใหม่ทั้งหน้า ความกว้างข้อความเปลี่ยน ซึ่งเกิด **หลัง** fonts.ready resolve
#    วัดตอนนั้นได้ค่าจากฟอนต์ fallback → ตัววัด tooltip ฟ้องล้นแบบผี ๆ (เจอจริง: แกว่ง 5↔7 จุด)
#    จึงต้องรอจน "ลายเซ็นของ layout" นิ่ง 2 เฟรมติด ไม่ใช่แค่รอ event ของฟอนต์
_JS_LAYOUT_STABLE = """() => new Promise(res => {
  const sig = () => {
    let s = document.body.scrollHeight + '|' + document.body.scrollWidth;
    const els = document.querySelectorAll('h1,h2,h3,td,th,label,button,.pill,.ph-count');
    const cap = Math.min(els.length, 40);
    for (let i = 0; i < cap; i++) s += '|' + Math.round(els[i].getBoundingClientRect().width);
    return s;
  };
  const a = sig();
  requestAnimationFrame(() => requestAnimationFrame(() => res(a === sig())));
})"""


def ready(pg, url=None, timeout=15000):
    """เปิดหน้าแล้วรอ load + ฟอนต์พร้อม + layout นิ่ง + timer/แอนิเมชันจบ

    ใช้แทน `pg.goto(url); pg.wait_for_timeout(1800–2200)`
    """
    try:
        pg.add_init_script(_JS_PATCH_TIMERS)   # มี guard ในตัว เรียกซ้ำไม่เป็นไร
        pg.add_init_script(_JS_TRAP_NATIVE_DIALOGS)   # C3.8 ดัก native confirm/alert/prompt
    except Exception:
        pass
    if url:
        pg.goto(url)
    pg.wait_for_load_state('load')
    pg.evaluate(_JS_PATCH_TIMERS)              # เผื่อหน้าถูกเปิดไปก่อนหน้านี้แล้ว
    pg.evaluate(_JS_TRAP_NATIVE_DIALOGS)       # เผื่อหน้าถูกเปิดไปก่อนหน้านี้แล้ว
    try:
        pg.evaluate("() => document.fonts ? document.fonts.ready : null")
    except Exception:
        pass                      # offline → fallback Thonburi ตามที่ CLAUDE.md ระบุ
    try:
        pg.wait_for_function(_JS_LAYOUT_STABLE, timeout=timeout)
    except Exception:
        pass                      # ไม่นิ่งในเวลา — ปล่อยให้ assertion ข้างนอกตัดสิน
    settle(pg, timeout)


def hush(pg):
    """ดับของที่ "หายเองตามเวลา" ก่อนกดชัตเตอร์ — toast ซ่อนตัวเองที่ 5 วินาที

    ทำไมต้องมี: ตอนใช้ sleep ตายตัว รอบตรวจช้าพอที่ toast จะหายไปเองก่อนถ่าย
    พอเปลี่ยนมาใช้ settle() รอบเร็วขึ้น 5 เท่า → toast ยังค้างอยู่ ภาพเลยต่างจากเดิม 4 ใบ
    (วัดแล้ว: ต่าง 1.66% ที่มุมขวาล่าง `(2346,1723)–(2880,1900)` เหมือนกันทั้ง 4 ใบ)
    ปล่อยไว้ = ภาพขึ้นกับความเร็วเครื่อง ซึ่งเป็นปัญหาเดียวกับที่ animations="disabled" แก้ไป
    """
    pg.evaluate("""() => {
        document.querySelectorAll('#toast, .toast, [role=status]').forEach(
            el => el.classList.remove('is-visible', 'show', 'is-open'));
    }""")


def after(pg, js, timeout=4000):
    """`pg.evaluate(js)` แล้วรอจอนิ่ง — คืนค่าที่ evaluate คืนมาเหมือนเดิม

    ใช้แทนคู่ `pg.evaluate(js); pg.wait_for_timeout(...)` ที่มีเยอะที่สุดในสคริปต์ feature
    """
    out = pg.evaluate(js)
    settle(pg, timeout)
    return out


# ── ตัวช่วยเล็ก ๆ ที่ใช้ซ้ำในทุก feature ──
def n(pg, sel):
    return len(pg.query_selector_all(sel))


def unrendered_visible_icons(pg, root='body'):
    """Return visible Lucide placeholders that were not replaced by SVG.

    A missing/unknown icon name leaves an empty ``<i data-lucide>`` in the UI.
    It still occupies 16×16 px, so geometry checks alone cannot see that the
    user is looking at a blank space.
    """
    return pg.evaluate("""root => {
      const host = document.querySelector(root) || document.body;
      return [...host.querySelectorAll('[data-lucide]:not(svg)')].filter(el => {
        const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none';
      }).map(el => ({name: el.getAttribute('data-lucide') || '', tag: el.tagName,
                    text: (el.closest('button')?.innerText || '').trim().slice(0, 50)}));
    }""", root)


def assert_icons_rendered(pg, root='body'):
    missing = unrendered_visible_icons(pg, root)
    assert not missing, f"visible Lucide icons were not rendered: {missing[:6]}"


JS_HEAD_GEOM = r"""
(a) => {
  const H = document.querySelector(a.head);
  if(!H) return {h: -1, bad: ['ไม่พบหัว overlay: ' + a.head]};
  const R = e => e.getBoundingClientRect(), CS = e => getComputedStyle(e);
  const bad = [];

  for(const rs of a.rows){
    const row = H.querySelector(rs);
    if(!row) continue;
    /* นับเฉพาะลูกที่มองเห็นจริง — ของกว้าง 0 คือถูกซ่อนอยู่ ไม่ใช่ความผิดของ layout */
    const kids = [...row.children].filter(e => R(e).width > 0);
    if(kids.length < 2) continue;

    /* ⚠️ กันสัญญาณหลอก: เส้นคั่น (กว้าง ≤2px เช่น .drawer-header-divider 1×22) ตั้งใจให้
       เตี้ยกว่าปุ่มและจัดกึ่งกลาง → ขอบบนต่างจากปุ่มเสมอ ไม่ใช่การตกบรรทัด · ตัดออกทั้ง ① และ ② */
    const solid = kids.filter(e => R(e).width > 2);

    /* ① ตกบรรทัด — ของในแถวเดียวกันขอบบนต้องตรงกัน (เผื่อ 3px กัน sub-pixel) */
    const tops = solid.map(e => R(e).top);
    const dt = Math.max(...tops) - Math.min(...tops);
    if(tops.length > 1 && dt > 3)
      bad.push('WRAP ' + rs + ' — ตกคนละบรรทัด (ขอบบนต่าง ' + Math.round(dt) + 'px)');

    /* ② สูงไม่เท่ากัน */
    const hs = solid.map(e => +R(e).height.toFixed(1));
    if(hs.length > 1 && Math.max(...hs) - Math.min(...hs) > 2)
      bad.push('H-MIX ' + rs + ' — สูงไม่เท่ากัน ' + [...new Set(hs)].join('/') + 'px');

    /* ③ ทรง/ฟอนต์คนละภาษา — เฉพาะของที่มีข้อความ (ปุ่มไอคอนล้วนไม่นับ ฟอนต์มันสืบทอดมา)
       ⚠️ ห้ามใช้ e.innerText ลอย ๆ — <svg> ของ Lucide เป็น SVGElement ที่ **ไม่มี innerText**
          (undefined.trim() = TypeError) · ใช้ textContent ซึ่งมีทุก Node */
    const worded = solid.filter(e => (e.textContent || '').trim());
    if(worded.length > 1){
      const rad = [...new Set(worded.map(e => CS(e).borderRadius.split(' ')[0]))];
      if(rad.length > 1) bad.push('SHAPE-MIX ' + rs + ' — border-radius ' + rad.join('/'));
      const fs = [...new Set(worded.map(e => CS(e).fontSize))];
      if(fs.length > 1) bad.push('FONT-MIX ' + rs + ' — font-size ' + fs.join('/'));
    }
  }

  /* ④ ข้อความถูกกล่องตัดโดยไม่มี ellipsis = หายเงียบ ผู้ใช้ไม่รู้ว่ายังมีต่อ */
  H.querySelectorAll('*').forEach(e => {
    if(e.children.length || !(e.textContent || '').trim()) return;
    const over = e.scrollWidth - e.clientWidth;
    if(over > 1 && CS(e).textOverflow !== 'ellipsis')
      bad.push('CLIP .' + (e.className || e.tagName) + ' — ข้อความล้น ' + over + 'px แต่ไม่มี ellipsis');
  });
  return {h: +R(H).height.toFixed(1), bad: bad};
}
"""


def head_geom(pg, head='.drawer-header', rows=('.drawer-subtitle', '.drawer-header-actions')):
    """วัดหัวของ overlay ที่เปิดอยู่ 1 ใบ → (ความสูง, [รายการที่ผิด])

    เพิ่มเมื่อ 2026-08-11 หลังผู้ใช้เจอเองว่าหัวลิ้นชัก "เบี้ยว/เละ" ทั้งที่
    qc-ux · qc-coverage · e2e ผ่านหมด — ทั้ง 3 ตัวไม่มีใครวัด getBoundingClientRect
    (ตัวที่วัดคือ `class Audit` ซึ่งถอนออกจาก step 5 ไปแล้ว 2026-08-10)

    จับ 4 อาการที่อ่านโค้ดแล้วมองไม่เห็น:
      WRAP       ของในแถวเดียวกันตกคนละบรรทัด → กล่องยืด ความสูงไม่คงที่ (Rule #35)
      H-MIX      ปุ่ม/ป้ายร่วมแถวสูงไม่เท่ากัน (Pass G ของ qc-ux เขียนไว้แต่ตรวจไม่ได้จริง)
      SHAPE/FONT ป้ายชนิดต่างกันใช้ทรง/ฟอนต์คนละระบบเรียงติดกัน
      CLIP       ข้อความถูกตัดโดยไม่มี ellipsis

    ⚠️ ความสูงต้องเรียกวนหลายเรคคอร์ดแล้วเทียบกันเอง — ใบเดียวบอกไม่ได้ว่าคงที่มั้ย
    """
    r = pg.evaluate(JS_HEAD_GEOM, {'head': head, 'rows': list(rows)})
    return r['h'], r['bad']


def txt(pg, sel):
    el = pg.query_selector(sel)
    return el.inner_text().strip() if el else ''


JS_STEPPER_GEOM = r"""
(sel) => {
  const box = document.querySelector(sel);
  if (!box) { return {bad: ['NO-STEPPER: ไม่พบ ' + sel], n: 0}; }
  /* รับได้ทั้ง 2 ตัวของ kit — .d-stepper/.stepper-item (label ใต้ dot) และ .stepper/.step */
  let items = [...box.querySelectorAll(':scope > .stepper-item')];
  let dotSel = '.stepper-circle', lblSel = '.stepper-label';
  if (!items.length) {
    items = [...box.querySelectorAll(':scope > .step')];
    dotSel = '.step-dot'; lblSel = '.step-label,.step-lbl';
  }
  if (items.length < 2) { return {bad: ['NO-STEPS: มี step ' + items.length + ' ตัว'], n: items.length}; }

  const bad = [], R = e => e.getBoundingClientRect();
  const ws = [], gaps = [], dotW = [];
  items.forEach((it, i) => {
    const d = it.querySelector(dotSel), l = it.querySelector(lblSel);
    if (!d || !l) { bad.push('NO-LABEL: step ' + (i + 1) + ' ไม่มี dot หรือ label'); return; }
    const ri = R(it), rd = R(d), rl = R(l);
    ws.push(Math.round(ri.width)); dotW.push(Math.round(rd.width));
    /* #47.1 ข้อ 4 — label ต้องอยู่ "ใต้" dot ห่างคงที่ 8px */
    if (rl.top < rd.bottom - 1) {
      bad.push('LABEL-SIDE: step ' + (i + 1) + ' label อยู่ข้าง dot ไม่ใช่ใต้ (#47.1 ข้อ 4 ระยะ dot→label 8px)');
    } else {
      gaps.push(Math.round(rl.top - rd.bottom));
    }
    /* label ต้องอยู่กึ่งกลาง dot */
    if (Math.abs((rd.left + rd.width / 2) - (rl.left + rl.width / 2)) > 2) {
      bad.push('OFF-CENTER: step ' + (i + 1) + ' label ไม่ตรงกึ่งกลาง dot');
    }
  });
  /* #47.1 ข้อ 1 — ทุก step กว้างเท่ากันเป๊ะ */
  if (new Set(ws).size > 1) { bad.push('W-MIX: step กว้างไม่เท่ากัน ' + JSON.stringify(ws) + ' (#47.1 ข้อ 1 flex:1 1 0)'); }
  /* #47.1 ข้อ 3 — dot ขนาดเดียวทั้งแถบ (is-current ห้ามขยาย) */
  if (new Set(dotW).size > 1) { bad.push('DOT-MIX: dot ขนาดไม่เท่ากัน ' + JSON.stringify(dotW) + ' (#47.1 ข้อ 3)'); }
  /* #47.1 ข้อ 4 — ระยะ dot→label เท่ากันทุก step */
  if (new Set(gaps).size > 1) { bad.push('GAP-MIX: ระยะ dot→label ไม่เท่ากัน ' + JSON.stringify(gaps) + ' (#47.1 ข้อ 4)'); }
  /* #47.1 ข้อ 2 — เส้นเชื่อมกึ่งกลางแนวตั้งของ dot */
  const first = items[0], fd = first.querySelector(dotSel);
  if (fd) {
    const cs = getComputedStyle(first, '::after');
    const top = parseFloat(cs.top);
    if (cs.content !== 'none' && !isNaN(top)) {
      const want = R(fd).height / 2;
      if (Math.abs(top + parseFloat(cs.height || 0) / 2 - want) > 2) {
        bad.push('LINE-OFF: เส้นเชื่อมไม่กึ่งกลาง dot (top ' + cs.top + ' · ต้อง ~' + want + 'px · #47.1 ข้อ 2)');
      }
    }
  }
  return {bad, n: items.length, widths: ws, gaps, dots: dotW};
}
"""


def stepper_geom(pg, sel='.d-stepper'):
    """วัด stepper ตาม Iron Rule #47.1 → (จำนวน step, [รายการที่ผิด])

    เพิ่มเมื่อ 2026-08-14 หลังผู้ใช้ทักเองจากภาพว่า "ข้อความไม่อยู่ใต้ dot"
    ทั้งที่ self_audit · audit.sh · e2e · render gate ผ่านหมด — ไม่มีใครวัดเรขาคณิตของ stepper

    ต้นเหตุ: kit มี stepper 2 ตัวหน้าตาคนละแบบ (`.stepper/.step` label อยู่ "ข้าง" dot ·
    `.d-stepper/.stepper-item` label อยู่ "ใต้" dot) — หยิบผิดตัวแล้วไม่มีตัววัดไหนทัก
    ทั้งที่ตัวแรกทำ #47.1 ข้อ 1 (กว้างเท่ากัน) และข้อ 4 (dot→label 8px) ไม่ได้เลย

    จับ 6 อาการ: LABEL-SIDE · OFF-CENTER · W-MIX · DOT-MIX · GAP-MIX · LINE-OFF
    """
    r = pg.evaluate(JS_STEPPER_GEOM, sel)
    return r['n'], r['bad']


# ⭐ เพิ่ม 2026-09-03 (F-HR-TRAIN) — ผู้ใช้เจอเอง 2 จุดที่ตัววัดเดิมมองไม่เห็นเลย
#
# (1) การ์ดผู้เรียนหลายคนในแท็บ "อนุมัติ/ค่าใช้จ่าย" ถูก nest ซ้อนกัน (secwrap ใน secwrap)
#     แทนที่จะเป็น sibling ระดับเดียวกัน → อ่านเป็นกล่องเดียวที่เนื้อหาปนกัน
#     ทำไมตัววัดเดิมมองไม่เห็น: JS_LAYOUT "element ซ้อนทับกัน" เทียบเฉพาะพี่น้องใน flex/grid
#     box เดียวกัน · การ์ดที่ nest กัน "ถูกต้องตาม box model" (ลูกอยู่ในพ่อจริง ๆ) จึงไม่นับว่า
#     overlap เลย · ไม่มีข้อไหนถามว่า "การ์ดระดับเดียวกันไป nest กันเองหรือเปล่า"
JS_NESTED_CARDS = r"""
(arg) => {
  const host = document.querySelector(arg.root) || document.body;
  const sel = arg.sel || '.secwrap';
  const out = [];
  host.querySelectorAll(sel).forEach(inner => {
    const r = inner.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;               // ซ่อนอยู่ ไม่นับ
    // การ์ดชนิดเดียวกันที่เป็น "บรรพบุรุษที่ใกล้ที่สุด" = การ nest ที่ไม่ควรเกิด
    let p = inner.parentElement, near = null;
    while (p && p !== host && p !== document.body) {
      if (p.matches(sel)) { near = p; break; }
      p = p.parentElement;
    }
    if (near) out.push({
      outer: (near.className || '').toString().slice(0, 44),
      inner: (inner.className || '').toString().slice(0, 44),
      text: (inner.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 40),
    });
  });
  return out;
}
"""


def nested_cards(pg, root='#drawer', sel='.secwrap'):
    """คืนรายการการ์ด (`sel`) ที่ไป nest อยู่ใน การ์ดชนิดเดียวกันภายใน `root`

    การ์ดระดับเดียวกัน (sibling) ต้อง "แบน" — พอ nest กันจะอ่านเป็นกล่องเดียวที่เนื้อหาปน
    (F-HR-TRAIN 2026-09-03: การ์ดผู้เรียนหลายคนในแท็บอนุมัติซ้อนกัน) · คืน [] = สะอาด
    ปรับ selector ได้ (`.secwrap`, `.card`, …) เผื่อ feature อื่นใช้ container คนละชื่อ
    """
    return pg.evaluate(JS_NESTED_CARDS, {'root': root, 'sel': sel})


# (2) combobox: เลือก option แล้วเมนู "เด้งกางใหม่" (reopen-after-select)
#     ที่มา: onSelect → refocus ช่องค้นหา → onfocus ยิง ssOpen() เปิดเมนูซ้ำ · ผู้ใช้เลือกไม่จบสักที
#     (input โชว์ค่าว่างเพราะ open=true → ssSetText แสดง query แทน label)
#     ทำไมตัววัดเดิมมองไม่เห็น: ทุกด้านวัด "ฉากนิ่ง" — ไม่มีตัวไหน "เลือกค่าแล้ววัดสถานะหลังเลือก"
#     (Audit.combobox_sweep ตรวจแนวนี้ แต่ผูกกับ workflow ของ class Audit + ใช้ wait_for_timeout
#      — ตัวนี้เป็น probe เดี่ยว ให้ Suite E2E เรียกได้ ไม่ต้องพึ่ง class Audit)
JS_COMBO_AFTER_SELECT = r"""
(arg) => {
  const key = arg.key, index = (arg.index == null ? 0 : arg.index);
  const ss = window.__ss || {};
  if (!ss[key]) return { error: 'no-combo:' + key };
  if (typeof ssPick !== 'function') return { error: 'no-ssPick' };
  ssPick(key, index);                                     // render() ของ kit ทำงาน sync ตรงนี้
  const s2 = (window.__ss || {})[key];
  const list = document.getElementById('ss-list-' + key);
  const input = document.getElementById('ss-input-' + key);
  let listHidden = true;
  if (list) {
    const cs = getComputedStyle(list);
    listHidden = list.classList.contains('hidden') || cs.display === 'none' ||
                 cs.visibility === 'hidden' || parseFloat(cs.opacity || '1') < 0.05;
  }
  return {
    open: !!(s2 && s2.open),
    listHidden: listHidden,
    inputValue: input ? input.value : '',
    value: s2 ? (s2.value == null ? null : s2.value) : null,
  };
}
"""


def combobox_state_after_select(pg, key, index=0):
    """เลือก option (`index`) ของ combobox `key` ผ่าน ssPick แล้วคืนสถานะหลังเลือก

    → {open, listHidden, inputValue, value} · ssPick + render() ของ kit ทำงานแบบ sync
    ภายใน evaluate นี้แล้ว จึงอ่านผลได้ทันที (ไม่ต้อง settle ก่อนอ่าน)
    """
    return pg.evaluate(JS_COMBO_AFTER_SELECT, {'key': key, 'index': index})


def assert_combobox_closes_after_select(pg, key, index=0):
    """กันบั๊ก reopen-after-select: เลือกแล้วเมนูต้องปิด + open flag=false + ช่องโชว์ค่าที่เลือก

    (F-HR-TRAIN 2026-09-03 · BUG-02 ที่ ses_course) — คืน state dict ถ้าผ่าน · assert ถ้าพัง
    """
    r = combobox_state_after_select(pg, key, index)
    assert 'error' not in r, f"combobox {key}: {r.get('error')}"
    assert r['open'] is False, f"combobox {key} เลือกแล้ว open ยัง True (เมนูเด้งกางใหม่ — reopen-after-select)"
    assert r['listHidden'] is True, f"combobox {key} เลือกแล้ว list ยังไม่ปิด (reopen-after-select)"
    assert r['inputValue'], f"combobox {key} เลือกแล้วช่องไม่โชว์ค่า (value ไม่ติด/เมนูเด้งเปิดล้าง label)"
    return r


# (3) combobox กาง dropdown "เอง" ตอน overlay เพิ่งเปิด (auto-open on modal open)
#     ที่มา (F-HR-TRAIN 2026-09-03 · BUG-04): trapFocus (Rule #29/#94) auto-focus ช่องแรกของ modal
#     ถ้าช่องแรกเป็น search-select → onfocus ยิง ssOpen() → dropdown กางเองทันทีที่ modal โผล่
#     ผู้ใช้ยังไม่ได้แตะอะไรเลยแต่เมนูเด้งค้างบังเนื้อหา
#     ทำไมตัววัดเดิมมองไม่เห็น: probe เดิมทั้งคู่วัด "หลังผู้ใช้เลือก/interact" (reopen-after-select,
#     combobox_sweep) — ไม่มีตัวไหนถามว่า "พอเปิด overlay ขึ้นมาเฉย ๆ มี combobox ไหนกางเองมั้ย"
#     คืนรายชื่อ key ของ search-select ใน overlay ที่ dropdown กางเอง (open flag=true หรือ list ไม่ hidden)
#     list อาจถูก portal ไป #overlay-root → หาแบบ global ด้วย id · [] = สะอาด
JS_MODAL_COMBO_AUTOOPEN = r"""
(arg) => {
  const rootSel = arg.rootSel || '#modalBackdrop .modal';
  const root = document.querySelector(rootSel);
  if (!root) return { error: 'no-root:' + rootSel };
  const ss = window.__ss || {};
  const out = [];
  root.querySelectorAll('.search-select').forEach(w => {
    const key = (w.id || '').replace(/^ss-/, '');
    if (!key) return;
    const list = document.getElementById('ss-list-' + key);   // portal-safe (global id)
    let listShown = false;
    if (list) {
      const cs = getComputedStyle(list);
      listShown = !list.classList.contains('hidden') && cs.display !== 'none' &&
                  cs.visibility !== 'hidden' && parseFloat(cs.opacity || '1') > 0.05;
    }
    const openFlag = !!(ss[key] && ss[key].open);
    if (openFlag || listShown) out.push({ key: key, openFlag: openFlag, listShown: listShown });
  });
  return out;
}
"""


def modal_autoopens_comboboxes(pg, root_sel='#modalBackdrop .modal'):
    """คืนรายชื่อ combobox ใน overlay ที่ "กาง dropdown เอง" ตอนเพิ่งเปิด (auto-open on modal open)

    (F-HR-TRAIN 2026-09-03 · BUG-04) — trapFocus auto-focus ช่องแรก ถ้าเป็น search-select →
    onfocus ยิง ssOpen เปิดเมนูเองตอน overlay โผล่ · [] = ไม่มีตัวไหนกางเอง (สะอาด)
    ต้องเรียก "หลัง" rAF ของ trapFocus + fix settle แล้ว (เรนเดอร์เสร็จ · ผู้ใช้ยังไม่แตะ)
    """
    r = pg.evaluate(JS_MODAL_COMBO_AUTOOPEN, {'rootSel': root_sel})
    if isinstance(r, dict) and r.get('error'):
        raise AssertionError(f"modal_autoopens_comboboxes: {r['error']}")
    return r


# ⭐ เพิ่ม 2026-09-08 (F-HR-WELFARE) — ผู้ใช้เจอ "NaN" โผล่เป็นข้อความบนจอที่ตัววัดเดิมมองไม่เห็น (§C3.8)
#
# ที่มา: มุมมองสวัสดิการ (benefit-view drawer) แถว "ครอบผู้ติดตาม" เรนเดอร์คำว่า `NaN` ตรง ๆ
#   ต้นเหตุคือ unary `+` หลง (`... + + kv(...)`) บีบสตริง HTML ที่ kv() คืนมาให้เป็น Number → NaN
#   แล้ว NaN ถูก concat กลับเป็นสตริง → ผู้ใช้เห็นคำว่า "NaN" คาช่องค่า
#
# เป็น "คลาส" ของบั๊ก ไม่ใช่จุดเดียว: NaN / undefined / null / [object Object] / Invalid Date
#   รั่วออกมาเป็น **ข้อความที่มองเห็น** เพราะ JS coercion/typo — เรนเดอร์ออกมาปกติทุกอย่าง
#   แต่เนื้อหาเป็นขยะ
#
# ทำไมตัววัดเดิมมองไม่เห็นเลยสักตัว:
#   · self_audit / audit.sh เทียบ "ข้อความต้นฉบับในไฟล์" — คำว่า NaN ไม่ได้อยู่ในซอร์ส
#     มันเกิด "ตอนรันไทม์" จากการคำนวณ จึงไม่มีสตริงให้ grep เจอ
#   · JS_LAYOUT / JS_OVERLAY_STACK / affordance ฯลฯ วัด "เรขาคณิต/พฤติกรรม" ไม่เคยอ่าน
#     "เนื้อความ" ว่าเป็นค่าที่มีความหมายมั้ย — NaN กินพื้นที่ 26px เหมือนข้อความปกติทุกประการ
#   · e2e เดิม assert เฉพาะฟิลด์ที่มันจงใจเช็ค — ช่องที่ไม่ได้ระบุใน assertion รอดสายตาหมด
# ตัวนี้จึงกวาด "text node ที่มองเห็นจริง" ทั้งฉาก แล้วถามตรง ๆ ว่ามี garbage token คา DOM มั้ย
#
# กันสัญญาณหลอก: ข้าม <script>/<style>/<textarea>/<template> · ข้าม node ที่ซ่อน (display/
#   visibility/opacity หรือ Range rect = 0) · จับเป็น "คำเดี่ยว" (\b) ไม่ใช่ substring
#   (เช่น "annuller"/"nullable" ไม่โดน) · มี allowlist opt-in เผื่อข้อความที่ตั้งใจมีคำพวกนี้จริง
JS_GARBAGE_TEXT = r"""
(arg) => {
  const scopeSel = arg && arg.scope;
  const allow = (arg && arg.allow) || [];
  const root = scopeSel ? document.querySelector(scopeSel) : document.body;
  if (!root) return { error: 'no-scope:' + scopeSel };
  // garbage token ที่รั่วเป็นข้อความเพราะ coercion/typo (จับเป็นคำเดี่ยว ไม่ใช่ substring)
  const TOKENS = [
    { re: /\bNaN\b/, name: 'NaN' },
    { re: /\bundefined\b/, name: 'undefined' },
    { re: /\bnull\b/, name: 'null' },
    { re: /\[object Object\]/, name: '[object Object]' },
    { re: /\bInvalid Date\b/, name: 'Invalid Date' },
  ];
  const SKIP_TAGS = new Set(['SCRIPT', 'STYLE', 'TEXTAREA', 'NOSCRIPT', 'TEMPLATE']);
  const hidden = el => {
    for (let p = el; p && p.nodeType === 1; p = p.parentElement) {
      const cs = getComputedStyle(p);
      if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity || '1') < 0.05)
        return true;
    }
    return false;
  };
  const out = [], seen = new Set();
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
  let node;
  while ((node = walker.nextNode())) {
    const t = node.nodeValue || '';
    if (!t.trim()) continue;
    const parent = node.parentElement;
    if (!parent || SKIP_TAGS.has(parent.tagName)) continue;
    if (allow.some(a => t.includes(a))) continue;           // allowlist opt-in
    let visible = !hidden(parent);
    if (visible) {                                           // Range rect กัน node ที่กว้าง/สูง 0
      try {
        const rg = document.createRange(); rg.selectNodeContents(node);
        const r = rg.getBoundingClientRect();
        if (r.width < 1 && r.height < 1) visible = false;
      } catch (e) {}
    }
    if (!visible) continue;
    for (const tok of TOKENS) {
      if (!tok.re.test(t)) continue;
      const key = tok.name + '|' + t.trim().slice(0, 40) + '|' + (parent.className || parent.tagName);
      if (seen.has(key)) continue; seen.add(key);
      out.push({
        token: tok.name,
        text: t.trim().replace(/\s+/g, ' ').slice(0, 60),
        tag: parent.tagName.toLowerCase(),
        cls: (parent.className || '').toString().slice(0, 44),
      });
    }
  }
  return out;
}
"""


def garbage_text_leaks(pg, scope=None, allow=None):
    """คืนรายการ garbage token (NaN/undefined/null/[object Object]/Invalid Date) ที่รั่วเป็น
    "ข้อความที่มองเห็น" บนหน้า/overlay/drawer ปัจจุบัน

    (F-HR-WELFARE 2026-09-08 · §C3.8 — NaN leak ในช่อง "ครอบผู้ติดตาม" ของ benefit-view drawer)
    สแกน text node ที่เรนเดอร์จริงเท่านั้น — ข้าม <script>/<style>/<textarea>, ข้าม node ที่ซ่อน,
    จับเป็นคำเดี่ยว (word boundary) ไม่ใช่ substring · คืน [] = สะอาด

    scope : selector จำกัดขอบเขต (เช่น '#drawer' · '#modalBackdrop .modal') · None = ทั้ง body
    allow : list สตริงที่ยอมให้มี (opt-in) — ข้าม text node ที่มีสตริงนั้นเป็น substring
    """
    r = pg.evaluate(JS_GARBAGE_TEXT, {'scope': scope, 'allow': allow or []})
    if isinstance(r, dict) and r.get('error'):
        raise AssertionError(f"garbage_text_leaks: {r['error']}")
    return r


def assert_no_garbage_text(pg, scope=None, allow=None):
    """assert ว่าไม่มี garbage token (NaN/undefined/null/[object Object]/Invalid Date) รั่วเป็น
    ข้อความบนจอ — คืน [] ถ้าผ่าน · โยน AssertionError พร้อมจุดที่เจอถ้าพัง (F-HR-WELFARE §C3.8)
    """
    leaks = garbage_text_leaks(pg, scope=scope, allow=allow)
    assert not leaks, f"garbage text รั่วเป็นข้อความบนจอ: {leaks[:8]}"
    return leaks


# ⭐ เพิ่ม 2026-09-08 (F-HR-WELFARE) — ผู้ใช้เจอชื่อคนกับตำแหน่ง/แผนกในเซลล์บุคคลชนกันบรรทัดเดียว (§C3.8)
#
# ที่มา: เซลล์บุคคลในรายการคำขอ (.tbl-person) ประกอบด้วย .pmain ที่ห่อ .pn (ชื่อ) และ .pm (ตำแหน่ง·แผนก)
#   .pn / .pm เป็น <span> = inline → ต้องพึ่ง .pmain เป็น flex-direction:column ถึงจะขึ้นบรรทัดใหม่
#   .pmain หล่น display:flex;flex-direction:column ไป → .pn กับ .pm ไหลต่อกันบรรทัดเดียว
#   ("สุนิสา วงศ์ทองนักบัญชี · ฝ่ายบัญชี") ชื่อชนตำแหน่งอ่านเป็นก้อนเดียว
#
# ทำไมตัววัดเดิมมองไม่เห็น:
#   · JS_LAYOUT ข้อ 8 (deadStyle) จับ inline ที่มี margin/width ตายเฉพาะที่ *ตัว inline เอง* ตั้ง style ไว้
#     — เคสนี้ .pn/.pm ไม่ได้ตั้ง margin แนวตั้ง การขึ้นบรรทัดมาจาก "พ่อ" (.pmain) จึงรอด
#   · textOverflow/cellOverflow วัด "ล้นกรอบ" — ที่นี่ไม่ล้น แค่ "อยู่บรรทัดเดียวกัน" ซึ่งไม่มีข้อไหนถาม
#   · rowTopMix เทียบเฉพาะ input/select/button ในแถวตาราง ไม่แตะ span ในเซลล์บุคคล
# ตัวนี้ถามตรง ๆ ว่า "บรรทัดตำแหน่ง (.pm) อยู่ใต้บรรทัดชื่อ (.pn) จริงมั้ย" — meta.top ต้อง ≥ name.bottom
JS_PERSON_CELL_COLLISION = r"""
(arg) => {
  const scopeSel = arg && arg.scope;
  const root = scopeSel ? document.querySelector(scopeSel) : document.body;
  if (!root) return { error: 'no-scope:' + scopeSel };
  const vis = el => { const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden'
           && parseFloat(cs.opacity || '1') >= 0.05; };
  const out = [], seen = new Set();
  root.querySelectorAll('.tbl-person').forEach(cell => {
    if (!vis(cell)) return;
    const nameEl = cell.querySelector('.pn');
    const metaEl = cell.querySelector('.pm');
    if (!nameEl || !metaEl) return;            // ไม่มีบรรทัด meta = ไม่มีอะไรให้ชน
    if (!vis(nameEl) || !vis(metaEl)) return;  // meta ว่าง/ซ่อน ไม่นับ
    const nr = nameEl.getBoundingClientRect();
    const mr = metaEl.getBoundingClientRect();
    if (nr.width < 1 || mr.width < 1) return;
    // meta ต้องเริ่มต่ำกว่าจุดจบของชื่อ (คนละบรรทัด · meta อยู่ใต้ name) — เผื่อ 1px กันปัดเศษ
    if (mr.top < nr.bottom - 1) {
      const name = (nameEl.textContent || '').trim().slice(0, 30);
      const meta = (metaEl.textContent || '').trim().slice(0, 30);
      const key = name + '|' + meta;
      if (seen.has(key)) return; seen.add(key);
      out.push({ name, meta });
    }
  });
  return out;
}
"""


def person_cell_line_collision(pg, scope=None):
    """คืนรายการเซลล์บุคคล (.tbl-person) ที่บรรทัดชื่อ (.pn) กับบรรทัดตำแหน่ง·แผนก (.pm) ชนกัน
    บรรทัดเดียว/ซ้อนกัน — คือ meta.top < name.bottom (meta ไม่ได้อยู่ "ใต้" name)

    (F-HR-WELFARE 2026-09-08 · §C3.8 — .pmain หล่น display:flex;flex-direction:column
    → ชื่อกับตำแหน่งไหลต่อกันบรรทัดเดียว เช่น "สุนิสา วงศ์ทองนักบัญชี · ฝ่ายบัญชี")
    ตรวจเฉพาะเซลล์ที่มองเห็นจริง · คืน [{name, meta}] ของเซลล์ที่ชน · [] = สะอาด

    scope : selector จำกัดขอบเขต (เช่น '#page-content' · '#drawer') · None = ทั้ง body
    """
    r = pg.evaluate(JS_PERSON_CELL_COLLISION, {'scope': scope})
    if isinstance(r, dict) and r.get('error'):
        raise AssertionError(f"person_cell_line_collision: {r['error']}")
    return r


def assert_no_person_cell_collision(pg, scope=None):
    """assert ว่าไม่มีเซลล์บุคคล (.tbl-person) ที่ชื่อกับตำแหน่ง·แผนกชนกันบรรทัดเดียว —
    คืน [] ถ้าผ่าน · โยน AssertionError พร้อมเซลล์ที่ชนถ้าพัง (F-HR-WELFARE §C3.8)
    """
    hits = person_cell_line_collision(pg, scope=scope)
    assert not hits, f"เซลล์บุคคลชื่อ/ตำแหน่งชนบรรทัดเดียว: {hits[:8]}"
    return hits


# ⭐ เพิ่ม 2026-09-09 (F-HR-Performance) — ผู้ใช้เจอ footer ลิ้นชักลอยกลางแผงมีที่ว่างข้างล่าง (§C3.8)
#
# ที่มา (BUG-1): `.drawer` เป็น display:flex;flex-direction:column เต็มความสูง แต่ innerHTML ห่อ
#   header/body/footer ไว้ใน `<div class="drawer-panel">` เดียว — และ `.drawer-panel` ไม่มี layout CSS
#   (มีแค่ .wide override ความกว้างใน media query) → panel ยุบเหลือความสูงเท่าเนื้อหา →
#   `.drawer-body{flex:1}` ขยายไม่ได้ (พ่อไม่ใช่ flex เต็มสูง) → footer ไปเกาะใต้เนื้อหากลางลิ้นชัก
#   มีที่ว่างโล่งข้างล่าง อ่านเป็น "ฟอร์มลอยไม่เต็ม" โดยเฉพาะฟอร์มเนื้อหาสั้น (newCycle)
#   แก้ด้วย: .drawer-panel{ display:flex; flex-direction:column; flex:1 1 auto; min-height:0; }
#
# ทำไมตัววัดเดิมมองไม่เห็น: JS_LAYOUT วัดล้น/ทับ/สูงไม่เท่า — footer ที่ลอยกลางแผง "ไม่ล้น ไม่ทับ"
#   แค่ไม่ได้ถูกดันไปก้นลิ้นชัก · head_geom วัดเฉพาะ "หัว" · ไม่มีข้อไหนถามว่า "footer เกาะก้น
#   ลิ้นชักจริงมั้ย" · เนื้อหาสั้น = ยิ่งมองไม่เห็นเพราะช่องว่างใหญ่ดูเหมือน padding ตั้งใจ
# ตัวนี้ถามตรง ๆ ว่า ระยะจากขอบล่างของ .drawer-footer ถึงขอบล่างของ .drawer เล็ก (≤ tol) มั้ย
JS_DRAWER_FOOTER_GAP = r"""
(arg) => {
  const drawerSel = (arg && arg.drawer) || '.drawer';
  const footerSel = (arg && arg.footer) || '.drawer-footer';
  const vis = el => { const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return r.width > 40 && r.height > 40 && cs.display !== 'none' && cs.visibility !== 'hidden'
           && parseFloat(cs.opacity || '1') >= 0.05; };
  const drawers = [...document.querySelectorAll(drawerSel)].filter(vis);
  if (!drawers.length) return { error: 'no-drawer:' + drawerSel };
  // ลิ้นชักที่เปิดอยู่ (transform เข้าจอแล้ว) — เอาตัวขวาสุดที่เห็นจริง
  const drawer = drawers.find(d => d.classList.contains('is-open')) || drawers[drawers.length - 1];
  const dr = drawer.getBoundingClientRect();
  const foot = [...drawer.querySelectorAll(footerSel)].filter(vis)[0];
  if (!foot) return { error: 'no-footer:' + footerSel };
  const fr = foot.getBoundingClientRect();
  // ช่องว่างใต้ footer จนถึงก้นลิ้นชัก — footer ปักก้น = ค่านี้ ~0 · footer ลอยกลาง = ค่านี้ใหญ่
  return {
    gapBelow: Math.round(dr.bottom - fr.bottom),
    drawerBottom: Math.round(dr.bottom),
    footerBottom: Math.round(fr.bottom),
    drawerHeight: Math.round(dr.height),
    footerTop: Math.round(fr.top),
  };
}
"""


def drawer_footer_gap(pg, drawer_sel='.drawer', footer_sel='.drawer-footer'):
    """คืนระยะช่องว่างใต้ .drawer-footer จนถึงก้น .drawer (px) ของลิ้นชักที่เปิดอยู่

    footer ปักก้นถูกต้อง = gapBelow ~0 · footer ลอยกลางแผง (panel ยุบ) = gapBelow ใหญ่
    คืน dict {gapBelow, drawerBottom, footerBottom, drawerHeight, footerTop} (F-HR-Performance §C3.8)
    """
    r = pg.evaluate(JS_DRAWER_FOOTER_GAP, {'drawer': drawer_sel, 'footer': footer_sel})
    if isinstance(r, dict) and r.get('error'):
        raise AssertionError(f"drawer_footer_gap: {r['error']}")
    return r


def assert_drawer_footer_pinned(pg, drawer_sel='.drawer', footer_sel='.drawer-footer', tol=4):
    """assert ว่า .drawer-footer ปักอยู่ก้น .drawer จริง (ไม่ลอยกลางแผงมีที่ว่างข้างล่าง)

    (F-HR-Performance 2026-09-09 · BUG-1 — .drawer-panel ไม่มี flex layout → panel ยุบ →
    drawer-body ขยายไม่ได้ → footer เกาะใต้เนื้อหากลางลิ้นชัก) · gapBelow ต้อง ≤ tol px
    เรียกตอนเปิดลิ้นชักที่เนื้อหา "สั้น" (เช่น newCycle) จะเห็นชัดสุด · คืน dict ถ้าผ่าน
    """
    r = drawer_footer_gap(pg, drawer_sel=drawer_sel, footer_sel=footer_sel)
    assert r['gapBelow'] <= tol, (
        f"drawer-footer ลอยไม่ปักก้นลิ้นชัก (BUG-1): ช่องว่างใต้ footer {r['gapBelow']}px "
        f"(footerBottom {r['footerBottom']} · drawerBottom {r['drawerBottom']} · "
        f"drawerHeight {r['drawerHeight']}) — .drawer-panel ไม่ได้ fill drawer")
    return r


# ⭐ เพิ่ม 2026-09-09 (F-HR-Performance · FIX-03/FIX-04) — "role-gated absence"
#
# ที่มา: BA gate จับได้ว่าการปิดบังด้วย mask() ปิดแค่ "ตัวเลขคะแนน" — persona พนักงานยังเห็น
#   ปุ่มสอบทาน/PIP/ส่ง* และเห็น decision + Gap ของเพื่อนร่วมงานทุกคน (RESTRICTED leak).
#   ของที่ role หนึ่ง "ต้องไม่เห็น" ต้อง **ไม่อยู่ใน DOM จริง** ไม่ใช่แค่ซ่อน/mask.
#
# ทำไมตัววัดเดิมมองไม่เห็น: JS_LAYOUT/affordance วัดเรขาคณิต · garbage_text วัดขยะ token —
#   ไม่มีตัวไหนถามว่า "สตริงที่ scope นี้ห้ามมี ยังโผล่ใน textContent มั้ย".
# generic reusable: ใช้เช็คปุ่มที่ถูก gate ตามสิทธิ์ (FIX-03) และชื่อ/decision/gap ข้ามคน (FIX-04)
def dom_text_absent(pg, needles, scope=None):
    """คืน list ของ needle (สตริง) ที่ยัง 'พบ' ใน textContent ของ scope — [] = ไม่พบเลย (สะอาด)

    scope : selector จำกัดขอบเขต (เช่น '#page-content' · '#drawer') · None = ทั้ง body
    """
    return pg.evaluate(
        """(arg) => { const root = arg.scope ? document.querySelector(arg.scope) : document.body;
             const t = root ? (root.textContent || '') : '';
             return (arg.needles || []).filter(n => t.indexOf(n) >= 0); }""",
        {"scope": scope, "needles": list(needles)})


def assert_text_absent(pg, needles, scope=None):
    """assert ว่าไม่มี needle ใดปรากฏใน DOM ของ scope — role-gated absence (FIX-03/FIX-04)

    คืน [] ถ้าผ่าน · โยน AssertionError พร้อม needle ที่ยังโผล่ถ้าพัง (F-HR-Performance 2026-09-09)
    """
    found = dom_text_absent(pg, needles, scope=scope)
    assert not found, f"พบข้อความที่ role นี้ไม่ควรเห็นใน DOM (role-gated absence): {found}"
    return found


def assert_no_native_dialog(pg, note=''):
    """C3.8 (F-WH-STKADJ 2026-09-14): assert ว่า flow ไม่เคยเรียก native confirm/alert/prompt

    ต้องใช้ modal ของแอป (Pattern D) เสมอ — native dialog หลุดธีม + ตัววัดเรขาคณิต/e2e ทั่วไปมองไม่เห็น
    (bug จริง: onChangeAdjType / เปลี่ยนคลัง ใช้ confirm() ดิบ — user จับได้ตอน UAT ตัววัดเดิมไม่จับ)
    ต้องเรียกหลังเดินทุก flow ที่มีจุดยืนยัน (เปลี่ยนคลัง/ประเภท · ลบ · ยกเลิก · กลับรายการ) แล้ว
    ทำงานได้ต่อเมื่อเปิดหน้าผ่าน ready() (ซึ่งติดตั้ง trap ให้) — คืน [] ถ้าผ่าน · โยนถ้าพบ
    """
    calls = pg.evaluate("()=>window.__NATIVE_DIALOGS||null")
    assert calls is not None, ("[native-dialog] trap ไม่ถูกติดตั้ง — ต้องเปิดหน้าผ่าน ready() ก่อน"
                               f"{(' · '+note) if note else ''}")
    kinds = [c.get('kind') for c in calls]
    assert not calls, (f"[native-dialog] พบการใช้ native {kinds} — ต้องเป็น modal ของแอป (Pattern D) "
                       f"ไม่ใช่ confirm/alert/prompt{(' · '+note) if note else ''}: {calls[:3]}")
    return f"ไม่มี native confirm/alert/prompt (ใช้ modal ของแอปทั้งหมด){(' · '+note) if note else ''}"


def assert_icon_inside_input(pg, wrap_sel, note=''):
    """C3.8 (F-WH-STKADJ 2026-09-14): assert ไอคอน overlay ในกล่อง search/input ไม่ 'ลอย' ออกนอกช่อง

    bug จริง: ไอคอนวางด้วย CSS selector `.wrap>i{position:absolute}` แต่ Lucide แปลง <i data-lucide>
    เป็น <svg> ตอน render → selector `>i` ไม่แมตช์ svg → ไอคอนหลุด position ลอยออกนอก input.
    ตัววัดเรขาคณิต/overflow เดิมมองไม่เห็น (ไอคอนยังอยู่ในหน้า แค่ผิดตำแหน่ง). fix = selector `>i,>svg`
    หรือ inline style. ตรวจ: center ของไอคอนต้องอยู่ในกรอบ bounding ของ input เดียวกัน.
    คืนข้อความถ้าผ่าน · โยน AssertionError ถ้าไอคอนลอยออกนอก.
    """
    r = pg.evaluate("""sel=>{
      const w=document.querySelector(sel); if(!w) return {err:'no-wrap'};
      const ic=w.querySelector('svg,i[data-lucide]'); const inp=w.querySelector('input,textarea');
      if(!ic||!inp) return {err:'no-icon-or-input'};
      const R=e=>e.getBoundingClientRect();
      const a=R(ic), b=R(inp);
      const cx=a.left+a.width/2, cy=a.top+a.height/2;
      return {inside: cx>=b.left-1&&cx<=b.right+1&&cy>=b.top-1&&cy<=b.bottom+1,
              icx:Math.round(cx),icy:Math.round(cy),
              box:[Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)],tag:ic.tagName};
    }""", wrap_sel)
    assert not r.get('err'), f"[icon-inside-input] {r.get('err')} ที่ {wrap_sel}{(' · '+note) if note else ''}"
    assert r['inside'], (f"[icon-inside-input] ไอคอน ({r['tag']} center {r['icx']},{r['icy']}) ลอยออกนอกกล่อง input "
                         f"{r['box']} — น่าจะ CSS `>i` หลุดหลัง Lucide swap เป็น svg{(' · '+note) if note else ''}")
    return f"ไอคอน overlay อยู่ในกล่อง input ({wrap_sel}){(' · '+note) if note else ''}"


def assert_pop_above_modal(pg, pop_sel, note=''):
    """C3.8 (F-WH-STKADJ 2026-09-16): assert dropdown/popover ที่เปิดใน modal ลอย 'อยู่หน้า' modal คลิกได้จริง

    bug จริง: search dropdown (combobox) ในกล่อง 'ส่งอนุมัติ' z=--z-portal(60) < modal z=--z-modal(70)
    → dropdown เรนเดอร์ 'จมอยู่หลัง' modal → user เห็นว่า 'ไม่มี option ชื่อคน' ทั้งที่ข้อมูลมี (DSP-02).
    ต้องเปิด dropdown ให้มี option แล้วเรียก. เช็คด้วย elementFromPoint ที่ตำแหน่งกลาง option แรก —
    ต้องได้ element ที่เป็นลูกของ pop (ไม่ถูก modal บัง). ตัววัด z-index/overflow เดิมมองไม่เห็น
    (option อยู่ใน DOM + มีขนาด แค่ถูกทับ). คืน dict ถ้าผ่าน · โยนถ้า option ถูกบัง.
    """
    r = pg.evaluate("""sel=>{
      const p=document.querySelector(sel); if(!p) return {err:'no-pop'};
      const opt=p.querySelector('button,[role=option],.opt,a'); if(!opt) return {err:'no-option'};
      const b=opt.getBoundingClientRect();
      if(b.width<1||b.height<1) return {err:'option-zero-size'};
      const cx=b.left+b.width/2, cy=b.top+b.height/2;
      const top=document.elementFromPoint(cx,cy);
      return {covered: !p.contains(top),
              topTag: top?(top.className||top.tagName):'none',
              popZ: getComputedStyle(p).zIndex};
    }""", pop_sel)
    assert not r.get('err'), f"[pop-above-modal] {r.get('err')} ที่ {pop_sel} (ต้องเปิด dropdown ให้มี option ก่อน){(' · '+note) if note else ''}"
    assert not r['covered'], (f"[pop-above-modal] dropdown ({pop_sel} z={r['popZ']}) ถูก modal บัง — "
                              f"element บนสุดที่ option = '{r['topTag']}' ไม่ใช่ลูกของ pop · "
                              f"z ของ pop ต่ำกว่า modal (DSP-02){(' · '+note) if note else ''}")
    return f"dropdown ลอยหน้า modal คลิกได้ ({pop_sel} z={r['popZ']}){(' · '+note) if note else ''}"


def assert_no_scroll_lock_leak(pg, lock_class='is-overlay-open', note=''):
    """C3.8 (F-WH-STKADJ 2026-09-16): assert หลังปิด overlay ทั้งหมด body ไม่ค้าง scroll-lock

    bug จริง: กลับรายการ (doReverse) navigate ไป view drawer ใหม่ 'ก่อน' closeModal + openViewDrawer
    ไม่ release trap ของ drawer เดิม → _trapStack ไม่ balance → body.is-overlay-open ค้าง → scroll ล็อก
    ปิด drawer เท่าไรก็ไม่หลุด. ต้องเรียก 'หลังปิด overlay หมดแล้ว'. เช็ค: body ไม่มี lock class +
    (ถ้ามี window._trapStack) length 0 + overflow ไม่ถูก freeze. ตัววัด z-index/overflow เดิมมองไม่เห็น
    (มันดูตอน 'เปิด' ไม่ถามว่า 'ปิดหมดแล้ว lock หลุดมั้ย'). คืนข้อความถ้าผ่าน · โยนถ้ายังค้าง.
    """
    r = pg.evaluate("""lc=>{
      const hasLock=document.body.classList.contains(lc);
      const ts=(typeof _trapStack!=='undefined'&&_trapStack)?_trapStack.length:null;
      const ov=getComputedStyle(document.body).overflowY;
      return {hasLock, ts, ov};
    }""", lock_class)
    assert not r['hasLock'], (f"[scroll-lock-leak] body ยังมี .{lock_class} หลังปิด overlay — trap stack ค้าง "
                              f"(_trapStack={r['ts']}) → scroll ล็อก (DSP-01){(' · '+note) if note else ''}")
    if r['ts'] is not None:
        assert r['ts'] == 0, (f"[scroll-lock-leak] _trapStack ยังเหลือ {r['ts']} รายการหลังปิด overlay "
                              f"(ต้อง 0){(' · '+note) if note else ''}")
    return f"ไม่มี scroll-lock ค้างหลังปิด overlay (trapStack={r['ts']}){(' · '+note) if note else ''}"


# ⭐ เพิ่ม 2026-09-09 (F-HR-EXPENSE · §C3.8 · user-found bugs ที่ตัววัดเดิมมองไม่เห็น)
# ─────────────────────────────────────────────────────────────────────────────
# BUG-6 (backdrop/overlay ค้างหลังปิด): closeDrawer/closeModal ถอด .is-open + ตั้ง state
#   หลัง timer แต่ไม่ render() → DOM overlay เก่าค้าง + ลิ้นชักที่ปิดแล้ว pointer-events:auto
#   ระหว่าง slide-out → คลิกแรกโดน overlay (ต้องคลิกซ้ำ). ตัววัดเรขาคณิต/z-index เดิมจับไม่ได้
#   เพราะมันดูตอน "เปิด" ไม่ได้ถามว่า "ปิดแล้ว overlay ยังกินคลิกมั้ย".
JS_OVERLAY_CLOSED_NONBLOCK = r"""
() => {
  const bad = [];
  // (1) overlay ที่ปิดแล้ว (ไม่มี .is-open) ต้อง pointer-events:none — deterministic (ไม่ขึ้นกับ transition)
  document.querySelectorAll('.drawer, .drawer-backdrop, .modal-backdrop').forEach(el => {
    if (el.classList.contains('is-open')) return;
    const cs = getComputedStyle(el);
    if (cs.pointerEvents !== 'none') bad.push({ el: el.id || el.className, why: 'pe=' + cs.pointerEvents });
  });
  // (2) คลิกกลางจอต้องไม่ตกบน overlay ที่ปิดแล้ว (ต้องทะลุไปถึงหน้าเพจ)
  const cx = Math.floor(innerWidth / 2), cy = Math.floor(innerHeight / 2);
  const hit = document.elementFromPoint(cx, cy);
  const onClosed = hit && hit.closest &&
    hit.closest('.drawer:not(.is-open), .drawer-backdrop:not(.is-open), .modal-backdrop:not(.is-open)');
  if (onClosed) bad.push({ center: onClosed.id || onClosed.className });
  return { ok: bad.length === 0, bad, centerHit: hit ? (hit.id || hit.className || hit.tagName) : null };
}
"""


def assert_overlay_cleared_after_close(pg, note=''):
    """assert ว่าหลังปิด drawer/modal ไม่มี overlay ที่ปิดแล้วดัก/บังคลิกกลางจอ (BUG-6 · F-HR-EXPENSE)

    เรียก **หลังสั่งปิดแล้ว settle** (after(pg,'()=>closeDrawer()')) — เช็ก 2 อย่าง:
      (1) ทุก .drawer/.drawer-backdrop/.modal-backdrop ที่ไม่มี .is-open ต้อง pointer-events:none
          (deterministic — ตัวจับตัวจริงของ bug: ลิ้นชักปิดแต่ pe:auto ระหว่าง slide-out)
      (2) document.elementFromPoint(กลางจอ) ไม่ตกบน overlay ที่ปิดแล้ว
    คืน dict ถ้าผ่าน · โยน AssertionError ถ้าพัง
    """
    r = pg.evaluate(JS_OVERLAY_CLOSED_NONBLOCK)
    assert r['ok'], (f"overlay ค้างหลังปิด (BUG-6) {note}: {r['bad']} · "
                     f"คลิกกลางจอโดน {r['centerHit']}")
    return r


# BUG-5 (payment card เบียด footer action ปุ่มหลุดจอ): HTML ผิดรูป (SEC() เกิน </div>) ดัน
#   .drawer-footer ออกนอก .drawer-panel → ปุ่ม อนุมัติ/ไม่อนุมัติ/ส่งจ่าย อยู่ต่ำกว่าจอ กดไม่ได้.
#   audit.sh/self_audit นับ token/เรขาคณิตนิ่ง — ไม่ได้ hit-test ว่าปุ่ม footer คลิกได้จริงมั้ย.
JS_FOOTER_ACTIONS_HITTABLE = r"""
(sel) => {
  const root = document.querySelector(sel || '#drawer');
  if (!root) return { ok: false, bad: [{ why: 'no-drawer' }] };
  const foot = root.querySelector('.drawer-footer');
  if (!foot) return { ok: false, bad: [{ why: 'no-footer' }] };
  const bad = [];
  // footer ต้องยังเป็นลูกของ .drawer-panel (ไม่หลุดออกจาก panel เพราะ HTML ผิดรูป)
  if (!foot.closest('.drawer-panel')) bad.push({ why: 'footer-outside-panel' });
  const vh = innerHeight, vw = innerWidth;
  const btns = [...foot.querySelectorAll('.btn')];
  btns.forEach(b => {
    const r = b.getBoundingClientRect();
    const label = (b.textContent || '').replace(/\s+/g, ' ').trim();
    if (r.width < 1 || r.height < 1) { bad.push({ label, why: 'zero-size' }); return; }
    if (r.bottom > vh + 1 || r.top < -1 || r.right > vw + 1 || r.left < -1) {
      bad.push({ label, why: 'offscreen', top: Math.round(r.top), bottom: Math.round(r.bottom) }); return;
    }
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    const el = document.elementFromPoint(cx, cy);
    const hit = !!(el && (el === b || b.contains(el) || (el.closest && el.closest('.btn') === b)));
    if (!hit) bad.push({ label, why: 'covered', hitBy: el ? (el.className || el.tagName) : null });
  });
  // payment/สถานะการจ่าย card ต้องไม่ position:fixed/sticky ทับ footer
  const pay = [...root.querySelectorAll('.sec')].find(s => /สถานะการจ่าย/.test(s.textContent || ''));
  let payPos = null;
  if (pay) { payPos = getComputedStyle(pay).position;
    if (payPos === 'fixed' || payPos === 'sticky') bad.push({ why: 'payment-card-' + payPos }); }
  return { ok: bad.length === 0, bad, btnCount: btns.length, payPos };
}
"""


def assert_footer_actions_hittable(pg, drawer_sel='#drawer', note=''):
    """assert ว่าปุ่ม action ใน .drawer-footer กดได้จริง (hit-test) + payment card ไม่ fixed/sticky (BUG-5)

    เรียกตอนเปิด view drawer ของใบที่มีปุ่ม footer (เช่น pending → อนุมัติ/ไม่อนุมัติ). เช็ก:
      footer ยังอยู่ใน .drawer-panel · ปุ่มทุกตัวอยู่ในจอ + elementFromPoint กลางปุ่มโดนตัวปุ่มเอง ·
      .sec 'สถานะการจ่าย' ไม่ position:fixed/sticky. คืน dict ถ้าผ่าน · โยน AssertionError ถ้าพัง
    """
    r = pg.evaluate(JS_FOOTER_ACTIONS_HITTABLE, drawer_sel)
    assert r['ok'], f"footer action ปุ่มกดไม่ได้/payment card pinned (BUG-5) {note}: {r['bad']}"
    return r


# BUG-3 (wizard stepper เพี้ยน): base-kit .step-dot (variant .stepper-row 30px วงกลมเทา) รั่วทับ
#   STEPH .step-dot (คอลัมน์) → item ได้ height:30/bg grey/border/radius:50% คลุม label. ตัววัด
#   เดิมไม่ได้ตรวจว่า item ของ stepper "ไม่มีกล่องพื้นหลัง/ขอบแปลกปลอม + สูงพอครอบวงกลม+label".
JS_STEPPER_WELL_FORMED = r"""
(sel) => {
  const items = [...document.querySelectorAll(sel + ' .step-dot')];
  if (items.length < 2) return { ok: false, bad: [{ why: 'no-stepper', n: items.length }] };
  const bad = [];
  const widths = items.map(it => Math.round(it.getBoundingClientRect().width));
  items.forEach((it, i) => {
    const cs = getComputedStyle(it);
    const bg = cs.backgroundColor;
    if (!(bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent')) bad.push({ i, why: 'item-bg', bg });
    if (parseFloat(cs.borderTopWidth) > 0.5) bad.push({ i, why: 'item-border', bw: cs.borderTopWidth });
    const dot = it.querySelector('.d');
    if (!dot) { bad.push({ i, why: 'no-circle' }); return; }
    const dr = dot.getBoundingClientRect(), ir = it.getBoundingClientRect();
    if (dr.width < 18 || dr.width > 34) bad.push({ i, why: 'circle-size', w: Math.round(dr.width) });
    // item ต้องไม่ตัด (clip) วงกลม/label — ก้น item ต้องคลุมก้นวงกลม
    if (ir.bottom < dr.bottom - 1) bad.push({ i, why: 'item-clips-circle', ib: Math.round(ir.bottom), db: Math.round(dr.bottom) });
  });
  const wmin = Math.min(...widths), wmax = Math.max(...widths);
  if (wmax - wmin > 4) bad.push({ why: 'uneven-widths', widths });
  return { ok: bad.length === 0, bad, widths };
}
"""


def assert_stepper_well_formed(pg, stepper_sel='#drawer .stepper', note=''):
    """assert ว่า stepper (STEPH .stepper > .step-dot) เรนเดอร์สะอาด — ไม่มี style รั่วจาก base-kit (BUG-3)

    เช็กแต่ละ .step-dot: พื้นหลังโปร่ง · ไม่มีขอบแปลกปลอม · มีวงกลม .d (18–34px) · item ไม่ตัดวงกลม ·
    ทุกขั้นกว้างเท่ากัน (±4px). คืน dict ถ้าผ่าน · โยน AssertionError ถ้าพัง
    """
    r = pg.evaluate(JS_STEPPER_WELL_FORMED, stepper_sel)
    assert r['ok'], f"stepper เรนเดอร์เพี้ยน (BUG-3) {note}: {r['bad']}"
    return r


# BUG-2 (filter row ล้นการ์ด): .filter-row (padding 0) วางตรงใน .card → controls ชิดขอบการ์ด.
#   วัด: control แรก/สุดท้ายในแถว filter ต้องมี gutter จากขอบการ์ด ≥ min (มี padding container).
JS_FILTER_INSIDE_CARD = r"""
(arg) => {
  const card = document.querySelector(arg.card);
  const bar = document.querySelector(arg.filter);
  if (!card || !bar) return { ok: false, bad: [{ why: 'missing', card: !!card, filter: !!bar }] };
  const ctrls = [...bar.querySelectorAll('input, select, button, .input, .fr-grow')];
  if (!ctrls.length) return { ok: false, bad: [{ why: 'no-controls' }] };
  const cr = card.getBoundingClientRect();
  let minLeft = Infinity, minRight = Infinity;
  ctrls.forEach(c => { const r = c.getBoundingClientRect(); if (r.width < 1) return;
    minLeft = Math.min(minLeft, r.left - cr.left); minRight = Math.min(minRight, cr.right - r.right); });
  const bad = [];
  const MIN = arg.min || 8;
  if (minLeft < MIN) bad.push({ why: 'left-gutter', px: Math.round(minLeft) });
  if (minRight < MIN) bad.push({ why: 'right-gutter', px: Math.round(minRight) });
  return { ok: bad.length === 0, bad, leftGutter: Math.round(minLeft), rightGutter: Math.round(minRight) };
}
"""


def assert_filter_inside_card(pg, card_sel='#view .card', filter_sel='#view .filter-bar, #view .filter-row', min_gutter=8, note=''):
    """assert ว่าแถว filter อยู่ในการ์ด มี gutter จากขอบ (ไม่ชิด/ล้นขอบการ์ด) (BUG-2)

    วัด control ที่ซ้าย/ขวาสุดในแถว filter เทียบขอบ .card — ต้องเว้น ≥ min_gutter px ทั้งสองด้าน.
    คืน dict ถ้าผ่าน · โยน AssertionError ถ้าพัง
    """
    r = pg.evaluate(JS_FILTER_INSIDE_CARD, {'card': card_sel, 'filter': filter_sel, 'min': min_gutter})
    assert r['ok'], f"filter row ล้น/ชิดขอบการ์ด (BUG-2) {note}: {r['bad']}"
    return r


# ⭐ เพิ่ม 2026-09-09 (F-HR-EXPENSE) — ผู้ใช้เจอ modal ส่งอนุมัติ (DOA slot picker) auto-pick ผู้อนุมัติให้เอง
#
# ที่มา (Bug A): modal 'ส่งอนุมัติ' เรนเดอร์ combobox 1 ตัวต่อ slot อนุมัติ (slot-0, slot-1, …) เก็บที่
#   state.doaDraft.picks[i]. เดิม initSelects PRE-FILL picks[i] ด้วยผู้อนุมัติที่ระบบแนะนำ → ปุ่มส่ง
#   ENABLED ตั้งแต่เปิด modal ทั้งที่ช่อง slot ดูว่าง → กดส่งได้เลยโดยได้คนที่ "ระบบเลือกให้" ไม่ใช่ที่ผู้ใช้เลือก
#   fix: ไม่ prefill — slot เปิดมาว่างจริง (picks={}), ปุ่ม disabled จนผู้ใช้เลือกครบทุก slot
#
# ทำไมตัววัด/gate เดิมมองไม่เห็น: qc-ux/qc-coverage grep โค้ด ไม่ได้เรนเดอร์แล้วกดจริง ·
#   ตัววัด e2e เดิม (helper รุ่นแรก) กลับ "ยืนยันพฤติกรรม auto-pick" — assert ว่าเปิดมาปุ่ม enabled
#   จึงผ่านตอนบั๊กยังอยู่ · e2e happy path (c_fn07/c_fn13) เรียก doSubmit() โดยไม่แตะ slot ได้เพราะ prefill
#
# ground-truth หลัง fix (ตัววัดนี้ต้อง assert):
#   (1) modal เพิ่งเปิด · ยังไม่แตะ → ปุ่ม DISABLED · picks ไม่มี valid pick · ช่อง slot input ว่าง (ไม่ auto-pick)
#   (2) กดส่งทั้งที่ยังไม่แตะ (ปุ่ม disabled → onclick ไม่ยิง · backstop doSubmit bail) → ไม่ commit
#   (3) เลือกผู้อนุมัติจริงครบทุก slot → ปุ่ม enable → doSubmit commit ได้
# ต้องเรียก "หลัง" เปิด submit modal + render (slot combos init) แล้ว · helper ขับ state เอง (กด+เลือก+doSubmit)
JS_SUBMIT_APPROVER_GATE = r"""
(arg) => {
  const btnId = arg.btnId || 'submitConfirmBtn';
  const btn = () => document.getElementById(btnId) ||
                    document.querySelector('#modalBackdrop .modal-foot .btn-primary');
  const out = { steps: 0, hadBtn: false, hadId: false,
                disabledWhenFresh: null, noAutoPick: null, slotInputsEmpty: null,
                submittedWhileUntouched: null, enabledWhenAllPicked: null,
                submittedWhenAllPicked: null, busy: null, bad: [] };
  if (!(state.modal.open && state.modal.type === 'submit' && state.doaDraft)) {
    out.bad.push({ why: 'submit-modal-not-open' }); return out;
  }
  const doa = resolveDoa((state.doaDraft.grand) || 0);
  out.steps = doa.steps.length;
  const b0 = btn();
  out.hadBtn = !!b0;
  out.hadId = !!document.getElementById(btnId);
  if (!b0) { out.bad.push({ why: 'no-confirm-btn:' + btnId }); return out; }

  // (1) modal เพิ่งเปิด · ผู้ใช้ยังไม่แตะ slot → ปุ่มต้อง DISABLED · ไม่มี auto-pick · ช่องว่างจริง
  out.disabledWhenFresh = b0.disabled === true;
  if (!out.disabledWhenFresh)
    out.bad.push({ why: 'enabled-when-fresh(auto-pick?)', picks: JSON.stringify(state.doaDraft.picks) });
  const picks = state.doaDraft.picks || {};
  const anyPrefilled = doa.steps.some((s, i) => APPROVERS.some(a => a.id === picks[i]));
  out.noAutoPick = !anyPrefilled;
  if (anyPrefilled)
    out.bad.push({ why: 'slot-prefilled(auto-pick)', picks: JSON.stringify(picks) });
  const slotVals = doa.steps.map((s, i) => {
    const el = document.getElementById('ss-input-slot-' + i); return el ? (el.value || '').trim() : ''; });
  out.slotInputsEmpty = slotVals.every(v => v === '');
  if (!out.slotInputsEmpty) out.bad.push({ why: 'slot-input-not-empty', slotVals });

  // (2) กดส่งทั้งที่ยังไม่แตะ (ปุ่ม disabled → onclick ไม่ยิง · backstop doSubmit ต้อง bail) → ไม่ commit
  const beforeN = EXP.docs.length;
  const docId = state.doaDraft.docId || null;
  const beforeStatus = docId ? ((findDoc(docId) || {}).status) : null;
  b0.click();
  doSubmit();
  const afterN = EXP.docs.length;
  const afterStatus = docId ? ((findDoc(docId) || {}).status) : null;
  out.submittedWhileUntouched = (afterN !== beforeN) || (docId ? (beforeStatus !== afterStatus) : false);
  if (out.submittedWhileUntouched) out.bad.push({ why: 'committed-while-untouched',
      beforeN, afterN, beforeStatus, afterStatus });

  // (3) เลือกผู้อนุมัติจริงครบทุก slot → ปุ่มต้อง enable → doSubmit ต้อง commit
  state._busy = false;
  doa.steps.forEach((s, i) => {
    if (typeof ssPick === 'function' && window.__ss && window.__ss['slot-' + i]) ssPick('slot-' + i, 0);
    else { state.doaDraft.picks[i] = (APPROVERS[i] || APPROVERS[0]).id;
           if (typeof onSlotPickChange === 'function') onSlotPickChange(); }
  });
  const b1 = btn();
  out.enabledWhenAllPicked = b1 ? (b1.disabled === false) : null;
  if (!out.enabledWhenAllPicked)
    out.bad.push({ why: 'still-disabled-after-all-picked', picks: JSON.stringify(state.doaDraft.picks) });
  const beforeN2 = EXP.docs.length;
  const beforeStatus2 = docId ? ((findDoc(docId) || {}).status) : null;
  doSubmit();
  const afterN2 = EXP.docs.length;
  const afterStatus2 = docId ? ((findDoc(docId) || {}).status) : null;
  out.submittedWhenAllPicked = (afterN2 !== beforeN2) || (docId ? (beforeStatus2 !== afterStatus2) : false);
  out.busy = state._busy;
  if (!out.submittedWhenAllPicked) out.bad.push({ why: 'not-committed-after-all-picked',
      beforeN2, afterN2, beforeStatus2, afterStatus2 });
  return out;
}
"""


def assert_submit_requires_all_approvers(pg, btn_id='submitConfirmBtn', note=''):
    """assert ว่า modal 'ส่งอนุมัติ' (DOA slot picker) ไม่ auto-pick ผู้อนุมัติ + ต้องเลือกครบทุก slot ก่อนส่ง

    เรียก **หลังเปิด submit modal + render** (slot combos init) แล้ว. เช็ก ground-truth หลัง fix (Bug A):
      (1) modal เพิ่งเปิด · ยังไม่แตะ → ปุ่มยืนยัน DISABLED · picks ไม่มี valid pick · ช่อง slot input ว่าง
          (ไม่มี auto-pick — พิสูจน์ว่าไม่ prefill คนให้เอง)
      (2) กดส่งทั้งที่ยังไม่แตะ (ปุ่ม disabled + backstop doSubmit) → ไม่ commit (ไม่สร้างใบ · ไม่ flip)
      (3) เลือกผู้อนุมัติจริงครบทุก slot (ssPick) → ปุ่ม enable → doSubmit commit ได้
    helper ขับ state เอง (กดส่งเปล่า → เลือกครบ → doSubmit) — คืน dict ถ้าผ่าน · โยน AssertionError ถ้าพัง
    """
    r = pg.evaluate(JS_SUBMIT_APPROVER_GATE, {'btnId': btn_id})
    assert r['bad'] == [], (f"submit modal auto-pick/ส่งได้ทั้งที่ slot ว่าง (F-HR-EXPENSE · Bug A) {note}: {r['bad']} · "
                            f"steps={r['steps']} hadId={r['hadId']}")
    return r


# ⭐ เพิ่ม 2026-09-09 (F-HR-EXPENSE) — ผู้ใช้เจอ backdrop ค้างหลัง "confirm action" (อนุมัติ/ตีกลับ/ยกเลิก)
#
# ที่มา (Bug B): doApprove/doReject/doCancel เดิมเรียกแค่ closeModal() ปิด modal อย่างเดียว → view-drawer
#   + drawerBackdrop (is-open · pointer-events:auto) ยังค้างบังทั้งจอ → ผู้ใช้ต้องคลิกอีกครั้งเพื่อเคลียร์
#   fix: ทั้งสามเรียก closeModal(); closeDrawer(); render(); (mirror doSubmit) → overlay เคลียร์คลิกเดียวจบ
#
# ทำไม assert_overlay_cleared_after_close (BUG-6) เดิมมองไม่เห็น: มันตรวจ path "ปิดด้วย X / คลิก backdrop"
#   เท่านั้น — ไม่ได้เดินผ่าน confirm action (doApprove/doReject/doCancel) ซึ่งเป็นคนละทางออก
# ตัวนี้ตรวจ "หลังกดปุ่มยืนยันใน modal-foot": backdrop ทั้งคู่ต้องไม่ is-open + pointer-events:none ·
#   และ elementFromPoint(กลางจอ) ต้องเป็น element ของหน้าเพจ ไม่ใช่ drawerBackdrop/modalBackdrop
JS_OVERLAY_CLEARED_AFTER_CONFIRM = r"""
() => {
  const db = document.getElementById('drawerBackdrop');
  const mb = document.getElementById('modalBackdrop');
  const out = { ok: true, bad: [], centerHit: null };
  const cx = Math.round(innerWidth / 2), cy = Math.round(innerHeight / 2);
  const el = document.elementFromPoint(cx, cy);
  out.centerHit = el ? (el.id || el.className || el.tagName).toString().slice(0, 34) : null;
  const chk = (bd, name) => {
    if (!bd) return;
    if (bd.classList.contains('is-open')) out.bad.push({ why: name + '-still-is-open' });
    const pe = getComputedStyle(bd).pointerEvents;
    if (pe !== 'none') out.bad.push({ why: name + '-pointer-events', pe });
  };
  chk(db, 'drawerBackdrop');
  chk(mb, 'modalBackdrop');
  if (el) {
    if (el === db || el === mb) out.bad.push({ why: 'center-on-backdrop', id: el.id });
    else if (el.closest && el.closest('.drawer-backdrop, .modal-backdrop'))
      out.bad.push({ why: 'center-under-backdrop' });
  }
  out.ok = out.bad.length === 0;
  return out;
}
"""


def assert_overlay_cleared_after_confirm_action(pg, note=''):
    """assert ว่าหลัง confirm action (อนุมัติ/ตีกลับ/ยกเลิก) backdrop ไม่ค้างบังจอ — คลิกเดียวจบ (Bug B · F-HR-EXPENSE)

    เรียก **หลังคลิกปุ่มยืนยันใน modal-foot แล้ว settle** (doApprove/doReject/doCancel รันแล้ว). เช็ก:
      (1) drawerBackdrop + modalBackdrop ต้องไม่มี .is-open และ pointer-events:none (ไม่ดักคลิก)
      (2) document.elementFromPoint(กลางจอ) เป็น element ของหน้าเพจ ไม่ใช่ backdrop ที่ปิดแล้ว
    คืน dict ถ้าผ่าน · โยน AssertionError ถ้าพัง
    """
    r = pg.evaluate(JS_OVERLAY_CLEARED_AFTER_CONFIRM)
    assert r['ok'], (f"backdrop ค้างหลัง confirm action (Bug B) {note}: {r['bad']} · "
                     f"คลิกกลางจอโดน {r['centerHit']}")
    return r


# ⭐ เพิ่ม 2026-09-09 (F-HR-EXPENSE) — ผู้ใช้เจอ combobox ผู้อนุมัติในกล่อง "ส่งอนุมัติ" ดัน modal scroll (§C3.8)
#
# ที่มา (Bug C): modal 'ส่งอนุมัติ' มี .modal-body{overflow-y:auto} · ข้างในเป็น combobox slot picker
#   ที่ dropdown (.ss-list) เป็น position:absolute. เปิด dropdown → เนื้อ list ดันพื้นที่ scroll ของ
#   modal-body (วัดจริง: scrollHeight 187→440, scrollbar โผล่) → ทั้ง modal เลื่อน (ดูแปลก) แทนที่ list
#   จะลอยทับขอบ modal. fix: render() toggle class 'has-combo' บน #modalBackdrop เมื่อ modal.type==='submit'
#   + CSS '.modal-backdrop.has-combo .modal, .modal-backdrop.has-combo .modal-body{overflow:visible}'
#   → dropdown ลอยพ้นกรอบ (ไม่ดัน scroll · ไม่ถูก clip) · เลือกยังทำงาน
#
# ทำไมตัววัด/gate เดิมมองไม่เห็น: qc-ux/qc-coverage grep โค้ด ไม่ได้เรนเดอร์แล้วเปิด dropdown จริง ·
#   DSP-02b (modal_autoopens) ตรวจแค่ "combobox ไม่กางเอง" ไม่ได้เปิดเองแล้ววัด overflow/scroll ·
#   ตัววัดเรขาคณิต (hscroll/clip) ดู scroll แนวนอน ไม่ได้ถามว่า "เปิด dropdown แล้ว modal-body เลื่อนมั้ย"
#
# ground-truth หลัง fix (ตัววัดนี้ต้อง assert):
#   (1) เปิด submit modal → #modalBackdrop มี class has-combo · modal-body overflowY = 'visible' (ไม่ auto/scroll)
#   (2) เปิด dropdown ของ slot → modal-body ยัง overflowY 'visible' + เลื่อนไม่ได้ (scrollTop set 50 อ่านกลับ 0)
#   (3) dropdown เรนเดอร์เต็ม (option ครบ · list มีความสูงจริง) · ลอยพ้นกรอบ modal ได้ (ไม่ถูก clip)
#   (4) เลือกผู้อนุมัติ (ssPick) → list ปิด · picks บันทึก · ปุ่มส่ง reflect validation (submitReady)
# helper self-contained: เปิด modal ของ draft แรก → รอ rAF (guard ทำงานจบ) → เปิด/วัด/เลือกเอง
JS_COMBOBOX_FLOATS_IN_MODAL = r"""
async (arg) => {
  const raf = () => new Promise(res => { let n = 0;
    const t = () => { n++; if (n >= 6) res(); else requestAnimationFrame(t); }; requestAnimationFrame(t); });
  const out = { steps: 0, optCount: 0, bad: [],
                hasCombo: null, bodyOverflowFresh: null, listVisibleAfterOpen: null,
                bodyOverflowOpen: null, scrollTrapped: null, listRendered: null, listFloatsBelow: null,
                pickClosedList: null, pickRecorded: null, btnReflects: null };
  // (0) เปิด submit modal ของ draft แรก
  const draft = (typeof EXP !== 'undefined') && EXP.docs.find(x => x.status === 'draft');
  if (!draft) { out.bad.push({ why: 'no-draft-doc' }); return out; }
  openSubmitDraft(draft.id);
  await raf();   // ให้ trapFocus + guardOverlayAutoCombo (DSP-02b) ทำงานจนจบก่อน (กันเปิดเองมาชน)
  if (!(state.modal.open && state.modal.type === 'submit' && state.doaDraft)) {
    out.bad.push({ why: 'submit-modal-not-open' }); return out; }
  const doa = resolveDoa((state.doaDraft.grand) || 0);
  out.steps = doa.steps.length;
  const backdrop = document.getElementById('modalBackdrop');
  const modal = document.querySelector('#modalBackdrop .modal');
  const body  = document.querySelector('#modalBackdrop .modal-body');
  if (!backdrop || !modal || !body) { out.bad.push({ why: 'no-modal-parts' }); return out; }

  // (1) has-combo ติด · modal-body ปล่อยลอย (overflowY visible ไม่ใช่ auto/scroll)
  out.hasCombo = backdrop.classList.contains('has-combo');
  if (!out.hasCombo) out.bad.push({ why: 'modalBackdrop-ไม่มี-has-combo' });
  out.bodyOverflowFresh = getComputedStyle(body).overflowY;
  if (out.bodyOverflowFresh !== 'visible')
    out.bad.push({ why: 'modal-body-overflowY-fresh', v: out.bodyOverflowFresh });

  // (2) เปิด dropdown ของ slot แรก → รอ settle
  ssOpen('slot-0');
  await raf();
  const list = document.getElementById(ssId('ss-list-', 'slot-0'));
  if (!list) { out.bad.push({ why: 'no-ss-list-slot-0' }); return out; }
  out.listVisibleAfterOpen = !list.classList.contains('hidden');
  if (!out.listVisibleAfterOpen) out.bad.push({ why: 'ss-list-ยังซ่อนหลัง-ssOpen' });

  // (3) modal-body ไม่ถูกดันให้ scroll (dropdown ลอยทับ) — เช็ก 2 ชั้น: overflowY + เลื่อนไม่ได้จริง
  out.bodyOverflowOpen = getComputedStyle(body).overflowY;
  if (out.bodyOverflowOpen !== 'visible')
    out.bad.push({ why: 'modal-body-overflowY-open(dropdown-ดัน-scroll)', v: out.bodyOverflowOpen });
  body.scrollTop = 50;                       // overflow:visible → ไม่ใช่ scroll container → อ่านกลับ 0
  out.scrollTrapped = body.scrollTop !== 0;  // true = พังจริง (modal-body เลื่อนได้ = dropdown ดันสูง)
  if (out.scrollTrapped) out.bad.push({ why: 'modal-body-เลื่อนได้', scrollTop: body.scrollTop });

  // (4) dropdown เรนเดอร์เต็ม · ลอยพ้นกรอบ modal ได้ (ไม่ถูก clip)
  const lr = list.getBoundingClientRect(), mr = modal.getBoundingClientRect();
  out.optCount = list.querySelectorAll('.ss-opt').length;
  out.listRendered = out.optCount === APPROVERS.length && lr.height > 10;
  if (!out.listRendered)
    out.bad.push({ why: 'dropdown-ไม่เรนเดอร์เต็ม', opt: out.optCount, want: APPROVERS.length, h: Math.round(lr.height) });
  out.listFloatsBelow = lr.bottom > mr.bottom;   // informational — ลอยพ้นกรอบ = คาดหวัง (ไม่ถูก clip)

  // (5) เลือกผู้อนุมัติจริง → list ปิด · picks บันทึก · ปุ่มส่ง reflect validation
  ssPick('slot-0', 0);
  await raf();
  out.pickClosedList = list.classList.contains('hidden');
  if (!out.pickClosedList) out.bad.push({ why: 'list-ไม่ปิดหลัง-ssPick' });
  const picks = state.doaDraft.picks || {};
  out.pickRecorded = APPROVERS.some(a => a.id === picks[0]);
  if (!out.pickRecorded) out.bad.push({ why: 'picks[0]-ไม่ถูกบันทึก', picks: JSON.stringify(picks) });
  const btn = document.getElementById(arg.btnId || 'submitConfirmBtn');
  out.btnReflects = btn ? (btn.disabled === !submitReady()) : null;
  if (out.btnReflects === false)
    out.bad.push({ why: 'ปุ่มส่งไม่-reflect-validation', disabled: btn.disabled, ready: submitReady() });
  return out;
}
"""


def assert_combobox_floats_in_modal(pg, btn_id='submitConfirmBtn', note=''):
    """assert ว่า combobox ในกล่อง 'ส่งอนุมัติ' เปิด dropdown แล้วลอยทับ — ไม่ดัน modal scroll (Bug C · F-HR-EXPENSE)

    self-contained: เปิด submit modal ของ draft แรก (openSubmitDraft) → รอ rAF → เปิด/วัด/เลือกเอง. เช็ก:
      (1) #modalBackdrop มี class has-combo · modal-body overflowY = 'visible' (ไม่ auto/scroll)
      (2) เปิด dropdown slot → modal-body ยัง overflowY 'visible' + เลื่อนไม่ได้ (scrollTop set 50 → อ่านกลับ 0)
      (3) dropdown เรนเดอร์เต็ม (option ครบ APPROVERS) · ลอยพ้นกรอบ modal ได้ (ไม่ถูก clip)
      (4) เลือกผู้อนุมัติ (ssPick) → list ปิด · picks[0] บันทึก · ปุ่มส่ง reflect submitReady()
    คืน dict ถ้าผ่าน · โยน AssertionError ถ้าพัง
    """
    r = pg.evaluate(JS_COMBOBOX_FLOATS_IN_MODAL, {'btnId': btn_id})
    assert r['bad'] == [], (f"combobox ในกล่องส่งอนุมัติดัน modal scroll / ถูก clip (Bug C · F-HR-EXPENSE) {note}: "
                            f"{r['bad']} · steps={r['steps']} hasCombo={r['hasCombo']} "
                            f"overflowY(fresh/open)={r['bodyOverflowFresh']}/{r['bodyOverflowOpen']}")
    return r


# ⭐ เพิ่ม 2026-09-10 (F-HR-EXPENSE) — ผู้ใช้เจอ slot combobox dropdown ในกล่อง "ส่งอนุมัติ" ทะลุก้นจอ (§C3.8)
#
# ที่มา (Bug D): modal 'ส่งอนุมัติ' ของยอด >50,000 มี 3 slot · เปิด dropdown ของ slot ล่างสุดที่จอเตี้ย
#   (~<900px) → .ss-list (absolute, top:100%) กางลงล่าง แล้วก้น list ทะลุขอบล่างของ window
#   (วัดจริงก่อนแก้: viewport 800/768/720/650 → ล้น 22/38/62/97px · ที่ 900 ยังพอดี)
#   fix: CSS '.ss-list.ss-up{top:auto;bottom:calc(100% + 4px);margin-top:0}' + JS ssPlaceList(key,list)
#   เรียกท้าย ssRenderList ตอน s.open — วัด wrap rect แล้วเติม class 'ss-up' เมื่อพื้นที่ด้านล่างไม่พอ
#   และด้านบนมากกว่า → dropdown flip ขึ้น กันทะลุก้นจอ
#
# ทำไมตัววัด/gate เดิมมองไม่เห็น: qc-ux/qc-coverage grep โค้ด ไม่ได้เปิด dropdown จริง · JS_LAYOUT ข้อ
#   'clipped' ตรวจแค่ 'ถูกกล่องแม่ (overflow) ตัด' — ที่นี่ list ลอยพ้นทุกกล่อง (modal overflow:visible จาก
#   has-combo, Bug C) จึงไม่มีบรรพบุรุษตัด แต่ก้นมันเลย innerHeight ไป · ไม่มีข้อไหนถามว่า 'list ทะลุ
#   "ก้นจอ" มั้ย' · ต้องเรนเดอร์ที่จอเตี้ย + เปิด slot ล่างสุดถึงจะเห็น
#
# ⚠️ ต้องเรียกที่ viewport เตี้ย (เช่น pg.set_viewport_size({'width':1440,'height':768})) + reload หน้าแล้ว
#   helper บังคับ submit modal 3 slot เอง (state.doaDraft grand 60000 → openModal('submit')) → เปิด slot
#   ล่างสุด → วัด · ground-truth หลัง fix: (1) list.bottom <= innerHeight (ไม่ทะลุ) · (2) list มี class 'ss-up'
JS_SLOT_DROPDOWN_NO_SPILL = r"""
async () => {
  const raf = () => new Promise(res => { let n = 0;
    const t = () => { n++; if (n >= 6) res(); else requestAnimationFrame(t); }; requestAnimationFrame(t); });
  const out = { ok: false, bad: [], nslots: 0, vh: window.innerHeight, lastKey: null,
                listTop: null, listBottom: null, spillPx: null, hasUp: null };
  if (typeof openModal !== 'function' || typeof resolveDoa !== 'function' ||
      typeof ssOpen !== 'function' || typeof ssId !== 'function') {
    out.bad.push({ why: 'missing-fns' }); return out; }
  // บังคับ submit modal 3 slot (ยอด >50,000 → DOA 3 ขั้น)
  state.doaDraft = { picks: {}, grand: 60000 };
  openModal('submit', {});
  await raf();
  if (!(state.modal.open && state.modal.type === 'submit' && state.doaDraft)) {
    out.bad.push({ why: 'submit-modal-not-open' }); return out; }
  const doa = resolveDoa((state.doaDraft.grand) || 0);
  out.nslots = doa.steps.length;
  if (out.nslots < 3) { out.bad.push({ why: 'not-3-slots', n: out.nslots }); return out; }
  const last = out.nslots - 1;
  out.lastKey = 'slot-' + last;
  ssOpen('slot-' + last);
  await raf();
  const list = document.getElementById(ssId('ss-list-', 'slot-' + last));
  if (!list) { out.bad.push({ why: 'no-ss-list-last' }); return out; }
  if (list.classList.contains('hidden')) { out.bad.push({ why: 'list-hidden-after-open' }); return out; }
  const r = list.getBoundingClientRect();
  out.listTop = Math.round(r.top);
  out.listBottom = Math.round(r.bottom);
  out.spillPx = Math.round(r.bottom - window.innerHeight);
  out.hasUp = list.classList.contains('ss-up');
  // (1) ก้น list ต้องไม่ทะลุก้นจอ (innerHeight)
  if (r.bottom > window.innerHeight + 1)
    out.bad.push({ why: 'spills-below-window', listBottom: out.listBottom, vh: window.innerHeight, over: out.spillPx });
  // (2) ที่จอเตี้ย + slot ล่างสุด ต้อง flip ขึ้น (ss-up) — ตัวจับตัวจริงของ fix
  if (!out.hasUp)
    out.bad.push({ why: 'ss-up-not-applied(flip-หาย)', listBottom: out.listBottom, vh: window.innerHeight });
  out.ok = out.bad.length === 0;
  return out;
}
"""


def assert_slot_dropdown_no_spill(pg, note=''):
    """assert ว่า slot combobox dropdown (กล่องส่งอนุมัติ 3 slot) ไม่ทะลุก้นจอ + flip ขึ้น (ss-up) ที่จอเตี้ย (Bug D · F-HR-EXPENSE)

    ⚠️ ต้องเรียก **หลังตั้ง viewport เตี้ย** (เช่น pg.set_viewport_size({'width':1440,'height':768})) + reload หน้า.
    helper บังคับ submit modal 3 slot เอง (state.doaDraft grand 60000 → openModal('submit')) → เปิด dropdown
    ของ slot ล่างสุด → วัด:
      (1) list.getBoundingClientRect().bottom <= innerHeight (ไม่ทะลุก้นจอ)
      (2) list มี class 'ss-up' (flip ขึ้นเมื่อพื้นที่ด้านล่างไม่พอ)
    คืน dict ถ้าผ่าน · โยน AssertionError ถ้าพัง
    """
    r = pg.evaluate(JS_SLOT_DROPDOWN_NO_SPILL)
    assert r['bad'] == [], (f"slot dropdown ทะลุก้นจอ/ไม่ flip ขึ้น (Bug D · F-HR-EXPENSE) {note}: {r['bad']} · "
                            f"nslots={r['nslots']} vh={r['vh']} listBottom={r['listBottom']} hasUp={r['hasUp']}")
    return r


# ⭐ เพิ่ม 2026-09-10 (F-HR-EXPENSE) — regression guard: ไม่มี backdrop ค้างหลังปิดกล่อง "ส่งอนุมัติ" ทุกทาง (§C3.8)
# ⭐ แก้ให้ FAITHFUL 2026-09-10 (F-HR-EXPENSE · backdrop bug) — เปิด modal "ผ่านลิ้นชักดูใบร่างจริง" ไม่ใช่เปิดตรง
#
# ที่มา: ปิด submit modal ได้หลายทาง (ปุ่มยกเลิก · คลิกฉากหลัง #modalBackdrop · Escape) — ทุกทางต้องเคลียร์
#   overlay คลิกเดียวจบ (mirror BUG-6/Bug B) · + Esc chain (Rule #94 ข้อ 3): ถ้า dropdown ของ slot เปิดค้าง
#   → Esc ครั้งแรกต้องปิด "แค่ dropdown" คงกล่องส่งอนุมัติไว้ (ห้าม Esc ทะลุไปปิด modal ทิ้งงานที่กรอกไว้)
#
# ⚠️ FALSE PASS ที่แก้: เวอร์ชันเดิมเปิด modal ด้วย openSubmitDraft() ตรง ๆ ใน eval → **ไม่มีลิ้นชักดูใบร่างอยู่ใต้ modal**
#   จึงไม่เคยเดินเคสจริงที่ผู้ใช้เจอ: กล่อง "ส่งอนุมัติ" เปิดจากปุ่มใน footer ของลิ้นชักดูใบร่าง (openSubmitDraft(id))
#   → ลิ้นชัก + drawerBackdrop (is-open · pe:auto) ค้างอยู่ใต้ modal · ปิด modal ทางเดียว เดิมเคลียร์แค่ modal
#   เหลือ drawerBackdrop หรี่จอค้าง ต้องคลิกซ้ำ. fix (expense.html · closeModal): submit-modal ที่มี doaDraft.docId
#   → เรียก closeDrawer() ด้วย ทุกทาง dismiss. ตัววัดต้องเปิด modal "ผ่านลิ้นชัก" ถึงจะจับ regression นี้ได้
#
# faithful path: openView(draftId) → คลิกปุ่ม 'ส่งอนุมัติ' ใน footer ลิ้นชัก → submit modal ทับลิ้นชัก (ทั้งคู่เปิด)
#   → ทุกทาง dismiss ต้องปิด **ทั้ง modal และลิ้นชัก** (state.drawer.open===false · ไม่มี backdrop ตัวไหนค้าง)
#
# หมายเหตุพฤติกรรมจริงที่ยืนยันแล้ว (2026-09-10 · ทั้ง fix เข้าแล้ว): ตราบใดที่โฟกัสยังค้างใน ss-input ของ slot
#   ssOnKey เรียก e.stopPropagation() ทุก Escape (BASE-KIT footgun — uikit combobox_sweep ก็เตือนไว้เรื่องเดียวกัน)
#   → Esc ครั้งถัดไปถูกกลืน · modal จึงยังไม่ปิดจนกว่าโฟกัสจะออกจาก combobox. การปิด modal ขั้นสุดท้ายจึงเดินผ่าน
#   window Esc handler เมื่อโฟกัสออกจาก ss-input แล้ว (blur → Escape) — ไม่แตะ expense.html
#
# ทำไม assert_overlay_cleared_after_* เดิมไม่ครอบ: BUG-6 ตรวจปิดด้วย X/คลิก backdrop · Bug B ตรวจหลัง confirm
#   action (อนุมัติ/ตีกลับ/ยกเลิก) — ทั้งคู่ไม่ได้เดิน Esc chain (dropdown ของ slot เปิดค้าง) ของ 'กล่องส่งอนุมัติ'
def assert_submit_modal_all_dismiss_clean(pg, note=''):
    """assert ว่ากล่อง 'ส่งอนุมัติ' (เปิดจากลิ้นชักดูใบร่าง) ปิดสะอาดทุกทาง — ทั้ง modal และลิ้นชักเคลียร์ (F-HR-EXPENSE)

    FAITHFUL: เปิด modal ผ่านทางจริง — openView(draftId) เปิดลิ้นชักดูใบร่าง แล้ว **คลิกปุ่ม 'ส่งอนุมัติ' ใน footer
    ของลิ้นชัก** (openSubmitDraft(id)) → submit modal เปิดทับลิ้นชัก (drawerBackdrop is-open ค้างอยู่ใต้ modal).
    ต่อทาง dismiss แล้ว assert:
      · modal ปิด (state.modal.open===false)
      · ลิ้นชักปิดด้วย (state.drawer.open===false) — fix closeModal ต้องเรียก closeDrawer เมื่อ submit จากใบร่าง
      · ไม่มี backdrop ตัวไหนค้าง (drawerBackdrop/modalBackdrop ไม่ is-open · pointer-events:none ·
        elementFromPoint กลางจอเป็น element ของหน้าเพจ ไม่ใช่ backdrop)
    ทาง dismiss: cancel-button · click-backdrop · escape · escape-chain (Esc#1 ปิดแค่ dropdown คง modal)
    คืน dict {'paths':[...]} ถ้าผ่าน · โยน AssertionError ถ้าพัง
    """
    def _raf():
        pg.evaluate("() => new Promise(res=>{let n=0;const t=()=>{n++;if(n>=6)res();else requestAnimationFrame(t);};requestAnimationFrame(t);})")

    def _open_fresh():
        draft = pg.evaluate("() => { const d=(typeof EXP!=='undefined')&&EXP.docs.find(x=>x.status==='draft'); return d?d.id:null; }")
        assert draft, f"ไม่มีใบร่างให้เปิดลิ้นชัก {note}"
        # (1) เปิดลิ้นชักดูใบร่าง เหมือนผู้ใช้คลิกแถวในลิสต์
        pg.evaluate("(id) => openView(id)", draft)
        settle(pg); _raf()
        assert pg.evaluate("() => state.drawer.open===true"), f"openView ไม่เปิดลิ้นชักดูใบร่าง {note}"
        # (2) คลิกปุ่ม 'ส่งอนุมัติ' ที่ footer ของลิ้นชัก (primary · onclick=openSubmitDraft(id)) — ไม่ใช่ 'ยกเลิก'
        clicked = pg.evaluate("""() => { const btns=[...document.querySelectorAll('#drawer .drawer-footer .btn, #drawer .drawer-footer button, #drawer button')];
            const s=btns.find(b=>/ส่งอนุมัติ/.test(b.textContent||'') && !/ยกเลิก/.test(b.textContent||'')); if(s){ s.click(); return true; } return false; }""")
        assert clicked, f"ไม่พบปุ่ม 'ส่งอนุมัติ' ใน footer ลิ้นชักดูใบร่าง {note}"
        settle(pg); _raf()
        st = pg.evaluate("""() => ({ modal: state.modal.open===true && state.modal.type==='submit',
            drawer: state.drawer.open===true, docId: !!(state.doaDraft&&state.doaDraft.docId) })""")
        assert st['modal'], f"คลิก 'ส่งอนุมัติ' ในลิ้นชักไม่เปิดกล่องส่งอนุมัติ {note}: {st}"
        assert st['drawer'], f"submit modal เปิดแล้วลิ้นชักดูใบร่างต้องยังเปิดอยู่ใต้ modal (over-drawer case) {note}: {st}"
        assert st['docId'], f"submit modal จากใบร่างต้องมี doaDraft.docId (จุดที่ closeModal ใช้ตัดสินปิดลิ้นชักด้วย) {note}: {st}"

    def _clean(path):
        r = pg.evaluate(JS_OVERLAY_CLEARED_AFTER_CONFIRM)
        drawer_closed = pg.evaluate("() => state.drawer.open===false")
        assert r['ok'] and drawer_closed, (
            f"overlay ค้างหลังปิดกล่องส่งอนุมัติจากลิ้นชัก [{path}] {note}: bad={r['bad']} · "
            f"state.drawer.open={pg.evaluate('() => state.drawer.open')} (ต้อง false) · คลิกกลางจอโดน {r['centerHit']}")

    paths = []

    # (a) ปุ่มยกเลิก (ghost) ใน modal-foot
    _open_fresh()
    clicked = pg.evaluate("""() => { const b=[...document.querySelectorAll('#modalBackdrop .modal-foot .btn-ghost, #modalBackdrop .modal-footer .btn-ghost')].find(x=>/ยกเลิก/.test(x.textContent||'')); if(b){ b.click(); return true; } return false; }""")
    assert clicked, f"ไม่พบปุ่มยกเลิกใน modal-foot ของกล่องส่งอนุมัติ {note}"
    settle(pg)
    assert pg.evaluate("() => state.modal.open") is False, f"กดยกเลิกแล้วกล่องส่งอนุมัติไม่ปิด {note}"
    _clean('cancel-button'); paths.append('cancel-button')

    # (b) คลิกที่ฉากหลัง #modalBackdrop
    _open_fresh()
    pg.evaluate("() => document.getElementById('modalBackdrop').click()")
    settle(pg)
    assert pg.evaluate("() => state.modal.open") is False, f"คลิก backdrop แล้วกล่องส่งอนุมัติไม่ปิด {note}"
    _clean('click-backdrop'); paths.append('click-backdrop')

    # (c) Escape (ไม่มี dropdown เปิด) → window Esc handler ปิด modal
    _open_fresh()
    pg.keyboard.press('Escape')
    settle(pg)
    assert pg.evaluate("() => state.modal.open") is False, f"กด Escape แล้วกล่องส่งอนุมัติไม่ปิด {note}"
    _clean('escape'); paths.append('escape')

    # (d) Esc chain: dropdown ของ slot เปิดค้าง → Esc#1 ปิดแค่ dropdown คง modal → (blur) Esc → ปิดสะอาด
    _open_fresh()
    pg.evaluate("() => { const i=document.getElementById(ssId('ss-input-','slot-0')); if(i) i.focus(); ssOpen('slot-0'); }")
    settle(pg); _raf()
    pg.keyboard.press('Escape')
    settle(pg)
    mid = pg.evaluate("""() => ({ modal: state.modal.open===true,
        listHidden: (()=>{const l=document.getElementById(ssId('ss-list-','slot-0'));return l?l.classList.contains('hidden'):null;})() })""")
    assert mid['modal'] is True, \
        f"Esc#1 (dropdown ของ slot เปิดค้าง) ปิด modal ทิ้ง — ควรปิดแค่ dropdown คง modal (Esc chain · Rule #94) {note}: {mid}"
    assert mid['listHidden'] is True, f"Esc#1 ไม่ปิด dropdown ของ slot {note}: {mid}"
    pg.evaluate("() => (typeof ssBlurActive==='function') && ssBlurActive()")   # โฟกัสออกจาก combobox → Esc ถึง window handler
    pg.keyboard.press('Escape')
    settle(pg)
    assert pg.evaluate("() => state.modal.open") is False, \
        f"ปิดกล่องส่งอนุมัติหลัง Esc chain ไม่สำเร็จ (โฟกัสออกจาก combobox แล้ว Esc ต้องปิด modal) {note}"
    _clean('escape-chain'); paths.append('escape-chain')

    return {'paths': paths, 'viaDrawer': True}


# ⭐ เพิ่ม 2026-09-10 (F-HR-EXPENSE · backdrop bug) — regression guard คู่กับ faithful dismiss ข้างบน (§C3.8)
#
# fix backdrop bug (closeModal) ผูกเงื่อนไข "ปิดลิ้นชักด้วย" ไว้กับ submit modal ที่ **มี doaDraft.docId**
#   (= เปิดจากใบร่าง openSubmitDraft) เท่านั้น. ต้องกันไม่ให้ fix นี้ไป regress กล่องส่งอนุมัติของ CREATE WIZARD
#   (เปิดด้วย openSubmit() — ไม่มี docId): กดยกเลิกกล่องส่งอนุมัติจาก wizard แล้ว **ลิ้นชัก wizard ต้องยังเปิด**
#   (ผู้ใช้แค่ยกเลิกการเลือกผู้อนุมัติ ไม่ได้ทิ้งใบที่กรอกไว้). ถ้า fix ไปปิด wizard drawer ตามด้วย = regression.
#
# ขับ create flow จริง (ไม่เรียก openDrawer('wizard') ตรง ๆ ที่ทิ้ง state.wizard.doc ไว้ว่างแล้ว throw):
#   คลิกปุ่ม '+ สร้างใบเบิก' (onclick=openCreate) → เดินไปขั้นตรวจสอบ + ใส่รายการ (ให้ปุ่มส่ง enable) →
#   คลิก 'บันทึกและส่งอนุมัติ' (openSubmit · ไม่มี docId) → เลือกผู้อนุมัติครบ → คลิก 'ยกเลิก' บน modal →
#   assert state.drawer.open===true && state.drawer.mode==='wizard' (wizard ยังเปิด · draft-view fix ไม่ regress)
# ⭐ FALSE-PASS fix 2026-09-10 (F-HR-EXPENSE · lingering-backdrop bug) — §C3.8
#
# เวอร์ชันเดิมของ helper นี้ assert แค่ `state.drawer.open===true && mode==='wizard'` (STATE flag)
# → FALSE PASS: บั๊กจริงคือ full render() เขียนทับ className ของ #drawer แล้ว "ทิ้ง class is-open"
#   (มีแต่ renderDrawerOnly ที่คงไว้) → พอ closeModal เรียก render() ตอน submit modal ของ wizard ปิด
#   ลิ้นชัก wizard สไลด์ออก (เสีย is-open) แต่ drawerBackdrop ยัง is-open → wizard หายจากตา
#   เหลือฉากหลังหรี่ค้าง (ต้องคลิกซ้ำ 1 ที) ทั้งที่ state.drawer.open ยัง true อยู่
# fix (expense.html render): คง is-open ปัจจุบันของ #drawer ข้ามการเขียน className:
#   const dwOpen=dw.classList.contains('is-open'); dw.className='drawer'+(dwOpen?' is-open':'')+(wizard?' wide':'')
#
# ตัววัดใหม่จึงต้องพิสูจน์ว่าลิ้นชัก "เปิดจริงบนจอ" ไม่ใช่แค่ธง — ครบทั้ง:
#   · #drawer มี class is-open (panel สไลด์เข้า)
#   · elementFromPoint(กลางจอ) ไม่ใช่ drawerBackdrop และอยู่ "ใน" #drawer (panel คลุมกลางจอ)
#   · stepper/wizard body มองเห็น (rect กว้าง×สูง>0)
#   · state.drawer.open===true · mode==='wizard' · modal ปิด
# drawerBackdrop จะยัง is-open (หรี่จอ) ได้ — ถูกต้องแล้ว เพราะลิ้นชักเปิดอยู่จริง
# ย้อนโค้ด fix กลับ (ตัด is-open preservation) → center = drawerBackdrop / #drawer เสีย is-open → เคสนี้ FAIL
JS_WIZARD_DRAWER_VISUALLY_OPEN = """
() => {
  const dw=document.getElementById('drawer'), db=document.getElementById('drawerBackdrop');
  const cx=Math.round(innerWidth/2), cy=Math.round(innerHeight/2);
  const el=document.elementFromPoint(cx, cy);
  const stepper=document.querySelector('#drawer .stepper');
  const sr=stepper?stepper.getBoundingClientRect():null;
  return {
    drawerIsOpen: dw ? dw.classList.contains('is-open') : false,
    drawerCls: dw ? dw.className : '(no #drawer)',
    backdropIsOpen: db ? db.classList.contains('is-open') : false,
    stateDrawerOpen: state.drawer.open, stateMode: state.drawer.mode, stateModalOpen: state.modal.open,
    centerCls: el ? (el.id||el.className||el.tagName).toString().slice(0,40) : null,
    centerInDrawer: !!(el && dw && dw.contains(el)),
    centerIsBackdrop: !!(el && (el.id==='drawerBackdrop' || /backdrop/.test((el.className||'').toString()))),
    stepperVisible: !!(sr && sr.width>0 && sr.height>0),
  };
}
"""


def assert_wizard_submit_cancel_keeps_drawer(pg, note=''):
    """assert ว่ากล่อง 'ส่งอนุมัติ' ที่เปิดจาก CREATE WIZARD (openSubmit · ไม่มี docId) แล้ว dismiss ทุกทาง
    (ยกเลิก / คลิก backdrop / Escape) → ลิ้นชัก wizard ยัง **เปิดจริงบนจอ** (ไม่ใช่แค่ธง state):
    #drawer มี is-open · กลางจอเป็นเนื้อ wizard (ไม่ใช่ drawerBackdrop) · stepper มองเห็น · mode==='wizard' · modal ปิด.

    กันทั้ง 2 ทิศ: (ก) draft-view fix ต้องไม่ปิด wizard drawer ตาม (regression) และ
    (ข) lingering-backdrop bug — full render() ทิ้ง is-open ของ #drawer → wizard สไลด์ออก เหลือฉากหลังหรี่ค้าง
    (เดิม assert แค่ state.drawer.open → FALSE PASS เพราะธงยัง true แต่จอไม่เห็นลิ้นชัก).
    page ต้องโหลดหน้าไว้แล้ว · viewport ปกติ. คืน dict {'paths','drawerOpen','drawerMode','center'} ถ้าผ่าน.
    """
    def _raf():
        pg.evaluate("() => new Promise(res=>{let n=0;const t=()=>{n++;if(n>=6)res();else requestAnimationFrame(t);};requestAnimationFrame(t);})")

    def _reload():
        # เปิดหน้าใหม่ (reset mock + ปิด overlay ทั้งหมด) เพื่อให้แต่ละทาง dismiss เดินจาก slate สะอาด
        pg.evaluate("() => location.reload()")
        pg.wait_for_load_state('load')
        pg.wait_for_function(
            "() => { const p=document.getElementById('page-content'); return p && p.innerHTML.trim().length>0; }",
            timeout=12000)
        settle(pg)

    def _open_wizard_submit():
        # (1) คลิกปุ่ม '+ สร้างใบเบิก' จริง → openCreate → wizard drawer เปิด (init state.wizard.doc ให้ครบ)
        made = pg.evaluate("""() => { const b=[...document.querySelectorAll('#page-content button, .btn')].find(x=>/สร้างใบเบิก/.test(x.textContent||'')); if(b){ b.click(); return true; } return false; }""")
        assert made, f"ไม่พบปุ่ม '+ สร้างใบเบิก' ในลิสต์ {note}"
        settle(pg); _raf()
        assert pg.evaluate("() => state.drawer.open===true && state.drawer.mode==='wizard'"), \
            f"คลิกสร้างใบเบิกไม่เปิด wizard drawer {note}"
        # (2) ไปขั้นตรวจสอบ (step 5) + ผู้เบิก + รายการ (ยอด>0 → ปุ่มส่ง enable)
        pg.evaluate("""() => { state.wizard.doc.emp='E01';
          state.wizard.doc.lines=[{date:'2569-08-28',cat:'other',desc:'x',qty:1,unit_price:500,vat_mode:'none'}];
          state.wizard.step=5; renderDrawerOnly(); }""")
        settle(pg)
        # (3) คลิก 'บันทึกและส่งอนุมัติ' ที่ footer wizard (เรียก openSubmit — ไม่มี docId)
        sent = pg.evaluate("""() => { const b=[...document.querySelectorAll('#drawer .drawer-footer .btn')].find(x=>/บันทึกและส่งอนุมัติ/.test(x.textContent||'')); if(b && !b.disabled){ b.click(); return true; } return false; }""")
        assert sent, f"ปุ่ม 'บันทึกและส่งอนุมัติ' ในขั้นตรวจสอบกดไม่ได้/ไม่พบ (ปุ่มควร enable เมื่อมีรายการ) {note}"
        settle(pg); _raf()
        st = pg.evaluate("""() => ({ modal: state.modal.open===true && state.modal.type==='submit',
            hasDocId: !!(state.doaDraft&&state.doaDraft.docId), drawer: state.drawer.open===true }) """)
        assert st['modal'], f"กล่องส่งอนุมัติจาก wizard ไม่เปิด {note}: {st}"
        assert st['hasDocId'] is False, \
            f"submit จาก wizard ต้องไม่มี docId (ไม่งั้นจะเข้าเงื่อนไข closeDrawerToo ผิด) {note}: {st}"
        assert st['drawer'], f"เปิด submit modal จาก wizard แล้ว wizard drawer ต้องยังเปิดอยู่ใต้ modal {note}: {st}"
        # (4) เลือกผู้อนุมัติครบทุก slot (เหมือนผู้ใช้กรอกจริง) แล้วค่อย dismiss
        pg.evaluate("""() => { const doa=resolveDoa((state.doaDraft&&state.doaDraft.grand)||0);
          doa.steps.forEach((s,i)=>{ if(window.__ss && window.__ss['slot-'+i]) ssPick('slot-'+i,0); }); }""")
        settle(pg); _raf()

    def _assert_visually_open(path):
        v = pg.evaluate(JS_WIZARD_DRAWER_VISUALLY_OPEN)
        base = f"[{path}] {note}: {v}"
        assert v['stateModalOpen'] is False, f"dismiss กล่องส่งอนุมัติ (wizard) แล้ว modal ไม่ปิด {base}"
        # ★ หัวใจของ fix false-pass: ลิ้นชักต้อง "เปิดจริงบนจอ" ไม่ใช่แค่ธง state
        assert v['drawerIsOpen'] is True, \
            f"#drawer เสีย class is-open หลัง dismiss (lingering-backdrop bug — render() ทิ้ง is-open) {base}"
        assert v['stateDrawerOpen'] is True and v['stateMode'] == 'wizard', \
            f"state.drawer ต้อง open + mode='wizard' (draft-view fix ต้องไม่ regress wizard) {base}"
        assert v['centerIsBackdrop'] is False, \
            f"กลางจอเป็น drawerBackdrop = ลิ้นชักสไลด์ออกเหลือฉากหลังหรี่ค้าง (ต้องคลิกซ้ำ) {base}"
        assert v['centerInDrawer'] is True, \
            f"กลางจอไม่ได้อยู่ใน panel #drawer (ลิ้นชักไม่คลุมกลางจอ = ไม่ได้เปิดจริง) {base}"
        assert v['stepperVisible'] is True, \
            f"stepper/เนื้อ wizard มองไม่เห็นหลัง dismiss (ลิ้นชักไม่ได้เรนเดอร์เนื้อ) {base}"
        return v

    dismissers = [
        ('cancel-button', lambda: pg.evaluate("""() => { const b=[...document.querySelectorAll('#modalBackdrop .modal-foot .btn-ghost, #modalBackdrop .modal-footer .btn-ghost')].find(x=>/ยกเลิก/.test(x.textContent||'')); if(b){ b.click(); return true; } return false; }""")),
        ('click-backdrop', lambda: pg.evaluate("() => { document.getElementById('modalBackdrop').click(); return true; }")),
        ('escape', None),   # จัดการแยกด้านล่าง (blur combobox ก่อนกัน Esc chain กลืน)
    ]

    paths, last = [], None
    for i, (path, act) in enumerate(dismissers):
        if i > 0:
            _reload()
        _open_wizard_submit()
        if act is None:
            # Esc: โฟกัสออกจาก combobox ก่อน (กัน Esc#1 ปิดแค่ dropdown คง modal ไว้) → Esc ถึง window handler ปิด modal
            pg.evaluate("() => (typeof ssBlurActive==='function') && ssBlurActive()")
            pg.keyboard.press('Escape')
            settle(pg); _raf()
            if pg.evaluate("() => state.modal.open"):     # เผื่อ Esc#1 ไปโดน dropdown ที่เปิดค้าง
                pg.evaluate("() => (typeof ssBlurActive==='function') && ssBlurActive()")
                pg.keyboard.press('Escape')
                settle(pg); _raf()
        else:
            ok = act()
            assert ok, f"dismiss [{path}] หา affordance ไม่เจอ {note}"
            settle(pg); _raf()
        last = _assert_visually_open(path)
        paths.append(path)

    return {'paths': paths, 'drawerOpen': last['stateDrawerOpen'],
            'drawerMode': last['stateMode'], 'center': last['centerCls']}


# ⭐ เพิ่ม 2026-09-10 (F-HR-ESS · §C3.8 · user-found bug ที่ qc-ux มองไม่เห็น)
# ─────────────────────────────────────────────────────────────────────────────
# บั๊กจริง: มี click listener ระดับ document/body ที่ผูกแบบ capture-phase (addEventListener
#   'click', ..., true) แล้วเรียก stopPropagation() → event ถูกหยุดตั้งแต่ขาลง (capture)
#   ยังไม่ทันถึง target เลย → onclick ของ 'ทุกปุ่มหลัก' (การ์ด dashboard .qcard ·
#   แถว action-picker .ap-row) ตายเงียบ: real click ไม่เกิดอะไร ทั้งที่ markup/attribute ถูกหมด.
#
# ทำไมตัววัดเดิมมองไม่เห็น: JS_AFFORDANCE ถามว่า "มี cursor:pointer มั้ย" (มี · ผ่าน) ·
#   JS_A11Y_REACH ถามว่า "คีย์บอร์ดไปถึงมั้ย" (native button ผ่าน) · JS_GHOST_CLASS/self_audit
#   ตรวจ markup/CSS แบบ static — ไม่มีข้อไหน "คลิกจริงแล้วดูว่า event ถึง target มั้ย".
#   qc-ux อ่านโค้ด+เรขาคณิต จึงเห็นปุ่มครบสวยแต่ทั้งหน้ากดไม่ติด.
# ข้อนี้ถามตรง ๆ: dispatch คลิกจริงที่ target แล้ว target ได้รับ event มั้ย — capture-phase
#   ancestor ที่ stopPropagation จะกันไม่ให้ event ลงมาถึง → probe ไม่ยิง = ตาย (จับได้).
def assert_affordances_fire(pg, selectors, note=''):
    """assert ว่า element ที่กดได้ (ตาม selector) 'ยิง handler จริง' เมื่อคลิก — จับ listener
    capture-phase ที่ stopPropagation กลืนคลิกทั้งหน้า (บั๊กที่ qc-ux มองไม่เห็น · F-HR-ESS)

    กลไก: ต่อ selector — หา match ที่ 'มองเห็น' ตัวแรก (re-query สด เพื่อให้ element ยังติดใน
    document ตอนคลิก · detached จะไม่วิ่งผ่าน capture ancestor จริง) → ติด probe listener บน
    target เอง (bubble) → el.click() (คลิกจริงผ่าน capture→target→bubble) → อ่านว่า probe ยิงมั้ย.
    ถ้า capture-phase ancestor เรียก stopPropagation event จะไม่ถึง target → probe เงียบ = 'ตาย'.
    selector ที่ไม่มี match มองเห็น = ข้าม (absent · ไม่นับตาย). คืน dict ถ้าผ่าน · โยน
    AssertionError พร้อมรายชื่อ selector ที่คลิกไม่ถึง target ถ้าพัง.
    """
    r = pg.evaluate(
        r"""(arg) => {
          const selectors = arg.selectors || [];
          const vis = el => { const rc = el.getBoundingClientRect(), cs = getComputedStyle(el);
            return rc.width > 0 && rc.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
          const dead = [], tested = [], absent = [];
          selectors.forEach(s => {
            // re-query สด: element ต้องยังติดใน document ตอนคลิก (การคลิก selector ก่อนหน้าอาจ
            //   navigate/render ใหม่) — detached node จะไม่วิ่งผ่าน capture ancestor จริง
            const el = [...document.querySelectorAll(s)].find(vis);
            if (!el) { absent.push(s); return; }
            let fired = false;
            const probe = () => { fired = true; };
            el.addEventListener('click', probe, false);
            try { el.click(); } catch (e) {}
            el.removeEventListener('click', probe, false);
            tested.push(s);
            if (!fired) dead.push(s);
          });
          return { dead, tested, absent };
        }""",
        {"selectors": list(selectors)})
    dead = r["dead"]
    assert not dead, (f"[{note}] คลิกไม่ถึง target (capture-phase กลืนคลิก?): {dead} · "
                      f"tested={r['tested']} · absent={r['absent']}")
    return r


# ⭐ เพิ่ม 2026-09-11 (F-MKT-CONSENT · §C3.8 · user-found cosmetic bugs ที่ตัววัดเดิมมองไม่เห็น)
# ─────────────────────────────────────────────────────────────────────────────
# 3 จุดที่ผู้ใช้เห็นเองแต่ qc-ux/e2e เดิมมองไม่เห็น — ล้วนเป็น "ระยะหายใจ" (spacing) ที่บวกอยู่
# แต่แคบเกินไป จึงไม่ทับ ไม่ล้น ไม่ตัด → ทุกตัวนับเดิมเงียบหมด:
#   (1) filter-bar แปะชิดการ์ดตาราง (แท็บทะเบียน) — margin-bottom หาย → แถวกรองติดหัวตาราง
#   (2) ปุ่มในลิ้นชัก/หน้าต่างชิดกัน — gap ของ container แคบ → ปุ่มติดกันอ่านเป็นก้อนเดียว
#   (3) กล่องเตือนใน modal ออกเวอร์ชันใหม่ อึดอัด — modal-body padding-top + warn-banner padding น้อย
#
# ทำไมตัววัดเดิมมองไม่เห็น: JS_LAYOUT วัด "ทับ/ล้น/สูงไม่เท่า/ถูกตัด" — ไม่มีข้อไหนถามว่า
#   "สององค์ประกอบที่ควรมีช่องไฟ กลับชิดกันเกินไป" (gap เป็นบวกแต่เล็ก = ผ่านทุกข้อ). ข้อ stackFlush
#   ตรวจเฉพาะลูก static+rounded ระดับ .content/.drawer-body/.modal-body — filter-bar→card ผ่านเมื่อ
#   margin แค่บางลง(ไม่ถึง 0) · ปุ่มใน footer เป็น inline-flex แถวเดียว (stackFlush ดูเฉพาะแถวซ้อน) ·
#   ไม่มีใครวัด clearance ของ warn-banner ใต้หัว modal เลย.
# ทั้ง 3 ตัวเป็น opt-in (feature เรียกเองใน e2e) · threshold อนุรักษ์นิยม (≥8 / ≥12) กัน false-positive
# ระยะปกติของ kit. พิสูจน์ว่าจับได้จริงด้วยการย้อน style ให้พัง (ดู e2e-consent.py E33/E34/E35 · C3.8).

# (1) filter-bar ต้องไม่แปะชิดการ์ด/ตารางที่ตามหลัง — ขอบล่างเว้น ≥ MIN px
JS_FILTER_FLUSH = r"""
(arg) => {
  const MIN = arg.min || 8;
  const vis = el => { const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return r.width > 4 && r.height > 4 && cs.display !== 'none' && cs.visibility !== 'hidden'
           && parseFloat(cs.opacity || '1') >= 0.05; };
  const bars = [...document.querySelectorAll('.filter-bar')].filter(vis);
  if (!bars.length) return { ok: false, why: 'no-filter-bar' };
  const cards = [...document.querySelectorAll('.card, table.table, .table-wrap, .table')].filter(vis);
  const pairs = [], bad = [];
  bars.forEach(bar => {
    const br = bar.getBoundingClientRect();
    // การ์ด/ตารางที่ "ตามหลัง" filter-bar: อยู่ต่ำลงมา (top >= bar.top) และไม่ใช่กล่องที่ห่อ/ถูกห่อโดย bar
    const below = cards.filter(c => !c.contains(bar) && !bar.contains(c)
                    && c.getBoundingClientRect().top >= br.top)
                    .sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
    if (!below.length) return;                 // ไม่มีตารางตามหลัง — ไม่นับเป็นความผิด
    const card = below[0], cr = card.getBoundingClientRect();
    const gap = Math.round(cr.top - br.bottom);
    const rec = { bar: (bar.className || '').toString().slice(0, 24),
                  card: (card.className || card.tagName).toString().slice(0, 24), gap };
    pairs.push(rec);
    if (gap < MIN) bad.push(rec);
  });
  const minGap = pairs.length ? Math.min(...pairs.map(p => p.gap)) : null;
  return { ok: bad.length === 0, bad, pairs, minGap, min: MIN, checked: pairs.length };
}
"""


def assert_filter_not_flush(pg, note=''):
    """assert ว่าแถบกรอง .filter-bar ไม่แปะชิดการ์ด/ตารางที่ตามหลัง (F-MKT-CONSENT · C3.8 · bug#1)

    ขอบล่าง .filter-bar ที่มองเห็น ต้องเว้น ≥ 8px เหนือขอบบนของตาราง/การ์ดที่ตามมา —
    flush/ทับ = fail. เรียกตอนอยู่แท็บที่มี filter-bar + ตาราง (เช่น registry). คืน dict ถ้าผ่าน
    """
    r = pg.evaluate(JS_FILTER_FLUSH, {'min': 8})
    if isinstance(r, dict) and r.get('why') == 'no-filter-bar':
        raise AssertionError(f"assert_filter_not_flush {note}: ไม่พบ .filter-bar ที่มองเห็นบนจอ")
    assert r['ok'], (f"[{note}] filter-bar แปะชิดตาราง/การ์ดที่ตามหลัง (ระยะหายใจหาย): "
                     + ' · '.join(f"{b['bar']}→{b['card']} เว้นแค่ {b['gap']}px (ต้อง ≥ {r['min']}px)"
                                  for b in r['bad']))
    return r


# (2) ปุ่มที่อยู่ติดกันในแต่ละ container ต้องมีช่องไฟ ≥ min_gap px (แนวนอนสำหรับแถว · แนวตั้งสำหรับกอง)
JS_ACTION_BTN_GAP = r"""
(arg) => {
  const sels = arg.selectors || [];
  const MIN = arg.min || 8;
  const vis = el => { const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return r.width > 1 && r.height > 1 && cs.display !== 'none' && cs.visibility !== 'hidden'
           && parseFloat(cs.opacity || '1') >= 0.05; };
  const tested = [], absent = [], bad = [], pairs = [];
  sels.forEach(sel => {
    const conts = [...document.querySelectorAll(sel)].filter(vis);
    if (!conts.length) { absent.push(sel); return; }
    let sawPair = false;
    conts.forEach(cont => {
      let btns = [...cont.querySelectorAll('button, .btn, a.btn')].filter(vis);
      btns = btns.filter(b => !btns.some(o => o !== b && o.contains(b)));   // ปุ่มซ้อนปุ่ม → เก็บตัวนอก
      if (btns.length < 2) return;
      const R = btns.map(b => { const r = b.getBoundingClientRect();
        return { l: r.left, r: r.right, t: r.top, b: r.bottom,
                 tx: (b.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 12) }; });
      R.sort((a, b) => (a.t - b.t) || (a.l - b.l));
      for (let i = 1; i < R.length; i++) {
        const a = R[i - 1], c = R[i];
        const yOverlap = Math.min(a.b, c.b) - Math.max(a.t, c.t);
        const xOverlap = Math.min(a.r, c.r) - Math.max(a.l, c.l);
        let axis, gap;
        if (yOverlap > 2) { axis = 'h'; gap = Math.round(c.l - a.r); }        // แถวเดียวกัน → ช่องไฟแนวนอน
        else if (xOverlap > 2) { axis = 'v'; gap = Math.round(c.t - a.b); }   // กองซ้อน → ช่องไฟแนวตั้ง
        else continue;                                                         // ทแยงกัน → ไม่ถือว่าติดกัน
        sawPair = true;
        const rec = { sel, axis, gap, a: a.tx, b: c.tx };
        pairs.push(rec);
        if (gap < MIN) bad.push(rec);
      }
    });
    if (sawPair) tested.push(sel);
  });
  return { ok: bad.length === 0, bad, pairs, tested, absent, min: MIN };
}
"""


def assert_action_button_gap(pg, container_sels, min_gap=8, note=''):
    """assert ว่าปุ่มที่ "อยู่ติดกัน" ในแต่ละ container มีช่องไฟ ≥ min_gap px (F-MKT-CONSENT · C3.8 · bug#2)

    container_sels : selector เดียว หรือ list ของ selector (เช่น ['.dw-footer-right','.modal-footer']).
    แต่ละคู่ปุ่มที่มองเห็นและอยู่ติดกัน — แถวเดียวกันวัดช่องไฟแนวนอน · ซ้อนกันวัดแนวตั้ง · คู่ที่ทแยงข้าม
    (space-between ซ้าย↔ขวา) ไม่ถือว่าติดกันจึงข้าม. container ที่มีปุ่ม < 2 ตัว = ข้าม (ไม่นับ).
    คืน dict {ok,bad,pairs,tested,absent} ถ้าผ่าน · โยน AssertionError พร้อม px ที่วัดได้ถ้าพัง.
    """
    if isinstance(container_sels, str):
        container_sels = [container_sels]
    r = pg.evaluate(JS_ACTION_BTN_GAP, {'selectors': list(container_sels), 'min': min_gap})
    assert r['ok'], (f"[{note}] ปุ่มที่อยู่ติดกันชิดเกินไป (ช่องไฟ < {r['min']}px): "
                     + ' · '.join(
                         f"“{b['a']}”↔“{b['b']}” ({'แนวนอน' if b['axis'] == 'h' else 'แนวตั้ง'}) "
                         f"เว้นแค่ {b['gap']}px @{b['sel']}" for b in r['bad']))
    return r


# (3) กล่องเตือน .warn-banner ใน modal ที่เปิดอยู่ ต้องไม่อึดอัด: เว้นใต้หัว modal + padding เพียงพอ
JS_MODAL_WARN_CRAMPED = r"""
(arg) => {
  const MINCLR = arg.clear || 8, MINPAD = arg.pad || 12;
  const vis = el => { const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return r.width > 4 && r.height > 4 && cs.display !== 'none' && cs.visibility !== 'hidden'
           && parseFloat(cs.opacity || '1') >= 0.05; };
  // modal ที่เปิดอยู่ (z สูงสุดถ้ามีหลายชั้น)
  const modal = [...document.querySelectorAll('.modal, [role=dialog]')].filter(vis)
    .sort((a, b) => (parseInt(getComputedStyle(b).zIndex) || 0) - (parseInt(getComputedStyle(a).zIndex) || 0))[0];
  if (!modal) return { ok: false, why: 'no-open-modal' };
  const head = [...modal.querySelectorAll('.modal-header')].filter(vis)[0];
  const warn = [...modal.querySelectorAll('.warn-banner')].filter(vis)[0];
  if (!warn) return { ok: false, why: 'no-warn-banner' };
  const cs = getComputedStyle(warn);
  const pad = { t: parseFloat(cs.paddingTop) || 0, r: parseFloat(cs.paddingRight) || 0,
                b: parseFloat(cs.paddingBottom) || 0, l: parseFloat(cs.paddingLeft) || 0 };
  const bad = [];
  let clearance = null;
  if (head) {
    clearance = Math.round(warn.getBoundingClientRect().top - head.getBoundingClientRect().bottom);
    if (clearance < MINCLR) bad.push({ why: 'clearance', px: clearance, min: MINCLR });
  }
  ['t', 'r', 'b', 'l'].forEach(k => {
    if (pad[k] < MINPAD) bad.push({ why: 'padding-' + k, px: Math.round(pad[k]), min: MINPAD }); });
  return { ok: bad.length === 0, bad, clearance,
           padding: [Math.round(pad.t), Math.round(pad.r), Math.round(pad.b), Math.round(pad.l)],
           minClear: MINCLR, minPad: MINPAD };
}
"""


def assert_modal_warn_not_cramped(pg, note=''):
    """assert ว่ากล่องเตือน .warn-banner ใน modal ที่เปิดอยู่ ไม่อึดอัด (F-MKT-CONSENT · C3.8 · bug#3)

    (a) ขอบบน .warn-banner ต้องเว้นใต้ขอบล่าง .modal-header ≥ 8px · (b) computed padding ทั้ง 4 ด้าน
    ต้อง ≥ 12px. เรียก "หลัง" เปิด modal ที่มี .warn-banner แล้ว (เช่น new-version). คืน dict ถ้าผ่าน ·
    โยน AssertionError ถ้าไม่มี modal/ไม่มี warn-banner หรืออึดอัด (พร้อม px ที่วัดได้)
    """
    r = pg.evaluate(JS_MODAL_WARN_CRAMPED, {'clear': 8, 'pad': 12})
    if isinstance(r, dict) and r.get('why'):
        raise AssertionError(f"assert_modal_warn_not_cramped {note}: {r['why']} "
                             f"(ต้องเปิด modal ที่มี .warn-banner ก่อนเรียก)")
    assert r['ok'], (f"[{note}] กล่องเตือนใน modal อึดอัด: "
                     + ' · '.join(
                         (f"ชิดใต้หัว modal แค่ {b['px']}px (ต้อง ≥ {b['min']}px)" if b['why'] == 'clearance'
                          else f"padding {b['why'].split('-')[1]} แค่ {b['px']}px (ต้อง ≥ {b['min']}px)")
                         for b in r['bad'])
                     + f" · [clearance={r['clearance']} · padding(t/r/b/l)={r['padding']}]")
    return r


# ─────────────────────────────────────────────────────────────────────────────
# C3.8 · interaction-guard helpers (append-only · 2026-09-14 · from F-MKT-CONSENT BA-gate)
# มาจาก bypass ที่ e2e/qc เดิมมองไม่เห็น: (a) mutation ตอบซ้ำ/ยิงซ้ำเพราะไม่มี _busy
# (double submit) · (b) read-only persona เรียก mutation ตรงผ่าน (persona guard เป็น UI-only).
# คลาสเดียวกับที่เคย block F101/F102/F131 มาแล้ว → generalize เป็นตัวตรวจกลาง.
# ทั้งคู่ generic: รับ JS snippet (fire/mutate + counter) — ไม่ผูกกับฟีเจอร์ใดฟีเจอร์หนึ่ง.
# ─────────────────────────────────────────────────────────────────────────────

def assert_double_submit_single(pg, fire_js, count_js, note=''):
    """ยิง mutation 2 ครั้งติดกันแบบ synchronous (ก่อน re-render/timeout จะรีเซ็ต busy flag)
    แล้ว counter ต้องเพิ่มไม่เกิน 1 = มี guard กัน double-submit จริง (Rule #44 / pattern F101).

    fire_js  : นิพจน์/คำสั่งเรียก mutation เช่น "submitReqCreate()" (ไม่ต้องมี arrow)
    count_js : นิพจน์นับผลลัพธ์ เช่น "state.requests.length"
    เรียกหลังจัดสถานะให้พร้อม submit แล้ว. คืน dict {before,after,delta} ถ้าผ่าน ·
    โยน AssertionError ถ้า delta > 1 (double submit หลุด).
    """
    before = pg.evaluate("() => (%s)" % count_js)
    pg.evaluate("() => { (%s); (%s); }" % (fire_js, fire_js))   # สองครั้งใน tick เดียว
    after_ = pg.evaluate("() => (%s)" % count_js)
    delta = after_ - before
    assert delta <= 1, (f"[{note}] double-submit หลุด: ยิง 2 ครั้งติดกัน → counter +{delta} "
                        f"(ต้อง ≤1 · {before}→{after_}) — ขาด _busy/loading guard")
    return {'before': before, 'after': after_, 'delta': delta}


def assert_role_write_blocked(pg, mutate_js, count_js, note=''):
    """ตั้ง read-only persona/บทบาทไว้ก่อน (โดยผู้เรียก) แล้วเรียก mutation ตรง → counter ต้องไม่ขยับ
    = guard อยู่ "ในฟังก์ชัน" ไม่ใช่แค่ตอน render ปุ่ม (persona/role bypass — B4 class).

    mutate_js : คำสั่งเรียก mutation ตรง เช่น "answerRequest('REQ-2601','all')"
    count_js  : นิพจน์นับ state ที่ mutation จะแก้ เช่น "state.consents.length"
    คืน dict {before,after} ถ้าผ่าน · โยน AssertionError ถ้า state เปลี่ยน (บทบาทอ่านอย่างเดียวเขียนได้).
    """
    before = pg.evaluate("() => (%s)" % count_js)
    pg.evaluate("() => { try { (%s); } catch(e){} }" % mutate_js)
    after_ = pg.evaluate("() => (%s)" % count_js)
    assert after_ == before, (f"[{note}] persona/role guard เป็น UI-only: บทบาทอ่านอย่างเดียวเรียก "
                              f"mutation ตรงแล้ว state เปลี่ยน ({before}→{after_}) — ต้อง guard ในฟังก์ชัน")
    return {'before': before, 'after': after_}
