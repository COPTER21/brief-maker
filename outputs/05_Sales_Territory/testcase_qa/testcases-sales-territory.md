# AI Test Cases — Sales Territory

เอกสาร Markdown สำหรับ AI browser/API test agent ทดสอบ F-05 แบบอิสระต่อเคส โดยใช้ `../01_HTML/sales-territory.html` เป็นแหล่ง route และข้อความบนจอ และใช้ FRD เป็น production contract. ห้ามตีความ fixture ของห้า future modules ว่าเป็น integration จริง

> Drift note: D-01 พนักงานขาย required บน prototype แต่ optional ใน FRD; D-02 prototype ยอมข้อความจังหวัดนอก dataset; D-03 prototype clamp/parse universe แทนการ reject. เคสที่เกี่ยวข้องจะแยก **Prototype observation** กับ **Production contract** และไม่ประกาศว่าเป็น defect จน PM/BA อนุมัติทิศทาง

## Meta

| รายการ | ค่า |
|---|---|
| Feature ID | F-05 / F-SALES-TERRITORY |
| ชื่อ | Sales Territory (ผังเขตขาย) |
| Version | 1.0 · 2026-08-13 |
| App entry | เปิดไฟล์/แอป prototype ที่ mount approved HTML |
| Routes | `#/sales-territory` เท่านั้น |
| Sources | ../04_FRD/FRD_F-05_Pack 7/7, ../03_BRD/BRD_Sales_Territory.md, ../01_HTML/sales-territory.html, ../05_UI_BRIEF/UI_BRIEF_Sales_Territory.md |
| Source priority | Approved lock/business baseline → HTML visible route/copy → FRD production contract; conflict logged, not hidden |
| จำนวนเคส | 75 เคส / 7 groups |
| Default policy | เคสที่อิง OQ/lane default ติด `[AI-DEFAULT]` |
| Files | ไม่มีไฟล์อัปโหลด |

## Coverage

| Group | Cases | จำนวน | ความสำคัญ |
|---|---|---:|---|
| N — Navigation/List/UI states | TC-N01–TC-N12 | 12 | สูง/กลาง |
| C — CRUD/Drawer/Responsive | TC-C01–TC-C10 | 10 | สูง |
| V — Validation/Boundary | TC-V01–TC-V15 | 15 | สูง |
| L — Lifecycle/Atomic/Resilience | TC-L01–TC-L13 | 13 | สูง |
| P — Permission/Security | TC-P01–TC-P08 | 8 | สูง |
| X — Map/Future hooks/Scope safeguards | TC-X01–TC-X16 | 16 | สูง/กลาง |
| Q — Performance proposal | TC-Q01 | 1 | ต่ำ / pending approval |

## Coverage Ledger

### Acceptance Criteria (06_TESTS)

| item | cases |
|---|---|
| AC-01 | TC-N01, TC-N02 |
| AC-02 | TC-C04 |
| AC-03 | TC-C01, TC-L06 |
| AC-04 | TC-C02, TC-V01–TC-V06, TC-V09 |
| AC-05 | TC-C05, TC-L06 |
| AC-06 | TC-C06, TC-V06 |
| AC-07 | TC-L01, TC-L02 |
| AC-08 | TC-L03 |
| AC-09 | TC-N08, TC-N09 |
| AC-10 | TC-X05, TC-X06, TC-X11, TC-X15 |
| AC-11 | TC-X01, TC-X02 |
| AC-12 | TC-X03, TC-X04 |
| AC-13 | TC-V10, TC-V11, TC-X07 |
| AC-14 | TC-L05 |
| AC-15 | TC-X14 `[AI-DEFAULT]` |
| AC-16 | TC-L07 `[AI-DEFAULT]` |
| AC-17 | TC-L08, TC-P08 `[AI-DEFAULT]` |
| AC-18 | TC-L09, TC-L10 `[AI-DEFAULT]` |
| AC-19 | TC-L11 `[AI-DEFAULT]` |
| AC-20 | TC-C09, TC-C10 |

### Existing Test Inventory Inputs (06_TESTS §6.2)

| inventory | expanded cases |
|---|---|
| TC-UI-01 | TC-N01–TC-N02 |
| TC-UI-02 | TC-C01, TC-C04–TC-C08 |
| TC-UI-03 | TC-L01–TC-L03 |
| TC-UI-04 | TC-N03–TC-N09 |
| TC-UI-05 | TC-X05, TC-X11 |
| TC-MAP-01 | TC-X01, TC-X02 |
| TC-MAP-02 | TC-X03, TC-X04 |
| TC-API-01 | TC-N10–TC-N12, TC-L12–TC-L13 |
| TC-API-02 | TC-C01–TC-C03, TC-V01–TC-V15, TC-L06 |
| TC-API-03 | TC-C05–TC-C06, TC-L06–TC-L10 |
| TC-API-04 | TC-L01–TC-L04, TC-L07–TC-L11 |
| TC-XT-01 | TC-X07–TC-X13 |
| TC-CON-01 | TC-L07 |
| TC-PERM-01 | TC-L08, TC-P01–TC-P04, TC-P08 |
| TC-IDEM-01 | TC-L09–TC-L10 |
| TC-RESP-01 | TC-C09–TC-C10 |
| TC-SEC-01 | TC-P01–TC-P08 |
| TC-PERF-01 | TC-Q01 `[AI-DEFAULT]` |

### Business Rules (05_RULES)

| rule | cases |
|---|---|
| BR-ST-01 | TC-N01, TC-C01 |
| BR-ST-02 | TC-V10, TC-V11 |
| BR-ST-03 | TC-V10, TC-X07 |
| BR-ST-04 | TC-V01–TC-V05 |
| BR-ST-05 | TC-C06, TC-V06 |
| BR-ST-06 | TC-C02, TC-V09 |
| BR-ST-07 | TC-X01, TC-X02 |
| BR-ST-08 | TC-V08, TC-X16 |
| BR-ST-09 | TC-L01–TC-L05 |
| BR-ST-10 | TC-C01, TC-C05, TC-L02, TC-L03, TC-L06 |
| BR-ST-11 | TC-X05, TC-X06, TC-X08–TC-X11 |
| BR-ST-12 | TC-X12 |
| BR-ST-13 | TC-X13 |
| BR-ST-14 | TC-L05 |
| BR-ST-15 | TC-X14 `[AI-DEFAULT]` |
| BR-ST-16 | TC-X06 `[AI-DEFAULT]` |
| BR-ST-17 | TC-X05 `[AI-DEFAULT]` |
| BR-ST-18 | TC-V07, TC-X16 `[AI-DEFAULT]` |
| BR-ST-19 | TC-X03, TC-X04 |
| BR-ST-20 | TC-X01, TC-X02, TC-X07, TC-X11, TC-X15 |

### Edge Cases and Lane Defaults

| item | cases / status |
|---|---|
| EC-01 invalid/duplicate/missing | TC-V01–TC-V08 |
| EC-02 blank province | TC-C02 |
| EC-03 salesperson provider absent | TC-V10, TC-X07 |
| EC-04 future salesperson inactive/deleted | TC-X07 `[AI-DEFAULT]`; safeguard only, no provider implementation |
| EC-05 customer count/archive warning | TC-X08 |
| EC-06 universe/coverage source absent | TC-C03, TC-X05, TC-X06 |
| EC-07 archive/restore + audit | TC-L02, TC-L03 |
| EC-08 pointer outside frame/side list | TC-X04 |
| EC-09 historical snapshot stable | TC-X12 `(ต้อง simulate)` |
| EC-10 any provider absent | TC-X07–TC-X13 |
| PR-2 stale data | TC-L07 `[AI-DEFAULT]` `(ต้อง simulate)` |
| PR-3 permission mid-flight | TC-L08 `[AI-DEFAULT]` `(ต้อง simulate)` |
| PR-4 network response loss | TC-L09 `[AI-DEFAULT]` `(ต้อง simulate)` |
| PR-7 double submit/key conflict | TC-L09, TC-L10 `[AI-DEFAULT]` `(ต้อง simulate)` |
| restore conflict | TC-L11 `[AI-DEFAULT]` `(ต้อง simulate)` |
| local geo corrupt | TC-X02 `[AI-DEFAULT]` `(ต้อง simulate)` |

### Error Codes

| error | cases |
|---|---|
| ERR_INVALID_QUERY | TC-V14 `(ต้อง simulate)` |
| ERR_NOT_AUTHENTICATED | TC-L13 `(ต้อง simulate)` |
| ERR_INSUFFICIENT_ROLE | TC-P03, TC-P04 `(ต้อง simulate)` |
| ERR_PERMISSION_REVOKED | TC-L08, TC-P08 `[AI-DEFAULT]` `(ต้อง simulate)` |
| ERR_ROUTE_NOT_FOUND | TC-L12 `(ต้อง simulate)` |
| ERR_ROUTE_CODE_CONFLICT | TC-V05 `(ต้อง simulate backend for authoritative result)` |
| ERR_STALE_DATA | TC-L07 `[AI-DEFAULT]` `(ต้อง simulate)` |
| ERR_IDEMPOTENCY_CONFLICT | TC-L10 `[AI-DEFAULT]` `(ต้อง simulate)` |
| ERR_RESTORE_CODE_CONFLICT | TC-L11 `[AI-DEFAULT]` `(ต้อง simulate)` |
| BR_ROUTE_CODE_INVALID | TC-V01–TC-V04 |
| BR_ROUTE_CODE_IMMUTABLE | TC-C06, TC-V06 `(ต้อง simulate backend mutation)` |
| BR_REQUIRED_FIELD | TC-V01, TC-V06, TC-V15 |
| BR_ROUTE_TYPE_INVALID | TC-V07 `(ต้อง simulate)` |
| BR_REGION_INVALID | TC-V08 `(ต้อง simulate)` |
| BR_PROVINCE_INVALID | TC-V09 `(ต้อง simulate; prototype drift D-02)` |
| BR_UNIVERSE_INVALID | TC-V12, TC-V13 `(ต้อง simulate; prototype drift D-03)` |
| BR_INVALID_STATE_TRANSITION | TC-L04 `(ต้อง simulate)` |
| ERR_AUDIT_WRITE_FAILED | TC-L06 `(ต้อง simulate)` |

### Validation Schema

| field/action | constraints | cases |
|---|---|---|
| route_code create | required, regex, length 2–12, tenant unique | TC-C01, TC-V01–TC-V05 |
| route_code edit | immutable | TC-C06, TC-V06 |
| route_name | required/nonblank | TC-V06 |
| route_type | required/accepted enum | TC-C01, TC-V07, TC-V15 |
| region | required/approved enum | TC-C01, TC-V08, TC-V15 |
| province_code | null or local dataset member | TC-C02, TC-V09 |
| salesperson_ref | nullable opaque string; max one; structural validation only | TC-V10, TC-V11 |
| universe | null/blank or integer ≥0 | TC-C03, TC-V12, TC-V13 |
| archive/restore | permission, state, version | TC-L01–TC-L04, TC-L07–TC-L08, TC-L11 |

### Permission Matrix — 24 cells

| cell | cases |
|---|---|
| sales_admin × View = allow | TC-P01 |
| sales_admin × Create = allow | TC-P01 |
| sales_admin × Edit = allow | TC-P01 |
| sales_admin × Archive = allow | TC-P01 |
| sales_admin × Restore = allow | TC-P01 |
| sales_admin × Workload/Map = allow | TC-P01 |
| system_admin × View = allow | TC-P02 |
| system_admin × Create = allow | TC-P02 |
| system_admin × Edit = allow | TC-P02 |
| system_admin × Archive = allow | TC-P02 |
| system_admin × Restore = allow | TC-P02 |
| system_admin × Workload/Map = allow | TC-P02 |
| sales_manager × View = hold | TC-P03 `[AI-DEFAULT]` |
| sales_manager × Create = deny | TC-P03 |
| sales_manager × Edit = deny | TC-P03 |
| sales_manager × Archive = deny | TC-P03 |
| sales_manager × Restore = deny | TC-P03 |
| sales_manager × Workload/Map = hold | TC-P03 `[AI-DEFAULT]` |
| salesperson × View = hold | TC-P04 `[AI-DEFAULT]` |
| salesperson × Create = deny | TC-P04 |
| salesperson × Edit = deny | TC-P04 |
| salesperson × Archive = deny | TC-P04 |
| salesperson × Restore = deny | TC-P04 |
| salesperson × Workload/Map = hold | TC-P04 `[AI-DEFAULT]` |

