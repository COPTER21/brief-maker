# NTF_BRIEF — F-HR-OT · OT / Shift (โอที)

> ออกโดย `ntf-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-29
> Input: `briefs/W2/F-HR-OT/PREBRIEF.md` v1.1 §12 (**authoritative**) + §5 state machine + §4 BR · `LANE_BRIEF.md` (chip) · `_lane/DECL.json`
> **DIVERGENCE: —** (chip `ntf ✓` = detect §12 = ตาราง `CONTEXT_PACK/HR.md` แถว OT / Shift → ✓)
> หมายเหตุ: `f-notify.html` (EVENT_GROUPS catalog) **ไม่มีในเวิร์กสเปซนี้** — เทียบชนชื่อ event แบบ Sync Read ไม่ได้ · ยึด naming convention `{feature}_{event}` snake_case จาก SKILL.md · ชื่อที่เสนอติด `[DEFAULT — รอยืนยัน]` และต้อง cross-check กับ catalog จริงก่อน register
> **ยิงผ่าน ENG-NOTIFY เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไขใน feature · DOA events มาอัตโนมัติ ไม่อยู่ในใบนี้**

## §1 Identity

| | |
|---|---|
| feature_code | `F-HR-OT` · OT / Shift · โอที |
| module | HR |
| archetype | Q-document |
| event prefix | `ot_` |
| version | 1.0 (2026-08-29) |
| จำนวน event ที่ประกาศ | **7** (ธุรกิจล้วน — ไม่มี event ของ DOA) |

## §2 Declared Events

| Event ID | Trigger (อ้าง PREBRIEF · จะแทนที่ด้วย FRD §03_LOGIC ที่ S5) | ผู้รับ | ข้อความ template (ไทย) | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| `ot_submitted` | §5 T-2 `ร่าง → รออนุมัติ` (S-09 · FN-25) | **ผู้ถือ slot ปัจจุบันของสาย DOA** (หัวหน้าโดยตรง) + ผู้ขอ (สำเนา) | ใบ OT **{ot_no}** — {employee_name} ขอทำงานล่วงเวลา {work_date} {time_from}–{time_to} รวม {hours_requested} ชม. · รออนุมัติจากคุณ | in-app | ✓ |
| `ot_decided` | §5 T-4 `รออนุมัติ → อนุมัติแล้ว` (S-10 · S-11 · FN-29) **และ** T-5 `รออนุมัติ → ไม่อนุมัติ` (S-12 · FN-30) **และ** อนุมัติบางส่วน (S-17 · FN-31) | **ผู้ขอ** + หัวหน้าโดยตรง (สำเนา) | ใบ OT **{ot_no}** — {decision} · {work_date} {hours_decided} ชม.{partial_suffix}{reason_suffix} | **in-app + email** | ✗ **บังคับ** |
| **`ot_cap_warning`** ⭐ | ชั่วโมงสะสมของสัปดาห์ **ถึงเกณฑ์เตือน** ของเพดานที่ resolve จาก HR Configuration (S-05 · FN-14 · BR-09) — เกณฑ์ default **80% ของ `cap_hours_week`** `[DEFAULT — รอยืนยัน · OQ-OT-10]` | **ผู้ขอ** + **หัวหน้าโดยตรง** | ชั่วโมง OT สะสมสัปดาห์นี้ของ {employee_name} = {hours_accumulated} ชม. จากเพดาน {cap_hours_week} ชม. — เหลือ {hours_remaining} ชม. | in-app | ✓ |
| **`ot_cap_exceeded`** ⭐ | ใบถูกส่งอนุมัติโดยที่ชั่วโมงสะสม **เกินเพดาน** → `over_cap = true` → **สายอนุมัติยาวขึ้น** (S-06 · S-11 · FN-15 · FN-28) | **ผู้ขอ** + **หัวหน้าโดยตรง** + **HR** (ต้องรู้เพราะเป็นประเด็นการปฏิบัติตามกฎหมายแรงงาน) | ใบ OT **{ot_no}** — ชั่วโมงสะสมสัปดาห์ {hours_accumulated} ชม. **เกินเพดาน {cap_hours_week} ชม.** · ต้องผ่านการอนุมัติเพิ่มอีก 1 ขั้น | **in-app + email** | ✗ **บังคับ** |
| `ot_cancelled` | §5 T-6 `รออนุมัติ → ยกเลิก` (S-13 · FN-39) | **ผู้ถือ slot ที่ค้างอยู่** (งานอนุมัติถูกปิด) | ใบ OT **{ot_no}** — {employee_name} ยกเลิกคำขอแล้ว · ไม่ต้องพิจารณา | in-app | ✓ |
| `ot_withdrawn` | §5 T-9 `อนุมัติแล้ว / ยืนยันเวลาจริงแล้ว → ถอน` (S-14 · S-34 · FN-41 · BR-27) | **ผู้ขอ** + หัวหน้าโดยตรง + **HR** (กระทบชั่วโมงที่เผยแพร่ให้ Payroll ไปแล้ว) | ใบ OT **{ot_no}** — ถอนใบที่อนุมัติแล้ว · คืน {hours_reversed} ชม. · เหตุผล: {withdraw_reason} | **in-app + email** | ✗ **บังคับ** |
| **`ot_confirm_pending`** ⭐ | ใบสถานะ "อนุมัติแล้ว" ที่ **วันที่ทำ OT ผ่านไปแล้วและเวลาเข้างานยืนยันแล้ว แต่ยังไม่ถูกยืนยันเวลาจริง** (S-16 · FN-21 · BR-17) **หรือ** ใบติดธง **"ต้องทวน"** จาก `attendance.day_adjusted` (S-23 · FN-43 · BR-22) | **หัวหน้าโดยตรง** + **HR** | ใบ OT **{ot_no}** — {pending_kind} · {work_date} · ต้องยืนยันเวลาจริงก่อนส่งเข้ารอบค่าจ้าง | in-app (+email เมื่อเป็นธง "ต้องทวน") | ✓ |

**หมายเหตุการออกแบบ event:**
- **แยกการเตือนเพดานเป็น 2 ตัว** (`ot_cap_warning` = ใกล้ถึง · `ot_cap_exceeded` = เกินแล้ว) เพราะ **ผลลัพธ์ทางธุรกิจต่างกันคนละเรื่อง** — ตัวแรกเป็นข้อมูลเชิงป้องกัน ปิดได้ · ตัวหลังเปลี่ยน **สายอนุมัติ** และเป็นประเด็นการปฏิบัติตามกฎหมายแรงงาน จึง **ปิดไม่ได้** และถึง HR ด้วย · scope note ระบุคำว่า "ceiling warnings" ไว้ตรง ๆ (`CONTEXT_PACK/HR.md` แถว OT)
- **ค่าเพดานและเกณฑ์เตือนใน payload มาจาก HR Configuration ที่ resolve ณ `work_date` เสมอ** — **ห้าม hardcode ตัวเลขในข้อความหรือในเงื่อนไขการยิง** (BR-01 · P-8)
- **`ot_decided` รวม อนุมัติ/ไม่อนุมัติ/อนุมัติบางส่วน ไว้ event เดียว** โดยแยกด้วย `{decision}` + `{partial_suffix}` — 1 เหตุการณ์ทางธุรกิจ = "ผลการตัดสิน" · ถ้า catalog เดิมแยกให้ใช้ของเดิม `[DEFAULT — รอยืนยัน]`
- **`ot_confirm_pending` เป็น event เดียวในใบนี้ที่ไม่ผูกกับการกดของคน** — ผูกกับเวลาผ่านไป/เหตุการณ์จากต้นทาง จึงต้องมี scheduler ฝั่ง feature เป็นตัวปล่อย (คู่ขนานกับ `leave_entitlement_expiring` ของ F-HR-LEAVE)
- ทุก event มี **ref** ชี้เอกสาร (`ot_no`) ยกเว้น `ot_cap_warning` ที่ชี้ (`employee_id` + `week_of`) — ไม่มี system broadcast ในใบนี้

## §3 Event ที่ **ไม่ประกาศ** (และเหตุผล) — ห้ามเงียบ

| ไม่ประกาศ | เหตุผล |
|---|---|
| **`doa_pending`** (มีใบรอคุณอนุมัติ) | **DOA engine ยิงให้อัตโนมัติ** — ประกาศซ้ำ = **BLOCK** (SKILL §Iron) · ดู `DOA_BRIEF.md §6` |
| **`doa_result`** (ผลการอนุมัติจาก engine) | เหมือนกัน — `ot_decided` ในใบนี้เป็น **event ธุรกิจของ OT** (แจ้งผู้ขอด้วยภาษาใบ OT + จำนวนชั่วโมงที่ได้จริง) ไม่ใช่ event ของ engine |
| **`doa_escalate`** / เตือนซ้ำเมื่อใบค้างอนุมัตินาน (reminder/SLA) · **การมอบฉันทะผู้อนุมัติ** | **DOA engine + ENG-NOTIFY เป็นเจ้าของ** (S1.5 G-10 · G-11 → SKIP) — feature ไม่ทำ reminder/delegation เอง |
| การบันทึกร่าง (S-08) · การแก้ร่าง | ยังไม่มีผลกับใคร — แจ้งเตือน = noise |
| การ validate ในหน้าจอ (S-07 · S-19 · S-20 · S-21 · S-22 · S-28 · S-29 · S-30 · S-43) | เป็น **การตรวจในหน้าจอ** ไม่ใช่เหตุการณ์ที่คนอื่นต้องรู้ |
| **การยืนยันเวลาจริงสำเร็จ (S-16 · T-8)** | ผู้ขอรู้ผลตอน `ot_decided` แล้ว · การยืนยันเป็นขั้นตอนภายในก่อนส่งเข้ารอบค่าจ้าง — **แจ้งเมื่อ "ยังไม่ยืนยัน" (`ot_confirm_pending`) มีประโยชน์กว่าแจ้งเมื่อยืนยันสำเร็จ** `[AI-DRAFT]` (OQ-NTF-02) |
| การเผยแพร่ให้ Payroll/ESS อ่าน (S-31 · S-32) | เป็น **read model** — ปลายทางดึงเอง ไม่ต้องยิงแจ้งเตือน |
| `hrconfig.*` · `attendance.*` · `leave.*` | เป็น event ของ **feature ต้นทาง** — OT เป็นผู้ **ฟัง** ไม่ใช่ผู้ประกาศ (BR-04) · ยกเว้นผลที่ตกกับใบเรา ซึ่งแจ้งผ่าน `ot_confirm_pending` (ธง "ต้องทวน") |

## §4 Payload Contract

| field | ชนิด | มาจาก (PREBRIEF) | หมายเหตุ / masking |
|---|---|---|---|
| `ot_no` | text | §3.1 เลขที่ใบ OT | ref หลักของ 6 event · ตัวหนาในข้อความ |
| `employee_id` · `employee_name` | employee ref · text | §3.1 ผู้ขอ | **ส่ง id เป็น ref · ชื่อใช้เฉพาะใน template ที่แสดงต่อผู้มีสิทธิ์เห็น** |
| `work_date` · `time_from` · `time_to` | date · time · time | §3.2 | — |
| `hours_requested` · `hours_decided` · `hours_reversed` | decimal(6,2) | §3.1 | **หน่วยชั่วโมง — ไม่มีจำนวนเงิน** (BR-18) |
| `decision` | enum | §5 | `อนุมัติแล้ว` / `ไม่อนุมัติ` |
| `partial_suffix` | text | §3.1 `hours_approved_total` + `partial_reason` | เติมท้ายเมื่ออนุมัติบางส่วน เช่น " (อนุมัติบางส่วนจากที่ขอ {hours_requested} ชม.)" |
| `reason_suffix` | text | §3.1 `reject_reason` | เติมท้ายเฉพาะกรณีไม่อนุมัติ (BR-12) |
| `withdraw_reason` | text | §3.1 | เฉพาะ `ot_withdrawn` |
| **`hours_accumulated` · `cap_hours_week` · `hours_remaining`** | decimal(6,2) | §3.5 + **HR Config `ot_rate.cap_hours_week` (resolve ณ `work_date`)** | **ค่าเพดานต้องมาจาก resolve ไม่ใช่ค่าคงที่ในข้อความ** (BR-01 · P-8) |
| `week_of` | date | §3.5 ขอบสัปดาห์ตาม `period_rule` | ref ของ `ot_cap_warning` (OQ-OT-09) |
| `pending_kind` | enum | §5 T-8 · T-11 | `ยังไม่ยืนยันเวลาจริง` / `ต้องทวน (เวลาเข้างานถูกแก้)` |
| `approver_slot_role` | text | DOA resolve | ใช้เลือกผู้รับของ `ot_submitted` — **ไม่ใส่ในข้อความ** |

- **ชั้นข้อมูล:** ใบ OT = **Confidential** (`reason` · `work_done`) → **ข้อความแจ้งเตือนห้ามมีเหตุผลความจำเป็นหรือรายละเอียดงานที่ทำ** · `reason_suffix` ใส่ได้เฉพาะ **เหตุผลที่ผู้อนุมัติเขียนตอนปฏิเสธ** ซึ่งส่งถึงผู้ขอเท่านั้น
- **ห้ามมีตัวเลขเงินในทุก payload/template** (BR-18) — ห้ามใส่ `multiplier` ไปคูณอะไรในข้อความ
- **ห้ามระบุ "ส่ง email/LINE" ใน logic ของ feature** — channel เป็นของ user preference + config กลาง (SKILL §Iron)

## §5 เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)

- กลุ่ม **"เอกสารธุรกรรม"** → `ot_submitted` · `ot_decided` · `ot_cancelled` · `ot_withdrawn` — **ตระกูลเดียวกับ `leave_*` ของ F-HR-LEAVE และ doc_status ของ SO/PO/PR** · ถ้ามีกลุ่มกลางอยู่แล้วให้ใช้ของเดิม **ห้ามตั้งกลุ่มใหม่**
- กลุ่ม **"เกณฑ์/เพดาน (threshold alert)"** → `ot_cap_warning` · `ot_cap_exceeded` — ตระกูลเดียวกับ `inv_low_stock` / เกินวงเงินเครดิต · ถ้ายังไม่มีกลุ่มนี้ **เสนอเพิ่ม 1 กลุ่ม**
- กลุ่ม **"งานค้างของฉัน"** → `ot_confirm_pending` — ถ้ามีกลุ่ม reminder กลางอยู่แล้วให้ใช้ของเดิม

## §6 Dev wiring note

- จุดเรียก: `ENG-NOTIFY.emit(event_id, {ref, vars})` ที่ transition ตาม §2 — **ห้ามเช็ค preference เอง ห้ามเลือกช่องทางเอง**
- `ot_cap_warning` / `ot_cap_exceeded` ยิงจากจุดที่คำนวณ `over_cap` (ตอนกรอกบรรทัดและตอนส่งอนุมัติ) — **ค่าเพดานต้องมาจาก `hr-config/resolve` ไม่ใช่ค่าคงที่**
- `ot_confirm_pending` ต้องมี **scheduler ฝั่ง feature** (รายวัน) ที่กวาดใบสถานะ "อนุมัติแล้ว" ที่เลยวันที่ทำ OT + ใบที่ติดธง "ต้องทวน"
- HTML (S2): คอมเมนต์ `// TODO: ENG-NOTIFY emit — ดู NTF_BRIEF.md` ที่ปุ่มส่งอนุมัติ · อนุมัติ/ไม่อนุมัติ · ยกเลิก · ถอน · จุดคำนวณเพดาน — **ห้ามวาด UI ตั้งค่าการแจ้งเตือนในหน้านี้** (#107) · **ห้ามมี hint banner อธิบายระบบแจ้งเตือน** ใช้ ⓘ `.tip` (#106)
- FRD (S5): แทน trigger ทุกแถวด้วย `03_LOGIC §x.x` จริง แล้ว **append ในไฟล์เดิม** (ห้ามออกใบใหม่)

