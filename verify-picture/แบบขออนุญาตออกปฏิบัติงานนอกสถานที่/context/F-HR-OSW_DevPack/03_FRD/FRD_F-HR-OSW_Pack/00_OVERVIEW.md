# 00_OVERVIEW — F-HR-OSW แบบขออนุญาตออกปฏิบัติงานนอกสถานที่ (Off-site Work Request)

> Audience: ทุกคน (PM · BA · FE · BE · QA · Architect) — อ่านไฟล์นี้ก่อน แล้วไปตาม §0.10

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD ID | FRD-HR-OSW-001 |
| Feature | F-HR-OSW (รหัสจริงกำหนดตอนเริ่มพัฒนา — ดู 07 CD-01) |
| Module | HR › Payroll & Time (Core Cube) |
| Version | 1.0.1 |
| Status | Ready for Dev handoff (มีเงื่อนไข — OQ-01 Sign-off) |
| Source BRD | `BRD_F-HR-OSW.md` v1.0 — Status APPROVED (มีเงื่อนไข) |
| Source HTML | `offsite-work-request.html` รอบ 4 (E2E 64/64 · PDF/DOA 13/13 · self_audit PASS · audit.sh FAIL 9 = กฎ B2 line editor ไม่ใช้กับเอกสารนี้) |
| Declarations | `DOA_BRIEF_F-HR-OSW.md` v1.1 · `DOCCFG_BRIEF_F-HR-OSW.md` v1.1 · `MDOC_BRIEF_OSW.md` (แนบใน pack) |
| Print | `print/osw_body.tpl.html` + `print/OSW_print-spec.md` (thai-doc-pdf-generator · FORM REPLICA) |
| **Pack Variant** | **FULL (9 ไฟล์ + INDEX)** — fallback จาก BRD: pages=3 (+5 modal) · states=5 · approval=Y · §9.5 มี Engine Management (DOA) |
| Generator | frd-generator-v6.1 · Sync Read: **html-generator-v9** (v6 ไม่ได้ติดตั้ง — ใช้เวอร์ชันสูงสุด) |
| Owner | BA ทีม 2BSimple · DA: Strike |
| Created | 5 ต.ค. 2569 |

## §0.2 Revision History
| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-10-05 | BA (frd-generator-v6) | Initial — BRD v1.0 + HTML รอบ 4 |
| 1.0.1 | 2026-10-05 | BA (doccfg-declaration) | sync DOCCFG_BRIEF v1.1: เช็คเปิดใช้ย้ายจาก F185 → F-DOCCFG · header_snapshot จาก Organization · ช่องลายเซ็นตาม sign_boxes config |

## §0.3 Scope
### In Scope
- รายการ / สร้าง (wizard 3 ขั้น) / แก้ไขร่าง / ดูรายละเอียด (4 แท็บ) / ส่งขออนุญาต / อนุญาต / ไม่อนุญาต / ยกเลิก / ทำซ้ำ / พิมพ์-ดาวน์โหลด PDF / ส่งออก CSV
- หลายช่วงวันที่ต่อใบ (ไม่จำกัด) · ไป-กลับ / ค้างคืน · ค่าเบี้ยเลี้ยง = คืน × อัตรานโยบาย
- สายอนุมัติจาก DOA กลาง (dynamic N ขั้น · sequential · ไม่มีวงเงิน)
- เลขที่จาก ENG-DOC-NUM · เก็บสำเนา PDF เมื่ออนุญาตครบ (ENG-DOC-STORE)
- PDF แบบฟอร์มลูกค้า FM-HRM-02 Rev.00 (logic-less template + data contract)

### Out of Scope
- ส่งต่อเวลาทำงาน (F-ATTEND-001) / เบิกจ่าย / เงินเดือน (F-PAYROLL-001) — DEC-02
- เปลี่ยนค่าในระบบเมื่ออนุญาต — DEC-01 · วงเงินในสายอนุมัติ — DEC-03 · ลายมือชื่อภาพ — DEC-09
- HR สร้างคำขอแทนพนักงาน · หน้าตั้งค่า DOA / เลขรัน / นโยบายเบี้ยเลี้ยง (เป็นของ feature กลาง)
- ตัวสลับผู้ใช้ใน prototype (เดโมเท่านั้น)

### Out of Scope (mark from Phase 2.5 skipped probes)
- PR-5 Bulk operation — ไม่มี bulk action ในจอ · PR-8 Rate limiting เฉพาะ — ใช้ default ของ platform

