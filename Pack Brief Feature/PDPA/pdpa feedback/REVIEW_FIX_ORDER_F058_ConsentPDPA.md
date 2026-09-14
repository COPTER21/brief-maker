# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
Marketing — F058 Consent PDPA (opt-in/out ลูกค้า) · consent-pdpa.html

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F058 Consent PDPA · mod Marketing · W1 · **S1 (security wave ก่อน production Credence)** · arch master · dec: csq |
| ไฟล์ที่ตรวจ | consent-pdpa.html (3,085 บรรทัด · single-file SPA) |
| วันที่ · ผู้ตรวจ | 2026-09-14 · BA gate (html-review-fix-order) |
| ขอบเขต | Re-gate ก่อนเข้า Phase B — เทียบ spec F058 + governance + interaction จริง + โจทย์เพิ่ม (lifecycle ครบ + ดูเนื้อหาที่ส่ง) |
| เครื่องมือ | node --check · audit.sh (v9) · Playwright walkthrough + bypass catalog |
| ผล Quality Gate | node OK 4 block · audit **FAIL=0** WARN=5 · Playwright **pageerror=0** · Esc chain ✓ |
| **Verdict** | 🟠 **BLOCK (รอบแก้สั้น)** — CRITICAL 1 · HIGH 5 · MINOR 2 |

## 1. สรุปผลตรวจ (Executive Summary)

ตามที่ประเมินมา — **โดยรวมโอเคจริง** และเป็นไฟล์ที่ governance ถูกแบบที่สุดใน batch: lifecycle ครบทั้งวง **สร้าง** (วัตถุประสงค์ + เอกสารนโยบายมีเวอร์ชัน บังคับแนบไฟล์ก่อน publish) → **จัดการ** (ทะเบียน consent · withdraw บังคับเหตุผล+ช่องทาง · renew · re-consent batch เมื่อออกเวอร์ชันใหม่ · ปิดวัตถุประสงค์แบบเก็บหลักฐาน BR-14/17) → **ส่ง** (คำขอ + ลิงก์ + QR + PDF form + multi-channel + บันทึกการส่ง + หน้าลูกค้าตอบจริงแบบ verify ตัวตนก่อน) → **บริหาร** (สถิติ · C360 รายลูกค้า · export CSV · resolve simulator) · **ดูเนื้อหาที่ส่งไปได้** — drawer คำขอมี section "เนื้อหาที่ให้เซ็น (BR-06)" เปิดอ่านเอกสารต่อวัตถุประสงค์ได้ และ viewPolicy เปิดดูเวอร์ชันเก่าได้

จุดแข็งพิเศษ: **CSQ declare-only envelope ถูกหลักที่สุดที่เคยตรวจ** (idempotency_key BR-CSQ-02 · reversal_of BR-CSQ-04 · ไม่ตีมูลค่า/ไม่ประทับผลรายท่อตาม LOCK-CSQ-04/05/06) · **resolve API default-deny** — คู่ที่ไม่เคยขอ = ส่งไม่ได้, นโยบายเก่ากว่าปัจจุบัน = block, หมดอายุ = block (c[3] ✓) · evidence ครบ 5 องค์ประกอบ + ผูก policyVersion ณ ตอนตอบ (c[2] ✓)

ที่ต้องแก้ก่อนผ่าน: (1) **คำขอที่ตอบแล้วถูกตอบซ้ำได้ไม่จำกัด** — แต่ละครั้งสร้าง consent ใหม่ + supersede หลักฐานเดิม (พิสูจน์: consent 9→11 ใบจากคำขอเดียว) = evidence chain ซึ่งเป็นหัวใจ PDPA ถูกเขียนทับได้ (2) sends ไม่ snapshot เวอร์ชันนโยบาย — panel "เนื้อหาที่ให้เซ็น" render เวอร์ชันปัจจุบันเสมอ ถ้า publish เวอร์ชันใหม่ระหว่างคำขอค้าง หลักฐาน "ส่งอะไรไป" จะไม่ตรงกับที่ส่งจริง (3) persona guard เป็น UI-only — Auditor เรียก mutation ตรงผ่าน (4) ไม่มี `_busy` ทั้งไฟล์ — double submit สร้างคำขอซ้ำ (5) contract anchors หาย (F136/F031/F157/DSAR = 0)

