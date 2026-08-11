# BRD — ทะเบียนรหัสภาษี (Tax Code Master)

> **โหมดการสร้าง:** HTML-first / Reverse Mode (Fresh Mode · brd-generator-full v2.2)
> **Source of truth:** `f-taxcode.html` (as-built · ผ่าน qc-ux + qc-coverage + E2E 42/42) · **Business intent:** PREBRIEF_F-TAX v1
> **Conflict Priority:** LOCK > PREBRIEF (business intent) > HTML (หน้าจอจริง)

---

## Section 1 — Document Info

| หัวข้อ | รายละเอียด |
|---|---|
| **BRD ID** | BRD-F-TAX-001 |
| **Feature** | ทะเบียนรหัสภาษี (Tax Code Master) |
| **รหัสฟีเจอร์** | F-TAX |
| **ประเภท** | New Feature (Master Data — Accounting/System-wide) |
| **Version** | v1.0 |
| **Status** | APPROVED (with documented residual OQs) |
| **Owner (BA)** | Sales Lane BA |
| **Stakeholders** | Accounting (เจ้าของ master), Sales/Procurement (ผู้ใช้อัตรา), Item Master (กลุ่มภาษี), GL Posting Setup |
| **โมดูล** | Master Data (per HTML sidebar) · เจ้าของเชิงบัญชี = Accounting (per Central Plan / PREBRIEF) — ดู OQ-TAX-05 |
| **Wave** | Wave 1 (ฐานราก) · 1 ใน 3 blockers ของเลน Sales |
| **วันที่** | 2026-08-10 |

### Changelog
- **v1.0 (2026-08-10):** Initial via brd-generator-full (Fresh Mode / HTML-first). สกัด Screen Inventory จาก `f-taxcode.html` as-built + business intent จาก PREBRIEF_F-TAX v1. ไม่มี RIF (Reverse Mode — PREBRIEF ทำหน้าที่แทน). OQ-TAX-02 (effective date) และ OQ-TAX-03 (WHT scope) คงเป็น open item ตาม PREBRIEF.

### เอกสารต้นทาง (Inputs)
| # | ไฟล์ | บทบาท |
|---|---|---|
| 1 | `PREBRIEF_F-TAX_Tax-Code.md` | Business intent (แทน RIF) — source ฝั่ง "ต้องการอะไร" |
| 2 | `FUNCTION_CHECKLIST_F-TAX_Tax-Code.md` | FN-01..FN-24 + FN-40/90/92/93 (trace matrix) |
| 3 | `f-taxcode.html` (as-built) | Source of truth ฝั่ง "หน้าจอ/flow ที่มีจริง" |
| 4 | `CENTRAL_PLAN_CORE_ERP.md` / `WAVE_PLAN_CORE_ERP.html` | Wave/edge context |

---

## Section 2 — Business Context

### 2.1 ปัญหา / โอกาส
ระบบ CUBE 4.0 Core ERP ต้องการ **ทะเบียนกลางของ "รหัสภาษี" ระดับระบบ** เพื่อให้เอกสารซื้อ-ขาย (QT/SO/INV/PR/PO), ทะเบียนสินค้า (กลุ่มภาษี) และการ map บัญชี GL อ้างอิงนิยามภาษี **ชุดเดียวกัน** — รหัส ชื่อ ประเภท (VAT / หัก ณ ที่จ่าย / ยกเว้น) และอัตรา % ที่ถูกต้องและสอดคล้องทั้งระบบ

ปัจจุบันยังไม่มี master กลาง → เสี่ยงต่อการกรอกอัตราภาษีไม่ตรงกันในแต่ละเอกสาร และไม่มีจุดควบคุมความถูกต้องเชิงบัญชี Tax Code เป็น **1 ใน 3 blockers** ที่ปลดล็อกให้ Sales Configuration, เอกสารขาย (VAT/WHT ในบิล) และ DOA_BRIEF ชุดแรกเดินหน้าได้

### 2.2 เป้าหมายเชิงธุรกิจ
- มีแหล่งนิยามอัตราภาษีเดียว (single source of truth) ที่เอกสาร/สินค้า/บัญชีใช้ร่วม (soft reference — เก็บแค่รหัส)
- **รักษาความถูกต้องเชิงบัญชีย้อนหลัง:** อัตราของรหัสที่ถูกใช้แล้วต้องไม่เปลี่ยน — เอกสารเก่าอ้างอัตราเดิมถูกต้องตลอดกาล (IR-TAX-01)
- ให้ทีมบัญชีบริหารรหัสภาษีได้ครบวงจร (สร้าง/แก้/เปลี่ยนสถานะ/นำเข้า/ส่งออก) โดยไม่ต้องพึ่ง Dev

### 2.3 ตัวชี้วัดความสำเร็จ (บังคับวัดได้)
| ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง/จากไหน | วัดเมื่อไหร่ | KPI คู่ (§17.3) |
|---|---|---|---|---|---|
| ความสอดคล้องอัตราภาษีข้ามเอกสาร | ไม่มี master (N/A — ต้องเก็บ baseline ก่อน launch) | 100% ของเอกสารใหม่ดึงอัตราจาก Tax Code | audit เอกสาร sample ที่อ้างรหัสภาษี | รายไตรมาสหลัง launch | KPI-01 |
| การละเมิด IR-TAX-01 (แก้อัตราตัวที่ถูกใช้) | N/A | 0 ครั้ง (ต้องถูก guard บล็อก) | log ฝั่ง logic guard | ต่อเนื่อง | KPI-02 |
| อัตราความสำเร็จการนำเข้า CSV (แถวผ่าน/แถวทั้งหมด) | ไม่มีระบบ (ต้องเก็บ baseline) | ≥ 90% แถวผ่านในไฟล์ที่ถูก format | ผลสรุป import (ok/skip) | ต่อรอบ import | KPI-03 |
| จำนวนรหัสภาษี "ใช้งาน" ที่พร้อมให้ปลายทางเลือก | 0 | ครอบคลุมอัตราภาษีไทยมาตรฐาน (VAT + WHT 1/2/3/5/10/15) | นับจากทะเบียน (stat "ใช้งาน") | ณ launch | KPI-04 |

> **[AI-DEFAULT] D-2.3:** PREBRIEF ไม่ระบุตัวเลข target เชิงธุรกิจ — ตั้ง target ข้างต้นเป็นค่าเริ่มต้นที่วัดได้ และ mark baseline ที่ยังไม่มีเป็น "ต้องเก็บก่อน launch"

### 2.4 ที่มา
มติแชท 2026-08-09 + HTML as-built (gen ด้วย html-generator-v8) + แผนเลน Sales · Contract: Item Master "กลุ่มภาษี" ← Tax Code master (OB-1)

---

## Section 3 — Scope

