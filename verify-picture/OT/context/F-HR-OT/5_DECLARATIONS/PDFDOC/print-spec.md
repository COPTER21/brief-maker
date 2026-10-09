# PRINT SPEC — ใบขอทำงานล่วงเวลา (OT)

> ออกโดย `thai-doc-pdf-generator` · **Lane Mode** · S1.8 · 2026-08-29 · feature `F-HR-OT` · OT / Shift · โอที
> เอกสารประกอบสำหรับ Dev — **แนบคู่กับ FRD** (`3_FRD/PRINT_SPEC.md` ที่ S5) ของ feature ที่จะ build เอกสารนี้ลงระบบ
> ไฟล์คู่: `template.html` (master · Sarabun ฝัง base64) + `sample.pdf` (ตัวอย่าง A4 1 หน้า)
> **html-generator-v9 (S2) ใช้ `template.html` ตัวเดียวกันนี้ใน view tab "PDF"** (Pattern Q · `.a4`) — **ห้ามวาดใบ OT ขึ้นใหม่ในหน้า HTML**

## 1. สรุป

| | |
|---|---|
| ประเภทเอกสาร | **ใบขอทำงานล่วงเวลา / Overtime Request Form** — `doc_type` = **`OT`** (ดู `../DOCCFG_BRIEF.md`) |
| ขนาด | A4 แนวตั้ง (210×297 mm) · ขอบ 14 mm · **1 หน้า** (ยืนยันจาก `sample.pdf` — `Page size: 595.276 x 841.89 pts` · `Pages: 1`) |
| ฟอนต์ | Sarabun (ฝัง base64 ใน HTML — ไม่พึ่ง network) |
| CI | CUBE NATIVE (Navy / Primary / Teal) ผ่าน `assets/base.css` — **ห้ามเขียน hex สีเองใน body** |
| Renderer ที่ใช้สร้าง `sample.pdf` ครั้งนี้ | **WeasyPrint 69.0** — `[หมายเหตุ]` เครื่องที่รัน **ติดตั้ง Chromium ของ Playwright ไม่ได้** (CDN ถูกบล็อกโดย egress allowlist) จึง render ด้วย WeasyPrint แทน · **วิธีเดียวกับที่ `F-HR-LEAVE` ใช้กับใบลา** · ผลลัพธ์ A4 1 หน้า ตรวจด้วยภาพแล้ว · **Dev ใช้ engine ใดก็ได้ที่ honor `@page` + Sarabun** (Chromium / Gotenberg / Puppeteer / WeasyPrint) |
| ข้อสังเกตของ renderer | WeasyPrint **ไม่ดัน `.doc-bottom` ชิดขอบล่างสุดของหน้า** เมื่อเนื้อหาสั้นกว่าหน้า (บล็อกลายเซ็น+footer จะอยู่ต่อจากเนื้อหา) — Chromium ดันชิดล่างตาม `.doc-bottom` · **เป็นเรื่องของ renderer ไม่ใช่ของ template** และไม่กระทบความถูกต้องของข้อมูล |
| ช่องลายเซ็น | **3 ช่องปกติ** (ผู้ขอทำงานล่วงเวลา · ผู้บังคับบัญชา · ฝ่ายบุคคล) · **4 ช่องเมื่อใบเกินเพดาน** (เพิ่ม ผู้บริหารต้นสังกัด) — **จำนวนช่อง = จำนวน step ที่ DOA resolve ได้จริง ห้าม render ตายตัว** (ดู `../DOA_BRIEF.md §3`) · `sample.pdf` แสดง **กรณีเกินเพดาน (4 ช่อง)** เพราะเป็นกรณีที่ต่างจากใบลา |
| เลขผู้เสียภาษี / สาขา | **ไม่มี** — ใบ OT ไม่ใช่เอกสารทางภาษี (ตัดออกจาก block HEADER โดยตั้งใจ) |
| **ตัวเลขเงิน** | **ไม่มีในเอกสารนี้เลย** — PREBRIEF **BR-18** · FN-53 · `multiplier` (×1.5 · ×1.0 · ×3.0) พิมพ์ไว้เป็น **ค่าอ้างอิงของอัตรา ไม่ใช่ตัวคูณเงินบนใบ** · มูลค่าเกิดที่ **Payroll (W4)** · `baht_text.py` **ไม่ใช้** |

