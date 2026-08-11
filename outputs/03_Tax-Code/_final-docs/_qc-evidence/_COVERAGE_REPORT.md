# _COVERAGE_REPORT · Tax Code (F-TAX) — ทะเบียนรหัสภาษี

> Skill: **qc-coverage-checker** (Step 4 / WF-01) — ตรวจ "ทำครบมั้ย" เชิง **business scope** (ไม่ใช่ form/UI polish — นั่นคืองาน qc-ux-html-checker)
> Artifact under test: `Pack Brief Feature/3. Tax Code/f-taxcode.html` (930 บรรทัด, html-generator-v8 as-built)
> วันที่ตรวจ: 2026-08-10 · Verdict ด้านล่าง

---

## ⚠️ Baseline Deviation (บันทึกตามคำสั่ง)

`workflow_graph.json` + `NODE_BRIEF` (จาก plan-module-workflow-mapper) **ไม่มีสำหรับ feature นี้** — ไม่เคยรัน graph mapper.
ตามหลักปกติของ skill นี้ "ไม่มี contract = หยุด" แต่รอบนี้ orchestrator สั่งให้**แทน baseline** ด้วยแหล่ง authoritative 3 ชุด และใช้เป็น contract แทน:

1. `PREBRIEF_F-TAX_Tax-Code.md` — Scenarios S-01..S-10, Business Rules BR-01..BR-10, Obligations OB-1..OB-8, §11 Coverage Matrix, §9 Edges
2. `FUNCTION_CHECKLIST_F-TAX_Tax-Code.md` — FN-01..FN-24 + FN-40 (scope-lock "ไม่รองรับ")
3. `Central Plan v2/CENTRAL_PLAN_CORE_ERP.md` — outbound edges ของ Tax Code (soft-reference)

ทุก ✓ อ้าง evidence เป็น function name / line / selector ในไฟล์ HTML — ไม่มีการเช็คจากความจำ.

**สัญกรณ์:** `✓` = พบ evidence · `✗` = ควรมีแต่ไม่พบ (gap) · `∅-ok` = scope-lock ต้อง "ไม่มี" และไม่มีจริง (ผ่าน) · `N/A-DS` = enforcement อยู่ฝั่ง downstream/consumer feature ที่ยังไม่มี HTML — ตรวจ enforcement ที่นี่ไม่ได้ แต่ data-hook พร้อม

---

## 1. Scenarios (S-01..S-10)

| S | สรุป | สถานะ | Evidence (HTML) |
|---|---|---|---|
| S-01 | สร้างรหัส VAT/WHT จาก drawer เดียว | ✓ | `openCreate()` L638 → `formHTML('create',{})` L573 → `saveUnit('create')` L641; auto code `autoCode()` L680 / finalCode L655; status 3 ค่า L619-623 |
| S-02 | สร้าง "ยกเว้นภาษี" → rate ล็อก 0 | ✓ | `onTypeChange()` L634-637: `exempt` → `el.value='0'; el.disabled=true;` · สลับกลับ → `el.disabled=false` |
| S-03 | แก้ตัว `used=0` ได้ทุก field | ✓ | `openEdit()` L639; `locked=isEdit&&(r.used||0)>0` L576 → ถ้า used=0 ไม่ locked; save else-branch L671 เขียนทุก field |
| S-04 | แก้ตัว `used>0` — code/rate/type ล็อก | ✓ | `locked` L576 + `lockTag` L577; `disabled` บน code L596 / rate L601 / category L615; logic guard L670 |
| S-05 | เปลี่ยนสถานะอิสระ (เดี่ยว/bulk) | ✓ | เดี่ยว `setStatus()` L846 (ไม่มี gate); status menu L732-734; bulk `bulkSetStatus()` L854 |
| S-06 | bulk ลบ — ตัวถูกใช้ถูกข้าม | ✓ | `openBulkDelete()` L859; `confirmBulkDelete()` L874-880: `used>0` → skip |
| S-07 | ข้อมูลผิด (dup / rate) | ✓ | `saveUnit()` dup L656-657 (`.toLowerCase()`), RATE_INVALID L662 |
| S-08 | นำเข้า CSV พร้อมสถานะ | ✓ | `bulkImport()` L792 → `bulkPick()` L793 → `bulkValidateRow()` L771 → preview L819 → `bulkConfirm()` L794 |
| S-09 | ส่งออก CSV ตาม filter + BOM | ✓ | `exportCSV()` L882: `getFiltered()` L883, BOM `'﻿'` L886, 7 คอลัมน์ L884 |
| S-10 | **ไม่รองรับ** (scope lock) | ∅-ok | ดูตาราง FN-40 §5 — ทุกข้อ①-⑥ ยืนยัน "ไม่มี" จริง |