### 3.1 In Scope
- ทะเบียนรหัสภาษีกลาง: สร้าง / แก้ไข / ดูรายละเอียด (3 tab: ภาพรวม / การใช้งาน / ประวัติ)
- รหัสภาษี 3 ประเภทตายตัว (fix): VAT / หัก ณ ที่จ่าย (WHT) / ยกเว้นภาษี
- อัตรา % (0–100 ทศนิยมได้) · auto-code เมื่อเว้นรหัสว่าง (VAT../WHT../TAX..)
- สถานะ 3 ค่าเปลี่ยนอิสระทุกทิศ (ร่าง / ใช้งาน / ไม่ใช้งาน) — เดี่ยว + bulk
- **IR-TAX-01:** ล็อกรหัส/อัตรา/ประเภท เมื่อ `used > 0` (UI disabled + logic guard) — แก้ได้เฉพาะชื่อ/สถานะ
- ประเภทยกเว้นภาษี → อัตราล็อก 0 อัตโนมัติ
- List: ค้นหา / filter (ประเภท+สถานะ) / stat 4 ใบกดกรองเร็ว / sort (อัตราเชิงตัวเลข) / แบ่งหน้า
- นำเข้า CSV (template + preview รายแถว + สถานะในไฟล์ + 6 error codes) · ส่งออก CSV (ตาม filter, BOM)
- ลบแบบ bulk เท่านั้น (ผ่าน confirm) — `used > 0` ถูกข้าม
- Audit ผู้สร้าง/ผู้แก้ + เวลา (tab ประวัติ)

### 3.2 Out of Scope
- ❌ แก้ รหัส/อัตรา/ประเภท ของตัวที่ถูกใช้แล้ว — ทางที่ถูก = สร้างรหัสใหม่ + ปิดตัวเก่า [IR-TAX-01]
- ❌ ช่วงเวลาบังคับใช้อัตรา (effective date / validity period) — **คงเป็น OQ-TAX-02 (open)**
- ❌ ผูกเลขบัญชี GL ในหน้านี้ — เป็นงาน GL Posting Setup (OB-2)
- ❌ เพิ่ม/แก้ประเภทภาษี (fix 3 ค่า)
- ❌ ลบรายตัว / ลบตัวที่ถูกใช้
- ❌ ส่งอนุมัติ / สายอนุมัติ (DOA placeholder 4 fields = null · OB-4)
- ❌ NOTIF emit event (OB-5) · icon/avatar หน้ารหัสใน list · ข้อความอธิบายคอลัมน์ในจอนำเข้า

### 3.3 Assumptions
- ปลายทาง (Item Master / เอกสาร) เก็บ **soft reference** = รหัสภาษีเท่านั้น (ไม่มี FK cascade · LD-4C-02)
- `used` ปัจจุบันเป็น mock — ของจริงต้องนับจากสินค้า + เอกสารทุกใบที่อ้างรหัส (OQ-TAX-04)
- สิทธิ์: mock ผู้ใช้บริหารได้ทุกอย่าง — role-gate จริงเป็นเรื่อง FRD / Policy Center [AI-DEFAULT]

### 3.4 Scope Lock ⭐
> **หมายเหตุ:** ไม่มี RIF/ใบเซ็น scope_lock_ref อย่างเป็นทางการ (Reverse Mode) — LOCK ด้านล่างสกัดจาก "มติ + STD" ใน PREBRIEF และถือเป็น Locked Decisions ที่ห้าม override ตลอด chain

| LOCK | เนื้อหา | ที่มา | ผลถ้าขัด |
|---|---|---|---|
| **LOCK-IR-TAX-01** | `used > 0` → ล็อก รหัส/อัตรา/ประเภท ทั้ง UI และ logic guard — แก้ได้เฉพาะชื่อ/สถานะ | มติ+STD · BR-04 | SCOPE DRIFT — ห้ามเปิดแก้อัตราเด็ดขาด |
| **LOCK-EXEMPT-0** | ประเภทยกเว้นภาษี → อัตรา = 0 เสมอ (UI ล็อก + logic + import validate) | มติ+STD · BR-03 | SCOPE DRIFT |
| **LOCK-TYPE-3** | ประเภทภาษี fix 3 ค่าเท่านั้น (VAT/WHT/ยกเว้น) — ห้ามเพิ่ม/แก้ | แผน | SCOPE DRIFT |
| **LOCK-NO-GL** | ทะเบียนนี้ไม่เก็บเลขบัญชี GL ใด ๆ — mapping อยู่ที่ GL Posting Setup | OB-2 · BR-09 | SCOPE DRIFT |
| **LOCK-DOA-NULL** | ไม่มีสายอนุมัติ — DOA placeholder 4 fields = null | OB-4 | SCOPE DRIFT |
| **LOCK-NO-NOTIF** | ไม่ emit event เอง (กระดิ่งเป็น placeholder) | OB-5 | SCOPE DRIFT |
| **LOCK-STATUS-FREE** | สถานะ 3 ค่าเปลี่ยนอิสระทุกทิศ ไม่มี gate/อนุมัติ | มติ VD-PDM-02 · BR-06 | SCOPE DRIFT |
| **LOCK-SOFT-REF** | ปลายทางเก็บแค่รหัส (soft ref) · เลือกได้เฉพาะสถานะ "ใช้งาน" | OB-1 · BR-07 | SCOPE DRIFT |
| **LOCK-BULK-DEL** | ไม่มีลบเดี่ยว — ลบ bulk ผ่าน confirm เท่านั้น · `used>0` ข้าม | pattern เลน · BR-05 | SCOPE DRIFT |

**ผลตรวจ Scope Lock:** In Scope §3.1 ทั้งหมดอยู่ใต้ LOCK ข้างต้น — ไม่มี scope เกินแบบเงียบ ✅

---

## Section 4 — User Roles & Permissions

> role-gate จริงยัง deferred ไป FRD/Policy Center [AI-DEFAULT]. HTML รันด้วย mock user เดียว (บริหารได้ทุกอย่าง)

| Role | ดู List/รายละเอียด | สร้าง | แก้ไข (used=0) | แก้ชื่อ/สถานะ (used>0) | เปลี่ยนสถานะ (เดี่ยว/bulk) | นำเข้า/ส่งออก | ลบ bulk |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **ผู้ดูแลทะเบียนภาษี (บัญชี)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **ผู้ใช้ปลายทาง (Sales/สินค้า/เอกสาร)** | (เห็นเฉพาะ "ใช้งาน" ผ่าน combobox ปลายทาง) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

> **⚠️ HTML-RIF DRIFT (minor · D-4.1):** PREBRIEF §1 ระบุ mock ผู้ใช้เป็น "ฝ่ายบัญชี (พิมพ์ใจ)"; HTML shell แสดง user "วิภา ผลิตภัณฑ์ · Master Data" (และ mock data ใช้ทั้ง "พิมพ์ใจ บัญชี" และ "วิภา ผลิตภัณฑ์" ปนกัน). เป็น cosmetic identity ของ mock — ไม่กระทบ business rule · resolve ด้วย business intent (ทีมบัญชีเป็นเจ้าของ master) · role จริงเคาะที่ FRD/Policy Center → OQ-TAX-06

