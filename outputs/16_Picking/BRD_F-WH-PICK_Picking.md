# BRD: Picking — ใบหยิบสินค้า

| Field | Value |
|---|---|
| BRD ID | BRD-F-WH-PICK |
| Feature | Picking — ใบหยิบสินค้า |
| Type | New Feature |
| Version | 1.0 |
| Status | APPROVED (AI Review) |
| Module / Wave | Warehouse Outbound / S5 |
| Source | PREBRIEF_F-WH-PICK + FUNCTION_CHECKLIST + f-wh-picking.html |
| Updated | 2026-08-18 |

## Changelog

- v1.0 — สร้างจาก prototype ที่ผ่าน UX/Coverage/E2E gate และคำตอบ PM/BA ล่าสุด

## 2. Business Context

### 2.1 ปัญหาและเป้าหมาย

คลังต้องเปลี่ยน Sales Order ที่พร้อมส่งให้เป็นงานหยิบที่ระบุตำแหน่งและล็อตจริง ลดการหยิบผิด ลดการแย่งสต๊อก และส่งผลที่หยิบได้ต่อ Packing ได้อย่างตรวจสอบย้อนหลังได้

### 2.2 เป้าหมายทางธุรกิจ

- รับเฉพาะ SO ที่ผ่านเงื่อนไขจอง พัก และ payment gate เข้าคิว
- ล็อกสต๊อกระดับตำแหน่งด้วย FEFO/FIFO และลำดับตำแหน่งของคลัง
- ให้หัวหน้าคลังมอบหมายงานและให้ผู้หยิบบันทึกครบ/ขาดได้
- ส่งผลต่อ Packing, Inventory และ Sales โดยไม่ทำงานของโมดูลเหล่านั้นแทน

### 2.3 ตัวชี้วัด

| Metric | Baseline | Target | วิธีวัด | รอบวัด |
|---|---|---|---|---|
| ใบหยิบที่ปิดได้โดยไม่มี allocation conflict | เก็บก่อน launch | 100% | audit allocation/release ต่อใบ | รายวัน |
| บรรทัดที่มี trace ตำแหน่ง/ล็อต/ผู้หยิบ | เก็บก่อน launch | 100% | movement + audit ต่อบรรทัด | รายวัน |
| งาน Picking ที่ส่งต่อ Packing ได้สำเร็จ | เก็บก่อน launch | ≥99% ของใบที่สถานะ picked | event/สถานะ to_pack | รายสัปดาห์ |
| เหตุการณ์ขาดที่แจ้ง Sales ได้ | เก็บก่อน launch | 100% | pick.short / pick.short_close | รายสัปดาห์ |

## 3. Scope

### 3.1 In Scope

- คิว SO → สร้างใบหยิบเดี่ยวหรือ wave → จัดสรรตำแหน่ง/ล็อต → มอบหมาย → เริ่มหยิบ → บันทึกครบ/ขาด → ปิดงาน → ส่ง Packing
- การเปลี่ยนตำแหน่ง หาใหม่ เลือกตำแหน่งเอง พัก ยกเลิก และปิดงานแบบขาด
- ใบหยิบ A4 และ audit append-only

### 3.2 Out of Scope

- คิว/trigger จาก Transfer, Replenishment, RTV หรือ Production
- จองระดับคลัง ซึ่งเป็นหน้าที่ Sales Order
- Pack, Delivery Note, การเติม Pick Face จริง, cycle count จริง, RF gun และ zone picking หลายคนต่อใบ
- กติกา DN สำหรับลูกค้ามารับเอง ให้ปรับตอนทำ Delivery Note

### 3.3 Assumptions

- master คลังและ Location เป็นข้อมูลจริง; รหัส SO ใน prototype เป็น mock
- หนึ่งตำแหน่งเก็บสินค้าล็อตเดียวตาม master ที่ยืนยัน
- รายชื่อผู้หยิบแสดงทุกคนก่อน ยังไม่แบ่งตามคลัง/ทีม

### 3.4 Scope Lock

