# 06_TESTS — F-TMP-002

## §6.1 Acceptance Criteria
| AC | Given / When / Then | อ้าง |
|---|---|---|
| AC-01 | owner สร้าง เลือกประเภทรถ + เดือนนี้ → วันนี้ "ปกติทั้งหมด" → บันทึกร่าง ได้เลข FLI-YYYY-NNNN | S-01 FN-03 |
| AC-02 | กดถัดไปโดยไม่เลือกประเภทรถ → บล็อก + ข้อความ "เลือกประเภทรถ" + toast | VR-01 |
| AC-03 | เดือนปัจจุบัน → ปุ่มวันหลังวันนี้ disabled · API ส่งวันอนาคต → 422 DAY_OUT_OF_RANGE | VR-02 VR-03 DEC-15 |
| AC-04 | กรอกบางรายการของวัน → บล็อกบันทึก ชี้วันที่ไม่ครบ · แถวที่ว่างแดง | VR-03 |
| AC-05 | ติ๊ก ✗ → แถบเตือนบนจอ · บันทึก → fli_defect_found ถึงหัวหน้างาน + audit "แจ้งพบรายการผิดปกติ" | BR-06 DEC-16 |
| AC-06 | เปลี่ยนประเภทรถหลังกรอก → ผลส่วนเฉพาะเดิมถูกล้าง + toast · PDF ตารางอีกประเภทว่าง | BR-03 DEC-14 |
| AC-07 | ส่ง → modal slot = จำนวนขั้น DOA · ค่าเริ่ม = หัวหน้างานตามผัง · ผู้ตรวจสอบไม่อยู่ในรายชื่อ | S-05 VR-05 |
| AC-08 | หัวหน้างาน "ตรวจสอบแล้ว" ขั้นสุดท้าย → approved · ล็อกแก้ไข · PDF เก็บ approved_final | S-06 |
| AC-09 | หัวหน้างาน "ส่งกลับแก้ไข" (เหตุผลบังคับ) → returned เลขเดิม · owner เห็นเหตุผล · แก้แล้วส่งใหม่ resolve สายใหม่ | S-07 BR-DOA-03 |
| AC-10 | PDF ทุกสถานะ 2 หน้าเท่ากัน · ไม่มี {{}} · ☑ ประเภทรถถูก · ตาราง 15/8/6 แถว × หัววัน 1–31 · ลายเซ็น = ผู้ตรวจสอบ + 1/ขั้น · HTML render = server render (parity) | S-08 BR-12 |
| AC-11 | ตั้ง DOA 1 / 2 / 6 ขั้น → slot 1 / 2 / 6 · PDF ช่องลงชื่อ 2 / 3 / 7 (6 ขั้น = 2 แถว 4+3) · อนุมัติเรียงขั้น | BR-12 DEC-03 |
| AC-12 | ยกเลิก: owner/ผู้จัดการคลัง · ร่าง/รอ/ส่งกลับ · เหตุผลบังคับ · approved ยกเลิกไม่ได้ | S-09 BR-10 |
| AC-13 | ผู้จัดการคลังเห็นทุกใบ · segmented "รอฉันตรวจสอบ" · CSV ตามตัวกรอง | S-10 |
| AC-14 | doc_type ปิดใช้ → ปุ่มสร้าง disabled + แถบแดง | EC-08 |

## §6.2 Permission / Deny cases (G8)
| TC | กรณี | คาด |
|---|---|---|
| TC-D01 | หัวหน้างานเปิด route ร่างของลูกทีม | ไม่เห็นร่าง · ไม่เปิด drawer (404 NOT_FOUND) |
| TC-D02 | owner ค้นหาใบของผู้ตรวจสอบคนอื่น | ไม่พบใบ ในรายการ |
| TC-D03 | ผู้อยู่ในสายแต่ไม่ใช่ขั้นปัจจุบันกดตัดสิน | 403 NOT_CURRENT_APPROVER · ไม่มีปุ่ม |
| TC-D04 | คนนอกสายยกเลิก | 403 NOT_OWNER |
| TC-D05 | บันทึกผลใบที่ pending/approved หรือไม่ใช่ของตน | ไม่มีปุ่มแก้ไข · 409 NOT_EDITABLE / 403 NOT_OWNER |
| TC-D06 | ผู้ตรวจสอบเลือกตัวเองเป็นผู้พิจารณา | ไม่มีในรายชื่อ · 422 SELF_APPROVAL |
| TC-D07 | ส่งผล section ของอีกประเภทรถผ่าน API | 422 SECTION_NOT_ALLOWED |

## §6.3 Test Data
personas (ชื่อสมมติ): owner = อนุชา (E01 · พนักงานขับรถ) · หัวหน้างาน = วิทยา (E02 · role-supervisor) · ผู้จัดการคลัง = ศิริพร (E08 · role-mgr-wh · admin view) · seed 10 ใบครบทุกสถานะ (ร่าง/รอตรวจสอบ/ส่งกลับ/ตรวจสอบแล้ว/ยกเลิก) · มีใบของคนอื่นที่ owner ไม่เห็น · print/*.data.json 5 สถานะ

## §6.4 DoD
API ครบ §2.1 · logic ตาม 03 · RLS · audit · PDF parity IDENTICAL · e2e_standard ผ่าน (ต้องรันบนเครื่องที่มี browser — รอบนี้ [NO-BROWSER]) · AC-01..14 + TC-D01..07 ผ่าน · declaration wired

## §6.8 AC → Logic
AC-01 FN-01/02/03 · AC-02..04 FN-01 · AC-05 FN-04/10 · AC-06 FN-04/09 · AC-07 FN-05 · AC-08 FN-06/09 · AC-09 FN-07 · AC-10/11 FN-09 · AC-12 FN-08 · AC-13 FN-11 · AC-14 FN-03

## §6.9 Cross-Module
XT-01 ENG-NOTIFY รับ fli_defect_found/fli_cancelled ถูกผู้รับ · XT-02 ENG-DOC-STORE เก็บ PDF ตอน approved · XT-03 ไม่ยิง fli.defect_recorded ไป Asset/Maintenance (DEC-02)
