# PRINT SPEC — ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม (CAR)

> เอกสารประกอบสำหรับ Dev — คู่กับ FRD/UI Brief ของ F-TMP-008 · โหมด **Replica** (แบบฟอร์มลูกค้า FM-CCC-04) · **2 หน้า (thai-doc R10)**
> ไฟล์คู่: `CAR_template.html` (master, fonts ฝัง) · `form.tpl.html` (template logic-less · สร้างจาก `.scratch/make_tpl.py`) · `*.data.json` (5 สถานะ · `make_data.py`) · `out/*.html`
> ⚠️ **[NO-BROWSER]** เครื่องที่ทำงานไม่มี browser → ยังไม่ได้ render PDF/PNG ด้วย `render_states.py` และยังไม่รัน `compare_original.py` — ต้องรันรอบเต็มบนเครื่องที่มี browser (`--max-pages 2`)
> ทุกมติที่อ้าง = AI-DEFAULT รอลูกค้ายืนยัน (DECISIONS.lock)

## 1. สรุป
- **ประเภทเอกสาร:** ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม Corrective Action Request (CAR) · Doc. No. FM-CCC-04 · Rev.00 : 01/07/2569
- **ขนาด:** A4 แนวตั้ง **2 หน้า** — ต้นฉบับเป็นชีต Excel แนวนอนหนาแน่น (print area A1:AM66 scale 45% → ตัวอักษรบนกระดาษเล็กกว่า 8pt) · 87 ช่อง · 18 กลุ่มแถวซ้ำ (แถวว่างรวม ~140 แถว) · ลงนาม 11 จุด → เข้าเงื่อนไข R10 (dense แล้วยัง < 8pt)
- **ฟอนต์:** Sarabun 8pt (ต่ำสุดในเนื้อฟอร์ม · ไม่บีบต่ำกว่า 8pt) · line-height 1.2 · หมึกเดียว · หัวคอลัมน์ไม่ระบายพื้น (ตามกระดาษ)
- **Renderer:** Playwright/Chromium (`prefer_css_page_size`, `print_background`)

## 2. โครง 2 หน้า (จุดตัดหน้าตั้งใจ)
| หน้า | เนื้อหา |
|---|---|
| 1 | หัว (โลโก้ · ชื่อเอกสาร · P-CAR No. · DOC NAME · DOC NO. · หน่วยงาน · ผู้พบปัญหา · วันที่/เวลาที่พบปัญหา) · รายงานสภาพผิดปกติโดยทันที (1 · 2 · ตาราง 3 + 6.3 + รวม) · ผู้เข้าร่วมประชุม · 4 (หัวข้อ · หมายเลขเอกสารที่ใช้ในการวิเคราะห์ · (…ภายใน N นาที)) · การจัดทำ ทำไม 1/2 · การตรวจสอบ ทำไม 1/2 · การจัดทำ ทำไม 3/สาเหตุรากเหง้า · "มีต่อหน้าถัดไป" |
| 2 | หัวย่อ (ชื่อเอกสาร + P-CAR No.) · การตรวจสอบ ทำไม 3/สาเหตุรากเหง้า · 5 (D) 5.1/6.1 การจัดทำ│การตรวจสอบ + กำหนดเสร็จ/ผู้รับผิดชอบ + ตรวจสอบโดย HOD│IC Mgr · 5.2/6.2 + 6.1ตรวจสอบโดย MD│IC Mgr. · 7 (A) เฉพาะกรณี/ทั้งระบบ · 8 · 9 · 10 + IC Mgr · 11 MD/IC Mgr. · 12 บล็อกลงชื่อ DOA ทั้งก้อน (`.signs-block`) |
- `.page-break` ที่ `.doc-page` หน้า 2 · หัวตารางทุกบล็อกอยู่ใน `<thead>` (ซ้ำเมื่อข้ามหน้า) · แถว `break-inside:avoid` · footer ทุกหน้า: เลขที่ · (ร่าง) · CUBE NATIVE │ Doc. No. · Rev. · "หน้า n/2"
- ตาราง 24 คอลัมน์เท่ากัน · ความกว้างแต่ละช่องกำหนดด้วย colspan (ไม่มี style ใน body)

