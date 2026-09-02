---
name: feature-lane-runner
description: >
  Core orchestrator v2.3 ของ WF-01 (HTML-first lane) — รับ WAVE_CHECKLIST.md (เลือกจากแผง Feature Checklist /
  POOL.json) แล้ววิ่งจบทั้งเลนต่อ feature แบบ one-shot ไม่หยุดถามคน: S0 lane brief → S0.5 standard baseline (Odoo/D365/SAP → MUST) → S1 PREBRIEF (FN ledger)
  → S1.5 standard quick → S1.8 declare (doa/ntf/csq/doccfg/pdfdoc) → S2 html-generator-v9 → S3 gates
  (audit · qc-ux+render · qc-coverage R1) → S4 BRD → S5 FRD → S6 TC×3 → S6.5 coverage R2+R15 → S7 UI brief
  → S8 DevPack + REGISTRY_PATCH → S9 OP sync. auto-fix loop ตาม retry matrix · BLOCK ครบ cap → _BLOCKED.md
  ข้ามตัวถัดไป ไม่ล้ม batch · resumable (_RUN_STATE/_LANE_STATE) · จบ wave ออก REVIEW_SHEET.html
  ใช้เมื่อ user พูดถึง "feature-lane-runner", "รัน lane", "/wave run", "/wave plan", "/pool", "one-shot pipeline",
  "รัน WF-01 อัตโนมัติ", "รัน pipeline ไม่ต้องเฝ้า", "lane runner", "auto pipeline", "รันทั้ง wave"
---

# Feature Lane Runner v2.3 — POOL → CHECKLIST → RUN (one-shot · standard-first)

> **หลักการเดียว:** skill นี้ **orchestrate อย่างเดียว** — ไม่เขียน HTML/เอกสาร/กฎ QC เอง ทุก step เรียก skill เจ้าของงาน
> ความรู้ CUBE อยู่ที่ `cube-master-knowledge` · กฎ UI อยู่ที่ `html-generator-v9` · contract ของ feature อยู่ที่ PREBRIEF

## 0. Position

```
P1 แผง CUBE Feature Checklist / POOL.json ──▶ P2 เลือก ──▶ waves/<W>/CHECKLIST.md ──▶ P3 /wave check
                                                                                        │
   ┌──────────────────────────── feature-lane-runner v2.1 (ต่อ feature · context สด) ───┴────────────┐
   │ S0 brief → S0.5 baseline → S1 PREBRIEF → S1.5 std gap → S1.8 declare → S2 HTML v9 → S3 gates → S4 BRD → S5 FRD │
   │ → S6 TC → S6.5 coverage R2 → S7 UI brief → S8 finalize → S9 OP                                     │
   └───────────────────────────────────────────────────────────────────────────────────────────────┘
                                             ▼
                 waves/<W>/REVIEW_SHEET.html · _BLOCKED.md · DIVERGENCE.md · REGISTRY_PATCH.md  → คนดู 5 นาที
```

## 1. Workspace (v2.3 — แยก "brief/งานระหว่างทาง" ออกจาก "output ส่ง dev")

