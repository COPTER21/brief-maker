# 07_LOCKED_DECISIONS — F-BNK Bank Master (บัญชีธนาคาร)

> **Audience:** All roles
> **Purpose:** Scope Lock (imported) + Locked Decisions — ห้ามเปิดอภิปรายซ้ำ

---

## §7.0 Scope Lock (Imported from LOCKED DECISIONS Strike 2026-08-11 + BRD §3.4 + GL Contract) ⭐ IMMUTABLE

> ข้อยืนยันจากมติ Strike 2026-08-11 (OQ-BNK-01..04) + GL Posting Group Contract — ห้าม override ตลอด pack และตลอด chain ปลายน้ำ (HTML/Test/Dev).
> **Conflict rule:** LOCK ชนะทุกกรณี. Ref: LOCKED DECISIONS (Strike 2026-08-11) + BRD §3.4 + F-PG DevPack.

| LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะใน FRD |
|---|---|---|---|
| **OQ-BNK-01 = NO** | เส้น Bank Master → Payment Method (F-0.20) **ตัดทิ้ง** · PM คง COA-direct · Bank Master ไม่ expose ให้ PM · ไม่ถือเป็น interface | Strike 2026-08-11 | ✅ สอดคล้อง — 02_API §2.7 (CUT row) · 00 §0.5 · 06 XT-05 (negative) · ไม่มี endpoint/UI ไป PM |
| **OQ-BNK-02 = binding OPTIONAL** | บันทึกได้โดยไม่ผูกกลุ่ม GL (view เตือน "GL post ไม่ได้จนกว่าจะผูกกลุ่ม") · picker เห็นเฉพาะ active (F-PG BR-06) · **คงกลุ่มที่ผูกไว้เดิม (แม้ draft) กันหลุด** (edge SCB-01) | Strike 2026-08-11 | ✅ BR-04 · 03_FN-14 (keep-bound) · 06 AT-11/AT-12 |
| **OQ-BNK-03 = IR-BNK-01 CONFIRMED** | `used>0` → ล็อก **ธนาคาร + เลขที่บัญชี** เท่านั้น (UI disabled + lock-tag + logic guard) · field อื่นแก้ได้ · ลบไม่ได้ (bulk ข้าม) · `used` = count Receipt/PV posted · **ไม่โชว์บนจอ** | Strike 2026-08-11 | ✅ BR-02 · 03_FN-02 (save guard) · 06 AT-08/AT-09/AT-15 |
| **OQ-BNK-04 = CONFIRMED** | Receipt/PV เลือกเฉพาะ active + ฝั่งตรง · ★ pre-select · snapshot ตอนบันทึก (ฝั่งปลายทางยังไม่ทำ) | Strike 2026-08-11 | ✅ BR-05 · 02_API-11/§2.7 · 03_FN-13b · 06 XT-01/XT-02 |
| **GL Contract** | soft-ref → GL Posting Group (F-PG kind=bank) · resolve บัญชีเงินฝากผ่านกลุ่ม (account_1) · master **ไม่เก็บ COA ตรง** · `?kind=bank` (**NOT `?type=`**) · **generic F-PG-API-01** (ไม่มี endpoint เฉพาะ) · active-only คืน KBANK เท่านั้น (SCB=draft filtered) | F-PG DevPack | ✅ 02_API §2.6 (3 drifts) · 04_DB (posting_group varchar, NO FK) · 03_FN-14 |
| **Pattern (VD-PDM)** | สถานะ 3 ค่าอิสระ ไม่มีอนุมัติ · statusMenu + bulk · **ไม่มีลบเดี่ยว** · import 3 จังหวะ merge-only · export roundtrip · ตัด hint/field-help · **ไม่โชว์ used** | เลน + มติ r2 | ✅ §5.2 + 01_UI (no single-delete, no hint) + BR-07 |
| **Governance** | DOA null (4 placeholder = null) · NOTIF ไม่ emit · THB-only (สกุลเงิน disabled) · CI v8 Warm Light · Iron Rules #29/#96/#97 · Esc chain | LOCK เลน | ✅ 00 §0.7 + 01_UI §1.0 + 04_DB (DOA null) + BR-09 |

