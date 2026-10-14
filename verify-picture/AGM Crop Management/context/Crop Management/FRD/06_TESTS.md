# 06_TESTS — F-AGM-004 Crop Management

> Audience: QA + ai-testcase-md-generator · microcopy-aware · legacy TC map

## §6.1 Acceptance Criteria

### สร้าง + double-binding (US-01/02)
- **AC-01** ค้นหา quota (exact, verified) → farmer owner snapshot แสดง
- **AC-02** เลือก plot (ของเจ้าของ quota + verified) → plot snapshot (ที่อยู่+ขนาด) · fields ปลดล็อก
- **AC-02b** quota ไม่พบ/ไม่ verified → "ไม่พบ Quota หรือสถานะไม่เป็น verified" block
- **AC-02c** plot owner mismatch/ไม่ verified → block
- **AC-03** กรอกปี(พ.ศ.)+เดือน+ตัน + รูป → ยืนยันสร้าง → toast "สร้างรอบปลูกสำเร็จ — [เลขรอบปลูก]" + status waiting_for_verify + audit
- **AC-04** year นอก 2500-2600 → "ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600"
- **AC-05** month ไม่เลือก → "กรุณาเลือกเดือนที่ปลูก"
- **AC-06** total_tons < 0 → "ปริมาณรวมต้องเป็นตัวเลขที่มากกว่าหรือเท่ากับ 0"
- **AC-07** submit ก่อนครบ quota+plot → block ("กรุณาเลือกโควตาและแปลงก่อน")
- **AC-08** upload photos หลายไฟล์ → preview ชื่อไฟล์
- **AC-08b** สายพันธุ์ select (ขอนแก่น 3/LK 92-11/UT 8) + ประเภทอ้อย select (อ้อยใหม่/อ้อยตอ) → บันทึกเป็น cane_variety/cane_type · optional (เว้นได้)
- **AC-08c** อายุอ้อย (เดือน) = derived read-only · auto-คำนวณจาก เดือนที่ปลูก + ปีผลิต (FN-AT-CROP-192) · แก้เองไม่ได้
- **AC-08d** พบโรค/ศัตรูพืช select (ไม่พบ/พบ) + รายละเอียด textarea → disease_pest_found/disease_pest_detail · optional
- **AC-08e** รหัสแปลง (plot_code) text optional
- **AC-08f** fields agronomic ทั้งหมดแสดง read-only บน Landing ภาพรวม + แก้ได้บน Edit drawer

### ค้นหา/กรอง/ส่งออก + remaining (US-10)
- **AC-09** search (crop_id/quota/plot/farmer) + filter status(5)+ปี · ไม่พบ → "ไม่พบรายการที่ค้นหา"
- **AC-10** sort crop_id/year/total_tons · export CSV เคารพ filter · pagination
- **AC-10b** ปุ่ม Export CSV (`btn-export`) → export ฝั่ง client เคารพ filter · ⚠️ backend export endpoint = **Pending Spec** (TC-581)
- **AC-29** remaining ติดลบ → badge แดง (list + landing)

### แก้ไข (US-08)
- **AC-11** แก้ crop waiting + save → version++ + audit
- **AC-11b** แก้ crop **verified** + save → **กลับ waiting_for_verify** (LOCK-05) + toast "บันทึกแล้ว — กลับสู่สถานะรอตรวจสอบ"
- **AC-12** stale (version เก่า) → 409 "ข้อมูลล้าสมัย กรุณารีเฟรช"
- **AC-13** quota/plot บนหน้า edit = read-only (แก้ไม่ได้)

### CSV (US-03)
- **AC-14** ไฟล์ดี N แถว → summary total/created/failed + ทุกแถว waiting_for_verify
- **AC-14b** CSV schema = **8 คอลัมน์ (ลำดับเป๊ะ):** quota_id, plot_id, production_year_be, plot_code, variety, cane_type, planted_month, total_tons (เดิม 5 · `year_be`→`production_year_be`)
- **AC-15** header ไม่ตรง → reject ทั้งไฟล์ + "คอลัมน์ไฟล์ไม่ตรงแม่แบบ: [x]"
- **AC-16** แถว quota/plot invalid → error รายแถว + report
- **AC-17** ไม่ใช่ .csv → "ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV"

