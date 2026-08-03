# AI Test Cases — F-VENDOR-PRICELIST-001 Vendor Price List

เอกสารนี้เป็นคำสั่งทดสอบแบบมองเห็นได้สำหรับ AI browser agent โดยยึด HTML ปัจจุบันเป็น UI source of truth และยึด FRD Pack เป็นกติกาธุรกิจ/ระบบ; จุดที่ต้นแบบพิสูจน์ไม่ได้ถูกแยกเป็น simulation อย่างชัดเจน

## Meta

| รายการ | ค่า |
|---|---|
| Feature | F-VENDOR-PRICELIST-001 — Vendor Price List (buy-side) |
| Feature ID | F-VENDOR-PRICELIST-001 |
| ชื่อ | Vendor Price List |
| เวอร์ชัน | Test pack v1.0 · BRD v2.4 · FRD v1.0 |
| App entry | `outputs/F-VENDOR-PRICELIST-001/vendor-price-list-v6.html#/vendor-price-list` |
| Routes | `#/vendor-price-list`, `#/vendor-price-list/vendor/:vendorId`, `#/vendor-price-list/batch`, `#/vendor-price-list/compare` |
| เอกสารต้นทาง | `BRD_VendorPriceList_v2.4.md` (APPROVED), `FRD_F-VENDOR-PRICELIST-001_Pack/`, `vendor-price-list-v6.html`, `UI_BRIEF_F-VENDOR-PRICELIST-001.md` |
| HTML source of truth | `outputs/F-VENDOR-PRICELIST-001/vendor-price-list-v6.html` |
| Vendor master | `outputs/F-VENDOR/_final-docs` |
| Product master | `Related context/Item Master` |
| ผู้รันเป้าหมาย | AI browser agent; เคสที่ระบุ “ต้อง simulate” ต้องใช้ test fixture/API harness ประกอบ |
| วันที่จัดทำ | 3 ส.ค. 2569 |
| ระดับ pack | FULL |
| จำนวนเคส/หมวด | 62 เคส · 8 หมวด (A–H) · P0 57 · P1 5 |
| กติกาหลัก | ใช้ข้อความที่เห็นบนจอเป็น anchor; ห้ามใช้ CSS selector/ชื่อฟังก์ชันเป็น action; refresh ก่อนแต่ละเคส เว้นแต่ Setup ระบุเป็นอย่างอื่น |

## Coverage

| Group | ขอบเขต | เคส | ความสำคัญ |
|---|---|---:|---|
| A | รายการ การนำทาง route, scope และ keyboard | 8 | สูง 5 · กลาง 3 |
| B | สร้าง/แก้ไข/master/field validation | 11 | สูง 10 · กลาง 1 |
| C | Approval, SoD, version, threshold, lifecycle | 12 | สูง 12 |
| D | Batch Entry | 5 | สูง 5 |
| E | Import preview/commit/idempotency | 7 | สูง 6 · กลาง 1 |
| F | Compare, calculation, resolve | 7 | สูง 7 |
| G | Permission, Confidential, concurrency | 5 | สูง 5 |
| H | Cross-module XT | 7 | สูง 7 |

รวมครอบคลุม Acceptance Criteria 16/16, Business Rules 21/21, Edge Cases 16/16, Cross-module Tests 7/7, Scope Locks 17/17, state 5 แบบ, route จริง 4 route + unknown route และ happy/negative/boundary/error/permission ครบ ข้อความ Expected ยึด HTML เช่น `สร้างรายการราคา`, `บันทึกร่าง`, `ยืนยันและส่งอนุมัติ`, `รออนุมัติ`, `ยืนยันนำเข้า`, `คำนวณ`; สิ่งที่ต้นแบบพิสูจน์ไม่ได้มี marker `⚠ ไม่พบใน HTML`/`(ต้อง simulate)`

## Coverage Ledger

สถานะ `COVERED` หมายถึงมี test case ด้านล่าง; `SCOPE-AUDIT` หมายถึงตรวจว่า UI ไม่มีความสามารถนอกขอบเขต; `SIMULATE` หมายถึงต้องใช้ระบบจริง/API harness เพราะ HTML ไม่สามารถพิสูจน์ได้

### 3.1 Acceptance Criteria

| Requirement | สถานะ | Test case |
|---|---|---|
| AC-01 List, filter, vendor drill-in | COVERED | TC-NAV-01..05 |
| AC-02 Create draft from list/vendor context | COVERED | TC-CRT-01, TC-NAV-05 |
| AC-03 Submit new price | COVERED | TC-CRT-02 |
| AC-04 Threshold behavior | COVERED/SIMULATE | TC-APR-06..08 |
| AC-05 Approval and SoD | COVERED | TC-APR-01..03 |
| AC-06 Reject and edit | COVERED | TC-APR-04..05 |
| AC-07 New version and immutable identity | COVERED | TC-APR-09..10, TC-CRT-11 |
| AC-08 Batch validation | COVERED | TC-BAT-01..04 |
| AC-09 Batch success | COVERED | TC-BAT-05 |
| AC-10 Import preview | COVERED | TC-IMP-01..04 |
| AC-11 Import commit/modes | COVERED/SIMULATE | TC-IMP-05..07 |
| AC-12 Compare | COVERED | TC-CMP-01..05 |
| AC-13 Resolve and snapshot | SIMULATE | TC-CMP-06..07, TC-XT-06..07 |
| AC-14 Confidential masking | SIMULATE | TC-SEC-03..05 |
| AC-15 Deactivate/reactivate | COVERED | TC-APR-11..12 |
| AC-16 Concurrency/idempotency | SIMULATE | TC-SEC-01..02 |

### 3.2 Business Rules

| Rule | สถานะ | Test case |
|---|---|---|
| BR-VPL-01 unique Header scope | SIMULATE | TC-CRT-10 |
| BR-VPL-02 active F-VENDOR only | COVERED | TC-CRT-03, TC-XT-01 |
| BR-VPL-03 active+purchasable Product only | COVERED | TC-CRT-04, TC-XT-02 |
| BR-VPL-04 positive price/price_per and non-negative landed cost | COVERED/SIMULATE | TC-CRT-06 |
| BR-VPL-05 vendor currency default, editable before create | COVERED | TC-CRT-01, TC-CRT-08 |
| BR-VPL-06 purchase UOM only | COVERED | TC-CRT-05 |
| BR-VPL-07 tax default from Product | COVERED | TC-CRT-08 |
| BR-VPL-08 tier ordering/no overlap | SIMULATE | TC-CMP-04 |
| BR-VPL-09 landed ex-tax formula and trace | COVERED/SIMULATE | TC-CMP-02, TC-CMP-06 |
| BR-VPL-10 effective_from and open-ended display | COVERED | TC-CRT-07 |
| BR-VPL-11 every version pending; threshold routes tier | COVERED/SIMULATE | TC-CRT-02, TC-APR-06..08 |
| BR-VPL-12 Maker ≠ Approver | COVERED | TC-APR-02..03 |
| BR-VPL-13 Confidential projection | SIMULATE | TC-SEC-03..05 |
| BR-VPL-14 non-active vendor excluded; history retained | SIMULATE | TC-XT-01 |
| BR-VPL-15 common qty/date/FX and ascending landed target | COVERED | TC-CMP-01..03 |
| BR-VPL-16 resolve explicit vendor; compare ranks many vendors | SIMULATE | TC-CMP-05..07 |
| BR-VPL-17 WORM history | SIMULATE | TC-APR-01, TC-APR-04, TC-SEC-01 |
| BR-VPL-18 one-business-day SLA and escalation | SIMULATE | TC-APR-08 |
| BR-VPL-19 one applicable answer | SIMULATE | TC-CMP-04, TC-CMP-07 |
| BR-VPL-20 PR/RFQ/PO snapshot immutable | SIMULATE | TC-XT-06 |
| BR-VPL-21 Contract > VPL > manual override | SIMULATE | TC-XT-07 |

### 3.3 Edge Cases

| Edge | สถานะ | Test case |
|---|---|---|
| EC-01 duplicate scope | SIMULATE | TC-CRT-10 |
| EC-02 vendor changes state after selection | SIMULATE | TC-XT-01 |
| EC-03 tier overlap | SIMULATE | TC-CMP-04 |
| EC-04 price ≤0/net negative | COVERED/SIMULATE | TC-CRT-06 |
| EC-05 batch blank/incomplete row | COVERED | TC-BAT-02..03 |
| EC-06 CSV unmatched master | COVERED | TC-IMP-03 |
| EC-07 missing change reason | COVERED | TC-CRT-09 |
| EC-08 own approval | COVERED | TC-APR-02 |
| EC-09 discount/freight invalid | COVERED | TC-CRT-06 |
| EC-10 missing/stale FX | SIMULATE | TC-CMP-03, TC-XT-05 |
| EC-11 concurrent update/approval | SIMULATE | TC-SEC-01 |
| EC-12 existing pending version | SIMULATE | TC-APR-10 |
| EC-13 inactive Header excluded | COVERED | TC-CMP-05 |
| EC-14 no applicable price | COVERED/SIMULATE | TC-CMP-05, TC-CMP-07 |
| EC-15 unauthorized export/log/print | SIMULATE | TC-SEC-04..05 |
| EC-16 scoped service vs UI mask | SIMULATE | TC-SEC-03 |

### 3.4 Field and Cross-field Validation

| Field/action | สถานะ | Test case |
|---|---|---|
| identity unique | SIMULATE | TC-CRT-10 |
| vendor_id same tenant/live active | COVERED/SIMULATE | TC-CRT-03, TC-XT-01 |
| product_id active+purchasable | COVERED/SIMULATE | TC-CRT-04, TC-XT-02 |
| buy_uom current purchase UOM | COVERED | TC-CRT-05 |
| price > 0 | COVERED | TC-CRT-06 |
| price_per > 0 | SIMULATE | TC-CRT-06 |
| discount_pct 0..100 | COVERED | TC-CRT-06 |
| freight >= 0 | COVERED | TC-CRT-06 |
| effective range | COVERED | TC-CRT-07 |
| tiers ordered/no overlap | SIMULATE | TC-CMP-04 |
| change reason required | COVERED | TC-CRT-09 |
| approval route + SoD | COVERED/SIMULATE | TC-APR-02..03, TC-APR-06..08 |
| Active overlap exactly one answer | SIMULATE | TC-CMP-04 |
| batch row blank ignored/started complete | COVERED | TC-BAT-02..03 |

### 3.5 Error Catalog

| Code | สถานะ | Test case |
|---|---|---|
| `ERR_VALIDATION_FAILED` | COVERED/SIMULATE | TC-CRT-06..09, TC-BAT-03 |
| `ERR_NOT_AUTHENTICATED` | SIMULATE | TC-SEC-03 |
| `ERR_INSUFFICIENT_ROLE` | SIMULATE | TC-SEC-03 |
| `ERR_PERMISSION_REVOKED` | SIMULATE | TC-SEC-03 |
| `ERR_VPL_NOT_FOUND` | SIMULATE | TC-NAV-07 |
| `ERR_STALE_DATA` | SIMULATE | TC-SEC-01 |
| `ERR_IDEMPOTENCY_CONFLICT` | SIMULATE | TC-SEC-02 |
| `ERR_ALREADY_DECIDED` | SIMULATE | TC-SEC-01 |
| `BR_VPL_DUPLICATE_HEADER` | SIMULATE | TC-CRT-10 |
| `BR_VENDOR_NOT_ACTIVE` | COVERED/SIMULATE | TC-CRT-03, TC-XT-01 |
| `BR_PRODUCT_NOT_PURCHASABLE` | COVERED/SIMULATE | TC-CRT-04, TC-XT-02 |
| `BR_UOM_NOT_PURCHASABLE` | COVERED | TC-CRT-05 |
| `BR_PRICE_INVALID` | COVERED/SIMULATE | TC-CRT-06 |
| `BR_DISCOUNT_INVALID` | COVERED/SIMULATE | TC-CRT-06 |
| `BR_FREIGHT_INVALID` | COVERED/SIMULATE | TC-CRT-06 |
| `BR_DATE_RANGE_INVALID` | COVERED | TC-CRT-07 |
| `BR_TIER_OVERLAP` | SIMULATE | TC-CMP-04 |
| `BR_ACTIVE_PRICE_OVERLAP` | SIMULATE | TC-CMP-04 |
| `BR_REASON_REQUIRED` | COVERED | TC-CRT-09 |
| `BR_PENDING_VERSION_EXISTS` | SIMULATE | TC-APR-10 |
| `BR_DOA_ROUTE_NOT_FOUND` | SIMULATE | TC-APR-08 |
| `BR_SOD_VIOLATION` | COVERED | TC-APR-02 |
| `NO_APPLICABLE_PRICE` | COVERED/SIMULATE | TC-CMP-05, TC-CMP-07 |
| `BR_PRICE_AMBIGUOUS` | SIMULATE | TC-CMP-04 |
| `ERR_FX_UNAVAILABLE` | SIMULATE | TC-CMP-03, TC-XT-05 |
| `ERR_PREVIEW_EXPIRED` | SIMULATE | TC-IMP-07 |
| `ERR_UPSTREAM_UNAVAILABLE` | SIMULATE | TC-XT-01..05 |

### 3.6 Permission Matrix

