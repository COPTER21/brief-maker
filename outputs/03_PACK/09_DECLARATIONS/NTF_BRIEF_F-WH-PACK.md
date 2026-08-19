# NTF_BRIEF — F-WH-PACK Packing

> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode channel, recipient resolution หรือ preference ใน Packing · Feature นี้ไม่มี DOA events

## Event declarations

| Event ID | Trigger ที่ commit แล้ว | Audience intent | Template variables | Catalog | ปิดได้ |
|---|---|---|---|---|:---:|
| `pack_started` | API-05 / FN-02: job queue → pack `in_progress` | ผู้รับผิดชอบงาน + หัวหน้าคลังตาม warehouse scope | `{pack_no,pick_no,source_ref,assignee_name,warehouse_code}` | `doc_status` | ✓ |
| `pack_box_closed` | API-08 / FN-05: carton `active→closed` | ผู้รับผิดชอบงาน; watcher ที่ตั้งค่ารับ progress | `{pack_no,box_no,total_boxes,packed_qty,remaining_qty,weight}` | `doc_status` | ✓ |
| `pack_done` | API-10 / FN-07: pack `in_progress→packed` | หัวหน้าคลัง + downstream audience ที่ Notification config resolve | `{pack_no,source_ref,total_boxes,total_pieces,total_weight,packed_at}` | `doc_status` | ✓ |
| `pack_cancelled` | API-12 / FN-09: pack → `cancelled` | ผู้รับผิดชอบ job + หัวหน้าคลัง + source owner ตาม config | `{pack_no,pick_no,source_ref,cancelled_by,cancel_reason}` | `doc_status` | ✗ |

Required envelope: `event_id`, `event_version`, `tenant_id`, `warehouse_id`, `ref:{type:'pack',id,pack_no}`, `actor_id`, `occurred_at`, `correlation_id`, `idempotency_key`, `vars`. Payload ห้ามมีที่อยู่/เบอร์ผู้รับเต็มถ้า template ไม่จำเป็น

## Catalog decision

F-NOTIFY snapshot (`Related context/f-notify/f-notify.html` lines 342–356) มี preference category `doc_status` อยู่แล้ว จึงไม่แก้ `EVENT_GROUPS`. Business event IDs ด้านบนใช้ routing/template registry แต่ map preference ไปหมวดเดิม

## Ownership exclusions

- `dn_created` เป็น event ของ Delivery Note owner และไม่มี locked DN artifact จึง **ไม่ประกาศโดย Packing**
- Picking `pick_done`/handoff เป็น event ของ Picking ห้ามยิงซ้ำ
- ไม่มี `doa_pending`, `doa_result`, `doa_escalate`
- print job success/failure เป็น operational telemetry ของ print platform ไม่ใช่ end-user event รอบนี้

## Dev wiring

Insert outbox row ใน transaction เดียวกับ state transition; worker เรียก `ENG-NOTIFY.emit` หลัง commit. Same dedupe key must not create duplicate notification. Notification failure retries independently and never rolls back pack/carton state. Channel, localization, recipient expansion, quiet hours and opt-out are owned by F-NOTIFY

## Verification

- 4 events trace to `03_LOGIC` and state/rule in `05_RULES`
- no event fires before commit or on failed/idempotent replay duplicate
- no channel/recipient hardcode in Packing
- no duplicated DOA/Picking/DN ownership
