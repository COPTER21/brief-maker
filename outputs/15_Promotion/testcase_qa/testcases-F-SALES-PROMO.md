# AI Test Cases — F-SALES-PROMO Promotion

ชุดทดสอบ Markdown สำหรับ browser-use/vision agent ยึด HTML `Promotion.html` เป็น anchor หน้าจอ และ FRD Pack เป็น contract ระบบ

## Meta

| Field | Value |
|---|---|
| Feature ID | F-SALES-PROMO |
| Version | 1.0 · 2026-08-18 |
| App entry | เปิด `Promotion.html` |
| Routes | `#/promotions` |
| Sources | BRD, FRD_Pack ทุกไฟล์, Promotion.html, DOA brief |
| Cases | 55 cases · 7 groups |
| Anchor priority | HTML verbatim → 01_UI → v8 microcopy |
| Note | persona selector is prototype-only; it simulates IAM roles |

## Coverage

| Group | Cases | Priority |
|---|---:|---|
| L — list/filter/overlay | 8 | medium/high |
| C — create/edit/validation | 12 | high |
| A — approval/lifecycle | 10 | critical |
| S — simulator/calculation | 12 | critical |
| P — permission/security | 4 | critical |
| X — cross-module/locks | 6 | high |
| N — concurrency/idempotency/performance | 3 | high |

## Coverage Ledger

### FR / Acceptance (06_TESTS)

| Item | Cases |
|---|---|
| AT-01 create draft | TC-C01, TC-C02 |
| AT-02 LINE rule/boundary | TC-C03, TC-C04 |
| AT-03 FREE rule | TC-C05 |
| AT-04 THRESHOLD | TC-C06, TC-C07 |
| AT-05 BUNDLE/coupon | TC-C08, TC-C09, TC-C10 |
| AT-06 overlap submit | TC-A01, TC-A02 |
| AT-07 sequential approve | TC-A03, TC-A04 |
| AT-08 reject | TC-A05 |
| AT-09 line discount after TA | TC-S01, TC-S10 |
| AT-10 coupon/scope/date | TC-S02, TC-S03, TC-S04 |
| AT-11 free goods | TC-S05 |
| AT-12 threshold | TC-S06, TC-S07 |
| AT-13 bundle | TC-S08 |
| AT-14 priority/exclusive | TC-S09 |
| AT-15 lifecycle | TC-A06..TC-A09 |
| AT-16 usage/budget/quota | TC-S11, TC-S12, TC-X03 |
| AT-17 edit vs copy | TC-C11, TC-C12 |
| AT-18 no customer scope | TC-P04 |
| AT-19 audit | TC-A10 |
| AT-20 frozen DOA | TC-X05 |
| AT-21 concurrency | TC-N01 |
| AT-22 double submit/usage | TC-N02 |
| AT-23 auth/permission | TC-P01..TC-P03 |
| AT-24 decimal | TC-S01, TC-S06, TC-S08 |

### Business Rules

| Rule | Cases |
|---|---|
| BR-PROMO-01 | TC-S01, TC-X01 |
| BR-PROMO-02 | TC-S02..TC-S04, TC-S11 |
| BR-PROMO-03 | TC-C03, TC-C04, TC-S01, TC-S10 |
| BR-PROMO-04 | TC-C05, TC-S05, TC-X04 |
| BR-PROMO-05 | TC-C06..TC-C08, TC-S06..TC-S08 |
| BR-PROMO-06 | TC-S09 |
| BR-PROMO-07/08 | TC-A01, TC-A02 |
| BR-PROMO-09/10 | TC-S11, TC-S12, TC-X03 |
| BR-PROMO-11 | TC-C11, TC-C12 |
| BR-PROMO-12 | TC-A06..TC-A09 |
| BR-PROMO-13/14 | TC-S05, TC-X03, TC-X04 |
| BR-PROMO-15 | TC-C09, TC-C10, TC-S02 |
| BR-PROMO-16 | TC-P04 |
| BR-PROMO-17 | TC-A10, TC-X03 |
| BR-DOA-01..07 | TC-A01..TC-A05, TC-P01..TC-P03, TC-X05 |

### Edge / Error Codes

| Item | Cases |
|---|---|
| EC-01 / ERR_VALIDATION_FAILED | TC-C02, TC-C04, TC-C07..TC-C10 |
| EC-02 / BR_PROMO_OVERLAP_ACK_REQUIRED | TC-A01, TC-A02 |
| EC-03 / ERR_SOD_VIOLATION | TC-P01 |
| EC-04 / BR_PROMO_REASON_REQUIRED | TC-A05..TC-A08 |
| EC-05 coupon skip | TC-S02 |
| EC-06 TA no-repeat | TC-S10 |
| EC-07 exclusive | TC-S09 |
| EC-08 budget/quota | TC-S11, TC-S12 |
| EC-09 ATP ownership | TC-X04 |
| EC-10 inactive master snapshot | TC-X06 |
| EC-11 invalid edit/state | TC-C11, TC-A09 |
| EC-12 duplicate usage | TC-N02, TC-X03 |
| EC-AI-01 / ERR_VERSION_CONFLICT | TC-N01 `[AI-DEFAULT]` |
| EC-AI-02 idempotency | TC-N02 `[AI-DEFAULT]` |
| EC-AI-03 frozen DOA | TC-X05 `[AI-DEFAULT]` |
| EC-AI-04 / 401/403 | TC-P02, TC-P03 `[AI-DEFAULT]` |
| EC-AI-05 decimal | TC-S01, TC-S06, TC-S08 `[AI-DEFAULT]` |
| ERR_PROMOTION_NOT_FOUND | TC-P03 |
| ERR_DUPLICATE_COUPON | TC-C10 |
| BR_PROMO_INVALID_TRANSITION | TC-A09 |
| ENG_ERR_INVALID_INPUT/RULE | TC-X01 |

### Permission Matrix

| Cell | Cases |
|---|---|
| Officer view/simulate/create/edit/submit/copy/export allow | TC-L01, TC-C01, TC-A01, TC-S01 |
| Officer approve/manage deny | TC-P01, TC-P02 |
| Sales Manager current approve/manage allow | TC-A03, TC-A06..TC-A08 |
| Sales Manager non-current approve deny | TC-P02 |
| BU Head current approve allow | TC-A04 |
| BU Head create/edit/manage deny | TC-P03 |
| Invoice service usage allow / human deny | TC-X03, TC-P03 |

### UI States / Events / State Machine

