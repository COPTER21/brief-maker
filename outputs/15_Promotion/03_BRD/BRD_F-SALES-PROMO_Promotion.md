# BRD: Promotion — โปรโมชัน

## 1. Document Info

| Field | Value |
|---|---|
| BRD ID | BRD-F-SALES-PROMO |
| Feature ID | F-SALES-PROMO |
| Feature Name | Promotion — โปรโมชัน |
| BRD Type | New Feature |
| Version | 1.0 |
| Status | APPROVED — AI Reviewed |
| Module | Sales |
| Owner | Sales / BA |
| Stakeholders | Sales, Marketing, Accounting, Inventory, PM/BA, Engineering, QA |
| Created / Updated | 2026-08-18 |
| Primary sources | PREBRIEF_F-SALES-PROMO, FUNCTION_CHECKLIST_F-SALES-PROMO, Promotion.html |

### Changelog

- v1.0 (2026-08-18): สร้าง BRD หลัง PM/BA อนุมัติ HTML gate และยืนยันคำตอบทางธุรกิจครบ

## 2. Business Context

### 2.1 ปัญหา / โอกาส

ฝ่ายขายต้องสร้างข้อเสนอชั่วคราวสำหรับลูกค้ากลุ่มกว้างโดยให้ราคา ข้อตกลงการค้า โปรโมชัน บัญชี และการอนุมัติทำงานเป็นลำดับเดียวกัน หากเก็บกติกาเหล่านี้กระจัดกระจายที่ใบเสนอราคาหรือใบสั่งขาย จะเกิดส่วนลดผิดลำดับ ซ้อนสิทธิ์ผิด นับโควตาผิด และตรวจย้อนหลังไม่ได้

### 2.2 เป้าหมายทาง Business

- ให้ Sales/Marketing สร้างโปรโมชันได้ 4 ชนิดสำหรับทุกลูกค้า กลุ่มลูกค้า หรือช่องทางขาย
- ให้ Quotation/Sales Order ประเมินโปรโมชันหลังราคาบัญชีและ Trade Agreement ด้วยกติกาเดียว
- ควบคุมการใช้งานด้วยช่วงเวลา คูปอง ลำดับ exclusive งบ และโควตา
- บังคับอนุมัติตาม DOA กลางแบบไม่มีวงเงินและแยกผู้ส่งออกจากผู้อนุมัติ
- ส่งผลส่วนลด ของแถม GL และ usage ไปปลายทางโดยมี audit ตรวจสอบได้

### 2.3 ตัวชี้วัดความสำเร็จ

| Metric | Baseline | Target | วิธีวัด | จังหวะวัด |
|---|---|---|---|---|
| ความถูกต้องของผล `calcPromo` เทียบ expected test | ยังไม่มีระบบจริง | 100% ของชุด regression ที่ยืนยัน | ผล automated + UAT เทียบส่วนลด/ของแถม/เหตุข้าม | ทุก release |
| การอนุมัติผิด SoD | ยังไม่มีระบบจริง | 0 รายการ | audit event ที่ submitter = approver | real-time + รายเดือน |
| usage จาก Invoice ที่ trace กลับโปรโมชันได้ | ยังไม่มีระบบจริง | 100% | promo usage event เทียบ Invoice line/reference | รายวัน |
| ข้อผิดพลาดจากข้อมูลไม่ครบก่อนส่ง | ยังไม่มี baseline | 0 รายการหลุดถึง pending approval | validation rejection เทียบ pending records | รายสัปดาห์ |

### 2.4 ที่มา

- Central Plan วาง Promotion เป็น upstream config ของ Sales Quotation และ Sales Order
- PREBRIEF กำหนด 27 scenarios, 17 business-rule groups และ contract `calcPromo(lines, doc)`
- PM/BA อนุมัติ HTML และยืนยันให้ยึด mock mapping โดยข้อมูลสินค้าอ้าง Item Master เป็น source of truth

## 3. Scope

### 3.1 In Scope

- รายการ ค้นหา กรอง แท็บสถานะ sort และ Export CSV
- สร้าง/แก้ร่างแบบ 3 ขั้น พร้อม 4 ชนิด: ส่วนลดสินค้า ซื้อ X แถม Y ยอดใบถึงเกณฑ์ ชุดราคาพิเศษ
- ขอบเขตทุกลูกค้า กลุ่มลูกค้า หรือช่องทางขายแบบหลายค่า
- คูปอง ลำดับ exclusive การซ้อน TA โควตารวม โควตาต่อลูกค้า งบ GL และผู้ดูแล
- ตรวจทับซ้อน เตือน และบังคับยืนยันก่อนส่งโดยไม่ตัดโปรโมชันเดิม
- DOA แบบไม่มีวงเงิน เรียงตามลำดับ ตำแหน่งอ่านจาก DOA config และผู้ส่งเลือกบุคคลต่อ slot
- อนุมัติ ไม่อนุมัติ ทำสำเนา ระงับ เปิดต่อ ปิดก่อนกำหนด ยกเลิก และ audit append-only
- ตะกร้าจำลองเพื่อพิสูจน์ `calcPromo` รวมเหตุผลติด/ข้าม
- Contract ไป Quotation, Sales Order, Invoice, GL Posting Group และ Inventory

### 3.2 Out of Scope

