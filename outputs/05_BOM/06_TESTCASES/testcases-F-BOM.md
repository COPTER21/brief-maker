# AI Test Cases — F-BOM-001 สูตรการผลิต (Bill of Materials)

ชุดทดสอบ Markdown สำหรับ browser-use/vision agent. ให้ยึดข้อความที่เห็นจริงใน `f-bom.html`; เคสที่ต้องใช้ API/dependency/tenant simulation ระบุไว้ชัดเจน.

## Meta

| Item | Value |
|---|---|
| Feature ID | F-BOM-001 |
| Version | FRD v6.1 STANDARD · 2026-08-12 |
| App entry | `#/bom` |
| Routes | `#/bom`, `#/bom/create`, `#/bom/edit/:id`, `#/bom/view/:id` |
| Sources | `04_FRD/FRD_F-BOM_Pack`, `03_BRD/BRD_F-BOM-001.md`, `01_HTML/f-bom.html` |
| Cases | 44 cases · UI/hybrid 32 · simulated/API/integration 12 |
| Anchor drift | HTML wins for visible text; production rules win for DRIFT-02/03. `nextStep()` says `ระบุเวอร์ชันสูตร`, final save says `ระบุเวอร์ชันสูตร (เช่น v1)` |

## Coverage

| Group | Cases | Priority |
|---|---:|---|
| List/navigation | 5 | high/medium |
| Create/edit/validation | 12 | high |
| Detail/default/status/bulk | 7 | high |
| Permission/security/reliability | 6 | high |
| Cross-module + scope lock | 6 | high/medium |

## Coverage Ledger

### FR / Acceptance

| item | cases |
|---|---|
| S-01 / AC-01..02 create | TC-C01..03 |
| S-02 / AC-03 default | TC-D03, TC-S02 |
| S-03 / AC-04 sibling | TC-D01 |
| S-04 / AC-05 amend used | TC-D02, TC-X02 |
| S-05 / AC-06 validation | TC-V01..08 |
| S-06 / AC-07 cascade | TC-C04, TC-V08 |
| S-07 / AC-08 lifecycle | TC-S01..03 |
| S-08 / AC-09 delete | TC-B03..04 |
| AC-10 cost classification | TC-P01..02 |

### Business Rules / Validation / Edge

| item | cases |
|---|---|
| BR-01..02 | TC-V02, TC-D03, TC-S02 |
| BR-03..06 | TC-C01, TC-C04, TC-V01, TC-V06..08 |
| BR-07..10 | TC-C01, TC-P01, TC-S01..03 |
| BR-11..15 `[AI-DEFAULT]` | TC-B03, TC-D02, TC-A01..03 |
| VR-01..08 | TC-V01..08 |
| EC-01..10 | TC-D03, TC-V02, TC-V06..08, TC-S02, TC-B03, TC-A01..03 |
| EC-AI-01..09 | TC-R01..04, TC-P01..03, TC-S02, TC-B03 |

### Error Codes

| errors | cases |
|---|---|
| required/duplicate/line/component/UoM/range business errors | TC-V01..08, TC-A02 |
| `ERR_NOT_AUTHENTICATED`, `ERR_INSUFFICIENT_ROLE` | TC-P02..03 |
| `ERR_BOM_NOT_FOUND`, `ERR_ACTIVE_BOM_NOT_FOUND` | TC-R04, TC-X03 |
| `ERR_IDEMPOTENCY_CONFLICT`, `ERR_STALE_DATA` | TC-R01..03 |
| `ERR_MASTER_DATA_UNAVAILABLE`, `ENG_BOM_COST_INVALID_INPUT` | TC-R05, TC-A02 |
| `BR_BOM_IN_USE` | TC-B03 |

### Permission Matrix

| cell | cases |
|---|---|
| Planner read/create/edit/status/delete allow | TC-C01, TC-D02, TC-S01, TC-B03 |
| Production active read only | TC-X01, TC-P03 |
| Costing read + cost allow, mutation deny | TC-P01, TC-P03 |
| Auditor read/audit allow, cost/mutation deny | TC-P02..03 |

### Cross-Module / Scope Lock / Cross-cutting

| item | cases |
|---|---|
| XT-01..03 Production/MO | TC-X01..03 |
| XT-04..05 Costing | TC-X04 |
| XT-06 master unavailable | TC-R05 |
| XT-07 audit fail closed | TC-R06 |
| XT-08 D-CLASS deny | TC-P02 |
| LOCK single-level + Item/UoM | TC-V07/08, TC-L05 |
| LOCK no approval/notification | TC-L05 |
| LOCK no CSV/print/document number | TC-L05 |
| LOCK no inventory/GL/effective scheduler | TC-L05, TC-X04 |
| list states/search/filter/sort/selection | TC-L01..04, TC-B01..02 |
| idempotency/concurrency/RLS/audit | TC-R01..06, TC-P04 |

## Data Sets