## 2. Field Mapping (UI/DB → ช่องในเอกสาร)

| ช่องในเอกสาร | Source (entity.field) | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| **เลขที่** | `ot_request.ot_no` | `OT-{YYYY}-{run:4}` | ✓ | **จาก `ENG-DOC-NUM.next('OT')` เท่านั้น** · ออกตอนส่งอนุมัติ · ห้าม format เอง (`DOCCFG_BRIEF §2`) |
| **วันที่ยื่น** | `ot_request.submitted_at` | วัน เดือน(ไทย) พ.ศ. | ✓ | ตัวอย่างใช้ พ.ศ. 2569 |
| **ประเภท** | `ot_request.request_mode` | `ขอล่วงหน้า` / `ขอย้อนหลัง` | ✓ | S-01 · S-02 · OQ-OT-15 |
| **สถานะ** | `ot_request.status` | text ไทย | ✓ | ร่าง · รออนุมัติ · อนุมัติแล้ว · **ยืนยันแล้ว** · ไม่อนุมัติ · ยกเลิก · ถอน |
| **ผู้ขอ — ชื่อ** | `employee.full_name` (snapshot) | text | ✓ | soft ref จาก Employee Master (LD-4C-02) |
| ผู้ขอ — รหัส/ตำแหน่ง/แผนก | `employee.code` · `position` · `department` (snapshot) | inline คั่น `·` | ✓ | 1 บรรทัด |
| ผู้ขอ — กะประจำ · โทร | `shift` snapshot (จาก Attendance) · `employee.phone` | inline | ⬜ | **กะเป็นข้อมูลอ่านมาแสดง — ไม่ใช่การจัดกะ** (Shift & Roster เป็นเจ้าของ) |
| **กล่องเพดาน — พาดหัว** | computed จาก `over_cap` | `เกินเพดานรายสัปดาห์ — ต้องอนุมัติเพิ่มอีก 1 ขั้น` / `อยู่ในเพดานรายสัปดาห์` | ✓ | **ถ้าไม่เกินเพดาน ให้ใช้พาดหัวแบบปกติและซ่อนบรรทัด "เกิน N ชม."** |
| กล่องเพดาน — สะสมสัปดาห์ | computed §3.5 + `week_of` | `#,##0.00` ชม. | ✓ | ขอบสัปดาห์ตาม `period_rule` (OQ-OT-09) |
| **กล่องเพดาน — เพดาน** | **`cap_snapshot_hours_week`** (snapshot จาก HR Config `ot_rate.cap_hours_week`) | `#,##0.00` ชม. | ✓ | **บังคับพิมพ์ค่าที่ใช้ตัดสินจริง** — พิสูจน์ว่าตัดสินด้วยเวอร์ชันไหน · **ห้าม hardcode ตัวเลข** (P-8 · BR-09) |
| **ตาราง: บรรทัด OT (loop)** | `ot_request_line[]` | 1 row = 1 ช่วงเวลา | ✓ | เรียงตามวันที่-เวลา |
| ตาราง: วันที่ · ช่วงเวลา | `line.work_date` + `line.time_from`–`line.time_to` | "จันทร์ 14 กันยายน 2569 · 18:00–21:00" | ✓ | กรณีข้ามคืนให้เติม "(ข้ามวัน)" ต่อท้ายเวลา |
| ตาราง: ประเภทวันและอัตรา (`.sub`) | `line.day_type` + `line.rate_type` + `line.multiplier` + `line.payroll_code` (ทั้งหมด snapshot) | "วันทำงานปกติ · อัตรา OT วันทำงาน ×1.5 · รหัสจ่าย OT01" | ✓ | **ชื่ออัตราและตัวคูณ ณ เวลาสร้าง** — อัตราที่ถูกปิดใช้ต้องยังพิมพ์ได้ (C-5 · BR-23) |
| ตาราง: ชม. ที่ขอ | `line.hours_requested` | `#,##0.00` ชิดขวา | ✓ | คำนวณจากช่วงเวลา หักพักตามกะ |
| ตาราง: ชม. ที่รับรอง | `line.hours_confirmed` (หรือ `line.hours_approved` เมื่อยังไม่ยืนยัน) | `#,##0.00` ชิดขวา | ✓ | **ต้องพิมพ์คู่กับ "ชม. ที่ขอ" เสมอ** เพื่อให้เห็นว่าถูกตัดตรงไหน (S-17 · FN-31) |
| **เหตุผลความจำเป็น** | `ot_request.reason` | ข้อความ | ✓ | **Confidential** — พิมพ์บนใบได้ (ใบเป็นของผู้ขอ) แต่ **ห้ามส่งออกใน payload NTF/CSQ** |
| **งานที่ทำ** | `ot_request.work_done` | ข้อความ | ✓ | **Confidential** — เงื่อนไขเดียวกัน |
| การยืนยันเวลาจริง | computed จาก `line.attendance_outside_hours` · `line.variance_hours` | ข้อความสรุปส่วนต่าง | ✓ | ระบุว่าตรง/ไม่ตรงกับชั่วโมงนอกกรอบกะที่บันทึกไว้ · **ถ้ายังไม่ยืนยัน ให้พิมพ์ "ยังไม่ยืนยันเวลาจริง"** (S-21 · S-22 · BR-08) |
| อ้างอิงเวอร์ชันนโยบาย | `ot_request.config_version_ids.ot_rate` | text | ✓ | **บังคับพิมพ์** — พิสูจน์ว่าคิดจากอัตราเวอร์ชันไหน (C-2 · BR-03) |
| หมายเหตุสายอนุมัติ | computed จาก `over_cap` + `approval_chain.length` | ข้อความ | ✓ | ระบุจำนวนขั้นที่ผ่าน · **ช่องเซ็นช่องที่ 4 ปรากฏเฉพาะใบที่เกินเพดาน** |
| หมายเหตุไม่มีเงิน | คงที่ | ข้อความ | ✓ | "เอกสารนี้ไม่แสดงจำนวนเงิน — การคำนวณค่าล่วงเวลาเป็นหน้าที่ของระบบเงินเดือน" (BR-18) |
| **ชั่วโมงที่ขอรวม** | `ot_request.hours_requested_total` | `#,##0.00` | ✓ | Σ `line.hours_requested` |
| **ชั่วโมงที่อนุมัติรวม** | `ot_request.hours_approved_total` | `#,##0.00` | ✓ | Σ `line.hours_approved` |
| **สะสมสัปดาห์ / เพดาน** | computed / `cap_snapshot_hours_week` | `#,##0.00 / #,##0.00` | ✓ | คู่กันเสมอ |
| **ชั่วโมง OT ที่รับรอง (ชม.)** | `ot_request.hours_confirmed_total` | `#,##0.00` | ✓ | แถบ navy (ตำแหน่งเดียวกับ "รวมทั้งสิ้น" ของเอกสารตระกูลตาราง) · **หน่วยชั่วโมง ไม่ใช่เงิน** |
| **ลายเซ็น 1** | ผู้ขอ — `employee` | ชื่อ · ตำแหน่ง | ✓ | |
| **ลายเซ็น 2** | ผู้บังคับบัญชา — **slot 1 จาก `approval_chain`** | ชื่อ · ตำแหน่ง | ✓ | **ชื่อจริงที่ DOA resolve ไม่ใช่ช่องว่างลอย** (มติ 2026-08-17 · FN-37) |
| **ลายเซ็น 3** | ฝ่ายบุคคล — **slot 2 จาก `approval_chain`** | ชื่อ · ตำแหน่ง | ✓ | |
| **ลายเซ็น 4** ⭐ | ผู้บริหารต้นสังกัด — **slot 3 จาก `approval_chain`** | ชื่อ · ตำแหน่ง | **✓ เฉพาะเมื่อ `over_cap = true`** | **ซ่อนทั้งช่องเมื่อใบอยู่ในเพดาน** — ไม่ปล่อยช่องว่างลอย |