- **Scope Lock Ref:** LOCKED DECISIONS (Strike 2026-08-11 · OQ-BNK-01..04) + BRD §3.4 + GL Posting Group Contract (F-PG DevPack).
- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** **ไม่มี** — ทุก spec สอดคล้อง LOCK. จุด tension เดียว (เส้นออก Payment Method) ถูกปิดโดย **OQ-BNK-01 = NO**. GL mock list ที่ list ทั้ง KBANK+SCB = integration note (Drift D-2), ไม่ใช่ scope drift — DEV ใช้ generic API-01 active-only จริง.

---

## §7.1 Locked Decisions (LD)

### LD-B-01: เส้น → Payment Method ตัดทิ้ง (OQ-BNK-01 = NO)
- **Date:** 2026-08-11 · **ผู้ตัดสิน:** Strike
- **Context:** เดิมพิจารณาให้ PM ชี้บัญชีจากทะเบียนนี้แทน COA ตรง
- **Decision:** **ไม่เอา** — PM คง `default_acct = COA` ตรง · Bank Master ไม่ต้อง expose ให้ PM · OQ-PM-02 ไม่เกี่ยว Bank Master แล้ว
- **Implications:** ไม่มี endpoint/UI/edge ไป PM · 02_API §2.7 (CUT) · 06 XT-05 negative
- **Reversibility:** MEDIUM (ถ้ากลับมา = เพิ่ม interface + endpoint)

### LD-B-02: GL binding OPTIONAL + picker active-only + keep-bound draft (OQ-BNK-02)
- **Date:** 2026-08-11 · **ผู้ตัดสิน:** Strike
- **Context:** SCB=ร่างใน F-PG · ควรบังคับผูกกลุ่มก่อนเปิดใช้ไหม
- **Decision:** binding **optional** (บันทึกได้ view เตือน) · picker เฉพาะ active (F-PG BR-06) · **คงกลุ่มที่ผูกไว้เดิมแม้ draft** (union current-bound) กันหลุด
- **Implications:** BR-04 · 03_FN-14 (`.filter(g=>g.status==='active'||g.code===current)`) · 06 AT-11/AT-12 · ไม่มี validation บล็อกตอน save
- **Reversibility:** EASY (เพิ่ม required guard ได้)

### LD-B-03: IR-BNK-01 — ล็อกเฉพาะ ธนาคาร+เลขบัญชี เมื่อ used>0 (OQ-BNK-03)
- **Date:** 2026-08-11 · **ผู้ตัดสิน:** Strike (ปลด [AI-DRAFT])
- **Context:** ต่างจาก Tax Code ที่ล็อกทั้งใบ — ต้องล็อกแค่ไหน
- **Decision:** ล็อก **2 field** (ธนาคาร + เลขที่บัญชี) เท่านั้น เมื่อ used>0 · field อื่นแก้ได้ · ลบไม่ได้ (bulk ข้าม) · เปลี่ยนเลข = เปิดบัญชีใหม่แทน · `used` = count Receipt/PV posted · **ไม่โชว์บนจอ**
- **Options:** A) ล็อกทั้งใบ (Tax Code) · **B) ล็อก 2 field (chosen)** — เอกสารเก่า snapshot ป้องกันผลกระทบ, ให้ยืดหยุ่นแก้ metadata
- **Implications:** 03_FN-02 (save guard `if(!locked){data.bank=…}`) · BR-02 · 06 AT-08/AT-09 · EC-01/EC-03
- **Reversibility:** MEDIUM (เปลี่ยน scope ของ lock)

### LD-B-04: Receipt/PV flow — active+ฝั่งตรง+★+snapshot (OQ-BNK-04)
- **Date:** 2026-08-11 · **ผู้ตัดสิน:** Strike
- **Context:** เอกสารปลายทาง (Receipt/PV) ยังไม่ทำ — ต้องประกาศ contract
- **Decision:** picker เลือกเฉพาะ active + ฝั่งตรง · ★ ฝั่งนั้น pre-select · snapshot ค่าตอนบันทึก
- **Implications:** 02_API-11 GET /active?side= · 03_FN-13b · BR-05 · 06 XT-01/XT-02 · enforce จริงที่ feature ปลายทาง
- **Reversibility:** EASY (contract ประกาศไว้, ปลายทางยังไม่ build)

