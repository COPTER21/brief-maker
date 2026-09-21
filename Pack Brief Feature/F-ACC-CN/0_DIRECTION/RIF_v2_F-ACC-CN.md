---
feature_id: F-ACC-CN (F096)
feature_name: Credit Note — ใบลดหนี้ลูกค้า
request_type: new
module: Accounting / AR
scope_lock_ref: CONTEXT_PACK W5-LITE §2.2 + §3 (OQ-CN-01) + GOLDEN_RULES 1–12
upstream_refs: briefs/W5P/CHECKLIST.md#F-ACC-CN · workflow_graph edge F-ACC-ARINV→F-ACC-CN · BRD_F-ACC-ARINV §12.1 (contract ar_open_item) · FEATURE_LIST F096/F090
confidence_overall: 83%
status: READY
date: 2026-09-20
---
# RIF v2 — Credit Note (ใบลดหนี้ลูกค้า)

## §1 Header
| Field | Value |
|---|---|
| Feature | F-ACC-CN · Credit Note · new · Accounting/AR |
| Scope Lock Ref | CONTEXT_PACK W5-LITE §2.2 · §3 OQ-CN-01 · GR 1–12 |
| Declarations (chip) | doa · ntf · csq · doccfg · pdfdoc ✅ (F096) |
| Dependency ในเลน | AR Invoice (F-ACC-ARINV) = **ba-done ✓** (2026-09-20) — ใช้ contract ar_open_item |

## §2 Context
- PAIN-01 ลดหนี้ด้วยการแก้ใบแจ้งหนี้เดิม (ผิดกฎหมายภาษี) · PAIN-02 ลดเกินยอดคงค้าง/ลดซ้ำ · PAIN-03 ไม่มีสายอนุมัติตามมูลค่า
- GOAL-01 ออกใบลดหนี้อ้างใบแจ้งหนี้ถูกต้องตาม ม.86/10 · GOAL-02 ลดไม่เกินยอดคงเหลือ (OQ-CN-01) · GOAL-03 อนุมัติตามมูลค่าผ่าน DOA

## §3 Roles & Permissions
| role_id | ชื่อ | Action |
|---|---|---|
| R-01 role-officer-ar [ASSUMED] | เจ้าหน้าที่ลูกหนี้ | A-01 สร้าง · A-02 ร่าง · A-03 แก้ร่าง · A-04 ส่งอนุมัติ · A-07 ส่งลูกค้า · A-08 ยกเลิกร่าง |
| R-02 role-mgr-sales | ผู้จัดการฝ่ายขาย | A-05/A-06 อนุมัติ/ไม่อนุมัติ (ขั้นตาม DOA) |
| R-03 role-mgr-acc [ASSUMED] | ผู้จัดการบัญชี | A-05/A-06 |
| R-04 role-cfo | CFO | A-05/A-06 (tier สูง) |
### 3.3 Approval Chain — resolve จาก DOA entry ของ F-ACC-CN ตามมูลค่า (DOA_BRIEF) · slot picker เลือกคน · ห้าม hardcode

## §4 As-Is
AS-01 แก้ยอดในใบแจ้งหนี้เดิม · AS-02 อนุมัติทางแชท · AS-03 ไม่เชื่อมยอดค้าง (PAIN-01..03)

## §5 Target Journey
| JRN | Step | ผู้ทำ | หน้า | Action | ผล |
|---|---|---|---|---|---|
| JRN-01 | เลือกใบแจ้งหนี้ที่มียอดคงค้าง | R-01 | P-02 s1 | A-01 | ดึงลูกค้า+บรรทัด |
| JRN-02 | เลือกเหตุผล (master) · ถ้ารับคืน เลือกใบรับคืน (W4-LITE mock) | R-01 | P-02 s2 | — | กำหนดโหมดบรรทัด |
| JRN-03 | ระบุจำนวน/มูลค่าที่ลด ≤ คงเหลือ | R-01 | P-02 s3 | — | VAT ลดตาม |
| JRN-04 | ส่งอนุมัติ → เลือกคนต่อขั้น | R-01 | P-03 modal | A-04 | pending_approval |
| JRN-05 | อนุมัติครบ → ออกเลข CN · ลดยอดค้าง AR · JE mock | R-02..04 | P-03 | A-05 | approved |
| JRN-06 | ส่งลูกค้า | R-01 | P-03 | A-07 | sent + snapshot |

## §6 Pages
| P | ชื่อ | route | layout |
|---|---|---|---|
| P-01 | รายการใบลดหนี้ | #/list | list-view |
| P-02 | สร้าง/แก้ไข (wizard 5) | #/create · #/edit/:id | form-wizard |
| P-03 | ดูใบลดหนี้ | #/view/:id | detail-tabs |

## §7 Fields (สรุป — full ใน PREBRIEF §3)
ใบแจ้งหนี้อ้างอิง (lookup ar_open_item · Y) · ลูกค้า (readonly) · วันที่ใบลดหนี้ (date · Y · ≥ วันที่ใบเดิม) · เหตุผล (select master · Y) · ใบรับคืน (lookup SR · เมื่อเหตุผล=รับคืน) · คำอธิบายเหตุผล (textarea · Y ≥10) · พนักงานขาย (lookup) · หมายเหตุ · line: สินค้า(ล็อกจากใบเดิม)/จำนวนลด/ราคาต่อหน่วยที่ลด/VAT

