# DevPack — F-INV-001 สต็อกตามตำแหน่ง (Stock by Location)

**Module:** Inventory · **PREBRIEF ID:** F-INV (ไม่มี BRD แยก — PREBRIEF ทำหน้าที่แทน ตามแบบเดียวกับ
F-CUST/F-CGRP/F-COA ในคลื่นก่อนหน้า)
**Pipeline:** WF-01 HTML-first lane (`feature-pack-workflow.md`) — **Reverse Mode** (HTML = source of
truth, ไม่ผ่าน html-generator-v8 ในเลนนี้) · **Assembled:** 2026-08-10/11

ชุดนี้รวบรวม artifact ทุกชิ้นที่ผ่านทุก gate ของ WF-01 แล้ว สำหรับส่งต่อให้ dev/QA/OPS ใช้เป็นชุดเดียว

## บริบท

feature นี้เป็น **Reverse Mode**: `f-inv.html` เป็น ENC pack (base) ที่ผ่านมติ vibe 2026-08-09 มาแล้ว
(superset — adjust modal + log + break/pack) จึงไม่ได้เกิดจาก `html-generator-v8` ในเลนนี้ — งานคือ
รับไฟล์มาเป็น `StockByLocation.html`, ตรวจอิสระผ่าน UX gate → coverage gate (2 รอบ) → FRD Pack →
HTML UI Brief → AI test cases → QA-friendly HTML → DevPack นี้

**PREBRIEF ยังไม่ผ่าน human sign-off** — มี §6 Open Questions 5 ข้อต้นทาง (OQ-INV-01..05) บวกอีก 1 ข้อ
ที่ QC เจอใหม่ระหว่างเลนนี้ (OQ-INV-06 — ดูหัวข้อถัดไป) รวม 6 ข้อ รอเจ้าภาพจริง (Strike / พี่เบิร์ด / ทีมขาย)
เคาะ

## สิ่งที่ QC เจอ — สำคัญพอจะอ่านก่อนใช้

**UX gate พบ 3 BLOCK จริงที่ไฟล์ ENC base เดิมไม่ได้ครอบคลุมตาม iron rules ปัจจุบันของ html-generator-v8:**
1. **Rule #11 (Drawer Width, BREAKING)** — `.drawer{width:540px}` (legacy) แทนที่จะเป็น 920px มาตรฐาน v2
   → แก้แล้ว
2. **Rule #49 (mandatory scrollbar CSS)** — ไม่มี scrollbar CSS เลยทั้งไฟล์ → เพิ่ม thin/rounded scrollbar
   block + `scrollbar-gutter:stable` (แยก dark-surface variant ให้เฉพาะ `.sidebar` ไม่ให้กระทบ `.drawer`
   สีขาว)
3. **Rule #2 (Font Stack)** — โหลด Google Fonts `Inter` ที่ไม่ได้ใช้จริงเลย + font-family สลับลำดับ/ไม่ครบ
   ในหลาย selector → ลบ Inter link ออก + แก้เป็น `'Satoshi','Noto Sans Thai',system-ui,sans-serif`
   มาตรฐานทุกจุด

**แก้ surgical ครบทั้ง 3 แล้ว ยืนยันซ้ำด้วย static_scan.py + self_audit.py อิสระ (BLOCK=0)** — เหลือ WARN
ที่ตั้งใจไม่แก้ (นอกขอบเขต surgical): extended badge palette (20 hex นอก ci-tokens whitelist — จำเป็นทาง
ธุรกิจสำหรับ 10 ประเภทตำแหน่ง + 4 สถานะสต็อกย่อย), typography/spacing drift (122 spacing values/18
font sizes — pre-existing pattern กว้าง ต้อง normalize แยกรอบ), Manual Adjustment เป็น modal 1440px
ไม่ใช่ drawer (Rule #14 tension — แต่ระบุไว้แล้วว่าเป็นมติ 2026-08-09 ตาม PREBRIEF OB-8 → ล็อกเป็น
LD-01 ใน FRD)

