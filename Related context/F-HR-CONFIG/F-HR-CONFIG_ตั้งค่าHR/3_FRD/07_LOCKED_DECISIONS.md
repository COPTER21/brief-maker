# 07_LOCKED_DECISIONS — F-HR-CONFIG · HR Configuration (ตั้งค่าHR)

> **Audience:** ทุก role (PM, BA, FE, BE, QA, DBA, Architect)
> **Purpose:** บันทึกสิ่งที่ถกแล้วจบแล้ว — **ห้ามเปิดอภิปรายซ้ำ**
> **Scope:** FULL variant

---

## §7.0 Scope Lock (Imported from BRD §3.4) ⭐ **IMMUTABLE**

> มติภายใน CUBE ที่ผูกงานนี้ — **ห้าม override ตลอด pack และตลอด chain ปลายน้ำ (HTML / Test / Dev)**
> ถ้า spec ใดใน pack ขัดกับ LOCK → **LOCK ชนะเสมอ**
> Scope Lock Ref: `LANE_BRIEF.md` §LOCK (2026-08-28) · pool_version: POOL.json gen 2026-08-25 (change 2026-08-27 HR re-plan)

| LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะใน FRD |
|---|---|---|---|
| **LOCK-HR-1** | legal/policy parameter ทุกตัวมี `effective_date` เสมอ · ห้าม hardcode · ห้ามเขียนทับ | current-state §3 · CONTEXT_PACK HR | ✅ สอดคล้อง — `00_OVERVIEW §0.14` P-1…P-9 · `04_DB` CHECK constraint · BR-01, BR-02, BR-03 |
| **LOCK-#107** | feature อื่นห้ามสร้างหน้า config เอง — อ้างมาที่นี่ | TASTE_LOG 2026-08-26 (Consent run 3) | ✅ สอดคล้อง — `00_OVERVIEW §0.13` เป็นสัญญากลาง · `05_RULES §5.9 NS-10` |
| **LOCK-LD-4C-02** | soft reference: master = picker assist · nullable · ไม่มี FK cascade · **ห้าม CRUD ของ feature อื่น** | current-state §3 | ✅ สอดคล้อง — `04_DB §4.3` (ไม่มี FK ไป `T_employee`/`T_company`) · `00_OVERVIEW §0.15` · `API-11` ไม่คืนข้อมูลภายในของ consumer |
| **LOCK-DOA-IRON** | ไม่มี hardcoded approval chain | current-state §3 | ✅ **N/A รอบนี้** — ไม่มี approval เลย · ถ้า OQ-01 เคาะกลับ → `GET /doa/resolve` ที่ **FN-06 จุดเดียว** (ระบุไว้ที่ `03_LOGIC §3.2`) |
| **LOCK-AUDIT** | audit append-only · **ไม่มี hard delete** (soft archive/deactivate เท่านั้น) | current-state §3 | ✅ สอดคล้อง — **ไม่มี DELETE endpoint ใน `02_API`** · ไม่มี `deleted_at` ใน `04_DB` · BR-07, BR-14 · ไม่ให้ DELETE grant ที่ DB |
| **LOCK-7C** | ห้ามประกาศท่อ **OC** (จาก OP) · **DC ระดับเอกสาร** (จาก DOA) · **SC** (สงวน) → register 422 | current-state §3 · CONTEXT_PACK | ✅ สอดคล้อง — **SecC เท่านั้น** 6 event · BR-CSQ-01 · `05_RULES §5.1b` |
| **LOCK-MODLINK** | Module Linkage — config เชื่อม/ไม่เชื่อม + manual status override | LANE_BRIEF | ✅ สอดคล้อง — `T_hr_config_usage.link_status` (ready/pending) · `API-11` |
| **LOCK-UI** | #102 combobox anatomy · #103 lean list · #104 1 feature = 1 เมนูซ้าย · #105 demo persona ใน `.demo-strip` · #106 ห้าม hint banner · CI Warm Light | html-generator-v9 iron rules · TASTE_LOG | ✅ สอดคล้อง — `01_UI §1.0` (observed จาก HTML ที่ผ่าน gate) · UX_CHECK 🟢 |

- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3): ไม่มี**
- **HTML–BRD–FRD alignment:** 7 route ตรงกันทั้ง 3 ชั้น · FN 53/53 · S 35/35 · event 6/6 ⊆ CSQ_BRIEF

---

## §7.1 Locked Decisions (LD)

