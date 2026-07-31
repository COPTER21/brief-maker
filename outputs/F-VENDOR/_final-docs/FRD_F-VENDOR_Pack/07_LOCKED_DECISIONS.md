# 07_LOCKED_DECISIONS — F-VENDOR ทะเบียนคู่ค้า

> **Audience:** All delivery roles  
> **Purpose:** บันทึกข้อยืนยันและข้อยุติที่ปลายน้ำห้ามตีความใหม่โดยไม่มี change approval

---

## §7.0 Scope Lock

| LOCK-ID | Confirmation | Evidence | Status |
|---|---|---|---|
| LOCK-01 | ไม่มี Scope Lock เพิ่มเติมสำหรับ feature Vendor | ผู้ใช้ยืนยันในบทสนทนาก่อนเริ่ม FRD, ย้ำ 2026-07-31 | ✅ applied |
| LOCK-02 | BRD v1.1 ใช้เป็นฐาน FRD ได้ | ผู้ใช้ตอบ `ยืนยัน` 2026-07-31 | ✅ applied |
| LOCK-03 | `../vendor.html` ล่าสุดเป็น UI source of truth | ผู้ใช้ตรวจและอนุมัติ HTML ก่อนขอสร้างเอกสารต่อ | ✅ applied |
| LOCK-04 | งานนี้สร้างเอกสารเท่านั้น ไม่มี codebase/implementation | ผู้ใช้ระบุชัดในบทสนทนา | ✅ applied |
| LOCK-05 | ห้ามใช้ `plan-from-spec` | ผู้ใช้ระบุชัดในบทสนทนา | ✅ applied |

**Scope Lock Ref:** N/A — ไม่มีใบเซ็น/Scope Lock ภายนอก; ใช้ explicit user confirmations ข้างต้น  
**Drift:** ไม่มี pack item ขัดกับ LOCK; historical BRD/HTML drift ถูกแก้ด้วย LD ด้านล่าง

## §7.1 Locked Decisions

### LD-01: Approved HTML is authoritative for UI

- **Date:** 2026-07-31
- **Decision:** route, surfaces, action visibility, UI state และ microcopy ยึด `../vendor.html`
- **Rationale:** เป็น artifact ล่าสุดที่ผู้ใช้ manual review และอนุมัติ
- **Implication:** old `vendor-master.html`, ZIP และ BRD screen detail เป็น historical reference
- **Reversibility:** ต้องแก้ HTML, re-approve แล้ว regenerate/drift-check downstream docs

### LD-02: Policy Center owns approval-chain resolution

- **Decision:** Vendor ส่งข้อมูลให้ Policy Center resolve chain; Vendor ไม่กำหนด credit threshold, role chain หรือ fallback production chain
- **Supersedes:** BRD BR-A03 placeholder threshold
- **Implication:** Policy timeoutทำให้ submit ล้มเหลวโดยคง state เดิม
- **Reversibility:** LOW; เปลี่ยน ownershipกระทบ policy governance และหลายโมดูล

### LD-03: OT is not automatically approved

- **Decision:** OT ยกเว้น tax ID/verified bank ได้ตาม rule แต่ยังผ่าน KYC และ Policy Center approval decision
- **Supersedes:** BRD BR-A04 `chain=[] auto-approve`
- **Rationale:** สอดคล้อง approved HTML และ governance เดียวกันทุก vendor type
- **Reversibility:** ต้องอนุมัติ policy/security change

### LD-04: Lifecycle has seven vendor states

- **Decision:** `draft`, `pending_kyc`, `pending_approval`, `active`, `blocked`, `inactive`, `blacklisted`
- **Supersedes:** old `prospect` terminology and six-state descriptions
- **Rationale:** `inactive` คือ normal offboarding; `blocked` คือ risk/operational hold; blacklist terminal
- **Implication:** rejectกลับ `pending_kyc`, not draft; all docs/tests must align

### LD-05: Soft-disable persisted child records

- **Decision:** persisted address, verified bank, attachment และ vendor masterไม่ hard delete
- **Behavior:** draft/new unpersisted childลบจาก formได้; active address/verified bankใช้ deactivateและเก็บ audit
- **Rationale:** transaction references, identity matching และ audit integrity
- **Implication:** no cascade delete; consumer history remains

### LD-06: Address role reassignment is explicit

- **Decision:** ลบ/ปิดใช้ billing/shipping address clear role และบังคับ userเลือก replacementก่อน save; ห้าม auto-assign silently
- **Rationale:** userต้องรับรู้ปลายทางใบกำกับ/จัดส่ง
- **Implication:** DB partial uniqueness + aggregate validation

### LD-07: Sanctions hit forces failed KYC and block

- **Decision:** เมื่อ sanctions hit ปุ่ม pass disabled, source+note required, actionเป็น `ไม่ผ่านและบล็อกคู่ค้า`
- **Evidence:** approved HTML revision requested by user
- **Implication:** source/note/reviewer/timeเป็น append-only KYC evidence

