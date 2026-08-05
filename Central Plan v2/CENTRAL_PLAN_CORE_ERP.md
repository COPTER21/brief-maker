# CUBE 4.0 — Central Plan · Core ERP + Cubic Commercial (แผนกลาง 85 features)

> **v1.4 · 2026-08-04** · คู่กับ `CUBE_Core_ERP.html` (แผนที่ interactive — data sync แล้ว รอ regen แผนภาพ)
> **12 module · 85 feature · 151 เส้นเชื่อม · 8 สายงาน** · v1.4: **มติ — ระนาบขายแยกไป Cubic (site แยก physical)** + Commercial Architecture ครบ (3 ระนาบ · sellable flag · handoff C-TEN-01..03) + 2 features ฝั่ง tenant (My Subscription · My Linkage Settings)
> Knowledge sync: `cube-master-knowledge → 05_features/` — อัพเดตที่นี่ = อัพเดต HTML ด้วยเสมอ

## วิธีใช้ไฟล์นี้

**คน:** เปิดดู module ที่ตัวเองรับผิดชอบ (§3) — รู้ทันทีว่ากล่องเรามี feature อะไร รับอะไรเข้า ส่งอะไรออก ต้องเคารพกติกากลางข้อไหน

**AI (เปิดแชทพัฒนา module ใหม่):** แปะไฟล์นี้เข้าแชท แล้วสั่ง "ทำ [module] ตาม Central Plan" — AI ต้องอ่าน:
1. §2 Global Contracts (บังคับทุก module)
2. §3 เฉพาะกล่องตัวเอง — **Inbound = สิ่งที่ mock รอ / Outbound = สิ่งที่ต้อง expose**
3. §4 สายงานที่กล่องตัวเองอยู่ (ลำดับเอกสารจริง)

กติกาเดิมของทีมยังใช้: 1 แชท = 1 module = 1 ไฟล์ HTML · ข้าม module ใช้ data contract ผอม ๆ แล้ว mock · DOA pre-placeholder ทุก feature ที่มีอนุมัติ

---

## §1 ภาพรวม — 12 module · 3 ชั้น

| ชั้น | Module | Features |
|---|---|---|
| Foundation | **Policy & Security** · นโยบาย-สิทธิ์ | 4: Policy Document · DOA · Roles & Permissions · Permission Matrix |
| Foundation | **System** · ระบบและผู้ใช้ | 4: User Management · Menu Registry · Monitor Logs · Ticket |
| Foundation | **Organization** · โครงสร้างองค์กร | 4: Company · Cost Center · Fiscal Periods · Working Calendar |
| Foundation | **Product** · ข้อมูลสินค้า | 4: Item Master · Unit of Measure · Bill of Materials · Product Catalog |
| Foundation | **Platform** · แพลตฟอร์ม | 3: Notification · Audit Trail · Document Center |
| Foundation | 🟪 **Tenant & Packaging** · แพ็คเกจ-ผู้เช่า — **[CUBIC · site แยก]** | 7: Tenant Mgt · Onboarding · Package & Entitlement · Linkage Config · Signup Portal · Subscription & Billing · Instant Provisioning |
| Transactions | **Sales** · การขาย | 10: Customer Master · Customer Group · Sales Price List · Prospect · Sales Quotation · Sales Order · Sales Return · Sales Channel · Promotion · Sales Configuration |
| Transactions | **Warehouse** · คลังสินค้า | 11: Warehouse & Bin · Goods Receipt · Put Away · Return to Vendor · Picking · Packing · Delivery Note · Stocktake · Stock Adjustment · Stock Transfer · Inventory |
| Transactions | **Purchase** · การจัดซื้อ | 6: Vendor Master · Vendor Price List · Purchase Configuration · Purchase Requisition · Quotation Comparison · Purchase Order |
| Finance · People | **Finance** · การเงิน | 5: Bank Master · Payment Method · Receipt Voucher · Payment Voucher · Bank Reconciliation |
| Finance · People | **Accounting** · บัญชี | 15: Chart of Accounts · GL Posting Group · Tax Code · Payment Terms · AR Invoice · AP Invoice · Credit / Debit Note · GR/IR Clearing · Journal Entry · Opening Balance · Period Close · Trial Balance · Financial Statements · VAT Return (PP.30) · Withholding Tax |
| Finance · People | **HR** · บุคคล | 5: Employee Master · Time & Attendance · Leave Management · Payroll · Expense Claim |

**ลำดับพัฒนา (dependency):** Wave 1 Foundation ทั้ง 6 กล่อง (รวม Tenant & Packaging — ทุก feature ต้องอ่าน linkage)

