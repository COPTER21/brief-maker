# CTX — F-WH-STOCKTAKE: Stocktake รอบตรวจนับใหญ่

> **derived from:** FRD F-WH-STOCKTAKE v1.0 · **generated:** 2026-09-20
> **module:** Warehouse · **status:** active
> ⚠ Derived artifact — source of truth คือ FRD Pack · ถ้า FRD revise ต้อง regen CTX

---

## 1. Summary

F-WH-STOCKTAKE จัดการรอบตรวจนับใหญ่ตามคลัง โซน หรือตำแหน่ง โดยหัวหน้างานสร้างรอบและสั่งล็อก scope ก่อนเก็บยอด จำนวน และต้นทุน ณ จุดเวลาเดียวกันเป็น snapshot ที่แก้ย้อนหลังไม่ได้ ผู้ตรวจนับที่ได้รับมอบหมายส่งผลแบบ blind count และระบบบังคับผู้ตรวจคนที่สองเมื่อผลต่างเกิน threshold version ของรอบ ผลต่างที่ยืนยันแล้ว resolve สายอนุมัติจาก DOA ตามมูลค่าส่วนต่างสัมบูรณ์ เมื่ออนุมัติครบ ระบบส่งข้อมูลให้ F082 สร้าง Stock Adjustment draft แล้วจึงปิดรอบและปล่อย lock; feature นี้ไม่แก้ on-hand โดยตรง

## 2. Data Contract

### Entities

| Entity | PK / uniqueness | Key fields ที่ feature อื่นใช้ | หมายเหตุ |
|---|---|---|---|
| `T_stocktake_round` | `id`; `adjustment_ref` unique | `tenant_id`, `round_code`, `scope_type`, `scope_key`, `status`, `freeze_at`, `snapshot_watermark`, `threshold_policy_ref`, `doa_entry_ref`, `approval_base_amount`, `approval_chain`, `adjustment_ref`, `version` | aggregate root; `round_code` ไม่ใช่ document number |
| `T_stocktake_snapshot_line` | `id`; unique `(round_id,item_id,location_id)` | `round_id`, `tenant_id`, `item_id`, `location_id`, `uom_id`, snapshot labels, `system_qty`, `unit_cost`, `captured_at`, `inventory_version` | immutable baseline; item/location/UoM เป็น soft reference |
| `T_stocktake_count_sheet` | unique `(round_id,count_round)` | `round_id`, `count_round`, `assignee_id`, `status`, `submitted_at` | `count_round` มีค่า 1 หรือ 2 |
| `T_stocktake_count_line` | ตาม schema ของ sheet line | `sheet_id`, `snapshot_line_id`, `counted_qty`, `evidence`, `submitted_at` | `counted_qty >= 0`; submission ต้องครบ snapshot |
| `T_stocktake_approval_step` | unique `(round_id,level)` | `round_id`, `level`, `role_slot`, `person_id`, `decision`, `reason`, `decided_at` | chain snapshot ตาม DOA; บังคับลำดับและ optimistic version |
| `T_stocktake_lock` | active unique `(tenant_id,scope_key)` พร้อม overlap check | `tenant_id`, `scope_key`, `round_id`, `active_from`, `released_at` | Inventory engine ใช้กัน movement ใน canonical scope |
| `T_stocktake_handoff` | `round_id` unique; idempotency key unique ภายใน tenant | `round_id`, `idempotency_key`, `payload_hash`, `adj_id`, `ack_status`, `ack_at` | เก็บ F082 request/ack ครั้งเดียว |
| `T_stocktake_audit_event` | `(round_id,seq)` | `round_id`, `seq`, `event_type`, `actor_id`, `occurred_at`, `payload` | append-only; ไม่มี UPDATE/DELETE grant |

### Enums / States

| Field | Values / transitions | Transition owner |
|---|---|---|
| `T_stocktake_round.status` | `draft → frozen → counting → recount? → review → pending → approved → closed`; `pending → rejected` | F-WH-STOCKTAKE |
| `count_round` | `1`, `2` | F-WH-STOCKTAKE |
| approval `decision` | pending/no decision → `approved` หรือ `rejected` | current DOA approver ผ่าน F-WH-STOCKTAKE |
| F082 `ack_status` | `draft` ตาม contract รุ่นนี้ | F082 |
| `scope_type` | `warehouse`, `zone`, `location` | Warehouse/Location contract; Stocktake เก็บ canonical key |

### State Transition Contract

| From | Action | To | Required condition |
|---|---|---|---|
| `draft` | freeze | `frozen` | supervisor; scope ไม่ทับ; snapshot ยังไม่มี |
| `frozen` | assign count round 1 | `counting` | active person |
| `counting` | submit count | `recount` | active assignee; `abs(diff) > threshold_version` อย่างน้อยหนึ่งรายการ |
| `counting` | submit count | `review` | active assignee; ทุกผลต่างไม่เกิน threshold version |
| `recount` | assign round 2 | `recount` | assignee คนที่สองต่างจากคนแรก |
| `recount` | submit count round 2 | `review` | active recount assignee |
| `review` | resolve and submit approval | `pending` | DOA slots ครบ ไม่ซ้ำ และไม่เป็น counters |
| `pending` | approve intermediate | `pending` | current person/current step |
| `pending` | approve final | `approved` | current person/current step |
| `pending` | reject with reason | `rejected` | current person/current step; release scope lock |
| `approved` | F082 draft acknowledgment | `closed` | handoff สำเร็จครั้งแรก; release scope lock |

