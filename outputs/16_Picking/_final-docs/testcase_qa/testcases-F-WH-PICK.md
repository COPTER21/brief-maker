# AI Test Cases — F-WH-PICK Picking

ทดสอบจาก FRD FULL pack + BRD + `f-wh-picking.html`. Anchor ข้อความยึด HTML จริง; เคสหลังบ้านที่ prototype ไม่มี UI ระบุ `(ต้อง simulate)`.

## Meta

| Item | Value |
|---|---|
| Feature / version | F-WH-PICK / 1.0 |
| App entry | เปิด `f-wh-picking.html#/list` |
| Routes | `#/list`, `#/create/:soId`, `#/view/:pickId` |
| Sources | BRD, FRD_Pack, HTML, checklist FN-01..24/FN-90..94 |
| Cases | 32 cases / 6 groups |

## Coverage

| Group | Cases | Priority |
|---|---:|---|
| Queue/list | 6 | P0/P1 |
| Create/allocation | 7 | P0/P1 |
| Assignment/permission | 4 | P0/P1 |
| Pick/exception | 8 | P0/P1 |
| Completion/integration | 5 | P0/P1 |
| UX/print/resilience | 2 | P1/P2 |

## Coverage Ledger

### Acceptance / FN

| Items | Cases |
|---|---|
| AT-01..02 / FN-01..04 | TC-Q01..Q06 |
| AT-03..07 / FN-05..09 | TC-C01..C07 |
| AT-08..09 / FN-10..11 | TC-A01..A04 |
| AT-10..16 / FN-12..18 | TC-P01..P08 |
| AT-17..22 / FN-19..24 | TC-X01..X05, TC-Q06 |
| AT-23 / FN-90..94 | TC-U01..U02 + relevant flow cases |

### Business Rules

| Rules | Cases |
|---|---|
| BR-PICK-01..04 | TC-Q01..Q06, TC-C01,C02 |
| BR-PICK-05..07 | TC-C03..C07, TC-P04..P06 |
| BR-PICK-08..11 | TC-A01..A04, TC-P01..P06 |
| BR-PICK-12..17 | TC-P07,P08, TC-X01..X05, TC-Q06,U02 |

### Edge / errors

| Item | Cases |
|---|---|
| EC-01..07 | TC-Q02,Q03,Q04,C06,P03,P04,U02 |
| EC-08 `[AI-DEFAULT]` / ERR_STALE_DATA | TC-X04 |
| EC-09 `[AI-DEFAULT]` / ERR_IDEMPOTENCY_CONFLICT | TC-X05 |
| EC-10 `[AI-DEFAULT]` | TC-C07 |
| EC-11 `[AI-DEFAULT]` | TC-X03 |
| EC-12 `[AI-DEFAULT]` | TC-X02 |
| role/not-assignee errors | TC-A03,A04 |
| source/gate/wave errors | TC-Q02,Q06,C02 |
| location/scan/qty/reason/transition errors | TC-C06,P02,P03,P04,X01 |
| downstream unavailable | TC-X02,X03 |

### Permission cells

| Cell | Cases |
|---|---|
| wh_lead view/create/assign/cancel/pick | TC-C01,A01,X01,P01 |
| picker own view/pick/close-short | TC-A02,P01,P03,X01 |
| picker create/other record deny | TC-A03 |
| viewer read allow/mutation deny | TC-A04 |

### Cross-module

| XT | Case |
|---|---|
| XT-01 Inventory allocation/release | TC-C01,X01 |
| XT-02 Inventory+SO pick/short | TC-P02,P03 |
| XT-03 Packing | TC-X02,X03 |
| XT-04 notification events | TC-A01,P03,X02 |
| XT-05 NTF down | TC-X02 |
| XT-06 Packing down | TC-X03 |

### Scope Locks

