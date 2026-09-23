# 06_TESTS — F-ACC-DN ใบลดหนี้ผู้ขาย (Debit Note)

> **Audience:** QA engineer + ai-testcase-md-generator (SOW3.5)
> **Purpose:** Acceptance Criteria + Test Inventory + DoD + Cross-module + WebSocket
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + **24 FN** (FUNCTION_CHECKLIST)
> **Expected text:** ยึด **ข้อความจริงบนจอ (verbatim จาก HTML)** ก่อน — ห้ามแต่งคำเอง (§6.10)

---

## §6.1 Acceptance Criteria (AC) — 1 ต่อ FN

### AC-01 (FN-01/03): เลือกใบตั้งหนี้คงค้าง → ดึงข้อมูล
**Given** เจ้าหน้าที่เจ้าหนี้ @ P-02 s1 **When** เลือกใบที่ dnRoom>0 **Then** เห็นคอลัมน์ ยอดสุทธิ/จ่ายแล้ว/ลดหนี้แล้ว/คงค้าง ต่อใบ **And** เลือกแล้ว s2 แสดงผู้ขาย/ที่อยู่/เลขภาษี/เลขใบกำกับเดิม (vinv) + บรรทัดถูกล็อกจากใบเดิม

### AC-02 (FN-05): RTV → ต้องเลือกใบคืนสินค้า
**Given** reason=คืนสินค้า (RTV) **When** ไม่เลือกใบคืนสินค้า **Then** field-error "เลือกใบคืนสินค้าของใบตั้งหนี้นี้" / block "เหตุผลคืนสินค้าต้องอ้างใบคืนสินค้า" **And** เลือก RTV → จำนวนบรรทัด = จำนวนจากใบคืนสินค้า (line.max = RTV qty)

### AC-06 (FN-06): OVERPRICE ราคาลด ≤ ราคาเดิม
**Given** reason=ผู้ขายคิดราคาเกิน (mode price) **When** กรอก unit_price > orig_price **Then** meta "— ราคาลดเกินราคาเดิม" + block "ราคาลดต่อหน่วยเกินราคาเดิม: {item}"

### AC-07 (FN-07): SHORT ลดเฉพาะบรรทัด · ลบ/เพิ่มบรรทัดกลับ
**Given** ใบมีหลายบรรทัด **When** ลบบรรทัด → เห็น chip readd ได้ **Then** ลดเฉพาะบรรทัดที่เลือก

### AC-08 (FN-08): ลดหลายรอบ — meta ถูกต้อง
**Given** ใบมี DN อนุมัติแล้ว 1 ใบ (ลดแล้ว) **When** สร้างใบใหม่อ้างใบเดิม **Then** meta "ใบเดิม N × ฿P · ลดแล้ว ฿X · ลดจำนวนได้อีก M · ลดมูลค่าได้อีก ฿Y" ถูกต้อง (dn_applied+dn_held)

### AC-09 (FN-09): ยอด/จำนวนเกิน → บล็อก + บอกยอด
**Given** draft grand > dnRoom **When** ดูสรุป/กดส่งอนุมัติ **Then** hard-warn/blockReason "ยอดลดหนี้เกินมูลค่าที่ลดได้ (บันทึกร่างได้)" + submit block "ยอดลดหนี้เกินมูลค่าที่ลดได้ของใบตั้งหนี้ (ลดได้ ฿X) — แก้ไขร่างก่อน" **And** บันทึกร่างได้

### AC-10 (FN-10): คำอธิบาย ≥10
**When** reason_text < 10 ตัว **Then** field-error/block "ระบุคำอธิบายเหตุผลอย่างน้อย 10 ตัวอักษร"

### ⭐ AC-19 (FN-19 · BR-11/BR-12): ส่วนลดท้ายบิล
**Given** s3 มีบรรทัดยอด after=X **When** เปิด toggle ส่วนลดท้ายบิล
- (a) กรอก ≤ ebCap → summary แสดง "ยอดลดก่อน VAT ฿netBefore", "ภาษีซื้อที่ลด · คิดจากฐานใหม่ (ม.86/10) ฿netVat", grand ลดลง
- (b) กรอก > ebCap → hard-warn "ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿X)" + helper "ลดได้สูงสุด ฿X" + **block submit**
- (c) DOA tier คิดจาก grand หลังหักส่วนลด (ดู AC-11) **And** ภ.พ.30/JE/PDF ใช้ netVat (ตรง ref tab)
**Expected calc (verbatim ENG dn-totals):** ebVat = ebAmt×(vat/after) · netBefore = before − (ebAmt − ebVat) · netVat = vat − ebVat · grand = max(0, after − ebAmt)

