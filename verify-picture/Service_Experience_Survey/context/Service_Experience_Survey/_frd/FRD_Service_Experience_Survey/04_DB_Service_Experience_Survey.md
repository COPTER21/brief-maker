# 04_DB — F-TMP-006

## §4.1 Table Overview
| Table | ใช้ |
|---|---|
| `sales_admin_eval_ovs` | header (1 ใบ = 1 ลูกค้าต่างประเทศ 1 ครั้งที่ตอบ) |
| `sales_admin_eval_ovs_score` | คะแนนรายข้อ (10 แถวต่อใบเมื่อครบ) |
| `sales_admin_eval_ovs_audit` | ประวัติ append-only |
| (Document Center) `attachment` | ไฟล์แนบ (ref_type='SEA') |

## §4.2 Per-Table
### sales_admin_eval_ovs
| column | type | null | หมายเหตุ / ช่องบนกระดาษ | Class |
|---|---|---|---|---|
| id | uuid PK | N | | Internal |
| tenant_id | uuid | N | RLS | Internal |
| doc_no | varchar(30) unique/tenant | N | เลขที่ (ENG-DOC-NUM · footer แบบพิมพ์) | Internal |
| status | enum(draft,recorded,cancelled) | N | | Internal |
| period_month | char(7) YYYY-MM | N | Month | Internal |
| customer_id | uuid | N | soft-ref Customer master (`customerId`) | Internal |
| customer_name_snapshot | varchar(255) | N | Company Name (snapshot ตอนบันทึก) | Internal |
| contact_person | varchar(120) | N | Contact Person — ข้อมูลส่วนบุคคล | Confidential (PDPA) |
| comment | text | Y | Additional Feedback | Internal |
| recorder_id | uuid | N | ผู้บันทึก (Employee) | Internal |
| recorded_at | timestamptz | Y | เวลาบันทึกผล | Internal |
| header_snapshot | jsonb | Y | Organization (ชื่ออังกฤษ · โลโก้) ณ ออกเลข | Internal |
| form_code / form_revision | varchar | N | FM-SAL-22 · Rev.00 : 01/07/2569 (จาก print_config ณ ออกเลข) | Internal |
| cancelled_by / cancelled_at / cancel_reason | uuid / timestamptz / text | Y | ยกเลิก (เหตุผลบังคับ) | Internal |
| version | int | N | optimistic lock | Internal |
| created_by / created_at / updated_by / updated_at | | N | created_at = วันที่บันทึก (กระดาษไม่มีช่องวันที่) | Internal |

### sales_admin_eval_ovs_score
| column | type | null | หมายเหตุ |
|---|---|---|---|
| eval_id | uuid FK | N | |
| q_key | varchar(4) | N | q1…q10 (กลุ่ม: q1–q3 Communication & Responsiveness · q4–q8 Documentation & Execution · q9–q10 Professionalism · ถ้อยคำ = FORM_SPEC / แบบพิมพ์ Rev.00) |
| score | smallint CHECK 1..5 | N | 1 = Very Dissatisfied … 5 = Very Satisfied |
PK (eval_id, q_key)

### sales_admin_eval_ovs_audit
| column | type | หมายเหตุ |
|---|---|---|
| id · eval_id · action · actor_id · at · note | | append-only · ห้าม UPDATE/DELETE |

## §4.3 Index / Constraint
- (tenant_id, doc_no) unique · (tenant_id, period_month, status) · (tenant_id, customer_id, period_month) · (tenant_id, recorder_id, status)
- ไม่มีคอลัมน์สายพิจารณาในตารางนี้ (DEC-03 — ไม่มีขั้นพิจารณา) · field ของ DOA engine ให้ดู 02 §2.2 / 03 FN-03 (`TODO: DOA engine`)
- PDPA: contact_person เก็บตามอายุเอกสาร · ลบ/ปิดบังตามนโยบาย PDPA ขององค์กร
