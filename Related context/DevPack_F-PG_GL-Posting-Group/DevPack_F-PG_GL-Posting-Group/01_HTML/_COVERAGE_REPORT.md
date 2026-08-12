# Coverage Report — F-PG GL Posting Group (รอบ 1: HTML) — Iteration 2 (LOOP)
- วันที่ 2026-08-10 · contract baseline: PREBRIEF_F-PG_GL-Posting-Group.md + FUNCTION_CHECKLIST_F-PG_GL-Posting-Group.md (ไม่มี workflow_graph.json/NODE_BRIEF สำหรับ feature นี้ — เหมือนรอบก่อน)
- Artifact ที่ตรวจ: f-postgrp.html (fix pass หลังรอบ 1: (1) ตัด CSV import Replace/Merge mode step ออกทั้งหมด กลับสู่ merge-only add (2) เพิ่ม block+toast ใน `submitSetup()` เมื่อแก้ bus/prod ของ record ที่ used>0 (3) เพิ่ม lock-tag แสดงผลบน code (tab1) / bus·prod (tab2) เมื่อ used>0)
- Checklist จาก contract: S-01..S-10 (10) · BR-01..BR-08 (8) · FN-01..FN-23 + FN-40 + FN-90 · Edges §9 (6) · Mock Data Spec §8

## Verdict: 🟢 PASS
สรุป: ครอบ 34/34 item ที่ตรวจได้ · gap block 0 · gap warn 0 · N/A-UI (ตามควร) 4 · NOT-CHECKED 0

ทั้ง 3 gap จากรอบ 1 (GAP-01 BLOCK, GAP-02/GAP-03 WARN) ปิดครบ ตรวจแล้วไม่มี regression ใหม่ในส่วนอื่นของ matrix

## Coverage Matrix