| Cell | สถานะ/Test case |
|---|---|
| procurement_officer × View = allow | TC-SEC-03 |
| procurement_officer × See price = allow | TC-SEC-03 |
| procurement_officer × Create/Edit/Import = allow | TC-SEC-03 |
| procurement_officer × Submit = allow | TC-SEC-03 |
| procurement_officer × Approve/Reject = deny | TC-SEC-03 |
| procurement_officer × Activate/Deactivate = allow | TC-SEC-03 |
| procurement_manager × View = allow | TC-SEC-03 |
| procurement_manager × See price = allow | TC-SEC-03 |
| procurement_manager × Create/Edit/Import = allow | TC-SEC-03 |
| procurement_manager × Submit = allow | TC-SEC-03 |
| procurement_manager × Approve/Reject = DOA+SoD | TC-APR-01..03 |
| procurement_manager × Activate/Deactivate = allow | TC-SEC-03 |
| procurement_director × View = allow | TC-SEC-03 |
| procurement_director × See price = allow | TC-SEC-03 |
| procurement_director × Create/Edit/Import = allow | TC-SEC-03 |
| procurement_director × Submit = allow | TC-SEC-03 |
| procurement_director × Approve/Reject = DOA+SoD | TC-APR-08 |
| procurement_director × Activate/Deactivate = allow | TC-SEC-03 |
| finance_viewer × View = allow | TC-SEC-03 |
| finance_viewer × See price = allow | TC-SEC-03 |
| finance_viewer × Create/Edit/Import = deny | TC-SEC-03 |
| finance_viewer × Submit = deny | TC-SEC-03 |
| finance_viewer × Approve/Reject = deny | TC-SEC-03 |
| finance_viewer × Activate/Deactivate = deny | TC-SEC-03 |
| admin × View = allow | TC-SEC-03 |
| admin × See price = allow | TC-SEC-03 |
| admin × Create/Edit/Import = allow | TC-SEC-03 |
| admin × Submit = allow | TC-SEC-03 |
| admin × Approve/Reject = DOA+SoD | TC-APR-03 |
| admin × Activate/Deactivate = allow | TC-SEC-03 |
| other authenticated × View = allow | TC-SEC-03 |
| other authenticated × See price = masked | TC-SEC-03..05 |
| other authenticated × Create/Edit/Import = deny | TC-SEC-03 |
| other authenticated × Submit = deny | TC-SEC-03 |
| other authenticated × Approve/Reject = deny | TC-SEC-03 |
| other authenticated × Activate/Deactivate = deny | TC-SEC-03 |
| downstream service × View = scoped | TC-SEC-05 |
| downstream service × See price = scoped | TC-SEC-03, TC-SEC-05 |
| downstream service × Create/Edit/Import = deny | TC-SEC-03 |
| downstream service × Submit = deny | TC-SEC-03 |
| downstream service × Approve/Reject = deny | TC-SEC-03 |
| downstream service × Activate/Deactivate = deny | TC-SEC-03 |

### 3.7 Cross-module Tests

| ID | สถานะ | Test case |
|---|---|---|
| XT-01 Vendor lifecycle drift | SIMULATE | TC-XT-01 |
| XT-02 Product lifecycle/purchasable drift | SIMULATE | TC-XT-02 |
| XT-03 F-VENDOR API-20 summary façade | SIMULATE | TC-XT-03 |
| XT-04 DOA config changes after submit | SIMULATE | TC-XT-04 |
| XT-05 FX missing/stale | SIMULATE | TC-XT-05 |
| XT-06 PR/RFQ/PO snapshot | SIMULATE | TC-XT-06 |
| XT-07 source precedence | SIMULATE | TC-XT-07 |

### 3.8 Scope Locks and Coverage Manifest

| Lock | สถานะ | Test case/evidence |
|---|---|---|
| LOCK-VPL-01 buy-side only | SCOPE-AUDIT | TC-NAV-06 |
| LOCK-VPL-02 old artifacts not authority | SCOPE-AUDIT/SIMULATE | TC-NAV-06 |
| LOCK-VPL-03 all create/version require approval | COVERED | TC-CRT-02, TC-APR-06..10 |
| LOCK-VPL-04 threshold config, absolute landed ex-tax change | SIMULATE | TC-APR-06..08 |
| LOCK-VPL-05 central DOA + 1-day SLA | SIMULATE | TC-APR-08 |
| LOCK-VPL-06 Confidential/masking | SIMULATE | TC-SEC-03..05 |
| LOCK-VPL-07 immutable Header/version identity | COVERED | TC-APR-09, TC-CRT-11 |
| LOCK-VPL-08 no ambiguous active answer | SIMULATE | TC-CMP-04 |
| LOCK-VPL-09 downstream calculation snapshot | SIMULATE | TC-XT-06 |
| LOCK-VPL-10 page/drawer/modal patterns | COVERED | TC-NAV-01, TC-NAV-08 |
| LOCK-VPL-11 batch/CSV preview/external ID | COVERED/SIMULATE | TC-BAT-01..05, TC-IMP-01..07 |
| LOCK-VPL-12 no AVL/contract editor/etc. | — ข้าม: นอกขอบเขตใบเซ็น; ห้ามสร้างเคสของฟังก์ชันเหล่านี้ | — |
| LOCK-VPL-13 no business A4/PDF | — ข้าม: นอกขอบเขตใบเซ็น; ห้ามสร้างเคส PDF | — |
| LOCK-VPL-14 Vendor source = `outputs/F-VENDOR/_final-docs` | COVERED/SIMULATE | TC-CRT-03, TC-XT-01 |
| LOCK-VPL-15 canonical feature ID only | SCOPE-AUDIT/SIMULATE | TC-NAV-06 |
| LOCK-VPL-16 VPL owns data; Vendor API-20 façade | SIMULATE | TC-XT-03 |
| LOCK-VPL-17 Product UUID/master/purchase UOM | COVERED/SIMULATE | TC-CRT-04..05, TC-XT-02 |

### 3.9 Cross-cutting, Events and States

| Item | สถานะ | Test case |
|---|---|---|
| State `draft` / UI `ร่าง` | COVERED | TC-CRT-01, TC-APR-04..05 |
| State `pending_approval` / UI `รออนุมัติ` | COVERED | TC-CRT-02, TC-BAT-05, TC-IMP-05 |
| State `active` / UI `ใช้งาน` | COVERED | TC-APR-01, TC-APR-09 |
| State `inactive` / UI `ปิดใช้งาน` | COVERED | TC-APR-11..12 |
| State `rejected` / UI `ปฏิเสธ` history | COVERED/SIMULATE | TC-APR-04 |
| `vendor_price_submitted_event` | SIMULATE | TC-CRT-02, TC-BAT-05, TC-IMP-05 |
| `vendor_price_approved_event` | SIMULATE | TC-APR-01 |
| `vendor_price_rejected_event` | SIMULATE | TC-APR-04 |
| `vendor_price_availability_changed_event` | SIMULATE | TC-APR-11..12 |
| consume `vendor_status_changed_event` | SIMULATE | TC-XT-01 |
| consume `product_status_changed_event` | SIMULATE | TC-XT-02 |
| RLS cross-tenant/company scope | SIMULATE | TC-SEC-05 |
| WORM history | SIMULATE | TC-APR-01, TC-APR-04 |
| idempotency + retry | SIMULATE | TC-SEC-02, TC-IMP-07 |
| optimistic concurrency | SIMULATE | TC-SEC-01 |
| loading/submitting state | COVERED | TC-CRT-02, TC-BAT-05, TC-IMP-05, TC-CMP-01 |
| empty list/filter/compare | COVERED | TC-NAV-03, TC-CMP-05 |

Coverage Manifest cross-check: Stories S-01..S-05 → AC-01..16 → cases above 5/5; Rules BR-VPL-01..21 → cases above 21/21; Edges EC-01..16 → cases above 16/16. ไม่มี `[AI-DEFAULT]` tag ใน FRD pack นี้ จึงไม่มี default ที่ต้อง propagate เพิ่ม

## Data Sets

| ID | ข้อมูล/ไฟล์ | ใช้กับ |
|---|---|---|
| DS-UI | fixture ที่มากับ `vendor-price-list-v6.html`: vendor/product/VPL หลายสถานะ | flow ที่ทดสอบจากต้นแบบ |
| DS-MASTER | vendor active/non-active สกุล THB/USD จาก F-VENDOR; product active+purchasable/non-purchasable/obsolete พร้อมหลาย purchase UOM | create, batch, compare, XT |
| DS-PRICE | draft/pending/active/inactive; flat/tier; finite/open-ended; same Header มี pending อยู่แล้ว | approval, lifecycle, resolve |
| DS-ROLE | procurement_officer, procurement_manager, procurement_director, finance_viewer, admin, other authenticated, downstream service | permission/SoD |
| DS-FX | dated fresh FX, missing FX, stale FX เกิน policy | compare/resolve |
| DS-CSV-OK | `vpl-valid-4-rows.csv` UTF-8 คอลัมน์ตรง Template | import happy path |
| DS-CSV-MASTER | `vpl-unmatched-master.csv` มี vendor/product/UOM ไม่ตรง master | import negative |
| DS-CSV-ID | `vpl-duplicate-external-id.csv` มี external ID ซ้ำทั้ง same/different content | import retry/conflict |
| DS-CSV-SCHEMA | `vpl-invalid-header.csv`, `vpl-invalid-encoding.csv` | schema/encoding |
| DS-CSV-SAFE | `vpl-formula-like-cell.csv` มีค่าขึ้นต้น `=`, `+`, `-`, `@` | export/import safety |
| DS-CONC | ผู้ใช้สอง session เปิด record/version เดียวกันพร้อม ETag เดียวกัน | concurrency |
| DS-XT | deterministic mocks ของ Vendor/Product/DOA/FX/PR/RFQ/PO/Contract | cross-module |

### ไฟล์ทดสอบ (Files)

| ชื่อไฟล์ที่ runner ต้องเตรียม | เนื้อหา/ผลที่ต้องการ |
|---|---|
| `vpl-valid-4-rows.csv` | UTF-8, header ตรง Template, 4 แถวผ่าน master validation |
| `vpl-unmatched-master.csv` | มี vendor/product/UOM ที่ไม่ตรง canonical master |
| `vpl-duplicate-external-id.csv` | external ID ซ้ำทั้ง content เดิมและ content ต่าง |
| `vpl-invalid-header.csv` | ชื่อ/จำนวนคอลัมน์ไม่ตรง Template |
| `vpl-invalid-encoding.csv` | encoding ที่ระบบไม่รองรับ |
| `vpl-formula-like-cell.csv` | cell text ขึ้นต้น `=`, `+`, `-`, `@` เพื่อทดสอบ formula injection |

### ชุด A — สร้างรายการที่ถูกต้องจาก fixture ปัจจุบัน

| ฟิลด์ | ค่า |
|---|---|
| คู่ค้า | `V-TH-MN-00001 · บริษัท สตีลโปร จำกัด` (active, THB) |
| สินค้า | `PM-4001 · กล่องลูกฟูก 5 ชั้น 60x40x40` (active+purchasable) |
| Purchase UOM | `BOX` |
| สกุลเงิน | `THB` |
| ประเภทราคา | ราคาคงที่ |
| ราคาตั้ง / ราคาต่อจำนวน | `295.00 / 1` |
| ส่วนลด / ค่าขนส่งต่อหน่วย | `0 / 0.50` |
| ภาษีซื้อ | `VAT7` |
| เริ่มใช้ / สิ้นสุด | `2026-08-15 / ว่าง` |
| เหตุผล | `ปรับราคาตามใบเสนอราคาล่าสุด` |

### ชุด B — Master ที่ต้องถูกปฏิเสธ

| ฟิลด์ | ค่า |
|---|---|
| vendor pending KYC | `V-TH-TR-00002 · บริษัท แพ็คเกจจิ้งดี` |
| vendor blocked | `V-TH-TR-00003 · บริษัท โกลบอลเทรด จำกัด` |
| vendor inactive | `V-TH-TR-00005 · บริษัท เก่าเลิกกิจการ` |
| vendor blacklisted | `V-TH-TR-00006 · บริษัท แบล็คลิสต์ จำกัด` |
| product non-purchasable | `FG-1010 · เก้าอี้สำนักงาน ergonomic` |
| invalid UOM for PM-4001 | `KG` (หน่วยที่ถูกต้องคือ PCS/BOX/PALLET) |

### ชุด C — Compare ที่ตรวจตัวเลขได้จากต้นแบบ

| ฟิลด์ | ค่า |
|---|---|
| สินค้า | `RM-2001 · ไม้สักแปรรูป เกรด A` |
| ปริมาณ | `1,000 KG` |
| วันที่ | `2026-08-20` |
| สกุลเงินเป้าหมาย | `THB` |
| FX fixture | THB=1, USD=36.40, EUR=39.10, CNY=5.02 |
| candidate อ้างอิง | VPL-001, VPL-009; VPL-005 ต้องถูกตัดเพราะ inactive |

### ชุด D — Boundary และค่าผิด

| ฟิลด์ | ค่า |
|---|---|
| price / price_per invalid | `0`, `-0.01` |
| discount invalid/boundary | `-0.01`, `0`, `100`, `100.01` |
| freight invalid/boundary | `-0.01`, `0` |
| date invalid | from=`2026-08-10`, to=`2026-08-09` |
| threshold boundaries | absolute landed change `9.99%`, `10.00%`, `10.01%` |
| known formula | price=120, price_per=12, discount=10%, freight=2 → landed=11.00 |

### ชุด E — Threshold fixture ที่กรอกตัวเลขได้ตรง

| ฟิลด์ | ค่า |
|---|---|
| active baseline | landed ex-tax=`100.00`, price_per=1, discount=0, freight=0 |
| below threshold | price=`109.99` → change=`+9.99%` |
| equal threshold | price=`110.00` → change=`+10.00%` |
| above threshold | price=`110.01` → change=`+10.01%` |

## Test Cases

### กลุ่ม A — รายการ การนำทาง และ UX พื้นฐาน

#### TC-NAV-01 — เปิดหน้ารายการและเห็นข้อมูลหลักครบ

- Group/Priority/Trace: Navigation · P0 · AC-01, LOCK-VPL-10
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-UI · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-UI
- Pass criteria: หน้าโหลดเป็นรายการราคา แสดงรหัสคู่ค้าและรหัสสินค้าเต็ม พร้อม action หลัก

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN route `#/vendor-price-list` | — | เห็นหัวข้อ `รายการราคาคู่ค้า` และคำอธิบาย `จัดการราคาซื้อที่ผ่านการอนุมัติ พร้อมประวัติราคาและรายละเอียดการคำนวณ` | ☐ |
| 2 | VERIFY แถบคำสั่งด้านบน | — | เห็น `Import`, `Batch Entry`, `เปรียบเทียบราคา`, `สร้างรายการราคา` | ☐ |
| 3 | VERIFY ตารางรายการ | — | แต่ละแถวเห็นชื่อพร้อมรหัสคู่ค้าเต็ม ชื่อพร้อมรหัสสินค้าเต็ม สถานะ และช่วงมีผล; ไม่มีข้อความล้นไปทับคอลัมน์ข้างเคียง | ☐ |

#### TC-NAV-02 — ค้นหาด้วยรหัสคู่ค้าและรหัสสินค้า

