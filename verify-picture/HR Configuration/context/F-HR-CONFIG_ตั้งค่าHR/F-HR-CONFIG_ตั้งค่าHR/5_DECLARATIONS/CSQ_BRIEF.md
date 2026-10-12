# CSQ_BRIEF — F-HR-CONFIG · HR Configuration (ตั้งค่าHR)

> ออกโดย `csq-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-28
> Input: `briefs/W1/F-HR-CONFIG/PREBRIEF.md` §12 (สัญญาณประกาศ · **authoritative**) + §5 state machine + §4 BR + §3 data dict · `LANE_BRIEF.md` (chip) · `DECL.json`
> **DIVERGENCE: —** (chip `csq ✓` = detect §12 = ตาราง CONTEXT_PACK/HR.md → ✓ SecC)
> หมายเหตุ: `references/csq-contract.md` และ `references/brief-template.md` **ไม่มีในเวิร์กสเปซนี้** — ยึด contract จาก SKILL.md (7 ท่อ · ท่อต้องห้าม · kind · naming) + `cube-4.0-current-state.md` §3 แทน · ชื่อท่อ/enum ไม่ได้แต่งใหม่

## §1 Identity

| | |
|---|---|
| profile_id | `CSQ-HRCFG` *(ตัวเลขลำดับจริงให้ Engine กำหนดตอน register)* `[DEFAULT — รอยืนยัน]` |
| feature_code | `F-HR-CONFIG` |
| feature name | HR Configuration · ตั้งค่าHR |
| module | HR |
| กลุ่ม backfill | **B — SecC on sensitive change** (นโยบายกระทบสิทธิ์) |
| archetype | master/config |
| version | 1.0 (2026-08-28) |
| ท่อที่ประกาศ | **SecC เท่านั้น** |

## §2 Declared Events

> trigger point อ้าง **PREBRIEF §5 (state machine)** และ **§4 (BR)** — ณ S1.8 ยังไม่มี FRD
> **ข้อผูกพันถึง S5 (`frd-generator-v6`):** ต้อง map ทุกแถวนี้เป็น `03_LOGIC §x.x` / `05_RULES BR-xx` จริง แล้ว **append ในไฟล์นี้** (ห้ามออกใบใหม่)

| # | event_id | trigger point (PREBRIEF) | ท่อที่ยิง | เงื่อนไข | payload fields |
|---|---|---|---|---|---|
| E1 | `hrconfig.published` | §5 transition `Draft → Scheduled` และ `Draft → Active` (BR-01, BR-03) | **SecC** | ทุกครั้งที่เวอร์ชันใหม่ของค่านโยบายถูกประกาศพร้อมวันมีผล | `config_code` · `group` · `version_id` · `effective_date` · `company_scope` · `companies[]` · `changed_by` · `change_reason` · `value_diff{field, old, new}` |
| E2 | `hrconfig.effective` | §5 transition `Scheduled → Active` (ระบบทำเมื่อถึงวันมีผล) · เวอร์ชันเดิม → `Superseded` | **SecC** | เมื่อค่าเริ่มมีผลจริงกับพนักงาน | `config_code` · `group` · `version_id` · `effective_date` · `superseded_version_id` · `company_scope` · `companies[]` |
| E3 | `hrconfig.cancelled` | §5 transition `Scheduled → Cancelled` (BR-20) | **SecC** | เวอร์ชันที่ประกาศไว้ถูกถอนก่อนมีผล | `config_code` · `version_id` · `effective_date` · `cancel_reason` · `changed_by` |
| E4 | `hrconfig.deactivated` | §5 transition `Active/Scheduled → Inactive` (BR-07, BR-08) | **SecC** | ปิดใช้ค่า (soft archive) — สิทธิ์ที่ผูกกับค่านั้นหยุดถูกเลือกใหม่ | `config_code` · `group` · `deactivate_reason` · `where_used_count` · `changed_by` |
| E5 | `hrconfig.reactivated` | §5 transition `Inactive → Active` | **SecC** | เปิดใช้ค่ากลับ (สร้างเวอร์ชันใหม่พร้อมวันมีผล) | `config_code` · `group` · `version_id` · `effective_date` · `changed_by` |
| E6 | `hrconfig.period_closed` | §3.3ง ตารางงวด · S-31 · BR-21 (ปิดงวดรอบตัดเวลา/รอบจ่าย) | **SecC** `[DEFAULT — รอยืนยัน]` | ปิดงวด = ล็อกไม่ให้แก้ค่าที่กระทบงวดนั้น (ฐานของ BR-04) | `period_code` · `period_from` · `period_to` · `pay_date` · `closed_by` · `closed_at` |

**ทำไมทุก event เป็น SecC:** ค่าที่ feature นี้ถือคือ **นโยบาย/พารามิเตอร์ทางกฎหมายที่กำหนดสิทธิ์ของพนักงาน** (โควตาลา · เงื่อนไขสะสม · อัตรา OT · วันหยุด · รอบจ่าย · รอบประเมิน) การเปลี่ยนค่าเหล่านี้ = **เปลี่ยนสิทธิ์/entitlement** → ตรงนิยาม "เปลี่ยนสิทธิ์-นโยบาย" ของท่อ SecC ใน SKILL.md §Trigger Rule (ตระกูลเดียวกับ Credit Limit · Roles · Data Masking)

## §3 ท่อที่ไม่ประกาศ (และเหตุผล) — ห้ามเงียบ

| ท่อ | ประกาศ? | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ **ห้าม** | มาจาก Operation Process (`sow.*`) อัตโนมัติ — feature นี้ไม่ได้สร้างงาน OP · ประกาศซ้ำ = **register reject 422** |
| **DC** (Decision) ระดับเอกสาร | ❌ **ห้าม** | มาจาก DOA engine · feature นี้ **ไม่มี approval เลย** (scope note ตัด · PREBRIEF S-23 · OQ-STD-01) และไม่มี terminal decision แบบ Continue/Adjust/Hold/Stop/Complete |
| **SC** | ❌ **ห้าม** | สงวนไว้ (OQ-C3 ยังไม่เคาะ) — `trigger=false` เสมอ |
| **EC** (Economic) | ⬜ ไม่ประกาศ | feature นี้เก็บ **อัตรา** (OT 1.5x · โควตาวันลา) ไม่ใช่ธุรกรรมที่เกิดมูลค่า — มูลค่าจริงเกิดตอน OT/Leave/Payroll **ประกาศ EC ที่นี่ = นับซ้ำ** (feature ปลายทางเป็นผู้ประกาศ EC ของตัวเอง ตามตาราง CONTEXT_PACK/HR.md) |
| **AC** (Accounting) | ⬜ ไม่ประกาศ | ไม่มีรายการทางบัญชีเกิดจาก feature นี้ (ตั้งหนี้/ตัดหนี้/ลงบัญชี = Payroll · Accounting) |
| **FC** (Financial) | ⬜ ไม่ประกาศ | ไม่มีเงินสด/งบเปลี่ยนจากการตั้งค่า — งบอัตรากำลังอยู่ที่ Manpower Planning |
| **DC** (terminal decision) | ⬜ ไม่ประกาศ | การแก้ค่า config ไม่ใช่ terminal decision ของกระบวนการ |

## §4 Payload Contract

| field | ชนิด | มาจาก (PREBRIEF) | หมายเหตุ / masking |
|---|---|---|---|
| `config_code` | text | §3.1 รหัสค่า (`code`) | key ธุรกิจ |
| `group` | enum 5 กลุ่ม | §3.1 กลุ่มค่า | ประเภทการลา · อัตรา OT/กะ · ปฏิทินวันหยุด · รอบเวลา/รอบจ่าย · รอบประเมิน |
| `version_id` | id | §3.2 config_version | 1 event = 1 เวอร์ชัน |
| `effective_date` | date | §3.2 (**HR-1**) | บังคับทุก event ที่มีเวอร์ชัน |
| `superseded_version_id` | id (nullable) | §3.2 สถานะ Superseded | เฉพาะ E2 |
| `company_scope` / `companies[]` | enum / list (soft ref) | §3.1 | ขอบเขตที่ได้รับผล (BR-13) |
| `changed_by` / `closed_by` | employee ref | §3.1 (combobox Employee Master #102) | ส่ง **employee_id เท่านั้น** — ห้ามส่งชื่อ/ข้อมูลบุคคลดิบ (BR-CSQ-03) |
| `change_reason` / `cancel_reason` / `deactivate_reason` | text | §3.2 เหตุผลการเปลี่ยน | บังคับตั้งแต่เวอร์ชันที่ 2 |
| `value_diff{field, old, new}` | list | §3.3 payload ต่อกลุ่ม | ส่งเฉพาะ field ที่เปลี่ยน · เป็นค่าตัวเลข/enum ของนโยบาย (ไม่ใช่ข้อมูลบุคคล) |
| `where_used_count` | number | §3.4 computed | เฉพาะ E4 — บอกขนาดผลกระทบ |
| `period_code` · `period_from` · `period_to` · `pay_date` · `closed_at` | text/date | §3.3ง ตารางงวด (S-31) | เฉพาะ E6 |

- **ชั้นข้อมูล:** ค่า config = **INTERNAL** (ไม่มีข้อมูลรายบุคคล) → ไม่ต้อง mask ยกเว้น field คน (`changed_by`/`closed_by` ส่งเป็น id)
- **idempotency_key** = `F-HR-CONFIG:{version_id|period_code}:{event_id}` — unique ต่อ (feature, ref, action) ตาม BR-CSQ-02
- **reversal:** การถอนเวอร์ชัน (E3) และการปิดใช้ (E4) **ไม่ลบ/ไม่แก้ผลเดิม** — เป็น event ใหม่ที่ชี้ `version_id` เดิม (BR-CSQ-04)

## §5 Register Checklist (ก่อน deploy)

- [ ] `POST /csq/profiles/register` ด้วยไฟล์นี้ → แถวใน Profile Registry ของ 7C Engine ขึ้นสถานะ `pending` → `connected`
- [ ] ตรวจว่า **ไม่มี** `oc` / `dc` (เอกสาร) / `sc` ในใบนี้ (ถ้ามี = reject 422)
- [ ] dev wire `emit` ที่ 6 transition จริงตาม §2 พร้อม `idempotency_key`
- [ ] **ห้าม** สร้าง column ผลรายท่อใน table ของ feature (`is_secc_triggered` ฯลฯ) — ผลอยู่ที่ `T_csq_stamp`
- [ ] **ห้าม** คำนวณมูลค่าใด ๆ ในหน้า HR Configuration — Engine (ENG-CSQ-02) เป็นเจ้าของการตีมูลค่า
- [ ] HTML (S2): มีคอมเมนต์ `// TODO: ENG-CSQ emit — ดู CSQ_BRIEF.md` ที่จุด publish / effective / cancel / deactivate / reactivate / period-close · **ห้ามวาดการ์ดผล 7 ท่อในหน้านี้**
- [ ] FRD (S5): §05_RULES มีหัวข้อ "ผลกระทบ 7C (CSQ)" + BR-CSQ-01..05 · §02_API มี producer contract ของ 6 event นี้ · เติม trigger point เป็น `03_LOGIC §x.x` แล้ว append กลับไฟล์นี้

