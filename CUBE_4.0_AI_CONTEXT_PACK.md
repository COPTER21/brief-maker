# CUBE 4.0 — AI Context Pack
### เอกสาร context กลางสำหรับ "AI ตัวอื่น" ที่มาช่วยผลิตฟีเจอร์ให้ CUBE 4.0

```yaml
doc: CUBE 4.0 AI Context Pack
owner: 2BSimple Co., Ltd.
version: 1.1.0
created: 2026-07-29
updated: 2026-07-29  # merge Central Plan (Trade Core Feature Map v4.0.0)
audience: AI assistant / BA / Dev ที่ไม่ได้อยู่ในแชทหลัก
source_of_truth:
  - Central_Plan/ (workflow_graph.json v4.0.0 · GOLDEN_RULES.md · DEVELOPMENT_PLAN.md · BUILD_ORDER.md) ⭐
  - CUBE_4.0_PROJECT_INSTRUCTIONS.md (project files)
  - CUBE_KNOWLEDGE_SNAPSHOT.md (project files)
  - FEATURE_REGISTRY.md (project files)
  - skill: cube-master-knowledge → knowledge/04_skills/workflow-master-wf01-06.md (version pin ⭐)
  - skill: html-generator-v6 (CI + iron rules)
```

---

## 0. อ่านก่อน — วิธีใช้เอกสารนี้

เอกสารนี้คือ **context ตั้งต้น** ให้ AI ตัวอื่นทำงานให้ CUBE 4.0 ได้ทิศทางเดียวกับทีมหลัก
อ่านจบแล้วต้องตอบได้ 5 ข้อ:

1. CUBE 4.0 คืออะไร ประกอบด้วยอะไร
2. คำศัพท์กลางของ business (VS/VC/Path/CL/SOP/SOW) แปลว่าอะไร ใช้ตัดสินยังไง
3. เราออกแบบ feature ด้วยวิธีไหน (HTML-first / Reverse Mode) และมี gate อะไรบ้าง
4. **Central Plan** คืออะไร ใช้ยังไง (กฎ XR/GR ที่บังคับทุก feature)
5. P2P / S2C ต้องดูข้อมูลอะไร ออกแบบยังไง
6. กติกาที่ห้ามละเมิด (CI, DOA, data pattern, scope lock)

**ก่อนแตะ feature ใด ๆ ในสายการค้า (Purchase · Inventory · Sales · Accounting · Finance):**
ต้องอ่าน **PART D — Central Plan** ก่อนเสมอ · `GOLDEN_RULES.md` คือกฎที่บังคับใช้จริง ไม่ใช่คำแนะนำ

**กติกาข้อแรกที่สุด:** เอกสารนี้เป็น *ภาพรวมและปรัชญา* — ค่าที่ต้อง "เป๊ะ" (เวอร์ชัน skill, สี, ขนาด drawer, กฎ audit)
ให้อ่านจาก **version pin ใน `workflow-master-wf01-06.md`** และ **skill ที่ pin ไว้** เสมอ **ห้ามจำเวอร์ชันเอง**
> บทเรียนจริง 2026-07: 7 skill จำเวอร์ชันกันเอง → v4/v5/-25 ปนกัน → CI ชนกัน → gate BLOCK ทั้งเลน

**ภาษา:** ทีมสื่อสารภาษาไทย เอกสาร/UI ภาษาไทยเป็นหลัก ตอบไทย กระชับ ตรงประเด็น ไม่ฟอร์แมตเกินจำเป็น
**บัญชีทีม:** shared account — ทีมคือ Bird (BE/Dev Manager), Strike (Lead Dev/Project Owner), Chin (UI), BA/QA
ห้ามสมมติชื่อบุคคลเอง

---

# PART A — CUBE 4.0 คืออะไร

## A1. นิยาม

**CUBE 4.0** = แพลตฟอร์ม ERP ของ 2BSimple แบบ **AI-native, federated multi-tenant**
แต่ละบริษัทลูกค้า = ERP แยกจริง (data silo) ผ่าน **PostgreSQL Row-Level Security (RLS)**
เชื่อมกันด้วย **Identity Hub** (global user + tenant switcher + SSO)

Stack: **React + Vite (FE) · Go (BE) · PostgreSQL (DB)**

## A2. Deployment ปัจจุบัน — ERP เดียว + 2 site แยก

> ⚠️ โครงสร้างเปลี่ยนแล้ว — เดิมแยกหลาย site ตอนนี้ **HR / Agent / Report / Policy Center ยุบรวมเข้า Core**
> กลายเป็น "area" (พื้นที่งาน) ภายใน ERP เดียว

### 🟦 Core Cube — `core.2bsimple.com` (ตัวที่ขาย/ติดตั้งให้ลูกค้า)

| Area | บทบาท |
|---|---|
| **Operation (ERP core)** | operation หลัก — Sales / Marketing / Purchase / Inventory / Accounting / Finance / Budget / CRM / Asset / Org / Operation Process |
| **HR** | เรื่องคน — Employee Lifecycle / Performance / Payroll / Time / Org |
| **Report** | read layer ดึงจากทุก area มาสรุป |
| **Policy Center** | governance กลาง — DOA → User Roles → PDPA → Data Classification → Security → Audit (คร่อมทุก area) |
| **Agent** | AI Agent orchestration + launcher |
| **QA** | Feature Test / Ticket |

### site ที่ยังแยก (เฉพาะเรา — ลูกค้าไม่ได้ install)

| Site | URL | บทบาท |
|---|---|---|
| **Cubic** | cubic4.2bsimple.com | System backbone — Registry กลาง (Platform / Module / Feature / AIR / Engine / API) + Notification + Sandbox + Onboarding |
| **Knowledge (+CMS)** | knowledge.2bsimple.com · cms-knowledge.2bsimple.com | Content Hub สาธารณะ + หลังบ้าน (Article / Pillar / Author / Scraping) |

```
        ┌──── Portal กลาง (อนาคต) ────┐
   ╔═══════════════ Core Cube (ERP เดียว) ═══════════════╗
   ║ [Policy Center] governance คร่อมทุก area            ║
   ║   ┌──────────┬──────┬────────┬───────┬─────┐        ║
   ║ Operation    HR   Report   Agent    QA              ║
   ║ หัวใจ        คน  ดึงทุก area  AI    ทดสอบ            ║
   ╚════════════════════════════════════════════════════╝
   [Cubic] backbone (แยก site)   [Knowledge+CMS] content (แยก site)
```

**ความสัมพันธ์ (mental model)**
- **Operation** = เดินงานจริง ศูนย์กลาง data
- **HR** = ดูแลคน → feed พนักงาน/org ให้ area อื่น
- **Report** = อ่านอย่างเดียว ดึงข้ามทุก area
- **Policy Center** = layer คร่อม — ใครเข้าอะไรได้, สายอนุมัติ (DOA), audit, data classification. **ทุก feature ต้อง pair กับ Policy**
- **Agent** = AI ที่เรียกทุก area ผ่าน API
- **Cubic / Knowledge** = backbone + content ที่ Core อาศัย

## A3. หลักการออกแบบ 8 ข้อ (Design Principles)

| # | หลักการ | ความหมายเชิงปฏิบัติ |
|---|---|---|
| 1 | **Area → Module → Feature** | โครง 3 ชั้นตายตัว ทุก feature ต้องบอกได้ว่าอยู่ area/module ไหน |
| 2 | **Federated Multi-Tenant** | ทุก query ต้อง tenant-scoped (RLS) — ห้ามออกแบบ query ข้าม tenant |
| 3 | **Master กลาง + Config ต่อ Module** | master data อยู่กับ module เจ้าของ (เช่น UoM conversion เป็นของ Product ไม่ใช่ uom_master) |
| 4 | **Governance-as-Layer** | Policy / DOA / Audit เป็น cross-cutting — **ห้ามฝัง rule อนุมัติในแต่ละ module** |
| 5 | **AI-First** | ทุก module ต้องให้ Agent เรียกผ่าน API ได้ + มี skill/action ที่ declare ไว้ |
| 6 | **Registry-First** | logic ที่ใช้ซ้ำ = "engine" ต้อง register ที่ CUBIC Registry (ห้าม copy-paste logic ข้าม feature) |
| 7 | **Data Classification 4 ระดับ** | Public / Internal / Confidential / Restricted — **default = Internal** ทุก field |
| 8 | **Module Linkage (standalone vs integrated)** | ทุก module ที่อาจรันเดี่ยวได้ ต้อง toggle "เชื่อม/ไม่เชื่อม" ได้ (ดู F4) |

## A4. Governance — Policy Center

| Term | ความหมาย |
|---|---|
| **DOA** | Delegation of Authority — ศูนย์กลาง approval rules (flat / sequential / threshold) |
| **RBAC / User Access** | role-based access matrix — ทุก feature ต้องมี entry |
| **Feature-DOA Pairing** | **iron rule** — ทุก feature ต้องมี DOA entry + User Access entry ก่อน deploy |
| **ENC** | Enhancement — เพิ่ม feature เข้า governance registry |
| **PDPA** | consent + Data Subject Request (กฎหมายไทย) |
| **Data Classification** | Public / Internal / Confidential / Restricted (default Internal) |

### ⭐ pre-DOA Placeholder Pattern (ใช้ทุก feature ที่มีการอนุมัติ)

```js
// ทุก feature ที่มี approval ต้องมี 3 field นี้ + comment
approver_role   : null,   // TODO: DOA engine
approved_by     : null,   // TODO: DOA engine
approval_chain  : [],     // TODO: DOA engine
```
- สร้าง **action + UI + field** ให้ครบ แต่ **ห้าม hardcode rule อนุมัติ**
- DOA engine (Policy Center) จะ centralize ทีหลัง — เมื่อถึงเวลาแค่ wire เข้า ไม่ต้องรื้อ feature
- feature ที่แตะ approval ทั้งหมด **ไม่เข้า lane การผลิตปกติ** จนกว่า DOA จะพร้อม (ดู D6 Boundary)

---

# PART B — ภาษากลางของ Business (สำคัญที่สุด)

> ทีมคุยกันด้วยลำดับชั้นนี้ทั้งหมด ถ้า AI ใช้ศัพท์ผิดชั้น = เอกสารทั้งชุดเพี้ยน

## B1. ลำดับชั้น 6 ระดับ

```
VS    Value Stream      "ระบบ business 1 ตัว"                 เช่น P2P, S2C
 └─ VC    Value Chain   "happy path หลัก ตัดสินใจก่อน start"     เช่น Postpay / Prepay / Deposit
     └─ Path            "event ระหว่างทาง เจอแล้วถึงรู้"          เช่น Happy / Short / QC-Fail
         └─ CL          "Chain Link — งานข้ามแผนก"
             └─ SOP     "Standard Operating Procedure — งานในแผนก"
                 └─ SOW "Statement of Work — task 1 คน 1 deliverable (A→B→C)"

Edge Case (system: timeout / double-submit / race) → ไป FRD §Error Handling ไม่อยู่ใน Bible
```

## B2. ตารางตัดสินว่าอะไรอยู่ชั้นไหน

| คำถาม | → layer |
|---|---|
| เลือกตอนเซ็นสัญญา / setup vendor / config ก่อนเริ่ม | **VC** |
| เห็นสถานการณ์จริงระหว่างทำแล้วถึงรู้ | **Path** |
| งานข้ามฝ่าย หลายคนทำต่อกัน | **CL** |
| งานในแผนกเดียว 1 phase | **SOP** |
| task 1 คน 1 deliverable (trigger→action→result) | **SOW** |
| ระบบล่ม / network fail / validation / กด back | **FRD Edge Case** (ไม่ใช่ business) |

**หัวใจ:** VC = *"เราจะวิ่งเส้นไหน?"* (lock ตอน trigger เช่น PO create) · Path = *"วิ่งไปแล้วเจออะไร?"* (เกิดเมื่อเจอ event)

### ความสับสนที่เจอบ่อย (ห้ามพลาด)
- **Scenario (QA) ≠ Path (business)** — Scenario ใช้เฉพาะเอกสาร test
- **Channel (ศัพท์เก่า) = VC** — ใช้ VC เป็น canonical
- **Edge Case ≠ Path** — Path = เหตุการณ์ธุรกิจปกติ (รับไม่ครบ, QC fail) · Edge Case = system anomaly

## B3. SOW Zigzag — A→B→C

```
SOW 1:  A1 (รอ...)  → B1 (task) → C1 (รอ...)
                                     ║ exact match
SOW 2:  A2 (= C1)   → B2 (task) → C2 (รอ...)
                                     ║
SOW 3:  A3 (= C2)   → B3 (task) → C3 (เสร็จสิ้น...)  ← = vs.outcome
```

