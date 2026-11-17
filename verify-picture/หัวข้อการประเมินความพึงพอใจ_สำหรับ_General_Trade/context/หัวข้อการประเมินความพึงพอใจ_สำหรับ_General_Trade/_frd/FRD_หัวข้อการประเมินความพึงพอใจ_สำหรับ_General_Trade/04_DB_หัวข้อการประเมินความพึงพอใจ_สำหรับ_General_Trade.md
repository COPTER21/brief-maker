# 04_DB — F-TMP-002

## §4.1 Table Overview
| Table | ใช้ |
|---|---|
| `csat_summary` | header |
| `csat_summary_line` | คะแนนต่อหัวข้อ (16 แถวตาม config) |
| `csat_summary_customer` | รายชื่อลูกค้าที่ประเมิน |
| `csat_summary_audit` | ประวัติ append-only |
| (Document Center) `attachment` | ไฟล์แนบ (ref_type='CSM') |

## §4.2 Per-Table
### csat_summary
| column | type | null | หมายเหตุ / ช่องบนกระดาษ | Class |
|---|---|---|---|---|
| id | uuid PK | N | | Internal |
| tenant_id | uuid | N | RLS | Internal |
| doc_no | varchar(30) unique/tenant | N | เลขที่ (ENG-DOC-NUM · CSM) | Internal |
| doc_date | date | N | วันที่บันทึกครั้งแรก | Internal |
| period_month | char(7) YYYY-MM | N | ประจำเดือน | Internal |
| status | enum(draft,pending,approved,cancelled) | N | | Internal |
| preparer_id | uuid | N | soft-ref F-EMP-001 (ผู้จัดทำ) | Internal |
| preparer_name_snapshot | varchar(200) | N | ลงชื่อ Sales Manager (PII) | Confidential·PII |
| position_snapshot | varchar(200) | Y | | Internal |
| unit_snapshot | varchar(200) | Y | หน่วยงาน/เขต | Internal |
| config_version | varchar(30) | N | SalesConfig version ที่ใช้ (หัวข้อ/น้ำหนัก/ช่วง) | Internal |
| overall_pct | numeric(5,2) | Y | สรุปผลการประเมิน - โดยรวม (snapshot ตอนอนุมัติ · computed) | Internal |
| overall_level | varchar(100) | Y | ข้อความแปลผล (snapshot) | Internal |
| header_snapshot | jsonb | Y | Organization (ชื่อ · โลโก้) ณ ออกเลข | Internal |
| approval_required | bool | N | จาก DOA | Internal |
| doa_ref | varchar(50) | Y | doa_entry_ref | Internal |
| approval_status | enum | N | = status (DOA contract) | Internal |
| approval_chain | jsonb | Y | snapshot ตอนส่ง (append-only) | Internal |
| approver_role | varchar(50) | Y | role ขั้นปัจจุบัน | Internal |
| approved_by | uuid | Y | | Internal |
| approved_at | timestamptz | Y | | Internal |
| returned_reason · returned_by · returned_at | text · uuid · timestamptz | Y | ไม่อนุมัติ → กลับร่าง (DEC-11) | Internal |
| cancelled_reason · cancelled_by · cancelled_at | text · uuid · timestamptz | Y | | Internal |
| version | int | N | optimistic lock | Internal |
| created_by/at · updated_by/at | | N | | Internal |

### csat_summary_line
| column | type | null | หมายเหตุ |
|---|---|---|---|
| id | uuid PK | N | |
| summary_id | uuid FK | N | |
| section_key | varchar(10) | N | q / d / s (ตาม config) |
| topic_id | varchar(30) | N | อ้าง SalesConfig.csat_topics |
| topic_text_snapshot | varchar(300) | N | ข้อความหัวข้อ ณ บันทึก (topic) |
| seq | int | N | ลำดับในด้าน |
| c5 · c4 · c3 · c2 · c1 | int ≥ 0 | N (default 0) | มากที่สุด · มาก · ปานกลาง · น้อย · ต้องปรับปรุง |
| total | int | N | รวม (computed) |
หมายเหตุ: รวมต่อคอลัมน์ (sum.c5..c1 · sum.total) และ % ต่อด้าน (pct) คำนวณตอนอ่าน (FN-02) ไม่เก็บ — ยกเว้น overall_pct snapshot ตอนอนุมัติ

### csat_summary_customer
| column | type | null | หมายเหตุ |
|---|---|---|---|
| id | uuid PK | N | |
| summary_id | uuid FK | N | |
| customer_id | uuid | N | soft-ref Customer (โดยมีรายชื่อดังนี้ · customer) · unique ต่อ summary |
| customer_name_snapshot | varchar(200) | N | PII ได้ |
| order_count | int | Y | จำนวนการสั่งซื้อ (snapshot ตอนส่ง · จาก Sale Order) |
| seq | int | N | |

### csat_summary_audit
| id · summary_id · action · actor_id · actor_name · at · note · tone | append-only |

## §4.3 Index
(tenant_id, doc_no) unique · (tenant_id, period_month, unit_snapshot) · (tenant_id, status) · csat_summary_customer (summary_id, customer_id) unique
