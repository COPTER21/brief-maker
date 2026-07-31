# AI Test Cases — Product Master (F-PRODUCT-MASTER-001)

ชุดเทสสำหรับ AI agent (browser-use / vision) รันบน prototype `product-master.html` (v6 · no-approval) —
ทุก anchor เป็นข้อความจริงบนจอ (verbatim จาก HTML + FRD v2.0 §6.10) · route = hash routing refresh-safe.
เคสที่ติด `[AI-DEFAULT]` = เกณฑ์ที่ AI ตัดสินแทน BA (FRD OQ-07) — fail อาจแปลว่า default ผิด ไม่ใช่โค้ดผิด.

## Meta

| Field | Value |
|---|---|
| Feature ID | F-PRODUCT-MASTER-001 (FRD v2.0 · FULL · Reverse Mode) |
| ชื่อ | Product Master — ทะเบียนสินค้า |
| App entry | เปิดไฟล์ `product-master.html` → route หลัก `#/products` |
| Routes | `#/products` · `#/products/create` · `#/products/edit/:id` · `#/products/view/:id` · `#/products/{archive\|obsolete\|discontinue}/:id` · bulk = modal ไม่มี hash |
| ที่มา | FRD_F-PRODUCT-MASTER-001_Pack (00/01/02/03/04/05/06/07) + HTML ต้นทาง (anchor ชนะ) |
| จำนวนเคส | 61 เคส / 12 กลุ่ม |
| หมายเหตุ | ไม่มีชั้นอนุมัติ/DOA (LD-01) — ห้ามคาดหวังคำว่า "อนุมัติ" บนจอ · prototype = mock in-memory (refresh = reset ข้อมูล) |

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| L รายการ/ค้นหา/กรอง | 8 | สูง |
| C สร้างสินค้า (wizard) | 6 | สูง |
| V Validation (negative) | 7 | สูง |
| E แก้ไข/amend | 5 | สูง |
| S State machine | 9 | สูง |
| W View drawer | 5 | กลาง |
| P Permission/pricing | 3 | สูง |
| B Bulk import | 4 | สูง |
| M รูปภาพ/เอกสาร | 3 | กลาง |
| U Routing/UX | 5 | กลาง |
| X Cross-module (XT) | 3 | กลาง (simulate) |
| A AI-DEFAULT (concurrency) | 3 | ต่ำ (ต้อง simulate — prototype เทสไม่ได้) |
| K Locked Decisions verify | รวมอยู่ใน L/C/S (ดู Ledger) | — |

## Coverage Ledger

### FR / AC (06_TESTS)
| item | cases |
|---|---|
| AC-01 list+filter+sort | TC-L01..L05 |
| AC-02 empty 2 เคส | TC-L06, TC-L07 |
| AC-03 create draft | TC-C05 |
| AC-04 create+activate happy | TC-C01..C04 |
| AC-05 NOT_READY gate | TC-V05, TC-S03 |
| AC-06 amend active | TC-E01, TC-E02 |
| AC-07 edit guard | TC-E04, TC-E05 |
| AC-08 UOM rules | TC-V02, TC-V03 |
| AC-09 IR-02 lock | TC-E03 |
| AC-10 VR-MM | TC-V04, TC-C03 |
| AC-11 pricing gate | TC-P01..P03 |
| AC-12 เลิกผลิต | TC-S01 |
| AC-13 reactivate | TC-S02, TC-S03 |
| AC-14 ยกเลิกถาวร | TC-S04 |
| AC-15 จัดเก็บ soft | TC-S05, TC-S06 |
| AC-16 bulk preview | TC-B01, TC-B02 |
| AC-17 bulk partial | TC-B03 |
| AC-18 audit+version | TC-W04 |
| AC-19 routing/Esc/context | TC-U01..U03 |
| AC-20 concurrency/idempotency | TC-A01, TC-A02 (simulate) |

### Business Rules (05_RULES)
| rule | cases |
|---|---|
| BR-PDM-01 code ซ้ำ | TC-V01, TC-B02 |
| BR-PDM-02 code immutable (IR-01) | TC-E02 (step verify), TC-C06 |
| BR-PDM-03 UOM VR-03/VR-04 | TC-V02, TC-V03, TC-C02 |
| BR-PDM-04 IR-02 lock has_txn | TC-E03 |
| BR-PDM-05 activation gate | TC-V05, TC-S03 |
| BR-PDM-06 VR-MM | TC-V04, TC-C03, TC-B02 |
| BR-PDM-07 amend version+1 | TC-E01, TC-W04 |
| BR-PDM-08 soft delete | TC-S05, TC-S06, TC-X03 |
| BR-PDM-09 behavior defaults | TC-C02, TC-C06 |
| BR-PDM-10 pricing Confidential | TC-P01..P03 |

### Edge Cases
| EC | cases / สถานะ |
|---|---|
| EC-01 concurrent amend [AI-DEFAULT] | TC-A01 (ต้อง simulate) |
| EC-02 idempotency [AI-DEFAULT] | TC-A02 (ต้อง simulate) · double-click กันด้วย loading — TC-C04 |
| EC-03 hash-hack guards | TC-E04, TC-E05, TC-S08 |
| EC-04 เปลี่ยน type regen code | TC-C06 |
| EC-05 bulk partial | TC-B03 |
| EC-06 genCode race [AI-DEFAULT] | TC-A03 (ต้อง simulate) |
| EC-07 ลบรูปปก auto-promote | TC-M02 |
| EC-08 reactivate ไม่พร้อม | TC-S03 |

### Error Codes (05 §5.6 — เฉพาะที่เห็นบนจอ prototype)
| error | cases |
|---|---|
| BR_CODE_DUPLICATE | TC-V01 |
| BR_UOM_FACTOR | TC-V02 |
| BR_UOM_DUP_BASE | TC-V03 (step) |
| BR_UOM_CROSS_CATEGORY | TC-V03 |
| BR_UOM_LOCKED (IR-02) | TC-E03 |
| BR_MINMAX_INVALID | TC-V04 |
| BR_NOT_READY | TC-V05, TC-S03 |
| BR_INVALID_STATE | TC-S07, TC-S08 |
| BR_REQUIRED (bulk) | TC-B02 † seed sample ไม่มีแถว REQUIRED — verify ผ่าน pill รูปแบบเดียวกัน ⚠ ยืนยัน anchor |
| BR_BAD_TYPE (bulk) | — ข้าม (sample จอไม่มีแถว BAD_TYPE — API-level, ต้องเทส BE) |
| ERR_STALE_DATA / ERR_DUPLICATE_IDEMPOTENCY_KEY | TC-A01, TC-A02 (simulate — API-level) |
| ERR_VALIDATION_FAILED/401/403/404 | — ข้าม (API-level, prototype ไม่มี server) |

### Permission Matrix
| cell | cases |
|---|---|
| product_manager (canManage+pricing) ทำครบ | ทุกเคสหลัก (default role ของ prototype) |
| role ไม่มี pricing → list `•••` + header `— จำกัด —` | TC-P01 |
| role ไม่มี pricing → tab ราคา = "ข้อมูลจำกัด (Confidential)" | TC-P02 |
| role ไม่ใช่ canManage → ปุ่มจัดการหาย | TC-P03 |

### Cross-Module (XT — 06 §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 threshold event | Inventory Monitoring | TC-X01 (ต้อง simulate — เช็คฝั่งต้นทาง) |
| XT-02 picker กรอง active | Sales/Purchase/BOM | TC-X02 (ต้อง simulate) |
| XT-03 archive คง FK | เอกสารเก่า | TC-X03 (ต้อง simulate) |

### Scope Lock / Locked Decisions (07 §7.0 = N/A standalone → verify LD ที่สังเกตได้)
| LD | ข้อยืนยัน | Case verify |
|---|---|---|
| LD-01 ไม่มีชั้นอนุมัติ | ไม่มีคำ "อนุมัติ"/"รออนุมัติ" บนจอ + ไม่มีสถานะ pending | TC-L08 |
| LD-02 DOA placeholder | data-level (ไม่มีผลบนจอ) | — ข้าม (ตรวจที่ DB/payload ตอน dev) |
| LD-03 ENG-STOCK-ALERT downstream | — | TC-X01 |
| LD-04 ไม่มี 4-Code | ไม่มี composer/ช่อง item/sku | TC-C01 (step verify) |
| LD-05 wizard 4 ขั้นตามจอ | stepper = 4 ขั้น ชื่อตรง | TC-C01 (step 1) |
| LD-06 soft reference picker | หมวด/กลุ่ม พิมพ์อิสระ/picker ไม่ block FK | TC-C02 (step) |