### Cross-Module Safeguards (XT)

| XT | downstream | case |
|---|---|---|
| XT-01 | Sales Team/Salesperson | TC-X07 |
| XT-02 | Customer Master/archive | TC-X08 |
| XT-03 | Sales Order/Customer/Target metrics | TC-X05, TC-X06, TC-X11 |
| XT-04 | Visit Operation hook | TC-X10 |
| XT-05 | all future consumers/snapshot | TC-X12, TC-X13 `(ต้อง simulate contract fixture)` |

### Scope Lock

| LOCK | verify case |
|---|---|
| LOCK-01 code unique/format/immutable | TC-V02–TC-V06 |
| LOCK-02 optional province/KPI | TC-C02 |
| LOCK-03 active/archive/restore/no delete | TC-L02–TC-L05 |
| LOCK-04 no approval/DOA | TC-L05 |
| LOCK-05 five modules hook/mock only | TC-X07–TC-X13 |
| LOCK-06 snapshot immutable | TC-X12 |
| LOCK-07 exactly one route | TC-N01 |
| LOCK-08 map valid-frame only | TC-X03–TC-X04 |
| LOCK-09 outer-page Structure scroll | TC-C09–TC-C10 |
| LOCK-10 R-BK-01 fixture only | TC-X16 |

### Coverage Manifest Cross-check — 38 items

| manifest set | item | cases |
|---|---|---|
| Story | US-01 Create Route | TC-C01–C03, TC-V01–V15 |
| Story | US-02 View detail | TC-C04 |
| Story | US-03 Edit Route | TC-C05–C06, TC-X12 |
| Story | US-04 Archive | TC-L01–L02, TC-X08 |
| Story | US-05 Restore | TC-L03, TC-L11 |
| Story | US-06 Search/filter/reset | TC-N03–N09 |
| Story | US-07 Workload | TC-X05–X06, TC-X11 |
| Story | US-08 Map | TC-X01–X04 |
| Story | US-09 Safe future hooks | TC-X07–X13 |
| Rule | BR-01 Route primary unit | TC-N01, TC-C01 |
| Rule | BR-02 one salesperson per Route | TC-V10, TC-V11 |
| Rule | BR-03 salesperson soft ref | TC-V10, TC-X07 |
| Rule | BR-04 code format/unique | TC-V01–V05 |
| Rule | BR-05 code immutable | TC-C06, TC-V06 |
| Rule | BR-06 province optional/KPI | TC-C02, TC-V09 |
| Rule | BR-07 offline 77 provinces | TC-X01, TC-X02 |
| Rule | BR-08 approved regions | TC-V08, TC-X16 |
| Rule | BR-09 archive/restore/no delete | TC-L01–L05 |
| Rule | BR-10 append-only audit | TC-C01, TC-C05, TC-L02, TC-L03, TC-L06 |
| Rule | BR-11 future-derived read-only | TC-X05–X11 |
| Rule | BR-12 historical snapshot immutable | TC-X12 |
| Rule | BR-13 archived excluded for new future records | TC-X13 |
| Rule | BR-14 no DOA/approval | TC-L05 |
| Rule | BR-15 overlap baseline | TC-X14 `[AI-DEFAULT]` |
| Rule | BR-16 coverage threshold prototype | TC-X06 `[AI-DEFAULT]` |
| Rule | BR-17 workload formula prototype | TC-X05 `[AI-DEFAULT]` |
| Rule | BR-18 Route Types unresolved | TC-V07, TC-X16 `[AI-DEFAULT]` |
| Rule | BR-19 map frame boundary | TC-X03, TC-X04 |
| Rule | BR-20 core resilience | TC-X01, TC-X02, TC-X07, TC-X11, TC-X15 |
| Confirmed edge | duplicate/invalid/missing | TC-V01–V06 |
| Confirmed edge | province blank | TC-C02 |
| Confirmed edge | salesperson provider absent | TC-X07 |
| Confirmed edge | future salesperson inactive/deleted | TC-X07 |
| Confirmed edge | linked-customer warning | TC-X08 |
| Confirmed edge | universe/coverage absent | TC-C03, TC-X05, TC-X06 |
| Confirmed edge | archive/restore + audit | TC-L02, TC-L03 |
| Confirmed edge | pointer outside map | TC-X04 |
| Confirmed edge | downstream snapshot immutable | TC-X12 |

### Cross-cutting / Events / States

| item | cases / status |
|---|---|
| authentication + role authorization | TC-L13, TC-P01–TC-P04 |
| tenant isolation `[AI-DEFAULT]` | TC-P05 `(ต้อง simulate)` |
| PII minimum response/logging | TC-P06, TC-P07 `(ต้อง simulate)` |
| append-only atomic audit | TC-L06 |
| idempotency/concurrency | TC-L07, TC-L09, TC-L10 `[AI-DEFAULT]` |
| lifecycle states active/archived | TC-L02–TC-L04 |
| UI loaded/loading/error/403 | TC-N10–TC-N12, TC-P03/P04; production-only states may require simulate |
| filtered-empty/reset | TC-N08–TC-N09 |
| drawer/modal/combobox/tooltip/toast state | TC-C07, TC-C08, TC-L01, TC-X03/X04 |
| notifications/realtime events | — N/A: FRD declares no business event/WebSocket |
| hard delete/approval/export/import/bulk | — ไม่สร้าง implementation case; OOS/LOCK verification only in TC-L05 |

## Data Sets

### ชุดข้อมูลกรอกได้

| ชุด | ฟิลด์ | ค่า |
|---|---|---|
| A valid central | code/name/type/region/province/rep/universe | `R-TC-01`; `ทดสอบภาคกลาง`; `Area Route (GT)`; `ภาคกลาง`; `กรุงเทพมหานคร`; `เอก ทวีสุข`; `30` |
| B blank optionals | code/name/type/region/province/rep/universe | `R-TC-02`; `เขตข้ามจังหวัด`; `B2B / องค์กร`; `ส่วนกลาง / ออนไลน์`; blank; blank; blank |
| C edit | name/type/region/province/rep/universe | `ทดสอบแก้ไข`; `Van Sales`; `ตะวันตก`; `นครปฐม`; `บอย รุ่งเรือง`; `42` |
| D overlap | code/name/province | `R-TC-03`; `เขตซ้อนทดสอบ`; จังหวัดเดียวกับ Route active seed |

### ชุดข้อมูลผิด/ขอบเขต

| ชุด | ค่า |
|---|---|
| I01 | code blank |
| I02 | code `r bad!*` |
| I03 | code `R` (1 ตัว) |
| I04 | code `R-12345678901` (13 ตัว) |
| I05 | code ซ้ำกับ active seed `R-BK-01` |
| I06 | name เป็นช่องว่างล้วน |
| I07 | route_type `unknown_type` |
| I08 | region `ภาคที่ไม่มีจริง` |
| I09 | province `จังหวัดที่ไม่มีจริง` |
| I10 | salesperson_ref โครงสร้างเกิน 100 ตัวอักษร |
| I11 | universe `-1` |
| I12 | universe `1.5` |

### Seeds และ environment

| seed | รายละเอียด |
|---|---|
| S1 | ≥3 active Routes และ ≥2 archived Routes; ครบ code/name/province/rep; มี `R-BK-01` fixture |
| S2 | active Route A มี customer fixture count >0; active Route B ไม่มี customer/provider |
| S3 | archived Route พร้อม version และไม่มี code conflict |
| S4 | two tenants มี route_code เดียวกัน; actor ของ tenant A/B |
| S5 | future transaction snapshot fixture มี code/name/type/region/province ก่อนแก้ master |

### ไฟล์ทดสอบ (Files)

ไม่มีไฟล์อัปโหลด (`files=—` ทุกเคส)

## Test Cases

### Group N — Navigation, List, Search and UI States

### TC-N01 — หนึ่ง route และสามแท็บ (happy)
- group: Navigation · ความสำคัญ: สูง · trace: AC-01 / US-06 / LOCK-07 / BR-ST-01
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: S1
- ผ่านเมื่อ: route คงเดิมและเห็นสามแท็บบนหน้าเดียว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็นหัวข้อ **ผังเขตขาย** และแท็บ **โครงสร้างเขต** เป็นค่าเริ่มต้น | ☐ |
| 2 | VERIFY แถบแท็บใต้ KPI | — | เห็น **โครงสร้างเขต**, **ภาระงาน**, **แผนที่** ครบ และ URL ยังเป็น `#/sales-territory` | ☐ |
| 3 | CLICK แท็บ **ภาระงาน** | — | เนื้อหาเปลี่ยนเป็นตารางภาระงานโดย URL ไม่เปลี่ยน | ☐ |
| 4 | CLICK แท็บ **แผนที่** | — | เห็นแผนที่ประเทศไทยโดย URL ไม่เปลี่ยน | ☐ |

### TC-N02 — hash ว่างเข้าหน้าหลัก
- group: Navigation · ความสำคัญ: กลาง · trace: AC-01 / LOCK-07
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 · files=—
- Start: OPEN app โดยไม่มี hash
- ชุดข้อมูล: S1
- ผ่านเมื่อ: ระบบเติม route จริงและ render P-01

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN app โดยไม่มี hash | — | URL เปลี่ยนเป็น `#/sales-territory` | ☐ |
| 2 | VERIFY หัวข้อและรายการ | — | เห็น **ผังเขตขาย**, **สร้างเขต**, และรายการ Route | ☐ |

### TC-N03 — ค้นหาด้วยรหัส
- group: List · ความสำคัญ: สูง · trace: US-06 / API-01
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 มี `R-BK-01` เพียงแถวเดียวที่ตรง · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: `R-BK-01`
- ผ่านเมื่อ: เหลือเฉพาะแถวรหัสตรงคำค้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็นช่อง **ค้นหา รหัส / ชื่อ / จังหวัด / พนักงานขาย** | ☐ |
| 2 | TYPE `R-BK-01` → ช่องค้นหา | `R-BK-01` | ช่องคง focus/caret และรายการแสดงแถว `R-BK-01` | ☐ |
| 3 | VERIFY ตารางโครงสร้าง | — | ทุกแถว Route ที่เห็นตรงคำค้น; ไม่มีแถว Route อื่น | ☐ |

### TC-N04 — ค้นหาด้วยชื่อภาษาไทย
- group: List · ความสำคัญ: กลาง · trace: US-06 / API-01
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 มีชื่อ Route เฉพาะ `กรุงเทพฯ ชั้นใน สาย 1` · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: `กรุงเทพฯ ชั้นใน`
- ผ่านเมื่อ: ค้นภาษาไทยได้และ focus ไม่หลุด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | แท็บ **โครงสร้างเขต** พร้อมใช้งาน | ☐ |
| 2 | TYPE `กรุงเทพฯ ชั้นใน` → ช่องค้นหา | — | รายการอัปเดตระหว่างพิมพ์และช่องยัง focus | ☐ |
| 3 | VERIFY แถวผลลัพธ์ | — | เห็นชื่อ `กรุงเทพฯ ชั้นใน สาย 1` และไม่เห็นแถวไม่ตรง | ☐ |

### TC-N05 — ค้นหาด้วยจังหวัด
- group: List · ความสำคัญ: กลาง · trace: US-06 / API-01
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 มี Route จังหวัด `นครปฐม` · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: `นครปฐม`
- ผ่านเมื่อ: ผลตรงจังหวัด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็นรายการ Route | ☐ |
| 2 | TYPE `นครปฐม` → ช่องค้นหา | — | เห็นเฉพาะ Route ที่คอลัมน์จังหวัดเป็น `นครปฐม` | ☐ |

