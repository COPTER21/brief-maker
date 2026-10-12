# 05_RULES — F-HR-CONFIG · HR Configuration (ตั้งค่าHR)

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + State Machine + Permission + Validation + Edge Cases + Errors + Security + **ผลกระทบ 7C (CSQ)**
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด
> **🚨 ห้าม hardcode:** ค่าตัวเลขทุกตัวที่มาจากกฎหมายอยู่ใน `T_hr_legal_minimum` · โหมดของ rule อยู่ใน `T_hr_config_param`

---

## §5.1 Business Rules (BR)

### BR-01: ทุกเวอร์ชันต้องมีวันมีผล
- **Statement:** `config_version` ที่ `status ≠ 'draft'` ต้องมี `effective_date` เสมอ
- **Tag:** **FIXED** — invariant ของ HR-1 (ห้ามเปลี่ยน)
- **Enforced by:** DB CHECK (`status='draft' OR effective_date IS NOT NULL`) + `FN-06 publishVersion`
- **Error:** `BR_EFFECTIVE_DATE_REQUIRED` → **422** · ข้อความบนจอ: `ต้องกรอกวันมีผลก่อนบันทึก (บันทึกร่างไว้ก่อนได้)`
- **Rationale:** ตอบได้เสมอว่า "ณ วันนั้นบริษัทใช้กติกาอะไร" (P-1)

### BR-02: ห้ามแก้ทับเวอร์ชันที่ใช้อยู่
- **Statement:** เวอร์ชันที่ `status ∈ {scheduled, active, superseded}` **แก้ไม่ได้** — การแก้ = สร้างเวอร์ชันใหม่ (`API-04`) · เวอร์ชันที่ 2 ขึ้นไปต้องมี `change_reason` ≥10 ตัวอักษร
- **Tag:** **FIXED**
- **Enforced by:** `API-05` รับเฉพาะ `status='draft'` · `FN-03 createConfigVersion` · DB CHECK บน `change_reason`
- **Error:** `BR_VERSION_NOT_EDITABLE` → 422 · `BR_CHANGE_REASON_REQUIRED` → 422 · ข้อความ: `กรอกเหตุผลการเปลี่ยนอย่างน้อย 10 ตัวอักษร`
- **Rationale:** P-2 — หลักฐานเดิมต้องอยู่ครบ

### BR-03: ห้ามช่วงวันมีผลซ้ำ/คร่อมกัน
- **Statement:** เวอร์ชันของ item เดียวกัน + ขอบเขตบริษัทเดียวกัน ห้ามมี `effective_date` ซ้ำ และช่วง `[effective_date, effective_to]` ห้ามทับกัน
- **Tag:** **FIXED**
- **Enforced by:** **UNIQUE partial index** + **EXCLUDE (gist)** ที่ `T_hr_config_version` + `FN-06`
- **Error:** `BR_EFFECTIVE_DATE_OVERLAP` → 422 · ข้อความ: `มีเวอร์ชันที่ใช้วันมีผลนี้อยู่แล้ว — เลือกวันอื่น`
- **Rationale:** P-3 · เป็นด่านสุดท้ายกัน race (EA-01)

### BR-04: ห้ามตั้งวันมีผลย้อนเข้างวดที่ปิดแล้ว
- **Statement:** `effective_date` ต้องไม่ตกในงวดที่ `T_hr_pay_period.period_status='closed'`
- **Tag:** **CONFIGURABLE** → **Admin Panel** (`T_hr_config_param.lock_closed_period_enforced` · default `true`) 🤖
- **Enforced by:** `FN-20 assertNotInClosedPeriod` — **เรียก 2 ครั้ง (validate + commit ภายใน transaction)**
- **Error:** `BR_EFFECTIVE_IN_CLOSED_PERIOD` → 422 พร้อม `earliest_allowed_date` · ข้อความ: `ตั้งวันมีผลย้อนเข้างวด <งวด> ที่ปิดแล้วไม่ได้ — วันที่ตั้งได้เร็วที่สุดคือ <วันที่>`
- **Rationale:** ยอดที่จ่ายไปแล้วต้องไม่เปลี่ยนย้อนหลัง — **ทดแทน retro ที่ไม่ทำในรอบนี้** (P-9 · OQ-04)
- **นิยาม "งวดที่ปิดแล้ว":** ดู **BR-21**

### BR-05: ตัวคูณ OT ต้องไม่ต่ำกว่าขั้นต่ำตามกฎหมาย
- **Statement:** `multiplier` ≥ ค่าใน `T_hr_legal_minimum` ที่มีผล ณ `effective_date` ของเวอร์ชัน (OT วันทำงาน 1.5 · ทำงานวันหยุด 1.0 · OT วันหยุด 3.0)
- **Tag:** **CONFIGURABLE** → **Admin Panel** (ตาราง legal minimum ที่ **effective-dated เอง**) 🤖 · **ห้าม hardcode `1.5` ในโค้ด** (P-8)
- **Enforced by:** `FN-05 validateVersionPayload`
- **Error:** `BR_OT_BELOW_LEGAL_MIN` → 422 พร้อม `min_value` · ข้อความ: `ตัวคูณต่ำกว่าขั้นต่ำตามกฎหมายแรงงาน — …`
- **Open:** แหล่งอ้างอิงทางกฎหมาย → **OQ-10** (บล็อกก่อน go-live)

### BR-06: เตือนเมื่อโควตาลาต่ำกว่าขั้นต่ำ
- **Statement:** โควตาลาพักร้อน < `T_hr_legal_minimum['leave.annual_min_days']` (พนักงานอายุงานครบ 1 ปี) → **เตือน ไม่บล็อก** ผู้ใช้ยืนยันแล้วบันทึกได้
- **Tag:** **CONFIGURABLE** → **Admin Panel** (`leave_min_quota_mode` = `warn` | `block`) 🤖
- **Enforced by:** `FN-05` (คืน `warnings[]`) · UI แสดง modal `โควตาต่ำกว่าขั้นต่ำตามกฎหมาย`
- **Error/Warning:** `BR_LEAVE_QUOTA_BELOW_LEGAL_MIN` → **warning (200 + warnings[])** ไม่ใช่ error
- **Audit:** การยืนยันต่อทั้งที่ถูกเตือน **ต้องบันทึก** (Anomaly Report · R-03)

### BR-07: ไม่มี hard delete
- **Statement:** ไม่มีการลบข้อมูลถาวรใน feature นี้ — item เลิกใช้ผ่าน `status='inactive'` · ร่างทิ้งผ่าน `status='discarded'`
- **Tag:** **FIXED** — มติ audit append-only
- **Enforced by:** **ไม่มี DELETE endpoint ใน 02_API** · ไม่มีคอลัมน์ `deleted_at` · **ไม่ให้ DELETE grant แก่ role ของแอปบนตารางของ feature นี้** (บังคับที่ระดับสิทธิ์ DB)
- **Error:** — (ไม่มีทางเรียก)
- **Rationale:** หลักฐานทางกฎหมายแรงงานต้องอยู่ตลอดไป (R-02)

