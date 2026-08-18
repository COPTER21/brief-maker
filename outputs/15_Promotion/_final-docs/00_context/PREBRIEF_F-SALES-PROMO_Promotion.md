# PREBRIEF · Promotion — โปรโมชัน (ข้อเสนอชั่วคราวสำหรับลูกค้ากลุ่มกว้าง)
> Sales · Wave S2 ⑮ · จาก WAVE_PLAN_SALES + HTML `f-promotion.html` (source of truth · md5 4bc0d62e) + มาตรฐาน (D365 Retail discounts: simple/quantity/threshold/mix-and-match · Odoo promotion program · SAP free goods) + contract §7.3 `calcPromo(lines, doc)` + มติแชท 17 ส.ค. 2569
> เอกสารนี้คือ source of truth เชิง business — ทีมย่อยใช้เขียน FRD/TC ต่อ · [มติ] เคาะแล้ว · [AI-DRAFT] รอ Strike · [STD] มาตรฐาน ERP

---

## 0. Obligations
| # | พันธะ | จาก | ถูกตอบที่ § |
|---|---|---|---|
| OB-1 | เส้นเข้า: Sales Price List ⑪ + Trade Agreement ⑭ → ราคาที่ลูกค้าได้ (หลัง TA) เป็นฐานคำนวณโปรฯ · บรรทัด TA "ไม่ลดซ้ำ" = โปรฯ ไม่ซ้อน | HTML calcPromo(promoAllowed) · มติ | §5.3, BR-01, S-11, S-16 |
| OB-2 | เส้นเข้า: Customer Group / Sales Channel (S1) → ขอบเขต · Customer Master → ช่องทางเริ่มต้น + นับโควตาต่อลูกค้า | HTML scopeMatch | §3.1, S-01, S-02 |
| OB-3 | เส้นเข้า: Item Master (S0) → สินค้า/หมวด/หน่วย/factor/ราคาตั้ง | HTML PRODUCTS | §3.2 |
| OB-4 | เส้นเข้า: **GL Posting Group** (S0) → บัญชี contra-revenue / ค่าใช้จ่ายส่งเสริมการขาย · contract §7.3 "ส่วนลดส่งเสริมการขายลง Sales Line Disc. Account" | WAVE_PLAN dep · PROJECT_INSTRUCTIONS §7.3 | §3.1 glAccount, S-17 |
| OB-5 | เส้นเข้า/ออก: DOA F-DLG-001 → `DOA-SALES-PROMO` ไม่มีวงเงิน สายเดียว · เลือกคนต่อ slot · Employee (HR) | มติ 17 ส.ค. | §3.4, BR-DOA-*, S-05..S-08 |
| OB-6 | เส้นออก: Quotation ⑫ / Sales Order → เรียก `calcPromo(lines, doc)` คืน discount + gl_account + ของแถม (ENG `promo-engine`) | contract §7.3 | §5.3, S-11..S-16 |
| OB-7 | เส้นออก: Invoice → ลง GL ส่วนลด/ของแถม · นับ usage (ครั้ง/ยอด/ลูกค้า) · Inventory → ตัดสต๊อกของแถม | HTML usage · GL | S-17, S-18 |
| OB-8 | เส้นออก: ENG-NOTIFY → doa_* + `promo.budget_warn` (90%) · `promo.exhausted` · `promo.ended` · `promo.expiring` | HTML | §9 |
| OB-9 | เส้นออก: Document Configuration → เลขรัน `PM-YYYY-NNN` | doccfg | §7 |
| OB-10 | มติ: ลูกค้าเฉพาะราย → ไม่อยู่ในโปรโมชัน (ไป Trade Agreement) · โปรฯ = ลูกค้ากลุ่มกว้าง | มติ 17 ส.ค. | §1, S-23 |
| OB-11 | มติ: ทับซ้อน = เตือน + ยืนยันตอนส่ง · **ไม่ทับ/ยกเลิกโปรฯ เดิม** (ต่างจาก TA) — engine ตัดสินด้วยลำดับ + exclusive | มติ 17 ส.ค. | S-09, BR-06..08 |
| OB-12 | มติ UI: avatar+ตำแหน่ง+ชื่อ · list 1 แถว · page tabs · kit stepper · drawer landing hero | มติ 17 ส.ค. | §6 |
| OB-13 | มติ process: BA ส่ง HTML + PREBRIEF | มติ 16 ส.ค. | ทั้งฉบับ |

---

