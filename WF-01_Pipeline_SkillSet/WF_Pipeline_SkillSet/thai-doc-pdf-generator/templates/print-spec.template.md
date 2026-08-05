# PRINT SPEC — {{DOC_NAME}} ({{DOC_TYPE}})

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ feature ที่จะ build เอกสารนี้ลงระบบ
> ไฟล์คู่: `{{TYPE}}_template.html` (master, fonts ฝัง) + `{{TYPE}}_sample.pdf` (ตัวอย่าง A4)

## 1. สรุป
- **ประเภทเอกสาร:** {{DOC_NAME}} / {{DOC_NAME_EN}}
- **ขนาด:** A4 แนวตั้ง (210×297mm), ขอบ 14mm
- **ฟอนต์:** Sarabun (ฝัง base64 ใน HTML — ไม่ต้องพึ่ง network)
- **CI:** CUBE NATIVE (Navy #0B1D3A / Primary #0B5CFF / Teal #00A88E)
- **Renderer ที่ใช้สร้าง PDF:** Playwright/Chromium → `print_background`, `prefer_css_page_size`

## 2. Field Mapping (UI/DB → ช่องในเอกสาร)

| ช่องในเอกสาร | Source (entity.field) | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่เอกสาร | {{...}} | `PREFIX-พ.ศ.-running` | ✓ | running จากระบบ |
| วันที่ | {{...}} | วัน เดือน(ไทย) พ.ศ. | ✓ | |
| ผู้ขาย/ลูกค้า | {{...}} | — | ✓ | |
| รายการ (loop) | {{...}} | — | ✓ | 1 row = 1 line item |
| ราคา/หน่วย, จำนวนเงิน | {{...}} | `#,##0.00` | ✓ | ชิดขวา |
| รวมเป็นเงิน | computed | `#,##0.00` | ✓ | Σ จำนวนเงิน |
| VAT 7% | computed | `#,##0.00` | (เฉพาะกลุ่มขาย) | ฐาน = หลังหักส่วนลด |
| รวมทั้งสิ้น | computed | `#,##0.00` | ✓ | |
| จำนวนเงินตัวอักษร | computed | ไทย | ✓ | ใช้ logic baht_text |
| ผู้ลงนาม (3 ชั้น) | {{...}} | — | ✓ | Maker/Checker/Approver |

## 3. กติกาคำนวณ
- `subtotal = Σ(qty × unit_price)`
- `after_discount = subtotal − discount`
- `vat = round(after_discount × 0.07, 2)`  *(ROUND_HALF_UP)*
- `grand_total = after_discount + vat (− wht ถ้ามี)`
- จำนวนเงินตัวอักษร: port `scripts/baht_text.py` (เอ็ด/ยี่สิบ/ล้าน/สตางค์/ถ้วน)

## 4. กติกาการพิมพ์ (ตาม Design Rules)
- A4 แนวตั้ง · lean type 9pt · หัวตารางเส้นบาง · ลายเซ็น+footer ชิดล่าง (.doc-bottom)
- หัวตารางซ้ำทุกหน้า (`thead { display:table-header-group }`)
- ห้ามตัด row กลาง (`tr { break-inside:avoid }`)
- block ลายเซ็นห้ามขึ้นหน้าใหม่แยกจากเนื้อหา (`break-inside:avoid`)
- เลข running หลายหน้า → footer "หน้า X / N"

## 5. วิธี build ใหม่ (regenerate)
```bash
python scripts/build_html.py BODY.html --title "{{DOC_NAME}}" -o {{TYPE}}_template.html
python scripts/render_pdf.py {{TYPE}}_template.html -o {{TYPE}}_sample.pdf
```
Dev ฝั่งระบบ: เอา `{{TYPE}}_template.html` เป็นต้นแบบ HTML แล้ว bind ข้อมูลตามตาราง §2
จากนั้น render เป็น PDF ด้วย engine ใดก็ได้ที่ honor `@page` + Sarabun (เช่น Chromium/Gotenberg/Puppeteer)

## 6. Checklist ก่อนส่งมอบ
- [ ] A4 พอดี ไม่ล้นหน้า
- [ ] ตัวเลขชิดขวา + `#,##0.00`
- [ ] VAT/ยอดรวม ถูกต้อง + ตัวอักษรตรงยอด
- [ ] เลขผู้เสียภาษี + (สำนักงานใหญ่/สาขา) ครบ (ถ้าเป็นใบกำกับภาษี)
- [ ] ลายเซ็นครบสาย + วันที่
