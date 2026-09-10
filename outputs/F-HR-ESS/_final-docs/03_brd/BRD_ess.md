# BRD — ESS Portal (พนักงานทำเอง) · F-HR-ESS (F059)

> Business Requirements Document · Lane Mode v2 (HTML-first) · WF-01 SOW3.2
> Conflict priority ที่ใช้เขียนเอกสารนี้: **LOCK (HANDOFF) > PREBRIEF business intent > HTML หน้าจอจริง**
> Source of truth หน้าจอ = `outputs/F-HR-ESS/ess.html` (portal aggregate · display-only launcher)

---

## Section 1 · Document Info

| ฟิลด์ | ค่า |
|---|---|
| BRD ID | BRD-F-HR-ESS |
| Feature | ESS Portal — พนักงานทำเอง (Employee Self-Service) |
| รหัสฟีเจอร์ | F059 · F-HR-ESS |
| ประเภท | New Feature |
| Archetype | **portal(aggregate)** — display-only + deep-link (ไม่ CRUD) |
| Version | v2.0 (pipeline BRD — sync กับ launcher HTML หลัง BA re-gate) |
| Status | APPROVED (ผ่าน Quality Gate §7 — ดู AI Review Report ท้ายเอกสาร) |
| Wave | W6 · Phase A |
| Owner | BA (2BSimple) |
| Stakeholders | HR, พนักงานทุกคน (self), Payroll/Leave/OT/Expense/Cert/Welfare/Training/Notification owner features |
| Declarations | **ntf = need** · **csq = need** · doa = no · doccfg = no · pdfdoc = no |

### Changelog
- v1.0 (Phase A · Lane Mode v2): BRD ฉบับแรกจาก PREBRIEF + FUNCTION_CHECKLIST + HTML (home dashboard + 4 tabs, display-only, deep-link)
- **v2.0 (2026-09-10): sync Screen Inventory กับ launcher HTML ปัจจุบัน หลัง BA re-gate** — เพิ่ม "ตารางกะของฉัน" (FN-04, read-only) + จัด deep-link เป็น 5 เส้นตามที่ปรากฏจริงบนจอ (leave/ot/expense/profile/cert) · ดู §14.7 Conflict/Drift Log

---

## Section 2 · Business Context

### 2.1 ปัญหา / โอกาส
ทุกวันนี้พนักงานต้องเข้าหลายระบบแยกกัน (เงินเดือน · การลา · OT/เวลา · เบิกค่าใช้จ่าย · หนังสือรับรอง · สวัสดิการ · อบรม · แจ้งเตือน) เพื่อดูข้อมูลของตัวเองและเริ่มยื่นคำขอ ทำให้เข้าถึงช้า สับสน และต้องพึ่ง HR เป็นตัวกลาง

### 2.2 เป้าหมาย business
รวม "มุมมองของฉัน" จากทุกโดเมน HR มาไว้ที่จุดเดียว (self-service) แบบอ่านอย่างเดียว และให้พนักงานเริ่มยื่นคำขอได้ในคลิกเดียวโดยนำทาง (deep-link) ไปยังหน้าฟีเจอร์เจ้าของ — ลดภาระ HR และเร่งการเข้าถึงข้อมูลของตัวเอง

### 2.3 ตัวชี้วัดความสำเร็จ (บังคับวัดได้)

| ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง / จากไหน | วัดเมื่อไหร่ |
|---|---|---|---|---|
| Self-service adoption (พนักงานที่เข้าใช้พอร์ทัล/เดือน) | ต้องเก็บ baseline ก่อน launch | ≥ 70% ของพนักงานทั้งหมด/เดือน | audit log การเข้าถึง (self-access) นับ unique employee | รายเดือน หลัง launch 90 วัน |
| % คำขอที่เริ่มต้นจากพอร์ทัล (deep-link initiate) | ต้องเก็บ baseline ก่อน launch | ≥ 50% ของคำขอ ลา/OT/เบิก | นับ deep-link click event เทียบยอดคำขอที่ owner feature | รายเดือน |
| เวลาเฉลี่ยเข้าถึงสลิป/สิทธิ์ของตัวเอง | ต้องเก็บ baseline (ผ่าน HR ปัจจุบัน) | ≤ 30 วินาที (self-serve) | client timing จาก login → เปิด view | รายไตรมาส |

> คู่ตัวชี้วัดกับ §17.3 KPI ครบทุกตัว (adoption/conversion/speed)

### 2.4 ที่มา
มติ OQ-HR-04 (ESS อ่านอย่างเดียว ไม่ CRUD ซ้ำ), STANDARD_BASELINE MUST-11 (capability matrix เทียบ Odoo/D365/SAP SF), LANE_BRIEF Phase A

---

## Section 3 · Scope

