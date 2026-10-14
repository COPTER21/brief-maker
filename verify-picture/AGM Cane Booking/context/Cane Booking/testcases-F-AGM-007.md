# AI Test Cases — F-AGM-007 Cane Booking Management (จัดการจองรอบส่งอ้อย)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `cane-booking-management.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ FRD 06_TESTS §6.10 microcopy + 05_RULES แล้ว) · Expected เช็คได้ด้วยตา
เคสที่ prototype จำลองไม่ได้ (server-side optimistic lock 409 / event idempotency-ซ้ำจริง / PDF·QR จริง / RBAC·SoD / Debt Mgt·Quota อ่านจริง / bulk ZIP·export) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-007 (AGM/CBM — จัดการจองรอบส่งอ้อย) |
| App entry | เปิดไฟล์ `cane-booking-management.html` ใน browser (Chrome desktop ≥1280px) |
| Routes | `#/bookings` (list — default) · `#/bookings/:booking_id` (detail drawer, refresh-safe) |
| ที่มา | FRD_F-AGM-007_Pack (06_TESTS AC-01..36 + XT-01..05 · 05_RULES BR-CBM-01..10 / VR-01..06 / EC-01..16) |
| จำนวนเคส | 54 เคส / 10 groups |
| Signature ⭐⭐⭐ | **3-AXIS state machine** (ไม่ใช่ cascade) — A การอนุมัติ · B ตัด&ขนส่ง (no-skip) · C การชำระเงิน → รวมเป็น **combined progress 10 ขั้น** ที่แสดงบนจอ |
| แกน A (approval) | `waiting_for_verify → verified → (rejected / cancelled = terminal)` |
| แกน B (cut_transport, no-skip) | `null → awaiting_cut_approval → awaiting_cutting → awaiting_dispatch → dispatching` (**ไม่มี state 'dispatched'** · ปิดแกนด้วย closed_at) |
| แกน C (payment) | `not_due → awaiting_payment → completed` |
| Combined 10 ขั้น (visible) | รออนุมัติ → อนุมัติรอบจองแล้ว → รอส่งอนุมัติตัด → รออนุมัติตัด → รอตัด → รอจัดส่ง → อยู่ระหว่างจัดส่ง → รอผลการเท → รอทำจ่าย → เสร็จสิ้น |
| Derived (ไม่ store) | "รอส่งอนุมัติตัด" = verified & cut=null · "อยู่ระหว่างจัดส่ง" = dispatch_started_at set · "รอผลการเท" = checkin & !dump_result |
| System-controlled 🔒 | 3 ขั้นท้าย (**รอผลการเท / รอทำจ่าย / เสร็จสิ้น**) มี 🔒 + badge **ระบบกำหนด** — เข้าถึงได้เฉพาะผ่านปุ่ม `จำลอง:` เท่านั้น · manual set ไม่ได้ |
| หมายเหตุ mock | prototype เป็น in-memory: refresh หน้า (F5) = ข้อมูล reset กลับ seed 10 การจอง + 4 โควตา — ใช้เป็นข้อดี: ทุกเคส independent โดย refresh ก่อนเริ่ม |
| Cross-module ⭐ | อ่าน Quota/Season (snapshot farmer) + Debt Mgt (ยอดหนี้ค้าง) · รับ event จากระบบรับอ้อย (receiving-completed) + ระบบการเงิน (payment-completed) — reconcile จริง = `(ต้อง simulate)` ที่ SIT |

**Seed ตั้งต้น (หลัง refresh — 10 การจอง CBM-2568-0000001..0000010):**

| เลขจอง | โควตา · เกษตรกร | รถ (ทะเบียน) | เลน/รอบ | บิล | หักหนี้% | combined สถานะ (ความคืบหน้า) |
|---|---|---|---|---|---|---|
| CBM-2568-0000001 | QUO-2568-0001 · สมชาย ไร่ทอง | รถ 6 ล้อ 70-1234 กจ | A1 08:00-10:00 | บิลเขียว | 10 | **รออนุมัติ** |
| CBM-2568-0000002 | QUO-2568-0002 · บุญมี ทุ่งกว้าง | รถ 10 ล้อ 82-5567 กจ | B1 10:00-12:00 | บิลขาว | 0 | **ปฏิเสธ** |
| CBM-2568-0000003 | QUO-2568-0003 · ประเสริฐ ใจดี | รถอีแต๋น บบ-9021 กจ | C1 06:00-08:00 | บิลเขียว | 15 | **รอส่งอนุมัติตัด** (verified & cut=null) |
| CBM-2568-0000004 | QUO-2568-0004 · วิไล สวนอ้อย | รถ 16 ล้อ 90-3311 นฐ | A2 13:00-15:00 | บิลขาว | 0 | **รออนุมัติตัด** |
| CBM-2568-0000005 | QUO-2568-0001 · สมชาย ไร่ทอง | รถ 10 ล้อ 70-8890 กจ | B2 15:00-17:00 | บิลเขียว | 20 | **รอตัด** |
| CBM-2568-0000006 | QUO-2568-0002 · บุญมี ทุ่งกว้าง | รถ 6 ล้อ 82-1102 กจ | A1 08:00-10:00 | บิลเขียว | 0 | **รอจัดส่ง** (cut: ตัดด้วยรถตัดอ้อย · 1 คัน) |
| CBM-2568-0000007 | QUO-2568-0003 · ประเสริฐ ใจดี | รถ 16 ล้อ 90-4478 นฐ | C1 10:00-12:00 | บิลขาว | 5 | **อยู่ระหว่างจัดส่ง** (dispatch_started_at) |
| CBM-2568-0000008 | QUO-2568-0004 · วิไล สวนอ้อย | รถ 10 ล้อ 90-7781 นฐ | B1 13:00-15:00 | บิลเขียว | 0 | **รอผลการเท** 🔒 |
| CBM-2568-0000009 | QUO-2568-0001 · สมชาย ไร่ทอง | รถ 10 ล้อ 70-2020 กจ | A2 06:00-08:00 | บิลเขียว | 30 | **รอทำจ่าย** 🔒 |
| CBM-2568-0000010 | QUO-2568-0003 · ประเสริฐ ใจดี | รถ 6 ล้อ 90-6655 นฐ | A1 08:00-10:00 | บิลขาว | 12 | **เสร็จสิ้น** 🔒 (read-only) |

- CBM-0000002 reject_reason = "ข้อมูลทะเบียนรถไม่ตรงกับที่แจ้ง กรุณาแก้ไขและส่งใหม่"
- **Stat cards:** การจองทั้งหมด = **10** · รออนุมัติ = **1** (0000001) · กำลังตัด/ขนส่ง = **5** (0000004/0000005/0000006/0000007/0000008) · เสร็จสิ้น = **1** (0000010)

**3-axis display บนตาราง (คอลัมน์ การอนุมัติ / ตัด&ขนส่ง / การชำระเงิน · ยังไม่เริ่มแสดง `-`):**

| เลขจอง | การอนุมัติ (A) | ตัด&ขนส่ง (B) | การชำระเงิน (C) | ความคืบหน้า (combined) |
|---|---|---|---|---|
| 0000001 | รออนุมัติ | `-` | `-` | รออนุมัติ |
| 0000002 | ปฏิเสธ | `-` | `-` | ปฏิเสธ |
| 0000003 | อนุมัติรอบจองแล้ว | รอส่งอนุมัติตัด | `-` | รอส่งอนุมัติตัด |
| 0000004 | อนุมัติรอบจองแล้ว | รออนุมัติตัด | `-` | รออนุมัติตัด |
| 0000005 | อนุมัติรอบจองแล้ว | รอตัด | `-` | รอตัด |
| 0000006 | อนุมัติรอบจองแล้ว | รอจัดส่ง | `-` | รอจัดส่ง |
| 0000007 | อนุมัติรอบจองแล้ว | อยู่ระหว่างจัดส่ง | `-` | อยู่ระหว่างจัดส่ง |
| 0000008 | อนุมัติรอบจองแล้ว | อยู่ระหว่างจัดส่ง | `-` | รอผลการเท 🔒 |
| 0000009 | อนุมัติรอบจองแล้ว | (ปิดแกน · closed_at) | รอทำจ่าย | รอทำจ่าย 🔒 |
| 0000010 | อนุมัติรอบจองแล้ว | (ปิดแกน · closed_at) | เสร็จสิ้น | เสร็จสิ้น 🔒 |

> ⚠ **derived signature:** 0000003 มี A=verified แต่ cut=null → B แสดง **รอส่งอนุมัติตัด** (ไม่ store) · 0000007/0000008 dispatch_started_at → B แสดง **อยู่ระหว่างจัดส่ง** · closed_at=null ทุกใบที่ ≤ 0000008 → C แสดง `-`

**Seed โควตา (4 รายการ — จาก `QUOTAS` const, READ-ONLY · quota search):**

| เลขโควตา | เกษตรกร | เบอร์ | ยอดหนี้ค้าง (Debt) |
|---|---|---|---|
| QUO-2568-0001 | สมชาย ไร่ทอง | 0812345678 | 125,000 |
| QUO-2568-0002 | บุญมี ทุ่งกว้าง | 0898765432 | **ไม่มีแฟ้มลูกหนี้** (null) |
| QUO-2568-0003 | ประเสริฐ ใจดี | 0861112222 | 48,000 |
| QUO-2568-0004 | วิไล สวนอ้อย | 0873334444 | **ไม่มีแฟ้มลูกหนี้** (null) |

> quota search placeholder = **พิมพ์เลขโควตา หรือ ชื่อเกษตรกร** · ค้นด้วยเลขโควตา/ชื่อเกษตรกร · ไม่พบ → **ไม่พบโควตา** · Debt read-only (Debt Mgt GET only — reconcile จริง = SIT)