## 1. สรุป + ผู้ใช้ + สิทธิ์
**ทำอะไร** [มติ] — เก็บ "ข้อเสนอชั่วคราว" สำหรับลูกค้ากลุ่มกว้าง (ทุกราย / กลุ่มลูกค้า / ช่องทางการขาย) มีช่วงเวลา งบส่วนลด โควตา · **1 โปรฯ = 1 ชนิด** จาก 4: **ส่วนลดสินค้า** (%/บาท · สินค้า/หมวด/ทุกสินค้า · ขั้นต่ำ) · **ซื้อ X แถม Y** · **ยอดใบถึงเกณฑ์** (ขั้นบันได) · **ชุดราคาพิเศษ** · + คูปองโค้ด · ลำดับ+exclusive · ซ้อน TA ได้/ไม่ · GL จาก GL Posting Group · ระงับชั่วคราว/เปิดต่อ · ปิดก่อนกำหนด · Quotation/SO เรียก `calcPromo` อัตโนมัติ**หลัง**ราคาบัญชี+TA
**ลำดับราคาทั้งสาย [มติ]**: ราคาบัญชี (⑪ Resolver) → ข้อตกลงการค้า (⑭ NET/DISC) → **โปรโมชัน** (ตามลำดับ · exclusive หยุด) → ท้ายบิล TA → เงินคืน TA ตอนปิดงวด (OQ-1 ยืนยันตำแหน่ง TOTAL ของ TA vs THRESHOLD ของโปรฯ)

**หน้าจอ** (`#/promotions`) — page tabs: ทั้งหมด · กำลังใช้ · รอถึงวันเริ่ม · รออนุมัติ · ร่าง · ระงับชั่วคราว · สิ้นสุดแล้ว (+ปุ่มใกล้สิ้นสุด) · list 1 แถว/โปรฯ · drawer 920: เงื่อนไข&ขอบเขต (hero + fact grid) / การใช้งาน&งบ / การอนุมัติ&ข้อมูล / ประวัติ · สร้าง/แก้ 3 ขั้น (ชนิดและขอบเขต → เงื่อนไข → ตรวจสอบและยืนยัน) · ทดสอบตะกร้า (drawer 920) · modal: ส่งอนุมัติ (slot+ยืนยันทับซ้อน) / อนุมัติ / ไม่อนุมัติ / ยกเลิก / ระงับ / ปิดก่อนกำหนด

| Role | ทำอะไรได้ |
|---|---|
| Sales/Marketing Officer | สร้าง/แก้ร่าง · ส่งอนุมัติ · ยกเลิกร่าง/รออนุมัติ · ทำสำเนา · ทดสอบตะกร้า · export |
| Sales Manager (`role-mgr-sales`) | + อนุมัติขั้นที่ถูกเลือก · ระงับ/เปิดต่อ · ปิดก่อนกำหนด |
| BU Head (`role-mgr-bu`) | อนุมัติขั้นที่ถูกเลือก |
> สิทธิ์จริงจาก IAM — **OQ-2** · เจ้าของ feature: Sales (ตาม WAVE_PLAN own) — Marketing Campaign ⑬ อ้างถึงโปรฯ ได้ (OQ-9)

---

## 2. Scenarios (derive D1-D6)
> D1 (ปริมาณ/ยอด/งบ) → S-11..S-15, S-19 · D2 (state) → S-05..S-08, S-20..S-22 · D3 (อนุมัติ) → S-05..S-08 · D4 (ต้นทาง: ราคา/TA/คูปอง/สต๊อก) → S-16, S-18, S-24 · D5 (ปลายทาง QT/SO/Invoice/GL/Inventory) → S-11..S-18 · D6 [STD] → S-13 (D365 quantity/mix-match), S-12 (SAP free goods inclusive/exclusive), S-15 (Odoo coupon), S-19 (budget cap)

