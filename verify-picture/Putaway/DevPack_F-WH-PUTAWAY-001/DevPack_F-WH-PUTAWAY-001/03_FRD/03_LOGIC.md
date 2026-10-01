# 03_LOGIC — F-WH-PUTAWAY · จัดเก็บเข้าที่

> ⚠️ **รหัส `FN-xx` ในไฟล์นี้เป็นคนละชุดกับ `FN-xx` ใน `FUNCTION_CHECKLIST`**
> ที่นี่ = **ฟังก์ชันชั้นโค้ด** (`F-WH-PUTAWAY-FN-01`…`-25`) · ที่โน่น = **ฟังก์ชันเชิงธุรกิจ** (44 ข้อ)
> ตาราง map อยู่ที่ `00_OVERVIEW` §0.12.5 — **อย่า rename ข้ามไฟล์**

> ชื่อฟังก์ชันในคอลัมน์ "ต้นแบบ" คือชื่อจริงใน `01_HTML/F-WH-PUTAWAY.html` (Sync Read) — ใช้เป็นสมอเวลาไล่โค้ด

---

## §3.1 Functions (Scope-Local)

### `F-WH-PUTAWAY-FN-01` · `buildPutawayQueue`
| | |
|---|---|
| หน้าที่ | สร้าง/รีเฟรชคิวงานค้างจัดเก็บจากใบรับของที่ `posted` **เฉพาะบรรทัดที่ผ่าน QC จำนวน > 0** |
| Input | `warehouseRef` · filter (queueKind · mineOnly · includeVoid · sort · q) |
| Output | `PutawayTask[]` |
| กติกา | R02 (แหล่งเดียวคือใบรับของ) · R03 (**1 งาน = 1 บรรทัด** ห้ามรวมข้ามใบ) · **DR-01 ไม่มีทางสร้างงานเอง** |
| ต้นแบบ | ชุด `TASKS` + `queueTasks()` |
| ระวัง | บรรทัดประเภทบริการ (ไม่มีของ) **ต้องไม่เข้าคิว** · ใบรับของสถานะร่างต้องไม่เข้าคิว |

### `F-WH-PUTAWAY-FN-02` · `computeTaskProgress`
`qtyDone = Σ(movement จัดเก็บ) − Σ(movement กลับรายการ)` · `qtyRemain = max(0, qtyRequired − qtyDone)`
**ค่าคำนวณล้วน ห้ามเก็บเป็นคอลัมน์ที่แก้มือได้** (DR-06) · ต้นแบบ: `remainOf()` · `t.done`

### `F-WH-PUTAWAY-FN-03` · `deriveTaskStatus`
```
GRN ต้นทางถูกกลับรายการ        → ถอนออก      (ทับทุกกรณี · R19)
qtyRemain = 0                  → จัดเก็บแล้ว
มีผู้ถือครอง                    → กำลังจัดเก็บ
อื่น ๆ                          → รอจัดเก็บ
```
ต้นแบบ: `t.status` + `confirmPutaway()` · **สถานะเป็นค่า derive ไม่ใช่ค่าที่ผู้ใช้ตั้งเอง** · ไม่มีสถานะ "ร่าง" และไม่มีสถานะอนุมัติ (LOCK-01/02)

### `F-WH-PUTAWAY-FN-04` · `computeTaskAge`
`ageHours = now − queuedAt` · `isAged = ageHours >= NC.aging_warn_hours`
**เกณฑ์อ่านจาก NC rules ตอนรัน** (R20 · CF-05 · `OQ-PUT-06`) — ต้นแบบ: `ageHours()` / `ageText()` / `NC.agingWarnHours`
> ยืนยันว่า config ถูกใช้จริง: `NC.agingWarnHours` ถูกอ่าน **4 จุด** (นับ KPI · ป้าย KPI · จุดสีในคิว · ช่องอายุงาน)

### `F-WH-PUTAWAY-FN-05` · `claimTask`
ตรวจ `holder` ว่าง หรือเป็นผู้เรียกเอง → ตั้ง `holder` + `กำลังจัดเก็บ` + audit `CLAIM`
ถ้าคนอื่นถืออยู่ → **ปฏิเสธ** + คืนชื่อผู้ถือ (R18) · ต้นแบบ: `claimTask()` บรรทัด 2834–2838

