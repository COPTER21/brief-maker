# 06_TESTS — F-ACC-CN ใบลดหนี้ลูกค้า (Credit Note)

> **Audience:** QA engineer + ai-testcase-md-generator (SOW3.5)
> **Purpose:** Acceptance Criteria + Test Inventory + DoD + Cross-module + WebSocket
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + 22 FN (FUNCTION_CHECKLIST)
> **Expected text:** ยึด **ข้อความจริงบนจอ (verbatim จาก HTML)** ก่อน — ห้ามแต่งคำเอง (§6.10)

---

## §6.1 Acceptance Criteria (AC) — 1 ต่อ FN

### AC-01 (FN-01/03): เลือกใบแจ้งหนี้คงค้าง → ดึงข้อมูล
**Given** เจ้าหน้าที่ลูกหนี้ @ P-02 s1 **When** เลือกใบที่ outstanding>0 **Then** เห็นคอลัมน์ ยอดสุทธิ/ลดหนี้แล้ว/คงค้าง ต่อใบ **And** เลือกแล้ว s2 แสดงลูกค้า/ที่อยู่/เลขภาษี + บรรทัดถูกล็อกจากใบเดิม

### AC-02 (FN-05): RET → ต้องเลือกใบรับคืน
**Given** reason=รับคืนสินค้า **When** ไม่เลือกใบรับคืน **Then** field-error "เลือกใบรับคืนของใบแจ้งหนี้นี้" **And** เลือก SR → จำนวนบรรทัด = จำนวนจากใบรับคืน (line.max = SR qty)

### AC-06 (FN-06): DISC ราคาลด ≤ ราคาเดิม
**Given** reason=ส่วนลดภายหลัง (mode price) **When** กรอก unit_price > orig_price **Then** meta "— ราคาลดเกินราคาเดิม" + block "ราคาลดต่อหน่วยเกินราคาเดิม: {item}"

### AC-07 (FN-07): PRICE/QTY ลดเฉพาะบรรทัด · ลบ/เพิ่มบรรทัดกลับ
**Given** ใบมีหลายบรรทัด **When** ลบบรรทัด → เห็น chip "บรรทัดจากใบเดิมที่ไม่ได้ลด" readd ได้ **Then** ลดเฉพาะบรรทัดที่เลือก

### AC-08 (FN-08): ลดหลายรอบ — meta ถูกต้อง
**Given** ใบมี CN อนุมัติแล้ว 1 ใบ (ลดแล้ว) **When** สร้างใบใหม่อ้างใบเดิม **Then** meta "ใบเดิม N × ฿P · ลดแล้ว ฿X · ลดจำนวนได้อีก M · ลดมูลค่าได้อีก ฿Y" ถูกต้อง (cn_applied+cn_held)

### AC-09 (FN-09): ยอด/จำนวนเกิน → บล็อก + บอกยอด
**Given** draft grand > available **When** ดูสรุป/กดส่งอนุมัติ **Then** hard-warn "ยอดลดหนี้เกินยอดคงเหลือของใบแจ้งหนี้อ้างอิง — ลดได้ ฿X · ใบนี้ ฿Y · เกิน ฿Z" **And** submit ถูกบล็อก (บันทึกร่างได้)

### AC-10 (FN-10): คำอธิบาย ≥10
**When** reason_text < 10 ตัว **Then** field-error "ระบุคำอธิบายอย่างน้อย 10 ตัวอักษร" + block

### ⭐ AC-19 (FN-19 · BR-11/BR-12): ส่วนลดท้ายบิล
**Given** s3 มีบรรทัดยอด after=X **When** เปิด toggle ส่วนลดท้ายบิล
- (a) กรอก ≤ ebCap → summary แสดง "ส่วนลดท้ายบิล · ลดฐานภาษี -฿ebBase", "ฐานภาษีหลังหักส่วนลด ฿netBefore", "ภาษีมูลค่าเพิ่ม (VAT) · คิดจากฐานใหม่ (ม.86/10) +฿netVat", grand ลดลง
- (b) กรอก > ebCap → hard-warn "ส่วนลดท้ายบิลเกินยอดที่ลดได้ — สูงสุด ฿X · ที่กรอก ฿Y ..." + **block submit** ("ยอดสุทธิห้ามติดลบ")
- (c) DOA tier คิดจาก grand หลังหักส่วนลด (ดู AC-11) **And** ภ.พ.30/JE/PDF ใช้ netVat (ตรง ref tab)
**Expected calc (verbatim ENG cn-totals):** ebVat = ebAmt×(vat/after) · netBefore = before − (ebAmt − ebVat) · netVat = vat − ebVat · grand = max(0, after − ebAmt)

