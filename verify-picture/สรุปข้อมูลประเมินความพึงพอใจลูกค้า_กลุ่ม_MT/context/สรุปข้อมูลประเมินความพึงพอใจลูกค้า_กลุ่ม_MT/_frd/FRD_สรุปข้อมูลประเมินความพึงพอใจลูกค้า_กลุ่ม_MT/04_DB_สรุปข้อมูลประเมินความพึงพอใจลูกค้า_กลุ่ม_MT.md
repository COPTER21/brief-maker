# 04_DB — F-TMP-008

## §4.1 Table Overview
| Table | ใช้ |
|---|---|
| `mt_csat_summary` | header (1 ใบ = 1 ครั้งการประเมิน) |
| `mt_csat_score` | คะแนนต่อหัวข้อ × ช่องทาง (config snapshot) |
| `mt_csat_recommendation` | ข้อเสนอแนะ (ลำดับ) |
| `mt_csat_audit` | ประวัติ append-only |
| (Document Center) `attachment` | ไฟล์แนบ (ref_type='MTS') |

## §4.2 Per-Table
### mt_csat_summary
| column | type | null | หมายเหตุ / ช่องบนกระดาษ | Class |
|---|---|---|---|---|
| id | uuid PK | N | | Internal |
| tenant_id | uuid | N | RLS | Internal |
| doc_no | varchar(30) unique/tenant | N | เลขที่ (ENG-DOC-NUM · MTS) | Internal |
| doc_date | date | N | วันที่บันทึกครั้งแรก | Internal |
| round_no | int ≥ 1 | N | ครั้งที่ (ท้ายหัวเรื่อง) | Internal |
| assessment_date | date | N | เอกสารประเมิน วันที่ | Internal |
| summary_date | date | N | สรุปข้อมูล วันที่ | Internal |
| status | enum(draft,final,cancelled) | N | | Internal |
| summarizer_id | uuid | N | soft-ref F-EMP-001 (ผู้สร้าง = ผู้สรุปการประเมิน) | Internal |
| summarizer_name_snapshot | varchar(200) | N | ผู้สรุปการประเมิณ (PII) | Confidential·PII |
| summarizer_position_snapshot | varchar(200) | Y | Sales Manager. | Internal |
| config_snapshot | jsonb | N | criteria[] (id · text · max_score) · channels[] (id · name) · std_pct · low_pct · bands[] ณ บันทึกครั้งแรก | Internal |
| max_total | int | N | รวมคะแนนเต็ม (computed จาก config snapshot) | Internal |
| pass_note | text | Y | ข้อความแนะนำกลุ่มผ่านมาตรฐาน | Internal |
| below_note | text | Y | ข้อความแนะนำกลุ่มต่ำกว่ามาตรฐานเล็กน้อย | Internal |
| far_note | text | Y | ข้อความแนะนำกลุ่มต่ำกว่าเกณฑ์ต่ำ | Internal |
| result_snapshot | jsonb | Y | ตอนยืนยันสรุป: ต่อช่องทาง {total, pct, status} + pass_channels · below_channels · far_channels | Internal |
| header_snapshot | jsonb | Y | Organization (ชื่อ · โลโก้) ณ ออกเลข | Internal |
| approval_required | bool | N | false (DEC-03) — นิยาม field DOA ทั้งชุดใน 02 §2.3 | Internal |
| approver_role · approved_by · doa_ref | varchar · uuid · varchar | Y | null · TODO: DOA engine (OQ-03) | Internal |
| finalized_at | timestamptz | Y | ยืนยันสรุป | Internal |
| cancelled_reason · cancelled_by · cancelled_at | text · uuid · timestamptz | Y | | Internal |
| version | int | N | optimistic lock | Internal |
| created_by/at · updated_by/at | | N | | Internal |

### mt_csat_score
| column | type | null | หมายเหตุ |
|---|---|---|---|
| id | uuid PK | N | |
| summary_id | uuid FK | N | |
| criterion_id | varchar(30) | N | อ้าง config_snapshot.criteria (หัวข้อประเมิน · topic) |
| channel_id | varchar(30) | N | อ้าง config_snapshot.channels (หัวคอลัมน์) |
| score | smallint | Y | คะแนนรายช่องทาง scores[channel_id] · 1..max_score · null = ยังไม่ประเมิน |
unique (summary_id, criterion_id, channel_id) · total / pct / status ต่อช่องทาง คำนวณตอนอ่าน (FN-02) — เก็บใน result_snapshot ตอนยืนยันสรุป

### mt_csat_recommendation
| column | type | null | หมายเหตุ |
|---|---|---|---|
| id | uuid PK | N | |
| summary_id | uuid FK | N | |
| seq | int | N | เลขกำกับ 1..n |
| text | text | N | ข้อเสนอแนะ |

### mt_csat_audit
| id · summary_id · action · actor_id · actor_name · at · note · tone | append-only |

## §4.3 Index
(tenant_id, doc_no) unique · (tenant_id, status) · (tenant_id, round_no, extract(year from assessment_date)) — ใช้ตรวจครั้งที่ซ้ำ (เตือน) · mt_csat_score (summary_id)
