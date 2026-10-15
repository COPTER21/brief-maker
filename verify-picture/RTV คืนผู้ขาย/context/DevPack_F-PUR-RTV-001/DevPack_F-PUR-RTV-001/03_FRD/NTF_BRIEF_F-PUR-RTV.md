# NTF_BRIEF — F-PUR-RTV · RTV คืนผู้ขาย

> ยิงผ่าน **ENG-NOTIFY** เท่านั้น — **ห้าม hardcode ช่องทาง/เงื่อนไข** ใน feature
> **DOA events (`doa_pending` / `doa_result` / `doa_escalate`) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้ (ประกาศซ้ำ = BLOCK)**
> trigger point อ้าง PREBRIEF_F-PUR-RTV §5.1 (state machine) และ §4 (business rules) — Phase B ต้อง re-map ไปที่ FRD 03_LOGIC

---

## 1. Event ธุรกิจของ feature นี้

| Event ID | Trigger (อ้าง PREBRIEF) | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| `rtv_returned` | transition `อนุมัติแล้ว → ส่งคืนแล้ว` (§5.1 · S-11) — ของออกจากคลังจริง | ผู้ขอคืน · ผู้อนุมัติทุก slot · จัดซื้อผู้ดูแลผู้ขายรายนี้ · บัญชี (AP) | ส่งคืนสินค้าตามใบ **{rtv_id}** ให้ {vendor_name} แล้ว — มูลค่า {return_amount} บาท รอเครดิตจากผู้ขาย | in-app + email | ✓ |
| `rtv_credited` | transition `ส่งคืนแล้ว → ปิดใบ` (§5.1 · S-12) — บันทึกเลขเอกสารเครดิตของผู้ขาย | ผู้ขอคืน · จัดซื้อ · บัญชี (AP) | ใบคืนสินค้า **{rtv_id}** ได้รับเครดิตจากผู้ขายแล้ว ({credit_doc_no} · {credit_amount} บาท) | in-app | ✓ |
| `rtv_reversed` | transition `ส่งคืนแล้ว → กลับรายการ` (§5.1 · S-14) — ผู้ขายปฏิเสธรับคืน/ของถูกตีกลับ | ผู้ขอคืน · หัวหน้าคลัง · ผู้อนุมัติทุก slot · บัญชี (AP) | **{rtv_id}** ถูกกลับรายการ — ของกลับเข้า {location_name} · เหตุผล: {reverse_reason} | in-app + email | ✗ บังคับ |
| `rtv_cancelled` | transition `ร่าง/รออนุมัติ/อนุมัติแล้ว → ยกเลิก` (§5.1 · S-10, S-13) | ผู้ขอคืน · ผู้อนุมัติที่เคยตัดสินในใบนี้ | ใบคืนสินค้า **{rtv_id}** ถูกยกเลิก — เหตุผล: {cancel_reason} | in-app | ✓ |
| `rtv_quarantine_aging` | เกณฑ์เวลา: บรรทัด GRN ที่มีของใน quarantine ค้างเกินเกณฑ์โดยยังไม่มี RTV (เกณฑ์อยู่ **NC rules** · §3.4) | หัวหน้าคลัง · จัดซื้อผู้ดูแลผู้ขายรายนั้น | มีของค้าง quarantine {qty} {uom} ({item_name}) จาก **{grn_id}** เกิน {days} วัน — ยังไม่ได้เปิดใบคืนผู้ขาย | in-app | ✓ |

---

## 2. Event ที่ **ไม่ประกาศ** ในใบนี้ (เจ้าของอื่นยิงให้แล้ว)

| Event | เจ้าของ | เหตุผล |
|---|---|---|
| `doa_pending` | **DOA engine (F-DLG-001)** | เกิดตอน `ร่าง → รออนุมัติ` — engine ยิงเองทุก feature ที่มี DOA · ประกาศซ้ำ = BLOCK |
| `doa_result` (อนุมัติ / ส่งกลับแก้ / ปฏิเสธ รายชั้น) | **DOA engine** | ผลการตัดสินของแต่ละ slot |
| `doa_escalate` | **DOA engine** | ค้างเกินเวลาในชั้นเดิม |
| แจ้งเตือนของ GRN (`grn_posted` ฯลฯ) | **F-WH-GRN** | คนละ feature — RTV ไม่ยิงแทน |
| แจ้งเตือนเรื่อง CN/JE ฝั่งบัญชี | **AP / GL (W5)** | ยังไม่มีในรอบนี้ — `TODO: JE posting` |

---

## 3. เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)

- กลุ่ม **"เอกสารธุรกรรม"** → `rtv_returned` · `rtv_credited` · `rtv_reversed` · `rtv_cancelled` (โครงเดียวกับ doc_status ของ PO/GRN — ใช้กลุ่มเดิม ไม่สร้างกลุ่มใหม่)
- กลุ่ม **"แจ้งเฉพาะ / เกณฑ์"** → `rtv_quarantine_aging` (กลุ่มเดียวกับ low stock — อิงเกณฑ์เวลา ไม่ใช่สถานะเอกสาร)
- ⚠️ Sync Read: ก่อน register จริงต้องเทียบกับ EVENT_GROUPS ปัจจุบันของ F-NOTIFY — ถ้ามี event ความหมายซ้อนอยู่แล้วให้ใช้ตัวเดิม

---

## 4. Dev wiring note (Phase B)

- จุดเรียก: `ENG-NOTIFY.emit(event_id, {ref: rtv_id, vars})` **ที่ transition ตาม trigger เท่านั้น** — ห้ามเช็ค preference/ช่องทางเองใน feature
- ทุก event มี `ref` = เลขใบ RTV (soft-reference) · `rtv_quarantine_aging` มี `ref` = เลข GRN + บรรทัด
- ข้อความ template อยู่ในใบประกาศนี้ **ห้ามฝังใน code feature**
- ตัวแปรวันที่ในข้อความทั้งหมดเป็น **ปี ค.ศ.**
- เกณฑ์ของ `rtv_quarantine_aging` (กี่วัน) มาจาก **NC rules** — feature ไม่เก็บเลขนี้เอง
- ใน HTML Phase A จุดที่ยังต่อ engine ไม่ได้ใช้ marker `FWD-WIRE: ENG-NOTIFY` (ใน .md ใช้ `TODO:` ตามปกติ)
