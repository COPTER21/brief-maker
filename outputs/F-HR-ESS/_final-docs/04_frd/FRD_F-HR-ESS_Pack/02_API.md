# 02_API — F-HR-ESS · ESS Portal (พนักงานทำเอง)

> **Audience:** BE dev (HTTP layer)
> **Purpose:** API contracts (HTTP layer only) + Cross-Module Contract (navigate / consume)
> **🚨 หลักการ (LK-1/LK-2/LK-6):** ESS API = **GET only (aggregate read)**. **ไม่มี POST/PUT/PATCH/DELETE ธุรกิจ** — ไม่มี create/update/approve/mutation ใดๆ. ยกเว้นเดียว = append access-audit (server-side, ไม่ใช่ธุรกรรมผู้ใช้). ทุก read = **self-scope enforced ที่ backend** (id ผ่าน param ≠ self → 403). "ยื่นคำขอ" = **navigate ฝั่ง client** ไม่ใช่ API call.

---

## §2.1 API Inventory

| ID | Method | Path | Purpose | FN | Mutation? |
|---|---|---|---|---|:--:|
| API-01 | GET | `/ess/dashboard` | สรุป read หลาย surface (5 การ์ด) | FN-01 | — |
| API-02 | GET | `/ess/payslips` · `/ess/payslips/:id` · `/ess/payslips/ytd` | สลิป + ประวัติ + YTD (self · all-or-nothing) | FN-02 | — |
| API-03 | GET | `/ess/surface/:type` · `/ess/surface/:type/:id` | อ่าน surface: leave/ot/shift/expense/cert/welfare/training | FN-03..07 | — |
| API-04 | — | *(deep-link = client navigate)* | ไม่มี API — ดู §2.4 | FN-03/05/06/08 | — |
| API-05 | GET | `/ess/notifications` | consume feed (self) + search/filter | FN-09/90 | — |
| API-06 | GET | `/ess/profile` | โปรไฟล์ (self · RESTRICTED masked) | FN-08 | — |
| API-07 | GET | `/ess/access-audit` | ประวัติการเข้าถึงของฉัน (append-only read) | FN-93 | — |
| (internal) | *(server hook)* | append `T_ess_access_audit` + emit CSQ self-access | ทุก read เขียน audit + ยิง SecC event | FN-93/10 | *(audit only)* |

> **ไม่มี mutation API ธุรกิจ** → R8 (mutation→function trace) satisfied vacuously (ดู 03_LOGIC §3.3). audit append = side-effect ของ read (03_LOGIC FN-07), ไม่ใช่ endpoint ที่ client เรียกตรง.

---

## §2.2 Contract Blocks

### API-01 · GET `/ess/dashboard` (FN-01)
- **Auth:** JWT · self-scope (backend ดึง employee_id จาก token — **ไม่รับ param employee_id**)
- **Response 200:**
```json
{
  "employee": { "id":"EMP-00123", "name":"สมชาย ใจดี", "position":"...", "dept":"...", "branch":"..." },
  "cards": {
    "latest_payslip": { "id":"PS-2568-07", "period":"กรกฎาคม 2568", "net": 38250.00 },
    "leave_left_days": 38,
    "ot_hours_month": 12, "ot_month":"กรกฎาคม 2568",
    "expense_pending_count": 1,
    "notification_unread": 2
  }
}
```
- **Note:** เป็นการ aggregate read จากหลาย surface (03_LOGIC FN-01). แต่ละ surface อาจ degrade แยก (OQ-ESS-04 `[AI-DEFAULT]` — per-card try/catch, ไม่ล้มทั้งหน้า). ค่า money = Restricted (all-or-nothing self).

### API-02 · GET `/ess/payslips` · `/:id` · `/ytd` (FN-02 · LK-3)
- **Auth:** self-scope only. **all-or-nothing** — คืนสลิปเต็มใบของ self หรือ 403; ไม่มี partial field projection.
- **`GET /ess/payslips`** → list (period/pay_date/net/status). **`/:id`** → รายละเอียด (gross/deduct/net/status). **`/ytd`** → {gross,tax,sso,net}.
- **Restricted:** money fields = Restricted; enforce mask/self ที่ backend. PDF = **จากต้นทาง Payroll** (ESS ไม่ผลิต · อาจส่ง `pdf_url` ที่ owner ออก).
- **Errors:** 403 (ไม่ใช่ self) · 404 (ไม่มีสลิป) · 502/degraded (Payroll down → OQ-ESS-04).

