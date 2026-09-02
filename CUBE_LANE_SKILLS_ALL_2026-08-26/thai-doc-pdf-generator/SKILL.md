---
name: thai-doc-pdf-generator
description: >
  สร้างเอกสารธุรกรรม/จดหมายทางการไทยเป็น PDF A4 มาตรฐาน 2BSimple จาก input อะไรก็ได้ —
  PR, PO, SO, ใบเสนอราคา, ใบกำกับภาษี, ใบแจ้งหนี้, ใบเสร็จ, ใบส่งของ, ใบลดหนี้,
  หนังสือราชการ, จดหมายธุรกิจ, บันทึกข้อความ, หนังสือรับรอง. CI CUBE NATIVE
  (Navy/Primary/Teal) + ฟอนต์ Sarabun ฝังในไฟล์ — ทุกเอกสาร pattern เหมือนกันเป๊ะ.
  รองรับโลโก้, ตาราง line items, VAT 7%, จำนวนเงินเป็นตัวอักษร, ช่องลายเซ็นสายอนุมัติ,
  เลขผู้เสียภาษี+สำนักงานใหญ่/สาขา, A4 แนวตั้งเสมอ. Output 3 ไฟล์/เอกสาร:
  template.html (Dev bind data ต่อ) + sample.pdf + print-spec.md (แนบ FRD).
  ใช้เมื่อ user พูดถึง "สร้างเอกสาร PDF", "ทำ PO/PR/SO/ใบเสนอราคา/ใบกำกับภาษี",
  "หนังสือราชการ/บันทึกข้อความ", "เอกสาร A4", "ทำ template เอกสาร", "เอกสารทางการไทย",
  "thai-doc-pdf-generator", "ทำเอกสารแนบ FRD", "เอกสารมีโลโก้/ตาราง/ช่องลายเซ็น".
  ใช้ทุกครั้งที่ต้องการเอกสารธุรกรรม/จดหมายทางการเป็น PDF A4 CI เดียวกัน.
---

# Thai Business Document — PDF Generator (A4)

สร้างเอกสารทางการไทยเป็น **PDF A4** ที่ทุกใบใช้ CI + ฟอนต์ + layout pattern เดียวกัน
โดย **lock ความสม่ำเสมอผ่าน build script** — Claude เขียนแค่ `<body>` ที่เหลือ engine จัดให้.

## หลักการ (อ่านก่อนเริ่ม)
- **Claude เขียนเฉพาะ body** (ประกอบจาก `patterns/blocks.md`) → `build_html.py` ฝัง
  head/CI/Sarabun ให้เอง → เอกสารทุกใบเหมือนกันเป๊ะ. **ห้ามเขียน hex สีเอง / ห้ามแก้ base.css ราย doc.**
- เอกสารคือ **ของแนบ FRD** — ทุกครั้งออก print-spec.md คู่เสมอ เพื่อให้ Dev build ลงระบบได้.

## 🔒 Design Rules (locked — base.css บังคับให้แล้ว)
1. **A4 แนวตั้งเสมอ** — ห้าม override ขนาดหน้า
2. **Lean type** — body 9pt / น้ำหนัก 400, เน้น 600 เฉพาะจุด, ไม่ถม 700 ทั้งหน้า
3. **ตารางผอม บรรทัดเดียว** — 1 row = 1 บรรทัด, รหัส/สเปคย่อย = inline `<span class="sub">`
4. **หัวตาราง + ยอดรวมทั้งสิ้น = แถบ navy เข้ม ตัวอักษรขาว** · เนื้อตารางคง minimal (ไม่มีเส้นแนวตั้ง/zebra)
5. **ลายเซ็น + footer ชิดล่างหน้า** — ห่อใน `.doc-bottom` (footer ล่างสุด / ลายเซ็นเหนือ footer)
6. โครงทุก body: `<div class="doc-page"><div class="doc-content">…</div><div class="doc-bottom">…</div></div>`

## Output ต่อ 1 เอกสาร (3 ไฟล์)
1. `[TYPE]_template.html` — master HTML, Sarabun ฝัง base64, เปิด/พิมพ์ได้ทุกที่ (Dev เอาไป bind data)
2. `[TYPE]_sample.pdf` — ตัวอย่าง render A4
3. `[TYPE]_print-spec.md` — เอกสารประกอบ (field map, สูตรคำนวณ, กติกาพิมพ์) สำหรับแนบ FRD/PR/PO

## Workflow

**1) ระบุชนิด + เก็บข้อมูล**
- อ่าน `knowledge/document-types.md` → เลือก type (PR/PO/SO/QO/INV/RC/DO/CN/LT/MEMO/CERT/APPROVAL).
  ถ้า user เล่าเนื้อหา: มีรายการ+ราคา = เอกสารตาราง, เป็นข้อความเล่า = จดหมาย.