### `F-WH-PUTAWAY-FN-06` · `releaseTask`
`holder = null` · `กำลังจัดเก็บ → รอจัดเก็บ` · **ห้ามสร้าง movement** (R18) · audit `RELEASE`
ยืนยัน runtime: จำนวน movement **ไม่เปลี่ยน** ก่อน/หลังคืนงาน · ต้นแบบ: `releaseTask()`

### `F-WH-PUTAWAY-FN-07` · `forceReleaseTask`
**หัวหน้าคลังเท่านั้น** — ปลดงานจากมือคนอื่น + audit `FORCE_RELEASE` (บันทึกชื่อผู้ถูกปลด) · ต้นแบบ: `forceRelease()`

### `F-WH-PUTAWAY-FN-08` · `expireHeldTasks` ⚠️ **ยังไม่ implement**
| | |
|---|---|
| หน้าที่ | คืนงานเข้าคิวอัตโนมัติเมื่อถือครองเกิน `NC.soft_lock_minutes` (R18 วรรค 3 · `OQ-PUT-03` · CF-06) |
| สถานะในต้นแบบ | **ไม่มีโค้ด** — `NC.softLockMinutes = 30` ถูกประกาศแต่ **ไม่มีที่ไหนอ่านไปใช้** (grep = 1 ครั้ง คือบรรทัดที่ประกาศเอง) · ไม่มี `setInterval` |
| ทำที่ไหนตอนของจริง | **ฝั่งเซิร์ฟเวอร์** — scheduled sweep + lazy check ตอนอ่านคิว (`[AI-DEFAULT]` AD-06) · ไม่ใช่ timer ฝั่งจอ |
| ทำไมต้นแบบทำไม่ได้ | state อยู่ในหน่วยความจำและหายทุกครั้งที่โหลดหน้า — timer ฝั่งจอไม่มีความหมายเชิงพิสูจน์ |
| บันทึกที่ | `07_LOCKED` **LD-05** · `_COVERAGE_REPORT` §1.1 · `06_TESTS` AT-15 (blocked-by-prototype) |

> **ห้ามลบข้อนี้ออกจากสเปคเพราะต้นแบบไม่ได้ทำ** — เป็นวรรคหนึ่งของ R18 ที่ BRD อนุมัติแล้ว

### `F-WH-PUTAWAY-FN-09` · `suggestBins` → เรียก `ENG-PUT-SUGGEST`
Wrapper ที่ประกอบ context (งาน · ประเภทต้นทาง · หมวดสินค้า · คลัง) แล้วส่งเข้า engine · คืน ≤ 3 รายการ · ต้นแบบ: `suggestBins()` บรรทัด 2220–2259

### `F-WH-PUTAWAY-FN-10` · `filterEligibleBins` — **hard filter (ขั้นที่ 1)**

| # | กรองออกเมื่อ | กติกา | ต้นแบบ |
|---|---|---|---|
| **F-5** | คนละคลังกับต้นทาง | R25 | `if(b.wh !== t.wh) continue` |
| **F-1a** | ต้นทาง = กักกัน แต่ปลายทางไม่ใช่กักกัน | R04 · LOCK-06 | `if(srcType==='quarantine'){ if(b.type!=='quarantine') continue; }` |
| **F-1b** | ต้นทางปกติ แต่ปลายทางไม่ใช่ `เก็บปกติ` | R05 · LOCK-07 | `else if(b.type !== 'storage') continue` — **ตัด `ระหว่างทาง` · `ของเสีย` · `พักรับเข้า` · `กักกัน` ออกพร้อมกัน** |
| **F-1c** | ปลายทาง = ต้นทางเอง | — | `if(b.code === t.src) continue` |
| **F-2** | ช่องล็อก หรือโซนปิด | R08 | `if(b.locked \|\| (z && !z.open)) continue` |
| **F-3** | เต็ม (ความจุคงเหลือ ≤ 0) | R09 | `if(free !== null && free <= 0) continue` |
| **F-4** | ห้ามปนสินค้า และมีสินค้าตัวอื่นอยู่ | R07 · S-24 (PREBRIEF) | `if(!b.mixed && items.length>0 && !(items.length===1 && items[0].code===t.code)) continue` |

