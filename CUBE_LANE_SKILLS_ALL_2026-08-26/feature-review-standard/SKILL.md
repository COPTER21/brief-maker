---
name: feature-review-standard
description: >
  Review feature ของ CUBE ERP เทียบกับ ERP Standard ระดับโลก (SAP, Odoo, D365, NetSuite, ERPNext)
  ด้วย real-time web search — สรุปเป็น Review Report + Baseline Checklist + Enhancement Brief
  ใช้เมื่อ user พูดถึง "review feature", "ตรวจ feature", "เทียบ standard", "feature ครบไหม",
  "ขาดอะไร", "gap analysis", "ERP standard", "feature-review-standard", "ตรวจ ERP",
  "review กับ SAP", "เทียบกับ Odoo", "feature ดีพอไหม", "สแกน feature",
  "เช็ค feature", "ตรวจความครบถ้วน", "ตรวจตาม standard"
  ใช้ Skill นี้ทุกครั้งที่ user ต้องการ review feature ของ CUBE ERP ว่าครบถ้วนตาม ERP standard หรือไม่
---

# Feature Review Standard

Review feature ของ CUBE ERP แบบ feature-by-feature เทียบกับ ERP ระดับโลก
ใช้ real-time web search ดึง standard จาก SAP, Odoo, D365, NetSuite, ERPNext
แล้วสรุปผลเป็น **3 ส่วนชัดเจน** พร้อมเอกสาร 3 ชิ้นส่งต่อ enhancement-ticket-pack-generator

## ตำแหน่งใน Pipeline

```
Feature ที่ทำเสร็จแล้ว (screenshots + context)
    ↓
★ Feature Review Standard ← Skill นี้
    ↓
Output 3 ส่วน (รวมใน 3 ไฟล์):
    ├── PART A: UI Issues          → REVIEW_[module]_[feature].docx  (Section 3)
    ├── PART B: Function ที่ต้องเพิ่ม → REVIEW_[module]_[feature].docx  (Section 4)
    │                               + BASELINE_[module]_[feature].xlsx
    └── PART C: ภาพรวมที่ต้องปรับ    → REVIEW_[module]_[feature].docx  (Section 5–6)
                                     + ENHANCE_BRIEF_[module]_[feature].md
    ↓
แต่ละ issue → enhancement-ticket-pack-generator
```

---

## 🧭 Baseline Mode (lane S0.5 — ก่อน PREBRIEF · 2026-08-25)

ใช้เมื่อยังไม่มี PREBRIEF — เป้าหมาย: "feature นี้ในโลก ERP มาตรฐานทำอะไรได้บ้าง แล้ว CUBE ควรเอาอะไร" **ก่อน** ใครจะเขียน scenario
- **Input:** LANE_BRIEF (ชื่อ feature · module · scope note · archetype ชั่วคราว) + cube-master-knowledge current-state §2 baseline
- **Research 3 แหล่งบังคับ:** Odoo (module/app ที่ตรง) · Microsoft Dynamics 365 (Customer Insights/F&O/BC ตามโดเมน) · SAP (S/4HANA หรือ Customer Data Cloud/SuccessFactors ตามโดเมน) — web search ≤6 ครั้ง (2 ต่อค่าย) + ความรู้ที่มี · ระบุแหล่งต่อข้อ
- **Output 1 ไฟล์ `STANDARD_BASELINE.md`:**
  ```
  ## 1. Capability matrix (แถว = ความสามารถ · คอลัมน์ = Odoo | D365 | SAP | CUBE-fit)
  | # | Capability | Odoo | D365 | SAP | CUBE-fit: MUST/SHOULD/NICE/SKIP | เหตุผล/มติที่อ้าง |
  ## 2. Lifecycle มาตรฐาน (state machine + actor + เอกสารที่ออก)   ← PREBRIEF ต้องครอบทุก state ที่ MUST
  ## 3. Archetype ที่ควรใช้ (จาก lifecycle: master / Q-document / hybrid / planner …) + surface ที่ต้องมี (สร้าง · ส่ง · เซ็น · PDF · เตือน · รายงาน)
  ## 4. Declarations ที่ standard บ่งชี้ (doa/ntf/csq/doccfg/pdfdoc) + เหตุผล
  ## 5. สิ่งที่ scope note ตัดแต่ standard ถือว่า MUST → ยก OQ ให้คนเคาะ (ห้ามตัดเงียบ)
  ```
