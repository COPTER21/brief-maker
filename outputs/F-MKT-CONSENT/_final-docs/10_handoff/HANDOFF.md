# Handoff — ความยินยอม PDPA (F-MKT-CONSENT · F058)

ปิดงาน WF-01 ครบ 12 step วันที่ 2026-09-13 · standalone (dep="") · module การตลาด · wave W1 · declaration = **csq เท่านั้น** (declare-only)

## เริ่มตรวจงานที่ไหน
1. **ต้นแบบจริง** → `01_prototype/consent-pdpa.html` (เปิดในเบราว์เซอร์เล่นได้เลย)
2. **สรุปฟีเจอร์อ่านง่าย** → `08_tldr/FEATURE_TLDR_F-MKT-CONSENT.html`
3. **Manual test** → `testcase_qa/ความยินยอม PDPA HTML Testcase.html` (62 เคสคนเล่นได้ · กรอกผล ✓/✗ + พิมพ์ PDF ได้)

## สถานะการตรวจ (ผ่านครบทุกด่าน)
- qc-ux **PASS** · coverage รอบ 1 **PASS** · coverage รอบ 2 **PASS** · audit.sh **FAIL=0**
- e2e **41/41 · FN ครอบ 20/20** · FN-40 negatives 10/10 (ของที่ต้องไม่มี ยืนยันว่าไม่มีจริง)

## 🔴 ต้องเคาะก่อนเปิดใช้จริง (dev ห้ามเดา — ดู `PROPOSALS_outbound.md`)
- **OQ-03** วิธียืนยันตัวตนจริงในมุมมองผู้รับ (ตอนนี้เป็น checkbox จำลอง)
- **OQ-04** ขึ้นทะเบียน `/consent/*` กับด่านบังคับใช้สิทธิ์ (Backend Enforcement Gate / F143)

## 🟠 งานประสาน / governance
- **OQ-01** BA sync PREBRIEF BR-05/06 + FN-01/02/09/10/11 ให้เป็นโมเดล **"อัปโหลดเอกสาร"** (DECLARED-01 — เปลี่ยนจากพิมพ์ข้อความตามที่ PM/BA สั่ง)
- reconcile microcopy FRD↔จอ (HTML เป็นตัวจริง) + เลขสรุป TC (สรุปเขียน 68 แต่มีจริง 72)

## เนื้อหาสำคัญของฟีเจอร์
- โมเดล triple key (เจ้าของ × วัตถุประสงค์ × ช่องทาง) · default-deny · เนื้อหา = เอกสารอัปโหลด versioned ต่อวัตถุประสงค์
- มุมมองผู้รับเต็มจอ: เปิดลิงก์ → อ่านเอกสาร → ยืนยันตัวตน → ยินยอม/ไม่ยินยอมรายวัตถุประสงค์ → หลักฐาน 5 อย่าง
- `/consent/resolve` = HTTP 200 เสมอ · never-asked → `allowed:false, status:"never_asked"` (ไม่ใช่ 404 / ไม่ใช่ "ไม่ยินยอม")
- ถอนความยินยอม = มีผลทันที ไม่ต้องอนุมัติ · ต่ออายุ = คำขอใหม่อ้างรายการเดิม

รายละเอียดข้อเสนอ/OQ ทั้งหมด → `PROPOSALS_outbound.md` · รายการ pending design-system → `PENDING_REGISTRY.md`
