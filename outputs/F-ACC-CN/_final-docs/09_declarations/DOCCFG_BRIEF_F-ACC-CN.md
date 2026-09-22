# DOCCFG_BRIEF — F-ACC-CN ใบลดหนี้ลูกค้า (Credit Note)

> Auto-register ลง Document Configuration (F-DOCCFG) ตอน deploy · admin ปรับค่าได้ทุกช่องหลัง register
> **เลขทุกใบจาก `ENG-DOC-NUM.next()` · สำเนาทุกใบจาก `ENG-DOC-STORE.store()` — ห้าม hardcode รูปแบบเลข / +1 / เงื่อนไขเก็บสำเนา** (LD-06)
> **Supersedes** upstream `Pack Brief Feature/F-ACC-CN/5_DECLARATIONS/DOCCFG_BRIEF_F-ACC-CN.md` — จัดตาม FRD Pack + HTML `nextCode()` (ม.718)

---

## §1. doc_type ที่ประกาศ

| Code | ชื่อ | Module | Preset default | Reset | Scope | No-gap | Snap: ส่งออก | Snap: อนุมัติ+เซ็น |
|---|---|---|---|---|:--:|:--:|:--:|:--:|
| **CN** | ใบลดหนี้ (ลูกค้า) | ACC (AR) | `{PREFIX}-{YYYY}-{run:4}` → **CN-2026-0001** | รายปี | global `[DEFAULT]` | ✓ | ✓ | ✓ |

- **format = `CN-YYYY-NNNN`** — `YYYY` = ปี **ค.ศ. (Gregorian)** 4 หลัก · `NNNN` = running 4 หลัก zero-pad
- ตรง HTML `nextCode()` (ม.718): `DOC.prefix('CN') + '-' + TODAY_ISO.slice(0,4) + '-' + padStart(4,'0')` → ปี ค.ศ. ยืนยัน (LD-10 · date ค.ศ.)
- **no-gap ✓** — เลขต่อเนื่องไม่มีรู (เอกสารภาษี ม.86/10)
- code `CN` unique — ไม่ชนกับ registry (DN แยกตัว) · ถ้ามี CN ใน registry แล้ว = ใช้ entry เดิม ห้ามประกาศซ้ำ
- scope `global` = [DEFAULT] · จุดตัด global-vs-branch admin เคาะที่ F-DOCCFG หลัง register

---

## §2. จุดออกเลข (ENG-DOC-NUM)

| เมื่อไหร่ | อ้าง FRD | หมายเหตุ |
|---|---|---|
| `pending_approval → approved` (อนุมัติ**ขั้นสุดท้าย** ครบสาย) | 03_LOGIC FN-11 `issueCreditNote` · 05_RULES BR-08 · §5.2 | **ไม่ออกเลขตอน draft / ส่งอนุมัติ** — ออกตอน final approve เท่านั้น (no-gap Iron 4) |

- Dev: `cn.code = ENG-DOC-NUM.next('CN', company_ctx)` ภายใน transaction อนุมัติขั้นสุดท้าย (FN-11 step 1)
- **feature ไม่รันเลขเอง** — ห้าม format / ห้าม +1 / ห้ามอ่าน max(code) เอง (HTML `nextCode()` เป็น mock ของ prototype เท่านั้น)
- เลข immutable — ออกแล้วห้ามเปลี่ยน/renumber ไม่ว่า config เปลี่ยน (Iron 3)

---

## §3. จุดเก็บสำเนา (ENG-DOC-STORE)

| Event (flag) | เมื่อไหร่ | อ้าง FRD |
|---|---|---|
| `approved_final` | อนุมัติครบ + ลายเซ็น (พร้อมออกเลข) | 03_LOGIC FN-11 · FN-15 `formatCreditNotePdf` |
| `sent_external` | กด "ส่งใบลดหนี้ให้ลูกค้า" (email) — รวม resend | 03_LOGIC FN-10 `sendToCustomer` (API-09) · HTML `openSendCN` (ม.679) |

- Dev: render PDF (A4 ม.86/10 อ้างเลข+วันที่ใบเดิม + เดิม/ถูกต้อง/ผลต่าง/ภาษี/เหตุผล + legal_basis) แล้ว `ENG-DOC-STORE.store(pdf,'CN',cn_id,'<flag>')` — engine เช็ค flag เองว่าจะเก็บไหม

---

## §4. Dev wiring note

- `cn.code = ENG-DOC-NUM.next('CN', company_ctx)` ที่ transition §2 — ห้าม format เอง ห้าม +1 เอง
- `ENG-DOC-STORE.store(pdf,'CN',cn_id,'approved_final'|'sent_external')` ที่ event §3
- ห้ามอ่าน/เขียนตาราง config ตรง — ผ่าน engine API เท่านั้น
- ทุก default (preset/reset/scope/snapshot) admin แก้ได้ที่จอ F-DOCCFG — ไม่มีค่า "บังคับแก้ไม่ได้"

---

## §5. Open Questions / [ASSUMED]

| item | สถานะ |
|---|---|
| scope global vs branch | `[DEFAULT — global]` · admin เคาะที่ F-DOCCFG หลัง register (เชื่อม docnum global-vs-branch OQ ตระกูล AR) |
| reset รายปี ค.ศ. | ยืนยันตาม HTML `nextCode()` (ปี ค.ศ. · LD-10) — ไม่มี OQ |