| S | ประเภท | ชื่อ | เกิดอะไร | **ข้อมูลที่ต้องมี** | ผลปลายทาง |
|---|---|---|---|---|---|
| S-01 | Happy | สร้างโปรฯ ทุกลูกค้า | เลือกชนิด · ช่วงเวลา · เงื่อนไข · GL → ส่งอนุมัติ | ตาม §3 | ร่าง → รออนุมัติ |
| S-02 | Alt | โปรฯ เฉพาะกลุ่มลูกค้า / ช่องทาง (หลายรายการ) | scope group/channel + refs ≥1 | soft-ref | engine เช็ค scopeMatch จากกลุ่มลูกค้า / ช่องทางบนเอกสาร (ว่าง = ช่องทางเริ่มต้นลูกค้า) |
| S-03 | Happy | ตั้งเงื่อนไข 4 ชนิด | LINE_DISC / FREE_GOODS / THRESHOLD / BUNDLE ตาม §3.2 | | validate ต่อชนิด |
| S-04 | Exception | เงื่อนไขไม่ผ่าน validate | % >100 · ไม่เลือกสินค้า · ขั้นไม่เรียง · ชุด <2 ตัว/ซ้ำ · ราคาชุด ≥ ราคาตั้งรวม · คูปองซ้ำ/รูปแบบผิด · วันเริ่มย้อนหลัง | | บล็อก + error |
| S-05 | Happy | ส่งอนุมัติ — เลือกคนต่อ slot | resolve DOA-SALES-PROMO (ไม่มีวงเงิน) → เลือกคนทุกขั้น | approval_chain | รออนุมัติ · My Approval · doa_pending |
| S-06 | Happy | อนุมัติตามลำดับจนครบ | คนที่ถูกเลือกขั้นปัจจุบัน | หมายเหตุ | มีผล/รอถึงวันเริ่ม · doa_result |
| S-07 | Exception | ไม่อนุมัติ (เหตุผล) | | | กลับร่าง · history |
| S-08 | Exception | SoD | | | ปุ่มซ่อน · picker ตัดตัวเอง |
| S-09 | Alt | **ทับซ้อน** ชนิดเดียวกัน + ขอบเขตตัดกัน + สินค้า/หมวดตัดกัน + ช่วงเวลาทับ | | รายการ + ลำดับ/exclusive ของแต่ละตัว | เตือน step 3 → **ติ๊กยืนยัน**ตอนส่ง (overlapAck) · ไม่ทับ/ยกเลิกของเดิม — engine ใช้ลำดับ+exclusive [มติ] |
| S-10 | Alt | ทำสำเนา | จากโปรฯ ใด ๆ | คูปองล้าง · วันเริ่มวันนี้ | ร่างใหม่ |
| S-11 | Happy | QT/SO: ส่วนลดสินค้า | บรรทัดตรง สินค้า/หมวด/ทั้งหมด · qty ฐาน ≥ ขั้นต่ำ · promoAllowed | ราคาหลัง TA · qty · factor | ลดต่อบรรทัด (% ของยอด · บาท×qtyฐาน ไม่เกินยอดบรรทัด) · GL |
| S-12 | Happy [STD] | QT/SO: ซื้อ X แถม Y | qty ฐานรวมของสินค้า X ≥ buyQty×factor → แถม getQty × ครั้ง (ทำซ้ำได้/ครั้งเดียว) | | บรรทัดของแถมราคา 0 · มูลค่า = ราคาที่ลูกค้าได้ × qty → GL ค่าใช้จ่าย · ตัดสต๊อก |
| S-13 | Happy [STD] | QT/SO: ยอดใบถึงเกณฑ์ | ฐาน = ยอดใบ − ส่วนลดบรรทัดโปรฯ ก่อนหน้า · ขั้นสูงสุดที่ถึง | | ลด %/บาท ทั้งใบ · ไม่ถึงบอก "ขาดอีก" |
| S-14 | Happy [STD] | QT/SO: ชุดราคาพิเศษ | จำนวนชุด = min(qty แต่ละตัว ÷ ที่ต้องมี) · ทำซ้ำได้/ชุดแรก | | ลด = (ราคาปกติรวมชุด − ราคาชุด) × ชุด |
| S-15 | Alt [STD] | คูปองโค้ด | โปรฯ มี coupon → เอกสารต้องใส่โค้ดตรง (ไม่สน case) | doc.coupon | ไม่ใส่ = ข้ามพร้อมเหตุ |
| S-16 | Alt | ซ้อนกับ TA / โปรฯ อื่น | ลำดับน้อยก่อน · exclusive ติดแล้วหยุด · TA net "ไม่ลดซ้ำ" → โปรฯ ส่วนลดบรรทัดข้ามสินค้านั้น · stackTA=false → ลูกค้าที่มี TA ไม่ได้โปรฯ (OQ-3) | | ladder แสดงติด/ข้าม+เหตุ |
| S-17 | Happy | ลงบัญชี | Invoice: ส่วนลดโปรฯ ลง GL ที่โปรฯ ระบุ (contra-revenue) · ของแถม: บรรทัด 0 บาท + ค่าใช้จ่ายส่งเสริมการขาย + ตัดสต๊อก | glAccount | GL Posting Group |
| S-18 | Happy | สะสม usage | ทุก Invoice ที่ใช้โปรฯ → uses/discount/customers/byCust | | ใช้กับโควตา งบ รายงาน |
| S-19 | Alt | งบ/โควตาหมด | discount ≥ budget หรือ uses ≥ limitTotal | | สถานะ "งบ/โควตาหมด" · engine ข้าม · 90% แจ้งเตือน · เพิ่มงบ = ทำสำเนาออกใหม่ (อนุมัติแล้วล็อก) |
| S-20 | Alt | ระงับชั่วคราว / เปิดต่อ | กำลังใช้ → ระงับ (เหตุผล) → เปิดต่อ | | เอกสารใหม่ไม่ได้โปรฯ ระหว่างระงับ · ช่วงเวลา/งบไม่เปลี่ยน |
| S-21 | Exception | ปิดก่อนกำหนด | กำลังใช้/รอเริ่ม/ระงับ/งบหมด · เหตุผล+วันมีผล | endEarly | เอกสารใหม่ไม่ได้ · เดิมไม่กระทบ · ย้อนกลับไม่ได้ |
| S-22 | Exception | ยกเลิก (ยังไม่มีผล) | ร่าง/รออนุมัติ · เหตุผล | | สถานะยกเลิก |
| S-23 | ไม่รองรับ | โปรฯ เฉพาะลูกค้ารายเดียว | — | — | ไป Trade Agreement ⑭ [มติ] |
| S-24 | Alt | ของแถมสต๊อกไม่พอ / ราคาหลัง TA เป็น 0 | | | engine ไม่เช็คสต๊อก — Inventory(ATP) ตอบตอนออก SO · แถมไม่ได้ = SO เตือน (OQ-4) |
| S-25 | Alt | โควตาต่อลูกค้า | byCust[cust] ≥ limitPerCust → ข้าม | | นับต่อ**ใบ** (Invoice) [AI-DRAFT] OQ-5 |
| S-26 | ไม่รองรับ | ลดแบบ multiline ข้ามสินค้าหลายตัวรวมชิ้น (D365 multiline discount) · โปรฯ ซ้อนหลายชนิดใน 1 โปรฯ | — | — | ทำเป็นหลายโปรฯ + ลำดับ [AI-DRAFT] |
| S-27 | ไม่รองรับ | บัตรสะสมแต้ม / loyalty point | — | — | นอก scope |

