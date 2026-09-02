---
name: qc-coverage-checker
description: "Quality Gate ตรวจ 'ทำครบมั้ย' เชิง business scope — เทียบ artifact กับ contract: workflow_graph.json + NODE_BRIEF และ/หรือ PREBRIEF + FUNCTION_CHECKLIST FN-XX (feature-prebrief) · Declaration coverage (DOA/NTF/CSQ/DOCCFG brief ต้องมีเมื่อเข้าเงื่อนไข · chip≠detect = DIVERGENCE) · Pattern Q surface coverage (html-generator-v9) ทำงาน 2 จังหวะ: รอบ 1 HTML (ทุก edge/FN/scenario มี hook จริง, exception path มีทางเข้า, scope creep) รอบ 2 FRD Pack + TC (rules ใน 05_RULES, FN↔TC ledger, R15) ทุก ✓ ต้องมี evidence ใช้เมื่อ user พูดถึง 'qc-coverage-checker', 'ตรวจครบมั้ย', 'coverage check', 'เช็ค scope', 'gap check', 'ตรวจก่อน pack', 'ขาดอะไรมั้ย' — ใช้ทุกครั้งหลัง HTML ผ่าน ux gate และก่อน pack ส่ง dev Output: _COVERAGE_REPORT.md + matrix + verdict PASS/WARN/BLOCK ห้ามใช้ตรวจ CI/iron rules — นั่นคือ qc-ux-html-checker"
---

# QC: Coverage Checker

## Purpose

ด่านตรวจ "ทำ**ครบ**มั้ย" (substance) — ตอบคำถามที่ทำให้ทีมวน vibe นาน:
"GRN ตัวนี้ครอบรับเกิน/รับขาดหรือยัง ต้องต่อ Credit Note มั้ย มี RTV มั้ย"
โดย**ไม่ใช้ความจำหรือความรู้สึกตัดสิน** — ใช้ contract ที่ประกาศไว้แล้วใน
`workflow_graph.json` + `NODE_BRIEF` (จาก plan-module-workflow-mapper) เป็นเกณฑ์เดียว

ไม่ตรวจ CI/iron rules/ความเรียบร้อย UI — นั่นคืองาน `qc-ux-html-checker`

## หลักการ 3 ข้อ (บังคับ)

1. **Graph คือ contract** — เกณฑ์ "ครบ" มาจาก graph/brief เท่านั้น ไม่ invent เกณฑ์ใหม่
   จากความรู้ ERP กลางอากาศ (ถ้าเห็นว่า graph เองขาด → เสนอกลับไป update ที่ mapper
   ห้ามแก้ graph เองใน skill นี้ — กัน truth แตก)
2. **Evidence-based** — ทุกช่อง ✓ ใน matrix ต้องชี้ตำแหน่งได้ (route+selector /
   ไฟล์ FRD+section / TC id) หา evidence ไม่เจอ = ✗ ไม่มี "น่าจะมี"
3. **สองจังหวะ คนละคำถาม** — รอบ 1 ถาม "UI มีทาง/ช่อง/สถานะรองรับครบมั้ย"
   รอบ 2 ถาม "spec และ test ผูกเรื่องพวกนั้นครบมั้ย"

## Input

| Input | รอบ 1 | รอบ 2 |
|---|---|---|
| `workflow_graph.json` หรือ `NODE_BRIEF F-XXX` | ✅ (อย่างน้อย 1 จาก 2 แถวนี้) | ✅ |
| **`PREBRIEF_F-XXX.md` + `FUNCTION_CHECKLIST_F-XXX.md`** (feature-prebrief) — ★ contract หลักใน auto-lane v9 | ✅ (อย่างน้อย 1 จาก 2 แถวนี้) | ✅ |
| `*_BRIEF.md` (DOA/NTF/CSQ/DOCCFG declaration) | ✅ ถ้าเข้าเงื่อนไข | ✅ |
| node id ที่ตรวจ | ✅ | ✅ |
| ไฟล์ .html | ✅ | ✅ (อ้าง evidence ร่วม) |
| FRD Pack (โฟลเดอร์/ไฟล์) | — | ✅ |
| testcases-*.md (จาก ai-testcase-md-generator) | — | ✅ |
| BRD | — | optional |