- โปรโมชันเฉพาะลูกค้ารายเดียว — ใช้ Trade Agreement
- หลายชนิดในโปรโมชันเดียว หรือ multiline discount ข้ามหลายสินค้า — แยกเป็นหลายโปรโมชัน
- Loyalty point / บัตรสะสมแต้ม
- ตรวจ ATP หรือเลือกการแถมบางส่วน — เป็นงาน Sales Order/Inventory
- แก้โปรโมชันหลังอนุมัติ รวมถึงเพิ่มงบ — ทำสำเนาใหม่
- การตั้งค่า DOA จริง — feature นี้ประกาศ contract เท่านั้น
- Campaign Management integration ในรอบนี้ — เชื่อมในอนาคตเมื่อ feature พร้อม
- Notification declaration และ Document Configuration declaration ในรอบนี้ตามคำสั่งผู้ใช้

### 3.3 Assumptions

- Customer Group, Sales Channel และ master อื่นใช้ mock mapping ที่สื่อ contract เดียวกับ source feature
- Item Master เป็น source of truth สำหรับสินค้า หมวด หน่วย factor และราคาตั้ง
- Sales Channel เป็นข้อมูลปรับแต่งได้ จึงใช้ค่าตาม mock โดยอ้างรหัส ไม่ hardcode ความหมายทางธุรกิจ
- Quotation/Sales Order เป็นผู้เรียก engine; Promotion ไม่ทำ flow สร้างเอกสารขาย
- จำนวนครั้งใช้โปรโมชันนับจาก Invoice ตามที่ PM/BA ยืนยัน

### 3.4 Scope Lock

- **Scope Lock Ref:** PREBRIEF_F-SALES-PROMO + PM/BA approval 2026-08-18

| LOCK-ID | ข้อยืนยัน |
|---|---|
| LOCK-PROMO-01 | UI และความสามารถยึด source pack กับ Promotion.html ที่ผ่าน PM/BA |
| LOCK-PROMO-02 | ไม่มีโปรโมชันเฉพาะลูกค้ารายเดียว |
| LOCK-PROMO-03 | Item Master เป็น source of truth; master อื่นใช้ soft-reference/mock mapping |
| LOCK-PROMO-04 | DOA ไม่มีวงเงิน ใช้ลำดับจาก config และผู้ส่งห้ามอนุมัติรายการตนเอง |
| LOCK-PROMO-05 | งาน ATP/ของแถมไม่พออยู่ที่ Sales Order ไม่ใช่ Promotion |
| LOCK-PROMO-06 | การนับ usage เกิดจาก Invoice และนับจำนวนครั้งใช้โปรโมชัน |
| LOCK-PROMO-07 | Campaign Management เป็น future integration |

## 4. User Roles & Permissions

### 4.1 Roles

| Role | หน้าที่ |
|---|---|
| Sales/Marketing Officer | สร้าง แก้ร่าง ส่งอนุมัติ ทำสำเนา ทดสอบตะกร้า Export และยกเลิกก่อนมีผล |
| Sales Manager (`role-mgr-sales`) | อนุมัติเมื่อถูกเลือกในขั้นปัจจุบัน ระงับ เปิดต่อ ปิดก่อนกำหนด |
| BU Head (`role-mgr-bu`) | อนุมัติเมื่อถูกเลือกในขั้นปัจจุบัน |
| System | validate, resolve/freeze DOA, ประเมินโปรโมชัน, เปลี่ยนสถานะตามเวลา/งบ/โควตา, audit |

### 4.2 Permission Matrix

| Action | Officer | Sales Manager | BU Head | System |
|---|:---:|:---:|:---:|:---:|
| ดูรายการ/รายละเอียด/ตะกร้าจำลอง | ✅ | ✅ | ✅ | — |
| สร้าง/แก้ร่าง/ทำสำเนา | ✅ | ✅ | ❌ | — |
| ส่งอนุมัติ/ยกเลิกก่อนมีผล | ✅ เจ้าของ/ผู้มีสิทธิ์ | ✅ | ❌ | validate |
| อนุมัติ/ไม่อนุมัติ | ❌ ผู้ส่ง | ✅ เมื่อเป็น current assignee | ✅ เมื่อเป็น current assignee | enforce sequence + SoD |
| ระงับ/เปิดต่อ/ปิดก่อนกำหนด | ❌ | ✅ | ❌ | enforce state |
| แก้โปรโมชันอนุมัติแล้ว | ❌ | ❌ | ❌ | block; ใช้สำเนา |

## 5. User Journey with COSO

### 5.1 Happy Path

| # | Step | Maker | Checker | Approver | System | Evidence UI |
|---|---|---|---|---|---|---|
| 1 | เปิดรายการและกด “สร้างโปรโมชัน” | Officer | — | — | เปิด wizard 3 ขั้น | `#/promotions`, `openCreate()` |
| 2 | กรอกชนิด ขอบเขต เงื่อนไข คูปอง งบ GL | Officer | — | — | validate ต่อขั้น | `formErrors()`, `nextStep()` |
| 3 | ตรวจสรุปและบันทึกร่าง | Officer | — | — | สร้างเลข mock และ audit | `saveForm()` |
| 4 | ส่งอนุมัติและเลือกคนครบทุก slot | Officer | — | — | resolve DOA, ตัดผู้ส่ง, freeze chain | `confirmSubmit()` |
| 5 | อนุมัติขั้นปัจจุบัน | — | — | current assignee | ตรวจ SoD, ส่งต่อขั้นถัดไป | `confirmApprove()` |
| 6 | อนุมัติครบสาย | — | — | final assignee | เป็นรอเริ่มหรือกำลังใช้ตามวันที่ | approval timeline |
| 7 | QT/SO เรียกประเมิน | — | — | — | คำนวณตาม priority/exclusive | ตะกร้าจำลอง ladder |
| 8 | Invoice ยืนยันการใช้ | — | — | — | เพิ่ม uses/discount/customers/byCust และ GL | tab การใช้งาน |

