# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
Accounting — F096 Credit Note (ใบลดหนี้ลูกค้า) · F-ACC-CN_credit-note.html

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F096 Credit Note · mod Accounting · W5 · arch **Q-document** · dec: doa + ntf + csq + doccfg + pdfdoc · auto: LITE |
| ไฟล์ที่ตรวจ | F-ACC-CN_credit-note.html (210 KB · single-file SPA · Q-DOC KERNEL W5-LITE) |
| วันที่ · ผู้ตรวจ | 2026-09-22 · BA gate (html-review-fix-order) |
| เครื่องมือ | node --check · audit.sh (v9) · Playwright walkthrough + bypass catalog |
| ผล Quality Gate | node OK 1 block · audit **FAIL=0** WARN=3 (#47 stepper · #99 segmented · font-size) · Playwright **pageerror=0** |
| **Verdict** | 🔴 **BLOCK** — CRITICAL 3 · HIGH 3 · MINOR 3 |

## 1. สรุปผลตรวจ (Executive Summary)

Kernel เอกสารของไฟล์นี้อยู่ระดับเดียวกับต้นแบบ F082/F085 และ**พิสูจน์ผ่านการรันแล้ว**: `confirmApprove` เดินทีละขั้น + `canActStep` (role/assignee + SoD ผู้ส่งอนุมัติเองไม่ได้ — ทดสอบผู้ไม่มีสิทธิ์ block จริง) · `resolveDoa` 3 tier ตามยอดลดหนี้ (50k/300k) + slot ไม่ prefill · **`approveGuard` re-check ยอดคงค้างใบแจ้งหนี้ ณ ขั้นสุดท้าย** (มีรับชำระ/ลดหนี้แทรกระหว่างรอ → ไม่อนุมัติ ตีกลับ) · `cnHeld` กันยอดใบที่ค้างอนุมัติ ไม่ให้ลดซ้ำเกินคงค้าง (`cnOver`/`lineOver`/`lineRoom` ต่อบรรทัด) · เลขออก**ตอนอนุมัติครบ** (`onFinalApprove` + `nextCode` max-based pad 4) · เหตุผลเป็น master (RET บังคับอ้างใบรับคืน SR · ผูก mode qty/price กำหนดวิธีคิด) · แท็บ "ใบแจ้งหนี้อ้างอิง · ภาษีขาย" แสดงผลกระทบ ภ.พ.30 + JE จำลอง (ประกาศรอเชื่อม F093) · **PDF ครบองค์ประกอบ ม.86/10** — ผู้ออก/ผู้ซื้อ + เลขผู้เสียภาษี + สาขา, อ้างใบกำกับเดิมเลข/วัน, มูลค่าเดิม/มูลค่าที่ถูกต้อง/ผลต่าง + VAT ของผลต่าง, เหตุผล, ต้นฉบับ/สำเนา · ปุ่มทุกตัวมี loading · Pattern Q view 5 แท็บ

ที่ต้อง **BLOCK** — pattern เดิม "ปุ่ม gate แต่ function ไม่ guard" แต่ครั้งนี้ตกบน**เอกสารภาษี**: (1) ใบลดหนี้ที่**ส่งลูกค้าแล้ว** (ออกเลข CN-2026-0021 แล้ว) ถูก**ยกเลิกเฉย ๆ**ผ่าน modal ได้ → ยอด AR ที่ลดไปเด้งกลับทันที ทั้งที่เอกสารภาษีที่ออกแล้วยกเลิกไม่ได้ ต้องแก้ด้วยเอกสารใหม่ (2) **ส่งใบ draft ให้ลูกค้าได้** → status sent โดยไม่ผ่านอนุมัติและ**ไม่มีเลขที่** (3) ใบ **approved ถูกส่งอนุมัติซ้ำ**ได้ → กลับ pending_approval + chain ใหม่ ทั้งที่ออกเลขแล้ว · นอกจากนี้ reason master ไม่ผูกกับ**เหตุตามประกาศอธิบดีฯ (ม.82/10)** — "ส่วนลดภายหลังการขาย" ไม่ใช่เหตุที่กฎหมายให้ออกใบลดหนี้ · dec csq/ntf/doccfg anchor = 0 · contract F094 ไม่ระบุรหัส

### 1.1 ความครบถ้วนเทียบ Spec F096

| Capability ตามแผน (c[]) | ผล | หมายเหตุ + หลักฐาน |
|---|---|---|
| สร้างจาก Sales Return/ปรับราคา อ้าง invoice เดิม | ✅ | source inv/SR · buildLinesFromInv + lineRoom ต่อบรรทัด · RET บังคับเลือก SR (F090 [ASSUMED]) |
| เหตุผลลดหนี้ตามกฎ + อนุมัติ | ⚠️ | อนุมัติ ✓ (DOA 3 tier + re-check) — เหตุผล 4 ข้อไม่ map กับเหตุตามประกาศฯ ม.82/10 (FIX-04) |
| ลด AR + กลับภาษีขายอัตโนมัติ | ✅ | cnApplied/invOutstanding ลดยอดคงค้าง · ผลกระทบ ภ.พ.30 + JE จำลอง — แต่ cancel ใบ sent ทำยอดเด้งกลับ (FIX-01) |
| PDF ใบลดหนี้เต็มรูป | ✅ | ครบ ม.86/10 (ดูภาพ) |
| d: อ้างเหตุตามประกาศสรรพากร | ❌ | ไม่มี legal_basis (FIX-04) |
| d: อนุมัติก่อนออก | ⚠️ | ออกเลขตอนอนุมัติครบ ✓ — แต่ส่ง draft ให้ลูกค้าได้ (FIX-02) |
| dec: doa | ✅ | ดีที่สุดใน batch ร่วมกับ F082 |
| dec: ntf · csq · doccfg | ❌ | grep = 0 ทั้งสาม (FIX-05) |
| dec: pdfdoc | ✅ | PDF Preview + ดาวน์โหลด/พิมพ์ |
| Contracts F090→F096 flow · F096→F094 data | ⚠️ | F090 [ASSUMED] ✓ · F094 ไม่ระบุรหัส (มีแต่ "AR Invoice contract ar_open_item") (FIX-05) |

## 2. รายการสั่งแก้ (Fix Order)

### FIX-01 · [CRITICAL] ใบลดหนี้ที่ออกเลข/ส่งลูกค้าแล้ว ถูกยกเลิกเฉย ๆ ได้

| ช่อง | รายละเอียด |
|---|---|
| อาการ | callback ใน `openCancelCN` ไม่เช็คสถานะ — ใบ sent (CN-2026-0021) ถูก cancel ผ่าน modal · `cnApplied` ไม่นับ cancelled → ยอดคงค้างใบแจ้งหนี้เด้งกลับทันที · VAT ที่ลดใน ภ.พ.30 หายไปเงียบ ๆ |
| หลักฐาน | Bypass C1: CN-2026-0021 sent → openCancelCN + ยืนยัน → `cancelled` |
| ผลกระทบ | เอกสารภาษีที่ออกแล้วยกเลิกไม่ได้ตามกฎ — ต้องแก้ด้วยเอกสารใหม่ (ใบเพิ่มหนี้/ใบลดหนี้ใหม่) และเลขห้ามหาย |
| ตำแหน่ง | callback ใน `openCancelCN` (+ ปุ่มใน view) |
| วิธีแก้ | guard: ยกเลิกได้เฉพาะ `draft` / `pending_approval` (ถอน) — approved/sent → block + toast ชี้ทาง "ออกใบเพิ่มหนี้/ใบลดหนี้ใหม่อ้างใบนี้" (flow แก้เอกสารภาษี = OQ-CN-02) · ใบที่ออกเลขแล้วต้องมีเฉพาะสถานะ void แบบมีเหตุผล+อ้างเอกสารทดแทน ไม่ใช่ cancelled |

เกณฑ์ตรวจรับ: cancel กับ approved/sent → block · draft/pending → ได้ตามเดิม · เลขที่ออกแล้วไม่หายจากทะเบียน

### FIX-02 · [CRITICAL] ส่งใบ draft ให้ลูกค้าได้ — ข้ามอนุมัติ ไม่มีเลขที่

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `openSendCN` ไม่เช็คสถานะ — ใบ draft (ไม่มี code) → sent |
| หลักฐาน | Bypass C2: R6 draft → openSendCN + ส่ง → `sent` · code ว่าง |
| ผลกระทบ | เอกสารภาษีถึงมือลูกค้าโดยไม่มีเลขที่และไม่ผ่าน DOA — ขัด d "อนุมัติก่อนออก" |
| ตำแหน่ง | `openSendCN` |
| วิธีแก้ | guard `s.status==='approved'` เท่านั้น · sent → ส่งซ้ำได้เป็น "ส่งสำเนาซ้ำ" (audit แยก ไม่เปลี่ยน status) |

เกณฑ์ตรวจรับ: send กับ draft/pending/cancelled → block · approved → sent + เลขครบ · sent → ส่งซ้ำบันทึกเป็นสำเนา

### FIX-03 · [CRITICAL] ใบ approved ถูกส่งอนุมัติซ้ำ — chain ถูกเขียนใหม่หลังออกเลข

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `confirmSubmit` ไม่เช็คสถานะ — ใบ approved (CN-2026-0022) → กลับ pending_approval + chain 1 ขั้นใหม่ + submittedBy เปลี่ยน |
| หลักฐาน | Bypass C4: approved → confirmSubmit → `{pending_approval, chain:[pending]}` |
| ผลกระทบ | ประวัติอนุมัติของเอกสารที่ออกเลขแล้วถูกเขียนทับ — ขัด Q-document "แก้หลังอนุมัติ = revision ใหม่" |
| ตำแหน่ง | `confirmSubmit` / `openSubmitModal` |
| วิธีแก้ | guard `s.status==='draft'` เท่านั้น (pending/approved/sent/cancelled → block) |

เกณฑ์ตรวจรับ: submit ได้เฉพาะ draft · approved/sent ยังคง chain + code เดิม

### FIX-04 · [HIGH] เหตุผลลดหนี้ไม่ผูกกับเหตุตามประกาศอธิบดีฯ (ม.82/10)

| ช่อง | รายละเอียด |
|---|---|
| อาการ | REASONS = RET / DISC "ส่วนลดภายหลังการขาย" / PRICE / QTY — ไม่มี `legal_basis` อ้างเหตุตามกฎหมาย · "ส่วนลดภายหลัง" ทั่วไปไม่ใช่เหตุที่ประกาศฯ ให้ออกใบลดหนี้ (เหตุตามกฎ: สินค้าผิดข้อกำหนด/ชำรุด/ขาดจำนวน/คำนวณราคาผิด · รับคืน/ยกเลิกบริการ · คืนเงินมัดจำ) · PDF พิมพ์เหตุผลจาก reasonText อิสระ |
| ผลกระทบ | c[2] "ตามกฎ" + d "ต้องอ้างเหตุตามประกาศสรรพากร" ไม่ผ่าน — ใบลดหนี้ที่เหตุไม่เข้าประกาศฯ ใช้ลดภาษีขายไม่ได้ |
| ตำแหน่ง | `CN_REASONS` · renderStep2 · PDF เหตุผล |
| วิธีแก้ | เพิ่ม `legal_basis` ต่อเหตุผล (รหัส+ข้อความตามประกาศฯ) · DISC ต้องเลือกเหตุย่อยที่เข้าข่าย (เช่น ลดราคาเพราะสินค้าผิดข้อกำหนด) หรือถ้าเป็นส่วนลดทางการค้าล้วน → ไม่ผ่านเป็นใบลดหนี้ภาษี (แจ้งผู้ใช้) · PDF พิมพ์ "เหตุผล: [legal_basis] — [รายละเอียด]" · comment `<!-- LEGAL: เหตุตามประกาศอธิบดีกรมสรรพากรเกี่ยวกับ VAT ฉบับที่ 82 — ยืนยันรายการกับบัญชี OQ-CN-01 -->` |

เกณฑ์ตรวจรับ: ทุกเหตุผลมี legal_basis · PDF พิมพ์เหตุตามกฎ · เหตุที่ไม่เข้าประกาศฯ ออกไม่ได้/แจ้งชัด

### FIX-05 · [HIGH] dec csq · ntf · doccfg anchor = 0 · contract F094 ไม่ระบุรหัส

| ช่อง | รายละเอียด |
|---|---|
| อาการ | grep CSQ/7C/ntf/NTF/ENG-DOC-NUM/doccfg = 0 · `nextCode` ทำถูกแล้วแต่ไม่มี comment hook · "AR Invoice contract ar_open_item" ไม่ระบุ F094 |
| ตำแหน่ง | `onFinalApprove` · `nextCode` · `openSendCN` · header dep comment |
| วิธีแก้ | (a) `nextCode`: `<!-- เลขจริงจาก ENG-DOC-NUM.next() ตาม doc_type CN ใน DOCCFG_BRIEF_F096 — ห้าม feature รันเลขเอง (F003) · สำเนา PDF ผ่าน ENG-DOC-STORE -->` (b) CSQ ที่ onFinalApprove: `<!-- CSQ: cn.issued → AC (ลด AR + ภาษีขาย) / FC ตาม CSQ_BRIEF_F096 (รอเคาะ OQ-CN-03) · DC จาก DOA engine ห้ามซ้ำ -->` (c) NTF: `cn.issued → ผู้สร้าง+AR` · `cn.sent → ลูกค้า` · doa_* ห้ามซ้ำ (NTF_BRIEF_F096) (d) `<!-- CONTRACT: F096 → F094 AR Invoice (data — ลดยอดคงค้าง ar_open_item) · F090 → F096 (flow — รับคืน → ใบลดหนี้) -->` |

เกณฑ์ตรวจรับ: anchor ครบ doccfg/csq/ntf + contract 2 เส้นระบุรหัส

### FIX-06 · [HIGH] ยกเลิกใบที่ออกเลขแล้ว — ต้องมีเส้นทางเอกสารทดแทน (ผูก FIX-01)

| ช่อง | รายละเอียด |
|---|---|
| อาการ | ไม่มีเส้นทางแก้ใบลดหนี้ที่ออกแล้ว (void แบบมีเหตุ + ออกใบใหม่/ใบเพิ่มหนี้อ้างใบเดิม) · reversal = 0 |
| ผลกระทบ | เมื่อ FIX-01 ปิดช่อง cancel ผู้ใช้จะไม่มีทางแก้ใบผิด |
| วิธีแก้ | เพิ่ม action display-only บนใบ approved/sent: "ออกเอกสารแก้ไข" → เลือก ใบเพิ่มหนี้ (Debit Note ลูกค้า — feature อื่น) หรือ ใบลดหนี้ใหม่อ้างใบนี้ + mark ใบเดิม `voided_by` (ไม่ลบ ไม่ถอนยอด) — flow จริงรอเคาะ OQ-CN-02 · comment anchor |

เกณฑ์ตรวจรับ: ใบออกแล้วมีปุ่ม "ออกเอกสารแก้ไข" (display-only) + ไม่มีปุ่มยกเลิก

### FIX-07 · [MINOR] WARN audit — #47 stepper ไม่ใช้ .step-dot · #99 segmented ฿/% · font-size residual

### FIX-08 · [MINOR] `_busy` ที่ confirmApprove/confirmSubmit/callbacks (busy() มีเฉพาะปุ่ม save/send) — pattern F101

### FIX-09 · [MINOR·PROD] demo-only (กติกา BA)

persona strip 4 คน · chip/ข้อความ "[ASSUMED contract]" · "จำลอง · รอเชื่อม Journal Entry F093" · "template ตาม thai-doc-pdf-generator" บนหัว PDF tab · badge DEMO → ครอบ class `demo-only` + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` · เกณฑ์: inject `.demo-only{display:none}` แล้วไม่เหลือศัพท์ dev + layout ไม่พัง

## 3. สิ่งที่ผ่านและขอคงไว้ (ห้ามแตะตอนแก้)

- `confirmApprove` ทีละขั้น + `canActStep` SoD · `resolveDoa` 3 tier · slot ไม่ prefill · **`approveGuard` re-check ยอดคงค้างขั้นสุดท้าย**
- `cnApplied`/`cnHeld`/`invAvailable`/`lineRoom` — กันลดหนี้เกินคงค้างทั้งระดับใบและบรรทัด
- ออกเลขตอนอนุมัติครบ (`onFinalApprove` + `nextCode` max-based) · reason master + mode qty/price · RET บังคับ SR
- แท็บภาษีขาย (ภ.พ.30) + JE จำลอง · PDF ม.86/10 ครบ · Pattern Q 5 แท็บ · loading state

## 4. ประเด็นเปิด (OQ)

| รหัส | ประเด็น | ผู้เคาะ | กระทบ |
|---|---|---|---|
| OQ-CN-01 | รายการเหตุลดหนี้ตามประกาศอธิบดีฯ ที่ CUBE รองรับ + การจัดการ "ส่วนลดทางการค้าภายหลัง" ที่ไม่เข้าประกาศฯ (ออกเป็นเอกสารอื่น?) | Strike + บัญชี | 05_RULES · PDF |
| OQ-CN-02 | เส้นทางแก้ใบลดหนี้ที่ออกเลขแล้ว — void + ใบใหม่ / ใบเพิ่มหนี้ลูกค้า (feature ไหนเป็นเจ้าของ Debit Note ฝั่งลูกค้า) | Strike | 03_LOGIC state machine |
| OQ-CN-03 | CSQ profile — cn.issued เข้า AC (ลด AR + VAT) และ/หรือ FC · cn.sent เป็น consequence หรือไม่ | Strike + Architect | CSQ_BRIEF_F096 |
| OQ-CN-04 | เดือนภาษีที่ลด — ตามวันที่ออกใบลดหนี้ (ไฟล์) หรืออนุญาต backdate ในเดือนภาษีเดิม | Strike + บัญชี | 03_LOGIC · ภ.พ.30 |

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] node --check ผ่าน · audit FAIL=0 (WARN #47/#99 หาย) · Playwright pageerror=0
- [ ] รันเคส C1/C2/C4 ซ้ำ → block ครบ · approve ทีละขั้น/SoD/re-check ยังทำงาน
- [ ] legal_basis ครบทุกเหตุผล + PDF พิมพ์ · anchors doccfg/csq/ntf/contract ครบ
- [ ] demo-only ติดครบ
- [ ] ส่ง re-gate เต็มรอบ (verdict BLOCK)
- [ ] ผ่านแล้ว: อัพเดต FEATURE_REGISTRY (F096) + แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q → Phase B