- กติกา: MUST ≥ ที่ทั้ง 3 ค่ายมีเหมือนกัน · CUBE-fit ต้องอ้าง baseline (ไม่ทำซ้ำ DOA/NOTIFY/DOCCFG) · ห้ามถาม · ≤ 25 แถว matrix
- ต่างจาก Quick Mode (S1.5): Baseline = ตั้งโจทย์ก่อนเขียน · Quick = ตรวจ gap หลังเขียน — lane v2.2 ใช้ทั้งคู่

## ⚡ Quick Mode (lane S1.5 — ตั้งแต่ 2026-08-25)

ใช้เมื่อ input เป็น **PREBRIEF** (ไม่มี screenshot/HTML) จาก feature-lane-runner v2 — เป้าหมายคือ "gap list ที่ merge เข้า PREBRIEF ได้ก่อนวาด" ไม่ใช่ review report เต็ม
- **Input:** `01_PREBRIEF.md` + `01_FUNCTION_CHECKLIST.md` + archetype (จาก LANE_BRIEF) · ห้ามถาม
- **Research:** ≤3 web search (SAP / Odoo / D365 ของ feature type นี้) · เฉพาะ scenario/rule/field ระดับ business — ไม่วิจารณ์ UI (ยังไม่มี)
- **Output 1 ไฟล์:** `02_STANDARD_GAP.md` =
  ```
  | # | Gap (standard มี · PREBRIEF ไม่มี) | ที่มา (ERP) | ชนิด: scenario / rule / field / edge | ข้อเสนอ: ADD → S-XX ใหม่ / FN-XX ใหม่ · หรือ DEFER → "ไม่รองรับ" + [OQ] | สำคัญ: MUST/SHOULD/NICE |
  ```
  + บรรทัดสรุป `merge: N scenario · M FN · K rule` ที่ runner จะ patch เข้า PREBRIEF (tag `[STD]`) — MUST = merge อัตโนมัติ · SHOULD = merge + `[AI-DRAFT]` · NICE = ลง "ไม่รองรับ" พร้อม [OQ]
- ข้ามได้เมื่อ LANE_BRIEF ระบุ archetype = master ง่าย ๆ และ feature type เคยทำแล้ว (catalog มี feature ใกล้เคียง done) → เขียน `02_STANDARD_GAP.md` ว่า `SKIPPED: reason`
- ไม่ออก REVIEW.docx / BASELINE.xlsx / ENHANCE_BRIEF ใน quick mode

## Input (Full Mode)

| Input | Required | คำอธิบาย |
|-------|----------|----------|
| Screenshots 4–8 ภาพ | ✅ บังคับ | ภาพรวม feature: List view, Create/Edit, View detail, Modal, Config ฯลฯ |
| Context text | ✅ บังคับ | อธิบายสั้นว่า feature ทำอะไร ใครใช้ flow หลักเป็นยังไง |
| Module name | ✅ บังคับ | ชื่อ Module เช่น Purchase, Sales, Warehouse, HR |
| Feature name | ✅ บังคับ | ชื่อ Feature เช่น Pick, Sales Order, PO, Employee Management |
| FRD (.md) | ⭕ Optional | ถ้ามี = เทียบ spec ได้ตรง / ถ้าไม่มี = ใช้ ERP standard เป็น baseline |

---

## Output — 3 ส่วน / 3 ไฟล์

### PART A — UI Issues (จากภาพที่แนบ)

> **วิธี deliver:** annotate ภาพจริง (วงแดง + label) + สรุปเป็น text ควบคู่กัน

**A1: Annotated Screenshots**

สำหรับแต่ละภาพที่รับมา ให้:
- วิเคราะห์ภาพและระบุจุดที่มีปัญหาหรือควรปรับ
- สร้าง HTML annotation overlay (วงแดง + กล่อง label ลอยอยู่บนภาพ) พร้อม Issue ID (UI-001, UI-002…)
- ถ้า annotate ภาพไม่ได้ (ภาพ format ไม่รองรับ) → พิมพ์บอกแทนพร้อม reference ว่าอยู่ตรงไหนของภาพ