```
CUBE-LANE/
├─ .claude/skills/                 ← skill ทั้งเลน
├─ POOL.json                       ← แผง 140 features (+status)                          scripts/pool.py
├─ knowledge/                      ← TASTE_LOG.md · CONTEXT_PACK/<module>.md · FEATURE_REGISTRY.md · golden-shots/
├─ briefs/                         ← ★ ฝั่งอ่าน/ทำงาน (runner อ่าน-เขียน · ไม่ส่ง dev)
│   └─ W1/
│       ├─ CHECKLIST.md            ← คนติ๊ก + scope note (สร้างด้วย pool.py plan)
│       ├─ _RUN_STATE.json · REVIEW_SHEET.html · DIVERGENCE.md · BLOCKED.md · REGISTRY_PATCH.md   (ระดับ wave)
│       └─ F-MKT-CONSENT/          ← โฟลเดอร์ brief ต่อ feature
│           ├─ LANE_BRIEF.md · STANDARD_BASELINE.md · PREBRIEF.md · FUNCTION_CHECKLIST.md/.html · STANDARD_GAP.md
│           └─ _lane/  LANE_STATE.json · LANE_LOG.md · DECL.json · MANIFEST.json · OP_MANIFEST.json · REGISTRY_PATCH.md · _NOTIFY.md · [BLOCKED.md]
│                       QC/ (audit.txt · UX_CHECK_REPORT.md · COVERAGE_R1.md · COVERAGE_R2.md · RENDER.json · shots/) · TC_work/
└─ output/                         ← ★ ฝั่งส่ง dev (เฉพาะไฟล์ที่มีผลต่อการพัฒนา · zip โฟลเดอร์นี้ส่งได้เลย)
    └─ 2026-08-26/                 ← จัดกลุ่มตามวันที่รัน (หลาย feature ต่อวันอยู่ด้วยกัน)
        └─ F-MKT-CONSENT_ความยินยอมการติดต่อ/
            ├─ 1_HTML/             <ชื่อ>.html (+ template_<doc>.html ถ้ามี PDF)
            ├─ 2_BRD/              BRD_<ชื่อ>.md (+ .docx)
            ├─ 3_FRD/              FRD Pack 00–07 + INDEX · UI_BRIEF_<ชื่อ>.md · PRINT_SPEC.md
            ├─ 4_TC/               testcases_<ชื่อ>.md · <ชื่อไทย> HTML Testcase.html · AI_TESTSET_<ชื่อ>.md
            └─ 5_DECLARATIONS/     DOA_BRIEF · NTF_BRIEF · CSQ_BRIEF · DOCCFG_BRIEF · PDFDOC/ (เฉพาะท่อที่ need) + NOT_NEEDED.md
```
- **output/ ไม่มี:** PREBRIEF · FN checklist · baseline/gap · QC report · shots · state/log · manifest — ทั้งหมดอยู่ `briefs/` (trace ได้ แต่ไม่ปน dev pack)
- ชื่อโฟลเดอร์ output = `<F-code>_<ชื่อไทย>` · วันที่ = วันที่เริ่มรัน feature นั้น (`_lane/LANE_STATE.json.out_dir` เป็นตัวชี้)
- output เก่า (features/… v2.1.1 หรือ 10_HTML v2.1.0) → `python scripts/reorganize.py <feature_dir> --wave W1 --date 2026-08-26`

## 2. Commands

| คำสั่ง | ทำอะไร |
|---|---|
| `/pool` · `/pool ready` | `python scripts/pool.py summary` · `ready` = เฉพาะ dep เสร็จ |
| `/wave plan W1 [ชื่อ, ชื่อ …]` | `pool.py plan W1 [--names]` → gen `briefs/W1/CHECKLIST.md` (ติ๊ก ✔ ทั้ง wave · คนแก้ + ใส่ scope note) |
| `/wave check W1` | `pool.py check W1` → มีใน pool · dep เสร็จ · ไม่ซ้ำ lane · scope note มี OQ ค้าง? → PASS/FAIL |
| `/wave run W1 [--lane A] [--mode full\|html-only\|docs-only]` | รัน §3 ทุก feature ที่ ✔ (lane A/B/C = แบ่งขนาน 3 session) |
| `/wave resume W1` | อ่าน `_RUN_STATE.json` → ต่อจาก stage ล่าสุดที่ผ่าน |
| `/lane run <feature>` | 1 feature (dry-run) |
| `/wave review W1` | `review_sheet.py W1` gen ใหม่จาก state |

## 3. The Lane (11 steps) — รายละเอียด I/O ใน `references/lane-spec.md`