**กลุ่ม module (v1.3 — ขยาย Global Contract #10):**
| กลุ่ม | Module | Lite/Full |
|---|---|---|
| **Sellable** (หน่วยขายใน Package & Entitlement) | Sales · Purchase · Warehouse · Product · HR · Finance · Accounting (Fin+Acc มัก bundle) | ✅ มี tier — tier = ชุดเส้นเชื่อมที่เปิด |
| **Shared Foundation** (มากับทุก package เสมอ — ไม่ใช่ของขาย) | Policy · System · Org & Company · Platform · Tenant & Packaging + master กลาง (UoM, Payment Terms, Working Calendar ฯลฯ) | ❌ ไม่มี tier — มีแต่ "อยู่ใน manifest ของ module ไหน" |
| **กรณีพิเศษ** | Item (อยู่ใน Product ซึ่งเป็นของขาย) | Item Lite = fallback เมื่อ tenant ไม่มี Product (OQ-LITE-01 รอ Strike) |

หลักจำ: **tier เกิดที่ module ขาย · master ไม่มี tier** — dual-mode (D7) มีเฉพาะเส้น [doc]/[post] ข้าม Sellable modules · เส้น [config] จาก Foundation = soft reference เหมือนเดิมทุกกรณี

### §1.5 Commercial Architecture — ระบบการขาย module (v1.4 · มติ: ระนาบขายอยู่ Cubic)

**3 ระนาบ (physical isolation):**
| ระนาบ | ใครใช้ | อยู่ไหน | มีอะไร |
|---|---|---|---|
| 🟪 **Provider plane** | ทีม 2B เท่านั้น | **Cubic** (cubic4.2bsimple.com — คนละระบบ คนละ DB คนละ credential กับ Core) | Tenant Mgt · Onboarding · Package & Entitlement (SKU master) · Module Linkage Config · Subscription & Billing (ฝั่งจัดการ) · Instant Provisioning |
| 🌐 **Public plane** | คนทั่วไป | หน้าเว็บ public (ยิงเข้า Cubic) | Signup Portal (สมัคร+เลือก module+จ่าย) |
| 🟦 **Tenant plane** | ลูกค้าแต่ละเจ้า | **Core** | ใช้ module ตาม entitlement + **My Subscription** (ดูสิทธิ์/บิล/ขอซื้อเพิ่ม) + **My Linkage Settings** (toggle เส้นที่ตัวเองมีสิทธิ์) — เห็นได้แค่ของตัวเองเสมอ |

**เหตุผลที่แยก Cubic (มติ v1.4):** isolation เป็น physical — Core พัง/โดน compromise ไม่ลามระนาบบริหารลูกค้าทุกเจ้า · deploy อิสระ · ตรงนิยาม Cubic เดิม · ตอบ security review ง่าย (ทีมยืนยันรับต้นทุนบริหาร 2 ระบบ)

**SKU / Package structure (Package & Entitlement):**
- `Package` = ชุด `module + tier` ที่ขาย เช่น Sales Lite = [Sales] · Sales Full = [Sales+Product+Warehouse]
- ทุก module/feature มี flag **`sellable: yes/no`** — ทุกอย่างในระนาบ Provider = `sellable: no` ถาวร **ห้ามโผล่ในทุก package** (ลูกค้าไม่มีทางซื้อ/เห็น Tenant Mgt)
- Entitlement ต่อ tenant = ผลรวม package ที่ซื้อ → Menu Registry render ตามนี้ → Linkage derive ตามนี้ (Contract #10)

**Handoff contracts รอยต่อ Cubic ↔ Core (ต้อง mock ตอนพัฒนาแยก):**
| # | เส้น | สัญญา |
|---|---|---|
| C-TEN-01 | Core อ่าน entitlement + linkage จาก Cubic | ผ่าน API + **cache ฝั่ง Core + fallback**: Cubic ล่ม ลูกค้าต้องใช้งานต่อได้ด้วยค่า cache ล่าสุด (ห้าม hard-depend runtime) |
| C-TEN-02 | Signup Portal (public) → Cubic | สมัคร/เลือก package/จ่าย → Billing → Instant Provisioning |
| C-TEN-03 | My Subscription (Core) ↔ Cubic | อ่านสิทธิ์/บิล (read) + ส่งคำขอ upgrade/ซื้อเพิ่ม (request — อนุมัติ/จ่ายจบที่ Cubic) |

**กติกาเหล็กใหม่ (ผูกทุก feature ระนาบ Provider):** TC ต้องมีชุด negative เสมอ — "login เป็น tenant ลูกค้าแล้วต้องเข้าไม่ได้/มองไม่เห็น 100%" → Wave 2 Transactions (Purchase/Warehouse คู่กัน, Sales) → Wave 3 Accounting → Finance → HR (HR เริ่มคู่ขนานได้ ติดแค่ Company + DOA)

---

## §2 Global Contracts — กติกากลางที่ทุก module ต้องยึด

1. **DOA ครอบเอกสารต้องเซ็นทั้งหมด (19 ใบ)** — feature ที่ออกเอกสารต่อไปนี้ ต้องมี field `approver_role / approved_by / approval_chain` + comment `TODO: DOA engine` ห้าม hardcode สายอนุมัติ:
   Sales Quotation · Sales Order · Sales Return · PR · Quotation Comparison · PO · Return to Vendor · AP Invoice · Credit/Debit Note · Stocktake · Stock Adjustment · Stock Transfer · Opening Balance · Journal Entry · Period Close · Payment Voucher · Leave · Expense Claim · Payroll
2. **Inventory เป็นแกน check stock** — เอกสารขาย (SQ/SO) ต้องเรียกเช็คยอดก่อนเสนอ/ยืนยัน · ทุก movement (Put Away, Picking, Adjustment, Transfer, RTV, Sales Return) ต้องอัพเดต Inventory · มูลค่าสต็อกลง GL ผ่าน Journal Entry
3. **Item Master ตัวเดียว สองสวิตช์** — สินค้าเข้าเอกสารซื้อได้เฉพาะตั้งค่า "ซื้อได้" · เข้าเอกสารขาย (SQ/SO) เฉพาะ "ขายได้"
4. **Company รวมโครงองค์กร** — สาขา/สายงาน/แผนก/ตำแหน่ง เป็นข้อมูลใน Company ใบเดียว · Employee อยู่ HR ไม่อยู่ Organization · โครงตำแหน่งเป็นฐานตั้งสายอนุมัติ (Company → DOA)
5. **Posting period control** — Journal Entry ลงได้เฉพาะงวดที่เปิด (Fiscal Periods คุม) · ปิดงวดเป็นเอกสารมี DOA
6. **Soft-reference (LD-4C-02)** — master ใช้เป็น picker input เท่านั้น ไม่ทำ FK cascade · คอลัมน์ nullable · enforce เฉพาะ format + uniqueness
7. **Append-only audit · soft archive · ไม่มี hard delete** ทุก module
8. **Prospect convert เป็น Customer ได้** — ปิดการขายจาก Prospect ต้องมีปุ่ม convert → เปิด Customer Master (CRM standard)
9. **CI ล็อก** ตาม html-generator-v6 (CUBE Warm Light) · 1 แชท = 1 module = 1 ไฟล์ SPA
10. **Entitlement → Linkage 3 ชั้น (Lite/Full editions)** — ชั้น1 `Package & Entitlement` ต่อ tenant กำหนดว่า "ซื้อ/เปิด module อะไร" → ชั้น2 `Module Linkage Config` derive อัตโนมัติว่าเส้นข้าม module เส้นไหน active (**ปลายทางไม่เปิด = force `manual`** ตาม Module Linkage Pattern §7 ของ KNOWLEDGE_SNAPSHOT) → ชั้น3 ทุก feature อ่าน linkage ตอน **runtime** แล้วสลับพฤติกรรม: `linked` = สถานะ auto/read-only + badge 🔗 · `manual` = dropdown/ปุ่มปรับเอง + audit + badge ✋
    - **Lite/Full = feature เดียว โค้ดเดียว ห้าม fork** — ต่างกันที่ linkage เปิด/ปิด · โหมด manual ไม่ใช่แค่ "ปิดของ" แต่ต้อง"เพิ่ม fallback" (ช่องกรอก/ปุ่มปรับสถานะเอง) เข้าไปใน feature เดียวกัน
    - **ทุกเส้นข้าม module ต้องนิยามพฤติกรรม 2 โหมด (เชื่อม/ไม่เชื่อม) ตั้งแต่ PREBRIEF** (แหล่ง derive D7 ของ feature-prebrief)
    - ตัวอย่าง SKU: **Sales Lite** = [Sales] จบใน module (Quotation→SO · จัดส่ง/บิล/รับเงิน = สถานะ manual) · **Sales Full** = [Sales + Product + Warehouse (+Accounting/Finance)] เชื่อม inventory + บิลอัตโนมัติ
    - ⚠ **OQ-LITE-01 (Strike):** Sales Lite ไม่มี Product module → ขายด้วยอะไร: (ก) Item Lite ฝังใน Sales แล้ว migrate ตอน upgrade หรือ (ข) บังคับ Product เป็นฐานทุก package

---

## §2.5 Data Contracts — เชื่อมข้อมูลระดับ field (หลัก "อะไรดึง อะไรส่ง")

### หลักทิศทางข้อมูล 5 แบบ (ทุกเส้นในแผนที่เป็น 1 ใน 5 นี้)

| แบบ | ทิศ | หลักการ | ตัวอย่าง |
|---|---|---|---|
| `config` master → เอกสาร | **PULL ตอนสร้าง** | เอกสารเปิด picker ดึง master แล้ว **snapshot ค่าลงเอกสาร** (ชื่อ/ราคา/เงื่อนไข ณ วันนั้น) — ไม่ lookup สดย้อนหลัง สอดคล้อง soft-reference | Customer → SO · Price List → SQ |
| `doc` เอกสาร → เอกสาร | **PUSH สร้างใบต่อ** | ใบปลายทางสร้างจากใบต้นทาง: copy header+lines ที่เกี่ยว + เก็บ `ref_doc_no` เสมอ + ยอดสะสม (เช่น qty_received) กันเกิน | SQ→SO · PO→GR |
| `post` เอกสาร → บัญชี | **POST event** | เอกสาร operational จบ → ยิงรายการบัญชีอัตโนมัติผ่าน GL Posting Group — คนไม่คีย์ JE เอง | GR→GR/IR · Payroll→JE |
| `gov` DOA → เอกสาร | **STATE MACHINE** | เอกสาร draft→pending→approved/rejected · DOA ตัดสินสายเซ็นจาก (ชนิดเอกสาร, วงเงิน, หน่วยงาน) · ห้าม hardcode | DOA→PO |
| `event` → แพลตฟอร์ม | **FIRE & FORGET** | แจ้งเตือน/log แบบ async ไม่บล็อกงานหลัก | DOA→Notification |

### โครง field กลาง (ทุกเอกสารใช้ร่วม)

```
DocHeader: doc_no · doc_date · status · ref_doc_type+ref_doc_no · company · branch
           created_by · approver_role · approved_by · approval_chain  ← DOA placeholder
DocLine:   line_no · item_code · item_name(snapshot) · qty · uom
           unit_price(snapshot) · discount · tax_code · line_amount · cost_center
```

### Handoff contract รายคู่สำคัญ (field ที่ต้องส่งต่อกันจริง)

| Handoff | ส่งอะไร | กติกา standard |
|---|---|---|
| Prospect → Customer | ชื่อ/ผู้ติดต่อ/ช่องทาง → เปิด customer + ผูก prospect_id ย้อนดูที่มา | CRM lead conversion — convert แล้ว prospect ปิดสถานะ ไม่ลบ |
| SQ → SO | quote_no, customer(snapshot), lines+ราคาที่ตกลง, valid_until | SO อ้าง quote เดียวหรือรวมหลาย quote ไม่ได้ (1:N จาก quote ฝั่งแก้ revision) |
| Inventory → SQ/SO | ยอด available = on_hand − allocated (+planned receipts เฟสถัดไป) | **ATP check** — เช็คก่อนยืนยัน กันรับปากเกินของ (SAP/D365 order promising) |
| SO → Picking | so_no, warehouse, ship_to, lines{item, qty_to_pick} | หยิบได้ ≤ qty_ordered − qty_picked สะสม |
| Picking → Packing → DN | qty_picked จริงต่อ line → DN คือหลักฐานส่ง | **AR Invoice ออกตามส่งจริง (bill from delivery)** ไม่ใช่ตาม SO |
| PR → CP | pr_no, lines, cost_center, need_by_date | PR ระบุศูนย์ต้นทุนตั้งแต่ขอ (budget dimension) |
| CP → PO | ผู้ขายที่เลือก + ราคา/เงื่อนไขที่ตกลง + เหตุผลเลือก | ผลเทียบต้องผ่าน DOA ก่อนออก PO |
| PO → GR | po_no, lines{qty_ordered, qty_received_สะสม} | **รับของที่ราคา PO เสมอ** · รับได้ ≤ ค้างรับ + tolerance |
| GR ↔ AP Invoice | จับคู่ po_no + gr_no + invoice: เทียบ qty·price·value | **3-way match** — ใน tolerance = ผ่านจ่าย · เกิน = block รอเคลียร์ (SAP MIRO/OMR6) |
| GR → GR/IR → AP | GR: Dr สต็อก / Cr GR/IR (ราคา PO) → AP: Dr GR/IR / Cr เจ้าหนี้ | GR/IR = บัญชีพักสะพานระหว่าง "รับของแล้ว" กับ "ใบแจ้งหนี้มา" เคลียร์รายบรรทัด PO |
| movement → Inventory | item, warehouse/bin, qty_delta(±), movement_type, ref_doc | ยอดคงเหลือห้ามแก้ตรง — เปลี่ยนได้ผ่าน movement เท่านั้น (ledger principle) |
| Stocktake → Adjustment | ผลนับ vs ยอดระบบ → ส่วนต่างออกใบปรับ (ผ่าน DOA) | นับไม่แก้ยอดเอง — แก้ผ่านเอกสารปรับเสมอ |
| Payroll → JE | สรุปยอดต่อ cost center (ไม่ลงรายคน) | GL เก็บ summary · รายคนอยู่ payroll register |
| Expense Claim → AP → PV | เบิกอนุมัติแล้วตั้งหนี้พนักงาน → จ่ายรวมรอบจ่ายปกติ | reimbursement ผ่าน AP ไม่จ่ายลัด |

---

## §3 รายกล่อง — features + contracts เข้า/ออก


### ▌Foundation — ต้องมีก่อน เปิดเอกสารไม่ได้ถ้าขาด


#### Policy & Security · นโยบาย-สิทธิ์ (4)

| Feature | ไทย | สถานะ | หมายเหตุ |
|---|---|---|---|
| Policy Document | เอกสารนโยบาย | อยู่ Registry (ระบบเดิมมี) | — |
| DOA | สายอนุมัติ (DOA) | อยู่ Registry (ระบบเดิมมี) | ทุก feature วาง placeholder แล้ว |
| Roles & Permissions | บทบาท-สิทธิ์ | อยู่ Registry (ระบบเดิมมี) | — |
| Permission Matrix | ตารางสิทธิ์ | ยังไม่เคยนับ — ต้องเริ่มใหม่ | — |

**รับเข้า (Inbound — เวลาพัฒนาแยก ให้ mock ของพวกนี้):**
- `User Management (System)` → **Roles & Permissions** — ผู้ใช้ ← บทบาท
- `Company (Organization)` → **DOA** — โครงตำแหน่ง → ตั้งสายอนุมัติ

**ส่งออก (Outbound — สิ่งที่กล่องนี้ต้อง expose ให้คนอื่น):**
- **DOA** → `Purchase Requisition (Purchase)` — อนุมัติขอซื้อ
- **DOA** → `Purchase Order (Purchase)` — อนุมัติสั่งซื้อ
- **DOA** → `Sales Order (Sales)` — อนุมัติส่วนลด
- **DOA** → `Payment Voucher (Finance)` — อนุมัติจ่าย
- **DOA** → `Journal Entry (Accounting)` — อนุมัติรายการปรับ
- **DOA** → `Leave Management (HR)` — อนุมัติลา
- **DOA** → `Notification (Platform)` — ถึงคิวอนุมัติ → แจ้ง
- **DOA** → `Sales Quotation (Sales)` — อนุมัติราคา/ส่วนลดเสนอ
- **DOA** → `Quotation Comparison (Purchase)` — อนุมัติผลเทียบราคา
- **DOA** → `AP Invoice (Accounting)` — อนุมัติตั้งหนี้ (3-way)
- **DOA** → `Credit / Debit Note (Accounting)` — อนุมัติลด/เพิ่มหนี้
- **DOA** → `Sales Return (Sales)` — อนุมัติรับคืน
- **DOA** → `Return to Vendor (Warehouse)` — อนุมัติคืนผู้ขาย
- **DOA** → `Stocktake (Warehouse)` — อนุมัติผลนับสต็อก
- **DOA** → `Stock Adjustment (Warehouse)` — อนุมัติปรับยอด
- **DOA** → `Stock Transfer (Warehouse)` — อนุมัติโอนคลัง
- **DOA** → `Opening Balance (Accounting)` — อนุมัติยอดยกมา
- **DOA** → `Period Close (Accounting)` — อนุมัติปิดงวด
- **DOA** → `Expense Claim (HR)` — อนุมัติเบิก
- **DOA** → `Payroll (HR)` — อนุมัติงวดเงินเดือน
- **Permission Matrix** → `Menu Registry (System)` — เมนูตามสิทธิ์

**เส้นในกล่อง:** Policy Document→DOA (นโยบาย → สายอนุมัติ) · Roles & Permissions→Permission Matrix (สรุปเป็นตารางสิทธิ์) · Policy Document→Roles & Permissions (นโยบาย → กรอบสิทธิ์)

#### System · ระบบและผู้ใช้ (6)

| Feature | ไทย | สถานะ | หมายเหตุ |
|---|---|---|---|
| User Management | ผู้ใช้ | อยู่ Registry (ระบบเดิมมี) | — |
| Menu Registry | ทะเบียนเมนู | ยังไม่เคยนับ — ต้องเริ่มใหม่ | consume TENANT_ENTITLEMENT |
| Monitor Logs | System Log / Error | ยังไม่เคยนับ — ต้องเริ่มใหม่ | — |
| Ticket | Ticket Feature | อยู่ Registry (ระบบเดิมมี) | — |
| My Subscription | แพ็คเกจของฉัน | ยังไม่พัฒนา (v1.4) | ฝั่ง tenant: ดู package/module ที่เปิด · บิล/รอบชำระ · ขอ upgrade/ซื้อเพิ่ม (ยิง request ไป Cubic — C-TEN-03) · read+request เท่านั้น |
| My Linkage Settings | ตั้งค่าการเชื่อมของฉัน | ยังไม่พัฒนา (v1.4) | ฝั่ง tenant: toggle เชื่อม/manual เฉพาะเส้นที่ entitlement เปิดสิทธิ์ (เช่น ซื้อ Full แต่ขอ run manual ก่อน) — เงาของ Linkage Config scope ตัวเอง |

**รับเข้า (Inbound — เวลาพัฒนาแยก ให้ mock ของพวกนี้):**
- `Employee Master (HR)` → **User Management** — พนักงาน → ผู้ใช้
- `Permission Matrix (Policy & Security)` → **Menu Registry** — เมนูตามสิทธิ์

**ส่งออก (Outbound — สิ่งที่กล่องนี้ต้อง expose ให้คนอื่น):**
- **User Management** → `Roles & Permissions (Policy & Security)` — ผู้ใช้ ← บทบาท
- **Ticket** → `Notification (Platform)` — อัพเดต ticket → แจ้ง
- **Monitor Logs** → `Notification (Platform)` — ระบบผิดพลาด → แจ้งทีม
- **User Management** → `Audit Trail (Platform)` — log เข้าใช้/เปลี่ยนสิทธิ์

**เส้นในกล่อง:** User Management→Ticket (ผู้แจ้ง/ผู้รับผิดชอบ)

#### Organization · โครงสร้างองค์กร (4)

| Feature | ไทย | สถานะ | หมายเหตุ |
|---|---|---|---|
| **— STRUCTURE · โครงสร้าง —** | | | |
| Company | บริษัท | อยู่ Registry (ระบบเดิมมี) | — |
| Cost Center | ศูนย์ต้นทุน | อยู่ Registry (ระบบเดิมมี) | — |
| **— PERIODS · งวดและปฏิทิน —** | | | |
| Fiscal Periods | ปีบัญชีและงวด | อยู่ Registry (ระบบเดิมมี) | — |
| Working Calendar | ปฏิทิน/วันหยุด | ยังไม่เคยนับ — ต้องเริ่มใหม่ | ใช้คำนวณ SLA/overdue |

**ส่งออก (Outbound — สิ่งที่กล่องนี้ต้อง expose ให้คนอื่น):**
- **Company** → `Warehouse & Bin (Warehouse)` — คลังสังกัดสาขาในบริษัท
- **Cost Center** → `Journal Entry (Accounting)` — มิติต้นทุน
- **Fiscal Periods** → `Period Close (Accounting)` — งวดบัญชี
- **Company** → `Employee Master (HR)` — สังกัด สายงาน ตำแหน่ง
- **Working Calendar** → `Time & Attendance (HR)` — วันทำงาน/วันหยุด
- **Cost Center** → `Expense Claim (HR)` — เบิกลงศูนย์ต้นทุน
- **Company** → `DOA (Policy & Security)` — โครงตำแหน่ง → ตั้งสายอนุมัติ
- **Cost Center** → `Purchase Requisition (Purchase)` — ระบุศูนย์ต้นทุนตอนขอซื้อ
- **Fiscal Periods** → `Journal Entry (Accounting)` — คุมงวดที่ลงบัญชีได้

#### Product · ข้อมูลสินค้า (4)

| Feature | ไทย | สถานะ | หมายเหตุ |
|---|---|---|---|
| **— MASTER · ข้อมูลหลัก —** | | | |
| Item Master | สินค้า/วัสดุ | เสร็จครบ pipeline | F-PRODUCT-MASTER-001 |
| Unit of Measure | หน่วยวัด | เสร็จครบ pipeline | F-UOM-MASTER-001 |
| **— STRUCTURE · โครงสินค้า —** | | | |
| Bill of Materials | สูตร/ชุดสินค้า | เสร็จครบ pipeline | F-BOM-001 |
| Product Catalog | แค็ตตาล็อกสินค้า | เสร็จครบ pipeline | ⚠ Central Plan ยังขึ้น "ต้องทำ" |

**ส่งออก (Outbound — สิ่งที่กล่องนี้ต้อง expose ให้คนอื่น):**
- **Product Catalog** → `Sales Price List (Sales)` — ตั้งราคาตามแค็ตตาล็อก
- **Item Master** → `Purchase Order (Purchase)` — เฉพาะสินค้าที่ตั้งค่า "ซื้อได้"
- **Item Master** → `Sales Order (Sales)` — เฉพาะสินค้าที่ตั้งค่า "ขายได้"
- **Item Master** → `Inventory (Warehouse)` — สินค้าที่ติดตามสต็อก
- **Item Master** → `Sales Quotation (Sales)` — สินค้าที่ตั้งค่า "ขายได้"

**เส้นในกล่อง:** Unit of Measure→Item Master (หน่วยนับ) · Bill of Materials→Item Master (สูตร/ชุด) · Item Master→Product Catalog (จัดเข้าแค็ตตาล็อก)

#### Platform · แพลตฟอร์ม (3)

| Feature | ไทย | สถานะ | หมายเหตุ |
|---|---|---|---|
| Notification | Notification Center | อยู่ Registry (ระบบเดิมมี) | F-NT-01/02/03 |
| Audit Trail | Audit Trail กลาง | อยู่ Registry (ระบบเดิมมี) | append-only |
| Document Center | ศูนย์เอกสาร/ไฟล์ | ยังไม่เคยนับ — ต้องเริ่มใหม่ | ★ ทุก module แนบไฟล์ แต่ไม่มีที่เก็บกลาง |

**รับเข้า (Inbound — เวลาพัฒนาแยก ให้ mock ของพวกนี้):**
- `DOA (Policy & Security)` → **Notification** — ถึงคิวอนุมัติ → แจ้ง
- `Journal Entry (Accounting)` → **Audit Trail** — ทุกรายการเก็บ log
- `Ticket (System)` → **Notification** — อัพเดต ticket → แจ้ง
- `Monitor Logs (System)` → **Notification** — ระบบผิดพลาด → แจ้งทีม
- `User Management (System)` → **Audit Trail** — log เข้าใช้/เปลี่ยนสิทธิ์

**ส่งออก (Outbound — สิ่งที่กล่องนี้ต้อง expose ให้คนอื่น):**
- **Document Center** → `Goods Receipt (Warehouse)` — แนบใบส่งของผู้ขาย
- **Document Center** → `AP Invoice (Accounting)` — แนบใบกำกับภาษี
- **Document Center** → `Expense Claim (HR)` — แนบใบเสร็จเบิก
- **Document Center** → `Sales Order (Sales)` — แนบ PO ลูกค้า

#### 🟪 Cubic · Tenant & Packaging — แพ็คเกจ-ผู้เช่า (7) — **SITE แยก (ไม่ใช่ area ใน Core)**

> ระนาบ Provider (2B เท่านั้น — ดู §1.5): ตอบว่า "tenant นี้ซื้ออะไร เปิด module ไหน เส้นไหน active" — **คนละระบบ/DB/credential กับ Core** ลูกค้าเข้าไม่ได้โดยสถาปัตยกรรม · Core อ่านผ่าน C-TEN-01 (cache+fallback) · ยังไม่พัฒนาทั้งกล่อง — เข้าคิว W1-W2 (user craft เอง)

| Feature | ไทย | สถานะ | หมายเหตุ |
|---|---|---|---|
| Tenant Management | จัดการผู้เช่า | ยังไม่พัฒนา — ต้องเริ่มใหม่ | provision บริษัทลูกค้า + สถานะ tenant · engine: ENG-TENANT-PROVISIONER |
| Onboarding | ขึ้นระบบลูกค้าใหม่ | ยังไม่พัฒนา (มีเอกสาร 6 phase ใน registry) | Contract→Provision→Data Prep→Import/Config→UAT→Go-live · CSV chain + ENG-CSV-IMPORT-VALIDATOR |
| Package & Entitlement | แพ็คเกจและสิทธิ์ใช้งาน | ยังไม่พัฒนา | SKU master: Lite/Full = ชุด module+feature ที่เปิดต่อ tenant — ฝ่ายขายใช้ |
| Module Linkage Config | ตั้งค่าการเชื่อม module | ยังไม่พัฒนา | matrix ต่อ tenant: เส้นข้าม module active/manual — derive จาก entitlement + toggle ได้ · ปลายทางปิด = force manual |
| **— SELF-SERVICE · สมัครเองแบบ Odoo (v1.3) —** | | | |
| Signup Portal | สมัครใช้งานหน้าบ้าน | ยังไม่พัฒนา | หน้า public: สมัคร + เลือก module/package (อ่าน SKU จาก Package & Entitlement) + คำนวณราคา |
| Subscription & Billing | ชำระเงิน-รอบบิล | ยังไม่พัฒนา | payment gateway + subscription/ต่ออายุ + upgrade/downgrade package + ใบกำกับ |
| Instant Provisioning | เปิดระบบทันที | ยังไม่พัฒนา | จ่ายสำเร็จ → สร้าง tenant + เปิด entitlement + derive linkage อัตโนมัติ → พร้อมใช้ทันที (orchestrate ENG-TENANT-PROVISIONER) |

**รับเข้า (Inbound):** — (ชั้นนี้อยู่เหนือ Core — ไม่รับจากเอกสารใน Core)

**ส่งออก (Outbound — สิ่งที่กล่องนี้ต้อง expose ให้คนอื่น):**
- **Package & Entitlement** → `Menu Registry (System)` — เมนู/feature เปิดตาม entitlement (Menu Registry มี note consume TENANT_ENTITLEMENT อยู่แล้ว)
- **Module Linkage Config** → `Sales Order (Sales)` — *ตัวแทน* ของ "ทุกเอกสารข้าม module อ่าน linkage ตอน runtime" (จงใจวาดเส้นเดียวกันรก — ดู §6)
- **[C-TEN-01]** Cubic → Core: entitlement + linkage ผ่าน API — **Core ต้อง cache + fallback** (Cubic ล่ม ลูกค้าใช้งานต่อได้)
- **[C-TEN-03]** Package & Entitlement ↔ `My Subscription (System · Core)` — read สิทธิ์/บิล + รับคำขอ upgrade
- **Module Linkage Config** → `My Linkage Settings (System · Core)` — scope เส้นที่ tenant มีสิทธิ์ toggle

**เส้นในกล่อง:** Tenant Management→Onboarding (เปิด tenant → เริ่มขึ้นระบบ) · Onboarding→Package & Entitlement (เลือก package ตอน onboarding) · Package & Entitlement→Module Linkage Config (derive matrix อัตโนมัติ) · **v1.3:** Package & Entitlement→Signup Portal (SKU/ราคาที่โชว์หน้าบ้าน) · Signup Portal→Subscription & Billing (สมัครแล้วไปจ่ายเงิน) · Subscription & Billing→Instant Provisioning (จ่ายสำเร็จ → เปิดระบบ) · Instant Provisioning→Tenant Management (สร้าง tenant อัตโนมัติ) · Instant Provisioning→Package & Entitlement (เปิดสิทธิ์ตามที่ซื้อ)

> **2 เส้นทางขึ้นระบบ:** (1) **Self-service** — Signup→Billing→Instant Provisioning เริ่มใช้เองทันทีแบบ Odoo (ลูกค้าเล็ก/ลองใช้) · (2) **Guided** — Onboarding 6 phase มีทีมพาขึ้น (ลูกค้า enterprise เช่น Credence) — ปลายทางเดียวกัน: tenant + entitlement + linkage

### ▌Transactions — เอกสารเดินงานจริง


#### Sales · การขาย (15) — Sellable · Lite/Full ✅ (แผน deliver ลูกค้าตัวแรก)

| Feature | ไทย | สถานะ | หมายเหตุ |
|---|---|---|---|
| **— MASTER · ข้อมูลหลัก —** | | | |
| Customer Master | ลูกค้า | มี HTML/บางส่วน | sales-module.html |
| Customer Group | กลุ่มลูกค้า | อยู่ Central Plan เดิม | W1 |
| Sales Price List | บัญชีราคาขาย | อยู่ Central Plan เดิม | W1 |
| **— PIPELINE · ก่อนขาย —** | | | |
| Prospect | ผู้สนใจ (ลีด) | เสร็จครบ pipeline | core-marketing-prospect.html |
| **— ORDERS · เอกสารขาย —** | | | |
| Sales Quotation | ใบเสนอราคา | มี HTML/บางส่วน | W3 |
| Sales Order | คำสั่งขาย | มี HTML/บางส่วน | W3 |
| Sales Return | รับคืนจากลูกค้า | อยู่ Central Plan เดิม | W7 |
| **— FIELD OPS · งานภาคสนาม/ร้านย่อย (v1.3 จาก sales-module.html) —** | | | |
| Sales Territory | เขตการขาย/สายวิ่ง | มี HTML/บางส่วน | sales-module.html · master เขต+พนักงานขายประจำสาย |
| Trade Agreement | ข้อตกลงการค้า | มี HTML/บางส่วน | sales-module.html · เงื่อนไข/ราคา/เป้าต่อลูกค้ารายสัญญา |
| Sales Target | เป้าการขาย | มี HTML/บางส่วน | sales-module.html · เป้าต่อเขต/พนักงาน เทียบยอดจริง |
| Visit Operation | ตรวจเยี่ยมร้านย่อย | มี HTML/บางส่วน | sales-module.html · Journey Plan ตามสาย + check-in พิกัด + เช็คสต๊อกร้านย่อย (ลูกค้าของลูกค้า) + survey + แผนที่เส้นทาง |
| Outlet Replenishment | เติมของร้านย่อย | ยังไม่พัฒนา | จากผลเช็คสต๊อกตอนเยี่ยม → สร้างคำสั่งเติม → ออก Sales Order อัตโนมัติ |
| **— CHANNEL & PROMO · ช่องทาง-โปรฯ —** | | | |
| Sales Channel | ช่องทางการขาย | อยู่ Central Plan เดิม | W1 |
| Promotion | โปรโมชัน | มี HTML/บางส่วน | W3 |
| **— CONFIG · ตั้งค่า —** | | | |
| Sales Configuration | ตั้งค่าการขาย | อยู่ Central Plan เดิม | W1 |

**รับเข้า (Inbound — เวลาพัฒนาแยก ให้ mock ของพวกนี้):**
- `Delivery Note (Warehouse)` → **Sales Return** — ลูกค้าคืนของ
- `Product Catalog (Product)` → **Sales Price List** — ตั้งราคาตามแค็ตตาล็อก
- `Item Master (Product)` → **Sales Order** — เฉพาะสินค้าที่ตั้งค่า "ขายได้"
- `DOA (Policy & Security)` → **Sales Order** — อนุมัติส่วนลด
- `Inventory (Warehouse)` → **Sales Quotation** — เช็คของก่อนเสนอราคา
- `Inventory (Warehouse)` → **Sales Order** — เช็คสต็อก + กันยอด
- `DOA (Policy & Security)` → **Sales Quotation** — อนุมัติราคา/ส่วนลดเสนอ
- `DOA (Policy & Security)` → **Sales Return** — อนุมัติรับคืน
- `Item Master (Product)` → **Sales Quotation** — สินค้าที่ตั้งค่า "ขายได้"
- `Document Center (Platform)` → **Sales Order** — แนบ PO ลูกค้า

**ส่งออก (Outbound — สิ่งที่กล่องนี้ต้อง expose ให้คนอื่น):**
- **Sales Order** → `Picking (Warehouse)` — สั่งหยิบของ
- **Sales Return** → `Credit / Debit Note (Accounting)` — ออกใบลดหนี้
- **Sales Return** → `Inventory (Warehouse)` — รับของกลับเข้าคลัง

**เส้นในกล่อง (เพิ่ม v1.3):** Sales Territory→Customer Master (ผูกลูกค้าเข้าเขต/สาย) · Sales Territory→Visit Operation (จัดสายเยี่ยม) · Sales Territory→Sales Target (เป้าต่อเขต) · Customer Master→Visit Operation (ร้านย่อยที่เยี่ยม) · Trade Agreement→Sales Order (เงื่อนไข/ราคาตามสัญญา) · Visit Operation→Outlet Replenishment (ผลเช็คสต๊อก → สั่งเติม) · Outlet Replenishment→Sales Order (สร้าง SO เติมของ)

**เส้นในกล่อง:** Prospect→Sales Quotation (ลูกค้ามุ่งหวัง → เสนอราคา) · Sales Quotation→Sales Order (ลูกค้าตอบรับ) · Customer Group→Sales Price List (ราคาต่อกลุ่มลูกค้า) · Sales Price List→Sales Quotation (ดึงราคา) · Customer Master→Sales Order (ลูกค้า) · Promotion→Sales Order (โปรฯ/ส่วนลดผูกตอนเปิดออเดอร์) · Sales Channel→Sales Order (ระบุช่องทางที่ขาย) · Customer Master→Sales Quotation (ลูกค้าในใบเสนอราคา) · Promotion→Sales Quotation (ส่วนลดตอนเสนอราคา) · Prospect→Customer Master (ปิดการขายได้ → convert เป็นลูกค้า) · Sales Configuration→Sales Order (กติกาการขาย) · Customer Group→Customer Master (จัดกลุ่มลูกค้า)

#### Warehouse · คลังสินค้า (11)

| Feature | ไทย | สถานะ | หมายเหตุ |
|---|---|---|---|
| **— MASTER · ข้อมูลหลัก —** | | | |
| Warehouse & Bin | คลังและตำแหน่ง | อยู่ Central Plan เดิม | W1 |
| **— INBOUND · รับเข้า —** | | | |
| Goods Receipt | ใบรับสินค้า | อยู่ Central Plan เดิม | W5 — หนักสุด 12 rules |
| Put Away | จัดเก็บเข้าตำแหน่ง | อยู่ Central Plan เดิม | W5 |
| Return to Vendor | คืนของผู้ขาย | อยู่ Central Plan เดิม | W8 |
| **— OUTBOUND · จัดส่ง —** | | | |
| Picking | หยิบสินค้า | อยู่ Central Plan เดิม | W6 |
| Packing | แพ็คสินค้า | อยู่ Central Plan เดิม | W6 |
| Delivery Note | ใบส่งของ | อยู่ Central Plan เดิม | W6 |
| **— STOCK CONTROL · จัดการสต็อก —** | | | |
| Stocktake | การนับสินค้า | อยู่ Central Plan เดิม | W2 |
| Stock Adjustment | ปรับยอดคงคลัง | เสร็จครบ pipeline | ENH pack |
| Stock Transfer | การโอนย้าย | อยู่ Central Plan เดิม | W2 |
| **— INVENTORY · สถานะรายการ —** | | | |
| Inventory | ยอดคงคลังตามที่เก็บ | เสร็จครบ pipeline | F-INV-STOCK-LOC-001 |

**รับเข้า (Inbound — เวลาพัฒนาแยก ให้ mock ของพวกนี้):**
- `Sales Order (Sales)` → **Picking** — สั่งหยิบของ
- `Sales Return (Sales)` → **Inventory** — รับของกลับเข้าคลัง
- `Purchase Order (Purchase)` → **Goods Receipt** — ของมาถึง
- `Company (Organization)` → **Warehouse & Bin** — คลังสังกัดสาขาในบริษัท
- `Document Center (Platform)` → **Goods Receipt** — แนบใบส่งของผู้ขาย
- `Item Master (Product)` → **Inventory** — สินค้าที่ติดตามสต็อก
- `DOA (Policy & Security)` → **Return to Vendor** — อนุมัติคืนผู้ขาย
- `DOA (Policy & Security)` → **Stocktake** — อนุมัติผลนับสต็อก
- `DOA (Policy & Security)` → **Stock Adjustment** — อนุมัติปรับยอด
- `DOA (Policy & Security)` → **Stock Transfer** — อนุมัติโอนคลัง

**ส่งออก (Outbound — สิ่งที่กล่องนี้ต้อง expose ให้คนอื่น):**
- **Delivery Note** → `AR Invoice (Accounting)` — วางบิลตามส่งจริง
- **Delivery Note** → `Sales Return (Sales)` — ลูกค้าคืนของ
- **Goods Receipt** → `GR/IR Clearing (Accounting)` — ตั้งพักรับของ
- **Goods Receipt** → `AP Invoice (Accounting)` — 3-way match
- **Return to Vendor** → `Credit / Debit Note (Accounting)` — ขอลดหนี้ผู้ขาย
- **Inventory** → `Sales Quotation (Sales)` — เช็คของก่อนเสนอราคา
- **Inventory** → `Sales Order (Sales)` — เช็คสต็อก + กันยอด
- **Inventory** → `Journal Entry (Accounting)` — มูลค่าสต็อก → GL

**เส้นในกล่อง:** Picking→Packing (หยิบครบ → แพ็ค) · Packing→Delivery Note (ออกใบส่งของ) · Goods Receipt→Put Away (เก็บเข้าตำแหน่ง) · Goods Receipt→Return to Vendor (ของไม่ผ่าน QC) · Put Away→Inventory (เพิ่มยอด) · Picking→Inventory (ตัดยอด) · Stock Adjustment→Inventory (ปรับยอด) · Stock Transfer→Inventory (ย้ายที่เก็บ) · Stocktake→Stock Adjustment (ผลนับต่าง → ปรับ) · Warehouse & Bin→Inventory (ยอดต่อที่เก็บ) · Return to Vendor→Inventory (คืนผู้ขาย → ตัดยอด) · Inventory→Stocktake (ยอดตามระบบไว้เทียบนับ)

#### Purchase · การจัดซื้อ (6)

| Feature | ไทย | สถานะ | หมายเหตุ |
|---|---|---|---|
| **— MASTER & SETUP · ข้อมูลหลัก —** | | | |
| Vendor Master | ผู้ขาย | อยู่ Central Plan เดิม | W1 |
| Vendor Price List | บัญชีราคาผู้ขาย | อยู่ Central Plan เดิม | W1 |
| Purchase Configuration | ตั้งค่าจัดซื้อ | มี HTML/บางส่วน | มีแล้วแต่ไม่มี artifact |
| **— DOCUMENTS · เอกสารซื้อ —** | | | |
| Purchase Requisition | ใบขอซื้อ | อยู่ Central Plan เดิม | W4 |
| Quotation Comparison | ใบเทียบราคา | อยู่ Central Plan เดิม | W4 |
| Purchase Order | ใบสั่งซื้อ | อยู่ Central Plan เดิม | W4 |

**รับเข้า (Inbound — เวลาพัฒนาแยก ให้ mock ของพวกนี้):**
- `Item Master (Product)` → **Purchase Order** — เฉพาะสินค้าที่ตั้งค่า "ซื้อได้"
- `Payment Terms (Accounting)` → **Purchase Order** — เครดิตเทอม
- `DOA (Policy & Security)` → **Purchase Requisition** — อนุมัติขอซื้อ
- `DOA (Policy & Security)` → **Purchase Order** — อนุมัติสั่งซื้อ
- `DOA (Policy & Security)` → **Quotation Comparison** — อนุมัติผลเทียบราคา
- `Cost Center (Organization)` → **Purchase Requisition** — ระบุศูนย์ต้นทุนตอนขอซื้อ

**ส่งออก (Outbound — สิ่งที่กล่องนี้ต้อง expose ให้คนอื่น):**
- **Purchase Order** → `Goods Receipt (Warehouse)` — ของมาถึง
- **Purchase Order** → `AP Invoice (Accounting)` — 3-way match

**เส้นในกล่อง:** Purchase Requisition→Quotation Comparison (เทียบราคาผู้ขาย) · Quotation Comparison→Purchase Order (เลือกผู้ขาย → สั่งซื้อ) · Vendor Master→Purchase Order (ผู้ขาย) · Vendor Price List→Quotation Comparison (ราคาอ้างอิง) · Purchase Configuration→Purchase Requisition (กติกาการซื้อ) · Vendor Master→Vendor Price List (ราคาต่อผู้ขาย)

### ▌Finance · People — ปลายทางเงินและคน


#### Finance · การเงิน (5)

| Feature | ไทย | สถานะ | หมายเหตุ |
|---|---|---|---|
| **— MASTER · ข้อมูลหลัก —** | | | |
| Bank Master | ธนาคาร | อยู่ Registry (ระบบเดิมมี) | — |
| Payment Method | วิธีชำระเงิน | อยู่ Registry (ระบบเดิมมี) | — |
| **— PAYMENTS · รับ-จ่ายเงิน —** | | | |
| Receipt Voucher | ใบสำคัญรับ | อยู่ Central Plan เดิม | W8 |
| Payment Voucher | ใบสำคัญจ่าย | อยู่ Central Plan เดิม | W9 |
| Bank Reconciliation | กระทบยอดธนาคาร | อยู่ Registry (ระบบเดิมมี) | — |

**รับเข้า (Inbound — เวลาพัฒนาแยก ให้ mock ของพวกนี้):**
- `AR Invoice (Accounting)` → **Receipt Voucher** — รับชำระ
- `AP Invoice (Accounting)` → **Payment Voucher** — ถึงกำหนดจ่าย
- `DOA (Policy & Security)` → **Payment Voucher** — อนุมัติจ่าย

**ส่งออก (Outbound — สิ่งที่กล่องนี้ต้อง expose ให้คนอื่น):**
- **Receipt Voucher** → `Journal Entry (Accounting)` — เงินเข้า
- **Payment Voucher** → `Journal Entry (Accounting)` — เงินออก
- **Payment Voucher** → `Withholding Tax (Accounting)` — หัก ณ ที่จ่าย

**เส้นในกล่อง:** Payment Method→Payment Voucher (วิธีจ่าย) · Payment Method→Receipt Voucher (วิธีรับ) · Bank Master→Bank Reconciliation (บัญชีธนาคาร) · Receipt Voucher→Bank Reconciliation (กระทบยอด) · Payment Voucher→Bank Reconciliation (กระทบยอด) · Bank Master→Payment Voucher (จ่ายจากบัญชีธนาคาร)

#### Accounting · บัญชี (15)

| Feature | ไทย | สถานะ | หมายเหตุ |
|---|---|---|---|
| **— MASTER · ข้อมูลหลัก —** | | | |
| Chart of Accounts | ผังบัญชี | อยู่ Central Plan เดิม | W1 |
| GL Posting Group | กลุ่มการลงบัญชี | มี HTML/บางส่วน | sales-module.html |
| Tax Code | รหัสภาษี | อยู่ Registry (ระบบเดิมมี) | — |
| Payment Terms | เงื่อนไขชำระเงิน | อยู่ Central Plan เดิม | W1 |
| **— AR / AP · ลูกหนี้-เจ้าหนี้ —** | | | |
| AR Invoice | ใบแจ้งหนี้/ใบกำกับภาษี | อยู่ Central Plan เดิม | W7 |
| AP Invoice | ตั้งหนี้เจ้าหนี้ (3-way) | อยู่ Central Plan เดิม | W7 — 15 rules |
| Credit / Debit Note | ใบลดหนี้/เพิ่มหนี้ | อยู่ Central Plan เดิม | W8 — 19 rules |
| GR/IR Clearing | บัญชีพักรับของ | อยู่ Central Plan เดิม | W8 |
| **— GL & CLOSING · ปิดบัญชี —** | | | |
| Journal Entry | สมุดรายวัน | อยู่ Registry (ระบบเดิมมี) | — |
| Opening Balance | ยอดยกมา | ยังไม่เคยนับ — ต้องเริ่มใหม่ | — |
| Period Close | ปิดงวด/ล็อกงวด | ยังไม่เคยนับ — ต้องเริ่มใหม่ | ★ ไม่มี = ปิดบัญชีไม่ได้ |
| Trial Balance | งบทดลอง | ยังไม่เคยนับ — ต้องเริ่มใหม่ | — |
| Financial Statements | งบการเงิน (PL/BS/CF) | ยังไม่เคยนับ — ต้องเริ่มใหม่ | ★ ปลายทางของ ERP ทั้งระบบ |
| **— TAX · ภาษี —** | | | |
| VAT Return (PP.30) | รายงานภาษีมูลค่าเพิ่ม (ภ.พ.30) | ยังไม่เคยนับ — ต้องเริ่มใหม่ | ★ บังคับตามกฎหมาย |
| Withholding Tax | ภาษีหัก ณ ที่จ่าย (ภ.ง.ด.3/53) | ยังไม่เคยนับ — ต้องเริ่มใหม่ | ★ บังคับตามกฎหมาย |

**รับเข้า (Inbound — เวลาพัฒนาแยก ให้ mock ของพวกนี้):**
- `Delivery Note (Warehouse)` → **AR Invoice** — วางบิลตามส่งจริง
- `Sales Return (Sales)` → **Credit / Debit Note** — ออกใบลดหนี้
- `Goods Receipt (Warehouse)` → **GR/IR Clearing** — ตั้งพักรับของ
- `Goods Receipt (Warehouse)` → **AP Invoice** — 3-way match
- `Purchase Order (Purchase)` → **AP Invoice** — 3-way match
- `Return to Vendor (Warehouse)` → **Credit / Debit Note** — ขอลดหนี้ผู้ขาย
- `Cost Center (Organization)` → **Journal Entry** — มิติต้นทุน
- `Receipt Voucher (Finance)` → **Journal Entry** — เงินเข้า
- `Payment Voucher (Finance)` → **Journal Entry** — เงินออก
- `Fiscal Periods (Organization)` → **Period Close** — งวดบัญชี
- `Payment Voucher (Finance)` → **Withholding Tax** — หัก ณ ที่จ่าย
- `Payroll (HR)` → **Journal Entry** — ค่าจ้าง → GL
- `Expense Claim (HR)` → **AP Invoice** — ตั้งหนี้คืนพนักงาน
- `DOA (Policy & Security)` → **Journal Entry** — อนุมัติรายการปรับ
- `Document Center (Platform)` → **AP Invoice** — แนบใบกำกับภาษี
- `Inventory (Warehouse)` → **Journal Entry** — มูลค่าสต็อก → GL
- `DOA (Policy & Security)` → **AP Invoice** — อนุมัติตั้งหนี้ (3-way)
- `DOA (Policy & Security)` → **Credit / Debit Note** — อนุมัติลด/เพิ่มหนี้
- `DOA (Policy & Security)` → **Opening Balance** — อนุมัติยอดยกมา
- `DOA (Policy & Security)` → **Period Close** — อนุมัติปิดงวด
- `Fiscal Periods (Organization)` → **Journal Entry** — คุมงวดที่ลงบัญชีได้

**ส่งออก (Outbound — สิ่งที่กล่องนี้ต้อง expose ให้คนอื่น):**
- **AR Invoice** → `Receipt Voucher (Finance)` — รับชำระ
- **AP Invoice** → `Payment Voucher (Finance)` — ถึงกำหนดจ่าย
- **Payment Terms** → `Purchase Order (Purchase)` — เครดิตเทอม
- **Journal Entry** → `Audit Trail (Platform)` — ทุกรายการเก็บ log

**เส้นในกล่อง:** GR/IR Clearing→AP Invoice (ล้างบัญชีพัก) · Payment Terms→AR Invoice (กำหนดชำระ) · Tax Code→AR Invoice (ภาษีขาย) · Tax Code→AP Invoice (ภาษีซื้อ) · Chart of Accounts→GL Posting Group (ผูกผังบัญชี) · GL Posting Group→Journal Entry (ลงบัญชีอัตโนมัติ) · Opening Balance→Journal Entry (ยอดยกมา) · AR Invoice→Journal Entry (ลงบัญชีลูกหนี้) · AP Invoice→Journal Entry (ลงบัญชีเจ้าหนี้) · Credit / Debit Note→Journal Entry (กลับรายการ) · Journal Entry→Trial Balance (รวมยอด) · Trial Balance→Period Close (ตรวจก่อนปิด) · Period Close→Financial Statements (ออกงบ) · AR Invoice→VAT Return (PP.30) (ภาษีขาย) · AP Invoice→VAT Return (PP.30) (ภาษีซื้อ) · Payment Terms→AP Invoice (กำหนดจ่ายเจ้าหนี้)

#### HR · บุคคล (5)

| Feature | ไทย | สถานะ | หมายเหตุ |
|---|---|---|---|
| **— MASTER · ข้อมูลหลัก —** | | | |
| Employee Master | พนักงาน | อยู่ Registry (ระบบเดิมมี) | feed ทุก module |
| **— TIME · เวลาทำงาน —** | | | |
| Time & Attendance | ลงเวลา | อยู่ Registry (ระบบเดิมมี) | — |
| Leave Management | วันลา | อยู่ Registry (ระบบเดิมมี) | — |
| **— PAYROLL · เงินเดือน —** | | | |
| Payroll | เงินเดือน | อยู่ Registry (ระบบเดิมมี) | — |
| Expense Claim | เบิกค่าใช้จ่าย | ยังไม่เคยนับ — ต้องเริ่มใหม่ | ★ ควรวิ่งเข้า AP |

**รับเข้า (Inbound — เวลาพัฒนาแยก ให้ mock ของพวกนี้):**
- `Company (Organization)` → **Employee Master** — สังกัด สายงาน ตำแหน่ง
- `Working Calendar (Organization)` → **Time & Attendance** — วันทำงาน/วันหยุด
- `DOA (Policy & Security)` → **Leave Management** — อนุมัติลา
- `Cost Center (Organization)` → **Expense Claim** — เบิกลงศูนย์ต้นทุน
- `DOA (Policy & Security)` → **Expense Claim** — อนุมัติเบิก
- `DOA (Policy & Security)` → **Payroll** — อนุมัติงวดเงินเดือน
- `Document Center (Platform)` → **Expense Claim** — แนบใบเสร็จเบิก

**ส่งออก (Outbound — สิ่งที่กล่องนี้ต้อง expose ให้คนอื่น):**
- **Payroll** → `Journal Entry (Accounting)` — ค่าจ้าง → GL
- **Expense Claim** → `AP Invoice (Accounting)` — ตั้งหนี้คืนพนักงาน
- **Employee Master** → `User Management (System)` — พนักงาน → ผู้ใช้

**เส้นในกล่อง:** Employee Master→Time & Attendance (คนที่ลงเวลา) · Employee Master→Leave Management (สิทธิ์ลา) · Employee Master→Payroll (ฐานเงินเดือน) · Time & Attendance→Payroll (ชั่วโมง/OT) · Leave Management→Payroll (หักลาไม่รับค่าจ้าง) · Employee Master→Expense Claim (ผู้เบิก)

---

## §4 สายงาน 8 สาย — หลักคิด + ลำดับเอกสารจริง


### ขาซื้อ (p2p) — 11 เส้น

หลักคิด: **ขอ → เทียบ → สั่ง → รับ → ตั้งหนี้ → จ่าย** · การเงินคุมด้วย 3-way match (PO×GR×Invoice ใน tolerance ถึงจ่ายได้) + GR/IR เป็นบัญชีพักตอน "ของถึงแต่บิลยังไม่มา" · ทุกใบผ่าน DOA ตามวงเงิน

- Purchase Requisition → Quotation Comparison — เทียบราคาผู้ขาย `[doc]`
- Quotation Comparison → Purchase Order — เลือกผู้ขาย → สั่งซื้อ `[doc]`
- Purchase Order → Goods Receipt — ของมาถึง `[doc]`
- Goods Receipt → Put Away — เก็บเข้าตำแหน่ง `[doc]`
- Goods Receipt → GR/IR Clearing — ตั้งพักรับของ `[post]`
- Goods Receipt → AP Invoice — 3-way match `[doc]`
- Purchase Order → AP Invoice — 3-way match `[doc]`
- AP Invoice → Payment Voucher — ถึงกำหนดจ่าย `[doc]`
- GR/IR Clearing → AP Invoice — ล้างบัญชีพัก `[post]`
- Goods Receipt → Return to Vendor — ของไม่ผ่าน QC `[doc]`
- Return to Vendor → Credit / Debit Note — ขอลดหนี้ผู้ขาย `[doc]`

### ขาขาย (o2c) — 13 เส้น

หลักคิด: **หา → เสนอ → ยืนยัน → ส่ง → วางบิล → เก็บเงิน** · เช็คสต็อก (ATP) ก่อนรับปากลูกค้าทั้งตอนเสนอและตอนยืนยัน · วางบิลตามส่งจริง ไม่ใช่ตามออเดอร์ · Prospect ปิดการขายได้ = convert เป็น Customer

- Prospect → Sales Quotation — ลูกค้ามุ่งหวัง → เสนอราคา `[doc]`
- Sales Quotation → Sales Order — ลูกค้าตอบรับ `[doc]`
- Sales Order → Picking — สั่งหยิบของ `[doc]`
- Picking → Packing — หยิบครบ → แพ็ค `[doc]`
- Packing → Delivery Note — ออกใบส่งของ `[doc]`
- Delivery Note → AR Invoice — วางบิลตามส่งจริง `[doc]`
- AR Invoice → Receipt Voucher — รับชำระ `[doc]`
- Delivery Note → Sales Return — ลูกค้าคืนของ `[doc]`
- Sales Return → Credit / Debit Note — ออกใบลดหนี้ `[doc]`
- Sales Return → Inventory — รับของกลับเข้าคลัง `[doc]`
- Inventory → Sales Quotation — เช็คของก่อนเสนอราคา `[config]`
- Inventory → Sales Order — เช็คสต็อก + กันยอด `[config]`
- Prospect → Customer Master — ปิดการขายได้ → convert เป็นลูกค้า `[doc]`

### สต็อก (stock) — 8 เส้น

หลักคิด: **ยอดคงเหลือคือ ledger — เปลี่ยนได้ผ่าน movement เท่านั้น** · รับเข้า/จ่ายออก/โอน/ปรับ ทุกใบวิ่งเข้า Inventory · นับจริง (Stocktake) เทียบระบบ → ส่วนต่างออกใบปรับผ่าน DOA · มูลค่าลง GL

- Put Away → Inventory — เพิ่มยอด `[doc]`
- Picking → Inventory — ตัดยอด `[doc]`
- Stock Adjustment → Inventory — ปรับยอด `[doc]`
- Stock Transfer → Inventory — ย้ายที่เก็บ `[doc]`
- Stocktake → Stock Adjustment — ผลนับต่าง → ปรับ `[doc]`
- Return to Vendor → Inventory — คืนผู้ขาย → ตัดยอด `[doc]`
- Inventory → Stocktake — ยอดตามระบบไว้เทียบนับ `[config]`
- Inventory → Journal Entry — มูลค่าสต็อก → GL `[post]`

### ปิดบัญชี (gl) — 16 เส้น

หลักคิด: **ทุกบรรทัดบัญชีอ้างเอกสารต้นทางได้ (document principle)** · เอกสาร operational ยิง JE อัตโนมัติผ่าน Posting Group · ลงได้เฉพาะงวดเปิด (posting period control) · ปิดงวด: ตรวจงบทดลอง → อนุมัติปิด → งวดล็อก → ออกงบ

- Opening Balance → Journal Entry — ยอดยกมา `[post]`
- AR Invoice → Journal Entry — ลงบัญชีลูกหนี้ `[post]`
- AP Invoice → Journal Entry — ลงบัญชีเจ้าหนี้ `[post]`
- Credit / Debit Note → Journal Entry — กลับรายการ `[post]`
- Receipt Voucher → Journal Entry — เงินเข้า `[post]`
- Payment Voucher → Journal Entry — เงินออก `[post]`
- Journal Entry → Trial Balance — รวมยอด `[post]`
- Fiscal Periods → Period Close — งวดบัญชี `[config]`
- Trial Balance → Period Close — ตรวจก่อนปิด `[post]`
- Period Close → Financial Statements — ออกงบ `[post]`
- AR Invoice → VAT Return (PP.30) — ภาษีขาย `[post]`
- AP Invoice → VAT Return (PP.30) — ภาษีซื้อ `[post]`
- Payment Voucher → Withholding Tax — หัก ณ ที่จ่าย `[post]`
- Receipt Voucher → Bank Reconciliation — กระทบยอด `[post]`
- Payment Voucher → Bank Reconciliation — กระทบยอด `[post]`
- Fiscal Periods → Journal Entry — คุมงวดที่ลงบัญชีได้ `[config]`

### คน–เงินเดือน (hr) — 11 เส้น

หลักคิด: **คน → เวลา → เงิน → บัญชี** · Employee เป็น master เดียวของคน (Company ให้โครงสังกัด) · เวลา/ลา feed เงินเดือน · GL รับ summary ต่อ cost center ไม่ลงรายคน

- Company → Employee Master — สังกัด สายงาน ตำแหน่ง `[config]`
- Employee Master → Time & Attendance — คนที่ลงเวลา `[config]`
- Employee Master → Leave Management — สิทธิ์ลา `[config]`
- Employee Master → Payroll — ฐานเงินเดือน `[config]`
- Working Calendar → Time & Attendance — วันทำงาน/วันหยุด `[config]`
- Time & Attendance → Payroll — ชั่วโมง/OT `[doc]`
- Leave Management → Payroll — หักลาไม่รับค่าจ้าง `[doc]`
- Payroll → Journal Entry — ค่าจ้าง → GL `[post]`
- Employee Master → Expense Claim — ผู้เบิก `[config]`
- Expense Claim → AP Invoice — ตั้งหนี้คืนพนักงาน `[doc]`
- Employee Master → User Management — พนักงาน → ผู้ใช้ `[config]`

### อนุมัติ–สิทธิ์ (gov) — 25 เส้น

หลักคิด: **นโยบายกำหนดกรอบ → DOA แปลงเป็นสายเซ็นต่อ (ชนิดเอกสาร, วงเงิน, หน่วยงาน) → เอกสารเดิน state machine** draft→pending→approved · แบบเดียวกับ release strategy ของ SAP · สิทธิ์: คน←บทบาท←นโยบาย สรุปเป็น Permission Matrix → คุมเมนู

- Policy Document → DOA — นโยบาย → สายอนุมัติ `[config]`
- DOA → Purchase Requisition — อนุมัติขอซื้อ `[gov]`
- DOA → Purchase Order — อนุมัติสั่งซื้อ `[gov]`
- DOA → Sales Order — อนุมัติส่วนลด `[gov]`
- DOA → Payment Voucher — อนุมัติจ่าย `[gov]`
- DOA → Journal Entry — อนุมัติรายการปรับ `[gov]`
- DOA → Leave Management — อนุมัติลา `[gov]`
- User Management → Roles & Permissions — ผู้ใช้ ← บทบาท `[config]`
- Roles & Permissions → Permission Matrix — สรุปเป็นตารางสิทธิ์ `[config]`
- DOA → Sales Quotation — อนุมัติราคา/ส่วนลดเสนอ `[gov]`
- DOA → Quotation Comparison — อนุมัติผลเทียบราคา `[gov]`
- DOA → AP Invoice — อนุมัติตั้งหนี้ (3-way) `[gov]`
- DOA → Credit / Debit Note — อนุมัติลด/เพิ่มหนี้ `[gov]`
- DOA → Sales Return — อนุมัติรับคืน `[gov]`
- DOA → Return to Vendor — อนุมัติคืนผู้ขาย `[gov]`
- DOA → Stocktake — อนุมัติผลนับสต็อก `[gov]`
- DOA → Stock Adjustment — อนุมัติปรับยอด `[gov]`
- DOA → Stock Transfer — อนุมัติโอนคลัง `[gov]`
- DOA → Opening Balance — อนุมัติยอดยกมา `[gov]`
- DOA → Period Close — อนุมัติปิดงวด `[gov]`
- DOA → Expense Claim — อนุมัติเบิก `[gov]`
- DOA → Payroll — อนุมัติงวดเงินเดือน `[gov]`
- Permission Matrix → Menu Registry — เมนูตามสิทธิ์ `[config]`
- Company → DOA — โครงตำแหน่ง → ตั้งสายอนุมัติ `[config]`
- Policy Document → Roles & Permissions — นโยบาย → กรอบสิทธิ์ `[config]`

### ข้อมูลหลัก (master) — 37 เส้น

หลักคิด: **master = golden record ใช้เป็น picker เท่านั้น** · เอกสาร snapshot ค่า ณ วันสร้าง ไม่ lookup สด · soft-reference: ไม่มี FK cascade — ลบ/แก้ master ไม่ทำเอกสารเก่าพัง

- Unit of Measure → Item Master — หน่วยนับ `[config]`
- Bill of Materials → Item Master — สูตร/ชุด `[config]`
- Item Master → Product Catalog — จัดเข้าแค็ตตาล็อก `[config]`
- Product Catalog → Sales Price List — ตั้งราคาตามแค็ตตาล็อก `[config]`
- Customer Group → Sales Price List — ราคาต่อกลุ่มลูกค้า `[config]`
- Sales Price List → Sales Quotation — ดึงราคา `[config]`
- Customer Master → Sales Order — ลูกค้า `[config]`
- Vendor Master → Purchase Order — ผู้ขาย `[config]`
- Vendor Price List → Quotation Comparison — ราคาอ้างอิง `[config]`
- Item Master → Purchase Order — เฉพาะสินค้าที่ตั้งค่า "ซื้อได้" `[config]`
- Item Master → Sales Order — เฉพาะสินค้าที่ตั้งค่า "ขายได้" `[config]`
- Promotion → Sales Order — โปรฯ/ส่วนลดผูกตอนเปิดออเดอร์ `[config]`
- Sales Channel → Sales Order — ระบุช่องทางที่ขาย `[config]`
- Company → Warehouse & Bin — คลังสังกัดสาขาในบริษัท `[config]`
- Warehouse & Bin → Inventory — ยอดต่อที่เก็บ `[config]`
- Payment Terms → AR Invoice — กำหนดชำระ `[config]`
- Payment Terms → Purchase Order — เครดิตเทอม `[config]`
- Tax Code → AR Invoice — ภาษีขาย `[config]`
- Tax Code → AP Invoice — ภาษีซื้อ `[config]`
- Chart of Accounts → GL Posting Group — ผูกผังบัญชี `[config]`
- GL Posting Group → Journal Entry — ลงบัญชีอัตโนมัติ `[config]`
- Payment Method → Payment Voucher — วิธีจ่าย `[config]`
- Payment Method → Receipt Voucher — วิธีรับ `[config]`
- Bank Master → Bank Reconciliation — บัญชีธนาคาร `[config]`
- Cost Center → Journal Entry — มิติต้นทุน `[config]`
- Item Master → Inventory — สินค้าที่ติดตามสต็อก `[config]`
- Customer Master → Sales Quotation — ลูกค้าในใบเสนอราคา `[config]`
- Promotion → Sales Quotation — ส่วนลดตอนเสนอราคา `[config]`
- Cost Center → Expense Claim — เบิกลงศูนย์ต้นทุน `[config]`
- Sales Configuration → Sales Order — กติกาการขาย `[config]`
- Customer Group → Customer Master — จัดกลุ่มลูกค้า `[config]`
- Item Master → Sales Quotation — สินค้าที่ตั้งค่า "ขายได้" `[config]`
- Purchase Configuration → Purchase Requisition — กติกาการซื้อ `[config]`
- Vendor Master → Vendor Price List — ราคาต่อผู้ขาย `[config]`
- Cost Center → Purchase Requisition — ระบุศูนย์ต้นทุนตอนขอซื้อ `[config]`
- Payment Terms → AP Invoice — กำหนดจ่ายเจ้าหนี้ `[config]`
- Bank Master → Payment Voucher — จ่ายจากบัญชีธนาคาร `[config]`

### แพลตฟอร์ม (plat) — 10 เส้น

หลักคิด: **cross-cutting แบบ async** — แจ้งเตือน/audit/ไฟล์แนบ เกาะทุกเอกสารโดยไม่บล็อกงานหลัก · audit append-only

- DOA → Notification — ถึงคิวอนุมัติ → แจ้ง `[event]`
- Journal Entry → Audit Trail — ทุกรายการเก็บ log `[event]`
- Document Center → Goods Receipt — แนบใบส่งของผู้ขาย `[config]`
- Document Center → AP Invoice — แนบใบกำกับภาษี `[config]`
- Ticket → Notification — อัพเดต ticket → แจ้ง `[event]`
- Monitor Logs → Notification — ระบบผิดพลาด → แจ้งทีม `[event]`
- User Management → Audit Trail — log เข้าใช้/เปลี่ยนสิทธิ์ `[event]`
- Document Center → Expense Claim — แนบใบเสร็จเบิก `[config]`
- User Management → Ticket — ผู้แจ้ง/ผู้รับผิดชอบ `[config]`
- Document Center → Sales Order — แนบ PO ลูกค้า `[config]`

---

## §5 เทียบ ERP standard สากล (research แล้ว)

| Concept ในแผนเรา | SAP | Odoo | D365 | หมายเหตุ |
|---|---|---|---|---|
| PR → CP → PO | Purchase Requisition → RFQ/Comparison → PO (ME51N/ME21N + release strategy) | PR → RFQ → PO | Purchase requisition → PO | เราแยก CP เป็นเอกสารเทียบ + DOA |
| 3-way match + GR/IR | MIGO (GR: Dr Stock/Cr GR-IR) + MIRO (LIV: เทียบ PO×GR×Inv, tolerance OMR6, เกิน = block MRBR) | Bill control 3-way | Product receipt ↔ invoice matching | ตรงกับเส้น PO→AP + GR→AP + GR→GR/IR→AP ของเรา |
| ATP check ตอน SO | SD availability check (stock + planned receipts − commitments → schedule line confirm) | Check availability | Order promising (sales lead time / ATP / CTP) | เส้น Inventory→SQ/SO · เฟสแรกใช้ on_hand−allocated · planned receipts = เฟสถัดไป |
| Bill from delivery | Delivery-related billing (VF01 จาก DN) | Invoice from delivered qty | Packing slip → invoice | เส้น DN→AR Invoice |
| Lead conversion | — (CRM) | Lead → Opportunity → Customer convert | Lead → qualify → Account | เรา: Prospect → convert → Customer (ข้าม opportunity ตามที่ทีมตัด) |
| Posting period control | Open/close posting periods (OB52) | Lock dates | Ledger calendar period open/close | เส้น Fiscal Periods→JE + Period Close |
| Release strategy / DOA | PO release strategy ตาม doc type + amount | Approval rules (amount-based) | Workflow approval | DOA ครอบเอกสารเซ็น 19 ใบ + Company→DOA (โครงตำแหน่ง) |
| Inventory ledger | Material document ทุก movement | Stock moves | Inventory transactions | ยอดแก้ตรงไม่ได้ — ผ่าน movement เท่านั้น |

อ้างอิงหลัก: SAP GR/IR & 3-way (doxis.com/blog/goods-receipt-checks · erpvits.com P2P cycle) · D365 order promising (learn.microsoft.com delivery-dates-available-promise) · Oracle ATP formula (docs.oracle.com MRP ATP)

---

## §6 Decision Log (4 รอบ review)

- **รอบ 1-2 (features):** กลั่น universe 472 → 71 ตามโฟลเดอร์ระบบจริง + ทีม cut · รวมโครงองค์กรเข้า Company · rename: Lead→Prospect, Stock on Hand→Inventory, Stock Count→Stocktake · ตัดไว้ก่อน (ไม่ถาวร): Number Series, Opportunity, Credit Limit, Warehouse Setup, Stock Reservation, Inventory Costing, Vendor Quotation, AR/AP Aging, Social Security, Approval Workflow Engine (ใช้ DOA ตรง)
- **รอบ 3 (เส้น):** DOA ครอบเอกสารเซ็น 19 ใบ · Inventory hub check-stock
- **รอบ 4 (analyze ทีละกล่อง):** Prospect→Customer convert · คืน Sales/Purchase Configuration · Company→DOA · Fiscal→JE · Payment Term→AP · Bank→PV · Vendor→Vendor Price List · Segment→Customer · Item→SQ · Cost Center→PR · Policy→Roles · User→Ticket · DC→SO
- **รอบ 5 (Lite/Full · 2026-08-03):** เพิ่มกล่อง Tenant & Packaging [Cubic] 4 features (ยังไม่พัฒนาทั้งหมด — คิว W1) + Global Contract #10 Entitlement→Linkage 3 ชั้น · มติ: Lite/Full = feature เดียวโค้ดเดียวห้าม fork, ปลายทางไม่เปิด = force manual, ทุกเส้นข้าม module ต้องมี dual-mode ตั้งแต่ PREBRIEF (D7) · OQ-LITE-01 Item Lite รอ Strike · เส้น Linkage→ทุก module วาดตัวแทนผ่าน Sales Order เส้นเดียว
- **รอบ 6 (v1.3 · 2026-08-04):** Sales +5 field ops จาก sales-module.html (Territory · Trade Agreement · Target · Visit Operation ตรวจเยี่ยม/เช็คสต๊อกร้านย่อย · Outlet Replenishment เติมของ→SO) — Sales เป็น module แรกที่จะ deliver ลูกค้า · Tenant & Packaging +3 self-service (Signup Portal → Subscription & Billing → Instant Provisioning เริ่มใช้ทันทีแบบ Odoo · แยก 2 เส้นทางขึ้นระบบ self-service/guided) · นิยามกลุ่ม module: Sellable (Lite/Full ✅) = Sales/Purchase/Warehouse/Product/HR/Finance/Accounting · Shared Foundation ไม่มี tier · Item = กรณีพิเศษ (OQ-LITE-01)
- **รอบ 7 (v1.4 · 2026-08-04):** มติสถาปัตยกรรมขาย — **ระนาบ Provider แยกไป Cubic แบบ physical** (พิจารณา Provider Admin area ใน Core แล้ว: บริหารง่ายกว่าแต่ blast radius ใหญ่ — ทีมยอมจ่ายต้นทุน 2 ระบบเพื่อ isolation) · เพิ่ม §1.5 Commercial Architecture (3 ระนาบ · sellable flag · C-TEN-01..03 cache+fallback) · +2 features ฝั่ง tenant ใน System: My Subscription, My Linkage Settings · กติกาเหล็ก negative TC ทุก feature ระนาบ Provider
- **จงใจไม่วาด (กันรก แต่ระบบจริงต้องทำ):** Audit Trail ครอบทุกเอกสาร (วาดตัวแทน JE + User log) · Warehouse & Bin เข้าเอกสารคลังทุกใบ (ผ่าน Inventory แทน) · Notification ครอบทุกเหตุการณ์ · Module Linkage Config ครอบทุกเส้นข้าม module (วาดตัวแทน → Sales Order)

## §7 สถานะ + งานถัดไป

- นับสถานะ (v1.4): 85 features — gap 25 (+My Subscription, +My Linkage Settings) — สถานะสดดูที่ WAVE_PLAN/tracking
- เปิดแชทพัฒนาต่อกล่อง: แปะไฟล์นี้ + สั่งทำตาม §2-§3 ของกล่องนั้น
- แก้แผน: แก้ที่ generator (แชท Core ERP map) → regen HTML + MD คู่กัน → sync knowledge
