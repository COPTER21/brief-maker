# PRINT SPEC — ใบขอซื้อ (PR)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD ของ F-PR-001 (Purchase Requisition)
> ไฟล์คู่: `PR_template.html` (master, fonts ฝัง) + `PR_sample.pdf` (ตัวอย่าง A4)

## 1. สรุป
- **ประเภทเอกสาร:** ใบขอซื้อ / Purchase Requisition
- **ขนาด:** A4 แนวตั้ง (210×297mm), ขอบ 14mm
- **ฟอนต์:** Sarabun (ฝัง base64 ใน HTML — ไม่ต้องพึ่ง network)
- **CI:** CUBE NATIVE (Navy #0B1D3A / Primary #0B5CFF / Teal #00A88E)
- **Renderer ที่ใช้สร้าง PDF:** Playwright/Chromium → `print_background`, `prefer_css_page_size`

## 2. Field Mapping (UI/DB → ช่องในเอกสาร)

| ช่องในเอกสาร | Source (entity.field) | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่เอกสาร | pr.pr_no | `PR-YYMM-NNNNN` | ✓ | running จาก Purchase Config (doc numbering) |
| วันที่ | pr.pr_date | วัน เดือน(ไทย) พ.ศ. | ✓ | |
| วันที่ต้องการ | pr.need_date | วัน เดือน(ไทย) พ.ศ. | ✓ | default = วันที่ขอ + 7 วัน |
| ความเร่งด่วน | pr.urgency | enum (ปกติ/ด่วน) | – | |
| ประเภท | pr.type | enum (สินค้า/บริการ) | ✓ | |
| ผู้ขอซื้อ | pr.requester (employee.name) | — | ✓ | เลือกจาก Employee master |
| แผนก / ตำแหน่ง | employee.dept / position | — | ✓ | |
| อ้างอิงงบปลดอายัด | pr.release_ref (br_no) | `BRT-YYYYMMDD-NNNN` | (เงื่อนไข) | แสดง/บังคับเมื่อ Purchase Config `require_unlock_ref = true` |
| รหัส/ชื่องบประมาณ | budget_release.code / name | — | (เงื่อนไข) | มาจากใบปลดอายัด (cost_center + budget_account) |
| ผู้ขายที่เสนอ | pr.vendor (optional) | — | – | เว้นได้ → เลือกขั้น CP/PO |
| สาขาปลายทาง (รับสินค้า) | pr.branch_id → branch.* | — | ✓ | **ดึงจาก Organization branch master** (code 5 หลัก + name + address) — แสดงเป็นบล็อก Ship-to Branch + เลขที่ meta |
| โลโก้บริษัท | organization.logo_url | image (base64 ฝังใน PDF) | – | **ดึงจาก Organization master** — ถ้าไม่มีโลโก้ → fallback ตัวย่อ gradient (`.doc-logo--ph`) |
| ชื่อ/ที่อยู่/เลขผู้เสียภาษี องค์กร | organization.* | — | ✓ | ดึงจาก Organization master (สำนักงานใหญ่/สาขา) |
| รายการ (loop) | pr.lines[] | — | ✓ | 1 row = 1 line item |
| รหัสสินค้า | line.item_code | — | ✓ | รหัสสั้นตาม Product master (เช่น PPR-A4) |
| จำนวน / หน่วย | line.qty / line.unit | — | ✓ | หน่วยเลือกจาก product.units[] (หลายหน่วย/ราคาต่างกัน) |
| ราคา/หน่วย | line.unit_price | `#,##0.00` | ✓ | ดึงจาก product.units[].price ตามหน่วยที่เลือก (แก้ได้) |
| จำนวนเงิน | computed `qty × unit_price` | `#,##0.00` | ✓ | ชิดขวา |
| รวมเป็นเงิน | computed | `#,##0.00` | ✓ | Σ จำนวนเงิน |
| ภาษีมูลค่าเพิ่ม 7% | computed | `#,##0.00` | (เฉพาะ line ที่ vat_group=VAT7) | ฐาน = หลังหักส่วนลด |
| รวมทั้งสิ้น | computed | `#,##0.00` | ✓ | |
| จำนวนเงินตัวอักษร | computed | ไทย | ✓ | ใช้ logic baht_text |
| ผู้ลงนาม (N ชั้น) | DOA chain | — | ✓ | **จำนวนช่องลายเซ็น = จำนวนขั้นใน DOA chain ของ F-PR-001 (ไม่ fix 3 ช่อง)** — render วน loop ตามที่ DOA resolver คืนค่า {role, position}; เรียกด้วย {feature_id, cost_center, amount} ไม่ hardcode |

## 3. กติกาคำนวณ
- `subtotal = Σ(qty × unit_price)`
- `after_discount = subtotal − discount`
- `vat = round(Σ(after_discount ของ line ที่ vat_group=VAT7) × 0.07, 2)` *(ROUND_HALF_UP)*
- `grand_total = after_discount + vat`
- จำนวนเงินตัวอักษร: port `scripts/baht_text.py`
- **ตัวอย่างในไฟล์นี้:** subtotal 14,520.00 · vat 1,016.40 · grand 15,536.40 (ทุก line เป็น VAT7)

## 4. กติกาการพิมพ์ (ตาม Design Rules)
- A4 แนวตั้ง · lean type 9pt · หัวตาราง+ยอดรวมแถบ navy · ลายเซ็น+footer ชิดล่าง (.doc-bottom)
- หัวตารางซ้ำทุกหน้า (`thead { display:table-header-group }`)
- ห้ามตัด row กลาง (`tr { break-inside:avoid }`)
- block ลายเซ็นห้ามขึ้นหน้าใหม่แยกจากเนื้อหา (`break-inside:avoid`)
- หลายหน้า → footer "หน้า X / N"

## 5. Governance (ตาม CUBE 4.0 Development Process Standard)
- **จำนวน + ลำดับชั้นช่องลายเซ็น ดึงจาก DOA chain** ของ F-PR-001 (เรียก DOA engine ด้วย `{feature_id, cost_center, amount}`) — render วน loop ตามจำนวนขั้นที่คืนค่า **ห้าม fix 3 ช่อง / ห้าม hardcode tier**
- **โลโก้ + ข้อมูลองค์กร (ชื่อ/ที่อยู่/เลขผู้เสียภาษี/สำนักงานใหญ่-สาขา) ดึงจาก Organization master** — ไม่มีโลโก้ → fallback ตัวย่อ gradient
- ฟิลด์อ้างอิงงบปลดอายัด gate ด้วย Purchase Config (`require_unlock_ref`) — ถ้า false ให้ซ่อนทั้ง section
- Data Classification ของเอกสาร PR = Internal (default)

## 6. วิธี build ใหม่ (regenerate)
```bash
python scripts/build_html.py pr_body.html --title "ใบขอซื้อ PR-2604-00015" -o PR_template.html
python scripts/render_pdf.py PR_template.html -o PR_sample.pdf
```
Dev ฝั่งระบบ: เอา `PR_template.html` เป็นต้นแบบ HTML แล้ว bind ข้อมูลตามตาราง §2
จากนั้น render เป็น PDF ด้วย engine ที่ honor `@page` + Sarabun (Chromium/Gotenberg/Puppeteer)

## 7. Checklist ก่อนส่งมอบ
- [x] A4 พอดี ไม่ล้นหน้า
- [x] ตัวเลขชิดขวา + `#,##0.00`
- [x] VAT/ยอดรวม ถูกต้อง + ตัวอักษรตรงยอด
- [x] ลายเซ็นครบสาย (ผู้ขอ/ผู้ตรวจสอบ/ผู้อนุมัติ) + วันที่
- [x] อ้างอิงงบปลดอายัด + รหัส/ชื่องบประมาณ ครบ
