# 03_LOGIC — F-HR-ESS · ESS Portal (พนักงานทำเอง)

> **Audience:** BE dev (business logic layer)
> **Scope:** non-HTTP logic — **read / aggregate / guard / mask** functions เท่านั้น. **ไม่มี mutation function · ไม่มี Engine · ไม่มี state transition** (ESS display-only · portal aggregate).
> **R9 note:** feature นี้ **ไม่ pure-display 100%** — มี read-side logic จริง (aggregate, self-scope guard, RESTRICTED masking, consume+filter feed, deep-link resolve, audit append). จึงมี §3.1 Functions ครบ. **§3.2 Engines = ว่าง** (ใช้ ENG-CSQ/ENG-NOTIFY ที่มีอยู่แล้ว ไม่สร้างใหม่).

---

## §3.1 Functions (Scope-Local)

### F-ESS-FN-01: buildDashboardSummary (FN-01)
- **Purpose:** aggregate read จากหลาย surface → 5 การ์ดสรุป (สลิปล่าสุด · โควตาลารวม · OT เดือน · ใบเบิกค้าง · แจ้งเตือน unread)
- **Input:** `{ employeeId (from token) }`
- **Output:** `DashboardSummary` (ดู 02_API-01)
- **Invoked by:** API-01 GET /ess/dashboard
- **Calls:** F-ESS-FN-02 (payslip latest), F-ESS-FN-03 (surface reads), F-ESS-FN-06 (notify count), F-ESS-FN-04 (self guard ทุก read)
- **Side effects:** F-ESS-FN-07 append audit (per surface touched) · per-surface try/catch (OQ-ESS-04 degrade)
- **Iron rule check:** ✅ no HTTP terms · read-only

### F-ESS-FN-02: readPayslipSelf (FN-02 · LK-3)
- **Purpose:** อ่านสลิป/ประวัติ/YTD ของ self แบบ **all-or-nothing** (เต็มใบ หรือ 403 — ไม่มี partial)
- **Input:** `{ employeeId, payslipId? }`
- **Output:** `Payslip | PayslipList | YTD | Forbidden`
- **Invoked by:** API-02
- **Calls:** F-ESS-FN-04 (self guard), Payroll PS-1 read-model (soft ref), F-ESS-FN-07 (audit)
- **Side effects:** append audit(surface='payslip') · emit CSQ self-access (OQ-ESS-01)
- **Iron rule check:** ✅ read-only · money = Restricted (no mask-partial → all-or-nothing)

### F-ESS-FN-03: readSurfaceSelf (FN-03/04/05/06/07)
- **Purpose:** อ่าน surface ทั่วไป (leave/ot/shift/expense/cert/welfare/training) ของ self · คืน list/detail สำหรับ tab/drawer
- **Input:** `{ employeeId, type, recordId? }`
- **Output:** `SurfaceRows | SurfaceDetail | Forbidden | Degraded`
- **Invoked by:** API-03
- **Calls:** F-ESS-FN-04 (self guard), owner read-model (soft ref · [ASSUMED] LK-5), F-ESS-FN-07 (audit)
- **Side effects:** owner ba-done/timeout → per-surface `Degraded` marker (FN-11 chip / OQ-ESS-04)
- **Iron rule check:** ✅ read-only · **ไม่มีทางเขียนกลับ owner**

### F-ESS-FN-04: enforceSelfScope (FN-10/94 · LK-4 · guard)
- **Purpose:** ตรวจว่า caller = เจ้าของข้อมูล (self). ถ้า target employee_id ≠ token employee_id → **403** (ไม่ leak field ใด)
- **Input:** `{ tokenEmployeeId, targetEmployeeId | requestScope }`
- **Output:** `void | Forbidden(403)`
- **Invoked by:** ทุก read function (FN-01/02/03/05/06/07) — **called ก่อน read ทุกครั้ง**
- **Side effects:** ปฏิเสธ → emit CSQ `access_denied` (OQ-ESS-01) + append audit(action='denied')
- **Iron rule check:** ✅ pure guard · **enforce ที่ backend ไม่ใช่ UI** (OQ-ESS-05)

### F-ESS-FN-05: maskRestricted (FN-08/94 · VR-2)
- **Purpose:** ปิดบัง field RESTRICTED (national_id, bank_account_no) ก่อนส่งถึง client · reveal ได้เฉพาะ self (toggle) → log
- **Input:** `{ profile, reveal: bool, isSelf: bool }`
- **Output:** `MaskedProfile` (masked หรือ full เมื่อ reveal && isSelf)
- **Invoked by:** API-06 (profile) · dashboard/qcard ที่แตะ RESTRICTED
- **Calls:** F-ESS-FN-07 (audit action='reveal_restricted' เมื่อ reveal)
- **Iron rule check:** ✅ transform · self-guarded

