# คำสั่งแก้ไข consent-pdpa.html (F058 Consent PDPA — opt-in/out ลูกค้า)

คุณจะแก้ HTML prototype single-file ตามรายการนี้เท่านั้น ห้ามแตะส่วนอื่น
ห้าม regenerate ทั้งไฟล์ — แก้เฉพาะจุด (surgical edit)

## บริบท
- ไฟล์: consent-pdpa.html · มาตรฐาน html-generator-v9 · F058 W1 · S1 (security ก่อน production Credence)
- ส่วนที่ผ่านการตรวจแล้ว **ห้ามเปลี่ยนพฤติกรรม**:
  - `emitConsequence` envelope (idempotency_key BR-CSQ-02 · reversal_of BR-CSQ-04 · invisible sink LOCK-CSQ-04/05/06)
  - `resolveConsent` default-deny + stale/expired block + reason strings
  - evidence block + policyVersion ณ ตอนตอบ ใน `applyAnswers` · `supersede` (BR-01)
  - `doPublishVersion` บังคับแนบเอกสาร + stale count · `reConsent` batch · BR-14/17 ปิด purpose เก็บหลักฐาน
  - recipient view (verify ตัวตน + บังคับเลือกครบ) · BR-06 panel · `viewPolicy(code, ver)` · QR/link/PDF form

## รายการแก้ (ทำตามลำดับ)

### 1. FIX-01 guard สถานะคำขอ — ตอบได้ครั้งเดียว — CRITICAL
ตำแหน่ง: `applyAnswers` (จุดเดียวคุมทั้ง answerRequest + submitRecipient)
สิ่งที่ผิด: คำขอ answered ถูกตอบซ้ำได้ไม่จำกัด — แต่ละครั้งสร้าง consent ใหม่ + supersede หลักฐานเดิม (B1: consents 9→11 จากคำขอเดียว) และสถานะคำขอไม่ถูกปิด
แก้เป็น:
- ต้น applyAnswers: `if(!['draft','pending'].includes(r.status)){ showToast('คำขอนี้ปิดแล้ว — ตอบซ้ำไม่ได้','warning'); return; }`
- จบการตอบ: `r.status='answered'; r.answeredAt=new Date().toISOString();`
- `recipientViewHTML`: ถ้าคำขอไม่ใช่ draft/pending → แสดงหน้าสถานะปิด "คำขอนี้ตอบแล้วเมื่อ [เวลา] — หากต้องการเปลี่ยนแปลง ติดต่อบริษัท" แทนฟอร์ม (ลูกค้าเปิดลิงก์ซ้ำ)
- การเปลี่ยนใจ = withdraw หรือคำขอใหม่ตาม flow เดิม (ห้ามทำ flow แก้คำตอบเอง — แขวน OQ-CNS-01)
ตรวจรับ: answerRequest/submitRecipient กับ answered/closed/expired → consent ไม่เพิ่ม + toast · pending ตอบครั้งเดียวแล้วปิด · recipient view ของคำขอที่ปิดแสดงหน้าสถานะ

