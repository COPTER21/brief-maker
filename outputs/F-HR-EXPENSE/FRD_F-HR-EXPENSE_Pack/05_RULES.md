# 05_RULES — F-HR-EXPENSE · Expense Claim (เบิกค่าใช้จ่าย)

> **Audience:** Backend developer + QA
> **Principle:** Declarative — อ่านเข้าใจโดยไม่ต้องดูโค้ด

---

## §5.1 Business Rules (BR)

### BR-01: line — จำนวนเงิน > 0 · หมวดจาก HR Config · VAT คำนวณกลาง
- **Statement:** ทุกรายการ unit_price > 0 · cat ∈ HR Config (#107) · VAT (none/add/included) คำนวณด้วย ENG-EXP-01 (calcLineVat)
- **Enforced by:** API-02/04 + FN-01/FN-03/FN-04 · **Error:** `BR_LINE_AMOUNT_REQUIRED` → 422 · **Tag:** FIXED

### BR-02 (LOCK-05/08): เพดานหมวด — เกิน = เตือน + บังคับเหตุผล (ไม่ hard block)
- **Statement:** เพดานหมวด (HR Config resolve) — unit_price > cap → เตือน + บังคับ over_reason · **ยังส่งได้** (ไม่ hard block)
- **Enforced by:** FN-13 checkOverCap (UI + submit · defense-in-depth) · **Error:** `BR_OVERCAP_REASON_REQUIRED` → 422 · **Tag:** **CONFIGURABLE** 🤖 (เพดาน = HR Config #107 · group ยังไม่มี → mock · A-EXP-04 · OQ-02)

### BR-03: ≥1 รายการ + ยอด>0 + แนบใบเสร็จตามนโยบายหมวด ก่อนส่ง
- **Statement:** submit ได้เมื่อ line count>0 && grand>0 (FN-05) + ใบเสร็จหมวดบังคับครบ (FN-12)
- **Enforced by:** FN-06 submitClaim + FN-14 · **Error:** `BR_SUBMIT_NO_LINES` / `BR_RECEIPT_REQUIRED` → 422 · **Tag:** FIXED

### BR-04 (LOCK-01): ส่งอนุมัติ = DOA resolve ตามยอดรวม (threshold)
- **Statement:** resolve สายจากยอดรวม · **ช่วงวงเงิน FREE ตั้งค่าอิสระที่ DOA กลาง** · ไม่ hardcode สาย/ไม่ใช่ 3-tier ตายตัว · เลือกผู้อนุมัติครบทุก slot จึงส่งได้ (FN-08)
- **Enforced by:** FN-05/FN-06 · DOA engine (F-DLG-001) · **Error:** `BR_DOA_SLOTS_INCOMPLETE` → 422 · **Tag:** **CONFIGURABLE** 🤖 (DOA กลาง · **OQ-01** CL-0013 แขวน · role-id เคาะ)

### BR-05 (FN-11): แก้ยอดหลังส่ง → re-resolve DOA ถ้าข้ามช่วง
- **Statement:** ยอดเปลี่ยนข้ามช่วงวงเงิน → resolve สายอนุมัติใหม่อัตโนมัติ (resolve ตอน submit · freeze หลังส่ง)
- **Enforced by:** FN-05 (เรียกซ้ำได้) · **Tag:** FIXED

### BR-06 (LOCK-02): เลข EXP + สำเนา = ENG-DOC-NUM/STORE · ออกตอนอนุมัติ
- **Statement:** เลข `EXP-<พ.ศ.>-NNNN` + สำเนา PDF ออกตอนอนุมัติครบ (immutable) · ตัวนับ global เดินหน้าอย่างเดียว (ไม่ซ้ำ · pad 4)
- **Enforced by:** FN-11/FN-23 · **Error:** — · **Tag:** **CONFIGURABLE** 🤖 (รูปแบบเลข = DOCCFG · ห้าม hardcode)

### BR-07 (LOCK-04 · FN-19): อนุมัติ → 7C = FC + EC เท่านั้น (ไม่มี AC)
- **Statement:** อนุมัติครบสาย → emit **FC (commit งบ) + EC (มูลค่า)** · **ไม่ประกาศ AC** (Accounting ปลายทาง post เอง)
- **Enforced by:** FN-22 · CSQ_BRIEF · **Tag:** FIXED (มติล็อก · OQ-EXP-02)

### BR-08 (LOCK-06): ตำแหน่ง/ศูนย์ต้นทุน = snapshot Movement ณ วันเบิก
- **Statement:** position/cost_center resolve จาก Movement ณ วันเบิก (soft ref · **null≠ไม่มี**)
- **Enforced by:** FN-15 · **Tag:** FIXED

### BR-09 (LOCK-03): จ่ายจริง/post = hook display-only
- **Statement:** จ่าย (payroll/transfer/PV/petty) + สถานะ paid = **hook display-only** — **F101 ไม่จ่าย/ไม่ post บัญชี/ไม่ปรับ ledger**
- **Enforced by:** FN-12 · **Tag:** FIXED · **OQ-03** (contract ปลายทาง Phase B)

### BR-10 (LOCK-07): audit append-only + masking + ไม่มี hard delete
- **Statement:** ทุก mutation → append-only log · ตัวเงิน RESTRICTED mask ตาม role · ยกเลิก = soft archive
- **Enforced by:** FN-21, FN-18 · **Tag:** FIXED

### BR-11 (FN-18 · LOCK-09): หักลบเงินทดรอง = soft-ref F103 · display-only
- **Statement:** ยอดจ่ายสุทธิ = grand − offset (offset = min(adv, grand)) · **display-only** · **F101 ไม่ปรับ ledger F103** (ส่งค่าหักลบให้ F103)
- **Enforced by:** FN-16 · ENG-EXP-02 · **Tag:** FIXED (touchpoint · OQ-EXP-01)

### BR-12 (FN-20 · LOCK-10): visibility scope + เจ้าหน้าที่ไม่อนุมัติ
- **Statement:** scope:self (ผู้เบิก/ธุรการ เห็นใบตน) / scope:all (ผู้อนุมัติ, เจ้าหน้าที่ HR/Finance) · **เจ้าหน้าที่ HR/Finance approver:false** (เห็นทุกใบแต่กดอนุมัติไม่ได้)
- **Enforced by:** FN-19 visibleDocsByScope · FN-20 canApprove · **Tag:** FIXED (RBAC · OQ-04)

### BR-13 (SoD): อนุมัติ/ตีกลับได้เฉพาะ role approver:true
- **Statement:** approve/reject เฉพาะ canApprove (re-check ที่ mutation) · กัน self-approve (ผู้เบิก approver:false)
- **Enforced by:** FN-07/FN-08/FN-20 · **Error:** `ERR_NOT_APPROVER` → 403 · **Tag:** FIXED (RBAC · OQ-04)

### BR-14 (FN-01/92): wizard ล็อกลำดับ + กัน double-submit
- **Statement:** wizard 5 ขั้น ล็อกลำดับ (STEP_KEYS) · step-advance gate (ขั้น2 มีผู้เบิก · ขั้น3 มีรายการ+ยอด>0) · ทุก action เปลี่ยนสถานะกัน double-submit (`state._busy`) + Idempotency-Key
- **Enforced by:** FN-06/07/08/09 (busy guard) · **Tag:** FIXED

### BR-15 (§3.4 OQ-EXP-04): ตรวจงบ F117 + สิทธิ์สวัสดิการ F102 = hook display-only
- **Statement:** ยอด > งบคงเหลือ (F117 mock) → เตือน · หมวดสวัสดิการ > สิทธิ์ (F102 mock) → เตือน · **display-only** (อ่านจริงตอน dev)
- **Enforced by:** FN-17 · **Tag:** **DYNAMIC** 🤖 (F117 W7 ยังไม่ dev / F102 ctl · OQ-EXP-04)

### BR-18 (reject reason): ไม่อนุมัติต้องระบุเหตุผล
- **Statement:** reject → reason required (ปุ่ม disabled จนกรอก · UX-06) · **Error:** `ERR_REASON_REQUIRED` → 400 · **Tag:** FIXED (D15)

---

## §5.2 State Machines

### Expense Claim (8 state · lifecycle)
```
draft ──ยื่น(submit)──▶ pending_approval ──อนุมัติครบสาย──▶ approved ──เลือกจ่าย(hook)──▶ sent_to_pay ──จ่ายจริง(hook)──▶ paid ──▶ closed
  │                          │
  │                          └──ตีกลับ(reason)──▶ rejected ──แก้/ยื่นใหม่(reopen)──▶ draft
  └──ยกเลิก(ฉบับร่าง)──▶ cancelled (soft archive)
```

| From | To | Action | Roles | Conditions |
|---|---|---|---|---|
| draft | pending_approval | ยื่น (submit) | ผู้เบิก | canSubmit: grand>0 + line>0 + over_reason ครบ + slot ครบ (FN-05/04/08) |
| draft | cancelled | ยกเลิก | ผู้เบิก | **เฉพาะฉบับร่าง** (FN-14) |
| pending_approval | approved | อนุมัติครบสาย | ผู้อนุมัติ DOA | ครบทุกขั้น → เลข+PDF+FC/EC (auto) |
| pending_approval | rejected | ตีกลับ (+เหตุผล) | ผู้อนุมัติ DOA | reason required (BR-18) |
| rejected | draft | แก้แล้วยื่นใหม่ (reopen) | ผู้เบิก | **เฉพาะ rejected** (FN-13 · กันเลขหาย) |
| approved | sent_to_pay | เลือก/ส่งช่องทางจ่าย (hook) | เจ้าหน้าที่/ผู้เบิก | display-only |
| sent_to_pay | paid | ปลายทางจ่ายจริง (hook อ่านกลับ) | ระบบ | display-only จาก Payroll/Finance |
| paid | closed | ปิดงาน | ระบบ | — |

> **HTML implements:** draft/pending_approval/approved/rejected/cancelled/paid (pill DST L2182) · sent_to_pay/closed = state ปลายทาง (hook · display-only)
> **⚠️ OQ-05:** ไม่มี transition "approved/paid → cancelled" ในระบบปัจจุบัน — ถ้า BA ต้องการ ต้องนิยาม reverse EC/release FC (EC-05)

---

## §5.3 Permission Matrix

| Role | View (scope) | Create/Edit/ยื่น | ยกเลิก (ร่าง) | Approve/Reject (DOA) | เลือกจ่าย (hook) | Unmask money |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| ผู้เบิก / ธุรการ (`admin`) | เฉพาะใบของตน (self) | ✅ (ใบของตน) | ✅ | ❌ | ✅ | ✅ ใบของตน · ❌ ใบคนอื่น (mask `฿ •••••`) |
| ผู้อนุมัติ (DOA · `mgr`) | ทั้งหมด (all) | ✅ | ✅ | ✅ | ✅ | ✅ (ต้องเห็นเต็มเพื่ออนุมัติตามวงเงิน) |
| เจ้าหน้าที่ (HR/Finance · `officer`) | ทั้งหมด (all) | ✅ ติดตาม | — | **❌ ไม่ใช่ผู้อนุมัติ** | ✅ | ✅ (unmask · ติดตาม/กระทบยอด) |

> **OQ-04:** mapping role→login จริง + สิทธิ์ "ธุรการสร้างแทนผู้เบิก" — SEC/BA เคาะ

---

## §5.4 Field Validation Rules

| Field | Rule | Error |
|---|---|---|
| `emp_id` | required (combobox #102) | ERR_VALIDATION_FAILED |
| `date` | required (พ.ศ.) | ERR_VALIDATION_FAILED |
| `pay` | required ∈ {payroll,transfer,pv,petty} | ERR_VALIDATION_FAILED |
| line `cat` | required ∈ HR Config #107 | ERR_VALIDATION_FAILED |
| line `unit_price` | required > 0 | BR_LINE_AMOUNT_REQUIRED |
| line `vat_mode` | ∈ {none,add,included} | ERR_VALIDATION_FAILED |
| line `over_reason` | required เมื่อ over-cap | BR_OVERCAP_REASON_REQUIRED |
| `receipt` | required ตามนโยบายหมวด (travel/lodge/ent) | BR_RECEIPT_REQUIRED |
| submit slots | ทุก slot มีผู้อนุมัติ | BR_DOA_SLOTS_INCOMPLETE |
| `reason` (reject) | required | ERR_REASON_REQUIRED |

**Cross-field:** grand = Σ line_total (totals · single source · computed) · over-cap = unit_price > cat.cap · submit precede: grand>0 + reasons ครบ + slots ครบ · เลข/PDF/7C ออกครั้งเดียวตอนอนุมัติครบ

---

## §5.5 Edge Cases (from Phase 2.5 Probing · Lane Mode `[AI-DEFAULT]`)

> Feature patterns → probes: approve/multi-step → **PR-1, PR-3** · mutation → **PR-4, PR-7** · cancel/reverse → **PR-8** · financial/threshold → **PR-9**
> ทุก `[AI-DEFAULT]` = conservative default (ล็อกไว้ก่อน) → carry เป็น OQ ให้ BA/SEC/Finance confirm

### EC-01: Concurrent approval (PR-1) `[AI-DEFAULT]`
- **Scenario:** 2 approver กด approve/reject ขั้นเดียวกันพร้อมกัน (BRD §10.2 [CA])
- **Resolution:** optimistic lock (`version`) — first commits, second → 409 `ERR_STALE_DATA`
- **Test:** TC-CC-01 (AC-17)

### EC-02: Permission mid-flight (PR-3) `[AI-DEFAULT]`
- **Scenario:** approver โดน demote ระหว่างเปิดหน้า แล้วกด approve
- **Resolution:** re-check canApprove ที่ **mutation time** → 403 `ERR_NOT_APPROVER`/`ERR_PERMISSION_REVOKED` (`doApprove` guard L2442)
- **Test:** TC-PR-01 (AC-18) · เกี่ยว OQ-04 (RBAC)

### EC-03: Network failure / double-submit (PR-4/PR-7) `[AI-DEFAULT]` (บางส่วน confirmed)
- **Scenario:** กด submit/approve/reject/cancel ซ้ำ (network ขาด/double-click)
- **Resolution:** Idempotency-Key (cache 24ชม) ทุก mutation · **UI `state._busy` guard** (confirmed ใน HTML L2428/2440/2474/2480)
- **Test:** TC-ID-01 (AC-14)

### EC-04: ตำแหน่ง/cost_center = null (ไม่มี assignment · [DI]) `[AI-DEFAULT]`
- **Scenario:** ผู้เบิกไม่มี Movement assignment ณ วันเบิก (BRD §10.1 · S-05)
- **Resolution:** null≠ไม่มี (BR-08) — snapshot เก็บ null · แสดง "—" ไม่ block · **Test:** TC-DI-01

### EC-05: ยกเลิก/แก้หลังออกเลข + ยิง FC/EC (PR-8) `[AI-DEFAULT]` → **OQ-05**
- **Scenario:** ต้องการยกเลิก/แก้ใบ **หลังอนุมัติ (เลข+FC/EC แล้ว)** (BRD §10.2 [ST] · กระทบเงิน)
- **Resolution (conservative):** **ระบบปัจจุบันไม่มี path นี้** — cancel เฉพาะ draft · reopen เฉพาะ rejected · ถ้า BA เปิด path → ต้องนิยาม **reverse EC / release FC commit** · flag Finance → **OQ-05 (รอ BA/Finance)**
- **Test:** TC-CANCEL-EC-01 (XT-04)

### EC-06: หักลบทดรอง เมื่อทดรอง > ยอดใบเบิก (CL) — fallback มีแล้ว
- **Scenario:** advance_outstanding > grand
- **Resolution:** net_pay = max(0, grand − offset) = 0 · adv_remain = adv − grand (ทดรองคงค้าง) · fallback ENG-EXP-02 (advanceClear Math.max) · **Test:** TC-ADV-01 (AC-11)

### EC-07: เจ้าหน้าที่ HR/Finance เห็นทุกใบ unmask — export/PDF ก็เคารพ scope/mask (PM)
- **Resolution:** FN-18 mask ทั้ง UI + API response + export/PDF ตาม role (ใบของตน/ผู้อนุมัติ/เจ้าหน้าที่ เห็นเต็ม · ใบคนอื่นสำหรับ mask:true = mask) · **Test:** TC-MASK-01 (AC-12/16)

### EC-08: ยอด > งบ (F117) / เกินสิทธิ์สวัสดิการ (F102) — display-only
- **Scenario:** grand > งบคงเหลือ mock / หมวดสวัสดิการ > สิทธิ์ mock
- **Resolution:** FN-17 เตือน display-only (ไม่ block · OQ-EXP-04) · **Test:** TC-HOOK-01

---

## §5.6 Error Catalog

| Code | HTTP | Message (i18n key) | Cause |
|---|---|---|---|
| `ERR_VALIDATION_FAILED` | 400 | error.validation.failed | field validate (FN-92) |
| `ERR_REASON_REQUIRED` | 400 | error.reason.required | reject ไม่ระบุเหตุผล (BR-18) |
| `ERR_NOT_AUTHENTICATED` | 401 | error.auth.unauth | no token |
| `ERR_INSUFFICIENT_ROLE` | 403 | error.auth.role | role ไม่พอ (ผู้เบิกสร้างใบคนอื่น) |
| `ERR_NOT_APPROVER` | 403 | error.auth.approver | ไม่ใช่ canApprove (BR-13/EC-02) |
| `ERR_PERMISSION_REVOKED` | 403 | error.auth.revoked | role เปลี่ยนกลางคัน (EC-02) |
| `ERR_NOT_FOUND` | 404 | error.notfound | record หาย |
| `ERR_STALE_DATA` | 409 | error.concurrency.stale | version mismatch (EC-01) |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | error.idempotency.dup | key เดิม body ต่าง |
| `BR_LINE_AMOUNT_REQUIRED` | 422 | br.line.amount | unit_price ≤ 0 (BR-01) |
| `BR_SUBMIT_NO_LINES` | 422 | br.submit.nolines | ไม่มีรายการ/ยอด=0 (FN-05/BR-03) |
| `BR_OVERCAP_REASON_REQUIRED` | 422 | br.overcap.reason | เกินเพดานไม่มีเหตุผล (BR-02) |
| `BR_RECEIPT_REQUIRED` | 422 | br.receipt.required | ใบเสร็จหมวดบังคับไม่ครบ (FN-12/BR-03) |
| `BR_DOA_SLOTS_INCOMPLETE` | 422 | br.doa.slots | เลือกผู้อนุมัติไม่ครบ (BR-04) |
| `BR_NOT_PENDING_APPROVAL` | 422 | br.approve.notpending | อนุมัติใบที่ไม่ได้รออนุมัติ |
| `BR_NO_PENDING_STEP` | 422 | br.doa.nopending | ไม่มีขั้น pending |
| `BR_CANCEL_ONLY_DRAFT` | 422 | br.cancel.onlydraft | ยกเลิกใบที่ไม่ใช่ฉบับร่าง (FN-14) |
| `BR_REOPEN_ONLY_REJECTED` | 422 | br.reopen.onlyrejected | reopen ใบที่ไม่ถูกตีกลับ (FN-13) |

---

## §5.7 Security Bible Application

> Domains: **D2, D5, D7, D9, D15, D17** · Security Preset **P6 (HR/PII Sensitive · 15 controls)**

### D2 Authentication — JWT ทุก endpoint · role-based (RBAC กลาง · persona demo = scaffolding)
### D5 Financial — ยอด/เพดาน/VAT/ทดรอง/FC/EC → audit mandatory · **ไม่ auto-post บัญชี / ไม่จ่ายเอง** (LOCK-03/04) · approval (DOA มีวงเงิน) · 7C = FC/EC (ไม่มี AC)
### D7 PII — emp_snapshot/approver = PII → PDPA scope · no PII in logs (ref id) · encrypt at rest (column)

### D-CLASS: Data Classification (per-field ดู 04_DB §4.2/§4.6)
| Layer | Confidential (emp/approver/reason) | Restricted (grand/unit_price/line_total/advance/FC·EC) |
|---|---|---|
| API response | mask ถ้าไม่ผ่าน role | excluded/mask `฿ •••••` ใบคนอื่น (mask:true role) |
| UI | snapshot/`***` | `฿ •••••` (ใบคนอื่น) · เต็ม (ใบตน/approver/officer) |
| Export/Print (PDF) | excluded ถ้า role ไม่ผ่าน | mask + require Restricted Resources |
| Audit | view+mutation | view+mutation+export |

**Wire:** Policy Center → Data Classification + Restricted Resources (OQ · 00_OVERVIEW §0.8)

### D9 Audit — ทุก mutation → T_expense_audit_log (append-only · ≥7 ปี · immutable · ไม่มี hard delete)
### D15 Admin/Approval — approve/reject/ออกเลข/ส่งจ่าย logged · approver identity · reason required (reject) · SoD (Maker≠Approver · officer ไม่อนุมัติ)
### D17 Multi-Tenant — RLS + X-Tenant-Id · cross-tenant forbidden · scope guard self/all (FN-20)

---

## §5.8 Compliance & Audit
| Requirement | Implementation |
|---|---|
| PDPA (ข้อมูลพนักงาน) | D7 encryption + retention + snapshot |
| SoD/COSO (Maker≠Approver) | ผู้เบิกยื่น · ผู้อนุมัติ DOA อนุมัติ · officer ไม่อนุมัติ |
| Audit trail | T_expense_audit_log append-only |
| Access control | RBAC (OQ-04) + scope self/all (FN-20) + masking (FN-94) |
| Money visibility segregation | RESTRICTED masking ใบคนอื่น (maskM) |
