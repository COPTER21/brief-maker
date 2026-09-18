# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
Warehouse — F083 Stock Transfer (ย้ายคลัง/สาขา) · F-WH-STKTRF.html

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F083 Stock Transfer · mod Warehouse · W3 · arch **Q-document** · dec: doa + ntf + csq + doccfg + pdfdoc · auto: LITE |
| ไฟล์ที่ตรวจ | F-WH-STKTRF.html (2,365 บรรทัด · single-file SPA) |
| วันที่ · ผู้ตรวจ | 2026-09-14 · BA gate (html-review-fix-order) |
| เครื่องมือ | node --check · audit.sh (v9) · Playwright walkthrough + bypass catalog |
| ผล Quality Gate | node OK 2 block · audit **FAIL=0** WARN=1 (font-size kit) · Playwright **pageerror=0** |
| **Verdict** | 🔴 **BLOCK** — CRITICAL 2 · HIGH 3 · MINOR 3 |

## 1. สรุปผลตรวจ (Executive Summary)

ระดับ engineering เดียวกับ F082 — guard ฝั่งขาไปทำถูกเกือบหมดและ**พิสูจน์ผ่านการรันแล้ว**: `doShip` guard สถานะ approved + **re-check ยอดคงเหลือต้นทางก่อนของขยับ** (ยอดเปลี่ยน → block พร้อมทางแก้) · `confirmApprove` เดินทีละขั้น + `canActStep` (role/assignee + SoD ผู้ส่งอนุมัติเองไม่ได้ — ทดสอบผู้ไม่มีสิทธิ์แล้ว block จริง) · `openCancelModal` guard "ยกเลิกได้เฉพาะก่อนของขยับ" + ชี้ทางตีกลับ/กลับรายการ · `openReturnModal` guard เฉพาะเจ้าหน้าที่คลังปลายทาง · `confirmReceive` validate ครบ (รับเกิน block ชี้ทางใบปรับยอด · bin จริงบังคับ · เหตุผลส่วนต่างบังคับ) · DOA แยก 2 มิติ (intra/inter) + สายแยกสำหรับตัดส่วนต่าง (write-off) ตามมูลค่า · shortage บังคับแนบหลักฐาน + SoD ผู้ส่งออกเซ็นตัดส่วนต่างไม่ได้ · สองขา issue/receive + in-transit tab + aging + return + reverse — c[] แม่นทั้ง 4 ข้อเชิงโครง

ที่ต้อง **BLOCK** — 3 จุดที่หลุดจากมาตรฐานเดียวกับส่วนอื่นของไฟล์: (1) `confirmReceive` ไม่ guard สถานะและเชื่อ `receiveState` ที่ UI สร้าง — เรียกกับใบ **closed** ได้ ยอด received ทะลุยอดส่ง (100→105) (2) `openReverseModal` ไม่ guard สถานะต้นทาง — กลับรายการใบ **pending_approval ที่ของยังไม่ขยับเลย**ได้ ใบ reversal เกิดเป็น moved + "movement ทิศตรงข้ามครบทุกเส้น" ทั้งที่ขาไปไม่เคยเกิด และ chain hardcode 1 ขั้น auto-approved ข้าม DOA (บทเรียน F082 FIX-03 เป๊ะ) (3) shortage chain — เลือกผู้อนุมัติแล้วระบบ**ปั๊ม approved แทนทุกคนทันที** ผู้อนุมัติตัวจริงไม่ได้กระทำ

### 1.1 ความครบถ้วนเทียบ Spec F083

| Capability | ผล | หมายเหตุ + หลักฐาน |
|---|---|---|
| สร้างใบย้าย + อนุมัติ | ✅ | wizard 5 ขั้น + DOA intra/inter ตามมูลค่า + ทีละขั้น + SoD (T2 ✓) |
| ตัดต้นทาง → in-transit → รับปลายทาง | ✅ กลไก / ❌ guard | doShip guard + re-check ยอด ✓ · in-transit tab + aging ✓ — แต่ receive ไม่ guard (FIX-01) |
| รับขาด/เกินพร้อมเหตุผล | ✅ | เกิน = block ชี้ใบปรับยอด · ขาด = diffAction (รอ/ตีกลับ/ตัด) + เหตุผลบังคับ + shortage DOA แยกสาย |
| พิมพ์เอกสารกำกับการย้าย | ✅ | PDF tab (pdfdoc) |
| d: สองขา กันของหายกลางทาง | ✅ | issue/receive แยกจังหวะ + returned/written-off + หลักฐานแนบ |
| d: ต้นทุนเคลื่อนตามของ | ✅ | มูลค่าจาก totals() เดียว + FWD-WIRE JE posting |
| dec: doa | ⚠️ | chain หลักถูก — shortage chain auto-approved (FIX-03) + reversal ข้าม DOA (FIX-02) |
| dec: ntf · csq | ❌ | grep = 0 ทั้งคู่ (FIX-04) |
| dec: doccfg | ⚠️ | nextCode max-based + pad ✓ — ขาด comment hook ENG-DOC-NUM (FIX-05) |
| Contract F008→F083 (data คลังต้นทาง-ปลายทาง) | ✅ | WAREHOUSES/bin master อ้างในไฟล์ |

