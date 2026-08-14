# Outbound Handoff — F-CUST-CL-001

## Open Questions ที่ต้องยืนยันก่อนต่อระบบจริง

1. DOA ใช้วงเงินที่ขอแบบยอดรวม หรือใช้ส่วนต่างจากวงเงินเดิม
2. ยืนยัน role ID และช่วงวงเงินจริงใน DOA กลางสำหรับ `F-CL-001`
3. การระงับ/ปลดระงับต้องผ่านสายอนุมัติหรือไม่
4. เกณฑ์ความเสี่ยงและค่าใกล้เต็ม 85% เป็นค่าที่ BA ยืนยันแล้วหรือยัง
5. เจ้าของและกำหนดส่ง contract ของ Customer Master, Sales Order, AR Invoice และ My Profile

## Declaration รอบนี้

`doa-declaration` — ใช้แล้ว: ออก `DOA_BRIEF_F-CL-001.md` สำหรับประกาศความต้องการสายอนุมัติกลาง

ไม่ได้ใช้ `doccfg-declaration` และ `ntf-declaration` ตามการยืนยันของ PM/BA

## Pending registry

ไม่มีรายการ Base-kit/CI ที่ต้องเพิ่มใน registry รอบนี้
