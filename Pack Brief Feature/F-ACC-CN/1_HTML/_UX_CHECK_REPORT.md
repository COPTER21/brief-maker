# _UX_CHECK_REPORT — F-ACC-CN_credit-note.html (qc-ux-html-checker · lane)
> Sync Read html-generator-v9 SKILL.md (md5 5ad76e6e · อ่านใหม่สำหรับ feature นี้ 2026-09-20) · **Verdict: WARN (BLOCK 0)**
| ตรวจ | ผล |
|---|---|
| audit.sh v9 | FAIL 0 · WARN 2 (font-size px canonical · stepper-item) |
| wizard steps | เลือกแหล่งที่มา › ข้อมูลหลัก › รายการสินค้า › เอกสารแนบ › ตรวจสอบและยืนยัน ✓ |
| view tabs | detail › ref (ใบแจ้งหนี้อ้างอิง · ภาษีขาย) › pdf › sign › history ✓ · เอกสารแนบใน detail ✓ |
| DOA | submit modal `.slot-row` เลือกคน (emp-av + ตำแหน่ง·แผนก + ชื่อ) · resolveDoa ตามมูลค่า 3 tier (mock ตาม DOA_BRIEF) · ไม่มี chain hardcode ✓ |
| static | emoji 0 · select_big 0 · td_multi_pill 0 · localStorage ไม่มี |
| **#67.1** | ✅ ไม่มี info/hint · เหลือ hard-warn ยอดเกินคงเหลือ + note.danger ยกเลิก (explicit PREBRIEF §6) · tile "ลดหนี้ไม่อ้างใบ" = ตัวเลือก disabled พร้อม pill ปิดไว้ (ไม่ใช่ banner) |
| **#104** | ✅ view เดียว · stat card กรอง · ขวาบน = CSV + สร้าง |
| **#105** | ✅ `[data-demo="persona-switch"]` + DEMO · `[data-demo="rv-simulate"]` + DEMO (ทดสอบ S-11) |
| **#106** | ✅ `.toolbar > .search-box` + select 170–200px + ล้างตัวกรอง |
| Heuristic (Playwright) | empty/Esc/loading "กำลังบันทึก…"/toast หลังปิด/destructive ผ่าน modal+เหตุผล ✓ · 1024 no h-scroll ✓ |
WARN ไหลต่อ: W-1..4 สืบทอด canonical (inline 234 < SO 341 · hex/stopProp/tabs = canonical)
