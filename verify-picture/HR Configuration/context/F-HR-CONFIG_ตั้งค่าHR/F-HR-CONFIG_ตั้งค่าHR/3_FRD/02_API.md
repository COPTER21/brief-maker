# 02_API — F-HR-CONFIG · HR Configuration (ตั้งค่าHR)

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts + **Cross-Module Contract (สัญญากับ 8 feature ปลายทาง)**
> **🚨 Iron Rule:** ห้ามมี business logic > 5 บรรทัดที่นี่ — ย้ายไป `03_LOGIC §3.1`
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน `03_LOGIC §3.3`
> **🚨 BR-07:** **ไม่มี DELETE endpoint ใน feature นี้แม้แต่ตัวเดียว** — การเลิกใช้ทำผ่าน `POST …/deactivate` เท่านั้น

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth |
|---|---|---|---|---|
| F-HR-CONFIG-API-01 | GET | `/api/v1/hr-config/items` | List ค่าตามกลุ่ม + filter + **as-of date** | required |
| F-HR-CONFIG-API-02 | GET | `/api/v1/hr-config/items/:id` | รายละเอียดค่า + เวอร์ชันปัจจุบัน/ถัดไป | required |
| F-HR-CONFIG-API-03 | POST | `/api/v1/hr-config/items` | สร้างค่าใหม่ + เวอร์ชันแรก (Draft) | required (hr_admin) |
| F-HR-CONFIG-API-04 | POST | `/api/v1/hr-config/items/:id/versions` | สร้าง**เวอร์ชันใหม่** (copy payload เดิม) | required (hr_admin) |
| F-HR-CONFIG-API-05 | PUT | `/api/v1/hr-config/versions/:id` | แก้เวอร์ชัน — **เฉพาะ `status='draft'`** | required (hr_admin) |
| F-HR-CONFIG-API-06 | POST | `/api/v1/hr-config/versions/:id/publish` | ตั้งวันมีผล → Scheduled/Active | required (hr_admin) |
| F-HR-CONFIG-API-07 | POST | `/api/v1/hr-config/versions/:id/cancel` | ยกเลิกเวอร์ชันที่รอมีผล | required (hr_admin) |
| F-HR-CONFIG-API-08 | POST | `/api/v1/hr-config/versions/:id/discard` | ทิ้งร่าง | required (hr_admin) |
| F-HR-CONFIG-API-09 | POST | `/api/v1/hr-config/items/:id/deactivate` | ปิดใช้ (soft archive) | required (hr_admin) |
| F-HR-CONFIG-API-10 | POST | `/api/v1/hr-config/items/:id/reactivate` | เปิดใช้กลับ (สร้างเวอร์ชันใหม่) | required (hr_admin) |
| F-HR-CONFIG-API-11 | GET | `/api/v1/hr-config/items/:id/usage` | where-used (ใครใช้ค่านี้) | required |
| F-HR-CONFIG-API-12 | GET | `/api/v1/hr-config/items/:id/history` | ประวัติเวอร์ชัน (timeline) | required |
| **F-HR-CONFIG-API-13** | **GET** | **`/api/v1/hr-config/resolve`** | **สัญญาหลักกับ 8 feature ปลายทาง** — ค่าที่ Active ณ วันที่ | required (service or user) |
| F-HR-CONFIG-API-14 | POST | `/api/v1/hr-config/period-rules/:id/periods/generate` | สร้างงวดทั้งปีจากกติกา | required (hr_admin) |
| F-HR-CONFIG-API-15 | POST | `/api/v1/hr-config/periods/:id/close` | ปิดงวด | required (hr_admin) |
| F-HR-CONFIG-API-16 | POST | `/api/v1/hr-config/periods/:id/reopen` | เปิดงวดกลับ (ต้องมีเหตุผล) | required (hr_admin) |
| F-HR-CONFIG-API-17 | GET | `/api/v1/hr-config/periods` | list งวด + สถานะ (ปลายทางอ่านได้) | required |
| **— (ไม่มี)** | ~~DELETE~~ | — | **ไม่มี endpoint ลบถาวรใด ๆ** (BR-07) | — |

---

## §2.2 Per-API Contract

### F-HR-CONFIG-API-01: GET /api/v1/hr-config/items

| Field | Value |
|---|---|
| **id** | F-HR-CONFIG-API-01 · **method** GET · **auth** required |
| **roles** | hr_admin, hr_staff, viewer (viewer เห็นเฉพาะ `active` ปัจจุบัน · ไม่มี `as_of`) |
| **rate-limit** | default (100/min) |