### TC-N06 — ค้นหาด้วยพนักงานขาย
- group: List · ความสำคัญ: กลาง · trace: US-06 / API-01
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 มี Route ของ `เอก ทวีสุข` · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: `เอก ทวีสุข`
- ผ่านเมื่อ: ผลตรง label fixture โดยไม่เรียก provider

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็นช่องค้นหา | ☐ |
| 2 | TYPE `เอก ทวีสุข` → ช่องค้นหา | — | เห็นเฉพาะ Route ที่แสดงพนักงานขาย `เอก ทวีสุข`; หน้าไม่ค้าง | ☐ |

### TC-N07 — กรองสถานะครบทุกค่า
- group: List · ความสำคัญ: สูง · trace: US-06 / API-01 / state active-archived
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 มี active และ archived · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: S1
- ผ่านเมื่อ: `ใช้งาน`, `เก็บเข้าคลัง`, `ทั้งหมด` ให้ผลตาม pill

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | ตัวกรองเริ่มที่ **ใช้งาน** และทุกแถวมี pill **ใช้งาน** | ☐ |
| 2 | SELECT **เก็บเข้าคลัง** → ตัวกรองสถานะ | — | ทุกแถวที่เห็นมี pill **เก็บเข้าคลัง** | ☐ |
| 3 | SELECT **ทั้งหมด** → ตัวกรองสถานะ | — | เห็นทั้ง pill **ใช้งาน** และ **เก็บเข้าคลัง** | ☐ |
| 4 | SELECT **ใช้งาน** → ตัวกรองสถานะ | — | กลับมาเห็นเฉพาะ active | ☐ |

### TC-N08 — filtered-empty ข้อความตรง HTML
- group: List · ความสำคัญ: สูง · trace: AC-09 / US-06
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: `ZZZ-NOT-FOUND`
- ผ่านเมื่อ: empty copy และ action ตรง source

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็นช่องค้นหา | ☐ |
| 2 | TYPE `ZZZ-NOT-FOUND` → ช่องค้นหา | — | เห็น **ไม่พบ Route** และ **ลองเปลี่ยนคำค้นหรือตัวกรองสถานะ** | ☐ |
| 3 | VERIFY empty action | — | เห็นปุ่ม **ล้างตัวกรอง** | ☐ |

### TC-N09 — ล้างตัวกรองคืน default
- group: List · ความสำคัญ: สูง · trace: AC-09 / US-06
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: `ZZZ-NOT-FOUND`, archived
- ผ่านเมื่อ: query ว่างและ status กลับ `ใช้งาน`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็นรายการ active | ☐ |
| 2 | SELECT **เก็บเข้าคลัง** → ตัวกรองสถานะ | — | เห็น archived | ☐ |
| 3 | TYPE `ZZZ-NOT-FOUND` → ช่องค้นหา | — | เห็น empty state | ☐ |
| 4 | CLICK ปุ่ม **ล้างตัวกรอง** | — | ช่องค้นหาว่าง; ตัวกรองเป็น **ใช้งาน**; รายการ active กลับมา | ☐ |

### TC-N10 — loaded state และ KPI semantics
- group: UI states · ความสำคัญ: สูง · trace: API-01 / BR-ST-06 / loaded state
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 โดยทราบจำนวน active/province-valid/universe/customer fixture · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: S1
- ผ่านเมื่อ: KPI นับ active และจังหวัด dataset-valid เท่านั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็น KPI **Route ใช้งาน**, **จังหวัดที่ครอบคลุม**, **ร้านในเขต / ลูกค้า**, **Coverage** | ☐ |
| 2 | VERIFY ค่า KPI เทียบ seed | S1 | Route ใช้งานเท่าจำนวน active; จังหวัดไม่นับ blank/invalid; archived ไม่ถูกนับ | ☐ |

### TC-N11 — list loading และ error/retry `(ต้อง simulate)`
- group: UI states · ความสำคัญ: กลาง · trace: 01_UI loading/error / API-01
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=inject API-01 delayed แล้วตอบ 500; runner ต้องมี production-wired UI เพราะ static prototype ไม่มี state นี้ · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: production UI รักษา header/filter และมี retry; prototype run ให้ `blocked` พร้อม evidence ไม่ใช่ fail

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | API-01 delayed | header/tabs ไม่ขยับ; เห็น loading list state ⚠ ยืนยัน anchor | ☐ |
| 2 | WAIT จน API-01 ตอบ 500 | — | เห็น generic central error/retry ⚠ ยืนยัน anchor และ filter ที่กรอกไว้ยังอยู่ | ☐ |
| 3 | CLICK ปุ่ม retry ของ error state ⚠ ยืนยัน anchor | API-01 success | รายการกลับเป็น loaded โดยไม่เปลี่ยน route | ☐ |

### TC-N12 — invalid list scope/not-found response separation `(ต้อง simulate)`
- group: API/UI states · ความสำคัญ: สูง · trace: API-01/02 / ERR_ROUTE_NOT_FOUND
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=route id ที่อยู่นอก authorized scope; inject API-02=404 · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: out-of-scope route id
- ผ่านเมื่อ: ไม่เปิดเผย record และไม่แสดงข้อมูล fixture แทน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | รายการไม่แสดง Route นอก scope | ☐ |
| 2 | OPEN deep action ที่เรียก detail id นอก scopeผ่าน test harness | API-02 404 | ไม่เห็นรายละเอียด/PII ของ record; แสดง error ที่ไม่เปิดเผย existence ⚠ ยืนยัน anchor | ☐ |

### Group C — CRUD, Drawer, Combobox and Responsive

### TC-C01 — สร้าง Route ครบฟิลด์ (happy)
- group: CRUD · ความสำคัญ: สูง · trace: AC-03 / US-01 / BR-ST-01/04/08/10 / API-03
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=ไม่มี code `R-TC-01` · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: A valid central
- ผ่านเมื่อ: drawer ปิด, toast สำเร็จ, แถว active ใหม่ปรากฏ; production มี Route+audit หนึ่งคู่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็นปุ่ม **สร้างเขต** | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawer หัวข้อ **เพิ่ม Route** เปิดและ focus ช่องแรก | ☐ |
| 3 | TYPE `R-TC-01` → ช่อง **รหัส Route** | A | ช่องแสดงค่า | ☐ |
| 4 | TYPE `ทดสอบภาคกลาง` → ช่อง **ชื่อ Route** | A | ช่องแสดงค่า | ☐ |
| 5 | SELECT `Area Route (GT)` → **ประเภท** | A | ค่าเลือกปรากฏ | ☐ |
| 6 | SELECT `ภาคกลาง` → **ภาค** | A | ค่าเลือกปรากฏ | ☐ |
| 7 | TYPE `กรุงเทพ` → ช่อง **จังหวัด** | A | dropdown แสดง `กรุงเทพมหานคร` | ☐ |
| 8 | CLICK ตัวเลือก `กรุงเทพมหานคร` | A | ช่องแสดง `กรุงเทพมหานคร`; dropdown ปิด | ☐ |
| 9 | TYPE `เอก` → ช่อง **พนักงานขายผู้รับผิดชอบ** | A | dropdown แสดง `เอก ทวีสุข` | ☐ |
| 10 | CLICK ตัวเลือก `เอก ทวีสุข` | A | ช่องแสดงชื่อที่เลือก | ☐ |
| 11 | TYPE `30` → ช่อง **ร้านในเขต (universe)** | A | ช่องแสดง `30` | ☐ |
| 12 | CLICK ปุ่ม **ยืนยันสร้าง** | — | ปุ่ม disabled และแสดง **กำลังบันทึก…** | ☐ |
| 13 | WAIT จนบันทึกเสร็จ | ≤3s | drawer ปิด; toast **สร้างเขตสำเร็จ**; เห็นแถว `R-TC-01` pill **ใช้งาน** | ☐ |

### TC-C02 — province ว่างไม่เพิ่ม KPI (edge: EC-02)
- group: CRUD · ความสำคัญ: สูง · trace: AC-04 / BR-ST-06 / LOCK-02 / EC-02
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=ไม่มี `R-TC-02`; จดค่า KPI จังหวัดได้ · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: B แต่เลือก salesperson fixture เพื่อผ่าน prototype D-01
- ผ่านเมื่อ: สร้างได้และ KPI จังหวัดเท่าเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็น KPI **จังหวัดที่ครอบคลุม** | ☐ |
| 2 | VERIFY และบันทึก KPI จังหวัดตั้งต้น | — | จดเลขฐาน `province_kpi_before` | ☐ |
| 3 | CLICK ปุ่ม **สร้างเขต** | — | drawer **เพิ่ม Route** เปิด | ☐ |
| 4 | TYPE/SELECT ฟิลด์ required ด้วยชุด B และเลือก `เอก ทวีสุข` | B | ช่อง **จังหวัด** ยังคงว่าง | ☐ |
| 5 | CLICK ปุ่ม **ยืนยันสร้าง** | — | เห็น **กำลังบันทึก…** แล้ว toast **สร้างเขตสำเร็จ** | ☐ |
| 6 | VERIFY KPI **จังหวัดที่ครอบคลุม** | — | เท่ากับ `province_kpi_before` ที่จดใน step 2 | ☐ |

### TC-C03 — universe ว่างบันทึกได้
- group: CRUD · ความสำคัญ: สูง · trace: EC-06 / validation universe
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=code ใหม่ `R-TC-U0`; เลือก rep fixture เพื่อผ่าน prototype · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: valid required + universe blank
- ผ่านเมื่อ: บันทึกสำเร็จและรายละเอียดแสดงค่าว่าง `—`/ไม่มีค่าปลอม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็น **สร้างเขต** | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawer เปิด | ☐ |
| 3 | TYPE/SELECT ฟิลด์ required และ salesperson fixture | code `R-TC-U0` | ช่อง universe ยังว่าง | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันสร้าง** | — | toast **สร้างเขตสำเร็จ** | ☐ |
| 5 | CLICK แถว `R-TC-U0` | — | view drawer แสดง **ร้านในเขต (universe)** เป็นค่าว่างมาตรฐาน `—`/ไม่แสดงตัวเลข production ที่แต่งขึ้น | ☐ |

### TC-C04 — ดูรายละเอียด read-only
- group: CRUD · ความสำคัญ: สูง · trace: AC-02 / US-02 / API-02
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 active Route `R-BK-01` · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: S1
- ผ่านเมื่อ: view drawer แสดง owned fields แบบอ่านอย่างเดียวและปุ่มปิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็นแถว `R-BK-01` | ☐ |
| 2 | CLICK แถว `R-BK-01` | — | drawer title `{code} — {name}` และ pill **ใช้งาน** ปรากฏ | ☐ |
| 3 | VERIFY ส่วน **ข้อมูล Route** | — | เห็น รหัส/ชื่อ/ประเภท/ภาค/จังหวัด/พนักงานขาย/ร้านในเขต แบบไม่มี input editable | ☐ |
| 4 | VERIFY footer drawer | — | เห็นปุ่ม **ปิด** และข้อความแก้ไขล่าสุด | ☐ |
| 5 | CLICK ปุ่ม **ปิด** | — | drawer ปิด; หน้า list ยังอยู่ route เดิม | ☐ |

### TC-C05 — แก้ไข mutable fields (happy)
- group: CRUD · ความสำคัญ: สูง · trace: AC-05 / US-03 / API-04 / BR-ST-10
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=active Route `R-EDIT-01` version=1 · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: C edit
- ผ่านเมื่อ: กลับ view drawer เห็นค่าที่แก้และ toast ตรง HTML; production version+audit เพิ่ม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็นแถว `R-EDIT-01` | ☐ |
| 2 | CLICK แถว `R-EDIT-01` | — | view drawer เปิด | ☐ |
| 3 | CLICK ปุ่ม **แก้ไข** | — | drawer title **แก้ไข Route — R-EDIT-01** | ☐ |
| 4 | TYPE `ทดสอบแก้ไข` → ช่อง **ชื่อ Route** | C | ช่องแสดงชื่อใหม่ | ☐ |
| 5 | SELECT `Van Sales` → **ประเภท** | C | ค่าใหม่ปรากฏ | ☐ |
| 6 | SELECT `ตะวันตก` → **ภาค** | C | ค่าใหม่ปรากฏ | ☐ |
| 7 | TYPE แล้ว CLICK `นครปฐม` → **จังหวัด** | C | ช่องแสดง `นครปฐม` | ☐ |
| 8 | TYPE แล้ว CLICK `บอย รุ่งเรือง` → **พนักงานขายผู้รับผิดชอบ** | C | ช่องแสดงชื่อใหม่ | ☐ |
| 9 | TYPE `42` → **ร้านในเขต (universe)** | C | ช่องแสดง `42` | ☐ |
| 10 | CLICK ปุ่ม **บันทึกการแก้ไข** | — | ปุ่มแสดง **กำลังบันทึก…** | ☐ |
| 11 | WAIT จนบันทึกเสร็จ | ≤3s | toast **บันทึกการแก้ไขแล้ว**; กลับ view drawer เห็นค่าชุด C | ☐ |

