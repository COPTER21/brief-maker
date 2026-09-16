# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
Warehouse — F082 Stock Adjustment (ปรับยอด + อนุมัติ) · F-WH-STKADJ.html

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F082 Stock Adjustment · mod Warehouse · W3 · arch **Q-document** · dec: doa + ntf + csq + doccfg + pdfdoc · auto: LITE |
| ไฟล์ที่ตรวจ | F-WH-STKADJ.html (1,129 บรรทัด · single-file SPA) |
| วันที่ · ผู้ตรวจ | 2026-09-14 · BA gate (html-review-fix-order) |
| ขอบเขต | Re-gate ก่อนเข้า Phase B — เทียบ spec F082 + governance + interaction จริง |
| เครื่องมือ | node --check · audit.sh (v9) · Playwright walkthrough + bypass catalog |
| ผล Quality Gate | node OK 2 block · audit **FAIL=0** WARN=3 · Playwright **pageerror=0** · Esc chain ✓ |
| **Verdict** | 🔴 **BLOCK** — CRITICAL 2 · HIGH 4 · MINOR 3 |

## 1. สรุปผลตรวจ (Executive Summary)

ครึ่ง DOA ของไฟล์นี้คือ**ตัวอย่างที่ถูกต้องที่ batch นี้รอมานาน**: `confirmApprove` เดินทีละขั้นจริง (พิสูจน์: chain 2 ขั้น อนุมัติขั้นแรก → เอกสารคง pending ส่งต่อขั้นถัดไป) · `canActStep` ตรวจทั้ง assignee/role และ **SoD — ผู้ส่งอนุมัติเองไม่ได้** · tier ตามมูลค่าปรับ (20k/200k/1M) · ส่งอนุมัติบังคับเลือกผู้อนุมัติครบทุกขั้น (BR-10) + ปุ่ม loading disabled · เลขรัน `nextCode` ตัวนับ global เดินหน้าอย่างเดียว + pad 4 หลัก (บทเรียน F101 ถูกใช้แล้ว) · ตีกลับเป็นร่างเก็บ approval_history append-only · `doReverse` = กลับรายการแบบสร้างใบใหม่ทิศตรงข้าม ผูกคู่ 2 ทาง + BR-18 กลับซ้ำไม่ได้ (ตรง d append-only) · เหตุผลเป็น master (RS-01..) พร้อม dir + GL mapping · FWD-WIRE chips (JE posting · valuation W5) ประกาศแล้ว · Pattern Q view 4 แท็บครบ

ประเด็นที่ต้อง **BLOCK**: ปุ่มถูก gate ตามสถานะแต่ **function ไม่ guard** — pattern เดียวกับที่ตรวจพบทั้ง batch: (1) `doPost` เรียกกับใบ **pending ที่ยังไม่อนุมัติ** ได้ → posted + movement เกิดจริง 4 ตัว = ข้าม DOA ทั้ง chain ในการเรียกเดียว และ post ซ้ำบนใบ posted ได้ (2) ใบ **posted ถูกยกเลิกได้** ทั้งที่ movement เกิดแล้ว — ขัด append-only ตรง ๆ (ทางถูกคือกลับรายการเท่านั้น) และขัด microcopy ตัวเอง (3) `doReverse` hardcode chain 1 ขั้น auto-approved — ใบมูลค่าสูงกลับรายการโดยข้าม tier DOA (4) c[4] trace ใบนับ = 0 ทั้งไฟล์ (5) dec csq + ntf ประกาศแต่ hook = 0

### 1.1 ความครบถ้วนเทียบ Spec F082