ถ้าได้ graph เต็ม → รัน `scripts/coverage_checklist.py` สกัด slice ของ node ก่อน
ถ้าได้ PREBRIEF/FUNCTION_CHECKLIST → รัน `scripts/prebrief_checklist.py <FUNCTION_CHECKLIST.md> <PREBRIEF.md> --html <file.html>`
→ ได้ FN-XX / S-XX / BR-XX / ไม่รองรับ / declaration signals / keyword hits ต่อ FN (แค่ตัวช่วยหา — evidence จริงต้องเปิดดู)
มีทั้งคู่ → **graph = เส้นเชื่อมข้าม feature** · **FN-XX = ความสามารถภายใน feature** ตรวจทั้งสองชั้น
ถ้าไม่มีสักอย่าง → **หยุด** แนะนำรัน plan-module-workflow-mapper หรือ feature-prebrief ก่อน
(ไม่มี contract = ตรวจความครบไม่ได้ อย่าเดาแทน)

---

## Workflow

### Phase 0 — เตรียม Checklist จาก Contract

1. โหลด graph/brief → รัน `scripts/coverage_checklist.py <graph.json> <node-id>`
   ได้ checklist JSON: edges in, edges out, golden rules (แยก block/warn),
   cross-node rules ที่แตะ node นี้, scope guard
2. ตรวจสุขภาพ contract ก่อน: ถ้า node ไม่มีใน graph / brief กับ graph ขัดกัน →
   แจ้งก่อน ห้ามเลือกเองเงียบ ๆ
3. แตก exception paths จาก edges type `reversal` + rules ที่พูดถึง exception
   ให้เป็นรายการตรวจชัด ๆ (เช่น over-receipt → RTV, over-receipt → CN)

### Phase 0b — Declaration Coverage (v9 · บังคับ)

จาก chip บนแผง (BACKLOG/LANE_BRIEF) **หรือ** สัญญาณใน PREBRIEF (`declarations` จาก prebrief_checklist.py):

| ท่อ | เข้าเงื่อนไขเมื่อ | ต้องมี | ไม่มี → |
|---|---|---|---|
| DOA | มี action อนุมัติ/ส่งอนุมัติ/ไม่อนุมัติ/เซ็น หรือ status `pending_approval` | `DOA_BRIEF_[F].md` + HTML มี slot picker เลือกคน (`.slot-row` · avatar+ตำแหน่ง+ชื่อ) + ไม่มี hardcoded chain | BLOCK |
| NTF | มี transition ที่ "ใครต้องรู้" (มอบหมาย/ส่งลูกค้า/threshold/ไฟล์แนบ) — ไม่นับ doa_pending/doa_result | `NTF_BRIEF_[F].md` + ทุก event ใน brief map กลับ S-XX/FN-XX ได้ | BLOCK |
| CSQ | กระทบ ต้นทุน/มูลค่า · ข้อมูลอ่อนไหว · บัญชี · เงินสด/งบ · ตัดสินใจปลายทาง | `CSQ_BRIEF_[F].md` — ห้ามประกาศ OC / DC-document / SC (register 422) | BLOCK |
| DOCCFG | เอกสารธุรกรรม (Pattern Q) / มีเลขรัน | `DOCCFG_BRIEF_[F].md` + HTML ไม่ hardcode รูปแบบเลข | BLOCK |
- chip กับ detect **ไม่ตรงกัน** → ตรวจตาม detect + ลง report หมวด `DIVERGENCE` (Strike ตัดสิน) — ห้ามเลือกเองเงียบ ๆ
- รอบ 2: FRD ต้อง sync read brief เดิม (event/slot ที่เพิ่มจาก HTML ต้อง append ใน brief ไม่ใช่ใบใหม่)

### Phase 0c — Archetype Surface Coverage (v9 · เมื่อ feature เป็นเอกสารธุรกรรม)

ไม่ตรวจความถูกของ UI (นั่นคือ qc-ux Pass D) — ตรวจว่า **business ครบทุก surface** ตาม `html-generator-v9/patterns/Q_*.md`:
| Surface | ต้องมี evidence |
|---|---|
| List | ทุกสถานะใน state machine ของ PREBRIEF โผล่ใน filter + `docPill` · แกนสถานะรอง (จัดส่ง/จ่าย/รับ) ที่ PREBRIEF ระบุ = คอลัมน์ตัวเอง |
| Wizard | step 1 มีเอกสารต้นทางครบทุก edge-in · step 2 field ครบตาม PREBRIEF data · step 3 line rule ครบ (BR ที่เกี่ยวกับ qty/price/discount/VAT) · step 5 review แสดงทุก field ที่ validate |
| View | ทุก edge-out มีปุ่ม/tab (เช่น SO → DN/INV/CN) · tab ลายเซ็น = DOA chain · tab ประวัติ = audit append-only · เอกสารแนบ section |
| PDF | ฟิลด์ตามเอกสารทางการ (ผู้เสียภาษี/สาขา ถ้า FRD ระบุ) · 3 ช่องเซ็น |
| Modals | ทุก transition ที่ต้องมีเหตุผล (ไม่อนุมัติ/ยกเลิก/พัก) มี reason modal |

