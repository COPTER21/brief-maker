# 04_DB — F-TMP-001

## §4.1 Table Overview
| Table | ใช้ |
|---|---|
| `customer_survey_gt` | header (1 ใบ = 1 ลูกค้า 1 ครั้งที่ตอบ) |
| `customer_survey_gt_score` | คะแนนรายหัวข้อ (16 แถวต่อใบเมื่อครบ) |
| `customer_survey_gt_audit` | ประวัติ append-only |
| (Document Center) `attachment` | ไฟล์แนบ (ref_type='CSG') |

## §4.2 Per-Table
### customer_survey_gt
| column | type | null | หมายเหตุ / ช่องบนกระดาษ | Class |
|---|---|---|---|---|
| id | uuid PK | N | | Internal |
| tenant_id | uuid | N | RLS | Internal |
| doc_no | varchar(30) unique/tenant | N | เลขที่ (ENG-DOC-NUM · footer แบบพิมพ์) | Internal |
| status | enum(draft,recorded,cancelled) | N | | Internal |
| period_month | char(7) YYYY-MM | N | ประจำเดือน | Internal |
| survey_date | date | N | วันที่ : | Internal |
| customer_id | uuid | N | soft-ref Customer master (`customerId`) | Internal |
| customer_name_snapshot | varchar(255) | N | ชื่อบริษัท : (snapshot ตอนบันทึก) | Internal |
| contact_dept | varchar(200) | Y | ฝ่าย/แผนก : | Internal |
| contact_phone | varchar(30) | Y | เบอร์โทร.ติดต่อ : | Confidential·PII |
| comment_staff | text | Y | ข้อเสนอแนะด้านเจ้าหน้าที่ผู้ให้บริการ/พนักงานขาย: | Internal |
| comment_other | text | Y | ข้อเสนอแนะอื่นๆ เพื่อการปรับปรุงให้ดียิ่งขึ้น | Internal |
| recorder_id | uuid | N | ผู้บันทึก (Employee) | Internal |
| recorded_at | timestamptz | Y | เวลาบันทึกผล | Internal |
| header_snapshot | jsonb | Y | Organization (ชื่อ · โลโก้) ณ ออกเลข | Internal |
| form_code / form_revision | varchar | N | FM-SAL-10 · Rev.00: 01/07/2569 (จาก print_config ณ ออกเลข) | Internal |
| cancelled_by / cancelled_at / cancel_reason | uuid / timestamptz / text | Y | ยกเลิก (เหตุผลบังคับ) | Internal |
| version | int | N | optimistic lock | Internal |
| created_by / created_at / updated_by / updated_at | | N | | Internal |

### customer_survey_gt_score
| column | type | null | หมายเหตุ |
|---|---|---|---|
| survey_id | uuid FK | N | |
| q_key | varchar(8) | N | q1_1 q1_2 q1_3 q1_4 · q2_1 q2_2 q2_3 q2_4 · q3_1 q3_2 q3_3 q3_4 q3_5 q3_6 q3_7 q3_8 (ถ้อยคำหัวข้อ = FORM_SPEC / แบบพิมพ์ Rev.00) |
| score | smallint CHECK 1..5 | N | ค่าที่เลือก 5 4 3 2 1 |
PK (survey_id, q_key)

### customer_survey_gt_audit
| column | type | หมายเหตุ |
|---|---|---|
| id · survey_id · action · actor_id · at · note | | append-only · ห้าม UPDATE/DELETE |

## §4.3 Index / Constraint
- (tenant_id, doc_no) unique · (tenant_id, period_month, status) · (tenant_id, customer_id, period_month) · (tenant_id, recorder_id, status)
- ไม่มีคอลัมน์สายพิจารณา (DEC-03 — ไม่มี DOA)