| # | Step | Skill | Output | Gate |
|---|---|---|---|---|
| S0 | INTAKE | `lane-brief-generator` v2 + `run_state.py init briefs/<W>/<F> "<ชื่อ>" <W> --out output/<date>/<F>_<ชื่อไทย>` | `briefs/<W>/<F>/LANE_BRIEF.md` | dep ไม่เสร็จ = **skip** · ไม่มี LOCK/OQ ref = Hard Stop |
| **S0.5** | **STANDARD BASELINE** | `feature-review-standard` **baseline mode** (Odoo · D365 · SAP → capability matrix · lifecycle · archetype · declarations) | `briefs/<W>/<F>/STANDARD_BASELINE.md` | MUST ≥ 5 · lifecycle มี state · archetype ระบุ · MUST ที่ scope note ตัด → OQ |
| S1 | PREBRIEF | `feature-prebrief` lane mode (ต้องครอบ MUST + lifecycle ของ S0.5) | `01_PREBRIEF.md` · `01_FUNCTION_CHECKLIST.md/.html` | ทุก S มี FN · ทุก FN มี trace · มี "ไม่รองรับ" |
| S1.5 | STANDARD | `feature-review-standard` quick | `briefs/<W>/<F>/STANDARD_GAP.md` → patch PREBRIEF [STD] | MUST merge · NICE → ไม่รองรับ |
| S1.8 | DECLARE | `scripts/decl_rule.py` → doa/ntf/csq/doccfg-declaration + `thai-doc-pdf-generator` (lane mode) | `_DECL.json` · `03_*_BRIEF.md` · `03_PDFDOC/` | NOT-NEEDED ต้องเขียน · chip≠detect → DIVERGENCE |
| S2 | HTML | `html-generator-v9` (archetype จาก PREBRIEF `archetype_confirmed` · input PREBRIEF+FN+03_*) | `output/<date>/<F>_<ชื่อ>/1_HTML/<ชื่อ>.html` | `node --check` · PREFLIGHT stamp |
| S3 | GATES | (a) `$GEN/scripts/audit.sh` → (b) `qc-ux-html-checker` **Pass G+D+R บังคับ** (shots · pageerror=0 · 1440+1024) → (c) `qc-coverage-checker` R1 (ตรวจไฟล์ใน `output/…` เขียน report ลง `briefs/<W>/<F>/_lane/QC/`) | `_lane/QC/` | FAIL=0 · BLOCK=0 · FN ✓/△ ครบ |
| S4 | BRD | `brd-generator-full` Lane Mode v2 (PREBRIEF+FN+03_*+HTML — ไม่มี RIF) | `output/…/2_BRD/BRD_<ชื่อ>.md` | Quality Gate APPROVED |
| S5 | FRD | `frd-generator-v6` Lane Mode v2 (sync read 03_* · manifest มี FN) | `output/…/3_FRD/` | Phase 3.5 A-M |
| S6 | TC | `ai-testcase-md-generator` (FN ledger) → `qa-friendly-html-generator` → `qa-html-to-ai-testset` | `output/…/4_TC/` testcases_<ชื่อ>.md · <ชื่อไทย> HTML Testcase.html · AI_TESTSET_<ชื่อ>.md | — |
| S6.5 | COVERAGE R2 | `qc-coverage-checker` R2 (+R15) | `_lane/QC/COVERAGE_R2.md` | FN↔TC · decl↔FRD · R15 |
| S7 | UI BRIEF | `html-ui-brief` | `output/…/3_FRD/UI_BRIEF_<ชื่อ>.md` | — |
| S8 | FINALIZE | `_lane/MANIFEST.json` (md5 ทุกไฟล์ · gates · decl) + `_lane/REGISTRY_PATCH.md` + `_lane/_NOTIFY.md` — **ไม่ zip** | — | — |
| S9 | OP SYNC | OP adapter (dry-run) | `_OP_MANIFEST.json` | — |

**ล็อกลำดับ:** S0.5 ก่อน S1 (baseline ตั้งโจทย์ก่อนเขียน scenario) · S1.5 ก่อน S1.8 ก่อน S2 (standard + declaration ต้องเข้า PREBRIEF ก่อนวาด) · S3 a→b→c · S7 หลังทุก gate (UI Brief สกัดจาก HTML สุดท้าย)
**Mode:** `html-only` = S0–S3 · `docs-only` = S4–S9 (ต้องมี S3 PASS ใน state)

## 4. Output — สองฝั่ง (ล็อก)

| ฝั่ง | path | ใส่อะไร | ใครใช้ |
|---|---|---|---|
| brief/งานระหว่างทาง | `briefs/<W>/<F>/` + `_lane/` | LANE_BRIEF · STANDARD_BASELINE · PREBRIEF · FN checklist · STANDARD_GAP · state/log/decl/manifest · QC reports+shots · TC_work | BA / runner / reviewer |
| dev pack | `output/<date>/<F>_<ชื่อ>/` | 1_HTML · 2_BRD · 3_FRD (+UI_BRIEF +PRINT_SPEC) · 4_TC · 5_DECLARATIONS | dev / QA — zip ส่งได้ทันที |

- S8 = เขียน `_lane/MANIFEST.json` (md5 ทุกไฟล์ทั้ง 2 ฝั่ง) + `_lane/REGISTRY_PATCH.md` + `_lane/_NOTIFY.md` · **ไม่ zip**
- gate ทุกตัวอ่านไฟล์จาก `output/` (ของจริง) แล้วเขียน report ลง `briefs/<W>/<F>/_lane/QC/`

## 5. Gate policy — one-shot (รายละเอียด `references/gate-policy.md`)

| Verdict | ทำ |
|---|---|
| PASS | ต่อ |
| WARN | log `_LANE_LOG.md` → ต่อ (auto-fix 1 ครั้งถ้า cosmetic) |
| BLOCK | fix loop ตาม retry matrix · **ฉีด report รอบก่อนเข้า fixer เสมอ** · รัน gate ซ้ำหลังแก้ |