**SoD:** Maker/submitter ไม่ใช่ Approver ทุกขั้น และถูกตัดจาก picker ✅

### 5.2 Alternative / Exception Paths

| Path | Maker | Checker | Approver | System outcome |
|---|---|---|---|---|
| Validation ไม่ผ่าน | Officer | — | — | อยู่ขั้นเดิม แสดง error |
| โปรโมชันทับซ้อน | Officer | — | — | แสดงรายการ; ต้องติ๊กยืนยันก่อนส่ง |
| ไม่อนุมัติ | — | — | current assignee | บังคับเหตุผล กลับร่าง เก็บ history |
| ระงับ/เปิดต่อ | — | Sales Manager | — | หยุด/กลับมาประเมินโดยช่วงเวลาและงบเดิม |
| ปิดก่อนกำหนด | — | Sales Manager | — | ไม่ใช้กับเอกสารใหม่ ย้อนกลับไม่ได้ |
| งบ/โควตาหมด | — | — | — | engine ข้ามพร้อมเหตุผล |

## 6. Data Entity & Fields

### 6.1 Entity Overview

| Entity | Type | Purpose |
|---|---|---|
| promotion | Header | ตัวตน ขอบเขต ระยะเวลา การควบคุม สถานะ DOA และ usage |
| promotion_rule | Detail | เงื่อนไขตาม 1 ใน 4 ชนิด |
| promotion_rule_item | Detail | สินค้า/ขั้น/รายการชุดตามชนิด rule |
| promotion_approval_step | Workflow snapshot | ขั้น ตำแหน่ง คน และผลอนุมัติแบบ freeze |
| promotion_usage | Transaction event | การใช้จาก Invoice พร้อมยอด/ลูกค้า/GL |
| promotion_audit | Append-only | ทุก mutation และ state transition |

### 6.2 Promotion Header — key fields

| Field | UI Label | Type | Required | Rule |
|---|---|---|:---:|---|
| promotion_id / code | รหัส | AUTO/TEXT | ✅ | `PM-YYYY-NNN`; unique |
| name / description | ชื่อ / รายละเอียด | TEXT/TEXTAREA | ✅/— | ชื่อห้ามว่าง |
| promotion_type | ชนิด | ENUM | ✅ | LINE_DISC/FREE_GOODS/THRESHOLD/BUNDLE |
| scope_type / scope_refs | ขอบเขต | ENUM/JSON | ✅ | all หรือ refs ≥1; ไม่มี customer scope |
| valid_from / valid_until | เริ่ม / สิ้นสุด | DATE | ✅/— | เริ่ม ≥ วันที่สร้าง; สิ้นสุด ≥ เริ่ม |
| coupon_code | คูปอง | TEXT | — | uppercase, A-Z0-9-_ 3–20, unique ในรายการยังไม่จบ |
| priority | ลำดับ | NUMBER | ✅ | 1–999; น้อยก่อน |
| exclusive / stack_ta | กันซ้อน / ซ้อน TA | TOGGLE | — | defaults false/true |
| limit_total / limit_per_customer | โควตา | NUMBER | — | 0 = ไม่จำกัด; นับจาก Invoice |
| budget_amount | งบ | NUMBER | — | 0 = ไม่จำกัด |
| gl_account_ref | บัญชี GL | LOOKUP | ✅ | GL Posting Group soft-ref |
| owner_ref | ผู้ดูแล | LOOKUP | ✅ | Employee soft-ref |
| status / paused / end_early | สถานะ | AUTO | ✅ | ตาม §8 |
| approval_* / approval_chain | การอนุมัติ | AUTO/JSON | ✅ | contract DOA; snapshot append-only |
| uses / discount_amount / customers / by_customer | การใช้งาน | AUTO | ✅ | event จาก Invoice เท่านั้น |
| version | เวอร์ชัน | AUTO | ✅ | optimistic concurrency |
| created_by/at, modified_by/at | Audit | AUTO | ✅ | ทุก entity |

### 6.3 Rule fields

| Type | Fields | Validation |
|---|---|---|
| LINE_DISC | target, ref, mode, value, min_qty_base | value >0; pct ≤100; ref เมื่อ target ไม่ใช่ all |
| FREE_GOODS | buy/get product, uom, qty, repeat | required; qty ≥1; ซื้อ/แถมตัวเดียวกันได้ |
| THRESHOLD | tiers[min,mode,value] | ≥1 tier; min เรียงขึ้น; pct ≤100 |
| BUNDLE | items[product,uom,qty], bundle_price, repeat | ≥2 สินค้าไม่ซ้ำ; ราคา bundle ต่ำกว่าราคาตั้งรวม |

