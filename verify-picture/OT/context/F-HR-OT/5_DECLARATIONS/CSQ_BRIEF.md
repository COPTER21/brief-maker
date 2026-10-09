# CSQ_BRIEF — F-HR-OT · OT / Shift (โอที)

> ออกโดย `csq-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-29
> Input: `briefs/W2/F-HR-OT/PREBRIEF.md` v1.1 §12 (**authoritative**) + §5 state machine + §4 BR · `LANE_BRIEF.md` (chip) · `_lane/DECL.json`
> **DIVERGENCE: —** (chip `csq ✓` = detect §12 = ตาราง `CONTEXT_PACK/HR.md` แถว OT / Shift → **✓ EC · FC**)
> หมายเหตุ: `references/csq-contract.md` และ `references/brief-template.md` **ไม่มีในเวิร์กสเปซนี้** — ยึด contract จาก SKILL.md (7 ท่อ · kind 3 ค่า · Envelope · Iron Rule · Quality Gate G1–G9) + `cube-4.0-current-state.md` §3 + `feature-catalog-master.md` §0 · ค่าที่เสนอเองติด `[DEFAULT — รอยืนยัน]`
> **feature ประกาศเท่านั้น — ห้ามคำนวณผลรายท่อ ห้ามตีมูลค่าเอง** (ENG-CSQ-02 เป็นเจ้าของการตีมูลค่า)

## §1 Identity

| | |
|---|---|
| profile_id | `CSQ-HROT` *(ตัวเลขลำดับจริงให้ Engine กำหนดตอน register)* `[DEFAULT — รอยืนยัน]` |
| feature_code | `F-HR-OT` |
| feature name | OT / Shift · โอที |
| module | HR |
| กลุ่ม backfill | **A + C ผสม** — A (EC on confirmed resource use: ชั่วโมงล่วงเวลาที่ยืนยันแล้ว) + C (FC on commitment: ภาระผูกพันค่าล่วงเวลาตอนอนุมัติ) |
| archetype | Q-document |
| version | 1.0 (2026-08-29) |
| ท่อที่ประกาศ | **EC · FC** · ทั้งสองท่อ `basis: declared` (**หน่วยชั่วโมง**) — **ไม่มีตัวเลขเงินในใบนี้เลย** (PREBRIEF BR-18) |

## §2 Declared Events

> trigger point อ้าง **PREBRIEF §5 (state machine)** · **§4 (BR)** · **§2 (S-XX)** — ณ S1.8 ยังไม่มี FRD
> **ข้อผูกพันถึง S5 (`frd-generator-v6`):** ต้อง map ทุกแถวนี้เป็น `03_LOGIC §x.x` / `05_RULES BR-xx` จริง แล้ว **append ในไฟล์นี้** (ห้ามออกใบใหม่)

| # | event_id | trigger point (PREBRIEF) | ท่อที่ยิง | เงื่อนไข | payload fields |
|---|---|---|---|---|---|
| **E1** | `ot.approved` | §5 **T-4** `รออนุมัติ → อนุมัติแล้ว` (S-10 · S-11 · S-17 · FN-29 · FN-31) | **FC** `kind: estimated` · `basis: declared` | การอนุมัติ OT = **ภาระผูกพันค่าล่วงเวลาที่องค์กรผูกพันแล้วแต่ยังไม่จ่ายจริง** — ตรงนิยาม "commit" ของท่อ FC · **ยังไม่ยิง EC** เพราะยังไม่ยืนยันว่าทำงานจริง (คำขอล่วงหน้าอาจไม่ได้ทำ) | `employee_id` · `ot_no` · `company_id` · `work_date` · `rate_type` · `multiplier` · `payroll_code` · `ot_rate_version_id` · **`hours_approved`** · `over_cap` · `cap_snapshot_hours_week` · `period_code` · `approved_by` |
| **E2** ⭐ | `ot.time_confirmed` | §5 **T-8** `อนุมัติแล้ว → ยืนยันเวลาจริงแล้ว` (S-16 · FN-21 · **BR-17**) | **EC** `kind: actual` · `basis: declared` **+ FC** `kind: actual` | ชั่วโมงล่วงเวลาที่ **ยืนยันกับเวลาจริงแล้ว** = **แรงงานที่องค์กรใช้ไปจริงนอกกรอบกะ** (EC) **และ** ภาระผูกพันเดิมกลายเป็นค่าใช้จ่ายที่แน่นอน (FC เปลี่ยนจาก `estimated` เป็น `actual`) | ทุก field ของ E1 + **`hours_confirmed`** · `attendance_outside_hours` · `attendance_version_ids` · `confirmed_by` · **`supersedes`** (ชี้ event E1 ของใบเดียวกัน) |
| **E3** | `ot.withdrawn` | §5 **T-9** `อนุมัติแล้ว / ยืนยันเวลาจริงแล้ว → ถอน` (S-14 · S-34 · FN-41 · FN-42 · BR-27) | **EC** `kind: actual` **+ FC** `kind: estimated`/`actual` (ตามสถานะที่ถอน) | ถอนใบ → **กลับรายการ** ทั้งชั่วโมงที่นับไปและภาระผูกพันที่ตั้งไว้ | ทุก field ของ E1/E2 + **`reversal_of`** (ชี้ event เดิม) · `withdraw_reason` · `withdrawn_by` |
| **E4** | `ot.rejected` | §5 **T-5** `รออนุมัติ → ไม่อนุมัติ` (S-12 · FN-30) | **FC** `kind: avoided` | คำขอถูกปฏิเสธ → **ภาระผูกพันที่อาจเกิดถูกหยุดไว้** = การประหยัดที่เกิดจากการหยุด ตรงนิยาม `avoided` · **ไม่ยิง EC** เพราะไม่เคยมีชั่วโมงล่วงเวลาที่ได้รับอนุมัติเกิดขึ้นจริง | `employee_id` · `ot_no` · `company_id` · `work_date` · `rate_type` · `multiplier` · `payroll_code` · **`hours_requested`** · `reject_reason` · `rejected_by` |
| **E5** | `ot.hours_adjusted` | §5 **T-4 (อนุมัติบางส่วน · S-17 · FN-31)** และการปรับชั่วโมงที่รับรองหลังธง "ต้องทวน" (S-23 · FN-43 · BR-22) | **EC** `kind: actual` **+ FC** `kind: estimated` | ชั่วโมงที่รับรอง **น้อยกว่า/ต่างจากที่เคยประกาศไว้** → ส่ง event ปรับปรุงที่ชี้ของเดิม **ห้ามแก้ผลเดิม** (BR-CSQ-04) | `employee_id` · `ot_no` · `hours_before` · `hours_after` · `adjust_kind` (`partial_approval` \| `attendance_adjusted`) · `adjust_reason` · **`supersedes`** · `adjusted_by` |

**ทำไม EC:** ชั่วโมงล่วงเวลาที่ยืนยันแล้วคือ **แรงงานที่องค์กรใช้ไปนอกกรอบกะปกติ** — ตรงนิยาม "มีมูลค่า/ต้นทุน/**เวลาที่ตีเป็นเงินได้**" ของท่อ EC ใน SKILL.md §Trigger Rule
**EC ตัวนี้ไม่ซ้ำกับ `CSQ-HRATT`:** Attendance ยิง `attendance.day_confirmed` ซึ่งเป็น **ชั่วโมงในกรอบกะ** และประกาศชัดว่า `outside_shift_hours` **ยังไม่ใช่ OT ที่อนุมัติ** (BR-18 ของแพ็กนั้น) — EC ในใบนี้คือ **ชั่วโมงนอกกะที่ผ่านการอนุมัติและยืนยันแล้ว** ซึ่งเป็นคนละก้อนโดยนิยาม · **ไม่ซ้ำกับ `CSQ-HRLV`** ซึ่งเป็น **วันลา (หน่วยวัน)**
**ทำไม FC:** การอนุมัติ OT ทำให้องค์กร **ผูกพันค่าล่วงเวลาก่อนที่ Payroll จะจ่ายจริง** — ตรงนิยาม "ทำให้เงินสดหรืองบเปลี่ยน (commit / ใช้จริง / คืน)" ของท่อ FC · เป็นเหตุผลเดียวกับที่ `CONTEXT_PACK/HR.md` แถว OT ระบุ **`✓ EC · FC`** และเป็นทางที่ทำให้ **การคุมงบค่าล่วงเวลาเกิดขึ้นได้โดยที่ feature ไม่ต้องมี Budget module** (OQ-STD-OT4)
**ทำไม E1 = FC เท่านั้น แต่ E2 = EC + FC:** อนุมัติ ≠ ทำจริง — คำขอล่วงหน้าอาจไม่ถูกใช้ · ถ้ายิง EC ตั้งแต่อนุมัติ จะเป็นการนับแรงงานที่ยังไม่เกิด และขัดกับ **BR-17** ที่กำหนดว่าเฉพาะใบที่ยืนยันเวลาจริงแล้วเท่านั้นที่นับเป็นของจริง
**`basis: declared` ทุกท่อ:** ทั้ง EC และ FC มาจาก **เวลา/แรงงานที่ยังไม่มี Rate Card** และ **feature นี้ห้ามมีตัวเลขเงินโดยเด็ดขาด** (BR-18) จึงส่งเป็น **ปริมาณชั่วโมงล้วน + `rate_type` + `multiplier` + `payroll_code` เป็นบริบท** แล้วปล่อยให้ **ENG-CSQ-02 เป็นผู้ตีมูลค่า** (G7)

## §3 ท่อที่ไม่ประกาศ (และเหตุผล) — ห้ามเงียบ

| ท่อ | ประกาศ? | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ **ห้าม** | มาจาก Operation Process (`sow.*`) อัตโนมัติ — feature นี้ไม่ได้สร้างงาน OP · ประกาศซ้ำ = **register reject 422** |
| **DC (Decision) ระดับเอกสาร** | ❌ **ห้าม** | **มาจาก DOA engine** — feature นี้มีการอนุมัติจริง **ถึงสองชั้น** (ดู `DOA_BRIEF.md`) ยิ่งต้องไม่ประกาศซ้ำ · การอนุมัติ/ไม่อนุมัติใบ OT = **การเซ็นอนุมัติเอกสาร** ไม่ใช่ terminal decision ของกระบวนการ → **422** |
| **SC** | ❌ **ห้าม** | สงวนไว้ (OQ-C3 ยังไม่เคาะ) — `trigger=false` เสมอ |
| **DC (terminal decision)** | ⬜ ไม่ประกาศ | ไม่มี decision แบบ Continue/Adjust/Hold/Stop/Complete ใน feature นี้ — ทุกจุดตัดสินใจคือการอนุมัติเอกสาร (ของ DOA) · **แม้แต่การที่ "เกินเพดานแล้วต้องขึ้นอีกชั้น" ก็เป็นการเลือกสายอนุมัติ ไม่ใช่ terminal decision** |
| **AC** (Accounting) | ⬜ ไม่ประกาศ | ไม่มีรายการทางบัญชีเกิดจากการอนุมัติ OT — การตั้งค่าใช้จ่ายค่าล่วงเวลาเกิดที่ **Payroll (W4)** และ Accounting · scope note ตัด "ไม่คิดเงิน OT" ชัด (OQ-STD-OT1) |
| **SecC** (Security/สิทธิ์-นโยบาย) | ⬜ ไม่ประกาศ | **นโยบาย OT (อัตรา · ตัวคูณ · เพดาน) เป็นของ HR Configuration** ซึ่งประกาศ SecC ไว้แล้ว (`CSQ-HRCFG` E1–E6) — ประกาศที่นี่ = **นับซ้ำ** · feature นี้ไม่เปลี่ยนสิทธิ์/นโยบายของใคร (ต่างจาก Leave ที่มีบัญชีสิทธิ์รายคนเป็นของตัวเอง จึงประกาศ SecC ได้) |

**event ที่จงใจ "ไม่ประกาศ" (กันนับซ้ำ/กัน noise) — ระบุไว้ให้ตรวจได้:**

| ไม่ประกาศ | เหตุผล |
|---|---|
| การบันทึกร่าง (S-08) · การแก้ร่าง | ยังไม่มีผลใด ๆ — ไม่ออกเลข ไม่ผูกพันอะไร |
| **การส่งอนุมัติ (S-09 · T-2)** | เป็นการ **ขออนุญาต** ยังไม่ผูกพัน — ผลจริงเกิดที่ E1 (อนุมัติ) หรือถูกหยุดที่ E4 (ปฏิเสธ) · ประกาศตรงนี้ = **นับซ้ำ** และยิง event ปริมาณมากทุกครั้งที่ยื่น |
| **การคำนวณ/เตือนเพดาน (S-05 · S-06)** | เป็น **การตรวจและการแจ้งเตือน** (ท่อ NTF) ไม่ใช่ผลกระทบทางทรัพยากร — และ `over_cap` ถูกส่งไปเป็น **field ใน payload ของ E1** อยู่แล้ว ให้ Engine ใช้เป็นบริบทได้ |
| การยกเลิกใบที่ยังรออนุมัติ (S-13) | ยังไม่เคยผูกพันอะไร — ไม่มีอะไรให้กลับรายการ |
| การแก้แล้วส่งใหม่ (S-15) | ยังไม่เคยอนุมัติ = ยังไม่เคยผูกพัน |
| การตรวจ/บล็อกทั้งหมด (S-07 · S-19 · S-21 · S-22 · S-28 · S-29 · S-30 · S-43) | เป็น validation ที่ **ไม่ทำให้อะไรเปลี่ยน** |
| **การเผยแพร่ให้ Payroll/ESS อ่าน (S-31 · S-32)** | เป็น **read model** ไม่ใช่เหตุการณ์ใหม่ — ผลถูกนับที่ E2 แล้ว · ประกาศอีก = **นับซ้ำ** |
| `attendance.*` (S-21 · S-22 · S-23) | เป็นของ Attendance (`CSQ-HRATT` E1–E3) — OT เป็นผู้อ่านอย่างเดียว (AT-5) · ผลที่ตกกับใบเราถูกประกาศเป็น **E5 `ot.hours_adjusted`** ซึ่งเป็นการเปลี่ยนของ **ใบ OT** ไม่ใช่ของเวลาเข้างาน |
| `hrconfig.*` (S-24 · S-25) | **เป็นของ HR Configuration** (`CSQ-HRCFG`) — OT เป็นผู้ฟัง · ประกาศที่นี่ = นับซ้ำ |
| `leave.*` (S-28) | เป็นของ Leave (`CSQ-HRLV`) — OT อ่านเพื่อกันทับเท่านั้น (LV-5) |
| การปิดงวด (S-29 · S-32) | เจ้าของสถานะงวดคือ **HR Configuration** (`hrconfig.period_closed`) — ที่นี่เป็นผู้ **บังคับใช้** ไม่ใช่ผู้ประกาศ |

## §4 Payload Contract

| field | ชนิด | มาจาก (PREBRIEF) | หมายเหตุ / masking |
|---|---|---|---|
| `employee_id` | employee ref | §3.1 ผู้ขอ (combobox Employee Master #102) | **ส่ง id เท่านั้น — ห้ามส่งชื่อ/ข้อมูลบุคคลดิบ** (BR-CSQ-03) |
| `ot_no` | text | §3.1 เลขที่ใบ OT (DOCCFG) | ref ของทุก event |
| `company_id` | soft ref (Organization) | §3.1 | แยกขอบเขตบริษัทลูก (OQ-HR-05) |
| `work_date` · `time_from` · `time_to` | date · time · time | §3.2 | ให้ Engine จัดกลุ่มตามวัน/ช่วงเวลาได้ |
| `rate_type` · `multiplier` · `payroll_code` | enum · numeric(4,2) · text | §3.2 **snapshot จาก HR Config `ot_rate`** | **เป็นบริบทให้ Engine ตีมูลค่า ไม่ใช่จำนวนเงิน และ feature ห้ามเอาไปคูณเอง** (BR-18 · Iron Rule) |
| `ot_rate_version_id` | id | §3.2 | **บังคับ** — บอกว่าใช้อัตราเวอร์ชันไหน (C-2) |
| **`hours_requested` · `hours_approved` · `hours_confirmed`** | decimal(6,2) | §3.1 | **หน่วยชั่วโมง** · แต่ละ event ส่งเฉพาะตัวที่เกี่ยวข้อง · **ไม่ใช่เงิน** |
| `attendance_outside_hours` · `attendance_version_ids` | decimal(5,2) · jsonb | §3.2 · §3.4 | เฉพาะ E2 — พิสูจน์ว่าชั่วโมงที่รับรองผูกกับเวลาจริงเวอร์ชันไหน (AT-2) |
| **`over_cap` · `cap_snapshot_hours_week`** | bool · numeric(5,2) | §3.1 | **บริบทการปฏิบัติตามกฎหมายแรงงาน** — ให้ Engine/Report เห็นว่าใบไหนเกินเพดานและเพดานตอนนั้นเท่าไร · **ค่ามาจาก HR Config ไม่ใช่ค่าคงที่** |
| `period_code` | text | §3.1 (HR Config `pay_period`) | ให้ Engine จัดกลุ่มตามงวด |
| `hours_before` · `hours_after` · `adjust_kind` · `adjust_reason` | decimal · decimal · enum · text | §3.1 | เฉพาะ E5 |
| `approved_by` · `rejected_by` · `confirmed_by` · `withdrawn_by` · `adjusted_by` | employee ref | §3.1 | ส่ง **employee_id เท่านั้น** |
| `reversal_of` · `supersedes` | event id | §5 T-9 · T-8 · T-4 | **BR-CSQ-04 ห้ามลบ/แก้ผลเดิม** |
| `reject_reason` · `withdraw_reason` | text | §3.1 | **ห้ามส่ง `reason` (เหตุผลความจำเป็น) และ `work_done` (งานที่ทำ) ของพนักงาน** — Confidential · ส่งเฉพาะเหตุผลของ **การตัดสิน/การถอน** |

- **ชั้นข้อมูล:** ชั่วโมง OT รายคน = **Confidential** → **ห้ามส่ง `reason` · `work_done` · ชื่อไฟล์แนบ** เข้า envelope · field คนส่งเป็น id เสมอ
- **idempotency_key** = `F-HR-OT:{ot_no}:{event_id}` สำหรับ E1–E4 · `F-HR-OT:{ot_no}:{event_id}:{seq}` สำหรับ E5 (ปรับได้หลายครั้ง) — unique ต่อ (feature, ref, action) ตาม BR-CSQ-02
- **reversal / supersede:** การถอน (E3) และการปรับชั่วโมง (E5) **ไม่ลบ/ไม่แก้ผลเดิม** — เป็น event ใหม่ที่ชี้ของเดิม (BR-CSQ-04 · PREBRIEF BR-27)
- **ห้ามคำนวณมูลค่าใด ๆ**: ไม่มี `cost = hours × multiplier × rate` ที่ไหนใน feature — **ENG-CSQ-02 เป็นเจ้าของการตีมูลค่า** (Iron Rule · PREBRIEF BR-18 · FN-53)

## §5 Register Checklist (ก่อน deploy)

- [ ] `POST /csq/profiles/register` ด้วยไฟล์นี้ → แถวใน Profile Registry ของ 7C Engine ขึ้น `pending` → `connected`
- [ ] ตรวจว่า **ไม่มี** `oc` / `dc` (เอกสาร) / `sc` ในใบนี้ — **โดยเฉพาะ `dc`: feature นี้มี approval จริงสองชั้น DOA เป็นเจ้าของ** (ถ้ามี = reject 422)
- [ ] ตรวจว่า **ไม่มี** `secc` — นโยบาย OT เป็นของ `CSQ-HRCFG` (ประกาศที่นี่ = นับซ้ำ)
- [ ] ตรวจว่า **ไม่มี** `ac` — รายการบัญชีเกิดที่ Payroll (W4)
- [ ] ตรวจว่า **`ec` ไม่ซ้ำกับ `CSQ-HRATT`** — EC ในใบนี้คือ **ชั่วโมงนอกกะที่อนุมัติและยืนยันแล้ว** ไม่ใช่ **ชั่วโมงในกรอบกะ** · และ **ไม่ซ้ำกับ `CSQ-HRLV`** ซึ่งเป็นหน่วยวัน
- [ ] ตรวจว่า **`fc` ไม่ซ้ำกับ Payroll (W4)** เมื่อ Payroll ถูกสร้าง — FC ในใบนี้คือ **ภาระผูกพันตอนอนุมัติ OT** · FC ของ Payroll คือ **การจ่ายจริง** → ต้องเป็น `supersedes`/คนละ kind ไม่ใช่การนับซ้ำ (**OQ-CSQ-03**)
- [ ] dev wire `emit` ที่ 5 จุดจริงตาม §2 พร้อม `idempotency_key`
- [ ] **ห้าม** สร้าง column ผลรายท่อใน table ของ feature (`is_ec_triggered` ฯลฯ) — ผลอยู่ที่ `T_csq_stamp`
- [ ] **ห้าม** มีตัวเลขเงิน/อัตราค่าแรง/สูตรคูณ ในหน้าจอ · payload · หรือที่ใดก็ตาม (BR-18 · FN-53)
- [ ] HTML (S2): คอมเมนต์ `// TODO: ENG-CSQ emit — ดู CSQ_BRIEF.md` ที่จุด **อนุมัติ · ไม่อนุมัติ · ยืนยันเวลาจริง · ถอน · ปรับชั่วโมง** · **ห้ามวาดการ์ดผล 7 ท่อในหน้านี้**
- [ ] FRD (S5): `05_RULES` มีหัวข้อ "ผลกระทบ 7C (CSQ)" + BR-CSQ-01..05 · `02_API` มี producer contract ของ 5 event · เติม trigger point เป็น `03_LOGIC §x.x` แล้ว append กลับไฟล์นี้

