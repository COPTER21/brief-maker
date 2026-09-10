# DOCCFG_BRIEF — F-HR-EXPENSE · เบิกค่าใช้จ่าย (F101 · Expense Claim)

> Auto-register ลง Document Configuration (F-DOCCFG) ตอน deploy · admin ปรับค่าได้ทุกช่องหลัง register
> เลขทุกใบจาก `ENG-DOC-NUM.next()` เท่านั้น · สำเนาทุกใบจาก `ENG-DOC-STORE.store()` เท่านั้น — **ห้าม hardcode รูปแบบเลข / +1 เอง / เงื่อนไขเก็บสำเนา**
> ตรวจ registry สดจาก `Related context/f-doccfg/f-doccfg.html` (TYPES + FMT_PRESETS) เมื่อ 2026-09-10

## ผลตรวจ registry (code collision)

**ประกาศ doc_type ใหม่** — `EXP` ยังไม่มีใน registry ปัจจุบัน (TYPES = QT/SO/PICK/PACK/DLV/INV/RV/CN/DN/JE/PR/PO/GRN) → ไม่ชน · code `EXP` (3 ตัว A-Z · unique) ผ่านกติกา
⚠️ **MODULES registry ไม่มี `HR`** (มีแค่ SAL/PUR/WMS/ACC/FIN) → ต้องเพิ่ม module HR หรือให้ BA เคาะ module owner ก่อน register (OQ-DOCCFG-05)

## doc_type ที่ประกาศ

| Code | ชื่อ | Module | Preset default (สังเกตจาก HTML) | Reset | Scope | No-gap | Snap: ส่งออก | Snap: อนุมัติ+เซ็น |
|---|---|---|---|---|---|---|---|---|
| `EXP` | ใบเบิกค่าใช้จ่าย | HR ⚠️(ไม่มีใน registry) | `{PREFIX}-{BBBB}-{run:4}` → `EXP-<พ.ศ.>-NNNN` | รายปี (พ.ศ.) | branch (แยกบริษัท) ⚠️ | yes | — (ใบภายใน · ไม่ส่งลูกค้า) | ✓ (`approved_final`) |

**รูปแบบเลขที่สังเกตได้จริง (expense.html · ห้ามถือเป็น production value):**
- `EXP.docSeq=(EXP.docSeq||2)+1; d.code='EXP-2569-'+String(EXP.docSeq).padStart(4,'0')` (L2462–2463)
- ปีในเลข = **2569 = พ.ศ. (Buddhist year)** → preset ที่ตรงคือ `{PREFIX}-{BBBB}-{run:4}` (รหัส-ปี **พ.ศ.**-เลขรัน) **ไม่ใช่** `{PREFIX}-{YYYY}-{run:4}` (ค.ศ. · = default ของ registry) → ดู OQ-DOCCFG-02
- **zero-pad 4 หลัก** (`padStart(4,'0')` → `0001`, `0003`, …)
- **ตัวนับ global เดินหน้าอย่างเดียว** (ไม่อิง count สถานะ → ไม่ซ้ำ · monotonic · FN-11 · FIX-06)

## จุดออกเลข — ENG-DOC-NUM

| เมื่อไหร่ (transition) | อ้าง FRD | หมายเหตุ |
|---|---|---|
| `pending_approval → approved` (อนุมัติครบสาย) | 03_LOGIC FN-07 (final chain) → **FN-11 `issueDocNumber`** · 05_RULES BR-06 (LOCK-02) | ออกเลข**ครั้งเดียวตอนอนุมัติครบทุกขั้น** · ไม่ออกตอน draft/submit/pending (no-gap · กันเลขเปลือง) |

- **`doc_no` nullable ก่อนอนุมัติ** — ยืนยันจาก 04_DB `T_expense_claim.doc_no varchar(20) NULL` (draft/pending แสดง `(ร่าง)`/`(รออนุมัติ)`) · UNIQUE(tenant_id, doc_no) WHERE doc_no IS NOT NULL
- **immutable หลังออกเลข** — แม้ admin เปลี่ยน config ภายหลัง เอกสารเดิมคงเลขเดิม (BR-06) · `rejected → reopen → draft` ไม่ล้างเลขที่ออกแล้ว (แต่ reject เกิดก่อน approved จึงยังไม่มีเลข → ไม่เผาเลข)
- ตัวนับเดินหน้าอย่างเดียว → **monotonic · ไม่ reuse · ไม่ renumber**

