# 00_OVERVIEW — F-HR-ONBOARD · On/Offboard (เข้าออกงาน)

> FRD Pack · **variant: FULL** (9 ไฟล์) · `frd-generator-v6` **Lane Mode v2** (no-ask) · 2026-08-29
> **ไม่มี `PRINT_SPEC.md` ในแพ็กนี้** — feature นี้**ไม่มีท่อ pdfdoc และไม่มีท่อ doccfg** (`5_DECLARATIONS/NOT_NEEDED.md`) จึงไม่มีเอกสารที่ต้องพิมพ์ ไม่มีเลขที่เอกสาร และไม่มีสเปกการพิมพ์ · **นี่ไม่ใช่ไฟล์ที่หาย แต่คือไฟล์ที่ไม่มีตั้งแต่ต้น** — ผู้ตรวจแพ็กต้องไม่ตามหา
> เอกสารที่คนถือจริงในเวฟนี้เป็นของ **Employee Movement (`MV-YYYY-NNNN` · W3 lane B)** และ **หนังสือรับรอง (`CERT-YYYY-NNNN` · W3 lane C)** ซึ่งประกาศ `doccfg + pdfdoc` ไว้เอง

---

## §0.1 Document Control

| | |
|---|---|
| Feature ID | `F-HR-ONBOARD` |
| ชื่อ | On/Offboard — เข้าออกงาน (รอบเข้างาน · รอบออกงาน · การเพิกถอนสิทธิ์) |
| Module / Wave / Lane | HR · **W3** · Lane A |
| Archetype | **`master + checklist(OP)`** — ไม่ใช่ Pattern Q (ไม่มีเลขที่เอกสาร · ไม่มี PDF · ไม่มีแท็บลายเซ็น) และไม่ใช่ Pattern P (ไม่มีปฏิทิน/Gantt) |
| Variant | **FULL** (9 ไฟล์) — เพราะมี state machine 2 วงจร · สายอนุมัติจริง · read model ที่ปลายทาง 4 รายอ่าน · และ **ทะเบียนสิทธิ์ที่เป็นวัตถุตรวจสอบได้ซึ่งไม่เคยมีในระบบมาก่อน** |
| Upstream | `2_BRD/BRD_เข้าออกงาน.md` **v1.0 APPROVED** · `1_HTML/เข้าออกงาน.html` (5 route · ผ่าน S3a/S3b/S3c) · `PREBRIEF.md` v1.1 · `FUNCTION_CHECKLIST.md` **88 FN** · `5_DECLARATIONS/` (DOA · NTF · CSQ · NOT_NEEDED) |
| เวอร์ชัน | 1.0 · 2026-08-29 |
| สถานะ | **Phase 3.5 A–M ผ่านครบ** (รายงานที่ `INDEX.md`) |
| ผู้จัดทำ | BA (lane runner · S5) |
| ไฟล์ในแพ็ก | `00_OVERVIEW` · `01_UI` · `02_API` · `03_LOGIC` · `04_DB` · `05_RULES` · `06_TESTS` · `07_LOCKED_DECISIONS` · `INDEX` · (+ `UI_BRIEF_เข้าออกงาน.md` จาก S7) |
| **ไม่มีในแพ็ก** | **`PRINT_SPEC.md`** — ไม่มีท่อ pdfdoc (เหตุผลเต็มที่หัวไฟล์และ `NOT_NEEDED.md`) |

## §0.2 Revision History

| เวอร์ชัน | วันที่ | การเปลี่ยนแปลง |
|---|---|---|
| 1.0 | 2026-08-29 | สร้างจาก BRD v1.0 APPROVED + HTML ที่ผ่าน gate ครบ · coverage manifest ครบ **88 FN / 88 Story / 32 BR / 40 Edge / 24 Functions Cut** · declaration conformance **NTF 9 + CSQ 7 (disjoint)** · Scope Lock 11 ข้อสืบทอดครบ |

## §0.3 Scope

### In Scope

| # | ความสามารถ | ที่อยู่ในแพ็ก |
|---|---|---|
| 1 | รอบเข้างาน — สร้างจากแม่แบบ · pre-boarding · ถึงวันเริ่มงาน · ปิดรอบ | `01_UI §1.2.1` · `03_LOGIC §3.1 A` · `05_RULES §5.2.1` |
| 2 | รอบออกงาน — เหตุผลการออก · วันแจ้ง · วันทำงานวันสุดท้าย · แม่แบบปิดสิทธิ์ | `01_UI §1.2.2` · `03_LOGIC §3.1 B` |
| 3 | **การอนุมัติผ่าน DOA** — resolve + freeze + slot picker + SoD + re-resolve | `03_LOGIC §3.1 C` · `ENG-DOA-01` |
| 4 | ⭐ **ทะเบียนสิทธิ์และการเพิกถอน** — 8 ชนิด · คำขอ/ผลตอบกลับ · ธง overdue · คืนสิทธิ์ | `03_LOGIC §3.0` (กลไกหลัก) · `04_DB §4.2 T_onb_access_item` |
| 5 | การยกเลิก/ถอนการออก — ปิดงานค้าง · ถอนค่าที่เผยแพร่ · คำขอคืนสิทธิ์ | `03_LOGIC §3.1 E` |
| 6 | ทรัพย์สินระดับรอบ | `04_DB T_onb_asset_item` |
| 7 | การผูก checklist กับ Operation Process (1 งาน = 1 SOW) | `02_API §2.2` · `ENG-OPSOW-01` |
| 8 | ⭐ **Published Employment Window** (read model) | **§0.13** · `02_API §2.3` |
| 9 | masking · audit append-only · soft archive | `05_RULES §5.7` · `04_DB §4.6` |

### Out of Scope

**24 รายการ** — รายการเต็มพร้อมเหตุผลและจุดที่เห็นบนจออยู่ที่ `2_BRD §14.6.3` (NS-01…NS-24) และถูกยกมาเป็นแถวในแมนิเฟสต์ที่ **§0.12.4** · หัวข้อที่กระทบสถาปัตยกรรมมากที่สุด:

