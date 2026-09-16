# NTF_BRIEF — F-WH-STKADJ · Stock Adjustment (ใบปรับยอดสต๊อก)

> ยิงผ่าน **ENG-NOTIFY (F-NOTIFY Notification Center)** เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไขแจ้งเตือนใน feature
> ⛔ **DOA events มาอัตโนมัติ ไม่อยู่ในใบนี้**: `doa_pending` · `doa_result` · `doa_escalate` — DOA engine (F-DLG-001) เป็นเจ้าของ · ประกาศซ้ำ = BLOCK
> ข้อความ template อยู่ในใบประกาศนี้เท่านั้น ไม่ฝังใน code feature · ทุก event มี `ref` (soft-reference ไปเอกสาร)
> **Companion skill · Sync Read** F-NOTIFY EVENT_GROUPS (`f-notify.html`) — ไม่ copy ค้าง · verify ชื่อซ้ำตอน wire

---

## 1. Identity

| ช่อง | ค่า |
|---|---|
| feature_id | `F-WH-STKADJ` (fid F082) |
| ชื่อ | Stock Adjustment — ใบปรับยอดสต๊อก |
| module | Warehouse (WH) |
| chip | 🔔 ntf (CONTEXT_PACK §2.2 · PREBRIEF §OUT ENG-NOTIFY) |
| ref กลาง | `adj_id` (เอกสาร `ADJ-YYYY-NNNN` · ปี **ค.ศ.**) |
| source of truth | FRD 03_LOGIC state machine (emit points) · 05_RULES §5.5 (BR) · PREBRIEF §5.1 |

---

## 2. Event ที่ประกาศ (event ธุรกิจของ feature เอง)

ทุก event อ้าง **จุด emit จริง** ใน FRD 03_LOGIC (Function ที่ยิง) — ไม่ใช่แค่ transition บนกระดาษ

| Event ID | Trigger — transition + จุด emit (FRD) | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| `adj_posted` | `อนุมัติแล้ว → ผ่านรายการ` · emit ใน **F082-FN-13 `postDocument`** (03_LOGIC §3.1) · S-07/S-17 · BR-19 | ผู้จัดทำ + หัวหน้าคลังของคลังนั้น + **บัญชี** | ปรับยอดสต๊อก **{adj_no}** ผ่านรายการแล้ว — มูลค่าที่ปรับ **{abs_amount}** บาท (สุทธิ {net_amount}) ที่คลัง {warehouse_name} | in-app + email | ✓ |
| `adj_reversed` | `ผ่านรายการ → กลับรายการแล้ว` · เกิดเมื่อ**ใบกลับรายการ post** แล้ว set ต้นฉบับ=reversed · emit ใน **F082-FN-13** ผ่านเงื่อนไข **BR-17.1** (03_LOGIC §3.1 FN-13) · S-10 · BR-17 | ผู้จัดทำใบเดิม + หัวหน้าคลัง + **บัญชี** + ผู้อนุมัติทุก slot ของใบเดิม | ปรับยอดสต๊อก **{adj_no}** ถูกกลับรายการ — เหตุผล: {reversal_reason} · ใบกลับรายการ **{reversal_adj_no}** | in-app + email | ✗ **บังคับ** |
| `adj_cancelled` | `ร่าง/รออนุมัติ → ยกเลิก` **เท่านั้น** · emit ใน **F082-FN-11 `cancelDocument`** (03_LOGIC §3.1) · S-09 · **BR-27/FIX-02** | ผู้จัดทำ + ผู้อนุมัติ slot ที่ยังค้างอยู่ (ถ้าอยู่สถานะ รออนุมัติ) | ใบปรับยอด **{adj_no}** ถูกยกเลิก — เหตุผล: {cancel_reason} | in-app | ✓ |
| `adj_high_value_submitted` | `ร่าง → รออนุมัติ` **conditional** — เฉพาะเมื่อ `Σ\|มูลค่า\|` (`abs_amount`) เกินเกณฑ์นัยสำคัญ · emit ต่อจาก **F082-FN-08 `submitForApproval`** · เกณฑ์อ่านจาก **NC rules** (BR-20 — ห้าม hardcode) | **บัญชี** + ผู้จัดการคลังสินค้า (แจ้งให้รู้ล่วงหน้า — ไม่ใช่คำขออนุมัติ) | ใบปรับยอดมูลค่าสูง **{adj_no}** ถูกส่งอนุมัติ — **{abs_amount}** บาท ที่คลัง {warehouse_name} | in-app + email | ✗ **บังคับ** |
| `adj_writeoff_posted` | `อนุมัติแล้ว → ผ่านรายการ` **conditional** — เฉพาะ `adjustment_type = ตัดจำหน่ายของเสีย` · emit ใน **F082-FN-13** (03_LOGIC §3.1) · S-19 | **บัญชี** + ผู้จัดการคลังสินค้า | ตัดจำหน่ายของเสียตามใบ **{adj_no}** — มูลค่า **{abs_amount}** บาท · หลักฐานแนบ {attachment_count} ไฟล์ | in-app + email | ✗ **บังคับ** |
| `adj_qty_drift_on_post` | ตรวจยอดซ้ำก่อน post พบยอดระบบต่างจาก snapshot · emit จาก **F082-FN-12 `recheckQtyBeforePost`** → surface ใน FN-13 (03_LOGIC §3.1) · **BR-15** · S-15 · `WARN_QTY_CHANGED` | ผู้กด post + ผู้จัดทำ | ใบ **{adj_no}** — ยอดระบบเปลี่ยนหลังสร้างรายการ ({item_name} ที่ {bin_code}: {snapshot_qty} → {current_qty}) ตรวจก่อนผ่านรายการ | in-app | ✓ |