> **DR-02: ต้องกรองออกก่อนจัดอันดับเสมอ** — ช่องที่ถูกกรอง **ห้ามหลุดเข้ารายการแนะนำในทุกกรณี**
> ยืนยันเชิงกล: ไล่ 12 งาน × ทุกการ์ด = **29 คู่ · violation 0**

### `F-WH-PUTAWAY-FN-11` · `rankBins` — **จัดอันดับ (ขั้นที่ 2–3)**

| rank | เงื่อนไข | เหตุผลที่แสดง (verbatim) |
|---|---|---|
| **R1** | มีสินค้าตัวเดียวกันอยู่แล้ว และยังมีที่ว่าง | `มีสินค้าตัวเดียวกันอยู่แล้ว <N> <หน่วย>` |
| **R2** | โซนระบุหมวด และหมวดสินค้าตรง | `โซน <code> รับหมวด <หมวด>` |
| **R3** | โซนไม่จำกัดหมวด (รับทุกหมวด) | `โซน <code> รับได้ทุกหมวด` |
| **R4** | fallback — ว่างและใกล้จุดรับเข้าที่สุด | `ว่าง · ใกล้จุดรับเข้าที่สุด` |
| (กักกัน) | ต้นทางกักกัน | `ช่องกักกันที่ยังรับได้ (ของ QC ไม่ผ่านออกได้ทางใบคืนผู้ขายเท่านั้น)` |

**Tie-break (ขั้นที่ 3):** `rank` → `near` (ใกล้จุดรับเข้า) → **ความจุคงเหลือมากกว่าอยู่ก่อน** (ไม่จำกัด = มากสุด) → รหัสช่องเรียงตัวอักษร

**ขั้นที่ 4 — ไม่มีอะไรผ่านเลย:** คืน `[]` + สรุปเหตุที่ถูกกรอง → จอแสดงข้อความตรง ๆ + 2 ทางออก (R09)

> **R07 = CONFIGURABLE** — **ลำดับ/น้ำหนักอ่านจาก config ผังคลัง ห้าม hardcode** (CF-02 · `OQ-PUT-05`)
> **DR-03** ทุกรายการต้องมีเหตุผล — ยืนยัน: 29/29 คู่มี `why` ไม่ว่างและ `rank ∈ {1,2,3,4}`

### `F-WH-PUTAWAY-FN-12` · `searchBinsForOverride`
ค้นช่องเก็บด้วยรหัส/ชื่อโซน — ใช้ hard filter **เฉพาะ F-5 · F-1a · F-1b** (คลัง + ประเภท) แต่ **ยังคืนช่องที่ล็อก/เต็ม/ห้ามปน** พร้อมธง `selectable=false` + เหตุผล
เหตุผลที่ต่างจาก FN-10: **R10 override ได้เสมอ** (ยกเว้นข้อจำกัดของ R04/R05) · **R08 ค้นเจอได้แต่เลือกไม่ได้**
ต้นแบบ: `pickerOptions()` + `chooseBin()` (ปฏิเสธช่องล็อก + toast) · ยืนยัน: เลือกช่องล็อกแล้ว **ปลายทางไม่เปลี่ยน**

### `F-WH-PUTAWAY-FN-13` · `classifyViolation`
```
ความจุคงเหลือ ≠ ไม่จำกัด และ qty > ความจุคงเหลือ  → 'เกินความจุ'
ช่องอยู่ใน 3 อันดับที่แนะนำ                        → ''  (ไม่ฝืนเกณฑ์)
โซนระบุหมวด และหมวดสินค้าไม่ตรง                    → 'ข้ามหมวดโซน'
อื่น ๆ                                            → 'นอกรายการแนะนำ'
```
ต้นแบบ: `violationOf()` บรรทัด 2262–2273 · **ต้องตรวจซ้ำฝั่งเซิร์ฟเวอร์เสมอ** (DR-04)
> ลำดับสำคัญ: **ตรวจความจุก่อน** — ช่องที่แนะนำอันดับ 1 ก็ยังฝืนเกณฑ์ได้ถ้ากรอกจำนวนเกินความจุ

