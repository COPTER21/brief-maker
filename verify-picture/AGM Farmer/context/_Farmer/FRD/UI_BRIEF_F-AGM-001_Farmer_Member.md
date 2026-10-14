# UI BRIEF — F-AGM-001 Farmer Member Management (AS-BUILT)

## §0 Document Control + Pairing

| Field | Value |
|---|---|
| Source HTML | `farmer-member-management.html` (v1.0, 2026-07-20 — html-generator-v6, audit FAIL=0) |
| FRD Pack | `FRD_F-AGM-001_Pack/` (7 ไฟล์, STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-001 APPROVED |
| Drift status | ดู §11 Drift Log — 3 รายการ (log แล้ว ไม่มีเงียบหาย) |
| ผู้อ่านเป้าหมาย | FE/BE dev สร้างระบบจริงจาก HTML + FRD Pack + Brief นี้ |
| กติกา | ทุก claim ใน Brief นี้ชี้ anchor ได้ (selector / function / ข้อความ verbatim) — HTML = source of truth |

---

## §1 Design Tokens AS-BUILT

### CSS Variables (`:root` — CUBE Warm Light)
| Token | ค่า | ใช้ทำ |
|---|---|---|
| `--c-navy` / `--c-navy-2` / `--c-ink` | `#111111` | text หลัก, sidebar, toast bg |
| `--c-primary` / `--c-primary-hover` | `#FF3B30` / `#E62E24` | action หลัก, active sidebar, focus ring |
| `--c-teal` / `--c-teal-light` | `#FF9A1F` / `#FFB763` | connection accent (logo gradient, pulse dot) |
| `--c-mute` / `-2` / `-3` | `#54565C` / `#73757B` / `#9A9CA2` | secondary text ไล่ระดับ |
| `--c-line` / `-2` / `-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | borders ไล่ระดับ |
| `--c-bg-off` | `#FAF8F5` | Ivory ground |
| `--c-success` / `--c-warning` / `--c-danger` | `#1F9D55` / `#E8870F` / `#E62E24` | semantic |
| `--sidebar-w` / `--shell-h` | `232px` / `52px` | shell |
| `--fs-*` | h1 22 / h2 17 / h3 15 / body 14 / sub 13 / meta 12 / cap 11 / kpi 28 | fixed type scale |
| `--sp-*` | 4 / 8 / 12 / 20 / 28 | fixed spacing |
| `--r-*` | 4 / 6 / 8 / 12 / 999 | fixed radius |

Fonts: `'Satoshi', 'Noto Sans Thai', system-ui` (Fontshare + Google Fonts) · Icons: Lucide 0.469.0 (multi-CDN loader ท้าย body, fallback no-op)
Scrollbar: 5px มุมมน track โปร่งใส — พื้นเข้ม (`.sidebar`) thumb ขาวโปร่ง (Rule #49)
Thai optical centering: `.btn { padding: 2px 14px 0 }` · `.pill { 4px 10px 3px }` · `td { 13px 14px 11px }` — ห้ามแก้เป็น line-height:1

### Z-Index Map (สูง → ต่ำ)
| z | Layer | Selector |
|---|---|---|
| 80 | Toast | `.toast` |
| 70 | Search-select list | `.ss-list` |
| 60 | Modal backdrop | `.modal-backdrop` |
| 50 | Drawer overlay | `.overlay-wrap` |
| 30 | User menu | `.user-menu` |
| 20 | Sidebar | `.sidebar` |
| 19 | Shell bar | `.shell-bar` |
| 3 | Sticky table header | `.table-scroll.is-sticky thead th` |

---

## §2 Route Map

| Route | หน้า | Handler |
|---|---|---|
| `#/members` (default) | P-01 list | `render()` — route อื่น/ว่าง redirect มาที่นี่ (`getRoute()` + `navigate()`) |
| `#/members/:member_id` | P-01 + view drawer เปิดทับ (P-02) | `render()` parse `parts[1]` → `mountViewDrawer()` — **refresh-safe** (refresh แล้ว drawer กลับมาเปิดเอง) |

Listener: `window.addEventListener('hashchange', function(){ render(); })` + boot รอ DOM+Lucide (`bootIfReady()`)
Overlay ที่ไม่ผูก route: create/edit drawer, modal ทั้ง 3 (state-driven เท่านั้น — refresh แล้วหาย)

---

## §3 Layout Shell

- ERP shell: Sidebar `232px` charcoal flat (`.sidebar`) + Shell-bar `52px` ขาว sticky (`.shell-bar`) + `.content` fluid (padding 22px, ไม่มี max-width)
- Sidebar (Rule #27): `.sb-module[data-module="agm"]` "เกษตรกรรม" → features: `จัดการสมาชิกเกษตรกร` (is-active), `โควตา`/`สัญญาส่งอ้อย`/`การส่งอ้อยเข้าโรงงาน` (is-disabled — feature ถัดไปของ AGM) + module `system` → Settings (disabled) · header module = `<button onclick="toggleModule(this)">` non-navigable
- Breadcrumb: `เกษตรกรรม › จัดการสมาชิกเกษตรกร` (chevron-right icon separator)
- User chip: "สมพร วงศ์ทะเบียน / เจ้าหน้าที่ทะเบียนชาวไร่ · WKN" + dropdown (`toggleUserMenu()`)
- `body { min-width: 1180px }` desktop-only

---

## §4 Page Anatomy

### P-01 `#/members` — รายชื่อสมาชิกเกษตรกร (`render()` → `#page-content`)
```
.ph  h1 "จัดการสมาชิกเกษตรกร" + .ph-count "[N] รายการ" + sub
     .ph-actions: [Import CSV secondary → openImportModal()]
                  [ตรวจสอบที่เลือก (N) secondary, disabled เมื่อ N=0 → openVerifyModal()]
                  [สร้างสมาชิก primary → openForm('create')]   ← ขวาสุด (Rule #46)
.stats 4 การ์ด: สมาชิกทั้งหมด · รอตรวจสอบ (+meta warn "ค้างเกิน 7 วัน N รายการ" เมื่อมี) · อนุมัติแล้ว · ปฏิเสธ
.card
 ├ .filter-bar: search ซ้าย (#q-search, debounce 300ms — onSearchInput) + select สถานะ 4 ค่า + ล้างตัวกรอง ghost ขวาสุด (resetFilters)
 ├ .bulk-bar (แสดงเมื่อ selectedIds.size > 0): "เลือก N รายการ (รอตรวจสอบ)" + ตรวจสอบที่เลือก + ยกเลิกการเลือก
 ├ .table-scroll.is-sticky > .table 8 คอลัมน์:
 │   ☑(เฉพาะ pending selectable — cb.is-disabled สำหรับแถวอื่น) · Member Id (mono แดง) · ชื่อ · นามสกุล ·
 │   เบอร์โทรศัพท์ · เลขบัตรประชาชน (masked — maskCitizen) · สถานะการยืนยัน (pill) · การดำเนินการ (pencil → trash-2 เฉพาะ pending)
 │   แถว .is-clickable → openView(member_id) · checkbox/actions มี stopPropagation
 │   sortable: member_id, first_name, last_name, verify_status (sortBy)
 └ .table-footer: pagination ซ้าย · "X – Y จาก Z รายการ" ขวา
```
Empty states (`emptyStateHTML`): ไม่มีข้อมูล → "ยังไม่มีสมาชิกเกษตรกร" + ปุ่ม สร้างสมาชิก/Import CSV · filter ไม่เจอ → "ไม่พบรายการที่ค้นหา" + ล้างตัวกรอง

---

## §5 Component Inventory (states ครบตาม R4)

| Component | Anchor | States ที่มีจริง |
|---|---|---|
| ปุ่ม `.btn` (primary/secondary/ghost/danger/danger.is-solid/link/sm) | CSS §BUTTONS | default / hover / disabled (`.55 opacity + pointer-events:none`) / submitting (disabled + `loader-2 .spin` + label "กำลัง…") — focus ring ไม่มี (—) |
| Checkbox `.cb` | `toggleSelect/toggleSelectAll` | unchecked / is-checked / is-partial (select-all บางส่วน) / is-disabled (แถวไม่ใช่ pending — title "เลือกได้เฉพาะรายการรอตรวจสอบ") |
| Status pill | `statusPill()` | `pill-warning` รอตรวจสอบ / `pill-success` อนุมัติแล้ว / `pill-danger` ปฏิเสธ — คำตายตัว `statusLabel()` |
| Quota pill | `quotaPill()` | `pill-outline` ไม่มีโควตา (Phase-1 คงค่า no_quota ทุก record — authoritative) · `pill-info` มีโควตา = component รองรับไว้สำหรับ Phase-2/Quota module (read-only จาก module Quota) |
| Search-select | `searchSelectHTML()/initSearchSelect()` (`#ss-{key}`) | ปิด (caret) / เลือกแล้ว (ปุ่ม X clear) / เปิด+พิมพ์กรอง (`<mark>` highlight, ↑↓ Enter Esc) / empty ("เลือกจังหวัดก่อน"/"เลือกอำเภอก่อน"/"ไม่พบรายการ") / disabled (`.is-disabled` — อำเภอ/ตำบลก่อนเลือกลำดับบน) — list = overlay z-70 ไม่ดันเนื้อหา |
| Field `.field` | `validateField()` on-blur | default / is-invalid (border แดง + `.field-error` visible — จองพื้นที่ min-height 15px ไม่กระตุก) / readonly (postal_code — bg เทา + help "ระบบกำหนดให้อัตโนมัติจากตำบล") |
| Table sticky header | `.table-scroll.is-sticky thead th` | bg ทึบที่ th + z-3 (scroll แล้ว row ไม่ทะลุ) |
| Stat card `.stat` | render() stats | ปกติ / meta warn (`is-warn` — Pending ค้าง > 7 วัน) |
| Timeline `.timeline` | renderViewDrawer tab history | dot ปกติ / is-success (approve) / is-danger (reject, delete) / is-warning (resubmit) + `.tl-note` กล่องหมายเหตุ |
| Toast `.toast` | `showToast(msg, variant, ms)` | success/info/warning/error — ขวาล่าง, auto-dismiss default 3200ms (bulk/import 4500ms), แสดงหลังปิด overlay เท่านั้น |

---

## §6 Overlay Registry

| Overlay | ขนาด | Mount | Dismiss rules | z |
|---|---|---|---|---|
| View drawer (P-02) | `.drawer-panel` 920px | `mountViewDrawer()` → `#view-content` · ผูก route `#/members/:id` | backdrop click / X / Esc / ปุ่ม `ปิด` → `closeView()` + navigate กลับ `#/members` | 50 |
| Create/Edit drawer (OV-01/02) | `.drawer-panel` 920px | `openForm(mode, id)` → `#form-content` | backdrop / X / Esc / `ยกเลิก` → `closeForm()` — **block ระหว่าง submitting** (`state.form.submitting`) | 50 |
| Verify modal (OV-04) | `.modal` 440px | `openVerifyModal(singleId?)` — ไม่ส่ง id = bulk จาก selectedIds | backdrop / X / Esc / `ยกเลิก` — **block ระหว่าง busy** | 60 |
| Delete modal (OV-05) | `.modal` 440px danger | `openDeleteModal(id)` — **guard: ไม่ใช่ pending → toast error ไม่เปิด modal** | backdrop / X / Esc / `ยกเลิก` — block ระหว่าง busy | 60 |
| CSV Import modal (OV-03) | `.modal.is-lg` 680px | `openImportModal()` — 3 phases: pick → preview → done | backdrop / X / Esc / `ยกเลิก` — block ระหว่าง busy (กำลังนำเข้า) | 60 |

Drawer animation: `.drawer-enter` translateX(100%) → `.drawer-active` translateX(0) 250ms ease-out · unmount หลัง 200ms (`closePanel`)
Modal animation: backdrop opacity 200ms + `.modal` scale 0.96→1
เปิด form ทับ view: `openForm` ปิด view state + navigate กลับ `#/members` ก่อน mount (ไม่ stack 2 drawers)

---

## §7 Interaction Spec

- **Esc chain (ตามลำดับใน handler จริง):** `state.modal.open → closeModal()` → `state.form → closeForm()` → `state.view → closeView()` · Esc ใน search-select เปิดอยู่ = ปิด list + `stopPropagation` (ไม่หลุดไปปิด drawer)
- **Click-outside:** search-select ปิดผ่าน document click listener (เช็ค `wrap.contains(e.target)`) · user-menu เช่นกัน
- **Search debounce:** `onSearchInput` — `setTimeout 300ms` reset ทุก keystroke (US-03/AC-12)
- **Render preservation (Rule #29):** `preserveRenderState()/restoreRenderState()` — เก็บ pageScroll + focus (by id → fallback placeholder) + cursor selection · drawer/modal ไม่โดน rebuild โดย `render()` (แยก render function ต่อ overlay) จึงไม่เด้ง
- **Row click = view (Rule #41):** `<tr class="is-clickable" onclick="openView(...)">` — ไม่มี eye icon · checkbox + actions cell `event.stopPropagation()`
- **Double-submit guard (Rule #44):** ทุก submit (`submitForm/submitVerify/confirmDelete/applyImport`) — flag `submitting/busy` + ปุ่ม disabled + `loader-2` + label "กำลังบันทึก…/กำลังดำเนินการ…/กำลังลบ…/กำลังนำเข้า…"
- **Cascade reset (VR-11):** เปลี่ยนจังหวัด → เคลียร์ อำเภอ+ตำบล+ไปรษณีย์ (`initAddressSelects` onSelect) · เปลี่ยนอำเภอ → เคลียร์ ตำบล+ไปรษณีย์ (`refreshAddressSelects`)
- **Layout stability (Rule #35):** `html { scrollbar-gutter: stable }` + ss-list/user-menu = absolute overlay + `.table-scroll` overflow-x

---

## §8 State-Driven UI Matrix

`verify_status` enum → ทุกจุดที่ UI เปลี่ยนตาม state:

| State | Pill | Checkbox list | ปุ่มลบ (list) | View header actions | Edit พิเศษ | Delete |
|---|---|---|---|---|---|---|
| `pending_approval` | รอตรวจสอบ (เหลือง) | selectable | มี | แก้ไข + **ตรวจสอบ** (primary) + **ลบ** (danger) + X | — | ได้ |
| `approved` | อนุมัติแล้ว (เขียว) | disabled | ไม่มี | แก้ไข + X | sub บอก "แก้ไขได้ทุกช่อง สถานะคงเดิม (บันทึกลงประวัติ)" — แก้ citizen_id → history note Anomaly | guard → toast "ลบได้เฉพาะรายการที่ยังไม่ได้ตรวจสอบ" |
| `rejected` | ปฏิเสธ (แดง) | disabled | ไม่มี | แก้ไข + X · detail มี `.dv-note` เหตุผลที่ปฏิเสธ | banner info "บันทึกแล้วรายการจะกลับเข้าคิวรอตรวจสอบ" → save = **กลับ pending อัตโนมัติ** (LOCK-06, `submitForm` resubmitted branch) + note เดิมย้ายเข้า history | guard เดียวกัน |
| `is_deleted` | — (หายจาก list ทุก filter) | — | — | route ตรง id ที่ถูกลบ → navigate กลับ | — | — |

History event → timeline dot: create/edit (ปกติ) · resubmit (warning) · approve (success) · reject / delete (danger)

---

## §9 Microcopy (verbatim 100% — dev/QA copy ตรงนี้)

**ปุ่ม:** `สร้างสมาชิก` · `Import CSV` · `ตรวจสอบที่เลือก (N)` · `ยืนยันสร้าง` · `บันทึกการแก้ไข` · `ยกเลิก` · `ปิด` · `แก้ไข` · `ตรวจสอบ` · `ลบ` · `ล้างตัวกรอง` · `เลือกไฟล์` · `ดาวน์โหลดแม่แบบ` · `ดาวน์โหลดรายงาน` · `ยืนยันนำเข้า (N แถว)` · `ยืนยัน` · `ยกเลิกการเลือก`
**Submitting:** `กำลังบันทึก…` · `กำลังดำเนินการ…` · `กำลังลบ…` · `กำลังนำเข้า…`

**Toast (ทุก call ของ showToast):**
| ข้อความ | Variant | จุดเกิด |
|---|---|---|
| `สร้างสมาชิกสำเร็จ — FM-NNNNNN` | success | submitForm create |
| `บันทึกการแก้ไขแล้ว` | success | submitForm edit (ไม่ resubmit) |
| `บันทึกแล้ว — รายการกลับเข้าคิวรอตรวจสอบ` | success | submitForm edit rejected (LOCK-06) |
| `ยืนยันสมาชิกเรียบร้อย` / `ปฏิเสธสมาชิกเรียบร้อย` | success | submitVerify เดี่ยว |
| `ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ X ล้มเหลว Y (FM-… ถูกตรวจสอบไปแล้ว)` | success/warning | submitVerify bulk (EC-12) |
| `ลบสมาชิกแล้ว` | success | confirmDelete |
| `ลบได้เฉพาะรายการที่ยังไม่ได้ตรวจสอบ` | error | openDeleteModal guard (EC-02) |
| `นำเข้าสมาชิก X รายการสำเร็จ — ข้าม Y แถว` | success/warning | applyImport (LOCK-04) |
| `กรุณาเลือกไฟล์ CSV เท่านั้น` / `ขนาดไฟล์ต้องไม่เกิน 5MB` | error | onCsvFilePicked guard (VR-08) |
| `ไฟล์ถูกปฏิเสธทั้งไฟล์ — header ไม่ตรงแม่แบบ` | error | EC-10 |
| `ไฟล์ว่าง ไม่มีข้อมูล` | error | CSV ว่าง |
| `กรุณากรอกข้อมูลให้ครบถ้วน` | warning | submitForm validation fail |
| `กรุณาเลือกผลการตรวจสอบ` / `จำเป็นต้องระบุเหตุผลเมื่อปฏิเสธ` | warning | submitVerify (VR-06/07) |

**Validation รายช่อง (`.field-error`):** `กรุณากรอกชื่อ/นามสกุล/ที่อยู่/เลขบัตรประชาชน/เบอร์โทรศัพท์` · `เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก` · `เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-12 หลัก` · `รูปแบบอีเมลไม่ถูกต้อง` · `กรุณาเลือกจังหวัด/อำเภอ/ตำบล` · `เลขบัตรประชาชนนี้มีในระบบแล้ว (FM-NNNNNN)` · `คอลัมน์ไฟล์ไม่ตรงแม่แบบ: [รายการ]`
**CSV row errors:** `เลขบัตรประชาชนซ้ำภายในไฟล์ (แถว N)` · `เลขบัตรประชาชนซ้ำ — มีในระบบแล้ว (FM-NNNNNN)` · `ไม่พบตำบลใน[อำเภอ]` · `ไม่พบอำเภอในจังหวัด[จังหวัด]` · `ไม่พบจังหวัดในระบบ` · `รหัสไปรษณีย์ไม่ตรงกับตำบล`
**Placeholder:** `ค้นหาชื่อ นามสกุล เบอร์โทร เลขบัตร Member Id` · `ชื่อ` `นามสกุล` `1234567890123` `0812345678` `example@email.com` `บ้านเลขที่ หมู่ ซอย ถนน` · `เลือกจังหวัด/อำเภอ/ตำบล` · verify note: `กรุณาระบุเหตุผลในการปฏิเสธ` / `หมายเหตุเพิ่มเติม (ไม่บังคับ)`
**Modal delete:** title `ลบสมาชิก?` · body `ต้องการลบ "[ชื่อ] (FM-NNNNNN)" ใช่หรือไม่ การลบไม่สามารถย้อนกลับได้` · warn `รายการจะถูกซ่อนจากระบบ (soft delete) และบันทึกลงประวัติการดำเนินการ`
**Empty:** `ยังไม่มีสมาชิกเกษตรกร` + `เริ่มต้นด้วยการสร้างสมาชิกแรกของคุณ หรือนำเข้าจากไฟล์ CSV` · `ไม่พบรายการที่ค้นหา` + `ลองปรับคำค้นหรือล้างตัวกรอง`
**Masking:** list = `maskCitizen` → `3-XXXX-XXXX-XX-1` (หลักแรก + หลักสุดท้าย) · detail = `fmtCitizenFull` → `3-7101-00234-56-1`

---

## §10 Data Binding & BACKEND anchors

`// BACKEND:` comments ในไฟล์ = จุด plug API (map ตรงกับ FRD 02_API):
| Anchor | แทนด้วย |
|---|---|
| `ADDRESS` const | M-01 address hierarchy lookup API (master กลาง) |
| `state.records` seed | API-01 GET /api/v1/farmer-members (list ส่ง citizen_id_masked + selectable) |
| `openForm('edit')` data clone | API-03 GET /:id (legacy FN-AT-AGM-102) |
| `submitForm()` setTimeout | API-02 POST (FN-SEQ-AGM-110) / API-04 PUT (FN-SEQ-AGM-111) + `Idempotency-Key {FN}:{id}:{user}` + `expected_updated_at` — resubmitted branch = server ทำใน transaction เดียว |
| `submitVerify()` loop | API-05 verify เดี่ยว / API-06 bulk-verify per-record (partial result) — legacy FN-AT-AGM-103 |
| `confirmDelete()` | API-07 DELETE soft (FN-AT-AGM-105) |
| `onCsvFilePicked/validateCsvRows/applyImport` | API-08 POST /import (FN-SEQ-AGM-110 batch) — client-side validate ใน mock = server-side จริงตาม FRD FN-08 |
| `downloadTemplate()` | API-09 GET /import/template (UTF-8 BOM) |
| `m.history` | API-10 GET /:id/history |

Mock: 16 members (7 pending — 4 ค้าง >7วัน · 7 approved · 2 rejected) — quota_status คงค่า `no_quota` ทุก record (authoritative; has_quota seed ถอดออกแล้ว 2026-07-22 — has_quota = Phase-2) + M-01 3 จังหวัด (กาญจนบุรี/ราชบุรี/สุพรรณบุรี) 2-3 อำเภอ × 2-3 ตำบล

---

## §11 Traceability + Drift Log

### Traceability (Brief ↔ FRD ↔ HTML)
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI P-01 (Pattern A) | `render()` → `#page-content` | §4 |
| 01_UI P-02 (Pattern C) | `renderViewDrawer()` tabs ข้อมูล/ประวัติ | §6 |
| 01_UI OV-01/02 (Pattern B) | `openForm/renderFormDrawer/submitForm` | §6 |
| 01_UI OV-03 (Rule #32) | `openImportModal` 3-phase | §6 |
| 01_UI OV-04/05 (Pattern D) | `openVerifyModal` / `openDeleteModal` | §6 |
| 02_API API-01..10 | §10 BACKEND anchors | §10 |
| 05_RULES §5.2 state machine (LOCK-02/06/07) | `submitForm` resubmit branch · `submitVerify` pending guard · `openDeleteModal` guard | §8 |
| 05_RULES §5.4 VR-01..11 | validators `vCitizen/vPhone/vEmail/vRequired` + cascade + `validateCsvRows` | §9 |
| 05_RULES EC-01..16 | ดูหมายเหตุ EC ใน comment ของ function ที่เกี่ยว | §8/§9 |
| 06_TESTS §6.10 microcopy | §9 verbatim ทั้งชุด | §9 |

### ⚠️ Drift Log
| # | รายการ | ทาง | ข้อเสนอ |
|---|---|---|---|
| D-01 | **Stats row 4 การ์ด (widget BRD §18.2)** — FRD 01_UI ไม่ได้ระบุใน P-01 | HTML-only (เสริม) | เก็บไว้ — ตรง BRD §18.2 dashboard widgets; sync เข้า FRD 01_UI ผ่าน html-to-frd-sync |
| D-02 | **Rule #32.5 Replace/Merge modes ไม่ implement** — import เป็น additive-only | FRD-only (Iron Rule ถูก override) | ตั้งใจ: Replace ขัด LOCK-04 + BR-AGM-10 (duplicate = row error, ทะเบียนมี verify state) — log เป็น Iron Rule deviation |
| D-03 | **Optimistic lock CONFLICT (VR-10/AC-25)** ไม่มีเส้นทาง demo ใน mock (single-user prototype) | FRD-only | พฤติกรรม 409 อยู่ที่ server จริง (API-04/05/06/07) — testcase ระบุเป็น API-level case; UI copy พร้อมแล้ว ("ข้อมูลถูกแก้ไขโดยผู้อื่น…" ใน FRD §5.6) |
| D-04 | **Role switching R-01/R-02** — prototype แสดงทุกปุ่มใน user เดียว | HTML simplification | ENC permission บังคับที่ระบบจริง (05_RULES §5.3) — prototype log ไว้ ไม่ใช่ spec ว่าทุกคนเห็นทุกปุ่ม |

> **Recheck reconciliation (2026-07-22 — align กับ authoritative spec + prototype ที่ fix แล้ว):** CSV header คอลัมน์ที่ 6 = `address` (map DB `address_line`) · email = **required** (LOCK-08 superseded) · quota_status คงค่า `no_quota` ทุก record (has_quota = Phase-2). LOCK-06/07 (re-submit ผ่าน edit) เป็น additive เกิน authoritative — คงไว้ รอ owner sign-off.

---

## §12 Diff จากเวอร์ชันก่อน

เทียบ legacy prototype (farmer-management.zip — Next.js/v0):
- คงไว้ 100%: ทุก capability (LOCK-01) — CRUD, verify เดี่ยว/กลุ่ม, CSV partial success, search 5 field + debounce 300ms, badge 3 สี, soft delete guard, microcopy หลัก ("ลบได้เฉพาะรายการที่ยังไม่ได้ยืนยัน" → ปรับเป็น "…ตรวจสอบ" ตาม pill vocabulary กลาง)
- เปลี่ยน: detail full-page (`/member/:id`) → view drawer tabbed (Layout Decision Log 01_UI §1.0) · CI shadcn → CUBE Warm Light · modal verify มี list รายชื่อ bulk · เพิ่ม: re-submit banner + auto pending (LOCK-06) · citizen_id masked บน list (S02-04) · email required (authoritative — LOCK-08 optional superseded 2026-07-22) · stats row · CSV header (`address`) / duplicate-in-file validation (EC-09..11 ระดับ client)
- Legacy testid (`q.search`, `actionbar.btn-create`, …) ไม่ถูก copy — anchor ใหม่ใช้ selector/function ตาม §5-6 (AI testcase ใช้ข้อความบนจอเป็น anchor แทน)

---

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)

1. เพิ่ม filter "ค้างเกิน 7 วัน" กดจาก stat card ได้ (ตอนนี้การ์ดเป็น display อย่างเดียว)
2. Bulk verify ควรมี progress ต่อรายการเมื่อ > 50 รายการ (ตอนนี้ mock รวดเดียว)
3. Tab ประวัติ: เพิ่ม diff Before/After ต่อ event (ข้อมูลมีใน FRD 04_DB history.diff แล้ว — UI ยังแสดงแค่ note)
