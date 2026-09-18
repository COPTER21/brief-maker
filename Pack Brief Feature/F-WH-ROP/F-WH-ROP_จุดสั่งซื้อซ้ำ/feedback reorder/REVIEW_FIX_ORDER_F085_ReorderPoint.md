# รายงานผลตรวจและใบสั่งแก้ไข (Review & Fix Order)
Warehouse — F085 Reorder Point (จุดสั่งเติม) · F-WH-ROP.html

| หัวข้อ | รายละเอียด |
|---|---|
| Feature | F085 Reorder Point · mod Warehouse · W4 · arch **master** · dec: ntf + csq · auto: FULL |
| ไฟล์ที่ตรวจ | F-WH-ROP.html (54 KB · single-file SPA · compact build) |
| วันที่ · ผู้ตรวจ | 2026-09-14 · BA gate (html-review-fix-order) |
| เครื่องมือ | node --check · audit.sh (v9) · Playwright walkthrough + bypass catalog |
| ผล Quality Gate | node OK 1 block · audit **FAIL=0** WARN=1 (font-size kit) · Playwright **pageerror=0** · Esc ✓ |
| **Verdict** | 🟠 **BLOCK (รอบแก้สั้น)** — CRITICAL 0 · HIGH 4 · MINOR 3 |

## 1. สรุปผลตรวจ (Executive Summary)

ไฟล์ตระกูล automation (ไม่ใช่เอกสาร) ที่ **engine ถูกหลักที่สุดใน batch** — ไม่มี CRITICAL: สูตรคำนวณ verify แล้วตรงนิยาม (`raw = max − ATP − onOrder + ADU×leadTime` → ปัดขึ้นตาม packSize · ตัวอย่าง ITEM-101: 30−8−0+2×7 = 36 · pack 12 → 36 ✓) · **idempotency key ทุกเส้นทาง** — recompute ซ้ำไม่สร้าง event ซ้ำ (พิสูจน์: events 5 → 5) ทั้ง suggestion / notification / PR draft พร้อม `replay:true` · **PR เป็น draft เท่านั้น ห้าม auto-submit เข้า DOA** (ack `submitted:false`) และรวม 1 PR ต่อคลังต่อรอบพร้อม `ref_external` + `source_policy` + `source_snapshot` ต่อบรรทัด (trace กลับได้) · นโยบายมี **version + effectiveDate** (อ่านนโยบายที่มีผล ณ วันนั้น) · validation แน่น `0 ≤ safety ≤ min ≤ max` + ตรวจ master จริง (พิสูจน์ 4 เคสเจาะ ไม่มีเคสหลุด) · edge code ชัด (`NO_POLICY` / `SNAPSHOT_UNAVAILABLE`) · ATP อ่านสำเร็จรูปจาก F009 พร้อม `asOf` ห้ามหัก reserved ซ้ำ · NTF envelope ครบ (eventType/tenantId/policyRef/policyVersion/idempotencyKey)

ที่ให้ **BLOCK รอบสั้น** คือช่องว่างเชิง spec/declaration ไม่ใช่ logic พัง: (1) **safety stock ตั้งได้ แต่ไม่มีผลต่ออะไรเลย** — ไม่อยู่ในเงื่อนไข trigger และไม่อยู่ในสูตรจำนวนแนะนำ ทั้งที่ c[1] และ d ระบุเป็น input หลัก (2) c[2] "ตรวจ**ทุกวัน**และ**ทุก movement**" มีแต่ข้อความใน rules + ปุ่มกดเอง — ไม่มี hook/anchor ของ scheduler หรือ movement event (3) dec **csq hook = 0** และ contract **F085→F072 (flow → PR)** ไม่มี anchor ทั้งที่ payload ส่ง PR จริง (4) **โค้ด scaffold ของ feature อื่นค้างในไฟล์** (F-WH-QHOLD / F-WH-CYCLE / F-WH-LOT / F-ACC-LC) — ปุ่ม "ขอปล่อยกัก / บันทึกผลนับ / คำนวณจัดสรร" ของ feature อื่นอยู่ในโค้ดเดียวกัน

### 1.1 ความครบถ้วนเทียบ Spec F085

