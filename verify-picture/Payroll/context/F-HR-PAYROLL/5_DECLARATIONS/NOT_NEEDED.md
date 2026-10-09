# NOT_NEEDED — F-HR-PAYROLL · Payroll (เงินเดือน)

> S1.8 · 2026-08-30 · บันทึกสิ่งที่ **จงใจไม่ทำ** ให้ตรวจได้ — **ห้ามเงียบ** · แหล่งตัดสิน: `_lane/DECL.json` (สร้างจาก `decl_rule.py`) + `PREBRIEF §12` (**authoritative**)

## ท่อประกาศ (5 ท่อ) — **ไม่มีท่อไหนถูกข้าม**

| ท่อ | chip (brief/POOL/CONTEXT_PACK) | detect (PREBRIEF §12) | ผล | ไฟล์ |
|---|---|---|---|---|
| **DOA** | ✓ | ✓ need | **ประกาศ** | `DOA_BRIEF.md` (25.5 KB · 5 action · 5 set) |
| **NTF** | ✓ | ✓ need | **ประกาศ** | `NTF_BRIEF.md` (16.2 KB · 7 event) |
| **CSQ** | ✓ | ✓ need — FC · AC · EC · SecC | **ประกาศ** | `CSQ_BRIEF.md` (29.6 KB · 8 event · 4 ท่อ) |
| **DOCCFG** | ✓ | ✓ need | **ประกาศ** | `DOCCFG_BRIEF.md` (13.9 KB · **2 doc_type**) |
| **PDF DOC** | ✓ | ✓ need | **ประกาศ** | `PDFDOC/` (`template.html` · `sample.pdf` A4 1 หน้า · `print-spec.md` · `_body.html`) |

**DIVERGENCE: ไม่มี** — chip = detect ทั้ง 5 ท่อ · ทุกท่อ `source: prebrief§12` (ไม่ต้องถอยไปใช้ chip)
**หมายเหตุทางเทคนิค:** `decl_rule.py` อ่าน `archetype_confirmed: Q-document+run` แล้วตัดเหลือ **`Q-document`** (regex `[\w-]+` หยุดที่ `+`) — **ไม่มีผลต่อการเลือก pattern** เพราะชั้นเอกสารของ feature นี้คือ Pattern Q จริง · ชั้น `run` เป็นโครงเพิ่มที่ระบุไว้ใน `PREBRIEF §3` ให้ `html-generator-v9` อ่านต่อ · **บันทึกไว้เพื่อไม่ให้ถูกเข้าใจว่าเป็น divergence**

## ท่อ 7C ที่ **ไม่ประกาศ** ภายใน `CSQ_BRIEF.md` (บันทึกไว้ให้ตรวจได้)

| ท่อ | เหตุผล |
|---|---|
| **OC** (Operation Consequence) | มาจาก **Operation Process** (`sow.*`) อัตโนมัติ — feature นี้ **ไม่สร้างงาน OP เลย** · ประกาศซ้ำ = **register reject 422** |
| **DC ระดับเอกสาร** (Decision Consequence) | **DOA engine เป็นเจ้าของ** — feature นี้มีสายอนุมัติ **5 แบบ** จึงเป็นจุดที่พลาดง่ายที่สุด · การอนุมัติ/ไม่อนุมัติรอบเป็นการเซ็นอนุมัติเอกสาร **ไม่ใช่ terminal decision** · **422** |
| **SC** | **สงวนไว้ทุกกรณี** (`OQ-C3` ยังไม่เคาะ) · **422** |
| **DC ที่ไม่ใช่การอนุมัติเอกสาร** | พิจารณา 3 จุดที่ดูคล้าย: การปิดรอบ (= การกระทำหลังได้รับอนุมัติ) · การสร้างรอบกลับรายการ (= เอกสารใหม่ที่มีสายอนุมัติของตัวเอง) · การทำเครื่องหมาย "ส่งไฟล์แล้ว" (= บันทึกข้อเท็จจริง ไม่มีทางเลือกให้ตัดสิน) — **ทั้งสามไม่เข้านิยาม DC** (`CSQ_BRIEF §3`) |

## Event ที่จงใจ **ไม่ประกาศ** ใน `NTF_BRIEF.md`

| event | เหตุผล |
|---|---|
| `doa_pending` · `doa_result` | **DOA Engine ยิงเองอัตโนมัติ** — ครอบ T-08 และ T-09 ทั้งคู่ · ประกาศซ้ำ = แจ้งสองครั้ง |
| `hrconfig.*` · `attendance.*` · `leave.*` · `ot.*` · `salstruct.*` · `ofb_case_*` | **เป็นของต้นทาง** — เราเป็นผู้ฟัง ไม่ใช่ผู้ประกาศ |
| "รอบถูกยกเลิก" (T-12) | เกิดก่อนอนุมัติเสมอ — ยังไม่มีผู้รับนอกทีมจัดทำที่ต้องรู้ |
| `payroll.gl_payload_ready` | **Accounting GL ยังไม่มีในระบบ → ไม่มีผู้รับ** · เพิ่มเมื่อ Module Linkage เปิด (`OQ-PAY-08`) |
| "สลิปของรอบปรับปรุงพร้อม" | ใช้ `payroll.payslip_available` ตัวเดิม — ไม่ตั้ง event ใหม่ให้ผู้รับต้องเรียนรู้สองแบบ |

