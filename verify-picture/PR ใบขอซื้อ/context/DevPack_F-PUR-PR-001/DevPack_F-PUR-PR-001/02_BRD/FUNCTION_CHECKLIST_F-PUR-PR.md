# FUNCTION_CHECKLIST — F-PUR-PR · PR ใบขอซื้อ
ติ๊ก 3 ด่าน: WF (Phase A) · DEV · QA — Phase A ติ๊กเฉพาะ WF

| FN | ฟังก์ชัน | จอ | Scenario | WF | DEV | QA |
|---|---|---|---|:--:|:--:|:--:|
| FN-01 | List PR + คอลัมน์ครบ (lean ไม่ซ้อน) | List | SC-15 | ☐ | ☐ | ☐ |
| FN-02 | ค้นหา + filter สถานะ/วันที่/หน่วยงาน/ผู้ขอ | List | SC-15 | ☐ | ☐ | ☐ |
| FN-03 | แถบเอกสารแนบใน landing | List | SC-11 | ☐ | ☐ | ☐ |
| FN-04 | empty / loading / error state | List | SC-15 | ☐ | ☐ | ☐ |
| FN-05 | เปิด wizard สร้างใบใหม่ (5 steps) | Wizard | SC-01 | ☐ | ☐ | ☐ |
| FN-06 | Step1 header ครบ + validate วันที่ต้องการใช้ | Wizard | SC-14 | ☐ | ☐ | ☐ |
| FN-07 | Cost center picker (soft-ref nullable) | Wizard | SC-03 | ☐ | ☐ | ☐ |
| FN-08 | Step2 B2 v2 line editor grid compact | Wizard | SC-01 | ☐ | ☐ | ☐ |
| FN-09 | Item combobox anatomy #102 + free-text | Wizard | SC-03 | ☐ | ☐ | ☐ |
| FN-10 | ส่วนลดรายบรรทัด (บาท/%) | Wizard | SC-01 | ☐ | ☐ | ☐ |
| FN-11 | VAT segmented (7% / ไม่มี / 0%) | Wizard | SC-01 | ☐ | ☐ | ☐ |
| FN-12 | Totals: รวม/ส่วนลด/ฐานภาษี/VAT/สุทธิ | Wizard | SC-01 | ☐ | ☐ | ☐ |
| FN-13 | เพิ่ม/ลบ/เรียงบรรทัด + กันบรรทัดว่าง | Wizard | SC-13 | ☐ | ☐ | ☐ |
| FN-14 | Step3 ผู้ขายแนะนำ (soft-ref · ไม่บังคับ) | Wizard | SC-01 | ☐ | ☐ | ☐ |
| FN-15 | Step4 แนบไฟล์ + validate ชนิด/ขนาด | Wizard | SC-11 | ☐ | ☐ | ☐ |
| FN-16 | Step5 สรุป read-only | Wizard | SC-01 | ☐ | ☐ | ☐ |
| FN-17 | แถบตรวจงบ **mock + TODO** ไม่ block | Wizard | SC-07 | ☐ | ☐ | ☐ |
| FN-18 | **DOA slot picker คนจริง** (avatar+ตำแหน่ง+ชื่อ) | Wizard | SC-06 | ☐ | ☐ | ☐ |
| FN-19 | บันทึกร่าง / ส่งอนุมัติ | Wizard | SC-02 | ☐ | ☐ | ☐ |
| FN-20 | View tab รายละเอียด + ปุ่มตามสถานะ | View | SC-08,SC-10 | ☐ | ☐ | ☐ |
| FN-21 | View tab PDF (A4 ตาม print spec) | View | SC-01 | ☐ | ☐ | ☐ |
| FN-22 | View tab ลายเซ็น (การ์ดต่อ slot) | View | SC-01,SC-04 | ☐ | ☐ | ☐ |
| FN-23 | View tab ประวัติ append-only | View | SC-05,SC-09 | ☐ | ☐ | ☐ |
| FN-24 | อนุมัติ / ไม่อนุมัติ(+เหตุผล) / เรียกคืน / ยกเลิก(+confirm) / คัดลอกใบ | View+List | SC-04,05,09,12 | ☐ | ☐ | ☐ |
