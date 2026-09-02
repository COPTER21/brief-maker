---
name: ai-testcase-md-generator
description: >-
  อ่าน feature pack (FRD + BRD + HTML ต้นทาง) แล้ว "เขียน" Test Case ละเอียดที่สุดเป็น Markdown
  ไฟล์เดียว — ไม่มีภาพ/HTML ไม่ต้องรัน script. ปลายทางคือ AI agent (browser-use/vision) จึง anchor
  ทุก action/expected ด้วยข้อความที่เห็นบนจอ + route จริง, expected เช็คได้ด้วยตา, มีตารางผล ☐ +
  result schema, ครอบคลุม happy/negative/edge/error/permission + trace กลับ FRD (06_TESTS/05_RULES).
  ทำงานที่ SOW3.5 ของ WF-01 คู่กับ qa-friendly-html-generator. v1.2 รองรับ FRD v6.1: XT cross-module
  (§6.9), microcopy กลาง v6 เป็น anchor source (Sync Read — ห้าม hardcode ข้อความ), Coverage
  Manifest cross-check (§0.12), Scope Lock verify, [AI-DEFAULT] propagation
  verify. ใช้เมื่อ user พูดถึง "สร้าง AI test case", "testcase ให้ browser-use รัน", "test case เป็น md",
  "แปลง FRD+HTML เป็น testcase", "ai-testcase-md-generator", "md testcase สำหรับ automate",
  "ให้ AI อ่านแล้วเทสตามหน้าจอ", "testcase จาก pack", "SOW3.5". ใช้ทุกครั้งที่มี pack แล้วอยากได้
  test case markdown ให้ AI รันเอง.
---