| Item | ประเภท | HTML | Evidence / หมายเหตุ |
|---|---|---|---|
| S-01 สร้าง tab1 (kind→ชุดช่องบัญชีเปลี่ยนตาม) | scenario | ✓ | `renderGroupForm()` L1171-1189 สลับ `acctFields` ตาม `f.kind` (ไม่เปลี่ยนจากรอบก่อน) |
| BR-01/R01/R02 บัญชี=COA leaf+ตรงประเภท | rule (block) | ✓ | `acctSelect()` filter `type` ต่อช่อง — ไม่เปลี่ยน |
| BR-02/R03 code unique | rule (block) | ✓ | `submitGroup()` L1475-1476,1480 หา dup code แล้ว block+toast |
| BR-02/R04 combination unique | rule (block) | ✓ | `submitSetup()` L1507-1508 หา dup bus×prod block ทั้ง 2 ช่อง |
| BR-03/R05 kind ล็อกหลังสร้างเสมอ | rule (block) | ✓ | `renderGroupForm()` L1204-1207: `isEdit` → kind static div `cursor:not-allowed` ไม่เช็ค used — ไม่เปลี่ยน |
| BR-03/R07 เปลี่ยน kind ก่อนบันทึก → ล้างช่องบัญชี | rule (block) | ✓ | `onKindChange()` ล้าง account fields — ไม่เปลี่ยน (ตรวจซ้ำ, ยังอยู่) |
| S-04/BR-05/IR-PG-01 used>0 ล็อกรหัส (tab1) | scenario+rule (block) | ✓ | `submitGroup()` L1483-1487 block+toast เมื่อ `g.used>0` และ code เปลี่ยน + `renderGroupForm()` L1211-1213 แสดง static locked div + `<span class="lock-tag">` ("ล็อก — มีการบันทึกบัญชีแล้ว") ล่วงหน้าตั้งแต่เปิดฟอร์ม — **GAP-03 (code) ปิดแล้ว** |
| S-04/BR-05/IR-PG-01 used>0 ล็อก combination (tab2) | scenario+rule (block) | ✓ | `submitSetup()` L1510-1517: เช็ค `t.used>0 && (f.bus!==t.bus||f.prod!==t.prod)` → mark `fld-bus`/`fld-prod` invalid + `showToast(...,'error')` + `return` (เหมือน pattern tab1 เป๊ะ) — **GAP-02 ปิดแล้ว**; `renderSetupForm()` L1254-1259 แสดง static locked div + lock-tag บน bus และ prod แยกกันเมื่อ `isEdit&&s.used>0` — **GAP-03 (bus/prod) ปิดแล้ว** |
| S-05 validation: code/name/บัญชีหลักว่าง | scenario/rule (block) | ✓ | `submitGroup()` L1472-1479 — ไม่เปลี่ยน |
| S-05 validation: combination ซ้ำ | scenario/rule (block) | ✓ | `submitSetup()` L1504-1508 — ไม่เปลี่ยน |
| S-06 เปลี่ยนสถานะ 3 ค่าอิสระ ทุกทิศ (view + bulk, ทั้ง 2 tab) | scenario | ✓ | ไม่เปลี่ยนจากรอบก่อน |
| BR-06 GL resolve/entity picker ใช้เฉพาะ "ใช้งาน" | rule (block) | N/A-UI | backend resolve — เก็บ FRD รอบ 2 (เหมือนรอบก่อน) |
| S-07/BR-04/R06 bulk ลบ used>0 ไม่ลบ + confirm บอกยอดข้าม | scenario+rule (block) | ✓ | ไม่เปลี่ยน |
| FN-90 ลบทุกทางผ่าน confirm | FN | ✓ | ไม่เปลี่ยน |
| S-08/BR-07 นำเข้า CSV merge-only per-tab | scenario+rule (block) | ✓ | `openImport()` L1597 เซ็ต `step:'pick'` ตรงเข้าจอ upload-box ทันที ไม่มี `state.import.mode` เลย · `applyImport()` L1646-1671 มีแค่ `state.groups.push(...)`/`state.setup.push(...)` ไม่มี `state.groups=[]`/`state.setup=[]` ที่ไหนในไฟล์ (grep ยืนยัน 0 match) — **GAP-01 ปิดแล้ว** |
| FN-16 จอแรก import = upload-box เท่านั้น ไม่มีตัวเลือกโหมด | FN | ✓ | `renderImportModal()` L1673-1685: `step==='pick'` render แค่ `<label class="upload-box">...` + ปุ่ม template — ไม่มี step `'mode'`, ไม่มี `.mode-opt`/`.mode-radio` ในไฟล์เลย (grep 0 match) — **GAP-01 ปิดแล้ว** |
| FN-17 preview: REQUIRED/BAD_KIND/CODE_DUPLICATE/combination ซ้ำ/บัญชีไม่มีใน COA/BAD_STATUS | FN | ✓ | `buildImportPreview()` L1604-1644 มีครบทุก error code และ **ไม่มีเงื่อนไข `mode==='replace'` คั่นแล้ว** — dedupe check (`CODE_DUPLICATE`/combination ซ้ำ) ทำงานเสมอไม่ถูก skip อีกต่อไป — ดีกว่ารอบก่อนด้วย |
| FN-18 นำเข้า=เพิ่มอย่างเดียว ทะเบียนเดิมไม่ถูกแตะ | FN | ✓ | `applyImport()` L1654 comment ยืนยัน "นำเข้า = เพิ่มอย่างเดียว (merge-only) — ทะเบียนเดิมไม่ถูกแตะ ไม่มีโหมดล้าง/ทับ" ตรงกับโค้ดจริง (push only) — **GAP-01 ปิดแล้ว** |
| FN-19 หน้าสรุปผล: ยอดนำเข้า/ข้าม + ตารางแถวข้าม | FN | ✓ | `renderImportModal()` step `done` L1701-1708 — ไม่เปลี่ยน |
| S-09/FN-20 export CSV per-tab ตาม filter, roundtrip columns, สถานะไทย, BOM, ชื่อไฟล์ | scenario+FN | ✓ | `exportCSV()` L1580-1595 — ไม่เปลี่ยน |
| FN-13 สลับ tab → selection เคลียร์ | FN | ✓ | ไม่เปลี่ยน |
| FN-14 stat 4 ใบต่อ tab กดกรอง | FN | ✓ | ไม่เปลี่ยน |
| FN-06 record ใหม่ DOA null + used=0 | FN | ✓ | ไม่เปลี่ยน |
| BR-08 feature นี้ไม่ post เอง | rule | N/A-UI | ไม่เปลี่ยน |
| Edge เข้า ← COA (F-COA-001) | edge in | ✓ (mock) | ไม่เปลี่ยน |
| Edge เข้า ← Item Master (F-PDM) GL contract endpoints | edge in | N/A-UI | ไม่เปลี่ยน |
| Edge เข้า ← Customer/Vendor/Bank master (อนาคต) | edge in | N/A-UI | ไม่เปลี่ยน |
| Edge ออก → GL/Journal engine | edge out | N/A-UI | ไม่เปลี่ยน |
| Edge ออก → Tax Code (VAT mapping gap) | edge out | ✓ (correctly absent) | ไม่เปลี่ยน |
| §8 Mock data (7 groups/3 setup, used values) | mock data | ✓ | ไม่เปลี่ยน |
| FN-40 · Replace/merge-overwrite import | must-NOT-have | ✓ absent | **ปิดแล้ว** — grep ยืนยันไม่มี `mode-opt`/`mode-radio`/`setImportMode`/`state.import.mode`/`state.groups=[]`/`state.setup=[]` เหลือในไฟล์เลย (0 match ทุกคำ) |
| FN-40 · เปลี่ยน kind หลังสร้าง | must-NOT-have | ✓ absent | ไม่เปลี่ยน |
| FN-40 · ปุ่มลบรายตัว/ลบตัวมี posting/archive-reactivate เดี่ยว | must-NOT-have | ✓ absent | ไม่เปลี่ยน |
| FN-40 · เปลี่ยนรหัส/combination ของ used>0 | must-NOT-have | ✓ absent (enforced + visual lock ล่วงหน้าแล้ว) | ทั้ง block+toast (submit-time) และ lock-tag (แสดงล่วงหน้า) ครบทั้ง 2 tab — ดีกว่ารอบก่อนที่มีแค่ enforce ไม่มี visual |
| FN-40 · VAT Posting Setup tab | must-NOT-have | ✓ absent | ไม่เปลี่ยน |
| FN-40 · UI จัดการค่ากลุ่มธุรกิจ/สินค้า | must-NOT-have | ✓ absent | ไม่เปลี่ยน |
| FN-40 · post บัญชีจริง / สายอนุมัติ | must-NOT-have | ✓ absent | ไม่เปลี่ยน |
| FN-40 · hint-i/field-help/ph-sub | must-NOT-have | ✓ absent | ไม่เปลี่ยน |

