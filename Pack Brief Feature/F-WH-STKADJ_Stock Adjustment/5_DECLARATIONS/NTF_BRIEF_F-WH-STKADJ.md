# NTF_BRIEF — F-WH-STKADJ · Stock Adjustment (ใบปรับยอดสต๊อก)

> ยิงผ่าน **ENG-NOTIFY (F-NOTIFY)** เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไขแจ้งเตือนใน feature
> ⛔ **DOA events มาอัตโนมัติ ไม่อยู่ในใบนี้**: `doa_pending` · `doa_result` · `doa_escalate` — DOA engine เป็นเจ้าของ · ประกาศซ้ำ = BLOCK
> ข้อความ template อยู่ในใบประกาศนี้ ไม่ฝังใน code feature · ทุก event มี `ref` (soft-reference ไปเอกสาร)

---

## 1. Identity

| ช่อง | ค่า |
|---|---|
| feature_id | `F-WH-STKADJ` (fid F082) |
| ชื่อ | Stock Adjustment — ใบปรับยอดสต๊อก |
| module | Warehouse (WH) |
| chip | 🔔 ntf (CONTEXT_PACK §2.2) |
| ref กลาง | `adj_id` (เอกสาร `ADJ-YYYY-NNNN`) |

---

## 2. Event ที่ประกาศ (event ธุรกิจของ feature เอง)

| Event ID | Trigger (อ้าง PREBRIEF) | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| `adj_posted` | `อนุมัติแล้ว → ผ่านรายการ` (§5.1 · S-07/S-17 · BR-19) | ผู้จัดทำ + หัวหน้าคลังของคลังนั้น + **บัญชี** | ปรับยอดสต๊อก **{adj_no}** ผ่านรายการแล้ว — มูลค่าที่ปรับ **{abs_amount}** บาท (สุทธิ {net_amount}) ที่คลัง {warehouse_name} | in-app + email | ✓ |
| `adj_reversed` | `ผ่านรายการ → กลับรายการแล้ว` (§5.1 · S-10 · BR-17) | ผู้จัดทำใบเดิม + หัวหน้าคลัง + **บัญชี** + ผู้อนุมัติทุก slot ของใบเดิม | ปรับยอดสต๊อก **{adj_no}** ถูกกลับรายการ — เหตุผล: {reversal_reason} · ใบกลับรายการ **{reversal_adj_no}** | in-app + email | ✗ **บังคับ** |
| `adj_cancelled` | `ร่าง/รออนุมัติ/อนุมัติแล้ว → ยกเลิก` (§5.1 · S-09) | ผู้จัดทำ + ผู้อนุมัติ slot ที่ยังค้างอยู่ (ถ้ามี) | ใบปรับยอด **{adj_no}** ถูกยกเลิก — เหตุผล: {cancel_reason} | in-app | ✓ |
| `adj_high_value_submitted` | `ร่าง → รออนุมัติ` **เฉพาะเมื่อ** `Σ\|มูลค่า\|` เกินเกณฑ์นัยสำคัญ (เกณฑ์อยู่ **NC rules** — BR-20) | **บัญชี** + ผู้จัดการคลังสินค้า (แจ้งให้รู้ล่วงหน้า ไม่ใช่คำขออนุมัติ) | ใบปรับยอดมูลค่าสูง **{adj_no}** ถูกส่งอนุมัติ — **{abs_amount}** บาท ที่คลัง {warehouse_name} | in-app + email | ✗ **บังคับ** |
| `adj_writeoff_posted` | `อนุมัติแล้ว → ผ่านรายการ` **เฉพาะ** ประเภทการปรับ = `ตัดจำหน่ายของเสีย` (§3.1 · S-19) | **บัญชี** + ผู้จัดการคลังสินค้า | ตัดจำหน่ายของเสียตามใบ **{adj_no}** — มูลค่า **{abs_amount}** บาท · หลักฐานแนบ {attachment_count} ไฟล์ | in-app + email | ✗ **บังคับ** |
| `adj_qty_drift_on_post` | ตรวจยอดซ้ำก่อน post พบยอดระบบต่างจาก snapshot (§4 BR-15 · S-15) | ผู้กด post + ผู้จัดทำ | ใบ **{adj_no}** — ยอดระบบเปลี่ยนหลังสร้างรายการ ({item_name} ที่ {bin_code}: {snapshot_qty} → {current_qty}) ตรวจก่อนผ่านรายการ | in-app | ✓ |

> ★ **`adj_high_value_submitted` ไม่ใช่ `doa_pending`** — `doa_pending` คือ "คุณต้องเซ็น" ที่ DOA engine ยิงให้ผู้อนุมัติ slot ปัจจุบัน · ตัวนี้คือ "แจ้งให้บัญชีรู้ว่ากำลังจะมีรายการใหญ่" ผู้รับคนละกลุ่ม เจตนาคนละอย่าง — **ไม่ซ้ำท่อ**
> ❌ **ไม่ประกาศ** `adj_submitted` แบบทั่วไป — ทับซ้อนกับ `doa_pending` ที่ DOA engine ยิงอยู่แล้ว
> ❌ **ไม่ประกาศ** `adj_approved` / `adj_rejected` — คือ `doa_result` ของ DOA engine
> ❌ **ไม่ประกาศ** `adj_draft_saved` — ไม่มีใครต้องรู้ (noise)

