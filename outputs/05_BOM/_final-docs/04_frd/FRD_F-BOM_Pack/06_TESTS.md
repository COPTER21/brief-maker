# 06_TESTS — F-BOM-001 สูตรการผลิต (Bill of Materials)

> **Audience:** QA + Developers  
> Coverage sources: BRD S-01..08, BR-01..15, VR-01..08, EC-01..10, APIs, functions, ENG-01, Scope Lock and downstream contracts.

---

## §6.1 Acceptance Criteria

### AC-01 — Open create wizard

**Given** authenticated Planner is at `#/bom`  
**When** selecting `สร้างสูตรใหม่`  
**Then** route is `#/bom/create`, Step 1 label is `ข้อมูลสูตร`, and no mutation occurs.

### AC-02 — Create draft or active

**Given** valid active FG, at least one valid component/UoM, unique version and positive quantities  
**When** selecting `บันทึกร่าง`  
**Then** API-02 creates `draft`, forces `is_default=false`, persists lines and one create audit.  
**When** instead selecting `บันทึก + เปิดใช้งาน`  
**Then** API-02 creates `active`, calculates cost using ENG-01, and applies requested default atomically.

### AC-03 — Exactly one active default

**Given** FG has active default A and active non-default B  
**When** B is saved as default  
**Then** B becomes default and A is cleared in the same transaction.  
**And** changing B to `draft` or `inactive` clears its default flag.

### AC-04 — Navigate sibling versions

**Given** an FG has multiple BOM versions  
**When** P-04 renders `เวอร์ชันอื่นของสินค้านี้ (${others.length})` and the user activates another version  
**Then** route changes to that record’s `#/bom/view/:id` and its detail is displayed.

### AC-05 — Amend referenced BOM without rewriting MO

**Given** BOM `used>0` and an existing MO stores its recipe snapshot  
**When** Planner saves an amended line set with current `If-Match`  
**Then** BOM version increments and audit is written, while the existing MO snapshot remains byte-for-byte unchanged under AID-01.

### AC-06 — Server validation matches visible errors

**Given** any VR-01..08 violation  
**When** the form attempts next/save or a caller bypasses UI and invokes API  
**Then** the mutation is blocked; UI preserves input and shows the verbatim HTML message where defined; API returns the stable code.

### AC-07 — Component/UoM cascade

**Given** a line has component/UoM  
**When** component changes  
**Then** old UoM is cleared and only active UoMs in the new component base category are selectable; server independently rejects a forged incompatible UoM.

### AC-08 — All-direction status change without approval

**Given** a BOM in any of three states  
**When** authorized Planner requests either other state with current version  
**Then** the transition succeeds without approval; target non-active clears default and writes audit.

### AC-09 — Guarded bulk delete

**Given** selection mixes `used=0` and `used>0`  
**When** confirmation `ลบสูตรการผลิต ${ids.length} รายการ?` is accepted  
**Then** only unused records are deleted, used records return `BR_BOM_IN_USE`, audit tombstones remain, and UI shows the full ledger. If all are used, the destructive button is disabled.

### AC-10 — Confidential cost

**Given** one caller has cost permission and another does not  
**When** both open list/detail  
**Then** the first sees server-calculated cost and `cost_as_of`; the second receives no raw cost (`null`, `cost_masked=true`) across list/detail/form, and API-07 never exposes cost.

## §6.2 Test Case Inventory

### Business-rule coverage

