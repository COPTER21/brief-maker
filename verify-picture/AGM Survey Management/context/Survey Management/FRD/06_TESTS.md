# 06_TESTS — F-AGM-006 Survey Management

> Audience: QA + ai-testcase-md-generator · microcopy-aware

## §6.1 Acceptance Criteria

### สร้าง + cascade (US-01/02)
- **AC-01** เลือก quota → farmer snapshot · เลือก plot → เลือก crop (cascade) · fields ปลดล็อก
- **AC-02** กรอกพื้นฐาน (วันที่/ผู้สำรวจ/ปี) + พืชผล (พันธุ์/ผลผลิต/ขนาด/สีดิน/สีใบ/โรค) + รูป 4 หมวด → ยืนยันสร้าง → toast "สร้างแบบสำรวจสำเร็จ — [เลขสำรวจ]" + status รอตรวจสอบ + audit
- **AC-02b** cascade ไม่ครบ → "กรุณากรอกข้อมูลให้ครบถ้วน" block
- **AC-03** ผลผลิต < 0 / ขนาดแปลง ≤ 0 → "กรุณาใส่ค่าที่ถูกต้อง"
- **AC-04** เลือกสีดิน/การตรวจสีใบ/โรค-ศัตรูพืช จาก dropdown
- **AC-05** แนบรูปแต่ละหมวด (รูปกับแปลง/รูปพืชผล/รูปลำต้นในกอ/รูปสีดิน) → preview
- **AC-06** submit ก่อนครบ cascade → block ("กรุณาเลือกโควตา แปลง และรอบปลูกก่อน")
- **AC-07** agronomic panel (optional): เลือกเดือนที่ปลูก(1–12) · ประเภทอ้อย(อ้อยใหม่/อ้อยตอ) · กรอกการวัดขนาดอ้อย (ระยะร่อง/ความสูงหัว-กลาง-ท้าย/ความยาวปล้อง/เส้นผ่านศูนย์กลาง/ลำต่อกอ/กอใน 10 ม.) · ชนิดดิน/ความหนาแน่นวัชพืช · พบโรค/ศัตรูพืช+รายละเอียด · รหัสไปรษณีย์ → บันทึกครบทุกฟิลด์
- **AC-07b** อายุอ้อย(เดือน) = **derived read-only** — คำนวณจากเดือนปลูก+ปี(พ.ศ.) อัตโนมัติ (FN-AT-CROP-192) · แก้ไขเองไม่ได้ · ไม่ส่งใน body
- **AC-07c** ค่าวัดขนาดติดลบ / เดือนปลูกนอกช่วง 1–12 / รหัสไปรษณีย์ ≠ 5 หลัก → validation block · ฟิลด์ agronomic ทั้งหมด optional (เว้นว่างได้)
- **AC-07d** ปริมาณรวม(ตัน) ↔ total_tons (required ≥0) · ผู้สำรวจ ↔ recorder (required)

### ค้นหา/กรอง/ส่งออก (US-10)
- **AC-10** search (survey_id/quota/plot/crop/ผู้สำรวจ) + filter status(5)+ปี · ไม่พบ → "ไม่พบรายการที่ค้นหา"
- **AC-28** sort + export CSV + pagination
- **AC-28b** ปุ่ม Export CSV (btn-export) → ดาวน์โหลด CSV ของผลกรองปัจจุบัน (client-side ใน prototype) · backend export endpoint = **Pending Spec** (TC-606)

### แก้ไข (US-08)
- **AC-11** แก้ survey waiting + save → version++ + audit
- **AC-11b** แก้ survey **verified** + save → **กลับ waiting** (LOCK-07) + toast "บันทึกแล้ว — กลับสู่สถานะรอตรวจสอบ"
- **AC-12** stale → 409 "ข้อมูลล้าสมัย กรุณารีเฟรช"
- **AC-13** quota/plot/crop บนหน้า edit = read-only

### CSV (US-03)
- **AC-14** ไฟล์ดี N แถว → summary + ทุกแถว waiting
- **AC-15** header ไม่ตรง → reject ทั้งไฟล์
- **AC-16** cascade/field invalid รายแถว → error report
- **AC-17** ไม่ใช่ .csv → "ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV"

