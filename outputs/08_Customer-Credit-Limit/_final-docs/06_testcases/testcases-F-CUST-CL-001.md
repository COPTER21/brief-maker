# AI Test Cases — Customer Credit Limit

ชุดทดสอบสำหรับ AI agent ที่อ้างอิง HTML prototype, BRD และ FRD Pack โดยตรง ทุกข้อความบนจอและเส้นทางอ้างจาก prototype ที่อนุมัติแล้ว

## Meta

| รายการ | ค่า |
|---|---|
| Feature ID | F-CUST-CL-001 |
| ชื่อ | Customer Credit Limit |
| App entry | `#/credit-limits` |
| Sources | BRD v1.0, FRD Pack v1.0, `01_HTML/f-credit-limit.html` |
| จำนวน | 26 เคส: list 4, คำขอ/DOA 8, อนุมัติ 5, hold/review 4, ข้อมูลเครดิต 3, integration/security 2 |

## Coverage

| กลุ่ม | เคส | ความสำคัญ |
|---|---:|---|
| รายการและการค้นหา | 4 | สูง/กลาง |
| คำขอปรับวงเงินและสายอนุมัติ | 8 | สูง |
| การอนุมัติและไม่อนุมัติ | 5 | สูง |
| ระงับ/ปลดระงับ/ทบทวน | 4 | สูง/กลาง |
| ยอดเครดิตและข้อมูล AR | 3 | สูง/กลาง |
| สัญญาเชื่อมต่อและความปลอดภัย | 2 | สูง |

## Coverage Ledger

### Acceptance / Function
| item | cases |
|---|---|
| AT-01, FN-01, FN-06 | TC-CL-05..07 |
| AT-02, FN-02, FN-09 | TC-CL-10, TC-CL-11 |
| AT-03, FN-03 | TC-CL-08 |
| AT-04, FN-04, FN-07 | TC-CL-05, TC-CL-09 |
| AT-05 | TC-CL-07 |
| AT-06 | TC-CL-06 |
| AT-07, FN-11 | TC-CL-13 |
| AT-08, FN-12, FN-13 | TC-CL-15, TC-CL-16 |
| AT-09, FN-14 | TC-CL-17 |
| AT-10, FN-91 | TC-CL-14, TC-CL-17 |
| AT-11, FN-15 | TC-CL-18 |
| AT-12, FN-16, FN-20 | TC-CL-19, TC-CL-20 |
| AT-13, FN-17 | TC-CL-21 |
| AT-14, FN-18 | TC-CL-12 |
| AT-15, FN-19 | TC-CL-25 |
| AT-16 | TC-CL-23 |
| AT-17 | TC-CL-09 |
| AT-18 | TC-CL-24 |
| AT-19, FN-92 | TC-CL-04 |
| AT-20, FN-21 | TC-CL-01..03 |

### Rules / errors / edge cases
| item | cases |
|---|---|
| BR-01..04, BR-DOA-01..05 | TC-CL-05, TC-CL-08..13 |
| BR-05, DOA_NO_AMOUNT_TIER, EC-02 | TC-CL-07 |
| BR-06, REQUEST_AMOUNT_UNCHANGED, REASON_REQUIRED, EC-01, EC-06 | TC-CL-06, TC-CL-13, TC-CL-15 |
| BR-07..08, EC-08 | TC-CL-18..21 |
| BR-09, EC-07 | TC-CL-15 |
| BR-10 | TC-CL-14, TC-CL-17 |
| BR-11, PROFILE_ALREADY_EXISTS | TC-CL-25 |
| BR-12..13 | TC-CL-12, TC-CL-22 |
| SELF_APPROVAL_FORBIDDEN, APPROVAL_STEP_MISMATCH, EC-03 | TC-CL-23 |
| REQUEST_NOT_DRAFT, EC-05 | TC-CL-24 |
| EC-04 | TC-CL-09 |

### Cross-module / scope locks
| item | cases |
|---|---|
| XT-01 Customer Master | TC-CL-25 |
| XT-02 DOA | TC-CL-07 |
| XT-03 My Profile / SoD | TC-CL-23 |
| XT-04 SO/AR projection | TC-CL-21 |
| XT-05 approved projection | TC-CL-11, TC-CL-15 |
| LOCK-CL-01..05 | TC-CL-05, TC-CL-09, TC-CL-12, TC-CL-22, TC-CL-25 |