### BR-08: ต้องเห็น where-used ก่อนปิดใช้
- **Statement:** ปิดใช้ค่าที่มี consumer อ้างอยู่ ต้องแสดงรายการ + ให้ผู้ใช้ยืนยัน (`acknowledged_usage=true`) + เหตุผล ≥10 ตัวอักษร
- **Tag:** **FIXED**
- **Enforced by:** `API-09` precondition + `FN-09` + `FN-12` — **บังคับที่ระดับ API ไม่ใช่แค่ UI**
- **Error:** `BR_WHERE_USED_NOT_ACKNOWLEDGED` → 422 · `BR_DEACTIVATE_REASON_REQUIRED` → 422
- **Rationale:** #107 ทำให้ค่านี้เป็นศูนย์กลางของ 8 feature — ปิดโดยไม่รู้ผล = ทำสิทธิ์พนักงานพัง (R-07)

### BR-09: วันหยุดห้ามซ้ำใน บริษัท + ปี เดียวกัน
- **Statement:** `holiday_date` ห้ามซ้ำภายในขอบเขตบริษัทและปีเดียวกัน — **ตรวจข้ามชุดปฏิทิน (`location`) ด้วย**
- **Tag:** **FIXED**
- **Enforced by:** `FN-05` (DB unique ทำไม่ได้เพราะ scope บริษัทอยู่คนละตาราง)
- **Error:** `BR_HOLIDAY_DUPLICATE` → 422 · ข้อความ: `วันที่ <วันที่> ซ้ำกับ …`
- **Rationale:** ปลายทางกันวันซ้ำ = นับวันลา/เวลาผิด

### BR-10: รอบประเมินห้ามทับซ้อนในปีเดียวกัน
- **Statement:** ช่วง `[period_from, period_to]` ห้ามทับซ้อนกับรอบอื่นในปีและขอบเขตบริษัทเดียวกัน
- **Tag:** **FIXED** · **Enforced by:** `FN-05`
- **Error:** `BR_APPRAISAL_OVERLAP` → 422 · ข้อความ: `ช่วงวันทับซ้อนกับรอบ “<ชื่อรอบ>”`

### BR-11: วันตัดเวลา ≤ วันจ่าย
- **Statement:** `cut_day` ต้องไม่เกิน `pay_day` ในงวดเดียวกัน
- **Tag:** **FIXED** · **Enforced by:** `FN-05`
- **Error:** `BR_CUTDAY_AFTER_PAYDAY` → 422 · ข้อความ: `วันตัดเวลาต้องไม่เกินวันจ่ายในงวดเดียวกัน`

### BR-12: ยกยอดต้องมีวันหมดอายุ
- **Statement:** `carry_max ≥ 0` · ถ้า `carry_max > 0` ต้องมี `carry_expiry` และต้องอยู่ในปีถัดไป
- **Tag:** **FIXED** · **Enforced by:** DB CHECK + `FN-05`
- **Error:** `BR_CARRY_EXPIRY_REQUIRED` → 422 · ข้อความ: `ยกยอดมากกว่า 0 ต้องระบุวันหมดอายุยกยอด`

### BR-13: ลำดับ resolve — บริษัทลูกทับค่ากลาง
- **Statement:** เมื่อมีทั้งค่ากลาง (`shared`) และค่าเฉพาะบริษัท (`company`) ของ `code` เดียวกัน → **ใช้ค่าของบริษัทเสมอ** · ผลลัพธ์ต้องบอกที่มา (`resolved_from`)
- **Tag:** **DYNAMIC** → **Rule Management** 🤖 — **ยกเป็น OQ-09** (C23 escalation)
- **Enforced by:** **`ENG-HRCFG-01 hr-config-resolve`**
- **Implementation note (Phase 1):** implement เป็น **ตารางลำดับ precedence** ไม่ใช่ if-else ในโค้ด — เพื่อยกเป็น Rule Management ใน Phase 3 โดยไม่ต้อง refactor
- **Error:** — (ไม่บล็อก — เป็นการเลือกค่า)

### BR-14: audit append-only ทุก transition
- **Statement:** ทุก create / แก้ / publish / cancel / discard / deactivate / reactivate / close-period / reopen-period **ต้องเขียน Policy Center Audit Trail** พร้อม before/after
- **Tag:** **FIXED** · **Enforced by:** `FN-17 writeAuditEntry` (เรียกจากทุก mutation function)
- **กฎเหล็ก:** **เขียน audit ไม่สำเร็จ → rollback transaction ทั้งก้อน** (SLA-05)
- **Error:** `ERR_AUDIT_WRITE_FAILED` → 500 (พร้อม rollback)
- **ห้าม:** สร้างตาราง audit ของ feature เอง · ลบ/แก้ log

