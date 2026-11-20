# PRINT SPEC — แบบฟอร์มบันทึกภาพรวมและเริ่มต้นโครงการ (PJI) · Replica FM-BDM-01
> โหมด Replica · R9 ตารางกรอบ (.form-grid) · **2 หน้าตาม R10** · template `form.tpl.html` (logic-less) · profile `profile.json` · print_config `print_config.json`
> ⚠️ [NO-BROWSER] รอบนี้ไม่ได้ render PDF/ภาพ (render_pdf.py ไม่มี browser) — มี HTML ทุกสถานะใน `out/*.html` · ต้องรัน `render_states.py --max-pages 2` + `compare_original.py` บนเครื่องที่มี browser ก่อนส่งมอบเต็ม

## 1. โครงหน้า (R10)
- ต้นฉบับ xlsx พิมพ์ 1 หน้าที่ scale 46% (ตัวอักษรจริงบนกระดาษ ≈ 5pt) → ถ้าพิมพ์ที่ ≥ 8pt ไม่พอ 1 หน้า (≈300mm เทียบพื้นที่ 277mm) → ออกแบบ 2 หน้าตั้งใจ
- หน้า 1: หัวกระดาษ (โลโก้ · ชื่อเอกสาร · ฝ่าย · บรรทัดบริษัท) + ข้อมูลกระบวนการ 5 แถว + ข้อมูลทั่วไปของโครงการ + วัตถุประสงค์และขอบเขต · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
- `.page-break` ก่อน "แผนงานเบื้องต้น" · หน้า 2: หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) + แผนงานเบื้องต้น (thead ซ้ำ) + การตรวจทาน/อนุมัติ (`.signs-block` ทั้งก้อน) + ประวัติการแก้ไข · footer "หน้า 2/2"
- ฟอนต์ 9pt (profile) ไม่ต่ำกว่า 8pt · ทุกสถานะ = 2 หน้า

## 2. Field map → data contract
| ช่องบนกระดาษ | key | source | format |
|---|---|---|---|
| โลโก้ / บรรทัดบริษัท | company.logo · company.group_line | Organization snapshot ตอนออกเลข | data URI · text |
| ชื่อเอกสาร · ฝ่าย | doc.title · doc.department | print_config / doc_type | text |
| เลขที่ (ระบบเพิ่มในตารางข้อมูลกระบวนการ) | doc.no | ENG-DOC-NUM (PJI) | PJI-2569-0001 |
| ใช้ในขั้นตอน / วัตถุประสงค์ / ผู้จัดทำ / ผู้ตรวจสอบ / ผู้อนุมัติ/รับทราบ | — | ข้อความคงที่บนกระดาษ | — |
| ชื่อโครงการ … ผู้สนับสนุน | project.name/origin/type_opportunity/owner/supporters | ผู้ใช้กรอก (owner = Employee.full_name) | text |
| วันที่เริ่มต้น / วันที่เป้าหมาย | project.date_range | `start_date` + " / " + `target_date` (DEC-07 เก็บแยก) | วัน เดือนเต็ม พ.ศ. |
| ระดับความสำคัญ / สถานะ | project.priority_status | `priority` + " / " + `status` | text |
| วัตถุประสงค์และขอบเขต 6 แถว | scope.* | ผู้ใช้กรอก | text |
| แผนงานเบื้องต้น | plan[].seq/activity/owner/supporter/start_date/due_date/status/remark | ผู้ใช้กรอก · เติมแถวว่างถึง 6 (DEC-05) · สถานะ 5 ค่า | วันที่ย่อ พ.ศ. |
| การตรวจทาน / อนุมัติ | sign_rows[].signs[] (role/name/position/decision/date) | ผู้จัดทำ + 1 แถวต่อขั้น DOA (ไม่ fix) · คำตัดสินตาม role | "ส่ง/พิจารณาในระบบ วันที่ เวลา" |
| ประวัติการแก้ไข | revisions[].version/date/detail/prepared_by/approved_by | ประวัติเวอร์ชันเอกสาร · เติมถึง 1 แถว (DEC-06) | text |

## 5. สถานะที่ render
draft · approved · rejected (ขั้น 1 ส่งกลับแก้ไข) · long-14rows (14 แถว + ประวัติ 2 ฉบับ) · approved-doa6steps (DOA 6 ขั้น → 7 แถวลงชื่อ · dense)
- parity_check: IDENTICAL 5/5 · ไม่มี `{{}}` หลง · missing key 0
- จำนวนหน้า: [NO-BROWSER] ยังไม่ได้วัด — ออกแบบให้ = 2 ทุกสถานะ (ประมาณการ: หน้า 2 สุดขั้ว ≈ 180–200mm)

## 7. ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ `1. FM-BDM-01 แบบฟอร์มบันทึกภาพรวมและเริ่มต้นโครงการ.xlsx` (Rev.00 : 01/07/2569) · compare_original: [NO-BROWSER] ข้าม (ต้องใช้ approved.pdf)
- ตั้งใจต่าง: (1) แยก 2 หน้า (R10) (2) เพิ่มแถว "เลขที่" ในตารางข้อมูลกระบวนการ + footer ระบบซ้าย (3) ตารางการตรวจทาน/อนุมัติ = แถวต่อขั้น DOA (DEC-08) · คอลัมน์ "ลายเซ็น" แสดงคำตัดสิน (ไม่ใช้ภาพ) (4) หัวส่วนพื้นเทาแทนน้ำเงินเข้ม (Replica หมึกเดียว) (5) ความกว้างคอลัมน์แผนงานเท่ากัน (ห้าม style ใน body)
- profile: form_fs 9pt · title 15pt · logo 12mm · title_gap 2px · grid_gap 6px
