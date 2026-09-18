# CTX — F-WH-ROP: Reorder Point / จุดสั่งซื้อซ้ำ

> **derived from:** FRD F-WH-ROP v2.0 · **generated:** 2026-09-18
> **module:** Warehouse · W4 FULL · **status:** active
> ⚠ Derived artifact — source of truth คือ FRD · ถ้า FRD revise ต้อง regen CTX

---

## 1. Summary

F-WH-ROP เก็บนโยบายเติมสินค้าแบบมีรุ่นต่อ Item×Warehouse และประเมินยอดพร้อมใช้จาก F009
เพื่อหาสินค้าที่ต่ำกว่าจุดสั่งเติม ระบบทำงานจากรอบเวลา การเปลี่ยนยอดสินค้า หรือการเรียกตรวจด้วยคน
เมื่อเข้าเงื่อนไข ระบบส่งข้อเท็จจริงให้ ENG-NOTIFY และขอให้ F072 สร้าง PR Draft รวมต่อคลังต่อรอบ
F085 ไม่แก้ยอดสินค้า ไม่คำนวณ Quality Hold ซ้ำ ไม่สร้าง PO และไม่ส่ง PR เข้าอนุมัติอัตโนมัติ
ผู้ใช้หลักคือผู้ดูแลนโยบายคลัง นักวางแผนเติมสินค้า และผู้ตรวจสอบประวัติ

## 2. Data Contract

### 2.1 Entities

| Entity | PK | Key fields | หมายเหตุ |
|---|---|---|---|
| `rop_policy_version` | `policy_ref` | `tenant_id`, `item_id`, `warehouse_id`, `version`, `effective_date`, `enabled` | นโยบายหนึ่งรุ่นแก้ย้อนหลังไม่ได้ |
| `rop_policy_version` | `policy_ref` | `min_qty`, `max_qty`, `safety_qty` | เกณฑ์เติมต่อ Item×Warehouse |
| `rop_policy_version` | `policy_ref` | `lead_time_days`, `adu_window_days`, `pack_size` | ตัวแปรการคำนวณและการปัดจำนวน |
| `rop_policy_version` | `policy_ref` | `preferred_vendor_id?` | ผู้ขายที่เสนอเท่านั้น ไม่ใช่ผู้ขายสุดท้าย |
| `rop_policy_version` | `policy_ref` | `created_at`, `created_by`, `correlation_id` | หลักฐานการสร้างรุ่น |
| `rop_run` | `run_id` | `tenant`, `trigger_type`, `trigger_ref`, `scope_ref` | รอบประเมินสินค้า |
| `rop_run` | `run_id` | `started_at`, `completed_at`, `status` | สถานะการทำงานของรอบ |
| `rop_run` | `run_id` | `idempotency_key`, `correlation_id` | ป้องกันทำรอบเดิมซ้ำ |
| `rop_suggestion_event` | `event_id` | `run_id`, `tenant`, `policy_ref`, `version` | ผลประเมินแบบ append-only |
| `rop_suggestion_event` | `event_id` | `snapshot_ref`, `as_of`, `item_id`, `warehouse_id` | อ้าง snapshot จาก F009 |
| `rop_suggestion_event` | `event_id` | `atp`, `adu`, `on_order`, `reorder_point` | ค่าต้นทางและจุดสั่งเติม |
| `rop_suggestion_event` | `event_id` | `raw_qty`, `suggested_qty`, `pack_size` | จำนวนก่อนและหลังปัด |
| `rop_suggestion_event` | `event_id` | `status`, `reason`, `occurred_at` | ผลและเหตุผลของการประเมิน |
| `rop_suggestion_event` | `event_id` | `idempotency_key` | ผลจากรอบเดียวกันต้องไม่ซ้ำ |
| `rop_integration_event` | `event_id` | `tenant`, `kind`, `source_ref`, `external_ref?` | หลักฐานการส่งข้ามระบบ |
| `rop_integration_event` | `event_id` | `warehouse_id`, `payload_digest`, `status` | เก็บ reference/digest เท่าที่จำเป็น |
| `rop_integration_event` | `event_id` | `occurred_at`, `idempotency_key`, `correlation_id` | รองรับ replay และ trace |