### 1.1 ความครบถ้วนเทียบ Spec F058 + โจทย์รอบนี้

| Capability | ผล | หมายเหตุ + หลักฐาน |
|---|---|---|
| c[1] บันทึก consent ต่อวัตถุประสงค์ + ช่องทางที่ได้มา | ✅ | consent ผูก subject×purpose×channel + supersede คู่ซ้ำ (BR-01) |
| c[2] ประวัติให้/ถอน + timestamp | ✅ | history ทุก transition + evidence (answeredAt/requestChannel/idMethod/policyVersion/ipDevice) |
| c[3] API ตรวจ consent ก่อนส่ง (Email/SMS block) | ✅ | resolveConsent default-deny (never_asked/withdrawn/expired/stale → allowed:false พร้อมเหตุผล) + tab จำลองการเรียก |
| c[4] รายงาน consent สำหรับ audit/DSAR | ⚠️ | สถิติ + ทะเบียน + export CSV ✓ — แต่ DSAR/F157 anchor = 0 (FIX-06) |
| d: เวอร์ชันตามนโยบาย | ✅ | versions ต่อ purpose · publish บังคับแนบเอกสาร · stale detect + re-consent batch |
| d: ถอนมีผลทันที | ✅ | effStatus + resolve block ทันที · withdraw บังคับเหตุผล+ช่องทาง + CSQ reversal |
| d: ฐานข้อมูลให้ DSAR | ⚠️ | โครงข้อมูลพร้อม แต่ไม่มี anchor F157 (FIX-06) |
| dec: csq | ✅ | emitConsequence envelope ถูกหลัก LOCK-CSQ — ดีที่สุดใน batch |
| โจทย์: lifecycle สร้าง→จัดการ→ส่ง→บริหาร | ✅ | ครบทั้งวง (สรุปด้านบน) |
| โจทย์: ดูเนื้อหาที่ส่งไปได้ | ⚠️ | BR-06 panel + viewPolicy(ver) มี — แต่ render เวอร์ชันปัจจุบัน ไม่ snapshot ตอนส่ง (FIX-03) |
| Contracts →F136 ctl · →F031 data · →F157 data | ❌ | grep F136/F031/F157 = 0 ทั้งไฟล์ (FIX-06) |

## 2. รายการสั่งแก้ (Fix Order)

### FIX-01 · [CRITICAL] คำขอที่ตอบแล้วถูกตอบซ้ำได้ — evidence chain ถูกเขียนทับ

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `answerRequest`/`applyAnswers` ไม่เช็คสถานะคำขอ — เรียกกับคำขอ `answered` ซ้ำได้ไม่จำกัด แต่ละครั้งสร้าง consent ใบใหม่ + supersede (withdraw) หลักฐานเดิมทั้งชุด และสถานะคำขอไม่ถูกปิด |
| หลักฐาน | Bypass B1: REQ-2603 (answered) → answerRequest → consents 9→11 · B2: REQ-2604 → 9→10 |
| ผลกระทบ | หลักฐานความยินยอม (หัวใจ PDPA + ฐาน DSAR) ถูก generate ทับซ้ำจากลิงก์เดียว — audit ไม่น่าเชื่อถือ |
| ตำแหน่ง | `applyAnswers` (guard) + `answerRequest`/`submitRecipient` |
| วิธีแก้ | guard ต้น applyAnswers: คำขอต้องสถานะ `draft`/`pending` เท่านั้น — answered/closed/expired → toast "คำขอนี้ปิดแล้ว" + return · ตอบแล้ว set `r.status='answered'` + `answeredAt` แล้วลิงก์/หน้า recipient แสดงสถานะปิด (ลูกค้าเปิดลิงก์ซ้ำเห็น "ตอบแล้วเมื่อ …") · การเปลี่ยนใจ = คำขอใหม่/withdraw ตาม flow ปกติ (แขวน OQ-CNS-01) |

