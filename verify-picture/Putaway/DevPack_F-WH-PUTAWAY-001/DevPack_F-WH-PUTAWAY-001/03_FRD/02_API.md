# 02_API — F-WH-PUTAWAY · จัดเก็บเข้าที่

> ชื่อ endpoint · รหัส error · กลไก concurrency = **`[AI-DEFAULT]`** (Lane Mode no-ask · ดู `00_OVERVIEW` §0.13 AD-01/02/04)
> **ไม่มี endpoint อนุมัติ · ไม่มี endpoint ออกเลขเอกสาร · ไม่มี endpoint พิมพ์/ลายเซ็น** — LOCK-01/02 · L3
> **ไม่มี endpoint update/delete บน movement** — LOCK-03 · DR-05

---

## §2.1 API Inventory

| # | Method + Path | ทำอะไร | Logic | สิทธิ์ |
|---|---|---|---|---|
| **API-01** | `GET /warehouse/putaway/tasks` | คิวงานค้างจัดเก็บ (+ filter/sort/paging) | FN-01, FN-02, FN-03, FN-04 | ดูคิว |
| **API-02** | `GET /warehouse/putaway/tasks/{taskId}` | รายละเอียดงาน 1 ชิ้น | FN-02, FN-03 | ดูคิว |
| **API-03** | `POST /warehouse/putaway/tasks/{taskId}/claim` | รับงานเข้ามือ (soft lock) | FN-05 | รับ/คืนงาน |
| **API-04** | `POST /warehouse/putaway/tasks/{taskId}/release` | คืนงานเข้าคิว | FN-06 | รับ/คืนงาน |
| **API-05** | `POST /warehouse/putaway/tasks/{taskId}/force-release` | **หัวหน้าคลัง** ปลดล็อกงานของคนอื่น | FN-07 | ปลดล็อกงาน |
| **API-06** | `GET /warehouse/putaway/tasks/{taskId}/suggested-bins` | ช่องเก็บที่แนะนำ + เหตุผล | FN-09 → `ENG-PUT-SUGGEST` | ดูคิว |
| **API-07** | `GET /warehouse/putaway/tasks/{taskId}/bin-options` | ค้นหาช่องเก็บเอง (override picker) | FN-12 | เลือก/override |
| **API-08** | `POST /warehouse/putaway/tasks/{taskId}/confirm` | **ยืนยันจัดเก็บ** → movement ต่อท้าย | FN-13, FN-14, FN-15, FN-16, FN-17, FN-24, FN-25 | ยืนยันจัดเก็บ |
| **API-09** | `GET /warehouse/bin-stock` | ยอดคงเหลือราย (bin, item) | FN-17 | ทุก role ที่ดูได้ |
| **API-10** | `GET /warehouse/zones` | ผัง คลัง › โซน › ช่องเก็บ + สถิติ | FN-17 | ทุก role ที่ดูได้ |
| **API-11** | `POST /warehouse/bins/{binCode}/lock` | ล็อกช่องเก็บ (เหตุผลบังคับ) | FN-19, FN-24 | ล็อก/ปลดล็อกช่อง |
| **API-12** | `POST /warehouse/bins/{binCode}/unlock` | ปลดล็อกช่องเก็บ | FN-20, FN-24 | ล็อก/ปลดล็อกช่อง |
| **API-13** | `GET /inventory/movements` | ประวัติการเคลื่อนไหว (+ filter) | — (อ่านตรง) | ดูประวัติ |
| **API-14** | `POST /inventory/movements/{movementId}/reverse` | **กลับรายการจัดเก็บ** | FN-18, FN-16, FN-17, FN-24, FN-25 | **กลับรายการ** |
| **API-15** | `GET /warehouse/putaway/kpi` | ตัวเลข 5 ตัวบนแถบบน | FN-23 | ดูคิว |
| **API-16** | `GET /warehouse/putaway/grn-guard/{grnRef}` | **GRN เรียกถาม** ว่ากลับรายการได้ไหม | FN-22 | ระบบต่อระบบ |

> **ไม่มีในรายการนี้โดยเจตนา:** `POST /tasks` (สร้างงานเอง — DR-01) · `PUT/DELETE /movements` (LOCK-03) · `PATCH /bin-stock` (DR-06) · endpoint ใด ๆ ที่เขียน location ประเภท `in-transit` / `damage` (R05)

---

