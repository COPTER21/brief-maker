# 04_DB — F-TMP-005

## §4.1 Table Overview
| Table | ใช้ |
|---|---|
| `sds_summary` | header |
| `sds_summary_column` | คอลัมน์ลูกค้า (≤ 12 ต่อใบ) + ระดับ 5 หัวข้อ (snapshot จาก SDA) |
| `sds_summary_audit` | ประวัติ append-only |
| (Document Center) `attachment` | ไฟล์แนบ (ref_type='SDS') |

## §4.2 Per-Table
### sds_summary
| column | type | null | หมายเหตุ / ช่องบนกระดาษ | Class |
|---|---|---|---|---|
| id | uuid PK | N | | Internal |
| tenant_id | uuid | N | RLS | Internal |
| doc_no | varchar(30) unique/tenant | N | เลขที่ (ENG-DOC-NUM · SDS) | Internal |
| doc_date | date | N | วันที่บันทึกครั้งแรก | Internal |
| period_month | char(7) YYYY-MM | N | ประจำเดือน (เพิ่ม · DEC-06) | Internal |
| status | enum(draft,pending,approved,cancelled) | N | | Internal |
| preparer_id | uuid | N | soft-ref F-EMP-001 (ผู้สรุปผลการประเมิน) | Internal |
| preparer_name_snapshot | varchar(200) | N | ลงชื่อผู้สรุป (PII) | Confidential·PII |
| position_snapshot | varchar(200) | Y | | Internal |
| unit_snapshot | varchar(200) | Y | หน่วยงาน | Internal |
| conclusion | text (≤ 1000) | Y | สรุปผลการประเมิน (บังคับตอนส่ง) | Internal |
| suggestion | text (≤ 1000) | Y | ข้อเสนอแนะ | Internal |
| config_version | varchar(30) | N | SalesConfig version ที่ใช้ (หัวข้อ/ระดับ) | Internal |
| header_snapshot | jsonb | Y | Organization (ชื่อ · โลโก้) ณ ออกเลข | Internal |
| approval_required | bool | N | จาก DOA | Internal |
| doa_ref | varchar(50) | Y | doa_entry_ref | Internal |
| approval_status | enum | N | = status (DOA contract) | Internal |
| approval_chain | jsonb | Y | snapshot ตอนส่ง (append-only) | Internal |
| approver_role | varchar(50) | Y | role ขั้นปัจจุบัน | Internal |
| approved_by | uuid | Y | | Internal |
| approved_at | timestamptz | Y | | Internal |
| returned_reason · returned_by · returned_at | text · uuid · timestamptz | Y | ไม่อนุมัติ → กลับร่าง (DEC-08) | Internal |
| cancelled_reason · cancelled_by · cancelled_at | text · uuid · timestamptz | Y | | Internal |
| version | int | N | optimistic lock | Internal |
| created_by/at · updated_by/at | | N | | Internal |

### sds_summary_column
| column | type | null | หมายเหตุ |
|---|---|---|---|
| id | uuid PK | N | |
| summary_id | uuid FK | N | |
| seq | int 1–12 | N | ลำดับคอลัมน์ |
| customer_id | uuid | N | soft-ref Customer · unique ต่อ summary (DEC-12) |
| customer_name | varchar(200) | N | หัวคอลัมน์ (snapshot · PII ได้) |
| sda_id | uuid | N | soft-ref F-TMP-004 SDA (สถานะ recorded) |
| survey_ref | varchar(60) | N | แถวใต้ชื่อลูกค้า = sda_doc_no + survey_date (snapshot · DEC-13) |
| sda_doc_no · survey_date | varchar(30) · date | N | |
| score_q1 · score_q2 · score_q3 · score_q4 · score_q5 | smallint 1–5 | Y | q1 ความรวดเร็วในการตอบคำถาม · q2 การให้ข้อมูลสินค้า · q3 การแก้ไขปัญหา (สินค้าเสียหาย) · q4 ความเหมาะสมในการแก้ปัญหา · q5 คุณภาพสินค้า (snapshot จาก SDA · ป้ายจาก sda_scale) |
| sda_count_in_period | smallint | N | จำนวนใบในเดือน (> 1 = ใช้ใบล่าสุด) |

### sds_summary_audit
| id · summary_id · action · actor_id · actor_name · at · note · tone | append-only |

## §4.3 Index
(tenant_id, doc_no) unique · (tenant_id, period_month) · (tenant_id, status) · sds_summary_column (summary_id, customer_id) unique · (sda_id)
