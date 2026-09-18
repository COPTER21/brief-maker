# CSQ_BRIEF — F-WH-STKTRF · Stock Transfer (ใบย้ายสินค้า)

> ใบประกาศ 7C Consequence → **ENG-CSQ (F-CSQ-01)** · deploy pipeline อ่านไฟล์นี้แล้ว auto-register
> feature **ประกาศ event เท่านั้น** — ห้าม hardcode การประทับผลรายท่อ ห้ามคำนวณมูลค่าเอง (ENG-CSQ-02 ทำ)
> ⛔ **ห้ามประกาศซ้ำท่อที่มาอัตโนมัติ** (register จะถูก reject 422):
> - **OC** — เจ้าของคือ Operation Process (`sow.*`) เท่านั้น → **ไม่ประกาศ**
> - **DC ระดับเอกสาร** — DOA engine ยิงให้ตอนอนุมัติ/ตีกลับแล้ว (**ทั้ง 2 จุดตัดสินใจ**) → **ไม่ประกาศ**
> - **SC** — สงวนไว้ `trigger = false` เสมอ → **ไม่ประกาศ**

---

## 1. Identity

| ช่อง | ค่า |
|---|---|
| profile key | `CSQ-WH-STKTRF` |
| feature_id | `F-WH-STKTRF` (fid F083) |
| ชื่อ | Stock Transfer — ใบย้ายสินค้า (ย้ายคลัง/สาขา) |
| module | Warehouse (WH) |
| กลุ่ม | A (feature ใหม่ · ประกาศพร้อม Phase A) |
| register status | `pending` |

---

## 2. Event ที่ประกาศ (เฉพาะ transition ที่ "จบแล้วมีผล")

> ❌ ไม่ประกาศ `ร่าง → รออนุมัติ` — ยังไม่มีผลทางธุรกิจ (ของยังไม่ขยับ)
> ❌ ไม่ประกาศ `รออนุมัติ → อนุมัติแล้ว` / การตีกลับ — **DC ระดับเอกสาร** DOA engine เป็นเจ้าของ

| # | event_id | Trigger (อ้าง PREBRIEF) | ท่อที่กระทบ | kind / basis | เงื่อนไข |
|---|---|---|---|---|---|
| 1 | ★ `trf_shipped_to_transit` | `อนุมัติแล้ว → ส่งออกแล้ว — อยู่ระหว่างทาง` · **โหมดข้ามคลังเท่านั้น** (§5.1 · S-01 ขา 1 · BR-15) | **EC** | `estimated` · `basis: computed` จาก `Σ (จำนวนที่ย้าย × ต้นทุนอ้างอิง)` | ★ **มูลค่าที่ "อยู่ในมือกิจการแต่ไม่อยู่ในคลังไหนเลย"** — เป็นความเสี่ยงที่ต้องเห็นได้ · `estimated` เพราะ **ยังไม่จบ** ปลายทางอาจรับไม่ครบ (event 3) |
| 2 | ★ `trf_received_at_destination` | `ส่งออกแล้ว/รับบางส่วน → ปิดใบ (รับครบ)` และทุกครั้งที่รับบางส่วน (§5.1 · S-01 ขา 2 · S-06) | **EC** | `actual` · `basis: computed` จาก `Σ (จำนวนที่รับครั้งนี้ × ต้นทุนอ้างอิง)` → **หักออกจากยอด `estimated` ของ event 1** | ★ **ปิดความเสี่ยงของ event 1 ทีละส่วน** — ยอด in-transit ที่ยังไม่ถูกหัก = ของที่ยังลอยอยู่จริง |
| 3 | ★★ `trf_shortage_written_off` | `→ ปิดใบพร้อมส่วนต่าง` หลัง **DOA สาย B1** อนุมัติครบ (§5.1 · S-07 · BR-18) | **EC** | `actual` · `basis: computed` จาก `Σ (จำนวนส่วนต่างที่ตัด × ต้นทุนอ้างอิง)` | ★★ **ผลขาดทุนจริงของกิจการ — event สำคัญที่สุดของ feature นี้** · ของหายไปจริง ไม่มีใครได้ใช้ · **ไม่รวมส่วนที่ตีกลับคืนต้นทาง** (BR-19) |
| 4 | `trf_returned_to_source` | `→ ตีกลับคืนต้นทางแล้ว` (§5.1 · S-08 · BR-19) | **EC** | `avoided` → **หักยอด `estimated` ของ event 1 ออกทั้งจำนวนที่ตีกลับ** | ★ **ของไม่ได้หาย — กลับเข้า bin ต้นทางครบ** จึงต้องปลดความเสี่ยงออกจากยอด in-transit ไม่ใช่ตัดเป็นขาดทุน |
| 5 | `trf_moved_intra_warehouse` | `อนุมัติแล้ว → ย้ายสำเร็จ` · **โหมดภายในคลังเท่านั้น** (§5.1 · S-02) | — **no-effect** | — | ★ **ประกาศเป็น no-effect โดยเจตนา** — ย้ายข้ามชั้นวางในคลังเดียวกัน **มูลค่ารวมไม่เปลี่ยน ไม่มีช่วง in-transit ไม่มีความเสี่ยงใหม่** · บันทึกไว้กันคนมาเติมท่อทีหลัง |
| 6 | `trf_reversed` | `ใบปิดแล้ว → กลับรายการแล้ว` (§5.1 · S-15 · BR-26) | **EC** | `avoided` → หักผลของ event 1/2/3 ของใบนั้นออก | เฉพาะใบที่เคยปิด · movement ทิศตรงข้ามครบทุกเส้น (append-only ไม่ลบของเดิม) |
| 7 | `trf_cancelled` | `ร่าง/รออนุมัติ/อนุมัติแล้ว → ยกเลิก` (§5.1 · S-13 · BR-21) | — **no-effect** | — | **ประกาศเป็น no-effect โดยเจตนา** — ของไม่เคยขยับ ไม่มีท่อไหนถูกกระทบ |

