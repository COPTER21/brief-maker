# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
HR — F059 ESS Portal (พนักงานทำเอง) · ess.html

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F059 ESS Portal (พนักงานทำเอง) · mod HR · arch master (portal/aggregate · display-only + deep-link) · dec: ntf + csq |
| ไฟล์ที่ตรวจ | ess.html (2,674 บรรทัด · single-file SPA) |
| วันที่ · ผู้ตรวจ | 2026-09-10 · BA gate (html-review-fix-order) |
| ขอบเขต | Re-gate ก่อนเข้า Phase B (FRD/TC) — เทียบ spec F059 + governance + interaction จริง |
| เครื่องมือ | node --check · audit.sh (v9) · Playwright walkthrough |
| ผล Quality Gate | node OK 4 block · audit **FAIL=0** WARN=3 (base-kit residuals) · Playwright **pageerror=0** · Esc chain ✓ |
| **Verdict** | 🟠 **BLOCK (รอบแก้สั้น)** — CRITICAL 0 · HIGH 3 · MINOR 1 → แก้ coverage + anchor แล้ว re-gate |

## 1. สรุปผลตรวจ (Executive Summary)

ไฟล์คุณภาพดีที่สุดใน batch นี้ — **ไม่มี CRITICAL เลย** สถาปัตยกรรมถูกต้องตามมติ OQ-HR-04: ESS เป็น portal display-only + deep-link "ESS ไม่รับหรือบันทึกคำขอเอง" — ในไฟล์ไม่มี mutation function แม้แต่ตัวเดียว (พิสูจน์แล้ว: ไม่มี do* ใน scope) จึงไม่มีช่อง bypass ให้เจาะ · scope SELF ทำถูกแบบ: self-banner + modal 403 "เข้าถึงถูกปฏิเสธ" สาธิต SecC · แจ้งเตือนอ่านจาก ENG-NOTIFY มี anchor ชัด (dec ntf ✓ ฝั่ง consume) · deep-link 4 เส้น (ลา/OT/เบิก/แก้ข้อมูล) พร้อม route + label · empty state, search/filter, Esc chain, pageerror สะอาดหมด · หมายเหตุ: icon เป็นกล่องเปล่าใน sandbox เพราะ CDN Lucide ถูก block — ไฟล์มี fallback + log ถูกต้อง ไม่นับเป็นข้อบกพร่อง

ประเด็นที่ให้ **BLOCK รอบสั้น** คือ coverage 2 จุดที่ขัด spec ตรง ๆ: (1) launcher "ยื่นคำขอ" ไม่มี **ขอหนังสือรับรอง** — c[1] ระบุ "ยื่นลา/OT/เบิก/**ขอหนังสือ** จากที่เดียว" และ F104 ระบุ "พนักงานขอผ่าน ESS" แต่ section หนังสือรับรองเป็นอ่านอย่างเดียว ไม่มีปุ่มขอ + LINKS ไม่มีเส้น cert (2) c[4] ระบุ "**ตารางกะ** + ประวัติลงเวลา" — มีเฉพาะประวัติสแกนเข้า-ออก ไม่มีตารางกะ (3) dec csq ประกาศแต่ไม่มี CSQ anchor ในไฟล์ (SecC ถูกพูดถึงใน copy แต่ decl_rule จับไม่ได้) · เพิ่มเติมตามคำสั่ง BA รอบนี้: ให้ mark ข้อความ demo/hint/สถานะ dev ทั้งหมดเป็น demo-only — **build จริงต้องไม่แสดง**

### 1.1 ความครบถ้วนเทียบ Spec F059

| Capability ตามแผน (c[]) | ผล | หมายเหตุ + หลักฐาน |
|---|---|---|
| ยื่นลา/OT/เบิก/ขอหนังสือ จากที่เดียว | ⚠️ 3/4 | actionPicker มี ลา/OT/เบิก/แก้ข้อมูล — **ขอหนังสือรับรองหาย** ทั้ง launcher และ LINKS (FIX-01) |
| ดูสลิปเงินเดือน + หนังสือรับรองที่เคยออก | ✅ | FN-02 สลิป (อ่าน Payroll PS-1 · self) + FN-06 ทะเบียนหนังสือ · drawer view ครบ |
| โควตาลา/สิทธิ์สวัสดิการคงเหลือ | ✅ | quota grid + FN-07 welfare/training |
| ตารางกะ + ประวัติลงเวลา ของตนเอง | ⚠️ ครึ่งเดียว | FN-04 มีประวัติสแกนเข้า-ออก — **ไม่มีตารางกะ** (grep กะ=0) (FIX-02) |
| อัพเดตข้อมูลติดต่อส่วนตัว (ผ่านอนุมัติ) | ✅ | FN-08 read + deep-link `#/profile/edit-request` "ขอแก้ข้อมูล = ขออนุมัติ" |
| d: scope SELF | ✅ | self-banner + accessDenied 403 + ข้อมูล mock มีเฉพาะ EMP เดียว |
| dec: ntf | ✅ | feed "จากศูนย์แจ้งเตือน (ENG-NOTIFY)" — anchor ฝั่ง consume ชัด · ESS ไม่ยิง event เอง (display-only) |
| dec: csq | ❌ | grep CSQ/csq/7C = 0 — SecC อยู่ใน copy แต่ไม่มี anchor ให้ decl_rule (FIX-03 + OQ-ESS-01) |
| มติ OQ-HR-04 (deep-link only) | ✅ | "ESS ไม่รับคำขอเอง" ประกาศใน modal + toast ทุกเส้น |

