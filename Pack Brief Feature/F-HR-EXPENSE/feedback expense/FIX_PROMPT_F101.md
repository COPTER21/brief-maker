# คำสั่งแก้ไข expense.html (F101 Expense Claim — เบิกค่าใช้จ่าย)

คุณจะแก้ HTML prototype single-file ตามรายการนี้เท่านั้น ห้ามแตะส่วนอื่น
ห้าม regenerate ทั้งไฟล์ — แก้เฉพาะจุด (surgical edit)

## บริบท
- ไฟล์: expense.html · มาตรฐาน html-generator-v9 (Pattern Q Transaction Document · CI Warm Light · vanilla JS)
- ส่วนที่ผ่านการตรวจแล้ว **ห้ามเปลี่ยนพฤติกรรม**: Pattern Q view 4 แท็บ (รายละเอียด/PDF Preview/ลายเซ็น·อนุมัติ/ประวัติ) + เอกสารแนบใน landing, B2 line editor + VAT engine, DOA ฝั่ง submit (resolveDoa ตามช่วงวงเงิน BR-04/LK-1 · slot ไม่ prefill · submitReady disable ปุ่มจนเลือกครบ), doReject บังคับเหตุผล, over-cap = เตือน+เหตุผลตามมติ A-EXP-05 (ไม่ hard block), `_busy` ทุก action, unsupportedNote

## รายการแก้ (ทำตามลำดับ)

### 1. FIX-01 doApprove precondition guard — CRITICAL
ตำแหน่ง: `function doApprove(id)`
สิ่งที่ผิด: อนุมัติใบ rejected ได้ → approved + ออกเลข EXP-2569-005
แก้เป็น: guard ต้น function — `d.status!=='pending_approval'` → toast warning + return
ตรวจรับ: doApprove กับ rejected/cancelled/draft/approved/paid → ไม่เปลี่ยน · pending_approval → เดินต่อ

### 2. FIX-02 DOA chain advance ทีละขั้น — CRITICAL
ตำแหน่ง: `doApprove`
สิ่งที่ผิด: `d.chain.forEach(s=>s.status='approved')` — chain 3 ขั้น (ผอ. ยัง pending) คลิกเดียว approved หมด
แก้เป็น: หา step แรกที่ pending → set approved + at (เวลา) · ถ้ายังมีขั้นถัดไป เอกสารคง `pending_approval` + toast "อนุมัติขั้น X แล้ว — รอขั้นถัดไป" · ขั้นสุดท้ายค่อย: `approved` + ออกเลข + PDF + 7C + payHook (side-effect ทั้งชุดครั้งเดียวตอนจบ chain)
ตรวจรับ: ใบ chain 3 ขั้น — คลิก 1–2 ยัง pending_approval · คลิก 3 approved + เลขออกครั้งเดียว · ทุกขั้นมี at

### 3. FIX-04 doReopen เฉพาะใบตีกลับ — CRITICAL
ตำแหน่ง: `doReopen`
สิ่งที่ผิด: เรียกกับใบ approved ได้ → กลับ draft + เลข EXP-2569-0001 ถูกทับเป็น "(ร่าง)"
แก้เป็น: guard — `d.status!=='rejected'` → toast + return (แก้ใบอนุมัติแล้ว = flow revision คนละเรื่อง ไม่ทำรอบนี้)
ตรวจรับ: approved/paid/pending/draft → ไม่เปลี่ยน · rejected → draft ได้

### 4. FIX-05 doCancel เฉพาะร่าง — CRITICAL
ตำแหน่ง: `doCancel`
สิ่งที่ผิด: ใบ paid ถูกยกเลิกได้
แก้เป็น: guard — `d.status!=='draft'` → toast + return
ตรวจรับ: paid/approved/rejected/pending → ยกเลิกไม่ได้ · draft → ได้

### 5. FIX-03 สลับทิศ masking + role guard — CRITICAL
ตำแหน่ง: `EXP.roles` · จุด render ปุ่มใน `dwView` foot · `doApprove/doReject`
สิ่งที่ผิด: ผู้อนุมัติ (mgr) `mask:true` เห็นเงิน ฿••••• แต่ต้องอนุมัติตามวงเงิน · ผู้เบิก/ธุรการเห็นเงินทุกใบ + เห็นปุ่มอนุมัติ (self-approve)
แก้เป็น: (a) mgr `mask:false` — ผู้อนุมัติเห็นเงินเต็ม (b) ผู้เบิก/ธุรการ: mask ยอดเงินใบของคนอื่น (ของตนเห็นเต็ม) + comment `<!-- SEC: scope ผู้เบิกรอเคาะ OQ-EXP-03 -->` (c) ปุ่มอนุมัติ/ไม่อนุมัติ render เฉพาะ role mgr + guard ต้น doApprove/doReject: role ต้องเป็น mgr — ไม่ผ่าน toast "สิทธิ์ไม่พอ"
ตรวจรับ: mgr เห็นเงินเต็มบนใบรออนุมัติ · admin ไม่เห็นปุ่มอนุมัติ + เรียก doApprove ตรงไม่ผ่าน

