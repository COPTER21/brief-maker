# 00_OVERVIEW — F-TMP-001 แบบฟอร์มใบแจ้งซ่อมสินทรัพย์ (Asset Repair Request)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-001 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · unattended) |
| Variant | **FULL** (pages=3, states=4, approval=Y, print=Y) |
| Source | BRD-ASM-RPR-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-001_v2 · FORM_SPEC FM-ASM-03 · DECISIONS.lock (16 DEC · AI-DEFAULT 12) · feature.html (html-generator-v9.4 · audit FAIL 0 · e2e 21/21) |
| Module / Area | Asset Management · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-02/03/05 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (แท็บ ทั้งหมด/รอฉันพิจารณา) · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · รายการแจ้งซ่อม 6 ช่อง · ประวัติการซ่อม (ผู้ตรวจสอบกรอก) · DOA 2 ขั้น · ไม่อนุมัติ→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-ASM-03 Replica · เลข RPR · CSV
### Out of Scope
Asset Master · Maintenance Schedule · ใบงานซ่อม/จัดซื้ออะไหล่ · ปรับมูลค่าสินทรัพย์ · ส่งต่อระบบอื่น (DEC-01/02) · ทำซ้ำ · ประกาศ (DEC-12)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้แจ้งซ่อม (พนักงาน) | Maker | owner |
| ผู้ตรวจสอบ | Checker | role-line-manager |
| ผู้อนุมัติ | Approver | role-mgr-acc |
| ผู้ดูแลงานซ่อม (ฝ่ายบริหารสินทรัพย์) | Custodian · admin view | admin role ของหน่วยงานเจ้าของเอกสาร (DEC-10) |

## §0.5 Dependencies
### Upstream
Employee (อ่าน) · Organization: Position & Tier · Department (อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type RPR · status · print_config) · Company/Organization (header_snapshot โลโก้)
### Downstream
ENG-NOTIFY (rpr_cancelled · rpr_ready_for_repair) · ENG-DOC-STORE (approved_final) · Maintenance Schedule / Asset Master (ประกาศ event `rpr.approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/asset-repair` (feature.html = source of truth) · BE: REST `/api/v1/asset-repair-requests` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เอกสาร/รายการ/ประวัติซ่อม · Confidential(PII): ชื่อผู้แจ้ง snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (12 ข้อ) | Strike | ก่อน UAT |
| OQ-03 | ผู้ตรวจสอบ = ผู้บังคับบัญชา (role-line-manager) หรือเจ้าหน้าที่สินทรัพย์/ช่าง (ต้องเพิ่ม role) | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | Asset Master / Maintenance Schedule (Phase 2) | Strike | – |
| OQ-05 | รหัส feature จริงแทน F-TMP-001 · function_code taxonomy | Strike | ก่อน register |
| OQ-06 | Rev. ของแบบฟอร์ม | ลูกค้า | – |

## §0.9 Glossary
ทะเบียนสินทรัพย์ = รหัสทรัพย์สินถาวร (AS-…) · ผู้ตรวจสอบ = ผู้พิจารณาขั้นแรก บันทึกประวัติการซ่อม · ตีกลับแก้ไข = ไม่อนุมัติแล้วกลับเป็นร่างเลขเดิม

## §0.12 Coverage Manifest (R13)
| แหล่ง | รายการ | ครอบที่ |
|---|---|---|
| ช่องในฟอร์ม (FORM_SPEC 14) | เลขที่ · ชื่อ-นามสกุล · ตําแหน่ง · ฝ่าย/แผนก · รายการ×6 · วันที่ผู้แจ้ง · ประวัติ×3 | 01 §1.2 · 04 §4.2 |
| ลายเซ็น 4 จุด | ผู้แจ้งซ่อม×2 · ผู้ตรวจสอบ · ผู้อนุมัติ | 03 FN-08 · 05 BR-09/10 |
| DEC 16 | DEC-01..16 | 07 §7.0 |
| Story 10 | S-01..10 | 06 §6.1 |
| HTML route 3 + modal 5 | P-01..03 · M-01..05 | 01 §1.1 |
