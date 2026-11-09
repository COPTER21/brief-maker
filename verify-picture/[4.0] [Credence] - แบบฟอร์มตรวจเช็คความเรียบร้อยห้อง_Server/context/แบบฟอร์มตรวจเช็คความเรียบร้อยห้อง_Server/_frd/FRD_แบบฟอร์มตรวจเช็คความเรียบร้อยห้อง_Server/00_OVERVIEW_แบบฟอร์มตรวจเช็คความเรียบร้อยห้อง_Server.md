# 00_OVERVIEW — F-TMP-002 แบบฟอร์มตรวจเช็คความเรียบร้อยห้อง Server (Server Room Check)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-002 v1.0 · frd-generator-v6 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **STANDARD** (pages=3, states=3, approval=N, money=N) |
| Source | BRD-ITS-SRC-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-002_v2 · FORM_SPEC FM-ITS-10 · DECISIONS.lock (13 DEC · AI-DEFAULT) · feature.html (html-generator-v9.4 · audit FAIL 0 · jsdom smoke 33/33 · NO-BROWSER) |
| Module / Area | IT Support · Core |
| Status | Ready for Dev (หลัง OQ-03/04 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (แท็บสถานะ) · สร้าง/แก้ร่าง (3 ขั้น · ตารางกรอกรายวัน) · ดู 4 แท็บ · เตือนเกณฑ์ · แจ้งผู้ดูแล · ส่งปิดรอบ (ไม่มีขั้นพิจารณา) · ยกเลิก · แนบไฟล์ · PDF FM-ITS-10 Replica 2 หน้า · เลข SRC · CSV
### Out of Scope
เปิด IT Ticket อัตโนมัติ (DEC-02) · ดึงค่าจาก sensor · หลายห้องในใบเดียว · ทำซ้ำ · ผู้ตรวจทานค่าเริ่ม (DEC-03)

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| เจ้าหน้าที่ IT (ผู้บันทึก/ผู้ตรวจสอบ) | Maker | owner |
| ผู้ดูแลห้อง Server (admin role ฝ่าย IT) | Monitor · admin view | admin_role (ยังไม่มีใน DOA contract — OQ-03) |
| ผู้ตรวจทาน | — | ไม่มีรอบนี้ (DEC-03) · enhancement ถ้าลูกค้ายืนยัน (OQ-02) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน) · F-ORG-001 (OrgUnit · อ่าน) · (ไม่ใช้ DOA — DEC-03) · F-DOCCFG/F003 (doc_type SRC · status · print_config) · ServerRoomCheckConfig (เกณฑ์ — ใหม่ OQ-04) · Company Master (logo/header)
### Downstream
ENG-NOTIFY (src_abnormal_found · src_submitted · src_cancelled) · IT Support › Ticket (ประกาศ event `src.abnormal_found` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/server-room-check` (อ้าง feature.html เป็น source of truth) · BE: REST `/api/v1/server-room-checks` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less) + data contract (03 FN-07)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: ผลตรวจ/เกณฑ์ · Confidential(PII): ชื่อผู้ตรวจสอบ snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (โดยเฉพาะ ไม่มีผู้ตรวจทาน) | Strike | ก่อน UAT |
| OQ-03 | admin role ฝ่าย IT — role id ใน RBAC/DOA | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | ServerRoomCheckConfig อยู่ที่ไหน | พี่เบิร์ด | ก่อน dev |
| OQ-05 | รูปแบบความดันถังดับเพลิง | ลูกค้า | – |
| OQ-06 | หลายห้อง Server ต่อบริษัทไหม | ลูกค้า | – |
| OQ-07 | function_code taxonomy SRC · รหัส feature จริง | Strike | ก่อน register |

## §0.9 Glossary
MDB = ตู้เมนไฟฟ้า (Main Distribution Board) · PDU = รางปลั๊กจ่ายไฟในตู้ Rack · %RH = ความชื้นสัมพัทธ์ · ปิดรอบ = ส่งใบตรวจเช็คที่ครบรอบแล้ว (ล็อกแก้ไข)

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F11 (FORM_SPEC) | check_date · access_log · extinguisher_pressure · temperature_c · humidity_rh · aircon · cctv · mdb · pdu · remark · checked_by | 01 §1.2 P-02 · 04 §4.2 · 03 FN-02/FN-07 |
| ค่าคงที่ 2 (18-27°C · 40-55 %RH) | criteria | 04 criteria_snapshot · 05 BR-01 · config |
| BRD S-01..S-08 | stories | 06 AC-01..AC-12 |
| BRD BR-01..10 · VR-01..05 · EC-01..08 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..13 | มติ | 07 §7.0 |
| declaration | NTF · DOCCFG · MDOC (ไม่มี DOA — DEC-03) | declarations/ · 03 FN-03/04/06/08 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..05 | 01 §1.1 |
ไม่มี requirement หล่น
