# 03_LOGIC — F-HR-CONFIG · HR Configuration (ตั้งค่าHR)

> **Audience:** Backend developer (business logic layer)
> **Scope:** logic ที่ไม่ใช่ HTTP ทั้งหมด — pure function, state transition, calculation, validation, integration
> **Naming:** Function code = `camelCase` · Engine code = `kebab-case`
> **🚨 R8:** ทุก mutation API ต้อง trace มาที่ Function/Engine ใน §3.3
> **🚨 CUBIC 3-layer:** Engine ห้ามอ้าง HTTP (req/res/header) · input/output เป็น pure object · feature ห้ามข้าม API ไปเรียก Engine ตรง ๆ

---

## §3.1 Functions (Scope-Local)

> logic ที่ใช้ใน feature นี้เท่านั้น ไม่ register CUBIC

### F-HR-CONFIG-FN-01: buildConfigListQuery
- **Purpose:** ประกอบ query สำหรับ list/detail/periods — รวมตัวกรอง + **as-of date** (คืนเวอร์ชันที่ Active ณ วันนั้น)
- **Input:** `{ tenantId, group?, status?, companyId?, q?, asOf?, limit, offset, sort, role }`
- **Output:** `{ rows: ConfigItemRow[], total, asOf }`
- **Invoked by:** `API-01`, `API-02`, `API-17`
- **Calls:** — (ใช้ index `IDX_cfgver_item_eff`)
- **Side effects:** — (read-only)
- **Rules:** BR-19 (ไม่คืน draft/scheduled เป็น "ค่าปัจจุบัน") · role `viewer` ส่ง `asOf` ไม่ได้ → 403
- **FN trace:** FN-90, FN-28
- **Iron rule check:** ✅ ไม่มีศัพท์ HTTP

