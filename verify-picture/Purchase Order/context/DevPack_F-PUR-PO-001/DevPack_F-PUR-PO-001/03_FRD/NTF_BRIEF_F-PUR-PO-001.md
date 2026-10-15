# NTF_BRIEF — F-PUR-PO · PO ใบสั่งซื้อ

> ยิงผ่าน **ENG-NOTIFY (F-NOTIFY)** เท่านั้น — **ห้าม hardcode ช่องทาง/เงื่อนไขใน feature**
> ⛔ **DOA events มาอัตโนมัติจาก DOA engine — ไม่อยู่ในใบนี้**: `doa_pending` · `doa_result` · `doa_escalate`
> (ประกาศซ้ำ = BLOCK) · ข้อความ template อยู่ในใบนี้ ไม่ฝังใน code feature

---

## 1. Event ธุรกิจของ PO ที่ประกาศ

| Event ID | Trigger (อ้าง PREBRIEF) | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| `po_sent_to_vendor` | transition `approved → sent` (§5 · S-07) | ผู้ขาย (ติดต่อภายนอก) + ผู้จัดซื้อผู้รับผิดชอบ | ส่งใบสั่งซื้อ **{po_no}** ให้ {vendor_name} แล้ว — กำหนดรับของ {required_date} | in-app + email | ✗ บังคับ |
| `po_partially_received` | transition `sent → partially received` (§5 · S-11) | ผู้จัดซื้อผู้รับผิดชอบ + ผู้ขอซื้อต้นทาง | **{po_no}** รับของบางส่วนแล้ว — คงเหลือรับ {open_qty_summary} | in-app | ✓ |
| `po_closed` | transition `→ closed` จากการรับครบ (§5 · S-10) | ผู้จัดซื้อผู้รับผิดชอบ + ผู้ขอซื้อต้นทาง | **{po_no}** รับของครบแล้ว — ปิดใบเรียบร้อย | in-app | ✓ |
| `po_short_closed` | transition `partially received → closed` โดยคน (§5 · S-12 · BR-12) | ผู้จัดซื้อ + หัวหน้าจัดซื้อ + ผู้ขอซื้อต้นทาง | **{po_no}** ถูกปิดก่อนรับครบ — เหตุผล: {close_reason} · ยอดค้างรับถูกยกเลิก | in-app + email | ✗ บังคับ |
| `po_cancelled` | transition `draft/approved/sent → cancelled` (§5 · S-13) | ผู้จัดซื้อ + ผู้ขอซื้อต้นทาง + **ผู้ขาย (เฉพาะกรณีเคย sent)** | **{po_no}** ถูกยกเลิก — เหตุผล: {cancel_reason} | in-app + email | ✗ บังคับ |
| `po_reapprove_required` | ผู้ใช้ยืนยันแก้ใบที่ `approved`/`sent` → Transition Guard (§5 · S-08 · BR-10) | ผู้อนุมัติชุดเดิมทุก slot + ผู้จัดซื้อ | **{po_no}** ถูกแก้ไขหลังอนุมัติ — ต้องอนุมัติใหม่ · เหตุผล: {reapprove_reason} | in-app | ✗ บังคับ |
| `po_delivery_due_soon` | ใกล้ถึง `required_date` ของใบที่ยังค้างรับ — **เกณฑ์จำนวนวันอยู่ NC rules** (PREBRIEF OB-16) | ผู้จัดซื้อผู้รับผิดชอบ + คลังปลายทาง | **{po_no}** ใกล้ถึงกำหนดรับของ ({required_date}) — ยังค้างรับ {open_qty_summary} | in-app | ✓ |
| `po_delivery_overdue` | เลย `required_date` แล้วยังค้างรับ — **เกณฑ์อยู่ NC rules** | ผู้จัดซื้อ + หัวหน้าจัดซื้อ | **{po_no}** เกินกำหนดรับของแล้ว {overdue_days} วัน — ค้างรับ {open_qty_summary} | in-app + email | ✓ |
| `po_budget_warning` | ผลตรวจงบ (mock) ตอบ "เกินวงเงิน" ตอนส่งอนุมัติ (§6.2 step 3 · S-06 · BR-15) | ผู้จัดซื้อ + ผู้อนุมัติ slot แรก | **{po_no}** ยอด {net_amount} อาจเกินวงเงินงบ {budget_ref} — โปรดตรวจก่อนอนุมัติ | in-app | ✓ |
| `po_attachment_added` | แนบไฟล์เข้าใบที่ ≥ `approved` (§7) | ผู้จัดซื้อผู้รับผิดชอบ + ผู้อนุมัติที่เกี่ยวข้อง | **{po_no}** มีเอกสารแนบใหม่: {file_name} | in-app | ✓ |

