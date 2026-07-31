# PRINT SPEC — ใบสั่งซื้อ (Purchase Order / PO)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD ของ F-PO-001
> ไฟล์คู่ (4 ชุดตามรูปแบบภาษี): `PO_VAT_*`, `PO_NoVAT_*`, `PO_Discount_*`, `PO_WHT_*` (template.html + sample.pdf)

## 1. สรุป
- **ประเภทเอกสาร:** ใบสั่งซื้อ / Purchase Order
- **ขนาด:** A4 แนวตั้ง (210×297mm), ขอบ 14mm
- **ฟอนต์:** Sarabun (ฝัง base64 ใน HTML — ไม่พึ่ง network)
- **CI:** CUBE NATIVE (Navy #0B1D3A / Primary #0B5CFF / Teal #00A88E)
- **Renderer:** Playwright/Chromium (`print_background`, `prefer_css_page_size`)
- **หมายเหตุ:** template เดียวกัน 1 โครง — รูปแบบภาษีต่างกันที่ **ส่วนยอดรวม (TOTALS)** เท่านั้น Dev ใช้ template ใดก็ได้แล้ว bind block totals ตามชนิดภาษีของเอกสารจริง

## 2. รูปแบบเอกสาร 4 ชุด (ตามการคิดภาษี/ส่วนลด)

| ชุด | ไฟล์ | กรณีใช้ | บล็อก TOTALS ที่แสดง |
|---|---|---|---|
| **VAT 7%** | `PO_VAT_*` | สินค้า/บริการคิด VAT ปกติ (เพิ่มนอกราคา) | รวมเป็นเงิน · ส่วนลด · VAT 7% · รวมทั้งสิ้น |
| **ไม่มี VAT** | `PO_NoVAT_*` | ผู้ขายไม่จด VAT / รายการยกเว้น VAT | รวมเป็นเงิน · ส่วนลด · ภาษีมูลค่าเพิ่ม = **ยกเว้น** · รวมทั้งสิ้น |
| **ส่วนลด + VAT** | `PO_Discount_*` | มีส่วนลดการค้า แล้วคิด VAT จากยอดหลังหักส่วนลด | รวมเป็นเงิน · ส่วนลด X% · **ยอดหลังหักส่วนลด** · VAT 7% · รวมทั้งสิ้น |
| **VAT + หัก ณ ที่จ่าย** | `PO_WHT_*` | งานบริการที่ต้องหัก ณ ที่จ่าย | รวมเป็นเงิน · VAT 7% · รวมทั้งสิ้น(รวม VAT) · **หัก ณ ที่จ่าย X%** · **ยอดชำระสุทธิ** |

> ตัวอย่างที่ฝังในหน้า HTML prototype (แท็บ PDF Preview) ใช้ชุด **VAT 7%** เป็นตัวแทน 1 ชุดพอ

## 3. Field Mapping (UI/DB → ช่องในเอกสาร)

| ช่องในเอกสาร | Source (entity.field) | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่เอกสาร | po.po_no | `PO-พ.ศ.-running` | ✓ | running จากระบบ |
| วันที่ | po.po_date | วัน เดือน(ไทย) พ.ศ. | ✓ | +543 จาก ค.ศ. |
| อ้างอิง | po.pr_no \| po.cp_no | — | – | PR หรือ CP (ถ้าเป็น PO อิสระ = "-") |
| เครดิต / กำหนดส่ง | po.payment_term, po.expected_date | — | ✓ | เครดิตจาก master payment term |
| ผู้ขาย | vendor.name / address / tax_id / contact | — | ✓ | snapshot ตอนสร้าง PO |
| สถานที่ส่งมอบ/ให้บริการ | po.ship_to | — | ✓ | บริการ → "สถานที่ให้บริการ" |
| รายการ (loop) | po.lines[] | — | ✓ | 1 row = 1 line item · รหัส/สเปค = `<span class="sub">` |
| จำนวน / หน่วย | line.qty, line.unit | — | ✓ | |
| ราคา/หน่วย, จำนวนเงิน | line.unit_price, line.amount | `#,##0.00` | ✓ | ชิดขวา (class `num`) |
| รวมเป็นเงิน | computed | `#,##0.00` | ✓ | Σ line.amount |
| ส่วนลด | line.discount (฿/%) + po.endbill_discount | `#,##0.00` | – | ดู §4 |
| VAT | computed | `#,##0.00` | ตามชนิด | ฐาน = หลังหักส่วนลด |
| หัก ณ ที่จ่าย | computed | `-#,##0.00` | เฉพาะ WHT | ฐาน = ก่อน VAT |
| รวมทั้งสิ้น / ยอดชำระสุทธิ | computed | `#,##0.00` | ✓ | navy bar |
| จำนวนเงินตัวอักษร | computed | ไทย | ✓ | logic `baht_text.py` (ตรงยอดสุทธิจริง) |
| ผู้ลงนาม 3 ชั้น | DOA chain | — | ✓ | Maker/Checker/Approver |

## 4. กติกาคำนวณ (รองรับทุกชุด)
ระดับรายการ (per line):
- `line_subtotal = qty × unit_price`
- `line_discount = (mode==='amount') ? min(discount_amt, line_subtotal) : line_subtotal × discount_pct/100`
- `line_net = line_subtotal − line_discount`
- VAT ต่อรายการ (mutually exclusive): `none` ไม่คิด · `add` คิดเพิ่มนอก (`net × 7%`) · `included` ราคารวม VAT แล้ว (ถอด VAT = `net × 7/107`)

ระดับเอกสาร (totals):
- `subtotal = Σ line_net`
- `endbill_discount = (mode==='amount') ? value : subtotal × value/100`  *(ส่วนลดท้ายบิล ถ้ามี)*
- `after_discount = subtotal − endbill_discount`
- `vat = round(after_discount × 0.07, 2)`  *(ROUND_HALF_UP; ชุดไม่มี VAT → vat = 0 และแสดง "ยกเว้น")*
- `total_incl_vat = after_discount + vat`
- `wht = round(after_discount × wht_rate, 2)`  *(เฉพาะชุด WHT; ฐานก่อน VAT; rate เช่น 1%/2%/3%/5%)*
- `net_payable = total_incl_vat − wht`
- จำนวนเงินตัวอักษร = `baht_text(net_payable)`  *(ชุดไม่ WHT ใช้ total_incl_vat)*

ตัวอย่างยอด (ตรงกับ sample.pdf):
- VAT: 15,850 → +VAT 1,109.50 → **16,959.50**
- ไม่มี VAT: 12,000 → **12,000.00**
- ส่วนลด: 71,000 − 3,550(5%) = 67,450 → +VAT 4,721.50 → **72,171.50**
- WHT: 70,000 → +VAT 4,900 = 74,900 → −หัก 2,100(3%) → **72,800.00**

## 5. กติกาการพิมพ์ (Design Rules)
- A4 แนวตั้ง · lean type 9pt · หัวตาราง+ยอดรวมทั้งสิ้น = แถบ navy ตัวขาว · เนื้อตาราง minimal
- หัวตารางซ้ำทุกหน้า (`thead { display:table-header-group }`) · ห้ามตัด row กลาง (`tr { break-inside:avoid }`)
- ลายเซ็น + footer ชิดล่างหน้า (`.doc-bottom`) · block ลายเซ็นห้ามขึ้นหน้าใหม่แยกเนื้อหา
- หลายหน้า → footer "หน้า X / N"

## 6. วิธี regenerate
```bash
# skill dir: /mnt/skills/user/thai-doc-pdf-generator
python scripts/build_html.py BODY.html --title "ใบสั่งซื้อ ..." -o PO_<variant>_template.html
python scripts/render_pdf.py PO_<variant>_template.html -o PO_<variant>_sample.pdf
```
Dev ฝั่งระบบ: ใช้ `*_template.html` เป็นต้นแบบ → bind ข้อมูลตาราง §2 → เลือกบล็อก TOTALS ตามชนิดภาษี (§2/§4) → render PDF ด้วย engine ที่ honor `@page` + Sarabun (Chromium/Gotenberg/Puppeteer)

## 7. Checklist ก่อนส่งมอบ
- [x] A4 พอดี ไม่ล้นหน้า (ทั้ง 4 ชุด)
- [x] ตัวเลขชิดขวา + `#,##0.00`
- [x] VAT/ส่วนลด/WHT/ยอดสุทธิ ถูกต้อง + ตัวอักษรตรงยอด (ทั้ง 4 ชุด)
- [x] เลขผู้เสียภาษี + (สำนักงานใหญ่) ครบ
- [x] ลายเซ็นครบสาย Maker/Checker/Approver + วันที่
- [ ] (Dev) เชื่อม running เลขที่จากระบบ + DOA chain เข้าช่องลงนาม