## §6 Open Questions

| # | ประเด็น | ค่าที่ใช้ไปก่อน | เจ้าภาพ |
|---|---|---|---|
| OQ-CSQ-01 | profile_id จริงในทะเบียน (`CSQ-XX`) | `CSQ-HROT` `[DEFAULT — รอยืนยัน]` | Architect (7C Engine) |
| **OQ-CSQ-02** | **E2 ยิง 2 ท่อพร้อมกัน (EC + FC) ได้หรือไม่** หรือต้องแตกเป็น 2 event | **ยิง 2 ท่อจาก event เดียว** `[DEFAULT — รอยืนยัน]` (เหตุการณ์เดียวมีผลสองด้านจริง: แรงงานที่ใช้ไป = EC · ภาระผูกพันที่แน่นอนขึ้น = FC) — ถ้า Engine ต้องการ 1 event : 1 ท่อ ให้แตกเป็น `ot.time_confirmed` (EC) + `ot.cost_committed` (FC) · **เป็นคำถามเดียวกับ OQ-CSQ-02 ของ `CSQ-HRLV`** ควรเคาะพร้อมกัน | Architect (ENG-CSQ) |
| **OQ-CSQ-03** ⭐ | **FC ของ OT (ภาระผูกพันตอนอนุมัติ) กับ FC ของ Payroll (การจ่ายจริง ณ W4) จะนับซ้ำกันหรือไม่** | ประกาศ FC ที่นี่เป็น `estimated` ตอนอนุมัติ แล้ว `actual` ตอนยืนยันเวลาจริง · **เมื่อ Payroll ถูกสร้าง ต้องออกแบบให้ FC ของ Payroll `supersedes` ของ OT ไม่ใช่บวกเพิ่ม** `[DEFAULT — รอยืนยัน]` | Architect (ENG-CSQ) + BA Payroll |
| OQ-CSQ-04 | E4 (`ot.rejected` → FC `avoided`) เป็นการประหยัดจริงหรือเป็นเพียงการไม่เกิดค่าใช้จ่าย | **ประกาศ `avoided`** `[DEFAULT — รอยืนยัน]` — ตระกูลเดียวกับ "ยกเลิก QT" ใน SKILL.md · ถ้า Engine ถือว่าไม่ใช่ ให้ตัด E4 ออก **ห้ามเปลี่ยนเป็นท่ออื่นเอง** | Architect / Strike |
| OQ-STD-OT1 | ถ้าเคาะให้คิดเงิน OT ที่นี่ → จะเกิดท่อ AC ขึ้นมา · **ห้าม**เพิ่มเองในใบนี้จนกว่า Strike จะเคาะ | ไม่คิดเงินที่นี่ | Strike (คู่ OQ-HR-01) |
| OQ-STD-OT4 | การคุมงบค่าล่วงเวลาจะทำผ่านท่อ FC นี้ทั้งหมดหรือไม่ (ยังไม่มี Budget module) | **ผ่าน FC** — feature ไม่ทำ budget control เอง | Architect (ENG-CSQ) |