---

## 3. Data
### 3.1 โปรโมชัน (header)
| Field | ชนิด | บังคับ | Default | Validation / หมายเหตุ | ที่มา |
|---|---|---|---|---|---|
| รหัส | `PM-YYYY-NNN` | auto | Document Config | unique | [แผน] |
| ชื่อ · รายละเอียด | text | ✓ / ⬜ | | | |
| ชนิด | enum `LINE_DISC` / `FREE_GOODS` / `THRESHOLD` / `BUNDLE` (1 โปรฯ = 1 ชนิด) | ✓ | LINE_DISC | เปลี่ยนชนิดล้าง rule | [มติ][STD] |
| ขอบเขต | `all` / `group` (refs Customer Group ≥1) / `channel` (refs Sales Channel ≥1) — soft-ref | ✓ | all | | [มติ] |
| เริ่ม · สิ้นสุด | date | ✓ / ⬜ | วันนี้ | เริ่ม ≥ วันนี้ · สิ้นสุด ≥ เริ่ม | [AI-DRAFT] |
| คูปองโค้ด | text A-Z0-9-_ 3–20 | ⬜ | | unique ในโปรฯ ที่ยังไม่จบ · เก็บ uppercase · ว่าง = อัตโนมัติ | [STD Odoo] |
| ลำดับ | int 1–999 | ✓ | 10 | น้อยก่อน | [STD D365] |
| exclusive | bool | | false | ติดแล้วหยุดโปรฯ ถัดไป | [STD] |
| stackTA | bool | | true | ซ้อนข้อตกลงการค้าได้ไหม | [AI-DRAFT] OQ-3 |
| โควตารวม · โควตาต่อลูกค้า | int | ⬜ | 0=ไม่จำกัด | นับต่อใบ | [AI-DRAFT] OQ-5 |
| งบส่วนลด/ของแถม | number ฿ | ⬜ | 0=ไม่จำกัด | ครบ → engine ข้าม | [AI-DRAFT] |
| บัญชี GL | รหัสจาก GL Posting Group (soft-ref) | ✓ | 4110-02 | ส่วนลด = contra-revenue · ของแถม = ค่าใช้จ่ายส่งเสริมการขาย | [แผน §7.3] |
| ผู้ดูแล | Employee/text | ✓ | ผู้สร้าง | | |
| สถานะ · paused · endEarly · overlapAck | | auto | | §5 | |
| usage: uses · discount · customers · byCust | | auto | | จาก Invoice | |
| DOA field contract: approval_required(true) · approval_status · doa_entry_ref (`DOA-SALES-PROMO`) · approver_role · approved_by/at · approval_chain (snapshot ขั้น→ตำแหน่ง→คน) · approval_history | | | | | [/doa-declaration] |

### 3.2 rule ตามชนิด
| ชนิด | field | validation |
|---|---|---|
| LINE_DISC | target (product/category/all) · ref · mode (pct/amt) · value · minQty (หน่วยฐาน) | value >0 · pct ≤100 · minQty ≥1 · ref บังคับถ้า target≠all |
| FREE_GOODS | buyProduct · buyUom · buyQty · getProduct · getUom · getQty · repeat | ทุกช่องบังคับ · qty ≥1 · get อาจ = buy (แถมตัวเอง) |
| THRESHOLD | tiers[{min, mode pct/amt, value}] | ≥1 ขั้น · min >0 เรียงขึ้น · value >0 · pct ≤100 · **1 บรรทัดต่อโปรฯ** |
| BUNDLE | items[{product, uom, qty}] ≥2 ไม่ซ้ำ · bundlePrice · repeat | bundlePrice >0 และ < ราคาตั้งรวม |