### Verify/Reject (US-05/06/07)
- **AC-18** waiting + ยืนยัน+Confirm → toast "ยืนยันเรียบร้อย" + pill เขียว(verified) + verified_by/at + audit
- **AC-19** ปฏิเสธ ไม่กรอกเหตุผล → "กรุณากรอกเหตุผลในการปฏิเสธ" block
- **AC-20** ปฏิเสธ + reason → pill แดง(rejected) + reject_reason แสดง landing + audit
- **AC-21** Bulk: เลือกทั้งหมด = เฉพาะ waiting · ยืนยันกลุ่ม → summary
- **AC-22** Bulk reject = เหตุผลบังคับ (ใช้ร่วม) · skip non-waiting
- **AC-23b** verified/rejected → verify ซ้ำ → 409 "สถานะเปลี่ยนแปลงแล้ว" (UI ซ่อนปุ่ม)

### Landing (US-04)
- **AC-24** Landing tabs: ภาพรวม/รูปภาพ/ETCD/Survey/ประวัติ + snapshot card (ดูโควตา/ดูแปลง)
- **AC-25** ETCD tab: bookings + total_booked + remaining (read-only) · Survey tab read-only
- **AC-25b** ETCD/Survey external down → fail-soft "ดึงข้อมูล...ไม่สำเร็จ" (landing ยังเปิดได้)
- **AC-26** ประวัติ = audit timeline
- **AC-26b** deep-link crop ไม่มี/deleted → "ไม่พบข้อมูลรอบปลูกที่เลือก" + กลับ list

### Cancel/Delete (US-09)
- **AC-27** ยกเลิก(cancelled) + เหตุผล → toast "ยกเลิกรอบปลูกแล้ว" + audit · ไม่ใส่เหตุผล → block
- **AC-28** ลบ(deleted) + เหตุผล → soft delete + ซ่อนจาก list + audit

## §6.9 Cross-Module Test Cases ⭐ (double read-only)
| XT | Scenario | Source | Expected |
|---|---|---|---|
| XT-01 | สร้าง crop | Quota+Plot (read) | crop.quota_id/plot_id set + snapshot ตรง · **quota/plot ไม่ถูกแก้** |
| XT-02 | quota search exact verified | Quota | คืน verified quota + farmer owner; ไม่ verified → block |
| XT-03 | plot load ของเจ้าของ quota | Plot | คืนเฉพาะ plot verified ของเจ้าของ; owner อื่น → excluded |
| XT-04 | ETCD compute remaining | ETCD external | remaining = total − ΣETCD · ติดลบ → badge |
| XT-05 | ETCD/Survey down | external | fail-soft (crop mutation/landing ยังทำงาน) |

## §6.10 Microcopy-Aware Expected (verbatim)
| จุด | ข้อความ |
|---|---|
| ปุ่มสร้าง | `สร้างรอบปลูก` |
| footer drawer | `ยกเลิก` · `ยืนยันสร้าง` / `บันทึกการแก้ไข` — `กำลังบันทึก…` |
| toast | `สร้างรอบปลูกสำเร็จ` · `บันทึกการแก้ไขแล้ว` · `บันทึกแล้ว — กลับสู่สถานะรอตรวจสอบ` · `ยืนยันเรียบร้อย` / `ปฏิเสธเรียบร้อย` · `ยกเลิกรอบปลูกแล้ว` / `ลบรอบปลูกแล้ว` |
| pills | `รอตรวจสอบ`(เหลือง) · `ตรวจแล้ว`(เขียว) · `ปฏิเสธ`(แดง) · `ยกเลิก`(เทา) · `ลบ`(เทา) |
| verify modal | `ตรวจสอบรอบปลูก` · radio `ยืนยัน` / `ปฏิเสธ` · reject `กรุณาระบุเหตุผลในการปฏิเสธ...` · verify note `หมายเหตุเพิ่มเติม (ไม่บังคับ)` |
| cancel/delete | `ยกเลิก/ลบรอบปลูก?` · radio `ยกเลิก` / `ลบ` · `เหตุผล` (บังคับ) |
| remaining badge | `คงเหลือ (ยังไม่จอง)` · ติดลบ = แดง |
| errors | ตาม §5.6 ตรงตัว |

## §6.8 Trace: AC → Logic
| AC | API | FN |
|---|---|---|
| AC-01/02 | API-13/14 | FN-11,12 |
| AC-03..08 | API-02/03/18 | FN-01,04 |
| AC-09/10/29 | API-01/17 | FN-05,13 |
| AC-11..13 | API-05 | FN-03,04,10 |
| AC-14..17 | API-09 | FN-09 |
| AC-18..23 | API-07/08 | FN-06,07,10 |
| AC-24..26 | API-04/15/16/12 | FN-13 |
| AC-27/28 | API-11 | FN-08,10 |
> Coverage FN-01..13 ✅ · XT-01..05 (double read-only + fail-soft) ✅

## §6.6 Performance
list p95<3s · create/update<1s · CSV 1,000<60s · ETCD/Survey fail-soft ≤1.5s · bulk chunk 200
