# คำสั่งแก้ไข อบรม.html (F133 Training & Development)

คุณจะแก้ HTML prototype single-file ตามรายการนี้เท่านั้น ห้ามแตะส่วนอื่น
ห้าม regenerate ทั้งไฟล์ — แก้เฉพาะจุด (surgical edit)

## บริบท
- ไฟล์: `อบรม.html` · มาตรฐาน html-generator-v9 (CI Warm Light · vanilla JS · single-file SPA · hash routing `#/train/<tab>`)
- ส่วนที่ผ่านการตรวจแล้ว **ห้ามเปลี่ยนพฤติกรรม**: viewerRO guards ทุกจุด, DOA modal + approvalSection, gap hook (Performance), EC ref card (Rate Card display-only), oos section, กันลงทะเบียนซ้ำ/เกิน capacity, ใบรับรองเฉพาะผู้ผ่าน, terminal state guards, tab fallback

## รายการแก้ (ทำตามลำดับ)

### 1. [FIX-01 · CRITICAL] ห้ามบันทึกผลก่อนปิดรอบอบรม
ตำแหน่ง: `openResultModal()` + จุด render ปุ่ม "บันทึกผล" ใน result tab และ learner tab (sessionLearners)
สิ่งที่ผิด: บันทึกผลผ่าน/ไม่ผ่านได้ขณะรอบยัง `status==='open'` (การอบรมยังไม่เกิด) — พิสูจน์แล้ว enroll ในรอบ open ถูก set เป็น passed ได้
แก้เป็น:
- `openResultModal(eid)`: เพิ่ม guard — ถ้า `getSession(e.sessionId).status!=='closed'` → `showToast('บันทึกผลได้หลังปิดรอบอบรม (จบการอบรม)','warning'); return;`
- ปุ่มบันทึกผลทั้ง 2 จุด: ขณะรอบยังไม่ closed ให้ render เป็น disabled + title/tooltip "บันทึกผลได้หลังปิดรอบ"
ตรวจรับ: รอบ open → ปุ่ม disabled และเรียก function ตรงถูกบล็อก state ไม่เปลี่ยน · ปิดรอบแล้ว flow เดิมครบ (audit+NTF)

### 2. [FIX-02 · HIGH] เพิ่ม guard ต้น function 4 ตัว (UI ถูกอยู่แล้ว — ห้ามแก้ UI)
- `enrollApprove(eid)` และ `enrollReject(eid)`: บรรทัดแรกหลัง viewerRO เพิ่ม
  `if(!PERSONAS[TC.persona].canApprove){showToast('เฉพาะผู้อนุมัติ (DOA) เท่านั้น','warning');return;}`
- `sendExpense(eid)`: เพิ่ม `if(!['confirmed','passed','failed'].includes(e.status)){showToast('ส่งได้หลังการลงทะเบียนได้รับอนุมัติ','warning');return;} if(e.expenseSent){showToast('ส่ง Expense Claim ไปแล้ว','info');return;}`
- `submitSession()`: ก่อนสร้าง เพิ่ม `const c=getCourse(TC.draft.courseId); if(!c||c.status!=='published'){showToast('สร้างรอบได้เฉพาะหลักสูตรที่เผยแพร่','warning');return;}`
ตรวจรับ: เรียกทั้ง 4 ด้วยเงื่อนไขผิด → toast + state ไม่เปลี่ยน · เส้นทาง UI ปกติเหมือนเดิม

### 3. [FIX-03 · HIGH] เพิ่ม เช็คชื่อ + ประเมินหลังอบรม (capability ตาม spec — ห้ามหายเงียบ)
ตำแหน่ง: learner tab ใน sessionViewDrawer + data enroll
แก้เป็น (mock ระดับ FN):
- เพิ่ม field `attended:null|true|false` และ `evalScore:null, evalComment:''` ใน enroll (mock เดิมเติม field ได้)
- เมื่อรอบ `closed`: แถวผู้เรียน confirmed แสดง toggle เช็คชื่อ **เข้า/ขาด** (append audit)
- ผู้เรียน `attended!==true` → บันทึกผลไม่ได้ (toast "ต้องเช็คชื่อเข้าอบรมก่อน")
- ใน modal บันทึกผล เพิ่มส่วน "ประเมินหลังอบรม": คะแนน 1-5 (ปุ่มเลือก) + comment (optional) เก็บลง enroll + แสดงในแถวผล
ตรวจรับ: ลำดับบังคับ ปิดรอบ→เช็คชื่อ→บันทึกผล · คนขาดบันทึกผลไม่ได้ · คะแนนประเมินแสดงผลได้

