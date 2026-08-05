# Revision Mode Guide — Drift Detection & Classification

คู่มือละเอียดสำหรับ Revision Mode ของ brd-generator-full
ใช้เมื่อ user vibe HTML แล้วต้อง sync กลับ BRD

---

## 🎯 Mission

แปลง "การแก้ HTML ของ user" เป็น "การ update BRD" อย่างปลอดภัย โดย:
1. ตรวจให้เจอ drift ทุกที่
2. Classify drift ตามความสำคัญ
3. ขออนุมัติ user สำหรับ Critical drift
4. Apply update แบบ surgical (เฉพาะที่กระทบ)
5. Audit trail ครบ

---

## 📊 Drift Classification

### 🟢 UX Drift — apply ทันที (low risk)

**ตัวอย่าง:**
- เปลี่ยนสี (Navy → Teal)
- ปรับ spacing/padding
- ย้ายตำแหน่งปุ่ม (header → footer)
- เปลี่ยน icon
- ปรับ copy text (label/placeholder/help text)
- เปลี่ยน layout pattern (table → card)

**Section ที่กระทบ:**
- BRD §6 (UI label only — ไม่กระทบ data type/validation)
- ส่วนใหญ่ไม่ต้อง update BRD เลย — sync ไป FRD §7 ดีกว่า

**Action:** apply เงียบ ๆ + log ใน Drift Report

---

### 🟡 Hidden Logic Drift — apply ถ้า make sense (medium risk)

**ตัวอย่าง:**
- เพิ่ม validation rule ที่ไม่เคยมี (e.g., "max discount 30%")
- เพิ่ม auto-calculation (e.g., "tax = subtotal × 0.07")
- เพิ่ม conditional show/hide field
- เพิ่ม default value ที่ smart (e.g., due_date = today + 30)

**Section ที่กระทบ:**
- BRD §9 (Business Rules + Validation)
- อาจกระทบ §10 Edge Cases ด้วย (กรณีที่ rule new ไม่ผ่าน)

**Action:** apply แต่ flag ใน Drift Report ให้ user รู้

---

### 🔴 Business Drift — apply พร้อม flag (high risk แต่ไม่ critical)

**ตัวอย่าง:**
- เพิ่ม field ใหม่ (e.g., "customer_tier")
- เพิ่ม status ใหม่ใน state machine (e.g., "On Hold")
- เพิ่ม action ใหม่ (e.g., "Bulk Approve")
- เปลี่ยน workflow step (e.g., เพิ่ม checker layer)
- เปลี่ยน role permission

**Section ที่กระทบ:**
- BRD §4, §5, §6, §7, §8, §9 (กระทบหลายที่)
- อาจกระทบ Philosophy embed (§16-18)

**Action:** apply + แสดง impact summary + แนะนำ stakeholder review

---

### 🚨 Critical Drift — ต้องถาม user ก่อน apply (highest risk)

**ตัวอย่าง:**

| Critical Pattern | ตัวอย่าง | เหตุผลที่ critical |
|---|---|---|
| **Tag Migration** | R04 FIXED → DYNAMIC | กระทบ implementation strategy + Delivery Phases |
| **Locked Section Change** | แก้ §13 ที่ Changelog ระบุว่า "Phase 1 locked by Stakeholder" | Stakeholder lock ไว้ — re-approve ต้อง |
| **Security Preset Change** | P1 → P4 | กระทบ compliance — ต้อง review controls + risk |
| **New Role Outside RIF** | เพิ่ม "Approval Committee" ที่ RIF ไม่ระบุ | DoA matrix + COSO ต้อง redesign |
| **COSO Role Removal** | ลบ "Checker layer" ออก | SoD อาจ violate |
| **Status Removal** | ลบ "Rejected" status | กระทบ existing transactions |
| **Field Type Change** | unit_price NUMBER → TEXT | ทำลาย calculation logic |

**Section ที่กระทบ:**
- หลาย sections พร้อมกัน + Philosophy embed
- มักกระทบ Section 13 (Delivery Phases) เสมอ

**Action:**
1. STOP — ห้าม apply
2. แจ้ง user ผ่าน Step R2 Critical Decision Gate
3. รอ user confirm: "ตั้งใจ" / "ไม่ตั้งใจ — revert"
4. Document decision ใน Changelog v[N]
5. ถ้า "ตั้งใจ" → ถามต่อ "Stakeholder รู้ไหม?"

---

## 🔍 Drift Detection Heuristics

### จาก HTML → BRD Section Mapping

```
HTML structure                    BRD section ที่เกี่ยวข้อง
────────────────────────────────  ────────────────────────────────
<form> + <input> fields           §6 Data Entity + §9 Validation
<select> options                  §9 Rules (enum) + lookup
<button> actions                  §5 User Journey + §7 Stories + §4 Permission
<status badge>                    §8 Status & Lifecycle
Mock data (status enum)           §8 State Transition
Disabled state logic              §9 Business Rules
Validation message                §9 Validation Rules
Permission gate (if/show)         §4 Permission Matrix
SLA badge / time display          §17 SLA + Health Check
KPI widget                        §17 KPI + §18 Dashboard
```