### F-HR-CONFIG-FN-02: createConfigItem
- **Purpose:** สร้าง `config_item` + เวอร์ชันแรก (Draft) + ผูกบริษัทตาม `company_scope`
- **Input:** `{ tenantId, actor, code, nameTh, nameEn?, group, companyScope, companyIds[], payrollCode?, ownerEmployeeId, note?, payload }`
- **Output:** `{ itemId, versionId, versionNo: 1, status: 'draft' } | ValidationError[]`
- **Invoked by:** `API-03` · **Calls:** FN-05, FN-17
- **Side effects:** INSERT `T_hr_config_item` (+ `T_hr_config_item_company`) · INSERT version (draft) · INSERT payload row · snapshot ชื่อผู้รับผิดชอบ/บริษัท
- **Rules:** VR-23 · VR-22 · BR-15
- **FN trace:** FN-01, FN-22, FN-30, FN-94 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-03: createConfigVersion
- **Purpose:** **การ "แก้ไข" ค่าที่ Active** — สร้างเวอร์ชันใหม่โดย copy payload เดิม (BR-02 · P-2)
- **Input:** `{ tenantId, actor, itemId, copyFromVersionId?, payload? }`
- **Output:** `{ versionId, versionNo, status: 'draft', copiedFrom }`
- **Invoked by:** `API-04` · **Calls:** FN-05, FN-17
- **Side effects:** INSERT version (draft) + payload row ใหม่ (**ไม่แตะ payload เดิม**)
- **Rules:** BR-02 · item ต้อง `status='active'`
- **FN trace:** FN-04 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-04: saveDraftVersion
- **Purpose:** บันทึกร่าง — **ไม่ต้องมี `effective_date`** และไม่กระทบ feature ใด
- **Input:** `{ tenantId, actor, versionId, patch }` · **Output:** `{ versionId, status:'draft' } | ValidationError[]`
- **Invoked by:** `API-03`, `API-05` · **Calls:** FN-05 (โหมดผ่อนปรน), FN-17
- **Side effects:** UPDATE draft row + payload · **ปฏิเสธถ้า `status ≠ 'draft'`** → `BR_VERSION_NOT_EDITABLE`
- **Rules:** BR-19 · ต้องมีชื่อค่าอย่างน้อย (`กรอกชื่อค่าก่อนบันทึกร่าง`)
- **FN trace:** FN-06 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-05: validateVersionPayload ⭐ (จุดรวม validation เชิงธุรกิจ)
- **Purpose:** validate payload ตาม `group` + business rules ที่ DB constraint ทำไม่ได้
- **Input:** `{ tenantId, group, payload, itemContext, mode: 'draft'|'publish' }`
- **Output:** `{ ok:true } | { ok:false, errors:[{field,code,message,hint?}], warnings:[…] }`
- **Invoked by:** `API-03`, `API-04`, `API-05`, `API-06`, `API-10` (ผ่าน FN-02/03/04/06/10)
- **Calls:** FN-18 · อ่าน `T_hr_legal_minimum` และ `T_hr_config_param`
- **Side effects:** — (pure ยกเว้น read)
- **Rules ที่บังคับที่นี่:**
  - **BR-05** ตัวคูณ OT ≥ ขั้นต่ำ (join `T_hr_legal_minimum` ตาม `effective_date` — **ห้าม hardcode 1.5**)
  - **BR-06** โควตาลาพักร้อน < ขั้นต่ำ → **warning ไม่ block** (โหมดจาก `leave_min_quota_mode`)
  - **BR-09** วันหยุดซ้ำใน (บริษัท + ปี) — **ตรวจข้ามชุดปฏิทินด้วย**
  - **BR-10** รอบประเมินทับซ้อนในปีเดียวกัน · **BR-11** วันตัด ≤ วันจ่าย
  - **BR-12** ยกยอด > 0 ต้องมีวันหมดอายุในปีถัดไป
  - **BR-16** milestone ต่อเนื่อง ไม่ทับซ้อน ไม่มีช่องว่าง (ขั้นสุดท้าย `year_to=null` = ไม่ถือว่ามีช่องว่าง · EA-11)
  - **BR-17** กะ: ออก > เข้า เว้นแต่ข้ามวัน · ช่วงพักอยู่ในช่วงกะ (**รองรับพักคร่อมเที่ยงคืน** · EA-08)
  - **BR-18** `payroll_code` ว่างในประเภทที่จ่าย → **warning** (โหมดจาก `payroll_code_mode`)
  - VR-09…VR-11, VR-18, VR-21, VR-22, VR-24 · **EA-14** ห้ามลบวันหยุดต้นทางที่มีวันชดเชยอ้างอยู่
- **FN trace:** FN-08, FN-09, FN-10, FN-11, FN-13, FN-14, FN-16, FN-17, FN-18, FN-20, FN-21, FN-29, FN-31, FN-32, FN-49, FN-50, FN-92
- **Iron rule check:** ✅

