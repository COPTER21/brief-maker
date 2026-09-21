# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
Warehouse — F084 Stocktake (ตรวจนับใหญ่) · F-WH-STOCKTAKE.html

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F084 Stocktake · mod Warehouse · W4 · arch master (process) · dec: doa + csq · auto: LITE |
| ไฟล์ที่ตรวจ | F-WH-STOCKTAKE.html (32 KB · single-file SPA · compact build) |
| วันที่ · ผู้ตรวจ | 2026-09-20 · BA gate (html-review-fix-order) |
| เครื่องมือ | node --check · audit.sh (v9) · Playwright walkthrough + bypass catalog |
| ผล Quality Gate | node OK 2 block · audit **FAIL=0** WARN=1 (font-size kit) · Playwright **pageerror=0** · Esc ✓ |
| **Verdict** | 🔴 **BLOCK** — CRITICAL 3 · HIGH 4 · MINOR 2 |

## 1. สรุปผลตรวจ (Executive Summary)

โครง process ตรงกับ spec ครบทั้ง 5 ข้อและตรรกะเฉพาะทางทำถูก — **พิสูจน์แล้ว**: freeze กัน scope ทับซ้อนกับรอบที่ยังเปิด + เก็บ snapshot ยอดตั้งต้น · **blind count จริง** (persona ผู้นับไม่เห็นยอดระบบบนใบนับ — ตรวจแล้วเลข 12 ไม่รั่ว) · ผลต่างเกิน `varianceThreshold` → บังคับนับซ้ำรอบ 2 และ **SoD ผู้นับซ้ำต้องเป็นคนละคน** (block จริง) · reject บังคับเหตุผล · เลือกผู้อนุมัติไม่ prefill · ปุ่มทุกตัวมี loading state · event log ทุก transition · handoff ปิดรอบ + ปลดล็อก

ประเด็นที่ต้อง **BLOCK** — pattern เดิมของ batch "ปุ่มถูก gate แต่ function ไม่ guard" แต่รอบนี้กระทบ**ความน่าเชื่อถือของผลนับโดยตรง**: (1) `freezeRound` เรียกซ้ำบนรอบที่**กำลังนับ**ได้ → สถานะถอยเป็น frozen และ **snapshot ยอดตั้งต้นถูกเขียนทับ** = ฐานเทียบส่วนต่างเปลี่ยนกลางคัน (2) `handoff` เรียกบนรอบ counting ได้ → ปิดรอบ + สร้าง ADJ-DRAFT ผีโดย**ไม่ผ่านการนับและอนุมัติเลย** — ข้าม c[5] ทั้งก้อน (3) `confirmModal('approve')` ไม่เช็คทั้งสถานะและตัวตน → persona ผู้นับอนุมัติผลต่างของรอบที่ยังนับอยู่ได้ · นอกจากนี้ DOA เป็น slot 1 คนตายตัว ไม่มีมูลค่าส่วนต่าง (ITEMS ไม่มีราคา) จึง resolve chain ตามวงเงินไม่ได้ · handoff ไป F082 เป็นแค่ string `ADJ-DRAFT-001` ไม่มี payload ส่วนต่าง · lock movement มีแต่ข้อความใน log ไม่มี anchor ให้ feature movement เช็ค · csq + F089 (สแกน) = 0

### 1.1 ความครบถ้วนเทียบ Spec F084