| Item | Cases |
|---|---|
| loaded/search/filter/sort/empty/export | TC-L01..TC-L07 |
| Esc portal→modal→drawer | TC-L08 |
| draft→pending→active/scheduled | TC-A01..TC-A04 |
| pending→draft reject | TC-A05 |
| active⇄paused | TC-A06, TC-A07 |
| valid states→ended_early | TC-A08 |
| forbidden transition | TC-A09 |
| append-only history | TC-A10 |

### Cross-Module (XT)

| XT | Case |
|---|---|
| XT-01 Price List/TA | TC-X01 |
| XT-02 QT/SO freeze | TC-X02 |
| XT-03 Invoice/GL/usage | TC-X03 |
| XT-04 Inventory ATP | TC-X04 |
| XT-05 DOA/Employee | TC-X05 |
| XT-06 master references | TC-X06 |

### Scope Locks

| Lock | Case |
|---|---|
| LOCK-PROMO-01 HTML fidelity | TC-L01, TC-L08 |
| LOCK-PROMO-02 no customer-specific | TC-P04 |
| LOCK-PROMO-03 Item Master truth | TC-X06 |
| LOCK-PROMO-04 DOA no amount/config/SoD | TC-A01, TC-P01, TC-X05 |
| LOCK-PROMO-05 ATP at SO | TC-X04 |
| LOCK-PROMO-06 usage from Invoice | TC-X03 |
| LOCK-PROMO-07 Campaign future | — ข้าม: นอกขอบเขตใบเซ็น; verify ว่าไม่มี UI/API ด้วย TC-P04 |

## Data Sets

### A — valid LINE draft

| Field | Value |
|---|---|
| name | โปรเปิดตัวชาเขียว 10% |
| type | ส่วนลดสินค้า |
| scope | ทุกลูกค้า |
| from | วันนี้ |
| priority | 25 |
| coupon | ว่าง |
| GL | 4110-02 ตาม mock picker |
| target | หมวด BEV |
| mode/value/min | 10% / 12 หน่วยฐาน |

### B — valid FREE / THRESHOLD / BUNDLE

| Set | Values |
|---|---|
| B-FREE | น้ำดื่ม 10 ลัง แถมน้ำดื่ม 1 ลัง, repeat |
| B-THRESHOLD | 20,000→3%; 50,000→5% |
| B-BUNDLE | สินค้า 2 รายการไม่ซ้ำ, qty 1, ราคา bundle ต่ำกว่ารวม 100 บาท |

### C — invalid values

| Name | Value |
|---|---|
| priority-low/high | 0 / 1000 |
| pct-over | 100.01 |
| coupon-short/long/bad | AB / 21 chars / `WELCOME 100` |
| tier-bad | 50,000 then 20,000 |
| bundle-bad | duplicate product or price equal list total |

### D — simulator seeds

| Seed | Value |
|---|---|
| default wholesale cart | ทองดี · ค้าส่ง · น้ำดื่ม 10 ลัง + ชาเขียว 48 ขวด + มันฝรั่ง 24 ซอง |
| coupon cart | channel เว็บไซต์/ออนไลน์ · coupon WELCOME100 · amount after prior line discount ≥500 |
| TA no-repeat line | one line has `promoAllowed=false` after TA net |

## Test Cases

## Group L — List, Filter, Overlay

### TC-L01 — เปิดหน้ารายการมาตรฐาน (happy)
- group: list · ความสำคัญ: สูง · trace: FN-90, LOCK-PROMO-01
- actor: Sales/Marketing Officer
- Setup: role=officer · seed=mock promotions ทั้งสถานะ · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: เห็นหัวข้อ รายการ แท็บ ตัวกรอง และปุ่มหลักตาม HTML

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/promotions` | — | route คง `#/promotions`; เห็น “ทดสอบตะกร้า”, “Export CSV”, “สร้างโปรโมชัน” | ☐ |
| 2 | VERIFY แท็บสถานะด้านบนรายการ | — | เห็น 7 แท็บ: ทั้งหมด, กำลังใช้, รอถึงวันเริ่ม, รออนุมัติ, ร่าง, ระงับชั่วคราว, สิ้นสุดแล้ว | ☐ |
| 3 | VERIFY ตารางรายการ | — | หนึ่งโปรโมชันต่อหนึ่งแถว; สินค้า/หน่วยไม่ล้นทับคอลัมน์อื่น | ☐ |

### TC-L02 — ค้นหาด้วยรหัส ชื่อ คูปอง (happy)
- group: list · ความสำคัญ: กลาง · trace: FN-90
- actor: Officer
- Setup: role=officer · seed=PM-2026-015 + WELCOME100 · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: แต่ละคำค้นคืนแถวที่ตรงเท่านั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `PM-2026-015` → ช่องค้นหา | — | เห็นแถวรหัส PM-2026-015 | ☐ |
| 2 | TYPE `WELCOME100` → ช่องค้นหา | — | เห็นโปรโมชันคูปอง WELCOME100 | ☐ |
| 3 | TYPE `คำที่ไม่มีจริง` → ช่องค้นหา | — | เห็น empty state ไม่พบรายการ; ไม่มีแถวเก่าค้าง | ☐ |

### TC-L03 — กรองชนิดทุกค่า (parameterized)
- group: list · ความสำคัญ: กลาง · trace: FN-90
- actor: Officer
- Setup: role=officer · seed=อย่างน้อยหนึ่งรายการต่อ 4 ชนิด · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: LINE/FREE/THRESHOLD/BUNDLE แต่ละค่าคืนเฉพาะชนิดนั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT แต่ละค่า → ตัวกรองชนิด | ส่วนลดสินค้า / ซื้อ X แถม Y / ยอดใบถึงเกณฑ์ / ชุดราคาพิเศษ | ทุกแถวที่เห็นตรงชนิดที่เลือก; dropdown เลือกได้จริง | ☐ |
| 2 | SELECT ทุกชนิด → ตัวกรองชนิด | — | รายการกลับมาครบตามแท็บปัจจุบัน | ☐ |

### TC-L04 — กรองขอบเขตทุกค่า (regression)
- group: list · ความสำคัญ: สูง · trace: FN-90, FN-03
- actor: Officer
- Setup: role=officer · seed=all/group/channel records · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: ทุกลูกค้า/กลุ่มลูกค้า/ช่องทางเลือกได้ ไม่ค้าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT “ทุกลูกค้า” → ตัวกรองขอบเขต | — | เห็นเฉพาะ scope ทุกลูกค้า | ☐ |
| 2 | SELECT “กลุ่มลูกค้า” → ตัวกรองขอบเขต | — | เห็นเฉพาะกลุ่มลูกค้า | ☐ |
| 3 | SELECT “ช่องทางการขาย” → ตัวกรองขอบเขต | — | เห็นเฉพาะช่องทาง | ☐ |
| 4 | SELECT “ทุกขอบเขต” → ตัวกรองขอบเขต | — | เห็นทุก scope | ☐ |

