---
name: feature-context-pack
description: "สร้าง Feature Context Card — .md ไฟล์เดียวต่อ feature (CTX_[F-XXX].md) ที่ extract จาก FRD Pack เป็น technical contract ฉบับย่อ (Summary + Data Contract + API Surface + Cross-boundary Rules + Integration) ไว้แนบเป็น reference เวลาออกบรีฟ feature อื่น หรือส่ง context ให้ AI ตัวอื่น แทนการโยน FRD เต็มทั้ง pack — เบากว่า ประหยัด token กว่า แต่ derive จาก FRD 100% ห้าม invent ใช้เมื่อ user พูดถึง 'สร้าง context pack', 'ทำ context card', 'feature-context-pack', 'CTX ของ feature', 'สรุป context ให้ feature อื่นใช้', 'ทำ ref ของ feature', 'extract context จาก FRD', 'แนบ context แทน FRD', 'สรุป db api ของ feature เดิม', 'context ของฟีเจอร์เดิม', 'ทำไฟล์ ref สำหรับบรีฟ', 'update CTX', 'regen context card' — ใช้ทุกครั้งหลัง FRD ของ feature เสร็จ (หรือถูก revise) แล้วต้องการ context card สำหรับ cross-feature reference แม้ user ไม่เรียกชื่อ skill ตรงๆ Output: CTX_[F-XXX].md ไฟล์เดียวต่อ feature รองรับ batch หลาย FRD Pack ในรอบเดียว"
---

# Feature Context Pack Generator

## Purpose

แปลง **FRD Pack (1 feature)** → **Context Card (.md 1 ไฟล์)** = technical contract ฉบับย่อของ feature

ใช้เป็น **cross-feature reference**: เวลาออกบรีฟ feature ใหม่ หรือรัน pipeline/AI ตัวอื่นที่ต้องรู้ว่า feature เดิมมีอะไร — แนบ CTX แทน FRD เต็ม

**ทำไมต้องมี skill นี้:**
- FRD Pack เต็มหนักมาก (6-9 ไฟล์ รวม UI/microcopy/tests) → กิน token มหาศาลเวลาแนบเป็น context
- คนออกบรีฟ feature B ต้องรู้แค่ **interface** ของ feature A (entities, keys, API, shared rules) — ไม่ต้องรู้ internals
- ป้องกันออกแบบซ้ำ / entity ชน / rebuild สิ่งที่มี API ให้เรียกอยู่แล้ว
- 1 ไฟล์ต่อ feature → แนบง่าย ส่งไปมาง่าย ไม่มีปัญหาแนบไม่ครบ

**หลักการแกน: EXTRACT + COMPRESS — ไม่ generate ใหม่**
ทุกบรรทัดใน CTX ต้อง trace กลับไป FRD ได้ ห้ามเขียนสิ่งที่ FRD ไม่มี

---

## When to Use

✅ FRD Pack ของ feature เสร็จแล้ว (ผ่าน frd-generator) → gen CTX ต่อท้าย pipeline
✅ FRD ถูก revise (เช่นผ่าน html-to-frd-sync) → regen CTX ให้ version ตรง
✅ Batch: มีหลาย FRD Pack ต้องการ CTX ครบทุก feature ในรอบเดียว
✅ กำลังจะออกบรีฟ feature ใหม่ แล้วต้องเตรียม context ของ features เดิมที่เกี่ยวข้อง

❌ ห้ามใช้ถ้ายังไม่มี FRD — ยังไม่มี source of truth ให้ extract (ใช้ frd-generator ก่อน)
❌ ไม่ใช่ vs-feature-handover-pack — ตัวนั้นแตกจาก VS Bible (pre-BRD ขาไป) · ตัวนี้ derive จาก FRD (post-FRD ขากลับ)
❌ ไม่ใช่ feature-tldr-html — ตัวนั้นสรุปภาษาคนให้มนุษย์อ่าน · ตัวนี้เป็น technical contract ให้ AI/BA ใช้ต่อ

---

## Input

**Required:**
- FRD Pack ของ feature (แนบ folder หรือไฟล์หลัก) — โดยเฉพาะ:
  - `02_API` — endpoints, payloads, events
  - `04_DB` — entities, fields, keys, enums, relationships
  - `05_RULES` — business rules
  - หัว FRD — feature id, name, version, module