| Capability ตามแผน (c[]) | ผล | หมายเหตุ + หลักฐาน |
|---|---|---|
| วางแผนนับ + freeze scope | ⚠️ | สร้างรอบ + freeze + กัน scope ทับซ้อน ✓ — freeze ซ้ำทับ snapshot ได้ (FIX-01) · lock movement ไม่มี anchor (FIX-06) |
| ใบนับแบบ blind count | ✅ | canSeeSystem = supervisor เท่านั้น · ใบนับผู้นับไม่มียอดระบบ (พิสูจน์แล้ว) |
| คีย์/สแกนผลนับ + นับซ้ำ | ⚠️ | คีย์ ✓ · threshold → recount ✓ · SoD ✓ — **สแกน (F089 data) = 0** (FIX-07) |
| สรุปส่วนต่าง → สร้าง Stock Adjustment อัตโนมัติ | ⚠️ | ตารางผลต่าง ✓ · handoff สร้างแค่ string ADJ-DRAFT ไม่มี payload/anchor F082 (FIX-05) และเรียกได้ทุกสถานะ (FIX-02) |
| อนุมัติผลก่อนปรับ | ❌ guard | เลือกผู้อนุมัติ + approve/reject มี — แต่ approve ไม่ guard สถานะ/ตัวตน (FIX-03) · chain 1 คนตายตัว ไม่มีฐานมูลค่า (FIX-04) |
| d: นับซ้ำรอบ 2 เมื่อเกิน threshold | ✅ | inventoryConfig.varianceThreshold + recount + SoD |
| d: lock movement ตาม scope | ❌ | มีแต่ log "ล็อกการเคลื่อนไหว" — ไม่มี hook/anchor ให้ F082/F083/GRN/Issue เช็ค (FIX-06) |
| dec: doa | ⚠️ | slot 1 คน hardcode · ไม่มี resolve ตามมูลค่าส่วนต่าง (FIX-04) |
| dec: csq | ❌ | grep CSQ/7C = 0 (FIX-07) |
| Contracts F084→F082 flow · F089→F084 data | ❌ | grep F082 = 0 · F089 = 0 (FIX-05/07) |

## 2. รายการสั่งแก้ (Fix Order)

### FIX-01 · [CRITICAL] freezeRound ไม่ guard สถานะ — freeze ซ้ำระหว่างนับ ทับ snapshot ยอดตั้งต้น

| ช่อง | รายละเอียด |
|---|---|
| อาการ | เรียก `freezeRound` กับรอบสถานะ counting ได้ → status ถอยเป็น frozen · `r.snapshot` ถูก regenerate จากยอดปัจจุบัน · freezeAt เปลี่ยน |
| หลักฐาน | Bypass B1: ST-2026-001 counting · แก้ ITEMS qty แล้ว freeze → `{frozen, snapshot changed:true, freezeAt 09-14 → 09-20}` |
| ผลกระทบ | ฐานเทียบส่วนต่างเปลี่ยนกลางรอบ — ผลนับที่คีย์ไปแล้วเทียบกับยอดคนละชุด = ผลตรวจนับใช้ไม่ได้ |
| ตำแหน่ง | `freezeRound` |
| วิธีแก้ | guard `r.status==='draft'` เท่านั้น — อื่น toast + return · snapshot เป็น immutable หลัง freeze (ห้ามเขียนทับทุกเส้นทาง) |

เกณฑ์ตรวจรับ: freeze กับ frozen/counting/recount/review/pending/approved/closed → ไม่เปลี่ยน · draft → frozen ครั้งเดียว

### FIX-02 · [CRITICAL] handoff ไม่ guard สถานะ — ปิดรอบ + สร้างใบปรับผีโดยไม่ผ่านนับ/อนุมัติ

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `handoff` เรียกบนรอบ counting ได้ → status closed + adjustmentRef ADJ-DRAFT-001 + ปลดล็อก |
| หลักฐาน | Bypass B2: counting → handoff → `{closed, adj:'ADJ-DRAFT-001'}` |
| ผลกระทบ | ข้าม c[5] "อนุมัติผลก่อนปรับ" ทั้งก้อน — ใบปรับยอดถูกสร้างจากผลนับที่ยังไม่ครบและไม่มีใครอนุมัติ |
| ตำแหน่ง | `handoff` |
| วิธีแก้ | guard `r.status==='approved'` เท่านั้น + handoff ได้ครั้งเดียว (`adjustmentRef` ว่างเท่านั้น) |

เกณฑ์ตรวจรับ: handoff กับสถานะอื่นที่ไม่ใช่ approved → block · approved → closed + ref ครั้งเดียว

### FIX-03 · [CRITICAL] approve/reject/doa ไม่ guard สถานะและตัวตน — ผู้นับอนุมัติเองได้

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `confirmModal` ไม่เช็ค (a) สถานะรอบ (b) ว่าผู้กดคือ `r.approver` — persona ผู้นับ อนุมัติรอบที่ยังนับอยู่ได้ · ส่งอนุมัติ (doa) ซ้ำได้ทุกสถานะ |
| หลักฐาน | Bypass B3: role counter · round counting → confirmModal approve → `approved` |
| ผลกระทบ | สายอนุมัติเป็นพิธีกรรม + toxic pair (ผู้นับ = ผู้อนุมัติผลตัวเอง) |
| ตำแหน่ง | `confirmModal` (ทุก branch) + ปุ่มใน renderVariance |
| วิธีแก้ | guard ต่อ branch: doa → เฉพาะ review + role supervisor · approve/reject → เฉพาะ pending + ผู้กดต้องเป็น `r.approver` (persona ปัจจุบัน) + ห้ามเป็น assignee/recountAssignee (SoD) · assign → เฉพาะ frozen (ครั้งแรก) / recount (ซ้ำ) · comment `<!-- SEC: บทบาทจริงจากล็อกอิน · mirror sec.can() -->` |

