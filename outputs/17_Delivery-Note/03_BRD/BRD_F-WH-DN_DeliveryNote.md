# BRD: Delivery Note — ใบส่งของ

| Field | Value |
|---|---|
| BRD ID | BRD-F-WH-DN |
| Feature | Delivery Note — ใบส่งของ |
| Type | New Feature |
| Version | 1.0 |
| Status | APPROVED (AI Review) |
| Module / Wave | Warehouse Outbound / S5 |
| Source | PREBRIEF_F-WH-DN + FUNCTION_CHECKLIST + f-wh-delivery-note.html + มติ PM/BA |
| Updated | 2026-08-20 |

## 1. Changelog

- v1.0 — สร้างจาก prototype ที่ผ่าน UX, Coverage และ E2E gate พร้อมรวมมติเรื่อง Stock Transfer, Manual DN และ search dropdown สำหรับผู้รับผิดชอบ/คนขนส่ง/รถ

## 2. Business Context

### 2.1 ปัญหาและเป้าหมาย

คลังต้องเปลี่ยนใบแพ็คที่พร้อมส่งให้เป็นใบส่งของที่ติดตามได้ตั้งแต่ร่างจนถึงผลส่งจริง เชื่อมการตัดสต๊อก การคืนสต๊อก สถานะเอกสารต้นทาง และหลักฐานการส่ง โดยไม่ให้ผู้ใช้รวมงานผิดลูกค้าหรือผิดปลายทาง

### 2.2 เป้าหมายทางธุรกิจ

- รวมใบแพ็คหลายใบเป็น DN เดียวได้เมื่อประเภทต้นทาง ลูกค้า และที่ส่งตรงกัน
- รองรับ Sales Order และ Stock Transfer ใน flow อ้างอิงจริงของรอบนี้
- รองรับ Manual DN แยกจาก flow อ้างอิง และเปลี่ยนสถานะด้วยคนได้ทุกสถานะโดยมีเหตุผล
- ตัดสต๊อกเมื่อออกรถ และกลับรายการอย่างถูกต้องเมื่อตีกลับหรือยกเลิกหลังออกรถ
- เก็บผลส่งรายสินค้า ประวัติการพยายามส่ง และเอกสาร A4 ที่ตรวจย้อนหลังได้

### 2.3 ตัวชี้วัด

| Metric | Baseline | Target | วิธีวัด | รอบวัด |
|---|---|---|---|---|
| DN อ้างอิงที่สร้างโดยไม่รวมข้าม customer/ship-to/source | เก็บก่อน launch | 100% | validation + audit ต่อการสร้าง | รายวัน |
| Goods Issue / Reverse GI ที่มี DN และ source ref ครบ | เก็บก่อน launch | 100% | inventory movement reconciliation | รายวัน |
| DN ที่บันทึก POD/เหตุผลล้มเหลวครบ | เก็บก่อน launch | 100% | delivery audit completeness | รายสัปดาห์ |
| การ sync SO/Transfer ถูกประเภทต้นทาง | เก็บก่อน launch | 100% | cross-module event reconciliation | รายวัน |
| notification event ที่ ENG-NOTIFY รับสำเร็จ | เก็บก่อน launch | ≥99% | outbox/emit monitor | รายวัน |

## 3. Scope

### 3.1 In Scope

- คิวใบแพ็คที่แพ็คเสร็จและยังไม่มี DN
- สร้าง DN จากใบแพ็คเดียวหรือหลายใบของ source type + ลูกค้า + ปลายทางเดียวกัน
- Sales Order และ Stock Transfer (`WH-01 → WH-02`) ใน reference flow
- ผู้รับผิดชอบเป็นพนักงานบริษัทแบบ search dropdown เท่านั้น
- คนขนส่งและรถเป็น search dropdown พร้อมตัวเลือกกรอกเอง; คนขนส่งกรอกชื่อ นามสกุล เบอร์โทร และรถกรอกเลขทะเบียน
- Draft → Ready → In transit → Delivered/Partial/Failed/Returned/Cancelled พร้อม tracking, attempts และ POD
- Manual DN แยกจาก Reference DN; Manual DN อัปเดตทุกสถานะด้วยเหตุผล และไม่มี GI/source sync อัตโนมัติ
- เอกสารใบส่งของ A4 และ audit append-only

