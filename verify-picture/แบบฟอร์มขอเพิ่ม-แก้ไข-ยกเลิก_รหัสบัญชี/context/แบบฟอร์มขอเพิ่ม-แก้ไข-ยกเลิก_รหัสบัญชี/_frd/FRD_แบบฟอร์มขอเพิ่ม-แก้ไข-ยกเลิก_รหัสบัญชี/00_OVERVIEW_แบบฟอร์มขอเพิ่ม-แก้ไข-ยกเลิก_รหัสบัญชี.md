# 00_OVERVIEW — F-TMP-003 แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี (Account Code Request)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-003 v1.0 · frd-generator-v6 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=5, approval=Y, money=N) |
| Source | BRD-ACC-ACR-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-003_v2 · FORM_SPEC FM-ACC-01 · DECISIONS.lock (14 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · e2e_standard 21/21 บน Chromium ใน container) |
| Module / Area | Accounting · Core Cube (ใกล้เคียง COA — ยังไม่มี BA artifact) |
| Status | Ready for Dev (หลัง OQ-03/04/06 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ประเภทคำขอ เพิ่ม/แก้ไข/ยกเลิก (เลือก 1) · ชื่อบัญชีที่ขอเพิ่มไม่จำกัดบรรทัด · DOA dynamic (ค่าเริ่ม 2 ขั้น ผู้ตรวจสอบ › ผู้อนุมัติ) · ไม่อนุมัติ→กลับร่าง · ยกเลิก · บันทึกเข้าระบบแล้ว (admin ฝ่ายบัญชี) · แนบไฟล์ · PDF FM-ACC-01 Replica · เลข ACR · CSV
### Out of Scope
แก้ COA อัตโนมัติ (DEC-01) · ส่งต่อระบบอื่น (DEC-02) · ตรวจรหัสบัญชีกับ COA (OQ-04) · ทำซ้ำ · ประกาศ

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้ขอเพิ่ม/แก้ไข/ยกเลิกรหัสบัญชี (พนักงาน) | Maker | owner |
| ผู้ตรวจสอบ | Checker | role-line-manager (ค่าเริ่ม DOA ขั้น 1 · relative role จากผังองค์กร) |
| ผู้อนุมัติ | Approver | role-mgr-acc (ค่าเริ่ม DOA ขั้น 2 · module accounting) |
| ผู้บันทึกเข้าระบบ (admin ฝ่ายบัญชี) | Executor · ดูทุกใบ | role ใหม่ — ยังไม่อยู่ใน DOA master (OQ-03) |

## §0.5 Dependencies
### Upstream
HR · Employee (ชื่อ/ตำแหน่ง · อ่าน) · Organization (Department · Company header/logo · ผังผู้บังคับบัญชา) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type ACR · status · print_config)
### Downstream
ENG-NOTIFY (acr_cancelled · acr_ready_to_record · acr_recorded) · ENG-DOC-STORE (approved_final) · COA (ประกาศ event `acr.approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/account-code-request` (feature.html = source of truth) · BE: REST `/api/v1/account-code-requests` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เอกสาร/รหัสบัญชี · Confidential(PII): ชื่อผู้ขอ/ผู้ลงนาม/ผู้บันทึก snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) | Strike | ก่อน UAT |
| OQ-03 | role admin ฝ่ายบัญชี (ผู้บันทึกเข้าระบบ) + role-line-manager ยังไม่อยู่ใน DOA master | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | COA field (code/name) · ตรวจรหัสมีจริง/ซ้ำ · เลือกจาก COA | พี่เบิร์ด | ก่อน dev |
| OQ-05 | SoD ผู้บันทึกเข้าระบบ ≠ ผู้อนุมัติ ไหม | ลูกค้า | – |
| OQ-06 | รหัส feature/REQ จริง · taxonomy function_code | Strike | ก่อน register |

## §0.9 Glossary
ประเภทคำขอ = ☐ เพิ่ม/แก้ไข/ยกเลิกรหัสบัญชี · ผู้ตรวจสอบ = ขั้น DOA แรก · ผู้บันทึกเข้าระบบ = ผู้แก้ผังบัญชีจริงแล้วยืนยันในใบ

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F13 (FORM_SPEC) | doc_no · req_date · request_type · add_lines[].account_name · add.purpose · edit.account_code/change_to/purpose · cancel.account_code/account_name/purpose · approval.reject_reason · approval.approved_at · posting.recorded_at | 01 §1.2 · 04 §4.2 · 03 FN-01/FN-08 |
| ลายเซ็น S1–S4 | ผู้ขอ · ผู้ตรวจสอบ (DOA) · ผู้อนุมัติ (DOA) · ผู้บันทึกเข้าระบบ | 03 FN-04/05/08/11 · 04 recorded_* |
| BRD S-01..S-14 | stories | 06 AC-01..AC-15 |
| BRD BR-01..10 · VR-01..09 · EC-01..09 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..14 | มติ | 07 §7.0 |
| declaration | DOA · NTF · DOCCFG · MDOC | declarations/ · 03 FN-03/04/05/06/09 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..06 | 01 §1.1 |
ไม่มี requirement หล่น
