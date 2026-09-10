# คำสั่งแก้ไข ess.html (F059 ESS Portal — พนักงานทำเอง)

คุณจะแก้ HTML prototype single-file ตามรายการนี้เท่านั้น ห้ามแตะส่วนอื่น
ห้าม regenerate ทั้งไฟล์ — แก้เฉพาะจุด (surgical edit)

## บริบท
- ไฟล์: ess.html · มาตรฐาน html-generator-v9 · archetype: portal (aggregate) **DISPLAY-ONLY + deep-link** ตามมติ OQ-HR-04 — "ESS ไม่รับหรือบันทึกคำขอเอง"
- ส่วนที่ผ่านการตรวจแล้ว **ห้ามเปลี่ยนพฤติกรรม**: โครง display-only (ห้ามเพิ่ม mutation ใด ๆ), scope SELF + modal 403 accessDenied, feed แจ้งเตือนจาก ENG-NOTIFY, deep-link pattern (LINKS + deepLink + toast), Esc chain, empty states, DSP-02 render preservation, BUG-6 drawer pointer-events guard
- หมายเหตุ: icon เป็นกล่องเปล่าใน sandbox ตรวจ = CDN Lucide ถูก block — ไม่ใช่บั๊ก ไม่ต้องแก้

## รายการแก้ (ทำตามลำดับ)

### 1. FIX-01 เพิ่ม "ขอหนังสือรับรอง" ให้ครบ c[1] — HIGH
ตำแหน่ง: `LINKS` · modal `actionPicker` · หัว section FN-06 (หนังสือรับรอง)
สิ่งที่ผิด: launcher มีแค่ ลา/OT/เบิก/แก้ข้อมูล — c[1] ระบุ "ยื่นลา/OT/เบิก/ขอหนังสือ จากที่เดียว" และ F104 ระบุ "พนักงานขอผ่าน ESS"
แก้เป็น:
- LINKS เพิ่ม `cert:{ label:'ขอหนังสือรับรอง', route:'#/cert/new' }`
- actionPicker เพิ่ม `apRow('award','ขอหนังสือรับรอง','ไปที่หน้า "หนังสือรับรอง"','cert')`
- หัว section หนังสือรับรอง (FN-06) เพิ่มปุ่ม `btn-primary btn-sm` "ขอหนังสือ" → `deepLink('cert')` — pattern เดียวกับปุ่ม "ยื่นเบิก" ของ FN-05
ตรวจรับ: launcher มี 5 รายการ · ปุ่มขอหนังสือที่ section · toast ระบุ route #/cert/new

### 2. FIX-02 เพิ่ม section "ตารางกะของฉัน" — HIGH
ตำแหน่ง: `renderPay` (FN-04 ต่อจาก OT & เวลาทำงาน)
สิ่งที่ผิด: c[4] "ตารางกะ + ประวัติลงเวลา" — มีแต่ประวัติสแกนเข้า-ออก ไม่มีตารางกะ
แก้เป็น: เพิ่ม section อ่านอย่างเดียว "ตารางกะของฉัน" — ตารางสัปดาห์ปัจจุบัน (7 วัน: วันที่ · กะ เช่น เช้า 08:00–17:00 / หยุด) mock ใน DATA.shifts + หมายเหตุแหล่งข้อมูลเป็น comment ใน code (อ่านจากระบบกะ/Time W2) — ห้ามมี action แก้กะ
ตรวจรับ: แท็บเงินเดือน & เวลา มี section ตารางกะ 7 วัน · ไม่มีปุ่ม mutation

### 3. FIX-03 CSQ anchor — HIGH
ตำแหน่ง: modal `accessDenied` + `openView` (จุดเปิดสลิป)
สิ่งที่ผิด: chip ◆csq ประกาศแต่ grep CSQ/7C = 0 — decl_rule จะ DIVERGENCE
แก้เป็น: เพิ่ม comment 2 จุด:
- ที่ accessDenied: `<!-- CSQ: ess.access_denied → ท่อ SecC ตาม CSQ_BRIEF_F059 (รอเคาะ OQ-ESS-01) -->`
- ที่ openView payslip: `<!-- CSQ: ess.restricted_view (เปิดดูสลิป/ข้อมูล RESTRICTED) → ท่อ SecC ตาม CSQ_BRIEF_F059 · ห้ามประกาศ OC/DC ซ้ำ -->`
ตรวจรับ: anchor ครบ 2 จุด · ไม่ประกาศท่อสงวน