- Group/Priority/Trace: Navigation · P0 · AC-01
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-UI · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-UI
- Pass criteria: ค้นด้วยรหัสเต็มแล้วเหลือเฉพาะแถวที่ตรง

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | TYPE ใน `ค้นหาคู่ค้า สินค้า หรือรหัส` | รหัสคู่ค้าที่เห็นในแถวแรก | ตารางเหลือรายการของคู่ค้ารหัสนั้น และรหัสเต็มยังอ่านได้ | ☐ |
| 2 | TYPE แทนค่าค้นหาเดิม | รหัสสินค้าที่เห็นในแถวหนึ่ง | ตารางเหลือรายการของสินค้ารหัสนั้น | ☐ |
| 3 | CLICK `ล้างตัวกรอง` | — | คำค้นหาว่างและจำนวนรายการกลับเท่า baseline ก่อนค้นหา | ☐ |

#### TC-NAV-03 — กรองสถานะและตรวจ empty state

- Group/Priority/Trace: Navigation · P0 · AC-01
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-UI · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-UI
- Pass criteria: ตัวกรองแสดงเฉพาะสถานะที่เลือกและ empty state มีทางกลับ

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | SELECT ตัวกรองสถานะ | `ร่าง` | ทุกแถวที่เหลือมี pill `ร่าง` | ☐ |
| 2 | SELECT `รออนุมัติ` → ตัวกรองสถานะ | — | ทุกแถวที่เหลือมี pill `รออนุมัติ` | ☐ |
| 3 | SELECT `ใช้งาน` → ตัวกรองสถานะ | — | ทุกแถวที่เหลือมี pill `ใช้งาน` | ☐ |
| 4 | SELECT `ปิดใช้งาน` → ตัวกรองสถานะ | — | ทุกแถวที่เหลือมี pill `ปิดใช้งาน` | ☐ |
| 5 | TYPE ใน `ค้นหาคู่ค้า สินค้า หรือรหัส` | ค่าไม่พบ `ZZZ-NOT-FOUND` | เห็น `ไม่พบรายการที่ค้นหา` และ `ล้างตัวกรอง` | ☐ |
| 6 | CLICK `ล้างตัวกรอง` | — | ตารางกลับมาและตัวกรองถูกล้าง | ☐ |

#### TC-NAV-04 — สลับมุมมองและเรียงตาราง

- Group/Priority/Trace: Navigation · P1 · AC-01
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-UI · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-UI
- Pass criteria: สลับมุมมองได้และการเรียงเปลี่ยนลำดับโดยไม่ทำข้อมูลหาย

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `แยกตามคู่ค้า` | — | ตารางเปลี่ยนเป็นรายการคู่ค้าและจำนวนรายการราคาต่อคู่ค้า | ☐ |
| 2 | CLICK หัวคอลัมน์ที่เรียงได้ | คู่ค้า | ลำดับคู่ค้าเปลี่ยน; จำนวนแถวเท่า baseline | ☐ |
| 3 | CLICK `ทุกรายการ` | — | กลับเป็นรายการราคาทีละรายการพร้อมรหัสคู่ค้าและสินค้าเต็ม | ☐ |

#### TC-NAV-05 — เจาะจากคู่ค้าและเริ่มสร้างโดยล็อกบริบทคู่ค้า

- Group/Priority/Trace: Navigation/Create · P0 · AC-01, AC-02
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-UI vendor active · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-UI
- Pass criteria: route คู่ค้าถูกต้องและ drawer สร้าง preload คู่ค้านั้น

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `แยกตามคู่ค้า` | — | ตารางเปลี่ยนเป็นรายการคู่ค้า | ☐ |
| 2 | CLICK แถวคู่ค้า active | — | route เป็น `#/vendor-price-list/vendor/{vendorId}`; เห็นชื่อและรหัสคู่ค้า | ☐ |
| 3 | CLICK `สร้างรายการราคา` | — | drawer หัวข้อ `สร้างรายการราคา` เปิด และช่อง `คู่ค้า` แสดงคู่ค้าจากหน้าก่อนหน้า | ☐ |
| 4 | PRESS `Escape` | — | drawer ปิดและยังอยู่หน้าคู่ค้าเดิม | ☐ |

#### TC-NAV-06 — ตรวจ feature identity และ source authority

- Group/Priority/Trace: Scope audit · P1 · LOCK-VPL-01/02/15
- Actor: procurement_manager
- Setup: `role=procurement_manager · seed=DS-UI · files=— · inject=build metadata/API contract fixture`
- Start route: `#/vendor-price-list`
- Data set: DS-UI
- Pass criteria: build เป็น buy-side Vendor Price List ใช้ canonical feature ID และ current pack

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | VERIFY หน้า list, drawer สร้าง, drawer ดู และหน้า compare | — | ทุกหน้าสื่อว่าเป็นราคาซื้อจากคู่ค้า ไม่ใช่ราคาขาย | ☐ |
| 2 | VERIFY metadata/API contract ของ build | — | canonical feature ID เป็น `F-VENDOR-PRICELIST-001`; legacy alias ไม่มี schema/owner แยก `⚠ ไม่ปรากฏบน UI — ต้อง simulate` | ☐ |
| 3 | VERIFY source/version ที่แนบกับ build | — | ใช้ HTML/FRD pack ปัจจุบัน; old HTML/FRD/tests เป็น reference เท่านั้น `⚠ ไม่ปรากฏบน UI — ต้องตรวจ build metadata` | ☐ |

#### TC-NAV-07 — refresh ทุก route และ unknown route

- Group/Priority/Trace: Routing · P1 · AC-01, ERR_VPL_NOT_FOUND
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-UI · files=—`
- Start route: routes ตาม step
- Data set: DS-UI
- Pass criteria: route จริง refresh ได้; unknown route มี fallback ที่สังเกตได้

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN `#/vendor-price-list` ด้วยการ refresh URL | — | เห็น `รายการราคาคู่ค้า` ไม่เป็นหน้าว่าง | ☐ |
| 2 | OPEN `#/vendor-price-list/batch` ด้วยการ refresh URL | — | เห็น `Batch Entry` ไม่เป็นหน้าว่าง | ☐ |
| 3 | OPEN `#/vendor-price-list/compare` ด้วยการ refresh URL | — | เห็น `เปรียบเทียบราคา` ไม่เป็นหน้าว่าง | ☐ |
| 4 | OPEN `#/vendor-price-list/vendor/{vendorId}` ด้วยการ refresh URL | vendor ที่มีจริง | เห็นชื่อ/รหัสคู่ค้าเดิม | ☐ |
| 5 | OPEN route ที่ไม่มีจริง | `#/vendor-price-list/not-found` | ต้นแบบปัจจุบัน fallback ไป `รายการราคาคู่ค้า`; ระบบจริงควรแสดง not-found ตาม contract — `⚠ ไม่พบใน HTML` | ☐ |

#### TC-NAV-08 — keyboard, focus และลำดับปิด overlay

- Group/Priority/Trace: Accessibility/Overlay · P0 · LOCK-VPL-10, DoD UI
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-UI · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-UI
- Pass criteria: native controls ใช้คีย์บอร์ดได้, focus มองเห็น, Escape ปิดชั้นบนก่อน

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | PRESS `Tab` ต่อเนื่องจากต้นหน้า | — | focus เดินตามลำดับอ่านและเห็นกรอบ focus ทุก control ที่ไปถึง | ☐ |
| 2 | PRESS `Enter` ที่ `สร้างรายการราคา` | — | drawer `สร้างรายการราคา` เปิด | ☐ |
| 3 | CLICK ช่อง `คู่ค้า` | — | รายการค้นหาเปิดเหนือ drawer | ☐ |
| 4 | PRESS `Escape` | — | รายการค้นหาปิดก่อน แต่ drawer ยังเปิด | ☐ |
| 5 | PRESS `Escape` อีกครั้ง | — | drawer ปิด | ☐ |
| 6 | PRESS `Enter` ที่ non-native control ซึ่งมี focus | — | ระบบจริงต้องทำงานเหมือน click; ต้นแบบอาจไม่ทำงาน `⚠ ไม่พบใน HTML` | ☐ |
| 7 | PRESS `Space` ที่ non-native control ซึ่งมี focus | — | ระบบจริงต้องทำงานเหมือน click; ต้นแบบอาจไม่ทำงาน `⚠ ไม่พบใน HTML` | ☐ |

### กลุ่ม B — สร้าง แก้ไข และตรวจข้อมูลรายการราคา

#### TC-CRT-01 — สร้างและบันทึกร่างด้วย master dropdown

- Group/Priority/Trace: Create happy path · P0 · AC-02, BR-VPL-05
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-MASTER
- Pass criteria: เลือก master ได้ ไม่พิมพ์ค่าลอย และบันทึกเป็นร่าง

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `สร้างรายการราคา` | — | drawer `สร้างรายการราคา` เปิดที่ขั้นข้อมูลรายการ | ☐ |
| 2 | TYPE ใน `ค้นหารหัสหรือชื่อคู่ค้า` | `V-TH-MN-00001` | เห็นผลลัพธ์ชื่อและรหัสคู่ค้าเต็ม | ☐ |
| 3 | SELECT `V-TH-MN-00001 · บริษัท สตีลโปร จำกัด` | — | คู่ค้าถูกเลือก; `สกุลเงิน` เริ่มต้นเป็น THB | ☐ |
| 4 | TYPE ใน `ค้นหารหัสหรือชื่อสินค้า` | `PM-4001` | เห็นผลลัพธ์ชื่อ/รหัสสินค้าเต็ม | ☐ |
| 5 | SELECT `PM-4001 · กล่องลูกฟูก 5 ชั้น 60x40x40` | — | `Purchase UOM` มีเฉพาะหน่วยซื้อของสินค้านี้ | ☐ |
| 6 | SELECT `BOX` → `Purchase UOM` | — | ช่องแสดง BOX | ☐ |
| 7 | CLICK `ถัดไป` | — | เห็นขั้น `เงื่อนไขราคา` และ `สรุปก่อนส่ง` | ☐ |
| 8 | TYPE ชุด A → ราคา/วันที่/เหตุผล | ชุด A | ไม่มีคำเตือนใต้ช่อง | ☐ |
| 9 | CLICK `บันทึกร่าง` | — | drawer ปิด เห็น toast `บันทึกร่างแล้ว` และมีแถวใหม่สถานะ `ร่าง` | ☐ |

#### TC-CRT-02 — ส่งรายการใหม่แล้วต้องเป็นรออนุมัติ

- Group/Priority/Trace: Submit happy path · P0 · AC-03, BR-VPL-11, LOCK-VPL-03
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER valid · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-MASTER
- Pass criteria: ส่งสำเร็จ กลับหน้ารายการ และสถานะเป็นรออนุมัติ ไม่ใช่ใช้งานทันที

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | VERIFY และจดจำนวนรายการ baseline | — | จดจำนวนก่อนสร้างไว้อ้างใน step 6 | ☐ |
| 2 | CLICK `สร้างรายการราคา` | — | drawer เปิด | ☐ |
| 3 | SELECT master และ UOM ตามชุด A | ชุด A | ปุ่ม `ถัดไป` ใช้งานได้ | ☐ |
| 4 | CLICK `ถัดไป` | — | เห็น `ราคาฉบับที่จะส่ง`, `สถานะหลังส่ง`, `ขั้นตอนการอนุมัติ` และสถานะหลังส่งเป็น `รออนุมัติ` | ☐ |
| 5 | TYPE ราคา/วันที่/เหตุผลตามชุด A | ชุด A | สรุปสะท้อนค่าที่กรอก | ☐ |
| 6 | CLICK `ยืนยันและส่งอนุมัติ` | — | ระหว่างส่งเห็น loading; จากนั้น drawer ปิดและ toast `ส่งรายการราคาเพื่ออนุมัติแล้ว` | ☐ |
| 7 | VERIFY หน้ารายการ | — | จำนวนรายการ = baseline step 1 + 1 และรายการใหม่มีสถานะ `รออนุมัติ` | ☐ |

#### TC-CRT-03 — ห้ามเลือก/ส่งคู่ค้าที่ไม่ active

- Group/Priority/Trace: Master validation · P0 · BR-VPL-02, EC-02
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER vendor non-active + list baseline=9 · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-MASTER
- Pass criteria: คู่ค้าที่ไม่ active ไม่ถูกยอมรับ และไม่มีรายการใหม่

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `สร้างรายการราคา` | — | drawer เปิด | ☐ |
| 2 | TYPE ใน `ค้นหารหัสหรือชื่อคู่ค้า` | code ของ vendor non-active | ไม่พบ vendor นี้เป็นตัวเลือกที่เลือกได้ หรือเห็นคำอธิบายว่าไม่พร้อมใช้งาน | ☐ |
| 3 | TYPE ค่าคู่ค้าเองโดยไม่ SELECT | vendor non-active code | ช่องแสดงข้อความที่พิมพ์แต่ยังไม่มี master selection | ☐ |
| 4 | CLICK `บันทึกร่าง` หลังกรอกส่วนอื่นครบ | — | เห็น `กรุณาเลือกคู่ค้าที่มีสถานะใช้งานจากรายการ` | ☐ |
| 5 | VERIFY หน้ารายการหลังปิด | baseline จาก Setup | จำนวนรายการเท่า baseline=9 | ☐ |

#### TC-CRT-04 — ห้ามเลือกสินค้าที่ไม่ active หรือซื้อไม่ได้

- Group/Priority/Trace: Master validation · P0 · BR-VPL-03, LOCK-VPL-17
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER product non-purchasable/obsolete + list baseline=9 · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-MASTER
- Pass criteria: product ที่ไม่ผ่าน master rule ไม่ถูกสร้างเป็นราคา

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `สร้างรายการราคา` | — | drawer เปิด | ☐ |
| 2 | SELECT คู่ค้า active | — | ช่องสินค้าเปิดให้ค้นหา | ☐ |
| 3 | TYPE ใน `ค้นหารหัสหรือชื่อสินค้า` | product non-purchasable/obsolete | ไม่พบเป็นตัวเลือกที่เลือกได้ หรือมีคำอธิบายไม่พร้อมใช้งาน | ☐ |
| 4 | TYPE product code ดังกล่าวโดยไม่เลือก master | product code ดังกล่าว | ช่องแสดงข้อความที่พิมพ์แต่ยังไม่มี master selection | ☐ |
| 5 | CLICK `บันทึกร่าง` | — | เห็น `กรุณาเลือกสินค้าที่ใช้งานและสั่งซื้อได้จากรายการ`; จำนวน record เท่า baseline=9 | ☐ |