## จุดเก็บสำเนา — ENG-DOC-STORE

| Event | เมื่อไหร่ | อ้าง FRD | flag |
|---|---|---|---|
| `approved_final` | อนุมัติครบสาย → snapshot PDF a4 (หัวบริษัท + รายการ + ยอด + ช่องลายเซ็น 3 ช่อง) immutable | 03_LOGIC **FN-23 `snapshotPdf`** (เรียกจาก FN-07 final) · PREBRIEF S-15 · 05_RULES BR-06 | Snap: อนุมัติ+เซ็น ✓ |
| ~~`sent_external`~~ | **ไม่ใช้** — ใบเบิกเป็นเอกสารภายใน ไม่ส่งลูกค้า/e-Tax | — | — |

## Dev wiring note

- `claim.doc_no = ENG-DOC-NUM.next('EXP', company_ctx)` ใน **FN-11 เท่านั้น** (เรียกจาก FN-07 ตอน chain ครบ) — ห้าม format เอง ห้าม +1 เอง ห้ามใช้เลข mock (`docSeq`) จาก HTML เป็น production value
- render PDF แล้วเรียก `ENG-DOC-STORE.store(pdf,'EXP',claim_id,'approved_final')` ใน FN-23 — engine เช็ค flag เองว่าเก็บหรือไม่
- ห้ามอ่าน/เขียนตาราง config ตรง — ผ่าน engine API เท่านั้น
- admin ปรับ format / reset / scope / no-gap / snapshot flags ได้ที่จอ F-DOCCFG — feature ไม่ล็อกค่าเหล่านี้ (มติ 2026-08-11 · แก้ได้ทุกช่อง)

## Open Questions — BA/Finance เคาะก่อน register (ห้ามเดา · dev เอาไปตั้งค่า engine จริง)

| id | เรื่อง | สังเกต / default ที่ประกาศ | ต้องเคาะอะไร |
|---|---|---|---|
| OQ-DOCCFG-01 | **Series key ปลายทาง** | HTML mock ใช้ code `EXP` (unique ใน registry) | ยืนยันว่า production ENG-DOC-NUM ใช้ series key `EXP` (ไม่มี series HR-expense เดิมภายใต้ code อื่น) |
| OQ-DOCCFG-02 | **ปี ค.ศ. vs พ.ศ.** | HTML ใช้ **พ.ศ. (2569)** → preset `{PREFIX}-{BBBB}-{run:4}` · registry default = ค.ศ. `{PREFIX}-{YYYY}-{run:4}` | เลือก preset ปี (พ.ศ./ค.ศ.) — กระทบขอบเขต reset ประจำปี |
| OQ-DOCCFG-03 | **Reset cadence** | ประกาศ `รายปี` (จากรูปแบบเลขมีปี) | ยืนยันตัดรอบรายปี (ตามปีปฏิทินอะไร) + ตัวนับ reset **ต่อบริษัท/สาขา หรือ global** |
| OQ-DOCCFG-04 | **Scope numbering** | BA brief ประกาศ `branch (แยกบริษัท)` แต่ **HTML mock ใช้ตัวนับ global เดียว** (ไม่แยก company/branch) — **DIVERGENCE** | เลือก scope จริง: `global` (รวมทั้งระบบ) vs `branch` (แยกต่อสาขา/บริษัท) — HTML mock ยังไม่ segregate |
| OQ-DOCCFG-05 | **Module owner** | registry MODULES ไม่มี `HR` (SAL/PUR/WMS/ACC/FIN) | เพิ่ม module `HR` ลง F-DOCCFG หรือ register `EXP` ใต้ module code ใด |
| OQ-DOCCFG-06 | **No-gap guarantee** | ประกาศ `no-gap=yes` · ออกเลขตอน approved เท่านั้น (reject/cancel ก่อน approved = ไม่เผาเลข) | ยืนยัน no-gap รับได้ (ไม่มี path ยกเลิกหลัง approved → ไม่มีรูเลข · อ้าง OQ-05 reverse EC) |

> chip DOCCFG (PREBRIEF §12) = ✓ · detect = need → **ตรงกัน ไม่มี DIVERGENCE ระดับ chip** (divergence ที่พบเป็น config detail scope · OQ-DOCCFG-04)