> ★ **`adj_high_value_submitted` ไม่ใช่ `doa_pending`** — `doa_pending` = "คุณต้องเซ็น" ที่ DOA engine ยิงให้ผู้อนุมัติ slot ปัจจุบัน · ตัวนี้ = "แจ้งให้บัญชี/ผจก.คลังรู้ว่ากำลังจะมีรายการใหญ่" · ผู้รับคนละกลุ่ม เจตนาคนละอย่าง — **ไม่ซ้ำท่อ**

### ❌ ไม่ประกาศ (DOA-sourced หรือ noise) — พร้อมเหตุผล

| ตัวที่ไม่ประกาศ | เหตุผล |
|---|---|
| `adj_submitted` (ทั่วไป) | ทับซ้อน **`doa_pending`** ที่ DOA engine ยิงตอน draft→pending อยู่แล้ว (03_LOGIC FN-08 "emit doa_pending") — ประกาศซ้ำ = BLOCK |
| `adj_approved` | คือ **`doa_result`** (approved) ที่ DOA engine ยิงตอน slot ครบ (03_LOGIC FN-09 "emit doa_result") |
| `adj_rejected` | คือ **`doa_result`** (rejected/returned) ของ DOA engine (03_LOGIC FN-10 `rejectDocument`) |
| `doa_escalate` (ใบค้างเกินอายุ) | เป็นหน้าที่ **DOA escalate** ของ F-DLG-001 (NC rules อายุใบค้าง BR-20) — ห้ามซ้ำ (ดู NTF-Q4) |
| `adj_draft_saved` | ไม่มีใครต้องรู้ → noise |

---

## 3. Payload (ตัวแปรในข้อความ + ref)

| ตัวแปร | ที่มา | หมายเหตุ |
|---|---|---|
| `ref` = `adj_id` | header (03_LOGIC · T_stock_adjustment) | soft-reference ทุก event |
| `adj_no` | doccfg `ADJ-YYYY-NNNN` (ENG-DOC-NUM · FN-08 · BR-21) | ปี **ค.ศ.** · ร่างยังไม่มีเลข → ถ้ายิงตอนร่างใช้ `(ร่าง)` (แต่ทุก event ในใบนี้ยิงหลังออกเลขแล้ว) |
| `abs_amount` | `Σ \|มูลค่าที่ปรับ\|` (F082-ENG-01 `abs_total`) | **ตัวเดียวกับฐาน DOA** (BR-09) |
| `net_amount` | มูลค่าสุทธิ (F082-ENG-01 `net_total`) | แสดงคู่กันกัน misread |
| `warehouse_name` · `warehouse_ref` | header คลัง (soft-ref) | nullable-safe |
| `adjustment_type` | header ประเภทการปรับ | ใช้กรอง `adj_writeoff_posted` |
| `reversal_reason` · `cancel_reason` | FN-14 / FN-11 (VR-14 บังคับกรอก) | บังคับอยู่แล้ว |
| `reversal_adj_no` | ใบกลับรายการ (soft link 2 ทาง · BR-18) | เฉพาะ `adj_reversed` |
| `attachment_count` | T_stock_adjustment_attachment (FN-15) | เฉพาะ `adj_writeoff_posted` |
| `item_name` · `bin_code` · `snapshot_qty` · `current_qty` | FN-12 drift[] (BR-15) | เฉพาะ `adj_qty_drift_on_post` |
| `occurred_at` · `actor` | ระบบ (T_audit_log) | timestamp **ค.ศ.** ทุก event |

---

## 4. เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)