### 6.4 Relationships

```text
promotion 1 ── N promotion_rule
promotion_rule 1 ── N promotion_rule_item
promotion 1 ── N promotion_approval_step
promotion 1 ── N promotion_usage
promotion 1 ── N promotion_audit
promotion N ── soft-ref ── Customer Group / Sales Channel / Item / GL Posting Group / Employee
promotion_usage N ── ref ── Invoice
```

## 7. User Stories & Acceptance Criteria

> Story title/intent แต่ละข้อเป็น single action; รายละเอียดเชิงผสมอยู่ใน AC

### US-01 สร้างโปรโมชัน

As a Sales/Marketing Officer, I want to สร้างโปรโมชัน, so that ใช้ข้อเสนอชั่วคราวกับกลุ่มเป้าหมายได้

- Given อยู่หน้า Promotion, When กด “สร้างโปรโมชัน”, Then เปิด wizard 3 ขั้น
- Given กรอกข้อมูลครบ, When กดบันทึกร่าง, Then ได้รายการสถานะ “ร่าง” พร้อม audit

### US-02 กำหนดเงื่อนไข

As a Sales/Marketing Officer, I want to เลือกเงื่อนไขหนึ่งชนิด, so that engine คำนวณตามโปรแกรมขาย

- Given เลือกชนิดใดชนิดหนึ่ง, When เปิดขั้นเงื่อนไข, Then เห็น editor ตรงชนิดนั้น
- Given ค่าไม่ผ่าน rule, When ไปขั้นถัดไป, Then แสดง error และไม่ย้ายขั้น

### US-03 ส่งอนุมัติ

As a Promotion Owner, I want to ส่งร่างเข้าสายอนุมัติ, so that ผู้มีอำนาจตรวจได้ตามลำดับ

- Given ร่าง valid, When เลือก assignee ทุก slot แล้วส่ง, Then chain ถูก freeze
- Given ผู้ส่งอยู่ใน candidate, When เปิด picker, Then ไม่พบผู้ส่ง

### US-04 ตัดสินรายการ

As a Current Approver, I want to อนุมัติหรือไม่อนุมัติ, so that โปรโมชันเดินสถานะถูกต้อง

- Given เป็น assignee ขั้นปัจจุบัน, When อนุมัติ, Then ส่งต่อขั้นถัดไปหรือมีผลตามวันที่
- Given ไม่อนุมัติพร้อมเหตุผล, When ยืนยัน, Then กลับร่างและเก็บ history

### US-05 ประเมินตะกร้า

As a Sales User, I want to ทดสอบตะกร้า, so that เห็นโปรโมชันที่ติดหรือข้ามก่อนนำไปใช้กับเอกสารขาย

- Given ลูกค้า ช่องทาง คูปอง และสินค้า, When คำนวณ, Then ladder เรียง priority พร้อมเหตุผล
- Given exclusive ติด, When engine ไปตัวถัดไป, Then หยุดและแสดงเหตุข้าม

### US-06 ควบคุมโปรโมชันมีผล

As a Sales Manager, I want to ระงับ เปิดต่อ หรือปิดก่อนกำหนด, so that ควบคุมรายการใหม่โดยไม่แก้ประวัติเดิม

- Given กำลังใช้, When ระงับพร้อมเหตุผล, Then เอกสารใหม่ไม่ได้โปรโมชัน
- Given ปิดก่อนกำหนด, When ยืนยันวันมีผล, Then action ย้อนกลับไม่ได้และเอกสารเดิมไม่เปลี่ยน

### US-07 ตรวจ usage

As a Promotion Owner, I want to ดูการใช้ งบ และบัญชี, so that ติดตามผลกระทบทางธุรกิจได้

- Given Invoice ใช้โปรโมชัน, When usage event สำเร็จ, Then uses/discount/customer ถูกเพิ่ม
- Given งบหรือโควตาครบ, When ประเมินใบใหม่, Then ข้ามพร้อมเหตุและแสดงสถานะหมด

## 8. Status & Lifecycle

```text
[*] → draft → pending_approval → scheduled → active ⇄ paused → ended
          └─ reject → draft             └─ budget_exhausted → ended_early
draft/pending_approval → cancelled
active/scheduled/paused/budget_exhausted → ended_early
```

| Current | Trigger | Next | Actor / Condition |
|---|---|---|---|
| — | create/copy/reject | draft | authorized maker |
| draft | submit | pending_approval | valid + assignees + overlap ack if needed |
| pending_approval | approve non-final | pending_approval | current assignee only |
| pending_approval | approve final | scheduled/active | compare valid_from with document date |
| pending_approval | reject | draft | reason required |
| active | pause/resume | paused/active | Sales Manager; reason on pause |
| active | budget/quota exhausted | budget_exhausted | System |
| active/scheduled/paused/budget_exhausted | end early | ended_early | Sales Manager; reason + effective date |
| draft/pending_approval | cancel | cancelled | authorized actor; reason |
| scheduled/active | clock | active/ended | System by validity |

## 9. Business Rules + Validation

### 9.1 Business Rules

