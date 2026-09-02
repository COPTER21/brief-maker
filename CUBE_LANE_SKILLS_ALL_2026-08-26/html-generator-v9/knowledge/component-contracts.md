# Component Density & Overlay Contracts (#63–#68) — v6.3

> หมวดกฎจาก defect จริงที่ user รายงาน (2026-07-26) เทียบกับระบบ production CUBE 4.0 Core:
> component ติดกัน · list ใหญ่เกิน · search dropdown อ้วน+ไม่ปิด · hint เขียนโต้ง ๆ · dropdown จมจอล่าง
> **Reference มาตรฐาน = ระบบจริง** — ตัวเลขทุกตัวในหมวดนี้วัดจากหน้าจอ production

---

## Rule #63 — List Density Standard (แก้ "list view ใหญ่เกิน")
ตารางรายการ (Pattern A) ยึด density ของระบบจริง:
```css
:root { --row-h: 44px; }
```
- แถวข้อมูล: height 44px (สูงสุด 48 ถ้ามี 2 บรรทัด) — td padding **8px 12px** ห้ามเกิน
- ฟอนต์ใน tbody = `--fs-table` (12.5) · หัวคอลัมน์ 11px uppercase `--c-mute-2`
- แถบ filter/tab: สูง 36px · chip/badge สูง 22–26px · ปุ่มในแถว 30px
- ❌ ห้าม: td padding แนวตั้ง >10px, ฟอนต์ tbody >13px, แถวสูงเกิน 48 — สามตัวนี้คือที่มา "ใหญ่เกิน"
- page ที่เนื้อหลักคือ list: ตารางต้องกินพื้นที่ ≥60% ของ viewport แนวตั้ง (stats/header อย่าเบียด)

## Rule #64 — Breathing Room (แก้ "component ติดกัน")
ระยะห่างขั้นต่ำระหว่าง sibling — ต่ำกว่านี้ = ติดกัน:
| ระหว่าง | ขั้นต่ำ |
|---|---|
| section ↔ section | 24px |
| card ↔ card (grid) | 16px (gap ของ grid — ห้ามใช้ margin ลูก) |
| filter bar ↔ ตาราง | 12px |
| control ในกลุ่มเดียว (ปุ่ม/input แถวเดียว) | 8px |
| label ↔ input | 6px |
| กล่องมี border 2 กล่อง | **ห้ามขอบชนกัน** — ต้องมี gap หรือรวมเป็นกล่องเดียว |
ทุกค่าต้องมาจาก scale #50 · ระยะ "0" ระหว่าง component ที่มองเห็นได้ = FAIL