### Detection Algorithm

```python
def detect_drift(html_v2, brd_v1):
    drifts = []

    # 1. Field-level drift
    html_fields = extract_form_fields(html_v2)
    brd_fields = parse_section_6(brd_v1)
    for field in symmetric_diff(html_fields, brd_fields):
        classify_field_drift(field, drifts)

    # 2. Action-level drift
    html_actions = extract_buttons_actions(html_v2)
    brd_actions = parse_section_5_steps(brd_v1)
    for action in symmetric_diff(html_actions, brd_actions):
        classify_action_drift(action, drifts)

    # 3. Status-level drift
    html_statuses = extract_status_enum(html_v2)
    brd_statuses = parse_section_8(brd_v1)
    for status in symmetric_diff(html_statuses, brd_statuses):
        classify_status_drift(status, drifts)

    # 4. Validation-level drift
    html_validations = extract_validation_messages(html_v2)
    brd_validations = parse_section_9_validation(brd_v1)
    for v in diff(html_validations, brd_validations):
        classify_validation_drift(v, drifts)

    # 5. Role/Permission drift
    html_roles = extract_role_gates(html_v2)
    brd_roles = parse_section_4(brd_v1)
    for r in symmetric_diff(html_roles, brd_roles):
        classify_role_drift(r, drifts)

    # 6. Critical pattern detection
    for drift in drifts:
        if is_critical_pattern(drift, brd_v1):
            drift.severity = "CRITICAL"

    return drifts
```

### Critical Pattern Recognition

```python
def is_critical_pattern(drift, brd_v1):
    # Tag migration
    if drift.section == 9 and drift.field == "tag":
        if drift.old_value == "FIXED" and drift.new_value in ["DYNAMIC", "WARNING"]:
            return True

    # Locked section
    changelog = parse_changelog(brd_v1)
    if drift.section_id in changelog.locked_sections:
        return True

    # Security preset change
    if drift.section == 16 and drift.field == "preset":
        return True

    # New role outside RIF
    if drift.section == 4 and drift.is_addition:
        rif = read_rif_if_available()
        if rif and drift.new_value not in rif.actors:
            return True

    # COSO role removal
    if drift.section == 5 and drift.field in ["Maker", "Checker", "Approver"]:
        if drift.is_removal:
            return True

    # Status removal (existing data risk)
    if drift.section == 8 and drift.is_removal:
        return True

    # Field type change
    if drift.section == 6 and drift.field == "input_type":
        return True

    return False
```

---

## 📝 Drift Report Format

```markdown
# _DRIFT_REPORT_v1.1.md

## Metadata
- BRD Base: BRD_quotation_v1.0.md (APPROVED 2026-05-10)
- HTML Source: HTML_quotation_v2.html (vibed by user 2026-05-12)
- HTML Baseline: HTML_quotation_v1.0.html (auto-generated)
- Diff timestamp: 2026-05-12 14:30:00

## Summary
| Severity | Count |
|---|:---:|
| 🚨 Critical | 1 |
| 🔴 Business | 3 |
| 🟡 Hidden Logic | 2 |
| 🟢 UX | 5 |

## 🚨 Critical Drifts (require user decision)

### C-01: Tag Migration — R04
- **Old:** R04 (สูตรส่วนลด) = FIXED, value = "5% flat"
- **New:** R04 = DYNAMIC, value = "tier-based (5%/10%/15%)"
- **Why critical:** Tag เปลี่ยน → ต้องสร้าง Rule Management infrastructure (Phase 3)
- **Impact:** §9, §9.5, §13 (Phase 1 → Phase 3), §14 Dev Summary
- **User decision:** ☐ Confirm ☐ Revert ☐ Discuss with stakeholder first

## 🔴 Business Drifts (auto-apply, FYI)

### B-01: New Field — customer_tier
- **Where:** Quote form, line 234
- **Type:** DROPDOWN-SINGLE (VIP / Standard / Trial)
- **Impact:** §6 (new row), §9 (validation), §10 (edge: tier=null)
- **Action:** ✅ Will apply

### B-02: New Status — "On Hold"
- **Where:** Status badge, mock data line 78
- **Transitions:** Submitted → On Hold (manual), On Hold → Submitted (release)
- **Impact:** §8 (new node), §5 (hold step), §9 (when allowed)
- **Action:** ✅ Will apply

### B-03: New Action — "Bulk Approve"
- **Where:** QT List page, header button
- **Permission:** Sales Manager only
- **Impact:** §5 (new journey), §7 (new story), §4 (permission)
- **Action:** ✅ Will apply

## 🟡 Hidden Logic Drifts (auto-apply with notice)

### HL-01: Validation — discount cap
- **Found:** validation message "ส่วนลดเกิน 30% ไม่อนุญาต"
- **Section affected:** §9.2 Validation Rules
- **Action:** ✅ Will add VR-NEW

### HL-02: Auto-calc — tax
- **Found:** computed field "tax = subtotal * 0.07"
- **Section affected:** §9 Rules
- **Action:** ✅ Will add R-NEW

## 🟢 UX Drifts (informational)

- UX-01: ปุ่ม "ส่งอนุมัติ" ย้าย header → footer
- UX-02: Color theme tweak (primary blue intensity)
- UX-03: Table layout: 3 col → 4 col (split qty + unit)
- UX-04: Icon เปลี่ยน (lucide → heroicons)
- UX-05: Copy text "บันทึก" → "บันทึกแบบร่าง"

**Action:** Note ไว้ — sync ไป FRD §7 ทีหลัง

## Sections Affected
| Section | Status | Drift Refs |
|---|---|---|
| §1 Document Info | UPDATE (Changelog only) | — |
| §2-§4 | PRESERVE | — |
| §5 User Journey | UPDATE | B-02, B-03 |
| §6 Data Entity | UPDATE | B-01 |
| §7 User Stories | UPDATE | B-03 |
| §8 Status & Lifecycle | UPDATE | B-02 |
| §9 Business Rules | UPDATE | C-01, B-01, B-02, HL-01, HL-02 |
| §9.5 Flexibility | UPDATE | C-01 |
| §10 Edge Cases | UPDATE | B-01 |
| §11-§12 | PRESERVE | — |
| §13 Delivery Phases | UPDATE | C-01 |
| §14 Dev Summary | UPDATE | C-01, B-01, B-02, B-03 |
| §15 Open Questions | UPDATE (if any new) | — |
| §16-§18 Philosophy | RE-CHECK | (review for impact) |

## Audit Note
⚠️ BRD v1 ได้รับการ approve โดย Stakeholder วันที่ 2026-05-10
   Critical drift C-01 อาจกระทบ Phase commitment — แนะนำส่งรายงานนี้ให้ Stakeholder review
```

