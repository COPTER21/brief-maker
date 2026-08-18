# PREBRIEF · Sales Order — คำสั่งขาย / ใบสั่งขาย (จุดรวม O2C)
> Sales · Wave S4 · จาก WAVE_PLAN_SALES + HTML `f-sales-order.html` (source of truth · md5 c9590328 · UX ล็อกตาม purchase-order.html reference · CI Warm Light v8) + contract §7.3 + F-PAYTERM / F-PAYMETHOD + มติแชท 16–18 ส.ค. 2569
> เอกสารนี้คือ source of truth เชิง business — ทีมย่อยใช้เขียน FRD/TC ต่อ · [มติ] เคาะแล้ว · [AI-DRAFT] รอ Strike · [STD] มาตรฐาน ERP (SAP SD Order / Odoo Sale / D365 SO)

---

## 0. Obligations
| # | พันธะ | จาก | ตอบที่ § |
|---|---|---|---|
| OB-1 | เส้นเข้า **Quotation ⑫** → แปลงเป็น SO (ค้นหา/กรอง/พิมพ์เลขที่+Enter · เฉพาะสถานะ ตกลง/รอตอบ · ราคาคำนวณใหม่ ณ วันสั่ง · QT → "แปลงแล้ว") | WAVE_PLAN S3 · HTML step 1 | S-01, S-02, BR-01 |
| OB-2 | เส้นเข้า **Customer Master ⑦** → ที่อยู่ส่ง/ออกบิล · ช่องทาง · rep · payment term default · เลขผู้เสียภาษี | HTML setCustomer | §3.1, S-03 |
| OB-3 | เส้นเข้า **Credit Limit ⑧** → hard control: exposure = ยอด − ส่วนที่จ่ายก่อน/มัดจำ vs (วงเงิน − AR − SO เปิดอยู่) · ยืนยัน = นับ openSO · ยกเลิก = ปล่อย · ลิงก์ขอเพิ่มวงเงิน | มติ · HTML creditCheck | S-14, BR-10..12 |
| OB-4 | เส้นเข้า **Salesperson ⑩** → rep + เป้า/คอมมิชชั่น (S8) | HTML | §3.1, S-31 |
| OB-5 | เส้นเข้า **Price List ⑪ → Trade Agreement ⑭ → Promotion ⑮** engine chain ต่อบรรทัด (auto · แสดง ladder · toggle TA/โปรฯ · คูปอง · ของแถม · ท้ายบิล) | มติ 17 ส.ค. · contract §7.3 | S-04..S-09, BR-02..07 |
| OB-6 | เส้นเข้า **Item Master** → goods vs **service** · units/factor · VAT group · ราคาตั้ง | HTML PRODUCTS.kind | §3.2, S-10, BR-08 |
| OB-7 | เส้นเข้า **Inventory** → ATP ต่อคลัง · **hard validate ขั้น 3 + ก่อนส่งอนุมัติ** · **reserve เมื่อยืนยัน** · backorder/retry · release เมื่อยกเลิก/close short · DN ตัดจ่าย · บริการข้าม | มติ 18 ส.ค. | S-10..S-13, BR-08, BR-13..16 |
| OB-8 | เส้นเข้า **Payment Term master (F-PAYTERM)** → 6 แบบฝั่งขาย + Warehouse trigger + due basis · **paymentPlan** ต่อ SO | f-payterm.html | §3.4, S-19..S-22, BR-17..19 |
| OB-9 | เส้นเข้า **Payment Method master (F-PAYMETHOD)** → รับชำระ (RV) วิธี/ค่าธรรมเนียม/settle | f-paymethod.html | S-23 |
| OB-10 | เส้นเข้า **Campaign ⑬** (S3) → อ้างแคมเปญ · นับยอดเข้าแคมเปญ | HTML | §3.1 |
| OB-11 | เส้นเข้า **DOA F-DLG-001** → `DOA-SALES-SO` ไม่มีวงเงิน · slot เลือกคน · SoD · Employee | มติ 17 ส.ค. | S-15..S-18, BR-DOA-* |
| OB-12 | เส้นออก **Warehouse (S5 Picking/Packing/DN)** → จัดส่งตาม reserve · trigger ตาม payment term · partial · pickup | HTML mockDN | S-24, S-25 |
| OB-13 | เส้นออก **AR Invoice / Receipt (S6)** → วางบิล (ตาม DN / ทั้งใบ) · ครบกำหนด/เกินกำหนด · GL contra ส่วนลด/ของแถม · RV จับคู่งวด | HTML | S-26, S-23 |
| OB-14 | เส้นออก **RMA / Credit Note (S7)** → รับคืนหลัง DN · ห้ามยกเลิก SO ที่ส่งแล้ว | HTML mockRMA | S-28, BR-21 |
| OB-15 | เส้นออก **Module Linkage (Sales Configuration)** dual-mode ส่ง/บิล/ชำระ auto vs manual + ปิดอัตโนมัติเมื่อครบ 3 | CUBE_KNOWLEDGE §7 | S-29, BR-22 |
| OB-16 | เส้นออก **Doc Center** (แนบไฟล์ขั้น 4) · **ENG-NOTIFY** (doa_* · so.confirmed · so.hold · so.cancelled · so.backorder) · **Document Config** เลขรัน SO- | | §7, §9 |
| OB-17 | มติ UI: drawers/landing/step 3 = ตาม PO reference 1:1 (Warm Light) · 5 ขั้น (แหล่งที่มา/ข้อมูลหลัก/รายการ/แนบไฟล์/ตรวจสอบ) · landing 6 แท็บ · ลายเซ็น = Approval Timeline v8 · list 1 แถว | มติ 17–18 ส.ค. | §6 |
| OB-18 | มติ process: BA ส่ง HTML + PREBRIEF | มติ 16 ส.ค. | ทั้งฉบับ |

