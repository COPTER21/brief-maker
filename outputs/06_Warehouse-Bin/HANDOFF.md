# HANDOFF — Warehouse & Bin (F-LOC) · WF-01 Steps 5–10

> ส่งต่อให้ AI agent อื่น (เช่น Codex) ทำ pipeline ที่เหลือ · อัปเดต 2026-08-12
> **Feature:** F-LOC / F-LOCATION-MASTER-001 · **Output dir:** `outputs/06_Warehouse-Bin/`

---

## ✅ ทำเสร็จแล้ว (Steps 1–4 + gate ผ่าน)
| Step | ผล |
|---|---|
| 1. html-generator-v8 | `warehouse-bin.html` (single-file SPA) — **source of truth ของทุก step ถัดไป** |
| 2. thai-doc-pdf | **SKIP** (master data ไม่มีเอกสารพิมพ์) |
| 3. qc-ux-html-checker | PASS (BLOCK 0) → `_UX_CHECK_REPORT.md` |
| 4. qc-coverage-checker | PASS (FN 19/20, edges 2/2, rules 13/13, creep 0) → `_COVERAGE_REPORT.md` |
| E2E (browser) | `02_QC/e2e_warehouse.py` — **33/33 × 2 รอบ PASS** |
| PM/BA review | **ผ่าน** (แก้ postcode disabled + ย้ายปุ่มสร้างเข้า filter-bar แล้ว) |

## 🎯 เหลือทำ (Steps 5–10) — ตามลำดับ ห้ามสลับ (แต่ละ step กินผลลัพธ์ step ก่อนหน้าเป็น input)
| # | Skill | Input | Output (แนะนำ path) | เกณฑ์ผ่าน |
|---|---|---|---|---|
| 5 | **brd-generator-full** (Fresh/HTML-first) | `warehouse-bin.html` + Pack Brief (PREBRIEF/CHECKLIST) + Company ref + `_UX_CHECK_REPORT.md` + `_COVERAGE_REPORT.md` | `03_BRD/BRD_Warehouse_Bin.md` | Screen Inventory ตรงหน้าจอจริง · Scope Lock (ดูด้านล่าง) · Downstream Impact |
| 6 | **frd-generator-v6** (HTML-first) | **BRD (step5)** + `warehouse-bin.html` | `04_FRD/FRD_F-LOCATION-MASTER-001_Pack/` (แยก layer UI/API/LOGIC/DB/Rules/Tests) | R8 traceability · R10 Data Class · Coverage Manifest · Section M (HTML alignment) |
| 7 | **html-ui-brief** | `warehouse-bin.html` + FRD pack (step6) | `05_UI_BRIEF/UI_BRIEF_F-LOCATION-MASTER-001.md` | Extraction-based 1:1 (ทุกบรรทัด trace หา selector/function จริงใน HTML) · Drift Log |
| 8 | **ai-testcase-md-generator** | FRD pack + BRD + `warehouse-bin.html` | `testcase_qa/testcases-F-LOCATION-MASTER-001.md` | anchor ด้วยข้อความบนจอ + route จริง · ครอบ happy/neg/edge/perm · trace กลับ 05_RULES/06_TESTS |
| 9 | **qa-friendly-html-generator** (Lite-first) | **testcases md (step8)** (+ HTML) | `testcase_qa/testcase-warehouse-bin.html` | คนไม่รู้ระบบทำตามได้ · คง TC id เดิม · ไม่มีค่า mock ค้าง |
| 10 | **feature-tldr-html** | FRD pack (+ HTML) | `08_TLDR/tldr-warehouse-bin.html` | ภาษาเด็ก 5 ขวบ · ไม่มี field/API/SQL |

**Companion skills (doa/ntf/doccfg) = ไม่ต้องทำ** — feature นี้ไม่มี DOA (RBAC), ไม่ออกเอกสาร, ไม่มี notify event ของตัวเอง

---