| LOCK | Case |
|---|---|
| 01–02 S5/create entry | TC-Q01,C01 |
| 03–04 master/one-lot | TC-C03,C04 |
| 05–06 ERP allocation/exceptions | TC-C03..C07,P03..P08 |
| 07 permission | TC-A01..A04 |
| 08 all assignees | TC-A01 |
| 09 picker self-service | TC-A02,P01,P03 |
| 10 pickup→Packing/DN normal | TC-Q05,X02 |
| 11 SO-only | TC-Q06 |
| 12 no download-like row icon | TC-P08 |

## Data Sets

| Set | Values |
|---|---|
| Q-READY | SO-2026-0207, pickup, CASH, gate passed, WH-01 |
| Q-PAY | SO-2026-0205/0206, payment not passed |
| Q-HOLD | SO-2026-0200, hold |
| Q-OPEN | SO-2026-0203, open PICK-2026-0891 |
| WAVE | two eligible WH-01 SO; plus one eligible WH-02 SO for negative |
| PICK | PICK-2026-0891 assigned/in-progress seed |
| PEOPLE | สมชาย ใจดี, วิภาวี ตั้งมั่น, ธนพล แสนสุข, ปรียา ศรีสมบัติ, อนุชา ว่องไว |
| SHORT | item required more than eligible balance; picked part >0 |

## Test Cases

### Queue / List

### TC-Q01 — SO พร้อมส่งเข้าคิว (happy)
- group: Queue · priority P0 · trace: AT-01/FN-01/BR-PICK-01
- actor: wh_lead
- Setup: role=wh_lead · seed=Q-READY · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: SO พร้อมส่งเลือกได้และข้อมูลหลักครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | เห็นหัวข้อ “ใบหยิบสินค้า (Picking)” และแท็บ “คิวรอหยิบ (SO)” | ☐ |
| 2 | TYPE `SO-2026-0207` → ช่องค้นหา | Q-READY | เห็นแถว SO พร้อม checkbox ใช้งานได้ | ☐ |
| 3 | VERIFY ข้อมูลแถว | — | เห็นลูกค้า คลัง กำหนดส่ง วิธีรับ รายการ คงเหลือ สถานะ และ priority | ☐ |

### TC-Q02 — payment gate บล็อกและปล่อยใหม่ (negative)
- group: Queue · P0 · trace: FN-02/EC-01/BR_PICK_QUEUE_GATE_FAILED
- actor: wh_lead
- Setup: role=wh_lead · seed=Q-PAY · files=—
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `SO-2026-0205` → ช่องค้นหา | Q-PAY | เห็นสถานะรอชำระและ checkbox disabled | ☐ |
| 2 | CLICK action Finance รับเงิน (เดโม) | — | toast แจ้งผลเดโมและคิวถูกประเมินใหม่ | ☐ |
| 3 | VERIFY แถวเดิม | — | เปลี่ยนเป็นพร้อมหยิบและเลือกได้ | ☐ |

### TC-Q03 — hold บล็อก; pickup ยังหยิบ (negative + lock)
- Setup: role=wh_lead · seed=Q-HOLD,Q-READY · files=—
- actor: wh_lead · trace: FN-03/LOCK-10
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `SO-2026-0200` → ช่องค้นหา | Q-HOLD | แถวพักเลือกไม่ได้ | ☐ |
| 2 | TYPE `SO-2026-0207` → ช่องค้นหา | Q-READY | แถวมารับเองเลือกได้ตามปกติ | ☐ |
| 3 | CLICK แถว SO มารับเอง | — | รายละเอียดไม่มี logic DN พิเศษใน Pick | ☐ |

### TC-Q04 — open Pick/partial remaining
- Setup: role=wh_lead · seed=Q-OPEN · files=—
- actor: wh_lead · trace: FN-04/EC-02
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `SO-2026-0203` → ช่องค้นหา | Q-OPEN | เห็น “มีใบหยิบค้าง” และเลือกไม่ได้ | ☐ |
| 2 | CLICK แถว SO | — | modal แสดงสั่ง/จอง/หยิบ/ในใบหยิบ/คงเหลือ/backorder และใบที่เกี่ยวข้อง | ☐ |