#### TC-CRT-05 — Purchase UOM ต้องตามสินค้าที่เลือก

- Group/Priority/Trace: Cross-field validation · P0 · BR-VPL-06
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER product multiple UOM · files=— · inject=API request with invalid UOM for server-path step`
- Start route: `#/vendor-price-list`
- Data set: DS-MASTER
- Pass criteria: UOM dependent และค่าเก่าที่ไม่ตรงถูก block

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `สร้างรายการราคา` และเลือกสินค้า A | — | `Purchase UOM` แสดง base UOM/หน่วยที่ `can_buy=true` ของสินค้า A เท่านั้น | ☐ |
| 2 | SELECT หน่วยซื้อของสินค้า A | — | ช่องแสดงหน่วยที่เลือก | ☐ |
| 3 | SELECT สินค้า B | — | รายการ UOM เปลี่ยนตามสินค้า B; ค่าเดิมไม่คงอยู่ถ้าไม่ใช่หน่วยซื้อของ B | ☐ |
| 4 | CLICK `บันทึกร่าง` พร้อมค่า UOM ที่ไม่ตรงจาก API harness | invalid UOM | เห็น `Purchase UOM ไม่ตรงกับ Product Master`; ไม่มี record ใหม่ | ☐ |

#### TC-CRT-06 — boundary ราคา ส่วนลด และค่าขนส่ง

- Group/Priority/Trace: Financial validation · P0 · BR-VPL-04, EC-04, EC-09
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER · files=— · inject=API boundary payloads for values browser blocks`
- Start route: `#/vendor-price-list`
- Data set: DS-MASTER
- Pass criteria: ไม่รับ price/price_per ≤0, discount นอก 0..100 หรือ freight ติดลบ

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `สร้างรายการราคา` | — | drawer เปิด | ☐ |
| 2 | SELECT master และ UOM ตามชุด A | ชุด A | ปุ่ม `ถัดไป` ใช้งานได้ | ☐ |
| 3 | CLICK `ถัดไป` | — | เห็นช่องตัวเลขราคา | ☐ |
| 4 | TYPE ชุด A ให้ครบยกเว้นตัวเลขที่กำลังทดสอบ | ชุด A | พร้อมทดสอบตัวเลข | ☐ |
| 5 | TYPE `0` → `ราคาตั้ง` | — | ช่องแสดง 0 | ☐ |
| 6 | CLICK `ยืนยันและส่งอนุมัติ` | — | เห็น `กรุณากรอกข้อมูลให้ครบถ้วน`; server ต้องให้ `BR_PRICE_INVALID` | ☐ |
| 7 | OPEN API request `price_per=0` | — | ถูกปฏิเสธด้วย `BR_PRICE_INVALID` `⚠ ไม่พบ validation เฉพาะใน HTML — ต้อง simulate` | ☐ |
| 8 | OPEN API request `discount=-0.01` | — | ถูกปฏิเสธด้วย `BR_DISCOUNT_INVALID`; ไม่ clamp เป็น 0 `⚠ ต้อง simulate` | ☐ |
| 9 | OPEN API request `discount=100.01` | — | ถูกปฏิเสธด้วย `BR_DISCOUNT_INVALID`; ไม่ clamp เป็น 100 `⚠ ต้อง simulate` | ☐ |
| 10 | OPEN API request `freight=-0.01` | — | ถูกปฏิเสธด้วย `BR_FREIGHT_INVALID`; ไม่แก้เป็นศูนย์ `⚠ ต้อง simulate` | ☐ |
| 11 | OPEN API request `valid numeric boundaries` | price=0.01, price_per=1, discount=100, freight=0 | ผ่าน field validation หาก landed cost ไม่ติดลบ `(ต้อง simulate)` | ☐ |

#### TC-CRT-07 — วันที่เริ่มบังคับและวันสิ้นสุดแบบเปิด

- Group/Priority/Trace: Date validation · P0 · BR-VPL-10
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER · files=— · inject=date-range API validation`
- Start route: `#/vendor-price-list`
- Data set: DS-MASTER
- Pass criteria: from required, end ไม่ก่อน start, ค่าว่างแสดง `เป็นต้นไป`

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `สร้างรายการราคา` | — | drawer เปิด | ☐ |
| 2 | SELECT master และ UOM ตามชุด A | ชุด A | ปุ่ม `ถัดไป` ใช้งานได้ | ☐ |
| 3 | CLICK `ถัดไป` | — | เห็น `เริ่มใช้` และ `สิ้นสุด` | ☐ |
| 4 | TYPE ชุด A ให้ครบยกเว้น `เริ่มใช้` | — | ช่องเริ่มใช้ว่าง | ☐ |
| 5 | CLICK `ยืนยันและส่งอนุมัติ` | — | เห็น `กรุณาระบุวันเริ่มราคา` (`BR_DATE_RANGE_INVALID`) `⚠ ไม่พบ anchor นี้ใน HTML — ต้อง simulate` | ☐ |
| 6 | TYPE `2026-08-10` → `เริ่มใช้` | — | ช่องแสดงวันที่เริ่ม | ☐ |
| 7 | TYPE `2026-08-09` → `สิ้นสุด` | — | ช่องแสดงวันที่สิ้นสุด | ☐ |
| 8 | CLICK `ยืนยันและส่งอนุมัติ` | — | ไม่ส่งและได้ `BR_DATE_RANGE_INVALID` `⚠ ไม่พบใน HTML — ต้อง simulate` | ☐ |
| 9 | TYPE ค่าว่าง → `สิ้นสุด` | — | ช่องสิ้นสุดว่างได้ | ☐ |
| 10 | CLICK `บันทึกร่าง` | — | รายการถูกบันทึก | ☐ |
| 11 | VERIFY ช่วงมีผลของรายการใหม่ | — | แสดง `10 ส.ค. 2569 – เป็นต้นไป` ไม่ใช้ em-dash เดี่ยวแทนวันสิ้นสุด | ☐ |

#### TC-CRT-08 — ค่า default สกุลเงินและภาษี

- Group/Priority/Trace: Defaults · P1 · BR-VPL-05, BR-VPL-07
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER vendor USD + product VAT7 · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-MASTER
- Pass criteria: default มาจาก master และผู้ใช้แก้ currency ได้ก่อนสร้าง

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `สร้างรายการราคา` | — | drawer เปิด | ☐ |
| 2 | SELECT vendor สกุล USD | — | `สกุลเงิน` แสดง USD อัตโนมัติ | ☐ |
| 3 | SELECT product VAT7 | — | `ภาษีซื้อ` แสดงค่าที่สอดคล้อง Product Master | ☐ |
| 4 | SELECT `THB` → `สกุลเงิน` | — | ค่าเปลี่ยนเป็น THB ได้ก่อนสร้างและแสดงตรงขั้นสรุป | ☐ |

#### TC-CRT-09 — เหตุผลเป็นข้อมูลบังคับก่อนส่ง

- Group/Priority/Trace: Validation · P0 · EC-07, BR_REASON_REQUIRED
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER valid · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-MASTER
- Pass criteria: ส่งไม่ได้เมื่อไม่มีเหตุผล และค่าที่กรอกอื่นไม่หาย

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `สร้างรายการราคา` | — | drawer เปิด | ☐ |
| 2 | SELECT master และ UOM ตามชุด A | — | ปุ่ม `ถัดไป` ใช้งานได้ | ☐ |
| 3 | CLICK `ถัดไป` | — | เห็นช่อง `เหตุผล` | ☐ |
| 4 | TYPE ราคา/วันที่ตามชุด A โดยเว้น `เหตุผล` | — | ช่องอื่นแสดงค่าที่กรอก | ☐ |
| 5 | CLICK `ยืนยันและส่งอนุมัติ` | — | เห็น `กรุณากรอกข้อมูลให้ครบถ้วน`; drawer ไม่ปิด (`BR_REASON_REQUIRED`) | ☐ |
| 6 | TYPE `ปรับราคาตามใบเสนอราคาล่าสุด` → `เหตุผล` | — | ช่องเหตุผลแสดงค่าที่กรอก; ช่องอื่นยังคงค่าเดิม | ☐ |
| 7 | CLICK `ยืนยันและส่งอนุมัติ` | — | ส่งได้และสถานะเป็น `รออนุมัติ` | ☐ |

#### TC-CRT-10 — ห้ามสร้าง Header ซ้ำ

- Group/Priority/Trace: Duplicate · P0 · BR-VPL-01, EC-01
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-PRICE existing identical identity · files=— · inject=real create API with DB unique guard`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE
- Pass criteria: identical tenant/company/site/vendor/product/UOM/currency ถูก block แบบ atomic

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `สร้างรายการราคา` และเลือก identity เดียวกับรายการที่มีอยู่ | same vendor/product/UOM/currency | UI แสดงค่าครบ | ☐ |
| 2 | CLICK `บันทึกร่าง` | — | ระบบจริงตอบ `มีรายการราคาสำหรับขอบเขตนี้แล้ว`; ไม่มีแถวซ้ำ `⚠ ไม่พบใน HTML — ต้อง simulate` | ☐ |
| 3 | VERIFY จำนวนรายการหลัง refresh | baseline count | เท่า baseline | ☐ |

#### TC-CRT-11 — clone ต้องเปลี่ยน UOM หรือสกุลเงิน

- Group/Priority/Trace: Clone/identity · P0 · AC-07, LOCK-VPL-07
- Actor: procurement_manager
- Setup: `role=procurement_manager · seed=DS-PRICE active · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE
- Pass criteria: vendor/product ล็อก; clone ค่า identity เดิมส่งไม่ได้

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN รายการสถานะ `ใช้งาน` | — | view drawer เปิด | ☐ |
| 2 | CLICK `สร้างรายการใหม่จากรายการนี้` | — | drawer `สร้างรายการใหม่จากรายการเดิม` เปิด | ☐ |
| 3 | VERIFY `คู่ค้า` และ `สินค้า` | — | แสดง `ล็อก` และ `ข้อมูลนี้เป็นส่วนหนึ่งของรายการเดิม จึงไม่สามารถแก้ไขได้`; UOM/currency แก้ได้ | ☐ |
| 4 | CLICK `บันทึกร่าง` โดยไม่เปลี่ยน UOM/currency | — | เห็น `กรุณาเปลี่ยน Purchase UOM หรือสกุลเงินก่อนบันทึกร่าง` | ☐ |
| 5 | SELECT Purchase UOM หรือ currency ใหม่ | valid alternative | identity ใหม่แสดงใน drawer | ☐ |
| 6 | CLICK `บันทึกร่าง` | — | สร้าง Header ใหม่สถานะ `ร่าง`; Header เดิมยังแสดงค่าเดิมจาก Setup | ☐ |

### กลุ่ม C — อนุมัติ Price Version และสถานะใช้งาน

#### TC-APR-01 — ผู้อนุมัติคนละคนอนุมัติรายการรออนุมัติ

- Group/Priority/Trace: Approval happy path · P0 · AC-05, BR-VPL-17
- Actor: procurement_manager (ไม่ใช่ maker)
- Setup: `role=procurement_manager · seed=DS-PRICE pending made by another user · files=— · inject=history/audit read harness`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE, DS-ROLE
- Pass criteria: pending เปลี่ยนเป็น active และมีประวัติ auditable

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN รายการสถานะ `รออนุมัติ` | — | drawer แสดง `อนุมัติ`, `ปฏิเสธ` และแท็บ `Approval & Audit` | ☐ |
| 2 | CLICK `อนุมัติ` | — | modal `อนุมัติราคาฉบับนี้หรือไม่?` เปิด | ☐ |
| 3 | CLICK `อนุมัติ` ใน modal | — | modal ปิด เห็น toast `อนุมัติแล้ว` และสถานะเป็น `ใช้งาน` | ☐ |
| 4 | CLICK `Approval & Audit` | — | เห็นผู้อนุมัติ เวลา และการเปลี่ยนสถานะ; ระบบจริงต้องเป็น WORM `(ต้อง simulate เพื่อพิสูจน์แก้ย้อนหลังไม่ได้)` | ☐ |

#### TC-APR-02 — maker อนุมัติรายการตนเองไม่ได้

- Group/Priority/Trace: SoD negative · P0 · AC-05, BR-VPL-12, EC-08
- Actor: procurement_manager ที่เป็น maker
- Setup: `role=procurement_manager · seed=DS-PRICE pending made by current user · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE, DS-ROLE
- Pass criteria: สถานะไม่เปลี่ยนและไม่เกิด success audit

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN รายการ `รออนุมัติ` ที่สร้างโดยผู้ใช้ปัจจุบัน | — | เห็น action `อนุมัติ` ตาม prototype fixture | ☐ |
| 2 | CLICK `อนุมัติ` และยืนยัน | — | เห็น `ไม่สามารถอนุมัติรายการที่ตนเองสร้างได้` | ☐ |
| 3 | VERIFY รายการและ `Approval & Audit` | — | ยังเป็น `รออนุมัติ`; ไม่มีเหตุการณ์ success ใหม่ | ☐ |

#### TC-APR-03 — admin ยังต้องผ่าน SoD

- Group/Priority/Trace: Permission/SoD · P0 · BR-VPL-12
- Actor: admin
- Setup: `role=admin · seed=DS-PRICE own pending + another maker pending · files=— · inject=admin auth and central DOA route`
- Start route: `#/vendor-price-list`
- Data set: DS-ROLE
- Pass criteria: admin อนุมัติของตนเองไม่ได้ แต่ของผู้อื่นได้เมื่ออยู่ใน DOA

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `อนุมัติ` ที่ own pending | — | ถูก block ด้วย `ไม่สามารถอนุมัติรายการที่ตนเองสร้างได้` `(ต้อง simulate role)` | ☐ |
| 2 | CLICK `อนุมัติ` ที่ pending ของ maker คนอื่น | — | อนุมัติได้ถ้า admin อยู่ใน route; สถานะเป็น `ใช้งาน` `(ต้อง simulate role/DOA)` | ☐ |

#### TC-APR-04 — ปฏิเสธต้องระบุเหตุผลและกลับเป็นร่าง