### F-HR-CONFIG-FN-06: publishVersion ⭐ (state transition หลัก)
- **Purpose:** Draft → **Scheduled** (วันมีผลอนาคต) หรือ **Active** (วันนี้) · จัดการ supersede + effective window
- **Input:** `{ tenantId, actor, versionId, effectiveDate, changeReason?, confirmBelowLegalMin?, ifMatch }`
- **Output:** `{ versionId, status, effectiveDate, supersededVersionId?, warnings[] } | ValidationError[]`
- **Invoked by:** `API-06` · และ **scheduler** (โหมด catch-up: scheduled → active ตามวัน)
- **Calls:** FN-05, **FN-20 (เรียกซ้ำภายใน transaction)**, FN-19, FN-17, FN-16
- **Side effects:** UPDATE version status · UPDATE เวอร์ชันก่อนหน้า (`effective_to`, `superseded`) · write audit · **emit `hrconfig.published`** (+ `hrconfig.effective` ถ้ามีผลทันที)
- **Rules:** **BR-01 · BR-03 · BR-04 · BR-02 · BR-14 · BR-19**
- **Concurrency:** transaction เดียว + `SELECT … FOR SHARE` บนแถวงวดที่เกี่ยวข้อง (PR-9 · EA-02) · unique/exclude constraint ของ DB เป็นด่านสุดท้าย (EA-01)
- **Scheduler catch-up (EA-04):** ถ้า job ขาดหลายวัน ต้องประมวลผลย้อนตามลำดับวันให้ครบ ห้ามข้าม · ค่าที่ FRD เลือก = **lazy resolve** (คำนวณสถานะจาก `effective_date` ตอนอ่าน) โดย scheduler ทำหน้าที่ materialize + ยิง event → **LD-02**
- **FN trace:** FN-01, FN-02, FN-03, FN-05, FN-19, FN-93 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-07: cancelScheduledVersion
- **Purpose:** ยกเลิกเวอร์ชันที่ยังไม่ถึงวันมีผล + **คำนวณ `effective_to` ของเวอร์ชันก่อนหน้าใหม่**
- **Input:** `{ tenantId, actor, versionId, cancelReason }` · **Output:** `{ versionId, status:'cancelled', recomputedWindows[] }`
- **Invoked by:** `API-07` · **Calls:** FN-19, FN-17, FN-16
- **Side effects:** UPDATE → cancelled · re-compute window ของเวอร์ชันก่อนหน้าจากเวอร์ชันถัดไป**ที่ยังเหลืออยู่** (EA-05 🔺 · OQ-14) · write audit · **emit `hrconfig.cancelled`**
- **Rules:** **BR-20** (ยกเลิกได้ก่อนมีผลเท่านั้น) · เหตุผล ≥10 ตัวอักษร
- **FN trace:** FN-07 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-08: discardDraftVersion
- **Purpose:** ทิ้งร่าง (Draft → Discarded) — **ไม่ลบแถว**
- **Input:** `{ tenantId, actor, versionId }` · **Output:** `{ versionId, status:'discarded' }`
- **Invoked by:** `API-08` · **Calls:** FN-17 · **Side effects:** UPDATE status · write audit · **ไม่ยิง event**
- **Rules:** BR-07 · ทำได้เฉพาะ `status='draft'`
- **FN trace:** FN-06, FN-91 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-09: deactivateConfigItem
- **Purpose:** ปิดใช้ค่า (soft archive) หลังผู้ใช้รับทราบ where-used
- **Input:** `{ tenantId, actor, itemId, deactivateReason, acknowledgedUsage }` · **Output:** `{ itemId, status:'inactive', usageCount }`
- **Invoked by:** `API-09` · **Calls:** FN-12, FN-17, FN-16
- **Side effects:** UPDATE item → inactive · version ที่ active → inactive · write audit · **emit `hrconfig.deactivated`**
- **Rules:** **BR-07 · BR-08** (`acknowledgedUsage` ต้อง true มิฉะนั้น `BR_WHERE_USED_NOT_ACKNOWLEDGED`) · เหตุผล ≥10 ตัวอักษร
- **Edge (EA-07):** item ที่มีแต่เวอร์ชัน draft → ทำเป็น **discard ร่าง** ไม่ใช่ soft archive
- **FN trace:** FN-24, FN-26, FN-91 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-10: reactivateConfigItem
- **Purpose:** เปิดใช้กลับ = **สร้างเวอร์ชันใหม่พร้อมวันมีผล** (ไม่ revert ของเดิม)
- **Input:** `{ tenantId, actor, itemId, effectiveDate, changeReason, payload }` · **Output:** `{ itemId, status:'active', versionId }`
- **Invoked by:** `API-10` · **Calls:** FN-05, **FN-20**, FN-06 (ใช้เส้นทาง publish เดียวกัน), FN-17, FN-16
- **Side effects:** UPDATE item → active · INSERT version · write audit · **emit `hrconfig.reactivated`**
- **Rules:** **BR-04 ยังบังคับ** (EA-06)
- **FN trace:** FN-25 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-11: buildVersionHistory
- **Purpose:** timeline ประวัติเวอร์ชัน + `value_diff` (ค่าเก่า→ค่าใหม่)
- **Input:** `{ tenantId, itemId }` · **Output:** `VersionHistoryEntry[]` (เรียง `effective_date` DESC)
- **Invoked by:** `API-12` · **Calls:** — · **Side effects:** — (read-only · **ไม่มีเส้นทางแก้/ลบประวัติ** · BR-14 · P-4)
- **FN trace:** FN-27, FN-93 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-12: buildWhereUsedList
- **Purpose:** รายการ consumer ที่อ้างค่านี้ + สถานะ Module Linkage (⏳/✅) + เวอร์ชันที่ปลายทางอ่านอยู่
- **Input:** `{ tenantId, itemId }` · **Output:** `{ usageCount, consumers[], currentVersionReadByConsumers }`
- **Invoked by:** `API-11`, `FN-09` · **Calls:** —
- **Side effects:** — · **ห้าม query ข้อมูลภายในของ consumer** (LD-4C-02) — อ่านจาก `T_hr_config_usage` เท่านั้น
- **FN trace:** FN-33, FN-26 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-13: generatePayPeriods
- **Purpose:** สั่งสร้างงวดทั้งปีจากกติกา + persist
- **Input:** `{ tenantId, actor, periodRuleId, year, overwriteOpenPeriods }` · **Output:** `{ generated, periods[] }`
- **Invoked by:** `API-14` · **Calls:** **ENG-HRCFG-02**, FN-17
- **Side effects:** INSERT `T_hr_pay_period` × N · write audit · **ไม่ยิง event**
- **Rules:** **BR-21** — ปีที่มีงวด `closed` อยู่แล้ว **ห้ามสร้างทับ** (`BR_PERIOD_CLOSED_CANNOT_REGENERATE`)
- **FN trace:** FN-48 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-14: closePayPeriod
- **Purpose:** ปิดงวด — **สร้างนิยาม "งวดที่ปิดแล้ว" ที่ BR-04 ใช้**
- **Input:** `{ tenantId, actor, periodId }` · **Output:** `{ periodCode, status:'closed', closedBy, closedAt }`
- **Invoked by:** `API-15` · **Calls:** FN-17, FN-16
- **Side effects:** UPDATE + `closed_by`/`closed_at` (**row lock — serialize กับ FN-06** · PR-9) · write audit · **emit `hrconfig.period_closed`**
- **Rules:** BR-21 · ปิดซ้ำ → `BR_PERIOD_ALREADY_CLOSED`
- **FN trace:** FN-48, FN-91 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-15: reopenPayPeriod
- **Purpose:** เปิดงวดกลับ — ต้องมีเหตุผล + audit (**ไม่ลบร่องรอยการปิดครั้งก่อน**)
- **Input:** `{ tenantId, actor, periodId, reopenReason }` · **Output:** `{ periodCode, status:'open' }`
- **Invoked by:** `API-16` · **Calls:** FN-17
- **Side effects:** UPDATE → open + เก็บ `reopen_reason` · write audit (append-only) · **ไม่ยิง event** (ไม่มี `period_reopened` ใน CSQ_BRIEF — **ห้ามประกาศ event นอก brief**)
- **Rules:** BR-21 · เหตุผล ≥10 ตัวอักษร (โหมดจาก `reopen_period_requires_reason`)
- **FN trace:** FN-48, FN-91 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-16: emitCsqEvent (integration wrapper)
- **Purpose:** ห่อการยิง event ให้ **ENG-CSQ 7C (ท่อ SecC)** — จุดเดียวที่ feature ยิง event
- **Input:** `{ tenantId, eventId, payload, idempotencyKey }` · **Output:** `{ accepted, stampRef? }`
- **Invoked by:** FN-06, FN-07, FN-09, FN-10, FN-14 · **Calls:** ENG-CSQ (baseline — **ไม่ re-implement**)
- **Side effects:** ส่ง event ออกนอก feature · **ห้ามเขียนคอลัมน์ผลรายท่อในตารางของ feature** (ผลอยู่ที่ `T_csq_stamp`)
- **Rules (BR-CSQ):** `event_id` ต้องอยู่ใน **6 ตัวที่ประกาศเท่านั้น** · ท่อ = **SecC เท่านั้น** (OC/DC-เอกสาร/SC = 422) · `idempotency_key = F-HR-CONFIG:{version_id|period_code}:{event_id}` · **ส่ง `employee_id` ไม่ส่งชื่อ** (D7)
- **FN trace:** — (infrastructure ของ CSQ_BRIEF) · **Iron rule check:** ✅ ไม่คำนวณมูลค่าใด ๆ

