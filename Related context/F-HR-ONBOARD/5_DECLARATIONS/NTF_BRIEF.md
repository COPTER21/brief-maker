# NTF_BRIEF — F-HR-ONBOARD · On/Offboard (เข้าออกงาน)

> ออกโดย `ntf-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-29
> Input: `briefs/W3/F-HR-ONBOARD/PREBRIEF.md` v1.1 §12 (**authoritative**) + §5 state machine + §4 BR · `LANE_BRIEF.md` (chip) · `_lane/DECL.json`
> **DIVERGENCE: —** (chip `ntf ✓` = detect §12 = `CONTEXT_PACK/HR.md` แถว On/Offboard → ✓ "งาน checklist/วันเริ่ม-ออก")
> หมายเหตุ: `f-notify.html` (EVENT_GROUPS catalog) **ไม่มีในเวิร์กสเปซนี้** — Sync Read เทียบชนชื่อ event ไม่ได้ · ยึด naming `{feature}_{event}` snake_case จาก SKILL.md · ชื่อที่เสนอติด `[DEFAULT — รอยืนยัน]` และต้อง cross-check กับ catalog จริงก่อน register
> **ยิงผ่าน ENG-NOTIFY เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไขใน feature · DOA events มาอัตโนมัติ ไม่อยู่ในใบนี้**

## §1 Identity

| | |
|---|---|
| feature_code | `F-HR-ONBOARD` · On/Offboard · เข้าออกงาน |
| module | HR |
| archetype | master + checklist(OP) |
| event prefix | `onb_` (รอบเข้างาน) · `ofb_` (รอบออกงาน) |
| version | 1.0 (2026-08-29) |
| จำนวน event ที่ประกาศ | **9** (ธุรกิจล้วน — ไม่มี event ของ DOA และไม่มี event ของ Operation Process) |

## §2 Declared Events

| Event ID | Trigger (อ้าง PREBRIEF · จะแทนที่ด้วย FRD §03_LOGIC ที่ S5) | ผู้รับ | ข้อความ template (ไทย) | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| `onb_case_started` | §5.1 **T-1** `ร่าง → รอวันเริ่มงาน` — ชุดงานถูกสร้างและมอบหมายแล้ว (S-01 · FN-01 · FN-02) | **ผู้รับผิดชอบทุกงานในชุด** + หัวหน้าของผู้เข้าใหม่ | รอบเข้างานของ **{employee_name}** เริ่มแล้ว — วันเริ่มงาน {start_date} · คุณมี {my_task_count} งานที่ต้องทำ กำหนดแรก {first_due_date} | in-app | ✓ |
| `onb_start_date_changed` | แก้ `start_date` แล้วกำหนดเสร็จถูกคำนวณใหม่ (S-07 · BR-22 · FN-11) | **ผู้รับผิดชอบทุกงานที่กำหนดเปลี่ยน** + หัวหน้า | รอบเข้างานของ **{employee_name}** เลื่อนวันเริ่มงานเป็น {start_date} — กำหนดเสร็จของ {affected_task_count} งานถูกปรับแล้ว | in-app + email | ✓ |
| **`access_request_failed`** ⭐ | ผลตอบกลับจาก Roles & Permissions = **ล้มเหลว** ทั้งขาเปิด (S-04 · FN-07) และ **ขาเพิกถอน** (S-29 · FN-40) | **ผู้รับผิดชอบงานนั้น** + **ผู้ดูแลสิทธิ์** + (ขาเพิกถอน) **HR** | คำขอ{request_kind}สิทธิ์ของ **{employee_name}** ไม่สำเร็จ {failed_count} รายการ — {fail_reason} · ครั้งที่ {retry_count} | **in-app + email** | ✗ **บังคับ** |
| `case_task_due_soon` | งานใน checklist ใกล้ถึงกำหนดเสร็จ (ทั้งสองวงจร · §3.2 `due_date`) `[AI-DRAFT · OQ-NTF-02]` | ผู้รับผิดชอบงาน | งาน **{task_name}** ของ {employee_name} ครบกำหนด {due_date} | in-app | ✓ |
| `case_task_overdue` | งานใน checklist **เลยกำหนดเสร็จ** (§3.2) | ผู้รับผิดชอบงาน + **หัวหน้าของผู้รับผิดชอบ** | งาน **{task_name}** ของ {employee_name} **เลยกำหนด {overdue_days} วัน** | in-app + email | ✓ |
| `ofb_case_approved` | §5.2 **T-8** `รออนุมัติ → อนุมัติแล้ว` (S-18 · FN-25 · FN-26) | **HR · หัวหน้า · ผู้รับผิดชอบทุกงานในชุดปิดสิทธิ์ · ผู้ดูแลสิทธิ์** | รอบออกงานของ **{employee_name}** อนุมัติแล้ว — วันทำงานวันสุดท้าย {last_working_day} · เพิกถอนสิทธิ์ {revocation_due_at} · คุณมี {my_task_count} งานที่ต้องทำ | **in-app + email** | ✗ **บังคับ** |
| **`ofb_access_revoked`** ⭐ | §5.2 **T-11** — **ทุกรายการในทะเบียนสิทธิ์มีผลตอบกลับว่าเพิกถอนแล้ว** (S-23 · FN-33) | **HR · หัวหน้า · ผู้ดูแลสิทธิ์** | สิทธิ์ทั้งหมดของ **{employee_name}** ถูกเพิกถอนครบ {revoked_count} รายการ เมื่อ {revoked_at} | **in-app + email** | ✗ **บังคับ** |
| **`ofb_revocation_overdue`** ⭐⭐ | **เลย `revocation_due_at` แล้วยังมีรายการที่ `revoke_state ≠ เพิกถอนแล้ว`** (S-24 · S-25 · BR-06 · FN-34 · FN-36) — ยิงซ้ำตามรอบจนกว่าจะครบ | **HR · ผู้ดูแลสิทธิ์ · หัวหน้า · (ยกระดับ) Policy Center** | ⚠ **{employee_name}** พ้นสภาพแล้วแต่ยังมีสิทธิ์ค้าง **{pending_count} รายการ** เลยกำหนด {overdue_hours} ชั่วโมง — {pending_labels} | **in-app + email** | ✗ **บังคับ — ปิดไม่ได้ทุกกรณี** |
| **`ofb_case_cancelled`** | §5.2 **T-13 · T-14** ยกเลิก/ถอนการออกจากงาน (S-37 · S-38 · FN-48 · FN-49 · FN-50) | **HR · หัวหน้า · ผู้รับผิดชอบงานที่ค้าง · ผู้ดูแลสิทธิ์ · (แจ้งการเปลี่ยนขอบเขตวันที่) ปลายทาง** | รอบออกงานของ **{employee_name}** ถูกยกเลิก — งานที่ค้าง {closed_task_count} งานถูกปิด{restore_suffix} · เหตุผล: {cancel_reason} | **in-app + email** | ✗ **บังคับ** |

**หมายเหตุการออกแบบ event:**
- ⭐ **`ofb_revocation_overdue` เป็น event ที่สำคัญที่สุดของใบนี้** — scope note บอกว่า "revoke สิทธิ์ทั้งหมดตอนออก + แจ้งเตือนผู้เกี่ยว" · **การเพิกถอนที่ไม่ครบไม่ใช่ "งานค้าง" แต่เป็นเหตุการณ์ความปลอดภัย** จึง **ปิดไม่ได้** · **ยิงซ้ำตามรอบ** · และ **ยกระดับผู้รับเมื่อเลยไปนาน** — ต่างจาก `case_task_overdue` ที่เป็นการเตือนงานปกติและปิดได้
- **แยก `ofb_access_revoked` (สำเร็จครบ) ออกจาก `ofb_revocation_overdue` (ไม่ครบ)** เพราะเป็นคนละผลลัพธ์ทางธุรกิจและคนละกลุ่มผู้รับ — และ **การเงียบเมื่อสำเร็จ** จะทำให้ไม่มีหลักฐานเชิงการแจ้งว่าเรื่องนี้จบแล้ว
- **`access_request_failed` ใช้ร่วมกันทั้งขาเปิดและขาเพิกถอน** โดยแยกด้วย `{request_kind}` — เป็น "คำขอสิทธิ์ไม่สำเร็จ" เหตุการณ์เดียว · ถ้า catalog เดิมแยกให้ใช้ของเดิม `[DEFAULT — รอยืนยัน]`
- **ไม่มี event ตอน "สร้างรอบออกงาน" (ร่าง)** — ยังไม่มีผลกับใคร · ผู้อนุมัติรู้ผ่าน `doa_pending` ที่ **engine ยิงเอง**
- **ทุก event มี ref** ชี้รอบ (`case_id`) และ `employee_id` · ไม่มี system broadcast ในใบนี้
- **ค่าเวลาทั้งหมดใน payload มาจากข้อมูลของรอบ** — **ห้าม hardcode ระยะเวลาเตือนใด ๆ ที่เป็นพารามิเตอร์กฎหมาย** (ระยะทดลองงาน/บอกกล่าว ยังไม่มีค่าให้อ่าน · OQ-STD-OB3) → **จึงไม่มี event เตือน "ใกล้ครบทดลองงาน" หรือ "ใกล้ครบบอกกล่าว" ในใบนี้** (ดู §3)

## §3 Event ที่ **ไม่ประกาศ** (และเหตุผล) — ห้ามเงียบ

| ไม่ประกาศ | เหตุผล |
|---|---|
| **`doa_pending`** · **`doa_result`** · **`doa_escalate`** | **DOA engine ยิงให้อัตโนมัติ** — ประกาศซ้ำ = **BLOCK** (SKILL §Iron · BR-29) · `ofb_case_approved` ในใบนี้เป็น **event ธุรกิจของ On/Offboard** (บอกวันสุดท้าย + เวลาเพิกถอน + งานที่ต้องทำ) ไม่ใช่ event ของ engine |
| **การเตือนซ้ำเมื่อรอบค้างอนุมัตินาน (SLA reminder)** · **การมอบฉันทะผู้อนุมัติ (delegation)** | **DOA Engine + ENG-NOTIFY เป็นเจ้าของ** (`catalog §0`: threshold/delegate/expiry/SoD) — feature ไม่ทำ reminder/delegation เอง · **S-57 คือการตรวจและสร้างงาน ไม่ใช่การแจ้งเตือนแทน DOA** |
| ⭐ **การมอบหมายงานใน Operation Process รายใบ (`sow.assigned` · `sow.closed` ฯลฯ)** | **Operation Process เป็นเจ้าของ** — งานทุกงานเป็น SOW และ OP มีการแจ้งของตัวเองอยู่แล้ว · ใบนี้ประกาศเฉพาะ **เหตุการณ์ระดับรอบ** (`onb_case_started` แจ้ง "ชุดงานของคุณเริ่มแล้ว" ครั้งเดียว) — **ไม่แจ้งซ้ำรายงาน** · `case_task_due_soon`/`case_task_overdue` ประกาศไว้เพราะกำหนดเสร็จผูกกับ **วันเริ่ม/วันสุดท้าย ซึ่งเป็นข้อมูลของ feature นี้** `[AI-DRAFT · OQ-NTF-02 — ถ้า OP แจ้งให้แล้ว ให้ตัดสองตัวนี้ออก]` |
| **เตือน "ใกล้ครบระยะทดลองงาน" / "ใกล้ครบระยะบอกกล่าว"** | ⛔ **ประกาศไม่ได้** — ต้องใช้ `employment_term.probation_days` / `notice_days_*` ที่ **HR Configuration ยังไม่เผยแพร่** (S-10 · S-16 · **OQ-STD-OB3 ← OQ-STD-06**) · **ห้ามเดาจำนวนวันเพื่อให้ยิง event ได้** — ปัญหาเดียวกับที่ Shift & Roster ประกาศ "ยังมีวันที่ยังไม่จัดกะ" ไม่ได้เพราะขาด `shift_rule.freeze_days` (OQ-NTF-03 ของ F-HR-ROSTER) |
| การบันทึกร่าง · การแก้ร่าง · การ validate/บล็อกในหน้าจอ | ยังไม่มีผลกับใคร / เป็นการตรวจในหน้าจอ — แจ้งเตือน = noise |
| การเผยแพร่ read model ให้ Attendance/Leave/Payroll/Welfare (S-40 · S-42) | เป็น **read model** — ปลายทางดึงเอง (pull) ไม่ต้องยิงแจ้งเตือน · **ยกเว้นการเปลี่ยนแปลงย้อนกลับ** ซึ่งแจ้งผ่าน `ofb_case_cancelled` |
| `hrconfig.*` · `attendance.*` · `leave.*` · `roles.*` | เป็น event ของ **feature ต้นทาง** — On/Offboard เป็นผู้ **ฟัง** ไม่ใช่ผู้ประกาศ |
| การปิดรอบสำเร็จ (T-3 · T-12) | ไม่มีใครต้องลงมือทำต่อ · ผลที่คนสนใจคือ `ofb_access_revoked` ซึ่งประกาศแล้ว `[AI-DRAFT · OQ-NTF-01]` |

## §4 Payload Contract

| field | ชนิด | มาจาก (PREBRIEF) | หมายเหตุ / masking |
|---|---|---|---|
| `case_id` · `case_type` | text · enum | §3.1 | **ref หลักของทุก event** |
| `employee_id` · `employee_name` | employee ref · text | §3.1 | **ส่ง id เป็น ref · ชื่อใช้เฉพาะใน template ที่แสดงต่อผู้มีสิทธิ์เห็น** (PII) |
| `start_date` · `last_working_day` · `revocation_due_at` | date · date · timestamp | §3.1 | — |
| `task_name` · `due_date` · `overdue_days` · `my_task_count` · `affected_task_count` · `closed_task_count` | text · date · int | §3.2 | — |
| `request_kind` | enum (`เปิด` · `เพิกถอน` · `คืน`) | §3.3 | ใช้แยกความหมายของ `access_request_failed` |
| `failed_count` · `fail_reason` · `retry_count` | int · text · int | §3.3 | **`fail_reason` อาจมีชื่อระบบภายใน — mask ก่อนส่งออกนอกกลุ่มผู้ดูแลสิทธิ์** |
| `revoked_count` · `revoked_at` · `pending_count` · `pending_labels` · `overdue_hours` | int · timestamp · int · text[] · int | §3.3 | ⭐ **`pending_labels` = ชื่อระบบที่ยังค้าง — Confidential · ส่งเฉพาะ HR + ผู้ดูแลสิทธิ์ + Policy Center** |
| `cancel_reason` · `restore_suffix` | text · text | §3.1 | `restore_suffix` = " · มีคำขอคืนสิทธิ์ {n} รายการ" เมื่อยกเลิกหลังเพิกถอน (S-38) |
| **ไม่มี** `termination_reason` ในทุก template | — | — | ⭐ **เหตุผลการออกเป็น Confidential (§7 masking)** — **ห้ามใส่ในข้อความแจ้งเตือนที่ส่งถึงคนหมู่มาก** · ผู้ที่ต้องรู้เปิดดูในรอบเอาเอง |
| **ไม่มีจำนวนเงินทุกชนิด** | — | BR-18 | ✅ |

## §5 เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)

- กลุ่ม **"งานและกระบวนการ"** → `onb_case_started` · `onb_start_date_changed` · `case_task_due_soon` · `case_task_overdue` · `ofb_case_approved` · `ofb_case_cancelled`
- กลุ่ม **"ความปลอดภัยและสิทธิ์" (ใหม่ — ถ้ายังไม่มี)** → **`access_request_failed` · `ofb_access_revoked` · `ofb_revocation_overdue`** — **ต้องเป็นกลุ่มที่ผู้ใช้ปิดไม่ได้** และควรอยู่กลุ่มเดียวกับ event ความปลอดภัยของ Policy Center `[DEFAULT — รอยืนยัน · OQ-NTF-04]`

## §6 Dev wiring note

- จุดเรียก: `ENG-NOTIFY.emit(event_id, {ref, vars})` ที่ transition ตาม §2 — **ห้ามเช็ค preference เอง · ห้ามเลือกช่องทางเอง**
- `ofb_revocation_overdue` เป็น **event เดียวในใบนี้ที่ไม่ผูกกับการกดของคน** — ผูกกับเวลาผ่านไป จึงต้องมี scheduler ฝั่ง feature เป็นตัวปล่อย (คู่ขนานกับ `ot_confirm_pending` ของ F-HR-OT และ `leave_entitlement_expiring` ของ F-HR-LEAVE) · **ยิงซ้ำตามรอบจนกว่ารายการจะครบ** — รอบการยิงซ้ำเป็นค่าที่ตั้งที่ ENG-NOTIFY ไม่ใช่ในโค้ด feature
- **ไม่มี UI ตั้งค่าการแจ้งเตือนในหน้าของ feature นี้** · **ไม่มี hint banner อธิบายว่าระบบจะส่งแจ้งเตือน** (#106 — ใช้ ⓘ `.tip` ถ้าจำเป็น) · **ไม่มีสตริง `doa_pending`/`doa_result` ในไฟล์ feature**

## §7 Open Questions

| # | ประเด็น | ค่าที่ใช้ไปก่อน | เจ้าภาพ |
|---|---|---|---|
| OQ-NTF-01 | ชื่อ event ชนกับ catalog เดิมหรือไม่ (`f-notify.html` ไม่มีในเวิร์กสเปซ) | ชื่อตาม §2 `[DEFAULT — รอยืนยัน]` | Chin (ENG-NOTIFY) |
| **OQ-NTF-02** | **`case_task_due_soon` / `case_task_overdue` ซ้ำกับการแจ้งของ Operation Process หรือไม่** — งานทุกงานเป็น SOW ซึ่ง OP อาจแจ้งอยู่แล้ว | **ประกาศไว้ก่อน** `[AI-DRAFT]` เพราะกำหนดเสร็จผูกกับวันเริ่ม/วันสุดท้ายซึ่งเป็นข้อมูลของ feature นี้ · **ถ้า OP แจ้งให้แล้วให้ตัดสองตัวนี้ออก ห้ามแจ้งซ้ำ** | Chin + BA Operation Process |
| **OQ-NTF-03** ⭐ | **เตือน "ใกล้ครบระยะทดลองงาน / ใกล้ครบระยะบอกกล่าว"** — ประกาศไม่ได้เพราะ HR Configuration ยังไม่เผยแพร่ `employment_term.*` | **ไม่ประกาศ** · **ห้ามเดาจำนวนวัน** — รอ **OQ-STD-OB3 ← OQ-STD-06** | **Strike + BA HR Configuration** |
| OQ-NTF-04 | กลุ่ม event ความปลอดภัยที่ผู้ใช้ปิดไม่ได้ มีอยู่แล้วหรือต้องสร้างใหม่ | เสนอกลุ่มใหม่ `[DEFAULT — รอยืนยัน]` | Chin / Policy Center |
| OQ-NTF-05 | รอบการยิงซ้ำของ `ofb_revocation_overdue` | ตั้งที่ ENG-NOTIFY `[ASSUMED]` — **ไม่ตั้งในโค้ด feature** | Chin |

## Quality Gate (self-check)

| # | เช็ค | ผล |
|---|---|---|
| N1 | ไม่ประกาศซ้ำ `doa_pending` / `doa_result` / `doa_escalate` | ✅ §3 ระบุชัด |
| N2 | ไม่ประกาศซ้ำ event ของ Operation Process (`sow.*`) | ✅ §3 — ประกาศเฉพาะเหตุการณ์ระดับรอบ · สองตัวที่คาบเกี่ยวติด `[AI-DRAFT]` + OQ-NTF-02 |
| N3 | ทุก event มี trigger ที่อ้าง PREBRIEF ได้จริง (จะแทนด้วย FRD § ที่ S5) | ✅ 9/9 |
| N4 | ทุก event มี ref | ✅ `case_id` + `employee_id` |
| N5 | ไม่ระบุ "ส่ง email/LINE" ใน logic ของ feature | ✅ channel เป็น default ของใบประกาศ · preference อยู่ที่ ENG-NOTIFY |
| N6 | ข้อความ template อยู่ในใบประกาศ ไม่ฝังในโค้ด | ✅ |
| N7 | ไม่มีตัวเลขเงิน · ไม่มีพารามิเตอร์กฎหมายที่เดาเอาเอง | ✅ BR-18 · OQ-NTF-03 |
| N8 | event ที่กระทบความปลอดภัย **ปิดไม่ได้** | ✅ `access_request_failed` · `ofb_access_revoked` · `ofb_revocation_overdue` · `ofb_case_approved` · `ofb_case_cancelled` |
