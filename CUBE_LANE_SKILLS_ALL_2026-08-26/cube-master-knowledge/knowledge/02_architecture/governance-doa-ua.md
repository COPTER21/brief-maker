---
file_id: KB-02-02
title: Governance Pattern — DOA + User Access (Feature-DOA Pairing)
version: 1.0.0
last_updated: 2026-05-27
status: stable
related: cube-4.0-master-bible.md §5
---

# CUBE 4.0 Governance — DOA + User Access

## Quick Reference (TL;DR)

**Iron rule**: ทุก feature ต้องผ่าน 2 governance checkpoints ก่อน deploy:
1. **User Access** (Policy Center → User Roles Access)
2. **DOA** (Policy Center → Data Governance → DOA) — ถ้ามี approve/sign/consent

**Pattern name**: "Feature-DOA Pairing" — สร้าง feature เป็นชุด พร้อม governance ครบทุกชุด

---

## 1. Why centralized

| Bad pattern (banned) | Good pattern |
|---|---|
| Hardcode `if user.role == "manager" && amount < 100000` | Call `DOA.checkApproval(feature_id, amount, user)` |
| Approval rule กระจายทุก module | All rules centralized in DOA module |
| Skip User Access registration | Every feature has entry in User Roles Access |
| Deploy feature without DOA entry (when approval needed) | Pair: Feature → DOA ENC → User Access ENC → Deploy |

---

## 2. Development Lifecycle (4 steps)

```
Step 1: Create Feature X
  ├─ Build UI + Logic + DB
  ├─ Add placeholder fields:
  │   ├─ approver_role
  │   ├─ approved_by
  │   └─ approval_chain
  └─ Add TODO comment for DOA wire

Step 2: ENC DOA for Feature X
  ├─ Add Feature X to DOA registry
  ├─ Set approval pattern: flat | sequential | threshold
  ├─ Define scope: document_sign | policy_approve | budget_approve
  └─ Wire to placeholder fields

Step 3: ENC User Access for Feature X
  ├─ Add Feature X to User Roles Access matrix
  └─ Define: who / role → permissions

Step 4: Feature X Production Ready
  ✓ Access control complete
  ✓ Approval rule complete
  ✓ Audit trail complete
```

---

## 3. DOA Registry Schema

```yaml
DOA Master Table:
  feature_id              # link to Feature in System Development module
  feature_name
  approval_required       # bool
  approval_scope          # document_sign | policy_approve | budget_approve
  approval_pattern        # flat | sequential | threshold
  approval_chain[]        # list of role / position
  threshold_rules[]:      # if pattern = threshold
    - amount_from
    - amount_to
    - required_approvers[]
  consent_required        # bool (PDPA / user consent)
  active                  # bool
  effective_date
```

---

## 4. User Roles Access Schema

```yaml
UserAccess Matrix:
  feature_id              # link to Feature
  role_id                 # link to Role
  permissions[]:
    - view
    - create
    - edit
    - delete
    - approve
    - export
    - print
  scope_filter            # optional: department / branch / project scope
```

---

## 5. Document Pipeline Compliance

ทุก **Feature Brief / BRD / FRD** ต้องมี section "Governance":

```yaml
Governance:
  User Access Requirements:
    - who / role
    - permissions[]
    - scope filter (if applicable)
  
  DOA Requirements (if feature has approval):
    - what to approve (document / policy / budget)
    - pattern (flat / sequential / threshold)
    - chain or threshold rules
    - consent required (PDPA)
```

### Skill Compliance
- `frd-generator-v6` — must include §Governance in every FRD
- `html-generator-v9` — must create UI placeholder fields
- `brd-generator-full` — must enforce User Access + DOA requirements

---

## 6. Audit Trail Standard

ทุก governance action ต้อง log:

```yaml
Audit Log:
  timestamp
  user_id
  feature_id
  action               # view | create | approve | reject | sign | consent
  before_state
  after_state
  approval_chain_state  # for approval action
  ip_address
  user_agent
```

**Storage**: Policy Center → Monitoring & Compliance → Audit

---

## 7. Anti-Patterns (FORBIDDEN — flag if seen)

| Anti-pattern | What to do instead |
|---|---|
| `if user.role == X && amount < N: auto_approve()` | `L-001.resolve_chain(feature_id, amount, user)` |
| Approval rule defined in feature's business logic | Define in DOA registry; feature calls engine |
| Feature deployed without User Access entry | Block deploy via QC layer |
| Feature deployed without DOA entry (when approval exists) | Block deploy via QC layer |
| Approval rule per module (decentralized) | All rules in Policy Center → Data Governance → DOA |

---

## 8. Reference

- Full architecture context: `02_architecture/cube-4.0-master-bible.md` §5
- Skill that enforces this: `frd-generator-v6` (Iron Rule R10)

---

## Change Log

- **1.0.0** (2026-05-27): Extracted from CUBE 4.0 Master Bible §5 as standalone reference