### 3.2 Out of Scope

- route optimization, แบ่ง DN เป็นหลายรถ, mobile e-POD/GPS จริง
- API 3PL จริง, คำนวณค่าขนส่งอัตโนมัติ, Credit Note อัตโนมัติ
- การสร้าง/แก้ Employee, Fleet หรือ Driver master จาก feature นี้
- Approval chain/DOA
- การ persist mock state หลัง refresh ใน prototype

### 3.3 Assumptions

- Production ใช้ master และ API จริง; prototype เก็บข้อมูลใน memory และ refresh แล้วกลับชุดข้อมูลตั้งต้น
- DN แบบอ้างอิงเก็บ snapshot ชื่อ/ที่อยู่/ผู้ติดต่อจากเอกสารต้นทาง จึงไม่ให้แก้ลูกค้าโดยตรงใน prototype
- Manual transport entry ใน prototypeเป็นค่าชั่วคราว; owner ของ master production ยังเป็น Open Question

### 3.4 Scope Lock

| LOCK | ข้อยืนยัน |
|---|---|
| LOCK-01 | งานทั้งหมดเขียนใต้ `outputs/17_Delivery-Note`; ห้ามแก้ source pack |
| LOCK-02 | UI final ยึด seed HTML เดิมและแก้เท่าที่จำเป็น |
| LOCK-03 | รวมหลายใบแพ็คได้เมื่อ source type, customer และ ship-to เดียวกัน |
| LOCK-04 | Stock Transfer อยู่ใน scope จริงและไม่ sync Sales Order |
| LOCK-05 | Manual create แยกจาก Reference create |
| LOCK-06 | Manual DN เปลี่ยนทุกสถานะด้วยคนได้ แต่ทุกครั้งต้องมีเหตุผล |
| LOCK-07 | Manual DN ห้ามทำ Goods Issue หรือ sync เอกสารต้นทางอัตโนมัติ |
| LOCK-08 | ผู้รับผิดชอบต้องเป็นพนักงานบริษัทและไม่มี manual option |
| LOCK-09 | คนขนส่ง manual ต้องมีชื่อ นามสกุล เบอร์โทร; รถ manual ต้องมีเลขทะเบียน |
| LOCK-10 | ออกรถของ Reference DN เป็นจุด Goods Issue |
| LOCK-11 | ตีกลับ/ยกเลิกหลัง GI ต้อง reverse GI ก่อนคืนใบแพ็คเข้าคิว |
| LOCK-12 | failed attempt เริ่มนับที่ 1 |

## 4. Roles & Permissions

| Action | `wh_lead` | `picker/driver` | `viewer/sales` |
|---|:---:|:---:|:---:|
| ดูคิว/ใบส่งของ | ✓ | ✓ งานที่เกี่ยวข้อง | ✓ |
| สร้าง Reference/Manual DN | ✓ | — | — |
| แก้ข้อมูล/ยืนยันพร้อมส่ง/ยกเลิก/ตีกลับ | ✓ | — | — |
| ออกรถ/Tracking/Failed/POD | ✓ | ✓ ใบที่รับผิดชอบ | — |
| อัปเดตสถานะ Manual | ✓ | ตาม policy ที่ยืนยันภายหลัง | — |
| พิมพ์/ดูประวัติ | ✓ | ✓ | ✓ |

## 5. User Journey + COSO

| # | Step | Maker | Checker | Approver | System |
|---|---|---|---|---|---|
| 1 | ใบแพ็คพร้อมส่งเข้าคิว | Packing | queue rule | — | derive queue |
| 2 | เลือกใบแพ็คและยืนยันสร้าง DN | wh_lead | source/customer/ship-to guard | — | bind packs; create draft |
| 3 | กำหนดผู้รับผิดชอบ/ขนส่ง/รถ/วันส่ง | wh_lead | required/capacity/deadline | — | validate master/snapshot |
| 4 | ยืนยันพร้อมส่ง | wh_lead | completeness rule | — | lock read-only view |
| 5 | ออกรถ | driver/wh_lead | tracking + state guard | — | Goods Issue + notify |
| 6 | Tracking/Failed/POD | driver/wh_lead | sequence/quantity/reason | — | append audit + notify |
| 7 | Delivered/Partial/Returned/Cancelled | wh_lead/system | reverse/return/source sync | — | downstream events |
| 8 | สร้าง/เปลี่ยนสถานะ Manual DN | wh_lead | required reason | — | audit only; no automatic integration |

