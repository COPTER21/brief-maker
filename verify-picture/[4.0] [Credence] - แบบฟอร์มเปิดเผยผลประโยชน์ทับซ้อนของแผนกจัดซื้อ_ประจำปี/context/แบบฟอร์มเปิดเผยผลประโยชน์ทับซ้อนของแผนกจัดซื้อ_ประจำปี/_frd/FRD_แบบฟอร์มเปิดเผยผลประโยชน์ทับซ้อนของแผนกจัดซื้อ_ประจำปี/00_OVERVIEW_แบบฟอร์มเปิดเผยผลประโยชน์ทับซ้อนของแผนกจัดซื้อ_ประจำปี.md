# 00_OVERVIEW — F-TMP-006 แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนของแผนกจัดซื้อ ประจำปี (Annual Conflict of Interest Disclosure — Purchasing)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-006 v1.0 · frd-generator-v6.2 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (fallback from BRD: pages=3, states=5, approval=Y, print=Y) |
| Source | BRD-PUR-COI-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-006_v2 · FORM_SPEC FM-PUR-04 · DECISIONS.lock (18 DEC) · feature.html (html-generator-v9.4 · audit FAIL 0 · jsdom smoke 39/39 · [NO-BROWSER] e2e ยังไม่รัน) |
| Module / Area | Purchase · Core Cube (Governance ของแผนกจัดซื้อ) |
| Data Classification | **Confidential** (Policy Center › Data Classification) |
| Status | Ready for Dev (หลัง OQ-03/06 ปิด) |
| Date | 2026-10-10 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-10 | สร้างจาก doc-master-pipeline ขั้น 7 (โหมดไม่เฝ้า) |

## §0.3 Scope
### In Scope
รายการ (segmented · ค้นหา · กรองสถานะ/ผลการเปิดเผย · CSV ไม่มีรายละเอียด) · ยื่น/แก้ไข (wizard 3 ขั้น: ถ้อยคำรับรอง · ไม่มี/มี + รายละเอียด · ยืนยัน · แนบไฟล์ · ตรวจสอบ) · ปีตัวแปรรอบปี · แจ้งเปลี่ยนแปลงระหว่างปี (ใบใหม่อ้างใบเดิม) · ดู 4 แท็บ · DOA dynamic (ค่าเริ่ม 1 ขั้นผู้บังคับบัญชา) · แจ้งฝ่ายกฎหมายเมื่อตอบ มี
### Out of Scope
ทะเบียน COI กลาง / เชื่อม Vendor master (OQ-04 · DEC-02) · เปิดรอบ/ติดตามผู้ยังไม่ยื่น (OQ-05) · หน้าตั้งค่า CoiDisclosureConfig (OQ-06) · ทำซ้ำ (DEC-11) · ประกาศ

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้เปิดเผย (พนักงานแผนกจัดซื้อ) | Maker | owner |
| ผู้บังคับบัญชา | Approver/Checker (รับทราบ/ส่งกลับแก้ไข) | role-line-manager (relative role · อยู่ในตาราง "ใช้จริงแต่ยังไม่อยู่ใน master" ของ DOA contract) |
| ฝ่ายกฎหมาย/กำกับดูแล | Monitor · Admin view · ยกเลิกได้ · (ขั้นเพิ่ม OQ-03) | role-compliance |

## §0.5 Dependencies
### Upstream
HR Employee (คำนำหน้า/ชื่อ/ตำแหน่ง · อ่าน) · F-ORG-001 (ผู้บังคับบัญชา · หัวกระดาษ) · F-DLG-001 DOA (resolve role-line-manager — TODO: DOA engine) · F-DOCCFG/F003 (doc_type COI · status · print_config) · CoiDisclosureConfig (ปีรอบ · ถ้อยคำรับรอง · detail_min — OQ-06) · Policy Center › Data Classification (Confidential)
### Downstream
ENG-NOTIFY (coi_conflict_declared · coi_cancelled) · ENG-DOC-STORE (approved_final) · ทะเบียน COI / Vendor master (ประกาศ event `coi.disclosure_acknowledged` — **ไม่ยิงรอบนี้** DEC-02) · Report (Compliance · อ่านเฉพาะสรุป)
### External
Document Center (ไฟล์แนบ · สิทธิ์ตามใบ)

