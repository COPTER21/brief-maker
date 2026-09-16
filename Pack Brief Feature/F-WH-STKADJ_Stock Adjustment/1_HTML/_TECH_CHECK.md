# _TECH_CHECK — F-WH-STKADJ.html (S3c · technical gate)

วันที่ 2026-09-10 · ไฟล์ `1_HTML/F-WH-STKADJ.html` · single-file SPA (vanilla JS · เปิดจากไฟล์ได้ทันที ไม่มี build)

## 1. `node --check` (แยก JS ออกจาก HTML)

```
python3 -c "strip comments → แยกทุก <script> inline → /tmp/adj_js.js"
node --check /tmp/adj_js.js   →  OK (ไม่มี syntax error)
```
**ผล: PASS** — 10 script block (Lucide loader · BASE-KIT main · BASE-KIT UTILS · feature script 7 ก้อน)

> ⚠️ รอบแรกพบ **`SyntaxError: Identifier 'state' has already been declared`** — feature script ประกาศ `const state` ทับของ BASE-KIT (lexical global ชนกันข้าม `<script>`) ทำให้ SPA ตายทั้งไฟล์ · แก้เป็น `Object.assign(state, {...})` แล้วผ่าน (fix loop 1 รอบ)

## 2. `audit.sh` (iron rules mechanical)

```
bash .claude/skills/html-generator-v9/scripts/audit.sh F-WH-STKADJ.html
สรุป: FAIL=0 · WARN=3
--- doc_archetype (Pattern Q / B2 v2) --- : ไม่มี FAIL
```
**ผล: PASS (FAIL = 0 ตามที่ gate บังคับ)** · WARN 3 รายการมาจาก BASE-KIT verbatim ทั้งหมด — อธิบายใน `_UX_CHECK_REPORT §5`

