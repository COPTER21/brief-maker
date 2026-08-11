# AI Test Cases — F-PAY เงื่อนไขชำระเงิน (Payment Terms)

ไฟล์นี้เขียนให้ **AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบนหน้าจอจริง + รายงานผลกลับ machine-readable.
ทุก action ขึ้นต้นด้วย **verb tag** (OPEN/CLICK/TYPE/SELECT/TOGGLE/PRESS/WAIT/VERIFY) + target ที่เห็นบนจอ.
ทุก Expected เช็คได้ด้วยตา (ข้อความปรากฏ/หาย · pill เปลี่ยนสี · จำนวนแถว · ปุ่ม disabled · toast).

> **Anchor source priority:** HTML SoT `01_HTML/f-payterm.html` (verbatim) > `01_UI` > microcopy กลาง html-generator-v8.
> **หน้าจอ = single-view SPA + overlay** (ไม่มี hash router จริง). "route (production)" คือเส้นทางที่เสนอ 1:1 กับ overlay —
> agent ที่รันบน prototype: เปิดไฟล์ HTML = เข้าหน้า List (P-01) เสมอ (reload = กลับ List, mock state in-memory).
> **Toast:** แสดง **บนสุดกึ่งกลางจอ (top-center)** · error/warning ค้าง **5 วินาที** · อื่น ๆ 2.8 วินาที.

---

## Meta

| Field | Value |
|---|---|
| Feature ID | F-PAY (F-PAYMENT-TERM-001) |
| Feature Name | Payment Term — เงื่อนไขการชำระเงิน |
| Module | การเงิน (Accounting) — sidebar item "เงื่อนไขชำระเงิน" (is-active) |
| FRD Version | 1.0 (2026-08-10, FULL pack) |
| App entry (observed) | โหลด `f-payterm.html` → หน้า List (P-01) · breadcrumb "การเงิน › เงื่อนไขชำระเงิน" |
| Routes (production 1:1) | List `#/finance/payment-term` · Create `…/new` · Edit `…/:id/edit` · View `…/:id` · Bulk-delete modal |
| แหล่งอ้างอิง | FRD `06_TESTS` (AT-01..19, XT-01..06) · `05_RULES` (BR-01..13, EC-01..11) · `01_UI` (P-01..05) · `07_LOCKED` (LD/Scope Lock) · HTML SoT · UI Brief |
| Seed data | 12 terms (t1..t12) — ครอบ 7 ประเภท · active 10 / inactive 1 / draft 1 · used 0..186 |
| จำนวนเคส | 89 เคส (ดู Coverage) |
| Note (regen) | รอบแรก — TC-id เสถียรสำหรับ regen ถัดไป (R16) |

**Seed อ้างอิง (จาก HTML `state.terms`) — ใช้เป็น precondition:**

| id | code | ชื่อ (TH) | ประเภท | สถานะ | used | default |
|---|---|---|---|---|---|---|
| t1 | PREPAY | ชำระเต็มก่อนส่ง | Full Prepay | ใช้งาน | 14 | — |
| t2 | POSTPAY | ชำระเต็มหลังรับของ | Full Postpay | ใช้งาน | 6 | — |
| t3 | **NET30** | เครดิต 30 วัน | Credit | ใช้งาน | **186** | **⭐ (credit default)** |
| t4 | NET60 | เครดิต 60 วัน | Credit | ไม่ใช้งาน | 0 | — |
| t5 | 2-10N30 | เครดิต 30 วัน ลดเร็ว 2% | Credit | ใช้งาน | 31 | — |
| t6 | EOM30 | สิ้นเดือน + 30 วัน | Credit | ใช้งาน | 8 | — |
| t7 | DEP50 | มัดจำ 50% ที่เหลือ 30 วัน | Deposit | ใช้งาน | 42 | — |
| t8 | DEP30 | มัดจำ 30% ที่เหลือ 15 วัน | Deposit | ใช้งาน | 3 | — |
| t9 | INST3 | แบ่ง 3 งวด (40/30/30) | Installment | ใช้งาน | 11 | — |
| t10 | PARTIAL | ทยอยส่ง จ่ายตามรับจริง | Partial Delivery | ใช้งาน | 5 | — |
| t11 | DIRECT-UTIL | จ่ายตรง — ค่าสาธารณูปโภค | Direct Payment | ใช้งาน | 9 | — |
| t12 | **NET45** | เครดิต 45 วัน (เตรียมใช้) | Credit | **ร่าง** | **0** | — |

> Stat cards เริ่มต้น: **ทั้งหมด 12 · ใช้งาน 10 · ไม่ใช้งาน 1 · ร่าง 1**.

---

## Coverage

| Group | รหัส | เคส | ความสำคัญ |
|---|---|---|---|
| A. List / Search / Filter (P-01) | TC-L01..L12 | 12 | สูง |
| B. Create happy — 7 ประเภท + trigger/due_basis | TC-C01..C11 | 11 | สูง |
| C. Create validation / negative | TC-V01..V15 | 15 | สูง |
| D. Edit / View | TC-E01..E06 | 6 | สูง |
| E. Status change (single + bulk) | TC-S01..S05 | 5 | กลาง |
| F. Bulk delete + guard used>0 | TC-D01..D05 | 5 | สูง |
| G. Default toggle | TC-DF01..DF04 | 4 | สูง |
| H. Edge / interaction | TC-EC01..EC09 (+EC02b) | 10 | กลาง |
| I. Scope-Lock verify (must-NOT-exist) | TC-SL01..SL08 | 8 | สูง |
| J. [AI-DEFAULT] propagation | TC-AD01..AD03 | 3 | กลาง |
| K. Cross-Module (XT — simulate) | TC-XT01..XT06 | 6 | กลาง |
| L. Permission | TC-PM01..PM02 | 2 | กลาง |
| M. Concurrency / Idempotency (simulate) | TC-CC01..CC02 | 2 | ต่ำ |
| **รวม** | | **89** | |

---

## Coverage Ledger

### FR / Acceptance (06_TESTS §6.1)
| item | cases |
|---|---|
| AT-01 create credit happy | TC-C01 |
| AT-02 code required + duplicate | TC-V01, TC-V02, TC-V03 |
| AT-03 credit net_days>0 | TC-V05 |
| AT-04 installment ≥2 & sum=100 | TC-V06, TC-V07, TC-EC03, TC-EC04 |
| AT-05 deposit % 0<x≤100 | TC-V08, TC-V09 |
| AT-05b deposit manual → value ว่าง | TC-C05b (in TC-C05) , TC-EC08 |
| AT-06 use_in ≥1 · no PR | TC-V10, TC-SL02 |
| AT-07 default 1/type + active | TC-DF01, TC-DF02, TC-V11 |
| AT-08 discount days boundary | TC-V12, TC-V13 |
| AT-09 edit used>0 snapshot | TC-E01, TC-AD01, TC-EC07 |
| AT-10 status change single | TC-S01, TC-S02 |
| AT-11 bulk status | TC-S03, TC-S04 |
| AT-12 bulk delete guard | TC-D01..D05 |
| AT-13 search/filter list | TC-L01..L12 |
| AT-14 no CSV | TC-SL01 |
| AT-15 active picker + credit lock | TC-SL03, TC-XT02 |
| AT-16 trigger default/type | TC-C02, TC-C03, TC-C06, TC-C11 |
| AT-17 direct disables docs | TC-C07, TC-SL02 |
| AT-18 due_basis 3 values | TC-C10 |
| AT-19 Viewer/Consumer 403 | TC-PM01, TC-PM02 |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-01 code unique + UPPERCASE | TC-V01, TC-V02, TC-V03, TC-C01 |
| BR-02 credit net_days>0 / postpay≥0 | TC-V05, TC-C02 |
| BR-03 deposit % 0<x≤100 | TC-V08, TC-V09 |
| BR-04 installment ≥2 + sum 100 | TC-V06, TC-V07 |
| BR-05 discount_days>0 & <net_days · 1 tier | TC-V12, TC-V13, TC-AD02 |
| BR-06 use_in ≥1 · no PR | TC-V10, TC-SL02 |
| BR-07 default 1/type + active | TC-DF01, TC-DF02, TC-DF03, TC-V11 |
| BR-08 used>0 ลบไม่ได้ · แก้ได้ | TC-D01, TC-D03, TC-E01, TC-AD01 |
| BR-09 no CSV | TC-SL01 |
| BR-10 active-only picker · credit trigger locked | TC-SL03, TC-XT02 |
| BR-11 trigger default/type · after_deposit deposit-only | TC-C06, TC-C11, TC-SL03 |
| BR-12 direct: no trigger · disable po/quotation/so | TC-C07, TC-SL02 |
| BR-13 due_basis 3 values (ยกเว้น direct) | TC-C10, TC-C07 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 concurrent default (409) | TC-CC01 (ต้อง simulate) |
| EC-02 double-submit create | TC-CC02 |
| EC-03 change type when used>0 | TC-EC07 |
| EC-04 นิยาม `used` (OQ-PAY-07) | — ข้าม (OPEN/blocking OQ — spec ยังไม่ปิด, ไม่มีผลสังเกตบน UI) |
| EC-05 term→inactive ระหว่างสร้างเอกสาร | TC-XT03 (ต้อง simulate) |
| EC-06 ลบ default (used=0) → ไม่มี default | TC-EC05 |
| EC-07 deposit VAT (OQ-PAY-04) | TC-XT04 (ต้อง simulate — downstream) |
| EC-08 EOM cross boundary | — ข้าม (downstream AP/AR calc, OQ) |
| EC-09 deposit manual → value ว่าง | TC-C05, TC-EC08 |
| EC-10 direct disable po/quotation/so | TC-C07, TC-SL02 |
| EC-11 installment days=0 หลายงวด (accepted) | TC-EC06 |

### Error Codes (05_RULES §5.6)
| error | cases |
|---|---|
| ERR_CODE_REQUIRED | TC-V01 |
| ERR_DUPLICATE_CODE | TC-V02, TC-V03 |
| ERR_NAME_REQUIRED | TC-V04 |
| ERR_CREDIT_DAYS_INVALID | TC-V05 |
| ERR_DEPOSIT_PCT_INVALID | TC-V08, TC-V09 |
| ERR_INSTALLMENT_COUNT | TC-V06, TC-EC04 |
| ERR_INSTALLMENT_SUM | TC-V07 |
| ERR_DISCOUNT_DAYS_INVALID | TC-V12, TC-V13 |
| ERR_USE_IN_EMPTY | TC-V10 |
| ERR_DEFAULT_NOT_ACTIVE | TC-V11 |
| ERR_INSUFFICIENT_ROLE (403) | TC-PM01, TC-PM02 (ต้อง simulate) |
| ERR_STALE_DATA (409) | TC-CC01 (ต้อง simulate) |
| ERR_DUPLICATE_IDEMPOTENCY_KEY | TC-CC02 (ต้อง simulate) |
| ERR_NOT_FOUND / ERR_NOT_AUTHENTICATED / ERR_VALIDATION_FAILED | — ข้าม (API-only, ไม่มี trigger บน UI prototype) |

### Permission Matrix (05_RULES §5.3)
| cell | cases |
|---|---|
| Finance Admin = ทุก action | ครอบทั้งไฟล์ (default user = Finance Lead/Admin) |
| Finance Viewer = view เท่านั้น (create/edit/bulk = deny) | TC-PM01 (ต้อง simulate role) |
| Consumer = picker active-only (mutation deny) | TC-PM02, TC-SL03 (ต้อง simulate) |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 PO snapshot code+config | PO/SO/PV | TC-XT01 (ต้อง simulate) |
| XT-02 master→inactive ไม่โผล่ picker | picker | TC-XT02 (ต้อง simulate; master-side observable) |
| XT-03 installment ใช้ที่ AP/AR | GL (ENG-PT-01) | TC-XT03 (ต้อง simulate) |
| XT-04 deposit VAT ณ จุดรับเงิน | Tax Code/GL | TC-XT04 (ต้อง simulate — OQ-PAY-04) |
| XT-05 trigger resolver คลัง | Warehouse (ENG-PT-02) | TC-XT05 (ต้อง simulate) |
| XT-06 central plan [config] edges | PO/AR/AP | TC-XT06 (ต้อง simulate) |

### Scope Lock (07_LOCKED §7.0) — LOCK ทุกข้อต้องมีเคส verify
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LD-01 / LD-F-01 | PR ไม่มี · use_in = 7 (PO/SO เท่านั้นฝั่งเอกสารซื้อขาย) | TC-SL02 |
| LD-05 | Direct ไม่ผ่าน PR/PO/SO | TC-C07, TC-SL02 |
| LD-08b | Credit trigger = ทันที (locked, แก้ไม่ได้) | TC-SL03 |
| LD-09 / BR-04 | installment รวม 100% | TC-V07, TC-C08 |
| LD-15 | Installment ≠ Partial (2 ประเภทแยก) | TC-C08, TC-C09 |
| VD-PDM (no single-delete) | ไม่มีปุ่มลบเดี่ยวในแถว | TC-SL04 |
| VD-PDM (no CSV) | ไม่มี import/export CSV | TC-SL01 |
| VD-PDM (no hint/field-help) | ตัด hint/field-help | TC-SL07 |
| Governance (DOA null / no approval) | ไม่มี approval UI | TC-SL05 |
| LD-F-05 (AD-02) | ส่วนลดจ่ายเร็ว 1 ช่วง | TC-AD02 |
| LD-F-06 (AD-03) | ไม่มี multi-currency | TC-AD03, TC-SL06 |
| Central Plan | soft-ref snapshot / no hard delete used>0 | TC-D01, TC-D03, TC-XT01 |

### [AI-DEFAULT] propagation (05_RULES · §0.8)
| AD | ข้อ | Case |
|---|---|---|
| AD-01 | used>0 = แก้ได้ / ลบไม่ได้ | TC-AD01 (+ TC-E01, TC-D01) |
| AD-02 | ส่วนลดจ่ายเร็ว 1 ช่วง | TC-AD02 |
| AD-03 | ไม่รองรับ multi-currency (THB) | TC-AD03 |
| AD-04 | optimistic-lock + idempotency | TC-CC01, TC-CC02 (ต้อง simulate) |