---

## 1. สรุป + ผู้ใช้ + สิทธิ์
**ทำอะไร** [มติ] — รับคำสั่งซื้อจากลูกค้า (สร้างใหม่ / แปลงจากใบเสนอราคา) · ราคาต่อบรรทัดคำนวณอัตโนมัติจาก **บัญชีราคา → ข้อตกลงการค้า → โปรโมชัน (+คูปอง · ของแถม · ท้ายบิล)** · แก้ราคาด้วยมือได้ตามสิทธิ์ (บังคับเหตุผล) · ตรวจ **เครดิต hard control** และ **สต๊อก ATP hard validate** (บริการไม่ตรวจ) · ผ่าน **DOA** (ไม่มีวงเงิน · เลือกคนต่อ slot) → **ยืนยัน = จองสต๊อก + นับเครดิต + ส่ง Warehouse ตาม payment trigger** → ติดตาม จัดส่ง / วางบิล / รับชำระ (ตามแผนการชำระของ payment term) / รับคืน / ปิดอัตโนมัติ · พัก · ยกเลิก · ปิดยอดค้าง · ทำสำเนา

**หน้าจอ** — list (filter card 5 ตัว + ตาราง สถานะ 3 แกน + สต๊อก + ลายเซ็น x/y + row menu) · create/edit wizard 5 ขั้น (drawer 1290) · landing drawer 6 แท็บ: รายละเอียด / สต๊อกและการส่ง / เครดิต·บิล·ชำระ / PDF Preview / ลายเซ็น·อนุมัติ / ประวัติ · modals: ส่งอนุมัติ (slot) · อนุมัติ · ไม่อนุมัติ · ยกเลิก · พัก · ปิดยอดค้าง · manual linkage · รับชำระ (RV)

| Role (IAM · persona สลับได้) | ทำอะไรได้ |
|---|---|
| Sales Officer / Rep | สร้าง/แก้ร่าง · แปลงจาก QT · ส่งอนุมัติ · ทำสำเนา · ยกเลิกร่าง/รออนุมัติ · แนบไฟล์ |
| Sales Manager (`role-mgr-sales`) | + อนุมัติขั้นที่ถูกเลือก · พัก/ปลดพัก · ยกเลิก SO ที่ยืนยัน (ยังไม่ส่ง) · ปิดยอดค้าง · แก้ราคาด้วยมือ (OQ) |
| BU Head (`role-mgr-bu`) | อนุมัติขั้นที่ถูกเลือก |
| Warehouse (นอก feature) | ออก DN ตาม reserve/trigger · retry จอง |
| Finance/AR (นอก feature) | วางบิล · รับชำระ (RV) · RMA/CN |
> สิทธิ์จริงจาก IAM/Policy Center — **OQ-2**

---

## 2. Scenarios (derive D1-D6)
> D1 (จำนวน/ราคา/ยอด/เครดิต/สต๊อก) → S-04..S-14 · D2 (state) → S-15..S-30 · D3 (อนุมัติ) → S-15..S-18 · D4 (ต้นทาง QT/ลูกค้า/master/term) → S-01..S-03, S-19..S-22 · D5 (ปลายทาง WH/AR/Fin/RMA/Linkage) → S-23..S-29 · D6 [STD] → S-11 (SAP ATP/reservation) · S-21 (deposit gate) · S-27 (close short = SAP reject remaining) · S-28 (return order)