| TC ID | Scenario | Expected | Trace | Priority |
|---|---|---|---|:---:|
| TC-BR-01 | versions `v1` and `V1` same FG | second blocked | BR-01 | P0 |
| TC-BR-02 | concurrent set-default | final state has exactly one active default | BR-02 | P0 |
| TC-BR-03 | inactive/non-FG parent | blocked | BR-03 | P0 |
| TC-BR-04 | inactive/FG component | blocked | BR-04 | P0 |
| TC-BR-05 | parent as component or nested FG | blocked | BR-05 | P0 |
| TC-BR-06 | forged cross-category UoM | blocked server-side | BR-06 | P0 |
| TC-BR-07 | known decimal inputs | exact ENG-01 line/total/unit result | BR-07 | P0 |
| TC-BR-08 | every pair of status transitions | all six succeed for Planner | BR-08 | P1 |
| TC-BR-09 | edit request includes fake cost | ignored; current Item cost used and protected | BR-09 | P0 |
| TC-BR-10 | unknown status | `BR_BOM_STATUS_INVALID` | BR-10 | P0 |
| TC-BR-11 | delete referenced BOM | skipped/blocked | BR-11/AID-02 | P0 |
| TC-BR-12 | amend referenced BOM | BOM changes, prior MO snapshot does not | BR-12/AID-01 | P0 |
| TC-BR-13 | import/export route/control probe | absent/404; no UI control | BR-13 | P2 |
| TC-BR-14 | scrap 0, 100, >100 | first two pass; >100 blocked | BR-14/AID-04 | P1 |
| TC-BR-15 | deactivate master after activation | read works; next save blocks until corrected | BR-15/AID-05 | P1 |

### Validation coverage

| TC ID | Input | Expected visible text / code |
|---|---|---|
| TC-VR-01 | parent empty | `เลือกสินค้าผลผลิตก่อน` / `BR_BOM_PARENT_REQUIRED` |
| TC-VR-02a | version blank | `ระบุเวอร์ชันสูตร (เช่น v1)` / `BR_BOM_VERSION_REQUIRED` |
| TC-VR-02b | duplicate normalized version | `เวอร์ชัน ${f.ver} ของสินค้านี้มีอยู่แล้ว` / `BR_BOM_VERSION_DUPLICATE` |
| TC-VR-03 | name blank | `ระบุชื่อสูตร` / `BR_BOM_NAME_REQUIRED` |
| TC-VR-04 | lines empty | `ต้องมีส่วนประกอบอย่างน้อย 1 รายการ` / `BR_BOM_LINE_REQUIRED` |
| TC-VR-05 | qty 0/negative | `ปริมาณของ ${l.item} ต้องมากกว่า 0` / `BR_BOM_NUMERIC_RANGE` |
| TC-VR-06 | component duplicate | `วัตถุดิบ ${l.item} ซ้ำ — รวมเป็นรายการเดียว` / `BR_BOM_COMPONENT_DUPLICATE` |
| TC-VR-07 | component equals parent | `ส่วนประกอบห้ามเป็นตัวสินค้าเอง (${l.item}) — กัน BOM วน` / `BR_BOM_SELF_COMPONENT` |
| TC-VR-08 | forged incompatible UoM | not offered in UI; API `BR_BOM_UOM_INVALID` |

### Confirmed edge coverage

| TC ID | Setup/action | Expected |
|---|---|---|
| TC-EC-01 | default A then default B | only B true |
| TC-EC-02 | Unicode/case-equivalent version | normalized duplicate blocked |
| TC-EC-03 | duplicate component rows | no silent merge; mutation blocked |
| TC-EC-04 | component=parent | blocked at UI and API |
| TC-EC-05 | change component category | prior UoM cleared/filter refreshed |
| TC-EC-06 | default active → inactive/draft | default false atomically |
| TC-EC-07 | mixed used/unused bulk delete | success/skip totals and rows correct |
| TC-EC-08 | cost 0 and null | total deterministic; missing flag for null |
| TC-EC-09 | scrap=100 | effective qty and cost exactly double pre-scrap |
| TC-EC-10 | later master deactivation | historical read preserved; save fails closed |

### Reliability, security and scope