### AC-11 (FN-11): ส่งอนุมัติ — สายตามมูลค่า + เลือกคนครบ
**Given** grand ในช่วง tier X **When** เปิด submit modal **Then** สายอนุมัติ = ตาม tier (1: ผจก.ขาย · 2: +ผจก.บัญชี · 3: +CFO) **And** ไม่เลือกครบ → "เลือกผู้อนุมัติให้ครบทุกขั้น" · เลือกครบ → pending_approval (chain freeze)

### AC-12 (FN-12): อนุมัติครบสาย → เลข CN
**Given** pending ขั้นสุดท้าย **When** อนุมัติ **Then** toast "อนุมัติครบสาย — ออกใบลดหนี้ CN-YYYY-NNNN · ลดยอดคงค้าง {inv}" **And** status "อนุมัติแล้ว · รอส่ง" + code ออก (no-gap)

### AC-13 (FN-13/04): ไม่อนุมัติ + ใบ void/ชำระครบ
- (reject) pending → "ไม่อนุมัติ" + เหตุผล → draft + badge "ถูกตีกลับ N ครั้ง" + ประวัติรอบก่อน (append-only)
- (picker) ใบ void/ชำระครบ ไม่โผล่ใน P-02 s1

### AC-14 (FN-02/14): ลดลอยปิด + SoD
- (FN-02) คลิก tile "ลดหนี้ไม่อ้างใบ" → toast "ลดหนี้ไม่อ้างใบแจ้งหนี้ถูกปิดไว้ (OQ-CN-01)" · tile disabled
- (FN-14 SoD) ผู้ส่ง login → เปิดใบตัวเองตอน pending → **ไม่มีปุ่ม "อนุมัติ"** (เห็นแค่ "ยกเลิก")

