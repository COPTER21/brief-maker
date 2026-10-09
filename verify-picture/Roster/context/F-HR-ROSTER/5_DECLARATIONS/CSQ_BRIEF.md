# CSQ_BRIEF — F-HR-ROSTER · Shift & Roster (จัดกะ)

> ออกโดย `csq-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-29
> Input: `briefs/W2/F-HR-ROSTER/PREBRIEF.md` **v1.1 §12 (authoritative)** + §5.1/§5.2 state machine + §4 BR + §3 data dict · `LANE_BRIEF.md` (chip) · `_lane/DECL.json`
> **DIVERGENCE: —** (chip `csq ✓` = detect §12 = `CONTEXT_PACK/HR.md` แถว Shift & Roster → **✓ EC**)
> หมายเหตุ: `references/csq-contract.md` และ `references/brief-template.md` **ไม่มีในเวิร์กสเปซนี้** — ยึด contract จาก SKILL.md (7 ท่อ · `kind` 3 ค่า · Envelope · Iron Rule · Quality Gate G1–G9) + `cube-4.0-current-state.md` §3 + `feature-catalog-master.md` §0 · ค่าที่เสนอเองติด `[DEFAULT — รอยืนยัน]`
> **feature ประกาศเท่านั้น — ห้ามคำนวณผลรายท่อ ห้ามตีมูลค่าเอง** (ENG-CSQ-02 เป็นเจ้าของการตีมูลค่า) · **feature นี้ไม่มีตัวเลขเงินเลย** (BR-27)

## §1 Identity

| | |
|---|---|
| profile_id | `CSQ-HRROSTER` *(ตัวเลขลำดับจริงให้ Engine กำหนดตอน register)* `[DEFAULT — รอยืนยัน]` |
| feature_code | `F-HR-ROSTER` |
| feature name | Shift & Roster · จัดกะ |
| module | HR |
| กลุ่ม backfill | **C (commitment/plan)** — ประกาศทรัพยากรที่ **วางแผนไว้** ยังไม่ใช่ที่ใช้ไปจริง |
| archetype | **P-planner** |
| version | 1.0 (2026-08-29) |
| ท่อที่ประกาศ | **EC ท่อเดียว** · `kind: **estimated**` · `basis: **declared**` (**หน่วยชั่วโมง-กะที่วางแผน**) — **ไม่มีตัวเลขเงินในใบนี้เลย** |

## §2 Declared Events

> trigger point อ้าง **PREBRIEF §5.1 (state machine)** · **§4 (BR)** · **§2 (S-XX)** — ณ S1.8 ยังไม่มี FRD
> **ข้อผูกพันถึง S5 (`frd-generator-v6`):** ต้อง map ทุกแถวนี้เป็น `03_LOGIC §x.x` / `05_RULES BR-xx` จริง และยืนยันว่าทุก payload field มีอยู่จริงใน `04_DB` แล้ว **append ในไฟล์นี้** (ห้ามออกใบใหม่)

| # | event_id | trigger point (PREBRIEF) | ท่อที่ยิง | เงื่อนไข | payload fields |
|---|---|---|---|---|---|
| **E1** ⭐ | `roster.published` | §5.1 **T-3** `ร่าง → เผยแพร่แล้ว` (S-08 · FN-23 · BR-14 · BR-15) | **EC** `kind: estimated` · `basis: declared` | **การเผยแพร่ตารางคือจุดที่องค์กรผูกกำลังคนไว้กับวัน** — ก่อนหน้านั้นเป็นร่างที่ไม่มีใครเห็นและไม่มีผลกับใคร (BR-18) · **ยังไม่ใช่ชั่วโมงที่ใช้ไปจริง** จึงเป็น `estimated` ไม่ใช่ `actual` | `roster_version_id` · `company_id` · `period_month` · `scope_team` · `employee_id[]` (คนที่มีกะ) · **`planned_shift_count`** · **`planned_hours_total`** (Σ `hours_per_day` — **ปริมาณล้วน ไม่มีเงิน**) · `planned_hours_by_employee[]` · `night_shift_count` · `holiday_shift_count` · `config_version_ids` (`shift_pattern` · `holiday` · `shift_rule` · `period`) · `published_by` · `published_at` · `warning_ack_items[]` |
| **E2** ⭐ | `roster.republished` | §5.1 **T-4** `เผยแพร่แล้ว → ถูกแทนที่` + published เวอร์ชันใหม่ (S-11 · S-12 · **S-20 การยืนยันคำขอสลับกะ** · FN-26 · FN-27 · FN-37 · BR-15 · BR-16 · BR-22) | **EC** `kind: estimated` | **การเปลี่ยนแผนคือการเปลี่ยนการจัดสรรทรัพยากร** — ส่ง event ปรับปรุงที่ **ชี้ของเดิม** · **ห้ามแก้ผลเดิม ห้ามลบ event เดิม** (BR-CSQ-04) | ทุก field ของ E1 + **`supersedes`** (ชี้ event E1/E2 ของเวอร์ชันก่อน) · **`adjust_kind`** (`manual_edit` \| **`shift_swap`**) · `changed_cell_count` · `affected_employee_id[]` · `planned_hours_delta_by_employee[]` · `publish_note` (เหตุผลบังคับ) · `rejected_locked_dates[]` (วันที่ถูกปฏิเสธเพราะปลายทางบริโภคไปแล้ว — **บริบทการปฏิบัติตาม P-7**) |

**ทำไม EC:** ตารางกะที่เผยแพร่แล้วคือ **การจัดสรรกำลังคน (แรงงาน) ให้กับวัน** — เป็น "ทรัพยากรที่มีมูลค่า/เวลาที่ตีเป็นเงินได้" ตรงตาม §Trigger Rule ของ SKILL.md · **แต่เป็นการผูกไว้ล่วงหน้า ไม่ใช่การใช้ไปแล้ว**

**⭐ ทำไม `kind: estimated` และทำไมไม่ทับ EC ของพี่น้องในโมดูลเดียวกัน (ข้อที่ต้องอ่านให้จบ):**

| feature | event | ท่อ · kind | ก้อนอะไร | หน่วย |
|---|---|---|---|---|
| **Attendance** `CSQ-HRATT` | `attendance.day_confirmed` | **EC `actual`** | **ชั่วโมงที่ทำงานจริงในกรอบกะ** หลังหักพัก | ชั่วโมง |
| **OT** `CSQ-HROT` | `ot.time_confirmed` | **EC `actual` + FC `actual`** | **ชั่วโมงล่วงเวลาที่อนุมัติและยืนยันกับเวลาจริงแล้ว** (นอกกรอบกะ) | ชั่วโมง |
| **Shift & Roster** *(ใบนี้)* | `roster.published` | **EC `estimated`** | **ชั่วโมง-กะที่วางแผนไว้** — กำลังคนที่ถูกผูกกับวันล่วงหน้า | ชั่วโมง |

- **สามก้อนนี้เป็นคนละชั้นเวลาโดยนิยาม:** *แผน (estimated) → ของจริงในกรอบกะ (actual) → ของจริงนอกกรอบกะที่อนุมัติแล้ว (actual)* · Engine แยกด้วย `kind` ได้ตรง ๆ **ไม่ต้องพึ่งการตีความ**
- **ตารางกะไม่เคยกลายเป็นชั่วโมงที่จ่ายได้ด้วยตัวเอง** — ชั่วโมงที่จ่ายได้เกิดจาก Attendance (ในกรอบกะ) และ OT (นอกกรอบกะ) เท่านั้น · **PREBRIEF BR-21 ห้าม feature นี้คำนวณชั่วโมงจริง** และ **BR-27 ห้ามมีตัวเลขเงินทุกที่**
- **ถ้าประกาศเป็น `actual` จะเป็นการนับซ้ำทันที** — คนที่ถูกจัดเวรไว้แต่ลาป่วยไม่มา ไม่ได้ใช้แรงงานขององค์กรเลย · แผนกับของจริงต่างกันเสมอ นั่นคือเหตุผลที่ Attendance มีอยู่
- **`planned_hours_total` เป็นปริมาณล้วน (`basis: declared`)** — ยังไม่มี Rate Card สำหรับแรงงาน และ feature นี้ห้ามมีเงิน → ส่งเป็น **ชั่วโมง + บริบท (จำนวนกะกลางคืน · จำนวนกะวันหยุด)** แล้วปล่อยให้ **ENG-CSQ-02 เป็นผู้ตีมูลค่า** (G7)
- **`night_shift_count` / `holiday_shift_count` เป็นบริบท ไม่ใช่ตัวคูณ** — ห้าม feature นี้แปลงเป็นค่ากะหรือค่าทำงานวันหยุด (นั่นเป็นองค์ประกอบค่าจ้างของ Salary Structure/Payroll)

## §3 ท่อที่ไม่ประกาศ (และเหตุผล) — ห้ามเงียบ

| ท่อ | ประกาศ? | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ **ห้าม** | มาจาก Operation Process (`sow.*`) อัตโนมัติ — feature นี้ไม่สร้างงาน OP · ประกาศซ้ำ = register **reject 422** (G1) |
| **DC ระดับเอกสาร** | ❌ **ห้าม** | มาจาก **DOA engine** — **แต่ feature นี้ไม่มี DOA เลย จึงไม่มีอะไรให้ประกาศตั้งแต่ต้น** · การที่หัวหน้ายืนยันคำขอสลับกะ **ไม่ใช่การเซ็นอนุมัติเอกสาร** และไม่ใช่ terminal decision → **422** ถ้าเผลอประกาศ (G2) |
| **SC** | ❌ **ห้าม** | สงวนไว้ (OQ-C3 ยังไม่เคาะ) — `trigger=false` เสมอ (G3) |
| **DC (terminal decision)** | ⬜ ไม่ประกาศ | ไม่มี decision แบบ Continue/Adjust/Hold/Stop/Complete ใน feature นี้ · การยืนยัน/ปฏิเสธคำขอสลับกะเป็น **การจัดการตารางของหัวหน้าโดยตรง** ไม่ใช่การตัดสินชะตากรรมของกระบวนการ |
| **FC** (Financial) | ⬜ **ไม่ประกาศ — จุดที่ต่างจาก OT อย่างชัดเจน** | **การจัดกะยังไม่ผูกพันเงินขององค์กร** · เงินเดือนของพนักงานประจำจ่ายอยู่แล้วไม่ว่าจะเข้ากะไหน — การย้ายคนจากกะเช้าไปกะดึกไม่ทำให้เงินสด/งบเปลี่ยนที่จุดนี้ · **ภาระผูกพันทางการเงินเกิดที่ OT ตอนอนุมัติ (`CSQ-HROT` E1 · FC `estimated`) และที่ Payroll ตอนปิดรอบ** · ประกาศ FC ที่นี่ = **สร้างภาระผูกพันที่ไม่มีอยู่จริง และนับซ้ำกับ OT** |
| **AC** (Accounting) | ⬜ ไม่ประกาศ | ไม่มีรายการทางบัญชีเกิดจากการจัดตารางกะ — การตั้งค่าใช้จ่ายค่าแรงเกิดที่ **Payroll (W4)** และ Accounting · scope note ตัด "ไม่ทำต้นทุนแรงงาน" ชัด (OQ-STD-R2) |
| **SecC** (Security/สิทธิ์-นโยบาย) | ⬜ ไม่ประกาศ | **นโยบายกะ (แพทเทิร์นกะ · ปฏิทินวันหยุด · งวด · ค่าพัก/เพดาน) เป็นของ HR Configuration** ซึ่งประกาศ SecC ไว้แล้ว (`CSQ-HRCFG` E1–E6) — ประกาศที่นี่ = **นับซ้ำ** · feature นี้ **ไม่เปลี่ยนสิทธิ์/นโยบายของใคร** และ **ไม่มีบัญชีสิทธิ์รายคนเป็นของตัวเอง** (ต่างจาก Leave ที่มีบัญชีโควตา จึงประกาศ SecC ได้) · ตารางกะเป็น **แผนการทำงาน ไม่ใช่ข้อมูลอ่อนไหว** — การเห็นตารางถูกคุมด้วยขอบเขตของ Policy Center อยู่แล้ว (BR-25) |

**event ที่จงใจ "ไม่ประกาศ" (กันนับซ้ำ/กัน noise) — ระบุไว้ให้ตรวจได้:**

| ไม่ประกาศ | เหตุผล |
|---|---|
| **การกางตาราง · การลากกะลงช่อง · การทาช่วง · การล้างกะ (S-01 · S-03 · S-05)** | **เกิดบนตารางร่างซึ่งไม่มีใครเห็นและไม่มีผลกับใคร** (BR-18) · ยิงทุกครั้งที่ลากกะหนึ่งช่อง = event ปริมาณมหาศาลที่ไม่มีความหมายทางธุรกิจ · **ผลจริงเกิดตอนเผยแพร่ (E1)** |
| **การบันทึกร่าง / การทิ้งร่าง (S-09 · S-10)** | ยังไม่เคยผูกพันอะไร — ไม่มีอะไรให้กลับรายการ |
| **การยื่น / ตอบรับ / ปฏิเสธ / ถอน / หมดอายุ ของคำขอสลับกะ (S-20…S-24)** | เป็น **การขออนุญาตและการเจรจา ยังไม่เปลี่ยนแผน** · ผลจริงเกิดตอนที่หัวหน้ายืนยันแล้วตารางเปลี่ยน ซึ่ง **ยิงเป็น E2 พร้อม `adjust_kind: shift_swap`** อยู่แล้ว · ประกาศตรงนี้ = **นับซ้ำ** |
| **การตรวจพบข้อขัดแย้ง / การรับทราบคำเตือน (S-14 · S-15 · S-16…S-19 · S-55)** | เป็น **การตรวจและการเตือนบนหน้าจอ** ไม่ใช่ผลกระทบทางทรัพยากร · `warning_ack_items[]` ถูกส่งเป็น **field ใน payload ของ E1/E2** อยู่แล้ว ให้ Engine ใช้เป็นบริบทได้ |
| **การล็อกตารางเมื่องวดปิด (S-13 · T-5)** | **ต้นทางเป็นผู้ประกาศ** — `hrconfig.period_closed` เป็น event ของ HR Configuration · ที่นี่เป็นผู้ฟัง · แผนไม่ได้เปลี่ยนตอนล็อก มันแค่แก้ไม่ได้แล้ว |
| **การรับทราบกะของพนักงาน (S-53)** | **BR-33** ระบุว่าไม่มีผลต่อตาราง — ไม่เปลี่ยนการจัดสรรทรัพยากรใด ๆ `[AI-DRAFT]` |
| **การที่ Attendance/OT อ่าน read model (S-35 · S-38)** | เป็น **pull** — การอ่านไม่ใช่เหตุการณ์ |

## §4 Payload Contract

| field | ชนิด | มาจาก (PREBRIEF) | Classification | หมายเหตุ |
|---|---|---|---|---|
| `roster_version_id` | uuid | §3.1 | Internal | `ref` ของ envelope · **ไม่ใช่เลขที่เอกสาร** |
| `company_id` · `period_month` · `scope_team` | uuid · text · text | §3.1 | Internal | ขอบเขตของแผน |
| `employee_id[]` · `affected_employee_id[]` | uuid[] | §3.2 | **PII** | **ส่ง id เท่านั้น — ห้ามส่งชื่อดิบเข้า envelope** (BR-CSQ-03) |
| `planned_shift_count` · `planned_hours_total` · `planned_hours_by_employee[]` · `planned_hours_delta_by_employee[]` | int · decimal · array | §3.6 (computed) | Internal | **ปริมาณล้วน · `basis: declared` · ห้ามมีตัวเลขเงิน** |
| `night_shift_count` · `holiday_shift_count` | int | §3.2 (จาก `is_overnight` · `holiday`) | Internal | **บริบทให้ Engine ตีมูลค่า — ไม่ใช่ตัวคูณ** |
| `config_version_ids` | object | §3.1 | Internal | `{ shift_pattern[], holiday[], shift_rule, period }` — **`shift_rule` เป็น `null` ได้** เพราะคีย์ยังไม่เผยแพร่ (S-19 · OQ-STD-R6) |
| `changed_cell_count` · `adjust_kind` · `publish_note` · `rejected_locked_dates[]` | int · enum · text · date[] | §3.1 · §3.2 | Internal | เฉพาะ E2 · `publish_note` เป็นเหตุผลการแก้ (บังคับ) |
| `warning_ack_items[]` · `published_by` · `published_at` | array · uuid · timestamp | §3.1 | Internal | ร่องรอยการรับทราบคำเตือน |
| `supersedes` | uuid | ระบบ | Internal | เฉพาะ E2 — **ชี้ event เดิม ห้ามแก้ผลเดิม** (BR-CSQ-04) |
| `idempotency_key` | text | ระบบ | Internal | unique ต่อ (`F-HR-ROSTER`, `roster_version_id`, action) — กันยิงซ้ำตอน retry (BR-CSQ-02) |

**ไม่มี field ใดเป็นจำนวนเงิน · ไม่มี field ใดเป็นตัวเลขความต้องการกำลังคน** — ตรวจอัตโนมัติได้ที่ S6 (เทียบกับ BR-27)

## §5 Register Checklist

- [ ] `profile_id` จริงจาก Engine (ใบนี้เสนอ `CSQ-HRROSTER` `[DEFAULT — รอยืนยัน]`)
- [ ] **G1** ไม่มี event ใดประกาศ `oc` — ✅ ตรวจแล้ว
- [ ] **G2** ไม่มี event ใดประกาศ `dc` จากการอนุมัติ — ✅ ตรวจแล้ว (**feature ไม่มี DOA เลย**)
- [ ] **G3** ไม่มี event ใดประกาศ `sc` — ✅ ตรวจแล้ว
- [ ] **G4** ทุก event มี trigger point อ้างได้จริง — ✅ (ณ S1.8 อ้าง PREBRIEF §5.1/§4/§2 · **ต้องแทนที่ด้วย `03_LOGIC §x.x` ที่ S5**)
- [ ] **G5** ทุก payload field มีจริงใน `04_DB` — ⏳ **ยังทำไม่ได้ที่ S1.8 (ยังไม่มี FRD)** · §4 ผูกกับ PREBRIEF §3.1/§3.2/§3.6 แล้วทุก field · **S5 ต้องยืนยันซ้ำแล้ว append**
- [ ] **G6** event ที่ยิง EC ระบุ `kind` ครบ — ✅ E1 · E2 = `estimated` ทั้งคู่
- [ ] **G7** EC จากเวลา/แรงงานที่ยังไม่มี Rate Card ระบุ `basis: declared` — ✅ **ไม่มีตัวเลขเงินในใบนี้เลย**
- [ ] **G8** ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` — ✅ (`profile_id`)
- [ ] **G9** `event_id` ไม่ชนกับ catalog เดิม — ✅ `roster.*` เป็น prefix ใหม่ · ไม่ทับ `attendance.*` · `ot.*` · `leave.*` · `hrconfig.*`
- [ ] dev wire `emit` ที่ transition จริง (T-3 · T-4) + `idempotency_key`
- [ ] deploy → แถวใน Profile Registry ของ 7C Engine เปลี่ยนเป็น **เชื่อมแล้ว**
- [ ] ตรวจ Event Log ว่า event แรกเข้ามาแล้วประทับผลถูกท่อ (**EC เท่านั้น** · ไม่ค้าง "ยังไม่ประเมิน")