## §2.2 API-01 · `GET /warehouse/putaway/tasks`

**Query**

| param | ชนิด | default | หมายเหตุ |
|---|---|---|---|
| `warehouseRef` | string | (ตามสิทธิ์) | `all` ได้เฉพาะหัวหน้าคลังขึ้นไป · **ห้ามคืน `WH-TRN`** (คลังเสมือน) |
| `queueKind` | `all` \| `normal` \| `quarantine` | `all` | คิวกักกันต้องแยกกลุ่มในผลลัพธ์ (R04) |
| `mineOnly` | bool | `false` | |
| `includeVoid` | bool | **`false`** | งาน `ถอนออก` **ซ่อนโดย default** (R19) |
| `sort` | `age` \| `queuedAt` \| `sourceZone` | **`age`** | `age` = ค้างนานสุดขึ้นก่อน (R20) |
| `q` | string | — | ค้นชื่อสินค้า · รหัสสินค้า · เลขใบรับของ |
| `page` / `size` | int | 1 / 50 | |

**Response 200** — แต่ละงานคืน: `taskId` · `taskVersion` · `grnRef` · `grnLineNo` · `itemRef` · `itemName` · `itemCategory` · `qtyRequired` · `qtyDone` · `qtyRemain` · `uomRef` · `sourceLocationRef` · `sourceLocationType` · `warehouseRef` · `queueKind` · `taskStatus` · `holder{ userRef, name, position, department }` · `queuedAt` (**ISO ค.ศ.**) · `ageHours` · `isAged` · `voidReason`

**กติกาบังคับ**
- คืนเฉพาะงานที่มาจากใบรับของสถานะ `posted` และบรรทัดที่ผ่าน QC จำนวน > 0 (R02) — บรรทัดบริการไม่เข้าคิว
- `isAged = ageHours >= NC.aging_warn_hours` — **ค่าเกณฑ์อ่านจาก NC rules ตอนรัน ห้าม compile ติดมา** (R20 · DR)
- `holder` ต้องเป็น **คนจริง** ครบ 3 ช่อง (R24) — ห้ามคืนรหัสบทบาท

---

## §2.3 API-03/04/05 · การถือครองงาน

### `POST .../claim`

| | |
|---|---|
| Body | `{ "taskVersion": 12 }` |
| สำเร็จ | `taskStatus = กำลังจัดเก็บ` · `holder = ผู้เรียก` · เขียน audit `CLAIM` |
| **409 `E-PUT-409-HELD`** | มีผู้ถือครองอยู่แล้วและไม่ใช่ผู้เรียก → คืน `holder` มาด้วยเพื่อให้จอแสดง `งานนี้ถูก <ชื่อ> ถือครองอยู่` (R18) |
| 409 `E-PUT-409-VERSION` | `taskVersion` ไม่ตรง (มีคนแก้ไปก่อน) |
| 422 `E-PUT-422-VOID` | งานถูกถอนออกแล้ว (R19) |

### `POST .../release`
คืนงาน — `holder = null` · `taskStatus = รอจัดเก็บ` · **ห้ามสร้าง movement ใด ๆ** (R18 · ยืนยัน runtime: `MOVES` ไม่เปลี่ยน) · audit `RELEASE`

### `POST .../force-release`
| | |
|---|---|
| สิทธิ์ | **หัวหน้าคลังเท่านั้น** |
| Body | `{ "taskVersion": 12 }` |
| ผล | `holder = null` · `taskStatus = รอจัดเก็บ` · audit `FORCE_RELEASE` พร้อมชื่อผู้ถูกปลด |
| 403 `E-PUT-403-ROLE` | ไม่ใช่หัวหน้าคลัง |

> **soft-lock timeout** (คืนคิวอัตโนมัติเมื่อหมดเวลา) **ไม่ได้ทำเป็น endpoint** — เป็นงานฝั่งเซิร์ฟเวอร์ (FN-08 · `[AI-DEFAULT]` AD-06) และ **ยังไม่ได้ implement ในต้นแบบ** → `07_LOCKED` **LD-05**

---

## §2.4 API-06 · `GET .../suggested-bins` — หัวใจของฟีเจอร์

**Response 200**