> ★ **ทำไม event 1 เป็น `estimated` ไม่ใช่ `actual`:** ตอนส่งออก **ยังไม่รู้ว่าจะจบยังไง** — อาจรับครบ (event 2 = actual) อาจหาย (event 3 = actual ขาดทุน) อาจตีกลับ (event 4 = avoided) · ถ้าประทับ `actual` ตั้งแต่ส่งออกจะ **นับซ้ำกับ event 2/3/4** ที่ตามมา
> ★ **สมการที่ Engine ต้องเห็นเป็นจริงเสมอ:** `event 1 (estimated) = event 2 (actual) + event 3 (actual) + event 4 (avoided) + ยอดที่ยังค้าง in-transit` — ตรงกับ invariant ใน PREBRIEF §5.2

---

## 3. ท่อที่ **ไม่** ประกาศ + เหตุผล (ต้องเขียนชัด กันประกาศซ้ำ)

| ท่อ | ประกาศไหม | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ ไม่ | เจ้าของคือ Operation Process (`sow.*`) — StockTransfer ไม่ใช่ต้นทาง OC |
| **DC** (Decision) | ❌ ไม่ | การอนุมัติ/ตีกลับ **ทั้ง 2 จุดตัดสินใจ** (อนุมัติการย้าย · อนุมัติการตัดส่วนต่าง) = **DC ระดับเอกสาร** ที่ DOA engine ยิงเองแล้ว · StockTransfer ไม่มี terminal decision (Continue/Adjust/Hold/Stop) นอกเหนือการเซ็นอนุมัติ · ★ *หมายเหตุ: "ปลายทางตีกลับคืนต้นทาง" (S-08) ดูคล้าย terminal decision แต่จริง ๆ คือ **การจัดการส่วนต่างเชิงปฏิบัติการ** ไม่ใช่การตัดสินชะตากรรมของ business object* `[AI-DRAFT]` — ดู CSQ-Q2 |
| **SC** | ❌ ไม่ | สงวนไว้ `trigger = false` เสมอ |
| **SecC** (Security) | ❌ ไม่ | StockTransfer ไม่แก้ข้อมูลอ่อนไหว/สิทธิ์/นโยบาย · Location Master + Item Master เป็นของ feature อื่น (soft-ref **อ่านอย่างเดียว** — BR-33 ห้ามแก้ผังในหน้านี้) `[AI-DRAFT]` |
| **AC** (Accounting) | ❌ ไม่ | **StockTransfer ไม่ post บัญชีเองในรอบนี้** — รายการบัญชีจริง (โอนระหว่างคลัง/สาขา · **ผลขาดทุนสินค้าระหว่างขนส่ง**) เกิดฝั่ง **GL ใน W5** · รอบนี้ mock + `TODO: JE posting` (PREBRIEF BR-24) · เมื่อ W5 มาแล้วให้ **GL เป็นเจ้าของท่อ AC** กันนับซ้ำ (สอดคล้อง StockAdj CSQ-Q2) |
| **FC** (Financial/เงินสด-งบ) | ❌ ไม่ | การย้ายสินค้า **ไม่กระทบเงินสดและไม่กิน commit งบ** — ไม่มีการจ่าย ไม่มีภาระผูกพันใหม่กับคู่ค้าภายนอก · แม้กรณีของหาย (event 3) ก็เป็นการรับรู้ขาดทุนทางบัญชี **ไม่ใช่กระแสเงินสดออก** `[AI-DRAFT]` |

---

## 4. Payload contract (field ที่ต้องมีจริงใน entity — ตรวจกับ PREBRIEF §3)

