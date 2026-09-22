# คำสั่งแก้ไข F-ACC-CN_credit-note.html (F096 Credit Note — ใบลดหนี้ลูกค้า)

คุณจะแก้ HTML prototype single-file ตามรายการนี้เท่านั้น ห้ามแตะส่วนอื่น
ห้าม regenerate ทั้งไฟล์ — แก้เฉพาะจุด (surgical edit)

## บริบท
- ไฟล์: F-ACC-CN_credit-note.html · Q-DOC KERNEL W5-LITE (html-generator-v9 Pattern Q + B2 v2) · F096 · dec ครบ 5
- ส่วนที่ผ่านการตรวจแล้ว **ห้ามเปลี่ยนพฤติกรรม**:
  - `confirmApprove` ทีละขั้น + `canActStep` SoD · `resolveDoa` 3 tier · slot ไม่ prefill · `approveGuard` re-check ยอดคงค้างขั้นสุดท้าย
  - `cnApplied`/`cnHeld`/`invAvailable`/`lineRoom`/`cnOver`/`lineOver` — กันลดหนี้เกินคงค้าง
  - `onFinalApprove` ออกเลขตอนอนุมัติครบ · `nextCode` max-based · `CN_REASONS` mode qty/price + RET บังคับ SR
  - แท็บใบแจ้งหนี้อ้างอิง·ภาษีขาย + JE จำลอง · PDF (ม.86/10 ครบ) · B2 line editor · busy() · Esc chain

## รายการแก้ (ทำตามลำดับ)

### 1. FIX-01 cancel เฉพาะก่อนออกเลข — CRITICAL
ตำแหน่ง: callback ใน `openCancelCN` + ปุ่มใน view
สิ่งที่ผิด: ใบ sent (CN-2026-0021 ออกเลขแล้ว) ถูกยกเลิกผ่าน modal ได้ → ยอด AR/VAT ที่ลดเด้งกลับ (C1)
แก้เป็น: บรรทัดแรกของ callback (และ openCancelCN เอง): `if(!['draft','pending_approval'].includes(s.status)){ closeModal(); return showToast('ใบลดหนี้ที่ออกเลขแล้วยกเลิกไม่ได้ — ใช้ "ออกเอกสารแก้ไข"','warning'); }` · ปุ่มยกเลิกไม่ render บน approved/sent
ตรวจรับ: cancel กับ approved/sent → block + toast · draft/pending → ได้ · เลขที่ออกแล้วยังอยู่ในทะเบียน

### 2. FIX-02 send เฉพาะ approved — CRITICAL
ตำแหน่ง: `openSendCN`
สิ่งที่ผิด: ส่งใบ draft (ไม่มีเลข) ให้ลูกค้าได้ → sent (C2)
แก้เป็น: `if(s.status!=='approved' && s.status!=='sent'){ return showToast('ต้องอนุมัติครบก่อนส่ง','warning'); }` · ถ้า `sent` อยู่แล้ว → modal หัวข้อ "ส่งสำเนาซ้ำ" + audit "ส่งสำเนาซ้ำ" ไม่เปลี่ยน status/sentAt เดิม
ตรวจรับ: send draft/pending/cancelled → block · approved → sent · sent → บันทึกสำเนาซ้ำ

### 3. FIX-03 submit เฉพาะ draft — CRITICAL
ตำแหน่ง: `confirmSubmit` + `openSubmitModal`
สิ่งที่ผิด: ใบ approved ส่งอนุมัติซ้ำได้ → chain ใหม่ทับของเดิม (C4)
แก้เป็น: ต้นทั้งสอง function `if(s.status!=='draft') return showToast('ส่งอนุมัติได้เฉพาะฉบับร่าง','warning');`
ตรวจรับ: submit กับ pending/approved/sent/cancelled → block · chain/code เดิมไม่เปลี่ยน

### 4. FIX-04 legal_basis ตามประกาศอธิบดีฯ — HIGH
ตำแหน่ง: `CN_REASONS` · `renderStep2` · PDF เหตุผล
สิ่งที่ผิด: เหตุผล 4 ข้อไม่ผูกกับเหตุตามกฎหมาย · "ส่วนลดภายหลังการขาย" ทั่วไปไม่ใช่เหตุที่ประกาศฯ ให้ออกใบลดหนี้
แก้เป็น:
- เพิ่ม `legal_basis` ต่อเหตุผล เช่น RET → "รับคืนสินค้า" · PRICE → "คำนวณราคาสินค้าผิดพลาดสูงกว่าที่เป็นจริง" · QTY → "จัดส่งสินค้าขาดจำนวน/คิดเกินที่ส่งจริง" · DISC → เปลี่ยนเป็น "ลดราคาเพราะสินค้าผิดข้อกำหนด/ชำรุด" (เลือกเหตุย่อยบังคับ) — ส่วนลดทางการค้าล้วน → ไม่ให้เลือกเป็นใบลดหนี้ภาษี + ข้อความแนะนำ (รอเคาะ OQ-CN-01)
- ขั้น 2 แสดง "เหตุตามกฎหมาย: …" ใต้ตัวเลือก · PDF บรรทัดเหตุผล = "[legal_basis] — [รายละเอียด]"
- comment `<!-- LEGAL: เหตุตามประกาศอธิบดีกรมสรรพากร (VAT ฉบับที่ 82) — รายการสุดท้ายรอบัญชียืนยัน OQ-CN-01 -->`
ตรวจรับ: ทุกเหตุผลมี legal_basis · PDF พิมพ์ · เหตุที่ไม่เข้าข่ายเลือกไม่ได้