## §8 Actions
A-01 สร้าง · A-02 บันทึกแบบร่าง · A-03 แก้ไข · A-04 ส่งอนุมัติ (slot picker) · A-05 อนุมัติ · A-06 ไม่อนุมัติ (เหตุผล) · A-07 ส่งให้ลูกค้า · A-08 ยกเลิก (draft/pending · เหตุผล) · A-09 CSV · A-10 PDF · A-11 ทำสำเนา

## §9 State Machine
| จาก | Action | ไป | เงื่อนไข |
|---|---|---|---|
| — | A-02 | draft | — |
| draft | A-04 | pending_approval | ≤ คงเหลือ · DOA resolve |
| pending_approval | A-05 ครบสาย | approved | re-check ≤ คงเหลือ → ออกเลข CN |
| pending_approval | A-06 | draft | เหตุผล · ประวัติ append-only |
| draft/pending | A-08 | cancelled | เหตุผล |
| approved | A-07 | sent | — |

## §10 Business Rules
RULE-01 อ้างใบแจ้งหนี้ได้เฉพาะ issued/sent ที่ outstanding > 0 (FIXED) · RULE-02 ยอด CN ≤ outstanding ใบอ้างอิง ณ ส่งและ ณ อนุมัติ (FIXED · OQ-CN-01) · RULE-03 จำนวนลดต่อบรรทัด ≤ จำนวนใบเดิม − ลดแล้ว (FIXED) · RULE-04 ราคาลดต่อหน่วย ≤ ราคาเดิม (FIXED) · RULE-05 เหตุผลจาก master config (CONFIGURABLE) · RULE-06 รับคืน = ต้องอ้างใบรับคืน W4-LITE (FIXED [ASSUMED contract]) · RULE-07 DOA ตามมูลค่า (CONFIGURABLE ผ่าน DOA กลาง) · RULE-08 เลข CN ออกตอนอนุมัติครบ (no-gap) · RULE-09 อนุมัติ → cn_applied ของใบเดิมเพิ่ม + JE mock (Dr รับคืน/ส่วนลด · Dr ภาษีขาย · Cr ลูกหนี้) · RULE-10 ลดภาษีขายในเดือนที่ออกใบลดหนี้ (ม.82/10) · RULE-11 ลดหนี้ลอยไม่อ้างใบ = ปิด (OQ-CN-01) · RULE-12 ผู้ขอไม่อนุมัติใบตัวเอง (BR-DOA-04)

## §11 Data
M-01 ar_open_item (F-ACC-ARINV) · M-02 Sales Return (F090 W4-LITE mock) · M-03 CN reason master [ASSUMED config] · M-04 DOA entry · M-05 Employee · entity credit_note 1—N credit_note_line → ar_invoice_line (soft)

## §12 Volume: ~120 ใบ/เดือน · SLA page p95<3s
## §13 Integration: IO-01 AR Invoice (in · contract) · IO-02 Sales Return W4-LITE (in · mock) · IO-03 VAT Report (out) · IO-04 JE F093 (out · mock) · IO-05 RV (อ่าน outstanding หลังลด)
## §14 Edge: EDGE-01 ใบเดิมถูกชำระเพิ่มระหว่างรออนุมัติ → re-check ตอนอนุมัติ · EDGE-02 ลดหลายรอบ · EDGE-03 ใบเดิม void → CN ที่ร่างค้างอ้างไม่ได้ · EDGE-04 ใบชำระครบแล้ว → ไม่โผล่ (คืนเงิน = ไม่รองรับ LITE)
## §15 KPI: KPI-01 CN เกินคงเหลือ = 0 · KPI-02 เวลาอนุมัติเฉลี่ย ≤ 1 วัน · KPI-03 CN ไม่มีเหตุผล/ไม่อ้างใบ = 0
## §16 Meta
| Q | คำถาม | owner |
|---|---|---|
| OQ-CN-01 | ลดไม่เกินคงเหลือ · ลดลอยปิด | Strike |
| OQ-CN-02 | ยกเลิกหลังอนุมัติ | Strike |
| OQ-CN-03 | ใบชำระครบแล้วต้องการลดหนี้ (คืนเงิน) | Strike + Finance |
| OQ-CN-04 | tier DOA (≤50k / ≤300k / >300k) | Policy Center |
| LOCK | ข้อความ | อ้าง |
|---|---|---|
| LOCK-01 | Q-document + B2 v2 | §2 · GR-2 |
| LOCK-02 | อ้าง AR Invoice (ในเลน · หลัง AR ba-done) | §2.2 |
| LOCK-03 | เหตุผล master config: รับคืน (SR mock)/ส่วนลดภายหลัง/ผิดราคา | §2.2 |
| LOCK-04 | ลดไม่เกินยอดคงเหลือใบอ้างอิง (OQ-CN-01) | §3 |
| LOCK-05 | DOA slot picker ตามมูลค่า | §2.2 · GR-3 |
| LOCK-06 | doccfg CN-YYYY-NNNN + pdfdoc อ้างเลขใบเดิม+เหตุผลตามประกาศสรรพากร | §2.2 |
| LOCK-07 | ระบุผลกระทบ VAT ขายใน BRD | §2.2 |
| LOCK-08 | dep ข้ามเลน (Sales Return/JE) = mock [ASSUMED contract] | GR-5 |
| LOCK-09 | UI #67.1/#104/#105/#106 BLOCK | GR-8..11 |
| LOCK-10 | ค.ศ. · append-only | GR-1,4 |
Confidence 83% READY