| S | ประเภท | ชื่อ | เกิดอะไร | **ข้อมูลที่ต้องมี** | ผลปลายทาง |
|---|---|---|---|---|---|
| S-01 | Happy | สร้างใหม่ | เลือก "สร้างใหม่" → เลือกลูกค้า → default ที่อยู่/ช่องทาง/rep/term/กำหนดส่ง+3 วัน/ที่อยู่ออกบิล | §3.1 | ร่าง |
| S-02 | Happy | แปลงจากใบเสนอราคา | ค้นหา/กรอง (สถานะ · ลูกค้า) หรือพิมพ์เลขที่+Enter → ดึงลูกค้า+รายการ · ราคาคำนวณใหม่ ณ วันสั่ง | QT status accepted/sent เท่านั้น | ร่าง อ้าง QT · QT → แปลงแล้ว (OQ-3 ล็อกราคา QT?) |
| S-03 | Alt | ข้อมูลหลัก | ผู้ติดต่อ · วิธีรับ (ส่ง/มารับเอง) · คูปอง · แคมเปญ · PO ลูกค้า · คลังที่จ่าย · ใบกำกับเต็ม/ย่อ · หมายเหตุ | | |
| S-04 | Happy | ราคาอัตโนมัติต่อบรรทัด | เพิ่มสินค้า → บัญชีราคาตามกลุ่มลูกค้า → TA (ราคาสุทธิ/ส่วนลด · "ไม่ลดซ้ำ") → โปรฯ (ส่วนลด/ของแถม/ท้ายบิล/คูปอง) · เปลี่ยน qty/หน่วย/ช่องทาง = คำนวณใหม่ | ladder + evals | ราคา/หน่วย + ส่วนลด% + บรรทัดของแถม 0 บาท + ท้ายบิลอัตโนมัติ |
| S-05 | Alt | การ์ดปรับราคา: ปิด/เปิด TA | toggle "ใช้ข้อตกลงการค้า" | audit | ราคากลับบัญชีราคา · ผู้อนุมัติเห็น (OQ-4 ต้องเหตุผล/สิทธิ์?) |
| S-06 | Alt | การ์ดปรับราคา: ปิด/เปิดโปรฯ รายตัว · คูปอง | toggle ต่อโปรฯ ที่ติด · ใส่คูปอง Enter/blur | evals: ติด/ไม่เข้าเงื่อนไข/ต้องคูปอง/ปิดไว้ | ของแถม/ส่วนลดหาย-กลับ · audit |
| S-07 | Alt | แก้ราคาด้วยมือ | พิมพ์ราคาต่างจากระบบ → flag override · ปุ่ม "ใช้ราคาระบบ" | เหตุผลบังคับก่อนบันทึก/ส่ง (ขั้น 5) | ผู้อนุมัติเห็นบรรทัด+เหตุผล (OQ-1 สิทธิ์/DOA เพิ่ม?) |
| S-08 | Alt | ส่วนลดท้ายบิลด้วยมือ | toggle + จำนวนเงิน/% (ทับค่าอัตโนมัติ) | audit | |
| S-09 | Alt | VAT ต่อบรรทัด (แถวขยาย lean) | ไม่คิด / บวกเพิ่ม / รวมแล้ว NET · % · หมายเหตุ | B2 calcLineVat 3 โหมด | totals ลำดับตายตัว |
| S-10 | Happy | สินค้าบริการ | เพิ่ม SV-xxxx | kind=service | ไม่ตรวจ ATP · ไม่จอง · ไม่ตัดคลัง · ตัดจ่ายเมื่อวางบิล |
| S-11 | Exception | สต๊อกไม่พอ (goods) | ATP ณ คลังที่เลือก < ต้องการ | การ์ด alert สัดส่วน (มี/ต้องการ/ขาด/%) | **บล็อกขั้น 3** และ **บล็อกส่งอนุมัติ** จน ลดจำนวน/เปลี่ยนคลัง/รอของเข้า [มติ 18 ส.ค.] |
| S-12 | Happy | ยืนยัน → จองสต๊อก | อนุมัติครบ → reserve ต่อบรรทัด goods ที่คลัง | reserve{need,reserved,backorder,wh} | สต๊อกถูกล็อก · ของหายไประหว่างรอ → backorder + notify + retry |
| S-13 | Alt | จองค้าง (backorder) | กด "จองสต๊อกที่ค้าง" เมื่อของเข้า | | reserved เพิ่ม · แท็บสต๊อกอัพเดต |
| S-14 | Exception | เครดิตเกิน (hard control) | exposure > คงเหลือ (เงินสด/prepay ไม่ใช้เครดิต · deposit นับเฉพาะส่วนเหลือ) | แถบแดง · ปุ่มส่ง disabled · บันทึกร่างได้ | ขอเพิ่มวงเงินที่ ⑧ (OQ-5 hard/soft ต่อ role) |
| S-15 | Happy | ส่งอนุมัติ — เลือกคนต่อ slot | เช็คสต๊อก+เครดิตซ้ำ → modal slot (ตำแหน่ง→คน) → freeze | approval_chain | รออนุมัติ · My Approval · doa_pending |
| S-16 | Happy | อนุมัติตามลำดับจนครบ | คนที่ถูกเลือกในขั้นปัจจุบัน (ปุ่มใน header + inline ใน timeline) | หมายเหตุ | ครบ → **ยืนยัน**: reserve · openSO += exposure · TA ผูกพัน · Warehouse (ตาม trigger) · doa_result |
| S-17 | Exception | ไม่อนุมัติ | เหตุผลบังคับ | | กลับร่าง · history append-only |
| S-18 | Exception | SoD | | | ปุ่มซ่อน · picker ตัดตัวเอง |
| S-19 | Happy [STD] | Payment term: เครดิต N วัน (+EOM · ลดจ่ายเร็ว) | แผน 1 งวด · ครบกำหนด invoice/EOM+N | | Warehouse ทันที · เกินกำหนด pill |
| S-20 | Happy | Payment term: เงินสด / ชำระเต็มก่อนส่ง | CASH = ครบกำหนดวันส่ง · PREPAY = 1 งวดเมื่อยืนยัน | | PREPAY: **Warehouse ล็อก DN จนรับเงินครบ** · ไม่ใช้เครดิต |
| S-21 | Happy [STD] | Payment term: มัดจำ + ส่วนเหลือ | งวด 1 มัดจำ % ตอนยืนยัน · งวด 2 หลังส่ง N วัน | | Warehouse ปล่อยหลังรับมัดจำ · เครดิตนับเฉพาะส่วนเหลือ |
| S-22 | Happy | Payment term: แบ่งงวด / ทยอยส่ง | INST3 งวดตาม master · PARTIAL งวดงอกตาม Invoice ของ DN | | |
| S-23 | Happy | รับชำระ (Finance mock) | เลือกงวด · วิธีชำระจาก Payment Method (ค่าธรรมเนียม/settle) · ยอด · อ้างอิง → RV | RV จับคู่งวด FIFO | สถานะชำระ auto (บางส่วน/ครบ) · AR ลด · Invoice ชำระแล้ว |
| S-24 | Happy | จัดส่ง (Warehouse) | ยืนยัน + trigger ผ่าน + ไม่พัก → DN บางส่วน/ครบ · ตัดจ่ายจากจอง | docs.dn · linkage.delivery | สถานะ กำลังส่ง → ส่งครบ |
| S-25 | Alt | ลูกค้ามารับเอง | deliveryMethod=pickup | | จองไว้รอรับ · DN = รับที่คลัง (OQ-6) |
| S-26 | Happy | วางบิล (AR) | ตาม DN/ทั้งใบ · ที่อยู่ออกบิล · ใบกำกับเต็ม/ย่อ · GL ส่วนลด/ของแถม | docs.inv + ครบกำหนด | สถานะ วางบิลครบ |
| S-27 | Alt [STD] | ปิดยอดค้าง (close short) | ส่งบางส่วนแล้ว ลูกค้าไม่รอ → เหตุผล | | ยกเลิกส่วนที่เหลือ · ปล่อยจอง · จัดส่ง = ครบ · AR วางบิลตามส่งจริง |
| S-28 | Alt [STD] | รับคืน (RMA → CN) | หลัง DN | docs.rma · CN | สถานะ "รับคืน/ลดหนี้" (บางส่วน = คงสถานะเดิม + RMA แสดง) · Warehouse รับเข้า |
| S-29 | Alt | Module Linkage manual | config ไม่เชื่อม → ผู้ใช้อัพเดตสถานะ ส่ง/บิล/ชำระ เอง (เหตุผล/อ้างอิง) | manual{} | สถานะรวมคำนวณเหมือน auto |
| S-30 | Exception | พัก / ปลดพัก · ยกเลิก | พัก (ร่าง→ไม่ · ยืนยัน/กำลังส่ง ได้) เหตุผล · Warehouse หยุด · จองคงไว้ (config) · ยกเลิก (ร่าง/รออนุมัติ/ยืนยัน/พัก) เหตุผล → ปล่อยจอง+เครดิต · **มี DN แล้วยกเลิกไม่ได้ → RMA** | | |
| S-31 | Alt | ปิดอัตโนมัติ · เป้า/คอมมิชชั่น | ส่ง+บิล+ชำระ ครบ → ปิด · ยอดก่อน VAT นับเป้า/คอมมิชชั่นตามช่องทาง (mock %) | | S8 Dashboard |
| S-32 | Alt | ทำสำเนา · แก้ไขร่าง · แนบไฟล์ · PDF/พิมพ์ | | Doc Center · A4 template | |
| S-33 | ไม่รองรับ | แก้ SO ที่ยืนยันแล้ว (เปลี่ยนรายการ/ราคา) | — | — | ยกเลิก/ทำสำเนา หรือ close short + SO ใหม่ [AI-DRAFT] OQ-7 |
| S-34 | ไม่รองรับ | ของแถม/ส่วนลดที่ไม่มีในโปรฯ/TA (manual free item) | — | — | ต้องผ่าน Promotion/TA หรือ DOA แยก [AI-DRAFT] OQ-8 |
| S-35 | ไม่รองรับ | ขายต่างสกุลเงิน · Drop-ship · Consignment | — | — | phase ถัดไป |