เกณฑ์ตรวจรับ: answerRequest/submitRecipient กับคำขอ answered/closed/expired → consent ไม่เพิ่ม + toast · คำขอ pending ตอบได้ครั้งเดียวแล้วปิด · เปิด recipient view ของคำขอที่ตอบแล้วเห็นสถานะปิด

### FIX-02 · [HIGH] Persona guard เป็น UI-only — Auditor เรียก mutation ตรงผ่าน

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `PERM()` ใช้แค่ตอน render ปุ่ม — function ไม่เช็ค: persona Auditor เรียก `answerRequest` ตรงสำเร็จ สร้าง consent ได้ |
| หลักฐาน | Bypass B4: persona auditor → answerRequest(REQ-2601) → consents 9→11 |
| ผลกระทบ | read-only role กลายพันธุ์เป็น writer — pattern เดียวกับที่ block F102/F131/F101 มาแล้ว |
| ตำแหน่ง | `applyAnswers` · `doWithdraw` · `doPublishVersion` · `doClosePurpose` · `submitReqCreate` · `sendVia` |
| วิธีแก้ | mirror guard ต้นทุก mutation: เช็ค `PERM()` ที่เกี่ยวข้อง (sign/withdraw/purpose/reqCreate/send) → ไม่ผ่าน toast "สิทธิ์ไม่พอ" + return + comment `<!-- SEC: บทบาทจริงจากล็อกอิน · mirror sec.can() -->` |

เกณฑ์ตรวจรับ: persona Auditor เรียกทุก mutation ตรง → state ไม่เปลี่ยน · Officer/DPO ตามสิทธิ์เดิม (purpose = DPO เท่านั้น)

### FIX-03 · [HIGH] การส่งไม่ snapshot เวอร์ชันนโยบาย — "เนื้อหาที่ส่งไป" ไม่ตรงกับที่ส่งจริง

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `sends[]` เก็บแค่ `{ch, at}` และ panel "เนื้อหาที่ให้เซ็น (BR-06)" render จาก `p.currentVer`/`curDoc()` สด — ถ้า publish เวอร์ชันใหม่ระหว่างคำขอ pending ค้าง หลักฐานจะแสดงเวอร์ชันใหม่ทั้งที่ตอนส่งเป็นเวอร์ชันเก่า |
| หลักฐาน | `sends[0] = {ch:'email', at:…}` (ไม่มี ver) + `policyRows` ใช้ `pp.currentVer` |
| ผลกระทบ | โจทย์ "ดูเนื้อหาที่ส่งไปได้" ผ่านเชิง UI แต่ไม่ผ่านเชิงหลักฐาน — audit ตอบไม่ได้ว่าส่งเอกสารเวอร์ชันไหน |
| ตำแหน่ง | `sendVia` · `createRequestRecord` · `reqViewDrawer` (policyRows) |
| วิธีแก้ | (a) ตอนส่ง: `sends.push({ch, at, vers:{PUR-01:2,…}})` — snapshot currentVer ต่อ purpose ณ เวลาส่ง (b) BR-06 panel: ถ้ามี sends ให้แสดงเวอร์ชัน ณ การส่งล่าสุด + ป้ายเตือนเมื่อเวอร์ชันปัจจุบันใหม่กว่า ("ส่ง v2 · ปัจจุบัน v3 — พิจารณาส่งคำขอใหม่") · `viewPolicy(code, ver)` รองรับอยู่แล้ว ใช้ ver จาก snapshot (c) คำขอที่ยังไม่ส่ง แสดง current ตามเดิม · นโยบาย auto-expire คำขอค้างเมื่อออกเวอร์ชันใหม่ แขวน OQ-CNS-02 |

เกณฑ์ตรวจรับ: ส่งคำขอ → publish เวอร์ชันใหม่ → เปิด drawer คำขอเดิม เห็นเวอร์ชัน ณ ตอนส่ง + ป้ายเตือนเวอร์ชันใหม่กว่า · viewPolicy เปิดเอกสารเวอร์ชันที่ส่งจริง

