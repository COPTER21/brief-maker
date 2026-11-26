# PRINT SPEC — แบบฟอร์มชุดเอกสารส่งมอบงาน (IVMF)

> เอกสารประกอบสำหรับ Dev · โหมด **Replica** (แบบฟอร์มลูกค้า FM-IVM-06) · มติ AI-DEFAULT ทั้งหมดรอลูกค้ายืนยัน
> ไฟล์คู่: `แบบฟอร์มชุดเอกสารส่งมอบงาน_template.html` (master, fonts ฝัง) · `form.tpl.html` (logic-less) · `*.data.json` · `out/*.html` (HTML ทุกสถานะ — NO-BROWSER ยังไม่ได้ PDF)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มชุดเอกสารส่งมอบงาน / Handover Document Package Form
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — ต้นฉบับ xlsx 1 หน้า แต่มี 5 หมวดกรอก (ข้อมูลการรับมอบ 6 แถว + ตาราง 8 คอลัมน์ 12 แถว + ข้อตกลงติดตาม 4 แถว + ตารางลงชื่อ + ประวัติการแก้ไข) ที่ฟอนต์ ≥ 8pt และสถานะบังคับ DOA 6 ขั้น (7 แถวลงชื่อ) / รายการยาว 16 แถว เกิน 1 หน้า → ออกแบบ 2 หน้าทุกสถานะเท่ากัน
- **ฟอนต์:** Sarabun 8.5pt (profile · ไม่ต่ำกว่า 8pt) · หมึกเดียว · ตารางกรอบ R9

## 2. Field Mapping
| ช่องในเอกสาร | key (data) | Source (entity.field) | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ (footer + หัวหน้า 2) | doc.no | ENG-DOC-NUM (IVMF) ออกตอนบันทึกครั้งแรก | ✓ | DEC-10 |
| บริษัท … และบริษัทในเครือ | company.name_line | Organization snapshot | ✓ | |
| ชื่อโครงการ | handover.project_name | ivmf.project_name | ✓ | ข้อความอิสระ (DEC-01) |
| ผู้ส่งมอบจากฝ่ายพัฒนาธุรกิจ | handover.sender_name | ivmf.sender_name | ✓ | |
| ผู้รับมอบจากฝ่ายบริหารการลงทุน | handover.receiver_name | ivmf.receiver_name | ✓ | ค่าเริ่ม = ผู้จัดทำ |
| วันที่ / เวลารับมอบ | handover.handover_at | ivmf.handover_at | ✓ | dd/mm/yyyy HH:mm น. |
| ฉบับชุดเอกสาร | handover.package_version | ivmf.package_version | ✓ | |
| ผลการรับมอบ | handover.result | ivmf.handover_result → label | ✓ | รับมอบครบถ้วน / รับมอบแบบมีเงื่อนไข / ยังไม่รับมอบ |
| ผลการตรวจรับเอกสาร (loop ≥ 12 แถว) | items[].seq/doc_name/doc_ref/received/completeness/issue/fix_owner/due_date | ivmf_item.* | ✓ ≥1 แถว | seq ระบบรัน 1, 2, 3 … (DEC-04) · received/completeness = label |
| ประเด็นค้างจากการรับมอบ | followup.open_issues | ivmf.open_issues | เงื่อนไข | บังคับเมื่อ รับมอบแบบมีเงื่อนไข (DEC-15) |
| เอกสาร / ข้อมูลที่ต้องส่งเพิ่มเติม | followup.pending_docs | ivmf.pending_docs | — | |
| กำหนดการติดตาม | followup.schedule | ivmf.followup_schedule | เงื่อนไข | บังคับเมื่อ รับมอบแบบมีเงื่อนไข |
| หมายเหตุจากฝ่ายบริหารการลงทุน | followup.ivm_remark | ivmf.ivm_remark | เงื่อนไข | บังคับเมื่อ ยังไม่รับมอบ |
| การตรวจทาน / อนุมัติ (loop) | sign_rows[].signs[] | requester + approval_chain (sign_rows.py) | ✓ | 1 แถวตารางต่อช่อง · จำนวนตาม DOA |
| ประวัติการแก้ไข (loop) | form_revisions[] | DOCCFG revision ของ IVMF | — | ข้อมูลแบบฟอร์ม ไม่ใช่ข้อมูลใบ (DEC-18) |
| Doc. No. / Rev. | doc.form_code · doc.revision | print_config | ✓ | FM-IVM-06 · Rev.00 : 01/07/2569 |

