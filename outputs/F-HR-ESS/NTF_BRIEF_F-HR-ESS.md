# NTF_BRIEF — F-HR-ESS · ESS Portal (พนักงานทำเอง) — F059

> ยิงผ่าน **ENG-NOTIFY (F-NOTIFY)** เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไขใน feature
> **DOA events (doa_pending / doa_result / doa_escalate) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้ (ประกาศซ้ำ = BLOCK)**
> Source: FRD 03_LOGIC (FN-06 `consumeNotifyFeed` · FN-09/90) + 05_RULES (§5.1 BR / VR-4 / §5.7) + `ess.html` L2481 (consume anchor) + PREBRIEF §12 (NTF chip ✓ · need)

## ⚠️ ESS = CONSUMER-ONLY — Declared EMIT events: **0 (ศูนย์)**

ESS เป็น **portal aggregate / display-only** (archetype = portal · PREBRIEF บรรทัด 2). มี **read-side logic** จริง (aggregate/self-guard/mask/consume feed) แต่ **ไม่มี mutation · ไม่มี state transition · ไม่มี Engine ของตัวเอง** (03_LOGIC §4 R9-note · §3.2 Engines = ว่าง). ดังนั้น:

- ✅ ESS **อ่าน (consume)** feed ของ ENG-NOTIFY = surface "แจ้งเตือนของฉัน" (FN-09/FN-06 · S-09)
- ❌ ESS **ไม่ผลิต business event ใด ๆ** ที่จะ wire เข้า ENG-NOTIFY — ทุก notifiable event เกิดที่ **owner feature ต้นทาง** (Leave / OT / Attendance / Expense / Cert / Welfare / Training / Payroll) ซึ่งประกาศ NTF ในใบของตัวเองแล้ว
- ❌ **ไม่มี DOA ใน ESS** (BR portal อ่านอย่างเดียว · §12 DOA=no) → จึง **ไม่มี `doa_pending`/`doa_result`/`doa_escalate`** ให้ประกาศ/ตัดออก (ไม่มีตั้งแต่ต้น)

> **ทำไม emit = 0 ไม่ใช่การมองข้าม:** notification ทุกใบใน feed ของ ESS (สลิปออก · ผลอนุมัติลา/OT/เบิก · หนังสือรับรองพร้อม ฯลฯ) ถูก **emit ที่ feature เจ้าของ event** แล้ว ESS แค่ดึงมาแสดงรวม + deep-link กลับไปหน้าต้นทาง. ถ้า ESS ประกาศ/emit ซ้ำ = **event ซ้ำซ้อน + ผิด ownership** (BR-01 ห้าม CRUD/แตะ logic feature อื่น).

---

## §A · Consume Surface (ฝั่งอ่าน — สิ่งที่ ESS "ทำ" กับ ENG-NOTIFY)

| # | Surface | อ้าง FRD | Scope | Contract (อ่าน) | หมายเหตุ |
|---|---|---|---|---|---|
| C-1 | แจ้งเตือนของฉัน (my notifications feed) | FN-06 `consumeNotifyFeed` · FN-09/90 · API-05 `GET /ess/notifications` · S-09 | **self เท่านั้น** (employee_id จาก token · FN-04 guard) | `ENG-NOTIFY.list(employee_id, self)` — **[ASSUMED contract · OQ-ESS-NTF-01]** | read + filter (q + unread) · consume-only · ไม่ write กลับ |
| C-2 | badge/นับ unread (การ์ด dashboard + ระฆัง) | FN-01 → FN-06 (notify count) · qcard 'bell' (`ess.html` L2323) | self | นับจาก feed เดียวกัน (C-1) | อ่านอย่างเดียว |