**Iron rules 5 ข้อ**
1. `A · Trigger` ขึ้นต้น "รอ..." เสมอ (SOW แรกใช้ `vs.trigger`)
2. `B · Task` = กริยา + object ชัดเจน — ห้าม "ดำเนินการ..."
3. `C · Result` ขึ้นต้น "รอ..." หรือ "เสร็จสิ้น..."
4. Chain: `C ของ SOW N = A ของ SOW N+1` (copy ตรงทุกอักษร)
5. ปิด chain: `C ของ SOW สุดท้าย = vs.outcome`

12 columns ต่อ SOW: `cl · cl_name · sop · sop_name · sow · sow_name · A · B · C · actor · target · sla · dod`

## B4. Outcome States (Path จบยังไงได้)

`Closed-Complete` · `Closed-PartialFulfill` · `Closed-Cancelled` · `Closed-Replaced` · `Closed-Returned` · `Disputed`
ทุก Path **ต้องจบที่หนึ่งใน state เหล่านี้** — ถ้าออกแบบแล้วมี path ที่ไม่จบ = ออกแบบไม่ครบ

## B5. layer ไหนอยู่เอกสารไหน

| layer | เอกสาร |
|---|---|
| VS | VS Charter / VS Bible §1 |
| VC | VS Bible §2 VC Catalog |
| Path | VS Bible §3 Path Catalog |
| CL / SOP | VS Bible §4 + BRD §Workflow |
| SOW | VS Bible §5 Zigzag + Test Scenarios |
| Edge Case | FRD §Error Handling / §NFR |

---

# PART C — วิธีทำงาน (Methodology)

## C1. หลักคิดใหญ่: **HTML-First / Reverse Mode**

> เดิม doc-first (BRD → FRD → HTML) · **ตอนนี้ HTML-first — HTML prototype คือ source of truth เชิงเวลา**
> เขียนเอกสารโดย "เห็นหน้าจอจริงแล้ว" ไม่ใช่จินตนาการ

```
HTML prototype (vibe จนพอใจ) → สกัดเป็น FRD → Test case → QA artifacts
```

**ข้อควรระวังเชิงอำนาจ (สำคัญ):**
- **HTML มาก่อนเชิงเวลา ไม่ใช่เชิงอำนาจ**
- **Design Authority อยู่ที่ FRD**
- ลำดับชนะกัน: **LOCK (ใบเซ็น) ชนะทุกอย่าง → RIF ชนะ HTML → ยกเว้นเรื่อง layout: HTML ชนะ**

## C2. WF-01 v2 — Feature Lane (เลนผลิต feature ใหม่ ทีละตัว)

**เหนือเลน (ต้องมีก่อน):**
- `plan-module-workflow-mapper` → ทำต่อ module ได้ `workflow_graph.json` + `GOLDEN_RULES.md` + `BUILD_ORDER.md` (Central Plan)
- `newfeature-signoff-generator` → ใบเซ็น sign-off ต่อ feature ได้ **LOCK-XX** (scope lock)
- `lane-brief-generator` → **LANE_BRIEF** (งานคนขั้นเดียวในเลน — บอกว่ารอบนี้ทำ feature ไหน scope แค่ไหน)

**ในเลน (AI รันต่อเนื่อง one-shot):**

| Step | งาน | Skill | หมายเหตุ |
|---|---|---|---|
| S0 | Brief → RIF | `requirement-intake-formatter` | input = Central Plan ทั้งก้อน + LANE_BRIEF · confidence ≥80% + LOCK ครบ |
| S1 | สร้าง HTML | `html-generator-v6` | อ่าน NODE_BRIEF + GOLDEN_RULES เสมอ |
| S2 | ตรวจ "ทำถูกมั้ย" (UX/CI/iron rules) | `qc-ux-html-checker` | UX **ก่อน** Coverage เสมอ — ล็อกแล้ว · ต้องมีหลักฐานภาพ (Render Gate) ไม่มีภาพ = BLOCK |
| S3 | ตรวจ "ครบมั้ย" (business scope) | `qc-coverage-checker` R1 | เทียบกับ workflow graph · ทุก ✓ ต้องมี evidence ชี้ตำแหน่ง |
| S4 | BRD | `brd-generator-full` | อ่าน HTML เป็น input ร่วม · gate C01–C23 ในตัว |
| S5 | FRD Pack | `frd-generator-v6` | Design Authority · gate Phase 3.5 A–M ในตัว |
| S6 | Test case + UAT doc | `ai-testcase-md-generator` → `qa-friendly-html-generator` | 1:1 **ห้าม drop เคส / ห้ามยุบ step** |
| S6.5 | Coverage รอบ 2 | `qc-coverage-checker` R2 | rules อยู่ใน 05_RULES + TC ครอบทุก block rule |
| S6.75 | Drift check (เงื่อนไข) | `html-to-frd-sync` | รันเมื่อ HTML ถูกแก้หลัง S5 |
| S7.5 | UI Brief | `html-ui-brief` | สกัดจาก HTML final แบบ 1:1 → เข้า DevPack |
| S8 | Pack | runner | DevPack.zip + `_OP_MANIFEST.json` |
| S9 | OP Sync | adapter (dry-run) | แขวนไฟล์+สถานะราย SOW |

**Orchestrator:** `feature-lane-runner` วิ่งทั้งเลนแบบไม่หยุดถาม · resumable ผ่าน `_LANE_STATE.json`

## C3. Gate Policy (กติกาผ่าน/ไม่ผ่าน)

- **PASS / WARN → ไหลต่อ**
- **BLOCK → วนแก้** (cap 3 ครั้ง/gate · 8 ครั้ง/feature · issue เดิมซ้ำ 2 รอบ = หยุด ออก `_BLOCKED.md` แล้วข้ามไป feature ถัดไป ไม่ล้ม batch)
- **NOT-CHECKED = BLOCK** (ตรวจไม่ได้ ≠ ผ่าน)
- **Hard Stop 5 ข้อ — ห้าม auto-fix เด็ดขาด:** ขัด LOCK · ขัดใบเซ็น sign-off · ขัด workflow graph · graph ขาดข้อมูล · ขัด governance
- **ไม่มี "ตัวตรวจอิสระ" แล้ว** — `output-checker` ถูกตัดออก (2026-07-25) เพราะเกณฑ์ผูก CI เก่า · งาน final check กระจายเข้า built-in gate ของแต่ละ skill
- **Post-lane rule:** ถ้า vibe HTML หลังได้ DevPack แล้ว → **ต้องรัน `html-to-frd-sync` เสมอ** ก่อนถือว่าเอกสารยัง valid

## C4. Document Chain & Scope Lock (ห้ามขาด)

```
ใบเซ็น Sign-off [LOCK-XX] → RIF §16.3 → BRD §3.4 → FRD 07_LOCKED → Test Case → DevPack
```
- Scope Lock **ห้าม override ตลอดสาย** — ขัดเมื่อไหร่ = Hard Stop
- ถ้า requirement ใหม่ขัด LOCK → ไม่ใช่ bug fix แต่คือ **เปลี่ยน scope** → ต้องออกใบเซ็นใหม่

## C5. Open Question (OQ) — วิธีจัดการสิ่งที่ยังไม่เคาะ

- ทุกจุดที่ยังไม่ชัด → log เป็น **OQ-xx** อย่าเดาแล้วเขียนลงเอกสาร
- routing: **Business/scope OQ → Strike (Project Owner)** · **UI/layout ที่หลุด pattern → Chin** · **BE/infra → พี่เบิร์ด** · **engine registration → Architect**
- OQ ที่ blocking ต้องเคาะ **ก่อน** ออก LANE_BRIEF (เช่น F-GOODS-RECEIPT ต้องเคาะ tolerance ชั้นไหน ก่อนเริ่ม)
- สิ่งที่ยังไม่มี data source จริง **ห้ามแต่งตัวเลข** → defer + label ว่า "เฟสถัดไป"

## C6. Workflow อื่น ๆ

| WF | ชื่อ | ใช้เมื่อ |
|---|---|---|
| WF-01 | New Feature (Full Loop) | สร้าง feature ใหม่ทั้งวง (ตาม C2) |
| WF-02 | Enhancement | ปรับ feature เดิม → `enc-doc-generator` (ENC Doc diff-only ไม่ regen ของเดิม) |
| WF-03 | New Requirement (Draft) | discovery ระดับ requirement |
| WF-04/05/06 | Report (Informative / CSV / Dashboard) | งานรายงาน 3 แบบ |

**Enhancement flow:** HTML เดิม → vibe ด้วย `html-generator-v6` → `enc-doc-generator` (ENC Doc ไฟล์เดียว diff-only) → test case → ส่ง dev
---

# PART D — Central Plan: Trade Core Feature Map (แผนที่กลาง)

> **นี่คือ "แผนที่กลาง" ที่ทุก feature ในสายการค้า (Purchase · Inventory · Sales · Accounting · Finance) ต้องอ้าง**
> ก่อนแตะ feature ใดก็ตาม **ต้องอ่าน Central Plan ก่อนเสมอ** — ไม่ใช่เดาจากชื่อ feature

```yaml
graph_id: TRADE-CORE
graph_name: CUBE 4.0 — Trade Core Feature Map (Purchase · Inventory · Sales)
version: 4.0.0
generated: 2026-07-24
nodes: 46          # 41 core (34 planned + 12 existing) + 5 boundary
edges: 94          # data 36 · config 29 · trigger 26 · reversal 3
golden_rules: 161  # block 136 · warn 25
rule_source: decision 82 · erp-standard 49 · bible 30
```

## D1. Central Plan ประกอบด้วยอะไร (6 ไฟล์)

| ไฟล์ | คืออะไร | ใช้ตอนไหน |
|---|---|---|
| **`workflow_graph.json`** | ต้นฉบับเครื่องอ่าน — 46 nodes · 94 edges · 161 rules (schema ด้านล่าง) | ให้ coverage checker เทียบ · ห้ามแก้มือแบบไม่ผ่าน mapper |
| **`GOLDEN_RULES.md`** | **ตัวกลางของทุกเส้น** — กฎที่ทุก feature ต้อง preserve (XR-* คร่อมทุก feature + GR-* ราย feature) · ส่วน 1–3 generate จาก graph ตรง ๆ **sync 100% ห้ามแก้มือ** | RIF / BRD / FRD / TC ทุกตัวต้องอ้าง `GR-*` / `XR-*` |
| **`DEVELOPMENT_PLAN.md`** | 41 features เรียงลำดับ 5 phases · depends-on · จำนวน rules ต่อ feature · Phase 0 rework | วางแผนว่าจะทำอะไรก่อนหลัง |
| **`BUILD_ORDER.md`** | 9 waves + เหตุผลของแต่ละ wave + ปลดล็อกอะไร + engine ที่ถูกยุบ | ตัดสินว่าเริ่ม feature นี้ได้หรือยัง |
| **`WORKFLOW_MAP.html`** | visual DAG (Warm Light) ดูความสัมพันธ์ทั้งแผนที่ | สื่อสาร / review กับทีม |
| **`_KNOWLEDGE_SYNC.md`** | patch ที่ต้อง sync กลับเข้า `cube-master-knowledge` + งานค้าง manual | หลังอัปเดตแผน |

## D2. Schema ของ `workflow_graph.json`

```jsonc
node = {
  id, code, name, name_th,
  type   : "feature" | "boundary",     // boundary = นอก scope แต่มี interface
  zone   : "core" | "boundary",
  status : "existing" | "planned",
  domain : "Master|Inventory|Warehouse|Sales|Purchase|Accounting|Finance|Marketing",
  summary, erp_refs[], artifacts{brd, frd, html}
}

edge = { id, from, to, type, relation, detail }
// type: data | config | trigger | reversal

golden_rule = { id, node, rule, source, erp_ref, lock_ref, severity }
// source  : bible | decision | erp-standard
// severity: block | warn
```

### ความหมายของ edge 4 ชนิด (สำคัญ — ใช้ตัดสินลำดับ build)

| type | ความหมาย | บล็อกลำดับ build ไหม | ตัวอย่าง |
|---|---|---|---|
| `config` | ต้องตั้งค่าให้เสร็จก่อนใช้ปลายทาง | ✅ บล็อก | Warehouse → Inventory · COA → ทุก posting |
| `data` | ส่งข้อมูล / อ้างเอกสารต้นทาง | ✅ บล็อก | PO → Goods Receipt |
| `trigger` | เหตุการณ์กระตุ้นงานถัดไป | ❌ ไม่บล็อก | GRN → Putaway |
| `reversal` | เอกสารแก้กลับของอีกตัว | ❌ ไม่บล็อก | AP Credit Note → AP Invoice |

## D3. ⭐ Cross-Feature Rules — XR-01..XR-14 (กฎคร่อมทุก feature)

> **นี่คือกฎที่ AI ทุกตัวต้องท่องได้** — ผิดข้อไหนข้อหนึ่ง = ระบบผิดเชิงธุรกิจ ไม่ใช่แค่ UI เพี้ยน