| Capability ตามแผน (c[]) | ผล | หมายเหตุ + หลักฐาน |
|---|---|---|
| ตั้ง min/max/safety รายสินค้า×คลัง | ⚠️ | ตั้งครบ + version/effectiveDate + validation ✓ — แต่ **safety ไม่ถูกใช้ในสูตรใด ๆ** (FIX-01) |
| ตรวจอัตโนมัติทุกวัน/ทุก movement | ❌ | มีปุ่ม "รันรอบตรวจ" (manual) + rules text — ไม่มี anchor scheduler/movement (FIX-02) |
| สร้าง PR draft อัตโนมัติ + รวมรายการ | ✅ | รวม 1 PR ต่อคลังต่อรอบ + draft ไม่ submit + idempotent + payload trace ครบ |
| รายงานสินค้าใกล้หมด | ⚠️ | แท็บคำแนะนำมี ATP/On-Order/ADU/แนะนำ ✓ — แต่มีแค่ 2 สถานะ (ต่ำกว่าจุด / ยังไม่ต่ำ) ไม่มีชั้น "ใกล้จุด" ที่คำว่า *ใกล้หมด* หมายถึง (FIX-04) |
| d: min/max + lead time ของ vendor ประกอบจำนวนแนะนำ | ⚠️ | leadTime + ADU + packSize เข้าสูตรครบ · `preferredVendor` มีใน policy แต่ตั้งค่าไม่ได้จาก UI (hardcode seed) |
| dec: ntf | ✅ | envelope + idempotencyKey + policyVersion — ดีที่สุดในหมู่ไฟล์ automation |
| dec: csq | ❌ | grep CSQ/7C = 0 (FIX-03) |
| Contract F085→F072 (flow → PR) | ❌ | grep F072 = 0 — payload ส่ง PR จริงแต่ไม่ประกาศปลายทาง (FIX-03) |

## 2. รายการสั่งแก้ (Fix Order)

### FIX-01 · [HIGH] safety stock ไม่ถูกใช้ในตรรกะใด ๆ

| ช่อง | รายละเอียด |
|---|---|
| อาการ | `ropEvaluatePair` ใช้ min (trigger) · max/onOrder/ADU/leadTime/pack (จำนวน) — **ไม่มี safety** · safety ปรากฏเฉพาะตอน validate/แสดงผล/เก็บลงนโยบาย |
| หลักฐาน | grep safety: validate + form + column + policy object เท่านั้น · formula check: `{raw:36 = max30 − atp8 − onOrder0 + adu2×lead7}` ไม่มี safety |
| ผลกระทบ | ผู้ใช้ตั้ง safety stock แล้วพฤติกรรมไม่เปลี่ยน — c[1] และ d ระบุเป็น input หลัก · FRD จะเขียนสูตรจาก prototype แล้วได้สูตรที่ทิ้งฟิลด์ |
| ตำแหน่ง | `ropEvaluatePair` |
| วิธีแก้ | เลือกนิยาม 1 แบบแล้วใส่ให้ครบทั้ง trigger และ qty โดยเคาะกับ Strike (OQ-ROP-01): แนวมาตรฐาน — reorder point = `safety + ADU×leadTime` (trigger เมื่อ ATP ต่ำกว่าค่านี้ หรือต่ำกว่า min แล้วแต่ policy) และ target = `max + safety` · แสดงบรรทัดคำนวณบนจอ ("ต่ำกว่าจุด เพราะ ATP 8 < จุดสั่งเติม 19 = safety 5 + 2×7") ให้ FRD คัดลอกได้ตรง · ถ้าทีมตั้งใจให้ safety เป็น "ตัวเลขอ้างอิงเฉย ๆ" ต้องเขียนมติกำกับในไฟล์ |

เกณฑ์ตรวจรับ: เปลี่ยน safety แล้วผลลัพธ์ trigger/qty เปลี่ยนตามนิยามที่เคาะ · จอแสดงที่มาของตัวเลขทุกตัว

### FIX-02 · [HIGH] c[2] ไม่มี anchor ของ "ตรวจทุกวัน / ทุก movement"

| ช่อง | รายละเอียด |
|---|---|
| อาการ | การตรวจเกิดจากปุ่ม "รันรอบตรวจ" เท่านั้น · คำว่าทุกวัน/ทุก movement อยู่ใน `CFG.rules` (ข้อความ) — ไม่มี comment/hook ให้ dev ผูก scheduler หรือ subscribe movement event |
| ผลกระทบ | c[2] เป็นหัวใจของ feature (automation) แต่ FRD จะไม่มีที่ยึดสำหรับ trigger จริง |
| ตำแหน่ง | `ropRecompute` |
| วิธีแก้ | comment anchor: `<!-- TRIGGER: (1) scheduler รายวัน 06:00 ต่อ tenant → ropRecompute ทั้ง catalog (2) subscribe movement events ที่ทำให้ ATP เปลี่ยน (GRN/Issue/Transfer/Adjust/Reserve) → evaluate เฉพาะคู่ item×warehouse ที่กระทบ · ปุ่มบนจอ = manual run สำหรับทดสอบ -->` + แสดง "ตรวจอัตโนมัติล่าสุด: …" (mock) ข้างปุ่ม |