### 3.3 Config ที่อ่าน (Sales Configuration)
currency · expiringDays (14) · applyOrder ทั้งสาย (§1) `[DEFAULT — รอยืนยัน OQ-1]`

### 3.4 DOA entry ที่ประกาศ
`DOA-SALES-PROMO` · F-SALES-PROMO · scope policy_approve · **ไม่มีวงเงิน** · sequential/merged · matrix 1 ชุด: 1) role-mgr-sales → 2) role-mgr-bu `[DEFAULT — รอยืนยัน OQ-7]` · ผู้ส่งเลือกคนต่อ slot (ตัดตัวเอง)

---

## 4. Business Rules
| BR | กติกา | S | ที่มา |
|---|---|---|---|
| BR-01 | โปรฯ คำนวณจากราคาที่ลูกค้าได้หลัง Price Resolver + TA · ราคาก่อน VAT | S-11..S-14 | [มติ] |
| BR-02 | เข้าข่ายเมื่อ: สถานะ "กำลังใช้" ณ วันที่เอกสาร (ไม่ระงับ · ไม่หมดงบ/โควตา · ในช่วงเวลา) + scope ตรง (ทุกราย / กลุ่มของลูกค้า / ช่องทางบนเอกสาร) + คูปองตรง (ถ้ามี) + ลูกค้ายังไม่ครบโควตา | S-11, S-15, S-19, S-20, S-25 | [มติ] |
| BR-03 | LINE_DISC: ต่อบรรทัด · qty ฐาน ≥ minQty · pct = ยอดบรรทัด×% · amt = value×qtyฐาน ไม่เกินยอดบรรทัด · ข้ามบรรทัดที่ TA "ไม่ลดซ้ำ" | S-11, S-16 | [มติ] |
| BR-04 | FREE_GOODS: รวม qty ฐานของสินค้า X ทุกบรรทัด ÷ (buyQty×factor) = ครั้ง (ทำซ้ำ) หรือ 1 · ของแถม = getQty×ครั้ง ราคา 0 · มูลค่าคิดจากราคาที่ลูกค้าได้ | S-12 | [STD SAP free goods] |
| BR-05 | THRESHOLD: ฐาน = ยอดใบ − ส่วนลดบรรทัดโปรฯ ก่อนหน้า · ใช้ขั้นสูงสุดที่ถึง (ไม่ marginal) · BUNDLE: ชุด = min(qty ÷ ต้องมี) · ลด = (ปกติ − ราคาชุด)×ชุด | S-13, S-14 | [STD] |
| BR-06 | ประเมินตาม**ลำดับ**น้อยก่อน (เท่ากัน → เริ่มล่าสุด) · โปรฯ ที่ติดและเป็น **exclusive** หยุดตัวถัดไป | S-16 | [STD D365] |
| BR-07 | ทับซ้อน = ชนิดเดียวกัน + ขอบเขตตัดกัน + (LINE_DISC: สินค้า/หมวดตัดกัน) + ช่วงเวลาทับ · สถานะ กำลังใช้/รอเริ่ม/รออนุมัติ/ระงับ → เตือน step 3 + บังคับยืนยันตอนส่ง (เก็บ overlapAck) | S-09 | [มติ] |
| BR-08 | ทับซ้อนไม่ทำให้โปรฯ เดิมถูกยกเลิก/ตัดวัน (ต่างจาก TA) — ผลลัพธ์กำหนดโดย BR-06 | S-09 | [มติ] |
| BR-09 | งบ: ถ้าส่วนลด/มูลค่าของแถมของใบนี้ทำให้เกินงบ → ข้ามพร้อมเหตุ · discount ≥ งบ หรือ uses ≥ โควตารวม → สถานะ "งบ/โควตาหมด" · 90% แจ้งเตือน | S-19 | [AI-DRAFT] |
| BR-10 | โควตาต่อลูกค้า นับต่อใบ (Invoice) · ครบ → ข้าม | S-25 | [AI-DRAFT] OQ-5 |
| BR-11 | อนุมัติแล้วล็อกแก้ไข — เปลี่ยนเงื่อนไข/งบ = ทำสำเนาออกใหม่ · ระงับ/เปิดต่อ/ปิดก่อนกำหนด ทำได้โดยไม่ต้อง DOA ใหม่ | S-10, S-20, S-21 | [AI-DRAFT] OQ-6 |
| BR-12 | ระงับได้เฉพาะ กำลังใช้ (เหตุผล) · เปิดต่อจากระงับ · ปิดก่อนกำหนดได้ กำลังใช้/รอเริ่ม/ระงับ/งบหมด (เหตุผล+วันมีผล) · ยกเลิกได้ ร่าง/รออนุมัติ (เหตุผล) | S-20..S-22 | [AI-DRAFT] |
| BR-13 | ของแถม: บรรทัดราคา 0 · ต้นทุนลง GL ค่าใช้จ่ายส่งเสริมการขาย · ตัดสต๊อก · engine ไม่เช็ค ATP (SO ทำ) | S-12, S-17, S-24 | [AI-DRAFT] OQ-4 |
| BR-14 | ส่วนลดโปรฯ ลง GL ที่โปรฯ ระบุ (จาก GL Posting Group · contra-revenue) ตอน Invoice · engine คืน gl_account ต่อรายการ | S-17 | [แผน §7.3] |
| BR-15 | คูปองโค้ด unique ในโปรฯ ที่ยังไม่สิ้นสุด · เทียบไม่สน case | S-04, S-15 | [AI-DRAFT] |
| BR-16 | โปรฯ ลูกค้าเฉพาะราย ไม่รองรับ — Trade Agreement | S-23 | [มติ] |
| BR-DOA-01..07 | ส่งได้เฉพาะร่าง · resolve→freeze ไม่มีวงเงิน · ไม่อนุมัติ→ร่าง append-only · SoD · เลือกคนทุก slot · sequential · เหตุผลบังคับ | S-05..S-08 | [/doa-declaration][มติ] |
| BR-17 | audit append-only ทุก transition/ระงับ/เปิดต่อ/ปิด/ยกเลิก/แก้ร่าง | ทุก S | [กติกากลาง] |

