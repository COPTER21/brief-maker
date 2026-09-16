# CSQ_BRIEF — F-WH-STKADJ · Stock Adjustment (ใบปรับยอดสต๊อก · F082)

> ใบประกาศ 7C Consequence → **ENG-CSQ (F-CSQ-01 Consequence Engine)** · deploy pipeline อ่านไฟล์นี้แล้ว `POST /csq/profiles/register` (auto-register)
> feature **ประกาศ event เท่านั้น** — ห้าม hardcode การประทับผลรายท่อ · ห้ามคำนวณมูลค่าเอง (ENG-CSQ-02 เป็นเจ้าของการตีมูลค่า)
> ⛔ **ห้ามประกาศซ้ำท่อที่มาอัตโนมัติ** (register จะถูก reject **422**):
> - **OC** (Operation) — เจ้าของคือ Operation Process (`sow.*`) → **ไม่ประกาศ**
> - **DC ระดับเอกสาร** (การอนุมัติ/ตีกลับ/ยกเลิกใบ) — DOA engine ยิงให้แล้ว → **ไม่ประกาศ**
> - **SC** — สงวนไว้ `trigger = false` เสมอ (OQ-C3 ยังไม่เคาะ) → **ไม่ประกาศ**
>
> Companion skill: `csq-declaration` (Sync Read F-CSQ-01) · ตระกูล declaration: `doa` ⚖ · `ntf` 🔔 · `doccfg` # · **`csq` ◆**

---

## 1. Identity

| ช่อง | ค่า |
|---|---|
| profile key | `CSQ-WH-STKADJ` |
| feature_id | `F-WH-STKADJ` (fid **F082**) |
| ชื่อ | Stock Adjustment — ใบปรับยอดสต๊อก |
| module | Warehouse (WH) |
| กลุ่ม backfill | A (feature ที่ทำ FRD/HTML แล้ว · มี event หลายแบบ — เจาะรายตัวจาก state machine) |
| register status | `pending` |
| version | v1.0 (2026-09-16) |

---

## 2. Declared Events — เฉพาะ transition ที่ "จบแล้วมีผลทางธุรกิจ"

> Trigger point อ้าง **FRD จริง**: `03_LOGIC §3.1` (Function ที่ emit) + `05_RULES` state-transition table (Scenario S-xx / BR-xx)
> ❌ ไม่ประกาศ `draft → pending` (ส่งอนุมัติ · S-07) — สต๊อกยังไม่ขยับ ยังไม่มีผลทางธุรกิจ
> ❌ ไม่ประกาศ `pending → approved` / `pending → draft` (อนุมัติ/ตีกลับ · S-08/S-11/S-12) — **DC ระดับเอกสาร** DOA engine เป็นเจ้าของ