### FIX-04 · [HIGH] ไม่มี `_busy` ทั้งไฟล์ — double submit สร้างคำขอซ้ำ

| ช่อง | รายละเอียด |
|---|---|
| อาการ | กดยืนยันรัว 2 ครั้ง → คำขอเกิด 2 ใบ (grep _busy = 0 · audit WARN #44 ไม่มี loading state) |
| หลักฐาน | Bypass B8: submitReqCreate ×2 → requests 4→6 |
| ผลกระทบ | คำขอ/ลิงก์ซ้ำถึงลูกค้า + ขัด FN-92 มาตรฐาน batch |
| ตำแหน่ง | `submitReqCreate` · `submitRecipient` · `doWithdraw` · `doPublishVersion` · `doClosePurpose` |
| วิธีแก้ | pattern เดียวกับ F101: `if(state._busy)return; state._busy=true; … setTimeout(()=>state._busy=false,500)` ทุก action เปลี่ยนสถานะ + ปุ่ม loading state (Rule #44) |

เกณฑ์ตรวจรับ: double-click ทุก mutation → เกิดผลครั้งเดียว

### FIX-05 · [HIGH] Guard สถานะย่อย — withdraw ซ้ำ / ส่งซ้ำหลังตอบแล้ว

| ช่อง | รายละเอียด |
|---|---|
| อาการ | (a) `doWithdraw` บน consent ที่ `withdrawn` แล้ว → history เพิ่ม + CSQ reversal envelope ยิงซ้ำ (b) `sendVia` บนคำขอ `answered` → บันทึกการส่งเพิ่มได้ทั้งที่คำขอจบแล้ว |
| หลักฐาน | B3: CNS-5004 withdrawn → withdraw ซ้ำ → history 3→4, _csq +1 · B7: REQ-2603 answered → sendVia → sends 1→2 |
| ผลกระทบ | หลักฐานถอน/การส่งซ้ำซ้อน — BR-CSQ-02 idempotency ถูกออกแบบไว้แต่ฝั่ง UI ยิงซ้ำเอง |
| ตำแหน่ง | `doWithdraw` · `sendVia` |
| วิธีแก้ | doWithdraw guard `effStatus(c)==='granted'` เท่านั้น · sendVia guard `['draft','pending'].includes(r.status)` |

เกณฑ์ตรวจรับ: withdraw ได้เฉพาะ granted · ส่ง/ส่งซ้ำได้เฉพาะคำขอ draft/pending

### FIX-06 · [HIGH] Contract anchors หาย — F136 ctl / F031 data / F157 DSAR = 0

| ช่อง | รายละเอียด |
|---|---|
| อาการ | contracts ใน Feature List: F058→F136 (ctl ตรวจ opt-in ก่อนส่งอีเมล) · F058→F031 (data สถานะ consent ผูกลูกค้า) · F058→F157 (data ประวัติ consent ประกอบ DSAR) — grep ทั้งสามรหัส + DSAR = 0 ทั้งไฟล์ |
| ผลกระทบ | resolve tab คือ simulator ของ API แต่ไม่ประกาศ consumer — Phase B เขียน §Integration ไม่ได้ · d "เป็นฐานข้อมูลให้ DSAR" ไม่มีร่องรอย |
| ตำแหน่ง | tab resolve (หัว section) · consentViewDrawer/registry · หัวไฟล์ |
| วิธีแก้ | comment anchors: `<!-- CONTRACT: resolveConsent = API ให้ F136 (Broadcast ctl ตรวจ opt-in ก่อนส่ง) + F031 (Customer 360 data) consume -->` · `<!-- CONTRACT: ประวัติ consent + evidence = ฐานข้อมูลให้ F157 DSAR (data) -->` — display-only ไม่ mock หน้าจอ feature อื่น |

เกณฑ์ตรวจรับ: anchor ครบ 3 contract · ไม่มีหน้าจอ feature อื่นเกิดใหม่

### FIX-07 · [MINOR·PROD] mark demo elements เป็น demo-only (กติกา BA จาก F059)

| ช่อง | รายละเอียด |
|---|---|
| อาการ | demo-strip (persona + ปุ่ม sim ตอบ) · simbar "จำลอง — นี่คือหน้าที่เจ้าของข้อมูลเห็น…" ใน recipient view · toast "(จำลอง — ไม่ส่งจริง)" — ยังไม่ติด class demo-only ตามกติกาที่ประกาศรอบ F059 |
| วิธีแก้ | ครอบด้วย class `demo-only` + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` · toast ใน prod = ข้อความจริงไม่มีวงเล็บจำลอง · ทดสอบ `.demo-only{display:none}` แล้ว layout ไม่พัง ไม่เหลือศัพท์ dev |

เกณฑ์ตรวจรับ: ทุก demo element ติด demo-only · ซ่อนแล้วหน้าจอสะอาด

### FIX-08 · [MINOR] audit WARN ที่ควรเก็บ

| ช่อง | รายละเอียด |
|---|---|
| อาการ | Rule #103/#40 เซลล์เดียวมี pill ≥2 (บรรทัด ~2530 ตาราง purposes) · Rule #44 loading state (ผูก FIX-04) |
| วิธีแก้ | แยกคอลัมน์สถานะ/จำนวน · ใส่ loader-2 ตอน submit |

เกณฑ์ตรวจรับ: audit WARN เหลือเฉพาะ base-kit residuals

## 3. สิ่งที่ผ่านและขอคงไว้ (ห้ามแตะตอนแก้)

- CSQ envelope declare-only (idempotency + reversal + invisible sink) — ต้นแบบให้ feature อื่นใน batch
- resolveConsent default-deny + stale/expired block + เหตุผลอ่านรู้เรื่อง
- Evidence 5 องค์ประกอบ + policyVersion ณ ตอนตอบ · supersede BR-01 · BR-14/17 ปิดแบบเก็บหลักฐาน
- doPublishVersion บังคับแนบเอกสาร + stale count + reConsent batch
- Recipient view แยก surface + verify ตัวตน + บังคับเลือกครบทุกข้อ
- BR-06 "เนื้อหาที่ให้เซ็น" + viewPolicy(ver) — เพิ่ม snapshot ตาม FIX-03 เท่านั้น

## 4. ประเด็นเปิด (OQ) — ต้องเคาะก่อนเขียน FRD

| รหัส | ประเด็น | ผู้เคาะ | กระทบ (ส่วน FRD) |
|---|---|---|---|
| OQ-CNS-01 | ลูกค้าเปลี่ยนใจหลังตอบแล้ว — ให้แก้ผ่านลิงก์เดิมไม่ได้ (FIX-01) แล้วเส้นทางถูกต้องคือส่งคำขอใหม่/withdraw ใช่ไหม + ใครมีสิทธิ์เปิดคำขอใหม่ | Strike | 03_LOGIC state machine |
| OQ-CNS-02 | publish นโยบายเวอร์ชันใหม่ระหว่างคำขอ pending ค้าง — auto-expire คำขอเก่า (บังคับสร้างใหม่) หรือให้ตอบกับเวอร์ชันปัจจุบัน | Strike | 03_LOGIC · BR |
| OQ-CNS-03 | รอบต่ออายุ — nearExpiry 30 วันมีแล้ว ใคร/อะไร trigger คำขอต่ออายุ (manual จาก registry หรือ batch อัตโนมัติ) | Strike | 03_LOGIC · NTF ฝั่ง F136 |

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] node --check ทุก script block ผ่าน
- [ ] audit.sh FAIL=0
- [ ] Playwright pageerror=0 ทุก tab/drawer/modal/recipient
- [ ] รันเคส B1/B2/B3/B4/B7/B8 ซ้ำ → ทุกตัวถูก block · snapshot เวอร์ชันตาม FIX-03 ทำงาน
- [ ] demo element ติด demo-only ครบ
- [ ] ส่งไฟล์กลับ re-gate (รอบสั้น — CRITICAL เดียวแก้ตรงจุด)
- [ ] ผ่านแล้ว: อัพเดต FEATURE_REGISTRY (BA status F058) + แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q → เข้า Phase B