**A2: UI Issue Table**

| Issue ID | ภาพอ้างอิง | Zone/Component | ปัญหาที่เห็น | ERP Standard ที่ถูกต้อง | Priority |
|----------|------------|----------------|--------------|--------------------------|----------|
| UI-001 | screenshot_1 | [Zone/Component ที่มีปัญหา] | [อธิบายปัญหา] | [ระบบอื่นทำยังไง] | Polish / Minor / Major |

หมวด UI Issues แบ่งเป็น:
- **Layout & Structure** — จัดวาง zone ผิด, ขาด section, content ล้น
- **Component** — ใช้ component ผิดประเภท, ขาด state, label ไม่ถูกต้อง
- **Status & State** — Badge สี status ไม่ครบ, ไม่มี empty state, ไม่มี loading state
- **Form & Validation** — field ขาด, label ไม่ชัด, ไม่มี hint/placeholder, ขาด validation indicator
- **Action & Flow** — ปุ่มหาย, action ผิด zone, ลำดับขั้นตอนสับสน

---

### PART B — Function ที่ต้องเพิ่ม

> **หลักการ:** output ส่วนนี้คือ **"เมนูให้ BA เลือก"** — ระบุว่าต้องเพิ่ม function อะไร ทำอะไร ทำไมถึงต้องมี
> ไม่ต้องลง spec ระดับ Dev — รายละเอียดจริงๆ จะเกิดใน enhancement-ticket-pack หรือ frd-generator-40 หลังจาก BA เลือกแล้ว

**B1: Function List**

| FN ID | Function Name | ประเภท | ทำอะไร (1 บรรทัด) | ทำไมต้องมี | ERP Reference | Priority |
|-------|---------------|--------|-------------------|------------|---------------|----------|
| FN-NEW-001 | [ชื่อ function] | New / Enhance / Config | [สรุปสั้นว่า function นี้ทำอะไร] | [business value — ถ้าไม่มีจะเกิดอะไร] | SAP/Odoo/D365 | Critical/Major/Minor |

**ประเภทของ Function:**
- **New** — ยังไม่มีใน CUBE เลย
- **Enhance** — มีแล้วแต่ logic ไม่ครบ
- **Config** — มีแล้ว แค่ปรับ config / rule

---

### PART C — ภาพรวมที่ต้องปรับ

> **จุดประสงค์:** สรุปให้ PM/BA เห็น "สภาพรวม" ของ feature — ไม่ใช่ list of issues แต่เป็นการประเมิน maturity

**C1: Feature Maturity Assessment**

| มิติ | คะแนน (1–5) | สรุป | Gap หลัก |
|------|-------------|------|----------|
| Functional Completeness | [1–5] | [สรุป] | [gap หลัก] |
| UX/UI Quality | [1–5] | [สรุป] | [gap หลัก] |
| Business Logic Depth | [1–5] | [สรุป] | [gap หลัก] |
| Automation & Efficiency | [1–5] | [สรุป] | [gap หลัก] |
| Reporting & Visibility | [1–5] | [สรุป] | [gap หลัก] |

คะแนน: 1=ไม่มีเลย / 2=มีพื้นฐาน / 3=ใช้งานได้ / 4=ดีกว่าค่าเฉลี่ย / 5=เทียบได้กับ ERP ชั้นนำ

**C2: ERP Gap Summary**

| Check Item | SAP | Odoo | D365 | NetSuite | Standard Level | CUBE Status | Gap |
|------------|-----|------|------|----------|----------------|-------------|-----|
| [item] | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | Must/Should/Nice | ✅/⚠️/❌ | [description] |

**C3: Priority Action Plan**

สรุปสิ่งที่ต้องทำทั้งหมดจาก PART A + B เรียงตาม priority:

| ลำดับ | Action | ที่มา | Priority | Effort | หมายเหตุ |
|-------|--------|-------|----------|--------|----------|
| 1 | [สิ่งที่ต้องทำ] | UI-001 / FN-NEW-001 | Critical | M | [หมายเหตุ] |

**C4: CUBE Advantages**