เกณฑ์ตรวจรับ: approve/reject ทำได้เฉพาะ pending โดย approver จริง · ผู้นับ/ผู้นับซ้ำอนุมัติไม่ได้ · doa ซ้ำบน pending/approved → block

### FIX-04 · [HIGH] DOA slot 1 คนตายตัว — ไม่มีมูลค่าส่วนต่าง จึง resolve chain ตามวงเงินไม่ได้

| ช่อง | รายละเอียด |
|---|---|
| อาการ | modal doa = 1 slot เสมอ · ITEMS ไม่มีต้นทุน/ราคา → ตารางผลต่างมีแต่จำนวน ไม่มีมูลค่า · dec doa ประกาศแต่ไม่มี resolve/tier |
| ผลกระทบ | ผลต่างมูลค่าสูงกับต่ำเดินสายเดียวกัน — ขัดหลัก DOA ตามวงเงิน (F082 ปลายทางใช้ tier ตามมูลค่า 20k/200k/1M) |
| ตำแหน่ง | `ITEMS` · `renderVariance` · modal doa |
| วิธีแก้ | เพิ่ม `cost` ต่อ item (mock อ่านจาก Item Master F008 — comment data contract) → ตารางผลต่างแสดงมูลค่า Σ|diff×cost| · resolve chain จาก DOA กลางตามฐาน "มูลค่าส่วนต่างสัมบูรณ์" (pattern F082: slots ตาม tier · ไม่ prefill · เดินทีละขั้น) · comment `<!-- DOA_BRIEF_F084: ฐาน = Σ|ส่วนต่าง×ต้นทุน| · tier ตาม DOA กลาง -->` |

เกณฑ์ตรวจรับ: ผลต่างแสดงมูลค่า · รอบมูลค่าสูงมี slot หลายขั้น · อนุมัติทีละขั้น

### FIX-05 · [HIGH] handoff ไป F082 เป็นแค่ string — ไม่มี payload ส่วนต่าง + ไม่มี anchor contract

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `r.adjustmentRef='ADJ-DRAFT-'+…` เท่านั้น · grep F082 = 0 · contract F084→F082 (flow) ประกาศใน Feature List |
| ผลกระทบ | F082 รับใบปรับจากใบนับไม่ได้เพราะไม่รู้ว่าต้องรับอะไร (F082 FIX-04 กำลังเพิ่ม `ref_count_doc` รออยู่) |
| ตำแหน่ง | `handoff` |
| วิธีแก้ | สร้าง payload แบบ F085→F072: `{ref_count_doc:r.id, scope, freezeAt, approvedBy, lines:[{item, system_qty, counted_qty, diff, reason?}]}` + ack `{adjId, status:'draft'}` แสดงในแท็บประวัติ · comment `<!-- CONTRACT: F084 → F082 (flow — ผลตรวจนับใหญ่ → ใบปรับยอด draft · payload/ack นี้) -->` |

เกณฑ์ตรวจรับ: handoff สร้าง payload รายบรรทัด + ack · anchor contract ครบ

### FIX-06 · [HIGH] lock movement ตาม scope — มีแต่ข้อความใน log

| ช่อง | รายละเอียด |
|---|---|
| อาการ | freeze เขียน log "ล็อกการเคลื่อนไหวเฉพาะ scope" แต่ไม่มี state/anchor ที่ feature movement (GRN/Issue/Transfer/Adjust) จะเช็ค |
| ผลกระทบ | d "ระหว่างนับ lock movement ตาม scope" ไม่มีที่ยึดสำหรับ FRD/Integration |
| ตำแหน่ง | `freezeRound` / `handoff` |
| วิธีแก้ | เพิ่ม registry `STOCKTAKE_LOCKS=[{scope, roundId, from, to}]` ตอน freeze/unlock + comment `<!-- LOCK: feature movement ทุกตัว (F081 GRN/Issue · F083 Transfer · F082 Adjust) ต้องเช็ค STOCKTAKE_LOCKS ก่อน post — scope ทับซ้อน = block · อ่านผ่าน ENG หรือ API F084 (รอเคาะ OQ-STK-02) -->` + แสดง "พื้นที่ถูกล็อก" บนหน้ารอบ |

