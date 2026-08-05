---
name: brd-generator-full
description: >
  สร้าง BRD ฉบับสมบูรณ์จาก RIF ในรอบเดียวจบ — SOW3.2 ของ WF-01 ครอบคลุม Draft → Enrich →
  Flexibility → Data Entity → Value Stream Impact → Quality Gate พร้อม COSO + Security Preset +
  Scope Lock สืบทอดจากใบเซ็น (§3.4) + Downstream Impact (§12.1) ★ v2.2 HTML-first: Fresh Mode
  รับ HTML (ผ่าน ux/coverage gate) เป็น input ร่วม — Screen Inventory สกัดจากหน้าจอจริง
  + Lane Mode (no-ask) สำหรับ feature-lane-runner + Conflict Priority (LOCK > RIF business intent
  > HTML หน้าจอจริง) ใช้เมื่อ user พูดถึง "สร้าง BRD", "เขียน BRD", "BRD จาก RIF", "BRD Full",
  "brd-generator-full", "BRD ฉบับสมบูรณ์", "ทำ BRD จาก Intake", "BRD pipeline", "SOW3.2"
  รองรับ New Feature / Enhancement / Bug Fix / Config + Revision Mode (sync HTML กลับ BRD)
  Input: RIF v2.1 + HTML จาก html-generator-v6 (แนะนำ) · Output: BRD .md + .docx + AI Review
  Pipeline: RIF → HTML(v6) → BRD → frd-generator-v6 · Version pin: workflow-master-wf01-06.md
---

# BRD Generator (Full Pipeline) — v2.2 HTML-first Edition

**ตำแหน่งใน workflow:** WF-01 · SOP3 · SOW3.2 (Actor: BA)
**DoD:** 1) BRD .md + .docx ครบ  2) AI Review ไม่มี Critical issue  3) Business Rules ติด flexibility tag ครบ
**v2.1 (2026-07-06):** ถอด Design Authority ออก (ย้ายไป FRD) → BRD เป็นเอกสาร business ล้วน + เพิ่ม Value Stream Impact (§12.1), Scope Lock (§3.4), ตัวชี้วัดบังคับวัดได้ (§2.3), Flexibility attribution (§9.5)
**v2.2 (2026-07-25) HTML-first:** Fresh Mode รับ HTML เป็น input ร่วม → Step 1.5 เปลี่ยนจาก "แต่ง" เป็น "สกัด" + Mode Detection แก้ให้ RIF+HTML = Fresh + Lane Mode (no-ask) + Conflict Priority มีที่ให้ HTML + pin v6

สร้าง BRD ฉบับสมบูรณ์จาก RIF ใน skill เดียวจบ — รวม 6 skills เดิมเข้าด้วยกัน
พร้อม Philosophy rules embedded: COSO + 78 Security Controls + SLA/KPI/Threshold

## 🔗 Document Chain Position

```
WF-01 v2 (HTML-first lane — ปัจจุบัน):
RIF.md → html-generator-v6 → [ux gate + coverage gate ผ่าน]
   ↓ (RIF + HTML เข้าคู่กัน)
[brd-generator-full]  ← Skill นี้ (Fresh Mode, HTML-first)
   ↓
BRD_[feature].md + .docx
   ↓
frd-generator-v6 → TC & Scenario → DevPack

Post-lane (คน vibe HTML หลังได้ DevPack):
HTML v2 + BRD v1 → [brd-generator-full] (Revision Mode) → BRD v2 + Changelog
```

## 🔀 2 Modes

| Mode | ใช้เมื่อ | Input หลัก |
|---|---|---|
| **Fresh Mode** (default) | สร้าง BRD ใหม่ตั้งแต่ต้น | RIF.md + HTML (แนะนำ — HTML-first) |
| **Revision Mode** ⭐ | Sync HTML v2 (ที่ vibe แล้ว) กลับ BRD | HTML v2 + BRD v1 |

---

## 📥 Input

### 🆕 Mode Detection (Auto)

Skill auto-detect mode จาก input ที่ user แนบ:

```
ถ้า input มี (HTML + BRD เก่า) หรือ user พูด "revise", "sync HTML กลับ BRD", "vibe เสร็จแล้ว", "post-pack revision"
   → Revision Mode
ถ้า input มี (RIF + HTML) โดยไม่มี BRD เก่า          ← เคสหลักของ WF-01 v2
   → Fresh Mode (HTML-first)
ถ้า input มี RIF อย่างเดียว หรือ raw requirement
   → Fresh Mode (doc-only — ใช้ได้แต่ Screen Inventory จะเป็นการคาดการณ์)
ถ้าคลุมเครือ:
   → Interactive: ถาม user 1 รอบ
   → Lane Mode (รันใต้ feature-lane-runner): ห้ามถาม — default = Fresh Mode + log ลง _LANE_LOG
```

**Lane Mode คืออะไร:** เมื่อถูกเรียกจาก `feature-lane-runner` (หรือ user บอกว่า "one-shot/ห้ามถาม")
ทุกจุดที่เขียนว่า "ถาม user" ให้เปลี่ยนเป็น **ใช้ default + log** — ห้ามหยุดรอคำตอบ
ยกเว้นชน Scope Lock ซึ่งเป็น Hard Stop ของเลนอยู่แล้ว

---

### 🆕 Revision Mode (เพิ่ม v1.1)

**ใช้เมื่อ:** vibe HTML แก้แล้ว ต้อง sync drift กลับ BRD เพื่อให้ chain (FRD/HTML/QA) regenerate ตรงตาม intent ใหม่

**Required Input:**
| # | ไฟล์ | อ่านเพื่อ |
|---|---|---|
| 1 | `BRD_[feature].md` (v1) | base ของ BRD เดิม + Changelog history |
| 2 | HTML file (v2 — ที่ vibe แล้ว) | source of new business intent |

**Optional Input:**
| # | ไฟล์ | อ่านเพื่อ |
|---|---|---|
| 3 | Diff notes (text) | user อธิบายว่าอะไรเปลี่ยน (ถ้าไม่บอก skill จะ detect เอง) |
| 4 | HTML v1 (ของเก่า — ก่อน vibe) | ช่วย diff แม่นขึ้น (ถ้าไม่มี ใช้ BRD v1 เป็น baseline) |

**Output:**
- **1 ไฟล์เดียว** (overwrite ของเก่า): `BRD_[feature].md` (Section 1 Changelog เพิ่ม revision entry)
- + `BRD_[feature].docx` (regenerate ใหม่)
- + AI Review Report (Revision-focused)

**Document Chain Check (Revision Mode):**
| สถานการณ์ | Action |
|---|---|
| ❌ ไม่มี BRD v1 | STOP — Revision ต้องมี BRD เก่าเป็น baseline |
| ❌ ไม่มี HTML v2 | STOP — Revision ต้องมี HTML ใหม่ |
| ⚠️ BRD v1 status ≠ APPROVED | warn — revision ของ BRD ที่ยังไม่ approved |
| ✅ มี BRD v1 + HTML v2 | proceed → Revision Workflow |

---

### Pipeline Mode / Fresh Mode (Cowork Automation)

**Required:**
| # | ไฟล์ | จากใคร | อ่านเพื่อ |
|---|---|---|---|
| 1 | `RIF_[feature].md` | requirement-intake-formatter | **business intent ทุก section** — source of truth ฝั่ง "ต้องการอะไร" |

**Recommended (เคสหลัก WF-01 v2 — HTML-first):**
| # | ไฟล์ | จากใคร | อ่านเพื่อ |
|---|---|---|---|
| 2 | `<feature>.html` | html-generator-v6 (ผ่าน ux+coverage gate แล้ว) | **หน้าจอ/flow ที่มีจริง** — Step 1.5 สกัด Screen Inventory · §5 Journey trace กับ route จริง · §8 status ที่มีจริงบนจอ |

> ⚠️ HTML ที่รับต้องผ่าน gate แล้วเท่านั้น — HTML ดิบที่ยังไม่ผ่าน qc-ux/qc-coverage
> ห้ามใช้เป็น ground truth (อาจมีหน้าเกิน scope หรือขาด exception path)