### LD-08: Verified bank is immutable

- **Decision:** verified bank fields read-only; correctionใช้ new account + deactivate old accountโดย Finance
- **Rationale:** evidence/audit consistency
- **Implication:** deactivating last verified bank does not change vendor active but payment eligibility false

### LD-09: Optimistic concurrency and idempotent mutations

- **Decision:** use vendor `version`/If-Match plus Idempotency-Key
- **Source:** active PR-1/PR-2/PR-4/PR-7 probes; conservative `[AI-DEFAULT]`
- **Implication:** first commit wins; retry replays original result; no duplicate audit
- **Reversibility:** MEDIUM; API/storage contract change

### LD-10: Transaction eligibility is a reusable pure engine

- **Decision:** centralize PO/PV readiness in F-VENDOR-ENG-01 and expose API-19
- **Rationale:** E-007 and Payment need identical interpretation of active/KYC/bank gates
- **Implication:** register/review in CUBIC before production or preserve identical scope-local contract

### LD-11: No A4 PDF artifact in Vendor Master

- **Decision:** skip `thai-doc-pdf-generator`
- **Rationale:** feature stores attachments but does not issue a PR/PO/invoice/letter/form PDF
- **Implication:** if future vendor application/certificate PDF is added, treat as new scoped document requirement

### LD-12: KYC failed without sanctions returns for correction

- **Decision:** failed without sanctions requires a note and keeps/returns vendor `pending_kyc`; only sanctions hit forces vendor `blocked`
- **Rationale:** approved HTML supports correction/resubmission and approved BRD explicitly reserves forced block for sanctions hit
- **Implication:** HTML, API-07, FN-07, rules and tests must preserve this distinction

## §7.2 Historical Drift Resolution

| Historical statement | Final decision |
|---|---|
| status `prospect` | use `draft` |
| six lifecycle states | use seven states including `inactive` |
| approval thresholds in Vendor | Policy Center owns decision |
| OT auto-approve | no auto-approve |
| technical `decision ref` note visible in UI | removed from user UI; reference stays backend/audit |
| `รออนุมัติ (0/1)` note | removed |
| `PO ยังไม่พร้อม` section | removed; eligibility remains backend/downstream contract |
| technical soft-block/match-key message | removed from user UI |
| reject subtitle says draft | implementation must say/perform `pending_kyc` consistently |
| address deletion without role cleanup | explicit cleanup + replacement requirement |
| missing approval chain creates Manager fallback | no local fallback; keep prior state and ask the user to retry |
| verified bank deactivates immediately | require a confirmation reason and preserve it in audit/history |
| unblock claims PO/PV are always ready | KYC + Policy gate unblock; PV additionally depends on verified bank |

## §7.3 Convention Deviations

### CD-01: Feature identifier is `F-VENDOR`

- **Convention default:** `F-XX`
- **Deviation:** retain Central Plan canonical node ID `F-VENDOR`; derived IDs are `F-VENDOR-API-NN`, `F-VENDOR-FN-NN`, `F-VENDOR-ENG-NN`
- **Reason:** cross-module graph E-002/E-007 and existing artifacts use `F-VENDOR`; renaming would break traceability
- **Approved source:** Central Plan

### CD-02: Custom action uses POST

- `/submit-kyc`, `/kyc-decisions`, `/submit-approval`, `/approval-decisions`, `/block`, `/unblock`, `/deactivate`, `/blacklist`
- Reason: each is audited domain action/state transition, not generic field patch

No CI deviation is declared; UI follows current html-generator-v6 and approved HTML.

## §7.4 Architecture Tradeoffs

| ID | Choice | Accepted tradeoff |
|---|---|---|
| AT-01 | PostgreSQL RLS + tenant middleware | extra query/session complexity for stronger isolation |
| AT-02 | immutable review/approval rounds | more rows/storage for defensible audit |
| AT-03 | no local Policy fallback | temporary submission unavailability instead of governance drift |
| AT-04 | soft-disable master/children | storage growth instead of broken transaction references |
| AT-05 | synchronous eligibility read + status events | consumers can verify current truth while events reduce stale cache |

## §7.5 Deferred Decisions

| Item | Owner | Related OQ |
|---|---|---|
| production sanctions provider/SLA | Security/Compliance | OQ-01 |
| KYC expiry policy | Compliance/Policy Center | OQ-02 |
| Price List summary ownership | Architect | OQ-03 |
| attachment limits/retention | Security/Product | OQ-04 |
| notification channels | Product/Platform | OQ-05 |
| Restricted Resources ACL/policy registration | Security/Policy Center | OQ-06 |
| physical stack/framework/migration tool | Tech Lead after codebase exists | implementation |

Deferred items may not weaken conservative behaviors in this pack without review.