**Scenarios: 10/10 covered** (S-10 คือ "ต้องไม่มี" และไม่มีจริง)

---

## 2. Business Rules (BR-01..BR-10) — block-severity ทำเข้ม

| BR | กติกา | UI | Logic | สถานะ | Evidence |
|---|---|---|---|---|---|
| BR-01 | รหัสห้ามซ้ำ (case-insensitive) — สร้าง/แก้/นำเข้า | ✓ | ✓ | ✓ | save `dup` L656 `.toLowerCase()...&&r.id!==id`; import L777 `.toLowerCase()` CODE_DUPLICATE |
| BR-02 | อัตรา 0–100 ทศนิยมได้ | ✓ | ✓ | ✓ | save L662 (`<0||>100||NaN`); import L774 RATE_INVALID; ทศนิยม `Number(rateRaw)` รับ 0.75 |
| BR-03 | ยกเว้น → rate=0 (UI+logic+import) | ✓ | ✓ | ✓ | UI `onTypeChange` L636; logic `if(category==='exempt') rate=0` L661; import EXEMPT_RATE L775 |
| **BR-04 (IR-TAX-01)** | `used>0` → รหัส/อัตรา/ประเภท ล็อก ทั้ง UI+logic | ✓ | ✓ | ✓ | UI `disabled` L596/601/615 + lockTag L577; **logic guard** L670 เขียนเฉพาะ name/status แม้ฝืน — **บังคับสองชั้นครบ** |
| BR-05 | `used>0` ลบไม่ได้ — bulk ข้าม | ✓ | ✓ | ✓ | `confirmBulkDelete()` L877 `(r.used>0?skip:del)`; confirm modal นับ skip L861,867 |
| BR-06 | สถานะ 3 ค่า เปลี่ยนอิสระทุกทิศ ไม่มีอนุมัติ | ✓ | ✓ | ✓ | `setStatus()` L846-847 ไม่มี gate; menu current disabled L734 |
| BR-07 | ปลายทางเลือกได้เฉพาะ "ใช้งาน" | N/A-DS | — | N/A-DS | Enforcement อยู่ที่ Item Master/เอกสาร (ยังไม่มี HTML) — **data-hook พร้อม**: status field exposed L619-623 + soft-ref comment L351 |
| BR-08 | นำเข้ารายแถว, ข้ามแถวผิด, status ว่าง=ร่าง, ประเภทชื่อไทย | ✓ | ✓ | ✓ | `bulkValidateRow()` L771-778; `bulkConfirm` L797 `STATUS_TH_MAP[...]||'draft'`; `CAT_TH_MAP` (ชื่อไทย) L762 |
| BR-09 | ไม่เก็บบัญชี GL ใด ๆ | ∅-ok | ∅-ok | ✓ | ไม่มี field GL ใน `formHTML` L578-632; comment L350 "GL Posting Setup อ้างรหัสจากที่นี่"; data model L376-386 ไม่มี account |
| BR-10 | audit ผู้สร้าง/แก้ + เวลา (tab ประวัติ) | ✓ | ✓ | ✓ | tab history `viewBody` L698-705; fields created/updated_by+at L376-386 |

**BR: 9/10 บังคับใน artifact นี้ครบ · BR-07 = N/A-DS (data-hook พร้อม)** · **ทุก block-rule (01-06,08,09) ครบทั้ง UI+logic**

---

## 3. Obligations (OB-1..OB-8)