### TC-Q05 — service ไม่เป็นบรรทัดหยิบ
- Setup: role=wh_lead · seed=SO มีสินค้า+บริการ · files=—
- actor: wh_lead · trace: FN-03/BR-PICK-02
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว SO ที่มีค่าบริการ | — | รายละเอียดต้นทางเห็นบริการได้ | ☐ |
| 2 | CLICK “สร้างใบหยิบ” สำหรับ SO นี้ | — | wizard ไม่มีบรรทัดบริการในรายการหยิบ | ☐ |

### TC-Q06 — source อื่นไม่เข้า Pick (negative contract)
- Setup: role=wh_lead · seed=TR/Replenishment/RTV/Production refs · files=—
- actor: wh_lead · trace: FN-24/LOCK-11/BR_PICK_SOURCE_NOT_ALLOWED
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ทุก tab/filter/source label | — | ไม่มีคิวหรือชนิดต้นทาง Transfer/Replenishment/RTV/Production | ☐ |
| 2 | VERIFY API create `(ต้อง simulate)` | source_type=TRANSFER | ได้ 422 `BR_PICK_SOURCE_NOT_ALLOWED`; ไม่มี Pick ใหม่ | ☐ |

### Create / Allocation

### TC-C01 — สร้างใบหยิบเดี่ยวแบบ assigned
- Setup: role=wh_lead · seed=Q-READY + balances · files=—
- actor: wh_lead · trace: FN-05..07/XT-01
- Start: OPEN `#/create/SO-2026-0207`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/create/SO-2026-0207` | — | drawer ขั้น 1 เปิดและ SO ถูกเลือก | ☐ |
| 2 | CLICK “ถัดไป” | — | ขั้น 2 เปิด; ผู้หยิบ/อุปกรณ์/priority/หมายเหตุแสดง | ☐ |
| 3 | SELECT `วิภาวี ตั้งมั่น` → “ผู้หยิบ” | PEOPLE | selected value แสดงกลางช่อง ไม่ชิดบนล่าง | ☐ |
| 4 | CLICK “ถัดไป” | — | ขั้น 3 แสดง route/location/lot/qty/rule | ☐ |
| 5 | CLICK “บันทึกและมอบหมาย” | — | toast สำเร็จ; ได้รหัส PICK-; route ไป view; status มอบหมายแล้ว | ☐ |
| 6 | VERIFY allocation baseline `(ต้อง simulate)` | — | Inventory allocated เพิ่มเท่าผลรวมบรรทัดครั้งเดียว | ☐ |

### TC-C02 — wave same warehouse / mixed/max blocked
- Setup: role=wh_lead · seed=WAVE · files=—
- actor: wh_lead · trace: FN-05/BR-PICK-03/BR_PICK_WAVE_INVALID
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TOGGLE checkbox SO WH-01 สองใบ | WAVE | ปุ่ม “สร้างใบหยิบ (2 SO)” enabled | ☐ |
| 2 | TOGGLE checkbox SO WH-02 | WAVE | เห็น “รวม wave ได้เฉพาะ SO คลังเดียวกัน” | ☐ |
| 3 | VERIFY max `(ต้อง simulate)` | waveMax+1 | เห็น warning “wave สูงสุด” และไม่สร้างใบ | ☐ |

### TC-C03 — FEFO lot allocation
- Setup: role=wh_lead · seed=item lot มี 2 expiry ใน WH-01 · files=—
- actor: wh_lead · trace: FN-06/BR-PICK-05/LOCK-03..05
- Start: OPEN `#/create/SO-2026-0207`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไปขั้น 3 | — | บรรทัด lot item แสดง rule FEFO | ☐ |
| 2 | VERIFY ลำดับล็อต | — | expiry ใกล้สุดมาก่อน และแบ่งหลายตำแหน่งเมื่อจำเป็น | ☐ |
| 3 | VERIFY ลำดับ route | — | Pick Face ก่อน Reserve/Bulk แล้วเรียง Zone›Area›Rack›Location | ☐ |