**Request — Query params:**
- `group` (optional): `leave_type` \| `ot_rate` \| `shift_pattern` \| `holiday_calendar` \| `period_rule` \| `appraisal_cycle`
- `status` (optional): `active` \| `inactive`
- `company_id` (optional, uuid) · `q` (optional, ค้นหาชื่อ/รหัส)
- **`as_of` (optional, date)** — ดูค่าที่มีผล ณ วันนั้น (ไม่ส่ง = วันนี้) · **viewer ส่งไม่ได้ → 403**
- `limit` (default 20, max 100) · `offset` (default 0) · `sort`
**Headers:** `X-Tenant-Id` (required)

**Response 200:**
```json
{
  "data": [{
    "id": "uuid", "code": "LV-VAC", "name_th": "ลาพักร้อน", "group": "leave_type",
    "status": "active",
    "company_scope": "shared", "companies": [],
    "current_version": { "version_id": "uuid", "version_no": 2, "effective_date": "2025-01-01", "effective_to": "2026-12-31", "status": "active", "summary": "โควตา 6 วัน/ปี" },
    "next_version":    { "version_id": "uuid", "version_no": 3, "effective_date": "2027-01-01", "status": "scheduled" },
    "owner": { "employee_id": "uuid", "name": "กมลชนก ใจดี" },
    "updated_at": "2026-08-20T09:12:00Z"
  }],
  "total": 7, "limit": 20, "offset": 0,
  "as_of": "2026-08-28"
}
```
**Errors:** 400 `ERR_INVALID_QUERY_PARAMS` · 401 `ERR_NOT_AUTHENTICATED` · 403 `ERR_INSUFFICIENT_ROLE`
**Preconditions:** — · **Side effects:** — (read-only)
**Calls (Logic):** `F-HR-CONFIG-FN-01 buildConfigListQuery` → `03_LOGIC §3.1`

---

### F-HR-CONFIG-API-02: GET /api/v1/hr-config/items/:id

**roles:** hr_admin, hr_staff, viewer · **Query:** `as_of` (optional)
**Response 200:** item + `current_version` (พร้อม payload เต็มตาม `group`) + `next_version` + `versions_count` + `usage_count`
**Errors:** 404 `ERR_NOT_FOUND` · 403
**Side effects:** — · **Calls (Logic):** `FN-01`

---

### F-HR-CONFIG-API-03: POST /api/v1/hr-config/items

| Field | Value |
|---|---|
| **roles** | hr_admin เท่านั้น |
| **Headers** | `X-Tenant-Id` (required) · **`Idempotency-Key` (required)** |

**Body:**
```json
{
  "code": "LV-VAC", "name_th": "ลาพักร้อน", "name_en": "Annual Leave",
  "group": "leave_type",
  "company_scope": "shared", "company_ids": [],
  "payroll_code": null,
  "owner_employee_id": "uuid",
  "note": null,
  "payload": { "unit": "day", "paid_type": "paid", "quota_per_year": 6, "...": "ตาม group" },
  "save_as_draft": true
}
```
**Validation (field-level ≤5 บรรทัด):** `code` required + `^[A-Z0-9-]+$` · `name_th` required ≤80 · `group` required enum · `owner_employee_id` required uuid
→ **validation เชิงธุรกิจทั้งหมดอยู่ที่ `F-HR-CONFIG-FN-05 validateVersionPayload`**

**Response 201:** `{ "item_id": "uuid", "version_id": "uuid", "version_no": 1, "status": "draft" }`
**Errors:** 400 `ERR_VALIDATION_FAILED` · 403 `ERR_INSUFFICIENT_ROLE` · 409 `ERR_DUPLICATE_IDEMPOTENCY_KEY` · 422 `BR_CONFIG_CODE_DUPLICATE`
**Preconditions:** `code` ไม่ซ้ำใน (`group`, `company_scope`)
**Side effects:** INSERT `T_hr_config_item` (+ `T_hr_config_item_company`) · INSERT `T_hr_config_version` (draft) · INSERT payload table · **write audit (Policy Center)** · **ไม่ยิง event** (draft ยังไม่กระทบสิทธิ์)
**Calls (Logic):** `FN-02 createConfigItem` · `FN-04 saveDraftVersion` · `FN-05 validateVersionPayload` · `FN-17 writeAuditEntry`

---

### F-HR-CONFIG-API-04: POST /api/v1/hr-config/items/:id/versions