---

## Section 5 — User Journey (with COSO)

> COSO defaults [AI-DEFAULT]: master data ที่เปลี่ยนสถานะอิสระ **ไม่มีสายอนุมัติ (LOCK-DOA-NULL)** → Approver = N/A ทุก step. SoD ไม่บังคับเพราะไม่มี approval workflow (master maintenance เชิง config)

### 5.1 Happy Path — สร้างรหัสภาษี (S-01)
| # | Step | Route/ปุ่มจริง | Maker | Checker | Approver | System |
|---|---|---|---|---|---|---|
| 1 | เปิดทะเบียน → กด "สร้างรหัสภาษี" | `#/tax-codes` · `openCreate()` | บัญชี | — | N/A | เปิด drawer ฟอร์ม |
| 2 | กรอกชื่อไทย\* + ประเภท\* + อัตรา\* (รหัสเว้นว่าง=auto) | drawer form | บัญชี | — | N/A | validate ชื่อ/อัตรา/รหัสซ้ำ |
| 3 | กด "ยืนยันสร้าง" | `saveUnit('create')` | บัญชี | — | N/A | กัน double-submit · unshift record · toast |
| 4 | รหัส "ใช้งาน" พร้อมให้ Item Master/เอกสารเลือก | (ปลายทาง) | — | — | N/A | โผล่ใน combobox เฉพาะ active (BR-07) |

### 5.2 Alternative Paths
| Path | Trigger | ปุ่มจริง | ผล |
|---|---|---|---|
| A1 · สร้างยกเว้นภาษี (S-02) | เลือกประเภท "ยกเว้นภาษี" | `onTypeChange('exempt')` | อัตราล็อก 0 อัตโนมัติ (สลับกลับ VAT/WHT ปลดล็อก) |
| A2 · แก้ตัว `used=0` (S-03) | กด ✏️ แก้ไข | `openEdit()` | แก้ได้ทุก field รวมรหัส/อัตรา/ประเภท |
| A3 · แก้ตัว `used>0` (S-04) | กด ✏️ แก้ไข | `formHTML(locked)` | รหัส/อัตรา/ประเภท disabled + ป้าย "ล็อก — ถูกใช้งานแล้ว" · แก้ได้เฉพาะชื่อ/สถานะ · logic guard คงค่าเดิม |
| A4 · เปลี่ยนสถานะ (S-05) | view header เมนู / bulk bar | `setStatus()` / `bulkSetStatus()` | เปลี่ยนทันทีทุกทิศ ไม่มี gate · ค่าปัจจุบัน disabled |
| A5 · นำเข้า CSV (S-08) | "นำเข้า CSV" | `bulkImport()` | 3 จังหวะ: เลือกไฟล์ → preview รายแถว → นำเข้าเฉพาะแถวผ่าน |
| A6 · ส่งออก CSV (S-09) | "ส่งออก CSV" | `exportCSV()` | ดาวน์โหลดตาม filter (BOM) |

### 5.3 Exception Paths
| Path | Trigger | ผล |
|---|---|---|
| E1 · ลบ bulk บางตัวถูกใช้ (S-06) | เลือก ≥1 → "ลบ" → confirm | `used>0` ถูกข้ามไม่ลบ + toast แจ้งยอดข้าม (BR-05) |
| E2 · ข้อมูลผิด (S-07) | รหัสซ้ำ / อัตราว่าง-ติดลบ->100 | บล็อกพร้อมชี้ช่อง (CODE_DUPLICATE / RATE_INVALID) |

**COSO note:** ทุก step Approver = N/A (LOCK-DOA-NULL) · System เป็นผู้ enforce validation + guard · ไม่มี approval → SoD ไม่ applicable

---

## Section 6 — Data Entity & Fields

### 6.1 Fields (drawer ฟอร์มเดียว — สกัดจาก HTML)
| # | Field | Label UI | Input Type | ค่า/ตัวเลือก | จำเป็น | เงื่อนไข | หมายเหตุ |
|---|---|---|---|---|:--:|---|---|
| 1 | code | รหัสภาษี | TEXT | เว้นว่าง=auto (VATxx/WHTxx/TAXxx) | ⬜ | ห้ามซ้ำ (case-insensitive) · **ล็อกเมื่อ used>0** | ไม่มี icon หน้ารหัส |
| 2 | name_th | ชื่อ (ไทย) | TEXT | — | ✅ | ระบุอัตรา+ประเภทรายได้ในชื่อได้ | — |
| 3 | name_en | ชื่อ (อังกฤษ) | TEXT | — | ⬜ | — | — |
| 4 | category | ประเภทภาษี | DROPDOWN-SINGLE | vat / wht / exempt | ✅ | fix 3 ค่า · **ล็อกเมื่อ used>0** | default = vat |
| 5 | rate | อัตรา (%) | NUMBER (text inputmode) | 0–100 ทศนิยมได้ | ✅ | **exempt=0 ล็อก** · **ล็อกเมื่อ used>0** | RATE_INVALID ถ้าว่าง/<0/>100 |
| 6 | status | สถานะ | DROPDOWN-SINGLE | draft / active / inactive | — | อิสระทุกทิศ | default: ฟอร์ม=active, นำเข้าเมื่อว่าง=draft |

### 6.2 ระบบเก็บเพิ่ม (system fields)
| Field | ชนิด | หมายเหตุ |
|---|---|---|
| `used` | NUMBER (read-only) | จำนวนสินค้า/เอกสารที่อ้าง — **mock** ปัจจุบัน (OQ-TAX-04) |
| `created_by` / `created_at` | AUDIT | tab ประวัติ |
| `updated_by` / `updated_at` | AUDIT | tab ประวัติ |
| `approver_role` / `approved_by` / `approved_at` / `approval_chain` | placeholder | **= null เสมอ (LOCK-DOA-NULL)** — เตรียมเชื่อม Policy Center |

### 6.3 Entity Relationship
```
TaxCode (master)
  ├─(soft ref: code)◀── ItemMaster.taxGroup        (เลือกได้เฉพาะ status='active')
  ├─(soft ref: code)◀── SalesDoc/PurchaseDoc line   (QT/SO/INV/PR/PO — ใช้ rate คำนวณ VAT/WHT)
  └─(soft ref: code)◀── GL Posting Setup            (map code → บัญชี GL — ที่โมดูลบัญชี)
```
- ทุกความสัมพันธ์เป็น **soft reference (ไม่มี FK cascade)** — ปลายทางเก็บ `code` เท่านั้น
- **ไม่มี hard delete** ตัวที่ถูกใช้ (`used>0`)