## 2. รายการสั่งแก้ (Fix Order)

### FIX-01 · [HIGH] c[1] ขอหนังสือรับรอง หายจาก launcher + LINKS

| ช่อง | รายละเอียด |
|---|---|
| อาการ | actionPicker "ยื่นคำขอ" มี 4 รายการ (ลา/OT/เบิก/แก้ข้อมูล) — ไม่มีขอหนังสือรับรอง · LINKS registry ไม่มีเส้น cert · section หนังสือรับรองใน docs เป็นอ่านอย่างเดียว ไม่มีปุ่มขอ |
| หลักฐาน | modal actionPicker (screenshot) · grep LINKS: leave/ot/expense/profile เท่านั้น |
| ผลกระทบ | ขัด c[1] ตรง ๆ และขัด spec F104 "พนักงานขอผ่าน ESS" (F104 ba-done W1 มีของแล้ว) |
| ตำแหน่ง | `LINKS` · modal `actionPicker` · section FN-06 (หัว section) |
| วิธีแก้ | เพิ่ม `cert:{label:'ขอหนังสือรับรอง', route:'#/cert/new'}` ใน LINKS + แถว apRow ใน actionPicker + ปุ่ม "ขอหนังสือ" (deep-link) ที่หัว section FN-06 — pattern เดียวกับปุ่มยื่นเบิก |

เกณฑ์ตรวจรับ: launcher มี 5 รายการครบตาม c[1] · ปุ่มขอหนังสือที่ section · deep-link toast ระบุ route

### FIX-02 · [HIGH] c[4] ตารางกะ ไม่มี — มีแต่ประวัติสแกน

| ช่อง | รายละเอียด |
|---|---|
| อาการ | FN-04 แสดง OT รวม + ตารางสแกนเข้า-ออก — ไม่มีตารางกะ (กะที่ถูกจัด/กะสัปดาห์นี้) |
| หลักฐาน | grep กะ = 0 ทั้งไฟล์ · FN-04 body |
| ผลกระทบ | c[4] ครึ่งเดียว — FRD จะไม่มี requirement ฝั่งตารางกะ |
| ตำแหน่ง | `renderPay` FN-04 |
| วิธีแก้ | เพิ่ม section "ตารางกะของฉัน" (อ่านอย่างเดียว · [ASSUMED] อ่านจากระบบกะ/Time W2): ตารางสัปดาห์ปัจจุบัน วัน·กะ·เวลา — mock 7 วัน · ถ้าทีมมีมติตัด scope กะออกจาก W9 ให้แขวน OQ แทน |

เกณฑ์ตรวจรับ: แท็บเงินเดือน & เวลา มี section ตารางกะ (หรือมติตัด scope เป็นลายลักษณ์อักษร)

### FIX-03 · [HIGH] dec csq ไม่มี anchor — SecC อยู่ใน copy แต่ decl_rule จับไม่ได้

| ช่อง | รายละเอียด |
|---|---|
| อาการ | chip ◆csq ประกาศใน Feature List — ไฟล์ไม่มี CSQ/7C anchor เลย มีแต่คำว่า SecC ในข้อความ banner/modal |
| หลักฐาน | grep CSQ=0 · csq=0 · 7C=0 (SecC=5 ใน copy) |
| ผลกระทบ | decl_rule.py (S1.8) chip vs detect → DIVERGENCE |
| ตำแหน่ง | modal accessDenied + จุด openView ข้อมูล RESTRICTED (สลิป) |
| วิธีแก้ | เพิ่ม comment anchor: `<!-- CSQ: ess.access_denied → ท่อ SecC · ess.restricted_view (เปิดดูสลิป) → ท่อ SecC — ตาม CSQ_BRIEF_F059 (event/ท่อจริงรอเคาะ OQ-ESS-01) · ห้ามประกาศ OC/DC ซ้ำ -->` ที่ modal 403 และ openView('payslip') |