เกณฑ์ตรวจรับ: มี anchor ครบ 2 ทาง (เวลา + event) · จอสื่อว่าปุ่มคือ manual run

### FIX-03 · [HIGH] dec csq hook = 0 · contract F085→F072 ไม่มี anchor

| ช่อง | รายละเอียด |
|---|---|
| อาการ | chip ◆csq ประกาศใน Feature List — grep CSQ/7C = 0 · payload PR ถูกสร้างจริงแต่ไม่ระบุว่าปลายทางคือ F072 (Purchase Requisition) ตาม contract flow |
| ผลกระทบ | decl_rule (S1.8) → DIVERGENCE · FRD เขียน §Integration ขาเข้า-ออกไม่ได้ |
| ตำแหน่ง | `ropPreparePR` · `ropNcCandidate` |
| วิธีแก้ | (a) `<!-- CONTRACT: F085 → F072 (flow — ต่ำกว่าจุดสั่งเติม สร้าง PR draft · payload/ack ตามสัญญานี้) · ATP/On-Order อ่านจาก F009 (data) -->` (b) `<!-- CSQ: rop.pr_draft_created / rop.threshold_breached → ท่อตาม CSQ_BRIEF_F085 (รอเคาะ OQ-ROP-02) · ห้ามประกาศ OC/DC ซ้ำ -->` |

เกณฑ์ตรวจรับ: anchor contract 2 เส้น (F072 ออก · F009 เข้า) + csq ≥1 จุด

### FIX-04 · [HIGH] โค้ด scaffold ของ feature อื่นค้างในไฟล์ + c[4] ไม่มีชั้น "ใกล้จุด"

| ช่อง | รายละเอียด |
|---|---|
| อาการ | (a) `domainView`/`domainAction` มีสาขาของ F-WH-LOT / F-WH-QHOLD / F-WH-CYCLE / F-ACC-LC — ปุ่ม "ขอปล่อยกัก / บันทึกผลนับ / คำนวณจัดสรร" ของ feature อื่นอยู่ในไฟล์นี้ · `stats()`/`validate()` generic เวอร์ชัน scaffold ยังค้าง (ถูก override ด้วยเวอร์ชัน ROP แต่โค้ดตายยังอยู่) (b) แท็บคำแนะนำมีแค่ 2 สถานะ ไม่มีชั้น "ใกล้จุด" ที่ c[4] *รายงานสินค้าใกล้หมด* สื่อถึง · ป้ายสถานะ "ต่ำกว่าจุด" ใช้ pill สีเขียวเหมือน "ยังไม่ต่ำกว่าจุด" |
| ผลกระทบ | dev หยิบไฟล์ไป implement แล้วลาก logic feature อื่นติดไป · ผู้ใช้กวาดตาแล้วแยกไม่ออกว่ารายการไหนวิกฤต |
| ตำแหน่ง | `domainView` · `domainAction` · generic `stats`/`validate`/`saveRecord` · ตาราง suggestions |
| วิธีแก้ | (a) ลบสาขา/ฟังก์ชัน scaffold ที่ไม่ใช่ ROP ออกให้หมด (b) เพิ่มชั้น "ใกล้จุด" (เช่น ATP ≤ min×1.2 หรือคาดว่าจะถึงจุดภายใน lead time) + สีป้าย 3 ระดับ (แดง=ต่ำกว่าจุด · ส้ม=ใกล้จุด · เขียว=ปกติ) + KPI card "ใกล้จุด" |

เกณฑ์ตรวจรับ: grep F-WH-QHOLD/F-WH-CYCLE/F-WH-LOT/F-ACC-LC = 0 · ตารางคำแนะนำมี 3 ระดับสถานะพร้อมสีต่างกัน

### FIX-05 · [MINOR] preferredVendor ตั้งจาก UI ไม่ได้