| OB | พันธะ | สถานะ | Evidence |
|---|---|---|---|
| OB-1 | Item Master ← active tax codes, soft-ref (แค่รหัส) | N/A-DS + hook | status field exposed L619-623; soft-ref comment L351 "เอกสาร/สินค้าเก็บแค่ code"; filtering จริงอยู่ downstream |
| OB-2 | GL Posting Setup map รหัส→GL; ทะเบียนนี้ไม่เก็บเลขบัญชี | ✓ | = BR-09; comment L350 |
| OB-3 | Master กลาง — เอกสารขาย/ซื้อใช้อัตราจากที่นี่ | ✓ (data) | rate field L599-603; BACKEND comment L350 "ขาย/ซื้อ/บัญชีใช้ร่วม" |
| OB-4 | DOA: ไม่มีสายอนุมัติ — placeholder 4 fields=null | ✓ | L389 `r.approver_role=null; approved_by=null; approved_at=null; approval_chain=null`; ไม่มี UI อนุมัติ |
| OB-5 | NOTIF: ไม่ emit event | ✓ | comment L390 "ไม่ emit event เอง"; กระดิ่ง L320-325 เป็น placeholder |
| OB-6 | Pattern เลน (3 status·bulk·import template ไม่มีข้อความคอลัมน์·export·ไม่มี icon·ไม่มีลบเดี่ยว·ตัดคำอธิบาย) | ✓ | 3 status L619; bulk L470-476; import จอแรกมีแค่ box+template L812-817; template `downloadTemplate` L780; export L502; ไม่มี icon หน้ารหัส (cell-code เปล่า) L459; ไม่มีลบเดี่ยว (row action มีแค่ "แก้ไข") L466; ไม่มี hint ใต้ช่อง (FN-04) |
| OB-7 | v8: #96 full-height · #97 responsive 768 · overlay-root · Esc chain | ✓ | #96 CSS L88-92; #97 L93-102 (min-width 768 L15); `#overlay-root` L927; Esc chain L917-923 (modal>drawer>menu) |
| OB-8 | เป็น 1 ใน 3 blockers (ปลดล็อก Sales Config/เอกสาร/DOA) | N/A (meta) | เป็นพันธะเชิงแผน — ตรวจใน artifact ไม่ได้ |

**OB: OB-2,3,4,5,6,7 ครบ · OB-1 N/A-DS(hook พร้อม) · OB-8 meta**

---

## 4. Function Checklist (FN-01..FN-24)

