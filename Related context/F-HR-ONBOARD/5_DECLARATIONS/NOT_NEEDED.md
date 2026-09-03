# NOT_NEEDED — F-HR-ONBOARD · On/Offboard (เข้าออกงาน)

> S1.8 · 2026-08-29 · คู่กับ `briefs/W3/F-HR-ONBOARD/_lane/DECL.json` — **ไฟล์นี้มีไว้เพื่อไม่ให้มีอะไรถูกข้ามเงียบ**

## ท่อประกาศ (5 ท่อ) — **ประกาศ 3 · ไม่ต้อง 2 · ไม่มีท่อไหนถูกข้ามเงียบ**

| ท่อ | chip (CHECKLIST/FEATURE_LIST_ALL/CONTEXT_PACK) | detect (PREBRIEF §12 · authoritative) | ผล | ไฟล์ |
|---|---|---|---|---|
| **DOA** | ✓ | need · **ไม่มีวงเงิน · จุดตัด = ประเภทการออก** | **ประกาศ** | `DOA_BRIEF.md` |
| **NTF** | ✓ | need · **9 event** | **ประกาศ** | `NTF_BRIEF.md` |
| **CSQ** | ✓ | need · **SecC ท่อเดียว · 7 event** | **ประกาศ** | `CSQ_BRIEF.md` |
| **DOCCFG** | — | **no** | **ไม่ต้อง** (เหตุผลด้านล่าง) | — |
| **PDF DOC** | — | **no** | **ไม่ต้อง** (เหตุผลด้านล่าง) | — |

**DIVERGENCE: —** (chip = detect ทั้ง 5 ท่อ · `_lane/DECL.json.divergence = []` · ทุกท่อ `source: prebrief§12`) · รายละเอียดที่ต้องรู้เพิ่มอยู่ใน `briefs/W3/F-HR-ONBOARD/_lane/DIVERGENCE.md`

---

## ⭐ ทำไม **DOCCFG ไม่ต้อง** (เหตุผลที่ต้องเขียน ห้ามเงียบ)

**feature นี้เป็นกระบวนการที่มี checklist — ไม่ใช่เอกสารที่คนถือ**

1. **ไม่มีสิ่งใดในระบบที่ต้องมีเลขที่เอกสาร** — สิ่งที่ผลิตออกมาคือ **รอบเข้างาน / รอบออกงาน** ที่มีสถานะและงานผูกอยู่ · รอบใช้ **รหัสภายในของระบบ** เท่านั้น ไม่มีใครถือกระดาษที่มีเลขนี้ไปยื่นให้ใคร (PREBRIEF §7)
2. **ไม่มีสำเนา (snapshot policy) ที่ต้องเก็บตามรอบเอกสาร** — หลักฐานของ feature นี้คือ **ประวัติ append-only + ผลตอบกลับจากต้นทาง (`ack_by`/`ack_at`/`ack_ref`)** ไม่ใช่สำเนา PDF (PREBRIEF §3.3 · BR-04 · BR-19)
3. ⭐ **เอกสารที่คนถือจริงเป็นของ feature พี่น้องในเวฟเดียวกัน — ไม่ใช่ของที่นี่:**
   - **คำสั่งเปลี่ยนแปลงพนักงาน `MV-YYYY-NNNN`** → **Employee Movement (W3 lane B)** ซึ่งประกาศ `doccfg + pdfdoc` ไว้เอง
   - **หนังสือรับรองการทำงาน `CERT-YYYY-NNNN`** → **feature หนังสือรับรอง (W3 lane C)** ซึ่งประกาศ `doccfg + pdfdoc` ไว้เอง
   - feature นี้มีได้แค่ **ลิงก์ไปขอ** ที่สอง feature นั้น (PREBRIEF §9 · OB-17) — **ออกเอกสารเองเมื่อไร = ทำซ้ำ #107**