---

## 3. Data
### 3.1 Header
| Field | ชนิด | บังคับ | Default/ที่มา | Validation | ที่มาข้อ |
|---|---|---|---|---|---|
| รหัส `SO-YYYY-NNNN` | auto | | Document Config | | |
| แหล่งที่มา · quotation | new / qt · รหัส QT (soft-ref) | | | QT ต้อง accepted/sent | S-02 |
| ลูกค้า | รหัส (soft-ref ⑦) | ✓ | picker | | |
| ที่อยู่จัดส่ง · ที่อยู่ออกบิล · ผู้ติดต่อ | text | ส่ง ✓ | จาก Customer addr[0] (เลือกได้หลายที่อยู่) | | |
| ช่องทาง · พนักงานขาย · แคมเปญ | soft-ref | ✓ ✓ ⬜ | default ลูกค้า | | |
| วันที่สั่ง · กำหนดส่ง | date | ✓ ✓ | วันนี้ / +3 วัน (config) | ส่ง ≥ สั่ง | |
| คลังที่จ่าย | soft-ref WH | ✓ | WH-BKK | กระทบ ATP/จอง | |
| วิธีรับสินค้า | deliver / pickup | | deliver | | |
| Payment term | รหัสจาก F-PAYTERM (use_in so) | ✓ | จาก Customer / TA | | §3.4 |
| ใบกำกับภาษี | bool | | true | | |
| คูปอง · PO ลูกค้า · หมายเหตุ | text | | | คูปอง uppercase | |
| useTA · promoDisabled[] | bool · list | | true · [] | audit | S-05, S-06 |
| endbill {enabled, mode, value, src} · couponAmt | | | auto/manual | | |
| priceOverride · overrideNote | bool · text | เหตุผลบังคับถ้า override | | | |
| attachments[] | Doc Center | | | | |
| status · hold · cancel · closeShort · linkage{delivery,invoice,payment} · manual{} · docs{dn,inv,rv,rma} · reserve ต่อบรรทัด | | | | | §5 |
| DOA field contract (approval_required · approval_status · doa_entry_ref `DOA-SALES-SO` · approver_role · approved_by/at · approval_chain · approval_history) | | | | | |
| createdBy/At · submittedBy/At · confirmedBy/At · audit[] | | | | | |

### 3.2 Line (B2 contract + SO)
| Field | หมายเหตุ |
|---|---|
| id · item_code · item_name · qty · unit · unit_price · discount_pct · vat_mode (none/add/included) · vat_pct · note | B2 verbatim |
| price_src (บัญชีราคา) · ta_src · promo_disc · _sysPrice · _noStack · override | สาย ⑪⑭⑮ |
| is_free · promo | บรรทัดของแถม (ราคา 0 · แก้ไม่ได้ · งอกอัตโนมัติ) |
| reserve {wh, need, reserved, backorder, shipped, released, skip(service)} | Inventory |
| kind (จาก Item Master) | goods / service |