## §0.4 Roles & Responsibilities (COSO)
| Role | COSO | ทำอะไร |
|---|---|---|
| พนักงาน (ผู้ขอ) | Maker | สร้าง · แก้ร่าง · ส่ง · ยกเลิกใบตัวเอง · ทำซ้ำ · พิมพ์ |
| ผู้พิจารณา (ตาม DOA — ค่าเริ่ม ผู้บังคับบัญชาตรง) | Approver | อนุญาต / ไม่อนุญาต เฉพาะขั้นปัจจุบันที่ได้รับมอบ |
| ฝ่ายบุคคล (HR) | Checker (ติดตาม) | เห็นทุกใบ · ยกเลิก · ส่งออก |
| System | System | ดึงข้อมูลผู้ขอ · คำนวณวัน/คืน/เบี้ยเลี้ยง · ออกเลข · resolve DOA · แจ้งเตือน · สร้าง/เก็บ PDF |
SoD: Maker ≠ Approver ทุกขั้น (BR-OSW-11)

## §0.5 Dependencies
### Upstream (this feature depends on)
| Feature / Engine | ใช้ทำอะไร | ชนิด |
|---|---|---|
| F-EMP-001 Employee | ชื่อ · ตำแหน่ง (snapshot) | read |
| F-ORG-001 OrgUnit | ฝ่าย · ผู้บังคับบัญชาตรง (resolve role-line-manager) | read |
| ExpensePolicy | per_diem (snapshot) | read |
| F-DLG-001 DOA engine | resolve สาย · decide ขั้น · My Approval · แจ้ง doa_pending/doa_result | call + callback |
| F-DOCCFG (F003 Document Configuration) · ENG-DOC-NUM · ENG-DOC-STORE | สถานะเปิดใช้ · print_config (แบบพิมพ์ · Doc No/Rev · min_rows · sign_boxes) · เลขที่ · เก็บสำเนา | call |
| Organization (ข้อมูลบริษัท) | หัวกระดาษ/โลโก้ → header_snapshot ตอนออกเลข | read |
| Document Center | ไฟล์แนบ | call |
| ENG-NOTIFY | แจ้งยกเลิก (event ของ feature เอง) | event |
| thai-doc-pdf-generator template | แบบพิมพ์ FORM REPLICA | file/config |

### Downstream (features that depend on this)
| Feature | สถานะ |
|---|---|
| F-ATTEND-001 · F-PAYROLL-001 | ❌ ไม่ส่งรอบนี้ (DEC-02) — สัญญาเหตุการณ์ `osw.approved` ประกาศไว้ใน 02 §2.X เพื่ออนาคต (ยังไม่มี consumer) |
| My Approval (DOA) | ✅ ผ่าน DOA engine |
| Document Store | ✅ PDF approved_final |

### External
- ไม่มี 3rd party

## §0.6 Stack & Architecture
- Core Cube (multi-tenant · PostgreSQL RLS) · REST `/api/v1/osw` · CUBIC 3-layer: UI → API (HTTP) → LOGIC (Functions/Engines) → DB
- PDF: render ฝั่ง server จาก `osw_body.tpl.html` + data contract (Chromium/Gotenberg ที่ honor `@page` + Sarabun)
- FE: SPA hash routing `#/offsite…` ตาม HTML prototype (single source ของ UI)

## §0.7 Multi-Tenant & Security Context
- ทุกตาราง `tenant_id` + RLS · ทุก API ต้องมี JWT + `X-Tenant-Id`
- Security Bible: ไม่พบ `Security_Spec_Bible.md` ใน uploads → ใช้ domain triggers จาก BRD §16 (Custom ฐาน P2 + PII) — log
- Domains ที่ trigger: D2 Auth/Session · D7 PII · D9 Audit · D17 Multi-Tenant · (D5 Financial = ไม่ — ไม่มีการเงิน/ลงบัญชี มีแค่ยอดอ้างอิง)

### §0.7.1 Data Classification Summary
| ระดับสูงสุดที่ feature แตะ | Field | เหตุผล |
|---|---|---|
| **Confidential** | `employee_name`, `employee_id`, `purpose` (สถานที่/ภารกิจ), `per_diem_amount` | ข้อมูลส่วนบุคคล + ที่อยู่ระหว่างปฏิบัติงาน + ยอดเงินรายบุคคล |
| Restricted | ไม่มี | ไม่มีเงินเดือน/ข้อมูลระดับ ACL รายบุคคล |