### LD-01: โครงข้อมูล 2 ชั้น (`config_item` + `config_version`) ไม่ใช่ตารางเดียวที่มีคอลัมน์วันที่
- **Date:** 2026-08-28
- **Context:** ต้องรองรับ HR-1 (ทุกค่ามีเวอร์ชัน + วันมีผล + ประวัติ)
- **Options considered:**
  A) ตารางเดียว + คอลัมน์ `effective_date` และเขียนทับเมื่อแก้
  B) **ตารางเดียว + soft-versioning ด้วย `valid_from`/`valid_to` ในแถวเดียวกัน**
  C) **2 ชั้น — `config_item` (identity) + `config_version` (ค่า + วันมีผล) + payload แยกตามกลุ่ม**
- **Decision:** **C**
- **Rationale:** payload ของ 5 กลุ่มค่าต่างกันมาก (ลา / OT / กะ / ปฏิทิน / รอบ / ประเมิน) — ยัดในตารางเดียวจะกลายเป็น EAV หรือ jsonb ที่ query/constraint ไม่ได้ · การแยก item ออกจาก version ทำให้ "ปิดใช้ค่า" (ระดับ item) กับ "เวอร์ชันถูกแทน" (ระดับ version) เป็นคนละเรื่องอย่างชัดเจน
- **Implications:** `04_DB` 16 ตาราง · `version.payload_table` + `payload_id` เป็น polymorphic reference (ไม่ใช่ FK จริง) · `FN-05` ต้อง dispatch ตาม `group`
- **Reversibility:** **HARD** — เปลี่ยนทีหลังต้อง migrate ทั้งโมดูล

### LD-02: สถานะเวอร์ชันใช้ **lazy resolve** เป็นความจริง · scheduler เป็นตัว materialize
- **Date:** 2026-08-28 · **Context:** EA-04 (scheduler ไม่ทำงานตรงวันมีผล) · SLA-01
- **Options:**
  A) scheduler เป็นเจ้าของความจริง — ถ้า job ขาด สถานะจะค้างผิดและปลายทางได้ค่าผิด
  B) **lazy resolve — `ENG-HRCFG-01` ตัดสิน "active ณ วันที่" จาก `effective_date` ทุกครั้งที่อ่าน · scheduler ทำหน้าที่ materialize `status` + ยิง `hrconfig.effective` เท่านั้น**
  C) hybrid ที่ปลายทางคำนวณเอง (ผิด — ละเมิด #107)
- **Decision:** **B**
- **Rationale:** ความถูกต้องของสิทธิ์พนักงาน **ห้ามขึ้นกับว่า cron ทำงานหรือไม่** — ถ้า job ล่ม ค่าที่ปลายทางอ่านต้องยังถูกต้อง
- **Implications:** `ENG-HRCFG-01` กรองด้วยช่วงวันที่ ไม่ใช่ `status='active'` เพียงอย่างเดียว (คอลัมน์ `status` ยังมีไว้เพื่อ UI/index) · scheduler ต้อง catch-up ย้อนตามลำดับวัน · `TC-ST-01` ทดสอบเคส job ขาด
- **Reversibility:** MEDIUM

### LD-03: register `hr-config-resolve` + `hr-period-generator` เข้า CUBIC ที่ **Phase 2** ไม่ใช่ Phase 1
- **Date:** 2026-08-28 · **Context:** consumer ทั้ง 8 ยัง ⏳ — ยังไม่มีใครใช้ engine จริง
- **Options:** A) register ทันที (ช้าลง แต่ได้ contract เร็ว) · B) **scope-local ก่อน register Phase 2 เมื่อ consumer ตัวที่ 2 ยืนยันการใช้งาน**
- **Decision:** **B**
- **Rationale:** หลีกเลี่ยง premature abstraction — แต่ **contract ของ `resolve()` ถูกล็อกไว้แล้วที่ `00_OVERVIEW §0.13.2` ตั้งแต่ Phase 1** ดังนั้น consumer เขียนโค้ดได้เลยโดยไม่ต้องรอ register
- **Implications:** `03_LOGIC §3.2` status = **DRAFT** · Phase 2 ต้อง register + update "Used by features" · **OQ-20**
- **Reversibility:** EASY