| # | event_id | Trigger point (FRD) | ท่อที่ยิง | kind · basis | เงื่อนไข |
|---|---|---|---|---|---|
| 1 | `adj_posted_increase` | `approved → posted` (`03_LOGIC` **FN-13 `postDocument`** — "emit … CSQ EC" · `05_RULES` S-07/S-17 · BR-16) — **เฉพาะบรรทัดที่ `delta_qty > 0`** | **EC** (มูลค่าคงคลัง**เพิ่ม**) | `actual` · `basis: computed` จาก `Σ line_amount (delta_qty>0)` | ทุกใบที่ post สำเร็จและมีบรรทัดผลต่าง + · **ของเพิ่มโดยไม่มีการซื้อ** = จุดที่ Engine ต้องตามรอย |
| 2 | `adj_posted_decrease` | `approved → posted` (**FN-13 `postDocument`** · S-07/S-17 · BR-16) — **เฉพาะบรรทัดที่ `delta_qty < 0`** | **EC** (มูลค่าคงคลัง**ลด**) | `actual` · `basis: computed` จาก `Σ \|line_amount\| (delta_qty<0)` | **ผลขาดทุนจริงของกิจการ** — ของหาย/เสียหาย/บันทึกขาด |
| 3 | `adj_writeoff_posted` | `approved → posted` (**FN-13 `postDocument`** · S-17) — **เฉพาะ `adjustment_type = 'damage'`** (ตัดจำหน่ายของเสีย) | **EC** | `actual` · `basis: computed` จาก `Σ \|line_amount\|` ของใบ | แยกจาก event 2 เพราะ **เหตุคนละอย่าง** (ตัดจำหน่ายตั้งใจ · หลักฐานบังคับ BR-23 vs ยอดคลาดเคลื่อน) — ให้ Engine จัดกลุ่มผลกระทบถูก |
| 4 | `adj_reversed` | ใบกลับรายการ post → ต้นฉบับ `posted → reversed` (**FN-14 `reverseDocument`** สร้างใบ → **FN-13 `postDocument`** ของใบ `is_reversal_doc=true` · `05_RULES` S-10 · BR-17/17.1/18) | **EC** | `avoided` · `basis: computed` — **หักผลของ event 1/2/3 ออก** | เฉพาะใบที่เคย `posted` · movement ทิศตรงข้าม (append-only ไม่ลบของเดิม) · envelope ต้องมี `reversal_of` (BR-CSQ-04) |
| 5 | `adj_cancelled` | `draft/pending → cancelled` (**FN-11 `cancelDocument`** — "emit adj_cancelled(NTF) + **CSQ no-effect**" · `05_RULES` S-09 · BR-27) | — **no-effect** | — | **ประกาศเป็น no-effect โดยเจตนา** — `approved` ยกเลิกไม่ได้ (BR-27) · สต๊อกไม่เคยขยับ ไม่มีท่อถูกกระทบ (บันทึกไว้กันคนมาเติมท่อทีหลัง) |

> **หมายเหตุ event 4:** ผลกระทบจริง (movement ทิศตรงข้าม) เกิด **เมื่อใบกลับรายการ post** (FN-13) ไม่ใช่ตอนกดริเริ่มกลับรายการ (FN-14) — BR-17.1. จุด emit = post ของใบ `is_reversal_doc=true`.

---

## 3. ท่อที่ **ไม่** ประกาศ + เหตุผล (เขียนชัดเพื่อกันประกาศซ้ำ → กัน reject 422)

| ท่อ | ประกาศไหม | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ ไม่ | เจ้าของคือ Operation Process (`sow.*`) — StockAdj ไม่ใช่ต้นทาง OC (**G1** enforce) |
| **DC** (Decision/Document) | ❌ ไม่ | การอนุมัติ (FN-09) / ตีกลับ (FN-10) / ยกเลิกใบ (FN-11) = **DC ระดับเอกสาร** ที่ DOA engine ยิงเองแล้ว · StockAdj **ไม่มี terminal decision** (Continue/Adjust/Hold/Stop) นอกเหนือการเซ็นอนุมัติ (**G2** enforce) |
| **SC** | ❌ ไม่ | สงวนไว้ `trigger = false` เสมอ (**G3** enforce) |
| **SecC** (Security) | ❌ ไม่ *(รอบนี้)* | StockAdj ไม่แก้ข้อมูลอ่อนไหว/สิทธิ์/นโยบาย · Location/Item Master เป็น soft-ref **อ่านอย่างเดียว** (LOCK-07 · `04_DB §4.1`) · ไม่มี field ระดับ **Restricted** (`04_DB §4.2/§4.6.2`) `[AI-DRAFT]` → ดู **CSQ-Q4** (quarantine/damage เป็นจุดเสี่ยงทุจริต — ผู้ตรวจสอบภายในต้องเคาะ) |
| **AC** (Accounting) | ❌ ไม่ *(รอบนี้)* | **StockAdj ไม่ post บัญชีเองในรอบนี้** — `je_status='รอลงบัญชี'` + marker `FWD-WIRE: JE posting` (BR-19 · `05_RULES`) · JE จริง (ปรับปรุงสินค้าคงเหลือ/ผลขาดทุนสินค้าสูญหาย) เกิดฝั่ง **GL ใน W5** · เมื่อ W5 มา ให้ **GL เป็นเจ้าของท่อ AC** กันนับซ้ำ → **CSQ-Q2** |
| **FC** (Financial/เงินสด-งบ) | ❌ ไม่ | การปรับยอดสต๊อก **ไม่กระทบเงินสด ไม่กิน commit งบ** — ไม่มีการจ่าย ไม่มีภาระผูกพันใหม่ (ต่างจาก RTV ที่มีสิทธิเรียกเครดิตจากผู้ขาย) `[AI-DRAFT]` |