---

## 5. State Machine
### 5.1 โปรโมชัน
`ร่าง` → `รออนุมัติ` → `รอถึงวันเริ่ม` → `กำลังใช้` ⇄ `ระงับชั่วคราว` → `สิ้นสุด` · derive: `งบ/โควตาหมด` (จากกำลังใช้เมื่อ BR-09) · แขนง: `ยกเลิก` (ร่าง/รออนุมัติ) · `ปิดก่อนกำหนด` (กำลังใช้/รอเริ่ม/ระงับ/งบหมด)
| จาก | ไป | ใครกด | เงื่อนไข | S |
|---|---|---|---|---|
| — | ร่าง | ผู้ใช้ | สร้าง / ทำสำเนา / ตีกลับ | S-01, S-10, S-07 |
| ร่าง | รออนุมัติ | ผู้ส่ง | validate + slot ครบ + ยืนยันทับซ้อน (ถ้ามี) | S-05, S-09 |
| รออนุมัติ | รออนุมัติ(ขั้นถัดไป) / รอเริ่ม / กำลังใช้ | คนขั้นปัจจุบัน | อนุมัติ | S-06 |
| รออนุมัติ | ร่าง | คนขั้นปัจจุบัน | ไม่อนุมัติ+เหตุผล | S-07 |
| กำลังใช้ | ระงับชั่วคราว | ผู้จัดการ | เหตุผล | S-20 |
| ระงับชั่วคราว | กำลังใช้ | ผู้จัดการ | เปิดต่อ | S-20 |
| กำลังใช้ | งบ/โควตาหมด | ระบบ | BR-09 | S-19 |
| กำลังใช้/รอเริ่ม/ระงับ/งบหมด | ปิดก่อนกำหนด | ผู้จัดการ | เหตุผล+วันมีผล | S-21 |
| ร่าง/รออนุมัติ | ยกเลิก | ผู้ใช้ | เหตุผล | S-22 |
| รอเริ่ม→กำลังใช้→สิ้นสุด | | ระบบ (เวลา) | | |
### 5.2 promo-engine `calcPromo(lines, doc)` — input: lines[{product, uom, qty, unit(ราคาหลัง TA), promoAllowed}] · doc{customer, channel, date, coupon} · output: applied[{promo, amount, gl, note, freeItems}] · lineDisc{idx→฿} · orderDisc · freeItems[] · skipped[{promo, why}] — QT/SO เรียกหลัง price-resolver + trade-agreement-engine · Invoice ใช้ gl ต่อรายการ

---