**VERBATIM microcopy (Expected anchors — copy เป๊ะ):**
- ปุ่ม: `สร้างการจอง` · `ยืนยันสร้าง` · `อนุมัติ` · `ปฏิเสธ` · `ยกเลิก` · `ขออนุมัติตัด` · `อนุมัติตัด` · `จบการตัด` · `เริ่มจัดส่ง` · `ย้อนสถานะ` · `ยืนยันย้อนสถานะ` · `พิมพ์ใบสั่งตัด` · `พิมพ์ใบส่งอ้อย` · `ปิด` · `ล้างตัวกรอง` · `ตรวจสอบที่เลือก (N)`
- Sim events (ทางเดียวสู่สถานะระบบ): `จำลอง: เช็คอินโรงงาน` · `จำลอง: รับอ้อยเสร็จ` · `จำลอง: จ่ายเงินเสร็จ` · system badge `ระบบกำหนด`
- Combined labels: `รออนุมัติ` · `อนุมัติรอบจองแล้ว` · `รอส่งอนุมัติตัด` · `รออนุมัติตัด` · `รอตัด` · `รอจัดส่ง` · `อยู่ระหว่างจัดส่ง` · `รอผลการเท` · `รอทำจ่าย` · `เสร็จสิ้น` · `ปฏิเสธ`
- List headers: `เลขจอง` · `เกษตรกร/โควตา` · `ฤดูกาล` · `วันเวลา/เลน` · `รถ(ทะเบียน)` · `การอนุมัติ` · `ตัด&ขนส่ง` · `การชำระเงิน` · `ความคืบหน้า` · `ดาวน์โหลด`
- Detail: stepper heading `ความคืบหน้ารวม (10 ขั้น)` · 3-axis labels `การอนุมัติ` · `ตัด&ขนส่ง` · `การชำระเงิน`
- Toasts: `สร้างการจองสำเร็จ — [เลขจอง]` · `อนุมัติแล้ว` · `ดำเนินการแล้ว` · `ย้อนสถานะแล้ว`
- Errors: `ไม่สามารถข้ามขั้นตอนได้` (no-skip) · `สถานะนี้ระบบจะอัปเดตให้อัตโนมัติ เมื่อข้อมูลจากระบบอื่นเสร็จสิ้น` (manual system state) · `กรุณาระบุเหตุผล` · `กรุณากรอกข้อมูลให้ครบถ้วน` · `กรุณาระบุคนขับ` · `กรุณากรอกปริมาณคาดส่ง` · `หักหนี้ต้องอยู่ระหว่าง 0-100` · `ไม่พบรายการที่ค้นหา` · `ไม่พบโควตา`
- Print gate: `ต้องอนุมัติตัดก่อน จึงจะพิมพ์ใบสั่งตัดได้` · `ต้องอยู่สถานะรอจัดส่งขึ้นไป จึงจะพิมพ์ใบนำส่งได้` · Doc no. `CBM-CUT-2568-000000N` / `CBM-DLV-2568-000000N` + QR
- Server (simulate): `ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรช` (409 stale) · `รายการซ้ำ (idempotent)` (409 dup) · `ไม่มีสิทธิ์ดำเนินการ` (403)

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| L — รายการ / 3-axis display / derived "-" / filters (ยังไม่เริ่ม) | TC-L01..L05 (5) | สูงสุด |
| C — สร้างการจอง + quota search + debt% + required | TC-C01..C07 (7) | สูงสุด |
| A — อนุมัติ / ปฏิเสธ / ยกเลิก (reason บังคับ) | TC-A01..A05 (5) | สูง |
| B — แกน B no-skip (send/approve/finish/dispatch + ข้ามขั้น block) ⭐ | TC-B01..B07 (7) | สูงสุด |
| E — System events (checkin/receiving/payment ผ่าน sim + manual block) ⭐ | TC-E01..E05 (5) | สูงสุด |
| W — Detail timeline 10-step + 🔒 + actions | TC-W01..W05 (5) | สูง |
| P — Print gates (CUT / DLV) | TC-P01..P05 (5) | สูง |
| V — ย้อนสถานะ / void + completed read-only | TC-V01..V04 (4) | สูง |
| Q — ค้นหา + export | TC-Q01..Q03 (3) | กลาง |
| X — Cross-module / event XT-01..05 + system simulate | TC-X01..X08 (8) | สูงสุด |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1)
| AC | รายละเอียด (ย่อ) | cases |
|---|---|---|
| AC-01 | สร้าง booking: quota → farmer snapshot · ฤดูกาล(open) · สถานที่ | TC-C01, TC-X01 |
| AC-02 | รอบเวลา/เลน + รถ(ประเภท/ทะเบียน/คนขับ/ตัน) required · ขาด → "กรุณากรอกข้อมูลให้ครบถ้วน" | TC-C05, TC-C07 |
| AC-03 | บิล green/white · หักหนี้ % 0-100 → นอกช่วง "หักหนี้ต้องอยู่ระหว่าง 0-100" | TC-C06 |
| AC-04 | แสดงยอดหนี้คงค้าง (Debt) หรือ "ไม่มีแฟ้มลูกหนี้" | TC-C02, TC-C03, TC-X02 |
| AC-05 | ยืนยันสร้าง → toast "สร้างการจองสำเร็จ — [เลขจอง]" + รออนุมัติ + audit | TC-C01 |
| AC-06 | อนุมัติ → verified · combined "อนุมัติรอบจองแล้ว" + Gate B เปิด | TC-A01, TC-A05 |
| AC-07 | ปฏิเสธ ไม่ใส่เหตุผล → "กรุณาระบุเหตุผล" block | TC-A02 |
| AC-08 | ปฏิเสธ + reason → rejected · แกน B/C = "-" | TC-A03, TC-L02 |
| AC-09 | ยกเลิก + reason → cancelled | TC-A04 |
| AC-10 | verified & cut=null → list "รอส่งอนุมัติตัด" (derived) | TC-L03, TC-B01 |
| AC-11 | ขออนุมัติตัด → awaiting_cut_approval ("รออนุมัติตัด") + เปิด อนุมัติตัด | TC-B01 |
| AC-12 | อนุมัติตัด → awaiting_cutting ("รอตัด") | TC-B02 |
| AC-13 | จบการตัด → awaiting_dispatch ("รอจัดส่ง") | TC-B03 |
| AC-14 | เริ่มจัดส่ง → dispatching ("อยู่ระหว่างจัดส่ง") + dispatch_started_at | TC-B04, TC-B07 |
| AC-15 | ข้ามขั้น (อนุมัติตัด ก่อนขออนุมัติตัด) → "ไม่สามารถข้ามขั้นตอนได้" | TC-B05 |
| AC-16 | จำลอง check-in → derived "รอผลการเท" + badge "ระบบกำหนด" | TC-E01 |
| AC-17 | จำลอง receiving-completed → ปิดแกน B (closed_at) + "รอทำจ่าย" | TC-E02, TC-X03 |
| AC-18 | manual set รอทำจ่าย/เสร็จสิ้น → block "สถานะนี้ระบบจะอัปเดตให้อัตโนมัติ…" | TC-E04 |
| AC-19 | จำลอง payment-completed → completed ("เสร็จสิ้น") + lock | TC-E03, TC-X04 |
| AC-20 | 3 คอลัมน์ (การอนุมัติ/ตัด&ขนส่ง/การชำระเงิน) แสดง badge/- | TC-L01 |
| AC-21 | approval≠verified → แกน B/C "-" | TC-L02 |
| AC-22 | verified & cut=null → แกน B "รอส่งอนุมัติตัด" | TC-L03 |
| AC-23 | closed_at=null → แกน C "-" | TC-L02, TC-L05 |
| AC-24 | filter "ยังไม่เริ่ม" (per คอลัมน์) คืนเฉพาะ derived "-" | TC-L04, TC-L05 |
| AC-25 | combined timeline 10 ขั้น highlight ปัจจุบัน | TC-W01 |
| AC-26 | ขั้น system (รอผลการเท/รอทำจ่าย/เสร็จสิ้น) มี 🔒 | TC-W02 |
| AC-27 | ปุ่ม actions ตามสถานะ/RBAC (ซ่อนปุ่มที่ทำ system-state) | TC-W04, TC-A05 |
| AC-28 | พิมพ์ใบสั่งตัด ก่อน awaiting_cutting → "ต้องอนุมัติตัดก่อน จึงจะพิมพ์ใบสั่งตัดได้" | TC-P01 |
| AC-29 | พิมพ์ใบสั่งตัด (≥awaiting_cutting) → CBM-CUT + QR | TC-P02 |
| AC-30 | พิมพ์ใบส่งอ้อย (≥awaiting_dispatch) → CBM-DLV + QR · ก่อนถึง → block | TC-P03, TC-P04 |
| AC-31 | bulk download → ZIP (ตัดที่ไม่ผ่าน gate + รายงาน) | TC-P05 (ต้อง simulate) |
| AC-33 | ย้อนสถานะ (void) ที่ อยู่ระหว่างจัดส่ง + reason → revert รอจัดส่ง | TC-V01, TC-V04 |
| AC-34 | completed → read-only (ไม่มีปุ่มแก้) | TC-V03 |
| AC-35 | search (booking/quota/farmer/ทะเบียนรถ) · ไม่พบ → "ไม่พบรายการที่ค้นหา" | TC-Q01, TC-Q02 |
| AC-36 | export CSV แสดง "-" ตามจอ | TC-Q03 (ต้อง simulate) |

> **หมายเหตุ:** FRD 06_TESTS ข้าม **AC-32** (ลำดับ AC-31 → AC-33 · US-09 void/lock ไม่มี AC-32) — ครอบคลุมทุก AC ที่ FRD นิยาม: AC-01..31, AC-33..36

### Cross-Module / Event (06_TESTS §6.9) ⭐
| XT | Scenario | Source | cases |
|---|---|---|---|
| XT-01 | สร้าง booking → snapshot farmer + season ตรง (source ไม่ถูกแก้) | Quota/Season (read) | TC-X01 |
| XT-02 | debt outstanding → แสดงยอด/ไม่มีแฟ้ม | Debt Mgt (read) | TC-X02, TC-C02, TC-C03 |
| XT-03 | receiving-completed → ปิดแกน B + รอทำจ่าย (idempotent) | ระบบรับอ้อย (event) | TC-X03, TC-E02 |
| XT-04 | payment-completed → เสร็จสิ้น + lock | ระบบการเงิน (event) | TC-X04, TC-E03 |
| XT-05 | event ซ้ำ (event_id เดิม) → 409/no-op ไม่ซ้ำผล | external | TC-X05 (ต้อง simulate) |