**Optional (ถ้ามีให้ใช้เสริม):**
| # | ไฟล์ | อ่านเพื่อ |
|---|---|---|
| 3 | `REQ_PHILO_[feature].md` (ถ้ามี) | ใช้ 5 Pillars rules ผสม — Philosophy hardening |
| 4 | `Feature_Brief_[feature].md` (จาก html-to-feature-brief) | mapping ตาม brd-draft-generator §92-104 |
| 5 | `System_Module_Registry.md/.csv` | สำหรับ Section 12.3 + 13 Delivery Phases |

### Standalone Mode

รับ input ในรูปแบบใดก็ได้:
- ข้อความเล่า requirement
- Transcript, screenshot, image
- Feature Brief (.md)
- BRD เก่า (rewrite mode)

ถ้าไม่มี RIF → **ถาม user คำถามจำเป็นก่อนเริ่ม** (Step 0.5 — Mini Intake)

### Document Chain Check

| สถานการณ์ | Action |
|---|---|
| ❌ ไม่มี RIF + ไม่มี input อื่น | STOP — ขอ RIF หรือ input ดิบ |
| ⚠️ ไม่มี System Module Registry | ทำ Section 12.3 แบบ "ไม่ระบุ — ขอ Registry ภายหลัง" + warn |
| ⚠️ ไม่มี REQ_PHILO | ใช้ Philosophy defaults (P1 preset, COSO standard) |
| ✅ มี RIF อย่างเดียว | ทำได้เต็มที่ — RIF เพียงพอ |

### Conflict Resolution Priority

หากแต่ละ source ขัดกัน (v2.2 — แยกตามประเภทคำถาม):
0. **LOCK-XX ชนะทุกอย่าง** — ขัด LOCK = SCOPE DRIFT flag ห้ามแก้เงียบ ๆ
1. คำถามเชิง business intent ("ต้องการอะไร ทำไม เกณฑ์อะไร") → **RIF ชนะ**
2. คำถามเชิง "หน้าจอ/flow มีอะไรจริง" → **HTML ชนะ** (เพราะผ่าน coverage gate เทียบ graph แล้ว)
3. HTML มีสิ่งที่ RIF ไม่ได้ขอ (เกิน intent) → **ห้าม**เขียนรับรองเข้า BRD เงียบ ๆ
   → flag `⚠️ HTML-RIF DRIFT` + Open Question (เลนจะส่งเข้า html-to-frd-sync ต่อ)
4. RIF ขอสิ่งที่ HTML ไม่มี → flag เดียวกัน (แปลว่า coverage gate อาจหลุด — ต้อง investigate ไม่ใช่แต่งหน้าเพิ่มเอง)
5. REQ_PHILO ขยาย / Feature Brief ใช้เป็น mapping (เหมือนเดิม)
6. ห้ามแต่ง spec ที่ไม่มีในทุก source → Section 15 Open Questions

---

## 📤 Output

ทุกครั้งสร้าง **2 ไฟล์:**

1. **`BRD_[feature].md`** — สำหรับ AI ใช้ต่อ (frd-generator-v6)
2. **`BRD_[feature].docx`** — สำหรับมนุษย์อ่าน (Thai font, cover, table styling)

พร้อม **AI Review Report** ในตอนท้าย (จาก Quality Gate)

---

## 🎯 Decision Rules (Master)

### By BRD Type

อ่าน `references/brd-types.md` เพื่อรู้ Sections ที่ต้องคลุม:

| ประเภท | Sections ที่ต้อง cover | ขนาด |
|---|---|:---:|
| **New Feature** | 1-15 ครบ (ทำเต็มทุก step) | เต็ม |
| **Enhancement** | 1-15 + "ของเก่า vs ของใหม่" ทุก section ที่เปลี่ยน + Regression Scope | เต็ม+ |
| **Bug Fix** | สั้น: Expected/Actual, Reproduce, Impact, Regression, Dev Summary | สั้น |
| **Config/Chore** | สั้นสุด: ค่าเก่า/ใหม่, เหตุผล, Impact, ผู้อนุมัติ | สั้นสุด |

### Skip / Run Matrix

| Step | New Feature | Enhancement | Bug Fix | Config/Chore |
|---|:---:|:---:|:---:|:---:|
| 1. Draft (Sec 1-9) | ✅ | ✅ | ⚡ สั้น | ⚡ สั้นสุด |
| 2. Enrich Edge Cases | ✅ | ✅ (เน้น "ของเก่าพัง") | ❌ | ❌ |
| 3. Flexibility | ✅ | ✅ (+ Migrate) | ❌ | ❌ (ตรวจ Admin Panel hint) |
| 4. Data Entity | ✅ | ⚡ ADD/MODIFY/REMOVE | ❌ | ❌ |
| 5. Existing System | ✅ | ✅ | ❌ | ❌ |
| 6. Philosophy Embed | ✅ | ✅ | ⚡ ย่อ | ⚡ ย่อ |
| 7. Quality Gate | ✅ C01-C23 | ✅ C01-C23 + CE01-CE03 | ✅ CB01-CB03 | ✅ CC01-CC04 |

---

## 📐 Workflow

Skill มี 2 workflow ตาม mode:
- **Fresh Mode** → Step 0-7 (สร้าง BRD ใหม่)
- **Revision Mode** → Step R1-R5 (sync HTML กลับ BRD)

---

## 🔄 Revision Workflow (Step R1-R5) ⭐ ใหม่

### Step R1 — Drift Detection

**R1.1 อ่าน Input:**
- BRD v1 (.md) — base ของเดิม
- HTML v2 (.html) — ที่ vibe แล้ว
- HTML v1 (ถ้ามี) — ของก่อน vibe (baseline ให้ diff)
- Diff notes (ถ้ามี) — user อธิบายเอง

**R1.2 Extract จาก HTML v2:**
- Pages list (จาก hash routes / view names)
- Fields ทุก form/input (label, type, validation, required)
- Actions (buttons, onclick handlers)
- State transitions (status flow ใน mock data)
- Workflow steps (ถ้ามี approval/multi-step)
- Edge cases (validation messages, error states)

**R1.3 Compare กับ BRD v1:**
อ่าน BRD v1 sections แล้วเทียบทีละ section:

| BRD Section | เทียบกับใน HTML |
|---|---|
| §4 Roles | ปุ่ม/menu ที่แสดงตาม role |
| §5 User Journey | flow ของ action ที่กดได้ |
| §6 Data Entity | fields ใน form |
| §7 User Stories | features ที่ HTML implement |
| §8 Status Lifecycle | status badge / transition |
| §9 Business Rules | validation rules, conditional logic |
| §10 Edge Cases | error messages, disabled states |
| §16 Security | permission gates, sensitive fields |
| §17 Health Check | SLA badges, KPI displays |
| §18 Monitoring | dashboard widgets |

**R1.4 Classify Drift:**

| Drift Class | ตัวอย่าง | Action |
|---|---|---|
| 🟢 **UX** | สี, layout, spacing, copy text, icon | sync ไป FRD ดีกว่า — แต่ถ้าเปลี่ยนมาก ก็ update BRD §6 minor |
| 🟡 **Hidden Logic** | validation rule ใหม่, calculation formula ที่ vibe เพิ่ม | update BRD §9 + ตรวจ Tag |
| 🔴 **Business** | field ใหม่/หาย, workflow step เพิ่ม, role ใหม่, status เปลี่ยน | update BRD §5/§6/§7/§9 + อาจกระทบ Philosophy embed |
| 🚨 **Critical** | Tag FIXED→DYNAMIC, ลบ Locked Section, Security Preset เปลี่ยน, ลบ COSO role | ⚠️ **Step R2 จะถาม user ก่อน** |

**Output ของ Step R1:**

