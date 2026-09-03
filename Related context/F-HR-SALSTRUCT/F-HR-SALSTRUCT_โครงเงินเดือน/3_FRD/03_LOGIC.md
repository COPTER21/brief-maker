# 03_LOGIC — F-HR-SALSTRUCT · Salary Structure (โครงเงินเดือน)

> **Audience:** BE dev (business logic layer)
> **Scope:** ทุก logic ที่ไม่ใช่ HTTP — pure function · state transition · การคำนวณ · validation · integration
> **R8:** ทุก mutation API ต้อง trace มาที่ Function/Engine ที่นี่ · ไม่มี Function/Engine ที่ไม่ถูกใช้ (ตรวจที่ §3.3)
> **Convention:** Function = `camelCase` (scope-local) · Engine = `kebab-case` (reusable · CUBIC)

## §3.1 Functions (Scope-Local) — 55 ฟังก์ชัน

### กลุ่ม A · กระบอก / เวอร์ชัน

| # | Function | Input → Output | ทำอะไร | บังคับกฎ | เรียกโดย |
|---|---|---|---|---|---|
| A1 | `createBandDraft` | `{grade, band, copyFromVersionId?, percentAdjust?}` → `{gradeId, versionId}` | สร้างระดับ (ถ้าใหม่) + ร่างเวอร์ชันกระบอกสถานะ `draft` | BR-01 | API-02 |
| A2 | `assertBandOrder` | `band[]` → `void \| BandOrderError{rows[]}` | ตรวจ `0 < min < mid < max` ทุกแถว **ตรวจซ้ำหลังปรับ %** | BR-01 · EC-24 | API-02 · API-03 · A3 |
| A3 | `applyPercentAdjust` | `{baseVersion, percent}` → `band[]` | คัดลอกเวอร์ชันเดิมแล้วปรับทุกระดับ · **ปัดเป็นหลักร้อย** (`[ASSUMED]` A9) → เรียก `assertBandOrder` ซ้ำ | BR-01 | API-02 |
| A4 | `assertVersionEditable` | `version` → `void \| Error` | อนุญาตแก้เฉพาะ `draft` — สถานะอื่น = `ERR_VERSION_NOT_EDITABLE` | **P-2′ · BR-02** | API-03 |
| A5 | `publishBandVersion` | `{versionId, effectiveDate, changeReason, reasons?}` → `version` | ประกาศ: ตรวจ overlap → งวดปิด → ค่าขั้นต่ำตามกฎหมาย → คำนวณ window → `scheduled` → ยิง E1 | BR-02, BR-03, BR-04, BR-23 | API-04 |
| A6 | `withdrawBandVersion` | `{versionId, cancelReason}` → `version` | `scheduled → cancelled` (บังคับเหตุผล) → ยิง E3 | BR-02 | API-05 |
| A7 | `deactivateGrade` | `{gradeId, reason, ackCount}` → `grade` | soft archive: `status='inactive'` · ต้องยืนยันจำนวนผู้ใช้ก่อน → ยิง E4 | BR-05, BR-22 | API-06 |
| A8 | `reactivateGrade` | `{gradeId, effectiveDate, reason}` → `version` | เปิดกลับ = **สร้างเวอร์ชันใหม่** `scheduled` (ไม่ย้อนสถานะ) | P-2′ | API-07 |
| A9 | `listVersionHistory` | `gradeId` → `version[]` | ประวัติทุกเวอร์ชัน + ผู้แก้ + เหตุผล (read-only) | BR-05 | API-08 |
| A10 | `buildVersionDiff` | `{fromId, toId}` → `rows[]` | ค่าเดิม → ค่าใหม่ → ส่วนต่าง → % ต่อระดับ · ระดับที่ไม่เปลี่ยนคืน `delta = 0` | — | API-09 |
| A11 | `resolveBandAt` | `{gradeId?, companyId, date}` → `band \| null` | **as-of read** — คืนเวอร์ชันที่ `active` ณ วันที่นั้น (ไม่ใช่คอลัมน์สถานะ) | P-6′ | API-01 · API-13 · API-24 · API-25 |
| A12 | `countWhereUsed` | `{targetType, targetId, date}` → `{employeeCount, consumerCount, sample[]}` | นับพนักงาน + consumer ที่อ้างค่านี้ | BR-22 | API-06 · API-12 |