### LD-04: **ไม่มี approval ในรอบนี้** — ใช้ effective_date + audit + CSQ SecC เป็น compensating control
- **Date:** 2026-08-28 · **Context:** scope note ตัด "ไม่มี approval" แต่ D365/SAP บังคับ workflow (STANDARD_BASELINE C-18 = MUST)
- **Options:** A) ทำ approval ตามมาตรฐาน ERP (ขัด scope note) · B) **ไม่ทำ + ยกเป็น OQ + ใส่ compensating control 5 ข้อ** · C) ไม่ทำและไม่พูดถึง (**ห้าม** — เป็นการตัดเงียบ)
- **Decision:** **B**
- **Rationale:** scope note เป็นใบสั่ง แต่ MUST ของมาตรฐานห้ามหายเงียบ → บันทึกเป็น **OQ-01 / OQ-STD-01** พร้อมเส้นทางกลับที่ชัดเจน
- **Implications:** `00_OVERVIEW §0.4` (Approver = "—" โดยเจตนา + compensating control) · `05_RULES §5.9 NS-01` · **ถ้าเคาะกลับ → เรียก DOA Engine ที่ `FN-06` จุดเดียว ห้ามสร้าง approval ใหม่**
- **Reversibility:** MEDIUM — เพิ่ม 1 จุดใน `FN-06` + `doa-declaration`

### LD-05: การถอน/ปิดใช้ **ไม่ reverse ผลเดิม** — เป็น event ใหม่ที่ชี้เวอร์ชันเดิม
- **Date:** 2026-08-28 · **Context:** Phase 2.5 PR-8 (Compensation)
- **Options:** A) ส่ง compensating event ที่ "ลบล้าง" ผลเดิมที่ 7C · B) **ส่ง event ใหม่ที่ชี้ `version_id` เดิม โดยไม่แตะผลเดิม**
- **Decision:** **B** (ตาม BR-CSQ-04 ใน CSQ_BRIEF)
- **Rationale:** ผลของ 7C เป็นบันทึกทางประวัติศาสตร์ — การลบล้างย้อนหลังทำลาย audit trail
- **Implications:** `FN-07`, `FN-09` · `02_API §2.X C` · **ไม่มี event `period_reopened`** (การเปิดงวดกลับบันทึกเป็น audit เท่านั้น — ข้อจำกัดที่รู้ตัว · OQ-18)
- **Reversibility:** EASY

### LD-06: บังคับ `date` ใน `resolve()` — **ไม่ default เป็นวันนี้**
- **Date:** 2026-08-28 · **Context:** EA-16 🔺 · สัญญากับ 8 feature
- **Options:** A) ไม่ส่ง = ใช้วันนี้ (สะดวก แต่ซ่อนบั๊ก) · B) **ไม่ส่ง = 400 `ERR_RESOLVE_DATE_REQUIRED`**
- **Decision:** **B** — `[AI-DEFAULT]` (Lane Mode conservative default) → **รอยืนยันที่ OQ-15**
- **Rationale:** ใบลาที่ยื่นย้อนหลังต้องใช้กติกาของ "วันที่ลา" ไม่ใช่ "วันนี้" — การ default เงียบ ๆ จะทำให้ปลายทางคำนวณสิทธิ์ผิดโดยไม่มีใครรู้
- **Implications:** `ENG-HRCFG-01` ขั้นที่ 1 · `API-13` · `XT-09` · **ทุก consumer ต้องแก้โค้ดถ้าเคาะกลับเป็น A**
- **Reversibility:** EASY (แต่ต้องแจ้ง consumer ทั้ง 8)

### LD-07: BR-04 ตรวจ **2 ครั้ง** (validate + commit) ไม่ใช่ครั้งเดียว
- **Date:** 2026-08-28 · **Context:** EA-02 🔺 (ปิดงวดชนกับการบันทึก) · PR-2/PR-9
- **Options:** A) ตรวจตอนเปิดฟอร์ม (เร็ว แต่มีช่องว่าง) · B) **ตรวจซ้ำภายใน transaction ตอน commit + `FOR SHARE` บนแถวงวด**
- **Decision:** **B** — `[AI-DEFAULT]` → **รอยืนยันที่ OQ-13**
- **Rationale:** ช่องว่างระหว่างเปิดฟอร์มกับกดบันทึกอาจนานหลายนาที — งวดถูกปิดระหว่างนั้นได้ · ผลของการพลาด = ยอดที่จ่ายไปแล้วเปลี่ยน (R-04)
- **Implications:** `FN-20` ถูกเรียก 2 ครั้ง · `FN-06`/`FN-10` ต้องทำใน transaction เดียว · `TC-CC-02`
- **Reversibility:** EASY

