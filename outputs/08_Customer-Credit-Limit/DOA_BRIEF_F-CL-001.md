# DOA Declaration — F-CL-001 Customer Credit Limit

> ประกาศเพื่อให้ผู้ดูแลตั้งค่าใน Policy Center DOA เท่านั้น — ไม่ได้ตั้งค่า DOA จริง และ feature ห้าม hardcode สายอนุมัติ

## 1. Identity

| Field | Value |
|---|---|
| feature_id | F-CL-001 |
| feature_name | Customer Credit Limit |
| module | Sales / O2C |
| platform | Policy Center DOA |
| approval_scope | `policy_approve` |
| chainMode | `merged` |
| wire_status | `pending` |

## 2. Approval action

| Action | Trigger | Approve outcome | Reject outcome |
|---|---|---|---|
| `credit_limit_change` | Credit Officer sends a draft with new absolute credit limit and reason | current step advances; final step applies new limit and publishes projection | request becomes rejected; current limit remains unchanged; reason/audit retained |

There is one approval action and it is amount-sensitive. The feature sends the requested **absolute** credit limit to DOA; this is `[DEFAULT — รอยืนยัน]` under OQ-CL-01.

## 3. Matrix to configure in DOA

> Values below come from the confirmed feature brief but remain `[DEFAULT — รอยืนยัน]` until DOA owner verifies the real policy. All boundaries are Thai baht and continuous.

| amount_from | amount_to | departments | chainMode | steps (role ids only) |
|---:|---:|---|---|---|
| 0 | 200,000 | `merged` | sequential | `[role-mgr-sales]` `[DEFAULT — รอยืนยัน]` |
| 200,001 | 1,000,000 | `merged` | sequential | `[role-mgr-sales] → [role-dir-sales]` `[DEFAULT — รอยืนยัน]` |
| 1,000,001 | null (unlimited) | `merged` | sequential | `[role-mgr-sales] → [role-dir-sales] → [role-cfo]` `[DEFAULT — รอยืนยัน]` |

No display name is authority in this declaration. `role-mgr-sales`, `role-dir-sales`, and `role-cfo` must be validated against the User Roles master before wiring.

## 4. Feature field contract

| Field | Type | Nullable | Contract |
|---|---|---:|---|
| approval_required | boolean | no | result of DOA entry/policy |
| approval_status | enum | no | draft, pending_approval, approved, rejected |
| doa_entry_ref | string | yes until wire | F-CL-001 entry reference |
| approver_role | string | yes | current role-id from resolved snapshot |
| approved_by | string | yes | real My Profile user id at signing |
| approval_chain | jsonb | yes before submit | immutable resolved snapshot |
| approved_at | timestamp | yes | final approval time |

## 5. UI contract

- `ส่งอนุมัติ` appears only for `draft`; it is visibly disabled until amount differs, reason is supplied, and DOA resolves.
- Status labels are `รอส่งอนุมัติ`, `รออนุมัติ`, `อนุมัติแล้ว`, and `ไม่อนุมัติ`.
- The DOA timeline shows each step status dot/check plus a My Profile avatar/name/position; display data is not DOA authority.
- Approve/reject are only enabled for the server-authorized current signer; reject requires reason.
- The prototype uses a mock resolved payload only to demonstrate the tiers; production must call DOA and My Profile.

## 6. Wire checklist

- [ ] Create/confirm DOA entry F-CL-001 in Policy Center using an approved matrix.
- [ ] Confirm role ids exist and the scope is `policy_approve`.
- [ ] Wire submit to resolve DOA and persist immutable `approval_chain` snapshot.
- [ ] Wire signature identity/SoD check to My Profile.
- [ ] Fail closed on no tier / resolver failure; do not create pending approval.
- [ ] Wire final approved limit/hold projection to Customer Master and Sales Order contract.
- [ ] Change `wire_status` from pending to wired only after integration test.

## 7. Open Questions

| ID | Decision needed | Owner |
|---|---|---|
| OQ-CL-01 | Resolve amount is absolute requested limit or change delta | BA / policy owner |
| OQ-CL-02 | Direct-set / empty-approver band exists | BA / compliance |
| OQ-CL-03 | Confirm role ids and names in User Roles master | DOA admin |
| OQ-CL-04 | Confirm 200k/1M boundaries are policy, not prototype mock | DOA owner |
| OQ-CL-05 | Hold/unhold requires DOA or direct credit-officer authority | Compliance |

## Quality gate

G1 role ids use `role-*`: PASS. G2 ranges complete: PASS. G3 ranges continuous/non-overlapping: PASS. G4 final range unlimited: PASS. G5 scope valid: PASS. G6 unconfirmed policy values marked default: PASS. G7 no feature-owned approval chain authority: PASS.

> Note: the skill's bundled `references/doa-contract.md` and template were absent from the workspace at execution time. This declaration is constrained to the approved PREBRIEF and must be checked against the central DOA master before it is wired.