| ID | Rule | Tag | Type / source |
|---|---|:---:|---|
| BR-01 | คำนวณจากราคาหลัง Price Resolver + TA ก่อน VAT | FIXED | confirmed |
| BR-02 | eligible เมื่อ active, date/scope/coupon/quota ตรง และไม่ paused/exhausted | DYNAMIC | promo-engine |
| BR-03 | LINE_DISC คิดต่อบรรทัด; บาทคูณ qty ฐาน; ไม่เกินยอด; ข้าม TA no-repeat | DYNAMIC | promo-engine |
| BR-04 | FREE_GOODS รวม qty ฐานแล้วหา repeat; line ของแถมราคา 0 | DYNAMIC | promo-engine |
| BR-05 | THRESHOLD ใช้ tier สูงสุด; BUNDLE ใช้จำนวนชุดต่ำสุด | DYNAMIC | promo-engine |
| BR-06 | priority น้อยก่อน; เท่ากันใช้ start ล่าสุด; exclusive หยุดตัวถัดไป | CONFIGURABLE | record values + fixed ordering |
| BR-07 | overlap ใช้ type+scope+target+date; ต้อง ack ตอน submit | DYNAMIC | validation function |
| BR-08 | overlap ไม่ยกเลิก/ตัดโปรโมชันเดิม | FIXED | confirmed |
| BR-09 | งบ/โควตา 0 = unlimited; เกินงบของใบให้ข้าม; 90% เป็น warning | CONFIGURABLE | record/config |
| BR-10 | โควตาต่อลูกค้านับต่อครั้ง Promotion จาก Invoice | FIXED | PM/BA confirmed |
| BR-11 | approved lock; เปลี่ยนเงื่อนไข/งบผ่าน copy | FIXED | confirmed |
| BR-12 | pause/resume/end/cancel จำกัดตาม state table | FIXED | lifecycle |
| BR-13 | ของแถมราคา 0; ATP อยู่ที่ SO; cost/stock ไป GL+Inventory | FIXED | cross-module |
| BR-14 | ส่วนลดคืน `gl_account` จาก GL Posting Group ให้ Invoice | FIXED | central contract |
| BR-15 | coupon uppercase; case-insensitive; format 3–20; unique ในโปรฯ ยังไม่จบ | CONFIGURABLE | validation |
| BR-16 | ไม่รองรับลูกค้ารายเดียว | FIXED | scope lock |
| BR-17 | audit append-only ทุก mutation/transition | FIXED | global contract |
| BR-DOA-01..07 | draft-only submit; resolve/freeze; sequential; SoD; reason; all slots | FIXED | DOA contract |

### 9.2 Validation Rules

| ID | Target | Condition | Result / visible text family |
|---|---|---|---|
| VR-01 | name, owner, GL, dates | required / valid range | block; “กรุณากรอกข้อมูลให้ครบถ้วน” |
| VR-02 | priority | integer 1–999 | block field |
| VR-03 | coupon | regex + uniqueness | block field |
| VR-04 | scope refs | group/channel requires ≥1 | block step |
| VR-05 | LINE_DISC | value >0, pct≤100, minQty≥1 | block step |
| VR-06 | FREE_GOODS | all product/uom/qty; qty≥1 | block step |
| VR-07 | THRESHOLD | ≥1, ascending min, valid value | block step |
| VR-08 | BUNDLE | unique ≥2, price >0 and below list total | block step |
| VR-09 | submit | assignees complete; overlap acknowledged | “เลือกผู้อนุมัติให้ครบทุกขั้น” / “ต้องยืนยันการทับซ้อนก่อนส่ง” |
| VR-10 | reject/cancel/pause/end | reason required | “กรุณากรอกข้อมูลให้ครบถ้วน” |
| VR-11 | approve | current assignee and submitter differs | “ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน” |
| VR-12 | concurrent save | version matches | reject conflict; reload current record |

### 9.3 Critical Decision Points

- **Eligibility:** trigger ตอน QT/SO ประเมิน; System ตัดสินจาก status/date/scope/coupon/quota; ผลคือ apply หรือ skipped พร้อมเหตุ; audit ที่ calculation trace
- **Approval:** trigger ตอน approver กด; current assignee ตัดสิน approve/reject; reject ต้องมีเหตุ; audit ทุกขั้น
- **Overlap:** trigger step 3/submit; maker ยืนยันว่าจะส่งต่อโดยไม่เปลี่ยนของเดิม; เก็บ overlapAck ผู้ยืนยันและเวลา

### 9.5 Flexibility Summary

| Rule | Marker | Level | Owner | Reason |
|---|:---:|---|---|---|
| BR-02..05 | ✅ | Rule/Engine Management | Sales business owner | เงื่อนไขโปรโมชันเป็น record data; algorithm อยู่ promo-engine |
| BR-06 | ✅ | Promotion record | Promotion owner | priority/exclusive ต่อรายการ |
| BR-09 | ✅ | Promotion record + Sales config | Promotion owner/Admin | budget/quota ต่อรายการ; warning threshold จาก config |
| BR-15 | ✅ | Config File for format; record for code | IT/Admin | format policy เปลี่ยนน้อย |
| DOA chain | ✅ | DOA central config | DOA Admin | ตำแหน่งและลำดับไม่ hardcodeใน feature |

## 10. Edge Cases

### 10.1 Confirmed from source

