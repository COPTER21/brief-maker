# PREBRIEF — F-INV · Stock by Location (สต็อกตามตำแหน่ง)

> **Source of truth เชิง business** ของ feature นี้ — สกัดจาก ENC pack (base) + มติ vibe 2026-08-09 ทั้งชุด
> HTML = source of truth (Reverse Mode) · ไฟล์: `f-inv.html` · Route: `#/stock/{wh}` · ทุกข้อที่ AI คิดเองติด `[AI-DRAFT]`

---

## §0 Obligations (STEP 0 — พันธะจากต้นทาง)

| # | พันธะ | ต้นทาง | อ้างกลับ |
|---|---|---|---|
| OB-1 | ENC HTML = base (superset: adjust modal + log + break/pack) → rebrand Warm Light + CUBE 4.0 | มติ 2026-08-09 | §2 ทั้งหมด |
| OB-2 | **2-code model**: รหัสกลาง (code) + รหัสเก่า (old_code) — ตัด code_item/code_sku ทุกจุด | มติ 2026-08-09 (ทับ ENH-PRODUCT-4CODE-001) | S-01, FN-05 |
| OB-3 | **Service exclusion**: สินค้า type SV ห้ามมี balance / ห้ามโผล่ทุกจอ / ปรับสต็อกไม่ได้ — BACKEND exclude `is_stock_item=false` ตั้งแต่ query | มติ 2026-08-09 · VD-PDM-05 (นับสต็อก = derived จากประเภท) | S-09, FN-03 |
| OB-4 | **หน่วยตามตำแหน่ง (1 location 1 uom)**: ledger เก็บหน่วยฐานเสมอ · จอแสดงตามหน่วยของตำแหน่ง + ฐานกำกับเมื่อ factor>1 | มติ 2026-08-09 · standard BC/D365 (line UoM + base qty) | S-02, S-03, FN-06..08 |
| OB-5 | **List "ตามสินค้า" = 1 สินค้า 1 แถว** (aggregate หน่วยฐาน — Item availability → drill to bin) · ตัด stat "คงเหลือรวม" ที่รวมข้ามหน่วย (ผิด logic) | มติ 2026-08-09 | S-02, FN-04 |
| OB-6 | **Low stock**: `min_stock` (threshold หน่วยฐาน) มาจาก Item Master (`PRODUCT_STOCK_THRESHOLD v1` — VD-PDM-14) · เทียบกับ "พร้อมใช้" | Central Plan handoff (Item Master → Inventory Monitoring) | S-08, FN-09 |
| OB-7 | **สถานะสต็อกใน list = คำสั้น 3 ค่า**: ปกติ / ต้องเติม / ขาดสต็อก — ปัญหารายจุด (damaged/blocked) ไปดูใน drawer | มติ 2026-08-09 | FN-04 |
| OB-8 | **Adjust สร้าง balance ใหม่ได้** (เพิ่มสินค้าเข้าตำแหน่งว่าง) + line editor grid (v8 B2) modal กว้าง ~1392px + summary bar | มติ 2026-08-09 | S-05, FN-13..17 |
| OB-9 | **#95 Overlay Portal** ทุก dropdown (adjust + break/pack) + Esc chain: Esc①ปิด dd → Esc②ปิด modal | v8 iron rule | FN-20 |
| OB-10 | **#67.1 Hint Opt-in**: ไม่มี hint/คำอธิบายสอนใช้งานทุกจอ | v8 + มติเลน | FN-21 |
| OB-11 | Allocated แตะไม่ได้ (ปรับได้เฉพาะส่วนเกินจอง) · append-only ADJ log ทุกครั้ง | ENC AC-ADJ + CUBE audit pattern | S-06, FN-15, FN-18 |
| OB-12 | RBAC: ปรับสต็อกได้เฉพาะ warehouse_staff + finance (mock) — จริงผูก Policy Center | ENC · BACKEND comment | S-10, FN-19 |

