# 04_DB — F-TMP-002

## §4.1 Table Overview
| Table | ใช้ |
|---|---|
| `server_room_check` | header (1 ใบ = 1 รอบการตรวจ) |
| `server_room_check_row` | ผลตรวจรายวัน (แถวซ้ำ) |
| `server_room_check_audit` | ประวัติ append-only |
| (Document Center) `attachment` | ไฟล์แนบ (ref_type='SRC') |

> ไม่มี field ของ DOA (DEC-03 — กระดาษไม่มีช่องผู้พิจารณา) · ถ้าลูกค้ายืนยันให้มีผู้ตรวจทาน (OQ-02) = enhancement: เพิ่ม field สายพิจารณา + DOA_BRIEF ตาม doa-declaration
| (config ใหม่ OQ-04) `server_room_check_config` | temp_min_c · temp_max_c · rh_min · rh_max ต่อ tenant |

## §4.2 Per-Table
### server_room_check
| column | type | null | หมายเหตุ | Class |
|---|---|---|---|---|
| id | uuid PK | N | | Internal |
| tenant_id | uuid | N | RLS | Internal |
| doc_no | varchar(30) unique/tenant | N | เลขที่ (ENG-DOC-NUM · SRC) | Internal |
| doc_date | date | N | วันที่สร้าง | Internal |
| status | enum(draft,submitted,cancelled) | N | ไม่มีขั้นพิจารณา (DEC-03) | Internal |
| owner_id | uuid | N | soft-ref F-EMP-001 | Internal |
| owner_name_snapshot | varchar(200) | N | ผู้บันทึก (PII) | Confidential·PII |
| dept_snapshot | varchar(200) | Y | ฝ่าย | Internal |
| criteria_snapshot | jsonb | N | {temp_min_c,temp_max_c,rh_min,rh_max} ณ ออกเลข (DEC-04) | Internal |
| header_snapshot | jsonb | Y | Organization (ชื่อ · โลโก้) ณ ออกเลข | Internal |
| submitted_at / closed_at | timestamptz | Y | ส่งปิดรอบ | Internal |
| cancel_reason | text | Y | | Internal |
| version | int | N | optimistic lock | Internal |
| created_by/at · updated_by/at | | N | | Internal |
### server_room_check_row
| column | type | หมายเหตุ (ป้ายกระดาษ) |
|---|---|---|
| id · check_id FK | | |
| check_date | date N | วันที่ |
| access_log | enum(yes,no) N | ทะเบียนคุมเข้าออก |
| extinguisher_pressure | varchar(30) N | ถังดับเพลิง (ความดัน) |
| temperature_c | numeric(4,1) N | อุณหภูมิ |
| humidity_rh | numeric(4,1) N | ความชื้นสัมพัทธ์ |
| aircon · cctv · mdb · pdu | enum(normal,abnormal) N | เครื่องปรับอากาศ · กล้องวงจรปิด · MDB · PDU |
| remark | varchar(500) Y | หมายเหตุ |
| checked_by | uuid N | ผู้ตรวจสอบ (ผู้บันทึกแถว) |
| checked_by_name_snapshot | varchar(200) N | (PII) |
| checked_at | timestamptz N | |
| issues | jsonb | คำนวณ (FN-02) |
### server_room_check_audit
id · check_id · action · actor_id · note · at (append-only · ไม่มี update/delete)

## §4.3 ER
server_room_check 1—N server_room_check_row · 1—N server_room_check_audit · 1—N attachment(ref)

## §4.5 Field Dictionary (FE)
`check_date` · `access_log` · `extinguisher_pressure` · `temperature_c` · `humidity_rh` · `aircon` · `cctv` · `mdb` · `pdu` · `remark` · `checked_by`

## §4.6 Data Classification
Default Internal · PII overlay: owner_name_snapshot · checked_by_name_snapshot · ข้อมูลตัวอย่าง prototype = ชื่อสมมติ

## §4.7 Retention
ตามนโยบายบันทึกการปฏิบัติงาน IT (ยืนยันกับ Policy Center) · ไม่ hard delete
