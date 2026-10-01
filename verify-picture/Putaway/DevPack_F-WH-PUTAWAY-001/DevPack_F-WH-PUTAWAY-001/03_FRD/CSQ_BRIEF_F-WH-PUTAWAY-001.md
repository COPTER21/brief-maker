# CSQ_BRIEF — F-WH-PUTAWAY · Putaway (จัดเก็บเข้าที่)

> ใบประกาศ 7C Consequence → **ENG-CSQ (F-CSQ-01)** · deploy pipeline อ่านไฟล์นี้แล้ว auto-register
> feature **ประกาศ event เท่านั้น** — ห้าม hardcode การประทับผลรายท่อ ห้ามคำนวณมูลค่าเอง (ENG-CSQ-02 ทำ)
> ⛔ **ห้ามประกาศซ้ำท่อที่มาอัตโนมัติ** (register จะถูก reject 422):
> - **OC** — เจ้าของคือ Operation Process (`sow.*`) เท่านั้น → **ไม่ประกาศ**
> - **DC ระดับเอกสาร** — DOA engine ยิงให้ตอนอนุมัติ/ปฏิเสธ · **Putaway ไม่มี DOA เลย** → **ไม่ประกาศ**
> - **SC** — สงวนไว้ `trigger = false` เสมอ (OQ-C3 ยังไม่เคาะ) → **ไม่ประกาศ**
> ★ **Putaway = console ไม่ใช่เอกสาร** — declarations รอบนี้มีแค่ `csq` (ไม่มี doa / ntf / doccfg / pdfdoc)

---

## 1. Identity

| ช่อง | ค่า |
|---|---|
| profile key | `CSQ-WH-PUTAWAY` |
| feature_id | `F-WH-PUTAWAY` (fid F081) |
| ชื่อ | Putaway — จัดเก็บเข้าที่ |
| module | Warehouse (WH) |
| arch | master/console (**ไม่ใช่เอกสาร · ไม่มีเลขรัน**) |
| register status | `pending` |

---

## 2. Event ที่ประกาศ (เฉพาะที่ "จบแล้วมีผลเฉพาะทางที่ยังไม่มีใครนับ")

> ❌ ไม่ประกาศ `รับงาน` / `คืนงาน` / `ปลดล็อกงาน` — เป็นการจองงาน ไม่มีผลทางธุรกิจ (ของไม่ขยับ)
> ❌ ไม่ประกาศ event การอนุมัติใด ๆ — **feature นี้ไม่มีสายอนุมัติ**
> ★ ❌ **ไม่ประกาศ `putaway_confirmed` (ทางเดินปกติ)** — เหตุผลเต็มอยู่ §3 (GRN เป็นเจ้าของมูลค่าของก้อนเดียวกันแล้ว → ประกาศซ้ำ = **นับซ้ำ**)

| # | event_id | Trigger (อ้าง PREBRIEF) | ท่อที่กระทบ | kind / basis | เงื่อนไข |
|---|---|---|---|---|---|
| 1 | `putaway_forced_override` | ยืนยันจัดเก็บโดยที่ `ที่มาของการเลือก = override` และ **ฝืนเกณฑ์** (นอกรายการแนะนำ / ข้ามหมวดโซน / เกินความจุ bin) — §5.1 `กำลังจัดเก็บ → จัดเก็บแล้ว` · S-07/S-08 · **BR-11 / BR-15** | **EC** (ต้นทุนแฝงจากการเก็บผิดที่: หยิบยาก · ต้องย้ายซ้ำภายหลัง · เสี่ยงของหาย) | `estimated` / **`basis: declared`** (qty-only) | ยิงเฉพาะแถวปลายทางที่ฝืนเกณฑ์ · **ห้ามใส่ตัวเลขเงิน** — ยังไม่มี Rate Card ของงานย้ายซ้ำ (§7 CSQ-Q2) |
| 2 | `putaway_reversed` | `จัดเก็บแล้ว → รอจัดเก็บ` (§5.1 · S-13 · **BR-17**) | **EC** (แรงงานจัดเก็บที่เสียเปล่า + ของกลับไปอยู่สถานะเบิกไม่ได้ชั่วคราว) | `estimated` / **`basis: declared`** (qty-only) · **ต้องมี `reversal_of`** | หัวหน้าคลังเท่านั้น + เหตุผลบังคับ · **ห้ามลบ/แก้ผลเดิม** (BR-CSQ-04) · movement append-only |

> ทั้ง 2 event เป็น **ผลกระทบที่ไม่มี feature ไหนในระบบนับอยู่** — คือเหตุผลเดียวที่ Putaway ต้องมีใบประกาศนี้

---

## 3. ท่อที่ **ไม่** ประกาศ + เหตุผล (ต้องเขียนชัด กันประกาศซ้ำ / กันนับซ้ำ)