**Purpose:** **การ "แก้ไข" ค่าที่ Active = เรียก endpoint นี้** — ไม่มีทางแก้ทับ (BR-02 · P-2)
**roles:** hr_admin · **Headers:** `Idempotency-Key` (required)
**Body:** `{ "copy_from_version_id": "uuid|null", "payload": {…}, "save_as_draft": true }`
**Response 201:** `{ "version_id": "uuid", "version_no": 3, "status": "draft", "copied_from": "uuid" }`
**Errors:** 403 · 404 · 409 `ERR_STALE_DATA` · 422 `BR_ITEM_INACTIVE` (ค่าปิดใช้อยู่ → ต้อง reactivate ก่อน)
**Preconditions:** item `status='active'`
**Side effects:** INSERT `T_hr_config_version` (draft) + payload row (copy) · write audit
**Calls (Logic):** `FN-03 createConfigVersion` · `FN-05` · `FN-17`

---

### F-HR-CONFIG-API-05: PUT /api/v1/hr-config/versions/:id

**Purpose:** แก้เวอร์ชัน **เฉพาะที่ `status='draft'`** — เวอร์ชันที่ scheduled/active/superseded **แก้ไม่ได้เด็ดขาด**
**roles:** hr_admin · **Headers:** `If-Match: <updated_at>` (required — optimistic lock PR-2)
**Body:** `{ "name_th": "...", "company_scope": "...", "company_ids": [...], "payload": {...} }`
**Response 200:** version object
**Errors:** 409 `ERR_STALE_DATA` · **422 `BR_VERSION_NOT_EDITABLE`** (status ≠ draft — บังคับ BR-02) · 403
**Side effects:** UPDATE draft row + payload · write audit · **ไม่ยิง event**
**Calls (Logic):** `FN-04 saveDraftVersion` · `FN-05` · `FN-17`

---

### F-HR-CONFIG-API-06: POST /api/v1/hr-config/versions/:id/publish ⭐

**Purpose:** ตั้งวันมีผล → Draft → **Scheduled** (อนาคต) หรือ **Active** (วันนี้)
**roles:** hr_admin · **Headers:** `Idempotency-Key` (required) · `If-Match` (required)
**Body:**
```json
{ "effective_date": "2027-01-01", "change_reason": "ปรับตามมติคณะกรรมการ 2026-08-15", "confirm_below_legal_min": false }
```
**Validation (field-level):** `effective_date` required date · `change_reason` required เมื่อ `version_no >= 2` (≥10 ตัวอักษร)

**Response 200:**
```json
{ "version_id":"uuid", "status":"scheduled", "effective_date":"2027-01-01",
  "superseded_version_id":null, "effective_to_of_previous":"2026-12-31",
  "warnings":[{"code":"BR_LEAVE_QUOTA_BELOW_LEGAL_MIN","message":"โควตา 4 วันต่อปี ต่ำกว่าขั้นต่ำ 6"}] }
```
**Errors:**
- 400 `ERR_VALIDATION_FAILED`
- 403 `ERR_INSUFFICIENT_ROLE` / `ERR_PERMISSION_REVOKED` (PR-3 — ตรวจ role ที่ mutation time)
- 409 `ERR_STALE_DATA` / `ERR_DUPLICATE_IDEMPOTENCY_KEY`
- **422 `BR_EFFECTIVE_DATE_REQUIRED`** (BR-01) · **`BR_EFFECTIVE_DATE_OVERLAP`** (BR-03) · **`BR_EFFECTIVE_IN_CLOSED_PERIOD`** (BR-04 — response แนบ `earliest_allowed_date`) · **`BR_OT_BELOW_LEGAL_MIN`** (BR-05 — แนบ `min_value`) · `BR_CHANGE_REASON_REQUIRED` (BR-02) · `BR_MILESTONE_GAP_OR_OVERLAP` (BR-16) · `BR_CARRY_EXPIRY_REQUIRED` (BR-12) · `BR_SHIFT_TIME_INVALID` (BR-17) · `BR_HOLIDAY_DUPLICATE` (BR-09) · `BR_APPRAISAL_OVERLAP` (BR-10) · `BR_CUTDAY_AFTER_PAYDAY` (BR-11)