## Data Sets

| ชุด | ฟิลด์ | ค่า |
|---|---|---|
| A | ลูกค้าเงินสด | ลูกค้าที่วงเงินปัจจุบัน 0 บาท และไม่ระงับ |
| A | วงเงินที่ขอ | 100,000 บาท |
| A | เหตุผล | เปิดเครดิตตามข้อตกลงการค้า |
| B | ลูกค้าเครดิต | ลูกค้าที่มีวงเงินปัจจุบันและไม่ระงับ |
| B | วงเงินเพิ่ม | สูงกว่าวงเงินปัจจุบัน 100,000 บาท |
| B | วงเงินลด | ต่ำกว่าวงเงินปัจจุบัน 100,000 บาท |
| C | เหตุผลระงับ | มียอดค้างเกินกำหนดตามนโยบาย |
| D | เหตุผลไม่อนุมัติ | ประวัติชำระล่าช้า |

## Test Cases

### รายการและการค้นหา

### TC-CL-01 — ค้นหารายการต่อเนื่องโดยไม่เสียโฟกัส (happy)
- group: รายการ · ความสำคัญ: สูง · trace: AT-20 / FN-21
- actor: Credit Officer
- Setup: role=credit_officer · seed=มีลูกค้าอย่างน้อย 2 ราย · files=—
- Start: OPEN `#/credit-limits`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ค้นหาได้ต่อเนื่องและเคอร์เซอร์ยังอยู่ในช่องค้นหา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/credit-limits` | — | เห็นหัวข้อ **วงเงินเครดิตลูกค้า** และช่อง **ค้นหา รหัส / ชื่อลูกค้า / พนักงานขาย** | ☐ |
| 2 | TYPE `ก` → ช่องค้นหา | ก | ตารางกรองตามคำค้น และเคอร์เซอร์ยังอยู่ในช่องเดิม | ☐ |
| 3 | TYPE `ท` → ช่องค้นหา | ท | คำค้นเป็น `กท` และตารางกรองต่อเนื่องโดยไม่หลุดโฟกัส | ☐ |

### TC-CL-02 — กรองสถานะและความเสี่ยง แล้วล้างตัวกรอง (happy)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-21
- actor: Credit Officer
- Setup: role=credit_officer · seed=มีลูกค้าหลายสถานะ/ความเสี่ยง · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: ตัวกรองจำกัดรายการตามที่เลือกและล้างกลับได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT **รออนุมัติ** → ตัวกรองสถานะ | — | เห็นเฉพาะรายการที่มีป้าย **รออนุมัติ** | ☐ |
| 2 | SELECT **ความเสี่ยงสูง** → ตัวกรองความเสี่ยง | — | เหลือเฉพาะรายการที่ตรงทั้งสองเงื่อนไข หรือเห็นข้อความว่าไม่พบรายการ | ☐ |
| 3 | CLICK ปุ่ม **ล้างตัวกรอง** | — | ตัวกรองกลับเป็นทุกสถานะและทุกระดับความเสี่ยง | ☐ |

### TC-CL-03 — เรียงข้อมูลและผลลัพธ์ว่าง (edge)
- group: รายการ · ความสำคัญ: กลาง · trace: FN-21
- actor: Credit Officer
- Setup: role=credit_officer · seed=มีลูกค้าอย่างน้อย 2 ราย · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: หัวตารางเรียงได้ และคำค้นที่ไม่พบแสดงผลว่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวตาราง **วงเงิน** | — | สัญลักษณ์เรียงลำดับของหัวข้อวงเงินเปลี่ยน และลำดับแถวเปลี่ยนตาม | ☐ |
| 2 | TYPE `ไม่มีชื่อนี้แน่นอน` → ช่องค้นหา | — | เห็นสถานะว่างแทนตารางข้อมูล | ☐ |

### TC-CL-04 — ปิดหน้าต่างตามลำดับ Esc (edge)
- group: รายการ · ความสำคัญ: สูง · trace: AT-19 / FN-92
- actor: Credit Officer
- Setup: role=credit_officer · seed=มีลูกค้าที่เปิดรายละเอียดได้ · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: Esc ปิด modal ก่อน change drawer ก่อน detail drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวลูกค้าหนึ่งรายการ | — | Detail drawer เปิดขึ้น | ☐ |
| 2 | CLICK ปุ่ม **ปรับวงเงิน** | — | Change drawer เปิดขึ้น | ☐ |
| 3 | PRESS Esc | — | Change drawer ปิดและกลับสู่ Detail drawer | ☐ |
| 4 | PRESS Esc | — | Detail drawer ปิดและกลับสู่หน้ารายการ | ☐ |

### คำขอปรับวงเงินและสายอนุมัติ

### TC-CL-05 — สร้างคำขอตั้งวงเงินและส่งอนุมัติ (happy)
- group: คำขอ · ความสำคัญ: สูง · trace: AT-01, AT-04 / BR-01..04
- actor: Credit Officer
- Setup: role=credit_officer · seed=ลูกค้าชุด A · files=—
- Start: OPEN `#/credit-limits`
- ชุดข้อมูล: A
- ผ่านเมื่อ: คำขออยู่สถานะ **รอส่งอนุมัติ** ก่อนกดส่ง และเปลี่ยนเป็น **รออนุมัติ** หลังส่ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวลูกค้าชุด A แล้ว CLICK **ปรับวงเงิน** | — | เห็นช่อง **วงเงินที่ขอ** และ **เหตุผล** พร้อมส่วน **สายอนุมัติที่จะใช้ (DOA)** | ☐ |
| 2 | TYPE `100,000` → ช่อง **วงเงินที่ขอ** | A | เห็นวงเงินที่กรอก และมีตัวอย่างสายอนุมัติจาก DOA | ☐ |
| 3 | TYPE เหตุผล → ช่อง **เหตุผล** | A | ปุ่ม **บันทึกคำขอ** เปลี่ยนเป็นกดได้ | ☐ |
| 4 | CLICK ปุ่ม **บันทึกคำขอ** | — | เห็นข้อความ **บันทึกคำขอแล้ว — พร้อมส่งอนุมัติ** และสถานะ **รอส่งอนุมัติ** | ☐ |
| 5 | CLICK ปุ่ม **ส่งอนุมัติ** | — | เห็นข้อความ **ส่งอนุมัติแล้ว — รออนุมัติขั้น 1** และสถานะ **รออนุมัติ** | ☐ |

