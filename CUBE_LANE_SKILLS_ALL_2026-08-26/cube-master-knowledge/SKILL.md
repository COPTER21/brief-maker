---
name: cube-master-knowledge
description: |
  Master knowledge base ของ CUBE NATIVE / CUBE 4.0 (2BSimple ERP platform). ใช้เมื่อ user ถาม
  เรื่อง CUBE concept, hierarchy ของ business process (VS/VC/Path/CL/SOP/SOW), architecture
  (7 domains: Cubic/Knowledge/Core Cube/Agent/Policy/HR/Report), Value Stream Bible (P2P เต็ม +
  template สำหรับ O2C/H2R/R2R), BA pipeline skills (frd-generator-v6, brd-generator-full,
  html-generator-v9, value-stream-bible-generator, requirement-classifier, etc.), Workflow Master
  (WF-01..WF-06 + skill mapping ต่อ SOW), feature
  catalog ทั้ง CUBE, CI standards (Navy/Blue/Teal), หรือ glossary term (DOA, 3-way match,
  RTV, AIR, ENC, RIF, BRD, FRD, etc.). ใช้เมื่อ user พูดถึง: "cube knowledge", "master knowledge",
  "VS/VC/Path คืออะไร", "อธิบาย CUBE",
  "DOA pattern", "skill ในไหน", "workflow master", "WF-01", "SOW ไหนใช้ skill อะไร",
  "บันทึก knowledge", "update master knowledge", "อัพเดต cube".
  Read + Write — อัพเดต knowledge ผ่าน chat ได้. Always check this skill BEFORE answering
  CUBE-related questions to avoid stale memory.
---

> **Sync Read (2026-08-25):** ทุกที่ที่อ้าง `html-generator-v9` = html-generator **เวอร์ชันสูงสุดที่ติดตั้ง**
> (`GEN=$(ls -d /mnt/skills/user/html-generator-v* | sort -V | tail -1)`) — ณ วันนี้คือ v9 (Pattern Q/P · B2 v2 · Iron Rules #1–#103)
> ห้าม hardcode CI/จำนวนกฎ/px จาก generator เก่า · FRD = frd-generator-v6 · BRD = brd-generator-full

# CUBE Master Knowledge

Single source of truth สำหรับทุก concept, architecture, skill, และ Value Stream ของ CUBE NATIVE / CUBE 4.0

---

## 🎯 When to use this skill

ใช้ทุกครั้งที่ user:
1. **ถาม** เรื่อง CUBE concept, term, hierarchy, architecture
2. **list** features/scenarios/paths ของ Value Stream ใดๆ
3. **อธิบาย** skill ใน BA pipeline ทำอะไร
4. **เพิ่ม/แก้** knowledge — user สั่ง "update master knowledge: [topic]" หรือ "บันทึกเข้า cube knowledge"
5. **recall** cube concept (เลือก skill นี้แทน memory ที่อาจ stale)

---

## 📂 Knowledge Organization (7 categories)

```
knowledge/
├── 01_hierarchy/      ← VS / VC / Path / CL / SOP / SOW definitions + decision rules
├── 02_architecture/   ← CUBE 4.0 (7 domains) + governance (DOA + UA) + development standards
├── 03_value_streams/  ← per-VS full bibles (P2P, O2C, H2R, R2R, I2C, CM, AM)
├── 04_skills/         ← BA pipeline skills (frd-generator-v6, brd-generator-full, ...)
├── 05_features/       ← CUBE-wide feature catalog
├── 06_ci_standards/   ← CUBE NATIVE CI (Navy/Blue/Teal, fonts, components)
└── 07_glossary/       ← term definitions (DOA, 3-way, RTV, AIR, ENC, Tier, ...)
```

## 🗺 Routing — เปิดไฟล์ไหนเมื่อถามอะไร

| User asks about | Open file(s) |
|---|---|
| Workflow Master / WF-01..06 / SOW ไหนใช้ skill อะไร | `knowledge/04_skills/workflow-master-wf01-06.md` ⭐ |
| VS/VC/Path/CL/SOP/SOW hierarchy | `knowledge/01_hierarchy/vs-vc-path-cl-sop-sow.md` |
| CUBE 4.0 architecture / domains / modules | `knowledge/02_architecture/cube-4.0-master-bible.md` |
| DOA / User Access / Governance pattern | `knowledge/02_architecture/governance-doa-ua.md` |
| P2P (procure-to-pay) — payment terms, paths, features | `knowledge/03_value_streams/p2p-full-bible.md` |
| O2C, H2R, etc. | `knowledge/03_value_streams/[vs]-bible.md` (อาจเป็น placeholder) |
| Specific skill behavior (frd-generator-v6, brd-generator-full, etc.) | `knowledge/04_skills/[skill-name].md` |
| **โครงปัจจุบัน (หลังยุบรวม) · baseline platform · มติ · OQ** | **`knowledge/02_architecture/cube-4.0-current-state.md`** ← อ่านก่อน bible |
| Feature catalog (แผง 7C 140 · เสร็จ/ค้าง · declarations · archetype) | `knowledge/05_features/feature-catalog-master.md` (v2.0) |
| Color, font, component standards | `knowledge/06_ci_standards/cube-native-ci.md` |
| Term definitions | `knowledge/07_glossary/terms.md` |
| "What's in the knowledge?" | Read `INDEX.md` first |

**Tip**: Always start by reading `INDEX.md` to see what's available + version dates.

---

## 🔄 Update workflow

When user says "update master knowledge: [topic]" or "บันทึกเข้า cube knowledge":

1. **Locate** the relevant file (using routing table above)
2. **Read** current content
3. **Identify** where to add/edit (append to relevant section, or create new section)
4. **Update** via `str_replace` or full rewrite
5. **Bump version**: increment in file's frontmatter + update `last_updated` date
6. **Sync INDEX.md**: update last-updated date for that file

**Versioning rule**:
- Minor edit (typo, clarification): patch bump (1.0.0 → 1.0.1)
- New section or concept added: minor bump (1.0.1 → 1.1.0)
- Restructure / breaking change: major bump (1.1.0 → 2.0.0)

---

## 📖 Answer workflow

When user asks a CUBE-related question:

1. **Identify** which knowledge category fits
2. **Read** the file(s) listed in routing table
3. **Answer** from the file content (cite which file if user asks where it's from)
4. If knowledge gap exists → tell user: "เรื่องนี้ยังไม่มีใน master knowledge — อยากให้บันทึกเพิ่มไหม?"

**Never fabricate** — if not in knowledge files, say so. Don't fall back to general memory.

---

## ⚙️ File structure within each knowledge file

```markdown
---
file_id: KB-XX-YY
title: [topic]
version: X.Y.Z
last_updated: YYYY-MM-DD
status: stable | draft | deprecated
---

# [Title]

## Quick Reference (TL;DR)
(short summary 2-3 lines)

## [Content sections]
...

## Change Log
- vX.Y.Z (YYYY-MM-DD): [change description]
```

This ensures every knowledge file is **self-describing** and **version-trackable**.

---

## 🚦 Boundaries

| Do | Don't |
|---|---|
| Read knowledge files before answering CUBE questions | Answer from training-data memory alone |
| Update knowledge when user shares new info | Update without user confirmation |
| Cite which file an answer came from | Make up file references |
| Tell user when knowledge is missing | Pretend to have answer when it's not in files |

---

**Skill version: 1.0.0**
**Last knowledge sync: 2026-05-27**