ไม่มี approval chain ใน Delivery Note; Checker เป็นกฎระบบและ transactional controls จึงไม่เกิด Maker/Approver conflict

## 6. Data Entity & Fields

### 6.1 Entities

| Entity | Purpose |
|---|---|
| `delivery_note` | หัว DN, source mode, ผู้รับ, ขนส่ง, lifecycle, GI/POD refs |
| `delivery_note_pack` | DN 1:N Packing reference |
| `delivery_note_line` | สินค้า/ล็อต/กล่อง/จำนวนส่ง-รับ-ปฏิเสธ |
| `delivery_attempt` | ครั้งส่งไม่สำเร็จ เริ่ม 1 |
| `delivery_tracking` | timeline ขนส่งตามลำดับ |
| `delivery_audit` | เหตุการณ์ append-only |
| `delivery_manual_transition` | จาก/ไป/เหตุผล/ผู้เปลี่ยน สำหรับ Manual DN |

### 6.2 Header fields

| Field | UI | Type | Required | Note |
|---|---|---|:---:|---|
| `dn_no` | เลขที่ใบส่งของ | AUTO | ✓ | จาก ENG-DOC-NUM เมื่อ confirm/issue ตาม declaration |
| `creation_mode` | แบบการสร้าง | AUTO | ✓ | `reference` / `manual` |
| `source_type` / `source_refs` | ต้นทาง | AUTO/LOOKUP | reference | `sales_order` / `stock_transfer` / `manual` |
| `warehouse_from_id` / `warehouse_to_id` | คลังต้นทาง/ปลายทาง | LOOKUP | transfer | แสดง `WH-01 → WH-02` |
| `customer_snapshot` / `ship_to_snapshot` | ผู้รับ/ที่ส่ง | SNAPSHOT | ✓ | Reference อ่านอย่างเดียว |
| `assignee_employee_id` | ผู้รับผิดชอบ | SEARCH LOOKUP | reference | Employee company only |
| `carrier_type` / `carrier_id` | ผู้ขนส่ง | SEARCH LOOKUP | reference | own/3PL/pickup/manual |
| `driver_id` / `driver_snapshot` | คนขนส่ง | SEARCH/MANUAL | own/manual | manual: first/last/phone |
| `vehicle_id` / `vehicle_plate_snapshot` | รถ | SEARCH/MANUAL | own/manual | manual: plate |
| `ship_date` / `slot` | วัน/รอบส่ง | DATE/DROPDOWN | reference | deadline warning |
| `status` / `version` | สถานะ/เวอร์ชัน | AUTO | ✓ | concurrency guard |
| `gi_ref` / `gi_at` | Goods Issue | AUTO | reference after dispatch | null after reversal |
| `created_by/at`, `modified_by/at` | audit | AUTO | ✓ | tenant/company context |

`delivery_note 1:N delivery_note_pack/line/attempt/tracking/audit/manual_transition`; source documents and masters use soft reference plus snapshots.

## 7. User Stories

| Story | Actor | Intent | Acceptance summary |
|---|---|---|---|
| US-01 | wh_lead | สร้าง DN จาก Packing | queue guard ถูก; รวมได้เฉพาะ key เดียวกัน; ยังไม่ GI |
| US-02 | wh_lead | เตรียมข้อมูลจัดส่ง | employee-only assignee; searchable transport; manual transport validation |
| US-03 | driver | ออกรถ | state guard ผ่าน; Reference เกิด GI; Manual ไม่เกิด GI |
| US-04 | driver | ติดตามและบันทึกผลส่ง | attempt เริ่ม 1; tracking ไม่ย้อน; POD ตรวจจำนวน/เหตุผล |
| US-05 | wh_lead | จัดการ partial/failed/return/cancel | return/reverse และ queue/source sync ถูกประเภท |
| US-06 | wh_lead | ส่ง Stock Transfer | เห็นคลังต้นทาง→ปลายทาง; ไม่แตะ SO |
| US-07 | wh_lead | สร้าง Manual DN | flow แยก; เปลี่ยนทุกสถานะด้วยเหตุผล; audit ครบ; no auto integration |
| US-08 | viewer | ตรวจสอบ/พิมพ์ | tabs/read-only/history/A4 ตรงข้อมูล |