### Business Rules (05_RULES §5.1)
| BR | cases |
|---|---|
| BR-CBM-01 no-skip A→B→C · Gate B เมื่อ A=verified · C เมื่อ B closed | TC-B01..B05, TC-B06, TC-A05 |
| BR-CBM-02 system-controlled (รอผลการเท/รอทำจ่าย/เสร็จสิ้น) manual ไม่ได้ · event เท่านั้น | TC-E01, TC-E03, TC-E04, TC-W02 |
| BR-CBM-03 idempotent + optimistic (row_version) ทุก action/event | TC-X05, TC-X06, TC-C01 |
| BR-CBM-04 reverse/reject/cancel/void ต้องมี reason + audit | TC-A02, TC-A03, TC-A04, TC-V01, TC-V02 |
| BR-CBM-05 debt % 0-100 · offset จริงที่ Payment | TC-C06, TC-X02 |
| BR-CBM-06 completed → read-only | TC-V03, TC-W02 |
| BR-CBM-07 print CUT ≥ awaiting_cutting · DLV ≥ awaiting_dispatch | TC-P01, TC-P02, TC-P03, TC-P04 |
| BR-CBM-08 ไม่มี dispatched · ปิดแกน B ด้วย closed_at | TC-B04, TC-E02, TC-L05 |
| BR-CBM-09 verified label "อนุมัติรอบจองแล้ว" | TC-A01, TC-L03 |
| BR-CBM-10 derived display + phase "-" + filter "ยังไม่เริ่ม" | TC-L02, TC-L03, TC-L04, TC-L05 |

### Validation (05_RULES §5.4)
| VR | cases |
|---|---|
| VR-01 quota/season/รถ/เลน/เวลา required → "กรุณากรอกข้อมูลให้ครบถ้วน" | TC-C05, TC-C07 |
| VR-02 debt % 0-100 → "หักหนี้ต้องอยู่ระหว่าง 0-100" | TC-C06 |
| VR-03 reason บังคับ (reject/cancel/void/reverse) → "กรุณาระบุเหตุผล" | TC-A02, TC-A04, TC-V02 |
| VR-04 no-skip guard → "ไม่สามารถข้ามขั้นตอนได้" | TC-B05 |
| VR-05 system-controlled manual → "สถานะนี้ระบบจะอัปเดตให้อัตโนมัติ เมื่อข้อมูลจากระบบอื่นเสร็จสิ้น" | TC-E04 |
| VR-06 print gate → "ต้องอนุมัติตัดก่อน…" / "ต้องอยู่สถานะรอจัดส่งขึ้นไป…" | TC-P01, TC-P03 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 approve booking → verified · Gate B เปิด | TC-A01, TC-A05 |
| EC-02 ขออนุมัติตัด ก่อน verified → block (Gate) | TC-B06 |
| EC-03 ข้ามขั้น → "ไม่สามารถข้ามขั้นตอนได้" | TC-B05 |
| EC-04 manual set รอทำจ่าย/เสร็จสิ้น → VR-05 block | TC-E04 |
| EC-05 check-in event → derived "รอผลการเท" | TC-E01 |
| EC-06 receiving-completed → ปิดแกน B + "รอทำจ่าย" | TC-E02, TC-X03 |
| EC-07 receiving สำเร็จ แต่สร้างคำขอจ่ายล้ม → banner + retry | TC-E05 (ต้อง simulate) |
| EC-08 payment-completed → completed (lock) | TC-E03, TC-X04 |
| EC-09 event ซ้ำ (event_id เดิม) → 409/no-op | TC-X05 (ต้อง simulate) |
| EC-10 print CUT ก่อน awaiting_cutting → block | TC-P01 |
| EC-11 print DLV ก่อน awaiting_dispatch → block | TC-P03 |
| EC-12 void ที่ อยู่ระหว่างจัดส่ง → revert รอจัดส่ง + clear dispatch_started_* | TC-V01, TC-V04 |
| EC-13 edit หลัง completed → read-only | TC-V03 |
| EC-14 phase display (approval≠verified → B/C "-" · verified&cut=null → รอส่งอนุมัติตัด) | TC-L02, TC-L03 |
| EC-15 filter "ยังไม่เริ่ม" B → cut=null | TC-L04 |
| EC-16 optimistic stale → 409 CONFLICT_UPDATE_STALE | TC-X06 (ต้อง simulate) |

### Error Catalog (05_RULES §5.6 — UI-observable)
| error | cases |
|---|---|
| VALIDATION_FAILED "กรุณากรอกข้อมูลให้ครบถ้วน" · "กรุณาระบุคนขับ" · "กรุณากรอกปริมาณคาดส่ง" · "หักหนี้ต้องอยู่ระหว่าง 0-100" | TC-C05, TC-C06, TC-C07 |
| (reason) "กรุณาระบุเหตุผล" | TC-A02, TC-A04, TC-V02 |
| ILLEGAL_STATE_TRANSITION "ไม่สามารถข้ามขั้นตอนได้" / "สถานะนี้ระบบจะอัปเดตให้อัตโนมัติ เมื่อข้อมูลจากระบบอื่นเสร็จสิ้น" | TC-B05, TC-E04 |
| (print gate) "ต้องอนุมัติตัดก่อน จึงจะพิมพ์ใบสั่งตัดได้" / "ต้องอยู่สถานะรอจัดส่งขึ้นไป จึงจะพิมพ์ใบนำส่งได้" | TC-P01, TC-P03 |
| (search / quota) "ไม่พบรายการที่ค้นหา" / "ไม่พบโควตา" | TC-Q02, TC-C04 |
| CONFLICT_UPDATE_STALE(409) "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรช" | TC-X06 (simulate) |
| CONFLICT(409) "รายการซ้ำ (idempotent)" | TC-X05 (simulate) |
| FORBIDDEN "ไม่มีสิทธิ์ดำเนินการ" | TC-X07 (simulate) |

### State Machine / Scope Lock (05_RULES §5.2 · LOCK-01..05)
| item | ข้อยืนยัน (ย่อ) | cases |
|---|---|---|
| A machine | waiting → verified → (rejected/cancelled) | TC-A01, TC-A03, TC-A04, TC-L02 |
| B machine (no-skip · ไม่มี dispatched) | null → cut_approval → cutting → dispatch → dispatching · ปิดด้วย closed_at | TC-B01..B04, TC-B07, TC-E02 |
| C machine | not_due → awaiting_payment → completed | TC-E02, TC-E03 |
| combined 10-step derived | รออนุมัติ…เสร็จสิ้น | TC-L01, TC-W01 |
| system-controlled 🔒 (3 ขั้นท้าย) | ผ่าน sim เท่านั้น | TC-E01, TC-E03, TC-E04, TC-W02 |

### Permission (05_RULES §5.3)
| cell | cases |
|---|---|
| CBM.Approver/Admin: create/approve/reject/cancel/void/print = allow (prototype user เดียวกดได้ทุก action) | TC-C01, TC-A01, TC-V01, TC-P02 |
| Cut.Manager / Dispatch.Manager: แกน B actions = allow | TC-B01..B04 |
| Finance.Manager (events) + SoD flag (OQ-CB4) — RBAC deny / SoD | TC-X07 (ต้อง simulate) |

**Manifest cross-check (FRD §0.12):** AC 35/35 (AC-01..31, 33..36 · AC-32 ไม่มีใน FRD) · XT-01..05 5/5 · BR-CBM-01..10 10/10 · VR-01..06 6/6 · EC-01..16 16/16 → ทุกแถว manifest มีคู่ใน Ledger ✅

---

## Data Sets

### ชุด A — การจองถูกต้อง (happy — QUO-2568-0001 · สมชาย ไร่ทอง)
| ฟิลด์ (ป้ายบนจอ) | ค่า |
|---|---|
| ค้นหาโควตา (placeholder "พิมพ์เลขโควตา หรือ ชื่อเกษตรกร") | เลือก **QUO-2568-0001 · สมชาย ไร่ทอง** *(sub "0812345678")* |
| farmer snapshot (read-only หลังเลือก) | สมชาย ไร่ทอง · 0812345678 |
| ยอดหนี้ค้าง (Debt) | **125,000** (แสดงอัตโนมัติจาก Debt Mgt) |
| ฤดูกาล (open) | ฤดูกาล 2568/69 |
| สถานที่ | ลานรับอ้อยหน้าโรงงาน |
| รอบเวลา/เลน | เลน A3 · 08:00-10:00 |
| ประเภทรถ / ทะเบียน | รถ 6 ล้อ / 70-4545 กจ |
| คนขับ | สมพงษ์ ขับดี |
| ปริมาณคาดส่ง (ตัน) | 18.50 |
| ประเภทบิล | **บิลเขียว** |
| หักหนี้ (%) | 10 |

### ชุด B — ค่าผิดสำหรับ negative (เลือก quota ชุด A ก่อน)
| กรณี | ฟิลด์ | ค่า | คาดหวัง (ข้อความจริง) |
|---|---|---|---|
| B1 | หักหนี้ (%) | `150` | หักหนี้ต้องอยู่ระหว่าง 0-100 |
| B2 | หักหนี้ (%) | `-5` | หักหนี้ต้องอยู่ระหว่าง 0-100 |
| B3 | เลน/รอบเวลา/รถ | *(เว้นว่าง)* | กรุณากรอกข้อมูลให้ครบถ้วน |
| B4 | คนขับ | *(เว้นว่าง)* | กรุณาระบุคนขับ |
| B5 | ปริมาณคาดส่ง (ตัน) | *(เว้นว่าง)* | กรุณากรอกปริมาณคาดส่ง |
| B6 | ค้นหาโควตา | พิมพ์ `QUO-9999` | ไม่พบโควตา |
| B7 | ค้นหาโควตา (debt null) | เลือก `QUO-2568-0002` | ไม่มีแฟ้มลูกหนี้ |

