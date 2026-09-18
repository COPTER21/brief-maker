# คำสั่งแก้ไข F-WH-STKTRF.html (F083 Stock Transfer — ย้ายคลัง/สาขา)

คุณจะแก้ HTML prototype single-file ตามรายการนี้เท่านั้น ห้ามแตะส่วนอื่น
ห้าม regenerate ทั้งไฟล์ — แก้เฉพาะจุด (surgical edit)

## บริบท
- ไฟล์: F-WH-STKTRF.html · html-generator-v9 · arch Q-document · F083 W3 (LITE) · สองขา issue/receive
- ส่วนที่ผ่านการตรวจแล้ว **ห้ามเปลี่ยนพฤติกรรม**:
  - `doShip` guard approved + re-check ยอดคงเหลือต้นทางก่อนของขยับ + confirm dialog
  - `confirmApprove` ทีละขั้น + `canActStep` (role/assignee + SoD) + loading disabled
  - `resolveDoa` 2 มิติ (intra/inter) + `resolveShortageDoa` ตามมูลค่าส่วนต่าง
  - `openCancelModal` guard สถานะ + ชี้ทาง · `openReturnModal` guard คลังปลายทาง (ME.wh)
  - validations ใน `confirmReceive` (รับเกิน block + ชี้ใบปรับยอด · binActual บังคับ · diffReason บังคับ) — คงไว้ทั้งหมด แล้วเพิ่ม guard ตามข้อ 1
  - B2 engine (totals() เดียว · vat_mode none) · `nextCode` max-based · in-transit tab + aging · SoD ใน confirmShortage (ผู้ส่งออกเซ็นไม่ได้) · หลักฐานแนบบังคับ

## รายการแก้ (ทำตามลำดับ)

### 1. FIX-01 confirmReceive guard + re-derive — CRITICAL
ตำแหน่ง: `confirmReceive` (+ `openReceiveModal`)
สิ่งที่ผิด: ไม่เช็คสถานะ + เชื่อ receiveState จาก UI — ใบ closed ถูกรับซ้ำ received 100→105 (T6)
แก้เป็น:
- guard ต้น function: `if(['in_transit','partial'].indexOf(s.status)===-1){ showToast('ใบนี้ไม่อยู่ในสถานะรอรับ','warning'); return; }` (ใส่ที่ openReceiveModal ด้วย)
- ใน loop: re-derive `var rem=lineRemaining(r.ref);` จาก doc จริง แล้ว `r.take=Math.min(r.take, rem);` — ห้ามใช้ r.rem จาก state ตรง ๆ
ตรวจรับ: receive กับ closed/closed_diff/moved/draft/pending → block · in_transit/partial รับได้ไม่เกินคงเหลือจริง · validations เดิมทำงานครบ

### 2. FIX-02 reverse guard สถานะ + เดิน DOA — CRITICAL
ตำแหน่ง: `openReverseModal`
สิ่งที่ผิด: เช็คแค่ reversedBy — reverse ใบ pending_approval (ของยังไม่ขยับ) ได้ → ใบ reversal เป็น moved + movement ผี (T5) · chain hardcode [wh_supervisor approved] + auto-moved ข้าม DOA
แก้เป็น:
- guard: `if(['moved','closed','closed_diff'].indexOf(s.status)===-1){ showToast('กลับรายการได้เฉพาะใบที่ของขยับแล้ว — ใบค้างระหว่างทางใช้ "ตีกลับคืนต้นทาง"','warning'); return; }`
- ใบ reversal: `status:'pending_approval'` + `approval_chain = resolveDoa(rev).steps.map(...pending, assignee:null)` — ผู้ส่งเลือกผู้อนุมัติผ่าน submit modal เดิม → อนุมัติครบ → ship ตามจังหวะปกติ · **ห้าม auto-moved** · ห้าม pre-fill received/binActual (ค่าพวกนี้เกิดตอน ship/receive จริง) · fast-track ต้องมีมติ (comment OQ-TRF-01)
- คง reversalOf/reversedBy + กลับซ้ำไม่ได้
ตรวจรับ: reverse ใบ draft/pending/in_transit/partial → block + toast ชี้ทาง · ใบ moved/closed → reversal pending รอ chain ตามมูลค่า · ship/receive ของใบ reversal เดินจังหวะปกติ