- ☑ EC-01 percentage >100, zero/negative values, invalid dates, duplicate item/tier/coupon → block (BR-03..05,15)
- ☑ EC-02 overlap requires explicit ack but preserves old promotion (BR-07,08)
- ☑ EC-03 submitter cannot be assignee/approver (BR-DOA)
- ☑ EC-04 reject/cancel/pause/end reason empty → block (BR-12,DOA)
- ☑ EC-05 coupon missing/wrong → skip with reason; case-insensitive match (BR-02,15)
- ☑ EC-06 TA no-repeat line → line promotion skipped (BR-03)
- ☑ EC-07 exclusive applied → later promotions skipped (BR-06)
- ☑ EC-08 budget/quota/per-customer exhausted → skip with reason (BR-09,10)
- ☑ EC-09 free-goods ATP shortage is handled by SO; promotion output remains deterministic (BR-13)
- ☑ EC-10 master record changed/deactivated → existing promotion keeps snapshot/reference display; new selection uses active source (BR-14/soft-ref)
- ☑ EC-11 approved record edit attempted → block and direct to copy (BR-11)
- ☑ EC-12 invoice usage retry → idempotent by invoice+promotion occurrence (BR-10,17)

### 10.2 Engineering safeguards `[AI-DEFAULT]`

- ☐ EC-AI-01 concurrent draft update → optimistic lock 409; no silent overwrite (CA-01)
- ☐ EC-AI-02 duplicate submit/approve click → idempotency key; one transition only (CA-08/ST)
- ☐ EC-AI-03 DOA config changes after submit → frozen snapshot remains unchanged (ST-05)
- ☐ EC-AI-04 API unauthorized/forbidden → 401/403 plus audit (PM-02/03)
- ☐ EC-AI-05 arithmetic uses decimal rounding consistently; no negative net (CL-03/04)

## 11. Impact / Regression Scope

New Feature; ไม่มี data migration. Regression ต้องครอบ Sales Price List, Trade Agreement, Quotation/SO price sequence, Invoice posting/usage และ Inventory free-goods hook เพื่อไม่ให้ Promotion เปลี่ยน contract เดิม

## 12. System Context & Cross-Module Impact

### 12.1 Value Stream

```text
Item/Customer/Group/Channel/GL + Price List + Trade Agreement + DOA
  → Promotion → Quotation / Sales Order → Invoice → GL + Usage
                                      └→ Free Goods → Inventory/ATP
```

| Direction/Module | Data / Trigger | แล้วไงต่อ | ถ้าแก้/ยกเลิก |
|---|---|---|---|
| Price List + TA → Promotion | unit after TA, promoAllowed | เป็นฐาน `calcPromo` | re-evaluate เฉพาะเอกสารที่ยังไม่ freeze ตาม contract QT/SO |
| Customer/Group/Channel → Promotion | group, default/doc channel | scope match | master changeไม่ย้อนแก้ snapshot เอกสารเดิม |
| Item Master → Promotion | product/category/uom/factor/list | validate rule + calculation | inactive itemหยุดเลือกใหม่; recordเดิมยัง audit ได้ |
| GL Posting Group → Promotion | contra-revenue / promo expense | engine คืน GL ให้ Invoice | inactive mappingต้อง block activation ใหม่ |
| DOA/Employee ↔ Promotion | slots, roles, assignees | freeze chain, My Approval | config changeไม่กระทบ in-flight |
| Promotion → QT/SO | discount, freeItems, skipped reason, gl | แสดงผลและล็อกผลตามเอกสาร | promotion later pause/end ไม่แก้เอกสารเดิม |
| Invoice → Promotion | usage event | เพิ่ม count/discount/customer idempotently | credit/reversal contract ต้องอ้าง event เดิมใน implementation |
| Promotion → Inventory | free item quantity | SO ตรวจ ATP; Invoice/fulfilmentตัด stock | shortageตัดสินที่ SO |
| Promotion → Campaign | future reference | ยังไม่เชื่อมรอบนี้ | ไม่มีผลในรอบนี้ |

### 12.2 Dependencies

- Locked references: Sales Price List, Trade Agreement, Customer Group, Sales Channel, Customer Master, Item Master, GL Posting Group, Inventory
- Missing feature references: Sales Quotation/Sales Order/Invoice ยังไม่มี pack; ใช้ Central Plan contract เท่านั้น
- Declaration used: DOA only

### 12.3 Existing System Reference

| Capability | Reuse | Contract |
|---|:---:|---|
| Price Resolver | ✅ | base price before Promotion |
| Trade Agreement engine | ✅ | net/discount + `promoAllowed` |
| DOA F-DLG-001 | ✅ | resolve sequential no-amount chain |
| Item/Customer/Group/Channel/GL masters | ✅ | lookup/soft-ref/snapshot |
| Inventory | ✅ | ATP/stock movement for free goods downstream |
| Document Configuration | future wiring | number format referenced, declaration skipped |
| Notification Center | future wiring | DOA/system events referenced, declaration skipped |
| Campaign Management | ❌ not available | future only |

## 13. Delivery Phases

### Phase 1 — Feature Launch

- Promotion entities, lifecycle, validation, approval hook, audit and usage idempotency
- `promo-engine` function/engine with 4 rule types and price-sequence contract
- Lookups to locked references; seed/mock values are examples, codes are contract
- No hardcoded DOA roles/assignees in feature logic