### TC-L05 — แท็บสถานะทุกค่า
- group: list · ความสำคัญ: กลาง · trace: FN-90, lifecycle
- actor: Officer
- Setup: role=officer · seed=records ครบสถานะ · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: แต่ละแท็บไม่ปนสถานะ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ทีละแท็บสถานะ | 7 แท็บ | ทุกแถวมีป้ายสถานะตรงกับแท็บ; แท็บ active ชัด | ☐ |
| 2 | CLICK แท็บที่ seed ไม่มีรายการ | — | เห็น empty state; toolbar ยังใช้งานได้ | ☐ |

### TC-L06 — Sort และ reset filter
- group: list · ความสำคัญ: กลาง · trace: FN-90
- actor: Officer
- Setup: role=officer · seed=หลาย priority/date/code · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: sort เปลี่ยนลำดับและ reset คืนค่าเริ่มต้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT แต่ละตัวเลือก → sort | ตาม dropdown ที่เห็น | ลำดับแถวเปลี่ยนตรงคำอธิบาย | ☐ |
| 2 | CLICK ปุ่ม/คำสั่งล้างตัวกรอง | — | search/filter กลับ default; รายการกลับครบ | ☐ |

### TC-L07 — Export CSV ตาม filter
- group: list · ความสำคัญ: กลาง · trace: FN-92
- actor: Officer
- Setup: role=officer · seed=active ≥2 · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: ดาวน์โหลด promotions.csv และมีเฉพาะแถวปัจจุบัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ “กำลังใช้” | — | เห็นเฉพาะรายการกำลังใช้ | ☐ |
| 2 | CLICK “Export CSV” | — | ดาวน์โหลด `promotions.csv`; toast `Export CSV แล้ว` | ☐ |
| 3 | VERIFY เนื้อหาไฟล์ดาวน์โหลด | — | header มี code/name/type/scope/status; ไม่มีรายการสถานะอื่น | ☐ |

### TC-L08 — Esc chain และ dropdown scroll (regression)
- group: overlay · ความสำคัญ: สูง · trace: FN-95, LOCK-PROMO-01
- actor: Officer
- Setup: role=officer · seed=products มากกว่าความสูง menu · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: Esc ปิดชั้นบนสุดทีละชั้นและ menu scroll/select ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “ทดสอบตะกร้า” | — | drawer simulator เปิด | ☐ |
| 2 | CLICK ช่องค้นหาเพิ่มสินค้า | — | dropdown portal เปิดเหนือ drawer | ☐ |
| 3 | VERIFY เลื่อนรายการ dropdown | — | รายการเลื่อนได้; focus/เมนูไม่หาย | ☐ |
| 4 | PRESS Esc | — | dropdown ปิด; drawer ยังเปิด | ☐ |
| 5 | PRESS Esc | — | drawer ปิด; กลับรายการ | ☐ |

## Group C — Create, Edit, Validation

### TC-C01 — สร้าง LINE draft ครบ 3 ขั้น (happy)
- group: create · ความสำคัญ: สูง · trace: AT-01, US-01, FN-01/02/04
- actor: Officer
- Setup: role=officer · seed=active Item/GL/Employee refs · files=—
- Start: OPEN `#/promotions`
- ชุดข้อมูล: A
- ผ่านเมื่อ: draft ใหม่แสดงใน list/detail และมีค่าครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “สร้างโปรโมชัน” | — | drawer เปิด step “ชนิดและขอบเขต” | ☐ |
| 2 | TYPE/SELECT ข้อมูล step 1 | Data A | ช่องสะท้อนค่า; scope “ทุกลูกค้า” | ☐ |
| 3 | CLICK “ถัดไป” | — | เปิด step “เงื่อนไข” | ☐ |
| 4 | SELECT/TYPE rule ส่วนลดสินค้า | Data A | แสดงสรุป 10% หมวด BEV ขั้นต่ำ 12 | ☐ |
| 5 | CLICK “ถัดไป” | — | เปิด “ตรวจสอบและยืนยัน”; สรุปค่าตรง | ☐ |
| 6 | CLICK “บันทึกร่าง” | — | toast `สร้างโปรโมชันสำเร็จ (ร่าง)`; detail ป้าย “ร่าง” | ☐ |

### TC-C02 — required fields ต่อ step (negative)
- group: validation · ความสำคัญ: สูง · trace: VR-01, ERR_VALIDATION_FAILED
- actor: Officer
- Setup: role=officer · seed=— · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: ฟอร์มไม่ข้าม step และ toast ตรง source

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “สร้างโปรโมชัน” | — | step 1 เปิด | ☐ |
| 2 | CLICK “ถัดไป” โดยไม่กรอก required | — | อยู่ step 1; field error ปรากฏ; toast `กรุณากรอกข้อมูลให้ครบถ้วน` | ☐ |
| 3 | TYPE/SELECT ให้ครบยกเว้น GL | — | GL ยังแสดง required/error เมื่อไปต่อ | ☐ |

### TC-C03 — LINE amount/base-UOM (happy)
- group: rule · ความสำคัญ: สูง · trace: BR-PROMO-03, FN-04
- actor: Officer
- Setup: role=officer · seed=product มีหลาย UOM/factor · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: editor เก็บจำนวนขั้นต่ำฐานและโหมดบาทได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “สร้างโปรโมชัน” → SELECT “ส่วนลดสินค้า” | — | step editor ตรงชนิด | ☐ |
| 2 | SELECT target “สินค้า” และสินค้าจาก Item Master | — | เห็น code/name จาก picker | ☐ |
| 3 | SELECT โหมด “บาท” → TYPE value/minimum | 5 บาท; 12 หน่วยฐาน | สรุป rule แสดงค่าตรง | ☐ |

### TC-C04 — percentage/priority boundaries (boundary)
- group: validation · ความสำคัญ: สูง · trace: VR-02,VR-04,EC-01
- actor: Officer
- Setup: role=officer · seed=base valid form · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: invalid block; exact min/max valid

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `0` → ลำดับ | — | ไปต่อ/บันทึกไม่ได้ | ☐ |
| 2 | TYPE `1000` → ลำดับ | — | ไปต่อ/บันทึกไม่ได้ | ☐ |
| 3 | TYPE `1` แล้ว `999` → ลำดับ | — | ทั้งสอง boundary ผ่าน validation | ☐ |
| 4 | TYPE `100.01` → ค่าเปอร์เซ็นต์ | — | field error; ไปต่อไม่ได้ | ☐ |
| 5 | TYPE `100` → ค่าเปอร์เซ็นต์ | — | ผ่าน validation | ☐ |