### 5. FIX-05 anchors doccfg / csq / ntf / contract — HIGH
- `nextCode`: `<!-- เลขจริงจาก ENG-DOC-NUM.next() ตาม doc_type CN ใน DOCCFG_BRIEF_F096 — ห้าม feature รันเลขเอง (F003) · สำเนา PDF ผ่าน ENG-DOC-STORE -->`
- `onFinalApprove`: `<!-- CSQ: cn.issued → AC (ลด AR + กลับภาษีขาย) / FC ตาม CSQ_BRIEF_F096 (รอเคาะ OQ-CN-03) · DC จาก DOA engine ห้ามซ้ำ -->` + audit line "บันทึกเข้า 7C ตาม CSQ_BRIEF_F096"
- NTF: `onFinalApprove` → `<!-- NTF: cn.issued → ผู้สร้าง + AR -->` · `openSendCN` → `<!-- NTF: cn.sent → ลูกค้า (ช่องทางที่ตั้งไว้) -->` · `<!-- doa_pending/doa_result มาจาก DOA engine ห้ามประกาศซ้ำ (NTF_BRIEF_F096) -->`
- header dep comment: `<!-- CONTRACT: F090 → F096 (flow — รับคืน → ใบลดหนี้) · F096 → F094 AR Invoice (data — ลดยอดคงค้าง ar_open_item) · JE → F093 (flow) -->`
ตรวจรับ: anchor ครบ doccfg/csq ≥1/ntf ≥2/contract ระบุรหัส

### 6. FIX-06 เส้นทางแก้ใบที่ออกเลขแล้ว — HIGH
ตำแหน่ง: ปุ่มใน view (approved/sent)
แก้เป็น: ปุ่ม "ออกเอกสารแก้ไข" (display-only) → modal อธิบาย 2 ทาง: ใบเพิ่มหนี้ลูกค้า (feature อื่น) / ใบลดหนี้ใหม่อ้างใบนี้ · เลือกแล้ว mark `s.voided_by='(รอเอกสารทดแทน)'` + audit ไม่เปลี่ยน status ไม่ถอนยอด · comment `<!-- flow แก้เอกสารภาษีที่ออกแล้ว รอเคาะ OQ-CN-02 -->`
ตรวจรับ: approved/sent มีปุ่มออกเอกสารแก้ไข · ไม่มีปุ่มยกเลิก

### 7. MINOR รวบ (ทำท้ายสุด)
- FIX-07: stepper → `.stepper > .step-dot` (Rule #47) · ส่วนลดท้ายบิล segmented ฿/% ตาม #99 · font-size residual
- FIX-08: `state._busy` (pattern F101) ครอบ `confirmApprove` / `confirmSubmit` / callbacks ของ reasonModal
- FIX-09 (กติกา demo-only): persona strip · chip/ข้อความ "[ASSUMED contract]" · "จำลอง · รอเชื่อม F093" · "template ตาม thai-doc-pdf-generator" · badge DEMO → class `demo-only` + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` · ทดสอบ `.demo-only{display:none}` → ไม่เหลือศัพท์ dev + layout ปกติ

## ข้อห้าม
- ห้ามเพิ่ม dependency/CDN · ห้ามแตะ BASE-KIT · ห้ามเปลี่ยน CI token
- ห้ามแตะ: canActStep/confirmApprove/approveGuard/resolveDoa, cnApplied/cnHeld/lineRoom, onFinalApprove, nextCode logic, PDF ม.86/10 fields, B2 engine, VAT tab
- ห้ามทำให้ใบที่ออกเลขแล้วหายจากทะเบียนหรือถอนยอด AR ย้อนหลังโดยไม่มีเอกสารทดแทน

## หลังแก้เสร็จ ให้รันเองก่อนส่ง
1. node --check
2. audit.sh → FAIL=0 (WARN #47/#99 หาย)
3. Playwright: pageerror=0 + เคส:
   - cancel ใบ approved/sent → block · draft/pending → ได้
   - send draft → block · approved → sent · sent → สำเนาซ้ำ
   - submit ใบ approved → block · chain/code เดิมคงอยู่
   - ทุกเหตุผลมี legal_basis + PDF พิมพ์
   - grep: ENG-DOC-NUM ≥1 · CSQ ≥1 · NTF ≥2 · F094 ≥1
   - approve ทีละขั้น/SoD/re-check ยอดคงค้างยังทำงาน
   - inject `.demo-only{display:none}` → สะอาด
แนบผลรันกลับมาพร้อมไฟล์ แล้วส่ง re-gate เต็มรอบ (verdict BLOCK)
