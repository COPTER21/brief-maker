# NTF_BRIEF — F-HR-WELFARE · สวัสดิการ
> ยิงผ่าน **ENG-NOTIFY (F-NOTIFY)** เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไขใน feature
> **DOA events (doa_pending / doa_result) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้ (ประกาศซ้ำ = BLOCK)**
> Source: FRD 03_LOGIC (state machine · FN-10/11/12/14/18) + 02_API §2.X + `_DECISION_LOG_OQ.md` (OQ-WEL-01 reversal)

## Declared Events (5)
| # | Event ID | Trigger (อ้าง FRD) | ผู้รับ | ข้อความ template (ไทย) | Channel default | บังคับ/ปิดได้ |
|---|---|---|---|---|---|---|
| 1 | `welfare_request_submitted` | submit: `draft→pending_approval` (API-11 · FN-10 · state machine §5.2a) | HR Welfare Admin (ผู้อนุมัติขั้นต้น) | มีคำขอใช้สิทธิ์สวัสดิการ **{request_no}** จาก {employee} รออนุมัติ | in-app | ✓ ปิดได้ |
| 2 | `welfare_request_result` | อนุมัติขั้นสุดท้าย `→approved` (FN-11) / `→rejected` (FN-12) | ผู้ยื่น | คำขอ **{request_no}** ของคุณ {ผล: อนุมัติ/ไม่อนุมัติ}{ · เหตุผล: {reason} เมื่อไม่อนุมัติ} | in-app + email | ✗ บังคับ |
| 3 | `welfare_quota_near_limit` | ยอดใช้สะสม ≥ 80% โควตา (BR-02 · FN-17 near-limit) | เจ้าของสิทธิ์ | สิทธิ์ **{benefit_type}** ใกล้เต็มโควตา (เหลือ {remaining}) | in-app | ✓ ปิดได้ |
| 4 | `welfare_eligibility_ended` | leaver signal → revoke (FN-18 · BR-06) | ผู้ยื่น + HR | สิทธิ์สวัสดิการของ {employee} สิ้นสุดตามวันพ้นสภาพ **{last_day}** | in-app + email | ✗ บังคับ |
| 5 | **`welfare_request_reversed`** ⭐ NEW | reverse: `approved→reversed` (API-15 · FN-14 · BR-11 · OQ-WEL-01) | **ผู้ยื่น + HR** | คำขอ **{request_no}** ถูกกลับรายการ · เหตุผล: {reason}{ · โปรดติดต่อ Payroll เรื่องการเบิกคืน — เมื่อ payroll_clawback} | in-app + email | ✗ บังคับ |

> **Reversal wording (มติ #81 · _DECISION_LOG_OQ.md):** ข้อความเป็น wording ทั่วไป "กลับรายการ" — **ห้ามโชว์ raw event id บนจอ** · payroll clawback แจ้งเป็นข้อความ display-only (ปลายทาง F065 · Welfare ไม่จ่าย/เบิกคืนเอง).

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
- กลุ่มใหม่ **"สวัสดิการ (welfare_*)"** — 5 event ข้างบน (ยังไม่มีในกลุ่มเดิม) · เพิ่ม `welfare_request_reversed` เข้ากลุ่มเดียวกัน.

## Dev wiring note
- จุดเรียก: `ENG-NOTIFY.emit(event_id, { ref: request_no|employee_id, vars })` ที่ transition ตาม trigger — **ห้ามเช็ค channel preference เอง** (config กลาง F-NOTIFY).
- ทุก event มี `ref` (soft-reference: request_no หรือ employee_id).
- emit จุดเดียวกับ side-effect ใน FN: submit(FN-10) · finalize approve/reject(FN-11/12) · reverse(FN-14) · leaver(FN-18) · near-limit(รายงาน/รอบคำนวณ FN-17).

## Iron check (Quality Gate)
- [x] **ไม่ประกาศ** doa_pending/doa_result/doa_escalate (DOA engine เจ้าของ) — no duplicate DOA event.
- [x] ทุก event มี ref.
- [x] ไม่ระบุ email/LINE ใน logic feature (channel = user preference + config กลาง).
- [x] template อยู่ในใบประกาศ ไม่ฝังใน code · **ตัวหนา** ที่เลขคำขอทุก event.
- [x] `welfare_request_reversed` = event ธุรกิจของ feature (state transition จริง FN-14) → ต้องประกาศที่นี่ (ไม่ใช่ DOA event).

---
_declaration รอบนี้: NTF (5 events incl. welfare_request_reversed) · 2026-09-08 · Source: FRD 03_LOGIC/02_API + _DECISION_LOG_OQ.md (OQ-WEL-01)_