## 6. Actions ต่อหน้า
| หน้า | action |
|---|---|
| หัวหน้า | ทดสอบตะกร้า · Export CSV · สร้างโปรโมชัน |
| page tabs + list | สถานะ 7 แท็บ + ปุ่มใกล้สิ้นสุด · ค้นหา (รวมคูปอง) · กรองชนิด/ขอบเขต · sort · แถวเปิด drawer · แก้(ร่าง) · ระงับ/เปิดต่อ · ยกเลิก(ร่าง/รออนุมัติ) · ปิดก่อนกำหนด |
| drawer (4 แท็บ) | แก้ไข · ส่งอนุมัติ · อนุมัติ/ไม่อนุมัติ · ระงับ/เปิดต่อ · ทำสำเนา · ยกเลิก · ปิดก่อนกำหนด · landing = hero เงื่อนไข + fact grid (ลำดับ/กันซ้อน/TA/โควตา/งบ/GL) |
| สร้าง/แก้ 3 ขั้น | ชนิด (seg 4) · ข้อมูล · ขอบเขต (seg + multi-pick) · คูปอง/ลำดับ/exclusive/stackTA/โควตา/งบ/GL → เงื่อนไขตามชนิด (LINE: target+ref+mode+value+minQty · FREE: buy/get+qty+uom+repeat · THRESHOLD: ขั้น +/− · BUNDLE: items +/− + ราคาชุด + ทุกชุด/ชุดแรก) → สรุป + note ทับซ้อน + สาย DOA · บันทึกร่าง / บันทึกและส่งอนุมัติ |
| modal ส่งอนุมัติ (กว้าง) | สรุป 4 ช่อง · slot คนต่อขั้น · ยืนยันทับซ้อน (ถ้ามี) |
| modal อื่น | อนุมัติ (หมายเหตุ) · ไม่อนุมัติ/ยกเลิก/ระงับ (เหตุผล) · ปิดก่อนกำหนด (เหตุผล+วันมีผล) |
| ทดสอบตะกร้า | ลูกค้า · ช่องทาง · คูปอง · เพิ่ม/ลบบรรทัด (สินค้า/หน่วย/qty) → บรรทัดลด · แถวของแถมราคา 0 · ยอดสุทธิ · ladder ติด/ข้าม+เหตุ |

---

## 7. Data behaviour
เลขรัน PM- จาก Document Config · soft-ref สินค้า/หมวด/กลุ่ม/ช่องทาง/GL/พนักงาน (LD-4C-02) · ไม่มี hard delete (ยกเลิก/ปิดก่อนกำหนด) · audit append-only · freeze approval_chain · overlapAck เก็บผู้ยืนยัน · สถานะ derive ตามเวลา+งบ+โควตา+paused · usage มาจาก Invoice (ไม่แก้มือ) · คูปอง uppercase

---

## 8. Mock Data Spec
| ชุด | prove |
|---|---|
| PM-011 ลด 10% BEV ทุกลูกค้า minQty 12 งบ 150k ใช้ 32% | S-01, S-11, S-19 |
| PM-012 ซื้อน้ำดื่ม 10 ลัง แถม 1 ลัง (ค้าส่ง · repeat · โควตา/ลูกค้า 5 · งบ 80k 77%) | S-02, S-12, S-25 |
| PM-013 ท้ายบิล 20k→3% 50k→5% (ออนไลน์/Marketplace) | S-13 |
| PM-014 ชุดสุขอนามัย 189 (หน้าร้าน/LINE · exclusive) รออนุมัติ | S-14, S-05..S-08 |
| PM-015 คูปอง WELCOME100 (ออนไลน์ · ต่อลูกค้า 1 · รวม 1000) ร่าง | S-15 |
| PM-009 ลด 5% ขนม GT ระงับชั่วคราว | S-20 |
| PM-005 ลด 8% ทุกสินค้า Mid-Year สิ้นสุด งบ 94% exclusive | S-16, S-19 |
| ตะกร้า default: ทองดี (ค้าส่ง) 10 ลังน้ำดื่ม + 48 ขวดชาเขียว + 24 ซองมันฝรั่ง → ติด PM-012 แถม 1 ลัง + PM-011 ลด BEV | S-11, S-12, S-16 |
| unit test 14 เคส (แถม/ทำซ้ำ/ขั้นต่ำ/ท้ายบิล/ระงับ/TA noStack/บาทต่อหน่วยฐาน/exclusive/ชุด/คูปอง/งบหมด) PASS | §5.2 |

---

## 9. Edges + Hotspot
| ทิศ | คู่ | จุด UI | ปลายทาง |
|---|---|---|---|
| เข้า | Price Resolver ⑪ + TA ⑭ | ทดสอบตะกร้า "ราคาหลังบัญชีราคา" | unit + promoAllowed |
| เข้า | Customer Group / Sales Channel / Customer | picker ขอบเขต · sim | scopeMatch · ช่องทางเริ่มต้น |
| เข้า | Item Master | picker สินค้า/หมวด | factor · ราคาตั้ง (validate ชุด) |
| เข้า | GL Posting Group | select GL | contra-revenue / ค่าใช้จ่ายของแถม |
| เข้า/ออก | DOA · Employee | modal ส่ง | DOA-SALES-PROMO |
| ออก | QT/SO | (ladder) | promo-engine · บรรทัดของแถม 0 บาท · ล็อกโปรฯ ในเอกสาร |
| ออก | Invoice | usage | ลง GL ต่อรายการ · usage/byCust · โควตา · งบ |
| ออก | Inventory | ของแถม | ตัดสต๊อก · ATP ตอน SO |
| ออก | ENG-NOTIFY | | doa_* · promo.budget_warn / exhausted / ended / expiring |
| ออก | Campaign ⑬ (S3) | — | แคมเปญอ้างโปรฯ หลายตัว (OQ-9) |

