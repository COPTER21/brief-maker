# 00_OVERVIEW — F-TMP-005 ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade

## §0.1 Document Control
| รายการ | ค่า |
|---|---|
| Feature | F-TMP-005 (ชั่วคราว) · Sales · Visit Operation ⟂ (อ้างอิง Sales Territory ⟂ · Customer) |
| Request | REQ-TMP-005 (ชั่วคราว) |
| แบบฟอร์ม | FM-SAL-09 Rev.00:01/07/2569 (1 หน้า A4 แนวนอน) |
| Generator | frd-generator-v6 (Input Mode 0 · Lane Mode) |
| Upstream | BRD_F-TMP-005 v1.0 (APPROVED) · DECISIONS.lock (18 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4) |
| Variant | STANDARD |

## §0.2 Revision History
| ver | date | by | note |
|---|---|---|---|
| v1.0 | 2026-10-08 | AI (unattended) | ฉบับแรก |

## §0.3 Scope
### In Scope
- รายการ · wizard 3 ขั้น · ดู 4 แท็บ · ส่งอนุมัติ · อนุมัติ/ไม่อนุมัติ (2 ขั้นค่าเริ่ม) · ยกเลิก · ใบใหม่แทนใบเดิม (เขต+รอบ) · แจ้ง TO/CC · CSV · แนบไฟล์ · แบบพิมพ์ FM-SAL-09 · เลข SVT · แจ้งเตือน 3 event
### Out of Scope
- แก้ Customer / Sales Territory (DEC-01) · สร้าง Visit/เช็กอินจริง (DEC-02) · ทำซ้ำ/ประกาศ (DEC-11) · dashboard · เป้ายอดขาย

## §0.4 Roles (COSO)
| role | ใคร | COSO |
|---|---|---|
| owner (ผู้นำเสนอ · ผู้รับผิดชอบเขต) | ผู้สร้างเอกสาร | Maker |
| DOA step 1 | resolve จาก DOA กลาง · ค่าเริ่ม `role-line-manager` (relative role — ผู้บังคับบัญชาตรงของผู้นำเสนอ) | Checker |
| DOA step 2 | ค่าเริ่ม `role-mgr-sales` | Approver |
| recipient (TO / CC) | to_recipient · cc_recipients | Recipient (ไม่ใช่ขั้น DOA) |
| `role-mgr-sales` | admin role ของหน่วยงานเจ้าของเอกสาร | Checker |

## §0.5 Dependencies
### Upstream
- Sales Territory ⟂ (code · name · owner_employee_id) — อ่านอย่างเดียว
- Customer (customerId · name · territory) — อ่านอย่างเดียว
- Employee / Position (ชื่อ · ตำแหน่ง · ผู้บังคับบัญชาตรง) — อ่านอย่างเดียว
- Organization — header_snapshot (ชื่อบริษัท · โลโก้)
- F-DOCCFG (doc_type SVT) · ENG-DOC-NUM · ENG-DOC-STORE · Document Center · ENG-NOTIFY · DOA กลาง (F-DLG-001)
### Downstream
- ไม่มี (DEC-02) — event svt_plan_published ประกาศไว้ให้ Visit Operation ใช้ภายหลัง
### External
- ไม่มี

## §0.6 Stack
- ตามมาตรฐาน CUBE (API REST · Postgres · RLS tenant) · Prototype = html-generator-v9.4 single-file · แบบพิมพ์ thai-doc v2.1 (logic-less template + parity) · server render A4 แนวนอนตาม print_config.paper

## §0.7 Multi-Tenant & Security
- ทุกตารางมี tenant_id + RLS · สิทธิ์ตาม 05 §5.3 · ใบที่ไม่มีสิทธิ์ = 404
### §0.7.1 Data Classification Summary
| ข้อมูล | Class |
|---|---|
| ชื่อผู้รับผิดชอบเขต / ผู้ลงนาม / TO / CC | Internal·PII |
| เขต · รอบ · ตลาด · ร้านค้า · จังหวัดที่พัก | Internal |
| เลขที่ · สถานะ · วันที่ | Internal |

## §0.8 Open Questions
| OQ | คำถาม |
|---|---|
| OQ-01 | ลูกค้ายืนยัน DEC AI-DEFAULT 11 ข้อ (ใบลงนาม) ก่อน UAT |
| OQ-02 | ผู้อนุมัติขั้น 1 = role-line-manager (ยังไม่อยู่ใน DOA master 14 role) หรือ role-supervisor · ขั้น 2 = role-mgr-sales |
| OQ-03 | ตัวชี้วัด |
| OQ-04 | function_code Taxonomy ของ SVT (F01 ชั่วคราว) |
| OQ-05 | รหัส feature จริง + เลข REQ จริง · "รอบการขาย" = เดือนปฏิทินหรือไม่ |
| OQ-06 | คอลัมน์ย่อยว่างใต้ "วันทำงาน" ใช้ทำอะไร |
| OQ-07 | แบบพิมพ์ A4 แนวนอน — thai-doc v2.1 ยังไม่มี token orientation |

## §0.9 Glossary
- ผู้นำเสนอ = ผู้รับผิดชอบเขตที่ส่งแผน · รอบการขาย = เดือน/ปี (YYYY-MM) · วันทำงาน = แถวแผนรายวัน · ใบใช้งาน = สถานะ approved · SVT = รหัสเอกสาร

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED · INDEX · declarations/

## §0.12 Coverage Manifest
| BRD | FRD |
|---|---|
| §2.4 DEC-01..18 | 07 §7.0 |
| §4 Journey | 01 §1.3 |
| §5 Data | 04 §4.2 |
| §6 US-01..12 | 06 §6.1 |
| §7 Status | 05 §5.2 |
| §8 BR-01..14 | 05 §5.1 |
| §9 EC-01..10 | 05 §5.5 |
| §14 Security | 00 §0.7 · 05 §5.3 |
