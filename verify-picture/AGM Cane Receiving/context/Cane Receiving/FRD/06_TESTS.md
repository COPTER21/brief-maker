# 06_TESTS — F-AGM-011 Cane Receiving

> Audience: QA + ai-testcase-md-generator · microcopy-aware · dump-v2 + Sync All + side-effects heavy

## §6.1 Acceptance Criteria

### List (US-01)
- **AC-01** 3 แท็บ (รอผลเท/เทแล้ว/ยกเลิก) + count + 4 stats
- **AC-02** ค้นหา (เลขเหรียญ/รหัส/ทะเบียน) · filter สถานะ + ประเภทอ้อย + ประเภทเข้า + date
- **AC-03** draft columns (รหัสเกษตรกร/เลขเหรียญ/วัน-เวลาเข้า/ผู้ขนส่ง/เบอร์/ทะเบียน/ประเภทรถ/คนขับ) · issued/void + มูลค่าอ้อย/ประเภทการเทอ้อย/สถานะ
- **AC-04** Export CSV → "กำลังส่งออกข้อมูล..." → "ส่งออกข้อมูลสำเร็จ"

### Issue Receiving + Dump v2 (US-02) ⭐
- **AC-05** เปิด Issue drawer → checkin snapshot read-only ครบ
- **AC-06** กด ดึงผลการเท (Auto) สำเร็จ → card v2 (ประเภทอ้อย code+name / เวลาเข้า / เวลาออก / น.น.รวม / น.น.รถเบา / น.น.อ้อยสุทธิ) + lock read-only + badge Auto
- **AC-07** ดึงผลการเท fail → "ไม่พบผลการเทจากโรงงาน — กรุณาเปลี่ยนเป็นโหมด Manual" + badge Manual
- **AC-08** manual net ว่าง → "กรุณากรอกน้ำหนักสุทธิ"
- **AC-09** manual net ผิดรูปแบบ → "กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง"
- **AC-10** manual ไม่ใส่เหตุผล → "กรุณากรอกเหตุผลการกรอกด้วยตนเอง"
- **AC-11** ออกใบรับอ้อย (auto/manual ครบ) → "ออกใบรับอ้อยสำเร็จ" + CRN + ย้ายไปแท็บเทแล้ว + side effects (CBM awaiting_payment, ปลดเหรียญ, PDF)

### Sync All (US-03) ⭐
- **AC-12** ปุ่ม Sync All (RBAC) ในแท็บรอผลเท
- **AC-13** Sync All ไม่เลือกวันที่ → บังคับเลือกวันที่ก่อน
- **AC-14** Sync All → "กำลังดึงผลการเท..." → result modal (ทั้งหมด N / สำเร็จ X / ล้มเหลว Y)
- **AC-15** result modal failed table (เลขเหรียญ/รหัสสมาชิก/เกษตรกร/error) · "ไม่พบข้อมูลผลการเทในระบบโรงงาน"
- **AC-16** ปุ่ม [ดูรายการที่ล้มเหลว] / [ปิด] · toast "ดึงผลการเทเสร็จสิ้น (สำเร็จ X, ล้มเหลว Y)"

### Detail + PDF (US-04/05)
- **AC-17** detail → block ผลการเท read-only + document info
- **AC-18** พิมพ์ → PDF A4 + QR viewer · ไม่มี PDF → "ไม่พบ PDF"

### Void (US-06) ⭐
- **AC-19** void reason <5 → "เหตุผลต้องมีความยาวอย่างน้อย 5 ตัวอักษร"
- **AC-20** void สำเร็จ → "Void ใบรับอ้อยสำเร็จ" + สถานะ Void + rollback CBM (note awaiting_dump_result)
- **AC-21** void ที่ชำระเงินแล้ว → block

### QR/Search (US-07)
- **AC-22** Scan QR / ค้นหาเลขเหรียญชั่ง → เลือกรายการ → issue flow

## §6.9 Cross-Module / Event Test Cases ⭐
| XT | Scenario | Source | Expected |
|---|---|---|---|
| XT-01 | Draft = checked-in ยังไม่ออกใบ | Check-in (F-AGM-010) | รายการ Draft ตรง |
| XT-02 | ดึงผลการเท v2 | Factory dump API | caneType+times+weights (ไม่มี CCS) |
| XT-03 | ออกใบ → CBM | → CBM (F-AGM-007) | awaiting_payment + free coin (idempotent) |
| XT-04 | Receiving → Payment | → Cane Payment | net_weight + cane_type (SoT) ส่งต่อ |
| XT-05 | void → CBM | → CBM | awaiting_dump_result (rollback, ไม่ชำระต่อ) |

## §6.10 Microcopy-Aware Expected (verbatim)
| จุด | ข้อความ |
|---|---|
| tabs | `รอผลเท` · `เทแล้ว` · `ยกเลิก` |
| ปุ่ม | `ออกใบรับอ้อย` · `ดึงผลการเท (Auto)` · `สลับเป็นโหมดกรอกมือ` · `รีเซ็ต / กลับไป Auto` · `Sync All & ออกใบรับอ้อยอัตโนมัติ` · `Scan QR` · `Export CSV` · `พิมพ์` · `Void` · `ดูรายการที่ล้มเหลว` · `ปิด` |
| dump card | `ประเภทอ้อย` · `เลขเหรียญชั่ง` · `เวลาเข้า (Time In)` · `เวลาออก (Time Out)` · `น.น. รวม (กก.)` · `น.น. รถเบา (กก.)` · `น.น. อ้อยสุทธิ (กก.)` |
| entry type | `จองคิว` · `ไม่จองคิว` · `โควต้ากลาง` |
| status | `รอผลเท`(Draft) · `เทแล้ว`(Issued) · `ยกเลิก`(Void) |
| Sync All modal | `ทั้งหมด` · `สำเร็จ` · `ล้มเหลว` · `รหัสสมาชิก` |
| toast | `ออกใบรับอ้อยสำเร็จ` · `Void ใบรับอ้อยสำเร็จ` · `กำลังดึงผลการเท...` · `ดึงผลการเทเสร็จสิ้น` · `กำลังส่งออกข้อมูล...` · `ส่งออกข้อมูลสำเร็จ` · `ไม่พบ PDF` |
| errors | `ไม่พบผลการเทจากโรงงาน — กรุณาเปลี่ยนเป็นโหมด Manual` · `กรุณากรอกน้ำหนักสุทธิ` · `กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง` · `กรุณากรอกเหตุผลการกรอกด้วยตนเอง` · `เหตุผลต้องมีความยาวอย่างน้อย 5 ตัวอักษร` · `ไม่พบข้อมูลผลการเทในระบบโรงงาน` |

## §6.8 Trace: AC → Logic
| AC | API | FN |
|---|---|---|
| AC-01..04 | API-01/03 | FN-01 |
| AC-05..11 | API-DUMP/C1 | FN-DUMP,C1,VALID,SIDE |
| AC-12..16 | API-SYNC | FN-SYNC |
| AC-17..18 | API-02/PDF | FN-PDF |
| AC-19..21 | API-V | FN-V |
| AC-22 | (UI) | — |
> Coverage FN + FN-SIDE (CBM+coin+PDF) + FN-11 idempotent ✅ · XT-01..05 ✅

## §6.6 Performance
list p95<3s · issue<2s · Sync All async batch idempotent · dump snapshot audit · PDF ไทย A4+QR · optimistic (etag)
