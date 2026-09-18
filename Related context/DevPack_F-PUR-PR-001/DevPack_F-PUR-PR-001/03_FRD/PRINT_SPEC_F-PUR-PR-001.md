# PRINT SPEC — ใบขอซื้อ (PR)
> pdfdoc declaration ของ F-PUR-PR · แนบคู่ BRD (Phase A) / FRD (Phase B)
> ไฟล์คู่ที่ Phase B ต้องสร้าง: `PR_template.html` (Sarabun ฝัง base64) + `PR_sample.pdf`

## 1. สรุป
- **ประเภทเอกสาร:** ใบขอซื้อ / Purchase Requisition — เอกสารภายใน (ไม่ใช่ใบกำกับภาษี)
- **ขนาด:** A4 แนวตั้ง 210×297mm · ขอบ 14mm
- **ฟอนต์:** Sarabun (ฝัง base64 — ไม่พึ่ง network)
- **CI:** CUBE NATIVE (Navy #0B1D3A / Primary #0B5CFF / Teal #00A88E)
- **Renderer:** Playwright/Chromium → `print_background`, `prefer_css_page_size`
- ★ **ปี = ค.ศ. ทุกจุด** (override default พ.ศ. ของ template ตาม golden rule ของ lane)

## 2. Field Mapping
| ช่องในเอกสาร | Source | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ใบขอซื้อ | `pr_header.pr_no` | `PR-YYYY-0000` (ค.ศ.) | ✓ | จาก ENG-DOC-NUM |
| วันที่เอกสาร | `pr_header.doc_date` | `d MMMM yyyy` (เดือนไทย · **ปี ค.ศ.**) | ✓ | |
| วันที่ต้องการใช้ | `pr_header.required_date` | เหมือนบน | ✓ | |
| ผู้ขอซื้อ / หน่วยงาน | `requester_name` / `department` | — | ✓ | |
| ศูนย์ต้นทุน | `cost_center_id` → ชื่อ | — | ✗ | soft-ref nullable |
| ประเภทการขอซื้อ | `pr_type` | สินค้า/บริการ/สินทรัพย์ | ✓ | |
| เหตุผลการขอซื้อ | `reason` | — | ✓ | |
| รายการ (loop) | `pr_line[]` | 1 row = 1 บรรทัด | ✓ | คอลัมน์: ลำดับ · รายการ · จำนวน · หน่วย · ราคา/หน่วย · ส่วนลด · จำนวนเงิน |
| ราคา/หน่วย · จำนวนเงิน | `unit_price_est` · `line_total` | `#,##0.00` ชิดขวา | ✓ | |
| รวมเป็นเงิน | computed `subtotal` | `#,##0.00` | ✓ | |
| ส่วนลดรวม | computed `discount_total` | `#,##0.00` | ✓ | |
| ฐานภาษี | computed `vat_base` | `#,##0.00` | ✓ | |
| ภาษีมูลค่าเพิ่ม 7% | computed `vat_amount` | `#,##0.00` | ✓ | เฉพาะบรรทัด `vat_mode=vat7` |
| รวมทั้งสิ้น | computed `grand_total` | `#,##0.00` | ✓ | |
| จำนวนเงินตัวอักษร | computed | ไทย | ✓ | logic `baht_text` |
| ผู้ขายที่แนะนำ | `pr_vendor_suggest[]` | — | ✗ | ถ้าไม่มี ซ่อนบล็อก |
| ผู้ลงนาม (ตามสาย DOA) | `approval_chain[]` | ชื่อ + ตำแหน่ง + วันที่ (ค.ศ.) | ✓ | **จำนวนช่องแปรตามสายที่ resolve** ไม่ fix 3 ชั้น |

## 3. กติกาคำนวณ
- `line_total = qty × unit_price_est − discount(line)`
- `subtotal = Σ line_total (ก่อนภาษี)` · `vat_base = Σ line_total เฉพาะ vat_mode=vat7`
- `vat_amount = round(vat_base × 0.07, 2)` ROUND_HALF_UP
- `grand_total = subtotal + vat_amount`
- จำนวนเงินตัวอักษร: port `scripts/baht_text.py`

## 4. กติกาการพิมพ์
- lean type 9pt · หัวตารางเส้นบาง · บล็อกลายเซ็น + footer ชิดล่าง (`.doc-bottom`)
- `thead {display:table-header-group}` หัวตารางซ้ำทุกหน้า · `tr {break-inside:avoid}`
- บล็อกลายเซ็น `break-inside:avoid` ห้ามขึ้นหน้าใหม่ลอย
- footer "หน้า X / N" · ไม่มีคำว่า "ต้นฉบับ/สำเนา" (เอกสารภายใน)

## 5. Checklist ก่อนส่งมอบ (Phase B)
- [ ] A4 พอดี ไม่ล้นหน้า
- [ ] ตัวเลขชิดขวา `#,##0.00`
- [ ] VAT / ยอดรวม ถูก + ตัวอักษรตรงยอด
- [ ] **ทุกปีเป็น ค.ศ.** ไม่มี พ.ศ. หลงเหลือ
- [ ] ช่องลายเซ็นแปรตามสาย DOA ที่ resolve จริง (ไม่ fix 3 ชั้น)
