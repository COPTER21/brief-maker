---
file_id: KB-04-02
title: Individual Skills — Detailed Reference
version: 2.0.0
last_updated: 2026-07-06
status: stable
---

# Individual Skills — Detailed Reference

## Quick Reference (TL;DR)

อธิบาย skill แต่ละตัวใน BA pipeline แยกตามหน้าที่:
- **Generation**: สร้าง artifact ใหม่ (brd/frd/html/bible)
- **Validation**: ตรวจ artifact
- **Reverse**: แปลง artifact ที่มีอยู่ → spec
- **Utility**: สนับสนุนการทำงาน

---

## 🛠 Generation Skills

### `value-stream-bible-generator` (v3.3)
- **Input**: chat discussion / brief / requirement
- **Output**: `VS_BIBLE.md` + `VS_BIBLE.html` (visual swim-lane navigator)
- **Purpose**: เอกสารแม่บทระดับ VS ที่ map VC → CL → SOP → SOW ต่อ scenario
- **Key sections**: department/position ownership, business-level data flow, cases (Happy/Alt/Error), edge cases, downstream module impact map

### `vs-feature-handover-pack`
- **Input**: VS Bible (.md)
- **Output**: 1 folder ต่อ feature (`F-XXX-NNN_Handover_Pack/`) — 7 ไฟล์ markdown
- **Files**: Brief, Capabilities, Dependencies, Governance, Related VCs, Locked Decisions, Checklist
- **Validation**: BLOCK ถ้าไม่ครบ
- **Plus**: `_SUMMARY.md` ที่ root + validation report

### `brd-generator-full` (v2.1 Business Edition — 2026-07-06)
- **ตำแหน่ง**: WF-01 SOW3.2
- **v2.1**: ถอด Design Authority ออก (ย้ายไป FRD) → BRD = business ล้วน · Scope Lock §3.4 สืบทอดใบเซ็น · §12.1 Value Stream + Downstream Impact Map (PR→PO→GRN→...) · §2.3 ตัวชี้วัดบังคับ baseline/target · §9.5 marker 🤖/✅ · Quality Gate C01-C23
- **Input**: RIF v2.1 (มี scope_lock_ref)
- **Output**: BRD_[feature].md + BRD_[feature].docx + AI Review Report
- **Coverage**: Draft → Enrich → Flexibility → Data Entity → Existing System → Quality Gate
- **Embedded**: Philosophy rules — COSO Roles, Security Preset (78 controls), SLA/KPI/Threshold tables
- **Types supported**: New Feature, Enhancement, Bug Fix, Config/Chore

### `frd-generator-v6` (v5.1)
- **Input**: Brief (.md) + BRD (.md) + Security Bible (auto-read)
- **Output**: FRD_F-XX_Pack/ — 6-9 ไฟล์ตาม variant (LEAN 6 / STANDARD 7 / FULL 9+INDEX)
- **Pack mode**: แยกไฟล์ตาม layer — 01_UI / 02_API / 03_LOGIC / 04_DB / 05_RULES / 06_TESTS
- **v5 features**: แยก Functions + Engines ใน 03_LOGIC, Logic Placement Decision Matrix, Iron Rule R8
- **v5.1 features**: Data Classification 4-level per-column (Public/Internal/Confidential/Restricted) + pii_flag + Iron Rule R10