### Relationships

- `T_stocktake_round` 1—N `T_stocktake_snapshot_line` ผ่าน `round_id`
- `T_stocktake_round` 1—N `T_stocktake_count_sheet` ผ่าน `round_id`
- `T_stocktake_count_sheet` 1—N `T_stocktake_count_line` ผ่าน `sheet_id`
- `T_stocktake_round` 1—N `T_stocktake_approval_step` ผ่าน `round_id`
- `T_stocktake_round` 1—N `T_stocktake_audit_event` ผ่าน `round_id`
- `T_stocktake_round` 1—0..1 active `T_stocktake_lock` ผ่าน `round_id`
- `T_stocktake_round` 1—0..1 `T_stocktake_handoff` ผ่าน `round_id`
- อ่าน Item, Location, UoM, User และ DOA เป็น soft reference; ไม่เป็นเจ้าของ master เหล่านี้
- ทุก table มี `tenant_id`/RLS ตาม contract; identity และข้อมูลผลต่างบางส่วนเป็น Confidential

## 3. API Surface

Base path: `/api/v1/stocktake-rounds`

ทุก endpoint ต้องมี authentication, tenant context และ authorization ตาม action; mutation ต้อง audit

| Method | Endpoint | ทำอะไร | Payload / response หลัก |
|---|---|---|---|
| GET | `/api/v1/stocktake-rounds` | list/filter รอบตาม tenant/status | filters → round summary |
| POST | `/api/v1/stocktake-rounds` | สร้าง draft | `{name,scope:{warehouse_id,zone_id?,location_id?}}` → `{id,status:"draft"}` |
| POST | `/api/v1/stocktake-rounds/:id/freeze` | lock scope และ capture snapshot ใน transaction เดียว | `{expected_version}` → `{status,freeze_at,snapshot_count,lock_ref}` |
| POST | `/api/v1/stocktake-rounds/:id/assign` | มอบหมาย count/recount | `{count_round:1|2,person_id}` → `{status,assignee}` |
| POST | `/api/v1/stocktake-rounds/:id/count-submissions` | ส่งผลนับของ active assignee | `{count_round,lines:[{item_id,counted_qty,evidence?}],expected_version}` |
| GET | `/api/v1/stocktake-rounds/:id/variance` | อ่าน snapshot/count/diff/value สำหรับผู้มีสิทธิ์ | response มี final diff, unit cost snapshot, value diff, `absolute_variance_value`, threshold/effective date |
| POST | `/api/v1/stocktake-rounds/:id/submit-approval` | resolve DOA และ freeze chain | `{selected_people:[{slot_no,person_id}],expected_version}` |
| POST | `/api/v1/stocktake-rounds/:id/approval-decisions` | ตัดสิน current approval step | `{decision:"approved"|"rejected",reason?,expected_version}` |
| POST | `/api/v1/stocktake-rounds/:id/adjustment-draft` | ส่ง F082 handoff ครั้งเดียว | approved round → `{adj_id,status:"draft",round_status:"closed"}` |
| GET | `/api/v1/stocktake-rounds/:id/audit-events` | อ่าน append-only timeline ตามสิทธิ์ | authorized event projection |

### Mutation Safety

- Mutation ทุกตัวใช้ `Idempotency-Key`; key และ body เดิมคืนผลเดิมภายใน 24 ชั่วโมง
- ถ้า key เดิมแต่ body ต่างกันให้ conflict; state mutation ใช้ `If-Match` หรือ `expected_version`
- Permission/person/state ต้องตรวจซ้ำตอน mutation ไม่เชื่อค่าจาก client
- Counter projection ต้องไม่ส่ง `system_qty`, `unit_cost`, variance หรือผล threshold
- F082 failure ต้องคงรอบเป็น `approved` และ lock ยัง active เพื่อ retry อย่างปลอดภัย

### External Calls / Contracts

| Target | Trigger | Contract หลัก |
|---|---|---|
| Inventory engine | freeze | acquire canonical scope lock; อ่าน qty/cost/watermark ใน atomic boundary |
| Inventory engine | rejected/closed | release lock เฉพาะ `round_id`/scope ของรอบ |
| DOA F019 | submit approval | resolve `{feature,action:"approve_variance",absolute_variance_value,effective_at}` |
| F082 Stock Adjustment | approved handoff | `{ref_count_doc,scope,freezeAt,approvedBy,lines:[{item,system_qty,counted_qty,diff,cost}]}` |
| F082 Stock Adjustment | handoff acknowledgment | `{adjId,status:"draft"}` |
| F089 Barcode | optional input | input hook เท่านั้น; contract implementation ยังไม่อยู่ใน release นี้ |

