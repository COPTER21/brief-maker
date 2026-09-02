# Pattern B2 — Document Line Editor **v2** (CUBE Warm Light) ⭐ v9

> **⭐ AUTHORITATIVE STANDARD — v9 re-locked to `references/document-archetype/_SOURCE_so-reference.html`
> (F-SALES-SO v2).** v8 เคยล็อกกับ PR reference (grid 8 คอลัมน์กว้าง 32/260/66/130/116/76/92/124/70) —
> **v9 เปลี่ยน canonical เป็น SO layout (compact + lean 1-line advanced row)** ตามมติ user 2026-08-25:
> "หน้าตาราง + add สินค้า · การกรอก item · ส่วนลด · VAT ต้อง fix ให้เหมือนกันเป๊ะ เผื่อไปทำ PR/PO อื่นในอนาคต"
>
> ทุกเอกสารที่มี "รายการสินค้า/บริการ" ใน CUBE — PR, PO, Quotation, SO, GRN, Invoice, Credit Note,
> Debit Note, RTV — **ต้องใช้ pattern นี้เสมอ** ห้ามออกแบบตารางกรอกรายการขึ้นใหม่เอง
>
> **Verbatim source of truth (copy from here — do not improvise):**
> - `references/document-archetype/_SOURCE_so-reference.html` — ไฟล์ทำงานเต็ม เปิด browser ดูเป้าหมาย 100% (step 3 ของ create drawer)
> - `references/document-archetype/line-editor-v2.js.txt` — JS ทั้งชุด 25 defs (`createBlankLine → linesTableView`)
> - `references/document-archetype/doc-archetype.css.html` — CSS ที่ต้องมี (`.line-tbl .free-row .hard-warn .line-expand-panel …`)
> - (legacy v8 PR reference ยังอยู่ที่ `references/drawer-standard/` — **ห้ามใช้ generate ใหม่** เก็บไว้เทียบเท่านั้น)
>
> **Rule:** ลอกโครงสร้าง, class, inline style, ลำดับคอลัมน์, ลำดับยอดรวม, และพฤติกรรม **ตรงตัว**
> ปรับได้เฉพาะ *field set / label / entity name / mock data* และ *hard control + optional blocks ที่เป็นของ business นั้น*
> — ห้ามปรับ shell, grid contract, VAT engine, discount engine, หรือ totals order

**B2 คือ step 3 ของ Pattern Q** (transaction document archetype) — Q ให้ shell (header + stepper + footer), B2 ให้ body ของ step "รายการสินค้า"

---

## 🎯 When to Use

✅ เอกสารธุรกรรมที่มี line items + ยอดรวม (PR / PO / QT / SO / GRN / INV / CN / DN / RTV) — เป็น step 3 ของ Pattern Q
✅ ทุกที่ที่ผู้ใช้ต้อง "ค้นหาสินค้า → เลือกหน่วย → ใส่จำนวน → ได้ยอด"
✅ ทุกที่ที่มีภาษี (VAT / WHT) หรือส่วนลดท้ายบิล

❌ ตาราง read-only ของรายการ (ใช้ `linesTableView` ใน view tab / step 5)
❌ ตาราง master list ที่ไม่มียอดรวม (ใช้ Pattern A)
❌ ฟอร์มที่ไม่มี line item (ใช้ Pattern B / Q โดยตัด step 3)

---

## 🏗️ Grid Contract v2 — 9 ช่อง (8 คอลัมน์ + action) — ห้ามเพิ่ม/ลด/สลับ/เปลี่ยนความกว้าง

`<table class="tbl line-tbl" style="font-size:12.5px">` ใน `.card` — `.line-tbl th/td { padding-left/right: 6px }`