**Preconditions:** version `status='draft'` · payload ผ่าน `FN-05` · **`FN-20 assertNotInClosedPeriod` ต้องผ่าน — ตรวจซ้ำ ณ commit ภายใน transaction พร้อม row lock บน `T_hr_pay_period`** (PR-2/PR-9 · OQ-13)
**Side effects:** UPDATE version → `scheduled`/`active` · UPDATE เวอร์ชันก่อนหน้า `effective_to` (และ `superseded` ถ้ามีผลทันที) · **write audit** · **emit `hrconfig.published` (SecC)** และถ้ามีผลทันที emit `hrconfig.effective` (SecC)
**Calls (Logic):** `FN-06 publishVersion` · `FN-05` · `FN-20` · `FN-19 computeEffectiveWindow` · `FN-17` · `FN-16 emitCsqEvent`

---

### F-HR-CONFIG-API-07: POST /api/v1/hr-config/versions/:id/cancel

**Body:** `{ "cancel_reason": "ตั้งวันผิด ต้องเลื่อนออกไป" }` (≥10 ตัวอักษร)
**Response 200:** `{ "version_id":"uuid", "status":"cancelled", "recomputed_effective_to": {...} }`
**Errors:** 422 **`BR_CANCEL_ONLY_BEFORE_EFFECTIVE`** (BR-20 — เวอร์ชัน active แล้ว) · 422 `BR_CANCEL_REASON_REQUIRED` · 403 · 409
**Side effects:** UPDATE → `cancelled` · **re-compute `effective_to` ของเวอร์ชันก่อนหน้า** จากเวอร์ชันถัดไปที่ยังเหลือ (EA-05 · OQ-14) · write audit · **emit `hrconfig.cancelled` (SecC)**
**Calls (Logic):** `FN-07 cancelScheduledVersion` · `FN-19` · `FN-17` · `FN-16`

---

### F-HR-CONFIG-API-08: POST /api/v1/hr-config/versions/:id/discard

**Purpose:** ทิ้งร่าง (Draft → Discarded) — **ไม่ใช่การลบ** (แถวยังอยู่ · BR-07)
**Errors:** 422 `BR_DISCARD_ONLY_DRAFT` · 403
**Side effects:** UPDATE → `discarded` · write audit · **ไม่ยิง event** (ร่างไม่เคยกระทบสิทธิ์)
**Calls (Logic):** `FN-08 discardDraftVersion` · `FN-17`

---

### F-HR-CONFIG-API-09: POST /api/v1/hr-config/items/:id/deactivate

**Body:** `{ "deactivate_reason": "นโยบายนี้ยกเลิกตั้งแต่ปี 2570", "acknowledged_usage": true }`
**Preconditions:** **client ต้องเรียก `API-11` ดู where-used ก่อน** และส่ง `acknowledged_usage=true` — ถ้าไม่ส่ง → **422 `BR_WHERE_USED_NOT_ACKNOWLEDGED`** (บังคับ BR-08 ที่ระดับ API ไม่ใช่แค่ UI)
**Response 200:** `{ "item_id":"uuid", "status":"inactive", "usage_count": 2 }`
**Errors:** 422 `BR_WHERE_USED_NOT_ACKNOWLEDGED` / `BR_DEACTIVATE_REASON_REQUIRED` · 403 · 409
**Side effects:** UPDATE item → `inactive` · version ที่ active → `inactive` · write audit · **emit `hrconfig.deactivated` (SecC)** พร้อม `where_used_count`
**Calls (Logic):** `FN-09 deactivateConfigItem` · `FN-12 buildWhereUsedList` · `FN-17` · `FN-16`

---

### F-HR-CONFIG-API-10: POST /api/v1/hr-config/items/:id/reactivate

**Body:** `{ "effective_date": "2027-01-01", "change_reason": "กลับมาใช้นโยบายเดิมตามมติ …", "payload": {…} }`
**Purpose:** เปิดใช้กลับ = **สร้างเวอร์ชันใหม่พร้อมวันมีผล** ไม่ใช่ revert ของเดิม
**Errors:** 422 `BR_EFFECTIVE_IN_CLOSED_PERIOD` (BR-04 ยังบังคับ · EA-06) · `BR_ITEM_NOT_INACTIVE` · 403
**Side effects:** UPDATE item → `active` · INSERT version ใหม่ · write audit · **emit `hrconfig.reactivated` (SecC)**
**Calls (Logic):** `FN-10 reactivateConfigItem` · `FN-05` · `FN-20` · `FN-17` · `FN-16`

---

### F-HR-CONFIG-API-11: GET /api/v1/hr-config/items/:id/usage

