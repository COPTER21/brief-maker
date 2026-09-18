# AI Test Cases — F-WH-STKTRF Stock Transfer

ชุดทดสอบสำหรับ browser/vision agent ยึดข้อความจริงจาก HTML และ route hash จริง ผลทุกขั้นตรวจด้วยสิ่งที่มองเห็นได้

## Meta

| Field | Value |
|---|---|
| Feature | F-WH-STKTRF · Stock Transfer |
| Version | FRD 1.0 / HTML 2026-09-17 |
| App entry | เปิด `F-WH-STKTRF.html` |
| Routes | `#/list`, `#/create`, `#/create/dup-:id`, `#/edit/:id`, `#/view/:id` |
| Sources | BRD v1.1, FRD Pack, HTML, UI Brief |
| Cases | 53 cases · 6 groups |

## Coverage

| Group | Cases | Priority |
|---|---:|---|
| A — lifecycle/happy/exception | 9 | High |
| V — validation and error | 21 | High |
| P — permission/SoD | 6 | High |
| L — list/UI/interaction | 6 | Medium |
| C — concurrency/atomic | 5 | High |
| X — cross-module/locks | 6 | High |

## Coverage Ledger

### Acceptance / stories

| Item | Cases |
|---|---|
| S-01 same-warehouse | TC-A01 |
| S-02/S-03 cross-warehouse shipment | TC-A02 |
| S-04 full receipt | TC-A02 |
| S-05 partial receipt | TC-A03 |
| S-06 shortage approval | TC-A04 |
| S-07 return | TC-A05 |
| S-08 cancel/reversal | TC-A06, TC-A07 |
| S-09 real-person DOA | TC-A08, TC-P05 |
| S-10 transit visibility | TC-L01, TC-L02 |

### Business rules and validations

| Item | Cases |
|---|---|
| BR-01 | TC-V10 |
| BR-02/03/05 | TC-A01, TC-A02, TC-V04 |
| BR-04 | TC-V07 |
| BR-06/07 | TC-V05, TC-V06 |
| BR-08/09b/10/11 | TC-V08, TC-P06 |
| BR-09 | TC-A09, TC-X01 |
| BR-12/13 | TC-A08, TC-P05 |
| BR-14 | TC-P02, TC-P03 |
| BR-15/16/17 | TC-A03, TC-V13 |
| BR-18 | TC-A04, TC-V15, TC-V16, TC-V17 |
| BR-19 | TC-A05 |
| BR-20 | TC-C01 |
| BR-21/22/23 | TC-A07, TC-P01, TC-V19 |
| BR-24 | TC-X06 |
| BR-25/26 | TC-A06, TC-C05, TC-V20 |
| BR-27 | TC-X03 |
| BR-28/29/30 | TC-X04, TC-C02, TC-L06 |
| BR-31/32/33 | TC-X05, TC-P06 |
| V-01..V-21 | TC-V01..TC-V21 one-to-one |

### Confirmed edge cases / errors

| Item | Cases |
|---|---|
| E-01..E-08 | TC-V05, TC-V06, TC-V07, TC-L05, TC-V04, TC-V08, TC-P06 |
| E-09..E-15 | TC-C01, TC-A03, TC-A04, TC-A05, TC-V13, TC-X03, TC-V19 |
| E-16..E-21 | TC-V20, TC-X04, TC-P02, TC-P03, TC-C02, TC-L03 |
| INVALID_STATE | TC-V19, TC-V20 |
| VERSION_CONFLICT | TC-C03 |
| DUPLICATE_ACTION | TC-C02 |
| INSUFFICIENT_STOCK | TC-C01 |
| RECEIVE_EXCEEDS_REMAINING | TC-V13 |
| TRANSIT_NOT_CONFIGURED | TC-V04 |
| LOCATION_NOT_ELIGIBLE | TC-V08 |
| APPROVER_REQUIRED | TC-V11 |
| SOD_VIOLATION | TC-P02, TC-P03 |
| EVIDENCE_REQUIRED | TC-V16 |
| FORBIDDEN_WAREHOUSE | TC-P03 |

