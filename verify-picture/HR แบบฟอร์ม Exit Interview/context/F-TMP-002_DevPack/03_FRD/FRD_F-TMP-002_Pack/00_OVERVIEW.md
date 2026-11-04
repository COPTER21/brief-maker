# 00_OVERVIEW — F-TMP-002 แบบสอบถามบุคลากรที่พ้นจากงาน (Exit Interview)

## §0.1 Document Control
| รายการ | ค่า |
|---|---|
| Feature | F-TMP-002 (ชั่วคราว) · HR · Offboard |
| Request | REQ-TMP-002 (ชั่วคราว) |
| แบบฟอร์ม | FM-HRM-06 Rev. 00 : 01/07/2569 |
| Generator | frd-generator-v6 (Input Mode 0 · Lane Mode) |
| Upstream | BRD_F-TMP-002 v1.0 (APPROVED) · DECISIONS.lock (17 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4) |
| Variant | STANDARD |

## §0.2 Revision History
| ver | date | by | note |
|---|---|---|---|
| v1.0 | 2026-10-08 | AI (unattended) | ฉบับแรก |

## §0.3 Scope
### In Scope
- รายการ · wizard 3 ขั้น · ดู 4 แท็บ · ส่ง · ยกเลิก · CSV · แนบไฟล์ · แบบพิมพ์ FM-HRM-06 · เลข EXI · แจ้งเตือน 2 event
### Out of Scope
- เปลี่ยนสถานะพนักงาน (DEC-01) · ส่งต่อระบบอื่น (DEC-02) · สายอนุมัติค่าเริ่ม (DEC-03) · ทำซ้ำ/ประกาศ (DEC-11) · dashboard

## §0.4 Roles (COSO)
| role | ใคร | COSO |
|---|---|---|
| owner | ผู้สร้างเอกสาร (ผู้ให้ข้อมูล หรือ HR ที่สร้างแทน) | Maker |
| informant | ผู้ให้ข้อมูล (employee_id) | Maker (ดูได้) |
| `role-mgr-hr` | admin role ของหน่วยงานเจ้าของเอกสาร | Checker |
| DOA step (optional) | ตั้งที่ DOA กลาง — ค่าเริ่ม 0 ขั้น | Approver |

## §0.5 Dependencies
### Upstream
- F-EMP-001 Employee (full_name, employee_code, birth_date, hire_date, employment_type, probation_status, education, contract_end_date) — อ่านอย่างเดียว
- F-ORG-001 OrgUnit / Position — ฝ่าย · แผนก · ตำแหน่ง
- Organization — header_snapshot (ชื่อบริษัท · โลโก้)
- F-DOCCFG (doc_type EXI) · ENG-DOC-NUM · ENG-DOC-STORE · Document Center · ENG-NOTIFY · DOA กลาง (F-DLG-001)
### Downstream
- ไม่มี (DEC-02) — event exi_submitted / exi_cancelled ผ่าน ENG-NOTIFY
### External
- ไม่มี

## §0.6 Stack
- ตามมาตรฐาน CUBE (API REST · Postgres · RLS tenant) · Prototype = html-generator-v9.4 single-file · แบบพิมพ์ thai-doc v2.1 (logic-less template + parity)

## §0.7 Multi-Tenant & Security
- ทุกตารางมี tenant_id + RLS · สิทธิ์ตาม 05 §5.3 · ใบที่ไม่มีสิทธิ์ = 404
### §0.7.1 Data Classification Summary
| ข้อมูล | Class |
|---|---|
| ชื่อ-นามสกุล · อายุตัว | Confidential·PII |
| คะแนน/ปัจจัย/ข้อเสนอแนะ | Confidential (ความเห็นต่อผู้บังคับบัญชา) |
| เลขที่ · สถานะ · วันที่ | Internal |

## §0.8 Open Questions
| OQ | คำถาม |
|---|---|
| OQ-01 | ลูกค้ายืนยัน DEC AI-DEFAULT 11 ข้อ (ใบลงนาม) ก่อน UAT |
| OQ-02 | ต้องการขั้น "HR รับทราบ" ที่ DOA กลางหรือไม่ |
| OQ-03 | ตัวชี้วัด |
| OQ-04 | function_code Taxonomy ของ EXI (F01 ชั่วคราว) |
| OQ-05 | รหัส feature จริง + เลข REQ จริง |

## §0.9 Glossary
- ผู้ให้ข้อมูล = พนักงานที่พ้นจากงาน · ref_date = วันที่ลาออก หรือวันสิ้นสุดสัญญา · EXI = รหัสเอกสาร

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED · INDEX · declarations/

## §0.12 Coverage Manifest
| BRD | FRD |
|---|---|
| §2.4 DEC-01..17 | 07 §7.0 |
| §4 Journey | 01 §1.3 |
| §5 Data | 04 §4.2 |
| §6 US-01..11 | 06 §6.1 |
| §7 Status | 05 §5.2 |
| §8 BR-01..10 | 05 §5.1 |
| §9 EC-01..09 | 05 §5.5 |
| §14 Security | 00 §0.7 · 05 §5.3 |