### TC-CL-06 — ปุ่มบันทึกคำขอปิดเมื่อข้อมูลไม่ครบหรือจำนวนเท่าเดิม (negative)
- group: คำขอ · ความสำคัญ: สูง · trace: AT-06 / REQUEST_AMOUNT_UNCHANGED, REASON_REQUIRED, EC-01
- actor: Credit Officer
- Setup: role=credit_officer · seed=ลูกค้าชุด B · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: ปุ่ม **บันทึกคำขอ** แสดงแบบ disabled อย่างชัดเจนจนข้อมูลถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวลูกค้าชุด B แล้ว CLICK **ปรับวงเงิน** | — | Change drawer เปิด | ☐ |
| 2 | VERIFY ปุ่ม **บันทึกคำขอ** | — | ปุ่มแสดงสีและสถานะ disabled ก่อนกรอกข้อมูล | ☐ |
| 3 | TYPE วงเงินเดิม → ช่อง **วงเงินที่ขอ** | วงเงินปัจจุบัน | ปุ่มยัง disabled แม้กรอกเหตุผล | ☐ |
| 4 | TYPE วงเงินใหม่แต่เว้นเหตุผล | B | ปุ่มยัง disabled | ☐ |

### TC-CL-07 — DOA ไม่พบช่วงวงเงินต้องห้ามส่ง (negative)
- group: คำขอ · ความสำคัญ: สูง · trace: AT-05 / BR-05, DOA_NO_AMOUNT_TIER, XT-02
- actor: Credit Officer
- Setup: role=credit_officer · seed=วงเงินที่ขออยู่นอกช่วงที่ตั้งไว้ใน DOA · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: ไม่มีคำขอเข้าสถานะรออนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/credit-limits` แล้ว CLICK **ปรับวงเงิน** | — | Change drawer เปิด | ☐ |
| 2 | TYPE วงเงินนอกช่วง → ช่อง **วงเงินที่ขอ** | ตาม setup | ส่วนสายอนุมัติแจ้งว่าไม่พบช่วงวงเงินที่ตั้งไว้ | ☐ |
| 3 | TYPE เหตุผล → ช่อง **เหตุผล** | A | ปุ่ม **บันทึกคำขอ** ยัง disabled และไม่สามารถส่งอนุมัติได้ | ☐ |

### TC-CL-08 — ปรับเพิ่มและปรับลดใช้กระบวนการเดียวกัน (happy)
- group: คำขอ · ความสำคัญ: สูง · trace: AT-03 / BR-01
- actor: Credit Officer
- Setup: role=credit_officer · seed=ลูกค้าชุด B · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: ทั้งวงเงินสูงขึ้นและต่ำลงสร้างคำขอได้ ไม่แก้วงเงินจริงทันที

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE วงเงินเพิ่ม → ช่อง **วงเงินที่ขอ** | B | เห็นสายอนุมัติที่ใช้กับวงเงินใหม่ | ☐ |
| 2 | CLICK **บันทึกคำขอ** | — | วงเงินจริงบนรายละเอียดเดิมยังไม่เปลี่ยน และมีคำขอรอส่ง | ☐ |
| 3 | CLICK **ปรับวงเงิน** แล้ว TYPE วงเงินลด | B | ระบบยอมรับจำนวนที่ต่ำกว่าวงเงินเดิมเมื่อมีเหตุผล | ☐ |

### TC-CL-09 — สายอนุมัติถูกเก็บตามคำขอเดิม (ต้อง simulate)
- group: คำขอ · ความสำคัญ: สูง · trace: AT-04, AT-17 / BR-DOA-02, EC-04
- actor: Administrator
- Setup: role=administrator · seed=มีคำขอที่ส่งแล้วและผู้ดูแลเปลี่ยนการตั้งค่าสายอนุมัติกลางได้ · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: คำขอที่ส่งแล้วแสดงขั้นอนุมัติเดิม ไม่เปลี่ยนตามการตั้งค่าใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แท็บ **คำขอ & อนุมัติ** ของคำขอที่ส่งแล้ว | — | เห็นลำดับขั้นอนุมัติ ชื่อผู้อนุมัติ ตำแหน่ง และสถานะเดิม | ☐ |
| 2 | VERIFY หลังเปลี่ยนการตั้งค่าสายอนุมัติกลาง (ต้อง simulate) | — | ลำดับในคำขอเดิมยังเท่าเดิม | ☐ |

### การอนุมัติและไม่อนุมัติ

### TC-CL-10 — อนุมัติขั้นกลางโดยยังไม่เปลี่ยนวงเงินจริง (happy)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AT-02 / BR-02
- actor: DOA Approver
- Setup: role=current_doa_approver · seed=คำขอมีอย่างน้อย 2 ขั้นและอยู่ที่ขั้นของผู้ทดสอบ · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: สถานะเดินไปขั้นถัดไป แต่วงเงินจริงคงค่าเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวคำขอ แล้ว CLICK แท็บ **คำขอ & อนุมัติ** | — | เห็นปุ่ม **อนุมัติขั้น** ของขั้นปัจจุบัน | ☐ |
| 2 | VERIFY+จดวงเงินจริงก่อนอนุมัติ | — | จดค่าวงเงินปัจจุบันไว้ใช้เทียบ | ☐ |
| 3 | CLICK ปุ่ม **อนุมัติขั้น** | — | เห็นข้อความ **อนุมัติแล้ว — ส่งต่อขั้น** | ☐ |
| 4 | VERIFY วงเงินจริง | — | วงเงินจริงเท่ากับค่าที่จดในขั้น 2 และสถานะรอขั้นถัดไป | ☐ |

### TC-CL-11 — อนุมัติขั้นสุดท้ายจึงเปลี่ยนวงเงินจริง (happy)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AT-02, XT-05 / BR-02
- actor: DOA Approver
- Setup: role=final_doa_approver · seed=คำขออยู่ขั้นสุดท้าย · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: วงเงินจริงเปลี่ยนเฉพาะเมื่ออนุมัติครบสาย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **คำขอ & อนุมัติ** | — | เห็นขั้นปัจจุบันเป็นขั้นสุดท้าย | ☐ |
| 2 | CLICK ปุ่ม **อนุมัติขั้น** | — | เห็นข้อความ **อนุมัติครบสาย — วงเงินใหม่** | ☐ |
| 3 | VERIFY ส่วนสรุปวงเงิน | — | วงเงินจริงเป็นจำนวนที่ขอ และไม่มีปุ่มแก้ไขคำขอเดิม | ☐ |

### TC-CL-12 — ทุกคนเห็นสถานะคำขอเดียวกัน (permission)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AT-14 / BR-12, LOCK-CL-04
- actor: ผู้มีสิทธิ์ดูเครดิต
- Setup: role=credit_viewer และ role=current_doa_approver · seed=คำขอ pending 1 รายการ · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: สถานะเดียวกันปรากฏแก่ทุกคน แต่ปุ่มอนุมัติเฉพาะผู้มีสิทธิ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ด้วยบัญชีผู้ดูเครดิต | — | เห็นสถานะ **รออนุมัติ** และ timeline เดียวกัน | ☐ |
| 2 | VERIFY ด้วยบัญชีผู้อนุมัติขั้นปัจจุบัน | — | เห็นสถานะเดียวกัน พร้อมปุ่ม **อนุมัติขั้น** และ **ไม่อนุมัติ** | ☐ |

### TC-CL-13 — ไม่อนุมัติต้องกรอกเหตุผล (negative)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AT-07 / BR-DOA-03, REASON_REQUIRED, EC-06
- actor: DOA Approver
- Setup: role=current_doa_approver · seed=คำขอ pending ของคนอื่น · files=—
- Start: OPEN `#/credit-limits`
- ชุดข้อมูล: D
- ผ่านเมื่อ: ยืนยันไม่อนุมัติไม่ได้หากว่าง และวงเงินจริงคงเดิมเมื่อไม่อนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ไม่อนุมัติ** | — | modal **ไม่อนุมัติคำขอปรับวงเงิน** เปิด | ☐ |
| 2 | VERIFY ปุ่ม **ยืนยันไม่อนุมัติ** | — | ปุ่ม disabled เมื่อยังไม่มีเหตุผล | ☐ |
| 3 | TYPE เหตุผล → ช่อง **เหตุผลที่ไม่อนุมัติ** | D | ปุ่มยืนยันเปลี่ยนเป็นกดได้ | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันไม่อนุมัติ** | — | เห็นข้อความ **บันทึกไม่อนุมัติแล้ว — วงเงินคงเดิม** | ☐ |