---

## Test Cases

## Group L — รายการ / 3-axis display / derived "-" / filters (P-01)

### TC-L01 — เปิดหน้า list + stats + 3-axis columns (happy — AC-20)
- group: L · ความสำคัญ: สูงสุด · trace: AC-20 / BR-CBM-10 / UI loaded
- Setup: seed=default 10 การจอง (refresh) · files=—
- Start: OPEN `#/bookings`
- ผ่านเมื่อ: list + stat cards + 3 axis columns แสดงตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bookings` | — | หัวข้อ **จัดการจองรอบส่งอ้อย** + count **10 รายการ** · sidebar/breadcrumb active | ☐ |
| 2 | VERIFY แถบ stats 4 การ์ด | — | **การจองทั้งหมด 10** · **รออนุมัติ 1** · **กำลังตัด/ขนส่ง 5** · **เสร็จสิ้น 1** | ☐ |
| 3 | VERIFY หัวคอลัมน์ตาราง | — | เรียง: **เลขจอง · เกษตรกร/โควตา · ฤดูกาล · วันเวลา/เลน · รถ(ทะเบียน) · การอนุมัติ · ตัด&ขนส่ง · การชำระเงิน · ความคืบหน้า · ดาวน์โหลด** | ☐ |
| 4 | VERIFY แถว CBM-2568-0000001 (รออนุมัติ) | — | การอนุมัติ = **รออนุมัติ** · ตัด&ขนส่ง = **-** · การชำระเงิน = **-** · ความคืบหน้า = **รออนุมัติ** | ☐ |
| 5 | VERIFY แถว CBM-2568-0000010 (เสร็จสิ้น) | — | ความคืบหน้า = **เสร็จสิ้น** + ไอคอน 🔒 + badge **ระบบกำหนด** · การชำระเงิน = **เสร็จสิ้น** | ☐ |
| 6 | VERIFY ปุ่มบน page header | — | ปุ่ม **สร้างการจอง** (ขวาบน) · ปุ่ม **ตรวจสอบที่เลือก (0)** (disabled) | ☐ |

### TC-L02 — approval≠verified → แกน B/C "-" (AC-21 / AC-23 / EC-14)
- group: L · ความสำคัญ: สูง · trace: AC-21, AC-23 / BR-CBM-10 / EC-14
- Setup: seed=default · files=—
- Start: OPEN `#/bookings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว CBM-2568-0000001 (waiting_for_verify) | — | ตัด&ขนส่ง = **-** · การชำระเงิน = **-** (แกน A ยังไม่ verified → B/C ยังไม่เริ่ม) | ☐ |
| 2 | VERIFY แถว CBM-2568-0000002 (rejected) | — | การอนุมัติ = **ปฏิเสธ** · ตัด&ขนส่ง = **-** · การชำระเงิน = **-** (terminal, ไม่เปิดแกน B/C) | ☐ |
| 3 | VERIFY แถว CBM-2568-0000007 (อยู่ระหว่างจัดส่ง) การชำระเงิน | — | การชำระเงิน = **-** (closed_at=null → C ยังไม่เริ่ม แม้ B กำลังทำงาน) | ☐ |

### TC-L03 — verified & cut=null → derived "รอส่งอนุมัติตัด" (AC-10 / AC-22 / BR-CBM-09)
- group: L · ความสำคัญ: สูงสุด · trace: AC-10, AC-22 / EC-14 / derived signature
- Setup: seed=default · files=—
- Start: OPEN `#/bookings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว CBM-2568-0000003 | — | การอนุมัติ = **อนุมัติรอบจองแล้ว** (verified label · BR-CBM-09) · ตัด&ขนส่ง = **รอส่งอนุมัติตัด** (derived: verified & cut=null · ไม่ store) · การชำระเงิน = **-** | ☐ |
| 2 | VERIFY ความคืบหน้าแถวเดียวกัน | — | combined = **รอส่งอนุมัติตัด** (ขั้นที่ 3 ใน 10 ขั้น) | ☐ |

### TC-L04 — filter "ยังไม่เริ่ม" บนแกน ตัด&ขนส่ง (AC-24 / EC-15)
- group: L · ความสำคัญ: สูง · trace: AC-24 / EC-15 / filter B "ยังไม่เริ่ม"
- Setup: seed=default · files=—
- Start: OPEN `#/bookings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT dropdown filter **ตัด&ขนส่ง** = **ยังไม่เริ่ม** | — | คืนเฉพาะ cut=null → 3 แถว: CBM-0000001 (B "-"), CBM-0000002 (B "-"), CBM-0000003 (B "รอส่งอนุมัติตัด") | ☐ |
| 2 | CLICK **ล้างตัวกรอง** | — | ตารางกลับ 10 รายการ | ☐ |

### TC-L05 — filter "ยังไม่เริ่ม" บนแกน การชำระเงิน (AC-24 / AC-23 / BR-CBM-08)
- group: L · ความสำคัญ: สูง · trace: AC-23, AC-24 / closed_at=null → C "-"
- Setup: seed=default · files=—
- Start: OPEN `#/bookings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT dropdown filter **การชำระเงิน** = **ยังไม่เริ่ม** | — | คืนเฉพาะ closed_at=null (C "-") → 8 แถว (0000001..0000008) · **ไม่รวม** 0000009 (รอทำจ่าย) และ 0000010 (เสร็จสิ้น) | ☐ |
| 2 | SELECT filter **การชำระเงิน** = *(ค่าที่แสดง รอทำจ่าย)* | — | เหลือ 1 แถว CBM-2568-0000009 · การชำระเงิน = **รอทำจ่าย** 🔒 | ☐ |
| 3 | CLICK **ล้างตัวกรอง** | — | กลับ 10 รายการ | ☐ |

---

## Group C — สร้างการจอง + quota search + debt% + required (OV-01)

### TC-C01 — สร้างการจอง happy (AC-01/05) ★
- group: C · ความสำคัญ: สูงสุด · trace: AC-01, AC-05 / BR-CBM-03 / XT-01
- Setup: seed=default · files=—
- Start: OPEN `#/bookings`
- ชุดข้อมูล: A
- ผ่านเมื่อ: สร้างสำเร็จ + toast + แถวใหม่ รออนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างการจอง** | — | drawer เปิดจากขวา หัวข้อ **สร้างการจอง** · ช่องค้นหาโควตา placeholder **พิมพ์เลขโควตา หรือ ชื่อเกษตรกร** | ☐ |
| 2 | TYPE "QUO-2568-0001" → เลือก **QUO-2568-0001 · สมชาย ไร่ทอง** | A | farmer snapshot แสดง **สมชาย ไร่ทอง · 0812345678** (read-only) · ยอดหนี้ค้าง **125,000** | ☐ |
| 3 | กรอก: ฤดูกาล 2568/69 · สถานที่ · เลน A3 08:00-10:00 · รถ 6 ล้อ 70-4545 กจ · คนขับ สมพงษ์ ขับดี · ปริมาณคาดส่ง 18.50 · บิลเขียว · หักหนี้ 10 | A | แสดงค่าครบทุก section | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันสร้าง** → WAIT | — | drawer ปิด + toast เขียว **สร้างการจองสำเร็จ — CBM-2568-0000011** | ☐ |
| 5 | VERIFY ตาราง | — | แถวใหม่ CBM-2568-0000011 · การอนุมัติ = **รออนุมัติ** · ตัด&ขนส่ง = **-** · count = **11 รายการ** · การ์ดรออนุมัติ = 2 | ☐ |

### TC-C02 — Quota search + debt แสดงยอด (happy — AC-04 / XT-02)
- group: C · ความสำคัญ: สูง · trace: AC-04 / XT-02 / BR-CBM-05
- Setup: seed=default · files=—
- Start: OPEN `#/bookings` → CLICK **สร้างการจอง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ประเสริฐ" → ช่องค้นหาโควตา (ค้นด้วยชื่อ) | — | dropdown พบ **QUO-2568-0003 · ประเสริฐ ใจดี** (sub "0861112222") | ☐ |
| 2 | CLICK ตัวเลือก QUO-2568-0003 | — | farmer snapshot = ประเสริฐ ใจดี · ยอดหนี้ค้าง **48,000** (จาก Debt Mgt) | ☐ |

### TC-C03 — Quota ไม่มีแฟ้มลูกหนี้ (edge — AC-04 / XT-02)
- group: C · ความสำคัญ: กลาง · trace: AC-04 / "ไม่มีแฟ้มลูกหนี้" (null)
- Setup: seed=default · files=—
- Start: OPEN `#/bookings` → CLICK **สร้างการจอง**
- ชุดข้อมูล: B7

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "QUO-2568-0002" → เลือก **QUO-2568-0002 · บุญมี ทุ่งกว้าง** | B7 | farmer snapshot = บุญมี ทุ่งกว้าง · ช่องยอดหนี้ค้างแสดง **ไม่มีแฟ้มลูกหนี้** (Debt = null) | ☐ |
| 2 | เลือก **QUO-2568-0004 · วิไล สวนอ้อย** | — | เช่นเดียวกัน: **ไม่มีแฟ้มลูกหนี้** | ☐ |

### TC-C04 — Quota ค้นไม่พบ → "ไม่พบโควตา" (negative — AC-01)
- group: C · ความสำคัญ: กลาง · trace: AC-01 / emptyText
- Setup: seed=default · files=—
- Start: OPEN `#/bookings` → CLICK **สร้างการจอง**
- ชุดข้อมูล: B6

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "QUO-9999" → ช่องค้นหาโควตา | B6 | dropdown แสดงข้อความว่าง **ไม่พบโควตา** · farmer snapshot ไม่ปรากฏ | ☐ |

