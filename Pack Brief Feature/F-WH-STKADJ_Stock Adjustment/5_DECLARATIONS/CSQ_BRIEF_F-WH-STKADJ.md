# CSQ_BRIEF — F-WH-STKADJ · Stock Adjustment (ใบปรับยอดสต๊อก)

> ใบประกาศ 7C Consequence → **ENG-CSQ (F-CSQ-01)** · deploy pipeline อ่านไฟล์นี้แล้ว auto-register
> feature **ประกาศ event เท่านั้น** — ห้าม hardcode การประทับผลรายท่อ ห้ามคำนวณมูลค่าเอง (ENG-CSQ-02 ทำ)
> ⛔ **ห้ามประกาศซ้ำท่อที่มาอัตโนมัติ** (register จะถูก reject 422):
> - **OC** — เจ้าของคือ Operation Process (`sow.*`) เท่านั้น → **ไม่ประกาศ**
> - **DC ระดับเอกสาร** — DOA engine ยิงให้ตอนอนุมัติ/ตีกลับแล้ว → **ไม่ประกาศ**
> - **SC** — สงวนไว้ `trigger = false` เสมอ → **ไม่ประกาศ**

---

## 1. Identity

| ช่อง | ค่า |
|---|---|
| profile key | `CSQ-WH-STKADJ` |
| feature_id | `F-WH-STKADJ` (fid F082) |
| ชื่อ | Stock Adjustment — ใบปรับยอดสต๊อก |
| module | Warehouse (WH) |
| register status | `pending` |

---

## 2. Event ที่ประกาศ (เฉพาะ transition ที่ "จบแล้วมีผล")

> ❌ ไม่ประกาศ `ร่าง → รออนุมัติ` — ยังไม่มีผลทางธุรกิจ (สต๊อกยังไม่ขยับ)
> ❌ ไม่ประกาศ `รออนุมัติ → อนุมัติแล้ว` / การตีกลับ — **DC ระดับเอกสาร** DOA engine เป็นเจ้าของ

| # | event_id | Trigger (อ้าง PREBRIEF) | ท่อที่กระทบ | kind / basis | เงื่อนไข |
|---|---|---|---|---|---|
| 1 | `adj_posted_increase` | `อนุมัติแล้ว → ผ่านรายการ` เฉพาะ**ส่วนที่ผลต่างเป็น +** (§5.1 · S-01/S-17 · BR-16) | **EC** (มูลค่าคงคลังเพิ่ม) | `actual` · `basis: computed` จาก `Σ (ผลต่าง+ × ต้นทุนอ้างอิง)` | ทุกใบที่ post สำเร็จและมีบรรทัดผลต่าง + · **ของเพิ่มขึ้นโดยไม่มีการซื้อ** = จุดที่ต้องตามรอย |
| 2 | `adj_posted_decrease` | `อนุมัติแล้ว → ผ่านรายการ` เฉพาะ**ส่วนที่ผลต่างเป็น −** (§5.1 · S-02/S-17) | **EC** (มูลค่าคงคลังลด) | `actual` · `basis: computed` จาก `Σ \|ผลต่าง− × ต้นทุนอ้างอิง\|` | **ผลขาดทุนจริงของกิจการ** — ของหาย/เสียหาย |
| 3 | `adj_writeoff_posted` | `อนุมัติแล้ว → ผ่านรายการ` เฉพาะ **ประเภท = ตัดจำหน่ายของเสีย** (§3.1 · S-19) | **EC** | `actual` · `basis: computed` | แยกจาก event 2 เพราะ **เหตุคนละอย่าง** (ตัดจำหน่ายตั้งใจ vs ยอดคลาดเคลื่อน) — ให้ Engine จัดกลุ่มผลกระทบได้ถูก |
| 4 | `adj_reversed` | `ผ่านรายการ → กลับรายการแล้ว` (§5.1 · S-10 · BR-17) | **EC** | `avoided` → หักผลของ event 1/2/3 ออก | เฉพาะใบที่เคย `ผ่านรายการ` · movement ทิศตรงข้าม (append-only ไม่ลบของเดิม) |
| 5 | `adj_cancelled` | `ร่าง/รออนุมัติ/อนุมัติแล้ว → ยกเลิก` (§5.1 · S-09) | — **no-effect** | — | **ประกาศเป็น no-effect โดยเจตนา** — สต๊อกไม่เคยขยับ ไม่มีท่อไหนถูกกระทบ (บันทึกไว้กันคนมาเติมท่อทีหลัง) |