ไม่มีแถว orphan — ทุก OB ถูกอ้างใน scenario/FN ด้านล่าง

---

## §1 Scope

**ทำ:** จอสต็อกคงเหลือระดับ (สินค้า × ตำแหน่ง) ใน 1 คลัง — 4 views (ตามสินค้า agg / ตามตำแหน่ง / แตก-แพ็ค / ประวัติการปรับ) + product drawer 3 tabs + balance drawer + location drawer + Manual Adjustment (multi-line, new-location) + Break/Pack + ADJ audit log + low stock monitoring
**ไม่ทำ (นอก scope):** GRN/Putaway/RTV (เมนูข้างเป็น stub) · Multi-UOM bucket ราย UoM (VD-PDM-05 ตัดแล้ว) · costing engine (VD-PDM-07) · การจอง (allocation มาจากระบบขาย — read-only ที่นี่) · โอนย้ายระหว่างตำแหน่ง (transfer = movement ประเภทอื่น, mock แสดงใน timeline เท่านั้น)

**เส้นเข้า:** Item Master (สินค้า + type + uom + convs + min_stock) · Location Hierarchy (ตำแหน่ง + type + status + 1-loc-1-uom) · ระบบขาย (allocated) · GRN (received/in_transit)
**เส้นออก:** ADJ log → Accounting (มูลค่าปรับ) [อนาคต] · low stock → Purchase (แจ้งเติม) [OQ-INV-05]

---

## §2 Scenarios (STEP 1 — derive D1..D6)

### View & อ่านข้อมูล
- **S-01 เปิดจอครั้งแรก (happy)** — เข้า `#/stock/WH-01` → stat 4 ใบ (สินค้า SKU / ต่ำกว่าขั้นต่ำ / สต็อกติดลบ / ตำแหน่ง HOLD) + list 1 สินค้า 1 แถว (คอลัมน์: สินค้า · คงเหลือ · จองแล้ว · พร้อมใช้ · สถานะสต็อก) — เลขฐาน + หน่วยฐานกำกับ · รหัสอ้างอิง 2 ชุดเท่านั้น (OB-2) · ไม่มีสินค้า SV (OB-3)
- **S-02 ดูรายสินค้า (product drawer)** — คลิกแถว → drawer: header (pill Master หยุดใช้งานถ้า inactive) → tabs บนสุด full-width [ภาพรวม default | ตำแหน่งจัดเก็บ | การเคลื่อนไหว] → ภาพรวม: สรุป 3 ใบฐาน + note low stock + การแปลงหน่วย + รายละเอียด (threshold, FIFO เก่าสุด, เคลื่อนไหวล่าสุด) + รหัส 2 ชุด · ตำแหน่งจัดเก็บ: ตารางต่อ loc จำนวนตามหน่วย loc / จอง-ว่าง-รวมเป็นฐาน (บวกตาเปล่าได้) · การเคลื่อนไหว: merge ทุก balance + `@ ตำแหน่ง` กำกับ · route refresh-safe `/sku/{pid}`
- **S-03 ดูรายตำแหน่ง (view ตามตำแหน่ง + loc drawer)** — การ์ด/แถวต่อ loc + utilization · เปิด loc drawer: "สิ่งที่อยู่ในตำแหน่งนี้" แสดงตามหน่วยของ loc (OB-4) · เจาะต่อเป็น balance drawer (`/sku/S{id}`) ได้
- **S-04 ค้นหา + กรอง** — ค้น รหัสกลาง/รหัสเก่า/ชื่อ · toggle ซ่อนสต็อก 0 · stat ใบ low/neg กดกรอง (toggle ซ้ำ = ยกเลิก) · sort คอลัมน์เลขใช้ค่าฐาน (เทียบข้ามหน่วยถูก)