---

## 4. Payload Contract (Event Envelope → `POST /csq/events`)

> ทุก field ต้องมีจริงใน `04_DB` (**G5**) · ค่ามูลค่าเป็น `basis: computed` จาก field ที่มีในใบ — **feature ห้ามตีมูลค่าเพิ่มเอง** ENG-CSQ-02 เป็นคนประเมิน (BR-CSQ-01)
> field ที่ระบบคำนวณจาก field จริง (ไม่ได้เก็บเป็นคอลัมน์) ติดป้าย **`[DERIVED — ไม่เก็บ]`** — ให้ Engine คำนวณจาก `lines[]` เอง ห้ามสร้างคอลัมน์ผลใน table ของ feature (BR-CSQ อิรอนรูล)

| field | ที่มา (04_DB) | Classification | หมายเหตุ |
|---|---|---|---|
| `ref` = `id` (adj_id) | `T_stock_adjustment.id` | Internal | soft-reference ทุก event |
| `adj_no` | `T_stock_adjustment.adj_no` | Internal | `ADJ-YYYY-NNNN` (ปี **ค.ศ.** · doccfg BR-21) |
| `warehouse_ref` | `T_stock_adjustment.warehouse_ref` | Internal | 1 ใบ = 1 คลัง (BR-04) |
| `adjustment_type` | `T_stock_adjustment.adjustment_type` | Internal | enum `general/damage/quarantine` — **ใช้แยก event 3** (`damage`) |
| `abs_adjustment_amount` | `T_stock_adjustment.abs_adjustment_amount` | **Confidential** (D5) | `Σ\|line_amount\|` · **ตัวเดียวกับฐาน DOA** (BR-09) · frozen at submit |
| `net_adjustment_amount` | `T_stock_adjustment.net_adjustment_amount` | **Confidential** | `Σ line_amount` (มีเครื่องหมาย) · ให้ Engine เลือกฐานได้ |
| `increase_amount` | `[DERIVED — ไม่เก็บ]` จาก `Σ line_amount (delta_qty>0)` | Confidential | ฐานของ event 1 — Engine คำนวณจาก `lines[]` |
| `decrease_amount` | `[DERIVED — ไม่เก็บ]` จาก `Σ\|line_amount\| (delta_qty<0)` | Confidential | ฐานของ event 2 — Engine คำนวณจาก `lines[]` |
| `lines[]` | `T_stock_adjustment_line`: `{bin_ref, location_type, item_ref, uom, system_qty_snapshot, correct_qty, delta_qty, unit_cost_ref, line_amount, reason_code, reason_note}` | line: มูลค่า = Confidential | ให้ Engine ผูกกับสินค้า/สถานที่/เหตุผล + คำนวณ increase/decrease/write-off |
| `reason_code[]` | `T_stock_adjustment_line.reason_code` → master `T_adj_reason` (RS-01..RS-99) | Internal | จัดกลุ่มผลกระทบ (ของหาย vs ตัดจำหน่าย vs บันทึกขาด) |
| `reason_gl_account_mock[]` | `T_adj_reason.gl_account_mock` | Internal | บัญชีปลายทาง **mock** — เตรียมให้ W5 (gap G-05) · รอบนี้ยังไม่ post |
| `cost_center_ref` | `T_stock_adjustment.cost_center_ref` | Internal | nullable · ใช้ตอน JE (W5) |
| `reversal_of` | `T_stock_adjustment.reversal_of` | Internal | เฉพาะ event 4 — envelope `reversal_of` (BR-CSQ-04 · BR-18) |
| `reversed_by_doc` | `T_stock_adjustment.reversed_by_doc` | Internal | soft link 2 ทาง (BR-17.1/18) |
| `attachment_count` | `[DERIVED — ไม่เก็บ]` COUNT(`T_stock_adjustment_attachment`) | Internal | เฉพาะ event 3 (หลักฐานบังคับ ≥1 · BR-23) |
| `actor` | `T_inventory_movement.actor` (= header `posted_by`) | Confidential + **PII** | คนจริงที่ผ่านรายการ — **mask ก่อนส่ง** (BR-CSQ-03) |
| `occurred_at` | `T_inventory_movement.occurred_at` | Internal | timestamp **ค.ศ.** ทุก event |
| `idempotency_key` | ระบบสร้าง = unique(`feature, ref, action`) | — | กันยิงซ้ำตอน retry (BR-CSQ-02) |

