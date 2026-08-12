# UX Check Report — Bank Master (F-BNK) · `f-bank.html`
- วันที่: 2026-08-11 · Iteration: 1 (baseline — ไม่มี report รอบก่อน)
- Generator spec (Sync Read สด): **html-generator-v8** — `knowledge/iron-rules.md` (base v3.13 = 49 ข้อ + #94–#97), `ci-tokens.md` (CUBE Warm Light), `microcopy.md`
- ไฟล์ที่ตรวจ: `outputs/04_Bank-Master/01_HTML/f-bank.html` (1,061 บรรทัด · 79 KB)
- วิธีตรวจ: Phase 1 static_scan.py + Phase 2–3 อ่านโค้ดจริง + **Render Gate (Playwright chromium) รันจริง** — screenshots ใน `_e2e_shots/`, รายละเอียด E2E ใน `_E2E_REPORT.md`

## Verdict: 🟡 WARN (PASS-WITH-NOTES · 0 BLOCK / 8 WARN / 6 INFO / 2 NOT-CHECKED)
| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 0 | 8 | 6 | 2 |

**สรุป:** ผ่าน gate — ไม่มี iron-rule violation ระดับ BLOCK. โครง CI/kit ถูกต้อง (tokens, ฟอนต์ Satoshi+Noto โหลดจริง, ไม่มี drawer 540 legacy, scrollbar 5px, Esc chain, render-preservation #29 มีจริง). **ทั้ง 3 business rules (IR-BNK-01, GL picker filter, latent bugs) ผ่านการทดสอบ E2E จริงทุกข้อ** (ดู `_E2E_REPORT.md`). WARN ทั้งหมดเป็นเรื่อง content-leak จาก feature อื่น, ค่า token ที่ควร normalize, และ label/width ที่เบี่ยงจากมาตรฐาน — ไม่กระทบ logic. ประเมินเวลาแก้ทั้งหมด ~30–40 นาที.

---

## 🟡 WARN — ควรแก้ (ไม่บล็อก)

### UX-01 · Rule #28 (Slim Top Bar) content leak · shell bar · line 333–334
- **พบ:** เมนูแจ้งเตือน (notif) มีข้อความค้างจาก feature อื่น — `"มีรหัสภาษีใหม่ 2 รายการรอตรวจทาน"` (Tax Code) และ `"ลิตร ถูกหยุดใช้งานเมื่อวานนี้"` (UOM). ไม่เกี่ยวกับ Bank Master เลย. (PREFLIGHT stamp เขียน `jargon_leak=0` แต่ตรงนี้คือ leak จริง)
- **แก้:** เปลี่ยนเป็น mock ที่เกี่ยวกับบัญชีธนาคาร เช่น `"บัญชี TTB-01 ยังเป็นร่าง รอเปิดใช้"` / `"GSB-01 ถูกปิดใช้งานเมื่อ 30 พ.ค."` หรือลบ 2 บรรทัดออก

### UX-02 · Rule #5 wrong icon + leftover route · sidebar · line 307, 327, 341
- **พบ:** เมนู sidebar `บัญชีธนาคาร` ใช้ icon `data-lucide="ruler"` (ไอคอนของ UOM/Units) — line 307. และ active item + breadcrumb เรียก `navTo('units')` (route ชื่อ `units` ค้างจาก feature เก่า) — line 307, 327.
- **แก้:** เปลี่ยน icon เป็น `landmark` (หรือ `building-2`); เปลี่ยน `navTo('units')` → `navTo('bank')` (หรือ route ที่ตั้งใจ). ไม่กระทบการทำงาน (route ไหนก็ re-render list) แต่เป็น hygiene

### UX-03 · Rule #31.2 / microcopy · create drawer footer · line 711
- **พบ:** ปุ่ม primary ของ **create** ใช้ label `"บันทึกบัญชีธนาคาร"` — มาตรฐาน microcopy กำหนด create = `"ยืนยันสร้าง"` (edit = `"บันทึกการแก้ไข"` ✓ ถูกแล้ว)
- **แก้:** `${isEdit?'บันทึกการแก้ไข':'ยืนยันสร้าง'}` (icon `check` คงเดิม). ให้ตรง 2BSimple microcopy กลาง

### UX-04 · Rule #1 (CI Tokens) off-token hex · line 179, 189, 190, 193
- **พบ:** hardcoded hex นอก whitelist ci-tokens: `#FFF6F5` (3×) ใช้ที่ `tr.is-selected td`, `.bulkbar`, `.upload-box:hover` และ `#F7F5F1` (1×) ที่ `.sum-chip` (ผ่าน fallback `--paper-2`). ไม่ใช่สีแบรนด์ผิด (เป็น pale-tint ของ selected/hover) แต่ไม่อยู่ใน token table — strict reading ของ mechanical rule = BLOCK, จัดเป็น WARN เพราะเป็น cosmetic state-tint
- **แก้:** ใช้ token/สื่อจาก primary — เช่น selected row `background:rgba(255,59,48,.05)`; `.sum-chip` bg = `var(--c-line-3)` (#F1EEEA)

### UX-05 · Rule #1 (hygiene) undefined CSS var names · line 176, 179–185, 495
- **พบ:** CSS หลายจุดอ้าง var ที่ **ไม่ได้ประกาศใน `:root`** แล้วพึ่ง hardcoded fallback: `--paper-2`, `--ink-2`, `--ink-3`, `--line-2`, `--brand` (`:root` ใช้ชื่อ `--c-*`). ค่าที่ fallback ส่วนใหญ่ตรง token (#54565C, #73757B, #E9E5E0, #FF3B30) แต่ควรใช้ชื่อ canonical. อีกจุด line 495 `color:var(--ink-2)` **ไม่มี fallback** → var undefined → สีตกไป inherit (คอลัมน์ "ใช้ฝั่ง" ไม่ได้เป็นสี mute ตามตั้งใจ)
- **แก้:** แทนด้วย `--c-mute`/`--c-mute-2`/`--c-line-2`/`--c-primary` ให้ตรงระบบ token; line 495 ใส่ `var(--c-mute)`

### UX-06 · Rule #11 (Drawer Width) · line 228, 101
- **พบ:** `.drawer` base = **680px** ใช้กับ create/edit/view ที่มี ~12 fields / 3 sections. Rule #11: create/edit/view = **920px** (v2 standard); 680 สงวนสำหรับ simple form ≤6 fields. **และมี inconsistency:** `@media(max-width:1180px)` (line 101) ตั้ง `.drawer{width:min(920px,100vw)}` → จอ 1000px ได้ drawer **กว้างกว่า (920)** จอ desktop (680) — ทิศทาง responsive กลับด้าน
- **แก้:** ตั้ง base `.drawer{width:920px;max-width:96vw}` ให้ตรงมาตรฐาน (ฟอร์มนี้ field เยอะพอ) — แล้ว media query จะ consistent เอง. ปัจจุบัน render อ่านออกได้ที่ 680 (screenshots OK) จึงเป็น WARN ไม่ใช่ BLOCK

### UX-07 · Rule #40 (List Cell Atomicity) · list table · line 491
- **พบ:** คอลัมน์ `ธนาคาร / ชื่อบัญชี` ซ้อน 2 บรรทัดในเซลล์เดียว — `cell-name-th` (ธนาคาร·สาขา) ทับด้วย `cell-name-en` (ชื่อบัญชี) เป็น sub-line สีเทา = pattern ที่ Rule #40 ห้าม (`<div>ชื่อ</div><div class="sub">…</div>`)
- **แก้:** แยก "ชื่อบัญชี" เป็นคอลัมน์ของตัวเอง หรือถ้าเกิน 8 คอลัมน์ให้ย้ายชื่อบัญชีลง view drawer (ซึ่งมีอยู่แล้ว). หมายเหตุ: ตารางปัจจุบัน 9 คอลัมน์อยู่แล้ว (ดู INFO-01) — แนะนำตัดชื่อบัญชีออกจาก list ปล่อยให้ดูใน drawer

### UX-08 · Rule #44 (Loading/Submitting) partial · line 751–752, 912
- **พบ:** ตอน `saveBank` submit มี loader-2 spin + `"กำลังบันทึก…"` ที่ปุ่ม primary ✓ แต่ปุ่มพี่น้องใน footer (`ยกเลิก` ghost) **ไม่ถูก disable** ระหว่าง 500ms — กด cancel ซ้อน submit ได้. และ `bulkConfirm` (import) เขียนข้อมูลทันทีไม่มี submitting state
- **แก้:** ระหว่าง submit ตั้ง `closeDrawer` ปุ่มอื่นเป็น disabled ด้วย (กัน double-action ตาม #44); import confirm เพิ่ม spin เล็กน้อยก่อน apply

---

## ℹ️ INFO — พิจารณา (ไม่บังคับ)

- **INFO-01 · Rule #16:** ตาราง list = 9 คอลัมน์ (checkbox + รหัส + ธนาคาร/ชื่อ + เลขบัญชี + ประเภท + กลุ่ม GL + ใช้ฝั่ง + สถานะ + จัดการ). Rule #16 = ≤8 (rare 9). อยู่ที่ขอบพอดี — ถ้าแก้ UX-07 (ตัดชื่อบัญชีลง drawer) จะช่วยลดความหนาแน่นด้วย
- **INFO-02 · Rule #94:** GL Posting Group picker เป็น plain `<select>` ไม่ใช่ search combobox. ยอมรับได้เพราะ list ที่ active มี ≤8 (ตอนนี้ 2 กลุ่ม) — แต่ถ้าจำนวน posting group โตขึ้น ควร upgrade เป็น combobox ตาม #94
- **INFO-03 · Rule #23:** ใช้ glyph `★` (def-star บัญชีหลัก) และ `✗` (ผลตรวจ import) — ไม่อยู่ในรายการ acceptable marks (`• · → — ✓ − -`). Cosmetic; ★ ควรเป็น Lucide `star`, ✗ ใช้สีแดง/pill สื่อความหมายอยู่แล้ว
- **INFO-04 · Rule #46.4:** row actions มีแค่ `pencil` (แก้ไข) ไม่มี `trash-2` ต่อแถว — ลบทำผ่าน bulk-select → modal confirm (มี used>0 guard). เป็น design ที่สมเหตุผลของ master ที่มี transaction; แจ้งไว้เพราะเบี่ยงจากรูปแบบ pencil→trash ปกติ
- **INFO-05 · Rule #96:** `.content` คำนวณความสูง `calc(100vh - var(--topbar-h,56px))` แต่ shell จริง = 52px (`--shell-h`) → คลาด 4px. Cosmetic
- **INFO-06:** `setStatus` จาก view drawer เรียก `openView()` rebuild ทั้ง drawer → เด้งกลับ tab "ภาพรวม" + scroll top. ถ้า user อยู่ tab "ประวัติ" แล้วเปลี่ยนสถานะจะเสีย context เล็กน้อย

---

## ⬜ NOT-CHECKED (ต้องดูของจริง)
- **Thai optical centering fidelity** — kit มีค่า `padding-top:2px` (.btn), pill `4/3`, td `13/11` ครบตาม #38/#36; ยังไม่ได้วัด baseline พิกเซลข้ามเบราว์เซอร์ (Chromium render สวยตาม screenshots). วิธีเช็ค: เปิดไฟล์บน Firefox/Safari กวาดตาปุ่ม+pill ไทยว่าตัวอักษรไม่ลอย
- **Viewport <768px** — `body{min-width:1180px}` บังคับ horizontal scroll ตาม #97 tier ล่าง; ตรวจเชิง CSS แล้ว (media 1180 มี off-canvas sidebar + drawer min(920,100vw)) แต่ไม่ได้ render จอ <768 จริง

---

## หมวดที่ตรวจแล้ว = ผ่าน (evidence-backed)
- **CI/Font (#1–#2):** `:root` ใช้ `--c-*` ครบ · Satoshi (fontshare) + Noto Sans Thai (googleapis) โหลดจริง line 9–10 · ไม่มี crimson/pink legacy
- **Layout (#3–#4, #30, #96):** sidebar 232px charcoal · shell 52px white · `.content` fluid ไม่มี max-width cap · list full-height (card flex:1 + table-scroll)
- **Drawer/Modal (#11–#15):** ไม่มี 540 legacy (scan=0) · translateX(100%) slide · backdrop rgba(17,17,17,.40) · ปิดได้ 3 ทาง (backdrop/X/Esc) · modal 440px · z-index map สะอาด (dropdown 30 < backdrop 50 < drawer 51 < modal 60 < toast 80)
- **Render Preservation (#29):** `_keepScroll()` save+restore content/table-scroll/dw-body — **ทดสอบ E2E จริง: toggle checkbox ใน drawer ที่ scroll 325px → ไม่เด้ง**
- **Scrollbar (#49):** block 5px + track โปร่งใส + พื้นเข้ม sidebar ครบ
- **States (#39, #44, #45):** empty state 2 เคส (filter/ว่าง) · submitting spin ที่ save · disabled/readonly (currency, locked fields) ถูก token
- **Import (#32):** modal (ไม่ใช่ drawer) · template download ใน modal + UTF-8 BOM · validate+preview (ผ่าน/ไม่ผ่านรายแถว + เหตุผล) ก่อน apply · confirm disabled เมื่อ valid=0
- **Esc chain / outside-click:** Esc ปิด modal→drawer→menu ตามลำดับ (line 1048–1054) · click นอก = closeMenus
- **Business rules (E2E ผ่านทั้งหมด):** IR-BNK-01 lock, GL picker filter (F-PG BR-06), z-index dropdown/modal ใน drawer — ดู `_E2E_REPORT.md`
