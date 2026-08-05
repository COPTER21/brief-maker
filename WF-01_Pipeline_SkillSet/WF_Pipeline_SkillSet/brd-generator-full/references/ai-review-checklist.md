# AI Review Checklist — Quality Gate

ใช้ใน Step 7 (Quality Gate) ของ brd-generator-full
แบ่งตามประเภท BRD: C (Core), CE (Enhancement), CB (Bug Fix), CC (Config/Chore), PE (Philosophy Embed)

---

## Core Checklist (C01-C19) — สำหรับ New Feature + Enhancement

### Document Foundation

**C01: Business Objective ชัดเจน วัดผลได้**
- ✅ มี Section 2.2 (เป้าหมาย) + Section 2.3 (ตัวชี้วัด)
- ❌ ถ้ามีแค่ "ทำให้ดีขึ้น" / "ปรับปรุง" โดยไม่มีตัวเลข

**C02: User Roles ครบ**
- ✅ Section 4 มี Role × Action matrix
- ❌ ถ้าระบุ "user" รวมๆ ไม่แยก role

**C03: Scope (In/Out) ชัดเจน**
- ✅ Section 3 มีทั้ง In Scope + Out of Scope + Assumptions
- ❌ ถ้ามีแค่ In Scope ไม่มี Out of Scope

### Stories & Flow

**C04: User Journey มี Happy Path + Alt Path**
- ✅ Section 5 มี Happy Path + อย่างน้อย 1 Alternative Path
- ❌ ถ้ามีแค่ flow เดียว ไม่ครอบคลุม reject/escalate

**C05: Story Breakdown ไม่มีคำว่า "และ"**
- ✅ ทุก Story description ใน Section 7 อ่านแล้วเป็น single action
- ❌ ถ้าเจอ "และ" ใน description → ต้องแยก Story

**C06: Acceptance Criteria แบบ Given-When-Then**
- ✅ ทุก Story มี AC อย่างน้อย 2 ข้อ format GWT
- ❌ ถ้าเป็น text สั้นๆ ไม่มี structure

### Data & Status

**C07: Data Entity ครบ + ER Diagram**
- ✅ Section 6 มี Entity Tables + ER Diagram
- ❌ ถ้ามีแค่ field list ไม่มี relationship

**C08: Audit Fields ทุก Entity**
- ✅ ทุก entity มี created_by, created_date, modified_by, modified_date
- ❌ ถ้าขาด audit fields

**C09: Status & Lifecycle มี State Diagram**
- ✅ Section 8 มี state diagram + transition table
- ❌ ถ้ามีแค่ list status

### Rules & Validation

**C10: Business Rules ติด Tag ทุกข้อที่มีตัวเลข/เงื่อนไข**
- ✅ Section 9 ทุก rule ที่มีตัวเลข/เงื่อนไข มี Tag (FIXED/CONFIGURABLE/DYNAMIC/WARNING)
- ❌ ถ้ามี rule กับตัวเลขแต่ไม่ติด Tag

**C11: ระดับความยืดหยุ่นชัดเจน (Section 9.5)**
- ✅ ทุก CONFIGURABLE/DYNAMIC มีระดับ (Config File / Admin Panel / Rule Management / Engine Management)
- ❌ ถ้ามีแค่ Tag ไม่มีระดับ

**C12: Validation Rules ครบ**
- ✅ Section 9.2 ครอบคลุมทุก field สำคัญ
- ❌ ถ้าขาด validation สำหรับ required fields

### Edge Cases

**C13: Edge Cases ครบหมวด**
- ✅ Section 10 มี Edge Cases อย่างน้อย 3 หมวด (ตาม patterns)
- ❌ ถ้ามีแค่ happy path เดียว ไม่มี edge

**C14: Edge Cases แยก BA-confirmed + AI-suggested**
- ✅ Section 10.1 (BA) + 10.2 (AI with ☐ checkbox)
- ❌ ถ้าเอาทุก edge case ผสมกัน

### Dependencies & Existing

**C15: Dependencies ระบุครบ**
- ✅ Section 12 มี Module + External dependencies
- ❌ ถ้ามีแค่ list ไม่อธิบาย relation

**C16: Existing System Reference (ถ้ามี Registry)**
- ✅ Section 12.3 ระบุว่าอะไร Reuse / สร้างใหม่
- ⚠️ ถ้าไม่มี Registry → ใส่ placeholder + warn

### Delivery & Summary

**C17: Delivery Phases (1-4)**
- ✅ Section 13 จัด Phase + ระบุงานต่อ Phase
- ❌ ถ้ามีแค่ "ทำทุกอย่างพร้อมกัน"