| LOCK | ข้อยืนยัน |
|---|---|
| LOCK-01 | Feature อยู่ใน Wave S5 |
| LOCK-02 | จุดเริ่มของงานผู้ใช้คือ “สร้างใบหยิบ” |
| LOCK-03 | Warehouse/Location ยึด master คลัง; prototype เป็น mock |
| LOCK-04 | หนึ่งตำแหน่งเก็บสินค้าล็อตเดียว |
| LOCK-05 | Allocation ใช้มาตรฐาน ERP และ PREBRIEF |
| LOCK-06 | Exception ใช้มาตรฐาน ERP ตามที่ PREBRIEF ระบุ |
| LOCK-07 | Permission ยึดของ Picking |
| LOCK-08 | ผู้หยิบเห็นทุกคนก่อน ยังไม่แยก |
| LOCK-09 | Picker ทำ flow ที่มอบหมายได้เอง |
| LOCK-10 | Pickup ยัง Pack → DN ปกติ; ปรับเฉพาะตอนทำ DN |
| LOCK-11 | Pick รับคิวจาก SO เท่านั้น; source อื่นไม่ trigger เข้ามา |
| LOCK-12 | UI ไม่มีปุ่มไอคอนดาวน์โหลดสำหรับขอเติม/โอนใน action รายบรรทัด |

## 4. Roles & Permissions

| Action | wh_lead | picker | viewer |
|---|:---:|:---:|:---:|
| ดูคิว/ใบหยิบ | ✓ ทุกใบ | ✓ งานตนเอง | ✓ |
| สร้าง/ยกเลิก/มอบหมาย | ✓ | — | — |
| เริ่ม/บันทึก/พัก/หยิบต่อ | ✓ | ✓ ใบตนเอง | — |
| เปลี่ยนตำแหน่ง/ปิดขาด | ✓ | ✓ ใบตนเอง | — |
| ส่ง Packing | ✓ | ✓ ใบตนเองเมื่อพร้อม | — |

## 5. User Journey + COSO

| # | Step | Maker | Checker | Approver | System |
|---|---|---|---|---|---|
| 1 | SO ผ่าน gate เข้าคิว | Sales/Finance upstream | — | — | derive queue |
| 2 | เลือก SO และสร้างใบหยิบ | wh_lead | allocation rules | — | allocate location/lot |
| 3 | มอบหมายผู้หยิบ | wh_lead | workload warning | — | emit pick.assigned |
| 4 | เริ่มและบันทึกหยิบ | picker/wh_lead | scan + quantity validation | — | movement pick |
| 5 | จัดการของขาด/เปลี่ยนตำแหน่ง | picker/wh_lead | eligibility rules | — | release/reallocate/backorder |
| 6 | ปิดครบหรือปิดขาด | picker/wh_lead | all-line readiness | — | emit done/short_close |
| 7 | ส่งต่อ Packing | picker/wh_lead | downstream contract | — | create PACK ref |

ไม่มี approval chain ใน Picking; Checker เป็นกฎระบบและ audit ไม่ใช่ผู้อนุมัติ จึงไม่เกิด SoD approval conflict

## 6. Data Entity & Fields

### 6.1 Entities

| Entity | Purpose |
|---|---|
| pick_header | หัวใบหยิบ/แหล่ง SO/คลัง/ผู้หยิบ/สถานะ |
| pick_line | สินค้า ตำแหน่ง ล็อต จำนวนจัดสรร/หยิบ/ขาด |
| pick_audit | เหตุการณ์ append-only |
| inventory_movement | allocation/pick/release อ้าง Pick + SO |

### 6.2 Header fields

| Field | UI | Type | Required | Note |
|---|---|---|:---:|---|
| pick_no | รหัสใบหยิบ | AUTO | ✓ | PICK-YYYY-NNNN |
| warehouse_id | คลัง | LOOKUP | ✓ | Warehouse master snapshot |
| source_type | ประเภทต้นทาง | AUTO | ✓ | SO เท่านั้นใน scope |
| source_refs | อ้างอิง SO | LOOKUP-MULTI | ✓ | คลังเดียวกัน ไม่เกิน waveMax |
| assignee_id | ผู้หยิบ | LOOKUP | — | ว่าง = draft |
| equipment | อุปกรณ์ | DROPDOWN | — | master/mock |
| priority | ความสำคัญ | DROPDOWN | ✓ | high/normal/low |
| status | สถานะ | AUTO | ✓ | lifecycle §8 |
| version | เวอร์ชัน | AUTO | ✓ | optimistic lock |
| created_by/at, modified_by/at | audit | AUTO | ✓ | append audit คู่กัน |