### TC-C05 — FREE_GOODS same-item repeat (happy)
- group: rule · ความสำคัญ: สูง · trace: BR-PROMO-04, FN-05
- actor: Officer
- Setup: role=officer · seed=water product/UOM · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: buy/get ตัวเดียวกันได้และ repeat ถูกบันทึก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT “ซื้อ X แถม Y” → step เงื่อนไข | B-FREE | เห็นช่องสินค้าซื้อ/แถม จำนวน หน่วย repeat | ☐ |
| 2 | SELECT สินค้าเดียวกันทั้งซื้อและแถม | น้ำดื่ม | ไม่มี duplicate error | ☐ |
| 3 | TYPE 10/1 และ TOGGLE ทำซ้ำ | — | summary “ซื้อ 10 ลัง แถม 1 ลัง” และ repeat | ☐ |

### TC-C06 — THRESHOLD valid tiers (happy)
- group: rule · ความสำคัญ: สูง · trace: BR-PROMO-05, FN-06
- actor: Officer
- Setup: role=officer · seed=— · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: เพิ่ม/ลบ tier และสรุปเรียงถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT “ยอดใบถึงเกณฑ์” → step เงื่อนไข | — | เห็นตารางขั้นและปุ่มเพิ่ม | ☐ |
| 2 | TYPE tier 20,000→3% | — | แถวแรกแสดงค่าตรง | ☐ |
| 3 | CLICK เพิ่มขั้น → TYPE 50,000→5% | — | สองแถวเรียง 20k ก่อน 50k | ☐ |
| 4 | CLICK ไอคอนลบท้ายแถวที่ 2 | — | เหลือหนึ่ง tier; layout ไม่พัง | ☐ |

### TC-C07 — THRESHOLD invalid order/duplicate (negative)
- group: validation · ความสำคัญ: สูง · trace: VR-06,EC-01
- actor: Officer
- Setup: role=officer · seed=valid step1 · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: descending/duplicate/empty tiers blocked

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE tiers 50,000 then 20,000 | C:tier-bad | error; ไป step 3 ไม่ได้ | ☐ |
| 2 | TYPE tiers min เท่ากัน | 20,000/20,000 | error; ไปต่อไม่ได้ | ☐ |
| 3 | CLICK ลบทุก tier | — | ต้องมีอย่างน้อยหนึ่งขั้น; error ปรากฏ | ☐ |

### TC-C08 — BUNDLE valid/invalid (boundary)
- group: rule · ความสำคัญ: สูง · trace: VR-07,BR-PROMO-05,FN-07
- actor: Officer
- Setup: role=officer · seed=two active products with list price · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: valid shows saving; duplicate/high price blocks

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT “ชุดราคาพิเศษ” → step เงื่อนไข | — | icon ค้นหาไม่ทับข้อความในช่องสินค้า | ☐ |
| 2 | SELECT สินค้าไม่ซ้ำ 2 รายการและ TYPE ราคา bundle | B-BUNDLE | เห็นประหยัดต่อชุดเป็นจำนวนบวก | ☐ |
| 3 | SELECT สินค้าซ้ำ | C:bundle-bad | error; ไปต่อไม่ได้ | ☐ |
| 4 | TYPE ราคาเท่าราคาตั้งรวม | C:bundle-bad | error; ไปต่อไม่ได้ | ☐ |

### TC-C09 — coupon format boundaries (boundary)
- group: validation · ความสำคัญ: สูง · trace: VR-08,BR-PROMO-15
- actor: Officer
- Setup: role=officer · seed=valid form · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: regex/length exact

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `AB` → คูปอง | — | invalid/บล็อก |
| 2 | TYPE 21 ตัวอักษร → คูปอง | — | invalid/บล็อก |
| 3 | TYPE `WELCOME 100` → คูปอง | — | invalid/บล็อก |
| 4 | TYPE `ABC` แล้วค่า 20 ตัวอักษรถูก format | — | ผ่านทั้ง min/max | ☐ |
| 5 | TYPE `welcome100` → คูปอง | — | ค่าถูก normalize เป็น uppercaseเมื่อบันทึก/สรุป | ☐ |

### TC-C10 — coupon duplicate case-insensitive (negative)
- group: validation · ความสำคัญ: สูง · trace: ERR_DUPLICATE_COUPON,BR-PROMO-15
- actor: Officer
- Setup: role=officer · seed=non-final promotion coupon WELCOME100 · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: duplicate lower/upper blocked

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “สร้างโปรโมชัน” → TYPE `welcome100` → คูปอง | — | duplicate error shown; save/submit blocked | ☐ |
| 2 | VERIFY รายการเดิม PM-2026-015 | — | coupon/value/status ไม่เปลี่ยน | ☐ |

### TC-C11 — แก้ได้เฉพาะร่าง (permission/state)
- group: edit · ความสำคัญ: สูง · trace: BR-PROMO-11,EC-11
- actor: Officer
- Setup: role=officer · seed=one draft + one active · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: draft edit saves; active edit blocked

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวสถานะ “ร่าง” → CLICK “แก้ไข” | — | edit drawer เปิดพร้อมค่าเดิม | ☐ |
| 2 | TYPE ชื่อใหม่ → CLICK บันทึก | — | toast `บันทึกการแก้ไขแล้ว`; detail แสดงชื่อใหม่ | ☐ |
| 3 | CLICK แถวสถานะ “กำลังใช้” → พยายาม CLICK “แก้ไข” | — | ปุ่มไม่มีหรือ toast `แก้ไขได้เฉพาะร่าง — ที่อนุมัติแล้วให้ทำสำเนาออกใหม่` | ☐ |

### TC-C12 — ทำสำเนาล้างค่าที่ต้องล้าง (happy/delta)
- group: copy · ความสำคัญ: สูง · trace: BR-PROMO-11,FN-17
- actor: Officer
- Setup: role=officer · seed=active promotion with coupon, usage and approval · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: new draft preserves rule/scope but clears coupon/usage/approval and start=today

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK active promotion → VERIFY และบันทึก rule/scope/coupon/usage | — | จดค่าต้นทางไว้ | ☐ |
| 2 | CLICK “ทำสำเนา” | — | create drawer เปิด; ชื่อมี `(สำเนา)` | ☐ |
| 3 | VERIFY fields ของสำเนา | — | rule/scope ตรง step1; coupon ว่าง; start วันนี้; approval/usage ไม่ติดมา | ☐ |
| 4 | CLICK “บันทึกร่าง” | — | ได้รหัสใหม่ สถานะ “ร่าง”; ต้นทางไม่เปลี่ยน | ☐ |

