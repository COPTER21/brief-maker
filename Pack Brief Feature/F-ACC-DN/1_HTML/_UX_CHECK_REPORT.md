# _UX_CHECK_REPORT — F-ACC-DN_debit-note.html (qc-ux-html-checker · lane)
> Sync Read html-generator-v9 SKILL.md (md5 5ad76e6e · อ่านใหม่สำหรับ feature นี้ 2026-09-20) · **Verdict: WARN (BLOCK 0)**
| ตรวจ | ผล |
|---|---|
| audit.sh v9 | FAIL 0 · WARN 2 (font-size px canonical · stepper-item) |
| wizard steps | เลือกแหล่งที่มา › ข้อมูลหลักใบลดหนี้ › รายการสินค้า › เอกสารแนบ › ตรวจสอบและยืนยัน ✓ |
| view tabs | รายละเอียด › ใบตั้งหนี้อ้างอิง·ภาษีซื้อ › PDF › ลายเซ็น › ประวัติ ✓ · เอกสารแนบใน รายละเอียด ✓ |
| DOA | submit modal `.slot-row` เลือกคน · resolveDoa 3 ช่วงตามมูลค่า (DOA_BRIEF) · ไม่มี chain hardcode ✓ |
| static | emoji 0 · localStorage ไม่มี · TODO 0 |
| **#67.1** | ✅ ไม่มี info/hint · เหลือ hard-warn "ยอดลดหนี้เกินยอดคงเหลือ" + field-error + note.danger ยกเลิก — ตรง PREBRIEF §6 · tile ลดลอย = ตัวเลือก disabled + pill ปิดไว้ |
| **#104** | ✅ view เดียว · stat 4 · ขวาบน = CSV + สร้าง |
| **#105** | ✅ `[data-demo="persona-switch"]` + DEMO · `[data-demo="pv-simulate"]` + DEMO (พิสูจน์ S-11) |
| **#106** | ✅ `.toolbar > .search-box` + select 170–220px ×3 + ล้างตัวกรอง |
| Heuristic (Playwright) | toast/Esc/loading "กำลังส่ง…"/destructive ผ่าน modal+เหตุผล ✓ · 1024 no h-scroll ✓ |
WARN ไหลต่อ: W-1..4 สืบทอด canonical (inline 233 < SO 341 · hex/stopProp/tabs = canonical)
