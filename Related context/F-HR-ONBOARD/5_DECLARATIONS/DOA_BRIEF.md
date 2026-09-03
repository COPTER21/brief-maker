# DOA_BRIEF — F-HR-ONBOARD · On/Offboard (เข้าออกงาน)

> ออกโดย `doa-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-29
> Input: `briefs/W3/F-HR-ONBOARD/PREBRIEF.md` v1.1 §12 (สัญญาณประกาศ · **authoritative**) + §5 state machine + §4 BR · `LANE_BRIEF.md` (chip) · `_lane/DECL.json`
> **DIVERGENCE: —** (chip `doa ✓` = detect §12 = `briefs/W3/CHECKLIST.md` = `FEATURE_LIST_ALL.md` = `CONTEXT_PACK/HR.md` แถว On/Offboard → ✓ "DOA อนุมัติการออก")
> หมายเหตุ: `references/doa-contract.md` และ `references/brief-template.md` **ไม่มีในเวิร์กสเปซนี้** — ยึด contract จาก SKILL.md (Iron Rule · Quality Gate G1–G7) + `cube-4.0-current-state.md §3` + `feature-catalog-master.md §0` · **`role-*` id ทุกตัวจึงติด `[DEFAULT — รอยืนยัน]`** (ต้อง cross-check กับ master 14 roles ที่ Policy Center ก่อน set จริง — เหมือน Leave/OT)
> **feature ประกาศเท่านั้น — ห้าม hardcode สายอนุมัติ** (`GET /doa/resolve`) · **hardcode = governance Hard Stop**

## §1 Identity

| | |
|---|---|
| feature_id | `F-HR-ONBOARD` |
| feature name | On/Offboard · เข้าออกงาน |
| module | HR |
| platform | Core ERP (core.2bsimple.com) |
| archetype | **master + checklist(OP)** (`archetype_confirmed: master`) |
| **approval_scope** | **`policy_approve`** — **ไม่ใช่ `document_sign`** เพราะ **feature นี้ไม่ออกเอกสารและไม่มีช่องลายเซ็นใน PDF** (ไม่มี `doccfg` · ไม่มี `pdfdoc` — ดู `NOT_NEEDED.md`) · สิ่งที่อนุมัติคือ **การสิ้นสุดสภาพการเป็นพนักงานและการเพิกถอนสิทธิ์** ซึ่งเป็นการตัดสินเชิงนโยบาย/สิทธิ์ ตรงกับนิยาม `policy_approve` ใน SKILL.md §Q4 (ตระกูลเดียวกับ credit limit / discount override) · **ยืนยันที่ OQ-DOA-05** |
| **มีวงเงิน (เงิน)?** | **❌ ไม่มีวงเงินเป็นเงินเลย** — **BR-18: ห้ามมีตัวเลขเงินทุกชนิดใน feature นี้** (ค่าชดเชย/เงินได้ครั้งสุดท้าย = Payroll W4 · scope note ตัดชัด) → ทุก set ใช้ `amount_from: 0` · `amount_to: null` |
| **มีจุดตัด (threshold) ไหม?** | **✅ มี — จุดตัดคือ "ประเภทของการออก" ไม่ใช่จำนวนเงิน** · ออกโดยสมัครใจ (ลาออก · ครบสัญญา · เกษียณ) = สายสั้น · **ออกโดยไม่สมัครใจหรือออกทันที (เลิกจ้าง · ไม่ผ่านทดลองงาน · `is_immediate_exit = true`) = สายยาวขึ้น** |
| จำนวนสายอนุมัติ | **2 สาย** (`matrix` 2 ชุด ผูก 2 action) · **สมัครใจ 2 ขั้น** · **ไม่สมัครใจ/ทันที 3 ขั้น** · + **1 action สำหรับการยกเลิกรอบ** ที่ยืม matrix ของรอบเดิม |
| chainMode | **`sequential`** ทั้งสองสาย — เซ็นไล่ทีละขั้น (PREBRIEF §5 T-8) |
| departments | **`merged`** — ทุกแผนกใช้กฎชุดเดียวกัน (ไม่มีสัญญาณแยกแผนกใน scope note) |
| version | 1.0 (2026-08-29) · `wire_status: pending` |

## §2 Approval Actions

| # | action_id | ชื่อ | trigger (PREBRIEF) | ผลเมื่อ **approve** | ผลเมื่อ **reject** |
|---|---|---|---|---|---|
| **A-1** | `offboard_approve_voluntary` | **อนุมัติการออกจากงาน (โดยสมัครใจ)** | §5 **T-7** `ร่าง → รออนุมัติ` เมื่อ `termination_reason ∈ {ลาออก, ครบสัญญา, เกษียณ}` **และ** `is_immediate_exit = false` (S-14 · S-17 · FN-19 · FN-23) แล้วไล่ slot จนถึง **T-8** | รอบเป็น **"อนุมัติแล้ว"** · **checklist ปิดสิทธิ์เดินได้** (BR-07 · FN-25) · **เผยแพร่ `last_working_day`** ให้ Attendance/Leave/Payroll + สัญญาณ leaver ให้ Welfare (BR-17 · FN-26) · ตั้ง `revocation_due_at` = สิ้นวัน `last_working_day` (BR-05) | รอบเป็น **"ไม่อนุมัติ"** · **บังคับ `reject_reason`** (T-9 · FN-27) · กลับ "ร่าง" ได้ (T-10) → ส่งใหม่ = **re-resolve สายใหม่** · **ไม่มีสิทธิ์ใดถูกแตะเลย** (S-19) |
| **A-2** ⭐ | `offboard_approve_involuntary` | **อนุมัติการออกจากงาน (ไม่สมัครใจ / ออกทันที)** | §5 **T-7** เมื่อ `termination_reason ∈ {เลิกจ้าง, ไม่ผ่านทดลองงาน}` **หรือ** `is_immediate_exit = true` (S-26 · FN-37) | เหมือน A-1 แต่ต้องผ่าน **3 ขั้น** ครบก่อน · ⭐ **ถ้า `is_immediate_exit = true` → `revocation_due_at` = เวลาที่อนุมัติครบสาย → เพิกถอนทันที ไม่รอวันสุดท้าย** (S-26 · BR-05 · FN-37) | เหมือน A-1 · **สิทธิ์ยังไม่ถูกแตะ** |
| **A-3** | `offboard_approve_cancellation` | **อนุมัติการยกเลิก/ถอนการออกจากงาน** `[ASSUMED · OQ-OB-11]` | §5 **T-13** `อนุมัติแล้ว → ยกเลิก` (S-37) **และ T-14** `เพิกถอนสิทธิ์แล้ว → ยกเลิก` (S-38 · FN-48 · FN-50) | รอบเป็น **"ยกเลิก"** · **ปิดงาน checklist ที่ค้างทั้งหมดอย่างชัดแจ้ง** (BR-13 · FN-48) · **ถอน `last_working_day` ที่เผยแพร่ไปแล้ว + แจ้งปลายทาง** (FN-49) · ⭐ **ถ้าเพิกถอนสิทธิ์ไปแล้ว → ออก "คำขอคืนสิทธิ์" ใหม่ ห้ามย้อนสถานะเงียบ ๆ** (BR-14 · FN-50 · FN-51) | รอบคงสถานะเดิม · บันทึกการปฏิเสธคำขอยกเลิกในประวัติ (append-only) |

> **A-3 ใช้ matrix ของ A-1 หรือ A-2 ตาม action ที่รอบนั้นใช้ตอนอนุมัติครั้งแรก** — ไม่มี matrix ของตัวเอง (การถอนการตัดสินใจต้องผ่านคนชุดเดียวกับที่ตัดสินใจ)

### §2.1 ⭐ สิ่งที่ **ไม่ใช่** DOA action ในใบนี้ (ตัดสินใจไว้ชัด ห้ามเผลอเพิ่ม)

| ไม่ใช่ action | เหตุผล |
|---|---|
| **การเพิกถอนสิทธิ์ (T-11)** | **เป็นผลอัตโนมัติของรอบที่อนุมัติแล้ว ไม่ใช่การตัดสินใจใหม่** — ถ้าใส่ชั้นอนุมัติคั่นตรงนี้ **ความล่าช้าจะกลายเป็นช่องโหว่ความปลอดภัยโดยตรง** (BR-06: เลยกำหนดแล้วยังค้าง = เหตุการณ์ความปลอดภัย) · การอนุมัติ "ว่าคนนี้จะออก" เกิดไปแล้วที่ A-1/A-2 |
| **การปิดงานแต่ละใบใน checklist** | เป็นงาน **SOW ของ Operation Process** — OP มีกลไกของตัวเอง (BR-02) |
| **รอบเข้างานทั้งวงจร** | scope note ระบุ DOA เฉพาะ **"อนุมัติการออก"** — การรับเข้าทำงานถูกอนุมัติไปแล้วที่ **Recruit (W5)** ก่อนถึง feature นี้ · **ไม่ยัด DOA เข้าจุดที่ไม่มีการอนุมัติ** (SKILL.md §Trigger Rule ข้อห้าม 4) |
| **การมอบฉันทะผู้อนุมัติของผู้ที่กำลังจะออก (S-57)** | **DOA Engine มี delegate อยู่แล้ว** (`catalog §0`) — feature นี้ **ตรวจและสร้างงาน** ให้คนไปทำที่ DOA เท่านั้น (BR-32 · FN-77 · FN-78) |

## §3 Matrix ที่จะไปตั้งค่า (กรอกลงหน้า DOA กลางได้ตรงช่อง)

| set | ผูกกับ action | amount_from | amount_to | departments | chainMode | steps[roles] |
|---|---|---|---|---|---|---|
| **1** | `offboard_approve_voluntary` | `0` บาท | `null` (ไม่จำกัด) | `merged` | `sequential` | **step 1:** `role-supervisor-direct` `[DEFAULT — รอยืนยัน]` — หัวหน้าโดยตรงของผู้ที่จะออก · **step 2:** `role-mgr-hr` `[DEFAULT — รอยืนยัน]` — ผู้จัดการฝ่ายบุคคล |
| **2** ⭐ | `offboard_approve_involuntary` | `0` บาท | `null` (ไม่จำกัด) | `merged` | `sequential` | **step 1:** `role-supervisor-direct` `[DEFAULT — รอยืนยัน]` · **step 2:** `role-mgr-hr` `[DEFAULT — รอยืนยัน]` · **step 3:** `role-exec-dept` `[DEFAULT — รอยืนยัน]` — ผู้บริหาร/ผู้จัดการฝ่ายต้นสังกัด |

- **`amount_to: null` ในชุดสุดท้ายของทั้งสอง set ✅ (G4)** — ไม่มีรอบไหนตกขอบไม่มีคนเซ็น
- **ไม่มีรู/ไม่ทับ ✅ (G3)** — แต่ละ action มีชุดเดียวที่ครอบ `0 → ไม่จำกัด`
- **หน่วยเงิน:** บาท — แต่ feature นี้ **ไม่ส่งค่าเงินเข้า resolve เลย** (BR-18) · ช่อง `amount` มีไว้ให้ record ถูก schema ของ DOA เท่านั้น

### §3.1 ⭐ ทำไมจุดตัดถึงเป็น **action** ไม่ใช่ช่วง `amount`

จุดตัดของ feature นี้คือ **"ประเภทของการออกจากงาน"** ซึ่งเป็น **ค่า enum ทางธุรกิจ ไม่ใช่ปริมาณ** — ต่างจาก PR/PO ที่จุดตัดเป็นจำนวนเงินจริง และต่างจาก OT ที่จุดตัดเป็นชั่วโมงเทียบเพดานจาก HR Configuration

- ช่อง `amount` ของ DOA record เป็น **ปริมาณต่อเนื่อง** — ยัด enum ลงไปไม่ได้โดยไม่บิดความหมาย (เช่น สมมติ "ลาออก = 0, เลิกจ้าง = 1") ซึ่งจะทำให้ **matrix อ่านไม่รู้เรื่องสำหรับคนที่ไป set ที่หน้า DOA กลาง** และพังทันทีที่เพิ่มเหตุผลการออกใหม่
- วิธีที่ประกาศไว้ในใบนี้: feature **ตัดสิน `approval_action_id` จาก `termination_reason` + `is_immediate_exit` ตอนกดส่งอนุมัติ** → ส่ง action นั้นเข้า `GET /doa/resolve` → **สายอนุมัติยังมาจาก DOA 100%** และ **การจับคู่เหตุผล→สาย เป็นข้อมูลใน DOA ไม่ใช่ logic ในหน้าจอ**
- **สิ่งที่ห้ามเด็ดขาด:** เขียน `if (reason === 'เลิกจ้าง') chain = [...]` หรือตารางเหตุผล→ผู้เซ็น ลงในไฟล์ feature — **นั่นคือ hardcoded approval chain = governance Hard Stop** (FN-29 พิสูจน์ว่าไม่มี)
- **ทางเลือกที่ต้องให้ Architect เคาะ (OQ-DOA-03):** ถ้า DOA Engine รองรับ **มิติจุดตัดที่ไม่ใช่เงิน** (`threshold_key: termination_kind`) ให้ยุบเหลือ **1 action 2 set** ได้ — **แต่ไม่ว่าทางไหนก็ห้ามเอา enum ไปใส่เป็นขอบของช่วง `amount`**

### §3.2 กติกาอื่นของสาย

- **step 1 = "หัวหน้าโดยตรง"** ต้อง resolve จากสายบังคับบัญชาใน **Employee Master ณ เวลาส่งอนุมัติ** — ไม่ใช่ role คงที่ (OQ-DOA-01)
- **มติ 2026-08-17 (บังคับ):** ทุก slot ต้องเลือก **"คน" ในตำแหน่ง** — แสดง **avatar + ตำแหน่ง + ชื่อ** ไม่ใช่ role id ลอย (FN-24)
- **SoD (BR-DOA-04 · BR-09 · FN-28):** ผู้สร้างรอบเซ็นอนุมัติรอบของตัวเองไม่ได้ · ⭐ **เคสเฉพาะที่ feature นี้ต้องระวังเป็นพิเศษ: รอบออกงานของ "หัวหน้า" เอง** — คนที่จะออกอาจเป็นผู้ถือ slot step 1 ของสายตัวเอง หรือเป็นผู้บังคับบัญชาของผู้ถือ slot → **engine ต้องขึ้นไปหาผู้บังคับบัญชาเหนือขึ้นไป** `[DEFAULT — รอยืนยัน]` (OQ-DOA-02)
- ⭐ **ผู้ที่กำลังจะออกต้องไม่ถูก resolve เป็นผู้อนุมัติของรอบใด ๆ ตั้งแต่วันที่รอบถูกอนุมัติ** — ผูกกับ S-57/BR-32 (งานอนุมัติที่ค้างของเขาต้องถูกมอบหมายต่อ) — **การมอบฉันทะทำที่ DOA ไม่ทำที่นี่**
- **จำนวน slot บนหน้าจอ = จำนวน step ที่ resolve ได้จริง (2 หรือ 3)** — html **ห้ามวาด slot ตายตัว** (FN-24)

## §4 Field Contract สำหรับ FRD (entity `offboard_case`)

| field | ชนิด | nullable | หมายเหตุ |
|---|---|---|---|
| `approval_required` | bool | ✗ | **มาจาก DOA entry — ไม่ใช่ค่าคงที่ในตาราง** |
| `approval_action_id` | string | ✓ (Phase 1) | `offboard_approve_voluntary` / `offboard_approve_involuntary` — **ตัดสินตอนกดส่ง จาก `termination_reason` + `is_immediate_exit`** |
| `approval_status` | enum | ✗ | `draft` · `pending_approval` · `approved` · `rejected` · `cancelled` — map กับสถานะไทยใน PREBRIEF §5.2 |
| `termination_reason` | enum | ✗ | ลาออก · ครบสัญญา · เลิกจ้าง · เกษียณ · ไม่ผ่านทดลองงาน — **ธงที่เลือกสาย** (PREBRIEF §3.1) · **Confidential (masking)** |
| `is_immediate_exit` | bool | ✗ | **ธงที่เลือกสาย + ธงที่ย่นเวลาเพิกถอน** (BR-05) |
| `doa_entry_ref` | string | ✓ (Phase 1) | FK ไปทะเบียน DOA |
| `approver_role` | string | ✓ | role ที่ต้องเซ็นในขั้นปัจจุบัน — **resolve จาก DOA ห้าม hardcode** |
| `approved_by` · `approved_at` | employee ref · timestamp | ✓ | ผู้เซ็นจริงในขั้นสุดท้าย |
| `approval_chain` | jsonb | ✓ | **snapshot ของสายที่ resolve ตอนกดส่ง · append-only** (BR-DOA-02) · **จำนวน step 2 หรือ 3** |
| `reject_reason` · `cancel_reason` | text | ✓ | **บังคับเมื่อไม่อนุมัติ / ยกเลิก** (FN-27 · FN-48) |
| **`revocation_due_at`** ⭐ | timestamp | ✗ | **ตั้งตอน approve** — สิ้นวัน `last_working_day` หรือ **เวลาที่อนุมัติครบสาย เมื่อ `is_immediate_exit = true`** (BR-05) |
| `cancellation_of_ref` | ref | ✓ | ใช้กับ A-3 — ชี้รอบเดิมที่ถูกยกเลิก (append-only · ไม่ลบของเดิม) |
| `config_version_ids` | jsonb | ✗ | `{holiday_calendar, period_rule, employment_term: null}` — **`employment_term` เป็น `null` ได้** (OQ-STD-OB3) |

**Business Rules ที่ FRD ต้องมีเสมอ (จาก SKILL §FRD Injection · ปรับให้เข้ากับ feature นี้):**

| BR | เนื้อหาที่ใช้กับ On/Offboard |
|---|---|
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะสถานะ `ร่าง` — ตรงกับ PREBRIEF §5.2 T-7 |
| BR-DOA-02 | สายอนุมัติ resolve ตอนกดส่ง แล้ว **freeze ลง `approval_chain`** — แก้ DOA ทีหลังไม่กระทบรอบที่ส่งไปแล้ว (BR-08) |
| BR-DOA-03 | reject → "ไม่อนุมัติ" · ประวัติ **append-only** (BR-19) · แก้แล้วส่งใหม่ = **re-resolve สายใหม่** (T-10) |
| BR-DOA-04 | **ผู้สร้างรอบเซ็นอนุมัติรอบของตัวเองไม่ได้** (SoD · BR-09) |
| **BR-DOA-05** *(ปรับ: จุดตัดไม่ใช่เงิน)* | **แก้ `termination_reason` หรือ `is_immediate_exit` หลังส่งอนุมัติ → ต้อง re-resolve สาย** — ชั้นของสายเปลี่ยนได้ (แทนการ re-resolve ตามยอดเงิน) |
| **BR-DOA-06** *(เพิ่มเฉพาะ feature นี้)* | **ห้ามอนุมัติเมื่อ `last_working_day` ตกในงวดที่ปิดแล้ว** — ตรวจซ้ำ ณ วินาทีอนุมัติ (BR-10 · P-7 · FN-21) |
| **BR-DOA-07** ⭐ *(เพิ่มเฉพาะ feature นี้)* | **การอนุมัติคือสิ่งที่ปลดล็อกทั้งการเดิน checklist ปิดสิทธิ์และการตั้งเวลาเพิกถอน** — ก่อนอนุมัติ **ห้ามมีคำขอเพิกถอนใด ๆ ออกไปยัง Roles & Permissions** (BR-07 · FN-25) |
| **BR-DOA-08** ⭐ *(เพิ่มเฉพาะ feature นี้)* | **การยกเลิกรอบที่เพิกถอนสิทธิ์ไปแล้ว ต้องผ่าน A-3 และผลคือ "คำขอคืนสิทธิ์" ใหม่ ไม่ใช่การย้อนสถานะ** (BR-14 · FN-50) |
| **BR-DOA-09** *(เพิ่มเฉพาะ feature นี้)* | **ผู้ที่กำลังจะออกต้องถูกกันออกจากการเป็นผู้อนุมัติของรอบอื่นตั้งแต่วันที่รอบถูกอนุมัติ** — งานอนุมัติที่เขาค้างอยู่ต้องถูกมอบหมายต่อผ่าน **delegate ของ DOA** ก่อนปิดรอบ (BR-32 · S-57) |

## §5 UI Contract สำหรับ HTML (html-generator-v9 Sync Read)

| ส่วน | รายละเอียดสำหรับ On/Offboard |
|---|---|
| ปุ่ม **ส่งอนุมัติ** | อยู่ที่ **drawer › ภาพรวม** ของรอบออกงาน (ไม่ใช่ wizard — archetype master ไม่ใช่ Pattern Q) · แสดงเฉพาะสถานะ "ร่าง" · disabled จนกว่า validate ผ่าน (เหตุผล · วันแจ้ง · วันสุดท้าย · ไม่ชนงวดปิด) |
| **แสดงสายที่จะได้ก่อนกดส่ง** | เมื่อเลือก `termination_reason` / ติ๊ก "ออกทันที" → บอกว่า **"สายอนุมัติจะมี N ขั้น"** พร้อมเหตุผล (FN-19 · FN-37) — **โดยที่ N มาจากผลของ `resolve` ไม่ใช่ตัวเลขในโค้ด** |
| **slot picker** (มติ 2026-08-17) | **จำนวน slot = ที่ DOA resolve คืนมา ห้ามวาดตายตัว** · แต่ละ slot เลือก **"คน" ในตำแหน่ง** แสดง **avatar → ชื่อ → ตำแหน่ง · แผนก** (#102) · **ห้ามแสดง role id ลอย** (FN-24) |
| Badge สถานะ | ร่าง / รออนุมัติ / อนุมัติแล้ว / **เพิกถอนแล้ว** / ปิดรอบแล้ว / ไม่อนุมัติ / ยกเลิก — `.pill` 22px **คำเดียว** (#38.1) · CI Warm Light (ห้ามม่วง/น้ำเงิน) |
| **Approval Timeline** | อยู่ใน **drawer › ภาพรวม** (ไม่มี tab "ลายเซ็น" เพราะไม่มีเอกสาร) — ไล่ทีละขั้น: ตำแหน่ง → ชื่อผู้เซ็น → เวลา → สถานะ · **เคสไม่สมัครใจต้องเห็นครบ 3 ชั้น** |
| ปุ่ม **อนุมัติ / ไม่อนุมัติ** | แสดงเฉพาะเจ้าของ slot ปัจจุบัน · **ไม่อนุมัติบังคับใส่เหตุผล** (FN-27) |
| ปุ่ม **ยกเลิกรอบ** | ทุกสถานะก่อนปิดรอบ · บังคับเหตุผล · **ถ้าเพิกถอนไปแล้วต้องเตือนชัดว่าจะเกิด "คำขอคืนสิทธิ์" ไม่ใช่การย้อนสถานะ** (FN-50) |
| ⭐ **ไม่มีปุ่มอนุมัติการเพิกถอน** | การเพิกถอนไม่ใช่ DOA action (§2.1) — แผงเพิกถอนมีแต่ปุ่ม **"เพิกถอนสิทธิ์ทั้งหมด"** (ส่งคำขอ) และ **"ส่งซ้ำ"** เท่านั้น |
| Hook **My Approval** | รอบที่ `pending_approval` ต้องโผล่ในกล่อง My Approval ของผู้ถือ slot |
| mock ที่อนุญาต | `// TODO: DOA engine — resolve จาก DOA entry ของ feature นี้ (ดู DOA_BRIEF.md)` + `MOCK_DOA_RESOLVED = { voluntary: {action:'offboard_approve_voluntary', chainMode:'sequential', steps:[{roles:['role-supervisor-direct']},{roles:['role-mgr-hr']}]}, involuntary: {action:'offboard_approve_involuntary', chainMode:'sequential', steps:[{roles:['role-supervisor-direct']},{roles:['role-mgr-hr']},{roles:['role-exec-dept']}]} }` — **เลือกก้อนไหนขึ้นกับ `termination_reason` + `is_immediate_exit`** |
| **ข้อห้าม** | ❌ `const APPROVAL_CHAIN = […]` ในไฟล์ feature · ❌ ตารางเหตุผลการออก → ผู้เซ็น ในหน้าจอหรือโค้ด · ❌ วาด slot 2 หรือ 3 ช่องตายตัว · ❌ ตัวเลขเงินทุกชนิด (BR-18) · ❌ ชั้นอนุมัติคั่นก่อนการเพิกถอน |

