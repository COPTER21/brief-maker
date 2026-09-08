# 05_RULES — F-HR-WELFARE · Welfare (สวัสดิการ)

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + State Machine + Permission + Validation + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด. Source: BRD §9 + Decision Log + PM/BA fix round.

---

## §5.1 Business Rules (BR)

| BR | กฎ | Tag | Enforced by | Error / trace |
|---|---|---|---|---|
| **BR-01** | eligibility: ต้องอยู่ในกลุ่มที่ type กำหนด **ณ วันยื่น** (resolve) | DYNAMIC | ENG-WEL-01 · FN-08/FN-09 | BR_NOT_ELIGIBLE · FN-07/11 |
| **BR-02** | โควตา/วงเงินต่อปีต่อคน — ใช้เกินคงเหลือ = บล็อก · **re-check ณ อนุมัติ (FIX-02)** | CONFIGURABLE | ENG-WEL-02 · FN-08/FN-11 | BR_OVER_BALANCE · FN-09/10/13 |
| **BR-03** | ทุกเวอร์ชัน type มี effective_date · **ช่วงไม่ทับ** | FIXED | FN-03 | BR_EFFECTIVE_OVERLAP · FN-02/04 |
| **BR-04** | คำขอผ่าน **DOA** ก่อนตัดคงเหลือ — GET /doa/resolve **ไม่ hardcode chain** (LK-1) | DYNAMIC | FN-10 · ENG-DOA | FN-08 |
| **BR-05** | ตัดคงเหลือ **เฉพาะ approved** · reject/cancel/revoke/**reversed ไม่ตัด (reversed = คืน)** | FIXED | ENG-WEL-02 | FN-11/12/13/14 |
| **BR-06** | ช่วงสิทธิ์ผูก employment window (joiner เปิด · leaver ปิด) · **null last-day ≠ ไม่มีวันจบ** | FIXED | FN-18 · ENG-WEL-01 | FN-16/18 |
| **BR-07** | balance ledger + คำขอ = **append-only** · audit ทุก create/approve/แก้/ยกเลิก/**กลับรายการ** · soft archive (LK-5) | FIXED | T_welfare_audit_log · no hard delete | FN-93 |
| **BR-08** | ข้อมูลบุคคล/ผู้ติดตาม/มูลค่า = **RESTRICTED masking ตาม role** (Policy Center · LK-5) · enforce backend | CONFIGURABLE | FN-19 · §5.7 D-CLASS | FN-94 |
| **BR-09** | มูลค่าสวัสดิการ approved = ผลได้พนักงาน → ยิง **CSQ EC** (welfare.granted) · **EC เท่านั้น (LK-6)** | FIXED | FN-11 · ENG-CSQ | §02_API §2.X |
| **BR-10** | snapshot ชื่อคน/บริษัท/config_version ณ บันทึก (soft ref LD-4C-02 · LK-4) | FIXED | FN-07 | ทุก write |
| **BR-11** (reversal) | **กลับรายการเฉพาะ approved + canApprove + เหตุผลบังคับ · คืนสิทธิ์ + EC reverse (negative offset) + payroll clawback flag เมื่อ pay=sent · append-only** (OQ-WEL-01) | DYNAMIC | FN-14 · ENG-WEL-02 · ENG-CSQ | E6 · US-16 |
| **BR-12** (exposure) | แสดง pending demand อื่นบนสิทธิ์เดียวกันประกอบการอนุมัติ · **display-only ไม่ soft-reserve** (OQ-WEL-03) | CONFIGURABLE | FN-16 | US-17 |

### BR-DOA (Governance guards — proven by PM/BA fix round) ⭐
รวมกฎ approval ที่พิสูจน์แล้วในรอบ fix (FIX-01..06) — **ห้าม dev ตีความใหม่**:
- **BR-DOA-1 (approve pending-only · FIX-01):** อนุมัติได้เฉพาะคำขอ `status='pending_approval'` เท่านั้น. สถานะอื่น → BR_APPROVE_PRECONDITION.
- **BR-DOA-2 (resolve-at-submit + freeze · LK-1):** สาย DOA resolve ตอนส่ง (GET /doa/resolve) แล้ว **freeze snapshot** (person {name,position}) ลง T_welfare_request_approval — append-only, ไม่ re-resolve ระหว่างทาง.
- **BR-DOA-3 (advance ONE step per approval · FIX-03):** อนุมัติ 1 ครั้ง = เลื่อน **1 ขั้น** (current→approved, next→current). **ห้าม collapse ทั้งสายในครั้งเดียว**. status คง pending_approval จนขั้นสุดท้าย.
- **BR-DOA-4 (re-check at final approval · FIX-02):** เฉพาะ **ขั้นสุดท้าย** ก่อน commit → re-check eligibility (BR-01) + เพดาน/remaining (BR-02) **atomic ที่ backend** (OQ-04). ผ่าน → ตัดคงเหลือ + EC + pay hook (ครั้งเดียว). ไม่ผ่าน → block (BR_NOT_ELIGIBLE_AT_APPROVAL / BR_OVER_BALANCE_AT_APPROVAL).
- **BR-DOA-5 (soft-reserve = NONE · OQ-WEL-03):** คำขอ pending **ไม่** จอง/ล็อกโควตา. exposure display-only ช่วยผู้อนุมัติเห็น pending demand เท่านั้น. จุดตัดสินจริง = ณ approval (BR-DOA-4).
- **BR-DOA-6 (permission · FIX-04):** approve/reject/reverse = `canApprove` (admin|manager). cancel = owner หรือ admin (`canCancelReq`). ทะเบียน (create/edit/archive) = admin. enforce **backend** (OQ-05).
- **BR-DOA-7 (cancel scope · FIX-05):** cancel เฉพาะ `draft`/`pending_approval` (pre-approval). approved → **ต้องใช้ reversal** (BR-11) ไม่ใช่ cancel. สองขอบเขตแยกกันไม่ทับ.
- **BR-DOA-8 (archive warns pending · FIX-06):** ปิดใช้ประเภทที่มีคำขอค้างอ้างอยู่ → **เตือนจำนวนใบ** ก่อน confirm (soft archive · คำขอเก่ายังอ่านได้).

### BR-BAL (Balance integrity)
- **BR-BAL-1:** balance = **live compute จาก ledger** (approved only) — ไม่เก็บซ้ำ (ENG-WEL-02).
- **BR-BAL-2:** **never negative-clamp ใน logic** — ค่าจริงติดลบได้ (สัญญาณ over-approval ต้องเห็น/audit); UI display อาจ clamp 0.
- **BR-BAL-3:** reversed คืนยอดเอง (นับเฉพาะ approved) — ไม่ปรับซ้ำ.

---

## §5.2 State Machine

### 5.2a Benefit Request (transaction)
```
draft ──submit(DOA slot picker)──▶ submitted ──resolve+freeze──▶ pending_approval
   │                                                                  │ (DOA per-step · one-step advance)
   │ cancel                              ┌── reject ──▶ rejected      ▼
   ▼                                     │                        approved ──reverse──▶ reversed (append-only)
cancelled                          (pending)                          │
                                                                      │ (ปิดรอบ/หมดอายุ)
(ทุกสถานะก่อน closed) ──leaver signal──▶ revoked                       ▼
                                                                    closed
```

| From | To | Action | Allowed roles | Conditions |
|---|---|---|---|---|
| draft | submitted→pending_approval | submit | ผู้ยื่น/admin | เลือก DOA ครบทุกขั้น (VR-09) |
| draft/pending_approval | cancelled | cancel | owner/admin | pre-approval เท่านั้น (BR-DOA-7) |
| pending_approval | pending_approval | approve (ขั้นกลาง) | approver (DOA) | one-step advance (BR-DOA-3) |
| pending_approval | approved | approve (ขั้นสุดท้าย) | approver (HR · DOA) | **re-check ผ่าน (BR-DOA-4)** → ตัดคงเหลือ + 7C EC + hook |
| pending_approval | rejected | reject | approver | reason required (VR-08) · ไม่ตัดคงเหลือ |
| **approved** | **reversed** | **reverse** | **admin/manager** | **reason required · append-only · คืนคงเหลือ + EC reverse + clawback flag (BR-11)** |
| any (pre-closed) | revoked | leaver signal | system | คงเหลือหยุด · null≠ทำงาน (BR-06) |
| approved | closed | ปิดรอบ | system | — |

> **UI mapping (HTML fidelity):** welfare.html รวม `submitted`+`pending_approval` เป็น pill "รออนุมัติ" (`pending`); reversed = pill "กลับรายการแล้ว". สถานะเชิงตรรกะครบ 9; UI แสดง draft/pending/approved/rejected/cancelled/revoked/reversed. **`reversed` เป็น state ทางการใน 03_LOGIC + DB.**

### 5.2b Benefit Type (master)
```
draft ──publish──▶ active(effective_date) ──edit(ออกเวอร์ชันใหม่)──▶ superseded/archived
```
soft archive · เวอร์ชันเก่ายังอ้างได้ (BR-03/BR-07).

---

## §5.3 Permission Matrix

| Role | ทะเบียน CRUD | ผู้ติดตาม | สร้างคำขอ | ส่งอนุมัติ | อนุมัติ/ไม่อนุมัติ | ยกเลิก | **กลับรายการ** | เห็นมูลค่า/บุคคล | เห็นผู้ติดตาม | รายงาน |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **admin** (HR Welfare) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ ทุกใบ | ✅ | ✅ | ✅ | ✅ |
| **manager** (หัวหน้า) | ✗ | ✗ | ✅ | ✅ | ✅ (ตาม DOA) | ✗ | ✅ | ✅ | ✗ (mask) | ✅ |
| **employee** | ✗ | ✗ | ✅ (ของตน) | ✅ (ของตน) | ✗ | ✅ (ของตน) | ✗ | ✗ (`•••`) | ✗ | ✗ |

- `canApprove` = admin|manager · `canSeeValue`/`canSeePerson` = admin|manager · `canSeeDependent` = **admin เท่านั้น** · `canCancelReq` = admin หรือ owner. **enforce backend** (BR-DOA-6 · OQ-05).

---

## §5.4 Field Validation Rules

| VR | Field/Action | เงื่อนไข | ประเภท | ข้อความ (verbatim จอ) | Error code |
|---|---|---|---|---|---|
| VR-01 | quota | ≤0 (เว้น percent) | Error | "โควตา/วงเงินต้องมากกว่า 0" | BR_QUOTA_INVALID |
| VR-02 | eff_from (edit) | ≤ วันมีผลเวอร์ชันเดิม | Error | "วันมีผลของเวอร์ชันใหม่ต้องหลัง … — ช่วงมีผลทับกันไม่ได้" | BR_EFFECTIVE_OVERLAP |
| VR-03 | groups | ว่าง | Error | "เลือกอย่างน้อย 1 กลุ่ม" | BR_GROUPS_REQUIRED |
| VR-04 | request value/amount | > คงเหลือ | Prevent | "ยื่นไม่ได้: เกินคงเหลือ" | BR_OVER_BALANCE |
| VR-05 | eligibility | นอกกลุ่ม/นอกช่วง/พ้นสภาพ | Prevent | "ยื่นไม่ได้: <เหตุ>" (เช่น "พนักงานพ้นสภาพแล้ว (leaver)…") | BR_NOT_ELIGIBLE |
| VR-06 | dependent dob | บุตร > 20 ปี | Error | "บุตรอายุเกิน 20 ปี — เกินเกณฑ์กลุ่ม" | BR_DEPENDENT_CHILD_AGE |
| VR-07 | dependent count | ≥ 3 | Warning (non-block) | เตือนเกินเกณฑ์ | BR_DEPENDENT_COUNT |
| VR-08 | reject/reverse reason | ว่าง | Error | "กรุณาระบุเหตุผล" | BR_REASON_REQUIRED |
| VR-09 | DOA slot | เลือกไม่ครบทุกขั้น | Prevent | "เลือกผู้อนุมัติให้ครบทุกขั้น" | BR_DOA_SLOT_INCOMPLETE |
| VR-10 | cancel | status ∉ {draft,pending_approval} | Prevent | "ยกเลิกได้เฉพาะร่าง/รออนุมัติ" | BR_CANCEL_NOT_ALLOWED |
| VR-11 | reverse | status ≠ approved หรือ !canApprove | Prevent | "กลับรายการได้เฉพาะคำขอที่อนุมัติแล้ว" | BR_REVERSE_NOT_ALLOWED |
| VR-12 | double-submit | คลิกซ้ำระหว่างบันทึก | Prevent | ปุ่ม is-disabled + "กำลัง…" (lockBtn) | — |

### Cross-field
- คงเหลือ = quota − SUM(approved) (ENG-WEL-02) · `use_for_dep_id` required เมื่อ use_for_type='dependent' · reversed_at ≥ approved_at.

---

## §5.5 Edge Cases

### Confirmed (BRD §10.1 · ☑)
- **EC-01** leaver ระหว่างคำขอค้าง → revoke · null last-day ≠ ทำงาน (BR-06) → TC AT-16.
- **EC-02** eligibility ผิดกลุ่ม/ช่วง = บล็อกพร้อมเหตุ (ห้ามบล็อกเงียบ) → AT-11.
- **EC-03** ใช้บางส่วน — คงเหลือถูกต้อง ใช้ต่อได้ → AT-09.
- **EC-04** ขอเกินคงเหลือ → บล็อก + แสดงยอด → AT-10.
- **EC-05** ปิดใช้ type ที่มีคำขอค้าง → เตือนจำนวนใบ (BR-DOA-8) → AT-03.
- **EC-06** กลับรายการหลังจ่ายแล้ว (pay=sent) → payroll_clawback flag (BR-11) → AT-24/XT-04.

### From Phase 2.5 probes (☐ AI-DEFAULT — รอ BA ยืนยัน, ดู OQ)
- **EC-07 (PR-1 concurrent · OQ-04):** 2 คำขอ pending สิทธิ์เดียวกัน อนุมัติพร้อมกัน → รวมเกินเพดาน. **`[AI-DEFAULT]`** re-check FIX-02 + **optimistic lock (version_lock)** + atomic backend; second → 409 ERR_STALE_DATA. → AT-26.
- **EC-08 (PR-7 idempotency):** double-click submit/approve. **`[AI-DEFAULT]`** Idempotency-Key → cached response, no duplicate INSERT/audit. → AT-21.
- **EC-09 (PR-3 permission mid-flight · OQ-05):** approver ถูก demote ก่อน commit. **`[AI-DEFAULT]`** re-check role ณ mutation (backend) → ERR_PERMISSION_REVOKED. → AT-23.
- **EC-10 (approver ในสาย DOA ลาออก/ย้ายกลางคัน):** สาย freeze แล้ว. **`[AI-DEFAULT]`** ค้างที่ขั้นนั้น → HR admin สามารถ reverse/จัดการ; re-resolve = OQ (กระทบสิทธิ์). → OQ-02.
- **EC-11 (reverse ซ้ำ):** reversed แล้วกลับอีก — reverse เฉพาะ approved ⇒ reversed กลับไม่ได้ (ถูกต้องโดยเจตนา · VR-11).
- **EC-12 (fiscal ปีสิทธิ์คร่อมปฏิทิน):** คงเหลือรีเซ็ตเมื่อไร → อ้าง HR Config (A-WEL-05) · reset ตามปีสิทธิ์จาก resolve.
- **EC-13 (HR Config resolve คืน company_scope ไม่ตรง):** fallback → OQ Phase B contract (OQ-03).
- **EC-14 (attachment ชนิด/ขนาด/virus):** policy deferred to impl (mock ปัจจุบัน).

---

## §5.6 Error Catalog

| Code | HTTP | i18n key | Cause |
|---|---|---|---|
| ERR_VALIDATION_FAILED | 400 | error.validation.failed | generic |
| ERR_NOT_AUTHENTICATED | 401 | error.auth.unauth | no/invalid token |
| ERR_INSUFFICIENT_ROLE | 403 | error.auth.role | role mismatch (BR-DOA-6) |
| ERR_PERMISSION_REVOKED | 403 | error.auth.revoked | mid-flight role change (EC-09) |
| ERR_NOT_FOUND | 404 | error.notfound | resource missing |
| ERR_DUPLICATE_IDEMPOTENCY_KEY | 409 | error.idempotency.dup | same key diff body |
| ERR_STALE_DATA | 409 | error.concurrency.stale | version mismatch (EC-07) |
| BR_QUOTA_INVALID | 422 | br.welfare.quota | VR-01 |
| BR_EFFECTIVE_OVERLAP | 422 | br.welfare.overlap | VR-02 / BR-03 |
| BR_GROUPS_REQUIRED | 422 | br.welfare.groups | VR-03 |
| BR_NOT_ELIGIBLE | 422 | br.welfare.eligible | VR-05 / BR-01 |
| BR_NOT_ELIGIBLE_AT_APPROVAL | 422 | br.welfare.eligible.approval | FIX-02 |
| BR_OVER_BALANCE | 422 | br.welfare.balance | VR-04 / BR-02 |
| BR_OVER_BALANCE_AT_APPROVAL | 422 | br.welfare.balance.approval | FIX-02 |
| BR_DEPENDENT_CHILD_AGE | 422 | br.welfare.dep.age | VR-06 |
| BR_DEPENDENT_COUNT | (warn) | br.welfare.dep.count | VR-07 |
| BR_REASON_REQUIRED | 422 | br.welfare.reason | VR-08 |
| BR_DOA_SLOT_INCOMPLETE | 422 | br.welfare.doa.slot | VR-09 |
| BR_APPROVE_PRECONDITION | 422 | br.welfare.approve.pre | BR-DOA-1 (FIX-01) |
| BR_CANCEL_NOT_ALLOWED | 422 | br.welfare.cancel | VR-10 (FIX-05) |
| BR_REVERSE_NOT_ALLOWED | 422 | br.welfare.reverse | VR-11 (OQ-WEL-01) |

---

## §5.7 Security Bible Application

> Domains: **D2, D5, D7, D9, D15, D17** · Preset **P6 HR/PII Sensitive**.

- **D2 Auth:** ทุก endpoint JWT · role admin/manager/employee.
- **D5 Financial:** `value` → audit mandatory (before/after) · **EC forward (approve) + EC reverse (reversal) คู่กัน** (BR-09/BR-11) · reconcile กับ Payroll (KPI-C2).
- **D7 PII:** employee/dependent snapshot → encrypt at rest · logs = ID reference (no PII).
- **D9 Audit:** ทุก mutation → T_welfare_audit_log append-only · 7 ปี · immutable.
- **D15 Admin actions:** ทุก transition logged · approver identity · reason บังคับ reject/reverse.
- **D17 Multi-tenant:** RLS + X-Tenant-Id · company_scope จาก HR Config.

### D-CLASS: Data Classification (per-field ที่ 04_DB §4.2/§4.6)
| Layer | Confidential (employee/dep snapshot, reason) | Restricted (`value`, dependent.name) |
|---|---|---|
| API response | mask if no permission | excluded ถ้าไม่ผ่าน ACL |
| UI | `•••` | hidden/`•••` + audit access |
| Export/Print | excluded ถ้า role ไม่ผ่าน | require Restricted Resources approval |
| Audit | view+mutation | view+mutation+export |

**Wire points:** Policy Center → Data Classification · Restricted Resources · DOA (approval ถ้า downgrade). **OQ-05:** enforce backend.

---

## §5.8 Compliance & Audit
| Requirement | Implementation |
|---|---|
| ภาษี/เงินได้ (7C · Revenue) | CSQ EC + EC reverse · reconcile Payroll (KPI-C2) |
| PDPA (PII บุคคล/ผู้ติดตาม) | D7 encrypt + retention + masking |
| Internal audit (SoD/approval) | DOA 2-step · Maker≠Approver · T_welfare_audit_log |
| Financial integrity | reversal append-only (ห้าม delete) · EC offset คู่ |