### Verify/Reject (US-05/06/07)
- **AC-18** waiting + ยืนยัน+Confirm → toast "ยืนยันเรียบร้อย" + pill เขียว(ยืนยันแล้ว) + audit
- **AC-19** ปฏิเสธ ไม่กรอกเหตุผล → "กรุณากรอกเหตุผลในการปฏิเสธ" block
- **AC-20** ปฏิเสธ + reason → pill แดง(ปฏิเสธ) + reject_reason แสดง + audit
- **AC-21** Bulk: เลือกทั้งหมด = เฉพาะ waiting · ยืนยันกลุ่ม → summary
- **AC-22** Bulk reject = เหตุผลบังคับ · skip non-waiting
- **AC-23b** verified/rejected → verify ซ้ำ → 409 "สถานะเปลี่ยนแปลงแล้ว"

### Detail (US-04)
- **AC-24** detail tabs: ข้อมูลสำรวจ/รูปภาพ/ประวัติ + snapshot card (ดูรอบปลูก)
- **AC-25** tab รูปภาพ = 4 หมวด · tab ประวัติ = audit
- **AC-25b** deep-link survey ไม่มี/deleted → "ไม่พบข้อมูลแบบสำรวจที่เลือก" + กลับ list

### Cancel/Delete (US-09)
- **AC-26** ยกเลิก + เหตุผล → toast "ยกเลิกแบบสำรวจแล้ว" + audit · ไม่ใส่เหตุผล → block
- **AC-27** ลบ + เหตุผล → soft delete + ซ่อน + audit

## §6.9 Cross-Module Test Cases ⭐
| XT | Scenario | Module | Expected |
|---|---|---|---|
| XT-01 | สร้าง survey | Quota/Plot/Crop (read) | survey.quota_id/plot_id/crop_id set + snapshot ตรง · source ไม่ถูกแก้ |
| XT-02 | cascade | Quota→Plot→Crop | เลือก quota → plots ของโควตา · เลือก plot → crops ของแปลง |
| XT-03 | survey verified feeds Crop | Crop (F-AGM-004) | survey verified แสดงในแท็บสำรวจของรอบปลูก |
| XT-04 | 1 crop หลาย survey | — | สำรวจรอบปลูกเดิมได้หลายครั้ง |

## §6.10 Microcopy-Aware Expected (verbatim)
| จุด | ข้อความ |
|---|---|
| ปุ่มสร้าง | `สร้างแบบสำรวจ` |
| footer drawer | `ยกเลิก` · `ยืนยันสร้าง` / `บันทึกการแก้ไข` — `กำลังบันทึก…` |
| toast | `สร้างแบบสำรวจสำเร็จ` · `บันทึกการแก้ไขแล้ว` · `บันทึกแล้ว — กลับสู่สถานะรอตรวจสอบ` · `ยืนยันเรียบร้อย` / `ปฏิเสธเรียบร้อย` · `ยกเลิกแบบสำรวจแล้ว` / `ลบแบบสำรวจแล้ว` |
| pills | `รอตรวจสอบ`(เหลือง) · `ยืนยันแล้ว`(เขียว) · `ปฏิเสธ`(แดง) · `ยกเลิก`(เทา) |
| verify modal | `ตรวจสอบแบบสำรวจ` · radio `ยืนยัน` / `ปฏิเสธ` · reject `กรุณาระบุเหตุผลในการปฏิเสธ...` |
| photo หมวด | `รูปกับแปลง` · `รูปพืชผล` · `รูปลำต้นในกอ` · `รูปสีดิน` |
| errors | ตาม §5.6 ตรงตัว |

## §6.8 Trace: AC → Logic
| AC | API | FN |
|---|---|---|
| AC-01/02 | API-13/14/02 | FN-11,01,04 |
| AC-03..06 | API-02 | FN-04 |
| AC-10/28 | API-01/15 | FN-05 |
| AC-11..13 | API-05 | FN-03 |
| AC-14..17 | API-09 | FN-09 |
| AC-18..23 | API-07/08 | FN-06,07 |
| AC-24/25 | API-04/12 | — |
| AC-26/27 | API-11 | FN-08 |
> Coverage FN-01..11 ✅ · XT-01..04 (cascade read + feeds Crop) ✅

## §6.6 Performance
list p95<3s · create<1s · CSV 1,000<60s · bulk chunk 200
