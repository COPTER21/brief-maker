# 06_TESTS — F-AGM-007 Cane Booking Management

> Audience: QA + ai-testcase-md-generator · microcopy-aware · state-machine heavy

## §6.1 Acceptance Criteria

### สร้าง (US-01/08)
- **AC-01** สร้าง booking: เลือกโควตา → farmer snapshot · เลือกฤดูกาล(open) · สถานที่
- **AC-02** รอบเวลา/เลน + รถ(ประเภท/ทะเบียน/คนขับ/ตัน) required · ขาด → "กรุณากรอกข้อมูลให้ครบถ้วน"
- **AC-03** ประเภทบิล green/white · หักหนี้ % 0-100 → นอกช่วง "หักหนี้ต้องอยู่ระหว่าง 0-100"
- **AC-04** แสดงยอดหนี้คงค้าง (Debt) หรือ "ไม่มีแฟ้มลูกหนี้"
- **AC-05** ยืนยันสร้าง → toast "สร้างการจองสำเร็จ — [เลขจอง]" + สถานะ รออนุมัติ + audit

### อนุมัติ/ปฏิเสธ/ยกเลิก (US-02)
- **AC-06** อนุมัติ → verified · combined = "อนุมัติรอบจองแล้ว" (LOCK-07) + Gate B เปิด
- **AC-07** ปฏิเสธ ไม่ใส่เหตุผล → "กรุณาระบุเหตุผล" block
- **AC-08** ปฏิเสธ + reason → rejected · แกน B/C = "-"
- **AC-09** ยกเลิก + reason → cancelled

### แกน B (ตัด/ขนส่ง, no-skip) (US-03)
- **AC-10** verified & cut=null → list แสดง "รอส่งอนุมัติตัด" (derived)
- **AC-11** ขออนุมัติตัด → awaiting_cut_approval ("รออนุมัติตัด") + เปิดปุ่ม อนุมัติตัด
- **AC-12** อนุมัติตัด → awaiting_cutting ("รอตัด")
- **AC-13** จบการตัด → awaiting_dispatch ("รอจัดส่ง")
- **AC-14** **เริ่มจัดส่ง** → dispatching ("อยู่ระหว่างจัดส่ง") + dispatch_started_at
- **AC-15** ข้ามขั้น (อนุมัติตัด ก่อนขออนุมัติตัด) → "ไม่สามารถข้ามขั้นตอนได้"

### System events (US-04)
- **AC-16** จำลอง check-in → derived "รอผลการเท" + badge "ระบบกำหนด"
- **AC-17** จำลอง receiving-completed → ปิดแกน B (closed_at) + payment=awaiting_payment ("รอทำจ่าย")
- **AC-18** manual set รอทำจ่าย/เสร็จสิ้น → block "สถานะนี้ระบบจะอัปเดตให้อัตโนมัติ…"
- **AC-19** จำลอง payment-completed → completed ("เสร็จสิ้น") + lock

### List 3-axis + derived (US-05)
- **AC-20** 3 คอลัมน์ (การอนุมัติ/ตัด&ขนส่ง/การชำระเงิน) แสดง badge/-
- **AC-21** approval≠verified → แกน B/C "-"
- **AC-22** verified & cut=null → แกน B "รอส่งอนุมัติตัด"
- **AC-23** closed_at=null → แกน C "-"
- **AC-24** filter "ยังไม่เริ่ม" (per คอลัมน์) คืนเฉพาะ derived "-"

### Detail timeline (US-06)
- **AC-25** combined timeline 10 ขั้น highlight ปัจจุบัน
- **AC-26** ขั้น system (รอผลการเท/รอทำจ่าย/เสร็จสิ้น) มี 🔒
- **AC-27** ปุ่ม actions ตามสถานะ/RBAC (ซ่อนปุ่มที่ทำ system-state)

