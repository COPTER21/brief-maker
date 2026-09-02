---
name: feature-prebrief
description: "เจาะ 1 feature จาก module-expand pack ให้เป็น PREBRIEF = source of truth เชิง business ของ feature นั้น — ครบทุก scenario (happy/alternate/exception เช่น GRN รับครบ/รับบางส่วน/รับเกิน/QC ไม่ผ่าน/ยกเลิก), ทุก flow, ทุก function, full data (header/line/ทุก field/ข้อมูลต่อ scenario) พร้อม Coverage Matrix กันตกหล่น และออก FUNCTION_CHECKLIST (FN-XX ติ๊กได้) ให้ทีมที่ทำต่อเปิดเช็คตาม ใช้เมื่อ user พูดถึง 'feature-prebrief', 'prebrief', 'ทำ prebrief feature', 'เจาะ feature ก่อน wireframe', 'brief ละเอียดเชิง logic', 'feature นี้ต้องทำอะไรได้บ้าง', 'ไล่ scenario ของ feature', 'function checklist', 'source of truth ของ feature', 'หยิบ feature จาก build order มาทำ' — ใช้ทุกครั้งที่หยิบ feature มาเริ่มทำจริง หลัง module-expand ก่อน wireframe-prototype Output: PREBRIEF_[F-code].md + FUNCTION_CHECKLIST_[F-code].md + FUNCTION_CHECKLIST_[F-code].html (ติ๊กได้ 3 ด่าน WF/DEV/QA · save ในเครื่อง · ส่งผล PDF/JSON/สรุปแชท — สร้างจาก md ด้วย scripts/build_checklist_html.py)"
---

