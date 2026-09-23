# คำสั่งแก้ไข F-ACC-DN_debit-note.html (F097 Debit Note — ใบลดหนี้ผู้ขาย)

คุณจะแก้ HTML prototype single-file ตามรายการนี้เท่านั้น ห้ามแตะส่วนอื่น
ห้าม regenerate ทั้งไฟล์ — แก้เฉพาะจุด (surgical edit)

## บริบท
- ไฟล์: F-ACC-DN_debit-note.html · Q-DOC KERNEL W5-LITE · F097 · dec ครบ 5
- ส่วนที่ผ่านการตรวจแล้ว **ห้ามเปลี่ยนพฤติกรรม** (พิสูจน์ผ่าน bypass ครบ):
  - status guards ใน openCancelDN / openSendDN / confirmSubmit + callbacks · `busyGate` · `.demo-only` ที่ครอบแล้ว
  - canActStep SoD · confirmApprove ทีละขั้น · approveGuard · resolveDoa 3 tier · slot ไม่ prefill
  - dnApplied/dnHeld/lineRoom · onFinalApprove ออกเลข · nextCode · DN_REASONS + RTV บังคับ
  - PDF ม.86/10 + ช่องใบลดหนี้ผู้ขาย · ภาษีซื้อคิดฐานใหม่ · ปิดทางเลือกไม่อ้างใบตั้งหนี้ (OQ-DN-01)

## รายการแก้ (ทำตามลำดับ)

### 1. FIX-01 เครดิตคงเหลือกับผู้ขาย (c[3]) — HIGH
ตำแหน่ง: `invAvailable` / `dnOver` / `step3Block` · view drawer summary · list stats
สิ่งที่ผิด: available = outstanding − held (หัก paid) → ใบจ่ายครบ (API-2026-0038) ออก DN ไม่ได้ · ไม่มี vendor credit balance
แก้เป็น:
- เพดานลดหนี้ = `invGrand − dnApplied − dnHeld` (ไม่หัก paid) → `dnOver` ใช้ค่านี้
- ตอนอนุมัติครบ (onFinalApprove): `applyToAp = min(grand, outstanding)` · `vendorCredit = grand − applyToAp` เก็บใน record
- view summary แสดง "หักจากหนี้ค้าง ฿X · เครดิตคงเหลือกับผู้ขาย ฿Y"
- เพิ่ม card ใน list stats "เครดิตคงเหลือรายผู้ขาย" + section display-only (ผู้ขาย · ยอด · ที่มา DN) + comment `<!-- flow การใช้เครดิต (หักใบถัดไป/ขอคืนเงิน) รอเคาะ OQ-DN-06 -->`
ตรวจรับ: ใบจ่ายครบออก DN ได้ไม่เกินมูลค่าใบ · summary แยก 2 ยอด · card เครดิตคงเหลือมีค่า

### 2. FIX-02 ภาษีซื้อยึดใบลดหนี้ผู้ขาย — HIGH
ตำแหน่ง: `blankData` / wizard ขั้น 2 (ช่อง vendorCn) · แท็บใบตั้งหนี้อ้างอิง·ภาษีซื้อ · onFinalApprove
สิ่งที่ผิด: เดือนภาษียึด dnDate ของเรา [ASSUMED OQ-DN-05] · vendorCn optional ไม่มีวันที่
แก้เป็น:
- เพิ่ม `vendorCnDate` (input date) ข้าง vendorCn · ทั้งคู่ optional ตอนสร้าง แต่คุมภาษี:
- แท็บภาษีซื้อ: ถ้าไม่มี vendorCn+vendorCnDate → สถานะ "รอใบลดหนี้ผู้ขาย — ยังไม่ลดภาษีซื้อใน ภ.พ.30" (chip เตือน) · มีครบ → เดือนภาษี = เดือนของ vendorCnDate · ฐาน/ภาษีที่ลดแสดงตามเดิม
- ปุ่ม "บันทึกใบลดหนี้ผู้ขาย" บน view ของใบ approved/sent (กรอก vendorCn+วันที่ ภายหลังได้ · audit)
- ตัดข้อความ "[ASSUMED OQ-DN-05]" ออกจากที่ผู้ใช้เห็น → comment `<!-- LEGAL: ผู้ซื้อลดภาษีซื้อในเดือนที่ได้รับใบลดหนี้ (ม.82/10) — ยืนยัน OQ-DN-05 -->`
ตรวจรับ: DN ไม่มี vendorCn → AP ลดได้ / ภาษีซื้อ "รอเอกสาร" · ใส่ครบ → เดือนภาษีตามวันที่ได้รับ

