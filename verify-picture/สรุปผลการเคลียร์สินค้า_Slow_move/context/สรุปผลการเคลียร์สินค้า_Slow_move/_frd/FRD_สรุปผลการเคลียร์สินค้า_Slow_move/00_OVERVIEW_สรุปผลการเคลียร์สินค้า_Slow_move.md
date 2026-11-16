# 00_OVERVIEW — F-TMP-003 สรุปผลการเคลียร์สินค้า Slow move (Slow Moving Stock Clearance Summary)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-003 v1.0 · frd-generator-v6 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (fallback from BRD: pages=3, states=5, approval=Y, print=Y) |
| Source | BRD-WHS-SMC-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-003_v2 · FORM_SPEC FM-WHS-09 · DECISIONS.lock (15 DEC) · feature.html (html-generator-v9.4 · audit FAIL 0 · jsdom smoke 44/44 · [NO-BROWSER] e2e ยังไม่รัน) |
| Module / Area | Inventory / Warehouse · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-04/05 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (segmented · ค้นหา · กรองสถานะ/เดือน · CSV) · สร้าง/แก้ไข (wizard 3 ขั้น · ตารางรายการ) · ดู 4 แท็บ · DOA dynamic (ค่าเริ่ม 1 ขั้น) · ไม่อนุมัติ→ร่างเลขเดิม · ยกเลิก · แนบไฟล์ · PDF FM-WHS-09 Replica 2 หน้า · เลข SMC
### Out of Scope
ตัดสต็อก/Stock Adjustment/Transfer/Return (DEC-01/02) · คำนวณรายการ Slow move อัตโนมัติ · หน้าตั้งค่าแนวทาง (OQ-04) · ช่องคลัง/คงเหลือ/หน่วย (OQ-03) · ทำซ้ำ (DEC-11 · OQ-06) · ประกาศ

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ (เจ้าหน้าที่คลังสินค้า) | Maker | owner |
| ผู้อนุมัติ (ผู้จัดการคลังสินค้าของหน่วยงาน) | Approver | role-mgr-wh |
| ผู้จัดการฝ่ายคลังสินค้า | Admin view · ยกเลิกได้ | role-mgr-wh (admin role ของหน่วยงานเจ้าของเอกสาร) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit/ผังองค์กร · หัวกระดาษ) · F-PRODUCT-MASTER-001 (T_product · รหัส/ชื่อ/หน่วย · อ่าน) · F-DLG-001 DOA (resolve role-mgr-wh) · F-DOCCFG/F003 (doc_type SMC · status · print_config) · SlowMoveConfig (แนวทางการเคลียร์ — ใหม่ · OQ-04)
### Downstream
ENG-NOTIFY (smc_cancelled) · ENG-DOC-STORE (approved_final) · Stock Adjustment/Transfer/Purchase Return (ประกาศ event `smc.approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/slow-move` (feature.html = source of truth) · BE: REST `/api/v1/slow-move-clearances` · PDF render ฝั่ง server จาก `print/form.tpl.html` (logic-less) + data contract (03 FN-09)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: รายการสินค้า/ผลการเคลียร์/สถานะ · Confidential(PII): ชื่อผู้จัดทำ/ผู้อนุมัติ snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT | Strike | ก่อน UAT |
| OQ-03 | ช่องคลัง/คงเหลือ/หน่วย/วันผลิต (DEC-12/15) | ลูกค้า | Phase 2 |
| OQ-04 | SlowMoveConfig อยู่ที่ไหน (feature ใหม่) | พี่เบิร์ด | ก่อน dev |
| OQ-05 | role-mgr-wh resolve ตามหน่วยงานผู้จัดทำ (relative) | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-06 | ปุ่มทำซ้ำของ archetype ขัด DEC-11 | Strike | – |
| OQ-07 | function_code taxonomy · รหัส feature จริง | Strike | ก่อน register |
| OQ-08 | แถวเกิน 53 ต่อใบ → แบบพิมพ์เพิ่มหน้า? | Strike | – |

## §0.9 Glossary
Slow move = สินค้าเคลื่อนไหวช้าที่ต้องติดตามเคลียร์ · ผลการเคลียร์ = วันที่ + จำนวน ที่เคลียร์ได้จริง · ใบ = 1 ผู้จัดทำ × 1 เดือน

## §0.12 Coverage Manifest
| แหล่ง | รายการ | ครอบคลุมที่ |
|---|---|---|
| ช่องในฟอร์ม (FORM_SPEC 12) | หัวกระดาษ F01/F02 · ประจำเดือน F03 · ลำดับ/รหัสสินค้า/รายละเอียด/วันที่ติดตาม/แนวทางการเคลียร์/วันที่/จำนวน/วันหมดอายุ/หมายเหตุ (F04–F12) | 01 §1.2 · 04 §4.2 |
| ค่าคงที่ | แนวทางการเคลียร์ → SlowMoveConfig.clearance_methods | 03 FN-02 · 05 BR-01 |
| ลายเซ็น | ผู้จัดทำ · ผู้อนุมัติ | 03 FN-09 · 05 BR-12 |
| Doc No./Rev. | FM-WHS-09 · Rev.00 : 01/07/2569 | print_config (F-DOCCFG) |
| DEC | 15 ข้อ | 07 §7.0 |
