# 00_OVERVIEW — F-TMP-008 ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม (Corrective Action Request · CAR)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-008 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) · รหัส feature ชั่วคราว |
| Variant | **FULL** (fallback from BRD: pages=4, states=5, approval=Y, money=N → states ≥ 4) |
| Source | BRD-TMP-008 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-008_v2 · FORM_SPEC FM-CCC-04 (87 ช่อง) · DECISIONS.lock (35 DEC · AI-DEFAULT 28 · VALID 7) · feature.html (html-generator-v9.4 · audit FAIL 0) |
| Module / Area | Governance / Policy · แผนกบริหารองค์กร และกำกับดูแล |
| Status | Ready for Dev (หลัง OQ-02/03 ปิด) · ทุกมติ [AI-DEFAULT] รอลูกค้ายืนยันในใบลงนาม |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (แท็บ ทั้งหมด/รอฉันดำเนินการ/รายงานของฉัน · กรองสถานะ/หน่วยงาน · CSV) · สร้าง/แก้ร่าง (3 ขั้น · ช่วงการจัดทำ) · บันทึกการตรวจสอบ (IC · ช่วงการตรวจสอบ + ข้อ 10) · ลงนามตรวจสอบ 7 จุด · ส่งอนุมัติ · DOA dynamic ข้อ 12 (ค่าเริ่ม 4 ขั้น GM/AMD/ผู้จัดการฝ่าย → MD → IC → IC Mgr.) · ไม่อนุมัติ/ตีกลับ → ร่างเลขเดิม · ยกเลิก · แนบไฟล์ · PDF FM-CCC-04 Replica 2 หน้า · เลข CAR
### Out of Scope
เปลี่ยนค่าในระบบ/ส่งต่อระบบอื่น (DEC-01/02) · เชื่อมทะเบียนเอกสาร (OQ-04) · ทำซ้ำ · ประกาศ (DEC-28)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ IC (กรอกช่วงการตรวจสอบ · ส่งอนุมัติ · admin view) | Checker | role-ic-officer — **ยังไม่อยู่ใน DOA contract (OQ-03)** |
| ผู้ลงนามตรวจสอบ HOD | Checker | role-line-manager (relative) |
| ผู้ลงนามตรวจสอบ IC Mgr (4 จุด) | Checker | role-ic-mgr — **ยังไม่อยู่ใน DOA contract (OQ-03)** |
| ผู้ลงนามตรวจสอบ MD (2 จุด) | Checker | role-md — **ยังไม่อยู่ใน DOA contract (OQ-03)** |
| ผู้อนุมัติข้อ 12 (DOA 4 ขั้น) | Approver | role-line-manager → role-md → role-ic-officer → role-ic-mgr (ค่าเริ่ม · ตั้งที่ DOA กลาง) |

## §0.5 Dependencies
| สิ่งที่ใช้ | feature | ใช้ทำอะไร |
|---|---|---|
| Employee / ผังองค์กร | F-EMP-001 · F-ORG-001 | หน่วยงานผู้จัดทำ · role-line-manager |
| DOA กลาง | F-DLG-001 | สายอนุมัติข้อ 12 (DOA_BRIEF_F-TMP-008) |
| Document Configuration | F-DOCCFG | doc_type CAR · เลขรัน · print_config · status เปิดใช้ |
| Master Document | F185 | ลงทะเบียนแบบเอกสาร (MDOC_BRIEF_CAR) |
| Notification | ENG-NOTIFY | car_submitted_for_review · car_review_returned · car_cancelled |
| Document Center | ENG-DOC-STORE | ไฟล์แนบ · สำเนา PDF ตอนอนุมัติครบ |

## §0.12 Coverage Manifest
| แหล่ง | จำนวน | ครอบคลุมที่ |
|---|---|---|
| ช่องในฟอร์ม (FORM_SPEC) | 87 | 01 §1.3 · 04 §4.1–4.3 |
| แถวซ้ำ | 18 กลุ่ม | 04 §4.2 · print_config.group_min_rows |
| ลายเซ็น | 11 (ตรวจสอบ 7 + อนุมัติ 4) | 04 §4.3 · 03 FN-06/09 · PDF sign_rows |
| DEC | 35 | 07 §7.0 |
| Story | 15 | 03 FN trace (INDEX) |

## §0.13 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ยืนยัน DEC · OQ-03 role นอก DOA contract (role-md · role-ic-officer · role-ic-mgr) · OQ-04 เชื่อมทะเบียนเอกสาร · OQ-05 เกิน 2 หน้า · OQ-06 ผู้กรอก 6.3 · OQ-07 รหัสจริง