**RENDER: UNAVAILABLE ตอน UX gate** (ไม่มี browser ในสภาพแวดล้อมตอนนั้น) — แต่ **ภายหลังตอนสร้าง
QA-friendly HTML พบว่า playwright + chromium ใช้งานได้จริง** จึงมี screenshot จริง 19 ภาพผ่านขั้นตอนนั้น
แทน (ดู `05_QA/`) — บันทึกไว้ตรง ๆ ว่า evidence ทางภาพมาจากคนละขั้นตอนกับที่ระบุใน `_UX_CHECK_REPORT.md`

**Coverage gate รอบ 1 พบ scope creep จริง (G-01 / OQ-INV-06):** ฟีเจอร์ costing/valuation เต็มรูปแบบ
(`canValuation()`/`canValExport()` L801-803, ปุ่ม "ดูมูลค่า/ซ่อนมูลค่า" L2047-2050, `.val-box` แสดง
on_hand × cost L2135-2144, toggle "รวมมูลค่า" ตอน export L1360-1374) หลงเหลือมาจาก ENC base template
โดยไม่มีการอ้างถึงใน PREBRIEF เลย และขัดกับบรรทัด "ไม่ทำ: costing engine (VD-PDM-07)" ใน §1 Scope
ตรง ๆ — **ไม่ได้ลบทิ้งเงียบ ๆ** เพราะการตัดฟีเจอร์ที่ทำงานได้จริงเป็นมติทางธุรกิจ ไม่ใช่ของ QC gate
ตัดสินเอง → carry เป็น OQ-INV-06 + ล็อกเป็น non-resolution ที่ `07_LOCKED_DECISIONS.md` LD-02

## Pipeline status