4. **สอดคล้องกับ ERP มาตรฐาน** — Odoo ใช้ระเบียนพนักงาน + activity plan · D365 ใช้ checklist instance · SAP ใช้ process instance · **ไม่มีค่ายไหนออกเลขที่เอกสารให้รอบ onboarding/offboarding** (`STANDARD_BASELINE §4`)
5. **ตรงกับ chip ทั้งสามแหล่ง** — `briefs/W3/CHECKLIST.md` (`doa · ntf · csq`) · `FEATURE_LIST_ALL.md` (`doa ntf csq`) · `CONTEXT_PACK/HR.md` แถว On/Offboard (DOCCFG = —)

> **ถ้าวันหนึ่งต้องมีเอกสารจริง** (เช่น "ใบส่งมอบ-รับคืนทรัพย์สิน" ที่ต้องเซ็นเป็นกระดาษ) → **ต้องกลับมาประกาศ `doccfg` + `pdfdoc` ใหม่ ห้ามแอบสร้างเลขที่เอง** — ยกเป็น OQ ตอนนั้น

## ⭐ ทำไม **PDF DOC ไม่ต้อง**

1. **ไม่มีแบบฟอร์มทางการที่ต้องพิมพ์ เซ็น หรือส่งออกจาก feature นี้** — ทุก output เป็นสถานะบนจอ + งานใน Operation Process + คำขอไปยัง Roles & Permissions
2. **archetype = master ไม่ใช่ Q-document** (`archetype_confirmed: master`) — ไม่มี wizard 5 ขั้น · ไม่มี view tab `รายละเอียด › PDF › ลายเซ็น › ประวัติ` · **ไม่มี tab PDF และไม่มี tab ลายเซ็น** (`STANDARD_BASELINE §3`) · `decl_rule.py` จึงไม่ตั้ง `pdfdoc = true` อัตโนมัติ (กติกา "archetype Q ⇒ pdfdoc" ไม่เข้าเงื่อนไข)
3. **การอนุมัติไม่ได้ทำให้เกิดเอกสาร** — `approval_scope` ของใบ DOA คือ **`policy_approve` ไม่ใช่ `document_sign`** (`DOA_BRIEF §1` · OQ-DOA-05) เพราะสิ่งที่อนุมัติคือการสิ้นสุดสภาพและการเพิกถอนสิทธิ์ ไม่ใช่การเซ็นเอกสาร
4. **ไม่ทำ e-signature รอบนี้** (S-36 · **OQ-STD-OB6**) — สอดคล้องกับ lane C (หนังสือรับรอง) ที่ประกาศไว้เองว่า "ไม่ทำ e-signature จริง (ช่องเซ็น + ตราบริษัท)"
5. **หลักฐานการรับทราบภาระผูกพัน (S-58)** และ **หลักฐานการปิดงาน** ใช้ **การแนบไฟล์ผ่าน Document Center** ที่มีอยู่แล้ว — feature เก็บเพียงการอ้างอิง (`evidence_ref`) · **ไม่ผลิตไฟล์เอง**
6. **ผลข้างเคียงที่ตั้งใจ:** ไม่ต้องรัน `thai-doc-pdf-generator` ในเลนนี้ → **ไม่มี `PDFDOC/` และไม่มี `PRINT_SPEC.md` ใน dev pack** · S5 (`frd-generator-v6`) ต้องไม่ไปหาไฟล์เหล่านี้ · **ไม่ใช่ของหาย แต่ไม่มีตั้งแต่ต้น**

---

## ท่อ 7C ที่ **ไม่ประกาศ** ภายใน `CSQ_BRIEF.md` (บันทึกไว้ให้ตรวจได้ · ห้ามเงียบ)