เกณฑ์ตรวจรับ: มี lock registry + anchor · ปลดล็อกตอน closed/rejected เท่านั้น

### FIX-07 · [HIGH] dec csq = 0 · contract F089 (สแกน) = 0

| ช่อง | รายละเอียด |
|---|---|
| อาการ | chip ◆csq ประกาศ — grep CSQ/7C = 0 · c[3] "คีย์/**สแกน**ผลนับ" + contract F089→F084 (data สแกนตรวจนับ) — grep สแกน/F089 = 0 |
| วิธีแก้ | comment anchors: `<!-- CSQ: stocktake.variance_approved / stocktake.handoff → ท่อตาม CSQ_BRIEF_F084 (รอเคาะ OQ-STK-01) · DC มาจาก DOA engine ห้ามซ้ำ -->` · ที่ใบนับ: `<!-- CONTRACT: F089 → F084 (data — ผลสแกน barcode/mobile เข้าช่องผลนับ · prototype คีย์มือแทน) -->` + ปุ่ม "สแกน" display-only |

เกณฑ์ตรวจรับ: csq anchor ≥2 · F089 anchor + ปุ่มสแกน display-only

### FIX-08 · [MINOR·PROD] demo-only (กติกา BA)

persona switch มี `class="demo" data-demo="persona-switch"` + badge DEMO — เปลี่ยน/เพิ่ม class **`demo-only`** + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` · เกณฑ์: inject `.demo-only{display:none}` แล้วไม่เหลือ persona switch/DEMO บนจอ + layout ไม่พัง

### FIX-09 · [MINOR] WARN audit font-size base-kit residual — แก้ตามสะดวก

## 3. สิ่งที่ผ่านและขอคงไว้ (ห้ามแตะตอนแก้)

- blind count (`canSeeSystem`) — ผู้นับไม่เห็นยอดระบบ (พิสูจน์แล้ว)
- threshold → recount + SoD ผู้นับซ้ำคนละคน · reject บังคับเหตุผล · ผู้อนุมัติไม่ prefill
- freeze กัน scope ทับซ้อน (`scopesOverlap`) + snapshot ตอน freeze (ทำให้ immutable ตาม FIX-01)
- `beginSubmit` loading state ทุกปุ่ม · event log ทุก transition · Esc chain

## 4. ประเด็นเปิด (OQ)

| รหัส | ประเด็น | ผู้เคาะ | กระทบ |
|---|---|---|---|
| OQ-STK-01 | CSQ profile — variance_approved / handoff เข้าท่อไหน · consequence ต้นทุนเป็นของ F084 หรือของใบปรับ F082 | Strike + Architect | CSQ_BRIEF_F084 |
| OQ-STK-02 | กลไก lock movement — F084 เป็นเจ้าของ lock registry ให้ feature อื่น query หรือลง ENG กลาง · movement ที่ค้าง in-transit ข้าม scope ทำอย่างไร | Strike + Architect | §Integration · 03_LOGIC |
| OQ-STK-03 | นับซ้ำรอบ 2 แล้วยังเกิน threshold → ไป review เลย (ตามไฟล์) หรือต้องนับรอบ 3/หัวหน้าตัดสิน | Strike | 03_LOGIC state machine |
| OQ-STK-04 | ฐาน DOA ของผลตรวจนับ = มูลค่าส่วนต่างสัมบูรณ์รวมทั้งรอบ หรือแยกรายบรรทัด · tier ใช้ชุดเดียวกับ F082 หรือไม่ | Strike | DOA_BRIEF_F084 |

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] node --check ผ่าน · audit FAIL=0 · Playwright pageerror=0
- [ ] รันเคส B1/B2/B3 ซ้ำ → block ครบ · approve เฉพาะ approver จริงบน pending
- [ ] มูลค่าส่วนต่าง + DOA tier · payload handoff + anchors (F082/F089/csq/lock)
- [ ] demo-only ติดครบ · blind/threshold/SoD เดิมยังทำงาน
- [ ] ส่ง re-gate เต็มรอบ (verdict BLOCK)
- [ ] ผ่านแล้ว: อัพเดต FEATURE_REGISTRY (F084) + แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q → Phase B
