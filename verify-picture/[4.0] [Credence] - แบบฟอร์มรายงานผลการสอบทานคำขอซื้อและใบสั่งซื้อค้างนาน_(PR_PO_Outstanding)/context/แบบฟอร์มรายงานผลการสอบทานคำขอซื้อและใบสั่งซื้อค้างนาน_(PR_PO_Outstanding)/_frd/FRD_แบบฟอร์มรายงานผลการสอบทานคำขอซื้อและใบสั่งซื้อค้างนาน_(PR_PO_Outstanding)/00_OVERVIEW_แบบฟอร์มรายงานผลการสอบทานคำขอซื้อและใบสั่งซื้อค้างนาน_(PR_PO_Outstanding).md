# 00_OVERVIEW — F-TMP-005 แบบฟอร์มรายงานผลการสอบทานคำขอซื้อและใบสั่งซื้อค้างนาน (PR/PO Outstanding Review Report)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-005 v1.0 · frd-generator-v6 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (fallback from BRD: pages=3, states=5, approval=Y, print=Y) |
| Source | BRD-PUR-PPO-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-005_v2 · FORM_SPEC FM-PUR-03 (ชีต 1 Rev.02) · DECISIONS.lock (16 DEC) · feature.html (html-generator-v9.4 · audit FAIL 0 · jsdom smoke 47/47 · [NO-BROWSER] e2e ยังไม่รัน) |
| Module / Area | Purchase · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-05/06 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (segmented · ค้นหา · กรองสถานะ/เดือน · CSV ระดับรายการ) · สร้าง/แก้ไข (wizard 3 ขั้น · ตารางรายการ 12 ช่อง) · ดู 4 แท็บ · DOA dynamic (ค่าเริ่ม 1 ขั้น) · ไม่อนุมัติ→ร่างเลขเดิม · ยกเลิก · แนบไฟล์ · PDF FM-PUR-03 Replica 2 หน้า · เลข PPO
### Out of Scope
ดึงรายการ PR/PO ค้างอัตโนมัติ · ปิด/ยกเลิก PR-PO (DEC-01/02 · PR F072/PO F078 ยังไม่มี · OQ-04) · คอลัมน์อายุค้าง/มูลค่า/เกณฑ์ค้างนาน (DEC-15 · OQ-03) · ทำซ้ำ (DEC-11) · ประกาศ · แบบพิมพ์ > 24 แถว (OQ-08)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำรายงาน (เจ้าหน้าที่จัดซื้อ) | Maker | owner |
| ผู้มีอำนาจอนุมัติ (ผู้จัดการจัดซื้อของหน่วยงาน) | Approver | role-mgr-pur |
| ผู้จัดการฝ่ายจัดซื้อ | Admin view · ยกเลิกได้ | role-mgr-pur (admin role ของหน่วยงานเจ้าของเอกสาร) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · ผู้จัดทำ/ตำแหน่ง · อ่าน) · F-ORG-001 (OrgUnit/ผังองค์กร · หน่วยงาน · ฝ่ายขอซื้อ · หัวกระดาษ) · F-PRODUCT-MASTER-001 (uom_master · หน่วย · อ่าน) · F-DLG-001 DOA (resolve role-mgr-pur) · F-DOCCFG/F003 (doc_type PPO · status · print_config)
### Downstream
ENG-NOTIFY (ppo_cancelled) · ENG-DOC-STORE (approved_final) · PR (F072)/PO (F078) (ประกาศ event `ppo.approved` — **ไม่ยิงรอบนี้** DEC-02 · ยังไม่มีในระบบ) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/pr-po-outstanding` (feature.html = source of truth) · BE: REST `/api/v1/pr-po-outstanding-reviews` · PDF render ฝั่ง server จาก `print/form.tpl.html` (logic-less) + data contract (03 FN-09)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เลข PR/PO · ผู้ขาย · รายละเอียด · สาเหตุ/สถานะ/แนวทาง · Confidential(PII): ชื่อผู้จัดทำ/ผู้อนุมัติ snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT | Strike | ก่อน UAT |
| OQ-03 | อายุค้าง/มูลค่า/งวด + เกณฑ์ค้างนาน (PurchaseConfig) (DEC-15) | ลูกค้า + พี่เบิร์ด | Phase 2 |
| OQ-04 | เมื่อ PR/PO/Supplier ขึ้นระบบ → search-select + ดึงรายการค้าง | พี่เบิร์ด | – |
| OQ-05 | role-mgr-pur resolve ตามหน่วยงานผู้จัดทำ (relative) · admin ระดับฝ่าย | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-06 | รหัสฟอร์ม/Rev ที่ถูกต้อง (FM-PUR-003 vs FM-PUR-03 · Rev.02 vs Rev.00) (DEC-12) | ลูกค้า | ก่อน UAT |
| OQ-07 | "วันที่รับ" = กำหนดรับ หรือรับจริง (DEC-13) | ลูกค้า | – |
| OQ-08 | รายการ > 24 แถว / ข้อความยาว → แบบพิมพ์เพิ่มหน้า? | Strike | – |
| OQ-09 | function_code taxonomy · รหัส feature จริง | Strike | ก่อน register |

## §0.9 Glossary
PR = คำขอซื้อ · PO = ใบสั่งซื้อ · ค้างนาน = PR ที่ยังไม่ออก PO หรือ PO ที่ยังไม่ได้รับสินค้า/บริการ ณ วันที่รายงาน · รายงาน = 1 ผู้จัดทำ × 1 วันที่รายงาน × 1 หน่วยงาน

## §0.12 Coverage Manifest
| แหล่ง | รายการ | ครอบคลุมที่ |
|---|---|---|
| ช่องในฟอร์ม (FORM_SPEC 17) | วันที่รายงาน F01 · หน่วยงาน F02 · ผู้จัดทำรายงาน F03 · ตำแหน่ง F04 · ลำดับ/เลขที่ PR/เลขที่ PO/วันที่สั่งซื้อ/วันที่รับ/ผู้ผลิต/รายละเอียด/จำนวนสั่งซื้อ/หน่วย/ฝ่าย-แผนก/สาเหตุคงค้าง/สถานะปัจจุบัน/แนวทางการแก้ไข (F05–F17) | 01 §1.2 · 04 §4.2 |
| ค่าคงที่ | เกณฑ์ "ค้างนาน" (ไม่มีบนกระดาษ) → PurchaseConfig.outstanding_days (เสนอ) | 05 BR-08 |
| ลายเซ็น | ผู้จัดทำ · ผู้มีอำนาจอนุมัติ | 03 FN-09 · 05 BR-13 |
| Doc No./Rev. | FM-PUR-03 · Rev. 02 : 16/6/2026 (กระดาษพิมพ์ FM-PUR-003) | print_config (F-DOCCFG) · DEC-12 |
| DEC | 16 ข้อ | 07 §7.0 |
