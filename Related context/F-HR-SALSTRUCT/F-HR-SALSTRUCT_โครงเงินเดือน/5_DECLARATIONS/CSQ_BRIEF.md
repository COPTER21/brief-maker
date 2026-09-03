# CSQ_BRIEF — F-HR-SALSTRUCT · Salary Structure (โครงเงินเดือน)

> ออกโดย `csq-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-28
> Input: `briefs/W1/F-HR-SALSTRUCT/PREBRIEF.md` **§12 (สัญญาณประกาศ · authoritative)** + §5 state machine (3 ชุด) + §4 BR-01…BR-24 + §3 data dict · `LANE_BRIEF.md` (chip) · `_lane/DECL.json`
> **DIVERGENCE: —** (chip `csq ✓` = detect §12 = ตาราง `CONTEXT_PACK/HR.md` `✓ EC/SecC` = `FEATURE_LIST_ALL.md` `csq` → ตรงกันทั้ง 4 แหล่ง)
> หมายเหตุ: `references/csq-contract.md` และ `references/brief-template.md` **ไม่มีในเวิร์กสเปซนี้** — ยึด contract จาก SKILL.md (7 ท่อ · ท่อต้องห้าม · trigger rule · kind · naming) + `cube-4.0-current-state.md` §3 + แพทเทิร์นที่ใช้จริงใน `F-HR-CONFIG/5_DECLARATIONS/CSQ_BRIEF.md` · **ชื่อท่อ/enum ไม่ได้แต่งใหม่**

## §1 Identity

| | |
|---|---|
| profile_id | `CSQ-SALSTRUCT` *(ลำดับจริงให้ Engine กำหนดตอน register)* `[DEFAULT — รอยืนยัน]` |
| feature_code | `F-HR-SALSTRUCT` |
| feature name | Salary Structure · โครงเงินเดือน |
| module | HR |
| กลุ่ม backfill | **A + B** — A (EC เมื่อภาระค่าจ้างคงที่เปลี่ยน) · B (SecC on sensitive change — ค่าจ้างรายบุคคล RESTRICTED + เปลี่ยนกระบอก = เปลี่ยน entitlement) |
| archetype | master/config (`archetype_confirmed` ใน PREBRIEF) |
| Data Classification | **RESTRICTED** (ค่าจ้างรายบุคคล) — ดู §4 masking |
| version | 1.0 (2026-08-28) |
| ท่อที่ประกาศ | **EC · SecC เท่านั้น** |

## §2 Declared Events

> trigger point อ้าง **PREBRIEF §5 (state machine)** และ **§4 (BR)** — ณ S1.8 ยังไม่มี FRD
> **ข้อผูกพันถึง S5 (`frd-generator-v6`):** ต้อง map ทุกแถวนี้เป็น `03_LOGIC §x.x` / `05_RULES BR-xx` จริง แล้ว **append ในไฟล์นี้** (ห้ามออกใบใหม่) · payload ทุก field ต้องชี้ column จริงใน `04_DB` (G5)

| # | event_id | trigger point (PREBRIEF) | ท่อที่ยิง | kind / basis | เงื่อนไข | payload fields |
|---|---|---|---|---|---|---|
| **E1** | `salstruct.published` | §5.1 `ร่าง → รอมีผล` (S-01, S-03 · BR-02, BR-03) | **SecC** | — | ทุกครั้งที่เวอร์ชันใหม่ของโครง/กระบอกถูกประกาศพร้อมวันมีผล | `structure_code` · `version_id` · `effective_date` · `company_scope` · `companies[]` · `changed_by` · `change_reason` · `value_diff[{grade_code, field, old, new}]` |
| **E2** | `salstruct.effective` | §5.1 `รอมีผล → ใช้งาน` (S-02 · ระบบทำเมื่อถึงวันมีผล) · เวอร์ชันเดิม → `ถูกแทนที่` | **SecC** | — | โครงเริ่มมีผลจริง — **ยังไม่ยิง EC ที่ระดับโครง** (ดู §3 เหตุผลกันนับซ้ำ) | `structure_code` · `version_id` · `effective_date` · `superseded_version_id` · `company_scope` · `companies[]` |
| **E3** | `salstruct.cancelled` | §5.1 `รอมีผล → ถอนแล้ว` (S-07) | **SecC** | — | เวอร์ชันที่ประกาศไว้ถูกถอนก่อนมีผล | `structure_code` · `version_id` · `effective_date` · `cancel_reason` · `changed_by` |
| **E4** | `salstruct.deactivated` | §5.1 `ใช้งาน → ปิดใช้` (S-08, S-12 · BR-05, BR-22) | **SecC** | — | ปิดใช้ระดับหรือองค์ประกอบค่าจ้าง (soft archive) — ผู้ที่อ้างอยู่หยุดถูกเลือกใหม่ | `structure_code` หรือ `component_code` · `deactivate_reason` · `where_used_count` · `changed_by` |
| **E5** | `salcomp.assigned` | §5.2 `รอมีผล → ปัจจุบัน` (S-13, S-19, S-29 · BR-10, BR-11, BR-24) | **SecC + EC** | `estimated` / `declared` | อัตราค่าจ้างของพนักงานเริ่มมีผล (รวมกรณีรับจาก Employee Movement) | `employee_id` · `grade_code` · `base_amount` 🔒 · `fte` · `currency` · `effective_date` · `superseded_record_id` · `change_reason_code` · `movement_doc_no` · `out_of_range_flag` |
| **E6** | `salcomp.cancelled` | §5.2 `รอมีผล → ถอนแล้ว` (S-20) | **SecC** | — | ถอนอัตราที่ยังไม่มีผล (คำสั่งถูกยกเลิก) — **ไม่ใช่ reversal ของ E5** เพราะ E5 ยังไม่เคยยิง | `employee_id` · `record_id` · `effective_date` · `cancel_reason` · `movement_doc_no` |
| **E7** | `salcomp.ended` | §5.2 `ปัจจุบัน → สิ้นสุด` (S-21) | **EC** | `avoided` / `declared` | พนักงานพ้นสภาพ → ภาระค่าจ้างคงที่ของคนนั้นหยุด ณ วันสุดท้าย | `employee_id` · `record_id` · `base_amount` 🔒 · `fte` · `effective_to` · `end_reason` |
| **E8** | `salrecur.started` | §5.3 `รอมีผล → ใช้งาน` (S-23, S-24 · BR-14, BR-15) | **SecC + EC** | `estimated` / `declared` | เงินได้/เงินหักประจำคงที่ของพนักงานเริ่มมีผล | `employee_id` · `component_code` · `direction` · `amount` 🔒 หรือ `percent` · `effective_from` · `effective_to` · `goal_amount` 🔒 |
| **E9** | `salrecur.ended` | §5.3 `ใช้งาน → สิ้นสุด` (S-25 · BR-14) | **EC** | `avoided` / `declared` | รายการประจำสิ้นสุด (ครบยอดเป้าหมาย หรือถึงวันสิ้นสุด) | `employee_id` · `component_code` · `item_id` · `amount` 🔒 · `end_trigger` {ครบเป้า, ถึงวันสิ้นสุด, ถอน} |
| **E10** | `salcomp.viewed_restricted` | §7 + §4 **BR-16** (S-28 · การเปิดดูตัวเลขค่าจ้างรายบุคคล) | **SecC** `[DEFAULT — รอยืนยัน]` | — | ผู้ใช้ที่มีสิทธิ์เปิดดูตัวเลขค่าจ้างที่ปกติถูกปิดบัง — ตรงนิยาม "เปิดดูข้อมูลที่ปกปิด" ใน Trigger Rule | `viewer_employee_id` · `subject_employee_id` · `viewed_at` · `view_scope` {รายคน, รายการ, export} · **ไม่ส่งจำนวนเงิน** |

**ทำไม EC:** เงินเดือนฐาน + เงินได้/เงินหักประจำ = **ภาระต้นทุนค่าจ้างคงที่ผูกพันต่องวด** ขององค์กร — การเริ่ม/หยุดของมันคือการเปลี่ยนมูลค่าที่ผูกพันจริง (D365 ผูก compensation กับ budget · SAP ผูก Total Target Cash) → `kind = estimated` ตอนเริ่ม · `avoided` ตอนหยุด
**ทำไม SecC:** (1) อัตราค่าจ้างรายบุคคล = **RESTRICTED** — การเปลี่ยน/เปิดดู = การแตะข้อมูลอ่อนไหว (2) กระบอกและระดับ = **นโยบายที่กำหนดสิทธิ์ของพนักงาน** — เปลี่ยน = เปลี่ยน entitlement (ตระกูลเดียวกับ Credit Limit · Roles · HR Configuration)
**`basis: declared` ทุก EC (G7):** feature นี้ **ส่งค่าที่มีอยู่ในฟิลด์เท่านั้น ไม่คำนวณมูลค่าใด ๆ** — ไม่มีการแปลงเป็นรายปี ไม่รวมยอด ไม่คิดภาษี (BR-13) · **ENG-CSQ-02 เป็นเจ้าของการตีมูลค่า**

## §3 ท่อที่ไม่ประกาศ (และเหตุผล) — ห้ามเงียบ

| ท่อ | ประกาศ? | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ **ห้าม** | มาจาก Operation Process (`sow.*`) อัตโนมัติ — feature นี้ไม่สร้างงาน OP · ประกาศซ้ำ = **register reject 422** |
| **DC** (Decision) ระดับเอกสาร | ❌ **ห้าม** | มาจาก DOA engine · feature นี้ **ไม่มี approval เลย** (scope note ตัด · PREBRIEF S-36 · BR-21 · FN-47 · OQ-STD-01) |
| **SC** | ❌ **ห้าม** | สงวนไว้ (`trigger=false` เสมอ · OQ-C3 ยังไม่เคาะ) |
| **DC** (terminal decision) | ⬜ ไม่ประกาศ | การแก้ master ค่าจ้างไม่ใช่ terminal decision ของกระบวนการ (ไม่มี Continue/Adjust/Hold/Stop/Complete) — การตัดสินใจ "ปรับหรือไม่ปรับ" เกิดที่ **Employee Movement** |
| **AC** (Accounting) | ⬜ ไม่ประกาศ | ไม่มีรายการทางบัญชีเกิดที่นี่ — การตั้งหนี้/ลงบัญชีค่าจ้างเกิดตอน **Payroll** ปิดงวด (Payroll ประกาศ AC ของตัวเองตามตาราง CONTEXT_PACK/HR.md) |
| **FC** (Financial) | ⬜ ไม่ประกาศ | ไม่มีเงินสดจ่ายจริง/งบผูกพันที่นี่ — **งบอัตรากำลังเป็นของ Manpower Planning** (ประกาศ `EC · FC` เอง) · ประกาศที่นี่ = นับซ้ำกับงบ |
| **EC ที่ระดับโครง (E2)** | ⬜ ไม่ประกาศ EC | **กันนับซ้ำ** — โครง/กระบอกคือ "ช่วงที่อนุญาต" ไม่ใช่ภาระที่ผูกพัน · ภาระจริงเกิดตอนผูกอัตราให้คน (E5/E8) · ถ้ายิง EC ทั้งสองระดับ = นับต้นทุนซ้ำสองรอบ |

## §4 Payload Contract

| field | ชนิด | มาจาก (PREBRIEF) | หมายเหตุ / masking |
|---|---|---|---|
| `structure_code` / `grade_code` | text | §3.1 | key ธุรกิจของระดับ/ชุดโครง |
| `component_code` | text | §3.2 | รหัสองค์ประกอบค่าจ้าง |
| `version_id` / `record_id` / `item_id` | id | §3.1, §3.3, §3.4 | 1 event = 1 เวอร์ชัน/เรคคอร์ด |
| `effective_date` / `effective_from` / `effective_to` | date | §3.1, §3.3, §3.4 (**HR-1 · P-1**) | บังคับทุก event ที่มีเวอร์ชัน |
| `superseded_version_id` / `superseded_record_id` | id (nullable) | §5.1, §5.2 | เฉพาะ E2, E5 |
| `company_scope` / `companies[]` | enum / list (soft ref) | §3.1 | ขอบเขตที่ได้รับผล (OQ-HR-05) |
| `employee_id` · `viewer_employee_id` · `subject_employee_id` · `changed_by` | employee ref | §3.3, §3.4 (combobox Employee Master #102) | **ส่ง `employee_id` เท่านั้น — ห้ามส่งชื่อ/ข้อมูลบุคคลดิบ** (BR-CSQ-03) |
| 🔒 `base_amount` · `amount` · `goal_amount` | money | §3.3, §3.4 | **ชั้น RESTRICTED** — ส่งค่าดิบเพราะ EC ต้องใช้ตีมูลค่า → **ต้องผ่านช่องทางที่ Engine เก็บใน scope จำกัด** · ดู **OQ-CSQ-02** · **ห้ามส่งใน E10** |
| `fte` · `currency` | decimal / enum | §3.3 | `fte` จำเป็นต่อการตีมูลค่า (BR-09) · `currency` = THB (S-38) |
| `change_reason_code` | enum 5 ค่า | §3.3 (**BR-24**) | ให้ Engine จัดกลุ่มสาเหตุได้ |
| `change_reason` / `cancel_reason` / `deactivate_reason` / `end_reason` | text | §3.1, §3.3 | บังคับตั้งแต่เวอร์ชันที่ 2 / ทุกการถอน |
| `movement_doc_no` | text (nullable · soft ref) | §3.3 (S-29) | เลขที่คำสั่งของ **Employee Movement** — feature นี้ไม่ออกเลข |
| `out_of_range_flag` | bool | §3.5 (BR-08, BR-23) | บอกว่าอัตราอยู่นอกกระบอก/ต่ำกว่าขั้นต่ำตามกฎหมาย |
| `value_diff[{grade_code, field, old, new}]` | list | §3.5 `version_diff` (S-03) | ส่งเฉพาะ field ที่เปลี่ยน — เป็นค่ากระบอก (ระดับองค์กร ไม่ใช่รายบุคคล) |
| `where_used_count` | number | §3.5 | เฉพาะ E4 — บอกขนาดผลกระทบ |
| `end_trigger` | enum {ครบเป้า, ถึงวันสิ้นสุด, ถอน} | §5.3 (BR-14) | เฉพาะ E9 |
| `view_scope` | enum {รายคน, รายการ, export} | §7 (BR-16) | เฉพาะ E10 |

- **ชั้นข้อมูล:** ค่ากระบอก/องค์ประกอบ = **INTERNAL** (ไม่ผูกบุคคล) · **จำนวนเงินรายบุคคล = RESTRICTED** 🔒 (BR-16) — masking บนหน้าจอเป็นหน้าที่ **Policy Center Data Masking** · ใน payload ส่งเป็น `employee_id` + จำนวนเงิน โดยไม่มีชื่อ/เลขบัตร/ข้อมูลติดต่อ
- **idempotency_key** = `F-HR-SALSTRUCT:{version_id|record_id|item_id|view_id}:{event_id}` — unique ต่อ (feature, ref, action) ตาม BR-CSQ-02
- **reversal:** E6 (ถอนอัตราที่ยังไม่มีผล) และ E3 (ถอนเวอร์ชัน) **ไม่ใช่ reversal** — E5/E2 ยังไม่เคยยิง · ถ้าอนาคตมีการยกเลิกผลที่ยิงไปแล้ว ต้องส่ง event ใหม่ที่มี `reversal_of` ชี้ event เดิม **ห้ามลบ/แก้ผลเดิม** (BR-CSQ-04)
- **ห้ามคำนวณ:** ไม่มีการรวมยอด ไม่มีการแปลงรายปี ไม่มีภาษี/ประกันสังคม ใน payload (BR-13 · S-42) — Engine ตีมูลค่าเอง

## §5 Register Checklist (ก่อน deploy)

- [ ] `POST /csq/profiles/register` ด้วยไฟล์นี้ → แถวใน Profile Registry ของ 7C Engine ขึ้น `pending` → `connected`
- [ ] ตรวจว่า **ไม่มี** `oc` / `dc` (เอกสาร) / `sc` ในใบนี้ (มี = reject 422)
- [ ] dev wire `emit` ที่ **10 จุด** ตาม §2 พร้อม `idempotency_key`
- [ ] **ห้าม** สร้าง column ผลรายท่อใน table ของ feature (`is_ec_triggered` ฯลฯ) — ผลอยู่ที่ `T_csq_stamp`
- [ ] **ห้าม** คำนวณมูลค่าใด ๆ ในหน้า Salary Structure (ไม่มี `cost = base * 12` · ไม่มีสูตรภาษี) — **ENG-CSQ-02 เป็นเจ้าของการตีมูลค่า**
- [ ] HTML (S2): มีคอมเมนต์ `// TODO: ENG-CSQ emit — ดู CSQ_BRIEF.md` ที่จุด publish / effective / cancel / deactivate / assign / end / recurring start-end / view-restricted · **ห้ามวาดการ์ดผล 7 ท่อในหน้านี้** · ห้าม `const PIPES_HIT = [...]`
- [ ] FRD (S5): `05_RULES` มีหัวข้อ "ผลกระทบ 7C (CSQ)" + **BR-CSQ-01…05** · `02_API` มี producer contract ของ 10 event · `04_DB` มีทุก field ใน §4 จริง · เติม trigger point เป็น `03_LOGIC §x.x` แล้ว **append กลับไฟล์นี้**