### 4. FIX-04 mark ข้อความ demo/hint ทั้งหมดเป็น demo-only — build จริงต้องไม่แสดง (คำสั่ง BA)
ตำแหน่ง: `renderPage` (self-banner + demo-strip) · `CH_ASSUMED` / `CH_RO` · sub-text ใน `sec()` และหัว section · `deepLink` toast
สิ่งที่ต้องทำ:
1. เพิ่ม class **`demo-only`** + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` ครอบ:
   - demo-strip ทั้งก้อน ("ตัวอย่าง (persona)" + ปุ่ม "ทดสอบเข้าถึงข้อมูลพนักงานอื่น")
   - chip `[ASSUMED contract]` (CH_ASSUMED) ทุกจุด
   - chip "อ่านอย่างเดียว" (CH_RO) — ใน prod ความ read-only สื่อด้วยการไม่มีปุ่ม ไม่ต้องมี chip
   - sub-text แหล่งข้อมูลเชิง dev เช่น "อ่านจากระบบเงินเดือน (PS-1)", "อ่านจากระบบการลา", "feed จากศูนย์แจ้งเตือน (ENG-NOTIFY)" — ย้ายสาระไปเป็น comment ใน code แทน
2. self-banner: คงได้แต่เปลี่ยนเป็นภาษาผู้ใช้ — "คุณกำลังดูข้อมูลของตนเอง (สมชาย ใจดี · EMP-00123)" ตัดคำว่า self-access · SecC ออกจากข้อความที่ผู้ใช้เห็น (ย้ายไป comment)
3. modal accessDenied: subtitle ตัด "self-access (SecC)" → "พนักงานเห็นได้เฉพาะข้อมูลของตนเอง" (ศัพท์ SecC ไปอยู่ใน comment CSQ ของ FIX-03)
4. `deepLink` toast: ตัด "[ASSUMED contract] + route" ออกจากข้อความ toast — ใช้ "กำลังนำทางไปหน้า 'X'" เฉย ๆ + ย้าย route/contract ไปเป็น comment ที่ LINKS · ใน prod จุดนี้คือ navigation จริง
5. เพิ่ม CSS `/* DEMO-ONLY */ .demo-only{ } /* prod build: .demo-only{display:none!important} หรือ strip ออก */` พร้อม comment อธิบาย
ตรวจรับ: ทุก element สาธิตติด demo-only + comment ครบ · เมื่อทดลองใส่ `.demo-only{display:none}` หน้าจอไม่เหลือศัพท์ dev/contract ("[ASSUMED]", "SecC", "PS-1", "ตัวอย่าง (persona)") และ layout ไม่พัง

## ข้อห้าม
- **ห้ามเพิ่ม mutation function ใด ๆ** — ESS เป็น display-only ตามมติ OQ-HR-04
- ห้ามเพิ่ม dependency/CDN · ห้ามแตะ BASE-KIT block · ห้ามเปลี่ยน CI token
- ห้ามลบ comment FN-xx / OQ-HR-04 / BUG-6 / PREFLIGHT
- ห้ามแตะ: LINKS เส้นเดิม 4 เส้น, accessDenied logic, notify filter, DSP-02, drawer pointer-events guard

## หลังแก้เสร็จ ให้รันเองก่อนส่ง
1. node --check ทุก script block
2. audit.sh → FAIL=0
3. Playwright: pageerror=0 + เคสต่อไปนี้ผ่าน:
   - actionPicker มี 5 รายการ (รวมขอหนังสือรับรอง) · deepLink('cert') toast ทำงาน
   - แท็บเงินเดือน & เวลา มี section ตารางกะ 7 วัน · ไม่มีปุ่ม mutation ใหม่
   - grep CSQ anchor ≥ 2 จุด
   - inject `.demo-only{display:none}` → ไม่เหลือศัพท์ dev บนจอ + layout ปกติ + Esc chain ยังทำงาน
แนบผลรันกลับมาพร้อมไฟล์ แล้วส่ง re-gate (รอบสั้น — ไม่มี CRITICAL)