| FN | ต้องทำได้ | สถานะ | Evidence |
|---|---|---|---|
| FN-01 | สร้างจาก drawer เดียว | ✓ | `formHTML`/`saveUnit` L573,641 |
| FN-02 | เว้นรหัส → auto ไม่ชน | ✓ | `autoCode()` L680; `finalCode=code||autoCode()` L655 |
| FN-03 | rate ทศนิยม + 3 status ตั้งแต่สร้าง | ✓ | rate `inputmode` L601 `Number()` รับ 0.75; status L619-623 |
| FN-04 | ฟอร์มไม่มีข้อความคำอธิบายใต้ช่อง (มีได้แค่ป้ายล็อก) | ✓ | `formHTML` L594-624 มีแค่ `.err` (validation) + `lockTag` — ไม่มี `.hint` ใต้ช่อง |
| FN-05 | ยกเว้น → rate ล็อก 0, สลับกลับปลดล็อก | ✓ | `onTypeChange()` L634-637 |
| FN-06 | used=0 แก้ได้ทุก field | ✓ | save else-branch L671 |
| FN-07 | used>0 disabled + ป้าย "ล็อก — ถูกใช้งานแล้ว"; ชื่อ/สถานะแก้ได้ | ✓ | lockTag L577 text ตรง; disabled L596/601/615; name/status ไม่ disabled |
| FN-08 | บันทึกตัวล็อก — คงค่า code/rate/type เดิม (guard ฝั่ง logic) | ✓ | L670 `if((r.used||0)>0){Object.assign(r,{name_th,name_en,status,...})}` — ไม่แตะ code/rate/category |
| FN-09 | view header เมนู 3 ค่า ทุกทิศ ค่าปัจจุบัน disabled ไม่มีอนุมัติ | ✓ | `viewHTML` L732-734: current → `stop(event)` (disabled) |
| FN-10 | checkbox + bulk bar 3 ค่า + toast จำนวน | ✓ | `bulkSetStatus()` L854-857 toast นับ n |
| FN-11 | ตัวไม่ active ไม่โผล่ dropdown ปลายทาง (ตรวจฝั่งปลายทาง) | N/A-DS | Downstream ยังไม่มี HTML — checklist เองระบุ "ตรวจฝั่งปลายทาง"; data-hook (status) พร้อม |
| FN-12 | bulk ลบ → confirm บอกลบจริง + ข้าม | ✓ | `openBulkDelete()` L866-871: title `ids.length`, desc used, ปุ่ม `ลบ ${ids.length-used}` |
| FN-13 | ยืนยัน: used=0 หาย · used>0 อยู่ + toast ข้าม | ✓ | `confirmBulkDelete()` L874-880 |
| FN-14 | รหัสซ้ำ → บล็อกชี้ช่อง | ✓ | L657 `err-code` + `has-err` บน `fld-code` |
| FN-15 | rate ว่าง/ลบ/>100 → บล็อก | ✓ | L662 `has-err` บน `fld-rate` |
| FN-16 | import จอแรก: แค่ box + ปุ่ม template (ไม่มีข้อความคอลัมน์) | ✓ | `bulkModalHTML` step='pick' L812-817; template `taxcode_import_template.csv` header+3 แถว+ทศนิยม L781-786 |
| FN-17 | preview รายแถว — เหตุตรงกรณี (6 codes) | ✓ | `bulkValidateRow` L772-777: REQUIRED/BAD_TYPE/RATE_INVALID/EXEMPT_RATE/BAD_STATUS/CODE_DUPLICATE; preview L824-827 |
| FN-18 | นำเข้าได้สถานะตามไฟล์ (ว่าง=ร่าง)+rate ทศนิยม, แถวผิดข้าม | ✓ | `bulkConfirm` L794-800 `STATUS_TH_MAP[...]||'draft'`, `Number(row.rate)` |
| FN-19 | ปิดจอผล → list + stat อัพเดต | ✓ | L801 `renderList()` หลัง import |
| FN-20 | export ตาม filter + BOM | ✓ | `exportCSV()` L882-889 |
| FN-21 | list คอลัมน์ (รหัสไม่มี icon)/ชื่อ/อัตรา%/ประเภท/ใช้/สถานะ(pill+icon); sort อัตราแบบตัวเลข | ✓ | table L457-467 (cell-code ไม่มี avatar); sort numeric L411 `if(col==='used'||col==='rate')`; statusPill icon L360 |
| FN-22 | stat 4 ใบ กดกรอง + กดซ้ำยกเลิก | ✓ | `stat()` L437; `quickFilter()` L548-552 `status===key?'all':key` (toggle) |
| FN-23 | tab การใช้งาน แสดงจำนวน — **ไม่มีแถวลบออกจากทะเบียน** | ✓ | `viewBody` usage L690-696 มีแค่ "จำนวนที่ถูกอ้างอิง" — ไม่มีปุ่ม/แถวลบ |
| FN-24 | 768–1180 responsive + Esc chain | ✓ | CSS #97 L93-102; Esc L917-923 |
| FN-90 | ลบทุกทางผ่าน confirm | ✓ | bulk delete มี modal confirm L863-872 (ไม่มีทางลบอื่น) |
| FN-92 | validate ก่อนบันทึก + กันกดซ้ำ (loader) | ✓ | `saveUnit` L649-663 validate; L665-666 `btn.classList.add('is-disabled')` + spinner |
| FN-93 | tab ประวัติ ผู้สร้าง/แก้ + เวลา | ✓ | `viewBody` history L698-705 |

**FN: 23/24 covered ใน artifact · FN-11 = N/A-DS · FN-90/92/93 ครบ**

---