### 3.3 Config (Sales Configuration)
vatPct 7 · defaultDeliveryDays 3 · creditHardControl true (OQ-5) · allowPriceOverride true · priceOverrideNeedsNote true · holdKeepsReserve true (OQ-9) · linkage {delivery, invoice, payment} auto/manual · atpSoft=false (บล็อก · มติ)

### 3.4 Payment Term ที่ SO รองรับ (F-PAYTERM)
| code | type | trigger | แผน |
|---|---|---|---|
| CASH | full_postpay | immediate | 1 งวด วันส่ง |
| PREPAY | full_prepay | **after_full** | 1 งวดเมื่อยืนยัน · ล็อก DN |
| N15/N30/N60/2-10N30/EOM30 | credit | immediate | 1 งวด basis+N · ลดจ่ายเร็ว · EOM |
| DEP50/DEP30 | deposit | **after_deposit** | มัดจำ % ตอนยืนยัน + ส่วนเหลือหลังส่ง N |
| INST3 | installment | immediate | งวดตาม master |
| PARTIAL | partial_delivery | immediate | งวดตาม Invoice ของ DN |
Direct Payment ไม่ผ่าน SO (ตาม master)

### 3.5 DOA entry
`DOA-SALES-SO` · F-SALES-SO · policy_approve · **ไม่มีวงเงิน** · sequential/merged · matrix 1 ชุด: 1) role-mgr-sales → 2) role-mgr-bu `[DEFAULT — รอยืนยัน OQ-10]` (wave plan เขียน "2 สาย" = 2 ขั้น sequential? OQ-10) · เลือกคนต่อ slot

---

## 4. Business Rules
| BR | กติกา | S | ที่มา |
|---|---|---|---|
| BR-01 | แปลงจาก QT ได้เฉพาะสถานะ ตกลง/รอตอบ · ราคาคำนวณใหม่ ณ วันสั่ง · QT → แปลงแล้ว | S-02 | [มติ] OQ-3 |
| BR-02 | ราคา/บรรทัด = price-resolver → trade-agreement-engine (NET แทน / DISC บวก / TOTAL ท้ายบิล) → promo-engine (LINE/FREE/THRESHOLD/COUPON) — ลำดับตายตัว · คำนวณใหม่เมื่อ qty/หน่วย/ช่องทาง/ลูกค้า/คลัง เปลี่ยน | S-04 | [มติ] |
| BR-03 | TA "ไม่ลดซ้ำ" → โปรฯ ส่วนลดบรรทัดข้ามสินค้านั้น · TA ท้ายบิล vs โปรฯ ท้ายบิล: โปรฯ ชนะถ้าติด (OQ-11) | S-04 | [มติ] |
| BR-04 | ของแถมจากโปรฯ = บรรทัด is_free ราคา 0 แก้ไม่ได้ · หายเมื่อปิดโปรฯ/qty ไม่ถึง | S-04, S-06 | |
| BR-05 | ปิด TA / ปิดโปรฯ รายตัว ทำได้ที่การ์ดปรับราคา · audit · ผู้อนุมัติเห็น (สิทธิ์/เหตุผล OQ-4) | S-05, S-06 | [AI-DRAFT] |
| BR-06 | แก้ราคาด้วยมือ (allowPriceOverride) → override flag · เหตุผลบังคับก่อนบันทึก/ส่ง · ผู้อนุมัติเห็นบรรทัดที่แก้ | S-07 | [AI-DRAFT] OQ-1 |
| BR-07 | totals: ก่อน VAT → VAT → หลัง VAT → ท้ายบิล → คูปอง → สุทธิ · VAT 3 โหมด mutually exclusive ต่อบรรทัด | S-08, S-09 | B2 |
| BR-08 | goods: ตรวจ ATP (onhand−reserved ต่อคลัง) · service: ไม่ตรวจ/ไม่จอง/ไม่ตัดคลัง | S-10, S-11 | [มติ 18 ส.ค.] |
| BR-09 | ATP ไม่พอ → บล็อกขั้น 3 และบล็อกส่งอนุมัติ (re-check ณ ตอนกด) · alert สัดส่วน | S-11 | [มติ 18 ส.ค.] |
| BR-10 | เครดิต exposure = ยอดสุทธิ − ส่วนที่จ่ายก่อน (prepay=0 · deposit=ส่วนเหลือ · cash=0) · คงเหลือ = วงเงิน − AR − openSO | S-14 | [มติ] |
| BR-11 | exposure > คงเหลือ → hard control: ส่งอนุมัติไม่ได้ (บันทึกร่างได้) · ขอเพิ่มวงเงินที่ ⑧ | S-14 | [มติ] OQ-5 |
| BR-12 | ยืนยัน → openSO += exposure · ยกเลิก/close short → คืน · รับชำระ → AR ลด | S-16, S-23, S-30 | |
| BR-13 | ยืนยัน (อนุมัติครบ) → reserve ทุกบรรทัด goods ที่คลัง: จอง = min(need, ATP) · เหลือ = backorder + notify | S-12 | [มติ 18 ส.ค.] |
| BR-14 | retry จอง backorder ได้ · DN ตัดจ่ายจาก reserved (partial=ครึ่ง mock) · DN ครบ = released | S-13, S-24 | |
| BR-15 | ยกเลิก / close short → release reserve · พัก → คงจอง (holdKeepsReserve) | S-27, S-30 | OQ-9 |
| BR-16 | มี DN แล้ว ยกเลิก SO ไม่ได้ → RMA/CN | S-28, S-30 | [มติ] |
| BR-17 | paymentPlan จาก term × ยอดสุทธิ × วันยืนยัน/วันส่ง · RV จับคู่งวด FIFO · สถานะงวด รอ/บางส่วน/ชำระแล้ว/เกินกำหนด | S-19..S-23 | F-PAYTERM |
| BR-18 | Warehouse trigger: after_full → DN ล็อกจนชำระครบ · after_deposit → ล็อกจนรับมัดจำ · immediate | S-20, S-21 | F-PAYTERM |
| BR-19 | linkage.payment auto = จากแผน (paid ≥ total) · manual = ผู้ใช้ตั้ง | S-23, S-29 | |
| BR-20 | สถานะ derive: ยืนยัน → กำลังส่ง/บิล (partial) → ส่งครบ → วางบิลครบ → **ปิดอัตโนมัติ** เมื่อ ส่ง+บิล+ชำระ ครบ | S-31 | [มติ] |
| BR-21 | RMA หลัง DN เท่านั้น → รับเข้าคลัง + CN · full return → สถานะ รับคืน/ลดหนี้ | S-28 | |
| BR-22 | Module Linkage dual-mode ต่อแกน (Sales Configuration) · manual override ต้องมีอ้างอิง (audit) | S-29 | CUBE §7 |
| BR-DOA-01..07 | ส่งเฉพาะร่าง · resolve→freeze ไม่มีวงเงิน · ไม่อนุมัติ→ร่าง append-only · SoD · เลือกคนทุก slot · sequential · เหตุผลบังคับ | S-15..S-18 | [/doa-declaration] |
| BR-23 | audit append-only ทุกเหตุการณ์ (รวม linkage events จากระบบ) | ทุก S | กติกากลาง |