### UI states / interaction
| item | cases |
|---|---|
| loaded list | TC-L01 |
| filtered-empty ("ไม่พบเงื่อนไขที่ตรงกับการค้นหา") | TC-L03 |
| scroll preservation (Iron Rule #29) | TC-EC01 |
| Esc chain (sdd→modal→drawer→sidebar) | TC-EC02 |
| hamburger ≤1180 / responsive | TC-EC09 → รวมใน TC-EC02b |
| installment live total badge | TC-EC03, TC-EC04 |
| toast top-center + 5s error | TC-V01 (สังเกต), ทุกเคส negative |

---

## Data Sets

> ทุกค่ากรอกได้จริง. code = **ตัวพิมพ์ใหญ่** (ระบบ upper อัตโนมัติขณะพิมพ์). ประเภทเลือกจาก dropdown "ประเภทเงื่อนไข"
> ด้วย **label ที่เห็นบนจอ** (คอลัมน์ "label บนจอ" ด้านล่าง).

### ชุดถูก (happy)
| Set | code | ชื่อ TH | ชื่อ EN | ประเภท (label บนจอ) | ค่าเฉพาะ | use_in (checkbox) | สถานะ |
|---|---|---|---|---|---|---|---|
| CR-1 | NET90 | เครดิต 90 วัน | Net 90 | เครดิต N วัน (Credit) | credit_days=90 | Purchase Order | ใช้งาน |
| CR-DISC | 2-10N60 | เครดิต 60 ลดเร็ว 2% | 2/10 Net 60 | เครดิต N วัน (Credit) | credit_days=60, ส่วนลด=2%, ภายใน=10 | Purchase Order | ใช้งาน |
| PREPAY-1 | PREPAY100 | ชำระเต็มก่อนส่ง 100% | Full Prepay | ชำระเต็มก่อนส่ง (Full Prepay) | — | Sales Order | ใช้งาน |
| POST-1 | POST7 | ชำระเต็มหลังรับ 7 วัน | Postpay 7 | ชำระเต็มหลังรับ (Full Postpay) | net_days=7 | Purchase Order, AP Invoice | ใช้งาน |
| DEP-1 | DEP20 | มัดจำ 20% | 20% Deposit | มัดจำ + ส่วนเหลือ (Deposit) | method=เปอร์เซ็นต์, value=20, remaining=หลังได้รับสินค้า, net_days=30 | Sales Order | ใช้งาน |
| DEP-MAN | DEP-M | มัดจำกำหนดเอง | Deposit manual | มัดจำ + ส่วนเหลือ (Deposit) | method=กำหนดเองตอนสร้างเอกสาร (value ซ่อน), net_days=30 | Sales Order | ใช้งาน |
| INST-1 | INST24 | แบ่ง 2 งวด 50/50 | 2 Installments | แบ่งงวด (Installment) | งวด1=50%, งวด2=50% | Purchase Order | ใช้งาน |
| PARTIAL-1 | PART1 | ทยอยส่ง | Partial | ทยอยส่ง (Partial Delivery) | net_days ต่อรอบ=0 | Purchase Order | ใช้งาน |
| DIRECT-1 | DIRECT-OT | จ่ายตรง อื่น ๆ | Direct Other | Direct Payment (จ่ายตรง) | หมวด=ค่าใช้จ่ายอื่น | AP Invoice | ใช้งาน |
| DUE-1 | EOMTEST | เครดิตสิ้นเดือน | EOM test | เครดิต N วัน (Credit) | credit_days=30, Due basis=นับจากสิ้นเดือน (End of Month) | Purchase Order | ใช้งาน |

### ชุดผิด (negative)
| Set | อธิบาย | ค่า |
|---|---|---|
| NEG-CODE-EMPTY | code ว่าง | เว้น code, name=ทดสอบ, type=credit, use_in=PO |
| NEG-DUP | code ซ้ำของจริง | code=**NET30** (ตรงกับ t3), name=ทดสอบซ้ำ, type=credit, use_in=PO |
| NEG-NAME-EMPTY | ชื่อ TH ว่าง | code=NAMEX, เว้น name, type=credit, use_in=PO |
| NEG-CREDIT-0 | credit วัน ≤0 | code=CR0, name=ทดสอบ, type=credit, credit_days=0, use_in=PO |
| NEG-INST-SUM | งวดรวม ≠100 | type=installment, งวด1=50, งวด2=30 (=80%), use_in=PO |
| NEG-DEP-0 | มัดจำ % =0 | type=deposit, method=%, value=0, use_in=SO |
| NEG-DEP-101 | มัดจำ % >100 | type=deposit, method=%, value=101, use_in=SO |
| NEG-USEIN | ไม่เลือก use_in | code=NOUSE, name=ทดสอบ, type=credit, credit_days=30, use_in=(ว่าง) |
| NEG-DISC-GE | ส่วนลดวัน ≥ credit | type=credit, credit_days=30, ส่วนลด=2%, ภายใน=30 |
| NEG-DISC-0 | ส่วนลดวัน =0 | type=credit, credit_days=30, ส่วนลด=2%, ภายใน=0 |
| NEG-DEFAULT | default บนสถานะ ≠ ใช้งาน | Set CR-1 valid + toggle Default ON + สถานะ=ร่าง |

### ไฟล์ทดสอบ (Files)
- **ไม่มี** — feature นี้ไม่มี CSV import/upload (BR-09). ทุกเคส `files=—`.

---

## Test Cases

### GROUP A — List / Search / Filter (P-01)

#### TC-L01 — เปิดหน้า List เห็นโครงครบ (happy / loaded)
- group: List · ความสำคัญ: สูง · trace: AT-13 / FN-04 / US-08
- actor (role): Finance Admin
- Setup: role=finance_admin · seed=12 terms ตามตาราง Meta · files=—
- Start: OPEN `#/finance/payment-term` (โหลด `f-payterm.html`)
- ผ่านเมื่อ: เห็นหัวข้อ + stat 4 ใบ + ตาราง 12 แถว + footer นับถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/finance/payment-term` | — | หน้า List โหลด · breadcrumb "การเงิน › เงื่อนไขชำระเงิน" · sidebar "เงื่อนไขชำระเงิน" เป็น active (แดง) | ☐ |
| 2 | VERIFY หัวข้อหน้า | — | เห็น "เงื่อนไขชำระเงิน" + badge "**12 เงื่อนไข**" | ☐ |
| 3 | VERIFY แถบ Stats (4 ใบ) | — | "ทั้งหมด **12**" · "ใช้งาน **10**" · "ไม่ใช้งาน **1**" · "ร่าง **1**" | ☐ |
| 4 | VERIFY ตาราง | — | หัวคอลัมน์: (checkbox) · รหัส · ชื่อเงื่อนไข · ประเภท · สรุปเงื่อนไข · สถานะ · จัดการ · มี 12 แถว | ☐ |
| 5 | VERIFY แถว NET30 | — | รหัส "NET30" มี **ดาว ⭐** ต่อท้าย · pill ประเภท "เครดิต N วัน" · pill สถานะ "ใช้งาน" (เขียว) | ☐ |
| 6 | VERIFY footer ตาราง | — | ข้อความ "แสดง **12** จาก **12** เงื่อนไข" | ☐ |
| 7 | VERIFY ปุ่ม toolbar | — | มีปุ่ม "เพิ่มเงื่อนไข" (แดง) ปุ่มเดียว — ไม่มีปุ่ม import/export | ☐ |

#### TC-L02 — ค้นหาด้วยรหัส (search พบ)
- group: List · ความสำคัญ: สูง · trace: AT-13 / FN-04
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: กรองเหลือเฉพาะแถวที่ตรง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่องค้นหา "ค้นหารหัส หรือชื่อเงื่อนไข..." | — | โฟกัสช่องค้นหา | ☐ |
| 2 | TYPE "NET30" → ช่องค้นหา | NET30 | ตารางเหลือ 1 แถว = รหัส "NET30" · footer "แสดง **1** จาก 12 เงื่อนไข" | ☐ |
| 3 | VERIFY caret/โฟกัส | — | โฟกัสยังอยู่ในช่องค้นหา (ไม่เด้งออก) · ตารางไม่เด้ง scroll ขึ้นบน | ☐ |

#### TC-L03 — ค้นหาไม่พบ (filtered-empty)
- group: List · ความสำคัญ: กลาง · trace: AT-13 / empty state
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ZZZNONE" → ช่องค้นหา | ZZZNONE | ตารางแสดงข้อความว่าง "**ไม่พบเงื่อนไขที่ตรงกับการค้นหา**" · footer "แสดง **0** จาก 12 เงื่อนไข" | ☐ |
| 2 | Clear ช่องค้นหา (ลบข้อความ) | (ว่าง) | ตารางกลับมา 12 แถว | ☐ |

#### TC-L04 — ค้นหาด้วยชื่อภาษาไทย
- group: List · ความสำคัญ: กลาง · trace: AT-13
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "เครดิต" → ช่องค้นหา | เครดิต | เหลือเฉพาะแถวที่ชื่อมี "เครดิต" (NET30/NET60/2-10N30/NET45 = 4 แถว) · footer "แสดง **4** จาก 12" | ☐ |

#### TC-L05 — ค้นหาด้วยชื่อภาษาอังกฤษ (name_en)
- group: List · ความสำคัญ: กลาง · trace: AT-13 / FN-04
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "Net 30" → ช่องค้นหา | Net 30 | เหลือแถวที่ name_en มี "Net 30" (NET30 "Net 30") · อย่างน้อย 1 แถว | ☐ |

#### TC-L06 — กรองด้วย Type filter = เครดิต
- group: List · ความสำคัญ: สูง · trace: AT-13 / FN-04
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dropdown ประเภท (ค่าเริ่มต้น "ทุกประเภท") | — | panel เปิด เห็น 8 ตัวเลือก (ทุกประเภท + 7 ประเภท) แต่ละบรรทัดมีคำอธิบายย่อยบรรทัดที่ 2 | ☐ |
| 2 | CLICK ตัวเลือก "เครดิต N วัน (Credit)" | — | panel ปิด · trigger แสดง "เครดิต N วัน (Credit)" · ตารางเหลือ **5** แถว (NET30/NET60/2-10N30/EOM30/NET45) · footer "แสดง 5 จาก 12" | ☐ |

#### TC-L07 — กรองด้วย Type filter = มัดจำ + ค้นหาใน 7 ประเภท
- group: List · ความสำคัญ: กลาง · trace: AT-13
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dropdown ประเภท → CLICK "มัดจำ + ส่วนเหลือ (Deposit)" | — | ตารางเหลือ 2 แถว (DEP50, DEP30) · footer "แสดง 2 จาก 12" | ☐ |
| 2 | CLICK dropdown ประเภท → พิมพ์ "direct" ในช่องค้นหา panel | direct | รายการ dropdown เหลือ "Direct Payment (จ่ายตรง)" | ☐ |
| 3 | CLICK "Direct Payment (จ่ายตรง)" | — | ตารางเหลือ 1 แถว (DIRECT-UTIL) | ☐ |

#### TC-L08 — Stat card filter = ร่าง (toggle-on)
- group: List · ความสำคัญ: สูง · trace: AT-13 / FN-04
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด "ร่าง" | — | การ์ด "ร่าง" ขึ้นกรอบแดง (is-on) · ตารางเหลือ **1** แถว (NET45, pill "ร่าง") · footer "แสดง 1 จาก 12" | ☐ |

#### TC-L09 — Stat card toggle-off (กดซ้ำยกเลิก)
- group: List · ความสำคัญ: กลาง · trace: AT-13
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด "ใช้งาน" | — | ตารางเหลือ 10 แถว · การ์ด "ใช้งาน" is-on | ☐ |
| 2 | CLICK การ์ด "ใช้งาน" ซ้ำ | — | filter ยกเลิก · ตารางกลับมา 12 แถว · การ์ดไม่มีกรอบแดง | ☐ |
| 3 | CLICK การ์ด "ทั้งหมด" | — | reset ทั้ง type+status · ตาราง 12 แถว | ☐ |

#### TC-L10 — filter ผสม (stat + type + search) ทำงานร่วมกัน
- group: List · ความสำคัญ: กลาง · trace: AT-13
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด "ใช้งาน" | — | 10 แถว | ☐ |
| 2 | CLICK dropdown ประเภท → "เครดิต N วัน (Credit)" | — | เหลือเครดิตที่ active (NET30/2-10N30/EOM30 = 3 แถว; NET60 inactive/NET45 draft ถูกตัด) | ☐ |
| 3 | TYPE "EOM" → ช่องค้นหา | EOM | เหลือ 1 แถว (EOM30) · footer "แสดง 1 จาก 12" | ☐ |

#### TC-L11 — Select all (checkbox หัวตาราง) เฉพาะที่มองเห็น
- group: List · ความสำคัญ: กลาง · trace: AT-13 / bulk selection
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด "ร่าง" | — | 1 แถว (NET45) | ☐ |
| 2 | CLICK checkbox หัวตาราง (select all) | — | แถว NET45 ถูกติ๊ก (พื้นแถวชมพู) · โผล่แถบ bulk ขาว "เลือก **1** รายการ" | ☐ |
| 3 | CLICK การ์ด "ทั้งหมด" | — | ตาราง 12 แถว · การเลือกยังคง 1 รายการ (bulk bar ยังโชว์ "เลือก 1 รายการ") | ☐ |

#### TC-L12 — คลิกแถว เปิด View drawer
- group: List · ความสำคัญ: สูง · trace: AT-13 / P-04
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "NET30" (นอกช่อง checkbox/ปุ่มแก้ไข) | — | drawer เลื่อนเข้าจากขวา · หัว drawer = ชื่อ "เครดิต 30 วัน" + code "NET30" + pill "เครดิต N วัน" | ☐ |
| 2 | VERIFY เนื้อ drawer | — | การ์ด "สรุปเงื่อนไข" = "ครบกำหนด 30 วัน" · section "รายละเอียดการคำนวณ" มีแถว "ครบกำหนด / 30 วัน" | ☐ |
| 3 | VERIFY use-tags + default | — | section "การใช้งานในเอกสาร" แสดง tag เอกสาร · มีแถว "ค่า Default / ✓ เลือกอัตโนมัติในเอกสารใหม่" | ☐ |
| 4 | CLICK ปุ่ม "ปิด" | — | drawer ปิด กลับหน้า List | ☐ |

---

### GROUP B — Create Happy (7 ประเภท + trigger/due_basis)

#### TC-C01 — สร้างเครดิต (Credit) ครบ field (happy · AT-01)
- group: Create · ความสำคัญ: สูง · trace: AT-01 / BR-01,02,06 / US-01
- actor (role): Finance Admin
- Setup: role=finance_admin · seed=seed 12 (ไม่มี code NET90) · files=—
- Start: OPEN `#/finance/payment-term` → CLICK ปุ่ม "เพิ่มเงื่อนไข"
- ชุดข้อมูล: CR-1
- ผ่านเมื่อ: drawer ปิด + toast "สร้างเงื่อนไขชำระเงินแล้ว" + แถวใหม่ NET90 ปรากฏ · badge นับเป็น 13

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม "เพิ่มเงื่อนไข" | — | drawer เปิด หัวข้อ "**เพิ่มเงื่อนไขชำระเงิน**" · footer ปุ่ม "บันทึกและสร้าง" · ประเภท default = "เครดิต N วัน (Credit)" · ช่อง "จำนวนวันเครดิต" = 30 | ☐ |
| 2 | TYPE "NET90" → ช่อง "รหัส (Code)" | CR-1 | ช่องแสดง "NET90" (ตัวพิมพ์ใหญ่) | ☐ |
| 3 | TYPE "เครดิต 90 วัน" → ช่อง "ชื่อเงื่อนไข (TH)" | CR-1 | ช่องแสดงค่าที่กรอก | ☐ |
| 4 | TYPE "Net 90" → ช่อง "ชื่อเงื่อนไข (EN)" | CR-1 | ช่องแสดงค่าที่กรอก | ☐ |
| 5 | TYPE "90" → ช่อง "จำนวนวันเครดิต (credit_days)" | CR-1 | ช่องแสดง 90 | ☐ |
| 6 | VERIFY trigger เครดิต | — | เห็น badge ล็อก "Warehouse/GRN trigger: ทันที (หลัง PO/SO Confirm) (ล็อกตามประเภท)" — ไม่มี dropdown | ☐ |
| 7 | CLICK checkbox "Purchase Order" (กลุ่ม ฝั่งซื้อ (P2P)) | CR-1 | checkbox ติ๊ก (กรอบแดง) · badge "การใช้งานในเอกสาร" = "1 เลือก" | ☐ |
| 8 | CLICK ปุ่ม "บันทึกและสร้าง" | — | drawer ปิด · WAIT toast (top-center) "**สร้างเงื่อนไขชำระเงินแล้ว**" (เขียว) | ☐ |
| 9 | VERIFY List | — | badge หัวหน้า "**13** เงื่อนไข" · มีแถว "NET90" ประเภท "เครดิต N วัน" สถานะ "ใช้งาน" | ☐ |

#### TC-C02 — สร้าง Full Postpay (net_days + trigger default immediate · AT-16)
- group: Create · ความสำคัญ: สูง · trace: AT-01,16 / BR-02,11
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: POST-1
- ผ่านเมื่อ: toast success + แถว POST7

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มเงื่อนไข" → CLICK dropdown "ประเภทเงื่อนไข" → CLICK "ชำระเต็มหลังรับ (Full Postpay)" | POST-1 | field set เปลี่ยน · เห็นช่อง "ชำระภายใน (วันหลังรับของ)" · เห็น dropdown "Warehouse / GRN / Ship Trigger" ค่าเริ่ม "ทันที (หลัง PO/SO Confirm)" | ☐ |
| 2 | TYPE "POST7" → รหัส · TYPE "ชำระเต็มหลังรับ 7 วัน" → ชื่อ TH | POST-1 | ช่องแสดงค่า | ☐ |
| 3 | TYPE "7" → "ชำระภายใน (วันหลังรับของ)" | POST-1 | ช่องแสดง 7 | ☐ |
| 4 | CLICK checkbox "Purchase Order" + "AP Invoice" | POST-1 | badge "2 เลือก" | ☐ |
| 5 | CLICK "บันทึกและสร้าง" | — | drawer ปิด · toast "สร้างเงื่อนไขชำระเงินแล้ว" · แถว POST7 ประเภท "ชำระเต็มหลังรับ" | ☐ |

#### TC-C03 — สร้าง Full Prepay (trigger default after_full · AT-16)
- group: Create · ความสำคัญ: สูง · trace: AT-01,16 / BR-11
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: PREPAY-1
- ผ่านเมื่อ: toast success + แถว PREPAY100

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มเงื่อนไข" → dropdown ประเภท → "ชำระเต็มก่อนส่ง (Full Prepay)" | PREPAY-1 | field เฉพาะประเภท = trigger dropdown เท่านั้น · ค่า trigger เริ่มต้น = "หลังชำระเต็มจำนวน" (after_full) | ☐ |
| 2 | TYPE "PREPAY100" → รหัส · TYPE "ชำระเต็มก่อนส่ง 100%" → ชื่อ TH | PREPAY-1 | ช่องแสดงค่า | ☐ |
| 3 | CLICK checkbox "Sales Order" (กลุ่ม ฝั่งขาย (S2C)) | PREPAY-1 | badge "1 เลือก" | ☐ |
| 4 | CLICK "บันทึกและสร้าง" | — | toast "สร้างเงื่อนไขชำระเงินแล้ว" · แถว PREPAY100 ประเภท "ชำระเต็มก่อนส่ง" | ☐ |

#### TC-C04 — สร้าง Deposit แบบ % (happy · AT-05/16)
- group: Create · ความสำคัญ: สูง · trace: AT-01,16 / BR-03,11
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: DEP-1
- ผ่านเมื่อ: toast success + แถว DEP20

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มเงื่อนไข" → dropdown ประเภท → "มัดจำ + ส่วนเหลือ (Deposit)" | DEP-1 | เห็นช่อง "วิธีระบุมัดจำ" (ค่า "เปอร์เซ็นต์ (%)") · "มูลค่ามัดจำ" (มี suffix %) · "ชำระส่วนที่เหลือ (remaining)" · "ส่วนที่เหลือ ครบกำหนด (วัน)" · trigger dropdown ค่าเริ่ม "หลังชำระมัดจำ" | ☐ |
| 2 | TYPE "DEP20" → รหัส · TYPE "มัดจำ 20%" → ชื่อ TH | DEP-1 | ช่องแสดงค่า | ☐ |
| 3 | Clear "มูลค่ามัดจำ" แล้ว TYPE "20" | DEP-1 | ช่องแสดง 20 · suffix "%" | ☐ |
| 4 | CLICK checkbox "Sales Order" | DEP-1 | badge "1 เลือก" | ☐ |
| 5 | CLICK "บันทึกและสร้าง" | — | toast "สร้างเงื่อนไขชำระเงินแล้ว" · แถว DEP20 ประเภท "มัดจำ + ส่วนเหลือ" | ☐ |

#### TC-C05 — สร้าง Deposit method = manual → ช่อง value ซ่อน (happy · AT-05b / EC-09)
- group: Create · ความสำคัญ: สูง · trace: AT-05b / EC-09 / BR-03
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: DEP-MAN
- ผ่านเมื่อ: บันทึกได้โดยไม่ต้องกรอกมูลค่ามัดจำ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มเงื่อนไข" → dropdown ประเภท → "มัดจำ + ส่วนเหลือ (Deposit)" | — | ฟอร์ม deposit แสดง ช่อง "มูลค่ามัดจำ" ปรากฏ | ☐ |
| 2 | CLICK dropdown "วิธีระบุมัดจำ" → CLICK "กำหนดเองตอนสร้างเอกสาร" | DEP-MAN | ช่อง "มูลค่ามัดจำ" **หายไป** (ไม่ต้องกรอก) | ☐ |
| 3 | TYPE "DEP-M" → รหัส · TYPE "มัดจำกำหนดเอง" → ชื่อ TH · CLICK checkbox "Sales Order" | DEP-MAN | ช่องแสดงค่า · badge "1 เลือก" | ☐ |
| 4 | CLICK "บันทึกและสร้าง" | — | ไม่มี error เรื่องมูลค่ามัดจำ · toast "สร้างเงื่อนไขชำระเงินแล้ว" · แถว DEP-M | ☐ |

#### TC-C06 — สร้าง Installment 2 งวด รวม 100% (happy · AT-04)
- group: Create · ความสำคัญ: สูง · trace: AT-04,16 / BR-04 / ENG-PT-01 / LD-09
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: INST-1
- ผ่านเมื่อ: badge "รวม 100% ✓" + toast success

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มเงื่อนไข" → dropdown ประเภท → "แบ่งงวด (Installment)" | INST-1 | เห็น "ตารางงวดการชำระเงิน (Schedule)" มี 2 งวด default (งวด 1 = 50, งวด 2 = 50) · badge "**รวม 100% ✓**" (เขียว) · trigger dropdown default "ทันที (หลัง PO/SO Confirm)" | ☐ |
| 2 | TYPE "INST24" → รหัส · TYPE "แบ่ง 2 งวด 50/50" → ชื่อ TH | INST-1 | ช่องแสดงค่า | ☐ |
| 3 | CLICK checkbox "Purchase Order" | INST-1 | badge "1 เลือก" | ☐ |
| 4 | CLICK "บันทึกและสร้าง" | — | toast "สร้างเงื่อนไขชำระเงินแล้ว" · แถว INST24 ประเภท "แบ่งงวด" สรุป "2 งวด (50% / 50%)" | ☐ |

#### TC-C07 — สร้าง Direct Payment → ปิด po/quotation/so + ไม่มี trigger/due_basis (AT-17 / EC-10)
- group: Create · ความสำคัญ: สูง · trace: AT-17 / BR-12 / EC-10 / LD-05
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: DIRECT-1
- ผ่านเมื่อ: po/quotation/so ถูกปิด ("ไม่รองรับ") + ไม่มี trigger/due_basis + toast success

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มเงื่อนไข" → dropdown ประเภท → "Direct Payment (จ่ายตรง)" | DIRECT-1 | เห็นช่อง "หมวดหมู่ค่าใช้จ่าย" (ค่าเริ่ม "ค่าสาธารณูปโภค") · note เตือน "ประเภทนี้**ไม่ผ่าน PR/PO/QUO→SO**…" · **ไม่มี** dropdown trigger · **ไม่มี** ช่อง "นับวันครบกำหนดจาก (Due basis)" | ☐ |
| 2 | VERIFY use_in ที่ถูกปิด | — | checkbox "Purchase Order", "Quotation", "Sales Order" เป็นสีจาง มีป้าย "**ไม่รองรับ**" กดไม่ได้ | ☐ |
| 3 | CLICK dropdown "หมวดหมู่ค่าใช้จ่าย" → "ค่าใช้จ่ายอื่น" | DIRECT-1 | ช่องแสดง "ค่าใช้จ่ายอื่น" | ☐ |
| 4 | TYPE "DIRECT-OT" → รหัส · TYPE "จ่ายตรง อื่น ๆ" → ชื่อ TH · CLICK checkbox "AP Invoice" | DIRECT-1 | badge "1 เลือก" | ☐ |
| 5 | CLICK "บันทึกและสร้าง" | — | toast "สร้างเงื่อนไขชำระเงินแล้ว" · แถว DIRECT-OT ประเภท "Direct Payment" | ☐ |

#### TC-C08 — สร้าง Installment 3 งวด (เพิ่ม/ปรับงวด · LD-15 Installment≠Partial)
- group: Create · ความสำคัญ: กลาง · trace: AT-04 / BR-04 / LD-09,15
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" → เลือกประเภท "แบ่งงวด (Installment)"
- ผ่านเมื่อ: 3 งวด รวม 100% → toast success

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกประเภท "แบ่งงวด (Installment)" | — | 2 งวด default (50/50) badge "รวม 100% ✓" | ☐ |
| 2 | CLICK ปุ่ม "เพิ่มงวด" | — | เพิ่มการ์ด "งวด 3" (%=0) · badge เปลี่ยนเป็น "รวม 100% ✓" ยังคง (งวด 3 = 0) → จริง ๆ รวม 100 · **ปรับ:** badge = "รวม 100%…" | ☐ |
| 3 | Clear % งวด 1 → TYPE "40" · Clear % งวด 2 → TYPE "30" · Clear % งวด 3 → TYPE "30" | 40/30/30 | badge live "**รวม 100% ✓**" (เขียว) | ☐ |
| 4 | TYPE "INST3B" → รหัส · TYPE "แบ่ง 3 งวด" → ชื่อ TH · CLICK checkbox "Sales Order" | — | badge "1 เลือก" | ☐ |
| 5 | CLICK "บันทึกและสร้าง" | — | toast "สร้างเงื่อนไขชำระเงินแล้ว" · แถวใหม่ ประเภท "แบ่งงวด" สรุป "3 งวด (40% / 30% / 30%)" | ☐ |

#### TC-C09 — สร้าง Partial Delivery (แยกจาก Installment · LD-15)
- group: Create · ความสำคัญ: กลาง · trace: AT-01 / BR-13 / LD-10,15
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: PARTIAL-1
- ผ่านเมื่อ: toast success + สรุป "ทยอยส่ง…"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกประเภท "ทยอยส่ง (Partial Delivery)" | PARTIAL-1 | เห็นช่อง "เครดิตต่อรอบ (วัน, optional)" · **ไม่มี** schedule editor (ต่างจาก Installment) · due_basis ตั้งค่า "นับจากวันส่ง/รับของ" | ☐ |
| 2 | TYPE "PART1" → รหัส · TYPE "ทยอยส่ง" → ชื่อ TH · CLICK checkbox "Purchase Order" | PARTIAL-1 | badge "1 เลือก" | ☐ |
| 3 | CLICK "บันทึกและสร้าง" | — | toast "สร้างเงื่อนไขชำระเงินแล้ว" · แถว PART1 ประเภท "ทยอยส่ง" สรุป "ทยอยส่ง · ชำระตามจำนวนที่รับจริงแต่ละรอบ" | ☐ |

#### TC-C10 — Due basis เลือกได้ 3 ค่า (AT-18)
- group: Create · ความสำคัญ: กลาง · trace: AT-18 / BR-13
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: DUE-1
- ผ่านเมื่อ: dropdown "นับวันครบกำหนดจาก (Due basis)" มี 3 ค่า + บันทึกด้วย eom ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกประเภท "เครดิต N วัน (Credit)" (default) · CLICK dropdown "นับวันครบกำหนดจาก (Due basis)" | — | panel แสดง **3 ตัวเลือก**: "นับจากวันที่ใบแจ้งหนี้" · "นับจากสิ้นเดือน (End of Month)" · "นับจากวันส่ง/รับของ" | ☐ |
| 2 | CLICK "นับจากสิ้นเดือน (End of Month)" | DUE-1 | trigger due_basis แสดง "นับจากสิ้นเดือน (End of Month)" | ☐ |
| 3 | TYPE "EOMTEST" → รหัส · TYPE "เครดิตสิ้นเดือน" → ชื่อ TH · TYPE "30" → จำนวนวันเครดิต · CLICK checkbox "Purchase Order" | DUE-1 | ค่าครบ | ☐ |
| 4 | CLICK "บันทึกและสร้าง" | — | toast "สร้างเงื่อนไขชำระเงินแล้ว" · แถว EOMTEST | ☐ |

#### TC-C11 — สร้าง Credit พร้อมส่วนลดจ่ายเร็ว (happy · discount valid)
- group: Create · ความสำคัญ: กลาง · trace: AT-08 / BR-05
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: CR-DISC
- ผ่านเมื่อ: discount_days(10) < net_days(60) → toast success

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มเงื่อนไข" (ประเภท default credit) · TYPE "2-10N60" → รหัส · TYPE "เครดิต 60 ลดเร็ว 2%" → ชื่อ TH | CR-DISC | ช่องแสดงค่า | ☐ |
| 2 | Clear "จำนวนวันเครดิต" → TYPE "60" | CR-DISC | ช่อง = 60 | ☐ |
| 3 | TYPE "2" → "ส่วนลดจ่ายเร็ว (%)" · TYPE "10" → "ภายในกี่วัน (Discount days)" | CR-DISC | ช่องแสดง 2 และ 10 | ☐ |
| 4 | CLICK checkbox "Purchase Order" | CR-DISC | badge "1 เลือก" | ☐ |
| 5 | CLICK "บันทึกและสร้าง" | — | toast "สร้างเงื่อนไขชำระเงินแล้ว" · สรุปมี "· ลด 2% ถ้าจ่ายใน 10 วัน" | ☐ |

---

### GROUP C — Create Validation / Negative

> ทุกเคสในกลุ่มนี้: toast แสดง **บนสุดกึ่งกลางจอ** ค้าง ~5 วินาที (error) · drawer **ไม่ปิด** · ช่องที่ผิดขึ้นกรอบแดง (is-invalid).

#### TC-V01 — code ว่าง → block (negative · ERR_CODE_REQUIRED)
- group: Validation · ความสำคัญ: สูง · trace: AT-02 / BR-01 / ERR_CODE_REQUIRED
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: NEG-CODE-EMPTY
- ผ่านเมื่อ: บันทึกไม่ได้ + ช่องรหัสขึ้น error "กรุณากรอกรหัส"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เว้นช่อง "รหัส (Code)" ว่าง · TYPE "ทดสอบ" → ชื่อ TH · CLICK checkbox "Purchase Order" | NEG-CODE-EMPTY | รหัสว่าง | ☐ |
| 2 | CLICK "บันทึกและสร้าง" | — | drawer **ไม่ปิด** · ช่อง "รหัส (Code)" กรอบแดง + ข้อความใต้ช่อง "**กรุณากรอกรหัส**" | ☐ |
| 3 | VERIFY ตำแหน่ง toast | — | ไม่มีแถวใหม่ใน List (ยังไม่บันทึก) | ☐ |

#### TC-V02 — code ซ้ำ NET30 → block (negative · ERR_DUPLICATE_CODE)
- group: Validation · ความสำคัญ: สูง · trace: AT-02 / BR-01 / ERR_DUPLICATE_CODE
- Setup: role=finance_admin · seed=seed มี t3 code=NET30 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: NEG-DUP
- ผ่านเมื่อ: ช่องรหัส error "รหัสนี้มีอยู่แล้ว — ใช้รหัสอื่น" + toast "รหัสเงื่อนไขนี้มีอยู่แล้ว"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "NET30" → รหัส · TYPE "ทดสอบซ้ำ" → ชื่อ TH · CLICK checkbox "Purchase Order" | NEG-DUP | ช่องรหัส = NET30 | ☐ |
| 2 | CLICK "บันทึกและสร้าง" | — | drawer ไม่ปิด · ช่องรหัสกรอบแดง + ข้อความ "**รหัสนี้มีอยู่แล้ว — ใช้รหัสอื่น**" | ☐ |
| 3 | WAIT toast ≤5s | — | toast error (top-center) "**รหัสเงื่อนไขนี้มีอยู่แล้ว**" | ☐ |

#### TC-V03 — code ซ้ำ (case/space) — ตรวจ trim/uppercase (negative)
- group: Validation · ความสำคัญ: กลาง · trace: AT-02 / BR-01
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ผ่านเมื่อ: พิมพ์ "net30" (ตัวเล็ก) → ระบบ upper เป็น NET30 → ซ้ำ block

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "net30" → รหัส | — | ช่องแสดง "NET30" (upper อัตโนมัติขณะพิมพ์) | ☐ |
| 2 | TYPE "ทดสอบ" → ชื่อ TH · CLICK checkbox "Purchase Order" · CLICK "บันทึกและสร้าง" | — | block · ช่องรหัส "รหัสนี้มีอยู่แล้ว — ใช้รหัสอื่น" + toast "รหัสเงื่อนไขนี้มีอยู่แล้ว" | ☐ |

#### TC-V04 — ชื่อ TH ว่าง → block (negative · ERR_NAME_REQUIRED)
- group: Validation · ความสำคัญ: สูง · trace: AT-02 (name) / ERR_NAME_REQUIRED
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: NEG-NAME-EMPTY
- ผ่านเมื่อ: ช่องชื่อ TH ขึ้นกรอบแดง drawer ไม่ปิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "NAMEX" → รหัส · เว้นช่อง "ชื่อเงื่อนไข (TH)" · CLICK checkbox "Purchase Order" | NEG-NAME-EMPTY | ชื่อว่าง | ☐ |
| 2 | CLICK "บันทึกและสร้าง" | — | drawer ไม่ปิด · ช่อง "ชื่อเงื่อนไข (TH)" กรอบแดง · ไม่มีแถวใหม่ | ☐ |

#### TC-V05 — credit net_days = 0 → block (negative · ERR_CREDIT_DAYS_INVALID)
- group: Validation · ความสำคัญ: สูง · trace: AT-03 / BR-02 / ERR_CREDIT_DAYS_INVALID
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" (ประเภท credit)
- ชุดข้อมูล: NEG-CREDIT-0
- ผ่านเมื่อ: toast "จำนวนวันเครดิตต้องมากกว่า 0"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "CR0" → รหัส · TYPE "ทดสอบ" → ชื่อ TH | NEG-CREDIT-0 | ช่องแสดงค่า | ☐ |
| 2 | Clear "จำนวนวันเครดิต" → TYPE "0" | NEG-CREDIT-0 | ช่อง = 0 | ☐ |
| 3 | CLICK checkbox "Purchase Order" · CLICK "บันทึกและสร้าง" | — | drawer ไม่ปิด · WAIT toast error "**จำนวนวันเครดิตต้องมากกว่า 0**" | ☐ |

#### TC-V06 — installment ปุ่มลบงวด disabled ที่ 2 งวด (guard <2 · AT-04)
- group: Validation · ความสำคัญ: สูง · trace: AT-04 / BR-04 / ERR_INSTALLMENT_COUNT
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" → ประเภท "แบ่งงวด (Installment)"
- ผ่านเมื่อ: เมื่อเหลือ 2 งวด ปุ่มลบ (ถังขยะ) ถูก disable → ป้องกัน <2 งวด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกประเภท "แบ่งงวด (Installment)" | — | เห็น 2 งวด default | ☐ |
| 2 | VERIFY ปุ่มลบ (ไอคอนถังขยะ) ในการ์ด "งวด 1" และ "งวด 2" | — | ปุ่มลบเป็นสีจาง (opacity ต่ำ) กดไม่ได้ (disabled) — เพราะเหลือ 2 งวดพอดี | ☐ |
| 3 | CLICK ปุ่ม "เพิ่มงวด" | — | มี 3 งวด · ปุ่มลบทั้ง 3 งวดกดได้แล้ว | ☐ |
| 4 | CLICK ปุ่มลบ (ถังขยะ) การ์ด "งวด 3" | — | เหลือ 2 งวด · ปุ่มลบกลับเป็น disabled อีกครั้ง | ☐ |

#### TC-V07 — installment รวม ≠ 100% → block (negative · ERR_INSTALLMENT_SUM)
- group: Validation · ความสำคัญ: สูง · trace: AT-04 / BR-04 / ERR_INSTALLMENT_SUM / ENG-PT-01
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" → ประเภท "แบ่งงวด (Installment)"
- ชุดข้อมูล: NEG-INST-SUM
- ผ่านเมื่อ: badge เตือน + toast "สัดส่วนงวดต้องรวมเป็น 100% (ตอนนี้ 80%)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกประเภท "แบ่งงวด (Installment)" · TYPE "INSTBAD" → รหัส · TYPE "งวดผิด" → ชื่อ TH | NEG-INST-SUM | ค่าครบ | ☐ |
| 2 | Clear % "งวด 1" → TYPE "50" · Clear % "งวด 2" → TYPE "30" | NEG-INST-SUM | badge live เปลี่ยนเป็น "**รวม 80% (ต้องเป็น 100%)**" (สีเหลือง/amber) | ☐ |
| 3 | CLICK checkbox "Purchase Order" · CLICK "บันทึกและสร้าง" | — | drawer ไม่ปิด · WAIT toast error "**สัดส่วนงวดต้องรวมเป็น 100% (ตอนนี้ 80%)**" | ☐ |

#### TC-V08 — deposit % > 100 → block (negative · ERR_DEPOSIT_PCT_INVALID)
- group: Validation · ความสำคัญ: กลาง · trace: AT-05 / BR-03 / ERR_DEPOSIT_PCT_INVALID
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" → ประเภท "มัดจำ + ส่วนเหลือ (Deposit)"
- ชุดข้อมูล: NEG-DEP-101
- ผ่านเมื่อ: toast "มัดจำแบบ % ต้องไม่เกิน 100"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกประเภท "มัดจำ + ส่วนเหลือ (Deposit)" · TYPE "DEP101" → รหัส · TYPE "มัดจำเกิน" → ชื่อ TH | NEG-DEP-101 | ค่าครบ | ☐ |
| 2 | Clear "มูลค่ามัดจำ" → TYPE "101" | NEG-DEP-101 | ช่อง = 101 | ☐ |
| 3 | CLICK checkbox "Sales Order" · CLICK "บันทึกและสร้าง" | — | drawer ไม่ปิด · ช่องมูลค่ามัดจำกรอบแดง · WAIT toast error "**มัดจำแบบ % ต้องไม่เกิน 100**" | ☐ |

#### TC-V09 — deposit % = 0 → block (negative · ERR_DEPOSIT_PCT_INVALID)
- group: Validation · ความสำคัญ: กลาง · trace: AT-05 / BR-03 / ERR_DEPOSIT_PCT_INVALID
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" → ประเภท "มัดจำ + ส่วนเหลือ (Deposit)"
- ชุดข้อมูล: NEG-DEP-0
- ผ่านเมื่อ: toast "มัดจำแบบ % ต้องมากกว่า 0"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกประเภท "มัดจำ + ส่วนเหลือ (Deposit)" · TYPE "DEP0" → รหัส · TYPE "มัดจำศูนย์" → ชื่อ TH | NEG-DEP-0 | ค่าครบ | ☐ |
| 2 | Clear "มูลค่ามัดจำ" → TYPE "0" | NEG-DEP-0 | ช่อง = 0 | ☐ |
| 3 | CLICK checkbox "Sales Order" · CLICK "บันทึกและสร้าง" | — | drawer ไม่ปิด · WAIT toast error "**มัดจำแบบ % ต้องมากกว่า 0**" | ☐ |

#### TC-V10 — ไม่เลือก use_in → block (negative · ERR_USE_IN_EMPTY)
- group: Validation · ความสำคัญ: สูง · trace: AT-06 / BR-06 / ERR_USE_IN_EMPTY
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: NEG-USEIN
- ผ่านเมื่อ: toast "เลือกเอกสารที่ใช้อย่างน้อย 1 รายการ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "NOUSE" → รหัส · TYPE "ทดสอบ" → ชื่อ TH · TYPE "30" → จำนวนวันเครดิต | NEG-USEIN | badge "การใช้งานในเอกสาร" = "0 เลือก" | ☐ |
| 2 | CLICK "บันทึกและสร้าง" (โดยไม่ติ๊ก use_in) | — | drawer ไม่ปิด · section use_in ขึ้น error "เลือกอย่างน้อย 1 เอกสาร" · WAIT toast error "**เลือกเอกสารที่ใช้อย่างน้อย 1 รายการ**" | ☐ |

#### TC-V11 — ตั้ง Default บนสถานะ ≠ ใช้งาน → block (negative · ERR_DEFAULT_NOT_ACTIVE)
- group: Validation · ความสำคัญ: สูง · trace: AT-07 / BR-07 / ERR_DEFAULT_NOT_ACTIVE
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ชุดข้อมูล: NEG-DEFAULT (CR-1 valid + Default ON + สถานะ ร่าง)
- ผ่านเมื่อ: toast "ตั้งเป็นค่า Default ได้เฉพาะเงื่อนไขสถานะ "ใช้งาน""

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "DEFDRAFT" → รหัส · TYPE "ทดสอบดีฟอลต์" → ชื่อ TH · TYPE "30" → จำนวนวันเครดิต · CLICK checkbox "Purchase Order" | NEG-DEFAULT | ค่าครบ (valid) | ☐ |
| 2 | CLICK toggle "ตั้งเป็นค่า Default" | — | checkbox default ติ๊ก (กรอบแดง) | ☐ |
| 3 | SELECT "ร่าง" → dropdown "สถานะ" | NEG-DEFAULT | สถานะ = ร่าง | ☐ |
| 4 | CLICK "บันทึกและสร้าง" | — | drawer ไม่ปิด · WAIT toast error "**ตั้งเป็นค่า Default ได้เฉพาะเงื่อนไขสถานะ "ใช้งาน"**" | ☐ |

#### TC-V12 — discount_days ≥ net_days → block (negative · ERR_DISCOUNT_DAYS_INVALID)
- group: Validation · ความสำคัญ: กลาง · trace: AT-08 / BR-05 / ERR_DISCOUNT_DAYS_INVALID
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" (credit)
- ชุดข้อมูล: NEG-DISC-GE
- ผ่านเมื่อ: toast "วันชำระเพื่อรับส่วนลดต้องมากกว่า 0 และน้อยกว่าวันเครดิต"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "DISCGE" → รหัส · TYPE "ส่วนลดผิด" → ชื่อ TH | NEG-DISC-GE | ค่าครบ | ☐ |
| 2 | จำนวนวันเครดิต = 30 (default) · TYPE "2" → "ส่วนลดจ่ายเร็ว (%)" · TYPE "30" → "ภายในกี่วัน (Discount days)" | NEG-DISC-GE | discount_days=30 = net_days | ☐ |
| 3 | CLICK checkbox "Purchase Order" · CLICK "บันทึกและสร้าง" | — | drawer ไม่ปิด · WAIT toast error "**วันชำระเพื่อรับส่วนลดต้องมากกว่า 0 และน้อยกว่าวันเครดิต**" | ☐ |

#### TC-V13 — discount_days = 0 (มีส่วนลด) → block (negative)
- group: Validation · ความสำคัญ: กลาง · trace: AT-08 / BR-05 / ERR_DISCOUNT_DAYS_INVALID
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" (credit)
- ชุดข้อมูล: NEG-DISC-0
- ผ่านเมื่อ: toast เดียวกับ TC-V12

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "DISC0" → รหัส · TYPE "ส่วนลดศูนย์วัน" → ชื่อ TH · TYPE "2" → "ส่วนลดจ่ายเร็ว (%)" · TYPE "0" → "ภายในกี่วัน (Discount days)" | NEG-DISC-0 | ส่วนลด 2% / 0 วัน | ☐ |
| 2 | CLICK checkbox "Purchase Order" · CLICK "บันทึกและสร้าง" | — | drawer ไม่ปิด · WAIT toast error "วันชำระเพื่อรับส่วนลดต้องมากกว่า 0 และน้อยกว่าวันเครดิต" | ☐ |

#### TC-V14 — ยกเลิก create ด้วยปุ่ม "ยกเลิก" (dirty ไม่บันทึก)
- group: Validation · ความสำคัญ: ต่ำ · trace: P-02 interaction
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ผ่านเมื่อ: drawer ปิดโดยไม่สร้างแถวใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "TEMPX" → รหัส · TYPE "ชั่วคราว" → ชื่อ TH | — | ค่ากรอกแล้ว | ☐ |
| 2 | CLICK ปุ่ม "ยกเลิก" (มุมล่างซ้าย drawer) | — | drawer ปิด · badge หน้ายังเป็น "12 เงื่อนไข" · ไม่มีแถว TEMPX | ☐ |

#### TC-V15 — เปลี่ยนประเภทกลางคัน → field set reset (ไม่ค้างค่าเดิม)
- group: Validation · ความสำคัญ: กลาง · trace: FN-09 / onTypeChange
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ผ่านเมื่อ: เปลี่ยน credit→deposit → field เฉพาะประเภทเปลี่ยนตาม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกประเภท default credit · TYPE "50" → จำนวนวันเครดิต | — | ช่อง = 50 | ☐ |
| 2 | CLICK dropdown ประเภท → "มัดจำ + ส่วนเหลือ (Deposit)" | — | field เปลี่ยนเป็นชุด deposit (วิธีระบุมัดจำ/มูลค่ามัดจำ/…) · ไม่มีช่อง "จำนวนวันเครดิต" แบบเดิมค้าง | ☐ |
| 3 | CLICK dropdown ประเภท → "เครดิต N วัน (Credit)" | — | กลับเป็นชุด credit · "จำนวนวันเครดิต" = 30 (ค่า default ใหม่ ไม่ใช่ 50 ที่พิมพ์ไว้) | ☐ |

---

### GROUP D — Edit / View

#### TC-E01 — แก้ไข term ที่ used>0 ได้ (AT-09 · AD-01 · snapshot)
- group: Edit · ความสำคัญ: สูง · trace: AT-09 / BR-08 / AD-01 / EC-03
- actor (role): Finance Admin
- Setup: role=finance_admin · seed=t3 NET30 used=186 · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: แก้ไขบันทึกได้ + toast "บันทึกการแก้ไขแล้ว"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข (ไอคอนดินสอ) ท้ายแถว "NET30" | — | drawer เปิด หัวข้อ "**แก้ไขเงื่อนไขชำระเงิน**" · footer ปุ่ม "**บันทึกการแก้ไข**" · ฟอร์ม prefill (รหัส NET30, ชื่อ เครดิต 30 วัน) | ☐ |
| 2 | Clear "ชื่อเงื่อนไข (TH)" → TYPE "เครดิต 30 วัน (แก้ไข)" | — | ช่องแสดงค่าใหม่ | ☐ |
| 3 | Clear "จำนวนวันเครดิต" → TYPE "45" | — | ช่อง = 45 (แก้ได้แม้ used=186) | ☐ |
| 4 | CLICK "บันทึกการแก้ไข" | — | drawer ปิด · WAIT toast "**บันทึกการแก้ไขแล้ว**" (เขียว) | ☐ |
| 5 | VERIFY แถว NET30 | — | ชื่อเปลี่ยนเป็น "เครดิต 30 วัน (แก้ไข)" · สรุป "ครบกำหนด 45 วัน" · badge ยังเป็น 12 เงื่อนไข (ไม่เพิ่มแถว) | ☐ |

#### TC-E02 — แก้ไขผ่านปุ่ม "แก้ไข" ใน View drawer
- group: Edit · ความสำคัญ: กลาง · trace: AT-09 / P-04→P-03
- Setup: role=finance_admin · seed=t8 DEP30 · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: view→edit→save สำเร็จ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "DEP30" | — | View drawer เปิด | ☐ |
| 2 | CLICK ปุ่ม "แก้ไข" (หัว drawer) | — | drawer เปลี่ยนเป็นโหมดแก้ไข "แก้ไขเงื่อนไขชำระเงิน" prefill DEP30 | ☐ |
| 3 | Clear "ชื่อเงื่อนไข (EN)" → TYPE "30% Deposit Net 15 v2" · CLICK "บันทึกการแก้ไข" | — | toast "บันทึกการแก้ไขแล้ว" | ☐ |

#### TC-E03 — View drawer แสดงรายละเอียดครบต่อประเภท (installment)
- group: View · ความสำคัญ: กลาง · trace: P-04 / US-02
- Setup: role=finance_admin · seed=t9 INST3 (40/30/30) · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: view แสดงงวดครบ 3 บรรทัด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "INST3" | — | View drawer · การ์ด "สรุปเงื่อนไข" = "3 งวด (40% / 30% / 30%)" | ☐ |
| 2 | VERIFY section "รายละเอียดการคำนวณ" | — | มี 3 แถวงวด (งวด 1..3) แต่ละแถวแสดง % · มีแถว "นับจาก" + "WH/GRN/Ship trigger" | ☐ |

#### TC-E04 — View drawer ของ Credit แสดง trigger lock + due basis
- group: View · ความสำคัญ: กลาง · trace: P-04 / BR-10
- Setup: role=finance_admin · seed=t5 2-10N30 (credit+discount) · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "2-10N30" | — | View drawer · สรุป "ครบกำหนด 30 วัน · ลด 2% ถ้าจ่ายใน 10 วัน" | ☐ |
| 2 | VERIFY แถว trigger | — | "WH/GRN/Ship trigger" = "ทันที (หลัง PO/SO Confirm)" · แถว "ส่วนลดจ่ายเร็ว" = "2% ภายใน 10 วัน" | ☐ |

#### TC-E05 — Edit: เปลี่ยน type ของ term used>0 ได้ (EC-03)
- group: Edit · ความสำคัญ: กลาง · trace: EC-03 / AT-09 / AD-01
- Setup: role=finance_admin · seed=t2 POSTPAY used=6 · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: เปลี่ยนประเภทได้ + save สำเร็จ (no retro)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข (ดินสอ) แถว "POSTPAY" | — | edit drawer prefill (ประเภท "ชำระเต็มหลังรับ") | ☐ |
| 2 | CLICK dropdown ประเภท → "เครดิต N วัน (Credit)" | — | field เปลี่ยนเป็นชุด credit · จำนวนวันเครดิต = 30 | ☐ |
| 3 | CLICK "บันทึกการแก้ไข" | — | toast "บันทึกการแก้ไขแล้ว" · แถว POSTPAY เปลี่ยน pill ประเภทเป็น "เครดิต N วัน" | ☐ |

#### TC-E06 — Edit: ปิด drawer ด้วย backdrop / X (ไม่บันทึก)
- group: Edit · ความสำคัญ: ต่ำ · trace: overlay dismiss (§6 UI Brief)
- Setup: role=finance_admin · seed=t4 NET60 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข แถว "NET60" · Clear ชื่อ TH → TYPE "เปลี่ยนแต่ไม่เซฟ" | — | ค่าในช่องเปลี่ยน | ☐ |
| 2 | CLICK ปุ่ม X (มุมขวาบน drawer) | — | drawer ปิด | ☐ |
| 3 | VERIFY แถว NET60 | — | ชื่อยังเป็น "เครดิต 60 วัน" (ไม่ถูกบันทึก) | ☐ |

---

### GROUP E — Status change (single + bulk)

#### TC-S01 — เปลี่ยนสถานะเดี่ยวผ่านเมนู View (AT-10)
- group: Status · ความสำคัญ: สูง · trace: AT-10 / US-06 / §5.2
- Setup: role=finance_admin · seed=t12 NET45 status=ร่าง · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: toast "เปลี่ยนสถานะเป็น ใช้งาน แล้ว" + pill เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "NET45" | — | View drawer เปิด (สถานะปัจจุบัน = ร่าง) | ☐ |
| 2 | CLICK ปุ่ม "เปลี่ยนสถานะ" (หัว drawer) | — | เมนูเปิด 3 รายการ (ร่าง/ใช้งาน/ไม่ใช้งาน) · "**ร่าง**" ถูก disable (ค่าปัจจุบัน) | ☐ |
| 3 | CLICK "ใช้งาน" | — | WAIT toast "**เปลี่ยนสถานะเป็น ใช้งาน แล้ว**" (เขียว) | ☐ |
| 4 | CLICK "ปิด" → VERIFY List | — | แถว NET45 pill สถานะ = "ใช้งาน" (เขียว) · การ์ด stat "ใช้งาน" = 11 · "ร่าง" = 0 | ☐ |

#### TC-S02 — เมนูเปลี่ยนสถานะ: ค่าปัจจุบัน disabled (AT-10 guard)
- group: Status · ความสำคัญ: กลาง · trace: AT-10 / §5.2 (current disabled)
- Setup: role=finance_admin · seed=t1 PREPAY status=ใช้งาน · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "PREPAY" → CLICK "เปลี่ยนสถานะ" | — | เมนูเปิด · "**ใช้งาน**" ถูก disable (จาง กดไม่ได้) · "ร่าง"/"ไม่ใช้งาน" กดได้ | ☐ |
| 2 | CLICK "ไม่ใช้งาน" | — | toast "เปลี่ยนสถานะเป็น ไม่ใช้งาน แล้ว" | ☐ |

#### TC-S03 — bulk เปลี่ยนสถานะหลายรายการ (AT-11)
- group: Status · ความสำคัญ: สูง · trace: AT-11 / US-06
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: toast "เปลี่ยนสถานะ 2 รายการเป็น ไม่ใช้งาน แล้ว"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว "PREPAY" · CLICK checkbox แถว "POSTPAY" | — | แถบ bulk ขาวโผล่ "เลือก **2** รายการ" มีปุ่ม ใช้งาน/ไม่ใช้งาน/ร่าง/ลบ/ยกเลิก | ☐ |
| 2 | CLICK ปุ่ม "ไม่ใช้งาน" (ในแถบ bulk) | — | WAIT toast "**เปลี่ยนสถานะ 2 รายการเป็น ไม่ใช้งาน แล้ว**" · แถบ bulk หาย | ☐ |
| 3 | VERIFY | — | แถว PREPAY, POSTPAY pill สถานะ = "ไม่ใช้งาน" (amber) · stat "ไม่ใช้งาน" = 3 | ☐ |

#### TC-S04 — bulk เปลี่ยนเป็น "ร่าง"
- group: Status · ความสำคัญ: กลาง · trace: AT-11
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว "EOM30" · CLICK ปุ่ม "ร่าง" (แถบ bulk) | — | toast "เปลี่ยนสถานะ 1 รายการเป็น ร่าง แล้ว" · EOM30 pill = "ร่าง" | ☐ |

#### TC-S05 — ยกเลิกการเลือก bulk (clear selection)
- group: Status · ความสำคัญ: ต่ำ · trace: bulk selection
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox 2 แถว · CLICK ปุ่ม "ยกเลิก" (แถบ bulk) | — | แถบ bulk หาย · ไม่มีแถวถูกติ๊ก (ไม่มีพื้นชมพู) | ☐ |

---

### GROUP F — Bulk delete + guard used>0

#### TC-D01 — bulk ลบ: มีทั้ง used>0 และ used=0 → ข้ามตัว used>0 (AT-12 · BR-08)
- group: Delete · ความสำคัญ: สูง · trace: AT-12 / BR-08 / CD-02
- actor (role): Finance Admin
- Setup: role=finance_admin · seed=t3 NET30 used=186 + t12 NET45 used=0 · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: NET45 ถูกลบ · NET30 ถูกข้าม · toast info "ลบแล้ว 1 รายการ · ข้าม 1 รายการที่ถูกใช้งาน"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว "NET30" · CLICK checkbox แถว "NET45" | — | แถบ bulk "เลือก 2 รายการ" | ☐ |
| 2 | CLICK ปุ่ม "ลบ" (แดง, แถบ bulk) | — | modal เปิด หัวข้อ "**ลบเงื่อนไขชำระเงิน**" · subtitle "เลือกไว้ 2 รายการ · **1 รายการถูกใช้งานอยู่จะถูกข้าม**" · ปุ่ม "**ลบ 1 รายการ**" | ☐ |
| 3 | VERIFY body modal | — | ข้อความ "ยืนยันการลบออกจากทะเบียน — รายการที่ถูกใช้ในเอกสารแล้วจะไม่ถูกลบ" | ☐ |
| 4 | CLICK ปุ่ม "ลบ 1 รายการ" | — | modal ปิด · WAIT toast info "**ลบแล้ว 1 รายการ · ข้าม 1 รายการที่ถูกใช้งาน**" | ☐ |
| 5 | VERIFY List | — | แถว **NET45 หายไป** · แถว **NET30 ยังอยู่** · badge "11 เงื่อนไข" | ☐ |

#### TC-D02 — bulk ลบ: เฉพาะ used=0 → ลบสำเร็จ (success)
- group: Delete · ความสำคัญ: สูง · trace: AT-12 / BR-08
- Setup: role=finance_admin · seed=t4 NET60 used=0 (inactive) · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: toast success "ลบแล้ว 1 รายการ" (ไม่มีข้อความข้าม)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว "NET60" · CLICK ปุ่ม "ลบ" (แถบ bulk) | — | modal · subtitle "เลือกไว้ 1 รายการ" (**ไม่มี** ข้อความ "ถูกใช้งานอยู่จะถูกข้าม") · ปุ่ม "ลบ 1 รายการ" (กดได้) | ☐ |
| 2 | CLICK "ลบ 1 รายการ" | — | modal ปิด · WAIT toast success "**ลบแล้ว 1 รายการ**" (ไม่มี "ข้าม") · badge "11 เงื่อนไข" · ไม่มีแถว NET60 | ☐ |

#### TC-D03 — bulk ลบ: เฉพาะ used>0 → ปุ่มลบ disabled (cannot delete used>0)
- group: Delete · ความสำคัญ: สูง · trace: AT-12 / BR-08 (guard)
- Setup: role=finance_admin · seed=t3 NET30 used=186 · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: ปุ่ม "ลบ 0 รายการ" ถูก disable → ลบไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว "NET30" (used=186) · CLICK ปุ่ม "ลบ" (แถบ bulk) | — | modal · subtitle "เลือกไว้ 1 รายการ · **1 รายการถูกใช้งานอยู่จะถูกข้าม**" · ปุ่ม "**ลบ 0 รายการ**" **disabled** (กดไม่ได้) | ☐ |
| 2 | CLICK "ยกเลิก" | — | modal ปิด · NET30 ยังอยู่ครบ · badge "12 เงื่อนไข" | ☐ |

#### TC-D04 — ปิด modal ลบด้วย Esc / backdrop (ไม่ลบ)
- group: Delete · ความสำคัญ: ต่ำ · trace: overlay dismiss / Esc chain
- Setup: role=finance_admin · seed=t12 NET45 used=0 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox "NET45" · CLICK ปุ่ม "ลบ" | — | modal เปิด | ☐ |
| 2 | PRESS Esc | — | modal ปิด · NET45 ยังอยู่ · แถว NET45 ยังถูกติ๊ก (selection ค้าง) | ☐ |

#### TC-D05 — bulk ลบหลายตัว used=0 พร้อมกัน
- group: Delete · ความสำคัญ: กลาง · trace: AT-12
- Setup: role=finance_admin · seed=t4 NET60 used=0 + t12 NET45 used=0 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กรอง stat: CLICK "ทั้งหมด" · CLICK checkbox NET60 + checkbox NET45 | — | "เลือก 2 รายการ" | ☐ |
| 2 | CLICK "ลบ" → modal subtitle "เลือกไว้ 2 รายการ" ปุ่ม "ลบ 2 รายการ" → CLICK "ลบ 2 รายการ" | — | toast success "ลบแล้ว 2 รายการ" · badge "10 เงื่อนไข" | ☐ |

---

### GROUP G — Default toggle

#### TC-DF01 — ตั้ง Default term ใหม่ (active) → ตัวเก่าประเภทเดียวกันหลุด default (AT-07)
- group: Default · ความสำคัญ: สูง · trace: AT-07 / BR-07 / US-04
- Setup: role=finance_admin · seed=t3 NET30 = credit default ⭐ · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ผ่านเมื่อ: สร้าง credit ใหม่เป็น default → NET30 หมดดาว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มเงื่อนไข" (credit) · TYPE "NETDEF" → รหัส · TYPE "เครดิตดีฟอลต์ใหม่" → ชื่อ TH · TYPE "30" → วันเครดิต · CLICK checkbox "Purchase Order" | — | ค่าครบ | ☐ |
| 2 | CLICK toggle "ตั้งเป็นค่า Default" (สถานะ default ใช้งาน) | — | checkbox default ติ๊ก | ☐ |
| 3 | CLICK "บันทึกและสร้าง" | — | toast "สร้างเงื่อนไขชำระเงินแล้ว" | ☐ |
| 4 | VERIFY List | — | แถว NETDEF มี **⭐** · แถว NET30 **ไม่มีดาวแล้ว** (หลุด default อัตโนมัติ) | ☐ |

#### TC-DF02 — Default ผูกต่อประเภท (คนละประเภทมี default ของตัวเอง)
- group: Default · ความสำคัญ: กลาง · trace: BR-07 (1/type)
- Setup: role=finance_admin · seed=t3 NET30 credit default · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ผ่านเมื่อ: สร้าง deposit default → NET30 (credit) ยังคงดาว (คนละประเภท)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกประเภท "มัดจำ + ส่วนเหลือ (Deposit)" · TYPE "DEPDEF" → รหัส · TYPE "มัดจำดีฟอลต์" → ชื่อ TH · CLICK checkbox "Sales Order" · CLICK toggle "ตั้งเป็นค่า Default" | — | ค่าครบ + default ติ๊ก | ☐ |
| 2 | CLICK "บันทึกและสร้าง" | — | toast success | ☐ |
| 3 | VERIFY | — | แถว DEPDEF มี ⭐ · แถว NET30 **ยังมี ⭐** (default credit ไม่กระทบ default deposit) | ☐ |

#### TC-DF03 — ยกเลิก Default (toggle off) แล้วบันทึก
- group: Default · ความสำคัญ: กลาง · trace: BR-07 / toggle
- Setup: role=finance_admin · seed=t3 NET30 default · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข แถว "NET30" | — | edit drawer · toggle "ตั้งเป็นค่า Default" ติ๊กอยู่ | ☐ |
| 2 | CLICK toggle "ตั้งเป็นค่า Default" (ปิด) · CLICK "บันทึกการแก้ไข" | — | toast "บันทึกการแก้ไขแล้ว" · แถว NET30 **ไม่มีดาว** | ☐ |

#### TC-DF04 — Default ถูก block เมื่อ edit เป็นสถานะ ≠ ใช้งาน (BR-07)
- group: Default · ความสำคัญ: กลาง · trace: BR-07 / ERR_DEFAULT_NOT_ACTIVE
- Setup: role=finance_admin · seed=t3 NET30 (active, default) · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข "NET30" · SELECT "ร่าง" → dropdown สถานะ (default toggle ยัง on) | — | สถานะ ร่าง + default on | ☐ |
| 2 | CLICK "บันทึกการแก้ไข" | — | drawer ไม่ปิด · toast error "ตั้งเป็นค่า Default ได้เฉพาะเงื่อนไขสถานะ "ใช้งาน"" | ☐ |

---

### GROUP H — Edge / interaction

#### TC-EC01 — Scroll preservation: interaction ในฟอร์มไม่เด้งขึ้นบน (Iron Rule #29)
- group: Edge · ความสำคัญ: สูง · trace: Iron Rule #29 / 01_UI §1.0
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" → ประเภท "มัดจำ + ส่วนเหลือ (Deposit)" (ฟอร์มยาว)
- ผ่านเมื่อ: toggle use_in ระหว่าง scroll ล่าง → drawer อยู่ตำแหน่งเดิม ไม่กระโดดขึ้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกประเภท "มัดจำ + ส่วนเหลือ (Deposit)" · Scroll เนื้อ drawer ลงจนเห็น section "การใช้งานในเอกสาร" | — | เห็น checkbox 7 เอกสาร | ☐ |
| 2 | CLICK checkbox "Sales Order" | — | checkbox ติ๊ก · **drawer ยังอยู่ที่ section use_in (ไม่เด้งขึ้นหัวฟอร์ม)** | ☐ |
| 3 | CLICK dropdown "ชำระส่วนที่เหลือ (remaining)" → เลือกค่าใด → VERIFY ตำแหน่ง scroll | — | หลังเลือก drawer ยังคง scroll ตำแหน่งเดิม (ไม่กระโดด) | ☐ |

#### TC-EC02 — Esc chain: sdd → drawer (ปิดทีละชั้น)
- group: Edge · ความสำคัญ: สูง · trace: Esc chain (§7.1 UI Brief)
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ผ่านเมื่อ: Esc ปิด dropdown ก่อน แล้ว Esc ปิด drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dropdown "ประเภทเงื่อนไข" (เปิด panel) | — | panel เปิด | ☐ |
| 2 | PRESS Esc | — | **panel ปิด** แต่ **drawer ยังเปิดอยู่** | ☐ |
| 3 | PRESS Esc | — | **drawer ปิด** กลับหน้า List | ☐ |

#### TC-EC02b — Esc chain: modal → drawer (modal บนสุดปิดก่อน)
- group: Edge · ความสำคัญ: กลาง · trace: Esc chain
- Setup: role=finance_admin · seed=t12 NET45 used=0 · files=—
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox "NET45" · CLICK "ลบ" (แถบ bulk) | — | modal เปิด | ☐ |
| 2 | PRESS Esc | — | modal ปิด (กลับหน้า List, ไม่ลบ) | ☐ |

#### TC-EC03 — Installment: live total badge อัปเดตทันที
- group: Edge · ความสำคัญ: กลาง · trace: BR-04 / ENG-PT-01 / onInstPct
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" → ประเภท "แบ่งงวด (Installment)"
- ผ่านเมื่อ: เปลี่ยน % แล้ว badge เปลี่ยนตัวเลข/สีทันที

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกประเภท "แบ่งงวด (Installment)" | — | badge "รวม 100% ✓" (เขียว is-ok) | ☐ |
| 2 | Clear % "งวด 1" → TYPE "40" | — | badge live เปลี่ยนเป็น "รวม **90%** (ต้องเป็น 100%)" (เหลือง is-warn) | ☐ |
| 3 | Clear % "งวด 2" → TYPE "60" | — | badge live เปลี่ยนเป็น "รวม **100%** ✓" (เขียว) | ☐ |

#### TC-EC04 — Installment: เพิ่มงวด/ลบงวด (add/remove rows)
- group: Edge · ความสำคัญ: กลาง · trace: BR-04 / addInst/removeInst
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" → ประเภท "แบ่งงวด (Installment)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือกประเภท "แบ่งงวด (Installment)" | — | 2 งวด | ☐ |
| 2 | CLICK "เพิ่มงวด" ×2 | — | มี 4 งวด (งวด 1..4) | ☐ |
| 3 | CLICK ปุ่มลบ (ถังขยะ) งวด 4 · งวด 3 | — | เหลือ 2 งวด · ปุ่มลบ disabled ทั้งคู่ | ☐ |

#### TC-EC05 — ลบ Default term (used=0) → ประเภทนั้นไม่มี default (EC-06)
- group: Edge · ความสำคัญ: กลาง · trace: EC-06 / BR-07
- Setup: role=finance_admin · seed=สร้าง credit default ใหม่ (used=0) ก่อน · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: หลังลบ default (used=0) → สร้าง credit ใหม่ไม่ auto-default

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มเงื่อนไข" · TYPE "TMPDEF" → รหัส · TYPE "ดีฟอลต์ชั่วคราว" → ชื่อ · TYPE "30" → วันเครดิต · CLICK checkbox "PO" · CLICK toggle Default · CLICK "บันทึกและสร้าง" | — | TMPDEF สร้าง (⭐) · NET30 หลุด default | ☐ |
| 2 | CLICK checkbox แถว "TMPDEF" (used=0) · CLICK "ลบ" → "ลบ 1 รายการ" | — | toast "ลบแล้ว 1 รายการ" · TMPDEF หาย | ☐ |
| 3 | VERIFY | — | ไม่มี term credit ใดมี ⭐ (ประเภท credit ไม่มี default) — ยอมรับได้ตาม EC-06 | ☐ |

#### TC-EC06 — Installment days=0 หลายงวด → ยอมรับได้ (EC-11, accepted)
- group: Edge · ความสำคัญ: ต่ำ · trace: EC-11 (accepted, no block)
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" → ประเภท "แบ่งงวด (Installment)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก installment · ตั้ง 2 งวด 50/50 (days ปล่อยเป็น 0 ทั้งคู่) · TYPE "INST00" → รหัส · TYPE "งวดวันชนกัน" → ชื่อ · CLICK checkbox "PO" | — | badge "รวม 100% ✓" | ☐ |
| 2 | CLICK "บันทึกและสร้าง" | — | บันทึกได้ (ไม่ block) · toast "สร้างเงื่อนไขชำระเงินแล้ว" | ☐ |

#### TC-EC07 — แก้ไข term used>0 → master อัปเดต (snapshot ปลายทางไม่กระทบ — AD-01)
- group: Edge · ความสำคัญ: กลาง · trace: AT-09 / EC-03 / AD-01
- Setup: role=finance_admin · seed=t7 DEP50 used=42 · files=— · หมายเหตุ: snapshot ฝั่งเอกสารปลายทางตรวจได้เฉพาะ downstream (ดู TC-XT01)
- Start: OPEN `#/finance/payment-term`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข "DEP50" · Clear "มูลค่ามัดจำ" → TYPE "55" | — | ค่าเปลี่ยน (used=42 ไม่บล็อกการแก้) | ☐ |
| 2 | CLICK "บันทึกการแก้ไข" | — | toast "บันทึกการแก้ไขแล้ว" · แถว DEP50 สรุปมัดจำเปลี่ยนเป็น 55% | ☐ |

#### TC-EC08 — Deposit สลับ method percent→manual→percent (ช่อง value ซ่อน/โผล่)
- group: Edge · ความสำคัญ: ต่ำ · trace: EC-09 / onDepMethodPick
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" → ประเภท "มัดจำ + ส่วนเหลือ (Deposit)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก deposit → VERIFY มีช่อง "มูลค่ามัดจำ" (percent) | — | ช่องปรากฏ suffix "%" | ☐ |
| 2 | CLICK dropdown "วิธีระบุมัดจำ" → "จำนวนเงินคงที่ (฿)" | — | ช่อง "มูลค่ามัดจำ" ยังอยู่ · suffix เปลี่ยนเป็น "บาท" | ☐ |
| 3 | CLICK dropdown "วิธีระบุมัดจำ" → "กำหนดเองตอนสร้างเอกสาร" | — | ช่อง "มูลค่ามัดจำ" **หายไป** | ☐ |

#### TC-EC09 — Responsive ≤1180: hamburger + sidebar off-canvas
- group: Edge · ความสำคัญ: กลาง · trace: Iron Rule #97 / responsive · **(ต้อง simulate viewport)**
- Setup: role=finance_admin · seed=seed 12 · files=— · **ตั้ง viewport กว้าง ≤1180px**
- Start: OPEN `#/finance/payment-term` (viewport width = 1100px)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ตั้ง viewport กว้าง 1100px · VERIFY shell bar | — | ปุ่ม hamburger (ไอคอน ☰ เมนู) ปรากฏซ้ายบน · sidebar ถูกซ่อน (off-canvas) | ☐ |
| 2 | CLICK ปุ่ม hamburger | — | sidebar เลื่อนเข้าจากซ้าย + ฉากหลังมืดลง | ☐ |
| 3 | PRESS Esc | — | sidebar ปิด (off-canvas อีกครั้ง) | ☐ |

---

### GROUP I — Scope-Lock verify (MUST-NOT-exist)

#### TC-SL01 — ไม่มี CSV import/export ที่ใดในระบบ (BR-09 / AT-14)
- group: ScopeLock · ความสำคัญ: สูง · trace: AT-14 / BR-09 / VD-PDM
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: ไม่พบปุ่ม/เมนู import/export/CSV ทั้ง toolbar และ drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY toolbar เหนือตาราง | — | มีเพียงปุ่ม "เพิ่มเงื่อนไข" · **ไม่มี** ปุ่ม "นำเข้า"/"ส่งออก"/"Import"/"Export"/"CSV" | ☐ |
| 2 | CLICK "เพิ่มเงื่อนไข" · VERIFY drawer | — | ในฟอร์มไม่มีตัวเลือกอัปโหลด/นำเข้าไฟล์ใด ๆ | ☐ |

#### TC-SL02 — use_in = 7 เอกสาร · **ไม่มี PR** (LD-01 / D-08 / BR-06)
- group: ScopeLock · ความสำคัญ: สูง · trace: AT-06 / BR-06 / LD-01 / LD-F-01
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ผ่านเมื่อ: section use_in มี 7 เอกสารพอดี · ไม่มี "ใบขอซื้อ (PR)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มเงื่อนไข" · Scroll ไป section "การใช้งานในเอกสาร" | — | 2 กลุ่ม: "ฝั่งซื้อ (P2P)" = Purchase Order, AP Invoice, Payment Voucher · "ฝั่งขาย (S2C)" = Sales Order, Quotation, AR Invoice, Receipt = **รวม 7** | ☐ |
| 2 | VERIFY ไม่มี PR | — | **ไม่มี** checkbox "ใบขอซื้อ" / "PR" / "Purchase Requisition" ในทั้ง 2 กลุ่ม | ☐ |
| 3 | เลือกประเภท "Direct Payment (จ่ายตรง)" · VERIFY | — | Purchase Order / Quotation / Sales Order เป็นสีจาง ป้าย "ไม่รองรับ" (ยังคง 7 เอกสาร, ไม่มี PR) | ☐ |

#### TC-SL03 — Credit trigger LOCKED (แก้ไม่ได้ · LD-08b / BR-10)
- group: ScopeLock · ความสำคัญ: สูง · trace: AT-15 / BR-10 / LD-08b
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" (credit)
- ผ่านเมื่อ: credit แสดง lock badge · ไม่มี dropdown ให้แก้ trigger

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มเงื่อนไข" (ประเภท default credit) · VERIFY trigger | — | เห็น badge (มีไอคอนกุญแจ) "Warehouse/GRN trigger: **ทันที (หลัง PO/SO Confirm)** (ล็อกตามประเภท)" | ☐ |
| 2 | VERIFY ไม่มี dropdown | — | **ไม่มี** dropdown/ช่องแก้ trigger สำหรับ credit (ต่างจาก prepay/postpay/deposit ที่มี dropdown) | ☐ |
| 3 | เปรียบเทียบ: CLICK dropdown ประเภท → "ชำระเต็มหลังรับ (Full Postpay)" | — | postpay มี dropdown "Warehouse / GRN / Ship Trigger" (แก้ได้) — ยืนยันว่า lock เป็นเฉพาะ credit | ☐ |

#### TC-SL04 — ไม่มีปุ่มลบเดี่ยวในแถว (VD-PDM / CD-02)
- group: ScopeLock · ความสำคัญ: สูง · trace: VD-PDM / CD-02
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: คอลัมน์ "จัดการ" มีเฉพาะปุ่มแก้ไข (ดินสอ) — ไม่มีถังขยะ/ลบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คอลัมน์ "จัดการ" ของทุกแถว | — | มีเพียงปุ่มแก้ไข (ไอคอนดินสอ) · **ไม่มี** ปุ่มลบ/ถังขยะรายแถว (ลบทำได้ผ่าน bulk เท่านั้น) | ☐ |

#### TC-SL05 — ไม่มี approval UI (DOA null / no-approval)
- group: ScopeLock · ความสำคัญ: สูง · trace: Governance DOA null / §0.4
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: ไม่มีปุ่ม "ส่งอนุมัติ"/"อนุมัติ"/ช่อง approver ที่ใด · status commit ทันที

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มเงื่อนไข" · VERIFY ฟอร์ม | — | **ไม่มี** ช่อง/ปุ่ม "ผู้อนุมัติ"/"ส่งอนุมัติ"/"สายอนุมัติ" · footer มีแค่ "ยกเลิก" + "บันทึกและสร้าง" | ☐ |
| 2 | CLICK แถวใด → View · VERIFY เมนู "เปลี่ยนสถานะ" | — | เปลี่ยนสถานะได้ทันที (ไม่มีขั้นรออนุมัติ) — 3 ค่าอิสระ | ☐ |

#### TC-SL06 — ไม่มี field สกุลเงิน (multi-currency · AD-03)
- group: ScopeLock · ความสำคัญ: กลาง · trace: AD-03 / LD-F-06
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สำรวจทุก section ในฟอร์ม create (ทุกประเภท) | — | **ไม่มี** ช่อง "สกุลเงิน"/"Currency"/dropdown เงินตรา · deposit fixed แสดงหน่วย "บาท" ตายตัว (THB สมมติ) | ☐ |

#### TC-SL07 — ไม่มี hint/field-help ใต้ช่อง (VD-PDM-04)
- group: ScopeLock · ความสำคัญ: ต่ำ · trace: VD-PDM (ตัด hint/field-help)
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ใต้ช่อง "รหัส (Code)" และช่องอื่น | — | ไม่มีข้อความ help สีเทาใต้ช่อง (แม้ label จะมีคำว่า "ตัวพิมพ์ใหญ่ ไม่ซ้ำ" ใน spec แต่ถูกตัดไม่แสดง) — แสดงเฉพาะ label + input | ☐ |

#### TC-SL08 — ไม่มีตัวเลือกส่วนลด > 1 ช่วง (AD-02 / LD-F-05)
- group: ScopeLock · ความสำคัญ: กลาง · trace: AD-02 / BR-05 (1 tier)
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" (credit)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ส่วนลดจ่ายเร็ว | — | มีเพียง **1 คู่**: "ส่วนลดจ่ายเร็ว (%)" + "ภายในกี่วัน (Discount days)" · **ไม่มี** ปุ่ม "เพิ่มช่วงส่วนลด"/tier ที่ 2 | ☐ |

---

### GROUP J — [AI-DEFAULT] propagation

> เคสกลุ่มนี้ verify ค่า default ที่ **AI ตัดสินแทน BA** (Lane Mode). ถ้า fail อาจแปลว่า "default ผิด" ไม่ใช่ "โค้ดผิด".

#### TC-AD01 — [AI-DEFAULT AD-01] used>0 แก้ได้ / ลบไม่ได้
- group: AI-Default · ความสำคัญ: สูง · trace: `[AI-DEFAULT]` AD-01 / BR-08 / AT-09
- Setup: role=finance_admin · seed=t3 NET30 used=186 · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: แก้ได้ (toast บันทึกแก้ไข) แต่ลบไม่ได้ (ปุ่มลบ 0 รายการ disabled)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข "NET30" · Clear ชื่อ EN → TYPE "Net 30 edited" · CLICK "บันทึกการแก้ไข" | — | toast "บันทึกการแก้ไขแล้ว" (แก้ได้แม้ used=186) | ☐ |
| 2 | CLICK checkbox "NET30" · CLICK "ลบ" | — | modal · ปุ่ม "ลบ 0 รายการ" **disabled** (ลบไม่ได้เพราะ used>0) | ☐ |
| 3 | CLICK "ยกเลิก" | — | NET30 ยังอยู่ | ☐ |

#### TC-AD02 — [AI-DEFAULT AD-02] ส่วนลดจ่ายเร็ว = 1 ช่วงเท่านั้น
- group: AI-Default · ความสำคัญ: กลาง · trace: `[AI-DEFAULT]` AD-02 / BR-05 / LD-F-05
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" (credit)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ฟอร์ม credit | — | ส่วนลดมีคู่เดียว (%,วัน) · ไม่มีทางเพิ่ม tier ที่ 2 (default AI = 1 ช่วง) | ☐ |

#### TC-AD03 — [AI-DEFAULT AD-03] ไม่รองรับ multi-currency (THB)
- group: AI-Default · ความสำคัญ: กลาง · trace: `[AI-DEFAULT]` AD-03 / LD-F-06
- Setup: role=finance_admin · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข" → ประเภท "มัดจำ + ส่วนเหลือ (Deposit)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dropdown "วิธีระบุมัดจำ" → "จำนวนเงินคงที่ (฿)" · VERIFY | — | หน่วยเงินตายตัว "บาท" · ไม่มี dropdown เลือกสกุลเงิน (default AI = THB) | ☐ |

---

### GROUP K — Cross-Module (XT — ต้อง simulate downstream)

> Prototype ไม่มีหน้าโมดูลปลายทาง (PO/SO/AP/AR/Warehouse/Tax) — เคสกลุ่มนี้ **ต้อง simulate**: runner เตรียม seed ปลายทาง
> หรือ verify ผ่าน API/event. ถ้าทำ downstream จริงไม่ได้ → mark BLOCKED พร้อม evidence.

#### TC-XT01 — PO เลือก active term → snapshot code+config (XT-01 · ต้อง simulate)
- group: Cross-Module · ความสำคัญ: กลาง · trace: XT-01 / Central Plan snapshot
- Setup: role=finance_admin + consumer · seed=t3 NET30 active + โมดูล PO (simulate) · files=—
- Start: (downstream) สร้าง PO ที่อ้าง term NET30
- ผ่านเมื่อ: PO เก็บ snapshot code+config · แก้ master ภายหลัง PO ไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) สร้าง PO เลือก term "NET30" → VERIFY+บันทึก snapshot บน PO (code=NET30, net_days=30) | — | จด snapshot ค่าไว้ (อ้างใน step ถัดไป) | ☐ |
| 2 | (F-PAY) แก้ master NET30 net_days 30→45 · บันทึก | — | toast "บันทึกการแก้ไขแล้ว" | ☐ |
| 3 | (simulate) เปิด PO เดิม → VERIFY snapshot | — | PO ยังแสดง net_days=30 (snapshot ไม่เปลี่ยนตาม master) — เทียบกับค่าที่จดใน step 1 | ☐ |

