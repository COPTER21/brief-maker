# 06_TESTS — F-PAY Payment Term (เงื่อนไขการชำระเงิน)

> **Audience:** QA engineer
> **Purpose:** Acceptance Criteria + DoD + Cross-Module + Microcopy-verbatim
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + HTML SoT
> **Expected text:** ยึด **HTML verbatim** ก่อน (§6.10) แล้ว fallback microcopy กลาง html-generator-v8 — ห้ามแต่งคำเอง

---

## §6.1 Acceptance Criteria (AC)

### AT-01: สร้างเงื่อนไข Credit — happy path (US-01)
**Given** Finance Admin เปิด create drawer, type=credit
**When** กรอก code (uppercase, ไม่ซ้ำ) + ชื่อ TH + net_days=30 + use_in≥1, กด "บันทึกและสร้าง"
**Then** POST /payment-terms → 201, status=active, used=0, DOA fields=null
**And** drawer ปิด + toast success **"สร้างเงื่อนไขชำระเงินแล้ว"**

### AT-02: code required + duplicate (BR-01)
**Given** create drawer · **When** code ว่าง → block, field-error **"กรุณากรอกรหัส"**
**When** code ซ้ำกับที่มีอยู่ → block, field-error **"รหัสนี้มีอยู่แล้ว — ใช้รหัสอื่น"** + toast **"รหัสเงื่อนไขนี้มีอยู่แล้ว"** · API → 409 ERR_DUPLICATE_CODE

### AT-03: Credit net_days > 0 (BR-02)
**Given** type=credit, net_days=0 (หรือว่าง) · **When** submit · **Then** block + toast **"จำนวนวันเครดิตต้องมากกว่า 0"** · API 422 ERR_CREDIT_DAYS_INVALID

### AT-04: Installment ≥2 & sum=100% (BR-04, ENG-PT-01)
**Given** type=installment · **When** 1 งวด → block + toast **"ต้องมีอย่างน้อย 2 งวด"** · ปุ่มลบงวด disabled เมื่อเหลือ 2 งวด
**When** รวม ≠ 100% → block + toast **"สัดส่วนงวดต้องรวมเป็น 100% (ตอนนี้ N%)"** · live total badge is-warn "(ต้องเป็น 100%)" / is-ok "✓" ที่ 100 · API → ENG-PT-01 valid=false

### AT-05: Deposit % 0<x≤100 (BR-03)
**Given** type=deposit, method=percent · **When** value>100 → toast **"มัดจำแบบ % ต้องไม่เกิน 100"** · **When** value≤0 → toast **"มัดจำแบบ % ต้องมากกว่า 0"** · API 422 ERR_DEPOSIT_PCT_INVALID
### AT-05b: Deposit manual → value ว่าง (EC-09)
**Given** method=manual · **Then** ช่อง value ซ่อน, ไม่ validate value, บันทึกได้

### AT-06: use_in ≥1 · ไม่มี PR (BR-06, D-08)
**Given** create · **When** use_in ว่าง → block + toast **"เลือกเอกสารที่ใช้อย่างน้อย 1 รายการ"**
**And** ตัวเลือก use_in = **7 เอกสาร** (po, ap_invoice, payment_voucher / so, quotation, ar_invoice, receipt) — **ไม่มี PR** ในทุกกลุ่ม · API ปฏิเสธค่า 'pr' (ไม่อยู่ใน enum)

### AT-07: Default 1/ประเภท + active (BR-07)
**Given** ตั้ง is_default=true บนตัว status≠active · **When** submit · **Then** block + toast **"ตั้งเป็นค่า Default ได้เฉพาะเงื่อนไขสถานะ ใช้งาน"**
**When** ตั้ง default ตัวใหม่ (active) → ตัวเก่าประเภทเดียวกันหลุด is_default อัตโนมัติ · list โชว์ ⭐ หลังรหัส

### AT-08: Discount days > 0 และ < net_days (BR-05)
**Given** type=credit, discount_pct=2, net_days=30 · **When** discount_days=30 (≥net) หรือ ≤0 · **Then** block + toast **"วันชำระเพื่อรับส่วนลดต้องมากกว่า 0 และน้อยกว่าวันเครดิต"**

