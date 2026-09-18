# Pattern Q — Transaction Document Archetype (CUBE Warm Light) ⭐ v9

> **⭐ AUTHORITATIVE STANDARD (locked to `references/document-archetype/_SOURCE_so-reference.html`).**
> ทุก feature ที่ "ออกเอกสารธุรกรรม" ใน CUBE — **PR · PO · QT · SO · GRN · INV · CN · DN · RTV · RV**
> **ต้องใช้โครงนี้เป๊ะ** ทั้ง 4 surface (list / create wizard / view drawer / PDF) — ห้ามออกแบบใหม่
> ปรับได้เฉพาะ *ชื่อเอกสาร / field set ของ step 2 / domain tabs / mock / business hook*
>
> **Verbatim source of truth:**
> - `references/document-archetype/_SOURCE_so-reference.html` — ไฟล์ทำงานเต็ม (เปิด browser = เป้าหมาย 100%)
> - `references/document-archetype/doc-create-wizard.js.txt` — create drawer + 5 steps + wizardNext/Back + combo
> - `references/document-archetype/line-editor-v2.js.txt` — step 3 (ดู `patterns/B2_document-line-editor.md`)
> - `references/document-archetype/doc-view-drawer.js.txt` — view drawer + tabs + SEC/KV/SECWRAP + PDF + Sign + History
> - `references/document-archetype/doc-approval-modals.js.txt` — ส่งอนุมัติ/อนุมัติ/ไม่อนุมัติ/ยกเลิก/พัก + DOA slot picker
> - `references/document-archetype/doc-archetype.css.html` — CSS fragments ที่ต้องมีเพิ่มจาก kit

**Q ประกอบจาก A (list) + B (drawer shell) + B2 v2 (line editor) + C (view tabs) + H (A4) + I (sign) + D (modal)**
แต่ **ลำดับ/ชื่อ/ตำแหน่ง ถูกล็อกไว้ที่นี่** — pattern เดี่ยวข้างบนคือชิ้นส่วน, Q คือ "แบบประกอบ" ที่ต้องตรง

---

## 🎯 When to Use

✅ Feature มี **เลขที่เอกสาร + สถานะเอกสาร + ลายเซ็น/อนุมัติ + PDF** (= เอกสารธุรกรรม)
✅ มี line items (สินค้า/บริการ) → ใช้ B2 v2 ใน step 3
✅ เอกสารที่ไม่มี line items แต่มีอนุมัติ+PDF (เช่น ใบขอเบิก, ใบลา) → ใช้ Q โดยตัด step 3 ออก (เหลือ 4 steps)

❌ Master data (ใช้ A+B+C ปกติ) · Dashboard (J) · Runner (O) · Planner (P)

---

## 🏗️ Surface 1 — List page (Pattern A + spec เพิ่ม)