### `F-WH-PUTAWAY-FN-14` · `validateDestinations`
รวมทุกเหตุที่ยืนยันไม่ได้ **ไว้ในกล่องเดียว** (#43) ตามลำดับ: งานถูกถอน → ยังไม่รับงาน → ไม่มีปลายทาง → เกินยอดค้าง → รายแถว (ติดลบ · ขาดเหตุผล · ขาดข้อความเพิ่ม)
ต้นแบบ: `destIssues()` บรรทัด 2488–2504 · ข้อความ verbatim อยู่ที่ `01_UI` §1.11
> **ความจุเกินไม่อยู่ในรายการนี้** — R15 บอกว่าเป็น **คำเตือน ไม่ใช่การบล็อก** · ไปโผล่เป็นสีแถว + บังคับเหตุผลผ่าน FN-13 แทน

### `F-WH-PUTAWAY-FN-15` · `confirmPutaway`
ลำดับ: `validateDestinations` → (ผ่าน) → ต่อ `appendMovement` **1 แถวต่อ 1 ปลายทาง** → `recomputeBinStock` → `qtyDone += Σqty` → `deriveTaskStatus` → `pushAudit` → `emitCsqEvents` → คืน `nextTaskId`
ต้นแบบ: `confirmPutaway()` บรรทัด 2906–2936 (`state.busy` กันกดซ้ำ · VR14)
ยืนยัน runtime: 2 ปลายทาง 50+50 → **2 movement คนละ bin** · งานปิด · ยอด bin 60→160

### `F-WH-PUTAWAY-FN-16` · `appendMovement` → เรียก `ENG-INV-MOVE`
**เขียนอย่างเดียว ไม่มี update/delete** (LOCK-03 · DR-05) · ต้นแบบ: `MOVES.push()` (**`MOVES.splice/shift/pop` = 0 ทั้งไฟล์**)

### `F-WH-PUTAWAY-FN-17` · `recomputeBinStock`
`Bin_Stock(bin, item) = Σ movement เข้า − Σ movement ออก` — **ค่า derive ล้วน ไม่มีตารางที่แก้มือได้** (DR-06)
ปรับพร้อมกันทั้งสองฝั่ง: ปลายทาง `+qty` · ต้นทาง `−qty` · ต้นแบบ: `addStock()` + ลดยอดต้นทาง + `usedOf()` / `stockAt()` / `freeOf()`
> **ฐานที่ F-WH-STKADJ และ F-WH-STKTRF อ่านต่อ** (LOCK-08)

### `F-WH-PUTAWAY-FN-18` · `reversePutaway`
**หัวหน้าคลัง + เหตุผลบังคับ** → สร้าง movement `กลับรายการ` **ทิศกลับด้าน** + เขียนคู่ `reversalOf`/`reversedBy` **สองทางในทรานแซกชันเดียว** (DR-07) → `qtyDone -= qty` → งานกลับ `รอจัดเก็บ`
**ห้ามลบ ห้ามแก้รายการเดิม** (R16) · **กลับได้ครั้งเดียวต่อ 1 รายการ** (กัน EC-18 ยอดติดลบ)
ต้นแบบ: `askReverse()` / `doReverse()` บรรทัด 2959–2985
ยืนยัน runtime: กดโดยไม่ใส่เหตุผล → **ไม่เกิดรายการ** · ใส่แล้ว → รายการเดิมยังอยู่ · ผูกคู่สองทาง · ทิศกลับด้าน · ยอด bin 60→0

### `F-WH-PUTAWAY-FN-19` / `-20` · `lockBin` / `unlockBin`
ล็อก: เหตุผลบังคับ (VR12) → `binStatus = ล็อก` (ทับทุกสถานะ) → **หายจากรายการแนะนำทันที** แต่ยังค้นเจอ (R08)
ปลดล็อก: กลับเข้ารายการแนะนำ · ทั้งคู่ลง audit ต่อท้าย
ต้นแบบ: `doLockBin()` / `doUnlockBin()` · ยืนยัน: กดโดยไม่ใส่เหตุผล → **ไม่ล็อก** · ล็อกแล้วหายจาก `suggestBins()` ทุกงาน แต่ยังอยู่ใน `pickerOptions()`

### `F-WH-PUTAWAY-FN-21` · `withdrawTasksOnGrnReversal`
ใบรับของถูกกลับรายการ → งานที่ยัง `รอจัดเก็บ`/`กำลังจัดเก็บ` → `ถอนออก` + เหตุผล (R19)
**ไม่ลบงาน** — ยังค้นเจอผ่านตัวกรอง `รวมที่ถอนออก` · ยืนยัน: ซ่อน default (12 แถว) → เปิดตัวกรอง (13 แถว)

### `F-WH-PUTAWAY-FN-22` · `guardGrnReversal`
ตอบ GRN ว่ากลับรายการได้ไหม — `putawayDoneQty > 0` → **`canReverse = false`** (GRN BR-16 · OB-12)
กรณี "กลับรายการจัดเก็บครบแล้ว ใบรับของกลับมากลับรายการได้อีกไหม" → **ยังไม่เคาะ `OQ-PUT-04`** (คู่กับ `OQ-GRN-04`)
สถานะในต้นแบบ: **mock** · marker `FWD-WIRE: grn reversal guard`

### `F-WH-PUTAWAY-FN-23` · `computeKpi`
5 ค่า: งานค้าง · หน่วยที่รอเก็บ · ค้างเกินเกณฑ์ · งานในมือฉัน · **อัตราฝืนเกณฑ์ 7 วัน**
อัตราฝืนเกณฑ์ = `ปลายทางที่ฝืนเกณฑ์ ÷ ปลายทางทั้งหมด` (KPI-03 · M3) — **นับรายการ ไม่ใช่เงิน** (CSQ_BRIEF §6)
ต้นแบบ: `kpi()` · ยืนยัน: `{open:12, units:1014}` ตรงกับการนับมือจาก `TASKS` เป๊ะ

### `F-WH-PUTAWAY-FN-24` · `pushAudit`
เขียน `Putaway_Audit` **ต่อท้ายอย่างเดียว** (R21) ทุกการ: `CLAIM` · `RELEASE` · `FORCE_RELEASE` · `CONFIRM` (พร้อมปลายทาง/จำนวน/ที่มาการเลือก/เหตุผล) · `REVERSE` · `LOCK_BIN` · `UNLOCK_BIN`
**ไม่มี hard delete ที่ไหนเลย** — ยืนยัน: ไล่ทุกปุ่มใน 3 มุมมองด้วย regex `ลบ|delete|remove` = **0**

### `F-WH-PUTAWAY-FN-25` · `emitCsqEvents`
ประกาศ **2 event เท่านั้น** ตาม `CSQ_BRIEF §2`

| event | ยิงเมื่อ | payload สำคัญ |
|---|---|---|
| `putaway_forced_override` | ยืนยันจัดเก็บ · **เฉพาะแถวปลายทางที่ `violationKind ≠ null`** | `violation_kind` · `override_reason` · `selection_source` · `bin_capacity_remaining` · `qty` (**ไม่มีตัวเลขเงิน**) |
| `putaway_reversed` | กลับรายการจัดเก็บ | **`reversal_of` บังคับ** (BR-CSQ-04) · `reversal_reason` · `qty` |

**ห้าม:** `PIPES_HIT` · คอลัมน์ผลรายท่อในตารางของฟีเจอร์ · การคิดมูลค่าเป็นเงิน (ทั้งคู่ `basis: declared`)
**ห้ามประกาศ `putaway_confirmed`** — `grn_posted` เป็นเจ้าของมูลค่าก้อนเดียวกันแล้ว (`07_LOCKED` **LD-04** · `CSQ-Q1`)
ต้นแบบ: `emitCsq()` บรรทัด 2901–2905 — ยืนยันเชิงกล: ที่เรียกจริง = 2 ตัวนี้พอดี · `PIPES_HIT` = false · ตัวเลขเงิน = false

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### `ENG-PUT-SUGGEST` · `putaway-bin-suggestion-engine` 🆕

| | |
|---|---|
| ระดับ | **Scope-local engine** — เฉพาะ Putaway เท่านั้นที่เสนอช่องเก็บ |
| Input | `{ task, sourceLocationType, itemRef, itemCategory, warehouseRef, binCatalog, zoneCatalog, binStock, rankConfig }` |
| Output | `{ suggestions[≤3], filteredOutSummary[], zoneCategoryMatched }` |
| ขั้นตอน | FN-10 (hard filter) → FN-11 (rank + tie-break) → ตัด 3 อันดับแรก |
| **Iron rule ของ engine** | 1) **ไม่แตะ DB เอง** — รับ catalog + stock เป็น input · 2) **บริสุทธิ์ (pure)** ให้ input เดิมต้องได้ผลเดิม ทดสอบได้โดยไม่ต้องมีฐานข้อมูล · 3) **`rankConfig` มาจาก config ห้าม hardcode** (R07) · 4) **ทุก suggestion ต้องมี `reason` และ `rank`** (DR-03) · 5) **ห้ามคืนช่องที่ถูก hard filter ตัด** (DR-02) |
| ทำไมเป็น engine ไม่ใช่ฟังก์ชันธรรมดา | มี **decision table ที่เปลี่ยนได้จาก config** + ต้องทดสอบแยกจาก UI/API + เป็นจุดที่ M3 (อัตราฝืนเกณฑ์) วัดผลตรง |

