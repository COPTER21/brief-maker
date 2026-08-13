# Coverage Report — Sales Territory (รอบ 1: HTML)

- วันที่: 2026-08-13
- Artifact: `../01_HTML/sales-territory.html` · route `#/sales-territory`
- Baseline override: PM/BA อนุมัติให้ใช้ `PREBRIEF_F-SALES-TERRITORY.md` + `FUNCTION_CHECKLIST_F-SALES-TERRITORY.md` + ทุกไฟล์ใน `Central Plan v2` แทน `workflow_graph.json`/`NODE_BRIEF`
- ข้อจำกัด: baseline นี้ไม่มี machine-readable severity/edge contract แบบ workflow graph; จึงตัดสินเฉพาะสิ่งที่ประกาศชัดใน Brief/Checklist และไม่ invent ERP contract เพิ่ม
- สถานะ downstream: Sales Team / Salesperson, Customer Master, Sales Order, Sales Target และ Visit Operation ยังไม่มี; PM/BA ให้ทำเพียง mock/future hooks และห้าม hard dependency

## Verdict: 🟡 WARN

สรุปตาม approved baseline: ครอบคลุม UI/mock behavior หลัก, lifecycle, validation, workload และแผนที่แล้ว ไม่พบ BLOCK ที่ยืนยันได้จาก baseline แต่มี 4 รายการที่ยังเป็น partial/NOT-CHECKED เพราะ OQ หรือ feature ปลายทางยังไม่พร้อม

| Covered | Partial / WARN | NOT-CHECKED | Scope creep |
|---:|---:|---:|---:|
| 37 | 3 | 3 | 0 |

## Coverage Matrix — PREBRIEF §0 Obligations

| Item | HTML | Evidence / หมายเหตุ |
|---|---|---|
| OB-1 Territory เป็นมิติบนเอกสารขาย/รายงาน | △ | บรรทัด 512 ประกาศการใช้เป็นมิติ; เอกสาร/รายงานปลายทางยังไม่มี จึงเป็น future hook |
| OB-2 1 เขต = พนักงานขาย 1 คน | ✓ | ฟอร์มมี salesperson combobox หนึ่งค่าและ required validation ใน save flow บรรทัด 854–865, 982–1007 |
| OB-3 soft ref Salesperson; ไม่สร้างคนที่นี่ | ✓ mock | contract/mock comments บรรทัด 424–440; combobox บรรทัด 910–913; ไม่มี create-person action |
| OB-4 ภาคเลือกเองตามชุด | ✓ | `REGIONS` บรรทัด 390 และ select บรรทัด 854 |
| OB-5 จังหวัด optional/77 จังหวัด | ✓ | `PROVINCES` บรรทัด 409; combobox บรรทัด 906; save รองรับ `—` บรรทัด 996 |
| OB-6 customer/coverage/order/workload read-only | ✓ mock | `CUST` บรรทัด 461–466; calculated display บรรทัด 468–595; ไม่มี editor ของค่าปลายทาง |
| OB-7 soft archive/restore + append-only audit | ✓ prototype | `AUDIT`/`pushAudit` บรรทัด 478–479; archive/restore บรรทัด 1012–1047; ไม่มี hard delete |
| OB-8 code unique/locked หลังสร้าง | ✓ | regex+duplicate check บรรทัด 988; edit drawer แสดง code แบบล็อก |
| OB-9 historical snapshot | NOT-CHECKED | UI มี microcopy แต่ต้องพิสูจน์กับเอกสาร/รายงานปลายทาง ซึ่งยังไม่มี |
| OB-10 ไม่มี DOA | ✓ | ไม่พบ approval/DOA flow ใน HTML |
| OB-11 แผนที่ไทย offline interactive | ✓ | inline `THMAP` บรรทัด 389; map tab บรรทัด 525; interaction/panel บรรทัด 599–778 |

## Coverage Matrix — PREBRIEF §2/§11 + Function Checklist