## 5. FN-40 — Scope Lock (ต้อง "ไม่มี" จริง)

| ห้ามมี | ควรมั้ย | ผลตรวจ | Evidence (ยืนยันไม่มี) |
|---|---|---|---|
| แก้ code/rate/type ของตัวที่ถูกใช้ (IR-TAX-01) | ∅ | ∅-ok | ล็อกจริง — disabled L596/601/615 + guard L670; ไม่มีทางแก้ |
| ช่วงเวลาบังคับใช้อัตรา (effective date / validity period) | ∅ | ∅-ok | ไม่มี field วันที่ใน `formHTML` L578-632; data model L376-386 ไม่มี effective_from/to |
| field ผูกเลขบัญชี GL | ∅ | ∅-ok | ไม่มี field GL account (= BR-09) |
| เพิ่ม/แก้ประเภทภาษี (fix 3 ค่า) | ∅ | ∅-ok | `CATEGORIES` fix 3 ค่า L352-356; ไม่มี UI เพิ่มประเภท; select อ่านจาก constant L571 |
| ปุ่มลบรายตัว / ลบตัวที่ถูกใช้ | ∅ | ∅-ok | row-actions มีแค่ปุ่ม "แก้ไข" L466 (ไม่มี trash เดี่ยว); bulk ข้าม used L877 |
| ขั้นส่งอนุมัติ / สายอนุมัติ | ∅ | ∅-ok | placeholder null L389; ไม่มี UI อนุมัติ; setStatus ไม่มี gate L846 |
| icon/avatar หน้ารหัสใน list · ข้อความอธิบายคอลัมน์จอนำเข้า | ∅ | ∅-ok | cell-code เปล่า L459; import จอแรกไม่มีข้อความคอลัมน์ L812-817 |

**FN-40: 7/7 scope-lock items ยืนยัน "ไม่มี" จริง — scope lock HOLDS**

---

## 6. Outbound Edges (§9 PREBRIEF + Central Plan) — soft-reference hooks

| ทิศ | คู่ | Central Plan ref | ผลตรวจ | Evidence |
|---|---|---|---|---|
| ออก | → Item Master (กลุ่มภาษี) — เฉพาะ active, soft-ref code | L451,113 (`tax_code` in line) | ✓ hook (enforce=N/A-DS) | status exposed L619; soft-ref comment L351; enforcement filter อยู่ Item Master wizard |
| ออก | → เอกสารขาย/ซื้อ (QT/SO/INV/PR/PO) — rate ให้ B2 line editor | L668 AR / L669 AP | ✓ hook (enforce=N/A-DS) | rate field L599; comment L350 "ขาย/ซื้อ...ใช้ร่วม" |
| ออก | → GL Posting Setup — รหัสให้ map เข้า GL | L34 (Accounting) | ✓ ถูกต้อง | ทะเบียนนี้ไม่เก็บ GL (BR-09/OB-2); comment L350 |
| — | DOA / NOTIF | — | ✓ placeholder-null | DOA L389 4 fields=null; NOTIF comment L390 ไม่ emit |

**Edges: 3/3 outbound hooked ถูกต้อง (soft-ref) · DOA/NOTIF placeholder-null ยืนยันแล้ว**
> หมายเหตุ: consumer features (AR/AP Invoice, Item Master combobox, GL Posting Setup) ยังไม่มี HTML — enforcement ปลายทางตรวจได้เมื่อ features เหล่านั้นถูกสร้าง (ตอนนั้นควรรัน mapper + qc-coverage รอบ 2)

---

## 7. Scope-Creep Check (ของเกิน contract)

**Business scope creep: 0** — ไม่พบ feature/flow เกินขอบเขตที่ประกาศ (ไม่มี effective date, ไม่มี GL account, ไม่มีสายอนุมัติ, ไม่มีเพิ่มประเภท, ไม่มีลบเดี่ยว)