### Permission, states, events, XT and locks

| Item | Cases |
|---|---|
| source officer create/edit/submit allow; ship deny | TC-P01 |
| source supervisor ship/reverse allow | TC-A02, TC-A06 |
| destination receive/return allow | TC-A02, TC-A05 |
| shipper receive/shortage approve deny | TC-P02 |
| non-destination receive deny | TC-P03 |
| read-only mutate deny | TC-P04 |
| current/non-current approver | TC-P05 |
| all 11 statuses | TC-A01..A09, TC-L01 |
| all 9 business events | TC-X03 |
| XT document engines | TC-X01 |
| XT DOA | TC-X02 |
| XT notification | TC-X03 |
| XT ledger/report | TC-X04 |
| XT compensating movement | TC-X05 |
| XT future JE disabled | TC-X06 |
| LK-1 Q/B2 | TC-L05 |
| LK-2/3/4 | TC-A01, TC-A02 |
| LK-5 | TC-X02 |
| LK-6 | TC-X01 |
| LK-7 | TC-X06 |
| LK-8 | TC-X05 |
| LK-9 | TC-P06 |
| LK-10 | TC-X05 |
| LK-11 | TC-L06 |

## Data Sets

| Set | Values |
|---|---|
| A | source `WH-BKK-01`, destination `WH-BKK-01`, source bin `A-01-01-A`, destination `C-01`, item `STA-PPR-A4`, qty 10 |
| B | source `WH-BKK-01`, destination `WH-CNX-01`, source bin `A-01-02-C`, destination `CNX-A-01-01-A`, item `STA-PEN-001`, qty 100 |
| C | B with receive 80, remaining 20, action `รอรับเพิ่ม` |
| D | B with receive 95, shortage 5, reason `ของหาย/เสียหายระหว่างทาง` |
| Invalid | qty 0, negative, above available, same bins, missing required fields |

### Files

- `transfer-note.pdf` — valid attachment.
- `shortage-evidence.jpg` — valid shortage evidence.
- `unsupported.exe` — invalid attachment type.

## Test Cases

### Group A — Lifecycle

