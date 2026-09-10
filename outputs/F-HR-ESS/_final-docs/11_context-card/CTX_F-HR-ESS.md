# CTX — F-HR-ESS: ESS Portal (พนักงานทำเอง)

> **derived from:** FRD_F-HR-ESS v1.0 (2026-09-10) · **generated:** 2026-09-11
> **module:** HR (CUBE 4.0) · **feature code:** F059 · **variant:** STANDARD · **status:** active (FRD DRAFT · พร้อม review)
> ⚠ Derived artifact — source of truth คือ FRD Pack · ถ้า FRD revise ต้อง regen CTX

---

## 1. Summary

**ESS Portal = display-only aggregator** (archetype `portal(aggregate)`) — รวม "มุมมองของฉัน" จากทุกโดเมน HR มาไว้จุดเดียวแบบ **อ่านอย่างเดียว**. พนักงาน (self) เปิดดูสลิป · วันลา/โควตา · OT/เวลา/ตารางกะ · ใบเบิก · หนังสือรับรอง · สวัสดิการ/อบรม · โปรไฟล์ · แจ้งเตือน — ทุก surface อ่านจาก owner feature ต้นทาง (self-scope). **ไม่มี CRUD · ไม่มี entity/lifecycle ของตัวเอง · ไม่มีเอกสาร/เลขรัน/อนุมัติ**. "ยื่นคำขอ" ทั้งหมด = **deep-link (navigate-out)** ไปหน้า owner feature (form/submit อยู่ที่นั่น). enforce **self-access ที่ backend** (เข้าถึงคนอื่น = 403 · SecC) + mask RESTRICTED (national_id/bank/สลิป) + consume feed จาก ENG-NOTIFY (ESS ไม่ยิง event เอง). ตารางเดียวที่ ESS เป็นเจ้าของ = access-audit (append-only). Feature นี้นิยามด้วย "สิ่งที่ห้ามทำ" — ไม่มี layer ที่ผลักขึ้น engine/mutation.

## 2. Data Contract

> Source: FRD 04_DB. **ESS ไม่เป็นเจ้าของข้อมูลธุรกิจ** — อ่าน read-model/view ของ owner feature (self-scope, no FK write-back) และมีตารางเดียวของตัวเอง = access-audit. ไม่มี running number · ไม่มี snapshot ธุรกิจ · ไม่มี state/lifecycle table.

### Read Surfaces (upstream · self-scope ทั้งหมด · read-only · ESS ไม่เก็บสำเนา)
| # | Surface | Owner feature (source of record) | ESS อ่านอะไร | หมายเหตุ |
|---|---|---|---|---|
| SR-1 | Payslip PS-1 | Payroll (F-HR-PAYROLL §0.13.2) | สลิป + ประวัติ + YTD | **all-or-nothing · RESTRICTED** (LK-3) |
| SR-2 | Leave / quota | การลา | โควตา + ประวัติลา | [ASSUMED] soft ref |
| SR-3 | OT / Attendance | OT/Attendance | OT เดือน + การสแกน | [ASSUMED] soft ref |
| SR-4 | Shift schedule | ระบบกะ/บันทึกเวลา (Time · W2) | ตารางกะสัปดาห์นี้ | [ASSUMED] · ESS ไม่แก้กะ |
| SR-5 | Expense | เบิกค่าใช้จ่าย (F101) | ใบเบิก + สถานะ | [ASSUMED] soft ref |
| SR-6 | Cert / เอกสาร | หนังสือรับรอง | เอกสารที่ออก | [ASSUMED] · PDF จากต้นทาง |
| SR-7 | Welfare / Training | สวัสดิการ (F102) / อบรม | คงเหลือ + ประวัติ + ใบรับรอง | [ASSUMED] soft ref |
| SR-8 | Employee profile | Employee Master | ข้อมูลส่วนตัว | **RESTRICTED masking** · แก้ = deep-link |
| SR-9 | Notification feed | ENG-NOTIFY (F-NOTIFY) | my notifications | **consume** · ESS ไม่เขียน/ยิง event |

> Contract field-level ของ SR-1..9 = **[ASSUMED · resolve เมื่อ owner ba-done]** (LK-5). ไม่มี FK เขียนกลับไปตาราง owner.

