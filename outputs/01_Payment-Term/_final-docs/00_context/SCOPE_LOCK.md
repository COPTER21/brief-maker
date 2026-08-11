# SCOPE LOCK · Payment Term (F-PAY)

> พันธะที่ **ห้ามฝืน** — สืบทอดจาก PREBRIEF OB-1 (FRD 07_LOCKED เดิม) + มติเลน + มติ 2026-08-09
> ⚠️ FRD pack เดิม = v5.1 **stale** — LD ที่ระบุด้านล่างคือชุดที่ยืนยันใน PREBRIEF; LD ที่ไม่ได้ enumerate ให้ re-derive ตอน regen FRD (step 6) และ cross-check กับ HTML

## Logic / Design Locks (LD)
| LD | กติกา (ห้ามฝืน) |
|----|-----------------|
| LD-01 | payment term อยู่ที่ **PO/SO เท่านั้น** · PR ไม่มี · Quotation = ฝั่งขาย (proposal) เท่านั้น |
| LD-02 | GRN/Ship trigger ตามประเภท: Prepay/Deposit รอชำระ · ที่เหลือ = ทันที |
| LD-05 | เปลี่ยน type หลัง approve เอกสารไม่ได้ |
| LD-08 | deposit % inherit + ปรับได้ที่ PO/SO |
| LD-08b | **Credit trigger = ทันที (locked)** — แก้ไม่ได้ |
| LD-09 | installment inherit + ปรับได้ · รวมต้อง 100% |
| LD-10 | Partial: GRN กำหนดยอดจ่ายต่อรอบ |
| LD-15 | Installment ≠ Partial (คนละประเภท) |

## Pattern Locks (เลน VD-PDM)
- สถานะ 3 ค่า **อิสระ** (ร่าง ⇄ ใช้งาน ⇄ ไม่ใช้งาน) · ไม่มีอนุมัติ
- bulk ได้ · **ไม่มีลบเดี่ยว** · ตัด hint / field-help / panelInfo
- ★ ยกเว้นของเลน: **ไม่มีนำเข้า/ส่งออก CSV** (มติ 2026-08-09 — ผ่านฟอร์มเท่านั้น)
- flag `salesOnly` = misnomer ตัดออกแล้ว

## Governance / CI Locks
- **DOA:** ไม่มีสายอนุมัติ — placeholder 4 fields = null (approver_role / approved_by / approved_at / approval_chain)
- **NOTIF:** ไม่ emit
- **CI:** v8 CUBE **Warm Light** (Ivory/Charcoal · Red #FF3B30 · Orange #FF9A1F · Satoshi + Noto Sans Thai)
- **Iron Rules:** #94 Master Combobox · #95 Overlay Portal · #96 List Full-Height · #97 Responsive 768–1180 · **#29 Scroll Preservation** (_keepScroll 3 ชั้น)

## Central Plan contracts (ห้ามขัด)
- Soft-reference (LD-4C-02): master = picker · snapshot ค่าลงเอกสาร · ไม่มี FK cascade
- edges [config]: Payment Terms → PO / AR Invoice / AP Invoice
- Append-only audit · soft archive · ไม่มี hard delete