## 8. Status & Lifecycle

Reference: `draft → ready → in_transit → delivered|partial|failed`; `failed → ready|returned`; `draft|ready|in_transit|failed → cancelled`; POD ปฏิเสธทั้งหมดไป `returned`.

Manual: สร้างเป็น `draft` แล้วผู้มีสิทธิ์เลือกสถานะปลายทางใดในชุด `draft, ready, in_transit, failed, delivered, partial, returned, cancelled` ได้ โดยบังคับเหตุผลและไม่เรียก automation ของ Reference DN.

| Current | Trigger | Next | Guard / side effect |
|---|---|---|---|
| — | confirm reference | draft | bind packs; no GI |
| draft | mark ready | ready | required delivery fields |
| ready | dispatch | in_transit | Reference GI; 3PL requires tracking |
| in_transit | tracking | in_transit | forward-only |
| in_transit | failed | failed | attempt = previous +1; no stock return |
| failed | reschedule | ready | attempt history preserved |
| in_transit | POD | delivered/partial/returned | return rejected qty; source sync by type |
| failed | return all | returned | reverse GI; packs back queue |
| pre/post dispatch | cancel | cancelled | reverse GI only if exists; packs back queue |
| any manual state | manual update | selected state | reason mandatory; audit only |

## 9. Business Rules & Validation

| Rule | Summary | Tag | Flex level |
|---|---|---|---|
| BR-01 | Queue = packed + no DN ref | FIXED | function |
| BR-02 | Combine key = source_type + customer + ship_to | FIXED | function |
| BR-03 | Confirm creates draft and does not issue stock | FIXED | transaction |
| BR-04 | Ready requires contact/address/assignee/date/carrier plus own transport fields | FIXED | validation |
| BR-05 | Vehicle over capacity warns but does not block | CONFIGURABLE | Admin Panel |
| BR-06 | 3PL dispatch requires tracking number | FIXED | validation |
| BR-07 | Tracking progresses forward; delivered comes from POD | FIXED | state rule |
| BR-08 | Reference dispatch performs atomic Goods Issue | FIXED | shared engine |
| BR-09 | POD requires receiver; rejected qty requires reason; max 4 photos | CONFIGURABLE | Admin Panel |
| BR-10 | POD result derives from rejected total | FIXED | function |
| BR-11 | Accepted/rejected updates stock and source accumulators by source type | FIXED | transaction |
| BR-12 | Failed attempt starts at 1; maximum attempts is configurable | CONFIGURABLE | Admin Panel |
| BR-13 | Return/cancel after GI reverses GI before queue/source restoration | FIXED | transaction |
| BR-14 | Sales Order sync only when source_type=sales_order | FIXED | cross-module |
| BR-15 | Stock Transfer shows from→to and never updates SO | FIXED | cross-module |
| BR-16 | Non-draft reference view is read-only except explicit edit in ready | FIXED | UI/state |
| BR-17 | Audit append-only for every mutation | FIXED | control |
| BR-18 | Manual DN is isolated from reference automation | FIXED | scope lock |
| BR-19 | Manual transition requires reason for every change | FIXED | validation |
| BR-20 | Assignee is Employee only; manual option exists only for driver/vehicle | FIXED | permission/master |
| BR-21 | Number/snapshot policy comes from F-DOCCFG engines only | FIXED | shared service |
| BR-22 | Notification channels/preferences come from ENG-NOTIFY only | FIXED | shared service |

### 9.5 Flexibility summary

| Rule | Source | Owner | Frequency | Level |
|---|---|---|---|---|
| BR-05 capacity warning | 🤖 inferred | Warehouse admin | เป็นระยะ | Admin Panel |
| BR-09 max photos | 🤖 inferred | Warehouse admin | นาน ๆ ครั้ง | Admin Panel |
| BR-12 max attempts | 🤖 inferred from PREBRIEF | Warehouse admin | เป็นระยะ | Admin Panel |

## 10. Edge Cases

### Confirmed

