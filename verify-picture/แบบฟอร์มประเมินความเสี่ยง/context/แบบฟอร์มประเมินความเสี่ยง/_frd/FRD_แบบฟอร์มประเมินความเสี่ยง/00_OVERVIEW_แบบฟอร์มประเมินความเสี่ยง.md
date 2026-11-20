# 00_OVERVIEW — F-TMP-002 แบบฟอร์มประเมินความเสี่ยง (Risk Assessment)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-002 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **FULL** (pages=3, states=4, approval=Y, repeat=Y) |
| Source | BRD-TMP-002-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-002_v2 · FORM_SPEC FM-BDM-02 · DECISIONS.lock (16 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · e2e 21/21) |
| Module / Area | Business Development (ฝ่ายพัฒนาธุรกิจ) |
| Status | Ready for Dev (หลัง OQ-03/04 ปิด · ลูกค้ายืนยัน AI-DEFAULT ก่อน UAT) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ทะเบียนความเสี่ยงไม่จำกัดแถว · คะแนนก่อนควบคุม = โอกาสเกิด × ผลกระทบ · ระดับตาม RiskMatrix · DOA 2 ขั้น · ไม่ผ่าน→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-BDM-02 Replica 2 หน้า · เลข RSK · CSV · แจ้งเตือนระดับสูงมาก
### Out of Scope
ผูกโครงการ FM-BDM-01 (OQ-05) · หน้าตั้งค่า RiskMatrix · ทำซ้ำ · ประกาศ · dashboard ติดตามข้ามใบ · ส่งต่อระบบอื่น (DEC-02)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (รองกรรมการผู้จัดการ / กรรมการผู้จัดการ) | Approver | role-gm (ชั่วคราว · OQ-03) |
| admin ฝ่ายพัฒนาธุรกิจ | Monitor · เห็นทั้งหมด · ยกเลิกได้ | admin_role |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type RSK · status · print_config · form_revisions) · RiskMatrix config (likelihood_scale · impact_scale · level_bands · categories) · Company Master (logo/header)
### Downstream
ENG-NOTIFY (rsk_cancelled · rsk_very_high_approved) · ENG-DOC-STORE (approved_final) · Report area (อ่าน · Phase 2)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/risk-assessment` (อ้าง feature.html เป็น source of truth) · BE: REST `/api/v1/risk-assessments` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less · 2 หน้า) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เอกสาร/ทะเบียนความเสี่ยง · Confidential(PII): ชื่อผู้จัดทำ/ผู้พิจารณา snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) | Strike | ก่อน UAT |
| OQ-03 | role รองกรรมการผู้จัดการ/กรรมการผู้จัดการ ไม่มีใน DOA master (ใช้ role-gm ชั่วคราว) · "ตามความเหมาะสม" | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | RiskMatrix config มีหรือยัง / เจ้าของ | พี่เบิร์ด | ก่อน dev |
| OQ-05 | ผูกกับโครงการ FM-BDM-01 ไหม | ลูกค้า | – |
| OQ-06 | รหัส RSK ชนไหม · taxonomy function_code | Strike | ก่อน register |

## §0.9 Glossary
คะแนนก่อนควบคุม (inherent) = โอกาสเกิด × ผลกระทบ ก่อนมีมาตรการ · คะแนนคงเหลือ (residual) = คะแนนหลังมาตรการควบคุม · ระดับ = ช่วงคะแนนตาม RiskMatrix

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F10 (FORM_SPEC) | seq · category · description · cause_effect · likelihood · impact · inherent_score · control_measure · residual_score · status | 01 §1.2 P-02 · 04 §4.2 · 03 FN-02/FN-08 |
| ค่าคงที่บนกระดาษ 3 ชุด | เกณฑ์ 1–5 · ช่วงระดับ · ประเภท | RiskMatrix config · 03 FN-02/08 · 05 BR-06 |
| ลายเซ็น S1–S3 | ผู้จัดทำ + DOA 2 ขั้น | 03 FN-04/05/08 · 05 BR-11 |
| BRD S-01..S-09 | stories | 06 AC-01..AC-13 |
| BRD BR-01..12 · VR-01..04 · EC-01..08 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..16 | มติ | 07 §7.0 |
| declaration | DOA · NTF · DOCCFG · MDOC | declarations/ · 03 FN-03/05/07/09 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..05 | 01 §1.1 |
ไม่มี requirement หล่น
