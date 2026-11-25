# 00_OVERVIEW — F-TMP-002 แบบฟอร์มยืมสินทรัพย์ (Asset Borrowing)

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD | FRD-F-TMP-002 v1.0 · frd-generator-v6 · **Input Mode 0** (prebrief-to-devpack v2) |
| Variant | **FULL** (pages=3, states=5, approval=Y, money=N) |
| Source | BRD-ASM-ALN-001 (APPROVED · Prebrief Mode) · PREBRIEF_REQ-TMP-002_v2 · FORM_SPEC FM-ASM-04 · DECISIONS.lock (13 DEC · AI-DEFAULT 11) · feature.html (html-generator-v9.4 · audit FAIL 0 · self_audit PASS · e2e jsdom 32/32 — [NO-BROWSER]) |
| Module / Area | Asset Management · Core Cube |
| Status | Ready for Dev (หลัง OQ-03/04/06 ปิด) |
| Date | 2026-10-11 |

## §0.2 Revision History
| v | วันที่ | เปลี่ยน |
|---|---|---|
| 1.0 | 2026-10-11 | สร้างจาก doc-master-pipeline ขั้น 7 (unattended) |

## §0.3 Scope
### In Scope
รายการ · สร้าง/แก้ร่าง (3 ขั้น) · ดู 4 แท็บ · เลือกทะเบียนสินทรัพย์ · DOA dynamic (ค่าเริ่ม 1 ขั้น ผู้ให้ยืม) · จำนวนที่ให้ยืม · ไม่ให้ยืม→กลับร่าง · ยกเลิก · บันทึกรับคืน · เลยกำหนดคืน (เตือน) · แนบไฟล์ · PDF FM-ASM-04 Replica · เลข ALN · CSV
### Out of Scope
อัปเดตสถานะ/ผู้ถือครองใน Asset Master (DEC-01) · ส่งต่อระบบอื่น (DEC-02) · ตรวจยืมซ้อนข้ามใบ (OQ-05) · รับคืนบางส่วน · ประกาศ

## §0.4 Roles (COSO)
| Role | COSO | id |
|---|---|---|
| ผู้ยืม (พนักงาน) | Maker | owner |
| ผู้ให้ยืม | Approver + Custodian | role-mgr-acc (ค่าเริ่ม DOA · module asset) |
| เจ้าหน้าที่บริหารสินทรัพย์ (admin view) | Checker (ติดตาม) · ผู้รับคืน | role ใหม่ — ยังไม่อยู่ใน DOA master (OQ-03) |

## §0.5 Dependencies
### Upstream
HR · Employee (ชื่อ/ตำแหน่ง · อ่าน) · Organization (Department · Company header/logo) · Asset Management · Asset Master (code/name · อ่าน) · F-DLG-001 DOA (resolve) · F-DOCCFG/F003 (doc_type ALN · status · print_config)
### Downstream
ENG-NOTIFY (aln_cancelled · aln_returned · aln_overdue) · ENG-DOC-STORE (approved_final) · Asset Master สถานะถือครอง (ประกาศ event `aln.approved` / `aln.returned` — **ไม่ยิงรอบนี้** DEC-02) · Report area (อ่าน)
### External
Document Center (ไฟล์แนบ)

## §0.6 Stack
FE: SPA module `#/asset-borrow` (feature.html = source of truth) · BE: REST `/api/v1/asset-borrows` · PDF render ฝั่ง server จาก `form.tpl.html` (logic-less) + data contract (03 FN-08)

## §0.7 Multi-Tenant & Security
PostgreSQL RLS ต่อ tenant · สิทธิ์ดูตาม 05 §5.3 · audit append-only
### §0.7.1 Data Classification Summary
Internal: เอกสาร/รายการสินทรัพย์ · Confidential(PII): ชื่อผู้ยืม/ผู้รับคืน snapshot

## §0.8 Open Questions
| OQ | เรื่อง | เจ้าของ | Block |
|---|---|---|---|
| OQ-01 | ตัวชี้วัด | ลูกค้า | – |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC AI-DEFAULT (11 ข้อ) | Strike | ก่อน UAT |
| OQ-03 | role admin ฝ่ายบริหารสินทรัพย์ / ผู้ให้ยืม = role-mgr-acc ตรง master DOA ไหม | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | Asset Master field (code/name/category) | พี่เบิร์ด | ก่อน dev |
| OQ-05 | ตรวจยืมซ้อน + อัปเดตสถานะทะเบียน | ลูกค้า | – |
| OQ-06 | รหัส feature/REQ จริง · taxonomy function_code · module enum F185 ไม่มี Asset | Strike | ก่อน register |

## §0.9 Glossary
ผู้ให้ยืม = ผู้ดูแลสินทรัพย์ที่อนุมัติให้ยืม · จำนวนที่ให้ยืม = จำนวนที่อนุญาตจริง (≤ ที่ขอ) · วันที่ส่งคืน = กำหนดคืน · รับคืน = บันทึกว่าได้รับคืนครบ

## §0.10 Pack Navigation
00 ภาพรวม · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED (DEC) · INDEX · declarations/

## §0.12 Coverage Manifest
| แหล่ง | รายการ | อยู่ที่ |
|---|---|---|
| ช่องในฟอร์ม F01–F13 (FORM_SPEC) | doc_no · requester name/position/dept · purpose · items(seq/asset_name/asset_code/qty_requested/qty_lent/borrow_date/return_date/remark) | 01 §1.2 · 04 §4.2 · 03 FN-01/FN-08 |
| ลายเซ็น S1–S4 | ผู้ยืม · ผู้ให้ยืม (DOA) · ผู้ส่งคืน · ผู้รับคืน | 03 FN-04/05/07/08 · 04 return_* |
| BRD S-01..S-13 | stories | 06 AC-01..AC-14 |
| BRD BR-01..11 · VR-01..08 · EC-01..09 | rules | 05 §5.1 / §5.4 / §5.5 |
| DEC-01..13 | มติ | 07 §7.0 |
| declaration | DOA · NTF · DOCCFG · MDOC | declarations/ · 03 FN-03/04/05/06/09 |
| หน้าจอ HTML | P-01 · P-02 · P-03 · M-01..06 | 01 §1.1 |
ไม่มี requirement หล่น