```markdown
_DRIFT_REPORT.md

## Drift Summary
- 🟢 UX drifts: 5 items
- 🟡 Hidden Logic drifts: 2 items
- 🔴 Business drifts: 3 items
- 🚨 Critical drifts: 1 item ← ต้องถาม user

## Critical Drifts (ต้อง decision)
- C-01: R04 (สูตรส่วนลด) เปลี่ยนจาก FIXED → DYNAMIC
  - ใน BRD v1 §9: ส่วนลด 5% flat (FIXED)
  - ใน HTML v2: ส่วนลดแปรตาม tier (5% → 10% → 15%)
  - กระทบ: Section 9, 9.5, 13 (Delivery Phase 3 ต้องมี Rule Management)

## Business Drifts (auto-apply, แค่แจ้ง)
- B-01: Field "customer_tier" เพิ่ม (กระทบ Section 6, 9)
- B-02: Status "On Hold" เพิ่ม (กระทบ Section 8)
- B-03: Action "Bulk Approve" เพิ่ม (กระทบ Section 5, 7)

## Hidden Logic Drifts
- HL-01: Validation "ห้าม discount > 30%" (เพิ่มใน §9.2)
- HL-02: Auto-calc "tax = subtotal * 0.07" (เพิ่มใน §9 Rules)

## UX Drifts (sync ไป FRD ทีหลังก็ได้)
- UX-01: Button "ส่งอนุมัติ" เปลี่ยนตำแหน่ง (header → footer)
- UX-02: Color theme tweak
... (5 items total)
```

---

### Step R2 — Critical Decision Gate ⭐

**ถ้า Step R1 พบ Critical Drifts → ถาม user 1 รอบ:**

```
พบ Critical Drift [N] ข้อ ที่อาจกระทบ business contract:

1. [C-01]: R04 Tag เปลี่ยนจาก FIXED → DYNAMIC
   - กระทบ: Implementation Phase + Rule Management infrastructure
   - ตั้งใจหรือเปล่า?

2. [C-02]: ...

ตอบครับ:
A. ✅ Critical ทุกข้อ — ตั้งใจเปลี่ยน → proceed (skill จะ apply ทั้งหมด + warn audit)
B. ⚠️ Critical บางข้อ — ระบุข้อที่ไม่ต้องการ → skill จะ revert เฉพาะที่ user เลือก
C. ❌ ไม่ critical เลย — เป็น drift ที่หลุดมา → skill จะ revert ทั้งหมด + log warning
```

**ถ้าไม่มี Critical Drift → ข้าม Step R2 ไป R3 เลย**

---

### Step R3 — Impact Analysis

**R3.1 หา Sections ที่กระทบ:**

จาก drift list → map ไป BRD sections:
```
B-01 (field customer_tier) → §6 (Data Entity) + §9 (Validation) + §10 (Edge: tier=null)
B-02 (status On Hold) → §8 (State Diagram) + §5 (Journey: hold step) + §9 (Rule: when allowed)
B-03 (Bulk Approve) → §5 (Journey) + §7 (Story) + §4 (Permission)
HL-01 (discount limit) → §9.2 (Validation)
HL-02 (tax calc) → §9 (Rule)
C-01 (R04 → DYNAMIC) → §9 + §9.5 + §13 (Phase 3 Rule Management) + §14 (Dev Summary)
```

**R3.2 Tag Re-evaluation:**

สำหรับ drifts ที่กระทบ Section 9:
- รัน Tag classification ใหม่กับ Rules ทั้งหมดที่ touched
- ถ้า Tag เปลี่ยน → flag ใน Changelog

**R3.3 Philosophy Embed Re-check:**

- COSO Roles: ถ้ามี role/action ใหม่ → update §5 + §4
- Security Preset: ถ้ามี sensitive field ใหม่ → re-evaluate preset
- SLA/KPI: ถ้ามี action ใหม่ → ต้องมี SLA?
- Monitoring: ถ้ามี state ใหม่ → ต้องมี widget/report?

**R3.4 Regression Scope:**

ระบุ:
- Section ที่ "ไม่กระทบ" (preserve เป็น-เป็น)
- Section ที่ "กระทบบางส่วน" (selective update)
- Section ที่ "rewrite" (rare — เฉพาะ Critical drift ใหญ่)

---

### Step R4 — Generate BRD v2

**R4.1 Strategy: Selective Update (ไม่ regenerate ทั้งฉบับ)**

```
For each section:
  ถ้า impact = none → copy from v1 (preserve)
  ถ้า impact = partial → update เฉพาะ rows ที่ drift
  ถ้า impact = full → rewrite section (rare)
```

**R4.2 Update Sections ที่กระทบ:**

ตัวอย่าง:
- §6 Data Entity → เพิ่ม row "customer_tier"
- §8 State Diagram → เพิ่ม node "On Hold" + edges
- §9 Rules → เพิ่ม R-NEW + อัปเดต Tag ของ R04
- §10 Edge Cases → เพิ่ม case "tier=null"
- §13 Delivery Phases → ย้าย R04 จาก Phase 1 → Phase 3

**R4.3 Section 1 Changelog (บังคับ):**

```markdown
## Changelog
- v1.0 (2026-05-10): Initial via brd-generator-full
- v1.1 (2026-05-12): Revision จาก HTML vibe ⭐
  - Source: HTML_quotation_v2.html (vibe โดย user)
  - Drift Summary: 5 UX + 2 Hidden Logic + 3 Business + 1 Critical
  - Sections updated: §6, §8, §9, §9.5, §10, §13, §14
  - Sections preserved: §1, §2, §3, §4 (partial), §11, §12, §15, §16, §17, §18
  - Critical decisions:
    - C-01: R04 Tag FIXED → DYNAMIC (confirmed by user)
  - Drift Report: _DRIFT_REPORT_v1.1.md
```

**R4.4 Quality Gate (Revision-specific):**

รัน checklist เดิม (C01-C23 + PE01-PE05) บน v2 + เพิ่ม:

- **CR01**: Changelog v1.1 entry มีครบทุก field
- **CR02**: Critical drifts ทั้งหมดมี user decision documented
- **CR03**: Sections preserved ไม่ถูก touch โดยไม่จำเป็น
- **CR04**: Tag changes (ถ้ามี) มี migration plan ใน §13/§14
- **CR05**: Philosophy embed ยังครบ (COSO/Security/SLA/Monitor)

---

### Step R5 — Output + Recommend Next Steps

**R5.1 Save Files:**
```
/mnt/user-data/outputs/BRD_[feature].md         ← overwrite v1
/mnt/user-data/outputs/BRD_[feature].docx       ← regenerate
/mnt/user-data/outputs/_DRIFT_REPORT_v1.1.md    ← เก็บ audit trail
/mnt/user-data/outputs/_AI_REVIEW_REPORT.md     ← Quality Gate report
```

**R5.2 Recommend Downstream:**

```
✅ BRD v2 พร้อมแล้ว (Status: APPROVED)

Drift Summary:
  - 1 Critical (R04 Tag เปลี่ยน — confirmed)
  - 3 Business drifts (applied)
  - 2 Hidden Logic drifts (applied)
  - 5 UX drifts (applied — มี note ให้ sync FRD)

Downstream ที่กระทบ:
  ⚠️ FRD ต้อง regenerate (Section 6, 9 เปลี่ยน schema)
     → เรียก frd-generator-v6 ใหม่ พร้อม BRD v2
  ⚠️ QA Tests ต้อง regenerate (Edge Cases ใหม่)
     → เรียก ai-testcase-md-generator + qa-friendly-html-generator พร้อม FRD ใหม่
  ✅ HTML v2 ถูกใช้เป็น source — ไม่ต้อง regenerate
     แต่อาจ run html-generator-v6 อีกครั้งเพื่อ "production cleanup"
  ⚠️ Dev Brief ต้อง regenerate (สรุปใหม่)

แนะนำลำดับ:
  1. /frd-generator-v6 (BRD v2) → FRD v2
  2. /ai-testcase-md-generator + qa-friendly-html-generator (FRD v2) → testcases + UAT HTML v2
  3. /dev-brief-generator (FRD v2 + HTML v2 + QA v2) → Dev Brief v2
```

**R5.3 Critical Warning (ถ้ามี):**

```
⚠️ AUDIT TRAIL NOTE:
   BRD ฉบับนี้ถูก revise จาก HTML vibe โดย user
   Stakeholder ที่ approve BRD v1 อาจไม่รู้ว่า:
   - R04 Tag เปลี่ยน
   - Phase 3 Rule Management ถูกเพิ่มเข้ามา

   แนะนำ: ส่ง _DRIFT_REPORT_v1.1.md ให้ stakeholder review ก่อน proceed
```