### 4. [FIX-04 · HIGH] เพิ่ม ประวัติอบรมรายคน + ชั่วโมงสะสม
ตำแหน่ง: result tab + learner tab — ชื่อผู้เรียนคลิกได้
แก้เป็น: คลิกชื่อ → drawer/section "ประวัติอบรม — [ชื่อ]" แสดง: ทุก enrollment ของคนนั้น (หลักสูตร · รอบ · ผล · ใบรับรอง) + **ชั่วโมงสะสมรวม** = ผลรวมชั่วโมง (parse จาก duration ของหลักสูตร) เฉพาะรายการสถานะ passed · ไม่มีประวัติ → empty state มาตรฐาน
ตรวจรับ: เปิดจากชื่อได้ทั้ง 2 แท็บ · ชั่วโมงนับเฉพาะผ่าน · empty state ถูก

### 5. [FIX-05 · HIGH] เพิ่มการ์ด "ต้นทุนต่อหัว (มุม EC)" ในแท็บรายงาน
แก้เป็น: ต่อหลักสูตรที่ `has_cost` แสดง งบ · จำนวนผู้ผ่าน · ต้นทุนต่อหัว = งบ/ผู้ผ่าน (ผู้ผ่าน=0 หรือฟรี → "—") + note ใต้การ์ด: "อัตรากลางจริงอ่านจาก Rate Card เมื่อพร้อม — ไม่ hardcode · EC ไม่ลงบัญชี"
ตรวจรับ: คำนวณถูก ไม่หารศูนย์ · note ครบ

### 6. [FIX-06 · MINOR] Icon/avatar ใน modal ไม่แสดง
- modal ลงทะเบียน: icon header + avatar การ์ด gap เป็นกล่องว่าง → ให้ `renderIcons()` ครอบ modal หลัง `tcOpenModal()` ทุกครั้ง + ตรวจ initials avatar ใน modal แสดงจริง
- ปุ่ม icon เล็กข้าง "บันทึกผล" ใน learner tab มองไม่เห็น icon → เพิ่ม contrast ทุก state
ตรวจรับ: ไม่มีกล่อง icon/avatar ว่างในทุก modal ที่ zoom 100%

### 7. [FIX-07 · MINOR] Combobox ผู้เรียนใน modal
- list โดนขอบ modal clip เหลือรายการเดียว → ยก overlay เป็น portal/แก้ z+overflow ตามหลัก Overlay Portal (#95) ให้เห็นอย่างน้อย 4-5 รายการ scroll ได้
- option เพิ่ม avatar initials ให้ครบ anatomy combobox คน (#102): avatar + ชื่อ + ตำแหน่ง
ตรวจรับ: list ไม่โดนตัด · ทุก option มี avatar+ชื่อ+ตำแหน่ง

## ข้อห้าม
- ห้ามเพิ่ม dependency/CDN · ห้ามแตะ BASE-KIT block · ห้ามเปลี่ยน CI token
- ห้ามลบ oos section / comment hook / GATE note (อัพเดตค่า GATE ได้หลังรันจริง)
- ถ้าทีมตัดสินใจ**ไม่ทำ** ข้อ 3 หรือ 4 → ห้ามข้ามเงียบ: เพิ่มรายการเข้า oos + แจ้ง BA เปิด OQ-17 ให้ Strike เคาะ

## หลังแก้เสร็จ ให้รันเองก่อนส่ง
1. `node --check` ทุก script block
2. `audit.sh` → FAIL=0
3. Playwright: pageerror=0 ทั้ง 4 แท็บ + เคสต่อไปนี้ผ่าน:
   - รอบ open: บันทึกผลถูกบล็อก (ปุ่ม+function) · ปิดรอบแล้วบันทึกได้
   - persona เจ้าหน้าที่เรียก enrollApprove ตรง → ถูกบล็อก
   - sendExpense ตอน pending_doa / ส่งซ้ำ → ถูกบล็อก
   - submitSession หลักสูตร closed → ถูกบล็อก
   - เช็คชื่อขาด → บันทึกผลไม่ได้
แนบผลรัน 3 ข้อนี้กลับมาพร้อมไฟล์
