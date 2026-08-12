# HTML UI Brief — F-PG กลุ่มการบันทึกบัญชีแยกประเภท (GL Posting Group)

> สำหรับ FE dev เริ่มงานเร็ว — อ่านไฟล์นี้ก่อน `FRD_F-PG_Pack/01_UI.md` เต็ม ๆ
> Source: `f-postgrp.html` (gate-passed: UX PASS BLOCK=0, 8 WARN · Coverage PASS round 1 fix + round 2 PASS clean)
> FRD Pack **STANDARD** variant

---

## 1. Entry & Routing

⚠️ **ไม่มี hash routing จริง** — `f-postgrp.html` เป็น SPA state-only ทั้งไฟล์ ทุกหน้า/tab/drawer/modal
สลับด้วย `state.tab` (`'groups'`/`'setup'`) + `state.drawer` (`{open,mode,recordId}`) + `state.modal`
+ `render()`/`renderPageOnly()` เท่านั้น — ไม่มี `location.hash`/`navTo()` ในไฟล์นี้เลย
(เหมือนกันเป๊ะกับ sibling F-COA/F-PM/F-CUST/F-CGRP — ไม่ใช่บั๊กที่ QC gate นี้แก้ให้)

**จุดเข้า:** เปิดไฟล์ → เข้าหน้า "Posting Groups" (tab 1) ทันที ไม่มี landing/redirect · tabbar สลับ tab
1/2 จะเคลียร์ selection + filter สถานะทุกครั้ง (`setTab()`)

---

## 2. CI Snapshot (Warm Light — Sync Read จาก html-generator-v8)

