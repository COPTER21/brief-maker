---
feature_id: F-ACC-DN
feature_name: Debit Note — ใบลดหนี้ผู้ขาย (ฝั่งซื้อ)
request_type: new
module: Accounting / AP
scope_lock_ref: CONTEXT_PACK W5-LITE §2 ข้อ 4 + §3 + GOLDEN_RULES 1–12
upstream_refs: briefs/W5Q/CHECKLIST.md#F-ACC-DN · workflow_graph AP Invoice→DN · BRD_F-ACC-APINV §12.1 (contract ap_open_item · input_vat_line)
confidence_overall: 82%
status: READY
date: 2026-09-20
---
# RIF v2 — Debit Note (ใบลดหนี้ผู้ขาย · ฝั่งซื้อ)

## §1 Header
| Field | Value |
|---|---|
| Feature | F-ACC-DN · Debit Note · new · Accounting/AP |
| Scope Lock Ref | CONTEXT_PACK W5-LITE §2 ข้อ 4 · GR 1–12 |
| Declarations (chip) | doa · ntf · csq · doccfg · pdfdoc ✅ |
| Dependency ในเลน | AP Invoice (F-ACC-APINV) = **ba-done ✓** (2026-09-20) — ใช้ contract ap_open_item / input_vat_line |

## §2 Context
- PAIN-01 คืนของ/ราคาเกินแล้วไม่ได้ลดหนี้ → จ่ายเกิน · PAIN-02 ลดหนี้เกินยอดค้าง/ซ้ำ · PAIN-03 ภาษีซื้อไม่ถูกลดตามใบลดหนี้
- GOAL-01 ลดหนี้ผู้ขายอ้างใบตั้งหนี้ถูกต้อง · GOAL-02 ไม่เกินยอดคงเหลือ · GOAL-03 อนุมัติตามมูลค่า + ลดภาษีซื้อถูกเดือน

## §3 Roles & Permissions
| role_id | ชื่อ | Action |
|---|---|---|
| R-01 role-officer-ap [ASSUMED] | เจ้าหน้าที่เจ้าหนี้ | A-01 สร้าง · A-02 ร่าง · A-03 แก้ร่าง · A-04 ส่งอนุมัติ · A-07 ส่งผู้ขาย · A-08 ยกเลิก |
| R-02 role-mgr-pur | ผู้จัดการจัดซื้อ | A-05/A-06 ขั้น 1 |
| R-03 role-mgr-acc [ASSUMED] | ผู้จัดการบัญชี | A-05/A-06 ขั้น 2 |
| R-04 role-cfo | CFO | A-05/A-06 ขั้น 3 |
### 3.3 Approval Chain — DOA-ACC-DN ตามมูลค่า · slot picker เลือกคน · ห้าม hardcode

## §4 As-Is
AS-01 หักยอดตอนจ่ายโดยไม่มีเอกสาร · AS-02 อนุมัติทางแชท · AS-03 ภาษีซื้อไม่ปรับ

## §5 Target Journey
| JRN | Step | ผู้ทำ | หน้า | Action | ผล |
|---|---|---|---|---|---|
| JRN-01 | เลือกใบตั้งหนี้ที่ยังค้างจ่าย | R-01 | P-02 s1 | A-01 | ดึงผู้ขาย + บรรทัด |
| JRN-02 | เลือกเหตุผล (คืนของ → อ้าง RTV W3-LITE mock) | R-01 | P-02 s2 | — | โหมดลดจำนวน/ราคา |
| JRN-03 | ระบุจำนวน/ราคาที่ลด ≤ คงเหลือ | R-01 | P-02 s3 | — | ภาษีซื้อลดตาม |
| JRN-04 | ส่งอนุมัติ → เลือกคนต่อขั้น | R-01 | modal | A-04 | pending_approval |
| JRN-05 | อนุมัติครบ → เลข DN · dn_applied ใบตั้งหนี้ · ภาษีซื้อลด · JE mock | R-02..04 | P-03 | A-05 | approved |
| JRN-06 | ส่งผู้ขาย | R-01 | P-03 | A-07 | sent |

