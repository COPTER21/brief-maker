# 00_OVERVIEW — F-TMP-004 แบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี (Annual Vendor/Service Provider Evaluation and Selection)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-004 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (fallback from BRD: pages=3, states=5, approval=Y, print=Y) |
| Source | BRD-PUR-VEV-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-004_v2 · FORM_SPEC FM-PUR-01 · DECISIONS.lock (17 DEC) · feature.html (html-generator-v9.4 · audit FAIL 0 · jsdom smoke 38/38 · [NO-BROWSER] e2e ยังไม่รัน) |
| Module / Area | Purchase · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-04/05 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (segmented · ค้นหา · กรองสถานะ/ผลประเมิน · CSV) · สร้าง/แก้ไข (wizard 3 ขั้น: ผู้ขาย · คะแนน 4 หัวข้อ · มาตรฐาน · ความคิดเห็น) · คะแนนรวม + สรุปผลคำนวณ · ดู 4 แท็บ · DOA dynamic (ค่าเริ่ม 2 ขั้น + ผู้บริหารเมื่อไม่ผ่าน) · ไม่เห็นด้วย/ไม่อนุมัติ→ร่างเลขเดิม · ยกเลิก · แนบไฟล์ · แจ้งผู้ขายไม่ผ่าน · เตือนประเมินซ้ำในปี · PDF FM-PUR-01 Replica 2 หน้า · เลข VEV
### Out of Scope
Vendor master / อัปเดตสถานะผู้ขาย AVL (OQ-03 · DEC-02) · ดึงคะแนนจาก PO/GRN · หน้าตั้งค่าเกณฑ์ (OQ-04) · ทำซ้ำ (DEC-11 · OQ-07) · ประกาศ

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้ประเมิน (Evaluated by) | Maker | owner |
| ผู้จัดทำ (แผนกจัดซื้อ) | Checker (เห็นด้วย/ไม่เห็นด้วย) | role-pur-officer ⚠ ไม่อยู่ใน DOA master (OQ-05) |
| ผู้จัดการแผนกจัดซื้อ | Approver · Admin view · ยกเลิกได้ | role-mgr-pur |
| ผู้บริหาร (เฉพาะผลไม่ผ่าน) | Approver | role-gm (ค่าเสนอ · OQ-05) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (Organization · หัวกระดาษ) · F-DLG-001 DOA (resolve role-pur-officer/role-mgr-pur · เงื่อนไขผลไม่ผ่าน → role-gm — TODO: DOA engine) · F-DOCCFG/F003 (doc_type VEV · status · print_config) · VendorEvaluationConfig (หัวข้อ/คะแนนเต็ม/เกณฑ์ผ่าน/มาตรฐาน — ใหม่ · OQ-04)
### Downstream
ENG-NOTIFY (vev_evaluation_failed · vev_cancelled) · ENG-DOC-STORE (approved_final) · Master › Supplier/Vendor (ประกาศ event `vev.evaluation_approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/vendor-evaluation` (feature.html = source of truth) · BE: REST `/api/v1/vendor-evaluations` · PDF render ฝั่ง server จาก `print/form.tpl.html` (logic-less) + data contract (03 FN-09)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: คะแนน/ผล/ข้อมูลผู้ขาย (นิติบุคคล) · Confidential(PII): ชื่อผู้ประเมิน/ผู้อนุมัติ snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT | Strike | ก่อน UAT |
| OQ-03 | Vendor master + อัปเดตสถานะ AVL ตามผล | ลูกค้า + พี่เบิร์ด | Phase 2 |
| OQ-04 | VendorEvaluationConfig อยู่ที่ไหน (Purchase Configuration?) | พี่เบิร์ด | ก่อน dev |
| OQ-05 | role-pur-officer นอก DOA master · DOA เงื่อนไขตามผล (ไม่ใช่วงเงิน) · ผู้บริหาร = role-gm หรือ role-proc-dir | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-06 | หัวคอลัมน์ "คะแนนเฉลี่ย" → "คะแนนเต็ม"? · ฝ่าย/แผนกจัดซื้อ | ลูกค้า | – |
| OQ-07 | ปุ่มทำซ้ำของ archetype ขัด DEC-11 | Strike | – |
| OQ-08 | function_code taxonomy · รหัส feature จริง | Strike | ก่อน register |

## §0.9 Glossary
คะแนนเฉลี่ย (บนกระดาษ) = คะแนนเต็มของหัวข้อ (DEC-12) · ผ่าน (Pass) = คะแนนรวม ≥ pass_threshold · ไม่ผ่าน (Fail, Non qualified) = < pass_threshold · AVL = Approved Vendor List

## §0.12 Coverage Manifest
| แหล่ง | รายการ | ครอบคลุมที่ |
|---|---|---|
| ช่องในฟอร์ม (FORM_SPEC 16) | ผู้ขาย F01/F02 · สินค้า/บริการ F03/F04 · อ้างอิง/เครดิต F05/F06 · หัวข้อ/คะแนนเฉลี่ย/คะแนนที่ได้ F07–F09 · รวม F10/F11 · อื่นๆ F12 · สรุปผล F13 · ความคิดเห็น F14 · ผู้ประเมิน/Date F15/F16 | 01 §1.2 · 04 §4.2 |
| ตัวเลือก | supply_type (goods/service) · certifications (8) · eval_result (pass/fail) · เห็นด้วย/ไม่เห็นด้วย · อนุมัติ/ไม่อนุมัติ | 01 · 04 · 05 BR-14 |
| ลายเซ็น | ผู้ประเมิน · ผู้จัดทำ (แผนกจัดซื้อ) · อนุมัติ (ผู้จัดการแผนกจัดซื้อ) (+ผู้บริหาร) | 03 FN-09 · 05 BR-14 |
| Doc No./Rev. | FM-PUR-01 · REV.00 : 01/07/2569 | print_config (F-DOCCFG) |
| DEC | 17 ข้อ | 07 §7.0 |
