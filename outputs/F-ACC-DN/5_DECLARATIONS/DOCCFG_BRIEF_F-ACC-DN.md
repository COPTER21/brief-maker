# DOCCFG_BRIEF — F-ACC-DN ใบลดหนี้ผู้ขาย (Debit Note)

> Auto-register ลง Document Configuration (F-DOCCFG) ตอน deploy · admin ปรับค่าได้ทุกช่องหลัง register
> **เลขทุกใบจาก `ENG-DOC-NUM.next()` · สำเนาทุกใบจาก `ENG-DOC-STORE.store()` — ห้าม hardcode รูปแบบเลข / +1 / เงื่อนไขเก็บสำเนา**
> **Supersedes** upstream `Pack Brief Feature/F-ACC-DN/5_DECLARATIONS/DOCCFG_BRIEF_F-ACC-DN.md` (stub) — จัดตาม FRD Pack + HTML `nextCode()`
> **Mirror ของ F-ACC-CN** — code แยกตัว (DN ≠ CN)

---

## §1. doc_type ที่ประกาศ

| Code | ชื่อ | Module | Preset default | Reset | Scope | No-gap | Snap: ส่งออก | Snap: อนุมัติ+เซ็น |
|---|---|---|---|---|:--:|:--:|:--:|:--:|
| **DN** | ใบลดหนี้ผู้ขาย (ฝั่งซื้อ) | ACC (AP) | `{PREFIX}-{YYYY}-{run:4}` → **DN-2026-0001** | รายปี | global `[DEFAULT]` | ✓ | ✓ | ✓ |

- **format = `DN-YYYY-NNNN`** — `YYYY` = ปี **ค.ศ. (Gregorian)** 4 หลัก · `NNNN` = running 4 หลัก zero-pad
- ตรง HTML `nextCode()`: `DOC.prefix('DN') + '-' + TODAY_ISO.slice(0,4) + '-' + padStart(4,'0')` → ปี ค.ศ. ยืนยัน (date ค.ศ.)
- **no-gap ✓** — เลขต่อเนื่องไม่มีรู (เอกสารภาษี ม.86/10)
- code `DN` unique — ไม่ชนกับ registry (CN แยกตัว) · ถ้ามี DN ใน registry แล้ว = ใช้ entry เดิม ห้ามประกาศซ้ำ
- scope `global` = [DEFAULT] · จุดตัด global-vs-branch admin เคาะที่ F-DOCCFG หลัง register

---

## §2. จุดออกเลข (ENG-DOC-NUM)

| เมื่อไหร่ | อ้าง FRD | หมายเหตุ |
|---|---|---|
| `pending_approval → approved` (อนุมัติ**ขั้นสุดท้าย** ครบสาย) | 03_LOGIC FN-12 `issueDebitNote` · 05_RULES BR-08 · §5.2 | **ไม่ออกเลขตอน draft / ส่งอนุมัติ** — ออกตอน final approve เท่านั้น (no-gap Iron 4) |

- Dev: `dn.code = ENG-DOC-NUM.next('DN', company_ctx)` ภายใน transaction อนุมัติขั้นสุดท้าย (FN-12 step 1)
- **feature ไม่รันเลขเอง** — ห้าม format / ห้าม +1 / ห้ามอ่าน max(code) เอง (HTML `nextCode()` เป็น mock ของ prototype เท่านั้น)
- เลข immutable — ออกแล้วห้ามเปลี่ยน/renumber ไม่ว่า config เปลี่ยน (Iron 3)

---

## §3. จุดเก็บสำเนา (ENG-DOC-STORE)

| Event (flag) | เมื่อไหร่ | อ้าง FRD |
|---|---|---|
| `approved_final` | อนุมัติครบ + ลายเซ็น (พร้อมออกเลข) | 03_LOGIC FN-12 · FN-92 `formatDebitNotePdf` |
| `sent_external` | กด "ส่งใบลดหนี้ให้ผู้ขาย" (email) — รวม resend | 03_LOGIC FN-16 `sendToVendor` (API-09) · HTML `openSendDN` |

- Dev: render PDF (A4 ม.86/10 อ้างเลข+วันที่ใบกำกับเดิมของผู้ขาย + เดิม/ถูกต้อง/ผลต่าง/**ภาษีซื้อ** + เหตุผล + legal_basis) แล้ว `ENG-DOC-STORE.store(pdf,'DN',dn_id,'<flag>')` — engine เช็ค flag เองว่าจะเก็บไหม

---

## §4. Dev wiring note

- `dn.code = ENG-DOC-NUM.next('DN', company_ctx)` ที่ transition §2 — ห้าม format เอง ห้าม +1 เอง
- `ENG-DOC-STORE.store(pdf,'DN',dn_id,'approved_final'|'sent_external')` ที่ event §3
- ห้ามอ่าน/เขียนตาราง config ตรง — ผ่าน engine API เท่านั้น
- ทุก default (preset/reset/scope/snapshot) admin แก้ได้ที่จอ F-DOCCFG — ไม่มีค่า "บังคับแก้ไม่ได้"

---

## §5. Open Questions / [ASSUMED]

| item | สถานะ |
|---|---|
| scope global vs branch | `[DEFAULT — global]` · admin เคาะที่ F-DOCCFG หลัง register (เชื่อม docnum global-vs-branch OQ ตระกูล AP) |
| reset รายปี ค.ศ. | ยืนยันตาม HTML `nextCode()` (ปี ค.ศ.) — ไม่มี OQ |