| TC ID | Scenario | Expected | Priority |
|---|---|---|:---:|
| TC-CC-01 | two updates use same `version_no` | first success; second `409 ERR_STALE_DATA` | P0 |
| TC-CC-02 | bulk status races single edit | per-record version ledger; no silent overwrite | P1 |
| TC-ID-01 | same key+body repeated within 24h | identical response; no duplicate DB/audit | P0 |
| TC-ID-02 | same key+different body | `409 ERR_IDEMPOTENCY_CONFLICT` | P0 |
| TC-NF-01 | server commits but response is lost | retry same key returns committed response | P1 |
| TC-BULK-01 | one forbidden, one stale, one valid | 207 with skip/fail/success; valid commits | P1 |
| TC-SEC-01 | no cost permission | no raw cost in response/DOM/client state | P0 |
| TC-SEC-02 | permission revoked before bulk mutation | denied per record at execution | P0 |
| TC-SEC-03 | cross-tenant BOM ID | not found/no data leak | P0 |
| TC-SEC-04 | audit inspection | actor/action/time/source/result/diff present; no secret | P1 |
| TC-NUM-01 | exceeds numeric precision | `BR_BOM_NUMERIC_RANGE` | P1 |
| TC-NUM-02 | repeating decimal/rounding boundary | decimal HALF_UP scale 6 matches all layers | P1 |
| TC-STATE-01 | client sends `draft + is_default=true` | persisted `draft + false` | P0 |
| TC-SCOPE-01 | approval endpoints/UI | absent | P1 |
| TC-SCOPE-02 | multi-level/routing controls | absent | P1 |
| TC-SCOPE-03 | import/export/print/PDF | absent | P1 |
| TC-SCOPE-04 | inventory/GL posting after save | no posting/event/ledger row | P0 |

## §6.3 Test Data Setup

- tenants: `tenant-bom-a`, `tenant-bom-b`
- users/capabilities: Planner with/without cost, Production, Costing, Auditor, revoked Planner
- Item masters: active FG x2; active RM/PM/TR across at least two UoM categories; inactive items; zero-cost and null-cost component
- UoM masters: active/inactive values in Weight, Count and Volume; include tenant-added `SET`
- BOMs: each status; two versions for one FG; one active default; one referenced by MO; one unused
- MO fixture: immutable snapshot referencing a BOM and a live usage counter/relationship

Use generated non-production identities. Do not place API keys, passwords, tokens, cookies, or real confidential cost data in fixtures/reports.

## §6.4 Definition of Done

### Code and data

- [ ] API-01..07 implemented with schema tests
- [ ] FN-01..09 and ENG-01 unit tests pass; logic-layer coverage ≥80%
- [ ] migration, constraints, unique races, RLS and append-only grants tested
- [ ] all mutation paths are idempotent/audited and all bulk paths return a ledger

### UI and integration

- [ ] P-01..04 match route/action/state/microcopy contracts
- [ ] Item/UoM/D-CLASS/MO adapters pass contract tests
- [ ] current HTML regression `outputs/05_BOM/02_QC/e2e_bom.py` remains 26/26
- [ ] sibling-version navigation remains clickable and keyboard accessible

### QA/security/release

- [ ] all P0/P1 cases pass; no open P0/P1 defects
- [ ] no raw Confidential cost without permission and no secret in audit/error
- [ ] performance targets pass with agreed load profile
- [ ] rollback keeps business/audit data; monitoring/alert ownership confirmed
- [ ] AID defaults accepted or replaced consistently across all seven files

## §6.5 Events / Notifications

No WebSocket or Notification Center event is declared. Audit records and HTTP results are not user-notification events.

## §6.6 Performance Benchmarks `[AI-DEFAULT]`

| Surface | Dataset/load | Target p95 |
|---|---|---:|
| API-01 list | 100k BOM headers/tenant, page 20, 50 concurrent | ≤500ms |
| API-03 detail | 500 lines + 200 audit rows paged, 50 concurrent | ≤500ms without cost; ≤1s with cost |
| API-02/API-04 | 500 lines, 20 concurrent | ≤2s |
| API-05/API-06 | 100 selected records | ≤2s excluding dependency outage |
| API-07 eligible | 50 versions, include lines false | ≤500ms |

Exact production load profile remains OQ-BOM-08. No pass/fail claim should be made from mock-only browser timing.

## §6.7 Test Environment Notes

- integration DB must support real RLS, partial unique indexes and transaction isolation; an in-memory substitute is insufficient for concurrency gates
- mock Item/UoM/Policy/MO adapters with deterministic fault modes, plus at least one staging contract run against each actual service
- freeze clock only in unit tests; API timestamps remain UTC
- use arbitrary-precision decimal assertions, not JavaScript/Python binary float equality

## §6.8 AC → API → Logic Coverage