## §6 Open Questions

| # | ประเด็น | ค่าที่ใช้ไปก่อน | เจ้าภาพ |
|---|---|---|---|
| **OQ-CSQ-01** | `salcomp.viewed_restricted` (E10) ควรเป็น SecC หรือปล่อยให้ **Audit Trail ของ Policy Center** รับไปอย่างเดียว (ปริมาณ event อาจสูงมาก) | ประกาศ SecC `[DEFAULT — รอยืนยัน]` · ถ้าเคาะว่าไม่เอา ให้ตัดแค่ E10 ใบนี้ยังใช้ได้ | Architect / Policy Center |
| **OQ-CSQ-02** | ENG-CSQ รับ payload ที่มี **จำนวนเงินรายบุคคล (RESTRICTED)** ได้หรือไม่ — หรือต้องส่งแบบรวมยอด/ปกปิด | ส่งค่าดิบ + `employee_id` (ไม่มีชื่อ) `[DEFAULT — รอยืนยัน]` เพราะ EC ต้องใช้ตีมูลค่า · **ถ้าเคาะว่าห้าม** → เปลี่ยนเป็นส่ง `amount_band` หรือยอดรวมระดับบริษัท | Architect (7C Engine) + Policy Center |
| **OQ-CSQ-03** | `profile_id` จริงในทะเบียน (`CSQ-XX`) | `CSQ-SALSTRUCT` `[DEFAULT — รอยืนยัน]` | Architect (7C Engine) |
| **OQ-CSQ-04** | EC ที่ระดับโครง (E2) — ถ้าฝ่ายบริหารอยากเห็น "ผลกระทบต้นทุนจากการปรับโครงทั้งชุด" ควรมาจากที่นี่หรือจาก **Manpower Planning** | ไม่ประกาศที่นี่ (กันนับซ้ำ) → ให้ Manpower Planning เป็นผู้ประกาศ `EC · FC` | Architect / Strike |
| **OQ-STD-01** | ถ้าเคาะว่าต้องมี approval ตอนเปลี่ยนอัตรา → DOA จะยิง **DC ระดับเอกสาร** ให้เอง · **ห้าม** เพิ่ม `dc` ในใบนี้ | ไม่มี approval (อยู่ Employee Movement) | Strike |
| **OQ-STD-08** | ถ้าเคาะว่าต้องแจ้งพนักงานจาก feature นี้ → ออก `NTF_BRIEF` แยก · ไม่กระทบใบ CSQ นี้ | ปลายทางแจ้ง | Chin (ENG-NOTIFY) |
| **OQ-STD-11** | ค่าแรงขั้นต่ำตามกฎหมาย (`legal_minimum`) ยังไม่อยู่ใน group ที่ HR Configuration เผยแพร่ — กระทบ `out_of_range_flag` ใน E5 | ส่งธงจาก BR-23 เท่าที่ resolve ได้ · ถ้าต้นทางยังไม่มีค่า → ส่ง `null` **ห้ามเดาตัวเลข** | BA / Architect |

