# คำสั่งแก้ไข F-WH-STOCKTAKE.html (F084 Stocktake — ตรวจนับใหญ่)

คุณจะแก้ HTML prototype single-file ตามรายการนี้เท่านั้น ห้ามแตะส่วนอื่น
ห้าม regenerate ทั้งไฟล์ — แก้เฉพาะจุด (surgical edit)

## บริบท
- ไฟล์: F-WH-STOCKTAKE.html · html-generator-v9 · arch master (process) · F084 W4 LITE · dec doa + csq
- ส่วนที่ผ่านการตรวจแล้ว **ห้ามเปลี่ยนพฤติกรรม**:
  - blind count: `canSeeSystem()` = supervisor เท่านั้น · ใบนับผู้นับไม่มียอดระบบ
  - `submitCount`: threshold → recount · SoD ผู้นับซ้ำคนละคน (ใน confirmModal assign)
  - `scopesOverlap` กัน scope ทับซ้อน · reject บังคับเหตุผล · ผู้อนุมัติไม่ prefill
  - `beginSubmit` loading state · event log · Esc chain · route

## รายการแก้ (ทำตามลำดับ)

### 1. FIX-01 freezeRound guard — CRITICAL
ตำแหน่ง: `freezeRound`
สิ่งที่ผิด: freeze ซ้ำบนรอบ counting ได้ → status ถอย frozen + snapshot ยอดตั้งต้นถูกเขียนทับ (B1)
แก้เป็น: ต้น function `if(r.status!=='draft'){ toast('ล็อกได้เฉพาะรอบที่ยังเป็นแบบร่าง'); return; }` — snapshot เขียนได้ครั้งเดียว (`if(r.snapshot.length) return;` เป็นชั้นที่สอง)
ตรวจรับ: freeze กับสถานะอื่นที่ไม่ใช่ draft → ไม่เปลี่ยน · snapshot ไม่เปลี่ยนหลัง freeze

### 2. FIX-02 handoff guard — CRITICAL
ตำแหน่ง: `handoff`
สิ่งที่ผิด: handoff บนรอบ counting → closed + ADJ-DRAFT ผี ไม่ผ่านนับ/อนุมัติ (B2)
แก้เป็น: `if(r.status!=='approved'||r.adjustmentRef){ toast('ต้องอนุมัติผลต่างก่อน และสร้างใบปรับได้ครั้งเดียว'); return; }`
ตรวจรับ: handoff เฉพาะ approved · ครั้งเดียว

### 3. FIX-03 confirmModal guard สถานะ + ตัวตน — CRITICAL
ตำแหน่ง: `confirmModal` ทุก branch + ปุ่มใน `renderVariance`/`renderSheets`
สิ่งที่ผิด: persona ผู้นับ approve รอบ counting ได้ (B3) · doa ส่งซ้ำได้ทุกสถานะ · assign ทำได้ทุกสถานะ
แก้เป็น (ต้นแต่ละ branch):
- assign ครั้งแรก: `r.status==='frozen'` · assign ซ้ำ: `r.status==='recount'` · role supervisor
- doa: `r.status==='review'` + role supervisor · ผู้อนุมัติต้องไม่ใช่ assignee/recountAssignee
- approve/reject: `r.status==='pending'` + ผู้กด (persona ปัจจุบัน — เพิ่ม `currentPerson` ผูกกับ role switch) ต้องเท่ากับ `r.approver` + ไม่ใช่ผู้นับ/ผู้นับซ้ำ
- ไม่ผ่าน → toast "สถานะไม่ถูกต้อง" / "ไม่ใช่ผู้มีสิทธิ์ในขั้นนี้" + return
- comment `<!-- SEC: บทบาท/ตัวตนจริงจากล็อกอิน · prototype mirror sec.can() -->`
ตรวจรับ: approve/reject เฉพาะ pending โดย approver จริง · ผู้นับอนุมัติไม่ได้ · doa/assign ผิดสถานะ → block

### 4. FIX-04 มูลค่าส่วนต่าง + DOA ตามวงเงิน — HIGH
ตำแหน่ง: `ITEMS` · `renderVariance` · modal doa
สิ่งที่ผิด: ITEMS ไม่มีต้นทุน → ผลต่างมีแต่จำนวน · doa slot 1 คนตายตัว ไม่มี tier
แก้เป็น:
- เพิ่ม `cost` ต่อ item (mock) + comment `<!-- data: ต้นทุนอ่านจาก Item Master F008 / valuation W5 -->`
- ตารางผลต่างเพิ่มคอลัมน์ มูลค่าส่วนต่าง = diff×cost + Σ|มูลค่า| ท้ายตาราง
- resolve chain: `MOCK_DOA_ENTRY` แบบ F082 (tier ตามฐาน Σ|ส่วนต่าง×ต้นทุน| เช่น <20k 1 ขั้น · ≥20k 2 ขั้น · ≥200k 3 ขั้น) → modal doa สร้าง slots ตามจำนวนขั้น ไม่ prefill · approve เดินทีละขั้น (ทุกขั้นมี by/at) · comment `<!-- DOA_BRIEF_F084: ฐาน = Σ|ส่วนต่าง×ต้นทุน| · tier จาก DOA กลาง (รอเคาะ OQ-STK-04) -->`
ตรวจรับ: ผลต่างแสดงมูลค่า · รอบมูลค่าสูงมีหลาย slot · อนุมัติทีละขั้น

