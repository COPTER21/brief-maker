# PRINT SPEC — ใบลดหนี้ลูกค้า (CN · Credit Note) · F-ACC-CN

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD Pack ของ F-ACC-CN (Credit Note)
> ไฟล์คู่: `template.html` (master, Sarabun ฝัง base64) + `sample.pdf` (ตัวอย่าง A4)
> ออกตาม **มาตรา 86/10 แห่งประมวลรัษฎากร** (ใบลดหนี้) · html-generator-v9 ใช้ `template.html` เดียวกันใน tab **PDF Preview** (Pattern Q · `.a4`)

## 1. สรุป
- **ประเภทเอกสาร:** ใบลดหนี้ (ลูกค้า) / Credit Note — doc_type `CN`
- **ขนาด:** A4 แนวตั้ง (210×297mm), ขอบ 14mm
- **ฟอนต์:** Sarabun (ฝัง base64 ใน HTML — ไม่พึ่ง network)
- **CI:** CUBE NATIVE (Navy #0B1D3A / Primary #0B5CFF / Teal #00A88E)
- **Renderer ที่ใช้สร้าง PDF:** Playwright/Chromium → `print_background`, `prefer_css_page_size`
- **เลขที่เอกสาร:** `CN-YYYY-NNNN` (ปี **ค.ศ.**) — จาก `ENG-DOC-NUM.next('CN', ctx)` ตอนอนุมัติขั้นสุดท้าย (DOCCFG_BRIEF · Iron 4) · **ห้าม format เอง**
- **⚠ วันที่ทั้งหมดเป็น ค.ศ. (Gregorian)** ตาม PREBRIEF OB-10 / GR-1 — จงใจ override default พ.ศ. ของ thai-standards

## 2. Field Mapping (UI/DB → ช่องในเอกสาร)

| ช่องในเอกสาร | Source (entity.field) | Format | บังคับ | หมายเหตุ · ม.86/10 |
|---|---|---|---|---|
| คำว่า "ใบลดหนี้ / Credit Note" | const | — | ✓ | ม.86/10 (1) |
| ผู้ขาย: ชื่อ/ที่อยู่/เลขภาษี/สาขา | company (placeholder 2BSimple) | — | ✓ | (2) — สำนักงานใหญ่/สาขาต่อท้ายเลขภาษี |
| ลูกค้า: ชื่อ/ที่อยู่/เลขภาษี/สาขา | snapshot จากใบกำกับภาษีเดิม | — | ✓ | (3) — readonly จากใบเดิม |
| เลขที่ CN | `cn.code` | `CN-YYYY-NNNN` | ✓ | (4) ออกตอน approved ขั้นสุดท้าย |
| วันที่ใบลดหนี้ | `cn.cn_date` | วัน เดือน(ไทย) **ค.ศ.** | ✓ | (5) ≥ วันที่ใบเดิม |
| **เลขที่ + วันที่ ใบกำกับภาษีเดิม** | `inv.no` · `inv.date` | — · ค.ศ. | ✓ | (6) อ้าง ar_open_item (F-ACC-ARINV) |
| ใบรับคืนสินค้า | `sr.no` | — | เมื่อเหตุ=รับคืน | soft-ref Sales Return W4-LITE (mock) |
| เหตุผลการลดหนี้ | `cn.reason` (master) | — | ✓ | (8) รับคืน/ส่วนลดภายหลัง/คิดราคาผิด/คิดจำนวนเกิน |
| คำอธิบายเหตุผล (พิมพ์บนใบ) | `cn.reason_text` | ≥10 ตัวอักษร | ✓ | (8) แสดงในบล็อกหมายเหตุ |
| รายการที่ลด (loop) | `cn.lines[]` | — | ✓ | 1 row = 1 line item |
| — มูลค่าตามใบเดิม (ต่อบรรทัด) | `line.orig_amount` | `#,##0.00` | ✓ | (7) = จำนวนเดิม × ราคาเดิม |
| — มูลค่าที่ถูกต้อง (ต่อบรรทัด) | `line.correct_amount` | `#,##0.00` | ✓ | (7) = (จำนวนเดิม − ลด) × ราคาที่ถูกต้อง |
| — ผลต่าง/มูลค่าที่ลด (ต่อบรรทัด) | `line.diff_amount` | `#,##0.00` | ✓ | (7) = orig − correct |
| — sub รายละเอียด qty | `line.orig_qty`/`credit_qty`/`unit_price` | — | — | จำนวนเดิม → คงเหลือ (รับคืน N @ ราคา) |
| มูลค่าตามใบกำกับภาษีเดิม (รวม) | computed | `#,##0.00` | ✓ | (7) Σ orig_amount |
| มูลค่าที่ถูกต้อง (รวม) | computed | `#,##0.00` | ✓ | (7) Σ correct_amount |
| ผลต่าง/มูลค่าที่ลด (รวม) | computed | `#,##0.00` | ✓ | (7) Σ diff_amount = ฐานลดหนี้ |
| ภาษีมูลค่าเพิ่ม 7% ของผลต่าง | computed | `#,##0.00` | ✓ | VAT credit — ลดภาษีขายเดือนที่ออก (BR-09) |
| รวมเงินลดหนี้ทั้งสิ้น | computed | `#,##0.00` | ✓ | grand_total = ผลต่าง + VAT ผลต่าง |
| จำนวนเงินลดหนี้ (ตัวอักษร) | computed | ไทย | ✓ | logic `baht_text.py` |
| ผู้ลงนาม (ผู้จัดทำ / ผู้อนุมัติ / ผู้รับ) | `approval_chain` snapshot | — | ✓ | slot generic — ดู §3.1 |

## 3. กติกาคำนวณ (ม.86/10 — ลดหนี้ = credit)
- `line.diff_amount = line.orig_amount − line.correct_amount`  *(ต่อบรรทัด · ต้อง ≥ 0)*
- `credit_base = Σ line.diff_amount`  *(ผลต่างรวม = ฐานเงินที่ลด, ก่อน VAT)*
- `vat_credit = round(credit_base × 0.07, 2)`  *(ROUND_HALF_UP — เฉพาะบรรทัดที่ใบเดิม VAT)*
- `grand_total = credit_base + vat_credit`  *(ยอดลดหนี้สุทธิ · เป็นฐานวงเงิน DOA)*
- ตัวเลขทั้งหมดเป็นค่าที่ **ลด (credit)** — dev อาจเก็บเป็นค่าลบใน JE/VAT report (contract `output_vat_line` negative) แต่ **บนใบพิมพ์แสดงเป็นค่าบวก** (ยอดที่ลด)
- ตรวจสอบ: `grand_total ≤ outstanding` ของใบอ้างอิง (BR-02) — ตอนส่งและตอนอนุมัติ
- จำนวนเงินตัวอักษร: port `scripts/baht_text.py`

### 3.1 ลายเซ็น — value-driven ตาม DOA (generic slots · ไม่ hardcode ชื่อ)
- **3 ช่องบนใบ:** `ผู้จัดทำ` (เจ้าหน้าที่ลูกหนี้) · `ผู้อนุมัติ (ตามสาย DOA)` · `ผู้รับใบลดหนี้ (ลูกค้า)`
- ช่อง **ผู้อนุมัติ = แสดงตาม `approval_chain` snapshot** ที่ freeze ตอนส่งอนุมัติ (DOA_BRIEF §3):
  - tier 1 (0–50,000): 1 ช่อง `[role-mgr-sales]`
  - tier 2 (50,000.01–300,000): 2 ช่อง `[role-mgr-sales]→[role-mgr-acc]`
  - tier 3 (>300,000): 3 ช่อง `[role-mgr-sales]→[role-mgr-acc]→[role-cfo]`
  - Dev ทำซ้ำ block `.sign` ตามจำนวนขั้นจริง — template แสดง 1 ช่องอนุมัติเป็นตัวอย่าง (sample = tier 1, ยอด 12,947.00)
- ใต้เส้น: `(วงเล็บชื่อ)` → ตำแหน่ง/บทบาท → วันที่ — **ห้าม hardcode ชื่อบุคคล** (ผูกจาก approval_history)

## 4. กติกาการพิมพ์ (ตาม Design Rules)
- A4 แนวตั้ง · lean type 9pt · หัวตาราง+ยอดรวม = แถบ navy ตัวอักษรขาว · ลายเซ็น+footer ชิดล่าง (`.doc-bottom`)
- หัวตารางซ้ำทุกหน้า · ห้ามตัด row กลาง · block ลายเซ็น break-inside:avoid
- footer ระบุ "ออกตามมาตรา 86/10 แห่งประมวลรัษฎากร" + "หน้า X / N"
- **วันที่ทุกช่องเป็น ค.ศ.** (เช่น 18 กันยายน 2026) — GR-1 / PREBRIEF OB-10

## 5. วิธี build ใหม่ (regenerate)
```bash
python scripts/build_html.py BODY.html --title "ใบลดหนี้ (Credit Note) — F-ACC-CN" -o template.html
python scripts/render_pdf.py template.html -o sample.pdf
```
Dev: เอา `template.html` เป็นต้นแบบ แล้ว bind ข้อมูลตาม §2 · render ด้วย engine ที่ honor `@page` + Sarabun

## 6. Placeholder / ค่าที่สมมติในตัวอย่าง (sample.pdf)
> ตัวอย่างเป็น **mock data** — ค่าจริง bind จากระบบตาม §2

| ช่อง | ค่าตัวอย่าง | ที่มา |
|---|---|---|
| ผู้ขาย (บริษัท+ที่อยู่+เลขภาษี) | บริษัท ทูบีซิมเปิล จำกัด · 0105560012345 (สำนักงานใหญ่) | placeholder มาตรฐาน 2BSimple |
| ลูกค้า (ผู้ซื้อ) | บริษัท กรุงสยาม เปเปอร์ แอนด์ ออฟฟิศ จำกัด · 0105551023456 | placeholder (จริง = snapshot ใบเดิม) |
| เลขที่ CN | CN-2026-0022 | placeholder (จริง = ENG-DOC-NUM) |
| วันที่ใบลดหนี้ / ใบเดิม | 18 ก.ย. 2026 / 15 ส.ค. 2026 | placeholder (ค.ศ.) |
| ใบกำกับภาษีเดิม / ใบรับคืน | INV-2026-0140 / SR-2026-0016 | อิง Mock Data Spec PREBRIEF §8 |
| เหตุผล | รับคืนสินค้า (สินค้าชำรุดจากการขนส่ง) | scenario S-01 |
| รายการที่ลด + จำนวน/ราคา | กระดาษ A4 (200→180 รีม @105) · หมึก (30→26 กล่อง @2,500) | mock |
| ยอด: ผลต่าง 12,100 · VAT 847 · รวม 12,947 | computed | ตรงสูตร §3 |

## 7. Checklist ก่อนส่งมอบ
- [x] A4 พอดี ไม่ล้นหน้า (1 หน้า)
- [x] ตัวเลขชิดขวา + `#,##0.00`
- [x] คำว่า "ใบลดหนี้" ชัดเจน + เลขภาษีสองฝ่าย + (สำนักงานใหญ่)
- [x] เลขที่+วันที่ ใบกำกับภาษีเดิม แสดงครบ (ม.86/10 (6))
- [x] มูลค่าเดิม / มูลค่าที่ถูกต้อง / ผลต่าง / ภาษีของผลต่าง แสดงครบ (ม.86/10 (7))
- [x] คำอธิบายเหตุผลแสดงบนใบ (ม.86/10 (8))
- [x] VAT/ยอดรวม ถูกต้อง + ตัวอักษรตรงยอด (12,947.00)
- [x] วันที่เป็น ค.ศ. (GR-1)
- [x] ลายเซ็น 3 สาย generic (ผู้จัดทำ/ผู้อนุมัติ DOA/ผู้รับ) — ไม่ hardcode ชื่อ