## 🔒 LOCKED SCOPE & DECISIONS (สำคัญ — อย่าให้ agent เพิ่ม/เปลี่ยนเอง)
1. **Ref แค่ Company เท่านั้น** ผ่าน `branch_id` → `T_branch` (soft-ref, picker active-only, ไม่มี FK cascade). **ไม่มี `company_id`** (1 ERP = 1 company). Child (Zone/Area/Rack/Location) inherit branch ผ่าน warehouse_id chain.
2. **ตัดทิ้ง (de-scoped โดย PM/BM):** F-INV build-out, Geo Master schema, GRN/Putaway/RTV/Pick-Pack-Ship. อย่าใส่กลับเป็น flow. (edge `Warehouse&Bin → Inventory` = soft [config] = storage_uom lock + hasStock เท่านั้น, mock ไว้แล้ว)
3. **ไม่มี DOA** — ใช้ RBAC `canManage` (OB-11 / LD-07). อย่าใส่สายอนุมัติ.
4. **CI = CUBE Warm Light v8** (Ivory/Charcoal/Red #FF3B30/Orange #FF9A1F, Satoshi + Noto Sans Thai). Iron rules v8.
5. **[AI-DEFAULT] convention** — สมมติฐานที่ต้องเดา ให้ mark `[AI-DEFAULT]` inline เสมอ (เช่น branch inactive `00003 สาขาระยอง` = mock สาธิต active-filter).
6. **HTML = source of truth** — microcopy/label ทุกจุดต้องดึงจาก `warehouse-bin.html` ตามจริง (Sync Read) **ห้าม hardcode/แต่งเอง**.

## 📎 Source-of-truth files (paths)
- Prototype: `outputs/06_Warehouse-Bin/warehouse-bin.html`
- QC: `outputs/06_Warehouse-Bin/_UX_CHECK_REPORT.md`, `_COVERAGE_REPORT.md`
- E2E: `outputs/06_Warehouse-Bin/02_QC/`
- Pack Brief: `Pack Brief Feature/6. Warehouse/` (PREBRIEF_F-LOC…, FUNCTION_CHECKLIST_F-LOC…)
- Architecture: `Central Plan v2/` (Company → Warehouse & Bin [config] · Warehouse & Bin → Inventory [config])
- Company ref: `Related context/Company/` (organization-management.html + FRD/*.md — **ข้าม `06_TESTS.md`**)

## 🧰 Skills (portable) — ให้ Codex โหลดเป็น instructions
ชุดพร้อมส่งต่อ: **`WF-01_Pipeline_SkillSet/WF_Pipeline_SkillSet/<skill>/SKILL.md`** (+ `references/` `templates/` `examples/`)
สำเนาเหมือนกันอยู่ที่ `.agents/skills/<skill>/` และ `.claude/skills/<skill>/`
> วิธีใช้กับ Codex: เปิด `SKILL.md` ของ step นั้น แปะเป็นคำสั่งระบบ แล้วป้อน input ตามตาราง → ทำตาม SKILL.md ตรง ๆ

## ⚠️ ข้อควรระวังเมื่อไม่ใช่ Claude Code
- **Chain ต่อเนื่อง**: ทำ 5→6→7→8→9→10 ตามลำดับ เอา output ตัวก่อนเป็น input ตัวถัดไป
- **Step 9 (qa-friendly)** มี `scripts/capture.py` ใช้ถ่าย screenshot จาก HTML (ต้องมี Python + Playwright + Chromium) — ถ้า Codex รัน browser ไม่ได้ ให้ทำโหมด no-shot หรือรัน capture.py เองแยก
- **Step 8 (testcase md)** เป็นการ "เขียน" markdown ล้วน ไม่ต้องรัน script — Codex ทำได้สบาย
- WF-01 pack README เขียนอ้าง html-generator-**v7** แต่ prototype จริงเป็น **v8** — ตอน Sync Read iron-rules/CI ให้ยึด v8 (ไฟล์ `html-generator-v8/`)
- จุดที่ agent อื่นมักหลุด → **รีวิวเป็นพิเศษ**: FRD traceability (R8), microcopy verbatim, Scope Lock (ข้อ 1–2 ด้านบน)

## 📋 Prompt เปิดงานให้ Codex (แปะได้เลย)
```
You are continuing the WF-01 documentation pipeline for feature F-LOC (Warehouse & Bin).
Read outputs/06_Warehouse-Bin/HANDOFF.md fully first. Steps 1–4 are DONE and PM/BA-approved.
Do Steps 5–10 IN ORDER. For each step: load the matching SKILL.md from
WF-01_Pipeline_SkillSet/WF_Pipeline_SkillSet/<skill>/, use the listed inputs (HTML is the
source of truth — never invent microcopy), write to the listed output path, and obey the
LOCKED SCOPE (ref ONLY Company via branch_id; no DOA; no dropped modules; mark [AI-DEFAULT]).
Feed each step's output as the next step's input. Stop and show me after Step 6 (FRD) for review.
```