### กลุ่ม B · องค์ประกอบค่าจ้าง

| # | Function | Input → Output | ทำอะไร | บังคับกฎ | เรียกโดย |
|---|---|---|---|---|---|
| B1 | `createPayComponent` | `componentInput` → `component` | สร้าง/สร้างเวอร์ชันใหม่ · บังคับ `payroll_code` · เก็บแฟล็กอ้างอิงทั้ง 4 ตัว | BR-13, BR-06 | API-11 |
| B2 | `detectComponentCycle` | `{componentId, baseComponentId}` → `void \| CycleError{path[]}` | เดินกราฟการอ้าง `percent_of` หา cycle · คืนเส้นทางที่วน | BR-12 | API-11 |
| B3 | `deactivateComponent` | `{componentId, reason, ackCount}` → `component` | soft archive + เตือนจำนวนผู้ใช้ → ยิง E4 | BR-05, BR-22 | API-12 |
| B4 | `computeBandBase` | `{employeeId, date}` → `money` | ผลรวม component ที่ `include_in_band_base = true` — **ไม่มีตัวไหนติดแฟล็ก → เตือน + ใช้ `BASE`** | BR-06 · EC-02 | API-13 · API-24 · ENG-SALBAND-01 |
| B5 | `computeTotalFixedMonthly` | `{employeeId, date}` → `money` | ฐาน + เงินได้ประจำ − เงินหักประจำ ที่มีผล — **ไม่ใช่ยอดจ่ายสุทธิ** | BR-13 | API-13 · API-24 |
| B6 | `filterActiveOptions` | `{options[], date}` → `options[]` | ตัดค่าที่ `inactive` ออกจาก **ตัวเลือกใหม่** (ยังแสดงของเดิมได้) | BR-18 · C-5 | API-01 · API-10 |

### กลุ่ม C · อัตรารายคน

| # | Function | Input → Output | ทำอะไร | บังคับกฎ | เรียกโดย |
|---|---|---|---|---|---|
| C1 | `assertCompRecordComplete` | `input` → `void \| Error` | บังคับ ระดับ + ฐาน + วันมีผล + เหตุผล (≥10) ครบ | BR-10 | API-14 |
| C2 | `assertChangeReasonCode` | `code` → `void \| Error` | ต้องเป็นค่าที่ `active` ใน `T_ss_change_reason` (**ไม่ใช่ enum ในโค้ด**) | BR-24 | API-14 |
| C3 | `evaluateOutOfRange` | `{bandBase, fte, band}` → `{flag, direction?}` | เทียบฐาน (ปรับ FTE) กับ min/max → เตือน + **บังคับเหตุผล** ไม่บล็อก | BR-08 | API-14 |
| C4 | `closePreviousCompRecord` | `{employeeId, newEffectiveDate}` → `record?` | ปิด `effective_to = newEffectiveDate − 1 วัน` · เปลี่ยนเป็น `history` (**ไม่ลบ**) | BR-05, BR-11 | API-14 |
| C5 | `createCompRecord` | `input` → `record` | สร้างเรคคอร์ดใหม่ (`scheduled`/`current` ตามวัน) + เก็บ `*_version_id` → ยิง E5 เมื่อมีผล | P-1′, C-2 | API-14 · C13 |
| C6 | `withdrawCompRecord` | `{recordId, cancelReason}` → `record` | `scheduled → cancelled` → ยิง E6 · อัตราปัจจุบันไม่เปลี่ยน | BR-10 | API-15 |
| C7 | `endCompRecord` | `{recordId, effectiveTo, endReason}` → `record` | `current → ended` ณ วันสุดท้าย → ยิง E7 (EC) | BR-05 | API-16 |
| C8 | `resolveCurrentRate` | `{employeeId, date}` → `record \| null` | as-of: เรคคอร์ดที่ครอบวันนั้น · **ไม่หยิบเรคคอร์ดอนาคต** | BR-11 · P-6′ | API-13 · API-24 |
| C9 | `listRateHistory` | `employeeId` → `record[]` | ทุกช่วงเรียงเวลา (append-only) | BR-05 | API-17 |
| C10 | `renderPersonSnapshot` | `{employeeId, nameSnapshot}` → `display` | ใช้ชื่อที่บันทึกไว้ + ป้าย "(พ้นสภาพ)" เมื่อต้นทางปิด — **ไม่ join แบบ hard** | BR-19 · EC-13 | API-13 · API-17 |
| C11 | `suggestGradeForEmployee` | `{employeeId, date}` → `gradeCode?` | เสนอระดับจากตำแหน่งของ Employee Master (**แก้ได้ · ไม่บังคับ**) | `[AI-DRAFT]` G-07 | API-13 (form init) |
| C12 | `computeUnassignedCount` | `{companyId, date}` → `int` | จำนวนพนักงาน active ที่ไม่มีเรคคอร์ดอัตราครอบวันนั้น | BR-19 | API-13 |
| C13 | `ingestMovementRate` | `movementPayload` → `record` | รับอัตราจากคำสั่งที่อนุมัติแล้ว → สร้าง `scheduled` เท่านั้น · **ไม่อนุมัติซ้ำ** | BR-21 · §0.13.5 | API-26 |