> ⚠️ **`unit_cost_ref` รอบนี้เป็น mock จาก Item Master** (`04_DB §4.2` line table · `03_LOGIC` FN-04 · gap **G-01** · `FWD-WIRE: valuation engine`) — ต้นทุนจริง (FIFO/เฉลี่ย) เป็นของ **Inventory Valuation (W5)** → เมื่อ engine จริงมาต้อง **re-basis** (**CSQ-Q3**)
> ⚠️ **Restricted mask:** ไม่มี field ระดับ Restricted (`04_DB §4.6`) · PII (person fields) ต้อง mask ที่ producer ก่อนส่ง — ส่งเข้า envelope เฉพาะ `actor` id ไม่ส่งชื่อ/`*_name_snap` ดิบ (BR-CSQ-03)

---

## 5. Register Checklist (ก่อน deploy จะ register สำเร็จ)

- [ ] **G1–G3 pass** — ไม่มี event ใดประกาศ `oc` / `dc` (จากอนุมัติ) / `sc` *(ตรวจแล้ว — ดู §7)*
- [ ] `05_RULES` เพิ่มหัวข้อ **"ผลกระทบ 7C (CSQ)"** ชี้มาไฟล์นี้ + BR-CSQ-01..05 *(ปัจจุบัน `03_LOGIC` FN-11/13 emit แล้ว แต่ `05_RULES` ยังไม่มีหัวข้อ CSQ — ให้ frd-generator inject รอบถัดไป)*
- [ ] `02_API` ระบุ producer contract (event ที่ปล่อยออก) ตาม Envelope F-CSQ-01 §2.3 *(API-09 post · API-10 reverse)*
- [ ] dev wire `emit` ที่ transition จริง (FN-13 post · FN-11 cancel) + ใส่ `idempotency_key` + `reversal_of` (event 4)
- [ ] mask PII (`actor`) + ไม่ส่ง `unit_cost_ref`/มูลค่าดิบเป็น Restricted (ไม่มี Restricted รอบนี้)
- [ ] deploy → ตรวจแถวใน **Profile Registry** ของ 7C Engine เปลี่ยนเป็น **เชื่อมแล้ว** + Event Log ประทับถูกท่อ
- [ ] Open Questions CSQ-Q1..Q5 ได้คำตอบจากเจ้าของ F-CSQ-01 (บางข้อไม่บล็อก register — ดู §6)

---

## 6. Open Questions

| # | ประเด็น | ใครตอบ | บล็อก register? |
|---|---|---|---|
| CSQ-Q1 | แยก `adj_posted_increase` / `adj_posted_decrease` เป็น 2 event ถูกไหม หรือควรเป็น 1 event ที่ส่งทั้ง `increase_amount`+`decrease_amount` ให้ Engine แยกเอง | เจ้าของ F-CSQ-01 | ไม่ (ปรับ mapping ได้ภายหลัง) |
| CSQ-Q2 | เมื่อ W5 (GL/JE) มาแล้ว ท่อ **AC** จะยิงจาก StockAdj หรือจาก GL — **กันนับซ้ำ** | เจ้าของ F-CSQ-01 + เจ้าของ GL (W5) | ไม่ (AC ไม่ประกาศรอบนี้) |
| CSQ-Q3 | มูลค่าตีของควรใช้ต้นทุนอ้างอิงจาก Item Master (mock รอบนี้) หรือ **ต้นทุนเฉลี่ย/FIFO** จาก Inventory Valuation (W5) — re-basis | เจ้าของ Valuation (W5) + F-CSQ-01 | ไม่ (basis เปลี่ยนเป็น field ยังคงเดิม) |
| CSQ-Q4 | การปรับยอด `quarantine`/`damage` ควรถือเป็น **SecC** ด้วยไหม (จุดเสี่ยงทุจริต) — รอบนี้ **ไม่ประกาศ** SecC | เจ้าของ F-CSQ-01 + ผู้ตรวจสอบภายใน | ไม่ (เพิ่ม event ได้ภายหลัง) |
| CSQ-Q5 | `adj_cancelled` = no-effect — ต้อง register แถวเปล่าไว้ หรือไม่ต้องส่งเข้า registry เลย | เจ้าของ F-CSQ-01 | ไม่ |
| CSQ-Q6 | naming convention ของ `event_id` — ใช้ `adj_posted_increase` (ตามที่ `03_LOGIC` FN-13/FN-11 emit) ตรงกับ catalog F-CSQ-01 ไหม `[ASSUMED — csq-contract.md vocabulary ไม่มีในแพ็ก skill]` | เจ้าของ F-CSQ-01 | อาจ (ถ้า catalog ใช้ dotted-prefix `adj.posted`) |