**Response 200:**
```json
{ "item_id":"uuid", "usage_count":2,
  "consumers":[
    {"consumer_feature":"leave","display_name":"การลา","link_status":"pending","usage_note":"ประเภทลา + กติกานับวัน","deeplink":"#/leave"},
    {"consumer_feature":"payroll","display_name":"เงินเดือน","link_status":"pending","usage_note":"รอบจ่าย","deeplink":"#/payroll"}
  ],
  "current_version_read_by_consumers":{"version_id":"uuid","effective_date":"2025-01-01"} }
```
**Side effects:** — (read-only) · **ห้ามคืนข้อมูลภายในของ consumer** (LD-4C-02)
**Calls (Logic):** `FN-12 buildWhereUsedList`

---

### F-HR-CONFIG-API-12: GET /api/v1/hr-config/items/:id/history

**Response 200:** array ของเวอร์ชัน (ทุกสถานะรวม superseded/cancelled/discarded) เรียงตาม `effective_date` DESC พร้อม `value_diff[{field, old, new}]` · `modified_by` (+ชื่อ snapshot) · `change_reason`
**Side effects:** — · **read-only ตลอดไป — ไม่มี endpoint แก้/ลบประวัติ** (BR-14 · P-4)
**Calls (Logic):** `FN-11 buildVersionHistory`

---

### F-HR-CONFIG-API-13: GET /api/v1/hr-config/resolve ⭐ **สัญญากับ 8 feature ปลายทาง**

| Field | Value |
|---|---|
| **id** | F-HR-CONFIG-API-13 · GET · auth required (service account หรือ user) |
| **roles** | ทุก role ที่ผ่าน auth + service accounts ของ 8 feature |
| **rate-limit** | **สูงกว่าปกติ (hot path)** — 2,000/min ต่อ service account |

**Request — Query params:**

| param | required | หมายเหตุ |
|---|---|---|
| `date` | **✅ บังคับเสมอ** | วันที่ของเหตุการณ์ทางธุรกิจ — **ไม่ส่ง = 400 `ERR_RESOLVE_DATE_REQUIRED`** (`[AI-DEFAULT]` · OQ-15) |
| `company_id` | ✅ เมื่อ tenant มีบริษัทลูก | ใช้ตัดสิน BR-13 (บริษัทลูกทับค่ากลาง) |
| `group` | ⬜ | ไม่ส่ง = คืนทุกกลุ่ม |
| `code` | ⬜ | เจาะค่าเดียว |

**Response 200:**
```json
{
  "as_of": "2026-09-01", "company_id": "uuid",
  "items": [{
    "code": "LV-VAC", "group": "leave_type", "name_th": "ลาพักร้อน",
    "version_id": "uuid", "version_no": 2,
    "effective_window": { "from": "2025-01-01", "to": "2026-12-31" },
    "resolved_from": "shared",
    "payload": { "unit":"day", "paid_type":"paid", "quota_per_year":6, "milestones":[…], "carry_max":5, "carry_expiry":"2027-03-31", "count_holiday":false, "half_day":true }
  }],
  "generated_at": "2026-08-28T10:00:00Z"
}
```
- `resolved_from` = `"company:<uuid>"` หรือ `"shared"` — **บอกปลายทางเสมอว่าใช้ค่าของใคร** (BR-13 · FN-23)
- คืน **เฉพาะเวอร์ชัน `status='active'` ณ `date`** — Draft/Scheduled/Inactive **ไม่ถูกคืน** (BR-19 · P-6)
- ค่าที่ item `status='inactive'` **ไม่ถูกคืนในรายการเลือกใหม่** แต่ `resolve` ด้วย `code` ตรง ๆ ยังคืนได้พร้อม `"item_status":"inactive"` เพื่อให้เอกสารเก่าแสดงผลได้ (§0.13.3 C-5)

**Errors:** **400 `ERR_RESOLVE_DATE_REQUIRED`** · 400 `ERR_INVALID_DATE` · 401 · 403 · 404 `ERR_CONFIG_NOT_FOUND` (เมื่อระบุ `code` แล้วไม่มีเวอร์ชัน active ณ วันนั้น)
**Preconditions:** — · **Side effects:** UPDATE `T_hr_config_usage.last_seen_at` (best-effort, async — ไม่บล็อก response)
**Caching:** `Cache-Control: private, max-age=<วินาทีถึงเที่ยงคืน>` — **ห้าม cache ข้ามวัน** · client ต้อง invalidate เมื่อได้ `hrconfig.effective` (EA-17 · §0.13.3 C-3)
**Calls (Logic):** **`ENG-HRCFG-01 hr-config-resolve`** → `03_LOGIC §3.2`