| id | กฎ | ที่มา |
|---|---|---|
| **XR-01 Conservation** | ทุก movement (รับ/เก็บ/หยิบ/แตก-แพ็ค/คืน/ปรับ/ย้าย/ส่ง) ต้อง conserve **base qty** — **คำนวณสด ห้ามพึ่ง field สะสม** | LD-02 |
| **XR-02 Allocated ศักดิ์สิทธิ์** | `allocated` แก้ได้โดย **Stock Reservation ผู้เดียว** — feature อื่นอ่านได้ห้ามเขียน · ลดสต็อกได้ไม่เกิน `on_hand − allocated` | AC-ADJ-04 + OQ-G04 |
| **XR-03 post แล้วห้ามแก้** | validate/post แล้ว → แก้ด้วยเอกสารแก้ไขเท่านั้น (reversal / CN / DN) **ห้าม edit-delete ตรง** — Tax Invoice เด็ดขาด | audit + ภาษีไทย |
| **XR-04 Reverse ≠ Return** | กลับรายการ (บันทึกผิด ของไม่เคลื่อน) ≠ คืนของจริง (ของออกจากคลัง) — คนละเอกสาร คนละ movement | SAP 102 vs 122 |
| **XR-05 Refund ผ่าน CN เสมอ** | คืนเงิน → PV `voucher_type=refund` ต้องอ้าง CN — **ห้ามจ่ายคืนลอย** | Bible |
| **XR-06 HOLD ไม่ใช่ของ** | HOLD / DAMAGED / QC ไม่นับ available — ทุก consumer (Picking, รายงาน, Adjustment ลด) ต้อง filter ออก | Bible |
| **XR-07 3-Way ยกเว้นทางเดียว** | 3-way บังคับทุก VC ยกเว้น VC7 Direct Payment — **รวมถึง GRN แบบ non-PO ที่ต้องวิ่งเส้น Direct Payment** | Bible + OQ-G02 |
| **XR-08 Partial ต้องมีสถานะ** | รับขาด/ส่งขาด/หยิบขาด/จ่ายขาด → line ค้างต้องเห็นสถานะ (partial หรือ closed+เหตุผล) **ห้ามหายเงียบ** | ปิดงวดไม่ได้ถ้ามองไม่เห็น |
| **XR-09 อนุมัติผ่าน DOA** | ทุกจุดอนุมัติเรียก Approval Authority — ระหว่างรอใช้ placeholder `approver_role / approved_by / approval_chain` **ห้าม hardcode** | กติกาเหล็ก CUBE |
| **XR-10 config ไม่ย้อนหลัง** | payment term / VC / tolerance / conversion factor เปลี่ยนแล้ว **มีผลเฉพาะเอกสารใหม่** — ที่ approve แล้ว snapshot ค่าตอนสร้าง | เอกสารเก่าต้อง reproduce ได้ |
| **XR-11 Lot ติดของ** | สินค้าที่เปิด tracking → lot/serial ติดทุก movement ตลอดเส้น **ห้ามรวม lot ต่างกันเป็นแถวเดียว** | OQ-G12 |
| **XR-12 Cancel/Reverse ราย feature** | **ไม่มี reversal engine กลาง** — แต่ละ feature ทำ cancel ของตัวเองภายใต้กติกาเดียวกัน | OQ-G03 |
| **XR-13 Cascade ต้องย้อนครบรอบ** | reverse เอกสารต้นทางที่มีปลายน้ำผูกอยู่ → **cascade ยกเลิกปลายน้ำพร้อมกัน** ใช้ `reversal_ref` ร่วม · **เงินที่จ่าย/รับไปแล้วเป็นเส้นหยุด** ต้อง void voucher ก่อน | OQ-G03a |
| **XR-14 Config หลายชั้น specific ชนะ** | ค่าที่ตั้งได้หลายระดับ (tolerance: config กลาง → material master → เอกสาร) → ชั้นเจาะจงชนะ **และต้องแสดงว่าใช้ค่าจากชั้นไหน** | OQ-G01a |

## D4. Decision Log — OQ-G01..G14 (ปิดครบ 2026-07-24)

| OQ | คำตอบที่เคาะ | ผลกับการออกแบบ |
|---|---|---|
| G01 tolerance | % config กลาง + override ต่อ PO line | → รวมเป็น `F-WAREHOUSE-CONFIG` |
| G01a tolerance ที่ material master | **ตั้งที่ material master ด้วย** | resolve **3 ชั้น**: config กลาง → Product → PO line (specific ชนะ) · Product ต้องมี field ค่าเผื่อ · XR-14 |
| G02 รับลอย (ไม่มี PO) | **ได้ทั่วไป** | ไม่มี config switch · non-PO ไม่เข้า 3-way → วิ่งเส้น Direct Payment |
| G03 ยกเลิกเอกสาร | แต่ละ feature ทำเอง | **ไม่มี reversal engine** · XR-12 |
| G03a reverse GRN หลัง invoice match | **ทำได้ แต่ต้องย้อนหมด** | **cascade reversal** ใช้ `reversal_ref` ร่วม: GRN + AP Invoice + GR/IR กลับพร้อมกัน · **PV จ่ายแล้ว = เส้นหยุด** ต้อง void ก่อน · XR-13 |
| G04 allocated | **จองทันทีตอน SO confirm** | `F-STOCK-RESERVATION` เป็นเจ้าของ allocated ผู้เดียว |
| G05 ของเสีย | ใช้ Stock Adjustment reason | **ไม่มีเอกสาร Scrap** |
| G06 vendor เก็บเพิ่ม | เอกสาร DN | อยู่ในเอกสาร **CN/DN ใบเดียว** (doc_type=DN ฝั่งเจ้าหนี้) |
| G07 เครดิตลูกค้า | **ไม่คุมในระบบ v1** | ห้าม dev ใส่ block เองโดยไม่แก้ decision นี้ |
| G08 วันส่ง | กรอกมือ | **ไม่มี ATP** |
| G09 ค้างส่ง | **status บน SO line** | **ไม่มีเอกสาร backorder** |
| G10 putaway | เลือกตำแหน่งมือ | ไม่มี auto putaway rule + log ผู้เลือก |
| G11 นับสินค้า | ยกคลัง + รอบ custom | อยู่ใน `F-STOCK-COUNT` |
| G12 lot/serial | **ต้องมี บังคับทั้งเส้น** | ยุบเข้า `F-INVENTORY` · XR-11 |
| G13 GR/IR | ตั้ง accrual | `F-GRIR-ACCRUAL` |
| G14 landed cost | ค่าขนส่ง/ภาษีนำเข้าลงค่าใช้จ่ายแยก | **ห้ามกระจายเข้า `unit_cost`** |

> ✅ **OQ ค้าง = 0** ใน GOLDEN_RULES v4.0.0
> ⚠️ แต่ `BUILD_ORDER.md` และ run list ยังเขียน G01a/G03a เป็น "ค้าง" อยู่ — **ให้ยืนยันกับ Strike อีกครั้งก่อนเริ่ม `F-GOODS-RECEIPT`** (ถ้ายืนยันแล้วให้ลบหมายเหตุนั้นออก)

## D5. โครงสร้างที่ถูกยุบ/รวมใน v4.0.0 (ห้ามสร้างของที่ยุบไปแล้วขึ้นมาใหม่)

| เดิม | ผลใน v4.0.0 |
|---|---|
| Credit Note / Debit Note แยกกัน | รวมเป็น **`F-CREDIT-DEBIT-NOTE` ใบเดียว** ครอบ 4 แบบ (CN/DN × เจ้าหนี้/ลูกหนี้) แยกด้วย `doc_type` + `party` |
| Direct Payment เป็น feature | **ไม่เป็น feature** — เป็น **โหมดบนหัว `F-AP-INVOICE`** (ติ๊กจ่ายตรง ข้าม PR/PO/GRN) |
| AR Ledger เป็น feature | **ไม่เป็น feature** — ยอดลูกหนี้คำนวณสด: `Invoice − ΣRV − ΣCN` |
| Lot / Serial / Expiry เป็น feature | **ยุบเข้า `F-INVENTORY`** (tracking + FEFO อยู่ในตัวยอดคงคลัง) |
| Receiving Tolerance Config | เปลี่ยนเป็น **`F-WAREHOUSE-CONFIG`** |
| COA | **เพิ่มใหม่** `F-COA` ผังบัญชี + mapping ต่อประเภทเอกสาร/reason — เงื่อนไขของทุก posting |
| ENG-3WAY (engine) | ยุบเข้า **`F-AP-INVOICE`** |
| ENG-INV-UOM (engine) | ยุบเข้า **`F-INVENTORY`** |
| ENG-DOA | เป็น boundary `F-APPROVAL-DOA` — บังคับผ่าน rule ของ feature ผู้เรียก |

**หลักการที่ตามมา:** *ไม่มี engine แยกใน Trade Core · ไม่มี feature ที่เป็นแค่ "โหมด" ของเอกสารอื่น*

## D6. Boundary — 5 feature ที่อยู่นอกเลนผลิต

`F-APPROVAL-DOA` · `F-USER-ACCESS` (Policy Center) · `F-NOTIFICATION` · `F-BUDGET-CONTROL` · `F-GL-POSTING`★
→ มี interface แต่ยังไม่พัฒนาในรอบนี้ · feature ที่แตะสิ่งเหล่านี้ใช้ **placeholder pattern** (XR-09) รอ wire ทีหลัง

## D7. Naming & Domain Convention (v4.0.0)

- ชื่อ feature **ตรงกับโฟลเดอร์จริงในระบบ**: Product · UOM · BOM · COA · Product Catalog · Sales Channel · Payment Term · Vendor · Vendor Price List · Warehouse · PR · CP · PO · Purchase Config
- งานที่ **กระทำต่อสต็อก** ใช้คำว่า **Stock** (Stock Adjustment / Transfer / Count / Reservation) · **ตัวยอดคงคลัง** คือ **Inventory**
- **Domain split (segregation of duties):**
  - **Accounting** = ตั้งหนี้ / ออกเอกสาร / ลงบัญชี → AP Invoice, AR Invoice, Credit/Debit Note, GR/IR, COA, GL
  - **Finance** = เงินเข้า-ออกจริง → Payment Voucher, Receipt Voucher

| Domain | จำนวน feature |
|---|---|
| Warehouse | 11 |
| Sales | 8 |
| Purchase | 6 |
| Master | 5 |
| Accounting | 5 |
| Inventory | 3 |
| Finance | 2 |
| Marketing | 1 |

## D8. วิธีใช้ Central Plan ตอนทำ feature (ท่ามาตรฐาน)

```
1. เปิด workflow_graph.json → หา node ของ feature
   → อ่าน summary / status / domain / erp_refs / artifacts (มีของเดิมไหม)
2. ดู edge ทุกเส้นที่ from = feature นี้
   → ทุกเส้น "ออก" ต้องมี hook ใน UI (เช่น GRN ต้องมีทางไป Putaway / RTV / GR-IR)
3. ดู edge ทุกเส้นที่ to = feature นี้
   → ต้นน้ำเสร็จหรือยัง (config/data บล็อก · trigger/reversal ไม่บล็อก)
4. เปิด GOLDEN_RULES.md ที่หัวข้อ feature นี้
   → rule severity=block ทุกข้อ **ต้องกลายเป็น AC ใน BRD** และมี test case
   → rule warn = best practice (ใส่ได้ ไม่บล็อก)
5. อ่าน XR-01..14 ทุกครั้ง (คร่อมทุก feature)
6. เช็ค §"เคสแปลก ๆ → เดินตามกฎไหน" ใน GOLDEN_RULES — ตอบเคสยากได้เร็วมาก
7. จบ: qc-coverage-checker เทียบกับ graph ว่าครบทุก node/edge/rule ที่ประกาศไว้
```

**กฎเหล็กที่มาจาก Central Plan:**
- rule `severity=block` ทุกข้อ → **ต้องเป็น AC** · ไม่มี AC = coverage gate BLOCK
- edge ออกทุกเส้น → **ต้องมี hook ใน HTML** · ไม่มี hook = coverage gate BLOCK
- **ห้ามเดา rule เอง** — ถ้ากฎที่ต้องการไม่มีใน GOLDEN_RULES = เป็น OQ ต้องเคาะ ไม่ใช่คิดแทน

## D9. ⚡ Cheat Sheet — เคสแปลกเดินตามกฎไหน (ย่อจาก GOLDEN_RULES §4)