### `ENG-INV-MOVE` · `inventory-movement-engine` 🆕 ★ **ของกลางระดับโมดูลคลัง**

| | |
|---|---|
| ระดับ | **Module-level reusable** — **F-WH-STKADJ และ F-WH-STKTRF ต้องใช้ตัวเดียวกันนี้** (LOCK-08) |
| หน้าที่ | บัญชีเดินสะพัดของการเคลื่อนไหวคลัง: `append(movement)` · `reverse(movementId, reason, actor)` · `projectBinStock()` |
| **Iron rule ของ engine** | 1) **append-only** — ไม่มี `update` ไม่มี `delete` ไม่มี endpoint ให้เรียก (LOCK-03 · DR-05) · 2) **reversal เขียนคู่สองทางในทรานแซกชันเดียว** (DR-07) · 3) **กลับรายการได้ครั้งเดียวต่อ 1 รายการ** · 4) **`Bin_Stock` เป็น projection** ห้ามมีตารางยอดที่แก้ตรง ๆ (DR-06) · 5) **ห้ามเขียน location ประเภท `ระหว่างทาง` / `ของเสีย` จากฝั่ง Putaway** (R05 · LOCK-07) — engine ต้องบังคับตาม caller feature |
| ทำไมเป็น module-level | ทั้ง 3 ฟีเจอร์ในคลื่นเขียนบัญชีเดียวกัน — ถ้าแยกกันเขียน **ยอดจะไม่ตรงกันทั้งโมดูล** (BRD §2.1 ปัญหาข้อสุดท้าย · §16.4 ความเสี่ยงข้อสุดท้าย) |