Retry matrix: S1 ×2 · S3a ×3 · S3b (qc-ux fix mode) ×3 · S3c (patch FN/hook) ×2 · S4 ×2 · S5 ×2 · S6.5 ×2 · **cap รวม 10/feature** · issue เดิมซ้ำ 2 รอบ = หยุดวน → `_BLOCKED.md` → feature ถัดไป

**Hard Stop (ห้าม auto-fix):** scope drift vs LOCK/มติ · ไม่มี LOCK/OQ ref ใน brief · OQ business-critical ไม่มีคำตอบ · governance invariant พัง (DOA hardcode / hard delete / effective_date หาย / 7C ท่อต้องห้าม) · S1.8 declaration ที่ need แต่ generate ไม่ได้
**Default policy:** ไม่ชัด → default ตาม gap-detection + `[ASSUMED]` (PREBRIEF §OQ · BRD §OQ) + ขึ้น REVIEW_SHEET — **ห้ามถาม**

## 6. Context discipline (กันบวม/รั่ว)

1. 1 feature = 1 sub-context (Cowork subtask) — ส่งเข้าไปแค่ LANE_BRIEF + path ของ knowledge · ห้ามพก output feature อื่น
2. HTML ที่ gen แล้ว **ไม่อ่านกลับเข้า context** — ตรวจด้วย audit/qc scripts เท่านั้น · `_shots/*.png` ดูภาพได้ · `shots_b64.json` ห้ามอ่าน
3. ทุก step เขียน `briefs/<W>/<F>/_lane/LANE_STATE.json` ทันที (`scripts/run_state.py set briefs/<W>/<F> <stage> <status>`) · `briefs/<W>/_RUN_STATE.json` ระดับ wave
4. ขนาน = `--lane A/B/C` คนละ session · feature ไม่ซ้ำ lane (`/wave check` กัน)

## 7. Rules / Anti-patterns

✅ อ่าน `cube-master-knowledge` (current-state + catalog §0) + `references/lane-spec.md` ก่อนทุก run · ✅ เรียก skill เจ้าของงานเสมอ · ✅ ทุก gate รันจริง (NOT-CHECKED = BLOCK) · ✅ log ทุก fix round · ✅ LOCK/มติ ไหล brief → PREBRIEF → BRD → FRD ครบ
❌ หยุดถามกลางเลน · ❌ ข้าม gate · ❌ แก้กฎ/knowledge/LOCK เอง · ❌ ล้ม batch เพราะ 1 feature · ❌ แขวน DevPack ทั้งที่ BLOCK · ❌ re-implement baseline (DOA/NOTIFY/DOCCFG/Roles/OP) — ประกาศเท่านั้น

## 8. Files
- `references/lane-spec.md` — I/O ต่อ step (อ่านก่อนรัน) · `references/gate-policy.md` · `references/cowork-commands.md` (prompt พร้อม paste) · `references/op-adapter-contract.md`
- `scripts/pool.py` · `scripts/decl_rule.py` · `scripts/run_state.py` (init ต้องระบุ `--out output/<date>/<F>_<ชื่อ>`) · `scripts/review_sheet.py` · `scripts/reorganize.py` (แปลง output เก่า → v2.3)
- `templates/CHECKLIST.template.md` · `_LANE_STATE.template.json` · `_RUN_STATE.template.json` · `_MANIFEST.template.json` · `REGISTRY_PATCH.template.md` · `op-binding.template.json`
- `_v0.3_archive/` — เวอร์ชันเดิม (RIF-first · v6) เก็บอ้างอิง

**Skill version: 2.3.0 (2026-08-26) — workspace แยก `briefs/` (งาน) กับ `output/<date>/` (dev pack เฉพาะไฟล์มีผลต่อการพัฒนา)** · 2.2.0 (2026-08-25) — เพิ่ม S0.5 STANDARD BASELINE (Odoo/D365/SAP capability matrix → MUST/lifecycle/archetype ก่อน PREBRIEF)** · 2.1.1 — โครง output ใหม่ 0_SOURCE/1_HTML/2_BRD/3_FRD/4_TC/_lane · ไม่ zip · decl_rule §12-authoritative** · 2.1.0 — POOL/CHECKLIST intake · PREBRIEF-first · 5 declarations · html-generator-v9 · gate 3 ตัว · ตัด RIF/taste/drift/output-checker/NF-SO ออกจากเลน**