```
{ "suggestions": [
    { "binCode": "B-01-01-A", "zoneCode": "B", "zoneName": "วัสดุก่อสร้าง",
      "rank": 1, "rankLabel": "แนะนำ",
      "reason": "มีสินค้าตัวเดียวกันอยู่แล้ว 60 ท่อน",
      "capacityFree": 440, "capacityUnlimited": false,
      "currentItems": [ { "itemRef": "PVC-P4", "itemName": "ท่อ PVC 4\" ชั้น 8.5", "qty": 60 } ] } ],
  "filteredOutSummary": ["เต็ม", "ล็อก", "ห้ามปนสินค้า", "ผิดประเภท"],
  "zoneCategoryMatched": true }
```

**กติกาบังคับ (R06 · R07 · R09 · DR-02 · DR-03)**

| # | กติกา |
|---|---|
| A-01 | **คืนได้สูงสุด 3 รายการ** เรียงตาม rank แล้ว near แล้วความจุคงเหลือมากกว่า แล้วรหัส |
| A-02 | **ทุกรายการต้องมี `reason` ไม่ว่าง และ `rank ∈ {1,2,3,4}`** — ไม่มีเหตุผล = ห้ามส่งมา |
| A-03 | **ห้ามคืนช่องที่ถูก hard filter ตัดออก** ไม่ว่ากรณีใด (F-1…F-5 · `03_LOGIC` FN-10) — ตรวจซ้ำฝั่งเซิร์ฟเวอร์เสมอ |
| A-04 | ไม่มีของแนะนำ → `suggestions: []` + `filteredOutSummary` ระบุเหตุที่ถูกกรอง (ให้จอแสดงข้อความ + 2 ทางออก) |
| A-05 | `zoneCategoryMatched = false` → จอขึ้นป้ายเตือนให้ผู้ดูแลผังไปตั้งหมวดของโซน (S-18 BRD story) |
| A-06 | **ลำดับ/น้ำหนักเกณฑ์อ่านจาก config ผังคลัง** (R07 CONFIGURABLE · CF-02) — ห้าม hardcode ลำดับในโค้ด |

> ยืนยันเชิงกลบนต้นแบบ: ไล่ทุกงาน × ทุกการ์ด = **29 คู่ · violation 0** (`_COVERAGE_REPORT` §2 FN-07)

---

## §2.5 API-07 · `GET .../bin-options`

**Query:** `q` (รหัสช่อง/ชื่อโซน) · `page`/`size`

**Response:** `binCode` · `zoneCode` · `zoneName` · `locationType` · `acceptCategories` · `capacityFree` · `binStatus` · **`selectable`** (bool) · **`notSelectableReason`**

| กติกา | พฤติกรรม |
|---|---|
| R25 / F-5 | **ห้ามคืนช่องของคลังอื่น** — ยืนยัน: violation 0 ทุกงาน |
| R04 / F-1 | งานจากกักกัน → คืนเฉพาะ `locationType = กักกัน` — ยืนยัน: `pickerOptions()` ทุกงานกักกันเป็น `quarantine` 100% |
| R05 | **ห้ามคืน `ระหว่างทาง` / `ของเสีย`** เด็ดขาด — ยืนยัน: violation 0 |
| R08 | ช่องที่ล็อก **คืนมาได้** แต่ `selectable = false` + `notSelectableReason = <เหตุผลที่ล็อก>` — จอต้องแสดงจางและเลือกไม่ได้ (FN-25) |

---

## §2.6 API-08 · `POST .../confirm` — ยืนยันจัดเก็บ

**Body**

```
{ "taskVersion": 12,
  "actorRef": "u-anucha",
  "note": "",
  "destinations": [
    { "binRef": "B-01-01-A", "qty": 60, "selectionSource": "แนะนำอันดับ 1",
      "overrideReason": null, "overrideNote": null },
    { "binRef": "B-01-01-B", "qty": 40, "selectionSource": "เลือกเอง",
      "overrideReason": "ช่องเก็บที่แนะนำเต็ม", "overrideNote": null } ],
  "idempotencyKey": "F-WH-PUTAWAY|PT-0001|2026-09-14T09:12:00Z|confirm" }
```

**ลำดับตรวจฝั่งเซิร์ฟเวอร์ (ต้องตรวจทุกข้อ แม้จอตรวจมาแล้ว — DR-04)**