### Print (US-07)
- **AC-28** พิมพ์ใบสั่งตัด ก่อน awaiting_cutting → "ต้องอนุมัติตัดก่อน จึงจะพิมพ์ใบสั่งตัดได้"
- **AC-29** พิมพ์ใบสั่งตัด (≥awaiting_cutting) → เอกสาร CBM-CUT + QR
- **AC-30** พิมพ์ใบส่งอ้อย (≥awaiting_dispatch) → CBM-DLV + QR
- **AC-31** bulk download → ZIP (ตัดรายการที่ไม่ผ่าน gate + รายงาน)

### Void/lock (US-09) + search (US-10)
- **AC-33** ย้อนสถานะ (void) ที่ อยู่ระหว่างจัดส่ง + reason → revert รอจัดส่ง
- **AC-34** completed → read-only (ไม่มีปุ่มแก้)
- **AC-35** search (booking/quota/farmer/ทะเบียนรถ) · ไม่พบ → "ไม่พบรายการที่ค้นหา"
- **AC-36** export CSV แสดง "-" ตามจอ

## §6.9 Cross-Module / Event Test Cases ⭐
| XT | Scenario | Source | Expected |
|---|---|---|---|
| XT-01 | สร้าง booking | Quota/Season (read) | snapshot farmer + season ตรง |
| XT-02 | debt outstanding | Debt Mgt (read) | แสดงยอด/ไม่มีแฟ้ม |
| XT-03 | receiving-completed | ระบบรับอ้อย (event) | ปิดแกน B + รอทำจ่าย (idempotent) |
| XT-04 | payment-completed | ระบบการเงิน (event) | เสร็จสิ้น + lock |
| XT-05 | event ซ้ำ | external | 409/no-op ไม่ซ้ำผล |

## §6.10 Microcopy-Aware Expected (verbatim)
| จุด | ข้อความ |
|---|---|
| ปุ่มสร้าง | `สร้างการจอง` |
| approval actions | `อนุมัติ` · `ปฏิเสธ` · `ยกเลิก` |
| cut/dispatch actions | `ขออนุมัติตัด` · `อนุมัติตัด` · `จบการตัด` · `เริ่มจัดส่ง` |
| sim event | `จำลอง: เช็คอินโรงงาน` · `จำลอง: รับอ้อยเสร็จ` · `จำลอง: จ่ายเงินเสร็จ` |
| combined labels | `รออนุมัติ` · `อนุมัติรอบจองแล้ว` · `รอส่งอนุมัติตัด` · `รออนุมัติตัด` · `รอตัด` · `รอจัดส่ง` · `อยู่ระหว่างจัดส่ง` · `รอผลการเท` · `รอทำจ่าย` · `เสร็จสิ้น` |
| system badge | `ระบบกำหนด` (🔒) |
| print | `พิมพ์ใบสั่งตัด` · `พิมพ์ใบส่งอ้อย` |
| toast | `สร้างการจองสำเร็จ` · `อนุมัติแล้ว` · `ดำเนินการแล้ว` · `ย้อนสถานะแล้ว` |
| errors | ตาม §5.6 (ไม่สามารถข้ามขั้นตอนได้ · สถานะนี้ระบบจะอัปเดตให้อัตโนมัติ… · กรุณาระบุเหตุผล) |
| derived "-" | `-` (ยังไม่เริ่มเฟส) |

## §6.8 Trace: AC → Logic
| AC | API | FN |
|---|---|---|
| AC-01..05 | API-02/D | FN-01,12 |
| AC-06..09 | API-A1/A2/A3 | FN-A,11 |
| AC-10..15 | API-B1..B4 | FN-B,11,06 |
| AC-16..19 | API-E1/E2/E3 | FN-E,11 |
| AC-20..24 | API-01 | FN-05,06 |
| AC-25..27 | API-04 | FN-06 |
| AC-28..31 | API-P1/P2/Pbulk | FN-P |
| AC-33/34 | API-V | FN-V,11 |
> Coverage FN + guard(FN-11) + events(FN-E) ✅ · XT-01..05 ✅

## §6.6 Performance
list p95<3s · action<1s · event idempotent · PDF ไทย+QR · optimistic lock