### Own Entity (ตารางเดียวของ ESS)
| Entity | PK | Key Fields | หมายเหตุ |
|---|---|---|---|
| `T_ess_access_audit` | id (uuid) | tenant_id (RLS), employee_id (=ผู้เข้าถึง=self เสมอ · Confidential/PII), surface, record_ref (soft ref · ไม่ FK), action, csq_event, accessed_at, ip, user_agent | **append-only** (revoke UPDATE/DELETE ที่ role) · RLS `tenant_id` + `employee_id = current_user` · index (employee_id, accessed_at DESC). เก็บแค่ "ใครเปิดอะไรเมื่อไหร่" ไม่เก็บเนื้อข้อมูล. `csq_event` = **[ASSUMED · OQ-ESS-01]** |

### Enums (ครบทุกค่า — ห้าม compress)
| Field | Values | Owner |
|---|---|---|
| `audit.action` | `view` (default) · `reveal_restricted` (กดแสดงข้อมูลปิดบัง) | feature นี้ |
| `audit.surface` | `payslip` · `leave` · `ot` · `shift` · `expense` · `cert` · `welfare` · `training` · `profile` · `notify` | feature นี้ |
| surface `:type` (API-03 param) | `leave` · `ot` · `shift` · `expense` · `cert` · `welfare` · `training` | owner features |
| Data Classification (ระดับที่ ESS แตะ) | `Restricted` · `Confidential` · `Internal` · `Public` (default = Internal · ไม่มี field Public) | Policy Center (owner register) |

> **ไม่มี state machine / document lifecycle ของตัวเอง** — สถานะที่แสดง (สลิปออกแล้ว · ใบเบิกรออนุมัติ ฯลฯ) = **อ่านมาจาก owner feature** แสดงเป็น pill/badge อ่านอย่างเดียว · ไม่มี transition ที่ ESS เป็นเจ้าของ.

### Restricted / masking (read-through · enforce จริงที่ owner + backend ESS)
| Field (read) | Surface | Classification | Masking (ESS) |
|---|---|---|---|
| `payslip.net`/`gross`/`deduct`/`ytd.*` | payslip | **Restricted** | all-or-nothing (เห็นทั้งใบ/ไม่เห็น) · self only |
| `national_id` | profile | **Restricted** (PII) | mask default · reveal ปุ่ม (self) → log `reveal_restricted` |
| `bank_account_no` | profile | **Restricted** (PII) | mask default · reveal (self) |
| `email`/`phone`/`dept`/`branch`/`start_date` | profile | Confidential (PII) | self only |
| `leave.*` / `expense.*` / `cert.*` / `training.*` | หลาย surface | Confidential | self only |
| `notification.*` | notify | Internal | self feed only |
| `shift.*` | shift | Internal | self only |

> Restricted = read-through จาก owner — **register Restricted Resources ทำที่ owner feature**; ESS enforce masking/self-scope ซ้ำที่ backend (OQ-ESS-05 · ห้าม enforce แค่ UI).

### Relationships
- พนักงาน (self) —(1:N read)— [Payslip · Leave · OT · Attendance · Shift · Expense · Cert · Welfare · Training · Profile · Notification] (owner-owned)
- ESS Portal —(aggregate/read-only · **no FK write-back**)— ทุก surface ข้างบน
- ESS Portal —(1:N append)— `T_ess_access_audit` (own · append-only)
- "ยื่นคำขอ" —(deep-link/navigate · **no data write**)— owner feature (leave/ot/expense/profile/cert)

## 3. API Surface

> Source: FRD 02_API. **GET only (aggregate read)** — self-scope enforced ที่ backend (employee_id จาก JWT token · endpoint **ไม่รับ param employee_id**; ส่ง id คนอื่น → 403). **ไม่มี POST/PUT/PATCH/DELETE ธุรกิจ** — ไม่มี create/update/approve/mutation. "ยื่นคำขอ" = client navigate (§Deep-link · ไม่ใช่ API call).