## 2. รายการสั่งแก้ (Fix Order)

### FIX-01 · [CRITICAL] confirmReceive ไม่ guard สถานะ + เชื่อ state จาก UI — รับซ้ำบนใบปิดแล้วได้

| ช่อง | รายละเอียด |
|---|---|
| อาการ | function ไม่เช็ค `s.status` และใช้ `receiveState.rows` (rem/take) ที่ UI ประกอบ — เรียกกับใบ closed ได้ ยอด received ทะลุยอดส่ง |
| หลักฐาน | Bypass T6: ใบ closed · received 100 → confirmReceive (inject rows) → received 105 |
| ผลกระทบ | ใบที่ปิดแล้วถูกบวกยอดรับเพิ่มได้ — ยอดคลังปลายทาง/ต้นทุนเพี้ยน |
| ตำแหน่ง | `confirmReceive` (+ `openReceiveModal`) |
| วิธีแก้ | (a) guard: `['in_transit','partial'].includes(s.status)` เท่านั้น (b) ใน function re-derive `rem = lineRemaining(l)` จาก doc จริง แล้ว clamp `take ≤ rem` — ไม่เชื่อค่าจาก state ที่ UI ส่งมา |

เกณฑ์ตรวจรับ: receive กับ closed/closed_diff/moved/draft/pending → block · in_transit/partial รับได้ไม่เกินคงเหลือจริง

### FIX-02 · [CRITICAL] กลับรายการใบที่ของยังไม่ขยับได้ + ใบ reversal ข้าม DOA

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `openReverseModal` เช็คแค่ `reversedBy` — ใบ pending_approval ถูกกลับรายการได้ → ใบ reversal เกิดเป็น `moved` + audit "movement ทิศตรงข้ามครบทุกเส้น" ทั้งที่ขาไปไม่เคยเกิด · chain hardcode `[wh_supervisor approved]` + auto-moved เสมอ ไม่คิด DOA ตามมูลค่า |
| หลักฐาน | Bypass T5: ใบ pending_approval → reverse → `{orig:reversed, rev:{moved, chain:[approved]}}` |
| ผลกระทบ | (a) movement ผี — กลับรายการสิ่งที่ไม่เคยเกิด (b) ช่องอ้อม DOA: reverse ใบมูลค่าสูงได้คนเดียว — ปัญหาเดียวกับ F082 FIX-03 |
| ตำแหน่ง | `openReverseModal` |
| วิธีแก้ | (a) guard สถานะ: กลับรายการได้เฉพาะใบที่ movement เกิดแล้ว — `['moved','closed','closed_diff'].includes(s.status)` (partial/in_transit ใช้ตีกลับคืนต้นทาง) (b) ใบ reversal เดิน DOA ตามมูลค่า: pending_approval + chain จาก `resolveDoa(rev)` → อนุมัติครบ + ship ตามจังหวะปกติ · fast-track ต้องมีมติ (OQ-TRF-01) |

เกณฑ์ตรวจรับ: reverse ใบ draft/pending/in_transit/partial → block พร้อมชี้ทางที่ถูก · ใบ moved/closed → reversal เป็น pending รอ chain ตาม tier · กลับซ้ำไม่ได้คงเดิม

### FIX-03 · [HIGH] shortage chain — เลือกผู้อนุมัติแล้วปั๊ม approved แทนทุกคนทันที

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `confirmShortage` สร้าง `shortage_chain` โดย set `status:'approved', by:assignee, at:now` ทุกขั้นทันที — ผู้รับปลายทางที่กดปุ่มกลายเป็นคนอนุมัติแทนทั้งสาย |
| หลักฐาน | Bypass T4: เลือก slot 'วีระ ชัยมงคล' → chain `['approved']` by วีระ ทั้งที่วีระไม่ได้กด |
| ผลกระทบ | สายอนุมัติตัดส่วนต่าง (write-off มูลค่าจริง) เป็นพิธีกรรม — class เดียวกับ F131 FIX-06 · SoD ที่ออกแบบไว้ (ผู้ส่งออกเซ็นไม่ได้) ไร้ความหมาย |
| ตำแหน่ง | `confirmShortage` |
| วิธีแก้ | สร้าง chain เป็น `pending` ทุกขั้น + `shortage_status:'pending'` — ผู้อนุมัติจริง (canActStep กับ shortage_chain) กดอนุมัติทีละขั้นแบบ chain หลัก · ครบสายค่อย write-off + ปิดใบ closed_diff · หลักฐานแนบ + SoD เดิมคงไว้ |

เกณฑ์ตรวจรับ: ยืนยันตัดส่วนต่าง → ใบคง partial + shortage_chain pending · ผู้อนุมัติจริงกดครบสายแล้วค่อย closed_diff + at ต่อขั้น