### กลุ่ม D · รายการประจำ

| # | Function | Input → Output | ทำอะไร | บังคับกฎ | เรียกโดย |
|---|---|---|---|---|---|
| D1 | `createRecurringItem` | `input` → `item` | สร้างรายการ (`scheduled`) · บังคับ `amount` หรือ `percent` อย่างใดอย่างหนึ่ง · `goal_amount` เฉพาะรายหัก → ยิง E8 เมื่อเริ่มมีผล | BR-14, BR-15 | API-19 |
| D2 | `withdrawRecurringItem` | `{itemId, cancelReason}` → `item` | `→ cancelled` (soft) → ยิง E9 `end_trigger: withdrawn` | BR-05 | API-20 |
| D3 | `evaluateRecurringEnd` | `item` → `{ended, trigger?}` | ปิดเมื่อ `accrued ≥ goal` **หรือ** เลย `effective_to` → ยิง E9 | BR-14 | ENG-RECUR-01 (scheduler) |

### กลุ่ม E · เวลา / ช่วงเวลา / งวด

| # | Function | Input → Output | ทำอะไร | บังคับกฎ | เรียกโดย |
|---|---|---|---|---|---|
| E1 | `computeEffectiveWindow` | `{entity, siblings[]}` → `{effectiveFrom, effectiveTo}` | คำนวณ `effective_to` จากเวอร์ชัน/เรคคอร์ดถัดไป — **ห้ามให้ผู้ใช้กรอก** | P-3′ | A5 · A8 · C4 · C5 · D1 |
| E2 | `assertNoOverlap` | `{scopeKey, range}` → `void \| OverlapError{conflictId, range}` | ตรวจช่วงทับ (กระบอก · อัตรา · รายการประจำ) — คู่กับ EXCLUDE constraint ที่ DB | BR-03, BR-11, BR-15 | A5 · C5 · D1 |
| E3 | `assertNotInClosedPeriod` | `{date, companyId}` → `void \| ClosedPeriodError{periodCode, earliestOpenDate}` | อ่าน `period_rule` จาก HR Config → ถ้า `period_status='closed'` **บล็อก** · **ตรวจ 2 ครั้ง (validate + commit)** | **P-7′ · BR-04** | A5 · C5 · C13 · D1 |
| E4 | `earliestOpenDate` | `{companyId, date}` → `date` | วันแรกที่ตั้งวันมีผลได้ (ใช้ในข้อความ + ปุ่มเติมวัน) — **ไม่ใช่การคิดย้อนหลัง** (P-9′) | BR-04 | E3 · API-14 |
| E5 | `advanceEffectiveStates` | `{tenantId, runDate}` → `{promoted, superseded, ended}` | งานเบื้องหลังเที่ยงคืน: `scheduled → active/current` · `active → superseded` · `current → history` · **idempotent รันซ้ำได้** | P-6′ | ENG-EFFDATE-01 (scheduler) |

