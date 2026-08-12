# Coverage Report — F-BOM-001 · Bill of Materials (รอบ 1: HTML vs Business Scope)

- วันที่: 2026-08-11 · WF-01 Step 4 · skill: qc-coverage-checker (รอบ 1)
- Artifact ที่ตรวจ: `outputs/05_BOM/01_HTML/f-bom.html` (753 บรรทัด)
- Contract (source-of-truth):
  - `Pack Brief Feature/5. BOM/FUNCTION_CHECKLIST_F-BOM_Bill-of-Materials.md` (FN-01..23 · FN-30 · FN-40)
  - `Pack Brief Feature/5. BOM/PREBRIEF_F-BOM_Bill-of-Materials.md` (§9 Edges · BR/VR · OQ)
  - `Central Plan v2/CENTRAL_PLAN_CORE_ERP.md` (BOM → Item Master = เส้นเดียว)
- Checklist: FN 23 · edges in 2 · edges out 2 (declared-unbuilt) · FN-30 pass-through 3 · FN-40 lock 8

## Verdict: 🟡 WARN
สรุป: ครอบ **22/23 FN** · △ partial 1 (FN-09) · edges in 2/2 · edges out 2/2 (placeholder ถูกต้อง) · FN-30 pass-through ถูกต้อง · FN-40 scope-creep = ไม่มี · ไม่มี block-rule/edge ที่ ✗ → ไม่ถึง BLOCK

เหตุ WARN: FN-09 (view "ภาพรวม" โชว์ทุก version ของ FG) มี UI hook ไม่ครบ — โค้ดคำนวณ `others` แล้วแต่ไม่ render ออกจอ (dead ternary)

---

## Coverage Matrix — FN-01..23