### Manual Adjustment
- **S-05 ปรับเพิ่ม/ลด (happy, multi-line)** — เลือกเหตุผล (บังคับ) → line editor: สินค้า / ตำแหน่ง / เพิ่ม-ลด / จำนวน (หน่วยตาม loc) / คงเหลือ live "ปัจจุบัน → หลังปรับ" → summary bar "พร้อมบันทึก n/m · เพิ่มรวม +x ฐาน · ลดรวม −y · รายการใหม่ z ตำแหน่ง" → บันทึก: RAW update + ADJ log 1 เอกสาร (หลายบรรทัด) + movement ต่อ balance + toast
- **S-05b เพิ่มเข้าตำแหน่งว่าง (new balance)** — dropdown ตำแหน่งทุกตัวใน wh ติด label "· ว่าง — เพิ่มเข้าได้ / · มีของ / · ล็อกอยู่" · เลือก loc ที่สินค้านั้นยังไม่มี → คอลัมน์คงเหลือขึ้น "รายการใหม่ในตำแหน่งนี้ · ปัจจุบัน 0 → n" → submit สร้าง balance ใหม่ + log (OB-8)
- **S-06 ลดชนเพดานจอง (blocked)** — ลดเกิน (on_hand − allocated) → error บรรทัด "ลดได้สูงสุด X" + ไม่ให้บันทึก (OB-11) · allocated ไม่ถูกแตะทุกกรณี
- **S-07 ตำแหน่ง/มาสเตอร์ไม่พร้อม (blocked)** — loc ถูก BP-order ล็อก / loc blocked-frozen / master inactive → error ต่อบรรทัด + submit ทั้งใบไม่ผ่านถ้ามีบรรทัด error · service (SV) ไม่มีใน picker และฝืน submit ก็ block (OB-3)

### Monitoring & อื่น ๆ
- **S-08 Low stock (ต้องเติม)** — สินค้า `min_stock>0` และ พร้อมใช้ < min → badge "ต้องเติม" ใน list + stat ใบต่ำกว่าขั้นต่ำนับ+กดกรอง + note ใน drawer "พร้อมใช้ X < threshold Y (ตั้งจาก Item Master)" (OB-6)
- **S-08b ขาดสต็อก (ติดลบ)** — พร้อมใช้ < 0 (จองเกิน — EC-07 by design จาก mock S011) → badge แดง "ขาดสต็อก" + stat ติดลบ + note reconcile ใน drawer — ระบบไม่ block การจองย้อนหลัง (เกิดจากระบบขาย) แต่ฟ้องให้ reconcile
- **S-09 สินค้าบริการ** — SV ไม่โผล่ list/picker/แตกแพ็ค ทุกจุด แม้ data หลุดมา (guard ชั้นจอ `isStockable`)
- **S-10 สิทธิ์** — role อื่นนอกจาก warehouse_staff/finance ไม่เห็นปุ่มปรับสต็อก (OB-12)
- **S-11 Break/Pack** — เปิดลัง→แตกเป็นฐาน / รวมฐาน→แพ็ค เป็น movement แยก · order ที่ active ล็อกตำแหน่งต้นทาง-ปลายทาง (โยงเข้า S-07)
- **S-12 Audit log** — ทุกการปรับ = เอกสาร ADJ (append-only): ผู้ทำ+role, เหตุผล, หมายเหตุ, รายบรรทัด (สินค้า, ตำแหน่ง, ±จำนวนตามหน่วย loc, ก่อน→หลังฐาน) · เปิดดูย้อนหลัง + ค้น/กรองได้

---

## §3 Functions → ดูไฟล์ `FUNCTION_CHECKLIST_F-INV_Stock-by-Location.md` (FN-01..FN-40)

## §4 Data (ต่อ scenario)