---

## 10. OQ + [AI-DRAFT] register
| # | ประเด็น | เจ้าภาพ |
|---|---|---|
| OQ-1 | ลำดับทั้งสาย: ราคาบัญชี → TA NET/DISC → โปรฯ → TA TOTAL ใช่ไหม · โปรฯ THRESHOLD กับ TA TOTAL ซ้อนกันได้ไหม | Strike |
| OQ-2 | สิทธิ์: ใครสร้าง/ระงับ/ปิดก่อนกำหนด · Marketing สร้างโปรฯ ได้ไหม | Strike |
| OQ-3 | stackTA=false ตีความว่า "ลูกค้าที่มี TA มีผลไม่ได้โปรฯ นี้เลย" ใช่ไหม | Strike |
| OQ-4 | ของแถมสต๊อกไม่พอ: SO เตือน/บล็อก/แถมบางส่วน · ต้นทุนของแถมลง GL ไหน (ค่าใช้จ่ายส่งเสริมการขาย vs COGS) | Strike · Accounting |
| OQ-5 | โควตาต่อลูกค้า นับต่อใบ หรือต่อครั้งที่ติด (ทำซ้ำหลายครั้งในใบเดียว) | Strike |
| OQ-6 | ระงับ/เปิดต่อ/ปิดก่อนกำหนด ต้อง DOA ไหม (ตอนนี้ไม่ต้อง) · เพิ่มงบต้องทำสำเนาใหม่ยืนยันไหม | Strike |
| OQ-7 | สาย DOA-SALES-PROMO 1) ผู้จัดการฝ่ายขาย → 2) หัวหน้า BU | Strike |
| OQ-8 | ทับซ้อน: บล็อกหรือแค่ยืนยัน (ตอนนี้ยืนยัน) | Strike |
| OQ-9 | Campaign Management ⑬ อ้างโปรฯ หลายตัว + งบรวมแคมเปญ — TA/โปรฯ รายงานเข้าแคมเปญไหม | Strike |
| OQ-10 | ลงทะเบียน ENG `promo-engine` (calcPromo) | Architect |

---

## 11. Coverage Matrix
| S | BR | transition | UI | FN |
|---|---|---|---|---|
| S-01 | BR-11 | —→ร่าง | สร้าง 3 ขั้น | FN-01, FN-02 |
| S-02 | BR-02 | | seg ขอบเขต + multi-pick | FN-03 |
| S-03 | BR-03, BR-04, BR-05 | | rule editor 4 ชนิด | FN-04, FN-05, FN-06, FN-07 |
| S-04 | BR-15 | | error | FN-08 |
| S-05 | BR-DOA-01, BR-DOA-02, BR-DOA-05 | ร่าง→รออนุมัติ | modal ส่ง | FN-09, FN-10 |
| S-06 | BR-DOA-06 | →มีผล | อนุมัติ · timeline | FN-11, FN-12 |
| S-07 | BR-DOA-03, BR-DOA-07 | →ร่าง | modal ไม่อนุมัติ | FN-13 |
| S-08 | BR-DOA-04 | | ปุ่มซ่อน | FN-14 |
| S-09 | BR-07, BR-08 | | note + ack | FN-15, FN-16 |
| S-10 | BR-11 | —→ร่าง | ทำสำเนา | FN-17 |
| S-11 | BR-01, BR-02, BR-03, BR-14 | | ตะกร้า | FN-18 |
| S-12 | BR-04, BR-13 | | ตะกร้า ของแถม | FN-19 |
| S-13 | BR-05 | | ตะกร้า | FN-20 |
| S-14 | BR-05 | | ตะกร้า | FN-21 |
| S-15 | BR-02, BR-15 | | คูปองในตะกร้า | FN-22 |
| S-16 | BR-06, BR-03 | | ladder | FN-23, FN-24 |
| S-17 | BR-14, BR-13 | | tab การใช้งาน "การลงบัญชี" | FN-25 |
| S-18 | BR-09, BR-10 | | tab การใช้งาน | FN-26 |
| S-19 | BR-09 | กำลังใช้→งบหมด | สถานะ · ladder ข้าม | FN-27 |
| S-20 | BR-12, BR-11 | กำลังใช้⇄ระงับ | ปุ่ม/modal | FN-28 |
| S-21 | BR-12 | →ปิดก่อนกำหนด | modal | FN-29 |
| S-22 | BR-12 | →ยกเลิก | modal | FN-30 |
| S-23, S-26, S-27 | BR-16 | ไม่รองรับ | — | — |
| S-24 | BR-13 | | — | FN-19 |
| S-25 | BR-10 | | ladder ข้าม | FN-31 |
| — | BR-17 | | audit | FN-94 |
ผ่าน: ทุก BR/transition ถูกอ้าง · ทุก S มี FN (ไม่รองรับระบุชัด) · OB-1..13 ถูกอ้าง