### TC-C06 — รหัส Route ล็อกใน edit
- group: CRUD/Validation · ความสำคัญ: สูง · trace: AC-06 / BR-ST-05 / BR_ROUTE_CODE_IMMUTABLE
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=active `R-EDIT-01` · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: attempt code `R-HACK-01`
- ผ่านเมื่อ: UI เปลี่ยน code ไม่ได้; backend ปฏิเสธ payload ที่พยายามเปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็นแถว `R-EDIT-01` | ☐ |
| 2 | CLICK แถว `R-EDIT-01` แล้ว CLICK **แก้ไข** | — | edit drawer เปิด | ☐ |
| 3 | VERIFY ฟิลด์ **รหัส Route** | — | code แสดง `R-EDIT-01` และ disabled/อ่านอย่างเดียว | ☐ |
| 4 | TYPE `R-HACK-01` → ฟิลด์ **รหัส Route** | — | ค่าไม่เปลี่ยนจาก `R-EDIT-01` | ☐ |
| 5 | CLICK ปุ่ม **บันทึกการแก้ไข** | — | หลังสำเร็จ Route code ยังเป็น `R-EDIT-01` | ☐ |

### TC-C07 — Esc/backdrop/X และ edit cancel chain
- group: Overlay/UX · ความสำคัญ: สูง · trace: UI interaction / AC-20
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 active Route · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: dismiss แต่ละทางทำตาม source; edit Esc/cancel กลับ view

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` แล้ว CLICK **สร้างเขต** | — | create drawer เปิด | ☐ |
| 2 | PRESS Esc | — | drawer ปิดโดยไม่มี toast สำเร็จ | ☐ |
| 3 | CLICK แถว active แล้ว CLICK **แก้ไข** | — | edit drawer เปิด | ☐ |
| 4 | PRESS Esc | — | กลับ view drawerของ Route เดิม ไม่ปิดทั้ง drawer | ☐ |
| 5 | CLICK ปุ่ม **แก้ไข** แล้ว CLICK ปุ่ม **ยกเลิก** | — | กลับ view drawer | ☐ |
| 6 | CLICK พื้นที่ backdrop นอก drawer | — | drawer ปิด | ☐ |
| 7 | CLICK แถวเดิม แล้ว CLICK ไอคอน X มุมขวาบน | — | drawer ปิด | ☐ |

### TC-C08 — combobox scroll/keyboard/portal/dismiss
- group: Overlay/UX · ความสำคัญ: สูง · trace: UI master combobox / AC-20
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=province list 77 + salesperson fixtures · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: province `นครปฐม`, rep `บอย รุ่งเรือง`
- ผ่านเมื่อ: menu ไม่ clip, scroll ได้, keyboard และ dismiss chain ถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` แล้ว CLICK **สร้างเขต** | — | drawer เปิด | ☐ |
| 2 | CLICK ช่อง **จังหวัด** | — | dropdown portal เปิดเหนือ drawer ไม่ถูกตัด | ☐ |
| 3 | PRESS ArrowDown หลายครั้ง | — | highlight เลื่อนและตัวเลือกที่ highlight ถูก scroll เข้ามาให้เห็น | ☐ |
| 4 | PRESS Enter | — | จังหวัดที่ highlight ปรากฏในช่องและ dropdown ปิด | ☐ |
| 5 | CLICK ปุ่ม **ล้างการเลือก** ของจังหวัด | — | ช่องว่างและ focus กลับช่องจังหวัด | ☐ |
| 6 | TYPE `นคร` → ช่อง **จังหวัด** | — | เห็นตัวเลือก `นครปฐม` และเมนูเลื่อนด้วย wheel/trackpad ได้ | ☐ |
| 7 | PRESS Esc | — | dropdown ปิดแต่ drawer ยังเปิด | ☐ |
| 8 | TYPE `บอย` → ช่อง **พนักงานขายผู้รับผิดชอบ** | — | เห็น `บอย รุ่งเรือง` | ☐ |
| 9 | CLICK พื้นที่ว่างภายในฟอร์มนอก dropdown | — | dropdown ปิด; ค่าที่ไม่ได้เลือกคืนเป็นค่าเดิม; click เป้าหมายไม่หาย | ☐ |