| FN | ต้องทำอะไรได้ | HTML | Evidence (selector/function/บรรทัด) |
|---|---|---|---|
| FN-01 | wizard 2 step + stepper · ไม่มี hint/note | ✓ | `renderForm()` stepper L620-623 (2 ขั้น "ข้อมูลสูตร"/"ส่วนประกอบ") · `nextStep()` L523 / `prevStep()` L534 |
| FN-02 | Step 1 FG combobox portal (ค้น+รูป+code+หน่วย) type FG only | ✓ | `#fgCombo`/`#fgInput` L580-585 · `renderFgOpts()` L465-466 (prodAvatar+code+หน่วย) · `PARENTS=filter type==='FG'` L296 |
| FN-03 | version + ชื่อ + ผลผลิต + out_uom + ★ | ✓ | `#f-ver` L588 · `#f-name` L589 · `#f-outqty` L590 · out_uom auto จาก FG (`selectFg` L484) · toggle ★ L592 → `toggleDefault()` L520 · *หมายเหตุ: out_uom = base uom ของ FG (derived/read-only ไม่มี dropdown แยก) — reflected ตรง §3* |
| FN-04 | Step 2 line editor combobox portal ค้น RM/PM/TR (suggest ลอยไม่ clip) | ✓ | `#lnCombo-i`/`#lnInput-i` L600-604 · `renderLineOpts()` L488-489 · `COMPS=filter RM/PM/TR` L297 · portal `#suggest-portal` L263 |
| FN-05 | qty(>0)+UoM กรองหมวด+scrap%+ลบบรรทัด | ✓ | `#ln-qty-i` L607 · `#ln-uom-i` select `uomsForItem()` L608/461 · `#ln-scrap-i` L609 · `delLine()` btn L610 |
| FN-06 | cost rollup สด Σ(std_cost×qty×(1+scrap%)) · std_cost read-only | ✓ | `lineCost()` L360 · `bomCost()` L361 · line-foot totalCost L613 · std_cost จาก `PMAP[].cost` (ไม่มี input แก้) |
| FN-07 | บันทึกร่าง/บันทึก+เปิดใช้ → DOA null 4 fields + used=0 | ✓ | `saveForm(activate)` L545 · create set `used=0` + `approver_role=null…` L556 · ปุ่ม L629-630 |
| FN-08 | ★ 1/FG ตั้งใหม่ปลดเก่าอัตโนมัติ · badge list+view | ✓ | clear อัตโนมัติ L560 (create) / L564 (edit) · badge-def list L414 · view L646 |
| FN-09 | view "ภาพรวม" โชว์ทุก version ของ FG + ป้ายสูตรหลัก/สถานะ | △ | `others=RAW.filter(...)` L640 คำนวณแล้ว **แต่ L652 `${others.length?\`\`:''}` render ค่าว่างทั้งสองฝั่ง → รายการ version อื่นไม่โผล่จอ** · overview tab แสดงเฉพาะข้อมูลสูตร L642-651 + รูป header L661 |
| FN-10 | แก้ได้ทุก field รวม lines แม้ used>0 | ✓ | ปุ่มแก้ไข `navTo('bom/edit/'+id)` L663 ไม่มี guard used>0 · `openForm('edit')` L504 clone ทั้ง record รวม lines |
| FN-11 | VR-01/03 ไม่เลือก FG · ชื่อว่าง → block+toast | ✓ | `saveForm` VR-01 L548 · VR-03 L552 (toast error) |
| FN-12 | VR-02 version ว่าง/ซ้ำ/parent → block (recheck on save) | ✓ | `saveForm` ว่าง L549 · dup case-insensitive/parent L550-551 (fix recheck OB-8) |
| FN-13 | VR-04/05 lines 0 · qty≤0 → block | ✓ | `validateLines()` lines 0 L536 · qty>0 L540 |
| FN-14 | VR-06/07 component ซ้ำ · component=parent (กัน BOM วน) → block | ✓ | `validateLines()` component=parent L539 · dup component L542 |
| FN-15 | เปลี่ยนวัตถุดิบ → UoM reset base uom ใหม่ + กรองหมวดใหม่ | ✓ | `selectLineItem()` L499 set `uom=p.uom` · `uomsForItem()` re-filter L461 |
| FN-16 | stat 4 ใบ + filter สินค้า/สถานะ + ค้น + sort ทำงานร่วม | ✓ | stats `quickFilter()` L384-387 · filter parent/status L391-392 · search L390 · `sortBy()` L407-409 · `filtered()` รวมทุกตัว L365-372 |
| FN-17 | statusMenu view 3 ค่าทุกทิศ (ไม่มีอนุมัติ) · หลุด active → ★ หลุด | ✓ | `#statusMenu` L666-667 · `setStatus()` L437-441 (`if st!=='active' is_default=false` L439) |
| FN-18 | bulk bar 3 สถานะ+ยกเลิก · select-all thead · แถวไฮไลต์ · หลุด active → ★ หลุด | ✓ | bulkbar L395-403 · `bulkSetStatus()` L430-435 (`is_default=false` L433) · `toggleSelAll()` thead L406/429 · `.is-sel` L411 |
| FN-19 | bulk ลบ confirm บอกยอด/ข้าม · used>0 ไม่ลบ · ไม่มีตัวลบ → disabled | ✓ | `openBulkDelete()` L445 · `confirmBulkDelete()` skip used>0 L449 · modal ยอด L688-691 · `disabled` เมื่อ ids-skip=0 L691 |
| FN-20 | FG รูปใน list+fgCombo+view header · onerror fallback | ✓ | `prodAvatar()` onerror→initials L355-359 · list L413 · combo L466 · view header L661 |
| FN-21 | #95 Overlay Portal (fixed จาก rect · select ปิด · scroll/resize reposition) | ✓ | `.cbx-suggest{position:fixed}` L192 · `placeSuggest()` L467-474 · `reflowSuggest()` scroll/resize L741-746 · select ปิด L484/499 |
| FN-22 | #96 sticky thead · #29 scroll · #97 768-1180 off-canvas · Esc chain | ✓ | sticky thead L108 · `_keepScroll()` L699 (#29) · `@media(max-width:1180px)` sidebar off-canvas L110-116 · Esc chain modal>statusMenu>drawer L725-732 |
| FN-23 | CI Warm Light + Satoshi · SVG icons renderIcons เอง | ✓ | `:root` Warm Light tokens L12-13 · `ICONS`+`renderIcons()` L266-279 (ไม่ใช้ lucide CDN) |
| FN-90 | ลบทุกทางผ่าน confirm เสมอ (bonus) | ✓ | ทางลบเดียว = bulk → modal confirm L445/688 · ไม่มี per-record delete |

