# NTF_BRIEF — F-WH-GRN · GRN รับของ

> ยิงผ่าน **ENG-NOTIFY (F-NOTIFY)** เท่านั้น — **ห้าม hardcode ช่องทาง/เงื่อนไขใน feature**
> ⛔ feature นี้ **ไม่มี DOA** → ไม่มี `doa_pending` / `doa_result` / `doa_escalate` ในระบบของ GRN เลย (ไม่ใช่ "ตัดออก" แต่ **ไม่มีจริง**)
> ⛔ **ห้ามประกาศซ้ำ event ที่ PO เป็นเจ้าของ** — `po_partially_received` · `po_closed` ประกาศไว้แล้วใน `NTF_BRIEF_F-PUR-PO.md`
> ข้อความ template อยู่ในใบนี้ ไม่ฝังใน code feature

---

## 1. Event ธุรกิจของ GRN ที่ประกาศ

| Event ID | Trigger (อ้าง PREBRIEF) | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| `grn_posted` | transition `draft → posted` (§5.1 · S-07) | ผู้จัดซื้อเจ้าของ PO + หัวหน้าคลัง | รับของตาม **{po_no}** แล้ว — ใบรับ **{grn_no}** วันที่ {receive_date} · รับ {received_summary} | in-app | ✓ |
| `grn_quarantined` | post แล้วมีบรรทัดที่ QC ไม่ผ่าน > 0 (§5.1 · S-12/S-13 · BR-09/BR-10) | ผู้ตรวจคุณภาพ + หัวหน้าคลัง + ผู้จัดซื้อเจ้าของ PO | **{grn_no}** มีของไม่ผ่านตรวจ {reject_qty_summary} เข้าพักที่ {quarantine_location} — เหตุผล: {reject_reason} · รอดำเนินการคืนผู้ขาย | in-app + email | ✗ บังคับ |
| `grn_over_received` | บรรทัดใดรับ > คงเหลือรับ (อยู่ในกรอบ tolerance) ตอน post (§2 · S-03 · BR-06/BR-07) | ผู้จัดซื้อเจ้าของ PO + หัวหน้าคลัง | **{grn_no}** รับเกินยอดค้างรับของ **{po_no}** {over_qty_summary} (ในกรอบ {tolerance_pct}%) — หมายเหตุ: {over_note} | in-app | ✓ |
| `grn_reversed` | transition `posted → reversed` (§5.1 · S-08 · BR-15) | ผู้จัดซื้อเจ้าของ PO + หัวหน้าคลัง + ผู้รับของเดิม + บัญชี | **{grn_no}** ถูกกลับรายการ — เหตุผล: {reversal_reason} · ยอดรับที่ **{po_no}** ถูกหักคืนแล้ว | in-app + email | ✗ บังคับ |
| `grn_late_delivery` | วันที่รับจริง เลยวันที่ต้องการรับใน PO line — **เกณฑ์จำนวนวันอยู่ NC rules** (§3.3 · S-26 · OB-17) | ผู้จัดซื้อเจ้าของ PO + หัวหน้าจัดซื้อ | ของตาม **{po_no}** มาถึงช้ากว่ากำหนด {late_days} วัน (ใบรับ **{grn_no}**) | in-app | ✓ |
| `grn_gr_ir_pending` | post สำเร็จ → ใบขึ้นป้าย "รอตั้ง GR/IR" (§3.1 · §7 · S-19) | บัญชีเจ้าหนี้ (AP) | **{grn_no}** รับของแล้ว มูลค่า {gr_ir_amount} — รอตั้ง GR/IR (`TODO: JE posting` · W5) | in-app | ✓ |
| `grn_attachment_added` | แนบไฟล์เข้าใบที่ `posted` (§7) | ผู้รับของ + ผู้จัดซื้อเจ้าของ PO | **{grn_no}** มีเอกสารแนบใหม่: {file_name} | in-app | ✓ |

> **ไม่ประกาศ** event ตอนบันทึกร่าง/แก้ร่าง/ทิ้งร่าง — ไม่มีผลทางธุรกิจ (stock ไม่ขยับ · PO ไม่เปลี่ยน)

---