### F-ESS-FN-06: consumeNotifyFeed (FN-09/90 · LK-6)
- **Purpose:** ดึง feed แจ้งเตือน self จาก ENG-NOTIFY · filter (q + unread) · empty detection. **ESS ไม่ยิง/สร้าง event**
- **Input:** `{ employeeId, q?, unread? }`
- **Output:** `NotificationRow[] | Empty`
- **Invoked by:** API-05
- **Calls:** ENG-NOTIFY feed read (consume), F-ESS-FN-04
- **Side effects:** ไม่มี write กลับ NOTIFY (mark-read = owner NOTIFY · [AI-DEFAULT])
- **Iron rule check:** ✅ read + filter · consume-only

### F-ESS-FN-07: appendAccessAudit (FN-93 · LK-6)
- **Purpose:** เขียน `T_ess_access_audit` (append-only) ทุกการเปิดข้อมูล/reveal · เป็นฐานของ self-access CSQ event
- **Input:** `{ employeeId, surface, recordRef?, action }`
- **Output:** `void`
- **Invoked by:** side-effect ของ FN-01/02/03/05 + reveal (FN-05)
- **Side effects:** INSERT audit (no update/delete) · emit CSQ self-access event (id = **[ASSUMED · OQ-ESS-01]**)
- **Iron rule check:** ✅ append-only · **ไม่ใช่ mutation ธุรกิจ** (security/audit side-effect ของ read)

### F-ESS-FN-08: resolveDeepLink (FN-03/05/06/08 · LK-2 · OQ-ESS-02)
- **Purpose:** map action key (leave/ot/expense/profile/cert) → route ปลายทาง owner feature (จาก **config ไม่ hardcode**) + fallback graceful ถ้ายังไม่พร้อม
- **Input:** `{ actionKey }`
- **Output:** `{ route, label } | Fallback` (route = **[ASSUMED contract]** · OQ-ESS-02)
- **Invoked by:** client deep-link handler (`deepLink()` / action-picker) — **ไม่ mutate, ไม่เรียก owner API**; แค่ navigate
- **Side effects:** ไม่มี data write. route ยังไม่พร้อม → Fallback message (OQ-ESS-03 `[AI-DEFAULT]`)
- **Iron rule check:** ✅ pure lookup · navigate-out (ไม่ใช่ submit)

---

## §3.2 Engines (Reusable / CUBIC-Registered)

> **ไม่มี engine ใน feature นี้.** ESS ใช้ engine กลางที่มีอยู่แล้วแบบ **consumer**:
> - **ENG-CSQ (SecC)** — self-access enforcement/event (ไม่สร้างใหม่ · CSQ_BRIEF_F059 · OQ-ESS-01)
> - **ENG-NOTIFY** — consume feed (ไม่สร้างใหม่ · ไม่ประกาศ event)
>
> ESS ไม่มี pure-calculation/algorithm ที่ต้อง register (ไม่มีการคำนวณเงิน/สิทธิ์ — read-only).

---

## §3.3 API ↔ Logic Trace Table (Phase 3.5 Anchor · R8)

| API | Calls Functions | Calls Engines | Mutation? |
|---|---|---|---|
| API-01 GET /ess/dashboard | FN-01 → FN-02/FN-03/FN-06/FN-04/FN-07 | (CSQ emit · NOTIFY consume) | — |
| API-02 GET /ess/payslips[/ytd] | FN-02, FN-04, FN-07 | CSQ | — |
| API-03 GET /ess/surface/:type | FN-03, FN-04, FN-07 | CSQ | — |
| API-05 GET /ess/notifications | FN-06, FN-04 | NOTIFY (consume) | — |
| API-06 GET /ess/profile | FN-05, FN-04, FN-07 | CSQ | — |
| API-07 GET /ess/access-audit | FN-04 (read own audit) | — | — |
| *(client deep-link)* | FN-08 | — | — *(navigate)* |

> **R8 check:** ไม่มี mutation API ธุรกิจในทั้ง feature → เงื่อนไข "ทุก mutation API ต้อง trace ≥1 function" **satisfied vacuously**. append-audit (FN-07) = side-effect ของ read (security/audit), ไม่ใช่ endpoint ที่ client mutate. **ไม่มี orphan function** — FN-01..08 ถูก trace ครบ. FN-08 = client-side (navigate), trace ที่ deep-link handler.