| Scenario / Function | HTML | Evidence / หมายเหตุ |
|---|---|---|
| S-01 / FN-01 create Route | ✓ | `openCreate` บรรทัด 784; form/save บรรทัด 812–1007 |
| FN-02 Route เป็นตัวเลือกเอกสารขาย | △ future hook | บันทึก Route ได้ แต่ document feature ยังไม่มี; baseline override ยอมรับการเตรียม hook |
| S-02 / FN-03 view-first → edit; code locked | ✓ | `openView/openEdit` บรรทัด 785–786; view/edit drawer |
| S-03 / FN-04 malformed/duplicate code blocked | ✓ | validation บรรทัด 988 และ field error flow |
| S-04 / FN-05–06 archive + customer warning | ✓ | confirm modal/linked-customer warning บรรทัด 1012–1042 |
| S-05 / FN-07 restore | ✓ | `restoreRoute` บรรทัด 1044–1047 |
| S-06 / FN-08 optional province | ✓ | province combobox + `—` fallback บรรทัด 906, 996 |
| S-07 / FN-09 required region/salesperson | ✓ | required fields + save validation บรรทัด 854–865, 982–1007 |
| S-08 / FN-10 Salesperson master empty | △ mock | search-no-result empty copy ชี้ Sales Team/Salesperson บรรทัด 910–913; ยังไม่มี runtime “master ทั้งชุดว่าง” เพราะใช้ mock list |
| S-09 / FN-11 inactive salesperson | NOT-CHECKED | PREBRIEF ระบุรอ OQ-03; HTML ไม่จำลอง inactive binding |
| S-10 / FN-12 one rep, multiple Routes | ✓ mock | workload aggregates active routes by rep บรรทัด 573–595 |
| S-11 / FN-13 universe empty | ✓ mock | `routeStats` รองรับ null coverage; table แสดง `—` บรรทัด 468–476, 556 |
| S-12 / FN-14 document snapshot | NOT-CHECKED | ต้องมีเอกสารปลายทางเพื่อยืนยันว่าเอกสารเก่าไม่เปลี่ยน |
| S-13 / FN-15 coverage threshold/color | ✓ mock | threshold 25% บรรทัด 556 และ map cards บรรทัด 688 |
| S-14 / FN-16 workload formula/utilization | ✓ mock | F4/F2/F1, prospect และ capacity บรรทัด 467–476, 573–595 |
| S-15 exclusivity ไม่รองรับ | ✓ scope guard | ไม่มี validation ห้ามเขตซ้อน |
| S-17 team assignment ไม่รองรับ | ✓ scope guard | form เลือก salesperson คนเดียว ไม่มี team assignment |
| S-18 hard delete/code edit ไม่รองรับ | ✓ scope guard | ไม่มี hard-delete action; code ล็อกใน edit |
| S-19 / FN-19 offline 77-province map | ✓ | inline dataset/map rendering บรรทัด 389–409, 599–778 |
| S-20 / FN-20 hover tooltip/panel | ✓ | `mapTip` บรรทัด 649; move/hover update บรรทัด 733–778 |
| S-21 / FN-21 pin/drill/clear | ✓ | `mapSelect` บรรทัด 726; clear action บรรทัด 694; route card opens drawer |
| S-22 / FN-22 region filter | ✓ | filter uses `REGIONS`; filtered panel/tooltip บรรทัด 601–721 |
| S-23 / FN-23 unmapped routes | ✓ | “ไม่ลงแผนที่” panel บรรทัด 721 พร้อม route drill |
| S-24 / FN-24 clear hover | ✓ | hover/tooltip reset behavior บรรทัด 733–778 |
| S-25/S-26 no full route line/GPS pins | ✓ scope guard | ไม่มี customer GPS pin หรือ visit route-line flow |
| FN-17 audit append-only | ✓ prototype | all create/edit/archive/restore call `pushAudit`; UI persistence เป็น implementation concern รอบหลัง |
| FN-18 view-first/Esc/future links | ✓ mock | view-first drawer; Esc chain; Customer/Visit buttons บรรทัด 831–832 แจ้งว่ายังไม่พร้อม |
| FN-90 search/status/group by region | ✓ | query/status filter บรรทัด 488–503; grouped table บรรทัด 535–570 |

## Coverage Matrix — PREBRIEF §4 Business Rules

| Rule | HTML | Evidence / หมายเหตุ |
|---|---|---|
| BR-01 code format/unique/immutable | ✓ | บรรทัด 988 และ locked edit presentation |
| BR-02 name required | ✓ | form error/validation ใน save flow |
| BR-03 region required/independent | ✓ | region select from fixed list |
| BR-04 province optional/system dataset | ✓ | optional combobox and dataset membership handling |
| BR-05 one salesperson required | ✓ | single required combobox |
| BR-06 Salesperson soft reference | ✓ mock | mock contract and lookup-only combobox; no person creation |
| BR-07 snapshot | NOT-CHECKED | backend/downstream behavior; destination features absent |
| BR-08 append-only audit | ✓ prototype | in-memory audit log with no edit/delete history action |
| BR-09 Roles & Permissions | NOT-CHECKED | PREBRIEF §1 ระบุ role behavior เป็น AI-DRAFT/OQ-02; ไม่มี approved permission matrix ให้ตัดสิน |
| BR-10 soft archive/restore | ✓ | archive/restore handlers; no hard delete |
| BR-11 downstream metrics read-only | ✓ mock | calculated display only |

