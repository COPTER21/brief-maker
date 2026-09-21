# FUNCTION_CHECKLIST — F-WH-STOCKTAKE

## หมวด 1 · รอบนับและ scope

| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-01 | เลือกคลัง/โซน/ตำแหน่งแบบค้นหาและกำหนด scope รอบนับใหญ่ | S05,S09/BR01 | — | — | — |
| FN-02 | แสดงรายการ Item/Location แบบ soft-reference | S05/BR01 | — | — | — |
| FN-03 | freeze movement เฉพาะ scope และกันรอบซ้อน | S05,S09,S12/BR01 | — | — | — |
| FN-04 | เก็บ snapshot ยอด ณ freeze time แบบไม่แก้ย้อนหลัง | S01,S05,S13/BR02 | — | — | — |

## หมวด 2 · ใบนับและผลต่าง

| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-05 | สร้างใบนับและมอบหมายคนจริง | S05/BR03 | — | — | — |
| FN-06 | ให้ผู้นับ blind ไม่เห็นยอดระบบ/ผลต่าง; supervisor reveal ตามสิทธิ์ | S01,S05/BR03 | — | — | — |
| FN-07 | บันทึกผลนับศูนย์ได้ แต่กันค่าติดลบและช่องว่าง | S01,S04/BR03 | — | — | — |
| FN-08 | คำนวณผลต่างหลังส่งและใช้ threshold config effective date | S02,S03,S08/BR04 | — | — | — |
| FN-09 | บังคับนับซ้ำโดยคนอิสระเมื่อเกิน threshold | S07/BR04 | — | — | — |

## หมวด 3 · อนุมัติและ handoff

| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-10 | ส่ง DOA slot คนจริง อนุมัติ/ปฏิเสธมีเหตุผลและ audit | S05,S06/BR05 | — | — | — |
| FN-11 | ส่งผลต่างไป Stock Adjustment W3-LITE mock แล้วปลด freeze ไม่ปรับยอดเอง | S10,S11/BR06 | — | — | — |
| FN-12 | แยก boundary Stocktake รอบใหญ่จาก Cycle Count ABC | S05/BR01 | — | — | — |

## สิ่งที่ไม่รองรับ

- ไม่เป็น Pattern Q หรือเอกสารเลขรัน/PDF — [แผน]
- ไม่ปรับ inventory on-hand โดยตรง; Stock Adjustment W3-LITE เป็น mock [ASSUMED contract]
- ไม่สร้าง Cycle Count ABC W4-FULL หรือ master Warehouse/Item — [แผน]