| Set | Field | Value |
|---|---|---|
| A | parent | `FG-1005 · ตู้เก็บเอกสาร 4 ชั้น` |
| A | version/name/out qty/date/default | `v2` / `สูตรมาตรฐานทดสอบ` / `1` / `2026-09-01` / on |
| A | line 1 | `RM-2001 · ไม้สักแปรรูป เกรด A`, qty `2.50`, UoM `KG`, scrap `5` |
| B | version/name | `v3` / `สูตรร่างทดสอบ` |
| DUP | parent/version | `FG-1001` / `V1` (ชนกับ `v1`) |
| BAD | qty/scrap | `0`, `101` |
| USED | BOM | `BOM-0001`, used=14, active/default |
| UNUSED | BOM | `BOM-0002`, used=0, draft |
| COST | component | `FG-1005` seed cost=0; simulated component cost=null |

ไม่มีไฟล์อัปโหลด—CSV/import อยู่นอก Scope Lock.

## Test Cases

### Group L — List and Navigation

### TC-L01 — ค้นหา/ล้างตัวกรอง (happy)
- group: list · ความสำคัญ: สูง · trace: FN-16 / API-01
- actor (role): Planner
- Setup: role=Planner · seed=มี BOM-0001..0004 · files=—
- Start: OPEN `#/bom`
- ผ่านเมื่อ: ค้นเจอ record ที่ตรง และล้างกลับมาเห็นทั้งหมด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bom` | — | เห็นหัวข้อ `สูตรการผลิต (BOM)` และ `สร้างสูตรใหม่` | ☐ |
| 2 | TYPE `BOM-0001` → ช่อง `ค้นหา รหัสสูตร / ชื่อ / สินค้า...` | — | ตารางเหลือแถว `BOM-0001` | ☐ |
| 3 | CLICK `ล้าง` | — | ช่องค้นหาว่างและ footer กลับเป็น `แสดง 4 จาก 4 สูตร` | ☐ |

### TC-L02 — filter ทุกสถานะ
- group: list · ความสำคัญ: สูง · trace: BR-10 / FN-16
- actor (role): Planner
- Setup: role=Planner · seed=มี active,draft,inactive อย่างน้อยอย่างละ 1 · files=—
- Start: OPEN `#/bom`
- ผ่านเมื่อ: `ใช้งาน`, `ไม่ใช้งาน`, `ร่าง`, `ทุกสถานะ` แสดงเฉพาะค่าที่เลือก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT `ใช้งาน` → dropdown `ทุกสถานะ` | — | ทุกแถวมี pill `ใช้งาน` | ☐ |
| 2 | SELECT `ไม่ใช้งาน` → dropdown สถานะ | — | ทุกแถวมี pill `ไม่ใช้งาน` หรือเห็น `ไม่พบสูตรการผลิต` หาก seed ไม่มี | ☐ |
| 3 | SELECT `ร่าง` → dropdown สถานะ | — | ทุกแถวมี pill `ร่าง` | ☐ |
| 4 | SELECT `ทุกสถานะ` → dropdown สถานะ | — | กลับมาเห็นทุกสถานะ | ☐ |

### TC-L03 — filtered empty
- group: list · ความสำคัญ: กลาง · trace: UI empty state
- actor (role): Planner
- Setup: role=Planner · seed=มี BOM อย่างน้อย 1 · files=—
- Start: OPEN `#/bom`
- ผ่านเมื่อ: ข้อความ empty ตรง HTML

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `NO-SUCH-BOM-999` → ช่องค้นหา | — | เห็น `ไม่พบสูตรการผลิต` และ footer `แสดง 0 จาก` | ☐ |

### TC-L04 — sort และเปิด detail
- group: list · ความสำคัญ: กลาง · trace: FN-16 / S-03
- actor (role): Planner
- Setup: role=Planner · seed=หลาย BOM · files=—
- Start: OPEN `#/bom`
- ผ่านเมื่อ: sort สลับลำดับและแถวเปิด route detail ถูก ID

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวตาราง `เวอร์ชัน` | — | ลำดับแถวเปลี่ยนตาม version | ☐ |
| 2 | CLICK หัวตาราง `เวอร์ชัน` อีกครั้ง | — | ลำดับกลับทิศ | ☐ |
| 3 | CLICK แถว `BOM-0001` | — | route เป็น `#/bom/view/b1`; drawer แสดง `BOM-0001` | ☐ |

### TC-L05 — Scope Lock ไม่มีของนอกขอบเขต
- group: scope · ความสำคัญ: สูง · trace: §0.11 / BR-13
- actor (role): Planner
- Setup: role=Planner · seed=มี BOM · files=—
- Start: OPEN `#/bom`
- ผ่านเมื่อ: ไม่พบ control/route สำหรับของ locked-out

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หน้า list และ drawer create/detail | — | ไม่มี approval/DOA, notification, CSV import/export, print/PDF, routing, multi-level tree, inventory/GL posting | ☐ |
| 2 | VERIFY ช่อง `เริ่มมีผล (effective)` | — | เป็นช่องวันที่เท่านั้น; ไม่มีข้อความ scheduler/auto status | ☐ |

### Group C/V — Create, Cascade and Validation