- **PRODUCTS**: code, name, type (FG/RM/PM/TR/CN/SV), typeLabel, uom (ฐาน), cost, status, old_code, **min_stock** (nullable — ไม่ตั้ง = ไม่เช็ค low)
- **LOCATIONS**: id, code, type (Pick Face/Reserve/Bulk/Pack/HOLD/Damaged/Virtual), loc_status (active/blocked/frozen), hierarchy refs · **1 loc 1 uom** ผ่าน `locUomIdx`
- **RAW (balances)**: id, pid, loc_id, on_hand (ฐานเสมอ), allocated (ฐาน), in_transit, status (available/damaged/blocked/quarantine), lot/serial/exp, received (FIFO), moved · invariant: (pid,loc_id) unique · ห้ามมี SV
- **ADJLOG**: docNo (ADJ-YYYY-NNNN), at, by+role, reason (6 ค่า), note, lines[{pid, loc_id, dir, qty(หน่วย loc), before/after(ฐาน)}] — append-only
- **BPORDERS**: order แตก/แพ็ค + status (active=ล็อก loc)
- **MOVEMENTS**: ต่อ balance — type (putaway/pick/allocate/adjustment/break/pack), qty ±ฐาน, ref, by, at

## §5 Coverage Matrix

| Scenario | FN หลัก | Guard | เทสแล้ว (E2E) |
|---|---|---|---|
| S-01 | FN-01..05 | OB-2/3 | ✓ one-row-per-sku, stats-new, no-sv |
| S-02 | FN-06..10 | OB-4/7 | ✓ tabs-top/fullwidth, overview default, uomloc consistent |
| S-03 | FN-11..12 | OB-4 | ✓ loc-drawer-unit (20 ลัง = 120 ตัว) |
| S-04 | FN-04, FN-22 | — | ✓ low-filter, sort-ok |
| S-05/05b | FN-13..17 | OB-8 | ✓ create-new-balance, summary, multi-line |
| S-06/07 | FN-15..16 | OB-11 | ✓ guard-allocated, bp-lock-blocks, sv-cannot-adjust |
| S-08/08b | FN-09 | OB-6 | ✓ low-badge, neg-only-EC07 |
| S-11 | FN-23 | — | ✓ bp view + locked badge |
| S-12 | FN-18 | append-only | ✓ adjlog-created, movement-linked |
| Portal/Esc | FN-20 | OB-9 | ✓ panel-in-portal, esc-chain, outside-click |

## §6 Open Questions (OQ)

| OQ | คำถาม | เจ้าภาพ |
|---|---|---|
| OQ-INV-01 | Manual Adjustment มูลค่าสูงต้องมีอนุมัติ (DOA) ไหม? ตอนนี้บันทึกตรงไม่มีสายอนุมัติ — ถ้ามี ให้ประกาศผ่าน DOA กลาง (มีวงเงิน = มูลค่าปรับ) [AI-DRAFT: ควรมี threshold] | Strike |
| OQ-INV-02 | `min_stock` เป็น per-item (รวมทุกคลัง) หรือ per-item-per-warehouse? ตอนนี้เทียบ avail ของคลังที่เปิดอยู่กับ threshold ก้อนเดียว [AI-DRAFT: standard = per warehouse/location group] | Strike + พี่เบิร์ด |
| OQ-INV-03 | หน่วยของตำแหน่ง (1-loc-1-uom) เปลี่ยนได้เมื่อไหร่ — เฉพาะตอน loc ว่างสนิท? ใครมีสิทธิ์? (กระทบ Location Hierarchy master) | Strike |
| OQ-INV-04 | สต็อกติดลบ (จองเกิน EC-07): ใครเป็นเจ้าภาพ reconcile + ระบบขายควรถูก block จองเกิน avail ตั้งแต่ต้นทางไหม | Strike + ทีมขาย |
| OQ-INV-05 | Low stock → ต่อ action อะไร: แจ้งเตือน (F-NT) / สร้าง PR อัตโนมัติ / รายงานเฉย ๆ | Strike |

## §7 Precedents ที่สืบทอด
- Soft-reference LD-4C-02 (master = picker aid) · append-only audit · สถานะ 3 ค่ามาตรฐานเลน (master) · #94 Master Combobox · #95 Portal · #67.1 no-hint · #31 header actions · structured doc ไม่มี import/export (precedent PayTerm/BOM)