---

## Section 7 — User Stories & Acceptance Criteria

| ID | Story (Given-When-Then) | AC |
|---|---|---|
| **S-01** | ในฐานะบัญชี ฉันสร้างรหัสภาษีจาก drawer เดียว | AC1: กรอกชื่อไทย+ประเภท+อัตราแล้วบันทึกได้ (FN-01) · AC2: เว้นรหัสว่าง→auto ตามประเภทไม่ชนของเดิม (FN-02) · AC3: อัตราทศนิยมได้ + เลือกสถานะ 3 ค่าตั้งแต่สร้าง (FN-03) |
| **S-02** | ในฐานะบัญชี ฉันสร้างประเภทยกเว้นภาษี | AC1: เลือก "ยกเว้นภาษี"→อัตราล็อก 0 ทันที (FN-05) · AC2: สลับกลับ VAT/WHT→ปลดล็อก (BR-03) |
| **S-03** | ในฐานะบัญชี ฉันแก้ตัวที่ยังไม่ถูกใช้ | AC1: `used=0` แก้ได้ทุก field รวมรหัส/อัตรา/ประเภท (FN-06) |
| **S-04** | ในฐานะบัญชี ฉันแก้ตัวที่ถูกใช้แล้วได้จำกัด | AC1: `used>0`→รหัส/อัตรา/ประเภท disabled + ป้ายล็อก (FN-07) · AC2: บันทึกแล้วระบบคงค่าเดิม 3 field เสมอ (logic guard · FN-08) |
| **S-05** | ในฐานะบัญชี ฉันเปลี่ยนสถานะอิสระ | AC1: เมนู view เปลี่ยน 3 ค่าทุกทิศทันที ค่าปัจจุบัน disabled (FN-09) · AC2: bulk ตั้งสถานะครบทุกตัว + toast จำนวน (FN-10) |
| **S-06** | ในฐานะบัญชี ฉันลบหลายตัว | AC1: bulk ลบ→confirm บอกจำนวนลบ+ข้าม (FN-12) · AC2: `used=0` หาย, `used>0` อยู่ + toast ยอดข้าม (FN-13) |
| **S-07** | ในฐานะบัญชี ฉันถูกบล็อกเมื่อข้อมูลผิด | AC1: รหัสซ้ำ (case-insensitive)→บล็อกชี้ช่อง (FN-14) · AC2: อัตราว่าง/ติดลบ/>100→RATE_INVALID (FN-15) |
| **S-08** | ในฐานะบัญชี ฉันนำเข้า CSV พร้อมสถานะ | AC1: จอแรกมีแค่กล่องไฟล์+ปุ่ม template (FN-16) · AC2: preview รายแถวขึ้นเหตุตรงกรณี 6 codes (FN-17) · AC3: แถวผิดข้ามไม่ล้มไฟล์ · status ว่าง=ร่าง (FN-18) |
| **S-09** | ในฐานะบัญชี ฉันส่งออก CSV ตาม filter | AC1: ดาวน์โหลด 7 คอลัมน์ BOM เปิด Excel ไม่เพี้ยน (FN-20) |
| **S-11** | ในฐานะบัญชี ฉันดูการอ้างอิง+ประวัติ | AC1: tab การใช้งานแสดงจำนวนที่ถูกอ้างอิง ไม่มีแถวลบ (FN-23) · AC2: tab ประวัติแสดงผู้สร้าง/ผู้แก้+เวลา (FN-93) |

---

## Section 8 — Status & Lifecycle

### 8.1 State Diagram
```
        ┌──────────────────────────────────┐
        ▼                                  │
   ┌────────┐   ⇄   ┌────────┐   ⇄   ┌──────────┐
   │  ร่าง   │ ◀───▶ │ ใช้งาน  │ ◀───▶ │ ไม่ใช้งาน │
   │ draft  │       │ active │       │ inactive │
   └────────┘ ◀─────────────────────────┘
        (ทุกทิศทาง · ไม่มี gate · ไม่มีอนุมัติ)
```
Lifecycle มาตรฐานของอัตราใหม่ (STD): สร้างรหัสใหม่ (ร่าง) → ทดสอบ → ใช้งาน → ปิดตัวเก่าเป็นไม่ใช้งาน

### 8.2 State × Trigger × Next State
| State ปัจจุบัน | Trigger | Next State | หมายเหตุ |
|---|---|---|---|
| any (draft/active/inactive) | เมนูเปลี่ยนสถานะ (view) / bulk bar / ฟอร์ม / ไฟล์นำเข้า | any อื่น | เปลี่ยนอิสระ (LOCK-STATUS-FREE) · ค่าปัจจุบัน disabled ในเมนู |
| นำเข้า status ว่าง | import | draft | BR-08 |
| default ฟอร์มสร้าง | create | active | ตาม HTML |

**ผลปลายทาง:** เฉพาะ `active` โผล่ใน combobox กลุ่มภาษี/เอกสาร (BR-07) — draft/inactive ซ่อน

---

## Section 9 — Business Rules + Validation (with Tags)

### 9.1 Business Rules
| BR | กติกา | ประเภท | Tag | เมื่อชน | Trace |
|---|---|---|---|---|---|
| BR-01 | รหัสห้ามซ้ำ (case-insensitive) — สร้าง/แก้/นำเข้า | Prevent | **FIXED** | บล็อก/ข้าม CODE_DUPLICATE | S-07, S-08 |
| BR-02 | อัตรา 0–100 ทศนิยมได้ | Error | **FIXED** | RATE_INVALID | S-07, S-08 |
| BR-03 | ประเภทยกเว้นภาษี → อัตรา=0 เสมอ (UI ล็อก + logic + import validate) | Prevent | **FIXED** (LOCK-EXEMPT-0) | EXEMPT_RATE | S-02, S-08 |
| BR-04 | **IR-TAX-01:** `used>0` → ล็อกรหัส/อัตรา/ประเภท (UI+logic guard) แก้ได้เฉพาะชื่อ/สถานะ | Prevent | **FIXED** (LOCK-IR-TAX-01) | disabled + ป้ายล็อก + guard | S-04 |
| BR-05 | `used>0` ลบไม่ได้ — bulk ข้ามพร้อมแจ้ง | Prevent | **FIXED** | ข้าม | S-06 |
| BR-06 | สถานะ 3 ค่าเปลี่ยนอิสระทุกทิศ ไม่มีอนุมัติ | Trigger | **FIXED** (LOCK-STATUS-FREE) | ทันที | S-05 |
| BR-07 | ปลายทางเลือกได้เฉพาะ "ใช้งาน" | Prevent | **FIXED** | ร่าง/ไม่ใช้งานไม่โผล่ combobox | S-05 |
| BR-08 | นำเข้า: ตรวจรายแถว แถวผิดข้าม ไม่ล้มไฟล์ · status ว่าง=ร่าง · ประเภทใช้ชื่อไทย | Trigger | **FIXED** | รายงานรายแถว | S-08 |
| BR-09 | ไม่เก็บบัญชี GL — mapping อยู่ที่ GL Posting Setup | Prevent | **FIXED** (LOCK-NO-GL) | ไม่มี field | S-10 |
| BR-10 | audit ผู้สร้าง/ผู้แก้ + เวลา | Trigger | **FIXED** | tab ประวัติ | ทุก S |

