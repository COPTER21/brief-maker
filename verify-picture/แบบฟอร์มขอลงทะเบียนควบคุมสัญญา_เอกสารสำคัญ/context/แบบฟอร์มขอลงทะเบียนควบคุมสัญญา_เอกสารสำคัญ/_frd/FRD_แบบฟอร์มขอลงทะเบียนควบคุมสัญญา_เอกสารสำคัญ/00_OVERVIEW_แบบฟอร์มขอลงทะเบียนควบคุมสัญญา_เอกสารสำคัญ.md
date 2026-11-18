# 00_OVERVIEW — F-TMP-009 แบบฟอร์มขอลงทะเบียนควบคุมสัญญา/เอกสารสำคัญ
> frd-generator-v6 · Input Mode 0 (PREBRIEF v2 + FORM_SPEC + DECISIONS.lock + BRD_F-TMP-009 + feature.html) · โหมดไม่เฝ้า — มติทั้งหมด AI-DEFAULT รอลูกค้ายืนยัน (OQ-02)

## §0.1 Scope
- เอกสารคำขอลงทะเบียนควบคุมสัญญา/เอกสารสำคัญ (Q-form) ตามแบบฟอร์มลูกค้า FM-AGM-01 Rev.00 : 01/07/2569 — ช่อง 1:1 (DEC-06)
- สายพิจารณา DOA dynamic ค่าเริ่ม 2 ขั้น (หัวหน้า/ผู้จัดการ → ผู้เชี่ยวชาญด้านบริหารสัญญา "รับทราบ") (DEC-03)
- ผู้ดูแลสัญญาลงทะเบียนควบคุม (ออกเลขทะเบียน) + บันทึกวันที่ได้รับต้นฉบับ/คู่ฉบับ
- PDF Replica FM-AGM-01 (thai-doc v2.2) · แนบไฟล์ · CSV
- Out: contract repository · แจ้งหมดอายุ · อ้างทะเบียนเดิม (OQ-04) · ทำซ้ำ (DEC-11)

## §0.2 Roles
| Role | ทำอะไร |
|---|---|
| ผู้รับผิดชอบ (Maker) | สร้าง/แก้ร่าง · ส่ง · ยกเลิกของตน |
| role-line-manager | ขั้น 1 อนุมัติ/ไม่อนุมัติ |
| role-compliance (ชั่วคราว = ผู้เชี่ยวชาญด้านบริหารสัญญา · OQ-03) | ขั้น 2 รับทราบ/ส่งกลับแก้ไข |
| ผู้ดูแลสัญญา (admin ฝ่ายบริหารสัญญา) | ลงทะเบียน · รับต้นฉบับ · เห็นทั้งหมด · ยกเลิก |

## §0.3 Dependencies
F-EMP-001 (ผู้ขอ/ตำแหน่ง) · F-ORG-001 (หน่วยงาน · ผู้บังคับบัญชา) · F-DLG-001 DOA กลาง · F-DOCCFG + ENG-DOC-NUM/ENG-DOC-STORE · ENG-NOTIFY · Document Center · F185 Master Document (MDOC)

## §0.4 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC · OQ-03 role ผู้เชี่ยวชาญด้านบริหารสัญญา (ไม่มีใน DOA master) · OQ-04 อ้างทะเบียนเดิม · OQ-05 ช่องระบุ "เอกสารสำคัญอื่นๆ" · OQ-06 รูปแบบเลขทะเบียนควบคุม · OQ-07 module AGM + taxonomy

## §0.5 Coverage Manifest
| FORM_SPEC | ที่อยู่ใน FRD |
|---|---|
| F01 วันที่ | 04 req_date · 03 FN-03 |
| F02 แก้ไข/เปลี่ยนแปลง ระบุสาเหตุ | 04 change_reason · 05 BR-02 VR-03 |
| F03 ชื่อคู่สัญญา | 04 counterparty_name · VR-04 |
| F04/F05 วันที่เริ่มต้นและสิ้นสุดสัญญา | 04 contract_start/contract_end · BR-03 VR-05 |
| F06 หน่วยงานเจ้าของสัญญา | 04 owner_unit_id/owner_unit_snapshot · BR-04 |
| F07 ทะเบียนควบคุมเลขที่ | 04 register_no · FN-07 |
| F08 ได้รับต้นฉบับ…วันที่ | 04 original_received_date · FN-08 |
| choices contract_type (8) · purpose (5) | 04 contract_type · purpose · BR-01 |
| S1–S3 ลายเซ็น | 04 approval_chain · FN-09 sign_rows · BR-12 |
| control FM-AGM-01 Rev.00 | print_config · DOCCFG_BRIEF |
