# PRINT SPEC — ฟอร์มแจ้งงานขนส่งนอก (OTN) · Replica FM-SAL-16
> โหมด Replica · template `form.tpl.html` (logic-less) · profile `profile.json` · print_config `print_config.json` · data ตัวอย่าง `render_data.py` (ข้อมูลสมมติ · โลโก้ placeholder)
> ⚠️ NO-BROWSER: เครื่องที่ทำงานไม่มี browser → ไม่ได้ render PDF ในชุดนี้ (มี HTML ต่อสถานะใน `out/`) · ต้องรัน `render_states.py … --max-pages 1` + `compare_original.py` ซ้ำบนเครื่องที่มี browser

## 1. หน้ากระดาษ
A4 แนวตั้ง · **1 หน้า** (ต้นฉบับ print area A1:E26 = 1 หน้า · ภาพ LibreOffice แตกคอลัมน์ วันที่นัดส่ง ไปหน้า 2 จากความกว้างคอลัมน์ → แก้ให้อยู่หน้าเดียว DEC-15) · ไม่ต้อง R10 (20 บรรทัด + บล็อกผู้จัดทำ จบ 1 หน้า ตรวจแล้วทุกสถานะ)
- เกิน 20 แถว (DEC-05 ไม่จำกัด) → แถวไหลไปหน้าถัดไปเอง · หัวตารางซ้ำ (thead = table-header-group) · แถวไม่ถูกตัดกลาง · บล็อกผู้จัดทำ `.signs-block` ไม่ถูกตัด = "ใบต่อ" ตาม R10 ข้อสุดท้าย — รอยืนยันว่าลูกค้าต้องการใบต่อหรือแยกใบใหม่ต่อรอบ (OQ)

## 2. Field map → data contract
| ช่องบนกระดาษ | key | source | format |
|---|---|---|---|
| โลโก้ | company.logo | Organization snapshot ตอนออกเลข | data URI |
| ฟอร์มแจ้งงานขนส่งนอก (หัว) | doc.title | FORM_SPEC.form.title | text |
| เส้นประต่อท้ายหัว | carrier_name | otn.carrier_name (เลือกจากผู้ขนส่ง/พิมพ์เอง) | text |
| รอบวันที | round_date_text | otn.round_date | วัน เดือนเต็ม พ.ศ. "15 มีนาคม 2569" |
| ต้นทาง | lines[].origin | otn_line.origin | text |
| ปลายทาง | lines[].destination | otn_line.destination | text |
| เลขที่PO | lines[].po_no | otn_line.po_no | text |
| จำนวน | lines[].qty | otn_line.qty | "#,##0" |
| วันที่นัดส่ง | lines[].delivery_date | otn_line.delivery_date | dd/mm/yyyy พ.ศ. |
| (เติมแถวว่าง) | lines[] | backend เติมจนครบ min_rows 20 | ทุก key = "" |
| ผู้จัดทำ | sign_rows[].signs[] (role/name/date) | sign_rows.py: requester = ผู้บันทึก · date = "ส่งในระบบ dd/mm/yyyy hh:mm" หรือเส้นประเมื่อยังไม่ส่ง | text |
| DOA | approver_role · approved_by · approval_chain | **TODO: DOA engine** — ไม่มีการอนุมัติ (DEC-03) → ว่าง · ถ้าเปิด DOA กลาง ช่องเพิ่มเองจาก chain | — |
| footer ซ้าย | doc.no · doc.is_draft · doc.is_cancelled | ENG-DOC-NUM · สถานะ | "เลขที่ … · ร่าง/ยกเลิก · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" |
| footer ขวา | doc.form_code · doc.revision | print_config | "Doc. No. : FM-SAL-16 · Rev.00 : 01/07/2569" |
| layout.dense | — | แถว > 20 · ข้อความต้นทาง/ปลายทาง > ~30 ตัวอักษร · ขั้น DOA > 4 | bool (เงื่อนไข section เท่านั้น) |