### Phase 2 — Admin Configuration

- Sales config for currency, expiring days and cross-engine order when central config is available
- Wire document numbering and notification only after their declarations/owners are ready

### Phase 3 — Rule/Engine Management

- Register `promo-engine` as reusable candidate if Architect approves
- Version calculation policy while preserving document snapshots

### Phase 4 — Future Integration

- Campaign Management references and combined campaign reporting

## 14. Dev Requirements Summary

### 14.1 Config Foundation

| Item | Requirement | Reuse |
|---|---|:---:|
| Promotion storage | header/rule/items/approval/usage/audit with version | new |
| DOA entry ref | `DOA-SALES-PROMO`; resolve from central config | ✅ DOA |
| Master adapters | code-based soft refs and snapshots | ✅ related features |
| Calculation trace | applied/skipped/freeItems/GL with deterministic order | new engine candidate |

### 14.2 Rules to implement

- Implement BR-01..17 and BR-DOA without embedding master names or approval chain
- Freeze approval chain at submit and pricing result at downstream document’s agreed point
- Make usage event idempotent and audit append-only
- Use decimal-safe money and base-UOM factor from Item Master

### 14.3 High-risk validation

- Boundary values for percent, priority, tier ordering, bundle price, dates, budget and quotas
- Permission + SoD + current-step enforcement at API and UI
- Double-submit, concurrent update and duplicate usage event
- Cross-feature order: Price List → TA → Promotion → downstream totals

### 14.4 Warnings / manual wiring

| Item | Owner | Status |
|---|---|---|
| ตั้งค่า DOA entry จริงตาม DOA_BRIEF | DOA Admin | manual after implementation |
| ลงทะเบียน `promo-engine` | Architect | proposal |
| เชื่อม Campaign | PM/BA | future scope |

### 14.5 Regression Scope

- Price List / TA calculations and `promoAllowed`
- QT/SO totals and free-goods rows
- Invoice GL/usage idempotency
- Inventory ATP/stock movement ownership

### 14.6 Screen Inventory + UI Signals

| P | Name | Route | Business type | Users | Purpose |
|---|---|---|---|---|---|
| P-01 | รายการโปรโมชัน | `#/promotions` | list + detail workbench | all roles | search/filter/status/actions |
| P-02 | รายละเอียดโปรโมชัน | `#/promotions` + view drawer | detail tabs | all roles | rule, usage, approval, history |
| P-03 | สร้าง/แก้โปรโมชัน | `#/promotions` + create/edit drawer | 3-step form | maker | author rule and submit |
| P-04 | ทดสอบตะกร้า | `#/promotions` + simulator drawer | calculator | sales users | verify eligibility and result |
| P-05 | Action confirmations | `#/promotions` + modal | confirmation | eligible actor | submit/approve/reject/cancel/pause/end |

**UI signals:** transaction with approval = yes; printable business document = no; PDF skipped; single hash route with stateful overlays; AS-BUILT source = Promotion.html

## 15. Open Questions

| ID | Status | Resolution / owner |
|---|:---:|---|
| OQ-01..08 from PREBRIEF | ✅ resolved | PM/BA confirmed decisions supplied in chat; reflected in Locks and rules |
| OQ-09 Campaign | ✅ scoped | future integration; no implementation now |
| OQ-10 engine registration | ⚠️ manual | Architect assigns registry id after review; does not block feature-local implementation |
| OQ-DOA-WIRE | ⚠️ manual | DOA Admin creates actual entry from DOA_BRIEF; no hardcode fallback |

## 16. Security & Compliance

### 16.1 Preset

**P2 — Approval/Workflow (14 controls).** เหตุผล: Promotion มี multi-step approval, price-impact logic, export และ audit; P2 covers P1 plus delegation/versioning. S01-01 applies as “DOA policy binding”; amount tier is explicitly unused for this feature.

### 16.2 Applicable Standards

| Standard | Applies | Reason |
|---|:---:|---|
| COSO | ✅ | Maker/Approver, DOA, audit |
| ISO 27001 | ✅ | access/session/input control |
| NIST CSF | ✅ | authorization and event trace |
| SOC 2 | ✅ | immutable evidence and reconciliation |
| SOX-style financial control | ✅ | discount/GL impact |
| OWASP API Security | ✅ | schema/auth/idempotency |
| PDPA / ISO 27701 | ✅ limited | employee/customer identifiers; no sensitive profile display |
| PCI DSS | ❌ | no payment card |
| HIPAA | ❌ | no health data |
| IEC 62443 / NIST OT | ❌ | no machine control |
| ISO 22301 | ✅ | sales continuity and audit recovery |
| NIST AI RMF | ❌ | no AI decision |
| GDPR portability/consent | ❌ feature-local | handled by master owners |
| Thai tax document control | ✅ downstream | Invoice/GL retains promotion reference |

### 16.3 P2 Control Checklist