**C18: WARNING ทุกข้อมีแผนหารือ**
- ✅ ทุก WARNING ใน Section 9 หรือ 15 ระบุ "หารือกับใคร + เมื่อไหร่"
- ❌ ถ้ามี WARNING ค้างโดยไม่ระบุแผน — **บังคับ Block ไม่ผ่าน**

**C19: Section 14 Dev Summary "ใบสั่ง" ครบ**
- ✅ Section 14.1-14.4 (+ 14.5 ถ้า Enhancement)
- ❌ ถ้ามีแค่ "ดู Section อื่นเอา"

---

## Enhancement Checklist (CE01-CE03)

**CE01: ของเก่า vs ของใหม่ ครบทุก Section ที่เปลี่ยน**
- ✅ ทุก Section ที่ระบุ "ของใหม่" มี "ของเก่า" คู่ด้วย
- ❌ ถ้าระบุแต่ "ของใหม่" ไม่ระบุ "ของเก่า"

**CE02: Regression Scope ระบุชัด (Section 11.2)**
- ✅ Feature เก่าที่ต้อง Test ซ้ำ ระบุครบ + เหตุผล
- ❌ ถ้าเขียน "test ทุกอย่าง" รวมๆ

**CE03: Migration Plan (ถ้ามี data ที่ต้อง migrate)**
- ✅ ระบุว่า existing data ต้อง migrate อย่างไร (fill default / grandfather / convert)
- ❌ ถ้าขาด migration plan สำหรับ schema change

---

## Bug Fix Checklist (CB01-CB03)

**CB01: Expected vs Actual + Reproduce Steps**
- ✅ ระบุ Expected behavior + Actual behavior ชัดเจน
- ✅ Reproduce Steps ทำตามได้
- ❌ ถ้าขาดอย่างใดอย่างหนึ่ง — **บังคับ Block**

**CB02: Impact Analysis + Affected Users/Data**
- ✅ ระบุกระทบใคร + กระทบ data ยังไง
- ❌ ถ้ามีแค่ "bug มีปัญหา"

**CB03: Regression Test ที่เพิ่ม**
- ✅ ระบุ Test Case ที่ต้องเพิ่มเพื่อป้องกัน bug กลับมา
- ❌ ถ้าไม่ระบุ Test ใหม่

---

## Config/Chore Checklist (CC01-CC04)

**CC01: ค่าเก่า → ค่าใหม่ ชัดเจน**
- ✅ ตาราง Setting × ค่าเก่า × ค่าใหม่
- ❌ ถ้ามีแค่ "ปรับ config"

**CC02: เหตุผล + ผลกระทบ**
- ✅ ระบุเหตุผลที่ต้องเปลี่ยน + กระทบอะไร
- ❌ ถ้าขาดอย่างใดอย่างหนึ่ง

**CC03: ผู้อนุมัติ Config Change**
- ✅ ระบุชื่อ + role ของผู้อนุมัติ
- ❌ ถ้าไม่ระบุ

**CC04: ตรวจว่าควรยกระดับเป็น Enhancement?**
- ✅ ระบุ assessment ว่า "Config นี้กระทบวงกว้าง — ควรยกระดับเป็น Enhancement?" หรือ "ไม่ต้องยกระดับ"
- ⚠️ ถ้ากระทบวงกว้างแต่ทำเป็น Config → แนะนำ user แต่ไม่ Block

---

## Philosophy Embed Checklist (PE01-PE05) — สำหรับ New Feature + Enhancement

**PE01: COSO Roles ครบทุก Step ใน Section 5**
- ✅ ทุก row ใน User Journey table มี 4 columns: Maker / Checker / Approver / System
- ❌ ถ้ามี step ที่ขาด COSO column

**PE02: SoD ผ่าน (Maker ≠ Approver)**
- ✅ ทุก approval step Maker ≠ Approver
- ❌ ถ้าเจอ row ที่ Maker = Approver — **บังคับ Block**

**PE03: Security Preset เลือกแล้ว + Controls Checklist ครบ**
- ✅ Section 16.1 ระบุ preset
- ✅ Section 16.2 ระบุ 14 standards (✅/❌)
- ✅ Section 16.3 มี Control Checklist
- ✅ Section 16.4 มี Risk Statement อย่างน้อย 3 risks
- ❌ ถ้าขาดข้อใดข้อหนึ่ง

