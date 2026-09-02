---
file_id: KB-02-03
title: CUBE 4.0 Current State (post-consolidation)
version: 1.0.0
last_updated: 2026-08-25
status: active
supersedes: cube-4.0-master-bible.md §2–§3 (โครง 7 domain แยก site — historical)
---

# CUBE 4.0 — Current State (ณ 2026-08-25)

## Quick Reference (TL;DR)

- **ยุบรวมเป็น ERP เดียว**: HR / Agent / Report / Policy Center / QA ถูกรวมเข้า **Core Cube** (core.2bsimple.com) เป็น "area" ภายในระบบเดียว — ลูกค้าติดตั้งตัวนี้ตัวเดียว
- เหลือแยก site 2 ตัว (เฉพาะเรา): **Cubic** (backbone/registry) · **Knowledge + CMS** (content)
- Policy Center = governance layer คร่อมทุก area · Agent = AI เรียกทุก area ผ่าน API · Report = read layer จาก 7C event
- Feature ทั้งหมดในแผง 7C = 140 (เสร็จ 54) → `05_features/feature-catalog-master.md` v2.0
- Bible เดิม (`cube-4.0-master-bible.md`) ยังใช้ได้เฉพาะ §4 patterns · §5 dev process · §8 glossary — โครง domain ใน §2–§3 **ล้าสมัย**

---

## 1. โครงสร้างปัจจุบัน

```
        ┌──── Portal กลาง (อนาคต) ────┐
   ╔═══════════════ Core Cube (ERP เดียว) ═══════════════╗
   ║ [Policy Center] governance คร่อมทุก area            ║
   ║   Operation · HR · Report(7C) · Agent · QA          ║
   ╚════════════════════════════════════════════════════╝
   [Cubic] backbone (แยก site)   [Knowledge+CMS] content (แยก site)
```

| Area ใน Core | Modules (แผง 7C) |
|---|---|
| Operation | **Operation Process** (CL/SOP/SOW · งาน · Cockpit · Action/Team Plan · Configuration) · General · Sales · Marketing · Purchase · Warehouse · OFM · Budget · Accounting · Finance · CS (+ CRM · Asset · Org · IT Ticket นอกแผง) |
| HR | HR 17 features (Employee Master → Payroll chain → ESS) |
| Policy Center | DOA · Roles & Permissions · Password/MFA/Session · Data Masking · Audit Trail · Data Classification (+ Security ~27 features tier ถัดไป) |
| Report | 7C Consequence 7 หน้า (OC/EC/AC/Business Central/FC/SecC/DC) |
| Agent | Chat Bubble · Agent Binding · Skill Library |
| QA | Feature Tester · Ticket |

## 2. Platform baseline (engines/ฐานที่มีแล้ว — ทุก feature เรียกใช้)

ดูตารางเต็มใน `05_features/feature-catalog-master.md §0` — สรุป: **OP (CL/SOP/SOW + งานของฉัน + Cockpit) · Action Plan · Team Plan · DOA Engine (doa-declaration) · Document Configuration (doccfg) · Notification (ntf) · Roles/Permission/Employee/User Mgmt · ENG-CSQ 7C (csq) · Knowledge Center · Agent · Cubic Registry**

Contract ของ feature ใหม่ = **ประกาศ ไม่ implement**: `DOA_BRIEF` / `NTF_BRIEF` / `CSQ_BRIEF` / `DOCCFG_BRIEF` (companion skills) → ระบบ auto-register ตอน deploy

## 3. Locked decisions (มติ) ที่ทุก feature ต้องเคารพ

| มติ | สาระ |
|---|---|
| DOA iron rule | ไม่มี hardcoded approval chain — ทุก feature `GET /doa/resolve` |
| มติ 2026-08-17 DOA UI | ตอนส่งอนุมัติ ทุก slot ต้องเลือก "คน" ในตำแหน่ง — แสดง avatar + position + name (ไม่ใช่ role id ลอย) |
| LD-4C-02 soft reference | master = picker assist · nullable · ไม่มี FK cascade |
| Audit | append-only · ไม่มี hard delete (soft archive) |
| HR-1 | legal/config parameter ใช้ `effective_date` เสมอ (กฎหมายแรงงานไทย) |
| Engine-in-feature | engine เกิดใน feature → Architect ลง CUBIC เป็น candidate (เช่น policy-change-diff-engine, ENG-OFM-SCOPE-01, task-lifecycle-engine) |
| Module Linkage | module ที่ run standalone ได้ต้องมี config เชื่อม/ไม่เชื่อม + manual status override |
| มติ 2026-08-16 Sales lane | BA ส่ง HTML + PREBRIEF เท่านั้น · sub-team ทำ FRD/TC |
| 7C ท่อต้องห้าม | OC (มาจาก OP) · DC-document (มาจาก DOA) · SC (สงวน) — ประกาศซ้ำ = 422 |
| UI standard | html-generator-v9: Pattern Q ทุกเอกสารธุรกรรม · B2 v2 line editor · #102 combobox anatomy · #103 lean list · CI Warm Light |

## 4. OQ ที่ยัง block (ณ 2026-08-25)

| OQ | เรื่อง | เจ้าของ | กระทบ |
|---|---|---|---|
| OQ-HR-01 | payroll build ภายในหรือไม่ | Strike | 12 HR features |
| OQ-N7 | Notification embed core-shell vs แยก | Chin | F-NT-03 |
| OQ-1..5 / OQ-6 | LINE integration F-AG-03/04/05 | พี่เบิร์ด / Strike | F-AG-05 |
| ENG-OFM-SCOPE-01 · ENG-CSQ-01/02 | register ใน CUBIC | Architect | OFM M2 · 7C dev |

## 5. Wave plan / automation

- แผง 7C: 9 waves (W1 24 ส.ค. → W9 1 ก.ย.) ~10 feature/wave · 3 lane ขนาน — **v2 dependency-corrected รอ rebuild** (v1 มี dep ผิด เช่น ESS Portal)
- Auto-lane (ออกแบบ 2026-08-25): POOL → WAVE CHECKLIST → Cowork run — ดู `04_skills/workflow-master-wf01-06.md` + CUBE_FULLRUN_WORKFLOW

## Change Log
- **1.0.0** (2026-08-25): สร้างใหม่หลังยุบรวม — แทน bible §2–§3 · รวมมติ/OQ/baseline ที่กระจายใน memory
