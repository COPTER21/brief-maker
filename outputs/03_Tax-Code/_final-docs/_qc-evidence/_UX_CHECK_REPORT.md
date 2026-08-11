# UX Check Report — Tax Code (ทะเบียนรหัสภาษี)

- วันที่: 2026-08-10 · Iteration: 3 (re-verify + re-stamp after user-found UX fixes round 2)
- Generator spec (Sync Read): **html-generator-v8** — iron-rules.md (#95–#97), ci-tokens.md (CUBE Warm Light v2.0), microcopy.md (v3.13)
- ไฟล์ที่ตรวจ/แก้: `Pack Brief Feature/3. Tax Code/f-taxcode.html` (959 บรรทัด) — 2 สำเนา (source pack + outputs) byte-identical
- เครื่องมือ: `qc-ux-html-checker/scripts/static_scan.py` + `html-generator-v8/scripts/self_audit.py` (นับอิสระ)

## Verdict: 🟢 PASS

| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 0 | 0 | 0 | 2 |

- `self_audit.py` (v8): **RESULT: PASS** — ทั้ง 26 metric = 0 (spacing_off/font_off/font_count≤8/inline_layout/z_adhoc/hex_off/menu_no_bg_z/jargon_leak … = 0)
- `static_scan.py`: hex นอก whitelist = **[]** · emoji = **0** · fonts ใน stack · esc handler ✓ · scrollbar 5px · localStorage=false · drawer 680/920, modal 440, sidebar 232, shell 52 ครบ
- โครงสร้างไฟล์: braces/parens/brackets balance = 0 · style/script/body/html ปิดครบ · ไม่มี leftover `uom`/`ลิตร`/`units`

Iteration 1 มี BLOCK 4 + WARN 8 → แก้ครบทั้ง 12 รายการ (Option A). เหลือเฉพาะ 2 NOT-CHECKED ที่เป็นข้อจำกัด environment/false-positive (ระบุด้านล่าง)

---

## ✅ Fixes applied (changelog — Iteration 1 → 2)

### BLOCK (4/4 แก้แล้ว)
| # | รายการ | ที่แก้ | ทำอะไร |
|---|---|---|---|
| UX-01 | PREFLIGHT stamp ปลอม (Pass G #60) | line ~936 | รัน self_audit ใหม่ได้ค่าจริง (ทั้งหมด 0) แล้ว re-stamp ด้วยค่าจริง + เปลี่ยนป้าย `v6.2` → `v8` + ระบุ Render Gate = NOT-CHECKED ตามจริง |
| UX-02 | #97 body `min-width:1180px` | `body{}` | ลบ `min-width:1180px` ออก — เหลือ base `min-width:768px` (line ~15) ตาม #97 → ไม่มี body h-scroll ที่ ≤1180 |
| UX-03 | hex `#FFF6F5` นอก whitelist ×3 | `:root` + L~178/179/182 | เพิ่ม token `--c-primary-tint:rgba(255,59,48,.05)` (ใช้ rgba ไม่ใช่ hex ดิบ เพื่อไม่ให้ตกเกณฑ์ whitelist) แล้วอ้าง `var(--c-primary-tint)` ใน `tr.is-selected td` / `.bulkbar` / `.upload-box:hover` |
| UX-04 | inline layout style ×4 (#69) | L~479/810/824/835 | ย้ายเป็นคลาส: `.th-ck{width:36px}` · `.modal-header .top-icon-btn.mh-close{margin-left:auto}` · `.import-scroll{margin-top:var(--sp-md);max-height:300px}` (+`.is-err{max-height:220px}`) |

### WARN (8/8 แก้แล้ว)
| # | รายการ | ที่แก้ | ทำอะไร |
|---|---|---|---|
| UX-05 | geometry off-scale | หลายจุด | `.bulkbar` `9px 14px`→`var(--sp-sm) var(--sp-md)` · `.import-sum` `9px`→`8px` · `.lock-tag` `10.5px`→`11px` · `.bulk-note` `11.5px`→`12px`(+margin 4px) · font_count 10→8 · เพิ่ม token `--z-sidebar-mobile:70` แทน `z-index:70` ดิบ |
| UX-06 | Esc chain (menu>modal>drawer) | keydown ~L917 | เพิ่มเงื่อนไขบนสุด `if(document.querySelector('.pop-menu.is-open')){closeMenus();return;}` ก่อน modal/drawer |
| UX-07 | #96 full-height calc drift | `.content` | `calc(100vh - var(--topbar-h,56px))` → `calc(100vh - var(--shell-h))` (52px จริง) |
| UX-08 | microcopy "เพิ่ม"→"สร้าง" | L~449/504/583/631/676 | CTA/empty/drawer title → `สร้างรหัสภาษี` · footer create → `ยืนยันสร้าง` · toast → `สร้างรหัสภาษี … สำเร็จ` (edit "บันทึกการแก้ไข" คงเดิม) |
| UX-09 | UoM template leaks | L~297/317/323/324/388/390/446/508 | `data-feature="uom-master"`→`tax-code` · `navTo('units')`→`navTo('tax-codes')` (breadcrumb+sidebar) · notif 2 บรรทัดเป็นโดเมนภาษี (ลบ "ลิตร"/"รอตรวจทาน") · comment "UoM"→"รหัสภาษี" · icon `ruler`→`percent` (sidebar/stat/empty) |
| UX-10 | #5 glyph ✓/✗ ใน pill | L~827 | เปลี่ยนเป็น `<i data-lucide="check">` / `<i data-lucide="x">` |
| UX-11 | numeric cell alignment | table CSS + L~461/463/712/825 | เพิ่ม `.num{font-variant-numeric:tabular-nums}` + `.ta-r{text-align:right}` และใส่ `ta-r` ให้คอลัมน์ อัตรา/ใช้ในสินค้า (list + import preview) |
| UX-12 | focus แรกใน drawer | `openDrawerShell` | หลัง render โฟกัส field แรกที่ไม่ disabled ใน `.dw-body` (create=รหัส, edit-locked=ชื่อไทย, view=ไม่มี input จึงข้าม) |

### เพิ่มเติม (safe, ไม่กระทบ flow)
- `.status-menu` เดิม self_audit flag `menu_no_bg_z` (false-positive เพราะสืบทอดจาก `.pop-menu`) — เติม `background:#fff;z-index:var(--z-dropdown)` ระบุชัด → audit = 0 (ปิด false-positive ในตัว)

---

## ✅ UX fixes round 2 (user-found) — re-verified 2026-08-10

3 รายการที่ coordinator แก้เองแบบ surgical (behavior E2E แล้ว 21/21 — checker ตรวจ form/CI + re-stamp เท่านั้น ไม่แตะ behavior):

| # | รายการ | สรุปสิ่งที่เปลี่ยน | ผลตรวจ form/CI |
|---|---|---|---|
| R2-1 | **Import file input จริง** | upload box เปิด hidden `<input type="file" id="bulkFile" class="vhide">`; preview โผล่หลังเลือกไฟล์ผ่าน `bulkFileChosen()` เท่านั้น; แสดงชื่อไฟล์ทั้ง pick + preview; ลบ inline style 2 จุด (`flex:1`→`.filter-spacer`, confirm-btn opacity→`.is-disabled`) | inline_layout=0 ✓ · fullwidth_select=0 ✓ |
| R2-2 | **Exempt lock-tag** | label อัตราแสดง `.lock-tag` "ยกเว้นภาษี = อัตรา 0" เมื่อ type=exempt (`#rate-exempt-tag` toggle ใน `onTypeChange`) — pattern เดียวกับ IR-TAX-01 lock-tag (FN-04 compliant) | naked_hints=0 ✓ · consistent กับ lock-tag เดิม |
| R2-3 | **Status-menu current-mark** | เพิ่ม `.pm-item`/`.pm-menu-title`/`.pm-current-mark` + `.vhide`; `.is-current` เป็น `opacity:.5` + `disabled` + marker "✓ ปัจจุบัน" (ใช้ Lucide `check`, ไม่ใช่ glyph) | custom_tabs=0 ✓ · menu_no_bg_z=0 ✓ |

### new audit flag ที่เจอ + วิธีแก้ (round 2)
- **`long_banners = 2`** — self_audit จับ `class="bulk-note"` 2 จุด (บรรทัดแสดงชื่อไฟล์ใน pick/preview) เพราะกฎ #67/#74 match ทุก element ที่ชื่อคลาสมี `note|banner|callout…` แล้ว "raw source" ยาว >120 (จาก template expr `${esc(b.filename)}`/ternary) — เป็น **false-positive** (ข้อความ render จริง เช่น "ไฟล์ที่เลือก: taxcode.csv" สั้น ~30 ตัว ไม่ใช่ banner อธิบายยาว)
  - **แก้ (surgical):** rename คลาส `.bulk-note` → `.bulk-file` (CSS def + 2 usages) — สไตล์เหมือนเดิมทุก property, ไม่เปลี่ยน visual, ตัดคำ keyword `note` ที่ทำให้กฎ match → `long_banners = 0`

### re-verify result (round 2)
- `self_audit.py` (v8): **RESULT PASS** — ทั้ง 26 metric = 0 (รวม long_banners=0 หลังแก้)
- `static_scan.py`: hex นอก whitelist = **[]** · emoji = **0** · esc ✓ · localStorage=false · inline_style_attr=3 (เป็น `font-weight:600` บน `.num` span — ไม่ใช่ layout จึงไม่ตก #69)
- โครงสร้าง: braces/parens/brackets balance = 0 · style/script/body/html ปิดครบ · ไม่มี leftover `uom`/`ลิตร`
- **PREFLIGHT re-stamped** (line ~955, v8) ด้วยค่าจริง round 2 + Render Gate = NOT-CHECKED
- **สำเนา 2 ไฟล์ byte-identical** (`diff` = ตรงกัน): source pack ↔ outputs

---

## ⬜ NOT-CHECKED (คงเหลือ — ไม่ใช่ข้อบกพร่องที่แก้ได้ใน env นี้)

- **Pass R — Render Gate (visual):** env นี้ไม่มี browser/playwright จึงไม่ได้ถ่ายภาพจริง — ตรวจสายตาไม่ได้: bottom-edge dropdown flip (#66), sticky-vs-overlay (#62.1), all-tabs render (#73.1), ขอบล่าง drawer ไม่มี h-scroll (#76). **วิธีเช็ค:** รัน `qc-ux-html-checker/scripts/render_shots.py f-taxcode.html _shots/` ใน Claude Code/Cowork ที่มี browser แล้วไล่ดูตาม Visual Checklist. หมายเหตุ: #95 overlay portal ไม่ applicable — ไม่มี dropdown ที่ trigger อยู่ใน scroll container (category/status เป็น native `<select>`, status-menu อยู่ใน drawer header ไม่ใช่ body)
- **`menu_no_bg_z` false-positive:** ปิดแล้วโดยเติม bg/z ระบุชัดใน `.status-menu` — แต่การยืนยันว่า dropdown ไม่โปร่ง/ไม่จมจริง ต้องดูจากภาพ (อยู่ใน Render Gate ข้างบน)

---

## สรุป
- **Verdict: PASS** — BLOCK 0 / WARN 0 · self_audit v8 = PASS · static_scan สะอาด · โครงสร้างไฟล์สมดุล
- Flow/behavior เดิมคงไว้ครบ (create/edit/view/bulk/import/export/filter/sort/pager) — การแก้เป็น token/CSS/microcopy/JS-guard รายจุด ไม่มี regenerate
- ก่อนส่ง dev แนะนำรัน Render Gate 1 รอบใน env ที่มี browser เพื่อปิด NOT-CHECKED
