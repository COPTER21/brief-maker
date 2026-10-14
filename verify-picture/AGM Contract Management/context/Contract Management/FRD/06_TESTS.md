# 06_TESTS — F-AGM-005 Contract Management

> Audience: QA + ai-testcase-md-generator · microcopy-aware · legacy API map

## §6.1 Acceptance Criteria

### สร้าง + build-path (US-01/02)
- **AC-01** เลือก quota → farmer snapshot แสดง
- **AC-02** เลือกแปลง(≥1) + รอบปลูก verified(≥1) → แสดงผลรวมตันของ crop เป็น helper · fields ปลดล็อก
- **AC-02b** quota/plots/crops ไม่ครบ → "กรุณาตรวจสอบข้อมูลให้ครบถ้วน" block
- **AC-02c** total_tons "จำนวนตันที่ทำสัญญา" = manual input บังคับ > 0 (ทุก 5 ประเภท) · ปุ่ม "ใช้ค่านี้" เติมค่าผลรวม crop · ว่าง/≤0 → block
- **AC-03** เลือกประเภทสัญญา 1 ใน 5 → type-specific field ปรากฏตามประเภท
- **AC-04** type=support → support_items[] repeater บังคับ ≥1 · แต่ละรายการ = ประเภทส่งเสริม (dropdown 5 masters: ปุ๋ย/ยาปราบ · เครื่องจักร · พันธุ์อ้อย · ยาปราบ · เงินส่งเสริม) + ราคา(≥0) + วันที่รับส่งเสริม + แนบต่อรายการ · รายการไม่ครบ → block
- **AC-05** type=promotion-7 → เลือกช่วงโปรโมชั่น (บังคับ) · dropdown 4 ค่า: โปรโมชัน 7 วันหลังเปิดหีบ / ก่อนปิดปีใหม่ / หลังเปิดปีใหม่ / ก่อนปิดหีบ
- **AC-06** type=promotion-crane → เลือกเครน (บังคับ) · dropdown 4 ค่า: กุดโดน / ชื่นชม2 / หนองกุงสวรรค์ / โนนสำราญ
- **AC-06b** type=early-purchase (ตกเขียว) → ต้องการเฉพาะ total_tons · **ไม่มี block เอกสารแนบ** (ซ่อน) · อีก 4 ประเภทมี attachments
- **AC-07** crop license=contracted → กันเลือกซ้ำ "รอบปลูกนี้ทำสัญญาแล้ว"
- **AC-08** ยืนยันสร้าง → toast "สร้างสัญญาสำเร็จ — [เลขสัญญา]" + status รอการตรวจสอบ + **crop license → contracted** + audit
- **AC-09** upload attachments → preview (ยกเว้น early-purchase)

### ค้นหา/กรอง/ส่งออก (US-09)
- **AC-10** search (contract_id/quota/farmer) + filter status(3)+type(5) · ไม่พบ → "ไม่พบรายการที่ค้นหา"
- **AC-23** sort + export CSV + pagination
- **AC-23b** ปุ่ม "ส่งออก CSV" (`btn-export`) → ดาวน์โหลด client-side CSV (UTF-8 BOM) คอลัมน์ contract_id/quota_id/farmer_name/contract_type/total_tons/plots_count/crops_count/status/created_by/created_at · **backend API = Pending Spec (TC-522)**

### แก้ไข (US-07)
- **AC-11** แก้ type-specific/attachments + save → version++ + audit
- **AC-12** quota/plots/crops บนหน้า edit = read-only

### อนุมัติ/ปฏิเสธ (US-04/05/06)
- **AC-13** waiting + อนุมัติ (ไม่ต้องมีเหตุผล) + Confirm → toast "อนุมัติเรียบร้อย" + pill เขียว(อนุมัติแล้ว) + approved_by/at + audit
- **AC-14** อนุมัติ → crop license คง contracted (ไม่เปลี่ยน)
- **AC-15** ปฏิเสธ ไม่กรอกเหตุผล → "กรุณากรอกเหตุผลในการปฏิเสธ" block
- **AC-16** ปฏิเสธ + reason → pill แดง(ปฏิเสธ) + reject_reason แสดง + **crop license → none (revert)** + audit
- **AC-17** Bulk: เลือกทั้งหมด = เฉพาะ waiting · อนุมัติกลุ่ม → summary
- **AC-18** Bulk reject = เหตุผลบังคับ (ใช้ร่วม) · skip non-waiting
- **AC-18b** verified/reject → approve ซ้ำ → 409 "สถานะเปลี่ยนแปลงแล้ว" (UI ซ่อนปุ่ม)