## Edge Matrix — PREBRIEF §9 (approved baseline override)

| Edge | HTML | Evidence / สถานะ |
|---|---|---|
| E-1 Customer Master → Territory | △ mock hook | customer/coverage mock; Customer button แจ้ง “ยังไม่พร้อม” บรรทัด 831 |
| E-2 Sales Order → Territory | △ mock hook | `orders90` mock and read-only totals; no SO dependency |
| E-3 Sales Team/Salesperson → Territory | △ mock hook | candidate shape/mock บรรทัด 424–440; no hard dependency |
| E-4 geo dataset → Territory | ✓ offline | inline 77-province dataset บรรทัด 389–409 |
| E-5 Roles & Permissions → Territory | NOT-CHECKED | permission contract ยังไม่เคาะ (OQ-02) |
| E-6 Territory → Quotation/SO | △ future hook | Territory dimension/snapshot intent present; destination absent |
| E-7 Territory → sales report/dashboard | △ future hook | local dashboard mock exists; report destination absent |
| E-8 Territory → Visit Operation | △ mock hook | button and payload intent present; destination absent บรรทัด 832 |

## Central Plan v2 Cross-check

Central Plan ระบุ Sales Territory เป็น feature ใน Sales และมี linkage `Sales Territory → Customer Master`, `→ Visit Operation`, `→ Sales Target`; linkage เหล่านี้สอดคล้องกับการเตรียม future hooks และไม่พบ HTML ที่สร้าง hard dependency ไปยัง feature ที่ยังไม่มี

Sales Target ไม่ปรากฏใน PREBRIEF §9 edge register จึงไม่เพิ่ม action/flow ใหม่ใน HTML; เก็บเป็น future integration note ตาม PM/BA confirmation เพื่อไม่ invent scope

## 🟡 Warnings / Gaps

### GAP-01 · Salesperson-master-empty state เป็นเพียง search empty

- ขาด: demo state เมื่อ endpoint/master ทั้งชุดคืนค่า 0 รายการตาม S-08/FN-10
- สถานะ: WARN; ปัจจุบันมีข้อความ no-result ที่ถูกต้อง แต่ mock list มีข้อมูลเสมอ
- แก้ที่: HTML state fixture หลัง PM/BA ยืนยันว่าต้องมี demo toggle; **ไม่แก้รอบนี้เพราะจะเพิ่ม scope/state เอง**

### GAP-02 · Inactive salesperson ยังไม่จำลอง

- ขาด: old binding + warning + required reselection ตาม S-09/FN-11
- สถานะ: NOT-CHECKED; PREBRIEF ผูก OQ-03 ชัดเจน
- แก้ที่: หลัง OQ-03 เคาะ ให้เติม mock inactive record และ edit validation ใน HTML/FRD

### GAP-03 · Snapshot พิสูจน์ end-to-end ไม่ได้

- ขาด: evidence ว่าเอกสาร/รายงานเก่าไม่เปลี่ยนหลัง edit/archive Territory
- สถานะ: NOT-CHECKED; ปลายทางยังไม่มี
- แก้ที่: FRD logic/API + test case รอบ 2 และ integration test เมื่อ Sales Order/report พร้อม

### GAP-04 · Permission behavior ยังไม่มี approved contract

- ขาด: role-to-action matrix สำหรับ create/edit/archive/restore/read-only
- สถานะ: NOT-CHECKED; PREBRIEF ระบุ AI-DRAFT/OQ-02
- แก้ที่: PM/BA เคาะ OQ-02 ก่อน FRD; ห้าม hardcode role ใน HTML ตอนนี้

## Scope / Drift Result

- ไม่พบ hard dependency ไปยัง future 5 features
- ไม่พบ hard delete, team assignment, geographic exclusivity, customer GPS pins หรือ visit route lines
- Sales Target ถูกเก็บเป็น future noteเท่านั้น ไม่มี flow ที่แต่งเพิ่ม
- รอบนี้ไม่แก้ HTML เพราะ gaps ทั้งหมดต้องอาศัย OQ/downstream contract หรือ PM/BA decision ก่อน

## Gate Decision

Coverage รอบ 1 ตาม PM/BA-approved baseline override = **WARN, ไม่ BLOCK** และพร้อมหยุดที่ GATE เพื่อ manual test/PM-BA review ก่อนเริ่ม skill 5+.