## Group A — Approval and Lifecycle

### TC-A01 — overlap ต้อง acknowledge ก่อนส่ง (negative)
- group: approval · ความสำคัญ: critical · trace: BR-PROMO-07/08, BR-DOA-01/05
- actor: Officer
- Setup: role=officer · seed=draft overlaps active same type/scope/target/date · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: no ack blocked; conflict details visible

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK draft → CLICK “ส่งอนุมัติ” | — | modal แสดง conflict code, priority, exclusive and approver slots | ☐ |
| 2 | SELECT ผู้อนุมัติครบทุกขั้น | candidates not submitter | slots show avatar + position + name | ☐ |
| 3 | CLICK ปุ่มยืนยันส่งโดยยังไม่ติ๊ก overlap | — | toast `ต้องยืนยันการทับซ้อนก่อนส่ง`; status remains draft | ☐ |

### TC-A02 — acknowledge overlap แล้วส่งได้ (happy)
- group: approval · ความสำคัญ: critical · trace: BR-PROMO-07/08,DOA,FN-09/10/16
- actor: Officer
- Setup: role=officer · seed=same as A01 · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: pending + frozen timeline; old promo unchanged

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK draft → CLICK “ส่งอนุมัติ” | — | submit modal opens | ☐ |
| 2 | SELECT assignee ทุก slot → TOGGLE ยืนยันการทับซ้อน | — | confirm enabled/no error | ☐ |
| 3 | CLICK ยืนยันส่ง | — | toast prefix `ส่งอนุมัติแล้ว — เข้ากล่อง My Approval ของ`; detail status “รออนุมัติ” | ☐ |
| 4 | VERIFY tab “การอนุมัติและข้อมูล” | — | timeline preserves selected people in step order | ☐ |
| 5 | VERIFY promotion conflict เดิม | — | original date/status unchanged | ☐ |

### TC-A03 — Sales Manager อนุมัติขั้นแรก (happy)
- group: approval · ความสำคัญ: critical · trace: BR-DOA-04/06,FN-11
- actor: Sales Manager current assignee
- Setup: role=role-mgr-sales/current-assignee · seed=pending step1 assigned to current persona · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: step1 approved and forwarded

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT persona “ผู้จัดการฝ่ายขาย” | — | demo role changes; pending record visible | ☐ |
| 2 | CLICK pending row → VERIFY approval tab | — | current step shows manager pending; approve/reject buttons visible | ☐ |
| 3 | CLICK “อนุมัติ” → TYPE optional note → CLICK confirm | ผ่านขั้นแรก | toast indicates step approved/next assignee; step1 approved, step2 pending | ☐ |

### TC-A04 — BU Head อนุมัติขั้นสุดท้าย (happy)
- group: approval · ความสำคัญ: critical · trace: BR-DOA-06,FN-12
- actor: BU Head current assignee
- Setup: role=role-mgr-bu/current-assignee · seed=pending final step; valid_from=today or future variant · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: final decision makes active or scheduled by date

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT persona “หัวหน้า BU” → CLICK target pending row | — | final current step visible and actionable | ☐ |
| 2 | CLICK “อนุมัติ” → CLICK confirm | — | today record: toast `อนุมัติครบสาย — โปรฯ มีผลทันที`; status “กำลังใช้” | ☐ |
| 3 | VERIFY future-date variant after same action | — | status “รอถึงวันเริ่ม”; date shown | ☐ |

### TC-A05 — reject บังคับเหตุผลและกลับร่าง (negative/happy)
- group: approval · ความสำคัญ: critical · trace: BR-DOA-03/07,EC-04
- actor: current assignee
- Setup: role=current-assignee · seed=pending promotion · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: blank blocked; valid reason returns draft with history

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK pending row → CLICK “ไม่อนุมัติ” | — | modal title `ไม่อนุมัติ — ตีกลับเป็นร่าง` | ☐ |
| 2 | CLICK confirm โดยเหตุผลว่าง | — | toast `กรุณากรอกข้อมูลให้ครบถ้วน`; modal remains open | ☐ |
| 3 | TYPE เหตุผล → CLICK “ไม่อนุมัติ” | ข้อมูลเงื่อนไขไม่ครบ | toast `ตีกลับแล้ว — กลับเป็นร่าง`; status “ร่าง” | ☐ |
| 4 | VERIFY tab “ประวัติ” | — | reject actor/time/reason remains appended | ☐ |

### TC-A06 — pause ต้องมีเหตุผล (negative/happy)
- group: lifecycle · ความสำคัญ: สูง · trace: BR-PROMO-12,FN-28
- actor: Sales Manager
- Setup: role=role-mgr-sales · seed=active promotion · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: blank blocked; reason pauses

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK active row → CLICK “ระงับ” | — | modal describes new documents do not receive promo | ☐ |
| 2 | CLICK confirm with blank reason | — | required error/toast; state remains active | ☐ |
| 3 | TYPE reason → CLICK “ระงับ” | รอตรวจสอบสต๊อก | detail status “ระงับชั่วคราว”; audit has reason | ☐ |

### TC-A07 — resume preserves date/budget (delta)
- group: lifecycle · ความสำคัญ: สูง · trace: BR-PROMO-12,FN-28
- actor: Sales Manager
- Setup: role=role-mgr-sales · seed=paused promotion · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: returns active and date/budget unchanged

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK paused row → VERIFY และบันทึก date/budget/used amount | — | initial values captured | ☐ |
| 2 | CLICK “เปิดต่อ” | — | toast contains promotion code + `เปิดใช้ต่อแล้ว`; status “กำลังใช้” | ☐ |
| 3 | VERIFY date/budget/used amount | — | equal values captured in step1 | ☐ |

### TC-A08 — end early irreversible (negative/happy)
- group: lifecycle · ความสำคัญ: critical · trace: BR-PROMO-12,FN-29
- actor: Sales Manager
- Setup: role=role-mgr-sales · seed=active/scheduled/paused/exhausted variants · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: each valid source can end; reason/date required; no reopen action

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK target row → CLICK “ปิดก่อนกำหนด” | — | modal title `ปิดโปรโมชันก่อนกำหนด` | ☐ |
| 2 | CLICK confirm with blank reason | — | blocked; current status unchanged | ☐ |
| 3 | TYPE reason + SELECT effective date today → CLICK confirm | ยุติแคมเปญ | status ended early; new validity end shown | ☐ |
| 4 | VERIFY action footer | — | no resume/edit; copy remains available | ☐ |