### 5. FIX-05 payload handoff + anchor F082 — HIGH
ตำแหน่ง: `handoff`
แก้เป็น: สร้าง `payload={ ref_count_doc:r.id, scope:r.scope, freezeAt:r.freezeAt, approvedBy:r.approver, lines:r.snapshot.map(s=>({item:s.item, system_qty:s.qty, counted_qty:<final vals>, diff, cost})) }` + `ack={adjId:'ADJ-DRAFT-…', status:'draft'}` เก็บใน `r.handoff` และแสดงในแท็บประวัติ + comment `<!-- CONTRACT: F084 → F082 (flow — ผลตรวจนับใหญ่ → ใบปรับยอด draft · F082 รับผ่าน ref_count_doc) -->`
ตรวจรับ: payload รายบรรทัด + ack + anchor

### 6. FIX-06 lock movement registry + anchor — HIGH
ตำแหน่ง: `freezeRound` / `handoff` / reject
แก้เป็น: `STOCKTAKE_LOCKS` array — push ตอน freeze `{scope, roundId, from}` · remove ตอน closed/rejected · แสดง chip "พื้นที่ถูกล็อก" บนหน้ารอบ · comment `<!-- LOCK: feature movement (GRN/Issue · F083 Transfer · F082 Adjust) ต้องเช็ค STOCKTAKE_LOCKS ก่อน post — scope ทับซ้อน = block · กลไก query รอเคาะ OQ-STK-02 -->`
ตรวจรับ: registry + anchor + ปลดล็อกเฉพาะ closed/rejected

### 7. FIX-07 CSQ + F089 anchors — HIGH
- ที่ approve/handoff: `<!-- CSQ: stocktake.variance_approved / stocktake.handoff → ท่อตาม CSQ_BRIEF_F084 (รอเคาะ OQ-STK-01) · DC มาจาก DOA engine ห้ามซ้ำ -->`
- ที่ใบนับ: ปุ่ม "สแกน" display-only + `<!-- CONTRACT: F089 → F084 (data — ผลสแกน barcode/mobile เข้าช่องผลนับ · prototype คีย์มือแทน) -->`
ตรวจรับ: csq ≥2 · F089 anchor + ปุ่มสแกน

### 8. MINOR รวบ (ทำท้ายสุด)
- FIX-08 (กติกา demo-only): persona switch `class="demo"` + badge DEMO → เพิ่ม class `demo-only` + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` · ทดสอบ `.demo-only{display:none}` → ไม่เหลือ persona/DEMO + layout ปกติ
- FIX-09: font-size base-kit residual — ตามสะดวก

## ข้อห้าม
- ห้ามเพิ่ม dependency/CDN · ห้ามแตะ BASE-KIT · ห้ามเปลี่ยน CI token
- ห้ามแตะ: canSeeSystem/blind rendering, threshold→recount, SoD ผู้นับซ้ำ, scopesOverlap, reject reason, beginSubmit, event log
- ห้ามทำให้ snapshot เขียนทับได้ไม่ว่ากรณีใดหลัง freeze

## หลังแก้เสร็จ ให้รันเองก่อนส่ง
1. node --check
2. audit.sh → FAIL=0
3. Playwright: pageerror=0 + เคส:
   - freeze บน counting → block · snapshot คงเดิม
   - handoff บน counting → block · approved → closed ครั้งเดียว + payload
   - persona ผู้นับ approve → block · approver จริงบน pending → ทีละขั้น
   - ผลต่างมีมูลค่า · รอบ ≥20k มีหลาย slot
   - grep: F082 ≥1 · F089 ≥1 · CSQ ≥2 · STOCKTAKE_LOCKS ≥1
   - blind: ผู้นับยังไม่เห็นยอดระบบ · threshold/SoD ยังทำงาน
   - inject `.demo-only{display:none}` → สะอาด
แนบผลรันกลับมาพร้อมไฟล์ แล้วส่ง re-gate เต็มรอบ (verdict BLOCK)