## 3. Field Mapping (ย่อ — ครบ 87 ช่องตาม FORM_SPEC)
| ช่องในเอกสาร | Source | Format | หมายเหตุ |
|---|---|---|---|
| P-CAR No. | ENG-DOC-NUM · doc_type CAR | `CAR-พ.ศ.-running` | ออกตอนบันทึกครั้งแรก (DEC-27) |
| DOC NAME / DOC NO. | car.doc_name / car.doc_ref_no | ข้อความ | ผู้ใช้กรอกเลขอ้างอิงเอง (DEC-01 · G1) |
| หน่วยงาน · ผู้พบปัญหา | Department snapshot · car.finder | | PDPA |
| วันที่/เวลาที่พบปัญหา | car.found_at | วันที่ไทย · `HH:MM น.` | อนาคต = บล็อก (DEC-04) |
| 1 · 2 | car.problem · car.kpi_target | | |
| จำนวนทั้งหมด … รายการ | car.total_qty | จำนวนเต็ม | |
| ตาราง 3 (+6.3) | car_symptoms[] | เกิดใหม่ = ☑/☐ · % = จำนวน ÷ จำนวนทั้งหมด × 100 (2 ตำแหน่ง) | ขั้นต่ำ 5 แถว (DEC-05) · เกิดใหม่↔เกิดซ้ำครั้งที่ (DEC-34) |
| รวม | Σ จำนวน · Σ % · Σ 6.3 จำนวน · Σ 6.3 % | คำนวณใน data | Σ > จำนวนทั้งหมด = เตือน (DEC-33) |
| ผู้เข้าร่วมประชุม 1.:–8.: | car_attendees[] | เรียงตามกระดาษ (1,2 คอลัมน์แรก · 3,4 …) | ขั้นต่ำ 8 (DEC-06) · ป้าย '7.;' → '7.:' (DEC-29) |
| หมายเลขเอกสารที่ใช้ในการวิเคราะห์ | car.analysis_doc_no | | |
| (วิเคราะห์สาเหตุและเริ่มดำเนินการภายใน N นาที) | CarConfig.analysis_start_minutes | ค่าเริ่ม 30 | ค่าคงที่อ่านจาก config (DEC-04) |
| ทำไม 1/2/3 · สาเหตุรากเหง้า × (การจัดทำ/การตรวจสอบ) | car_causes[] (level, phase) | ผล = "จริง"/"ไม่จริง" | ขั้นต่ำ 7 แถว/กลุ่ม (DEC-07…14) · ช่วงการตรวจสอบ = IC (DEC-31) |
| 5.1/6.1 · 5.2/6.2 · 7 (A) | car_actions[] (kind, phase) | กำหนดเสร็จ `dd/mm/yy` (พ.ศ.) | ขั้นต่ำ 6 · 5 · 3+4 แถว (DEC-15…20) |
| 8 · 9 · 10 | car_docs_to_fix[] · car.risk_* · car_doc3_checks[] | | ขั้นต่ำ 3 · – · 3 (DEC-21/22) |
| จุดลงนามตรวจสอบ 7 จุด | car_review_signs (hod · icm_d · md_61 · icm_61 · icm_10 · md_11 · icm_11) | ชื่อ + `dd/mm/yy` · ว่าง = เส้นจุด | ไม่ใช่ DOA (DEC-04 ส่งอนุมัติต้องครบ 7) |
| 12 (อนุมัติ) | approval_chain[] (DOA) | ☑ อนุมัติ / ☑ ไม่อนุมัติ + "พิจารณาในระบบ …" | 1 ช่อง/ขั้น ค่าเริ่ม 4 (DEC-03/24) · ไม่มีช่องผู้จัดทำ |