### `html-generator-v9` (rebrand จาก v3.13 — 2026-07-06)
- **v4.0**: 48 Iron Rules (+#44-48: Loading, Form Section, Placement Contract, Stepper, Landing) · patterns A-M (+J Dashboard, K Report, L Collection, M Landing) · Unified Drawer v2 920/680 · Fixed Tokens · microcopy.md กลาง · One-Shot Policy (audit.sh = hard gate)

### `html-generator-v9` (superseded — ดู v4)
- **Input**: FRD v4 Pack หรือ Brief / BRD / screenshot / requirement text (flexible)
- **Output**: 1 ไฟล์ .html (single-file SPA)
- **Stack**: vanilla JS + self-contained CSS (no Tailwind CDN), hash routing (#/route refresh-safe)
- **Theme**: CUBE NATIVE — Navy #0B1D3A, Primary #0B5CFF, Teal #00A88E
- **Iron rule**: Create/Edit = Drawer slide-in 540px (NOT modal)
- **Patterns**: A-I + iron rules + CI tokens แยกไฟล์ load on-demand
- **Modes**: Pipeline (รับ FRD Pack — 01_UI.md primary) หรือ Standalone (รับ input อะไรก็ได้)

### `html-generator-v9`
- **Input**: Anything (Brief / FRD / Figma Spec / screenshot / text)
- **Output**: 1 ไฟล์ .html
- **Stack**: HTML + Tailwind CDN + vanilla JS
- **Difference from v3**: ใช้ Tailwind CDN (เก่ากว่า), Component Catalog 37 ตัว, Layout Library 5 templates

### `frd-to-html-prototype`
- **Input**: FRD + Figma Spec
- **Output**: single HTML file — render ทุกหน้าของ feature
- **Behavior**: hash routing, form interaction, modal/drawer/tab, mock data จาก §10.2 schema

### `figma-spec-generator`
- **Input**: FRD (.md) จาก frd-generator
- **Output**: FIGMA_[feature].md — prompt-ready spec สำหรับ Figma Make AI

### `feature-brief-generator`
- **Input**: flexible (text, screenshot, audio, video demo, transcript, mix)
- **Output**: Feature Brief (.md) ตาม template 10 sections
- **Next**: pair กับ `feature-brief-to-ui-spec` หรือ `scenario-generator`

### `pipeline-zigzag-designer`
- **Input**: problem / process / requirement
- **Output**: Zigzag.xlsx (1 sheet ต่อ channel) + data_contract_zigzag.json
- **Process**: 7 phases — Understand → VS → Channels → CL→SOP → Expand SOW → Self-check → Generate
- **Self-check**: Chain integrity (`C ของ SOW N = A ของ SOW N+1`)

---

## 🔍 Validation Skills

### `output-checker`
- **Purpose**: Final QC ของ pipeline (RIF + BRD + FRD + HTML)
- **Output**: `_OUTPUT_CHECK_REPORT.md` + verdict (PASS / WARN / BLOCK) + remediation plan
- **Auto-fix mode**: แนะนำ skill ที่จะรันแก้

### `frd-qa-generator`
- **Input**: FRD + Figma Spec
- **Output**: 3 .docx — Test Cases (Lean Stepper), Scenario List, Data Sample

### `compliance-preservation-checker`
- **Purpose**: Quality Gate Stage 4.5 — ตรวจ refactored HTML+FRD ว่า preserve invariants 100% (Axis A) + comply กับ Component/Layout catalog (Axis B)
- **Verdict**: PASS/WARN/BLOCK
- **Trigger**: run เมื่อมี `invariants.md` ใน folder (Refactor Wave path)

### `html-to-frd-sync`
- **Purpose**: ตรวจ drift ระหว่าง HTML ที่ vibe แก้แล้ว กับ FRD ต้นฉบับ
- **Classification**: UX drift (auto-sync) / Hidden logic (interactive Q&A) / Business drift (BLOCK + redirect RIF)

### Template Validation Chain (4 agents)
- `template-validation-orchestrator` — main entry
- `template-normalization-agent` — normalize format
- `schema-validation-agent` — schema + master lookup
- `business-rules-agent` — hierarchy + cross-field
- `quality-analysis-agent` — threshold + AI naming check

---

## ↩️ Reverse Skills

### `reverse-feature-analyzer`
- **Input**: existing code, DB schema, API, running UI
- **Output**: Feature Summary + FRD Input (.md)
- **Purpose**: extract spec จาก existing system (codebase → doc)

### `legacy-sources-reverser`
- **Input**: existing artifacts (FRD/HTML/Code/API/DB/Postman/screenshots/notes)
- **Output**: RIF.md (reverse-engineered) + invariants.md + reverse-report.md
- **Use**: Stage 0 entry of Refactor Wave path

### `frd-to-brd-reverse`
- **Input**: existing FRD (no BRD)
- **Output**: BRD AS-IS
- **Purpose**: บันทึก feature ที่พัฒนาไปแล้วเป็น BRD เพื่อ refactor

### `html-to-feature-brief`
- **Input**: HTML mockup/prototype
- **Output**: Feature Brief (.md) + Design Token (.md)
- **Classification**: Dashboard / Console / Feature → ส่งต่อ skill เฉพาะทาง

---

## ⚙️ Enhancement Skills

### `enhancement-ticket-pack-generator` (v2.0)
- **Input**: HTML before/after, BRD/FRD เดิม, screenshot, text, mix
- **Output**: ENH_[name]_Pack/ — 4-5 ไฟล์ markdown (diff-focused, ไม่ regen ของเดิม)
- **Variants**: SMALL 4 / MEDIUM 5 / LARGE 5+linked-FRD

### `enhancement-frd-generator`
- **Input**: existing UI/feature เดิม + requirement ใหม่
- **Output**: Enhancement FRD + Figma Spec + HTML Preview
- **Use**: เพิ่ม/ปรับ feature ที่มีอยู่แล้ว

### `enhance-analysis-generator`
- **Output**: Enhancement Analysis + UI Mockup Prototype + Dev Summary
- **Use**: วิเคราะห์ Enhancement พร้อม Prototype

---

## 🛠 Utility Skills

### `requirement-intake-formatter` (v2.1 Workflow Edition — 2026-07-06)
- **ตำแหน่ง**: WF-01 SOW3.1 · **v2.1**: Upstream Chain detection (REQ_CLASSIFY/SCOPE_CONFIRM/Pre-Brief/Sign-off) · V-12 Scope Lock (BLOCK) + V-13 Scope Drift (WARN) · templates จริงใน references/
- **Input**: HTML mockup / Client Doc / Chat Context / Filled Template
- **Output**: RIF_v2_[feature].md (16 sections) + Filled_Client_Spec + Gap_Report
- **Confidence**: ≥80% to BRD

### `psap-generator`
- **Output**: PSAP/OSAP/POSAP Brief — Stage 0 (Pre-Brief) ที่แปลง Raw Input → 6 องค์ประกอบ
- **Modes**: PSAP (Problem) / OSAP (Opportunity) / POSAP (Hybrid)

### `feature-decomposer`
- **Output**: Feature Map — กี่ Feature, กี่ BRD, ลำดับยังไง

### `module-decomposer` / `module-decomposer-erp`
- **Input**: HTML Module (multi-feature) + Client Spec
- **Output**: Feature Inventory + per-feature briefs
- **ERP version**: เพิ่ม SAP/Odoo standard research

### `dev-brief-generator`
- **Input**: FRD + Figma Spec
- **Output**: DEV_BRIEF_[feature].docx — quick bible สำหรับ Dev 15 นาที

### `cube-native-ci-converter`
- **Input**: any HTML
- **Output**: HTML ตรง CUBE NATIVE CI 100% (Strict Mode)

### `manual-generator` / `module-manual-builder` / `vdo-to-user-guide`
- **Purpose**: สร้างคู่มือผู้ใช้/Operation Manual จาก FRD/video/screenshot/transcript

---

## 📊 Specialized Generators

### `dashboard-query-brief-generator-v2`
- **Input**: Feature Brief (Type=Dashboard) + Schema
- **Output**: Dashboard Brief — query mapping ทุก section
- **Use**: dashboard ทั่วไป (ไม่ใช่ Report Module)

### `report-brief-generator-v3`
- **Output**: Report Brief สำหรับ Dashboard (D) / Data Report (T) × 3 classes (Operation/Performance/Custom)

### `console-brief-generator`
- **Use**: หน้าจอที่ทั้งแสดงข้อมูล + ทำ action (display + action)
- **Output**: Console Brief — display spec + action spec + state management

### `entity-spec-generator`
- **Use**: Master Data Browser & Export module
- **Input**: Database Schema
- **Output**: Entity Spec (.md)

---

## Change Log

- **1.0.0** (2026-05-27): Initial catalog of BA pipeline skills

## 🆕 Workflow Skills (2026-07-06)

### `requirement-classifier` (v1.0 — SOW1.2)
- อ่านคำขอลูกค้าทุกรูปแบบ → จำแนก New Requirement / New Feature / Enhancement + confidence + anchor feature + effort S/M/L + routing WF-01/02/03
- Output: REQ_CLASSIFY_*.docx (8 sections) + .md — Round เดียวจบ
- แทน `ticket-checker` ในสาย workflow (ticket-checker ยังใช้ triage Bug ฝั่ง Airtable)

### `business-proposal-generator` (v2.0 — SOW1.3)
- Mode A: Scope Confirmation (งานในสัญญา) / Mode B: Proposal+Pricing Annex VAT7% (นอกสัญญา)
- รับ REQ_CLASSIFY เป็น input · Customer Approval บังคับทุกโหมด · Output SCOPE_CONFIRM_*/PROPOSAL_* .docx+.md