### TC-C01 — สร้างและเปิดใช้งาน (happy)
- group: create · ความสำคัญ: สูง · trace: AC-01/02 / BR-03..07
- actor (role): Planner
- Setup: role=Planner+cost_view · seed=Data Set A version ยังไม่ซ้ำ · files=—
- Start: OPEN `#/bom/create`
- ชุดข้อมูล: A
- ผ่านเมื่อ: toast `เปิดใช้งานแล้ว`, route list, เห็นแถว v2/ใช้งาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bom/create` | — | drawer `สร้างสูตรการผลิตใหม่`, step `ข้อมูลสูตร` active | ☐ |
| 2 | CLICK ช่อง `สินค้าผลผลิต (FG)` แล้ว SELECT `FG-1005 · ตู้เก็บเอกสาร 4 ชั้น` | A | ช่องแสดงสินค้าและ version default `v1` | ☐ |
| 3 | TYPE `v2` → `เวอร์ชันสูตร`; TYPE `สูตรมาตรฐานทดสอบ` → `ชื่อสูตร` | A | ช่องแสดงค่าครบ | ☐ |
| 4 | TYPE `1` → `ผลผลิตต่อสูตร`; TYPE `2026-09-01` → `เริ่มมีผล (effective)` | A | ช่องแสดงค่าที่กรอก | ☐ |
| 5 | TOGGLE `ตั้งเป็นสูตรหลัก` | on | switch เป็นสีส้ม | ☐ |
| 6 | CLICK `ถัดไป` | — | step `ส่วนประกอบ` active | ☐ |
| 7 | CLICK component row แล้ว SELECT `RM-2001 · ไม้สักแปรรูป เกรด A` | A | แถวแสดง RM-2001 และ UoM `KG · กิโลกรัม` | ☐ |
| 8 | TYPE `2.50` → `ปริมาณ`; TYPE `5` → `เผื่อเสีย%` | A | footer ต้นทุนรวมอัปเดต | ☐ |
| 9 | CLICK `บันทึก + เปิดใช้งาน` | — | toast `เปิดใช้งานแล้ว`; route `#/bom`; แถวใหม่ pill `ใช้งาน` | ☐ |

### TC-C02 — บันทึกร่าง `[AI-DEFAULT]`
- group: create · ความสำคัญ: สูง · trace: AC-02 / BR-02 / EC-AI-07
- actor (role): Planner
- Setup: role=Planner · seed=Data Set B unique · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: toast `บันทึกร่างแล้ว`; production contract ต้องแสดง `ร่าง` และไม่แสดง `สูตรหลัก`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bom/create` และกรอก Data Set B ให้ถึง step `ส่วนประกอบ` | B | form ผ่าน validation | ☐ |
| 2 | TOGGLE `ตั้งเป็นสูตรหลัก` | on | switch on ก่อนบันทึก | ☐ |
| 3 | CLICK `บันทึกร่าง` | — | toast `บันทึกร่างแล้ว`; แถวใหม่ pill `ร่าง`; **ต้องไม่มี** badge `สูตรหลัก` (HTML ปัจจุบันอาจ fail: DRIFT-02) | ☐ |

### TC-C03 — ย้อนกลับคงค่า
- group: wizard · ความสำคัญ: กลาง · trace: wizard state
- actor (role): Planner
- Setup: role=Planner · seed=Data Set A · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: กลับ step 1 แล้วยังเห็นค่าที่กรอก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bom/create` แล้วกรอก parent/version/name | A | เห็นค่าครบ | ☐ |
| 2 | CLICK `ถัดไป` | — | step `ส่วนประกอบ` active | ☐ |
| 3 | CLICK `ย้อนกลับ` | — | step `ข้อมูลสูตร` activeและค่าก่อนหน้ายังคงอยู่ | ☐ |

### TC-C04 — เปลี่ยน component แล้ว UoM reset
- group: cascade · ความสำคัญ: สูง · trace: AC-07 / BR-06 / EC-05
- actor (role): Planner
- Setup: role=Planner · seed=form valid at step 2, line RM-2001/KG · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: เลือก PM-4001 แล้วหน่วยเป็น count ไม่คง KG

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง component แล้ว SELECT `PM-4001 · กล่องลูกฟูก 5 ชั้น` | — | component เปลี่ยนเป็น PM-4001; UoM เป็น `PCS · ชิ้น` | ☐ |
| 2 | CLICK dropdown หน่วย | — | ตัวเลือกมี count (`PCS`,`SET`,`BOX`) และไม่มี `KG`/`L` | ☐ |

