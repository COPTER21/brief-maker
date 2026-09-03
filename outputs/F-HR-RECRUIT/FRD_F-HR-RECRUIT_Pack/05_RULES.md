# 05_RULES — F-HR-RECRUIT (F127) สรรหา / Recruit

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + Validation + State Machine + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านเข้าใจโดยไม่ต้องดูโค้ด

---

## §5.1 Business Rules (BR) — จาก BRD §9 (คง numbering เพื่อ traceability)

### BR-01: req ต้องอนุมัติ (DOA) ครบก่อนประกาศ
- **Statement:** req เข้า status=open ได้เมื่อ approval_chain ทุก slot = approved
- **Enforced by:** F127-FN-04 approveApprovalStep + F127-FN-06 announceRequisition
- **Error:** `BR_REQ_NOT_APPROVED` → 422 · **Tag:** FIXED

### BR-02: consent PDPA + retention ก่อนเก็บ/ดำเนินการ
- **Statement:** เก็บผู้สมัครได้ (แม้ consent=false) แต่ **ดำเนินต่อ (คัดกรอง/สัมภาษณ์/ข้อเสนอ) ไม่ได้จนกว่า consent_ok=true** · retention period อ่านจาก Policy Center
- **Enforced by:** F127-FN-12 moveCandidateStage (guard) + FN-13/FN-15 (assess/offer guard)
- **Error:** `BR_CONSENT_REQUIRED` → 422 · **Tag:** CONFIGURABLE (retention period · **OQ-16 ค้างค่า · ห้าม hardcode**)

### BR-03: ทุก pipeline transition ต้อง audit
- **Statement:** ทุก create/แก้/เลื่อน/อนุมัติ/hire/close → append T_recruit_audit
- **Enforced by:** F127-FN-21 appendAudit (เรียกในทุก mutation) · **Tag:** FIXED

### BR-04: offer ต้องอนุมัติ (DOA) ก่อนเสนอ · เงินตามระดับ (band soft-ref)
- **Statement:** offer sent ได้เมื่อ status=approved (DOA ครบ) · salary อ้าง band
- **Enforced by:** F127-FN-16/17 + FN-18a sendOffer · **Error:** `BR_OFFER_NOT_APPROVED` → 422 · **Tag:** FIXED (flow)

### BR-05: hired → ยิง handoff On/Offboard (event · ไม่สร้าง employee)
- **Statement:** candidate hired → emit `recruit.candidate.hired` (fire-and-forget) · **ไม่สร้าง employee record**
- **Enforced by:** F127-FN-19 hireCandidate · **Tag:** FIXED · **OQ-15** ฝั่งรับ (ไม่บล็อกฝั่งเรา)

### BR-06: ข้อมูลผู้สมัคร RESTRICTED · masking + PDPA ตาม role
- **Statement:** name/contact/resume = Restricted · mask ตาม role (recruiter unmask · manager/viewer mask) + mask เมื่อ !consent
- **Enforced by:** F127-FN-23 maskCandidatePII · 04_DB §4.6 · **Tag:** FIXED

### BR-07: audit append-only · soft archive (talent pool)
- **Statement:** audit ไม่ลบ/แก้ · terminate = soft archive (stage=talent_pool/rejected/withdrawn · ไม่ลบ record)
- **Enforced by:** T_recruit_audit append-only + F127-FN-20 · **Tag:** FIXED

### BR-08: อัตราอ้าง Manpower = hook · null ไม่บังคับ (เตือน)
- **Statement:** manpower_ref=null → บันทึกได้ + audit kind=warn + chip "ไม่มีแผน" · **ไม่บล็อก**
- **Enforced by:** F127-FN-01 createRequisition · **Tag:** CONFIGURABLE (เมื่อ F124 มีจริง) · A-REC-01

### BR-09: snapshot ผู้สัมภาษณ์ + freeze band version_id
- **Statement:** ผู้สัมภาษณ์ = Employee snapshot ณ นัด · band_version_id freeze ณ สร้าง offer (ไม่ re-resolve)
- **Enforced by:** F127-FN-13 (interviewer snapshot) + FN-15 createOffer (band freeze) · **Tag:** FIXED

