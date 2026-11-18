# 04_DB — F-TMP-004

## §4.1 Table Overview
| Table | ใช้ |
|---|---|
| `sale_admin_eval_dom` | header (1 ใบ = 1 ลูกค้า 1 ครั้งที่ตอบ) |
| `sale_admin_eval_dom_score` | ระดับรายข้อ (5 แถวต่อใบเมื่อครบ) |
| `sale_admin_eval_dom_audit` | ประวัติ append-only |
| (Document Center) `attachment` | ไฟล์แนบ (ref_type='SDA') |

## §4.2 Per-Table
### sale_admin_eval_dom
| column | type | null | หมายเหตุ / ช่องบนกระดาษ | Class |
|---|---|---|---|---|
| id | uuid PK | N | | Internal |
| tenant_id | uuid | N | RLS | Internal |
| doc_no | varchar(30) unique/tenant | N | เลขที่ (ENG-DOC-NUM · footer แบบพิมพ์) | Internal |
| status | enum(draft,recorded,cancelled) | N | | Internal |
| period_month | char(7) YYYY-MM | N | ประจำเดือน | Internal |
| customer_id | uuid | N | soft-ref Customer master (`customerId`) | Internal |
| customer_name_snapshot | varchar(255) | N | ชื่อลูกค้า (snapshot ตอนบันทึก) | Internal |
| survey_date | date | N | วันที่ | Internal |
| comment | text | Y | ข้อเสนอแนะเพิ่มเติม | Internal |
| recorder_id | uuid | N | ผู้บันทึก (Employee) | Internal |
| recorded_at | timestamptz | Y | เวลาบันทึกผล | Internal |
| header_snapshot | jsonb | Y | Organization (ชื่อ · โลโก้) ณ ออกเลข | Internal |
| form_code / form_revision | varchar | N | FM-SAL-20 · Rev.00 : 01/07/2569 (จาก print_config ณ ออกเลข) | Internal |
| cancelled_by / cancelled_at / cancel_reason | uuid / timestamptz / text | Y | ยกเลิก (เหตุผลบังคับ) | Internal |
| version | int | N | optimistic lock | Internal |
| created_by / created_at / updated_by / updated_at | | N | | Internal |

### sale_admin_eval_dom_score
| column | type | null | หมายเหตุ |
|---|---|---|---|
| eval_id | uuid FK | N | |
| q_key | varchar(4) | N | q1 q2 q3 q4 q5 (ถ้อยคำรายละเอียด = FORM_SPEC / แบบพิมพ์ Rev.00) |
| score | smallint CHECK 1..5 | N | 5=มากที่สุด · 4=มาก · 3=ปานกลาง · 2=น้อย · 1=ควรปรับปรุง |
PK (eval_id, q_key)

### sale_admin_eval_dom_audit
| column | type | หมายเหตุ |
|---|---|---|
| id · eval_id · action · actor_id · at · note | | append-only · ห้าม UPDATE/DELETE |

## §4.3 Index / Constraint
- (tenant_id, doc_no) unique · (tenant_id, period_month, status) · (tenant_id, customer_id, period_month) · (tenant_id, recorder_id, status)
- ไม่มีคอลัมน์สายพิจารณาในตารางนี้ (DEC-03 — ไม่มีขั้นพิจารณา) · field ของ DOA engine ให้ดู 02 §2.2 / 03 FN-03 (`TODO: DOA engine`)
