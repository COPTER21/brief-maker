# Pattern B2 — Document Line Editor (CUBE Warm Light)

> **⭐ AUTHORITATIVE STANDARD (locked to `_SOURCE_line-editor-reference.html`).**
> ทุกเอกสารที่มี "รายการสินค้า/บริการ" ใน CUBE — PR, PO, Quotation, SO, GRN,
> Invoice, Credit Note, Debit Note, RTV — **ต้องใช้ pattern นี้เสมอ** ห้ามออกแบบ
> ตารางกรอกรายการขึ้นใหม่เอง
>
> **Verbatim source of truth (copy from here — do not improvise):**
> - `references/drawer-standard/_SOURCE_line-editor-reference.html` — ไฟล์ทำงานเต็ม เปิด browser ดูเป้าหมาย 100%
> - `references/drawer-standard/line-editor.css.html` — CSS ที่ต้องมี
> - `references/drawer-standard/line-editor.js.txt` — JS ทั้งชุด (21 top-level defs)
>
> **Rule:** ลอกโครงสร้าง, class, inline style, ลำดับคอลัมน์, ลำดับยอดรวม, และ
> พฤติกรรม **ตรงตัว** ปรับได้เฉพาะ *field set / label / entity name / mock data*
> และ *hard control ที่เป็นของ business นั้น* — ห้ามปรับ shell, grid contract,
> VAT engine, หรือ totals order

**B2 คือส่วนขยายของ Pattern B** (create/edit drawer wizard) ไม่ใช่ pattern เดี่ยว —
B ให้ shell (header + stepper + footer), B2 ให้ body ของ step "รายการ"

---

## 🎯 When to Use

✅ เอกสารธุรกรรมที่มี line items + ยอดรวม (PR / PO / QT / SO / GRN / INV / CN / DN / RTV)
✅ ทุกที่ที่ผู้ใช้ต้อง "ค้นหาสินค้า → เลือกหน่วย → ใส่จำนวน → ได้ยอด"
✅ ทุกที่ที่มีภาษี (VAT / WHT) หรือส่วนลดท้ายบิล

❌ ตาราง read-only ของรายการ (ใช้ Pattern C/G view drawer)
❌ ตาราง master list ที่ไม่มียอดรวม (ใช้ Pattern A)
❌ ฟอร์มที่ไม่มี line item (ใช้ Pattern B ล้วน)

---

## 🏗️ Grid Contract — 8 คอลัมน์ (ห้ามเพิ่ม/ลด/สลับ)

| # | Header | width | align | เนื้อหา |
|---|---|---|---|---|
| 1 | `#` | `32px` (+`padding-left:8px`) | center | ลำดับแถว |
| 2 | `สินค้า` | `min-width:260px` | left | **item combobox** + `.tbl-meta` code + note indicator |
| 3 | `จำนวน` | `66px` | right | `<input type=number min=1 step=1>` |
| 4 | `หน่วย` | `130px` | left | `<select>` UoM (ถ้าสินค้ามีหลายหน่วย) / text ถ้ามีหน่วยเดียว |
| 5 | `ราคา/หน่วย` | `116px` | right | `<input type=number min=0 step=0.01>` |
| 6 | `ส่วนลด %` | `76px` | right | `<input type=number min=0 max=100 step=0.01>` |
| 7 | `ภาษี` | `92px` | center | **tax badge** (คลิกไม่ได้ — แก้ในแถวขยาย) |
| 8 | `จำนวนเงิน` | `124px` | right | ยอดสุทธิของแถว `.num` |
| 9 | *(no header)* | `70px` | center | ปุ่มขยาย (chevron) + ปุ่มลบ |

**คอลัมน์ 4 กว้าง 130px เพราะต้องรองรับ `<select>` หน่วย** — ถ้า feature ไหน
สินค้ามีหน่วยเดียวทั้งหมด ยังคง 130px ไว้ อย่าบีบ (กัน layout กระโดดเวลาเพิ่มหน่วยทีหลัง)

**Drawer ต้องเป็น `.drawer-panel.wide` (1290px)** — B2 เป็นข้อยกเว้นเดียวของ
Rule #11 (920/680) เพราะ 8 คอลัมน์ + แถวขยายไม่พอที่ 920px
`.wide` ถูกประกาศแยกไว้แล้ว ห้ามไปแก้ค่า base `.drawer-panel` เป็น 1290

---

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

## 💰 Totals Block — ลำดับตายตัว 6 บรรทัด

```
1. รวมยอด (N รายการ)          = Σ ราคาก่อน VAT
2. ภาษีมูลค่าเพิ่ม (VAT)        = Σ vatAmount
3. รวมยอดหลัง VAT             = (1) + (2)
4. หัก ภาษี ณ ที่จ่าย X%        = (1) × X%      ← ฐาน = ก่อน VAT เสมอ
5. ส่วนลดท้ายบิล               = จำนวนเงิน หรือ (3) × %
6. ยอดสุทธิทั้งหมด             = (3) − (4) − (5)
```

**กฎที่พลาดบ่อย:** ฐาน WHT คือยอด**ก่อน** VAT ไม่ใช่ยอดหลัง VAT
สำหรับแถว `included` ต้องถอด VAT ออกก่อนเข้าฐาน (`netAmount − vatAmount`)

บรรทัด 4, 5 แสดงเฉพาะเมื่อ toggle เปิด · บรรทัด 6 เป็น `.num` ตัวหนา สีเข้ม เสมอ

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

## 📂 Expandable Row (ยืมจาก Pattern E)

- ขยายได้ **ทีละแถวเดียว** (`createWizard.expandedLineId`)
- แถวขยายเป็น `<tr class="line-expand-panel-anchor">` พื้น `var(--c-primary-08)`
- ข้างในเป็นการ์ดขาว `.line-expand-panel-inner` — มี VAT mode selector,
  `vat_pct`, และ `note`
- animation: เข้า `line-expand-slide` 220ms / ออก `line-collapse-slide` 200ms
- ห้าม rename selector 3 ตัวนี้ — `toggleLineExpand()` query ด้วย selector ตรง

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
| label คอลัมน์ (`สินค้า` → `บริการ`) | จำนวน/ลำดับ/ความกว้างคอลัมน์ |
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
| 83 | grid ต้องมี 8 คอลัมน์ + ความกว้างตรง contract | BLOCK |
| 84 | ยอดในบรรทัด "ยอดสุทธิทั้งหมด" = ผลรวมที่คำนวณจาก `lines[]` จริง (reconcile ได้) | BLOCK |
| 85 | `vat_mode` ต้อง mutually exclusive — ห้ามมี state ที่ add + included พร้อมกัน | BLOCK |
| 86 | ฐาน WHT = ยอดก่อน VAT (แถว `included` ต้องถอด VAT ก่อน) | BLOCK |
| 87 | ขยายแถวได้ทีละแถวเดียว | WARN |
| 88 | ทุกช่องเงิน/จำนวน ต้องมี `.num` (tabular-nums) | WARN |
| 89 | เปลี่ยน UoM ต้อง cascade ราคาใหม่ | BLOCK |
| 90 | hard control ต้อง disable ปุ่มส่งจริง ไม่ใช่เตือนอย่างเดียว | BLOCK |
| 91 | item combobox ต้องมี keyboard nav ↑↓/Enter/Esc เท่ากับ combobox อื่นในฟอร์ม | WARN |
| 92 | แถวว่าง (ไม่มี `item_code`) ต้องบล็อกการไปขั้นถัดไป | BLOCK |