### 6.3 Line fields

| Field | UI | Required | Note |
|---|---|:---:|---|
| source_line_id / item_id | SO line / สินค้า | ✓ | soft reference + snapshot name/uom |
| location_id / balance_id | ตำแหน่ง | ตาม allocation | hard eligible location |
| lot_no / expiry_date | ล็อต/หมดอายุ | ตาม item | FEFO |
| required_qty / allocated_qty / picked_qty / short_qty | จำนวน | ✓ | base UOM |
| rule | กติกา | ✓ | FEFO/FIFO |
| line_status / reason | สถานะ/เหตุผล | ✓ | pending/partial/picked/short |

`pick_header 1:N pick_line`; `pick_header 1:N pick_audit`; pick line soft-ref SO line, item, location, balance และ movement

## 7. User Stories

| Story | Actor | Intent | Acceptance summary |
|---|---|---|---|
| US-01 | wh_lead | สร้างใบหยิบจาก SO พร้อมหยิบ | เลือกคลังเดียวกัน; allocation ถูก; บันทึกได้ |
| US-02 | wh_lead | มอบหมายงาน | ค้นผู้หยิบ; workload แสดง; assigned event ถูกยิง |
| US-03 | picker | บันทึกหยิบ | scan ครบ; จำนวนไม่เกินคงเหลือ; movement ถูกสร้าง |
| US-04 | picker | จัดการของขาด | ระบุเหตุผล; release/backorder; แจ้งผู้เกี่ยวข้อง |
| US-05 | wh_lead | ส่งผลต่อ Packing | ทำได้เมื่อพร้อม; แยก PACK ต่อ SO |
| US-06 | viewer | ตรวจสอบย้อนหลัง | เห็นข้อมูลและ audit แต่ไม่มีปุ่ม mutation |

## 8. Status & Lifecycle

`draft → assigned → in_progress ⇄ on_hold → picked → to_pack`; `draft|assigned → cancelled`

| Current | Trigger | Next | Guard |
|---|---|---|---|
| — | save without assignee | draft | allocation persisted |
| —/draft | assign | assigned | wh_lead + assignee |
| assigned | start | in_progress | assignee/lead |
| in_progress | hold/resume | on_hold/in_progress | reason on hold |
| in_progress | finish/close-short | picked | all lines terminal + picked > 0 |
| picked | send Packing | to_pack | downstream contract succeeds |
| draft/assigned | cancel | cancelled | reason; release allocation |

## 9. Business Rules & Validation

| Rule | Summary | Tag | Flex level |
|---|---|---|---|
| BR-01 | Queue gate = confirmed + reserved + !hold + payment passed | FIXED | function |
| BR-02 | remaining = reserved − picked − open-pick; service/backorder excluded | FIXED | function |
| BR-03 | wave same warehouse and ≤ waveMax | CONFIGURABLE | Admin Panel |
| BR-04 | running number through Document Config contract | FIXED | shared service |
| BR-05 | item lot → FEFO else FIFO; Pick Face→Reserve→Bulk; route order | DYNAMIC | Engine Management [AI-DEFAULT] |
| BR-06 | SO reserve warehouse; Pick allocate location; pick/release updates balance atomically | FIXED | engine/function |
| BR-07 | auto/manual location must pass hard eligibility | FIXED | function |
| BR-08 | workload threshold warns only; does not block | CONFIGURABLE | Admin Panel |
| BR-09 | scan location + item/lot before confirm; short requires reason/action | FIXED | validation |
| BR-10 | short releases allocation, moves SO qty to backorder, emits notification | FIXED | transaction |
| BR-11 | refresh uses latest balances and hard-allocates when found | FIXED | engine |
| BR-12 | replenishment/transfer belongs to Inventory; no inbound Pick trigger | FIXED | cross-module |
| BR-13 | picked requires terminal lines and picked qty > 0; Packing split per SO | FIXED | transition |
| BR-14 | close-short requires in_progress, prior picked qty, reason | FIXED | transition |
| BR-15 | hold keeps allocation; cancel only before start and releases allocation | FIXED | transition |
| BR-16 | audit append-only; movement refs Pick + SO | FIXED | control |