### BR-10: duplicate detect email/phone → เตือน ไม่บล็อก
- **Statement:** match email/phone → dup_flag + chip "เคยสมัคร" · **บันทึกได้ปกติ**
- **Enforced by:** F127-FN-09 + ENG-RCT-02 · **Tag:** CONFIGURABLE (match field · Admin)

---

## §5.2 State Machine

### Requisition
```
draft ──submit-approval(DOA)──▶ pending ──approve ครบ slot──▶ approved ──announce──▶ open
open ──filled≥count──▶ closed
draft/approved/open ──cancel(confirm+reason)──▶ cancelled
```
| From | To | Action | Roles | Conditions |
|---|---|---|---|---|
| draft | pending | submit-approval | recruiter/manager | fields ครบ · DOA resolve |
| pending | approved | approve | manager (slot) | ทุก slot approved (SoD maker≠approver) |
| pending | draft | reject | manager (slot) | reason required |
| approved | open | announce | recruiter/manager | — |
| open | closed | (auto) | system | filled≥count |
| draft/approved/open | cancelled | close | recruiter/manager | confirm + reason (guard active candidate · OQ-17) |

### Candidate (pipeline)
```
applied ─▶ screening ─▶ interview ─▶ offer ─▶ hired(→handoff event)
  └─(ทุกขั้น)─▶ rejected / withdrawn / talent_pool
```
**Guards:** เลื่อน dir>0 ต้อง consent_ok=true (BR-02) · เข้า offer ต้องมี offer object · เข้า hired ต้อง offer.status=accepted **และ route ผ่าน hire เท่านั้น** (FIX-01 · ไม่ move-stage ตรง).

### Offer
```
pending ──DOA approve──▶ approved ──send──▶ sent ──respond──▶ accepted / declined
```
| From | To | Action | Conditions |
|---|---|---|---|
| pending | approved | approve | DOA slot ครบ (BR-04) |
| approved | sent | send | — |
| sent | accepted | respond | — → พร้อม hire |
| sent | declined | respond | reason? → candidate.withdrawn |

> Transitions enforced: F127-FN-04/06/07 (req) · FN-12/19/20 (candidate) · FN-16/17/18/18a (offer).

---

## §5.3 Permission Matrix

| Role | View | Create req/cand | Edit | Move stage | Approve (DOA) | Consent | Offer | Hire | Terminate | Restricted data |
|---|---|---|---|---|---|---|---|---|---|---|
| recruiter | all | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ (unmask) |
| manager (Hiring) | all | ✅ | ✅ | ✅ | **✅ (slot)** | ✅ | ✅ | ✅ (co-sign) | ✅ | mask |
| viewer | all (masked) | — | — | — | — | — | — | — | — | ✗ (mask) |