**พฤติกรรมฝั่ง consume ที่ต้องรู้:**
- **filter/empty:** ค้น/กรอง (ทั้งหมด · ยังไม่อ่าน) ไม่พบ → **empty state ไม่ใช่ error** (VR-4 · FN-90 · "ไม่พบการแจ้งเตือน / ลองล้างคำค้นหรือตัวกรอง")
- **deep-link:** กดรายการ → navigate ไปหน้า owner feature (FN-08 · route จาก config · ไม่ mutate · ไม่ยิง event)
- **mark-read:** = **owner ของ ENG-NOTIFY** ทำ ไม่ใช่ ESS (`[AI-DEFAULT]` · 03_LOGIC FN-06 side-effect "ไม่มี write กลับ NOTIFY")
- **group ที่ feed อ้างถึง:** ใช้ EVENT_GROUPS เดิมของ F-NOTIFY ทั้งหมด (DOA · เอกสารธุรกรรม · อื่น ๆ) filter ด้วย self-scope — ESS ไม่นิยาม group/type ใหม่

---

## §B · Emit Events (ฝั่งยิง)

**ไม่มี — ว่างโดยเจตนา (0 event).**

| Event ID | Trigger | สถานะ |
|---|---|---|
| — | — | ESS emits no events (consumer-only · ดู §A) |

---

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)

**ไม่เพิ่ม — 0 บรรทัด.** ESS ไม่ประกาศ event ใหม่ · EVENT_GROUPS ปัจจุบัน (DOA / เอกสารธุรกรรม / อื่น ๆ) ครอบ feed ที่ ESS อ่านอยู่แล้ว. **ไม่มีกลุ่ม "ess_*"**.

## Dev wiring note

- **ฝั่ง consume เท่านั้น:** ESS เรียก `ENG-NOTIFY.list(employee_id, self)` (read feed) — **ไม่มี `ENG-NOTIFY.emit(...)` ใน ESS เลย**
- self-scope บังคับที่ **backend** (FN-04 · VR-3 · OQ-ESS-05) — feed ต้อง filter employee_id = token, เข้าถึง feed คนอื่น = 403 (ไม่ leak)
- **ห้ามเช็ค channel preference / mark-read เอง** — เป็นของ ENG-NOTIFY + config กลาง (F-NOTIFY)
- notification ทุกใบใน feed มี `ref` (soft-ref ไปเอกสารต้นทาง เช่น PR/SO/leave_no) — ref นี้ **owner feature เป็นคนใส่ตอน emit** ไม่ใช่ ESS

## Iron check (Quality Gate)

- [x] **ไม่ประกาศ** `doa_pending`/`doa_result`/`doa_escalate` — ไม่มี DOA ใน ESS (portal อ่านอย่างเดียว · §12 DOA=no) → ไม่มีตั้งแต่ต้น
- [x] **ไม่ประกาศ emit event ปลอม** — ทุก event มาจาก owner feature ต้นทาง (BR-01) · ESS = consumer
- [x] ไม่ระบุ email/LINE ใน logic feature (channel = user preference + config กลาง F-NOTIFY)
- [x] consume surface มี `ref` ครบ (soft-ref จาก owner) · self-scope บังคับที่ backend
- [x] **ไม่แตะ CSQ:** `ess.self_access` / `ess.restricted_view` / `ess.access_denied` = ท่อ **SecC/CSQ** (CSQ_BRIEF_F059 · OQ-ESS-01) — **ไม่ใช่ NTF event** ไม่อยู่ในใบนี้

## OQ / [ASSUMED] carried

- **OQ-ESS-NTF-01 [ASSUMED contract]:** signature/scope จริงของ feed read (`ENG-NOTIFY.list(employee_id, self)` — ชื่อ method · pagination · filter param `q`/`unread`) ยังเป็น [ASSUMED] · ให้ ENG-NOTIFY owner ยืนยัน read-contract ก่อน dev wire
- **[AI-DEFAULT]:** mark-read เป็นของ ENG-NOTIFY (ESS ไม่ write กลับ) — รอ BA ยืนยันว่า ESS ต้องมีปุ่ม mark-read (proxy call) หรือ read-only ล้วน
- **หมายเหตุ scope:** csq (SecC self-access) จัดการแยกใน `CSQ_BRIEF_F059` + FRD 05_RULES §5.7 — **ไม่มี runnable declaration skill** · ไม่รันในรอบนี้

---
_declaration รอบนี้: NTF (CONSUMER-ONLY · 0 emit events · consume feed FN-06/FN-09 self-scope) · 2026-09-10 · Source: FRD 03_LOGIC/05_RULES + ess.html L2481 + PREBRIEF §12_