### TC-V01 — parent required (negative)
- group: validation · ความสำคัญ: สูง · trace: VR-01 / `BR_BOM_PARENT_REQUIRED`
- actor (role): Planner
- Setup: role=Planner · seed=— · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: อยู่ step เดิมและเห็น `เลือกสินค้าผลผลิตก่อน`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ถัดไป` โดยไม่เลือก FG | — | toast `เลือกสินค้าผลผลิตก่อน`; ยังอยู่ `ข้อมูลสูตร` | ☐ |

### TC-V02 — version ว่างและซ้ำ (negative)
- group: validation · ความสำคัญ: สูง · trace: VR-02a/b / BR-01 / EC-02
- actor (role): Planner
- Setup: role=Planner · seed=FG-1001 มี v1 · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: ทั้งว่างและ `V1` ถูก block

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT `FG-1001` แล้ว TYPE ค่าว่าง → `เวอร์ชันสูตร`; CLICK `ถัดไป` | — | toast `ระบุเวอร์ชันสูตร`; อยู่ step เดิม | ☐ |
| 2 | TYPE `V1` → `เวอร์ชันสูตร`; TYPE `ทดสอบซ้ำ` → `ชื่อสูตร`; CLICK `ถัดไป` | DUP | HTML อาจผ่าน exact-case step check; เมื่อ save ต้องเห็น `เวอร์ชัน V1 ของสินค้านี้มีอยู่แล้ว` และไม่สร้างแถว | ☐ |

### TC-V03 — name required (negative)
- group: validation · ความสำคัญ: สูง · trace: VR-03
- actor (role): Planner
- Setup: role=Planner · seed=parent/version valid · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: toast `ระบุชื่อสูตร`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ค่าว่าง → `ชื่อสูตร`; CLICK `ถัดไป` | — | toast `ระบุชื่อสูตร`; step ไม่เปลี่ยน | ☐ |

### TC-V04 — no component (negative)
- group: validation · ความสำคัญ: สูง · trace: VR-04
- actor (role): Planner
- Setup: role=Planner · seed=form step 2 valid, 1 line · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: toast exact และไม่มี record

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนถังขยะท้าย component ทุกแถว | — | เห็น `ยังไม่มีส่วนประกอบ — กดเพิ่มด้านล่าง` | ☐ |
| 2 | CLICK `บันทึก + เปิดใช้งาน` | — | toast `ต้องมีส่วนประกอบอย่างน้อย 1 รายการ`; drawer คงอยู่ | ☐ |

### TC-V05 — qty ≤0 (boundary)
- group: validation · ความสำคัญ: สูง · trace: VR-05
- actor (role): Planner
- Setup: role=Planner · seed=form step 2 line RM-2001 · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: toast exact และไม่บันทึก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `0` → `ปริมาณ`; CLICK `บันทึก + เปิดใช้งาน` | — | toast `ปริมาณของ RM-2001 ต้องมากกว่า 0` | ☐ |

### TC-V06 — duplicate component (negative)
- group: validation · ความสำคัญ: สูง · trace: VR-06 / EC-03
- actor (role): Planner
- Setup: role=Planner · seed=form step 2 มี RM-2001 · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: duplicate block ไม่ merge

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `เพิ่มส่วนประกอบ` และ SELECT `RM-2001` ในแถวใหม่ | — | เห็น RM-2001 สองแถว | ☐ |
| 2 | CLICK `บันทึก + เปิดใช้งาน` | — | toast `วัตถุดิบ RM-2001 ซ้ำ — รวมเป็นรายการเดียว`; สองแถวยังคงให้แก้ | ☐ |

### TC-V07 — self component / single-level (negative)
- group: validation · ความสำคัญ: สูง · trace: VR-07 / BR-05 / LOCK
- actor (role): Planner
- Setup: role=Planner · seed=ต้อง inject forged payload component=parent เพราะ UI pickerไม่เสนอ FG · files=—
- Start: OPEN `#/bom/create` (ต้อง simulate API)
- ผ่านเมื่อ: API block `BR_BOM_SELF_COMPONENT`; UI แสดง `ส่วนประกอบห้ามเป็นตัวสินค้าเอง (FG-1001) — กัน BOM วน`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY component picker | — | ไม่มี Item type FG ให้เลือก | ☐ |
| 2 | VERIFY simulated forged save result | component=`FG-1001` | mutation ไม่เกิด; เห็น error ตามข้อความข้างต้น | ☐ |

### TC-V08 — forged cross-category UoM (negative)
- group: validation · ความสำคัญ: สูง · trace: VR-08 / `BR_BOM_UOM_INVALID`
- actor (role): Planner
- Setup: role=Planner · seed=ต้อง inject API body RM-2001 + UoM L · files=—
- Start: OPEN `#/bom/create` (ต้อง simulate API)
- ผ่านเมื่อ: UI ไม่เสนอ L และ API คืน `BR_BOM_UOM_INVALID`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT RM-2001 แล้ว CLICK dropdown หน่วย | — | เห็นเฉพาะ `KG · กิโลกรัม`, `G · กรัม` | ☐ |
| 2 | VERIFY simulated forged save | `uom_code=L` | ไม่สร้าง record; error `BR_BOM_UOM_INVALID` | ☐ |

### Group D/S/B — Detail, Default, Status, Bulk

### TC-D01 — sibling version navigation
- group: detail · ความสำคัญ: สูง · trace: AC-04 / FN-09
- actor (role): Planner
- Setup: role=Planner · seed=FG-1001 มี b1,b2 · files=—
- Start: OPEN `#/bom/view/b1`
- ผ่านเมื่อ: คลิก v2 แล้ว route/detail เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bom/view/b1` | — | tab `ภาพรวม` active; เห็น `เวอร์ชันอื่นของสินค้านี้ (1)` | ☐ |
| 2 | CLICK แถว version `v2` | — | route `#/bom/view/b2`; header แสดง `BOM-0002`/`v2` | ☐ |