### Cross-cutting / States
| item | cases |
|---|---|
| UI states: loaded/empty/filtered-empty | TC-L01, TC-L06, TC-L07 |
| Stats 4 tiles + สอดคล้อง filter | TC-L01, TC-S01 (delta R17) |
| Pagination windowing + page size | TC-L05 |
| Audit timeline + version footer | TC-W04 |
| Notification placeholder (F-NT) | TC-U05 |
| Submitting state `กำลังบันทึก…` (Rule #44) | TC-C04 |

## Data Sets

### ชุด A — สินค้าใหม่ (happy · activate ได้)
| ฟิลด์ (ป้ายบนจอ) | ค่า |
|---|---|
| ชื่อสินค้า (ไทย) | โต๊ะทดสอบ AI รุ่น A |
| ชื่อสินค้า (อังกฤษ) | AI Test Table A |
| ประเภทสินค้า | สินค้าสำเร็จรูป (FG) — default |
| หมวดหลัก | เฟอร์นิเจอร์ |
| ต้นทุนมาตรฐาน | 120 |
| ราคาขาย | 250 |
| Posting Group (สินค้า) | เลือกตัวแรกที่ไม่ว่าง (FINISHED) |
| กลุ่มภาษี | เลือกตัวแรกที่ไม่ว่าง (VAT7) |
| สต็อกขั้นต่ำ (Min) | 50 |
| สต็อกสูงสุด (Max) | 500 |

### ชุด B — ค่าผิดสำหรับ negative
| กรณี | ค่า |
|---|---|
| VR-MM ผิด | Min = 50 · Max = 10 |
| VR-03 ผิด | factor หน่วยแปลง = 0 |
| หน่วยข้ามหมวด | หน่วยฐาน PCS (นับจำนวน) + เพิ่มหน่วยแปลง KG (น้ำหนัก) |
| code ซ้ำ | ตั้งชื่อใด ๆ แล้วแก้ช่องรหัสไม่ได้ (readonly) → ใช้เคส bulk แถว FG-1005 แทน |

### Seed ในไฟล์ (ใช้เป็น Setup — มีอยู่แล้วเมื่อเปิดไฟล์)
| Code | สถานะ | ใช้ทดสอบ |
|---|---|---|
| FG-1001 | ใช้งาน | transitions loop (S) |
| RM-2001 | ใช้งาน + มี transaction (has_txn) | IR-02 lock (TC-E03) |
| FG-1010 | ร่าง · ข้อมูลไม่ครบ (ไม่มี Posting Group) | NOT_READY (TC-V05) |
| FG-1020 | เลิกผลิต + มี transaction | reactivate + amend (TC-S02, TC-E01) |
| FG-1030 | ใช้งาน | view/modal-over-view (TC-U02) |
| NS-6001 | ใช้งาน (sellable=false) | behavior flags (TC-W03) |

### ไฟล์ทดสอบ (Files)
- ไม่มีไฟล์จริง — bulk ใช้ **mock preview ในตัว** (`คลิกกล่อง "เลือกไฟล์ CSV / Excel"` → โหลด sample 5 แถว: FG-1050 ✓, RM-2050 ✓, TR-4050 ✓, FG-1005 = CODE_DUPLICATE, PM-3050 = MINMAX_INVALID)

---

## Test Cases

### กลุ่ม L — รายการ / ค้นหา / กรอง

### TC-L01 — เปิดหน้ารายการครั้งแรก (loaded state + stats)
- group: L · ความสำคัญ: สูง · trace: AC-01 / H-01
- actor (role): product_manager (default ของ prototype)
- Setup: role=product_manager · seed=ตามไฟล์ · files=—
- Start: OPEN `#/products`
- ผ่านเมื่อ: ตาราง + stats + filter bar ครบตามจอ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/products` | — | หัวหน้า **ทะเบียนสินค้า** + badge จำนวนรายการ; breadcrumb `Master Data > Product Master` | ☐ |
| 2 | VERIFY แถบ stats 4 ใบ | — | ป้าย: **สินค้าทั้งหมด** · **ใช้งาน** · **เลิกผลิต · ยกเลิก** · **ร่าง (backlog)** — ไม่มีใบ "รออนุมัติ" | ☐ |
| 3 | VERIFY หัวตาราง | — | 8 คอลัมน์: **รหัส · สินค้า · รหัสเก่า · ประเภท · หน่วยฐาน · ราคา/ต้นทุน · สถานะ · (คอลัมน์ปุ่ม)** | ☐ |
| 4 | VERIFY ปุ่มหัวหน้า | — | **นำเข้าจำนวนมาก** (รอง) + **เพิ่มสินค้า** (แดง primary) | ☐ |
| 5 | VERIFY แถว FG-1001 | — | เห็น pill สถานะ **ใช้งาน** (เขียว) + ราคาเป็นตัวเลข ฿ (role นี้เห็นราคา) | ☐ |

### TC-L02 — ค้นหาเจอ (ชื่อ) + ไม่กระทบ stats
- group: L · trace: AC-01 · Setup: role=product_manager · seed=ตามไฟล์ · files=—
- Start: OPEN `#/products`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดจำนวนแถวทั้งหมด | — | จดจำนวน (อ้าง step 4) | ☐ |
| 2 | TYPE `โต๊ะ` → ช่องค้นหา (placeholder **ค้นหารหัส / ชื่อ / GTIN / หมวด / กลุ่ม...**) | โต๊ะ | ตารางเหลือเฉพาะแถวที่ชื่อมี "โต๊ะ" | ☐ |
| 3 | TYPE ล้างช่องค้นหาเป็นว่าง | — | แถวกลับมาเท่าค่าที่จดใน step 1 | ☐ |
| 4 | TYPE `OLD-DESK-001` → ช่องค้นหา | OLD-DESK-001 | เจอแถว **FG-1001** (ค้นด้วยรหัสเก่าได้) | ☐ |

### TC-L03 — filter ประเภท + สถานะ ทุกตัวเลือกหลัก
- group: L · trace: AC-01 / BR-PDM-09 · Setup: role=product_manager · seed=ตามไฟล์
- Start: OPEN `#/products`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT `วัตถุดิบ (RM)` → dropdown **ทุกประเภท** | RM | เหลือเฉพาะแถว pill ประเภท **RM** | ☐ |
| 2 | SELECT กลับ `ทุกประเภท` | — | แถวกลับมาครบ | ☐ |
| 3 | SELECT `ร่าง` → dropdown **ทุกสถานะ** | ร่าง | เหลือเฉพาะ pill **ร่าง** (มี FG-1010) | ☐ |
| 4 | VERIFY ตัวเลือกใน dropdown สถานะ | — | มี 5 ค่า: ร่าง/ใช้งาน/เลิกผลิต/ยกเลิก/จัดเก็บ — **ไม่มี "รออนุมัติ"** | ☐ |
| 5 | SELECT `ใช้งาน` → สถานะ | ใช้งาน | เหลือเฉพาะ pill **ใช้งาน** | ☐ |

### TC-L04 — sort คอลัมน์รหัส 2 ทิศ
- group: L · trace: AC-01 · Setup: role=product_manager · seed=ตามไฟล์
- Start: OPEN `#/products`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวคอลัมน์ **รหัส** | — | ลูกศร sort ชี้ขึ้น/ลง + ลำดับแถวเรียงตามรหัส | ☐ |
| 2 | CLICK หัวคอลัมน์ **รหัส** อีกครั้ง | — | ทิศกลับด้าน (แถวแรก↔แถวท้ายสลับกลุ่ม) | ☐ |
| 3 | CLICK หัวคอลัมน์ **สินค้า** | — | เรียงตามชื่อ (ลูกศรย้ายมาคอลัมน์สินค้า) | ☐ |

### TC-L05 — page size + pagination windowing
- group: L · trace: AC-01 / H-01 · Setup: role=product_manager · seed=ตามไฟล์ (13+ แถว)
- Start: OPEN `#/products`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT `10` → ตัวเลือกจำนวนต่อหน้า (ท้ายตาราง) | 10 | ตารางแสดง ≤10 แถว + ปุ่มเลขหน้า ≥2 หน้า | ☐ |
| 2 | CLICK ปุ่มหน้า **2** | — | แถวเปลี่ยนชุด + ปุ่ม 2 เป็น active | ☐ |
| 3 | SELECT `ร่าง` → dropdown สถานะ | — | กลับหน้า 1 อัตโนมัติ (ปุ่ม 1 active) | ☐ |
| 4 | SELECT `50` → จำนวนต่อหน้า + SELECT `ทุกสถานะ` | 50 | ทุกแถวอยู่หน้าเดียว | ☐ |

### TC-L06 — empty แบบ filter ไม่เจอ + ล้างตัวกรอง
- group: L · trace: AC-02 (filtered-empty) · Setup: role=product_manager
- Start: OPEN `#/products`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `zzzz-ไม่มีจริง` → ช่องค้นหา | zzzz-ไม่มีจริง | ตารางหาย แสดง empty **ไม่พบสินค้าตามเงื่อนไข** + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** (ใน empty) | — | ตารางกลับมาครบ + toast **ล้างตัวกรองแล้ว** | ☐ |

### TC-L07 — empty แบบไม่มีข้อมูลเลย (edge)
- group: L · trace: AC-02 · Setup: role=product_manager · seed=**ต้อง simulate** — ล้างข้อมูลทั้งหมด (prototype: ไม่มีปุ่มลบทั้งหมด → เคสนี้ BLOCKED ได้ ให้ตรวจจากโค้ด/OK ที่มีข้อความสำรอง)
- Start: OPEN `#/products`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (เมื่อไม่มีข้อมูลเลย) | — | empty **ยังไม่มีสินค้าในทะเบียน** + ปุ่ม **เพิ่มสินค้า** | ☐ |

### TC-L08 — ไม่มีร่องรอยชั้นอนุมัติ (verify LD-01)
- group: L · trace: LD-01 / H-13 · Setup: role=product_manager
- Start: OPEN `#/products`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ทั้งหน้า list | — | ไม่มีคำ **อนุมัติ / รออนุมัติ / DOA** ที่ใดบนจอ | ☐ |
| 2 | CLICK แถว FG-1001 → VERIFY view ทุกแท็บ | — | แท็บมี 5: **ภาพรวม · หน่วยนับ · ราคา · รูปภาพ & เอกสาร · ประวัติ** — ไม่มีแท็บ "การอนุมัติ" | ☐ |
| 3 | PRESS Esc | — | กลับ `#/products` | ☐ |

---

### กลุ่ม C — สร้างสินค้า (wizard 4 ขั้น)

### TC-C01 — เปิด wizard + โครง 4 ขั้น + gen code (happy step 1)
- group: C · ความสำคัญ: สูง · trace: AC-04 / LD-04 / LD-05 / BR-PDM-02
- Setup: role=product_manager · seed=— · files=—
- Start: OPEN `#/products` แล้ว CLICK ปุ่ม **เพิ่มสินค้า**
- ชุดข้อมูล: A

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เพิ่มสินค้า** | — | drawer เปิด (route = `#/products/create`) + stepper **4 ขั้น**: ข้อมูลหลัก · หน่วยนับ · ราคา · รูปภาพ & เอกสาร | ☐ |
| 2 | VERIFY ช่อง **รหัสสินค้า** | — | มีค่าอัตโนมัติรูปแบบ `FG-xxxx` + แก้ไขไม่ได้ (readonly) — ไม่มีช่อง item/sku composer ใด ๆ | ☐ |
| 3 | TYPE ชุด A → ช่อง **ชื่อสินค้า (ไทย)** | โต๊ะทดสอบ AI รุ่น A | ช่องแสดงค่า | ☐ |
| 4 | SELECT `เฟอร์นิเจอร์` → ช่อง **หมวดหลัก** | A | ค่าแสดงในช่อง | ☐ |
| 5 | CLICK ปุ่ม **ถัดไป** | — | ไปขั้น 2 **หน่วยนับ** (stepper ขั้น 2 active) | ☐ |

### TC-C02 — ขั้น 2 หน่วยนับ: default + เพิ่มหน่วยแปลงถูกต้อง
- group: C · trace: AC-04 / BR-PDM-03 / LD-06 · Setup: role=product_manager (ต่อจาก TC-C01 หรือเริ่มใหม่ให้ถึงขั้น 2)
- Start: OPEN `#/products/create` → กรอกขั้น 1 (ชุด A) → CLICK **ถัดไป**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง **หน่วยฐาน** | — | ค่า default = PCS (หน่วยเล็กสุด) + hint บอกว่าหน่วยฐานคือหน่วยเล็กสุด | ☐ |
| 2 | CLICK ปุ่มเพิ่มหน่วยแปลง (ป้าย **เพิ่มหน่วยแปลง**) | — | แถวใหม่: `1 [หน่วย] = [factor] PCS` + toggle ซื้อ/ขาย/เริ่มต้น/เก็บสต็อก | ☐ |
| 3 | SELECT `BOX` → หน่วยของแถวใหม่ + TYPE `12` → factor | BOX/12 | แถวแสดง `1 BOX = 12 PCS` | ☐ |
| 4 | VERIFY ส่วน behavior toggles | — | มี 3 ตัว: เก็บสต็อก · ขายได้ · ซื้อได้ — ค่า default ตามประเภท FG (เก็บสต็อก ✓, ขายได้ ✓, ซื้อได้ ✗) | ☐ |
| 5 | CLICK **ถัดไป** | — | ไปขั้น 3 **ราคา** | ☐ |

### TC-C03 — ขั้น 3 ราคา + VR-MM block แล้วแก้ผ่าน (boundary)
- group: C · trace: AC-10 / BR-PDM-06 · Setup: role=product_manager · ชุดข้อมูล: A + B
- Start: ต่อจาก TC-C02 (อยู่ขั้น 3)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `120` → **ต้นทุนมาตรฐาน** และ `250` → **ราคาขาย** | A | ช่องแสดงค่า | ☐ |
| 2 | SELECT Posting Group + กลุ่มภาษี (ตัวเลือกแรกที่ไม่ว่าง) | A | ค่าแสดง | ☐ |
| 3 | TYPE `50` → **สต็อกขั้นต่ำ (Min)** และ `10` → **สต็อกสูงสุด (Max)** | B | — | ☐ |
| 4 | CLICK **ถัดไป** | — | **ไม่ไปขั้น 4** + toast **สต็อกสูงสุด (Max) ต้องไม่ต่ำกว่าขั้นต่ำ (Min) — MINMAX_INVALID** | ☐ |
| 5 | TYPE `500` → **สต็อกสูงสุด (Max)** แล้ว CLICK **ถัดไป** | A | ไปขั้น 4 **รูปภาพ & เอกสาร** | ☐ |

### TC-C04 — submit "บันทึกและเปิดใช้งาน" (happy + loading state)
- group: C · ความสำคัญ: สูง · trace: AC-04 / H-03 / Rule #44 · Setup: role=product_manager
- Start: ต่อจาก TC-C03 (อยู่ขั้น 4)
- ผ่านเมื่อ: record ใหม่เป็น **ใช้งาน** ทันที ไม่ผ่านสถานะรอใด ๆ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม primary ที่ footer | — | ป้าย = **บันทึกและเปิดใช้งาน** (ไม่ใช่ "ส่งอนุมัติ") | ☐ |
| 2 | CLICK ปุ่ม **บันทึกและเปิดใช้งาน** | — | ปุ่ม disabled + ป้ายเปลี่ยนเป็น **กำลังบันทึก…** (spinner) | ☐ |
| 3 | WAIT จน drawer ปิด (≤3s) | — | กลับ `#/products` + toast **บันทึกและเปิดใช้งานแล้ว** | ☐ |
| 4 | TYPE `โต๊ะทดสอบ AI` → ช่องค้นหา | — | เห็นแถวใหม่ pill **ใช้งาน** | ☐ |
| 5 | CLICK แถวนั้น → CLICK แท็บ **ประวัติ** | — | timeline มี **สร้างรายการ (v1)** และ **เปิดใช้งาน** | ☐ |

### TC-C05 — บันทึกแบบร่าง (ขั้นไหนก็ได้)
- group: C · trace: AC-03 · Setup: role=product_manager · ชุดข้อมูล: A (เฉพาะขั้น 1)
- Start: OPEN `#/products/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ชื่อ `ร่างทดสอบ AI` → **ชื่อสินค้า (ไทย)** + SELECT หมวดหลัก | — | ค่าแสดง | ☐ |
| 2 | CLICK ปุ่ม **บันทึกแบบร่าง** | — | drawer ปิด + toast **บันทึกร่างแล้ว** | ☐ |
| 3 | SELECT `ร่าง` → dropdown สถานะ | — | เห็นแถว "ร่างทดสอบ AI" pill **ร่าง** | ☐ |

### TC-C06 — เปลี่ยนประเภทตอน create → regen code + behavior reset (edge: EC-04)
- group: C · trace: EC-04 / BR-PDM-09 / BR-PDM-02 · Setup: role=product_manager
- Start: OPEN `#/products/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดค่า **รหัสสินค้า** | — | รูปแบบ `FG-xxxx` (จดไว้เทียบ) | ☐ |
| 2 | SELECT `วัตถุดิบ (RM)` → **ประเภทสินค้า** | RM | รหัสเปลี่ยน prefix เป็น `RM-xxxx` (ต่างจากค่าที่จดใน step 1) | ☐ |
| 3 | CLICK **ถัดไป** → (กรอกชื่อก่อนถ้าถูก block) → VERIFY behavior ขั้น 2 | — | defaults ของ RM: เก็บสต็อก ✓ · ขายได้ ✗ · ซื้อได้ ✓ | ☐ |
| 4 | PRESS Esc → CLICK ยืนยันทิ้ง (ถ้ามี confirm) | — | กลับ list ไม่มี record ใหม่ | ☐ |

---

### กลุ่ม V — Validation (negative)

### TC-V01 — code ซ้ำ (negative — ผ่าน bulk sample)
- group: V · trace: BR-PDM-01 · หมายเหตุ: ช่องรหัสใน wizard เป็น readonly (gen เอง) — เคสซ้ำตรวจผ่าน bulk แถว FG-1005
- Setup: role=product_manager · seed=FG-1005 มีอยู่แล้ว (ใช้งาน) · files=mock sample
- Start: OPEN `#/products` → CLICK **นำเข้าจำนวนมาก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK กล่อง **เลือกไฟล์ CSV / Excel** | — | เข้าหน้า preview ตาราง 5 แถว | ☐ |
| 2 | VERIFY แถว **FG-1005** | — | pill error **CODE_DUPLICATE** (รหัสชนกับ record เดิม) | ☐ |
| 3 | PRESS Esc | — | modal ปิด | ☐ |

### TC-V02 — VR-03 factor ต้อง ≥ 1 (negative)
- group: V · trace: BR-PDM-03 · Setup: role=product_manager · ชุด B
- Start: OPEN `#/products/create` → กรอกขั้น 1 → **ถัดไป**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มหน่วยแปลง** + SELECT `BOX` + TYPE `0` → factor | B | — | ☐ |
| 2 | CLICK **ถัดไป** | — | ถูก block + toast แจ้งจำนวนหน่วยฐานต้อง **≥ 1** | ☐ |
| 3 | TYPE `12` → factor แล้ว CLICK **ถัดไป** | — | ผ่านไปขั้น 3 | ☐ |

### TC-V03 — VR-04 ห้ามซ้ำ base / ห้ามข้ามหมวด (negative)
- group: V · trace: BR-PDM-03 · Setup: role=product_manager · ชุด B
- Start: OPEN `#/products/create` → ขั้น 2 (หน่วยฐาน PCS)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มหน่วยแปลง** + SELECT `PCS` (ซ้ำหน่วยฐาน) | — | ถูก block/toast แจ้ง **ซ้ำกับหน่วยฐาน** เมื่อกดถัดไป | ☐ |
| 2 | SELECT `KG` (คนละหมวดกับ PCS) | B | — | ☐ |
| 3 | CLICK **ถัดไป** | — | ถูก block + toast แจ้ง **คนละหมวดกับหน่วยฐาน** | ☐ |
| 4 | SELECT `BOX` + TYPE `12` → CLICK **ถัดไป** | — | ผ่านไปขั้น 3 | ☐ |

### TC-V04 — VR-MM ที่ view/edit ของ record เดิม (negative)
- group: V · trace: BR-PDM-06 · Setup: role=product_manager · seed=FG-1001 (ใช้งาน, stocked)
- Start: OPEN `#/products` → CLICK แถว FG-1001 → CLICK **แก้ไข**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK stepper ขั้น **ราคา** (หรือกดถัดไปจนถึงขั้น 3) | — | เห็นช่อง **สต็อกขั้นต่ำ (Min)** / **สต็อกสูงสุด (Max)** | ☐ |
| 2 | TYPE `50` → Min และ `10` → Max | B | — | ☐ |
| 3 | CLICK **ถัดไป** | — | block + toast **…MINMAX_INVALID** (เด้งอยู่ขั้น 3) | ☐ |
| 4 | TYPE `500` → Max → CLICK **ถัดไป** จนขั้น 4 → CLICK **บันทึก** | — | drawer ปิด + toast **บันทึกการแก้ไขแล้ว** | ☐ |

### TC-V05 — NOT_READY: เปิดใช้งานร่างที่ข้อมูลไม่ครบ (negative)
- group: V · ความสำคัญ: สูง · trace: AC-05 / BR-PDM-05 · Setup: role=product_manager · seed=FG-1010 (ร่าง ไม่มี Posting Group)
- Start: OPEN `#/products` → CLICK แถว **FG-1010**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY header actions ของ view | — | มีปุ่ม **แก้ไข** + **เปิดใช้งาน** (primary) | ☐ |
| 2 | CLICK ปุ่ม **เปิดใช้งาน** | — | toast error **ข้อมูลไม่พร้อมใช้งาน: … (NOT_READY)** — ระบุรายการที่ขาด | ☐ |
| 3 | VERIFY pill สถานะบน header | — | ยังเป็น **ร่าง** (ไม่เปลี่ยน) | ☐ |

### TC-V06 — step 1 gate: ไม่กรอกชื่อ (required negative)
- group: V · trace: BR field validation (name_th required) · Setup: role=product_manager
- Start: OPEN `#/products/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ถัดไป** ทันทีโดยไม่กรอกอะไร | — | อยู่ขั้น 1 เดิม + แจ้งเตือนช่องบังคับ (ชื่อไทย/หมวดหลัก) | ☐ |
| 2 | TYPE ชื่อ + SELECT หมวดหลัก → CLICK **ถัดไป** | A | ไปขั้น 2 | ☐ |

### TC-V07 — บันทึกและเปิดใช้งานโดยไม่กรอกราคา (NOT_READY จาก wizard)
- group: V · trace: AC-05 / BR-PDM-05 · Setup: role=product_manager
- Start: OPEN `#/products/create` → กรอกขั้น 1 เท่านั้น → กด **ถัดไป** ข้ามถึงขั้น 4 (ไม่ใส่ต้นทุน/Posting Group)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกและเปิดใช้งาน** | — | toast **ข้อมูลไม่พร้อมใช้งาน: … (NOT_READY)** + เด้งกลับขั้น **ราคา** (ขั้น 3) | ☐ |
| 2 | VERIFY drawer | — | ยังเปิดอยู่ (ไม่ปิด, ข้อมูลที่กรอกไว้ยังอยู่) | ☐ |

---

### กลุ่ม E — แก้ไข / amend

### TC-E01 — amend สินค้าใช้งาน: ปุ่ม "บันทึก" + คงสถานะ + version+1
- group: E · ความสำคัญ: สูง · trace: AC-06 / BR-PDM-07 · Setup: role=product_manager · seed=FG-1020 (เลิกผลิต — reactivate ก่อน) หรือใช้ FG-1001 (ใช้งาน)
- Start: OPEN `#/products` → CLICK แถว FG-1001 → CLICK ปุ่ม **แก้ไข**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แท็บประวัติก่อนแก้ (เปิด view ก่อนกดแก้ไข) → จด version จาก footer `version N` | — | จดค่า N ไว้เทียบ step 6 | ☐ |
| 2 | CLICK **แก้ไข** → TYPE ต่อท้ายชื่อ ` (แก้โดย AI)` → ช่อง **ชื่อสินค้า (ไทย)** | — | ค่าแสดง | ☐ |
| 3 | CLICK **ถัดไป** จนถึงขั้น 4 | — | ถึงขั้น **รูปภาพ & เอกสาร** | ☐ |
| 4 | VERIFY ปุ่ม primary footer | — | ป้าย = **บันทึก** (ไม่ใช่ "บันทึกและเปิดใช้งาน") | ☐ |
| 5 | CLICK **บันทึก** → WAIT drawer ปิด | — | toast **บันทึกการแก้ไขแล้ว** + แถวในตารางชื่อใหม่ + pill ยังเป็น **ใช้งาน** | ☐ |
| 6 | CLICK แถวนั้น → VERIFY footer + แท็บ **ประวัติ** | — | `version N+1` (เทียบค่า step 1) + timeline มี **แก้ไข (vN+1)** | ☐ |

### TC-E02 — IR-01: รหัสแก้ไม่ได้ตอน edit
- group: E · trace: BR-PDM-02 · Setup: role=product_manager · seed=FG-1001
- Start: OPEN `#/products/edit/` ของ FG-1001 (คลิกแถว → แก้ไข)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง **รหัสสินค้า** ขั้น 1 | — | ค่า `FG-1001` + readonly (คลิก/พิมพ์ไม่เปลี่ยน) | ☐ |
| 2 | SELECT ประเภทเป็น `วัตถุดิบ (RM)` | — | **รหัสไม่เปลี่ยน** (regen เฉพาะตอน create — edit คงรหัสเดิม) | ☐ |
| 3 | PRESS Esc (ทิ้งการแก้) | — | ออกโดยไม่บันทึก | ☐ |

### TC-E03 — IR-02: หน่วยนับถูกล็อกเมื่อมี transaction
- group: E · ความสำคัญ: สูง · trace: AC-09 / BR-PDM-04 · Setup: role=product_manager · seed=**RM-2001** (ใช้งาน + has_txn)
- Start: OPEN `#/products` → TYPE `RM-2001` → ค้นหา → CLICK แถว → CLICK **แก้ไข**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไปขั้น 2 **หน่วยนับ** | — | ช่อง **หน่วยฐาน** disabled + แถวหน่วยแปลง disabled | ☐ |
| 2 | VERIFY ข้อความแจ้งในขั้น 2 | — | โน้ตล็อก: **สูตรหน่วยแปลงถูกล็อก — มี transaction แล้ว (IR-02)** | ☐ |
| 3 | PRESS Esc | — | ออกไม่บันทึก | ☐ |

### TC-E04 — edit guard: hash ตรงไปแก้ record ที่แก้ไม่ได้ (edge: EC-03)
- group: E · trace: AC-07 / EC-03 · Setup: role=product_manager · seed=ทำ FG-1001 ให้เป็น **ยกเลิก** ก่อน (รัน TC-S01+TC-S04 หรือทำ transition ผ่าน view)
- Start: OPEN `#/products/view/` ของ record ยกเลิก → จด id จาก URL

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/products/edit/<id ที่จดไว้>` (พิมพ์ hash ตรง) | — | ระบบ**เด้งไปหน้า view** ของ record นั้นแทน (เห็น drawer แบบแท็บ ไม่ใช่ wizard) | ☐ |
| 2 | VERIFY header actions | — | สถานะ **ยกเลิก** → มีเฉพาะปุ่ม **จัดเก็บ** | ☐ |

### TC-E05 — แก้ร่างต่อ (draft → wizard → บันทึกและเปิดใช้งาน)
- group: E · trace: AC-06/AC-04 · Setup: role=product_manager · seed=ร่างจาก TC-C05 หรือ FG-1050 (ร่างจาก bulk)
- Start: OPEN `#/products` → filter สถานะ **ร่าง** → CLICK แถวร่าง → CLICK **แก้ไข**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม footer ขั้น 4 (กดถัดไปจนสุด — เติมข้อมูลขั้น 3 ให้ครบ: ต้นทุน 120 / ราคา 250 / Posting Group / ภาษี) | A | ป้ายปุ่ม = **บันทึกและเปิดใช้งาน** (เพราะ record เป็นร่าง) | ☐ |
| 2 | CLICK **บันทึกและเปิดใช้งาน** → WAIT | — | toast **บันทึกและเปิดใช้งานแล้ว** + pill เป็น **ใช้งาน** | ☐ |

---

### กลุ่ม S — State machine (5 สถานะ)

### TC-S01 — active → เลิกผลิต (modal) + stats delta
- group: S · ความสำคัญ: สูง · trace: AC-12 / §5.2 · Setup: role=product_manager · seed=FG-1001 (ใช้งาน)
- Start: OPEN `#/products`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดตัวเลข stat **ใช้งาน** และ **เลิกผลิต · ยกเลิก** | — | จดค่าไว้เทียบ step 5 | ☐ |
| 2 | CLICK แถว FG-1001 → CLICK ปุ่ม **เลิกผลิต** | — | modal ยืนยัน **เลิกผลิต** ทับ view (route มี `/obsolete/`) — เนื้อหาบอกว่า ขายสต็อกคงเหลือได้ งดซื้อ/ผลิตเพิ่ม | ☐ |
| 3 | CLICK ปุ่มยืนยัน **เลิกผลิต** ใน modal | — | modal ปิด กลับ view + pill header = **เลิกผลิต** + toast **เปลี่ยนสถานะเป็น เลิกผลิต แล้ว** | ☐ |
| 4 | VERIFY header actions | — | เปลี่ยนเป็น: **แก้ไข · ใช้งานอีกครั้ง · ยกเลิกถาวร** | ☐ |
| 5 | PRESS Esc → VERIFY stats | — | **ใช้งาน** ลด 1 · **เลิกผลิต · ยกเลิก** เพิ่ม 1 (เทียบค่าที่จด step 1) | ☐ |

### TC-S02 — obsolete → ใช้งานอีกครั้ง (reactivate — direct ไม่มี modal)
- group: S · trace: AC-13 · Setup: role=product_manager · seed=FG-1020 (เลิกผลิต · ข้อมูลครบ)
- Start: OPEN `#/products` → TYPE `FG-1020` → CLICK แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ใช้งานอีกครั้ง** | — | **ไม่มี modal** — pill เปลี่ยนเป็น **ใช้งาน** ทันที + toast **สินค้ากลับมาสถานะ ใช้งาน แล้ว** | ☐ |
| 2 | CLICK แท็บ **ประวัติ** | — | timeline มีรายการกลับมาใช้งาน (reactivate) ล่าสุด | ☐ |

### TC-S03 — reactivate ของที่ข้อมูลไม่ครบ → NOT_READY (edge: EC-08)
- group: S · trace: EC-08 / BR-PDM-05 · Setup: role=product_manager · seed=**ต้องเตรียม**: ร่าง FG-1010 ไม่ใช้ได้ (เป็นร่าง) — ใช้วิธี: แก้ FG-1020 ลบ Posting Group (SELECT ค่าว่าง) → บันทึก → เลิกผลิต → แล้วลอง reactivate · ถ้าแก้ให้ว่างไม่ได้บนจอ → mark BLOCKED + เทสที่ API แทน
- Start: OPEN view ของ record เลิกผลิตที่ข้อมูลไม่ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ใช้งานอีกครั้ง** | — | toast **ข้อมูลไม่พร้อมใช้งาน: … (NOT_READY)** + pill ยังเป็น **เลิกผลิต** | ☐ |

### TC-S04 — obsolete → ยกเลิกถาวร (modal danger)
- group: S · trace: AC-14 · Setup: role=product_manager · seed=record เลิกผลิต (ทำ TC-S01 กับ FG-1001 ก่อน)
- Start: view ของ FG-1001 (เลิกผลิต)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยกเลิกถาวร** | — | modal ยืนยัน (ปุ่มยืนยันสีแดง **ยกเลิกถาวร**) — บอกปิดการขาย/ซื้อทุกช่องทาง | ☐ |
| 2 | CLICK **ยกเลิกถาวร** | — | pill = **ยกเลิก** + toast **เปลี่ยนสถานะเป็น ยกเลิก แล้ว** | ☐ |
| 3 | VERIFY header actions | — | เหลือเฉพาะ **จัดเก็บ** (ไม่มีแก้ไข/ใช้งานอีกครั้ง) | ☐ |

### TC-S05 — discontinued → จัดเก็บ (soft delete)
- group: S · trace: AC-15 / BR-PDM-08 · Setup: role=product_manager · seed=record ยกเลิก (ต่อจาก TC-S04)
- Start: view ของ FG-1001 (ยกเลิก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **จัดเก็บ** | — | modal **จัดเก็บสินค้า** | ☐ |
| 2 | CLICK ปุ่มยืนยัน **จัดเก็บ** | — | toast **จัดเก็บสินค้าแล้ว (soft delete)** + pill = **จัดเก็บ** | ☐ |
| 3 | VERIFY header actions + ตาราง | — | ไม่มีปุ่ม action ใด (ดูอย่างเดียว) + แถวยังอยู่ในตารางเมื่อ filter สถานะ **จัดเก็บ** (ไม่หายไป = soft) | ☐ |

### TC-S06 — active → จัดเก็บตรง + คำเตือน has_txn
- group: S · trace: AC-15 / BR-PDM-08 · Setup: role=product_manager · seed=**RM-2001** (ใช้งาน + has_txn)
- Start: OPEN view ของ RM-2001

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **จัดเก็บ** | — | modal จัดเก็บ + ข้อความเตือนว่า **มี transaction อ้างอิง** (archived เท่านั้น / BR-002) | ☐ |
| 2 | CLICK ปุ่ม **ยกเลิก** (ghost) ใน modal | — | modal ปิด กลับ view — pill ยังเป็น **ใช้งาน** (ไม่เปลี่ยน) | ☐ |

### TC-S07 — INVALID_STATE: ยิง action ผิดสถานะผ่าน hash (negative)
- group: S · trace: §5.2 guards / EC-03 · Setup: role=product_manager · seed=FG-1010 (ร่าง)
- Start: OPEN `#/products/view/` ของ FG-1010 → จด id จาก URL

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/products/obsolete/<id ของ FG-1010>` (พิมพ์ hash ตรง — ร่างห้ามเลิกผลิต) | — | ไม่เกิด transition: toast แจ้ง **…(INVALID_STATE)** + modal ไม่ค้าง (กลับ context) | ☐ |
| 2 | VERIFY pill ของ FG-1010 | — | ยังเป็น **ร่าง** | ☐ |

### TC-S08 — INVALID_STATE: archive ร่างผ่าน hash (negative)
- group: S · trace: §5.2 · Setup: role=product_manager · seed=FG-1010 (ร่าง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/products/archive/<id ของ FG-1010>` | — | toast **…(INVALID_STATE)** (จัดเก็บได้เฉพาะ ใช้งาน/ยกเลิก) + สถานะไม่เปลี่ยน | ☐ |

### TC-S09 — วงจรเต็ม: draft → active → obsolete → active (loop กลับ)
- group: S · trace: §5.2 ครบ loop · Setup: role=product_manager · seed=สร้างใหม่จากชุด A (TC-C04) หรือใช้ record ที่เพิ่ง active
- Start: view ของ record ใช้งาน (สร้างใหม่)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลิกผลิต** → ยืนยัน | — | pill **เลิกผลิต** | ☐ |
| 2 | CLICK **ใช้งานอีกครั้ง** | — | pill **ใช้งาน** (ข้อมูลครบ — ผ่าน gate) | ☐ |
| 3 | CLICK แท็บ **ประวัติ** | — | เห็นลำดับ: เปิดใช้งาน → เลิกผลิต → กลับมาใช้งาน เรียงตามเวลา | ☐ |

---

### กลุ่ม W — View drawer

### TC-W01 — โครง view: header + 5 แท็บ + footer
- group: W · trace: H-12 / 01_UI P-04 · Setup: role=product_manager · seed=FG-1001 (หรือ record ใช้งานใด ๆ)
- Start: OPEN `#/products` → CLICK แถว FG-1030

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY header | — | ชื่อสินค้า + pill สถานะ + บรรทัดรอง (รหัส · ประเภท) + ปุ่ม action ตามสถานะ + X | ☐ |
| 2 | VERIFY แท็บ | — | 5 แท็บ: **ภาพรวม · หน่วยนับ · ราคา · รูปภาพ & เอกสาร · ประวัติ** — active เริ่มที่ ภาพรวม | ☐ |
| 3 | VERIFY footer | — | `version N · สร้าง <วันที่>` + ปุ่ม **ปิด** | ☐ |
| 4 | CLICK ปุ่ม **ปิด** | — | drawer ปิด กลับ `#/products` | ☐ |

### TC-W02 — แท็บภาพรวม: ข้อมูล + Min/Max section
- group: W · trace: H-06 / BR-PDM-06 · Setup: role=product_manager · seed=FG-1001 (ตั้ง min/max ไว้)
- Start: view FG-1001 แท็บ **ภาพรวม**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัวข้อ **แจ้งเตือนระดับสต็อก** | — | แสดง Min/Max เป็น `N <หน่วยฐาน>` หรือ **— ไม่เตือน** เมื่อ null | ☐ |
| 2 | VERIFY info ใต้ section | — | ข้อความเชื่อม **Inventory Monitoring** (การเตือนจริงอยู่ปลายทาง) | ☐ |
| 3 | VERIFY ส่วนพฤติกรรม | — | badges เก็บสต็อก/ขายได้/ซื้อได้ ตรงกับค่า record | ☐ |

### TC-W03 — behavior flags ของ NS (sellable=false)
- group: W · trace: BR-PDM-09 · Setup: role=product_manager · seed=NS-6001
- Start: OPEN `#/products` → TYPE `NS-6001` → CLICK แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แท็บภาพรวม ส่วนพฤติกรรม | — | **ขายได้ = ปิด/ไม่ติ๊ก** (NS-6001 sellable=false) | ☐ |

### TC-W04 — แท็บประวัติ: audit เรียงเวลา + สี variant
- group: W · trace: AC-18 · Setup: role=product_manager · seed=record ที่ผ่านหลาย mutation (FG-1020 หลัง TC-S02/E01)
- Start: view record นั้น → CLICK แท็บ **ประวัติ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY timeline | — | มีรายการ create/แก้ไข/สถานะ พร้อมผู้ทำ+เวลา เรียงลำดับ | ☐ |
| 2 | VERIFY ไม่มีรายการ "ส่งอนุมัติ/อนุมัติ" | — | คำว่า อนุมัติ ไม่ปรากฏใน timeline (LD-01 — seed เขียนเป็น **เปิดใช้งาน**) | ☐ |

### TC-W05 — แท็บหน่วยนับ: ตาราง conversion + โน้ต IR-02
- group: W · trace: BR-PDM-03/04 · Setup: role=product_manager · seed=RM-2001 (has_txn)
- Start: view RM-2001 → CLICK แท็บ **หน่วยนับ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตารางหน่วย | — | หน่วยฐาน + แถวแปลง `1 X = n <base>` + flags | ☐ |
| 2 | VERIFY โน้ตล็อก | — | ข้อความ IR-02 (มี transaction — แก้สูตรไม่ได้) ปรากฏ | ☐ |

---

### กลุ่ม P — Permission / pricing

> prototype login เป็น product_manager — การสลับ role ต้อง **ต้อง simulate** (แก้ CURRENT_USER ใน dev build หรือรอระบบจริง). เคส P ระบุวิธีเช็คที่ทำได้บนจอปัจจุบัน + สิ่งที่ runner ต้องเตรียมถ้าจะเทสเต็ม.

### TC-P01 — role ไม่มีสิทธิ์ราคา: list ซ่อนราคา (permission · ต้อง simulate)
- group: P · ความสำคัญ: สูง · trace: AC-11 / BR-PDM-10 · Setup: role=**master_data_clerk** (canManage แต่ไม่อยู่ใน canSeePricing) — ต้อง simulate เปลี่ยน role ก่อนเปิดไฟล์
- Start: OPEN `#/products`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัวคอลัมน์ราคา | — | แสดง **— จำกัด —** | ☐ |
| 2 | VERIFY cell ราคาในทุกแถว | — | แสดง **•••** ไม่มีตัวเลข ฿ | ☐ |

### TC-P02 — role ไม่มีสิทธิ์ราคา: tab ราคา = Confidential (permission · ต้อง simulate)
- group: P · trace: AC-11 · Setup: role=master_data_clerk (simulate)
- Start: view record ใด ๆ → CLICK แท็บ **ราคา**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY เนื้อหาแท็บราคา | — | empty state **ข้อมูลจำกัด (Confidential)** — ไม่มีตัวเลขราคา/ต้นทุน | ☐ |

### TC-P03 — role ที่มีสิทธิ์ (default) เห็นราคา + Confidential tag
- group: P · trace: AC-11 · Setup: role=product_manager (default)
- Start: view FG-1001 → แท็บ **ราคา**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แท็บราคา | — | เห็นต้นทุน/ราคาเป็นตัวเลข ฿ + มีป้ายกำกับชั้นข้อมูล (Confidential) | ☐ |
| 2 | VERIFY list คอลัมน์ราคา | — | ตัวเลข ฿ ปกติ | ☐ |

---

### กลุ่ม B — Bulk import

### TC-B01 — เปิด bulk + โหลด preview 5 แถว
- group: B · trace: AC-16 · Setup: role=product_manager · files=mock sample ในตัว
- Start: OPEN `#/products` → CLICK **นำเข้าจำนวนมาก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY modal ขั้นแรก | — | กล่อง **เลือกไฟล์ CSV / Excel** + คำอธิบายคอลัมน์ | ☐ |
| 2 | CLICK กล่องเลือกไฟล์ | — | เข้าหน้า preview: ตาราง **5 แถว** (FG-1050, RM-2050, TR-4050, FG-1005, PM-3050) | ☐ |

### TC-B02 — preview: pill validate ต่อแถว + ปุ่มนับเฉพาะแถวผ่าน
- group: B · ความสำคัญ: สูง · trace: AC-16 / BR-PDM-01/06 · Setup: ต่อจาก TC-B01

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว FG-1050 / RM-2050 / TR-4050 | — | pill **พร้อมนำเข้า** (✓) | ☐ |
| 2 | VERIFY แถว FG-1005 | — | pill error **CODE_DUPLICATE** | ☐ |
| 3 | VERIFY แถว PM-3050 | — | pill error **MINMAX_INVALID** (min 80 > max 20) | ☐ |
| 4 | VERIFY ปุ่ม primary | — | ป้าย **นำเข้า 3 แถว** (นับเฉพาะแถวผ่าน) | ☐ |

### TC-B03 — commit partial + summary + record เป็นร่าง
- group: B · ความสำคัญ: สูง · trace: AC-17 / EC-05 · Setup: ต่อจาก TC-B02

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดจำนวนแถวตารางหลัก (ปิด modal ชั่วคราวไม่ได้ — จดจาก badge จำนวนรายการก่อนเปิด bulk) | — | ใช้ค่าที่จดก่อนเริ่ม TC-B01 (อ้าง step 4) | ☐ |
| 2 | CLICK **นำเข้า 3 แถว** | — | หน้า done: **นำเข้าเสร็จ — สร้างร่าง 3 แถว · ข้าม 2 แถว (IMPORT_ERROR)** + ตารางแถวที่ข้ามพร้อมเหตุผล + โน้ตว่ารายการอยู่สถานะ **ร่าง** | ☐ |
| 3 | CLICK ปุ่ม **ปิด** | — | modal ปิด + toast **นำเข้าแล้ว 3 แถว · ข้าม 2 แถว (IMPORT_ERROR)** | ☐ |
| 4 | SELECT `ร่าง` → filter สถานะ | — | เห็น FG-1050 / RM-2050 / TR-4050 pill **ร่าง** (จำนวนรวมเพิ่ม 3 จากค่าที่จด) | ☐ |

### TC-B04 — ยกเลิกกลางทาง (ไม่ commit)
- group: B · trace: AC-16 · Setup: role=product_manager
- Start: OPEN `#/products` → CLICK **นำเข้าจำนวนมาก** → CLICK กล่องเลือกไฟล์ (ถึง preview)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS Esc | — | modal ปิด — ไม่มี record ใหม่ (filter ร่าง ไม่เห็น FG-1050 เพิ่มถ้ายังไม่เคย commit) | ☐ |

---

### กลุ่ม M — รูปภาพ / เอกสารแนบ

### TC-M01 — เพิ่มรูป + ตั้งปก
- group: M · trace: H-11 · Setup: role=product_manager · seed=record ใช้งานที่มีรูป ≥1 (FG-1001)
- Start: view FG-1001 → CLICK **แก้ไข** → ไปขั้น 4 **รูปภาพ & เอกสาร**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มเพิ่มรูป (mock) | — | รูปใหม่ปรากฏใน gallery | ☐ |
| 2 | CLICK ปุ่มตั้งปกบนรูปที่ 2 | — | badge ปกย้ายไปรูปที่ 2 + toast **ตั้งเป็นรูปปกแล้ว** | ☐ |

### TC-M02 — ลบรูปปก → รูปแรกเป็นปกอัตโนมัติ (edge: EC-07)
- group: M · trace: EC-07 · Setup: ต่อจาก TC-M01 (มีรูป ≥2 และปกอยู่รูปที่ 2)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนลบ บนรูปที่เป็นปก | — | รูปหาย + badge ปกย้ายไปรูปแรกที่เหลืออัตโนมัติ | ☐ |

### TC-M03 — เอกสารแนบ: เพิ่ม/ลบ + empty state
- group: M · trace: H-11 · Setup: role=product_manager · seed=record ที่ไม่มีเอกสารแนบ
- Start: view record → แท็บ **รูปภาพ & เอกสาร**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ส่วนเอกสารแนบ (เมื่อว่าง) | — | ข้อความ **ยังไม่มีเอกสารแนบ** | ☐ |
| 2 | CLICK **แก้ไข** → ขั้น 4 → CLICK แนบเอกสาร (mock) | — | รายการไฟล์ปรากฏ (ชื่อ+ชนิด+ขนาด) | ☐ |

---

### กลุ่ม U — Routing / UX

### TC-U01 — Esc chain: modal → drawer → list
- group: U · trace: AC-19 · Setup: role=product_manager · seed=FG-1030 (ใช้งาน)
- Start: OPEN view FG-1030 → CLICK **จัดเก็บ** (เปิด modal ทับ view)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS Esc | — | **modal ปิดก่อน** — view ยังเปิดอยู่ | ☐ |
| 2 | PRESS Esc | — | view ปิด กลับ `#/products` | ☐ |

### TC-U02 — modal-over-view: ยกเลิกแล้วกลับ view คงแท็บเดิม
- group: U · ความสำคัญ: สูง · trace: AC-19 / H-12 · Setup: role=product_manager · seed=FG-1030
- Start: OPEN view FG-1030

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ราคา** | — | แท็บราคา active | ☐ |
| 2 | CLICK **จัดเก็บ** | — | modal จัดเก็บทับ view (route `/archive/`) | ☐ |
| 3 | CLICK ปุ่ม **ยกเลิก** ใน modal | — | กลับ view เดิม + **แท็บยังอยู่ที่ ราคา** + route กลับ `/view/` | ☐ |

### TC-U03 — refresh-safe: reload ที่ view/create แล้ว state เดิม
- group: U · trace: AC-19 · Setup: role=product_manager
- Start: OPEN view FG-1001

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS F5 (reload หน้า) ขณะ route `/view/` | — | โหลดแล้ว view FG-1001 เปิดเหมือนเดิม (hash routing ทำงาน) — หมายเหตุ: ข้อมูล mock reset เป็น seed | ☐ |
| 2 | OPEN `#/products/create` ตรง ๆ | — | wizard เปิดขั้น 1 | ☐ |

### TC-U04 — ปิด wizard 3 ทาง (Esc / ปุ่มยกเลิก / X)
- group: U · trace: UX standard · Setup: role=product_manager
- Start: OPEN `#/products/create`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS Esc | — | drawer ปิด กลับ list | ☐ |
| 2 | OPEN `#/products/create` → CLICK ปุ่ม **ยกเลิก** (footer) | — | drawer ปิด | ☐ |
| 3 | OPEN `#/products/create` → CLICK **X** มุม header | — | drawer ปิด | ☐ |

### TC-U05 — กระดิ่งแจ้งเตือน = placeholder F-NT
- group: U · trace: H-13 / 01_UI §1.5 · Setup: role=product_manager
- Start: OPEN `#/products`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ไอคอนกระดิ่งบน shell-bar | — | **ไม่มีจุดแดง** (ไม่มี notification จริง) | ☐ |
| 2 | CLICK ไอคอนกระดิ่ง | — | toast **ศูนย์แจ้งเตือนจะเชื่อมกับ Notification Center (F-NT) ภายหลัง** | ☐ |

---

### กลุ่ม X — Cross-module (XT — ทั้งหมด "ต้อง simulate": prototype ไม่มีหน้า module ปลายทาง)

### TC-X01 — XT-01: threshold event ไป Inventory Monitoring (ต้อง simulate)
- group: X · trace: XT-01 / LD-03 / contract `PRODUCT_STOCK_THRESHOLD v1` · Setup: role=product_manager · seed=สภาพแวดล้อมจริงที่มี event bus + consumer Inventory Monitoring (prototype: เช็คได้แค่ฝั่งต้นทาง)
- Start: แก้ min/max ของ record ใช้งาน (TC-V04 flow ใส่ Min 50 / Max 500) → บันทึก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ฝั่งต้นทาง) view → ภาพรวม → แจ้งเตือนระดับสต็อก | — | ค่า Min/Max ใหม่แสดง `50 PCS / 500 PCS` | ☐ |
| 2 | VERIFY (ระบบจริง) payload event `product_threshold_changed_event` | — | `{product_id, code, min_stock:50, max_stock:500, uom_base:'PCS'}` — null ด้านใด = ไม่เตือนด้านนั้น | ☐ |

### TC-X02 — XT-02: สินค้าไม่ active หายจาก picker ปลายทาง (ต้อง simulate)
- group: X · trace: XT-02 · Setup: ระบบจริงมี Sales/Purchase/BOM picker · seed=สินค้า A active อยู่ใน picker ก่อน
- Start: ทำสินค้า A → **เลิกผลิต** (TC-S01 flow)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY picker สินค้าในเอกสารขาย/ซื้อ/BOM (module ปลายทาง) | — | สินค้า A **ไม่ปรากฏ** ใน picker (กรอง status=active) | ☐ |

### TC-X03 — XT-03: archive ไม่ทำ FK เอกสารเก่าพัง (ต้อง simulate)
- group: X · trace: XT-03 / BR-PDM-08 · Setup: ระบบจริง — สินค้า B มี transaction ในเอกสารเดิม · seed=SO/PO เก่าอ้างสินค้า B
- Start: จัดเก็บสินค้า B (TC-S06 flow ยืนยันจริง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY เอกสารเก่าที่อ้างสินค้า B | — | เปิดดูได้ปกติ ชื่อ/รหัสสินค้ายังแสดง (soft delete — FK ไม่พัง) | ☐ |

---

### กลุ่ม A — AI-DEFAULT (concurrency/idempotency — ต้อง simulate ที่ระบบจริง/API)

### TC-A01 — [AI-DEFAULT] concurrent amend → 409 (ต้อง simulate)
- group: A · trace: EC-01 / AC-20 · Setup: ระบบจริง 2 sessions role=canManage · seed=record ใช้งาน 1 ตัว
- Start: เปิด edit record เดียวกัน 2 sessions

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | Session 1 บันทึกก่อน | — | สำเร็จ version+1 | ☐ |
| 2 | Session 2 บันทึกตาม (If-Match version เก่า) | — | ถูกปฏิเสธ 409 **ERR_STALE_DATA** — UI แจ้งข้อมูลถูกแก้โดยผู้อื่น ⚠ ยืนยัน anchor (ข้อความ UI จริงยังไม่กำหนด) | ☐ |

### TC-A02 — [AI-DEFAULT] idempotency key ซ้ำ (ต้อง simulate)
- group: A · trace: EC-02 / AC-20 · Setup: ระบบจริง — ยิง POST /products ซ้ำ key เดิม body เดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ยิง request แรก | — | 201 สร้าง record | ☐ |
| 2 | ยิงซ้ำ key เดิม body เดิม | — | response เดิม (ไม่สร้างซ้ำ — จำนวน record ไม่เพิ่ม) | ☐ |

### TC-A03 — [AI-DEFAULT] genCode race (ต้อง simulate)
- group: A · trace: EC-06 · Setup: ระบบจริง — ยิง create type เดียวกันพร้อมกัน 2 requests

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ยิง create FG พร้อมกัน 2 ตัว | — | ได้รหัสไม่ซ้ำกัน 2 ตัว (retry on conflict ทำงาน) — ไม่มี 500 | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `product-master.html` ใน browser (viewport ≥1366 กว้าง) — รอ icon/font โหลด ~1-2s
2. รันทีละเคสตามลำดับกลุ่ม (L → C → V → E → S → W → P → B → M → U) — **ทุกเคสเริ่มที่ `Start` ของตัวเอง** ไม่พึ่งสถานะเคสก่อน ยกเว้นระบุ "ต่อจาก TC-xx"
3. ⚠ prototype เป็น mock in-memory: **refresh = ข้อมูล reset เป็น seed** — เคสที่สร้าง state ต่อเนื่อง (S04→S05) ให้รันติดกันไม่ refresh คั่น
4. เคส mark **(ต้อง simulate)** (P01/P02, X, A, L07, S03): ถ้า runner เตรียมสภาพไม่ได้ → รายงาน `blocked` พร้อมเหตุผล — อย่าเดา pass
5. ทุก step ติ๊ก Result: ผ่าน=`✓` ไม่ผ่าน=`✗` + จดสิ่งที่เห็นจริงลง evidence
6. จบทุกเคสแล้วกรอก **Result Report** ตาม schema ท้ายไฟล์

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FR/AC (06_TESTS AC-01..20) | 20 / 20 |
| Business rules (BR-PDM-01..10) | 10 / 10 |
| Edge cases (EC-01..08) | 8 / 8 (3 ตัว = simulate) |
| Error codes (จอ prototype สังเกตได้) | 8 / 8 · API-level 4 ตัว = simulate/ข้าม (BR_BAD_TYPE, ERR_4xx ทั่วไป) |
| Permission cells สำคัญ | 3 / 3 (2 ตัว simulate role switch) |
| State transitions (ถูก 6 + ผิด 2 ตัวแทน) | 8 / 8 |
| UI states (loaded/empty/filtered-empty/loading) | 4 / 4 (L07 empty แท้ = simulate) |
| Cross-Module (XT) | **3 / 3** (ทั้งหมด simulate — prototype ไม่มีปลายทาง) |
| Scope Lock / LD verify | **4 / 6** — LD-02 (data-level), LD-06 บางส่วน = ตรวจที่ dev/DB |
| **Manifest cross-check (FRD §0.12 H-01..H-14)** | **✅ 14/14** — ทุกแถวมีเคสใน Ledger |

### ข้าม (พร้อมเหตุผล)
- `BR_BAD_TYPE` (bulk) — sample บนจอไม่มีแถว type ผิด → เทสที่ BE/API ตอน dev
- `ERR_VALIDATION_FAILED / 401 / 403 / 404 / ERR_DUPLICATE_IDEMPOTENCY_KEY / ERR_STALE_DATA` ระดับ HTTP — prototype ไม่มี server (A-group คุม 2 ตัวหลังแบบ simulate)
- LD-02 DOA placeholder — data-level ไม่มีผลบนจอ (dev ตรวจ payload/schema)
- Lot/Serial/Expiry/regulated — Out of Scope v6 (OQ-04/05)

## Result Report (schema)

```json
{
  "feature_id": "F-PRODUCT-MASTER-001",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 61, "pass": 0, "fail": 0, "blocked": 0 }
}
```
