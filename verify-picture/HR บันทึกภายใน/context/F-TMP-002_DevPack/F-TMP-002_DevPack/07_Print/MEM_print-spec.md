# PRINT SPEC — บันทึกภายใน (MEM)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-TMP-002
> ไฟล์คู่: `MEM_template.html` (master, fonts ฝัง) + `out/<state>.html` (ตัวอย่างทุกสถานะ)
> **โหมด: Replica** (แบบฟอร์มลูกค้า FM-HRM-54) — กรอก §7–§9 ครบ

## 1. สรุป
- **ประเภทเอกสาร:** บันทึกภายใน / Internal Memo
- **ขนาด:** A4 แนวตั้ง (210×297mm) ขอบ 14mm
- **ฟอนต์:** Sarabun (ฝัง base64 ใน HTML)
- **CI:** Replica = หมึกเดียวตาม profile ลูกค้า (ไม่ใช้สี CI CUBE ในเนื้อฟอร์ม)
- **Renderer ที่ใช้สร้าง PDF:** Playwright/Chromium → `print_background`, `prefer_css_page_size`
- ⚠️ **รอบนี้รันในโหมด NO-BROWSER** — ยังไม่ได้ออก PDF จริง (ดู §8)

## 2. Field Mapping (UI/DB → ช่องในเอกสาร)

| ช่องในเอกสาร | Source (entity.field) | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| วันที่ | `memo.doc_date` (F01) | วัน เดือน(ไทย) พ.ศ. | ✓ | ระบบใส่ตอนบันทึกครั้งแรก แก้ได้ก่อนส่ง |
| เรียน | `memo.to` (F02) | ข้อความ | ✓ | ผู้ใช้กรอก ไม่ผูก user ในระบบ |
| จาก | `memo.from` (F03) ← `Employee.full_name · Employee.department_name` | ข้อความ | ✓ | ค่าเริ่มจากผู้สร้างเอกสาร |
| เรื่อง | `memo.subject` (F04) | ข้อความ | ✓ | |
| เลขที่ | `memo.doc_no` (F05) | `MEM-{พ.ศ.}-{run:4}` | ✓ | ENG-DOC-NUM เท่านั้น |
| (พื้นที่เนื้อหาบันทึก) | `memo.body` (F06) → `body_lines[]` | ย่อหน้า | ✓ | backend แตกย่อหน้าให้ |
| ข้อคิดเห็นฝ่ายกฎหมาย | `memo.legal_opinion` (F07) → `legal_lines[]` | บรรทัดเส้นประ ≥2 | — | กรอกโดยผู้พิจารณาเท่านั้น |
| ช่องลงชื่อ | `approval_chain` (DOA snapshot) → `sign_rows[]` | — | ✓ | 1 ช่องต่อขั้น · ไม่มีช่องผู้ขอ |
| วันที่ (ในบล็อกลงชื่อ) | `memo.legal_opinion_date` (F08) | `พิจารณาในระบบ …` | — | คนละช่องกับ F01 (DEC-13) |

## 3. กติกาคำนวณ
- **ไม่มี** — ฟอร์ม FM-HRM-54 ไม่มีสูตร ไม่มีค่าคงที่ ไม่มียอดเงิน (FORM_SPEC `formulas` = 0 · `constants` = 0)

## 4. กติกาการพิมพ์
- A4 แนวตั้ง · เนื้อหา 9.6pt · กรอบหัวกระดาษ/กรอบข้อคิดเห็นเป็นตารางเส้นทึบ (`form-grid`) ตามต้นฉบับ
- บล็อกลงชื่อห้ามถูกตัดข้ามหน้า (`.signs-block { break-inside:avoid }`)
- ช่องลงชื่อแถวละ ≤4 ช่อง แบ่งเฉลี่ย · ขั้น > 4 → `layout.dense`
- footer ซ้าย = เลขที่ + "· ร่าง" เมื่อเป็นร่าง · footer ขวา = `Doc No. FM-HRM-54 · Rev.00 : 01/07/2569`