---

## 5. State Machine
`ร่าง` → `รออนุมัติ` → `ยืนยัน·รอจัดส่ง` → `กำลังส่ง/บิล` → `ส่งครบ` → `วางบิลครบ` → `ปิดแล้ว` · แขนง: `พัก(hold)` ⇄ (จาก ยืนยัน/กำลังส่ง) · `ยกเลิก` (ร่าง/รออนุมัติ/ยืนยัน/พัก · ก่อน DN) · `รับคืน/ลดหนี้` (หลัง DN) · close short (กำลังส่ง → ส่งครบ)
| จาก | ไป | ใครกด | เงื่อนไข |
|---|---|---|---|
| — | ร่าง | ผู้ใช้ | สร้าง / QT / สำเนา / ตีกลับ |
| ร่าง | รออนุมัติ | ผู้ส่ง | validate 5 ขั้น · ATP ผ่าน · เครดิตผ่าน · slot ครบ |
| รออนุมัติ | (ขั้นถัดไป) / ยืนยัน | คนขั้นปัจจุบัน | อนุมัติ · ครบ = reserve + openSO + WH/AR |
| รออนุมัติ | ร่าง | คนขั้นปัจจุบัน | ไม่อนุมัติ+เหตุผล |
| ยืนยัน/กำลังส่ง | พัก | ผู้จัดการ | เหตุผล · WH หยุด |
| พัก | ยืนยัน | ผู้จัดการ | ปลดพัก |
| ร่าง/รออนุมัติ/ยืนยัน/พัก | ยกเลิก | ผู้ใช้/ผู้จัดการ | เหตุผล · ไม่มี DN · ปล่อยจอง+เครดิต |
| ยืนยัน → กำลังส่ง → ส่งครบ → วางบิลครบ → ปิด | ระบบ (linkage/plan) | DN · INV · RV ครบ |
| กำลังส่ง | ส่งครบ (close short) | ผู้จัดการ | เหตุผล · ปล่อยจองที่เหลือ |
| ส่งครบ/วางบิล | รับคืน/ลดหนี้ | ระบบ (RMA) | RMA + CN |
Sub-state ต่อบรรทัด: reserve พร้อมจอง/จองครบ/บางส่วน+backorder/ปล่อยแล้ว/บริการ · งวดชำระ: รอ/บางส่วน/ชำระแล้ว/เกินกำหนด · Warehouse gate: ปลด/ล็อกรอมัดจำ/ล็อกรอชำระเต็ม

---

## 6. Actions ต่อหน้า
| หน้า | action |
|---|---|
| list | ค้นหา (เลขที่/ลูกค้า/PO/QT/rep/สินค้า) · filter สถานะ 8 / จัดส่ง / การจ่าย / rep · sort · pagination · row menu (ดู/แก้/สำเนา/ยกเลิก) · export CSV · สร้างใบสั่งขาย |
| create ขั้น 1 | สร้างใหม่ / จากใบเสนอราคา (search+filter+Enter · ใช้ใบนี้) |
| ขั้น 2 | ข้อมูลหลัก 16 ช่อง · การ์ดข้อมูลจาก QT · การ์ดแผนการชำระ preview |
| ขั้น 3 | line editor B2 (เพิ่ม/ลบ/แถวขยาย lean · หน่วย cascade · แก้ราคา/ใช้ราคาระบบ) · alert สต๊อก · การ์ดปรับราคา ①②③ (toggle TA · toggle โปรฯ · คูปอง) · ท้ายบิล · summary + เครดิตคงเหลือ · คำนวณราคาใหม่ |
| ขั้น 4 | แนบไฟล์ (Doc Center) |
| ขั้น 5 | การ์ดข้อมูล / แผนการชำระ / เหตุผลแก้ราคา / รายการ+totals / สต๊อกและการจอง / DOA / ไฟล์แนบ · บันทึกแบบร่าง · บันทึกและส่งอนุมัติ |
| landing header | ตามสถานะ: ยกเลิก(link)·แก้ไข·ส่งอนุมัติ / ไม่อนุมัติ·อนุมัติ / พัก·ยกเลิก / ปลดพัก · icon สำเนา·พิมพ์·ดาวน์โหลด·ปิด |
| แท็บ รายละเอียด | sections PO-style + เอกสารแนบ + ข้อมูลระบบ |
| แท็บ สต๊อกและการส่ง | ตารางจองต่อบรรทัด · retry จอง · Warehouse gate · DN (mock) · RMA (mock) · ปิดยอดค้าง |
| แท็บ เครดิต·บิล·ชำระ | เครดิต+ขอเพิ่มวงเงิน · TA ผูกพัน/rebate · AR วางบิล (mock) + ครบกำหนด · แผนการชำระ + บันทึกรับชำระ (RV mock · payment method) · เป้า/คอมมิชชั่น · linkage manual |
| แท็บ PDF Preview · ลายเซ็น/อนุมัติ (timeline v8 · action inline · history) · ประวัติ | |