---

### F-HR-CONFIG-API-14: POST /api/v1/hr-config/period-rules/:id/periods/generate

**Body:** `{ "year": 2569, "overwrite_open_periods": false }`
**Response 201:** `{ "generated": 12, "periods": [{ "period_code":"2569-01", "date_from":"2568-12-26", "date_to":"2569-01-25", "pay_date":"2569-01-30", "period_status":"open" }, …] }`
**Errors:** 422 `BR_PERIOD_RULE_NOT_ACTIVE` (กติกายังไม่ active) · **422 `BR_PERIOD_CLOSED_CANNOT_REGENERATE`** (มีงวดที่ปิดแล้วในปีนั้น — ห้ามทับ) · 403 · 409
**Side effects:** INSERT `T_hr_pay_period` × N · write audit · **ไม่ยิง event** (การสร้างงวดยังไม่กระทบสิทธิ์)
**Calls (Logic):** `FN-13 generatePayPeriods` · **`ENG-HRCFG-02 hr-period-generator`** · `FN-17`

---

### F-HR-CONFIG-API-15: POST /api/v1/hr-config/periods/:id/close

**Body:** `{ "confirm": true }` · **Headers:** `Idempotency-Key` (required)
**Response 200:** `{ "period_code":"2569-07", "period_status":"closed", "closed_at":"…", "closed_by":"uuid" }`
**Errors:** 422 `BR_PERIOD_ALREADY_CLOSED` · 403 · 409
**Side effects:** UPDATE `period_status='closed'` + `closed_by` + `closed_at` (**ใน transaction พร้อม row lock — serialize กับ API-06 · PR-9**) · write audit · **emit `hrconfig.period_closed` (SecC)**
**Calls (Logic):** `FN-14 closePayPeriod` · `FN-17` · `FN-16`

---

### F-HR-CONFIG-API-16: POST /api/v1/hr-config/periods/:id/reopen

**Body:** `{ "reopen_reason": "พบรายการตกหล่นต้องแก้ยอดของงวดนี้" }` (≥10 ตัวอักษร)
**Errors:** 422 `BR_REOPEN_REASON_REQUIRED` · `BR_PERIOD_NOT_CLOSED` · 403
**Side effects:** UPDATE → `open` + เก็บ `reopen_reason` · write audit (**append-only — ไม่ลบร่องรอยการปิดครั้งก่อน**) · **ไม่ยิง event ใหม่** (ไม่มี event `period_reopened` ใน CSQ_BRIEF — **ห้ามประกาศ event นอก brief**) · บันทึกเป็น audit เท่านั้น
**Calls (Logic):** `FN-15 reopenPayPeriod` · `FN-17`

---

### F-HR-CONFIG-API-17: GET /api/v1/hr-config/periods

**Query:** `period_rule_id` (optional) · `year` (optional) · `status` (optional) · `date` (optional — หางวดที่ครอบวันนั้น)
**Response 200:** array ของงวด + สถานะ · **ใช้โดย Attendance/Payroll เพื่อรู้ว่างวดไหนปิดแล้ว**
**Side effects:** — · **Calls (Logic):** `FN-01` (query builder ร่วม)

---

## §2.3 Common Concerns

### Idempotency (PR-7 — mandatory)
ทุก mutation API (`POST`/`PUT`) รับ header **`Idempotency-Key` (required)**
- server cache ผลลัพธ์ 24 ชั่วโมง · key เดิม + body เดิม → คืน response เดิม (ไม่ INSERT ซ้ำ)
- key เดิม + body ต่าง → **409 `ERR_DUPLICATE_IDEMPOTENCY_KEY`**
- **สอดคล้องกับ `idempotency_key` ของ CSQ:** `F-HR-CONFIG:{version_id|period_code}:{event_id}` (CSQ_BRIEF §4)

### Optimistic Locking (PR-1 / PR-2)
`PUT` และ action endpoint ที่แก้สถานะ (`API-05`, `API-06`, `API-07`, `API-09`) ต้องส่ง **`If-Match: <updated_at>`**
- ตรงกัน → ทำต่อ · ไม่ตรง → **409 `ERR_STALE_DATA`**
- เพิ่มชั้นที่สอง: **unique constraint** `(config_item_id, effective_date)` ป้องกันสองคนสร้างเวอร์ชันวันเดียวกันพร้อมกัน (EA-01)