สิ่งที่ CUBE ทำได้ดีกว่า ERP อื่น หรือเป็น differentiator:
- [advantage 1]

---

## Output Files — 3 ไฟล์

### ไฟล์ 1: REVIEW_[module]_[feature].docx

> อ่าน `/mnt/skills/public/docx/SKILL.md` ก่อนสร้างทุกครั้ง — ใช้ docx-js

**โครงสร้างเอกสาร:**

```
Cover Page
  - Logo placeholder (ถ้ามี) + ชื่อเอกสาร "Feature Review Report"
  - Module / Feature / Version / วันที่ / จัดทำโดย

§1  Feature Summary        (Heading 1 สีน้ำเงินเข้ม #1F3864)
§2  ERP Standard Research  (Heading 1)
§3  UI Issues              (Heading 1) ← PART A
§4  Functions ที่ต้องเพิ่ม  (Heading 1) ← PART B
§5  ภาพรวมที่ต้องปรับ       (Heading 1) ← PART C
§6  Gap vs FRD             (Heading 1, เฉพาะถ้ามี FRD)
```

**Styling rules:**

| Element | Style |
|---------|-------|
| Font | Arial 11pt ทั้งเอกสาร |
| Page size | A4 (11906 × 16838 DXA) margins 1 inch |
| Heading 1 | Bold 14pt สี #1F3864 spacing before 240 after 120 |
| Heading 2 | Bold 12pt สี #2E75B6 spacing before 180 after 90 |
| Heading 3 | Bold 11pt สี #404040 spacing before 120 after 60 |
| Body text | Arial 11pt สี #1A1A1A line spacing 1.15 |
| Table header row | Fill #2E75B6 text สีขาว Bold |
| Table even rows | Fill #EEF4FB |
| Table odd rows | Fill #FFFFFF |
| Priority: Critical | ตัวอักษร Bold สี #C00000 |
| Priority: Major | ตัวอักษร Bold สี #E36C00 |
| Priority: Minor | ตัวอักษร Bold สี #595959 |
| Priority: Polish | ตัวอักษร สี #7F7F7F |
| Score badge | ใส่ใน TableCell shading ตามคะแนน: 1–2=#FFE0E0, 3=#FFF2CC, 4–5=#E2EFDA |

**§1 Feature Summary — layout:**
- ตาราง 2 คอลัมน์ (Label | Value) ไม่มี border ภายนอก
- แถว: Module / Feature / วันที่ review / Reviewer / สถานะปัจจุบัน / Target Users / Use Cases หลัก

**§2 ERP Standard Research — layout:**
- Heading 2 ต่อแต่ละ ERP ที่ search
- Bullet list สรุป capabilities ที่พบ
- URL อ้างอิงเป็น hyperlink สีน้ำเงิน underline

**§3 UI Issues (PART A) — layout:**
- Heading 2: "3.1 สรุป UI Issues" → ตาราง A2 (UI Issue Table) ครบทุก column
- Heading 2: "3.2 รายละเอียดต่อ Issue" → ต่อแต่ละ UI-xxx มี Heading 3 + body text อธิบาย
- ถ้ามี annotated image → แทรก ImageRun ของภาพ annotated ใต้ Issue นั้น (width 100% content)

**§4 Functions ที่ต้องเพิ่ม (PART B) — layout:**
- Heading 2: "4.1 Function Summary" → ตาราง B1 (Function Spec Table)
- Heading 2: "4.2 ERP Reference ต่อ Function" → ต่อแต่ละ FN-NEW-xxx ที่เป็น Critical/Major มี:
  - Heading 3 = "FN-NEW-001: [Function Name]"
  - body text: ทำอะไร + ทำไมต้องมี (2–3 บรรทัด)
  - bullet list: ERP ที่มี feature นี้ทำยังไง (SAP/Odoo/D365 — สั้นๆ)

**§5 ภาพรวมที่ต้องปรับ (PART C) — layout:**
- Heading 2: "5.1 Feature Maturity" → ตาราง C1 พร้อม score badge shading
- Heading 2: "5.2 ERP Gap Summary" → ตาราง C2
- Heading 2: "5.3 Priority Action Plan" → ตาราง C3 เรียงลำดับตาม priority
- Heading 2: "5.4 CUBE Advantages" → bullet list สีเขียว ✅