### F-HR-CONFIG-FN-17: writeAuditEntry (integration wrapper)
- **Purpose:** ห่อการเขียน **Policy Center Audit Trail** (append-only)
- **Input:** `{ tenantId, actor, action, resource, before, after, reason? }` · **Output:** `{ ok, auditId }`
- **Invoked by:** ทุก mutation function (FN-02…FN-15) · **Calls:** Policy Center Audit Trail (baseline)
- **Side effects:** เขียน log · **ถ้าเขียนไม่สำเร็จ → rollback transaction ทั้งก้อน** (SLA-05 · R-02 · BR-14)
- **FN trace:** FN-93 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-18: computeShiftHours (pure helper)
- **Purpose:** ชั่วโมงทำงาน/วัน = (ออก − เข้า) − พัก · **รองรับกะข้ามวันและช่วงพักคร่อมเที่ยงคืน**
- **Input:** `{ timeIn, timeOut, overnight, breaks[] }` · **Output:** `{ hoursPerDay } | Error`
- **Invoked by:** FN-05 · **Calls:** — · **Side effects:** — (pure)
- **Rules:** BR-17 · **ใช้เวลาเชิงเส้น (บวก 24 ชม. เมื่อ `overnight`) ไม่ใช่ modulo 24** (EA-08)
- **FN trace:** FN-14 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-19: computeEffectiveWindow (pure helper)
- **Purpose:** คำนวณ `effective_to` ของทุกเวอร์ชันของ item หนึ่งจากลำดับ `effective_date`
- **Input:** `{ versions:[{id, effectiveDate, status}] }` · **Output:** `[{ id, effectiveFrom, effectiveTo }]`
- **Invoked by:** FN-06, FN-07 · **Calls:** — · **Side effects:** — (pure)
- **Rules:** `effective_to` = `effective_date` ของเวอร์ชันถัดไปที่ยังมีผลได้ − 1 วัน · เวอร์ชันล่าสุด = `null`
- **Edge (EA-05):** เมื่อเวอร์ชันกลางถูกยกเลิก ต้องคำนวณใหม่ทั้งชุด ไม่ใช่แค่คู่ที่ติดกัน
- **FN trace:** FN-02, FN-05, FN-28 · **Iron rule check:** ✅