### กลุ่ม F · HR Configuration / ค่านโยบาย

| # | Function | Input → Output | ทำอะไร | บังคับกฎ | เรียกโดย |
|---|---|---|---|---|---|
| F1 | `resolveHrConfig` | `{date, companyId, group}` → `{values, versionId}` | เรียก `GET /api/v1/hr-config/resolve` — **ส่ง `date` เสมอ** · เก็บผลลง `T_ss_cfg_ref` · cache ภายในวัน | **C-1, C-2, C-3** | F2 · E3 · API-21 · API-23 |
| F2 | `resolveLegalMinimum` | `{date, companyId}` → `{monthlyMin?, dailyMin?, versionId?}` | อ่าน `group=legal_minimum` · **ยังไม่มีค่า → คืน `null` + เหตุผล "ยังไม่ได้ตั้งค่า"** ห้ามเดาตัวเลข | **P-8′ · BR-23 · OQ-STD-11** | A5 · C5 |
| F3 | `evaluateBelowLegalMin` | `{amount, legalMin}` → `{flag, versionId}` | ต่ำกว่าขั้นต่ำ → **เตือน + บังคับเหตุผล (ไม่บล็อก)** · ไม่มีค่าอ้างอิง → ไม่ตั้งธง แต่แสดงข้อความ | BR-23 | A5 · C5 |
| F4 | `invalidateConfigCache` | `{groups[], reason}` → `refreshed[]` | ล้างค่าที่ดึงไว้ + ถามใหม่ (ทั้งจากปุ่มบนจอ และจาก event `hrconfig.*`) | C-3 | API-23 · event handler |
| F5 | `listConfigRefs` | `{tenantId}` → `ref[]` | รายการค่าที่อ่านจาก HR Config + `version_id` + เวลาที่ดึง | C-2 | API-21 |
| F6 | `registerWhereUsed` | `{consumerCode, itemIds[]}` → `void` | ลงทะเบียนการใช้งาน 2 ทาง: consumer ของเรา + `POST /hr-config/items/:id/usage` | **C-6 · SS-7** | API-27 |
| F7 | `listConsumers` / `setLinkStatus` | — | ทะเบียน consumer + ปรับสถานะ Module Linkage เอง (admin action → audit) | BR-22 | API-21 · API-22 |

### กลุ่ม G · สิทธิ์ / การแสดงผล / โครงสร้างร่วม

| # | Function | Input → Output | ทำอะไร | บังคับกฎ | เรียกโดย |
|---|---|---|---|---|---|
| G1 | `maskMoney` | `{value, subjectEmployeeId, viewer}` → `money \| null` | เรียก ENG-MASK-01 → ไม่มีสิทธิ์คืน `null` + `masked: true` · **ทำที่ชั้น API ก่อน serialize** | BR-16 · D7 | ทุก endpoint ที่คืนเงิน |
| G2 | `logRestrictedView` | `{viewer, subject, scope}` → `void` | บันทึกการเปิดดูข้อมูล Restricted ไป Policy Center + ยิง E10 | BR-16 · D9 | API-13(detail) · API-17 |
| G3 | `emitAuditEvent` | `{actor, action, target, before?, after?}` → `void` | audit ทุก mutation (append-only ที่ Policy Center) | D9 | ทุก mutation |
| G4 | `formatMoney` | `{value, digits}` → `string` | คั่นหลักพัน + 2 ตำแหน่ง · THB — **การปัดเพื่อจ่ายจริงเป็นของ Payroll** | VR-21 · FN-94 | ทุกจุดที่แสดงเงิน |
| G5 | `buildListQuery` | `{filters, paging}` → `query` | ประกอบเงื่อนไขค้นหา/กรอง/เรียง + เพจ (server-side) | FN-90 · TP-01 | API-01/10/13/18 |
| G6 | `assertIdempotent` | `{key, endpoint, payloadHash}` → `cached? \| void` | กันการทำซ้ำ (คืนผลเดิมเมื่อ key+payload เดิม) | PR-7 · EC-30 | ทุก POST |
| G7 | `computeFteAdjustedBase` | `{bandBase, fte}` → `money` | `bandBase ÷ fte` (FTE < 1) | BR-09 | ENG-SALBAND-01 |
| G8 | `buildRateSnapshot` | `{employeeId \| companyId, date, include[]}` → `snapshot` | ประกอบคำตอบของ **§0.13.2** — ฐาน + components + recurring + band_position + **`version_id` เสมอ** | **BR-20 · P-5′** | API-24 |
| G9 | `buildBandSnapshot` | `{companyId, date, gradeCode?}` → `bands[]` | คำตอบของ **§0.13.3** (mid-point + headcount · ไม่ระบุตัวบุคคล) | BR-20 | API-25 |