### `ENG-CSQ` · 7C consequence engine *(ของกลาง — F-CSQ-01)*
ฟีเจอร์ **ประกาศ event เท่านั้น** · engine เป็นคนประทับผลรายท่อและตีมูลค่า · **ห้ามฟีเจอร์คำนวณเอง**

### `NC-RULES` · configuration service *(ของกลาง)*
คืนค่า `aging_warn_hours` (CF-05) · `soft_lock_minutes` (CF-06) · `reversal_window_days` (CF-07)
**อ่านตอนรัน ห้าม compile ติดมา** (R20 DYNAMIC) — ค่าจริงทั้ง 3 ตัว **ยังรอเคาะ**

### ✗ engine ที่ **ไม่** ใช้ — และเหตุผล
`ENG-DOC-NUM` (ไม่มีเลขรัน · L3) · `ENG-DOC-STORE` (ไม่เก็บสำเนาเอกสาร) · `ENG-DOA` (ไม่มีสายอนุมัติ · LOCK-02) · `ENG-NOTIFY` (ไม่มีชิป `ntf`) · `thai-doc-pdf-generator` (ไม่มีใบพิมพ์)

---

## §3.3 Logic Placement Matrix

| ตรรกะ | วางที่ไหน | เหตุผล |
|---|---|---|
| กรอง + จัดอันดับช่องเก็บ | **`ENG-PUT-SUGGEST`** | decision table + config-driven + ต้องทดสอบแยก |
| ต่อท้าย movement + กลับรายการ + projection ยอด | **`ENG-INV-MOVE`** (module-level) | 3 ฟีเจอร์ใช้ร่วม — แยกกันเขียนแล้วยอดเพี้ยน |
| ตรวจความถูกต้องก่อนยืนยัน (FN-14) | **API layer (server)** | DR-04 ต้องตรวจซ้ำฝั่งเซิร์ฟเวอร์เสมอ แม้จอตรวจแล้ว |
| จัดคิว + เรียง + aging | **API layer** | ขึ้นกับ query + config ไม่ใช่ decision table |
| soft-lock timeout (FN-08) | **Server scheduler** | `[AI-DEFAULT]` AD-06 — จอทำไม่ได้ |
| แสดงผล/microcopy/สีสถานะ | **UI layer** | `01_UI` |
| เกณฑ์เวลา/ตัวเลขทั้งหมด | **NC rules / config** | R20 · **ห้ามอยู่ในโค้ดฟีเจอร์** |

