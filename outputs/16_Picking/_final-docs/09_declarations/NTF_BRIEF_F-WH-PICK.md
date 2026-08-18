# NTF_BRIEF — F-WH-PICK Picking

> ยิงผ่าน ENG-NOTIFY เท่านั้น ห้าม hardcode channel/preference ใน Picking · Feature นี้ไม่มี DOA events

## Event declarations

| Event ID | Trigger (FRD) | ผู้รับ | Template | Catalog group | Channel default | ปิดได้ |
|---|---|---|---|---|---|:---:|
| `pick_assigned` | assign สำเร็จ: `03_LOGIC` FN-05 / API-04 | ผู้หยิบที่ได้รับมอบหมาย + หัวหน้าคลังที่เกี่ยวข้อง | **{pick_no}** ถูกมอบหมายให้ {assignee_name} — กำหนดส่ง {due_date} | `mention` | in-app | ✓ |
| `pick_short` | รายงานขาดต่อบรรทัด: FN-08 / API-07 | Sales owner ของ SO + หัวหน้าคลัง | **{pick_no}** หยิบ {item_name} ได้ไม่ครบ {short_qty} {uom} — SO {so_no} มี backorder | `doc_status` | in-app | ✗ |
| `pick_done` | `in_progress → picked`: FN-12 / API-11 | หัวหน้าคลัง + ผู้เกี่ยวข้องกับ SO/Packing | **{pick_no}** หยิบเสร็จแล้ว — พร้อมส่งต่อ Packing | `doc_status` | in-app | ✓ |
| `pick_short_close` | close-short: FN-13 / API-12 | Sales owner ของทุก SO + หัวหน้าคลัง | **{pick_no}** ปิดงานแบบขาด — ส่ง Packing เฉพาะสินค้าที่หยิบได้ | `doc_status` | in-app | ✗ |

Required payload ทุก event: `ref:{type:'pick',id,pick_no}`, `warehouse_id`, `source_refs[]`, `actor_id`, `occurred_at`, `idempotency_key`; เพิ่มตัวแปรเฉพาะ event ตาม template.

## Event catalog decision

F-NOTIFY ปัจจุบันมี `doc_status` และ `mention` ซึ่งครอบความหมายแล้ว จึง **ไม่เพิ่มแถวใหม่ใน EVENT_GROUPS**. Event ID ด้านบนเป็น business event สำหรับ routing/template แต่ preference category reuse ของเดิม.

## Excluded ownership

- `so_released` เป็น event ของ Sales Order/Finance upstream ไม่ประกาศซ้ำใน Pick
- `inv_replenish_request` และ `inv_replenished` เป็น event ของ Inventory contract ไม่ประกาศเป็น event เจ้าของโดย Pick
- ไม่มี `doa_pending`, `doa_result`, `doa_escalate`

## Dev wiring

`ENG-NOTIFY.emit(event_id,{ref,vars,...})` ถูกเรียกผ่าน transactional outbox หลัง transition/transaction สำเร็จตาม FN ที่อ้าง. Picking ห้ามอ่าน preference, เลือก email/LINE หรือฝังข้อความ template ใน feature code. Notification failure ค้าง retry และไม่ย้อน business transaction.

## Verification

- event ทุกตัวมี Pick ref และ transition จริง
- ไม่มี event ซ้ำกับ DOA
- catalog mapping ใช้ของเดิม ไม่แก้ feature F-NOTIFY
- OQ-06 ปิดแล้ว: catalog snapshot จาก `Related context/f-notify/f-notify.html` EVENT_GROUPS