### ⭐ AC-20 (FN-04/FN-20 · BR-13): เครดิตคงเหลือกับผู้ขาย
**Given** ใบตั้งหนี้ **จ่ายครบแล้ว** (paid=grand · เช่น API-2026-0038) **When** สร้าง DN คืนของ (grand > outstanding)
- (1) ใบยังโผล่ใน picker (dnRoom ไม่หัก paid) · (2) อนุมัติครบ → `applyToAp = min(grand, outstanding)` · `vendorCredit = grand − applyToAp > 0`
- (3) audit "หักหนี้ค้าง ฿Y · เครดิตคงเหลือกับผู้ขาย ฿Z" · (4) P-01 KPI card + modal รายผู้ขาย แสดง credit_balance · ref tab แยกยอด
**And** ใบที่ dnRoom=0 (ลดเต็มแล้ว) ไม่โผล่ใน picker

### ⭐ AC-21 (FN-21 · BR-14): ภาษีซื้อกลับตาม vendorCn
**Given** DN approved (ยังไม่กรอก vendorCn) **When** เปิด ref tab
- (1) note.warn "รอใบลดหนี้ผู้ขาย" (read-only) · input VAT ยังไม่ลง ภ.พ.30
- (2) กด "บันทึกใบลดหนี้ผู้ขาย" (openVendorCn) → กรอก vendorCn + วันที่ (API-16) → input_vat_line ลง ภ.พ.30 **เดือน = vendorCnDate** (ม.82/10)
- (3) audit "บันทึกใบลดหนี้ผู้ขาย {vendor_cn} ({vendor_cn_date})"

### AC-11 (FN-11): ส่งอนุมัติ — สายตามมูลค่า + เลือกคนครบ
**Given** grand ในช่วง tier X **When** เปิด submit modal **Then** สายอนุมัติ = ตาม tier (1: ผจก.จัดซื้อ · 2: +ผจก.บัญชี · 3: +CFO) **And** ไม่เลือกครบ → "เลือกผู้อนุมัติให้ครบทุกขั้น" · เลือกครบ → pending_approval (chain freeze)

### AC-12 (FN-12): อนุมัติครบสาย → เลข DN
**Given** pending ขั้นสุดท้าย **When** อนุมัติ **Then** toast "อนุมัติครบสาย — ออกใบลดหนี้ {code} · ลดยอดคงค้าง {inv}" **And** status "อนุมัติแล้ว · รอส่ง" + code ออก (DN-YYYY-NNNN no-gap)

### AC-13 (FN-13/04): ไม่อนุมัติ + ใบที่ลดเต็มแล้ว
- (reject) pending → "ไม่อนุมัติ" + เหตุผล → draft + badge "ถูกตีกลับ N ครั้ง" + ประวัติรอบก่อน (append-only)
- (picker) ใบที่ dnRoom=0 ไม่โผล่ใน P-02 s1

### AC-14 (FN-02/14): ลดลอยปิด + SoD
- (FN-02) คลิก tile "ลดหนี้ไม่อ้างใบ" → toast (ปิดไว้) · tile disabled `not-allowed` · ไม่ผูก setSource
- (FN-14 SoD) ผู้ส่ง login → เปิดใบตัวเองตอน pending → **ไม่มีปุ่ม "อนุมัติ"** (เห็นแค่ "ยกเลิก")