### F-HR-CONFIG-FN-20: assertNotInClosedPeriod ⭐ (guard ของ BR-04)
- **Purpose:** ตรวจว่า `effective_date` ไม่ตกในงวดที่ `period_status='closed'` + คืน **วันแรกที่ตั้งได้**
- **Input:** `{ tenantId, effectiveDate, companyScopeContext }` · **Output:** `{ ok:true } | { ok:false, blockingPeriodCode, earliestAllowedDate }`
- **Invoked by:** FN-06, FN-10 — **เรียก 2 ครั้ง: ตอน validate เพื่อแสดงผล และอีกครั้งภายใน transaction ตอน commit** (EA-02 🔺 · OQ-13)
- **Calls:** — (อ่าน `T_hr_pay_period` ด้วย `IDX_payperiod_lookup` + `FOR SHARE`)
- **Side effects:** — (read + row lock ชั่วคราว)
- **Rules:** **BR-04 + BR-21** · เปิด/ปิดการบังคับผ่าน `T_hr_config_param.lock_closed_period_enforced` (**default true — ห้าม hardcode `if(true)`**)
- **FN trace:** FN-19 · **Iron rule check:** ✅

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### ENG-HRCFG-01: `hr-config-resolve` — **NEW · status DRAFT (register Phase 2 — LD-03)**
- **id:** (assigned at CUBIC Registry registration)
- **code:** `hr-config-resolve` · **name:** HR Configuration Effective-Dated Resolver · **category:** `policy-resolution`
- **input schema:** `{ tenantId, date (required), companyId?, group?, code? }`
- **output schema:**
  `{ asOf, companyId, items: [{ code, group, nameTh, versionId, versionNo, effectiveWindow{from,to}, resolvedFrom: "company:<uuid>"|"shared", itemStatus: "active"|"inactive", payload{…} }], generatedAt }`
