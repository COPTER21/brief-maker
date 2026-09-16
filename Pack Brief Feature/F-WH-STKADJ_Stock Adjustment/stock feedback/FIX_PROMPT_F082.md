# คำสั่งแก้ไข F-WH-STKADJ.html (F082 Stock Adjustment — ปรับยอด + อนุมัติ)

คุณจะแก้ HTML prototype single-file ตามรายการนี้เท่านั้น ห้ามแตะส่วนอื่น
ห้าม regenerate ทั้งไฟล์ — แก้เฉพาะจุด (surgical edit)

## บริบท
- ไฟล์: F-WH-STKADJ.html · html-generator-v9 · arch Q-document · F082 W3 (LITE)
- ส่วนที่ผ่านการตรวจแล้ว **ห้ามเปลี่ยนพฤติกรรม** (เป็นต้นแบบ DOA ของ batch):
  - `confirmApprove` เดินทีละขั้น + `canActStep` (role/assignee + SoD ผู้ส่งอนุมัติเองไม่ได้)
  - `doaTiers` ตามมูลค่า (20k/200k/1M) + `renderSignProgress` + BR-10 บังคับเลือกผู้อนุมัติครบ + ปุ่ม loading disabled ใน submitForApproval
  - `nextCode` (global DOC_SEQ + padStart 4) · `openReject` ตีกลับเป็นร่าง + approval_history append-only
  - โครง `doReverse` (ใบใหม่ทิศตรงข้าม + reversalOf/reversedBy + BR-18 กลับซ้ำไม่ได้) — แก้เฉพาะ chain ตามข้อ 3
  - REASONS master + GL mapping · FWD-WIRE declarations · Pattern Q view 4 แท็บ · Esc chain · wizard 5 ขั้น

## รายการแก้ (ทำตามลำดับ)

### 1. FIX-01 doPost precondition guard — CRITICAL
ตำแหน่ง: `function doPost(id,useLatest)`
สิ่งที่ผิด: post ใบ pending (ยังไม่อนุมัติสักขั้น) ได้ → posted + movement เกิดจริง (S1) · post ซ้ำบนใบ posted ได้ (S2 — audit ปนซ้ำ)
แก้เป็น: guard ต้น function — `if(!d || d.status!=='approved'){ showToast('ต้องอนุมัติครบทุกขั้นก่อนผ่านรายการ','warning'); return; }`
ตรวจรับ: doPost กับ draft/pending/posted/cancelled/reversed → ไม่เปลี่ยน ไม่เกิด movement · approved → posted ครั้งเดียว

### 2. FIX-02 cancel เฉพาะก่อนผ่านรายการ — CRITICAL
ตำแหน่ง: callback ใน `openCancel`
สิ่งที่ผิด: ใบ posted ถูก cancel ผ่าน modal ได้ (S2b) — ขัด append-only + ขัด copy ตัวเอง "ยกเลิกก่อนผ่านรายการ"
แก้เป็น: บรรทัดแรกของ callback — `if(!['draft','pending'].includes(d.status)){ showToast('ใบนี้ผ่านรายการแล้ว — ใช้ "กลับรายการ" แทน','warning'); closeModal(); return; }`
ตรวจรับ: posted/reversed/approved/cancelled → ยกเลิกไม่ได้ + toast ชี้ทางกลับรายการ · draft/pending → ได้ตามเดิม

### 3. FIX-03 reversal เดิน DOA ตามมูลค่า — HIGH
ตำแหน่ง: `doReverse`
สิ่งที่ผิด: hardcode `approval_chain:[{WH_LEAD, approved}]` + `status:'posted'` ทันทีเสมอ — ใบมูลค่าสูงกลับรายการข้าม tier (≥20k WH_MGR · ≥200k FIN_MGR · ≥1M DIR)
แก้เป็น: ใบกลับรายการเป็นเอกสารปรับปกติ: `status:'pending'` + `approval_chain = doaTiers(docAbs(rev)).map(t=>({roles:t.roles.slice(), assignee:null, status:'pending', by:null, at:null}))` — ผู้ส่งเลือกผู้อนุมัติผ่าน submit modal เดิม (reuse submitStart/confirmSubmit flow) → อนุมัติครบแล้วค่อยกดผ่านรายการตามปกติ · คง reversalOf/reversedBy + BR-18 · **ห้าม auto-post** · ถ้ามีมติ fast-track ให้ comment อ้างมติแทน (OQ-ADJ-01)
ตรวจรับ: reverse ใบมูลค่า ≥20k → ใบกลับรายการ pending รอ chain ตาม tier · อนุมัติครบ + post แล้ว movement ทิศตรงข้ามเกิด · กลับซ้ำไม่ได้เหมือนเดิม