### TC-D02 — edit referenced `[AI-DEFAULT]`
- group: edit · ความสำคัญ: สูง · trace: AC-05 / BR-12 / AID-01
- actor (role): Planner
- Setup: role=Planner · seed=USED BOM + MO snapshot baseline; files=—
- Start: OPEN `#/bom/view/b1`
- ผ่านเมื่อ: edit ไม่ถูก block และ MO snapshot เดิมไม่เปลี่ยน (ต้อง simulate downstream verify)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึก snapshot ของ MO ที่อ้าง b1 | — | จด lines/version ก่อนแก้ | ☐ |
| 2 | CLICK `แก้ไขสูตร` | — | route `#/bom/edit/b1`; drawer edit เปิด | ☐ |
| 3 | CLICK `ถัดไป`; TYPE ค่า qty ใหม่; CLICK `บันทึก + เปิดใช้งาน` | qty=`12.50` | toast `เปิดใช้งานแล้ว` | ☐ |
| 4 | VERIFY snapshot MO เดิม (ต้อง simulate) | — | เท่ากับค่าที่จด step 1 ทุก field | ☐ |

### TC-D03 — move default atomically
- group: default · ความสำคัญ: สูง · trace: AC-03 / BR-02 / EC-01
- actor (role): Planner
- Setup: role=Planner · seed=b1 active default, b2 active non-default · files=—
- Start: OPEN `#/bom/edit/b2`
- ผ่านเมื่อ: b2 มี `สูตรหลัก`, b1 ไม่มี

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TOGGLE `ตั้งเป็นสูตรหลัก`; CLICK `ถัดไป`; CLICK `บันทึก + เปิดใช้งาน` | — | toast `เปิดใช้งานแล้ว` | ☐ |
| 2 | OPEN `#/bom/view/b2` | — | เห็น badge `สูตรหลัก` | ☐ |
| 3 | OPEN `#/bom/view/b1` | — | ไม่เห็น badge `สูตรหลัก` | ☐ |

### TC-S01 — single status all directions
- group: status · ความสำคัญ: สูง · trace: AC-08 / BR-08/10
- actor (role): Planner
- Setup: role=Planner · seed=unused BOM · files=—
- Start: OPEN `#/bom/view/b2`
- ผ่านเมื่อ: เปลี่ยนไป `ใช้งาน`, `ไม่ใช้งาน`, `ร่าง` ได้โดยไม่มี approval

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `เปลี่ยนสถานะ`; CLICK `ใช้งาน` | — | toast `เปลี่ยนสถานะเป็น ใช้งาน แล้ว`; pill `ใช้งาน` | ☐ |
| 2 | CLICK `เปลี่ยนสถานะ`; CLICK `ไม่ใช้งาน` | — | toast `เปลี่ยนสถานะเป็น ไม่ใช้งาน แล้ว`; pill `ไม่ใช้งาน` | ☐ |
| 3 | CLICK `เปลี่ยนสถานะ`; CLICK `ร่าง` | — | toast `เปลี่ยนสถานะเป็น ร่าง แล้ว`; pill `ร่าง`; ไม่มี approval dialog | ☐ |

### TC-S02 — leaving active clears default
- group: status · ความสำคัญ: สูง · trace: BR-02 / EC-06 / EC-AI-07
- actor (role): Planner
- Setup: role=Planner · seed=active default BOM · files=—
- Start: OPEN `#/bom/view/b1`
- ผ่านเมื่อ: non-active ไม่มี badge default

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY badge `สูตรหลัก` ก่อนเปลี่ยน | — | badge ปรากฏ | ☐ |
| 2 | CLICK `เปลี่ยนสถานะ`; CLICK `ไม่ใช้งาน` | — | pill `ไม่ใช้งาน`; badge `สูตรหลัก` หาย | ☐ |

### TC-S03 — bulk status + selection
- group: bulk · ความสำคัญ: สูง · trace: FN-18 / API-05
- actor (role): Planner
- Setup: role=Planner · seed=≥2 BOM · files=—
- Start: OPEN `#/bom`
- ผ่านเมื่อ: select all current filtered rows, bulk status, clear bar

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox หัวตาราง | — | ทุกแถวที่เห็นไฮไลต์; bar `เลือก N รายการ` ปรากฏ | ☐ |
| 2 | CLICK `ไม่ใช้งาน` ใน bulk bar | — | toast `เปลี่ยนสถานะ N สูตรเป็น ไม่ใช้งาน แล้ว`; pill ของ record ที่เปลี่ยนเป็น `ไม่ใช้งาน`; bar หาย | ☐ |

### TC-B01 — select one/cancel
- group: bulk · ความสำคัญ: กลาง · trace: UI selection
- actor (role): Planner
- Setup: role=Planner · seed=≥2 BOM · files=—
- Start: OPEN `#/bom`
- ผ่านเมื่อ: one row selected then cleared

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถวแรก | — | แถวไฮไลต์; bar `เลือก 1 รายการ` | ☐ |
| 2 | CLICK `ยกเลิก` ใน bulk bar | — | highlight/bar หาย | ☐ |