### TC-C04 — FIFO non-lot allocation
- Setup: role=wh_lead · seed=non-lot item หลาย balance · files=—
- actor: wh_lead · trace: FN-06/BR-PICK-05/LOCK-04
- Start: OPEN `#/create/:soId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไปขั้น 3 | — | non-lot line แสดง FIFO | ☐ |
| 2 | VERIFY allocation | — | ไม่มี dropdown กลยุทธ์; ตำแหน่งตาม type/route และหนึ่ง location หนึ่ง lot | ☐ |

### TC-C05 — relocate ใน wizard
- Setup: role=wh_lead · seed=บรรทัดมี candidate อื่น · files=—
- actor: wh_lead · trace: FN-08
- Start: OPEN `#/create/:soId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนตำแหน่งในบรรทัดขั้น 3 | — | modal “เปลี่ยนตำแหน่ง/ล็อต” แสดง candidates เรียงถูก | ☐ |
| 2 | CLICK “ใช้ตำแหน่งนี้” | — | toast “เปลี่ยนตำแหน่งแล้ว (จองจริงเมื่อบันทึก)” | ☐ |

### TC-C06 — no eligible balance creates short
- Setup: role=wh_lead · seed=SHORT ไม่มี eligible balance · files=—
- actor: wh_lead · trace: FN-09/EC-03/BR_PICK_LOCATION_INELIGIBLE
- Start: OPEN `#/create/:soId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไปขั้น 3 | SHORT | เห็นบรรทัดขาด ไม่มีตำแหน่ง แต่ยังบันทึกใบได้ | ☐ |
| 2 | VERIFY actions | — | เห็น “หาใหม่” และไอคอนเลือกตำแหน่ง; ไม่เห็นปุ่ม download-like | ☐ |

### TC-C07 — stale/inactive master revalidation `[AI-DEFAULT]`
- Setup: role=wh_lead · seed=เปิด wizard แล้ว deactivate candidate ก่อน save `(ต้อง simulate)` · files=—
- actor: wh_lead · trace: EC-10/BR_PICK_LOCATION_INELIGIBLE
- Start: OPEN `#/create/:soId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY candidate ที่เห็นก่อน | — | จด location/lot ที่เลือกไว้ | ☐ |
| 2 | CLICK “บันทึกและมอบหมาย” หลัง inject inactive | — | ไม่ commit allocation; แสดง conflict/eligibility error ให้ refresh | ☐ |

### Assignment / Permission

### TC-A01 — assignee combobox all people + keyboard
- Setup: role=wh_lead · seed=PEOPLE/workloads · files=—
- actor: wh_lead · trace: FN-10/LOCK-08
- Start: OPEN `#/create/SO-2026-0207`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง “ผู้หยิบ” | — | options เปิดเหนือ drawer ไม่ถูกบัง; เห็นทุกคนพร้อม role/คลัง/งานค้าง/badge | ☐ |
| 2 | TYPE `วิภาวี` → search | PEOPLE | เหลือ option ที่ตรง | ☐ |
| 3 | PRESS ArrowDown แล้ว Enter | — | option ถูกเลือกและ selected display มีระยะบนล่างเหมาะสม | ☐ |
| 4 | PRESS Esc หลังเปิดใหม่ | — | popover ปิดแต่ drawer ยังเปิด | ☐ |

### TC-A02 — picker operates own assignment
- Setup: role=picker วิภาวี · seed=PICK assigned to วิภาวี · files=—
- actor: picker · trace: FN-11/LOCK-09
- Start: OPEN `#/view/PICK-2026-0891`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN route | PICK | เห็นใบของตนและปุ่ม “เริ่มหยิบ” | ☐ |
| 2 | CLICK “เริ่มหยิบ” | — | toast “เริ่มหยิบ — บันทึกทีละบรรทัด (สแกน)” และ actions หยิบปรากฏ | ☐ |

