# 00_OVERVIEW — F-TMP-002 แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท์ประจำวัน (Forklift Daily Inspection Checklist)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-002 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (fallback from BRD: pages=3, states=5, approval=Y, print=Y) |
| Source | BRD-WHS-FLI-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-002_v2 · FORM_SPEC FM-WHS-04 · DECISIONS.lock (17 DEC) · feature.html (html-generator-v9.4 · audit FAIL 0 · jsdom smoke 27/27 · [NO-BROWSER] e2e ยังไม่รัน) |
| Module / Area | Inventory / Warehouse · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-04/05 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (segmented · ค้นหา · กรอง · CSV) · สร้าง/บันทึกผลรายวัน (wizard 3 ขั้น) · ดู 4 แท็บ · DOA dynamic (ค่าเริ่ม 1 ขั้น) · ส่งกลับแก้ไข→ร่างเลขเดิม · ยกเลิก · แนบไฟล์ · แจ้งพบผิดปกติ · PDF FM-WHS-04 Replica 2 หน้า · เลข FLI
### Out of Scope
ทะเบียนรถ/ผูกรถรายคัน (OQ-03) · ใบแจ้งซ่อม/Maintenance (DEC-02) · หน้าตั้งค่ารายการตรวจ (OQ-04) · ทำซ้ำ (DEC-13 · OQ-06) · ประกาศ

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้ตรวจสอบ (พนักงานขับรถ/คลัง) | Maker | owner |
| หัวหน้างานตรวจสอบ | Checker/Approver | role-supervisor |
| ผู้จัดการคลังสินค้า | Admin view · ยกเลิกได้ | role-mgr-wh |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit/ผังองค์กร · หัวกระดาษ) · F-DLG-001 DOA (resolve role-supervisor) · F-DOCCFG/F003 (doc_type FLI · status · print_config) · ForkliftChecklistConfig (รายการตรวจ — ใหม่ · OQ-04)
### Downstream
ENG-NOTIFY (fli_defect_found · fli_cancelled) · ENG-DOC-STORE (approved_final) · Asset/Maintenance (ประกาศ event `fli.defect_recorded` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/forklift` (feature.html = source of truth) · BE: REST `/api/v1/forklift-inspections` · PDF render ฝั่ง server จาก `print/form.tpl.html` (logic-less) + data contract (03 FN-09)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: ผลตรวจ/สถานะ · Confidential(PII): ชื่อผู้ตรวจสอบ/หัวหน้างาน snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT | Strike | ก่อน UAT |
| OQ-03 | ช่องหมายเลข/ทะเบียนรถ (DEC-17) | ลูกค้า | Phase 2 |
| OQ-04 | ForkliftChecklistConfig อยู่ที่ไหน (feature ใหม่) | พี่เบิร์ด | ก่อน dev |
| OQ-05 | role-supervisor แบบ relative (ผังองค์กร) | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-06 | ปุ่มทำซ้ำของ archetype ขัด DEC-13 | Strike | – |
| OQ-07 | function_code taxonomy · รหัส feature จริง | Strike | ก่อน register |

## §0.9 Glossary
✓ = ปกติ / พร้อมใช้งาน (ok) · ✗ = ผิดปกติ / ต้องแก้ไข (ng) · ว่าง = ยังไม่ตรวจ · ใบ = 1 ผู้ตรวจสอบ × 1 ประเภทรถ × 1 เดือน

## §0.12 Coverage Manifest
| แหล่ง | รายการ | ครอบคลุมที่ |
|---|---|---|
| ช่องในฟอร์ม (FORM_SPEC 12) | หัวกระดาษ F01/F02 · ประจำเดือน F03 · ลำดับ/รายการ/ผลรายวัน × 3 กลุ่ม (F04–F12) | 01 §1.2 · 04 §4.2 |
| ตัวเลือก | ประเภทรถ (fuel/electric) · เกณฑ์ ✓/✗ | 01 · 04 `vehicle_type` · `result` |
| ลายเซ็น | ผู้ตรวจสอบ · หัวหน้างานตรวจสอบ | 03 FN-09 · 05 BR-12 |
| Doc No./Rev. | FM-WHS-04 · Rev.00 : 01/07/2569 | print_config (F-DOCCFG) |
| DEC | 17 ข้อ | 07 §7.0 |