### 3.1 In Scope
- หน้ารวมของฉัน (home dashboard) — สรุป read จากหลาย surface: สลิปล่าสุด · โควตาลาคงเหลือ · OT เดือนนี้ · ใบเบิกค้าง · แจ้งเตือน
- ดูสลิปเงินเดือน + ประวัติ + YTD (อ่าน Payroll PS-1 · self · all-or-nothing)
- ดูวันลา/โควตาคงเหลือ (read)
- ดู OT / เวลา / การสแกน (read) + **ตารางกะของฉัน (read-only)**
- ดูใบเบิกค่าใช้จ่าย ของฉัน (read)
- ดูหนังสือรับรอง / เอกสาร ของฉัน (read)
- ดูสวัสดิการ/คงเหลือ · อบรม/ใบรับรอง ของฉัน (read)
- ดูโปรไฟล์/ข้อมูลส่วนตัว (read)
- แจ้งเตือนของฉัน (my notifications · อ่าน feed จาก ENG-NOTIFY)
- ยื่นคำขอ = **deep-link** ไปหน้าฟีเจอร์เจ้าของ (5 เส้น: ลา · OT · เบิก · แก้ข้อมูลส่วนตัว · หนังสือรับรอง)
- self-access guard (เห็นเฉพาะข้อมูลของตัวเอง · SecC · คนอื่น = 403)