## Rule #65 — Search Dropdown / Autocomplete Contract (แก้ "อ้วน + บัค")
โครง item บังคับ (ตามระบบจริง — ช่องมอบหมายงาน):
```
[ avatar 28px กลม | หรือวงกลมอักษรย่อ ] [ ชื่อหลัก 13px ]        [ meta ขวา: tag/count ]
                                        [ บรรทัดรอง 12px · truncate 1 บรรทัด ]
```
- **2 บรรทัดต่อ item เท่านั้น** — ห้ามยัดตาราง/detail หลายแถว ("อ้วน" = FAIL)
- เมนู: กว้าง = trigger · `max-height: 320px` + `overflow-y: auto` (บังคับมีเสมอ) · item padding 8px 12px
- มีช่อง search ในเมนูเมื่อรายการ >10 · empty state "ไม่พบ…" ในเมนู (เมนูห้ามหายเฉย ๆ)
- **ปิดเมื่อ: เลือก / คลิกนอก / Esc / Tab-blur** — ครบทั้ง 4 ไม่มีข้อยกเว้น (ดู #68)
- พิมพ์ค้นหา: debounce 200ms · แสดง "กำลังค้นหา…" ระหว่างรอ (ห้ามเมนูค้างของเก่า)

## Rule #66 — Overlay Position Awareness (แก้ "dropdown จมจอล่าง")
overlay ทุกชนิดที่ยึด trigger (dropdown / select / autocomplete / menu / date picker) ต้องวัดก่อนเปิด:
```js
function positionMenu(trigger, menu){
  const r = trigger.getBoundingClientRect();
  const spaceBelow = window.innerHeight - r.bottom - 12;
  const spaceAbove = r.top - 12;
  const h = Math.min(menu.scrollHeight, 320);
  if (spaceBelow < h && spaceAbove > spaceBelow){
    menu.classList.add('drop-up');                 // เปิดขึ้นบน
    menu.style.maxHeight = Math.min(h, spaceAbove) + 'px';
  } else {
    menu.classList.remove('drop-up');
    menu.style.maxHeight = Math.min(h, spaceBelow) + 'px'; // ไม่พอ = หด + scroll ภายใน
  }
}
```
- ใช้ util นี้ (หรือ logic เทียบเท่า) **ทุกจุดที่เปิดเมนู** — ห้ามเปิดดิ่งลงอย่างเดียว
- `.drop-up { bottom:100%; top:auto; margin-bottom:4px }` คู่กับ default ล่าง
- เมนูใน drawer/modal: stacking context ของ overlay แม่ครอบอยู่แล้ว — ใช้ `var(--z-dropdown)` ภายในได้

## Rule #67 — Hint → Tooltip (แก้ "hint เขียนโต้ง ๆ")
- ❌ ห้ามคำอธิบาย/hint ยาว (>60 ตัวอักษร) โชว์เปลือย ๆ บนฟอร์ม/ใต้ field
- ✅ ใช้ไอคอน ⓘ (lucide `info` 14px สี `--c-mute-2`) ต่อท้าย label + tooltip ตอน hover
  (spec tooltip ตาม Rule #33: พื้น charcoal ตัวขาว max-width 340px มี arrow)
- **ข้อยกเว้นที่ต้องโชว์เสมอ:** error message · validation แดง · คำเตือน destructive · empty state
- placeholder ใน input = คำสั้น ("ค้นหาชื่อ / ตำแหน่ง / แผนก…") ไม่ใช่ย่อหน้าอธิบาย

## Rule #67.1 — Hint Opt-in Only (v7.1 — "ตอนพัฒนาไม่ต้องเอา hint ขึ้น")
- **Default = ไม่ gen hint/ⓘ ใด ๆ เลย** — ทั้ง tooltip icon, help text ใต้ field, คำอธิบาย section
  — จะมีได้ต่อเมื่อ FRD/Brief **ระบุ explicit** ว่า field/section นั้นต้องมีคำอธิบาย เท่านั้น
- ยกเว้นที่ต้องมีเสมอ (ไม่ใช่ hint): error message · validation แดง · คำเตือน destructive (`.note.is-warn`
  ผูก action จริง) · empty state
- placeholder สั้นใน input ยังใช้ได้ตามเดิม (ไม่นับเป็น hint)
- เหตุผล: hint ที่ AI แต่งเองตอน gen = เดา spec → สร้าง noise ให้ reviewer และรั่วเป็นข้อความ
  ที่ไม่มีใน requirement — ถ้าอยากได้ hint ให้เป็น decision ของ BA ใน FRD ไม่ใช่ของ generator
- audit: grep `hint-i` / `data-tip` — ทุกตัวที่พบต้อง trace กลับ requirement ได้ ไม่มี source = FAIL

## Rule #68 — Overlay Discipline (แก้ "บัคไม่ปิดเอง")
สาเหตุจริงของ "ไม่ปิด" 90% = แต่ละเมนูเขียน handler เอง + `stopPropagation` เหมา — บังคับโครงเดียว:
```js
// global เดียวทั้งไฟล์ — ประกาศครั้งเดียว
document.addEventListener('click', e => {
  document.querySelectorAll('[data-overlay].open').forEach(m => {
    if (!m.contains(e.target) && !m._trigger?.contains(e.target)) closeOverlay(m);
  });
});
```
- ทุกเมนู/dropdown ติด `data-overlay` + จดทะเบียน trigger — **ห้าม element ไหนเขียน outside-click เอง**
- เปิดตัวใหม่ → ปิดตัวเก่าก่อนเสมอ (เปิดพร้อมกันได้ทีละตัว)
- ❌ ห้าม `e.stopPropagation()` แบบเหมาบน container ใหญ่ — คือตัวการที่ global handler ไม่เห็น click
- Esc chain ตามกฎเดิม: ปิดชั้นบนสุดก่อน (tooltip → dropdown → modal → drawer)
- เลือกค่าแล้ว: ปิดเมนู + คืน focus ให้ trigger

## Rule #74 — Drawer Tab Bar Contract (defect: tab กระจุก+เส้นซ้อน)
- tab bar ใช้ class จาก BASE-KIT **เท่านั้น** (`.drawer-tabs` > `.drawer-tab`) — ห้ามประดิษฐ์ tab เอง
  (kit ทำ flush + เส้นเดียว + active merge ขอบให้แล้ว — ที่พังคือคนไม่ใช้)
- ❌ ห้ามมี border/hr/เส้นใด ๆ ประชิดใต้ tab bar อีกเส้น — section แรกหลัง tab ห้ามมี border-top
- tab bar กว้างเต็ม drawer, padding ข้าง = padding ของ body (24px) — เริ่มชิดซ้ายเสมอกัน
- tab เกินความกว้าง → scroll แนวนอนเฉพาะ tab bar (ห้ามตกบรรทัด)

## Rule #75 — Form Composition ใน Drawer (defect: spacing โดด/สถานะลอย)
- โครง: field ใน section เดียวกัน = **grid 2 คอลัมน์ gap 16×20** · ระหว่าง section = 24px มีหัวข้อคั่น
  — ห้ามช่องว่างแนวตั้งเกิน 24px ระหว่าง element ที่มองเห็น (ช่องโหว่ง ๆ = FAIL)
- **ห้ามมี orphan element** — ทุก field/ป้ายต้องสังกัด section ที่มีหัวข้อ · สถานะปัจจุบันของ entity
  แสดงเป็น pill ใน **drawer header** (identity block #72) ไม่ใช่ field ลอยท้ายฟอร์ม
- textarea เต็มแถว = `grid-column:1/-1` · toggle group เรียงชิดกัน gap 8 ไม่กระจาย

## Rule #76 — No Horizontal Overflow (defect: scrollbar ล่าง)
- drawer/modal body: `overflow-x` ต้องไม่เกิด — ทุกลูก `max-width:100%` · grid ใช้ `minmax(0,1fr)`
  ห้าม fixed width เกินความกว้าง container · table ใน drawer ครอบ `.table-wrap` (scroll เฉพาะตาราง)
- Render Gate ตรวจ: screenshot drawer แล้วต้องไม่เห็น scrollbar แนวนอนที่ขอบล่าง

## Rule #77 — Mock Completeness + Compound Widget (defect: ข้อมูลขาด/หน่วยนับจืด)
- ทุก section ใน detail/form ต้องมี **ข้อมูลตัวอย่างจริงครบ** — ห้าม placeholder ว่าง
  (รูปภาพ: มี thumb จริง ≥1 · เอกสาร: ไฟล์ชื่อจริง · หน่วยนับ: factor กรอกแล้ว)
- **widget ความสัมพันธ์/อัตราแปลง (conversion, ratio, mapping) ต้องมี 3 ชิ้น:**
  1. แถวสมการอ่านได้: `1 BOX = 12 ชิ้น` (ตัวเลขจริงจาก mock)
  2. ตัวอย่างประกอบ callout: "ถ้ามี 144 ชิ้นในคลัง ระบบมองเป็น 12 BOX"
  3. chip บทบาทต่อหน่วย (ซื้อ/ขาย/หลัก/เก็บสต๊อก) — ไม่ใช่ dropdown เปล่า ๆ เรียงกัน
- หลักคิด: prototype ที่ช่องว่าง = dev เดา spec เอง — ทุกช่องต้องสาธิตค่าที่ถูกต้อง

## Rule #78 — Filter Zone Spec (ละเอียด — วัดได้ทุกข้อ)
**78.1 โครง 1 แถวเท่านั้น** สูง 36px: `[search][select…][select…][ล้างตัวกรอง]` เรียง flex gap 12
— โซนกรองทั้งหมดสูงรวม ≤52px (แถว 36 + margin) · ❌ filter แตกเป็น ≥2 แถว = BLOCK
**78.2 ความกว้าง:** search `flex:1;min-width:220;max-width:420` · select `width` ตามเนื้อหา
**140–240px ตายตัว** — ❌ select ไม่จำกัดความกว้าง/เต็มแถวโดดเดี่ยว = BLOCK (defect หลักที่เจอ)
**78.3 ล้างตัวกรอง:** `btn-ghost btn-sm` **ต่อท้ายในแถวเดียวกัน** — ❌ ลอยแถวตัวเอง/มุมขวาโดด ·
แสดงเฉพาะเมื่อมี filter active
**78.4 ห้ามช่องว่างแนวตั้ง** >12px ภายในโซนกรอง · ห้ามครอบด้วยกล่อง border ที่ padding แนวตั้ง >12px
**78.5 นับที่เดียว:** มี stat row (คลิกกรอง) → **ห้ามมี chip row นับซ้ำ** — เลือกอย่างเดียว:
stat row (แนะนำเมื่อ ≤6 มิติ) หรือ chip row (เมื่อสถานะเยอะ) — มีทั้งคู่ = BLOCK
**78.6 ระยะโซน:** stat row → filter = 16px · filter → ตาราง = 12px
**78.7 ตัวกรอง = select dropdown เท่านั้น** (defect F-UOM) — ❌ segmented/pill-group ในโซน filter
(segmented สงวนไว้สลับ view เช่น ตาราง↔การ์ด) · เมนู filter dropdown ต้องมี **พื้นทึบ
`background:#fff` + border + shadow + `z-index:var(--z-dropdown)`** — โปร่งใส/จมใต้ thead = BLOCK
**78.8 chip ใน td:** บรรทัดเดียว · `vertical-align:middle` · สูง 22-24px · อยู่กึ่งกลางแนวตั้งแถวเสมอ

## Rule #79 — Create-Mode Progressive States (defect: widget โชว์ placeholder ประหลาด)
- compound widget ตอนยังไม่มีข้อมูล → แสดง **empty prompt** (กรอบ dashed + คำชวน 1 บรรทัด)
  ❌ ห้าม render แถวสมการที่มี "(ยังไม่เลือกหน่วย)" / factor ว่าง
- กรอกข้อมูลแล้ว → ค่อยโชว์แถวสมการ + example callout (progressive disclosure)
- role chips มี**สีตาม semantic** (ซื้อ=ฟ้า ขาย=เขียว เก็บสต๊อก=ส้ม) — ไม่ใช่ outline เทาเรียงกัน
- wizard step ที่เนื้อน้อย → เติม example/best-practice note ให้จอไม่โล่ง (ดู erp-ux-patterns)

## Rule #80 — Entity Avatar (defect: รูปแตก 17 จุด)
- prototype ห้ามมี `<img>` placeholder/ไอคอนรูปแตก — เซลล์ entity ใช้ **initial block สีตามประเภท**
  (RM/FG/SV/PK/EX — โทนอ่อนของ semantic) ตาม `blocks/avatar-cell.html`
- มีรูปจริงเมื่อไหร่ค่อยแทน initial — โครง markup เดียวกัน

## Rule #81 — UI Copy ห้ามรั่วศัพท์ภายใน (defect F-UOM detail)
- ❌ ห้ามโชว์บนจอ: edge/rule id (`E-044`, `GR-XXX`, `XR-`), ศัพท์ plan/pipeline
  ("hook", "คาย", "bucket model", "self-slice", "node", "contract")
- section การเชื่อมโยง → เขียนเป็นภาษาผู้ใช้: "ถูกใช้อยู่ใน: สินค้าคงคลัง (132 รายการ)" ·
  รายละเอียดเชิง technical เก็บใน FRD ไม่ใช่บนจอ · traceability ใส่เป็น comment ใน code ได้
- ยกเว้น: รหัสที่ user รู้จักจริง (รหัสสินค้า, เลขเอกสาร)

## Rule #68.1 — Overlay ระบบเดียว (defect: drawer เด้งเปิด-ปิด)
- เปิด/ปิด overlay ผ่าน `openOverlay()/closeOverlay()` ของ kit **เท่านั้น** — ❌ เขียน toggle/
  classList เอง คู่กับ global handler = สองระบบชนกัน (ปิดแล้ว bubble ไปเปิดใหม่ = อาการเด้ง)
- ปุ่ม X/ปิด: เรียก `closeOverlay(el)` ตรง ๆ — trigger เดิมห้าม re-fire จาก event เดียวกัน

## Rule #73.1 — ทุก tab ต้องมีชีวิต
- ทุก tab ต้องมี pane จับคู่ + switch ทำงาน + มีเนื้อหา (อย่างน้อย empty state ที่ตั้งใจ)
- ❌ tab ที่กดแล้วเงียบ = BLOCK · Render Gate ต้อง**คลิกทุก tab + screenshot ทุก pane**

## Rule #82 — Behavior จาก Kit เท่านั้น (กุญแจ one-shot)
- **JS ใน reference ถูก strip ทิ้งแล้วทั้งหมด** — mirror ได้เฉพาะ markup/CSS composition
  behavior ทุกอย่าง (overlay/tab/toast/sort/filter) เขียนด้วย kit utils + pattern มาตรฐานของ skeleton
- ก่อนส่งไฟล์: ทุก `onclick` ต้องชี้ function ที่มีจริง · ทุก `getElementById` ต้องมี id จริง
  (audit v7: `undefined_handlers` / `missing_ids` — tab ตาย/ปุ่มใบ้ตายตั้งแต่ static แล้ว)
- ทุก interactive element ต้องถูก "เดินครบ" ใน Self-Review รอบ 2: เปิด→ปิด→เปิดซ้ำ overlay ทุกตัว /
  คลิกทุก tab / submit ทุก form / Esc ทุกชั้น — ติ๊กพร้อมหลักฐาน

## Rule #83–#92 — Document Line Editor Contract (Pattern B2) — v6.11 ⭐
บังคับกับทุกเอกสารธุรกรรมที่มี line items (PR/PO/QT/SO/GRN/INV/CN/DN/RTV) —
source of truth: `patterns/B2_document-line-editor.md` + `references/drawer-standard/line-editor.{css.html,js.txt}`

| # | กฎ | ตรวจยังไง | verdict |
|---|---|---|---|
| 83 | grid 8 คอลัมน์ + ความกว้างตรง contract (`#32 · สินค้า min260 · จำนวน66 · หน่วย130 · ราคา116 · ส่วนลด76 · ภาษี92 · เงิน124 · action70`) | นับ `<th>` + grep width | BLOCK |
| 84 | "ยอดสุทธิทั้งหมด" reconcile กับผลรวมที่คำนวณจาก `lines[]` จริง | render + คำนวณเทียบ | BLOCK |
| 85 | `vat_mode` mutually exclusive — ไม่มี state ที่ add+included พร้อมกัน | grep การ set vat_mode | BLOCK |
| 86 | ฐาน WHT = ยอดก่อน VAT (แถว `included` ถอด VAT ออกจากฐานก่อน) | อ่าน `renderLineSummary` | BLOCK |
| 87 | ขยายแถวได้ทีละแถวเดียว (`expandedLineId` เดี่ยว) | render + คลิก 2 แถว | WARN |
| 88 | ทุกช่องเงิน/จำนวนมี `.num` (tabular-nums) | grep cell เงินที่ไม่มี `.num` | WARN |
| 89 | เปลี่ยน UoM แล้วราคา cascade (`setLineUnit` → `itemUnitPrice`) | render + เปลี่ยนหน่วย | BLOCK |
| 90 | hard control ต้อง **disable ปุ่มส่งจริง** (flag `createWizard._*` → footer) ไม่ใช่เตือนเฉย ๆ | render เคสเกิน limit | BLOCK |
| 91 | item combobox มี keyboard nav ↑↓/Enter/Esc เท่ากับ combobox อื่น (= Rule #94 ข้อ 3) | grep `onItemKey` + กดจริง | WARN |
| 92 | แถวว่าง (ไม่มี `item_code`) บล็อกการไป step ถัดไป | render + กดถัดไป | BLOCK |

หมายเหตุ: ทุก field ที่อ้าง master ใน line editor และในฟอร์มรอบ ๆ อยู่ใต้ **Rule #94**
(iron-rules Group 18) ด้วยเสมอ — combobox pattern เดียวกันทั้งไฟล์

## ⭐⭐ Reference-First Rule (v6.8 — เหนือ Block-First)
`templates/reference/` = **ไฟล์ทั้งตัวที่ user อนุมัติแล้ว** (Golden Reference — CSS heal แล้ว):

| Archetype | ไฟล์ | ใช้กับ |
|---|---|---|
| Master data (drawer form) | `product-master.reference.html` | master ทั่วไป field ไม่เยอะ (UOM/VENDOR/COA…) |
| Master data (fullpage create) | `master-fullpage.reference.html` | master ข้อมูลเยอะ — landing + หน้า create เต็ม (ไม่ใช้ drawer) |
| Operational console | `console-operation.reference.html` | งานปฏิบัติการ (PICKING/PACKING/STOCK-COUNT…) |
| **General standard (default)** | `general-standard.reference.html` | **feature ทั่วไปทุกตัวที่ไม่เข้า archetype อื่น** — สี/token ยึด CI เรา ไม่ยึดไฟล์ |

เลือก archetype: LANE_BRIEF ระบุ > เดาจากลักษณะ feature (field >20 หรือ multi-section หนัก → fullpage):
- feature type ตรงกับ reference (เช่น master data ↔ product-master.reference.html)
  → **mirror ทั้งโครง**: ลำดับ section · composition ทุกหน้า · widget design · ระยะ — bind data ใหม่เท่านั้น
- inline style ใน reference = อ่านเพื่อเข้าใจ design แต่ตอน gen ต้องแปลงเป็น class (#56/#69)
- reference ขัดกับกฎเรา → กฎชนะ (reference heal แล้วแต่ inline ยังมี — อย่าลอก inline)
- feature type ไม่มี reference → ใช้ Block-First + anatomy ตามเดิม
- user vibe ไฟล์ใหม่แล้วพอใจ → เพิ่มเข้า reference/ (ผ่านการ heal ก่อนเสมอ)

## ⭐ Block-First Rule (สำคัญสุดของ v6.7)
สถานการณ์ที่มี block ใน `templates/blocks/` (toolbar-filter · uom-editor · avatar-cell — จะเพิ่มเรื่อย ๆ)
→ **ลอก block แล้ว bind data เท่านั้น ห้ามออกแบบเอง** — เหตุผลเดียวกับ BASE-KIT:
กฎบรรยายให้ "ถูก" ได้ แต่ "หน้าตาแบบที่ user รับ" ต้องลอกของจริง — block คือของจริงที่กลั่นจากไฟล์ vibe ที่ผ่านตาแล้ว

---

### Self-check เพิ่มใน pre-flight (ต่อจาก #60)
10. เมนู custom ทุกตัวมี `max-height` + `overflow` (#65) และเรียก `positionMenu` (#66)
11. มี global outside-click handler ตัวเดียว + ไม่มี `stopPropagation` เหมา (#68)
12. grep ข้อความ hint เปลือย >60 chars นอก whitelist (#67)
13. td padding แนวตั้ง ≤10px · tbody font ≤13px (#63)
14. ไม่มี border-box 2 กล่องขอบชนกัน (#64)
15. tab ใช้ class kit เท่านั้น + ไม่มีเส้นซ้อนใต้ tab bar (#74)
16. ฟอร์ม: ไม่มี orphan element / ช่องว่าง >24px / สถานะอยู่ header (#75)
17. drawer ไม่มี horizontal overflow (#76) · ทุก section มี mock ครบ + conversion widget มีสมการ+ตัวอย่าง (#77)
18. toolbar แถวเดียว + counts ที่เดียว (#78) · create widget เป็น progressive ไม่มีสมการ placeholder (#79)
19. ไม่มี img placeholder — ใช้ avatar initial สีตามประเภท (#80) · เคสที่มี block → ลอก block (Block-First)
20. combobox ใน scroll container (.table-wrap / drawer body / B2 grid) ใช้ `portalMenu` — ไม่มีเมนู absolute ค้างใน DOM ที่โดน clip (#95)
21. ทุก `selectX` ที่ autofill field อื่น มี `clearX` ที่ล้างครบชุด + confirm ก่อนล้าง line items (#94.1)
22. หน้า list ใช้ `.page-fill` + `.table-wrap` scroll ภายใน + `.table-foot` ติดล่าง — ตารางชิดขอบล่าง viewport (#96)
23. viewport 1024px: drawer ไม่ล้นจอ (`min(…,100vw)`) · ไม่มี body horizontal scrollbar · sidebar off-canvas/rail (#97)
24. ไม่มี hint/ⓘ ที่ไม่มี source ใน FRD (#67.1) · stepper: dot แนวเดียว + ช่องไฟเท่า + CSS จาก kit เท่านั้น (#47.1)

---

## v9.0 — Rule #83 re-scoped to B2 v2 (SO reference)
- #83 grid = `.tbl.line-tbl` 9 ช่อง widths 26/—/64/92/92/78/72/104/54 (เดิม PR 32/260/66/130/116/76/92/124/70 = legacy ห้ามใช้ gen)
- #83.1 แถวขยาย = lean 1-line (VAT segmented · % · หมายเหตุ · [ราคาระบบ]) — BLOCK ถ้ามีแถว 2
- #83.2 ส่วนลดท้ายบิล = card toggle + segmented ฿/% + input 180px suffix — WARN
- ดู Group 20 ใน iron-rules.md (#98–#101) สำหรับ Document Archetype ทั้งชุด
