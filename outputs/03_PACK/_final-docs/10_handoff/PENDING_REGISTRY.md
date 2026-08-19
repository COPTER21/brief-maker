# Pending Registry — F-WH-PACK

| ID | ประเด็น | ผลกระทบ | เจ้าของคำตอบ | สถานะ |
|---|---|---|---|---|
| PACK-OQ-01 | น้ำหนักสินค้าต่อหน่วยและแหล่งข้อมูลมาตรฐาน | การคำนวณน้ำหนักประมาณการ | BA / Warehouse master owner | Open |
| PACK-OQ-02 | รายการชนิดกล่อง น้ำหนักเปล่า และความจุที่อนุมัติ | การแนะนำกล่องและเอกสารพิมพ์ | BA / Warehouse master owner | Open |
| PACK-OQ-DN-01 | contract จริงของ Delivery Note ยังไม่มี artifact ให้อ้างอิง | ห้ามเปิดการสร้างใบส่งของจริง | Delivery Note owner | Guarded Open |
| PACK-OQ-XT-01 | contract ของ Transfer → Packing ยังไม่ยืนยัน | ไม่รับ Transfer เป็นงานจริงในรอบนี้ | Transfer/Picking owner | Guarded Open |
| PACK-UX-01 | UX checker พบข้อไม่ผ่านหลายรายการ แต่ HTML ถูก waive ให้ใช้ตามสภาพ | เป็นหนี้ด้านรูปแบบ ห้ามยกเป็นมาตรฐานหน้าจอใหม่ | PM/BA / UI owner | Waived, unresolved |
| PACK-TOOL-01 | ไม่พบ shared `ui-brief-check.py` ที่ skill กำหนด | UI Brief ตรวจด้วยหลักฐานในเอกสาร แต่ยังไม่มีผลจาก verifier กลาง | Workspace tooling owner | Open |

รายละเอียด UX ใช้ `_UX_CHECK_REPORT.md` เป็นหลัก การ waive หมายถึงอนุญาตให้เดินงานต่อ ไม่ใช่ผล PASS

