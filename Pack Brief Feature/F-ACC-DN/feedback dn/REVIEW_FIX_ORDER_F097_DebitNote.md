# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
Accounting — F097 Debit Note (ใบลดหนี้ผู้ขาย) · F-ACC-DN_debit-note.html

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F097 Debit Note · mod Accounting · W5 · arch **Q-document** · dec: doa + ntf + csq + doccfg + pdfdoc · auto: LITE |
| ไฟล์ที่ตรวจ | F-ACC-DN_debit-note.html (219 KB · Q-DOC KERNEL W5-LITE) |
| วันที่ · ผู้ตรวจ | 2026-09-23 · BA gate (html-review-fix-order) |
| เครื่องมือ | node --check · audit.sh (v9) · Playwright walkthrough + bypass catalog |
| ผล Quality Gate | node OK · audit **FAIL=0** WARN=1 (font-size kit) · Playwright **pageerror=0** |
| **Verdict** | 🟠 **BLOCK (รอบแก้สั้น)** — CRITICAL 0 · HIGH 3 · MINOR 2 |

## 1. สรุปผลตรวจ (Executive Summary)

**ไฟล์แรกของ batch ที่ guard ครบตั้งแต่ส่งมา** — บทเรียน F096 ถูกใส่แล้วทั้งชุด (comment `status guard in handler`) และ**พิสูจน์ผ่านการรันทั้งหมด**: ยกเลิกใบ sent → block พร้อมอ้าง OQ-DN-04 · ส่งใบ draft → block · ส่งอนุมัติซ้ำใบ approved → block · ผู้ไม่มีสิทธิ์อนุมัติ → block · persona ผู้อนุมัติจริง → เดินทีละขั้น · `busyGate` กันกดซ้ำ · `.demo-only` ครอบ persona switch / pv-simulate / "จำลอง · รอเชื่อม F093" แล้ว · kernel เดิมครบ (resolveDoa 3 tier · approveGuard re-check คงค้าง · dnHeld/lineRoom · ออกเลขตอนอนุมัติครบ · PDF ครบ ม.86/10 พร้อมช่อง "ใบลดหนี้ผู้ขาย TFS-xxxx") · ภาษีซื้อคิดใหม่จากฐานที่ลด (ม.86/10) · ทางเลือก "ลดหนี้ไม่อ้างใบตั้งหนี้" ปิดไว้พร้อมอ้าง OQ-DN-01

ที่ให้ **BLOCK รอบสั้น** เป็นประเด็น domain ของฝั่งผู้ซื้อ ไม่ใช่ guard: (1) **c[3] "ติดตามเครดิตคงเหลือกับ vendor" ไม่รองรับ** — ใบตั้งหนี้ที่จ่ายครบแล้ว (API-2026-0038 paid = grand) available = 0 → ออกใบลดหนี้ผู้ขายไม่ได้เลย ทั้งที่กรณีจริง (คืนของหลังจ่าย) คือที่มาของ vendor credit ที่ต้องติดตาม (2) **ภาษีซื้อกลับตามวันที่ใบลดหนี้ของเรา** [ASSUMED OQ-DN-05] — ตามกฎ ผู้ซื้อลดภาษีซื้อในเดือนที่**ได้รับใบลดหนี้จากผู้ขาย** และเอกสารภาษีคือใบลดหนี้ของผู้ขาย ไม่ใช่ DN ของเรา → ช่อง `vendorCn` ต้องบังคับก่อนกลับภาษีซื้อ + มีวันที่ได้รับ (3) dec csq/ntf/doccfg anchor = 0 · contracts F080/F095 ไม่ระบุรหัส

### 1.1 ความครบถ้วนเทียบ Spec F097

| Capability ตามแผน (c[]) | ผล | หมายเหตุ + หลักฐาน |
|---|---|---|
| สร้างจาก RTV/ข้อตกลงส่วนลด อ้าง AP invoice เดิม | ✅ | source inv + RTV (needRTV) · lineRoom ต่อบรรทัด · 3 เหตุผล (RTV/OVERPRICE/SHORT) |
| ลด AP + ปรับภาษีซื้อ | ⚠️ | dnApplied ลดยอดคงค้าง ✓ · ภาษีซื้อคิดฐานใหม่ ✓ — แต่เดือนภาษี/เอกสารอ้างอิงยึด DN ของเรา ไม่ใช่ใบลดหนี้ผู้ขาย (FIX-02) |
| ติดตามเครดิตคงเหลือกับ vendor | ❌ | ใบจ่ายครบ → available 0 → ออก DN ไม่ได้ · ไม่มี vendor credit balance (FIX-01) |
| PDF เอกสารครบ | ✅ | ผู้ขาย/เรา + เลขภาษี + สาขา · อ้างใบกำกับผู้ขาย + ใบตั้งหนี้ · มูลค่าเดิม/ถูกต้อง/ผลต่าง + VAT · เหตุผล · ใบลดหนี้ผู้ขาย |
| d: คู่ขนานกับ RTV | ✅ | RTV [ASSUMED] · pickRTV เติมบรรทัด |
| d: อนุมัติก่อนบันทึก | ✅ | DOA 3 tier + guard ครบ (พิสูจน์แล้ว) |
| dec: doa · pdfdoc | ✅ | — |
| dec: ntf · csq · doccfg | ❌ | grep = 0 ทั้งสาม (FIX-03) |
| Contracts F080→F097 flow · F097→F095 data | ⚠️ | RTV/ใบตั้งหนี้อ้างในไฟล์ แต่ไม่ระบุรหัส F080/F095 (FIX-03) |