## §0.8 Open Questions
| # | คำถาม | ผู้ตอบ | สถานะ | Block? |
|---|---|---|:---:|---|
| OQ-01 | Sign-off ลูกค้ายืนยัน DEC-01–10 (ไม่มีใบเซ็น) | BA → ลูกค้า | ⚠️ | ก่อน dev handoff |
| OQ-02 | ยืนยันของจากโครงมาตรฐาน: เอกสารแนบ · ทำซ้ำ · ส่งออก CSV | ลูกค้า (ใน Sign-off) | ⚠️ | ไม่ |
| OQ-03 | เจ้าของ/หน้าตั้งค่า ExpensePolicy.per_diem | Bird | ⚠️ | ก่อน BE เริ่ม FN-02 |
| OQ-04 | SLA การพิจารณาต่อขั้น (BR-OSW-20 WARNING) | HR ลูกค้า | ⚠️ | ไม่ (ไม่สร้าง SLA timer) |
| OQ-05 | positioning H2R เมื่อมี VS Bible | ทีม VS | ⚠️ | ไม่ |
| OQ-06 | code `OSW` ชน registry F-DOCCFG หรือไม่ | ทีม 2B ตอน deploy | ⚠️ | ก่อน deploy |
| OQ-07 | รัน qc-ux-html-checker + qc-coverage-checker อย่างเป็นทางการ | BA | ⚠️ | ไม่ |
| OQ-08 `[AI-DEFAULT]` | ระยะเก็บรักษาข้อมูล (04 §4.7) — ใช้นโยบาย tenant (default 5 ปี) | DA / ลูกค้า | ⚠️ | ไม่ |
| OQ-09 `[AI-DEFAULT]` | ยกเลิกใบอนุญาตแล้วหลังวันเดินทางผ่าน — อนุญาต (ตาม HTML) หรือบล็อก | ลูกค้า | ⚠️ | ไม่ |
| OQ-10 `[AI-DEFAULT]` | อัตราเบี้ยเลี้ยง snapshot ตอนสร้าง (ไม่ใช่ตอนส่ง) | DA | ⚠️ | ไม่ |

**Phase 2.5 probes ที่ใช้ default (one-shot · ไม่ถาม):** PR-1 concurrent decide → optimistic lock 409 (BR §5.5 EC-01) · PR-2 version ทุก transition · PR-3 สิทธิ์ถูกถอนกลางทาง → 403 + รีเฟรช · PR-4 network ล้ม → transaction rollback + client คงข้อมูล · PR-6 delegation → ใช้ของ DOA กลาง · PR-7 idempotency key บน POST create/submit/decide/cancel · PR-9 ข้อมูลต้นทางหาย (ไม่มีหัวหน้า/อัตรา) → slot ว่าง/บล็อกค้างคืน — ทั้งหมดติด `[AI-DEFAULT]` ใน 05_RULES

## §0.9 Glossary
OSW = Off-site Work Request · DOA = Delegation of Authority (F-DLG-001) · DEC-xx = มติ DA (แทน Scope Lock) · FORM REPLICA = pattern แบบพิมพ์ที่คงหน้าตาแบบฟอร์มลูกค้า · snapshot = เก็บค่า ณ เวลาทำรายการ

## §0.10 Pack Navigation
| ไฟล์ | อ่านเมื่อ |
|---|---|
| 01_UI | FE — หน้า/route/component/ข้อความจริง |
| 02_API | BE — HTTP contract + cross-module |
| 03_LOGIC | BE — Functions/Engines + trace |
| 04_DB | DBA/BE — schema + classification |
| 05_RULES | BE/QA — rules · state · edge · errors · security |
| 06_TESTS | QA — AC · test inventory · verbatim text |
| 07_LOCKED_DECISIONS | ทุกคน — สิ่งที่ห้ามเปลี่ยน |
| INDEX | cross-reference |
| `declarations/` · `print/` | DOA / DOCCFG / MDOC · แบบพิมพ์ |

## §0.11 Scope Lock
FULL variant → ดู **07 §7.0** (DEC-01–10 · ยังไม่มีใบเซ็น — OQ-01)