---

## 🚦 Decision Flow

```
START
  ↓
[R1] Drift Detection
  ↓
  [drift count > 0?]
  ├─ No → return "No drift detected" + exit
  └─ Yes
       ↓
  [R2] Has Critical drift?
  ├─ No → skip to R3
  └─ Yes → Ask user (single round)
       ↓
       User answer:
       A. All critical = intentional → log + proceed
       B. Some critical = mistake → revert specified + proceed with rest
       C. All critical = unintentional → revert all critical + proceed
       ↓
[R3] Impact Analysis
  ↓ (parallel)
  ├─ Map drifts → BRD sections
  ├─ Re-evaluate Tags (if §9 changes)
  ├─ Re-check Philosophy embed
  └─ Compute regression scope
  ↓
[R4] Generate BRD v2
  ↓
  For each section:
    if affected → update (preserve unaffected rows)
    else → copy verbatim
  ↓
  Section 1 Changelog → add v[N] entry
  ↓
  Quality Gate (CR01-CR05 + existing checks)
  ↓
  [Quality Gate pass?]
  ├─ Yes → Save .md + .docx + Drift Report
  └─ No → return NEEDS REVISION

[R5] Recommend Downstream
  ↓
  Identify sections changed
  ↓
  Recommend regeneration order:
    - If §6/§9 changed → FRD must regen
    - If §5/§8 changed → HTML may need cleanup
    - If §9/§10 changed → QA must regen
    - Always → Dev Brief regen
END
```

---

## ⚠️ Common Pitfalls

### Pitfall 1: Auto-apply Critical Drift
- **ผิด:** "user vibe เปลี่ยน Tag → assume intentional → apply"
- **ถูก:** ทุก Critical ผ่าน Step R2 เสมอ

### Pitfall 2: Rewrite ทั้ง Section ที่ไม่จำเป็น
- **ผิด:** "Section 5 มี drift 1 step → rewrite ทั้ง §5"
- **ถูก:** update เฉพาะ row/step ที่ drift, preserve ที่เหลือ

### Pitfall 3: ไม่ Update Changelog
- **ผิด:** Save BRD v2 ไม่ระบุว่ามาจาก revision
- **ถูก:** Section 1 Changelog ต้องมี v[N] entry ที่ link ไป _DRIFT_REPORT

### Pitfall 4: ลืม Re-check Philosophy
- **ผิด:** Business drift apply แต่ไม่ตรวจว่า COSO/Security/SLA ยัง valid
- **ถูก:** Step R3.3 บังคับ — Philosophy embed re-check ทุกรอบ

### Pitfall 5: ไม่แจ้ง Stakeholder Audit Need
- **ผิด:** Critical drift apply → ปิด skill เงียบ ๆ
- **ถูก:** Step R5.3 — แจ้ง audit warning + แนะนำ stakeholder review

---

## 🔗 Related References

- `references/change-likelihood-tags.md` — Tag classification (FIXED/CONFIG/DYNAMIC/WARNING)
- `references/edge-case-patterns.md` — 9 หมวด edge patterns
- `references/philosophy-embed-guide.md` — COSO/Security/Health/Monitoring rules
- `references/ai-review-checklist.md` — Quality Gate (รวม CR01-CR05)