| เคส | เส้นทางที่ถูกต้อง | กฎ |
|---|---|---|
| ของมาเกิน PO | เกิน tolerance → **block ที่ GRN** ต้องแก้ PO หรือปฏิเสธก่อนรับ | GR-WHCFG-01/02 · GR-GRN-03 |
| ของมาขาด | GRN partial → รอครบ หรือ Close Balance + เหตุผล | GR-GRN-04 · XR-08 |
| รับของไม่มี PO (รับลอย) | ได้ แต่ระบุ `source=non-PO` + เหตุผล → ไม่เข้า 3-way → วิ่งเส้น Direct Payment | GR-GRN-01 · XR-07 |
| ของถึงก่อนใบแจ้งหนี้ | GRN → ตั้ง GR/IR accrual → clear ตอน invoice match | GR-GRIR-01 |
| ใบแจ้งหนี้ถึงก่อนของ (VC2) | AP Invoice → PV → GRN ทีหลัง → match ย้อน | GR-GRN-02 · GR-APINV-03 |
| QC ไม่ผ่าน | HOLD → **RTV** หรือ **Stock Adjustment reason=ของเสีย** | GR-GRN-05 · GR-RTV-01 · XR-06 |
| บันทึกรับผิด (ของไม่เคลื่อน) | cancel/reverse ใน GRN เอง (ต้องยังไม่ putaway/หยิบ/ขาย) | GR-GRN-07 · XR-04/12 |
| บันทึกรับผิด **หลัง invoice match** | reverse GRN ได้ แต่ **cascade ยกเลิก AP Invoice + กลับ GR/IR พร้อมกัน** (`reversal_ref` เดียว) · PV จ่ายแล้วต้อง void ก่อน | GR-GRN-08/09/10 · XR-13 |
| ค่าเผื่อขัดกันหลายชั้น | PO line > material master > config กลาง · **GRN ต้องบอกว่าใช้ชั้นไหน** | XR-14 |
| vendor ลดหนี้ / เก็บเพิ่ม | **CN/DN ใบเดียว** เลือก `doc_type` · net = Invoice + ΣDN − ΣCN | GR-CN-01/06/07 |
| ยกเลิก PV ที่จ่ายแล้ว | reversal ใน PV เอง → แจ้ง GL + invoice กลับเป็นค้างจ่าย | GR-PV-05 · XR-12 |
| ปรับสต็อกชนยอดจอง | ลดได้แค่ `on_hand − allocated` · allocated ไม่เปลี่ยน | GR-ADJ-01 · XR-02 |
| SO ยืนยันแต่ของไม่พอ | **confirm ได้ จองเท่าที่มี** ส่วนขาดค้าง partial (ไม่ block) | GR-SO-01 · GR-RSV-02 |
| ส่งลูกค้าไม่ครบ | ค้างเป็น **status partial บน SO line** (ไม่มีเอกสาร backorder) | GR-DN-02 · GR-PICK-03 · XR-08 |
| ลูกค้าเครดิตเต็ม | **v1 ไม่คุม** — ฝ่ายขายรับผิดชอบเอง | GR-SO-02 · GR-DN-04 |
| ลูกค้าคืนของ | Sales Return → QC → pass เข้า available / fail → Adjustment → ออก CN | GR-RMA-01/02/03 |
| ยกเลิก SO | ก่อนส่ง = ปลดจอง · หลังส่ง = ผ่าน RMA · หลัง invoice = ผ่าน CN | GR-SO-04 · XR-03 |
| แก้ Tax Invoice ที่ออกแล้ว | **ไม่ได้** — CN/DN เท่านั้น | GR-ARINV-02 · XR-03 |
| ลูกค้าจ่ายไม่ครบ/เกิน | RV partial ค้าง **ห้าม auto-close** | GR-RV-01 · XR-08 |
| ค่าขนส่ง / ภาษีนำเข้า | ค่าใช้จ่ายแยก **ห้ามเข้า `unit_cost`** | GR-APINV-11 |
| จ่ายค่าไฟ/บริการ ไม่มี PO | **AP Invoice ติ๊กโหมดจ่ายตรง** (ไม่มี feature แยก) + approval สูงกว่าปกติ | GR-APINV-08/09 |
| ขายบริการ ไม่มี SO/DN | **AR Invoice ออกตรง** ตาม config (โหมดของเอกสารเดียวกัน) | GR-ARINV-05 |
| อยากรู้ยอดลูกหนี้คงค้าง | คำนวณสด `Invoice − ΣRV − ΣCN` — ไม่เก็บยอด mutable | GR-ARINV-06 |
| บัญชียังไม่ได้ map | **post ไม่ได้** — mapping COA ต้องครบก่อน | GR-COA-03 |
| เพิ่มสินค้าเข้าคลังครั้งแรก | Product active + มี location → สร้าง balance ผ่าน **Stock Adjustment** ห้ามสร้างยอดลอย | GR-INV-07/08 · GR-WH-02 |
| สินค้าไม่อยู่ในแค็ตตาล็อกแต่อยากขาย | เสนอ/ตั้งราคาไม่ได้ ต้องเพิ่มเข้าแค็ตตาล็อกก่อน หรือขออนุมัติ | GR-PCAT-01 |
| ราคาต่างกันตามช่องทาง | Price List แยกตาม Sales Channel — SO ต้องระบุช่องทาง | GR-SCH-01 · GR-PLIST-01 |
| นับสินค้าไม่ตรง | Stock Count → ผลต่างออกเป็น **Stock Adjustment เท่านั้น** | GR-CNT-01/03 |
| สินค้าใกล้หมดอายุ | หยิบตาม **FEFO เป็น default** — override ต้องมีเหตุผล + log | GR-INV-10 |

---

# PART E — Value Streams: P2P และ S2C

## E0. สูตรกลาง — ออกแบบ VS ใหม่ต้องได้ 9 อย่างนี้

ไม่ว่าจะ P2P, S2C หรือ VS อื่น (H2R/R2R/I2C) ก่อนแตะหน้าจอต้องตอบให้ครบ:

| # | สิ่งที่ต้องได้ | คำถามนำ |
|---|---|---|
| 1 | **Identity** | trigger คืออะไร · outcome คืออะไร · ใครเป็นเจ้าของ VS |
| 2 | **VC Catalog** | มีกี่เส้นทางหลัก · ตัดสินที่ document ไหน step ไหน · ใครตัดสิน · เปลี่ยนทีหลังได้ไหม |
| 3 | **Path Catalog ต่อ VC** | ระหว่างทางเจออะไรได้บ้าง (ขาด/เกิน/เสีย/คืน/ยกเลิก) และแต่ละอันจบที่ outcome state ไหน |
| 4 | **Invariants** | กฎที่ห้ามผิดทุกกรณี (เช่น 3-way match) — เขียนเป็นสมการได้ยิ่งดี |
| 5 | **Locked Decisions** | ข้อที่เคาะแล้วห้ามเถียงซ้ำ (D01, D02, ...) พร้อมเหตุผล |
| 6 | **Document Chain** | เอกสารไหลจากอะไรไปอะไร · เอกสารไหน trigger สถานะไหน |
| 7 | **Master data ที่ต้องมีก่อน** | ถ้า master ยังไม่มี = feature นี้ทำไม่ได้ (dependency) |
| 8 | **จุดตัดกับ GL / Inventory / DOA** | ลง GL ตอนไหน · ตัด stock ตอนไหน · ใครอนุมัติตอนไหน |
| 9 | **Feature Catalog** | แตกเป็นกี่ feature · feature ไหนมีของเดิมแล้ว (★) · ลำดับ wave |

> ทำได้ครบ 9 ข้อ = ได้ **VS Bible** → แตกเป็น feature brief → เข้า lane
> skill ที่เกี่ยวข้อง: `vs-bible-intake` → `vs-bible-md-updater` → `vs-bible-to-brief-expander` → `plan-module-workflow-mapper`

---

## E1. P2P (Procure-to-Pay) — **มี Bible เต็มแล้ว**

- **Trigger:** ความต้องการสินค้า/บริการ (PR หรือ direct invoice)
- **Outcome:** ชำระเงิน vendor + ปิด PO + บันทึก GL
- **Invariants หลัก:** 3-way match บังคับ (ยกเว้น Direct Payment) · Close-Balance trigger ที่ GRN เท่านั้น

### E1.1 VC Catalog (7 เส้น)

| VC | ชื่อ | ลำดับเอกสาร | GRN trigger | 3-way match |
|---|---|---|---|---|
| VC1 | Full Postpay | PR/PO → GRN → Inv → PV | ทันที | ✅ |
| VC2 | Full Prepay | PR/PO → AP Inv → PV → GRN | หลัง PV confirm | ✅ |
| VC3 | Deposit | PR/PO → Inv มัดจำ → PV มัดจำ → GRN → Inv balance → PV balance | หลัง PV มัดจำ | ✅ (ที่ Inv balance) |
| VC4 | Installment | PR/PO → GRN → AP Inv → PV งวด 1..N | ทันที | ✅ (หลัง GRN ครั้งเดียว) |
| VC5 | Partial Delivery | PR/PO → GRN รอบ 1 → Inv qty จริง → PV → ... → GRN รอบ N | ทันที | ✅ (ต่อรอบ) |
| VC6 | Credit N วัน | PR/PO → GRN → Inv (due = วันออก + N) → PV ก่อน due | ทันที | ✅ |
| VC7 | **Direct Payment** | AP Inv ตรง → PV (bypass PR/PO/GRN) | N/A | ❌ bypass |

**VC Decision:** เลือกที่ **PO Wizard Step 2** · โดย Procurement Officer (+ HOD ถ้าเกิน threshold) · **เปลี่ยนไม่ได้หลัง PO approve** (ต้อง cancel + สร้างใหม่)
**ข้อยกเว้น:** Subcontract Unit Conversion → lock VC1 อัตโนมัติ

### E1.2 Receiving Rules (Path master — ใช้ทุก VC ยกเว้น VC7)

| สถานการณ์ | Rule | Action | ผลกับ AP Invoice |
|---|---|---|---|
| รับครบ + QC ผ่านหมด | Happy Path | Putaway ทั้งหมด | Invoice = PO qty · 3-way pass ทันที |
| รับครบ + QC fail บางส่วน | Partial QC | qty ดี → Putaway · qty fail → HOLD → สร้าง RTV | Invoice เต็ม → Hold → รอ CN → จ่าย net |
| รับครบ + QC fail ทั้งหมด | Full Reject | ทุก qty เข้า HOLD → RTV ทั้งล็อต | CN เต็มจำนวน → refund หรือส่งใหม่ |
| รับไม่ครบ (qty < PO) | **Partial always** | ตัดสินที่ GRN: รอรอบ 2 / Close PO balance | Invoice = qty รับจริง · PO eff = closed qty |
| รับไม่ครบ + QC fail บางส่วน | Hyper Case | Close balance qty ขาด → HOLD qty fail → RTV → Putaway qty ผ่าน | Invoice = qty รับ · CN = ขาด+fail · PV = Putaway qty |

**Iron rule:** *รับไม่ครบ = Partial เสมอ* ไม่มีข้อยกเว้น และ decision อยู่ที่หน้า GRN เท่านั้น

### E1.3 สมการ Invariant

```
3-Way Match:   PO effective qty  =  GRN qty รับจริง  =  AP Invoice net qty
PO effective   =  PO original qty  หลัง Close Balance
Invoice net    =  Invoice − CN
```
ทั้ง 3 ต้องตรงก่อนสร้าง PV ได้ (ยกเว้น VC7)

### E1.4 Locked Decisions 15 ข้อ (ห้ามเถียงซ้ำ)

| # | Decision |
|---|---|
| D01 | Payment term เลือกที่ PO เท่านั้น (PR/Comparison ไม่มี) |
| D02 | GRN trigger ตาม VC — VC2/VC3 รอ PV ก่อน · อื่น ๆ ทันที |
| D03 | รับไม่ครบ = Partial เสมอ ไม่มี exception |
| D04 | Auto-close PO เมื่อ GRN cumulative = PO qty |
| D05 | เปลี่ยน payment type ไม่ได้หลัง PO approve |
| D06 | 3-Way Match บังคับทุกกรณี (ยกเว้น VC7) |
| D07 | Close PO Balance trigger ที่ GRN เท่านั้น (ห้ามจาก Invoice/PV) |
| D08 | Deposit: inherit % + ปรับได้ที่ PO · remaining จ่ายหลัง GRN confirm |
| D09 | Installment: inherit + ปรับ % และ due_date ต่องวดได้ที่ PO |
| D10 | Partial Delivery: GRN กำหนดยอดจ่าย (GRN qty = Invoice qty = PV amount ต่อรอบ) |
| D11 | Credit overdue: เตือน ไม่ block |
| D12 | Unit Conversion (Subcontract) = Full Postpay lock อัตโนมัติ |
| D13 | Payment Voucher 2 types ใน document เดียว (`voucher_type` = payment / refund) |
| D14 | CN ต้องมาจาก vendor เท่านั้น (ออกเองไม่ได้ ต้องแนบไฟล์ CN ของ vendor) |
| D15 | Installment ≠ Partial Delivery (Installment = ส่งรอบเดียวแบ่งจ่าย N งวด · Partial = ส่งหลายรอบ) |

### E1.5 Business Edge Cases