| ลำดับ | ตรวจ | error |
|---|---|---|
| 1 | `taskVersion` ตรง | `E-PUT-409-VERSION` |
| 2 | งานไม่ใช่ `ถอนออก` (R19 · VR10) | `E-PUT-422-VOID` |
| 3 | ผู้เรียกเป็นผู้ถือครอง (R24 · VR09) | `E-PUT-409-NOTHOLDER` |
| 4 | `actorRef` มีตัวตนและเป็นคนจริง (R24) | `E-PUT-422-ACTOR` |
| 5 | ทุก `binRef` อยู่คลังเดียวกับต้นทาง (R25 · VR06) | `E-PUT-422-CROSSWH` |
| 6 | ทุก `binRef` เข้ากันได้กับประเภทต้นทาง (R04/R05 · VR05) | `E-PUT-422-LOCTYPE` |
| 7 | ไม่มี `binRef` ที่ล็อก (R08 · VR04) | `E-WHBIN-422-BINLOCKED` |
| 8 | ทุก `qty ≥ 0` (VR01) | `E-PUT-422-QTYNEG` |
| 9 | มีอย่างน้อย 1 แถว `qty > 0` (R13 · VR03) | `E-PUT-422-QTYZERO` |
| 10 | `Σ qty ≤ qtyRemain` (R12 · VR02) | `E-PUT-422-QTYOVER` |
| 11 | ทุกแถวที่ `violationKind ≠ null` ต้องมี `overrideReason` (R11 · VR07) | `E-PUT-422-REASON` |
| 12 | `overrideReason = "อื่น ๆ"` ต้องมี `overrideNote` (VR08) | `E-PUT-422-REASONNOTE` |
| 13 | **ความจุเกิน = เตือน ไม่บล็อก** (R15 · VR13) — คืน `warnings[]` ไม่ใช่ error | — |

**ผลเมื่อสำเร็จ (ทรานแซกชันเดียว)**

1. สร้าง `Inv_Movement` **1 แถวต่อ 1 ปลายทาง** (kind = `จัดเก็บ`) — ยืนยัน runtime: 2 ปลายทาง → **2 movement คนละ bin**
2. อัปเดต projection `Bin_Stock` — ปลายทาง `+qty` · ต้นทาง `−qty` (ยืนยัน: `usedOf()` 60 → 160)
3. `qtyDone += Σ qty` → ถ้า `qtyRemain = 0` → `taskStatus = จัดเก็บแล้ว` · `holder = null`
4. เขียน `Putaway_Audit` (R21)
5. **ยิง `putaway_forced_override` เฉพาะแถวที่ `violationKind ≠ null`** (`05_RULES` §5.5)
6. คืน `nextTaskId` ให้จอเด้งไปงานถัดไป (S-01 BRD story · FN-08 checklist)

**Response 200:** `movements[]` · `task{ qtyDone, qtyRemain, taskStatus, taskVersion }` · `binStock[]` · `warnings[]` · `nextTaskId`

### Idempotency (DR-09 · AD-04)

`idempotencyKey` **unique ต่อ (feature, taskId, binRef, action)** — **ต้องมี `binRef` ในคีย์** เพราะ 1 งานเก็บได้หลายช่องในครั้งเดียว (BR-CSQ-02)
ยิงซ้ำด้วยคีย์เดิม → คืนผลเดิม **ไม่สร้าง movement ซ้ำ**

---

## §2.7 API-14 · `POST /inventory/movements/{movementId}/reverse` — กลับรายการ

| | |
|---|---|
| สิทธิ์ | **หัวหน้าคลังเท่านั้น** (R17) |
| Body | `{ "reason": "เก็บผิดช่อง — สลับกับล็อตของอีกใบ", "movementVersion": 1 }` |
| ตรวจ | เหตุผลบังคับ (VR11) · รายการต้อง `kind = จัดเก็บ` · **ยังไม่เคยถูกกลับรายการ** (`reversedBy` ว่าง) · ของยังไม่ถูกใช้ต่อ |
| ผล | สร้าง movement ใหม่ `kind = กลับรายการ` **ทิศกลับด้าน** · เขียนคู่ `reversalOf` / `reversedBy` **ทั้งสองทางในทรานแซกชันเดียว** (DR-07) · `qtyDone -= qty` · งานกลับ `รอจัดเก็บ` · ยิง `putaway_reversed` |
| **ห้าม** | **ห้ามลบ ห้ามแก้รายการเดิม** (R16 · LOCK-03) — ยืนยัน runtime: รายการเดิมยังอยู่ใน `MOVES` หลังกลับรายการ |