#### TC-XT02 — master → inactive → ไม่โผล่ใน picker ใหม่ (XT-02 · ต้อง simulate)
- group: Cross-Module · ความสำคัญ: กลาง · trace: XT-02 / EC-05 / BR-10
- Setup: role=finance_admin + consumer · seed=t5 2-10N30 active · files=—
- Start: OPEN `#/finance/payment-term`
- ผ่านเมื่อ: set inactive → picker GET /active ไม่คืน term นี้ · เอกสารเก่ายังใช้ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (F-PAY) CLICK "2-10N30" → "เปลี่ยนสถานะ" → "ไม่ใช้งาน" | — | toast "เปลี่ยนสถานะเป็น ไม่ใช้งาน แล้ว" · pill = ไม่ใช้งาน | ☐ |
| 2 | (simulate) เปิด picker term ใน PO ใหม่ (GET /active) | — | รายการ **ไม่มี** 2-10N30 (คืนเฉพาะ active) | ☐ |
| 3 | (simulate) เปิดเอกสารเก่าที่เคยอ้าง 2-10N30 | — | snapshot เดิมยังแสดง/ใช้ได้ (EC-05) | ☐ |

#### TC-XT03 — installment ใช้ที่ AP/AR → journal split ต่องวด (XT-03 · ต้อง simulate)
- group: Cross-Module · ความสำคัญ: กลาง · trace: XT-03 / ENG-PT-01
- Setup: role=consumer · seed=t9 INST3 (40/30/30) + โมดูล AP/AR + ENG-PT-01 (simulate) · files=—
- Start: (downstream) สร้าง AP Invoice อ้าง INST3
- ผ่านเมื่อ: ระบบแตก journal/aging ต่องวด (3 งวด)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) สร้าง AP Invoice เลือก term INST3 | — | เกิด schedule 3 งวด (40/30/30) — aging แยกต่องวด (ENG-PT-01) | ☐ |