| Capability ตามแผน (c[]) | ผล | หมายเหตุ + หลักฐาน |
|---|---|---|
| สร้างใบปรับ + เหตุผลรายบรรทัด | ✅ | wizard 5 ขั้น + reason master รายบรรทัด (RS-xx · dir · needNote · GL) |
| อนุมัติตามวงเงินมูลค่าปรับ (DOA) | ✅ กลไก / ❌ guard | tier ตามมูลค่า + เดินทีละขั้น + SoD ✓ — แต่ doPost ข้ามได้ทั้ง chain (FIX-01) และ reversal ข้าม tier (FIX-03) |
| post แล้วกระทบยอด+ต้นทุนทันที | ⚠️ | movement + มูลค่า + JE "รอลงบัญชี" + FWD-WIRE ✓ — แต่ post ไม่ guard สถานะ (FIX-01) |
| trace กลับใบนับที่เป็นต้นเรื่อง | ❌ | grep ใบนับ/trace/F084/F086 = 0 — contract flow เข้า 2 เส้นไม่มีหลักฐานบนจอ (FIX-04) |
| d: เหตุผลเป็น master | ✅ | REASONS master + filter ตามทิศ |
| d: append-only | ⚠️ | reversal pattern ถูกแบบ + ตีกลับเก็บ history ✓ — แต่ cancel ใบ posted ได้ (FIX-02) |
| dec: doa | ✅ | ครบทั้ง resolve/slot/ทีละขั้น/SoD — ดีที่สุดใน batch |
| dec: ntf | ❌ | grep ntf/NTF = 0 (FIX-05) |
| dec: csq | ❌ | grep CSQ/7C = 0 (FIX-05) |
| dec: doccfg | ⚠️ | เลขรันถูกหลักแล้ว แต่ไม่มี comment hook ENG-DOC-NUM/DOCCFG_BRIEF (FIX-06) — ENG-DOC-NUM โผล่เฉพาะใน label ผู้ใช้ |
| dec: pdfdoc | ✅ | แท็บ PDF Preview |
| Pattern Q archetype | ✅ | list + wizard + view 4 แท็บ + เอกสารแนบ |

## 2. รายการสั่งแก้ (Fix Order)

### FIX-01 · [CRITICAL] doPost ไม่มี precondition guard — post ใบที่ยังไม่อนุมัติได้ (ข้าม DOA ทั้ง chain)

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `doPost` ไม่เช็คสถานะ — เรียกกับใบ pending (chain ยังไม่อนุมัติสักขั้น) ได้ → posted + movement เกิดจริง · เรียกซ้ำบนใบ posted ได้ (audit ปนซ้ำ + movements ถูก regenerate) |
| หลักฐาน | Bypass S1: d3 pending → doPost → `{posted, movements:4}` · S2: double doPost บน approved → audit 4→6 |
| ผลกระทบ | สายอนุมัติตามวงเงิน (c[2]) ถูกข้ามได้ในการเรียกเดียว — ยอด+ต้นทุนกระทบโดยไม่มีใครอนุมัติ |
| ตำแหน่ง | `function doPost(id,useLatest)` |
| วิธีแก้ | guard ต้น function: `if(d.status!=='approved') return showToast('ต้องอนุมัติครบก่อนผ่านรายการ','warning')` — posted/pending/draft/cancelled/reversed → block |

เกณฑ์ตรวจรับ: doPost กับทุกสถานะที่ไม่ใช่ approved → ไม่เปลี่ยน ไม่เกิด movement · approved → posted ครั้งเดียว

### FIX-02 · [CRITICAL] ใบ posted ถูกยกเลิกได้ — ขัด append-only

| ช่อง | รายละเอียด |
|---|---|
| อาการ | callback ของ `openCancel` ไม่เช็คสถานะ — ใบ posted (movement เกิดแล้ว) ถูก cancel ผ่าน modal ได้ ทั้งที่ copy ในไฟล์เขียนเอง "ยกเลิกก่อนผ่านรายการ" |
| หลักฐาน | Bypass S2b: ใบ posted → openCancel + ยืนยัน → `cancelled` |
| ผลกระทบ | เอกสารที่กระทบยอดแล้วหายจากสถานะ posted โดยไม่มี movement กลับ — ขัด d append-only · ทางถูกของใบ posted คือ "กลับรายการ" เท่านั้น |
| ตำแหน่ง | callback ใน `openCancel` |
| วิธีแก้ | guard ใน callback (ไม่ใช่แค่ตอน render ปุ่ม): `if(!['draft','pending'].includes(d.status)) return showToast('ใบผ่านรายการแล้ว — ใช้กลับรายการแทน','warning')` |

