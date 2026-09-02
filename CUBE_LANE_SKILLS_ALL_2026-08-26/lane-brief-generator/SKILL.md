---
name: lane-brief-generator
description: >
  สร้าง LANE_BRIEF — ใบสั่งเข้าเลน WF-01 ต่อ feature (S0 ของ feature-lane-runner v2). ★ v2: รับ input จาก
  WAVE_CHECKLIST.md / POOL.json (แผง Feature Checklist) + cube-master-knowledge (current-state มติ/baseline ·
  catalog archetype/declarations) + CONTEXT_PACK ต่อ module — Central Plan (workflow_graph) เป็น optional.
  Validate ก่อนออกเสมอ: feature มีใน pool/graph · dependency เสร็จ · LOCK/OQ refs มีจริง · archetype ชัด.
  Brief แบกเจตนา + ตัวชี้ (archetype · declarations doa/ntf/csq/doccfg/pdfdoc · scope note · skill ที่ต้องรัน)
  ห้าม copy กฎลง brief. รองรับ single feature และ batch ทั้ง wave. ใช้เมื่อ user พูดถึง "lane-brief-generator",
  "สร้าง LANE_BRIEF", "ออกบรีฟเข้าเลน", "บรีฟตั้งต้น", "เตรียมบรีฟ SOW1", "ออกใบสั่ง feature", "บรีฟทั้ง wave",
  "เตรียมงานเข้า pipeline", "จะรัน feature ไหนดี". Output: LANE_BRIEF_<id>.md ต่อ feature + _VALIDATION.md
---

# Lane Brief Generator v2 — ออกใบสั่งเข้าเลน (S0)

> งานเดียว: แปลง "รอบนี้ทำ feature X" (แถวใน WAVE_CHECKLIST) ให้เป็น `LANE_BRIEF_<id>.md` ที่ **validate แล้ว**
> พร้อมให้ `feature-lane-runner v2` วิ่ง S1 (PREBRIEF) ต่อโดยไม่ต้องถามคน — brief คือจุดเดียวที่คนใส่เจตนา

## Position (workflow POOL → CHECKLIST → RUN)

```
P1 แผง Feature Checklist (POOL.json)   P2 เลือก → WAVE_CHECKLIST.md   P3 /wave check
                                                   ↓
                                       [lane-brief-generator v2]  ← S0
                                                   ↓
                LANE_BRIEF_<id>.md → S1 feature-prebrief → S1.5 standard → S1.8 declare → S2 html v9 → …
```

## Input (ลำดับศักดิ์ — บนทับล่างเมื่อขัด)

| # | Input | จำเป็น | ใช้ทำอะไร |
|---|---|---|---|
| 1 | แถว feature ใน `briefs/<W>/CHECKLIST.md` **หรือ** entry ใน `POOL.json` (BACKLOG_7C) | ✅ | ชื่อ · module · wave · status · **declarations {doa,ntf,csq,doccfg,pdfdoc}** · archetype_guess · depends_on · **scope note / OQ ที่คนตอบไว้** |
| 2 | `cube-master-knowledge/02_architecture/cube-4.0-current-state.md` | ✅ | §2 baseline ที่ห้าม re-implement · §3 มติ (DOA 17 ส.ค., LD-4C-02, HR-1, Sales lane…) · §4 OQ ที่ block |
| 3 | `cube-master-knowledge/05_features/feature-catalog-master.md` | ✅ | §0 baseline table · ยืนยัน archetype/declarations ของ feature · feature ข้างเคียงใน module |
| 4 | `knowledge/CONTEXT_PACK/<module>.md` (ถ้ามี) | ⬜ | มติ/LOCK/pattern เฉพาะ module ที่เคาะในแชท (สะสมจาก wave ก่อน) |
| 5 | Central Plan `GRAPH/workflow_graph.json` + `GOLDEN_RULES.md` + `BUILD_ORDER.md` | ⬜ optional | edges in/out · golden rules · LOCK sources — ถ้ามี = contract ข้าม feature (coverage ใช้) |
| 6 | `FEATURE_REGISTRY.md` + `_LANE_STATE.json` เดิม | ⬜ | สถานะ dep (BA เสร็จ) · artifacts เดิม (กัน ENH ทับ new) |
| 7 | `knowledge/TASTE_LOG.md` | ⬜ | ส่งต่อให้ S2/S3e ทาง brief (ไม่ copy เนื้อ — อ้าง path) |

ไม่มี #1 = หยุด ("ไม่มี feature ใน pool/checklist — สร้างด้วย `/wave plan` หรือเลือกในแผงก่อน")

## ขั้นตอน (รอบเดียวจบ — ไม่ถาม เว้นแต่ validation ตก)

### 1. Resolve feature
- หา entry ใน POOL/CHECKLIST (ชื่อไทย/EN/id ใดก็ได้) → ได้ module · wave · chips · dep · scope note
- ถ้ามี graph → map เป็น node id (ไม่มี node = แจ้งว่า "ไม่มีใน graph — จะใช้ PREBRIEF เป็น contract แทน" ไม่ block)