#### TC-XT04 — deposit รับมัดจำ → ใบกำกับภาษี ณ จุดรับเงิน (XT-04 · ต้อง simulate · OQ-PAY-04 OPEN)
- group: Cross-Module · ความสำคัญ: ต่ำ · trace: XT-04 / EC-07 / Hook-2 (Tax Code)
- Setup: role=consumer · seed=t7 DEP50 + Tax Code + GL (simulate) · files=— · **หมายเหตุ: OQ-PAY-04 ยังเปิด — spec deposit GL ยังไม่ปิด**
- Start: (downstream) รับมัดจำจากเอกสารที่อ้าง DEP50
- ผ่านเมื่อ: ออกใบกำกับภาษี ณ จุดรับเงิน (pending spec)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) รับมัดจำ 50% (DEP50) | — | Hook-2 ออกใบกำกับภาษี ณ จุดรับเงิน (เชื่อม Tax Code) — **BLOCKED ถ้า OQ-PAY-04 ยังไม่ปิด** | ☐ |

#### TC-XT05 — trigger resolver คลังตามประเภท (XT-05 · ต้อง simulate)
- group: Cross-Module · ความสำคัญ: ต่ำ · trace: XT-05 / ENG-PT-02 / BR-10,11
- Setup: role=consumer · seed=t1 PREPAY(after_full) + t7 DEP50(after_deposit) + t3 NET30(immediate) + Warehouse (simulate) · files=—
- Start: (downstream) สร้างเอกสาร P2P/S2C แต่ละประเภท
- ผ่านเมื่อ: unlock คลังตาม trigger: prepay=after_full, deposit=after_deposit, credit=immediate(locked)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) PO อ้าง NET30 (credit) confirm | — | Warehouse unlock **ทันที** (immediate, locked) | ☐ |
| 2 | (simulate) PO อ้าง PREPAY confirm | — | Warehouse unlock **หลังชำระเต็ม** (after_full) | ☐ |
| 3 | (simulate) PO อ้าง DEP50 confirm | — | Warehouse unlock **หลังชำระมัดจำ** (after_deposit) | ☐ |

