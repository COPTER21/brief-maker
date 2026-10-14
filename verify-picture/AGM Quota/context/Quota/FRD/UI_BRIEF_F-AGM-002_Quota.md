# UI BRIEF — F-AGM-002 Quota Management (AS-BUILT)

## §0 Document Control + Pairing

| Field | Value |
|---|---|
| Source HTML | `quota-management.html` (v1.0, 2026-07-20 — html-generator-v6, audit FAIL=0 · WARN=2 inherited) |
| FRD Pack | `FRD_F-AGM-002_Pack/` (7 ไฟล์, STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-002 APPROVED (LOCK-01..11) |
| Cross-module | F-AGM-001 Farmer Member (อ่าน member + เขียน `quota_status` กลับ ผ่าน ENG-EXT-03) |
| Drift status | ดู §11 Drift Log — 4 รายการ (log แล้ว ไม่มีเงียบหาย) |
| ผู้อ่านเป้าหมาย | FE/BE dev สร้างระบบจริงจาก HTML + FRD Pack + Brief นี้ |
| กติกา | ทุก claim ใน Brief นี้ชี้ anchor ได้ (selector / function / ข้อความ verbatim) — HTML = source of truth |

---

## §1 Design Tokens AS-BUILT

### CSS Variables (`:root` — CUBE Warm Light — เหมือน F-AGM-001 100%)
| Token | ค่า | ใช้ทำ |
|---|---|---|
| `--c-navy` / `--c-navy-2` / `--c-ink` | `#111111` | text หลัก, sidebar, toast bg |
| `--c-primary` / `--c-primary-hover` | `#FF3B30` / `#E62E24` | action หลัก, active sidebar, focus ring |
| `--c-teal` / `--c-teal-light` | `#FF9A1F` / `#FFB763` | **connection accent — cross-module link "ดูสมาชิก" + member card** |
| `--c-mute` / `-2` / `-3` | `#54565C` / `#73757B` / `#9A9CA2` | secondary text ไล่ระดับ |
| `--c-line` / `-2` / `-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | borders ไล่ระดับ |
| `--c-bg-off` | `#FAF8F5` | Ivory ground |
| `--c-success` / `--c-warning` / `--c-danger` | `#1F9D55` / `#E8870F` / `#E62E24` | semantic (pill สถานะ) |
| `--sidebar-w` / `--shell-h` | `232px` / `52px` | shell |
| `--fs-*` | h1 22 / h2 17 / h3 15 / body 14 / sub 13 / meta 12 / cap 11 / kpi 28 | fixed type scale |
| `--sp-*` / `--r-*` | 4/8/12/20/28 · 4/6/8/12/999 | fixed spacing / radius |

Fonts: `'Satoshi', 'Noto Sans Thai', system-ui` · Icons: Lucide 0.469.0 (multi-CDN loader ท้าย body, fallback no-op หลัง 5s)
Thai optical centering: `.btn { padding: 2px 14px 0 }` · `.pill { 4px 10px 3px }` · `td { 13px 14px 11px }` — ห้ามแก้เป็น line-height:1 (Rule #36)

### Z-Index Map (สูง → ต่ำ)
| z | Layer | Selector |
|---|---|---|
| 80 | Toast | `.toast` |
| 70 | Search-select list / member-search list | `.ss-list` / `.ms-list` |
| 60 | Modal backdrop (verify / delete / import) | `.modal-backdrop` |
| 50 | Drawer overlay (view / create-edit) | `.overlay-wrap` |
| 30 | User menu | `.user-menu` |
| 20 / 19 | Sidebar / Shell bar | `.sidebar` / `.shell-bar` |
| 3 | Sticky table header | `.table-scroll.is-sticky thead th` |

---

## §2 Route Map

| Route | หน้า | Handler |
|---|---|---|
| `#/quotas` (default) | P-01 list | `render()` — route อื่น/ว่าง redirect มาที่นี่ (`getRoute()` บรรทัด 712 + `navigate()` 713) |
| `#/quotas/:quota_number` | P-01 + view drawer เปิดทับ (P-02) | `render()` parse `parts[1]` → `findQuota()` → `mountViewDrawer()` (บรรทัด 807) — **refresh-safe** (refresh แล้ว drawer กลับมาเปิดเอง; ถ้า id ถูกลบ → `navigate('quotas')`) |

`getRoute()`: `#`/`#/`/ว่าง → `'quotas'` · `openView(qn)` = `navigate('quotas/'+qn)` · `closeView()` navigate กลับ `quotas`
Listener: `hashchange` → `render()` + boot รอ DOM+Lucide (`bootIfReady()`)
Overlay ที่ไม่ผูก route: create/edit drawer + modal ทั้ง 3 (state-driven — refresh แล้วหาย)

---

## §3 Layout Shell

- ERP shell: Sidebar `232px` charcoal flat + Shell-bar `52px` ขาว sticky + `.content` fluid (padding 22px, ไม่มี max-width — Rule #30)
- Sidebar (Rule #27): module `เกษตรกรรม` → `จัดการสมาชิกเกษตรกร` (is-disabled — feature อื่น), **`จัดการโควตา` (is-active — feature นี้)**, `สัญญาส่งอ้อย`/`การส่งอ้อยเข้าโรงงาน` (is-disabled) + module `system` → Settings (disabled)
- Breadcrumb: `เกษตรกรรม › จัดการโควตา`
- User chip: "สมพร วงศ์ทะเบียน / เจ้าหน้าที่ทะเบียนโควตา · WKN" + dropdown (`toggleUserMenu`)
- `body { min-width: 1180px }` desktop-only

---

## §4 Page Anatomy

### P-01 `#/quotas` — จัดการโควตา (`render()` → `#page-content`)
```
.ph  h1 "จัดการโควตา" + .ph-count "[N] รายการ" + sub "ทะเบียนโควตาชาวไร่ · ผูกสมาชิกหรือไม่ผูกก็ได้ · ตรวจสอบยืนยัน และนำเข้าจาก CSV"
     .ph-actions: [Import CSV secondary → openImportModal()]
                  [ตรวจสอบที่เลือก (N) secondary, disabled เมื่อ N=0 → openVerifyModal()]
                  [สร้างโควตา primary → openForm('create')]   ← ขวาสุด (Rule #46)
.stats 4 การ์ด: โควตาทั้งหมด (sub "ไม่รวมที่ถูกลบ") · รออนุมัติ (+meta warn "ค้างเกิน 7 วัน N รายการ") · อนุมัติ (sub "พร้อมทำสัญญา") · ไม่อนุมัติ (sub "คืนสถานะโควตาสมาชิกแล้ว")
.card
 ├ .filter-bar: search ซ้าย (debounce 300ms — onSearchInput, กรอง 6 field) + select สถานะ (ทุกสถานะ/รออนุมัติ/อนุมัติ/ไม่อนุมัติ) + ล้างตัวกรอง ghost ขวาสุด (resetFilters)
 ├ .bulk-bar (แสดงเมื่อ selectedIds.size > 0): "เลือก N รายการ (รออนุมัติ)" + ตรวจสอบที่เลือก + ยกเลิกการเลือก
 ├ .table-scroll.is-sticky > .table 8 คอลัมน์:
 │   ☑(เฉพาะ unverified selectable · แถวอื่น cb.is-disabled) · เลขโควต้า (mono แดง, link) · ชื่อ · นามสกุล ·
 │   เบอร์โทรศัพท์ · เลขบัตรประชาชน (masked — maskCitizen) · สถานะ (pill) · การดำเนินการ (pencil → trash-2 เฉพาะ unverified)
 │   แถว .is-clickable → openView(quota_number) · checkbox/actions มี stopPropagation
 │   sortable: quota_number, first_name, last_name, verify_status (sortBy)
 └ .table-footer: pagination ซ้าย · "X – Y จาก Z รายการ" ขวา
```
Empty states (`emptyStateHTML`): ไม่มีข้อมูล → "ยังไม่มีโควตา" + ปุ่ม สร้างโควตา/Import CSV · filter ไม่เจอ → "ไม่พบรายการที่ค้นหา" + ล้างตัวกรอง

---

## §5 Component Inventory (states ครบตาม R4)

| Component | Anchor | States ที่มีจริง |
|---|---|---|
| ปุ่ม `.btn` (primary/secondary/ghost/danger/link/sm) | CSS §BUTTONS | default / hover / disabled (`.55 opacity + pointer-events:none`) / submitting (disabled + `loader-2 .spin` + label "กำลัง…") |
| Checkbox `.cb` | `toggleSelect/toggleSelectAll` | unchecked / is-checked / is-partial / is-disabled (แถว ≠ unverified — title "เลือกได้เฉพาะรายการรออนุมัติ") |
| Status pill | `statusPill()` | `pill-warning` รออนุมัติ / `pill-success` อนุมัติ / `pill-danger` ไม่อนุมัติ — คำตายตัว |
| **Member-search select** ⭐ | `initMemberSearch()/selectMember()` (create drawer) | ปิด / พิมพ์กรอง (dropdown สมาชิก Approved: ชื่อ + FM-id + เบอร์) / **แถวสมาชิกที่ has_quota แสดง "มีโควตาแล้ว" + block เลือก (1:0..1 — LOCK-05)** / เลือกแล้ว → member card + prefill + ปุ่มถอด / empty "ไม่พบสมาชิก" |
| Search-select (address) | `searchSelectHTML()/initSearchSelect()` `#ss-{key}` ×2 ชุด (current + id_card) | ปิด / เลือกแล้ว (X clear) / เปิด+พิมพ์ (`<mark>` highlight, ↑↓ Enter Esc) / empty ("เลือกจังหวัดก่อน"/"ไม่พบรายการ") / disabled (ลำดับล่างก่อนเลือกบน) — list overlay z-70 |
| Field `.field` | on-blur validate | default / is-invalid (border แดง + `.field-error` — จองพื้นที่ min-height) / readonly (postal ×2 — "ระบบกำหนดให้อัตโนมัติจากตำบล") |
| Stat card `.stat` | render() stats | ปกติ / meta warn (`is-warn` — unverified ค้าง > 7 วัน) |
| Member card ⭐ | `renderViewDrawer` / create prefill | "ผูกกับสมาชิก [FM-id] · [ชื่อ] · [เบอร์]" (พื้น teal อ่อน) + ปุ่ม `ดูสมาชิก` (external-link, teal) — เฉพาะ linked · No-Member ไม่แสดง |
| Timeline `.timeline` | renderViewDrawer tab ประวัติ | dot ปกติ (create/edit) / is-success (approve) / is-danger (reject, delete) / **quota_status_written (cross-module event)** + `.tl-note` |
| Toast `.toast` | `showToast(msg, variant, ms)` | success/info/warning/error — ขวาล่าง, auto-dismiss 3200ms (bulk/import/write-back 4000–4800ms) |

---

## §6 Overlay Registry

| Overlay | ขนาด | Mount | Dismiss rules | z |
|---|---|---|---|---|
| View drawer (P-02) | `.drawer-panel` 920px | `mountViewDrawer()` → 3 tabs (ข้อมูลทั่วไป/ไฟล์ที่อัปโหลด/ประวัติ) · ผูก route `#/quotas/:qn` | backdrop / X / Esc / `ปิด` → `closeView()` + navigate กลับ | 50 |
| Create/Edit drawer (OV-01/02) | `.drawer-panel` 920px | `openForm(mode, id)` → member-search sub-flow + 6 form sections | backdrop / X / Esc / `ยกเลิก` → `closeForm()` — **block ระหว่าง submitting** | 50 |
| Verify modal (OV-03) | `.modal` 440px | `openVerifyModal(singleId?)` — ไม่ส่ง id = bulk · radio อนุมัติ/ปฏิเสธ · **reject + linked → warning banner คืนสถานะ** | backdrop / X / Esc / `ยกเลิก` — block busy | 60 |
| Delete modal (OV-04) | `.modal` 440px danger | `openDeleteModal(id)` — **guard: ≠ unverified → toast error ไม่เปิด · linked → warning คืนสถานะ** | backdrop / X / Esc / `ยกเลิก` — block busy | 60 |
| CSV Import modal (OV-05) | `.modal.is-lg` 680px | `openImportModal()` — **No-Member เท่านั้น** · 3 phases: pick → preview → done | backdrop / X / Esc / `ยกเลิก` — block busy | 60 |

Drawer animation: `.drawer-enter` translateX(100%) → `.drawer-active` translateX(0) 250ms · unmount หลัง 200ms (`closePanel`)
เปิด form ทับ view: `openForm` ปิด view state + navigate กลับ `#/quotas` ก่อน mount (ไม่ stack 2 drawers)

---

## §7 Interaction Spec

- **Member-search sub-flow (create) ⭐:** พิมพ์ → dropdown สมาชิก Approved (`initMemberSearch`) · ค้นด้วย ชื่อ/นามสกุล/เบอร์/เลขบัตร/**email** · เลือก (`selectMember`) → ถ้า `has_quota` → `showToast('สมาชิกนี้มีโควต้าอยู่แล้ว','warning')` + block (1:0..1) · ถ้าผ่าน → prefill ชื่อ/เลขบัตร/เบอร์/ที่อยู่ + member card + set `linkedMemberId` · ข้ามได้ = No-Member (ไม่ผูก) — **แยก 2 create modes ตอน submit** · **0 match → ข้อความมาตรฐานสีแดง `ไม่พบข้อมูลสมาชิกที่ตรงกับคำค้นหา` (AS-BUILT target — legacy `create-slide-in.tsx:110` มี)** · timeout/DEPENDENCY → banner + Retry (ไม่ prefill / Save disabled — TC-322)
- **Verify modal a11y (AS-BUILT target — TC-316):** focus-trap + focus แรกไป radio ผล · `aria-modal="true"` + `aria-labelledby`(title) · `aria-live` ประกาศ success/fail · reject = danger-variant อ่านคำเตือนคืนสถานะออกเสียง
- **Esc chain:** `state.modal → closeModal()` → `state.form → closeForm()` → `state.view → closeView()` · Esc ใน search-select เปิดอยู่ = ปิด list + stopPropagation
- **Click-outside:** search-select + member-search + user-menu ปิดผ่าน document click (เช็ค `wrap.contains`)
- **Search debounce:** `onSearchInput` — setTimeout 300ms reset ทุก keystroke (กรอง 6 field: เลขโควตา/ชื่อ/นามสกุล/เบอร์/เลขบัตร/อีเมล)
- **Render preservation (Rule #29):** `preserveState()/restoreState()` — pageScroll + focus + cursor · overlay ไม่โดน rebuild โดย `render()`
- **Row click = view (Rule #41):** `<tr class="is-clickable" onclick="openView(...)">` — ไม่มี eye icon · checkbox + actions `stopPropagation`
- **Double-submit guard (Rule #44):** `submitForm/submitVerify/confirmDelete/applyImport` — flag + disabled + `loader-2` + "กำลังบันทึก…/กำลังดำเนินการ…/กำลังลบ…/กำลังนำเข้า…"
- **Cascade reset (VR-10) ×2 ชุด:** เปลี่ยนจังหวัด → เคลียร์ อำเภอ+ตำบล+ไปรษณีย์ (แต่ละที่อยู่แยกกัน — current / id_card ไม่กระทบกัน) · `initAddr/refreshAddr`
- **quota_number uniqueness:** `checkQuotaNumber()` on-blur → "เลขโควต้านี้ถูกใช้แล้ว" (VR-05, exclude self ตอน edit)

---

## §8 State-Driven UI Matrix

`verify_status` enum → ทุกจุดที่ UI เปลี่ยน:

| State | Pill | Checkbox list | ปุ่มลบ (list) | View header actions | Cross-module ตอน action |
|---|---|---|---|---|---|
| `unverified` | รออนุมัติ (เหลือง) | selectable | มี | แก้ไข + **ตรวจสอบ** + **ลบ** + X | ลบ/reject (ถ้า linked) → **member.quota_status → no_quota** |
| `verified` | อนุมัติ (เขียว) | disabled | ไม่มี | แก้ไข + X (ตรวจสอบ/ลบ ซ่อน) | — (create ตอนแรกเขียน has_quota แล้ว) |
| `rejected` | ไม่อนุมัติ (แดง) | disabled | ไม่มี | แก้ไข + X · detail มีเหตุผลปฏิเสธ (ถ้ามี — note optional LOCK-09) | write-back no_quota เกิดตอน reject แล้ว · edit ไม่ auto re-submit (OQ-Q3) |
| `is_deleted` | — (หายจาก list) | — | — | route ตรง id ที่ถูกลบ → navigate กลับ | write-back no_quota เกิดตอนลบแล้ว |

**Create modes:** From-Member (linked) → submit เขียน `member.quota_status → has_quota` (XT-03) · No-Member → ไม่เขียน quota_status
**Member write-back (AS-BUILT target — G1):** create/reject/delete → เขียน member.quota_status idempotent เป็น **step แยกหลัง mutation commit** · fail → **ไม่ rollback** + `member_update_status=scheduled_retry` + non-blocking banner "กำลังอัปเดตสถานะสมาชิก (จะ retry อัตโนมัติ)" (prototype mock เขียนทันที — ระบบจริง async idempotent retry FN-12/FN-AT-AGQ-127)
History event → timeline dot: create/edit (ปกติ) · approve (success) · reject/delete (danger) · **quota_status_written (cross-module — label "อัปเดตสถานะโควตาของสมาชิก" + "สถานะโควตา → มีโควตา/ไม่มีโควตา")**

---

## §9 Microcopy (verbatim 100% — dev/QA copy ตรงนี้)

**ปุ่ม:** `สร้างโควตา` · `Import CSV` · `ตรวจสอบที่เลือก (N)` · `ยืนยันสร้าง` · `บันทึกการแก้ไข` · `ยกเลิก` · `ปิด` · `แก้ไข` · `ตรวจสอบ` · `ลบ` · `ล้างตัวกรอง` · `ดูสมาชิก` · `ยืนยัน` · `ยกเลิกการเลือก`
**Submitting:** `กำลังบันทึก…` · `กำลังดำเนินการ…` · `กำลังลบ…` · `กำลังนำเข้า…`

**Toast (ทุก call จริงของ showToast):**
| ข้อความ | Variant | จุดเกิด |
|---|---|---|
| `สร้างโควตาสำเร็จ — [เลขโควต้า] (สมาชิก [FM] → มีโควตา)` / `… (No-Member)` | success | submitForm create (แยกข้อความ 2 modes) |
| `บันทึกการแก้ไขแล้ว` | success | submitForm edit |
| `[อนุมัติ/ปฏิเสธ]เรียบร้อย — คืนสถานะโควตาสมาชิกแล้ว` | success | submitVerify (คำท้ายเฉพาะ reject+linked write-back) |
| `ตรวจสอบกลุ่มเสร็จสิ้น — สำเร็จ X ล้มเหลว Y (…)` | success/warning | submitVerify bulk (EC-12) |
| `ลบโควตาแล้ว — คืนสถานะโควตาสมาชิกแล้ว` | success | confirmDelete (คำท้ายเฉพาะ linked) |
| `สมาชิกนี้มีโควต้าอยู่แล้ว` | warning | selectMember 1:0..1 block ⭐ |
| `ลบได้เฉพาะรายการที่รออนุมัติ` | error | openDeleteModal guard |
| `นำเข้าโควตา X รายการสำเร็จ — ข้าม Y แถว` | success/warning | applyImport (No-Member) |
| `กรุณาเลือกไฟล์ CSV เท่านั้น` / `ขนาดไฟล์ต้องไม่เกิน 5MB` | error | onCsvPicked guard |
| `ไฟล์ถูกปฏิเสธทั้งไฟล์ — header ไม่ตรงแม่แบบ` / `ไฟล์ว่าง` | error | parseCsv |
| `กรุณากรอกข้อมูลให้ครบถ้วน` | warning | submitForm validation |
| `กรุณาเลือกผลการตรวจสอบ` | warning | submitVerify |

**Validation รายช่อง (`.field-error`):** `กรุณากรอกเลขโควต้า/ชื่อ/นามสกุล` · `เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก` · `เบอร์โทรศัพท์ต้องเป็นตัวเลข 9-12 หลัก` · `รูปแบบอีเมลไม่ถูกต้อง` · `กรุณาเลือกจังหวัด/อำเภอ/ตำบล` · `เลขโควต้านี้ถูกใช้แล้ว`
**CSV row errors:** `เลขโควต้าซ้ำภายในไฟล์ (แถว N)` · `เลขโควต้าซ้ำ — มีในระบบแล้ว` · `ไม่พบตำบล/อำเภอ/จังหวัด` · `รหัสไปรษณีย์ไม่ตรงกับตำบล`
**Member-search:** placeholder `ค้นหา ชื่อ / นามสกุล / เบอร์ / เลขบัตร / email` · help `แสดงเฉพาะสมาชิกที่อนุมัติแล้ว · เลือกแล้วระบบจะกรอกข้อมูลให้อัตโนมัติ` · แถว has_quota suffix `· มีโควตาแล้ว` · **0 match (มาตรฐาน AS-BUILT target) `ไม่พบข้อมูลสมาชิกที่ตรงกับคำค้นหา` (สีแดง)** · timeout → banner + Retry · **write-back scheduled_retry banner `กำลังอัปเดตสถานะสมาชิก (จะ retry อัตโนมัติ)`**
**Verify modal:** title `ตรวจสอบโควตา` · radio `อนุมัติ` / `ปฏิเสธ` · note `หมายเหตุ (ไม่บังคับ)` · **warning (reject+linked)** `จะคืนค่าสถานะโควตาของสมาชิก [FM] เป็น ไม่มีโควตา`
**Delete modal:** title `ลบโควตา?` · warn (linked) `จะคืนค่าสถานะโควตาของสมาชิกที่ผูกไว้กลับเป็น ไม่มีโควตา`
**Masking:** list = `maskCitizen` → `3-XXXX-XXXX-XX-1` · detail = `fmtCitizenFull` → เต็ม (ตาม permission) · bank/BAAC = `maskAcct` ตาม permission

---

## §10 Data Binding & BACKEND anchors

`// BACKEND:` comments = จุด plug API (map ตรงกับ FRD 02_API):
| Anchor | แทนด้วย |
|---|---|
| `ADDRESS` const | M-01 address hierarchy (master กลาง) |
| `MEMBERS` const + `memberQuota` map ⭐ | **F-AGM-001 Farmer API ผ่าน ENG-EXT-03** — API-13 member-search (Approved), check quota_status (1:0..1) |
| `state.records` seed | API-01 GET /quotas (list ส่ง citizen_id_masked + selectable) |
| `openForm('edit')` clone | API-04 GET /:id |
| `checkQuotaNumber()` | API-06 GET /check-number (unique) |
| `submitForm()` create | API-02 POST /from-member (FN-01 → **FN-12 write has_quota**) / API-03 POST /no-member (FN-02) + Idempotency-Key + expected_version |
| `submitForm()` edit | API-05 PUT /:id (FN-03, optimistic lock, ไม่เปลี่ยน status) |
| `submitVerify()` | API-07 verify เดี่ยว / API-08 bulk — **reject+linked → FN-12 write no_quota** |
| `confirmDelete()` | API-11 DELETE soft — **linked → FN-12 write no_quota** |
| `writeMemberQuotaStatus()` (mock) ⭐ | **FN-12 cross-module PATCH farmer_member.quota-status เป็น step แยก idempotent หลัง mutation commit (keep-quota, ไม่ rollback)** (ENG-EXT-03) — fail → `scheduled_retry` + non-blocking banner "กำลังอัปเดตสถานะสมาชิก (จะ retry อัตโนมัติ)" · mock บันทึก history event=quota_status_written + toast |
| `onCsvPicked/parseCsv/applyImport` | API-09 POST /import (No-Member, 12 cols) — client validate = server จริงตาม FN-09 |
| `q.history` | API-12 GET /:id/history |

Mock: **8 quota records** (5 unverified — 2 ค้าง >7วัน · 2 verified · 1 rejected · mix From-Member/No-Member) + **6 farmer members Approved** (FM-000001/07/08/12/14 = no_quota · FM-000002 = has_quota เพื่อ demo 1:0..1 block) + M-01 3 จังหวัด

---

## §11 Traceability + Drift Log

### Traceability (Brief ↔ FRD ↔ HTML)
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI P-01 (Pattern A) | `render()` → `#page-content` | §4 |
| 01_UI P-02 (Pattern C 3-tabs) | `renderViewDrawer()` + member card | §6/§5 |
| 01_UI OV-01/02 (Pattern B) | `openForm/renderFormDrawer` + member-search sub-flow | §6/§7 |
| 01_UI OV-03 verify (Pattern D) | `openVerifyModal/renderVerifyModal` + warning คืนสถานะ | §6 |
| 01_UI OV-05 CSV | `openImportModal` 3-phase (No-Member) | §6 |
| 02_API API-01..13 | §10 BACKEND anchors | §10 |
| 03_LOGIC FN-11/12 (cross-module) | `selectMember` (check) · `writeMemberQuotaStatus` (write) | §7/§10 |
| 04_DB 1:0..1 partial unique | `selectMember` has_quota block | §5/§8 |
| 05_RULES §5 state machine (LOCK-02/05/06) | `submitVerify` guard · `openDeleteModal` guard · optimistic version | §8 |
| 06_TESTS §6.9 XT-01..04 | write-back reject/delete/create + member-หาย skip | §8/§10 |

### ⚠️ Drift Log
| # | รายการ | ทาง | ข้อเสนอ |
|---|---|---|---|
| D-01 | **Stats row 4 การ์ด** — FRD 01_UI ไม่ระบุใน P-01 | HTML-only (เสริม) | เก็บไว้ — ตรง BRD dashboard; sync เข้า FRD ผ่าน html-to-frd-sync |
| D-02 | **Cross-module write-back จำลองใน memory** (`writeMemberQuotaStatus`) — prototype standalone ไม่มี Farmer API จริง | HTML simulation | ระบบจริง = ENG-EXT-03 PATCH เป็น step แยก idempotent หลัง mutation commit (keep-quota, **ไม่ rollback**) + async retry (OQ-F03 / FN-AT-AGQ-127) — mock แสดง history + toast เท่านั้น |
| D-03 | **Optimistic lock CONFLICT (AC-25)** ไม่มีเส้นทาง demo (single-user) | FRD-only | 409 อยู่ที่ server จริง (API-05/07/08) — UI copy พร้อม ("ข้อมูลถูกแก้ไขโดยผู้อื่น…" FRD §5.6) |
| D-04 | **Role/SoD switching (RC-05)** — prototype แสดงทุกปุ่ม user เดียว | HTML simplification | ENC permission + SoD flag บังคับที่ระบบจริง (05_RULES) — prototype log ไว้ |

---

## §12 Diff จากเวอร์ชันก่อน

เทียบ legacy prototype (quotamanagement.zip — Next.js/v0):
- คงไว้ 100% (LOCK-01): CRUD, verify เดี่ยว/กลุ่ม, CSV No-Member partial success, 2 create modes (From-Member/No-Member), 1:0..1, cross-module write-back, badge 3 สี, soft delete guard, quota_number user-entered unique
- เปลี่ยน: detail full-page (`/quota/:id`) → view drawer 3-tabbed + member card · CI shadcn → CUBE Warm Light · verify note optional (LOCK-09) · citizen_id masked list (S02-04) · email optional (LOCK-11) · เพิ่ม stats row + cross-module warning banner (reject/delete คืนสถานะ) + CSV header/duplicate validation
- Legacy testid ไม่ถูก copy — anchor ใหม่ใช้ selector/function ตาม §5-6 (AI testcase ใช้ข้อความบนจอเป็น anchor)

---

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)

1. Member card ควร deep-link ไป Farmer detail (`#/members/:id`) จริง (ตอนนี้ mock toast "จำลองเปิดหน้าสมาชิก") — เมื่อ deploy รวม 2 features
2. Cross-module write-back ควรมี inline status indicator ("กำลังคืนสถานะสมาชิก…") เมื่อ latency สูง (ตอนนี้ mock ทันที) — รองรับ retry queue (OQ-F03) ที่ backend
3. Tab ประวัติ: แสดง `linked_write` payload (member_id + quota_status) ต่อ event quota_status_written เพื่อ audit cross-module ชัดขึ้น (ข้อมูลมีใน 04_DB history.linked_write)