## Quality Gate (self-check)

| # | เช็ค | ผล |
|---|---|---|
| G1 | ไม่มี event ไหนประกาศท่อ `oc` | ✅ §3 ระบุชัด |
| G2 | ไม่มี event ไหนประกาศ `dc` เพราะการอนุมัติ | ✅ §3 — feature มี approval **สองชั้น** ยิ่งต้องไม่ประกาศ |
| G3 | ไม่มี event ไหนประกาศ `sc` | ✅ |
| G4 | ทุก event มี trigger point อ้าง PREBRIEF § ได้ | ✅ 5/5 อ้าง §5 transition + S-XX + FN-XX + BR-XX |
| G5 | ทุก payload field มีจริงใน data dict ของ feature | ✅ ทุก field อ้าง PREBRIEF §3.1 / §3.2 / §3.4 (S5 จะ map เป็น `04_DB` จริง) |
| G6 | event ที่ยิง EC ระบุ `kind` ครบ | ✅ E2 `actual` · E3 `actual` (reversal) · E5 `actual` |
| G7 | EC จากเวลา/แรงงานที่ยังไม่มี Rate Card ระบุ `basis: declared` | ✅ **ทุก event ทั้ง EC และ FC** เป็น `basis: declared` หน่วยชั่วโมง · **ไม่มีตัวเลขเงินในใบนี้** |
| G8 | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` ครบ | ✅ profile_id · OQ-CSQ-02 · OQ-CSQ-03 · OQ-CSQ-04 |
| G9 | `event_id` ไม่ชนกับ catalog เดิมโดยความหมายซ้อน | ✅ `ot.*` ไม่ซ้ำกับ `attendance.*` (ชั่วโมงในกรอบกะ) · `leave.*` (วัน) · `hrconfig.*` (นโยบาย) — ระบุความต่างไว้ใน §2 และ §5 |

**Verdict: PASS** — 5 event · 2 ท่อ (**EC · FC**) พร้อม register เข้า Profile Registry

---

## §6 FRD Mapping (append โดย S5 · `frd-generator-v6` · 2026-08-29) — **ไม่ออกใบใหม่**

> ข้อผูกพันจาก §2: "ต้อง map ทุกแถวนี้เป็น `03_LOGIC §x.x` / `05_RULES BR-xx` จริง แล้ว append ในไฟล์นี้" — ทำแล้วตามตารางนี้

| # | event_id | trigger จริงใน FRD | ท่อ · kind | rule ที่บังคับ |
|---|---|---|---|---|
| E1 | `ot.approved` | `03_LOGIC §3.1 F-39 approveStep` (ขั้นสุดท้าย) → `F-65 emitImpactEvent` | **FC** `estimated` · `declared` | `05_RULES §5.2 T-4` · BR-10 · BR-18 |
| **E2** ⭐ | `ot.time_confirmed` | `03_LOGIC §3.1 F-45 confirmActualHours` → `F-65` | **EC + FC** `actual` · `declared` | `05_RULES §5.2 T-8` · **BR-17** · BR-21 |
| E3 | `ot.withdrawn` | `03_LOGIC §3.1 F-44 finalizeWithdrawal` → `F-65` | **EC + FC** (`reversal_of`) | `05_RULES §5.2 T-9` · BR-27 |
| E4 | `ot.rejected` | `03_LOGIC §3.1 F-41 rejectRequest` → `F-65` | **FC** `avoided` | `05_RULES §5.2 T-5` · BR-12 |
| E5 | `ot.hours_adjusted` | `03_LOGIC §3.1 F-40 approvePartial` · `F-49 adjustConfirmedHours` → `F-65` (`supersedes`) | **EC + FC** | `05_RULES §5.2 T-4 · T-11` · BR-21 · BR-22 |

**ยืนยันความสอดคล้อง (gate ของ Lane Mode v2):**
- FRD ใช้ **5 event = 5 event ที่ประกาศไว้ในใบนี้** · **2 ท่อ = EC + FC เท่านั้น** — **ไม่มีตัวเพิ่ม** (`00_OVERVIEW §0.16.2`)
- **ไม่ประกาศ OC · DC ระดับเอกสาร · SC · AC · SecC** — ยืนยันอีกครั้งที่ `00_OVERVIEW §0.16.2` · เหตุผลของแต่ละท่ออยู่ที่ §3 ของใบนี้ **ไม่มีข้อใดเปลี่ยน**
- **DC ระดับเอกสารยังเป็นของ DOA** — feature นี้มีสายอนุมัติจริง **สองรูปแบบ (2 ขั้น / 3 ขั้น)** ดังที่ `00_OVERVIEW §0.16.4` ระบุ จึงยิ่งต้องไม่ประกาศซ้ำ
- ชุด event 7C ของใบนี้ (`ot.*` dot) **ไม่ทับกับ 7 event แจ้งเตือนของ `NTF_BRIEF` (`ot_*` underscore) แม้แต่ตัวเดียว**
- **ห้ามคำนวณมูลค่า** ยังมีผล — ไม่มีสูตร `ชั่วโมง × ตัวคูณ × อัตรา` ที่ใดในแพ็ก FRD (`06_TESTS IA-07` · `03_LOGIC F-67`)
- `idempotency_key` ตามที่ §4 กำหนด — ทดสอบที่ `06_TESTS CM-10`