### TC-CL-14 — Timeline และประวัติแสดงผู้ทำ/เวลา (happy)
- group: อนุมัติ · ความสำคัญ: กลาง · trace: FN-08, FN-10, FN-91
- actor: Credit Officer
- Setup: role=credit_officer · seed=คำขอที่ผ่านอย่างน้อย 1 ขั้น · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: เห็นเครื่องหมายผ่าน ชื่อ ตำแหน่ง เวลา และเส้นไม่ทับไอคอน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **คำขอ & อนุมัติ** | — | เห็นหัวข้อ **สายอนุมัติ (DOA)** | ☐ |
| 2 | VERIFY ขั้นที่ผ่านแล้ว | — | เห็นไอคอนเครื่องหมายถูก ชื่อผู้อนุมัติ ตำแหน่ง และเวลา โดยเส้นเชื่อมหยุดระหว่างจุด | ☐ |
| 3 | CLICK แท็บ **ประวัติ** | — | เห็นรายการการบันทึกการส่งหรืออนุมัติ พร้อมผู้ทำและเวลา | ☐ |

### TC-CL-15 — ระงับเครดิตต้องมีเหตุผล (happy/negative)
- group: ระงับเครดิต · ความสำคัญ: สูง · trace: AT-08 / BR-06, BR-09, EC-07
- actor: Credit Officer
- Setup: role=credit_officer · seed=ลูกค้าที่ไม่ระงับ · files=—
- Start: OPEN `#/credit-limits`
- ชุดข้อมูล: C
- ผ่านเมื่อ: สถานะเป็น **ระงับเครดิต** หลังยืนยัน และมีประวัติการทำรายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวลูกค้า แล้ว CLICK **ระงับเครดิต** | — | modal **ระงับเครดิตลูกค้า** เปิด | ☐ |
| 2 | VERIFY ปุ่ม **ยืนยันระงับ** | — | ปุ่ม disabled เมื่อยังไม่มีเหตุผล | ☐ |
| 3 | TYPE เหตุผล → ช่อง **เหตุผล** | C | ปุ่มยืนยันเปลี่ยนเป็นกดได้ | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันระงับ** | — | เห็นข้อความ **ระงับเครดิตแล้ว** และป้าย **ระงับเครดิต** | ☐ |

