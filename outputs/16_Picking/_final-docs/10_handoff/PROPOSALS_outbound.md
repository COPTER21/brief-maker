# Outbound Handoff — F-WH-PICK Picking

เอกสารนี้รวบรวมเฉพาะเรื่องที่ต้องส่งให้เจ้าของระบบที่เกี่ยวข้องพิจารณาต่อ ยังไม่ถือว่าได้รับอนุมัติ และรอบนี้ไม่มีการแก้ artifact ของฟีเจอร์อื่น

## Open Questions ที่ยังต้องยืนยัน

1. **OQ-01 — ค่าควบคุมการสร้างงาน:** `waveMax` และเกณฑ์เตือนจำนวนงานค้างของผู้หยิบ มาจาก setting ใด และฝ่ายใดเป็นเจ้าของการตั้งค่า — รอ BA และ Warehouse owner
2. **OQ-02 — ขอบเขตสิทธิ์ผู้หยิบ:** ผู้หยิบทั่วไปปิดงานแบบของขาดหรือ override ตำแหน่งหยิบได้เองหรือไม่ หรือจำกัดเฉพาะหัวหน้าคลัง — รอ BA และ IAM
3. **OQ-03 — เจ้าของ allocation engine:** ต้องลงทะเบียน `pick-allocation-engine` ที่ใด ใครเป็นเจ้าของ และผู้ใช้กลุ่มใดเปลี่ยนกลยุทธ์การจัดสรรได้ — รอ Architect และ BA
4. **OQ-04 — เหตุผลการ override:** การเปลี่ยนตำแหน่งหรือล็อตที่ระบบแนะนำต้องบังคับกรอกเหตุผลทุกครั้งหรือไม่ — รอ Warehouse owner
5. **OQ-05 — Contract ส่งต่อ Packing:** รูปแบบข้อมูลที่ Packing รับจาก Pick และวิธีป้องกันการสร้าง PACK ซ้ำจากใบสั่งขายเดียวกัน — รอเจ้าของ Packing/Delivery Note

`OQ-06` ปิดแล้วจากการตรวจ event catalog ของ F-NOTIFY ระหว่างทำ NTF declaration

## ข้อเสนอส่งต่อเจ้าของระบบ

1. **Architect / BA:** กำหนด owner, registration และขอบเขตการตั้งค่าของ `pick-allocation-engine`
2. **BA / Warehouse owner:** กำหนดแหล่ง setting และผู้ดูแลค่า `waveMax` กับ workload warning
3. **IAM / Warehouse owner:** ยืนยัน permission matrix สำหรับปิดงานแบบของขาด, manual override และข้อกำหนดเรื่องเหตุผล
4. **Packing / Delivery Note:** จัดทำ idempotent intake contract, กติกาป้องกัน PACK ซ้ำ และพฤติกรรมกรณีลูกค้ามารับเอง โดยไม่เพิ่ม logic เหล่านี้ใน Pick
5. **Notification owner:** wire event `pick_assigned`, `pick_short`, `pick_done` และ `pick_short_close` ตาม `NTF_BRIEF_F-WH-PICK.md`; ใช้ event group ที่มีอยู่แล้ว จึงไม่ต้องเพิ่มรายการ catalog รอบนี้

## Pending registry

ไม่มีรายการ Base-kit/CI ใหม่ที่ต้องเพิ่มใน `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md`

## Declaration รอบนี้

`ntf-declaration` — ดำเนินการแล้วและออก `NTF_BRIEF_F-WH-PICK.md`

ไม่ได้ใช้ `doccfg-declaration` และ `doa-declaration` ตามการเลือกของผู้ใช้
