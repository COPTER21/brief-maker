# 00_OVERVIEW — F-TMP-001 แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction Evaluation)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-001 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · unattended) |
| Variant | **FULL** (fallback from BRD: pages=3, states=3, approval=N, money=N → STANDARD + 07 §7.0 จาก DECISIONS.lock + INDEX ตาม Mode 0) |
| Source | BRD-TMP-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-001_v2 · FORM_SPEC FM-SAL-06 · DECISIONS.lock (13 DEC) · feature.html (html-generator-v9.4 · audit FAIL 0 · e2e [NO-BROWSER] ยังไม่รัน) |
| Module / Area | Sales · ลูกค้าสัมพันธ์ (Core Cube) |
| Status | Ready for Dev (หลัง OQ-02/03 ปิด · ต้องรัน e2e บนเครื่องที่มี browser) |
| Date | 2026-10-08 |
| รหัสชั่วคราว | F-TMP-001 · REQ-TMP-001 — รอเลขจริง (OQ-03) |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-08 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ข้อ 1–4 · คะแนน 9 หัวข้อ (1–5) · ข้อเสนอแนะ · ส่ง (ไม่มีสายพิจารณา DEC-03) · ยกเลิก · แนบไฟล์ · PDF FM-SAL-06 Replica · เลข CSE · CSV
### Out of Scope
ร้านค้าตอบเองผ่านลิงก์ (OQ-04) · รายงาน/แดชบอร์ดคะแนน · ส่งคะแนนเข้า CRM/Customer (DEC-02) · ทำซ้ำ · ประกาศ (DEC-10)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| เจ้าหน้าที่ขาย (ผู้ประเมิน/ผู้บันทึก) | Maker | owner |
| ผู้จัดการฝ่ายขาย | Monitor · admin view | role-mgr-sales |

## §0.5 Dependencies
### Upstream
Organization (legal_name · logo — อ่าน) · Customer master (Sales › Customer — ตัวช่วยเลือกชื่อร้าน · อ่าน) · F-DOCCFG (doc_type CSE · status · print_config) · Employee (ชื่อ/ตำแหน่งผู้บันทึก)
### Downstream
ENG-NOTIFY (`cse_submitted`) · CRM/Customer (ประกาศ event `cse.submitted` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน · Phase 2)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/customer-satisfaction` (feature.html = source of truth) · BE: REST `/api/v1/customer-satisfactions` · PDF render ฝั่ง server จาก `print/form.tpl.html` (logic-less) + data contract (03 FN-06)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: ทั้งเอกสาร · ไม่มีช่อง PII บนกระดาษ · ชื่อผู้บันทึก = ข้อมูลพนักงาน (Internal)

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (ไม่มีสายพิจารณา · สิทธิ์ยกเลิก · ผจก.ขายเห็นทุกใบ) | ทีม BA | ก่อน UAT |
| OQ-03 | รหัสชั่วคราว F-TMP-001 / REQ-TMP-001 → เลขจริง · function_code taxonomy | ทีม BA | ก่อน register |
| OQ-04 | ผู้ประเมิน = ผู้บันทึกในระบบ หรือให้ร้านค้าตอบเอง | ลูกค้า | ก่อน UAT |
| OQ-05 | ชื่อบริษัทที่ถูกต้อง (จำกัด / จำกัด (มหาชน)) — ระบบอ่าน Organization | ลูกค้า | – |

## §0.9 Glossary
ห้าง/ร้านค้า = ลูกค้าที่ถูกถามความเห็น · บริษัทคู่ค้า = บริษัทเจ้าของเอกสาร (ผู้ถูกประเมิน) · ผู้ประเมิน = ผู้บันทึกแบบประเมินในระบบ

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F12 (FORM_SPEC) | store.name · partner.company_name · business_type · relationship_years · rating × 9 · suggestion | 01 §1.2 P-02 · 04 §4.2 · 03 FN-01/FN-06 |
| BRD S-01..S-12 | stories | 06 AC-01..AC-12 |
| BRD BR-01..09 · VR-01..06 · EC-01..08 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..13 | มติ | 07 §7.0 |
| declaration | DOCCFG · MDOC · NTF (ไม่มี DOA — DEC-03) | declarations/ · 03 FN-03/FN-05 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..03 | 01 §1.1 |
ไม่มี requirement หล่น