### TC-C05 — required ครบชุด → block (negative — AC-02 / VR-01)
- group: C · ความสำคัญ: สูง · trace: AC-02 / VR-01 / "กรุณากรอกข้อมูลให้ครบถ้วน"
- Setup: seed=default · files=—
- Start: OPEN `#/bookings` → CLICK **สร้างการจอง** → เลือก QUO-2568-0001
- ชุดข้อมูล: B3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เว้น **เลน/รอบเวลา/รถ** ว่าง → CLICK **ยืนยันสร้าง** | B3 | ไม่บันทึก + toast/ข้อความ **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | VERIFY count ตาราง (หลังปิด drawer) | — | ยัง 10 รายการ | ☐ |

### TC-C06 — หักหนี้ % นอกช่วง 0-100 (negative — AC-03 / VR-02)
- group: C · ความสำคัญ: สูง · trace: AC-03 / VR-02 / BR-CBM-05
- Setup: seed=default · files=—
- Start: OPEN `#/bookings` → CLICK **สร้างการจอง** → เลือก QUO-2568-0001 → กรอกฟิลด์ครบ
- ชุดข้อมูล: B1, B2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "150" → ช่อง **หักหนี้ (%)** → CLICK **ยืนยันสร้าง** | B1 | ข้อความแดง **หักหนี้ต้องอยู่ระหว่าง 0-100** — ไม่บันทึก | ☐ |
| 2 | แก้เป็น "-5" → CLICK **ยืนยันสร้าง** | B2 | เช่นเดียวกัน **หักหนี้ต้องอยู่ระหว่าง 0-100** | ☐ |
| 3 | แก้เป็น "10" → CLICK **ยืนยันสร้าง** → WAIT | — | บันทึกสำเร็จ toast **สร้างการจองสำเร็จ — [เลขจอง]** | ☐ |

### TC-C07 — คนขับ / ปริมาณคาดส่ง required (negative — AC-02 / VR-01)
- group: C · ความสำคัญ: สูง · trace: AC-02 / VR-01 / field-level messages
- Setup: seed=default · files=—
- Start: OPEN `#/bookings` → CLICK **สร้างการจอง** → เลือก QUO-2568-0001 → กรอกฟิลด์อื่นครบ
- ชุดข้อมูล: B4, B5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เว้น **คนขับ** ว่าง → CLICK **ยืนยันสร้าง** | B4 | ข้อความแดง **กรุณาระบุคนขับ** | ☐ |
| 2 | กรอกคนขับ · เว้น **ปริมาณคาดส่ง (ตัน)** ว่าง → CLICK **ยืนยันสร้าง** | B5 | ข้อความแดง **กรุณากรอกปริมาณคาดส่ง** | ☐ |

---

## Group A — อนุมัติ / ปฏิเสธ / ยกเลิก (OV-02)

### TC-A01 — อนุมัติ → verified "อนุมัติรอบจองแล้ว" (happy — AC-06 / EC-01)
- group: A · ความสำคัญ: สูง · trace: AC-06 / BR-CBM-01/09 / EC-01
- Setup: seed=default (CBM-0000001 รออนุมัติ) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000001`
- ผ่านเมื่อ: อนุมัติ → combined "อนุมัติรอบจองแล้ว" + Gate B เปิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว drawer + ปุ่ม | — | หัวข้อ **CBM-2568-0000001** · combined **รออนุมัติ** · มีปุ่ม **อนุมัติ / ปฏิเสธ / ยกเลิก** | ☐ |
| 2 | CLICK ปุ่ม **อนุมัติ** → WAIT | — | toast เขียว **อนุมัติแล้ว** · combined เปลี่ยนเป็น **อนุมัติรอบจองแล้ว** · ตัด&ขนส่ง = **รอส่งอนุมัติตัด** (Gate B เปิด · cut=null) | ☐ |
| 3 | VERIFY ปุ่ม actions หลังอนุมัติ | — | ไม่มี อนุมัติ/ปฏิเสธ แล้ว · มีปุ่ม **ขออนุมัติตัด** (แกน B เริ่มได้) | ☐ |

### TC-A02 — ปฏิเสธ ไม่ใส่เหตุผล → block (negative — AC-07 / VR-03)
- group: A · ความสำคัญ: สูงสุด · trace: AC-07 / VR-03 / BR-CBM-04
- Setup: seed=default (CBM-0000001 รออนุมัติ) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000001` → CLICK **ปฏิเสธ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ปฏิเสธ** โดย **ไม่กรอกเหตุผล** | — | **block** + ข้อความ **กรุณาระบุเหตุผล** — ไม่เปลี่ยนสถานะ | ☐ |

### TC-A03 — ปฏิเสธ + reason → rejected · B/C "-" (happy — AC-08)
- group: A · ความสำคัญ: สูง · trace: AC-08 / EC-14
- Setup: seed=default (CBM-0000001 รออนุมัติ) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000001` → CLICK **ปฏิเสธ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "เอกสารประกอบไม่ครบ" → ช่องเหตุผล → CLICK **ปฏิเสธ** → WAIT | — | toast **ดำเนินการแล้ว** · combined = **ปฏิเสธ** · ตัด&ขนส่ง = **-** · การชำระเงิน = **-** | ☐ |
| 2 | VERIFY (seed) CBM-2568-0000002 reject_reason | — | เปิด CBM-0000002 → แสดง reason **ข้อมูลทะเบียนรถไม่ตรงกับที่แจ้ง กรุณาแก้ไขและส่งใหม่** | ☐ |

### TC-A04 — ยกเลิก + reason → cancelled (happy — AC-09 / VR-03)
- group: A · ความสำคัญ: สูง · trace: AC-09 / BR-CBM-04
- Setup: seed=default (CBM-0000001 รออนุมัติ) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000001` → CLICK **ยกเลิก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิก** โดยไม่กรอกเหตุผล | — | block + **กรุณาระบุเหตุผล** | ☐ |
| 2 | TYPE "เกษตรกรขอยกเลิกรอบส่ง" → CLICK **ยกเลิก** → WAIT | — | toast **ดำเนินการแล้ว** · combined = สถานะ **ยกเลิก** (cancelled · terminal) | ☐ |