### 6. FIX-06 เลขรันห้ามซ้ำ + hook ENG-DOC-NUM — CRITICAL
ตำแหน่ง: `doApprove` บรรทัด gen code
สิ่งที่ผิด: `'EXP-2569-00'+(3+count(approved))` — count-based ทำเลขซ้ำได้จริง (E6: สองใบได้ EXP-2569-005) + ไม่ pad 4 หลัก + ไม่มีร่องรอย ENG-DOC-NUM/DOCCFG
แก้เป็น: ตัวนับ global เดินหน้าอย่างเดียว เช่น `EXP.docSeq=(EXP.docSeq||2)+1` → `'EXP-2569-'+String(EXP.docSeq).padStart(4,'0')` + comment `<!-- เลขจริงจาก ENG-DOC-NUM.next() ตาม doc_type ใน DOCCFG_BRIEF_F101 — ห้าม feature รันเลขเอง (F003) · สำเนา PDF ผ่าน ENG-DOC-STORE -->`
ตรวจรับ: อนุมัติ → reopen → อนุมัติใบอื่น → เลขไม่ซ้ำ ไม่ reuse · format 4 หลักเสมอ

### 7. FIX-07 hook ตรวจงบ F117 + เพดานสวัสดิการ F102 — HIGH
ตำแหน่ง: wizard ขั้นสรุปก่อนส่ง + `dwView` tab รายละเอียด
สิ่งที่ผิด: c[2] ระบุ "ตรวจงบ (F117) + เพดานสิทธิ์สวัสดิการ" — ไฟล์มีแค่เพดานหมวด HR Config (grep F117=0, สวัสดิการ hook=0 ทั้งที่ contract F102→F101 ctl lock แล้ว)
แก้เป็น: display-only hook 2 จุด — (a) กล่อง "ตรวจงบประมาณ (Budget Control F117 — W7 ยังไม่ dev · hook display-only)" สถานะ mock ผ่าน/เตือน (b) บรรทัดหมวดสวัสดิการ → โชว์ "สิทธิ์คงเหลือจาก F102: ฿X (mock)" + เตือนถ้าเกิน — ห้าม mock หน้าจอ F117/F102 ขึ้นใหม่
ตรวจรับ: หน้าสรุปก่อนส่งเห็น hook ทั้งสอง + note ที่มา

### 8. FIX-08 NTF anchor — HIGH
ตำแหน่ง: `doSubmit` / `doApprove` / `doReject`
สิ่งที่ผิด: chip ntf ประกาศแต่ไม่มี anchor — มีแต่ข้อความ toast
แก้เป็น: comment ต่อจุด: `<!-- NTF: exp.submitted → ผู้อนุมัติขั้นแรก -->` · `<!-- NTF: exp.approved → ผู้เบิก -->` · `<!-- NTF: exp.rejected → ผู้เบิก -->` + หมายเหตุรวม `<!-- doa_pending/doa_result มาจาก DOA engine — ห้ามประกาศซ้ำ (NTF_BRIEF_F101) -->`
ตรวจรับ: ทุก transition แจ้งเตือนมี NTF anchor · ไม่มี doa_* ซ้ำ

### 9. MINOR รวบ (ทำท้ายสุด)
- FIX-09: เรียก `renderIcons()` หลังเติม drawer innerHTML — ปุ่มปิด drawer ต้องมี svg เสมอ (ตอนนี้กล่องเปล่า)
- FIX-10: microcopy "ยิง 7C (FC/EC)" ใน modal approve + toast → เปลี่ยนเป็น "บันทึกเข้า 7C ตาม CSQ_BRIEF_F101" (ห้าม hardcode ชื่อท่อ — รอเคาะ OQ-EXP-02)

## ข้อห้าม
- ห้ามเพิ่ม dependency/CDN · ห้ามแตะ BASE-KIT block · ห้ามเปลี่ยน CI token
- ห้ามลบ comment มติ (A-EXP-04/05, LK-1, UX-06, DSP-02, FN-xx) และ unsupportedNote
- ห้ามแตะ: resolveDoa/DOA_RANGES, submitReady/slot picker, doReject reason flow, over-cap flow, VAT engine, view tabs, a4Doc

## หลังแก้เสร็จ ให้รันเองก่อนส่ง
1. node --check ทุก script block
2. audit.sh → FAIL=0
3. Playwright: pageerror=0 + เคสต่อไปนี้ผ่านครบ:
   - doApprove กับ rejected/cancelled/draft/approved/paid → ไม่เปลี่ยน
   - chain 3 ขั้น → ต้อง 3 คลิกจึง approved · เลขออกครั้งเดียวตอนจบ
   - doReopen เฉพาะ rejected · doCancel เฉพาะ draft
   - role mgr เห็นเงินเต็ม + admin ไม่มีปุ่มอนุมัติ + เรียกตรงไม่ผ่าน
   - เคสเลขซ้ำ (อนุมัติ→reopen→อนุมัติใบอื่น) → เลขไม่ซ้ำ · pad 4 หลัก
   - หน้าสรุปมี hook งบ F117 + สิทธิ์สวัสดิการ F102
แนบผลรัน 3 ข้อนี้กลับมาพร้อมไฟล์ แล้วส่ง re-gate เต็มรอบ (verdict BLOCK)