| กลุ่ม | รายการ |
|---|---|
| **เอกสารธุรกรรม** (มีอยู่แล้ว) | ใช้ `doc_status` เดิมสำหรับ `adj_cancelled` — **ไม่เพิ่มกลุ่มใหม่** |
| **สต๊อกเคลื่อนไหว / คลังสินค้า** | เพิ่ม `adj_posted` · `adj_reversed` · `adj_qty_drift_on_post` (กลุ่มเดียวกับ event ของ GRN/RTV/Putaway ในเลนนี้ — ถ้ากลุ่มยังไม่มีให้สร้าง "สต๊อกเคลื่อนไหว") |
| **บัญชี/การเงิน (แจ้งเพื่อทราบ)** | เพิ่ม `adj_high_value_submitted` · `adj_writeoff_posted` — **ผู้รับหลักคือบัญชี** ไม่ใช่คลัง |

> เช็คชนกับ catalog เดิม: ยังไม่มี event ชื่อ `adj_*` ในทะเบียน → ไม่มีชื่อซ้ำ/ความหมายซ้อน `[AI-DRAFT]` — **ต้อง Sync Read `f-notify.html` EVENT_GROUPS จริงตอน wire (Phase B)** ก่อน register

---

## 5. Dev wiring note

- จุดเรียก: `ENG-NOTIFY.emit(event_id, {ref, vars})` ที่ **transition + Function ตาม §2 เท่านั้น** (ตรงกับ state machine FRD 03_LOGIC §3.1) — **ห้ามเช็ค user preference เอง ห้ามเลือกช่องทางเอง**
- `adj_high_value_submitted` และ `adj_writeoff_posted` เป็น **conditional emit** — เงื่อนไข "มูลค่าสูง" อ่านจาก **NC rules** ไม่ใช่เลขในโค้ด feature (BR-20 · 05_RULES §5.9)
- `adj_cancelled` guard = `status ∈ {draft, pending}` เท่านั้น (F082-FN-11 · **BR-27/FIX-02**) — **`อนุมัติแล้ว` ยกเลิกไม่ได้** จึงไม่มี emit จากสถานะนั้น
- `adj_reversed` ยิงตอน**ใบกลับรายการ post** (ไม่ใช่ตอนกด "กลับรายการ") — reversal เป็นใบใหม่วิ่งสาย DOA ก่อน (FIX-03/LD-05) แล้ว FN-13 set ต้นฉบับ=reversed (BR-17.1)
- FRD Phase B alignment: `03_LOGIC` FN-08/11/12/13 มีจุด emit ตรงกับตาราง §2 · `05_RULES §5.9` ชี้ช่องทางแจ้งเตือนมาที่ไฟล์นี้ (F-NOTIFY ห้าม hardcode)

---

## 6. Open Questions (ยก BA / เจ้าของ engine — WF-01 C3.10)

| # | ประเด็น | ใครตอบ |
|---|---|---|
| NTF-Q1 | เกณฑ์ "มูลค่าสูง" ของ `adj_high_value_submitted` — ตัวเลขจริงใน NC rules คือเท่าไร และควรผูกกับจุดตัด DOA set หรือแยก | BA/Strike + เจ้าของ NC rules |
| NTF-Q2 | บัญชีควรได้ `adj_posted` **ทุกใบ** หรือเฉพาะใบเกินเกณฑ์ (กัน noise) | BA + เจ้าของบัญชี |
| NTF-Q3 | `adj_reversed` ควรแจ้ง**ผู้อนุมัติทุก slot ของใบเดิม**ด้วยไหม (รอบนี้ = แจ้ง) | เจ้าของ F-NOTIFY |
| NTF-Q4 | event เตือน "ใบค้างอนุมัติเกินเกณฑ์อายุ" — รอบนี้ **ไม่ประกาศ** เพราะเป็นหน้าที่ **DOA escalate** (`doa_escalate`) ห้ามซ้ำ · ยืนยัน DOA เป็นเจ้าของ | เจ้าของ F-NOTIFY + F-DLG-001 |
| NTF-Q5 | **[แก้จาก BA ref]** BA reference (`5_DECLARATIONS/NTF_BRIEF`) เขียน trigger `adj_cancelled` รวม `อนุมัติแล้ว → ยกเลิก` — ขัด **BR-27/FIX-02** (BA re-gate 2026-09-15) ที่ล็อกว่า `อนุมัติแล้ว` ยกเลิกไม่ได้ · ใบนี้แก้ให้ตรง FRD (draft/pending only) แล้ว — ยืนยัน BA ref ล้าสมัย ไม่ใช่มติใหม่ | BA |

---

## 7. Verdict

**PASS (with 5 Open Questions)** — event ทั้ง 6 ผูก transition + จุด emit จริงใน FRD 03_LOGIC ครบ · DOA-sourced (`doa_pending`/`doa_result`/`doa_escalate`) ตัดออกถูกต้อง ไม่ประกาศซ้ำ · ไม่มี channel/threshold hardcode · เกณฑ์มูลค่าสูงชี้ NC rules (BR-20) · แก้ trigger `adj_cancelled` ให้ตรง BR-27/FIX-02 (NTF-Q5)