- Group/Priority/Trace: Reject · P0 · AC-06, BR-VPL-17
- Actor: procurement_manager (ไม่ใช่ maker)
- Setup: `role=procurement_manager · seed=DS-PRICE pending · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE
- Pass criteria: reason required; success กลับ draft และเก็บเหตุผล

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN pending record | — | view drawer เปิด | ☐ |
| 2 | CLICK `ปฏิเสธ` | — | modal `ปฏิเสธราคาฉบับนี้หรือไม่?` และช่อง `ระบุเหตุผลที่ปฏิเสธ` เปิด | ☐ |
| 3 | CLICK `ปฏิเสธ` ใน modalโดยไม่กรอก | — | modal ยังเปิดและสถานะยังเป็น `รออนุมัติ` ตาม Setup | ☐ |
| 4 | TYPE `ราคาไม่ตรงใบเสนอราคา` → `ระบุเหตุผลที่ปฏิเสธ` | — | ช่องแสดงค่าที่กรอก | ☐ |
| 5 | CLICK `ปฏิเสธ` | — | modal ปิด เห็น `ส่งกลับเป็นร่างแล้ว`; สถานะเป็น `ร่าง` | ☐ |
| 6 | CLICK `Approval & Audit` | — | เห็นเหตุผลที่ปฏิเสธตรงตามที่กรอก | ☐ |

#### TC-APR-05 — แก้ไข draft ได้รวม identity

- Group/Priority/Trace: Edit draft · P0 · AC-06, LD-04
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-PRICE draft · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE
- Pass criteria: draft แก้ vendor/product/UOM/currency และรายละเอียดราคาได้

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN รายการ `ร่าง` | — | view drawer เปิด | ☐ |
| 2 | CLICK `แก้ไขร่าง` | — | drawer `แก้ไขร่าง` เปิด | ☐ |
| 3 | SELECT ค่าใหม่ใน `คู่ค้า`, `สินค้า`, `Purchase UOM`, `สกุลเงิน` | valid master values | ทุกช่องแก้ได้และ UOM เปลี่ยนตาม product | ☐ |
| 4 | TYPE ราคา/เหตุผลใหม่ | valid | ช่องแสดงค่าใหม่ | ☐ |
| 5 | CLICK `บันทึกร่าง` | — | เห็น `บันทึกร่างแล้ว`; แถวเดิมอัปเดตและยังเป็น `ร่าง` | ☐ |

#### TC-APR-06 — ต่ำกว่า threshold ยังต้องรออนุมัติ

- Group/Priority/Trace: DOA boundary · P0 · AC-04, BR-VPL-11, LOCK-VPL-04
- Actor: procurement_manager
- Setup: `role=procurement_manager · seed=ชุด E active baseline landed=100; config threshold=10% · files=— · inject=deterministic DOA config`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE
- Pass criteria: absolute landed ex-tax change 9.99% เป็น normal tier แต่ยัง pending

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN active record | — | view drawer เปิด | ☐ |
| 2 | CLICK `สร้างราคาฉบับใหม่` | — | identity ล็อก พร้อม helper อธิบาย | ☐ |
| 3 | CLICK `ถัดไป` | — | เห็นช่อง `ราคาตั้ง` และ `สรุปก่อนส่ง` | ☐ |
| 4 | TYPE `109.99` → `ราคาตั้ง` | ชุด E | ขั้น `สรุปก่อนส่ง` แสดงการเปลี่ยนแปลง `9.99%` จากราคาปัจจุบัน | ☐ |
| 5 | CLICK `ยืนยันและส่งอนุมัติ` | — | version ใหม่เป็น `รออนุมัติ`; ไม่ active ทันที `(ต้อง simulate ค่า exact/route)` | ☐ |

#### TC-APR-07 — เท่ากับ threshold ใช้ elevated tier และยัง pending

- Group/Priority/Trace: DOA boundary · P0 · AC-04, LOCK-VPL-04
- Actor: procurement_manager
- Setup: `role=procurement_manager · seed=ชุด E active baseline landed=100; config threshold=10% · files=— · inject=deterministic DOA config`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE
- Pass criteria: abs(change)=10.00% เข้า elevated ตาม >= ไม่ใช่ >

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN active record | — | view drawer เปิด | ☐ |
| 2 | CLICK `สร้างราคาฉบับใหม่` | — | form drawer เปิด | ☐ |
| 3 | CLICK `ถัดไป` | — | เห็นช่อง `ราคาตั้ง` และ `สรุปก่อนส่ง` | ☐ |
| 4 | TYPE `110.00` → `ราคาตั้ง` | ชุด E | ขั้นสรุปแสดง change `10.00%` จาก landed ex-tax แบบ absolute | ☐ |
| 5 | VERIFY `ขั้นตอนการอนุมัติ` และ `เกณฑ์ตรวจสอบเพิ่มเติม` | — | ระบุ elevated route จาก config; ไม่แสดง 10% เป็นค่าฮาร์ดโค้ด production `⚠ route ต้อง simulate` | ☐ |
| 6 | CLICK `ยืนยันและส่งอนุมัติ` | — | version ใหม่เป็น `รออนุมัติ` | ☐ |

#### TC-APR-08 — เหนือ threshold, route หาย และ SLA

- Group/Priority/Trace: DOA/SLA · P0 · AC-04, BR-VPL-18
- Actor: procurement_manager/director
- Setup: `role=procurement_manager · seed=ชุด E active baseline landed=100; threshold=10%; elevated route fixture · files=— · inject=DOA route present/missing and frozen business clock`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE, DS-ROLE
- Pass criteria: >10% route ไป director; route หาย block; overdue escalate ตาม snapshot

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN active record ที่ route มีจริง | — | view drawer เปิด | ☐ |
| 2 | CLICK `สร้างราคาฉบับใหม่` | — | form drawer เปิด | ☐ |
| 3 | CLICK `ถัดไป` | — | เห็นช่อง `ราคาตั้ง` และ `สรุปก่อนส่ง` | ☐ |
| 4 | TYPE `110.01` → `ราคาตั้ง` | ชุด E | ขั้นสรุปแสดง change `10.01%` และ elevated approval tier `(ต้อง simulate)` | ☐ |
| 5 | CLICK `ยืนยันและส่งอนุมัติ` | — | สถานะ `รออนุมัติ`; director ที่อยู่ใน route อนุมัติได้ | ☐ |
| 6 | OPEN active fixture ที่ไม่มี DOA route | — | form drawerขั้นสรุปพร้อมข้อมูล valid เปิด `(ต้อง simulate)` | ☐ |
| 7 | CLICK `ยืนยันและส่งอนุมัติ` | — | ถูก block ด้วย `ไม่พบสายอนุมัติที่ใช้ได้`; fixture นี้ไม่มี pending record `(ต้อง simulate)` | ☐ |
| 8 | WAIT ด้วย business clock fixtureเกิน 1 วันทำการ | — | pending จาก step 5 ถูก escalate ตาม central DOA; audit เก็บ policy snapshot `(ต้อง simulate)` | ☐ |

#### TC-APR-09 — active version ล็อก identity แต่แก้ราคาได้

- Group/Priority/Trace: Versioning · P0 · AC-07, LOCK-VPL-07
- Actor: procurement_manager
- Setup: `role=procurement_manager · seed=DS-PRICE active · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE
- Pass criteria: vendor/product/UOM/currency แก้ไม่ได้; ราคา/วันที่/เหตุผลแก้เพื่อสร้าง version ได้

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN active record | — | view drawer เปิด | ☐ |
| 2 | CLICK `สร้างราคาฉบับใหม่` | — | drawer ชื่อ `สร้างราคาฉบับใหม่` | ☐ |
| 3 | VERIFY identity ทั้งสี่ช่อง | — | `คู่ค้า`, `สินค้า`, `Purchase UOM`, `สกุลเงิน` มี `ล็อก` และ helper `ข้อมูลนี้เป็นส่วนหนึ่งของรายการเดิม จึงไม่สามารถแก้ไขได้` | ☐ |
| 4 | CLICK `ถัดไป` | — | เห็นขั้นราคา | ☐ |
| 5 | TYPE ราคา/วันที่/เหตุผลใหม่ | valid | ขั้นสรุปแสดงค่าฉบับใหม่ | ☐ |
| 6 | CLICK `ยืนยันและส่งอนุมัติ` | — | สร้าง version ใหม่ `รออนุมัติ`; version active เดิมยังใช้จนกว่าจะอนุมัติใหม่ | ☐ |

#### TC-APR-10 — มี pending version อยู่แล้วต้องสร้างซ้ำไม่ได้

- Group/Priority/Trace: Version conflict · P0 · EC-12
- Actor: procurement_manager
- Setup: `role=procurement_manager · seed=DS-PRICE active header with pending version · files=— · inject=DB/API one-pending guard`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE
- Pass criteria: Header เดียวมี pending ได้หนึ่งรายการ

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN active Header ที่มี pending version อยู่ | — | เห็นประวัติ active และ pending ที่มีอยู่ | ☐ |
| 2 | CLICK `สร้างราคาฉบับใหม่` | — | drawer สร้าง version เปิด | ☐ |
| 3 | CLICK `ยืนยันและส่งอนุมัติ` หลังกรอก valid new price | valid new price | ระบบจริง block ด้วย `BR_PENDING_VERSION_EXISTS`; ไม่มี pending ซ้ำ `⚠ ไม่พบใน HTML — ต้อง simulate` | ☐ |

#### TC-APR-11 — ปิดใช้งานแล้วถูกตัดจากการใช้งาน

- Group/Priority/Trace: Lifecycle · P0 · AC-15, EC-13
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-PRICE active · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE
- Pass criteria: confirm แล้ว status inactive และไม่เข้า compare/resolve

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK action `ปิดใช้งาน` ที่แถว active | — | modal `ปิดใช้งานรายการราคา?` และข้อความ `รายการนี้จะไม่ถูกใช้ในการเลือกราคาและเปรียบเทียบราคา` | ☐ |
| 2 | CLICK `ปิดใช้งาน` ใน modal | — | เห็น `ปิดใช้งานรายการแล้ว`; pill เป็น `ปิดใช้งาน` | ☐ |
| 3 | OPEN `เปรียบเทียบราคา` และคำนวณเงื่อนไขเดิม | — | รายการที่ปิดไม่ปรากฏในผล | ☐ |

#### TC-APR-12 — เปิดใช้งานกลับได้เมื่อ master ยังผ่าน

- Group/Priority/Trace: Lifecycle · P0 · AC-15, LD-07
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-PRICE inactive; master still valid · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-PRICE
- Pass criteria: reactivation reversible แต่ revalidate master ก่อน

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK action `เปิดใช้งาน` ที่แถว inactive | — | modal `เปิดใช้งานรายการราคา?` และข้อความ `รายการนี้จะกลับมาใช้ในการเลือกราคาและเปรียบเทียบราคา` | ☐ |
| 2 | CLICK `เปิดใช้งาน` ใน modal | — | เห็น `เปิดใช้งานรายการแล้ว`; pill เป็น `ใช้งาน` | ☐ |
| 3 | CLICK `เปิดใช้งาน` กับ fixture ที่ vendor/product ไม่พร้อม | — | เห็น `ไม่สามารถเปิดใช้งานได้ เนื่องจากคู่ค้าหรือสินค้าไม่พร้อมใช้งาน`; ยังคง `ปิดใช้งาน` | ☐ |

### กลุ่ม D — Batch Entry

#### TC-BAT-01 — เพิ่มและลบแถวโดยคงอย่างน้อยหนึ่งแถว

- Group/Priority/Trace: Batch UX · P0 · AC-08
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-UI · files=—`
- Start route: `#/vendor-price-list/batch`
- Data set: DS-UI
- Pass criteria: add/remove ทำงาน และลบแถวสุดท้ายไม่ได้

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN `#/vendor-price-list/batch` | — | เห็น `Batch Entry`, `เพิ่มแถว`, `ตรวจสอบและส่งอนุมัติ` และอย่างน้อย 1 แถว | ☐ |
| 2 | VERIFY และจดจำนวนแถว baseline | — | baseline=1 แถว | ☐ |
| 3 | CLICK `เพิ่มแถว` | — | จำนวนแถว=2 | ☐ |
| 4 | CLICK `เพิ่มแถว` | — | จำนวนแถว=3 | ☐ |
| 5 | CLICK ปุ่มลบของแถวกลาง | — | เห็น `ลบแถวแล้ว`; จำนวนแถว=2 | ☐ |
| 6 | CLICK ปุ่มลบจนเหลือหนึ่งแถว | — | จำนวนแถว=1 | ☐ |
| 7 | CLICK ปุ่มลบของแถวสุดท้าย | — | แถวสุดท้ายยังอยู่; เห็น `ต้องมีอย่างน้อย 1 แถว` หรือปุ่ม disabled | ☐ |

#### TC-BAT-02 — แถวว่างทั้งแถวไม่ถูกส่ง

- Group/Priority/Trace: Batch edge · P0 · EC-05
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-UI · files=—`
- Start route: `#/vendor-price-list/batch`
- Data set: DS-UI
- Pass criteria: blank row ไม่สร้างข้อมูลและไม่ถูกนับว่าผ่าน

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `เพิ่มแถว` | — | แถวใหม่ว่างทั้งหมดและไม่ถูกนับว่าผ่าน | ☐ |
| 2 | CLICK `ตรวจสอบและส่งอนุมัติ` | — | แถวว่างไม่สร้าง record; ถ้าไม่มี valid row ให้คงหน้าเดิมและแจ้ง `กรุณากรอกข้อมูลให้ครบถ้วน` | ☐ |

#### TC-BAT-03 — แถวที่เริ่มกรอกแต่ไม่ครบต้อง block

- Group/Priority/Trace: Batch validation · P0 · AC-08, EC-05
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER · files=—`
- Start route: `#/vendor-price-list/batch`
- Data set: DS-MASTER
- Pass criteria: invalid row ถูกชี้ตำแหน่งและไม่มี partial commit

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | SELECT `คู่ค้า` ในแถว 1 แต่เว้นสินค้า/UOM/ราคา/วันที่ | active vendor | summary `ต้องแก้` เพิ่ม 1 | ☐ |
| 2 | CLICK `ตรวจสอบและส่งอนุมัติ` | — | เห็น `กรุณากรอกข้อมูลให้ครบถ้วน`; แถว 1 ถูก highlight | ☐ |
| 3 | VERIFY หน้าปัจจุบันและจำนวน list หลังกลับ | baseline count | ยังคงหน้า Batch; ไม่มี record ใดถูกบันทึก | ☐ |