### FIX-04 · [HIGH] dec csq + ntf ประกาศแต่ hook = 0

| ช่อง | รายละเอียด |
|---|---|
| อาการ | grep CSQ/7C/ntf/NTF = 0 (FWD-WIRE เป็น wire คนละชั้น) |
| ตำแหน่ง | `doShip` · `confirmReceive` (ปิดใบ) · shortage write-off · reverse |
| วิธีแก้ | ตาม pattern F082: CSQ comments — `trf.shipped` / `trf.received` / `trf.shortage_writeoff` (reversal_of ที่ reverse) → ท่อตาม CSQ_BRIEF_F083 (รอเคาะ OQ-TRF-02) · NTF comments — `trf.shipped → คลังปลายทาง` · `trf.received/shortage → ผู้ส่ง+ต้นทาง` · doa_* ห้ามประกาศซ้ำ (NTF_BRIEF_F083) |

เกณฑ์ตรวจรับ: csq anchor ≥3 จุด · ntf ครบ transition สำคัญ · ไม่ประกาศท่อ/event สงวน

### FIX-05 · [HIGH] doccfg anchor

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `nextCode` max-based + pad ✓ แต่ไม่มี comment hook — ENG-DOC-NUM โผล่เฉพาะ label ผู้ใช้ |
| วิธีแก้ | comment `<!-- เลขจริงจาก ENG-DOC-NUM.next() ตาม doc_type TRF ใน DOCCFG_BRIEF_F083 (F003) · สำเนา PDF ผ่าน ENG-DOC-STORE -->` + ย้ายศัพท์ engine ออกจาก label (FIX-08) |

เกณฑ์ตรวจรับ: comment hook ครบ · label ผู้ใช้ไม่มีศัพท์ engine

### FIX-06 · [MINOR] `_busy` จุดที่เหลือ

confirmApprove/confirmReceive/confirmShortage มี disabled แล้ว — เติม `state._busy` (pattern F101) ที่ `doShip` และ callbacks ของ reasonModal (cancel/return/reverse/reject) · เกณฑ์: double-click ทุก action → ผลครั้งเดียว

### FIX-07 · [MINOR] WARN audit font-size base-kit residual — แก้ตามสะดวก

### FIX-08 · [MINOR·PROD] ศัพท์ dev บนจอ — mark demo-only (กติกา BA)

FWD-WIRE chips/audit notes (27 จุด) · "ENG-DOC-NUM" ใน label เลขที่ · การอ้าง BR ใน copy → ครอบ class `demo-only` + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` · label เปลี่ยนเป็น "ออกเลขอัตโนมัติเมื่อส่งอนุมัติ" · เกณฑ์: inject `.demo-only{display:none}` แล้วไม่เหลือศัพท์ dev + layout ไม่พัง

## 3. สิ่งที่ผ่านและขอคงไว้ (ห้ามแตะตอนแก้)

- `doShip` guard + re-check ยอดต้นทางก่อนของขยับ — จุดแข็งเฉพาะไฟล์นี้
- `confirmApprove` ทีละขั้น + `canActStep` SoD (T2 พิสูจน์แล้ว) · DOA 2 มิติ intra/inter + สาย shortage แยกตามมูลค่า
- `openCancelModal` guard + ชี้ทาง · `openReturnModal` guard คลังปลายทาง · validations ใน confirmReceive (เกิน/bin/เหตุผล)
- B2 totals() เดียว (vat_mode none ตาม contract) · nextCode max-based · in-transit tab + aging · Pattern Q + PDF

## 4. ประเด็นเปิด (OQ)

| รหัส | ประเด็น | ผู้เคาะ | กระทบ |
|---|---|---|---|
| OQ-TRF-01 | นโยบาย DOA ใบกลับรายการ — เดินตามมูลค่าเหมือนใบย้าย หรือ fast-track role ใด (ตอนนี้ hardcode wh_supervisor) — เคาะรวมกับ OQ-ADJ-01 ของ F082 ให้เป็นมาตรฐานเดียว | Strike | 03_LOGIC · DOA_BRIEF |
| OQ-TRF-02 | CSQ profile — shipped/received/shortage_writeoff เข้าท่อไหน (EC ต้นทุนเคลื่อน? AC?) | Strike + Architect | CSQ_BRIEF_F083 |
| OQ-TRF-03 | shortage ที่ผู้อนุมัติปฏิเสธ — ของค้าง in-transit ต่อ หรือบังคับตีกลับต้นทาง | Strike | 03_LOGIC state machine |

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] node --check ผ่าน · audit FAIL=0 · Playwright pageerror=0
- [ ] รันเคส T4/T5/T6 ซ้ำ → block/เดินสายถูกครบ · reversal เดิน DOA
- [ ] anchors (csq/ntf/doccfg) ครบ · demo-only ติดครบ
- [ ] ส่ง re-gate เต็มรอบ (verdict BLOCK)
- [ ] ผ่านแล้ว: อัพเดต FEATURE_REGISTRY (F083) + แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q → Phase B
