# 00_OVERVIEW — F-TMP-006 แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร (Data Room Index and Document Control Register · IVMD)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-006 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=4, approval=Y, money=N) |
| Source | BRD-IVM-IVMD-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-006_v2 · FORM_SPEC FM-IVM-04 · DECISIONS.lock (22 DEC · AI-DEFAULT 14) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · smoke 46/46 · jsdom 26/26 · NO-BROWSER) |
| Module / Area | ฝ่ายบริหารการลงทุน (Investment) · Core Cube (Operation) |
| Status | Ready for Dev (หลัง OQ-03/04/06/08 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (4 ขั้น) · ดู 4 แท็บ · ชื่อโครงการ / ธุรกรรม · โครงสร้างโฟลเดอร์ห้องข้อมูล 6 คอลัมน์ (ตั้งต้น 8 โฟลเดอร์จาก config) · มาตรฐานการตั้งชื่อไฟล์ (อ่านจาก config) · ทะเบียนสถานะเอกสารและประวัติฉบับ 10 คอลัมน์ · การเปลี่ยนแปลงเอกสาร 10 คอลัมน์ · บันทึกสิทธิการเข้าถึงข้อมูล 10 คอลัมน์ · รหัส D-/CH-/ลำดับ ระบบรัน · ชื่อไฟล์ตามมาตรฐาน · DOA 2 ขั้น · ส่งกลับ→กลับร่าง · ยกเลิก · แนบไฟล์ · PDF FM-IVM-04 Replica 2 หน้า · เลข IVMD · CSV
### Out of Scope
สร้าง/ถอนสิทธิจริงในไดรฟ์ (บันทึกเป็นทะเบียน · DEC-01/02) · ตรวจชื่อไฟล์จริงในไดรฟ์ · ทะเบียนโครงการ / FM-IVM-01 (ชื่อโครงการกรอกเอง) · แก้ทะเบียนหลังอนุมัติ (OQ-07) · ส่งต่อ FM-IVM-11 · ทำซ้ำเป็นฟีเจอร์ทางการ (DEC-14)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้จัดทำ | Maker | owner |
| ผู้ตรวจสอบ (ผู้จัดการฝ่ายบริหารการลงทุน) | Checker | role-line-manager |
| ผู้อนุมัติ / รับทราบ (รองกรรมการผู้จัดการ / กรรมการผู้จัดการ) | Approver | role-gm |
| admin ฝ่ายบริหารการลงทุน (ผู้ดูแลห้องข้อมูล) | Monitor · admin view | (ยังไม่มี role id — OQ-04) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type IVMD · status · print_config · revisions) · Organization (header/logo) · config FileNamingPolicy / DataRoomPolicy (อ่าน · เจ้าของ OQ-08)
### Downstream
ENG-NOTIFY (ivmd_cancelled · ivmd_register_approved) · ENG-DOC-STORE (approved_final) · FM-IVM-11 (ประกาศ event `ivmd.approved` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
ตาม CUBE Core (API REST · PostgreSQL RLS · PDF render server-side จาก template logic-less เดียวกับ prototype)

## §0.7 Open Questions
OQ-01 ตัวชี้วัด · OQ-02 ใบเซ็นยืนยัน DEC (AI-DEFAULT · รวมช่องเพิ่มชื่อโครงการ) · OQ-03 role/module ใน DOA master · OQ-04 admin role id · OQ-05 ทะเบียนโครงการ · OQ-06 รหัส IVMD/feature id/taxonomy · OQ-07 แก้ทะเบียนหลังอนุมัติ · OQ-08 เจ้าของ config FileNamingPolicy / DataRoomPolicy (รายละเอียด BRD §13)

## §0.8 Coverage Manifest
| FORM_SPEC | ที่ |
|---|---|
| F01 ชื่อโครงการ / ธุรกรรม (ช่องเพิ่ม) | 04 §4.2 project_name · 01 P-02 ขั้น 1 การ์ด ① |
| F02–F07 โครงสร้างโฟลเดอร์ห้องข้อมูล | 04 ivm_data_room_folder · 01 P-02 ขั้น 1 การ์ด ② |
| constants มาตรฐานการตั้งชื่อไฟล์ (5) + โฟลเดอร์มาตรฐาน | 04 naming_snapshot · 03 FN-12 · 01 P-02 ขั้น 1 การ์ด ③ · 05 BR-01/02 |
| F08–F17 ทะเบียนสถานะเอกสารและประวัติฉบับ | 04 ivm_data_room_document · 01 P-02 ขั้น 2 การ์ด ① |
| F18–F27 การเปลี่ยนแปลงเอกสาร | 04 ivm_data_room_change · 01 P-02 ขั้น 2 การ์ด ② |
| F28–F37 บันทึกสิทธิการเข้าถึงข้อมูล | 04 ivm_data_room_access · 01 P-02 ขั้น 3 การ์ด ① |
| S1–S3 ลายเซ็น | 03 FN-09 sign_rows · 05 BR-15 |
| control FM-IVM-04 Rev.00 | print_config · DOCCFG |
| anomalies 8 | DEC-15..22 → 05 |
