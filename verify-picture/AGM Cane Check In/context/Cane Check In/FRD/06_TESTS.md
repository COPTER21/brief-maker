# 06_TESTS — F-AGM-010 Cane Check-In

> Audience: QA + ai-testcase-md-generator · microcopy-aware · sync/idempotency + multi-method heavy

## §6.1 Acceptance Criteria

### List (US-01)
- **AC-01** 2 แท็บ (ต้องส่ง/เช็คอินแล้ว) + count "N รายการ" + 4 stats
- **AC-02** ค้นหา (CBM/NBM/ทะเบียน/เหรียญ/โควต้า/คนขับ) · filter สถานะ + แผนก + วันที่
- **AC-03** table columns ครบ · entry-type badge · status badge · pending: ปุ่มเช็คอิน
- **AC-04** checked-in tab: คอลัมน์ "สถานะ Booking" (CBM only) · non-CBM = "-"
- **AC-05** Export CSV → "กำลังดาวน์โหลดไฟล์ CSV" · pagination · empty → "ไม่พบรายการที่ค้นหา"

### Method chooser (US-02..04)
- **AC-06** เช็คอิน → modal 3 วิธี (เช็คอินจาก CBM / ไม่มีคิว-สมาชิก / ไม่มีคิว-โควต้ากลาง)

### CBM Check-In (US-02) ⭐
- **AC-07** ป้อนรหัส CBM ไม่มีจริง → "ไม่พบรหัส CBM นี้"
- **AC-08** ป้อนรหัส CBM มีจริง → farmer info แสดง
- **AC-09** weighToken ว่าง → "กรุณาใส่เลขเหรียญชั่ง"
- **AC-10** ยืนยันเช็คอิน → check-in + sync booking → "รอผลการเท"
- **AC-11** sync ล้ม → badge "ซิงก์ล้มเหลว" + ปุ่ม retry
- **AC-12** retry สำเร็จ → "ซิงก์สถานะ Booking สำเร็จ" · ล้ม → "ซิงก์ล้มเหลว กรุณาลองใหม่"

### Member Check-In (US-03)
- **AC-13** ค้นโควต้าไม่พบ → "ไม่พบโควต้านี้"
- **AC-14** ค้นพบ → "พบข้อมูลสมาชิก" + auto-fill
- **AC-15** ข้อมูลไม่ครบ → "กรุณากรอกข้อมูลให้ครบถ้วน"
- **AC-16** payment bill (งวด1/2) ไม่ครบ → "กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน"
- **AC-17** เช็คอินสำเร็จ → "เช็คอินสำเร็จ" (NBM doc)

### Central Quota Check-In (US-04)
- **AC-18** เช็คอินโควต้ากลาง (ข้อมูลรถ + payment bill) → "เช็คอินสำเร็จ"
- **AC-19** entryType กลาง → badge "โควต้ากลาง" · phaseA "-"

### QR Scan (US-05)
- **AC-20** Scan QR → modal "สแกน QR — CBM" · ป้อนรหัส → ไป → CBM flow

### Detail + Void (US-07/08)
- **AC-21** คลิกรหัสเอกสาร → detail drawer (เวลาเข้า/โควต้า/เกษตรกร/ทะเบียน/รถ/คนขับ/เหรียญ/ประเภทเข้า/สถานะ/สถานะ Booking)
- **AC-22** void → "ยกเลิกเช็คอิน (Void)" · เหตุผล(ไม่บังคับ) → "ยกเลิกเช็คอินสำเร็จ"

## §6.9 Cross-Module / Event Test Cases ⭐
| XT | Scenario | Source | Expected |
|---|---|---|---|
| XT-01 | CBM check-in | → Cane Booking (F-AGM-007) | event CHECK_IN → booking "รอผลการเท" (idempotent) |
| XT-02 | pending list | CBM dispatching (read) | รถ dispatching รอเข้าโรงงาน |
| XT-03 | member check-in | Quota/Member (read) | ค้นโควต้า + auto-fill |
| XT-04 | sync retry ซ้ำ (same checkin_id) | external Booking | 409/no-op ไม่ซ้ำผล |
| XT-05 | void | → Booking reversal | ยกเลิก + reversal event (SIT) |

## §6.10 Microcopy-Aware Expected (verbatim)
| จุด | ข้อความ |
|---|---|
| tabs | `ต้องส่ง` · `เช็คอินแล้ว` |
| ปุ่ม | `เช็คอิน` · `Scan QR` · `Export CSV` · `ล้าง` · `ยืนยันเช็คอิน` · `ยืนยัน` · `ไป` |
| method chooser | `เช็คอินจาก CBM` · `เช็คอินแบบไม่มีคิว — สมาชิก` · `เช็คอินแบบไม่มีคิว — โควต้ากลาง` |
| entry type | `โควต้าจองคิว` · `โควต้าไม่ได้จองคิว` · `โควต้ากลาง` |
| status | `จัดส่ง` · `รอทำจ่าย` · `เสร็จสิ้น` |
| booking sync | `ซิงก์ล้มเหลว` · `รอผลการเท` · `อยู่ระหว่างจัดส่ง` |
| payment bill | `บิลเขียว` · `บิลขาว` · `งวดที่ 1` · `งวดที่ 2` |
| vehicle type | `อีแต๋น` · `6ล้อ` · `10ล้อ` · `16ล้อ` |
| toast | `เช็คอินสำเร็จ` · `พบข้อมูลสมาชิก` · `ซิงก์สถานะ Booking สำเร็จ` · `ซิงก์ล้มเหลว กรุณาลองใหม่` · `ยกเลิกเช็คอินสำเร็จ` · `กำลังดาวน์โหลดไฟล์ CSV` |
| errors | `ไม่พบรหัส CBM นี้` · `ไม่พบโควต้านี้` · `กรุณาใส่เลขเหรียญชั่ง` · `กรุณากรอกข้อมูลให้ครบถ้วน` · `กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน` |
| void | `ยกเลิกเช็คอิน (Void)` · `เหตุผล (ไม่บังคับ)` |
| column | `เลขเหรียญชั่ง` · `ประเภทการเข้าโรงงาน` · `สถานะ Booking` |

## §6.8 Trace: AC → Logic
| AC | API | FN |
|---|---|---|
| AC-01..05 | API-01 | FN-01 |
| AC-06 | (UI) | — |
| AC-07..12 | API-C1/SYNC/RETRY | FN-C1,SYNC,11 |
| AC-13..17 | API-C2/04 | FN-C2,03 |
| AC-18..19 | API-C3 | FN-C3 |
| AC-20 | API-03 | FN-02 |
| AC-21..22 | API-02/V | FN-V |
> Coverage FN + FN-SYNC idempotent + FN-V ✅ · XT-01..05 ✅

## §6.6 Performance
list p95<3s · check-in<2s (inc sync) · sync idempotent + retry-safe · weighToken บังคับ · CSV ไทย