| ท่อ | ประกาศไหม | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ ไม่ | เจ้าของคือ Operation Process (`sow.*`) — Putaway เป็นงาน execution ในคลัง ไม่ใช่ต้นทาง OC · **ประกาศ = reject 422** |
| **DC** (Decision) | ❌ ไม่ | **Putaway ไม่มีสายอนุมัติ (ไม่มี DOA)** (CONTEXT_PACK §2.2) และ "ยืนยันจัดเก็บ" ไม่ใช่ terminal decision — เป็นการบันทึกว่างานทำเสร็จ |
| **SC** | ❌ ไม่ | สงวนไว้ `trigger = false` เสมอ |
| **SecC** (Security) | ❌ ไม่ | ไม่แตะข้อมูลอ่อนไหว/สิทธิ์/นโยบาย — master ทุกตัวเป็น soft-ref อ่านอย่างเดียว (LD-4C-02 · BR-23) |
| **AC** (ลงบัญชี) | ❌ ไม่ | Putaway = **ย้ายของภายในคลังเดียวกัน** (BR-25) → ไม่เกิดรายการทางบัญชี · **`grn_posted` ตั้ง GR/IR ไปแล้ว** (`CSQ_BRIEF_F-WH-GRN.md` event 1) · ยิงอีก = นับซ้ำ · กรณีข้าม valuation area ยังไม่เคาะ → **CSQ-Q3** |
| **FC** (เงินสด/งบ) | ❌ ไม่ | **PO เป็นเจ้าของวงจร commitment ทั้งหมด** (`po_commitment_consumed` ใน `CSQ_BRIEF_F-PUR-PO.md`) — putaway ไม่แตะเงินสดหรืองบเลย |
| **EC จากการจัดเก็บปกติ** (`putaway_confirmed`) | ❌ **ไม่ประกาศ** | ★ **มูลค่าสินค้าคงคลังของก้อนนี้ถูก `grn_posted` ประกาศ EC ไปแล้ว** — putaway แค่เปลี่ยน location ไม่ได้เพิ่ม/ลดมูลค่า · ประกาศอีก = **นับซ้ำทั้งก้อน** → ดู **CSQ-Q1** |
| **EC ของ quarantine** | ❌ ไม่ | `grn_quarantined` (GRN event 2) เป็นเจ้าของมูลค่าของที่ถูกกักแล้ว · การย้ายของ quarantine ระหว่าง bin quarantine ด้วยกัน (BR-04) ไม่เปลี่ยนมูลค่าที่ถูกกัก · **ผู้ปลดคือ RTV** |

---

## 4. Payload contract (ทุก field มีอยู่จริงใน PREBRIEF §3 — ห้ามแต่งฟิลด์ใหม่)

| field | ที่มา | ใช้กับ event | หมายเหตุ |
|---|---|---|---|
| `ref` = `putaway_task_id` | รหัสงาน `PT-<seq>` (§3.1) | 1, 2 | **รหัสภายใน ไม่ใช่เลขที่เอกสาร** — Putaway ไม่มีเลขรัน |
| `grn_ref` · `grn_line_no` | อ้างอิง GRN / GRN line (§3.1) | 1, 2 | soft-ref กลับเอกสารต้นทาง |
| `item_ref` · `item_category` | สินค้า · หมวดสินค้า (§3.1) | 1, 2 | soft-ref LD-4C-02 · nullable-safe |
| `qty` · `uom_ref` | จำนวนที่เก็บ (§3.2) · หน่วย (§3.1) | 1, 2 | **หน่วยนับ ไม่ใช่เงิน** (basis: declared) |
| `warehouse_ref` · `from_location_ref` | คลัง · location ต้นทาง (§3.1 · §3.0) | 1, 2 | ประเภทตาม §3.0.2 |
| `to_bin_ref` · `to_zone_ref` | bin/โซนปลายทาง (§3.2 · §3.0.4) | 1, 2 | soft-ref |
| `selection_source` | ที่มาของการเลือก — `แนะนำอันดับ 1 / แนะนำอันดับรอง / override` (§3.2) | 1 | **ตัวคัดกรอง event 1** — ยิงเฉพาะ `override` ที่ฝืนเกณฑ์ |
| `override_reason` | เหตุผล override จาก master เหตุผล (§3.2 · §3.6) | 1 | **บังคับ** เมื่อฝืนเกณฑ์ (BR-11) |
| `violation_kind` | derive: `นอกรายการแนะนำ / ข้ามหมวดโซน / เกินความจุ` (§3.5 · S-07/S-08) | 1 | ให้ engine แยกชนิดต้นทุนแฝงได้ |
| `bin_capacity_remaining` | ความจุคงเหลือของ bin (§3.0.4 · §3.2) | 1 | ใช้กับ `violation_kind = เกินความจุ` |
| `reversal_of` · `reversal_reason` | รายการที่ถูกกลับ · เหตุผลกลับรายการ (§3.3) | 2 | **บังคับ** (BR-CSQ-04 · BR-17) |
| `occurred_at` | timestamp (**ค.ศ. ล้วน**) (§3.3) | 1, 2 | BR-22 |
| `actor` | ผู้จัดเก็บ / ผู้กลับรายการ — **คนจริง** (§3.1 · BR-24) | 1, 2 | ห้าม role ID |

