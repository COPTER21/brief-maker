# 00_OVERVIEW — F-TMP-008 หนังสือยินยอมในการเก็บรวบรวม ใช้ และเปิดเผยข้อมูลส่วนบุคคล (Personal Data Consent)

## §0.1 Document Control
| | |
|---|---|
| Feature | F-TMP-008 *(รหัสชั่วคราว)* · module HR (กำกับดูแลร่วมกับ Policy Center › PDPA) |
| คำขอ | REQ-TMP-008 *(รหัสชั่วคราว)* |
| Variant | STANDARD |
| Upstream | BRD_F-TMP-008.md (APPROVED · AI-DEFAULT) · feature.html · FORM_SPEC.json · DECISIONS.lock.json |
| แบบพิมพ์ | FM-HRM-31 Rev. 00 : 01/07/2569 · โหมด Replica (thai-doc-pdf-generator v2.1) |
| รหัสเอกสาร | PDC (F-DOCCFG) |

## §0.2 Revision History
| v | วันที่ | สาระ |
|---|---|---|
| v1.0 | 2026-10-07 | ฉบับแรก (Mode 0 — prebrief-to-devpack v2 · โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
list · wizard 3 ขั้น · view 4 แท็บ · ยืนยันความยินยอม · ถอนความยินยอม · แบบพิมพ์ Replica + PDF · เอกสารแนบ · ส่งออก CSV · สิทธิ์การมองเห็น
### Out of Scope
การบังคับใช้ผลความยินยอมกับ module อื่น (DEC-02) · การแก้ถ้อยคำ/ออกฉบับใหม่ของหนังสือ · ความยินยอมของลูกค้า/คู่ค้า · ลายมือชื่อแบบภาพ

## §0.4 Roles (COSO)
`เจ้าของข้อมูลส่วนบุคคล` (ผู้ให้ความยินยอม) · `role-mgr-hr` (ผู้ดูแลงานบุคคล) · `role-compliance` (ผู้กำกับดูแล) · ผู้พิจารณาตาม DOA (0 ขั้นในรอบนี้ · DEC-03)

## §0.5 Dependencies
### Upstream
- Organization (ชื่อบริษัท · โลโก้ · ลิงก์นโยบายความเป็นส่วนตัว) — อ่านอย่างเดียว snapshot ตอนออกเลข
- ConsentPurpose master ของฉบับ (รายการและถ้อยคำความยินยอม) — ผูกกับ revision ของหนังสือ
- ทะเบียนบุคลากร/ผู้สมัครงาน (ชื่อ · ตำแหน่ง · หน่วยงาน) — **ยังไม่มีรหัส feature ในทะเบียน → OQ-07**
### Downstream
- Policy Center › PDPA / Audit (อ่านหลักฐานความยินยอม) · HR › Recruit/Onboard/Attendance (รอบนี้ยังไม่ผูก · DEC-02)
### External
- `ENG-DOC-NUM` (เลขที่) · `ENG-DOC-STORE` (สำเนา PDF) · `ENG-NOTIFY` (แจ้งเตือน) · DOA engine (F-DLG-001) · Document Center (ไฟล์แนบ)

## §0.6 Stack
CUBE NATIVE · vanilla JS SPA (prototype) · แบบพิมพ์ render จาก template logic-less เดียวกันทั้ง FE และ server

## §0.7 Multi-Tenant & Security
ข้อมูลผูกบริษัท (tenant) · row-level scope ตาม §5.3 · การเข้าดูข้อมูลอ่อนไหวต้องบันทึก audit

### §0.7.1 Data Classification Summary
ระดับสูงสุดที่ feature แตะ = **Restricted** (ความยินยอมต่อข้อมูลสุขภาพ · ศาสนา · ชีวภาพ · ประวัติอาชญากรรม — PDPA ม.26 · DEC-15)

## §0.8 Open Questions
OQ-01 ผู้สมัครกรอกเองหรือเจ้าหน้าที่บันทึกแทน · OQ-02 มติทุกข้อยังเป็น AI-DEFAULT รอใบเซ็น · OQ-03 ผลของการไม่ยินยอมข้อมูลชีวภาพต่อระบบบันทึกเวลา · OQ-04 นำกระดาษเดิมเข้าระบบย้อนหลัง · OQ-05 ถ้อยคำข้อสุดท้ายอ้างทับตัวเอง (DEC-11) · OQ-06 คำสะกดในต้นฉบับ (DEC-12) · OQ-07 รหัส feature/REQ จริง · OQ-08 function_code / taxonomy_def_id ของ mdoc

## §0.9 Glossary
| คำ | ความหมาย |
|---|---|
| เจ้าของข้อมูลส่วนบุคคล | ผู้สมัครงานหรือบุคลากรที่ให้ความยินยอม |
| ฉบับของหนังสือ (revision) | เวอร์ชันถ้อยคำของหนังสือยินยอม ผูกกับ F-DOCCFG |
| ความยินยอมที่ยังมีผล | ข้อที่เลือก "ยินยอม" และยังไม่ถูกถอน |
| ถอนความยินยอม | การใช้สิทธิของเจ้าของข้อมูลให้หยุดประมวลผลข้อมูลที่ให้ความยินยอมไว้ |

## §0.10 Pack Navigation
ดู INDEX.md

## §0.12 Coverage Manifest
| ที่มา (BRD) | ไปอยู่ที่ |
|---|---|
| §2.1 In Scope 1-6 | 01_UI §1.1-§1.2 · 02_API §2.1 |
| §5 Data | 04_DB §4.2 · §4.5 |
| §7 Status & Lifecycle | 05_RULES §5.2 |
| §8 Business Rules BR-01..BR-08 | 05_RULES §5.1 |
| §9 Edge Cases EC-01..EC-07 | 05_RULES §5.5 · 06_TESTS §6.1 |
| §10 Value Stream | 02_API §2.X · 05_RULES §5.8 |
| §12 Dev Summary 1-7 | 03_LOGIC · 04_DB · 05_RULES |
| §13 Open Questions | 07 §7.3 |
| §14 Security | 04_DB §4.6 · 05_RULES §5.7 |