#### TC-XT06 — Central Plan [config] edges: PO/AR/AP อ้าง term ผ่าน use_in (XT-06 · ต้อง simulate)
- group: Cross-Module · ความสำคัญ: ต่ำ · trace: XT-06 / use_in representable
- Setup: role=consumer · seed=term ที่ use_in ครอบ po/ap_invoice/ar_invoice · files=—
- Start: (downstream)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) เปิด picker term ที่ PO, AP Invoice, AR Invoice | — | ทั้ง 3 เอกสารเห็น/อ้าง term ผ่าน use_in ได้ (representable) | ☐ |

---

### GROUP L — Permission

#### TC-PM01 — Finance Viewer: ดูได้ แต่ create/edit/bulk ถูกปฏิเสธ (AT-19 · ต้อง simulate role)
- group: Permission · ความสำคัญ: กลาง · trace: AT-19 / §5.3 / ERR_INSUFFICIENT_ROLE
- Setup: role=**finance_viewer** (ต้อง login เป็น viewer — prototype default = Finance Lead/Admin ต้อง simulate) · seed=seed 12 · files=—
- Start: OPEN `#/finance/payment-term` (as viewer)
- ผ่านเมื่อ: ไม่มีปุ่ม create/edit/bulk · เรียก mutation ตรง → 403 ERR_INSUFFICIENT_ROLE

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หน้า List (as viewer) | — | เห็นตาราง+ค้นหาได้ · **ไม่มี** ปุ่ม "เพิ่มเงื่อนไข" · **ไม่มี** ปุ่มแก้ไข (ดินสอ)/checkbox bulk | ☐ |
| 2 | (simulate API) เรียก POST /payment-terms ตรงในฐานะ viewer | — | ตอบ **403 ERR_INSUFFICIENT_ROLE** | ☐ |