### TC-A03 — picker denied create/other pick
- Setup: role=picker · seed=Pick assigned to another person · files=—
- actor: picker · trace: FN-11/ERR_NOT_ASSIGNEE
- Start: OPEN `#/list`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY page header | — | ไม่มีปุ่มสร้างใบหยิบ | ☐ |
| 2 | OPEN `#/view/:otherPick` | — | mutation buttons ของอีกคนไม่แสดง | ☐ |
| 3 | VERIFY direct mutation `(ต้อง simulate)` | — | 403 `ERR_NOT_ASSIGNEE` | ☐ |

### TC-A04 — viewer read-only
- Setup: role=viewer · seed=PICK · files=—
- actor: viewer · trace: FN-11/ERR_INSUFFICIENT_ROLE
- Start: OPEN `#/view/PICK-2026-0891`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY 4 tabs and details | — | อ่านข้อมูลได้ | ☐ |
| 2 | VERIFY action area | — | ไม่มี mutation actions; direct API returns 403 `(ต้อง simulate)` | ☐ |

### Pick / Exception

### TC-P01 — start and progress
- Setup: role=picker assigned · seed=PICK assigned · files=—
- actor: picker · trace: FN-12
- Start: OPEN `#/view/PICK-2026-0891`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “เริ่มหยิบ” | — | status กำลังหยิบ; progress แสดงหน่วย/บรรทัด | ☐ |

### TC-P02 — full line pick with scans
- Setup: role=picker assigned · seed=in_progress line allocated qty>0 · files=—
- actor: picker · trace: FN-13/XT-02
- Start: OPEN `#/view/:pickId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “บันทึกหยิบ” ที่บรรทัด | — | modal scan/stepper เปิด; confirm disabled | ☐ |
| 2 | CLICK กล่องสแกนตำแหน่ง | allocated location | สถานะ scan location ✓ | ☐ |
| 3 | CLICK กล่องสแกนสินค้า/ล็อต | allocated item/lot | “สแกนครบ ✓”; confirm enabled | ☐ |
| 4 | CLICK “ยืนยันหยิบครบ” | full qty | toast แสดงจำนวนที่บันทึก; line เป็นหยิบแล้ว; progress เพิ่ม | ☐ |
| 5 | VERIFY delta `(ต้อง simulate)` | baseline on_hand/alloc/SO picked | on_hand และ alloc ลด qty; SO picked เพิ่ม qty; movement ref Pick+SO | ☐ |

### TC-P03 — partial short + reason/event
- Setup: role=picker assigned · seed=SHORT in_progress · files=—
- actor: picker · trace: FN-14/BR-PICK-09,10/XT-02,04
- Start: OPEN `#/view/:pickId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “บันทึกหยิบ” และสแกนครบ | — | quantity control พร้อมใช้ | ☐ |
| 2 | SELECT จำนวนต่ำกว่าต้องหยิบ | SHORT | เหตุผล chips + short/relocate choices แสดง | ☐ |
| 3 | CLICK “ยืนยัน · รายงานขาด” โดยไม่เลือกเหตุผล | — | ปุ่มยัง disabled/แจ้งต้องระบุเหตุผล | ☐ |
| 4 | SELECT เหตุผล “ของไม่พอ” แล้ว CLICK ยืนยัน | — | บันทึกส่วนที่ได้; remainder short; allocation release; backorder; event `pick_short` `(simulate downstream)` | ☐ |

### TC-P04 — partial relocate + hard eligibility
- Setup: role=picker assigned · seed=partial qty + candidates including forbidden types · files=—
- actor: picker · trace: FN-15,17/BR_PICK_LOCATION_INELIGIBLE
- Start: OPEN `#/view/:pickId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT partial qty and action “ไปหยิบตำแหน่งอื่น” | — | modal candidates เปิด | ☐ |
| 2 | VERIFY candidate list | — | same WH active eligible only; HOLD/STAGING/PACK/blocked/frozen/inactive ไม่เลือกได้ | ☐ |
| 3 | CLICK “ใช้ตำแหน่งนี้” | eligible candidate | first part saved; remainder allocated new location; audit exists | ☐ |

### TC-P05 — refresh no stock
- Setup: role=picker assigned · seed=short line no location/no stock · files=—
- actor: picker · trace: FN-16
- Start: OPEN `#/view/:pickId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “หาใหม่” | — | toast “ยังไม่มีสต๊อกที่หยิบได้ — ขอเติม/โอน หรือรอ GRN แล้วกดหาใหม่” | ☐ |