- ข้อมูลที่ขาดและจำเป็น → เติม placeholder ที่สมจริง (เลขที่ `PREFIX-2569-NNNNN`, ที่อยู่ตัวอย่าง)
  แล้ว **บันทึกไว้ใน print-spec ว่า field ไหนเป็น placeholder**. อย่าถามทีละข้อถ้าเดาได้.

**2) อ่านมาตรฐาน + blocks**
- `knowledge/design-rules.md` (กฎ R1–R9) + `knowledge/thai-standards.md` (VAT/วันที่ พ.ศ./ลายเซ็น/ใบกำกับภาษี)
- `patterns/blocks.md` (ชิ้นส่วน HTML ทั้งหมด)

**3) เขียน body**
- สร้างไฟล์ body = `<div class="doc-page"><div class="doc-content">…</div><div class="doc-bottom">…</div></div>`
- `.doc-content`: เอกสารตาราง = HEADER→META→PARTIES→ITEMS→(NOTES+TOTALS) · จดหมาย = HEADER→LETTER
- `.doc-bottom`: SIGNATURES (ถ้ามี) แล้ว FOOTER — ถูกดันชิดล่างหน้าอัตโนมัติ
- ตัวเลขเงินทุกช่อง `#,##0.00` + class `num`. จำนวนเงินตัวอักษร: `python scripts/baht_text.py <ยอด>`

**4) build + render**
```bash
cd <skill_dir>
python scripts/build_html.py /path/body.html --title "ใบสั่งซื้อ ..." -o /mnt/user-data/outputs/PO_template.html
python scripts/render_pdf.py /mnt/user-data/outputs/PO_template.html -o /mnt/user-data/outputs/PO_sample.pdf
```

**5) ตรวจสายตา** — rasterize PDF (`pdftoppm -png -r 110 x.pdf prev`) แล้ว `view` ภาพ.
ตรวจ: ล้นหน้าไหม, ตัวเลขชิดขวา, VAT/ยอดถูก, ลายเซ็นครบ. แก้ body แล้ว build ใหม่ถ้าจำเป็น.

**6) print-spec** — คัดลอก `templates/print-spec.template.md` เติมค่าจริง → `[TYPE]_print-spec.md`

**7) present_files** — ส่ง PDF เป็นไฟล์แรก, ตามด้วย HTML + print-spec.

## โลโก้
- มีไฟล์/URL → `<img class="doc-logo" src="...">`. เพื่อให้ PDF self-contained ให้ base64 ก่อน:
  `data:image/png;base64,...` (อ่านไฟล์ → `base64`). ไม่มีโลโก้ → ใช้ `.doc-logo--ph` (ตัวย่อ gradient).

## เพิ่มชนิดเอกสารใหม่
ไม่ต้องสร้าง CSS ใหม่ — เพิ่มแถวใน `knowledge/document-types.md` แล้วประกอบจาก block เดิม.
ถ้าต้อง component ใหม่จริง ๆ → เพิ่ม class ใน `assets/base.css` (ใช้ CI var เท่านั้น) แล้ว doc ทุกใบได้ทันที.

## สิ่งแวดล้อม
- Renderer: Playwright/Chromium (ติดตั้งแล้ว). ฟอนต์ Sarabun อยู่ใน `assets/fonts/`.
- ถ้า `playwright` ไม่พร้อม: `pip install playwright && playwright install chromium`.

## ห้าม
- ❌ เปลี่ยนขนาดหน้าเป็นอย่างอื่นนอกจาก A4
- ❌ เขียน hex สีเองใน body (ใช้ class)
- ❌ ใช้ฟอนต์อื่นแทน Sarabun
- ❌ ส่งมอบโดยไม่มี print-spec คู่


## ⚙️ Lane Mode (feature-lane-runner v2 · S1.8 เมื่อ chip `pdfdoc`)
- Input = `01_PREBRIEF.md` (ชื่อเอกสาร · field header/line/totals · ช่องเซ็น) + `03_DOCCFG_BRIEF.md` (doc_type/เลขรัน) — ห้ามถาม · ข้อมูลบริษัท/ภาษี ใช้ placeholder มาตรฐาน 2BSimple
- Output ลง `03_PDFDOC/`: `template.html` + `sample.pdf` + `print-spec.md` — html-generator-v9 ใช้ `template.html` เดียวกันใน tab **PDF Preview** (Pattern Q · `.a4`) · frd-generator-v6 แนบ `print-spec.md`
- ถ้าเอกสารมีหลาย variant (เช่น ใบกำกับภาษี/ใบส่งของ) → 1 template ต่อ variant · ชื่อไฟล์ `template_<doc_type>.html`