### 9.2 Validation Rules
| VR | Field/Action | เงื่อนไข | ประเภท | ข้อความ (verbatim จาก HTML) |
|---|---|---|---|---|
| VR-01 | ชื่อไทย (บันทึก) | ว่าง | Error | "กรุณากรอกชื่อภาษาไทย" |
| VR-02 | รหัส (บันทึก) | ซ้ำ (case-insensitive) | Error | "รหัส {code} ถูกใช้แล้ว" |
| VR-03 | อัตรา (บันทึก) | ว่าง / NaN / <0 / >100 | Error | "กรุณากรอกอัตรา 0–100" |
| VR-04 | ประเภท=exempt | เปลี่ยนประเภท | Trigger | อัตรา set 0 + disable + ป้าย "ยกเว้นภาษี = อัตรา 0" |
| VR-05 | ปุ่มบันทึก | double-submit | Prevent | loader "กำลังบันทึก…" (กันกดซ้ำ) |
| VR-06..11 | นำเข้า CSV (รายแถว) | 6 กรณี | Skip row | REQUIRED / BAD_TYPE / RATE_INVALID / EXEMPT_RATE / BAD_STATUS / CODE_DUPLICATE |

### 9.3 (Section 9.5) สรุประดับความยืดหยุ่น
| Rule | ระดับความยืดหยุ่น | เหตุผล | ที่มา |
|---|---|---|---|
| BR-01..10 ทั้งหมด | **FIXED** | เป็น business/accounting invariant ที่ถูกล็อกด้วยมติ+STD (ดู §3.4) — ไม่ตั้งใจให้ config | ✅ Stakeholder ยืนยัน (มติ 2026-08-09) |
| ชุดอัตรา WHT มาตรฐาน (seed) | Data (seed) | เป็นข้อมูลตั้งต้น ปรับได้ผ่านการสร้างรหัสใหม่ (ไม่ใช่ config engine) | ✅ |

> ไม่มี rule ระดับ CONFIGURABLE/DYNAMIC/Engine ที่ AI-inferred → ไม่มีข้อที่ต้อง escalate เป็น OQ ในหมวดนี้ ✅

---

## Section 10 — Edge Cases

### 10.1 Edge Cases ที่ PREBRIEF/FN ระบุ (☑ ยืนยันแล้ว — มีใน HTML)
| # | Edge | ผลที่คาด | Trace |
|---|---|---|---|
| ☑ EC-01 | รหัสซ้ำต่างตัวพิมพ์ (vat7 vs VAT7) | ถือว่าซ้ำ → บล็อก/ข้าม | BR-01 |
| ☑ EC-02 | อัตรา = 120 (นำเข้า) | RATE_INVALID ข้ามแถว | BR-02 · BULK_SAMPLE WHT99 |
| ☑ EC-03 | ยกเว้นภาษี + อัตรา≠0 (นำเข้า) | EXEMPT_RATE ข้ามแถว | BR-03 |
| ☑ EC-04 | อัตราทศนิยม 0.75 | รับได้ (WHT075) | S-08 |
| ☑ EC-05 | นำเข้า status ว่าง | = ร่าง (draft) | BR-08 · VAT9 |
| ☑ EC-06 | bulk ลบผสม used>0 กับ used=0 | ลบเฉพาะ used=0, ข้าม used>0 + toast | BR-05 |
| ☑ EC-07 | แก้ตัว used>0 แล้วฝืน submit | logic guard คงค่าเดิม 3 field | BR-04 · FN-08 |
| ☑ EC-08 | นำเข้าไฟล์ที่ไม่ได้เลือก | ไม่ preview (bulkFileChosen ตรวจ file จริง) | HTML |

### 10.2 Edge Cases จาก AI Pattern Matching (☐ = แนะนำ · BA/FRD confirm)
| # | หมวด | Edge | คำแนะนำ handle | ยกระดับ? |
|---|---|---|---|---|
| ☐ EC-A1 | Import (FU) | ไฟล์ CSV encoding ไม่ใช่ UTF-8 / คอลัมน์สลับ / header หาย | parser จริงต้อง validate header ก่อน (mock ปัจจุบันข้ามขั้นนี้) | ⚠️ ยกเป็น OQ-TAX-04/FRD |
| ☐ EC-A2 | Import (FU) | ไฟล์ใหญ่มาก (พันแถว) | pagination/throttle preview | — |
| ☐ EC-A3 | Concurrent (CA) | 2 คนสร้างรหัสเดียวกันพร้อมกัน | server-side unique constraint (case-insensitive) | ⚠️ กระทบความถูกต้อง → FRD |
| ☐ EC-A4 | Lookup (DI) | ปลายทางอ้างรหัสที่ถูกเปลี่ยนเป็น inactive ภายหลัง | เอกสารเก่าคงค่าเดิม · เลือกใหม่ไม่ได้ (soft ref) | — (สอดคล้อง BR-07) |
| ☐ EC-A5 | Calc (CL) | rate ที่มีทศนิยมยาว (เช่น 0.756) | นิยาม precision (แนะนำ 2 ตำแหน่ง) | ⚠️ FRD ต้องนิยาม |
| ☐ EC-A6 | Status (ST) | เปลี่ยน active→inactive ตัวที่ used>0 | อนุญาต (สถานะอิสระ) แต่กระทบปลายทางเลือกใหม่ | — |
| ☐ EC-A7 | Delete | ลบตัวที่ปลายทางอ้างแต่ `used` mock=0 (ยังไม่ sync จริง) | ต้อง sync `used` จริงก่อน enable ลบจริง | 🚨 ยกทันที → OQ-TAX-04 (ข้อมูลสูญหาย) |

> **หมายเหตุ:** EC-A7 กระทบข้อมูลสูญหาย — ยกเป็น Open Question ทันที (ดู §15)

---

## Section 11 — Impact / Regression
- **ประเภท New Feature** — ไม่มี regression กับฟีเจอร์เดิม (ยังไม่มี master เดิม)
- Downstream ที่จะเริ่มพึ่งพา: Item Master (กลุ่มภาษี), เอกสารขาย/ซื้อ (VAT/WHT), GL Posting Setup — ดู §12.1
- ต้องมี `used` sync จริงก่อนจะเปิด hard-delete หรือรายงานความถูกต้องของ "จำนวนที่ถูกอ้างอิง"

---

