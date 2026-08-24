# NTF_BRIEF — F-WH-DN Delivery Note

> ตรวจ catalog สดจาก `Related context/f-notify/f-notify.html` แล้วเมื่อ 2026-08-20
> ยิงผ่าน ENG-NOTIFY เท่านั้น — ห้าม hardcode channel/preference · ไม่มี DOA events ในใบนี้

## Business events

| Event ID | Trigger (FRD) | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| `dn_ready` | draft→ready; FN-06 | ผู้รับผิดชอบ DN + ทีมคลัง | **{dn_no}** พร้อมส่งแล้ว — นัด {ship_date} {slot} | in-app | ✓ |
| `dn_dispatched` | ready→in_transit หลัง GI สำเร็จ; FN-07 | ผู้สร้าง/ผู้รับผิดชอบ + Sales/Transfer owner + ผู้ติดต่อที่เปิดรับ | **{dn_no}** ออกรถแล้ว — {carrier_summary} | in-app | ✓ |
| `dn_tracking_updated` | append tracking stage; FN-08 | ผู้เกี่ยวข้องกับเอกสาร + ผู้ติดต่อที่เปิดรับ | **{dn_no}** อัปเดตการจัดส่ง — {tracking_stage} | in-app | ✓ |
| `dn_failed` | in_transit→failed; FN-09 | ผู้รับผิดชอบ + หัวหน้าคลัง + Sales/Transfer owner | **{dn_no}** ส่งไม่สำเร็จ ครั้งที่ {attempt_no} — {reason} | in-app | ✗ บังคับฝ่ายปฏิบัติการ |
| `dn_rescheduled` | failed→ready; FN-11 | ผู้เกี่ยวข้องกับเอกสาร + ผู้ติดต่อที่เปิดรับ | **{dn_no}** นัดส่งใหม่ — {ship_date} {slot} | in-app | ✓ |
| `dn_delivered` | POD result delivered; FN-10 | ผู้สร้าง/ผู้รับผิดชอบ + Sales/Transfer owner + ผู้ติดต่อที่เปิดรับ | **{dn_no}** ส่งสำเร็จ — ผู้รับ {receiver_name} | in-app | ✓ |
| `dn_partial` | POD result partial; FN-10 | ผู้รับผิดชอบ + หัวหน้าคลัง + Sales/Transfer owner | **{dn_no}** ส่งได้บางส่วน — ไม่รับ {rejected_total} หน่วย | in-app | ✗ บังคับฝ่ายปฏิบัติการ |
| `dn_returned` | return all / rejected; FN-12/FN-10 | ผู้รับผิดชอบ + หัวหน้าคลัง + Sales/Transfer owner | **{dn_no}** ตีกลับทั้งใบ — คืนสต๊อกและคืนใบแพ็คเข้าคิวแล้ว | in-app | ✗ บังคับฝ่ายปฏิบัติการ |
| `dn_cancelled` | cancel pre/post dispatch; FN-13 | ผู้เกี่ยวข้องกับเอกสาร + Sales/Transfer owner | **{dn_no}** ถูกยกเลิก — {reason} | in-app | ✓ |
| `dn_backorder_decided` | partial retry/close-short; FN-14 | Sales owner + ผู้รับผิดชอบ DN | **{dn_no}** ตัดสินใจของไม่รับแล้ว — {decision_label} | in-app | ✗ บังคับเจ้าของงาน |

Manual status changes do **not** emit the events above automatically because LOCK-07/BR-DN-18 isolates Manual DN from reference automation. หากธุรกิจต้องการแจ้ง Manual status ในอนาคต ให้ประกาศ event แยกหลัง PM/BA ยืนยัน ไม่ reuse transition โดยเดา.

## Event Catalog mapping

F-NOTIFY ปัจจุบันมี category `doc_status` ซึ่งครอบสถานะเอกสารธุรกรรมทั้งหมดข้างบน จึง **ไม่เพิ่ม EVENT_GROUPS ใหม่**. Event IDs เป็น business routing/template IDs และ preference category reuse `doc_status`.

ไม่มี `doa_pending`, `doa_result` หรือ `doa_escalate` เพราะ Delivery Note รอบนี้ไม่มี approval chain และ events เหล่านั้นเป็นของ DOA engine.

## Payload minimum

ทุก emit มี `{ ref:{type:'DLV',id:dn_id,no:dn_no}, vars, tenant_id, company_id, actor_id, correlation_id }`. `vars` ส่งเฉพาะค่าที่ template ใช้; ห้ามส่งที่อยู่เต็ม เบอร์โทร ลายเซ็น หรือรูป POD โดยไม่จำเป็น.

## Dev wiring note

- เรียก `ENG-NOTIFY.emit(event_id,{ref,vars})` ผ่าน transactional outbox ที่ transition ใน `03_LOGIC`
- feature ไม่เลือก email/LINE และไม่อ่าน preference เอง; Notification Center ตัดสิน channel
- emit ล้มเหลวไม่ rollback business transaction เมื่อ outbox ถูก commit แล้ว; worker retry ด้วย event idempotency key

## Open items

- OQ-NTF-01: ยืนยันกลุ่มผู้ติดต่อภายนอกที่มี consent/ช่องทางอยู่แล้ว; จนกว่าจะยืนยันให้ recipient resolver คืนเฉพาะผู้ใช้ภายใน
- OQ-NTF-02: ยืนยันว่า `dn_tracking_updated` ทุก stage หรือเฉพาะ milestone สำคัญ เพื่อลด notification noise