### TC-A01 — ย้ายภายในคลังครบ flow (happy)
- group: lifecycle · priority: high · trace: S-01 / BR-03 / LK-2
- actor: source supervisor
- Setup: role=source_supervisor · seed=Set A stock available and approvers ready · files=—
- Start: `#/create`
- pass: status becomes `ย้ายสำเร็จ`; no receive step.

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/create` | Set A | drawer `สร้างใบย้ายสินค้า` opens | ☐ |
| 2 | SELECT source/destination warehouses and bins | Set A | mode indicates same warehouse; no transit location | ☐ |
| 3 | TYPE quantity and CLICK `บันทึกและส่งอนุมัติ` | 10 | approver modal opens; draft number text disappears after submit | ☐ |
| 4 | CLICK `อนุมัติ` for every current slot | — | status `อนุมัติแล้ว` | ☐ |
| 5 | CLICK `ย้ายสินค้า` then `ยืนยันย้ายสินค้า` | — | toast `พร้อมย้ายสินค้า`; status `ย้ายสำเร็จ` | ☐ |

### TC-A02 — ข้ามคลัง ส่งและรับครบ (happy)
- group: lifecycle · priority: high · trace: S-02..04 / BR-14..17 / LK-3,4
- actor: source supervisor then destination officer
- Setup: role identities for both warehouses · seed=Set B · files=—
- Start: `#/create`
- pass: transit step exists; destination closes with full receipt.

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/create` and SELECT Set B warehouses | B | mode says cross-warehouse; transit code is read-only | ☐ |
| 2 | TYPE line qty and CLICK `บันทึกและส่งอนุมัติ` | 100 | real-person approver selection appears | ☐ |
| 3 | CLICK `อนุมัติ` through chain | — | status `อนุมัติแล้ว` | ☐ |
| 4 | CLICK `ส่งออกจากต้นทาง` then `ยืนยันส่งออก` | — | CUBE modal closes; status `ส่งออกแล้ว — อยู่ระหว่างทาง` | ☐ |
| 5 | CLICK `ยืนยันรับ` as destination actor | receive 100 | receive modal shows sent/remaining/destination bin | ☐ |
| 6 | CLICK `ยืนยันรับ` | — | toast `รับครบแล้ว — ปิดใบ`; status `ปิดใบ (รับครบ)` | ☐ |

### TC-A03 — รับบางส่วนแล้วรับต่อ (exception)
- trace: S-05 / E-10 / BR-16
- Setup: role=destination_officer · seed=in_transit Set B remaining=100 · files=—
- Start: `#/view/:id`
- pass: first receipt leaves 20, second closes.

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ยืนยันรับ` | C receive 80 | modal accepts 80 and `รอรับเพิ่ม` | ☐ |
| 2 | CLICK `ยืนยันรับ` | — | toast `บันทึกการรับแล้ว — ยังค้างระหว่างทาง`; status `รับบางส่วน` | ☐ |
| 3 | CLICK `ยืนยันรับ` again | receive 20 | displayed remaining is 20 | ☐ |
| 4 | CLICK `ยืนยันรับ` | — | status `ปิดใบ (รับครบ)` | ☐ |

### TC-A04 — ตัดส่วนต่างครบสาย (exception)
- trace: S-06 / BR-18 / E-11
- Setup: role=destination_officer + shortage approvers · seed=in_transit 100 · files=shortage-evidence.jpg
- Start: `#/view/:id`
- pass: write-off occurs only after final approver.

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ยืนยันรับ` and TYPE received | 95 | shortage 5 is visible | ☐ |
| 2 | SELECT `ของหาย/เสียหายระหว่างทาง` and TYPE reason | D | request panel opens | ☐ |
| 3 | UPLOAD `shortage-evidence.jpg` | file | toast `แนบไฟล์แล้ว` | ☐ |
| 4 | CLICK `ยืนยันตัดส่วนต่าง` and select approvers | — | toast starts `ส่งขออนุมัติตัดส่วนต่างแล้ว — รอ`; status stays partial/pending | ☐ |
| 5 | CLICK `อนุมัติตัดส่วนต่าง` as each slot | — | intermediate step says `อนุมัติแล้ว — ส่งต่อ`; no close until final | ☐ |
| 6 | CLICK `อนุมัติตัดส่วนต่าง` as final slot | — | toast `อนุมัติครบสาย — ปิดใบพร้อมส่วนต่าง`; status matches | ☐ |

### TC-A05 — ตีกลับคืนต้นทาง
- trace: S-07 / BR-19 / E-12
- Setup: role=destination_officer · seed=in_transit remaining=100 · files=—
- Start: `#/view/:id`
- pass: returned, not shortage.

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ตีกลับคืนต้นทาง` | — | confirmation states `ไม่นับเป็นของหาย` | ☐ |
| 2 | TYPE reason and CLICK confirm | `ปลายทางไม่รับสินค้า` | toast `ตีกลับคืนต้นทางแล้ว — ของกลับเข้าช่องเก็บเดิมครบ`; status returned | ☐ |

### TC-A06 — กลับรายการหลังปิด
- trace: S-08 / BR-25,26 / E-16
- Setup: role=source_supervisor · seed=completed transfer not reversed · files=—
- Start: `#/view/:id`
- pass: new pending approval reversal; original changes only after completion.

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `กลับรายการ` | — | reason/approver flow opens | ☐ |
| 2 | TYPE reason and CLICK create | `เลือกปลายทางผิด` | toast starts `สร้างใบกลับรายการ`; new document is pending approval | ☐ |
| 3 | VERIFY original before reversal movement | — | original is not yet `กลับรายการแล้ว` | ☐ |
| 4 | CLICK approvals then execute reversal | — | original status `กลับรายการแล้ว`; reversal shows opposite route | ☐ |