## 3. กติกาคำนวณ (ไม่มีสูตรเงิน)

- `line.hours_requested` = ช่วงเวลา (`time_to − time_from`) **หักช่วงพักตามกะที่ทับซ้อน** · กรณีข้ามเที่ยงคืนให้บวก 24 ชม. ก่อนหัก และ `work_date` = **วันเข้ากะ** (LD-01 · S-03)
- **การปัดเศษ/หน่วยขั้นต่ำ:** ต้องอ่านจาก HR Configuration — **ค่านี้ยังไม่ถูกเผยแพร่** (`ot_rate` มีแค่ `multiplier` · `base` · `cap_hours_week` · `payroll_code`) → **รอบนี้ใช้ค่าดิบไม่ปัด** (BR-30 · **OQ-OT-16**) · **ห้ามใส่ตัวเลขปัดเศษลงโค้ด**
- `hours_requested_total` = Σ `line.hours_requested` · `hours_approved_total` = Σ `line.hours_approved` · `hours_confirmed_total` = Σ `line.hours_confirmed` — **3 ตัวเลขอยู่คู่กัน ไม่เขียนทับกัน**
- `over_cap` = (ชั่วโมงสะสมของสัปดาห์ **>** `cap_snapshot_hours_week`) — **ค่าเพดานมาจาก `hr-config/resolve(date=work_date, company_id)` เท่านั้น** (BR-09 · P-8)
- **ไม่มี** `subtotal` / `VAT` / `grand_total` / `จำนวนเงินตัวอักษร` / `hours × multiplier × rate` — เอกสารนี้ไม่มีเงิน (`baht_text.py` **ไม่ใช้**)
- อัตรา · ประเภทวัน · ปฏิทินวันหยุด · กะ · งวด resolve ด้วย `date = วันที่ทำ OT` (ไม่ใช่วันนี้) + `company_id` (C-1 · BR-02)