---

## 📐 Fresh Workflow (Step 0-7 + Quality Gate)

### Step 0 — Identify Type + Read RIF

**0.1 อ่าน RIF ทั้งฉบับ + ระบุประเภท BRD**

- อ่าน frontmatter: `request_type` (จาก RIF v2.1) → ใช้เป็นประเภทเลยไม่ต้องถาม
- อ่าน `scope_lock_ref` + §16.3 Locked Decisions → เก็บไว้ใช้ Step 1 (Section 3.4) ⭐

ถ้า input ไม่ระบุประเภท (RIF เก่า/standalone) → ถาม user:
> "ประเภท BRD เป็นอะไรครับ? (1) New Feature (2) Enhancement (3) Bug Fix (4) Config/Chore"

**0.2 Branch ตามประเภท:**
- Bug Fix → ข้าม Step 1-6 ไป **Bug Fix Mini Flow** (ดู `references/brd-types.md` §Bug Fix)
- Config/Chore → ข้าม Step 1-6 ไป **Config Mini Flow** (ดู `references/brd-types.md` §Config)
- New Feature / Enhancement → ทำต่อ Step 1

**0.3 Skip Decomposer:**
สมมติว่า RIF = 1 feature เสมอ ไม่ต้อง split ถ้า user ระบุชัดว่ามีหลาย feature → แจ้ง user ว่า "Skill นี้ทำ 1 BRD ต่อ feature — กรุณาแยก RIF เป็นไฟล์ละ feature"

---

### Step 1 — Draft Sections 1-9

อ่าน `references/brd-template-v3.md` + `references/change-likelihood-tags.md`

**Section 1: Document Info**
- BRD ID, ชื่อ Feature, ประเภท, Version, Status = "Draft", Owner, Stakeholders, วันที่

**Section 2: Business Context** (จาก RIF §1-3)
- ปัญหา / โอกาส
- เป้าหมาย business
- **ตัวชี้วัดความสำเร็จ (บังคับวัดได้ — v2.1):** ตาราง | ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง/จากไหน | วัดเมื่อไหร่ |
  - ห้ามเขียนลอย ("ทำงานเร็วขึ้น") — ต้องมีตัวเลข/แหล่งวัด; ไม่มี baseline → ระบุ "ต้องเก็บ baseline ก่อน launch" เป็น action
  - ทุกตัวชี้วัดต้องมีคู่ใน §17.3 KPI (business KPI ไม่ใช่แค่ system health) — Quality Gate ตรวจ (C22)
- ที่มา (เคสที่เกิด, request จาก stakeholder, KPI gap)

**Section 3: Scope** (จาก RIF §8 In/Out scope)
- In Scope (ทำอะไร)
- Out of Scope (ไม่ทำอะไร — สำคัญ; รวม Exclusions จากใบยืนยันขอบเขต/Proposal)
- Assumptions
- **3.4 Scope Lock ⭐ (v2.1):** ยก `scope_lock_ref` + Locked Decisions (LOCK-XX) จาก RIF §16.3 มาทั้งชุด
  - In Scope ทุกข้อต้องอยู่ใต้ขอบเขตใบเซ็น — ข้อที่เกิน/ชน Exclusions → ห้ามใส่เงียบ ๆ ต้อง flag `⚠️ SCOPE DRIFT` + Open Question ให้ PM/ลูกค้าเคาะ
  - LOCK-XX ห้าม override ตลอด chain — ถ้า business rule ใดขัดกับ LOCK → LOCK ชนะ + แจ้งใน AI Review

**Section 4: User Roles & Permissions**
- ตาราง Role × Action (ใครทำอะไรได้)
- ใช้ data จาก RIF §4 (Actors)

**Section 5: User Journey (with COSO)** ⭐ Philosophy Embedded
- Happy Path step-by-step
- Alternative Paths
- **ทุก step ต้องมี column COSO Roles: Maker / Checker / Approver / System**
- SoD check: Maker ≠ Approver ในทุก approval step
- ถ้าข้อมูล COSO ไม่ครบ → Interactive: ถาม user · **Lane Mode: ใช้ default จาก `knowledge/coso-defaults.md` + log** (ห้ามถาม)
- (v2.2) ถ้ามี HTML: ทุก step ใน Journey ต้อง map กับ route/ปุ่มที่มีจริง — step ที่ไม่มีที่ยืนบนจอ = flag drift

**Section 6: Data Entity & Fields** — ทำที่ Step 4 (เพื่อให้ใช้ Edge Cases + Validation ที่ enrich แล้ว)

**Section 7: User Stories & Acceptance Criteria** (จาก RIF §11 + Feature Brief mapping)
- แตก Story แบบ Given-When-Then
- กฎ: Story description ห้ามมีคำว่า "และ" — ถ้ามี แยก Story
- ทุก Story มี AC อย่างน้อย 2 ข้อ

**Section 8: Status & Lifecycle**
- State Diagram (Mermaid หรือ ASCII)
- ตาราง State × Trigger × Next State

**Section 9: Business Rules + Validation (Draft + Tags)**
- รวบรวมจาก RIF §5 (Brain) + §7 (Threshold)
- ทุก rule ที่มีตัวเลข/เงื่อนไข → ติด **Change Likelihood Tag**: FIXED / CONFIGURABLE / DYNAMIC / WARNING
- อ่าน `knowledge/change-likelihood-tags.md` Misclassification Patterns
- ติด WARNING ไว้ก่อนถ้าไม่แน่ใจ — Step 3 จะ resolve

**Screen List Draft** (จาก RIF §10 UI Hint)
- ตาราง: ชื่อหน้า, Layout Hint (จาก RIF), ใครเข้าถึง, Function ของหน้า
- ระบุแค่ประเภทหยาบ — Step 1.5 จะจัดเป็น Screen Inventory (spec จริงไป FRD)

---

### Step 1.5 — Screen Inventory (หยาบ) — BRD ไม่ตัดสิน Layout

**หลักการ (v2.1):** BRD = เอกสาร business — บอกแค่ "มีหน้าอะไร ประมาณไหน ใครใช้ กี่หน้า"
**Layout/Pattern/CI spec จริง = หน้าที่ของ FRD** (frd-generator-v6 เป็น Design Authority, html-generator-v6 enforce) — BRD ห้ามระบุ Layout Template ID / pattern / สี / ขนาด

**1.5.0 เลือกวิธีตาม input (v2.2):**
- **มี HTML (เคสหลัก)** → **สกัด** Screen Inventory จาก HTML: ไล่ทุก route/หน้า ที่มีจริง
  แล้วเติมคอลัมน์ business (ผู้ใช้หลัก/หน้าที่) จาก RIF — **ห้ามแต่งหน้าเพิ่ม ห้ามตัดหน้า**
  ทุกแถวต้องมี route จริงอ้างอิง (เช่น `#/pr-list`) · หน้าใน HTML ที่ RIF ไม่กล่าวถึง หรือกลับกัน → flag `⚠️ HTML-RIF DRIFT` (ดู Conflict Priority)
- **ไม่มี HTML (doc-only)** → คาดการณ์จาก RIF §10 UI Hint แบบเดิม + ระบุใน BRD ว่า inventory เป็น "คาดการณ์ — รอ HTML ยืนยัน"

**1.5.1 สร้าง Screen Inventory:**

| # | ชื่อหน้า | route (จาก HTML) | ประเภทหยาบ | ผู้ใช้หลัก | หน้าที่ของหน้า (business) | หมายเหตุ |
|---|---|---|---|---|---|---|
| P-01 | รายการใบขอซื้อ | `#/pr-list` | หน้ารายการ | จัดซื้อ, ผู้ขอ | ค้นหา/ติดตามสถานะ PR ทั้งหมด | |
| P-02 | สร้างใบขอซื้อ | `#/pr-create` | ฟอร์มสร้าง (หลายขั้น) | ผู้ขอ | กรอกรายการ + ส่งอนุมัติ | |
| P-03 | รายละเอียด PR | `#/pr/:id` | หน้ารายละเอียด | ทุก role | ดูข้อมูล + อนุมัติ/ตีกลับ | มีเอกสารแนบ+ลายเซ็น |