**ข้อสังเกตเชิง cosmetic (ไม่ใช่ scope creep — เป็นงาน qc-ux, แจ้งเพื่อบันทึก):**
- N-1 | Notif placeholder L323-324 เป็นข้อความค้างจาก template UoM: "มีรหัสภาษีใหม่ 2 รายการ**รอตรวจทาน**" (คำว่า "รอตรวจทาน" สื่อ workflow ตรวจทาน/อนุมัติ ที่ขัดกับ BR-06 no-approval) และ ""ลิตร" ถูกหยุดใช้งานเมื่อวานนี้" ("ลิตร" = หน่วยนับ ไม่เกี่ยวภาษี) — เป็น placeholder ไม่ใช่ functional hook แต่ควรแก้ข้อความ
- N-2 | comment/route ค้างจาก UoM: `data-feature="uom-master"`, `onclick="navTo('units')"` L297/317, comments "UoM ไม่มีสายอนุมัติ" L388-390, footer "UAT · v6" L313, "kit ... v6" — cosmetic ไม่กระทบ scope
- → ทั้งหมดเป็น microcopy/technical leftover → ส่งต่อให้ **qc-ux-html-checker** ไม่นับเป็น coverage gap

---

## 8. Coverage Summary

| หมวด | ครบ | N/A-DS (downstream) | Gap (in-scope) | Scope-lock ∅-ok |
|---|---|---|---|---|
| Scenarios | 9 (S-01..09) | — | 0 | S-10 (∅-ok) |
| Business Rules | 9 (01-06,08,09,10) | 1 (BR-07) | 0 | — |
| Obligations | 6 (02-07) + OB-8 meta | 1 (OB-1) | 0 | — |
| FN-01..24 | 23 + FN-90/92/93 | 1 (FN-11) | 0 | — |
| FN-40 scope-lock | — | — | 0 | 7/7 hold |
| Outbound edges | 3/3 hooked + DOA/NOTIF | (enforce ปลายทาง) | 0 | — |

- **Covered (in-scope, evidence-backed):** ทุก Scenario · ทุก block-rule (UI+logic สองชั้น) · ทุก FN มี UI hook · edges hooked ถูก
- **True in-scope gaps:** **0**
- **Business scope-creep:** **0** (cosmetic leftover 2 รายการ → qc-ux)
- **N/A-DS (verify ไม่ได้ใน artifact นี้ — data-hook พร้อม):** BR-07, OB-1, FN-11 (enforcement เลือกเฉพาะ active อยู่ฝั่ง consumer)

---

## 9. VERDICT: ✅ **PASS**

**เหตุผล:** ทุก block-severity rule (BR-01..06, BR-09, IR-TAX-01) ครอบครบ **ทั้ง UI และ logic guard** พร้อม evidence · ทุก Scenario S-01..S-09 มี UI+function · S-10/FN-40 scope-lock 7/7 ยืนยัน "ไม่มี" จริง · outbound edges 3/3 hooked เป็น soft-reference ถูกต้อง (ไม่เก็บ GL) · DOA/NOTIF placeholder-null · ไม่มี business scope creep.

**เงื่อนไข/หมายเหตุ (advisory — ไม่ลด verdict):**
1. **N/A-DS items (BR-07 / OB-1 / FN-11):** การบังคับ "ปลายทางเลือกได้เฉพาะ active" ตรวจ enforcement ใน artifact นี้ไม่ได้เพราะ consumer features (Item Master combobox, AR/AP Invoice, GL Posting Setup) ยังไม่มี HTML — data-hook (status field + soft-ref) พร้อมแล้ว. **ต้อง re-verify ตอน consumer features ถูกสร้าง** (แนะนำรัน plan-module-workflow-mapper เพื่อสร้าง workflow_graph.json แล้ว qc-coverage รอบ 2 cross-module).
2. **Cosmetic microcopy leftover** (notif "รอตรวจทาน"/"ลิตร", comment/route UoM) → domain ของ **qc-ux-html-checker**, ไม่ใช่ coverage.
3. **Contract debt:** feature นี้ไม่มี workflow_graph/NODE_BRIEF — baseline ครั้งนี้ substitute จาก PREBRIEF+FUNCTION_CHECKLIST+Central Plan. เพื่อ traceability ระยะยาวควรรัน mapper ย้อนหลัง.
