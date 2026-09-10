# NTF_BRIEF — F-HR-EXPENSE · Expense Claim (เบิกค่าใช้จ่าย · F101)
> ยิงผ่าน **ENG-NOTIFY.emit(event_id, {ref, vars})** เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไขใน feature
> DOA events (`doa_pending` / `doa_result` / `doa_escalate` / step-approved) มาจาก DOA engine (F-DLG-001) อัตโนมัติ — **ไม่อยู่ในใบนี้**
> 7C `FC (commit งบ) + EC (มูลค่า)` (อนุมัติครบสาย) = cross-module emit → อยู่ที่ **CSQ_BRIEF** ไม่ใช่ notification ปลายทาง — **ไม่อยู่ในใบนี้**
> `exp.pay_hook` / `exp.advance_offset` = hook ข้ามโมดูล (Payroll/Finance/F103 · display-only) ไม่ใช่ notification — **ไม่อยู่ในใบนี้**

## Event ประกาศ (5 ตัว)

| Event ID (FRD/HTML locked) | Trigger (อ้าง FRD + HTML anchor) | ผู้รับ | Payload (ref + vars) | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|---|
| `exp.submitted` | `draft → pending_approval` — ยื่น (API-05 side-effect · FN-06 `submitClaim`) · HTML `doSubmit` NTF-ANCHOR **L2435** · PREBRIEF S-01 | **ผู้อนุมัติขั้นแรก** ของสาย DOA ที่ resolve ตามยอด (dynamic · slot#1) — *role-id จริงมาจาก DOA resolve* [OQ-NTF-02] | `ref = claim_id` · `{code, grand, employee}` | มีใบเบิก **{code}** จาก {employee} รออนุมัติ (ยอด {grand}) | in-app | ✓ |
| `exp.approved` | `pending_approval → approved` **ครบสาย** (API-06 final · FN-07 ขั้นสุดท้าย) · HTML `doApprove` NTF-ANCHOR **L2464** · PREBRIEF S-06 (ผล) | **ผู้เบิก** (เจ้าของใบ · maker) | `ref = claim_id` · `{code}` | ใบเบิก **{code}** อนุมัติแล้ว — ออกเลข + PDF พร้อมแล้ว | in-app + email | ✗ บังคับ |
| `exp.rejected` | `pending_approval → rejected` (API-07 · FN-08 `rejectClaim` · reason required BR-18) · HTML `doReject` NTF-ANCHOR **L2478** · PREBRIEF S-06 (ตีกลับ) | **ผู้เบิก** (เจ้าของใบ) | `ref = claim_id` · `{reason}` | ใบเบิก **{code}** ถูกตีกลับ: {reason} — แก้แล้วยื่นใหม่ได้ | in-app | ✓ |
| `exp.paid` | `sent_to_pay → paid` — **hook อ่านกลับ** จาก Payroll/Finance (API-11 pay-status · FN-16) · PREBRIEF S-14 | **ผู้เบิก** (เจ้าของใบ) | `ref = claim_id` · `{code}` | ใบเบิก **{code}** จ่ายแล้ว | in-app | ✓ |
| `exp.overcap` | ยื่นใบที่มี **รายการเกินเพดานหมวด** (API-05 · BR-02 checkOverCap · มี over_reason ครบแล้ว) · PREBRIEF S-03 | **ผู้อนุมัติ** (สายที่ resolve) | `ref = claim_id` · `{code}` | ใบเบิก **{code}** มีรายการเกินเพดานหมวด (ระบุเหตุผลแล้ว) — โปรดพิจารณา | in-app | ✓ |

**Cross-check กับหน้าจอจริง (`expense.html`):** 3/5 event มี NTF-ANCHOR ยิงตรงจุด transition จริง — `doSubmit` (L2435) → `exp.submitted` · `doApprove` ขั้นสุดท้าย (L2464) → `exp.approved` · `doReject` (L2478) → `exp.rejected`. · `exp.overcap` ผูกกับ over-cap ที่ตรวจตอน submit (FN-13 · เดียวกับ L2435). · `exp.paid` **ไม่มี anchor บนจอ** เพราะ `sent_to_pay`/`paid` = state ปลายทาง hook display-only (05_RULES §5.2 "HTML implements … paid pill เท่านั้น") — ยิงเมื่อ hook Payroll/Finance อ่านกลับว่าจ่ายจริง ไม่ใช่ Expense ตัดสินเอง (BR-09). · **HTML L2436 `doa_pending` + L2453 `doa_step_approved` = DOA engine → ตัดออก ไม่ประกาศซ้ำ.**

## ตัดออกจากใบนี้ (โดยเจตนา)
| ตัด | เหตุผล |
|---|---|
| `doa_pending` (ส่งเข้าอนุมัติ) · `doa_result` · `doa_step_approved` (HTML L2436/L2453) · `doa_escalate` | DOA engine (F-DLG-001) เป็นเจ้าของ — ประกาศซ้ำ = BLOCK |
| `FC` (commit งบ) · `EC` (มูลค่า) — อนุมัติครบสาย (BR-07 · FN-19/22) | 7C/CSQ cross-module emit ไม่ใช่ notification ปลายทาง — อยู่ที่ **CSQ_BRIEF** |
| `exp.pay_hook` (เลือกช่องทางจ่าย · API-10) · `exp.advance_offset` (F103 · API-16) | hook ข้ามโมดูล display-only (02_API §2.X) — ไม่ใช่ notification ผู้ใช้ |

## ⚠️ เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS) — ต้องยืนยันก่อน dev wire
Sync Read `Related context/f-notify/f-notify.html` → `EVENT_GROUPS` (L343) ปัจจุบันมีเฉพาะสาย Sales/DOA:
`doa_pending · doa_result · doa_escalate · doc_status · doc_attach · mention · system`
— **ไม่มีกลุ่ม HR/ค่าใช้จ่าย และไม่มี event `exp.*` ในทะเบียนกลาง**

5 event ข้างต้นเป็น **feature-proposed + locked ระดับ FRD** (ชื่อตรงกันทุกที่: 01_UI §1.5 / 02_API §2.X / HTML NTF-ANCHOR) แต่ **ยังไม่ถูกลงทะเบียนในทะเบียนกลาง F-NOTIFY** จึงต้องเพิ่มเป็นกลุ่มใหม่ตอน deploy:

```
กลุ่มใหม่ (เสนอ): "ค่าใช้จ่าย (HR)"
  exp.submitted  — มีใบเบิกรออนุมัติถึงคุณ            (default: app on)
  exp.approved   — ใบเบิกของคุณอนุมัติแล้ว             (default: app+email, lock=on บังคับ)
  exp.rejected   — ใบเบิกของคุณถูกตีกลับ               (default: app on)
  exp.paid       — ใบเบิกของคุณจ่ายแล้ว                (default: app on)
  exp.overcap    — ใบเบิกมีรายการเกินเพดาน (ถึงผู้อนุมัติ) (default: app on)
```

## OPEN QUESTIONS (ยก BA เคาะ · [รอยืนยัน] — ห้ามเดา/ตั้งระบบจริงจนกว่าจะเคาะ)
- **OQ-NTF-01 (exact event_id + กลุ่มใหม่):** สตริง event_id ปลายทาง + การเพิ่มกลุ่ม "ค่าใช้จ่าย (HR)" ต้องยืนยันกับเจ้าของ F-NOTIFY ก่อน dev wire — ไม่พบ HR/expense master ในทะเบียนกลาง (Sales/DOA-only) จึงยืนยันรหัสจากทะเบียนไม่ได้.
- **OQ-NTF-01b (naming reconcile):** NTF_BRIEF ต้นทางของ BA (`5_DECLARATIONS/NTF_BRIEF.md`) ใช้ snake_case + **รวมผลเป็น 4 event** (`expense_submitted` / `expense_result` [approved+rejected รวม] / `expense_over_cap` / `expense_paid`). ใบนี้ตาม **FRD/HTML ที่ล็อกไว้** = dotted + **แยกผลเป็น 5 event** (`exp.approved` / `exp.rejected` แยกกัน · ตรงกับ HTML anchor L2464/L2478). BA เคาะว่าจะจดทะเบียนแบบ `exp.*` (5 · ตาม dev wire) หรือ `expense_*` (4 · รวมผล) — **เลือกแบบเดียวให้ตรงทั้ง FRD/HTML/registry**.
- **OQ-NTF-02 (recipient role-id ของ `exp.submitted`/`exp.overcap`):** "ผู้อนุมัติขั้นแรก/ผู้อนุมัติ" = สายที่ DOA resolve ตามวงเงิน (dynamic) — **role-id ปลายทางยังไม่เคาะ** (BR-04 OQ-01 · **CL-0013 แขวน**). ห้าม hardcode สาย/role-id ใน feature; recipient ผูกกับ chain ที่ DOA คืนตอน submit.
- **OQ-NTF-03 (new role "เจ้าหน้าที่ (HR/Finance)" · scope:all · BR-12):** role นี้ (`officer` · approver:false · เห็นทุกใบ · unmask · ติดตาม/กระทบยอด) **อาจเป็นผู้รับเพิ่ม**สำหรับ event เชิงการเงิน (`exp.approved` · `exp.paid`) เพื่อติดตาม/กระทบยอด — แต่ **ไม่ assume subscription** ในใบนี้ (default ตารางบน = ผู้เบิก/ผู้อนุมัติเท่านั้น). BA เคาะว่าให้ officer subscribe finance-relevant events หรือไม่ (RBAC · OQ-04).

## Dev wiring note
- จุดเรียก: `ENG-NOTIFY.emit(event_id, { ref: claim_id, vars })` ที่ transition ตาม trigger — **ห้าม feature เช็ค preference/channel เอง** (user preference + config กลางที่ F-NOTIFY จัดการ).
- `exp.submitted` → ใน FN-06 หลัง `status='pending_approval'` (API-05 side-effect · HTML L2435). ยิงครั้งเดียวต่อ submit; re-submit หลัง reopen = ยิงใหม่ตามรอบ.
- `exp.overcap` → ยิงคู่ `exp.submitted` เมื่อมี line over-cap (FN-13 checkOverCap = true).
- `exp.approved` → ใน FN-07 **เฉพาะขั้นสุดท้าย** (approval ครบสาย → ออกเลข · HTML L2464) — ยิงครั้งเดียวต่อใบ ไม่ยิงตอนอนุมัติขั้นกลาง (ขั้นกลาง = `doa_step_approved` ของ DOA engine · ตัดออก).
- `exp.rejected` → ใน FN-08 หลัง `status='rejected'` (API-07 · HTML L2478).
- `exp.paid` → เมื่อ hook pay-status (API-11 · FN-16) อ่านกลับ `paid` จาก Payroll/Finance — **ไม่ใช่ Expense ตัดสินเอง** (BR-09 display-only).
- email เป็น default ของ `exp.approved` เท่านั้น (event สำคัญ/ยืนยันผล · lock=on บังคับ) — ที่เหลือ in-app; ผู้ใช้ override ได้ที่ศูนย์ตั้งค่า F-NOTIFY.

## Quality Gate (Iron rules ของ skill)
- [x] ไม่ประกาศ `doa_pending`/`doa_result`/`doa_step_approved`/`doa_escalate` ซ้ำ (ตัดออกชัดเจน · HTML L2436/L2453)
- [x] ไม่ประกาศ 7C (FC/EC) / pay_hook / advance_offset ซ้ำ — cross-module emit อยู่ CSQ/hook ไม่ใช่ notification
- [x] ไม่ระบุ "ส่ง email/LINE" ใน logic feature — channel เป็น default ระดับใบประกาศ + user preference กลาง
- [x] ข้อความ template อยู่ในใบประกาศ ไม่ฝังใน code feature
- [x] ทุก event มี ref (`claim_id`) — ครบ 5/5
- [x] recipient/role-id ที่ยังไม่ชัด (DOA chain · officer subscribe) → ยกเป็น OQ ให้ BA ไม่เดา
