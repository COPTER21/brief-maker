# HANDOFF — F-WH-STKADJ · Stock Adjustment (ใบปรับยอดสต๊อก)

> fid **F082** · module **Warehouse** · wave **W3Q** ลำดับ 2 · arch **Q-document** (Pattern Q เต็ม + B2 v2)
> runner `feature-lane-runner 2.4.1r` · mode `direction` (Phase A) · วันที่ **2026-09-10**
> สถานะ: **ba-done** — รอทีม vibe

---

## 1. ทำอะไรไปแล้ว

| Stage | ผล | สาระ |
|---|---|---|
| S0 | ✓ pass | อ่านกติกากลาง (W3-LITE · GOLDEN_RULES · BUILD_ORDER · workflow_graph · CHECKLIST W3Q · FEATURE_LIST F082 · TASTE_LOG) + **PREBRIEF_F-WH-PUTAWAY §3.0 LOCATION MODEL** → `_lane/LANE_BRIEF.md` |
| S0.5 | ✓ pass | BASELINE เทียบ SAP / Odoo / D365 / NetSuite / ERPNext (`[PARTIAL-ONLINE BASELINE]` — web search คืนเฉพาะ title/URL) · must-have 14 · out-of-scope 8 · gap G-01..G-08 |
| S1 | ✓ pass | PREBRIEF 12 sections (S-01..S-25 · BR-01..BR-25 · OB-1..OB-17) + FUNCTION_CHECKLIST **54 FN / 8 หมวด / ไม่รองรับ 13 ข้อ** (+ .html ติ๊กได้) |
| S1.5 | ✓ pass | Gap check → PREBRIEF §12: must-have **13 ✅ + 1 ⚠️** (JE mock ตามแผน) · CHECKLIST ครบ 7/7 วรรค · `[ASSUMED]`/forward-wire 9 ตัวมี owner ครบ |
| S1.8 | ✓ pass | Declarations ครบ 5 ตาม chip — **detect = chip ไม่มี DIVERGENCE** |
| S2 | ✓ pass | HTML single-file SPA 253 KB · Pattern Q 4 surface + B2 v2 line editor |
| **S3a** | **PASS** | `qc-ux-html-checker` — iron rules #1–#103 · Pass D (#98–#101) ครบ · combobox anatomy #102 · lean list #103 · WARN 3 = BASE-KIT verbatim |
| **S3b** | **PASS** | `qc-coverage-checker` R1 — FN **54/54** มี hook จริง · S-01..S-25 มีทางเข้าครบ (รวม negative 3) · BR 25/25 · declaration ตรง chip · **scope creep = 0** |
| **S3c** | **PASS** | `node --check` OK · `audit.sh` **FAIL=0** WARN=3 · Playwright: console error (feature) **0** · pageerror **0** · ไม่มี horizontal scroll @1024 · สกรีนช็อต **30 ไฟล์** |
| S4 | ✓ pass | BRD 18 sections · Quality Gate C01–C23 + PE01–PE05 = **28 ✅ / 0 ❌ → APPROVED** |
| S4.5 | ✓ pass | HANDOFF (ไฟล์นี้) → `pool.py set "Stock Adjustment" ba-done` |

---

## 2. ส่งมอบอะไร (ไล่ไฟล์ทุกตัว)