### TC-A07 — ยกเลิกก่อน movement
- trace: S-08 / BR-21,22
- Setup: role=creator · seed=draft transfer · files=—
- Start: `#/view/:id`
- pass: cancelled; no stock movement.

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK cancel action | — | reason modal opens | ☐ |
| 2 | TYPE reason and CLICK confirm | `ไม่ใช้แล้ว` | toast includes `ยกเลิก`; status `ยกเลิก` | ☐ |
| 3 | VERIFY history/transit tab | — | no movement row exists | ☐ |

### TC-A08 — ไม่อนุมัติแล้วส่งใหม่
- trace: S-09 / BR-13
- Setup: role=current_approver then creator · seed=pending approval transfer · files=—
- Start: `#/view/:id`
- pass: reject requires reason, returns draft, same number reused.

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ไม่อนุมัติ` | — | reason required | ☐ |
| 2 | TYPE reason and CLICK confirm | `ข้อมูลไม่ครบ` | status `ร่าง`; number remains visible | ☐ |
| 3 | CLICK `แก้ไข`, correct data, then `ส่งอนุมัติ` | — | same document number; new frozen chain | ☐ |

### TC-A09 — บันทึกร่างยังไม่ออกเลข
- trace: BR-09 / LK-6
- Setup: role=source_officer · seed=— · files=—
- Start: `#/create`
- pass: draft label is visible and no TRF number allocated.

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE partial valid data | A | draft screen remains editable | ☐ |
| 2 | CLICK `บันทึกแบบร่าง` | — | toast `บันทึกร่างแล้ว`; label contains `ร่าง — ออกเลขอัตโนมัติเมื่อส่งอนุมัติ` | ☐ |

### Group V — Validation (V-01..V-21)

Each case is independent and starts from the indicated route.

| Case | Setup / Start | Action | Expected | Result |
|---|---|---|---|---|
| TC-V01 | source officer · `#/create` | CLICK next with warehouses blank | labels `เลือกคลังต้นทาง` / `เลือกคลังปลายทาง` remain actionable | ☐ |
| TC-V02 | source officer · `#/create` | TYPE future transfer date or arrival before transfer date | date error appears and next step is blocked | ☐ |
| TC-V03 | source officer · `#/create` | CLICK next without transfer reason | warning `เลือกเหตุผลการย้าย` | ☐ |
| TC-V04 | source officer · `#/create` · seed=warehouse pair without transit | CLICK next after selecting pair | error `คู่คลังนี้ยังไม่มีจุดพักระหว่างทาง — ติดต่อผู้ดูแลผังตำแหน่งให้ตั้งค่าก่อน` | ☐ |
| TC-V05 | source officer · wizard line | TYPE quantity above available | error starts `จำนวนที่ย้ายเกินยอดคงเหลือของ`; submit disabled | ☐ |
| TC-V06 | source officer · wizard line | TYPE 0 then negative quantity | warning `จำนวนที่ย้ายต้องมากกว่า 0 ทุกบรรทัด` | ☐ |
| TC-V07 | source officer · wizard line | SELECT same source/destination bin | warning `bin ต้นทางและปลายทางต้องต่างกัน` | ☐ |
| TC-V08 | source officer · wizard line · seed=quarantine item/bin | SELECT normal destination | warning `ของกักกันย้ายได้เฉพาะไปช่องเก็บกักกันด้วยกัน — ล้าง bin ปลายทางแล้ว` | ☐ |
| TC-V09 | source officer · wizard line · seed=locked bin | CLICK locked bin | warning contains `ถูกล็อก —`; selection unchanged | ☐ |
| TC-V10 | source officer · wizard lines | ADD duplicate source+item+destination | warning begins `มีบรรทัดซ้ำ (bin ต้นทาง + สินค้า + bin ปลายทาง):` | ☐ |
| TC-V11 | source officer · review | CLICK submit with empty approver slot | warning `เลือกผู้อนุมัติให้ครบทุกขั้น` | ☐ |
| TC-V12 | source supervisor · approved transfer · seed=stock reduced after approval | CLICK move/ship | error includes `ยอดคงเหลือที่` and `แก้จำนวนตามยอดล่าสุด หรือตีกลับไปแก้` | ☐ |
| TC-V13 | destination officer · receive | TYPE quantity above remaining and CLICK `ยืนยันรับ` | error `รับเกินจำนวนที่ส่งออกไม่ได้ — ถ้าของงอกจริงต้องใช้ใบปรับยอดสต๊อก` | ☐ |
| TC-V14 | destination officer · receive | TYPE positive receipt, leave actual bin blank, CLICK confirm | warning `ระบุ bin ที่ลงจริงของทุกบรรทัดที่รับ` | ☐ |
| TC-V15 | destination officer · receive discrepancy | leave discrepancy reason blank and CLICK confirm | warning `เลือกเหตุผลของส่วนต่างให้ครบ` | ☐ |
| TC-V16 | destination officer · shortage | CLICK request without file | warning `แนบหลักฐานอย่างน้อย 1 ไฟล์ก่อนขออนุมัติ` | ☐ |
| TC-V17 | shortage requester · approver picker | SELECT shipper as shortage approver | error `ผู้ที่กดส่งออกจากต้นทางเซ็นอนุมัติการตัดส่วนต่างไม่ได้` | ☐ |
| TC-V18 | non-destination actor · in-transit view | CLICK disabled receive wrapper/focus | reason `ยืนยันรับได้เฉพาะเจ้าหน้าที่ของคลังปลายทาง (` is visible | ☐ |
| TC-V19 | destination officer · shipped view | VERIFY cancellation action | cancel absent/disabled; attempting stale action shows `ยกเลิกได้เฉพาะก่อนของขยับ` | ☐ |
| TC-V20 | source supervisor · reversed original | VERIFY reversal action | action absent/disabled; stale action warns `ใบนี้ถูกกลับรายการไปแล้ว — กลับรายการซ้ำไม่ได้` | ☐ |
| TC-V21 | any mutation screen | CLICK primary mutation twice quickly | button disables/loads; second attempt warns `กำลังดำเนินการ กรุณารอสักครู่`; one result only | ☐ |