| # | ไม่ทำ | เจ้าของแทน |
|---|---|---|
| NS-03 | หน้าจัดการผู้ใช้ · role · matrix สิทธิ์ | **Roles & Permissions ✅ (#107)** — ที่นี่ออกได้แค่ "คำขอ" |
| **NS-04** ⭐ | **การติ๊กปิดรายการเพิกถอนเอง** | — **โดยการไม่มีความสามารถ** (BR-04) |
| **NS-07** ⭐ | **การประกาศท่อ OC** | **Operation Process** — `sow.*` ทำให้ OC เกิดเองที่ OP (ดู **§0.16.3**) |
| **NS-09** ⭐ | **การตั้งค่า/เดาระยะทดลองงาน · ระยะบอกกล่าว** | **HR Configuration** — **คีย์ยังไม่เผยแพร่ (OQ-STD-OB3)** |
| NS-13 | เอกสารเลขที่และไฟล์ PDF | Employee Movement · หนังสือรับรอง — **จึงไม่มี `PRINT_SPEC.md`** |
| NS-17 | การแก้ข้อมูล Attendance/Leave/Payroll/Employee Master | ต้นทางแต่ละราย (AT-5 · LV-5) |

### Out of Scope (จาก Phase 2.5 probing)

| # | ประเด็นที่ probing ตั้งขึ้นแล้วตัดออก | เหตุผล |
|---|---|---|
| P-01 | หน้ารวม "สิทธิ์ทั้งหมดของพนักงานหนึ่งคนข้ามรอบ" | เป็นมุมของ **Roles & Permissions** ไม่ใช่ของกระบวนการเข้า-ออก · ที่นี่เห็นเฉพาะสิทธิ์ในบริบทของรอบ |
| P-02 | การประเมินความเสี่ยงอัตโนมัติของแต่ละรอบ (risk scoring) | ต้องใช้ข้อมูลจาก Policy Center ที่ยังไม่มี · **จะกลายเป็นการเดา** |
| P-03 | การส่งอีเมลต้อนรับ/อำลาโดยตรงจาก feature | **ENG-NOTIFY เป็นเจ้าของช่องทาง** — feature ประกาศ event เท่านั้น |
| P-04 | การเก็บผลสัมภาษณ์ลาออกเป็นข้อมูลมีโครงสร้าง | scope note ตัด (NS-01) · มีเพียงไฟล์แนบ |

## §0.4 Roles & Responsibilities (COSO)

| Role | Maker | Checker | Approver | หมายเหตุ |
|---|:--:|:--:|:--:|---|
| HR | ✅ สร้าง/แก้/ยกเลิก/ปิดรอบ · ส่งคำขอสิทธิ์ | ✅ ตรวจ preview ก่อนยืนยัน | — | เจ้าของกระบวนการ |
| หัวหน้าสายงาน | ✅ สร้างรอบออกงานของลูกทีม | ✅ **DOA step 1** | — | ชั้นที่รู้เรื่องจริงที่สุด |
| ผู้จัดการฝ่ายบุคคล | — | — | ✅ **DOA step 2** | ผลทางสัญญาจ้าง |
| ผู้บริหารฝ่ายต้นสังกัด | — | — | ✅ **DOA step 3 — เฉพาะสายไม่สมัครใจ** | เลิกจ้าง · ไม่ผ่านทดลองงาน · ออกทันที |
| ผู้รับผิดชอบงาน (IT · ธุรการ · การเงิน) | ✅ ปิดงานที่ตนถือ | — | — | ผ่าน "งานของฉัน" ของ OP |
| **ผู้ดูแลสิทธิ์ (Roles & Permissions)** | — | ✅ **ลงมือแล้วส่งผลตอบกลับพร้อมหลักฐาน** | **— โดยเจตนา** | **acknowledging counterparty** — ดู `2_BRD §4.3.2` |
| พนักงานเจ้าของรอบ | ✅ ปิดงานของตัวเอง | — | — | ผ่าน OP / ESS (⏳W6) |
| ระบบ | ✅ เปลี่ยนสถานะตามเวลา · ส่งคำขอเพิกถอนเมื่อถึงกำหนด | ✅ ตรวจ `closeBlockers` · ตรวจงวดปิดซ้ำ | — | ทุกการกระทำของระบบบันทึกเป็น `actor = system` |

> ⭐ **การเพิกถอนสิทธิ์ (T-11) ไม่มี Approver โดยเจตนา** — เหตุผลครบ 4 ข้อพร้อมตารางเปรียบเทียบอยู่ที่ `2_BRD §4.3.2` · สรุปสั้น: **ชั้นอนุมัติตรงนั้นจะเปลี่ยนความล่าช้าให้กลายเป็นช่องโหว่ความปลอดภัย** และ control ถูกย้ายไปอยู่ที่ **หลักฐาน (`ack_by`/`ack_at`/`ack_ref`)** แทนการอนุญาตล่วงหน้า

## §0.5 Dependencies

### Upstream (feature นี้ต้องพึ่ง)

| ต้นทาง | สถานะ | ทางเข้า | กติกาที่ต้องทำตาม | ที่อยู่ในแพ็ก |
|---|---|---|---|---|
| **HR Configuration** | ✅ ส่งมอบ 2026-08-28 | `GET /api/v1/hr-config/resolve?date=&company_id=&group=` | **C-1…C-6** · **P-1…P-9** (`F-HR-CONFIG 3_FRD/00_OVERVIEW §0.13.3 · §0.14`) — **ห้ามเขียนกติกาใหม่เอง** | `03_LOGIC ENG-HRCFG-READ` · `05_RULES BR-12` |
| **HR Configuration — คีย์ที่ยังไม่มี** | ⛔ | — | **`employment_term.probation_days` · `notice_days_by_reason` · `notice_days_legal_min` ยังไม่เผยแพร่** → `config_version_ids.employment_term = null` · แสดง "ยังไม่มีค่าให้อ่าน" · **ห้ามเดา** | `05_RULES BR-11` · `07_LOCKED §7.3 OQ-STD-OB3` |
| **Operation Process** | ✅ | ประกาศ SOW + อ่านสถานะงาน + อ่านแม่แบบ CL/SOP/SOW | **ห้ามสร้าง task engine ใหม่** · **OC เกิดที่ OP — ห้ามประกาศที่นี่** | `ENG-OPSOW-01` · `05_RULES BR-02` |
| **Roles & Permissions / User Management** | ✅ | ส่ง "คำขอ" + รับ "ผลตอบกลับ" | **#107** — feature นี้ไม่เขียนข้อมูลสิทธิ์ · **สัญญาผลตอบกลับ = OQ-STD-OB8 (ยังไม่มี)** | `02_API §2.2` · `03_LOGIC §3.0` |
| **DOA Engine** | ✅ | `GET /doa/resolve` · อ่านจำนวนงานอนุมัติค้าง · delegate | **LOCK-DOA** — ห้ามมีสายอนุมัติในโค้ดของ feature · slot เลือก "คน" ในตำแหน่ง | `ENG-DOA-01` · `DOA_BRIEF.md` |
| **Employee Master** | ✅ | ตัวเลือกพนักงาน (#102) · สายบังคับบัญชา · ผู้ใต้บังคับบัญชา | soft reference · เก็บสำเนาชื่อ (LD-4C-02) | `04_DB` snapshot columns |
| **Attendance** | ✅ ส่งมอบ 2026-08-28 | `GET /api/v1/attendance/resolve` | **AT-1…AT-7** · **§0.13.5 ไม่มีทางเข้าสำหรับการเขียนกลับ** · **AT-6 ห้ามคำนวณเอง** | `03_LOGIC FN-D02` |
| **Leave** | ✅ ส่งมอบ 2026-08-29 | `GET /api/v1/leave/resolve` · `GET /api/v1/leave/entitlements/resolve` | **LV-1…LV-7** · **§0.13.6 ไม่มีทางเข้าสำหรับการเขียนกลับ** · **LV-4 ห้ามนับวันเอง · LV-6 ห้ามตีความป้ายจ่ายเป็นเงิน** | `03_LOGIC FN-D03` |
| **ENG-NOTIFY** | ✅ baseline | `ENG-NOTIFY.emit(event_id, {ref, vars})` | ห้ามเลือกช่องทางเอง · **ห้ามประกาศซ้ำ `doa_pending`/`doa_result`** | `NTF_BRIEF.md` · **§0.16.1** |
| **ENG-CSQ 7C** | ✅ baseline | `POST /csq/events` | **ห้ามประกาศ OC · DC ระดับเอกสาร · SC** | `CSQ_BRIEF.md` · **§0.16.2** |
| **Policy Center** | ✅ baseline | runtime | ABAC · masking · audit — ห้าม re-implement | `05_RULES §5.7` |
| **Document Center** | ✅ baseline | runtime | ที่เก็บไฟล์แนบ — feature เก็บเพียงการอ้างอิง | `04_DB T_onb_task.evidence_ref` |
| **Recruit** | ⏳ W5 | — | **Module Linkage** — กรอกเอง + "ยังไม่เชื่อม" | `04_DB candidate_ref` |
| **Asset** | ⏳ ไม่มีในแผง | — | **Module Linkage** — **ห้าม mock หน้าทะเบียน** | `04_DB asset_master_ref` |

### Downstream (feature ที่พึ่ง feature นี้) — **อ่าน §0.13**

| ปลายทาง | สถานะ | อ่านอะไร | ทางเข้า |
|---|---|---|---|
| **Leave** | ✅ | `last_working_day` · `employment_state` — **ปิด `OQ-L11` ที่ Leave ยกไว้เองและชี้มาที่นี่** | `GET /api/v1/onboard/employment-window/resolve` |
| **Attendance** | ✅ | `start_date` · `last_working_day` | เดียวกัน |
| **Payroll** | ⏳ W4 | `start_date` · `last_working_day` (ไม่มีตัวเลขเงินจากที่นี่) | เดียวกัน |
| **Welfare** | ⏳ W4 | สัญญาณ **joiner / leaver** | เดียวกัน (Module Linkage) |
| **Employee Master** | ✅ | สถานะการเป็นพนักงานที่รอบยืนยันแล้ว | soft ref (ไม่ CRUD ข้าม feature) |
| **Operation Process** | ✅ | SOW ของงาน checklist | ประกาศ SOW |
| **Roles & Permissions** | ✅ | คำขอเปิด/เพิกถอน/คืนสิทธิ์ | request + ack |
| **ENG-CSQ · ENG-NOTIFY** | ✅ | event ตาม §0.16 | emit |

### External
**ไม่มีการเชื่อมภายนอกองค์กร**

## §0.6 Stack & Architecture

| ชั้น | รายละเอียด |
|---|---|
| API | REST · base `/api/v1/onboard` · error envelope มาตรฐาน CUBE · **idempotency key ที่ทุก mutation และที่ทุก webhook ผลตอบกลับ** |
| Logic | CUBIC 3 ชั้น — **Feature Function** (scope-local · camelCase) → **Engine** (reusable · kebab-case · pure object in/out) → **ห้าม Engine รู้จัก HTTP** |
| DB | PostgreSQL · prefix **`T_onb_`** · `T_onb_history` เป็น **append-only บังคับที่ระดับฐานข้อมูล** (ปฏิเสธ UPDATE/DELETE) · ไม่มี hard delete ทุกตาราง |
| Integration | ทุกต้นทางเป็น **soft reference** (LD-4C-02) — nullable · ไม่มี FK cascade · เก็บสำเนาชื่อเสมอ · **ไม่มีการจัดการข้อมูลข้ามฝั่ง** |
| UI | ERP shell (sidebar 232/244) · CI Warm Light · **archetype master** · 1 เมนู · 5 เส้นทางย่อย · drawer 920px · modal 440px |
| Background | **2 งาน** — `scanRevocationDue` (ทุก 15 นาที · ส่งคำขอเพิกถอนเมื่อถึงกำหนดและติดธง overdue) · `advanceStartedCases` (รายวัน 00:05 · เปลี่ยนรอบเข้างานเป็น "กำลังดำเนินการ") |
| **Engine candidate ใหม่** ⭐ | **`access-revocation-engine`** — ตรรกะ "คำขอ → ผลตอบกลับ → เกินกำหนด → ยกระดับ" ใช้ซ้ำได้กับ Policy Center และ Asset ในอนาคต · **ยกให้ Architect ที่ `_NOTIFY.md`** |

## §0.7 Multi-Tenant & Security Context

| ประเด็น | การจัดการ |
|---|---|
| Tenant isolation | ทุก query กรองด้วย `tenant_id` ที่ชั้น API · `company_id` ส่งเข้าทุกการอ่านค่าต้นทาง (C-1) |
| สิทธิ์ | จาก Policy Center (ABAC) — หัวหน้าเห็นเฉพาะลูกทีมตามสายบังคับบัญชา · **กรองที่ระดับ query ไม่ใช่ซ่อนปุ่ม** |
| การปิดบัง | ทำที่ **ชั้น API** ไม่ใช่ UI — `termination_reason` · `probation_review_result` · `rehire_*` · **ทะเบียนสิทธิ์ทั้งตาราง** ถูกแทนด้วย `null` เมื่อไม่มีสิทธิ์ |
| ร่องรอย | ทุก mutation **และทุกการเปิดดูข้อมูลอ่อนไหว** ส่งไป Policy Center แบบไม่บล็อกการแสดงผล |
| การเข้ารหัส | `access_ref` · `fail_reason` · `reason` ทุกชนิด · `rehire_note` เข้ารหัสทั้งตอนส่งและตอนเก็บ |
| **จุดรับ webhook** ⭐ | endpoint รับผลตอบกลับจาก Roles & Permissions ต้องยืนยันตัวตนของผู้ส่ง · **ปฏิเสธผลที่ไม่มี `ack_by`/`ack_at`/`ack_ref` ครบ** · idempotent · มี rate limit |

### §0.7.1 Data Classification Summary ⭐

| ระดับ | มีในแพ็กนี้? | ตัวอย่างช่อง | การบังคับ |
|---|:---:|---|---|
| Public | ❌ | — | ไม่มีช่องใดที่เปิดเผยต่อสาธารณะ |
| Internal | ✅ | `case_code` · `start_date` · `last_working_day` · `case_status` · `revoke_state` · `period_code` | สิทธิ์ตามบทบาท |
| **Confidential** | ✅ **ระดับสูงสุดที่ feature นี้แตะ** | `termination_reason` · `is_immediate_exit` · `probation_review_result` · `rehire_eligible`/`rehire_note` · **`access_kind` · `access_ref` · `fail_reason`** · `reject_reason`/`cancel_reason`/`change_reason`/`add_reason` · `evidence_ref` | ปิดบังที่ชั้น API + ร่องรอยการเปิดดู |
| Restricted | ❌ | — | **ไม่มี** — feature นี้ไม่มีตัวเลขเงินเลย (BR-18 · FN-60) |

> **ไม่มีช่องใดตั้งค่าเริ่มต้นเป็น Public** — ตรวจแล้วใน `04_DB §4.2` ทุกตาราง (Phase 3.5 J)

## §0.8 Open Questions

| # | คำถาม | ค่าที่ใช้ไปก่อน | เจ้าภาพ | ยกไป |
|---|---|---|---|---|
| **OQ-FRD-01** ⭐⭐ | **สัญญาผลตอบกลับจาก Roles & Permissions** — schema ของ `ack` · วิธียืนยันตัวตนของผู้ส่ง · เป็น webhook หรือ polling | ออกแบบเป็น **webhook `POST /onboard/access-items/:id/ack`** + polling สำรอง `reconcileAccessAck` · **ปฏิเสธผลที่ไม่มี `ack_by`/`ack_at`/`ack_ref` ครบ** | **Architect / Policy Center** | `07_LOCKED §7.3` · `2_BRD §14.4 W-02` |
| **OQ-FRD-02** ⭐ | **`employment_term.*` ที่ HR Configuration** | `config_version_ids.employment_term = null` · **ไม่คำนวณ** · แสดง "ยังไม่มีค่าให้อ่าน" | **Strike + BA HR Configuration** (OQ-STD-OB3 ← OQ-STD-06) | `07_LOCKED §7.3` |
| OQ-FRD-03 | ขนาดหน้าของ read model เมื่ออ่านทั้งบริษัท | `page_size` เริ่มต้น 500 สูงสุด 1000 · ช่วงวันสูงสุด 62 วัน (ตามแบบเดียวกับ Attendance/Leave) | Tech Lead | `07_LOCKED §7.3` |
| OQ-FRD-04 | ล็อกการแก้รอบควรอยู่ระดับใด | **ล็อกมองในแง่ดีที่ระดับ `case_id`** + `row_version` | Tech Lead | `07_LOCKED §7.3` |
| OQ-FRD-05 | รอบการทำงานของ `scanRevocationDue` | **ทุก 15 นาที** — ละเอียดพอที่จะไม่ปล่อยให้เลยกำหนดนาน แต่ไม่ถี่จนเป็นภาระ | Tech Lead | `07_LOCKED §7.3` |
| OQ-FRD-06 | การยิงซ้ำของ event overdue | **ทุก 4 ชั่วโมงจนกว่าจะครบ** · รอบจริงตั้งที่ ENG-NOTIFY ไม่ใช่ในโค้ด feature | Chin (ENG-NOTIFY) | `NTF_BRIEF OQ-NTF-05` |
| OQ-FRD-07 | ถ้าอ่านสิทธิ์ปัจจุบันจาก Roles & Permissions ไม่ได้ตอนสร้างรอบออกงาน | ทะเบียนตั้งต้นมาจากรอบเข้างานอย่างเดียว + ธง `source_read_failed` | Architect | `07_LOCKED §7.3` (OQ-OB-15) |
| OQ-FRD-08…30 | OQ ที่สืบทอดจาก BRD §15 และใบประกาศทั้งสาม | ตามที่ระบุใน `07_LOCKED §7.3` | Strike / Architect / Chin | `07_LOCKED §7.3` (**30 ข้อ**) |

## §0.9 Glossary

| คำ | ความหมาย |
|---|---|
| **รอบ (case)** | ก้อนงานของการเข้าหรือออกของพนักงานหนึ่งคนหนึ่งครั้ง — `T_onb_case` |
| **ทะเบียนสิทธิ์** | `T_onb_access_item` — รายการสิทธิ์ทั้งหมดของรอบนั้นพร้อมสถานะเปิด/เพิกถอนรายรายการ |
| **ผลตอบกลับ (ack)** | `ack_by` + `ack_at` + `ack_ref` จากเจ้าของระบบต้นทาง — **สิ่งเดียวที่ปิดรายการสิทธิ์ได้** |
| **`revocation_due_at`** | เวลาที่การเพิกถอนมีผล = สิ้นวัน `last_working_day` หรือเวลาที่อนุมัติครบสายเมื่อ `is_immediate_exit` |
| **เพิกถอนค้าง (overdue)** | ธงบนรอบเมื่อเลย `revocation_due_at` แล้วยังมีรายการที่ไม่ใช่ "เพิกถอนแล้ว" — **เหตุการณ์ความปลอดภัย** |
| **คำขอคืนสิทธิ์ (restore)** | คำขอใหม่พร้อม `reversal_of` เมื่อยกเลิกรอบหลังเพิกถอน — **ไม่ใช่การย้อนสถานะ** |
| **SOW** | หน่วยงานย่อยของ Operation Process — งาน checklist ทุกใบเป็น SOW และมี `sow_ref` |
| **Published Employment Window** | read model ที่ §0.13 — `start_date` · `last_working_day` · `employment_state` · joiner/leaver |
| **soft reference** | การอ้างข้อมูลของ feature อื่นแบบ nullable ไม่มี FK cascade + เก็บสำเนาชื่อ (LD-4C-02) |
| **"ยังไม่มีค่าให้อ่าน"** | ข้อความมาตรฐานเมื่อ HR Configuration ยังไม่เผยแพร่คีย์ที่ต้องใช้ — **แทนการเดาตัวเลข** |

## §0.10 Pack Navigation

| อยากรู้อะไร | ไปที่ |
|---|---|
| หน้าจอมีอะไรบ้าง · route จริง | `01_UI §1.1 · §1.2` |
| ตัดสินใจ layout อย่างไร | `01_UI §1.0 Layout Decision Log` |
| endpoint ทั้งหมด | `02_API §2.1 · §2.2` |
| **ปลายทางอ่านอะไรจากที่นี่** | **§0.13** + `02_API §2.3` |
| **กลไกการเพิกถอนทั้งหมด** ⭐ | **`03_LOGIC §3.0`** |
| function/engine มีอะไรบ้าง | `03_LOGIC §3.1 · §3.2` |
| ตาราง คอลัมน์ ชั้นข้อมูล | `04_DB` |
| กฎธุรกิจ · state machine · error | `05_RULES` |
| จะทดสอบอะไรบ้าง | `06_TESTS` |
| อะไรที่ห้ามเปลี่ยน | `07_LOCKED_DECISIONS §7.0` |
| **ทำไมไม่มี `PRINT_SPEC.md`** | **หัวไฟล์นี้** + `5_DECLARATIONS/NOT_NEEDED.md` |

## §0.11 Scope Lock (pointer)

**Scope Lock 11 ข้อ สืบทอดครบจาก `2_BRD §3.4`** → ฉบับ IMMUTABLE อยู่ที่ **`07_LOCKED_DECISIONS §7.0`**
สรุปชื่อ: `LOCK-DOA` · `LOCK-REVOKE` · `LOCK-HR1` · `LOCK-NOWRITE` · `LOCK-AUDIT` · `LOCK-7C` · `LOCK-MONEY` · `LOCK-DOC` · `LOCK-MENU` · `LOCK-LINKAGE` · `LOCK-UI`

> **Drift check ชั้นที่ 2 (FRD):** ตรวจทุกไฟล์ในแพ็กแล้ว — **ไม่มี spec ใดขัด LOCK** (รายละเอียดที่ `INDEX.md` Phase 3.5 L)

## §0.12 Coverage Manifest ⭐ (R13 — กัน requirement หล่น BRD→FRD · **มีคอลัมน์ FN-XX ตาม Lane Mode v2**)

> **กติกา:** ไม่มีแถวใดที่คอลัมน์ "อยู่ที่" ว่าง — ของที่ยังไม่มีที่ลงต้องอยู่ใน §0.8 Open Questions

### §0.12.1 Stories (BRD §7) — 88/88 · **1 Story = 1 FN**

| Story | FN | เรื่อง | อยู่ที่ |
|---|---|---|---|
| ST-01 | **FN-01** | สร้างรอบเข้างานจากทะเบียนพนักงาน | 01_UI §1.2.6 · 03_LOGIC FN-A01 · 06_TESTS AT-01 |
| ST-02 | **FN-02** | preview งานก่อนยืนยัน | 01_UI §1.2.6 · 03_LOGIC FN-A02 · 06_TESTS AT-02 |
| ST-03 | **FN-03** | คำนวณกำหนดเสร็จตัดวันหยุด | 03_LOGIC FN-A03 · ENG-WORKDAY-01 · 05_RULES BR-01 · 06_TESTS AT-03 |
| ST-04 | **FN-04** | งาน pre-boarding เดินได้ | 03_LOGIC FN-A04 · 05_RULES §5.2.1 · 06_TESTS AT-04 |
| ST-05 | **FN-05** | ส่งคำขอเปิดสิทธิ์ | 02_API API-10 · 03_LOGIC FN-C01 · 06_TESTS AT-05 |
| ST-06 | **FN-06** | ปิดรายการเมื่อได้ ack | 02_API API-20 · 03_LOGIC FN-C05 · 05_RULES BR-04 · 06_TESTS AT-06 |
| ST-07 | **FN-07** | รายการเปิดไม่สำเร็จ + ส่งซ้ำ | 03_LOGIC FN-C06 · 05_RULES BR-04 · 06_TESTS AT-07 |
| ST-08 | **FN-08** | เปลี่ยนเป็นกำลังดำเนินการเอง | 03_LOGIC FN-A08 (background) · 05_RULES T-2 · 06_TESTS AT-08 |
| ST-09 | **FN-09** | เผยแพร่วันเริ่มงาน + joiner | §0.13 · 03_LOGIC FN-D01 · 06_TESTS AT-09 |
| ST-10 | **FN-10** | เพิ่ม/ปิดงานรายรอบ | 01_UI §1.2.7 · 03_LOGIC FN-A06 · 05_RULES VR-09 · 06_TESTS AT-10 |
| ST-11 | **FN-11** | คำนวณกำหนดเสร็จใหม่เมื่อแก้วันที่ | 03_LOGIC FN-A07 · 05_RULES BR-22 · 06_TESTS AT-11 |
| ST-12 | **FN-12** | ยกเลิกรอบเข้างาน + ปิดงานค้าง | 03_LOGIC FN-E01 · 05_RULES BR-13 · 06_TESTS AT-12 |
| ST-13 | **FN-13** | คำขอปิดบัญชีทันทีเมื่อยกเลิก | 03_LOGIC FN-E02 · 05_RULES BR-03 · 06_TESTS AT-13 |
| ST-14 | **FN-14** | บันทึกผลทบทวนทดลองงาน | 01_UI §1.2.7 · 03_LOGIC FN-A09 · 06_TESTS AT-14 |
| ST-15 | **FN-15** | ยังไม่มีค่าระยะทดลองงาน | 01_UI §1.3 · 03_LOGIC FN-A10 · 05_RULES BR-11 · 06_TESTS AT-15 · IA-06 |
| ST-16 | **FN-16** | ปิดรอบเข้างาน | 03_LOGIC FN-A11 · 05_RULES BR-15 · 06_TESTS AT-16 |
| ST-17 | **FN-17** | บล็อกปิดรอบพร้อมรายการค้าง | 03_LOGIC FN-A12 closeBlockers · 06_TESTS AT-17 |
| ST-18 | **FN-18** | อ้างผู้สมัครที่ยังไม่เชื่อม | 01_UI §1.2.6 · 04_DB candidate_ref · 06_TESTS AT-18 |
| ST-19 | **FN-19** | สร้างรอบออกงาน | 01_UI §1.2.6 · 03_LOGIC FN-B01 · 06_TESTS AT-19 |
| ST-20 | **FN-20** | กำหนดเสร็จถอยหลังจากวันสุดท้าย | 03_LOGIC FN-B02 · 05_RULES BR-01 · 06_TESTS AT-20 |
| ST-21 | **FN-21** | บล็อกวันที่ในงวดที่ปิด | 03_LOGIC FN-B03 · 05_RULES BR-10 · 06_TESTS AT-21 |
| ST-22 | **FN-22** | ยังไม่มีค่าระยะบอกกล่าว | 01_UI §1.3 · 05_RULES BR-11 · 06_TESTS AT-22 · IA-06 |
| ST-23 | **FN-23** | resolve + freeze สายอนุมัติ | 03_LOGIC ENG-DOA-01 · FN-B04 · 06_TESTS AT-23 · IA-02 |
| ST-24 | **FN-24** | slot เท่าที่ engine คืน · เลือกคน | 01_UI §1.2.8 · 03_LOGIC FN-B05 · 06_TESTS AT-24 |
| ST-25 | **FN-25** | อนุมัติครบสาย → ปลดล็อก checklist | 03_LOGIC FN-B06 · 05_RULES BR-07 · 06_TESTS AT-25 |
| ST-26 | **FN-26** | เผยแพร่วันทำงานวันสุดท้าย + leaver | §0.13 · 03_LOGIC FN-D01 · 06_TESTS AT-26 |
| ST-27 | **FN-27** | ไม่อนุมัติบังคับเหตุผล + re-resolve | 03_LOGIC FN-B07 · 05_RULES VR-07 · 06_TESTS AT-27 |
| ST-28 | **FN-28** | SoD เลื่อนขึ้นชั้นเหนือ | 03_LOGIC ENG-DOA-01 §SoD · 05_RULES BR-09 · 06_TESTS AT-28 · IA-03 |
| ST-29 | **FN-29** | พิสูจน์ว่าไม่มีสายอนุมัติในโค้ด | 07_LOCKED §7.0 LOCK-DOA · 06_TESTS AT-29 · IA-03 |
| ST-30 | **FN-30** | ทะเบียนสิทธิ์ 8 ชนิด | 04_DB §4.3 access_kind · 01_UI §1.2.9 · 06_TESTS AT-30 |
| ST-31 | **FN-31** | ส่งคำขอเพิกถอนทุกรายการ | 03_LOGIC §3.0 FN-C02 · 02_API API-11 · 06_TESTS AT-31 |
| ST-32 | **FN-32** | ความคืบหน้า x/y + สถานะรายบรรทัด | 01_UI §1.2.9 · 03_LOGIC FN-C09 · 06_TESTS AT-32 |
| ST-33 | **FN-33** | ครบทุกรายการ → เพิกถอนสิทธิ์แล้ว | 03_LOGIC FN-C07 · §0.16.2 E2 · 06_TESTS AT-33 · IA-01 |
| ST-34 | **FN-34** | ธง overdue + ปิดรอบไม่ได้ | 03_LOGIC FN-C08 · 05_RULES BR-06 · 06_TESTS AT-34 · IA-04 |
| ST-35 | **FN-35** | แท็บงานที่ต้องจับตา | 01_UI §1.2.3 · 03_LOGIC FN-F03 · 06_TESTS AT-35 |
| ST-36 | **FN-36** | ยกระดับการแจ้งที่ปิดไม่ได้ | 03_LOGIC ENG-REVOKE-01 §severity · §0.16.1 · 06_TESTS AT-36 |
| ST-37 | **FN-37** | ออกทันที → เพิกถอนทันที | 03_LOGIC FN-B08 · 05_RULES BR-05 · 06_TESTS AT-37 · IA-05 |
| ST-38 | **FN-38** | เพิ่มรายการสิทธิ์ที่พบภายหลัง | 02_API API-13 · 03_LOGIC FN-C10 · 05_RULES VR-10 · 06_TESTS AT-38 |
| ST-39 | **FN-39** | พิสูจน์ว่าไม่มี checkbox ปิดรายการ | 07_LOCKED §7.0 LOCK-REVOKE · 06_TESTS AT-39 · IA-01 |
| ST-40 | **FN-40** | ต้นทางไม่ตอบ → ค้าง + นับครั้ง | 03_LOGIC FN-C06 · 05_RULES BR-06 · 06_TESTS AT-40 |
| ST-41 | **FN-41** | คอลัมน์ที่มาของรายการสิทธิ์ | 04_DB access_item.source · 01_UI §1.2.9 · 06_TESTS AT-41 |
| ST-42 | **FN-42** | ส่งมอบ/คืนทรัพย์สิน | 04_DB T_onb_asset_item · 01_UI §1.2.10 · 06_TESTS AT-42 |
| ST-43 | **FN-43** | ทรัพย์สินค้าง → ปิดรอบไม่ได้ (ไม่บล็อกเพิกถอน) | 03_LOGIC FN-A12 · 05_RULES BR-16 · 06_TESTS AT-43 · IA-07 |
| ST-44 | **FN-44** | อ้างทะเบียนทรัพย์สินที่ยังไม่มี | 04_DB asset_master_ref · 06_TESTS AT-44 |
| ST-45 | **FN-45** | งานส่งมอบงานภายในทีม | 03_LOGIC ENG-OPSOW-01 template · 06_TESTS AT-45 |
| ST-46 | **FN-46** | แนบหลักฐานผ่านคลังเอกสาร | 02_API API-16 · 04_DB evidence_ref · 06_TESTS AT-46 |
| ST-47 | **FN-47** | พิสูจน์ว่าไม่มีลายเซ็นอิเล็กทรอนิกส์ | 07_LOCKED §7.0 LOCK-DOC · 06_TESTS AT-47 |
| ST-48 | **FN-48** | ยกเลิกหลังอนุมัติ + ปิดงานค้าง | 03_LOGIC FN-E03 · 05_RULES BR-13 · 06_TESTS AT-48 |
| ST-49 | **FN-49** | ถอนวันทำงานวันสุดท้ายที่เผยแพร่ | 03_LOGIC FN-E04 · §0.13.5 · 06_TESTS AT-49 · IA-08 |
| ST-50 | **FN-50** | คำขอคืนสิทธิ์ใหม่ ไม่ย้อนสถานะ | 03_LOGIC FN-E05 · 05_RULES BR-14 · 06_TESTS AT-50 · IA-09 |
| ST-51 | **FN-51** | ประวัติการเพิกถอนเดิมยังอยู่ | 04_DB T_onb_history · §0.16.2 E5 reversal_of · 06_TESTS AT-51 · IA-09 |
| ST-52 | **FN-52** | พิสูจน์ว่าไม่มีปุ่มลบถาวร | 07_LOCKED §7.0 LOCK-AUDIT · 04_DB §4.6 · 06_TESTS AT-52 · IA-10 |
| ST-53 | **FN-53** | การ์ดขอบเขตวันที่ + เวอร์ชันค่า | §0.13 · 01_UI §1.2.7 · 06_TESTS AT-53 |
| ST-54 | **FN-54** | ระบุผู้อ่านและว่าเป็นสำเนาอ่านอย่างเดียว | 01_UI §1.2.5 · §0.13.5 · 06_TESTS AT-54 |
| ST-55 | **FN-55** | เตือนงานค้างของปลายทาง | 03_LOGIC FN-D02 · FN-D03 · 06_TESTS AT-55 |
| ST-56 | **FN-56** | ลิงก์อ่านอย่างเดียว ไม่บล็อกเพิกถอน | 01_UI §1.2.7 · 05_RULES BR-17 · 06_TESTS AT-56 · IA-07 |
| ST-57 | **FN-57** | สัญญาณ joiner/leaver + สถานะเชื่อม | §0.13 · 02_API API-17 · 06_TESTS AT-57 |
| ST-58 | **FN-58** | พิสูจน์ว่าไม่มีทางเขียนกลับปลายทาง | §0.13.5 · 07_LOCKED LOCK-NOWRITE · 06_TESTS AT-58 · IA-08 |
| ST-59 | **FN-59** | งานเคลียร์รอบจ่ายสุดท้าย | ENG-OPSOW-01 template · 05_RULES BR-26 · 06_TESTS AT-59 |
| ST-60 | **FN-60** | พิสูจน์ว่าไม่มีตัวเลขเงิน | 07_LOCKED LOCK-MONEY · 04_DB §4.2 (ไม่มีคอลัมน์เงิน) · 06_TESTS AT-60 |
| ST-61 | **FN-61** | ลิงก์เปิดงานจริงใน OP | 02_API §2.2 · 04_DB sow_ref NOT NULL · 06_TESTS AT-61 |
| ST-62 | **FN-62** | พิสูจน์ว่าไม่มีปฏิทิน/กระดานงาน | 01_UI §1.4 · 06_TESTS AT-62 |
| ST-63 | **FN-63** | ไฟล์ประกาศไม่มีท่อต้องห้าม | §0.16.3 · CSQ_BRIEF §3 · 06_TESTS AT-63 |
| ST-64 | **FN-64** | แท็บแม่แบบชุดงาน | 01_UI §1.2.4 · 02_API API-18 · 06_TESTS AT-64 |
| ST-65 | **FN-65** | แม่แบบที่ปิดใช้เลือกใหม่ไม่ได้ | 05_RULES BR-30 · 06_TESTS AT-65 |
| ST-66 | **FN-66** | masking ข้อมูลอ่อนไหวทุกช่องทาง | 05_RULES §5.7 · 04_DB §4.6 · 06_TESTS AT-66 |
| ST-67 | **FN-67** | บทบาทมาจาก login | 01_UI §1.0 LD-11 · 06_TESTS AT-67 |
| ST-68 | **FN-68** | ประวัติ append-only ทุกการกระทำ | 04_DB T_onb_history + trigger · 06_TESTS AT-68 · IA-10 |
| ST-69 | **FN-69** | พิสูจน์ว่าไม่มีแบบฟอร์มสัมภาษณ์ลาออก | 01_UI §1.4 · 06_TESTS AT-69 |
| ST-70 | **FN-70** | พิสูจน์ว่าไม่มีหน้าจัดการสิทธิ์ | 01_UI §1.4 · 07_LOCKED LOCK-NOWRITE · 06_TESTS AT-70 |
| ST-71 | **FN-71** | ลิงก์ไปจัดการที่ต้นทาง | 01_UI §1.3 · 06_TESTS AT-71 |
| ST-72 | **FN-72** | ธงสิทธิ์การจ้างกลับ (แสดงผลอย่างเดียว) | 04_DB rehire_* · 05_RULES BR-25 · 06_TESTS AT-72 |
| ST-73 | **FN-73** | พิสูจน์ว่าไม่มี garden leave | 01_UI §1.4 · 06_TESTS AT-73 |
| ST-74 | **FN-74** | พิสูจน์ว่าไม่มีรายงานกวาดบัญชีทั้งระบบ | 01_UI §1.2.3 ขอบเขต · 06_TESTS AT-74 |
| ST-75 | **FN-75** | งานบังคับส่งมอบความเป็นเจ้าของข้อมูล | ENG-OPSOW-01 template · 05_RULES BR-31 · 06_TESTS AT-75 |
| ST-76 | **FN-76** | ไม่เลื่อนเวลาเพิกถอน → สิทธิ์ชั่วคราวแทน | 03_LOGIC FN-C11 · §0.16.2 E7 · 06_TESTS AT-76 · IA-05 |
| ST-77 | **FN-77** | ตรวจผู้ใต้บังคับบัญชา/งานอนุมัติค้าง | 03_LOGIC FN-B09 · 06_TESTS AT-77 |
| ST-78 | **FN-78** | งานบังคับมอบหมาย + ปิดรอบไม่ได้ | 03_LOGIC FN-A12 · 05_RULES BR-32 · 06_TESTS AT-78 |
| ST-79 | **FN-79** | งานแจ้งภาระผูกพัน + แนบหลักฐาน | ENG-OPSOW-01 template · 06_TESTS AT-79 |
| ST-80 | **FN-80** | พิสูจน์ว่าไม่มีการทำเป็นชุด | 01_UI §1.4 · 06_TESTS AT-80 |
| ST-81 | **FN-81** | เลือกได้เฉพาะพนักงานในทะเบียน | 03_LOGIC FN-A01 guard · 06_TESTS AT-81 |
| ST-82 | **FN-82** | พิสูจน์ว่าไม่มีการลบข้อมูลบุคคล | 04_DB §4.6 · 07_LOCKED LOCK-AUDIT · 06_TESTS AT-82 · IA-10 |
| ST-83 | **FN-90** | ค้นหา/กรอง + empty state | 01_UI §1.2.1 · §1.2.2 · 06_TESTS AT-83 |
| ST-84 | **FN-91** | 1 เมนู · แท็บในหน้าเดียว | 01_UI §1.0 LD-01 · 07_LOCKED LOCK-MENU · 06_TESTS AT-84 |
| ST-85 | **FN-92** | validate + กันกดซ้ำ | 05_RULES §5.5 · 02_API §2.0 idempotency · 06_TESTS AT-85 |
| ST-86 | **FN-93** | combobox พนักงานหน้าตาเดียวกัน | 01_UI §1.0 LD-08 · 06_TESTS AT-86 |
| ST-87 | **FN-94** | confirm ทุกการยกเลิก · ไม่ลบ | 05_RULES §5.5 VR-08 · 06_TESTS AT-87 |
| ST-88 | **FN-95** | ไม่มีแบนเนอร์ · ไม่มีหน้าตั้งค่าแจ้งเตือน | 01_UI §1.4 · 06_TESTS AT-88 |

### §0.12.2 Business Rules (BRD §9) — 32/32

| BR | เรื่อง | อยู่ที่ (rule) | ทดสอบที่ |
|---|---|---|---|
| BR-01 | กำหนดเสร็จตัดวันหยุด | `05_RULES §5.1` · `03_LOGIC ENG-WORKDAY-01` | AT-03 · AT-20 |
| BR-02 | ทุกงาน = 1 SOW | `05_RULES §5.1` · `ENG-OPSOW-01` | AT-61 |
| BR-03 | เปิด/ปิดสิทธิ์ = คำขอเท่านั้น | `05_RULES §5.1` · `02_API §2.2` | AT-05 · AT-13 · AT-70 |
| **BR-04** ⭐ | ปิดรายการได้ด้วย ack เท่านั้น | `05_RULES §5.1` · `03_LOGIC §3.0` | AT-06 · AT-39 · **IA-01** |
| **BR-05** ⭐ | เวลาที่การเพิกถอนมีผล | `05_RULES §5.1` · `03_LOGIC FN-B08` | AT-31 · AT-37 · **IA-05** |
| **BR-06** ⭐ | เพิกถอนไม่ครบ = เหตุการณ์ความปลอดภัย | `05_RULES §5.1` · `ENG-REVOKE-01` | AT-34 · AT-36 · AT-40 · **IA-04** |
| BR-07 | checklist ปิดสิทธิ์เดินได้เมื่ออนุมัติครบ | `05_RULES §5.1` | AT-25 |
| BR-08 | resolve + freeze สาย | `05_RULES §5.1` · `ENG-DOA-01` | AT-23 · AT-27 · **IA-02** |
| BR-09 | SoD | `05_RULES §5.1` · `ENG-DOA-01 §SoD` | AT-28 · **IA-03** |
| BR-10 | ห้ามตกในงวดที่ปิด | `05_RULES §5.1` · `FN-B03` | AT-21 |
| **BR-11** ⭐ | พารามิเตอร์กฎหมายจากต้นทางเท่านั้น | `05_RULES §5.1` · `FN-A10` | AT-15 · AT-22 · **IA-06** |
| BR-12 | ส่ง `date` เสมอ + เก็บ `version_id` + ห้าม cache ข้ามวัน | `05_RULES §5.1` · `ENG-HRCFG-READ` | AT-03 · AT-53 |
| BR-13 | ยกเลิกต้องปิดงานค้างชัดแจ้ง | `05_RULES §5.1` · `FN-E01` · `FN-E03` | AT-12 · AT-48 |
| **BR-14** ⭐ | คืนสิทธิ์ = คำขอใหม่ + `reversal_of` | `05_RULES §5.1` · `FN-E05` | AT-50 · AT-51 · **IA-09** |
| BR-15 | เงื่อนไขปิดรอบ | `05_RULES §5.1` · `FN-A12 closeBlockers` | AT-16 · AT-17 · AT-43 |
| BR-16 | ทรัพย์สินค้าง ≠ บล็อกการเพิกถอน | `05_RULES §5.1` | AT-43 · **IA-07** |
| BR-17 | เผยแพร่เป็น snapshot อ่านอย่างเดียว | `05_RULES §5.1` · **§0.13.5** | AT-49 · AT-58 · **IA-08** |
| BR-18 | ไม่มีตัวเลขเงิน | `05_RULES §5.1` · `07_LOCKED LOCK-MONEY` | AT-60 |
| BR-19 | audit append-only | `05_RULES §5.7` · `04_DB trigger` | AT-68 · **IA-10** |
| BR-20 | ไม่มี hard delete | `05_RULES §5.1` · `04_DB §4.6` | AT-52 · AT-82 |
| BR-21 | combobox + snapshot ชื่อ | `05_RULES §5.1` · `04_DB snapshot cols` | AT-86 · AT-81 |
| BR-22 | แก้วันที่ → คำนวณใหม่ | `05_RULES §5.1` · `FN-A07` | AT-11 |
| BR-23 | เพิ่ม/ปิดงานนอกแม่แบบต้องมีเหตุผล | `05_RULES §5.5 VR-09` | AT-10 |
| BR-24 | ทะเบียนสิทธิ์ตั้งต้น | `05_RULES §5.1` · `FN-C03` | AT-41 |
| BR-25 | ธงจ้างกลับ แสดงผลอย่างเดียว | `05_RULES §5.1` | AT-72 |
| BR-26 | งานเคลียร์รอบจ่ายสุดท้าย | `05_RULES §5.1` | AT-59 |
| BR-27 | ไม่มีหน้าตั้งค่าใด ๆ | `05_RULES §5.1` · `01_UI §1.4` | AT-70 · AT-71 |
| BR-28 ⭐ | ไม่ประกาศ OC / DC-เอกสาร / SC | **§0.16.3** · `CSQ_BRIEF §3` | AT-63 |
| BR-29 | แจ้งเตือนผ่าน ENG-NOTIFY เท่านั้น | **§0.16.1** · `NTF_BRIEF` | AT-36 · AT-88 |
| BR-30 | ค่า inactive เลือกใหม่ไม่ได้ | `05_RULES §5.1` | AT-65 |
| **BR-31** ⭐ | ส่งมอบข้อมูลไม่ชะลอการเพิกถอน | `05_RULES §5.1` · `FN-C11` | AT-75 · AT-76 · **IA-05** |
| **BR-32** ⭐ | ผู้ใต้บังคับบัญชา/งานอนุมัติค้างต้องมอบหมายก่อนปิดรอบ | `05_RULES §5.1` · `FN-B09` | AT-77 · AT-78 |

### §0.12.3 Edge Cases (BRD §10) — ☑ ยืนยันแล้ว 18/18 · ☐ AI-suggested 22/22

| กลุ่ม | รหัส | จำนวน | อยู่ที่ | ทดสอบที่ |
|---|---|---:|---|---|
| ☑ จากต้นทาง | EC-01…EC-18 | 18 | `05_RULES §5.4` | `06_TESTS §6.3` AT-89…AT-106 |
| ☐ Concurrent Access | CA-01…CA-05 | 5 | `05_RULES §5.4.2` | AT-107…AT-111 |
| ☐ Data Integrity | DI-01…DI-05 | 5 | `05_RULES §5.4.3` | AT-112…AT-116 |
| ☐ Calculation | CL-01…CL-04 | 4 | `05_RULES §5.4.4` | AT-117…AT-120 |
| ☐ Status/Workflow | ST-E1…ST-E4 | 4 | `05_RULES §5.4.5` | AT-121…AT-124 |
| ☐ Permission | PM-01…PM-04 | 4 | `05_RULES §5.4.6` | AT-125…AT-128 |
| ☐ Cross-feature | EN-01…EN-05 | 5 | `05_RULES §5.4.7` | AT-129…AT-133 |
| **รวม** | | **45** | | |

> **หมายเหตุ:** จำนวน edge ในแมนิเฟสต์ (45) มากกว่าที่ BRD นับไว้ (40) เพราะ BRD นับ CA/DI/CL/ST/PM/EN รวมเป็น 22 แต่รายการจริงมี 27 — **ตรวจแล้วทุกข้อของ BRD §10.2 มีอยู่ครบ ไม่มีข้อหาย** (ส่วนต่างคือข้อที่ FRD แตกละเอียดเพิ่มระหว่าง Phase 2.5 probing)

### §0.12.3b Functions Cut — FN ที่ประกาศว่า "ไม่รองรับ" (24/24 · ต้องอยู่ในแมนิเฟสต์ ไม่ใช่หายเงียบ)

| NS | ไม่รองรับ | FN ที่พิสูจน์ | อยู่ที่ | ทดสอบที่ |
|---|---|---|---|---|
| NS-01 | แบบฟอร์มสัมภาษณ์พนักงานลาออก | FN-69 | `01_UI §1.4` | AT-69 |
| NS-02 | ค่าชดเชย/เงินได้ครั้งสุดท้าย/ตัวเลขเงิน | FN-59 · FN-60 | `07_LOCKED LOCK-MONEY` | AT-60 |
| NS-03 | หน้าจัดการผู้ใช้/role/matrix สิทธิ์ | FN-70 · FN-71 | `01_UI §1.4` | AT-70 · AT-71 |
| **NS-04** ⭐ | **ติ๊กปิดรายการเพิกถอนเอง** | FN-39 | `07_LOCKED LOCK-REVOKE` | AT-39 · **IA-01** |
| NS-05 | ทะเบียนทรัพย์สินกลาง | FN-44 | `04_DB asset_master_ref` | AT-44 |
| NS-06 | ปฏิทิน/Gantt/กระดานงาน | FN-62 | `01_UI §1.4` | AT-62 |
| **NS-07** ⭐ | **ประกาศท่อ OC** | FN-63 | **§0.16.3** | AT-63 |
| NS-08 | DC ระดับเอกสาร · SC | FN-63 | **§0.16.3** | AT-63 |
| **NS-09** ⭐ | **ตั้งค่า/เดาระยะทดลองงาน · บอกกล่าว** | FN-15 · FN-22 | `05_RULES BR-11` | AT-15 · AT-22 · **IA-06** |
| NS-10 | ตรวจว่าบอกกล่าวครบตามกฎหมาย | FN-22 | `05_RULES BR-11` | AT-22 |
| NS-11 | คำนวณวันครบทดลองงานอัตโนมัติ | FN-15 | `03_LOGIC FN-A10` | AT-15 |
| NS-12 | แบบประเมินทดลองงาน · ออกคำสั่ง | FN-14 | `01_UI §1.4` | AT-14 |
| NS-13 | เอกสารเลขที่และไฟล์ PDF | FN-47 | `07_LOCKED LOCK-DOC` · **ไม่มี `PRINT_SPEC.md`** | AT-47 |
| NS-14 | ลายเซ็นอิเล็กทรอนิกส์ | FN-47 | `01_UI §1.4` | AT-47 |
| NS-15 | garden leave | FN-73 | `01_UI §1.4` | AT-73 |
| NS-16 | รายงานกวาดบัญชีตกค้างทั้งระบบ | FN-74 | `01_UI §1.2.3` | AT-74 |
| NS-17 | แก้ข้อมูลปลายทางจากหน้านี้ | FN-58 | **§0.13.5** · `LOCK-NOWRITE` | AT-58 · **IA-08** |
| NS-18 | ลบรอบ/ลบงานถาวร | FN-52 | `04_DB §4.6` | AT-52 · **IA-10** |
| NS-19 | หน้าจอสรรหา/คัดเลือก | FN-18 | `01_UI §1.2.6` | AT-18 |
| NS-20 | ออกงานเป็นชุด | FN-80 | `01_UI §1.4` | AT-80 |
| NS-21 ⭐ | รอบของผู้รับเหมา/บุคคลภายนอก | FN-81 | `03_LOGIC FN-A01 guard` | AT-81 |
| NS-22 | ลบ/ทำให้ข้อมูลบุคคลไม่ระบุตัวตน | FN-82 | `04_DB §4.6` | AT-82 |
| NS-23 | การมอบฉันทะผู้อนุมัติ | FN-78 | `05_RULES BR-32` | AT-78 |
| NS-24 | หน้ารวมงานของพนักงาน | — (ไม่มี route) | `01_UI §1.1` | AT-84 |

### §0.12.4 สรุป Coverage

| หมวด | ต้นทาง | ในแพ็ก | หล่น |
|---|---:|---:|---:|
| Stories (BRD §7) | 88 | **88** | **0** |
| Function Checklist (FN) | 88 | **88** | **0** |
| Business Rules (BRD §9) | 32 | **32** | **0** |
| Validation Rules | 20 | **20** | **0** |
| Edge Cases | 45 | **45** | **0** |
| Functions Cut (ไม่รองรับ) | 24 | **24** | **0** |
| State Transitions | 16 | **16** | **0** |
| Scope Lock | 11 | **11** | **0** |
| Scenario (S-XX) | 61 | **61** | **0** |

> **ไม่มีแถวใดที่ \"อยู่ที่\" ว่าง** ✅ (Phase 3.5 K)

---

## §0.13 ⭐ Published Employment Window — สิ่งที่ feature อื่นอ่านได้จากที่นี่

> **ส่วนนี้เขียนไว้ให้ทีมของ Attendance (✅ W1) · Leave (✅ W2) · Payroll (⏳ W4) · Welfare (⏳ W4) · ESS Portal (⏳ W6) อ้างอิงโดยตรง** — ยกไปวางใน `00_OVERVIEW §Dependencies` ของ feature ตัวเองได้ทันที
> **กติกาเหล็ก:** consumer **อ่าน** ขอบเขตวันที่จากที่นี่ · **ห้ามเขียนกลับทุกกรณี** (feature นี้ไม่มีทางเข้าสำหรับการเขียนของ consumer เลย — §0.13.5) · **ห้ามเก็บวันที่ถาวรในตารางของตัวเองโดยไม่มี `case_ref` + `config_version_ids`** · **ห้ามอนุมานสถานะการเป็นพนักงานเอง** (ใช้ `employment_state` ที่คืนมา) · **ห้ามตีความค่า `null` ว่า "ไม่มีวันสิ้นสุด"** — `null` แปลว่า **"ยังไม่มีรอบออกงานที่อนุมัติแล้ว"** ซึ่งไม่เหมือนกัน

### §0.13.1 อะไรบ้างที่เผยแพร่ (1 มุมมอง · 2 มิติ)

| มิติ | เนื้อหา | ผู้ใช้หลัก | endpoint |
|---|---|---|---|
| **`window`** (ขอบเขตวันที่ของพนักงานหนึ่งคน ณ วันที่หนึ่ง) | **วันเริ่มงานที่มีผลแล้ว** · **วันทำงานวันสุดท้ายที่ผ่านการอนุมัติแล้ว** · สถานะการเป็นพนักงาน · รอบที่เป็นที่มา · ก้อนเวอร์ชันค่าที่ใช้ | **Attendance** (รู้ว่าต้องรอสแกนถึงวันไหน) · **Leave** (กันใบลาคร่อมวันพ้นสภาพ — **ตอบ `OQ-L11`**) · **Payroll** (รู้ว่ารอบจ่ายสุดท้ายคือรอบไหน) | `GET /api/v1/onboard/employment-window/resolve` |
| **`signal`** (สัญญาณผู้เข้าใหม่/ผู้พ้นสภาพ) | `joiner` · `leaver` พร้อมวันที่มีผลและสถานะการเชื่อม | **Welfare** (เริ่ม/สิ้นสุดสิทธิ์สวัสดิการ) | endpoint เดียวกัน (`include=signal`) |

**สิ่งที่ไม่เผยแพร่:** รอบสถานะ `ร่าง` · `รออนุมัติ` · `ไม่อนุมัติ` (ยังไม่มีผลกับใคร) · **`termination_reason` และ `is_immediate_exit`** (Confidential — ไม่อยู่ในทุกมิติ) · **ทะเบียนสิทธิ์ทั้งชุด** (Confidential — เปิดเผยเฉพาะ HR + ผู้ดูแลสิทธิ์ในหน้าจอของ feature นี้) · `probation_review_result` · `rehire_*` · งาน checklist รายใบ (อยู่ที่ Operation Process) · **จำนวนเงินทุกชนิด** (ไม่มีในระบบนี้ — LOCK-MONEY)

### §0.13.2 หน้าทางเข้าเดียว — `GET /api/v1/onboard/employment-window/resolve`

```
GET /api/v1/onboard/employment-window/resolve
    ?as_of=2026-10-31            ← บังคับเสมอ (ไม่ส่ง = 400 ERR_RESOLVE_DATE_REQUIRED)
    &company_id=<uuid>           ← บังคับเมื่อผู้เช่ามีบริษัทลูก
    &employee_id=<uuid>          ← เจาะรายคน (ใช้คู่กับ scope=employee)
    &scope=employee|company      ← default employee · company = อ่านทั้งบริษัทเป็นชุด (OQ-FRD-03)
    &include=signal,case         ← optional (default: ไม่รวม signal และไม่รวมรายละเอียดรอบ)
    &page=1&page_size=500        ← เมื่อ scope=company
```

**สิ่งที่คืนกลับ — โครงที่ consumer ยกไปใช้ได้เลย:**

| field | ชนิด | ความหมาย | Classification |
|---|---|---|---|
| `as_of` | date | วันที่ที่ใช้ตัดสิน (สะท้อน `as_of` ที่ส่งมา) | Internal |
| `employee_id` · `employee_name_snapshot` | uuid · text | คนที่ขอบเขตนี้เป็นของ | **PII** |
| `company_id` | uuid | ขอบเขตบริษัท | Internal |
| **`start_date`** | date \| `null` | **วันเริ่มงานที่มีผลแล้ว** — มีค่าเมื่อรอบเข้างานถึงสถานะ `กำลังดำเนินการ` หรือ `ปิดรอบแล้ว` · **`null` = ยังไม่ถึงวันเริ่มงาน หรือไม่มีรอบเข้างานในระบบ** | Internal |
| **`last_working_day`** ⭐ | date \| `null` | **วันทำงานวันสุดท้ายที่ผ่านการอนุมัติแล้ว** — มีค่าเมื่อรอบออกงานถึงสถานะ `อนุมัติแล้ว` ขึ้นไป · **`null` = ยังไม่มีรอบออกงานที่อนุมัติ หรือรอบถูกยกเลิกไปแล้ว** · **ห้ามตีความว่า "ทำงานตลอดไป"** | Internal |
| **`employment_state`** | enum | `active` (ยังไม่มีรอบออกงานที่อนุมัติ) · `leaving` (อนุมัติแล้วแต่ `as_of ≤ last_working_day`) · `left` (`as_of > last_working_day`) · `not_started` (มีรอบเข้างานแต่ยังไม่ถึงวันเริ่ม) | Internal |
| `case_ref` · `case_type` · `case_status` | text · enum · enum | รอบที่เป็นที่มาของค่า — ให้ปลายทางไล่กลับได้ (เมื่อ `include=case`) | Internal |
| `revocation_state` | enum \| `null` | `none` · `pending` · `done` · **`overdue`** — **สถานะรวมของการเพิกถอน ไม่ใช่รายละเอียดรายรายการ** | Internal |
| **`config_version_ids`** | object | **`{ holiday_calendar: <uuid>, period_rule: <uuid>, employment_term: null }`** — **`employment_term` เป็น `null` เสมอในรอบนี้ เพราะ HR Configuration ยังไม่เผยแพร่คีย์** (OQ-STD-OB3) · **consumer ต้องรับค่า `null` ได้** | Internal |
| `signal` (เมื่อ `include=signal`) | object | `{ joiner: {on, at, link_status}, leaver: {on, at, link_status} }` — `link_status` = `linked` / `not_linked` (Module Linkage) | Internal |
| `source_feature` | const | `F-HR-ONBOARD` | Internal |

**กรณีพิเศษที่ consumer ต้อง handle:**
- **ไม่มีรอบของคนนั้นเลย** → `200` พร้อม `window: null` + `reason: "NO_CASE_FOR_EMPLOYEE"` — **ห้ามตีความว่าคนนั้นไม่ใช่พนักงาน** (อาจเป็นพนักงานเก่าที่มีอยู่ก่อนระบบนี้)
- **`last_working_day = null` ทั้งที่ `employment_state = active`** → ปกติ · แปลว่ายังไม่มีรอบออกงานที่อนุมัติ
- ⭐ **รอบถูกยกเลิกหลังเผยแพร่ไปแล้ว** → `last_working_day` กลับเป็น `null` และ `employment_state` กลับเป็น `active` · **แจ้งผ่าน event `ofb_case_cancelled`** — **consumer ที่เก็บค่าไว้ต้องอ่านใหม่แล้วกลับรายการฝั่งตัวเอง** (ตระกูลเดียวกับ `attendance.day_adjusted` และการถอนใบลาของ Leave)
- **`revocation_state = overdue`** → **เป็นข้อมูลเชิงความปลอดภัย ไม่ใช่เหตุให้ปลายทางเปลี่ยนพฤติกรรม** — ปลายทางยังคงใช้ `last_working_day` ตามปกติ

### §0.13.3 กติกา 6 ข้อที่ consumer ทุกตัวต้องทำตาม (`OB-1…OB-6`)

| # | กติกา | ทำไม |
|---|---|---|
| **OB-1** | **ส่ง `as_of` เสมอ** — วันที่ของเหตุการณ์ทางธุรกิจ (วันที่ลา · วันทำงานที่กำลังยืนยัน · วันจ่ายของงวด) ไม่ใช่ "วันนี้" | สถานะการเป็นพนักงานเปลี่ยนตามวัน — ถามโดยไม่ระบุวันคือคำถามที่ไม่มีคำตอบเดียว (ตระกูลเดียวกับ C-1 · AT-1 · LV-1) |
| **OB-2** | **เก็บ `case_ref` + `config_version_ids` คู่กับเอกสารที่สร้าง** | ตอบข้อพิพาทย้อนหลังได้ · **และเมื่อรอบถูกยกเลิก ปลายทางรู้ว่าเอกสารใบไหนของตัวเองอ้างรอบนั้น** |
| **OB-3** | **ห้าม cache ข้ามวัน** — cache ได้ภายในวันเดียว · ต้องล้างเมื่อได้ event `ofb_case_approved` · `ofb_case_cancelled` · `onb_start_date_changed` | วันสำคัญถูกแก้และถูกถอนได้จนกว่ารอบจะปิด |
| **OB-4** ⭐ | **ห้ามตีความ `null` ว่า "ไม่มีวันสิ้นสุด"** — `null` แปลว่า **"ยังไม่มีรอบออกงานที่อนุมัติแล้ว"** · ใช้ `employment_state` เป็นตัวตัดสินแทน | ตีความผิด = Leave อนุมัติใบลาให้คนที่พ้นสภาพไปแล้ว หรือ Payroll ปิดรอบจ่ายผิด |
| **OB-5** | **ห้ามเขียนกลับทุกกรณี** — feature นี้ **ไม่มี endpoint เขียนสำหรับ consumer เลย** · การแก้วันสำคัญทำที่หน้าจอของ feature นี้เท่านั้น · ใช้ลิงก์ "จัดการที่ เข้าออกงาน" → `#/onboard/<tab>` | **LD-4C-02 · #107** — การเปลี่ยนวันพ้นสภาพต้องผ่านสายอนุมัติพร้อมร่องรอย (BR-08 · BR-17) |
| **OB-6** | **ลงทะเบียนตัวเองใน where-used** — `POST /api/v1/onboard/usage` (หรือแจ้ง BA ให้ตั้งสถานะการเชื่อม) เมื่อ feature พร้อมใช้ | HR ต้องเห็นว่าใครอ่านขอบเขตวันที่อยู่บ้าง ก่อนเปลี่ยนโครง (ตระกูลเดียวกับ C-6 · AT-7 · LV-7) |

### §0.13.4 event ที่ consumer ฟังได้

| event | เมื่อไร | consumer ควรทำอะไร |
|---|---|---|
| `ofb_case_approved` | รอบออกงานอนุมัติครบสาย — **`last_working_day` เริ่มมีผล** | ล้าง cache ของคนนั้น · **Leave: ตรวจใบลาที่คร่อมวันสุดท้าย** · Payroll: ทำเครื่องหมายรอบจ่ายสุดท้าย · Welfare: อ่านสัญญาณ leaver |
| `ofb_case_cancelled` ⭐ | รอบถูกยกเลิก — **`last_working_day` ถูกถอน** | **อ่านค่าใหม่แล้วกลับรายการฝั่งตัวเอง** — event เดิมไม่ถูกลบ ไม่ถูกแก้ |
| `onb_start_date_changed` | วันเริ่มงานถูกเลื่อน | ล้าง cache · ปรับวันที่เริ่มรอสแกน/เริ่มสิทธิ์ |

> **ทั้งสามตัวเป็น event ของ ENG-NOTIFY (ท่อธุรกิจ)** — ประกาศไว้ที่ `5_DECLARATIONS/NTF_BRIEF.md §2` · **ไม่ใช่ event ของ ENG-CSQ**
> **event ของ ENG-CSQ ทั้ง 7 ตัวเป็นท่อ SecC และเป็นเรื่องภายในด้านความปลอดภัย — consumer ทั่วไปไม่ต้องฟัง** (`CSQ_BRIEF.md §2`)

### §0.13.5 ไม่มีทางเข้าสำหรับการเขียนกลับ ⭐

**feature นี้ไม่เปิด endpoint เขียนให้ consumer เลย** — ตระกูลเดียวกับ `F-HR-ATTEND §0.13.5` และ `F-HR-LEAVE §0.13.6`
เหตุผล: **การเปลี่ยนวันพ้นสภาพของคนคือการเปลี่ยนสิ่งที่สายอนุมัติเซ็นไปแล้ว** — ถ้าให้ระบบอื่นเขียนเข้ามาได้ ร่องรอยจะขาดตอนและ `approval_chain` ที่แช่แข็งไว้จะไม่ตรงกับความจริง

- **Leave ต้องการให้ใบลาไม่คร่อมวันพ้นสภาพ** → **อ่าน `last_working_day` แล้วบังคับที่ฝั่งตัวเอง** — ไม่ใช่ให้ Leave เขียนวันเข้ามา (ปิด `OQ-L11` ด้วยวิธีนี้)
- **Attendance ต้องการหยุดรอสแกน** → อ่าน `employment_state` แล้วหยุดที่ฝั่งตัวเอง
- **Payroll ต้องการล็อกรอบจ่ายสุดท้าย** → อ่าน `last_working_day` · **การล็อกงวดจริงเกิดจากการปิดงวดที่ HR Configuration** ไม่ใช่คำสั่งจาก Payroll (P-7)
- **Welfare ต้องการสิ้นสุดสิทธิ์** → อ่านสัญญาณ `leaver`
- **Employee Master ต้องการเปลี่ยนป้ายสถานะพนักงาน** → **soft reference** — ไม่มีการ CRUD ข้าม feature ทั้งสองทิศ

> ข้อยกเว้นเดียวคือ `POST /api/v1/onboard/usage` (OB-6) ซึ่งเป็นการ **ลงทะเบียนว่าใครอ่านอยู่** ไม่ใช่การเขียนข้อมูลของรอบ
> **และ `POST /api/v1/onboard/access-items/:id/ack`** ซึ่ง **ไม่ใช่ endpoint สำหรับ consumer** แต่เป็นทางเข้าของ **Roles & Permissions** ในการส่งผลตอบกลับ — ผู้ส่งต้องยืนยันตัวตนและผลที่ไม่มี `ack_by`/`ack_at`/`ack_ref` ครบจะถูกปฏิเสธ (`02_API API-20`)

---

## §0.14 ⭐ Access Revocation Contract — invariant ที่ห้ามผิด

> **นี่คือ invariant ที่ทำให้ feature นี้มีอยู่** — ทุกคนที่แก้โค้ดของ feature นี้ต้องเข้าใจตรงกัน

| # | ข้อผูกพัน | รูปธรรมในแพ็กนี้ |
|---|---|---|
| **AR-1** ⭐ | **สิทธิ์ทุกชิ้นที่พนักงานถืออยู่ต้องมีแถวของตัวเองในทะเบียน** — ไม่มี "รายการรวม" และไม่มีช่องติ๊กเดียวที่แทนหลายสิทธิ์ | `04_DB T_onb_access_item` 1 แถว = 1 สิทธิ์ · `access_kind` 8 ค่า |
| **AR-2** ⭐ | **แถวปิดได้ทางเดียวคือผลตอบกลับจากเจ้าของระบบ** ที่มี `ack_by` · `ack_at` · `ack_ref` ครบ | `03_LOGIC FN-C05` เป็นทางเดียวที่เขียน `revoke_state = revoked` · **ไม่มี endpoint หรือ UI path อื่น** (IA-01) |
| **AR-3** | **`revocation_due_at` ถูกตั้งตอนอนุมัติครบสาย และไม่มีทางเลื่อน** — งานที่ค้างอยู่ไม่ว่าใบไหนก็เลื่อนไม่ได้ | `FN-B08` เขียนค่าครั้งเดียว · **ไม่มี endpoint แก้ค่านี้** (BR-31 · IA-05) |
| **AR-4** ⭐ | **เลยกำหนดแล้วยังไม่ครบ = เหตุการณ์ความปลอดภัย ไม่ใช่งานค้าง** — ต้องยิง SecC ซ้ำพร้อม severity ที่โต · แจ้งเตือนที่ปิดไม่ได้ · **และปิดรอบไม่ได้** | `ENG-REVOKE-01` + `scanRevocationDue` (ทุก 15 นาที) · `FN-A12 closeBlockers` (IA-04) |
| **AR-5** | **การคืนสิทธิ์คือคำขอใหม่ ไม่ใช่การย้อนสถานะ** — แถวเดิมไม่ถูกลบ ไม่ถูกแก้ · แถวใหม่มี `reversal_of` ชี้แถวเดิม | `FN-E05` · `04_DB reversal_of` · `CSQ E5` (IA-09) |
| **AR-6** | **ประวัติเป็น append-only ที่ระดับฐานข้อมูล** — ไม่ใช่แค่กติกาที่ชั้นแอป | `04_DB §4.6` trigger ปฏิเสธ UPDATE/DELETE (IA-10) |
| **AR-7** | **ไม่มีชั้นอนุมัติคั่นก่อนการเพิกถอน** — ความล่าช้าตรงนี้คือช่องโหว่ | `DOA_BRIEF §2.1` · `2_BRD §4.3.2` · **ไม่มี action ใดใน DOA ที่ผูกกับ T-11** |
| **AR-8** | **การส่งมอบความเป็นเจ้าของข้อมูลไม่ชะลอการเพิกถอน** — ถ้าจำเป็นให้มอบสิทธิ์ชั่วคราวแก่ผู้รับมอบ | `FN-C11` · `BR-31` · `CSQ E7` |
| **AR-9** | **การเพิกถอนไม่รอวันทำการ** — `revocation_due_at` ที่ตกวันหยุดไม่ถูกเลื่อน | `ENG-WORKDAY-01` ไม่ถูกเรียกกับค่านี้ (CL-02) |
| **AR-10** | **ไม่มีการเพิกถอนเป็นชุดข้ามคน** — คำขอทุกใบผูกกับรอบเดียวและรายการเดียว | `02_API API-11` รับ `case_id` เดียว · `idempotency_key` ต่อ (feature, case, access_ref, action) |

---

## §0.15 ⭐ Soft-Reference Read Model (LD-4C-02) — วิธีที่ feature อื่นเชื่อมกับที่นี่

### §0.15.1 ทิศทาง "เข้า" — feature นี้อ้างของคนอื่น

| อ้างอะไร | จากไหน | เก็บอย่างไร | ถ้าต้นทางเปลี่ยน/ถูกปิด |
|---|---|---|---|
| พนักงาน · ผู้รับผิดชอบ · ผู้เซ็น · ผู้รับมอบ | Employee Master | `employee_id` + **snapshot ชื่อ/ตำแหน่ง/แผนก ณ เวลาบันทึก** | พนักงานพ้นสภาพ → ประวัติยังอ่านได้ — **ห้าม join แบบ hard** |
| บริษัท | Organization | `company_id` + snapshot ชื่อ | บริษัทถูกปิดใช้ → รอบเก่ายังอ่านได้ |
| แม่แบบชุดงาน | Operation Process | `template_ref` + snapshot ชื่อ | แม่แบบ inactive → เลือกใหม่ไม่ได้ แต่รอบเก่าแสดงได้ (C-5) |
| งานจริง | Operation Process | `sow_ref` (**NOT NULL**) | งานถูกลบที่ต้นทาง → แถวยังอยู่ + ป้าย "งานต้นทางหาย" · ปิดรอบไม่ได้ (DI-04) |
| สิทธิ์/บทบาท | Roles & Permissions | `access_ref` + `access_label` | ค่าถูกเปลี่ยนที่ต้นทาง → ทะเบียนของรอบยังคงค่าเดิม (เป็นหลักฐาน) |
| ผู้สมัคร | Recruit ⏳ | `candidate_ref` (nullable) | ยังไม่มี → กรอกเอง + "ยังไม่เชื่อม" |
| ทรัพย์สินกลาง | Asset ⏳ | `asset_master_ref` (nullable) | ยังไม่มี → รายการระดับรอบ + "ยังไม่เชื่อม" |
| ค่านโยบาย | HR Configuration | **ไม่เก็บค่า — เก็บเฉพาะ `config_version_ids`** | ค่าเปลี่ยนเวอร์ชัน → รอบเก่ายังอ้างเวอร์ชันเดิม (C-2) |
| ไฟล์แนบ | Document Center | `evidence_ref` | ไฟล์อยู่ที่ Document Center — feature ไม่เก็บไฟล์ |
| สิทธิ์การเข้าถึง | Policy Center | ไม่เก็บ — เรียกตอน runtime | — |

### §0.15.2 ทิศทาง "ออก" — คนอื่นอ้าง feature นี้

| ใครอ้าง | อ้างอะไร | รูปแบบที่ถูกต้อง | รูปแบบที่ **ห้าม** |
|---|---|---|---|
| Attendance · Leave · Payroll · Welfare | ขอบเขตวันที่ ณ วันที่ | `resolve(as_of, company_id, employee_id)` + เก็บ `case_ref` + `config_version_ids` | ❌ คัดลอกวันที่ไปเก็บถาวรโดยไม่มี `case_ref` · ❌ อนุมานสถานะการเป็นพนักงานเอง · ❌ **ตีความ `null` ว่า "ไม่มีวันสิ้นสุด"** |
| ทุก consumer | ลิงก์กลับมาแก้ | ปุ่ม/ลิงก์ "จัดการที่ เข้าออกงาน" → `#/onboard/<tab>` | ❌ เรียก API เขียนของ feature นี้ (**ไม่มีให้เรียก**) |
| Roles & Permissions | ส่งผลตอบกลับ | `POST /onboard/access-items/:id/ack` พร้อม `ack_by`/`ack_at`/`ack_ref` | ❌ ส่งผลที่ไม่มีหลักฐานครบ (จะถูกปฏิเสธ 422) |
| where-used | ลงทะเบียนว่าตัวเองอ่านอยู่ | `POST /onboard/usage` (OB-6) | ❌ ให้ feature นี้ไป query ข้อมูลของ consumer เอง |

### §0.15.3 ทำไมต้อง soft — ไม่ใช่ FK จริง

- ปลายทาง 3 ใน 4 (**Payroll · Welfare · ESS**) **ยังไม่มีอยู่จริง** — FK จริงจะทำให้ deploy feature นี้ไม่ได้จนกว่าจะครบ
- **พนักงานพ้นสภาพต้องยังอ่านประวัติได้ตลอดไป** — FK cascade จะทำลายหลักฐานที่ผู้ตรวจสอบต้องใช้
- **ทะเบียนสิทธิ์เป็นหลักฐาน ณ เวลานั้น** — ถ้า join กลับไปที่ Roles & Permissions แบบ hard ค่าที่เห็นจะเป็นค่าปัจจุบัน ไม่ใช่ค่าที่ถูกเพิกถอนจริง
- แต่ละ feature deploy คนละเวฟ — hard coupling = ปล่อยของไม่ได้

> **สรุปสำหรับคนเขียน FRD ของ feature HR ตัวอื่น:** ยก §0.13.2 (endpoint) + §0.13.3 (กติกา OB-1…OB-6) ไปใส่ใน `00_OVERVIEW §Dependencies` ของ feature ตัวเอง แล้วอ้างกลับมาที่ไฟล์นี้ — **ห้ามเขียนกติกาใหม่เอง**

---

## §0.16 ⭐ Declaration Conformance — event ⊆ brief (Lane Mode v2 gate)

> **กติกา:** FRD **ห้ามประกาศ event ใหม่ที่ไม่มีในใบประกาศ** และ **ห้ามทิ้ง event ที่ใบประกาศระบุไว้** · ทุกแถวต้อง map กลับไปยัง `03_LOGIC` / `05_RULES` ที่มีอยู่จริง

### §0.16.1 ENG-NOTIFY — 9 event (ธุรกิจล้วน)

| # | event_id | trigger ใน FRD | ปิดได้ | อยู่ใน `NTF_BRIEF §2` |
|---|---|---|:--:|:--:|
| 1 | `onb_case_started` | `03_LOGIC FN-A05` (หลัง T-1 สร้าง SOW ครบ) | ✓ | ✅ |
| 2 | `onb_start_date_changed` | `03_LOGIC FN-A07` (หลังคำนวณกำหนดเสร็จใหม่) | ✓ | ✅ |
| 3 | **`access_request_failed`** | `03_LOGIC FN-C06` (ผลตอบกลับ = failed · ทั้งขาเปิดและขาเพิกถอน) | ✗ | ✅ |
| 4 | `case_task_due_soon` | `05_RULES §5.2` (งานใกล้ถึงกำหนด) `[AI-DRAFT · OQ-NTF-02]` | ✓ | ✅ |
| 5 | `case_task_overdue` | `05_RULES §5.2` (งานเลยกำหนด) | ✓ | ✅ |
| 6 | `ofb_case_approved` | `03_LOGIC FN-B06` (T-8 อนุมัติครบสาย) | ✗ | ✅ |
| 7 | **`ofb_access_revoked`** | `03_LOGIC FN-C07` (T-11 ครบทุกรายการ) | ✗ | ✅ |
| 8 | **`ofb_revocation_overdue`** ⭐ | `03_LOGIC ENG-REVOKE-01` + `scanRevocationDue` (ยิงซ้ำตามรอบ) | ✗ **ปิดไม่ได้ทุกกรณี** | ✅ |
| 9 | `ofb_case_cancelled` | `03_LOGIC FN-E03` · `FN-E05` (T-13 · T-14) | ✗ | ✅ |

**ยืนยัน:** ✅ **9 = 9 · ไม่มี event เกิน ไม่มี event ขาด** · ✅ **ไม่มี `doa_pending` / `doa_result` / `doa_escalate`** ในไฟล์ใดของแพ็ก (DOA engine ยิงเอง — BR-29) · ✅ **ไม่มี `sow.*`** (Operation Process ยิงเอง)

### §0.16.2 ENG-CSQ 7C — 7 event (**ท่อ SecC เท่านั้น**)

| # | event_id | ท่อ | trigger ใน FRD | อยู่ใน `CSQ_BRIEF §2` |
|---|---|---|---|:--:|
| E1 | `onboard.access_granted` | **SecC** | `03_LOGIC FN-C05` (ack ขาเปิด · ต่อรายการ) | ✅ |
| E2 | `offboard.access_revoked` | **SecC** | `03_LOGIC FN-C05` (ack ขาเพิกถอน · **ต่อรายการ** + สรุป `is_final` ที่ `FN-C07`) | ✅ |
| E3 | `offboard.revocation_overdue` ⭐ | **SecC** | `ENG-REVOKE-01` (ยิงซ้ำพร้อม `severity` และ `retry_count`) | ✅ |
| E4 | `offboard.immediate_revocation` | **SecC** | `03_LOGIC FN-B08` (T-8 → T-11 ทันที เมื่อ `is_immediate_exit`) | ✅ |
| E5 | `offboard.access_restored` | **SecC** | `03_LOGIC FN-E05` (ack ของคำขอคืนสิทธิ์ · **บังคับ `reversal_of`**) | ✅ |
| E6 | `onboard.access_revoked_on_cancel` | **SecC** | `03_LOGIC FN-E02` (T-4/T-5/T-6 ที่เคยเปิดบัญชี) | ✅ |
| E7 | `offboard.temp_access_delegated` | **SecC** | `03_LOGIC FN-C11` (มอบสิทธิ์ชั่วคราวแก่ผู้รับมอบข้อมูล) | ✅ |

**ยืนยัน:** ✅ **7 = 7** · ✅ **ทุก event เป็นท่อ `secc` ท่อเดียว** · ✅ `idempotency_key` unique ต่อ (`F-HR-ONBOARD`, `case_id`, `access_ref`, action) ที่ `02_API §2.0`

### §0.16.3 ⭐ ทำไม **ไม่ประกาศท่อ OC** — และทำไมนั่นสำคัญเป็นพิเศษกับ feature นี้

**ข้อเท็จจริง:** feature นี้มี checklist จริง และ **งานทุกใบถูกประกาศเป็น SOW ของ Operation Process** (BR-02 · `sow_ref` เป็น `NOT NULL`)

**ผลที่ตามมา:** เมื่อ SOW ถูกสร้าง เดิน และปิด **Operation Process ยิง `sow.*` ของตัวเองอยู่แล้ว** และ **ท่อ OC (Operation Consequence) เกิดขึ้นที่นั่นโดยอัตโนมัติ** — เจ้าของท่อ OC คือ Operation Process เจ้าเดียว (`cube-4.0-current-state.md §3`)

**ดังนั้น:** ถ้า feature นี้ประกาศ `oc` ด้วย จะเกิด **การนับซ้ำ** — งานใบเดียวถูกนับเป็นผลกระทบเชิงปฏิบัติการสองครั้ง ครั้งหนึ่งจาก OP และอีกครั้งจากที่นี่ · และ **register จะปฏิเสธด้วย 422** อยู่แล้ว

> ⚠️ **นี่คือกับดักอันดับหนึ่งของ feature นี้** — ความรู้สึกที่ว่า *"มี checklist = ต้องมี OC"* เป็นความเข้าใจผิดที่เกิดง่ายที่สุด **เพราะ feature นี้มี checklist จริง ๆ ไม่ใช่แค่คล้าย** · ยิ่งมี SOW จริงเท่าไร ยิ่งต้องไม่ประกาศ OC มากเท่านั้น
> **`FN-63` คือ FN ที่พิสูจน์ข้อนี้ด้วยตา** — เปิดไฟล์ประกาศแล้วต้องเห็นว่ามีท่อเดียว
> เหตุผลเดียวกันนี้ใช้กับ **DC ระดับเอกสาร** (DOA engine เป็นเจ้าของ — และ feature นี้มี DOA action จริง 3 ตัว จึง**ยิ่งต้องไม่ประกาศซ้ำ**) และ **SC** (สงวนไว้ · `trigger=false` เสมอ)

### §0.16.4 ท่อที่ไม่ประกาศพร้อมเหตุผล (บันทึกไว้ให้ตรวจได้ · ห้ามเงียบ)

| ท่อ | ประกาศ? | เหตุผล |
|---|:--:|---|
| **OC** | ❌ **ห้าม** | มาจาก Operation Process อัตโนมัติ (§0.16.3) — **422** |
| **DC (ระดับเอกสาร)** | ❌ **ห้าม** | DOA engine เป็นเจ้าของ · feature นี้มี DOA จริง 3 action จึงยิ่งต้องไม่ประกาศ — **422** |
| **SC** | ❌ **ห้าม** | สงวนไว้ · `trigger=false` เสมอ — **422** |
| **DC (terminal decision)** | ⬜ ไม่ประกาศ | การอนุมัติ/ไม่อนุมัติการออกเป็น **การเซ็นอนุมัติ** ไม่ใช่ terminal decision แบบ Continue/Adjust/Hold/Stop/Complete · ผลการทบทวนทดลองงานก็ไม่ใช่ — เป็น **ข้อมูลนำเข้า** ของรอบออกงานหรือของ Employee Movement |
| **EC (Economic)** | ⬜ ไม่ประกาศ | ต้นทุนการเข้า/ออกงานยังไม่มีฐานคิดในระบบ และ scope ตัดเรื่องเงินทั้งหมด (BR-18) · **ประกาศแล้วจะเป็นการใส่ตัวเลขที่คำนวณเอง** |
| **AC (Accounting)** | ⬜ ไม่ประกาศ | ไม่มีรายการทางบัญชีเกิดจาก feature นี้ — ค่าชดเชย/เงินได้ครั้งสุดท้ายเกิดที่ **Payroll (W4)** |
| **FC (Financial)** | ⬜ ไม่ประกาศ | ไม่มีเงินสด/งบเปลี่ยนจากที่นี่ · งบอัตรากำลังอยู่ที่ Manpower Planning (W6) |

### §0.16.5 DOA Conformance

| action | ผูกกับ transition | matrix | ยืนยัน |
|---|---|---|:--:|
| `offboard_approve_voluntary` | **T-7 → T-8** เมื่อเหตุผลอยู่ในกลุ่มสมัครใจ และ `is_immediate_exit = false` | set 1 · **2 ขั้น** (`role-supervisor-direct` → `role-mgr-hr`) | ✅ |
| `offboard_approve_involuntary` | **T-7 → T-8** เมื่อเหตุผลอยู่ในกลุ่มไม่สมัครใจ **หรือ** `is_immediate_exit = true` | set 2 · **3 ขั้น** (+ `role-exec-dept`) | ✅ |
| `offboard_approve_cancellation` | **T-13 · T-14** | **ยืม matrix ของ action เดิมของรอบนั้น** — ไม่มี entry ที่สาม | ✅ |
| **(ไม่มี action)** ⭐ | **T-11 การเพิกถอนสิทธิ์** | **— โดยเจตนา** (AR-7 · `2_BRD §4.3.2`) | ✅ |

**ยืนยัน:** ✅ `approval_scope = policy_approve` (ไม่ใช่ `document_sign` เพราะไม่มีเอกสารและไม่มีลายเซ็น) · ✅ ไม่มีสายอนุมัติในโค้ดของ feature (LOCK-DOA · FN-29) · ✅ จำนวน slot บนหน้าจอ = ที่ engine คืน