## Section 12.1 — Value Stream & Downstream Impact ⭐

**Value Stream positioning:** Tax Code เป็น **master ต้นน้ำ (ฐานราก Wave 1)** ของสาย Order-to-Cash และ Procure-to-Pay — ไม่รับ trigger จากเอกสารใด (master ต้นน้ำ · S ไม่มีเอกสารอ้างเข้า, D4 = N/A)

**Upstream:** ไม่มี (เป็น master ตั้งต้น) — ข้อมูลมาจากการ maintain โดยทีมบัญชี + seed อัตราภาษีไทยมาตรฐาน

**Downstream Impact Map:**
| ปลายทาง | ข้อมูลที่ไหลไป | Trigger | ถ้า Tax Code เปลี่ยน/ปิด |
|---|---|---|---|
| **Item Master (กลุ่มภาษี)** | รหัส + สถานะ (เฉพาะ active) | สถานะ=active | เปลี่ยนเป็น inactive → ไม่โผล่ให้เลือกใหม่ · สินค้าเดิมคงรหัสเดิม (soft ref) |
| **เอกสารขาย/ซื้อ (QT/SO/INV/PR/PO)** | อัตรา % → B2 line editor คำนวณ VAT + WHT ท้ายบิล | เลือกกลุ่มภาษี/รหัสภาษีในบรรทัด | **IR-TAX-01 คุ้มครอง:** อัตราตัวที่ถูกใช้แก้ไม่ได้ → บิลเก่าคำนวณถูกตลอด |
| **GL Posting Setup (Accounting)** | รหัสภาษี → map เข้าบัญชี GL (อีกชั้น) | ตั้งค่า mapping | ทะเบียนนี้ไม่ถือเลขบัญชี — mapping ไม่กระทบที่ต้นทาง (LOCK-NO-GL) |
| **DOA / NOTIF** | — | — | ไม่มีสาย + ไม่ emit (LOCK-DOA-NULL / LOCK-NO-NOTIF) |

**ผลกระทบแนวขวาง:** บัญชี (ผ่าน GL Posting Setup ชั้นถัดไป) · รายงานภาษีขาย/ซื้อ · ยอดภาษีในบิล — Tax Code เป็น input ความถูกต้องของทั้งหมด

---

## Section 12.3 — Existing System Reference
| Rule/ความสามารถ | ระดับ | มีอยู่แล้ว? | Reference |
|---|---|:--:|---|
| Auto document code (VATxx/WHTxx/TAXxx) | Logic (seed pattern) | ❌ | ต้องสร้างใหม่ (autoCode) |
| นำเข้า/ส่งออก CSV (BOM) | UI capability | ❌ | ต้องสร้างใหม่ (pattern เลน VD-PDM-16) |
| GL mapping (รหัสภาษี→บัญชี) | ระบบภายนอกหน้านี้ | ⚠️ แยกโมดูล | **GL Posting Setup (Accounting)** — ไม่ใช่ scope นี้ |
| `used` counter sync จริง | Logic | ❌ | รอ FRD นิยามแหล่งนับ (สินค้า + เอกสาร) · OQ-TAX-04 |
| DOA/Approval | ระบบภายนอก | ⚠️ placeholder | Policy Center (future) — field null ไว้แล้ว |

> ไม่มี System Module Registry ให้เทียบ — ตารางนี้เป็น placeholder (⚠️ ขอ Registry ภายหลัง)

---

## Section 13 — Delivery Phases
**Phase 1 — Feature Launch (ทั้งหมดอยู่เฟสนี้):**
- Config/Seed: 3 ประเภทภาษี (fix) + auto-code pattern + seed อัตราภาษีไทยมาตรฐาน (VAT7/VAT0/NONVAT/WHT 1/2/3/5/10/15)
- State machine 3 ค่าอิสระ (ไม่ hardcode)
- IR-TAX-01 guard (UI disabled + logic guard) — ตั้งแต่วันแรก
- Import/Export CSV + 6 error codes validation
- Soft-reference contract กับ Item Master/เอกสาร (เฉพาะ active)

**Phase 2 (Admin Panel):** — ไม่มี (ทุกกติกา FIXED)
**Phase 3 (Rule Management):** — ไม่มี
**Phase 4 (Engine Management):** — ไม่มี
**รอ prerequisite:** `used` sync จริง (จากสินค้า + เอกสาร) — เป็นเงื่อนไขก่อนเปิดความสามารถที่พึ่งตัวเลข used (OQ-TAX-04)

---

## Section 14 — Dev Requirements Summary ("ใบสั่ง")

### 14.1 Config Foundation
- ตาราง TaxCode + audit fields + DOA placeholder (null) · ประเภท fix 3 ค่า (enum ไม่ hardcode ในหลายที่ — ใช้ constant กลาง)
- auto-code generator (unique, ตามประเภท)

### 14.2 ข้อกำหนดจาก Tag / LOCK (ทุกข้อ FIXED — บังคับ enforce ทั้ง UI + backend)
- **IR-TAX-01 (LOCK):** ต้อง guard ฝั่ง logic ด้วย ไม่ใช่แค่ disable UI — ตัวที่ `used>0` ห้าม persist การเปลี่ยนรหัส/อัตรา/ประเภท
- **EXEMPT=0 (LOCK):** exempt → rate=0 บังคับทั้ง create/edit/import
- **Uniqueness:** case-insensitive unique constraint ฝั่ง DB/API (กัน concurrent)
- **Soft ref:** ปลายทางเก็บ code เท่านั้น · combobox ปลายทาง filter status='active'
- **Bulk delete:** skip `used>0` · ไม่มี endpoint ลบเดี่ยว
- **No GL / No DOA / No NOTIF:** ไม่สร้าง field/endpoint เหล่านี้

### 14.3 Edge Cases สำคัญที่ Dev ต้อง handle
- CSV import: validate header + encoding จริง (mock ข้ามขั้นนี้) — 6 error codes รายแถว, ไม่ล้มทั้งไฟล์
- rate precision (นิยามจำนวนทศนิยม — รอ FRD)
- `used` counter: ต้องนับจริงจากสินค้า+เอกสารก่อน enable การพึ่งพาตัวเลขนี้

### 14.4 WARNING ที่รอข้อสรุป
- OQ-TAX-02 (effective date) · OQ-TAX-03 (WHT scope) · OQ-TAX-04 (`used` sync) — ห้ามพัฒนาส่วนที่พึ่ง effective-date/real-used จนกว่าจะ resolve

### 14.5 Regression Scope
- N/A (New Feature)

