# thai-doc-pdf-generator

สร้างเอกสารธุรกรรม/จดหมายทางการไทยเป็น **PDF A4** ที่ทุกใบใช้ CI + ฟอนต์ + layout เดียวกัน
(PR, PO, SO, ใบเสนอราคา, ใบกำกับภาษี, ใบเสร็จ, ใบส่งของ, ใบลดหนี้, จดหมาย, บันทึกข้อความ ฯลฯ)

- **CI:** CUBE NATIVE (Navy #0B1D3A / Primary #0B5CFF / Teal #00A88E) — ตรงกับ `html-generator-v3`
- **ฟอนต์:** Sarabun (มาตรฐานเอกสารราชการไทย) ฝัง base64 → PDF เหมือนกันทุกเครื่อง ไม่พึ่ง network
- **Renderer:** Playwright/Chromium → A4 แนวตั้ง, ขอบ 14mm

## โครงสร้าง
```
SKILL.md                         router + workflow (อ่านก่อน)
assets/base.css                  master stylesheet (CI + anatomy ทั้งหมด) — ห้ามแก้ราย doc
assets/fonts/Sarabun-*.ttf       ฟอนต์ฝังเวลา build
patterns/blocks.md               ชิ้นส่วน HTML (copy → ประกอบ body)
knowledge/document-types.md      ทะเบียนชนิดเอกสาร + field
knowledge/thai-standards.md      VAT / พ.ศ. / ลายเซ็น / ใบกำกับภาษี
scripts/build_html.py            body → self-contained HTML (ฝัง CI+font)
scripts/render_pdf.py            HTML → PDF A4
scripts/baht_text.py             จำนวนเงิน → ตัวอักษรไทย
templates/print-spec.template.md เอกสารประกอบแนบ FRD
examples/                        PO + Memo ตัวอย่าง (HTML/PDF/body)
```

## ใช้งานเร็ว
```bash
python scripts/build_html.py body.html --title "ใบสั่งซื้อ ..." -o PO_template.html
python scripts/render_pdf.py PO_template.html -o PO_sample.pdf
python scripts/baht_text.py 218922       # → สองแสนหนึ่งหมื่น...บาทถ้วน
```

## Output ต่อเอกสาร (3 ไฟล์)
`[TYPE]_template.html` (master ให้ Dev bind data) · `[TYPE]_sample.pdf` (ตัวอย่าง) · `[TYPE]_print-spec.md` (แนบ FRD)