**Optional (ช่วยให้ section 5 แม่นขึ้น):**
- BRD (§ Downstream Impact / Value Stream Impact)
- Declaration briefs: `DOA_BRIEF`, `NTF_BRIEF`, `CSQ_BRIEF`, `DOCCFG_BRIEF`
- WAVE_PLAN / workflow_graph.json (dependency ระหว่าง feature)

**Batch mode:** แนบหลาย FRD Pack → ได้ CTX ครบทุกตัว ไม่ต้องสั่งทีละ feature

---

## Output

```
CTX_[F-XXX-NNN].md          ← 1 ไฟล์ต่อ feature จบในตัว
```

Batch → หลายไฟล์ + `_CTX_INDEX.md` (list ทุก CTX + version ที่ derive)

**Size budget: ~150-400 บรรทัดต่อ feature** — ถ้าเกิน 400 แปลว่า compress ไม่พอ ไม่ใช่ feature ใหญ่

---

## CTX Template (โครงบังคับ)

```markdown
# CTX — [F-XXX-NNN]: [Feature Name]

> **derived from:** FRD_[F-XXX-NNN] v[N] · **generated:** [YYYY-MM-DD]
> **module:** [module] · **status:** [active / superseded]
> ⚠ Derived artifact — source of truth คือ FRD · ถ้า FRD revise ต้อง regen CTX

---

## 1. Summary
[3-5 บรรทัด: ทำอะไร · ใครใช้ · trigger จากไหน · จบที่ผลลัพธ์อะไร]
[ภาษา business กระชับ — ไม่เล่า flow ละเอียด]

## 2. Data Contract
### Entities
| Entity | PK | Key Fields | หมายเหตุ |
|---|---|---|---|
| [entity] | [pk] | [fields ที่ feature อื่นน่าจะ join/อ่าน] | |

### Enums / States
| Field | Values | Transition owner |
|---|---|---|
| status | draft → submitted → approved → ... | feature นี้ |

### Relationships
- [entity_a] 1—N [entity_b] (fk: ...)
- อ้าง master: [M_XXX ที่ feature นี้อ่าน — ระบุว่าอ่านอย่างเดียวหรือเขียน]

## 3. API Surface
| Method | Endpoint | ทำอะไร | Payload หลัก |
|---|---|---|---|
| POST | /api/... | ... | { field, field } |

### Events emitted
| Event | Trigger point | Payload key |
|---|---|---|
| [event] | [state transition ไหน] | [ids] |

## 4. Shared Rules (cross-boundary เท่านั้น)
| Rule ID | Rule | กระทบใคร |
|---|---|---|
| R-XX | [rule ที่ feature อื่นต้อง conform เช่น เลขรัน, 3-way match, ห้าม delete ถ้า referenced] | [F-YYY, module] |

## 5. Integration
- **Depends on:** [F-AAA (ใช้ API/entity อะไร)]
- **Depended by:** [F-BBB (มาอ่าน/เรียกอะไรของเรา)]
- **Declarations:** DOA [yes/no + scope] · NTF [events] · CSQ [ท่อ] · DOCCFG [doc_type]
- **Engine hooks:** [ENG-DOC-NUM / ENG-NOTIFY / ฯลฯ ที่ wire]

---
*trace: §2 ← FRD 04_DB · §3 ← FRD 02_API · §4 ← FRD 05_RULES · §5 ← BRD/Briefs*
```

---

## Workflow

### Step 1: Read FRD Pack
อ่านหัว FRD (id, name, version, module) + 02_API + 04_DB + 05_RULES
ถ้า BRD / declaration briefs แนบมาด้วย → อ่านประกอบ section 5