- **logic outline:**
  1. **ปฏิเสธถ้าไม่มี `date`** (`ERR_RESOLVE_DATE_REQUIRED`) — `[AI-DEFAULT]` · OQ-15 · P-5
  2. คัดเฉพาะเวอร์ชัน `status='active'` ที่ `date` อยู่ใน `[effective_date, effective_to]` (BR-19 · P-6)
  3. แยกผลเป็น 2 ชั้น: ค่าเฉพาะบริษัท (`company_scope='company'` และ `companyId` ตรง) กับค่ากลาง (`shared`)
  4. **บริษัทลูกทับค่ากลางเสมอ** ต่อ `code` เดียวกัน (BR-13) — บันทึกผลที่ `resolvedFrom`
  5. item ที่ `status='inactive'` ไม่อยู่ในผลรวม — คืนได้เฉพาะเมื่อระบุ `code` ตรง (พร้อม `itemStatus:"inactive"`) เพื่อให้เอกสารเก่าแสดงผลได้ (C-5)
  6. คืน `versionId` ทุกแถวเสมอ เพื่อให้ปลายทางเก็บเป็น snapshot (C-2)
- **Used by features:** F-HR-CONFIG (this) · **Leave · OT/Shift · Shift & Roster · Attendance · Payroll · Performance · Welfare · Salary Structure** (8 ตัว — ทั้งหมด ⏳)
- **ทำไมเป็น Engine ไม่ใช่ Function:** ✅ pure (อ่านอย่างเดียว) · ✅ reusable ข้าม feature ≥2 (8 ตัว) · ✅ มี algorithm ชัด (precedence + interval matching) → tie-breaker 3/3
- **Iron rule check:** ✅ pure · ✅ ไม่มีศัพท์ HTTP · ✅ ปลายทางเรียกผ่าน `API-13` ไม่เรียก engine ตรง

### ENG-HRCFG-02: `hr-period-generator` — **NEW · status DRAFT (register Phase 2 — LD-03)**
- **code:** `hr-period-generator` · **category:** `calendar-calculation`
- **input schema:** `{ year, frequency: "monthly"|"semi_monthly", cutDay: "1".."31"|"eom", payDay: "1".."31"|"eom" }`
- **output schema:** `{ periods: [{ periodCode, dateFrom, dateTo, payDate }] }`
- **logic outline:**
  1. แปลง `cutDay`/`payDay` เป็นวันจริงของแต่ละเดือน — **`31` ในเดือน 30 วันหรือกุมภาพันธ์ → fallback สิ้นเดือน** (EA-10)
  2. รองรับ **ปีอธิกสุรทิน** (29 ก.พ.) (EA-09)
  3. งวด n = `[วันตัดของเดือนก่อน + 1, วันตัดของเดือนนี้]` · `payDate` = วันจ่ายของเดือนนั้น
  4. `monthly` → 12 งวด · `semi_monthly` → 24 งวด
  5. คืนผลอย่างเดียว — **ไม่เขียน DB** (persist เป็นหน้าที่ของ FN-13)
- **Used by features:** F-HR-CONFIG (this) · **Payroll (W4) และ Attendance (W1/C)** จะใช้ตรรกะเดียวกันตอนตรวจงวด → candidate สำหรับ reuse
- **ทำไมเป็น Engine:** ✅ pure (ไม่มี I/O) · ✅ reusable ≥2 features · ✅ algorithm ชัด → 3/3
- **Iron rule check:** ✅ pure · ✅ ไม่มีศัพท์ HTTP