### 4. FIX-04 trace กลับใบนับ (c[4]) — HIGH
ตำแหน่ง: wizard `renderStep1` (แหล่งที่มา) + `renderViewDrawer` ข้อมูลเอกสาร + `buildDoc`
สิ่งที่ผิด: c[4] "trace กลับใบนับที่เป็นต้นเรื่อง" — grep ใบนับ/F084/F086 = 0 ทั้งไฟล์
แก้เป็น:
- data: เพิ่ม `ref_count_doc` (nullable) + mock ใบนับ 2-3 ใบ `[{code:'CNT-2026-0012', src:'F084 ตรวจนับใหญ่'}, {code:'CYC-2026-0031', src:'F086 นับหมุนเวียน'}]`
- wizard ขั้น 1: ตัวเลือกแหล่งที่มา — "ปรับตรง" (default) หรือ "จากใบนับ" + combobox เลือกใบนับ (display-only ไม่เปิดหน้าใบนับ)
- view drawer: แถว "ใบนับต้นเรื่อง: CNT-2026-0012 (F084)" เมื่อมี ref
- comment: `<!-- CONTRACT: F084 (ตรวจนับใหญ่) + F086 (cycle count) → F082 (flow — ส่วนต่างจากการนับสร้างใบปรับ + ref กลับใบนับ) -->`
ตรวจรับ: สร้างใบจากใบนับ → view โชว์ ref · ปรับตรงไม่บังคับ · ไม่มีหน้าจอใบนับเกิดใหม่

### 5. FIX-05 CSQ + NTF anchors — HIGH
ตำแหน่ง: `doPost` · `doReverse` · `confirmApprove`/`openReject` · `submitForApproval`
สิ่งที่ผิด: chip ◆csq + 🔔ntf ประกาศ แต่ grep = 0 ทั้งคู่
แก้เป็น:
- CSQ ที่ doPost: audit line "บันทึกเข้า 7C ตาม CSQ_BRIEF_F082" + comment `<!-- CSQ: adj.posted → ท่อตาม CSQ_BRIEF_F082 (มูลค่าปรับกระทบต้นทุน/บัญชี — รอเคาะ OQ-ADJ-02) · ห้ามประกาศ OC/DC ซ้ำ -->`
- CSQ ที่ doReverse: comment `<!-- CSQ: adj.reversed → reversal_of ผูก event ใบเดิม (BR-CSQ-04) -->`
- NTF comments: doSubmit/confirmApprove/openReject/doPost — `<!-- NTF: adj.posted → ผู้สร้างใบ + บัญชี · doa_pending/doa_result มาจาก DOA engine ห้ามประกาศซ้ำ (NTF_BRIEF_F082) -->`
ตรวจรับ: csq anchor ≥2 จุด · ntf ครบทุก transition · ไม่ประกาศท่อ/event สงวน

### 6. FIX-06 doccfg anchor — HIGH
ตำแหน่ง: `nextCode`
แก้เป็น: comment `<!-- เลขจริงจาก ENG-DOC-NUM.next() ตาม doc_type ADJ ใน DOCCFG_BRIEF_F082 — ห้าม feature รันเลขเอง (F003) · สำเนา PDF ผ่าน ENG-DOC-STORE -->` (logic เดิมคงไว้ ถูกแล้ว)
ตรวจรับ: comment hook ครบ

### 7. MINOR รวบ (ทำท้ายสุด)
- FIX-07: `state._busy` guard (pattern F101 — 500ms) ครอบ `confirmApprove`, `doPost`, callbacks ของ reasonModal
- FIX-08: wizard stepper เปลี่ยนเป็น component กลาง `.stepper > .step-dot` (Rule #47/#47.1)
- FIX-09 (กติกา demo-only จาก BA): chip `FWD-WIRE: …` + การอ้าง BR-xx ใน toast/modal desc → ครอบ class `demo-only` + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` · label ผู้ใช้ "(ร่าง — ยังไม่ออกเลขที่ · ออกโดย ENG-DOC-NUM ตอนส่งอนุมัติ)" → "(ร่าง — ออกเลขอัตโนมัติเมื่อส่งอนุมัติ)" · ทดสอบ `.demo-only{display:none}` แล้วไม่เหลือศัพท์ dev (ENG-DOC-NUM/FWD-WIRE/BR-xx) และ layout ไม่พัง

## ข้อห้าม
- ห้ามเพิ่ม dependency/CDN · ห้ามแตะ BASE-KIT · ห้ามเปลี่ยน CI token
- ห้ามแตะ: canActStep/confirmApprove step logic, doaTiers, nextCode logic, openReject flow, REASONS master, BR-18 guard, wizard validation, Esc chain
- ห้ามลบ comment BR-xx / FWD-WIRE (ย้ายเข้า demo-only ได้ แต่เนื้อหาคงไว้)

## หลังแก้เสร็จ ให้รันเองก่อนส่ง
1. node --check ทุก script block
2. audit.sh → FAIL=0 (WARN #47 ต้องหาย)
3. Playwright: pageerror=0 + เคสต่อไปนี้ผ่านครบ:
   - doPost กับ draft/pending/posted → block · approved → posted ครั้งเดียว
   - cancel ใบ posted → block + toast ชี้กลับรายการ
   - reverse ใบ ≥20k → ใบกลับรายการ pending รอ chain ตาม tier (ไม่ auto-post)
   - ใบจากใบนับ → view โชว์ ref ใบนับ
   - grep: CSQ ≥2 · NTF ≥3 · DOCCFG/ENG-DOC-NUM comment ครบ
   - inject `.demo-only{display:none}` → ไม่เหลือศัพท์ dev + layout ปกติ
แนบผลรันกลับมาพร้อมไฟล์ แล้วส่ง re-gate เต็มรอบ (verdict BLOCK)