policy มีฟิลด์ `preferredVendor` (ส่งเข้า `vendor_suggests` ของ PR) แต่ฟอร์มไม่มีช่องให้เลือก — hardcode ใน seed เท่านั้น · แก้: เพิ่ม field เลือกผู้ขายหลัก (optional · combobox mock) ในฟอร์มนโยบาย · เกณฑ์: ตั้งค่าแล้วสะท้อนใน payload PR

### FIX-06 · [MINOR] ปุ่ม/ผลลัพธ์ไม่มี `_busy`

grep `_busy` = 0 — "รันรอบตรวจ" / "สร้าง PR" กดรัวได้ (idempotency กันผลซ้ำอยู่แล้ว แต่ UI ควรกัน race) · แก้: `state._busy` pattern เดียวกับไฟล์อื่นใน batch + loading state ปุ่ม (Rule #44)

### FIX-07 · [MINOR·PROD] ข้อความ demo — mark demo-only (กติกา BA)

chip `DEMO` ที่ topbar + `tenantId:'TENANT-DEMO'` ที่แสดงในหน้าประวัติ/envelope + คำว่า "ผู้ใช้งานตัวอย่าง" → ครอบ class **`demo-only`** + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` (ไฟล์มี class `.demo` อยู่แล้ว เปลี่ยนชื่อ/เพิ่มให้ตรงกติกากลาง) · เกณฑ์: inject `.demo-only{display:none}` → ไม่เหลือศัพท์ demo/tenant mock บนจอ + layout ไม่พัง

## 3. สิ่งที่ผ่านและขอคงไว้ (ห้ามแตะตอนแก้)

- สูตรจำนวนแนะนำ + packSize rounding (verify แล้ว) · edge code `NO_POLICY`/`SNAPSHOT_UNAVAILABLE`
- **idempotency key ทุกเส้นทาง** (suggestion / notification / PR draft) + `replay:true` — ต้นแบบให้ feature automation อื่นใน W4
- PR draft-only ห้าม auto-submit เข้า DOA + รวม 1 PR ต่อคลังต่อรอบ + `ref_external`/`source_policy`/`source_snapshot`
- policy version + effectiveDate + `ropPolicyActive` (นโยบายที่มีผล ณ วัน)
- validation `0 ≤ safety ≤ min ≤ max` + ตรวจ master จริง · NTF envelope + policyVersion + asOf
- ATP อ่านสำเร็จรูปจาก F009 (ไม่หัก reserved ซ้ำ)

## 4. ประเด็นเปิด (OQ)

| รหัส | ประเด็น | ผู้เคาะ | กระทบ |
|---|---|---|---|
| OQ-ROP-01 | นิยาม safety stock — เข้าเงื่อนไข trigger (`ROP = safety + ADU×lead`) และ/หรือ target (`max + safety`) หรือเป็นตัวเลขอ้างอิงเฉย ๆ | Strike | 03_LOGIC สูตรหลัก |
| OQ-ROP-02 | CSQ profile — `pr_draft_created` / `threshold_breached` เข้าท่อไหน (OC ปฏิบัติการ? EC?) · การสร้าง PR draft ถือเป็น consequence ของ F085 หรือของ F072 | Strike + Architect | CSQ_BRIEF_F085 |
| OQ-ROP-03 | On-Order นับอะไรบ้าง — rules ระบุ "PO เปิดค้างรับ + PR draft ที่ยังไม่ปิด" แต่ snapshot มาจาก F009 สำเร็จรูป: ใครคำนวณ (F009 หรือ F085) และกันนับซ้ำกับ PR ที่ตัวเองเพิ่งสร้างอย่างไร | Strike + Architect | §Integration · 03_LOGIC |

## 5. ขั้นตอนหลังแก้ (Re-gate Checklist)

- [ ] node --check ผ่าน · audit FAIL=0 · Playwright pageerror=0
- [ ] safety เข้าสูตรตามนิยามที่เคาะ + จอแสดงที่มาตัวเลข
- [ ] anchors ครบ: trigger (scheduler+movement) · contract F072/F009 · csq
- [ ] scaffold feature อื่นถูกลบหมด · ตารางมี 3 ระดับสถานะ
- [ ] demo-only ติดครบ · idempotency เดิมยังทำงาน (รัน recompute ซ้ำ events ไม่เพิ่ม)
- [ ] ส่ง re-gate (รอบสั้น — ไม่มี CRITICAL)
- [ ] ผ่านแล้ว: อัพเดต FEATURE_REGISTRY (F085) + แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q → Phase B