## §3.2 Engines (Reusable / CUBIC-Registered)

> **สำหรับ Architect:** 3 ตัวแรกเป็น **engine candidate ใหม่** ที่ควรพิจารณาขึ้นทะเบียน CUBIC — ทั้งสามเป็นแพทเทิร์นที่ feature HR อื่นจะใช้ซ้ำแน่นอน (Employee Movement · Payroll · Welfare · Attendance)

### ENG-EFFDATE-01 · `effective-window-resolver` **[NEW — CUBIC candidate]**
- **หน้าที่:** จัดการวัตถุที่มี `effective_date` ทุกชนิด — คำนวณ `effective_to` · ตรวจช่วงไม่ทับ · เลื่อนสถานะเมื่อถึงวันมีผล (idempotent)
- **Input:** `{ entityType, scopeKey, ranges[], runDate }` → **Output:** `{ windows[], promoted[], superseded[], conflicts[] }`
- **Pure:** ไม่มี HTTP · ไม่รู้จัก request/response · รับ-คืน object ล้วน
- **ทำไมควร reuse:** HR Configuration (P-1…P-4) · Salary Structure · Employee Movement · Shift & Roster ใช้กติกาเดียวกันทั้งหมด — ตอนนี้แต่ละ feature เขียนเอง = ความเสี่ยงว่านิยาม "ทับกัน" ไม่ตรงกัน
- **ผูกกับ:** `computeEffectiveWindow` · `assertNoOverlap` · `advanceEffectiveStates`

### ENG-SALBAND-01 · `salary-band-position-calculator` **[NEW — CUBIC candidate]**
- **หน้าที่:** คำนวณตำแหน่งในกระบอก — `compa_ratio` · `range_penetration` · `fte_adjusted_base` · `out_of_range_flag`
- **Input:** `{ bandBase, fte, band: {min, mid, max} }` → **Output:** `{ compaRatio, rangePenetration, fteAdjustedBase, outOfRange: {flag, direction} }`
- **กติกาในตัว:** ไม่มีกระบอก → คืน `null` ทุกค่า (ไม่คำนวณมั่ว · EC-01) · เป็น **การแสดงผล ไม่ใช่เกณฑ์อนุมัติ** (BR-07)
- **ทำไมควร reuse:** Employee Movement (ตอนร่างคำสั่ง) · Manpower Planning · Performance ต้องใช้สูตรเดียวกันเป๊ะ — **SS-6 ห้าม consumer คำนวณเอง** จึงต้องมี engine กลาง
- **ผูกกับ:** `computeBandBase` · `computeFteAdjustedBase` · `evaluateOutOfRange`

