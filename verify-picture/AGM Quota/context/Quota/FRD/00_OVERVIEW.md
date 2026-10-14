# 00_OVERVIEW — F-AGM-002 Quota Management (จัดการโควตาชาวไร่)

> **Audience:** All roles · **Purpose:** Meta + Scope + Roles + Dependencies + Scope Lock + Coverage Manifest

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-AGM-002 |
| **Feature Name** | Quota Management (จัดการโควตาชาวไร่) |
| **Feature Code** | AGM-QUOTA |
| **Module** | AGM / Quota · **Client** | WKN |
| **Variant** | STANDARD (7 files) |
| **Status** | DRAFT (generated) |
| **FRD Version** | 1.0 (2026-07-20) · **Generator** | frd-generator-v6 |
| **Source BRD** | BRD_F-AGM-002_Quota.md (APPROVED, 2026-07-20) |
| **Constraint** | invariants.md LOCKED 🔒 (LOCK-01..11) |
| **Legacy source** | quota-management.zip (Next.js/v0) |
| **Related** | F-AGM-001 Farmer Member (cross-module) |

**Variant decision:** STANDARD — handover + module consistency กับ Farmer. Fallback check: pages=2+5 overlays, states=3 (unverified/verified/rejected)+deleted, approval=Yes, money=No → STANDARD (cross-module complexity handled ใน 02_API/03_LOGIC)

---

## §0.4 Roles & Responsibilities (COSO)
| Role | Person | Responsibilities |
|---|---|---|
| **Maker** | R-01 เจ้าหน้าที่ทะเบียนโควตา | สร้าง (From/No-Member) / แก้ / ลบ (unverified) / CSV |
| **Checker** | R-02 หัวหน้างานโควตา | Verify เดี่ยว/กลุ่ม |
| **Approver** | DOA placeholder (OQ-Q5) | Phase 4 |
| **Owner** | แผนกทะเบียนโควตา WKN | Monitor + reconcile |

> SoD: R-01 ≠ R-02 (EC-15, OQ-Q6)

---

## §0.5 Dependencies

### Upstream
| Dependency | Type | Source |
|---|---|---|
| M-01 Thai Address Hierarchy | Lookup API | CUBE core ✅ |
| **F-AGM-001 Farmer Member** | Cross-module API | query member (Approved) + write quota_status ✅ |
| Central Import Framework | Engine | CUBE core (เพิ่ม config entity=quota) |
| Document Storage | Service | CUBE core ✅ (เอกสารแนบ) |
| User Access ENC | Policy | Policy Center |

### Downstream (BRD §12.1)
| Consumer | What |
|---|---|
| **Farmer Member (upstream write)** | quota_status (has/no_quota) — เขียนกลับ |
| สัญญาส่งอ้อย (อนาคต) | quota_number + linked_member_id (verified) |
| การเงินชาวไร่ (อนาคต) | bank/BAAC |

---

## §0.7 Multi-Tenant & Security Context
- [x] Multi-tenant (RLS) · [x] PII (citizen_id, phone, email, address, bank/BAAC) · [ ] Financial calc · [x] Audit log · [x] Document storage
- **Security Preset:** P3 Master Data + Document Access (BRD §16.3)

### §0.7.1 Data Classification Summary
Highest: **Restricted** (citizen_id) · Confidential (phone/email/address/bank/BAAC/documents) · Internal (ชื่อ/สถานะ/quota_number)
**Linkage:** citizen_id → Restricted Resources (OQ-F02) · เอกสารแนบ → Document Access control

---

## §0.8 Open Questions
| ID | Question | Blocking? | Owner |
|---|---|---|---|
| OQ-Q1 | verify reject บังคับ note ไหม (align Farmer) | NO (คง optional) | Strike/WKN |
| OQ-Q2 | has_quota เขียนตอน create-link/verify | NO (lock: create-link) | Strike |
| OQ-Q3 | rejected → re-submit อัตโนมัติไหม | NO (คงตาม legacy) | Strike |
| OQ-Q4 | quota_number บังคับ format | NO (free-text+unique) | Strike/WKN |
| OQ-Q5 | DOA chain จริง | NO (placeholder) | WKN + Policy |
| OQ-Q6 | SoD self-verify | NO (หลัง flag) | Strike/WKN |
| OQ-F02 | wire citizen_id → Restricted Resources | NO | Policy |
| OQ-F03 | write-back failure policy (retry queue) — ต้องไม่ปล่อยเงียบ | NO | Dev/Policy |

---

## §0.9 Glossary
| Term | Definition |
|---|---|
| No-Member quota | โควตาที่ไม่ผูกสมาชิก (standalone) |
| has_quota / no_quota | quota_status ใน farmer_member — เขียนโดย Quota เท่านั้น |
| 1:0..1 | สมาชิก 1 คนมีโควตาได้ ≤ 1 |
| BAAC | ธ.ก.ส. |
| Write-back | Quota เขียน quota_status กลับ farmer_member |

---

## §0.10 Pack Navigation
00 OVERVIEW · 01 UI · 02 API (+cross-module contract) · 03 LOGIC (+farmer connector) · 04 DB · 05 RULES · 06 TESTS (+XT)

---