### 3. FIX-03 anchors — HIGH
- `nextCode`: `<!-- เลขจริงจาก ENG-DOC-NUM.next() ตาม doc_type DN ใน DOCCFG_BRIEF_F097 — ห้าม feature รันเลขเอง (F003) · สำเนา PDF ผ่าน ENG-DOC-STORE -->`
- `onFinalApprove`: `<!-- CSQ: dn.issued → AC (ลด AP) · dn.vat_applied (เมื่อมีใบลดหนี้ผู้ขาย) → AC ภาษีซื้อ ตาม CSQ_BRIEF_F097 (รอเคาะ OQ-DN-07) · DC จาก DOA engine ห้ามซ้ำ -->` + audit "บันทึกเข้า 7C ตาม CSQ_BRIEF_F097"
- NTF: `<!-- NTF: dn.issued → ผู้สร้าง + AP · dn.sent → ผู้ขาย · doa_pending/doa_result มาจาก DOA engine ห้ามซ้ำ (NTF_BRIEF_F097) -->`
- header dep comment: `<!-- CONTRACT: F080 RTV → F097 (flow — คืนของ → ใบลดหนี้ผู้ขาย) · F097 → F095 AP Invoice (data — ลดยอดหนี้ตั้งซื้อเดิม) · JE → F093 (flow) -->`
ตรวจรับ: grep ENG-DOC-NUM ≥1 · CSQ ≥1 · NTF ≥2 · F080 ≥1 · F095 ≥1

### 4. MINOR รวบ (ทำท้ายสุด)
- FIX-04 (demo-only จุดที่เหลือ): "template ตาม thai-doc-pdf-generator" หัว PDF tab · "(DEMO)" ใน toast สลับบทบาท · "[ASSUMED …]" ที่ผู้ใช้เห็น → ครอบ `demo-only` หรือย้ายเป็น comment · ทดสอบ `.demo-only{display:none}` → สะอาด
- FIX-05: font-size base-kit residual — ตามสะดวก

## ข้อห้าม
- ห้ามเพิ่ม dependency/CDN · ห้ามแตะ BASE-KIT · ห้ามเปลี่ยน CI token
- ห้ามคลาย guard ที่มีอยู่ (cancel/send/submit/approve) · ห้ามแตะ approveGuard, resolveDoa, lineRoom, nextCode logic, PDF fields, B2 engine
- ห้ามให้ภาษีซื้อลดใน ภ.พ.30 โดยไม่มี vendorCn+วันที่

## หลังแก้เสร็จ ให้รันเองก่อนส่ง
1. node --check
2. audit.sh → FAIL=0
3. Playwright: pageerror=0 + เคส:
   - ใบจ่ายครบ (API-2026-0038) ออก DN ได้ · summary แสดงเครดิตคงเหลือ · card รายผู้ขายมีค่า
   - DN ไม่มี vendorCn → ภาษีซื้อ "รอเอกสาร" · ใส่ vendorCn+วันที่ → เดือนภาษีเปลี่ยนตาม
   - guards เดิม: cancel sent/send draft/resubmit approved/approve unauthorized → block ทั้งหมด
   - grep anchors ครบตามข้อ 3
   - inject `.demo-only{display:none}` → ไม่เหลือศัพท์ dev
แนบผลรันกลับมาพร้อมไฟล์ แล้วส่ง re-gate (รอบสั้น)