| Token | ค่า |
|---|---|
| Ground | Ivory `#FAF8F5` |
| Text/Sidebar | Charcoal `#111111` (flat) |
| Action/Priority | Red `#FF3B30` |
| Connection | Orange `#FF9A1F` |
| Font | Satoshi + Noto Sans Thai |
| Sidebar | 232px flat charcoal · Shell-bar 52px ขาว |
| Drawer | 920px (`max-width:96vw`) — ใช้ค่าเดียวทั้งไฟล์ ไม่มี `.standard` 680px override (ฟอร์ม kind-based มีช่องบัญชีแปรผัน ≤8 fields ต่อ mode แต่ยึด 920 ตามการแก้ UX-01) |
| Modal | 440px (confirm ลบ bulk + import 3-จังหวะ — ไม่มี `.is-wide`) |
| z-scale | `--z-content:1 --z-sticky:10 --z-dropdown:30 --z-backdrop:50 --z-drawer:51 --z-modal:60 --z-toast:80` (ครบตาม registry v8 `layout-integrity.md` #62 — เพิ่มเข้าไฟล์ระหว่าง UX fix pass รอบที่ 1, เดิมเป็นเลขลอย) |

ค่าจริงยึด Sync Read จาก `html-generator-v8/knowledge/ci-tokens.md` เสมอ — ไม่ hardcode ซ้ำในไฟล์นี้
เพื่อกัน spec โกหกถ้า CI เปลี่ยนรุ่น (ไฟล์นี้ผ่าน QC ตอน v7 ยัง current — v8 มาทีหลัง ค่า token/registry ตรงกันพอดี ไม่มี drift)

---

## 3. Pages / Tabs / Patterns

| Page/Tab ID | ชื่อ | Pattern | ความกว้าง | หมายเหตุ |
|---|---|---|---|---|
| T-01 | Posting Groups (tab 1) | A (list-view) | full | stat 4 ใบ + filter (ประเภทกลุ่ม + สถานะ) + checkbox/bulk + sticky thead |
| T-02 | General Posting Setup (tab 2) | A (list-view) | full | stat 4 ใบ + filter (ค้น bus/prod + สถานะ) + checkbox/bulk |
| P-01 | สร้าง Posting Group (drawer) | B (create) | 920px | kind picker (4 ค่า) → ชุดช่องบัญชีเปลี่ยนตาม kind (R07 ล้างช่องเดิม) |
| P-02 | แก้ไข Posting Group (drawer) | B (edit) | 920px | kind แสดงแบบ lock-tag เสมอ (R05) · code เพิ่ม lock-tag เมื่อ `used>0` (IR-PG-01) — ชื่อ/บัญชี/สถานะ editable เสมอ |
| P-03 | สร้าง/แก้ไข Posting Setup (drawer) | B (create/edit) | 920px | bus×prod + บัญชี 3 ช่อง (sales/purchase/COGS) · bus/prod แต่ละช่องได้ lock-tag แยกกันเมื่อ `used>0` |
| P-04 | View drawer (ทั้ง 2 entity) | C (view) | 920px | ชุดบัญชีที่ผูก + เมนูเปลี่ยนสถานะ 3 ค่า + ปุ่มแก้ไข |
| P-05 | นำเข้า CSV (3 จังหวะ pick→preview→done) | D (modal, single-modal wizard) | 440px | **ไม่มี mode selector** จอแรก (merge-only บังคับ — ดู §6) · per-tab (แยก template/preview ตาม tab ที่เปิดอยู่) |
| P-06 | ยืนยันลบ bulk | D (confirm) | 440px | บอกยอด "ลบแล้ว N รายการ · ข้าม M (มีการบันทึกบัญชีผ่านแล้ว)" |

**ไม่มี:** VAT Posting Setup (tab 3 — decided แล้วแต่ deferred Phase 2, ดู §7), stepper wizard,
role switcher, tree/hierarchy, ปุ่มลบเดี่ยวต่อแถว (มีแต่ bulk delete)

---

## 4. Lock-Rule Guard Map (จุดที่ FE dev ต้อง wire ให้ตรง — 2 กฎแยกกันเด็ดขาด)

⚠️ **ห้ามรวม guard เดียวกัน** — นี่คือ 2 rule คนละที่มา คนละเงื่อนไข:

| Rule | เงื่อนไข lock | Field ที่ล็อก | Field ที่ยัง editable |
|---|---|---|---|
| **R05** (BR-03) | เสมอ — ไม่เช็ค `used` เลย, ล็อกตั้งแต่โหมด edit | `kind` (tab1) | ทุกอย่างอื่น |
| **IR-PG-01** (BR-05, ✅ confirmed มติ 2026-08-09 — ไม่ใช่ AI-draft) | `used > 0` เท่านั้น | `code` (tab1) / `bus`+`prod` (tab2) | name/ชื่อ, บัญชีทุกช่อง, สถานะ — **แก้ได้ปกติแม้ used>0** |

**Side effect ของ IR-PG-01 เมื่อฝืนแก้ตอน `used>0`:**
- Tab1: toast error "กลุ่มนี้มีการบันทึกบัญชีผ่านแล้ว — เปลี่ยนรหัสไม่ได้ (แก้ชื่อ/บัญชี/สถานะได้ปกติ)" (`is-invalid` บน field code)
- Tab2: toast error "ชุดกลุ่มนี้มีการบันทึกบัญชีผ่านแล้ว — เปลี่ยนกลุ่มธุรกิจ/สินค้าไม่ได้" (`is-invalid` บน field bus+prod)

**R07 side effect:** เปลี่ยน kind ก่อน submit (โหมดสร้างเท่านั้น เพราะ edit ล็อก kind อยู่แล้ว) → ล้างช่องบัญชีทั้งหมดที่ผูกกับ kind เดิมทันที (`onKindChange`)

**Visual indicator:** ทั้ง 3 field ที่ล็อกได้ (`kind` เสมอ, `code`/`bus`+`prod` เมื่อ `used>0`) render เป็น static `.sdd-trigger` + `.lock-tag` (ไอคอนล็อก + ข้อความ) แทน dropdown ที่กดได้ — ไม่ใช่แค่ disabled attribute เฉย ๆ

---

## 5. Microcopy Anchors (สกัด verbatim จาก `f-postgrp.html` ที่ผ่าน gate แล้ว — ห้ามแต่งใหม่)

| จุด | ข้อความจริงในไฟล์ |
|---|---|
| Toast สร้าง Posting Group | "สร้าง Posting Group แล้ว" |
| Toast สร้าง Posting Setup | "สร้าง Posting Setup แล้ว" |
| Toast แก้ไข Posting Group | "บันทึกการแก้ไขกลุ่มแล้ว" |
| Toast แก้ไข Posting Setup | "บันทึกการแก้ไข setup แล้ว" |
| Toast เปลี่ยนสถานะ (เดี่ยว) | "เปลี่ยนสถานะเป็น {label} แล้ว" |
| Toast เปลี่ยนสถานะ (bulk) | "เปลี่ยนสถานะ {n} รายการเป็น {label} แล้ว" |
| ปุ่ม primary สร้างใหม่ | "ยืนยันสร้าง" (create) / "บันทึกการแก้ไข" (edit) |
| Error: code ซ้ำ (tab1) | "รหัสกลุ่มนี้มีอยู่แล้ว" |
| Error: combination ซ้ำ (tab2) | "ชุดกลุ่มนี้มีอยู่แล้ว" |
| Error: IR-PG-01 ฝืนแก้ code (tab1) | "กลุ่มนี้มีการบันทึกบัญชีผ่านแล้ว — เปลี่ยนรหัสไม่ได้ (แก้ชื่อ/บัญชี/สถานะได้ปกติ)" |
| Error: IR-PG-01 ฝืนแก้ combination (tab2) | "ชุดกลุ่มนี้มีการบันทึกบัญชีผ่านแล้ว — เปลี่ยนกลุ่มธุรกิจ/สินค้าไม่ได้" |
| Toast ลบ bulk สำเร็จ (ไม่มีข้าม) | "ลบแล้ว {n} รายการ" |
| Toast ลบ bulk สำเร็จ (มีข้าม used>0) | "ลบแล้ว {n} รายการ · ข้าม {m} (มีการบันทึกบัญชีผ่านแล้ว)" |
| Confirm ลบ bulk (modal body) | "ยืนยันการลบ — รายการที่มีการบันทึกบัญชีผ่าน mapping แล้วจะไม่ถูกลบ (R06 — soft-delete เท่านั้น)" |
| Import preview summary | "ตรวจแล้ว {N} แถว — นำเข้าได้ {ok} แถว …" |
| Import done summary | "นำเข้าแล้ว {n} รายการ" + (ถ้ามีข้าม: " · ข้าม {m} แถว") |
| Empty state (มี filter) | "ไม่พบรายการที่ตรงกับเงื่อนไข" / "ลองปรับคำค้นหรือล้างตัวกรอง" |
| Toast ดาวน์โหลด template | "ดาวน์โหลด template ตัวอย่างแล้ว" |
| Toast export สำเร็จ | "ส่งออก {n} รายการเป็น CSV แล้ว" |
| Export filename (tab1/tab2) | `postgrp_groups_export_YYYY-MM-DD.csv` / `postgrp_setup_export_YYYY-MM-DD.csv` |
| Import template filename (tab1/tab2) | `postgrp_groups_import_template.csv` / `postgrp_setup_import_template.csv` |

ค่าที่ไม่ verbatim ในไฟล์ (toast/ปุ่ม/confirm มาตรฐานอื่น ๆ ที่ไม่ระบุด้านบน) → Sync Read จาก
`html-generator-v8/knowledge/microcopy.md` เสมอ ห้ามหยิบจากความจำ

---

## 6. FN-40 Guard Checklist (สิ่งที่ FE dev ต้อง**ไม่**เพิ่มระหว่าง build — ตรวจซ้ำก่อน PR merge)

- [ ] ไม่มีโหมดนำเข้า Replace/merge-overwrite — จอแรกของ P-05 มีแค่ upload-box + ปุ่ม template ต่อ tab เท่านั้น ไม่มี mode selector (ถูกเพิ่มเข้ามาแล้วเอาออกไปแล้วรอบ coverage-fix — ดู §7 gap #1)
- [ ] ไม่มีทางเปลี่ยน `kind` หลังสร้าง (R05 ล็อกเสมอในโหมด edit)
- [ ] ไม่มีปุ่มลบเดี่ยวต่อแถว (row actions มีแค่ปุ่มแก้ไข — มีแต่ bulk delete)
- [ ] ไม่มี tab 3 "VAT Posting Setup" (decided แล้วแต่ deferred Phase 2 — ดู §7 gap #2)
- [ ] ไม่มี UI จัดการค่ากลุ่มธุรกิจ/กลุ่มสินค้า (R09 DYNAMIC — decided แล้วแต่ deferred Phase 2 — ดู §7 gap #3)
- [ ] ไม่มี UI ที่ post บัญชีจริง (feature นี้ไม่ post เอง — BR-08, GL engine เป็นผู้ post)
- [ ] ไม่มี UI สายอนุมัติใด ๆ ผูกกับ record (DOA placeholder 4 fields = null เสมอ — OB-5)
- [ ] ไม่มี hint-i/field-help/ph-sub ใต้ช่องฟอร์ม (มติเลน)

---

## 7. Known Gaps (ส่งต่อ FRD/BRD Open Questions — อย่า report ซ้ำเป็นบั๊กใหม่ตอน QA)

1. **CSV import — ไม่มี mode selector เป็นเจตนา ไม่ใช่ของหลุด** — เคยมีการเพิ่ม Replace/Merge
   mode step เข้ามาระหว่าง UX-fix pass (ตามแพทเทิร์นมาตรฐาน CSV import ของเลน) แต่ถูก **revert
   ออกทั้งหมด** ในรอบ coverage-fix เพราะขัดกับ BR-07/FN-40 ของฟีเจอร์นี้โดยเฉพาะ (ห้ามมีทาง
   wipe/overwrite ทะเบียน mapping ที่ระบบใช้งานจริง) — ถ้าเห็น diff เก่าที่มี mode step อย่า apply กลับ
2. **VAT Posting Setup (tab 3) — decided (Option B) แต่ยัง build ไม่ได้** (OQ-PG-01, ปิด 2026-08-10)
   → อยู่ BRD §13 Phase 2 — lane รอบถัดไปจะผลิต HTML/FRD ของตัวเองผ่าน gate ใหม่ ก่อนถึงตอนนั้น
   dev ห้าม implement tab 3
3. **Product-group axis (GOODS/SERVICE) — decided ให้เปลี่ยนเป็นชุด Item Master 6 ค่า แต่ยัง
   build ไม่ได้** (OQ-PG-04, ปิด 2026-08-10) → Phase 2 เดียวกับข้อ 2 — HTML ปัจจุบันยังเป็น
   DOMESTIC/FOREIGN × GOODS/SERVICE ตาม as-built เดิม
4. **COA dropdown ยัง mock 16 บัญชี hardcode** — real API contract เขียนไว้แล้วที่
   `FRD_F-PG_Pack/02_API.md` §2.5 (`GET /api/v1/coa/accounts?is_leaf=true&is_postable=true&status=active&type=...`
   + `ENG-PG-01 coa-account-resolver`) แต่ HTML **ยังไม่ swap เป็น API จริง** — dev ต้อง implement ตาม contract นั้นตอน build จริง
5. **`used` ยังเป็น mock นิ่ง (ไม่ sync journal จริง)** — OQ-PG-03 ยังเปิด กำหนดต้องปิดก่อน dev handoff
   (มิฉะนั้น IR-PG-01 lock อาจไม่ตรงกับ posting จริงตอน production)
6. **ไม่มี confirm modal ตอนเปลี่ยนสถานะเป็น "ไม่ใช้งาน"** (ทั้งเดี่ยวและ bulk) — ต่างจาก bulk-delete
   ที่มี confirm แล้ว (WARN UX-17, ยังไม่ fix — เกณฑ์ user ตัดสินใจได้ว่าจะ fix ก่อน build จริงหรือไม่)
7. **Empty state มีแค่เคส "filter ไม่เจอ"** — ไม่มี branch "ยังไม่มีข้อมูลเลย" ที่ควรมีปุ่ม primary
   "เพิ่ม Posting Group/Setup" (WARN UX-18, ยังไม่ fix — mock data ไม่เคยว่างจริงจึงไม่เคย exercise เคสนี้)
8. **ไม่มี hash routing** — เหมือน sibling ทุกตัวในเลนนี้ (ดู §1)

---

## 8. Screenshots อ้างอิง

ดู `_shots/` (โฟลเดอร์เดียวกับไฟล์นี้ — `01_HTML/_shots/`) — 33 ภาพ ครอบ: list ทั้ง 2 tab (groups/
filterbar/bulkbar/rowactions/empty), create drawer (info/kind/acct-vendor/footer, setup-fields/footer),
edit drawer (kind-locked, group-locked/unlocked, setup-locked/unlocked — พิสูจน์ partial-lock ของ §4),
import 3 จังหวะ (pick/preview/done), bulk delete confirm modal.
