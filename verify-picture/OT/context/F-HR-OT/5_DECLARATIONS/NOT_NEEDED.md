# NOT_NEEDED — F-HR-OT · OT / Shift (โอที)

> S1.8 · 2026-08-29 · คู่กับ `_lane/DECL.json` — **ไฟล์นี้มีไว้เพื่อไม่ให้มีอะไรถูกข้ามเงียบ**

## ท่อประกาศ (5 ท่อ) — **ไม่มีท่อไหนถูกข้าม**

| ท่อ | chip (POOL/CHECKLIST/CONTEXT_PACK) | detect (PREBRIEF §12 · authoritative) | ผล | ไฟล์ |
|---|---|---|---|---|
| **DOA** | ✓ | need · **2 ชั้นตามเพดาน** | **ประกาศ** | `DOA_BRIEF.md` |
| **NTF** | ✓ | need | **ประกาศ** | `NTF_BRIEF.md` |
| **CSQ** | ✓ | need · **EC + FC** | **ประกาศ** | `CSQ_BRIEF.md` |
| **DOCCFG** | ✓ | need | **ประกาศ** | `DOCCFG_BRIEF.md` |
| **PDF DOC** | ✓ | need | **ประกาศ** | `PDFDOC/{template.html, sample.pdf, print-spec.md}` |

**DIVERGENCE: —** (chip = detect ทั้ง 5 ท่อ · `_lane/DECL.json.divergence = []` · ทุกท่อ `source: prebrief§12`)

## ท่อ 7C ที่ **ไม่ประกาศ** ภายใน `CSQ_BRIEF.md` (บันทึกไว้ให้ตรวจได้ · ห้ามเงียบ)

| ท่อ | สถานะ | เหตุผล |
|---|---|---|
| **OC** | ❌ **ห้ามประกาศ** | มาจาก Operation Process (`sow.*`) อัตโนมัติ — feature นี้ไม่สร้างงาน OP · ประกาศซ้ำ = register **422** |
| **DC ระดับเอกสาร** | ❌ **ห้ามประกาศ** | **DOA engine เป็นเจ้าของ** — feature นี้มีการอนุมัติจริง **ถึงสองชั้น** ยิ่งต้องไม่ประกาศซ้ำ · **422** |
| **SC** | ❌ **ห้ามประกาศ** | สงวนไว้ (OQ-C3 ยังไม่เคาะ) · `trigger=false` เสมอ |
| **DC (terminal decision)** | ⬜ ไม่ประกาศ | ไม่มี decision แบบ Continue/Adjust/Hold/Stop/Complete — **แม้แต่ "เกินเพดานแล้วขึ้นอีกชั้น" ก็เป็นการเลือกสายอนุมัติ ไม่ใช่ terminal decision** |
| **AC** | ⬜ ไม่ประกาศ | ไม่มีรายการทางบัญชีที่นี่ — ตั้งค่าใช้จ่ายค่าล่วงเวลาเกิดที่ **Payroll (W4)** และ Accounting · scope note ตัด "ไม่คิดเงิน OT" ชัด (OQ-STD-OT1) |
| **SecC** | ⬜ ไม่ประกาศ | **นโยบาย OT (อัตรา · ตัวคูณ · เพดาน) เป็นของ HR Configuration** ซึ่งประกาศ SecC ไว้แล้ว (`CSQ-HRCFG` E1–E6) — ประกาศที่นี่ = **นับซ้ำ** · feature นี้ไม่มีบัญชีสิทธิ์รายคนเป็นของตัวเอง (ต่างจาก Leave ที่มี จึงประกาศ SecC ได้) |

## Event ที่จงใจ **ไม่ประกาศ** ใน `NTF_BRIEF.md` (กันประกาศซ้ำท่อ)

| ไม่ประกาศ | เจ้าของจริง |
|---|---|
| `doa_pending` · `doa_result` · `doa_escalate` | **DOA Engine** ยิงอัตโนมัติ — ประกาศซ้ำ = BLOCK |
| การมอบฉันทะผู้อนุมัติ (delegation) · การเตือนซ้ำเมื่อใบค้างอนุมัตินาน (SLA reminder) | **DOA Engine + ENG-NOTIFY** (`feature-catalog-master.md §0` ระบุว่า DOA มี threshold/delegate/expiry/SoD) — S1.5 G-10 · G-11 → SKIP |
| `hrconfig.*` · `attendance.*` · `leave.*` | **feature ต้นทาง** — OT เป็นผู้ฟัง ไม่ใช่ผู้ประกาศ |
| การบันทึกร่าง · การ validate/บล็อกในหน้าจอ · การเผยแพร่ read model | ไม่ใช่เหตุการณ์ที่คนอื่นต้องรู้ / เป็น pull ไม่ใช่ push |

## ความสามารถที่ **ไม่ implement** เพราะเป็นของ baseline (ห้าม re-implement)

| ความสามารถ | เจ้าของ | feature นี้ทำอะไรแทน |
|---|---|---|
| สายอนุมัติ · threshold · delegate · expiry · SoD | **DOA Engine** (Policy Center) | ประกาศ `DOA_BRIEF` 2 action + เรียก `GET /doa/resolve` |
| เลขรันเอกสาร · policy สำเนา | **Document Configuration** (`ENG-DOC-NUM` · `ENG-DOC-STORE`) | ประกาศ `DOCCFG_BRIEF` |
| การแจ้งเตือน · ช่องทาง · preference | **ENG-NOTIFY** | ประกาศ `NTF_BRIEF` (event ธุรกิจเท่านั้น) |
| การตีมูลค่า/ประทับผล 7 ท่อ | **ENG-CSQ / ENG-CSQ-02** | ประกาศ `CSQ_BRIEF` + emit event (ไม่คำนวณเอง · ไม่มีการ์ดผล 7 ท่อในหน้า) |
| สิทธิ์ · role · masking · ข้อมูลพนักงาน | **Policy Center + Employee Master** | อ้าง role id · combobox #102 |
| งาน/แผน/ปฏิทินงาน | **Operation Process + Action/Team Plan** | ไม่สร้าง planner ใหม่ |
| **อัตรา OT · ตัวคูณ · เพดาน · ปฏิทินวันหยุด · แพทเทิร์นกะ · งวด** | **HR Configuration** (W1) | `resolve(date, company)` + เก็บ `version_id` · ลิงก์ "จัดการที่ HR Configuration" (#107 · HR-1) |
| **เวลาเข้า-ออกจริง · ชั่วโมงในกรอบกะ · สาย/ขาด** | **Attendance** (W1) | อ่าน `outside_shift_hours` อย่างเดียว · **ไม่มีการเขียนกลับ** (AT-5) |
| **สิทธิ์/โควตาการลา** | **Leave** (W2 lane A) | อ่าน `GET /leave/resolve` เพื่อกันขอ OT ทับวันลา (LV-5) |
| **การจัดกะ/ตารางเวร/ขอสลับกะ** | **Shift & Roster** (W2 lane C · ⏳) | ไม่ทำ — มีเพียงกะที่อ่านมาเป็นข้อมูลประกอบ + hook กันจัดกะทับ (Module Linkage) |
| **การคำนวณค่าล่วงเวลาเป็นเงิน · payslip** | **Payroll** (W4 · ⏳) | เผยแพร่ **ชั่วโมง + rate_type + multiplier + payroll_code** ให้อ่าน · **ไม่มีตัวเลขเงิน** |
