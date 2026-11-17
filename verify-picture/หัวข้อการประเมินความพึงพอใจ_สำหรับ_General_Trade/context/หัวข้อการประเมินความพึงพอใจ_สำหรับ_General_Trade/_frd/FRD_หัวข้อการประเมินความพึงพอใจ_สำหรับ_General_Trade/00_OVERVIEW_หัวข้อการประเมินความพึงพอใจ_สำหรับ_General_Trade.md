# 00_OVERVIEW — F-TMP-002 หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade (GT CSAT Summary)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-002 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=N) |
| Source | BRD-SAL-CSM-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-002_v2 · FORM_SPEC FM-SAL-11 (47 ช่อง) · DECISIONS.lock (20 DEC · AI-DEFAULT 14) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · e2e ยังไม่รัน — NO-BROWSER) |
| Module / Area | Sales · Core Cube (Customer / CRM) |
| Feature / Doc code | F-TMP-002 · CSM — **รหัสชั่วคราว** (OQ-07) |
| Status | Ready for Dev (หลัง OQ-03/04 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ตารางคะแนน 3 ด้าน (หัวข้อจาก config) · คำนวณ รวม/%/โดยรวม/แปลผล · รายชื่อลูกค้า + จำนวนสั่งซื้อ (Sale Order) · DOA dynamic · ไม่อนุมัติ→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-SAL-11 Replica 2 หน้า · เลข CSM · CSV
### Out of Scope
แบบสำรวจ FM-SAL-10 + ดึงคะแนนอัตโนมัติ · เปลี่ยนค่า/ส่งต่อระบบอื่น (DEC-01/02) · ทำซ้ำ · ประกาศ · กันซ้ำเดือนเดียวกัน (OQ-06)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| Sales Manager (ผู้จัดทำ) | Maker | owner (role-mgr-sales) |
| ผู้อำนวยการสายงานการขาย | Approver | role-mgr-bu (ชั่วคราว — OQ-03) |
| ผู้ดูแลเอกสารฝ่ายขาย (Sales admin) | Monitor · admin view · ยกเลิก | sales_admin (สิทธิ์ระดับ module) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · Sales › Customer (อ่าน) · Sales › Sale Order (COUNT ต่อเดือน · อ่าน) · Sales Configuration (SalesConfig.csat_* · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type CSM · status · print_config) · Organization (header/logo)
### Downstream
ENG-NOTIFY (csm_cancelled · csm_low_csat) · ENG-DOC-STORE (approved_final) · รายงาน CSAT (ประกาศ event `csm.approved` — **ไม่ยิงรอบนี้** DEC-02)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/csat-gt` (feature.html = source of truth) · BE: REST `/api/v1/csat-summaries` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: คะแนน/สรุป · Confidential(PII): ชื่อลูกค้า (อาจเป็นบุคคลธรรมดา) · ชื่อผู้จัดทำ/ผู้อนุมัติ snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (สูตร % · 1 ขั้น · กลับร่าง) | Strike | ก่อน UAT |
| OQ-03 | role "ผู้อำนวยการสายงานการขาย" ไม่มีใน DOA master (ใช้ role-mgr-bu) | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | SalesConfig.csat_* ใน Sales Configuration | พี่เบิร์ด | ก่อน dev |
| OQ-05 | ผูกแบบสำรวจ FM-SAL-10 | Strike | – |
| OQ-06 | กันสร้างซ้ำเดือน/หน่วยงาน | ลูกค้า | – |
| OQ-07 | F-TMP-002 / CSM / function_code ชั่วคราว | Strike | ก่อน register |

## §0.9 Glossary
CSAT = Customer Satisfaction Score · GT = General Trade (ร้านค้าปลีก/ค้าส่งดั้งเดิม) · ระดับคะแนน มากที่สุด…ต้องปรับปรุง (น้ำหนักจาก config) · คำตอบ = จำนวนลูกค้าที่ให้คะแนนระดับนั้น
