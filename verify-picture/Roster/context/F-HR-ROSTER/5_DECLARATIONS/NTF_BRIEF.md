# NTF_BRIEF — F-HR-ROSTER · Shift & Roster (จัดกะ)

> ออกโดย `ntf-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-29
> Input: `briefs/W2/F-HR-ROSTER/PREBRIEF.md` **v1.1 §12 (authoritative)** + §5.1/§5.2 state machine + §4 BR · `LANE_BRIEF.md` (chip) · `_lane/DECL.json` (`source: prebrief§12` ทุกท่อ)
> **DIVERGENCE: —** (chip `ntf ✓` = detect §12 = `POOL.json` = `CHECKLIST.md` = `FEATURE_LIST_ALL.md` = `CONTEXT_PACK/HR.md` แถว Shift & Roster → ✓ "เผยแพร่ตาราง/สลับกะ")
> หมายเหตุ: `f-notify.html` (EVENT_GROUPS catalog) **ไม่มีในเวิร์กสเปซนี้** — เทียบชนชื่อ event แบบ Sync Read ไม่ได้ · ยึด naming `{feature}_{event}` snake_case จาก SKILL.md · ชื่อที่เสนอติด `[DEFAULT — รอยืนยัน]` และต้อง cross-check กับ catalog จริงก่อน register
> **ยิงผ่าน ENG-NOTIFY เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไขใน feature**
> ⭐ **feature นี้ไม่มี DOA เลย** จึง **ไม่มี `doa_pending` / `doa_result` / `doa_escalate` ให้ตัดออกตั้งแต่ต้น** — ต่างจากพี่น้อง Leave/OT ในเวฟเดียวกัน (ดู `NOT_NEEDED.md`)

## §1 Identity

| | |
|---|---|
| feature_code | `F-HR-ROSTER` · Shift & Roster · จัดกะ |
| module | HR |
| archetype | **P-planner** (ไม่ใช่เอกสาร — ไม่มีเลขที่เอกสารในข้อความแจ้งเตือน) |
| event prefix | `roster_` |
| version | 1.0 (2026-08-29) |
| จำนวน event ที่ประกาศ | **6** (ธุรกิจล้วน — ตรงกับ N1–N6 ใน PREBRIEF §12) |

## §2 Declared Events

| # | Event ID | Trigger (อ้าง PREBRIEF · จะแทนที่ด้วย FRD `03_LOGIC` ที่ S5) | ผู้รับ | ข้อความ template (ไทย) | Channel default | ปิดได้ |
|---|---|---|---|---|---|---|
| **N1** | `roster_published` | §5.1 **T-3** `ร่าง → เผยแพร่แล้ว` (S-08 · FN-23) | **พนักงานทุกคนที่มีกะอย่างน้อย 1 ช่องในตารางนั้น** + ผู้จัดตาราง (สำเนา) | ตารางกะเดือน **{period_month}** ของ {scope_team} เผยแพร่แล้ว — คุณมีเวร {shift_count} วัน · กดดูตารางของคุณ | **in-app + email** | ✗ **บังคับ** — ตารางเวรคือสิ่งที่คนต้องรู้เพื่อมาทำงาน ปิดไม่ได้ |
| **N2** ⭐ | `roster_shift_changed` | §5.1 **T-4** `เผยแพร่แล้ว → ถูกแทนที่` + published เวอร์ชันใหม่ (S-11 · S-39 · FN-26 · FN-29 · **BR-17**) | **เฉพาะพนักงานที่กะของตัวเองเปลี่ยนจริงในเวอร์ชันใหม่** (ไม่ใช่ทุกคนในตาราง) | กะของคุณเปลี่ยน — {change_count} วันในเดือน **{period_month}** · {sample_change} · เหตุผล: {publish_note} | **in-app + email** | ✗ **บังคับ** |
| **N3** | `roster_swap_requested` | §5.2 **W-1** `(ไม่มี) → ยื่นคำขอ` (S-20 · FN-31) | **คู่สลับ** (ผู้ถูกขอ) | {requester_name} ขอสลับเวรกับคุณ — {requester_work_date} {requester_shift_name} ⇄ {counterpart_work_date} {counterpart_shift_name} · เหตุผล: {request_reason} | in-app | ✓ |
| **N4** | `roster_swap_accepted` | §5.2 **W-2** `ยื่นคำขอ → รอหัวหน้ายืนยัน` (S-20 · FN-34) | **หัวหน้าสายบังคับบัญชาของผู้ขอ** (ผู้มีสิทธิ์ยืนยัน · resolve จาก Policy Center **ไม่ใช่ DOA**) + ผู้ขอ (สำเนา) | {counterpart_name} ตอบรับคำขอสลับเวรของ {requester_name} แล้ว — รอคุณยืนยัน · ผลตรวจ: {validation_summary} | in-app | ✓ |
| **N5** | `roster_swap_decided` | §5.2 **W-3** `รอหัวหน้ายืนยัน → ยืนยันแล้ว` (S-20 · FN-37) **และ** **W-4** `→ ถูกปฏิเสธ` ทั้งกรณีคู่สลับปฏิเสธและหัวหน้าปฏิเสธ (S-21 · S-22 · FN-34 · FN-39) | **ผู้ขอ + คู่สลับ** | คำขอสลับเวร {requester_work_date} — **{decision}**{reason_suffix}{effective_suffix} | **in-app + email** | ✗ **บังคับ** |
| **N6** | `roster_swap_expired` | §5.2 **W-6** `ยื่นคำขอ / รอหัวหน้ายืนยัน → หมดอายุ` (S-24 · FN-41 · BR-29) | **ผู้ขอ + คู่สลับ** (+ หัวหน้าที่ค้างงาน) | คำขอสลับเวร {requester_work_date} หมดอายุแล้ว — ถึงวันของกะโดยยังไม่มีข้อสรุป · ตารางไม่เปลี่ยน | in-app | ✓ |

**Payload ร่วมของทุก event (ref + ตัวแปรในข้อความ):**
`ref` = `roster_version_id` (N1 · N2) หรือ `swap_request_id` (N3…N6) — **soft reference ทุกกรณี** · `company_id` · `period_month` · `employee_id` ของผู้รับ · **ไม่มีตัวเลขเงิน ไม่มีข้อมูลชั้น Restricted ดิบ** (ชื่อคนที่ปรากฏในข้อความเป็น snapshot ที่ผู้รับมีสิทธิ์เห็นอยู่แล้วตามขอบเขตของ Policy Center)

**หมายเหตุการเลือกช่องทาง:** ทั้ง 6 event ระบุเพียง **default** — **ช่องทางจริงเป็นของ user preference + config กลางของ ENG-NOTIFY** · feature **ห้ามเช็ค preference เอง ห้ามเขียน "ส่ง email/LINE" ในตรรกะของตัวเอง** · ค่า default in-app + email มาจากตาราง default ของ `gate-policy.md` `[ASSUMED]`

## §3 Event ที่จงใจ **ไม่ประกาศ** (ห้ามเงียบ)

| ไม่ประกาศ | เหตุผล |
|---|---|
| **`doa_pending` · `doa_result` · `doa_escalate`** | **ไม่มีอะไรให้ตัดออก — feature นี้ไม่มีสายอนุมัติเลย** · การยืนยันคำขอสลับกะเป็นสิทธิ์ตามสายบังคับบัญชาจาก Policy Center ไม่ใช่การ resolve สายอนุมัติจากทะเบียนกลาง (ดู `NOT_NEEDED.md`) |
| **การรับทราบกะของพนักงาน (S-53 · FN-67)** | เป็น **ส่วนขยายของ N1/N2** ไม่ใช่ event ใหม่ — คนที่ต้องรู้คือหัวหน้า ซึ่งเห็นตัวนับ "ยังไม่รับทราบ" บนหน้าจออยู่แล้ว (pull ไม่ใช่ push) · **BR-33** ระบุว่าการรับทราบไม่มีผลต่อตาราง จึงไม่ใช่เหตุการณ์ทางธุรกิจที่ต้องกระจาย `[AI-DRAFT]` |
| **การเตือน "ยังมีวันที่ยังไม่จัดกะก่อนถึงวัน"** (แนวคิดที่ `LANE_BRIEF §Declarations` เสนอไว้) | **ยังประกาศไม่ได้** — ต้องมีเกณฑ์ "ก่อนถึงวันกี่วัน" ซึ่งเป็นค่าตั้งได้ที่ **HR Configuration ยังไม่เผยแพร่** (`shift_rule.freeze_days` — **OQ-R15** ชุดเดียวกับ **OQ-STD-R6**) · **ประกาศตอนนี้ = ต้องเดาตัวเลข ซึ่งผิด P-8** → รอ Strike เคาะแล้วค่อย **append ในใบนี้** (ห้ามออกใบใหม่) |
| การบันทึกร่าง · การทิ้งร่าง · การแก้ช่องระหว่างร่าง (S-03 · S-05 · S-09 · S-10) | ตารางร่าง **ไม่มีใครนอกทีมเห็น** (BR-18) — ยังไม่มีผลกับใคร · ยิง = noise ทุกครั้งที่ลากกะหนึ่งช่อง |
| การรับทราบคำเตือนตอนเผยแพร่ (S-15) | เป็นการบันทึก audit ภายใน ไม่ใช่เหตุการณ์ที่คนอื่นต้องรู้ |
| ข้อขัดแย้งที่ตรวจพบ (S-16…S-19 · S-30…S-32 · S-55) | เป็น **การตรวจบนหน้าจอ (validation)** ไม่ใช่การกระจายข่าว — ผู้จัดตารางเห็นทันทีในแผงข้อขัดแย้ง |
| การล็อกตารางเมื่องวดปิด (S-13 · T-5) | **ต้นทางเป็นผู้ประกาศ** — `hrconfig.period_closed` เป็น event ของ **HR Configuration** · ประกาศที่นี่ = ประกาศซ้ำของคนอื่น |
| `hrconfig.*` · `attendance.*` · `ot.*` · `leave.*` | **feature ต้นทางเป็นเจ้าของ** — Roster เป็นผู้ฟัง ไม่ใช่ผู้ประกาศ |
| การที่ Attendance/OT อ่าน read model (S-35 · S-38) | เป็น **pull** ไม่ใช่ push · การล้าง cache ใช้ event ของ **ท่อ CSQ** ที่ประกาศไว้ใน `CSQ_BRIEF.md` (`roster.published` · `roster.republished`) ไม่ใช่การแจ้งเตือนคน |

## §4 เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)

- **กลุ่มที่มีอยู่เดิม "เอกสารธุรกรรม" (`doc_status`) — ใช้ไม่ได้** เพราะ feature นี้ไม่ใช่เอกสาร (ไม่มีเลขที่ · ไม่มีสถานะเอกสาร)
- **เสนอกลุ่มใหม่: "ตารางกะ/เวร" (`roster`)** `[DEFAULT — รอยืนยัน]` — สมาชิกตั้งต้น 6 event ข้างบน · กลุ่มนี้จะถูกใช้ซ้ำโดย **ESS Portal (W6)** เมื่อแสดง "เวรของฉัน"
- **ผู้รับแบบ "ทุกคนที่มีกะในตาราง" (N1) เป็น recipient resolver แบบใหม่** — ไม่ใช่ role คงที่ และไม่ใช่ "ผู้เกี่ยวข้องกับเอกสาร" · ต้อง resolve จาก **รายชื่อ employee_id ที่มีอย่างน้อย 1 cell ในเวอร์ชันที่เผยแพร่** → แจ้ง F-NOTIFY ให้รองรับ `[DEFAULT — รอยืนยัน]`

## §5 Dev wiring note

- จุดเรียก: `ENG-NOTIFY.emit(event_id, {ref, vars})` ที่ **transition จริง** ตาม §2 — **ห้ามเช็ค preference เอง ห้ามเลือกช่องทางเอง**
- **N2 ต้องคำนวณ "ใครกะเปลี่ยน" จาก diff ระหว่างเวอร์ชันเก่ากับใหม่ก่อน emit** — emit ทีละคนพร้อมจำนวนวันที่เปลี่ยนของคนนั้น · **ห้าม emit ให้ทุกคนในตาราง** (BR-17 — แจ้งทุกคนทุกครั้ง = คนเลิกอ่าน แล้วจะพลาดครั้งที่สำคัญจริง)
- **N1 กับ N2 ต้องไม่ยิงพร้อมกันในการกระทำเดียว** — การเผยแพร่ครั้งแรกของเดือน = N1 · การเผยแพร่ซ้ำ = N2 เท่านั้น
- **N5 ยิงครั้งเดียวต่อคำขอ** ไม่ว่าจบด้วยยืนยันหรือปฏิเสธ (ค่า `{decision}` เป็นตัวแยก) — กันยิงสองใบสำหรับเหตุการณ์เดียว
- ข้อความ template ทั้งหมด **อยู่ในใบประกาศนี้ ไม่ฝังในโค้ดของ feature**
- ทุก event มี `ref` เป็น soft reference — **ไม่มี event ไหนเป็น system broadcast**