### LD-B-05: GL contract = generic F-PG-API-01 `?kind=bank&status=active` (3 drifts) — DEV ห้ามลอก mock
- **Date:** 2026-08-11 · **Owner:** Architect / F-PG owner (OQ-BNK-06)
- **Context:** mock ใน HTML มี 3 จุดที่ต่างจาก f-postgrp as-built
- **Decision:** consume **generic F-PG-API-01** (ไม่มี endpoint เฉพาะ) · ใช้ `?kind=bank` (NOT `?type=`) · active-only จริงคืน **KBANK เท่านั้น** (SCB=draft filtered) · เก็บเฉพาะ `posting_group.code` (NO FK) · resolve บัญชีเงินฝากผ่าน account_1 ของกลุ่ม ตอน post (external GL engine)
- **Implications:** 02_API §2.6 (D-1/D-2/D-3) · 03_FN-14 · 04_DB posting_group varchar no-FK · 06 XT-03
- **Reversibility:** N/A (real upstream contract — ต้อง confirm กับ F-PG owner ก่อน cutover)

### LD-B-06: ไม่มี CUBIC engine ของ feature นี้ (§3.2 ว่างโดยตั้งใจ)
- **Date:** 2026-08-11 · **ผู้ตัดสิน:** BA (Design Authority)
- **Context:** sibling F-PAY มี 2 engines; Bank Master = registry + validation ล้วน
- **Decision:** ไม่ register engine — logic ทั้งหมดเป็น scope-local function (FN-01..14). GL resolve + `used` increment = **external GL engine** (นอก scope, contract §3.4/§2.7)
- **Implications:** 03_LOGIC §3.2 empty (R9 satisfied via note) · R8 trace ไม่มี engine column · variant ยังเป็น FULL เพราะ state/lock/integration complexity
- **Reversibility:** EASY (register engine ทีหลังถ้าต้อง standardize cross-feature resolver)

### LD-B-07: Optimistic lock + Idempotency (conservative default)
- **Date:** 2026-08-11 · **ผู้ตัดสิน:** `[AI-DEFAULT AD-BNK-02]` — Phase 2.5 probe (PR-1/PR-7) — pending OQ-BNK-CC-01
- **Context:** concurrency (2 admin ตั้ง ★ ฝั่งเดียวกัน) + double-submit · HTML mock ไม่มี race แต่ production networked
- **Decision:** PUT/POST-status require `If-Match` (version) → 409 stale · POST/import require `Idempotency-Key`
- **Implications:** 02_API §2.3 · 04_DB `version` column · 05_RULES EC-08/EC-09 · TC-CC-01/TC-ID-01
- **Reversibility:** MEDIUM (API contract)

---

## §7.2 Convention Deviations

### CD-01: Route model = single-view SPA + overlay (hash route เดียว)
- **Convention default:** list/detail/create มี hash route แยก
- **Deviation:** HTML prototype = single view `#/bank-master` + overlay (openCreate/openView/bulkImport) — navigation ภายใน = function calls
- **Reason:** HTML SoT as-built (gate-passed). 01_UI §1.0 บันทึก route (observed) = trigger + route (production) เสนอ 1:1
- **Approved by:** HTML gate (UX/Coverage/E2E R1 21/21 + R2 15/15) · **Apply to:** ทุกหน้า P-01..06

### CD-02: DELETE ทำผ่าน POST /bulk-delete (ไม่มี DELETE /:id)
- **Convention default:** DELETE /resource/:id (single)
- **Deviation:** ไม่มี single-delete — bulk เท่านั้น (POST) + guard used>0 + confirm modal
- **Reason:** pattern เลน VD-PDM ("ไม่มีลบเดี่ยว") + soft-guard steer used>0 ไปเปลี่ยนสถานะแทน
- **Approved by:** SCOPE_LOCK · **Apply to:** F-BNK-API-07