#### TC-BAT-04 — dropdown คู่ค้า สินค้า และ UOM ในแต่ละแถว

- Group/Priority/Trace: Batch master · P0 · AC-08, BR-VPL-02/03/06
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER · files=—`
- Start route: `#/vendor-price-list/batch`
- Data set: DS-MASTER
- Pass criteria: ทุก master field เป็น search dropdown และ UOM ตามสินค้าในแถวนั้น

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | SELECT active vendor จาก search dropdown แถว 1 | active vendor | ผลลัพธ์แสดงชื่อและรหัส; พิมพ์ค่าที่ไม่เลือกไม่ถือว่า valid | ☐ |
| 2 | SELECT active+purchasable product จาก search dropdown แถว 1 | active+purchasable product | เห็นชื่อ/รหัสสินค้าเต็ม | ☐ |
| 3 | OPEN `Purchase UOM` | — | มีเฉพาะ purchase UOM ของ product แถว 1 | ☐ |
| 4 | SELECT product อื่นในแถว 2 | — | UOM ของแต่ละแถวไม่ปะปนกัน | ☐ |

#### TC-BAT-05 — Batch สำเร็จกลับ list และทุกแถวรออนุมัติ

- Group/Priority/Trace: Batch happy path · P0 · AC-09, LD-06
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER two valid rows · files=—`
- Start route: `#/vendor-price-list/batch`
- Data set: DS-MASTER
- Pass criteria: count เพิ่มตามจำนวน valid rows และ status ทุกแถว pending

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | VERIFY และจดจำนวนรายการ baseline ที่หน้า list | — | จด baseline ได้ | ☐ |
| 2 | TYPE ชุดข้อมูล valid ให้ครบ 2 แถวใน Batch | — | summary แสดง `ผ่าน 2 แถว`, `ต้องแก้ 0 แถว` | ☐ |
| 3 | CLICK `ตรวจสอบและส่งอนุมัติ` | — | ระหว่างส่งเห็น `กำลังส่ง…`; จากนั้นกลับ `#/vendor-price-list` | ☐ |
| 4 | VERIFY toast และตาราง | — | เห็น `ส่งรายการราคา 2 รายการเพื่ออนุมัติแล้ว`; count = baseline+2 และทั้งสองแถว `รออนุมัติ` | ☐ |

### กลุ่ม E — Import Vendor Price List

#### TC-IMP-01 — เปิด/ปิด Import modal และ layout เป็นลำดับ

- Group/Priority/Trace: Import UX · P1 · AC-10, LOCK-VPL-11
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-UI · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-UI
- Pass criteria: modal แสดง 4 ส่วนชัด และปิดได้ทุกทางโดยไม่เปลี่ยนข้อมูล

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `Import` | — | modal `Import Vendor Price List` เปิด; เห็น `เลือกไฟล์`, `ตั้งค่าการนำเข้า`, `ผลการตรวจสอบ`, `ตัวอย่างข้อมูล` ตามลำดับ | ☐ |
| 2 | PRESS `Escape` | — | modal ปิด; ไม่มี import outcome | ☐ |
| 3 | CLICK `Import` | — | modal เปิดรอบที่สอง | ☐ |
| 4 | CLICK พื้นหลังนอก modal | — | modal ปิด | ☐ |
| 5 | CLICK `Import` | — | modal เปิดรอบที่สาม | ☐ |
| 6 | CLICK ปุ่ม X มุมขวาบน | — | modal ปิด | ☐ |

#### TC-IMP-02 — ยังไม่เลือกไฟล์ต้องยืนยันไม่ได้

- Group/Priority/Trace: Import gating · P0 · AC-10
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-UI · files=—`
- Start route: `#/vendor-price-list`
- Data set: DS-UI
- Pass criteria: ก่อนมี preview ปุ่ม confirm ไม่ทำงาน

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `Import` | — | เห็น `ยังไม่ได้เลือกไฟล์` และ `กรุณาเลือกไฟล์เพื่อเริ่มตรวจสอบข้อมูล` | ☐ |
| 2 | VERIFY `ยืนยันนำเข้า` | — | disabled หรือคลิกแล้วไม่ commit; ไม่มี outcome สำเร็จ | ☐ |
| 3 | CLICK `Template` | — | ระบบดาวน์โหลด template ชนิดที่ระบุ หรือแจ้งผลชัดเจน; ต้นแบบอาจเป็น mock `⚠ ตรวจไฟล์จริงใน implementation` | ☐ |

#### TC-IMP-03 — preview ไฟล์ที่มี master ไม่ตรง

- Group/Priority/Trace: Import negative · P0 · EC-06
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER · files=vpl-unmatched-master.csv · inject=real import preview endpoint`
- Start route: `#/vendor-price-list`
- Data set: DS-CSV-MASTER
- Pass criteria: invalid rows ถูกนับและระบุเหตุผล; commit ไม่ข้ามเงียบ

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `Import` | — | modal เปิด | ☐ |
| 2 | UPLOAD `vpl-unmatched-master.csv` | — | แสดงชื่อไฟล์และเริ่มตรวจสอบ | ☐ |
| 3 | VERIFY `ผลการตรวจสอบ` | — | `ไม่ผ่าน` > 0 และแถวตัวอย่างบอกว่า vendor/product/UOM ใดไม่ตรง | ☐ |
| 4 | VERIFY `ยืนยันนำเข้า` | — | disabled เมื่อ accepted set ว่าง; ถ้ามีบางแถวผ่าน ต้องแสดงจำนวนที่จะ commit และจำนวนไม่ผ่านอย่างชัดเจน `(ต้อง simulate สำหรับไฟล์จริง)` | ☐ |

#### TC-IMP-04 — preview ไฟล์ valid 4 แถว

- Group/Priority/Trace: Import preview happy · P0 · AC-10
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER · files=vpl-valid-4-rows.csv`
- Start route: `#/vendor-price-list`
- Data set: DS-CSV-OK
- Pass criteria: preview counts และตัวอย่างตรงไฟล์; confirm เปิดใช้

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `Import` | — | modal เปิด | ☐ |
| 2 | UPLOAD `vpl-valid-4-rows.csv` | — | ผลตรวจแสดง `รายการทั้งหมด 4`, `ผ่านการตรวจ 4`, `ไม่ผ่าน 0` | ☐ |
| 3 | VERIFY checklist | — | เห็น `คู่ค้า active ใน F-VENDOR`, `สินค้า active และสั่งซื้อได้`, `UOM ตรงกับ Purchase UOM` | ☐ |
| 4 | VERIFY action | — | เห็น `พร้อมนำเข้า 4 แถว`; `ยืนยันนำเข้า` enabled | ☐ |

#### TC-IMP-05 — merge เพิ่ม/อัปเดตแล้วทุก record เข้ารออนุมัติ

- Group/Priority/Trace: Import commit · P0 · AC-11, LD-06
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER matching existing drafts · files=vpl-valid-4-rows.csv · inject=real import commit endpoint`
- Start route: `#/vendor-price-list`
- Data set: DS-CSV-OK
- Pass criteria: outcome แยกเพิ่ม/อัปเดต/ข้าม และ record ที่ส่งเป็น pending

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | VERIFY และจดจำนวนรายการ/สถานะ baseline | — | จด baseline ก่อน import | ☐ |
| 2 | CLICK `Import` | — | modal เปิด | ☐ |
| 3 | UPLOAD `vpl-valid-4-rows.csv` | — | preview ผ่าน 4 แถว | ☐ |
| 4 | SELECT `เพิ่มรายการใหม่และอัปเดตรายการเดิม` | — | note อธิบายว่าจะอัปเดตที่ตรงกันและเพิ่มใหม่โดยไม่ลบ | ☐ |
| 5 | CLICK `ยืนยันนำเข้า` | — | เห็น `กำลังนำเข้า…`; modal ปิดเมื่อสำเร็จ | ☐ |
| 6 | VERIFY import outcome บนหน้า list | — | แสดงจำนวนเพิ่มใหม่/อัปเดต/ข้ามอย่างเป็นระเบียบและ toast `นำเข้าสำเร็จ · เพิ่มใหม่ {N} · อัปเดต {N}` | ☐ |
| 7 | VERIFY records ที่นำเข้า | — | new/updated version เป็น `รออนุมัติ`, active เดิมที่ไม่ได้อยู่ accepted-set ตรง baseline step 1 `(ต้อง simulate backend commit)` | ☐ |

#### TC-IMP-06 — replace-unused ไม่แตะรายการที่เริ่มใช้งานแล้ว

- Group/Priority/Trace: Import mode · P0 · AC-11
- Actor: procurement_manager
- Setup: `role=procurement_manager · seed=DS-PRICE draft+pending+active · files=vpl-valid-4-rows.csv · inject=real replace-unused commit endpoint`
- Start route: `#/vendor-price-list`
- Data set: DS-CSV-OK, DS-PRICE
- Pass criteria: แทนได้เฉพาะ draft/pending; active ถูกข้ามและรายงาน

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `Import` | — | modal เปิด | ☐ |
| 2 | UPLOAD `vpl-valid-4-rows.csv` | — | preview ผ่าน | ☐ |
| 3 | SELECT `แทนที่รายการที่ยังไม่ถูกนำไปใช้` | — | note ระบุ `แทนที่ได้เฉพาะรายการร่างหรือรายการที่รออนุมัติ และจะข้ามรายการที่เริ่มใช้งานแล้ว` | ☐ |
| 4 | CLICK `ยืนยันนำเข้า` | — | commit สำเร็จแบบ atomic accepted-set `(ต้อง simulate)` | ☐ |
| 5 | VERIFY outcome และ records | — | active เดิมตรงกับค่า seed ก่อน import; จำนวนข้ามระบุชัด; draft/pending ที่แทนมี version/historyตาม contract | ☐ |

#### TC-IMP-07 — external ID retry, schema/encoding และ preview expiry

- Group/Priority/Trace: Import edge/security · P0 · AC-11, LOCK-VPL-11
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-MASTER · files=vpl-duplicate-external-id.csv,vpl-invalid-header.csv,vpl-invalid-encoding.csv,vpl-formula-like-cell.csv · inject=idempotency store + expirable preview token`
- Start route: `#/vendor-price-list`
- Data set: DS-CSV-ID, DS-CSV-SCHEMA, DS-CSV-SAFE
- Pass criteria: safe retry ไม่สร้างซ้ำ; conflict/error ชัด; formula text ไม่ execute

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | VERIFY และจดจำนวนรายการ baseline | — | จด baseline ก่อน retry | ☐ |
| 2 | UPLOAD `vpl-duplicate-external-id.csv` | content เดิม | preview พร้อม commit | ☐ |
| 3 | CLICK `ยืนยันนำเข้า` | — | commit ครั้งแรกสำเร็จและ outcome แสดงจำนวน | ☐ |
| 4 | UPLOAD `vpl-duplicate-external-id.csv` | content เดิม | preview ระบุรายการเดิม | ☐ |
| 5 | CLICK `ยืนยันนำเข้า` | — | แสดง `ไม่มีรายการใหม่ · ข้าม {N}`; count เท่าหลัง step 3 `(ต้อง simulate)` | ☐ |
| 6 | UPLOAD external ID เดิมแต่ content ต่าง | modified fixture | แสดง conflict; ไม่เขียนทับค่าจาก step 3 `(ต้อง simulate)` | ☐ |
| 7 | UPLOAD `vpl-invalid-header.csv` | — | ถูกปฏิเสธพร้อมเหตุผล schema; confirm disabled `(ต้อง simulate)` | ☐ |
| 8 | UPLOAD `vpl-invalid-encoding.csv` | — | ถูกปฏิเสธพร้อมเหตุผล encoding; confirm disabled `(ต้อง simulate)` | ☐ |
| 9 | UPLOAD `vpl-formula-like-cell.csv` | — | ค่า formula-like แสดงเป็นข้อความ ไม่ execute และไม่ถูกส่งออกเป็นสูตร `(ต้อง simulate)` | ☐ |
| 10 | WAIT ให้ preview token หมดอายุ | — | preview แสดงว่าหมดอายุ | ☐ |
| 11 | CLICK `ยืนยันนำเข้า` | — | ระบบให้ตรวจใหม่; ไม่มี commit เพิ่มจาก count หลัง step 3 `⚠ ไม่พบใน HTML — ต้อง simulate` | ☐ |

### กลุ่ม F — เปรียบเทียบราคาและเลือกใช้ราคา

#### TC-CMP-01 — กดคำนวณแล้วเรียงต้นทุน THB ต่ำไปสูง

- Group/Priority/Trace: Compare happy path · P0 · AC-12, BR-VPL-15
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-PRICE multiple eligible vendors + DS-FX fresh · files=—`
- Start route: `#/vendor-price-list/compare`
- Data set: DS-PRICE, DS-FX
- Pass criteria: ใช้ input เดียวกันทุก vendor, เรียง ascending และอันดับหนึ่งชัด

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN `#/vendor-price-list/compare` | — | เห็น `เปรียบเทียบราคา`, ช่องสินค้า/ปริมาณ/วันที่/สกุลเงิน และปุ่ม `คำนวณ` align ในแถวเดียวกัน | ☐ |
| 2 | SELECT สินค้า active | ชุด C | ช่องสินค้าแสดง RM-2001 | ☐ |
| 3 | TYPE `100` → `ปริมาณ` | — | ช่องแสดง 100 | ☐ |
| 4 | TYPE วันที่ valid → `วันที่` | ชุด C | ช่องแสดงวันที่ | ☐ |
| 5 | SELECT `THB` → สกุลเงินเป้าหมาย | — | input ครบ | ☐ |
| 6 | CLICK `คำนวณ` | — | เห็น `กำลังคำนวณ…` แล้ว `คำนวณราคาใหม่แล้ว`; ผลลัพธ์ปรากฏ | ☐ |
| 7 | VERIFY ค่า `ต้นทุนเทียบ THB` จากบนลงล่าง | — | ทุกค่าถัดไป ≥ ค่าก่อนหน้า; แถวแรกมีสัญลักษณ์ถ้วย/อันดับ `1` ว่าเป็นราคาดีที่สุด | ☐ |