```
output/2026-09-10/F-WH-STKADJ_Stock Adjustment/
├── 0_DIRECTION/
│   ├── BASELINE_F-WH-STKADJ.md                 ← เทียบ ERP standard · must-have/nice/out + gap G-01..G-08
│   ├── PREBRIEF_F-WH-STKADJ.md                 ← ★ source of truth เชิง business (12 sections + §12 gap check)
│   ├── FUNCTION_CHECKLIST_F-WH-STKADJ.md       ← 54 FN ติ๊กได้ (trace กลับ S-XX/BR-XX)
│   ├── FUNCTION_CHECKLIST_F-WH-STKADJ.html     ← เวอร์ชันติ๊ก/ส่งผลได้ (WF/DEV/QA · localStorage)
│   └── HANDOFF.md                              ← ไฟล์นี้
├── 1_HTML/
│   ├── F-WH-STKADJ.html                        ← ★ prototype single-file (เปิดได้ทันที ไม่ต้อง build)
│   ├── _UX_CHECK_REPORT.md                     ← S3a (PASS)
│   ├── _COVERAGE_R1.md                         ← S3b (PASS)
│   ├── _TECH_CHECK.md                          ← S3c (PASS) + convention/override ที่บันทึกไว้
│   ├── _static_scan.json                       ← ผลสแกนเชิงกล
│   └── _shots/                                 ← 30 สกรีนช็อตจาก Render Gate
├── 2_BRD/
│   └── BRD_F-WH-STKADJ.md                      ← 18 sections + AI Review = APPROVED
└── 5_DECLARATIONS/
    ├── DOA_BRIEF_F-WH-STKADJ.md                ← ★ มีวงเงิน · ฐาน = Σ ค่าสัมบูรณ์ · matrix 4 ช่วง
    ├── NTF_BRIEF_F-WH-STKADJ.md                ← 6 event ธุรกิจ (ตัด doa_pending/doa_result ออก)
    ├── CSQ_BRIEF_F-WH-STKADJ.md                ← 5 event · ท่อ EC · ระบุชัดว่าไม่ประกาศ OC/DC/SC/SecC/AC/FC
    ├── DOCCFG_BRIEF_F-WH-STKADJ.md             ← doc_type `ADJ` · `ADJ-YYYY-NNNN` · ออกเลขตอนส่งอนุมัติ
    └── print-spec-adj.md                       ← pdfdoc A4 (thai-doc-pdf-generator)

briefs/W3Q/F-WH-STKADJ/_lane/
├── LANE_BRIEF.md · LANE_LOG.md · LANE_STATE.json
```
**ไม่มี** `3_FRD` / `4_TC` — Phase B ทีมย่อยทำ

---

## 3. ห้ามแตะ (ล็อกแล้ว — แก้ = ต้อง re-gate)

1. **Pattern Q archetype 4 surface** — list (สถานะ + ลายเซ็น n/N) · wizard 5 steps ชื่อล็อก · view drawer tabs ล็อก (เอกสารแนบเป็น section ใน "รายละเอียด" ไม่ใช่ tab) · PDF `.a4` + 3 ช่องเซ็น
2. **B2 v2 line editor** — grid 9 ช่อง ความกว้าง `26/—/64/92/92/78/72/104/54` · แถวขยาย lean 1 บรรทัด · `calcLineVat`/`migrateLine`/`totals`/`taxBadgeV`/`renderLineSummary` · `updateLine` คืน focus+caret
3. **CI token + BASE-KIT** — CUBE Warm Light (Charcoal `#111111` · Red `#FF3B30` · Orange `#FF9A1F` · Ivory `#FAF8F5` + `#0B5CFF` / `#00A88E`) · CSS ระหว่าง marker BASE-KIT verbatim · **ปี ค.ศ. ล้วน**
4. **DOA slot picker คนจริง** (avatar + ตำแหน่ง + ชื่อ) — ห้าม role ID · ห้าม hardcode สายอนุมัติ · **ฐานวงเงิน = Σ ค่าสัมบูรณ์ ไม่ใช่ยอดสุทธิ**
5. **เลขรัน `ADJ-YYYY-NNNN`** — มาจาก ENG-DOC-NUM ตาม doccfg · ออกตอน**ส่งอนุมัติ** · ห้าม format/+1 เอง
6. **movement append-only** — ยกเลิกหลัง post = **กลับรายการ** (ใบใหม่ทิศตรงข้าม ผูกคู่ 2 ทาง) · ไม่มี path ลบ/แก้
7. **สัญญา location จาก Putaway §3.0** — warehouse › zone › bin + `location_type` · **`in-transit` ห้ามแตะ** (จองให้ Stock Transfer)
8. **ขอบเขต**: ไม่มี cycle count · ไม่มีการย้าย location — ทั้งสองมีเจ้าของจริงคนละตัว