## §6 Open Questions

| # | ประเด็น | เจ้าภาพ |
|---|---|---|
| **OQ-STD-R2** ⭐ | **ต้นทุนแรงงานของตาราง** — scope ตัด "ไม่ทำต้นทุนแรงงาน" · ใบนี้จึงส่ง **ชั่วโมงล้วน** แล้วให้ **ENG-CSQ-02** ตีมูลค่า · ถ้า Strike ต้องการเห็นต้นทุนของแผนบนหน้าจอ **ต้องมี Rate Card ของแรงงานก่อน** และต้องทบทวน BR-27 | **Strike** + BA Payroll (W4) |
| **OQ-STD-R1** | **coverage/capacity** — ถ้าเปิดในอนาคต จะเกิดคำถามว่า "คนไม่พอ" ควรเป็นท่อ EC หรือไม่ · ใบนี้ **ไม่ประกาศ** เพราะไม่มีตัวเลขความต้องการให้เทียบ | Strike + BA Manpower (W6) |
| **OQ-C-R1** | **`planned_hours_total` ควรถูกหักด้วยวันลาที่อนุมัติแล้วก่อนส่งหรือไม่** — ใบนี้ default **ไม่หัก** (`[DEFAULT — รอยืนยัน]`) เพราะ **BR-12 บล็อกการลงกะทับวันลาอยู่แล้ว** จึงไม่ควรมีชั่วโมงของวันลาอยู่ในแผนตั้งแต่ต้น · ถ้าอนาคตเปลี่ยน BR-12 เป็น "เตือน" ต้องกลับมาทบทวนข้อนี้ | Strike + BA Leave |
| **OQ-C-R2** | **การปิดฉากของ `estimated`** — เมื่อเดือนผ่านไปและ Attendance ยิง `actual` ครบแล้ว Engine ควร reconcile แผนกับของจริงอย่างไร · **ไม่ใช่หน้าที่ของ feature นี้** (feature ไม่คำนวณผล) แต่ต้องมีคนออกแบบที่ฝั่ง Engine | **Architect / ENG-CSQ-02** |
| **OQ-STD-R6** | `config_version_ids.shift_rule` เป็น `null` ได้ เพราะ HR Configuration ยังไม่เผยแพร่คีย์ `shift_rule.*` — Engine ต้องยอมรับ `null` โดยไม่ถือเป็น payload ไม่ครบ | Strike + BA HR Configuration |