### TC-A05 — Gate B ปิดจนกว่า approve · actions ตามสถานะ (AC-06 / AC-27 / EC-01)
- group: A · ความสำคัญ: สูง · trace: AC-06, AC-27 / BR-CBM-01 (Gate B)
- Setup: seed=default · files=—
- Start: OPEN `#/bookings/CBM-2568-0000001` (รออนุมัติ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม actions บน CBM-0000001 (รออนุมัติ) | — | มี **อนุมัติ / ปฏิเสธ / ยกเลิก** · **ไม่มี** ปุ่ม ขออนุมัติตัด (Gate B ปิด เพราะ A≠verified) | ☐ |
| 2 | OPEN CBM-2568-0000003 (verified & cut=null) → VERIFY ปุ่ม | — | มีปุ่ม **ขออนุมัติตัด** (Gate B เปิดแล้ว) · ไม่มี อนุมัติ/ปฏิเสธ | ☐ |

---

## Group B — แกน B (ตัด/ขนส่ง, no-skip) (OV-03) ⭐

### TC-B01 — ขออนุมัติตัด → "รออนุมัติตัด" (happy — AC-10/11)
- group: B · ความสำคัญ: สูงสุด · trace: AC-10, AC-11 / BR-CBM-01
- Setup: seed=default (CBM-0000003 รอส่งอนุมัติตัด) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000003`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY combined | — | **รอส่งอนุมัติตัด** · มีปุ่ม **ขออนุมัติตัด** | ☐ |
| 2 | CLICK ปุ่ม **ขออนุมัติตัด** → WAIT | — | toast **ดำเนินการแล้ว** · combined = **รออนุมัติตัด** (awaiting_cut_approval) · ปรากฏปุ่ม **อนุมัติตัด** | ☐ |

### TC-B02 — อนุมัติตัด → "รอตัด" (happy — AC-12)
- group: B · ความสำคัญ: สูง · trace: AC-12 / BR-CBM-01
- Setup: seed=default (CBM-0000004 รออนุมัติตัด) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000004`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY combined + ปุ่ม | — | **รออนุมัติตัด** · มีปุ่ม **อนุมัติตัด** | ☐ |
| 2 | CLICK ปุ่ม **อนุมัติตัด** → WAIT | — | toast **ดำเนินการแล้ว** · combined = **รอตัด** (awaiting_cutting) · ปรากฏปุ่ม **จบการตัด** | ☐ |

### TC-B03 — จบการตัด → "รอจัดส่ง" (happy — AC-13)
- group: B · ความสำคัญ: สูง · trace: AC-13 / BR-CBM-01
- Setup: seed=default (CBM-0000005 รอตัด) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000005`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY combined + ปุ่ม | — | **รอตัด** · มีปุ่ม **จบการตัด** | ☐ |
| 2 | CLICK ปุ่ม **จบการตัด** → WAIT | — | toast **ดำเนินการแล้ว** · combined = **รอจัดส่ง** (awaiting_dispatch) · ปรากฏปุ่ม **เริ่มจัดส่ง** | ☐ |

### TC-B04 — เริ่มจัดส่ง → "อยู่ระหว่างจัดส่ง" (happy — AC-14 / BR-CBM-08)
- group: B · ความสำคัญ: สูงสุด · trace: AC-14 / BR-CBM-08 (ไม่มี dispatched · dispatch_started_at)
- Setup: seed=default (CBM-0000006 รอจัดส่ง) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000006`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY combined + ปุ่ม | — | **รอจัดส่ง** · มีปุ่ม **เริ่มจัดส่ง** | ☐ |
| 2 | CLICK ปุ่ม **เริ่มจัดส่ง** → WAIT | — | toast **ดำเนินการแล้ว** · combined = **อยู่ระหว่างจัดส่ง** (derived: dispatch_started_at set · ไม่มี state 'dispatched') | ☐ |
| 3 | VERIFY ปุ่ม actions หลังเริ่มจัดส่ง | — | ปรากฏปุ่ม **ย้อนสถานะ** (void ได้) · ปุ่มถัดไปของแกน B ไม่มี (รอ event เช็คอิน — system) | ☐ |

### TC-B05 — ข้ามขั้น → "ไม่สามารถข้ามขั้นตอนได้" (negative — AC-15 / VR-04 / EC-03)
- group: B · ความสำคัญ: สูงสุด · trace: AC-15 / VR-04 / EC-03 / no-skip guard
- Setup: seed=default (CBM-0000003 รอส่งอนุมัติตัด · cut=null) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000003`
- ผ่านเมื่อ: พยายามข้าม (อนุมัติตัด ก่อน ขออนุมัติตัด) → block

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY UI: ที่ รอส่งอนุมัติตัด ปุ่มที่เปิดคือ **ขออนุมัติตัด** เท่านั้น | — | ปุ่ม **อนุมัติตัด/จบการตัด/เริ่มจัดส่ง** ไม่ปรากฏ (UI บังคับลำดับ · no-skip) | ☐ |
| 2 | (ยิง transition อนุมัติตัด ตรง ๆ ผ่าน guard) | — | guard FN-11 คืน **ไม่สามารถข้ามขั้นตอนได้** — สถานะไม่เปลี่ยน | ☐ |

### TC-B06 — ขออนุมัติตัด ก่อน verified → block (negative — EC-02 / Gate B)
- group: B · ความสำคัญ: สูง · trace: EC-02 / BR-CBM-01 (Gate B ปิดเมื่อ A≠verified)
- Setup: seed=default (CBM-0000001 รออนุมัติ) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000001`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม actions | — | มีเฉพาะ **อนุมัติ / ปฏิเสธ / ยกเลิก** · **ไม่มี** ปุ่ม ขออนุมัติตัด (Gate B ปิด — ต้อง verified ก่อน) | ☐ |

### TC-B07 — B chain เต็มลูป (รอส่งอนุมัติตัด → อยู่ระหว่างจัดส่ง) (integration — AC-11..14)
- group: B · ความสำคัญ: สูง · trace: AC-11..14 / BR-CBM-01 (no-skip sequence)
- Setup: seed=default (CBM-0000003 รอส่งอนุมัติตัด) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000003`
- ผ่านเมื่อ: เดินครบ 4 step ตามลำดับ ไม่ข้าม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ขออนุมัติตัด** → WAIT | — | combined = **รออนุมัติตัด** | ☐ |
| 2 | CLICK **อนุมัติตัด** → WAIT | — | combined = **รอตัด** | ☐ |
| 3 | CLICK **จบการตัด** → WAIT | — | combined = **รอจัดส่ง** | ☐ |
| 4 | CLICK **เริ่มจัดส่ง** → WAIT | — | combined = **อยู่ระหว่างจัดส่ง** (dispatch_started_at) · ครบ 4 transition ไม่ข้ามขั้น | ☐ |

---

## Group E — System events (checkin/receiving/payment ผ่าน sim เท่านั้น) (OV-04) ⭐

### TC-E01 — จำลอง เช็คอินโรงงาน → "รอผลการเท" 🔒 (happy — AC-16 / EC-05)
- group: E · ความสำคัญ: สูงสุด · trace: AC-16 / BR-CBM-02 / EC-05
- Setup: seed=default (CBM-0000007 อยู่ระหว่างจัดส่ง) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000007`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY combined + ปุ่ม sim | — | **อยู่ระหว่างจัดส่ง** · มีปุ่ม **จำลอง: เช็คอินโรงงาน** | ☐ |
| 2 | CLICK ปุ่ม **จำลอง: เช็คอินโรงงาน** → WAIT | — | combined = **รอผลการเท** (derived: checkin & !dump_result) + ไอคอน 🔒 + badge **ระบบกำหนด** | ☐ |
| 3 | VERIFY ปุ่ม | — | ปรากฏปุ่มถัดไป **จำลอง: รับอ้อยเสร็จ** · ไม่มีปุ่ม manual set สถานะ | ☐ |

### TC-E02 — จำลอง รับอ้อยเสร็จ → ปิดแกน B + "รอทำจ่าย" (happy — AC-17 / EC-06 / XT-03)
- group: E · ความสำคัญ: สูงสุด · trace: AC-17 / EC-06 / BR-CBM-08 / XT-03
- Setup: seed=default (CBM-0000008 รอผลการเท 🔒) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000008`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY combined + ปุ่ม sim | — | **รอผลการเท** 🔒 badge **ระบบกำหนด** · มีปุ่ม **จำลอง: รับอ้อยเสร็จ** | ☐ |
| 2 | CLICK ปุ่ม **จำลอง: รับอ้อยเสร็จ** → WAIT | — | ปิดแกน B (closed_at set) + payment = awaiting_payment · combined = **รอทำจ่าย** 🔒 badge **ระบบกำหนด** | ☐ |
| 3 | VERIFY การชำระเงิน column (กลับ list) | — | การชำระเงิน = **รอทำจ่าย** (C เริ่มหลัง B closed) | ☐ |

### TC-E03 — จำลอง จ่ายเงินเสร็จ → "เสร็จสิ้น" + lock (happy — AC-19 / EC-08 / XT-04)
- group: E · ความสำคัญ: สูงสุด · trace: AC-19 / EC-08 / BR-CBM-06 / XT-04
- Setup: seed=default (CBM-0000009 รอทำจ่าย 🔒) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000009`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY combined + ปุ่ม sim | — | **รอทำจ่าย** 🔒 · มีปุ่ม **จำลอง: จ่ายเงินเสร็จ** | ☐ |
| 2 | CLICK ปุ่ม **จำลอง: จ่ายเงินเสร็จ** → WAIT | — | combined = **เสร็จสิ้น** 🔒 badge **ระบบกำหนด** · การจองถูก lock (read-only) | ☐ |
| 3 | VERIFY ปุ่ม actions หลังเสร็จสิ้น | — | ไม่มีปุ่ม action ใด ๆ (completed → read-only · BR-CBM-06) | ☐ |

### TC-E04 — manual set สถานะระบบ → block (negative — AC-18 / VR-05 / EC-04)
- group: E · ความสำคัญ: สูงสุด · trace: AC-18 / VR-05 / EC-04 / BR-CBM-02
- Setup: seed=default (CBM-0000007 อยู่ระหว่างจัดส่ง) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000007`
- ผ่านเมื่อ: ไม่มีทาง manual ไปสถานะระบบ · ถ้าลอง → block

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY: ไม่มีปุ่ม manual สำหรับ รอผลการเท/รอทำจ่าย/เสร็จสิ้น | — | สถานะระบบ 3 ขั้นท้ายไม่มีปุ่มกดเอง — มีเฉพาะ **จำลอง:** events | ☐ |
| 2 | (ยิง transition ไป awaiting_payment ตรง ๆ ผ่าน guard) | — | block + **สถานะนี้ระบบจะอัปเดตให้อัตโนมัติ เมื่อข้อมูลจากระบบอื่นเสร็จสิ้น** (VR-05 · ILLEGAL_STATE_TRANSITION) | ☐ |

### TC-E05 — receiving สำเร็จ แต่สร้างคำขอจ่ายล้ม → banner + retry (edge — EC-07) (ต้อง simulate)
- group: E · ความสำคัญ: กลาง · trace: EC-07 · **prototype: sim สำเร็จเสมอ (ไม่มี fault injection) — failure path = SIT**
- Setup: **simulate — ระบบจริง:** receiving-completed ผ่าน แต่ API สร้างคำขอจ่ายล้ม
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): receiving-completed สำเร็จ · สร้างคำขอจ่ายล้ม | — | คง **อยู่ระหว่างจัดส่ง**/รอผลการเท + banner **สร้างคำขอจ่ายไม่สำเร็จ — ระบบจะพยายามใหม่อัตโนมัติ** + retry (idempotent) | ☐ |

---

## Group W — Detail timeline 10-step + 🔒 + actions (P-02)

### TC-W01 — Detail combined timeline 10 ขั้น highlight (AC-25)
- group: W · ความสำคัญ: สูง · trace: AC-25 / stepper "ความคืบหน้ารวม (10 ขั้น)"
- Setup: seed=default (CBM-0000006 รอจัดส่ง) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000006`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY heading stepper | — | หัวข้อ **ความคืบหน้ารวม (10 ขั้น)** · แสดง 10 ขั้น: รออนุมัติ → อนุมัติรอบจองแล้ว → รอส่งอนุมัติตัด → รออนุมัติตัด → รอตัด → รอจัดส่ง → อยู่ระหว่างจัดส่ง → รอผลการเท → รอทำจ่าย → เสร็จสิ้น | ☐ |
| 2 | VERIFY ขั้นปัจจุบัน highlight | — | ขั้นที่ **รอจัดส่ง** (ขั้น 6) ถูก highlight เป็นปัจจุบัน · ขั้น 1-5 ทำเสร็จ (past) · ขั้น 7-10 ยังไม่ถึง | ☐ |

### TC-W02 — system steps 🔒 + badge "ระบบกำหนด" (AC-26 / BR-CBM-02/06)
- group: W · ความสำคัญ: สูง · trace: AC-26 / BR-CBM-02 / system-controlled
- Setup: seed=default (CBM-0000010 เสร็จสิ้น 🔒) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000010`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY 3 ขั้นท้ายของ stepper | — | **รอผลการเท / รอทำจ่าย / เสร็จสิ้น** แต่ละขั้นมีไอคอน 🔒 + badge **ระบบกำหนด** | ☐ |
| 2 | VERIFY combined + actions | — | combined = **เสร็จสิ้น** · ไม่มีปุ่ม action (read-only · BR-CBM-06) | ☐ |

### TC-W03 — 3-axis section (การอนุมัติ/ตัด&ขนส่ง/การชำระเงิน) ใน detail (AC-25)
- group: W · ความสำคัญ: กลาง · trace: AC-25 / 3-axis section labels
- Setup: seed=default (CBM-0000007 อยู่ระหว่างจัดส่ง) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000007`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY 3 section แกน | — | section **การอนุมัติ** = อนุมัติรอบจองแล้ว (verified) · **ตัด&ขนส่ง** = อยู่ระหว่างจัดส่ง · **การชำระเงิน** = - (ยังไม่เริ่ม) | ☐ |
| 2 | VERIFY snapshot จอง | — | โควตา QUO-2568-0003 · ประเสริฐ ใจดี · รถ 16 ล้อ 90-4478 นฐ · เลน C1 10:00-12:00 · บิลขาว · หักหนี้ 5% | ☐ |

### TC-W04 — actions ตามสถานะ/RBAC (ซ่อนปุ่ม system-state) (AC-27)
- group: W · ความสำคัญ: สูง · trace: AC-27 / BR-CBM-02
- Setup: seed=default · files=—
- Start: OPEN `#/bookings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN CBM-0000005 (รอตัด) | — | มีปุ่ม **จบการตัด** + **พิมพ์ใบสั่งตัด** · ไม่มีปุ่ม system-state | ☐ |
| 2 | OPEN CBM-0000008 (รอผลการเท 🔒) | — | มีเฉพาะ **จำลอง: รับอ้อยเสร็จ** · ไม่มีปุ่ม manual สำหรับสถานะระบบ | ☐ |
| 3 | OPEN CBM-0000010 (เสร็จสิ้น 🔒) | — | ไม่มีปุ่ม action ใด ๆ (read-only) | ☐ |

### TC-W05 — Deep-link refresh-safe + not found (routes)
- group: W · ความสำคัญ: กลาง · trace: 01_UI routes / refresh-safe
- Setup: seed=default · files=—
- Start: OPEN `#/bookings/CBM-2568-0000003` (พิมพ์ URL ตรง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bookings/CBM-2568-0000003` | — | list โหลด + Detail drawer **CBM-2568-0000003** เปิดเองทันที | ☐ |
| 2 | PRESS F5 (refresh) | — | drawer CBM-2568-0000003 ยังเปิด (refresh-safe) — ยืนยัน mock reset seed กลับ 10 การจอง | ☐ |
| 3 | OPEN `#/bookings/CBM-2568-9999999` (ไม่มี) | — | ไม่เปิด drawer + เด้งกลับ `#/bookings` | ☐ |

---

## Group P — Print gates (CUT / DLV) (OV-05)

### TC-P01 — พิมพ์ใบสั่งตัด ก่อน awaiting_cutting → block (negative — AC-28 / VR-06 / EC-10)
- group: P · ความสำคัญ: สูง · trace: AC-28 / VR-06 / EC-10 / BR-CBM-07
- Setup: seed=default (CBM-0000003 รอส่งอนุมัติตัด · < awaiting_cutting) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000003`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **พิมพ์ใบสั่งตัด** (หรือไอคอน ดาวน์โหลด) | — | block + ข้อความ **ต้องอนุมัติตัดก่อน จึงจะพิมพ์ใบสั่งตัดได้** — ไม่ออกเอกสาร | ☐ |
| 2 | OPEN CBM-0000004 (รออนุมัติตัด · ยังไม่ถึง awaiting_cutting) → CLICK **พิมพ์ใบสั่งตัด** | — | เช่นเดียวกัน block **ต้องอนุมัติตัดก่อน จึงจะพิมพ์ใบสั่งตัดได้** | ☐ |

### TC-P02 — พิมพ์ใบสั่งตัด (≥awaiting_cutting) → CBM-CUT + QR (happy — AC-29)
- group: P · ความสำคัญ: สูง · trace: AC-29 / BR-CBM-07
- Setup: seed=default (CBM-0000005 รอตัด · = awaiting_cutting) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000005`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **พิมพ์ใบสั่งตัด** | — | เปิดเอกสารใบสั่งตัด เลขที่ **CBM-CUT-2568-0000005** + QR (prototype = mock preview · PDF จริง = SIT) | ☐ |
| 2 | VERIFY: CBM-0000006 (รอจัดส่ง · > awaiting_cutting) พิมพ์ CUT ได้ | — | ออกใบสั่งตัด **CBM-CUT-2568-0000006** ได้ (สถานะสูงกว่ายังพิมพ์ CUT ได้) | ☐ |

### TC-P03 — พิมพ์ใบส่งอ้อย ก่อน awaiting_dispatch → block (negative — AC-30 / VR-06 / EC-11)
- group: P · ความสำคัญ: สูง · trace: AC-30 / VR-06 / EC-11 / BR-CBM-07
- Setup: seed=default (CBM-0000005 รอตัด · < awaiting_dispatch) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000005`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **พิมพ์ใบส่งอ้อย** | — | block + **ต้องอยู่สถานะรอจัดส่งขึ้นไป จึงจะพิมพ์ใบนำส่งได้** | ☐ |

### TC-P04 — พิมพ์ใบส่งอ้อย (≥awaiting_dispatch) → CBM-DLV + QR (happy — AC-30)
- group: P · ความสำคัญ: สูง · trace: AC-30 / BR-CBM-07
- Setup: seed=default (CBM-0000006 รอจัดส่ง = awaiting_dispatch · CBM-0000007 อยู่ระหว่างจัดส่ง) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000006`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **พิมพ์ใบส่งอ้อย** | — | ออกใบส่งอ้อย เลขที่ **CBM-DLV-2568-0000006** + QR | ☐ |
| 2 | OPEN CBM-0000007 (อยู่ระหว่างจัดส่ง) → CLICK **พิมพ์ใบส่งอ้อย** | — | ออก **CBM-DLV-2568-0000007** ได้ (สถานะสูงกว่ายังพิมพ์ DLV ได้) | ☐ |

### TC-P05 — Bulk download → ZIP (ตัดที่ไม่ผ่าน gate) (AC-31) (ต้อง simulate)
- group: P · ความสำคัญ: กลาง · trace: AC-31 · **prototype: ZIP จริง/รายงาน = server-side — mark BLOCKED บน prototype**
- Setup: **simulate — ระบบจริง**
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): เลือกหลายรายการ → bulk download | — | ได้ ZIP เฉพาะรายการที่ผ่าน gate (CUT/DLV) + รายงานรายการที่ถูกตัด (ไม่ผ่าน gate) | ☐ |