## 2. Payload ต่อ event (ref = soft-reference ไปเอกสาร · ทุก field มีจริงใน PREBRIEF §3)

| ตัวแปร | ที่มา |
|---|---|
| `ref` | `grn_id` (soft-ref — ทุก event มี) |
| `grn_no` | เลขที่จาก doccfg `GRN-YYYY-NNNN` (ปี **ค.ศ.**) — §3.1 |
| `po_no` | เลขที่ PO ต้นทาง (§3.1 อ้างอิง PO) |
| `receive_date` | วันที่รับจริง (แสดง **ค.ศ.**) — §3.1 |
| `received_summary` | สรุปจำนวนรับครั้งนี้ต่อบรรทัด (§3.2) |
| `reject_qty_summary` · `reject_reason` | จำนวนที่ไม่ผ่าน QC + เหตุผลที่ไม่ผ่าน (§3.2) |
| `quarantine_location` | quarantine location (§3.1 / §3.2) |
| `over_qty_summary` · `tolerance_pct` · `over_note` | ส่วนที่รับเกิน · tolerance % จาก PO line · หมายเหตุบรรทัดบังคับ (§3.2 · BR-07) |
| `reversal_reason` | เหตุผลกลับรายการ (§3.1 · BR-15) |
| `late_days` | `วันที่รับจริง − วันที่ต้องการรับ` (§3.3) |
| `gr_ir_amount` | มูลค่า GR/IR ที่จะตั้ง = ยอดรวมก่อนภาษี (§3.3) — **mock** `TODO: JE posting` |
| `file_name` | ชื่อไฟล์แนบ |
| `actor` | ผู้กด transition (ผู้รับของ / ผู้กลับรายการ) |

---

## 3. เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)

| กลุ่ม | ท่าที |
|---|---|
| **เอกสารธุรกรรม (doc_status)** | ใช้กลุ่มเดิม — `grn_posted` · `grn_reversed` เป็น event สถานะเอกสารมาตรฐาน |
| **คลัง/สต๊อก** | `grn_quarantined` · `grn_over_received` — ถ้ายังไม่มีกลุ่ม "คลัง" ให้เพิ่มกลุ่มใหม่ (ใช้ร่วมกับ RTV/Putaway/StockAdj ที่จะตามมาในเลนนี้) |
| **กำหนดส่ง/SLA** | `grn_late_delivery` — เกณฑ์วันอยู่ **NC rules** ไม่อยู่ feature |
| **บัญชี** | `grn_gr_ir_pending` — เตรียมไว้ให้ W5 รับต่อ (ตอนนี้ปลายทางเป็น mock) |

---

## 4. Dev wiring note (Phase B)

- จุดเรียก: `ENG-NOTIFY.emit(event_id, {ref, vars})` ที่ transition ตาม §1 — **ห้ามเช็ค preference/ช่องทางเอง**
- Phase A (HTML): ใส่เป็นคอมเมนต์ `FWD-WIRE: ENG-NOTIFY emit <event_id>` ที่จุด action (ในไฟล์ .md ใช้ `TODO:` ตามปกติ)
- `grn_quarantined` เป็นตัวส่งต่อไปยัง **RTV** ในเลนเดียวกัน — RTV จะเป็นคนประกาศ event ของตัวเอง ห้าม GRN ประกาศแทน

---

## 5. Open Questions

| # | ประเด็น | ใครตอบ |
|---|---|---|
| NTF-Q1 | `grn_posted` ควรแจ้งผู้ขายด้วยไหม (ยืนยันว่าของถึงแล้ว) — รอบนี้ **ไม่แจ้ง** เพราะยังไม่มี vendor portal | Strike |
| NTF-Q2 | `grn_late_delivery` ควรยิงจาก GRN (ตอนรับ) หรือจาก PO (ตอนเลยกำหนดแล้วยังไม่มีของ = `po_delivery_overdue` ที่ PO ประกาศไว้แล้ว) — กันแจ้งซ้ำ | เจ้าของ F-NOTIFY + Strike |
| NTF-Q3 | `grn_gr_ir_pending` จะถูกแทนที่ด้วย event ฝั่ง GL เมื่อ W5 มาแล้วหรือไม่ | เจ้าของ GL (W5) |