**กฎเพิ่มเติม:**
- ใส่ Page Break ก่อน Heading 1 ทุกอัน (ยกเว้น §1)
- ใส่ Footer: ชื่อเอกสาร (ซ้าย) + เลขหน้า (ขวา) ทุกหน้า
- ใส่ Header: "CONFIDENTIAL — 2BSimple Internal" (ซ้าย) ทุกหน้า (ยกเว้น Cover)
- ตารางทุกตัว: ใช้ `WidthType.DXA` เสมอ, ใส่ cell margins `{top:80, bottom:80, left:120, right:120}`
- ห้ามใช้ unicode bullet — ใช้ `LevelFormat.BULLET` กับ numbering config

### ไฟล์ 2: BASELINE_[module]_[feature].xlsx

> อ่าน `/mnt/skills/public/xlsx/SKILL.md` ก่อนสร้าง

**Sheet 1: Comparison Matrix** — ERP gap comparison ทั้งหมด (มาจาก PART C2)
**Sheet 2: Research Sources** — URL + วันที่ search + สรุปสั้น ต่อแต่ละ ERP

### ไฟล์ 3: ENHANCE_BRIEF_[module]_[feature].md

สรุปรายการที่ BA เลือกทำได้ — พร้อมส่งต่อ enhancement-ticket-pack-generator หรือ frd-generator-40:

```markdown
# Enhancement Brief — [Module] / [Feature]
วันที่: [วันที่] | Reviewer: [ชื่อ] | Feature Maturity: [N]/5

## PART A: UI ที่ต้องแก้
| UI-ID | ส่วนที่ต้องแก้ | Priority |
|-------|---------------|----------|
| UI-001 | ... | ... |

## PART B: Function ที่ต้องเพิ่ม
| FN ID | Function | ประเภท | ทำอะไร | Priority |
|-------|----------|--------|--------|----------|
| FN-NEW-001 | ... | New | ... | Critical |

## PART C: สรุปภาพรวม
[2–3 บรรทัด — สถานะปัจจุบัน + สิ่งที่สำคัญที่สุดที่ต้องทำ]

## ขั้นตอนถัดไป
- BA เลือก item ที่จะทำ → ส่งเข้า enhancement-ticket-pack-generator ทีละ item
- ถ้าต้องการ FRD formal → ส่งเข้า frd-generator-40 แทน
- Engine register จะเกิดขึ้นใน frd-generator-40 หลัง BA ยืนยันเท่านั้น
```

---

## Process — 4 Phase

### Phase 1: Intake — รับ Input + ถามข้อมูลที่ขาด

**Step 1:** รับ input ทั้งหมด (screenshots, context, FRD)

**Step 2:** ตรวจว่าครบหรือไม่:
- ถ้าไม่มี screenshots → บังคับขอ (ขาดแล้วทำต่อไม่ได้)
- ถ้าไม่มี context → ถาม: "feature นี้ทำอะไร ใครใช้ flow หลักเป็นยังไง"
- ถ้าไม่มี Module/Feature name → ถามให้ชัด
- ถ้าไม่มี FRD → แจ้งว่าจะใช้ ERP standard เป็น baseline แทน

**Step 3:** วิเคราะห์ screenshots ทุกภาพก่อน:
- อ่าน UI — fields, buttons, layout, navigation, status, empty/error states
- จดทุก UI issue ที่เห็นทันที (จะใช้ใน PART A)
- จดว่า feature ทำอะไรได้แล้ว (As-Is)

---

### Phase 2: Research — ค้นหา ERP Standard (Real-time Web Search)

```
Search Round 1 — ภาพรวม feature:
  "SAP [module] [feature] process overview"
  "Odoo [module] [feature] workflow"
  "Dynamics 365 [module] [feature] functionality"
  "NetSuite [module] [feature] features"

Search Round 2 — เจาะลึก field/validation/flow:
  "SAP [feature] mandatory fields configuration"
  "Odoo [feature] validation rules"
  "D365 [feature] business rules best practice"

Search Round 3 — เฉพาะจุดที่พบ gap จาก screenshots:
  "[ERP] [specific gap topic] how to handle"
```