### 2. FIX-04 เพิ่ม _busy ทุก mutation — HIGH
ตำแหน่ง: `submitReqCreate` · `submitRecipient` · `doWithdraw` · `doPublishVersion` · `doClosePurpose`
สิ่งที่ผิด: ไม่มี _busy ทั้งไฟล์ — double submit สร้างคำขอซ้ำ (B8: requests 4→6)
แก้เป็น: pattern F101: `if(state._busy)return; state._busy=true; … setTimeout(function(){state._busy=false;},500);` + ปุ่ม submit ใส่ loading state (Rule #44 — icon loader-2 ระหว่างรอ)
ตรวจรับ: double-click ทุก mutation → เกิดผลครั้งเดียว · audit WARN #44 หาย

### 3. FIX-05 guard สถานะย่อย — HIGH
ตำแหน่ง: `doWithdraw` · `sendVia`
สิ่งที่ผิด: withdraw ซ้ำบน consent withdrawn ได้ (history+CSQ ซ้ำ) · sendVia บนคำขอ answered ได้
แก้เป็น: doWithdraw guard `if(effStatus(c)!=='granted'){ showToast('รายการนี้ไม่อยู่ในสถานะยินยอม','warning'); return; }` · sendVia guard `if(!['draft','pending'].includes(r.status)){ showToast('คำขอนี้ปิดแล้ว','warning'); return; }`
ตรวจรับ: withdraw ได้เฉพาะ granted · ส่งได้เฉพาะ draft/pending

### 4. FIX-02 mirror persona guard ใน function — HIGH
ตำแหน่ง: `applyAnswers` · `doWithdraw` · `doPublishVersion` · `doClosePurpose` · `submitReqCreate` · `sendVia`
สิ่งที่ผิด: PERM() ใช้แค่ render ปุ่ม — persona Auditor เรียก answerRequest ตรงสำเร็จ (B4)
แก้เป็น: ต้นแต่ละ function เช็ค flag ที่ตรง: sign→applyAnswers · withdraw→doWithdraw · purpose→doPublishVersion/doClosePurpose · reqCreate→submitReqCreate · send→sendVia — ไม่ผ่าน `showToast('สิทธิ์ไม่พอสำหรับบทบาทนี้','warning'); return;` + comment `<!-- SEC: บทบาทจริงจากล็อกอิน · prototype mirror sec.can() -->`
ตรวจรับ: Auditor เรียกทุก mutation ตรง → state ไม่เปลี่ยน · Officer/DPO ตามสิทธิ์เดิม (จัดการวัตถุประสงค์ = DPO เท่านั้น)

### 5. FIX-03 snapshot เวอร์ชันนโยบายตอนส่ง — HIGH (โจทย์ "ดูเนื้อหาที่ส่งไปได้")
ตำแหน่ง: `sendVia` · `reqViewDrawer` (policyRows)
สิ่งที่ผิด: sends เก็บแค่ {ch, at} และ BR-06 panel render p.currentVer สด — publish เวอร์ชันใหม่ระหว่างคำขอค้าง หลักฐาน "ส่งอะไรไป" ไม่ตรงกับที่ส่งจริง
แก้เป็น:
- `sendVia`: snapshot ต่อ purpose — `r.sends.push({ch:ch, at:…, vers:Object.fromEntries(r.purposes.map(function(c){return [c, currentVer(c)];}))})` (เขียนแบบ ES5 ตาม style ไฟล์)
- `policyRows`: ถ้า `r.sends.length` → ใช้เวอร์ชันจาก sends ล่าสุด: แสดง `v[ส่ง]` + เรียก `viewPolicy(code, verส่ง)` · ถ้าเวอร์ชันปัจจุบันใหม่กว่า → ป้ายเตือน "ส่ง v2 · ปัจจุบัน v3 — พิจารณาส่งคำขอใหม่" · คำขอยังไม่ส่ง แสดง current ตามเดิม
- นโยบาย auto-expire คำขอค้างเมื่อออกเวอร์ชันใหม่ = ห้ามทำเอง แขวน OQ-CNS-02 (comment ไว้)
ตรวจรับ: ส่งคำขอ → publish เวอร์ชันใหม่ → drawer คำขอเดิมแสดงเวอร์ชัน ณ ตอนส่ง + ป้ายเตือน · viewPolicy เปิดเอกสารเวอร์ชันที่ส่งจริง

### 6. FIX-06 contract anchors — HIGH
ตำแหน่ง: หัว tab resolve · `consentViewDrawer`/registry · ใกล้หัวไฟล์
สิ่งที่ผิด: F136/F031/F157/DSAR = 0 ทั้งไฟล์ ทั้งที่ contract ประกาศใน Feature List
แก้เป็น: comment 3 จุด:
- `<!-- CONTRACT: resolveConsent = API ให้ F136 Broadcast (ctl — ตรวจ opt-in ก่อนส่ง Email/SMS block อัตโนมัติ) และ F031 Customer 360 (data — สถานะ consent ผูกลูกค้า) consume -->`
- `<!-- CONTRACT: ทะเบียน consent + evidence + history = ฐานข้อมูลให้ F157 DSAR (data — ประวัติ consent ประกอบคำขอ) -->`
- display-only เท่านั้น ห้าม mock หน้าจอ F136/F031/F157
ตรวจรับ: anchor ครบ 3 contract

### 7. FIX-07 + FIX-08 MINOR รวบ (ทำท้ายสุด)
- demo-only (กติกา BA จาก F059): ครอบ demo-strip (persona + ปุ่ม sim), simbar "จำลอง" ใน recipient view, ข้อความ "(จำลอง — ไม่ส่งจริง)" ใน toast ด้วย class `demo-only` + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` · ทดสอบ `.demo-only{display:none}` แล้ว layout ไม่พัง ไม่เหลือศัพท์ dev
- ตาราง purposes เซลล์ที่มี pill ≥2 (แถว ~2530) → แยกคอลัมน์สถานะออกจากตัวเลข (Rule #103/#40)

## ข้อห้าม
- ห้ามเพิ่ม dependency/CDN · ห้ามแตะ BASE-KIT block · ห้ามเปลี่ยน CI token
- ห้ามแตะ: emitConsequence envelope, resolveConsent logic, evidence/supersede, doPublishVersion validation, reConsent, recipient verify flow, BR-06/viewPolicy(ver), BR-14/17
- ห้ามลบ comment BR-xx / FN-xx / LOCK-CSQ / MUST-FIX / S-xx

## หลังแก้เสร็จ ให้รันเองก่อนส่ง
1. node --check ทุก script block
2. audit.sh → FAIL=0 (WARN #44 ต้องหาย)
3. Playwright: pageerror=0 + เคสต่อไปนี้ผ่านครบ:
   - answerRequest/submitRecipient บนคำขอ answered/closed/expired → consent ไม่เพิ่ม · pending ตอบครั้งเดียวแล้วปิด · ลิงก์เปิดซ้ำเห็นหน้าสถานะปิด
   - Auditor เรียกทุก mutation ตรง → ไม่เปลี่ยน
   - double-click submit ทุกจุด → ผลครั้งเดียว
   - withdraw เฉพาะ granted · sendVia เฉพาะ draft/pending
   - ส่ง → publish v ใหม่ → drawer แสดงเวอร์ชัน ณ ตอนส่ง + ป้ายเตือน
   - inject `.demo-only{display:none}` → หน้าจอสะอาด layout ปกติ
แนบผลรันกลับมาพร้อมไฟล์ แล้วส่ง re-gate (รอบสั้น)