(doc-only mode: คอลัมน์ route = "— รอ HTML")

**ประเภทหยาบที่ใช้ได้ (คำ business เท่านั้น):** หน้ารายการ / ฟอร์มสร้าง (ขั้นเดียว|หลายขั้น) / ฟอร์มแก้ไข / หน้ารายละเอียด / หน้ายืนยัน / dashboard / รายงาน (ดู+พิมพ์) / หน้าแรก-landing

**1.5.2 สรุปจำนวนหน้าโดยประมาณ** — "ฟีเจอร์นี้มี ~N หน้า (รายการ 1, ฟอร์ม 2, รายละเอียด 1, ...)" เพื่อให้ประเมิน effort ได้

**1.5.3 UI Signal ที่ต้องส่งต่อ FRD (แค่ signal ไม่ใช่ spec):**
- เป็น Document/Transaction ไหม (มี approver + พิมพ์เอกสาร + ลายเซ็น) → FRD จะเลือก pattern เอกสารเอง
- มีหน้าที่ต้อง print/PDF ไหม
- RIF ระบุ `NON-STANDARD` / `keep original UI` explicit ไหม → ส่งต่อ flag ตรง ๆ + Open Question ให้ stakeholder approve (BRD ไม่ตัดสิน)

**สิ่งที่ BRD ไม่ทำแล้ว (ย้ายไป FRD):** Layout Template ID, Sync Read html-generator, CI lock check, Iron Rules compliance, Layout Deviation Log — ทั้งหมดเป็นหน้าที่ frd-generator-v6 + html-generator-v6

> **ระวัง (v2.2):** การ "เห็น HTML" ไม่ได้แปลว่า BRD ได้อำนาจตัดสิน layout กลับคืน —
> BRD สกัดแค่ **การมีอยู่ + หน้าที่ business** ของหน้า · pattern/CI/spec ยังเป็นของ FRD 100%

---

### Step 2 — Enrich Edge Cases + Validation

อ่าน `references/edge-case-patterns.md`

**2.1 Pattern Matching:**
สแกน Section 5 (Journey) + Section 9 (Rules) แล้วเทียบกับ pattern:
- File Upload → FU patterns
- Concurrent Access → CA patterns
- Email/Notification → EM patterns
- Lookup Master Data → DI patterns
- Calculation → CL patterns
- Status/Workflow → ST patterns
- PDF Generation → PD patterns
- Permission → PM patterns
- Enhancement-specific → EN patterns

**2.2 สร้าง Section 10: Edge Cases**

โครงสร้าง:
- **10.1 Edge Cases ที่ user/RIF ระบุ** (ดึงจาก RIF §5 + §11) — default ☑
- **10.2 Edge Cases จาก AI Pattern Matching** — แยกหมวด ทุกข้อมี checkbox ☐
  - **เจ้าของการ confirm = BA ที่ SOW3.7 (Vibe Fix & Final Test)** — ☐ = "แนะนำ" dev ยังไม่ต้อง implement จนกว่า BA ติ๊ก ☑ หรือระบุใน FRD; ข้อที่กระทบเงิน/สิทธิ์/ข้อมูลสูญหาย → ยกเป็น Open Question ทันทีไม่รอ

**2.3 อัปเดต Section 9: Validation Rules**

จาก Edge Cases ใหม่ → เพิ่ม Validation Rules ใน Section 9
ทุก VR ต้องมี: Field/Action, เงื่อนไข, ประเภท (Error/Warning/Trigger/Prevent), ข้อความ

**2.4 Tag Review Report**

ตรวจ Section 9 Tags:
```
✅ R01: FIXED — ถูกต้อง
⚠️ R06: CONFIGURABLE → แนะนำ DYNAMIC (เหตุผล: มีหลายเงื่อนไขซ้อน)
❌ R11: ไม่มี Tag → แนะนำ CONFIGURABLE
```

**2.5 Enhancement เพิ่มเติม:**
- ตรวจว่า "ของเก่า vs ของใหม่" ครบทุก section ที่เปลี่ยน
- เพิ่ม Regression Scope ใน Section 11 (Impact)

---

### Step 3 — Flexibility Auto-Resolve

อ่าน `references/flexibility-questionnaire-guide.md` + `knowledge/cube-defaults.md`

**3.1 หา rules ที่ต้อง resolve:**
สแกน Section 9 → หา rules ที่ติด CONFIGURABLE / DYNAMIC / WARNING

**3.2 Auto-Resolve (Pipeline Mode — ไม่มี Stakeholder):**

ใช้ inference logic:
- **IT/Dev + นานๆ ครั้ง + แค่เปลี่ยนค่า** → **Config File**
- **Admin + เป็นระยะ + แค่เปลี่ยนค่า** → **Admin Panel**
- **ผู้บริหาร + เป็นระยะ-บ่อย + เปลี่ยนเงื่อนไข** → **Rule Management**
- **ผู้บริหาร + เปลี่ยน Flow/สูตร** → **Engine Management**

Inference cues:
- Module = HR → P6 preset, security mode
- Module = Finance → P4 preset, strict mode
- Rule = limit/cap/threshold → Admin Panel default
- Rule = formula/calculation → Rule Management default
- Rule = workflow logic → Engine Management default

**3.3 Standalone Mode (มี Stakeholder จริง):**

สร้างชุดคำถามให้ user ไปถาม Stakeholder:
- CONFIGURABLE/DYNAMIC: ใครเปลี่ยน + บ่อยแค่ไหน
- DYNAMIC เพิ่ม: เงื่อนไขปัจจุบัน, อนาคต, เปลี่ยนค่าหรือ Logic
- WARNING: ตัดสินใจได้เมื่อไหร่
- Enhancement: Rule เดิมอยู่ในรูปแบบไหน

แล้วรอ user กรอกคำตอบกลับ → resolve

**3.4 อัปเดต Section 9:**
- เพิ่มคอลัมน์ "ใครเปลี่ยน + บ่อยแค่ไหน + ระดับ"

**3.5 สร้าง Section 9.5: สรุประดับความยืดหยุ่น**
- Summary table: Rule ID × ระดับ × เหตุผล × **ที่มา (🤖 AI-inferred / ✅ Stakeholder ยืนยัน)** ⭐ v2.1
- **Escalation บังคับ:** ข้อที่ 🤖 AI-inferred และระดับ = DYNAMIC หรือ Engine Management → ต้องลง Section 15 Open Questions ให้ stakeholder ยืนยันก่อนพัฒนา Phase นั้น (ระดับ Config File/Admin Panel ที่ AI เดา ปล่อยผ่านได้แต่ mark 🤖 ไว้)

**3.6 WARNING ที่ยัง Resolve ไม่ได้:**
- ระบุแผนหารือ (กับใคร, กำหนดวันที่) → ใส่ Section 15 Open Questions

---

### Step 4 — Data Entity Design

อ่าน `references/erp-data-patterns.md`

**4.1 วิเคราะห์ Section 5 + 9 → ระบุ Entities:**
- Header data
- Detail/Line items
- File attachments
- Status/Workflow fields
- Master data references

**4.2 เลือก Pattern + สร้าง Entity Tables:**

**ถ้า New Feature:**
- สร้าง Entity ใหม่ตาม pattern
- เพิ่ม Audit Fields ทุก entity (created_by, created_date, modified_by, modified_date)
- เพิ่ม Snapshot Fields สำหรับ lookup ที่ต้องเก็บค่า ณ เวลาสร้าง
- เพิ่ม Running Number ตาม pattern

**ถ้า Enhancement:**
- ใช้ตาราง Action: ADD / MODIFY / REMOVE / NO CHANGE
- ระบุ Field × ก่อน × หลัง × กระทบ
- ตรวจว่า Field ใหม่กระทบ Entity Relationship เดิมหรือไม่

**4.3 สร้าง Section 6 ตาราง Fields:**
ทุก field มี: #, Field Name, Label UI, Input Type, ค่า/ตัวเลือก, จำเป็น, เงื่อนไข, หมายเหตุ
Input Types: AUTO, TEXT, NUMBER, DATE, DATETIME, DROPDOWN-SINGLE, DROPDOWN-MULTI, LOOKUP, TOGGLE, RICHTEXT, TEXTAREA