### 2. Validate (ตก = ไม่ออก brief · เขียนเหตุใน `_VALIDATION.md`)
| เช็ค | ผลถ้าปล่อยผ่าน |
|---|---|
| status ≠ done (ถ้า done → ถาม ENH หรือข้าม) | ทำซ้ำของจริง |
| `depends_on` ทุกตัว = done/ba-done (จาก POOL/registry/_LANE_STATE) | hook อ้างของที่ไม่มี → coverage BLOCK |
| baseline check: feature ไม่ใช่สิ่งที่ current-state §2 บอกว่า "มีแล้ว ห้าม re-implement" (DOA/NOTIFY/DOCCFG/Roles/OP/Planner) | สร้าง engine ซ้อน |
| OQ ที่ block feature นี้ (current-state §4 · scope note) มีคำตอบ หรือ business-critical? | ไม่มีคำตอบ + critical → Hard Stop · ไม่ critical → brief สั่ง `[ASSUMED]` |
| LOCK refs (LD/AC/OQ-G/มติ) ที่จะใส่ มีจริงใน knowledge/graph | LOCK ปลอม |
| archetype **ชั่วคราว** (Q-document / master / P-planner / J-dashboard / console / hybrid) — จาก chips + catalog + ชื่อ · S0.5 STANDARD_BASELINE จะยืนยัน/เปลี่ยน (Consent ที่ดูเหมือน master อาจต้องมี "สร้าง→ส่ง→เซ็น→PDF" = hybrid) | HTML ผิดโครง (#98) |

### 3. Derive (สกัด — ไม่แต่ง)
- **Scope รอบนี้**: จาก catalog description + scope note + (graph node summary) → "ทำ: … / hook ไป: …"
- **ไม่ทำรอบนี้**: ของ feature ปลายทาง + สิ่งที่ scope note ตัด + baseline ที่ต้องเรียกใช้แทนทำเอง — **ห้ามว่าง**
- **Archetype + reference**: Q → `html-generator-v9/patterns/Q_*` + `references/document-archetype/_SOURCE_so-reference.html` · P → planner refs · master → product-master ref · J → dashboard
- **Declarations ที่ต้องรัน (S1.8)** — จาก chips ตั้งต้น (S1.8 จะ detect ซ้ำจาก PREBRIEF · ต่างกัน = DIVERGENCE):
  | chip | skill | output |
  |---|---|---|
  | doa | `doa-declaration` | DOA_BRIEF |
  | ntf | `ntf-declaration` | NTF_BRIEF |
  | csq | `csq-declaration` | CSQ_BRIEF |
  | doccfg | `doccfg-declaration` | DOCCFG_BRIEF |
  | **pdfdoc** | **`thai-doc-pdf-generator`** | `template.html` + `sample.pdf` + `print-spec.md` (แนบ FRD · HTML tab PDF Preview ใช้ template เดียวกัน) — บังคับเมื่อ feature ออกเอกสาร/แบบฟอร์มทางการ (SO/PO/INV/CN/RV/ใบสำคัญ/หนังสือรับรอง/รายงานภาษี/payslip) |
- **LOCK/มติ**: ระบุ id เท่านั้น (ไม่ copy เนื้อ) — DOA iron rule · มติ 17 ส.ค. slot picker · LD-4C-02 · HR-1 · audit append-only · 7C ท่อต้องห้าม · + LD/AC/OQ-G จาก graph ถ้ามี
- **[ASSUMED] policy**: OQ ที่ไม่มีคำตอบและไม่ critical → list ไว้ให้ lane ใช้ default + tag
- **Context Preview** (FYI คนตรวจ): dep · edges (ถ้ามี graph) · artifacts เดิม · feature ข้างเคียงใน module

### 4. Generate
- `briefs/<W>/<F-code>/LANE_BRIEF.md` ตาม `templates/LANE_BRIEF.template.md` (v2) — ใน lane v2.3 ชื่อไฟล์ตายตัว `LANE_BRIEF.md` อยู่โฟลเดอร์ brief ของ feature (manual mode ใช้ `LANE_BRIEF_<id>.md` ได้)
- batch (`/wave plan W1` หรือ "บรีฟทั้ง wave"): 1 ไฟล์ต่อ feature เรียงตาม dep → `_VALIDATION.md` ตารางรวม (ผ่าน/ตก/เหตุ)
- สรุปท้ายแชท ≤10 บรรทัด: ออกกี่ใบ · ตกกี่ใบเพราะอะไร · DIVERGENCE/ASSUMED ที่ควรรู้

## กติกาเหล็ก
1. **Brief แบกเจตนา + ตัวชี้เท่านั้น** — ห้าม copy golden rules/มติ/spec ลง brief (อ้าง id + path ให้เลน slice สดเอง)
2. **ห้ามออก brief ให้ feature ที่ validate ตก**
3. **"ไม่ทำรอบนี้" ต้องมีเนื้อเสมอ** — รวม baseline ที่ต้อง "เรียกใช้ ไม่ทำเอง"
4. **archetype ต้องระบุ** — ไม่ชัดให้เลือก master + log เหตุ (เลน S1 ยืนยันซ้ำจาก PREBRIEF)
5. ระบุ `pool_version` / `plan_version` / `knowledge_version` ใน brief — runner เช็คคู่กัน
6. ลำดับตาม dep (BUILD_ORDER ถ้ามี · ไม่มีใช้ depends_on ใน POOL) — ข้ามได้ต้อง acknowledge

## Templates
- `templates/LANE_BRIEF.template.md` — v2 (เพิ่ม archetype · declarations+skills · scope note · ASSUMED · knowledge refs)

**Skill version: 2.0.0 (2026-08-25) — input จาก POOL/CHECKLIST + knowledge current-state · graph optional · declarations 5 ท่อ (+pdfdoc → thai-doc-pdf-generator)**