| ท่อ | สถานะ | เหตุผล |
|---|---|---|
| **OC** | ❌ **ห้ามประกาศ — จุดที่พลาดง่ายที่สุดของ feature นี้** | งาน checklist **ทุกงานถูกประกาศเป็น SOW ของ Operation Process จริง** (PREBRIEF S-45 · BR-02) → OP ยิง `sow.*` และ **OC เกิดเองที่ฝั่ง OP** · ประกาศที่นี่ = **นับซ้ำ + register 422** · **"มี checklist" ไม่ได้แปลว่า "ต้องประกาศ OC" — เจ้าของท่อ OC คือ Operation Process เจ้าเดียว** |
| **DC ระดับเอกสาร** | ❌ **ห้ามประกาศ** | **DOA engine เป็นเจ้าของ** — feature นี้มี approval จริง **3 action** (`DOA_BRIEF §2`) ยิ่งต้องไม่ประกาศซ้ำ · **422** |
| **SC** | ❌ **ห้ามประกาศ** | สงวนไว้ (OQ-C3 ยังไม่เคาะ) · `trigger=false` เสมอ |
| **DC (terminal decision)** | ⬜ ไม่ประกาศ | ไม่มี decision แบบ Continue/Adjust/Hold/Stop/Complete — **การอนุมัติการออกเป็นการเซ็นอนุมัติ** และ **ผลการทบทวนทดลองงานเป็นข้อมูลนำเข้าของรอบออกงาน/Employee Movement ไม่ใช่จุดจบของกระบวนการที่นี่** |
| **EC** | ⬜ ไม่ประกาศ | ต้นทุนการเข้า-ออกงาน (สรรหา · ตำแหน่งว่าง · เวลาทำ checklist) **ยังไม่มีฐานคิด** และ **scope note ตัดเรื่องเงินทั้งหมด** (BR-18) — ใส่ตัวเลขที่คำนวณเอง = **CSQ G7 FAIL** · ถ้ามี Rate Card ในอนาคตให้กลับมาเคาะ (OQ-CSQ-05) |
| **AC** | ⬜ ไม่ประกาศ | ไม่มีรายการทางบัญชีที่นี่ — **ค่าชดเชย/เงินได้ครั้งสุดท้ายเกิดที่ Payroll (W4)** และ Accounting (S-44 · OQ-STD-OB5) |
| **FC** | ⬜ ไม่ประกาศ | ไม่มีเงินสด/งบเปลี่ยน — **งบอัตรากำลังอยู่ที่ Manpower Planning (W6)** · การจ่ายจริงอยู่ที่ Payroll |

## Event ที่จงใจ **ไม่ประกาศ** ใน `NTF_BRIEF.md` (กันประกาศซ้ำท่อ)

| ไม่ประกาศ | เจ้าของจริง |
|---|---|
| `doa_pending` · `doa_result` · `doa_escalate` | **DOA Engine** ยิงอัตโนมัติ — ประกาศซ้ำ = BLOCK |
| การเตือนซ้ำเมื่อรอบค้างอนุมัตินาน (SLA reminder) · **การมอบฉันทะผู้อนุมัติ (delegation)** | **DOA Engine + ENG-NOTIFY** (`catalog §0` — threshold/delegate/expiry/SoD) · **S-57 คือการ "ตรวจและสร้างงาน" ไม่ใช่การทำ delegation หรือแจ้งแทน DOA** |
| **การมอบหมาย/ปิดงานรายใบใน Operation Process (`sow.*`)** | **Operation Process** — ใบนี้ประกาศเฉพาะเหตุการณ์ **ระดับรอบ** · สองตัวที่คาบเกี่ยว (`case_task_due_soon` · `case_task_overdue`) ติด `[AI-DRAFT]` + **OQ-NTF-02** ให้ตัดออกถ้า OP แจ้งให้แล้ว |
| **"ใกล้ครบระยะทดลองงาน" · "ใกล้ครบระยะบอกกล่าว"** | ⛔ **ประกาศไม่ได้** — ต้องใช้ `employment_term.*` ที่ **HR Configuration ยังไม่เผยแพร่** · **ห้ามเดาจำนวนวันเพื่อให้ยิง event ได้** (OQ-NTF-03 ← **OQ-STD-OB3 ← OQ-STD-06**) |
| `hrconfig.*` · `attendance.*` · `leave.*` · `roles.*` | **feature ต้นทาง** — On/Offboard เป็นผู้ฟัง ไม่ใช่ผู้ประกาศ |
| การบันทึกร่าง · การ validate ในหน้าจอ · การเผยแพร่ read model | ไม่ใช่เหตุการณ์ที่คนอื่นต้องรู้ / เป็น pull ไม่ใช่ push |

## ความสามารถที่ **ไม่ implement** เพราะเป็นของ baseline (ห้าม re-implement)