| Method | Endpoint | ทำอะไร | FN |
|---|---|---|---|
| GET | `/ess/dashboard` | สรุป read หลาย surface (5 การ์ด) · per-card degrade แยก | FN-01 |
| GET | `/ess/payslips` · `/:id` · `/ytd` | สลิป + ประวัติ + YTD (self · all-or-nothing · ไม่มี partial projection) | FN-02 |
| GET | `/ess/surface/:type` · `/:type/:id` | อ่าน surface: leave/ot/shift/expense/cert/welfare/training | FN-03..07 |
| GET | `/ess/notifications` | consume feed (self) `?q=&unread=` · search/filter client-side | FN-09/90 |
| GET | `/ess/profile` | โปรไฟล์ (self · RESTRICTED masked default) | FN-08 |
| GET | `/ess/access-audit` | ประวัติการเข้าถึงของฉัน (append-only read · จาก T_ess_access_audit) | FN-93 |
| *(server hook)* | append `T_ess_access_audit` + emit CSQ self-access | side-effect ของทุก read (ไม่ใช่ endpoint ที่ client เรียกตรง) | FN-93/10 |

- **PDF สลิป** = จากต้นทาง Payroll (ESS ไม่ผลิต · อาจส่ง `pdf_url` ที่ owner ออก).
- **mark-as-read** notification = ทำที่ ENG-NOTIFY (owner) · ESS แค่ display unread state (`[AI-DEFAULT]`).
- **Idempotency/lock:** N/A (read-only · ไม่มี mutation).

### Error contract (HTTP · consumers/gateway ต้อง honor)
| Code | HTTP | เมื่อไหร่ |
|---|---|---|
| ERR-403-SELF | 403 | เข้าถึงข้อมูลพนักงานคนอื่น (id ≠ self ผ่าน param/URL) → ปิดบัง · ไม่ leak field (FN-10 · VR-3) |
| ERR-404 | 404 | record ไม่มี (สลิป/surface) |
| ERR-DEGRADED | 502 / soft | surface/owner down/timeout → per-card degrade · **ไม่ throw ทั้งหน้า** (OQ-ESS-04 · `[AI-DEFAULT]`) |
| ERR-LINK-NA | soft | deep-link route ยังไม่พร้อม → graceful notice · คงหน้าเดิม · **ไม่โชว์ route/contract ดิบ** (OQ-ESS-03 · `[AI-DEFAULT]`) |

### Deep-link (navigate-out · **NO API** · client-side · OQ-ESS-02)
> "ยื่นคำขอ" ทั้ง 5 = client navigate ไปหน้า owner feature. **ESS ไม่มี endpoint รับคำขอ** (LK-1/LK-2). route = **[ASSUMED contract]** อ่านจาก config · ยืนยันกับ owner ก่อน dev · เดาผิด = navigate ค้าง.

| Action | target route **[ASSUMED · OQ-ESS-02]** | owner (form/submit/approval) |
|---|---|---|
| ยื่นลา | `#/leave/new` | การลา |
| ขอ OT | `#/ot/new` | OT |
| ยื่นเบิก | `#/expense/new` | Expense (F101) |
| ขอแก้ข้อมูล | `#/profile/edit-request` | Employee Master |
| ขอหนังสือ | `#/cert/new` | หนังสือรับรอง |

### Events emitted
| Event | สถานะ |
|---|---|
| — | **NONE (0 event) — ESS = consumer-only.** ทุก notifiable event (สลิปออก · ผลอนุมัติลา/OT/เบิก · หนังสือพร้อม) emit ที่ **owner feature ต้นทาง** แล้ว. ESS ประกาศ/emit ซ้ำ = event ซ้ำซ้อน + ผิด ownership (BR-01). ไม่มี `doa_*` (ไม่มี DOA ใน ESS). |

> **ผลลัพธ์เดียวที่ไหลออกจาก ESS** = (1) **navigation** (deep-link) + (2) **audit / CSQ self-access event** (in-flow security · §4). ไม่มี downstream data write เชิงบัญชี/สต๊อก/งบ/สถานะ owner.

## 4. Shared Rules (cross-boundary เท่านั้น)

> Source: FRD 05_RULES. เอาเฉพาะ rule ที่ module/feature อื่นต้อง conform หรือถูกกระทบ. Rule ภายใน (form validation, UI behavior, empty state) ตัดออก.