### TC-C09 — responsive 1024×768 และ outer-page scroll
- group: Responsive · ความสำคัญ: สูง · trace: AC-20 / LOCK-09
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=≥30 Routes ให้หน้ายาว · viewport=1024×768 · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: 30 Routes
- ผ่านเมื่อ: เลื่อนทั้งหน้าได้ ไม่มี nested Structure scroll และ drawer action เข้าถึงได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` ที่ 1024×768 | — | header/tabs/ตารางไม่ล้นนอก baseline 768px; คอลัมน์ responsive ถูกซ่อนตาม source | ☐ |
| 2 | VERIFY แล้ว scroll จากพื้นที่นอกตารางลงท้ายรายการ | — | scrollbar หลักด้านขวาของพื้นที่เนื้อหาเลื่อนรายการทั้งหมด; ไม่มีกล่อง list scrollbar แนวตั้งแยก | ☐ |
| 3 | CLICK ปุ่ม **สร้างเขต** | — | drawerสูงเต็ม viewportและ footer **ยืนยันสร้าง** เข้าถึงได้ด้วย drawer-body scroll | ☐ |
| 4 | TYPE `นคร` → ช่อง **จังหวัด** | — | dropdown ไม่ clip/จมหลัง drawer | ☐ |

### TC-C10 — responsive 1440×900 และ overlay stacking
- group: Responsive · ความสำคัญ: สูง · trace: AC-20 / LOCK-09
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 active Route · viewport=1440×900 · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: S1
- ผ่านเมื่อ: shell/table/drawer/modal/toast ไม่ clip หรือซ้อนผิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` ที่ 1440×900 | — | sidebar 232px, topbar, KPI, ตารางอ่านได้โดยไม่เกิด horizontal page overflow | ☐ |
| 2 | CLICK แถว active แล้ว CLICK **เก็บเข้าคลัง** | — | modal อยู่เหนือ drawer/backdrop และปุ่ม **ยกเลิก**/**เก็บเข้าคลัง** เข้าถึงได้ | ☐ |
| 3 | CLICK ปุ่ม **ยกเลิก** | — | modal ปิด; drawerยังอยู่; ไม่มี clipping/scroll jump | ☐ |

### Group V — Validation and Boundaries

### TC-V01 — code ว่าง (negative)
- group: Validation · ความสำคัญ: สูง · trace: AC-04 / EC-01 / BR_ROUTE_CODE_INVALID / BR_REQUIRED_FIELD
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=— · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: I01 + valid remaining fields
- ผ่านเมื่อ: drawerคงอยู่และไม่มี record

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็น **สร้างเขต** | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawer **เพิ่ม Route** เปิด | ☐ |
| 3 | TYPE/SELECT ฟิลด์อื่นให้ถูกและเว้น **รหัส Route** | I01 | ฟิลด์อื่นคงค่า | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันสร้าง** | — | drawerไม่ปิด; ฟิลด์ code แสดง `ระบุรหัส A-Z 0-9 - _ ยาว 2-12 ตัว และห้ามซ้ำกับที่มีอยู่`; toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |

### TC-V02 — code มี lowercase/ช่องว่าง/อักขระผิด (negative)
- group: Validation · ความสำคัญ: สูง · trace: BR-ST-04 / BR_ROUTE_CODE_INVALID / EC-01
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=— · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: I02
- ผ่านเมื่อ: format ผิดถูกบล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | หน้าโหลด | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawer เปิด | ☐ |
| 3 | TYPE `r bad!*` → ช่อง **รหัส Route** | I02 | ช่องแสดงค่าทดสอบ | ☐ |
| 4 | TYPE/SELECT remaining required fields ให้ถูก | A | พร้อม submit | ☐ |
| 5 | CLICK ปุ่ม **ยืนยันสร้าง** | — | drawerคงอยู่; เห็น field error code-format และ toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |

### TC-V03 — code ต่ำกว่า min 2 (boundary)
- group: Validation · ความสำคัญ: สูง · trace: BR-ST-04 / BR_ROUTE_CODE_INVALID
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=— · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: I03
- ผ่านเมื่อ: 1 ตัวถูก reject

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | หน้าโหลด | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawer เปิด | ☐ |
| 3 | TYPE `R` → ช่อง **รหัส Route** | I03 | ช่องแสดง `R` | ☐ |
| 4 | TYPE/SELECT remaining required fields ให้ถูก | A | พร้อม submit | ☐ |
| 5 | CLICK ปุ่ม **ยืนยันสร้าง** | — | ไม่สร้าง Route; code field error ปรากฏ | ☐ |

### TC-V04 — code เกิน max 12 (boundary)
- group: Validation · ความสำคัญ: สูง · trace: BR-ST-04 / BR_ROUTE_CODE_INVALID
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=— · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: I04
- ผ่านเมื่อ: 13 ตัวถูก reject

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | หน้าโหลด | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawer เปิด | ☐ |
| 3 | TYPE `R-12345678901` → ช่อง **รหัส Route** | I04 | ช่องแสดงค่าทดสอบ | ☐ |
| 4 | TYPE/SELECT remaining required fields ให้ถูก | A | พร้อม submit | ☐ |
| 5 | CLICK ปุ่ม **ยืนยันสร้าง** | — | ไม่สร้าง Route; code field error ปรากฏ | ☐ |

### TC-V05 — code ซ้ำ tenant เดียวกัน (negative)
- group: Validation · ความสำคัญ: สูง · trace: BR-ST-04 / ERR_ROUTE_CODE_CONFLICT / EC-01
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 มี `R-BK-01`; production runner ต้องตรวจ response/audit · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: I05
- ผ่านเมื่อ: ไม่สร้าง record/audit success ซ้ำ; prototype แสดง generic field validation

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็น `R-BK-01` เดิมหนึ่งแถว | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawer เปิด | ☐ |
| 3 | TYPE `R-BK-01` → ช่อง **รหัส Route** | I05 | ช่องแสดง duplicate | ☐ |
| 4 | TYPE/SELECT remaining required fields ให้ถูก | A | พร้อม submit | ☐ |
| 5 | CLICK ปุ่ม **ยืนยันสร้าง** | — | drawerคงอยู่; prototype แสดง code field error + toast **กรุณากรอกข้อมูลให้ครบถ้วน**; production API เป็น 409 `ERR_ROUTE_CODE_CONFLICT` | ☐ |
| 6 | VERIFY รายการหลังปิด drawer | — | `R-BK-01` ยังมีหนึ่ง record; ไม่มี success toast | ☐ |

### TC-V06 — name ว่างและ code immutable
- group: Validation · ความสำคัญ: สูง · trace: BR_REQUIRED_FIELD / BR_ROUTE_CODE_IMMUTABLE / AC-06
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=active `R-EDIT-01` · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: I06
- ผ่านเมื่อ: name ว่างถูกบล็อกและ code เปลี่ยนไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็น `R-EDIT-01` | ☐ |
| 2 | CLICK แถว `R-EDIT-01` | — | view drawer เปิด | ☐ |
| 3 | CLICK ปุ่ม **แก้ไข** | — | edit drawer เปิด; code locked | ☐ |
| 4 | TYPE ช่องว่าง → ช่อง **ชื่อ Route** | I06 | ช่องแสดงช่องว่าง | ☐ |
| 5 | CLICK ปุ่ม **บันทึกการแก้ไข** | — | drawerคงอยู่; error `ระบุชื่อ Route`; toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |

### TC-V07 — route_type นอก enum `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Validation · ความสำคัญ: สูง · trace: BR-ST-18 / BR_ROUTE_TYPE_INVALID / OQ-07
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=inject API-03 body route_type=`unknown_type`; native select ป้อนค่านี้ไม่ได้ · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: I07
- ผ่านเมื่อ: production contract reject; prototype enum ยังคง 10 ค่าเท่านั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | หน้าโหลด | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | dropdown **ประเภท** แสดงเฉพาะ 10 ค่าจาก HTML | ☐ |
| 3 | VERIFY dropdown **ประเภท** | — | ไม่มี `unknown_type` ให้เลือก | ☐ |
| 4 | OPEN API test harness สำหรับ API-03 | I07 | response 422 `BR_ROUTE_TYPE_INVALID`; ไม่มี record/audit success | ☐ |

### TC-V08 — region นอก enum `(ต้อง simulate)`
- group: Validation · ความสำคัญ: สูง · trace: BR-ST-08 / BR_REGION_INVALID
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=inject API-03 region=`ภาคที่ไม่มีจริง` · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: I08
- ผ่านเมื่อ: UI ไม่มีค่านอก enumและ API reject

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | หน้าโหลด | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | dropdown **ภาค** เปิดได้ | ☐ |
| 3 | VERIFY dropdown **ภาค** | — | เห็น 10 region รวม **ภาคกลาง** และ **ส่วนกลาง / ออนไลน์**; ไม่มีค่าทดสอบผิด | ☐ |
| 4 | OPEN API test harness สำหรับ API-03 | I08 | response 422 `BR_REGION_INVALID`; ไม่มี record | ☐ |

### TC-V09 — province นอก dataset: contract vs prototype drift D-02 `(ต้อง simulate)`
- group: Validation · ความสำคัญ: สูง · trace: BR-ST-06/07 / BR_PROVINCE_INVALID / D-02
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=code ใหม่; production API harness พร้อม · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: I09
- ผ่านเมื่อ: บันทึก observation แยกจาก contract; ไม่ฟันธง defectก่อน decision

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | หน้าโหลด | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawer เปิด | ☐ |
| 3 | TYPE `จังหวัดที่ไม่มีจริง` → ช่อง **จังหวัด** | I09 | dropdown แสดง `ไม่พบจังหวัด "จังหวัดที่ไม่มีจริง" ในชุดข้อมูลระบบ` | ☐ |
| 4 | VERIFY current prototype ก่อน submit | — | ช่องยังอาจคงข้อความที่พิมพ์: **Prototype observation D-02** | ☐ |
| 5 | OPEN API test harness สำหรับ API-03 ด้วย province invalid | I09 | **Production contract** ตอบ 422 `BR_PROVINCE_INVALID`; ไม่มี record/audit success | ☐ |

### TC-V10 — salesperson ว่าง: contract vs prototype drift D-01
- group: Validation · ความสำคัญ: สูง · trace: AC-13 / BR-ST-02/03 / EC-03 / D-01
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=code ใหม่; Salesperson provider ไม่มี · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: valid required + salesperson blank
- ผ่านเมื่อ: เก็บ evidence ทั้งสองชั้นและไม่สร้าง hard dependency

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | หน้าโหลด | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawer เปิด; label salesperson มี `*` ตาม prototype | ☐ |
| 3 | TYPE/SELECT required fields ยกเว้น salesperson | code `R-NOREP-01` | salesperson ว่าง | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันสร้าง** | — | **Prototype observation D-01:** drawerคงอยู่; error `เลือกพนักงานขายจากทะเบียน Sales Team / Salesperson`; toast generic | ☐ |
| 5 | OPEN API test harness สำหรับ API-03 ด้วย `salesperson_ref:null` | — | **Production contract:** บันทึกได้โดยไม่มี provider request; record มี ref null | ☐ |

### TC-V11 — salesperson_ref structural invalid `(ต้อง simulate)`
- group: Validation · ความสำคัญ: สูง · trace: BR-ST-02/03 / BR_SALESPERSON_REF_INVALID
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=API harness body ref ยาว >100; provider absent · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: I10
- ผ่านเมื่อ: structural invalid ถูก reject โดยไม่ resolve provider

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN API test harness สำหรับ API-03 | I10 | request ส่ง opaque ref เกิน schema | ☐ |
| 2 | VERIFY response | — | 422 structural reference error; ไม่มี outbound call ไป Salesperson และไม่มี record | ☐ |

### TC-V12 — universe ติดลบ: contract vs prototype drift D-03 `(ต้อง simulate)`
- group: Validation · ความสำคัญ: สูง · trace: BR_UNIVERSE_INVALID / D-03
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=code ใหม่; API harness พร้อม · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: I11
- ผ่านเมื่อ: prototype coercion ถูกบันทึกเป็น observation; contract reject

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | หน้าโหลด | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawer เปิด | ☐ |
| 3 | TYPE/SELECT valid fields แล้ว TYPE `-1` → **ร้านในเขต (universe)** | I11 | input แสดงค่าหรือ browser constraint ตาม environment | ☐ |
| 4 | VERIFY current prototype submit behavior | — | **Prototype observation D-03:** code path clamp เป็น 0; บันทึก evidence ไม่ตีความเป็น approved rule | ☐ |
| 5 | OPEN API test harness สำหรับ API-03 universe=-1 | I11 | **Production contract:** 422 `BR_UNIVERSE_INVALID`; ไม่มี record | ☐ |

### TC-V13 — universe ทศนิยม: contract vs prototype drift D-03 `(ต้อง simulate)`
- group: Validation · ความสำคัญ: สูง · trace: BR_UNIVERSE_INVALID / D-03
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=code ใหม่; API harness พร้อม · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: I12
- ผ่านเมื่อ: contract ไม่ silently truncate

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | หน้าโหลด | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawer เปิด | ☐ |
| 3 | TYPE `1.5` → **ร้านในเขต (universe)** | I12 | input แสดง/จำกัดค่าตาม browser; บันทึก actual | ☐ |
| 4 | VERIFY current prototype behavior | — | **Prototype observation D-03:** `parseInt` อาจได้ 1; ไม่ถือเป็น contract | ☐ |
| 5 | OPEN API test harness สำหรับ API-03 universe=1.5 | I12 | **Production contract:** 422 `BR_UNIVERSE_INVALID`; ไม่มี record | ☐ |

### TC-V14 — list query/pagination ผิด `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Validation/API · ความสำคัญ: กลาง · trace: ERR_INVALID_QUERY / API-01
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=API harness; query `limit=101&offset=-1&status=bad` · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: invalid query
- ผ่านเมื่อ: 400 และไม่คืนข้อมูลข้าม scope

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN API test harness สำหรับ API-01 ด้วย invalid query | `limit=101&offset=-1&status=bad` | response 400 `ERR_INVALID_QUERY` ตาม error envelope | ☐ |
| 2 | VERIFY response body | — | ไม่มี Route data; มี correlation_id opaque; ไม่มี PII | ☐ |

### TC-V15 — required type/region หาย `(ต้อง simulate)`
- group: Validation/API · ความสำคัญ: สูง · trace: BR_REQUIRED_FIELD / BR_ROUTE_TYPE_INVALID / BR_REGION_INVALID
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=API harness; native selects ไม่สามารถว่างด้วย UI · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: body ตัด route_type แล้วรอบสองตัด region
- ผ่านเมื่อ: แต่ละ required field ถูก reject อิสระ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN API test harness สำหรับ API-03 โดยไม่มี `route_type` | valid remaining | 422 field error `BR_REQUIRED_FIELD`/`BR_ROUTE_TYPE_INVALID`; ไม่มี record | ☐ |
| 2 | OPEN API test harness สำหรับ API-03 โดยไม่มี `region` | valid remaining | 422 field error `BR_REQUIRED_FIELD`/`BR_REGION_INVALID`; ไม่มี record | ☐ |

### Group L — Lifecycle, Atomicity and Resilience

### TC-L01 — archive modal dismiss ทุกทาง
- group: Lifecycle/Overlay · ความสำคัญ: สูง · trace: AC-07 / S-07
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=active `R-ARC-01` · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยกเลิก/X/backdrop/Esc ไม่ mutate

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็น `R-ARC-01` pill **ใช้งาน** | ☐ |
| 2 | CLICK action **เก็บเข้าคลัง** ของแถว | — | modal title **เก็บ Route เข้าคลัง** เปิด | ☐ |
| 3 | CLICK ปุ่ม **ยกเลิก** | — | modal ปิด; Route ยัง **ใช้งาน** | ☐ |
| 4 | CLICK action **เก็บเข้าคลัง** แล้ว PRESS Esc | — | modal ปิดก่อน drawer; Route ยัง **ใช้งาน** | ☐ |
| 5 | CLICK action **เก็บเข้าคลัง** แล้ว CLICK backdrop นอก card | — | modal ปิด; Route ยัง **ใช้งาน** | ☐ |
| 6 | CLICK action **เก็บเข้าคลัง** แล้ว CLICK ไอคอน X | — | modal ปิด; ไม่มี success toast | ☐ |

### TC-L02 — archive สำเร็จพร้อม warning/audit
- group: Lifecycle · ความสำคัญ: สูง · trace: AC-07 / BR-ST-09/10 / EC-05/07 / API-05
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S2 active Route A customer fixture >0 version current · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: S2
- ผ่านเมื่อ: status archived, toast exact, no delete, audit appended

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | Route A แสดง pill **ใช้งาน** | ☐ |
| 2 | CLICK action **เก็บเข้าคลัง** ของ Route A | — | modalอธิบายผลย้อนหลังและ warning `เขตนี้มีลูกค้า {n} ราย ผูกอยู่ — ควรย้ายลูกค้าไป Route อื่นก่อน (ทำที่ทะเบียน Customer)` | ☐ |
| 3 | CLICK ปุ่ม **เก็บเข้าคลัง** | — | ปุ่ม disabled แสดง **กำลังบันทึก…** | ☐ |
| 4 | WAIT จนสำเร็จ | ≤3s | toast `เก็บ Route {code} เข้าคลังแล้ว` | ☐ |
| 5 | SELECT **เก็บเข้าคลัง** → ตัวกรองสถานะ | — | Route A ยังอยู่ด้วย pill **เก็บเข้าคลัง**; ไม่ถูก hard delete | ☐ |
| 6 | VERIFY production audit evidence ผ่าน authorized harness | — | มี audit action archived หนึ่งรายการ actor/time/result และ before/after; Route row ยังมีอยู่ | ☐ |

### TC-L03 — restore สำเร็จพร้อม audit
- group: Lifecycle · ความสำคัญ: สูง · trace: AC-08 / BR-ST-09/10 / EC-07 / API-06
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S3 archived Route no conflict · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: S3
- ผ่านเมื่อ: active, toast exact, audit one

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | หน้า default active | ☐ |
| 2 | SELECT **เก็บเข้าคลัง** → ตัวกรองสถานะ | — | เห็น archived seed | ☐ |
| 3 | CLICK action **กู้คืน** ของ archived seed | — | toast `กู้คืน Route {code} แล้ว` | ☐ |
| 4 | SELECT **ใช้งาน** → ตัวกรองสถานะ | — | Route เดิมกลับมาพร้อม pill **ใช้งาน** | ☐ |
| 5 | VERIFY production audit evidence ผ่าน authorized harness | — | มี restored audit หนึ่งรายการและ version เพิ่ม | ☐ |

### TC-L04 — state transition ผิด `(ต้อง simulate)`
- group: Lifecycle · ความสำคัญ: สูง · trace: BR_INVALID_STATE_TRANSITION / state machine
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=active A + archived B; API harness · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: archive B; restore A
- ผ่านเมื่อ: ทั้งสอง transition ผิดถูก rejectและ stateเดิมคงอยู่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN API test harness แล้วส่ง API-05 ให้ archived B | current version | 422 `BR_INVALID_STATE_TRANSITION`; B ยังคง archived | ☐ |
| 2 | OPEN API test harness แล้วส่ง API-06 ให้ active A | current version | 422 `BR_INVALID_STATE_TRANSITION`; A ยังคง active | ☐ |

### TC-L05 — ไม่มี hard delete/approval/DOA
- group: Scope Lock · ความสำคัญ: สูง · trace: AC-14 / BR-ST-09/14 / LOCK-03/04
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: UI/lifecycle/API inventory ไม่มีสิ่ง OOS

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็นเฉพาะ create/edit/archive/restore/view; ไม่มี **ลบ**, **ส่งอนุมัติ**, **อนุมัติ**, **ปฏิเสธ** | ☐ |
| 2 | CLICK แถว active | — | view drawer ไม่มี delete/approval action | ☐ |
| 3 | VERIFY production API inventory ผ่าน harness | — | มี API-01–06; ไม่มี DELETE และไม่มี approval/DOA endpoint/state | ☐ |

### TC-L06 — audit write fail rollback `(ต้อง simulate)`
- group: Atomicity · ความสำคัญ: สูง · trace: ERR_AUDIT_WRITE_FAILED / BR-ST-10 / FN-08
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=inject audit INSERT failure สำหรับ create/edit/archive/restore ทีละรอบ; จด record/version/status ก่อน · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: A + existing route
- ผ่านเมื่อ: ไม่มี partial mutationทุก action

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY และบันทึก record/version/status ตั้งต้น | — | มีค่าฐานสำหรับเทียบ | ☐ |
| 2 | OPEN API test harness แล้ว submit create ขณะ audit fail | A | 500 `ERR_AUDIT_WRITE_FAILED`; ไม่มี Route ใหม่ | ☐ |
| 3 | OPEN API test harness แล้ว submit edit ขณะ audit fail | C | 500; existing values/version เท่าค่าฐาน | ☐ |
| 4 | OPEN API test harness แล้ว submit archive ขณะ audit fail | — | 500; status/version เท่าค่าฐาน | ☐ |
| 5 | OPEN API test harness แล้ว submit restore ขณะ audit fail | — | 500; archived status/version เท่าค่าฐาน | ☐ |

### TC-L07 — stale concurrent edit `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Concurrency · ความสำคัญ: กลาง · trace: AC-16 / PR-2 / ERR_STALE_DATA / OQ-16
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=Route version=5; client A/B โหลด version=5 · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: A edits name X; B edits name Y
- ผ่านเมื่อ: first wins; second 409; UIรักษาค่าเพื่อ reload

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY และบันทึก Route version/name ฐาน | version=5 | จดฐาน version=5 | ☐ |
| 2 | OPEN API harness client A แล้ว PATCH If-Match=5 | name X | 200; version=6; auditหนึ่งรายการ | ☐ |
| 3 | OPEN API harness client B แล้ว PATCH If-Match=5 | name Y | 409 `ERR_STALE_DATA`; ไม่มี lost update/audit successเพิ่ม | ☐ |
| 4 | VERIFY drawer client B | — | ค่าที่กรอกยังอยู่และมีคำขอ reload ⚠ ยืนยัน anchor; prototype-only run ให้ blocked | ☐ |

### TC-L08 — permission revoked mid-flight `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Security · ความสำคัญ: สูง · trace: AC-17 / PR-3 / ERR_PERMISSION_REVOKED
- actor (role): Sales Admin then revoked
- Setup: role=sales_admin · seed=active Route; revoke roleหลังเปิด editก่อน save · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: C
- ผ่านเมื่อ: 403; no mutation/audit success

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | mutation actions visibleก่อน revoke | ☐ |
| 2 | CLICK แถว Route แล้ว CLICK **แก้ไข** | — | edit drawer เปิด | ☐ |
| 3 | TYPE `ทดสอบหลังถอนสิทธิ์` → **ชื่อ Route** | — | unsaved value visible | ☐ |
| 4 | VERIFY runner ถอน role ของ session | — | session ไม่มี mutation authority | ☐ |
| 5 | CLICK ปุ่ม **บันทึกการแก้ไข** | — | server 403 `ERR_PERMISSION_REVOKED`; ไม่มี success toast; persisted value/version/audit success ไม่เปลี่ยน | ☐ |

### TC-L09 — retry same idempotency key/body `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Idempotency · ความสำคัญ: สูง · trace: AC-18 / PR-4/07
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=code ใหม่; API harness drop first responseหลัง commit; key=`11111111-1111-4111-8111-111111111111` · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: A with unique code `R-IDEM-01`
- ผ่านเมื่อ: cached result; one Route/audit

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN API harness แล้ว POST API-03 ด้วย key/body | A | server commit แต่ response ถูก dropตาม injection | ☐ |
| 2 | OPEN API harness แล้ว retry key/body เดิม | A | ได้ cached 201/record เดิม | ☐ |
| 3 | VERIFY persisted Route/audit | — | มี `R-IDEM-01` หนึ่ง recordและ created auditหนึ่งรายการ | ☐ |

### TC-L10 — same key different body `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Idempotency · ความสำคัญ: สูง · trace: AC-18 / ERR_IDEMPOTENCY_CONFLICT
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=idempotency key ถูกใช้กับ body A แล้ว · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: same key + name changed
- ผ่านเมื่อ: 409; original unchanged

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY และบันทึก original record/audit count | — | จดค่าฐาน | ☐ |
| 2 | OPEN API harness แล้ว POST key เดิมแต่ body ต่าง | changed name | 409 `ERR_IDEMPOTENCY_CONFLICT` | ☐ |
| 3 | VERIFY original record/audit | — | เท่าค่าฐาน step 1; ไม่มี mutation/audit successใหม่ | ☐ |

### TC-L11 — restore code conflict `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Lifecycle · ความสำคัญ: สูง · trace: AC-19 / ERR_RESTORE_CODE_CONFLICT / OQ-20
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=archived Route code conflictตาม migration/test injection; version current · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: conflict seed
- ผ่านเมื่อ: 409 และยัง archived

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY archived status/version ฐาน | — | จดค่าฐาน | ☐ |
| 2 | OPEN API harness แล้ว POST restore | current If-Match/key | 409 `ERR_RESTORE_CODE_CONFLICT` | ☐ |
| 3 | VERIFY Route หลัง response | — | status/version เท่าค่าฐาน; ไม่มี restored audit success | ☐ |

### TC-L12 — Route not found `(ต้อง simulate)`
- group: API · ความสำคัญ: สูง · trace: ERR_ROUTE_NOT_FOUND / API-02/04/05/06
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=UUID ที่ไม่มีจริง · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: missing UUID
- ผ่านเมื่อ: ทุก API record-specific ไม่สร้างผลข้างเคียง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN API-02 ด้วย missing UUID | — | 404 `ERR_ROUTE_NOT_FOUND` | ☐ |
| 2 | OPEN API-04 ด้วย missing UUID | — | 404; ไม่มี audit | ☐ |
| 3 | OPEN API-05 ด้วย missing UUID | — | 404; ไม่มี audit | ☐ |
| 4 | OPEN API-06 ด้วย missing UUID | — | 404; ไม่มี audit | ☐ |

### TC-L13 — unauthenticated ทุก API `(ต้อง simulate)`
- group: Security · ความสำคัญ: สูง · trace: ERR_NOT_AUTHENTICATED / all APIs
- actor (role): anonymous
- Setup: role=anonymous · seed=remove/expire session token · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 401 และไม่เปิดเผย data/PII

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` โดยไม่มี session | — | ไม่เห็น Route master data; ถูกส่ง/แสดง auth stateตาม platform ⚠ ยืนยัน anchor | ☐ |
| 2 | OPEN API-01 ถึง API-06 โดยไม่มี auth ผ่าน harness | — | ทุก request ตอบ 401 `ERR_NOT_AUTHENTICATED`; ไม่มี mutation/audit success | ☐ |

### Group P — Permission and Security

### TC-P01 — sales_admin 6 cells = allow
- group: Permission · ความสำคัญ: สูง · trace: permission matrix sales_admin
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1 + unique create code · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: A
- ผ่านเมื่อ: View/Create/Edit/Archive/Restore/Workload-Map มี authority

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | list/detail accessible | ☐ |
| 2 | VERIFY ปุ่ม **สร้างเขต** และ row actions | — | เห็น create/edit/archive; archived filterมี restore | ☐ |
| 3 | CLICK แท็บ **ภาระงาน** | — | เข้าถึง read-only tab | ☐ |
| 4 | CLICK แท็บ **แผนที่** | — | เข้าถึง map tab | ☐ |
| 5 | VERIFY API authorization harness สำหรับ API-01–06 | — | ไม่ได้ 401/403 เมื่อ requestถูกต้อง | ☐ |

### TC-P02 — system_admin 6 cells = allow
- group: Permission · ความสำคัญ: สูง · trace: permission matrix system_admin
- actor (role): System Admin
- Setup: role=system_admin · seed=S1 · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: authority เทียบ sales_admin

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | list/detail accessible | ☐ |
| 2 | VERIFY ปุ่มและแท็บ | — | เห็น create/edit/archive/restoreและ workload/map | ☐ |
| 3 | VERIFY API authorization harness สำหรับ API-01–06 | — | requestถูกต้องไม่ถูก 403 | ☐ |

### TC-P03 — sales_manager hold + mutation deny `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Permission · ความสำคัญ: สูง · trace: OQ-02 / ERR_INSUFFICIENT_ROLE
- actor (role): Sales Manager
- Setup: role=sales_manager · seed=S1; permissionยัง hold ต้อง configure runnerตาม current release deny mutation · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 4 mutation cells deny; view/workload-map recorded blocked/allowedตาม approved OQ, ไม่เดา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | ถ้า OQ-02 ยังไม่ปิด ให้ mark view cell `blocked`; ห้ามถือ prototype visibilityเป็นสิทธิ์ | ☐ |
| 2 | VERIFY mutation actions | — | production UI ซ่อน create/edit/archive/restore หรือ serverจะ deny | ☐ |
| 3 | OPEN API-03/04/05/06 ผ่าน harness | — | ทุก mutation 403 `ERR_INSUFFICIENT_ROLE`; ไม่มี audit success | ☐ |
| 4 | CLICK แท็บ **ภาระงาน** และ **แผนที่** เมื่อได้รับ view permission | — | หาก OQ ยัง hold ให้ `blocked`; หากอนุมัติ viewer จึงเห็น read-only | ☐ |

### TC-P04 — salesperson hold + mutation deny `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Permission · ความสำคัญ: สูง · trace: OQ-02 / ERR_INSUFFICIENT_ROLE
- actor (role): Salesperson
- Setup: role=salesperson · seed=S1; own-scope policyยัง hold · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: mutation deny; read/own-scopeไม่ถูกเดา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | หาก OQ-02 ยังไม่ปิดให้ mark view `blocked`; ไม่มีการเปิดเผย all-scopeโดยสมมติ | ☐ |
| 2 | VERIFY mutation actions | — | create/edit/archive/restore ซ่อนหรือ server deny | ☐ |
| 3 | OPEN API-03/04/05/06 ผ่าน harness | — | 403 `ERR_INSUFFICIENT_ROLE`; ไม่มี mutation | ☐ |
| 4 | CLICK แท็บ **ภาระงาน** และ **แผนที่** เมื่อ permissionอนุมัติ | — | own-scope behaviorต้องตรง decision; หากยัง hold ให้ `blocked` | ☐ |

### TC-P05 — tenant isolation `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Security · ความสำคัญ: สูง · trace: OQ-FRD-01 / tenant isolation
- actor (role): Sales Admin tenant A
- Setup: role=sales_admin tenant=A · seed=S4 same codeใน tenants A/B + route id B · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: S4
- ผ่านเมื่อ: tenant A ไม่เห็น/แก้ B; uniqueness scoped tenant

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` as tenant A | — | listมีเฉพาะ records tenant A | ☐ |
| 2 | OPEN API-02 ด้วย route id tenant B | — | 404/emptyตาม canonical platform contract; ไม่มี B data/PII | ☐ |
| 3 | OPEN API-04/05/06 ด้วย route id tenant B | — | ไม่ mutate B; responseไม่เปิดเผยข้อมูล | ☐ |
| 4 | OPEN API-03 tenant A ด้วย codeที่มีเฉพาะ tenant B | — | uniquenessไม่ conflictข้าม tenant | ☐ |

### TC-P06 — minimum response และ PII visibility `(ต้อง simulate)`
- group: Security · ความสำคัญ: สูง · trace: D-CLASS / salesperson_ref actor IDs
- actor (role): Authorized Sales Admin
- Setup: role=sales_admin · seed=Routeมี salesperson_refและ audit actor · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: authorized responseเท่าที่จำเป็น; future provider dataไม่ปน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN API-02 ผ่าน authorized harness | — | responseมี owned Route + audit_summaryขั้นต่ำ; ไม่มี Customer/Order/Target/Visit live payload | ☐ |
| 2 | VERIFY view drawer | — | แสดง salesperson label/แก้ไขล่าสุดตามสิทธิ์ แต่ไม่แสดง raw actor UUID/รายละเอียดบุคคลเกินจำเป็น | ☐ |

### TC-P07 — operational logs ไม่มี raw PII `(ต้อง simulate)`
- group: Security · ความสำคัญ: สูง · trace: D-CLASS / BR-ST-20
- actor (role): Security QA
- Setup: role=security_qa · seed=execute create/edit with salesperson_ref; access sanitized test logs · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: A
- ผ่านเมื่อ: logsไม่มี raw display name/body/PII; audit protectedแยก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN test log viewerหลัง mutation | — | operational logไม่มีชื่อพนักงาน/raw personal body; correlation_idเป็น opaque | ☐ |
| 2 | VERIFY protected auditผ่าน authorized channel | — | before/afterมี classification Confidentialและไม่เปิดให้ roleทั่วไป | ☐ |

### TC-P08 — denied/revoked mutation ไม่มี success audit `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Security · ความสำคัญ: สูง · trace: ERR_PERMISSION_REVOKED / audit atomicity
- actor (role): Revoked user
- Setup: role=revoked · seed=จด Route value/version/audit count · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: C
- ผ่านเมื่อ: persisted stateและ success-auditเท่าเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY และบันทึก Route value/version/audit count ฐาน | — | จดค่าฐาน | ☐ |
| 2 | OPEN API-04 ด้วย revoked credential | C | 403 `ERR_PERMISSION_REVOKED` | ☐ |
| 3 | VERIFY Route และ success audit | — | เท่าค่าฐาน step 1; security denialอาจอยู่ platform auditแยก | ☐ |

### Group X — Map, Future Hooks and Scope Safeguards

### TC-X01 — offline local map
- group: Map · ความสำคัญ: สูง · trace: AC-11 / BR-ST-07/20 / US-08
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=S1; block external networkหลังโหลด app bundleแต่คง local/inline assets · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: local THMAP 77 provinces
- ผ่านเมื่อ: mapและ core masterใช้งานได้โดยไม่ต้อง external map service

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` ขณะ offline | — | หน้า **ผังเขตขาย** และแท็บ **โครงสร้างเขต** ใช้งานได้ | ☐ |
| 2 | CLICK แท็บ **แผนที่** | — | แผนที่ประเทศไทย renderจาก local/inline asset; ไม่มี critical external map failure | ☐ |
| 3 | CLICK แท็บ **โครงสร้างเขต** | — | list/create/viewยังใช้งานได้ | ☐ |

### TC-X02 — local geo asset corrupt `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Map · ความสำคัญ: กลาง · trace: AC-11 / OQ-19 / BR-ST-20
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=inject corrupt/missing geo assetใน production-wired build · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: corrupt asset
- ผ่านเมื่อ: contained errorเฉพาะ map; structure CRUDยังอยู่; exact copyยัง OQ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | Structure listยัง render | ☐ |
| 2 | CLICK แท็บ **แผนที่** | — | เห็น contained map error ⚠ ยืนยัน anchor; หน้าไม่ crash | ☐ |
| 3 | CLICK แท็บ **โครงสร้างเขต** | — | ค้นหาและปุ่ม **สร้างเขต** ยังใช้ได้ | ☐ |

### TC-X03 — valid map hover/select
- group: Map · ความสำคัญ: สูง · trace: AC-12 / BR-ST-19 / US-08
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=active Routeในจังหวัดที่มี interactive path/pin · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: จังหวัด interactive
- ผ่านเมื่อ: valid targetเท่านั้นอัปเดต tooltip/panel/selectionสัมพันธ์กัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | หน้าโหลด | ☐ |
| 2 | CLICK แท็บ **แผนที่** | — | เห็น map canvasและ side panel | ☐ |
| 3 | VERIFY pointer hoverบนจังหวัด interactive ภายในกรอบ | — | จังหวัด highlight; tooltip/panelแสดงชื่อจังหวัดเดียวกัน | ☐ |
| 4 | CLICK จังหวัด interactive ที่ hover | — | selectionถูกตรึง; side panelมีข้อความ `(คลิกเพื่อตรึง)` เฉพาะตอน hoverก่อน clickและมี **ยกเลิกการเลือก** หลัง select | ☐ |
| 5 | CLICK ปุ่ม **ยกเลิกการเลือก** | — | selectionหายและ panelกลับ overview | ☐ |

### TC-X04 — pointer นอก 4 ด้าน/4 มุม/side list ไม่ trigger (edge: EC-08)
- group: Map · ความสำคัญ: สูง · trace: AC-12 / BR-ST-19 / LOCK-08 / EC-08
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=active province selected; runnerจับชื่อ panel/selectionฐาน · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: 9 pointer samples
- ผ่านเมื่อ: ทุก sampleนอก frameไม่สร้าง hover/tooltip/selection/stateใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` แล้ว CLICK แท็บ **แผนที่** | — | mapพร้อม | ☐ |
| 2 | CLICK จังหวัด interactive หนึ่งจังหวัด | — | จด selected province/panelเป็นฐาน | ☐ |
| 3 | VERIFY pointer เลยขอบบน กลางบน | — | ไม่มี tooltipใหม่; selected/panelเท่าฐาน | ☐ |
| 4 | VERIFY pointer เลยขอบล่าง กลางล่าง | — | ไม่มี state mutation | ☐ |
| 5 | VERIFY pointer เลยขอบซ้าย กลางซ้าย | — | ไม่มี state mutation | ☐ |
| 6 | VERIFY pointer เลยขอบขวา กลางขวา | — | ไม่มี state mutation | ☐ |
| 7 | VERIFY pointerเลยมุมซ้ายบน/ขวาบน/ซ้ายล่าง/ขวาล่างทีละจุด | — | ทั้งสี่จุดไม่แสดง tooltip/highlightใหม่; selectionคงฐาน | ☐ |
| 8 | VERIFY pointerบนรายการด้านข้างนอก map canvas | — | side list hoverไม่สั่ง map hover/tooltip; selectionคงฐาน | ☐ |
| 9 | VERIFY pointerออกนอกกรอบทั้งหมด | — | tooltipซ่อน; ไม่มีจังหวัดใหม่ถูกเลือก | ☐ |

### TC-X05 — workload mock/read-only `[AI-DEFAULT]`
- group: Future data · ความสำคัญ: สูง · trace: AC-10 / BR-ST-11/17 / XT-03 / OQ-06
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=fixture reps/routes; block all future provider network · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: fixture workload
- ผ่านเมื่อ: read-only prototypeแสดงสูตรแต่ไม่อ้างว่า productionและไม่ block core

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | core listโหลด | ☐ |
| 2 | CLICK แท็บ **ภาระงาน** | — | เห็นตาราง read-only, labels `รับได้`/`ตึงมือ`/`เกินกำลัง`หรือ `งานแพลตฟอร์ม`ตาม fixture | ☐ |
| 3 | VERIFY ข้อความสูตรใต้ตาราง | — | แสดงสูตร F4×4/F2×2/F1×1 และ capacities ตรง HTML; ถือเป็น `[AI-DEFAULT]` prototypeเท่านั้น | ☐ |
| 4 | VERIFY network/provider harness | — | ไม่มี callไป Customer/Sales Order/Target/Salesperson | ☐ |

### TC-X06 — coverage threshold/derived values ไม่เป็น production truth `[AI-DEFAULT]`
- group: Future data · ความสำคัญ: กลาง · trace: BR-ST-11/16 / EC-06 / OQ-04
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=fixture universe/customer; providerไม่มี · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: fixture coverage
- ผ่านเมื่อ: ค่าเป็น mock/read-only; ไม่มี persistence/API mutation

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็น KPI **Coverage** จาก fixture | ☐ |
| 2 | VERIFY ค่า/สี coverage | — | บันทึก actual prototype; threshold 25%ถูก tag `[AI-DEFAULT]` ไม่ใช้เป็น production acceptanceนอกเคสนี้ | ☐ |
| 3 | VERIFY API/network harness | — | ไม่มี coverage engine/persistence/provider call | ☐ |

### TC-X07 — Salesperson provider absent/inactive unknown (XT-01) `[AI-DEFAULT]`
- group: Cross-module · ความสำคัญ: สูง · trace: XT-01 / EC-03/04/10 / BR-ST-03/20 / D-01
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=Salesperson module/endpointไม่มี; prototype fixturesมี; API accepts nullable ref · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: null ref + fixture ref
- ผ่านเมื่อ: coreไม่ call provider; inactive policyไม่ถูกเดา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | core listทำงานแม้ providerไม่มี | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | prototype comboboxแสดง fixtureและข้อความอ้าง future; ไม่มี network call | ☐ |
| 3 | TYPE `ไม่มีคนนี้` → ช่อง **พนักงานขายผู้รับผิดชอบ** | — | empty text `ไม่พบ "ไม่มีคนนี้" ในทะเบียนพนักงานขาย — เพิ่มคนใหม่ที่ Sales Team / Salesperson` | ☐ |
| 4 | VERIFY production API create nullable ref ผ่าน harness | — | core saveได้โดยไม่มี provider; D-01 UI requiredถูกบันทึกเป็น drift | ☐ |
| 5 | VERIFY inactive/deleted future ref behavior | — | mark `blocked` pending OQ-03; ระบบไม่ block silentlyด้วยกฎที่ไม่ได้อนุมัติ | ☐ |

### TC-X08 — Customer provider absentตอน archive (XT-02)
- group: Cross-module · ความสำคัญ: สูง · trace: XT-02 / EC-05/10 / BR-ST-13
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=active Route; Customer providerไม่มี; fixture countอาจมีหรือไม่มี · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: S2
- ผ่านเมื่อ: archiveไม่ถูก blockหรือ call provider

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | core listโหลด | ☐ |
| 2 | CLICK action **เก็บเข้าคลัง** ของ active Route | — | modalเปิด; ถ้า fixture count>0แสดง warning count, ถ้าไม่มี providerยังเปิดได้ | ☐ |
| 3 | CLICK ปุ่ม **เก็บเข้าคลัง** | — | archiveสำเร็จและ toastปรากฏ; ไม่มี Customer network call | ☐ |

### TC-X09 — Customer future hook warning ไม่มี navigation/API
- group: Cross-module · ความสำคัญ: สูง · trace: US-09 / BR-ST-11 / LOCK-05
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=active Route `R-BK-01`; Customer moduleไม่มี · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: warning exact, routeคงเดิม, no call

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็น `R-BK-01` | ☐ |
| 2 | CLICK แถว `R-BK-01` | — | view drawerเปิดและเห็นปุ่ม `ดูลูกค้าในเขต ({n})` | ☐ |
| 3 | CLICK ปุ่ม `ดูลูกค้าในเขต ({n})` | — | toast `ทะเบียนลูกค้ายังไม่พร้อม — ระบบจะใช้เขต R-BK-01 เป็นตัวกรองเมื่อเชื่อมต่อแล้ว` | ☐ |
| 4 | VERIFY route/network | — | URLยัง `#/sales-territory`; ไม่มี Customer API/navigation | ☐ |

### TC-X10 — Visit future hook warning ไม่มี navigation/API (XT-04)
- group: Cross-module · ความสำคัญ: สูง · trace: XT-04 / US-09 / LOCK-05
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=active Route `R-BK-01`; Visit moduleไม่มี · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: warning exact, no navigation/API

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็น Route | ☐ |
| 2 | CLICK แถว `R-BK-01` | — | view drawerเห็นปุ่ม **แผนเยี่ยมในเขต** | ☐ |
| 3 | CLICK ปุ่ม **แผนเยี่ยมในเขต** | — | toast `แผนเยี่ยมยังไม่พร้อม — ระบบจะส่งเขต R-BK-01 เมื่อเชื่อมต่อแล้ว` | ☐ |
| 4 | VERIFY route/network | — | URLคงเดิม; ไม่มี Visit API/navigation | ☐ |

### TC-X11 — ทุก workload provider absent ไม่ block core (XT-03)
- group: Cross-module · ความสำคัญ: สูง · trace: XT-03 / EC-10 / BR-ST-11/20
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=block Customer/Sales Order/Sales Target provider namesทั้งหมด · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: workloadยังเป็น fixture/unavailableและ CRUDทำงาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | Structure listโหลด | ☐ |
| 2 | CLICK แท็บ **ภาระงาน** | — | อ่าน fixture/mockได้; ไม่มี production metric claimหรือ provider errorที่ทำหน้าแตก | ☐ |
| 3 | CLICK แท็บ **โครงสร้างเขต** | — | ปุ่ม **สร้างเขต** และ row actionsยังพร้อม | ☐ |
| 4 | VERIFY network harness | — | ไม่มี outbound requestไปสาม provider | ☐ |

### TC-X12 — future snapshot ไม่เปลี่ยนย้อนหลัง (XT-05) `(ต้อง simulate)`
- group: Cross-module · ความสำคัญ: สูง · trace: XT-05 / BR-ST-12 / EC-09 / LOCK-06
- actor (role): Integration QA
- Setup: role=integration_qa · seed=S5 snapshot fixture `{code,name,type,region,province}` + Route masterก่อนแก้; consumerเป็น contract fixtureไม่ใช่ moduleจริง · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: C edit
- ผ่านเมื่อ: masterเปลี่ยนแต่ snapshotทั้งห้าค่า byte/value stable

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY และบันทึก snapshot fixtureห้าค่า + masterห้าค่าตั้งต้น | S5 | จดค่าฐาน snapshot/master | ☐ |
| 2 | OPEN `#/sales-territory` | — | เห็น Routeต้นทาง | ☐ |
| 3 | CLICK แถว Route แล้ว CLICK **แก้ไข** | — | edit drawerเปิด | ☐ |
| 4 | TYPE/SELECT ค่าชุด C แล้ว CLICK **บันทึกการแก้ไข** | C | toast **บันทึกการแก้ไขแล้ว**; masterแสดงค่าใหม่ | ☐ |
| 5 | VERIFY snapshot fixture ผ่าน contract harness | — | code/name/type/region/provinceทุกค่าตรงฐาน step 1; ไม่ถูก rewrite | ☐ |

### TC-X13 — archived Route excludedเฉพาะ new future choices `(ต้อง simulate)`
- group: Cross-module · ความสำคัญ: สูง · trace: BR-ST-13 / XT-05 / LOCK-05
- actor (role): Integration QA
- Setup: role=integration_qa · seed=consumer contract fixtureมี historical snapshot + choice list adapter stub; target modulesไม่ implement · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: active Route with snapshot
- ผ่านเมื่อ: archiveไม่แก้ history; active-choice contractไม่เสนอ archived

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY และบันทึก historical snapshot + active choice listฐาน | — | Routeอยู่ใน active choicesและ snapshotมีค่าฐาน | ☐ |
| 2 | OPEN API harness แล้ว archive Route | — | status archived | ☐ |
| 3 | VERIFY contract fixtureหลัง archive | — | historical snapshotเท่าฐาน; active choice listไม่เสนอ Route archived | ☐ |
| 4 | VERIFY runtime dependencies | — | ไม่มี endpoint/moduleปลายทางจริงถูกสร้างจากเคสนี้ | ☐ |

### TC-X14 — overlap allowed baseline `[AI-DEFAULT]`
- group: Business default · ความสำคัญ: กลาง · trace: AC-15 / BR-ST-15 / OQ-09
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=active Routeจังหวัดเดียวกับชุด D; codeใหม่; เลือก rep fixture · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: D overlap
- ผ่านเมื่อ: prototypeไม่ enforce overlap; ผล failอาจหมาย defaultไม่ approved

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` | — | เห็น existing Routeจังหวัดเป้าหมาย | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawerเปิด | ☐ |
| 3 | TYPE/SELECT ชุด D + required values | D | provinceซ้ำกับ existing | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันสร้าง** | — | ตาม `[AI-DEFAULT]` prototype สร้างได้; ไม่มี overlap warning/enforcement | ☐ |

### TC-X15 — external fonts failแต่ coreยังใช้ได้
- group: Resilience · ความสำคัญ: กลาง · trace: BR-ST-20 / AC-10
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=block fonts.googleapis.com, fonts.gstatic.com, api.fontshare.com · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: fallback fontไม่ทำให้ controlหาย/กดไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` ขณะ font hostsถูก block | — | ข้อความไทยอ่านได้ด้วย system fallback; layout/controlไม่หาย | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | drawerเปิดและ inputกดได้ | ☐ |
| 3 | PRESS Esc | — | drawerปิดตามปกติ | ☐ |

### TC-X16 — region/type fixture และ R-BK-01 boundary `[AI-DEFAULT]`
- group: Fixture/Scope Lock · ความสำคัญ: กลาง · trace: LOCK-10 / BR-ST-08/18 / OQ-07/14
- actor (role): Sales Admin
- Setup: role=sales_admin · seed=prototype approved fixtureมี `R-BK-01`; production seed environmentแยก · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: —
- ผ่านเมื่อ: prototypeเห็น central fixture/10 types; productionไม่ seedโดยอัตโนมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sales-territory` ใน prototype/UAT fixture env | — | เห็น `R-BK-01` จัดในกลุ่ม **ภาคกลาง** | ☐ |
| 2 | CLICK ปุ่ม **สร้างเขต** | — | **ประเภท** มี 10 ค่า HTMLและ **ภาค** มี **ภาคกลาง**/**ส่วนกลาง / ออนไลน์** | ☐ |
| 3 | OPEN production seed verification harness | — | ไม่มี `R-BK-01` จาก migration เว้น OQ-14ถูกอนุมัติ; type listยัง `[AI-DEFAULT]` pending OQ-07 | ☐ |