### TC-CL-16 — ปลดระงับเครดิตต้องมีเหตุผล (happy)
- group: ระงับเครดิต · ความสำคัญ: สูง · trace: AT-08 / BR-06
- actor: Credit Officer
- Setup: role=credit_officer · seed=ลูกค้าที่สถานะระงับเครดิต · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: สถานะกลับเป็นปกติหลังระบุเหตุผล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวลูกค้าที่ระงับ แล้ว CLICK **ปลดระงับ** | — | modal **ปลดระงับเครดิต** เปิด | ☐ |
| 2 | TYPE เหตุผล → ช่อง **เหตุผล** | แก้ไขยอดค้างเรียบร้อย | ปุ่ม **ยืนยันปลดระงับ** กดได้ | ☐ |
| 3 | CLICK ปุ่ม **ยืนยันปลดระงับ** | — | เห็นข้อความ **ปลดระงับเครดิตแล้ว** และสถานะไม่ใช่ระงับเครดิต | ☐ |

### TC-CL-17 — ทบทวนเครดิตบันทึกเวลาและประวัติ (happy)
- group: ระงับเครดิต · ความสำคัญ: กลาง · trace: AT-09, AT-10 / BR-10
- actor: Credit Officer
- Setup: role=credit_officer · seed=ลูกค้า 1 รายการ · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: วันทบทวนล่าสุดและประวัติเปลี่ยนหลังคลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวลูกค้า | — | Detail drawer เปิด | ☐ |
| 2 | CLICK ปุ่ม **ทบทวน** | — | เห็นข้อความ **บันทึกการทบทวนเครดิตแล้ว** | ☐ |
| 3 | VERIFY ข้อมูล **ทบทวนล่าสุด** และแท็บ **ประวัติ** | — | วันทบทวนล่าสุดเป็นวันที่ทำรายการ และมีบรรทัดทบทวนเพิ่ม | ☐ |