## 3. กติกาตรวจ (อ้าง DECISIONS.lock)
- ไม่ได้รับ → ความครบถ้วน = ไม่ครบถ้วน (ระบบตั้งให้ · บล็อก ครบถ้วน) (DEC-13)
- แถวที่ไม่ใช่ ได้รับ + ครบถ้วน ต้องมีประเด็นที่พบ · ผู้รับผิดชอบแก้ไข · กำหนดส่งเพิ่มเติม (บล็อกตอนส่ง) (DEC-14)
- รับมอบครบถ้วน → ทุกแถว ได้รับ + ครบถ้วน · รับมอบแบบมีเงื่อนไข → ประเด็นค้าง + กำหนดการติดตาม · ยังไม่รับมอบ → หมายเหตุจากฝ่ายบริหารการลงทุน (บล็อก) (DEC-04/15)
- กำหนดส่งเพิ่มเติม ≥ วันที่รับมอบ (บล็อก) (DEC-16)

## 4. กติกาการพิมพ์
- หน้า 1 = หัว + ข้อมูลกระบวนการ + ข้อมูลการรับมอบ + ผลการตรวจรับเอกสาร · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- หน้า 2 (`.page-break`) = หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + ประเด็นค้างและข้อตกลงการติดตาม + การตรวจทาน/อนุมัติ (`.signs-block` ไม่ตัดข้ามหน้า) + ประวัติการแก้ไข · footer "หน้า 2/2"
- ตารางผลการตรวจรับเอกสารมี `thead` → แถวเกินหน้า หัวตารางซ้ำ · แถวไม่ตัดกลาง

## 5. วิธี build ใหม่
```bash
TD_SCRIPTS=$TD/scripts python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มชุดเอกสารส่งมอบงาน" --max-pages 2   # ต้องมี browser
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o compare --region 0:0.72        # ต้องมี PDF
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · [x] ไม่มี {{}} หลง (render_doc --strict + build_html ทุกสถานะ) · [x] ฟอนต์ ≥ 8pt · [x] ลายเซ็นครบตามสาย DOA (3 / 7 แถว)
- [ ] ทุกสถานะ 2 หน้าเท่ากัน — **[NO-BROWSER] ยังไม่ได้ตรวจ** (render_states/render_pdf ข้าม) → รันรอบเต็มบนเครื่องที่มี browser

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `6. FM-IVM-06 แบบฟอร์มชุดเอกสารส่งมอบงาน.xlsx` (ชีต INV-FM-06) · Doc. No. FM-IVM-06 · Rev.00 : 01/07/2569
- Profile token ที่ต่าง: form_fs 8.5pt · form_title_fs 14pt · form_logo_h 11mm · form_title_gap 2px · form_grid_gap 4px
- ความต่างที่ตั้งใจ: แบ่ง 2 หน้า (R10) · ลำดับแถวระบบรัน (แถวว่างยังพิมพ์เลขต่อจนครบ 12 ตามกระดาษ) · dropdown แสดงเป็นข้อความ label · ตารางลงชื่อวนตาม DOA (ไม่ fix 3 แถว) · ช่องลายเซ็น = ☐/☑ คำตัดสินตาม role + "ส่งในระบบ / พิจารณาในระบบ วันที่ เวลา" (DEC-07) · footer เลขที่ + CUBE NATIVE · โลโก้จาก Organization · แถบหัวหมวดสีน้ำเงินเข้ม → หมึกเดียวตัวหนา · ตัดแถวเว้นว่างคั่นหมวด
- compare_original: **[NO-BROWSER] ข้าม** (ต้องใช้ PDF สถานะ approved) — ต้องรันบนเครื่องที่มี browser แล้วบันทึกคะแนนที่นี่

## 8. (Replica) Data contract + สถานะ
- สถานะ: draft · approved (รับมอบแบบมีเงื่อนไข) · rejected (ส่งกลับ · ยังไม่รับมอบ) · long-16rows (รับมอบครบถ้วน) · approved-doa6steps (ข้อมูลสมมติทั้งหมด)
- parity JS ↔ Python: IDENTICAL 5/5
- print_config: `print/print_config.json` (IVMF · decision_words by_role: role-line-manager = ตรวจสอบแล้ว/ส่งกลับ · role-mgr-bu = รับทราบ/ส่งกลับ)