เกณฑ์ตรวจรับ: posted/reversed/cancelled/approved → ยกเลิกไม่ได้ + toast ชี้ทางกลับรายการ · draft/pending → ได้ตามเดิม

### FIX-03 · [HIGH] doReverse hardcode chain 1 ขั้น auto-approved — reversal มูลค่าสูงข้าม tier DOA

| ช่อง | รายละเอียด |
|---|---|
| อาการ | ใบกลับรายการถูกสร้างพร้อม `approval_chain:[{WH_LEAD, approved}]` + post ทันทีเสมอ ไม่ว่ามูลค่ากลับรายการจะเข้า tier ไหน (≥20k ต้อง WH_MGR · ≥200k FIN_MGR · ≥1M DIR) |
| หลักฐาน | code `doReverse` hardcode chain + `status:'posted'` ทันที (S6: ใบ mock มูลค่าต่ำจึงไม่ trigger แต่ logic ไม่มีการคิด tier เลย) |
| ผลกระทบ | ช่องอ้อม DOA: post ใบเล็กหลายใบไม่ได้ แต่ reverse ใบใหญ่ได้คนเดียว — มูลค่ากระทบเท่ากับใบปรับปกติ |
| ตำแหน่ง | `doReverse` |
| วิธีแก้ | ใบกลับรายการเดิน DOA ตามมูลค่าเหมือนใบปรับปกติ: สร้างเป็น pending + chain จาก `doaTiers(docAbs(rev))` ให้ผู้มีสิทธิ์อนุมัติแล้วค่อย post · ถ้าทีมต้องการ fast-track ต้องมีมติ (แขวน OQ-ADJ-01) แล้ว comment อ้างมติ |

เกณฑ์ตรวจรับ: reverse ใบมูลค่า ≥20k → ใบกลับรายการเป็น pending รอ chain ตาม tier · มูลค่าต่ำ tier เดียวตามสิทธิ์ · BR-18 กลับซ้ำไม่ได้คงเดิม

### FIX-04 · [HIGH] c[4] trace กลับใบนับ — หายทั้งข้อ

| ช่อง | รายละเอียด |
|---|---|
| อาการ | ไม่มี field/section อ้างอิงใบนับต้นเรื่อง — grep ใบนับ/trace/F084/F086 = 0 ทั้งที่ contract flow เข้า 2 เส้น (F084 ตรวจนับใหญ่ · F086 cycle count → F082) |
| ผลกระทบ | c[4] coverage หาย — FRD เขียน integration ขาเข้าไม่ได้ · เจตนา spec "ทุกการแก้ยอด trace ได้" ขาดครึ่ง |
| ตำแหน่ง | wizard ขั้น 1 (แหล่งที่มา) + view drawer ข้อมูลเอกสาร |
| วิธีแก้ | เพิ่ม field `ref_count_doc` (display-only · optional): wizard ขั้นแรกเลือกแหล่งที่มา "จากใบนับ CNT-xxxx (F084/F086)" หรือ "ปรับตรง" — mock 2-3 ใบนับ · view drawer โชว์ลิงก์ใบนับต้นเรื่อง + comment `<!-- CONTRACT: F084/F086 → F082 (flow — ส่วนต่างจากการนับสร้างใบปรับ + ref กลับ) -->` — ห้าม mock หน้าจอใบนับ |

