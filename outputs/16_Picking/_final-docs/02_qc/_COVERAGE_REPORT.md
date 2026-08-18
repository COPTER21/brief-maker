# COVERAGE REPORT รอบ 1 — F-WH-PICK Picking

**วันที่:** 18 สิงหาคม 2569
**Artifact ที่ตรวจ:** f-wh-picking.html, PICK_template.html, PICK_sample.pdf
**ผล:** PASS WITH GOVERNANCE WARN
**FN:** 29/29 มี evidence ในหน้าจอหรือ negative contract

## Source set และ precedence

1. Scope Lock จากคำตอบผู้ใช้ 1–11
2. PREBRIEF และ Function checklist 29 FN
3. Central Plan v2 ทุกไฟล์
4. Locked refs: Sales Order, Inventory, Warehouse, Item Master, organization-management, employee-management
5. Packing/Delivery Note ยังไม่มี ref จึงตรวจเฉพาะ handoff จาก Pick ไม่กำหนด contract ภายในของปลายทาง

## Scope Lock ที่ override เอกสารตั้งต้น

- Wave อยู่ S5 และ payment gate บล็อกตอนสร้างใบหยิบ
- รหัสคลังยึด Warehouse Master; ค่าใน SO เป็น mock
- หนึ่ง location เก็บหนึ่ง lot
- Auto allocation ใช้ ERP standard + PREBRIEF; Pick เป็นเจ้าของ FEFO/FIFO precedence
- Manual override ใช้ hard eligibility เดียวกับ auto และข้ามได้เฉพาะลำดับ priority
- Assignee เห็นพนักงานทั้งหมดก่อน ยังไม่แยกคลัง/แผนก
- Picker ย้ายตำแหน่งและปิดงานแบบขาดเองได้
- Customer pickup เดิน Pack → Delivery Note ตามปกติ
- Pick รับ upstream source จาก SO เท่านั้น; source อื่นไม่ trigger เข้าคิว Pick

## FN evidence matrix

| FN | ผล | Evidence ใน HTML / เอกสาร |
|---|---|---|
| FN-01 | ✓ | gate, queueRows, renderRows แสดง SO, ลูกค้า, คลัง, กำหนดส่ง, คงเหลือ, gate, priority |
| FN-02 | ✓ | gate บล็อก after_full/after_deposit; checkbox disabled; mockPay จำลอง Finance release |
| FN-03 | ✓ | gate บล็อก hold; soPickable ตัด service; pickup อยู่คิวปกติ; backorder ไม่ถูกเพิ่มใน qty หยิบ |
| FN-04 | ✓ | soRemaining, openPickQty, soPickStatus, openSoModal แสดงฐาน/หยิบแล้ว/ใบเปิด/คงเหลือ |
| FN-05 | ✓ | toggleSO, savePick, CFG.waveMax, same-warehouse guard และ canManage |
| FN-06 | ✓ | isPickEligible, candidateBals, sortBals, allocateSO, routeSort; ไม่มี strategy dropdown |
| FN-07 | ✓ | savePick เพิ่ม allocated ระดับ balance/location และออก PICK-2026-* เป็น draft/assigned |
| FN-08 | ✓ | openRelocModal, confirmReloc ปล่อยจองเดิม/จองใหม่และ pushAudit |
| FN-09 | ✓ | allocateSO สร้าง short line; linesTable แสดง หาใหม่/เลือกเอง/ขอเติม |
| FN-10 | ✓ | assigneeCombo, cbOpen/cbKey/cbPick, workload, equipment, priority, note และเปลี่ยนผู้หยิบ |
| FN-11 | ✓ | canManage, canPick, persona switch, งานของฉัน และ action ตาม role; picker ทำ relocation/short close ของใบตนได้ |
| FN-12 | ✓ | startPick, pickProgress, progress unit/line |
| FN-13 | ✓ | openPickLineModal, scan tiles, qty stepper, confirmPickLine; update on_hand/alloc/SO picked และ movement |
| FN-14 | ✓ | partial quantity, reason chips และ action short ใน paintPickLine/confirmPickLine |
| FN-15 | ✓ | action relocate บันทึกส่วนแรกแล้วเปิด openRelocModal สำหรับส่วนเหลือ |
| FN-16 | ✓ | refreshOne/refreshLine อ่าน balance ล่าสุด; สำเร็จแล้ว allocate+audit, ไม่พบมี warning/request action |
| FN-17 | ✓ | candidatesFor แบบ manual ยังเรียก isPickEligible; manual ข้าม priority แต่ไม่ข้าม hard constraints |
| FN-18 | ✓ | requestReplenish สรุปขาด/Reserve/Bulk/คลังอื่นและสร้าง Inventory task แบบ mock |
| FN-19 | ✓ | action หยิบครบทั้งหมดและ status guard ให้ picked เมื่อทุกบรรทัดจบและมี qty หยิบ |
| FN-20 | ✓ | action ส่งต่อ Packing สร้าง PACK ต่อ SO, อัปเดต SO/pick และ audit; pickup ใช้ flow เดียวกัน |
| FN-21 | ✓ | openShortCloseModal เหตุผล, release allocation, SO backorder และพร้อมส่ง Packing เฉพาะที่ได้ |
| FN-22 | ✓ | hold reason modal, คง allocation และ resumePick |
| FN-23 | ✓ | cancel เฉพาะ draft/assigned, reason, release allocation และ SO กลับคิว |
| FN-24 | ✓ negative | SRC_TYPES มี SO เท่านั้น, refLabel ไม่มีประเภทอื่น และไม่มี TR_BY/TRANSFER/RTV/PRODUCTION |
| FN-90 | ✓ | renderListPage: 2 tabs, search/filter/งานของฉัน/export/row drawer และ full-height table |
| FN-91 | ✓ | renderViewDrawer, tabBtn: lines/detail SO/print/history + status/role actions |
| FN-92 | ✓ | pdfTab และชุด PICK_template.html, PICK_sample.pdf, PICK_print-spec.md |
| FN-93 | ✓ | document Esc chain, cbKey, backdrop/X/close action และ keyboard combobox |
| FN-94 | ✓ | pushAudit แสดง history แบบ append-only และ MOVEMENTS อ้าง pick+SO |