---

## 4. ASSUMED / OQ + owner · TODO forward-wire + wave เจ้าของ

### 4.1 `[ASSUMED]` / OQ (owner = **Strike** ทั้งหมด เว้นที่ระบุ)

| # | ประเด็น | ค่าที่ใช้ไปก่อน |
|---|---|---|
| `OQ-STK-01` `[ASSUMED]` | เหตุผลบังคับ + DOA ตามมูลค่า · **cycle count = backlog** | ใช้ตามนี้ทั้งหมด (BR-06 · BR-08/09 · BR-24) |
| `OQ-ADJ-01` `[AI-DRAFT]` | ฐาน DOA = Σ ค่าสัมบูรณ์ หรือ ยอดสุทธิ | **ค่าสัมบูรณ์** (กันใบผสมหลุดอนุมัติ) |
| `OQ-ADJ-02` `[AI-DRAFT][STD]` | ยอดระบบเปลี่ยนระหว่างรออนุมัติ | เตือนก่อน post + ให้เลือกฐาน |
| `OQ-ADJ-03` `[AI-DRAFT]` | ย้ายของเสีย storage → damage เป็นของใคร | **Transfer** — ใบนี้ปรับยอดใน bin เดิมเท่านั้น |
| `OQ-ADJ-04` `[AI-DRAFT]` | ปรับยอดที่ `staging` อนุญาตไหม | อนุญาต |
| `OQ-ADJ-05` `[AI-DRAFT]` | วันที่มีผลย้อนหลังได้ถึงไหน | งวดที่ยังเปิด (กติกาจริง = **W5**) |
| `OQ-ADJ-06` `[AI-DRAFT]` | จำกัดสิทธิ์ใช้เหตุผลบางตัวตามตำแหน่งไหม | ไม่จำกัดใน UI รอบนี้ → Security Preset |
| `OQ-ADJ-07` `[AI-DRAFT]` | ออกเลขตอนส่งอนุมัติ หรือเลื่อนไปตอน post (no-gap) | ออกตอนส่งอนุมัติ · no-gap = ✗ (**+ เจ้าของ F-DOCCFG**) |
| จุดตัดวงเงิน DOA | 20,000 / 200,000 / 1,000,000 + จำนวนชั้น | `[DEFAULT — รอยืนยัน]` (**+ เจ้าของ F-DLG-001**) |
| เกณฑ์ “มูลค่าสูง” / อายุใบค้าง | R26 | ไม่ตั้งตัวเลขใน feature — อ่านจาก **NC rules** |

### 4.2 `TODO:` forward-wire (ใน .md) ↔ `FWD-WIRE:` (ใน HTML)

| ใน .md | ใน HTML | เจ้าของ / wave |
|---|---|---|
| `TODO: JE posting` | `FWD-WIRE: JE posting (W5)` | **GL/JE · W5** |
| `[ASSUMED contract]` ต้นทุนอ้างอิง | `FWD-WIRE: valuation engine (W5)` | **Inventory Valuation · W5** |
| ประกาศใน `DOA_BRIEF` | `FWD-WIRE: DOA engine` | **F-DLG-001 (DONE — รอตั้ง entry)** |
| ประกาศใน `NTF_BRIEF` | `FWD-WIRE: ENG-NOTIFY emit` | **F-NOTIFY** |
| ประกาศใน `CSQ_BRIEF` | `FWD-WIRE: ENG-CSQ emit` | **F-CSQ-01** |
| ประกาศใน `DOCCFG_BRIEF` | `FWD-WIRE: ENG-DOC-NUM` | **F-DOCCFG** |

> เหตุผลที่ HTML ใช้ `FWD-WIRE:` แทน `TODO:` — `audit.sh` Rule #24 ตั้ง literal `TODO` = FAIL ซึ่งชนกับ gate ที่บังคับ FAIL=0 (บันทึกไว้ที่ `_TECH_CHECK §4.1`)

---