| ส่วน | ล็อก |
|---|---|
| `.ph` | h1 ชื่อเอกสาร (ไทย + EN ในวงเล็บ) · `.ph-sub` 1 บรรทัดบอก "ทำอะไร → ส่งต่อใคร" + chip นับ `N รายการ · เปิดอยู่ M` |
| `.ph-right` | `ส่งออก CSV` (secondary) → `สร้าง[เอกสาร]` (primary ขวาสุด) |
| Filter card | search (ค้นเลขที่/คู่ค้า/อ้างอิง/ผู้ทำ) · dropdown สถานะเอกสาร · dropdown แกนสถานะรอง (จัดส่ง/การจ่าย/รับของ…) · dropdown ผู้รับผิดชอบ · `รีเซ็ต` ghost |
| Table | เลขที่ (sortable, `.tbl-mono` สี primary) · วันที่ · คู่ค้า · กำหนด · อ้างอิง · **สถานะเอกสาร** (`docPill`) · แกนรอง (`axisPill`) · **ลายเซ็น** (`renderSignProgress` = `n/N` + bar 46px) · ยอดรวม (right, sortable) · ⋮ menu |
| Row click | เปิด view drawer (Rule #41) — `⋮` = `openRowMenu` (ทำสำเนา / พิมพ์ / ยกเลิก ตามสถานะ) |
| Footer | แสดงต่อหน้า (ซ้าย) · pagination (ขวา) |

Route: `#/list` · `#/view/:id` · `#/create` · `#/edit/:id` (refresh-safe)

---

## 🏗️ Surface 2 — Create/Edit Wizard (drawer `.drawer-panel.wide` 1290) — **5 steps ล็อกลำดับ**

```
renderCreateDrawer()
├─ header (18px 24px 16px · border-bottom)
│    eyebrow  [file-plus] "สร้างเอกสารใหม่" | [pencil] "แก้ไขเอกสาร"
│    h2 20px/700 "สร้าง[ชื่อเอกสาร]ใหม่" | "แก้ไข[ชื่อ] [code]"      X = .top-icon-btn 32px
│    .stepper (margin-top 18px) → renderStepperItem × 5   (Rule #47 / #47.1)
├─ body  flex:1 overflow-y:auto  padding 22px 24px
│    step === n ? renderStepN() : ''
└─ footer (14px 24px · border-top · bg off-white)
     ซ้าย: [ย้อนกลับ] secondary (step>1)
     ขวา:  [ยกเลิก] ghost → step<5: [ถัดไป] primary
                             step=5: [บันทึกแบบร่าง] secondary → [บันทึกและส่งอนุมัติ] primary (disabled ถ้า hard control)
```

| Step | ชื่อ (ล็อก) | เนื้อหา | ตัวอย่างต่อเอกสาร |
|---|---|---|---|
| 1 | **เลือกแหล่งที่มา** | 2 tile-buttons (`สร้างใหม่` / `จาก[เอกสารต้นทาง]`) → ถ้าเลือกต้นทาง แสดง card ค้นหา + list เลือก (Enter เลือกได้) | SO←QT · PO←PR · GRN←PO · INV←DN · CN←INV |
| 2 | **ข้อมูลหลัก [เอกสาร]** | `.form-grid` 2 คอลัมน์: คู่ค้า (combo `.full` + field-help เครดิต/ข้อตกลง) · วันที่ · กำหนด · ผู้รับผิดชอบ (combo) · ช่องทาง/คลัง/แผนก · เงื่อนไขชำระ (master) · อ้างอิงภายนอก · ที่อยู่ · หมายเหตุ · toggle group (ใบกำกับ/วิธีรับ) | field set เปลี่ยนตามเอกสาร — โครง grid ไม่เปลี่ยน |
| 3 | **รายการสินค้า** | **B2 v2 ทั้งชุด** (line table → [alert block] → [pricing block] → ส่วนลดท้ายบิล → สรุปยอด) | ดู B2 |
| 4 | **เอกสารแนบ** | `STEPH('paperclip', 'แนบเอกสารประกอบ (ถ้ามี)', hint)` + `.upload-zone` (ว่าง = icon 48 + ข้อความ + ปุ่ม `เลือกไฟล์` · มีไฟล์ = list card ชื่อ+ขนาด+X + `แนบไฟล์เพิ่ม`) | เหมือนกันทุกเอกสาร |
| 5 | **ตรวจสอบและยืนยัน** | `STEPH('check-circle-2', …)` → [hard-warn ถ้ามี] → card "ข้อมูล[เอกสาร]" `<dl>` grid 2 col → card แผน/เงื่อนไข (ถ้ามี) → card override reason (ถ้ามีแก้ราคา) → ตารางรายการ read-only (`linesTableView`) → เอกสารแนบ | review เท่านั้น ห้ามมี input ยกเว้นเหตุผล |

- **ทุก step header ใช้ `STEPH(icon, title, hint)`** — hint เป็น 1 บรรทัดสี mute ใต้หัว (ยกเว้น Rule #67.1: ไม่มี ⓘ)
- `wizardNext()` validate ต่อ step: step 2 `markErr(id, cond)` + toast "กรุณากรอกข้อมูลให้ครบถ้วน" · step 3 ต้องมี ≥1 บรรทัดที่มีสินค้า+qty>0+ราคา>0, ห้ามแถวว่าง, ห้ามสินค้า+หน่วยซ้ำ, hard validate ของ domain (เช่น ATP)
- stepper ที่ `done` คลิกย้อนได้ · `active` ไม่คลิก · อนาคตไม่คลิก
- Edit mode = wizard เดียวกัน เริ่ม step 2 (ข้าม source) และ prefill

---

## 🏗️ Surface 3 — View Drawer (`.drawer-panel` 920) — **tabs ล็อกลำดับ**

```
renderViewDrawer()
├─ header (18px 24px 12px · border-bottom)
│    eyebrow 11px uppercase "[ชื่อเอกสาร] (EN)"
│    row: h2.tbl-mono 20px สี primary = code · docPill(status) · [chip เพิ่ม เช่น "แก้ราคา"]
│    summary line 13px mute: คู่ค้า · ผู้รับผิดชอบ · จาก [ต้นทาง] · ยอดสุทธิ ฿… · [แกนรอง]
│    actions (ขวา) = action group ตามสถานะ + divider + icon btns:
│        draft:            [ยกเลิก] btn-link danger · [แก้ไข] secondary · [ส่งอนุมัติ] primary | ‖
│        pending_approval: [ไม่อนุมัติ] btn-link danger · [อนุมัติ] btn-success | ‖   (เฉพาะ canActStep)
│        confirmed/in_progress: [ยกเลิก]? · [พัก] secondary | ‖
│        on_hold:          [ยกเลิก] btn-link · [ปลดพัก] primary | ‖
│        เสมอ: [copy ทำสำเนา] [printer → tab pdf] [download] [X]   (.top-icon-btn)
│    .tabs (margin-top 14px):
│        รายละเอียด › [domain tabs 1-2] › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ
├─ body  flex:1 overflow-y:auto  padding 20px 24px  → renderXxxTab(s)
└─ footer 12px 24px off-white: "แก้ไขล่าสุด … · by" + 🔒 "ยืนยันแล้ว ล็อกแก้ไข" เมื่อผ่านอนุมัติ
```

| Tab | key | icon | เนื้อหา (ล็อก) |
|---|---|---|---|
| **รายละเอียด** (landing) | `detail` | file-text | banners (hard-warn / note.warn / note.danger) → `SECWRAP(SEC('info','ข้อมูลเอกสาร')…, true)` KV grid 2 col → `SEC('layers','สถานะ')` 3 col (doc pill + แกนรอง pill + `pgl` bar) → `SEC('file-text','เอกสารอ้างอิง')` → `SEC('user','คู่ค้าและผู้รับผิดชอบ')` → `SEC('info','เงื่อนไขและ…')` → ยอดรวม block → `SEC('list','รายการสินค้า (N)')` + `linesTableView` → **`SEC('paperclip','เอกสารแนบ (N ไฟล์ · Document Center)')`** list card → `SEC('user','ข้อมูลระบบ')` |
| domain tabs | เช่น `stock` / `fin` | package / wallet | 0-2 tab ตามเอกสาร (SO: สต๊อกและการส่ง · เครดิต·บิล·ชำระ / PO: รับของ · วางบิล / GRN: QC) — ใช้ `docTbl` + `linkBlock` |
| **PDF Preview** | `pdf` | file | toolbar (ตัวอย่าง PDF · A4 · n/n) + [ดาวน์โหลด][พิมพ์] ghost sm → กล่องเทา `#E5E7EB` padding 20 → `.a4` (720 max · 36/40 pad · 11px) = โลโก้+บริษัท / ชื่อเอกสาร EN+code / คู่ค้า+อ้างอิง 2 col / ตาราง # รายการ จำนวน หน่วย ราคา ลด% จำนวนเงิน / totals 300px ขวา / หมายเหตุ / 3 ช่องเซ็น (ผู้จัดทำ · ผู้อนุมัติ · [คู่ค้า]ยืนยัน) — template ตาม `thai-doc-pdf-generator` |
| **ลายเซ็น / อนุมัติ** | `sign` | pen-tool | card KV 4 col (DOA entry `.kbd` · สถานะ pill + ขั้น n/N · ผู้ส่ง `empChip` · ยืนยันโดย) + progress bar → note.warn ถ้าแก้ราคา → `SEC('pen-tool','ลำดับการอนุมัติ')` `.tl` timeline: ส่งอนุมัติ → ขั้น 1..N (role / `empChip(person)` / เวลา / note · ขั้นปัจจุบัน+canAct มีปุ่ม [ไม่อนุมัติ][อนุมัติ] inline) → ผลลัพธ์ → ประวัติอนุมัติ |
| **ประวัติ** | `history` | history | `SEC('history','ประวัติ (append-only)')` + `.tl` จาก `s.audit` (ok/warn/bad จาก act) |

**เอกสารแนบไม่ใช่ tab แยก** — เป็น section ใน "รายละเอียด" (landing) เพื่อให้เห็นครบในหน้าแรก

---

## 🏗️ Surface 4 — Modals (Pattern D) — DOA (มติ 2026-08-17)

- `openSubmitModal` → `renderSubmitModal`: resolve DOA → `.slot-row` ต่อขั้น (`34px 200px 1fr`: เลขขั้น · ตำแหน่ง · **combo เลือกคน** แสดง `empChip` = avatar + position + name) · สรุปยอด · [ยกเลิก][ส่งอนุมัติ]
- `openApproveModal` / `reasonModal` (ไม่อนุมัติ · ยกเลิก · พัก): textarea เหตุผล required + preset chips
- ทุก modal → `pushAudit` + toast **หลังปิด** (Rule #46)
- ห้าม hardcode chain — `resolveDoa()` เป็น stub `TODO: DOA engine`-free (ใช้ comment "resolve จาก GET /doa/resolve")

---

## 📦 Record contract (ขั้นต่ำที่ทุกเอกสารต้องมี)

```js
{ id, code, status, orderDate, dueDate, partner, rep, ref, sourceRef,
  lines: [ /* B2 line model */ ], endbill: {enabled, mode:'amount'|'percent', value, src},
  attachments: [{name,size}], note,
  doa_entry_ref, approval_status, approval_chain: [{roles, assignee, status, by, at, note}],
  submittedBy, submittedAt, confirmedBy, confirmedAt,
  audit: [{act, by, at, note}],           // append-only
  createdBy, createdAt, updatedBy, updatedAt }
```

---

## ✅ Self-check (Phase 5 — เพิ่มจาก checklist ปกติ)

- [ ] wizard 5 steps ชื่อตรง: เลือกแหล่งที่มา › ข้อมูลหลัก › รายการสินค้า › เอกสารแนบ › ตรวจสอบและยืนยัน
- [ ] step 3 = B2 v2 verbatim (grid widths 26/—/64/92/92/78/72/104/54 · `.line-tbl`)
- [ ] view tabs ลำดับ: รายละเอียด › [domain] › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ
- [ ] "เอกสารแนบ" อยู่ใน tab รายละเอียด (ไม่ใช่ tab)
- [ ] list มีคอลัมน์ ลายเซ็น (`renderSignProgress`) + สถานะเอกสาร (`docPill`)
- [ ] header actions เปลี่ยนตามสถานะ + divider + copy/printer/download/X
- [ ] PDF = `.a4` + 3 ช่องเซ็น
- [ ] submit modal = slot picker เลือกคน (avatar+position+name)
- [ ] CSS จาก `doc-archetype.css.html` ครบ (`.hard-warn .upload-zone .a4 .tl .free-row .line-tbl .slot-row .emp-chip .combo-pop`)
