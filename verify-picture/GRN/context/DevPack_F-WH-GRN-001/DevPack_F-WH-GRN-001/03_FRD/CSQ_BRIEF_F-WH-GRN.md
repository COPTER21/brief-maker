# CSQ_BRIEF — F-WH-GRN · GRN รับของ

> ใบประกาศ 7C Consequence → **ENG-CSQ (F-CSQ-01)** · deploy pipeline อ่านไฟล์นี้แล้ว auto-register
> feature **ประกาศ event เท่านั้น** — ห้าม hardcode การประทับผลรายท่อ ห้ามคำนวณมูลค่าเอง (ENG-CSQ-02 ทำ)
> ⛔ **ห้ามประกาศซ้ำท่อที่มาอัตโนมัติ** (register จะถูก reject 422):
> - **OC** — เจ้าของคือ Operation Process (`sow.*`) เท่านั้น → **ไม่ประกาศ**
> - **DC ระดับเอกสาร** — DOA engine ยิงให้ตอนอนุมัติ/ปฏิเสธ · **GRN ไม่มี DOA เลย** → **ไม่ประกาศ**
> - **SC** — สงวนไว้ `trigger = false` เสมอ (OQ-C3 ยังไม่เคาะ) → **ไม่ประกาศ**

---

## 1. Identity

| ช่อง | ค่า |
|---|---|
| profile key | `CSQ-WH-GRN` |
| feature_id | `F-WH-GRN` (fid F079) |
| ชื่อ | GRN รับของ |
| module | Warehouse (WH) |
| register status | `pending` |

---

## 2. Event ที่ประกาศ (เฉพาะ transition ที่ "จบแล้วมีผล")

> ❌ ไม่ประกาศ `— → draft` / แก้ร่าง / ทิ้งร่าง — ไม่มีผลทางธุรกิจ (stock ไม่ขยับ)
> ❌ ไม่ประกาศ event การอนุมัติใด ๆ — **feature นี้ไม่มีสายอนุมัติ**

| # | event_id | Trigger (อ้าง PREBRIEF) | ท่อที่กระทบ | kind / basis | เงื่อนไข |
|---|---|---|---|---|---|
| 1 | `grn_posted` | `draft → posted` (§5.1 · S-07) | **AC** (ลงบัญชี — ตั้ง GR/IR) · **EC** (มูลค่าสินค้าคงคลังเพิ่ม) | `actual` / `basis: computed` จากมูลค่าที่รับ (§3.3) | ทุกใบที่ post สำเร็จ · มูลค่า = ยอดรวมก่อนภาษี · **JE จริงยังไม่ post** `TODO: JE posting` (W5) |
| 2 | `grn_quarantined` | post แล้วมีบรรทัดที่ QC ไม่ผ่าน > 0 (§5.1 · S-12/S-13 · BR-09/BR-10) | **EC** (มูลค่าของที่ถูกกักไว้ ใช้/ขายไม่ได้) | `estimated` / `basis: computed` — `[DEFAULT — รอยืนยัน]` | เฉพาะจำนวนที่ไม่ผ่าน QC × ราคาต่อหน่วยจาก PO · ปลดเมื่อ RTV/ปล่อยของ (feature ถัดไปเป็นคนยิง) |
| 3 | `grn_reversed` | `posted → reversed` (§5.1 · S-08 · BR-15) | **AC** · **EC** | `actual` (กลับรายการ) · ต้องมี `reversal_of` = event id ของ `grn_posted` ใบเดิม | ทั้งใบเท่านั้น (ไม่ reverse บางบรรทัด) · **ห้ามลบ/แก้ผลเดิม** (BR-CSQ-04) |

---

## 3. ท่อที่ **ไม่** ประกาศ + เหตุผล (ต้องเขียนชัด กันประกาศซ้ำ)

| ท่อ | ประกาศไหม | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ ไม่ | เจ้าของคือ Operation Process (`sow.*`) — GRN ไม่ใช่ต้นทาง OC |
| **DC** (Decision) | ❌ ไม่ | **GRN ไม่มีสายอนุมัติ (ไม่มี DOA)** และไม่มี terminal decision นอกเหนือการบันทึกข้อเท็จจริงการรับของ (CONTEXT_PACK §2.2) |
| **SC** | ❌ ไม่ | สงวนไว้ `trigger = false` เสมอ |
| **SecC** (Security) | ❌ ไม่ | GRN ไม่แก้ข้อมูลอ่อนไหว/สิทธิ์/นโยบาย — master ทุกตัวเป็น soft-ref อ่านอย่างเดียว (LD-4C-02) |
| **FC** (เงินสด/งบ) | ❌ ไม่ | **PO เป็นเจ้าของวงจร commitment ทั้งหมด** — `po_commitment_consumed` ถูกประกาศไว้แล้วใน `CSQ_BRIEF_F-PUR-PO.md` (event 5) · ถ้า GRN ยิง FC ด้วยจะ **นับซ้ำ** → ดู CSQ-Q2 |

---

## 4. Payload contract (ทุก field มีอยู่จริงใน PREBRIEF §3 — ห้ามแต่งฟิลด์ใหม่)