RTV · Credit Note · Refund (VC2) · Close PO Balance · Cancel PO · Overdue (แจ้งเตือน ไม่ block) · Auto Close (Partial Delivery) · Installment + QC fail · Deposit + QC fail
→ ทุกอันมีวิธีจัดการเขียนไว้ใน `cube-master-knowledge/knowledge/03_value_streams/p2p-full-bible.md` §4 — **อ่านก่อนออกแบบ อย่าคิดเอง**

### E1.6 Inventory Locations (P2P)

`HOLD` (QC fail — **ไม่นับเป็น available stock**) · `QC` (กำลังตรวจ) · `DAMAGED` (sub ของ HOLD) · `PICK_FACE` (พร้อมหยิบ หลัง Putaway) · `RESERVE`

### E1.7 P2P ใน Central Plan — Bible แปลงเป็น Golden Rules แล้ว

Bible เป็น "ที่มา" · **Central Plan เป็นตัวบังคับใช้** — เวลาทำ feature ให้ยึด `GR-*` เพราะมี id ให้ trace เข้า AC/TC ได้

| เรื่องใน Bible | กลายเป็นกฎ |
|---|---|
| VC เลือกที่ PO Wizard Step 2 · เปลี่ยนหลัง approve ไม่ได้ | `GR-PO-01` (D01/D05) |
| Subcontract lock VC1 | `GR-PO-02` (D12) |
| GRN trigger ตาม VC | `GR-GRN-02` |
| รับเกิน tolerance → block ที่ GRN | `GR-GRN-03` + `GR-WHCFG-01..04` |
| รับขาด → partial / Close Balance | `GR-GRN-04` · `GR-PO-03` |
| QC inline → HOLD → RTV หรือ Adjustment | `GR-GRN-05` · `GR-RTV-01` |
| Close-Balance เกิดที่ GRN เท่านั้น (D07) | `GR-GRN-06` |
| 3-Way = PO eff = GRN = Invoice net | `GR-APINV-01/02` · `XR-07` |
| mismatch → Hold ห้ามไหลเข้า PV | `GR-APINV-04` |
| PV 2 voucher_type + refund ต้องอ้าง CN (D13) | `GR-PV-02` · `XR-05` |
| CN many-to-one + ต้องมีไฟล์ vendor CN (D14) | `GR-CN-01/02/11` |
| Direct Payment (VC7) | **ไม่ใช่ feature** — โหมดบนหัว AP Invoice `GR-APINV-08/09` |

**สิ่งที่ Central Plan เพิ่มจาก Bible:** cascade reversal (`XR-13`, `GR-GRN-08/09/10`) · tolerance 3 ชั้น (`XR-14`) · GR/IR accrual (`GR-GRIR-01..03`) · DN ฝั่งเจ้าหนี้รวมในเอกสาร CN/DN ใบเดียว (`GR-CN-05/06/07`) · landed cost แยก (`GR-APINV-11`)

---

## E2. S2C (Sales-to-Cash / Order-to-Cash) — **ไม่มี VS Bible แต่มี Golden Rules แล้ว**

> สถานะจริง: **ไม่มี O2C/S2C Bible** ใน `cube-master-knowledge` (ยังเป็น roadmap)
> **แต่** Central Plan v4.0.0 มี golden rules ฝั่งขายครบแล้ว → **ให้ยึด `GOLDEN_RULES.md` เป็นหลัก ห้ามเดา**
> สิ่งที่ยังขาดคือ **VC Catalog** (โครงสร้างการชำระเงินฝั่งขาย) — ยังไม่ถูกเคาะเหมือนฝั่ง P2P

### E2.1 โครงเอกสารฝั่งขาย (ตาม Central Plan)

```
Prospect (ลีด)  ──convert──▶ Customer
                                 │
                            Quotation ──▶ Sales Order
                                              │  confirm → จอง allocated ทันที (GR-SO-01)
                                              ├─▶ Picking → Packing → Delivery Note   (Outbound W6)
                                              │        └─ post DN = ตัดสต็อกจริง + ปลด allocated (GR-DN-03)
                                              ├─▶ AR Invoice / Tax Invoice            (W7)
                                              │        └─▶ Receipt Voucher (RV)       (W8)
                                              └─▶ Sales Return (RMA) ──▶ Credit/Debit Note (W7-W8)
```
Master ที่ต้องมีก่อน: **Product · UOM · Product Catalog · Price List · Sales Channel · Customer Segment · Payment Term · Sales Config · Warehouse · COA**

### E2.2 กฎฝั่งขายที่เคาะแล้ว (ห้ามออกแบบขัด)

| เรื่อง | กฎที่เคาะแล้ว | id |
|---|---|---|
| **จองของ** | SO confirm → จอง `allocated` **ทันที** ผ่าน Stock Reservation · ของไม่พอ **confirm ได้ จองเท่าที่มี** | GR-SO-01 · XR-02 |
| **วงเงินเครดิต** | **v1 ไม่คุมเครดิตลูกค้า** — ฝ่ายขายรับผิดชอบเอง · **ห้าม dev ใส่ block เองโดยไม่แก้ decision** | GR-SO-02 · GR-DN-04 (OQ-G07) |
| **แก้ SO หลัง confirm** | กระทบ qty/ราคา → revision log + re-check allocation | GR-SO-03 |
| **ยกเลิก SO** | ก่อนส่ง = ปลด allocation · หลังส่ง = ผ่าน RMA · หลัง invoice = ผ่าน CN — **ห้ามลบเอกสาร** | GR-SO-04 · XR-03 |
| **ส่งไม่ครบ** | ค้างเป็น **status partial บน SO line** — **ไม่มีเอกสาร backorder แยก** | GR-DN-02 · GR-PICK-03 (OQ-G09) · XR-08 |
| **ส่งเกิน** | DN อ้าง SO/pack — **ส่งเกิน SO ไม่ได้** | GR-DN-01 |
| **หยิบของ** | หยิบเฉพาะ available ตาม allocation — **ห้ามหยิบจาก HOLD/locked** · หยิบขาด = partial pick + เหตุผล | GR-PICK-01/03 · XR-06 |
| **แพ็ค** | qty pack ≤ qty picked ต่อ line — เกิน block · bundle ตาม BOM ต้อง conserve ส่วนประกอบครบ | GR-PACK-01/02 |
| **ตัดสต็อก** | **post DN = ตัดสต็อกจริง + ปลด allocated** · ยกเลิกหลัง post ต้อง reverse movement | GR-DN-03 |
| **วันส่ง** | **กรอกมือ ไม่มี ATP** | OQ-G08 |
| **invoicing policy** | AR Invoice ออก **ตาม qty ส่งจริง (DN)** — ยกเว้นมัดจำ/invoice ก่อนส่งตาม config | GR-ARINV-01 |
| **ขายบริการ ไม่มี SO/DN** | ออก **AR Invoice ตรงได้** ตาม config — เป็น**โหมดของเอกสารเดียวกัน ไม่ใช่ feature แยก** | GR-ARINV-05 |
| **Tax Invoice** | ออกแล้ว **แก้/ยกเลิกไม่ได้** — ปรับด้วย CN/DN เท่านั้น (ภาษีไทย) · validate → posting AR + ภาษีขายทันที | GR-ARINV-02/04 · XR-03 |
| **ยอดลูกหนี้** | คำนวณสด `Invoice − ΣRV − ΣCN` — **ไม่มี AR Ledger แยก ไม่เก็บยอด mutable** · aging ต้อง trace ถึงเอกสารต้นทางทุกบรรทัด | GR-ARINV-06/07/08 |
| **รับเงิน** | RV อ้าง invoice — รับขาด/เกิน → **ค้าง partial ห้าม auto-close** · reconcile bank ก่อนปิดงวด | GR-RV-01/02 · XR-08 |
| **ลูกค้าคืนของ** | RMA อ้าง DN/SO **คืนเกิน qty ที่ส่งไม่ได้** · ของคืนเข้า **QC ก่อน** (pass → available · fail → HOLD → ตัดด้วย Adjustment reason=ของเสีย) | GR-RMA-01/02 |
| **ลำดับเงินตอนคืนของ** | จ่ายแล้ว → CN + refund · ยังไม่จ่าย → CN ลดหนี้ · **เปลี่ยนสินค้า → RMA + DN รอบใหม่ ไม่แตะเงิน** | GR-RMA-03 · XR-05 |
| **CN จากการคืนของ** | ออกได้ **หลัง RMA รับของแล้วเท่านั้น** — ถ้าแค่ลดราคา (ลูกค้าเก็บของไว้) ไม่ต้องมี RMA | GR-CN-12/17 |
| **ราคา / ช่องทาง** | ทุก SO **ต้องระบุ Sales Channel** ใช้ resolve ราคา + แยกรายงาน · Price List แยกตามช่องทาง | GR-SCH-01 · GR-PLIST-01 |
| **แค็ตตาล็อก** | เสนอขาย/ตั้งราคาได้เฉพาะสินค้าใน **แค็ตตาล็อก active** — นอกแค็ตตาล็อกต้องขออนุมัติ | GR-PCAT-01 |
| **โปรโมชัน** | ซ้อนกันต้องมีกติกา stacking/priority ชัด — **ห้ามลดซ้ำเงียบ ๆ** | GR-PROMO-01 |
| **Quotation** | ราคา/ส่วนลดมาจาก pricelist + promotion · override ต้องมีสิทธิ์ + log · หมดอายุ (`valid_until`) → convert ไม่ได้ ต้อง revise | GR-QT-01/02 |
| **Prospect → Customer** | `converted` เป็น **terminal ห้าม reverse** (undo = สร้าง Prospect ใหม่ link Customer เดิม) · convert ผ่าน Create Modal handoff + prefill ตาม mapping ที่ lock | GR-PROSP-02 · GR-CUST-01 |

### E2.3 สิ่งที่ยัง**ไม่**ถูกเคาะฝั่ง S2C (ต้อง OQ กับ Strike)

VC Catalog ฝั่งขายยังไม่มี — candidate ที่ต้องเคาะก่อนออกแบบ flow การเงินฝั่งลูกค้า:

| VC candidate | คำถามที่ต้องเคาะ |
|---|---|
| **Cash Sale / หน้าร้าน** | รับเงินก่อนส่งของไหม · ออก tax invoice ทันทีไหม |
| **Credit Sale (N วัน)** | due date คำนวณจาก payment term ลูกค้าอย่างเดียวใช่ไหม (v1 ไม่คุมวงเงินอยู่แล้ว) |
| **Deposit / มัดจำ** | มัดจำ % · หัก invoice balance ยังไง (GR-ARINV-03 บอกว่าหักออกจาก balance) · trigger การจองของที่ไหน |
| **Prepay** | เงินเข้าก่อนถึงเริ่ม pick ไหม |
| **Installment** | แบ่งงวดรับเงินฝั่งขายมีไหม (P2P มี — ฝั่งขายยังไม่เคาะ) |
| **Consignment / ฝากขาย** | ตัด revenue ตอนไหน (ส่ง vs ขายจริง) |
| **Partial Delivery** | invoice ต่อรอบส่ง หรือรวมท้าย |

> **ห้ามเดา** — ถ้า feature ที่กำลังทำต้องใช้ VC ฝั่งขาย ให้ log เป็น OQ แล้วส่ง Strike

### E2.4 สิ่งที่ต้องเปิดดูก่อนออกแบบ feature ฝั่ง S2C

1. **`workflow_graph.json`** — node ของ feature + edge ออก/เข้า (เช่น Delivery Note → Sales Return / AR Invoice)
2. **`GOLDEN_RULES.md`** หัวข้อ feature นั้น + **XR-01..14**
3. **`DEVELOPMENT_PLAN.md`** — depends-on ครบหรือยัง · จำนวน rules (เผื่อ fix rounds)
4. **`FEATURE_REGISTRY.md`** — มีของเดิมไหม (★) และ contract เดิมคืออะไร
5. **Cross-module contract ที่มีแล้ว** (ดู F5) — `calcPromo(lines, doc)`, `lead_source`, `customerId`
6. **`BUILD_ORDER.md`** — feature ต้นน้ำใน wave ก่อนหน้าเสร็จหรือยัง

---

## E3. Value Stream อื่น ๆ

| VS | สถานะ knowledge |
|---|---|
| **P2P** Procure-to-Pay | ✅ Bible เต็ม + Golden Rules ใน Central Plan |
| **S2C / O2C** Sales-to-Cash | ⚠️ ไม่มี Bible — **แต่มี Golden Rules ครบใน Central Plan** (ขาดแค่ VC Catalog) |
| **R2R** Record-to-Report (การเงิน/บัญชี) | ⚠️ ไม่มี Bible — ส่วนตั้งหนี้/รับ-จ่ายเงินอยู่ใน Central Plan (Accounting/Finance domain) |
| **H2R** Hire-to-Retire (HR) | ⚠️ ยังไม่มี Bible |
| **I2C** Inventory-to-Consume | ⚠️ ยังไม่มี Bible |

