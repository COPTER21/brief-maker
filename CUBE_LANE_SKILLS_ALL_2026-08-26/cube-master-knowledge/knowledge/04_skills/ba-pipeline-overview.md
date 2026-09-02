---
file_id: KB-04-01
title: BA Pipeline Overview
version: 2.0.0
last_updated: 2026-07-06
status: stable
---

# BA Pipeline Overview

> ⭐ **v2.0 (2026-07-06): operating model หลักย้ายไป Workflow Master (WF-01..WF-06)** —
> ดู `04_skills/workflow-master-wf01-06.md` เป็นตัวจริง ไฟล์นี้คงไว้เป็นมุมมอง stage-based (Bible path)
> ใช้ Bible path (Stage A-E) เมื่อออกแบบ VS/module ใหม่ทั้งก้อน · ใช้ WF-01 เมื่อทำ feature ตามงานลูกค้า

## Quick Reference (TL;DR)

Pipeline ของ BA ที่ 2BSimple ใช้ — ต้นทาง requirement → HTML prototype พร้อม dev:

```
Requirement
   ↓
[Stage A] vs-charter-intake (planned)
   ↓
[Stage B] value-stream-bible-generator (v3.3 → v2 upgrade planned)
   ↓
[Stage C] vs-feature-handover-pack OR bible-to-brief-expander (planned)
   ↓
[Stage D] brd-generator-full v2.1 → frd-generator-v6 → html-generator-v9
   ↓
[Stage E] pipeline-strict-qc (planned)
   ↓
Hand-off to Dev
```

---

## 1. Pipeline Stages

### Stage A — Intake
**Goal**: รับ requirement ดิบ → จัดให้เป็นเอกสารโครงสร้างมาตรฐาน
- Existing: `requirement-intake-formatter`, `psap-generator`, `feature-decomposer`
- Planned: `vs-charter-intake`

### Stage B — VS Bible
**Goal**: สร้างเอกสารแม่ระดับ VS ที่ครอบทุก VC + Path + Feature
- Existing: `value-stream-bible-generator` (v3.3)
- Planned upgrade: v2 — เพิ่ม Feature Catalog, Dependency Map, Shared Logic, Integration Points, HTML navigator, XLSX matrix

### Stage C — Feature Brief Pack
**Goal**: แตก VS Bible → Brief Pack per feature
- Existing: `vs-feature-handover-pack`
- Planned: `bible-to-brief-expander` (replacement)

### Stage D — Document Generation
**Goal**: One-shot generate BRD → FRD → HTML
- `brd-generator-full` v2.1 → BRD.md (+ §3.4 Scope Lock, §12.1 Value Stream Impact)
- `frd-generator-v6` → FRD pack (6-9 ไฟล์: UI / API / LOGIC / DB / Rules / Tests)
- `html-generator-v9` → single-file SPA HTML (48 Iron Rules, patterns A-M, One-Shot)

### Stage E — QC
**Goal**: ตรวจ consistency ทุก layer ก่อนส่ง dev
- Existing: `output-checker`, `frd-qa-generator`
- Planned: `pipeline-strict-qc` — 4-layer report

---

## 2. Document Chain

```
Charter (.md)
    ↓
VS Bible (.md + .html + .xlsx)
    ↓
Brief Pack/F-XXX/ (4 .md files)
    ↓
BRD_F-XXX.md
    ↓
FRD_F-XXX_Pack/ (6-9 files)
    ↓
F-XXX.html (single-file SPA)
    ↓
[QC Report]
```

---

## 3. When to Use What

| User intent | Skill to use |
|---|---|
| requirement/ticket เข้า → คัดประเภท | `requirement-classifier` (SOW1.2) |
| เคาะ scope/ราคา ก่อนเปิดงาน | `business-proposal-generator` v2 (SOW1.3) |
| มี requirement ดิบ → ทำให้ structured | `requirement-intake-formatter` v2.1 หรือ `psap-generator` |
| ตั้งโจทย์ใหญ่ → แตกเป็น feature | `feature-decomposer` |
| ออกแบบ VS แม่บท | `value-stream-bible-generator` |
| มี VS Bible → ทำ Brief per feature | `vs-feature-handover-pack` |
| มี Brief → ทำ BRD | `brd-generator-full` |
| มี BRD → ทำ FRD | `frd-generator-v6` |
| มี FRD → ทำ HTML | `html-generator-v9` |
| ตรวจ output | `output-checker` หรือ `frd-qa-generator` |
| แก้ feature ที่มีอยู่แล้ว | `enhancement-ticket-pack-generator` หรือ `enhancement-frd-generator` |
| reverse จาก code → doc | `reverse-feature-analyzer` หรือ `frd-to-brd-reverse` |
| reverse จาก HTML → spec | `html-to-feature-brief` หรือ `legacy-sources-reverser` |
| สร้าง zigzag จาก process | `pipeline-zigzag-designer` |
| ตรวจ Template CL/SOP/SOW | `template-validation-orchestrator` |

---

## 4. Skill Status Map

### Production-ready (ใช้งานจริง)
- `frd-generator-v6` (v5.1 — มี Data Classification + Iron Rule R10)
- `brd-generator-full`
- `html-generator-v9` (rebrand จาก v3.13)
- `value-stream-bible-generator` (v3.3)
- `vs-feature-handover-pack`
- `pipeline-zigzag-designer`
- `feature-brief-generator`
- `requirement-intake-formatter`
- `enhancement-ticket-pack-generator` v2.0
- Template validation chain (4 agents)

### Planned (จากการคุยล่าสุด)
- `vs-charter-intake` (Stage A bootstrap)
- `vs-bible-generator-v2` (upgrade Stage B — เพิ่ม §5-§10)
- `bible-to-brief-expander` (Stage C replacement)
- `pipeline-strict-qc` (Stage E new)

---

## 5. Iron Rules ที่ทุก skill ใน pipeline ต้องปฏิบัติ

1. **CUBE 4.0 §5 — Feature-DOA Pairing**: ทุก BRD/FRD ต้องมี §Governance
2. **No hardcode approval logic**: ทุก approval ผ่าน DOA registry
3. **Data Classification R10**: ทุก column ใน FRD §DB มี `classification` + `pii_flag`
4. **3-layer hierarchy**: UI / API / Engine แยกกัน (FRD pack mode)
5. **CUBE NATIVE CI**: Navy `#0B1D3A` / Primary `#0B5CFF` / Teal `#00A88E` / Inter + Noto Sans Thai

---

## Change Log

- **2.0.0** (2026-07-06): ชี้ Workflow Master เป็น operating model หลัก + sync ชื่อ skill (html-generator-v9, brd v2.1, RIF v2.1, requirement-classifier, business-proposal v2)
- **1.0.0** (2026-05-27): Initial pipeline overview