| field | ที่มา | หมายเหตุ |
|---|---|---|
| `ref` = `trf_id` | header | soft-reference ทุก event |
| `trf_no` | doccfg `TRF-YYYY-NNNN` (§3.1) | ปี **ค.ศ.** |
| ★ `transfer_mode` | §3.1 derive `intra_warehouse \| inter_warehouse` | **ตัวแยกว่า event 5 (no-effect) หรือ event 1–4** |
| `warehouse_from_ref` / `warehouse_to_ref` | §3.1 (soft-ref LD-4C-02) | 1 ใบ = 1 คู่คลัง (BR-02) |
| ★ `in_transit_location_ref` | §3.1 (`TR-*` ใน `WH-TRN`) | ★ **ระบบจับคู่ให้ ผู้ใช้แตะไม่ได้** (BR-05) · ว่างเมื่อโหมด intra |
| ★ `total_transfer_amount` | §3.3 `Σ (จำนวนที่ย้าย × ต้นทุนอ้างอิง)` | **ตัวเดียวกับฐาน DOA สาย A1/A2** — บวกเสมอ |
| ★ `received_amount_this_time` | §3.2 · §3.3 | ฐานของ event 2 (ยิงทุกครั้งที่รับ ไม่ใช่แค่ตอนปิดใบ) |
| ★ `shortage_written_off_amount` | §3.3 `มูลค่าส่วนต่างที่ตัดทิ้ง` | **ตัวเดียวกับฐาน DOA สาย B1** · **ไม่รวมที่ตีกลับคืนต้นทาง** |
| ★ `returned_to_source_amount` | §3.2 · §3.3 | ฐานของ event 4 (`avoided`) |
| ★ `in_transit_remaining_amount` | §3.3 `Σ (คงค้างระหว่างทาง × ต้นทุนอ้างอิง)` | ★ **ตัวที่ทำให้สมการใน §2 ตรวจได้** |
| `shortage_reason_code` | §3.2 master เหตุผลส่วนต่าง (`DF-01`…`DF-99`) | ใช้จัดกลุ่มผลกระทบ · มี **บัญชีปลายทาง mock** ติดมาด้วย |
| `unit_cost_ref` | §3.2 Item Master (**mock**) | ★ `[ASSUMED contract]` — **valuation engine จริง = W5** · `FWD-WIRE: valuation engine` |
| `actor_ref` + `occurred_at` | §3.4 movement | **คนจริง** + timestamp ปี **ค.ศ.** |

> **Restricted / masking:** feature นี้ **ไม่มี field อ่อนไหว** (ไม่มีข้อมูลบุคคล/ราคาขาย/เครดิต) — ต้นทุนอ้างอิงเป็นข้อมูลภายในที่ผู้ใช้คลังเห็นอยู่แล้ว `[AI-DRAFT]`

---

## 5. Register Checklist (ก่อน deploy จะ register สำเร็จ)

- [ ] ทุก event มี `ref` (soft-reference) ครบ ✅ 7/7
- [ ] ไม่มี **OC** / **DC** / **SC** ในรายการที่ประกาศ ✅ (ตรวจแล้ว §3)
- [ ] event ที่ยิง **EC** มี `kind` ครบ (`estimated` / `actual` / `avoided`) ✅ 5/5
- [ ] event `no-effect` ระบุเหตุผลชัด ✅ 2/2 (event 5 · event 7)
- [ ] payload field ทุกตัวมีอยู่จริงใน entity ตาม PREBRIEF §3 ✅
- [ ] `unit_cost_ref` ติด `[ASSUMED contract]` + `FWD-WIRE: valuation engine` ✅ (ยังไม่มี valuation engine จริง)
- [ ] ★ ตรวจสมการกันนับซ้ำ: `event 1 = event 2 + event 3 + event 4 + คงค้าง` ✅ (ตรงกับ invariant PREBRIEF §5.2)
- [ ] toggle register status `pending → connected`

---

## 6. Open Questions

| # | คำถาม | ค่าที่ใช้รอบนี้ | ใครต้องตอบ |
|---|---|---|---|
| **CSQ-Q1** | event 1 ควรเป็น `estimated` หรือไม่ควรยิงเลยจนกว่าจะจบ | **ยิงเป็น `estimated`** — เพราะยอด in-transit คือความเสี่ยงที่ต้องเห็นระหว่างทาง ไม่ใช่หลังจบ `[AI-DRAFT]` | **Strike / เจ้าของ ENG-CSQ** |
| **CSQ-Q2** | "ปลายทางตีกลับคืนต้นทาง" (S-08) ควรนับเป็น **DC terminal decision** ไหม | **ไม่** — เป็นการจัดการส่วนต่างเชิงปฏิบัติการ ไม่ใช่การตัดสินชะตากรรม business object `[AI-DRAFT]` | **Strike / เจ้าของ F-CSQ-01** |
| **CSQ-Q3** | เมื่อ W5 มา ใครเป็นเจ้าของท่อ **AC** สำหรับผลขาดทุนระหว่างขนส่ง | **GL (W5)** — StockTransfer ไม่ประกาศ AC เพื่อกันนับซ้ำ (สอดคล้อง StockAdj) | **W5** |
| **CSQ-Q4** | ต้นทุนอ้างอิงถือเป็นข้อมูล Restricted ที่ต้อง mask ไหม | **ไม่** รอบนี้ `[AI-DRAFT]` — ยกไปเป็น Security Preset ตอน BRD | **Strike** |