### LD-08: wizard **3 ขั้น** ไม่ใช่ 5 ขั้น
- **Date:** 2026-08-28 (สืบทอด `[ASSUMED]` จาก S2) · **Context:** Rule #100 ล็อก wizard 5 ขั้น
- **Options:** A) ใช้ 5 ขั้นตาม Rule #100 · B) **ใช้ Rule #47 stepper กลาง (2–5 ขั้น · ขั้นสุดท้าย "ตรวจสอบและยืนยัน")**
- **Decision:** **B** — 3 ขั้น: ข้อมูลค่า › ค่าที่ใช้ › ตรวจสอบและยืนยัน
- **Rationale:** **Rule #100 ใช้กับ Pattern Q (เอกสารธุรกรรม) เท่านั้น** — archetype นี้เป็น master/config ที่ไม่มีเลขที่เอกสาร/ลายเซ็น/PDF → เข้าเกณฑ์ Rule #47
- **Implications:** `01_UI §1.0 P-08` · ยืนยันแล้วโดย UX gate (UX_CHECK 🟢 · Stepper #47/#47.1 ผ่าน)
- **Reversibility:** EASY

---

## §7.2 Convention Deviations

### CD-01: ยังไม่มี deviation จาก `knowledge/conventions.md`
- API path = `/api/v1/hr-config/*` (kebab-case) ✅ · `field_key` = snake_case ✅ · Function = camelCase ✅ · Engine = kebab-case ✅ · Error = UPPER_SNAKE ✅ · Table = `T_snake_case` ✅

### CD-02: ใช้ `POST /versions/:id/publish` แทน `PATCH /versions/:id`
- **Convention default:** PATCH สำหรับการเปลี่ยนสถานะบางส่วน
- **Deviation:** POST custom action
- **Reason:** "publish" เป็น **action ที่มี side effect ข้ามระบบ** (สร้าง effective window · supersede เวอร์ชันเดิม · ยิง event SecC) ไม่ใช่การแก้ property — และ PATCH จะทำให้เข้าใจผิดว่าแก้ทับได้ (ขัด BR-02 เชิงความหมาย)
- **Approved by:** FRD Design Authority (Lane Mode) · **Apply to:** API-06, 07, 08, 09, 10, 14, 15, 16 (action endpoints ทั้งหมด)

### CD-03: มี `T_hr_config_item_company` เป็น join table แทน array column
- **Convention default:** ใช้ array/jsonb สำหรับ multi-select ง่าย ๆ
- **Deviation:** join table แยก
- **Reason:** ต้องเก็บ `company_name_snapshot` ต่อบริษัท (EA-12) และต้อง index เพื่อ `resolve()` ตาม `company_id` ให้เร็ว (hot path)
- **Approved by:** FRD Design Authority

---

## §7.3 Open Questions Promoted to LD

> เมื่อ OQ ใน `00_OVERVIEW §0.8` ถูก resolve → ย้ายมาที่นี่เป็น LD

| OQ | สถานะ | จะกลายเป็น LD เมื่อ |
|---|---|---|
| OQ-13 (re-validate ตอน commit) | ⚠️ รอ — ใช้ `[AI-DEFAULT]` ตาม **LD-07** | Architect ยืนยัน → LD-07 เปลี่ยนจาก `[AI-DEFAULT]` เป็น confirmed |
| OQ-14 (ยกเลิกเวอร์ชันซ้อน) | ⚠️ รอ — ใช้ `FN-19` คำนวณใหม่ทั้งชุด | BA + Architect ยืนยัน → LD ใหม่ |
| OQ-15 (`resolve()` บังคับ `date`) | ⚠️ รอ — ใช้ `[AI-DEFAULT]` ตาม **LD-06** | Architect ยืนยัน → LD-06 confirmed |
| OQ-09 (BR-13 DYNAMIC?) | ⚠️ รอ | Strike + Architect เคาะ → LD ใหม่ + Phase 3 เริ่มได้ |
| OQ-01 (approval) | ⚠️ รอ — **LD-04** ระบุเส้นทางกลับไว้แล้ว | Strike เคาะ |
| OQ-10 (ค่าขั้นต่ำตามกฎหมาย) | ⚠️ รอ — **บล็อก go-live** | ฝ่ายกฎหมาย/HR ยืนยันแหล่งอ้างอิง |
| OQ-18 (E6 SecC?) · OQ-19 (profile_id) | ⚠️ รอ | Architect (7C Engine) เคาะ |
| OQ-11 · OQ-12 (`[AI-DRAFT]` G-02/G-03) | ⚠️ รอ | BA ยืนยันผ่าน wireframe review |

---

## §7.4 Architecture Tradeoffs Acknowledged

### AT-01: `resolve()` เป็น single point of dependency ของทั้งโมดูล HR
- **Tradeoff:** ความสอดคล้อง (ทุก feature ใช้ค่าชุดเดียวกัน · #107) **แลกกับ** blast radius (ล่ม 1 จุด = กระทบ 8 feature)
- **Accepted:** **YES** — เป็นเจตนาของ feature นี้ (ทางเลือกอื่นคือแต่ละ feature เก็บ config เอง ซึ่งเป็นปัญหาที่ทำ feature นี้ขึ้นมาแก้)
- **Mitigation:** partial index บน hot path · read replica เมื่อเกิน 500 req/s · alert P95 > 300 ms (แดงที่ 500 ms) · **client cache ภายในวัน** · Anomaly Report (R-05)

### AT-02: ไม่มี retro — แก้ผลย้อนหลังทำไม่ได้โดยออกแบบ
- **Tradeoff:** ความปลอดภัยของยอดที่จ่ายไปแล้ว **แลกกับ** ความยืดหยุ่นตอนตั้งค่าผิด
- **Accepted:** **YES สำหรับรอบนี้** — ถ้าตั้งผิดต้องแก้ด้วยเวอร์ชันใหม่ที่มีผลข้างหน้า
- **Re-evaluate:** เมื่อ OQ-04 เคาะ → engine candidate `hr-policy-retro-engine` (Phase 4)

### AT-03: polymorphic payload (`payload_table` + `payload_id`) ไม่มี FK จริง
- **Tradeoff:** ความยืดหยุ่นของ 6 กลุ่มค่าที่ schema ต่างกัน **แลกกับ** ไม่มี referential integrity ระดับ DB บน pointer นี้
- **Accepted:** **YES** — ทางเลือกอื่น (EAV / jsonb) ทำให้ validation และ query แย่กว่ามาก
- **Mitigation:** `payload_table` เป็น enum ที่คุมด้วย CHECK · integration test ตรวจว่าไม่มี version ที่ payload หาย · **ไม่มีการลบ payload อยู่แล้ว** (BR-07)

### AT-04: audit เขียนแบบ synchronous (rollback ถ้าล้มเหลว)
- **Tradeoff:** latency ของทุก mutation สูงขึ้น **แลกกับ** การรับประกันว่าไม่มี transition ที่ไม่มี log
- **Accepted:** **YES** — feature นี้เขียนน้อยมาก (20–50 ครั้ง/ปี) แต่ค่าของ audit สูงมาก (หลักฐานทางกฎหมาย · R-02)

---

## §7.5 Decisions Deferred to Implementation

| Item | Owner | Deadline |
|---|---|---|
| เลือก library สำหรับ interval/EXCLUDE constraint และ date arithmetic (Thai calendar display) | Tech Lead | Sprint planning |
| กลยุทธ์ cache ของ `resolve()` ฝั่ง server (in-memory vs Redis · TTL ถึงเที่ยงคืน) | DevOps + Tech Lead | ก่อน load test |
| รูปแบบ `period_code` ที่แสดงผล (พ.ศ. บนจอ vs ค.ศ. ใน DB) | BA + FE | Sprint planning |
| ค่า threshold จริงของ alert (`resolve()` P95 · จำนวนงวดค้าง) | DevOps + PM | ก่อน deploy |
| i18n key naming สำหรับข้อความไทยทั้งหมดใน `06_TESTS §6.10` | FE Lead | ก่อน production |
| วิธี anonymize `*_name_snapshot` เมื่อมี RTBF request | Policy Center owner | ก่อน production |

---

## §7.6 References

- **Convention source:** `frd-generator-v6/knowledge/conventions.md`
- **CUBIC Registry policy:** `frd-generator-v6/references/cubic-schema-templates.md`
- **Edge case origins:** `frd-generator-v6/references/edge-case-probes.md` (PR-1…PR-9)
- **Scope Lock source:** `briefs/W1/F-HR-CONFIG/LANE_BRIEF.md` §LOCK · BRD §3.4
- **Declarations:** `5_DECLARATIONS/CSQ_BRIEF.md` (SecC · 6 event) · `5_DECLARATIONS/NOT_NEEDED.md` (DOA/NTF/DOCCFG/PDFDOC)
- **Related FRDs (อนาคต):** Leave · OT/Shift · Shift & Roster · Attendance · Payroll · Performance · Welfare · Salary Structure — **ทุกตัวต้องอ่าน `00_OVERVIEW §0.13–§0.15` ของไฟล์นี้ก่อนเริ่ม**
