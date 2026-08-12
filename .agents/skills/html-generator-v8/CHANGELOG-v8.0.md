# CHANGELOG — html-generator-v8.0 (2026-08-09)

## Consolidated release — แทน html-generator-v7 (รวม v7.1 field feedback เป็น major)

### กฎใหม่ (จาก field feedback รอบ 2026-08-09)
- **#95 Overlay Portal (BREAKING)** — root cause "dropdown จม" = ancestor overflow clip
  ไม่ใช่ z-index → เมนูใน scroll container (.table-wrap / drawer body / B2 line grid)
  ต้อง `portalMenu(trigger, menu)` ไป `#overlay-root` (position:fixed + flip-up + maxHeight
  + reposition on scroll/resize). util + `.menu-fixed` อยู่ใน skeleton BASE-KIT แล้ว
- **#94.1 Cascade Clear** — clear master combobox → field ที่ autofill ตามต้องเคลียร์ครบชุด
  + confirm ก่อนล้าง line items ที่ผูกกับค่านั้น
- **#96 List Full-Height** — `.page-fill` + card flex:1 + `.table-wrap` scroll ภายใน
  + thead sticky + `.table-foot` ติดล่าง — ตารางยืดชิดขอบล่าง viewport ทุกขนาดจอ
- **#97 Responsive Desktop-Base (BREAKING — แทน doctrine desktop-only)** —
  ≥1180 เต็มรูปแบบ · 768–1180 adaptive (sidebar off-canvas generic / icon rail Pattern N,
  drawer ทุกขนาด = min(กว้างเดิม,100vw), content padding 16) · <768 horizontal scroll
  ไม่ guarantee · `body min-width: 768px` · Render Gate เพิ่ม viewport 1024px
- **#67.1 Hint Opt-in Only** — default ไม่ gen hint/ⓘ ใด ๆ — มีได้เฉพาะ FRD ระบุ explicit
  (error / validation / destructive warn / empty state คงไว้ — ไม่ใช่ hint)
- **#47.1 Stepper Geometry Lock** — step กว้างเท่ากันเป๊ะ (flex:1 1 0), connector กึ่งกลาง
  dot, dot ขนาดเดียวทั้งแถบ, CSS จาก kit verbatim, Render Gate วัด alignment จริง

### Skeleton (templates/file-skeleton.template.html)
- `body min-width: 1180px` → `768px` + `@media (max-width:1180px)` block
  (drawer min(…,100vw) / sidebar off-canvas + `.nav-toggle` / content padding 16)
- CSS ใหม่: `.page-fill` / `.table-wrap` full-height + sticky thead / `.table-foot` /
  `.menu-fixed`
- BASE-KIT UTILS: เพิ่ม `portalMenu()` (ทำงานร่วม `[data-overlay]` + global outside-click เดิม)

### เอกสาร sync
- erp-design-guide + Rule #30 rationale: desktop-only → desktop-base (#97)
- Self-check เพิ่มข้อ 20–24 (component-contracts)
- SKILL.md Checklist F: min-width 768 + viewport 1024 + `.page-fill`

### Lineage
html-generator-25 → v3.x → v4.x → v6 → v7 (+v7.1) → **v8.0**