### Re-validation at commit (PR-2 / PR-9 · **สำคัญที่สุดของ feature นี้**)
`API-06` และ `API-10` ต้อง **ตรวจ BR-04 ซ้ำภายใน transaction เดียวกับการเขียน** พร้อม `SELECT … FOR SHARE` บนแถว `T_hr_pay_period` ที่เกี่ยวข้อง — ไม่ใช่ตรวจตอนเปิดฟอร์ม (EA-02 🔺 · `[AI-DEFAULT]` → **OQ-13**)

### Permission at mutation time (PR-3)
ตรวจ role ทุกครั้งที่ mutation ไม่ใช่ตอน GET → ถ้าถูกถอนสิทธิ์ระหว่างทาง = **403 `ERR_PERMISSION_REVOKED`** (EA-15 — บังคับที่ API ไม่ใช่ซ่อนปุ่ม)

### Multi-Tenant
ทุก endpoint ต้องมี `X-Tenant-Id` · auto-apply ที่ middleware · DB filter ด้วย PostgreSQL RLS

### Audit Log
ทุก mutation เขียน **Policy Center Audit Trail** (append-only) ผ่าน `FN-17`: actor · action · resource (`T_hr_config_version:<id>`) · timestamp · diff (before/after)
**กฎเหล็ก:** ถ้าเขียน audit ไม่สำเร็จ → **rollback ทั้ง transaction** (SLA-05 · R-02) — ห้ามให้ transition สำเร็จโดยไม่มี log

### Retry (PR-4)
client ควร retry 3 ครั้งแบบ exponential backoff บน 5xx/timeout **โดยใช้ `Idempotency-Key` เดิม**

### ไม่มีอยู่โดยเจตนา
- **ไม่มี DELETE endpoint** (BR-07)
- **ไม่มี bulk/import endpoint** (NS-08 · PR-5 ไม่ activate)
- **ไม่มี endpoint approve/reject** (NS-01 · ไม่มี approval)
- **ไม่มี endpoint คำนวณเงิน** (NS-03 · สูตรอยู่ Salary Structure/Payroll)

---

## §2.4 API → Logic Trace (Anchor for R8)

> **Authoritative source:** `03_LOGIC.md §3.3 Trace Table` — ที่นี่เป็น summary

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
| **API-10 POST /items/:id/reactivate** | FN-10, FN-05, FN-20, FN-17, FN-16 | — |
| API-11 GET /items/:id/usage | FN-12 | — |
| API-12 GET /items/:id/history | FN-11 | — |
| API-13 GET /resolve | — | **ENG-HRCFG-01** |
| **API-14 POST /periods/generate** | FN-13, FN-17 | **ENG-HRCFG-02** |
| **API-15 POST /periods/:id/close** | FN-14, FN-17, FN-16 | — |
| **API-16 POST /periods/:id/reopen** | FN-15, FN-17 | — |
| API-17 GET /periods | FN-01 | — |

> **R8 Check:** mutation API ทั้ง 10 ตัว (API-03…API-10, API-14…API-16) มี ≥1 Function/Engine ครบทุกแถว ✅
> `FN-18 computeShiftHours` ถูกเรียกจาก `FN-05` (nested) — trace เต็มดู `03_LOGIC §3.3`

---

## §2.X Cross-Module Contract ⭐ (จาก BRD §12.1 Downstream Impact Map)

> **นี่คือหน้าสัญญาที่อีก 8 feature ต้องอ่าน** — ดูภาพรวมเชิงธุรกิจที่ `00_OVERVIEW §0.13`

### A. Endpoint ที่ปลายทางเรียก (pull)

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก |
|---|---|---|---|---|
| **Leave** (W2) | Endpoint | `GET /hr-config/resolve?date=&company_id=&group=leave_type` | ทุกครั้งที่คำนวณสิทธิ์/สร้างใบลา | policy ประเภทลาเต็ม + `version_id` |
| **OT / Shift** (W2) | Endpoint | `…&group=ot_rate` และ `…&group=shift_pattern` | ตอนสร้าง/อนุมัติใบ OT | ตัวคูณ · ฐาน · เพดาน · `payroll_code` |
| **Shift & Roster** (W2) | Endpoint | `…&group=shift_pattern` และ `…&group=holiday_calendar` | ตอนจัดตารางกะ | กะมาตรฐาน + ปฏิทิน (+`location`) |
| **Attendance** (W1/C) | Endpoint | `…&group=holiday_calendar,period_rule` + `GET /hr-config/periods?date=` | ประมวลผลเวลารายวัน + ปิดยอดงวด | ปฏิทิน · วันตัดเวลา · **สถานะงวด** |
| **Payroll** (W4) | Endpoint | `…&group=period_rule,ot_rate` + `GET /hr-config/periods` | เปิด/ปิดรอบจ่าย | รอบจ่าย · งวดจริง · อัตรา · `payroll_code` |
| **Performance** (W5) | Endpoint | `…&group=appraisal_cycle` | ตอนเปิดรอบประเมิน | ช่วงประเมิน · ช่วงเปิดกรอก |
| **Welfare** (W4) | Endpoint | `…&group=leave_type` (อ่านนโยบายที่เกี่ยว) | ตอนตรวจสิทธิ์ | policy ที่เกี่ยว |
| **Salary Structure** (W1/B) | Endpoint | `…&group=period_rule,ot_rate` | ตอนจับคู่องค์ประกอบค่าจ้าง | รอบจ่าย · `payroll_code` |