### Group P — Permission / SoD

| Case | Setup / Start | Action | Expected | Result |
|---|---|---|---|---|
| TC-P01 | role=source_officer · approved transfer · `#/view/:id` | VERIFY header actions | edit/submit per state; ship unavailable without supervisor permission | ☐ |
| TC-P02 | role=shipper · in_transit transfer | CLICK receive/shortage approval affordance | visible reason `ผู้ที่กดส่งออกจากต้นทาง ยืนยันรับเองไม่ได้ (แยกหน้าที่)` or shortage SoD error | ☐ |
| TC-P03 | role=other_warehouse · in_transit transfer | CLICK disabled `ยืนยันรับ` wrapper | destination-only explanation visible; no modal mutation | ☐ |
| TC-P04 | role=accounting_readonly · `#/view/:id` | VERIFY actions | detail/PDF/history visible; mutation buttons absent/disabled | ☐ |
| TC-P05 | role=non_current_approver then current_approver · pending | CLICK `อนุมัติ` | first sees `ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน`; current actor advances step | ☐ |
| TC-P06 | role=source_officer · wizard location picker | SEARCH damaged/receiving/transit locations | excluded locations are not selectable; no create/edit-location action exists | ☐ |

### Group L — List and interaction

| Case | Setup / Start | Action | Expected | Result |
|---|---|---|---|---|
| TC-L01 | seed=all statuses · `#/list` | CLICK each tab/KPI | rows/status counts change; `รอฉันรับ` and `อยู่ระหว่างทาง` are available | ☐ |
| TC-L02 | seed=known creator/reason · `#/list` | TYPE creator in search then SELECT reason filter | matching row shows creator and reason columns | ☐ |
| TC-L03 | `#/list` | TYPE impossible search | filtered empty state appears; reset action visible | ☐ |
| TC-L04 | viewport=1024 · `#/list` | SCROLL table horizontally | rightmost columns/actions become visible; no cell overlap | ☐ |
| TC-L05 | `#/create` | CLICK through five steps; UPLOAD `transfer-note.pdf` | step 3 columns align; step 4 shows uploaded file; step 5 totals/recipient context visible | ☐ |
| TC-L06 | any drawer/modal | PRESS Esc repeatedly | closes combobox → menu → modal → create drawer → view drawer in documented order; dates show Gregorian year | ☐ |