| error | เมื่อ |
|---|---|
| `E-INVMV-403-ROLE` | ไม่ใช่หัวหน้าคลัง |
| `E-INVMV-422-REASON` | ไม่มีเหตุผล |
| `E-INVMV-409-ALREADY` | ถูกกลับรายการไปแล้ว (กัน EC-18 ยอดติดลบ) |
| `E-INVMV-422-KIND` | รายการนี้ไม่ใช่ประเภท `จัดเก็บ` |
| `E-INVMV-409-CONSUMED` | ของถูกใช้ต่อไปแล้ว — **`[AI-DEFAULT]` ยังบังคับใช้ไม่ได้จนกว่า F-WH-STKTRF / F040 พร้อม** (`OQ-PUT-04` · EC-17) |

---

## §2.8 Cross-Module Contract (R12 — จาก BRD §12.1)

### 2.8.1 ← ใบรับของ (F-WH-GRN · F079 · ปิดแล้ว)

| ทิศ | สัญญา |
|---|---|
| **เข้า** | เมื่อใบรับของถูก `posted` → สร้างงาน putaway **1 งานต่อ 1 บรรทัดที่ผ่าน QC** (R03) พร้อม `grnRef` · `grnLineNo` · `itemRef` · `qtyRequired` (= จำนวนผ่าน QC) · `sourceLocationRef` · `uomRef` |
| **เข้า** | ใบรับของถูกกลับรายการ → งานที่ยัง `รอจัดเก็บ`/`กำลังจัดเก็บ` **ถูกถอนออกอัตโนมัติ** (FN-21 · R19) |
| **ออก (API-16)** | GRN เรียกถามก่อนกลับรายการ — คืน `{ canReverse, putawayDoneQty, blockingTasks[] }` · ถ้า `putawayDoneQty > 0` → `canReverse = false` (GRN BR-16 · FN-22) |
| สถานะปัจจุบันในต้นแบบ | **mock** — ปุ่มเปิดใบรับของยิง toast `เปิดใบรับของ <GRN> (จำลอง — อยู่คนละหน้าจอ)` · marker `FWD-WIRE: grn reversal guard` |

### 2.8.2 → ใบปรับยอดสต๊อก (F-WH-STKADJ · F082 · **ยังไม่มีจริง**)

| | |
|---|---|
| จุดเชื่อม | ปุ่ม `ปรับยอด` บนการ์ดช่องเก็บ (มุมมองผัง) |
| สัญญาที่ต้องส่ง | `binRef` · `warehouseRef` · `zoneRef` · ยอดคงเหลือปัจจุบันราย item |
| **ข้อผูกพัน (LOCK-08)** | F082 **ต้องอ่านสัญญา location + `Bin_Stock` ของ FRD ฉบับนี้ ห้ามสร้างโครงใหม่** · เป็นเจ้าของ `location_type = ของเสีย` |
| สถานะปัจจุบัน | **mock** — toast `ส่งต่อไปใบปรับยอดสต๊อกของช่อง <code> (จำลอง)` · marker `FWD-WIRE: stock-adjust handoff` |

### 2.8.3 → ใบย้ายสินค้า (F-WH-STKTRF · F083 · **ยังไม่มีจริง**)

| | |
|---|---|
| จุดเชื่อม | ปุ่ม `ย้ายสินค้า` บนการ์ดช่องเก็บ · และเป็น **ทางออกของ S-14 (PREBRIEF)** เมื่อเก็บผิดช่องแล้วของถูกใช้ต่อแล้ว |
| **ข้อผูกพัน (LOCK-07/08)** | F083 เป็น **เจ้าของ `location_type = ระหว่างทาง`** ที่ฟีเจอร์นี้ **จองไว้ให้แต่ไม่เขียน** · ต้องใช้ enum + ผังชุดเดียวกัน |
| สถานะปัจจุบัน | **mock** — toast `ส่งต่อไปใบย้ายสินค้าจากช่อง <code> (จำลอง)` · marker `FWD-WIRE: stock-transfer handoff` |

### 2.8.4 → ใบคืนผู้ขาย (F-PUR-RTV · F080 · ปิดแล้ว)

ของกักกันออกได้ทางเดียวคือคืนผู้ขาย (R04 · LOCK-06) · ปัจจุบัน **mock** — toast `ส่งของกักกันต่อไปใบคืนผู้ขาย (จำลอง)` · marker `FWD-WIRE: RTV handoff`