### 2.2 Keys and uniqueness

- `rop_policy_version` unique: `(tenant_id, item_id, warehouse_id, version)`
- การเลือกนโยบายใช้คู่ Item×Warehouse และวันที่มีผล
- `rop_run.idempotency_key` ต้อง unique
- `rop_suggestion_event.idempotency_key` ต้อง unique
- `rop_integration_event.idempotency_key` ต้อง unique
- ข้อมูลทุก entity อยู่ภายใต้ tenant scope
- F085 ไม่เป็นเจ้าของ table เอกสาร PR ของ F072

### 2.3 Enums / States

| Field | Values | Transition owner |
|---|---|---|
| `rop_run.trigger_type` | `schedule`, `movement`, `manual` | F085 |
| `rop_suggestion_event.status` | `triggered`, `near`, `normal`, `no_policy`, `snapshot_unavailable` | F085 evaluator |
| `rop_integration_event.kind` | `notification.emitted`, `pr.draft.created`, `csq.master.changed` | F085 integration layer |
| Policy lifecycle | `Future`, `Effective`, `Superseded` | F085 version selection |
| F072 acknowledgement | `draft` with `submitted=false` | F072 |

### 2.4 Relationships

- `rop_policy_version` 1—N `rop_suggestion_event` ผ่าน `policy_ref` และ `version`
- `rop_run` 1—N `rop_suggestion_event` ผ่าน `run_id`
- `rop_suggestion_event` 1—N `rop_integration_event` ผ่าน `source_ref`
- `item_id` อ้าง Item Master; F085 อ่านและตรวจ reference แต่ไม่เป็นเจ้าของ master
- `warehouse_id` อ้าง Warehouse Master และต้องผ่าน warehouse authorization
- `preferred_vendor_id` อ้าง Vendor Price List แบบ optional และใช้เป็นข้อเสนอเท่านั้น
- `snapshot_ref` อ้าง snapshot ที่ F009 เป็นเจ้าของ
- `external_ref` อาจอ้าง Notification acknowledgement หรือ F072 PR Draft

### 2.5 Constraints and classification

- Quantity ทุกค่าต้องไม่ติดลบ
- `safety_qty ≤ min_qty ≤ max_qty`
- `lead_time_days ≥ 0`
- `pack_size ≥ 1`
- `adu_window_days` เป็น `30`, `60` หรือ `90`
- Policy values และ stock figures เป็น Confidential business data
- Actor reference และ audit metadata ใช้ classification กลาง
- Integration envelope ไม่ส่งชื่อบุคคลดิบโดยไม่จำเป็น

## 3. API Surface

| ID | Method | Endpoint | ทำอะไร | Payload/keys หลัก |
|---|---|---|---|---|
| API-01 | GET | `/v1/reorder-policies` | อ่านรายการนโยบายและจำนวนสรุป | item, warehouse, status, search, asOf, page |
| API-02 | POST | `/v1/reorder-policies` | สร้างนโยบายรุ่นใหม่ | item/warehouse, min/max/safety, lead, ADU window, pack, vendor?, effective date, enabled, expected version |
| API-03 | GET | `/v1/reorder-suggestions` | อ่านผลประเมินและที่มาของสูตร | item, warehouse, status, asOf |
| API-04 | POST | `/v1/reorder-runs` | เริ่มรอบประเมิน | scope, trigger type/ref, idempotency key |
| API-05 | POST | `/v1/reorder-notifications` | ส่งเหตุการณ์แจ้งเตือน | suggestion, policy/version, snapshot/asOf, idempotency key |
| API-06 | POST | `/v1/reorder-pr-drafts` | ขอสร้าง PR Draft รวมต่อคลัง | warehouse, run, lines, origin type/ref, idempotency key |
| API-07 | GET | `/v1/reorder-events` | อ่านประวัติแบบ append-only | filters, page |