## Edge Hooks (§9 PREBRIEF + Central Plan)

| Edge | ทิศ | HTML | Evidence |
|---|---|---|---|
| ← Item Master (F-PDM): FG picker (type FG) + component picker (RM/PM/TR) + std_cost read-only + รูป | in | ✓ | `PARENTS` FG-only L296 · `COMPS` RM/PM/TR L297 · std_cost จาก `PMAP[].cost` (read-only) · img data-URI mock L284-286 · *active-flag ไม่มีใน mock — soft-ref ทุกตัวถือว่า active (ยอมรับได้สำหรับ mock)* |
| ← UoM Master (0.1): line unit dropdown กรองหมวด base-uom วัตถุดิบ (VR-08/BR-06) | in | ✓ | `uomsForItem()` L461 กรองด้วย `uomCat()` L460 · `UOMS` มี `cat` L299-303 |
| → Production/MO (declared-unbuilt): used = MO count = mock delete-guard | out | ✓ | comment `used = count MO (mock · guard ลบ)` L336 · guard ใน `confirmBulkDelete()` L449 · **ไม่มีหน้า MO ถูกสร้าง** — sidebar "ใบสั่งผลิต" L247 เป็น nav placeholder (ไม่มี onclick/route) |
| → Costing (declared): cost rollup ป้อนต้นทุนมาตรฐาน downstream | out | ✓ | `bomCost()`/`lineCost()` L360-361 แสดงใน list+view+form · **ไม่มีหน้า Costing ถูกสร้าง** |

## FN-30 — Edge cases ประกาศ "รอเคาะ" (OQ-BOM-04) · ต้อง pass-through

| กรณี | คาดหวัง = ปล่อยผ่าน | HTML | Evidence |
|---|---|---|---|
| std_cost=0/null (EC-CL-01) | ไม่ block | ✓ ถูกต้อง | `lineCost()` L360 คำนวณปกติ (cost 0 → 0) · seed `FG-1005 cost:0` L286 + b4 ใช้ได้ L324 · ไม่มี validate block |
| scrap 100% (EC-CL-02) | ไม่ block | ✓ ถูกต้อง | `#ln-scrap` `max="100"` L609 อนุญาต 100 · ไม่มี block/warn ประดิษฐ์ |
| FG/component deactivate หลัง active (EC-ST-01/02) | ไม่ flag | ✓ ถูกต้อง | ไม่มี logic ตรวจ deactivate · สูตรยัง valid |

**FN-30 pass-through ถูกต้อง: YES** — HTML ไม่ประดิษฐ์ block/warn ที่ยังไม่เคาะ (ตรงมติ "ปล่อยผ่าน" pending PM/BA)

## FN-40 — Anti Scope-Creep (LOCK) · ต้อง "ไม่มี"

| ห้ามมี | โผล่มั้ย | Evidence |
|---|---|---|
| multi-level/nested BOM | ✗ ไม่มี | `COMPS` = RM/PM/TR เท่านั้น (ไม่รับ FG เป็น component) L297 · `validateLines` block component=parent L539 · single-level |
| approval chain / DOA UI | ✗ ไม่มี | DOA fields = null L556 · modal comment "ไม่ใช้ approve" L683 · ไม่มีปุ่มอนุมัติ (match `approv*` = null placeholder ทั้งหมด) |
| import/export CSV | ✗ ไม่มี | grep import/export/csv = 0 hit ใน UI |
| routing/operation/labor | ✗ ไม่มี | ไม่มี field/หน้า |
| co-product/by-product | ✗ ไม่มี | lines รับ output เดียว |
| per-row (record) delete นอก confirm | ✗ ไม่มี | ลบ record เฉพาะ bulk→confirm · `delLine()` L610 = ลบ line ใน wizard (คือ FN-05 ที่ต้องมี ไม่ใช่ record delete) |
| ★ หลายตัว/FG | ✗ ไม่มี | บังคับ 1/FG (clear อัตโนมัติ L560/564) |
| hint-note | ✗ ไม่มี | ไม่มี `class="note"`/`class="hint"`/`data-tip` ถูก render · toggle-row `<small>` L592 = field description (ยอมรับได้) |