### Step 2: Extract per section
- **§1 Summary** — จากหัว FRD + BRD objective · เขียนใหม่ให้สั้นได้ แต่ห้ามเพิ่มข้อเท็จจริง
- **§2 Data Contract** — จาก 04_DB · **compress**: เอาเฉพาะ entities + fields ที่ feature อื่นน่าจะแตะ (keys, fk, status, amount, refs) · field ประกอบ UI ล้วนๆ (เช่น note, display_order) ตัดได้ · enums/states เอาครบทุกค่า ห้ามตัด
- **§3 API Surface** — จาก 02_API · ทุก endpoint ที่ expose · payload เอาเฉพาะ key fields · internal helper ไม่ต้อง
- **§4 Shared Rules** — จาก 05_RULES · **กรองเข้มสุด**: เอาเฉพาะ rule ที่ cross-boundary (feature อื่น/module อื่นต้อง conform หรือถูกกระทบ) · rule ภายใน (validation ฟอร์ม, UI behavior) ไม่เอา
- **§5 Integration** — จาก BRD Downstream Impact + declaration briefs + dependency graph · ถ้าไม่มี source → เขียนเท่าที่ FRD ระบุ + mark `[not documented]` ห้ามเดา

### Step 3: Compress check
- นับบรรทัด → เกิน 400 = กลับไปตัด §2/§3 ให้เหลือ interface จริง
- ตรวจว่าไม่มีเนื้อหาต้องห้าม: UI spec, microcopy, test cases, wireframe, layout — **ศูนย์บรรทัด**

### Step 4: Trace stamp
- ใส่ `derived from: FRD v[N]` บนหัว + trace footer ล่างสุด
- Batch → เขียน `_CTX_INDEX.md`

### Step 5 (Update mode): FRD revised
- อ่าน FRD version ใหม่ เทียบ CTX เดิม → regen เฉพาะ section ที่กระทบ + bump version stamp
- CTX เดิมที่ derive จาก FRD version เก่า = stale ทันที ห้ามใช้ต่อ

---

## Iron Rules

| Rule | Description |
|---|---|
| **R1** | ห้าม invent — ทุกข้อเท็จจริงต้อง trace กลับ FRD/BRD/Brief ได้ · ไม่มี source → `[not documented]` |
| **R2** | 1 feature = 1 ไฟล์ CTX จบในตัว · ห้ามแตกหลายไฟล์ · ห้าม merge หลาย feature |
| **R3** | หัวไฟล์ต้องมี `derived from: FRD v[N]` เสมอ — กัน drift |
| **R4** | เนื้อหาต้องห้าม: UI spec / microcopy / test cases / layout — CTX คือ contract ไม่ใช่ spec |
| **R5** | §4 เอาเฉพาะ cross-boundary rules · rule ภายใน feature ไม่จัดเป็น context ของคนอื่น |
| **R6** | Enums/states ต้องครบทุกค่า ห้าม compress — feature อื่น conform ผิดค่าเดียวก็พัง |
| **R7** | Size ~150-400 บรรทัด · เกิน = compress ไม่พอ |
| **R8** | ห้ามใช้เป็น input แทน FRD ในงาน implement — CTX สำหรับ **บรีฟ/reference** เท่านั้น dev ทำจริงต้องอ่าน FRD |
| **R9** | FRD revise → CTX เก่า stale ทันที · regen ก่อนใช้ต่อ |
| **R10** | ชื่อไฟล์: `CTX_[F-XXX-NNN].md` ตรงตาม feature id |

---

## Integration with Pipeline

```
frd-generator (FRD Pack เสร็จ / revised)
    ↓
[feature-context-pack]  ⭐ THIS SKILL
    ↓ CTX_[F-XXX].md
    ↓
ใช้เป็น attachment:
- ออกบรีฟ feature ใหม่ (feature-prebrief / lane-brief / RIF) → แนบ CTX ของ features ที่เกี่ยว
- AI/pipeline อื่นต้องการ context ของ feature เดิม → แนบ CTX แทน FRD Pack
```

**คู่กับ html-to-frd-sync:** หลัง sync FRD version ใหม่ → รัน skill นี้ regen CTX ต่อเลย

---

## Anti-Patterns

❌ Gen CTX จาก HTML หรือความจำ — source เดียวที่ยอมรับคือ FRD (+BRD/Briefs)
❌ ยัด UI/microcopy เข้า CTX "เผื่อมีประโยชน์" — ทำให้หนักโดยไม่เพิ่ม accuracy ของบรีฟ
❌ เดา integration ที่เอกสารไม่ระบุ — mark `[not documented]` ให้คนไปเติมใน FRD แทน
❌ ใช้ CTX เก่ากับ FRD ใหม่ — เช็ค version stamp ก่อนแนบทุกครั้ง