---

## §7 Append จาก S5 (`frd-generator-v6`) — ปิด G4 · G5 ที่ค้างไว้ตั้งแต่ S1.8

> **append ในใบเดิมตามข้อผูกพันที่ §2 ระบุไว้ — ไม่ออกใบใหม่** · 2026-08-29

### §7.1 G4 — trigger point อ้าง `03_LOGIC` จริงแล้ว ✅

| event | trigger เดิม (S1.8 · อ้าง PREBRIEF) | **trigger จริงที่ S5** |
|---|---|---|
| **E1** `roster.published` | §5.1 T-3 (S-08 · FN-23) | **`3_FRD/03_LOGIC.md §3.1 F-25 publishRoster`** (T-3) · ยิงหลัง commit สำเร็จเท่านั้น (`§3.4 SQ-9`) |
| **E2** `roster.republished` | §5.1 T-4 (S-11 · S-12 · S-20) | **`3_FRD/03_LOGIC.md §3.1 F-28 republishRoster`** (T-4) — ถูกเรียกจากทั้ง `F-27 applyManualEdits` (`adjust_kind: manual_edit`) และ `F-39 confirmSwapRequest` (`adjust_kind: shift_swap`) |

**จุดยิงจริงในโค้ด:** `F-59 emitImpactEvent` — เรียก ENG-CSQ เท่านั้น · สร้าง `idempotency_key` ต่อ (`F-HR-ROSTER`, `roster_version_id`, action) · **ยิงหลัง commit เสมอ ห้ามยิงก่อน**