### TC-A09 — forbidden transition (negative parameterized)
- group: lifecycle · ความสำคัญ: สูง · trace: BR_PROMO_INVALID_TRANSITION,AT-15
- actor: Manager/Officer
- Setup: roles=officer,manager · seed=draft/ended/cancelled · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: invalid action hidden or rejected with no state change

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY draft footer for pause/end actions | — | invalid actions absent | ☐ |
| 2 | VERIFY ended/cancelled footer for edit/submit/resume | — | invalid actions absent | ☐ |
| 3 | VERIFY state/history after attempted direct request `(ต้อง simulate)` | BR_PROMO_INVALID_TRANSITION | state unchanged; no successful transition audit | ☐ |

### TC-A10 — history append-only across round
- group: audit · ความสำคัญ: สูง · trace: BR-PROMO-17,FN-94
- actor: Officer + approvers
- Setup: seed=promotion created→edited→submitted→rejected→resubmitted→approved · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: all events remain chronological and prior rejection not overwritten

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK seeded promotion → CLICK tab “ประวัติ” | — | timeline lists create/edit/submit/reject/resubmit/approve | ☐ |
| 2 | VERIFY rejection round | — | old assignee/time/reason still visible | ☐ |
| 3 | VERIFY approval timeline | — | latest frozen chain distinct from prior round | ☐ |

## Group S — Simulator and Calculation

### TC-S01 — LINE discount from post-TA price (happy/boundary)
- group: simulator · ความสำคัญ: critical · trace: BR-PROMO-01/03/14,AT-09,EC-AI-05 `[AI-DEFAULT]`
- actor: Officer
- Setup: seed=active 10% LINE promo + line post-TA unit=100 qty=12 promoAllowed=true · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: line discount=120, no negative net, GL trace visible in evaluation detail

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “ทดสอบตะกร้า” | — | simulator opens | ☐ |
| 2 | SELECT customer/channel → add product → TYPE qty 12 | resolved unit 100 | line total 1,200 displayed | ☐ |
| 3 | VERIFY “ลดโปรฯ” and summary | — | discount 120; net 1,080; applied ladder entry visible | ☐ |

### TC-S02 — coupon case-insensitive / missing skip
- group: simulator · ความสำคัญ: critical · trace: BR-PROMO-02/15,FN-22
- actor: Officer
- Setup: seed=PM-2026-015 active/date valid/channel ONLINE/coupon WELCOME100/amount≥500 · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: blank skips; lowercase applies -100

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “ทดสอบตะกร้า” → SELECT ช่องทาง “เว็บไซต์ / ออนไลน์” | — | channel explicitly selected | ☐ |
| 2 | TYPE blank/clear → ช่อง “คูปอง” | — | PM-2026-015 ladder shows skipped with coupon reason | ☐ |
| 3 | TYPE `welcome100` → ช่อง “คูปอง” | — | focus remains in input; PM-2026-015 shows `ติด` and `-100.00 ฿` | ☐ |

### TC-S03 — scope uses explicit channel
- group: simulator · ความสำคัญ: สูง · trace: BR-PROMO-02,FN-03
- actor: Officer
- Setup: seed=customer default SalesRep + promo online only · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: explicit online channel overrides customer default

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT customer with default SalesRep; leave channel blank | — | online-only promotion skipped | ☐ |
| 2 | SELECT “เว็บไซต์ / ออนไลน์” → ช่องทาง | — | eligible online promotion becomes candidate/applied if other conditions pass | ☐ |

### TC-S04 — date/status eligibility
- group: simulator · ความสำคัญ: สูง · trace: BR-PROMO-02
- actor: Officer
- Setup: seed=draft,scheduled,active,paused,ended variants same rule · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: only active for document date applies

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN simulator with qualifying cart | — | ladder lists applicable candidates/skips | ☐ |
| 2 | VERIFY each variant reason | — | active applies; draft/scheduled-before-date/paused/ended skip with distinct reason | ☐ |

### TC-S05 — FREE_GOODS repeat and zero-price row
- group: simulator · ความสำคัญ: critical · trace: BR-PROMO-04/13,FN-19
- actor: Officer
- Setup: seed=PM-012 active wholesale buy10 get1 repeat · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: 20 buy units→2 free; zero price

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT wholesale customer/channel → add water qty 20 base-equivalent | — | line shows quantity and base price | ☐ |
| 2 | VERIFY free-goods row | — | pill “ของแถม”, qty 2, price 0.00,total 0.00 | ☐ |
| 3 | VERIFY ladder | — | PM-012 applied and explains repeat count | ☐ |

### TC-S06 — THRESHOLD highest tier after line discount
- group: simulator · ความสำคัญ: critical · trace: BR-PROMO-05,FN-20
- actor: Officer
- Setup: seed=threshold 20k→3%,50k→5% + prior line promo · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: base after prior line discount chooses highest reached tier only

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT/TYPE สินค้าและจำนวนให้ยอด gross สูงกว่า 50k แต่หลัง line discount ต่ำกว่า50kและสูงกว่า20k | — | summary records subtotal and prior line discount | ☐ |
| 2 | VERIFY threshold result | — | 3% tier applies, not 5%; exact amount from post-line-discount base | ☐ |

### TC-S07 — THRESHOLD below minimum says remaining
- group: simulator · ความสำคัญ: สูง · trace: BR-PROMO-05,FN-20
- actor: Officer
- Setup: seed=minimum threshold 20,000 · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: no discount and ladder shows how much remains

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT/TYPE สินค้าและจำนวนให้ net threshold base 19,000 | — | summary base visible | ☐ |
| 2 | VERIFY threshold ladder entry | — | skipped/not reached; text states `ขาดอีก` 1,000 equivalent | ☐ |

### TC-S08 — BUNDLE complete-set minimum
- group: simulator · ความสำคัญ: critical · trace: BR-PROMO-05,FN-21
- actor: Officer
- Setup: seed=bundle requires A2+B1, price189, repeat · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: A5+B2 yields 2 sets and correct savings

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT product A และ B แล้ว TYPE qty5/qty2 | — | both rows visible; unit columns do not overlap | ☐ |
| 2 | VERIFY applied bundle | — | set count 2 = minimum complete count; discount `(normal-set - 189)×2` | ☐ |

### TC-S09 — priority and exclusive stop
- group: simulator · ความสำคัญ: critical · trace: BR-PROMO-06,FN-23
- actor: Officer
- Setup: seed=multiple eligible promos, lower priority number exclusive · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: ladder sorted and later promos skipped

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT/TYPE สินค้าและจำนวนให้ผ่านหลายโปรโมชัน | — | multiple candidates visible | ☐ |
| 2 | VERIFY ladder order | — | ascending priority; tie newest start first | ☐ |
| 3 | VERIFY rows after exclusive applied | — | marked skipped with exclusive stop reason; no discounts from them | ☐ |

