# PRINT SPEC — ใบลดหนี้ (ผู้ขาย) · DN · Debit Note · F-ACC-DN

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD Pack ของ F-ACC-DN (Debit Note ฝั่งซื้อ/AP)
> ไฟล์คู่: `template.html` (master, Sarabun ฝัง base64) + `sample.pdf` (ตัวอย่าง A4)
> ออกตาม **มาตรา 86/10 แห่งประมวลรัษฎากร** (ใบลดหนี้ — โครงเดียวกับ CN แต่ฝั่งซื้อ ลด **ภาษีซื้อ**) · html-generator-v9 ใช้ `template.html` เดียวกันใน tab **PDF Preview** (Pattern Q · `.a4`)

## 1. สรุป
- **ประเภทเอกสาร:** ใบลดหนี้ (ผู้ขาย) / Debit Note — doc_type `DN` (ฝั่ง AP/เจ้าหนี้ · ผู้รับ = ผู้ขาย)
- **ขนาด:** A4 แนวตั้ง (210×297mm), ขอบ 14mm
- **ฟอนต์:** Sarabun (ฝัง base64 ใน HTML — ไม่พึ่ง network)
- **CI:** CUBE NATIVE (Navy #0B1D3A / Primary #0B5CFF / Teal #00A88E)
- **Renderer ที่ใช้สร้าง PDF:** Playwright/Chromium → `print_background`, `prefer_css_page_size`
- **เลขที่เอกสาร:** `DN-YYYY-NNNN` (ปี **ค.ศ.**) — จาก `ENG-DOC-NUM.next('DN', ctx)` ตอนอนุมัติครบสาย (DOCCFG_BRIEF · BR-08 · Iron 4) · **ห้าม format เอง**
- **⚠ วันที่ทั้งหมดเป็น ค.ศ. (Gregorian)** ตาม PREBRIEF OB-9 / GR — จงใจ override default พ.ศ. ของ thai-standards

## 2. Field Mapping (UI/DB → ช่องในเอกสาร)

| ช่องในเอกสาร | Source (entity.field) | Format | บังคับ | หมายเหตุ · ม.86/10 |
|---|---|---|---|---|
| คำว่า "ใบลดหนี้ (ผู้ขาย) / Debit Note" | const | — | ✓ | (1) |
| ผู้ซื้อ (ผู้ออก): ชื่อ/ที่อยู่/เลขภาษี/สาขา | company (placeholder 2BSimple) | — | ✓ | (2) — สำนักงานใหญ่/สาขาต่อท้ายเลขภาษี |
| ผู้ขาย (ผู้รับ): ชื่อ/ที่อยู่/เลขภาษี/สาขา | vendor snapshot (`PARTNER_BY[dn.partner]`) | — | ✓ | (3) — readonly จากใบตั้งหนี้ |
| เลขที่ DN | `dn.code` | `DN-YYYY-NNNN` | ✓ | (4) ออกตอน approved ครบสาย (BR-08) |
| วันที่ใบลดหนี้ | `dn.dnDate` | วัน เดือน(ไทย) **ค.ศ.** | ✓ | (5) ≥ วันที่ใบกำกับเดิม (step2Validate) |
| ใบตั้งหนี้อ้างอิง (AP invoice) | `inv.no` (`ap_open_item`) | — | ✓ | (6) soft-ref F-ACC-APINV · outstanding>0 (BR-01) |
| **เลขที่ + วันที่ ใบกำกับภาษีเดิมของผู้ขาย** | `inv.vinv` · `inv.vdate` | — · ค.ศ. | ✓ | (6) ม.86/10 อ้างใบกำกับเดิม |
| ใบคืนสินค้า (RTV) | `dn.rtv` | — | เมื่อเหตุ=คืนของ | soft-ref RTV W3-LITE (mock) · BR-06 |
| เหตุผลการลดหนี้ | `dn.reason` (master `REASON_BY`) | — | ✓ | (8) คืนสินค้า RTV / ผู้ขายคิดราคาเกิน / ของขาด |
| คำอธิบายเหตุผล (พิมพ์บนใบ) | `dn.reasonText` | ≥10 ตัวอักษร | ✓ | (8) แสดงในบล็อกหมายเหตุ · BR-05 |
| เลขที่ใบลดหนี้จากผู้ขาย | `dn.vendorCn` | — | — | ใช้ยืนยันการลดภาษีซื้อ (ถ้าผู้ขายออกให้) |
| รายการที่ลด (loop) | `dn.lines[]` | — | ✓ | 1 row = 1 line item (B2 v2) |
| — มูลค่าตามใบเดิม (ต่อบรรทัด) | `line.origQty × line.origPrice` | `#,##0.00` | ✓ | (7) = จำนวนเดิม × ราคาเดิม |
| — มูลค่าที่ถูกต้อง (ต่อบรรทัด) | computed | `#,##0.00` | ✓ | (7) = orig − ผลต่าง |
| — ผลต่าง/มูลค่าที่ลด (ต่อบรรทัด) | `line.qty × line.unit_price` | `#,##0.00` | ✓ | (7) = จำนวนลด × ราคาลด |
| — sub รายละเอียด qty | `origQty`/คงเหลือ/`qty`/`unit_price`/`rtv` | — | — | จำนวนเดิม → คงเหลือ (คืน N @ ราคา) · RTV |
| มูลค่าตามใบกำกับภาษีเดิม (รวม) | computed | `#,##0.00` | ✓ | (7) Σ orig_amount |
| มูลค่าที่ถูกต้อง (รวม) | computed | `#,##0.00` | ✓ | (7) Σ correct_amount |
| ผลต่าง/มูลค่าที่ลด (รวม) | `totals().before` | `#,##0.00` | ✓ | (7) Σ diff = ฐานลดหนี้ |
| ภาษีซื้อ 7% ของผลต่าง | `totals().vat` | `#,##0.00` | ✓ | **ภาษีซื้อ** (input VAT) — ลดเดือนที่ออก (BR-09) |
| รวมเงินลดหนี้ทั้งสิ้น | `totals().grand` | `#,##0.00` | ✓ | grand = ผลต่าง + VAT ผลต่าง · ฐานวงเงิน DOA |
| จำนวนเงินลดหนี้ (ตัวอักษร) | computed | ไทย | ✓ | logic `baht_text.py` |
| ผู้ลงนาม (ผู้จัดทำ / ผู้อนุมัติ / ผู้รับ) | `approval_chain` snapshot | — | ✓ | slot generic — ดู §3.1 |

## 3. กติกาคำนวณ (ม.86/10 — ลดหนี้ฝั่งซื้อ = ลดเจ้าหนี้ + ลดภาษีซื้อ)
- `line.orig_amount = line.origQty × line.origPrice`  *(มูลค่าตามใบตั้งหนี้เดิม ต่อบรรทัด)*
- `line.diff_amount = line.qty × line.unit_price`  *(มูลค่าที่ลด ต่อบรรทัด · qty=จำนวนลด, unit_price=ราคาลด)*
- `line.correct_amount = line.orig_amount − line.diff_amount`  *(ต้อง ≥ 0 · BR-03/BR-04)*
- `credit_base = Σ line.diff_amount`  *(ผลต่างรวม = ฐานเงินที่ลด, ก่อน VAT · `totals().before`)*
- `vat_credit = round(credit_base × 0.07, 2)`  *(ROUND_HALF_UP — เฉพาะบรรทัดที่ใบเดิม VAT7)*
- `grand_total = credit_base + vat_credit`  *(ยอดลดหนี้สุทธิ · เป็นฐานวงเงิน DOA)*
- ตัวเลขทั้งหมดเป็นค่าที่ **ลด** — dev อาจเก็บเป็นค่าลบใน JE/VAT report (contract `input_vat_line` **negative**) แต่ **บนใบพิมพ์แสดงเป็นค่าบวก** (ยอดที่ลด)
- ตรวจสอบ: `grand_total ≤ outstanding` ของใบตั้งหนี้อ้างอิง (BR-02) — ตอนส่งและตอนอนุมัติ (re-check · S-11)
- จำนวนเงินตัวอักษร: port `scripts/baht_text.py`

### 3.1 ลายเซ็น — value-driven ตาม DOA (generic slots · ไม่ hardcode ชื่อ)
- **3 ช่องบนใบ:** `ผู้จัดทำ` (เจ้าหน้าที่บัญชีเจ้าหนี้) · `ผู้อนุมัติ (ตามสาย DOA)` · `ผู้รับใบลดหนี้ (ผู้ขาย)`
- ช่อง **ผู้อนุมัติ = แสดงตาม `approval_chain` snapshot** ที่ freeze ตอนส่งอนุมัติ (DOA_BRIEF · `DOA-ACC-DN`):
  - tier 1 (0–50,000): 1 ช่อง `[role-mgr-pur]`
  - tier 2 (50,000.01–300,000): 2 ช่อง `[role-mgr-pur]→[role-mgr-acc]`
  - tier 3 (>300,000): 3 ช่อง `[role-mgr-pur]→[role-mgr-acc]→[role-cfo]`
  - Dev ทำซ้ำ block `.sign` ตามจำนวนขั้นจริง — template แสดง 1 ช่องอนุมัติเป็นตัวอย่าง (sample = tier 1, ยอด 11,984.00)
- ใต้เส้น: `(วงเล็บชื่อ)` → ตำแหน่ง/บทบาท → วันที่ — **ห้าม hardcode ชื่อบุคคล** (ผูกจาก approval_history)

## 4. กติกาการพิมพ์ (ตาม Design Rules)
- A4 แนวตั้ง · lean type 9pt · หัวตาราง+ยอดรวม = แถบ navy ตัวอักษรขาว · ลายเซ็น+footer ชิดล่าง (`.doc-bottom`)
- หัวตารางซ้ำทุกหน้า · ห้ามตัด row กลาง · block ลายเซ็น break-inside:avoid
- footer ระบุ "ออกตามมาตรา 86/10 แห่งประมวลรัษฎากร" + "หน้า X / N"
- **วันที่ทุกช่องเป็น ค.ศ.** (เช่น 20 กันยายน 2026) — GR / PREBRIEF OB-9

## 5. วิธี build ใหม่ (regenerate)
```bash
# body = fragment .doc-page (Claude เขียนเฉพาะ body)
python .claude/skills/thai-doc-pdf-generator/scripts/build_html.py BODY.html --title "ใบลดหนี้ (Debit Note) — F-ACC-DN" -o template.html
.claude/venv/Scripts/python.exe .claude/skills/thai-doc-pdf-generator/scripts/render_pdf.py template.html -o sample.pdf
```
Dev: เอา `template.html` เป็นต้นแบบ แล้ว bind ข้อมูลตาม §2 · render ด้วย engine ที่ honor `@page` + Sarabun

## 6. Placeholder / ค่าที่สมมติในตัวอย่าง (sample.pdf)
> ตัวอย่างเป็น **mock data** — ค่าจริง bind จากระบบตาม §2 · อิง seed HTML `F-ACC-DN_debit-note.html` (INVOICES/PARTNERS/RTVS/DN_REASONS)

| ช่อง | ค่าตัวอย่าง | ที่มา |
|---|---|---|
| ผู้ซื้อ (บริษัท+ที่อยู่+เลขภาษี) | บริษัท ทูบีซิมเปิล จำกัด · 0105560012345 (สำนักงานใหญ่) | placeholder มาตรฐาน 2BSimple |
| ผู้ขาย (ผู้รับ) | บริษัท ไทยฟิลเตอร์ซัพพลาย จำกัด · 0105551023456 | seed PARTNERS V-2001 (จริง = snapshot ใบตั้งหนี้) |
| เลขที่ DN | DN-2026-0014 | placeholder (จริง = ENG-DOC-NUM) · sample แทนใบตัวแทน |
| วันที่ใบลดหนี้ / ใบกำกับเดิม | 20 ก.ย. 2026 / 2 ก.ย. 2026 | placeholder (ค.ศ.) |
| ใบตั้งหนี้อ้างอิง / ใบกำกับเดิม | API-2026-0041 / TFS-6601 | seed INVOICES |
| ใบคืนสินค้า (RTV) | RTV-2026-0007 · RTV-2026-0010 | seed RTVS (อ้าง API-2026-0041) |
| เลขที่ใบลดหนี้จากผู้ขาย | TFS-6642 | seed DN k=1 `vendorCn` |
| เหตุผล | คืนสินค้า (อ้างใบคืนสินค้า RTV) | DN_REASONS `RTV` · scenario S-01 |
| รายการที่ลด + จำนวน/ราคา | ไส้กรอง CT-10 (20→18 กล่อง @3,000 · คืน 2) · เครื่องกรอง AP-500 (6→5 เครื่อง @5,200 · คืน 1) | mock (2 บรรทัดจาก INVOICES API-2026-0041) |
| ยอด: ผลต่าง 11,200 · VAT ซื้อ 784 · รวม 11,984 | computed | ตรงสูตร §3 |

## 7. Checklist ก่อนส่งมอบ
- [x] A4 พอดี ไม่ล้นหน้า (1 หน้า)
- [x] ตัวเลขชิดขวา + `#,##0.00`
- [x] คำว่า "ใบลดหนี้ (ผู้ขาย)" ชัดเจน + เลขภาษีสองฝ่าย + (สำนักงานใหญ่)
- [x] เลขที่+วันที่ ใบกำกับภาษีเดิมของผู้ขาย + เลขใบตั้งหนี้ แสดงครบ (ม.86/10 (6))
- [x] มูลค่าเดิม / มูลค่าที่ถูกต้อง / ผลต่าง / ภาษีของผลต่าง แสดงครบ (ม.86/10 (7))
- [x] คำอธิบายเหตุผลแสดงบนใบ (ม.86/10 (8))
- [x] VAT = **ภาษีซื้อ** (input VAT) 7% ของผลต่าง + ยอดรวม + ตัวอักษรตรงยอด (11,984.00)
- [x] วันที่เป็น ค.ศ. (GR)
- [x] ลายเซ็น 3 สาย generic (ผู้จัดทำ/ผู้อนุมัติ DOA/ผู้รับ=ผู้ขาย) — ไม่ hardcode ชื่อ
- [x] ไม่มี leakage ฝั่งลูกค้า/AR (ลูกค้า/ภาษีขาย/Credit Note/CN- = 0)