### 2.8.5 → 7C Consequence (ENG-CSQ · F-CSQ-01)

ประกาศ **2 event เท่านั้น** ผ่าน `CSQ_BRIEF_F-WH-PUTAWAY-001.md` — `putaway_forced_override` · `putaway_reversed`
**feature ประกาศเท่านั้น ห้ามประเมินผลรายท่อเอง ห้ามคิดมูลค่าเป็นเงิน** · ทั้งคู่เป็น `basis: declared` (qty-only)
ยืนยันเชิงกล: `emitCsq()` ที่เรียกจริงในซอร์ส = ทั้ง 2 ตัวนี้พอดี · `PIPES_HIT` ในไฟล์ = **false** · ตัวเลขเงินใน payload = **false**

### 2.8.6 → GL / การลงบัญชี (W5) — ✗ **ไม่มีเส้นในรอบนี้**

putaway = ย้ายภายในคลังเดียวกัน → **ไม่กระทบมูลค่ารวม** (R25 · OS-10) · ป้ายบนจอระบุชัด · marker `FWD-WIRE: JE posting`
กรณีข้ามเขตตีมูลค่ายังไม่เคาะ → `OQ-PUT-08` + `CSQ-Q3`

### 2.8.7 ✗ DOA · ENG-NOTIFY · F-DOCCFG · thai-doc-pdf-generator — **ไม่มีเส้นโดยเจตนา**

| | เหตุผล |
|---|---|
| **DOA** | ไม่มีสายอนุมัติเลย — งาน execution (LOCK-02 · LD-01) |
| **ENG-NOTIFY** | registry ไม่ติดชิป `ntf` รอบนี้ · ถ้าอนาคตต้องเตือนงานค้าง **ให้ประกาศที่ ENG-NOTIFY ห้าม hardcode ในฟีเจอร์** (LD-01) |
| **F-DOCCFG** | ไม่ใช่เอกสาร ไม่มีเลขรัน — `PT-<seq>` เป็นรหัสภายใน (L3 · LD-02) |
| **pdfdoc** | ไม่มีใบพิมพ์ (LD-01) |

---

## §2.9 Authorization Matrix (จาก BRD §4.2)

| API | จนท.คลัง | หัวหน้าคลัง | ผู้ดูแลผัง | QC | จัดซื้อ/บัญชี | ผู้ดูแลระบบ |
|---|---|---|---|---|---|---|
| API-01/02 คิว | ✅ คลังตัวเอง | ✅ ทุกคลัง | ✅ | ✅ **เฉพาะ `queueKind=quarantine`** | ⬜ | ✅ |
| API-03/04 รับ/คืนงาน | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| API-05 ปลดล็อกงาน | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| API-06/07 แนะนำ/ค้นช่อง | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| **API-08 ยืนยันจัดเก็บ** | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| API-09/10 ยอด + ผัง | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| API-11/12 ล็อก/ปลดล็อกช่อง | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ |
| API-13 ประวัติ | ✅ คลังตัวเอง | ✅ | ✅ | ⬜ | ✅ | ✅ |
| **API-14 กลับรายการ** | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| API-15 KPI | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ |
| API-16 GRN guard | ระบบต่อระบบ | | | | | |
| **ลบข้อมูลใด ๆ** | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ **ไม่มี endpoint** |

> **ไม่มี role ไหนมีสิทธิ์ลบ** — ไม่ใช่เพราะไม่ให้สิทธิ์ แต่เพราะ **ไม่มี endpoint ให้เรียก** (LOCK-03 · DR-05)
> เคสทดสอบสิทธิ์ครบทุกช่อง ⬜ ที่สำคัญอยู่ที่ `06_TESTS` §6.2

---

## §2.10 Concurrency & Idempotency `[AI-DEFAULT]` (AD-04)

| กรณี | กลไก |
|---|---|
| 2 คนกดรับงานพร้อมกัน | optimistic lock ด้วย `taskVersion` + ตรวจ `holder` → คนที่สองได้ `E-PUT-409-HELD` (R18) |
| 2 คนยืนยันงานเดียวกัน | `taskVersion` เปลี่ยนหลังคนแรกสำเร็จ → คนที่สองได้ `E-PUT-409-VERSION` |
| กดยืนยันซ้ำ (double-submit) | `idempotencyKey` + จอปิดปุ่ม + `กำลังบันทึก…` (VR14) |
| 2 คนเก็บลง bin เดียวกันจนเกินความจุ (EC-16) | ตรวจความจุอีกครั้งตอนบันทึก → **คืน `warnings[]` ไม่บล็อก** (R15) — ยัง `[AI-DEFAULT]` รอ `OQ-PUT-02` |
| กลับรายการซ้อน (EC-18) | `reversedBy` ไม่ว่าง → `E-INVMV-409-ALREADY` |
| อ่านยอด bin ขณะมีคนเขียน | `Bin_Stock` refresh ในทรานแซกชันเดียวกับ movement (AD-05) → อ่านได้ค่าล่าสุดเสมอ (SLA "ทันทีหลังยืนยัน") |

