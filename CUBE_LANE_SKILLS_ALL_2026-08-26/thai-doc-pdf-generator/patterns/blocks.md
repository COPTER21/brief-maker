# Document Blocks — คลังชิ้นส่วน HTML (copy → ประกอบเป็น body)

> Claude เขียน **เฉพาะ body** โดยประกอบจาก block ด้านล่าง แล้วให้ `build_html.py`
> ฝัง head/CI/font ให้เอง → ทุกเอกสารหน้าตาเหมือนกันเป๊ะ

## 🔒 DESIGN RULES (locked — ทุกเอกสารต้องตาม)
1. **A4 แนวตั้งเสมอ** (กำหนดใน base.css — ห้าม override)
2. **Lean type** — body 9pt น้ำหนัก 400, เน้นด้วย 600 เฉพาะที่จำเป็น, ห้ามถม 700 ทั้งหน้า
3. **ตารางผอม บรรทัดเดียว** — 1 row = 1 บรรทัด, รหัส/สเปคย่อยใส่ inline `<span class="sub">` (ขึ้น `·` ให้เอง)
4. **หัวตาราง = แถบ navy เข้ม ตัวอักษรขาว** · เนื้อตารางคง minimal (ไม่มีเส้นแนวตั้ง/zebra) รับข้อมูลได้มาก
5. **ลายเซ็น + footer ชิดล่างหน้าเสมอ** — ห่อไว้ใน `.doc-bottom` (footer ล่างสุด, ลายเซ็นเหนือ footer)
6. **ห้ามเขียน hex สีเอง** ใน body — ใช้ class จาก base.css เท่านั้น

## 📐 โครงหน้า (บังคับ)
```html
<div class="doc-page">
  <div class="doc-content">
    <!-- เนื้อหาทั้งหมด: HEADER / META / PARTIES / ITEMS / TOTALS หรือ LETTER -->
  </div>
  <div class="doc-bottom">
    <!-- SIGNATURES (ถ้ามี) แล้วตามด้วย FOOTER — กลุ่มนี้ถูกดันชิดล่างหน้าอัตโนมัติ -->
  </div>
</div>
```
- 1 `.doc-page` = 1 หน้า A4. เนื้อหายาวเกิน → Chromium ตัดหน้าให้ และ `.doc-bottom` ลงล่างสุดของหน้าสุดท้าย
- ลำดับเอกสารตาราง (ใน .doc-content): HEADER → META → PARTIES → ITEMS → (NOTES+TOTALS)
- ลำดับจดหมาย (ใน .doc-content): HEADER → LETTER

---

## B1 · HEADER
```html
<div class="doc-head">
  <div class="doc-head__brand">
    <!-- โลโก้จริง: <img class="doc-logo" src="data:image/png;base64,..."> -->
    <div class="doc-logo doc-logo--ph">2B</div>
    <div>
      <div class="doc-org__name">ชื่อบริษัท จำกัด</div>
      <div class="doc-org__line">ที่อยู่เต็มบรรทัดเดียว ...</div>
      <div class="doc-org__line">โทร. ... อีเมล ...</div>
      <div class="doc-org__tax">เลขประจำตัวผู้เสียภาษี 0105560012345 (สำนักงานใหญ่)</div>
    </div>
  </div>
  <div class="doc-head__title">
    <div class="doc-title">ใบสั่งซื้อ</div>
    <div class="doc-title__en">Purchase Order</div>
    <div class="doc-copy">ต้นฉบับ</div>
  </div>
</div>
```

## B2 · META STRIP
```html
<div class="doc-meta">
  <div class="doc-meta__item"><span class="doc-meta__k">เลขที่</span><span class="doc-meta__v">PO-2569-00142</span></div>
  <div class="doc-meta__item"><span class="doc-meta__k">วันที่</span><span class="doc-meta__v">3 มิถุนายน 2569</span></div>
</div>
```

