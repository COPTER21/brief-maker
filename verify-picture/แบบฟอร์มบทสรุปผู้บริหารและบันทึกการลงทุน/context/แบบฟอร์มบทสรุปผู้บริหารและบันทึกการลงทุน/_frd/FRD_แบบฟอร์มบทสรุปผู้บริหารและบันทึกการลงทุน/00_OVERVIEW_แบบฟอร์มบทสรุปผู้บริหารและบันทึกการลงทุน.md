# 00_OVERVIEW — F-TMP-005 แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน (Executive Summary & Investment Memo)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-005 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2 · โหมดไม่เฝ้า) |
| Variant | **FULL** (pages=3, states=4, approval=Y, repeat=Y) |
| Source | BRD-TMP-005-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-005_v2 · FORM_SPEC FM-BDM-05 · DECISIONS.lock (16 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · e2e 21/21) |
| Module / Area | Business Development (ฝ่ายพัฒนาธุรกิจ) |
| Status | Ready for Dev (หลัง OQ-03/04/06 ปิด · ลูกค้ายืนยัน AI-DEFAULT ก่อน UAT) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · ข้อมูลสรุปโครงการ/การลงทุน 4 ช่อง · บทสรุปผู้บริหาร 13 หัวข้อ · เอกสารและเงื่อนไขประกอบ (ไม่จำกัดแถว) · DOA 2 ขั้น · ไม่ผ่าน→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-BDM-05 Replica 2 หน้า · เลข IVM · CSV · แจ้งเตือนเงื่อนไขค้างหลังอนุมัติ
### Out of Scope
ผูกโครงการ FM-BDM-01/03 · ส่งต่อ FM-BDM-06 (OQ-05) · สร้างงบลงทุน · matrix อนุมัติตามวงเงิน (ตั้งที่ DOA กลาง · OQ-06) · หน้าตั้งค่า InvestmentMemo · ทำซ้ำ · ประกาศ · เตือนเงื่อนไขใกล้กำหนด · ส่งต่อระบบอื่น (DEC-02)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ (ผู้เชี่ยวชาญด้านพัฒนาธุรกิจ / ผู้รับผิดชอบที่ได้รับมอบหมาย) | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายพัฒนาธุรกิจ / รองกรรมการผู้จัดการ) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (กรรมการผู้จัดการ / ผู้มีอำนาจตามตารางอำนาจอนุมัติ) | Approver | role-gm (ชั่วคราว · OQ-03) |
| admin ฝ่ายพัฒนาธุรกิจ | Monitor · เห็นทั้งหมด · ยกเลิกได้ | admin_role |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน — ผู้จัดทำ/ผู้เสนอ/ผู้รับผิดชอบเงื่อนไข) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve · amount) · F-DOCCFG/F003 (doc_type IVM · status · print_config · form_revisions) · InvestmentMemo config (condition_statuses) · Company Master (logo/header)
### Downstream
ENG-NOTIFY (ivm_cancelled · ivm_approved_open_conditions) · ENG-DOC-STORE (approved_final) · Report area (อ่าน · Phase 2)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/investment-memo` (อ้าง feature.html เป็น source of truth) · BE: REST `/api/v1/investment-memos` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less · 2 หน้า) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เอกสาร/บทสรุป/ข้อมูลการลงทุน (อ่อนไหวทางธุรกิจ) · Confidential(PII): ชื่อผู้จัดทำ/ผู้เสนอ/ผู้รับผิดชอบ/ผู้พิจารณา snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) + เงื่อนไขค้าง = เตือนไม่บล็อก | Strike | ก่อน UAT |
| OQ-03 | role กรรมการผู้จัดการ/ผู้มีอำนาจตามตาราง ไม่มีใน DOA master (ใช้ role-gm ชั่วคราว) · ผู้ตรวจสอบ "รองกรรมการผู้จัดการ" ไม่มี role | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | InvestmentMemo config มีหรือยัง / เจ้าของ | พี่เบิร์ด | ก่อน dev |
| OQ-05 | ผูกกับโครงการ FM-BDM-01 / ผลคัดกรอง FM-BDM-03 / ส่งต่อ FM-BDM-06 ไหม | ลูกค้า | – |
| OQ-06 | ตารางอำนาจอนุมัติตามวงเงิน (ตั้งที่ DOA กลาง) | ลูกค้า | ก่อน wire |
| OQ-07 | เงื่อนไขเกิน 20 แถว → PDF หน้า 3 ได้ไหม | ลูกค้า | – |
| OQ-08 | รหัส IVM ชนไหม · taxonomy function_code | Strike | ก่อน register |

## §0.9 Glossary
บทสรุปผู้บริหาร = Executive Summary เสนอผู้บริหารตัดสินใจ (ขั้นตอนที่ 5) · เงื่อนไขค้าง = เอกสาร/เงื่อนไขประกอบที่สถานะยังไม่ "แล้วเสร็จ" · สถานะเงื่อนไข = ข้อมูลในเอกสาร ไม่ใช่สถานะเอกสาร

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F23 (FORM_SPEC) | project_name · project_type · proposer · estimated_amount · decision_requested · project_summary · strategic_rationale · market_opportunity · business_model · implementation_plan · financial_analysis · investment_framework · key_risks · alternatives · pre_approval_conditions · bd_recommendation · next_steps · seq · item · owner · due_date · status · remark | 01 §1.2 P-02 · 04 §4.2 · 03 FN-01/FN-08 |
| ค่าคงที่บนกระดาษ 2 ชุด | สถานะเงื่อนไข 4 ค่า · ผู้อนุมัติตามตารางอำนาจอนุมัติ | InvestmentMemo config · DOA กลาง · 03 FN-01/04/08 · 05 BR-06/07 |
| ลายเซ็น S1–S3 | ผู้จัดทำ + DOA 2 ขั้น | 03 FN-04/05/08 · 05 BR-11 |
| BRD S-01..S-09 | stories | 06 AC-01..AC-13 |
| BRD BR-01..13 · VR-01..07 · EC-01..11 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..16 | มติ | 07 §7.0 |
| declaration | DOA · NTF · DOCCFG · MDOC | declarations/ · 03 FN-03/05/07/09 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..05 | 01 §1.1 |
ไม่มี requirement หล่น