**ถ้า AI ต้องทำงานกับ VS ที่ยังไม่มี Bible:** ห้ามเดา rule → ทำงานจาก **Central Plan (PART D)** + LANE_BRIEF เท่านั้น และ log ทุกช่องว่างเป็น OQ
**ลำดับความน่าเชื่อถือของกฎธุรกิจ:** LOCK (ใบเซ็น) > `GOLDEN_RULES.md` (GR/XR) > VS Bible > เอกสารเก่า > ความจำ

---

# PART F — กติกาเชิงเทคนิค (ห้ามละเมิด)

## F1. CI Standards — ⚠️ มี 2 ชุด ต้องรู้ว่าใช้ตัวไหน

### ✅ ปัจจุบัน (ใช้กับงานใหม่ทุกชิ้น) — **CUBE Warm Light** (`html-generator-v6`)

```
Ivory  (พื้น/ground)      : #FAF8F5
White  (card surface)     : #FFFFFF
Charcoal (text/sidebar)   : #111111   ← flat ไม่มี gradient
Red    (action/priority)  : #FF3B30
Orange (connection)       : #FF9A1F
Fonts                     : Satoshi (EN/ตัวเลข) + Noto Sans Thai (TH)
Icons                     : Lucide 0.469.0 (pinned, multi-CDN fallback)
```
> CSS variable ยังใช้ชื่อเดิมเพื่อ backward-compat: `--c-navy` = Charcoal · `--c-primary` = Red · `--c-teal` = Orange

### 🗄️ Legacy (เอกสารเก่ายังเขียนไว้ — **ห้ามใช้กับงานใหม่**) — CUBE NATIVE Navy

```
Navy #0B1D3A · Primary #0B5CFF · Teal #00A88E · Inter + Noto Sans Thai
```
> ใช้ได้เฉพาะกับไฟล์เก่าที่ยังไม่ rebrand · ถ้าเอามาปนกับงานใหม่ = **UX gate BLOCK**
> generator ที่ห้ามใช้แล้ว: `html-generator-v3` / `-v4` / `-25`

## F2. Iron Rules ของ HTML (สรุปหมวด — ตัวเต็มอยู่ใน `html-generator-v6/knowledge/iron-rules.md`)

ปัจจุบันมี **49 iron rules + Layout Integrity #50–62 + Component Contracts #63–68 + Kit Integrity #69 + Page Anatomy #70–73 + Contracts #74–77 + Blocks-First #78–80 + #81–82**

| หมวด | สาระ |
|---|---|
| Brand & CI (1–5) | token ล็อก · font stack · sidebar/topbar มาตรฐาน · Lucide เท่านั้น |
| Layout (6–10) | page header `.ph` · breadcrumb · stat row · filter bar อยู่ใน card · table footer = pagination + count |
| Drawer & Modal (11–15) | **Drawer 920px / .standard 680px** (ไม่มี 540 แล้ว) · create/edit = drawer ไม่ใช่ modal · modal ใช้เฉพาะ confirm |
| Table & Form (16–20) | table ≤ 8 คอลัมน์ · responsive grid · ซ่อน number spinner · toggle pattern |
| Code Quality (21–26) | ไอคอนต้องมี size class · **ห้าม console.log / TODO ค้าง** · ห้าม emoji สี · ห้าม dev-tool bar · `renderIcons()` หลัง render ทุกครั้ง |
| Behavior (29–37) | render preservation (scroll+focus) · fluid width · drawer button contract · CSV import convention · hint = tooltip ไม่ใช่ banner · search-select เมื่อข้อมูลเยอะ · no layout shift |
| Thai/List/State (38–45) | Thai vertical rhythm · empty state เสมอ · 1 ข้อมูล = 1 คอลัมน์ · row click = เปิด view (ไม่มีไอคอนดวงตา) · sticky header · inline validation · loading/submitting state |
| Placement (46) | **"ของทุกอย่างมีที่อยู่ตายตัว"** — ปุ่มสร้างขวาสุด · primary ใน drawer ล่างขวา · status pill หลังชื่อ 8px · แก้ไข→ลบ · ลบผ่าน confirm เสมอ · toast ขวาล่าง 3.5s |
| Stepper/Landing (47–48) | stepper กลางจาก skeleton · landing มี 3 variant เท่านั้น |
| Scrollbar (49) | minimal scrollbar 5px — ห้าม default |

**ข้อห้ามเด็ดขาดในทุก HTML:**
- ❌ Tailwind CDN
- ❌ browser storage (localStorage / sessionStorage)
- ❌ `console.log` / `TODO` ค้าง
- ❌ `data-lucide="undefined"` · ไอคอนไม่มี `w-/h-`
- ❌ `class="page-head"` (ใช้ `.ph`)

## F3. Validation Gate — บังคับทุกครั้งที่แตะ HTML

```bash
node --check <extracted-script>     # syntax ต้องผ่าน
./audit.sh                          # FAIL = 0 เท่านั้น
Playwright E2E / render capture     # ต้องมีหลักฐานภาพ ไม่มีภาพ = BLOCK
JS console errors                   # ต้อง = 0
```
- `export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers` ก่อนรัน capture script เสมอ
- ส่งไฟล์: เขียนที่ `/home/claude` → `rm -f` ปลายทาง → `cp` ไป `/mnt/user-data/outputs/` → `present_files` + verify md5
- **การแก้ไฟล์:** ใช้ Python raw-string patch script + assertion (`assert a in s`) — ปลอดภัยกว่าแก้มือเพราะมีข้อความไทย + JS template literal
- **ห้าม auto dead-code sweep** (เคยทำแล้วหน้าเว็บขาวทั้งหน้า)

## F4. Data & Schema Conventions

| กติกา | รายละเอียด |
|---|---|
| **Soft-reference policy** | master data ที่ใช้เป็น picker input → **ไม่ทำ FK cascade** · column nullable · บังคับแค่ format (soft) + uniqueness (blocking) |
| **Append-only audit log** | log ห้ามแก้/ลบ (WORM) |
| **Soft archive เท่านั้น** | **ห้าม hard delete** ทุกกรณี |
| **Data Classification** | ทุก field ต้องมีระดับ · default = Internal · field ที่เป็นต้นทุน/ราคาทุน = Confidential (mask ตาม role) |
| **DOA placeholder** | ทุก approval ต้องมี `approver_role / approved_by / approval_chain` + `// TODO: DOA engine` |
| **Engine registry** | logic ที่ใช้ซ้ำข้าม feature → แยกเป็น engine + register ที่ CUBIC · ห้าม copy logic |
| **Tenant scope** | ทุก query ต้องผ่าน RLS — ห้ามออกแบบ cross-tenant query |
| **ห้ามแต่งข้อมูล** | metric ที่ไม่มี data source จริง = defer + label "เฟสถัดไป" ห้าม mock เป็น "ของจริง" |

### Module Linkage Pattern (standalone vs integrated) — ใช้ทุก module ที่รันเดี่ยวได้

- มี **config "เชื่อม / ไม่เชื่อม"** ต่อปลายทาง (เช่น SO ↔ Delivery, SO ↔ Invoice, SO ↔ Payment)
- **เชื่อม** → สถานะ downstream อัปเดตอัตโนมัติ · field เป็น read-only/locked
- **ไม่เชื่อม** → ผู้ใช้เปลี่ยนสถานะ manual ได้เอง (dropdown/ปุ่ม)
- ตรงกับมาตรฐานสากล: Odoo invoicing policy (ordered/delivered) + app installed → auto / not installed → manual

## F5. Cross-Module Data Contract Pattern

handoff ข้าม module → นิยาม **contract ผอม ๆ** แล้วแต่ละฝั่ง mock อีกฝั่ง

ตัวอย่างที่มีแล้ว (ใช้อ้างอิงได้เลย):

| Contract | From → To | Payload / กลไก |
|---|---|---|
| Prospect Convert | Prospect → Customer | `{contact_name, contact_email, company_name, lead_source, prospect_ref_id, first_contact_date, notes}` + reverse link + `status='converted'` |
| Lead Origin | ทุก Customer | `lead_source`: field_sale / walk_in / referral / event / online_direct / manual (+5 prospect sources) |
| Promotion Calc | Promotion → Quotation/SO | `calcPromo(lines, doc)` → `{discount, gl_account}` |
| GL ↔ Promotion | GL Posting Group ↔ Promotion | ส่วนลดลง Sales Line Disc. Account (contra-revenue) ผ่าน `COA_ACCOUNTS` |
| Customer ref | Visit/Quotation/SO → Customer | อ้างด้วย `customerId` |
| BOM → Product/UOM | BOM → Product Master / UOM Master | FK `product_code` / `uom_code` · cost roll-up `std_material_cost = Σ(standard_cost × qty × (1+scrap%))` |

**Pattern ที่นำไปใช้ต่อได้ (handoff "from X"):**
prefill mapping + reverse link + origin/source field + section บนหน้า view ที่โชว์ที่มา + **ปุ่ม convert อยู่ฝั่ง upstream** (เช่น ปุ่ม convert อยู่ที่ Prospect ไม่ใช่ Customer)
---

# PART G — ลำดับการผลิตและการจัดไฟล์

## G1. กติกาการจัดไฟล์

1. **1 แชท = 1 module = 1 ไฟล์ HTML** (single-file SPA, hash routing `#/route` refresh-safe)
   - feature ที่อ้างถึงกันตรง ๆ อยู่ไฟล์เดียวกัน (เช่น Sales: Customer / Quotation / SO / Promotion / Visit)
   - ข้าม module → ใช้ data contract ผอม ๆ แล้ว mock
   - สัญญาณต้องแตกไฟล์ใหม่: ไฟล์แตะ ~6–8k บรรทัด หรือแก้ทีนึงหนัก/ช้า
2. **HTML 1 feature = chain v1 → v2 → vN ไม่แตกสาขา** (ห้าม branch)
3. **เอกสาร = ต่อ feature** (RIF → BRD → FRD → TC)
4. **Design system / knowledge = รวมศูนย์** (skill + project files)

## G2. Naming Convention

| ของ | รูปแบบ |
|---|---|
| QA test case HTML | `<ชื่อ feature ภาษาไทย> HTML Testcase.html` — ใช้ **ชื่อ feature ไม่ใช่รหัส** (เช่น `ทะเบียนเครื่องจักร HTML Testcase.html`) |
| ห้ามใช้ในชื่อไฟล์ | `&` → ใช้ "และ" แทน |
| ใบเซ็น new feature | `NF-SO-YYYY-NNNN_[feature]_Sign-off.docx` |
| ใบเซ็น enhancement | `ENH-SO-YYYY-NNNN_[feature]_Sign-off.docx` |
| Feature ID | `F-[MODULE]-[NN]` เช่น `F-OFM-12`, `F-GOODS-RECEIPT` |

## G3. แผนการผลิต — 41 features · 5 phases · 9 waves (Trade Core v4.0.0)

> ที่มา: `DEVELOPMENT_PLAN.md` + `BUILD_ORDER.md` ใน Central Plan
> **ลำดับมาจาก dependency `data`/`config` เท่านั้น** — สลับได้ภายใน phase เดียวกัน **แต่ห้ามข้าม phase**
> `Rules` = จำนวน golden rules (ในวงเล็บ = severity `block` ที่ **ต้อง map เป็น AC ใน BRD**)
> ✅ = มีของเดิมแล้ว (ต้องระบุใน brief ว่าเป็น ENH กัน Hard Stop สร้างซ้ำ)

### Phase 0 — Rework ของเดิม (ENH ไม่ใช่ feature ใหม่) — ต้องทำก่อน Phase 1

| # | งาน | Feature เดิม | เหตุผล |
|---|---|---|---|
| 0.1 | เพิ่ม lot / serial / expiry dimension | `F-INVENTORY` | OQ-G12 บังคับทั้งเส้น — schema ต้องรองรับก่อนทุก movement |
| 0.2 | เพิ่ม damage reason code + GL mapping | `F-STOCK-ADJUSTMENT` | OQ-G05 ใช้ Adjustment แทนเอกสาร Scrap |
| 0.3 | Reserve on confirm + partial line status | `F-SALES-ORDER` | OQ-G04 จองทันที · OQ-G09 ค้างส่งเป็น status |
| 0.4 | เพิ่ม field ค่าเผื่อรับเกิน/ขาด ต่อสินค้า | `F-PRODUCT` | OQ-G01a — tolerance ต้องมีชั้น material master |
| 0.5 | เก็บ BRD / FRD / Testcase ให้ครบ | `F-CUSTOMER` · `F-QUOTATION` · `F-SALES-ORDER` · `F-PROMOTION` | มีแค่ HTML — Phase ถัดไปจะอ้าง SO เป็น contract |

### Phase 1 — Masters & Config · 15 features (W1)
*ปลดล็อก: เปิดใช้ Inventory ได้ · เอกสารทุกใบมี master + บัญชีให้อ้าง*

