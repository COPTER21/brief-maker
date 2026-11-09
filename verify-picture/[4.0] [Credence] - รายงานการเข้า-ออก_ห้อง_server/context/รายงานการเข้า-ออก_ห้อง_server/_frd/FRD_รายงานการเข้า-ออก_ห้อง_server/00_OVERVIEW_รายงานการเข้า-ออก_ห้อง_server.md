# 00_OVERVIEW — F-TMP-006 รายงานการเข้า-ออก ห้อง server (Server Room Access Log)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-006 v1.0 · frd-generator-v6 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **STANDARD** (pages=3, states=3, approval=N, money=N) |
| Source | BRD-ITS-SRAL-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-006_v2 · FORM_SPEC FM-ITS-09 · DECISIONS.lock (14 DEC · AI-DEFAULT) · feature.html (html-generator-v9.4 · audit FAIL 0 · jsdom smoke 46/46 · NO-BROWSER) |
| Module / Area | IT Support · Core |
| Status | Ready for Dev (หลัง OQ-03/04 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (แท็บสถานะ) · สร้าง/แก้ร่าง (3 ขั้น · ตารางกรอกการเข้า-ออก) · ดู 4 แท็บ · ลายเซ็นผู้เข้าในระบบ · รับรองรายแถวโดยเจ้าหน้าที่ IT (≠ ผู้เข้า) · ตรวจเวลา (ออกก่อนเข้า = บล็อก · เกินเวลา = เตือน) · แจ้งเตือน · ส่งปิดรอบ (ไม่มีขั้นพิจารณา · ต้องออกครบ+รับรองครบ) · ยกเลิก · แนบไฟล์ · PDF FM-ITS-09 Replica 2 หน้า · เลข SRAL · CSV
### Out of Scope
เชื่อมระบบประตู/บัตร (DEC-02) · ขออนุมัติก่อนเข้าห้อง (DEC-03) · หลายห้องในใบเดียว · ทำซ้ำ · ลายมือชื่อภาพ

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| เจ้าหน้าที่ IT ผู้บันทึก (เจ้าของรายงาน) | Maker | owner (มี role-it-officer) |
| เจ้าหน้าที่ IT ผู้รับรอง | Checker รายแถว | role-it-officer (ยังไม่มีใน doa-roles-contract — OQ-03) |
| ผู้ดูแลห้อง server (admin role ฝ่าย IT) | Monitor · admin view · Checker รายแถว | admin_role (ยังไม่มีใน DOA contract — OQ-03) |
| ผู้อนุมัติ | — | ไม่มีรอบนี้ (DEC-03) · enhancement ถ้าลูกค้ายืนยัน (OQ-02) |

## §0.5 Dependencies
### Upstream
F-EMP-001 (Employee · อ่าน — รายชื่อ/ฝ่ายสำหรับผู้เข้าที่เป็นพนักงาน · ผู้รับรอง) · F-ORG-001 (OrgUnit · อ่าน) · (ไม่ใช้ DOA — DEC-03) · F-DOCCFG/F003 (doc_type SRAL · status · print_config) · ServerRoomAccessConfig (max_stay_hours — ใหม่ OQ-04) · Company Master (logo/header)
### Downstream
ENG-NOTIFY (sral_certify_pending · sral_overstay · sral_submitted · sral_cancelled) · ระบบประตู/บัตร (ไม่มีรอบนี้ — DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/server-room-access` (อ้าง feature.html เป็น source of truth) · BE: REST `/api/v1/server-room-access` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less) + data contract (03 FN-07)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม §5.3 · audit append-only (รวมการรับรองรายแถว)
### §0.7.1 Data Classification Summary
Internal: เวลาเข้า-ออก/เหตุผล · Confidential(PII): ชื่อผู้เข้า · ชื่อผู้รับรอง snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (โดยเฉพาะ ไม่มีขออนุมัติก่อนเข้า · ผู้รับรอง ≠ ผู้เข้า) | Strike | ก่อน UAT |
| OQ-03 | role-it-officer · admin role ฝ่าย IT — role id ใน RBAC/DOA contract | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | ServerRoomAccessConfig อยู่ที่ไหน | พี่เบิร์ด | ก่อน dev |
| OQ-05 | บุคคลภายนอกต้องเก็บข้อมูลเพิ่มไหม (เลขบัตร — PDPA) | ลูกค้า | – |
| OQ-06 | หลายห้อง server ต่อบริษัทไหม | ลูกค้า | – |
| OQ-07 | function_code taxonomy SRAL · รหัส feature จริง | Strike | ก่อน register |

## §0.9 Glossary
ผู้เข้า = คนที่เข้าห้อง server (พนักงานหรือบุคคลภายนอก) · ผู้รับรอง = เจ้าหน้าที่ IT ที่ยืนยันว่าการเข้า-ออกนั้นเกิดจริง · ปิดรอบ = ส่งรายงานที่ครบรอบแล้ว (ล็อกแก้ไข) · ยังอยู่ในห้อง = แถวที่ยังไม่มีเวลาออก

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F09 (FORM_SPEC) | visitor_name · visitor_department · in_date · in_time · out_date · out_time · purpose · visitor_signed · certified_by | 01 §1.2 P-02 · 04 §4.2 · 03 FN-02/FN-07 |
| ค่าคงที่ | ไม่มีบนกระดาษ · เกณฑ์เวลาอยู่ในห้อง (ใหม่ DEC-04) | 04 config · 05 BR-01 |
| BRD S-01..S-08 | stories | 06 AC-01..AC-14 |
| BRD BR-01..11 · VR-01..06 · EC-01..09 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..14 | มติ | 07 §7.0 |
| declaration | NTF · DOCCFG · MDOC (ไม่มี DOA — DEC-03) | declarations/ · 03 FN-03/04/06/08/10 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..04 | 01 §1.1 |
ไม่มี requirement หล่น
