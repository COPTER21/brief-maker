# 06_TESTS — F-AGM-008 Debt Management

> Audience: QA + ai-testcase-md-generator · microcopy-aware · ledger/allocation heavy

## §6.1 Acceptance Criteria

### List (US-01)
- **AC-01** list แสดงลูกหนี้ + 4 stats (ลูกหนี้ทั้งหมด/ยอดคงค้างรวม/เกินกำหนด/ตัดหนี้สูญ)
- **AC-02** ค้นหา (โควตา/ชื่อ/เลขลูกหนี้) · กรอง สถานะ + Aging
- **AC-03** คอลัมน์ครบ (ID/โควตา/ชื่อ/ยอดคงค้าง/ภาระ#/Aging pill/สถานะ pill/อัปเดต/การกระทำ) · ยอดติดลบ = แดง
- **AC-04** ส่งออก CSV "เริ่มส่งออกรายงานแล้ว" · รายงาน Aging "กำลังสร้างรายงานอายุหนี้..."
- **AC-05** empty filter → "ไม่พบลูกหนี้" + สร้างลูกหนี้ใหม่

### Debtor Create (US-02)
- **AC-06** ค้นโควตา ว่าง → "กรุณากรอกรหัสโควตา"
- **AC-07** ค้นโควตาที่มีลูกหนี้แล้ว → "มีลูกหนี้อยู่แล้ว" + navigate detail (BR-01)
- **AC-08** ค้นโควตาใหม่ → "พบข้อมูลโควตา" + preview + auto-fill ชื่อ/เบอร์
- **AC-09** สร้าง โดยไม่มีชื่อ → "กรุณากรอกชื่อเกษตรกร"
- **AC-10** สร้างสำเร็จ → "สร้างลูกหนี้สำเร็จ" → detail

### Debtor Detail (US-03)
- **AC-11** header (ชื่อ+id+status) + quick stats 4 (คงค้าง/ภาระ/aging/อัปเดต)
- **AC-12** 5 แท็บ (ภาพรวม/ภาระหนี้ N/บัญชีสมุด N/เอกสาร/การตั้งค่า)
- **AC-13** แท็บภาระหนี้: table + source badge (สัญญา🔒 น้ำเงิน/แมนนวล/ปรับปรุง) + ปุ่ม ดู/แก้ไข/ตัดหนี้
- **AC-14** แท็บบัญชีสมุด: double-entry (เดบิต/เครดิต/คงเหลือ) + kind badge + ส่งออก Statement
- **AC-15** แท็บการตั้งค่า: ค่าเริ่มต้น (ดอก 5.00/ค่าปรับ 2.00/simple_daily_365/percent_of_net_proceeds)

### Obligation Create (US-04)
- **AC-16** source=สัญญา ไม่ใส่ contract_id → "กรุณาระบุรหัสสัญญาเมื่อแหล่งที่มาเป็น \"จากสัญญา\""
- **AC-17** source=ปรับปรุง ไม่เลือกชนิด → "กรุณาเลือกชนิดการปรับปรุง"
- **AC-18** source=ปรับปรุง ไม่อ้างอิง → "การปรับปรุงต้องอ้างอิงรายการเดิม (ภาระหนี้หรือรายการสมุดบัญชี)"
- **AC-19** type=อื่นๆ ไม่ใส่ desc → "กรุณากรอกรายละเอียดประเภทอื่นๆ"
- **AC-20** ต้นทุน ≤ 0 → "จำนวนต้นทุนต้องมากกว่า 0"
- **AC-21** disbursement > start_interest → "วันที่เบิกต้องไม่เกินวันเริ่มคิดดอกเบี้ย"
- **AC-22** start_interest > maturity → "วันเริ่มคิดดอกเบี้ยต้องไม่เกินวันครบกำหนด"
- **AC-23** บันทึกสำเร็จ → "บันทึกภาระหนี้สำเร็จ"

### Manual Payment (US-05) ⭐
- **AC-24** จำนวน ≤ 0 → "กรุณากรอกจำนวนเงินที่ถูกต้อง"
- **AC-25** กด ตรวจสอบการจัดสรร → allocation preview (ดอกเบี้ย→ค่าปรับ→ต้นทุน ตาม priority) + "ตรวจสอบการจัดสรรเรียบร้อย"
- **AC-26** allocation waterfall ถูกต้อง (interest ก่อน penalty ก่อน principal · เรียง priority)
- **AC-27** จัดสรรไม่หมด → "เหลือ: X ฿"
- **AC-28** save โดยไม่ validate → "กรุณาตรวจสอบการจัดสรรก่อน"
- **AC-29** save โดยไม่มีเลขอ้างอิง → "กรุณากรอกเลขอ้างอิง"
- **AC-30** save สำเร็จ → "บันทึกการชำระเรียบร้อย" + ledger(payment)

### Write-off (US-06) ⭐
- **AC-31** ไม่ติ๊ก confirm → "กรุณายืนยันการตัดหนี้"
- **AC-32** ไม่ใส่เหตุผล → "กรุณากรอกเหตุผลการตัดหนี้"
- **AC-33** amount > outstanding → inline "จำนวนเกินยอดคงเหลือ"
- **AC-34** amount > 100,000 → "จำนวนเกินขีดจำกัด - ต้องการอนุมัติจากผู้จัดการ" (DOA)
- **AC-35** ตัดสำเร็จ (≤DOA) → "ตัดหนี้เรียบร้อย" + ledger(write_off) + status→ตัดหนี้สูญ

### Ledger / Cross-module (US-07/09)
- **AC-36** export statement → "สร้างเอกสารเรียบร้อย"

## §6.9 Cross-Module / Event Test Cases ⭐
| XT | Scenario | Source | Expected |
|---|---|---|---|
| XT-01 | สร้างลูกหนี้ | Quota (read) | snapshot farmer/quota verified |
| XT-02 | obligation source=contract | Contract (read) | contract_id + 🔒 locked · แก้ไม่ได้ (423) |
| XT-03 | outstanding อ่านโดย CBM | → CBM (F-AGM-007) | debtor_outstanding ตรง Σ obligation |
| XT-04 | write-off > DOA | Manager approval | PENDING_APPROVAL (idempotent) |
| XT-05 | adjustment reverse | append ledger | ledger reverse + status reversed (append-only, ไม่แก้ของเดิม) |

## §6.10 Microcopy-Aware Expected (verbatim)
| จุด | ข้อความ |
|---|---|
| ปุ่ม list | `สร้างลูกหนี้` · `ส่งออก CSV` · `รายงาน Aging` |
| ปุ่ม detail | `บันทึกการชำระ` · `สร้างภาระหนี้` · `ส่งออก Statement` · `ตัดหนี้` |
| tabs | `ภาพรวม` · `ภาระหนี้` · `บัญชีสมุด` · `เอกสาร` · `การตั้งค่า` |
| source badge | `สัญญา` (🔒) · `แมนนวล` · `ปรับปรุง` |
| status | `ใช้งาน` · `ระงับ` · `ปิด` · `ตัดหนี้สูญ` · `ย้อนรายการ` |
| aging | `0-30` · `31-60` · `61-90` · `90+` |
| ledger kind | `ตั้งหนี้` · `ดอกเบี้ย` · `ค่าปรับ` · `ชำระ` · `ปรับปรุง` · `ตัดหนี้สูญ` · `ย้อนรายการ` |
| payment | `บันทึกการชำระเงิน` · `ตรวจสอบการจัดสรร` · `ตรวจสอบการจัดสรรเรียบร้อย` · `บันทึกการชำระเรียบร้อย` · วิธี `เงินสด`/`โอนเงิน`/`หักกลบ` |
| allocation types | `ดอกเบี้ย` · `ค่าปรับ` · `ต้นทุน` |
| write-off | `ตัดหนี้สูญ` · `ยืนยันตัดหนี้` · `ตัดหนี้เรียบร้อย` |
| toast create | `พบข้อมูลโควตา` · `มีลูกหนี้อยู่แล้ว` · `สร้างลูกหนี้สำเร็จ` · `บันทึกภาระหนี้สำเร็จ` |
| errors | ตาม §5.4 (verbatim) |

## §6.8 Trace: AC → Logic
| AC | API | FN |
|---|---|---|
| AC-01..05 | API-01/05/06 | FN-03,AGING |
| AC-06..10 | API-04/02 | FN-01,02 |
| AC-11..15 | API-03/LED1 | FN-03,LED |
| AC-16..23 | API-OB1 | FN-OB,11 |
| AC-24..30 | API-PAY1/PAY2 | FN-ALLOC,PAY,LED |
| AC-31..35 | API-WO1 | FN-WO,11,LED |
| AC-36 | API-LED2 | FN-LED,ENG-DOC |
> Coverage FN + FN-11 guard + FN-LED ledger ✅ · XT-01..05 ✅

## §6.6 Performance
list p95<3s · action<1s · allocation deterministic · ledger append-only+immutable · statement ไทย · optimistic lock
