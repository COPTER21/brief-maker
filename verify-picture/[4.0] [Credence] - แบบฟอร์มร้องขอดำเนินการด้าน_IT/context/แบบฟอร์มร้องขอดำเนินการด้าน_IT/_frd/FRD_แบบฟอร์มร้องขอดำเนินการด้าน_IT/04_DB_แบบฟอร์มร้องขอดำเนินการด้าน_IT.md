# 04_DB — F-TMP-001

## §4.1 it_request
| column | type | null | ที่มา / หมายเหตุ | Data class |
|---|---|:-:|---|---|
| id | uuid PK | N | | Internal |
| company_id | uuid FK | N | tenant | Internal |
| doc_no | varchar(30) UNIQUE(company_id) | Y→N หลังบันทึกครั้งแรก | ENG-DOC-NUM (ITRS) · ป้าย "ITRS." | Internal |
| req_date | date | N | auto · ป้าย "วันที่" | Internal |
| employee_id | uuid FK → Employee | N | ผู้ร้องขอ | Internal |
| name_snapshot | varchar(200) | N | ชื่อ-นามสกุล ณ วันที่ขอ | **Confidential (PII)** |
| position_snapshot | varchar(200) | N | ตำแหน่ง | Internal |
| due_date | date | N | วันที่ต้องการส่งมอบ | Internal |
| delivery_location | varchar(200) | N | สถานที่ส่งมอบ | Internal |
| subject | varchar(200) | N | เรื่องที่ต้องการ | Internal |
| job_types | text[] (enum: buy_device, user_email, install_software, install_accessory, internet_wifi, other) | N | ประเภทงาน ≥1 | Internal |
| job_type_other | varchar(200) | Y | อื่นๆ (บังคับเมื่อมี other) | Internal |
| detail | text | N | รายละเอียดการร้องขอ | Internal |
| reason | text | N | เหตุผล วัตถุประสงค์ หรือ ความจำเป็น | Internal |
| spec | text | Y | มาตรฐาน หรือ Spec ที่ต้องการ | Internal |
| status | enum(draft, pending, approved, done, cancelled) | N | | Internal |
| doa_ref | varchar(40) | Y | DOA entry ที่ resolve | Internal |
| approval_chain | jsonb | Y | snapshot ตอนส่ง `[{step, role_id, label, assignee, status, at, note}]` | Internal |
| approved_by · approved_at | uuid · timestamptz | Y | ขั้นสุดท้าย | Internal |
| returned_reason · returned_by · returned_at | text · uuid · timestamptz | Y | DEC-08 | Internal |
| performed_by · performed_at · done_note | uuid · timestamptz · text | Y | ช่อง "ดำเนินการโดย" (role-it-officer) | Internal |
| cancel_reason · cancelled_by · cancelled_at | text · uuid · timestamptz | Y | | Internal |
| header_snapshot | jsonb | Y | Organization ชื่อ/โลโก้ ณ ออกเลข (print_config.header_source) | Internal |
| submitted_at | timestamptz | Y | | Internal |
| created_by/at · updated_by/at · version | | N | optimistic lock (409 STALE) | Internal |

## §4.2 it_request_audit (append-only)
id · request_id FK · action · actor_id · at · note — ห้าม UPDATE/DELETE

## §4.3 attachments
Document Center (owner_type='it_request', owner_id) — file_policy กลาง

## §4.4 Index
(company_id, status) · (employee_id) · (company_id, req_date desc) · GIN(approval_chain)
