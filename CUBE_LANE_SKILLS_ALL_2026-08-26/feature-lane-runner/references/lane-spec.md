# Lane Spec v2.1 — I/O ต่อ step (อ่านก่อนรันทุกครั้ง)

`$GEN` = `ls -d /mnt/skills/user/html-generator-v* | sort -V | tail -1` · **`$B` = `briefs/<W>/<F-code>/`** (งาน) · **`$O` = `output/<date>/<F-code>_<ชื่อไทย>/`** (dev pack) · `$Q` = `$B/_lane/QC/`

| Step | เรียก | Input (path) | Output (path) | ผ่านเมื่อ | ตกแล้ว |
|---|---|---|---|---|---|
| S0 | `lane-brief-generator` | แถว CHECKLIST + POOL.json + cube-master-knowledge current-state/catalog + knowledge/CONTEXT_PACK/<module>.md + GRAPH (opt) | `$B/LANE_BRIEF.md` · `$B/_VALIDATION.md` | validation ทุกข้อผ่าน · archetype ระบุ | dep ไม่เสร็จ → `state=skipped` · LOCK/OQ critical → `_BLOCKED.md` |
| S0.5 | `feature-review-standard` (baseline mode) | `$B/LANE_BRIEF.md` + current-state §2 · web search Odoo/D365/SAP ≤6 | `$B/STANDARD_BASELINE.md` (matrix · lifecycle · archetype · declarations · OQ จาก MUST ที่ถูกตัด) | MUST ≥5 · lifecycle มี ≥3 state · archetype ระบุ | ×1 → ต่อด้วย WARN (ห้ามข้ามเงียบ) |
| S1 | `feature-prebrief` (lane mode · ครอบ MUST/lifecycle ของ S0.5) | `00_LANE_BRIEF.md` + knowledge | `$B/PREBRIEF.md` (หัวมี `archetype_confirmed:` · §12 signals) · `$B/FUNCTION_CHECKLIST.md` · `.html` | STEP 5 gate ของ skill · `prebrief_checklist.py` → `scenarios_without_fn=[]` · `fn_without_trace=[]` · not_supported ≥1 | วนแก้ ×2 → BLOCK |
| S1.5 | `feature-review-standard` (quick) | `01_PREBRIEF.md` + FN + archetype | `$B/STANDARD_GAP.md` → runner patch PREBRIEF (MUST auto · SHOULD +[AI-DRAFT] · NICE → ไม่รองรับ+OQ) | ไฟล์มี (หรือ `SKIPPED: reason`) | ข้าม (WARN) |
| S1.8 | `scripts/decl_rule.py $F` → declaration skills | `01_PREBRIEF.md` §12 + `00_LANE_BRIEF.md` chips | `$B/_lane/DECL.json` · **`$O/5_DECLARATIONS/`** = `DOA_BRIEF.md` / `NTF_BRIEF.md` / `CSQ_BRIEF.md` / `DOCCFG_BRIEF.md` / `PDFDOC/{template.html,sample.pdf,print-spec.md}` (เฉพาะ need) + `NOT_NEEDED.md` | ทุกท่อมีไฟล์ · Quality Gate ของ skill ผ่าน | ท่อ need แต่ gen ไม่ได้ = Hard Stop |
| S2 | `html-generator-v9` (Pipeline Mode · PREBRIEF-as-pack) | `01_PREBRIEF.md` + `01_FUNCTION_CHECKLIST.md` + `03_*` + `knowledge/TASTE_LOG.md` (opt) · archetype → Pattern Q/P/master/J | `$O/1_HTML/<ชื่อ>.html` (+ PREFLIGHT stamp) · Coverage Map → `$B/_lane/COVERAGE_MAP.md` · template PDF copy ไว้ `1_HTML/` | `node --check` ผ่าน · stamp มี | regen ×1 |
| S3a | `bash $GEN/scripts/audit.sh $O/1_HTML/*.html` | html | `$Q/audit.txt` | FAIL=0 | patch ×3 |
| S3b | `qc-ux-html-checker` (Pass G+D+R บังคับ · loop mode) | html + report รอบก่อน | `$Q/UX_CHECK_REPORT.md` · `$Q/shots/` · `$Q/RENDER.json` (render_shots.py ต้องรัน) (routes/drawers/tabs เดิน · pageerror) | BLOCK=0 · pageerror=0 · shots ≥1/route | fix mode ×3 |
| S3c | `qc-coverage-checker` R1 | html + PREBRIEF + FN + `_DECL.json` + 03_* (+GRAPH) | `$Q/COVERAGE_R1.md` | BLOCK=0 · FN ทุกข้อ ✓/△ · DECL-* ✓/NA · SURFACE-* (Q) ✓ | patch html เฉพาะ FN/hook ×2 → S3a |
| S4 | `brd-generator-full` (Lane Mode v2) | PREBRIEF + FN + 03_* + html + LANE_BRIEF | `$O/2_BRD/BRD_<ชื่อ>.md` (+.docx) | Quality Gate C01-C23 APPROVED · §14.6 = "ไม่รองรับ" | ×2 |
| S5 | `frd-generator-v6` (Lane Mode v2) | BRD + html + PREBRIEF + FN + 03_* + print-spec | `$O/3_FRD/` (00_OVERVIEW…07_LOCKED · INDEX) + `$O/3_FRD/PRINT_SPEC.md` (pdfdoc) | Phase 3.5 A-M · manifest มี FN ครบ · event ⊆ brief | ×2 |
| S6 | `ai-testcase-md-generator` → `qa-friendly-html-generator` → `qa-html-to-ai-testset` | FRD + html + FN | `$O/4_TC/testcases_<ชื่อ>.md` · `$O/4_TC/<ชื่อไทย> HTML Testcase.html` · `$O/4_TC/AI_TESTSET_<ชื่อ>.md` · ไฟล์ทำงาน (cases.json · shot-spec · shots_b64 · _qa_shots) → `$B/_lane/TC_work/` | Coverage Audit `FN cross-check ✅` | regen ตามไฟล์ที่ตก |
| S6.5 | `qc-coverage-checker` R2 | FRD + TC×3 + 03_* + FN | `$Q/COVERAGE_R2.md` (มี R15 table) | BLOCK=0 · R15 case/step ตรง 3 ไฟล์ | ×2 |
| S7 | `html-ui-brief` | html สุดท้าย + FRD | `$O/3_FRD/UI_BRIEF_<ชื่อ>.md` (Drift Log) — **อยู่ใน 3_FRD เสมอ** | ไฟล์มี | — |
| S8 | runner | `$B` + `$O` | `$B/_lane/MANIFEST.json` (md5 ทั้ง 2 ฝั่ง · gates · decl · out_dir) · `$B/_lane/REGISTRY_PATCH.md` · `$B/_lane/_NOTIFY.md` — ไม่ zip · ตรวจว่า `$O` ไม่มีไฟล์นอก 5 หมวด | — | — |
| S9 | OP adapter | `$B/_lane/MANIFEST.json` + `op-binding.json` | `$B/_lane/OP_MANIFEST.json` | dry-run ok | — |

**ไม่มี DevPack.zip** — คน zip `output/<date>/<F>_<ชื่อ>/` ส่ง dev ได้ทันที (ไม่มีอะไรต้องตัด)

**REGISTRY_PATCH.md:** บรรทัดสำหรับ FEATURE_REGISTRY (feature · BA status · artifacts · contracts/engine candidates ใหม่) — คน paste เอง (Claude เขียน project file ไม่ได้)
**_NOTIFY.md:** ข้อความสั้นให้ พี่เบิร์ด (อัพ Google Sheet H·F·Q) · Architect (engine candidates จาก FRD §3.2) · Strike (DIVERGENCE / ASSUMED ที่ต้องเคาะ)