เกณฑ์ตรวจรับ: ใบปรับที่มาจากใบนับแสดง ref + ลิงก์ (display) · ปรับตรงไม่บังคับ · anchor contract ครบ

### FIX-05 · [HIGH] dec csq + ntf ประกาศแต่ hook = 0 ทั้งไฟล์

| ช่อง | รายละเอียด |
|---|---|
| อาการ | chip ◆csq + 🔔ntf ใน Feature List — grep CSQ/7C/ntf/NTF = 0 (FWD-WIRE JE/valuation มีแล้วแต่เป็น wire คนละชั้น) |
| ผลกระทบ | decl_rule (S1.8) → DIVERGENCE ทั้งสอง chip |
| ตำแหน่ง | `doPost` (จุด post) · `confirmApprove`/`openReject` (แจ้งผล) · `submitForApproval` |
| วิธีแก้ | ตาม pattern F058/F101: (a) CSQ — comment + audit line ที่ doPost: `<!-- CSQ: adj.posted → ท่อตาม CSQ_BRIEF_F082 (มูลค่าปรับกระทบต้นทุน/บัญชี — รอเคาะ OQ-ADJ-02) · ห้ามประกาศ OC/DC ซ้ำ -->` และที่ doReverse (reversal_of ผูกใบเดิม) (b) NTF — comment ต่อจุด: `adj.posted → ผู้สร้างใบ/บัญชี` · `doa_pending/doa_result มาจาก DOA engine ห้ามประกาศซ้ำ (NTF_BRIEF_F082)` |

เกณฑ์ตรวจรับ: anchor csq ≥2 จุด (post + reverse) · ntf ครบทุก transition แจ้งเตือน · ไม่ประกาศท่อ/event สงวน

### FIX-06 · [HIGH] doccfg anchor — เลขรันถูกหลักแล้วแต่ไม่มี comment hook

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `nextCode` ทำถูก (global seq + pad 4) แต่ไม่มี comment ประกาศว่าเลขจริงมาจาก ENG-DOC-NUM ตาม DOCCFG_BRIEF — คำว่า ENG-DOC-NUM โผล่เฉพาะใน label ที่ผู้ใช้เห็น |
| ตำแหน่ง | `nextCode` |
| วิธีแก้ | comment `<!-- เลขจริงจาก ENG-DOC-NUM.next() ตาม doc_type ADJ ใน DOCCFG_BRIEF_F082 — ห้าม feature รันเลขเอง (F003) · สำเนา PDF ผ่าน ENG-DOC-STORE -->` + ย้ายศัพท์ ENG-DOC-NUM ออกจาก label ผู้ใช้ (ดู FIX-09) |

เกณฑ์ตรวจรับ: comment hook ครบ · label ผู้ใช้ไม่มีศัพท์ engine

### FIX-07 · [MINOR] guard กันกดซ้ำใน action ที่เหลือ

| ช่อง | รายละเอียด |
|---|---|
| อาการ | submitForApproval มี disabled+loading แล้ว ✓ แต่ `confirmApprove`/`doPost`/reason callbacks ไม่มี — กดรัวได้ |
| วิธีแก้ | `state._busy` pattern เดียวกับ F101 ครอบ 3 จุด (FIX-01/02 guard สถานะจะกันผลซ้ำส่วนใหญ่อยู่แล้ว — ข้อนี้กัน race UI) |

เกณฑ์ตรวจรับ: double-click ทุก action → ผลครั้งเดียว

### FIX-08 · [MINOR] WARN audit — stepper ไม่ใช้ component กลาง

| ช่อง | รายละเอียด |
|---|---|
| อาการ | Rule #47 — wizard stepper custom ไม่ใช้ `.step-dot` (geometry กลาง #47.1) |
| วิธีแก้ | เปลี่ยนเป็น markup `.stepper > .step-dot` ตาม BASE-KIT v9 |

เกณฑ์ตรวจรับ: audit WARN #47 หาย