| Rule ID | Rule | กระทบใคร |
|---|---|---|
| BR-06 / LK-4 / VR-3 | **self-access เท่านั้น** · เข้าถึง employee_id ≠ self (ผ่าน param/URL) → **403 ที่ backend** (ไม่ใช่แค่ UI · ไม่ leak field ใด) | ENG-CSQ (SecC), Auth/gateway, all owner read-models · OQ-ESS-05 |
| BR-02 / LK-3 / VR-5 | สลิปอ่าน PS-1 · **self เท่านั้น · all-or-nothing** (เต็มใบ หรือ 403 · ห้าม partial field projection) | Payroll (F-HR-PAYROLL) |
| BR-03 / LK-2 | ยื่นคำขอ = **navigate (deep-link)** ไปหน้า owner feature · ESS ไม่ทำ form/ไม่รับ/ไม่บันทึกคำขอเอง · route [ASSUMED] ห้าม hardcode contract | Leave/OT/Expense/Profile/Cert owner features · OQ-ESS-02 |
| BR-03 (payload) | deep-link ส่งต่อ **การนำทาง (navigation) เท่านั้น · ไม่ส่ง payload ข้อมูล** — owner feature อ่าน context ผู้ใช้ (employee_id จาก session) เอง | 5 owner feature ปลายทาง |
| BR-01 / LK-1 | **ห้าม CRUD surface feature อื่น** (display-only) · ไม่มี mutation endpoint | ทุก owner feature ต้นทาง |
| BR-08 / LK-6 | audit อ่าน **append-only** (แก้/ลบไม่ได้) · masking ตาม self | audit/finance, DBA, ENG-CSQ (feed self-access) |
| CSQ (SecC) | ESS ยิง **self-access event เข้าท่อ SecC** ทุก read · event id = `ess.self_access` (CSQ_BRIEF_F059 ประกาศ) — **[ASSUMED · OQ-ESS-01]** ต้อง reconcile กับ HTML anchors `ess.restricted_view` (เปิด RESTRICTED) + `ess.access_denied` (403) ว่าท่อ SecC รับ 1 event รวม หรือ 2–3 event แยก. **ESS ห้ามประกาศ OC/DC ซ้ำ** (ประกาศเฉพาะ self-access ของ portal) | ENG-CSQ owner · OQ-ESS-01 |
| NTF (consume-only) | ESS **consume feed ของ ENG-NOTIFY เท่านั้น** (self-scope) · **ไม่ประกาศ/ไม่ยิง event** · ใช้ EVENT_GROUPS เดิมของ F-NOTIFY (ไม่นิยาม group/type ใหม่ · ไม่มีกลุ่ม `ess_*`) · `ref` ในแต่ละใบ = owner ใส่ตอน emit ไม่ใช่ ESS | ENG-NOTIFY (F-NOTIFY) · OQ-ESS-NTF-01 |
| RESTRICTED (VR-2) | national_id/bank/สลิป money = **read-through จาก owner** · ESS mask ก่อนส่งถึง client + enforce self ที่ backend · reveal เฉพาะ self → log `reveal_restricted`. Register Restricted Resources ทำที่ owner feature (ESS อ้างอิง) | Policy Center (Data Classification), owner features · OQ-ESS-05 |

**Permission matrix (backend-enforced):** พนักงาน (self) = ดูข้อมูลตัวเองทุก surface (masking ตาม self) · ยื่นคำขอ = navigate-out · ดูข้อมูลคนอื่น = **❌ 403** · CRUD ใน ESS = ❌ (ไม่มี) · อนุมัติ = ❌ (ไม่มีในพอร์ทัล). ไม่มี admin/manager ในรอบนี้ (NS-4). **SoD N/A ภายใน ESS** (ไม่มี maker/approver ของตัวเอง — mutation/approval ทั้งหมดเกิดที่ owner feature หลัง deep-link).

## 5. Integration