### 3.1 Success contracts

- API-02 คืน `201` พร้อม policy version ใหม่
- API-03 คืน F009 references, formula result และ suggestion status
- API-04 คืน run summary
- API-05 คืน accepted event reference
- API-06 คืน `{pr_draft_id, status:'draft', submitted:false}`
- API-07 คืน event ที่แปลงเป็นข้อความสำหรับผู้ใช้ได้

### 3.2 Error/replay contracts

- ทุก API ที่อ่านหรือเขียนข้อมูลธุรกิจต้องตรวจ authentication และ authorization
- API-02 ตอบ `409` เมื่อ version conflict และ `422` เมื่อข้อมูลหรือ master reference ไม่ถูกต้อง
- API-03 ตอบ `424` เมื่อ snapshot dependency ใช้งานไม่ได้
- API-04 replay key เดิมคืนผลเดิม; dependency failure ตอบ `424`
- API-05 failure จาก ENG-NOTIFY ตอบ `424`; replay ต้องไม่ส่ง event ซ้ำ
- API-06 replay คืน PR Draft เดิม; failure จาก F072 ตอบ `424`

### 3.3 Snapshot consumed from F009

```text
item_id
warehouse_id
atp
adu
on_order
as_of
snapshot_ref
```

ATP เป็นค่าสุดท้ายจาก F009 และห้าม F085 หัก reserved หรือ hold ซ้ำ

### 3.4 PR Draft contract to F072

- รวมเฉพาะ lines ที่มีจำนวนเป็นบวกของคลังเดียวกันใน run เดียวกัน
- หนึ่ง warehouse/run สร้าง PR Draft ได้หนึ่งใบ
- แต่ละ line ต้องอ้าง policy reference/version และ snapshot reference
- Preferred vendor เป็น suggestion และห้ามใช้แยก PR Draft ตาม vendor
- `origin_type='reorder_point'`
- `origin_ref={item_id, warehouse_id, rop_run_id}`
- F072 เป็นเจ้าของ `doc.created`, `doc.approved` และ lifecycle หลังจากรับ Draft

### 3.5 Events emitted

| Event | Trigger point | Payload keys |
|---|---|---|
| `reorder_point.triggered` | บันทึก suggestion ที่ `ATP < ROP` สำเร็จแล้ว | tenant, item, warehouse, policy/version, snapshot/asOf, ATP, ROP, suggested qty, idempotency, correlation |
| `master.changed` | commit นโยบายสำคัญรุ่นใหม่สำเร็จ | tenant, item, warehouse, policy, config version, changed fields, old/new values, actor, time, idempotency, correlation |

### 3.6 Events not owned by F085

- Threshold detection ไม่ใช่ CSQ event; เป็น trigger ของ `reorder_point.triggered`
- PR lifecycle events เป็นของ F072 และต้องไม่ประกาศซ้ำใน F085
- DOA events เกิดหลังคนส่ง PR เข้าอนุมัติใน F072

## 4. Shared Rules