## 4. กติกาคำนวณ (ใน data — template ไม่มีสูตร)
- `%` = qty ÷ total × 100 → `#,##0.00` · แถวว่างเว้นทุกช่อง (ไม่ใส่ 0) · `sum.*` ว่างถ้าไม่มีแถว
- แถวซ้ำเติมแถวว่างจนครบขั้นต่ำตามกระดาษ (`print_config.group_min_rows`) · กลุ่มที่วางคู่ซ้าย-ขวา (การจัดทำ│การตรวจสอบ / ทำไม 1│2 / ทำไม 3│รากเหง้า) zip เป็น `{a,b}` / `{p,r}` ยาวเท่าฝั่งที่ยาวกว่า
- `analysis_note` สร้างจาก CarConfig · `doc3_rows[0].first/span` = ช่องลงนาม IC Mgr ข้อ 10 (rowspan) · `docs_rows` = 3 ช่อง/แถว

## 5. วิธี build ใหม่
```bash
python3 ../.scratch/make_tpl.py form.tpl.html          # (ถ้าแก้โครง) สร้าง template
python3 make_data.py                                   # data 5 สถานะ (ข้อมูลสมมติทั้งหมด)
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม" --max-pages 2
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.5
```

## 6. Checklist
- [x] parity JS ↔ Python IDENTICAL 5/5
- [x] ไม่มี {{…}} หลง · ไม่มี key ขาด (ทุกสถานะ)
- [x] ตัวอักษรเนื้อฟอร์ม ≥ 8pt (Sarabun 8pt · footer/หมายเหตุใช้ขนาดกลางของสกิล)
- [ ] A4 2 หน้า ทุกสถานะ — **[NO-BROWSER] ยังไม่ยืนยันด้วย render_states บนเครื่องงาน** (ตรวจเบื้องต้นนอกเครื่องงานด้วย Chromium: 5/5 สถานะ = 2 หน้า · หน้า 2 สถานะ DOA 6 ขั้นสูงสุด 256/269 มม. — ไม่ใช่ผลด่านทางการ)
- [x] บล็อกลงชื่อข้อ 12 ไม่ถูกตัด (`.signs-block`) · 1 ช่องต่อขั้น DOA แถวละ ≤4

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `4. FM-CCC-04 ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม Corrective Action Request (CAR).xlsx` · footer Doc. No. : FM-CCC-04 · Rev.00 : 01/07/2569
- Profile: form_fs 8pt · form_lh 1.2 · form_grid_row_h 4.4mm · form_grid_pad 2px · head_bg #FFFFFF · logo 8mm
- ความต่างที่ตั้งใจ: (1) 1 หน้าแนวนอนหนาแน่น → 2 หน้าแนวตั้ง (R10) · บล็อกที่กระดาษวางเคียงกัน 3 คอลัมน์ (ทำไม 3│รากเหง้า│5 D และ 5.2/6.2│7│8–12) แยกเป็นแถวคู่ซ้าย-ขวา (2) ป้ายแนวตั้ง 'รายงานสภาพผิดปกติโดยทันที' / 'การจัดทำ' / 'การตรวจสอบ' → หัวแถว/หัวบล็อกแนวนอน (ไม่มี class หมุนตัวอักษร) (3) ข้อ 1/2 เต็มความกว้างเหนือตาราง 3 (กระดาษวางซ้ายตาราง) · หัว P-CAR/DOC NAME/DOC NO./หน่วยงาน… รวมเป็น 3 แถวบนสุด (4) ข้อ 8 แสดง 3 รายการ/แถว (5) ลงนาม IC Mgr ข้อ 10 อยู่ช่องซ้ายของตาราง Doc No./Result (6) ข้อ 12 = แถวช่องลงชื่อ 1 ช่อง/ขั้น DOA (ค่าเริ่ม 4 ตามกระดาษ) ใต้ชื่อ = (ชื่อ) + "พิจารณาในระบบ …" (7) วันที่ในตาราง `dd/mm/yy` (พ.ศ.) ตามรูปแบบ "../../.." บนกระดาษ (8) footer เลขที่/ร่าง + Doc. No. · Rev. + หน้า n/2 (9) ป้าย '7.;' → '7.:' (DEC-29) · ป้าย 6.1 ซ้ำคงตามกระดาษ (DEC-30)
- ข้อจำกัด: ข้อความยาวมาก/แถวเกินขั้นต่ำในหลายกลุ่มพร้อมกัน ทำให้แถวสูงขึ้น → อาจเกิน 2 หน้า (หัวตารางซ้ำ · แถวไม่ถูกตัด) → OQ ลูกค้า: ยอมรับหน้า 3 "ใบต่อ" หรือไม่
- compare_original: **[NO-BROWSER] ข้าม** (ต้องมี approved.pdf) — layout เปลี่ยนตั้งใจจากแนวนอน→แนวตั้ง 2 หน้า คาดว่า WARN (อธิบายตามข้อ 7)