### 3. FIX-03 shortage chain ต้องรอผู้อนุมัติจริง — HIGH
ตำแหน่ง: `confirmShortage` (+ ปุ่มอนุมัติใน view สำหรับ shortage)
สิ่งที่ผิด: เลือกผู้อนุมัติแล้ว set approved/by/at แทนทุกคนทันที (T4) — ผู้อนุมัติไม่ได้กระทำ
แก้เป็น:
- `shortage_chain = slots.map(st=>({roles, assignee:st.assignee, status:'pending', by:null, at:null}))` + `shortage_status:'pending'` — ใบคง partial + audit "ส่งขออนุมัติตัดส่วนต่าง"
- เพิ่มปุ่ม "อนุมัติตัดส่วนต่าง" ใน view (แสดงเมื่อ shortage_status pending และ ME คือ assignee ขั้น current — reuse canActStep logic กับ shortage_chain) → อนุมัติทีละขั้น + at · ครบสายค่อย: write-off (writtenOff/movement) + `closed_diff` + audit
- SoD เดิม (ผู้ส่งออกเซ็นไม่ได้) + หลักฐานแนบบังคับ คงไว้
ตรวจรับ: ยืนยันตัดส่วนต่าง → ใบคง partial + chain pending · ผู้อนุมัติจริงกดครบสาย → closed_diff · ทุกขั้นมี at

### 4. FIX-04 CSQ + NTF anchors — HIGH
ตำแหน่ง: `doShip` · `confirmReceive` (จุดปิดใบ) · จุด write-off · `openReverseModal`
แก้เป็น: comment anchors ตาม pattern F082:
- `<!-- CSQ: trf.shipped / trf.received / trf.shortage_writeoff → ท่อตาม CSQ_BRIEF_F083 (รอเคาะ OQ-TRF-02) · reverse ผูก reversal_of (BR-CSQ-04) · ห้ามประกาศ OC/DC ซ้ำ -->`
- `<!-- NTF: trf.shipped → คลังปลายทาง · trf.received/trf.shortage → ผู้ส่ง+ต้นทาง · doa_pending/doa_result มาจาก DOA engine ห้ามประกาศซ้ำ (NTF_BRIEF_F083) -->`
ตรวจรับ: csq anchor ≥3 · ntf ครบ transition สำคัญ

### 5. FIX-05 doccfg anchor — HIGH
ตำแหน่ง: `nextCode`
แก้เป็น: comment `<!-- เลขจริงจาก ENG-DOC-NUM.next() ตาม doc_type TRF ใน DOCCFG_BRIEF_F083 — ห้าม feature รันเลขเอง (F003) · สำเนา PDF ผ่าน ENG-DOC-STORE -->` (logic เดิมถูกแล้ว คงไว้)

### 6. MINOR รวบ (ทำท้ายสุด)
- FIX-06: `state._busy` (pattern F101 · 500ms) ครอบ `doShip` และ callbacks ของ reasonModal (cancel/return/reverse/reject)
- FIX-07: font-size base-kit residual — แก้ตามสะดวก
- FIX-08 (กติกา demo-only): FWD-WIRE chips/audit notes ทุกจุด + "ENG-DOC-NUM" ใน label เลขที่ + BR refs ใน copy → ครอบ class `demo-only` + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` · label เปลี่ยนเป็น "(ร่าง — ออกเลขอัตโนมัติเมื่อส่งอนุมัติ)" · ทดสอบ `.demo-only{display:none}` ไม่เหลือศัพท์ dev + layout ปกติ

## ข้อห้าม
- ห้ามเพิ่ม dependency/CDN · ห้ามแตะ BASE-KIT · ห้ามเปลี่ยน CI token
- ห้ามแตะ: doShip re-check ยอด, canActStep/confirmApprove, resolveDoa/resolveShortageDoa, openCancelModal/openReturnModal guards, B2 totals(), nextCode logic, in-transit tab/aging, validations เดิมใน confirmReceive/confirmShortage
- ห้ามลบ comment BR/FWD-WIRE (ย้ายเข้า demo-only ได้ เนื้อหาคงไว้)

## หลังแก้เสร็จ ให้รันเองก่อนส่ง
1. node --check ทุก script block
2. audit.sh → FAIL=0
3. Playwright: pageerror=0 + เคส:
   - receive ใบ closed → block · in_transit รับได้ไม่เกินคงเหลือจริง (inject state แล้วต้องถูก clamp)
   - reverse ใบ pending/in_transit → block · ใบ moved → reversal pending + เดิน chain ตามมูลค่า
   - shortage → chain pending · ผู้อนุมัติจริงกดครบค่อย closed_diff
   - grep: CSQ ≥3 · NTF ≥3 · DOCCFG comment ครบ
   - inject `.demo-only{display:none}` → สะอาด + layout ปกติ
แนบผลรันกลับมาพร้อมไฟล์ แล้วส่ง re-gate เต็มรอบ (verdict BLOCK)