> ⚠️ **ทุก event ในใบนี้เป็น `basis: declared` (qty-only)** — ยังไม่มี Rate Card ของงานหยิบ/ย้ายซ้ำ → **feature ห้ามใส่ตัวเลขเงินเด็ดขาด** (Quality Gate G7) · ENG-CSQ-02 เป็นคนตีมูลค่าเมื่อมี Rate Card

---

## 5. Register Checklist (ก่อน deploy)

- [ ] `CSQ-WH-PUTAWAY` ยังไม่มีใน Profile Registry (ถ้ามีแล้ว = update ไม่ใช่ register ใหม่)
- [ ] ทุก event มี trigger point ที่ชี้ transition จริงใน PREBRIEF §5.1 ได้ (G4)
- [ ] **ไม่มี OC / DC / SC ในใบนี้** (กัน 422 · G1–G3)
- [ ] ไม่มี AC / FC ในใบนี้ — เจ้าของคือ GRN และ PO ตามลำดับ (กันนับซ้ำ)
- [ ] ทุก event EC ระบุ `kind` ครบ (G6) และเป็น `basis: declared` ไม่มีตัวเลขเงิน (G7)
- [ ] `putaway_reversed` ส่ง `reversal_of` เสมอ (BR-CSQ-04)
- [ ] `idempotency_key` unique ต่อ (feature, putaway_task_id, to_bin_ref, action) — **1 งานเก็บได้หลาย bin (split S-03) จึงต้องมี bin ใน key** (BR-CSQ-02)

---

## 6. HTML/FRD Injection note

- HTML **ไม่ต้องวาด UI ประเมินผลกระทบ 7 ท่อ** — Engine เป็นคนประทับ · feature แค่รู้ว่า emit ตอนไหน
- จุด emit = **ปุ่ม "ยืนยันจัดเก็บ"** (เฉพาะแถวที่ `selection_source = override` + ฝืนเกณฑ์) และ **"กลับรายการจัดเก็บ"** ในมุมมองประวัติ
- Phase A (HTML): mock + marker **`FWD-WIRE: ENG-CSQ emit`** (ในไฟล์ .md ใช้ `TODO:` ตามปกติ)
- ❌ ห้ามมี `const PIPES_HIT = [...]` หรือ column เก็บผลรายท่อในตารางของ feature
- ❌ ห้ามคำนวณ "ต้นทุนแฝงจากการเก็บผิดที่" เป็นเงินในหน้าจอ — แสดงได้แค่ **ป้าย "ฝืนเกณฑ์"** + **KPI อัตรา override (นับรายการ)** (§3.4)
- FRD Phase B: `05_RULES.md` เพิ่มหัวข้อ "ผลกระทบ 7C (CSQ)" ชี้มาที่ไฟล์นี้ + BR-CSQ-01..05

---

## 7. Open Questions

| # | ประเด็น | ใครตอบ |
|---|---|---|
| CSQ-Q1 | ★ ควรมี event `putaway_confirmed` แบบ **value-neutral** (ไม่ยิงท่อ) ไว้ให้ Engine ไล่ timeline ของก้อนสินค้าได้ไหม — รอบนี้ **ไม่ประกาศ** เพราะกลัวนับซ้ำกับ `grn_posted` | เจ้าของ F-CSQ-01 |
| CSQ-Q2 | Rate Card ของ **งานย้ายซ้ำ / งานหยิบที่ยากขึ้น** ใครเป็นเจ้าของ — จนกว่าจะมี ทั้ง 2 event เป็น `basis: declared` (qty-only) | เจ้าของ ENG-CSQ-02 + Strike |
| CSQ-Q3 | putaway **ข้าม valuation area** (ถ้าอนาคตมีคลังคนละ valuation) ต้องยิง **AC** ไหม — รอบนี้ถือว่าไม่กระทบบัญชี (`OQ-PUT-08 [AI-DRAFT]`) | เจ้าของ GL (W5) + Strike |
| CSQ-Q4 | เกณฑ์ **aging งานค้างจัดเก็บ** (ของรับแล้วแต่เบิกไม่ได้) ควรเป็น event เข้า 7C หรือเป็นแค่ KPI ในหน้าจอ — รอบนี้เป็น KPI + NC rules เท่านั้น | เจ้าของ F-CSQ-01 + Strike (`OQ-PUT-06`) |
| CSQ-Q5 | เมื่อ **Stock Transfer** (W3Q ตัวถัดไป) มา ต้องระวังไม่ให้ยิง EC ซ้ำกับ `putaway_forced_override` กรณีที่การย้ายเกิดเพราะเก็บผิดที่ตั้งแต่แรก | เจ้าของ F-WH-STKTRF + เจ้าของ F-CSQ-01 |