---

## 7. Data behaviour
เลขรัน SO- (Document Config) · soft-ref ทุก master (LD-4C-02) · ไม่มี hard delete · audit append-only (รวม event จาก Warehouse/AR/Finance) · freeze approval_chain · snapshot ราคา/ที่มา ต่อบรรทัด ณ ยืนยัน (ราคาบัญชี/TA/โปรฯ ที่เปลี่ยนภายหลังไม่กระทบใบเดิม) · reserve/plan derive ณ runtime · สถานะ derive จาก linkage/plan · ยืนยันแล้วล็อกแก้ไข

---

## 8. Mock Data Spec (prove)
SO-0201 ทองดี (TA net + free + promo 14% · DN บางส่วน · INV บางส่วน · N30) · SO-0202 Tops (TA net×2 + disc + ท้ายบิล + service SV-9001 · ยืนยัน · N60) · SO-0203 หัวหิน รออนุมัติ (สาย มานพ→ศิริพร · เครดิตเกินก่อนหน้า) · SO-0204 BestBuy ร่าง DEP50 (แผนมัดจำ) · SO-0198 ปิดแล้ว (RV ครบ) · SO-0199 ยกเลิก · SO-0200 พัก backorder (ยาสีฟัน ATP 34) · QT 6 ใบ 4 สถานะ · Payment term 11 · Payment method 7 · Inventory 2 คลัง · บริการ 2 · persona 3 · unit test/e2e 14 flow PASS

---

## 9. Edges + Hotspot
| ทิศ | คู่ | ปลายทาง |
|---|---|---|
| เข้า | QT ⑫ | แปลง · QT status |
| เข้า | Customer ⑦ · Credit ⑧ · Salesperson ⑩ · Campaign ⑬ | defaults · exposure/openSO/AR · rep · แคมเปญ |
| เข้า | Price List ⑪ → TA ⑭ → Promo ⑮ | 3 engines · TA commitment/rebate นับจากใบที่ยืนยัน · โปรฯ usage/งบ |
| เข้า | Item Master · Inventory | goods/service · ATP/reserve/release |
| เข้า | F-PAYTERM · F-PAYMETHOD | plan/trigger · RV |
| เข้า/ออก | DOA · Employee | DOA-SALES-SO |
| ออก | Warehouse S5 | DN ตาม reserve+trigger · pickup |
| ออก | AR S6 · Finance | INV/ครบกำหนด · RV/ค่าธรรมเนียม · GL |
| ออก | RMA/CN S7 | หลัง DN |
| ออก | Dashboard/Commission S8 | ยอดก่อน VAT · อัตราตามช่องทาง |
| ออก | ENG-NOTIFY | doa_* · so.confirmed · so.backorder · so.hold · so.cancelled · so.closed |
| ออก | Doc Center · Document Config | แนบไฟล์ · เลขรัน |

---

