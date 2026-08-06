# PIPELINE_STATUS — 11_Warehouse (F-LOCATION-MASTER-001 · คลังและตำแหน่ง / Warehouse & Bin)

> Snapshot สถานะ WF-01 · อัปเดต 2026-08-07 · **PIPELINE COMPLETE (steps 1-9)** — ส่งมอบที่ `_final-docs/` · ใช้กู้ context หลัง compact/session ใหม่
> Source of truth = ไฟล์ใน `00_CONTEXT/` (DECISION_LOG D1-D14, AI_DEFAULTS AD-1..9, COVERAGE_MAP) + HTML

## ✅ เสร็จแล้ว (steps 1-4 + gate work)
| Step | Skill | ผล | ไฟล์ |
|---|---|---|---|
| 1 | html-generator-v7 | ✅ | `01_HTML/WarehouseBin.html` (207KB) |
| 2 | thai-doc-pdf | ⏭️ SKIP (D2) | — |
| 3 | qc-ux-html-checker | 🟢 PASS (iter 3, หลังแก้ + tree) | `02_QC/WarehouseBin_UX_CHECK_REPORT.md` |
| 4 | qc-coverage-checker | 🟢 PASS 51/51 | `02_QC/WarehouseBin_COVERAGE_REPORT.md` |