### B. Event ที่ feature นี้เป็น producer (push · ผ่าน ENG-CSQ ท่อ **SecC** เท่านั้น)

| event | Trigger (API) | Payload หลัก | consumer ควรทำ |
|---|---|---|---|
| `hrconfig.published` | API-06 | `config_code` · `group` · `version_id` · `effective_date` · `company_scope` · `companies[]` · `changed_by` · `change_reason` · `value_diff[]` | เตรียมตัว — ยังไม่เปลี่ยนพฤติกรรม |
| `hrconfig.effective` | scheduler (FN-06 catch-up) หรือ API-06 เมื่อมีผลทันที | `config_code` · `group` · `version_id` · `effective_date` · `superseded_version_id` · `company_scope` · `companies[]` | **invalidate cache** + ใช้ค่าใหม่ |
| `hrconfig.cancelled` | API-07 | `config_code` · `version_id` · `effective_date` · `cancel_reason` · `changed_by` | ยกเลิกการเตรียมตัว |
| `hrconfig.deactivated` | API-09 | `config_code` · `group` · `deactivate_reason` · `where_used_count` · `changed_by` | ซ่อนจากตัวเลือกใหม่ · **ห้ามลบของเก่า** |
| `hrconfig.reactivated` | API-10 | `config_code` · `group` · `version_id` · `effective_date` · `changed_by` | นำกลับเข้าตัวเลือก |
| `hrconfig.period_closed` | API-15 | `period_code` · `period_from` · `period_to` · `pay_date` · `closed_by` · `closed_at` | ล็อกการแก้ข้อมูลของงวดนั้น |

- **6 event นี้ = ชุดเดียวกับ `5_DECLARATIONS/CSQ_BRIEF.md §2` เป๊ะ — ไม่มี event เกิน ไม่มี event ขาด**
- ท่อที่ยิง = **SecC เท่านั้น** · **ห้ามยิง OC / DC ระดับเอกสาร / SC (register reject 422)**
- `changed_by` / `closed_by` **ส่ง `employee_id` เท่านั้น ห้ามส่งชื่อดิบ** (BR-CSQ-03 · D7)
- **การถอน/ปิดใช้ไม่ลบผลเดิม** — เป็น event ใหม่ที่ชี้ `version_id` เดิม (BR-CSQ-04)

### C. Compensating / แก้กลางทาง

| เหตุการณ์ | Compensating action | ผลที่ปลายทาง |
|---|---|---|
| ยกเลิกเวอร์ชันที่รอมีผล (API-07) | `hrconfig.cancelled` + re-compute `effective_to` ของเวอร์ชันก่อนหน้า | ปลายทางยกเลิกการเตรียมตัว · **ค่าที่ Active เดิมยังใช้ต่อ** |
| ปิดใช้ค่า (API-09) | `hrconfig.deactivated` + `where_used_count` | ปลายทางซ่อนจากตัวเลือก · **ข้อมูลเก่ายังอ่านได้** |
| เปิดงวดกลับ (API-16) | **ไม่มี event** — audit เท่านั้น (ไม่มี `period_reopened` ใน CSQ_BRIEF) | ปลายทางต้อง poll `GET /hr-config/periods` ก่อนล็อกยอด — ระบุไว้เป็นข้อจำกัดที่รู้ตัว (**OQ-18**) |
| **ไม่มี retro** | — | แก้ผลย้อนหลังทำไม่ได้โดยออกแบบ (P-9 · OQ-STD-04) |

> ทุกแถวในตาราง A และ B มี cross-module test case คู่ใน `06_TESTS §6.9` (XT-01…XT-10) อย่างน้อย 1 case