| # | Header | width (th) | align | เนื้อหา (td) |
|---|---|---|---|---|
| 1 | `#` | `26px` (+`padding-left:6px`) | center | ลำดับแถว สี mute |
| 2 | `สินค้า` | *(auto — ที่เหลือ)* `padding-right:12px` | left | **item combobox** `.item-combo[data-line-id]` > `<input class="input" style="height:32px;font-size:12.5px;padding:0 10px">` แสดง `CODE — ชื่อ` |
| 3 | `จำนวน` | `64px` | right | `<input type=number min=1 step=1 class="input num" style="height:30px;font-size:12.5px;text-align:right;padding:0 8px">` |
| 4 | `หน่วย` | `92px` | left | `<select class="select" style="height:30px;font-size:12px;padding:0 6px;width:100%">` ถ้า `units.length>1` / `<span 12px mute>` ถ้าหน่วยเดียว |
| 5 | `ราคา/หน่วย` | `92px` | right | `<input type=number min=0 step=0.01 class="input num" 30px>` · `disabled` ถ้า `!CFG.allowPriceOverride` · `border-color: var(--c-warning)` เมื่อ `l.override` |
| 6 | `ส่วนลด %` | `78px` | right | `<input type=number min=0 max=100 step=0.01 class="input num" 30px>` |
| 7 | `ภาษี` | `72px` | center | **tax badge** `taxBadgeV(l)` — pill 11px มีจุด 4px: ไม่คิด (mute) / `VAT n%` (purple=Orange) / `NET n%` (primary) — คลิกไม่ได้ แก้ในแถวขยาย |
| 8 | `จำนวนเงิน` | `104px` | right | `฿${formatMoney(lineTotal)}` 13px/600 navy tabular-nums |
| 9 | *(no header)* | `54px` | center | `inline-flex gap:2px`: [chevron-down/up] toggle expand (active = bg primary) → [trash-2] danger — ทั้งคู่ `.btn.btn-ghost.sm padding:0 6px` |