### TC-S10 — TA no-repeat line
- group: simulator · ความสำคัญ: critical · trace: BR-PROMO-03,FN-24,XT-01
- actor: Officer
- Setup: seed=two lines, one `promoAllowed=false`, one true · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: only allowed line discounted

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN simulator seeded with both lines `(ต้อง simulate TA flag)` | — | both post-TA prices displayed | ☐ |
| 2 | VERIFY discount per line | — | false line shows no promo discount; true line discounts | ☐ |
| 3 | VERIFY ladder reason | — | TA “ไม่ลดซ้ำ” reason visible | ☐ |

### TC-S11 — budget remaining prevents overflow
- group: simulator · ความสำคัญ: critical · trace: BR-PROMO-09,FN-27
- actor: Officer
- Setup: seed=active promo remaining budget 50; candidate discount 100 · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: whole application skipped, not partially applied

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT/TYPE สินค้าและจำนวนให้ candidate discount=100 | — | net does not include that discount | ☐ |
| 2 | VERIFY ladder | — | skipped because budget insufficient; no partial 50 discount | ☐ |

### TC-S12 — per-customer quota
- group: simulator · ความสำคัญ: critical · trace: BR-PROMO-10,FN-31
- actor: Officer
- Setup: seed=customer usage count equals limit_per_customer · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: promotion skipped for that customer, eligible for another

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT exhausted customer and qualifying cart | — | ladder skips with per-customer quota reason | ☐ |
| 2 | SELECT different customer with zero usage | — | same promotion can apply | ☐ |

## Group P — Permission and Security

### TC-P01 — submitter self-approval blocked (SoD)
- group: permission · ความสำคัญ: critical · trace: BR-DOA-04,ERR_SOD_VIOLATION,FN-14
- actor: Officer submitter
- Setup: role=submitter · seed=draft and candidate roster includes same employee at source DOA · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: self absent from picker and no approval action after submit

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK draft → CLICK “ส่งอนุมัติ” → OPEN each slot picker | — | submitter name absent; other candidates visible | ☐ |
| 2 | CLICK ส่งด้วย assignee คนอื่น แล้ว VERIFY detail ใน persona ผู้ส่ง | — | approve/reject buttons absent | ☐ |

### TC-P02 — wrong current approver denied
- group: permission · ความสำคัญ: critical · trace: BR-DOA-06,ERR_FORBIDDEN
- actor: Sales Manager not assigned
- Setup: role=role-mgr-sales non-assignee · seed=pending assigned to another manager · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: no decision buttons/direct attempt forbidden

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK pending promotion | — | timeline visible; approve/reject absent | ☐ |
| 2 | VERIFY direct action attempt `(ต้อง simulate)` | — | 403/`ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน`; state unchanged | ☐ |

### TC-P03 — BU Head and human service boundaries
- group: permission · ความสำคัญ: critical · trace: permission matrix,401/403,ERR_PROMOTION_NOT_FOUND
- actor: BU Head/human
- Setup: role=role-mgr-bu not assigned + human user; seed=other-tenant id `(ต้อง simulate)` · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: create/manage/usage/cross-tenant access unavailable

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY page actions as BU Head | — | create/edit/pause/end absent unless allowed contract; assigned decision only | ☐ |
| 2 | VERIFY human usage-event request `(ต้อง simulate)` | — | 403 and no count change | ☐ |
| 3 | VERIFY other-tenant id read `(ต้อง simulate)` | — | 404/not visible; no data leak | ☐ |

### TC-P04 — excluded capabilities absent
- group: scope lock · ความสำคัญ: high · trace: LOCK-PROMO-02/07,BR-PROMO-16
- actor: Officer
- Setup: role=officer · seed=— · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: no customer-specific/campaign/loyalty/mixed-type controls

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “สร้างโปรโมชัน” → VERIFY scope choices | — | only ทุกลูกค้า/กลุ่มลูกค้า/ช่องทาง; no individual customer | ☐ |
| 2 | VERIFY type choices and form | — | one of four only; no loyalty or multi-type | ☐ |
| 3 | VERIFY whole page/detail | — | no Campaign Management control/link | ☐ |

## Group X — Cross-Module

### TC-X01 — Price List/TA input contract `(ต้อง simulate)`
- group: XT · ความสำคัญ: critical · trace: XT-01,LOCK-PROMO-03
- actor: integration tester
- Setup: role=integration · seed=same line has list150, TA net100,promoAllowed true/false variants · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: calculation uses 100, never 150; malformed missing unit rejected

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN simulator/inject resolved line variant | unit100 | visible base price 100 | ☐ |
| 2 | VERIFY 10% result | — | discount 10 per quantity base, not 15 | ☐ |
| 3 | VERIFY missing resolved unit API case | — | ENG_ERR_INVALID_INPUT/RULE; no guessed price | ☐ |

### TC-X02 — QT/SO freezes evaluation `(ต้อง simulate)`
- group: XT · ความสำคัญ: critical · trace: XT-02
- actor: sales document tester
- Setup: seed=QT/SO draft with evaluated promo + source promotion later paused · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: existing document snapshot does not change; new evaluation skips paused promo

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY applied amount/source on downstream document และบันทึกค่าไว้ | — | baseline captured | ☐ |
| 2 | CLICK “ระงับ” ผ่าน manager flow | — | source becomes paused | ☐ |
| 3 | VERIFY existing document snapshot | — | same amount/source as step1 | ☐ |
| 4 | VERIFY new evaluation | — | paused promo skipped | ☐ |

### TC-X03 — Invoice usage/GL idempotent `(ต้อง simulate)`
- group: XT · ความสำคัญ: critical · trace: XT-03,LOCK-PROMO-06,BR-PROMO-10/14/17
- actor: invoice service tester
- Setup: seed=promotion uses=10, discount=1000; event E1 amount100 GL4110-02 · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: first event increments once; retry no delta; GL/audit trace visible

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN detail → VERIFY และบันทึก uses/discount/GL | — | 10 / 1000 / 4110-02 captured | ☐ |
| 2 | VERIFY runner ส่ง usage event E1 `(ต้อง simulate)` | occurrence1,amount100 | API applied | ☐ |
| 3 | OPEN detail → VERIFY usage | — | 11 / 1100; GL unchanged; history has event | ☐ |
| 4 | VERIFY runner ส่ง E1 ซ้ำแล้วเปิด detail | — | still 11 / 1100; prior-result response | ☐ |