#### TC-PM02 — Consumer: เข้าถึงผ่าน picker active-only เท่านั้น (AT-19 · ต้อง simulate)
- group: Permission · ความสำคัญ: ต่ำ · trace: AT-19 / §5.3 (Consumer)
- Setup: role=**consumer** (downstream) · seed=seed 12 · files=—
- Start: (downstream) picker
- ผ่านเมื่อ: consumer เห็นเฉพาะ active ผ่าน picker · เรียก mutation → 403

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) consumer เปิด picker GET /active | — | คืนเฉพาะ term active (read-only) | ☐ |
| 2 | (simulate) consumer เรียก PUT /payment-terms/:id ตรง | — | **403 ERR_INSUFFICIENT_ROLE** | ☐ |

---

### GROUP M — Concurrency / Idempotency (ต้อง simulate — API level)

#### TC-CC01 — 2 admin ตั้ง default ประเภทเดียวกันพร้อมกัน → 409 (EC-01 · ต้อง simulate)
- group: Concurrency · ความสำคัญ: ต่ำ · trace: EC-01 / AD-04 / ERR_STALE_DATA
- Setup: role=finance_admin ×2 session · seed=t3 NET30 (credit default) · files=— · **ต้อง inject: 2 request PATCH default พร้อมกันด้วย If-Match version เดียวกัน**
- Start: (API) 2 concurrent set-default
- ผ่านเมื่อ: first commit ชนะ · second → 409 ERR_STALE_DATA

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) admin A + admin B ยิง set default credit พร้อมกัน (version เดียวกัน) | — | A สำเร็จ (200) · B ได้ **409 ERR_STALE_DATA** (optimistic lock) | ☐ |