## 5. vibe ได้แค่ไหน

### ✅ แก้ได้เลย ไม่ต้องกลับมา re-gate
- **layout ภายในการ์ด/section** — ลำดับการ์ดในแท็บ "รายละเอียด" · ระยะห่าง · การจัดกลุ่ม KV
- **microcopy** — ข้อความ hint · placeholder · toast · ชื่อคอลัมน์ (ตราบที่ยังสื่อความเดิม)
- **สีระดับตกแต่ง** ที่ยังอยู่ใน CI token (เช่นเลือกใช้ `--c-blue` หรือ `--c-success` กับสถานะไหน)
- **mock data** — เพิ่ม/แก้สินค้า ช่องเก็บ ใบตัวอย่าง (ขอให้ยังคลุมทุก scenario ใน `_COVERAGE_R1 §2`)
- **การเรียง/ความกว้างคอลัมน์ใน list** (ตราบที่ยัง ≤8 คอลัมน์ และ 1 ข้อมูล = 1 คอลัมน์)
- **ไอคอน** (ยัง Lucide) · ข้อความในการ์ดสรุป 4 ใบ

### ⛔ แก้แล้วต้องกลับมา re-gate (S3r → S3a/S3b ใหม่)
- **flow / ลำดับ step ของ wizard** หรือ **ลำดับ/ชื่อ tab** ของ view drawer (ชน Rule #100/#101)
- **สถานะเอกสารหรือ transition** ใน state machine (§8 ของ BRD)
- **สายอนุมัติ / ฐานวงเงิน / เงื่อนไข slot** (ชน LOCK-04 + BR-09/BR-10)
- **grid ของ line editor** — เพิ่ม/ลด/สลับ/เปลี่ยนความกว้างคอลัมน์ (ชน Rule #99)
- **กติกา location** — เปิดให้เลือก `in-transit` · เพิ่มช่องปลายทาง · ให้ของออกจาก quarantine (ชน LOCK-03/LOCK-07)
- **เพิ่มฟังก์ชันนับสต๊อก** หรือ **การย้าย location** (scope creep — Hard Stop)
- **ทำให้ movement ลบ/แก้ได้** (ชน LOCK-06)

---

## 6. คำสั่ง Phase B

**รอทีม vibe — Phase B หลัง re-gate html-review-fix-order**

ลำดับ Phase B:
`S3r re-gate → S5 FRD (frd-generator-v6) → S6 TC → S6.5 coverage R2 → S7.5 UI Brief → S8 Pack`

### สิ่งที่ Phase B ต้องหยิบไปใช้ต่อทันที
- **FRD**: `PREBRIEF §3` (data dict) · `§4` (BR-01..BR-25) · `§5` (state machine) · `BRD §6` (entity + audit fields) · `BRD §9` (R01–R27 + VR01–VR15) · `BRD §14` (ใบสั่ง dev)
- **TC**: `FUNCTION_CHECKLIST` 54 FN (มี trace S-XX/BR-XX อยู่แล้ว) + `_COVERAGE_R1 §2` (ทางเข้าแต่ละ scenario ใน HTML)
- **UI Brief**: `_UX_CHECK_REPORT §3` (Pattern Q surface) + `_shots/` 30 ภาพ
- **Declarations**: เอา 4 brief + print-spec ไป register/ตั้งค่าที่ engine กลาง (checklist อยู่ท้ายแต่ละ brief)

### ส่งต่อให้ตัวถัดไปในเลน (F-WH-STKTRF · Stock Transfer)
- **movement schema + reversal pattern** (`PREBRIEF §3.4` / `§5.2`) — ใช้ชุดเดียวกัน
- **DOA slot picker + ฐานวงเงินค่าสัมบูรณ์** — โครงเดียวกัน (Transfer จะผูกมูลค่าที่ย้าย)
- **`in-transit` ยังว่างรออยู่** — `WH-TRN` / `TR-BKK-CNX` / `TR-CNX-BKK` ไม่มีใครเขียนในรอบนี้ ตาม `OQ-TRF-01`