- EC-01 เลือก Packing คนละ source/customer/ship-to ต้องถูกล็อกและบล็อก confirm
- EC-02 refresh prototype ปิด drawer และกลับ `#/list`; mock state reset เป็นข้อจำกัด prototype
- EC-03 failed ครั้งแรกต้องแสดงครั้งที่ 1
- EC-04 Return all บังคับเหตุผล คืนสต๊อก และคืน Packing เข้าคิว
- EC-05 Cancel ก่อน dispatch ไม่มี reverse; หลัง dispatch reverse ก่อนคืนคิว
- EC-06 Transfer fixture `PACK-2026-0460 / TR-2026-0012` แสดง `WH-01 → WH-02` และไม่มี SO sync
- EC-07 Manual transition เหตุผลว่างต้องถูกบล็อก; history ต้องเพิ่มทุกครั้ง
- EC-08 Manual assignee ไม่มี free text; manual driver/vehicle validation ครบ
- EC-09 long Thai/หลาย line ต้องพิมพ์ A4 ได้โดยไม่ตัดข้อมูลสำคัญ

### Conservative engineering defaults

- `[AI-DEFAULT]` EC-10 optimistic lock; stale mutation returns conflict and reload prompt
- `[AI-DEFAULT]` EC-11 every mutation requires idempotency key to avoid duplicate GI/reversal/event
- `[AI-DEFAULT]` EC-12 master revalidation occurs at confirm/dispatch while stored snapshot remains historical
- `[AI-DEFAULT]` EC-13 downstream/notification failure uses transactional outbox and safe retry
- `[AI-DEFAULT]` EC-14 GI/reverse uses all-or-nothing transaction; partial commit is forbidden

## 11. Impact / Regression

Regression covers Packing queue/ref, Inventory movements/balance, SO shipped/returned/status, Stock Transfer visibility, Employee/IAM, print, Document Configuration and Notification Center. Feature must call contracts and must not write another module’s storage directly.

## 12. System Context & Value Stream

`Sales Order / Stock Transfer → Picking → Packing → Delivery Note → Inventory + Sales/Transfer + AR`

| Direction/Module | Data/trigger | If changed/cancelled |
|---|---|---|
| Packing → DN | packed boxes/lines/source/customer/ship-to | remove from queue only after DN creation; restore on return/cancel |
| Employee/Fleet/Carrier → DN | assignee/driver/vehicle/carrier | revalidate active selection; retain snapshot |
| DN → Inventory | GI, reverse GI, return_in | atomic/idempotent; reconcile by DN ref |
| DN → Sales Order | issued/shipped/returned/status | only SO source; reverse/partial recalculates |
| DN → Stock Transfer | dispatch/delivery status | transfer source only; no SO mutation |
| DN → AR | delivered/partial actual quantity | retry without duplicate billing request |
| DN → ENG-NOTIFY | ready/dispatch/tracking/failed/delivered/returned | outbox retry; no business rollback |
| DN → Document Store | printable external snapshot | policy determined centrally |

### 12.3 Existing systems

| Need | Reference |
|---|---|
| Packing intake | F-WH-PACK locked output |
| Sales source/status | Sales Order context |
| Transfer source/status | Stock Transfer context; exact contract is OQ-04 |
| Balance/movement | Inventory context |
| Employee/IAM | Employee + User Role Access |
| Number/snapshot | F-DOCCFG / ENG-DOC-NUM / ENG-DOC-STORE |
| Notification | F-NOTIFY / ENG-NOTIFY |

## 13. Delivery Phases

- Phase 1: reference SO/Transfer, manual mode, state machine, GI/reversal/POD, audit, A4, permissions and shared-service wiring
- Phase 2: admin settings for capacity warning, max photos and max attempts after owner confirmation
- Phase 3: real 3PL/tracking integration and transport master governance after OQs are resolved
- Phase 4: route optimization/mobile e-POD are explicitly outside this delivery

## 14. Dev Requirements Summary

- Keep Reference and Manual mutation paths separate at API and logic layers
- Use atomic transaction, optimistic lock, idempotency and append-only audit
- Call Inventory/Sales/Transfer/AR through contracts; never direct-write foreign tables
- Use Employee-only lookup for assignee; driver/vehicle may accept validated manual snapshot
- Issue document number and snapshot only through document engines; notify only through ENG-NOTIFY
- Preserve current HTML text, routes, tab structure, drawer/modal behavior and source-specific display