### Engine ภายนอกที่ **เรียกใช้ ไม่สร้างใหม่** (baseline — catalog §0)

| Engine | สถานะ | ใช้ที่ | ข้อห้าม |
|---|---|---|---|
| **ENG-CSQ 7C** | EXISTING ✅ | FN-16 (6 event · ท่อ SecC) | ห้ามคำนวณมูลค่าเอง · ห้ามสร้างคอลัมน์ผลรายท่อ · ห้ามประกาศ OC/DC-เอกสาร/SC |
| **Policy Center — Audit Trail** | EXISTING ✅ | FN-17 (ทุก mutation) | ห้ามสร้างตาราง audit เอง · ห้ามลบ/แก้ log |
| **Policy Center — Roles & Permissions / Data Masking** | EXISTING ✅ | ทุก endpoint (middleware) | ห้ามทำ permission เอง |
| **DOA Engine** | EXISTING ✅ — **ไม่ใช้รอบนี้** | — | ถ้า OQ-01 เคาะว่าต้องมี approval → เรียก `GET /doa/resolve` ที่ **FN-06 (Draft→Scheduled) จุดเดียว** · ห้าม hardcode chain · ห้ามสร้าง approval ใหม่ |
| **Document Configuration · ENG-NOTIFY · Operation Process** | EXISTING ✅ — **ไม่ใช้** | — | ดู `5_DECLARATIONS/NOT_NEEDED.md` |

---

## §3.3 API ↔ Logic Trace Table (Phase 3.5 Anchor)

| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01 GET /items | FN-01 | — |
| API-02 GET /items/:id | FN-01 | — |
| **API-03 POST /items** | FN-02, FN-04, FN-05, FN-17 | — |
| **API-04 POST /items/:id/versions** | FN-03, FN-05, FN-17 | — |
| **API-05 PUT /versions/:id** | FN-04, FN-05, FN-17 | — |
| **API-06 POST /versions/:id/publish** | FN-06, FN-05, FN-20, FN-19, FN-17, FN-16 | — |
| **API-07 POST /versions/:id/cancel** | FN-07, FN-19, FN-17, FN-16 | — |
| **API-08 POST /versions/:id/discard** | FN-08, FN-17 | — |
| **API-09 POST /items/:id/deactivate** | FN-09, FN-12, FN-17, FN-16 | — |
| **API-10 POST /items/:id/reactivate** | FN-10, FN-05, FN-20, FN-06, FN-17, FN-16 | — |
| API-11 GET /items/:id/usage | FN-12 | — |
| API-12 GET /items/:id/history | FN-11 | — |
| API-13 GET /resolve | — | **ENG-HRCFG-01** |
| **API-14 POST /period-rules/:id/periods/generate** | FN-13, FN-17 | **ENG-HRCFG-02** |
| **API-15 POST /periods/:id/close** | FN-14, FN-17, FN-16 | — |
| **API-16 POST /periods/:id/reopen** | FN-15, FN-17 | — |
| API-17 GET /periods | FN-01 | — |
| *(scheduler job — ไม่ใช่ API)* | FN-06 (catch-up), FN-19, FN-17, FN-16 | — |
| *(nested)* FN-05 | FN-18 | — |

> **R8 Check:** mutation API ทั้ง 10 ตัว (API-03…API-10, API-14…API-16) มี ≥1 Function/Engine ✅
> **Orphan check:** FN-01…FN-20 ถูก trace ครบทุกตัว (FN-18 ผ่าน FN-05 · FN-19 ผ่าน FN-06/FN-07) ✅ · ENG-HRCFG-01 ผ่าน API-13 ✅ · ENG-HRCFG-02 ผ่าน API-14/FN-13 ✅ — **ไม่มี orphan**

---

## §3.4 Engine Candidates (ยังไม่สร้างรอบนี้ — ส่งให้ Architect)