| Rule ID | Rule | กระทบใคร |
|---|---|---|
| BR-ROP-03 | F085 ใช้ ATP จาก F009 ตามที่ได้รับ ห้าม query hold หรือหัก reserved/hold ซ้ำ | F009, Inventory integrations |
| BR-ROP-04 | `ROP=max(min,safety+ADU×lead)` และ trigger เฉพาะ `ATP<ROP` | F009 data provider, reporting consumers |
| BR-ROP-05 | `raw=max(0,max+safety−ATP−on_order)` แล้วปัดขึ้นตาม pack size | F009, F072 line consumer |
| BR-ROP-07 | Schedule 06:00, movement และ manual trigger ใช้ evaluator เดียวกัน | Scheduler, F009 movement producer |
| BR-ROP-08 | Notification ต้อง replay-safe และการตั้งค่าผู้รับ/ช่องทางอยู่ที่ส่วนกลาง | ENG-NOTIFY |
| BR-ROP-09 | หนึ่ง F072 Draft ต่อ warehouse/run; รวมหลาย line; ห้าม split ตาม vendor | F072, Procurement |
| BR-ROP-10 | PR ต้องเป็น Draft และ `submitted=false`; คนส่งเข้า DOA ภายหลัง | F072, DOA engine |
| BR-CSQ-01 | ส่ง `master.changed` เฉพาะ successful sensitive policy commit | F-CSQ-01 |
| BR-CSQ-02 | Candidate profile `CSQ-ROP-01`, SecC, unique ต่อ pair+version | F-CSQ-01 Registry |
| BR-CSQ-03 | Invalid/no-effect save ห้ามส่ง CSQ | F-CSQ-01 |
| BR-CSQ-04 | Threshold detection เป็น Notification ไม่ใช่ CSQ | ENG-NOTIFY, F-CSQ-01 |
| BR-CSQ-05 | PR lifecycle และ origin reference เป็นความรับผิดชอบของ F072 | F072 |

## 5. Integration

### 5.1 Depends on

- **F009 Inventory:** ให้ ATP, ADU, On-Order, `as_of` และ `snapshot_ref`
- **Item/Warehouse masters:** ใช้ตรวจ references และ authorization scope
- **Vendor Price List:** ให้ preferred vendor และค่าเริ่มต้น lead time เมื่อมี
- **ENG-NOTIFY:** รับ `reorder_point.triggered`; เป็นเจ้าของ recipient, template และ channel
- **F072 Purchase Requisition:** สร้าง PR Draft และเป็นเจ้าของ document lifecycle
- **F-CSQ-01:** รับ `master.changed` เข้า SecC หลัง policy commit

### 5.2 Depended by

- **F072:** รับ Draft lines พร้อม origin references เพื่อให้ตามกลับถึง ROP run ได้
- **Procurement flow:** ใช้ PR Draft ที่คนตรวจและ submit แล้วไปเปรียบเทียบ vendor และสร้าง PO
- **Audit/monitoring:** อ่าน append-only events, correlation และ external references
- Feature อื่นที่อ่าน policy/suggestion ของ F085: `[not documented]`

### 5.3 Declarations

- **DOA:** no declaration ใน F085; F072/DOA ทำงานหลังคน submit PR
- **NTF:** yes — `reorder_point.triggered`
- **CSQ:** yes — `master.changed` → SecC สำหรับ sensitive policy commit เท่านั้น
- **DOCCFG:** no declaration; F085 ไม่ออกเอกสารหรือเลขรัน

### 5.4 Engine hooks

- `ENG-NOTIFY.emit('reorder_point.triggered', facts)` จาก outbox consumer หลัง evaluation commit
- CSQ producer ส่ง `master.changed` หลัง policy version และ audit/outbox commit สำเร็จ
- F085 ไม่เก็บผลท่อ 7C และไม่แสดงการ์ดผล 7C
- F072 รับ origin fields และเป็นเจ้าของเหตุการณ์ของเอกสาร PR

### 5.5 Open integration questions

- รอยืนยัน `CSQ-ROP-01` กับ Profile Registry
- รอยืนยัน `master.changed` vocabulary และ trigger status กับเจ้าของ F-CSQ-01
- รอตัดสินว่า `enabled` เป็น sensitive change หรือไม่
- รอยืนยัน release ที่ F072 รองรับ `origin_type` และ `origin_ref`
- รอยืนยัน Data Classification ของ Inventory Config ก่อน production

---

*trace: §1 ← FRD 00_OVERVIEW + BRD §2–5 · §2 ← FRD 04_DB · §3 ← FRD 02_API + NTF/CSQ briefs · §4 ← FRD 05_RULES · §5 ← FRD 00_OVERVIEW + BRD §11–15 + declaration briefs*