### Events Emitted

FRD ระบุ audit event สำหรับทุก mutation และ state transition ผ่าน `T_stocktake_audit_event`; ชื่อ integration event/topic ภายนอกไม่ได้กำหนดเป็น contract ใน FRD v1.0 (`[not documented]`)

## 4. Shared Rules (cross-boundary เท่านั้น)

| Rule ID | Rule | กระทบใคร |
|---|---|---|
| BR-ST-01 | freeze ต้องได้ canonical scope lock และห้าม active scope แบบเดียวกัน/parent/child ทับกัน | Inventory movement features และ Warehouse scope owner |
| BR-ST-02 | qty, unit cost และ watermark ต้อง capture atomically และ immutable หลัง freeze | Inventory engine, F082, audit/reconciliation |
| BR-ST-03 | counter-facing contract ห้ามเปิด system balance, cost หรือ variance | identity/permission layer และ consumer ของ count DTO |
| BR-ST-04 | recount gate ใช้ `abs(diff) > threshold_version`; ค่าเท่ากับ threshold ไม่ trigger | Inventory policy/config และ F086 ที่วางแผน reuse engine |
| BR-ST-07 | DOA basis คือ `Σ abs(diff_qty × unit_cost_snapshot)` | DOA F019 และ finance/audit consumers |
| BR-ST-08 | resolve DOA ตอน submit แล้ว freeze chain; slots ต้องครบ ไม่ซ้ำ และไม่เป็น counters | DOA F019, identity master, approval consumers |
| BR-ST-10 | ส่ง F082 หลัง approved ได้ครั้งเดียว; close/release lock เฉพาะเมื่อได้ draft acknowledgment | F082 และ Inventory engine |
| LOCK-ST-05 | Stocktake ไม่ post movement หรือแก้ on-hand; F082 เป็นเจ้าของการปรับยอดจริง | F082 และ Inventory ledger |

### Cross-Boundary Calculation

- Final count ใช้ count round 2 เมื่อมี submission มิฉะนั้นใช้ count round 1
- `diff = final_count - system_qty_snapshot`
- `value_diff = diff × unit_cost_snapshot`
- `absolute_variance_value = Σ abs(value_diff)`
- Handoff line ใช้ final accepted count และ cost snapshot ห้ามอ่าน current cost ใหม่

## 5. Integration

- **Depends on:** Warehouse/Location F008 สำหรับ scope; Inventory F009/Item สำหรับ balance, cost และ watermark; Roles F020/User สำหรับ assignee/approver; DOA F019 สำหรับ action `approve_variance`
- **Depended by:** F082 Stock Adjustment รับ approved variance เป็น draft; Inventory movement engine อ่าน active lock; F086 Cycle Count วางแผน reuse variance engine/adapter ตาม FRD
- **Optional input:** F089 Barcode เป็น hook สำหรับรับ count input; contract จริงยัง `[not documented]`
- **Declarations:** DOA yes — action `approve_variance`, scope `policy_approve`, sequential chain, basis `absolute_variance_value`; NTF no declaration ในรอบนี้; CSQ `[not documented]`; DOCCFG no เพราะไม่ใช่เอกสาร/ไม่มี running number
- **DOA wire status:** `pending`; role ids, ช่วงวงเงินจริง และ merged/per-warehouse mode ยังต้องยืนยันใน DOA กลาง
- **Engine hooks:** `stocktake-variance-engine` [DRAFT] และ `stock-adjustment-draft-adapter` [DRAFT]
- **Lock lifecycle:** acquire ตอน freeze; release เมื่อ rejected หรือเมื่อ F082 draft ack ทำให้ round closed; failure ห้าม release
- **Data boundary:** multi-tenant RLS ทุก table; `system_qty`, `unit_cost`, `variance_value`, selected people และ approval identity เป็น Confidential/PII ตาม field
- **Retention:** round/count/approval/handoff/audit 7 ปี หรือ Warehouse policy ถ้านานกว่า

### Unresolved Contract Points

- กลไก query/registry ของ lock สำหรับ movement features ยังต้องยืนยันกับ Inventory owner
- permission จริงสำหรับ supervisor reveal และ approver ต้องยืนยันกับ Policy owner
- DOA tier และ `role-*` mapping จริงต้องยืนยันกับ Warehouse BA/DOA admin
- F082 payload/ack/error/retry contract สุดท้ายต้องยืนยันกับ F082 owner

---

*trace: §1 ← FRD `00_OVERVIEW` + BRD §§1–3 · §2 ← FRD `04_DB` + `05_RULES` §5.2 · §3 ← FRD `02_API` + `03_LOGIC` · §4 ← FRD `05_RULES` · §5 ← BRD §12 + `DOA_BRIEF_F-WH-STOCKTAKE.md`*