### 9.2 Validation messages

| ID | Condition | Type | Visible expectation |
|---|---|---|---|
| VR-01 | mixed warehouse / wave > max | prevent | แจ้งให้เลือก SO คลังเดียวกัน/จำนวนไม่เกินกำหนด |
| VR-02 | no assignee on assign | prevent | “เลือกผู้หยิบ” |
| VR-03 | scan incomplete | disabled | ปุ่มยืนยันยังใช้ไม่ได้ |
| VR-04 | short without reason | prevent | ต้องเลือก/ระบุเหตุผล |
| VR-05 | cancel/hold/close-short without reason | prevent | “กรุณาระบุเหตุผล” |

### 9.5 Flexibility summary

| Rule | Source | Owner | Frequency | Level |
|---|---|---|---|---|
| BR-03 waveMax | 🤖 inferred | Warehouse admin | เป็นระยะ | Admin Panel |
| BR-05 strategy/ranking | 🤖 inferred | Warehouse owner | นาน ๆ ครั้ง | Engine Management |
| BR-08 workload threshold | 🤖 inferred | Warehouse admin | เป็นระยะ | Admin Panel |

## 10. Edge Cases

### Confirmed

- EC-01 payment gate/hold prevents selection; finance release re-evaluates queue
- EC-02 open pick subtracts remaining and prevents duplicate allocation
- EC-03 allocation has no eligible location but document can be created as short
- EC-04 partial pick can short or relocate remaining qty
- EC-05 cancel releases all unpicked allocation; started pick cannot cancel
- EC-06 picker/viewer permission removes unauthorized actions
- EC-07 A4 wraps long text and embeds Thai font

### Conservative engineering defaults

- [AI-DEFAULT] EC-08 concurrent mutation uses `version`; stale write returns conflict and reload prompt
- [AI-DEFAULT] EC-09 mutation retry uses idempotency key to prevent double allocation/movement/event
- [AI-DEFAULT] EC-10 master record inactive after draft blocks new allocation but preserves snapshot for history
- [AI-DEFAULT] EC-11 downstream Packing failure keeps status `picked` and allows safe retry
- [AI-DEFAULT] EC-12 notification failure does not roll back business transaction; ENG-NOTIFY queues/retries

## 11. Impact / Regression

New feature; regression checks apply to SO reserved/picked/backorder, Inventory balances/movements, employee visibility, Packing intake and notification catalog. No direct mutation of another feature’s storage is allowed.

## 12. System Context & Value Stream

`Sales Order → Picking → Packing → Delivery Note`

| Direction/Module | Data/trigger | If changed/cancelled |
|---|---|---|
| SO → Pick | confirmed/reserved/payment/hold/lines | queue re-derived; open allocation prevents duplicate |
| Item/Location/Inventory → Pick | item strategy, eligible balances, lot/expiry | revalidate before allocate/relocate |
| Employee/IAM → Pick | role, visibility, assignee | unauthorized action blocked |
| Pick → Inventory | allocation/pick/release movement | idempotent reversal/release |
| Pick → Sales | picked/backorder + short event | Sales follows its own policy |
| Pick → Packing | picked quantities split per SO | retry without duplicate PACK |
| Pick → ENG-NOTIFY | assigned/short/done/short_close | notification failure queued |

### 12.3 Existing systems

| Need | Reference |
|---|---|
| SO gate/reserve | Related context/Sales Order |
| balance/lot/movement | Related context/1. Inventory |
| warehouse/location | Related context/6. Warehouse |
| item/UOM | Related context/Item-master |
| user/role/workload | organization-management + employee-management |
| Packing/DN contract | ยังไม่มี locked artifact; ใช้ OQ-05 |

## 13. Delivery Phases