### ยอดเครดิตและข้อมูล AR

### TC-CL-18 — คำนวณวงเงินใช้และวงเงินคงเหลือ (happy)
- group: ข้อมูลเครดิต · ความสำคัญ: สูง · trace: AT-11 / BR-07
- actor: Credit Officer
- Setup: role=credit_officer · seed=ลูกค้ามีวงเงินจริงและยอดค้างจากข้อมูล AR/SO · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: ยอดใช้และคงเหลือสอดคล้องกับยอดจาก AR/SO

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวลูกค้า | — | เห็นวงเงินจริง ยอดใช้ และวงเงินคงเหลือในส่วนสรุป | ☐ |
| 2 | VERIFY ค่าเครดิต | — | วงเงินคงเหลือเท่ากับวงเงินจริงลบยอดใช้ และยอดใช้ตรงกับข้อมูล AR/SO ล่าสุดที่ระบบได้รับ | ☐ |

### TC-CL-19 — ป้ายใกล้เต็มและเกินวงเงิน (boundary)
- group: ข้อมูลเครดิต · ความสำคัญ: กลาง · trace: AT-12 / BR-08
- actor: Credit Officer
- Setup: role=credit_officer · seed=ลูกค้าใช้วงเงินตั้งแต่ 85% และลูกค้าเกิน 100% อย่างละ 1 ราย · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: ป้ายการใช้วงเงินสื่อสถานะถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถวลูกค้าใช้วงเงินตั้งแต่ 85% | — | เห็นป้าย **ใกล้เต็มวงเงิน** | ☐ |
| 2 | VERIFY แถวลูกค้าใช้วงเงินเกินวงเงินจริง | — | เห็นป้าย **เกินวงเงิน** | ☐ |

### TC-CL-20 — ลูกค้าเงินสดไม่แสดงแถบเครดิตหรือ AR (edge)
- group: ข้อมูลเครดิต · ความสำคัญ: กลาง · trace: AT-12 / BR-08
- actor: Credit Officer
- Setup: role=credit_officer · seed=ลูกค้าวงเงินจริง 0 บาท · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: ลูกค้าเงินสดมีข้อความ **เงินสด** และไม่มีข้อมูลเครดิตที่ไม่เกี่ยวข้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวลูกค้าเงินสด | — | เห็นคำว่า **เงินสด** ในสรุปเครดิต | ☐ |
| 2 | VERIFY ส่วนสรุปเครดิต | — | ไม่มีแถบการใช้วงเงินหรือรายการ AR ที่อ้างวงเงินจริง | ☐ |