- **Depends on (upstream · soft ref/hook · read-only · self-scope):**
  - Payroll (F-HR-PAYROLL §0.13.2) — Payslip PS-1 (all-or-nothing · RESTRICTED · PDF จากต้นทาง)
  - การลา · OT/Attendance · ระบบกะ/บันทึกเวลา (Time·W2) · Expense (F101) · หนังสือรับรอง · สวัสดิการ (F102)/อบรม · Employee Master (profile) — read-model view (field-level contract = [ASSUMED · resolve เมื่อ owner ba-done])
  - **ENG-NOTIFY (F-NOTIFY)** — consume feed my notifications (read-only · ESS ไม่ยิง event)
  - **ENG-CSQ (SecC)** — self-access enforcement (ทุก read ผ่าน guard · emit self-access event)
- **Depended by (downstream):** **ไม่มี documented consumer — ESS = leaf portal** (ไม่ผลิตธุรกรรม/entity/event ให้ feature อื่นอ่าน). ผลลัพธ์ที่ไหลออก = navigation (deep-link ไป 5 owner feature) + self-access audit/CSQ event เท่านั้น · ไม่มี downstream เชิงบัญชี/สต๊อก/งบ. `[not documented]` — ไม่มี feature ใดอ่าน/เรียกของ ESS.
- **Declarations (รอบนี้ 2026-09-10 · NOTE only ใน FRD — ไม่ generate ใน pack):**
  - **DOA** [no] — NOT-NEEDED (portal อ่านอย่างเดียว · ไม่มี approval step ในพอร์ทัล · §12 doa=no)
  - **NTF** [need · **consume-only**] — 0 emit events · consume ENG-NOTIFY feed (FN-06/FN-09 · self-scope). owner features ประกาศ event ในใบของตัวเอง. Read-contract `ENG-NOTIFY.list(employee_id, self)` = **[ASSUMED · OQ-ESS-NTF-01]** (signature/pagination/filter รอ ENG-NOTIFY owner ยืนยัน)
  - **CSQ** [need] — self-access เข้าท่อ **SecC** · event `ess.self_access` (**[ASSUMED · OQ-ESS-01]** reconcile กับ `ess.restricted_view` + `ess.access_denied`). ไม่ประกาศ OC/DC/AC/FC/SC. csq ไม่มี runnable declaration skill (คัดใส่ pack ตามมติผู้ใช้)
  - **DOCCFG** [no] · **PDFDOC** [no] — ไม่มีเอกสาร/เลขรัน/PDF ของตัวเอง (มาจาก owner feature)
- **Engine hooks:** ENG-CSQ (SecC · self-access) · ENG-NOTIFY (consume feed) — external, existing · **ESS ไม่สร้าง engine ใหม่**. Auth = JWT + role-based · self-scope enforced ที่ backend.
- **Open dependencies (blocking · [ASSUMED]/[not documented]):**
  - **OQ-ESS-01** (YES · security wire) — CSQ event id ปลายทาง SecC: `ess.self_access` (1 รวม) vs `ess.restricted_view`+`ess.access_denied` (2 แยก) — PM/BA + ENG-CSQ owner เคาะก่อน dev
  - **OQ-ESS-02** (YES · navigation) — 5 deep-link routes ยัง **[ASSUMED contract]** — ยืนยัน route จริงกับ owner feature ก่อน dev
  - **OQ-ESS-05** (YES · PII) — self enforcement ที่ **backend** (employee_id ผ่าน URL/param → 401/403 ไม่ leak field) `[AI-DEFAULT]` = server-side guard ทุก read
  - **OQ-ESS-NTF-01** — read-contract feed ENG-NOTIFY = [ASSUMED] (รอ owner ยืนยัน) · mark-read เป็นของ ENG-NOTIFY `[AI-DEFAULT]`
  - (non-blocking `[AI-DEFAULT]`) OQ-ESS-03 deep-link fallback (route ไม่พร้อม → graceful notice) · OQ-ESS-04 surface down → per-card degrade · OQ-ESS-06 re-auth ก่อนเปิด RESTRICTED (P6 optional)

---
*trace: §1 ← FRD 00_OVERVIEW + BRD §2 · §2 ← FRD 04_DB · §3 ← FRD 02_API · §4 ← FRD 05_RULES (+ CSQ/NTF briefs) · §5 ← BRD §12.1 + NTF/CSQ briefs + 00_OVERVIEW §0.5/§0.8*
