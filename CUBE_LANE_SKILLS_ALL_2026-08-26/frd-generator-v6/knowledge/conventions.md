# Conventions — frd-generator-v6

> **Purpose:** Cross-feature naming + format rules ที่ทุก FRD ใน 2BSimple ต้องใช้ตรงกัน
> **Used by:** Phase 1.1 (Sync Read) + Phase 3.5 Section I (Convention Compliance)
> **Scope:** ID, naming, format, structure

---

## 🆔 ID Conventions

### Feature ID
```
F-XX            (XX = 2-digit zero-padded)
F-01, F-02, F-04, F-15, F-99
```

### API ID (scope-local)
```
F-XX-API-NN     (NN = 2-digit zero-padded, sequence within feature)
F-04-API-01, F-04-API-02, ...
```

### Function ID (scope-local)
```
F-XX-FN-NN
F-04-FN-01 (camelCase function name)
```
**Format consistency:** ใช้ uppercase `F-XX-FN-NN` ใน 03_LOGIC §3.1, §3.3 trace, และทุก reference

### Engine ID
**Scope-local (in FRD draft):**
```
F-XX-ENG-NN     (for draft engines candidate)
F-04-ENG-01
```

**Global (after CUBIC registration):**
```
ENG-NNN         (NNN = 3-digit, assigned by CUBIC Registry)
ENG-005, ENG-024
```

> **Note:** ใน FRD ใช้ scope-local ก่อน — Dev/Architect แปลงเป็น global ตอน register

### Table ID (DB)
```
T_snake_case_table_name
T_payroll, T_payroll_period, T_employee_salary_history
```

### Field key (DB column + API field)
```
snake_case
employee_id, base_salary, created_at
```

### Function code (in 03_LOGIC §3.1)
```
camelCase verb + noun
createPayrollRecord, validateThaiID, calculateOvertimeHours
```

### Engine code (in 03_LOGIC §3.2)
```
kebab-case noun phrase
payroll-calculation-engine, thai-id-validator, omise-payment-gateway
```

### Error code
```
UPPER_SNAKE_CASE
ERR_VALIDATION_FAILED, ERR_PAYROLL_PERIOD_LOCKED, ENG_ERR_INVALID_INPUT
```
**Prefix conventions:**
- `ERR_*` — general API error
- `ENG_ERR_*` — engine-specific error
- `BR_*` — business rule violation (in 05_RULES)

### Status value
```
snake_case past tense (state values)
draft, submitted, approved, rejected, cancelled, refunded
```

### Event name
```
snake_case past tense + _event
payroll_submitted_event, customer_created_event
```

### Locked Decision ID
```
LD-NN
LD-01, LD-02 (sequential within FRD)
```

### Business Rule ID
```
BR-FEATURE-NN
BR-PAY-01, BR-PAY-02, BR-CRM-05
```

---

## 📂 File Naming

### FRD Pack folder
```
FRD_F-XX_Pack/
```

### FRD files
```
00_OVERVIEW.md
01_UI.md
02_API.md
03_LOGIC.md
04_DB.md
05_RULES.md
06_TESTS.md
07_LOCKED_DECISIONS.md
INDEX.md
```
> ใช้ underscore เสมอ — ห้าม dash หรือ space

---

## 🌐 HTTP Conventions

### Path format
```
/api/v1/<resource>           # collection: GET, POST
/api/v1/<resource>/:id       # item: GET, PUT, PATCH, DELETE
/api/v1/<resource>/:id/<action>  # custom action: POST /payrolls/:id/submit
```
- ใช้ plural noun: `/payrolls` ไม่ใช่ `/payroll`
- ใช้ kebab-case ใน path ถ้าหลายคำ: `/payment-vouchers`
- Version prefix mandatory: `/api/v1/...`

### HTTP Method usage
| Method | Use case |
|---|---|
| GET | Read (idempotent) |
| POST | Create / custom action / non-idempotent |
| PUT | Full replace |
| PATCH | Partial update |
| DELETE | Soft/hard delete |

### Status codes
| Code | Meaning |
|---|---|
| 200 | OK (GET/PUT/PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Validation failed |
| 401 | Not authenticated |
| 403 | Forbidden (auth ok, role wrong) |
| 404 | Not found |
| 409 | Conflict (idempotency, concurrency) |
| 422 | Business rule violated |
| 500 | Internal error |

### Headers
| Header | Use |
|---|---|
| `Authorization: Bearer <token>` | Auth |
| `X-Tenant-Id: <uuid>` | Multi-tenant |
| `Idempotency-Key: <uuid>` | Mutation safety (PR-7) |
| `If-Match: <etag>` | Optimistic locking (PR-2) |

---

## 📝 Markdown Conventions

### Heading structure
```
# 03_LOGIC — F-XX [Feature Name]    ← H1: file title
## §3.1 Functions                    ← H2: major section
### F-XX-FN-01: functionName         ← H3: individual item
#### Sub-detail (if needed)          ← H4
```

### Code blocks
- ใช้ ` ```language ` เสมอ
- Language tags: `json`, `sql`, `typescript`, `javascript`, `bash`

### Tables
- Header bold ผ่าน column header (Markdown auto)
- Align `|---|---|---|`
- Empty cells = `—` ไม่ใช่ blank

### Cross-reference
- Same file: "ดู §3.3"
- Other file in pack: "ดู `05_RULES.md` §2"
- External: "ดู `references/cubic-schema-templates.md`"

---

## 🎨 Layout / UI Conventions (Reference)

> **Source of Truth (v6):** FRD 01_UI §1.0 Layout Decision Log (Design Authority = frd-generator-v6 Phase 1.5) + pattern ความหมายจาก html-generator-v9 (Sync Read)
> ใน FRD 01_UI.md **copy ID ตรง ๆ จาก BRD** — ห้ามตัดสินใจ Layout ใหม่

### Layout Patterns (from html-generator-v9 — A-N, อ่านสดทุก session)
- Pattern A: List + Detail Drawer
- Pattern B: Master-Detail Page
- Pattern C: Form Wizard
- Pattern D: Dashboard Grid
- Pattern E: Calendar/Schedule
- Pattern F: Kanban Board
- Pattern G: Timeline/Activity Feed
- Pattern H: Settings/Tab Page
- Pattern I: Report/Print Layout

---

## 🔒 Security Conventions (Reference)

> **Source of Truth:** Security_Spec_Bible §0.1 Domain Triggers
> ใน 05_RULES.md ระบุ Domain (D1-D28) ที่ apply

### Role naming
```
snake_case
admin, manager, cashier, hr_staff, finance_approver
```

### Permission action
```
snake_case verbs
view, create, edit, delete, approve, export
```

---

## ✅ Compliance Self-Check

ก่อน deliver — verify:

- [ ] ทุก ID format ตรงตาม convention
- [ ] ไฟล์ใน Pack ตั้งชื่อตาม pattern
- [ ] API path = plural + kebab + /api/v1
- [ ] Field key = snake_case ทั้งหมด
- [ ] Function code = camelCase
- [ ] Engine code = kebab-case
- [ ] Error code = UPPER_SNAKE
- [ ] Status = snake_case past tense
- [ ] LD-NN sequential ภายใน FRD

ขาดข้อใด → Phase 3.5 Section I จะ flag