#### TC-CC02 — double-submit create → idempotency (EC-02 · ต้อง simulate)
- group: Concurrency · ความสำคัญ: ต่ำ · trace: EC-02 / AD-04 / ERR_DUPLICATE_IDEMPOTENCY_KEY
- Setup: role=finance_admin · seed=seed 12 · files=— · **ต้อง inject: double POST ด้วย Idempotency-Key เดียวกัน**
- Start: OPEN `#/finance/payment-term` → CLICK "เพิ่มเงื่อนไข"
- ผ่านเมื่อ: ไม่เกิดแถวซ้ำ (request 2 คืน cached)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กรอก CR-1 valid · double-click ปุ่ม "บันทึกและสร้าง" เร็ว ๆ | CR-1 | drawer ปิดหลังคลิกแรก · เกิดแถว NET90 **เพียง 1 แถว** (ไม่ซ้ำ) · badge +1 เท่านั้น | ☐ |
| 2 | (simulate API) 2 POST ด้วย Idempotency-Key เดียวกัน | — | request 2 คืน cached (ไม่ INSERT ซ้ำ, ไม่ dup audit) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. **เตรียม state:** ทุกเคสสมมติ seed 12 terms ตั้งต้น (ตาราง Meta). ถ้า prototype = mock in-memory → **reload หน้า (OPEN ใหม่) ก่อนทุกเคส** เพื่อคืน state (เพราะ create/delete/status ก่อนหน้าเปลี่ยน state). Refresh = กลับ List เสมอ.
2. **อ่าน Start** ของเคส → ไปหน้านั้น (prototype: เปิดไฟล์ = List; create/edit/view = คลิกปุ่ม/แถวตามระบุ).
3. **ทำ step ตามลำดับ** — Action ขึ้นต้น verb tag (OPEN/CLICK/TYPE/SELECT/TOGGLE/PRESS/WAIT/VERIFY). ผูก target ด้วย **ข้อความที่เห็นบนจอ** (ปุ่ม/label/หัวข้อ).
4. **ตรวจ Expected ด้วยตา** — ข้อความปรากฏ/หาย · pill/สี · จำนวนแถว · ปุ่ม disabled · toast (บนสุดกึ่งกลาง, error/warning ค้าง 5s → ใช้ WAIT ≤5s ก่อนเช็ค).
5. **ติ๊กผล** `☐→✅ (pass)` / `❌ (fail)` / `⛔ (blocked)`. เคส `(ต้อง simulate)` ถ้า runner เตรียม downstream/role/inject ไม่ได้ → **BLOCKED** พร้อม evidence.
6. **กรอก Result Report (schema)** ด้านล่างเมื่อจบทุกเคส.