## §0.12 Coverage Manifest
| BRD Ref | Requirement | อยู่ที่ (file §) |
|---|---|---|
| §7 S-01 | สร้างคำขอโดยไม่กรอกข้อมูลตัวเอง | 01 P-02 · 02 API-12 · 03 FN-02 · 06 AC-01 |
| §7 S-02 | ระบุช่วงวันที่ + เพื่อ | 01 P-02 Z2 · 03 FN-03 · 05 BR-OSW-06 · VR-01..04 · 06 AC-02 |
| §7 S-03 | เพิ่ม/ลบช่วง | 01 P-02 Z2 · 06 AC-03 |
| §7 S-04 | เปลี่ยนเวลา | 01 P-02 Z2 · 05 VR-05/06 · 06 AC-04 |
| §7 S-05 | ค้างคืน + เบี้ยเลี้ยง | 01 P-02 Z3 · 03 FN-04 · 05 BR-OSW-03/04/05 · 06 AC-05 |
| §7 S-06 | ปรับจำนวนคืน | 01 P-02 Z3 · 05 VR-08..10 · 06 AC-06 |
| §7 S-07 | ส่งขออนุญาต | 01 M-01 · 02 API-05/06 · 03 FN-07/08 · 06 AC-07 |
| §7 S-08 | อนุญาต | 01 P-03 · M-02 · 02 API-07/13 · 03 FN-09 · 06 AC-08 |
| §7 S-09 | ไม่อนุญาต | 01 M-03 · 02 API-08 · 03 FN-09 · 06 AC-09 |
| §7 S-10 | ยกเลิก | 01 M-04 · 02 API-09 · 03 FN-10 · 06 AC-10 |
| §7 S-11 | พิมพ์ PDF | 01 P-03 T2 · 02 API-10 · 03 FN-11/12 · ENG-01 · 06 AC-11 |
| §7 S-12 | รอฉันพิจารณา | 01 P-01 Z2 · 02 API-01 · 03 FN-01 · 06 AC-12 |
| §7 S-13 | ทำซ้ำ | 01 P-02 (copy) · 02 API-03 · 03 FN-05 · 06 AC-13 |
| §9 R01–R04 | สถานะเริ่ม · snapshot · ไป-กลับ/ค้างคืน · สูตรเบี้ยเลี้ยง | 05 BR-OSW-01..04 · 06 AC-05 |
| §9 R05 | อัตราจากนโยบาย | 05 BR-OSW-05 · 03 FN-02 · 06 AC-05 |
| §9 R06–R07 | คืนเริ่มต้น · เกินช่วง = เตือน | 05 BR-OSW-06/07 · 03 FN-04 · 06 AC-06 |
| §9 R08 | เวลาเริ่มต้น | 05 BR-OSW-08 · 02 API-12 |
| §9 R09–R10 | DOA resolve+freeze · sequential | 05 BR-OSW-09/10 · 03 FN-07/08/09 · 06 AC-07/08 |
| §9 R11 | SoD | 05 BR-OSW-11 · 06 AC-14 |
| §9 R12–R13 | เหตุผลบังคับ · แก้เฉพาะร่าง | 05 BR-OSW-12/13 · 06 AC-09/10/15 |
| §9 R14–R15 | เลขที่ · เช็คแบบเอกสาร | 05 BR-OSW-14/15 · 03 FN-05 · 06 AC-16 |
| §9 R16 | ไฟล์แนบ | 05 BR-OSW-16 · 06 AC-17 |
| §9 R17–R18 | แบบพิมพ์ · เก็บสำเนา | 05 BR-OSW-17/18 · 03 FN-11/13 · 06 AC-11/18 |
| §9 R19 | การมองเห็น | 05 BR-OSW-19 · 03 FN-01 · 06 AC-19 |
| §9 R20 | SLA (WARNING) | 05 BR-OSW-20 · OQ-04 |
| §9.2 VR01–VR15 | validation | 05 §5.4 VR-01..15 · 06 §6.10 |
| §10 E01–E12 (☑) | edge ยืนยันแล้ว | 05 EC-01..EC-12 · 06 AC (ตาม EC) |
| §10 E13–E22 (☐) | edge แนะนำ | 05 EC-13..EC-22 (status: แนะนำ — BA ยืนยัน SOW3.7) |
| §12.1 Downstream | My Approval · ผลพิจารณา · Document Store · F-DOCCFG · (อนาคต) ATTEND/PAYROLL | 02 §2.X · 03 FN-08/09/13 · 06 §6.9 |