### Group Q — Performance Proposal

### TC-Q01 — list/search p95 10k Routes `(ต้อง simulate)` `[AI-DEFAULT]`
- group: Performance · ความสำคัญ: ต่ำ · trace: TC-PERF-01 / OQ-21 / proposed p95≤2s
- actor (role): Performance QA
- Setup: role=performance_qa · seed=tenantเดียว 10,000 Routes, 50 concurrent users, approved test environment; OQ-21ยัง pending · files=—
- Start: OPEN `#/sales-territory`
- ชุดข้อมูล: 10k fixture
- ผ่านเมื่อ: รายงาน p95เทียบ proposal; failไม่ถือ business defectจน OQ-21อนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN performance harness สำหรับ API-01/list | 10k/50 concurrent | เก็บ latency/errorโดยไม่ expose PII | ☐ |
| 2 | TYPE query code/name/province ผ่าน workload script/harness | representative mix | paginationถูกต้อง; accepted invalid/duplicate=0 | ☐ |
| 3 | VERIFY report p95 | — | รายงานเทียบ proposal ≤2sและระบุ `[AI-DEFAULT] OQ-21`; ไม่เปลี่ยน outer-page scroll contract | ☐ |

## วิธีที่ agent รัน (Run protocol)

1. รันทีละเคสแบบ independent: reset app/session/seedตาม `Setup`, เปิด `Start` ใหม่ทุกครั้ง และห้ามใช้ stateค้างจากเคสก่อน
2. ทำ Action ตามลำดับ; ทุก stepบันทึก `☐` เป็น pass/fail/blocked พร้อมข้อความ/route/ค่าที่เห็นจริง
3. เคส `(ต้อง simulate)` ต้อง injectตาม Setup. ถ้า runnerไม่มี API/network/DB/audit harness ให้ mark `blocked` ไม่ใช่ `pass` จากการเดา
4. เคส `[AI-DEFAULT]` ใช้พิสูจน์ defaultที่ยังรอ approval; failอาจเป็น defaultไม่ตรง business ไม่ใช่ defectโดยอัตโนมัติ
5. D-01–D-03 ให้บันทึก Prototype observation และ Production contractแยกกัน; ห้ามรวม verdictจน PM/BAเคาะ
6. Expected แบบ deltaต้องอ้างค่าฐานที่จดใน stepก่อน. เก็บ screenshot/log referenceใน `evidence` แต่ไม่ฝังภาพในไฟล์นี้
7. ห้ามสร้าง/ติดตั้ง/seed module Salesperson, Customer, Sales Order, Sales Target, Visit; ใช้ fixture/stub safeguardเท่านั้น