### TC-CL-21 — ข้อมูล AR เป็นข้อมูลอ่านอย่างเดียว (permission)
- group: ข้อมูลเครดิต · ความสำคัญ: กลาง · trace: AT-13, XT-04
- actor: Credit Officer
- Setup: role=credit_officer · seed=มีลูกค้าที่มีรายการ AR และข้อมูล AR/SO ล่าสุด · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: เห็นเอกสารค้างชำระ อายุหนี้ และ DSO แต่แก้ไขยอดจากหน้านี้ไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวลูกค้า แล้ว CLICK แท็บ **รายการ AR** | — | ตารางแสดงเอกสาร วันครบกำหนด มูลค่า ยอดค้าง และสถานะ | ☐ |
| 2 | VERIFY ข้อมูล AR | — | เห็นข้อมูลล่าสุดที่ระบบได้รับ; ไม่มีปุ่มแก้ยอดเอกสารจากหน้านี้ | ☐ |

### สัญญาเชื่อมต่อและความปลอดภัย

### TC-CL-22 — Customer Master ดูได้เฉพาะวงเงินจริงที่อนุมัติแล้ว (ต้อง simulate)
- group: สัญญาเชื่อมต่อ · ความสำคัญ: สูง · trace: BR-13, LOCK-CL-01, LOCK-CL-05
- actor: ผู้ดูแลข้อมูลลูกค้า
- Setup: role=customer_master_viewer · seed=มีคำขอ draft/pending และมีวงเงินจริงก่อนหน้า · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: คำขอที่ยังไม่อนุมัติไม่ถูกส่งเป็นวงเงินจริงไปหน้าลูกค้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY รายละเอียดคำขอที่ยังไม่อนุมัติ | — | หน้าเครดิตแยกวงเงินจริงออกจากวงเงินที่ขอ | ☐ |
| 2 | VERIFY ฝั่ง Customer Master (ต้อง simulate) | — | เห็นเฉพาะวงเงินจริงที่อนุมัติล่าสุด ไม่เห็นวงเงิน draft/pending เป็นวงเงินจริง | ☐ |

### TC-CL-23 — ผู้ขอและผู้ไม่มีสิทธิ์อนุมัติไม่ได้ (permission, ต้อง simulate)
- group: สัญญาเชื่อมต่อ · ความสำคัญ: สูง · trace: AT-16 / SELF_APPROVAL_FORBIDDEN, APPROVAL_STEP_MISMATCH, XT-03
- actor: Requester / non-current approver
- Setup: role=requester หรือ non_current_approver · seed=คำขอ pending ที่ผู้ทดสอบไม่ใช่ผู้อนุมัติขั้นปัจจุบัน · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: ไม่มีการอนุมัติสำเร็จและวงเงินจริงไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แท็บ **คำขอ & อนุมัติ** ด้วยบัญชีผู้ขอ | — | ไม่เห็นหรือกดปุ่มอนุมัติคำขอตนเองไม่ได้ | ☐ |
| 2 | CLICK ปุ่มอนุมัติผ่านคำขอที่ผิดขั้น (ต้อง simulate) | — | ระบบปฏิเสธการอนุมัติ และคำขอยังอยู่สถานะเดิม | ☐ |

### TC-CL-24 — คำขอที่ส่งแล้วแก้จำนวนหรือส่งซ้ำไม่ได้ (negative, ต้อง simulate)
- group: สัญญาเชื่อมต่อ · ความสำคัญ: สูง · trace: BR-DOA-01, BR-DOA-05, REQUEST_NOT_DRAFT, EC-05
- actor: Credit Officer
- Setup: role=credit_officer · seed=คำขอ pending 1 รายการ · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: ต้องสร้างคำขอใหม่ ไม่สามารถเปลี่ยนคำขอที่ส่งแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คำขอ pending | — | ไม่เห็นช่องแก้วงเงินหรือปุ่มส่งคำขอเดิมซ้ำ | ☐ |
| 2 | CLICK ส่งซ้ำผ่าน API/test harness (ต้อง simulate) | — | ระบบปฏิเสธและคำขอเดิมไม่ถูกเปลี่ยน | ☐ |