---

## Group V — ย้อนสถานะ / void + completed read-only (OV-06)

### TC-V01 — ย้อนสถานะ (void) ที่ อยู่ระหว่างจัดส่ง + reason → revert รอจัดส่ง (happy — AC-33 / EC-12)
- group: V · ความสำคัญ: สูง · trace: AC-33 / EC-12 / BR-CBM-04
- Setup: seed=default (CBM-0000007 อยู่ระหว่างจัดส่ง) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000007`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ย้อนสถานะ** | — | modal/ช่องเหตุผลปรากฏ + ปุ่ม **ยืนยันย้อนสถานะ** | ☐ |
| 2 | TYPE "รถเสียกลางทาง ต้องจัดคิวใหม่" → CLICK **ยืนยันย้อนสถานะ** → WAIT | — | toast **ย้อนสถานะแล้ว** · combined กลับ **รอจัดส่ง** (revert + clear dispatch_started_*) | ☐ |

### TC-V02 — ย้อนสถานะ ไม่ใส่เหตุผล → block (negative — VR-03)
- group: V · ความสำคัญ: สูง · trace: VR-03 / BR-CBM-04
- Setup: seed=default (CBM-0000007 อยู่ระหว่างจัดส่ง) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000007` → CLICK **ย้อนสถานะ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยืนยันย้อนสถานะ** โดยไม่กรอกเหตุผล | — | block + **กรุณาระบุเหตุผล** — สถานะไม่เปลี่ยน | ☐ |

### TC-V03 — completed → read-only (AC-34 / EC-13 / BR-CBM-06)
- group: V · ความสำคัญ: สูง · trace: AC-34 / EC-13 / BR-CBM-06
- Setup: seed=default (CBM-0000010 เสร็จสิ้น 🔒) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000010`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY drawer CBM-0000010 | — | combined **เสร็จสิ้น** 🔒 · **ไม่มี** ปุ่มแก้/อนุมัติ/ย้อนสถานะ/action ใด ๆ (read-only) | ☐ |
| 2 | VERIFY list แถว CBM-0000010 คอลัมน์ | — | ไม่มีปุ่ม action ในแถว (lock) | ☐ |

### TC-V04 — void confirm ต้องกด "ยืนยันย้อนสถานะ" (AC-33)
- group: V · ความสำคัญ: กลาง · trace: AC-33 / confirm gate
- Setup: seed=default (CBM-0000007 อยู่ระหว่างจัดส่ง) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000007` → CLICK **ย้อนสถานะ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE เหตุผล → CLICK **ปิด** (ไม่กด ยืนยัน) | — | ไม่ย้อนสถานะ · combined ยัง **อยู่ระหว่างจัดส่ง** (ต้องกด ยืนยันย้อนสถานะ เท่านั้นจึง commit) | ☐ |

---

## Group Q — ค้นหา + export (OV-07)

### TC-Q01 — ค้นหา booking/farmer/ทะเบียนรถ (happy — AC-35)
- group: Q · ความสำคัญ: สูง · trace: AC-35
- Setup: seed=default · files=—
- Start: OPEN `#/bookings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "CBM-2568-0000005" → ช่องค้นหา | เลขจอง | เหลือ 1 แถว CBM-2568-0000005 (สมชาย ไร่ทอง · รอตัด) | ☐ |
| 2 | CLICK **ล้างตัวกรอง** → TYPE "ประเสริฐ" | ชื่อเกษตรกร | เหลือแถวของ ประเสริฐ ใจดี (CBM-0000003, 0000007, 0000010 — QUO-2568-0003) | ☐ |
| 3 | CLICK **ล้างตัวกรอง** → TYPE "70-8890" | ทะเบียนรถ | เหลือ 1 แถว CBM-2568-0000005 (รถ 10 ล้อ 70-8890 กจ) | ☐ |

### TC-Q02 — ค้นไม่พบ → "ไม่พบรายการที่ค้นหา" (edge — AC-35)
- group: Q · ความสำคัญ: กลาง · trace: AC-35 / empty state
- Setup: seed=default · files=—
- Start: OPEN `#/bookings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ไม่มีการจองนี้แน่นอน" → ช่องค้นหา | — | ตารางว่าง + empty state **ไม่พบรายการที่ค้นหา** + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 2 | CLICK **ล้างตัวกรอง** | — | กลับ 10 รายการ | ☐ |

