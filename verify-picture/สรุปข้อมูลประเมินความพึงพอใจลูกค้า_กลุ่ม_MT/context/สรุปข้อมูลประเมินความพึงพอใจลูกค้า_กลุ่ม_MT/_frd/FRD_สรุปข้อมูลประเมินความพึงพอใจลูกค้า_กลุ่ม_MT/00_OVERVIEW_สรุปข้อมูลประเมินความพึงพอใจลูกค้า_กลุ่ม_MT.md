# 00_OVERVIEW — F-TMP-008 สรุปข้อมูลประเมินความพึงพอใจลูกค้า กลุ่ม MT (MT CSAT Summary)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-008 v1.0 · frd-generator-v6 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **FULL** (pages=3, states=3, approval=N, money=N) |
| Source | BRD-SAL-MTS-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-008_v2 · FORM_SPEC FM-SAL-07 (20 ช่อง) · DECISIONS.lock (20 DEC · AI-DEFAULT 12) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · e2e ยังไม่รัน — NO-BROWSER) |
| Module / Area | Sales · Core Cube (Customer / CRM) |
| Feature / Doc code | F-TMP-008 · MTS — **รหัสชั่วคราว** (OQ-07) |
| Status | Ready for Dev (หลัง OQ-04 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (4 ขั้น) · ดู 4 แท็บ · ตารางคะแนน หัวข้อ × ช่องทาง (จาก config) · คำนวณ รวม/%/ผลเทียบมาตรฐาน/รายชื่อกลุ่ม · ข้อความแนะนำ · ข้อเสนอแนะ · ยืนยันสรุป (ไม่มีผู้อนุมัติ) · ยกเลิก · แนบไฟล์ · PDF FM-SAL-07 Replica 2 หน้า · เลข MTS · CSV
### Out of Scope
แบบประเมินรายลูกค้า MT + ดึงคะแนนอัตโนมัติ · เปลี่ยนค่า/ส่งต่อระบบอื่น (DEC-01/02) · สายอนุมัติ (DEC-03 · OQ-03) · ทำซ้ำ · ประกาศ

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| Sales Manager (ผู้สรุปการประเมิน) | Maker | owner (role-mgr-sales) |
| ผู้ดูแลเอกสารฝ่ายขาย (Sales admin) | Monitor · admin view · ยกเลิก | sales_admin (สิทธิ์ระดับ module) |
| หัวหน้าหน่วยธุรกิจ | ผู้รับแจ้ง (ไม่ตัดสิน) | role-mgr-bu (role ใกล้สุดของผู้บริหารฝ่ายขายใน master) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · Sales Configuration (SalesConfig.mt_* · อ่าน) · Customer master กลุ่ม MT (ผ่าน SalesConfig.mt_channels — OQ-04) · F-DOCCFG/F003 (doc_type MTS · status · print_config) · Organization (header snapshot)
### Downstream
ENG-NOTIFY (mts_low_channel · mts_cancelled) · ENG-DOC-STORE (final snapshot) · รายงาน CSAT (ประกาศ event `mts.finalized` — **ไม่ยิงรอบนี้** DEC-02)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/csat-mt` (feature.html = source of truth) · BE: REST `/api/v1/mt-csat-summaries` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less) + data contract (03 FN-07)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: คะแนน/สรุป/ชื่อช่องทาง (บริษัทคู่ค้า) · Confidential(PII): ชื่อผู้สรุป snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (ไม่มีผู้อนุมัติ · เกณฑ์ 95/80 · ถ้อยคำป้ายเหลือง/แดง) | Strike | ก่อน UAT |
| OQ-03 | ต้องการผู้รับรองรายงานหรือไม่ (ถ้าต้องการ → DOA กลาง role-mgr-bu) | ลูกค้า + พี่เบิร์ด | – |
| OQ-04 | SalesConfig.mt_* ใน Sales Configuration · ผูกช่องทางกับ Customer master | พี่เบิร์ด | ก่อน dev |
| OQ-05 | ผูกแบบประเมินลูกค้า MT | Strike | – |
| OQ-06 | แบบพิมพ์แนวตั้ง 2 หน้า (ต้นฉบับแนวนอน) | ลูกค้า | ก่อน UAT |
| OQ-07 | F-TMP-008 / MTS / function_code ชั่วคราว | Strike | ก่อน register |

## §0.9 Glossary
MT = Modern Trade (ห้าง/ร้านค้าปลีกสมัยใหม่) · ช่องทาง = ลูกค้า MT แต่ละราย (หัวคอลัมน์) · ครั้งที่ = รอบการประเมิน (ต่อปี) · ผลเทียบมาตรฐาน = ผ่านมาตรฐาน / ต่ำกว่ามาตรฐาน / ค่อนข้างต่ำกว่ามาตรฐาน