---

## 3. ท่อที่ **ไม่** ประกาศ + เหตุผล (ต้องเขียนชัด กันประกาศซ้ำ)

| ท่อ | ประกาศไหม | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ ไม่ | เจ้าของคือ Operation Process (`sow.*`) — StockAdj ไม่ใช่ต้นทาง OC |
| **DC** (Decision) | ❌ ไม่ | การอนุมัติ/ตีกลับใบปรับยอด = **DC ระดับเอกสาร** ที่ DOA engine ยิงเองแล้ว · StockAdj ไม่มี terminal decision (Continue/Adjust/Hold/Stop) นอกเหนือการเซ็นอนุมัติ |
| **SC** | ❌ ไม่ | สงวนไว้ `trigger = false` เสมอ |
| **SecC** (Security) | ❌ ไม่ | StockAdj ไม่แก้ข้อมูลอ่อนไหว/สิทธิ์/นโยบาย · Location Master + Item Master เป็นของ feature อื่น (soft-ref อ่านอย่างเดียว) `[AI-DRAFT]` — ดู CSQ-Q4 |
| **AC** (Accounting) | ❌ ไม่ | **StockAdj ไม่ post บัญชีเองในรอบนี้** — รายการบัญชีจริง (JE ปรับปรุงสินค้าคงเหลือ / ผลขาดทุนสินค้าสูญหาย) เกิดฝั่ง **GL ใน W5** · รอบนี้ mock + `TODO: JE posting` (PREBRIEF BR-19) · เมื่อ W5 มาแล้วให้ **GL เป็นเจ้าของท่อ AC** กันนับซ้ำ (`CSQ-Q2`) |
| **FC** (Financial/เงินสด-งบ) | ❌ ไม่ | การปรับยอดสต๊อก **ไม่กระทบเงินสดและไม่กิน commit งบ** — ไม่มีการจ่าย ไม่มีภาระผูกพันใหม่ · ต่างจาก RTV ที่มีสิทธิเรียกเครดิตจากผู้ขาย `[AI-DRAFT]` |

---

## 4. Payload contract (field ที่ต้องมีจริงใน entity — ตรวจกับ PREBRIEF §3)

| field | ที่มา | หมายเหตุ |
|---|---|---|
| `ref` = `adj_id` | header | soft-reference ทุก event |
| `adj_no` | doccfg `ADJ-YYYY-NNNN` (§3.1) | ปี **ค.ศ.** |
| `warehouse_ref` | §3.1 (soft-ref LD-4C-02) | 1 ใบ = 1 คลัง (BR-04) |
| `adjustment_type` | §3.1 `ปรับยอดทั่วไป / ตัดจำหน่ายของเสีย / ปรับยอดกักกัน` | ใช้แยก event 3 |
| **`abs_adjustment_amount`** | §3.3 `Σ \|มูลค่าต่อบรรทัด\|` | **ตัวเดียวกับฐาน DOA** |
| `net_adjustment_amount` | §3.3 มูลค่าสุทธิ | ให้ Engine เลือกฐานได้ |
| `increase_amount` · `decrease_amount` | แยกตามทิศของผลต่าง (§3.3) | ฐานของ event 1 / 2 |
| `lines[]` | §3.2 ต่อบรรทัด: `{bin_ref, location_type, item_ref, uom, system_qty_snapshot, correct_qty, delta_qty, unit_cost_ref, line_amount, reason_code}` | ให้ Engine ผูกกับสินค้า/สถานที่/เหตุผล |
| `reason_code[]` | §3.2 · master เหตุผล §8 (`RS-01`..`RS-99`) | ใช้จัดกลุ่มผลกระทบ (ของหาย vs ตัดจำหน่าย vs บันทึกขาด) |
| `reason_gl_account_mock[]` | master เหตุผล §8 คอลัมน์บัญชีปลายทาง (**mock**) | เตรียมให้ W5 — รอบนี้ยังไม่ post (gap G-05) |
| `cost_center_ref` | §3.1 (soft-ref) | nullable |
| `reversal_of_adj_id` / `reversed_by_adj_id` | §3.1 soft link | เฉพาะ event 4 |
| `attachment_count` | §3.1 | เฉพาะ event 3 (หลักฐานบังคับ BR-23) |
| `occurred_at` · `actor` | ระบบ | timestamp **ค.ศ.** ทุก event |

