# 04_DB — F-TMP-005

## §4.1 change_request
| column | type | null | ที่มา / หมายเหตุ | Data class |
|---|---|:-:|---|---|
| id | uuid PK | N | | Internal |
| company_id | uuid FK | N | tenant | Internal |
| doc_no | varchar(30) UNIQUE(company_id) | Y→N หลังบันทึกครั้งแรก | ENG-DOC-NUM (ITCR) · กระดาษไม่มีช่อง (DEC-17) | Internal |
| request_date | date | N | auto · ป้าย "วันที่" | Internal |
| employee_id | uuid FK → Employee | N | ผู้ขอ | Internal |
| name_snapshot | varchar(200) | N | ชื่อ-นามสกุล ณ วันที่ขอ | **Confidential (PII)** |
| position_snapshot | varchar(200) | N | ตำแหน่ง | Internal |
| due_date | date | N | วันที่ต้องการส่งมอบ | Internal |
| delivery_location | varchar(200) | N | สถานที่ส่งมอบ | Internal |
| subject | varchar(200) | N | เรื่องที่ต้องการ | Internal |
| change_types | text[] (enum: software, hardware, network, security, other) | N | ประเภทของการเปลี่ยนแปลง ≥1 | Internal |
| change_type_other | varchar(200) | Y | อื่นๆ — บังคับเมื่อมี other | Internal |
| change_detail | text | N | รายละเอียดของการเปลี่ยนแปลง | Internal |
| objective | text | N | วัตถุประสงค์ของการเปลี่ยนแปลง | Internal |
| impact | text | N | ระบบที่ได้รับผลกระทบและ ผลกระทบที่อาจเกิดขึ้น | Internal |
| action_plan | text | N | แผนการดำเนินการ | Internal |
| status | enum(draft, pending, approved, cancelled) | N | | Internal |
| doa_ref | varchar(40) | Y | DOA entry ที่ resolve | Internal |
| approval_chain | jsonb | Y | snapshot ตอนส่ง `[{step, role_id, label, assignee, status, at, note}]` | Internal |
| approver_role · approved_by · approved_at | varchar(40) · uuid · timestamptz | Y | ขั้นสุดท้าย — `TODO: DOA engine` เติมจาก callback | Internal |
| returned_reason · returned_by · returned_at | text · uuid · timestamptz | Y | DEC-08 | Internal |
| cancel_reason · cancelled_by · cancelled_at | text · uuid · timestamptz | Y | | Internal |
| header_snapshot | jsonb | Y | Organization ชื่อ/โลโก้ ณ ออกเลข (print_config.header_source) | Internal |
| submitted_at | timestamptz | Y | | Internal |
| created_by/at · updated_by/at · version | | N | optimistic lock (409 STALE) | Internal |

## §4.2 change_request_audit (append-only)
id · request_id FK · action · actor_id · at · note — ห้าม UPDATE/DELETE

## §4.3 attachments
Document Center (owner_type='change_request', owner_id) — file_policy กลาง · ห้ามแนบไฟล์ที่มีรหัสผ่าน/คีย์

## §4.4 Index
(company_id, status) · (employee_id) · (company_id, request_date desc) · GIN(change_types) · GIN(approval_chain)