| field | ที่มา | หมายเหตุ |
|---|---|---|
| `ref` = `grn_id` | header (§3.1) | soft-reference ทุก event |
| `grn_no` | doccfg `GRN-YYYY-NNNN` (§3.1) | ปี **ค.ศ.** · มีเมื่อ post แล้วเท่านั้น |
| `po_ref` / `po_no` | อ้างอิง PO (§3.1) | soft-ref ไปเอกสารต้นทาง |
| `vendor_ref` | ผู้ขาย (§3.1 · จาก PO · soft-ref LD-4C-02) | nullable-safe |
| `warehouse_ref` · `quarantine_location_ref` | คลังปลายทาง · quarantine location (§3.1/§3.2) | soft-ref |
| `received_value_ex_vat` | ยอดรวมก่อนภาษีของใบรับ (§3.3) | ใช้กับ event 1 และ 3 |
| `quarantined_value` | `Σ (จำนวนที่ไม่ผ่าน QC × ราคาต่อหน่วยสุทธิ)` (§3.2/§3.3) | ใช้กับ event 2 |
| `line_refs[]` | อ้าง PO line + ลำดับบรรทัด (§3.2) | ให้ engine ไล่กลับได้ |
| `reject_reason` | เหตุผลที่ไม่ผ่าน QC (§3.2) | เฉพาะ event 2 |
| `reversal_of` · `reversal_reason` | ใบ/เหตุผลกลับรายการ (§3.1) | เฉพาะ event 3 — **บังคับ** |
| `occurred_at` | timestamp (**ค.ศ.**) | ทุก event |
| `actor` | ผู้รับของ / ผู้กลับรายการ (คนจริง §3.1) | ทุก event |

> ⚠️ ทุกมูลค่าเป็น `basis: computed` จาก field ที่มีจริงในใบ — **feature ห้ามตีมูลค่าเพิ่มเอง** (ห้ามคิด landed cost / ต้นทุนเฉลี่ย — F069/F070 · W4 เป็นเจ้าของ) · ENG-CSQ-02 เป็นคนประเมิน

---

## 5. Register Checklist (ก่อน deploy)

- [ ] `CSQ-WH-GRN` ยังไม่มีใน Profile Registry (ถ้ามีแล้ว = update ไม่ใช่ register ใหม่)
- [ ] ทุก event มี trigger point ที่ชี้ transition จริงใน PREBRIEF §5.1 ได้
- [ ] ไม่มี OC / DC / SC / FC ในใบนี้ (กัน 422)
- [ ] `grn_reversed` ส่ง `reversal_of` เสมอ (BR-CSQ-04)
- [ ] `idempotency_key` unique ต่อ (feature, grn_id, action) — กันยิงซ้ำตอน retry (BR-CSQ-02)

---

## 6. HTML/FRD Injection note

- HTML **ไม่ต้องวาด UI ประเมินผลกระทบ 7 ท่อ** — Engine เป็นคนประทับ · feature แค่รู้ว่า emit ตอนไหน
- จุด emit = transition ตาม §2 เท่านั้น (ตรงกับ state machine PREBRIEF §5.1)
- Phase A (HTML): mock + marker `FWD-WIRE: ENG-CSQ emit` ที่ปุ่ม "รับเข้า (post)" และ "กลับรายการ" (ในไฟล์ .md ใช้ `TODO:` ตามปกติ)
- ❌ ห้ามมี `const PIPES_HIT = [...]` หรือ column เก็บผลรายท่อในตารางของ feature
- FRD Phase B: `05_RULES.md` เพิ่มหัวข้อ "ผลกระทบ 7C (CSQ)" ชี้มาที่ไฟล์นี้ + BR-CSQ-01..05

---

## 7. Open Questions

| # | ประเด็น | ใครตอบ |
|---|---|---|
| CSQ-Q1 | `grn_posted` ยิง **AC** ทั้งที่ JE ยังไม่ post จริง (W5) — ควรยิงตอนนี้เลย หรือรอให้ GL เป็นคนยิงเมื่อ W5 มา (กันนับซ้ำ) | เจ้าของ F-CSQ-01 + เจ้าของ GL (W5) |
| CSQ-Q2 | **FC**: PO ยิง `po_commitment_consumed` ตอนปิดใบ — ถ้าอยากได้ FC ตอน "ของถึงจริง" ต้องย้ายเจ้าของท่อมาที่ GRN หรือไม่ | เจ้าของ F-CSQ-01 + Strike |
| CSQ-Q3 | `grn_quarantined` (EC ของที่ถูกกัก) ควรเป็น event ของ GRN หรือของ **RTV** ที่เป็นคนจัดการปลายทาง — และใครเป็นคน "ปลด" มูลค่านั้น | เจ้าของ F-CSQ-01 + เจ้าของ F-PUR-RTV |
| CSQ-Q4 | มูลค่าที่รับควรใช้ราคาจาก PO หรือรอ landed cost (F069 · W4) — รอบนี้ใช้ราคาจาก PO ตรง ๆ | เจ้าของ F069 + Strike |