> ⚠️ ทุกค่ามูลค่าเป็น `basis: computed` จาก field ที่มีจริงในใบ — **feature ห้ามตีมูลค่าเพิ่มเอง** ENG-CSQ-02 เป็นคนประเมิน
> ⚠️ **`unit_cost_ref` รอบนี้เป็น mock จาก Item Master** (`[ASSUMED contract]` · gap G-01) — ต้นทุนจริง (FIFO/เฉลี่ย) เป็นของ **Inventory Valuation (W5)** → เมื่อ engine จริงมา ต้อง re-basis (`CSQ-Q3`)

---

## 5. HTML/FRD Injection note

- HTML **ไม่ต้องวาด UI ประเมินผลกระทบ** — Engine เป็นคนประทับ · feature แค่รู้ว่า emit ตอนไหน
- จุด emit = transition ตาม §2 เท่านั้น (ตรงกับ state machine PREBRIEF §5.1)
- ในโค้ด Phase A ใส่เป็น mock + marker **`FWD-WIRE: ENG-CSQ emit`** ที่ transition ที่เกี่ยว (ใน .md ใช้ `TODO: ENG-CSQ emit` ตามปกติ · _RUNNER_BRIEF §2.11)
- FRD Phase B: `05_RULES.md` เพิ่มหัวข้อ "ผลกระทบ 7C" ชี้มาที่ไฟล์นี้

---

## 6. Open Questions

| # | ประเด็น | ใครตอบ |
|---|---|---|
| CSQ-Q1 | แยก `adj_posted_increase` / `adj_posted_decrease` เป็น 2 event ถูกไหม หรือควรเป็น 1 event ที่ส่งทั้ง `increase_amount` + `decrease_amount` ให้ Engine แยกเอง | เจ้าของ F-CSQ-01 |
| CSQ-Q2 | เมื่อ W5 (GL/JE) มาแล้ว ท่อ **AC** จะยิงจาก StockAdj หรือจาก GL — **กันนับซ้ำ** | เจ้าของ F-CSQ-01 + เจ้าของ GL (W5) |
| CSQ-Q3 | มูลค่าที่ใช้ตีของควรเป็นต้นทุนอ้างอิงจาก Item Master (รอบนี้) หรือ **ต้นทุนเฉลี่ย/FIFO** จาก Inventory Valuation (W5) | เจ้าของ Valuation (W5) + F-CSQ-01 |
| CSQ-Q4 | การปรับยอดที่ `quarantine` / `damage` ควรถือเป็น **SecC** ด้วยไหม (เป็นจุดเสี่ยงทุจริต) — รอบนี้ **ไม่ประกาศ** SecC | เจ้าของ F-CSQ-01 + ผู้ตรวจสอบภายใน |
| CSQ-Q5 | `adj_cancelled` ประกาศเป็น no-effect — ต้อง register แถวเปล่าไว้ หรือไม่ต้องส่งเข้า registry เลย | เจ้าของ F-CSQ-01 |