## Coverage Audit

| หมวด | covered / total | หมายเหตุ |
|---|---:|---|
| Acceptance Criteria | 20 / 20 | AC-01–20 |
| Existing inventory inputs | 18 / 18 | ทุกแถว §6.2 ถูก expand |
| Business rules | 20 / 20 | BR-ST-01–20 |
| Confirmed edge cases | 10 / 10 | EC-01–10 |
| Lane/default probes | 6 / 6 | stale, revoke, network retry, double submit, restore conflict, corrupt geo |
| Error codes | 18 / 18 | ทุก codeใน §5.6 |
| Validation fields/actions | 9 / 9 | รวม archive/restore action |
| Permission cells | 24 / 24 | 4 roles × 6 columns; hold cellsไม่เดา |
| Cross-Module XT | 5 / 5 | safeguards/contract fixture only |
| Scope Lock | 10 / 10 | LOCK-01–10 |
| UI/state families | 10 / 10 | route/tabs/list/loading/error/empty/drawer/modal/combo/map/toastรวมตาม ledger |
| Cross-cutting security/atomicity | 8 / 8 | auth/RBAC/tenant/PII/audit/idempotency/concurrency/asset integrity |
| Events/realtime | N/A | ไม่มี business event/WebSocketใน scope |

- Cross-Module (XT): **5/5**
- Scope Lock (LOCK): **10/10**
- **Manifest cross-check (FRD §0.12): ✅ 38/38** — stories 9/9 + rules 20/20 + confirmed edges 9/9
- Total detailed cases: **75**
- Action verb-tag audit: **0 violations / 313 step rows**
- Setup audit: **0 missing / 75 cases**