## Cross-feature edges

| Edge | ผล | Evidence / ขอบเขต |
|---|---|---|
| Sales Order → Pick | ✓ | confirmed/reserved/not held/payment gate; SO-only queue and drilldown |
| Inventory → Pick | ✓ | balance, on_hand, allocated, lot/expiry, stock/location hard eligibility |
| Warehouse/Location → Pick | ✓ | Warehouse Master code, location type/status/pickable/output block, route sequence |
| Item Master → Pick | ✓ | goods vs service, lot flag, UOM/factor, FEFO/FIFO strategy |
| Employee/IAM → Pick | ✓ | person/role/workload plus action permission; assignee pool not split yet |
| Pick → Inventory | ✓ | hard allocation, release, movement pick, replenishment/transfer request mock |
| Pick → Packing | ✓ | handoff PACK per SO and picked quantities; Packing internal contract not invented |
| Packing → Delivery Note | △ out of scope | customer pickup ยังเดินเส้นปกติ; รอ ref ของ Packing/DN ตอนทำ feature นั้น |

## Exception and negative coverage

- รอชำระ, hold, already-open pick, service item, backorder, no eligible location
- cross-warehouse wave, waveMax, manual blocked location, other-warehouse stock display-only
- partial/short, relocation, replenish request, hold/resume, cancel before start, close-short after start
- viewer read-only, picker own-task action, manager full action
- upstream source ที่ไม่ใช่ SO ไม่ปรากฏและไม่ trigger

## Governance WARN

- Central Plan ชุดนี้ไม่มี workflow_graph.json/NODE_BRIEF สำหรับ F-WH-PICK จึงใช้ PREBRIEF coverage matrix + global contracts + locked refs แทนตาม source ที่ผู้ใช้ยืนยัน
- Packing/Delivery Note ref ยังไม่มี จึงห้ามขยาย contract ภายในปลายทาง; จุดนี้ไม่บล็อก Pick เพราะ handoff และ ownership boundary ชัดเจนแล้ว

## Verdict

PASS WITH GOVERNANCE WARN — rerun หลัง PM/BA ให้ซ่อนปุ่มไอคอนใบเติมรายบรรทัด; กลไก mock ภายในคงเดิม, WF ยังครบ 29/29 และ feature E2E ผ่าน 14/14
# Round 2 — FRD + Test Cases vs Contract (2026-08-18)

## Verdict: PASS

| Contract item | HTML | FRD | TC | Evidence |
|---|---|---|---|---|
| SO queue gates/remaining | ✓ | ✓ | ✓ | UI queue; `05_RULES` BR-PICK-01/02; TC-Q01..Q05 |
| create/wave/allocation | ✓ | ✓ | ✓ | create drawer; BR-PICK-03..07 + ENG-01; TC-C01..C07 |
| assignment/role/ownership | ✓ | ✓ | ✓ | assignee combo/persona; BR-PICK-08; TC-A01..A04 |
| pick/scan/quantity | ✓ | ✓ | ✓ | pick-line modal; FN-07; TC-P01..P03 |
| short/relocate/refresh/manual | ✓ | ✓ | ✓ | line actions/modals; BR-PICK-07,09..11; TC-P03..P06 |
| Inventory request boundary | ✓ | ✓ | ✓ | internal mock/no row icon; BR-PICK-12; TC-P07/P08 |
| finish/hold/cancel/close-short | ✓ | ✓ | ✓ | status actions; BR-PICK-13..15; TC-X01/X02 |
| Packing handoff | ✓ | ✓ | ✓ | toPack; API-15/FN-16; XT-03/06, TC-X02/X03 |
| Inventory/Sales effects | ✓ | ✓ | ✓ | movements/backorder mock; API contracts; XT-01/02 |
| notification events | ✓ | ✓ | ✓ | audit hooks; NTF brief + outbox; XT-04/05 |
| SO-only source lock | ✓ | ✓ | ✓ | no non-SO UI; BR-PICK-17; TC-Q06 |
| A4/Esc/audit | ✓ | ✓ | ✓ | print/Esc/history; AT-23; TC-U01/U02 |

### Round 2 audit

- Block rules in FRD: 17/17
- Confirmed and AI-default edge cases in FRD: 12/12
- Test coverage: FN 29/29; XT 6/6; LOCK 12/12
- N/A-UI backend controls retained: concurrency, idempotency, downstream failure, NTF retry — all have simulated cases
- Scope creep: none; Transfer/Replenishment/RTV/Production positive flow remains excluded
- Diff from Round 1: HTML evidence unchanged; FRD and TC columns are now complete

---
