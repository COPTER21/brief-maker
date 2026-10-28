# 00_OVERVIEW — F-TMP-003 แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน

## §0.1 Document Control
| รายการ | ค่า |
|---|---|
| Feature | F-TMP-003 (ชั่วคราว) · HR · เสนอเมนูใหม่ "ขอเข้าพื้นที่สำนักงาน" |
| Request | REQ-TMP-003 (ชั่วคราว) |
| แบบฟอร์ม | FM-HRM-05 Rev. 00 : 01/07/2569 (1 หน้า) |
| Generator | frd-generator-v6 (Input Mode 0 · Lane Mode) |
| Upstream | BRD_F-TMP-003 v1.0 (APPROVED) · DECISIONS.lock (15 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4) · print/form.tpl.html |
| Variant | STANDARD (1 หน้า list + drawer · สายอนุมัติ DOA) |

## §0.2 Revision History
| ver | date | by | note |
|---|---|---|---|
| v1.0 | 2026-10-08 | AI (unattended) | ฉบับแรก |

## §0.3 Scope
### In Scope
- รายการ · wizard 3 ขั้น · ดู 4 แท็บ · ส่งขออนุมัติ · อนุมัติ / ไม่อนุมัติ (กลับร่าง) · ยกเลิก · CSV · แนบไฟล์ · แบบพิมพ์ FM-HRM-05 · เลข VAR · สาย DOA dynamic · แจ้งเตือน var_cancelled
### Out of Scope
- เปลี่ยนค่าในระบบ (DEC-01) · ส่งต่อระบบแลกบัตร/ประตู (DEC-02) · บัญชีผู้ใช้ผู้มาติดต่อ · ลายมือชื่อภาพ (DEC-07) · ทำซ้ำ/ประกาศ (DEC-11) · dashboard

## §0.4 Roles (COSO)
| role | ใคร | COSO |
|---|---|---|
| owner | ผู้บันทึก (`owner_id`) — พนักงานผู้รับการติดต่อ หรือผู้บันทึกแทน | Maker |
| host | พนักงานผู้รับการติดต่อ (`host_employee_id`) | Maker (ดูได้) |
| `role-line-manager` (DOA ขั้น 1 ค่าเริ่ม) | ผู้บังคับบัญชาต้นสังกัดของ host | Approver |
| `role-mgr-hr` | admin role ของหน่วยงานเจ้าของแบบฟอร์ม | Checker |
| ผู้มาติดต่อ | บุคคลภายนอก — ไม่มีบัญชี | — |

## §0.5 Dependencies
### Upstream
- F-EMP-001 Employee (full_name, position) — อ่านอย่างเดียว
- F-ORG-001 OrgUnit / line_manager — สังกัดฝ่าย · ผู้บังคับบัญชาต้นสังกัด
- Organization — header_snapshot (Company.name_th · โลโก้) · DEC-13
- F-DOCCFG (doc_type VAR) · ENG-DOC-NUM · ENG-DOC-STORE · Document Center · ENG-NOTIFY · DOA กลาง (F-DLG-001)
### Downstream
- ไม่มี (DEC-02) — event var_cancelled ผ่าน ENG-NOTIFY · doa_pending/doa_result ผ่าน DOA engine
### External
- ไม่มี

## §0.6 Stack
- ตามมาตรฐาน CUBE (API REST · Postgres · RLS tenant) · Prototype = html-generator-v9.4 single-file · แบบพิมพ์ thai-doc v2.1 (logic-less template + parity)

## §0.7 Multi-Tenant & Security
- ทุกตารางมี tenant_id + RLS · สิทธิ์ตาม 05 §5.3 · ใบที่ไม่มีสิทธิ์ = 404
### §0.7.1 Data Classification Summary
| ข้อมูล | Class |
|---|---|
| ชื่อ-นามสกุล · หมายเลขโทรศัพท์ผู้มาติดต่อ | Confidential·PII |
| วัตถุประสงค์ · ความเห็นผู้บังคับบัญชา | Internal |
| เลขที่ · สถานะ · วันที่ · บริษัท/หน่วยงาน | Internal |

## §0.8 Open Questions
| OQ | คำถาม |
|---|---|
| OQ-01 | ลูกค้ายืนยัน DEC AI-DEFAULT 11 ข้อ (ใบลงนาม) ก่อน UAT |
| OQ-02 | host ไม่มีผู้บังคับบัญชา → ใครพิจารณา · role-line-manager ยังไม่อยู่ใน DOA master (14 role) |
| OQ-03 | ตัวชี้วัด |
| OQ-04 | ใบที่อนุมัติแล้วยกเลิกได้หรือไม่ |
| OQ-05 | ส่งต่อจุดรับแขก/ระบบแลกบัตร (รอบถัดไป) |
| OQ-06 | function_code Taxonomy ของ VAR (F01 ชั่วคราว) · รหัส feature/REQ จริง |
| OQ-07 | ถ้อยคำยินยอม PDPA บนแบบฟอร์ม |

## §0.9 Glossary
- host = พนักงานผู้รับการติดต่อ · ผู้มาติดต่อ = บุคคลภายนอก · VAR = รหัสเอกสาร (Visitor Access Request)

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED · INDEX · declarations/

## §0.12 Coverage Manifest
| BRD | FRD |
|---|---|
| §2.4 DEC-01..15 | 07 §7.0 |
| §4 Journey | 01 §1.3 |
| §5 Data (ช่องในฟอร์ม 14) | 04 §4.2 · 01 §1.2 |
| §6 US-01..10 | 06 §6.1 |
| §7 Status | 05 §5.2 |
| §8 BR-01..12 | 05 §5.1 |
| §9 EC-01..11 | 05 §5.5 |
| §14 Security | 00 §0.7 · 05 §5.3 |