### AT-09: แก้ไขได้แม้ used>0 (BR-08 / AD-01)
**Given** term ที่ used>0 · **When** edit เปลี่ยน field → PUT /:id 200 · **Then** master อัปเดต, **เอกสารเก่า snapshot ไม่เปลี่ยน** · toast **"บันทึกการแก้ไขแล้ว"** · (EC-03: เปลี่ยน type ก็ทำได้, no retro)

### AT-10: เปลี่ยนสถานะเดี่ยว (US-06)
**Given** P-04 view · **When** เมนู "เปลี่ยนสถานะ" เลือกค่าใหม่ (ค่าปัจจุบัน disabled) → PATCH /:id/status · **Then** toast **"เปลี่ยนสถานะเป็น [label] แล้ว"** (label: ร่าง/ใช้งาน/ไม่ใช้งาน)

### AT-11: bulk เปลี่ยนสถานะ (US-06)
**Given** เลือก N รายการ · **When** bulk bar กด "ใช้งาน/ไม่ใช้งาน/ร่าง" → POST /bulk-status · **Then** toast **"เปลี่ยนสถานะ N รายการเป็น [label] แล้ว"**

### AT-12: bulk ลบ + guard used>0 (US-07 / BR-08)
**Given** เลือกรายการรวม used>0 · **When** bulk "ลบ" → modal "เลือกไว้ N รายการ · M รายการถูกใช้งานอยู่จะถูกข้าม" · ปุ่ม **"ลบ D รายการ"** (disabled ถ้า D=0)
**When** ยืนยัน → POST /bulk-delete · **Then** toast **"ลบแล้ว D รายการ · ข้าม M รายการที่ถูกใช้งาน"** (info) หรือ **"ลบแล้ว D รายการ"** (success ถ้าไม่มีข้าม)

