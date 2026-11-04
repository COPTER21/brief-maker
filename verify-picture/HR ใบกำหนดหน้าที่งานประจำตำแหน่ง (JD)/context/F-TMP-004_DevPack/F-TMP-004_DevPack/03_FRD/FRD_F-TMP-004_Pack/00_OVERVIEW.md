# 00_OVERVIEW — F-TMP-004 ใบกำหนดหน้าที่งานประจำตำแหน่ง (Job Description)

## §0.1 Document Control
| รายการ | ค่า |
|---|---|
| Feature | F-TMP-004 (ชั่วคราว) · HR · เรื่องคน (อ้างอิง Organization · Position & Tier) |
| Request | REQ-TMP-004 (ชั่วคราว) |
| แบบฟอร์ม | FM-HRM-32 Rev. 00 : 01/07/2569 (2 หน้า) |
| Generator | frd-generator-v6 (Input Mode 0 · Lane Mode) |
| Upstream | BRD_F-TMP-004 v1.0 (APPROVED) · DECISIONS.lock (17 DEC · AI-DEFAULT 12) · feature.html (html-generator-v9.4) |
| Variant | STANDARD |

## §0.2 Revision History
| ver | date | by | note |
|---|---|---|---|
| v1.0 | 2026-10-08 | AI (unattended) | ฉบับแรก |

## §0.3 Scope
### In Scope
- รายการ · wizard 3 ขั้น · ดู 4 แท็บ · ส่งอนุมัติ · อนุมัติ/ไม่อนุมัติ · ยกเลิก · ระบุผู้ดำรงตำแหน่ง · รับทราบ · ฉบับใหม่แทนฉบับเดิม · CSV · แนบไฟล์ · แบบพิมพ์ FM-HRM-32 · เลข JD · แจ้งเตือน 4 event
### Out of Scope
- แก้ Position master (DEC-01) · ส่งต่อ Performance/Recruit (DEC-02) · ทำซ้ำ/ประกาศ (DEC-12) · dashboard

## §0.4 Roles (COSO)
| role | ใคร | COSO |
|---|---|---|
| owner (ผู้จัดทำ) | ผู้สร้างเอกสาร | Maker |
| DOA step (ผู้อนุมัติ) | resolve จาก DOA กลาง · ค่าเริ่ม 1 ขั้น `role-line-manager` (relative role — ผู้บังคับบัญชาตรงของผู้จัดทำ) | Approver |
| incumbent (ผู้ดำรงตำแหน่ง) | acknowledged_by | Acknowledger (ไม่ใช่ขั้น DOA) |
| `role-mgr-hr` | admin role ของหน่วยงานเจ้าของเอกสาร | Checker |

## §0.5 Dependencies
### Upstream
- Organization · Position & Tier (Position.name_th, org_unit, reports_to) — อ่านอย่างเดียว
- OrgUnit (แผนก · ฝ่าย) · Employee (position_id · ผู้บังคับบัญชาตรง) — อ่านอย่างเดียว
- Organization — header_snapshot (ชื่อบริษัท · โลโก้)
- F-DOCCFG (doc_type JD) · ENG-DOC-NUM · ENG-DOC-STORE · Document Center · ENG-NOTIFY · DOA กลาง (F-DLG-001)
### Downstream
- ไม่มี (DEC-02) — event jd_acknowledged / jd_superseded ประกาศไว้ให้ Performance/Recruit ใช้ภายหลัง
### External
- ไม่มี

## §0.6 Stack
- ตามมาตรฐาน CUBE (API REST · Postgres · RLS tenant) · Prototype = html-generator-v9.4 single-file · แบบพิมพ์ thai-doc v2.1 (logic-less template + parity)

## §0.7 Multi-Tenant & Security
- ทุกตารางมี tenant_id + RLS · สิทธิ์ตาม 05 §5.3 · ใบที่ไม่มีสิทธิ์ = 404
### §0.7.1 Data Classification Summary
| ข้อมูล | Class |
|---|---|
| ชื่อผู้ลงนาม / ผู้ดำรงตำแหน่ง | Internal·PII |
| เนื้อหา JD · ตำแหน่ง · ผังหัวหน้า/ลูกน้อง | Internal |
| เลขที่ · สถานะ · วันที่ | Internal |

## §0.8 Open Questions
| OQ | คำถาม |
|---|---|
| OQ-01 | ลูกค้ายืนยัน DEC AI-DEFAULT 12 ข้อ (ใบลงนาม) ก่อน UAT |
| OQ-02 | ผู้อนุมัติค่าเริ่ม role-line-manager (ยังไม่อยู่ใน DOA master 14 role) หรือ role-mgr-hr |
| OQ-03 | ตัวชี้วัด |
| OQ-04 | function_code Taxonomy ของ JD (F01 ชั่วคราว) |
| OQ-05 | รหัส feature จริง + เลข REQ จริง · Position master มีชื่ออังกฤษหรือไม่ |

## §0.9 Glossary
- ผู้จัดทำ = Prepared By · ผู้อนุมัติ = Approved By · ผู้ดำรงตำแหน่ง = Acknowledged By · ฉบับใช้งาน = สถานะ approved/acknowledged · JD = รหัสเอกสาร

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED · INDEX · declarations/

## §0.12 Coverage Manifest
| BRD | FRD |
|---|---|
| §2.4 DEC-01..17 | 07 §7.0 |
| §4 Journey | 01 §1.3 |
| §5 Data | 04 §4.2 |
| §6 US-01..13 | 06 §6.1 |
| §7 Status | 05 §5.2 |
| §8 BR-01..13 | 05 §5.1 |
| §9 EC-01..10 | 05 §5.5 |
| §14 Security | 00 §0.7 · 05 §5.3 |