## 5. สถานะที่ทำ (parity IDENTICAL 5/5 · ไม่มี {{}} หลง · ไม่มี key ขาด)
| สถานะ | สิ่งที่ต้องเห็น |
|---|---|
| draft | footer "· ร่าง" · 3 แถว · ผู้จัดทำเส้นประวันที่ |
| submitted | 8 แถว (ใกล้การใช้งานจริง) · ผู้จัดทำ + "ส่งในระบบ …" |
| cancelled | footer "· ยกเลิก" |
| long-20rows | 20 แถวเต็มกระดาษ · ปลายทางยาว 2 บรรทัดทุก 4 แถว · `layout.dense` · ยัง 1 หน้า |
| blank | แบบฟอร์มเปล่า (ไม่มีเลขที่) สำหรับพิมพ์กรอกมือ |
- สถานะ DOA หลายขั้น: **ไม่ใช้** — ไม่มีการอนุมัติ (DEC-03) · กลไก sign_rows รองรับถ้าเปิด DOA ภายหลัง
- ตรวจเสริม (คอนเทนเนอร์ Claude · Playwright): ทุกสถานะ 1 หน้า · ถ้าทั้ง 20 แถวยาว 2 บรรทัด บล็อกผู้จัดทำขึ้นหน้า 2 ทั้งก้อน (ใบต่อ)

## 7. ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ `16. FM-SAL-16 ฟอร์มแจ้งงานขนส่งนอก.xlsx` (Rev.00 : 01/07/2569) · ภาพต้นฉบับจาก LibreOffice ไม่มีฟอนต์ไทย (กล่อง) + คอลัมน์ E หลุดหน้า
- compare (render ในคอนเทนเนอร์ ไม่ได้แพ็ก PDF) = **0.161 WARN** (บรรทัดตรง 1/7 · cols 0.20 · ssim 0.55) — เหตุผล: ต้นฉบับไม่มีอักษรไทย (เส้นข้อความไม่ถูกนับ) · ต้นฉบับเป็น 4 คอลัมน์ในหน้า 1 (E หลุด) ของเราครบ 5 · ระยะขอบ/สเกล LibreOffice ต่างจาก A4 ของระบบ · บล็อกผู้จัดทำย้ายเป็นแถวล่างตามหลัก B6 · คนดูภาพวางคู่ (`compare_preview/compare_side.png`) แล้ว โครงตรง: โลโก้ → หัว + เส้นประ → รอบวันที → ตาราง 5 คอลัมน์ 20 บรรทัด หัวพื้นเทา → ผู้จัดทำ
- ตั้งใจต่าง: (1) โลโก้อยู่บรรทัดบน หัวเรื่องกึ่งกลาง (ต้นฉบับโลโก้ซ้ายคู่หัวเรื่อง — replica.css ไม่มี layout โลโก้ข้างหัว · ห้ามแก้ CSS รายลูกค้า) (2) คอลัมน์ วันที่นัดส่ง อยู่หน้าเดียว (DEC-15) (3) "ผู้จัดทำ……" → บล็อกลงชื่อแถวล่าง (DEC-07) (4) footer ระบบซ้าย · Doc. No. ขวา (5) ถ้อยคำ "รอบวันที" คงตามกระดาษ (DEC-11)
- ความกว้างคอลัมน์ตาม xlsx (A 17.4 · B 25.4 · C 17.4 · D 11.7 · E 15.6) → 20/32/18/12/18 % (ปลายทางกว้างขึ้นเล็กน้อยให้ชื่อลูกค้า 1 บรรทัด)
- profile: form_fs 9.5pt (≥ 8pt) · lh 1.4 · title 15pt · logo 12mm ชิดซ้าย · grid row 6.8mm (dense 5.6mm) · head bg #D9D9D9

## 8. print_config → F-DOCCFG
`print_config.json` (doc_type OTN · form_code FM-SAL-16 · min_rows 20 · sign_boxes requester "ผู้จัดทำ" + doa_step:* (ปัจจุบัน 0 ขั้น))

## 9. ภาพประกอบ (NO-BROWSER)
- `out/_states_sheet_preview.png` + `compare_preview/` = render ในคอนเทนเนอร์ Claude จาก HTML ต่อสถานะใน `out/` — ใช้ดูหน้าตาเท่านั้น · PDF ทางการต้อง render ซ้ำบนเครื่องที่มี browser