#### TC-CMP-02 — ปุ่มคำนวณใช้ draft ล่าสุดและแสดงเวลา run

- Group/Priority/Trace: Compare behavior · P0 · AC-12, BR-VPL-09
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-PRICE · files=—`
- Start route: `#/vendor-price-list/compare`
- Data set: DS-PRICE
- Pass criteria: เปลี่ยน input แล้วผลเก่าไม่อ้างว่าเป็นค่าปัจจุบัน; กดแล้วคำนวณใหม่

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | SELECT `RM-2001 · ไม้สักแปรรูป เกรด A` | — | สินค้าถูกเลือก | ☐ |
| 2 | TYPE `10` → `ปริมาณ` | — | ช่องแสดง 10 | ☐ |
| 3 | TYPE `2026-08-20` → `วันที่` | — | input ครบ | ☐ |
| 4 | CLICK `คำนวณ` | — | แสดงผล/เวลา run และจดต้นทุนแถวแรกไว้ | ☐ |
| 5 | TYPE `1,000` → `ปริมาณ` | — | input เปลี่ยน แต่ผลยังระบุว่าเป็น run ก่อนหน้าหรือถูกทำเครื่องหมายว่าต้องคำนวณใหม่ | ☐ |
| 6 | CLICK `คำนวณ` | — | เวลา run อัปเดตและผลสะท้อน qty=1,000; tier/landed ex-tax ต่างจากหรือเท่ากับค่าที่จดใน step 4 ตาม tier fixture | ☐ |

#### TC-CMP-03 — FX missing/stale ต้องไม่เดา rate

- Group/Priority/Trace: Compare error · P0 · EC-10, ERR_FX_UNAVAILABLE
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-PRICE multi-currency + DS-FX missing/stale · files=— · inject=FX mock returning missing/stale rate`
- Start route: `#/vendor-price-list/compare`
- Data set: DS-FX
- Pass criteria: ไม่มี fallback 1:1 หรือ rate ล่าสุดที่หมดอายุ

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | SELECT สินค้า multi-currency | DS-FX missing-date fixture | สินค้าถูกเลือก | ☐ |
| 2 | TYPE qty/date ที่ไม่มี FX | — | compare input ครบ | ☐ |
| 3 | CLICK `คำนวณ` | — | แสดงเหตุผล FX unavailable; ไม่แสดงค่า THB ที่เดาเอง `⚠ ไม่พบใน HTML — ต้อง simulate` | ☐ |
| 4 | CLICK `คำนวณ` ด้วย FX stale เกิน policy | — | ตัด candidate พร้อมเหตุผลหรือ fail ทั้ง compare ตาม contract; ไม่ใช้ stale rate `⚠ ต้อง simulate` | ☐ |

#### TC-CMP-04 — tier และช่วง active ต้องให้คำตอบเดียว

- Group/Priority/Trace: Pricing ambiguity · P0 · BR-VPL-08/19, EC-03
- Actor: procurement_manager
- Setup: `role=procurement_manager · seed=DS-PRICE tier boundary + overlap fixtures · files=— · inject=tier/active-overlap API payloads`
- Start route: `#/vendor-price-list/compare`
- Data set: DS-PRICE
- Pass criteria: boundary เลือก tier เดียว; overlap ถูก block ก่อน active/resolve

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | SELECT สินค้าที่มี tier boundary fixture | — | สินค้าถูกเลือก | ☐ |
| 2 | TYPE qty เท่ากับขอบ tier | exact min/max boundary | input แสดงค่า boundary | ☐ |
| 3 | CLICK `คำนวณ` | — | candidate ใช้ tier เดียวตาม inclusive/exclusive contract `(ต้อง simulate exact tier)` | ☐ |
| 4 | CLICK submit ใน test harness ของ fixture tiers ซ้อนกัน/ไม่เรียง | overlap ranges | เห็น `ช่วงปริมาณ (tier) ซ้อนทับกัน`; ไม่สร้าง active ambiguity `⚠ tier editor ไม่พบใน HTML` | ☐ |
| 5 | CLICK `คำนวณ` กับ fixture ที่มี active validity ซ้อน | — | ระบบ block/config error `ช่วงวันที่หรือปริมาณซ้อนกับราคาที่ใช้งานอยู่`; ไม่จัดอันดับคำตอบกำกวม `(ต้อง simulate)` | ☐ |

#### TC-CMP-05 — ไม่รวม inactive/master invalid และแสดง no result

- Group/Priority/Trace: Compare exclusion · P0 · EC-13/14
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-PRICE only inactive/out-of-date candidates · files=—`
- Start route: `#/vendor-price-list/compare`
- Data set: DS-PRICE
- Pass criteria: excluded candidates ไม่โผล่; empty state บอกให้แก้ input

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | SELECT product fixture ที่มี active และ inactive candidate | — | สินค้าถูกเลือก | ☐ |
| 2 | TYPE วันที่ที่ active candidate มีผล | — | input แสดงวันที่ | ☐ |
| 3 | CLICK `คำนวณ` | — | เห็นเฉพาะ Header `ใช้งาน` ที่ vendor/product/date valid | ☐ |
| 4 | TYPE วันที่ที่ไม่มีราคามีผล | — | input แสดงวันใหม่ | ☐ |
| 5 | CLICK `คำนวณ` | — | เห็น `ไม่มีราคาที่ใช้งานได้` และ `ไม่พบราคาที่ใช้งานอยู่ซึ่งตรงกับวันที่และปริมาณ`; ผลจาก step 3 ไม่ค้าง | ☐ |
| 6 | VERIFY รายการที่ `ปิดใช้งาน` | — | ไม่ปรากฏในผลทั้งสอง run | ☐ |

#### TC-CMP-06 — สูตร landed ex-tax และ calculation trace

- Group/Priority/Trace: Calculation · P0 · BR-VPL-09, AC-13
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=known price=120 price_per=12 discount=10 freight=2 · files=— · inject=resolve/trace read endpoint`
- Start route: `#/vendor-price-list/compare`
- Data set: deterministic known-price fixture
- Pass criteria: landed = (120/12)*(1-0.10)+2 = 11.00 และ trace ระบุ version/formula inputs

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | SELECT product ของ known-price fixture | — | สินค้าถูกเลือก | ☐ |
| 2 | TYPE qty/date ของ known-price fixture | — | compare input พร้อม | ☐ |
| 3 | SELECT source currency → สกุลเงินเป้าหมาย | — | target currency เท่าต้นทาง | ☐ |
| 4 | CLICK `คำนวณ` | — | ต้นทุนต่อหน่วยก่อนภาษี = `11.00` | ☐ |
| 5 | OPEN รายละเอียดผลหรือรายการราคา | — | เห็น `ราคาฉบับที่ {N} · รหัสอ้างอิง {VPL-ID}` และรายละเอียดคำนวณที่ตรวจย้อนกลับได้ | ☐ |
| 6 | VERIFY raw trace payload | — | formula version, price, price_per, discount, freight, qty/date/FX ครบ `⚠ รายละเอียดเต็มไม่พบใน HTML — ต้อง simulate API` | ☐ |

#### TC-CMP-07 — resolve explicit vendor และกรณีไม่มีราคา

- Group/Priority/Trace: Resolution · P0 · AC-13, BR-VPL-16/19
- Actor: downstream service
- Setup: `role=downstream service · seed=DS-PRICE explicit vendor candidates · files=— · inject=resolve API harness with scoped service token`
- Start route: N/A — API harness; ใช้หน้า `#/vendor-price-list/compare` เป็น visual evidence เท่านั้น
- Data set: DS-PRICE
- Pass criteria: resolve ไม่จัดอันดับหลาย vendor และคืน 1 answer หรือ explicit error

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN API request `resolve explicit vendor` ใน harness | explicit vendor/product/UOM/currency/qty/date | ได้ candidate ของ vendor ที่ระบุเพียงหนึ่งคำตอบ พร้อม version/trace `(ต้อง simulate)` | ☐ |
| 2 | OPEN API request `resolve without vendor` ใน harness | same other inputs | ถูก validation block; compare เท่านั้นที่จัดอันดับหลาย vendor `(ต้อง simulate)` | ☐ |
| 3 | OPEN API request `resolve no tier` ใน harness | date/qty ที่ไม่มี tier มีผล | ได้ `NO_APPLICABLE_PRICE` พร้อมเหตุผล ไม่คืน null เงียบ `(ต้อง simulate)` | ☐ |

### กลุ่ม G — Security, Permission, Concurrency และ Idempotency

#### TC-SEC-01 — concurrent edit/approval ให้คำตอบเดียว

- Group/Priority/Trace: Concurrency · P0 · AC-16, EC-11
- Actor: two authorized sessions
- Setup: `role=procurement_manager A+B · seed=DS-CONC · files=— · inject=two sessions sharing the same ETag`
- Start route: `#/vendor-price-list`
- Data set: DS-CONC
- Pass criteria: first valid commit wins; second conflict; ไม่มีสอง active/audit success

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN pending record เดียวกันใน session A และ B | same ETag/version | ทั้งคู่เห็น `รออนุมัติ` `(ต้อง simulate two sessions)` | ☐ |
| 2 | CLICK `อนุมัติ` และยืนยันใน A | — | A สำเร็จเป็น `ใช้งาน` | ☐ |
| 3 | CLICK `อนุมัติ` และยืนยันใน B | — | B ได้ `ERR_STALE_DATA` หรือ `ERR_ALREADY_DECIDED`; UI refresh เป็น `ใช้งาน` | ☐ |
| 4 | VERIFY history | — | มี approval success หนึ่งเหตุการณ์เท่านั้น | ☐ |

#### TC-SEC-02 — retry mutation ด้วย idempotency key

- Group/Priority/Trace: Idempotency · P0 · AC-16
- Actor: procurement_officer/API client
- Setup: `role=procurement_officer · seed=DS-MASTER · files=— · inject=API proxy that drops first response and reuses idempotency key`
- Start route: API harness
- Data set: DS-MASTER
- Pass criteria: same key/body คืนผลเดิม; same key/different body conflict

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN API request `create/commit K body A` โดย proxy ทิ้ง response แรก | body A | server commit หนึ่งครั้ง `(ต้อง simulate)` | ☐ |
| 2 | OPEN API request `retry K body A` | body A | คืน record/result เดิม; count เท่าหลัง step 1 | ☐ |
| 3 | OPEN API request `retry K body B` | body B | ได้ `ERR_IDEMPOTENCY_CONFLICT`; record ยังมี body A | ☐ |

#### TC-SEC-03 — permission matrix และ role เปลี่ยนระหว่างทำรายการ

- Group/Priority/Trace: Authorization · P0 · AC-14, Permission Matrix
- Actor: ทุก role ใน DS-ROLE
- Setup: `role=DS-ROLE each · seed=DS-PRICE · files=— · inject=auth switcher + mid-flight role revoke`
- Start route: `#/vendor-price-list`
- Data set: DS-ROLE
- Pass criteria: capability ตรง matrix; server recheck role ทุก mutation

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN หน้าเป็น procurement_officer/manager/director/admin | — | เห็นราคา; create/edit/import/submit/status ตาม matrix; approve เฉพาะ role+DOA+SoD `(ต้อง simulate)` | ☐ |
| 2 | OPEN เป็น finance_viewer | — | เห็นราคาและ view/compare; ไม่เห็นหรือใช้ create/import/submit/approve/status action ไม่ได้ `(ต้อง simulate)` | ☐ |
| 3 | OPEN เป็น other authenticated | — | เห็น list แบบราคาถูก mask; mutation action ไม่มี `(ต้อง simulate)` | ☐ |
| 4 | CLICK submit หลัง revoke permission ระหว่างเปิด drawer | — | ได้ `ERR_PERMISSION_REVOKED`; UI ปิด/refresh ตาม policy; ไม่มี write `(ต้อง simulate)` | ☐ |
| 5 | OPEN โดยไม่มี auth | — | ไป login/401 behavior; raw data ไม่ปรากฏ `(ต้อง simulate)` | ☐ |

#### TC-SEC-04 — Confidential ไม่รั่วใน UI/export/log/analytics

- Group/Priority/Trace: Data classification · P0 · BR-VPL-13, EC-15
- Actor: other authenticated
- Setup: `role=other authenticated · seed=DS-PRICE confidential · files=— · inject=masked projection + access to sanitized test logs/events`
- Start route: `#/vendor-price-list`
- Data set: DS-ROLE, DS-PRICE
- Pass criteria: raw price/discount/freight/landed/FX/change% ไม่อยู่ในทุก channel ที่ไม่มีสิทธิ์

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN list/view/compare เป็น masked role | — | ค่า Confidential แสดง placeholder/masked; ค้น source/DOM ไม่พบ raw value `(ต้อง simulate; HTML fixture ยังแสดงราคา)` | ☐ |
| 2 | CLICK export/print ถ้ามีใน implementation | — | raw fields ถูก omit/mask; ความพยายามถูก audit `(ต้อง simulate)` | ☐ |
| 3 | VERIFY application logs, network payload และ analytics event | correlation ID ของ run | ไม่มี raw Confidential values `(ต้อง simulate)` | ☐ |

#### TC-SEC-05 — tenant/company scope และ downstream projection

- Group/Priority/Trace: RLS/service scope · P0 · AC-14, EC-16
- Actor: procurement_manager tenant A + downstream service
- Setup: `role=procurement_manager/downstream service · seed=two tenants/companies · files=— · inject=tenant A/B tokens and scoped service token`
- Start route: `#/vendor-price-list`
- Data set: DS-ROLE, DS-PRICE
- Pass criteria: ไม่มีข้อมูลข้าม tenant/company และ service ได้เฉพาะ granted scope

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN list/search/detail ด้วย session tenant A | IDs ของ tenant B | ไม่พบ record tenant B; direct ID ได้ not-found-in-scope `(ต้อง simulate RLS)` | ☐ |
| 2 | OPEN API request `downstream scoped read` | one company/vendor | payload มีเฉพาะ scope ที่ granted และ field projection ตามสิทธิ์ `(ต้อง simulate)` | ☐ |
| 3 | VERIFY historical snapshot ผ่าน authorized service | existing transaction | snapshot อ่านได้แต่แก้ไม่ได้; masked UI ไม่ได้รับ raw snapshot `(ต้อง simulate)` | ☐ |

