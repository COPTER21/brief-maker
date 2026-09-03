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
    except Exception:
        pass
    if url:
        pg.goto(url)
    pg.wait_for_load_state('load')
    pg.evaluate(_JS_PATCH_TIMERS)              # เผื่อหน้าถูกเปิดไปก่อนหน้านี้แล้ว
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