### TC-B02 — delete confirmation dismissed
- group: bulk delete · ความสำคัญ: กลาง · trace: FN-90
- actor (role): Planner
- Setup: role=Planner · seed=UNUSED selected · files=—
- Start: OPEN `#/bom`
- ผ่านเมื่อ: ยกเลิกแล้วจำนวนแถวไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึกจำนวนใน card `สูตรทั้งหมด` | — | จดค่าเริ่มต้น | ☐ |
| 2 | CLICK checkbox BOM-0002; CLICK `ลบ` | — | modal `ลบสูตรการผลิต 1 รายการ?` | ☐ |
| 3 | CLICK `ยกเลิก` | — | modal ปิด; card `สูตรทั้งหมด` เท่าค่า step 1 | ☐ |

### TC-B03 — mixed guarded delete `[AI-DEFAULT]`
- group: bulk delete · ความสำคัญ: สูง · trace: AC-09 / BR-11 / EC-07 / AID-02
- actor (role): Planner
- Setup: role=Planner · seed=USED+UNUSED selected · files=—
- Start: OPEN `#/bom`
- ผ่านเมื่อ: unused หาย, used อยู่, toast ledger ถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox `BOM-0001` และ `BOM-0002`; CLICK `ลบ` | — | modal `ลบสูตรการผลิต 2 รายการ?`; ข้อความ `มี 1 สูตร...จะถูกข้าม` | ☐ |
| 2 | CLICK `ลบ 1 สูตร` | — | toast `ลบแล้ว 1 สูตร · ข้าม 1 (มีใบสั่งผลิตอ้างแล้ว)` | ☐ |
| 3 | TYPE `BOM-0001` → search | — | ยังเห็น BOM-0001 | ☐ |
| 4 | TYPE `BOM-0002` → search | — | เห็น `ไม่พบสูตรการผลิต` | ☐ |

### TC-B04 — all used delete disabled
- group: bulk delete · ความสำคัญ: สูง · trace: AC-09
- actor (role): Planner
- Setup: role=Planner · seed=เลือกเฉพาะ USED · files=—
- Start: OPEN `#/bom`
- ผ่านเมื่อ: danger button disabled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox `BOM-0001`; CLICK `ลบ` | — | modal มี `ลบ 0 สูตร`; ปุ่มซีดและกดไม่ได้ | ☐ |

### Group P/R/A — Permission, Reliability, AI Defaults

### TC-P01 — Costing sees cost
- group: permission · ความสำคัญ: สูง · trace: AC-10 / BR-09
- actor (role): Costing
- Setup: role=Costing+cost_view · seed=BOM known cost · files=—
- Start: OPEN `#/bom/view/b1`
- ผ่านเมื่อ: เห็นต้นทุน/หน่วยและรวม; mutation controls absent/denied in production build

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab `ส่วนประกอบ (5)` | — | เห็นหัว `ต้นทุน/หน่วย`, `รวม`, `ต้นทุนวัตถุดิบรวม` พร้อมตัวเลข | ☐ |
| 2 | VERIFY header actions | — | production UI ต้องไม่มี/ปฏิเสธ `แก้ไขสูตร` และ `เปลี่ยนสถานะ` สำหรับ Costing (prototype mock อาจ fail) | ☐ |

### TC-P02 — cost denied/masked
- group: permission · ความสำคัญ: สูง · trace: AC-10 / EC-AI-08 / XT-08
- actor (role): Auditor
- Setup: role=Auditor without cost_view · seed=BOM known cost · files=—
- Start: OPEN `#/bom`
- ผ่านเมื่อ: ไม่มี raw cost ใน list/detail/client-visible response

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY column `ต้นทุนรวม` | — | ค่า cost ถูก mask/ว่าง; ห้ามเห็นตัวเลขจริง (prototype mock ปัจจุบันอาจ fail: DRIFT-03) | ☐ |
| 2 | OPEN `#/bom/view/b1`; CLICK `ส่วนประกอบ (5)` | — | cost cells ไม่เปิดเผยตัวเลขจริง | ☐ |

### TC-P03 — denied mutations by non-Planner (ต้อง simulate)
- group: permission · ความสำคัญ: สูง · trace: `ERR_INSUFFICIENT_ROLE`
- actor (role): Production/Costing/Auditor
- Setup: role=แต่ละบทบาทไม่มี Planner capability · seed=BOM · files=—
- Start: OPEN `#/bom`
- ผ่านเมื่อ: create/edit/status/delete controls unavailable or API 403; record unchanged

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY actions ด้วยแต่ละ role | — | ไม่สามารถเรียก create/edit/status/delete; forged mutation ได้ `ERR_INSUFFICIENT_ROLE` | ☐ |

