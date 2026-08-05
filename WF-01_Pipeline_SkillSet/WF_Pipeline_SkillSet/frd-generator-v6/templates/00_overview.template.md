# 00_OVERVIEW — F-XX [Feature Name]

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-XX |
| **Feature Name** | [Full name] |
| **Feature Code** | [CB-XXX / CRM-XXX / ...] |
| **Module** | [Module name] |
| **Variant** | LEAN / STANDARD / FULL |
| **Status** | DRAFT / IN-REVIEW / APPROVED |
| **FRD Version** | 1.0 (YYYY-MM-DD) |
| **Generator** | frd-generator-v6 |
| **Source Brief** | F-XX_CODE.md (vN, date) |
| **Source BRD** | BRD_F-XX.md (status: APPROVED, date) |
| **Author** | [BA name / team] |
| **Reviewers** | [Tech Lead, PM, QA Lead] |

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | YYYY-MM-DD | [name] | Initial FRD generation |

---

## §0.3 Scope

### In Scope
- [Major feature 1]
- [Major feature 2]
- [Major feature 3]

### Out of Scope
- [Explicitly excluded item 1] — reason: [why]
- [Explicitly excluded item 2] — reason: [why]

### Out of Scope (mark from Phase 2.5 skipped probes)
- [Probe PR-X skipped by user] — flagged as Open Question

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | [role] | Create draft / submit |
| **Checker** | [role] | Review / validate |
| **Approver** | [role] | Final approval |
| **Owner** | [role] | Maintain / monitor |

> รายละเอียดต่อ workflow → ดู `01_UI.md §1.X Journey`

---

## §0.5 Dependencies

### Upstream (this feature depends on)
| Dependency | Type | Source |
|---|---|---|
| [Feature/Module/Service] | Data / API / Engine | F-YY / Module Z / CUBIC ENG-NNN |

### Downstream (features that depend on this)
| Consumer | What it uses |
|---|---|
| F-YY | uses ENG-005 from this FRD §3.2 |

### External
| Service | Purpose |
|---|---|
| Omise | Payment processing |
| [Service] | [Purpose] |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | React / Next.js / Tailwind |
| API | Node.js / Strapi |
| Database | PostgreSQL (with RLS for multi-tenant) |
| Engine layer | CUBIC Registry |
| Auth | JWT + role-based |
| Hosting | AWS / GCP |

---

## §0.7 Multi-Tenant & Security Context

- [ ] Multi-tenant feature: YES / NO
- [ ] PII data involved: YES / NO (ดูรายละเอียดต่อ field ใน 04_DB §4.2 + §4.6)
- [ ] Financial data: YES / NO
- [ ] Audit log required: YES / NO

**Security Bible domains applied:** [D1, D2, D5, ...] — see 05_RULES.md §Security

### §0.7.1 Data Classification Summary ⭐ (v5.1)

Highest classification level ที่ feature นี้แตะ:
- [ ] Has Restricted fields (ระบุใน 04_DB §4.2)
- [ ] Has Confidential fields
- [ ] Internal only (default)
- [ ] Public-facing data

**Linkage:** ฟิลด์ Restricted/Confidential ต้อง register ที่ Policy Center → Data Classification + Restricted Resources (ดู 04_DB §4.6.6)

---

## §0.8 Open Questions

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| OQ-01 | [Unresolved question] | YES/NO | [Who decides] |
| OQ-02 | [From Phase 2.5 probe skipped] | NO | [Role] |

> Resolved questions → move to 07_LOCKED_DECISIONS as LD-NN

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| [Domain term] | [Meaning in this feature context] |
| [Acronym] | [Full form + meaning] |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | This file — meta + scope |
| 01_UI.md | FE dev | Pages + Components + Journey |
| 02_API.md | BE dev (HTTP) | API contracts |
| 03_LOGIC.md | BE dev (logic) | Functions + Engines + Trace |
| 04_DB.md | DBA / BE | Tables + Fields + Relationships |
| 05_RULES.md | BE + QA | Business Rules + Edge Cases + Errors |
| 06_TESTS.md | QA | Acceptance + DoD |
| 07_LOCKED_DECISIONS.md | All | LDs + Convention deviations |
| INDEX.md (FULL only) | All | Cross-reference quick nav |

---

## §0.11 Scope Lock (LEAN/STANDARD variant) ⭐ v6

> FULL variant → อยู่ที่ 07_LOCKED §7.0 แทน · โครงเดียวกัน: LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะ
> Scope Lock Ref: [เลขใบเซ็น] / "N/A — standalone"

## §0.12 Coverage Manifest ⭐ v6 (กัน requirement หล่น BRD→FRD)

> ทุก Story (BRD §7) / Rule (§9) / Edge confirmed (§10) ต้องมีแถว — ไม่มีที่ลง = Open Question

| BRD Ref | Requirement (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| §7 S-01 | สร้าง [entity] | 01_UI P-02 · 02_API-02 · 03_FN-01 · 06 AT-01 |
| §9 R-04 | [rule] | 05_RULES BR-04 · 06 AT-07 |
| §10 E-03 | [edge] | 05_RULES EC-03 |

**สรุป:** Stories N/N ✅ · Rules N/N ✅ · Edges N/N ✅ · ไม่มีที่ลง → OQ: [รายการ/ไม่มี]