## B3 · PARTIES (1–2 กล่อง)
```html
<div class="parties">
  <div class="party">
    <div class="party__label">ผู้ขาย / Vendor</div>
    <div class="party__name">ชื่อคู่ค้า จำกัด</div>
    <div class="party__line">ที่อยู่เต็มบรรทัดเดียว ...</div>
    <div class="party__line">เลขผู้เสียภาษี ... โทร. ... ผู้ติดต่อ: ...</div>
  </div>
  <div class="party"> ... </div>
</div>
```
กล่องเดียว = ใส่ `.party` อันเดียว. Label เปลี่ยนตามเอกสาร (ผู้ขาย/ผู้ซื้อ/ลูกค้า/เรียกเก็บจาก/ส่งมอบ).

## B4 · ITEMS TABLE (บรรทัดเดียว/แถว)
```html
<table class="items">
  <thead>
    <tr>
      <th class="col-no">#</th>
      <th>รายการ / รายละเอียด</th>
      <th class="col-qty num">จำนวน</th>
      <th class="col-unit ctr">หน่วย</th>
      <th class="col-price num">ราคา/หน่วย</th>
      <th class="col-amt num">จำนวนเงิน</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="col-no">1</td><td>ชื่อสินค้า<span class="sub">รหัส / สเปคย่อย</span></td><td class="num">20</td><td class="ctr">ตัว</td><td class="num">4,500.00</td><td class="num">90,000.00</td></tr>
  </tbody>
</table>
```
- เงิน/จำนวน → class `num` (ชิดขวา) + format `#,##0.00`. ไม่ใช่เงิน → `ctr`
- รหัส/สเปค → `<span class="sub">` (อยู่ในบรรทัดเดียวกับชื่อ, ขึ้น `·` ให้อัตโนมัติ)
- หัวตารางซ้ำทุกหน้า + row ไม่ถูกตัดกลาง (จัดการใน base.css แล้ว)
- ตารางไม่มีราคา (เช่น PR/DO) → ตัด `col-price`/`col-amt` + ข้าม TOTALS

## B5 · TOTALS + NOTES (ซ้าย-ขวา)
```html
<div class="foot-grid">
  <div class="foot-left">
    <div class="notes">
      <div class="notes__title">เงื่อนไขและหมายเหตุ</div>
      <ol><li>...</li></ol>
    </div>
  </div>
  <div class="totals">
    <div class="totals__row"><span class="k">รวมเป็นเงิน</span><span class="v">219,750.00</span></div>
    <div class="totals__row totals__row--rule"><span class="k">ส่วนลด</span><span class="v">0.00</span></div>
    <div class="totals__row"><span class="k">ภาษีมูลค่าเพิ่ม 7%</span><span class="v">15,382.50</span></div>
    <div class="totals__grand"><span class="k">จำนวนเงินรวมทั้งสิ้น</span><span class="v">235,132.50</span></div>
  </div>
</div>
<!-- จำนวนเงินตัวอักษร = เต็มความกว้าง อยู่ใต้ foot-grid -->
<div class="baht-text"><span class="baht-text__k">จำนวนเงิน (ตัวอักษร)</span><b>(สองแสนสามหมื่นห้าพัน...บาทห้าสิบสตางค์)</b></div>
```
- คอลัมน์ totals แคบ (60mm) ชิดขวา · จำนวนเงินตัวอักษรแยกออกมาเต็มกว้าง อ่านชัด
baht-text: `python scripts/baht_text.py <ยอดรวม>`. WHT → เพิ่ม row "หัก ณ ที่จ่าย X%".

## B6 · SIGNATURES (อยู่ใน .doc-bottom)
```html
<div class="signs">
  <div class="sign">
    <div class="sign__line"></div>
    <div class="sign__paren">(...........................................)</div>
    <div class="sign__role">ผู้จัดทำ</div>
    <div class="sign__name">ตำแหน่ง</div>
    <div class="sign__date">วันที่ ........./........./.........</div>
  </div>
  <!-- ทำซ้ำ: ผู้ตรวจสอบ, ผู้อนุมัติ (2–4 ช่อง) -->
</div>
```
ใบเสนอราคา 2 ช่อง · จดหมาย/บันทึก 0 ช่อง (ใช้ letter__close แทน) · DO 2 ช่อง (ผู้ส่ง/ผู้รับ)

