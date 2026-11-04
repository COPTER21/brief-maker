# 02_API — F-TMP-003 คำขอมีและใช้ลายเซ็นดิจิทัล (DSR)

ฐาน: `/api/hr/digital-signature-request`

## 1. รายการ
`GET /api/hr/digital-signature-request?q=&status=&case_kind=&department=&page=&size=`
กรองตามสิทธิ์ (DEC-09) ที่ชั้น service เสมอ — เจ้าของ · ผู้พิจารณาหลังส่ง · admin role เห็นทั้งหมด
```json
{ "total": 12, "items": [{ "id":"...", "doc_no":"DSR-2569-0007", "doc_date":"2026-10-01",
  "requester":{ "emp_id":"E01", "name_th":"…", "department":"…" },
  "case_kind":"change", "change_type":"both", "status":"approved", "signed":"1/1" }] }
```

## 2. อ่านใบเดียว
`GET /api/hr/digital-signature-request/{id}` → ทุกช่องตาม 04_DB + `approval_chain` + `audit[]` + `attachments[]`
ไม่มีสิทธิ์ → `403 NOT_ALLOWED` · ไม่พบ → `404 NOT_FOUND`

## 3. สร้าง / แก้ร่าง
`POST /api/hr/digital-signature-request` · `PUT /api/hr/digital-signature-request/{id}`
```json
{ "made_at":"สำนักงานใหญ่ กรุงเทพมหานคร", "case_kind":"change", "renew_reason":null, "change_type":"both",
  "old_first_name_th":"สมชาย", "old_last_name_th":"ใจดี",
  "new_first_name_th":"ชยพล", "new_last_name_th":"ใจดีมาก",
  "new_first_name_en":"Chayapon", "new_last_name_en":"Jaideemak",
  "certified": true, "attachments":[{ "file_id":"…" }] }
```
- แก้ได้เฉพาะ `status = draft` และผู้เรียกเป็นเจ้าของ (ไม่งั้น `403 NOT_OWNER`)
- POST ครั้งแรก = ออกเลขที่จาก **ENG-DOC-NUM** (DEC-10) · ก่อนออกเลขเช็ค doc_type เปิดใช้ที่ **F-DOCCFG** ไม่เปิด → `409 DOCTYPE_INACTIVE`
- ช่องผู้ขอ (ชื่อ/ตำแหน่ง/หน่วยงาน/อีเมล/โทร) ไม่รับจาก payload — service snapshot จากทะเบียนพนักงาน (F-EMP-001)

## 4. ส่งอนุมัติ / พิจารณา / ยกเลิก
| Endpoint | ทำอะไร |
|---|---|
| `POST /{id}/submit` body `{ "approvers":["E08"] }` | resolve DOA แล้ว freeze ลง `approval_chain` (BR-DOA-02) · `draft → pending` · กรณี `case_kind = change` ยิง `dsr_name_change_requested` ผ่าน ENG-NOTIFY |
| `POST /{id}/approve` body `{ "note":"" }` | ขั้นปัจจุบันผ่าน → ขั้นถัดไป หรือ `approved` ("ดำเนินการได้") |
| `POST /{id}/reject` body `{ "reason":"…" }` | บันทึกผล "ไม่สามารถดำเนินการได้" → เอกสาร **กลับเป็นร่างเลขเดิม** (DEC-08) |
| `POST /{id}/cancel` body `{ "reason":"…" }` | เจ้าของหรือ admin role · สถานะ `draft`/`pending` · ยิง `dsr_cancelled` ผ่าน ENG-NOTIFY |

ไม่ใช่ผู้พิจารณาขั้นปัจจุบัน → `403 NOT_CURRENT_APPROVER` · ผู้ขออนุมัติใบตัวเอง → `403 SELF_APPROVE` (BR-DOA-04)

## 5. แบบพิมพ์ / ส่งออก
| Endpoint | ทำอะไร |
|---|---|
| `GET /{id}/pdf` | render จาก `print/form.tpl.html` + data contract ฝั่ง server · สำเนาเก็บผ่าน **ENG-DOC-STORE** เมื่อ `approved_final` |
| `GET /export.csv?...` | ส่งออกตามตัวกรองเดิม (DEC-11) |

**DEC-02** — รอบนี้ไม่มี endpoint ส่งต่อระบบอื่น · ไม่เรียก API ของ F-EMP-001 เพื่อแก้ชื่อ-นามสกุล (แจ้งเตือนอย่างเดียว)