## §7 Open Questions

| # | ประเด็น | ค่าที่ใช้ไปก่อน | เจ้าภาพ |
|---|---|---|---|
| OQ-NTF-01 | ชื่อ event ชนกับ catalog เดิมหรือไม่ (ไม่มี `f-notify.html` ให้ Sync Read) | `ot_*` ตาม convention `[DEFAULT — รอยืนยัน]` — **ถ้าชน ใช้ของเดิม ห้ามตั้งชื่อเลี่ยง** | Architect / F-NOTIFY owner |
| OQ-NTF-02 | ต้องแจ้งเมื่อ **ยืนยันเวลาจริงสำเร็จ** ด้วยหรือไม่ | **ไม่แจ้ง** `[AI-DRAFT]` — แจ้งเฉพาะเมื่อยังไม่ยืนยัน (`ot_confirm_pending`) ซึ่งเป็นสิ่งที่ต้องลงมือทำ | BA |
| **OQ-OT-10** | **เกณฑ์ "ใกล้ถึงเพดาน"** ที่ใช้ยิง `ot_cap_warning` | **80% ของ `cap_hours_week`** `[DEFAULT — รอยืนยัน]` — **ค่านี้ควรอยู่ที่ HR Configuration ไม่ใช่ในโค้ด** (ชุดเดียวกับ OQ-STD-OT5 · OQ-OT-16) | Strike + BA HR Configuration |
| OQ-OT-14 | ยกเลิกใบที่รออนุมัติต้องกรอกเหตุผลหรือไม่ (กระทบข้อความของ `ot_cancelled`) | **ไม่บังคับ** `[AI-DRAFT]` | BA |