## 🔴 Gaps
ไม่มี — ทั้ง 3 gap รอบ 1 ปิดครบ ไม่พบ gap ใหม่จากการตรวจ full matrix ซ้ำ

## 🟡 Warnings / Scope Creep
ไม่พบ — comment PREFLIGHT (L609-626) ระบุ round3 (coverage gate) ตรงกับ fix pass ที่ตรวจอยู่นี้ สอดคล้องกับที่รายงานจริง ไม่มี route/feature เกิน contract

## ⬜ NOT-CHECKED
ไม่มี

## 💡 เสนอเข้า contract
ไม่มี

## Loop Diff จากรอบก่อน (iteration 1 → 2)

**ปิดแล้ว (3/3):**
- **GAP-01** [BLOCK] CSV import Replace mode ล้างทะเบียนเดิม — ปิดแล้ว: `openImport()` เข้า `step:'pick'` ตรงทันที, ไม่มี step `'mode'`/`.mode-opt`/`.mode-radio`/`setImportMode`/`state.import.mode` เหลือในไฟล์เลย, `applyImport()` เหลือแค่ push (ไม่มี `state.groups=[]`/`state.setup=[]`), `buildImportPreview()` ไม่มีเงื่อนไข `mode==='replace'` คั่น dedupe check อีกแล้ว
- **GAP-02** [WARN] tab2 silent revert เมื่อ used>0 ไม่มี toast — ปิดแล้ว: `submitSetup()` L1510-1517 เพิ่ม block+toast ("ชุดกลุ่มนี้มีการบันทึกบัญชีผ่านแล้ว — เปลี่ยนกลุ่มธุรกิจ/สินค้าไม่ได้") ตรง pattern tab1 เป๊ะ
- **GAP-03** [WARN] ไม่มี visual lock indicator บน code/bus/prod เมื่อ used>0 — ปิดแล้ว: `renderGroupForm()`/`renderSetupForm()` แสดง static locked div + `.lock-tag` (ใช้ CSS class ที่เดิมนิยามไว้แต่ไม่ถูกใช้) ทั้ง code (tab1) และ bus/prod แยกช่อง (tab2) ทันทีที่เปิดฟอร์ม edit ของ record used>0

**ค้าง:** ไม่มี

**ใหม่:** ไม่มี — ตรวจ full matrix ซ้ำทั้ง 34 item ไม่พบ regression จากการแก้ 3 จุดนี้ (import flow, submitSetup, lock-tag) ต่อส่วนอื่นของฟีเจอร์