## §0.6 Stack
FE: SPA module `#/coi-disclosure` (feature.html = source of truth) · BE: REST `/api/v1/coi-disclosures` · PDF render ฝั่ง server จาก `print/form.tpl.html` (logic-less) + data contract (03 FN-09)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant + row policy ตาม 05 §5.3 (owner ∨ in-chain-after-submit ∨ role-compliance) · audit append-only (รวม view log — เสนอ)
### §0.7.1 Data Classification Summary
Confidential: conflict_detail · approval_chain[].comment · ชื่อผู้เปิดเผย/ผู้พิจารณา snapshot · ไฟล์แนบ — ไม่ส่งออก CSV · ไม่อยู่ในข้อความแจ้งเตือน · Internal: เลขที่ · ปี · สถานะ · ผล ไม่มี/มี

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT | Strike | ก่อน UAT |
| OQ-03 | "ฝ่ายกฎหมาย" ใต้ช่องลงชื่อ: ต้องลงนามเป็นขั้น 2 ไหม · = role-compliance ไหม | ลูกค้า + พี่เบิร์ด | ก่อน wire |
| OQ-04 | ทะเบียน COI กลาง + เตือนตอนจัดซื้อกับผู้ขายที่เกี่ยวข้อง | ลูกค้า + พี่เบิร์ด | Phase 2 |
| OQ-05 | ใช้กับแผนกอื่น · เปิดรอบ/ติดตามผู้ยังไม่ยื่น | ลูกค้า | – |
| OQ-06 | CoiDisclosureConfig อยู่ที่ไหน (Purchase Configuration / Policy Center) | พี่เบิร์ด | ก่อน dev |
| OQ-07 | แยกรายละเอียดเป็นช่อง | ลูกค้า | – |
| OQ-08 | function_code taxonomy · รหัส feature จริง | Strike | ก่อน register |

## §0.9 Glossary
ผลประโยชน์ทับซ้อน (ตามถ้อยคำบนกระดาษ) = บิดา มารดา สามี ภรรยา บุตร เครือญาติ ดำรงตำแหน่งผู้จัดการบริษัท หรือเป็นหุ้นส่วนที่มีอำนาจบริหารในบริษัท/ห้างหุ้นส่วน · รับทราบ = ผู้บังคับบัญชาพิจารณาแล้ว (คำตัดสิน approve) · ถูกแทนที่ = ใบเดิมของปีเดียวกันเมื่อใบใหม่รับทราบแล้ว

## §0.12 Coverage Manifest
| แหล่ง | รายการ | ครอบคลุมที่ |
|---|---|---|
| ช่องในฟอร์ม (FORM_SPEC 10) | ประจำปี F01 · ข้าพเจ้า นาย/นาง/นางสาว F02 · ตำแหน่ง F03 · รายละเอียด F04 · ลงชื่อ/วันที่ F05/F06 · ข้อคิดเห็นของผู้บังคับบัญชา F07 · (ชื่อ)/ฝ่ายกฎหมาย/วันที่ F08–F10 | 01 §1.2 · 04 §4.2 · 03 FN-09 |
| ตัวเลือก | has_conflict (none/has) · คำตัดสิน รับทราบ/ส่งกลับแก้ไข | 01 · 04 · 05 BR-03/14 |
| ค่าคงที่ | ประจำปี (ปี) · ถ้อยคำรับรอง | 05 BR-01/02 (config) |
| ลายเซ็น | ผู้เปิดเผย · ผู้บังคับบัญชา (กรอบข้อคิดเห็น · "ฝ่ายกฎหมาย") | 03 FN-09 · 05 BR-14 · OQ-03 |
| Doc No./Rev. | FM-PUR-04 · REV.00 : 01/07/2569 | print_config (F-DOCCFG) |
| DEC | 18 ข้อ | 07 §7.0 |
