# DOCCFG_BRIEF — F-WH-STKADJ · Stock Adjustment (ใบปรับยอดสต๊อก) · F082

> Auto-register ลง **Document Configuration (F-DOCCFG · Document Type Master กลาง)** ตอน deploy (XT-3 ของ F-DOCCFG) · admin ปรับค่าได้ทุกช่องหลัง register
> **เลขทุกใบจาก `ENG-DOC-NUM.next()` เท่านั้น · สำเนาทุกใบจาก `ENG-DOC-STORE.store()` เท่านั้น — ห้าม hardcode รูปแบบเลข / การ +1 / เงื่อนไขเก็บสำเนา** (LOCK-05 · BR-21 · Iron #1)
> Companion / Sync-Read F-DOCCFG (TYPES + FMT_PRESETS) — ค่าที่ประกาศคือ **default ตอน register** ไม่ใช่ค่าตายตัว (มติ 2026-08-11 · Iron #6)

---

## 1. doc_type ที่ประกาศ

| Code | ชื่อ | Module | Preset default | Reset | Scope | No-gap | Snap: ส่งออกนอกระบบ | Snap: อนุมัติ+เซ็นครบ |
|---|---|---|---|---|---|---|---|---|
| **ADJ** | ใบปรับยอดสต๊อก | WH | `{PREFIX}-{YYYY}-{run:4}` → **`ADJ-YYYY-NNNN`** | รายปี (ปี **ค.ศ.**) | global `[DEFAULT — รอยืนยัน DOC-Q2]` | ✗ `[DEFAULT — รอยืนยัน DOC-Q1]` | ✗ (**ใบภายในล้วน** ไม่ส่งออกนอกองค์กร) | ✓ (`approved_final`) |

**ปีในเลขรัน = ค.ศ. ล้วน** (NOT พ.ศ.) — บนหน้าจอ · ใน list · ใน PDF ทุกจุด (LOCK-10 · GOLDEN §1 · TASTE_LOG · print-spec-adj §7)

**เช็คชนกับ registry (เลน Warehouse):** `ADJ` ยังไม่ถูกใช้ — เลนนี้มี `PO` · `GRN` · `RTV` แล้ว · `TRF` จองไว้ให้ F083 Stock Transfer ตัวถัดไป · ความหมายไม่ซ้อนกับ `JE` (ใบสำคัญบัญชี = doc_type ฝั่ง GL คนละเจ้าของ · W5) — **ไม่มี conflict** (Iron #2)

> **`Snap: ส่งออกนอกระบบ = ✗`** ต่างจาก `RTV` โดยเจตนา — ใบปรับยอดไม่มีคู่ค้าภายนอกรับใบ เป็นเอกสารควบคุมภายใน (ยัง**พิมพ์เก็บแฟ้ม**ได้ผ่าน tab PDF แต่ไม่นับเป็น `sent_external`) `[AI-DRAFT]` → DOC-Q3

---

## 2. จุดออกเลข (ENG-DOC-NUM)

| เมื่อไหร่ | อ้าง FRD | หมายเหตุ |
|---|---|---|
| transition **`ร่าง(draft) → รออนุมัติ(pending)`** — กดส่งอนุมัติ | 03_LOGIC F082-FN-08 (submitForApproval) · 02_API API-05 (`POST /:id/submit`) · 05_RULES **BR-21** · 07 **LOCK-05** | **ไม่ออกเลขตอนร่าง** (กันเลขกระโดดจากร่างที่ถูกทิ้ง) · ออกตอนส่งอนุมัติเพราะผู้อนุมัติต้องอ้างเลขใบ + tab PDF ต้องพิมพ์ได้ตั้งแต่ `รออนุมัติ` |
| **ใบกลับรายการ (reversal)** — ตอนสร้างใบ reversal (`is_reversal_doc`) จาก `ผ่านรายการ(posted)` | 03_LOGIC F082-FN-14 (reverseDocument) · 02_API API-10 (`POST /:id/reverse`) · 05_RULES BR-17/17.1/18 · 07 **LD-05** | ใบกลับรายการ **ได้เลข `ADJ` ของตัวเอง** (ชุดเลขเดียวกัน ไม่แยก prefix) · วิ่ง draft→pending→approved→posted ตามสาย DOA ของตัวเอง · ผูก soft link 2 ทางกับใบเดิม — mock `ADJ-2026-0007` ↔ `ADJ-2026-0008` |

> `ADJ` ตั้ง **no-gap = ✗** โดยเจตนา เพราะใบที่ถูกตีกลับ/ยกเลิกหลังออกเลขจะทำให้เลขขาดช่วง (BR-27: `อนุมัติแล้ว` ยกเลิกไม่ได้ แต่ `ร่าง`/`รออนุมัติ` ยกเลิกได้ → เลขที่ออกไปแล้วถูกทิ้ง) · ถ้าบัญชีต้องการ no-gap ต้องเลื่อนจุดออกเลขไปที่ `ผ่านรายการ` แทน (07_LOCKED "no-gap เลขรัน" → owner **F-DOCCFG**) → **DOC-Q1**

---

## 3. จุดเก็บสำเนา (ENG-DOC-STORE)

| Event flag | trigger point (FRD authoritative) | อ้าง FRD |
|---|---|---|
| `approved_final` | **`postDocument`** — transition `อนุมัติแล้ว(approved) → ผ่านรายการ(posted)` เรียก `ENG-DOC-STORE.store(pdf,'ADJ',adj_id,'approved_final')` | 03_LOGIC **F082-FN-13** (postDocument · "store PDF (approved_final)") · 02_API API-09 (`POST /:id/post`) |
| — `sent_external` | **ไม่เปิดใช้** — ใบภายในล้วน ไม่ส่งออกนอกองค์กร (พิมพ์เก็บแฟ้มได้ แต่ไม่ถือเป็น sent_external) | print-spec-adj §1 · §7 |

> ⚠️ **Divergence ต้องเคาะ — DOC-Q6:** BA brief ต้นฉบับ (§3) บรรยายว่า `approved_final` ยิงตอนใบเป็น **`อนุมัติแล้ว`** (มีลายเซ็นครบสาย DOA) แต่ **FRD 03_LOGIC F082-FN-13** เรียก `store()` จริงในขั้น **`postDocument`** (ตอน `ผ่านรายการ`) ไม่ใช่ตอน approved · ใบประกาศนี้ยึด **FRD (ผ่านรายการ)** เป็น trigger จริง เพราะ FRD เป็น source of truth ของ logic — ต้องให้ **Strike + เจ้าของ F-DOCCFG** ยืนยันว่าจุด store ที่ถูกต้องคือ `approved` หรือ `posted`
> ★ ใบที่ **ตัดจำหน่ายของเสีย** อาจต้องเก็บสำเนาเพิ่มเพื่อการตรวจสอบ/ภาษี — รอบนี้ยังไม่ประกาศ event เพิ่ม (`approved_final` ครอบอยู่แล้ว) → **DOC-Q4**

---

## 4. Dev wiring note (Phase B)

- `adj.number = ENG-DOC-NUM.next('ADJ', company_ctx)` ที่ transition `ร่าง → รออนุมัติ` (F082-FN-08) — **ห้าม format เอง ห้าม +1 เอง**
- เลขที่ออกแล้ว **immutable** (Iron #3) — ใบที่ถูกตีกลับยังใช้เลขเดิม (ไม่ออกเลขใหม่แม้แก้บรรทัด/มูลค่าจนสายอนุมัติเปลี่ยน) · ใบที่ยกเลิกเก็บเลขไว้ไม่นำกลับมาใช้ซ้ำ
- ใบกลับรายการเรียก `ENG-DOC-NUM.next('ADJ', ...)` **อีกครั้ง** (ใบใหม่ `is_reversal_doc`) — **ไม่ใช่การ renumber ใบเดิม** (BR-18 · LD-05)
- render PDF แล้วเรียก `ENG-DOC-STORE.store(pdf,'ADJ',adj_id,'approved_final')` ที่ `postDocument` (F082-FN-13) — engine เช็ค flag เองว่าเก็บหรือไม่
- **ห้ามอ่าน/เขียนตาราง config ตรง** — ผ่าน engine API เท่านั้น (Iron #1)
- ปีในเลขรัน + วันที่ทุกช่องเป็น **ค.ศ.** ทุกจุด — หน้าจอ · list · PDF (LOCK-10 · print-spec-adj §7)
- ใน HTML Phase A จุดที่ยังต่อ engine ไม่ได้ใช้ marker **`FWD-WIRE: ENG-DOC-NUM`** (ใน .md ใช้ `TODO:` ตามปกติ)
- ร่างแสดงข้อความ `(ร่าง — ยังไม่ออกเลขที่)` แทนเลข — **ห้ามแสดงเลขคาดเดาล่วงหน้า** (BR-21)

---

## 5. Open Questions

| # | ประเด็น | ใครตอบ |
|---|---|---|
| DOC-Q1 | ออกเลขตอน **ส่งอนุมัติ** (ค่าปัจจุบัน · BR-21) หรือควรเลื่อนไปตอน **ผ่านรายการ** เพื่อรองรับ no-gap (07_LOCKED "no-gap เลขรัน") | **Strike** + เจ้าของ F-DOCCFG |
| DOC-Q2 | scope ควรเป็น `global` หรือ `branch` — StockAdj ผูก 1 ใบ = 1 คลัง (BR-04) จึงมีเหตุผลจะเป็น branch ถ้าแต่ละคลัง/สาขาต้องมีชุดเลขของตัวเอง | Strike |
| DOC-Q3 | ใบปรับยอดถือเป็น "ใบภายในล้วน" จริงไหม — ถ้าผู้สอบบัญชีภายนอกขอ ต้องเปิด `sent_external` ไหม | Strike + เจ้าของบัญชี |
| DOC-Q4 | ใบ **ตัดจำหน่ายของเสีย** ต้องเก็บสำเนาแยก/นานกว่าปกติเพื่อการตรวจสอบภาษีไหม | เจ้าของบัญชี + F-DOCCFG |
| DOC-Q5 | ใบกลับรายการควรใช้ชุดเลข `ADJ` เดียวกัน (ค่าปัจจุบัน · LD-05) หรือแยก prefix เช่น `ADJR` | เจ้าของ F-DOCCFG |
| DOC-Q6 | **[ใหม่ · consistency]** `approved_final` ยิง `store()` ที่ **`อนุมัติแล้ว`** (BA brief §3) หรือ **`ผ่านรายการ`** (FRD 03_LOGIC F082-FN-13 — ใบประกาศนี้ยึดตาม FRD) | Strike + เจ้าของ F-DOCCFG |