### CD-03: IR-BNK-01 field-lock = logic guard (ไม่ใช่ DB constraint)
- **Convention default:** immutable field = DB trigger/constraint
- **Deviation:** ล็อก ธนาคาร+เลขบัญชี ที่ logic/API (FN-02 save guard) ไม่ใช่ DB — เพราะแก้ field อื่นในแถวเดียวกันได้
- **Reason:** ล็อกเฉพาะ 2 field เมื่อ used>0 (conditional, per-field) — DB constraint จะล็อกทั้งแถว
- **Approved by:** LD-B-03 · **Apply to:** F-BNK-FN-02 + UI disabled

---

## §7.3 Open Questions Promoted to LD
> เมื่อ OQ ปิด → move ที่นี่. ปัจจุบัน pending (ดู 00_OVERVIEW §0.8):
- OQ-BNK-06 (GL 3 drifts source), OQ-BNK-07 (used def — blocking), OQ-BNK-08 (masking level), OQ-BNK-CC-01 (concurrency) — ยังเปิด, ยังไม่ promote.
- OQ-BNK-01..04 = ปิดแล้ว (LOCK Strike 2026-08-11) → import เป็น §7.0 + LD-B-01..04.

---

## §7.4 Architecture Tradeoffs Acknowledged

### AT-01: Soft-reference snapshot over FK cascade
- **Tradeoff:** ข้อมูล snapshot ซ้ำในเอกสารปลายทาง vs. integrity guarantee (แก้/ปิดบัญชี ไม่พังเอกสารเก่า)
- **Accepted:** YES — reuse Payment Term / Tax Code pattern · เสริมด้วย IR-BNK-01 (ล็อก ธนาคาร+เลขบัญชี) กันแม้ snapshot เพี้ยน

### AT-02: posting_group = code varchar (soft-ref) over FK
- **Tradeoff:** ไม่มี referential integrity ระดับ DB vs. decoupling จาก F-PG (resolve ผ่านกลุ่มตอน post)
- **Accepted:** YES (มาตรฐาน BC Bank Posting Group) — GL engine ตรวจ valid ตอน post · picker keep-bound draft กันหลุด

### AT-03: ไม่มี engine ของ feature (registry-only)
- **Tradeoff:** GL resolve + used increment ต้องพึ่ง external GL engine vs. self-contained
- **Accepted:** YES — Bank Master = master registry; resolve = concern ของ GL module (declared §2.7/§3.4)

### AT-04: Server-side validation mirror ของ mock UI
- **Tradeoff:** duplicate logic (UI + server) vs. security (C4 — client validation ไม่พอ)
- **Accepted:** YES — F-BNK-FN-03 mirror `saveBank()` + `bulkValidateRow()`

---

## §7.5 Decisions Deferred to Implementation
| Item | Owner | Deadline |
|---|---|---|
| นิยาม `used` precise (นับ draft Receipt/PV?) — **blocking delete/lock guard** | FRD/BA (OQ-BNK-07) | ก่อน dev delete/IR guard จริง |
| GL posting_group source (3 drifts, generic API-01) — confirm F-PG endpoint live | Architect / F-PG owner (OQ-BNK-06) | ก่อน dev GL picker/resolve cutover |
| account_no masking level (ตาราง/def-grid) + access log | Security (OQ-BNK-08) | ก่อน production (Confidential) |
| Concurrency policy (★ ฝั่งเดียวกัน) | BE/Architect (OQ-BNK-CC-01) | pre-deploy |
| Receipt/PV picker+snapshot flow build | BA (feature ปลายทาง, OQ-BNK-04) | รอ feature Receipt/PV |
| Cache strategy /active + F-PG picker (Redis TTL) | DevOps | pre-deploy |

---

## §7.6 References
- **Scope Lock source:** LOCKED DECISIONS (Strike 2026-08-11 · OQ-BNK-01..04) + BRD §3.4 + GL Posting Group Contract
- **GL contract:** DevPack_F-PG_GL-Posting-Group / 03_FRD/02_API.md (F-PG-API-01) — §2.6
- **CUBIC Registry:** ไม่มี engine ของ feature นี้ (LD-B-06)
- **Related:** Payment Term / Tax Code master (soft-ref snapshot pattern) · Receipt/PV (downstream, ยังไม่ทำ)