## B7 · FOOTER (อยู่ใน .doc-bottom, ล่างสุด)
```html
<div class="doc-footer">
  <span>เอกสารนี้จัดทำโดยระบบ CUBE NATIVE</span>
  <span>หน้า 1 / 1</span>
</div>
```

## B8 · OFFICIAL LETTER / MEMO (สารบรรณ — อยู่ใน .doc-content)
หัวกระดาษใช้ B1 แบบ **โลโก้ชิดซ้าย ไม่มี title ขวา** (สำหรับหนังสือภายนอก). บันทึกข้อความ = ใส่ title "บันทึกข้อความ" ขวาได้.
```html
<div class="doc-head">
  <div class="doc-head__brand">
    <div class="doc-logo doc-logo--ph">2B</div>
    <div>
      <div class="doc-org__name">บริษัท ... จำกัด</div>
      <div class="doc-org__line">ที่อยู่ ...</div>
    </div>
  </div>
</div>

<div class="letter">
  <!-- ที่ (ซ้าย) + ส่วนราชการ/ที่อยู่ (ขวา) -->
  <div class="letter__refrow">
    <div class="letter__ref">ที่ ทบ ๐๑๐๖/ว ๐๑๔๒</div>
    <div class="letter__agency">บริษัท ... จำกัด<br>ที่อยู่ย่อ ...</div>
  </div>

  <!-- วันที่ กึ่งกลาง (ไม่มีคำว่า "วันที่" นำ) -->
  <div class="letter__date">๓ มิถุนายน ๒๕๖๙</div>

  <!-- หัวเรื่อง — hanging indent -->
  <div class="letter__field"><span class="lbl">เรื่อง</span><span class="val"><b>หัวข้อเรื่อง</b></span></div>
  <div class="letter__field"><span class="lbl">เรียน</span><span class="val">ผู้รับ ...</span></div>
  <div class="letter__field"><span class="lbl">อ้างถึง</span><span class="val">หนังสือ ... (ถ้ามี)</span></div>
  <div class="letter__field"><span class="lbl">สิ่งที่ส่งมาด้วย</span><span class="val">เอกสารแนบ ... (ถ้ามี)</span></div>

  <!-- เนื้อหา -->
  <div class="letter__body">
    <p>ย่อหน้านำ ... นั้น</p>
    <p>เนื้อความ ...</p>
    <p>จึงเรียนมาเพื่อโปรดทราบและพิจารณาดำเนินการต่อไป</p>
  </div>

  <!-- คำลงท้าย + ลายเซ็น ชิดขวา -->
  <div class="letter__close">
    <div>ขอแสดงความนับถือ</div>
    <div class="sp"></div>
    <div class="nm">(ชื่อผู้ลงนาม)</div>
    <div class="pos">ตำแหน่ง</div>
  </div>
</div>
```
**เจ้าของเรื่อง** วางใน `.doc-bottom` (ล่างซ้าย) เหนือ footer:
```html
<div class="doc-bottom">
  <div class="letter__owner">ฝ่าย/ส่วนงาน<br>โทร. ... โทรสาร ... อีเมล ...</div>
  <div class="doc-footer"><span>เอกสารนี้จัดทำโดยระบบ CUBE NATIVE</span><span>หน้า ๑ / ๑</span></div>
</div>
```
- ใช้ **เลขไทย** (๐–๙) ตามแบบราชการ · เรื่อง = ตัวหนา · ฟิลด์ wrap แบบ hanging indent อัตโนมัติ
- **บันทึกข้อความ (ภายใน):** ใส่ title "บันทึกข้อความ" ขวาใน B1 + เพิ่มฟิลด์ "ส่วนงาน" ใน refrow — โครงเนื้อหาเดียวกัน

---

## CI quick-ref (ใช้ผ่าน class แล้ว)
- หัวตาราง = แถบ navy เข้ม font ขาว · ยอดรวมทั้งสิ้น = แถบ navy เข้ม font ขาว
- label/accent = `--c-primary` · โลโก้ placeholder = navy→teal gradient
- tag สถานะ: `.tag--info / --ok / --warn / --danger`
