# 02_API — F-TMP-002 บันทึกภายใน

> HTTP layer บาง — ตรรกะอยู่ที่ 03_LOGIC · ทุก endpoint ตรวจสิทธิ์ตาม DEC-09 ก่อนเสมอ

| # | Method · Path | ใช้ทำอะไร | เรียก Function |
|---|---|---|---|
| API-01 | `GET /api/memo` | รายการบันทึกที่ผู้ใช้ปัจจุบันเห็นได้ (query: `q` `status` `dept` `page`) | MEM-FN-07 |
| API-02 | `GET /api/memo/{id}` | รายละเอียด 1 ฉบับ | MEM-FN-07 |
| API-03 | `POST /api/memo` | สร้าง/บันทึกร่างครั้งแรก → ออกเลขที่ | MEM-FN-01 |
| API-04 | `PUT /api/memo/{id}` | แก้ร่างของตัวเอง | MEM-FN-02 |
| API-05 | `POST /api/memo/{id}/submit` | ส่งอนุมัติ (body: `assignees[]` ต่อขั้น) | MEM-FN-03 |
| API-06 | `POST /api/memo/{id}/approve` | อนุมัติขั้นปัจจุบัน (body: `legal_opinion`) | MEM-FN-04 |
| API-07 | `POST /api/memo/{id}/reject` | ไม่อนุมัติ (body: `legal_opinion` **บังคับ**) | MEM-FN-05 |
| API-08 | `POST /api/memo/{id}/cancel` | ยกเลิกเอกสาร (body: `reason` **บังคับ**) → ยิง event `mem_cancelled` | MEM-FN-06 |
| API-09 | `POST /api/memo/{id}/reopen` | ใบที่ถูกตีกลับ → กลับเป็นร่างด้วยเลขที่เดิม (DEC-08) | MEM-FN-08 |
| API-10 | `GET /api/memo/{id}/pdf` | แบบพิมพ์ A4 (server render template เดียวกับ prototype) | MEM-FN-09 |
| API-11 | `GET /api/memo/export.csv` | ส่งออกรายการตามตัวกรองปัจจุบัน (DEC-11) | MEM-FN-07 |
| API-12 | `POST /api/memo/{id}/attachments` | แนบไฟล์ผ่าน Document Center | MEM-FN-10 |

## §2.1 รหัสผลลัพธ์ที่ใช้ร่วม
| HTTP | code | เมื่อไหร่ |
|---|---|---|
| 400 | `VALIDATION_FAILED` | เรียน/เรื่อง/เนื้อหา ว่าง · เหตุผลว่างตอน reject/cancel |
| 403 | `NOT_OWNER` | แก้/ส่ง ใบที่ไม่ใช่ของตัวเอง |
| 403 | `NOT_CURRENT_APPROVER` | อนุมัติ/ไม่อนุมัติ ทั้งที่ไม่ใช่ผู้พิจารณาขั้นปัจจุบัน |
| 403 | `SELF_APPROVAL_DENIED` | ผู้จัดทำพิจารณาใบตัวเอง (BR-DOA-04) |
| 404 | `NOT_FOUND` | เปิดใบที่ตนไม่มีสิทธิ์เห็น (ไม่บอกว่ามีอยู่ — DEC-09) |
| 409 | `STALE_STATE` | สถานะเปลี่ยนไปแล้วระหว่างเปิดหน้าจอ |
| 423 | `DOCTYPE_INACTIVE` | แบบเอกสารยังไม่เปิดใช้งานที่ F-DOCCFG |