## 8. (Replica) Data contract + สถานะ
| key | Source | ตัวอย่าง |
|---|---|---|
| `company.name` · `company.logo` | Organization header_snapshot | data URI |
| `doc.title` · `doc.title_full` · `doc.no` · `doc.is_draft` · `doc.form_code` · `doc.revision` | ค่าคงที่ · ENG-DOC-NUM · status · print_config | `CAR-2569-0001` |
| `head.{doc_name, doc_ref_no, dept, finder, found_date, found_time}` | car.* | `10 ตุลาคม 2569` · `09:15 น.` |
| `problem` · `kpi_target` · `total_qty` | car.* | |
| `symptoms[].{no,symptom,new_box,repeat_no,qty,pct,c_qty,c_pct}` · `sum.{qty,pct,c_qty,c_pct}` | car_symptoms | `☑` · `15.00` |
| `attendee_rows[].{label, cells[].{no,name}}` | car_attendees | `1.:` |
| `analysis_doc_no` · `analysis_note` | car · CarConfig | |
| `w12_prep` · `w12_rev` · `w3r_prep` · `w3r_rev` → `[{a:{no,cause,method,result}, b:{…}}]` | car_causes (level 1/2/3/root × phase) | `จริง` |
| `act_rows[{p:{no,fix,eff}, r:{…}}]` · `act_due.{p,r}.{due,owner}` | car_actions kind=immediate | |
| `fix_rows[{p:{fix,result}, r}]` · `fix_due` | car_actions kind=fix | |
| `prev_rows[{p:{scope,text,owner,due}, r}]` | car_actions kind=prevent scope=case/system | `เฉพาะกรณี` |
| `docs_rows[].{label, cells[].{no,text}}` · `risk.{subject,old,new,due}` · `doc3_rows[].{no,doc_no,result,first,span}` | car_docs_to_fix · car.risk_* · car_doc3_checks | |
| `rv.{hod,icm_d,md_61,icm_61,icm_10,md_11,icm_11}.{name,date}` | car_review_signs | เส้นจุดเมื่อยังไม่ลงนาม |
| `sign_rows[].signs[].{role,name,date,decision}` | approval_chain (DOA) | sign_rows.py `build_signs()[1:]` + `chunk_signs` |

- parity: IDENTICAL 5/5
- สถานะ: draft (ช่วงการตรวจสอบว่าง · จุดลงนามเส้นจุด · DOA รอ) · approved (ครบ 4 ขั้น) · rejected (MD ไม่อนุมัติ) · long-text (เต็มความจุกระดาษทุกกลุ่ม + ข้อความยาว) · approved-doa6steps (6 ช่อง 3+3) → HTML ครบ · PDF [NO-BROWSER]

## 9. (Replica) print_config
ดู `print_config.json` (doc_type CAR · pages 2 · group_min_rows · review_points 7 · sign_boxes `doa_step:*` · decision_words default อนุมัติ/ไม่อนุมัติ · config_reads analysis_note)
