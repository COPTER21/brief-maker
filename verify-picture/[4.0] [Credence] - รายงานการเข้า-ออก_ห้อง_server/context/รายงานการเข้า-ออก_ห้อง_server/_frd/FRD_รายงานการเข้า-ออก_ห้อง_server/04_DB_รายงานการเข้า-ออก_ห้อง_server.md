# 04_DB — F-TMP-006

## §4.1 Table Overview
| Table | ใช้ |
|---|---|
| `server_room_access` | header (1 ใบ = 1 รอบ) |
| `server_room_access_entry` | การเข้า-ออกแต่ละครั้ง (แถวซ้ำ) |
| `server_room_access_audit` | ประวัติ append-only |
| (Document Center) `attachment` | ไฟล์แนบ (ref_type='SRAL') |
| (config ใหม่ OQ-04) `server_room_access_config` | max_stay_hours ต่อ tenant (ค่าเริ่ม 12) |

> ไม่มี field ของ DOA (DEC-03 — กระดาษไม่มีช่องผู้พิจารณาท้ายใบ) · ถ้าลูกค้ายืนยันให้มีขั้นพิจารณาก่อนเข้าห้อง (OQ-02) = enhancement: เพิ่ม field สายพิจารณา + DOA_BRIEF ตาม doa-declaration · ลายเซ็นผู้รับรอง = field ระดับแถว (certified_by) ไม่ใช่ขั้น DOA

## §4.2 Per-Table
### server_room_access
| column | type | null | หมายเหตุ | Class |
|---|---|---|---|---|
| id | uuid PK | N | | Internal |
| tenant_id | uuid | N | RLS | Internal |
| doc_no | varchar(30) unique/tenant | N | เลขที่ (ENG-DOC-NUM · SRAL) | Internal |
| doc_date | date | N | วันที่สร้าง | Internal |
| status | enum(draft,submitted,cancelled) | N | ไม่มีขั้นพิจารณา (DEC-03) | Internal |
| owner_id | uuid | N | soft-ref F-EMP-001 | Internal |
| owner_name_snapshot | varchar(200) | N | ผู้บันทึก (PII) | Confidential·PII |
| dept_snapshot | varchar(200) | Y | ฝ่าย | Internal |
| header_snapshot | jsonb | Y | Organization (ชื่อ · โลโก้) ณ ออกเลข | Internal |
| submitted_at / closed_at | timestamptz | Y | ส่งปิดรอบ | Internal |
| cancel_reason | text | Y | | Internal |
| version | int | N | optimistic lock | Internal |
| created_by/at · updated_by/at | | N | | Internal |
### server_room_access_entry
| column | type | หมายเหตุ (ป้ายกระดาษ) |
|---|---|---|
| id · access_id FK | | |
| visitor_emp_id | uuid Y | soft-ref F-EMP-001 (null = บุคคลภายนอก) |
| visitor_name | varchar(120) N | ชื่อ–นามสกุล (PII) |
| visitor_department | varchar(120) N | ฝ่าย/แผนก |
| in_date · in_time | date N · time N | วันที่เข้า · เวลาที่เข้า |
| out_date · out_time | date Y · time Y | วันที่ออก · เวลาที่ออก (null = ยังอยู่ในห้อง) |
| purpose | varchar(300) N | เหตุผลการเข้าใช้ |
| visitor_signed_by · visitor_signed_at | uuid N · timestamptz N | ลายเซ็นผู้เข้า (ลงชื่อในระบบ) |
| certified_by · certified_by_name_snapshot · certified_at | uuid Y · varchar(200) Y · timestamptz Y | ลายเซ็นผู้รับรอง (PII) |
| issues | jsonb | คำนวณ (FN-02) |
| overstay_notified_at | timestamptz Y | กันแจ้งซ้ำ |
### server_room_access_audit
id · access_id · entry_id? · action · actor_id · note · at (append-only · ไม่มี update/delete)

## §4.3 ER
server_room_access 1—N server_room_access_entry · 1—N server_room_access_audit · 1—N attachment(ref)

## §4.5 Field Dictionary (FE)
`visitor_name` · `visitor_department` · `in_date` · `in_time` · `out_date` · `out_time` · `purpose` · `visitor_signed` · `certified_by`

## §4.6 Data Classification
Default Internal · PII overlay: owner_name_snapshot · visitor_name · certified_by_name_snapshot · ข้อมูลตัวอย่าง prototype = ชื่อสมมติ

## §4.7 Retention
ตามนโยบายบันทึกความปลอดภัย IT (ยืนยันกับ Policy Center) · ไม่ hard delete