### AC-15 (FN-15): ยกเลิก draft/pending + เหตุผล → cancelled + คืนยอด held
### AC-16 (FN-16): ส่งลูกค้า → "ส่งลูกค้าแล้ว" · sent → "ส่งสำเนาซ้ำ" (ไม่เปลี่ยนวันที่ส่งเดิม)
### AC-17 (FN-17 · BR-02): re-check ตอนอนุมัติขั้นสุดท้าย
**Given** pending · outstanding ลดลง (demoPay/RV) จนไม่พอ **When** อนุมัติขั้นสุดท้าย **Then** block "อนุมัติไม่ได้ — ยอดคงค้าง {inv} เหลือ ฿X น้อยกว่ายอดลดหนี้ ... ให้ไม่อนุมัติกลับไปแก้"
### AC-18 (FN-18): ref tab — คงค้างก่อน/หลัง + ภาษีขายที่ลด + JE
**Then** แสดง ยอดสุทธิใบเดิม/รับชำระ/ลดแล้ว/คงค้างก่อน/**คงค้างหลังใบนี้** · ผลกระทบภาษีขาย (เดือน cnDate/ฐาน/netVat) · JE (Dr 4110-4120 netBefore · Dr 2150 netVat · Cr 1130 grand) เฉพาะ approved/sent
### AC-90 (FN-90): ค้นหา/กรอง สถานะ/เหตุผล/ลูกค้า + empty · stat 4 tile คลิก filter · CSV
### AC-91 (FN-91): ประวัติ append-only ทุกการกระทำ (ไม่มีลบ)
### AC-92 (FN-92): PDF อ้างเลข/วันที่ใบเดิม · มูลค่าเดิม/ถูกต้อง/ผลต่าง/ภาษี · เหตุผล(+legal_basis) · ค.ศ.

---

## §6.2 Test Case Inventory

> **หมายเหตุ (R15 count-sync):** ตารางนี้คือ **core inventory** (1 TC ต่อ AC หลัก, ~26 เคส). ไฟล์ `testcases-F-ACC-CN.md` คือ **full expansion = 88 เคส · 13 group** ที่แตกย่อยเพิ่ม (TC-19d/e/f/g, TC-11d/e, TC-P0x, TC-X0x, TC-GRD-0x, TC-NEG-0x, TC-LK-0x). ทุก FN ยังครอบครบทั้งสองระดับ — จำนวนจริงที่ dev/QA ใช้ = 88 ในไฟล์ testcases.


| TC ID | Name | Type | Maps to | Priority |
|---|---|---|---|---|
| TC-01 | สร้าง CN RET (happy S-01) | E2E | AC-01,02,11,12 | P0 |
| TC-06 | DISC ราคาลด ≤ เดิม | UI/negative | AC-06 | P1 |
| TC-07 | PRICE/QTY ลบ/readd บรรทัด | UI | AC-07 | P1 |
| TC-08 | ลดหลายรอบ meta | UI | AC-08 | P0 |
| TC-09 | ยอดเกินคงเหลือ block | negative | AC-09 | P0 |
| TC-10 | reason_text <10 block | negative | AC-10 | P1 |
| **TC-19a** | **end-bill ลด VAT ถูกต้อง (BR-12)** | UI/calc | AC-19(a) | **P0** |
| **TC-19b** | **end-bill เกิน cap block (BR-11)** | negative | AC-19(b) | **P0** |
| **TC-19c** | **DOA tier คิดจาก grand หลัง end-bill (LD-05)** | E2E | AC-19(c),AC-11 | **P0** |
| TC-11 | slot picker ครบ/ไม่ครบ | UI | AC-11 | P0 |
| TC-12 | อนุมัติครบสาย → เลข CN no-gap | E2E | AC-12 | P0 |
| TC-13 | reject → draft + history | E2E | AC-13 | P1 |
| TC-14a | tile ลดลอยปิด | UI/negative | AC-14 | P1 |
| TC-14b | SoD ผู้ส่งไม่เห็นปุ่มอนุมัติ | E2E/permission | AC-14 | P0 |
| TC-15 | cancel + คืน held | E2E | AC-15 | P1 |
| TC-16 | send + resend | E2E | AC-16 | P1 |
| TC-17 | re-check outstanding block (S-11) | E2E | AC-17 | P0 |
| TC-18 | ref tab คงค้าง/VAT/JE | UI | AC-18 | P1 |
| TC-13c | ใบ void/ชำระครบ ไม่โผล่ | negative | AC-13 | P1 |
| TC-90 | search/filter/stat/CSV/empty | UI | AC-90 | P1 |
| TC-91 | audit append-only | E2E | AC-91 | P1 |
| TC-92 | PDF ครบตาม ม.86/10 | UI | AC-92 | P1 |
| TC-CC-01 | concurrent approval → 409 | stress | EC-CC-01 | P2 |
| TC-ID-01 | idempotency double-submit | API | EC-ID-01 | P1 |

> **e2e step-5 (runtime) note:** e2e ต้องครอบทุก FN + ทดสอบ negatives (FN-02 tile ปิด · FN-14 SoD ไม่มีปุ่ม · no hard delete) แบบ render จริง. feature นี้ **ไม่มี FN-40 เดี่ยว** — negatives = TC-14a/TC-14b/TC-91.

---

## §6.3 Test Data Setup (จาก HTML mock — พิสูจน์ scenario)
- INV-2026-0140 (10 กล่อง, CN-0021 ลดแล้ว 1) + SR-2026-0016 (2 กล่อง) → S-01/S-04
- INV-2026-0137 (บริการ) → S-02 · INV-2026-0135 → S-03
- INV-2026-0141 (770,400) + SR-2026-0014 → tier 2/3 DOA
- INV-2026-0136 ชำระครบ · INV-2026-0143 void → S-13 ไม่โผล่
- Personas (DEMO): วราภรณ์ (officer-ar) · มานพ (mgr-sales) · ประเสริฐ (mgr-acc) · อรุณี (cfo)

---

## §6.4 Definition of Done (DoD)
**Code:** ทุก AC implemented + unit tests · integration (API+DB+engine) · E2E happy+edge · review · security (D5/D7/D9) · coverage ≥80% logic
**Docs:** API docs (จาก 02_API) · FRD 07_LOCKED final · CUBIC register ENG cn-totals + ar-open-item · DOA entry DOA-ACC-CN + doc_type CN registered
**QA:** P0+P1 pass · ไม่มี P0/P1 bug · **e2e ครอบ 22/22 FN + negatives**
**Deploy:** migration tested · **DEMO artifacts stripped** (persona switcher · demoPay · .demo-only) · monitoring (stat tiles/netVat)

---

## §6.5 WebSocket / Notification Events (จาก NTF_BRIEF)
| Event | Trigger | Channel | Test |
|---|---|---|---|
| ar_cn_approved_applied | approve last | officer-ar + sales-rep (in-app) | maker/rep เห็น toast + คงค้างใหม่ |
| ar_cn_sent | approved→sent | customer (ตาม preference, แนบ PDF) | ลูกค้าได้ PDF |
| ar_cn_cancelled | →cancelled | ผู้สร้าง (in-app) | ผู้สร้างได้แจ้ง |
> doa_pending/doa_result = DOA engine — ไม่ test ในนี้ (external).

---

## §6.6 Performance
| Endpoint | P95 |
|---|---|
| GET list | <3s (RIF §12) |
| GET detail | <500ms |
| POST submit/approve | <1s |

---

## §6.8 Trace: AC → Logic Coverage
| AC | API | Functions | Engines |
|---|---|---|---|
| AC-01 | API-11,02 | FN-01,03 | ar-open-item |
| AC-02 | API-03 | FN-05 | ar-open-item (SR) |
| AC-06 | API-04 | FN-06 | cn-totals |
| AC-07 | API-04 | FN-07 | cn-totals |
| AC-08 | API-02,04 | FN-08 | cn-totals,ar-open-item |
| AC-09 | API-04 | FN-09 | cn-totals,ar-open-item |
| AC-10 | API-04 | FN-10 | — |
| AC-19 | API-03/04 | FN-19 | **cn-totals** |
| AC-11 | API-05 | FN-11 | ENG-DOA,cn-totals |
| AC-12 | API-06 | FN-12 | DOC-NUM,cn-totals,ar-open-item |
| AC-13 | API-07 | FN-13,04 | — |
| AC-14 | API-05 | FN-02,14 | ENG-DOA (SoD) |
| AC-15 | API-08 | FN-15 | ar-open-item |
| AC-16 | API-09 | FN-16 | DOC-STORE |
| AC-17 | API-06 | FN-17 | cn-totals,ar-open-item |
| AC-18 | API-02 | FN-18 | cn-totals |
| AC-90 | API-01,10 | FN-90 | — |
| AC-91 | API-12 | FN-91 | — |
| AC-92 | API-13 | FN-92 | cn-totals,DOC-STORE |
> ทุก FN-01..19 + FN-90/91/92 + ENG cn-totals/ar-open-item/DOC-NUM/DOC-STORE/ENG-DOA ถูก trace ≥1 AC. ✅

---

## §6.9 Cross-Module Test Cases ⭐ (BRD §12.1 Downstream — R12)
| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | อนุมัติ CN ครบสาย | AR ar_open_item (F094) | cn_applied += grand → outstanding ลด (ปิดเมื่อ=0) — ref tab "คงค้างหลังใบนี้" ตรง |
| XT-02 | อนุมัติ CN | VAT Report ภ.พ.30 (F105) | output_vat_line negative = netVat เดือน cnDate (ม.82/10) |
| XT-03 | อนุมัติ CN | Journal Entry (F093 mock) | Dr 4110/4120 netBefore · Dr 2150 netVat · Cr 1130 grand |
| XT-04 | **ยกเลิก CN (draft/pending)** | AR ar_open_item | held คืน → available เพิ่มกลับ |
| XT-05 | ยกเลิกหลังอนุมัติ (ไม่รองรับ) | — | ปุ่ม "ออกเอกสารแก้ไข" (display-only, ไม่ถอนยอด) — OQ-CN-02 |
| XT-06 | RET reason | Sales Return (F090 mock) | SR ของใบเดียวกัน · จำนวน ≤ ที่รับคืน |

---

## §6.10 Microcopy-Aware Expected Text (verbatim จาก HTML — ห้ามแต่งเอง)
- toast บันทึกร่าง: "บันทึกแบบร่างใบลดหนี้เรียบร้อย"
- toast อนุมัติครบ: "อนุมัติครบสาย — ออกใบลดหนี้ {code} · ลดยอดคงค้าง {inv}"
- toast ส่งอนุมัติ: "ส่งเพื่ออนุมัติแล้ว — My Approval ของ {ชื่อ}"
- toast อนุมัติขั้นกลาง: "อนุมัติขั้น {n} แล้ว — ส่งต่อ {ชื่อ}"
- toast ตีกลับ: "ตีกลับเพื่อแก้ไข" · ยกเลิก: "ยกเลิกเรียบร้อย"
- toast ส่งลูกค้า: "ส่ง {code} ให้ลูกค้าแล้ว" · resend: "ส่งสำเนา {code} ซ้ำแล้ว"
- toast ลดลอยปิด: "ลดหนี้ไม่อ้างใบแจ้งหนี้ถูกปิดไว้ (OQ-CN-01)"
- ปุ่ม wizard: "บันทึกแบบร่าง" · "บันทึกและส่งอนุมัติ" · "ถัดไป"/"ย้อนกลับ"
- ปุ่ม view: "ยกเลิก" · "แก้ไข" · "ส่งอนุมัติ" · "ไม่อนุมัติ" · "อนุมัติ" · "ส่งให้ลูกค้า" · "ส่งสำเนาซ้ำ" · "ออกเอกสารแก้ไข"
- tab: "รายละเอียด" · "ใบแจ้งหนี้อ้างอิง · ภาษีขาย" · "PDF Preview" · "ลายเซ็น · อนุมัติ" · "ประวัติ"
- summary rows: "ราคาก่อน VAT" · "ส่วนลดท้ายบิล · ลดฐานภาษี" · "ฐานภาษีหลังหักส่วนลด" · "ภาษีมูลค่าเพิ่ม (VAT) · คิดจากฐานใหม่ (ม.86/10)" · "ยอดสุทธิทั้งหมด"
> ผลลัพธ์: testcase จาก ai-testcase-md-generator จะ match จอ 1:1.