| ด่าน | Skill | ผล |
|---|---|---|
| HTML (Reverse Mode) | — (คัดลอกจาก `f-inv.html` ตรง ๆ ไม่ผ่าน html-generator-v8) | `StockByLocation.html` = ENC base superset (มติ 2026-08-09) |
| UX Gate (อิสระ) | `qc-ux-html-checker` | 🔴 เริ่ม 3 BLOCK + ~10 WARN category → แก้ surgical ครบ (#11 drawer 540→920px, #49 scrollbar CSS เพิ่มใหม่, #2 font stack) → 🟢 **PASS with warnings** (BLOCK=0) ยืนยันด้วย static_scan.py + self_audit.py อิสระ · RENDER unavailable ตอนนั้น |
| Coverage Gate (2 รอบ) | `qc-coverage-checker` | รอบ 1 (HTML vs PREBRIEF): 🟡 **WARN** — OB 12/12 ✓ · S 14/14 ✓ · FN 25/26 ✓ (FN-40 = build gate, out of scope ตัวเช็คนี้) · **scope creep 1 จุด (G-01 costing/valuation)** · รอบ 2 (FRD vs PREBRIEF, appended ไฟล์เดียวกัน): 🟡 **WARN** (เหตุผลเดิม G-01/OQ-INV-06 ยังเปิดอยู่ — ไม่มี block rule หายไปจาก FRD) · TC (dedicated) มาร์ก PENDING เพราะยังไม่มี testcases-f-inv.md ตอนนั้น |
| FRD | `frd-generator-v6` (Sync Read v8) | **FULL variant** (9 ไฟล์ + INDEX — ตัดสินจาก balance status ≥4 สถานะ + 3 CUBIC-Engine candidate จริง ไม่ default เอง; ไม่นับ approval∧money เพราะไม่มี DOA จริง) · R8 trace ยึดฟังก์ชันจริงจากไฟล์ (เช่น `adjLineError()` L2598, `submitBPOrder()` L2327) · OQ-INV-06 ถูกล็อกเป็น LD-02 non-resolution |
| Coverage round 2 | (ในแถวเดียวกับ Coverage Gate ด้านบน) | ดูรายละเอียด `01_HTML/_COVERAGE_REPORT.md` ส่วน Round 2 |
| HTML UI Brief | (handoff, ไม่มี skill แยก) | สรุป UI สำหรับ FE dev — routing จริง (`getRoute()` L1261 ใช้ hash routing จริง ต่างจาก F-CUST ที่ hash ตายเปล่า), component map, RBAC, known gaps |
| Test cases (AI) | `ai-testcase-md-generator` | **94 เคส · 12 กลุ่ม** (GATE, LIST, PD, LOC, ADJ, STK, RBAC, BP, LOG, OV, XT, OOS) · Coverage Audit: AC 17/17 · BR 12/12 · permission cell 12/12 · XT 2/2 · Manifest cross-check ✅ |
| Test cases (Tester) | `qa-friendly-html-generator` (Pipeline Mode) | 94/94 เคส · 280/280 step แปล 1:1 · 19 region screenshot จริง (playwright ใช้งานได้จริงตอนนี้) · เคส `sys:true` 2 (`TC-ADJ-24` ต้องเปิด devtools, `TC-RBAC-07` ต้อง simulate backend) |

## ช่องว่างที่รู้แล้ว (ตั้งใจไม่แก้ในเลนนี้ — ทุกจุด trace ไปที่ FRD OQ)

1. **G-01 / OQ-INV-06 — ฟีเจอร์ costing/valuation หลงเหลือจาก ENC base** ขัดกับ "ไม่ทำ: costing engine"
   ใน PREBRIEF §1 ตรง ๆ (`canValuation()` L801, `.val-box` L2135-2144) — ยังทำงานได้จริงในโปรโตไทป์
   แต่ไม่มี spec รองรับ → รอทีมตัดสินว่าจะรับเข้า scope อย่างเป็นทางการหรือถอดออก (`07_LOCKED_DECISIONS.md`
   LD-02, `05_QA/testcases-f-inv.md TC-OOS-01` เช็คแค่การมี/ไม่มี ไม่ assert pass/fail)
2. **OQ-INV-01..05 (ต้นทางจาก PREBRIEF §6)** ยังไม่เคาะ — DOA สำหรับ manual adjustment มูลค่าสูง,
   `min_stock` per-item vs per-warehouse, สิทธิ์เปลี่ยนหน่วยตำแหน่ง, เจ้าภาพ reconcile สต็อกติดลบ,
   low-stock ต่อ action อะไร — ดู `00_OVERVIEW.md §0.8` สำหรับสถานะล่าสุด
3. **AC-08 negative-stock ใน list-aggregate ไม่ reproduce ได้กับ seed data ปัจจุบัน** — RM-2010
   aggregate ต่อคลังยังเป็นบวกแม้ balance ย่อย S011 ติดลบ พบระหว่างสร้าง test cases (`TC-STK-05`
   บันทึกไว้เป็น discrepancy ให้ QA ไปยืนยันกับ build จริง ไม่ใช่ข้อสรุปสำเร็จรูป)
4. **1440px Manual Adjustment modal แทน drawer** — เบี่ยงจาก Rule #14 แต่เป็นมติ 2026-08-09 ตาม
   PREBRIEF OB-8 → ล็อกเป็น LD-01
5. **Extended badge palette (20 hex นอก ci-tokens whitelist)** และ **typography/spacing drift**
   (122 spacing values, 18 font sizes) — WARN ที่ตั้งใจปล่อยไว้ (ดู `01_HTML/_UX_CHECK_REPORT.md`)
   ไม่ใช่ของที่ QC gate ควรลดทอนความชัดเจนทางธุรกิจเพื่อให้ตรง token limit

## ยังไม่ได้ทำในเลนนี้

- **BA/เจ้าภาพ sign-off:** PREBRIEF §6 มี Open Questions รวม 6 ข้อ (OQ-INV-01..05 ต้นทาง + OQ-INV-06
  ใหม่จาก QC) รอ Strike/พี่เบิร์ด/ทีมขาย เคาะ (ดู `03_FRD/00_OVERVIEW.md §0.8`)
- **ส่งขึ้น OPS** — ยังไม่ทำ ณ จุดนี้ (ต้อง confirm กับผู้ใช้ก่อนตามนโยบาย risky-action)
- **FRD/ENC pack (Navy) เดิม stale ตาม FUNCTION_CHECKLIST** — ระบุไว้แล้วว่า regen ค้างจนกว่า
  OQ-INV-01..06 จะเคาะ (FRD Pack ใหม่ใน `03_FRD/` ของ DevPack นี้แทนที่ Navy pack เดิม แต่ยังพก
  OQ ไม่เคาะเหมือนกัน)
- **Permission gate ของจริง:** prototype ใช้ mock role switcher เท่านั้น ไม่ใช่ auth จริง (ผูก Policy
  Center ตาม PREBRIEF OB-12) — ดู `04_UI_BRIEF/HTML_UI_BRIEF_F-INV-001.md §5` สำหรับ role matrix
  ที่ dev ต้อง wire จริง
- **ไม่ได้ zip DevPack** — ตามข้อกำหนดเลนนี้ ปล่อยเป็นโฟลเดอร์ไม่บีบอัด

## โครงสร้างโฟลเดอร์

```
DevPack_F-INV-001/
├── README.md                                          ← ไฟล์นี้
├── 01_HTML/
│   ├── StockByLocation.html                           ← prototype ที่ผ่าน UX gate — ground truth (Reverse Mode)
│   ├── _UX_CHECK_REPORT.md                            ← PASS with warnings (BLOCK=0), RENDER unavailable ตอนนั้น
│   └── _COVERAGE_REPORT.md                            ← รอบ 1 (HTML vs PREBRIEF) + รอบ 2 (FRD vs PREBRIEF) ในไฟล์เดียว, ทั้งคู่ WARN (G-01/OQ-INV-06)
├── 02_BRD/
│   ├── PREBRIEF_F-INV_Stock-by-Location.md            ← ของเดิม ไม่ได้เขียนใหม่ (AI-drafted, ไม่ approved)
│   └── FUNCTION_CHECKLIST_F-INV_Stock-by-Location.md  ← ของเดิม, ระบุ FRD/ENC (Navy) เดิม stale
├── 03_FRD/                                            ← FRD_F-INV-001 Pack (FULL, 9 ไฟล์: 00-07 + INDEX)
├── 04_UI_BRIEF/
│   └── HTML_UI_BRIEF_F-INV-001.md                     ← สรุป UI สำหรับ FE dev (routing/patterns/RBAC/known gaps)
└── 05_QA/
    ├── testcases-f-inv.md                             ← สำหรับ AI browser-use agent ทดสอบ (94 เคส)
    └── testcase-f-inv.html                            ← สำหรับผู้ทดสอบที่เป็นคน (เปิดในเบราว์เซอร์ได้เลย, offline, 3.2MB)
```

## ใช้งานยังไง

- **Dev เริ่มงาน:** อ่าน `04_UI_BRIEF/` ก่อน (ย่อ) → ตามด้วย `03_FRD/` (สัญญาเต็ม UI/API/Logic/DB/Rules)
  → เปิด `01_HTML/StockByLocation.html` เทียบจอจริงไปด้วย — **อ่านหัวข้อ "ช่องว่างที่รู้แล้ว" ด้านบนก่อน**
  โดยเฉพาะ G-01 (costing/valuation) ที่ยังทำงานได้จริงในจอแต่ไม่มี spec รองรับ อย่าเผลอ build ต่อจากมัน
  ก่อนเช็คกับทีม
- **QA ทดสอบ:** เปิด `05_QA/testcase-f-inv.html` ในเบราว์เซอร์ ทำตามทีละเคส — เคส `TC-ADJ-24` และ
  `TC-RBAC-07` เป็น `sys:true` (ต้องใช้ devtools/simulate backend) ไม่ต้องพยายามทำเป็นคนธรรมดา
- **AI agent ทดสอบ:** ป้อน `05_QA/testcases-f-inv.md` ให้ agent อ่านแล้วรันเองตาม schema ท้ายไฟล์
- **Rebuild `testcase-f-inv.html` ใหม่:** ต้นน้ำ (`cases.json`/`shot-spec.json`/`shots_b64.json`) ไม่ได้
  เก็บไว้ในโฟลเดอร์นี้หลัง build เสร็จ — ถ้าต้อง rebuild จากศูนย์ให้รัน `qa-friendly-html-generator` ใหม่
  ทั้งกระบวนการจาก `testcases-f-inv.md`