## §6 Wire Checklist (pending → wired)

- [ ] เอา §3 ไปสร้าง **2 entry** ที่หน้า **DOA กลาง (Policy Center)** — `offboard_approve_voluntary` (2 steps) และ `offboard_approve_involuntary` (3 steps) · ทั้งคู่ `amount_from 0 / amount_to null` · `merged` · `sequential`
- [ ] ผูก **A-3 `offboard_approve_cancellation`** ให้ยืม matrix ของ action เดิมของรอบนั้น (ไม่สร้าง entry ที่ 3)
- [ ] **ยืนยัน `role-*` id จริง** กับ master 14 roles ก่อน set (ตอนนี้ทุกตัวเป็น `[DEFAULT — รอยืนยัน]`) — โดยเฉพาะวิธี resolve "หัวหน้าโดยตรง" จาก Employee Master
- [ ] **เคาะ OQ-DOA-05** — `approval_scope` = `policy_approve` ถูกต้องหรือไม่ (feature นี้ไม่มีเอกสาร/ลายเซ็น จึงไม่ใช่ `document_sign`)
- [ ] **เคาะ OQ-DOA-03** — DOA รองรับมิติจุดตัดที่ไม่ใช่เงิน (`threshold_key: termination_kind`) หรือไม่ · ถ้ารองรับให้ยุบเหลือ 1 action 2 set · **ไม่ว่าทางไหนก็ห้ามเอา enum ไปใส่เป็นขอบของช่วง `amount`**
- [ ] dev wire `GET /doa/resolve` ที่ **ปุ่มส่งอนุมัติ** (ส่ง `action_id` ที่เลือกจาก `termination_reason` + `is_immediate_exit`) + จุดอนุมัติ/ปฏิเสธ/ยกเลิกรอบ (A-1…A-3)
- [ ] snapshot `approval_chain` + `config_version_ids` ตอนส่ง (freeze) และ **re-resolve เมื่อแก้เหตุผล/ธงออกทันทีแล้วส่งใหม่** (BR-DOA-05)
- [ ] เพิ่ม guard **BR-DOA-06** (งวดปิด) · **BR-DOA-07** (ห้ามมีคำขอเพิกถอนก่อนอนุมัติ) · **BR-DOA-08** (ยกเลิกหลังเพิกถอน = คำขอคืนสิทธิ์) · **BR-DOA-09** (กันผู้ที่จะออกจากการเป็นผู้อนุมัติ + มอบหมายงานอนุมัติค้างผ่าน delegate ของ DOA)
- [ ] **ห้ามทำ delegation / expiry / reminder เอง** — DOA Engine มีให้แล้ว (`catalog §0`) · S-57 คือการ **ตรวจและสร้างงาน** ไม่ใช่การ implement delegation
- [ ] ตรวจว่ารอบโผล่ใน **My Approval** จริง และ **`doa_pending`/`doa_result` แจ้งเตือนอัตโนมัติ** — **`NTF_BRIEF` ของ feature นี้ต้องไม่ประกาศซ้ำ**
- [ ] **ตรวจว่า `CSQ_BRIEF` ไม่มี `dc`** — DC ระดับเอกสารเป็นของ DOA engine (register 422 ถ้าซ้ำ)
- [ ] `wire_status: pending → wired` · อัพเดต `FEATURE_REGISTRY.md` · แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q