| AC | API | Functions | Engine |
|---|---|---|---|
| AC-01 | — route | — | — |
| AC-02 | API-02 | FN-03/FN-05/FN-08 | ENG-01 |
| AC-03 | API-02/API-04/API-05 | FN-03/FN-04/FN-06/FN-08 | — |
| AC-04 | API-03 | FN-02 | ENG-01 if permitted |
| AC-05 | API-04/API-07 | FN-04/FN-09 | ENG-01 |
| AC-06 | API-02/API-04 | FN-05 | — |
| AC-07 | upstream + API-02/API-04 | FN-05 | — |
| AC-08 | API-05 | FN-06/FN-08 | — |
| AC-09 | API-06 | FN-07 | — |
| AC-10 | API-01/API-03/API-07 | FN-01/FN-02/FN-09 | ENG-01 |

No function or engine is orphaned: FN-01 appears in AC-10/list tests; FN-02 AC-04/10; FN-03 AC-02/03; FN-04 AC-03/05; FN-05 AC-02/06/07; FN-06 AC-03/08; FN-07 AC-09; FN-08 AC-02/03/08; FN-09 AC-05/10; ENG-01 AC-02/04/05/10.

## §6.9 Cross-Module Test Cases (R12)

| ID | Scenario | Module | Expected |
|---|---|---|---|
| XT-01 | MO requests eligible BOMs for FG | Production/MO | active only; default first; no cost |
| XT-02 | MO selects BOM then BOM lines change | Production/MO | saved MO snapshot unchanged; a new MO receives current version |
| XT-03 | active BOM becomes inactive after MO creation | Production/MO | existing MO snapshot remains; API-07 excludes it for new MO |
| XT-04 | Costing caller opens BOM | Item Master + Costing | formula uses current standard costs and reports `cost_as_of` |
| XT-05 | Item cost changes between reads | Costing | recalculated value changes deterministically; no false accounting posting |
| XT-06 | Item/UoM service unavailable during mutation | upstream masters | mutation fails `ERR_MASTER_DATA_UNAVAILABLE`; no partial aggregate/audit |
| XT-07 | audit append fails | audit adapter | mutation rolls back under AID-08 |
| XT-08 | D-CLASS denies cost | Policy Center | cost excluded/masked; access decision does not leak internals |

## §6.10 Microcopy-Aware Expected Text

Browser/vision assertions must anchor to exact current text:

- primary action `สร้างสูตรใหม่`
- steps `ข้อมูลสูตร`, `ส่วนประกอบ`
- footer `ย้อนกลับ`, `ยกเลิก`, `บันทึกร่าง`, `บันทึก + เปิดใช้งาน`
- detail actions `แก้ไขสูตร`, `เปลี่ยนสถานะ`, `ปิด`
- tabs `ภาพรวม`, `ส่วนประกอบ (${b.lines.length})`, `ประวัติ`
- sibling heading `เวอร์ชันอื่นของสินค้านี้ (${others.length})`
- status labels `ร่าง`, `ใช้งาน`, `ไม่ใช้งาน`
- validation strings in §6.2 TC-VR-01..08

Do not substitute a central fallback string where the source HTML contains a different visible string; for example the actual back label is `ย้อนกลับ`.

## §6.11 AI-Default Propagation Verification

| Test | Default IDs | Evidence expected |
|---|---|---|
| TC-AID-01 | AID-01/02 | edit referenced succeeds; delete referenced skips |
| TC-AID-02 | AID-03/04 | missing-cost flag and scrap boundary match ENG-01 |
| TC-AID-03 | AID-05 | deactivated master read/save split |
| TC-AID-04 | AID-06 | idempotency TTL and max sizes configurable/tested |
| TC-AID-05 | AID-07 | scale/mode identical in engine/API/UI expected value |
| TC-AID-06 | AID-08/09/10 | audit fail-closed, retention config, code sequence behavior documented |

## §6.12 Coverage Exit Check

- [ ] S-01..08 each maps to acceptance test
- [ ] BR-01..15 each has `TC-BR-*`
- [ ] VR-01..08 each has `TC-VR-*`
- [ ] EC-01..10 each has `TC-EC-*`
- [ ] every mutation API has happy, negative, idempotency, permission and audit coverage
- [ ] every downstream in BRD §12.1 has at least one XT case, including amend/inactivate after consumption
- [ ] Scope Lock and `[AI-DEFAULT]` propagation checks pass