### BR-15: ทุก field ที่เป็นคน = combobox Employee Master
- **Statement:** `owner_employee_id`, `created_by`, `modified_by`, `closed_by` มาจาก Employee Master (avatar/icon → ชื่อ → ตำแหน่ง · แผนก) — **ห้ามพิมพ์ชื่ออิสระ**
- **Tag:** **FIXED** (#102) · **Enforced by:** UI combobox + API รับเฉพาะ uuid
- **Error:** `ERR_VALIDATION_FAILED` (ไม่ใช่ uuid) → 400
- **Data:** เก็บ **snapshot ชื่อ** คู่เสมอ (EA-13 · LD-4C-02)

### BR-16: ขั้นอายุงานต้องต่อเนื่อง
- **Statement:** milestone ต้องเรียงต่อเนื่อง ไม่ทับซ้อน ไม่มีช่องว่าง · ขั้นสุดท้าย `year_to = null` = "ขึ้นไป" (ไม่ถือว่ามีช่องว่าง)
- **Tag:** **FIXED** · **Enforced by:** `FN-05` (ตรวจทั้งชุดพร้อมกัน — DB constraint รายแถวทำไม่ได้)
- **Error:** `BR_MILESTONE_GAP_OR_OVERLAP` → 422 · ข้อความ: `ช่วงอายุงานทับซ้อนกันที่ขั้นที่ …` / `ช่วงอายุงานมีช่องว่างระหว่างขั้นที่ …`

### BR-17: กะ — เวลาออกและช่วงพัก
- **Statement:** `time_out > time_in` เว้นแต่ `overnight=true` · ช่วงพักทุกช่วงต้องอยู่ในช่วงกะ (รวมกรณีคร่อมเที่ยงคืน)
- **Tag:** **FIXED** · **Enforced by:** DB CHECK + `FN-05` + `FN-18 computeShiftHours`
- **Error:** `BR_SHIFT_TIME_INVALID` → 422 · ข้อความ: `เวลาออกต้องมากกว่าเวลาเข้า หรือติ๊ก “กะข้ามวัน”` / `ช่วงพักต้องอยู่ในช่วงเวลาของกะ`

### BR-18: `payroll_code` เป็น soft reference
- **Statement:** ประเภท/อัตราที่จ่ายค่าจ้าง **ควร** ระบุ `payroll_code` — ไม่บังคับ · **ห้ามผูกสูตรคำนวณเงินใด ๆ ที่ feature นี้**
- **Tag:** **CONFIGURABLE** → **Admin Panel** (`payroll_code_mode` = `warn` | `require`) 🤖
- **Enforced by:** `FN-05` (warning)
- **Warning:** `BR_PAYROLL_CODE_MISSING` → warnings[] · **OQ-03** (เปิดเป็น require เมื่อ Salary Structure พร้อม)

### BR-19: Draft/Scheduled ไม่ถูกเผยแพร่
- **Statement:** `resolve()` คืนเฉพาะเวอร์ชัน `status='active'` — Draft/Scheduled/Cancelled/Discarded/Inactive **ไม่ถูกส่งให้ปลายทาง**
- **Tag:** **FIXED** · **Enforced by:** `ENG-HRCFG-01` + `FN-01`
- **Error:** — (การกรอง ไม่ใช่ error)

### BR-20: ยกเลิกได้เฉพาะก่อนถึงวันมีผล
- **Statement:** เวอร์ชัน `scheduled` ยกเลิกได้ · เมื่อกลายเป็น `active` แล้ว **ยกเลิกไม่ได้** — ต้องสร้างเวอร์ชันใหม่แทน
- **Tag:** **FIXED** · **Enforced by:** `FN-07`
- **Error:** `BR_CANCEL_ONLY_BEFORE_EFFECTIVE` → 422 · UI: ปุ่มยกเลิกหายเมื่อ active

### BR-21: งวดที่ปิดแล้ว
- **Statement:** งวดที่ `period_status='closed'` **ล็อก** — ห้ามแก้ค่าที่กระทบงวดนั้น (เป็นนิยามที่ BR-04 ใช้) · การปิดต้องบันทึก `closed_by` + `closed_at` · การเปิดกลับต้องมี `reopen_reason` + audit · **ห้ามสร้างงวดทับปีที่มีงวดปิดแล้ว**
- **Tag:** **CONFIGURABLE** → **Admin Panel** (`reopen_period_requires_reason` · default `true`) 🤖
- **Enforced by:** `FN-13`, `FN-14`, `FN-15`, `FN-20`
- **Error:** `BR_PERIOD_ALREADY_CLOSED` · `BR_PERIOD_NOT_CLOSED` · `BR_REOPEN_REASON_REQUIRED` · `BR_PERIOD_CLOSED_CANNOT_REGENERATE` → 422

---

## §5.1b Business Rules — ผลกระทบ 7C (CSQ) ⭐ ตามข้อผูกพันใน `CSQ_BRIEF.md §5`

### BR-CSQ-01: ประกาศได้เฉพาะท่อ SecC
- **Statement:** feature นี้ยิง event เข้า ENG-CSQ ได้เฉพาะท่อ **SecC** · **ห้าม OC (มาจาก Operation Process) · DC ระดับเอกสาร (มาจาก DOA) · SC (สงวน)** — ประกาศซ้ำ = **register reject 422**
- **Enforced by:** `FN-16 emitCsqEvent` (whitelist ท่อ) · ตรวจตอน register profile
- **Rationale:** การเปลี่ยนนโยบาย = เปลี่ยนสิทธิ์/entitlement ของพนักงาน (ไม่ใช่ธุรกรรมที่เกิดมูลค่า → **ไม่ประกาศ EC/AC/FC** เพราะจะนับซ้ำกับ OT/Leave/Payroll)

### BR-CSQ-02: idempotency ของ event
- **Statement:** `idempotency_key = F-HR-CONFIG:{version_id|period_code}:{event_id}` — unique ต่อ (feature, ref, action)
- **Enforced by:** `FN-16` · สอดคล้องกับ `Idempotency-Key` ของ API (02_API §2.3)

### BR-CSQ-03: ห้ามส่งข้อมูลบุคคลดิบใน payload
- **Statement:** `changed_by` / `closed_by` ส่ง **`employee_id` เท่านั้น** — ห้ามส่งชื่อ/ตำแหน่ง/ข้อมูลบุคคล
- **Enforced by:** `FN-16` (สร้าง payload จาก id) · **D7 PII**

### BR-CSQ-04: reversal ไม่ลบผลเดิม
- **Statement:** การถอนเวอร์ชัน (`hrconfig.cancelled`) และการปิดใช้ (`hrconfig.deactivated`) **ไม่ลบ/ไม่แก้ผลเดิมที่ 7C** — เป็น event ใหม่ที่ชี้ `version_id` เดิม
- **Enforced by:** `FN-07`, `FN-09`

### BR-CSQ-05: ผลของ 7C ไม่อยู่ในตารางของ feature
- **Statement:** **ห้ามสร้างคอลัมน์ผลรายท่อ** (`is_secc_triggered` ฯลฯ) ในตารางของ feature — ผลอยู่ที่ `T_csq_stamp` ของ ENG-CSQ · **ห้ามคำนวณมูลค่าใด ๆ** ในหน้า HR Configuration (ENG-CSQ-02 เป็นเจ้าของการตีมูลค่า)
- **Enforced by:** schema review (04_DB) + code review

### Event ↔ Trigger map (**append กลับ `CSQ_BRIEF.md` แล้วตาม §5 checklist**)

| # | event_id | trigger point ใน FRD | ท่อ | BR ที่เกี่ยว |
|---|---|---|---|---|
| E1 | `hrconfig.published` | `03_LOGIC §3.1 FN-06 publishVersion` (Draft→Scheduled/Active) · `02_API-06` | SecC | BR-01, BR-03 |
| E2 | `hrconfig.effective` | `03_LOGIC §3.1 FN-06` (โหมด scheduler/lazy-resolve: Scheduled→Active · เวอร์ชันเดิม→Superseded) | SecC | BR-02, BR-19 |
| E3 | `hrconfig.cancelled` | `03_LOGIC §3.1 FN-07 cancelScheduledVersion` · `02_API-07` | SecC | BR-20 |
| E4 | `hrconfig.deactivated` | `03_LOGIC §3.1 FN-09 deactivateConfigItem` · `02_API-09` | SecC | BR-07, BR-08 |
| E5 | `hrconfig.reactivated` | `03_LOGIC §3.1 FN-10 reactivateConfigItem` · `02_API-10` | SecC | BR-04 |
| E6 | `hrconfig.period_closed` | `03_LOGIC §3.1 FN-14 closePayPeriod` · `02_API-15` | SecC `[DEFAULT — รอยืนยัน OQ-18]` | BR-21 |

> **event ใน FRD = 6 ตัว ⊆ CSQ_BRIEF §2 (6 ตัว) เป๊ะ — ไม่มี event เกินจาก brief** ✅
> **ไม่มี event `period_reopened`** (การเปิดงวดกลับบันทึกเป็น audit เท่านั้น) — เป็นข้อจำกัดที่รู้ตัว · ผลกระทบกับปลายทางระบุไว้ที่ `02_API §2.X C`

---

## §5.2 State Machine

### 5.2.1 `config_version` — 5 states

```
        create/บันทึกร่าง            publish (eff อนาคต)              ถึงวันมีผล (ระบบ)
   —  ─────────────────▶  Draft  ──────────────────────▶  Scheduled  ────────────────▶  Active
                            │                                │                            │
                 ทิ้งร่าง     │                    ยกเลิก + เหตุผล │            มีเวอร์ชันใหม่ถึงวัน │
                            ▼                                ▼                            ▼
                       Discarded                        Cancelled                    Superseded (read-only)
                            
   Draft ──publish (eff = วันนี้)──▶ Active
   Active / Scheduled ──ปิดใช้ (confirm + where-used)──▶ Inactive ──เปิดใช้กลับ (เวอร์ชันใหม่)──▶ Scheduled/Active
```

| From | To | Action | Allowed roles | Conditions | Function | Event |
|---|---|---|---|---|---|---|
| — | draft | create / save draft | hr_admin | มีชื่อค่า | FN-02, FN-04 | — |
| draft | scheduled | publish (eff อนาคต) | hr_admin | BR-01, BR-03, BR-04, BR-02 | FN-06 | `hrconfig.published` |
| draft | active | publish (eff = วันนี้) | hr_admin | เดียวกัน + ไม่มีเวอร์ชันชน | FN-06 | `published` + `effective` |
| draft | discarded | ทิ้งร่าง + confirm | hr_admin | — | FN-08 | — |
| scheduled | active | ถึงวันมีผล | **system** | อัตโนมัติ / lazy resolve | FN-06 (catch-up) | `hrconfig.effective` |
| scheduled | cancelled | ยกเลิก + เหตุผล | hr_admin | **ยังไม่ถึงวันมีผล** (BR-20) | FN-07 | `hrconfig.cancelled` |
| active | superseded | มีเวอร์ชันใหม่ถึงวันมีผล | **system** | set `effective_to` | FN-06 | `hrconfig.effective` (ของเวอร์ชันใหม่ · แนบ `superseded_version_id`) |
| active / scheduled | inactive | ปิดใช้ | hr_admin | BR-07, BR-08 + เหตุผล | FN-09 | `hrconfig.deactivated` |
| inactive | scheduled/active | เปิดใช้กลับ | hr_admin | ต้องมีวันมีผลใหม่ · BR-04 ยังบังคับ | FN-10 | `hrconfig.reactivated` |
| superseded | — | — | — | **read-only ตลอดไป** (หลักฐาน HR-1) | — | — |

### 5.2.2 `pay_period` — lifecycle ย่อย

| From | To | Action | Roles | Conditions | Function | Event |
|---|---|---|---|---|---|---|
| — | open | สร้างงวดทั้งปี | hr_admin | กติกา active · ปีนั้นไม่มีงวด closed | FN-13 | — |
| open | closed | ปิดงวด + confirm | hr_admin | — | FN-14 | `hrconfig.period_closed` |
| closed | open | เปิดงวดกลับ + เหตุผล | hr_admin | เหตุผล ≥10 ตัวอักษร | FN-15 | — (audit เท่านั้น) |

---

## §5.3 Permission Matrix

| Role | View list | View as-of | View history | View where-used | Create | Edit draft | Publish | Cancel | Deactivate | Reactivate | Gen periods | Close/Reopen period | Resolve | **Delete** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `hr_admin` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **❌ ไม่มี** |
| `hr_staff` | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | **❌** |
| `viewer` (หัวหน้า/ทั่วไป) | ✅ (เฉพาะ active ปัจจุบัน) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | **❌** |
| `service` (8 consumer) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ (API-13, API-17 เท่านั้น)** | **❌** |

- สิทธิ์ทั้งหมดมาจาก **Policy Center → Roles & Permissions** — feature ไม่ทำ permission เอง
- **บังคับที่ระดับ API เสมอ ไม่ใช่ซ่อนปุ่ม** (EA-15) · role ถูกถอนกลางทาง → `ERR_PERMISSION_REVOKED` 403 (PR-3)
- **ไม่มี role ใดในระบบที่ลบข้อมูลของ feature นี้ได้** (BR-07)

---

## §5.4 Field Validation Rules (VR-01…VR-30 · จาก BRD §9.2)

| VR | Field / Action | เงื่อนไข | ประเภท | Error code | ข้อความบนจอ (verbatim) |
|---|---|---|---|---|---|
| VR-01 | `effective_date` | ว่างขณะ publish | Error | `BR_EFFECTIVE_DATE_REQUIRED` | `ต้องกรอกวันมีผลก่อนบันทึก (บันทึกร่างไว้ก่อนได้)` |
| VR-02 | `effective_date` | ซ้อนช่วงกับเวอร์ชันอื่น | Error | `BR_EFFECTIVE_DATE_OVERLAP` | `มีเวอร์ชันที่ใช้วันมีผลนี้อยู่แล้ว — เลือกวันอื่น` |
| VR-03 | `effective_date` | อยู่ในงวดที่ปิด | Prevent | `BR_EFFECTIVE_IN_CLOSED_PERIOD` | `ตั้งวันมีผลย้อนเข้างวด <งวด> ที่ปิดแล้วไม่ได้ — วันที่ตั้งได้เร็วที่สุดคือ <วันที่>` |
| VR-04 | `change_reason` | `version_no ≥ 2` และ < 10 ตัวอักษร | Error | `BR_CHANGE_REASON_REQUIRED` | `กรอกเหตุผลการเปลี่ยนอย่างน้อย 10 ตัวอักษร` |
| VR-05 | `cancel/deactivate/reopen_reason` | < 10 ตัวอักษร | Error | `BR_*_REASON_REQUIRED` | `กรอกเหตุผลอย่างน้อย 10 ตัวอักษร` |
| VR-06 | `multiplier` | < ขั้นต่ำตามประเภท | Prevent | `BR_OT_BELOW_LEGAL_MIN` | `ตัวคูณต่ำกว่าขั้นต่ำตามกฎหมายแรงงาน — …` |
| VR-07 | `cap_hours_week` | ว่าง หรือ ≤ 0 | Error | `ERR_VALIDATION_FAILED` | `เพดานชั่วโมงต้องมากกว่า 0` |
| VR-08 | `quota_per_year` (ลาพักร้อน) | < ขั้นต่ำ | **Warning** | `BR_LEAVE_QUOTA_BELOW_LEGAL_MIN` | `โควตาลาพักร้อน <n> วันต่อปี ต่ำกว่าขั้นต่ำ <m>` |
| VR-09 | `quota_per_year` | = 0 โดยไม่ติ๊ก "ไม่จำกัด" | Error | `ERR_VALIDATION_FAILED` | `โควตาต้องไม่ติดลบ` / ต้องติ๊กไม่จำกัด |
| VR-10 | `paid_pct` | `paid_type='partial'` และไม่อยู่ 1–99 | Error | `ERR_VALIDATION_FAILED` | `เปอร์เซ็นต์ที่จ่ายต้องอยู่ระหว่าง 1–99` |
| VR-11 | `doc_note` | `need_doc=true` และว่าง | Error | `ERR_VALIDATION_FAILED` | `ระบุเอกสารที่ต้องแนบ` |
| VR-12 | `carry_expiry` | `carry_max > 0` และว่าง/ไม่อยู่ปีถัดไป | Error | `BR_CARRY_EXPIRY_REQUIRED` | `ยกยอดมากกว่า 0 ต้องระบุวันหมดอายุยกยอด` |
| VR-13 | milestone | ทับซ้อน / มีช่องว่าง | Error | `BR_MILESTONE_GAP_OR_OVERLAP` | `ช่วงอายุงานทับซ้อนกันที่ขั้นที่ …` / `ช่วงอายุงานมีช่องว่างระหว่างขั้นที่ …` |
| VR-14 | `time_out` vs `time_in` | ≤ และไม่ติ๊กข้ามวัน | Error | `BR_SHIFT_TIME_INVALID` | `เวลาออกต้องมากกว่าเวลาเข้า หรือติ๊ก “กะข้ามวัน”` |
| VR-15 | ช่วงพัก | อยู่นอกช่วงกะ | Error | `BR_SHIFT_TIME_INVALID` | `ช่วงพักต้องอยู่ในช่วงเวลาของกะ` |
| VR-16 | `workdays` | 0 วัน | Error | `ERR_VALIDATION_FAILED` | `เลือกวันทำงานอย่างน้อย 1 วัน` |
| VR-17 | `holiday_date` | ซ้ำใน บริษัท+ปี (ข้ามชุด) | Prevent | `BR_HOLIDAY_DUPLICATE` | `วันที่ <วันที่> …` |
| VR-18 | `source_date` | ประเภทชดเชยแต่ว่าง/ไม่มีจริง | Error | `ERR_VALIDATION_FAILED` | ระบุวันหยุดต้นทางของวันหยุดชดเชย |
| VR-19 | `cut_day` vs `pay_day` | ตัด > จ่าย | Error | `BR_CUTDAY_AFTER_PAYDAY` | `วันตัดเวลาต้องไม่เกินวันจ่ายในงวดเดียวกัน` |
| VR-20 | ช่วงประเมิน | ทับซ้อนรอบอื่นในปีเดียวกัน | Prevent | `BR_APPRAISAL_OVERLAP` | `ช่วงวันทับซ้อนกับรอบ “<ชื่อรอบ>”` |
| VR-21 | ช่วงเปิดกรอก | อยู่ก่อนช่วงประเมินเริ่ม | Error | `ERR_VALIDATION_FAILED` | `ช่วงเปิดกรอกต้องอยู่หลังหรือคร่อมช่วงประเมิน` |
| VR-22 | `companies[]` | `scope='company'` แต่ 0 บริษัท | Error | `ERR_VALIDATION_FAILED` | `เลือกบริษัทอย่างน้อย 1 บริษัท` |
| VR-23 | `code` | ซ้ำใน (`group`,`company_scope`) | Error | `BR_CONFIG_CODE_DUPLICATE` | `รหัสค่านี้มีอยู่แล้วในกลุ่ม …` |
| VR-24 | `name_th` | ว่าง หรือ > 80 ตัวอักษร | Error | `ERR_VALIDATION_FAILED` | `กรอกชื่อค่า (ไทย)` |
| VR-25 | `payroll_code` | ประเภทที่จ่ายแต่ว่าง | **Warning** | `BR_PAYROLL_CODE_MISSING` | (เตือนเบา — บันทึกได้) |
| VR-26 | ปุ่มบันทึกทุกจุด | กดซ้ำระหว่างประมวลผล | Prevent | — | ปุ่ม disable + loader (+ `Idempotency-Key`) |
| VR-27 | ปิดใช้ / ยกเลิก / ปิด-เปิดงวด | ไม่ผ่านหน้ายืนยัน | Prevent | — | modal ยืนยันทุกครั้ง |
| VR-28 | ปิดใช้ที่มี where-used | ไม่ได้ acknowledge | Prevent | `BR_WHERE_USED_NOT_ACKNOWLEDGED` | modal แสดงรายการก่อนยืนยัน |
| VR-29 | field ที่เป็นคน | พิมพ์ชื่ออิสระ | Prevent | `ERR_VALIDATION_FAILED` | combobox Employee Master เท่านั้น |
| VR-30 | `applies_to` | พยายามแก้ | Prevent | `ERR_FIELD_READ_ONLY` | read-only รอบนี้ (hook · OQ-02) |

### Cross-field rules
- `effective_to` ของทุกเวอร์ชัน **คำนวณโดยระบบเท่านั้น** (`FN-19`) — ไม่ใช่ user input
- `hours_per_day` ของกะ **คำนวณโดย `FN-18`** — ไม่ใช่ user input
- `resolve()` ต้องคืนค่าที่ `effective_date ≤ date ≤ effective_to` เสมอ — ถ้าไม่มี = 404 (ไม่ใช่คืนค่าล่าสุด)

---

## §5.5 Edge Cases

### §5.5.1 ยืนยันแล้ว (จาก BRD §10.1 · ☑ 15 ข้อ)

| ID | Scenario | Resolution | Error / ผล | Test |
|---|---|---|---|---|
| **EC-01** | ตั้งตัวคูณ OT 1.2x สำหรับ OT วันทำงาน | บล็อกที่ `FN-05` | `BR_OT_BELOW_LEGAL_MIN` · ค้างที่ขั้น 2 ของ wizard | AT-14 |
| **EC-02** | ตั้งวันมีผลย้อนเข้างวดที่ปิด | บล็อกที่ `FN-20` | `BR_EFFECTIVE_IN_CLOSED_PERIOD` + `earliest_allowed_date` | AT-31 |
| **EC-03** | เพิ่มวันหยุดซ้ำ (ในชุดและข้ามชุด) | บล็อกที่ `FN-05` | `BR_HOLIDAY_DUPLICATE` | AT-19 |
| **EC-04** | รอบประเมินคร่อมรอบเดิม | บล็อก | `BR_APPRAISAL_OVERLAP` | AT-24 |
| **EC-05** | โควตาลาต่ำกว่าขั้นต่ำ | **เตือน ไม่บล็อก** + บันทึกการยืนยัน | warning | AT-11 |
| **EC-06** | ปิดใช้ค่าที่มี consumer อ้างอยู่ | แสดง where-used + บังคับ acknowledge + เหตุผล | `BR_WHERE_USED_NOT_ACKNOWLEDGED` ถ้าข้าม | AT-29 |
| **EC-07** | milestone มีช่องว่าง/ทับซ้อน | บล็อก | `BR_MILESTONE_GAP_OR_OVERLAP` | AT-06 |
| **EC-08** | กะข้ามวันโดยไม่ติ๊ก "ข้ามวัน" | บล็อก | `BR_SHIFT_TIME_INVALID` | AT-15 |
| **EC-09** | ยกยอด > 0 ไม่มีวันหมดอายุ | บล็อก | `BR_CARRY_EXPIRY_REQUIRED` | AT-07 |
| **EC-10** | วันตัด > วันจ่าย | บล็อก | `BR_CUTDAY_AFTER_PAYDAY` | AT-20 |
| **EC-11** | เลือก "เฉพาะบริษัท" แต่ไม่เลือกบริษัท | บล็อก | `ERR_VALIDATION_FAILED` | AT-25 |
| **EC-12** | `effective_date` ซ้ำ/คร่อมเวอร์ชันเดิม | บล็อก (DB constraint เป็นด่านสุดท้าย) | `BR_EFFECTIVE_DATE_OVERLAP` | AT-38 |
| **EC-13** | จ่ายค่าจ้างแต่ไม่มี `payroll_code` | เตือนเบา บันทึกได้ | warning | AT-13 |
| **EC-14** | เปิดงวดที่ปิดแล้วกลับโดยไม่ให้เหตุผล | บล็อก + audit เมื่อสำเร็จ | `BR_REOPEN_REASON_REQUIRED` | AT-21 |
| **EC-15** | กดบันทึกซ้ำระหว่างประมวลผล | ปุ่ม disable + `Idempotency-Key` | 409 `ERR_DUPLICATE_IDEMPOTENCY_KEY` ถ้ายิงซ้ำ | AT-34 |

### §5.5.2 จาก Phase 2.5 Probing / AI Pattern Matching (BRD §10.2 · ☐ 17 ข้อ — BA confirm ที่ SOW3.7)

| ID | Probe | Scenario | Resolution (`[AI-DEFAULT]` ที่ FRD เลือก) | Test |
|---|---|---|---|---|
| **EA-01** | PR-1 | สองคนสร้างเวอร์ชันวันเดียวกันพร้อมกัน | **optimistic lock** (`version` + `If-Match`) + **unique/exclude constraint** เป็นด่านสุดท้าย → คนหลังได้ 409 ไม่ใช่เขียนทับ | TC-CC-01 |
| **EA-02** 🔺 | PR-2 / PR-9 | ปิดงวดขณะมีคนกำลังบันทึกเวอร์ชันที่มีผลในงวดนั้น | **re-validate BR-04 ตอน commit** ภายใน transaction + `FOR SHARE` บนแถวงวด → **OQ-13** | TC-CC-02 |
| **EA-03** | PR-2 | ปิดใช้ค่าขณะมีคนเปิด drawer แก้ค้างอยู่ | ตอน submit ตรวจ `item.status` → 422 `BR_ITEM_INACTIVE` พร้อมข้อความว่าค่าถูกปิดใช้แล้ว | TC-CC-03 |
| **EA-04** | — | scheduler ไม่ทำงานตรงวันมีผล | **lazy resolve** (สถานะคำนวณจาก `effective_date` ตอนอ่าน) + scheduler catch-up ย้อนตามลำดับวัน ไม่ข้าม → **LD-02** | TC-ST-01 |
| **EA-05** 🔺 | PR-8 | ยกเลิกเวอร์ชัน Scheduled ที่มีเวอร์ชันอื่นซ้อนอยู่ข้างหลัง | `FN-19` **คำนวณ `effective_to` ใหม่ทั้งชุด** จากเวอร์ชันที่ยังเหลือ → **OQ-14** | TC-ST-02 |
| **EA-06** | — | เปิดใช้กลับด้วยวันมีผลย้อนหลัง | **BR-04 ยังบังคับ** — บล็อกเหมือนกรณีปกติ | TC-ST-03 |
| **EA-07** | PR-6 | ปิดใช้ค่าที่มีแต่เวอร์ชัน Draft | ทำเป็น **discard ร่าง** ไม่ใช่ soft archive | TC-ST-04 |
| **EA-08** | — | กะข้ามวัน + ช่วงพักคร่อมเที่ยงคืน | `FN-18` ใช้เวลาเชิงเส้น (บวก 24 ชม.) ไม่ใช่ modulo 24 | TC-CL-01 |
| **EA-09** | — | ปีอธิกสุรทิน (29 ก.พ.) | `ENG-HRCFG-02` รองรับ — สร้างงวดและวันหมดอายุยกยอดถูกต้อง | TC-CL-02 |
| **EA-10** | — | วันตัด/จ่าย = 31 ในเดือน 30 วัน / ก.พ. | `ENG-HRCFG-02` **fallback เป็นสิ้นเดือน** | TC-CL-03 |
| **EA-11** | — | milestone ขั้นสุดท้าย `year_to = null` | `FN-05` ถือว่า "ขึ้นไป" — ไม่ถือว่ามีช่องว่าง | TC-CL-04 |
| **EA-12** | — | บริษัทที่ถูกปิดใช้ที่ Organization | soft ref + `company_name_snapshot` → ยังแสดงชื่อได้ ไม่พัง | TC-DI-01 |
| **EA-13** | — | พนักงานที่เป็นผู้แก้ไขลาออก | soft ref + `*_name_snapshot` → ประวัติยังแสดงชื่อได้ | TC-DI-02 |
| **EA-14** | — | ลบวันหยุดต้นทางที่มีวันชดเชยอ้างอยู่ | `FN-05` บล็อก + ชี้วันชดเชยที่อ้างอยู่ | TC-DI-03 |
| **EA-15** | PR-3 | เรียก API สร้าง/แก้ตรง ๆ โดยข้าม UI | **บังคับสิทธิ์ที่ระดับ API** → 403 `ERR_INSUFFICIENT_ROLE` / `ERR_PERMISSION_REVOKED` | TC-PR-01 |
| **EA-16** 🔺 | — | `resolve()` ไม่ส่งพารามิเตอร์ "วันที่" | **ปฏิเสธ 400 `ERR_RESOLVE_DATE_REQUIRED`** (ไม่ default เป็นวันนี้) → **OQ-15** | TC-XT-09 |
| **EA-17** | — | ปลายทาง cache ค่าข้ามวัน | `Cache-Control` หมดอายุที่เที่ยงคืน + invalidate เมื่อได้ `hrconfig.effective` · **ห้าม cache ข้ามวัน** | TC-XT-10 |
| *(เพิ่ม)* **EA-18** | PR-4 | network fail กลางทาง (server ทำแล้วแต่ response หาย) | retry ด้วย `Idempotency-Key` เดิม 3 ครั้ง exponential backoff → คืน response เดิม ไม่สร้างซ้ำ | TC-NF-01 |

---

## §5.6 Error Catalog

| Code | HTTP | i18n key | Cause |
|---|---|---|---|
| `ERR_VALIDATION_FAILED` | 400 | `error.validation.failed` | field-level validation |
| `ERR_RESOLVE_DATE_REQUIRED` | **400** | `error.resolve.date_required` | **`resolve()` ไม่ส่ง `date`** (EA-16 · OQ-15) |
| `ERR_INVALID_DATE` | 400 | `error.validation.date` | รูปแบบวันที่ผิด |
| `ERR_INVALID_QUERY_PARAMS` | 400 | `error.query.invalid` | query param ผิด |
| `ERR_NOT_AUTHENTICATED` | 401 | `error.auth.unauth` | ไม่มี/หมดอายุ token |
| `ERR_INSUFFICIENT_ROLE` | 403 | `error.auth.role` | role ไม่พอ |
| `ERR_PERMISSION_REVOKED` | 403 | `error.auth.revoked` | role ถูกถอนกลางทาง (PR-3) |
| `ERR_FIELD_READ_ONLY` | 403 | `error.field.readonly` | แก้ `applies_to` |
| `ERR_NOT_FOUND` | 404 | `error.notfound` | item/version ไม่มี |
| `ERR_CONFIG_NOT_FOUND` | 404 | `error.config.notfound` | `resolve()` ระบุ `code` แต่ไม่มีเวอร์ชัน active ณ วันนั้น |
| `ERR_STALE_DATA` | 409 | `error.concurrency.stale` | `If-Match` ไม่ตรง (PR-1/PR-2) |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | `error.idempotency.dup` | key เดิม body ต่าง (PR-7) |
| `BR_EFFECTIVE_DATE_REQUIRED` | 422 | `br.eff.required` | BR-01 |
| `BR_CHANGE_REASON_REQUIRED` | 422 | `br.reason.required` | BR-02 |
| `BR_VERSION_NOT_EDITABLE` | 422 | `br.version.locked` | BR-02 (แก้เวอร์ชันที่ไม่ใช่ draft) |
| `BR_EFFECTIVE_DATE_OVERLAP` | 422 | `br.eff.overlap` | BR-03 |
| `BR_EFFECTIVE_IN_CLOSED_PERIOD` | 422 | `br.eff.closed_period` | BR-04 + BR-21 |
| `BR_OT_BELOW_LEGAL_MIN` | 422 | `br.ot.legal_min` | BR-05 |
| `BR_LEAVE_QUOTA_BELOW_LEGAL_MIN` | **200 + warnings[]** | `br.leave.quota_warn` | BR-06 (**เตือน ไม่บล็อก**) |
| `BR_PAYROLL_CODE_MISSING` | **200 + warnings[]** | `br.payroll_code.warn` | BR-18 |
| `BR_WHERE_USED_NOT_ACKNOWLEDGED` | 422 | `br.whereused.ack` | BR-08 |
| `BR_DEACTIVATE_REASON_REQUIRED` | 422 | `br.deactivate.reason` | BR-08 |
| `BR_CANCEL_ONLY_BEFORE_EFFECTIVE` | 422 | `br.cancel.too_late` | BR-20 |
| `BR_CANCEL_REASON_REQUIRED` | 422 | `br.cancel.reason` | BR-20 |
| `BR_DISCARD_ONLY_DRAFT` | 422 | `br.discard.draft_only` | BR-07 |
| `BR_ITEM_INACTIVE` | 422 | `br.item.inactive` | แก้/สร้างเวอร์ชันบน item ที่ปิดใช้ (EA-03) |
| `BR_ITEM_NOT_INACTIVE` | 422 | `br.item.not_inactive` | reactivate item ที่ยัง active |
| `BR_CONFIG_CODE_DUPLICATE` | 422 | `br.code.duplicate` | VR-23 |
| `BR_HOLIDAY_DUPLICATE` | 422 | `br.holiday.duplicate` | BR-09 |
| `BR_APPRAISAL_OVERLAP` | 422 | `br.appraisal.overlap` | BR-10 |
| `BR_CUTDAY_AFTER_PAYDAY` | 422 | `br.period.cut_after_pay` | BR-11 |
| `BR_CARRY_EXPIRY_REQUIRED` | 422 | `br.carry.expiry` | BR-12 |
| `BR_MILESTONE_GAP_OR_OVERLAP` | 422 | `br.milestone.invalid` | BR-16 |
| `BR_SHIFT_TIME_INVALID` | 422 | `br.shift.time` | BR-17 |
| `BR_PERIOD_ALREADY_CLOSED` | 422 | `br.period.closed` | BR-21 |
| `BR_PERIOD_NOT_CLOSED` | 422 | `br.period.not_closed` | BR-21 |
| `BR_REOPEN_REASON_REQUIRED` | 422 | `br.period.reopen_reason` | BR-21 |
| `BR_PERIOD_CLOSED_CANNOT_REGENERATE` | 422 | `br.period.regen_blocked` | BR-21 |
| `BR_PERIOD_RULE_NOT_ACTIVE` | 422 | `br.period.rule_inactive` | สร้างงวดจากกติกาที่ยังไม่ active |
| `ERR_AUDIT_WRITE_FAILED` | 500 | `error.audit.write` | BR-14 (พร้อม rollback) |
| `ENG_ERR_INVALID_INPUT` | 500 | `error.engine.input` | input ของ ENG-HRCFG-01/02 ผิดสัญญา |

---

## §5.7 Security Bible Application

> Domains ที่ trigger: **D2 · D7 · D9 · D15 · D17 · D-CLASS** (จาก BRD §16 · preset **P6 HR/PII Sensitive**)

### D2: Authentication & Session
- ทุก endpoint ต้องมี JWT · service account ของ 8 consumer ใช้ token แยกที่มี scope เฉพาะ `API-13` / `API-17`
- **MFA แนะนำสำหรับ role `hr_admin`** (S02-02 · ○ Optional — นโยบายระดับแพลตฟอร์ม)

### D7: PII Protection
- field ที่อ้างถึงคน 4 ช่อง + snapshot ชื่อ = **Confidential + PII** → masking ตาม Policy Center
- **event payload ส่ง `employee_id` เท่านั้น ห้ามส่งชื่อดิบ** (BR-CSQ-03)
- **RTBF:** ⚠️ ห้ามลบแถวประวัติเวอร์ชัน — anonymize `*_name_snapshot` แทน · **ห้ามเปิด Dynamic Data Purging** บนตารางของ feature นี้

### D9: Audit Logging
- ทุก mutation → Policy Center Audit Trail พร้อม diff (before/after) · **append-only** · retention ≥7 ปี
- **เขียนไม่สำเร็จ = rollback** (BR-14 · SLA-05)

### D15: Admin Actions
- ทุก transition ของเวอร์ชันและงวดบันทึกผู้ทำ + เวลา + เหตุผล
- **การยืนยันต่อทั้งที่ถูกเตือน (BR-06)** ต้องบันทึกเป็น anomaly

### D17: Multi-Tenant Isolation
- PostgreSQL RLS ทุกตาราง · middleware ตรวจ `X-Tenant-Id` · **ห้าม query ข้าม tenant**

### D-CLASS: Data Classification (รายละเอียดที่ `04_DB §4.2` + `§4.6`)

| Layer | Confidential fields (4 + snapshot) | Restricted fields |
|---|---|---|
| API response | mask ถ้า role ไม่ผ่าน | **ไม่มีใน feature นี้** |
| UI display | แสดง `***` ถ้าไม่มีสิทธิ์ | — |
| Export | excluded column ถ้า role ไม่ผ่าน | — |
| Audit | log view + mutation | — |

**Wire points:** Policy Center → Data Classification · PDPA consent scope · **ไม่ต้อง wire Restricted Resources** (ไม่มี Restricted field)

### D5 (Financial) — **ไม่ trigger**
feature นี้ **ไม่มี amount field** — มีแต่ multiplier/quota/วัน ที่เป็นพารามิเตอร์นโยบาย · มูลค่าจริงเกิดที่ OT/Leave/Payroll · **บันทึกไว้เพื่อไม่ให้เข้าใจว่าลืม**

---

## §5.8 Compliance & Audit Requirements

| Requirement | Implementation |
|---|---|
| กฎหมายแรงงานไทย — ขั้นต่ำ OT | BR-05 + `T_hr_legal_minimum` (effective-dated) · **OQ-10** ยืนยันแหล่งอ้างอิง |
| กฎหมายแรงงานไทย — โควตาลาพักร้อนขั้นต่ำ | BR-06 (เตือน) + `T_hr_legal_minimum` |
| หลักฐานตอบข้อพิพาทแรงงาน | ประวัติเวอร์ชัน append-only (BR-14) + `API-12` + Transaction Report (BRD §18.6) |
| PDPA | D7 + Data Classification + **ห้าม purge** |
| Internal audit | Policy Center Audit Trail + Closing Report รายเดือน (BRD §18.4) |
| 7C compliance | BR-CSQ-01…05 · **SecC เท่านั้น** |

---

## §5.9 Functions Cut — "ไม่รองรับ" (14 รายการ · จาก BRD §14.6.3)

> **ตัดสินแล้ว — อย่าเผลอทำ** · ทุกข้อ **เห็นบนหน้าจอ** ผ่าน ⓘ `.tip` และมีที่อยู่ในเอกสาร ไม่หายเงียบ
> ครอบ **FN-40…FN-47, FN-51…FN-53 (11 FN)** และ **S-23…S-30, S-33…S-35 (11 scenario)**

| # | ไม่รองรับ | FN | Scenario | เหตุผล / เจ้าของจริง | OQ |
|---|---|---|---|---|---|
| NS-01 | approval workflow ตอนแก้ค่านโยบาย — **ไม่มี endpoint approve/reject และไม่มีปุ่มบนจอ** | FN-40 | S-23 | scope note ตัด · คุมด้วย `effective_date` + audit | OQ-01 |
| NS-02 | คำนวณย้อนหลัง (retro) | FN-41 | S-24 | บล็อกที่ BR-04 แทน · candidate `hr-policy-retro-engine` | OQ-04 |
| NS-03 | สูตรคำนวณเงินเดือน / earning code mapping | FN-42 | S-25 | Salary Structure + Payroll · ที่นี่มีแค่ `payroll_code` | OQ-03 |
| NS-04 | leave balance รายคน | FN-43 | S-26 | Leave (W2) เป็นเจ้าของ balance | OQ-HR-02 (ตอบแล้ว) |
| NS-05 | UI สลับบริษัท (company switcher) | FN-44 | S-27 | มี field company แต่ยังไม่ทำหน้าสลับ | OQ-HR-05 (ตอบแล้ว) |
| NS-06 | auto-import วันหยุดราชการ | FN-45 | S-28 | NICE (C-23) · รอบนี้กรอกมือ | — |
| NS-07 | แจ้งเตือนพนักงานเมื่อนโยบายเปลี่ยน | FN-46 | S-29 | ปลายทางประกาศ NTF เอง — **feature นี้ไม่ประกาศท่อ NTF** | OQ-05 |
| NS-08 | import/export config เป็นชุด | FN-47 | S-30 | pattern import เป็นของ Attendance (W1/C) · **PR-5 ไม่ activate** | — |
| NS-09 | eligibility ตามประเภทจ้าง/ระดับ/แผนก | (FN-30 hook) | S-22 | รอบนี้ระดับบริษัท · field `applies_to` เผื่อไว้ · candidate `hr-eligibility-rule-engine` | OQ-02 |
| NS-10 | หน้าตั้งค่าของ feature HR อื่น | — | — | ทุก feature อ้างมาที่นี่ | **#107** |
| NS-11 | ลบค่าถาวร (hard delete) | FN-24 (negative) | S-18 | มติ audit append-only — **ไม่มี DELETE endpoint** | — |
| NS-12 | probation / notice period | FN-51 | S-33 | นอก 6 กลุ่มค่า · On/Offboard + Employee Movement (W3) | OQ-06 |
| NS-13 | calculation frequency (รายสัปดาห์/ปักษ์) | FN-52 | S-34 | Payroll (W4) · ที่นี่หยุดที่รอบจ่าย | OQ-07 |
| NS-14 | Time Profile (มัดชุดค่าให้กลุ่มพนักงาน) | FN-53 | S-35 | รอบนี้ระดับบริษัท | OQ-02 |