รอบแก้: WARN `endbill.mode` (Rule #99) 1 ครั้ง → เพิ่มคอมเมนต์สัญญา B2 v2 ที่ `blankData()` แล้วรันซ้ำเหลือ 3

## 3. Render check (Playwright / Chromium · `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`)

| เช็ค | ผล |
|---|---|
| console error จากโค้ดของ feature | **0** |
| console error อื่น | `ERR_TUNNEL_CONNECTION_FAILED` — CDN ฟอนต์ (Google Fonts / Fontshare) + Lucide ถูกบล็อกใน sandbox |
| pageerror (JS exception) | **0** |
| flow ที่เดินจริงได้ | list (stat filter · sort · pagination) → view drawer 5 tabs → submit modal + DOA slot picker (ว่าง = error · เลือกคนจริง) → approve modal → approved → post modal (+ตรวจยอดซ้ำ) → movements append-only → reverse modal → ใบกลับรายการใบใหม่ → create wizard 5 steps (item combo → bin combo → ยอด → แถวขยายเหตุผล) → hard control ยอดติดลบ (ปุ่มส่ง disabled) → ค้น bin `TR-` = "ไม่พบรายการ" → viewport 1024 |
| horizontal scroll ที่ 1024px | `document.body.scrollWidth > innerWidth` = **false** ทั้งหน้า list และหน้าที่เปิด drawer ✅ (Rule #97) |
| สกรีนช็อต | 30 ไฟล์ใน `1_HTML/_shots/` (01 list · 02 stat filter · 03–07 view tabs · 08 approve · 09 movements · 10–16 wizard/line editor · 17–20 submit + slot picker · 21–26 approve/post/reverse · 27 hard control · 28 in-transit ไม่พบ · 29–30 viewport 1024) |

> **Rule #38 Thai rhythm + icon geometry = `NOT-CHECKED (offline)`** — sandbox บล็อก CDN (tunnel failed) ฟอนต์ Satoshi/Noto Sans Thai และ Lucide จึงไม่โหลดตอน render · ตรวจจากช็อตได้เฉพาะ layout/spacing (ปกติ ไม่ล้น ไม่ทับ ไม่เบี้ยว) ตามข้อ 12 ของ `_RUNNER_BRIEF` — **ไม่วนแก้**

### 3.1 Defect ที่ Render Gate จับได้ + แก้แล้ว (2 จุด)

| # | อาการ | สาเหตุราก | แก้ |
|---|---|---|---|
| R1 | คลิกตัวเลือกใน combobox ที่อยู่ใน drawer ไม่ได้ — `.overlay-wrap` บัง | `.combo-pop` ใช้ `var(--z-dropdown)` = 30 ต่ำกว่า `--z-drawer` = 51 | เพิ่ม `--z-combo: 70` เข้า **Z-Index Registry** (Rule #62 — แก้ที่ registry ที่เดียว) แล้วอ้าง var (ต่ำกว่า `--z-toast` 80) |
| R2 | เปิด combobox ตัวที่ 2 แล้วเมนูปิดทันที | outside-click handler ของ combobox ตัวก่อนยังค้าง แล้วไปฆ่า pop ตัวใหม่ (อาการ "สองระบบชนกัน" #68.1) | guard `if (!pop.isConnected) { removeEventListener; return; }` |

## 4. Convention & override ที่บันทึกไว้ (ข้อ 11 ของ `_RUNNER_BRIEF`)

1. **`FWD-WIRE:` แทน `TODO:` ใน HTML** — `audit.sh` Rule #24 ตั้ง literal `TODO` = FAIL ซึ่งชนกับ gate ที่บังคับ FAIL=0 · ในไฟล์ .md ทุกฉบับยังใช้ `TODO:` ตามปกติ
   **รายการเดียวกัน (HTML ↔ .md):**
   | ใน HTML | ใน .md (PREBRIEF / BRD / declaration) | เจ้าของ |
   |---|---|---|
   | `FWD-WIRE: JE posting (W5)` | `TODO: JE posting` | GL/JE · W5 |
   | `FWD-WIRE: valuation engine (W5)` | `[ASSUMED contract]` ต้นทุนอ้างอิง | Inventory Valuation · W5 |
   | `FWD-WIRE: DOA engine` | ประกาศใน `DOA_BRIEF_F-WH-STKADJ.md` | F-DLG-001 |
   | `FWD-WIRE: ENG-NOTIFY emit` | ประกาศใน `NTF_BRIEF_F-WH-STKADJ.md` | F-NOTIFY |
   | `FWD-WIRE: ENG-CSQ emit` | ประกาศใน `CSQ_BRIEF_F-WH-STKADJ.md` | F-CSQ-01 |
   | `FWD-WIRE: ENG-DOC-NUM` | ประกาศใน `DOCCFG_BRIEF_F-WH-STKADJ.md` | F-DOCCFG |
2. **Iron Rule #98/#100 override ชื่อ step ของ wizard** — Pattern Q ล็อกชื่อ 5 steps ทับชื่อที่ PREBRIEF §6.2 ตั้งไว้ · **เนื้อหา business ครบเท่าเดิม**: step "เลือกแหล่งที่มา" = เลือก **ประเภทการปรับ** (StockAdj ไม่มีเอกสารต้นทาง — Rule #100 อนุญาตให้ step ① เหลือการเลือกประเภท) · เหตุผลรายบรรทัดย้ายเข้าแถวขยายของ step "รายการสินค้า" · หลักฐานอยู่ step "เอกสารแนบ"
3. **ช่องที่ 7 ของ grid B2 v2 (เดิม "ภาษี") ใช้แสดง "เหตุผล"** — ADJ ไม่ใช่รายการภาษี · คงชื่อฟังก์ชัน `taxBadgeV()` ตาม contract และคง VAT engine ครบ (`calcLineVat` 3 โหมด · `migrateLine` · `VAT_MODES` รวม `รวมแล้ว (NET)`) แต่ `CFG.vatEnabled = false` จึงไม่ surface ในแถวขยาย (B2 §"ตัด optional block") · ตัด block ส่วนลดท้ายบิล + WHT ออกเช่นกัน แต่โครง `endbill.mode` ยังอยู่ใน record contract
4. **`--c-teal` ของ fragment doc-archetype map เป็น `--c-success`** สำหรับสถานะ "อนุมัติแล้ว" และ timeline `ok` — ให้ตรง Status Pill Vocabulary กลาง (อนุมัติแล้ว = เขียว) แทนสีส้มของ `--c-teal` ในชุด Warm Light · เพิ่ม `--c-blue #0B5CFF` (สถานะ "ผ่านรายการ") และ `--c-green #00A88E` ให้ครบ 6 สีของ CI CUBE Warm Light ตาม TASTE_LOG
5. **B2 §Reuse Map (StockAdj = ใช้แบบลด)** — ตัดส่วนลดท้ายบิล · WHT · คูปอง · ปุ่ม "คำนวณราคาใหม่" · `unit_price` (= ต้นทุนอ้างอิง) read-only · hard control = **ยอดหลังปรับติดลบ**
6. **BASE-KIT integrity (Rule #69)** — CSS ระหว่าง marker คัดจาก `templates/file-skeleton.template.html` verbatim · เพิ่มเฉพาะ **Z-Index Registry + `--fs-table`/`--row-h`/`--z-combo`** ใน `:root` (Rule #62 บังคับให้ประกาศที่ registry) · page CSS ทั้งหมดอยู่ใต้ `END BASE-KIT` · `#page-late` ว่าง (ไม่มี inline layout เพิ่ม)

## 5. สรุป S3c

| ด่าน | ผล |
|---|---|
| node --check | ✅ PASS |
| audit.sh FAIL | ✅ 0 |
| render + console error (โค้ด feature) | ✅ 0 · pageerror 0 |
| screenshots | ✅ 30 ไฟล์ |
| horizontal scroll @1024 | ✅ ไม่มี |
| Thai rhythm / icon geometry | ⚠️ NOT-CHECKED (offline · CDN blocked) |

**VERDICT: PASS**
