---
name: qc-coverage-checker
description: "Quality Gate ตรวจ 'ทำครบมั้ย' เชิง business scope — เทียบ artifact กับ workflow_graph.json + NODE_BRIEF จาก plan-module-workflow-mapper ว่า feature ครอบทุก node/edge/golden rule ที่ประกาศไว้ ทำงาน 2 จังหวะ: รอบ 1 ตรวจ HTML prototype (ทุก edge out มี hook ใน UI มั้ย เช่น GRN มีทางไป RTV/Credit Note, golden rules ถูก reflect มั้ย, exception paths มีทางเข้ามั้ย, scope creep มั้ย) รอบ 2 ตรวจ FRD Pack + Test cases ก่อนส่ง dev (rules อยู่ใน 05_RULES, TC ครอบทุก block rule + exception path) ทุก ✓ ต้องมี evidence ชี้ตำแหน่ง ห้ามเช็คจากความจำ ใช้เมื่อ user พูดถึง 'qc-coverage-checker', 'ตรวจครบมั้ย', 'coverage check', 'ทำครบหรือยัง', 'เช็ค scope', 'ครบตาม graph มั้ย', 'ตรวจกับ NODE_BRIEF', 'gap check', 'ตรวจก่อน pack', 'มี hook ครบมั้ย', 'ขาดอะไรมั้ย', 'ตรวจความครบ' — ใช้ทุกครั้งหลัง HTML ผ่าน ux gate และก่อน pack ส่ง dev แม้ไม่เรียกชื่อ skill Output: _COVERAGE_REPORT.md + coverage matrix + verdict PASS/WARN/BLOCK ห้ามใช้ตรวจ CI/iron rules/ความเรียบร้อย UI — นั่นคืองาน qc-ux-html-checker"
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
| `workflow_graph.json` หรือ `NODE_BRIEF F-XXX` | ✅ (อย่างน้อย 1) | ✅ |
| node id ที่ตรวจ | ✅ | ✅ |
| ไฟล์ .html | ✅ | ✅ (อ้าง evidence ร่วม) |
| FRD Pack (โฟลเดอร์/ไฟล์) | — | ✅ |
| testcases-*.md (จาก ai-testcase-md-generator) | — | ✅ |
| BRD | — | optional |

ถ้าได้ graph เต็ม → รัน `scripts/coverage_checklist.py` สกัด slice ของ node ก่อน
ถ้าไม่มีทั้ง graph และ brief → **หยุด** แนะนำรัน plan-module-workflow-mapper ก่อน
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

### Phase 1 — รอบ 1: HTML vs Contract

ไล่ checklist ทีละข้อ หา evidence ใน HTML จริง (เปิดไฟล์ ไล่ route):

| ตรวจ | เกณฑ์ผ่าน | Evidence ที่ต้องจด |
|---|---|---|
| Edge **out** ทุกเส้น | UI มี "ทางไป" จริง — ปุ่ม/action/สถานะ/แถวเมนู ที่พาไป node ปลาย | route + selector + ข้อความบนปุ่ม |
| Edge **in** ทุกเส้น | UI รองรับการอ้างอิง — ช่องเลือก/แสดง document ต้นทาง + fields ตาม edge.fields | route + field ที่แสดง |
| Golden rule (block) | พฤติกรรม UI/mock logic สะท้อน rule — หรือ rule เป็น backend-only → mark `N/A-UI` พร้อมเหตุผล (ไปเก็บที่รอบ 2) | จุดที่เห็น validate/state/microcopy |
| Exception paths | มีทางเข้าใน UI (สถานะ, ปุ่ม, tab, filter) ไม่ใช่แค่ happy path | route + องค์ประกอบ |
| Scope guard | ของที่ brief ระบุว่า "ห้ามหลุดเข้ามา" ไม่โผล่ใน HTML | ถ้าโผล่ → flag scope creep |

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

### Phase 3 — Coverage Matrix + Report

สร้าง `_COVERAGE_REPORT.md` ตาม `references/report-format.md` หัวใจคือ matrix:

```
| Item (rule/edge/path) | HTML | FRD | TC | Evidence |
|---|---|---|---|---|
| GR-GRN-04 over→RTV/CN | ✓ #/grn/view ปุ่ม "ส่งคืน" | ✓ 05_RULES §4 | ✗ ไม่มีเคส | ... |
```

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

## References

- `references/check-protocol.md` — รายละเอียดวิธีหา evidence ต่อ artifact + เคสก้ำกึ่ง
- `references/report-format.md` — โครง _COVERAGE_REPORT.md + ตัวอย่าง
- `scripts/coverage_checklist.py` — สกัด checklist ของ node จาก graph + validate graph