**4.4 สร้าง Entity Relationship Diagram:**
```
Entity A ──(1:N)──▶ Entity B
Entity C ──(referenced by)──▶ Entity B
```
ระบุ FK, ประเภท (1:1/1:N/N:M), ทิศทาง

---

### Step 5 — System Context Mapping (Value Stream + Existing System) ⭐ v2.1

**5.0 Value Stream Positioning + Downstream Impact (บังคับ New Feature/Enhancement):**

> BRD ที่ดีต้อง "เข้าใจว่า feature นี้อยู่ตรงไหนของสายธุรกิจ และสะท้อนต่อไปที่ไหน" —
> เช่น Purchase Request ต้องรู้ว่าไหลต่อไป PO → GRN → Putaway → AP Invoice → Payment

ขั้นตอน:
1. **เปิด `cube-master-knowledge`** (VS Bible + feature catalog) — หา Value Stream/VC/CL ที่ feature นี้สังกัด
   ถ้าเข้าไม่ถึง → ใช้ความรู้ ERP standard + ระบุ "รอ confirm กับ VS Bible" ใน Open Questions
2. **Upstream:** feature นี้รับข้อมูล/trigger จากเอกสารหรือขั้นตอนไหน (เช่น PR รับจาก Budget/แผนจัดซื้อ)
3. **Downstream Impact Map:** เอกสาร/module ที่รับผลต่อ — ต่อรายการระบุ: ข้อมูลอะไรไหลไป, สถานะไหน trigger, ถ้า feature นี้เปลี่ยน/ยกเลิกกลางทางจะกระทบยังไง
4. **ผลกระทบแนวขวาง:** สต๊อก / บัญชี(GL, งบ) / รายงาน / งบประมาณ — โดนอะไรบ้าง
5. เขียนลง **Section 12.1** (ตาราง + diagram ลูกโซ่เอกสาร) — ทุกแถวต้องตอบได้ว่า "แล้วไงต่อ"

ตัวอย่าง Downstream Impact Map (PR):
| ปลายทาง | ข้อมูลที่ไหลไป | Trigger | ถ้า PR ถูกยกเลิก/แก้ |
|---|---|---|---|
| PO | รายการสินค้า+จำนวน+budget commit | PR approved | PO ที่อ้าง PR นี้ต้อง revalidate |
| Budget | commit amount | PR approved | release commitment คืน |
| GRN→Putaway | (ทางอ้อมผ่าน PO) | — | — |

**5.1 Check Registry:**
- ถ้ามี System Module Registry → ทำ mapping
- ถ้าไม่มี → สร้าง Section 12.3 แบบ placeholder + warn user

**5.2 สร้าง Section 12.3: Existing System Reference**

อ่าน Section 9 + 9.5 → หา rules ที่ระบุระดับแล้ว เทียบกับ Registry:

| Rule | ระดับ | มีอยู่แล้ว? | Reference |
|---|---|:---:|---|
| R11 (เลขที่เอกสาร) | Admin Panel | ✅ | Admin → System Config → Document Numbering |
| R08 (เพดานส่วนลด) | Admin Panel | ❌ | ต้องสร้างใหม่ |
| R18 (SLA อนุมัติ) | Admin Panel | ⚠️ บางส่วน | Approval Module มีแล้ว แต่ยังไม่มี SLA Timer |

**5.3 สร้าง Section 13: Delivery Phases**

จัดกลุ่ม Rules → Phases:

**Phase 1: Feature Launch**
- ทุก rule: Config Table + Seed / Rule Table + Seed / State Machine
- ห้าม Hardcode ตั้งแต่วันแรก
- Reuse ของเดิม

**Phase 2: Admin Panel**
- Rules ที่ต้องการ Admin Panel + ❌ ยังไม่มี

**Phase 3: Rule Management**
- Rules ที่ต้องการ Rule Management + ❌ ยังไม่มี

**Phase 4: Engine Management**
- Rules ที่ต้องการ Engine Management + ❌ ยังไม่มี

---

### Step 6 — Philosophy Embed (Full) ⭐

อ่าน `knowledge/security-presets.md` + `knowledge/security-78-controls.md` + `references/philosophy-embed-guide.md`

**6.1 Security Preset Selection:**

ถ้า REQ_PHILO มี preset แล้ว → ใช้ตามนั้น
ถ้าไม่มี → infer จาก Module:
- Standard Transaction (QT/PO/SO/Invoice) → P1 (12 controls)
- Approval/Workflow → P2 (14 controls)
- Master Data → P3 (10 controls)
- Financial/Payment → P4 (16 controls)
- Report/Dashboard → P5 (9 controls)
- HR/PII Sensitive → P6 (15 controls)
- Integration/API → P7 (11 controls)
- AI/Automation → P8 (10 controls)
- OT/Manufacturing → P9 (13 controls)
- Audit/Compliance → P10 (12 controls)
- Critical → P-MAX (78 controls)
- Internal tool → P-MIN (5 controls)

แจ้ง user preset ที่เลือก + เปิดให้ override

**6.2 สร้าง Section 16: Security & Compliance**
- 16.1 Preset ที่ใช้ + เหตุผล
- 16.2 Applicable Standards (14 standards × ✅/❌)
- 16.3 Control Checklist (ทุก control: Required ✓Must/○Optional + Implementation Notes)
- 16.4 Risk Statement (R-XX → Risk → Mitigated by Control IDs, อย่างน้อย 3 risks)

**6.3 สร้าง Section 17: Health Check**

อ่าน `references/health-monitoring-patterns.md`

- 17.1 **SLA** — ทุก step ที่มีเวลาควบคุม + Owner
- 17.2 **Control Points** — map จาก Section 16 controls
- 17.3 **KPI** — Volume / Quality / Speed / Compliance / Conversion (อย่างน้อย 3 ตัว)
- 17.4 **Threshold** — Min / Max / Action when breached
- 17.5 **Throughput** — Capacity / Baseline / Stress Point

**6.4 สร้าง Section 18: Monitoring**
- 18.1 Reports Overview (4 types: Performance/Closing/Anomaly/Transaction)
- 18.2 Dashboard Widgets (อ้างอิง KPI/Threshold จาก Section 17)
- 18.3 Performance Report
- 18.4 Closing Report
- 18.5 Anomaly Report
- 18.6 Transaction Report

**6.5 Cross-Section Coverage Check:**
- ทุก Business Condition ใน Section 9 → มี Edge Case/Scenario cover ใน Section 10 ✅
- ทุก Control runtime ใน Section 16 → มี Control Point ใน Section 17 ✅
- ทุก SLA/KPI/Threshold ใน Section 17 → มี Widget/Report ใน Section 18 ✅

---

### Step 7 — Quality Gate (Built-in)

อ่าน `references/ai-review-checklist.md`

**7.1 สร้าง Section 14: Dev Requirements Summary "ใบสั่ง"**

**14.1 Config Foundation ที่ต้องเตรียม:**
- รวบรวมจาก Section 9.5 + Section 12.3
- ระบุ: โครงสร้าง, รองรับ Rule ไหน, มีอยู่แล้วหรือไม่

**14.2 ข้อกำหนดจาก Tag:**
- ทุก rule ที่ไม่ใช่ FIXED
- ระบุ: Rule, ระดับ, Dev ต้องทำอะไร (ชัดเจน ไม่ใช่แค่ "ห้าม Hardcode")
- Rule ที่ ✅ มีอยู่แล้ว → "ใช้ [Module] ที่มีอยู่แล้ว ไม่ต้องสร้างใหม่"

**14.3 ข้อกำหนดจาก Edge Cases / Validation:**
- Edge Cases สำคัญที่ Dev ต้อง Handle เป็นพิเศษ

**14.4 WARNING ที่รอข้อสรุป:**
- ประเด็น, หารือกับใคร, กำหนดวันที่, สถานะ
- ห้ามเริ่มพัฒนาส่วนที่เกี่ยวข้องจนกว่า Resolve

**14.5 Regression Scope** (Enhancement เท่านั้น)
- Feature เก่าที่ต้อง Test ซ้ำ + เหตุผล