เกณฑ์ตรวจรับ: มี CSQ anchor อย่างน้อย 2 จุด (access_denied + restricted_view) · ไม่ประกาศท่อสงวน

### FIX-04 · [MINOR·PROD] ข้อความ demo/hint/สถานะ dev — build จริงต้องไม่แสดง (คำสั่ง BA รอบนี้)

| ช่อง | รายละเอียด |
|---|---|
| อาการ | องค์ประกอบสำหรับสาธิต/สื่อสารทีมปนอยู่ใน UI: (a) demo-strip "ตัวอย่าง (persona)" + ปุ่ม "ทดสอบเข้าถึงข้อมูลพนักงานอื่น" (b) chip "[ASSUMED contract]" ทุก section (c) chip "อ่านอย่างเดียว" แบบศัพท์ contract (d) sub-text หัว section เช่น "อ่านจากระบบเงินเดือน (PS-1)" (e) toast deep-link ต่อท้าย "[ASSUMED contract] #/route" (f) self-banner ใช้ศัพท์ dev "self-access · SecC" |
| ผลกระทบ | ถ้าหลุดไป production ผู้ใช้เห็นศัพท์ dev/contract ปนหน้าจอ |
| ตำแหน่ง | `renderPage` (self-banner + demo-strip) · `CH_ASSUMED`/`CH_RO` · `sec()` sub-text · `deepLink` toast |
| วิธีแก้ | (1) ครอบทุก element ข้างต้นด้วย class **`demo-only`** + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` (2) demo-strip + ปุ่มทดสอบ + chip [ASSUMED contract] = ถอดทิ้งใน prod ทั้งก้อน (3) self-banner คงไว้ได้แต่เปลี่ยนเป็นภาษาผู้ใช้ "คุณกำลังดูข้อมูลของตนเอง" (ตัด self-access · SecC) (4) toast deep-link ใน prod = นำทางจริง ไม่มีข้อความ contract (5) sub-text แหล่งข้อมูล ("อ่านจากระบบเงินเดือน (PS-1)") ย้ายไปเป็น comment ใน code · สรุปรายการ demo-only ทั้งหมดลง UI Brief ตอน Phase B เพื่อให้ dev ตัดครบ |

เกณฑ์ตรวจรับ: ทุก element สาธิตติด class demo-only + comment · ไม่มีศัพท์ contract/dev ("[ASSUMED]", "SecC", "PS-1") ในข้อความที่ผู้ใช้เห็นเมื่อซ่อน demo-only

## 3. WARN จาก audit (แก้ตามสะดวก · ไม่บล็อก)

- Rule #21 / Rule #40 / font-size — base-kit residuals ตามที่ PREFLIGHT ในไฟล์ระบุไว้แล้ว
- Icon กล่องเปล่าใน sandbox = CDN Lucide ถูก block — ไม่ใช่ข้อบกพร่องไฟล์ (fallback + log ถูกต้อง) · ทีมเปิดในเครื่องที่มีเน็ตจะเห็น icon ปกติ

## 4. ประเด็นเปิด (OQ) — ต้องเคาะก่อนเขียน FRD

| รหัส | ประเด็น | ผู้เคาะ | กระทบ (ส่วน FRD) |
|---|---|---|---|
| OQ-ESS-01 | CSQ profile ของ F059 — portal display-only ยิง event ใด (secc.access_denied? การเปิดดูข้อมูล RESTRICTED?) เข้าท่อ SecC | Strike + Architect | CSQ_BRIEF_F059 |
| OQ-ESS-02 | route deep-link ทั้ง 5 เส้นยัง [ASSUMED contract] (#/leave/new · #/ot/new · #/expense/new · #/profile/edit-request · #/cert/new) — ยืนยัน route จริงกับ feature เจ้าของก่อนเขียน FRD §Integration | Strike + ทีมเจ้าของ feature | §Integration · contract ปลายทาง |

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] node --check ทุก script block ผ่าน
- [ ] audit.sh FAIL=0
- [ ] Playwright pageerror=0 ทุก tab/drawer/modal
- [ ] launcher 5 รายการ + ตารางกะ + CSQ anchor ครบ · ทุก demo element ติด demo-only
- [ ] ส่งไฟล์กลับ re-gate (รอบสั้น — ไม่มี CRITICAL)
- [ ] ผ่านแล้ว: อัพเดต FEATURE_REGISTRY (BA status F059) + แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q → เข้า Phase B (FRD/TC)