### TC-CL-25 — สร้างโปรไฟล์เงินสดหนึ่งครั้งต่อหนึ่งลูกค้า (ต้อง simulate)
- group: สัญญาเชื่อมต่อ · ความสำคัญ: สูง · trace: AT-15 / BR-11, PROFILE_ALREADY_EXISTS, XT-01, LOCK-CL-03
- actor: System Administrator
- Setup: role=system_administrator · seed=สร้างลูกค้าใหม่ 1 รายและส่งเหตุการณ์ซ้ำได้ · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: ลูกค้าใหม่มีโปรไฟล์เดียว วงเงินจริง 0 บาท และเหตุการณ์ซ้ำไม่สร้างรายการซ้ำ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หลังสร้างลูกค้าใหม่ (ต้อง simulate) | — | เห็นลูกค้าใหม่ในรายการเครดิตพร้อมคำว่า **เงินสด** | ☐ |
| 2 | VERIFY หลังส่งเหตุการณ์เดิมซ้ำ (ต้อง simulate) | — | ยังมีโปรไฟล์เครดิตเพียงหนึ่งรายการสำหรับลูกค้ารายนั้น | ☐ |

### TC-CL-26 — สถานะขัดแย้งให้โหลดข้อมูลล่าสุด (negative, ต้อง simulate)
- group: สัญญาเชื่อมต่อ · ความสำคัญ: กลาง · trace: AT-18 / EC-08, [AI-DEFAULT]
- actor: Credit Officer
- Setup: role=credit_officer · seed=คำขอเดียวกันถูกแก้ไขจากอีก session ก่อนกดยืนยัน · files=—
- Start: OPEN `#/credit-limits`
- ผ่านเมื่อ: การเปลี่ยนแปลงเก่าไม่ทับข้อมูลใหม่ และผู้ใช้เห็นข้อมูลล่าสุดหลังโหลดใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การทำรายการที่ข้อมูลเก่า (ต้อง simulate) | — | ระบบแจ้งว่าข้อมูลมีการเปลี่ยนแปลงและไม่บันทึกทับ | ☐ |
| 2 | VERIFY หลังโหลดใหม่ | — | เห็นสถานะและข้อมูลล่าสุดจากการทำรายการที่สำเร็จก่อนหน้า | ☐ |

## วิธีที่ agent รัน (Run protocol)

1. รันแต่ละเคสแบบ refresh-safe ตาม Start และ Setup ของเคสเอง
2. บันทึก Result ทุกขั้นเป็น pass/fail/blocked; เคสที่ระบุ **ต้อง simulate** ให้ mark blocked หากไม่มี test harness
3. อย่าใช้ข้อมูล mock ใน prototype ยืนยันผลของระบบจริง; ใช้ค่าที่สร้างในเคสนั้นหรือ seed ที่ระบุ

## Coverage Audit

| หมวด | covered / total |
|---|---:|
| Acceptance tests (AT-01..20) | 20 / 20 |
| Function checklist (FN-01..21, 91, 92) | 23 / 23 |
| Business rules BR-01..13 + BR-DOA-01..05 | 18 / 18 |
| Edge cases EC-01..08 | 8 / 8 |
| Error catalog | 7 / 7 |
| Cross-module XT-01..05 | 5 / 5 |
| Scope locks LOCK-CL-01..05 | 5 / 5 |
| UI states / Esc / search | 6 / 6 |

- Manifest cross-check (FRD §0.12): ✅ 7/7
- ไม่มีรายการนอกขอบเขตถูกสร้างเป็น test case. Sales Order, AR Invoice, Customer Master, My Profile และ DOA ตรวจเฉพาะ contract ที่เชื่อม ไม่สร้างหรือแก้ฟีเจอร์เหล่านั้น

## Result Report (schema)

```json
{
  "feature_id": "F-CUST-CL-001",
  "run_at": "<iso datetime>",
  "results": [
    {"id":"TC-CL-01","status":"pass|fail|blocked","failed_step":null,"evidence":"","note":""}
  ],
  "summary":{"total":26,"pass":0,"fail":0,"blocked":0}
}
```