> ประกาศไว้ไม่ให้หายเงียบ · **ไม่นับเป็น orphan** เพราะ **ยังไม่ implement** (ถูก gate ด้วย OQ)

| Candidate code | ทำอะไร | ปลดล็อกเมื่อ | ผลถ้าเคาะว่าต้องทำ |
|---|---|---|---|
| **`hr-policy-retro-engine`** | คำนวณผลย้อนหลังเมื่อแก้นโยบายคร่อมงวดที่ปิดแล้ว | **OQ-04 / OQ-STD-04** เคาะว่า "ต้อง retro" | Phase 4 · ต้องรื้อ BR-04 จาก "บล็อก" เป็น "อนุญาต + คำนวณย้อน" — กระทบ Payroll/Attendance โดยตรง |
| **`hr-eligibility-rule-engine`** | ตัดสินว่าค่าชุดไหนใช้กับพนักงานกลุ่มไหน (ประเภทจ้าง/ระดับ/แผนก) | **OQ-02 / OQ-STD-02** | Phase 3 · ต่อยอดจาก field `applies_to` ที่เผื่อไว้ (FN-30) — **ไม่ต้องรื้อ schema** |
| **(ยกระดับ)** `hr-config-resolve` → ผูก Rule Management | ทำให้ลำดับ resolve (BR-13) แก้ได้โดยไม่ deploy | **OQ-09** ยืนยันว่า BR-13 เป็น DYNAMIC จริง | Phase 3 · Phase 1 implement เป็น **ตารางลำดับ** อยู่แล้ว จึงยกระดับได้โดยไม่ refactor |

**สรุปสำหรับ Architect:** engine ที่จะ register จริงรอบนี้ = **`hr-config-resolve` + `hr-period-generator` (2 ตัว · Phase 2)** · candidate ที่รอ OQ = **`hr-policy-retro-engine` + `hr-eligibility-rule-engine` (2 ตัว)**

---

## §3.5 Logic Placement Compliance (Matrix check)

| Matrix # | Pattern | ควรอยู่ที่ | ในงานนี้ | ✅ |
|---|---|---|---|---|
| 1 | HTTP routing / parsing | 02_API | routing + query parsing เท่านั้น | ✅ |
| 2 | Field validation < 5 บรรทัด | 02_API | `code` regex · required · uuid · enum | ✅ |
| 3 | createX / updateX | 03_LOGIC §3.1 | FN-02, FN-03, FN-04 | ✅ |
| 4 | format/transform helper | 03_LOGIC §3.1 | FN-18, FN-19 | ✅ |
| 5 | validation รวมศูนย์ใช้ข้าม API | 03_LOGIC §3.1 | **FN-05** (ใช้โดย 5 API) | ✅ |
| 6 | pure calculation | 03_LOGIC §3.2 | **ENG-HRCFG-02** | ✅ |
| 7 | reusable ข้าม feature ≥2 | 03_LOGIC §3.2 | **ENG-HRCFG-01** (8 consumer) | ✅ |
| 8 | external integration | 03_LOGIC (wrap by API) | FN-16 (ENG-CSQ) · FN-17 (Audit Trail) — **wrapper ระดับ Function เพราะเป็นการเรียก baseline engine ที่มีอยู่แล้ว ไม่ใช่ engine ใหม่** | ✅ |
| 9 | state transition rule | 05_RULES (declarative) + 03_LOGIC (trigger) | 05_RULES §5.2 + FN-06/07/08/09/10/14/15 | ✅ |
| 10 | business constant / threshold | 05_RULES | BR-05/BR-06 ค่าจริงอยู่ `T_hr_legal_minimum` · โหมดอยู่ `T_hr_config_param` | ✅ |

**ตรวจซ้ำ:** ไม่มี `createX/updateX` แอบใน 02_API ✅ · ไม่มี pure calculation แอบใน 02_API ✅ · logic ตาม matrix #3–#8 อยู่ใน 03_LOGIC ครบ ✅
