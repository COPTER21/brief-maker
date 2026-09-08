# CSQ_BRIEF — F-HR-WELFARE · สวัสดิการ
> ประกาศ event→ท่อ เท่านั้น · auto-register ตอน deploy · **ไม่คำนวณมูลค่าเอง** (ENG-CSQ-02 ทำ · basis=declared)
> Source: FRD 05_RULES (BR-09/BR-11 · LK-6) + 02_API §2.X + `_DECISION_LOG_OQ.md` (OQ-WEL-01 reversal)

## 1. Identity
feature_id: F-HR-WELFARE · module: HR · engine: **ENG-CSQ (F-CSQ-01)** · ท่อที่ใช้: **EC เท่านั้น** (LK-6)

## 2. Declared Events
| # | event_id | trigger point (อ้าง FRD) | ท่อที่ยิง | เงื่อนไข | payload fields |
|---|---|---|---|---|---|
| 1 | `welfare.granted` | อนุมัติขั้นสุดท้าย: `pending_approval→approved` (API-12 · FN-11 · BR-09) | **EC (forward)** | เมื่ออนุมัติคำขอใช้สิทธิ์ที่มีมูลค่า (claimable · ไม่ใช่ percent) | `ref: request_no` · `employee_id` (snapshot) · `benefit_type` · `value_declared` · `currency=THB` · `basis=declared` (มูลค่าที่กรอก · **ไม่คำนวณเอง**) |
| 2 | `welfare.granted` **reverse** ⭐ NEW | กลับรายการ: `approved→reversed` (API-15 · FN-14 · BR-11 · OQ-WEL-01) | **EC (negative offset)** | เมื่อคำขอที่ approved ถูกกลับรายการ (append-only) — คืนมูลค่าเข้าเงินได้ 7C·EC | `ref: request_no` (ใบเดิม) · `employee_id` · `benefit_type` · `value_declared: -x` (**negative offsetting entry**) · `currency=THB` · `basis=declared` · `reason` |

> **EC forward + EC reverse เป็นคู่กัน** (BR-09/BR-11 · 05_RULES §5.5 EC-06 · §5.8 D5) — reversal ไม่ลบ entry เดิม แต่บันทึก **negative offsetting entry** อ้าง request_no ใบเดิม (audit trail append-only · reconcile Payroll KPI-C2).

## 3. ท่อที่ไม่ประกาศ (และเหตุผล — no OC/DC/SC)
- **OC** — ไม่ประกาศ · มาจาก Operation Process (Welfare ไม่มี sow.*).
- **DC (เอกสาร) + doa_*** — ไม่ประกาศ · DOA engine ยิงให้อัตโนมัติ (การอนุมัติคำขอ = การเซ็น ไม่ใช่ terminal decision) · Welfare ไม่ออกเอกสารเลขรัน (DOCCFG NOT-NEEDED).
- **AC / FC** — ไม่ประกาศ · Welfare ไม่ลงบัญชี/ไม่กระทบเงินสด-งบเอง (จ่ายจริง = Payroll/Expense เป็นผู้ประกาศ AC/FC · payroll_clawback = flag ปลายทาง F065 ไม่ใช่ event ของ F102).
- **SC** — สงวน (trigger=false เสมอ · OQ-C3).

## 4. Register Checklist (dev)
- [ ] event `welfare.granted` (forward) อยู่ในกลุ่ม **EC** · payload มี ref + value_declared + `basis=declared`
- [ ] event `welfare.granted` reverse (EC negative offset) ผูกกับ `reverse` (FN-14) · `value_declared` เป็นลบ · อ้าง request_no ใบเดิม
- [ ] **ไม่ซ้ำท่อ OC/DC/SC/AC/FC** → กัน reject 422
- [ ] reconcile กับ Payroll (KPI-C2) — forward + reverse ต้องหักล้างกันได้

---
_declaration รอบนี้: CSQ (EC forward + EC reverse) · 2026-09-08 · Source: FRD 05_RULES BR-09/BR-11 + 02_API §2.X + _DECISION_LOG_OQ.md (OQ-WEL-01)_