## §6 Open Questions

| # | ประเด็น | ค่าที่ใช้ไปก่อน | เจ้าภาพ |
|---|---|---|---|
| OQ-CSQ-01 | `hrconfig.period_closed` (E6) ควรเป็น SecC หรือไม่ประกาศเลย (เป็น operational lock) | ประกาศ SecC `[DEFAULT — รอยืนยัน]` | Architect / Strike |
| OQ-CSQ-02 | profile_id จริงในทะเบียน (`CSQ-XX`) | `CSQ-HRCFG` `[DEFAULT — รอยืนยัน]` | Architect (7C Engine) |
| OQ-STD-01 | ถ้าเคาะว่าต้องมี approval ตอนแก้นโยบาย → DOA จะยิง DC ระดับเอกสารให้เอง · **ห้าม**เพิ่ม `dc` ในใบนี้ | ไม่มี approval | Strike |
| OQ-STD-05 | ถ้าเคาะว่าต้องแจ้งพนักงานจาก feature นี้ → ออก `NTF_BRIEF` แยก · ไม่กระทบใบ CSQ นี้ | ปลายทางแจ้ง | Chin (ENG-NOTIFY) |

## Quality Gate (self-check)

| # | เช็ค | ผล |
|---|---|---|
| G1 | ไม่มี event ประกาศท่อ `oc` | ✅ |
| G2 | ไม่มี `dc` จากการอนุมัติ | ✅ (feature ไม่มี approval เลย) |
| G3 | ไม่มี `sc` | ✅ |
| G4 | ทุก event มี trigger point อ้างได้จริง | ✅ อ้าง PREBRIEF §5/§4/§3.3 (FRD § ยังไม่มีที่ S1.8 — ผูกพันเติมที่ S5) |
| G5 | ทุก payload field มีจริงใน data dict | ✅ อ้าง §3.1/§3.2/§3.3/§3.4 ครบทุก field |
| G6 | event ที่ยิง EC ระบุ `kind` | N/A — **ไม่ประกาศ EC** (§3) |
| G7 | EC จากเวลา/แรงงานที่ไม่มี Rate Card ใช้ `basis: declared` | N/A — ไม่ประกาศ EC · **ไม่มีตัวเลขเงินในใบนี้** |
| G8 | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` | ✅ (profile_id · E6) |
| G9 | `event_id` ไม่ชนความหมายกับ catalog เดิม | ✅ ใช้ prefix `hrconfig.` + verb ที่จบแล้ว (published/effective/cancelled/deactivated/reactivated/period_closed) |

**Verdict: PASS — พร้อมส่ง**

---

## §7 Trigger Point ยืนยันจาก FRD (append ที่ S5 · 2026-08-28 — ตามข้อผูกพันใน §2 และ §5 checklist)

> เติมโดย `frd-generator-v6` (Lane Mode v2 · S5) — **ไม่ออกใบใหม่ · ไม่แก้ §1–§6**
> FRD pack: `3_FRD/` (FULL variant · 9 ไฟล์) · event ใน FRD = **6 ตัว ⊆ ตาราง §2 เป๊ะ ไม่มีเกิน**

| # | event_id | trigger point จริงใน FRD | API | BR ที่ผูก | payload สร้างที่ |
|---|---|---|---|---|---|
| E1 | `hrconfig.published` | `03_LOGIC.md §3.1 F-HR-CONFIG-FN-06 publishVersion` (Draft→Scheduled และ Draft→Active) | `02_API.md F-HR-CONFIG-API-06` | `05_RULES.md` BR-01, BR-03 | `FN-16 emitCsqEvent` |
| E2 | `hrconfig.effective` | `03_LOGIC.md §3.1 FN-06` โหมด scheduler / lazy-resolve (Scheduled→Active · เวอร์ชันเดิม→Superseded) | (scheduler job · หรือ API-06 เมื่อ eff = วันนี้) | BR-02, BR-19 | `FN-16` |
| E3 | `hrconfig.cancelled` | `03_LOGIC.md §3.1 FN-07 cancelScheduledVersion` | `F-HR-CONFIG-API-07` | BR-20 | `FN-16` |
| E4 | `hrconfig.deactivated` | `03_LOGIC.md §3.1 FN-09 deactivateConfigItem` | `F-HR-CONFIG-API-09` | BR-07, BR-08 | `FN-16` |
| E5 | `hrconfig.reactivated` | `03_LOGIC.md §3.1 FN-10 reactivateConfigItem` | `F-HR-CONFIG-API-10` | BR-04 | `FN-16` |
| E6 | `hrconfig.period_closed` | `03_LOGIC.md §3.1 FN-14 closePayPeriod` | `F-HR-CONFIG-API-15` | BR-21 | `FN-16` |

**สิ่งที่ FRD ทำตาม §5 Register Checklist:**
- ✅ `05_RULES.md §5.1b` มีหัวข้อ **"ผลกระทบ 7C (CSQ)"** พร้อม **BR-CSQ-01…BR-CSQ-05** ครบ
- ✅ `02_API.md §2.X Cross-Module Contract ส่วน B` = producer contract ของ 6 event นี้ (trigger + payload + สิ่งที่ consumer ควรทำ)
- ✅ `03_LOGIC.md §3.1 FN-16 emitCsqEvent` = **จุดเดียว**ที่ feature ยิง event · whitelist ท่อ = SecC เท่านั้น
- ✅ `04_DB.md §4.1` ระบุชัดว่า **ห้ามสร้างคอลัมน์ผลรายท่อ** (`is_secc_triggered` ฯลฯ) — ผลอยู่ที่ `T_csq_stamp`
- ✅ `idempotency_key = F-HR-CONFIG:{version_id|period_code}:{event_id}` สอดคล้องกับ `Idempotency-Key` ของ API (`02_API §2.3`)
- ✅ `changed_by` / `closed_by` ส่ง **`employee_id` เท่านั้น** (BR-CSQ-03 · D7) — `04_DB §4.6.4`
- ✅ **ไม่มี event `period_reopened`** — การเปิดงวดกลับบันทึกเป็น audit เท่านั้น (`03_LOGIC FN-15`) · ผลกระทบกับปลายทางระบุไว้ที่ `02_API §2.X C` และยกเป็น **OQ-18**
- ⚠️ `[DEFAULT — รอยืนยัน]` ที่ยังค้าง: **E6 เป็น SecC หรือไม่ประกาศ (OQ-CSQ-01 → FRD OQ-18)** · **`profile_id` จริง (OQ-CSQ-02 → FRD OQ-19)**