| Feature | ไทย | Domain | Status | Depends on | Rules |
|---|---|---|---|---|---|
| `F-PRODUCT` | ข้อมูลสินค้า/วัสดุ | Master | ✅ | — | 4 (4) |
| `F-UOM` | หน่วยวัด | Master | ✅ | — | 2 (2) |
| `F-BOM` | สูตร/ชุดสินค้า | Master | ✅ | — | 2 (1) |
| `F-COA` | ผังบัญชี | Accounting | ต้องทำ | — | 3 (3) |
| `F-PRODUCT-CATALOG` | แค็ตตาล็อกสินค้า | Master | ต้องทำ | — | 2 (1) |
| `F-SALES-CHANNEL` | ช่องทางการขาย | Sales | ต้องทำ | — | 2 (1) |
| `F-PAYMENT-TERM` | เงื่อนไขการชำระเงิน | Master | ต้องทำ | — | 2 (2) |
| `F-VENDOR` | ข้อมูลผู้ขาย | Purchase | ต้องทำ | — | 1 (1) |
| `F-VENDOR-PRICE-LIST` | บัญชีราคาผู้ขาย | Purchase | ต้องทำ | F-VENDOR | 1 (0) |
| `F-WAREHOUSE` | คลังและตำแหน่งจัดเก็บ | Warehouse | ต้องทำ | — | 2 (2) |
| `F-WAREHOUSE-CONFIG` | ตั้งค่าคลังสินค้า | Warehouse | ต้องทำ | — | 5 (5) |
| `F-PURCHASE-CONFIG` | ตั้งค่าจัดซื้อ | Purchase | ✅ | — | 1 (1) |
| `F-CUSTOMER-SEGMENT` | กลุ่มลูกค้า | Sales | ต้องทำ | — | 1 (0) |
| `F-PRICE-LIST` | บัญชีราคาขาย | Sales | ต้องทำ | F-PRODUCT-CATALOG · F-SALES-CHANNEL | 1 (0) |
| `F-SALES-CONFIG` | ตั้งค่าการขาย | Sales | ต้องทำ | — | 1 (0) |

### Phase 2 — Inventory Core · 5 features (W2)
*ปลดล็อก: สต็อกเดินได้จริง · `allocated` มีเจ้าของ · ทุก movement พก lot ได้*

| Feature | ไทย | Domain | Status | Depends on | Rules |
|---|---|---|---|---|---|
| `F-INVENTORY` | สินค้าคงคลัง (รวม lot/serial/expiry) | Inventory | ✅ | F-STOCK-RESERVATION · F-WAREHOUSE | 11 (11) |
| `F-STOCK-ADJUSTMENT` | ปรับยอดคงคลัง | Inventory | ✅ | F-COA | 6 (5) |
| `F-STOCK-RESERVATION` | การจองสินค้า | Inventory | ต้องทำ | — | 3 (3) |
| `F-STOCK-TRANSFER` | การโอนย้ายสินค้า | Warehouse | ต้องทำ | F-WAREHOUSE | 2 (1) |
| `F-STOCK-COUNT` | การนับสินค้า | Warehouse | ต้องทำ | F-WAREHOUSE | 3 (2) |

### Phase 3 — Front Documents · 8 features (W3 ขาย ‖ W4 ซื้อ)
*ปลดล็อก: มี SO เป็น contract ให้งานส่งของและ invoice อ้าง · มี PO ให้รับของและตั้งหนี้*

| Feature | ไทย | Domain | Status | Depends on | Rules |
|---|---|---|---|---|---|
| `F-PROSPECT` | ผู้สนใจ (ลีด) | Marketing | ✅ | — | 2 (1) |
| `F-CUSTOMER` | ข้อมูลลูกค้า | Sales | ✅ | F-CUSTOMER-SEGMENT · F-PAYMENT-TERM | 1 (1) |
| `F-QUOTATION` | ใบเสนอราคา | Sales | ✅ | F-PRICE-LIST · F-PRODUCT-CATALOG | 2 (0) |
| `F-SALES-ORDER` | คำสั่งขาย | Sales | ✅ | F-SALES-CHANNEL · F-SALES-CONFIG | 4 (3) |
| `F-PROMOTION` | โปรโมชัน | Sales | ✅ | — | 1 (0) |
| `F-PR` | ใบขอซื้อ | Purchase | ต้องทำ | — | 3 (2) |
| `F-CP` | ใบเทียบราคา | Purchase | ต้องทำ | F-PR · F-VENDOR-PRICE-LIST | 2 (1) |
| `F-PO` | ใบสั่งซื้อ | Purchase | ต้องทำ | F-CP · F-PAYMENT-TERM · F-PR · F-VENDOR | 6 (5) |

### Phase 4 — Warehouse Operations · 5 features (W5 Inbound ‖ W6 Outbound)
*ปลดล็อก: ของเข้าคลังได้จริงจากเส้นซื้อ · ส่งของได้จริง + มี DN ให้ออก invoice ตามส่งจริง*

| Feature | ไทย | Domain | Status | Depends on | Rules |
|---|---|---|---|---|---|
| `F-GOODS-RECEIPT` | ใบรับสินค้า (GRN) ⚠️ | Warehouse | ต้องทำ | F-PO · F-WAREHOUSE · F-WAREHOUSE-CONFIG | **12 (11)** |
| `F-PUTAWAY` | จัดเก็บเข้าตำแหน่ง | Warehouse | ต้องทำ | — | 3 (3) |
| `F-PICKING` | การหยิบสินค้า | Warehouse | ต้องทำ | — | 3 (3) |
| `F-PACKING` | การแพ็คสินค้า | Warehouse | ต้องทำ | F-PICKING | 2 (1) |
| `F-DELIVERY-NOTE` | ใบส่งของ | Warehouse | ต้องทำ | F-PACKING | 4 (3) |

### Phase 5 — Billing · Exceptions · Money · 8 features (W7–W9)
*ปลดล็อก: เส้นซื้อ-ขายเดินครบรอบ · cascade reversal ครบเส้น · จ่าย/รับเงินได้ทุก VC*

| Feature | ไทย | Domain | Status | Depends on | Rules |
|---|---|---|---|---|---|
| `F-AP-INVOICE` | ใบแจ้งหนี้เจ้าหนี้ (รวม 3-Way + โหมดจ่ายตรง) | Accounting | ต้องทำ | F-COA · F-GOODS-RECEIPT · F-PAYMENT-TERM · F-PO | **15 (15)** |
| `F-AR-INVOICE` | ใบแจ้งหนี้/ใบกำกับภาษี | Accounting | ต้องทำ | F-COA · F-DELIVERY-NOTE · F-PAYMENT-TERM | 9 (7) |
| `F-SALES-RETURN` | รับคืนจากลูกค้า (RMA) | Warehouse | ต้องทำ | F-DELIVERY-NOTE | 3 (3) |
| `F-RETURN-TO-VENDOR` | คืนของผู้ขาย | Warehouse | ต้องทำ | — | 4 (4) |
| `F-CREDIT-DEBIT-NOTE` | ใบลดหนี้/เพิ่มหนี้ (4 แบบในใบเดียว) | Accounting | ต้องทำ | — | **19 (19)** |
| `F-RECEIPT-VOUCHER` | ใบสำคัญรับ | Finance | ต้องทำ | F-AR-INVOICE · F-COA | 2 (1) |
| `F-GRIR-ACCRUAL` | บัญชีพักรับของ-รอใบแจ้งหนี้ | Accounting | ต้องทำ | F-COA | 3 (2) |
| `F-PAYMENT-VOUCHER` | ใบสำคัญจ่าย | Finance | ต้องทำ | F-AP-INVOICE · F-COA · F-CREDIT-DEBIT-NOTE | 6 (6) |

### ⚠️ จุดระวังของแผน

- **Phase 1 ห้ามข้าม** — `F-PRODUCT` + `F-UOM` + `F-WAREHOUSE` ไม่ครบ = เปิดใช้ Inventory ไม่ได้ (`GR-INV-08`, `GR-WH-02`) · **COA ไม่ครบ = post บัญชีไม่ได้** (`GR-COA-03`)
- **`F-STOCK-RESERVATION` ต้องมาก่อน `F-PICKING`** — เป็นเจ้าของ `allocated` แต่ผู้เดียว (XR-02)
- **`F-GOODS-RECEIPT` หนักสุดในแผนที่** — รับเกิน/ขาด · QC · รับลอย · reverse · accrual · Close Balance รวมที่เดียว
- **`F-AP-INVOICE` (15) / `F-CREDIT-DEBIT-NOTE` (19)** — rules หนักสุดในระบบ เผื่อ fix rounds มากกว่าปกติ
- **Cascade reversal (XR-13)** — `F-GOODS-RECEIPT` · `F-AP-INVOICE` · `F-GRIR-ACCRUAL` · `F-PAYMENT-VOUCHER` **ต้องออกแบบ reversal ร่วมกันตั้งแต่แรก** ไม่ใช่ค่อยไปคิดตอน Phase 5
- **Wave 3 ✅ ทั้ง wave** — มี HTML แล้ว งานคือเก็บ BRD/FRD/TC ให้ครบ + ผูก Sales Channel และ Stock Reservation
- ทุก feature: **rule `severity=block` ทุกข้อต้องกลายเป็น AC · edge ออกทุกเส้นต้องมี hook ใน HTML**

## G4. Source of Truth — อยากรู้อะไร เปิดอะไร

| อยากรู้ | เปิด |
|---|---|
| **กฎธุรกิจของ feature (บังคับใช้) ⭐** | `Central_Plan/GOLDEN_RULES.md` — GR-* ราย feature + XR-01..14 |
| **ความสัมพันธ์ feature / dependency / edge** | `Central_Plan/workflow_graph.json` (+ `WORKFLOW_MAP.html` ดูภาพ) |
| **ลำดับ phase/wave + depends-on + จำนวน rules** | `Central_Plan/DEVELOPMENT_PLAN.md` · `Central_Plan/BUILD_ORDER.md` |
| universe map / working rules / master process | `CUBE_4.0_PROJECT_INSTRUCTIONS.md` |
| feature ทั้งหมด + สถานะ BA + contract | `FEATURE_REGISTRY.md` |
| architecture/governance ลึก · VS/VC/Path · glossary | `CUBE_KNOWLEDGE_SNAPSHOT.md` |
| concept ล่าสุด / VS Bible เต็ม / รายละเอียด skill | skill `cube-master-knowledge` (read+write ผ่าน chat) |
| **version pin ของ skill ทุกตัว ⭐** | `cube-master-knowledge/knowledge/04_skills/workflow-master-wf01-06.md` |
| checklist สถานะรันรายตัว | `.../04_skills/wf01-run-list.md` |
| สถานะ **dev** สด | Google Sheet `CUBE 4.0 List` ผ่าน `cube-master-tracking-generator` (**ดึง live ทุกครั้ง ห้ามใช้เลขเก่า**) |
| CI / component / iron rules ตอน build HTML | skill `html-generator-v6` |

## G5. หลังทำ feature เสร็จ — งานประจำที่ต้องทำเสมอ

1. อัปเดต **`FEATURE_REGISTRY.md`** (วงเล็บ BA status ท้าย feature + contract ใหม่)
2. แจ้ง **พี่เบิร์ด** ให้อัปเดต Google Sheet (H·F·Q + feature registry ฝั่ง dev)
3. แจ้ง **Architect** ถ้ามี engine candidate ใหม่ (register เข้า CUBIC)
4. เคลียร์ **OQ** ที่ค้างกับ Strike / Chin
5. อัปเดต run list: `"อัพเดต run list — F-XXX done"`

### งานค้างระดับแผน (จาก `_KNOWLEDGE_SYNC.md` — ยังไม่เคลียร์)

- [ ] อัปเดต `FEATURE_REGISTRY.md` ให้เป็นชุด v4.0.0 (41 features + 9 waves + decision log)
- [ ] แจ้งพี่เบิร์ด: สถานะ `F-PURCHASE-CONFIG` ขัดกัน (Bible ว่า done · registry ว่า —) + อัปชีท H·F·Q
- [ ] คุย Accounting: ผัง COA + บัญชีพัก GR/IR + mapping reason code → GL ของ Stock Adjustment
- [ ] ยืนยันกับ Strike: domain split Accounting/Finance + การรวม CN/DN เป็นใบเดียว
- [ ] ยืนยัน OQ-G01a / G03a ปิดแล้วจริง (GOLDEN_RULES ว่าปิด · BUILD_ORDER ว่าค้าง) ก่อนเริ่ม `F-GOODS-RECEIPT`
- [ ] ออก ENH ย้อนกลับ 4 ตัว: `F-INVENTORY` · `F-STOCK-ADJUSTMENT` · `F-SALES-ORDER` · `F-PRODUCT` (ดู G3 Phase 0)