- ทุก `td` `vertical-align: middle` · แถวที่ขยายอยู่ `background: var(--c-primary-08)`
- **แถวของแถม** (`l.is_free`) = `<tr class="free-row">` (พื้น teal-08) แสดง pill `ของแถม` + ชื่อ + note, ราคา 0.00, ลด `-`, ยอด `฿0.00` สี teal, ช่อง action = ข้อความ `อัตโนมัติ` (แก้/ลบไม่ได้)
- **Drawer ต้องเป็น `.drawer-panel.wide` (1290px)** — ข้อยกเว้นเดียวของ Rule #11
- จอ <1180: grid scroll แนวนอนใน wrap ของตัวเอง — ห้ามยุบคอลัมน์ (Rule #97)

### หัว step 3 (บนตาราง) — ล็อก

```
[list icon] รายการสินค้า — {ชื่อคู่ค้า}                       [refresh-cw คำนวณราคาใหม่] secondary sm · [plus เพิ่มรายการ] primary sm
   hint 11.5px mute: "ราคาจาก … · คลิกแถวเพื่อเปิดตัวเลือกขั้นสูง (VAT · หมายเหตุ · ราคาที่ระบบเสนอ)"
```
ปุ่ม `คำนวณราคาใหม่` มีเฉพาะ feature ที่มี price engine (SO/QT) — PR/PO/GRN ตัดได้ · `เพิ่มรายการ` ต้องมีเสมอ

### ลำดับ block ใต้ตาราง — ล็อก

```
1. <table.line-tbl>                                   (บังคับ)
2. stockAlert()   card ขอบ warning — สต๊อกไม่พอ         (optional: SO/QT/DN)
3. pricingPanel() card 3 คอลัมน์ ① บัญชีราคา ② ข้อตกลง ③ โปรฯ+คูปอง   (optional: SO/QT)
4. ส่วนลดท้ายบิล  card: หัว (percent icon + title + pill "อัตโนมัติ · src" + toggle)
                  → เปิด: แถว off-white = segmented [จำนวนเงิน (฿)|เปอร์เซ็นต์ (%)] + input 180px suffix ฿/%   (บังคับ — ปิดได้ด้วย toggle)
5. [หัก ณ ที่จ่าย  card toggle → select %]              (optional: PR/PO/INV ฝั่งจ่าย — SO ไม่มี)
6. <div id="line-summary-wrap">renderLineSummary()</div>   (บังคับ)
```

## 📦 Line Model (data contract)

```js
{
  id: 'L' + Date.now() + rand,   // client-side only
  item_code: '', item_name: '',
  qty: 1,
  unit: '-',                      // ต้อง match uom ใน item.units[]
  unit_price: 0,
  discount_pct: 0,
  vat_mode: 'none',               // 'none' | 'add' | 'included'  ← mutually exclusive
  vat_pct: 7,
  note: '',
  // v2 (SO) — optional ตาม business:
  price_src: '', ta_src: '', promo_disc: 0,   // ที่มาของราคา (price engine)
  _sysPrice: 0, override: false,             // ราคาที่ระบบเสนอ / ผู้ใช้แก้มือ → ต้องมีเหตุผลใน step 5
  is_free: false,                            // ของแถม → free-row (แก้/ลบไม่ได้)
  discount_mode: 'percent', discount_amt: 0, // ส่วนลดเป็นจำนวนเงิน (ถ้า feature ต้องการ)
}
```

**Item master ต้องมี `units[]`** — นี่คือสัญญาที่ทำให้ dropdown หน่วยทำงาน:

```js
{ code: 'SUG-001', name: 'น้ำตาลทรายขาว', vat_group: 'NONE', units: [
    { uom: 'กก.', price: 26.75, is_default: true },
    { uom: 'กระสอบ 50กก.', price: 1250.00 },
    { uom: 'ตัน', price: 24500.00 } ] }
```

`vat_group` (`NONE` / `VAT7`) เป็นตัวกำหนด `vat_mode` เริ่มต้นตอนเลือกสินค้า —
สินค้าที่ยกเว้นภาษี (สินค้าเกษตร) จะได้ `none` อัตโนมัติ ผู้ใช้ override ได้ในแถวขยาย

---

## 🧮 VAT Engine — 3 โหมด mutually exclusive

`calcLineVat(l)` เป็น single source of truth ห้ามคำนวณ VAT ที่อื่น

| mode | ความหมาย | vatAmount | lineTotal |
|---|---|---|---|
| `none` | ไม่มี VAT | `0` | `netAmount` |
| `add` | ราคายังไม่รวม VAT | `netAmount × vat%` | `netAmount × (1 + vat%)` |
| `included` | ราคารวม VAT แล้ว (NET) | `netAmount × vat% / (1 + vat%)` — **คำนวณย้อน** | `netAmount` (ไม่เปลี่ยน) |

โดย `netAmount = qty × unit_price × (1 − discount_pct/100)`

`migrateLine()` แปลง schema เก่า (`vat_enabled` + `net_enabled`) → `vat_mode`
ให้อัตโนมัติ **ต้องเรียกทุกครั้งก่อนคำนวณ** — เก็บไว้แม้ feature ใหม่ไม่มีข้อมูลเก่า

---

## 💰 Totals Block v2 — `renderLineSummary()` — ลำดับตายตัว

```
[hard-warn]  ← ถ้า hard control เตือน (บนสุด นอก card)
.card
  .card-head 12/18: [calculator] "สรุปยอด (N รายการ [+ ของแถม M])"        11px mute: "ราคาจาก …"
  .card-body 12/18  <table width:100% 13px>
    1. ราคาก่อน VAT                       ฿before   (600)
    2. ภาษีมูลค่าเพิ่ม (VAT)   สี purple    +฿vat
    ── border-top soft ──
    3. ยอดรวมหลัง VAT                     ฿after    (600)
    4. [หัก ภาษี ณ ที่จ่าย X%]           −฿wht     (เฉพาะ feature มี WHT · ฐาน = ก่อน VAT)
    5. [ส่วนลดท้ายบิล (n%) · src] mute    −฿ebAmt   (เมื่อ endbill.enabled)
    6. [คูปอง CODE] teal                   −฿coupon  (เมื่อมี)
    ── border-top 2px ──
    7. ยอดสุทธิทั้งหมด  14px/700           ฿grand    16px/700 สี primary
    8. [บรรทัด hook ของ business]  11.5px  เช่น "เครดิตคงเหลือหลังใบนี้ ฿…" (teal/danger)
```

`totals(doc)` = single source: `before` = Σ(net หรือ net−vat ถ้า included) · `vat` = Σ vatAmount · `after = before+vat` ·
`ebAmt` = amount หรือ `after×%` · `grand = max(0, after − ebAmt − coupon)`
**ฐาน WHT = ยอดก่อน VAT เสมอ** (แถว `included` ถอด VAT ก่อน)

### Read-only ใน view/step 5 — `linesTableView(s)`
ตาราง `.tbl` 9 คอลัมน์: # · สินค้า (ชื่อ + pill ของแถม/แก้ราคา + บรรทัดรอง code · src · note) · หน่วย · จำนวน · ราคา/หน่วย · ส่วนลด % · ภาษี · **รวม (Net)** · **รวม (Gross)** primary
`<tfoot>` off-white: ราคาก่อน VAT / VAT n% (purple) / [ส่วนลดท้ายบิล] / [คูปอง] / ยอดสุทธิ

---

## 🔍 Item Combobox — สัญญาการค้นหา (instance ของ Rule #94)

- `<input class="input">` ใน `.item-combo` — พิมพ์แล้วค้นทั้ง `code` และ `name`
- แสดงค่าเป็น `CODE — ชื่อสินค้า` เมื่อเลือกแล้ว
- `onfocus` → เปิด suggest list ทันที (ไม่ต้องพิมพ์)
- `oninput` → กรอง + ไฮไลต์ substring ด้วย `<mark>`
- เลือกแล้ว → `applyItemToLine()` เซ็ต `item_code`, `item_name`, `unit` (default uom),
  `unit_price` (ราคาของ uom นั้น), `vat_mode` (จาก `vat_group`) ในคราวเดียว
- เปลี่ยน `<select>` หน่วย → `setLineUnit()` **cascade ราคาใหม่อัตโนมัติ**

> ✅ **v6.11:** item combobox มี keyboard nav ครบแล้ว (`onItemKey` — ↑↓/Enter/Esc,
> Esc ปิด list ก่อนแล้ว drawer ค่อยปิดตาม Esc chain) + drop-up ตาม Rule #66
> เมื่อแถวอยู่ใกล้ขอบล่างจอ — ปิด gap OQ-B2-01 ใน reference แล้ว
> ทุก combobox ในไฟล์ (BR / employee / vendor / item) จึงอยู่ใต้ contract เดียวกัน
> ของ **Rule #94** — ดู `references/drawer-standard/master-combobox.js.txt`

---

## 📂 Expandable Row v2 — "lean 1-line advanced row" (ล็อก)

- ขยายได้ **ทีละแถวเดียว** (`createWizard.expandedLineId`)
- `<tr class="line-expand-panel-anchor" data-line-id>` พื้น `var(--c-primary-08)` · `td colspan=9 padding: 0 16px 10px 44px`
- ข้างใน `.line-expand-panel-inner` = การ์ดขาว ขอบ primary-12 · `padding:10px 12px` · **flex แถวเดียว** `gap:14px` wrap · 12px:
  ```
  VAT  [ไม่คิด | บวกเพิ่ม | รวมแล้ว (NET)]  [n]% = ฿vat   │  หมายเหตุ [input flex:1 min 220]  │  ระบบเสนอ ฿x (src → ta · โปรฯ n%) [undo-2 ใช้ราคาระบบ]   [chevron-up]
  ```
  - segmented = `inline-flex bg off-white border radius var(--r) padding:2px` · ปุ่ม active `bg primary / white` 11.5px/600
  - input % แสดงเฉพาะ `vat_mode !== 'none'` (28px × 58px) + ข้อความ `% = ฿…` สี purple
  - divider `1px × 22px` bg border ระหว่างกลุ่ม
  - "ระบบเสนอ" + ปุ่ม `ใช้ราคาระบบ` แสดงเฉพาะ feature ที่มี price engine — ถ้าไม่มี ตัดกลุ่มนี้ (คง VAT + หมายเหตุ)
- animation: เข้า `line-expand-slide` 220ms / ออก `line-collapse-slide` 200ms (`toggleLineExpand` ใส่ `.line-collapse-panel` ก่อน render)
- ห้าม rename selector 3 ตัว (`.line-expand-panel-anchor` `.line-expand-panel-inner` `.line-collapse-panel`)
- **ห้ามใส่ field เพิ่มเป็นแถวที่ 2** — ถ้าต้องเพิ่ม (เช่น lot/expiry ของ GRN) ให้ต่อในแถวเดียวกันด้วย divider หรือย้ายไป modal

---

## 💸 Discount Engine (ล็อก — สูตรเดียว)

ระดับบรรทัด: `discount_pct` (default) หรือ `discount_mode:'amount'` + `discount_amt` (cap ≤ subtotal) — คำนวณใน `calcLineVat` เท่านั้น
ระดับใบ: `endbill {enabled, mode:'amount'|'percent', value, src}` — `src` = ที่มาอัตโนมัติ (ข้อตกลง/โปรฯ); แก้มือ → `src=''` + audit
คูปอง (`couponAmt`) หักหลัง end-bill · `grand = max(0, after − ebAmt − coupon)`

---

## ⌨️ updateLine — focus preservation (ล็อก)

`updateLine()` render ทั้ง drawer แล้ว **คืน focus + caret** ให้ input ที่พิมพ์อยู่ (จับด้วย `oninput` string + `selectionStart`) —
ห้ามเปลี่ยนเป็น partial update ที่ทำให้ยอดรวม/ badge ไม่ sync · `endbill.value` ใช้ `updateLineSummaryOnly()` (render เฉพาะ summary) ได้

---

## ⚙️ Toggle Blocks (ยืมจาก Pattern F)

**หักภาษี ณ ที่จ่าย:** toggle → เผย `<select>` % (1/2/3/5)
**ส่วนลดท้ายบิล:** toggle → เผย mode switch (จำนวนเงิน / เปอร์เซ็นต์) + ช่องค่า

ทั้งคู่ใช้ `.section-row` เป็นหัว + `.toggle > .toggle-slider` มาตรฐาน
**ปรับได้ตาม business:** feature ที่ไม่มี WHT (เช่น GRN) ตัด block นี้ออกได้
แต่ block ที่เหลือต้องคง layout เดิม

---

## 🚦 Hard Control Hook (business-pluggable)

`renderLineSummary()` มีจุดเสียบ hard control ก่อน `return`:

```js
const overBudget = !!(selBr && grandTotal > selBr.remaining + 0.0001);
createWizard._overBudget = overBudget;   // ← footer อ่านตัวนี้ไป disable ปุ่มส่ง
```

**นี่คือส่วนที่แต่ละ feature เปลี่ยนได้** — PR เช็คงบคงเหลือของใบปลดอายัด,
PO เช็คยอดคงเหลือของ PR, GRN เช็คจำนวนคงเหลือของ PO ฯลฯ

แต่ **สัญญา 3 ข้อนี้ห้ามเปลี่ยน:**
1. แถบเตือนอยู่ **บนสุด** ของ summary card (`overWarn` มาก่อน `<div class="card">`)
2. ใช้พื้น `rgba(239,68,68,0.08)` + ขอบ `rgba(239,68,68,0.25)` + icon `alert-triangle`
3. ตั้ง flag บน `createWizard._*` เพื่อให้ footer **disable ปุ่มส่งจริง** —
   ห้ามเตือนอย่างเดียวแล้วปล่อยให้กดผ่าน (นั่นคือ soft control ไม่ใช่ hard control)

Epsilon `+ 0.0001` กันปัญหา float ห้ามตัดทิ้ง

---

## ✅ ปรับได้ / ❌ ห้ามแตะ

| ปรับได้ตาม business | ห้ามแตะเด็ดขาด |
|---|---|
| label คอลัมน์ (`สินค้า` → `บริการ`) | จำนวน/ลำดับ/ความกว้างคอลัมน์ (contract v2) |
| ตัด optional block (stockAlert / pricingPanel / WHT) | segmented VAT + discount engine + `updateLine` focus logic |
| item master + `vat_group` mapping | `calcLineVat()` สูตร 3 โหมด |
| ตัด WHT / end-bill block ที่ไม่ใช้ | ลำดับ 6 บรรทัดของ totals |
| เงื่อนไข hard control | รูปแบบ + การ disable ปุ่มของ hard control |
| เพิ่ม field ในแถวขยาย | selector 3 ตัวของแถวขยาย |
| default `vat_pct` (7 → อื่น) | `migrateLine()` |
| จำนวน step ของ wizard | `.drawer-panel.wide` |

---

## 🗺️ Reuse Map

| เอกสาร | ใช้ B2 | ต่างจาก PR ตรงไหน |
|---|---|---|
| **PO** | ✅ เต็ม | hard control = ยอดคงเหลือของ PR · เพิ่มคอลัมน์ *ในแถวขยาย* ไม่ใช่ใน grid |
| **Quotation** | ✅ เต็ม | ไม่มี hard control · มักเปิด end-bill discount default |
| **SO** | ✅ เต็ม | hard control = credit limit ลูกค้า |
| **GRN** | ✅ ลด | ตัด WHT + end-bill · `unit_price` เป็น read-only · hard control = qty คงเหลือของ PO |
| **Invoice / CN / DN** | ✅ เต็ม | CN/DN: `qty` เป็นลบได้ → `min` ของ input ต้องเปลี่ยน |
| **RTV** | ✅ ลด | เหมือน GRN แต่ qty ผูกกับยอดที่รับจริง |

---

## 🔬 QC Checklist (Rule #83–#92 — ลงทะเบียนใน `knowledge/component-contracts.md` แล้ว, qc-ux Sync Read)

| # | กฎ | verdict ถ้าพลาด |
|---|---|---|
| 83 | grid ต้องมี 9 ช่อง (8 คอลัมน์+action) + ความกว้างตรง contract v2 (26/—/64/92/92/78/72/104/54) + `.line-tbl` | BLOCK |
| 83.1 | แถวขยายเป็น lean 1-line (VAT segmented · % · หมายเหตุ · [ราคาระบบ]) — ห้ามแถว 2 | BLOCK |
| 83.2 | ส่วนลดท้ายบิล = card toggle + segmented ฿/% + input 180px suffix | WARN |
| 84 | ยอดในบรรทัด "ยอดสุทธิทั้งหมด" = ผลรวมที่คำนวณจาก `lines[]` จริง (reconcile ได้) | BLOCK |
| 85 | `vat_mode` ต้อง mutually exclusive — ห้ามมี state ที่ add + included พร้อมกัน | BLOCK |
| 86 | ฐาน WHT = ยอดก่อน VAT (แถว `included` ต้องถอด VAT ก่อน) | BLOCK |
| 87 | ขยายแถวได้ทีละแถวเดียว | WARN |
| 88 | ทุกช่องเงิน/จำนวน ต้องมี `.num` (tabular-nums) | WARN |
| 89 | เปลี่ยน UoM ต้อง cascade ราคาใหม่ | BLOCK |
| 90 | hard control ต้อง disable ปุ่มส่งจริง ไม่ใช่เตือนอย่างเดียว | BLOCK |
| 91 | item combobox ต้องมี keyboard nav ↑↓/Enter/Esc เท่ากับ combobox อื่นในฟอร์ม | WARN |
| 92 | แถวว่าง (ไม่มี `item_code`) ต้องบล็อกการไปขั้นถัดไป | BLOCK |