### Group C — Concurrency / atomic (`[AI-DEFAULT]`)

| Case | Setup / Start | Action | Expected | Result |
|---|---|---|---|---|
| TC-C01 | `[AI-DEFAULT]` role=source_supervisor · seed=two approved docs over same stock | CLICK shipment on first then second | first succeeds; second displays latest-balance error; no negative stock | ☐ |
| TC-C02 | `[AI-DEFAULT]` role=destination_officer · seed=in_transit | CLICK receive twice/retry same action | one receipt result; duplicate gets original outcome or duplicate warning | ☐ |
| TC-C03 | `[AI-DEFAULT]` two sessions same draft | TYPE/save session A then save stale B | B shows conflict/reload result; A data remains | ☐ |
| TC-C04 | `[AI-DEFAULT]` inject ledger failure during shipment | CLICK confirm shipment | error visible; status and movement list both remain unchanged from baseline | ☐ |
| TC-C05 | `[AI-DEFAULT]` two sessions completed original | CLICK reversal create simultaneously | one reversal exists; second is blocked as already reversed/in progress | ☐ |

### Group X — Cross-module and locks

| Case | Setup / Start | Action | Expected | Result |
|---|---|---|---|---|
| TC-X01 | `(ต้อง simulate)` DOCCFG available · draft without number | CLICK submit then inspect PDF tab | one `TRF-YYYY-NNNN`; resubmit after reject keeps same code; closed document snapshot opens | ☐ |
| TC-X02 | `(ต้อง simulate)` DOA tiers configured | CLICK submit for low/high value examples | real-person slots differ per central matrix; no role ID shown | ☐ |
| TC-X03 | `(ต้อง simulate)` notification collector | CLICK actions producing nine declared events | each business event appears once; no duplicate `doa_pending/result/escalate` | ☐ |
| TC-X04 | `(ต้อง simulate)` ledger/report read model seeded | CLICK ship/receive then OPEN transit view | report/UI reflects committed transit; retired master still shows snapshot text | ☐ |
| TC-X05 | completed transfer · `#/view/:id` | CLICK reversal flow then VERIFY movements | original rows remain; compensating rows link opposite direction; no adjust/count/location edit appears | ☐ |
| TC-X06 | completed moved/received transfer | VERIFY accounting status/history | visible `รอลงบัญชี`; no real JE reference/post action exists | ☐ |

## Run protocol

1. Reset to each case Setup; never reuse mutated state unless Setup says so.
2. Execute one Action per row and tick Result only after the visible Expected is observed.
3. For `(ต้อง simulate)` cases, mark blocked if the integration injector/collector is unavailable.
4. Capture the exact visible text and route on failure; do not infer backend success from a click.

## Coverage Audit

| Category | Covered / total |
|---|---:|
| Stories/acceptance | 10 / 10 |
| Business rules | 34 / 34 |
| Validation rules | 21 / 21 |
| Confirmed edge cases | 21 / 21 |
| Error codes | 11 / 11 |
| Important permission cells | 6 / 6 |
| Business events | 9 / 9 |
| Lifecycle states | 11 / 11 |
| Cross-module XT | 6 / 6 |
| Scope locks | 11 / 11 |

- Skipped: AI-suggested BRD §10.2 items not confirmed are not release acceptance; conservative concurrency defaults are explicitly tested as `[AI-DEFAULT]`.
- Out of scope and therefore not tested as capabilities: stock adjustment, cycle count, location-master mutation, real JE posting, hard delete.
- **Manifest cross-check (FRD §0.12): ✅ 9/9 manifest rows represented in Ledger.**

## Result Report (schema)

```json
{
  "feature_id": "F-WH-STKTRF",
  "run_at": "<iso datetime>",
  "results": [
    {"id":"TC-A01","status":"pass|fail|blocked","failed_step":null,"evidence":"","note":""}
  ],
  "summary":{"total":53,"pass":0,"fail":0,"blocked":0}
}
```