### Detail (US-03)
- **AC-19** detail tabs: ข้อมูลทั่วไป/แปลง/รอบปลูก/เอกสาร/ประวัติ + snapshot card
- **AC-20** tab รอบปลูก = crop list + tons · tab ประวัติ = audit + license write events
- **AC-20b** deep-link contract ไม่มี/deleted → "ไม่พบข้อมูลสัญญาที่เลือก" + กลับ list

### ลบ (US-08)
- **AC-21** ลบ + confirm → toast "ลบสัญญาแล้ว" + ลบ attachments + audit
- **AC-22** ลบสัญญา → crop license revert none (EC-12)

## §6.9 Cross-Module Test Cases ⭐ (read + WRITE-BACK)
| XT | Scenario | Module | Expected |
|---|---|---|---|
| XT-01 | สร้างสัญญา | Crop (write) | **crop.license_status → contracted** ทุก crop ที่ผูก + Crop detail แสดง "ทำสัญญาแล้ว" |
| XT-02 | ปฏิเสธสัญญา | Crop (write) | **crop.license_status → none** (revert) ทุก crop ที่ผูก |
| XT-03 | ลบสัญญา | Crop (write) | crop.license_status → none (เหมือน XT-02) |
| XT-04 | available-items | Plot+Crop (read) | คืนเฉพาะ plot/crop verified ของโควตา + crop license≠contracted |
| XT-05 | crop ผูกสัญญาแล้ว | Crop | กันเลือกซ้ำ (1 crop : 1 active contract) |

## §6.10 Microcopy-Aware Expected (verbatim)
| จุด | ข้อความ |
|---|---|
| ปุ่มสร้าง | `สร้างสัญญา` |
| footer drawer | `ยกเลิก` · `ยืนยันสร้าง` / `บันทึกการแก้ไข` — `กำลังบันทึก…` |
| toast | `สร้างสัญญาสำเร็จ` · `บันทึกการแก้ไขแล้ว` · `ลบสัญญาแล้ว` · `อนุมัติเรียบร้อย` / `ปฏิเสธเรียบร้อย — คืนสถานะสิทธิ์รอบปลูกแล้ว` |
| pills | `รอการตรวจสอบ`(เหลือง) · `อนุมัติแล้ว`(เขียว) · `ปฏิเสธ`(แดง) |
| approve/reject modal | `ตรวจสอบสัญญา` · radio `อนุมัติ` / `ปฏิเสธ` · reject `กรุณาระบุเหตุผลในการปฏิเสธ...` |
| ประเภทสัญญา | `สัญญาตันสูญเปล่า` · `สัญญาส่งเสริม` · `สัญญาโปรโมชั่น โปร 7 วัน` · `สัญญาโปรโมชั่นเครน` · `สัญญาตกเขียว` |
| delete | `ยืนยันการลบสัญญา` · warn ข้อมูล+ไฟล์แนบจะถูกลบ |
| errors | ตาม §5.6 ตรงตัว |

## §6.8 Trace: AC → Logic
| AC | API | FN |
|---|---|---|
| AC-01/02 | API-13/14 | FN-11 |
| AC-03..08 | API-02 | FN-01,04,12 |
| AC-10/23 | API-01/15 | FN-05 |
| AC-11/12 | API-05 | FN-03 |
| AC-13/14 | API-07 | FN-06 |
| AC-15/16 | API-08 | FN-06,12 |
| AC-17/18 | API-09 | FN-07 |
| AC-19/20 | API-04/12 | — |
| AC-21/22 | API-11 | FN-08,12 |
> Coverage FN-01..12 ✅ · XT-01..05 (write-back contracted/none) ✅

## §6.6 Performance
list p95<3s · create/approve<1s · license write <500ms sync · bulk chunk 200