### TC-P06 — refresh after inventory inbound
- Setup: role=picker assigned · seed=short line + inbound balance added `(ต้อง simulate)` · files=—
- actor: picker · trace: FN-16/BR-PICK-11
- Start: OPEN `#/view/:pickId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY line ก่อน refresh | — | ไม่มี location และ status short | ☐ |
| 2 | CLICK “หาใหม่” | inbound balance | toast พบสต๊อก/จอง; line มี location/lot; allocated เพิ่มครั้งเดียว | ☐ |

### TC-P07 — Inventory request mechanism `(ต้อง simulate)`
- Setup: role=wh_lead · seed=short line no stock · files=—
- actor: wh_lead · trace: FN-18/BR-PICK-12
- Start: OPEN `#/view/:pickId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY internal contract call | short qty | แสดง need/local reserve/other WH/task type และสร้าง Inventory task; ไม่สร้าง Pick source ใหม่ | ☐ |

### TC-P08 — removed replenishment icon
- Setup: role=wh_lead · seed=short line · files=—
- actor: wh_lead · trace: FN-18/LOCK-12
- Start: OPEN `#/view/:pickId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY action ท้ายบรรทัดขาด | — | มี “หาใหม่” และไอคอนตำแหน่ง; **ไม่มี** icon/button รูป download สำหรับขอเติม | ☐ |

### Completion / Integration

### TC-X01 — hold/resume/cancel guards
- Setup: role=wh_lead · seed=assigned Pick และ in_progress Pick · files=—
- actor: wh_lead · trace: FN-22,23/BR-PICK-15
- Start: OPEN `#/view/:pickId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “พัก” แล้วเว้นเหตุผล | — | “กรุณาระบุเหตุผล” | ☐ |
| 2 | TYPE เหตุผลแล้ว CLICK “พัก” | ตรวจสินค้า | status พัก; allocation เท่าเดิม | ☐ |
| 3 | CLICK “หยิบต่อ” | — | status กลับกำลังหยิบ | ☐ |
| 4 | VERIFY cancel หลังเริ่ม | — | ไม่มี/ถูก block; ต้องใช้ปิดขาด | ☐ |
| 5 | OPEN assigned Pick แล้ว CLICK ยกเลิกพร้อมเหตุผล | — | toast “ยกเลิกแล้ว”; allocation release; SO กลับคิว | ☐ |

### TC-X02 — finish and Packing + NTF resilience
- Setup: role=picker assigned · seed=all lines terminal with picked>0 · files=—
- actor: picker · trace: FN-19,20/XT-03,04,05
- Start: OPEN `#/view/:pickId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “หยิบครบ” | — | toast “หยิบครบ — พร้อมส่งต่อ Packing”; status picked | ☐ |
| 2 | CLICK “ส่งต่อ Packing” | — | toast มี PACK ref; status to_pack; หนึ่ง ref ต่อ SO | ☐ |
| 3 | VERIFY NTF down `(ต้อง simulate)` | inject ENG-NOTIFY down | Pick/Pack result ไม่ย้อน; event queued | ☐ |

### TC-X03 — Packing unavailable/retry `[AI-DEFAULT]`
- Setup: role=picker assigned · seed=picked Pick; Packing down `(ต้อง simulate)` · files=—
- actor: picker · trace: EC-11/XT-06
- Start: OPEN `#/view/:pickId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK “ส่งต่อ Packing” | — | error visible; status remains picked; retry action remains | ☐ |
| 2 | CLICK “ส่งต่อ Packing” หลัง service ฟื้น | same idempotency key | ได้ PACK ref เดียว ไม่มี duplicate | ☐ |

