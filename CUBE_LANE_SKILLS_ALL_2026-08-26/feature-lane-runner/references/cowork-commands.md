# Cowork / Claude Code — prompt พร้อม paste (v2.1)

## Setup ครั้งเดียว
```
โฟลเดอร์งาน: CUBE-LANE/  (โครงตาม feature-lane-runner SKILL.md §1)
- POOL.json ← BACKLOG_7C.json
- knowledge/ ← GOLDEN_RULES.md · FEATURE_REGISTRY.md · TASTE_LOG.md · CONTEXT_PACK/*.md
- skills ที่ต้องมี: feature-lane-runner lane-brief-generator feature-prebrief feature-review-standard
  doa-declaration ntf-declaration csq-declaration doccfg-declaration thai-doc-pdf-generator html-generator-v9
  qc-ux-html-checker qc-coverage-checker brd-generator-full frd-generator-v6 ai-testcase-md-generator
  qa-friendly-html-generator qa-html-to-ai-testset html-ui-brief cube-master-knowledge
```

## วางแผน wave
```
/wave plan W1
→ อ่าน POOL.json · gen briefs/W1/CHECKLIST.md (ทุก feature W1 ที่ dep พร้อม ✔ ไว้) · ผมจะแก้ ✔ และใส่ scope note เอง
```
```
/wave check W1
→ validate checklist: มีใน pool · dep เสร็จ · ไม่ซ้ำ lane · OQ critical ไม่มีคำตอบ → บอก · ผ่านค่อยรัน
```

## รัน 1 feature (dry-run)
```
รัน feature-lane-runner v2.1: /lane run "หนังสือรับรอง"
- workspace CUBE-LANE/ · ใช้ briefs/W1/CHECKLIST.md แถว "หนังสือรับรอง"
- อ่าน .claude/skills/feature-lane-runner/references/lane-spec.md + gate-policy.md ก่อน
- วิ่ง S0→S9 ต่อเนื่อง ห้ามหยุดถาม ยกเว้น Hard Stop 5 ข้อ · ไม่ชัด = default table + [ASSUMED]
- HTML ที่ gen แล้วห้ามอ่านกลับเข้า context — ตรวจด้วย audit/qc scripts เท่านั้น
- เริ่ม: python scripts/run_state.py init briefs/W1/<F> "<ชื่อ>" W1 --out output/<วันนี้>/<F>_<ชื่อไทย> · ทุก step: run_state.py set briefs/W1/<F> <stage> <status>
- จบ: python scripts/run_state.py wave briefs/W1 && python scripts/review_sheet.py W1 แล้วสรุป 10 บรรทัด (verdict/stage · fix rounds · ASSUMED · DIVERGENCE)
```

## รันทั้ง wave (ขนาน 3 session)
```
/wave run W1 --lane A      ← session 1
/wave run W1 --lane B      ← session 2
/wave run W1 --lane C      ← session 3
- 1 feature = 1 subtask context สด · feature blocked → _BLOCKED.md แล้วไปตัวถัดไป
- session สุดท้ายที่จบ: /wave review W1
```

## Resume
```
/wave resume W1
- อ่าน briefs/W1/_RUN_STATE.json + briefs/W1/*/_lane/LANE_STATE.json · ต่อจาก stage ล่าสุดที่ status=pass · ห้ามรัน step ที่ผ่านแล้วซ้ำ
```