### 3.2 Out of Scope
- สร้าง/แก้/ลบ ข้อมูลของ feature อื่น (ลา/เบิก/OT/เงินเดือน/โปรไฟล์) — ESS ไม่ CRUD (OQ-HR-04)
- ทำฟอร์มยื่นลา/OT/เบิก เองในพอร์ทัล — ทุกการยื่น = deep-link ไปหน้าเจ้าของ (A-ESS-02)
- ออกสลิป / หนังสือรับรอง / PDF เอง — มาจาก feature ต้นทาง (soft ref)
- ออกเอกสาร/เลขรันเอง (ไม่มี doccfg)
- อนุมัติ / สายอนุมัติในพอร์ทัล (ไม่มี doa)
- Manager self-service / ทีมของฉาน / อนุมัติแทน — NICE → ไม่รองรับรอบนี้ (ESS = พนักงาน)
- config เมนู/สิทธิ์เอง — Roles/Permission กลาง (#107)
- เข้าถึงข้อมูลพนักงานคนอื่น (403)

### 3.3 Assumptions
- surface ของ feature ที่ยัง ba-done → แสดงแบบ display-only + หมายเหตุ **[ASSUMED contract]** (soft ref)
- route ปลายทาง deep-link ทั้ง 5 เส้นเป็น **[ASSUMED contract]** — ต้องยืนยัน route จริงกับ feature เจ้าของก่อน FRD (ดู OQ-ESS-02)
- พนักงานใช้งานบนมือถือ (responsive)

### 3.4 Scope Lock ⭐ (สืบทอดจาก HANDOFF §3)

| LOCK | เนื้อหา | อ้าง |
|---|---|---|
| LK-1 | display-only ทุก surface · ห้าม CRUD feature อื่น | OQ-HR-04 · BR-01 |
| LK-2 | ยื่นคำขอ = navigate (deep-link) ไปหน้าฟีเจอร์เจ้าของ · ไม่ทำ form เอง | A-ESS-02 · BR-03 |
| LK-3 | สลิปอ่านจาก Payroll PS-1 · self เท่านั้น · **all-or-nothing** | F-HR-PAYROLL §0.13.2 · BR-02 |
| LK-4 | self-access เท่านั้น · เข้าถึงคนอื่น = 403 (SecC) | current-state §3 · BR-06 |
| LK-5 | surface ba-done = [ASSUMED contract] soft ref | BR-07 |
| LK-6 | CSQ = SecC เท่านั้น + NTF = อ่าน feed (ไม่นับ doa_*) · ไม่มี doa/doccfg/pdfdoc · audit อ่าน (append-only) | §12 · HANDOFF §3 |

> **LK-XX ห้าม override ตลอด chain** — business rule ใดขัด LOCK → LOCK ชนะ · SCOPE DRIFT ที่พบ = ดู §14.7 (ไม่มี drift ที่ชน LOCK — มีแค่ inventory sync)

---

## Section 4 · User Roles & Permissions

| Role | ดูข้อมูลของตัวเอง | เริ่มยื่นคำขอ (deep-link) | ดูข้อมูลคนอื่น | CRUD ใน ESS | อนุมัติ |
|---|:--:|:--:|:--:|:--:|:--:|
| พนักงาน (self) | ✅ ทุก surface (masking ตาม self) | ✅ (นำทางออก) | ❌ 403 | ❌ (ไม่มี) | ❌ (ไม่มีในพอร์ทัล) |
| System (ESS) | serve read จาก surface ต้นทาง | route ออกไปเจ้าของ | ปิดบัง/403 | — | — |

> role เดียวที่ใช้จริง = **พนักงาน (เห็นเฉพาะข้อมูลของตัวเอง)** · mobile-friendly · ไม่มี admin/manager ในรอบนี้

---

## Section 5 · User Journey (with COSO)

> **หมายเหตุ COSO/SoD:** ESS ไม่สร้างธุรกรรมของตัวเอง (display-only) — Maker/Checker/Approver ของคำขอทั้งหมดเกิดที่ **หน้าฟีเจอร์เจ้าของ** หลัง deep-link. ในพอร์ทัลมีเพียง System (serve read) + Employee (viewer). SoD จึง N/A ภายใน ESS และไม่ถูกละเมิด (ESS ไม่มี approval step).

| # | Step | ผู้ทำ | COSO Role | หน้าจอ/route จริง |
|---|---|---|---|---|
| 1 | login → เห็นหน้ารวมของฉัน (5 การ์ดสรุป) | พนักงาน | System (serve read) · Employee (view) | `home` |
| 2 | สลับแท็บ: หน้าหลัก / เงินเดือน & เวลา / เอกสาร & สิทธิ์ / แจ้งเตือน | พนักงาน | Employee (view) | `home`·`pay`·`docs`·`notify` |
| 3 | แตะการ์ด/แถว → เปิด drawer อ่านรายละเอียด (read-only) | พนักงาน | System (serve read) | drawer: payslip/leave/expense/cert/training/profile/notify |
| 4 | กด "ยื่นคำขอ" → action-picker เลือกประเภท | พนักงาน | Employee | modal `actionPicker` |
| 5 | เลือกประเภท → **navigate ออก** ไปหน้าฟีเจอร์เจ้าของ (form/submit อยู่ที่นั่น) | พนักงาน → owner feature | Maker/Checker/Approver = **owner feature** | deep-link `#/leave·ot·expense·profile·cert` |
| 6 (Exception) | พยายามเข้าถึงข้อมูลคนอื่น → ปิดบัง + 403 | System | System (guard) | modal `accessDenied` (403) |

**Alternative:** ดูสลิปย้อนหลัง/ประวัติ YTD (read · self · all-or-nothing) · ดูตารางกะสัปดาห์นี้ (read) · ดู feed แจ้งเตือน + ค้นหา/กรอง

---

## Section 6 · Data Entity & Fields

**ESS ไม่มี entity ของตัวเอง — เป็น aggregator (read-only view layer).** ไม่มีการเขียนข้อมูล ไม่มี running number ไม่มี snapshot ของตัวเอง

### 6.1 Surface ที่อ่าน (upstream · self-scope ทั้งหมด)

| # | Surface (view) | เจ้าของ feature | อ่านอะไร | หมายเหตุ |
|---|---|---|---|---|
| SR-1 | Payslip PS-1 | Payroll | สลิป + ประวัติ + YTD | self · all-or-nothing · RESTRICTED masking |
| SR-2 | Leave / โควตา | การลา | วันลา · โควตาคงเหลือ | [ASSUMED] |
| SR-3 | OT / เวลา / สแกน | OT/Attendance | OT เดือนนี้ · การสแกน | [ASSUMED] |
| SR-4 | ตารางกะ | ระบบกะ/บันทึกเวลา (Time · W2) | กะสัปดาห์นี้ (read) | [ASSUMED] · ESS ไม่แก้กะ |
| SR-5 | Expense | เบิกค่าใช้จ่าย | ใบเบิก + สถานะ | [ASSUMED] |
| SR-6 | Cert / เอกสาร | หนังสือรับรอง | เอกสารที่ออก | [ASSUMED] |
| SR-7 | Welfare / Training | สวัสดิการ/อบรม | คงเหลือ · ประวัติอบรม · ใบรับรอง | [ASSUMED] |
| SR-8 | Employee profile | ทะเบียนพนักงาน | ข้อมูลส่วนตัว | RESTRICTED masking · แก้ = deep-link |
| SR-9 | Notification feed | ENG-NOTIFY | แจ้งเตือนของฉัน (consume · ไม่ยิง event เอง) | ntf anchor ฝั่ง consume |
| SR-10 | Access audit | (ตัวเอง — อ่านผ่าน guard) | ประวัติการเข้าถึงข้อมูลของฉัน (append-only) | audit อ่าน |

### 6.2 ER Diagram
```
พนักงาน (self) ──(1:N read)──▶ [Payslip · Leave · OT · Attendance · Shift · Expense · Cert · Welfare · Training · Profile · Notification]
ESS Portal ──(aggregate/read-only)──▶ ทุก surface ข้างบน  (ไม่มี FK เขียนกลับ · ไม่มี entity ของตัวเอง)
ยื่นคำขอ ──(deep-link/navigate)──▶ owner feature (Leave/OT/Expense/Profile/Cert)
```

---

## Section 7 · User Stories & Acceptance Criteria (FN-01..94 · 15 FN)

| FN | Story (Given-When-Then ย่อ) | AC หลัก | trace |
|---|---|---|---|
| FN-01 | ในฐานะพนักงาน เมื่อเปิดหน้ารวม ต้องเห็นสรุปสลิปล่าสุด/โควตาลา/OT/ใบเบิกค้าง/แจ้งเตือน | 5 การ์ด read จากหลาย surface · แตะการ์ดเปิด view | S-01·BR-04 |
| FN-02 | เมื่อเปิดสลิป ต้องเห็นสลิป+ประวัติ+YTD เฉพาะของตัวเอง | อ่าน PS-1 · self · all-or-nothing · PDF จากต้นทาง | S-02·BR-02 |
| FN-03 | เมื่อดูวันลา ต้องเห็นโควตาคงเหลือ + ปุ่ม "ยื่นลา" นำทางออก | read · ปุ่มยื่นลา = deep-link `leave` (ไม่ทำ form เอง) | S-03·BR-03 |
| FN-04 | เมื่อดู OT/เวลา ต้องเห็น OT/การสแกน + ตารางกะสัปดาห์นี้ (read) | read-only · ไม่มี action แก้กะ | S-04·BR-01 |
| FN-05 | เมื่อดูใบเบิก ต้องเห็นใบเบิกของตัวเอง + ปุ่ม "ยื่นเบิก" นำทางออก | read · ปุ่ม = deep-link `expense` | S-05·BR-03 |
| FN-06 | เมื่อดูหนังสือรับรอง ต้องเห็นเอกสารที่ออก + ขอหนังสือ = นำทางออก | read · ขอ = deep-link `cert` | S-06·BR-01 |
| FN-07 | เมื่อดูสวัสดิการ/อบรม ต้องเห็นคงเหลือ+ประวัติ+ใบรับรอง | read | S-07·BR-01 |
| FN-08 | เมื่อดูโปรไฟล์ ต้องเห็นข้อมูลส่วนตัว + ปุ่ม "ขอแก้ข้อมูล" = ขออนุมัติ (นำทางออก) | read · แก้เองไม่ได้ · deep-link `profile` | S-08·BR-03 |
| FN-09 | เมื่อเปิดแจ้งเตือน ต้องเห็น feed ของฉัน (จากศูนย์แจ้งเตือน) | consume ENG-NOTIFY · ไม่ยิง event เอง | S-09·BR-08 |
| FN-10 | เมื่อพยายามเข้าถึงข้อมูลคนอื่น ต้องถูกปิดบัง + 403 | self-access · SecC · เห็นเฉพาะของตัวเอง | S-10·BR-06 |
| FN-11 | surface ที่ feature ยังไม่เสร็จเต็ม → แสดง display-only + [ASSUMED contract] | soft ref chip บนจอ | S-11·BR-07 |
| FN-90 | ค้นหา/กรองในรายการ + empty state | search notif + empty | กติกากลาง |
| FN-92 | หน้าจอ responsive ใช้บนมือถือได้ | breakpoint 1080/760 | BR-05 |
| FN-93 | audit การเข้าถึงข้อมูลของตัวเอง (append-only) | drawer "ประวัติการเข้าถึงข้อมูลของฉัน" | กติกากลาง |
| FN-94 | ปิดบัง/ไม่แสดงข้อมูลนอกขอบเขตของตัวเอง | banner self-scope + guard | BR-06 |

> ทุก Story ไม่มีคำว่า "และ" ที่ทำให้ต้องแยก (C05) · deep-link ไม่นับเป็น CRUD

---

## Section 8 · Status & Lifecycle

**ESS ไม่มี document lifecycle ของตัวเอง** — แสดงสถานะที่ **อ่านมาจาก feature ต้นทาง** (เช่น สลิป: ออกแล้ว · ใบเบิก: รออนุมัติ/อนุมัติ · อบรม: ผ่าน). ไม่มี state transition ที่ ESS เป็นเจ้าของ ไม่มี trigger ที่เปลี่ยนสถานะจากพอร์ทัล

```
(ไม่มี lifecycle ของตัวเอง)
owner feature state ──(read)──▶ ESS แสดงเป็น pill/badge อ่านอย่างเดียว
```

---

## Section 9 · Business Rules + Validation (+ Tags)

| BR | กฎ | ประเภท | Tag | ใครเปลี่ยน/บ่อย |
|---|---|---|---|---|
| BR-01 | ห้าม CRUD surface feature อื่น (display-only) | Prevent | **FIXED** | — (สถาปัตยกรรม) |
| BR-02 | สลิปอ่าน PS-1 · self เท่านั้น · all-or-nothing | Prevent | **FIXED** | — |
| BR-03 | ยื่นคำขอ = navigate ไปหน้าเจ้าของ (ไม่ทำ form เอง) | Trigger | **FIXED** | — |
| BR-04 | dashboard = สรุป read จากหลาย surface | — | **CONFIGURABLE** 🤖 | HR/Admin · การ์ดที่โชว์ (นานๆครั้ง) |
| BR-05 | responsive (พนักงานใช้มือถือ) | — | **FIXED** | — |
| BR-06 | self-access เท่านั้น · เข้าถึงคนอื่น = 403 (SecC) | Prevent/Error | **FIXED** | — (ท่อ CSQ SecC) |
| BR-07 | surface ba-done = [ASSUMED contract] soft ref | Warning | **WARNING** | resolve ตอน feature เจ้าของ done |
| BR-08 | audit(อ่าน) append-only · masking ตาม self | — | **FIXED** | — |

### 9.x Validation
- VR-1: route deep-link ปลายทางไม่ยืนยัน → แสดง [ASSUMED] chip · ไม่ hardcode contract (ยกเป็น OQ-ESS-02)
- VR-2: ข้อมูล RESTRICTED (personal/salary) → masking ตาม self · ไม่โชว์นอกขอบเขต
- VR-3: เข้าถึง employee id ≠ self → 403 modal (ไม่ leak field ใด)

---

## Section 9.5 · สรุประดับความยืดหยุ่น

| Rule | ระดับ | เหตุผล | ที่มา |
|---|---|---|---|
| BR-01/02/03/05/06/08 | FIXED | สัญญาสถาปัตยกรรม portal display-only + SecC — เปลี่ยนไม่ได้โดยไม่เปลี่ยน archetype | ✅ LOCK |
| BR-04 (การ์ด dashboard ที่โชว์) | Admin Panel (CONFIGURABLE) | รายการ surface/การ์ดที่รวมอาจปรับได้เป็นระยะ | 🤖 AI-inferred |
| BR-07 (soft ref) | WARNING | รอ feature เจ้าของ ba-done → เปลี่ยนเป็น contract จริง | ✅ |

> ไม่มี rule ระดับ DYNAMIC/Engine ที่ AI เดา → ไม่ต้อง escalate เกินที่ลง §15 · BR-04 (🤖 Admin Panel) ปล่อยผ่านได้ mark 🤖 ไว้

---

## Section 10 · Edge Cases

### 10.1 จาก PREBRIEF/HTML (☑ ยืนยันแล้ว)
- ☑ เข้าถึงข้อมูลคนอื่น → 403 + ปิดบัง (มี modal จริง)
- ☑ surface ba-done → display-only + [ASSUMED] chip
- ☑ ยื่นคำขอ = deep-link (ไม่มี form ในพอร์ทัล)
- ☑ empty state feed แจ้งเตือน (ค้นไม่เจอ → "ไม่พบการแจ้งเตือน")
- ☑ mobile responsive (พนักงานใช้มือถือ)
- ☑ สลิป all-or-nothing (เห็นทั้งใบ หรือไม่เห็นเลย)

### 10.2 จาก AI Pattern Matching (☐ แนะนำ — BA เคาะที่ SOW3.7)
- ☐ [PM] deep-link ปลายทาง route เปลี่ยน/ยังไม่พร้อม → fallback message (ไม่ค้าง) — **กระทบ navigation ยกเป็น OQ-ESS-02**
- ☐ [DI] surface ต้นทาง down/timeout → การ์ด/แถวแสดง "โหลดไม่ได้" ไม่ทำทั้งหน้าพัง
- ☐ [PM] session หมดอายุระหว่างเปิด drawer → re-auth ก่อนอ่าน RESTRICTED
- ☐ [CA] employee id ถูกส่งผ่าน URL/param ตรง ๆ → ต้อง enforce self ที่ server ไม่ใช่แค่ UI (401/403)
- ☐ [PD] สลิป PDF จากต้นทางยังไม่ออก → ปุ่มดาวน์โหลด disabled + เหตุผล

---

## Section 11 · Impact / Regression
New Feature — ไม่มี regression ของ ESS เอง. **ผลกระทบทางอ้อม:** ผูกกับ surface ของ 9-10 feature ต้นทาง — ถ้า owner feature เปลี่ยน field/route ที่ ESS อ่าน/ลิงก์ → ESS ต้อง re-verify contract (ดู §12.1)

---

## Section 12.1 · Value Stream & Downstream Impact ⭐

**Value Stream positioning:** ESS = **HR self-service access layer** — ไม่ผลิตธุรกรรมเอง เป็นหน้าต่างรวม (read) + จุดเริ่ม (deep-link) ของสาย HR (Payroll/Leave/OT/Expense/Cert/Welfare/Training)

**Upstream (อ่านเข้ามา):** 10 surface (§6.1) — self-scope ทั้งหมด

**Downstream Impact Map:**

| ปลายทาง | ข้อมูล/สิ่งที่ไหลไป | Trigger | ถ้า ESS เปลี่ยน/ปลายทางเปลี่ยน |
|---|---|---|---|
| การลา (Leave) | navigate ผู้ใช้ไปหน้ายื่นลา | กด "ยื่นลา"/action-picker | route `#/leave/new` [ASSUMED] — ยืนยันก่อน FRD |
| ขอ OT | navigate ไปหน้ายื่น OT | action-picker | route `#/ot/new` [ASSUMED] |
| เบิกค่าใช้จ่าย (Expense) | navigate ไปหน้ายื่นเบิก | กด "ยื่นเบิก"/picker | route `#/expense/new` [ASSUMED] |
| แก้ข้อมูลพนักงาน (Profile) | navigate ไปหน้าขออนุมัติแก้ข้อมูล | กด "ขอแก้ข้อมูล"/picker | route `#/profile/edit-request` [ASSUMED] |
| หนังสือรับรอง (Cert) | navigate ไปหน้าขอหนังสือ | กด "ขอหนังสือ"/picker | route `#/cert/new` [ASSUMED] |
| ENG-NOTIFY | consume feed (อ่าน) · ESS ไม่ยิง event | เปิดแท็บแจ้งเตือน | ถ้า event catalog เปลี่ยน → ปรับ mapping (OQ-ESS-01) |
| ENG-CSQ (SecC) | self-access enforcement | ทุกการอ่าน | เปลี่ยน SecC policy → ปรับ guard |

> ไม่มี downstream เชิงบัญชี/สต๊อก/งบ (ESS ไม่ผลิตธุรกรรม) · ไม่มี DOA/DOCCFG/PDFDOC

---

## Section 12.3 · Existing System Reference

| Rule/Need | ระดับ | มีอยู่แล้ว? | Reference |
|---|---|:--:|---|
| self-access SecC (BR-06) | Engine (กลาง) | ⚠️ ผูก | ENG-CSQ · CSQ_BRIEF_F059 (SecC · event `ess.restricted_view` / `ess.access_denied`) |
| notification feed (BR-08) | Engine (กลาง) | ✅ | ENG-NOTIFY (consume — ไม่ประกาศ event ใหม่ที่ยิงเอง) |
| surface อ่าน 10 ตัว | owner feature | ⚠️ บางตัว ba-done | [ASSUMED contract] soft ref (BR-07) |
| deep-link routes (5) | owner feature | ⚠️ ยังไม่ยืนยัน | route ปลายทาง [ASSUMED] → OQ-ESS-02 |

---

## Section 13 · Delivery Phases

- **Phase 1 (Launch):** home dashboard + 4 tabs + read drawers ทั้งหมด · self-access guard (403) · masking · consume ENG-NOTIFY feed · deep-link stub 5 เส้น (navigate-out) · [ASSUMED] chip บน surface ba-done · audit อ่าน append-only. ห้าม hardcode contract/route — อ่านจาก config/owner feature
- **Phase 2 (Admin Panel):** BR-04 — ปรับรายการการ์ด/surface ที่ dashboard รวม (ถ้าต้องการ)
- **Phase 3 (Rule Mgmt):** — (ไม่มี rule ระดับนี้)
- **Phase 4 (Engine):** — (ผูก ENG-CSQ/ENG-NOTIFY กลางที่มีอยู่แล้ว — ไม่สร้าง engine ใหม่)

---

## Section 14 · Dev Requirements Summary "ใบสั่ง"

### 14.1 Config Foundation
- surface registry: รายการ surface + route อ่าน (self-scope) — จาก config ไม่ hardcode
- deep-link route table (5 เส้น) — อ่านจาก config/owner feature (ยัง [ASSUMED] · ยืนยันก่อน dev)
- CSQ SecC binding: `ess.restricted_view`, `ess.access_denied` (ตาม CSQ_BRIEF_F059 · ห้ามประกาศ OC/DC ซ้ำ)

### 14.2 ข้อกำหนดจาก Tag
- BR-04 (Admin Panel): ทำ dashboard card list เป็น config-driven — ไม่ hardcode ว่าโชว์การ์ดไหน
- BR-01/02/03/06 (FIXED): enforce ที่ server — **self-access ต้องบังคับที่ backend** ไม่ใช่แค่ซ่อน UI

### 14.3 Edge Cases สำคัญ
- self enforcement ที่ server (id ผ่าน param → 403) · surface down → graceful degrade ต่อการ์ด · สลิป all-or-nothing

### 14.4 WARNING รอข้อสรุป
- BR-07 surface ba-done → รอ feature เจ้าของ done เพื่อเปลี่ยน [ASSUMED] เป็น contract จริง (หารือ BA/owner)
- deep-link routes → รอยืนยัน route จริง (OQ-ESS-02)

### 14.5 Regression Scope
N/A (New Feature) — แต่ผูก contract กับ owner features (ตรวจซ้ำเมื่อ owner เปลี่ยน)

### 14.6 Functions Cut (= หมวด "ไม่รองรับ" ใน FUNCTION_CHECKLIST)
- ✕ แก้ไข/สร้าง/ลบ ข้อมูลของ feature อื่น — [OQ-HR-04] ESS อ่านอย่างเดียว
- ✕ ทำฟอร์มลา/เบิก/OT เองในพอร์ทัล — [A-ESS-02] deep-link ไปเจ้าของ
- ✕ ออกสลิป/หนังสือรับรอง/PDF เอง — มาจาก feature ต้นทาง (soft ref)
- ✕ Manager self-service / อนุมัติในพอร์ทัล — [OQ NICE] รอบนี้ ESS พนักงาน
- ✕ config เมนู/สิทธิ์เอง — [#107] Roles/Permission กลาง

### 14.7 Screen Inventory + UI Signals (หยาบ — spec จริงไป FRD)

| # | หน้าจอ/มุมมอง | route/anchor (จาก HTML) | ประเภทหยาบ | ผู้ใช้ | หน้าที่ (business) | FN |
|---|---|---|---|---|---|---|
| P-01 | หน้ารวมของฉัน (dashboard) | tab `home` | dashboard | พนักงาน | 5 การ์ดสรุป read + ทางลัด + ปุ่มยื่นคำขอ | FN-01 |
| P-02 | เงินเดือน & เวลา | tab `pay` | หน้ารายการ (read) | พนักงาน | สลิป · วันลา+ยื่นลา · OT/เวลา/สแกน · ตารางกะ | FN-02·03·04 |
| P-03 | เอกสาร & สิทธิ์ | tab `docs` | หน้ารายการ (read) | พนักงาน | ใบเบิก+ยื่นเบิก · หนังสือรับรอง+ขอ · สวัสดิการ/อบรม · โปรไฟล์+ขอแก้ | FN-05·06·07·08 |
| P-04 | แจ้งเตือน | tab `notify` | หน้ารายการ (read) | พนักงาน | feed แจ้งเตือน + ค้นหา/กรอง + empty | FN-09·90 |
| P-05 | action-picker "ยื่นคำขอ" | modal `actionPicker` | หน้ายืนยัน/ตัวเลือก | พนักงาน | 5 แถว → navigate ออก (ลา/OT/เบิก/แก้ข้อมูล/หนังสือรับรอง) | FN-03·05·06·08 |
| P-06 | drawer อ่านรายละเอียด (read-only) | `openView(...)` | หน้ารายละเอียด | พนักงาน | payslip/leave/expense/cert/training/profile/notify (read) | FN-02..09 |
| P-07 | เข้าถึงถูกปฏิเสธ (403) | modal `accessDenied` | หน้าแจ้งข้อผิดพลาด | System | ปิดบัง + 403 self-access | FN-10·94 |

**สรุป:** ~7 มุมมอง (1 dashboard + 3 tab list + 1 action-picker + read drawers + 1 403 modal) — **หน้าจอทั้งหมดใน 1 เมนู/พอร์ทัลเดียว (#106 · 1 feature = 1 เมนู)**

**UI Signals ส่งต่อ FRD:** ❌ ไม่ใช่ Document/Transaction (ไม่มี approver/พิมพ์/ลายเซ็นของตัวเอง) · ❌ ไม่มี print/PDF ที่ ESS ผลิตเอง (มาจากต้นทาง) · ✅ deep-link semantics (navigate-out ทุก action) เป็น pattern หลัก · ✅ read-only drawer pattern · ✅ 403 self-access modal · ⚠️ 5 deep-link route = [ASSUMED contract] (OQ-ESS-02)

### 14.8 Conflict / Drift Log (BA old BRD vs current launcher HTML)
> HTML = truth สำหรับหน้าจอ · PREBRIEF/HANDOFF = truth สำหรับ business lock. รายงานไว้ ไม่ resolve เงียบ:

| # | จุด | BA old BRD (pack) | Launcher HTML ปัจจุบัน | ตัดสิน |
|---|---|---|---|---|
| D-01 | ชุด deep-link | §12.1 ระบุ 6 ปลายทาง: Leave/Expense/OT/**Training/Welfare**/Cert (ไม่มี Profile) | action-picker + ปุ่ม inline = **5 เส้น: leave/ot/expense/profile/cert** (ไม่มี Training/Welfare) | **ใช้ HTML** — 5 เส้นตามจอจริง · Training/Welfare = read-only ไม่มีปุ่ม navigate · Profile มี "ขอแก้ข้อมูล" = deep-link |
| D-02 | ตารางกะ (shift table) | ไม่ระบุชัดใน §3/§6 | มี "ตารางกะของฉัน" (read-only) ใต้ FN-04 แท็บ pay | **เพิ่มเข้า inventory** (D-01/D-02 คือของที่ BA re-gate เพิ่ม) |
| D-03 | จำนวน tab | §1 "home dashboard + 4 tabs" | home/pay/docs/notify = 4 seg-tab (home รวม dashboard) | ตรงกัน ✅ |

> ไม่มี drift ที่ชน LOCK — ทั้งหมดเป็นการ sync inventory ให้ตรงจอ (business intent เดิมคงอยู่: display-only + deep-link)

---

## Section 15 · Open Questions

| OQ | คำถาม | สถานะ | หมายเหตุ |
|---|---|:--:|---|
| **OQ-ESS-01** | CSQ event id ที่ ESS ใช้ (`ess.restricted_view` / `ess.access_denied`) ยืนยันปลายทาง SecC → ส่งต่อ FRD | ⚠️ รอ | ห้าม ESS ประกาศ OC/DC ซ้ำ · อ้าง CSQ_BRIEF_F059 |
| **OQ-ESS-02** | 5 deep-link routes (`#/leave/new`·`#/ot/new`·`#/expense/new`·`#/profile/edit-request`·`#/cert/new`) ยัง [ASSUMED contract] — ยืนยัน route จริงกับ feature เจ้าของก่อน FRD | ⚠️ รอ | เดาผิด = navigate ค้าง |
| OQ-ESS-A1 | A-ESS-01 อ่านทุก surface display-only (OQ-HR-04) | ✅ ตอบแล้ว | LOCK LK-1 |
| OQ-ESS-A3 | A-ESS-03 surface ba-done = [ASSUMED contract] soft ref | ✅ ตอบแล้ว | BR-07 |

---

## Section 16 · Security & Compliance

- **16.1 Preset:** **P6 (HR / PII Sensitive · 15 controls)** — ข้อมูลเงินเดือน/ส่วนตัวเป็น RESTRICTED
- **16.2 มาตรฐานที่ใช้:** self-access (SecC) · least privilege · data masking · audit trail
- **16.3 Control Checklist (หลัก):**
  - ✓Must: self-access enforcement ที่ **server** (ไม่ใช่แค่ UI) · เข้าถึงคนอื่น = 403
  - ✓Must: masking personal/salary (RESTRICTED) ตาม self
  - ✓Must: audit อ่าน (append-only · แก้/ลบไม่ได้)
  - ✓Must: ESS ไม่มี write path → ลด attack surface (display-only by design)
  - ○Optional: re-auth ก่อนเปิดข้อมูล RESTRICTED (session)
- **16.4 Risk Statement:**
  - R-A: leak ข้อมูลคนอื่น (id ผ่าน param) → Mitigate: server-side self guard + 403 (BR-06/FN-10/FN-94)
  - R-B: สลิปบางส่วนรั่ว → Mitigate: all-or-nothing (BR-02)
  - R-C: deep-link ปลายทางปลอม/เปลี่ยน → Mitigate: route จาก config + ยืนยัน contract (OQ-ESS-02)

---

## Section 17 · Health Check

- **17.1 SLA:** เปิดหน้ารวม/สลิป ≤ 2 วินาที (read) · deep-link redirect ≤ 1 วินาที
- **17.2 Control Points:** self-access guard (ทุก read) · audit append (ทุกการเปิดข้อมูล)
- **17.3 KPI:**
  - Adoption: unique employee ที่ใช้พอร์ทัล/เดือน (≥70%) — คู่ §2.3
  - Conversion: % คำขอที่เริ่มจาก deep-link (≥50%) — คู่ §2.3
  - Speed: เวลาเข้าถึงสลิป/สิทธิ์ (≤30 วินาที) — คู่ §2.3
- **17.4 Threshold:** 403 rate ผิดปกติ (พยายามเข้าถึงคนอื่น) เกิน N ครั้ง/ชม. → alert security
- **17.5 Throughput:** อ่าน-only → scale ตาม read replica ของ surface ต้นทาง (ESS ไม่เพิ่ม write load)

---

## Section 18 · Monitoring

- **18.1 Reports:** Access report (self-access log) · Adoption report · Deep-link conversion report
- **18.2 Dashboard Widgets:** adoption trend (KPI) · 403 attempts (threshold) · conversion funnel (deep-link)
- **18.3 Performance:** เวลาโหลด dashboard/สลิป
- **18.5 Anomaly:** 403 spike (เข้าถึงคนอื่นผิดปกติ) · surface อ่านไม่ได้ต่อเนื่อง
- **18.6 Transaction:** N/A (ESS ไม่มีธุรกรรมของตัวเอง) — วัด event: view/open/deep-link เท่านั้น

---

## AI Review Report — BRD Generator Full

```
═══════════════════════════════════════
AI REVIEW REPORT — BRD F-HR-ESS (ESS Portal)
ประเภท: New Feature · portal(aggregate) display-only
วันที่ตรวจ: 2026-09-10
═══════════════════════════════════════
CHECKLIST:
✅ C01 Business Objective วัดผลได้ (§2.3 มี baseline/target/วิธีวัด)
✅ C02 User Roles ครบ (พนักงาน self + System)
✅ C05 ไม่มี Story ที่ต้องแยกด้วย "และ"
✅ C10 ทุก BR ที่มีเงื่อนไขติด Tag (FIXED/CONFIGURABLE/WARNING)
✅ C13 Edge Cases ครบหมวด (PM/DI/CA/PD)
✅ C18 WARNING ทุกข้อมีแผน (BR-07, deep-link → OQ)
✅ C19 §14 ใบสั่งครบ
✅ C20 Scope Lock §3.4 ครบ (LK-1..6 จาก HANDOFF) · ไม่มี scope เกินเงียบ
✅ C21 Value Stream §12.1 upstream + Downstream Map ตอบ "แล้วไงต่อ" ครบ
✅ C22 ตัวชี้วัด §2.3 มีคู่ใน §17.3 KPI
✅ C23 §9.5 marker 🤖/✅ ครบ · ไม่มี 🤖 DYNAMIC/Engine ค้าง
✅ PE01 COSO ระบุทุก step (SoD N/A — ESS ไม่มี approval; หมายเหตุใน §5)
✅ PE02 SoD ไม่ถูกละเมิด (ESS ไม่มี maker/approver ของตัวเอง)
✅ PE03 Security Preset P6 (HR/PII) + controls
✅ PE04 SLA/KPI/Threshold §17 ครบ
✅ PE05 Cross-section coverage ผ่าน (BR↔Edge, Control↔Health, KPI↔Monitor)
✅ Screen Inventory §14.7 = 7 มุมมอง · ทุกแถวมี route/anchor จริงจาก HTML · sync launcher (D-01/D-02 logged)

SUMMARY: ผ่าน 16/16 · สถานะ: ✅ APPROVED
หมายเหตุ: 2 OQ carried (OQ-ESS-01 CSQ event → FRD · OQ-ESS-02 5 deep-link routes [ASSUMED])
Declarations: ntf=need · csq=need · doa/doccfg/pdf=no
```

**สถานะเอกสาร: ✅ APPROVED — พร้อมเข้า frd-generator-v6**