### AC-15 (FN-15): ยกเลิก draft/pending + เหตุผล → cancelled + คืนยอด held
### AC-16 (FN-16): ส่งผู้ขาย → "ส่งผู้ขายแล้ว" · sent → "ส่งสำเนาซ้ำ" (ไม่เปลี่ยนวันที่ส่งเดิม)
### AC-17 (FN-17 · BR-02/BR-13): re-check ตอนอนุมัติขั้นสุดท้าย
**Given** pending · dnRoom ลดลง (ใบอื่น approved / demoPay) จนไม่พอ **When** อนุมัติขั้นสุดท้าย **Then** block "อนุมัติไม่ได้ — มูลค่าที่ลดได้ของ {inv} เหลือ ฿Y น้อยกว่ายอดลดหนี้ ... ให้ไม่อนุมัติกลับไปแก้"
### AC-18 (FN-18): ref tab — คงค้างก่อน/หลัง + ภาษีซื้อที่ลด + JE
**Then** แสดง ยอดสุทธิใบเดิม/จ่ายแล้ว/ลดแล้ว/คงค้างก่อน/**คงค้างหลังใบนี้** · แยก applyToAp/vendorCredit · ผลกระทบภาษีซื้อ (input_vat_line ติดลบ = netVat) · JE (Dr 2110 applyToAp · Cr 5xxx netBefore · Cr 1150 netVat) เฉพาะ approved/sent
### AC-90 (FN-90): ค้นหา/กรอง สถานะ/เหตุผล/ผู้ขาย + empty ("ไม่พบรายการ") · stat 4 tile คลิก filter · CSV "ส่งออก CSV {n} รายการ"
### AC-91 (FN-91): ประวัติ append-only ทุกการกระทำ (ไม่มีลบ · pushAudit unshift-only)
### AC-92 (FN-92): PDF อ้างเลข/วันที่ใบกำกับเดิม · มูลค่าเดิม/ถูกต้อง/ผลต่าง/ภาษีซื้อ · เหตุผล(+legal_basis) · ค.ศ. · 3 ช่องเซ็น

---

## §6.2 Test Case Inventory

> **หมายเหตุ (R15 count-sync):** ตารางนี้คือ **core inventory** (1 TC ต่อ AC หลัก). ไฟล์ `testcases-F-ACC-DN.md` (SOW3.5) จะ **แตกย่อยเพิ่ม** เป็น full expansion. ทุก FN (24) ครอบครบทั้งสองระดับ. e2e step-5 = 36/36 (E01..E36 incl. E20 vendor credit · E21 vendorCn).

| TC ID | Name | Type | Maps to | Priority |
|---|---|---|---|---|
| TC-01 | สร้าง DN RTV (happy S-01) | E2E | AC-01,02,11,12 | P0 |
| TC-06 | OVERPRICE ราคาลด ≤ เดิม | UI/negative | AC-06 | P1 |
| TC-07 | SHORT ลบ/readd บรรทัด | UI | AC-07 | P1 |
| TC-08 | ลดหลายรอบ meta | UI | AC-08 | P0 |
| TC-09 | ยอดเกิน dnRoom block | negative | AC-09 | P0 |
| TC-10 | reason_text <10 block | negative | AC-10 | P1 |
| **TC-19a** | **end-bill ลด input VAT ถูกต้อง (BR-12)** | UI/calc | AC-19(a) | **P0** |
| **TC-19b** | **end-bill เกิน cap block (BR-11)** | negative | AC-19(b) | **P0** |
| **TC-19c** | **DOA tier คิดจาก grand หลัง end-bill (LD-05)** | E2E | AC-19(c),AC-11 | **P0** |
| **TC-20a** | **ใบจ่ายครบยังออก DN ได้ → vendorCredit (BR-13)** | E2E | AC-20 | **P0** |
| **TC-20b** | **vendor credit ledger card/modal (FN-20)** | UI | AC-20 | P1 |
| **TC-21a** | **DN approved ไม่มี vendorCn → "รอเอกสาร" (BR-14)** | UI | AC-21(1) | **P0** |
| **TC-21b** | **บันทึก vendorCn → input VAT เดือน vendorCnDate (ม.82/10)** | E2E | AC-21(2,3) | **P0** |
| TC-11 | slot picker ครบ/ไม่ครบ | UI | AC-11 | P0 |
| TC-12 | อนุมัติครบสาย → เลข DN no-gap | E2E | AC-12 | P0 |
| TC-13 | reject → draft + history | E2E | AC-13 | P1 |
| TC-14a | tile ลดลอยปิด | UI/negative | AC-14 | P1 |
| TC-14b | SoD ผู้ส่งไม่เห็นปุ่มอนุมัติ | E2E/permission | AC-14 | P0 |
| TC-15 | cancel + คืน held | E2E | AC-15 | P1 |
| TC-16 | send + resend | E2E | AC-16 | P1 |
| TC-17 | re-check dnRoom block (S-11) | E2E | AC-17 | P0 |
| TC-18 | ref tab คงค้าง/VAT/JE + split | UI | AC-18 | P1 |
| TC-13c | ใบลดเต็มแล้วไม่โผล่ | negative | AC-13 | P1 |
| TC-90 | search/filter/stat/CSV/empty | UI | AC-90 | P1 |
| TC-91 | audit append-only | E2E | AC-91 | P1 |
| TC-92 | PDF ครบตาม ม.86/10 | UI | AC-92 | P1 |
| TC-CC-01 | concurrent approval → 409 | stress | EC-CC-01 | P2 |
| TC-ID-01 | idempotency double-submit | API | EC-ID-01 | P1 |
| TC-CA-01 | vendorCn ซ้ำ/เดือนปิดงวด (OQ) | edge | EC-CA-01 | P2 |

> **e2e step-5 (runtime) note:** e2e ต้องครอบทุก FN (24) + ทดสอบ negatives (FN-02 tile ปิด · FN-14 SoD ไม่มีปุ่ม · no hard delete · no refund · no RTV CRUD) แบบ render จริง. feature นี้ **ไม่มี FN-40 เดี่ยว** — negatives = TC-14a/TC-14b/TC-91 + หมวด "สิ่งที่ไม่รองรับ" (E36). ปัจจุบัน e2e ผ่าน 36/36 (coverage R1).

---

## §6.3 Test Data Setup (จาก HTML mock — พิสูจน์ scenario)
- API-2026-0041 (จ่ายบางส่วน · DN-0011 คืน 1 เครื่อง · ร่างคืน 2 กล่อง) + RTV-2026-0007/0010 → S-01/S-04
- API-2026-0043 (ราคา 4,100) → S-02/S-07 (draft ตีกลับ 1 ใบ)
- API-2026-0046 (60 ใบ · 526,440) · DN รอ ขั้น 1 (tier 2) + รอ ขั้น 2 (tier 3) + RTV-2026-0009 → S-03/S-06/S-11
- **API-2026-0038 จ่ายครบ** → S-13 (ยังออก DN ได้ → vendorCredit)
- API-2026-0044 (cancelled)
- DN 8 ใบ: sent ×2 · approved · pending ×2 · draft ×2 (1 ตีกลับ) · cancelled → list/stat/sign
- Personas (DEMO): สุภาพร เจ้าหนี้ดี (officer-ap) · สมศักดิ์ จัดซื้อ (mgr-purchase) · (mgr-acc) · (cfo)

---

## §6.4 Definition of Done (DoD)
**Code:** ทุก AC implemented + unit tests · integration (API+DB+engine) · E2E happy+edge · review · security (D5/D7/D9) · coverage ≥80% logic
**Docs:** API docs (จาก 02_API) · FRD 07_LOCKED final · CUBIC register ENG dn-totals + ap-open-item · DOA entry DOA-ACC-DN + doc_type DN registered
**QA:** P0+P1 pass · ไม่มี P0/P1 bug · **e2e ครอบ 24/24 FN + negatives (ปัจจุบัน 36/36)**
**Deploy:** migration tested · **DEMO artifacts stripped** (persona switcher · demoPay · .demo-only) · monitoring (stat tiles/netVat/credit ledger)

---

## §6.5 WebSocket / Notification Events (จาก NTF_BRIEF)
| Event | Trigger | Channel | Test |
|---|---|---|---|
| dn.issued | approve last | officer-ap + AP (in-app) | maker เห็น toast + คงค้างใหม่ |
| dn.sent | approved→sent | vendor (ตาม preference, แนบ PDF) | ผู้ขายได้ PDF |
| dn.cancelled | →cancelled | ผู้สร้าง (in-app) | ผู้สร้างได้แจ้ง |
> doa_pending/doa_result = DOA engine — ไม่ test ในนี้ (external). dn.vat_applied (CSQ, เมื่อ vendorCn) = OQ-DN-07.

---

## §6.6 Performance
| Endpoint | P95 |
|---|---|
| GET list | <3s (BRD §17) |
| GET detail | <500ms |
| POST submit/approve | <1s |

---

## §6.8 Trace: AC → Logic Coverage
| AC | API | Functions | Engines |
|---|---|---|---|
| AC-01 | API-11,02 | FN-01,03,14 | ap-open-item |
| AC-02 | API-03,12 | FN-05 | ap-open-item (RTV) |
| AC-06 | API-04 | FN-06 | dn-totals |
| AC-07 | API-04 | FN-07 | dn-totals |
| AC-08 | API-02,04 | FN-08 | dn-totals,ap-open-item |
| AC-09 | API-04 | FN-09 | dn-totals,ap-open-item |
| AC-19 | API-03/04 | FN-19 | **dn-totals** |
| AC-20 | API-06,17 | FN-04,20 | **ap-open-item (dnSplit)** |
| AC-21 | API-16 | FN-21 | ENG-CSQ |
| AC-11 | API-05 | FN-11 | ENG-DOA,dn-totals |
| AC-12 | API-06 | FN-12 | DOC-NUM,dn-totals,ap-open-item |
| AC-13 | API-07 | FN-13,04 | — |
| AC-14 | API-05 | FN-02,14 | ENG-DOA (SoD) |
| AC-15 | API-08 | FN-15 | ap-open-item |
| AC-16 | API-09 | FN-16 | DOC-STORE |
| AC-17 | API-06 | FN-17 | dn-totals,ap-open-item |
| AC-18 | API-02 | FN-18 | dn-totals,ap-open-item |
| AC-90 | API-01,10 | FN-90,12 | dn-totals |
| AC-91 | API-* | FN-91 | — |
| AC-92 | API-13 | FN-92 | dn-totals,DOC-STORE |
> ทุก FN-01..21 + FN-90/91/92 + ENG dn-totals/ap-open-item/DOC-NUM/DOC-STORE/ENG-DOA/ENG-CSQ ถูก trace ≥1 AC. ✅

---

## §6.9 Cross-Module Test Cases ⭐ (BRD §12.1 Downstream — R12)
| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | อนุมัติ DN ครบสาย | AP ap_open_item (F-ACC-APINV) | dn_applied += applyToAp → outstanding ลด (ปิดเมื่อ=0) — ref tab "คงค้างหลังใบนี้" ตรง |
| XT-02 | บันทึก vendorCn | VAT Report ภ.พ.30 | input_vat_line negative = netVat เดือน **vendorCnDate** (ม.82/10) |
| XT-03 | อนุมัติ DN | Journal Entry (F093 mock) | Dr 2110 applyToAp · Cr 5xxx netBefore · Cr 1150 ภาษีซื้อ netVat |
| XT-04 | **ยกเลิก DN (draft/pending)** | AP ap_open_item | held คืน → dnRoom เพิ่มกลับ |
| XT-05 | ยกเลิกหลังอนุมัติ (ไม่รองรับ) | — | ปุ่ม "ออกเอกสารแก้ไข" (display-only, ไม่ถอนยอด) — OQ-DN-04 |
| XT-06 | RTV reason | RTV (W3-LITE mock) | RTV ของใบเดียวกัน · จำนวน ≤ ที่คืน |
| XT-07 | **ใบจ่ายครบ → vendorCredit** | Vendor Credit Ledger (F097) | vendorCredit = grand − applyToAp → credit ledger รายผู้ขาย (display-only · flow OQ-DN-06) |

---

## §6.10 Microcopy-Aware Expected Text (verbatim จาก HTML — ห้ามแต่งเอง)
- toast บันทึกร่าง: "บันทึกแบบร่างใบลดหนี้ผู้ขายเรียบร้อย" *(`บันทึกแบบร่าง${DOC.name}เรียบร้อย`)*
- toast อนุมัติครบ: "อนุมัติครบสาย — ออกใบลดหนี้ {code} · ลดยอดคงค้าง {inv}"
- toast อนุมัติขั้นกลาง: "อนุมัติขั้น {n} แล้ว — ส่งต่อ {assignee}"
- toast CSV: "ส่งออก CSV {n} รายการ" · toast persona (DEMO): "สลับบทบาทเป็น {roleLabel} (DEMO)"
- audit ออกเลข: "ออกเลข {code} · ลดหนี้ {inv} ฿X (หักหนี้ค้าง ฿Y · เครดิตคงเหลือกับผู้ขาย ฿Z) · ภาษีซื้อ ฿V (กลับเมื่อได้รับใบลดหนี้ผู้ขาย) · บันทึกเข้า 7C ตาม CSQ_BRIEF_F097 (จำลอง)"
- blockReason: "ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿X)" · "ยอดลดหนี้เกินมูลค่าที่ลดได้ (บันทึกร่างได้)" · "ระบุคำอธิบายเหตุผลอย่างน้อย 10 ตัวอักษร" · "เหตุผลคืนสินค้าต้องอ้างใบคืนสินค้า"
- guard toast: "แก้ไขได้เฉพาะฉบับร่าง" · "กรุณากรอกข้อมูลให้ครบถ้วน"
- field vendorCn: label "เลขที่ใบลดหนี้จากผู้ขาย (ถ้าได้รับแล้ว)" · placeholder "เช่น TFS-6650" · "วันที่ได้รับใบลดหนี้ผู้ขาย" + helper "ใช้กำหนดเดือนภาษีที่ลดภาษีซื้อใน ภ.พ.30"
- summary rows: "ยอดลดก่อน VAT" · "ภาษีซื้อที่ลด" · "ยอดลดหนี้สุทธิ" (+ "THB")
- status pill: "ฉบับร่าง" · "รออนุมัติ" · "อนุมัติแล้ว · รอส่ง" · "ส่งผู้ขายแล้ว" · "ยกเลิก"
- tab: "รายละเอียด" · "ใบตั้งหนี้อ้างอิง · ภาษีซื้อ" · "PDF Preview" · "ลายเซ็น / อนุมัติ" · "ประวัติ"
- note.warn ภาษีซื้อ: "รอใบลดหนี้ผู้ขาย"
> ผลลัพธ์: testcase จาก ai-testcase-md-generator จะ match จอ 1:1.
