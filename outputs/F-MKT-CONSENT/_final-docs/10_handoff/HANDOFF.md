# Handoff — ความยินยอม PDPA (F-MKT-CONSENT · F058)

ปิดงาน WF-01 ครบ 12 step · standalone (dep="") · module การตลาด · wave W1/S1 · declaration = **csq เท่านั้น** (declare-only)

> 🔁 **ผ่านรอบแก้ BA gate (2026-09-14):** BA ตีกลับ BLOCK → แก้ HTML 8 จุด (FIX-01..08) แล้ว re-gate + regen เอกสารทั้งชุดเป็น v1.1

## เริ่มตรวจงานที่ไหน
1. **ต้นแบบจริง** → `01_prototype/consent-pdpa.html` (เปิดในเบราว์เซอร์เล่นได้เลย)
2. **สรุปฟีเจอร์อ่านง่าย** → `08_tldr/FEATURE_TLDR_F-MKT-CONSENT.html`
3. **Manual test** → `testcase_qa/ความยินยอม PDPA HTML Testcase.html` (71 เคสคนเล่นได้ · กรอกผล ✓/✗ + พิมพ์ PDF ได้)

## สถานะการตรวจ (ผ่านครบทุกด่าน · หลังแก้ BA gate)
- qc-ux **PASS** · coverage รอบ 1 **PASS** · coverage รอบ 2 **PASS** · audit.sh **FAIL=0** (WARN=3 base-kit)
- e2e **49/49 · FN ครอบ 20/20** · FN-40 negatives 10/10 (ของที่ต้องไม่มี ยืนยันว่าไม่มีจริง)
- 8 จุดที่ BA ตีกลับแก้ครบ (FIX-01 ตอบครั้งเดียว · FIX-02 สิทธิ์ตามบทบาทจริง · FIX-03 เห็นเวอร์ชันที่ส่ง · FIX-04 กันกดซ้ำ · FIX-05 guard สถานะ · FIX-06 anchor สัญญา · FIX-07 demo-only · FIX-08 คอลัมน์สถานะ)

## 🔴 ต้องเคาะก่อนเปิดใช้จริง (dev ห้ามเดา — ดู `PROPOSALS_outbound.md`)
- **OQ-03** วิธียืนยันตัวตนจริงในมุมมองผู้รับ (ตอนนี้เป็น checkbox จำลอง)
- **OQ-04** ขึ้นทะเบียน `/consent/*` กับด่านบังคับใช้สิทธิ์ (Backend Enforcement Gate / F143)

## 🟠 งานประสาน / governance + ประเด็นเปิดใหม่จาก BA (Strike เคาะก่อนเขียน FRD ปลายทาง)
- **OQ-01** BA sync PREBRIEF BR-05/06 + FN-01/02/09/10/11 ให้เป็นโมเดล **"อัปโหลดเอกสาร"** (DECLARED-01 — เปลี่ยนจากพิมพ์ข้อความตามที่ PM/BA สั่ง)
- **OQ-CNS-01** เปลี่ยนใจหลังตอบแล้ว = คำขอใหม่/withdraw (ไม่แก้ผ่านลิงก์เดิม) · ใครเปิดคำขอใหม่ได้
- **OQ-CNS-02** publish เวอร์ชันใหม่ระหว่างคำขอค้าง — build ปัจจุบัน **ไม่ auto-expire** (แสดงเวอร์ชัน ณ ตอนส่ง + เตือน)
- **OQ-CNS-03** รอบต่ออายุ trigger แบบ manual หรือ batch
- reconcile microcopy FRD↔จอ (HTML เป็นตัวจริง) · เลขสรุป TC reconcile แล้ว (83 ตรงกัน)

## เนื้อหาสำคัญของฟีเจอร์
- โมเดล triple key (เจ้าของ × วัตถุประสงค์ × ช่องทาง) · default-deny · เนื้อหา = เอกสารอัปโหลด versioned ต่อวัตถุประสงค์
- มุมมองผู้รับเต็มจอ: เปิดลิงก์ → อ่านเอกสาร → ยืนยันตัวตน → ยินยอม/ไม่ยินยอมรายวัตถุประสงค์ → หลักฐาน 5 อย่าง
- `/consent/resolve` = HTTP 200 เสมอ · never-asked → `allowed:false, status:"never_asked"` (ไม่ใช่ 404 / ไม่ใช่ "ไม่ยินยอม")
- ถอนความยินยอม = มีผลทันที ไม่ต้องอนุมัติ · ต่ออายุ = คำขอใหม่อ้างรายการเดิม

รายละเอียดข้อเสนอ/OQ ทั้งหมด → `PROPOSALS_outbound.md` · รายการ pending design-system → `PENDING_REGISTRY.md`