**กฎการ search:**
- ใช้ web_search tool ทุกครั้ง ห้ามใช้ความจำอย่างเดียว
- Search อย่างน้อย 5 queries ต่อ feature
- ใช้ web_fetch อ่านหน้าเต็มถ้า snippet ไม่พอ
- บันทึก source URL ทุกรายการ

**สรุปผล → Baseline Checklist:**
- 3/4+ ระบบมี → Must-have | 2/4 → Should-have | 1/4 → Nice-to-have | CUBE เด่นกว่า → CUBE Advantage

---

### Phase 3: Review — เทียบ CUBE + Interactive Q&A + สร้าง 3 PART

**Step 1: สร้าง PART A — UI Issues**
- ระบุ UI issue แต่ละจุด พร้อม Issue ID (UI-001…)
- วางแผน annotation (วงแดง + label) สำหรับแต่ละภาพ
- จัดกลุ่มตาม category: Layout / Component / Status / Form / Action

**Step 2: สร้าง PART B — Function ที่ต้องเพิ่ม**
- แต่ละ Must-have/Should-have ที่ CUBE ขาด → สร้าง function spec พร้อม business logic ครบ
- ระบุ engine type เบื้องต้น (T1 Transaction / Validation / Workflow / Approval / Notification ฯลฯ)

**Step 3: Interactive Q&A**
- ถามเฉพาะประเด็น Critical/Major — รวมในชุดเดียว ไม่เกิน 5 คำถาม
- ถ้าตอบ "ยังไม่ได้ทำ" → ยืนยันเป็น gap

**Step 4: สร้าง PART C — ภาพรวม**
- ประเมิน Maturity Score ทุก 5 มิติ
- รวม issues จาก PART A + B เป็น Priority Action Plan
- ระบุ CUBE Advantages

---

### Phase 4: Generate — สร้าง Output 3 ไฟล์

**Step 1:** สร้าง REVIEW_[module]_[feature].docx
- อ่าน `/mnt/skills/public/docx/SKILL.md` ก่อนทุกครั้ง
- ใช้ docx-js สร้างไฟล์ .js แล้วรัน node → output .docx
- ใช้ styling ตาม "Output Files > ไฟล์ 1" ทุกข้อ — font Arial, page A4, header/footer ทุกหน้า
- เรียงตาม 6 sections พร้อม Page Break ก่อน Heading 1 ทุกอัน (ยกเว้น §1)
- ตาราง: header row fill #2E75B6 / even row fill #EEF4FB / WidthType.DXA ทุกตาราง
- ถ้ามี annotated image → แทรก ImageRun ใน §3 ใต้ Issue นั้น

**Step 2:** สร้าง BASELINE_[module]_[feature].xlsx
- อ่าน `/mnt/skills/public/xlsx/SKILL.md` ก่อน

**Step 3:** สร้าง ENHANCE_BRIEF_[module]_[feature].md

**Step 4:** บันทึก 3 ไฟล์ → `/mnt/user-data/outputs/` → present_files

แสดงสรุปใน chat:

```
📋 Feature Review — [Module] / [Feature]

ERP Standard Research: SAP ✓ | Odoo ✓ | D365 ✓ | NetSuite ✓

━━━ PART A: UI Issues ━━━
  🔴 Critical: [N] | 🟠 Major: [N] | 🟡 Minor: [N] | 🎨 Polish: [N]
  Annotated screenshots: [N] ภาพ

━━━ PART B: Functions ที่ต้องเพิ่ม ━━━
  🔴 Critical: [N] | 🟠 Major: [N] | 🟡 Minor: [N]

━━━ PART C: ภาพรวม ━━━
  Feature Maturity: [N]/5
  ⭐ CUBE Advantages: [N] items

สร้างเอกสาร 3 ไฟล์:
  1. Review Report (.docx) — ครบทั้ง 3 ส่วน
  2. Baseline Checklist (.xlsx) — Comparison Matrix + Sources
  3. Enhancement Brief (.md) — พร้อมส่งต่อ ticket-pack
```

---

## Decision Rules