- Phase 1: transaction, allocation engine/function, state machine, permissions, audit, integrations, A4, notification wiring
- Phase 2: admin settings for waveMax/workload threshold if BA confirms ownership
- Phase 3: rule management for strategy/ranking only after OQ confirmation
- Phase 4: no engine-management UI in this delivery; register reusable engine contract only

## 14. Dev Requirements Summary

- Atomic allocation/pick/release with optimistic lock and idempotency
- No source type beyond SO in queue/API mutation
- Allocation uses Item + Location + Balance master and never auto-selects HOLD/STAGING/PACK
- All mutation APIs trace to logic functions/engine and audit event
- Do not hardcode notification channels/preferences or Packing/DN logic
- Keep mock-only Finance release, inbound and “pick all” clearly separated from production API

### 14.6 Screen inventory extracted from HTML

| Page | Route | Type | Purpose |
|---|---|---|---|
| P-01 | `#/list` | list + tabs | SO queue and pick list |
| P-02 | `#/create/:soId` | 3-step drawer | select SO, assign, review allocation |
| P-03 | `#/view/:pickId` | tabbed document drawer | lines, details/SO, printable pick, history |

UI signals: transaction document, printable A4, no approval chain, shell/list/drawer/modal/popover patterns observed in HTML

## 15. Open Questions

| OQ | Question | Status/owner |
|---|---|---|
| OQ-01 | waveMax และ workload warning มาจาก setting ใด/ใครแก้ | รอ BA + Warehouse owner |
| OQ-02 | picker ปิดขาด/override location ได้ถาวรหรือให้ wh_lead เท่านั้น | รอ BA/IAM |
| OQ-03 | กลยุทธ์/ranking ต้อง register `pick-allocation-engine` และให้ใครเปลี่ยน | รอ Architect + BA |
| OQ-04 | manual override ต้องบังคับเหตุผลทุกครั้งหรือไม่ | รอ Warehouse owner |
| OQ-05 | Packing intake contract และวิธีป้องกัน PACK ซ้ำ | รอ Packing/DN feature |
| OQ-06 | event catalog ของ F-NOTIFY มี event ใดอยู่แล้ว | ตรวจตอน NTF declaration |

## 16. Security & Compliance

Preset: P1 Standard Transaction. Highest data classification: **Confidential** (employee assignment/workload and operational transaction); no Restricted field identified.

| Control | Requirement |
|---|---|
| AC-01 | IAM authorization per action and own-assignment scope |
| AU-01 | append-only audit for state/allocation/override |
| IN-01 | validate quantity, location eligibility, source scope |
| TX-01 | atomic transaction + optimistic lock + idempotency |
| DP-01 | minimum employee data; no sensitive HR detail in Pick |
| IR-01 | log and correlate failures by pick/source ref |

Risks: unauthorized pick (AC-01/AU-01), double allocation (TX-01/IN-01), lost traceability (AU-01/IR-01), employee data overexposure (DP-01).

## 17. Health Check

| KPI/Control | Target / threshold | Action |
|---|---|---|
| allocation conflict rate | 0%; any conflict | alert + rollback/retry safely |
| movement without Pick+SO ref | 0 | block commit + audit error |
| Packing handoff success | ≥99%; retry failures | keep picked + retry idempotently |
| notification emit accepted | ≥99%; failures queued | ENG-NOTIFY retry |
| queue evaluation latency | baseline before launch; p95 target agreed in OQ | monitor slow query |

Throughput baseline must be measured before launch; stress test at 2× measured peak wave volume.

## 18. Monitoring

- Performance: queue evaluation, allocation duration, Packing handoff latency
- Closing: created/assigned/picked/to_pack/cancelled counts by warehouse
- Anomaly: negative balance attempt, stale version, duplicate idempotency key, unauthorized action
- Transaction: full Pick audit and Inventory movement refs
- Dashboard: open queue, work in progress, short rate, allocation conflict, handoff failure

## AI Review Report

- C01–C23: PASS; metrics, scope lock, value stream, tags and screen inventory present
- PE01–PE05: PASS; COSO/system checks, controls, KPI/threshold and monitoring linked
- Warnings: OQ-01..06 are explicit and do not authorize scope expansion
- Verdict: **APPROVED — ready for FRD**
