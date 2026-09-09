# คำสั่งแก้ไข performance.html (F131 Performance — ประเมินผลงาน)

คุณจะแก้ HTML prototype single-file ตามรายการนี้เท่านั้น ห้ามแตะส่วนอื่น
ห้าม regenerate ทั้งไฟล์ — แก้เฉพาะจุด (surgical edit)

## บริบท
- ไฟล์: performance.html · มาตรฐาน html-generator-v9 (CI Warm Light · vanilla JS · single-file · BASE-KIT)
- ส่วนที่ผ่านการตรวจแล้ว **ห้ามเปลี่ยนพฤติกรรม**: KPI weight sum=100 guard, `_busy` double-submit guard, submitNewCycle validation + อ้าง config ตั้งค่า HR, sendMovement/sendTraining (display-only), state machine ลำดับ goal→self→mgr→calibration→published, mask() ฝั่งคะแนน, Esc chain, overlay portal

## รายการแก้ (ทำตามลำดับ)

### 1. FIX-01 doCalib precondition guard — CRITICAL
ตำแหน่ง: `function doCalib(id)`
สิ่งที่ผิด: สอบทาน+เผยแพร่ record ขั้น goal ที่คะแนนหัวหน้า null ทั้งหมดได้ decision "ผ่าน"
แก้เป็น: guard ต้น function — `a.status!=='calibration'` หรือ `rawScore(a)==null` → toast warning + return
ตรวจรับ: doCalib กับ goal/self/mgr/published → ไม่เปลี่ยน · calibration คะแนนครบ → เดินต่อได้

### 2. FIX-02 guard ตามขั้นทุก save — CRITICAL
ตำแหน่ง: `saveKpi` · `saveSelf` · `saveMgr`
สิ่งที่ผิด: เรียกกับ record published ได้ สถานะถอยกลับ (published→mgr) แก้คะแนนหลังประกาศผล
แก้เป็น: saveKpi เฉพาะ `status==='goal'` · saveSelf เฉพาะ `'self'` · saveMgr เฉพาะ `'mgr'` — อื่น toast + return · ห้ามเพิ่ม flow re-open เอง (แขวน OQ-PERF-01)
ตรวจรับ: เรียกสามตัวกับสถานะไม่ตรงขั้น → ไม่เปลี่ยน · flow ปกติเดินครบ

### 3. FIX-05 lock รอบที่ปิด — CRITICAL
ตำแหน่ง: `saveKpi/saveSelf/saveMgr/doCalib/doPip`
สิ่งที่ผิด: รอบ closed แล้วยัง mutate แบบประเมินได้ (ขัด toast "ล็อกการแก้ไข")
แก้เป็น: guard ร่วมต้นทุก function — `cyc(a.cycle).status==='closed'` → toast "รอบนี้ปิดแล้ว — แก้ไขไม่ได้" + return
ตรวจรับ: รอบ closed → ทุก mutation block · รอบ open ปกติ

### 4. FIX-03 role guard ทั้ง UI + function — CRITICAL
ตำแหน่ง: `saveMgr/doCalib/doPip/doCloseCycle/sendMovement/sendTraining` + `reviewView`
สิ่งที่ผิด: role staff เรียก saveMgr สำเร็จ (audit who = พนักงานเอง) · staff เห็นปุ่ม สอบทาน (DOA)/เปิดแผน PIP/ส่งไปอบรม/ส่งเรื่องปรับตำแหน่ง
แก้เป็น: (a) function: saveMgr ต้อง `curRole().id==='mgr'||curRole().manage` · doCalib/doPip/doCloseCycle/send* ต้อง `curRole().manage` — ไม่ผ่าน toast "สิทธิ์ไม่พอ" + return (b) UI: reviewView ไม่ render ปุ่ม mutation ให้ role ที่ไม่ผ่านเงื่อนไขเดียวกัน
ตรวจรับ: staff เรียกทุก mutation ตรง → state ไม่เปลี่ยน + ไม่เห็นปุ่ม · hr/mgr ตามสิทธิ์เดิม

### 5. FIX-04 scope SELF สำหรับพนักงาน — CRITICAL
ตำแหน่ง: `reviewView` · `apprView` · `tabDetail`
สิ่งที่ผิด: persona พนักงานเห็น decision + Gap ของทุกคน (คะแนน mask แต่ decision/gap ไม่) — ขัด "เกรดเป็นความลับต่อคน"
แก้เป็น: role staff (mask=true) → apprView/reviewView กรองเหลือเฉพาะแบบประเมินของตนเอง (map staff ↔ พนักงานในข้อมูล mock ให้ชัด เช่น สมชาย ใจดี) · ข้อมูลคนอื่นไม่อยู่ใน DOM เลย ไม่ใช่แค่ mask · เพิ่ม comment `<!-- SEC: scope_type SELF สำหรับ role พนักงาน — ประกาศใน SEC_BRIEF -->`
ตรวจรับ: staff ไม่พบชื่อ/decision/gap ของคนอื่นใน DOM · hr/mgr เห็นตามเดิม