| ความสามารถ | เจ้าของ | feature นี้ทำอะไรแทน |
|---|---|---|
| สายอนุมัติ · threshold · delegate · expiry · SoD | **DOA Engine** (Policy Center) | ประกาศ `DOA_BRIEF` 3 action + เรียก `GET /doa/resolve` |
| การแจ้งเตือน · ช่องทาง · preference · การยิงซ้ำ | **ENG-NOTIFY** | ประกาศ `NTF_BRIEF` (event ธุรกิจเท่านั้น) |
| การตีมูลค่า/ประทับผล 7 ท่อ | **ENG-CSQ / ENG-CSQ-02** | ประกาศ `CSQ_BRIEF` + emit event · **ไม่มีการ์ดผล 7 ท่อในหน้า** |
| ⭐ **บัญชีผู้ใช้ · role · permission matrix · MFA · session** | **Roles & Permissions + User Management + Password/MFA (Policy Center)** | **ส่ง "คำขอ" เปิด/เพิกถอน/คืนสิทธิ์ แล้วรอผลตอบกลับ** · **ไม่มีหน้าจัดการสิทธิ์ที่นี่เลย** (FN-70 · FN-71) |
| ⭐ **งาน · แม่แบบกระบวนการ · ปฏิทินงาน · Gantt · "งานของฉัน"** | **Operation Process (CL/SOP/SOW · Template · Configuration) + Action/Team Plan + Cockpit** | **ประกาศงานทุกงานเป็น SOW** แล้วอ้าง `sow_ref` (FN-61 · FN-62) |
| **เลขรันเอกสาร · policy สำเนา** | **Document Configuration** (`ENG-DOC-NUM` · `ENG-DOC-STORE`) | **ไม่ใช้รอบนี้** — ไม่มีเอกสาร (ดูเหตุผลด้านบน) |
| **ที่เก็บไฟล์แนบ** | **Document Center** | เก็บเพียงการอ้างอิง (`evidence_ref`) |
| สิทธิ์การมองเห็น · masking · audit | **Policy Center (Data Masking · Audit Trail)** | ใช้ของกลาง · ไม่ทำ audit เอง (BR-19) |
| ข้อมูลพนักงาน/ตำแหน่ง/แผนก/บริษัท | **Employee Master + Organization** | combobox #102 + snapshot ชื่อ · **ไม่ CRUD ข้าม feature** |
| **ระยะทดลองงาน · ระยะบอกกล่าว · ปฏิทินวันหยุด · งวด** | **HR Configuration** (W1) | `resolve(date, company)` + เก็บ `version_id` · ลิงก์ "จัดการที่ HR Configuration" (#107 · HR-1) · ⭐ **คีย์ `employment_term.*` ยังไม่ถูกเผยแพร่ → แสดง "ยังไม่มีค่าให้อ่าน" ห้ามเดา** |
| **เวลาเข้า-ออกจริง · วันลา · ยอดสิทธิ์คงเหลือ** | **Attendance (W1) · Leave (W2)** | อ่านอย่างเดียวเพื่อเตือนก่อนปิดรอบ · **ไม่มีการเขียนกลับ** (AT-5 · LV-5) |
| **ค่าชดเชย · เงินได้ครั้งสุดท้าย · payslip** | **Payroll (W4 · ⏳)** | เผยแพร่ `last_working_day` ให้อ่าน · **ไม่มีตัวเลขเงิน** |
| **ทะเบียนทรัพย์สิน** | **Asset (⏳ ยังไม่มีในแผง 142)** | เก็บรายการระดับรอบ + hook + Module Linkage · **ห้าม mock หน้าทะเบียน** |
| **สรรหา/คัดเลือกผู้สมัคร** | **Recruit (W5 · ⏳)** | ช่องอ้างผู้สมัคร + Module Linkage |
| **สวัสดิการ** | **Welfare (W4 · ⏳)** | เผยแพร่สัญญาณ joiner/leaver |
| **คำสั่งเปลี่ยนแปลงพนักงาน · หนังสือรับรอง** | **Employee Movement (W3/B) · หนังสือรับรอง (W3/C)** | **ลิงก์ไปขอเท่านั้น** |