## §6 Pages: P-01 #/list · P-02 #/create #/edit/:id (wizard 5) · P-03 #/view/:id (tabs + "ใบตั้งหนี้อ้างอิง · ภาษีซื้อ")
## §7 Fields: ใบตั้งหนี้อ้างอิง (lookup ap_open_item) · ผู้ขาย (readonly) · วันที่ใบลดหนี้ (≥ วันที่ใบกำกับเดิม) · เหตุผล (master) · RTV (เมื่อคืนของ) · คำอธิบายเหตุผล (≥10) · เลขที่ใบลดหนี้จากผู้ขาย (ถ้ามี) · หมายเหตุ · line: สินค้า(ล็อก)/จำนวนลด/ราคาลดต่อหน่วย/VAT
## §8 Actions: A-01..A-11 (เหมือน CN · A-07 = ส่งผู้ขาย)
## §9 State Machine: draft → pending_approval → approved → sent · pending→draft · draft/pending→cancelled
## §10 Business Rules
RULE-01 อ้างได้เฉพาะใบตั้งหนี้ approved ที่ outstanding > 0 · RULE-02 ยอด DN ≤ outstanding (ตอนส่ง + ตอนอนุมัติ) · RULE-03 จำนวนลด ≤ จำนวนเดิม − ลดแล้ว · RULE-04 ราคาลด ≤ ราคาเดิม · RULE-05 เหตุผล master (คืนของ RTV / ราคาเกิน / ของขาด) · RULE-06 คืนของต้องอ้าง RTV ของใบเดียวกัน [ASSUMED contract] · RULE-07 DOA ตามมูลค่า · RULE-08 เลข DN ตอนอนุมัติครบ · RULE-09 อนุมัติ → dn_applied_amount ใบตั้งหนี้ + input_vat_line ติดลบ + JE mock · RULE-10 ลดภาษีซื้อในเดือนที่ออก/ได้รับใบลดหนี้ · RULE-11 ลดลอยไม่อ้างใบ = ปิด [ASSUMED ตาม OQ-CN-01] · RULE-12 ผู้ขอไม่อนุมัติเอง
## §11 Data: M-01 ap_open_item (F-ACC-APINV) · M-02 RTV (W3-LITE mock) · M-03 DN reason master [ASSUMED config] · M-04 DOA entry · entity debit_note 1—N debit_note_line → ap_invoice_line (soft)
## §12 Volume ~60 ใบ/เดือน · §13 Integration: AP Invoice (in) · RTV (in mock) · PV (อ่าน outstanding) · VAT ซื้อ (out) · JE (out mock)
## §14 Edge: ใบตั้งหนี้ถูกจ่ายเพิ่มระหว่างรออนุมัติ → re-check · ลดหลายรอบ · จ่ายครบแล้ว → ไม่โผล่ (เรียกคืนเงิน = OQ-DN-03)
## §15 KPI: DN เกินคงเหลือ = 0 · อนุมัติ ≤ 1 วัน · DN ไม่อ้างใบ/ไม่มีเหตุผล = 0
## §16 Meta
| Q | คำถาม | owner |
|---|---|---|
| OQ-DN-01 | ลดลอยไม่อ้างใบ ปิด [ASSUMED ตาม OQ-CN-01] | Strike |
| OQ-DN-02 | tier DOA ≤50k/≤300k/>300k [DEFAULT] | Policy Center |
| OQ-DN-03 | ใบตั้งหนี้จ่ายครบแล้ว → เรียกเงินคืน | Strike + Finance |
| OQ-DN-04 | ยกเลิก DN หลังอนุมัติ | Strike |
| OQ-DN-05 | ภาษีซื้อลดเดือนที่ออก DN หรือเดือนที่ได้รับใบลดหนี้ผู้ขาย [ASSUMED เดือนวันที่ใบลดหนี้] | Tax |
| LOCK | ข้อความ | อ้าง |
|---|---|---|
| LOCK-01 | Q-document + B2 v2 | GR-2 |
| LOCK-02 | อ้าง AP Invoice ในเลน (หลัง AP ba-done) | §2 ข้อ 4 |
| LOCK-03 | เหตุผล: คืนของ RTV (mock) / ราคาเกิน / ของขาด | §2 ข้อ 4 |
| LOCK-04 | ลดไม่เกินยอดคงเหลือ | §2 ข้อ 4 |
| LOCK-05 | DOA ตามมูลค่า | §2 ข้อ 4 |
| LOCK-06 | doccfg DN-YYYY-NNNN · pdfdoc ใบลดหนี้ฝั่งซื้อ (อ้างเลขใบเดิม + เหตุผล) | §2 ข้อ 4 · user rule |
| LOCK-07 | VAT ซื้อระบุใน BRD | §2 ข้อ 4 |
| LOCK-08 | RTV/JE = mock [ASSUMED contract] | GR-5 |
| LOCK-09 | UI #67.1/#104/#105/#106 BLOCK · ค.ศ. · append-only | GR |
Confidence 82% READY