**7.2 สร้าง Section 15: Open Questions**
- WARNING ที่ยังไม่ Resolve
- คำถามจาก Stakeholder ที่ยังไม่ตอบ
- ประเด็นที่ Tech Lead ยังไม่ Confirm

ทุกข้อมี: คำถาม, สถานะ (⚠️ รอ / ✅ ตอบแล้ว), คำตอบ (ถ้ามี)

**7.3 AI Review Checklist**

อ่าน `references/ai-review-checklist.md` แล้วตรวจ:

| ประเภท | Checklist | จำนวน |
|---|---|:---:|
| New Feature | C01-C23 | 23 |
| Enhancement | C01-C23 + CE01-CE03 | 26 |
| Bug Fix | CB01-CB03 | 3 |
| Config/Chore | CC01-CC04 | 4 |

**ข้อสำคัญที่ต้องไม่พลาด:**
- C05: Story description ไม่มีคำว่า "และ"
- C10: ทุก rule ที่มีตัวเลข/เงื่อนไข ติด Tag แล้ว
- C13: Edge Cases ครบหมวด
- C18: WARNING ทุกข้อมีแผนหารือ
- C19: Section 14 ใบสั่งครบ
- **C20 (v2.1): Scope Lock — §3.4 ครบจาก RIF, ไม่มี scope เกินใบเซ็นแบบเงียบ**
- **C21 (v2.1): Value Stream — §12.1 มี upstream + Downstream Impact Map ที่ตอบ "แล้วไงต่อ" ได้ทุกแถว**
- **C22 (v2.1): ตัวชี้วัด §2.3 ทุกตัวมี baseline/target/วิธีวัด + มีคู่ใน §17.3**
- **C23 (v2.1): §9.5 marker 🤖/✅ ครบ — 🤖 ระดับสูงลง OQ แล้ว**
- (Philosophy Embed Checks) PE01-PE05:
  - PE01: COSO Roles ครบทุก step ใน Section 5
  - PE02: SoD ผ่าน (Maker ≠ Approver)
  - PE03: Security Preset เลือกแล้ว + Controls ครบ
  - PE04: SLA + KPI + Threshold ใน Section 17 ครบ
  - PE05: Cross-section coverage ผ่าน (BC↔Edge, Control↔Health, Metric↔Monitoring)

**7.4 สร้าง AI Review Report:**

```
═══════════════════════════════════════
AI REVIEW REPORT — BRD Generator Full
═══════════════════════════════════════
BRD: [BRD ID] — [ชื่อ Feature]
ประเภท: [ประเภท]
วันที่ตรวจ: [วันที่]

CHECKLIST RESULTS:
───────────────────────────────────────
✅ C01: Business Objective ชัดเจน วัดผลได้
✅ C02: User Roles ครบ
❌ C05: Story Breakdown — S-03 มีคำว่า "และ" ต้องแยก
⚠️ C10: R11 ยังไม่ติด Tag
✅ PE01: COSO Roles ครบ
✅ PE02: SoD ผ่าน
...

SUMMARY:
───────────────────────────────────────
ผ่าน: 22/24
ไม่ผ่าน: 2/24

สถานะ: ⚠️ NEEDS REVISION

ต้องแก้:
1. C05: แยก Story S-03
2. C10: ติด Tag R11

แก้แล้วเรียก skill นี้ใหม่ได้
```

**7.5 ตั้งสถานะเอกสาร:**
- ✅ **APPROVED** → ทุกข้อผ่าน → พร้อมเข้า frd-generator-v6
- ⚠️ **NEEDS REVISION** → ผ่านบางส่วน → ระบุข้อที่ต้องแก้
- ❌ **MAJOR REVISION** → ไม่ผ่านเกินครึ่ง → กลับไปทำ Step ที่เกี่ยวข้องใหม่

---

### Step 8 — Generate Outputs

**8.1 Save .md:**
```
/mnt/user-data/outputs/BRD_[feature_name].md
```

**8.2 Generate .docx:**
ใช้ `scripts/md_to_docx.py` หรือ python-docx โดยตรง

```bash
python /home/claude/brd-generator-full/scripts/md_to_docx.py \
  /mnt/user-data/outputs/BRD_[feature].md \
  /mnt/user-data/outputs/BRD_[feature].docx \
  "[ชื่อ Feature]"
```

**8.3 Present 2 ไฟล์ + AI Review Report:**

ใช้ `present_files` แสดง:
1. `BRD_[feature].md` (สำหรับ AI / frd-generator-v6)
2. `BRD_[feature].docx` (สำหรับมนุษย์อ่าน)

บอก next step:
- ถ้า APPROVED → "BRD พร้อมส่งเข้า frd-generator-v6 แล้ว"
- ถ้า NEEDS REVISION → "แก้ [จำนวน] ข้อ แล้วเรียก skill นี้ใหม่"
- ถ้า MAJOR REVISION → "แนะนำกลับไปทำ Step [X] ใหม่"

---

## 🚨 Critical Rules

### R1: ห้ามเดาข้อมูล
- ถ้า RIF ไม่มี + user ไม่ตอบ → ใส่ Section 15 Open Questions
- ห้ามเขียน "TBD" — ใส่ใน Open Questions แทน
- ห้ามแต่ง business rule ที่ไม่มีใน source

### R2: COSO ในทุก Step ของ Section 5
- ทุก step ระบุ Maker / Checker / Approver / System
- SoD บังคับ: Maker ≠ Approver

### R3: Tag ทุก Rule ที่มีตัวเลข/เงื่อนไข
- FIXED / CONFIGURABLE / DYNAMIC / WARNING
- ตรวจ Misclassification Patterns

### R4: Cross-Section Coverage
- BC ↔ Edge Cases / Scenarios
- Control ↔ Health Check Control Points
- Metric ↔ Monitoring Widget/Report

### R5: Output 2 Files Always
- `.md` + `.docx` เสมอ
- บันทึกที่ `/mnt/user-data/outputs/`

### R6: Quality Gate Mandatory
- ทุก BRD ต้องผ่าน Step 7 ก่อนปิด skill
- ถ้าไม่ผ่าน → return NEEDS REVISION report → ไม่ generate .docx

### R7: Conflict Resolution
- RIF > REQ_PHILO > Feature Brief
- ห้ามแต่ง spec ที่ไม่มีในใด source ใด

### R8: Philosophy Embed บังคับใน New Feature + Enhancement
- ไม่ใช่ optional
- Bug Fix / Config/Chore → ย่อ (ตัด Section 17-18)

### R9: Revision Mode — Critical Drift Decision ⭐ ใหม่
- ทุก Critical Drift ต้องผ่าน Step R2 (ถาม user) ก่อน apply
- ห้าม auto-apply Critical Drift เด็ดขาด — แม้ user ดูเหมือนตั้งใจ
- User decision ต้อง document ใน Changelog v[N] entry
- ถ้า user ไม่ตอบ → save BRD ไม่ได้, return NEEDS REVISION

### R10: Revision Mode — Preserve Untouched Sections ⭐ ใหม่
- Section ที่ไม่ drift → copy verbatim จาก BRD v1
- ห้าม "ปรับปรุง" หรือ rewrite section ที่ไม่กระทบ — ทำให้ audit trail สับสน
- เฉพาะ Section 1 Changelog ที่ update เสมอ + Section ที่ระบุใน Drift Report
- Output `_DRIFT_REPORT.md` ระบุชัดว่า section ไหน "preserved" vs "updated"

### R11: UI หยาบเท่านั้น — Design Authority อยู่ที่ FRD ⭐ v2.1
- BRD ระบุแค่ Screen Inventory หยาบ (ชื่อหน้า/ประเภท business/ผู้ใช้/หน้าที่/จำนวนหน้า) + UI signals
- **ห้าม** ระบุ Layout Template ID, pattern, สี, ขนาด, iron rules — เป็นหน้าที่ frd-generator-v6 (Design Authority) + html-generator-v6 (enforce)
- RIF ระบุ NON-STANDARD explicit → ส่งต่อ flag + Open Question เท่านั้น ไม่ตัดสินเอง