### ENG-RECUR-01 · `recurring-item-terminator` **[NEW — CUBIC candidate]**
- **หน้าที่:** ปิดรายการที่เกิดซ้ำเมื่อครบเงื่อนไข (ยอดสะสมถึงเป้า **หรือ** ถึงวันสิ้นสุด) แล้วคืนเหตุที่ปิด
- **Input:** `{ items[], asOfDate }` → **Output:** `{ ended: [{itemId, trigger}] }`
- **ทำไมควร reuse:** Welfare (สิทธิ์ที่มีเพดาน) · Expense Claim (ผ่อนจ่าย) · Payroll (salary attachment) ใช้แพทเทิร์นเดียวกัน
- **ผูกกับ:** `evaluateRecurringEnd`

### ENG-CSQ-01 · `csq-event-emitter` **[EXISTING — ENG-CSQ 7C]**
- ยิง 10 event ตาม `5_DECLARATIONS/CSQ_BRIEF.md §2` (ท่อ **EC + SecC** เท่านั้น) · **ห้ามยิง OC / DC ระดับเอกสาร / SC** (register 422)
- feature เรียกผ่าน service layer — **ไม่ implement ซ้ำ**

### ENG-MASK-01 · `data-masking-resolver` **[EXISTING — Policy Center]**
- ตัดสินว่า viewer เห็นค่า Restricted ของ subject ได้หรือไม่ (RBAC + **ABAC** `manager_of`) · คืน `null` เมื่อไม่มีสิทธิ์
- **ห้ามทำ permission logic เองในแพ็กนี้** (BR-16 · catalog §0)