**PE04: Section 17 ครบ (SLA + KPI + Threshold + Throughput)**
- ✅ Section 17.1 SLA อย่างน้อย 1 step
- ✅ Section 17.2 Control Points map จาก Section 16
- ✅ Section 17.3 KPI อย่างน้อย 3 ตัว
- ✅ Section 17.4 Threshold ระบุ Min/Max
- ✅ Section 17.5 Throughput (Capacity/Baseline/Stress)
- ❌ ถ้าขาดข้อใดข้อหนึ่ง

**PE05: Cross-Section Coverage ผ่าน**
- ✅ ทุก BC ใน Section 9 มี Edge Case cover ใน Section 10
- ✅ ทุก runtime Control ใน Section 16 มี Control Point ใน Section 17.2
- ✅ ทุก SLA/KPI/Threshold ใน Section 17 มี Widget/Report ใน Section 18
- ❌ ถ้าขาด coverage ข้อใดข้อหนึ่ง

---

## Revision Mode Checklist (CR01-CR05) — สำหรับ Step R4

**CR01: Changelog v[N] entry ครบทุก field**
- ✅ Section 1 Changelog มี entry ใหม่ ระบุ: version, date, source HTML file, drift summary
- ✅ Sections updated + Sections preserved list ครบ
- ❌ ถ้าขาด หรือ "v1.1: revised" สั้น ๆ โดยไม่มี detail

**CR02: Critical Drifts ทุกข้อมี user decision documented**
- ✅ ทุก Critical drift มี entry ใน Changelog ระบุ user decision (Confirm / Revert / Discuss)
- ❌ ถ้ามี Critical drift apply โดยไม่มี user decision — **บังคับ Block**
- ❌ ถ้า user decision = "Discuss" แต่ apply ไปแล้ว

**CR03: Sections preserved ไม่ถูก touch โดยไม่จำเป็น**
- ✅ Sections ที่ระบุ "PRESERVE" ใน _DRIFT_REPORT ตรงกับ BRD v1 100%
- ❌ ถ้า section ที่ไม่กระทบถูก rewrite (audit trail สับสน)

**CR04: Tag Changes มี Migration Plan**
- ✅ ทุก Rule ที่ Tag เปลี่ยน (FIXED→CONFIGURABLE→DYNAMIC) มี entry ใน §13 Delivery Phases ระบุ phase ที่ implement
- ✅ §14 Dev Summary ระบุ migration scope (existing data, refactor needed)
- ❌ ถ้า Tag เปลี่ยนแต่ Phase ไม่ update

**CR05: Philosophy Embed ยังครบหลัง Revision**
- ✅ COSO Roles ครบทุก step (รวม step ที่เพิ่ม)
- ✅ SoD ผ่าน (Maker ≠ Approver)
- ✅ Security Preset ยังเหมาะกับ feature (re-evaluate ถ้ามี sensitive field ใหม่)
- ✅ SLA/KPI/Threshold cover action ใหม่
- ✅ Monitoring widget cover metric ใหม่
- ❌ ถ้า drift apply แต่ Philosophy embed ขาด coverage

---

## Business Completeness Checklist (C20-C23) — v2.1 (แทน CLE เดิม — Layout ย้ายไป FRD)

**C20: Scope Lock**
- ✅ §3.4 มี scope_lock_ref + LOCK-XX ครบตาม RIF §16.3
- ✅ ไม่มี In Scope เกินใบเซ็นแบบเงียบ — SCOPE DRIFT ทุกข้อมี OQ คู่
- ❌ ถ้างานผ่าน chain แต่ §3.4 ว่าง → FAIL

**C21: Value Stream & Downstream**
- ✅ §12.1 มี positioning + document flow chain + upstream + Downstream Impact Map
- ✅ ทุกแถว downstream ตอบได้: ข้อมูลอะไรไหลไป / trigger อะไร / แก้-ยกเลิกกลางทางกระทบยังไง
- ⚠️ ระบุไม่ได้ → ต้องเป็น OQ ไม่ใช่เว้นว่าง

**C22: ตัวชี้วัดวัดได้จริง**
- ✅ §2.3 ทุกตัวมี Baseline / Target / วิธีวัด / จังหวะวัด
- ✅ ทุกตัวมีคู่ใน §17.3 KPI
- ❌ ตัวชี้วัดลอย ("ดีขึ้น/เร็วขึ้น" ไม่มีตัวเลข) → FAIL

**C23: Flexibility Attribution**
- ✅ §9.5 ทุก rule มี marker 🤖/✅
- ✅ 🤖 + DYNAMIC/Engine Management → อยู่ใน §15 OQ ครบ


## Verdict Logic