### R12: Scope Lock Inheritance ⭐ v2.1
- `scope_lock_ref` + LOCK-XX จาก RIF ต้องโผล่ใน Section 3.4 ครบ
- In Scope เกินใบเซ็น/ชน Exclusions → flag SCOPE DRIFT + Open Question — ห้ามใส่เงียบ ห้ามตัดเงียบ
- LOCK ห้าม override — ขัดกันเมื่อไหร่ LOCK ชนะ + รายงานใน AI Review

### R13: Value Stream Awareness ⭐ v2.1
- New Feature/Enhancement ต้องมี Section 12.1 (VS positioning + Upstream + Downstream Impact Map) — ทุกแถวตอบ "แล้วไงต่อ" ได้
- Downstream ที่ระบุไม่ได้/ไม่แน่ใจ → Open Question ไม่ใช่ละไว้

## 📋 Output Validation Checklist

ก่อนปิด skill ต้องตอบได้ทุกข้อ:

### Document Structure
- [ ] Section 1: Document Info ครบ
- [ ] Section 2: Business Context (ปัญหา, เป้าหมาย, ตัวชี้วัด)
- [ ] Section 3: Scope (In/Out + Assumptions)
- [ ] Section 4: User Roles & Permissions
- [ ] Section 5: User Journey + **COSO ทุก step**
- [ ] Section 6: Data Entity & Fields + ER Diagram
- [ ] Section 7: User Stories + AC (Given-When-Then)
- [ ] Section 8: Status & Lifecycle + State Diagram
- [ ] Section 9: Business Rules + **Tags ครบ**
- [ ] Section 9.5: สรุประดับความยืดหยุ่น
- [ ] Section 10: Edge Cases (10.1 BA + 10.2 AI)
- [ ] Section 11: Impact / Regression (Enhancement)
- [ ] Section 12.3: Existing System Reference
- [ ] Section 13: Delivery Phases (1-4)
- [ ] Section 14: Dev Summary "ใบสั่ง"
- [ ] **Section 14.6: Screen Inventory + UI Signals** (หยาบ — ส่งต่อ FRD)
- [ ] Section 15: Open Questions
- [ ] Section 16: Security & Compliance (Preset + 78 Controls)
- [ ] Section 17: Health Check (SLA/KPI/Threshold)
- [ ] Section 18: Monitoring (Reports/Widgets)
- [ ] Section 12.1: Value Stream & Downstream Impact ครบ

### Screen Inventory (หยาบ) + Business Completeness ⭐ v2.1
- [ ] Screen Inventory ครบทุกหน้า — ชื่อ/ประเภท business/ผู้ใช้/หน้าที่ (ไม่มี Layout Template ID/pattern/สี)
- [ ] **(v2.2 — เมื่อมี HTML)** ทุกแถวใน Inventory มี route จริงจาก HTML · จำนวนหน้าใน Inventory = จำนวนหน้าใน HTML เป๊ะ · drift ทุกจุดถูก flag ไม่ใช่แก้เงียบ
- [ ] UI signals ส่งต่อ FRD ครบ (Doc/Transaction? print? NON-STANDARD flag?)
- [ ] **Section 3.4 Scope Lock:** scope_lock_ref + LOCK-XX ครบจาก RIF — SCOPE DRIFT (ถ้ามี) flag เป็น OQ
- [ ] **Section 2.3 ตัวชี้วัด:** ทุกตัวมี Baseline/Target/วิธีวัด — ไม่มีตัวชี้วัดลอย
- [ ] **Section 12.1 Value Stream:** positioning + upstream + Downstream Impact Map ครบ ทุกแถวตอบ "แล้วไงต่อ"
- [ ] **Section 9.5:** ทุก rule มี marker 🤖/✅ — 🤖+DYNAMIC/Engine อยู่ใน OQ ครบ

### Cross-Pillar (Philosophy)
- [ ] BC ทุกข้อมี Edge Case cover
- [ ] Control runtime ทุกตัวมี Control Point
- [ ] Metric ทุกตัวมี Widget/Report

### Quality Gate
- [ ] AI Review Checklist รันครบ
- [ ] สถานะระบุชัดเจน (APPROVED/NEEDS REVISION/MAJOR REVISION)
- [ ] AI Review Report สร้างแล้ว

### Output
- [ ] บันทึก `.md` ที่ /mnt/user-data/outputs/
- [ ] บันทึก `.docx` ที่ /mnt/user-data/outputs/
- [ ] Present 2 ไฟล์ + AI Review Report

---

## 📚 Reference Files

| File | Purpose |
|---|---|
| `references/brd-template-v3.md` | โครงสร้าง BRD 18 sections |
| `references/brd-types.md` | 4 ประเภท + Section coverage matrix |
| `references/change-likelihood-tags.md` | FIXED/CONFIGURABLE/DYNAMIC/WARNING + Misclassification Patterns |
| `references/edge-case-patterns.md` | Patterns 9 หมวด (FU/CA/EM/DI/CL/ST/PD/PM/EN) |
| `references/flexibility-questionnaire-guide.md` | คำถาม Stakeholder + วิเคราะห์ระดับ |
| `references/erp-data-patterns.md` | 11 หมวด data patterns |
| `references/philosophy-embed-guide.md` | คู่มือ embed COSO/Security/Health/Monitoring |
| `references/health-monitoring-patterns.md` | Patterns สำหรับ Section 17 + 18 |
| `references/ai-review-checklist.md` | C01-C23 (รวม C20-C23 v2.1) + CE/CB/CC + PE01-PE05 + CR01-CR05 |
| `references/revision-mode-guide.md` ⭐ | คู่มือ Drift Detection + Classification + Critical Decisions |
| `references/layout-enforcement-guide.md` | [DEPRECATED v2.1] — Design Authority ย้ายไป frd-generator-v6 (เหลือ stub กันหยิบกลับมาใช้) |
| `knowledge/coso-defaults.md` | COSO defaults ตาม module type |
| `knowledge/security-presets.md` | 12 presets (P1-P10/P-MAX/P-MIN/Custom) |
| `knowledge/security-78-controls.md` | 78 controls × 14 standards |
| `knowledge/cube-defaults.md` | CUBE business defaults |
| `scripts/md_to_docx.py` | Converter `.md` → `.docx` |

---

## 🔄 Comparison vs Skills เดิม

| มิติ | brd-generator-full (ใหม่) | 6 Skills เดิม |
|---|---|---|
| จำนวน skill | 1 | 6 |
| Input | RIF เป็นหลัก + optional | ต่อ skill ต่างกัน |
| Philosophy | Embedded ใน BRD | แยก skill REQ_PHILO |
| Quality Gate | Built-in step 7 | แยก skill (finalizer) |
| Output | 2 files + Review Report | กระจาย |
| ใช้กับ pipeline | Cowork Automation ตรง | ต้อง orchestrate เอง |
| Revision (HTML→BRD) | **Built-in Revision Mode** ⭐ | ไม่มี — ต้องเขียนใหม่ |

## 🎓 Quick Start

### Fresh Mode (BRD ใหม่)
```
User: "สร้าง BRD จาก RIF นี้" + แนบ RIF_xxx.md

Skill:
  1. อ่าน RIF → ระบุ Type
  2. ถ้าไม่ระบุ → ถาม (New Feature / Enh / Bug / Config)
  3. รัน Step 1-7 ตาม type
  4. Quality Gate → APPROVED?
     ✅ → generate .docx + present
     ❌ → report + แนะนำแก้
```

### Revision Mode (Sync HTML กลับ BRD) ⭐ ใหม่
```
User: "Sync HTML นี้กลับ BRD" + แนบ HTML_quotation_v2.html + BRD_quotation.md

Skill:
  R1. Drift Detection — diff HTML vs BRD → classify (UX/Hidden/Business/Critical)
  R2. ถ้ามี Critical → ถาม user 1 รอบ
  R3. Impact Analysis — หา sections ที่กระทบ + re-evaluate tags + philosophy
  R4. Generate BRD v2 — selective update + Changelog entry
  R5. Quality Gate → APPROVED?
     ✅ → overwrite BRD + present _DRIFT_REPORT + แนะนำ downstream regenerate
     ❌ → return NEEDS REVISION
```