### TC-X04 — optimistic conflict `[AI-DEFAULT]`
- Setup: role=wh_lead · seed=same Pick opened by two sessions `(ต้อง simulate)` · files=—
- actor: wh_lead · trace: EC-08/ERR_STALE_DATA
- Start: OPEN `#/view/:pickId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK mutation จาก session A | version N | สำเร็จและ version เพิ่ม | ☐ |
| 2 | CLICK mutation จาก session B | stale version N | 409 stale; เห็น prompt/reload; ไม่มี side effect ซ้ำ | ☐ |

### TC-X05 — idempotent retry `[AI-DEFAULT]`
- Setup: role=wh_lead · seed=eligible SO `(ต้อง simulate request retry)` · files=—
- actor: wh_lead · trace: EC-09/ERR_IDEMPOTENCY_CONFLICT
- Start: OPEN `#/create/:soId`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK save แล้ว retry request เดิม | key K/body A | ได้ Pick เดิม; allocation/audit/event ไม่เพิ่มซ้ำ | ☐ |
| 2 | VERIFY key K/body B | changed body | 409 idempotency conflict | ☐ |

### UX / Print

### TC-U01 — Esc chain and overlay stack
- Setup: role=wh_lead · seed=create drawer + combo/modal available · files=—
- actor: wh_lead · trace: FN-93
- Start: OPEN `#/create/SO-2026-0207`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK assignee combobox | — | popover above drawer, not clipped | ☐ |
| 2 | PRESS Esc | — | combobox closes, drawer remains | ☐ |
| 3 | OPEN a modal then PRESS Esc | — | modal closes first, drawer remains | ☐ |
| 4 | PRESS Esc | — | drawer closes and route returns list | ☐ |

### TC-U02 — 4 tabs, print A4, audit
- Setup: role=viewer · seed=PICK with long Thai item/audit · files=—
- actor: viewer · trace: FN-91,92,94/EC-07
- Start: OPEN `#/view/PICK-2026-0891`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tabs “รายการหยิบ”, “รายละเอียด · SO”, “ใบหยิบ”, “ประวัติ” | — | แต่ละ tab แสดงเนื้อหาถูกประเภท | ☐ |
| 2 | CLICK “พิมพ์” | — | A4 route-sorted columns + 3 signature areas; Thai text wraps/readable | ☐ |
| 3 | VERIFY “ประวัติ” | — | state/allocation/override/movement refs append-only และมี actor/time | ☐ |

## วิธีที่ agent รัน

รันแต่ละเคสแบบ independent: reset prototype/seed, login persona ตาม Setup, เปิด Start route ใหม่, ทำ Action ตาม verb ทีละแถว, บันทึกสิ่งที่เห็นจริงและ screenshot เมื่อ fail. เคส `(ต้อง simulate)` ใช้ API/fixture harness; ถ้าไม่มีให้ mark blocked ไม่เดาผล.

## Coverage Audit

| Category | Covered / Total |
|---|---:|
| Acceptance/FN groups | 29 / 29 |
| Business rules | 17 / 17 |
| Edge cases | 12 / 12 |
| Error catalog groups | 13 / 13 |
| Important permission cells | 9 / 9 |
| Cross-module XT | 6 / 6 |
| Scope Locks | 12 / 12 |
| Routes/overlays/print/audit | 3 routes + critical states covered |

- skipped implementation cases: none in-scope; backend-only items are retained as `(ต้อง simulate)`
- out-of-scope Pack/DN logic, real replenishment/cycle count, RF gun, zone picking, non-SO source flows: no positive feature cases created
- Manifest cross-check (FRD §0.12): ✅ 9/9 rows

## Result Report (schema)

```json
{"feature_id":"F-WH-PICK","run_at":"<iso datetime>","results":[{"id":"TC-Q01","status":"pass|fail|blocked","failed_step":null,"evidence":"","note":""}],"summary":{"total":32,"pass":0,"fail":0,"blocked":0}}
```