```
นับผลการตรวจ:
- ผ่าน (✅): pass_count
- ไม่ผ่าน (❌): fail_count
- เตือน (⚠️): warn_count

Verdict:
- fail_count == 0 → ✅ APPROVED
- fail_count > 0 AND fail_count <= total_checks / 2 → ⚠️ NEEDS REVISION
- fail_count > total_checks / 2 → ❌ MAJOR REVISION

Override:
- ถ้า C18 ไม่ผ่าน → บังคับ NEEDS REVISION (WARNING ค้างไม่ผ่าน)
- ถ้า PE02 ไม่ผ่าน → บังคับ NEEDS REVISION (SoD violation)
- ถ้า CB01 ไม่ผ่าน (Bug Fix) → บังคับ MAJOR REVISION (no reproduce)
- ถ้า CR02 ไม่ผ่าน (Revision Mode) → บังคับ MAJOR REVISION (Critical drift apply โดยไม่มี user decision)
- ถ้า CR03 ไม่ผ่าน (Revision Mode) → บังคับ NEEDS REVISION (preserved section ถูก touch)
- ถ้า C20/C22 ไม่ผ่าน → บังคับ NEEDS REVISION (scope/metric violation)
- ถ้า C21/C23 ไม่ผ่าน → NEEDS REVISION (business completeness)
- (CLE01-CLE09 retired v2.1 — Layout ย้ายไป FRD; ใช้ C20-C23 แทน)
```

### Checklist by Mode

| Mode | Checklist ที่รัน |
|---|---|
| Fresh — New Feature | C01-C23 + PE01-PE05 |
| Fresh — Enhancement | C01-C23 + CE01-CE03 + PE01-PE05 |
| Fresh — Bug Fix | CB01-CB03 |
| Fresh — Config/Chore | CC01-CC04 |
| **Revision Mode** ⭐ | (existing checklist of original type) + **CR01-CR05** + C20-C23 (re-validate) |

---

## AI Review Report Template

```markdown
═══════════════════════════════════════
AI REVIEW REPORT — brd-generator-full
═══════════════════════════════════════
BRD: [BRD ID] — [Feature Name]
ประเภท: [New Feature / Enhancement / Bug Fix / Config/Chore]
วันที่ตรวจ: [YYYY-MM-DD HH:mm]
Total Checks: [N]

CORE CHECKLIST (C01-C19)
───────────────────────────────────────
✅ C01: Business Objective ชัดเจน
✅ C02: User Roles ครบ
✅ C03: Scope ชัดเจน
✅ C04: User Journey มี Alt Path
❌ C05: Story Breakdown — S-03, S-07 มีคำว่า "และ" ต้องแยก
✅ C06: AC แบบ GWT
✅ C07: Data Entity + ER Diagram
✅ C08: Audit Fields ครบ
✅ C09: State Diagram มี
⚠️ C10: R11 ไม่มี Tag → แนะนำ CONFIGURABLE
✅ C11: ระดับความยืดหยุ่นชัดเจน
✅ C12: Validation Rules ครบ
✅ C13: Edge Cases ครบหมวด
✅ C14: แยก BA + AI edge cases
✅ C15: Dependencies ครบ
⚠️ C16: ไม่มี System Module Registry → placeholder
✅ C17: Delivery Phases 1-3 (Phase 4 not applicable)
✅ C18: WARNING ทุกข้อมีแผน
✅ C19: Section 14 ใบสั่งครบ

PHILOSOPHY EMBED CHECKLIST (PE01-PE05)
───────────────────────────────────────
✅ PE01: COSO Roles ครบทุก step
✅ PE02: SoD ผ่าน
✅ PE03: Security Preset P1 + Controls 12/12
✅ PE04: Section 17 ครบ 5 sub-sections
✅ PE05: Cross-section coverage ผ่าน

ENHANCEMENT-SPECIFIC (CE01-CE03)
───────────────────────────────────────
[ถ้าเป็น Enhancement]

SUMMARY
───────────────────────────────────────
ผ่าน: 22/24
ไม่ผ่าน: 1/24
เตือน: 2/24 (informational)

สถานะ: ⚠️ NEEDS REVISION

ต้องแก้:
1. C05: แยก Story S-03 และ S-07
2. C10: ติด Tag R11 (แนะนำ CONFIGURABLE)

หมายเหตุ:
- C16: ขอ System Module Registry เพื่อปรับ Section 12.3 ให้สมบูรณ์ขึ้น (ไม่บังคับ)

แก้ตามรายการแล้วเรียก brd-generator-full ใหม่ได้ครับ
```