## §7 Open Questions

| # | ประเด็น | ค่าที่ใช้ไปก่อน | เจ้าภาพ |
|---|---|---|---|
| OQ-DOA-01 | **`role-*` id จริง** ของ "หัวหน้าโดยตรง" · "ผจก.HR" · "ผู้บริหารต้นสังกัด" — master 14 roles ไม่มีในเวิร์กสเปซ · "หัวหน้าโดยตรง" ต้อง dynamic resolve จาก Employee Master | `role-supervisor-direct` · `role-mgr-hr` · `role-exec-dept` `[DEFAULT — รอยืนยัน]` | Architect / Policy Center |
| OQ-DOA-02 ⭐ | **SoD เมื่อคนที่จะออกคือหัวหน้า** — เขาอาจเป็น step 1 ของสายตัวเอง หรือเป็นผู้บังคับบัญชาของผู้ถือ slot | **ขึ้นไปหาผู้บังคับบัญชาเหนือขึ้นไป** `[DEFAULT — รอยืนยัน]` | Strike / Policy Center |
| **OQ-DOA-03** ⭐ | **DOA Engine รองรับมิติจุดตัดที่ไม่ใช่เงินหรือไม่** (`threshold_key: termination_kind`) | **ประกาศเป็น 2 action แยก** `[DEFAULT — รอยืนยัน]` — ปลอดภัยที่สุด (ดู §3.1) · **คู่ขนานกับ OQ-DOA-03 ของ F-HR-OT ที่ยกประเด็นเดียวกันด้วยธง `over_cap`** | Architect (DOA Engine) |
| OQ-DOA-04 | **การยกเลิกรอบ (A-3) ต้องผ่านสายเดิมทั้งสายหรือแค่ผู้อนุมัติชั้นสุดท้าย** | **ผ่านสายเดิมทั้งสาย** `[ASSUMED]` (OQ-OB-11 · การถอนการตัดสินใจควรผ่านคนชุดเดียวกับที่ตัดสินใจ) | Strike |
| **OQ-DOA-05** | **`approval_scope` ควรเป็น `policy_approve` ใช่หรือไม่** — feature นี้ไม่มีเอกสาร/ช่องลายเซ็น จึงไม่เข้า `document_sign` และไม่ใช่ `budget_approve` | **`policy_approve`** `[DEFAULT — รอยืนยัน]` | Architect / Policy Center |
| OQ-DOA-06 | **รอบเข้างานควรมีการอนุมัติด้วยหรือไม่** (บาง ERP ให้ hiring manager review) | **ไม่มี** — scope note ระบุ DOA เฉพาะการออก · การรับเข้าอนุมัติแล้วที่ Recruit (W5) | Strike |

## Quality Gate (self-check)

| # | เช็ค | ผล |
|---|---|---|
| G1 | ทุก role เป็น `role-*` (ไม่มีชื่อตำแหน่งลอย) | ✅ 3 ตัว · ทุกตัวติด `[DEFAULT — รอยืนยัน]` |
| G2 | ทุก set มี `amount_from` และ `amount_to` ครบ | ✅ 2 set |
| G3 | ช่วงต่อเนื่อง ไม่ทับ ไม่มีรู | ✅ แต่ละ action มีชุดเดียวครอบ `0 → null` |
| G4 | set สุดท้าย `amount_to: null` | ✅ ทั้งสอง set |
| G5 | `approval_scope` เป็น 1 ใน 3 ค่าที่มีจริง | ✅ **`policy_approve`** (พร้อมเหตุผลใน §1 + OQ-DOA-05) |
| G6 | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` ครบ | ✅ role ทุกตัว · `approval_scope` · OQ-DOA-03 |
| G7 | ไม่มีสายอนุมัติ hardcode หลุดเข้า FRD/HTML | ✅ §3.1 · §5 ข้อห้าม · **FN-29 เป็น FN ที่พิสูจน์ข้อนี้ด้วยตา** |