### TC-P04 — tenant isolation (ต้อง simulate)
- group: security · ความสำคัญ: สูง · trace: RLS / `ERR_BOM_NOT_FOUND`
- actor (role): Planner tenant B
- Setup: role=Planner tenant B · seed=b1 belongs tenant A · files=—
- Start: OPEN `#/bom/view/b1`
- ผ่านเมื่อ: ไม่เห็นข้อมูล tenant A; response not-found/list fallback

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bom/view/b1` as tenant B | — | ไม่เห็นชื่อ/lines/cost/audit ของ b1; server result `ERR_BOM_NOT_FOUND` | ☐ |

### TC-R01 — stale edit (ต้อง simulate)
- group: reliability · ความสำคัญ: สูง · trace: EC-AI-01 / `ERR_STALE_DATA`
- actor (role): Planner
- Setup: role=Planner · seed=two sessions open same version_no · files=—
- Start: OPEN `#/bom/edit/b2`
- ผ่านเมื่อ: first save wins; second does not overwrite and receives stale indication

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY session A and B show same initial name/version | — | จด initial value/version | ☐ |
| 2 | CLICK save in session A after changing name | — | success | ☐ |
| 3 | CLICK save in session B with different name | — | `ERR_STALE_DATA`; valueจาก A ยังอยู่เมื่อ refresh | ☐ |

### TC-R02 — idempotent retry `[AI-DEFAULT]` (ต้อง simulate)
- group: reliability · ความสำคัญ: สูง · trace: TC-ID-01 / AID-06
- actor (role): Planner
- Setup: role=Planner · seed=unique create command · inject lost response after commit · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: retry same key produces one BOM/one create audit

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK final save with injected lost response | — | UI sees transport failure while server committed | ☐ |
| 2 | CLICK retry using same request/key | — | original success result returned; list has exactly one matching BOM | ☐ |

### TC-R03 — idempotency conflict (ต้อง simulate)
- group: reliability · ความสำคัญ: สูง · trace: `ERR_IDEMPOTENCY_CONFLICT`
- actor (role): Planner
- Setup: role=Planner · seed=reuse one key with two bodies · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: second body rejected, first record unchanged

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY simulated same-key/different-body response | — | `409 ERR_IDEMPOTENCY_CONFLICT`; ไม่มี record ที่สอง | ☐ |

### TC-R04 — unknown ID
- group: error · ความสำคัญ: กลาง · trace: `ERR_BOM_NOT_FOUND` / DRIFT-05
- actor (role): Planner
- Setup: role=Planner · seed=id `missing-bom` absent · files=—
- Start: OPEN `#/bom/view/missing-bom`
- ผ่านเมื่อ: production design shows not-found/return action; current prototype silently routes `#/bom` and should be recorded as drift

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bom/view/missing-bom` | — | ไม่แสดงข้อมูลอื่นแทน; production expected visible not-found, prototype actual redirects list | ☐ |

### TC-R05 — master unavailable (ต้อง simulate)
- group: integration error · ความสำคัญ: สูง · trace: XT-06 / `ERR_MASTER_DATA_UNAVAILABLE`
- actor (role): Planner
- Setup: role=Planner · seed=valid unsaved form · inject Item/UoM service unavailable · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: save fails, form retained, no partial BOM

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `บันทึก + เปิดใช้งาน` after injection | — | safe error for unavailable master; drawer/input remain; list has no partial record | ☐ |

### TC-R06 — audit failure closed `[AI-DEFAULT]` (ต้อง simulate)
- group: integration error · ความสำคัญ: สูง · trace: XT-07 / AID-08
- actor (role): Planner
- Setup: role=Planner · seed=valid edit · inject audit append failure · files=—
- Start: OPEN `#/bom/edit/b2`
- ผ่านเมื่อ: mutation rolls back

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึกชื่อเดิม | — | จดค่าเดิม | ☐ |
| 2 | TYPE ชื่อใหม่; CLICK save | — | safe failure; after refresh ชื่อเท่าค่าเดิม step 1; ไม่มี audit success | ☐ |

### TC-A01 — missing/zero cost `[AI-DEFAULT]`
- group: boundary · ความสำคัญ: กลาง · trace: EC-08 / AID-03
- actor (role): Planner+cost_view
- Setup: role=Planner+cost_view · seed=line cost 0 and simulated null · files=—
- Start: OPEN `#/bom/view/:id`
- ผ่านเมื่อ: zero deterministic; null contributes zero and production response flags missing

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab `ส่วนประกอบ (...)` | — | zero cost displays ฿0.00; null case has visible/response missing-cost indicator, no NaN | ☐ |

### TC-A02 — scrap/numeric boundary `[AI-DEFAULT]`
- group: boundary · ความสำคัญ: สูง · trace: EC-09 / AID-04/07 / `BR_BOM_NUMERIC_RANGE`
- actor (role): Planner+cost_view
- Setup: role=Planner+cost_view · seed=line qty=2 cost=100 · files=—
- Start: OPEN `#/bom/create`
- ผ่านเมื่อ: scrap100 cost=400; 101/overflow blocked

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `100` → `เผื่อเสีย%` | — | live totalเท่ากับ 400 สำหรับ seed | ☐ |
| 2 | TYPE `101`; CLICK save | — | production API block `BR_BOM_NUMERIC_RANGE` (HTML input max alone is insufficient) | ☐ |

### TC-A03 — deactivated master `[AI-DEFAULT]`
- group: edge · ความสำคัญ: กลาง · trace: EC-10 / AID-05
- actor (role): Planner
- Setup: role=Planner · seed=active BOM then deactivate one component in Item Master · files=—
- Start: OPEN `#/bom/view/:id`
- ผ่านเมื่อ: read still works; next save rejected until corrected

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN detail after deactivation | — | existing structure remains readable | ☐ |
| 2 | CLICK `แก้ไขสูตร`; CLICK final save | — | `BR_BOM_MASTER_INACTIVE`; no partial update | ☐ |

