# CHANGELOG v6.0 — Consolidated Release (2026-07-09)

**html-generator-v6** = skill ตัวเดียวที่รวม 3 งานเข้าด้วยกัน แทนที่ html-generator-v4:

1. **Base เดิมจาก v4.0** — patterns A-M, Iron Rules #1-#48, Unified Drawer v2 (920/680),
   Fixed Tokens (--fs/--sp/--r), microcopy.md, Pipeline/Standalone mode, One-Shot Policy, audit.sh
2. **CUBE CI Rebrand (เดิม v4.1)** — Warm Light theme: Ivory `#FAF8F5` / White cards /
   Charcoal `#111111` / Red `#FF3B30` (action) / Orange `#FF9A1F` (connection) /
   Satoshi + Noto Sans Thai — ชื่อ CSS var คงเดิม (--c-navy=Charcoal, --c-primary=Red, --c-teal=Orange)
   ดูตาราง mapping เต็มใน CHANGELOG-v4.1-cube-rebrand.md
3. **Pattern N + Rule #49 (เดิม v4.2)** — Sidebar Navigation Shell 3 ระดับ + icon rail + slide panel
   (`patterns/N_sidebar-nav-shell.md` + `references/sidebar-shell/`) และ Minimal Scrollbar
   (5px, track โปร่งใส, ขาวโปร่งบนพื้นเข้ม) — ดู CHANGELOG-v4.2-sidebar-shell.md

**การเปลี่ยนชื่อ:** ทุก self-reference ใน skill ชี้ที่ html-generator-v6 แล้ว ·
Pipeline Mode รับ "FRD Pack (v4-v6)" (ชื่อกลาง ไม่ผูก version เดียว) ·
html-generator-v4 ถูก mark DEPRECATED ชี้มาที่ v6

**Chain:** brd-generator-full v2.1 → frd-generator-v6 → **html-generator-v6** + ai-testcase-md-generator
