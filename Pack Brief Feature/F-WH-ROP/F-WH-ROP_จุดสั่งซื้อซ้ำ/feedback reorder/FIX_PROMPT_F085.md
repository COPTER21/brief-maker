# คำสั่งแก้ไข F-WH-ROP.html (F085 Reorder Point — จุดสั่งเติม)

คุณจะแก้ HTML prototype single-file ตามรายการนี้เท่านั้น ห้ามแตะส่วนอื่น
ห้าม regenerate ทั้งไฟล์ — แก้เฉพาะจุด (surgical edit)

## บริบท
- ไฟล์: F-WH-ROP.html · html-generator-v9 · arch master (automation) · F085 W4 FULL
- ส่วนที่ผ่านการตรวจแล้ว **ห้ามเปลี่ยนพฤติกรรม**:
  - สูตรจำนวนแนะนำ + packSize rounding · edge code NO_POLICY / SNAPSHOT_UNAVAILABLE
  - **idempotency key ทุกเส้นทาง** (suggestion.evaluated / notification.emitted / pr.draft.created) + replay:true
  - PR **draft เท่านั้น ห้าม auto-submit** + รวม 1 PR ต่อคลังต่อรอบ + ref_external/source_policy/source_snapshot
  - policy version + effectiveDate + ropPolicyActive · validation 0 ≤ safety ≤ min ≤ max + ตรวจ master จริง
  - NTF envelope (eventType/tenantId/policyRef/policyVersion/asOf/idempotencyKey) · ATP อ่านจาก F009 ห้ามหัก reserved ซ้ำ

## รายการแก้ (ทำตามลำดับ)

### 1. FIX-01 ให้ safety stock มีผลจริง — HIGH
ตำแหน่ง: `ropEvaluatePair` (+ จุดแสดงผลในแท็บคำแนะนำ / drawer)
สิ่งที่ผิด: safety ตั้งได้/validate ได้ แต่ไม่อยู่ในเงื่อนไข trigger และไม่อยู่ในสูตร qty เลย — c[1] และ d ระบุเป็น input หลัก
แก้เป็น (ค่าเริ่มต้นถ้ายังไม่ได้เคาะ OQ-ROP-01 — ใส่ comment อ้าง OQ ไว้):
- จุดสั่งเติม `rop = Math.max(policy.min, policy.safety + adu*policy.leadTime)`
- trigger เมื่อ `atp < rop` (แทน `atp < policy.min`)
- target `raw = Math.max(0, (policy.max + policy.safety) - atp - onOrder)` แล้วปัดขึ้นตาม pack เหมือนเดิม
- แสดงที่มาบนจอทุกแถวที่ trigger: "ATP 8 < จุดสั่งเติม 19 (safety 5 + ADU 2 × lead 7)" — ให้ FRD คัดลอกได้ตรง
ตรวจรับ: เปลี่ยน safety แล้ว trigger/qty เปลี่ยนตาม · จอแสดงที่มาของตัวเลข · pack rounding เดิมยังทำงาน

### 2. FIX-02 anchor ของการตรวจอัตโนมัติ (c[2]) — HIGH
ตำแหน่ง: `ropRecompute` + ปุ่ม "รันรอบตรวจ"
สิ่งที่ผิด: มีแต่ปุ่มกดเอง + ข้อความใน CFG.rules — ไม่มี hook ให้ dev ผูก scheduler/movement
แก้เป็น: comment `<!-- TRIGGER: (1) scheduler รายวัน 06:00 ต่อ tenant → ropRecompute ทั้ง catalog (2) subscribe movement events ที่ทำให้ ATP เปลี่ยน (GRN / Issue / Transfer / Adjust / Reserve) → evaluate เฉพาะคู่ item×warehouse ที่กระทบ · ปุ่มบนจอ = manual run สำหรับทดสอบเท่านั้น -->` + ข้างปุ่มแสดง "ตรวจอัตโนมัติล่าสุด: 2026-09-14 06:00 (mock)"
ตรวจรับ: anchor ครบ 2 ทาง · จอสื่อว่าปุ่มคือ manual run