### TC-X04 — Inventory ATP remains downstream `(ต้อง simulate)`
- group: XT · ความสำคัญ: high · trace: XT-04,LOCK-PROMO-05
- actor: SO tester
- Setup: seed=free goods qualifies but on_hand=0 · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: promo output includes free item; simulator does not claim stock; SO owns outcome

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT/TYPE สินค้าและจำนวนให้ผ่าน free-goods rule | — | simulator shows free row price0 | ☐ |
| 2 | VERIFY promotion detail/simulator | — | no ATP check/block control in Promotion | ☐ |
| 3 | VERIFY SO downstream behavior `(ต้อง simulate)` | stock0 | SO warning/block/partial follows SO contract; promo result remains traceable | ☐ |

### TC-X05 — DOA config-driven frozen chain `(ต้อง simulate)`
- group: XT · ความสำคัญ: critical · trace: XT-05,LOCK-PROMO-04,EC-AI-03 `[AI-DEFAULT]`
- actor: DOA integration tester
- Setup: seed=DOA v1 roles step1/2 + draft; change to v2 after submit · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: submit UI mirrors v1; in-flight remains v1 after config changes

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK draft → CLICK “ส่งอนุมัติ” | DOA v1 | slots/order/candidates match v1, no amount bands | ☐ |
| 2 | SELECT assignees → CLICK confirm | — | timeline freezes v1 people/roles | ☐ |
| 3 | VERIFY runner เปลี่ยน central DOA เป็น v2 แล้ว OPEN same detail `(ต้อง simulate)` | — | timeline unchanged | ☐ |
| 4 | CLICK new draft → CLICK “ส่งอนุมัติ” | — | new modal uses v2 | ☐ |

### TC-X06 — Item/master source and inactive snapshot `(ต้อง simulate)`
- group: XT · ความสำคัญ: high · trace: XT-06,LOCK-PROMO-03,EC-10
- actor: Officer/master tester
- Setup: seed=active product P with UOM/factor/list; approved promo references P; then deactivate P · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: old detail remains readable; new picker omits inactive P

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN approved promo detail → VERIFY product code/name/UOM | — | historical snapshot visible | ☐ |
| 2 | VERIFY runner ปิดใช้งาน P ใน Item Master `(ต้อง simulate)` | — | source changes | ☐ |
| 3 | OPEN approved detail again | — | same historical snapshot visible | ☐ |
| 4 | CLICK “สร้างโปรโมชัน” → OPEN product picker | — | inactive P unavailable for new selection | ☐ |

## Group N — Concurrency, Idempotency, Performance

### TC-N01 — stale update conflict `(ต้อง simulate)` `[AI-DEFAULT]`
- group: reliability · ความสำคัญ: high · trace: EC-AI-01,ERR_VERSION_CONFLICT
- actor: two Officers
- Setup: role=officer A/B · seed=same draft version1 in two sessions · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: second stale save rejected and latest data preserved

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN draft in session A and B → VERIFY initial name/version | — | both see version1 | ☐ |
| 2 | TYPE name A → CLICK save in session A | — | success; version2 | ☐ |
| 3 | TYPE name B → CLICK save in stale session B | — | conflict/reload message; no success toast | ☐ |
| 4 | OPEN detail fresh | — | name A preserved, not silently overwritten | ☐ |

### TC-N02 — duplicate click/idempotency `(ต้อง simulate)` `[AI-DEFAULT]`
- group: reliability · ความสำคัญ: critical · trace: EC-AI-02,EC-12,FN-93
- actor: Officer/Approver/service
- Setup: seed=valid draft,pending,event; network retry duplicates same key · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: create/submit/approve/usage each executes once

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK submit confirm rapidly twice | — | one pending transition, one audit submit, buttons busy/disabled | ☐ |
| 2 | CLICK approve confirm rapidly twice | — | one step decision/advance | ☐ |
| 3 | VERIFY runner retry usage event key เดิม `(ต้อง simulate)` | — | count increments once | ☐ |

### TC-N03 — designed-load response `(ต้อง simulate)`
- group: performance · ความสำคัญ: high · trace: NFR,BRD §17
- actor: performance tester
- Setup: seed=10k promotions/evaluations dataset,100 concurrent users · files=—
- Start: OPEN `#/promotions`
- ผ่านเมื่อ: p95 list/evaluate ≤2s and UI stays usable

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN list under designed load | — | content loaded p95≤2s; no broken layout | ☐ |
| 2 | OPEN simulator and change qty/coupon under load | — | result refresh p95≤2s; input focus stable | ☐ |

## วิธีที่ agent รัน (Run protocol)

1. Start every case from a fresh page at its stated route; reset prototype seed/reload unless Setup says preserve a seeded backend record.
2. Select the required persona only to simulate role in prototype. On production, log in as actual role.
3. Execute one row at a time; set Result to `☑ Pass`, `☒ Fail` or `◫ Blocked` in the runner record.
4. For `(ต้อง simulate)`, inject the specified API/master/clock/concurrency state; if unavailable, mark Blocked rather than guessing.
5. Capture visible evidence on failure: actual text, status, values, and current route. Do not inspect DOM selectors as acceptance evidence.
6. Refresh/reset after each independent case; never depend on prior case state unless Setup explicitly seeds it.

## Coverage Audit

| Category | Covered / Total |
|---|---:|
| Acceptance AT | 24 / 24 |
| Business rule groups | 18 / 18 |
| Confirmed edge cases | 12 / 12 |
| AI-default edge cases | 5 / 5 |
| Error catalog items | 11 / 11 |
| Permission cells | 7 / 7 grouped cells |
| UI/state/event items | 10 / 10 |
| Cross-Module XT | 6 / 6 |
| Scope Locks | 7 / 7 (LOCK-07 verified by absence; no campaign behavior case) |

- Skipped implementation cases: Campaign functionality, loyalty, customer-specific promotion, ATP decision inside Promotion — outside Scope Lock. Absence is verified, not treated as a functional test.
- `[AI-DEFAULT]` cases remain labeled for BA/engineering confirmation: concurrency, idempotency, DOA version freeze, auth semantics, decimal handling.
- **Manifest cross-check (FRD §0.12): ✅ 42/42 manifest rows represented in Ledger.**
- Overall in-scope coverage: **100%**.

## Result Report (schema)

```json
{
  "feature_id": "F-SALES-PROMO",
  "run_at": "<iso datetime>",
  "environment": "<prototype|staging|production-like>",
  "results": [
    {"id":"TC-L01","status":"pass|fail|blocked","failed_step":null,"evidence":"","note":""}
  ],
  "summary": {"total":55,"pass":0,"fail":0,"blocked":0}
}
```