## 10. OQ register
| # | ประเด็น | เจ้าภาพ |
|---|---|---|
| OQ-1 | แก้ราคาด้วยมือ: ใครมีสิทธิ์ · ต้อง DOA เพิ่มขั้นไหม (ตอนนี้แค่เหตุผล+ผู้อนุมัติเห็น) | Strike |
| OQ-2 | สิทธิ์แต่ละ role: สร้าง/ยกเลิกใบยืนยัน/พัก/ปิดยอดค้าง/รับชำระ | Strike |
| OQ-3 | แปลง QT: ราคาใหม่ ณ วันสั่ง (ตอนนี้) หรือล็อกราคา QT · QT ที่แปลงแล้วแก้ไม่ได้ | Strike |
| OQ-4 | ปิด TA / ปิดโปรฯ ด้วยมือ ต้องเหตุผล/สิทธิ์ไหม | Strike |
| OQ-5 | เครดิตเกิน hard control ทุก role หรือ soft สำหรับผู้จัดการ · ขอวงเงินชั่วคราวใน flow | Strike |
| OQ-6 | ลูกค้ามารับเอง (pickup) — Warehouse ออก DN แบบไหน · ตัดสต๊อกตอนไหน | Strike/WH |
| OQ-7 | แก้ SO ที่ยืนยันแล้ว: ห้ามเด็ดขาด (ตอนนี้) หรืออนุญาต amendment ผ่าน DOA | Strike |
| OQ-8 | ของแถม/ส่วนลดที่ไม่มีในโปรฯ/TA ให้ทำได้ไหม (manual free item + DOA) | Strike |
| OQ-9 | พัก (hold) คงจองสต๊อก (ตอนนี้) หรือปล่อย · backorder = WH ทยอยส่งอัตโนมัติหรือรอ retry · จอง FIFO ข้าม SO | Strike/WH |
| OQ-10 | สาย DOA-SALES-SO: 1) ผู้จัดการฝ่ายขาย → 2) หัวหน้า BU · wave plan "2 สาย" = 2 ขั้น sequential? | Strike |
| OQ-11 | ท้ายบิลจาก TA และโปรฯ ชนกัน ใครชนะ/รวม | Strike |
| OQ-12 | จองสต๊อกตอน "ยืนยัน" (ตอนนี้) หรือตอน "ส่งอนุมัติ" กัน race · ATP นับของกำลังเข้า (PO/GRN) ไหม | Strike/WH |
| OQ-13 | บริการตัดจ่ายเมื่อวางบิลหรือเมื่อยืนยัน · แสดงในรายงานสต๊อกไหม | Accounting |
| OQ-14 | มัดจำ: ออกใบเสร็จ/ใบกำกับมัดจำที่ AR ตอนไหน · ส่วนลดจ่ายเร็ว 2/10 ใครคำนวณ · เช็ค settle T+3 นับชำระเมื่อไหร่ · installment นับจาก DN แรก/สุดท้าย | Accounting |
| OQ-15 | ปิดอัตโนมัติเมื่อชำระครบ (linkage payment auto) — Finance เชื่อมจริงหรือ manual ในเฟสแรก | Strike/Finance |
| OQ-16 | ลงทะเบียน ENG: `price-resolver` · `trade-agreement-engine` · `promo-engine` · `payment-plan-engine` · `inventory-reserve` | Architect |
| OQ-17 | Customer Master ⑦: ต้องมี "ที่อยู่ออกใบกำกับ" แยกจากที่อยู่ส่ง + เลขผู้เสียภาษี/สาขา (LD ส่งกลับ ⑦) | Chin/Strike |

---

## 11. Coverage Matrix
| S | BR | transition | UI | FN |
|---|---|---|---|---|
| S-01 | — | —→ร่าง | ขั้น 1–2 | FN-01, FN-02 |
| S-02 | BR-01 | —→ร่าง | ขั้น 1 QT picker | FN-03 |
| S-03 | — | | ขั้น 2 | FN-04 |
| S-04 | BR-02, BR-03, BR-04, BR-07 | | ขั้น 3 line editor + การ์ดปรับราคา | FN-05, FN-06, FN-07 |
| S-05 | BR-05 | | toggle TA | FN-08 |
| S-06 | BR-04, BR-05 | | toggle โปรฯ · คูปอง | FN-09, FN-10 |
| S-07 | BR-06 | | override · เหตุผลขั้น 5 | FN-11 |
| S-08 | BR-07 | | ท้ายบิล | FN-12 |
| S-09 | BR-07 | | แถวขยาย VAT | FN-13 |
| S-10 | BR-08 | | บริการ | FN-14 |
| S-11 | BR-08, BR-09 | ร่าง (บล็อก) | alert สต๊อก · ปุ่ม disabled | FN-15 |
| S-12 | BR-13 | รออนุมัติ→ยืนยัน | แท็บสต๊อก | FN-16 |
| S-13 | BR-14 | | retry จอง | FN-17 |
| S-14 | BR-10, BR-11 | ร่าง (บล็อก) | hard-warn · disabled | FN-18 |
| S-15 | BR-DOA-01, BR-DOA-02, BR-DOA-05, BR-09, BR-11 | ร่าง→รออนุมัติ | modal ส่ง | FN-19, FN-20 |
| S-16 | BR-DOA-06, BR-12, BR-13 | →ยืนยัน | อนุมัติ · timeline | FN-21, FN-22 |
| S-17 | BR-DOA-03, BR-DOA-07 | →ร่าง | modal ไม่อนุมัติ | FN-23 |
| S-18 | BR-DOA-04 | | | FN-24 |
| S-19 | BR-17 | | แผนการชำระ | FN-25 |
| S-20 | BR-17, BR-18, BR-10 | | gate PREPAY | FN-26 |
| S-21 | BR-17, BR-18, BR-10 | | gate DEP | FN-27 |
| S-22 | BR-17 | | INST/PARTIAL | FN-28 |
| S-23 | BR-17, BR-19, BR-12 | | modal RV | FN-29 |
| S-24 | BR-14, BR-18 | ยืนยัน→กำลังส่ง→ส่งครบ | DN mock | FN-30 |
| S-25 | — | | pickup | FN-31 |
| S-26 | BR-20 | →วางบิลครบ | INV mock · ครบกำหนด | FN-32 |
| S-27 | BR-15 | กำลังส่ง→ส่งครบ | ปิดยอดค้าง | FN-33 |
| S-28 | BR-16, BR-21 | →รับคืน | RMA mock | FN-34 |
| S-29 | BR-19, BR-22 | | manual linkage | FN-35 |
| S-30 | BR-12, BR-15, BR-16 | พัก/ยกเลิก | modals | FN-36, FN-37 |
| S-31 | BR-20 | →ปิด | auto · เป้า/คอม | FN-38, FN-39 |
| S-32 | — | | สำเนา · แก้ร่าง · แนบ · PDF | FN-40, FN-41, FN-42 |
| S-33, S-34, S-35 | — | ไม่รองรับ | — | — |
| ทุก S | BR-23 | | audit | FN-94 |
ผ่าน: ทุก BR/transition ถูกอ้าง · ทุก S มี FN (ไม่รองรับระบุชัด) · OB-1..18 ถูกอ้าง