## 4. กติกาการพิมพ์ (ตาม Design Rules — locked ใน `base.css`)

- A4 แนวตั้ง · lean type 9pt · หัวตาราง + แถบยอดรวม = แถบ navy ตัวอักษรขาว · **ลายเซ็น + footer อยู่ใน `.doc-bottom`**
- หัวตารางซ้ำทุกหน้า (`thead { display:table-header-group }`) — จำเป็นเมื่อใบมีหลายบรรทัด (เช่น ขอ OT ทั้งเดือนในใบเดียว → หลายหน้า)
- ห้ามตัด row กลาง (`tr { break-inside:avoid }`) · บล็อกลายเซ็นห้ามขึ้นหน้าใหม่แยกจากเนื้อหา (`.signs { break-inside:avoid }`)
- footer "หน้า X / N" — ต้อง bind จริงเมื่อเอกสารเกิน 1 หน้า
- **จำนวนช่องลายเซ็นต้องมาจาก `approval_chain.length` ที่ resolve ได้จริง (2+1 หรือ 3+1)** — ห้ามวาด 3 หรือ 4 ช่องตายตัว
- **สำเนา:** เก็บอัตโนมัติเมื่ออนุมัติครบสาย ผ่าน `ENG-DOC-STORE.store(pdf,'OT',ot_request_id,'approved_final')` — **render จากข้อมูล ณ เวลาอนุมัติ ห้าม re-render จากข้อมูลปัจจุบัน** (`DOCCFG_BRIEF §3`)