## Quality Gate (self-check)

| # | เช็ค | ผล |
|---|---|---|
| G1 | ไม่มี event ไหนประกาศท่อ `oc` | ✅ ผ่าน — ไม่มี `oc` (feature ไม่สร้างงาน OP) |
| G2 | ไม่มี `dc` ที่มาจากการอนุมัติ | ✅ ผ่าน — feature ไม่มี approval เลย (BR-21 · S-36) |
| G3 | ไม่มี `sc` | ✅ ผ่าน |
| G4 | ทุก event มี trigger point อ้างได้จริง | ✅ ผ่าน — อ้าง PREBRIEF §5.1/§5.2/§5.3 + §4 BR (FRD § จะเติมที่ S5) |
| G5 | ทุก payload field มีจริงใน data dict | ✅ ผ่าน — ทุก field ชี้ PREBRIEF §3.1–§3.5 (ณ S1.8 ยังไม่มี `04_DB` — ผูกพันตรวจซ้ำที่ S5) |
| G6 | event ที่ยิง EC ระบุ `kind` ครบ | ✅ ผ่าน — E5/E8 = `estimated` · E7/E9 = `avoided` |
| G7 | EC ที่ยังไม่มี Rate Card ระบุ `basis: declared` และไม่ใส่ตัวเลขที่คำนวณเอง | ✅ ผ่าน — ทุก EC `basis: declared` · ส่งค่าฟิลด์ดิบเท่านั้น ไม่มีการคำนวณ |
| G8 | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` | ✅ ผ่าน — `profile_id` · E10 · payload RESTRICTED |
| G9 | `event_id` ไม่ชนความหมายกับ catalog เดิม | ✅ ผ่าน — ใช้ prefix `salstruct.*` / `salcomp.*` / `salrecur.*` ตามแพทเทิร์น `{feature}.{verb ที่จบแล้ว}` เดียวกับ `hrconfig.*` |