**HTML สถานะปัจจุบัน = final candidate:** 6 จอ + **dual-view (List + Hierarchy tree)** · branch picker + geo cascade · role switcher (align กับปุ่มสร้าง, prototype-only) · node soft-archive (GC#7) · reparent stock guard · CUBE Warm Light off-palette hex=0 · display "คลังและตำแหน่ง (Warehouse & Bin)" · latent bug 2 ตัว (drawer re-render + in-drawer modal z-index) verified CLEAN

## ✅ E2E 2 รอบ — รันแล้ว PASS (2026-08-06)
- รัน `02_QC/e2e_2rounds_warehouse.py` ด้วย venv Playwright เสร็จ → **VERDICT: PASS**
- **213/213 assertions · 0 fail · 0 console error · 0 page error** · ทั้ง 2 รอบเขียวครบทุก viewport (1280/1440/1920)
  - Round 1 (Happy + dual-view): 30 assertions × 3vw = 90 ✅
  - Round 2 (negative/guards/RBAC/state/robustness): 41 × 3vw = 123 ✅
- Output: `02_QC/E2E_2_ROUNDS_REPORT.md` + `02_QC/E2E_2_ROUNDS_RESULT.json` + `02_QC/e2e_shots/` (159 shots)
- latent bug 2 ตัว + Esc chain 3-tier = CLEAN · UX-06/07/08 = by-design note carry ลง FRD/UI-brief
- **ถัดไป: user ทดสอบมือเอง** → ถ้าผ่าน เปิด gate เข้า step 5 (brd-generator-full)

## 🔧 รอบแก้หลัง PM/BA review (D15 + manual-QA) — HTML เปลี่ยนหลัง E2E
ทำหลัง E2E PASS · เป็น text/CSS/label ล้วน ไม่แตะ logic · verify เฉพาะจุดที่แตะ (0 page error):
- barcode copy 3 จุด → ภาษาคน (ตัด `loc_require_barcode` ออกจาก UI) · shots `02_QC/fix_verify_loc_view.png`
- location view: แถบ tab (ภาพรวม/ความจุ/ประวัติ) ชิดขอบ align หัวข้อ (24px, negative margin) · `fix_verify_loc_tabs.png`
- **D15:** ถอด role switcher · breadcrumb & Full Path: **ตัด branch ออก** + code→ชื่อ (zone/area/rack; WH+location คง code) · "Location"→"ตำแหน่ง" ทุกจุด · order W→Z→A→R→L verified ครบ · reverse D7 (branch ใน path) · branch ยังอยู่ใน field คลัง + คอลัมน์ List · shots `fix_verify_breadcrumb.png` / `fix_verify_order.png`
- ⚠️ **ถ้าจะรัน E2E ซ้ำ:** สคริปต์ `e2e_2rounds_warehouse.py` มีเทสต์ที่อิง role switcher (RBAC switch + "D13 role switcher aligned") — จะ FAIL เพราะถอดออกแล้ว · ต้องแก้สคริปต์ให้ set `state.role` ตรงแทนการกด switcher ก่อนรัน (ยังไม่ทำ — รอ user สั่ง)

## ✅ step 5-6 เสร็จ (2026-08-07) · manual test ผ่าน → เปิด gate แล้ว
- **5. BRD** ✅ `03_BRD/BRD_Warehouse_Bin.md` (44KB, APPROVED, 18 sections) · gen ~134k token
  - ⚠️ `.docx` ไม่ได้ gen (skill md_to_docx.py path Linux ไม่มีบน Windows) — `.md` ครบ, ทำ docx ทีหลังได้
- **6. FRD** ✅ `04_FRD/FRD_F-LOCATION-MASTER-001_Pack/` (FULL 9 ไฟล์ 84KB) · gen ~142k token
  - FN 18 (17 active + WHB-FN-18 deferred) · API 18 · Engine 2 (HIER-PATH, BULK-PLAN) · EC 18 · LD 13 (+7 Scope Lock) · BR 18 · errors 17 · stories 10
  - D15 reflect: full_path branch-excluded + code/name mix (ENG-HIER-PATH) · role switcher = dead-code LD-04/LD-10 · SPA no-hash-route = LD-08 · trace ครบกับ BRD Scope Lock

## ✅ step 7-9 เสร็จ (2026-08-07, รันหลัง user เปลี่ยน account token เหลือเฟือ) — PIPELINE COMPLETE 🎉
- **7. UI Brief** ✅ `05_UI_BRIEF/UI_BRIEF_F-LOCATION-MASTER-001.md` (37.5KB) · 13/13 sections · 8 screens+2 views+3 modal · overlay registry 6 · z-index 7+3 · microcopy ~16 toast · trace 12 rows · **Drift Log 8 (ZERO business drift)** — role switcher ยืนยันหายจาก renderHeader, logged dead .role-switch/setRole/base-kit hash router, path builder verified no-branch
- **8. Testcases** ✅ `06_TESTCASES/testcases-F-LOCATION-MASTER-001.md` (107KB) + `.zip` · **70 TC** (happy 24/negative 20/edge 8/permission 9/XT 4/Scope-Lock 5) · trace FR 13/13 · BR 17/18 · EC 15/18 · errors 17/17 · perm 15/15 · XT 4/4 · LOCK 7/7 · stories 10/10 · RBAC via console setRole (ไม่ใช้ switcher) · 3 skips documented (BR-018/EC-14/EC-15)
- **9. UAT** ✅ `07_UAT/testcase-warehouse-bin.html` (2.7MB self-contained) · 70/70 TC rendered · 197 steps 1:1 (R15 PASS) · 196/197 มี screenshot จริง (Playwright 17 regions) · 40 data-sample buttons · lightbox + export PDF · XT 4 = sys case (นับ pass 66/70) · 0 console error
- **รวมเล่ม** ✅ `_final-docs/` — prototype + BRD + FRD pack + UI brief + testcases + UAT + README index
- 💰 ต้นทุนจริง step 7-9 ≈ 178k / 178k / 210k token

## 3 INFO จาก qc-ux (dev-handoff note, ไม่ block, carry ลง FRD/UI-brief)
- UX-06: drill/tree position อยู่ใน memory — refresh กลับ root (ไม่มี spec บังคับ hash-encode)
- UX-07: role switcher = demo affordance (dev ลบตอน prod) · label "Warm Light" เป็นชื่อ theme
- UX-08: tree row ยังไม่มี keyboard/arrow-key nav (toggle + switcher เป็น real button แล้ว)

## วิธีทำงาน (convention)
- รัน heavy skill ผ่าน general-purpose agent + verify ไฟล์เขียนจริง · user gate ทุก step
- แก้ legacy = ห้าม (regenerate HTML-first) · legacy อยู่ `00_CONTEXT/_legacy/`