## 5. Placeholder ที่ใช้ใน `sample.pdf` (ต้องแทนด้วยข้อมูลจริงตอน bind)

| ช่อง | ค่าใน sample | หมายเหตุ |
|---|---|---|
| ชื่อ/ที่อยู่/โทร/อีเมลบริษัท | บริษัท ทูบี ซิมเปิล จำกัด · 99/1 อาคารทูบี … | **placeholder มาตรฐาน 2BSimple** |
| โลโก้ | `.doc-logo--ph` ("2B") | แทนด้วย `<img class="doc-logo" src="data:image/png;base64,…">` เมื่อมีโลโก้จริง |
| ผู้ขอ / ผู้อนุมัติ 3 ชั้น | สมชาย ใจดี · วราภรณ์ ศรีสุข · อนุชา พูนทรัพย์ · จิราภรณ์ วงศ์ทอง | ชุด mock เดียวกับ PREBRIEF §8 (M-3 = ใบที่เกินเพดาน) |
| เลขที่ · วันที่ · ประเภท | `OT-2026-0003` · 10 ก.ย. 2569 · ขอล่วงหน้า | ตรงกับ mock M-3 |
| **อัตราและตัวคูณ** | OT วันทำงาน ×1.5 (OT01) · ทำงานวันหยุด ×1.0 (HL01) · OT วันหยุด ×3.0 (OT03) | **เป็นค่าที่ mock ว่าอ่านมาจาก ตั้งค่า HR — ไม่ใช่ค่าที่ตั้งในเอกสารนี้** · ระบบจริงต้อง resolve ทุกครั้ง (BR-01) |
| **เพดาน 36.00 ชม./สัปดาห์** | ค่าใน sample | **เป็นค่าที่ mock ว่ามาจาก `ot_rate.cap_hours_week` — ห้ามลอกเป็นค่าคงที่ลงระบบจริง** (P-8 · เทียบเคียง `OT_MIN` ของ F-HR-CONFIG ที่ถูกสั่งให้ย้ายเข้า `T_hr_legal_minimum`) |
| เวอร์ชันนโยบาย | `HRCFG-OT-2026-007` | รูปแบบ id จริงมาจาก HR Configuration |
| ช่องลายเซ็นที่ 4 | **แสดงใน sample** (เพราะ sample เป็นใบที่เกินเพดาน) | **ใบที่อยู่ในเพดานต้องซ่อนช่องนี้ทั้งช่อง** |

## 6. วิธี build ใหม่ (regenerate)

```bash
cd .claude/skills/thai-doc-pdf-generator
python3 scripts/build_html.py <BODY.html> --title "ใบขอทำงานล่วงเวลา · Overtime Request Form" \
        -o <out>/template.html
# เครื่องนี้ไม่มี Chromium (CDN ถูกบล็อก) → render ด้วย WeasyPrint แทน render_pdf.py
python3 -c "import weasyprint; weasyprint.HTML('<out>/template.html').write_pdf('<out>/sample.pdf')"
pdfinfo <out>/sample.pdf        # ต้องได้ Pages: 1 · Page size: 595.276 x 841.89 pts
pdftoppm -png -r 100 <out>/sample.pdf prev && ตรวจภาพด้วยตา
```
- ไฟล์ body ต้นทางของรอบนี้เก็บไว้ที่ `briefs/W2/F-HR-OT/_lane/PDFDOC_BODY.html` · ภาพตรวจที่ `briefs/W2/F-HR-OT/_lane/QC/shots/pdfdoc_sample.png`
- **แก้เนื้อหา = แก้ body แล้ว build ใหม่** — ห้ามแก้ `template.html` ตรง ๆ (head/CI/ฟอนต์ถูก inject โดย script)