**Scope-creep จาก FN-40: NO** (ไม่มีของต้องห้ามโผล่)

---

## 🟡 Gaps (เรียงตามความเสี่ยง)

### GAP-01 · FN-09 — view "ภาพรวม" ไม่ render รายการ version อื่นของ FG (△ partial)
- **หาย**: view tab "ภาพรวม" ต้องโชว์ทุก version ของ FG นั้น + ป้ายสูตรหลัก/สถานะ (S-03 · §6 View) — ตอนนี้แสดงเฉพาะข้อมูลสูตรตัวเดียว
- **สาเหตุ**: `renderView()` คำนวณ `const others=RAW.filter(...)` (L640) แต่บรรทัด output คือ `${others.length?\`\`:''}` (L652) — ternary render ค่าว่างทั้งสองฝั่ง (dead code · น่าจะลืมใส่ template ตาราง version)
- **แก้ที่**: `f-bom.html` `renderView()` overview branch L652 — เติม template render `others` (เช่น mini-list: ver-tag + badge สูตรหลัก + status pill + ต้นทุน ต่อแต่ละ version) เมื่อ `others.length>0`
- **หลักฐานว่ามี intent**: seed มี FG-1001 2 version (b1 v1 / b2 v2 L309-318) — เคสทดสอบ S-03 มีจริงแต่จอไม่โชว์
- **ผลกระทบ**: ผู้ใช้เปิด view สูตร FG-1001 v1 จะไม่เห็นว่ามี v2 อยู่ → เทียบ version ไม่ได้ (ผลปลายทาง S-03 "เทียบ v1/v2 ได้" ไม่บรรลุ)

## 🟢 ของที่ครบดีเด่น (ยืนยันจากตาราง)
- VR recheck ครบ (FN-11..14 · OB-8) — จุดที่ pack v3.5 เดิมเป็นช่องโหว่ ตอนนี้ `saveForm` enforce VR-01/02/03 + `validateLines` ครบ
- Edge in ทั้ง 2 เส้น (Item Master + UoM) มี UI hook จริง · Edge out ทั้ง 2 เส้นเป็น placeholder ถูกต้อง (ไม่ประดิษฐ์หน้า MO/Costing)
- FN-30 pass-through + FN-40 lock สะอาด — ไม่มี scope creep, ไม่มี block ที่ยังไม่เคาะ

## ⬜ NOT-CHECKED
- (ไม่มี — รอบ 1 ตรวจ HTML ครบทุก item ของ contract)
- รอบ 2 (FRD 05_RULES + testcases) ยังไม่รัน — golden-rule wording / TC ต่อ block-rule จะตรวจใน Step ถัดไปของ pipeline

## 💡 เสนอเข้า graph / brief (ไม่กระทบ verdict)
- Mock `PRODUCTS` ไม่มี field `active` — edge "type FG **active** / component **active**" (BR-03/04) ตรวจ active ไม่ได้ในระดับ UI (soft-ref ถือทุกตัว active). ถ้าต้องการพิสูจน์ active-filter ควรเพิ่ม `active` flag ใน mock master (คงเป็น mock nicety ไม่ใช่ gap — จริง sync F-PDM active-only ตาม OQ-BOM-03)
- CSS `.hint`/`.note` (L46/L180-183) เป็น residual จาก base-kit (นิยามแต่ไม่ถูก render) — เรื่องความสะอาด CSS เป็นงาน `qc-ux-html-checker` ไม่ใช่ coverage gap

## Diff จากรอบก่อน
- (ไม่มี — นี่คือ coverage รอบ 1 ครั้งแรกของ F-BOM)