---

## 7. Quality Gate Result (self-check ก่อนส่ง)

| # | เช็ค | ผล |
|---|---|---|
| G1 | ไม่มี event ประกาศ `oc` | ✅ PASS |
| G2 | ไม่มี event ประกาศ `dc` จากการอนุมัติ | ✅ PASS (อนุมัติ/ตีกลับ/ยกเลิก = DC เอกสาร DOA เจ้าของ) |
| G3 | ไม่มี event ประกาศ `sc` | ✅ PASS |
| G4 | ทุก event มี trigger point อ้าง FRD § | ✅ PASS (FN-13/FN-11/FN-14 + 05_RULES S-07/S-09/S-10/S-17 + BR-16/17/19/23/27) |
| G5 | ทุก payload field มีจริงใน 04_DB | ✅ PASS (field คำนวณติดป้าย `[DERIVED — ไม่เก็บ]` ให้ Engine คิดจาก `lines[]` — ไม่แต่งคอลัมน์ใหม่) |
| G6 | event EC ระบุ `kind` ครบ | ✅ PASS (event 1/2/3 `actual` · event 4 `avoided`) |
| G7 | EC จากเวลา/แรงงานไม่มี Rate Card → `basis: declared` | ✅ N/A (มูลค่าจาก unit_cost ไม่ใช่แรงงาน · mock cost = gap G-01 → CSQ-Q3) |
| G8 | ค่าที่ยังไม่ยืนยันติดป้าย | ✅ PASS (`[AI-DRAFT]` SecC/FC · `[ASSUMED]` naming · `[DERIVED]` fields) |
| G9 | `event_id` ไม่ชนความหมายซ้อน | ✅ PASS (ยึดคำที่ FRD FN-13/FN-11 emit — CSQ-Q6 ให้ F-CSQ-01 ยืนยัน convention) |

**VERDICT: ✅ PASS — พร้อม register (pending)** · G1–G3 (กฎที่ระบบ enforce จริง) ผ่านครบ · Open Questions CSQ-Q1..Q6 ไม่บล็อก register (ยกเว้น Q6 กรณี catalog ใช้ dotted-prefix)

---

## 8. HTML / FRD Injection note

- **HTML ไม่ต้องวาด UI ประเมินผลกระทบ 7 ท่อ** — Engine เป็นคนประทับ · feature แค่รู้ว่า emit ตอนไหน
- จุด emit = transition ตาม §2 เท่านั้น (post = FN-13 · cancel = FN-11) — ตรงกับ state machine `05_RULES` + `03_LOGIC §3.1`
- โค้ด Phase A ใส่ mock + marker **`FWD-WIRE: ENG-CSQ emit`** (ใน .md ใช้ `// TODO: ENG-CSQ emit — ดู CSQ_BRIEF_F-WH-STKADJ.md`) · **ห้าม** `const PIPES_HIT=[...]` ในไฟล์ feature
- FRD `05_RULES` ให้เพิ่มหัวข้อ **"ผลกระทบ 7C (CSQ)"** + BR-CSQ-01..05 ชี้มาไฟล์นี้ (รอบถัดไป) · `02_API` ระบุ producer contract (API-09/API-10)