## ความสามารถที่ **ไม่ implement** เพราะเป็นของ baseline (ห้าม re-implement)

| baseline | เราทำแค่ | เราไม่ทำ |
|---|---|---|
| **DOA Engine** | ประกาศ `action_id` 5 ตัว + matrix 5 set · เรียก `GET /doa/resolve` | ไม่เขียนสายอนุมัติเอง · ไม่ทำ delegate/expiry/reminder/SoD engine · **ไม่มี chain ใดใน feature** |
| **Document Configuration** | ประกาศ doc_type `PAY` · `PS` · เรียก `next()` / `store()` | **ไม่ format เลขเอง** · ไม่ทำคลังสำเนาเอง |
| **ENG-NOTIFY** | ประกาศ event ธุรกิจ 7 ตัว | ไม่ทำระบบส่ง · ไม่ทำ preference · ไม่ประกาศซ้ำ `doa_*` |
| **ENG-CSQ 7C** | ประกาศ profile `CSQ-HRPAY` + event 8 ตัว | **ไม่ตีมูลค่าเอง** (`ENG-CSQ-02` เป็นเจ้าของ) · ไม่ทำหน้า 7C |
| **Roles & Permissions / Policy Center** | อ้าง role id · แสดงผลตามสิทธิ์ที่ได้มา | **ไม่ทำ matrix สิทธิ์เอง** · ไม่ทำ masking engine · ไม่ให้/ไม่เพิกถอนสิทธิ์ |
| **Operation Process** | — | ไม่ผูก SOW รอบนี้ · **และห้ามประกาศท่อ OC** |
| **HR Configuration** | อ่านค่าผ่าน `resolve` · แสดงลิงก์ "จัดการที่ …" | **ไม่มีหน้าตั้งค่าใด ๆ** (#107 · S-58 · FN-76) |
| **ต้นทางทั้ง 6** | อ่านอย่างเดียว + snapshot + ลงทะเบียน where-used | **ไม่มี write path ออกไปเลย** (BR-07) · ไม่คำนวณชั่วโมง/วัน/สาย/ขาด เอง |

## ความสามารถที่ **ไม่ทำรอบนี้** (จาก `STANDARD_BASELINE §5` — มีอยู่ใน "ไม่รองรับ" ของ FUNCTION_CHECKLIST แล้วครบ)

| # | ไม่ทำ | OQ | ทำอะไรแทน |
|---|---|---|---|
| 1 | 50 ทวิ · ภ.ง.ด.1ก | `OQ-STD-PAY-A` | เก็บ **YTD** ให้ครบ (S-44) ให้ Accounting มาอ่าน |
| 2 | ไฟล์ยื่น ภ.ง.ด.1 รายเดือน | `OQ-STD-PAY-A` | **คำนวณยอดหักครบ** (MUST) แต่ไม่ออกแบบฟอร์ม |
| 3 | สปส.1-10 · รายงานนำส่งกองทุนสำรองฯ | `OQ-STD-PAY-B` | คำนวณเงินสมทบทั้งสองฝ่ายครบ |
| 4 | wizard สร้าง/แก้สลิปรายใบ | `OQ-STD-PAY-C` | รายการปรับด้วยมือในรอบที่ยังไม่ปิด (S-25) |
| 5 | จ่ายจริง · ตัดบัญชี · กระทบยอดธนาคาร | `OQ-STD-PAY-D` | ออกไฟล์โอน (S-40) แล้วหยุด |
| 6 | post GL จริง | `OQ-STD-PAY-E` · `OQ-PAY-08` | payload + hook + Module Linkage ปิด (S-41) |
| 7 | ใช้ `outside_shift_hours` เป็น OT | มติ `AT-6` · `OT-4` | ใช้ `hours_confirmed` จากใบที่ `time_confirmed` |
| 8 | retro recalculation ของงวดที่ปิด | มติ `P-9` | รอบปรับปรุงในงวดที่เปิดอยู่ที่อ้างรอบเดิม (S-46) |
| 9 | ⭐ **เดา/ตั้งค่าเริ่มต้นให้อัตราตามกฎหมาย** | `OQ-STD-PAY1…PAY6` · `OQ-PAY-06` · `OQ-PAY-07` | **"ยังไม่มีค่าให้อ่าน" · บรรทัด `ยังคำนวณไม่ได้` · ส่งอนุมัติไม่ได้** (BR-14…BR-19) |