---

## 3. Payload (ตัวแปรในข้อความ + ref)

| ตัวแปร | ที่มา (PREBRIEF) | หมายเหตุ |
|---|---|---|
| `ref` = `adj_id` | header | soft-reference ทุก event |
| `adj_no` | §3.1 เลขที่ (doccfg `ADJ-YYYY-NNNN`) | ปี **ค.ศ.** · ร่างยังไม่มีเลข → event ที่ยิงตอนร่างใช้ `(ร่าง)` |
| `abs_amount` | §3.3 `Σ \|มูลค่าที่ปรับ\|` | **ตัวเดียวกับฐาน DOA** |
| `net_amount` | §3.3 มูลค่าสุทธิ | แสดงคู่กันเพื่อไม่ให้เข้าใจผิด |
| `warehouse_name` · `warehouse_ref` | §3.1 คลัง (soft-ref) | nullable-safe |
| `adjustment_type` | §3.1 ประเภทการปรับ | ใช้กรอง `adj_writeoff_posted` |
| `reversal_reason` · `cancel_reason` | §3.1 · BR-11/BR-17 | บังคับกรอกอยู่แล้ว |
| `reversal_adj_no` | §3.1 ใบกลับรายการ (soft link) | เฉพาะ `adj_reversed` |
| `attachment_count` | §3.1 เอกสารแนบ | เฉพาะ `adj_writeoff_posted` |
| `item_name` · `bin_code` · `snapshot_qty` · `current_qty` | §3.2 | เฉพาะ `adj_qty_drift_on_post` |
| `occurred_at` · `actor` | ระบบ | timestamp **ค.ศ.** ทุก event |

---

## 4. เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)

| กลุ่ม | รายการ |
|---|---|
| **เอกสารธุรกรรม** (มีอยู่แล้ว) | ใช้ `doc_status` เดิมสำหรับ `adj_cancelled` — **ไม่เพิ่มกลุ่มใหม่** |
| **คลังสินค้า / สต๊อก** | เพิ่ม `adj_posted` · `adj_reversed` · `adj_qty_drift_on_post` (กลุ่มเดียวกับ event ของ GRN/RTV/Putaway ในเลนนี้ — ถ้ากลุ่มยังไม่มีให้สร้าง "สต๊อกเคลื่อนไหว") |
| **บัญชี/การเงิน (แจ้งเพื่อทราบ)** | เพิ่ม `adj_high_value_submitted` · `adj_writeoff_posted` — **ผู้รับหลักคือบัญชี** ไม่ใช่คลัง |

> เช็คชนกับ catalog เดิม: ยังไม่มี event ชื่อ `adj_*` ในทะเบียน → ไม่มีชื่อซ้ำ/ความหมายซ้อน `[AI-DRAFT]` (ต้องตรวจซ้ำกับ `f-notify.html` EVENT_GROUPS จริงตอน Phase B)

---

## 5. Dev wiring note

- จุดเรียก: `ENG-NOTIFY.emit(event_id, {ref, vars})` ที่ **transition ตาม §2 เท่านั้น** (ตรงกับ state machine PREBRIEF §5.1) — **ห้ามเช็ค user preference เอง ห้ามเลือกช่องทางเอง**
- `adj_high_value_submitted` และ `adj_writeoff_posted` เป็น **conditional emit** — เงื่อนไข "มูลค่าสูง" อ่านจาก **NC rules** ไม่ใช่เลขในโค้ด feature (BR-20 · OB-15)
- Phase A ใน HTML ใส่เป็น mock + marker **`FWD-WIRE: ENG-NOTIFY emit`** (ใน .md ใช้ `TODO: ENG-NOTIFY emit` ตามปกติ · _RUNNER_BRIEF §2.11)
- FRD Phase B: `03_LOGIC` state machine ต้องมีจุด emit ตรงกับตาราง §2 · `05_RULES` ชี้มาที่ไฟล์นี้

---

## 6. Open Questions

| # | ประเด็น | ใครตอบ |
|---|---|---|
| NTF-Q1 | เกณฑ์ "มูลค่าสูง" ของ `adj_high_value_submitted` — ตัวเลขจริงใน NC rules คือเท่าไร และควรผูกกับจุดตัด DOA set 3 หรือแยก | **Strike** + เจ้าของ NC rules |
| NTF-Q2 | บัญชีควรได้ `adj_posted` ทุกใบ หรือเฉพาะใบเกินเกณฑ์ (กัน noise) | Strike + เจ้าของบัญชี |
| NTF-Q3 | `adj_reversed` ควรแจ้งผู้อนุมัติทุก slot ของใบเดิมด้วยไหม (รอบนี้ = แจ้ง) | เจ้าของ F-NOTIFY |
| NTF-Q4 | ต้องมี event เตือน "ใบค้างอนุมัติเกินเกณฑ์อายุ" ไหม — รอบนี้ **ไม่ประกาศ** เพราะเป็น **หน้าที่ของ DOA escalate** (`doa_escalate`) ห้ามซ้ำ | เจ้าของ F-NOTIFY + F-DLG-001 |