### ENG-HRCFG-01 · `hr-config-resolver` **[EXISTING — อยู่ที่ F-HR-CONFIG]**
- เรียกผ่าน **HTTP contract เท่านั้น** (`GET /api/v1/hr-config/resolve`) — feature นี้ **ไม่เรียก engine ข้าม service โดยตรง** (Engine Iron Rule: ห้าม bypass API)

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| Function / Engine | ถูกเรียกจาก | เรียกต่อไปยัง |
|---|---|---|
| `createBandDraft` (A1) | API-02 | `assertBandOrder` · `applyPercentAdjust` |
| `assertBandOrder` (A2) | API-02 · API-03 · A3 | — |
| `applyPercentAdjust` (A3) | API-02 | `assertBandOrder` |
| `assertVersionEditable` (A4) | API-03 | — |
| `publishBandVersion` (A5) | API-04 | `assertNoOverlap` · `assertNotInClosedPeriod` · `resolveLegalMinimum` · `evaluateBelowLegalMin` · `computeEffectiveWindow` · ENG-CSQ-01 |
| `withdrawBandVersion` (A6) | API-05 | ENG-CSQ-01 |
| `deactivateGrade` (A7) | API-06 | `countWhereUsed` · ENG-CSQ-01 |
| `reactivateGrade` (A8) | API-07 | `computeEffectiveWindow` |
| `listVersionHistory` (A9) | API-08 | — |
| `buildVersionDiff` (A10) | API-09 | — |
| `resolveBandAt` (A11) | API-01 · API-13 · API-24 · API-25 | — |
| `countWhereUsed` (A12) | API-06 · API-12 | — |
| `createPayComponent` (B1) | API-11 | `detectComponentCycle` |
| `detectComponentCycle` (B2) | API-11 | — |
| `deactivateComponent` (B3) | API-12 | `countWhereUsed` · ENG-CSQ-01 |
| `computeBandBase` (B4) | API-13 · API-24 · ENG-SALBAND-01 | — |
| `computeTotalFixedMonthly` (B5) | API-13 · API-24 | `maskMoney` |
| `filterActiveOptions` (B6) | API-01 · API-10 | — |
| `assertCompRecordComplete` (C1) | API-14 | — |
| `assertChangeReasonCode` (C2) | API-14 | — |
| `evaluateOutOfRange` (C3) | API-14 | ENG-SALBAND-01 |
| `closePreviousCompRecord` (C4) | API-14 | `computeEffectiveWindow` |
| `createCompRecord` (C5) | API-14 · C13 | `assertNoOverlap` · `assertNotInClosedPeriod` · `resolveLegalMinimum` · ENG-CSQ-01 |
| `withdrawCompRecord` (C6) | API-15 | ENG-CSQ-01 |
| `endCompRecord` (C7) | API-16 | ENG-CSQ-01 |
| `resolveCurrentRate` (C8) | API-13 · API-24 | — |
| `listRateHistory` (C9) | API-17 | `renderPersonSnapshot` · `maskMoney` |
| `renderPersonSnapshot` (C10) | API-13 · API-17 | — |
| `suggestGradeForEmployee` (C11) | API-13 (form init) | — |
| `computeUnassignedCount` (C12) | API-13 | — |
| `ingestMovementRate` (C13) | API-26 | `assertIdempotent` · `createCompRecord` |
| `createRecurringItem` (D1) | API-19 | `assertNoOverlap` · `assertNotInClosedPeriod` · ENG-CSQ-01 |
| `withdrawRecurringItem` (D2) | API-20 | ENG-CSQ-01 |
| `evaluateRecurringEnd` (D3) | ENG-RECUR-01 (scheduler) | ENG-CSQ-01 |
| `computeEffectiveWindow` (E1) | A5 · A8 · C4 · C5 · D1 | ENG-EFFDATE-01 |
| `assertNoOverlap` (E2) | A5 · C5 · D1 | ENG-EFFDATE-01 |
| `assertNotInClosedPeriod` (E3) | A5 · C5 · C13 · D1 | `resolveHrConfig` · `earliestOpenDate` |
| `earliestOpenDate` (E4) | E3 · API-14 | `resolveHrConfig` |
| `advanceEffectiveStates` (E5) | ENG-EFFDATE-01 (scheduler) | ENG-CSQ-01 |
| `resolveHrConfig` (F1) | E3 · F2 · API-21 · API-23 | (HTTP → ENG-HRCFG-01 ที่ F-HR-CONFIG) |
| `resolveLegalMinimum` (F2) | A5 · C5 | `resolveHrConfig` |
| `evaluateBelowLegalMin` (F3) | A5 · C5 | — |
| `invalidateConfigCache` (F4) | API-23 · event handler | `resolveHrConfig` |
| `listConfigRefs` (F5) | API-21 | — |
| `registerWhereUsed` (F6) | API-27 | (HTTP → hr-config usage) |
| `listConsumers` / `setLinkStatus` (F7) | API-21 · API-22 | `emitAuditEvent` |
| `maskMoney` (G1) | ทุก endpoint ที่คืนเงิน | ENG-MASK-01 |
| `logRestrictedView` (G2) | API-13(detail) · API-17 | ENG-CSQ-01 (E10) |
| `emitAuditEvent` (G3) | ทุก mutation | — |
| `formatMoney` (G4) | ทุกจุดที่แสดงเงิน | — |
| `buildListQuery` (G5) | API-01/10/13/18 | — |
| `assertIdempotent` (G6) | ทุก POST | — |
| `computeFteAdjustedBase` (G7) | ENG-SALBAND-01 | — |
| `buildRateSnapshot` (G8) | API-24 | `resolveCurrentRate` · `resolveBandAt` · `computeBandBase` · ENG-SALBAND-01 · `maskMoney` |
| `buildBandSnapshot` (G9) | API-25 | `resolveBandAt` |
| **ENG-EFFDATE-01** | E1 · E2 · E5 · scheduler | — |
| **ENG-SALBAND-01** | C3 · G8 · API-13 | `computeBandBase` · `computeFteAdjustedBase` |
| **ENG-RECUR-01** | scheduler | `evaluateRecurringEnd` |
| **ENG-CSQ-01** | A5 · A6 · A7 · B3 · C5 · C6 · C7 · D1 · D2 · D3 · E5 · G2 | — |
| **ENG-MASK-01** | G1 | — |
| **ENG-HRCFG-01** | ผ่าน HTTP จาก F1 เท่านั้น | — |

