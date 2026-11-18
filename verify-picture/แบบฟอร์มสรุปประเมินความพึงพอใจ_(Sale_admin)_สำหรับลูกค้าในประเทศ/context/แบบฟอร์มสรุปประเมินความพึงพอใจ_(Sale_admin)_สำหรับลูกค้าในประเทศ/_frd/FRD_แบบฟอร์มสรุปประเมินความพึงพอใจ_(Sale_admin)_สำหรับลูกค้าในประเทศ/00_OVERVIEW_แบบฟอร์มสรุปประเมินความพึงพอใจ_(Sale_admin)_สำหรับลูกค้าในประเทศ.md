# 00_OVERVIEW — F-TMP-005 แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ (SDS)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-005 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=N) |
| Source | BRD-SAL-SDS-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-005_v2 · FORM_SPEC FM-SAL-21 (10 ช่อง) · DECISIONS.lock (16 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · e2e ทางการยังไม่รัน — NO-BROWSER) |
| Module / Area | Sales · Core Cube (Customer / CRM) |
| Feature / Doc code | F-TMP-005 · SDS — **รหัสชั่วคราว** (OQ-07) |
| Status | Ready for Dev (หลัง OQ-03/04 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ประจำเดือน · ดึงแบบประเมิน SDA (FM-SAL-20) ที่บันทึกผลแล้วของเดือน ≤ 12 ราย · ตารางหัวข้อ 5 ข้อ × ลูกค้า (อ่านอย่างเดียว) · สรุปผลการประเมิน · ข้อเสนอแนะ · DOA dynamic · ไม่อนุมัติ→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-SAL-21 Replica 2 หน้า · เลข SDS · CSV
### Out of Scope
แก้คะแนนในใบสรุป (แก้ที่ SDA ต้นทาง) · คะแนนรวม/% (กระดาษไม่มี) · เปลี่ยนค่า/ส่งต่อระบบอื่น (DEC-01/02) · ทำซ้ำ · ประกาศ · กันซ้ำเดือนเดียวกัน (OQ-06)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| Sales Administrative Manager / Sale admin (ผู้สรุปผลการประเมิน) | Maker | owner |
| Managing Director (ผู้รับทราบและอนุมัติ) | Approver | role-ceo (ชั่วคราว — OQ-03) |
| ผู้จัดการฝ่ายขาย | Monitor · admin view · ยกเลิก | role-mgr-sales |

## §0.5 Dependencies
### Upstream
F-TMP-004 แบบประเมิน SDA (FM-SAL-20 · อ่านเฉพาะสถานะ recorded) · F-EMP-001 (Employee · อ่าน) · Sales › Customer (อ่าน) · Sales Configuration (SalesConfig.sda_topics / sda_scale · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type SDS · status · print_config) · Organization (header/logo)
### Downstream
ENG-NOTIFY (sds_cancelled · sds_low_score_approved) · ENG-DOC-STORE (approved_final) · รายงานความพึงพอใจ (ประกาศ event `sds.approved` — **ไม่ยิงรอบนี้** DEC-02)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/csat-domestic-summary` (feature.html = source of truth) · BE: REST `/api/v1/sds-summaries` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less) + data contract (03 FN-07)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: ระดับความพึงพอใจ/สรุป · Confidential(PII): ชื่อลูกค้า (มีบุคคลธรรมดา) · ชื่อผู้สรุป/ผู้อนุมัติ snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (ประจำเดือน · แถวใต้ชื่อ · ≤ 12 ราย · 1 ขั้น · กลับร่าง) | Strike | ก่อน UAT |
| OQ-03 | role "Managing Director" ไม่มีใน DOA master (ใช้ role-ceo) | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | SalesConfig.sda_topics/sda_scale ใน Sales Configuration (ร่วม F-TMP-004) | พี่เบิร์ด | ก่อน dev |
| OQ-05 | แบบพิมพ์แนวตั้ง 2 หน้า 12 คอลัมน์ แทนต้นฉบับแนวนอน 1 หน้า 6 คอลัมน์ | ลูกค้า | ก่อน UAT |
| OQ-06 | กันสร้างซ้ำเดือน / ลูกค้า > 12 ราย | ลูกค้า | – |
| OQ-07 | F-TMP-005 / SDS / function_code ชั่วคราว | Strike | ก่อน register |

## §0.9 Glossary
SDA = แบบประเมินความพึงพอใจ (Sale admin) ลูกค้าในประเทศ FM-SAL-20 (F-TMP-004) · SDS = ใบสรุปของ SDA (feature นี้) · ระดับ มากที่สุด(5)…ควรปรับปรุง(1) (น้ำหนักจาก config) · ระดับต่ำ = น้อย/ควรปรับปรุง