### กลุ่ม H — Cross-module และ Integration Contract

#### TC-XT-01 — Vendor เปลี่ยนจาก active หลังเปิด picker

- Group/Priority/Trace: Cross-module · P0 · XT-01, BR-VPL-02/14
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-XT vendor active→blocked · files=— · inject=F-VENDOR status event controller`
- Start route: `#/vendor-price-list`
- Data set: DS-XT
- Pass criteria: mutation/resolve/compare recheck live status; historyไม่ถูกลบ

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN drawer `สร้างรายการราคา` | — | drawer เปิด | ☐ |
| 2 | SELECT vendor active | — | vendor ถูกเลือกได้ | ☐ |
| 3 | OPEN fixture action `vendor active → blocked` | — | F-VENDOR event/cache ถูกอัปเดต `(ต้อง simulate)` | ☐ |
| 4 | CLICK `ยืนยันและส่งอนุมัติ` | — | เห็น `สถานะคู่ค้าเปลี่ยนแล้ว รายการใหม่นี้ไม่สามารถส่งได้`; ไม่มี record ใหม่ | ☐ |
| 5 | VERIFY ผล compare/resolve และ historyเดิม | — | vendor ถูก exclude จากใหม่ แต่ประวัติราคาเดิมยังอ่านได้ `(ต้อง simulate integration)` | ☐ |

#### TC-XT-02 — Product เปลี่ยนเป็น obsolete/ซื้อไม่ได้

- Group/Priority/Trace: Cross-module · P0 · XT-02, BR-VPL-03
- Actor: procurement_officer
- Setup: `role=procurement_officer · seed=DS-XT product active→obsolete · files=— · inject=Product status event controller`
- Start route: `#/vendor-price-list`
- Data set: DS-XT
- Pass criteria: new mutation/resolve/compare block; historical snapshot readable

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN drawer `สร้างรายการราคา` | — | drawer เปิด | ☐ |
| 2 | SELECT คู่ค้า active | — | ช่องสินค้าเลือกได้ | ☐ |
| 3 | SELECT active+purchasable product | — | เลือกได้และ UOM แสดงจาก Product Master | ☐ |
| 4 | OPEN fixture action `product → obsolete/purchasable=false` | — | event/cache update `(ต้อง simulate)` | ☐ |
| 5 | CLICK submit/compare ใน harness | — | เห็น `สินค้าไม่อยู่ในสถานะใช้งานหรือซื้อไม่ได้`; ไม่มีคำตอบราคาใหม่ | ☐ |
| 6 | OPEN transaction/history ก่อนเปลี่ยน | — | snapshot เดิมยังอ่านได้ `(ต้อง simulate)` | ☐ |

#### TC-XT-03 — Vendor API-20 summary เป็น façade ของ VPL

- Group/Priority/Trace: Cross-module ownership · P0 · XT-03, LOCK-VPL-16
- Actor: procurement_manager/API client
- Setup: `role=procurement_manager · seed=DS-XT known VPL counts · files=— · inject=VPL API-15 + F-VENDOR API-20 + DB inspection harness`
- Start route: API harness; visual check vendor drill-in
- Data set: DS-XT
- Pass criteria: Vendor summary = VPL summary และ Vendor ไม่เก็บ price rows ซ้ำ

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN API request `VPL API-15 summary` | vendor fixture | ได้ counts/status summaryและจดไว้อ้างใน step 2 `(ต้อง simulate)` | ☐ |
| 2 | OPEN API request `F-VENDOR API-20 summary` | same vendor | ค่าทุก count ตรงค่าที่จดจาก step 1 | ☐ |
| 3 | VERIFY Vendor persistence/schema | — | ไม่มี duplicated price/version/tier rows ใน F-VENDOR; owner ยังเป็น VPL `(ต้อง simulate)` | ☐ |

#### TC-XT-04 — DOA config เปลี่ยนหลัง submit ไม่เปลี่ยน route เงียบ

- Group/Priority/Trace: Cross-module policy · P0 · XT-04, LOCK-VPL-04/05
- Actor: procurement_manager
- Setup: `role=procurement_manager · seed=DS-XT threshold v1=10%, v2=5% · files=— · inject=versioned DOA config controller`
- Start route: `#/vendor-price-list`
- Data set: DS-XT
- Pass criteria: pending request ใช้ submit-time policy snapshot ที่ตรวจย้อนหลังได้

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `ยืนยันและส่งอนุมัติ` สำหรับ version change 7% เมื่อ threshold=10% | — | pending route normal; audit เก็บ policy/config version v1 `(ต้อง simulate)` | ☐ |
| 2 | OPEN fixture action `central threshold v2=5%` | — | config v2 มีผลกับ submit ใหม่เท่านั้น | ☐ |
| 3 | OPEN pending เดิมและ approval audit | — | route เดิมไม่เปลี่ยนเงียบ; เห็น snapshot v1 `(ต้อง simulate)` | ☐ |
| 4 | CLICK `ยืนยันและส่งอนุมัติ` สำหรับ version ใหม่ 7% | — | ใช้ elevated route ตาม v2 `(ต้อง simulate)` | ☐ |

#### TC-XT-05 — FX service unavailable/missing/stale

- Group/Priority/Trace: Cross-module FX · P0 · XT-05, EC-10
- Actor: procurement_officer/downstream service
- Setup: `role=procurement_officer/downstream service · seed=DS-XT FX missing/stale/down · files=— · inject=FX service fault controller + monitoring read`
- Start route: `#/vendor-price-list/compare`
- Data set: DS-XT, DS-FX
- Pass criteria: compare/resolve fail explicitly และไม่ fallback

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | CLICK `คำนวณ` เมื่อ FX service down | — | แสดง error ที่ผู้ใช้เข้าใจได้; ไม่แสดงอันดับเท็จ `(ต้อง simulate)` | ☐ |
| 2 | OPEN API request `resolve with missing/stale dated FX` | — | ได้ `ERR_FX_UNAVAILABLE` พร้อม reason/date; ไม่มี price snapshot `(ต้อง simulate)` | ☐ |
| 3 | VERIFY monitoring | correlation ID | FX failure ถูกนับ/แจ้งเตือนโดยไม่มี raw Confidential leak `(ต้อง simulate)` | ☐ |

#### TC-XT-06 — PR/RFQ/PO เก็บราคาฉบับและรายละเอียดคำนวณเดิม

- Group/Priority/Trace: Cross-module snapshot · P0 · XT-06, BR-VPL-20, LOCK-VPL-09
- Actor: procurement_officer/downstream service
- Setup: `role=downstream service · seed=DS-XT resolved VPL then later changed · files=— · inject=PR/RFQ/PO API + mutable VPL/FX fixtures`
- Start route: API harness; visual anchor `ราคาฉบับที่ {N} · รหัสอ้างอิง {VPL-ID}`
- Data set: DS-XT
- Pass criteria: transaction เดิมไม่ recalculate เมื่อ VPL/FX เปลี่ยน

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN API scenario `resolve explicit vendor → create PR/RFQ/PO line` | qty/date/currency | transaction เก็บ `price_version_id` + calculation snapshot/trace `(ต้อง simulate)` | ☐ |
| 2 | CLICK test-harness action `approve new VPL version + change FX` | — | current resolve เปลี่ยนตามข้อมูลใหม่ | ☐ |
| 3 | OPEN transaction เดิม | — | ราคา/version/formula inputs เดิมไม่เปลี่ยน; แสดงรหัสอ้างอิงตรวจย้อนหลังได้ `(ต้อง simulate)` | ☐ |

#### TC-XT-07 — source precedence Contract > VPL > manual override

- Group/Priority/Trace: Cross-module sourcing · P0 · XT-07, BR-VPL-21
- Actor: procurement_officer/downstream service
- Setup: `role=downstream service · seed=DS-XT approved Contract + approved VPL + authorized manual override · files=— · inject=Contract/VPL/override resolve harness`
- Start route: API harness; VPL compare remains visual evidence
- Data set: DS-XT
- Pass criteria: approved Contract ถูกเลือกก่อน; VPL ยังอยู่เป็น evidence; manual ใช้เมื่อ authorized ตาม policy

| # | Action | Input | Expected | Result |
|---:|---|---|---|---|
| 1 | OPEN API scenario `Contract + VPL both applicable` | same vendor/product/UOM/date/qty | source ที่เลือกเป็น approved Contract; VPL candidate ยังแสดงเป็น lower-priority evidence `(ต้อง simulate)` | ☐ |
| 2 | OPEN API scenario `Contract unavailable; VPL applicable` | — | เลือก approved VPL | ☐ |
| 3 | OPEN API scenario `manual override denied/allowed` | two role fixtures | role แรก block; role หลังเลือก override ตาม policy พร้อม audit `(ต้อง simulate)` | ☐ |
| 4 | VERIFY UI scope | — | ไม่มี contract editor ใน Vendor Price List ตาม LOCK-VPL-12 | ☐ |

## วิธีที่ agent รัน (Run protocol)

1. เปิด `vendor-price-list-v6.html` ผ่าน local HTTP server หรือ implementation environment ที่ route/hash ทำงานได้ ห้ามสรุปผลจากการอ่าน source
2. Reset fixture และ refresh ก่อนทุก test case; กรณี delta ให้จด baseline count/status/value ก่อน action เสมอ
3. รัน P0 ก่อน P1 ตามลำดับกลุ่ม A→H เพื่อให้ master/approval/snapshot dependency อ่านง่าย แต่ทุกเคสต้อง independent
4. Action ต้องหา control จากข้อความที่เห็นบนจอ เช่น `สร้างรายการราคา` ไม่ใช้ selector, ID หรือชื่อฟังก์ชัน
5. รอเงื่อนไขเฉพาะ เช่น toast, route, status, row count หรือ enabled state; ห้ามใช้ fixed sleep เพื่อกลบอาการค้าง
6. ถ้า expected มี `⚠ ไม่พบใน HTML` ให้รันกับ implementation/API harness และบันทึก `BLOCKED` เมื่อไม่มี environment; ห้ามให้ PASS จาก prototype mock
7. เก็บ screenshot เมื่อ FAIL/BLOCKED โดยให้เห็น route, anchor, input และ expected ที่ขาด; เก็บ response code/correlation ID เฉพาะเคส simulate
8. ผลแต่ละ step ใช้ `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`; เคสผ่านเมื่อทุก step เป็น PASS เท่านั้น
9. หลังจบตรวจว่า raw Confidential data ไม่ติด screenshot/log/report ของ role ที่ไม่มีสิทธิ์

## Coverage Audit

| รายการตรวจ | เป้าหมาย | ผลก่อนรัน |
|---|---:|---|
| Test cases | 62 | ☐ ยังไม่รัน |
| P0 / P1 | 57 / 5 | ☐ ยังไม่รัน |
| FR/Acceptance Criteria (06_TESTS) | 16/16 | ☐ mapped |
| Business Rules | 21/21 | ☐ mapped |
| Edge Cases | 16/16 | ☐ mapped |
| Field validations | 14/14 | ☐ mapped |
| Error catalog codes | 27/27 | ☐ mapped |
| Permission cells | 42/42 | ☐ mapped |
| Cross-cutting/events/states/UI states | 17/17 | ☐ mapped |
| Cross-module XT | 7/7 | ☐ mapped |
| Scope Locks | 17/17 accounted: 15 verified + 2 OOS skipped | ☐ mapped |
| Routes | 4/4 + unknown | ☐ mapped |
| UI-visible vs simulate separation | ทุก expected ที่ไม่มีใน HTML มี marker | ☐ verify |
| Coverage Manifest | Stories 5/5 · Rules 21/21 · Edges 16/16 | ☐ mapped |

- Manifest cross-check: ✅ 42/42
- `[AI-DEFAULT]` propagation: 0/0 — FRD pack ไม่มี tag นี้
- ข้าม LOCK-VPL-12: AVL/contract editor/lead/MOQ/preferred/attachment/OCR/AI recommendation เป็นนอกขอบเขตใบเซ็น จึงห้ามสร้างเคสของฟังก์ชันเหล่านี้
- ข้าม LOCK-VPL-13: business A4/PDF เป็นนอกขอบเขตใบเซ็นและไม่มีเอกสารให้ทดสอบ

สิ่งที่ AI/browser ตรวจจาก HTML อย่างเดียวไม่ได้: server-side authorization/RLS, API status/error code, transaction atomicity, WORM immutability, idempotency, optimistic concurrency, DOA/SLA scheduler, event delivery, database ownership, raw application logs/analytics, real Vendor/Product/FX/Contract/PR-RFQ-PO integration และ performance SLO. รายการเหล่านี้ต้องใช้ implementation environment, deterministic fixture และ API/DB observability ที่ได้รับอนุญาต

## Result Report (schema)

```json
{
  "feature_id": "F-VENDOR-PRICELIST-001",
  "source_html": "outputs/F-VENDOR-PRICELIST-001/vendor-price-list-v6.html",
  "run_id": "string",
  "started_at": "ISO-8601",
  "finished_at": "ISO-8601",
  "environment": {
    "base_url": "string",
    "build": "string",
    "browser": "string",
    "viewport": "string",
    "fixture_version": "string"
  },
  "summary": {
    "total": 62,
    "pass": 0,
    "fail": 0,
    "blocked": 0,
    "not_run": 62
  },
  "cases": [
    {
      "id": "TC-NAV-01",
      "status": "PASS|FAIL|BLOCKED|NOT_RUN",
      "actor": "procurement_officer",
      "start_route": "#/vendor-price-list",
      "started_at": "ISO-8601",
      "finished_at": "ISO-8601",
      "steps": [
        {
          "no": 1,
          "status": "PASS|FAIL|BLOCKED|NOT_RUN",
          "observed": "ข้อความที่เห็นจริง",
          "screenshot": "relative/path.png",
          "response_code": null,
          "correlation_id": null
        }
      ],
      "evidence": ["relative/path.png"],
      "defect_id": null,
      "note": "string"
    }
  ],
  "coverage": {
    "acceptance_criteria": "16/16",
    "business_rules": "21/21",
    "edge_cases": "16/16",
    "cross_module": "7/7",
    "scope_locks": "17/17"
  },
  "limitations": [
    "รายการที่ BLOCKED เพราะไม่มี API/role/master fixture",
    "สิ่งที่ตรวจจาก browser อย่างเดียวไม่ได้"
  ]
}
```