> **หมายเหตุค่าที่คาดหวังอิง seed:** ถ้า runner ใช้ seed ต่างจากตาราง Meta ให้ปรับตัวเลข (badge/นับ/ยอดข้าม) ตาม seed จริง — logic เดิม.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Acceptance (AT-01..19) | 19 / 19 |
| Business rules (BR-01..13) | 13 / 13 |
| Edge cases (EC-01..11) | 9 / 11 (ข้าม EC-04, EC-08 — OQ/downstream) |
| Error codes (catalog) | 12 / 16 (ข้าม 4 API-generic ที่ไม่มี trigger UI) |
| Permission cells | 3 / 3 (Admin/Viewer/Consumer — Viewer/Consumer ต้อง simulate) |
| Cross-Module (XT-01..06) | 6 / 6 (ทั้งหมด simulate) |
| Scope Lock (LOCK) | 12 / 12 |
| [AI-DEFAULT] (AD-01..04) | 4 / 4 (AD-04 simulate) |
| UI states / interaction | ครบ (loaded/filtered-empty/scroll/Esc/responsive/live-badge) |

- Cross-Module (XT): **6 / 6** (มีเคส verify ครบ — mark (ต้อง simulate))
- Scope Lock (LOCK): **12 / 12** (ทุกข้อยืนยันมีเคส verify)
- [AI-DEFAULT]: **AD-01/02/03/04 ครบ** — เคสติดแท็ก `[AI-DEFAULT]` ที่หัว (TC-AD01..03, TC-CC01/02)
- **Manifest cross-check (FRD §0.12): ✅ 8/8 Stories · 13/13 Rules · 19/19 Edges (10 confirmed + 9 probe) mapped**
  - Stories: US-01→TC-C01/B · US-02→TC-C06/E03 · US-03→TC-SL02/V10 · US-04→TC-DF01..04 · US-05→TC-E01/AD01 · US-06→TC-S01..05 · US-07→TC-D01..05 · US-08→TC-L01..12 ✅

### ข้าม (พร้อมเหตุผล)
- **EC-04 (นิยาม `used`)** — OQ-PAY-07 ยัง OPEN (blocking delete guard); ไม่มีผลสังเกตบน UI prototype (used = mock ตายตัว) → verify เมื่อ spec ปิด.
- **EC-08 (EOM cross boundary)** — due date คำนวณที่ downstream (AP/AR), OQ; F-PAY เก็บแค่ config → นอกขอบเขต master UI.
- **XT-04 / EC-07 (deposit VAT)** — OQ-PAY-04 ยัง OPEN → เคส TC-XT04 mark BLOCKED จนกว่า spec ปิด.
- **Error codes ที่ข้าม (4):** ERR_NOT_AUTHENTICATED (401) · ERR_NOT_FOUND (404) · ERR_VALIDATION_FAILED (400 generic) · ENG_ERR_INVALID_INPUT (500) — เป็น API-level ที่ไม่มี trigger บน UI prototype (server-side; ทดสอบใน API test suite).
- **Out of Scope (นอกขอบเขตใบเซ็น — ห้ามสร้างเคส positive):** CSV import/export (verify absence = TC-SL01) · PR ใน use_in (verify absence = TC-SL02) · แก้ Credit trigger (verify lock = TC-SL03) · single-row delete (verify absence = TC-SL04) · approval UI (verify absence = TC-SL05) · multi-currency (verify absence = TC-SL06) · discount >1 tier (verify absence = TC-SL08) — ทั้งหมดมีเคส **verify ว่าไม่มี** ตาม Scope Lock (ไม่สร้างเคสให้ทำงาน).

---

## Result Report (schema)

```json
{
  "feature_id": "F-PAY",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 89, "pass": 0, "fail": 0, "blocked": 0 }
}
```

> `evidence` = สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (ข้อความ toast จริง · pill/สีที่ปรากฏ · route/สถานะที่ค้าง · ปุ่มที่คาดว่า disabled แต่กดได้). `note` = หมายเหตุ (เช่น "ต้อง simulate downstream — runner เตรียมไม่ได้").
> เคส `(ต้อง simulate)` = TC-XT01..06, TC-PM01/02, TC-CC01/02, TC-EC09(viewport) — ถ้า environment ไม่รองรับ ให้ status=`blocked` + ระบุเหตุใน note.
</content>
</invoke>