## 2. รายการสั่งแก้ (Fix Order)

### FIX-01 · [HIGH] c[3] เครดิตคงเหลือกับ vendor — ใบตั้งหนี้ที่จ่ายครบแล้วออก DN ไม่ได้

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `invAvailable = outstanding − held` · ใบจ่ายครบ (API-2026-0038 grand 87,740 / paid 87,740) → available 0 → `dnOver` block ทุกบรรทัด · ไม่มีแนวคิด vendor credit balance เลย |
| หลักฐาน | D5: API-2026-0038 avail = 0 · grep เครดิตคงเหลือ = 0 |
| ผลกระทบ | เคสหลักของ RTV (คืนของหลังจ่ายเงินแล้ว) ทำไม่ได้ · c[3] หายทั้งข้อ |
| ตำแหน่ง | `invAvailable` / `dnOver` / `step3Block` · view drawer · list stats |
| วิธีแก้ | แยกเพดานเป็น "มูลค่าที่ลดได้ของใบตั้งหนี้" (grand − dnApplied − held · ไม่หัก paid) จาก "ผลลัพธ์": ส่วนที่เกินยอดค้างจ่าย = **vendor credit** (เครดิตคงเหลือ) · ใบ DN แสดง "หักจากหนี้ค้าง ฿X · เครดิตคงเหลือกับผู้ขาย ฿Y" · เพิ่ม card/แท็บ "เครดิตคงเหลือรายผู้ขาย" (display) + status การใช้เครดิต (หักใบตั้งหนี้ถัดไป/ขอคืนเงิน — flow รอเคาะ OQ-DN-06) |

เกณฑ์ตรวจรับ: ใบจ่ายครบออก DN ได้ไม่เกินมูลค่าใบ · ระบบแยกยอดหักหนี้ vs เครดิตคงเหลือ · มีที่ดูเครดิตคงเหลือรายผู้ขาย

### FIX-02 · [HIGH] ภาษีซื้อกลับต้องยึดใบลดหนี้ของผู้ขาย — vendorCn บังคับ + วันที่ได้รับ

| ช่อง | รายละเอียด |
|---|---|
| อาการ | แท็บภาษีซื้อ: "เดือนภาษีที่ลด — ตามวันที่ใบลดหนี้ [ASSUMED OQ-DN-05]" ยึด `dnDate` ของเรา · `vendorCn` เป็นช่อง optional ("เช่น TFS-6650") ไม่มีวันที่ |
| ผลกระทบ | ตามกฎ VAT ผู้ซื้อลดภาษีซื้อในเดือนที่ได้รับใบลดหนี้จากผู้ขาย และเอกสารภาษีคือใบลดหนี้ผู้ขาย — ถ้าไม่บังคับ ภ.พ.30 จะลดภาษีซื้อโดยไม่มีเอกสารรองรับ |
| ตำแหน่ง | `blankData`/wizard ขั้น 2 · แท็บใบตั้งหนี้อ้างอิง·ภาษีซื้อ · onFinalApprove |
| วิธีแก้ | เพิ่ม `vendorCnDate` (วันที่ใบลดหนี้ผู้ขาย/วันที่ได้รับ) · state ภาษี 2 ขั้น: DN approved = ลดหนี้ AP ได้ · **กลับภาษีซื้อได้เมื่อมี vendorCn + vendorCnDate** (ก่อนหน้านั้นแสดง "รอใบลดหนี้ผู้ขาย" ใน ภ.พ.30) · เดือนภาษี = เดือนของ vendorCnDate · comment `<!-- LEGAL: ผู้ซื้อลดภาษีซื้อในเดือนที่ได้รับใบลดหนี้ (ม.82/10) — ยืนยัน OQ-DN-05 -->` |

เกณฑ์ตรวจรับ: DN ไม่มี vendorCn → AP ลดได้ แต่ภาษีซื้อสถานะ "รอเอกสาร" · ใส่ vendorCn+วันที่ → เดือนภาษีตามวันที่ได้รับ