---

## 2. Payload ต่อ event (ref = soft-reference ไปเอกสาร)

| ตัวแปร | ที่มา |
|---|---|
| `ref` | `po_id` (soft-ref — ทุก event มี) |
| `po_no` | เลขที่จาก doccfg `PO-YYYY-NNNN` (ปี **ค.ศ.**) |
| `vendor_name` | ผู้ขาย (soft-ref LD-4C-02) |
| `required_date` · `overdue_days` | วันที่ต้องการรับ (แสดง **ค.ศ.**) |
| `open_qty_summary` | สรุปยอดค้างรับจาก line (§3.3) |
| `net_amount` | ยอดสุทธิ (§3.3) |
| `close_reason` · `cancel_reason` · `reapprove_reason` | เหตุผลบังคับกรอกตาม BR-11/BR-12/BR-10 |
| `budget_ref` | หมวดงบ/cost center — **mock** (`TODO: budget-control hook`) |
| `file_name` | ชื่อไฟล์แนบ |

---

## 3. เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)

| กลุ่ม | ท่าที |
|---|---|
| **เอกสารธุรกรรม (doc_status)** | ใช้กลุ่มเดิม — `po_sent_to_vendor` · `po_partially_received` · `po_closed` · `po_short_closed` · `po_cancelled` · `po_reapprove_required` |
| **เตือนตามกำหนดเวลา** | `po_delivery_due_soon` · `po_delivery_overdue` — ถ้ายังไม่มีกลุ่มนี้ ให้เพิ่มกลุ่ม "เตือนกำหนดส่งของ" |
| **เตือนเฉพาะเรื่อง (threshold)** | `po_budget_warning` — เกณฑ์อยู่ Budget Control/NC rules ไม่อยู่ feature |
| **ไฟล์แนบ** | `po_attachment_added` — ใช้กลุ่มเดิมถ้ามี |

> เช็คชนกับ catalog เดิม: ยังไม่มี event ที่ขึ้นต้น `po_` ในทะเบียนเลนนี้ — ไม่มีชื่อซ้ำ/ความหมายซ้อน

---

## 4. Dev wiring note (Phase B)

- จุดเรียก: `ENG-NOTIFY.emit(event_id, { ref: po_id, vars: {...} })` **ที่ transition ตาม trigger เท่านั้น**
- ❌ ห้ามเช็ค user preference / เลือกช่องทางเองใน feature — engine จัดการ
- ❌ ห้ามเขียน "ส่งอีเมล/LINE" ลง logic ของ PO
- ❌ ห้ามประกาศ/emit `doa_pending` · `doa_result` · `doa_escalate` — DOA engine ยิงเอง
- ⏱ event ตามกำหนดเวลา (`due_soon` / `overdue`) เป็น scheduled evaluation ฝั่ง engine — feature แค่ประกาศเงื่อนไข ไม่ตั้ง timer เอง
- 📅 ทุกวันที่ในข้อความ render เป็น **ค.ศ.** (PREBRIEF BR-19)