---

## §2.11 Error Catalog

| code | HTTP | ข้อความบนจอ (verbatim จากต้นแบบถ้ามี) |
|---|---|---|
| `E-PUT-403-ROLE` | 403 | (ปุ่มไม่แสดงตั้งแต่ต้น) |
| `E-PUT-409-HELD` | 409 | `งานนี้ถูก <ชื่อ> ถือครองอยู่` |
| `E-PUT-409-VERSION` | 409 | `ข้อมูลงานถูกแก้ไปแล้ว — กรุณาโหลดใหม่` `[AI-DEFAULT]` |
| `E-PUT-409-NOTHOLDER` | 409 | `ต้องกดรับงานก่อนจึงจะยืนยันได้` |
| `E-PUT-422-VOID` | 422 | `งานนี้ถูกถอนออกจากคิวแล้ว (ใบรับของต้นทางถูกกลับรายการ)` |
| `E-PUT-422-ACTOR` | 422 | `ต้องระบุผู้จัดเก็บที่เป็นคนจริง` `[AI-DEFAULT]` |
| `E-PUT-422-QTYNEG` | 422 | `ปลายทางที่ <N>: จำนวนติดลบไม่ได้` |
| `E-PUT-422-QTYZERO` | 422 | `ต้องมีปลายทางอย่างน้อย 1 รายการที่จำนวนมากกว่า 0` |
| `E-PUT-422-QTYOVER` | 422 | `จำนวนรวมเกินยอดคงค้างเก็บ <N> <หน่วย>` |
| `E-PUT-422-REASON` | 422 | `ปลายทางที่ <N> (<ชนิดการฝืน>): ต้องเลือกเหตุผลก่อนยืนยัน` |
| `E-PUT-422-REASONNOTE` | 422 | `ปลายทางที่ <N>: เลือก "อื่น ๆ" ต้องพิมพ์เหตุผลเพิ่ม` |
| `E-PUT-422-CROSSWH` | 422 | (กันที่แหล่ง — ช่องคลังอื่นไม่โผล่ในตัวเลือก) |
| `E-PUT-422-LOCTYPE` | 422 | (กันที่แหล่ง — ประเภทที่เข้ากันไม่ได้ไม่โผล่) |
| `E-WHBIN-422-BINLOCKED` | 422 | `ช่อง <code> ถูกล็อก — <เหตุผล>` |
| `E-WHBIN-422-LOCKREASON` | 422 | (ปุ่มล็อกถูกปิดจนกว่าจะกรอก · VR12) |
| `E-INVMV-403-ROLE` | 403 | (ปุ่มกลับรายการไม่แสดงสำหรับ role อื่น) |
| `E-INVMV-422-REASON` | 422 | (ปุ่มกลับรายการถูกปิดจนกว่าจะกรอก · VR11) |
| `E-INVMV-409-ALREADY` | 409 | `รายการนี้ถูกกลับรายการไปแล้ว` `[AI-DEFAULT]` |
| `E-INVMV-422-KIND` | 422 | `กลับรายการได้เฉพาะรายการประเภทจัดเก็บ` `[AI-DEFAULT]` |
| `E-INVMV-409-CONSUMED` | 409 | `ของถูกใช้ต่อไปแล้ว — ใช้ใบย้ายสินค้าแทน` `[AI-DEFAULT]` · รอ `OQ-PUT-04` |

> **รวม 20 รหัส** — map กับเคสทดสอบครบที่ `06_TESTS` §6.13
> ข้อความที่ติด `[AI-DEFAULT]` คือข้อความที่ **ยังไม่มีในต้นแบบ** (เป็น error ฝั่งเซิร์ฟเวอร์ล้วน) — ต้องให้ BA เคาะถ้อยคำก่อนขึ้นจริง