> **VR-05:** viewer = read-only จริง — ปุ่มสร้างซ่อน + `viewerGuard()` (F127-FN-24) ต้นทุก mutation (FIX-02 · 15 จุด). persona = prototype demo (Iron #105) · prod ผูก role master.

---

## §5.4 Field Validation Rules

### Per-field
| Field | Rule | Error code |
|---|---|---|
| requisition.position | required | `BR_REQUIRED_FIELD` (VR-01) |
| requisition.count | required, int ≥1 | `BR_INVALID_COUNT` |
| requisition.grade_code | required, in HR Config | `BR_INVALID_GRADE` |
| requisition.hiring_manager | required, active employee | `BR_INVALID_HM` |
| candidate.name | required | `BR_REQUIRED_FIELD` |
| candidate.contact | อย่างน้อย 1 (email/phone) | `BR_CONTACT_REQUIRED` |
| offer.start_date | required | `BR_REQUIRED_FIELD` |
| offer.salary | required, > 0 | `BR_REQUIRED_FIELD` |
| offer.out_of_range_reason | required ถ้า salary นอก band | `BR_OUT_OF_BAND_REASON` (VR-03) |
| terminate.reason | required | `BR_REASON_REQUIRED` |

### Cross-field
- offer.salary in [band.min, band.max] → else warn + require reason (VR-03 · CONFIGURABLE HR Config)
- candidate stage เลื่อน dir>0 → consent_ok=true (BR-02)
- hired → offer.status=accepted (FIX-01)
- **VR-02 double-submit:** RC.busy guard + loader (ปุ่ม disable · FIX-07)
- **VR-04 DOA dynamic:** สาย resolve runtime จาก Policy Center — **ห้าม hardcode** (declaration)

---

## §5.5 Edge Cases (from BRD §10 + Phase 2.5 Lane Mode probing)

### EC-01: no-consent → บล็อกดำเนินต่อ (E1 · confirmed)
- **Scenario:** consent_ok=false → เลื่อน/สัมภาษณ์/offer
- **Resolution:** guard block → `BR_CONSENT_REQUIRED` · toast "ยังไม่ได้รับความยินยอม PDPA — เลื่อนสถานะไม่ได้" · mask contact
- **Test:** AT-11

### EC-02: duplicate email/phone → เตือน (E2 · confirmed)
- **Resolution:** dup_flag + chip "เคยสมัคร" + live note ใน form — **ไม่บล็อก** (BR-10)
- **Test:** AT-08

### EC-03: เปิดอัตราไม่มี Manpower → เตือน ทำได้ (A1 · confirmed)
- **Resolution:** manpower_ref=null → บันทึก + audit warn + chip "ไม่มีแผน" (BR-08)
- **Test:** AT-02

### EC-04: offer salary นอก band → เตือน + บังคับเหตุผล (confirmed)
- **Resolution:** note + out_of_range_reason บังคับ · freeze band snapshot ยังคง (VR-03)
- **Test:** AT-14

### EC-05: board ข้ามขั้นไป hired โดยไม่ผ่าน offer accepted (FIX-01 · confirmed)
- **Resolution:** move-stage → hired บล็อก (`BR_HIRE_ROUTE_ONLY`) · hire route เดียว (F127-FN-19) · offer ยังไม่ accepted → toast "ต้องให้ผู้สมัครตอบรับข้อเสนอก่อน"
- **Test:** AT-16

### EC-06: viewer เรียก mutation ทางอ้อม (FIX-02 · confirmed)
- **Resolution:** viewerGuard (F127-FN-24) block + re-guard mid-drawer (OQ-D3) · toast "สิทธิ์อ่านอย่างเดียว"
- **Test:** AT-24

### EC-07 `[AI-DEFAULT]` (PR-1): concurrent stage move
- **Scenario:** 2 recruiter เลื่อนผู้สมัครคนเดียวกันพร้อมกัน
- **Resolution:** optimistic lock (If-Match/version) — first wins, second → 409 `ERR_STALE_DATA` · audit ทั้งคู่
- **Owner:** BA confirm (OQ-D1) · **Test:** AT-26

### EC-08 `[AI-DEFAULT]` (OQ-17): req closed/cancelled ขณะ pipeline ค้าง
- **Scenario:** cancel req ที่มี active candidate
- **Resolution (conservative):** ไม่ยกเลิก candidate อัตโนมัติ · close(cancelled) require reason + warn "มีผู้สมัครค้างใน pipeline" · candidate ค้างยังจัดการต่อได้ (offer อาจ declined ภายหลัง)
- **Owner:** BA/HR (OQ-17) · **Test:** AT-25

### EC-09 `[AI-DEFAULT]` (PR-7): idempotency / double-submit network
- **Resolution:** Idempotency-Key required บน mutation · same key+body → cached (OQ-D2) · **Test:** AT-21

### EC-10 `[AI-DEFAULT]` (EM): NTF ยิงล้มเหลว
- **Resolution:** queue/retry ผ่าน ENG-NOTIFY — **ไม่บล็อก** business transition (OQ-D4)

### EC-11 `[AI-DEFAULT]` (DI): band version เปลี่ยนหลังสร้าง offer ก่อน accept
- **Resolution:** ยึด **freeze snapshot** (band_version_id) — ไม่ re-resolve (BR-09) · **Test:** AT-14
### EC-12 (DI): hiring_manager/interviewer ถูกลบจาก Employee Master → ใช้ snapshot (BR-09)

---

## §5.6 Error Catalog

| Code | HTTP | Message (i18n key) | Cause |
|---|---|---|---|
| `ERR_VALIDATION_FAILED` | 400 | error.validation.failed | field validation |
| `ERR_NOT_AUTHENTICATED` | 401 | error.auth.unauth | no/invalid token |
| `ERR_INSUFFICIENT_ROLE` | 403 | error.auth.role | viewer / role mismatch (VR-05) |
| `ERR_NOT_IN_SLOT` | 403 | error.doa.slot | approve นอก slot (SoD) |
| `ERR_NOT_FOUND` | 404 | error.notfound | resource missing |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | error.idempotency.dup | same key diff body |
| `ERR_STALE_DATA` | 409 | error.concurrency.stale | version mismatch (EC-07) |
| `ERR_INVALID_STATE` | 409 | error.state.invalid | state machine violation |
| `BR_REQ_NOT_APPROVED` | 422 | br.req.notapproved | BR-01 |
| `BR_CONSENT_REQUIRED` | 422 | br.consent.required | BR-02 / EC-01 |
| `BR_OFFER_REQUIRED` | 422 | br.offer.required | เข้า offer stage ไม่มี offer |
| `BR_OFFER_NOT_APPROVED` | 422 | br.offer.notapproved | BR-04 |
| `BR_OFFER_NOT_ACCEPTED` | 422 | br.offer.notaccepted | hire ก่อน accepted (EC-05) |
| `BR_HIRE_ROUTE_ONLY` | 422 | br.hire.routeonly | move-stage→hired (FIX-01) |
| `BR_OUT_OF_BAND_REASON` | 422 | br.band.reason | VR-03 |
| `BR_REASON_REQUIRED` | 422 | br.reason.required | terminate/cancel |
| `BR_DOA_UNRESOLVED` | 422 | br.doa.unresolved | Policy Center ไม่คืน chain |
| `BR_BAND_UNRESOLVED` | 422 | br.band.unresolved | Salary Structure ไม่คืน band |

---

## §5.7 Security Bible Application

> Domains: **D2, D7, D9, D15, D17** (Preset P6 — HR/PII)

### D2: Authentication
- ทุก endpoint JWT · TTL 1h · refresh 7d

### D7: PII Protection (⭐ core)
- candidate name/contact/resume = **Restricted + PII** — mask ตาม role + consent gate (BR-02/BR-06)
- encrypt at rest (contact/resume column-level)
- API response: no full PII unless permitted role · logs: no PII (ID refs)
- **PDPA:** consent ก่อนเก็บ/ดำเนิน · retention จาก Policy Center (OQ-16) · **microcopy ห้ามระบุ "เก็บไม่มีวันหมดอายุ"** (FIX-03) · withdraw consent → OQ-16

### D-CLASS: Data Classification ⭐
รายละเอียด per-field → 04_DB §4.2 + §4.6

| Layer | Confidential (salary/score/band) | Restricted (candidate PII) |
|---|---|---|
| API response | mask if no permission | excluded/masked ถ้าไม่ผ่าน ACL |
| UI display | `***` | mask + consent gate |
| Export/Print | excluded ถ้า role ไม่ผ่าน | require Restricted Resources approval |
| Audit | view + mutation | view + mutation + **access log** |

**Wire points:** Policy Center → Data Classification · Restricted Resources (OQ-R1) · PDPA consent scope + retention (OQ-16).

### D9: Audit Logging
- ทุก mutation + Restricted access → T_recruit_audit · retention ≥7y · append-only (BR-03/BR-07)

### D15: Admin/Approval Actions
- ทุก DOA approval + status transition logged · approver identity + slot recorded · reject/cancel/terminate require reason

### D17: Multi-Tenant Isolation
- PostgreSQL RLS ทุกตาราง · middleware validate X-Tenant-Id · cross-tenant forbidden

---

## §5.8 Compliance & Audit
| Requirement | Implementation |
|---|---|
| PDPA (consent + retention) | BR-02 · D7 · retention config (OQ-16) |
| Data classification (RESTRICTED applicant) | D-CLASS · 04_DB §4.6 · Policy Center |
| SoD (Maker≠Approver) | §5.2 DOA · recruiter≠manager |
| Audit trail | T_recruit_audit append-only · ≥7y |
| Scope Lock (ไม่สร้าง employee ฯลฯ) | ดู 07_LOCKED §7.0 |