### AT-13: ค้นหา/กรอง List (US-08)
**Given** P-01 · **When** search รหัส/ชื่อ/EN + type filter + stat card (กดซ้ำยกเลิก) · **Then** ทำงานร่วมกัน, footer "แสดง N จาก M เงื่อนไข", scroll ไม่เด้ง (Iron Rule #29)

### AT-14: ไม่มี CSV (BR-09 — negative)
**Then** ไม่มีปุ่ม/จอ/endpoint import/export CSV ที่ใดในระบบ (toolbar มีแค่ "เพิ่มเงื่อนไข")

### AT-15: ปลายทาง active-only + Credit trigger locked (BR-10)
**Given** GET /active · **Then** คืนเฉพาะ status=active · **And** type=credit trigger แสดง lock badge "ทันที (ล็อกตามประเภท)" แก้ไม่ได้ (ไม่มี dropdown)

### AT-16: trigger default ต่อประเภท · after_deposit เฉพาะ deposit (BR-11)
**Then** prepay default after_full · deposit default+เฉพาะ after_deposit · postpay/installment/partial/credit default immediate

### AT-17: Direct ปิด po/quotation/so (BR-12)
**Given** type=direct_payment · **Then** ไม่มี trigger, ไม่มี due_basis · use_in po/quotation/so disabled ("ไม่รองรับ") + auto-remove · note "ไม่ผ่าน PR/PO/QUO→SO"

### AT-18: due_basis 3 ค่า (BR-13)
**Given** ประเภท ≠ direct · **Then** due_basis เลือกได้ 3 ค่า (invoice_date/eom/delivery)

### AT-19: Viewer/Consumer 403 (PM edge)
**Given** role=Finance Viewer เรียก POST/PUT/PATCH/bulk ตรง · **Then** 403 ERR_INSUFFICIENT_ROLE

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to | Priority |
|---|---|---|---|---|
| TC-01 | List + filter | API | AT-13 | P0 |
| TC-02 | Create credit happy | API | AT-01 | P0 |
| TC-03 | code required/dup | API neg | AT-02 | P0 |
| TC-04 | credit days>0 | API neg | AT-03 | P0 |
| TC-05 | installment ≥2/sum100 | API neg + ENG | AT-04 | P0 |
| TC-06 | deposit % range | API neg | AT-05 | P1 |
| TC-07 | use_in ≥1 / no PR | API neg | AT-06 | P0 |
| TC-08 | default 1/type + active | API | AT-07 | P0 |
| TC-09 | discount days | API neg | AT-08 | P1 |
| TC-10 | edit used>0 (snapshot) | API | AT-09 | P0 |
| TC-11 | status change (single/bulk) | API | AT-10/11 | P1 |
| TC-12 | bulk delete guard | API | AT-12 | P0 |
| TC-13 | no CSV (absence) | Static/API | AT-14 | P1 |
| TC-14 | active picker + credit lock | API | AT-15 | P1 |
| TC-15 | direct disables docs | API/UI | AT-17 | P1 |
| TC-CC-01 | concurrent default (409) | API stress | EC-01 | P1 |
| TC-ID-01 | idempotency create | API | EC-02 | P1 |
| TC-PR-01 | Viewer 403 | API | AT-19 | P1 |
| TC-UI-01 | P-01 render + scroll #29 | E2E | AT-13 | P1 |

---

## §6.3 Test Data Setup
- Seed 12 reference terms (จาก HTML `state.terms`) ครอบ 7 ประเภท · mix status (active/inactive/draft) · mix used (0..186)
- Roles: `qa_finance_admin`, `qa_finance_viewer`, `qa_consumer` (downstream)
- Tenants: 2 (isolation test)

---

## §6.4 Definition of Done (DoD)

### Code
- [ ] ทุก AT (AT-01..19) implemented + unit tests
- [ ] Integration: API + DB + ENG-PT-01/02
- [ ] E2E: happy + 7 validations + bulk + edit-used>0
- [ ] Server-side mirror ครบ 7 validations (Control C4)
- [ ] Coverage ≥ 80% logic layer

### Documentation
- [ ] API docs auto จาก 02_API
- [ ] FRD 07_LOCKED สะท้อน final
- [ ] **CUBIC Registry: ENG-PT-01 + ENG-PT-02 registered** (Architect — OQ-ENG-REG)

### QA
- [ ] P0 + P1 pass · ไม่มี P0/P1 bug open
- [ ] Security checklist D2/D5/D9/D15/D17 verified
- [ ] **Blocking OQ ปิด:** OQ-PAY-04 (deposit VAT), OQ-PAY-07 (used def) ก่อน dev ส่วนที่เกี่ยว

### Deployment
- [ ] Migration tested (2 tables + config seed, ห้าม hardcode)
- [ ] Downstream picker SLA <500ms verified

---

## §6.5 WebSocket / Realtime
- **N/A** — ไม่มี NOTIF/WebSocket (SCOPE_LOCK). Feedback = toast เท่านั้น.

---

## §6.6 Performance Benchmarks
| Endpoint | P95 | Note |
|---|---|---|
| GET /payment-terms (list) | < 800ms | small master |
| GET /payment-terms/active (picker) | **< 500ms** | BRD §17.1 SLA · cacheable |
| POST/PUT /payment-terms | < 1000ms | validate + ENG-PT-01 |

---

## §6.7 Test Environment Notes
- ENG-PT-01/02 ใน TEST mode (deterministic) · downstream (PO/Invoice) = mock consumer เรียก GET /active
- `used` = mock counter จนกว่า OQ-PAY-07 ปิด (นิยามจริง)

---

## §6.8 Trace: AC → Logic Coverage

| AT | API tested | Functions | Engines |
|---|---|---|---|
| AT-01 | API-02 | FN-01, FN-03, FN-09 | — |
| AT-02 | API-02/04 | FN-03 | — |
| AT-03 | API-02 | FN-03 | — |
| AT-04 | API-02 | FN-03 | ENG-PT-01 |
| AT-05 | API-02 | FN-03 | — |
| AT-06 | API-02 | FN-03 | — |
| AT-07 | API-02/04 | FN-08 | — |
| AT-08 | API-02 | FN-03 | — |
| AT-09 | API-04 | FN-02 | — |
| AT-10/11 | API-05/06 | FN-05, FN-06 | — |
| AT-12 | API-07 | FN-07 | — |
| AT-13 | API-01 | FN-04, FN-10 | — |
| AT-15 | API-08 | FN-11 | ENG-PT-02 |
| AT-16/17 | API-02 | FN-09 | — |

> **Coverage check:** FN-01..11 + ENG-PT-01/02 ทุกตัวถูก trace ≥1 AT ✅

---

## §6.9 Cross-Module Test Cases ⭐ (จาก BRD §12.1 Downstream)

| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | ปลายทาง (PO) เลือก active term → สร้างเอกสาร | PO / SO / PV | snapshot code+config ลง PO · master แก้ทีหลัง → PO snapshot ไม่เปลี่ยน |
| XT-02 | master → inactive | picker | ไม่โผล่ใน PO ใหม่ · เอกสารเก่า snapshot ยังใช้ได้ (EC-05) |
| XT-03 | installment term ใช้ที่ AP/AR Invoice | Accounting/GL | ENG-PT-01 แตก journal item ต่องวด → aging ต่องวด |
| XT-04 | deposit term รับมัดจำ | Tax Code / GL (Hook-2) | ออกใบกำกับภาษี ณ จุดรับเงิน (pending OQ-PAY-04) |
| XT-05 | deposit/prepay term → คลัง | Warehouse/GRN/Ship (ENG-PT-02) | trigger resolver: prepay=after_full, deposit=after_deposit, credit=immediate(locked) · P2P→GRN, S2C→Ship |
| XT-06 | Central Plan [config] edges | PO / AR Invoice / AP Invoice | ทั้ง 3 อ้าง term ผ่าน use_in ได้ (representable) |

---

## §6.10 Microcopy-Aware Expected Text (HTML verbatim)

> ยึดข้อความจริงบนจอก่อนเสมอ. ค่าเหล่านี้ extracted จาก `01_HTML/f-payterm.html` — ห้ามแต่งใหม่.

**Buttons:** "เพิ่มเงื่อนไข" (list) · "บันทึกและสร้าง" (create footer) · "บันทึกการแก้ไข" (edit footer) · "ยกเลิก" · "ปิด" (view) · "แก้ไข" · "เปลี่ยนสถานะ" · modal "ลบ D รายการ" / "ยกเลิก".

**Toasts:**
| เหตุการณ์ | ข้อความ verbatim | variant |
|---|---|---|
| สร้างสำเร็จ | `สร้างเงื่อนไขชำระเงินแล้ว` | success |
| แก้ไขสำเร็จ | `บันทึกการแก้ไขแล้ว` | success |
| bulk status | `เปลี่ยนสถานะ N รายการเป็น [label] แล้ว` | success |
| status เดี่ยว | `เปลี่ยนสถานะเป็น [label] แล้ว` | success |
| bulk delete (มีข้าม) | `ลบแล้ว D รายการ · ข้าม M รายการที่ถูกใช้งาน` | info |
| bulk delete (ไม่ข้าม) | `ลบแล้ว D รายการ` | success |
| code ซ้ำ | `รหัสเงื่อนไขนี้มีอยู่แล้ว` | error |
| installment <2 | `ต้องมีอย่างน้อย 2 งวด` | error |
| installment ≠100 | `สัดส่วนงวดต้องรวมเป็น 100% (ตอนนี้ N%)` | error |
| deposit %>100 | `มัดจำแบบ % ต้องไม่เกิน 100` | error |
| deposit %≤0 | `มัดจำแบบ % ต้องมากกว่า 0` | error |
| credit ≤0 | `จำนวนวันเครดิตต้องมากกว่า 0` | error |
| use_in ว่าง | `เลือกเอกสารที่ใช้อย่างน้อย 1 รายการ` | error |
| discount days | `วันชำระเพื่อรับส่วนลดต้องมากกว่า 0 และน้อยกว่าวันเครดิต` | error |
| default non-active | `ตั้งเป็นค่า Default ได้เฉพาะเงื่อนไขสถานะ "ใช้งาน"` | error |

**Field errors (inline):** code ว่าง = `กรุณากรอกรหัส` · code ซ้ำ = `รหัสนี้มีอยู่แล้ว — ใช้รหัสอื่น` · installment = `สัดส่วนงวดต้องรวมเป็น 100%` · use_in = `เลือกอย่างน้อย 1 เอกสาร`.

**Empty/list:** empty = `ไม่พบเงื่อนไขที่ตรงกับการค้นหา` · footer = `แสดง N จาก M เงื่อนไข` · ph-count = `N เงื่อนไข`.

**Status labels:** `ร่าง` / `ใช้งาน` / `ไม่ใช้งาน`. **Trigger lock badge:** `Warehouse/GRN trigger: ทันที (ล็อกตามประเภท)`.

> ผลลัพธ์: testcase ที่ ai-testcase-md-generator สร้างต่อจะ match หน้าจอจริง 1:1.