> **Sync Read (2026-08-25):** ทุกที่ที่อ้าง `html-generator-v9` = html-generator **เวอร์ชันสูงสุดที่ติดตั้ง**
> (`GEN=$(ls -d /mnt/skills/user/html-generator-v* | sort -V | tail -1)`) — ณ วันนี้คือ v9 (Pattern Q/P · B2 v2 · Iron Rules #1–#103)
> ห้าม hardcode CI/จำนวนกฎ/px จาก generator เก่า · FRD = frd-generator-v6 · BRD = brd-generator-full

# Feature Prebrief — source of truth เชิง business ของ 1 feature

## Purpose

PB จาก module-expand คือใบจองระดับกล่อง — ยังตื้นเกินกว่าจะสร้างของที่ทำงานจริงได้
skill นี้เจาะทีละ feature จนเป็น **source of truth เชิง business**: ใครก็ตามที่อ่าน
(wireframe, dev, QA) ต้องรู้ครบว่า feature นี้ **ทำอะไรได้บ้าง เกิดอะไรได้บ้าง และแต่ละกรณี
ต้องมีข้อมูลอะไร** โดยไม่ต้องเดาเพิ่มเอง

```
module-expand (_EXPAND_[Module]/)
      ▼  หยิบ feature ตามคิว wave
★ feature-prebrief — PREBRIEF_[F-code].md + FUNCTION_CHECKLIST_[F-code].md + .html (ติ๊กส่งผลได้)
      ▼
wireframe-prototype (functional greyscale — implement ตาม PREBRIEF, ทีมติ๊ก CHECKLIST ตาม)
      ▼
[รีวิวหัวหน้า] → decision-log → pack ส่ง dev (v7 → BRD → FRD → TC ก็เช็คกับ CHECKLIST เดิม)
```

**PREBRIEF ≠ FRD**: ไม่มี API/DB schema/test manifest — FRD ตัวจริงยังสกัดจาก HTML ตาม
Reverse Mode PREBRIEF คือสมมติฐาน business ครบถ้วนที่จะ prove ด้วย wireframe ทุกข้อที่ AI
คิดเองติด `[AI-DRAFT]` และกลายเป็น pin ให้หัวหน้าเคาะ

## Input

| Input | จำเป็น | ใช้ทำอะไร |
|---|---|---|
| **`LANE_BRIEF_[F].md` (lane-brief-generator v2)** — ★ lane mode input หลัก | ✅ (lane) | feature · archetype · declarations chips · scope note · LOCK/มติ id · OQ answered/ASSUMED · dep |
| `PB_[F-code].md` + `_CONTRACT_SLICE.md` + `_BUILD_ORDER.md` | ✅ (manual) / ⬜ (lane) | scope, edge, entity/status/enum ร่วม, รู้ว่า mock อะไร |
| Central Plan (workflow_graph) | ⬜ optional | เส้นเชื่อม + global contracts + LOCK — ไม่มีก็ทำได้ (เส้นเข้า/ออกใช้จาก catalog + archetype แทน) |
| `cube-master-knowledge/02_architecture/cube-4.0-current-state.md` + `05_features/feature-catalog-master.md §0` | ✅ | มติ · baseline ที่ต้องเรียกใช้ (DOA/DOCCFG/NOTIFY/Roles/OP) · feature ข้างเคียง |
| `cube-master-knowledge` skill | ✅ | pattern CUBE: DOA placeholder, soft reference LD-4C-02, soft archive, audit append-only |
| **ERP standard research (web)** | ✅ **บังคับ** สำหรับเอกสารธุรกรรม/feature ที่ทีมไม่เคยทำ · ⬜ master ง่าย ๆ | ไล่ scenario มาตรฐานที่ AI/ทีมนึกไม่ถึง (partial receipt, over-receipt tolerance, QC hold, reversal) — SAP/Odoo/D365 · tag [AI-DRAFT][STD] |
| มติจากแชท/หัวหน้า | ⬜ | ใส่เป็น [มติ] ได้เลย |

## Lane Mode (no-ask) — เมื่อ input เป็น LANE_BRIEF จาก feature-lane-runner

- **ถ้ามี `STANDARD_BASELINE.md` ในโฟลเดอร์ brief เดียวกัน (S0.5)** → ทุก capability MUST + ทุก state ใน lifecycle §2 ต้องมี S-XX/FN-XX รองรับ · archetype ใช้ตาม baseline §3 (ทับ archetype ชั่วคราวใน brief · เขียนเหตุใน `archetype_confirmed:`) · MUST ที่ scope note ตัด → ลง "ไม่รองรับ" พร้อม [OQ] ไม่ตัดเงียบ
- **ห้ามถาม** — ทุกช่องว่างตัดสินด้วย default ตาม ERP standard + มติใน current-state แล้ว tag `[AI-DRAFT]` / `[ASSUMED]` (ตาม OQ list ใน brief) · business-critical ที่ brief บอก Hard Stop → หยุดออก `_BLOCKED.md`
- **Archetype จาก brief** ตัดสินโครง scenario: Q-document → D1-D6 ครบ (ปริมาณ/state machine/QC/อ้างอิง/ปลายทาง/STD) · master → D2+D4 เป็นหลัก · P-planner → capacity/overlap/lock · J-dashboard → data freshness/filter/drill
- **Declarations signals** — ต้องเขียน §12 "สัญญาณประกาศ" ให้ S1.8 อ่าน: action อนุมัติ (DOA) · transition ที่ใครต้องรู้ (NTF — ไม่นับ doa_*) · ผลเงิน/ข้อมูลอ่อนไหว/บัญชี/งบ/decision (CSQ) · เลขรัน/สำเนา (DOCCFG) · เอกสารทางการที่ต้องพิมพ์/ส่ง (PDF DOC → thai-doc-pdf-generator) — เทียบกับ chip ใน brief · ต่าง = เขียน `DIVERGENCE:` ไว้ท้ายตาราง
- **Baseline ห้าม re-implement**: ทุก scenario ที่แตะ อนุมัติ/แจ้งเตือน/เลขเอกสาร/สิทธิ์/งาน OP ให้เขียนเป็น "เรียก <engine>" ไม่ใช่ออกแบบใหม่
- ERP standard research: ทำ **quick** (≤3 search) เฉพาะ archetype Q หรือ feature ที่ทีมไม่เคยทำ — master ง่าย ๆ ข้าม (S1.5 ของเลนจะเสริมอีกชั้น)
- Output เพิ่ม: บรรทัด `archetype_confirmed:` (ยืนยัน/เปลี่ยนจาก brief พร้อมเหตุ) ในหัว PREBRIEF · html-generator-v9 อ่านตัวนี้
- Gate STEP 5 เดิมต้องผ่านเหมือน manual — ตกแล้ววนแก้เองได้ 2 รอบ

## Process

### STEP 0 — Intake Gate: รับพันธะจากต้นทางให้ครบก่อนเขียน
สร้าง **ตารางพันธะ (Obligations)** ก่อนเริ่ม — ไล่จากต้นทางทั้งหมด:
1. ทุก **เส้นเข้า/ออก** ของ feature ใน Central Plan/PB → 1 แถว
2. ทุก **LOCK / Global Contract / Handoff contract** ที่แตะ feature → 1 แถว
3. ทุก **สถานะ/enum ร่วม** ใน Contract Slice → 1 แถว
4. ทุก **W-note / หมายเหตุพิเศษ** ในแผน (เช่น "หนักสุด 12 rules") → 1 แถว
กติกา: ทุกแถวต้องถูก **อ้างกลับ** จากอย่างน้อย 1 จุดใน PREBRIEF (§ไหน) — จบงานแล้วมีแถว
orphan = ยังไม่ครบ ห้ามส่ง · ต้นทางขาด/ขัดกัน = OQ ห้ามแก้เอง

### STEP 1 — Scenario Derivation: ไล่ scenario แบบบังคับครบ (หัวใจของ skill)
ห้ามนั่งนึกเอง — ต้อง derive จาก 6 แหล่งนี้ **ทีละแหล่ง** แล้วรวม dedupe:

| แหล่ง | วิธี derive | ตัวอย่าง (GRN) |
|---|---|---|
| D1 · ปริมาณ/จำนวน | ทุกช่องตัวเลขเทียบเอกสารอ้างอิง: ครบ / ขาด / เกิน / ศูนย์ | รับครบตาม PO · รับบางส่วน (PO ค้างรับ) · รับเกิน (tolerance?) |
| D2 · State machine | ทุก transition = อย่างน้อย 1 scenario + ทางที่ถูกปฏิเสธ | draft→posted · posted→cancelled · ยกเลิกหลัง post ได้ไหม |
| D3 · คุณภาพ/เงื่อนไขรับ | จุดตรวจ/อนุมัติทุกจุด: ผ่าน / ไม่ผ่าน / ผ่านบางส่วน | QC ผ่าน · QC ไม่ผ่านทั้งใบ (→RTV) · ไม่ผ่านบาง line + เหตุผล+disposition |
| D4 · เอกสารอ้างอิง (เส้นเข้า) | ต้นทางอยู่สถานะต่าง ๆ: ปกติ / ถูกยกเลิก / ถูกแก้ / ไม่มี | PO ถูกยกเลิกก่อนรับ · รับโดยไม่มี PO (อนุญาตไหม?) |
| D5 · ผลกระทบปลายทาง (เส้นออก) | ทุกเส้นออก: เกิดอะไรที่ปลายทางเมื่อ scenario นี้จบ | post แล้ว stock ขยับ · PO เปลี่ยนเป็น "รับครบ" · ตั้ง GR/IR |
| D6 · ERP standard [STD] | research: มาตรฐานมี scenario อะไรที่ D1-D5 ยังไม่มี | reversal/return หลัง post · รับข้าม UoM · batch/lot |

ทุก scenario ได้รหัส `S-XX` + ประเภท (Happy/Alt/Exception) + **ข้อมูลที่ scenario นั้นต้องมี**
(นี่คือคำตอบของ "QC ไม่ผ่านต้องมีข้อมูลอะไรบ้าง" — เหตุผล, จำนวน reject, disposition, ผู้ตรวจ)

### STEP 2 — เขียน PREBRIEF ตาม `references/PREBRIEF_TEMPLATE.md` (12 sections)
ลำดับ: Obligations → Scenario → Data (header/line/ทุก field) → BR → State → Actions →
Data behaviour → Mock Data Spec → Edges → Coverage Matrix → OQ/[AI-DRAFT]
- feature ประเภทเอกสาร: **ต้องมี Header/Line data dict** (ตาม B2 grid ของ v7) + ช่องปริมาณ
  ครบวงจร (สั่ง/รับแล้วสะสม/ครั้งนี้/คงเหลือ) + computed fields
- ทุกข้อระบุที่มา **[แผน] / [มติ] / [AI-DRAFT]** (+[STD]) — ห้ามเนียน

### STEP 3 — Coverage Matrix (ledger กันตกหล่น — ใน PREBRIEF §11)
ตารางไขว้: ทุก `S-XX` ↔ BR ที่เกี่ยว ↔ transition ที่ใช้ ↔ หน้าจอ/field ↔ FN ใน checklist
Gate อัตโนมัติจาก matrix:
- ทุก BR ปรากฏใน ≥1 scenario · ทุก transition ปรากฏใน ≥1 scenario
- ทุก scenario มีหน้าจอ/ปุ่มรองรับ (ไม่มี scenario ลอยที่ UI ทำไม่ได้)
- ทุกพันธะจาก STEP 0 ถูกอ้าง

### STEP 4 — ออก FUNCTION_CHECKLIST_[F-code].md (ไฟล์ที่ 2)
แปลง PREBRIEF เป็น checklist แบน ๆ ที่ทีมเปิดเช็คตามได้ใน 5 นาที ตาม
`references/FUNCTION_CHECKLIST_TEMPLATE.md`:
- `FN-XX` ต่อความสามารถ 1 ข้อ ("สร้าง GRN จาก PO ที่ค้างรับได้", "บันทึกรับบางส่วนแล้ว PO
  แสดงยอดค้างถูกต้อง", "QC ไม่ผ่านต้องบังคับกรอกเหตุผล+จำนวน") — ภาษาติ๊กได้ ไม่ใช่ภาษา spec
- จัดกลุ่มตามหมวด + คอลัมน์ trace กลับ (S-XX/BR-XX) + ช่องติ๊ก 3 ด่าน: `WF` (wireframe) /
  `DEV` / `QA` — ไฟล์เดียวใช้ทั้ง chain
- จำนวน FN ต้อง cover ทุก scenario + ทุก action หลัก — matrix ใน STEP 3 คือตัวพิสูจน์
- **เขียนให้ parser อ่านได้** (md คือ source of truth ของ HTML ใน STEP 4.5): หมวด = `## หมวด N · ชื่อ`,
  หัวตาราง `| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |`, แถว `| FN-XX | ... |`, section
  สุดท้าย `## สิ่งที่ไม่รองรับ` เป็น bullet `- ข้อความ — [มติ/OQ]` — ห้ามเปลี่ยนโครง

### STEP 4.5 — ออก FUNCTION_CHECKLIST_[F-code].html (ไฟล์ที่ 3 — checklist ติ๊กได้ ส่งผลได้)
md เปิดอ่านได้แต่ **ติ๊กแล้วส่งกลับไม่ได้** — ไฟล์นี้คือ md เดิมในร่าง HTML ให้คนเปิดใน browser
กดติ๊ก แล้วส่งผลกลับมาได้จริง (shell เดียวกับเอกสารทดสอบของ qa-friendly-html-generator แต่
**ไม่มีภาพแคป/ไม่มี step** — เป็น checklist ล้วน):
```
python3 scripts/build_checklist_html.py FUNCTION_CHECKLIST_[F-code].md
→ FUNCTION_CHECKLIST_[F-code].html ข้าง ๆ md  (parse md → ฉีด PAYLOAD ลง references/FUNCTION_CHECKLIST_HTML_TEMPLATE.html)
```
- **1 MD FN = 1 HTML FN · หมวดเดิม · ลำดับเดิม · id เดิม** — script ห้ามตัด/รวม/แต่งข้อความ (Pipeline
  Mode เดียวกับ qa-friendly R12) · แก้ข้อความ = แก้ที่ md แล้ว build ใหม่ ห้ามแก้ใน HTML
- 3 ด่าน = 3 คนที่เปิดไฟล์เดียวกันคนละช่วง: **WF** = BA/UX ที่รีวิว wireframe-prototype (คนแรกที่ใช้
  checklist — เช็คว่า wireframe มีทุก FN) · **DEV** = ผู้พัฒนาตอนทำจริง · **QA** = ผู้ทดสอบ
- ในไฟล์: sidebar เลือก **ด่านที่กำลังเช็ค (WF/DEV/QA)** + progress ต่อด่าน + หมวด · ทุก FN มี
  ปุ่ม ✓/✗/— ต่อด่าน + ช่องหมายเหตุ · filter "ยังไม่เช็ค/ไม่ผ่าน" · ปุ่ม "ผ่านทั้งหมวด (ด่านนี้)" ·
  หมวด "สิ่งที่ไม่รองรับ" แสดงเป็นหน้าแยก (อ่านอย่างเดียว) · ผลบันทึก localStorage อัตโนมัติ
- **ส่งผล**: ปุ่ม "ส่งผล / พิมพ์รายงาน" → เอกสาร A4 สรุปต่อด่าน + ตาราง FN ทุกข้อ (3 ด่าน+หมายเหตุ)
  + ช่องผู้เช็ค → พิมพ์ / ดาวน์โหลด PDF / **ดาวน์โหลด JSON** (`CHECKLIST_[F]_result.json` —
  โครง `{feature_id, lanes[], items[{id,result{wf,dev,qa},note}]}` ให้ qc-coverage-checker หรือ
  คนรวมผลอ่านต่อได้) / **คัดลอกสรุปส่งแชท** (ข้อความสั้น: ผ่าน x/y · รายการที่ไม่ผ่าน · ผู้เช็ค)
- **ส่งต่อข้ามเครื่อง/ข้ามทีม**: ผลบันทึกใน localStorage ของ browser เครื่องนั้น (ปิดแล้วเปิดใหม่ยังอยู่
  ตราบที่ไฟล์ path เดิม + FN id เดิม) แต่ **ไม่ข้ามเครื่องเอง** → คนแรก "ดาวน์โหลดผล (JSON)" แนบไป
  กับ HTML · ทีมถัดไปเปิด HTML → "นำเข้าผล (JSON)" → ผลด่านเดิมเข้ามา (ทับเฉพาะด่านที่ไฟล์มีผล ด่านอื่น
  ในเครื่องคงเดิม · หมายเหตุต่อท้าย) → ติ๊กด่านตัวเองต่อ → ดาวน์โหลด JSON ใหม่ส่งต่อ — ไฟล์ JSON
  ล่าสุดคือผลรวมทุกด่าน
- ด่านปรับได้จากหัวตาราง md (เช่น เพิ่ม `UAT`) — default WF/DEV/QA · CI Warm Light ชุดเดียวกับ
  html-generator-v9/qa-friendly (ห้ามแก้ token ในไฟล์นี้เอง)
- script `[WARN]` FN ไม่มี trace / ไม่มี section ไม่รองรับ · `[BLOCK]` FN id ซ้ำ หรือไม่พบ FN — แก้ md
  แล้ว build ใหม่ · ตรวจ HTML ที่ได้ด้วย `node --check` (ดึง `<script>` ออก) ก่อนส่ง

### STEP 5 — Gate ก่อนส่ง
- [ ] Obligations table: 0 orphan
- [ ] Scenario: ทุกแหล่ง D1-D6 ถูกไล่แล้ว (ระบุในเอกสารว่าแหล่งไหนให้ scenario อะไร แหล่งไหน N/A เพราะอะไร)
- [ ] ทุก field มี ชนิด+บังคับ+ที่มา — ไม่มี TBD ลอย (ไม่รู้ = OQ + เจ้าภาพ)
- [ ] ทุกสถานะมีทางเข้า-ออก · ทุก transition มีคนกด
- [ ] Coverage Matrix ผ่าน 3 เงื่อนไข STEP 3
- [ ] FUNCTION_CHECKLIST.md: ทุก S-XX มี ≥1 FN · ทุก FN trace กลับได้ · โครง md ตาม parser
- [ ] FUNCTION_CHECKLIST.html: build จาก md ผ่าน (0 BLOCK) · จำนวน FN/หมวด/ไม่รองรับใน HTML = md ทุกตัว
  · `node --check` ผ่าน · เปิดแล้วติ๊ก/สลับด่าน/ส่งผล ทำงาน
- [ ] `rm -f` → `cp` → `present_files` + md5 ทั้ง 3 ไฟล์ (PREBRIEF.md · CHECKLIST.md · CHECKLIST.html)

## Rules

1. Central Plan + Contract Slice = source of truth ต้นทาง — PREBRIEF เป็น source of truth
   **ระดับ feature** ที่ขยายจากมัน ขัดกันเมื่อไหร่ = OQ
2. ภาษา business ไทยล้วน — ห้าม API path/SQL/JSON schema
3. ระดับความลึก: dev อ่านแล้วพัฒนาได้โดยไม่ต้องเดา field/rule/scenario เพิ่ม — ถ้ายังต้องเดา
   แปลว่า PREBRIEF ยังไม่จบ
4. สืบทอด pattern กลาง: DOA pre-placeholder · soft reference LD-4C-02 · soft archive ·
   audit append-only
5. 1 feature = 1 PREBRIEF + 1 CHECKLIST (.md + .html คู่กันเสมอ) — อย่ารวมหลาย feature ·
   md = source of truth ของ checklist · html = ร่างติ๊ก/ส่งผล ต้อง build ใหม่ทุกครั้งที่ md เปลี่ยน
6. Scenario ที่ตัดสินใจ "ไม่รองรับ" (เช่น ไม่ให้รับเกิน) ต้องเขียนไว้ชัดใน §Scenario ว่า
   **ไม่รองรับ + เหตุผล/มติ** — การไม่พูดถึงถือว่าตกหล่น ไม่ใช่การตัด scope


**v1.3 (2026-08-25):** Lane Mode (no-ask) · input LANE_BRIEF v2 · archetype_confirmed · §12 declaration signals (5 ท่อ) · graph optional