### TC-Q03 — Export CSV แสดง "-" ตามจอ (AC-36) (ต้อง simulate)
- group: Q · ความสำคัญ: กลาง · trace: AC-36 · **prototype: ไฟล์ CSV จริง = server-side — mark BLOCKED บน prototype**
- Setup: **simulate — ระบบจริง**
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): Export CSV | — | ไฟล์ CSV คอลัมน์ตรงตาราง · แกนที่ยังไม่เริ่มแสดงค่า **-** (ตรงกับจอ) | ☐ |

---

## Group X — Cross-module / event XT-01..05 + system simulate (06_TESTS §6.9) ⭐

### TC-X01 — สร้าง booking → snapshot farmer + season ตรง (XT-01) ★
- group: X · ความสำคัญ: สูงสุด · trace: XT-01 / AC-01 / source ไม่ถูกแก้
- Setup: seed=default · files=—
- Start: OPEN `#/bookings` → CLICK **สร้างการจอง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก **QUO-2568-0001 · สมชาย ไร่ทอง** → กรอกฟิลด์ครบ → CLICK **ยืนยันสร้าง** → WAIT | — | toast **สร้างการจองสำเร็จ — [เลขจอง]** · แถวใหม่ farmer snapshot = สมชาย ไร่ทอง (ตรงต้นทาง Quota) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): เปิด Quota record ก่อน/หลังผูก | — | Quota/Season **ไม่มี field เปลี่ยน** (read-only GET only · no write-back) | ☐ |

### TC-X02 — Debt outstanding อ่านจาก Debt Mgt (XT-02)
- group: X · ความสำคัญ: สูง · trace: XT-02 / AC-04 / BR-CBM-05
- Setup: seed=default · files=—
- Start: OPEN `#/bookings` → CLICK **สร้างการจอง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก QUO-2568-0001 | — | ยอดหนี้ค้าง **125,000** | ☐ |
| 2 | เลือก QUO-2568-0003 | — | ยอดหนี้ค้าง **48,000** | ☐ |
| 3 | เลือก QUO-2568-0002 / QUO-2568-0004 | — | **ไม่มีแฟ้มลูกหนี้** (null · ไม่มี record) | ☐ |
| 4 | VERIFY (ระบบจริง — SIT): reconcile ยอดกับ Debt Mgt | — | ยอดตรงกับระบบลูกหนี้จริง (prototype = mock const) | ☐ |

### TC-X03 — receiving-completed event → ปิดแกน B + รอทำจ่าย (XT-03)
- group: X · ความสำคัญ: สูงสุด · trace: XT-03 / AC-17 / EC-06 / idempotent
- Setup: seed=default (CBM-0000008 รอผลการเท 🔒) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000008`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **จำลอง: รับอ้อยเสร็จ** → WAIT | — | combined = **รอทำจ่าย** 🔒 · closed_at set (ปิดแกน B) · payment=awaiting_payment | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): event มาจากระบบรับอ้อย | — | event ปิดแกน B + สร้างคำขอจ่าย (idempotent · event_id เดียวกันไม่ทำซ้ำ) | ☐ |

### TC-X04 — payment-completed event → เสร็จสิ้น + lock (XT-04)
- group: X · ความสำคัญ: สูงสุด · trace: XT-04 / AC-19 / EC-08 / BR-CBM-06
- Setup: seed=default (CBM-0000009 รอทำจ่าย 🔒) · files=—
- Start: OPEN `#/bookings/CBM-2568-0000009`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **จำลอง: จ่ายเงินเสร็จ** → WAIT | — | combined = **เสร็จสิ้น** 🔒 · lock (read-only) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): event มาจากระบบการเงิน | — | payment-completed → completed + lock (idempotent) | ☐ |

### TC-X05 — event ซ้ำ (event_id เดิม) → 409/no-op (XT-05 / EC-09) (ต้อง simulate)
- group: X · ความสำคัญ: สูง · trace: XT-05 / EC-09 / BR-CBM-03 · **prototype single-session ไม่ยิง event ซ้ำจริงได้ — SIT**
- Setup: **simulate — ระบบจริง:** ยิง receiving-completed/payment-completed ด้วย event_id เดิม 2 ครั้ง
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): POST event ซ้ำ event_id เดิม | — | 409 **รายการซ้ำ (idempotent)** หรือ no-op — ผลไม่ซ้ำ (ไม่สร้างคำขอจ่าย/ไม่ complete ซ้ำ) | ☐ |

### TC-X06 — Optimistic lock stale → 409 (EC-16) (ต้อง simulate)
- group: X · ความสำคัญ: สูง · trace: EC-16 / BR-CBM-03 · **prototype single-session ทำไม่ได้ — SIT**
- Setup: **simulate — ระบบจริง:** 2 sessions — A แก้/transition ก่อน · B commit ด้วย row_version เก่า
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): B commit หลัง A เปลี่ยนสถานะไปแล้ว | — | 409 + **ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรช** — ของ A ไม่ถูกทับ | ☐ |

### TC-X07 — RBAC deny + SoD (OQ-CB4) (ต้อง simulate)
- group: X · ความสำคัญ: กลาง · trace: §5.3 permission / SoD · **prototype ไม่มี role switching (user เดียวกดได้ทุก action) — mark BLOCKED บน prototype**
- Setup: **simulate — ระบบจริง:** RBAC + SoD flag
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง — RBAC): user ไม่มีสิทธิ์ approve/void | — | ปุ่มถูกซ่อน · ถ้ายิง API → 403 **ไม่มีสิทธิ์ดำเนินการ** | ☐ |
| 2 | VERIFY (ระบบจริง — SoD flag ON): ผู้สร้างอนุมัติเอง | — | block (ผู้สร้างไม่ควรอนุมัติเอง) · flag OFF → ผ่านแต่ log anomaly | ☐ |

### TC-X08 — no write-back ยืนยัน source read-only (XT-01/02)
- group: X · ความสำคัญ: กลาง · trace: XT-01, XT-02 / §0.14 no write-back
- Setup: seed=default · files=—
- Start: OPEN `#/bookings` → CLICK **สร้างการจอง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก QUO-2568-0001 สร้าง 2 การจอง (1 quota : N bookings) | — | สร้างได้ทั้ง 2 (ไม่ขึ้น "ถูกใช้แล้ว" · Quota ไม่ถูก mutate · ไม่มี has_booking flag) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT) | — | เปิด Quota/Debt record ก่อน/หลัง = ไม่มี field เปลี่ยน (read-only GET only) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `cane-booking-management.html` ใน browser (desktop ≥1280px) — รอ ~2s ให้ font/icon โหลด
2. **ทุกเคสเริ่มด้วย refresh (F5)** แล้ว OPEN route ตาม `Start:` — mock เป็น in-memory, refresh = reset seed 10 การจอง + 4 โควตา (ทำให้เคส independent)
3. ทำตาม step ตามลำดับ — Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SELECT/PRESS/WAIT/VERIFY)
4. `WAIT` = รอ ≤3s จนสิ่งที่ Expected ระบุปรากฏ (toast มุมขวาล่าง · action/event ~0.6-0.9s · toast แสดง 4-4.8s)
5. **3-AXIS state machine:** ทุก transition แกน B เดินตามลำดับ no-skip (รอส่งอนุมัติตัด → รออนุมัติตัด → รอตัด → รอจัดส่ง → อยู่ระหว่างจัดส่ง) · แกน A ต้อง verified ก่อน Gate B เปิด · แกน C เริ่มหลัง B closed
6. **สถานะระบบ 3 ขั้นท้าย (รอผลการเท/รอทำจ่าย/เสร็จสิ้น) 🔒** เข้าถึงได้เฉพาะปุ่ม `จำลอง:` เท่านั้น — manual set ไม่ได้ (block VR-05)
7. step ไหน Expected ไม่ตรง = FAIL เคสนั้น → บันทึก `failed_step` + `evidence` แล้วไปเคสถัดไป
8. เคส `(ต้อง simulate)` — ถ้ารันบน prototype ทำไม่ได้ ให้ status = `blocked` + note "SIT case"

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Stories/AC (06_TESTS §6.1) | 35 / 35 (AC-01..31, 33..36 · AC-32 ไม่มีใน FRD) |
| Cross-Module / Event (XT-01..05) | 5 / 5 (XT-05 event ซ้ำ = simulate) |
| Business rules (BR-CBM-01..10) | 10 / 10 |
| Validation (VR-01..06) | 6 / 6 |
| Edge cases (EC-01..16) | 16 / 16 (EC-07/09/16 = simulate) |
| Error catalog (UI-observable) | ครบ · 409 stale/dup + 403 FORBIDDEN = simulate |
| Permission cells | CBM.Approver/Cut/Dispatch allow ครบ · RBAC deny / SoD = TC-X07 (simulate) |
| State machine (A/B/C + combined 10-step + 🔒) | ครบทุกแกน + system-controlled |

- **Manifest cross-check (FRD §0.12): ✅ 35 AC + 5 XT + 10 BR + 6 VR + 16 EC — ทุกแถวมีคู่ใน Ledger**

### เคส (ต้อง simulate) / SIT (7 เคส)
- TC-E05 (receiving สำเร็จ แต่สร้างคำขอจ่ายล้ม — fault injection)
- TC-P05 (bulk download ZIP — server-side)
- TC-Q03 (export CSV — server-side)
- TC-X05 (event ซ้ำ idempotency 409/no-op)
- TC-X06 (optimistic lock stale 409 — single session)
- TC-X07 (RBAC deny / SoD — ไม่มี role switching)
- (X01/X02/X03/X04 มี step (ระบบจริง — SIT) reconcile ควบด้วย)

## Result Report (schema)

```json
{
  "feature_id": "F-AGM-007",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 54, "pass": 0, "fail": 0, "blocked": 0 }
}
```