### FIX-03 · [HIGH] anchors csq · ntf · doccfg · contracts F080/F095

| ช่อง | รายละเอียด |
|---|---|
| อาการ | grep CSQ/7C/ntf/ENG-DOC-NUM/doccfg = 0 · RTV และใบตั้งหนี้อ้างในไฟล์แต่ไม่ระบุรหัส F080/F095 |
| ตำแหน่ง | `nextCode` · `onFinalApprove` · `openSendDN` · header dep comment |
| วิธีแก้ | (a) `<!-- เลขจริงจาก ENG-DOC-NUM.next() ตาม doc_type DN ใน DOCCFG_BRIEF_F097 (F003) · สำเนา PDF ผ่าน ENG-DOC-STORE -->` (b) `<!-- CSQ: dn.issued → AC (ลด AP) · dn.vat_applied → AC ภาษีซื้อ ตาม CSQ_BRIEF_F097 (รอเคาะ OQ-DN-07) · DC จาก DOA ห้ามซ้ำ -->` (c) NTF: `dn.issued → ผู้สร้าง+AP` · `dn.sent → ผู้ขาย` · doa_* ห้ามซ้ำ (d) `<!-- CONTRACT: F080 RTV → F097 (flow — คืนของ → ใบลดหนี้ผู้ขาย) · F097 → F095 AP Invoice (data — ลดยอดหนี้ตั้งซื้อเดิม) -->` |

เกณฑ์ตรวจรับ: anchor ครบ 3 chip + contract 2 เส้นระบุรหัส

### FIX-04 · [MINOR·PROD] demo-only จุดที่เหลือ

"template ตาม thai-doc-pdf-generator" บนหัว PDF tab · "[ASSUMED OQ-DN-05]" ใน KV ผู้ใช้เห็น · "(DEMO)" ใน toast สลับบทบาท → ครอบ `demo-only`/ย้ายเป็น comment · เกณฑ์: inject `.demo-only{display:none}` แล้วไม่เหลือศัพท์ dev

### FIX-05 · [MINOR] WARN audit font-size base-kit residual — แก้ตามสะดวก

## 3. สิ่งที่ผ่านและขอคงไว้ (ห้ามแตะตอนแก้)

- status guards ใน openCancelDN / openSendDN / confirmSubmit (+ ใน callback) · `busyGate` · `.demo-only` ที่ครอบแล้ว — **ต้นแบบให้ทีม vibe ใช้แก้ F096 และไฟล์ก่อนหน้า**
- canActStep SoD · confirmApprove ทีละขั้น · approveGuard re-check คงค้าง · resolveDoa 3 tier · slot ไม่ prefill
- dnApplied/dnHeld/lineRoom · ออกเลขตอนอนุมัติครบ · nextCode max-based · reason master + RTV บังคับ
- PDF ม.86/10 + ช่องใบลดหนี้ผู้ขาย · ภาษีซื้อคิดฐานใหม่ · ปิดทางเลือกไม่อ้างใบตั้งหนี้ (OQ-DN-01)

## 4. ประเด็นเปิด (OQ) — เพิ่มจากที่ไฟล์ประกาศ (OQ-DN-01/04/05)

| รหัส | ประเด็น | ผู้เคาะ | กระทบ |
|---|---|---|---|
| OQ-DN-05 (ยืนยัน) | เดือนภาษีที่ลดภาษีซื้อ = เดือนที่ได้รับใบลดหนี้ผู้ขาย · vendorCn บังคับก่อนกลับภาษีซื้อ | Strike + บัญชี | 03_LOGIC · ภ.พ.30 |
| OQ-DN-06 | การใช้เครดิตคงเหลือกับผู้ขาย — หักใบตั้งหนี้ถัดไปอัตโนมัติ / ขอคืนเงิน / อายุเครดิต · feature ไหนเป็นเจ้าของ (F097 หรือ AP) | Strike | 03_LOGIC · §Integration |
| OQ-DN-07 | CSQ profile — dn.issued (AC ลด AP) กับ dn.vat_applied (ภาษีซื้อ) เป็น event เดียวหรือแยกตามเอกสารผู้ขาย | Strike + Architect | CSQ_BRIEF_F097 |

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] node --check ผ่าน · audit FAIL=0 · Playwright pageerror=0
- [ ] ใบจ่ายครบออก DN ได้ + เครดิตคงเหลือแสดง · vendorCn+วันที่คุมภาษีซื้อ
- [ ] anchors csq/ntf/doccfg/contract ครบ · demo-only จุดที่เหลือ
- [ ] guards เดิม (D1–D4) ยังผ่านทั้งหมด
- [ ] ส่ง re-gate (รอบสั้น — ไม่มี CRITICAL)
- [ ] ผ่านแล้ว: อัพเดต FEATURE_REGISTRY (F097) + แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q → Phase B