### 14.6 Screen inventory extracted from HTML

| Page | Route | Type | Purpose |
|---|---|---|---|
| P-01 | `#/list` | list + 2 tabs | Packing queue and DN list; Reference/Manual create entry |
| P-02 | `#/create/:packIds` | confirmation modal over list | summarize selected packs and capture assignment/transport before Reference create |
| P-03 | `#/view/:dnId` | tabbed transaction drawer | delivery data, lines/boxes, printable document and history |

Other overlays are part of P-01/P-03: pack drill, manual create, manual status, dispatch, tracking/fail, POD, return, cancel and backorder decision.

## 15. Open Questions

| OQ | Question | Status/owner |
|---|---|---|
| OQ-01 | maxAttempts และ max POD photos ให้ค่าเริ่มต้นเท่าไร/ใครแก้ | รอ Warehouse owner |
| OQ-02 | สิทธิ์ picker สำหรับ cancel/return/manual transition ใน production | รอ BA/IAM |
| OQ-03 | manual driver/vehicle เป็น snapshot ต่อใบหรือสร้าง Fleet master candidate | รอ PM/BA + Fleet owner |
| OQ-04 | Stock Transfer contract สำหรับ dispatched/delivered/reversed และ ownership ปลายทาง | รอ Inventory architect |
| OQ-05 | ของปฏิเสธต้องเข้า RTN/QC ก่อน available stock หรือไม่ | รอ Warehouse/QC |
| OQ-06 | AR billing/close-short/Credit Note contract ที่แท้จริง | รอ AR/Accounting |
| OQ-07 | event/catalog และ doc type code ใดมีอยู่แล้วใน F-NOTIFY/F-DOCCFG | ตรวจ declaration; ชนแล้ว reuse ห้ามประกาศซ้ำ |
| OQ-08 | KPI latency/throughput target หลังได้ production baseline | รอ Ops |

## 16. Security & Compliance

Preset: P1 Standard Transaction. Highest classification: **Confidential** (ชื่อ/เบอร์ผู้ติดต่อ คนขนส่ง ที่อยู่จัดส่ง และ operational audit); no Restricted field identified.

| Control | Requirement |
|---|---|
| AC-01 | IAM authorization and assignment scope on every mutation |
| AU-01 | append-only audit with actor/time/reason/source ref |
| IN-01 | validate source combine key, quantities, phone, tracking and state |
| TX-01 | atomic GI/reversal/source-sync + optimistic lock + idempotency |
| DP-01 | minimize PII in UI/log/export; preserve tenant/company isolation |
| IR-01 | correlate failures by DN and engine/outbox reference |

Risks: unauthorized state change (AC/AU), double GI (TX/IN), wrong cross-source sync (IN/TX), personal-data leakage (DP/AC), lost notification/snapshot (IR/outbox).

## 17. Health Check

| KPI/Control | Target / threshold | Action |
|---|---|---|
| GI/reverse without DN+source ref | 0 | block/rollback + alert |
| duplicate GI/idempotency conflict | 0 committed duplicates | return safe prior result/conflict |
| source sync mismatch | 0 | quarantine event + reconcile |
| failed attempt numbering | continuous from 1 | reject invalid append |
| notification/doc snapshot accepted | ≥99%; failures queued | retry via shared engine |
| page/API latency and daily volume | baseline before launch | set p95/stress at 2× peak after OQ-08 |

## 18. Monitoring

- Performance: queue query, create/dispatch/POD latency, shared-engine latency
- Closing: counts by source/mode/status/warehouse and GI reconciliation
- Anomaly: combine-key violation, stale version, duplicate key, orphan GI, unauthorized manual transition
- Transaction: DN audit, attempts, tracking, POD and inventory/source event refs
- Dashboard: open queue, ready/in-transit/failed, first-attempt success, returned/cancelled, outbox failures

## AI Review Report

- C01–C23: PASS; measurable metrics, Scope Lock, Value Stream, rule tags and screen inventory present
- PE01–PE05: PASS; COSO/system checks, security controls, KPI thresholds and monitoring are linked
- HTML alignment: PASS; 3 routes plus overlays match the approved prototype
- Warnings: OQ-01..08 remain explicit and do not authorize scope expansion
- Verdict: **APPROVED — ready for FRD**