### 6. FIX-06 DOA slot ห้าม preset + แยกจังหวะสอบทาน — HIGH
ตำแหน่ง: `initFeatureSelects` (doa0/doa1) · `doCalib` · modal `doaCalib`
สิ่งที่ผิด: slot preset value P1/P2 อัตโนมัติ + ปุ่มเดียว "สอบทาน + เผยแพร่ผล" ทำ 2 ขั้น + decision + publish ใน action เดียว
แก้เป็น: (a) `value:null` ทั้งสอง slot — validation เดิมจะบังคับเลือกเอง (b) แยกจังหวะ: ปุ่มแรก "ส่งสอบทาน" = freeze รายชื่อผู้สอบทาน (บันทึก approvals 2 ขั้น สถานะ current/pending — สถานะคำขอคง calibration) · ผู้สอบทานขั้น current บันทึกผลของตน (ขั้นละ action พร้อม at) · ขั้นสุดท้ายบันทึกแล้วค่อย published + decision + notif
ตรวจรับ: modal เปิดมา slot ว่าง · ไม่เลือกครบ → block · publish หลังขั้นสุดท้ายเท่านั้น · ทุกขั้นมี at/ผู้กระทำ

### 7. FIX-07 เพิ่ม CSQ hook — HIGH
ตำแหน่ง: จุด publish ใน `doCalib` + audit + ใกล้หัวไฟล์ส่วน comment
สิ่งที่ผิด: dec ◆csq แต่ไม่มี CSQ/7C ในไฟล์เลย
แก้เป็น: ตอน publish — pushAudit เพิ่มบรรทัด "บันทึกผลประเมินเข้า 7C (ตาม CSQ_BRIEF)" + toast พ่วงข้อความ 7C + comment `<!-- CSQ hook: perf.result.published → ท่อตาม CSQ_BRIEF_F131 (รอเคาะ OQ-PERF-02) — ห้ามประกาศ OC/DC ซ้ำ -->`
ตรวจรับ: publish แล้วเห็นร่องรอย 7C ใน audit/toast · ไม่มีการประกาศท่อสงวน

### 8. FIX-08 Calibration ระดับทีม (view) — HIGH
ตำแหน่ง: `reviewView`
สิ่งที่ผิด: c[3] ระบุ calibrate ระดับทีม/บริษัท — มีแต่สอบทานรายคน
แก้เป็น: เพิ่ม section "Calibration ระดับทีม" (mock): ตารางทุกคนในรอบ — คะแนนถ่วงน้ำหนัก · เกรดเสนอ · ช่องปรับเกรด (mock select) + สรุป distribution ต่อเกรด — เป็นมุมมองประกอบก่อนกดสอบทานรายคน · ถ้ามีมติ OQ-PERF-04 ตัด scope ให้ข้ามข้อนี้และแนบมติ
ตรวจรับ: มี view เทียบทั้งทีม (หรือมติตัด scope แนบมา)

### 9. FIX-09 hook ส่งเข้า Succession — HIGH
ตำแหน่ง: `reviewView` hookbox + ใกล้ sendMovement
สิ่งที่ผิด: c[5] Movement/Succession/Training — ขาด Succession
แก้เป็น: เพิ่ม `function sendSuccession(id){ showToast('ส่งผลเข้า Succession Planning (ส่งต่อ ไม่แก้ที่นี่)','info'); }` + ปุ่ม display-only ใน hookbox ของผลที่เผยแพร่
ตรวจรับ: ผลเผยแพร่มีปุ่ม Succession เคียง Movement/Training

### 10. MINOR รวบ (ทำท้ายสุด)
- FIX-10: เรียก `renderIcons()` หลังเติม drawer innerHTML ใน `render()` — ปุ่มปิด drawer ต้องมี svg เสมอ (ตอนนี้เป็นกล่องเปล่า)
- FIX-11: ช่อง `.slot-pick` ใน modal doaCalib — ขยายกว้าง/ย่อ placeholder เป็น "เลือกผู้สอบทาน…" ไม่ให้ตัดกลางคำ

## ข้อห้าม
- ห้ามเพิ่ม dependency/CDN · ห้ามแตะ BASE-KIT block · ห้ามเปลี่ยน CI token
- ห้ามลบ comment TODO/OQ/FN ที่มีอยู่ (ยกเว้นจุดที่สั่งแก้)
- ห้ามแตะ: KPI weight guard, _busy guard, submitNewCycle, state machine ลำดับขั้น, mask() ฝั่งคะแนน, sendMovement/sendTraining เดิม

## หลังแก้เสร็จ ให้รันเองก่อนส่ง
1. node --check ทุก script block
2. audit.sh → FAIL=0
3. Playwright: pageerror=0 + เคสต่อไปนี้ผ่านครบ:
   - doCalib กับ record goal/self/mgr/published → ไม่เปลี่ยน · calibration ครบคะแนน → ได้
   - saveKpi/saveSelf/saveMgr กับสถานะไม่ตรงขั้น → ไม่เปลี่ยน
   - รอบ closed → ทุก mutation block
   - role staff: เรียก saveMgr/doCalib/doPip ตรง → ไม่เปลี่ยน + ไม่เห็นปุ่ม + ไม่เห็นข้อมูลคนอื่นใน DOM
   - modal doaCalib เปิดมา slot ว่าง · publish เกิดหลังขั้นสุดท้ายบันทึกผลเท่านั้น
   - publish แล้วมีร่องรอย CSQ/7C ใน audit
แนบผลรัน 3 ข้อนี้กลับมาพร้อมไฟล์ แล้วส่ง re-gate เต็มรอบ (verdict BLOCK)