## Quality Gate (self-check)

| # | เช็ค | ผล |
|---|---|---|
| N1 | ไม่ประกาศซ้ำ `doa_pending` / `doa_result` / `doa_escalate` | ✅ §3 ระบุชัดทั้ง 3 ตัว + delegation/reminder |
| N2 | ทุก event มี trigger point อ้าง PREBRIEF § ได้จริง | ✅ 7/7 อ้าง §5 transition + S-XX + FN-XX |
| N3 | ทุก event มี ref (soft reference) | ✅ `ot_no` 6 ตัว · `employee_id`+`week_of` 1 ตัว |
| N4 | ข้อความ template อยู่ในใบประกาศ ไม่ฝังใน code | ✅ §2 |
| N5 | ไม่ระบุช่องทางใน logic ของ feature | ✅ channel เป็น default ที่ user/config กลางเปลี่ยนได้ |
| N6 | payload ไม่มีข้อมูลชั้น Confidential ดิบ | ✅ ไม่มี `reason` / `work_done` ในทุก template |
| **N7** | **ไม่มีตัวเลขเงิน และไม่มีค่าเพดานที่ hardcode ในข้อความ/เงื่อนไข** | ✅ `cap_hours_week` เป็นตัวแปรที่มาจาก resolve (§4) |
| N8 | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` / `[AI-DRAFT]` ครบ | ✅ ชื่อ event · เกณฑ์ 80% · OQ-NTF-02 |

**Verdict: PASS** — 7 event ธุรกิจ พร้อม register เข้า ENG-NOTIFY

---

## §8 FRD Mapping (append โดย S5 · `frd-generator-v6` · 2026-08-29) — **ไม่ออกใบใหม่**

> ข้อผูกพันจาก §6: "FRD (S5): แทน trigger ทุกแถวด้วย `03_LOGIC §x.x` จริง แล้ว append ในไฟล์เดิม" — ทำแล้วตามตารางนี้

| Event ID | trigger จริงใน FRD | อ้าง |
|---|---|---|
| `ot_submitted` | `03_LOGIC §3.1 F-37 submitRequest` (หลัง `freezeApprovalChain` สำเร็จ) | `05_RULES §5.2 T-2` · `02_API API-06` |
| `ot_decided` | `03_LOGIC §3.1 F-39 approveStep` (ขั้นสุดท้าย) · `F-40 approvePartial` · `F-41 rejectRequest` | `05_RULES §5.2 T-4 · T-5` · `02_API API-08 · API-09 · API-10` |
| `ot_cap_warning` | `03_LOGIC §3.1 F-25 computeCapWarning` (เรียกจาก `F-35 buildPreSubmitReport` และตอนกรอกบรรทัด) | `02_API API-04 · API-05` |
| `ot_cap_exceeded` | `03_LOGIC §3.1 F-24 computeOverCap` = true ภายใน `F-37 submitRequest` | `05_RULES §5.2 T-2` · `02_API API-06` |
| `ot_cancelled` | `03_LOGIC §3.1 F-42 cancelRequest` | `05_RULES §5.2 T-6` · `02_API API-11` |
| `ot_withdrawn` | `03_LOGIC §3.1 F-44 finalizeWithdrawal` | `05_RULES §5.2 T-9` · `02_API API-12` |
| `ot_confirm_pending` | `03_LOGIC §3.1 F-66 sweepPendingConfirm` (scheduler รายวัน) · `F-47 onAttendanceDayAdjusted` (ธง "ต้องทวน") | `05_RULES §5.2 T-11` · `02_API API-17` |

**ยืนยันความสอดคล้อง (gate ของ Lane Mode v2):**
- FRD ใช้ **7 event = 7 event ที่ประกาศไว้ในใบนี้** — **ไม่มีตัวเพิ่ม ไม่มีตัวเกิน** (`00_OVERVIEW §0.16.1`)
- **ไม่มีการประกาศซ้ำ `doa_pending` / `doa_result` / `doa_escalate` / reminder / delegation** — ยืนยันอีกครั้งที่ `00_OVERVIEW §0.16.3`
- ชุด event ของใบนี้ (`ot_*` underscore) **ไม่ทับกับชุด 7C ของ `CSQ_BRIEF` (`ot.*` dot) แม้แต่ตัวเดียว**
- ข้อห้าม payload ยังมีผลทุกข้อ: **ห้ามใส่ `reason` / `work_done` / ชื่อไฟล์แนบ ลงใน vars** · **ห้ามมีตัวเลขเงิน** — บังคับผ่าน `03_LOGIC F-67 assertNoMoneyField` และ `06_TESTS IA-07`