| Control | Required | Implementation |
|---|:---:|---|
| S01-01 DOA policy binding | Must | resolve central entry; amount dimension unused |
| S01-02 Maker-Checker | Must | submitter excluded from approve |
| S01-03 Temporary Delegation | Must | accept delegated assignee from DOA snapshot + audit |
| S01-04 SoD conflict | Must | enforce API + UI |
| S01-06 Tolerance | Must | decimal/rounding/budget boundaries deterministic |
| S01-07 Immutable log | Must | promotion_audit append-only |
| S02-01 Password policy | Shared | IAM |
| S02-03 Session management | Shared | IAM/session layer |
| S03-02 Policy versioning | Must | `doa_entry_ref` + frozen chain |
| S04-05 Master mapping | Must | reference codes + snapshots |
| S04-06 SLA/escalation | Shared | expose pending age; channel wiring future |
| S06-03 Standard audit content | Must | who/what/when/before/after/result |
| S11-02 Change authorization | Must | ticket/ref supported for admin wiring |
| S14-02 Payload validation | Must | request schema + business validation |

### 16.4 Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Unauthorized/self approval | Medium | High | S01-02/03/04, frozen current assignee |
| Wrong discount/GL | Medium | High | S01-06, S04-05, deterministic trace, regression |
| Usage counted twice | Medium | High | S06-03, idempotency, reconciliation |
| Master/DOA changes alter in-flight record | Medium | High | S03-02, snapshots |

## 17. Health Check

### 17.1 SLA

| Step | Target | Owner | Breach action |
|---|---|---|---|
| List/search/simulator response | p95 ≤ 2 seconds at designed load | Engineering | performance alert |
| Submit → visible to current approver | ≤ 1 minute | DOA integration | retry/log; in-app queue remains source |
| Invoice → usage reflected | ≤ 5 minutes | Invoice integration | retry idempotently + reconciliation alert |
| Approval decision | business target ≤ 1 business day/step | selected approver | pending-age report; notification wiring future |

### 17.2 Runtime Control Points

| Control | Where | When | Expected result |
|---|---|---|---|
| S01-02/04 | submit + approve | pre-action | block self/unauthorized action |
| S03-02 | submit | transaction commit | freeze DOA version/chain |
| S01-06 | calcPromo | every evaluation | no over-discount/negative net |
| S04-05 | lookup + calculation | select/evaluate | codes map to source master version |
| S06-03 | all mutation | post-action | append audit record |
| S14-02 | every mutation endpoint | pre-action | invalid payload never persists |

### 17.3 KPI

| KPI | Category | Target | Formula/source |
|---|---|---|---|
| Promo calculation correctness | Quality | 100% regression pass | passed calc cases / total |
| SoD violation | Compliance | 0 | blocked/escaped self approvals |
| Usage reconciliation | Compliance | 100% | matched usage events / invoice promo occurrences |
| Approval turnaround | Speed | ≤1 business day median | approved_at - submitted_at per step |

### 17.4 Thresholds

| Metric | Green | Warn | Critical | Action |
|---|---|---|---|---|
| budget use | <90% | ≥90% | ≥100% | warn; then skip new applications |
| quota use | below limit | — | at limit | skip new applications |
| usage reconciliation | 100% | 99–<100% | <99% | retry; investigate |
| SoD escaped | 0 | — | >0 | security incident |
| p95 response | ≤2s | >2s | >5s | performance investigation |

### 17.5 Throughput

- Designed target: 100 concurrent sales users and 10,000 promotion evaluations/day
- Baseline: collect during pilot; no production baseline exists
- Stress point: 80 concurrent users or 8,000 evaluations/day; validate p95 and DB contention

## 18. Monitoring

### 18.1 Reports

| Report | Type | Frequency | Audience |
|---|---|---|---|
| Promotion performance | Performance | daily | Sales/Marketing Manager |
| Promotion closing/usage | Closing | monthly/end | Sales + Accounting |
| Promotion anomaly | Anomaly | real-time/daily | Manager + Auditor |
| Promotion transaction trail | Transaction | on-demand | Auditor/Support |

### 18.2 Widgets

| Widget | Source | Threshold |
|---|---|---|
| ใช้โปรโมชัน/ส่วนลด/ลูกค้า | §17.3 usage | budget/quota §17.4 |
| Approval pending age | §17.3 turnaround | >1 business day |
| Usage reconciliation | §17.3 reconciliation | <100% |
| Evaluation health | §17.3 correctness + response | fail or p95>2s |

### 18.3–18.6 Report Content

- Performance: uses, discount, customers, conversion by type/scope/channel and trend
- Closing: budget used/remaining, ended/exhausted items, Invoice/GL reconciliation
- Anomaly: self-approval attempts, rapid approvals, duplicate usage, excessive discount, master mapping failure
- Transaction: header versions, rule snapshots, calculation trace, state history, approval chain, usage/Invoice refs

## Appendix A — Glossary

- DOA: ทะเบียนสายอนุมัติกลาง
- TA: Trade Agreement
- Usage: จำนวนครั้งที่ Invoice ยืนยันการใช้โปรโมชัน
- Exclusive: เมื่อโปรโมชันติดแล้วหยุดประเมินตัวถัดไป
- Soft-reference: เก็บรหัสอ้างอิงและ snapshot โดยไม่ cascade เอกสารเก่า

## Appendix B — AI Review Summary

- Core C01–C23: 23/23 PASS
- Philosophy PE01–PE05: 5/5 PASS
- Critical issues: 0
- Informational manual follow-ups: DOA wiring, engine registry, future Campaign
- Verdict: **APPROVED — พร้อมเข้า frd-generator-v6**