**Convention วงเล็บสถานะ BA:** `(—)` ยังไม่ทำ · `(H)` มี HTML · `(H·B·F·Q)` ครบ HTML+BRD+FRD+QA · `(H @sales)` อยู่ในไฟล์ sales-module.html · `⟂` feature ที่เราเพิ่มเอง ยังไม่อยู่ในชีท

---

# PART H — Master Process ระดับองค์กร (บริบทรอบ ๆ งาน BA)

1. **Dev หลัก 14 step:** Requirement (RIF) → Vibe HTML → BRD → FRD → Test Case → Pack ส่ง Dev → Full Stack Analyze → Tri-Stream Plan + API Contract (locked) → FE/BE Execute → INT wire-up (zero mock) → Dev Review & Fix → QA Test → Bug loop จนผ่าน
2. **Manual + Demo Video:** feature ผ่าน QA → Demo Script → อัดวิดีโอ → แปลงเป็นคู่มือ (`module-manual-builder`) → QA review → ตัดต่อ → publish คลังความรู้
3. **Demo & Training:** Demo env + script → Demo ลูกค้า → Training Plan → Key User Training → UAT → End User Training → Follow-up
4. **Onboarding ลูกค้า (6 phase ~4 สัปดาห์):** Contract → Provision → Data Prep → Import/Config (Sandbox) → UAT + Sign-off → Go-live → Hypercare 30 วัน
   - CSV dependency chain: `organization → employee → user → user_roles → menu_setting → feature_config` (**dry-run validate ก่อน commit เสมอ**)

---

# PART I — Glossary (ย่อ)

**P2P:** PR (ใบขอซื้อ) · PO (ใบสั่งซื้อ) · GRN/GR (ใบรับของ) · AP · AP Invoice · PV (ใบสำคัญจ่าย, `voucher_type` payment/refund) · CN (ใบลดหนี้) · RTV (คืน vendor) · 3-Way Match · PO Effective Qty · Invoice Net · Close PO Balance · Direct Payment · HOLD location

**S2C/O2C:** Quotation · SO · Delivery Note · AR Invoice / Tax Invoice · RV (ใบสำคัญรับ) · RMA (รับคืนลูกค้า) · Credit Note

**Inventory:** BOM · UoM · FIFO/Avg/Standard · Item Master (ถังเดียวแยก type) · Item Type (raw/finished/consumable/service/asset/packaging)

**Architecture:** Identity Hub · RLS · AIR Schema (Architecture Index Registry) · CUBIC Registry · UBA + Smart Code · Data Classification

**Governance:** DOA · RBAC/User Access · Feature-DOA Pairing · ENC · PDPA · Restricted Resources

**Process:** VS · VC · Path · CL · SOP · SOW · Zigzag (A→B→C) · Edge Case

**BA artifacts:** RIF (Requirement Intake Format) · BRD · FRD (Pack Mode = แยกไฟล์ UI/API/LOGIC/DB/RULES/TESTS) · UI Brief · TC · SCN · DevPack · LOCK-XX (scope lock) · OQ (Open Question) · LANE_BRIEF · Central Plan (workflow_graph + GOLDEN_RULES + BUILD_ORDER)

**Report Framework v2 (4 กลุ่ม):** CL = Closing (P&L, ภ.พ.30) · PF = Performance (KPI/trend) · OP = Operation (SLA/backlog realtime) · TX = Transaction (รายการที่แผนกสร้าง)

**Org (WKN model):** Tier M (บริหาร M1–M7) · Tier S (วิชาการ S1–S6) · Tier E (ปฏิบัติการ E8–E9) · career path M5 ↔ S1

---

# PART J — Boundaries + บทเรียนที่ต้องไม่ทำซ้ำ

## J1. ทำ / ไม่ทำ

| ✅ ทำ | ❌ ไม่ทำ |
|---|---|
| อ่าน `cube-master-knowledge` + version pin ก่อนตอบ concept ลึก | ตอบจากความจำล้วน |
| 1 แชท = 1 module = 1 ไฟล์ | ยัดทุก module ไฟล์เดียว |
| validate + audit = 0 ทุกเทิร์นที่แตะ HTML | ส่งงานโดยไม่ตรวจ |
| pre-DOA placeholder + comment | hardcode rule อนุมัติ |
| ดึง tracking live ทุกครั้ง | ใช้ตัวเลข progress เก่า |
| ยึด `GOLDEN_RULES.md` เป็นกฎบังคับ (อ้าง GR/XR id) | เดา rule ธุรกิจเอง / คิดแทนลูกค้า |
| เช็ค D5 ก่อนเปิด feature ใหม่ | สร้าง feature ที่ถูกยุบไปแล้ว |
| log สิ่งที่ไม่ชัดเป็น OQ | เดาแล้วเขียนลงเอกสาร |
| defer metric ที่ไม่มี data source | แต่งตัวเลขให้ดูสวย |
| surgical patch + assertion | auto dead-code sweep |
| ภาษาไทย กระชับ | ยาวเกิน / ฟอร์แมตเกินจำเป็น |
| ไม่ฝัง credential ในเอกสาร | เก็บ password เป็น plaintext |

## J2. บทเรียนจริงที่เจ็บมาแล้ว

| เหตุการณ์ | บทเรียน |
|---|---|
| 7 skill จำเวอร์ชันกันเอง → v4/v5/-25 ปนกัน CI ชนกัน | **version pin ที่เดียว** — ห้ามจำเวอร์ชันเอง |
| HTML ผ่าน audit แต่หน้าตาเบี้ยว | audit ผ่าน ≠ สวย → เพิ่ม Layout Integrity + **Render Gate บังคับหลักฐานภาพ** |
| skeleton ป่วยเอง (56 spacing / 14 fonts เพี้ยน) | **Kit Integrity** — BASE-KIT verbatim ห้ามแก้ · checkpoint ทุก phase |
| auto dead-code sweep → หน้าขาวทั้งหน้า | แก้แบบ surgical + assert เท่านั้น |
| feature สร้างซ้ำเพราะไม่รู้ว่ามีของเดิม | brief ต้องระบุ ★ ของเดิม + อ้าง artifact เดิม |
| เอกสารเพี้ยนหลัง vibe HTML | vibe หลัง DevPack → **ต้องรัน `html-to-frd-sync` เสมอ** |
| สร้าง feature ที่ถูกยุบไปแล้ว (Direct Payment / AR Ledger / Lot Tracking แยก) | เช็ค **D5 โครงสร้างที่ถูกยุบ** ก่อนเปิดงานเสมอ |
| กฎกระจายอยู่หลายที่ ทีมจำคนละแบบ | รวมเป็น **GOLDEN_RULES.md ที่เดียว** generate จาก graph · ห้ามแก้มือ |
| reverse เอกสารต้นทางแล้วปลายน้ำค้าง | **cascade reversal (XR-13)** — ออกแบบ reversal ของ GRN/Invoice/GR-IR/PV ร่วมกันตั้งแต่แรก |
| ตรวจไม่ได้แล้วปล่อยผ่าน | **NOT-CHECKED = BLOCK** |

---

# PART K — Checklist สำหรับ AI ที่มาช่วยผลิต feature

## K0. ก่อนเริ่ม — ต้องมีของครบ
- [ ] LANE_BRIEF ของ feature นี้ (ระบุ scope + ✅ ของเดิม → ถ้ามีของเดิมต้องทำเป็น ENH ไม่ใช่สร้างใหม่)
- [ ] Central Plan ครบชุด (`workflow_graph.json` + `GOLDEN_RULES.md` + `DEVELOPMENT_PLAN.md` + `BUILD_ORDER.md`)
- [ ] อ่าน node + edge เข้า/ออก ของ feature นี้ใน graph แล้ว
- [ ] list `GR-*` ของ feature นี้ + `XR-01..14` ออกมาแล้ว (แยก block / warn)
- [ ] เช็คว่า feature นี้ไม่ใช่ของที่ถูกยุบไปแล้วใน v4.0.0 (ดู D5)
- [ ] LOCK-XX จากใบเซ็น (หรือ LD/AC/OQ-G ถ้าเป็นงาน internal)
- [ ] `depends_on` ทุกตัว (`config`/`data`) เสร็จแล้ว — phase ก่อนหน้าไม่ข้าม
- [ ] OQ ที่ blocking เคาะจบแล้ว

## K1. ตอนทำ HTML
- [ ] ใช้ `html-generator-v6` (Warm Light) เท่านั้น
- [ ] อ่าน NODE_BRIEF + GOLDEN_RULES ก่อนวาง layout
- [ ] Drawer 920 / .standard 680 · create-edit = drawer ไม่ใช่ modal
- [ ] ทุก approval → pre-DOA placeholder + `// TODO: DOA engine` (XR-09)
- [ ] **edge ออกทุกเส้นใน graph มี hook ใน UI** (เช่น GRN ต้องมีทางไป Putaway / RTV / GR-IR)
- [ ] กฎที่ผูกกับหน้าจอ reflect จริง (partial ต้องเห็นสถานะ · HOLD ไม่โผล่ใน available · config หลายชั้นต้องแสดงว่าใช้ชั้นไหน)
- [ ] empty / loading / error state ครบทุกหน้า
- [ ] `node --check` ผ่าน · `audit.sh` FAIL = 0 · JS console error = 0
- [ ] มีหลักฐานภาพ (screenshot / Playwright) ก่อนบอกว่า "เสร็จ"

## K2. ตอนทำเอกสาร
- [ ] FRD สกัดจาก HTML final (ไม่ใช่เขียนล่วงหน้า) แต่ Design Authority = FRD
- [ ] **`GR-*` severity=block ทุกข้อ → กลายเป็น AC** (ไม่มี AC = coverage gate BLOCK) และอ้าง id ได้
- [ ] `XR-01..14` ที่เกี่ยวข้องถูกอ้างในเอกสาร ไม่ตกหล่น
- [ ] Coverage Manifest: AC / BR / EC / XT / LOCK ครบ cross-check ก่อนเขียน test case
- [ ] จำนวนเคส + จำนวน step ตรงกันเป๊ะระหว่าง MD ↔ HTML ↔ testset
- [ ] ทุก edge/exception path ใน graph มี hook ใน UI และมี test case
- [ ] ไม่มี rule ไหนที่เขียนใน BRD/FRD แล้วไม่ปรากฏบนหน้าจอ (และกลับกัน)

## K3. ก่อนส่ง
- [ ] ไฟล์อยู่ `/mnt/user-data/outputs/` + `present_files` + verify md5
- [ ] อัปเดต `FEATURE_REGISTRY.md`
- [ ] แจ้งพี่เบิร์ด (Google Sheet) · แจ้ง Architect (engine ใหม่) · เคลียร์ OQ กับ Strike/Chin
- [ ] list "งานค้างที่ต้องทำมือ" ท้าย session ทุกครั้ง

---

## ภาคผนวก — Skill Pipeline (ชื่อ skill ที่ทีมใช้)

| งาน | skill (ปัจจุบัน) |
|---|---|
| วางแผน module ก่อนเริ่ม | `plan-module-workflow-mapper` |
| ใบเซ็น scope | `newfeature-signoff-generator` / `enhancement-signoff-generator` |
| บรีฟเข้าเลน | `lane-brief-generator` |
| Requirement → RIF | `requirement-intake-formatter` |
| HTML prototype | **`html-generator-v6`** |
| ตรวจ UX/CI | `qc-ux-html-checker` |
| ตรวจ scope ครบ | `qc-coverage-checker` |
| BRD | `brd-generator-full` |
| FRD | **`frd-generator-v6`** |
| Test case (AI) | `ai-testcase-md-generator` |
| Test case (คนทดสอบ) | `qa-friendly-html-generator` → `qa-html-to-ai-testset` |
| UI Brief ให้ dev | `html-ui-brief` |
| Drift check หลัง vibe | `html-to-frd-sync` |
| Enhancement | `enc-doc-generator` |
| Orchestrator ทั้งเลน | `feature-lane-runner` |
| Knowledge base | `cube-master-knowledge` (read/write) |
| Tracking สด | `cube-master-tracking-generator` |
| VS Bible | `vs-bible-intake` → `vs-bible-md-updater` → `vs-bible-to-brief-expander` |

**ห้ามใช้แล้ว:** `html-generator-v3/-v4/-25` (Navy) · `frd-generator-v5/-25` · `output-checker` · `uba-taxonomy-register` · `dev-brief-generator` (ใช้ `html-ui-brief` แทน)

---

**เอกสารนี้เป็นภาพรวม — ค่าที่ต้องเป๊ะให้ยืนยันกับ version pin และ skill เสมอ**
**ถ้าเจอข้อขัดแย้ง ลำดับความน่าเชื่อถือ:**
- **กฎธุรกิจ:** LOCK (ใบเซ็น) > `GOLDEN_RULES.md` (GR/XR) > VS Bible > project files > เอกสารนี้ > ความจำ
- **เวอร์ชัน/เครื่องมือ/CI:** version pin (`workflow-master-wf01-06.md`) > skill file > project files > เอกสารนี้ > ความจำ