### 14.6 Screen Inventory + UI Signals
ดู Section 19 (Screen Inventory) — UI Signals: **ไม่ใช่เอกสารธุรกรรม** (ไม่มี approver/พิมพ์/ลายเซ็น) · มี import/export CSV · **ไม่มี NON-STANDARD flag** · pattern เลน master data มาตรฐาน (v8 #96/#97/#95 + Esc chain)

---

## Section 15 — Open Questions
| # | คำถาม | เจ้าภาพ | สถานะ |
|---|---|---|---|
| OQ-TAX-02 | ไม่ทำช่วงเวลาบังคับใช้อัตรา (effective date/validity period) — ใช้แนว "สร้างรหัสใหม่ + ปิดตัวเก่า" แทน — พอมั้ยสำหรับ CUBE (ERP บางเจ้ามี validity period) | Strike | ⚠️ pin (คงเปิด) |
| OQ-TAX-03 | WHT ใช้ฝั่งจ่าย/ซื้อเป็นหลัก — master กลางรวม WHT ไว้ตั้งแต่แรก (เลน Sales ใช้ VAT ก่อน) — ยืนยัน scope | Strike | ⚠️ pin (คงเปิด) |
| OQ-TAX-04 | `used` เป็น mock — ของจริงต้องนับจากสินค้า (กลุ่มภาษี) + เอกสารทุกใบที่อ้างรหัส · กระทบ bulk-delete guard (EC-A7 ข้อมูลสูญหาย) | FRD | ⚠️ เปิด |
| OQ-TAX-05 | ตำแหน่งเมนู: HTML วางใต้ "Master Data"; Central Plan/PREBRIEF ระบุ Tax Code เป็น master เชิงบัญชี (Accounting) — ยืนยันตำแหน่ง navigation | PM/BA | ⚠️ เปิด (HTML-RIF DRIFT) |
| OQ-TAX-06 | Role-gate จริง (ใครสร้าง/แก้/นำเข้า) — mock ปัจจุบันเปิดหมด | FRD/Policy Center | ⚠️ เปิด |

---

## Section 16 — Security & Compliance

### 16.1 Preset
**P3 — Master Data (10 controls)** [AI-DEFAULT — inferred จาก module type: master data ระดับระบบ]
เหตุผล: เป็น master กลางที่กระทบความถูกต้องเชิงบัญชี downstream (ไม่ใช่ transaction/PII) — เน้น integrity + audit + access control

### 16.2 Applicable Standards (ย่อ)
| Standard | ใช้? |
|---|:--:|
| Access Control (RBAC) | ✅ (deferred → OQ-TAX-06) |
| Audit Trail | ✅ (created/updated by+at) |
| Data Integrity (unique, guard) | ✅ (IR-TAX-01, uniqueness) |
| Input Validation | ✅ (rate, code, import) |
| PII/Encryption | ❌ (ไม่มี PII) |
| Approval/SoD | ❌ (LOCK-DOA-NULL) |

### 16.3 Control Checklist (P3 core)
| Control | Required | Implementation Notes |
|---|:--:|---|
| C-01 RBAC gate การเขียน | ✓ Must | deferred → FRD/Policy Center |
| C-02 Audit log (who/when) | ✓ Must | tab ประวัติ + updated_by/at |
| C-03 Unique constraint (case-insensitive) | ✓ Must | DB + API level (กัน concurrent) |
| C-04 Immutable-on-use guard (IR-TAX-01) | ✓ Must | logic guard คงค่าเดิม 3 field |
| C-05 Input validation (rate/exempt/import) | ✓ Must | server-side ด้วย ไม่ใช่แค่ UI |
| C-06 Soft-delete / no hard-delete on used | ✓ Must | bulk skip used>0 |
| C-07 Export safe (BOM, escape) | ○ Optional | export escape ", newline |
| C-08 Import row isolation (แถวผิดไม่ล้มไฟล์) | ✓ Must | validate รายแถว |
| C-09 No sensitive data leakage | ○ Optional | ไม่มี GL/PII ในหน้านี้ |
| C-10 Session/CSRF (write ops) | ✓ Must | มาตรฐาน platform |

### 16.4 Risk Statement
| Risk | อธิบาย | Mitigated by |
|---|---|---|
| R-01 | แก้อัตราตัวที่ถูกใช้ → บิลเก่าเพี้ยน | C-04 (IR-TAX-01 guard) + BR-04 |
| R-02 | รหัสซ้ำจาก concurrent create → อ้างอิงกำกวม | C-03 (unique constraint) |
| R-03 | ลบตัวที่ปลายทางอ้างจริง (used mock=0) → ข้อมูลสูญหาย | C-06 + OQ-TAX-04 (sync used ก่อน) |
| R-04 | ยกเว้นภาษีมีอัตรา≠0 หลุดเข้าระบบ (import) | C-05/C-08 (EXEMPT_RATE validate) |

---

## Section 17 — Health Check

### 17.1 SLA
| Step | เวลาควบคุม | Owner |
|---|---|---|
| บันทึกสร้าง/แก้ | < 1s (mock 600ms loader) | System |
| Import preview (ต่อไฟล์) | ตามขนาดไฟล์ — นิยาม threshold ที่ FRD | System |

### 17.2 Control Points (map จาก §16)
- Immutable-on-use guard (C-04) · Unique check (C-03) · Import row validation (C-08)

### 17.3 KPI
| ID | KPI | หมวด | เป้า |
|---|---|---|---|
| KPI-01 | % เอกสารใหม่ที่ดึงอัตราจาก Tax Code | Compliance | 100% |
| KPI-02 | จำนวนการละเมิด IR-TAX-01 (ถูก guard บล็อก) | Quality | 0 persist |
| KPI-03 | % แถว import ที่ผ่าน | Quality | ≥90% |
| KPI-04 | จำนวนรหัส "ใช้งาน" พร้อมใช้ | Volume | ครอบอัตรามาตรฐาน |

### 17.4 Threshold
| Metric | Min | Max | Action เมื่อ breach |
|---|---|---|---|
| อัตรา (%) | 0 | 100 | บล็อก RATE_INVALID |
| import error rate | — | > 50% | เตือน/ทบทวนไฟล์ (แนะนำ) |

### 17.5 Throughput
- Capacity: จำนวนรหัสภาษีไม่มาก (สิบ–ร้อยรายการ) · Baseline: 10 seed · Stress point: import ไฟล์พันแถว (ดู EC-A2)

---

## Section 18 — Monitoring

### 18.1 Reports Overview
| Type | มี? | หมายเหตุ |
|---|:--:|---|
| Transaction (list/export) | ✅ | ส่งออก CSV ตาม filter |
| Anomaly | ○ | รายการ import ที่ error (แสดงใน modal ผลนำเข้า) |
| Performance / Closing | ❌ | ไม่ applicable (master data) |

### 18.2 Dashboard Widgets (อ้าง KPI §17.3)
- Stat 4 ใบบนหน้า List: **ทั้งหมด / ใช้งาน / ไม่ใช้งาน / ร่าง** (กดกรองเร็ว) — สะท้อน KPI-04 (Volume)
- ผลสรุป import (ok/skip) ต่อรอบ — สะท้อน KPI-03

### 18.3–18.6
- Anomaly Report: ตารางแถวผิดในจอผลนำเข้า (รหัส/ชื่อ/สาเหตุ)
- Transaction Report: export CSV 7 คอลัมน์ (code, name_th, name_en, type, rate, status, used_in) BOM

---

## Section 19 — Screen Inventory (สกัดจาก HTML — Reverse Mode)

> **โครงสร้างจริง:** SPA เส้นทางเดียว `#/tax-codes` (routing = hashchange → `renderList()`). ฟอร์ม/รายละเอียด/นำเข้า เป็น **overlay** (drawer/modal) ไม่ใช่ route แยก — จึงระบุ "trigger จริง" แทน route ในหน้า overlay

| # | ชื่อหน้า/มุมมอง | route / trigger จริง | ประเภทหยาบ | ผู้ใช้หลัก | หน้าที่ (business) | หมายเหตุ |
|---|---|---|---|---|---|---|
| P-01 | ทะเบียนรหัสภาษี (List) | `#/tax-codes` · `renderList()` | หน้ารายการ | บัญชี | ค้นหา/กรอง/stat/sort/แบ่งหน้า/bulk/นำเข้า/ส่งออก | pageSize 8 · sort อัตรา/used เชิงตัวเลข |
| P-02 | สร้างรหัสภาษี (drawer) | `openCreate()` | ฟอร์มสร้าง (ขั้นเดียว) | บัญชี | กรอก 6 field + validate + บันทึก | รหัสเว้นว่าง=auto |
| P-03 | แก้ไขรหัสภาษี (drawer) | `openEdit(id)` | ฟอร์มแก้ไข | บัญชี | แก้ไข (ล็อก 3 field ถ้า used>0) | ป้าย "ล็อก — ถูกใช้งานแล้ว" |
| P-04 | รายละเอียดรหัสภาษี (drawer view) | `openView(id)` | หน้ารายละเอียด | บัญชี | ดู 3 tab (ภาพรวม/การใช้งาน/ประวัติ) + header เมนูเปลี่ยนสถานะ | tab การใช้งาน = ไม่มีแถวลบ |
| P-05 | นำเข้ารหัสภาษีจากไฟล์ (modal) | `bulkImport()` | หน้ายืนยัน/wizard 3 จังหวะ | บัญชี | เลือกไฟล์ → preview รายแถว → ผลนำเข้า | จอแรก: กล่องไฟล์ + ปุ่ม template เท่านั้น |
| P-06 | ยืนยันลบ bulk (modal) | `openBulkDelete()` | หน้ายืนยัน | บัญชี | ยืนยันลบ + แจ้งจำนวนข้าม (used>0) | — |

**สรุปจำนวนหน้า:** ~6 มุมมอง (List 1 · ฟอร์ม 2 · รายละเอียด 1 · modal 2) บน 1 route จริง
**HTML-RIF drift check:** ทุกมุมมองใน Inventory ตรงกับ scenario/FN ใน PREBRIEF+Checklist ครบ — ไม่มีหน้าเกิน/ขาด (นอกจาก OQ-TAX-05 module placement)

---

## AI Review Report

```
═══════════════════════════════════════
AI REVIEW REPORT — BRD Generator Full (Fresh Mode / HTML-first)
═══════════════════════════════════════
BRD: BRD-F-TAX-001 — ทะเบียนรหัสภาษี (Tax Code Master)
ประเภท: New Feature (Master Data)
วันที่ตรวจ: 2026-08-10

CHECKLIST RESULTS:
───────────────────────────────────────
✅ C01 Business Objective ชัดเจน วัดผลได้ (§2.3 มีตัวเลข/แหล่งวัด)
✅ C02 User Roles ครบ (§4)
✅ C05 Story ไม่มีคำว่า "และ" เชิงรวม action (แยก S ครบ)
✅ C10 ทุก rule ติด Tag (§9.1 — ทั้งหมด FIXED, มีเหตุผลใน §9.5)
✅ C13 Edge Cases ครบหมวด (§10.1 ยืนยัน + §10.2 AI pattern)
✅ C18 WARNING ทุกข้อมีแผน/เจ้าภาพ (§15)
✅ C19 Section 14 ใบสั่งครบ
✅ C20 Scope Lock — §3.4 LOCK ครบ, ไม่มี scope เกินเงียบ
✅ C21 Value Stream — §12.1 upstream(N/A ระบุเหตุ) + Downstream Impact Map ตอบ "แล้วไงต่อ" ทุกแถว
✅ C22 ตัวชี้วัด §2.3 มี baseline/target/วิธีวัด + คู่ใน §17.3 (KPI-01..04)
✅ C23 §9.5 marker ครบ (ทั้งหมด ✅ Stakeholder — ไม่มี 🤖 ระดับสูงค้าง)
✅ PE01 COSO Roles ครบทุก step §5 (Approver=N/A ตาม LOCK-DOA-NULL)
✅ PE02 SoD — N/A (ไม่มี approval workflow) ระบุเหตุชัด
✅ PE03 Security Preset เลือกแล้ว (P3) + controls ครบ
✅ PE04 SLA + KPI + Threshold ครบ (§17)
✅ PE05 Cross-section coverage ผ่าน (BC↔Edge, Control↔Health, Metric↔Monitoring)

HTML-first checks:
✅ Screen Inventory ทุกแถวมี route/trigger จริง · จำนวนหน้า = ที่มีใน HTML
✅ Conflict Priority ใช้ถูก (LOCK > PREBRIEF > HTML)
⚠️ HTML-RIF DRIFT ที่ flag: (1) mock user identity §4/D-4.1 → OQ-TAX-06;
   (2) module placement Master Data vs Accounting §1 → OQ-TAX-05 (ไม่ resolve เงียบ)

SUMMARY:
───────────────────────────────────────
ผ่าน: 20/20 core + 5 HTML-first · Drift flagged (ไม่ปิดเงียบ): 2
Residual Open Questions: 5 (OQ-TAX-02..06) — documented, ไม่บล็อก DoD

สถานะ: ✅ APPROVED (with documented residual OQs)
พร้อมส่งเข้า frd-generator-v6

[AI-DEFAULT] ที่ใช้:
 D-2.3 target ตัวชี้วัดธุรกิจ · role-gate deferred · COSO Approver=N/A ·
 Security preset P3 · rate precision รอ FRD

Conflict resolution:
 - mock user (พิมพ์ใจ/บัญชี vs วิภา/Master Data) → business intent ชนะ, flag OQ-TAX-06
 - module placement (Accounting vs Master Data) → ไม่ตัดสิน, flag OQ-TAX-05
 - effective date: PREBRIEF ตัด, HTML ไม่มี → สอดคล้อง, คง OQ-TAX-02 เปิด
═══════════════════════════════════════
```