---

## §3.4 API ↔ Logic Trace Table (R8 Anchor)

| API | Functions | Engines |
|---|---|---|
| API-01 `GET tasks` | FN-01, FN-02, FN-03, FN-04 | — |
| API-02 `GET tasks/{id}` | FN-02, FN-03, FN-04 | — |
| API-03 `claim` | FN-05, FN-24 | — |
| API-04 `release` | FN-06, FN-24 | — |
| API-05 `force-release` | FN-07, FN-24 | — |
| API-06 `suggested-bins` | FN-09, FN-10, FN-11 | **ENG-PUT-SUGGEST** |
| API-07 `bin-options` | FN-12 | — |
| **API-08 `confirm`** | FN-13, FN-14, FN-15, FN-16, FN-17, FN-02, FN-03, FN-24, FN-25 | **ENG-INV-MOVE**, ENG-CSQ |
| API-09 `bin-stock` | FN-17 | ENG-INV-MOVE |
| API-10 `zones` | FN-17 | ENG-INV-MOVE |
| API-11 `lock` | FN-19, FN-24 | — |
| API-12 `unlock` | FN-20, FN-24 | — |
| API-13 `movements` | — (อ่านตรง) | ENG-INV-MOVE |
| **API-14 `reverse`** | FN-18, FN-16, FN-17, FN-02, FN-03, FN-24, FN-25 | **ENG-INV-MOVE**, ENG-CSQ |
| API-15 `kpi` | FN-23, FN-04 | — |
| API-16 `grn-guard` | FN-22, FN-02 | — |
| **(scheduler)** | **FN-08** ⚠️ ยังไม่ implement | NC-RULES |
| **(event จาก GRN)** | FN-21, FN-03 | — |

### R8 verification

| เช็ค | ผล |
|---|---|
| ทุก function ถูกอ้างโดยอย่างน้อย 1 API หรือ trigger | ✅ **25/25** (FN-08 ผูกกับ scheduler · FN-21 ผูกกับ event จาก GRN) |
| ทุก API ผูกกับอย่างน้อย 1 function หรือ engine | ✅ **16/16** |
| function ที่ไม่มีใครเรียก (orphan) | ✅ **0** |
| API ที่ไม่มี logic รองรับ | ✅ **0** |
| engine ทุกตัวมี iron rule เขียนกำกับ | ✅ **2/2** (`ENG-PUT-SUGGEST` 5 ข้อ · `ENG-INV-MOVE` 5 ข้อ) |
| function ที่ประกาศแต่ **ยังไม่ implement** | ⚠️ **1 — FN-08** (`07_LOCKED` LD-05) |