### Trace Verification (Self-Check)
- ✅ ทุก **mutation API** (API-02…API-07 · 11 · 12 · 14…16 · 19 · 20 · 22 · 23 · 26 · 27) มี ≥1 Function/Engine
- ✅ ทุก Function ใน §3.1 (55 ตัว) ถูก trace อย่างน้อย 1 API หรือ 1 scheduler job
- ✅ ทุก Engine ใน §3.2 (6 ตัว) ถูกเรียกผ่าน Function หรือ API
- ✅ **ไม่มี orphan** — ไม่มี Function/Engine ที่ไม่มีใครเรียก
- ✅ ไม่มี Engine ตัวใดอ้างคำศัพท์ HTTP (req/res/header) · input/output เป็น object ล้วน
- ✅ feature ไม่ bypass API เพื่อเรียก engine ของ feature อื่น (`ENG-HRCFG-01` เรียกผ่าน HTTP เท่านั้น)

## §3.4 Dependencies

**External Function/Engine ที่แพ็กนี้เรียก**
| ตัว | ของใคร | เรียกอย่างไร |
|---|---|---|
| `hr-config-resolver` (ENG-HRCFG-01) | F-HR-CONFIG | HTTP `GET /api/v1/hr-config/resolve` (ห้ามเรียก engine ตรง) |
| `data-masking-resolver` (ENG-MASK-01) | Policy Center | service call ตอน runtime |
| `csq-event-emitter` (ENG-CSQ-01) | ENG-CSQ 7C | service call |
| Employee combobox / person lookup | Employee Master | HTTP อ่านอย่างเดียว |

**External ที่เรียกเข้ามาในแพ็กนี้**
| ใคร | เรียกอะไร |
|---|---|
| Payroll · หนังสือรับรอง · Employee Movement | `GET /resolve` (API-24) |
| Manpower Planning | `GET /bands/resolve` (API-25) |
| Employee Movement | `POST /rates/from-movement` (API-26) · `POST /rates/{id}/withdraw` (API-15) |
| HR Configuration event bus | `hrconfig.effective` · `hrconfig.deactivated` · `hrconfig.period_closed` → `invalidateConfigCache` (F4) |

## §3.5 Open Questions / Locked Decisions Referenced

| อ้าง | เรื่อง | ที่อยู่ |
|---|---|---|
| OQ-FRD-01 | โหมด `scope=company` ของ API-24 | `00_OVERVIEW §0.8` |
| OQ-FRD-02 | scheduler + as-of read คู่กัน (`advanceEffectiveStates` idempotent) | `00_OVERVIEW §0.8` |
| OQ-FRD-04 | masking ที่ชั้น API | `05_RULES §5.7 D7` |
| OQ-STD-09 | นิยามฐานเทียบกระบอก (`computeBandBase`) | BRD §15 |
| OQ-STD-03 | วิธีเทียบ FTE (`computeFteAdjustedBase`) | BRD §15 |
| OQ-SS-01 | นอกกระบอก เตือนหรือบล็อก (`evaluateOutOfRange`) | BRD §15 · `07_LOCKED §7.3` |
| OQ-SS-02 | ที่มาของ `accrued_amount` (`evaluateRecurringEnd`) | BRD §15 |
| OQ-STD-11 | group `legal_minimum` ยังไม่เผยแพร่ (`resolveLegalMinimum`) | BRD §15 · `_NOTIFY.md` |
| LD-01…LD-06 | การตัดสินใจที่ล็อกแล้ว | `07_LOCKED_DECISIONS §7.1` |

## Audience Cheat-Sheet
- **จะเพิ่ม endpoint ใหม่?** ต้องมี Function/Engine รองรับที่นี่ก่อน แล้วต่อ trace ใน §3.3
- **จะเพิ่มการคำนวณเงิน?** ถามก่อนว่าเป็นของ feature นี้จริงไหม — ภาษี/ปกส./ยอดสุทธิ **เป็นของ Payroll** (BR-13)
- **จะเพิ่มเงื่อนไขวันที่?** ผ่าน `ENG-EFFDATE-01` เท่านั้น — ห้ามเขียนตรรกะช่วงเวลาซ้ำในแต่ละ endpoint