## 5. วิธี build ใหม่ (regenerate)
```bash
S=_system/skills/pack/thai-doc-pdf-generator/scripts
python3 $S/parity_check.py print/form.tpl.html print/*.data.json
python3 $S/render_states.py print/form.tpl.html print/*.data.json -o print/out \
        --mode replica --profile print/profile.json --title "บันทึกภายใน"
python3 $S/compare_original.py orig/SAMPLE.pdf print/out/approved.pdf -o print/out/compare
python3 $S/build_html.py print/form.tpl.html --mode replica --profile print/profile.json \
        --title "บันทึกภายใน" -o print/MEM_template.html
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity JS ↔ Python IDENTICAL ทุกไฟล์
- [x] ไม่มี `{{}}` หลงเหลือทุกสถานะ
- [x] ลายเซ็นครบตามสาย (1 ช่องต่อขั้น · ทดสอบถึง 6 ขั้น)
- [ ] **A4 พอดี ไม่ล้นหน้า** — ยังตรวจไม่ได้ (NO-BROWSER)
- [ ] **เทียบต้นฉบับ (compare_original)** — ยังตรวจไม่ได้ (NO-BROWSER)

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `orig/บันทึกภายใน.doc` → `orig/SAMPLE.pdf` (แปลงด้วย LibreOffice) · Doc No. `FM-HRM-54` · `Rev.00 : 01/07/2569`
- Profile `profile.json` — token ที่ต่างจาก default:
  - `form_title_gap: 4px` (ชื่อเอกสารอยู่ในกรอบหัวกระดาษ ไม่ได้อยู่กลางหน้าโล่ง)
  - `form_logo_h: 14mm` (ขนาดโลโก้ตามต้นฉบับ)
  - `form_num_w: 18mm` (ป้ายหัวบรรทัด วันที่/เรียน/จาก/เรื่อง/เลขที่ กว้างเท่ากัน ให้ `:` ตรงแนวเหมือนต้นฉบับ)
  - `form_grid_row_h: 7mm` (ความสูงกรอบ)
- **ความต่างจากกระดาษ (ตั้งใจ + เหตุผล)**
  1. **บล็อกลงชื่อเป็นช่องตาม DOA** — กระดาษมีช่องลงชื่อ "ฝ่ายกฎหมาย" 1 ช่องตายตัว · ระบบสร้าง 1 ช่องต่อขั้นที่ตั้งใน DOA กลาง (DEC-03 G2 · DEC-07 G6 · AI-DEFAULT)
  2. **ไม่มีช่องลงชื่อผู้ขอ** — กระดาษไม่มีช่องลงชื่อผู้จัดทำ จึงไม่เพิ่ม (DEC-14 VALID) · ผู้จัดทำยึดจากช่อง "จาก"
  3. **มีคำตัดสิน ☐ อนุมัติ / ☐ ไม่อนุมัติ ในช่องลงชื่อ** — กระดาษ**ไม่มี** ☐ นี้ · ระบบเพิ่มตามมติ G6/DEC-07 เพราะขั้น DOA ต้องแสดงผลพิจารณาบนแบบพิมพ์ · **เป็น AI-DEFAULT รอลูกค้ายืนยัน** (ถ้าลูกค้าไม่ต้องการ ให้ตั้ง `print_config.sign_boxes[].show_decision = false` — ไม่ต้องแก้ template)
  4. **บรรทัดวันที่ใช้ข้อความ "พิจารณาในระบบ …"** แทนการเซ็นด้วยมือ (G6 `handwriting_image: false`)
  5. **footer ซ้าย** เพิ่มเลขที่ + "ร่าง" + "เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" — เป็นสิ่งที่ระบบเพิ่มได้โดยไม่ต้องถาม (form-replica §2)
  6. **เส้นประเปล่ามุมขวาล่างของกรอบข้อคิดเห็น** บนกระดาษ ไม่ได้ทำเป็นช่องกรอก (DEC-12 VALID)
- **ผล compare_original:** ⚠️ **ยังไม่ได้รัน — รอบนี้เครื่องอยู่ในโหมด NO-BROWSER** (`[NO-BROWSER] ข้าม compare_original.py`)
  - ต้องรันรอบเต็มบนเครื่องที่มี browser แล้วดู `print/out/compare/compare_side.png` ก่อนส่งลูกค้า · region ที่แนะนำ `--region 0:0.72` (ตัดส่วนบล็อกลงชื่อที่ตั้งใจเปลี่ยน)

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `MEM_data-contract.md`
- parity JS ↔ Python: **IDENTICAL 5/5**
- สถานะที่ render (HTML ครบ · PDF ยังไม่ได้ออก):

| ไฟล์ | สถานะ | ช่องลงชื่อ | เนื้อหา | dense |
|---|---|---|---|---|
| `draft` | ร่าง (footer มี "· ร่าง") | 1 ช่อง · ☐/☐ · `วันที่ ..../..../....` | 3 ย่อหน้า | — |
| `approved` | อนุมัติแล้ว | 1 ช่อง · ☑ อนุมัติ · "พิจารณาในระบบ …" | 3 ย่อหน้า | — |
| `rejected` | ไม่อนุมัติ | 1 ช่อง · ☑ ไม่อนุมัติ | 2 ย่อหน้า | — |
| `long-12rows-3signs` | เนื้อหายาว + สายหลายขั้น | 3 ช่อง 1 แถว | 14 ย่อหน้า (รายการ 12 รายการ) | ✓ |
| `doa-6steps` | DOA 6 ขั้น | 6 ช่อง **2 แถว (3+3)** | 2 ย่อหน้า | ✓ |

- ⚠️ **จำนวนหน้า:** ยังยืนยันไม่ได้ว่าทุกสถานะอยู่ใน 1 หน้า (NO-BROWSER) — ต้องรัน `render_states.py --max-pages 1` บนเครื่องที่มี browser
- หมายเหตุ: ฟอร์มนี้ไม่มี repeat group → สถานะ "ยาว" ใช้จำนวน**ย่อหน้าเนื้อหา** แทนจำนวนแถวรายการ

## 9. (Replica) print_config (ค่าเริ่มต้นส่งให้ F-DOCCFG ผ่าน doccfg-declaration)
ดู `print/print_config.json` — สรุปค่าสำคัญ:
- `doc_type: MEM` · `form_code: FM-HRM-54` · `revision: Rev.00 : 01/07/2569` · `paper: A4-portrait`
- `min_rows: 2` (บรรทัดเส้นประของข้อคิดเห็นฝ่ายกฎหมาย — ฟอร์มนี้ไม่มี repeat group ของรายการ)
- `sign_boxes: [{ box: "doa_step:*", label: "from_doa_role", show_decision: true, show_date: true }]` — **ไม่ fix จำนวนขั้น**
- `decision_words.default: { approve: "อนุมัติ", reject: "ไม่อนุมัติ" }` — ยังไม่มี `by_role` override
- `sign_layout: { max_per_row: 4, split: even, dense_when_steps_over: 4, keep_together: true }`