### §7.2 G5 — ทุก payload field ยืนยันแล้วว่ามีจริงใน `04_DB` ✅

| field | มีจริงที่ | หมายเหตุ |
|---|---|---|
| `roster_version_id` · `company_id` · `period_month` · `scope_team` | `04_DB T_roster_version` #1 #3 #2 #5 | `ref` ของ envelope |
| `employee_id[]` · `affected_employee_id[]` | derive จาก `T_roster_cell.employee_id` (#3) | **PII — ส่ง id เท่านั้น** |
| `planned_shift_count` · `planned_hours_total` · `planned_hours_by_employee[]` · `planned_hours_delta_by_employee[]` | `04_DB §4.4` view `v_roster_period_summary` (computed จาก `hours_per_day` #14) | **ปริมาณล้วน ไม่มีเงิน** |
| `night_shift_count` · `holiday_shift_count` | `04_DB §4.4` (derive จาก `is_overnight` #12 · `holiday_ref` #22) | บริบท ไม่ใช่ตัวคูณ |
| `config_version_ids` | `T_roster_version` #15 | **`shift_rule` เป็น `null` ได้** |
| `published_by` · `published_at` · `warning_ack_items[]` | `T_roster_version` #9 #10 #14 | — |
| `changed_cell_count` · `publish_note` | derive จาก `T_roster_cell` + `T_roster_version` #11 | เฉพาะ E2 |
| **`adjust_kind`** | **`T_roster_version` #19** (enum `manual_edit` \| `shift_swap`) | **ตัวกันนับซ้ำของการสลับกะ** |
| `rejected_locked_dates[]` | `T_roster_version` #20 | บริบทการปฏิบัติตาม P-7 |
| `supersedes` | `T_roster_version` #7 | ชี้ event เดิม |
| `idempotency_key` | สร้างที่ `03_LOGIC F-59` | — |

**ตรวจซ้ำแล้ว: ไม่มี field ใดเป็นจำนวนเงิน · ไม่มี field ใดเป็นชื่อคนดิบ · ไม่มี field ใดเป็นตัวเลขความต้องการกำลังคน** (`04_DB §4.2` ไม่มีคอลัมน์เหล่านั้นเลย · `06_TESTS IA-09`)

### §7.3 Register Checklist ที่อัปเดตแล้ว

- [x] **G4** ทุก event มี trigger point อ้าง `03_LOGIC §x.x` จริง — ✅ **ปิดแล้วที่ §7.1**
- [x] **G5** ทุก payload field มีจริงใน `04_DB` — ✅ **ปิดแล้วที่ §7.2**
- [ ] `profile_id` จริงจาก Engine (ยังเป็น `CSQ-HRROSTER` `[DEFAULT — รอยืนยัน]` · **OQ-CSQ-01**)
- [ ] Engine ยอมรับ `config_version_ids.shift_rule = null` โดยไม่ถือว่า payload ไม่ครบ (**OQ-CSQ-02** · `3_FRD/07_LOCKED §7.3`)
- [ ] dev wire `emit` ที่ `F-25` / `F-28` + `idempotency_key`