| สถานการณ์ | Action | เหตุผล |
|-----------|--------|--------|
| User ส่ง screenshots + context ครบ | เข้า Phase 2 Research ทันที | ข้อมูลพอเริ่ม review |
| User ส่ง screenshots แต่ไม่บอก context | ถามว่า feature ทำอะไร ใครใช้ | ต้องรู้ scope ก่อน research |
| User ไม่ส่ง screenshots | บังคับขอ — ขาดแล้วทำ PART A ไม่ได้ | ต้องเห็น UI จริงถึงจะ annotate ได้ |
| มี FRD | เพิ่ม §6 Gap vs FRD ใน REVIEW report | เทียบ spec กับ implementation |
| ไม่มี FRD | ใช้ ERP standard เป็น baseline 100% | ยังคง review ได้แม้ไม่มี spec |
| UI ในภาพชัดเจน annotate ได้ | สร้าง HTML annotation + UI table ควบคู่ | ทั้ง 2 อย่างตาม spec |
| UI ในภาพไม่ชัด / resolution ต่ำ | พิมพ์บอกแทน พร้อม reference zone | ไม่ annotate ภาพที่ไม่ชัด |
| Function ใหม่ที่แนะนำ ควร map เข้า engine | ระบุ engine type เบื้องต้นใน PART B3 | ช่วย frd-generator-40 ตอนเขียน §10 |
| Function ใหม่ยังไม่แน่ใจ engine | flag "TBD — ให้ frd-generator-40 กำหนด" | ไม่ force mapping ที่ไม่แน่ใจ |
| Feature search ไม่พบ standard ชัด | ขยาย keyword + ดู industry best practice | บาง feature อาจเป็น niche |
| CUBE มี feature ที่ระบบอื่นไม่มี | ระบุเป็น CUBE Advantage ใน PART C4 | ไม่ใช่ทุกอย่างที่ CUBE ขาด |
| Issue เกี่ยวกับ UI polish | จัดใน PART A หมวด Polish | แยก UI issue กับ function gap ชัดเจน |
| Issue เกี่ยวกับ logic ที่หายไป | จัดใน PART B เป็น function spec | logic = function ต้องระบุให้ dev ได้เลย |
| User ถาม "ทำต่อยังไง" | แนะนำเอา Enhancement Brief เข้า enhancement-ticket-pack-generator | pipeline ต่อเนื่อง |
| Feature มี sub-features เยอะมาก | แยก review เป็นรอบ | ไม่ให้ report ยาวเกินไป |

---

## ERP Reference Systems

| ระบบ | จุดเด่นที่ช่วย review | ใช้เมื่อ |
|------|----------------------|---------|
| **SAP S/4HANA** | Enterprise-grade, process ครบสุด, configuration ลึก | ดู "gold standard" ของ feature |
| **Odoo** | Open-source, modular, UI ใกล้เคียง CUBE | ดู practical implementation |
| **Microsoft Dynamics 365** | Cloud-native, integration ดี, UX modern | ดู UX best practice |
| **NetSuite** | SaaS ERP, mid-market, workflow automation | ดู automation patterns |
| **ERPNext** | Open-source, simple, lean | ดู minimum viable feature |

---

## Notes

- Skill นี้ใช้ web_search ทุกครั้ง — ข้อมูลจะ up-to-date เสมอ
- ระวังเรื่อง copyright — paraphrase เสมอ ห้าม quote ยาว
- ถ้า search ไม่พบข้อมูลชัดเจนของ ERP บางตัว → ข้ามไป ไม่ fabricate
- **PART A** = สิ่งที่เห็นจากภาพ (UI layer) / **PART B** = function ที่ขาด (BA เลือกทำ) / **PART C** = ภาพรวม maturity
- Output ทั้งหมดคือ **"เมนูให้ BA เลือก"** — ไม่ใช่ spec Dev ยังใช้งานไม่ได้โดยตรง
- หลัง BA เลือก item แล้ว → ส่งเข้า enhancement-ticket-pack-generator (ได้ชุดงาน Dev) หรือ frd-generator-40 (ได้ FRD formal)
- Engine register เกิดใน frd-generator-40 เท่านั้น — review-standard ไม่ touch engine-registry.md
- ถ้า user ต้องการ review หลาย features พร้อมกัน → แนะนำทำทีละ feature เพื่อคุณภาพ