### API-03 · GET `/ess/surface/:type[/:id]` (FN-03..07)
- **:type** ∈ `leave` · `ot` · `shift` · `expense` · `cert` · `welfare` · `training`. self-scope.
- **List** → rows ตาม surface (จาก HTML mock schema: leave{type,range,days,status} · expense{title,date,amount,status} · cert{title,issued,by,status} · training{course,date,hours,cert,status} · shift{date,shift} · ot{hours,approved,pending}+scans). **`/:id`** → detail สำหรับ drawer.
- **[ASSUMED contract]:** schema field-level ของ owner ยัง soft ref (LK-5) → chip [ASSUMED] บนจอ (FN-11). dev อ่านจาก owner read-model, ไม่ hardcode.
- **Errors:** 403 (คนอื่น) · owner ba-done/timeout → per-surface degrade (FN-11 / OQ-ESS-04).

### API-05 · GET `/ess/notifications` (FN-09/90 · consume)
- **Query:** `?q=<คำค้น>&unread=<bool>`. self feed.
- **Response:** `[{ id, icon, title, desc, time, unread }]` (mirror ENG-NOTIFY feed).
- **Source:** **consume จาก ENG-NOTIFY** (ntf ฝั่งอ่าน). **ESS ไม่ยิง/สร้าง notification event** (LK-6). search/filter = client-side บน feed ที่ดึงมา (03_LOGIC FN-06) — empty → UI empty state.
- **mark-as-read:** ถ้ามี = ทำที่ ENG-NOTIFY (owner), ESS แค่ display unread state (`[AI-DEFAULT]` · OQ ปลายทาง NTF).

### API-06 · GET `/ess/profile` (FN-08 · Restricted)
- **Auth:** self only. **Response** masked by default: `national_id`/`bank_account_no` = masked. reveal = client toggle (self) → **log `reveal_restricted`** (audit hook) — backend ยัง enforce ว่าเป็น self ก่อนคืน full value.
- **แก้ไข:** **ไม่มี PUT** — "ขอแก้ข้อมูล" = navigate `#/profile/edit-request` (§2.4 · LK-1/LK-2).

### API-07 · GET `/ess/access-audit` (FN-93)
- self-scope · append-only read. **Response:** `[{ time, what }]` (จาก `T_ess_access_audit`). แสดงใน profile drawer "ประวัติการเข้าถึงข้อมูลของฉัน".

---

## §2.3 Cross-Module Contract — Consume (Value Stream R12 · in-flow)

| Source | Contract | ESS ทำอะไร | หมายเหตุ |
|---|---|---|---|
| **ENG-NOTIFY** | GET feed (self) | อ่านอย่างเดียว (API-05) | **ESS ไม่ประกาศ event** · consume only (LK-6) |
| **ENG-CSQ (SecC)** | emit self-access event ทุก read | ยิง event เข้า SecC pipe | event id = **[ASSUMED · OQ-ESS-01]** — ห้าม hardcode/invent (ดู 05_RULES §5.7) |
| Payroll / Leave / OT / Expense / Cert / Welfare / Training / Employee | GET read-model (self) | อ่าน surface (API-02/03/06) | contract field-level = [ASSUMED soft ref · LK-5] |

> **ESS ไม่มี downstream data write** — ไม่ commit budget/บัญชี/สต๊อก/สถานะ owner. ผลลัพธ์เดียวที่ไหลออก = **navigation** (§2.4) + **audit/CSQ self-access event** (in-flow security).

---

## §2.4 Cross-Module — Deep-link (navigate-out · **NO API** · OQ-ESS-02)

> "ยื่นคำขอ" ทั้ง 5 = **client-side navigation** ไปหน้า owner feature (form/submit อยู่ที่นั่น). **ESS ไม่มี endpoint รับคำขอ** (LK-1/LK-2). route ปลายทาง = **[ASSUMED contract]** อ่านจาก config, ยืนยันกับ owner ก่อน dev.

| Action | target route [ASSUMED] | owner รับผิดชอบ form/submit/approval |
|---|---|---|
| ยื่นลา | `#/leave/new` | การลา |
| ขอ OT | `#/ot/new` | OT |
| ยื่นเบิก | `#/expense/new` | Expense (F101) |
| ขอแก้ข้อมูล | `#/profile/edit-request` | Employee Master |
| ขอหนังสือ | `#/cert/new` | หนังสือรับรอง |

**Fallback (OQ-ESS-03 `[AI-DEFAULT]`):** route ยังไม่พร้อม → แสดง notice/toast graceful, คงหน้า ESS เดิม (ไม่ค้าง/ไม่ error หน้าเปล่า).

---

## §2.5 Common
- **Auth:** ทุก endpoint = JWT · **self-scope จาก token เท่านั้น** — endpoint **ไม่รับ `employee_id` param**; ถ้ามีการส่ง id คนอื่นผ่าน path/param → **403** (05_RULES ERR-403 · FN-10 · OQ-ESS-05).
- **Idempotency/lock:** N/A (read-only · ไม่มี mutation ธุรกิจ).
- **Errors catalog:** ดู 05_RULES §5.6.