### 3. FIX-03 contract + CSQ anchors — HIGH
ตำแหน่ง: `ropPreparePR` · `ropNcCandidate`
แก้เป็น:
- `<!-- CONTRACT: F085 → F072 Purchase Requisition (flow — ต่ำกว่าจุดสั่งเติม สร้าง PR draft ตาม payload/ack นี้) · ATP/On-Order/ADU อ่านจาก F009 (data) -->`
- `<!-- CSQ: rop.threshold_breached / rop.pr_draft_created → ท่อตาม CSQ_BRIEF_F085 (รอเคาะ OQ-ROP-02) · ห้ามประกาศ OC/DC ซ้ำ -->`
ตรวจรับ: anchor contract 2 เส้น + csq ≥1 จุด

### 4. FIX-04 ลบ scaffold feature อื่น + เพิ่มชั้น "ใกล้จุด" — HIGH
ตำแหน่ง: `domainView` · `domainAction` · generic `stats`/`validate`/`saveRecord` ที่ถูก override · ตาราง suggestions
สิ่งที่ผิด: (a) มีสาขา F-WH-LOT / F-WH-QHOLD / F-WH-CYCLE / F-ACC-LC ค้าง (ปุ่ม "ขอปล่อยกัก / บันทึกผลนับ / คำนวณจัดสรร" ของ feature อื่น) + ฟังก์ชัน scaffold ที่ไม่ถูกเรียก (b) c[4] "รายงานสินค้าใกล้หมด" — มีแค่ 2 สถานะ และ "ต่ำกว่าจุด" ใช้ pill เขียวเหมือนสถานะปกติ
แก้เป็น:
- ลบโค้ดที่ไม่ใช่ ROP ออกให้หมด (grep ต้องไม่เหลือ F-WH-QHOLD / F-WH-CYCLE / F-WH-LOT / F-ACC-LC)
- เพิ่มสถานะ "ใกล้จุด": trigger=false แต่ `atp <= rop * 1.2` (หรือคาดถึงจุดภายใน lead time) → pill สีส้ม · "ต่ำกว่าจุด" = แดง · ปกติ = เขียว/เทา
- เพิ่ม KPI card "ใกล้จุด" ในแถว stats
ตรวจรับ: grep scaffold = 0 · ตารางมี 3 ระดับสถานะ สีต่างกัน · KPI ครบ

### 5. MINOR รวบ (ทำท้ายสุด)
- FIX-05: เพิ่มช่อง "ผู้ขายหลัก (ไม่บังคับ)" ในฟอร์มนโยบาย → เก็บลง `preferredVendor` → สะท้อนใน `vendor_suggests` ของ payload PR
- FIX-06: `state._busy` (500ms) + loading state ปุ่ม "รันรอบตรวจ" / "สร้าง PR" / "ส่งแจ้งเตือน" (Rule #44)
- FIX-07 (กติกา demo-only): chip `DEMO` ที่ topbar + "ผู้ใช้งานตัวอย่าง" + ค่า `TENANT-DEMO` ที่โชว์บนจอ → ครอบ class `demo-only` + comment `<!-- DEMO-ONLY: ห้าม render ใน production build -->` · ทดสอบ `.demo-only{display:none}` → ไม่เหลือศัพท์ demo/tenant mock + layout ไม่พัง

## ข้อห้าม
- ห้ามเพิ่ม dependency/CDN · ห้ามแตะ BASE-KIT · ห้ามเปลี่ยน CI token
- ห้ามแตะ: idempotency key logic ทุกเส้น, PR draft-only + grouping ต่อคลัง, policy version/effectiveDate, ropValidate, NTF envelope, การอ่าน ATP จาก F009
- ห้ามทำให้ PR auto-submit เข้า DOA ไม่ว่ากรณีใด

## หลังแก้เสร็จ ให้รันเองก่อนส่ง
1. node --check
2. audit.sh → FAIL=0
3. Playwright: pageerror=0 + เคส:
   - เปลี่ยน safety → trigger/qty เปลี่ยนตามนิยาม · จอแสดงที่มาตัวเลข
   - รัน recompute ซ้ำ 2 รอบ → events ไม่เพิ่ม (idempotency เดิมยังทำงาน)
   - PR ack ยัง `submitted:false` · รวม 1 PR ต่อคลัง
   - grep: F-WH-QHOLD/F-WH-CYCLE/F-WH-LOT/F-ACC-LC = 0 · CONTRACT F072/F009 ≥1 · CSQ ≥1 · TRIGGER anchor ≥1
   - ตารางมี 3 ระดับสถานะ + KPI ใกล้จุด
   - inject `.demo-only{display:none}` → สะอาด + layout ปกติ
แนบผลรันกลับมาพร้อมไฟล์ แล้วส่ง re-gate (รอบสั้น)
