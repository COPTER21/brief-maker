# DOA BRIEF — F-SALES-PROMO Promotion

> ใบประกาศสำหรับนำไปตั้งค่าที่ DOA กลาง F-DLG-001 · feature นี้ประกาศ contract เท่านั้น ไม่ตั้งค่าระบบจริง

## 1. Identity

| Field | Value |
|---|---|
| feature_id | `F-SALES-PROMO` |
| feature_name | Promotion — โปรโมชัน |
| module | Sales |
| platform | CUBE ERP |
| doa_entry_ref | `DOA-SALES-PROMO` |
| approval_scope | `policy_approve` |
| chain_mode | sequential |
| department_mode | merged |
| amount_dimension | **ไม่มีวงเงิน** |
| wire_status | pending |

## 2. Approval Actions

| Action | Trigger | Preconditions | Approve result | Reject result |
|---|---|---|---|---|
| `promotion_submit` | ผู้มีสิทธิ์กด “ส่งอนุมัติ” | status=draft, form valid, assigneesครบ, overlap ackถ้ามี | create frozen chain; status=pending_approval | — |
| `promotion_decide` | current assignee กดอนุมัติ/ไม่อนุมัติ | sequential current step; submitter≠approver | advance next step; final → scheduled/active | reason required; return draft; preserve round history |

No separate DOA is required for pause, resume, cancel or end-early in the approved scope.

## 3. Matrix to Configure

### 3.1 Set

| Field | Value |
|---|---|
| amount_from | `0` THB |
| amount_to | `null` — ไม่จำกัด |
| departments | `[]` / merged all departments |
| chainMode | `sequential` |
| scope | `policy_approve` |

### 3.2 Steps

| step_no | role id in DOA master | candidate rule | required |
|---:|---|---|:---:|
| 1 | `role-mgr-sales` | active employees holding configured role; exclude submitter | yes |
| 2 | `role-mgr-bu` | active employees holding configured role; exclude submitter | yes |

These roles are **configuration data in the DOA entry**, not constants in Promotion code. DOA Admin may change positions/order through the central config; new submissions use the latest entry while in-flight submissions keep their snapshot.

### 3.3 Interval Check

- One set only: `[0, null]` ✅
- No overlap/gap ✅
- Last `amount_to=null` ✅
- Amount does not alter the chain ✅

## 4. Field Contract for FRD

| Field | Type | Nullable | Source / behavior |
|---|---|:---:|---|
| approval_required | boolean | no | true for submitted promotion |
| approval_status | enum | no | draft/pending_approval/approved/rejected/cancelled |
| doa_entry_ref | string | yes before submit | `DOA-SALES-PROMO` from resolved config |
| doa_policy_version | string | yes before submit | frozen at submit |
| approver_role | string | yes | current step role from snapshot |
| submitted_by / submitted_at | user/timestamp | yes | maker/time |
| approved_by / approved_at | user/timestamp | yes | final decision |
| approval_chain | jsonb | yes before submit | frozen step→role→employee snapshot |
| approval_history | related append-only records | no | every round/decision |

Mandatory rules:

- resolve only at submit; freeze chain/version
- no hardcoded role list, person, amount threshold or fallback chain in feature
- reject returns draft; history remains append-only
- submitter cannot be selected or decide own promotion

## 5. UI Contract for HTML / Production UI

| UI | Contract |
|---|---|
| “ส่งอนุมัติ” | only draft + valid; opens slot picker from resolved entry |
| slot candidate | avatar + position + name; no submitter |
| status badge | draft / pending / approved / rejected/cancelled vocabulary |
| approval timeline | sequential step, role, selected person, time, pending/approved/rejected |
| “อนุมัติ / ไม่อนุมัติ” | current assignee only; reject reason required |
| My Approval hook | current pending step appears for selected employee |

## 6. Wire Checklist

- [ ] DOA Admin creates `DOA-SALES-PROMO` with set `[0,null]`
- [ ] DOA Admin confirms role ids exist in the current master
- [ ] Promotion submit adapter resolves entry + policy version + candidates
- [ ] API removes submitter and validates selected employee server-side
- [ ] Promotion saves immutable approval steps before pending state commit
- [ ] DOA/My Approval receives current pending task
- [ ] Approve/reject callbacks validate current assignee and idempotency
- [ ] Rejection round and all decisions remain append-only
- [ ] Automated test changes DOA config after submit and proves frozen chain unchanged
- [ ] `wire_status` changes pending → wired only after integration test passes

## 7. Open Questions / Manual Ownership

| Item | Status | Owner |
|---|:---:|---|
| No amount; sequential; merged; policy scope | confirmed | PM/BA |
| Initial positions `role-mgr-sales` then `role-mgr-bu` | confirmed source/default; configure centrally | DOA Admin |
| Actual employees available per role | runtime config data | HR/DOA Admin |
| Temporary delegation behavior | inherited from DOA central | DOA owner |

## Quality Gate

| Gate | Result |
|---|:---:|
| all roles use `role-*` ids | PASS |
| amount_from/to complete | PASS |
| no range gap/overlap | PASS |
| final amount_to null | PASS |
| approval_scope valid | PASS |
| no unmarked invented default | PASS |
| no approval chain hardcoded into feature | PASS |

Verdict: **PASS — ready for central DOA configuration; wire_status remains pending until implemented.**
