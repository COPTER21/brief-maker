# PROPOSALS outbound — F-WH-STOCKTAKE

## สถานะ

ไม่มีข้อเสนอใดเป็น blocker ของ pack รอบนี้ และไม่มีการแก้ feature อื่นโดยพลการ

## ข้อเสนอสำหรับ implementation จริง

1. เพิ่ม focus trap และคืน focus ให้ปุ่มต้นทางเมื่อปิด drawer/modal เพื่อรองรับ keyboard user
2. ล็อก body scroll ขณะ overlay เปิด โดยใช้มาตรฐาน shared UI kit
3. bundle icon/font ที่จำเป็นใน production เพื่อไม่พึ่ง CDN ระหว่างใช้งานคลัง
4. แสดง loading/error/retry state ของ inventory snapshot, DOA lookup และ F082 handoff ให้ชัดเจน
5. เก็บ persona switch ไว้เฉพาะ demo/test build; production ต้องผูก identity/permission จริง

## Open Questions ที่ BA/PM ต้องยืนยันก่อน production

| OQ | คำถาม | ผลกระทบ |
|---|---|---|
| OQ-ST-01 | movement ที่ timestamp เท่ากับ `locked_at` ให้อยู่ก่อนหรือหลัง cut-off | สูตร snapshot และ integration test |
| OQ-ST-02 | mapping role/person จริงของ DOA แต่ละ tier คืออะไร | การตั้งค่า F-DLG-001; prototype เป็นตัวอย่างเท่านั้น |
| OQ-ST-03 | contract สุดท้ายของ F082 adapter รวม error/retry/ack field ใช้ชื่อใด | handoff และ idempotency |

## PENDING_REGISTRY

ไม่มีรายการใหม่ที่เป็นปัญหา BASE-KIT/CI ร่วม ระบบเตือน font-size hardcode เป็น warning ระดับ style ของ prototype และไม่กระทบ business coverage; ข้อเสนอเฉพาะ feature อยู่ในเอกสารนี้แล้ว