### FIX-09 · [MINOR·PROD] ศัพท์ dev ในข้อความผู้ใช้ — mark demo-only (กติกา BA)

| ช่อง | รายละเอียด |
|---|---|
| อาการ | ข้อความที่ผู้ใช้เห็นมีศัพท์ dev: label "(ร่าง — ยังไม่ออกเลขที่ · ออกโดย **ENG-DOC-NUM** ตอนส่งอนุมัติ)" · chip **FWD-WIRE: JE posting / valuation engine** · การอ้าง **BR-15/BR-18/BR-10** ใน toast/คำอธิบาย modal |
| วิธีแก้ | ตามกติกา demo-only (F059): chip FWD-WIRE + BR-xx refs ครอบ class `demo-only` + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` · label ผู้ใช้เปลี่ยนเป็น "ออกเลขอัตโนมัติเมื่อส่งอนุมัติ" (ศัพท์ engine ไปอยู่ comment FIX-06) · ทดสอบ `.demo-only{display:none}` layout ไม่พัง |

เกณฑ์ตรวจรับ: ซ่อน demo-only แล้วไม่เหลือศัพท์ dev (ENG-DOC-NUM/FWD-WIRE/BR-xx) บนจอ

## 3. สิ่งที่ผ่านและขอคงไว้ (ห้ามแตะตอนแก้)

- `confirmApprove` เดินทีละขั้น + `canActStep` (role/assignee + SoD ผู้ส่งอนุมัติเองไม่ได้) — **ต้นแบบ DOA ของ batch ให้ทีม vibe ใช้แก้ F102/F131/F101**
- `doaTiers` ตามมูลค่า + signProgress + BR-10 บังคับเลือกคนครบ + loading disabled
- `nextCode` global seq + pad · `openReject` ตีกลับเป็นร่าง + approval_history append-only
- `doReverse` โครง reversal (ใบใหม่ทิศตรงข้าม + ผูกคู่ + BR-18) — แก้เฉพาะ chain ตาม FIX-03
- REASONS master + GL mapping · FWD-WIRE declarations · Pattern Q view 4 แท็บ · Esc chain

## 4. ประเด็นเปิด (OQ) — ต้องเคาะก่อนเขียน FRD

| รหัส | ประเด็น | ผู้เคาะ | กระทบ (ส่วน FRD) |
|---|---|---|---|
| OQ-ADJ-01 | นโยบายอนุมัติใบกลับรายการ — เดิน DOA ตามมูลค่าเหมือนใบปรับ หรือ fast-track ให้ role ใด (ตอนนี้ hardcode WH_LEAD คนเดียว) | Strike | 03_LOGIC · DOA_BRIEF |
| OQ-ADJ-02 | CSQ profile ตอน post — มูลค่าปรับเข้า EC (ต้นทุน) และ/หรือ AC (ลงบัญชี) · reversal ผูก reversal_of อย่างไร | Strike + Architect | CSQ_BRIEF_F082 |
| OQ-ADJ-03 | JE "รอลงบัญชี" — trigger ลง JE จริงเป็นของ F093 (W5) ตาม FWD-WIRE: ยืนยันรูปแบบ contract (flow หรือ data) ก่อนเขียน §Integration | Strike | §Integration |

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] node --check ทุก script block ผ่าน
- [ ] audit.sh FAIL=0
- [ ] Playwright pageerror=0 ทุก route/drawer/modal
- [ ] รันเคส S1/S2/S2b/S6 ซ้ำ → ถูก block ครบ · reversal เดิน DOA ตาม tier
- [ ] trace ใบนับ + anchors (csq/ntf/doccfg/contract) ครบ · demo-only ติดครบ
- [ ] ส่งไฟล์กลับ re-gate เต็มรอบ (verdict BLOCK)
- [ ] ผ่านแล้ว: อัพเดต FEATURE_REGISTRY (BA status F082) + แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q → เข้า Phase B
