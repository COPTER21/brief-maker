# frd-generator-v6

> **Skill สำหรับสร้าง FRD (Functional Requirements Document) มาตรฐาน 2BSimple v6.0**
> Pack Mode adaptive output แยกไฟล์ตาม layer (CUBIC 3-layer architecture)

---

## 🚀 Quick Install

1. Unzip ไฟล์นี้ → ได้ folder `frd-generator-v6/`
2. Upload เข้า Claude → Settings → Skills → Upload Skill (.zip)
3. ใช้งานผ่าน trigger: "สร้าง FRD จาก Brief + BRD นี้"

---

## 📂 Folder Structure

```
frd-generator-v6/
├── SKILL.md                              ← Core skill (entry point)
├── README.md                             ← This file
│
├── references/                           ← Decision-making references
│   ├── logic-placement-matrix.md         ⭐ NEW v5 — Function vs Engine decision
│   ├── pack-variants.md                  — LEAN/STANDARD/FULL decision tree
│   ├── cubic-schema-templates.md         — API + Engine schemas (CUBIC format)
│   └── edge-case-probes.md               — PR-1 to PR-9 probing patterns
│
├── knowledge/                            ← Convention rules
│   └── conventions.md                    — ID/naming/format standards
│
├── templates/                            ← FRD Pack file templates (9)
│   ├── 00_overview.template.md           — Document Control + Scope + Roles
│   ├── 01_ui.template.md                 — Pages + Components + Journey
│   ├── 02_api.template.md                — API contracts (HTTP layer)
│   ├── 03_logic.template.md              ⭐ NEW v5 — Functions + Engines + Trace
│   ├── 04_db.template.md                 — Tables + Fields + Relationships
│   ├── 05_rules.template.md              — Business Rules + Edge Cases + Errors
│   ├── 06_tests.template.md              — Acceptance + DoD + WebSocket events
│   ├── 07_locked_decisions.template.md   — LDs + Convention deviations
│   └── INDEX.template.md                 — Cross-reference + Quick nav (FULL only)
│
└── examples/                             ← Walkthrough examples
    ├── frd_v6_lean_walkthrough.md        — F-01 Customer Quick-Add (LEAN, 6 files, 0 engines)
    ├── frd_v6_standard_walkthrough.md    ⭐ NEW — F-02 Product Catalog (STANDARD, 7 files, 1 engine)
    └── frd_v6_full_walkthrough.md        — F-04 Payroll Cycle (FULL, 9 + INDEX, 3+ engines)
```

**Total:** 18 files · ~4,200 lines · ~135 KB

---

## 🎯 Key Features (v5 vs v4)

| Feature | v4 | v5 |
|---|---|---|
| **03_LOGIC.md** | Only FULL variant | **All variants (mandatory)** |
| **LEAN structure** | 02_API_DB merged | **02_API + 04_DB separate** |
| **Logic placement** | Implicit | **Explicit Matrix (10 patterns)** |
| **Function vs Engine** | Engine only | **Scope-local Functions + Reusable Engines** |
| **R8 Traceability** | ❌ | **✅ API → Function/Engine trace mandatory** |
| **Orphan detection** | ❌ | **✅ Phase 3.5 Section C** |
| **Hidden logic block** | Tolerated | **✅ Phase 3.5 Section G** |
| **File count** | 4 / 6 / 9 | **6 / 7 / 9** |

---

## 📥 Input Required

| File | Purpose |
|---|---|
| `F-XX_CODE.md` (Brief) | §3.4 Generator Hints (complexity, has-state, has-entity) |
| `BRD_F-XX.md` (APPROVED) | All 18 sections — primary spec source |

**Auto-read by skill:**
- Security Spec Bible
- html-generator-v9 SKILL.md (Layout patterns)
- `knowledge/conventions.md`
- `references/logic-placement-matrix.md`
- `references/cubic-schema-templates.md`

---

## 📤 Output

### Variant Selection (auto from Brief §3.4)

| Variant | File count | When to use |
|---|---|---|
| **LEAN** | 6 | Simple view/search/single-page feature |
| **STANDARD** | 7 | CRUD + simple workflow, ≤ 3 APIs |
| **FULL** | 9 + INDEX | Critical / state-machine / multi-engine / multi-step approval |

---

## 🔗 Pipeline Position

```
module-decomposer-erp
    ↓ Brief (F-XX_CODE.md)
brd-generator-full
    ↓ BRD (BRD_F-XX.md APPROVED)
frd-generator-v6  ⭐ THIS SKILL
    ↓ FRD_F-XX_Pack/
    ├──→ html-generator-v9     (HTML prototype)
    └──→ ai-testcase-md-generator + qa-friendly-html-generator (SOW3.5)
```

---

## ⚠️ Known Issues (จาก review รอบล่าสุด — pending fix)

1. **R9 ขัดกับ Matrix #6** — R9 บอก "pure display อาจ mark 03_LOGIC = N/A" แต่ Matrix #6 บอก "query builder = Function ใน §3.1" → recommend ใช้ Matrix เป็นหลัก (มี Function เสมอ)
2. **Function ID convention** — body ของ SKILL.md ยังมีบาง section ใช้ lowercase `f-xx-fn-nn` แทน `F-XX-FN-NN` (cosmetic)
3. **Trace Table ขนาด FULL** — ถ้า feature มี API 10+ × Function 15+ table จะใหญ่ — INDEX.md ช่วย group ได้ระดับหนึ่ง

แนะนำ dry-run กับ feature 1 ตัวก่อน (LEAN ก่อน) ก่อน rollout ใช้จริง

---

## 🎓 Quick Start Trigger

```
User → Claude:
  "สร้าง FRD จาก Brief + BRD นี้"
   + แนบ F-XX_CODE.md + BRD_F-XX.md

Skill (auto):
  Phase 0: Read Brief §3.4 → decide variant
  Phase 1: Sync read 6 references
  Phase 2: Generate Pack files in order (00→01→04→02→03→05→06→07→INDEX)
  Phase 2.5: Edge case probing (if triggers match)
  Phase 3.5: Mechanical verification (R8 + Logic Placement + Security)
  Phase 4: Deliver Pack + show next steps
```

---

## 📚 Documentation

- **Core spec:** `SKILL.md` (start here)
- **Logic decision guide:** `references/logic-placement-matrix.md`
- **Examples:** `examples/frd_v6_lean_walkthrough.md`, `frd_v6_standard_walkthrough.md`, and `frd_v6_full_walkthrough.md`
- **Conventions:** `knowledge/conventions.md`

---

## 🆚 Migration Notes

**From v4:**
- Old `03_ENGINE.md` → renamed to `03_LOGIC.md` with §3.1 Functions + §3.2 Engines
- LEAN no longer merges `02_API_DB` → separate files now
- All variants get `03_LOGIC.md` (was FULL only)
- New `references/logic-placement-matrix.md` is mandatory read in Phase 1

**From v25 (v2.8):**
- Single-file FRD → Pack folder
- Manual gates (Step 0, 0.5) → auto-detect from Brief §3.4
- Adds CUBIC alignment, Security Bible, R8 traceability

---

## 📝 Version

- **Version:** 5.0
- **Date:** 2026-05-18
- **Author:** 2BSimple team (with Claude)
- **License:** Internal use — 2BSimple Co., Ltd.