### Group X — Cross-module

### TC-X01 — MO eligible/default (ต้อง simulate)
- group: XT · ความสำคัญ: สูง · trace: XT-01
- actor (role): Production
- Setup: role=Production · seed=FG has active default + active non-default + draft · files=—
- Start: OPEN MO create screen (downstream prototype ไม่พบ)
- ผ่านเมื่อ: eligible list active only, default first, no cost

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY simulated API-07 choices | parent FG | มีเฉพาะ active; default อยู่บน; ไม่มี standard/line/total cost | ☐ |

### TC-X02 — MO snapshot after amendment `[AI-DEFAULT]` (ต้อง simulate)
- group: XT · ความสำคัญ: สูง · trace: XT-02 / AID-01
- actor (role): Planner + Production
- Setup: role=both · seed=MO snapshot from b1 · files=—
- Start: OPEN `#/bom/edit/b1`
- ผ่านเมื่อ: old snapshot conserved, new MO gets current

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึก old MO snapshot | — | จด version/lines | ☐ |
| 2 | CLICK save after changing BOM line | — | BOM detail shows new value | ☐ |
| 3 | VERIFY old and new MO snapshots | — | old equals step 1; new equals amended BOM | ☐ |

### TC-X03 — inactive excluded from new MO (ต้อง simulate)
- group: XT · ความสำคัญ: สูง · trace: XT-03 / `ERR_ACTIVE_BOM_NOT_FOUND`
- actor (role): Planner + Production
- Setup: role=both · seed=one active BOM used by old MO · files=—
- Start: OPEN `#/bom/view/:id`
- ผ่านเมื่อ: old MO retains; API-07 excludes inactive

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `เปลี่ยนสถานะ`; CLICK `ไม่ใช้งาน` | — | BOM pill `ไม่ใช้งาน` | ☐ |
| 2 | VERIFY simulated API-07/old MO | — | inactive absent; old snapshot still present; if no active remains code `ERR_ACTIVE_BOM_NOT_FOUND` | ☐ |

### TC-X04 — current Costing recalc, no posting (ต้อง simulate)
- group: XT · ความสำคัญ: สูง · trace: XT-04/05 / Scope Lock
- actor (role): Costing
- Setup: role=Costing+cost_view · seed=component cost changes 100→120 · files=—
- Start: OPEN `#/bom/view/:id`
- ผ่านเมื่อ: displayed current rollup changes predictably; no inventory/GL row/event

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึก total before Item cost change | — | จด total/cost_as_of | ☐ |
| 2 | VERIFY after simulated Item cost change | — | total reflects 120-based formula and cost_as_of newer; no inventory/GL posting | ☐ |

## วิธีที่ agent รัน (Run protocol)

1. Reset seed before each case; do not depend on a previous case’s mutations.
2. Use the exact Start route. For `:id`, substitute the seeded ID stated in Setup.
3. Execute one row at a time; mark `☐` as pass/fail and capture what was visibly observed.
4. If Setup says `(ต้อง simulate)` and the runner cannot inject role/dependency/API state, mark `blocked`, not pass.
5. Treat `[AI-DEFAULT]` failure as either implementation defect or unresolved business-decision mismatch; preserve evidence.
6. Never put authentication tokens, cookies, passwords, API keys, or secrets in evidence/report.

## Coverage Audit

| หมวด | covered / total |
|---|---:|
| Stories / AC | 10 / 10 |
| Business rules | 15 / 15 |
| Validations | 8 / 8 |
| Confirmed edge cases | 10 / 10 |
| AI edge/default groups | 9 / 9 |
| Error catalog groups | 19 / 19 |
| Permission capability cells | 8 / 8 |
| Cross-module XT | 8 / 8 |
| Scope Lock groups | 4 / 4 |
| UI list/form/detail/bulk states present in HTML | 12 / 12 |

- Cross-Module (XT): **8/8**
- Scope Lock: **4/4 grouped assertions**
- `[AI-DEFAULT]` propagation: **10/10 AID values covered** across TC-C02/D02/B03/R02/R06/A01..03/X02
- **Manifest cross-check (FRD §0.12): ✅ 8/8 rows**

### ข้ามพร้อมเหตุผล

- loading skeleton, request error/retry, visible stale/permission/not-found designs: FRD requires them but source HTML has no visual anchor; retained as simulated cases where behavior is contractual.
- CSV/import/export, approval, notification, multi-level/routing, print/PDF, inventory/GL posting: exclusions; only verify absence under Scope Lock, no functional test was invented.
- WebSocket/events: none declared.

## Result Report (schema)

```json
{
  "feature_id": "F-BOM-001",
  "run_at": "<iso datetime>",
  "results": [
    {"id":"TC-L01","status":"pass|fail|blocked","failed_step":null,"evidence":"","note":""}
  ],
  "summary":{"total":44,"pass":0,"fail":0,"blocked":0}
}
```