### Phase 1 — รอบ 1: HTML vs Contract

ไล่ checklist ทีละข้อ หา evidence ใน HTML จริง (เปิดไฟล์ ไล่ route):

| ตรวจ | เกณฑ์ผ่าน | Evidence ที่ต้องจด |
|---|---|---|
| Edge **out** ทุกเส้น | UI มี "ทางไป" จริง — ปุ่ม/action/สถานะ/แถวเมนู ที่พาไป node ปลาย | route + selector + ข้อความบนปุ่ม |
| Edge **in** ทุกเส้น | UI รองรับการอ้างอิง — ช่องเลือก/แสดง document ต้นทาง + fields ตาม edge.fields | route + field ที่แสดง |
| Golden rule (block) | พฤติกรรม UI/mock logic สะท้อน rule — หรือ rule เป็น backend-only → mark `N/A-UI` พร้อมเหตุผล (ไปเก็บที่รอบ 2) | จุดที่เห็น validate/state/microcopy |
| Exception paths | มีทางเข้าใน UI (สถานะ, ปุ่ม, tab, filter) ไม่ใช่แค่ happy path | route + องค์ประกอบ |
| Scope guard | ของที่ brief ระบุว่า "ห้ามหลุดเข้ามา" / หมวด "สิ่งที่ไม่รองรับ" ใน FUNCTION_CHECKLIST ไม่โผล่ใน HTML | ถ้าโผล่ → flag scope creep |
| **FN-XX ทุกข้อ** (จาก FUNCTION_CHECKLIST) | UI ทำได้จริงตามข้อความ (มีปุ่ม/ช่อง/สถานะ + handler เดินได้ ไม่ใช่ปุ่มหลอก) — `keyword_hit_ratio` ต่ำ = จุดสงสัยให้เปิดดูก่อน | route + selector + handler · ติ๊กช่อง WF ของ FN นั้นได้ |
| **S-XX ทุก scenario** (PREBRIEF) | เดินจากทางเข้าจนจบผลลัพธ์ทางธุรกิจได้ใน UI (happy/alt/exception) — `scenarios_without_fn` = contract เองมีรู → เสนอกลับ prebrief | ลำดับ route/action ที่เดิน |
| **Coverage Map ของ generator (Rule #37)** | ถ้า HTML แนบ Coverage Map/summary "Gaps Filled" — ทุกแถว ❌/default ต้องปรากฏใน report นี้ (ไม่ให้ generator ตัดเงียบ) | อ้างแถวใน map |

**ของเกิน contract**: เจอ feature/flow ใน HTML ที่ graph ไม่รู้จัก → แยก 2 กรณี
(a) scope creep ตอน vibe → WARN เสนอถอด/ยืนยัน (b) graph ล้าสมัย →
เสนอ user รัน mapper update mode — ตัวเลือกเป็นของ user เสมอ

### Phase 2 — รอบ 2: FRD + TC vs Contract

| ตรวจ | เกณฑ์ผ่าน |
|---|---|
| Golden rules ทุกข้อ | ปรากฏใน FRD (05_RULES หรือ section ที่ทีมใช้) เนื้อหาตรง ไม่เจือจาง — block rule หายไป = BLOCK |
| Edges ทุกเส้น | FRD ฝั่ง API/LOGIC มี integration/hook ไป node ปลาย (รวม XT cross-module ถ้า FRD v6) |
| N/A-UI จากรอบ 1 | ต้องถูกเก็บใน FRD ครบ — นี่คือจุดที่ของ backend-only ชอบหาย |
| Test cases | ทุก block rule มี TC ≥ 1 · ทุก exception path มี TC ≥ 1 · TC อ้าง trace กลับ rule/edge ได้ |
| Lock refs | rule ที่มี lock_ref → ข้อความใน FRD ไม่ขัดกับ LOCK-XX |
| **FN ↔ TC (ledger-first)** | ทุก FN-XX มี TC ≥1 ใน testcases-*.md ที่ trace กลับ FN/S/BR · จำนวน case/step ตรงกันข้าม MD ↔ QA HTML ↔ AI Testset (R15) |
| **Declaration ↔ FRD** | DOA/NTF/CSQ/DOCCFG brief ถูก sync read ใน FRD (03_LOGIC/05_RULES/§XT) · event ใน FRD ⊆ brief · ไม่มี hardcoded chain/ช่องทางแจ้งเตือน/รูปแบบเลขรันใน FRD |
| **Standard gap (02_STANDARD_GAP)** | ทุก gap ที่ tag [STD] ถูก merge เข้า PREBRIEF และมี FN/TC — ที่ตัดออกต้องอยู่ใน "ไม่รองรับ" พร้อม [มติ/OQ] |

### Phase 3 — Coverage Matrix + Report

สร้าง `_COVERAGE_REPORT.md` ตาม `references/report-format.md` หัวใจคือ matrix:

```
| Item (rule/edge/path/FN/decl) | HTML | FRD | TC | Evidence |
|---|---|---|---|---|
| GR-GRN-04 over→RTV/CN | ✓ #/grn/view ปุ่ม "ส่งคืน" | ✓ 05_RULES §4 | ✗ ไม่มีเคส | ... |
| FN-05 กรอกเกิน+tolerance → บล็อก | ✓ step3 wizardNext toast | ✓ 05_RULES BR-01 | ✓ TC-014 | ... |
| DECL-DOA | ✓ .slot-row submit modal | ✓ 03_LOGIC §DOA sync | ✓ TC-030..033 | DOA_BRIEF_F-XX v1 |
```
matrix ต้องมีแถว **ทุก FN-XX** + **ทุก S-XX** + **DECL-*** (4 ท่อ: ✓ / N/A พร้อมเหตุผล) + **SURFACE-*** (list/wizard/view/pdf/modals ถ้าเป็น Pattern Q)

- **Verdict**: `BLOCK` = block rule/edge ไม่ครอบ ≥1 · `WARN` = warn rule ขาด
  หรือ scope creep · `PASS`
- **Gap list** เรียงตามความเสี่ยง: แต่ละ gap บอก อะไรหาย + ต้องไปเพิ่มที่ไหน
  (HTML route ไหน / FRD ไฟล์ไหน / เพิ่ม TC แบบไหน) — ให้แก้ได้ทันทีไม่ต้องตีความ
- รอบ 2 ให้แนบ diff กับรอบ 1: gap ที่ปิดแล้ว / ยังค้าง / เกิดใหม่

## Quality Gates ของตัว checker เอง

- [ ] ทุก ✓ มี evidence ระบุตำแหน่ง — สุ่มไม่ได้แม้แต่ช่องเดียว
- [ ] ไม่มีเกณฑ์ที่ invent เองนอก contract (ข้อเสนอเพิ่มเติมแยกไว้หมวด "เสนอเข้า graph")
- [ ] item ที่ตรวจไม่ได้ (เช่น ไม่มีไฟล์ FRD ส่วนนั้น) = NOT-CHECKED ไม่ใช่ ✓
- [ ] scope creep ถูก flag เสมอ ไม่ตัดสินแทน user
- [ ] verdict BLOCK เมื่อใดก็ตามที่ block-severity ไม่ครอบ — ไม่มีข้อยกเว้น
- [ ] Declaration coverage (0b) ตรวจทุกครั้ง — ท่อที่เข้าเงื่อนไขแต่ไม่มี brief = BLOCK · chip≠detect ลง DIVERGENCE
- [ ] ใช้ contract เวอร์ชันล่าสุด: FRD v6.1 (XT §6.9 · Coverage Manifest §0.12) · html-generator-v9 Pattern Q · feature-prebrief FN-XX

## References

- `references/check-protocol.md` — รายละเอียดวิธีหา evidence ต่อ artifact + เคสก้ำกึ่ง
- `references/report-format.md` — โครง _COVERAGE_REPORT.md + ตัวอย่าง
- `scripts/coverage_checklist.py` — สกัด checklist ของ node จาก graph + validate graph
- `scripts/prebrief_checklist.py` — ★ v9 สกัด FN/S/BR/ไม่รองรับ/declaration signals จาก feature-prebrief + keyword hits ใน HTML