> **Sync Read (2026-08-25):** ทุกที่ที่อ้าง `html-generator-v9` = html-generator **เวอร์ชันสูงสุดที่ติดตั้ง**
> (`GEN=$(ls -d /mnt/skills/user/html-generator-v* | sort -V | tail -1)`) — ณ วันนี้คือ v9 (Pattern Q/P · B2 v2 · Iron Rules #1–#103)
> ห้าม hardcode CI/จำนวนกฎ/px จาก generator เก่า · FRD = frd-generator-v6 · BRD = brd-generator-full

# ai-testcase-md-generator — v1.1 Workflow Edition

**ตำแหน่งใน workflow:** WF-01 · SOP3 · SOW3.5 (คู่กับ `qa-friendly-html-generator` ที่รับ testcases-*.md ไปทำ UAT HTML แบบ 1:1)
**DoD:** Coverage Audit = 100% ของ in-scope (รวม XT) + Ledger cross-check กับ FRD Coverage Manifest ผ่าน

อ่าน feature pack แล้ว **เขียน Test Case ละเอียดที่สุด** เป็น **Markdown ไฟล์เดียว** สำหรับให้
**AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบนหน้าจอจริง + รายงานผลกลับ.

> อ่าน `references/iron-rules.md` ให้ครบก่อนเริ่มเสมอ และยึด `references/output-format.md`
> เป็นโครงสร้างไฟล์ผลลัพธ์เป๊ะ ๆ

## หลักคิดที่ทำให้ skill นี้ต่างจากเพื่อนบ้าน
ผู้บริโภคคือ **AI** ไม่ใช่คน — จึง **กลับขั้ว** จาก qa-friendly-html-generator (ที่ห้ามมีศัพท์
เทคนิคเพราะคนอ่าน). ที่นี่เรา *คง* รายละเอียดที่ agent ใช้นำทางได้: route ที่ต้องไป + anchor ด้วย
"ข้อความ/ป้ายที่เห็นบนจอ" + expected ที่เช็คได้จากสิ่งที่ปรากฏ. งานหลักคือ **ใช้สมองอ่าน pack
แล้วเขียน** ไม่ใช่รัน engine ใด ๆ.

**ต่างจากตัวอื่น:** ไม่ใช่ `qa-html-to-ai-testset` (ตัวนั้นเป็น *extractor* — ต้องมี HTML ที่ฝัง
PAYLOAD มาก่อน); ไม่ใช่ `frd-qa-generator*` (.docx/CSV สำหรับคน/Feature Tester); ตัวนี้
**generate จาก pack ตรง ๆ → MD ล้วนสำหรับ agent**.

## Input
- **FRD** — เน้น `06_TESTS` (ดึงเคส/trace — รวม **§6.9 XT cross-module** + **§6.10 microcopy note**),
  `05_RULES` (rule → negative/edge), `01_UI` + `03_LOGIC` (เขียน expected และลำดับ step),
  **`00_OVERVIEW §0.12 Coverage Manifest`** (cross-check Ledger), **Scope Lock** (`07_LOCKED §7.0`
  หรือ `00 §0.11`). รับ pack mode หรือไฟล์เดี่ยวก็ได้ (v6 หรือ v5 ก็อ่านได้ — ชื่อไฟล์เดิม)
- **BRD** (ถ้ามี) — scope, business rule, actor/permission
- **HTML ต้นทาง** ของฟีเจอร์ (สำคัญ) — อ่านเพื่อรู้ **route จริง** (hash routing `#/...`), **ข้อความ/
  ป้ายของ element จริง** (ปุ่ม/ฟิลด์/หัวข้อ/ตาราง/ป้ายสถานะ), และ flow
  - ถ้าไม่มี HTML: ยังเขียนได้จาก FRD แต่ทุก anchor ที่ยืนยันไม่ได้ต้องติด `⚠ ไม่พบใน HTML`

## Output
ไฟล์เดียว `testcases-<feature>.md` — pure Markdown, ไม่มีภาพ/base64/HTML. โครงตาม
`references/output-format.md`.

---

## กระบวนการ 6 ขั้น (ลำดับนี้สำคัญ — Ledger ต้องมาก่อนเขียนเคส)

### 1) อ่าน pack ให้ทะลุ — อ่าน **ทุกไฟล์** ที่ให้มา
อย่าอ่านแค่ 1-2 ไฟล์. ต้องเปิด: **06_TESTS** (FR + acceptance ราย layer), **05_RULES** (rules + edge
cases + error catalog + permission matrix + validation schema), **01_UI** (pages/routes/anchors/
journeys), **03_LOGIC/02_API/04_DB** (เสริม), **BRD** (scope, OOS). + HTML ต้นทางถ้ามี.
ทำสารบัญในหัว: routes ทั้งหมด (hash จริง), element/ข้อความที่เห็นต่อหน้า, rules/EC/error ทั้งหมด,
**XT ทั้งหมด (§6.9), LOCK ทั้งหมด (Scope Lock), แถว Coverage Manifest (§0.12)**.

> **Fallback — pack คนละฟอร์แมต:** ชื่อไฟล์ `06_TESTS/05_RULES/01_UI` เป็นชื่อมาตรฐานของ
> frd-generator-v6 (v5 ใช้ชื่อเดียวกัน — อ่านได้ทั้งคู่). ถ้า pack ใช้ชื่ออื่น/รวมไฟล์เดียว ให้ **map ตามเนื้อหา** แทน: หาส่วนที่เป็น acceptance/FR
> (= 06_TESTS), business rules + error + permission (= 05_RULES), pages/routes/UI (= 01_UI). ถ้าไม่มี
> HTML และไม่มี 01_UI ให้ดึง anchor จาก BRD/screenshot เท่าที่มี แล้วติดธง `⚠ ยืนยัน anchor` ให้มากขึ้น.

### 2) ★ สร้าง Coverage Ledger ก่อน + ออกให้เห็นก่อนเขียนเคส (Ledger-first gate)
**v1.3 (lane v2):** ถ้ามี `01_FUNCTION_CHECKLIST.md` → Ledger ต้องมีแถว **ทุก FN-XX** (คอลัมน์ `FN | S-XX | BR | TC ids`) — FN ไม่มี TC = Ledger ไม่ครบ · หมวด "ไม่รองรับ" = ข้าม พร้อมเหตุ · FN-90..93 (ทั่วไป) ต้องมี TC เหมือนกัน · Coverage Audit เพิ่มบรรทัด `FN cross-check: ✅ N/N`
ไล่ **ทุก item** ที่ทดสอบได้ออกมาเป็นตาราง **ก่อน** เขียนเคส: ทุก FR, ทุก rule (R-xxx), ทุก EC,
ทุก error code, ทุก field validation, ทุก cell ของ permission matrix, cross-cutting, events, states,
**ทุก XT (06_TESTS §6.9 cross-module — v6)** และ **ทุก LOCK (Scope Lock — ต้องมีเคส verify)**.
**Cross-check กับ FRD `00 §0.12 Coverage Manifest`:** ทุกแถวใน manifest ต้องมีคู่ใน Ledger —
manifest มีแต่ Ledger ไม่มี = Ledger ยังไม่ครบ. ของที่อยู่นอก Scope Lock (Exclusions) → **ห้ามสร้างเคส**
(ลง Ledger เป็นข้าม เหตุผล "นอกขอบเขตใบเซ็น").
**ออก Ledger + โครง Coverage Audit (covered/total) ให้เห็นและเช็คว่าครบก่อน** แล้วค่อยลงมือเขียนเคสจริง
ทุกแถวต้องได้ case (หรือ mark ข้ามพร้อมเหตุผล). นี่คือ "รายการที่ต้องเก็บให้ครบ" — ถ้ายังไม่ครบ ห้ามข้ามไปขั้น 5.

### 3) ขยายแต่ละแถว → หลายเคส ด้วย `references/derivation-playbook.md`
เดินทุกแถวผ่าน playbook ตามชนิด (ฟิลด์ → required/format/boundary/enum/FK/unique; permission →
allow+deny ทุก cell; list → search/filter ทุกค่า/sort/pagination/states; 1:N → add/delete/primary/
auto-promote; cascade; CSV; bulk; convert atomic; PII/RLS; state machine; UX dirty-check; EC).
**pack FULL คาดหวัง 50-100+ เคส** — อย่าหยุดที่ happy path.

### 4) Ground anchor — ลำดับแหล่ง: HTML จริง > 01_UI > microcopy กลาง v6 ⭐ v1.2
ทุกเคสกำหนด **Start** route (refresh-safe — v6.1 pack: 01_UI มี route ทุกหน้า copy ได้ตรง ๆ).
ทุก action/expected ผูกกับ **ข้อความ/ป้ายที่เห็นจริง** ตามลำดับแหล่ง:
1. **HTML ต้นทาง** (ดีสุด — ข้อความจริง verbatim)
2. **01_UI** ของ pack (FRD v6.1 เขียนจาก HTML เดียวกัน — ปกติตรงกับข้อ 1; **ถ้าไม่ตรง → HTML ชนะ
   + note drift ไว้หัวไฟล์** เพราะแปลว่า FRD กับจอหลุดกัน เป็นสัญญาณให้คนไป investigate)
3. **microcopy กลางของ html-generator-v9** — อ่านสดจาก
   `/mnt/skills/user/html-generator-v9/knowledge/microcopy.md` (ถ้า v6 ไม่มี → หา `html-generator-v*`
   เวอร์ชันสูงสุดที่ติดตั้ง + log ว่าใช้ตัวไหน) — สำหรับข้อความมาตรฐาน: toast, ปุ่ม primary,
   confirm ลบ, empty state, status pill vocabulary
   → ข้อความจากแหล่งนี้ **ไม่ต้องติดธง** ⚠ (เป็น standard ที่ enforce แล้ว)
   → **ห้าม hardcode ตัวอย่างข้อความ/สี pill ในเคสจากความจำ** — ต้องเปิดไฟล์ microcopy จริงทุก session
     (บทเรียน: v1.1 ฝังข้อความ/สียุค Navy ไว้ในตัว skill — v6 เปลี่ยนเป็น Warm Light แล้วค่าพวกนั้นผิดหมด)
ห้าม CSS selector ดิบ/JS. element ไม่มีข้อความ → บรรยายตำแหน่งที่เห็น. anchor ที่ทั้ง 3 แหล่งยืนยันไม่ได้
→ ติด `⚠ ยืนยัน anchor`. (FRD v6.1 §6.10 เขียน expected verbatim จาก HTML อยู่แล้ว — copy ได้ตรง ๆ)

**[AI-DEFAULT] propagation (v1.2):** rule ใน 05_RULES ที่ติด `[AI-DEFAULT]` (FRD v6.1 Lane Mode
ตอบ probe เอง) → ทุกเคสที่ derive จาก rule นั้นต้องติด `[AI-DEFAULT]` ที่หัวเคสด้วย —
ให้คนรัน UAT รู้ว่าเกณฑ์ข้อนี้ AI ตัดสินแทน BA อยู่ ผลเทส fail อาจแปลว่า "default ผิด" ไม่ใช่ "โค้ดผิด" 

### 5) เขียน Test Cases (ยึด output-format.md + iron-rules.md)
- หัวเคส: group · ความสำคัญ · `trace:` (FR/rule/EC/error) · actor · **`Setup:` (role+seed+files)** · Start · ชุดข้อมูล · ผ่านเมื่อ
- ตาราง step = `# | Action | Input | Expected | Result(☐)`
- **Action ทุกช่องขึ้นต้น verb tag** (OPEN/CLICK/TYPE/SELECT/TOGGLE/UPLOAD/PRESS/VERIFY) + target ที่เห็น (R13)
- ไฟล์อัปโหลดใช้ **ชื่อจริง** (R8) ระบุใน `### ไฟล์ทดสอบ (Files)` ของ Data Sets + ใน Setup
- **เคส XT (cross-module):** Setup ต้องระบุ seed ของ module ปลายทาง (เช่น `seed=budget line มี commitment ของ PR นี้`);
  ถ้า prototype ไม่มีหน้า module ปลายทาง → mark `(ต้อง simulate)` + Expected เช็คจาก event/toast/สถานะฝั่งต้นทางแทน
- happy-flow หลาย section → step ต่อ section (R12); Expected เช็คได้ด้วยตาเสมอ (R4)

### 6) ★ Coverage Audit + ส่งมอบ
ปิดท้ายด้วย `## Coverage Audit` นับจริง `covered/total` ต่อหมวด (**รวมหมวด XT + LOCK — v1.1**) + list รายการที่ข้าม (เหตุผล Phase 2/OOS/นอกขอบเขตใบเซ็น) + บรรทัด **Manifest cross-check: ✅/❌**.
ถ้าไม่ครบและไม่มีเหตุผล = กลับไปเพิ่มเคส (R11). **ห้าม truncate** — pack ใหญ่ (>~60 เคส) เขียน/append
ทีละ group จนครบ เคสกลุ่มท้ายลึกเท่ากลุ่มแรก (R15). ถ้าเป็น **regen** ของ pack เดิม คง TC-id เดิม
เพิ่มเคสใหม่ต่อท้าย (R16). แล้ว `present_files` ไฟล์ `.md` เดียว.

---

## ไฟล์ในสกิล
```
SKILL.md
references/
  iron-rules.md            # R1–R12 (R5 ไล่ครบ · R11 audit · R12 depth) — กฎกลับขั้ว
  derivation-playbook.md   # เมนูแตก 1 element → หลายเคส (ใช้ขั้น 3)
  output-format.md         # โครงไฟล์ .md (มี Coverage Ledger + Coverage Audit) — ยึดเป๊ะ
examples/
  testcases-F-CUSTOMER.md  # ตัวอย่างจริงจาก FULL pack (Core CRM Customer) — บาร์ความครบ/ละเอียด
```

## หมายเหตุ
- ไม่ต้องมี dependency/script/Playwright — งาน "อ่าน→เขียน" ล้วน ผลลัพธ์เปิดอ่านได้ทุกที่
- pack ใหญ่หลายฟีเจอร์ → ทำ **ทีละฟีเจอร์ = 1 ไฟล์ .md** (อย่ายัดรวม)
- ถ้าได้เคสน้อยผิดปกติ (FULL pack แต่ < 30 เคส) = ยังไล่ Coverage Ledger ไม่ครบ ให้กลับไปขั้น 2–3