### ข้าม (พร้อมเหตุผล)

- Implement five future modules/endpoints/events — นอกขอบเขตใบเซ็น; ทดสอบเฉพาะ absence/hook/snapshot safeguards TC-X07–X13
- Hard delete, approval/DOA, multi-owner, GPS/route-line/full choropleth, overlap enforcement, import/export/bulk/PDF — นอกขอบเขต; TC-L05/X14ตรวจว่าไม่ถูกเพิ่ม
- Audit Trail business UI, monitoring/dashboard/report UI — ไม่อยู่ใน approved HTML; ใช้ authorized API/DB/ops harnessเฉพาะข้อควบคุมที่จำเป็น
- Sales Manager/Salesperson read/own-scope cells — OQ-02 hold; TC-P03/P04ต้อง blockedหรือรันตาม decisionที่แนบมา ห้ามสมมติ
- Exact copyของ API conflict/loading/error/access-denied/geo-contained error — HTMLไม่มี; ติด `⚠ ยืนยัน anchor` และใช้ error code/visual stateโดยไม่แต่งข้อความ

Verdict: **Coverage-ready with approved warnings/defaults explicitly isolated.** In-scope ledger coverage 100%; OOS ไม่มี implementation case.

## Result Report (schema)

```json
{
  "feature_id": "F-05",
  "run_at": "ISO_DATETIME",
  "environment": "prototype|uat|production-like",
  "results": [
    {
      "id": "TC-N01",
      "status": "pass|fail|blocked",
      "failed_step": null,
      "evidence": "",
      "note": ""
    }
  ],
  "drift_observations": [
    { "id": "D-01|D-02|D-03", "prototype": "", "contract": "", "decision": "pending|approved" }
  ],
  "summary": { "total": 75, "pass": 0, "fail": 0, "blocked": 0 }
}
```