## §0.11 Scope Lock (STANDARD) ⭐
> Ref: `invariants.md` LOCKED 🔒 — immutable, spec ขัด → LOCK ชนะ

| LOCK-ID | ข้อความ | สถานะใน pack |
|---|---|---|
| LOCK-01 | capability legacy 100% | ✅ Coverage Manifest ครบ |
| LOCK-02 | state machine unverified→verified/rejected + soft delete | ✅ 05_RULES §5.2 |
| LOCK-03 | quota_number user-entered + unique | ✅ 05_RULES BR-AGQ-01 + 03 FN validate |
| LOCK-04 | 2 create modes (From/No-Member, 1:0..1, approved) | ✅ 02_API API-02/03 + 03 FN-01/02/11 |
| LOCK-05 | cross-module write-back has/no_quota | ✅ 02_API §2.X + 03 FN-12 + 06 XT |
| LOCK-06 | optimistic lock + idempotency | ✅ 02_API §2.3 |
| LOCK-07 | CSV No-Member + partial success + error report | ✅ 02_API API-09 + 05 BR-AGQ-10 |
| LOCK-08 | ลบเฉพาะ unverified + soft | ✅ 05_RULES BR-AGQ-06 |
| LOCK-09 | verify note optional | ✅ 05_RULES BR-AGQ-05 |
| LOCK-10 | governance additions | ✅ 04_DB + 05_RULES §5.7 |
| LOCK-11 | email optional | ✅ 04_DB §4.2 |

**Drift check:** governance additions (masking/approved-check/optimistic UX) อยู่ใต้ LOCK-10 — ไม่ drift

---

## §0.12 Coverage Manifest ⭐

### Stories (BRD §7)
| BRD Ref | Requirement | อยู่ที่ |
|---|---|---|
| §7 US-01 | สร้าง From-Member | 01 OV-01 · 02 API-02 · 03 FN-01/11/12 · 06 AC-01..03 |
| §7 US-02 | สร้าง No-Member | 01 OV-01 · 02 API-03 · 03 FN-02 · 06 AC-04 |
| §7 US-03 | quota_number unique | 01 OV-01 · 02 API-06 · 03 FN-04 · 06 AC-05 |
| §7 US-04 | CSV No-Member | 01 OV-05 · 02 API-09/10 · 03 FN-09 · 06 AC-14..17 |
| §7 US-05 | ค้นหา | 01 P-01 · 02 API-01 · 03 FN-05 · 06 AC-18/19 |
| §7 US-06 | Verify เดี่ยว | 01 OV-03 · 02 API-07 · 03 FN-06/12 · 06 AC-20..22 |
| §7 US-07 | Verify กลุ่ม | 01 OV-03 · 02 API-08 · 03 FN-07 · 06 AC-23 |
| §7 US-08 | แก้ไข (optimistic lock) | 01 OV-02 · 02 API-05 · 03 FN-03 · 06 AC-24/25 |
| §7 US-09 | ลบ | 01 OV-04 · 02 API-11 · 03 FN-08/12 · 06 AC-26/27 |
| §7 US-10 | detail + files + history | 01 P-02 · 02 API-04/12 · 06 AC-28/29 |

### Rules (BRD §9)
| BRD Ref | Rule | อยู่ที่ |
|---|---|---|
| §9 R01 | quota_number unique | 05 BR-AGQ-01 · 06 AC-05 |
| §9 R02 | 2 create modes | 05 BR-AGQ-02 · 06 AC-01/04 |
| §9 R03 | เริ่ม unverified | 05 §5.2 · 06 AC-03 |
| §9 R04 | verify เฉพาะ unverified | 05 BR-AGQ-04 · 06 AC-22 |
| §9 R05 | note optional | 05 BR-AGQ-05 · 06 AC-21 |
| §9 R06 | ลบเฉพาะ unverified + soft | 05 BR-AGQ-06 · 06 AC-26/27 |
| §9 R07 | cross-module write-back | 05 BR-AGQ-07 · 03 FN-12 · 06 XT-01..03 |
| §9 R08 | approved + 1:0..1 | 05 BR-AGQ-08 · 06 AC-01/02 |
| §9 R09 | optimistic lock | 05 BR-AGQ-09 · 06 AC-25 |
| §9 R10 | CSV No-Member partial | 05 BR-AGQ-10 · 06 AC-14 |
| §9 R11 | postal auto ×2 | 05 BR-AGQ-11 · 06 AC-08 |
| §9 R12 | file limits | 05 BR-AGQ-12 · 06 AC-13 |
| §9 R13 | DOA placeholder | 05 BR-AGQ-13 · OQ-Q5 |
| §9 VR-01..11 | validation | 05 §5.4 |

### Edge Cases (BRD §10)
| BRD Ref | Edge | อยู่ที่ |
|---|---|---|
| §10 EC-01..08 ☑ | confirmed | 05 §5.5.1 · 06 AC/XT |
| §10 EC-09..17 ☐ | recommended | 05 §5.5.2 · 06 §6.11 |

**สรุป:** Stories 10/10 ✅ · Rules 13/13 + VR 11/11 ✅ · Edges ☑ 8/8 + ☐ 9/9 (marked) · ไม่มีหล่น
