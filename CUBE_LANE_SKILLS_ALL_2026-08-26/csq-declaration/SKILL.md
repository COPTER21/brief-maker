---
name: csq-declaration
description: >
  Companion skill ฉีด context เรื่อง 7C Consequence (ENG-CSQ — F-CSQ-01 Consequence Engine) เข้า pipeline
  ตอนทำ FRD และ HTML ของ feature ที่ทำให้เกิดผลกระทบเฉพาะทาง (ต้นทุน/มูลค่า, ความปลอดภัยข้อมูล,
  ลงบัญชี, กระทบเงินสด-งบ, การตัดสินใจปลายทาง) แล้วออก CSQ_BRIEF_[F-xxx].md = ใบประกาศ event→ท่อ
  ที่ระบบ auto-register เข้า Profile Registry ตอน deploy — feature ประกาศเท่านั้น ห้าม hardcode
  การประทับผลรายท่อใน feature
  ★ หัวใจ: ห้ามประกาศซ้ำท่อที่มาอัตโนมัติ — OC มาจาก Operation Process (sow.*) · DC ระดับเอกสาร
  มาจาก DOA engine · SC สงวนไว้ (trigger=false เสมอ) — ประกาศซ้ำ = register ถูก reject 422
  ใช้เมื่อ user พูดถึง "csq-declaration", "ทำ CSQ brief", "ประกาศ consequence", "ผูก 7C",
  "feature นี้ยิงท่อไหน", "ประกาศ event เข้า 7C Engine", "backfill register", "เตรียม CSQ entry",
  "7c declaration" — และใช้อัตโนมัติทุกครั้งที่รัน frd-generator กับ feature ที่ติด chip ◆ ใน WAVE_PLAN
  แม้ไม่เรียกชื่อ skill
  ★ ไม่ใช่ standalone — เป็น companion (Sync Read F-CSQ-01) ★ รองรับ batch mode สำหรับ backfill
  feature ที่พัฒนาไปแล้ว
---

> **Sync Read (2026-08-25):** ทุกที่ที่อ้าง `html-generator-v9` = html-generator **เวอร์ชันสูงสุดที่ติดตั้ง**
> (`GEN=$(ls -d /mnt/skills/user/html-generator-v* | sort -V | tail -1)`) — ณ วันนี้คือ v9 (Pattern Q/P · B2 v2 · Iron Rules #1–#103)
> ห้าม hardcode CI/จำนวนกฎ/px จาก generator เก่า · FRD = frd-generator-v6 · BRD = brd-generator-full

# CSQ Declaration v1.0 — Companion Skill

> **Positioning:** F-CSQ-01 Consequence Engine = **ทะเบียนกลาง + เครื่องประเมิน** ของผลกระทบ 7 ด้านทั้งระบบ
> feature อื่น (SO/PO/GRN/Payroll/…) = **ผู้ประกาศ** ว่า "ฉันมี event แบบนี้ กระทบท่อพวกนี้ ภายใต้เงื่อนไขนี้"
> skill นี้ = **ล่าม** ที่ทำให้ FRD/HTML พูดภาษาเดียวกับ Engine ตั้งแต่วันแรก

**ตระกูลเดียวกัน:** `doa-declaration` (⚖ ใครเซ็น) · `ntf-declaration` (🔔 ใครต้องรู้) · `doccfg-declaration` (เลขเอกสาร) · **`csq-declaration` (◆ กระทบอะไร)**

---

## 🎯 ปัญหาที่ skill นี้แก้

Engine เกิดทีหลัง feature จำนวนมาก → feature ที่ทำไปแล้วไม่มีใครบอกว่า event ของมันกระทบท่อไหน
และ feature ใหม่ก็เสี่ยงจะไป **hardcode การคิดผลกระทบไว้ในตัวเอง** (เช่น คำนวณต้นทุนเองในหน้า Work Order)
ซึ่งทำให้ตัวเลขแต่ละหน้าไม่ตรงกัน และนับซ้ำ

skill นี้ทำให้:
1. **ตอน FRD** — รู้ตั้งแต่ต้นว่า event ไหนต้องยิงเข้า Engine + payload ต้องมี field อะไร
2. **ตอน HTML** — ไม่ต้องวาด UI ประเมินผลเอง (Engine เป็นคนประทับ) แต่รู้ว่าต้อง emit ตอนไหน
3. **ออก CSQ_BRIEF** — ไฟล์ที่ deploy pipeline อ่านแล้ว auto-register ได้ทันที (`POST /csq/profiles/register`)

---

## 📍 Position in Pipeline

```
LANE_BRIEF / RIF
      ↓
frd-generator-v6  ←──── ★ csq-declaration (Sync Read: §CSQ Contract + §FRD Injection)
      ↓                        │
FRD Pack                       ├─→ CSQ_BRIEF_[F-xxx].md   ← output เดียวของ skill นี้
      ↓                        │      (วางไว้ในโฟลเดอร์ FRD Pack ของ feature)
html-generator-v9 ←──── ★ csq-declaration (Sync Read: §HTML Injection)
      ↓
HTML prototype
      ↓
[deploy] pipeline อ่าน CSQ_BRIEF → POST /csq/profiles/register → status: pending → connected
      ↓
Profile Registry (แท็บใน 7C Engine) แถวนั้นเปลี่ยนเป็นเขียว = ความครบ 7C เพิ่มขึ้น 1
```

**ขอบเขตชัด ๆ**
- ✅ ทำ: ประกาศ event → ท่อ → เงื่อนไข → payload ของ feature หนึ่ง ๆ
- ❌ ไม่ทำ: register จริง (deploy pipeline ทำ) · ไม่แก้ตัว F-CSQ-01 เอง · ไม่คำนวณมูลค่าเอง (ENG-CSQ-02 ทำ) · ไม่ทำ DOA/NTF (คนละ skill)

---

## 🚦 Trigger Rule (เมื่อไหร่ต้องรัน)

รันเมื่อ feature **มีอย่างน้อย 1 ข้อ**:

| สัญญาณ | ท่อที่มักเกี่ยว | ตัวอย่าง |
|---|---|---|
| มีมูลค่า/ต้นทุน/เวลาที่ตีเป็นเงินได้ · หรือมีการ "ประหยัดที่เกิดจากการหยุด" | **EC** | Work Order · Training · ยกเลิก QT |
| แก้ข้อมูลอ่อนไหว / เปิดดูข้อมูลที่ปกปิด / เปลี่ยนสิทธิ์-นโยบาย | **SecC** | Credit Limit · Vendor Master · Roles · Data Masking |
| ทำให้เกิดรายการทางบัญชี (ตั้งหนี้ ตัดหนี้ ลงบัญชี ค่าเสื่อม) | **AC** | AR/AP Invoice · JE · Fixed Asset |
| ทำให้เงินสดหรืองบเปลี่ยน (commit / ใช้จริง / คืน) | **FC** | PO · Payment Voucher · Budget Control |
| มีการตัดสินใจปลายทาง (Continue/Adjust/Hold/Stop/Complete) นอกเหนือจากการอนุมัติเอกสาร | **DC** | Prospect convert/lost · Readiness go-no-go |
| ติด chip ◆ csq-declaration ใน WAVE_PLAN | — | บังคับ |
| อยู่ในตาราง `CSQ_BACKFILL_REGISTER.md` (feature ที่พัฒนาไปแล้ว) | ตามที่ระบุ | batch mode |

**ไม่ต้องรันเมื่อ:** feature เป็น read model / dashboard / master ที่ไม่อ่อนไหว / view ของ OP
→ ดูรายการ "ไม่ต้องประกาศ" ใน `references/csq-contract.md` ก่อนเสมอ ห้ามยัดใบประกาศเปล่า

---

## ⚙️ Lane Mode (no-ask — เมื่อเรียกจาก feature-lane-runner v2 · S1.8)

- Input = `01_PREBRIEF.md` (§12 สัญญาณประกาศ) + `00_LANE_BRIEF.md` (chip + scope note) — **ห้ามถาม** ทุกคำถาม interview ตอบเองจาก PREBRIEF/scope note/มติ current-state · ตอบไม่ได้ → default ตามตาราง default ของ skill + tag `[ASSUMED]` ใน brief
- ถ้า PREBRIEF §12 ระบุ `need = no` และ chip = — → เขียน `03_<ท่อ>_BRIEF.md` 3 บรรทัด `NOT-NEEDED: reason` (ไม่ข้ามเงียบ)
- chip ≠ detect → รันตาม detect + ใส่บรรทัด `DIVERGENCE:` หัวไฟล์ (runner รวมเข้า DIVERGENCE.md ให้ Strike)
- ออกก่อน HTML: html-generator-v9 Sync Read ไฟล์นี้ (slot picker / bell hook / doc number / PDF template) · frd-generator-v6 Sync Read ซ้ำ — event ที่เพิ่มจาก HTML ให้ **append ในไฟล์เดิม** ไม่สร้างใบใหม่
- Quality Gate ของ skill ยังบังคับ · ตกแล้ววนแก้เองได้ 2 รอบ

## 📥 Input

| # | Input | จำเป็น | ใช้ทำอะไร |
|---|---|---|---|
| 1 | Feature identity (code / ชื่อ / module) | **required** | key ของ profile (`CSQ-XX`) |
| 2 | FRD Pack (เน้น `03_LOGIC` state machine + `05_RULES` + `04_DB`) หรือ PREBRIEF | **required** | หา event candidate + payload field ที่มีจริง |
| 3 | `references/csq-contract.md` | **required** | master ที่ห้ามแต่งเอง (ท่อ 7 · trigger_status 4 · kind ของมูลค่า 3 · naming) |
| 4 | `CSQ_BACKFILL_REGISTER.md` | ถ้ามี | batch mode — รู้ว่า feature อยู่กลุ่ม A/B/C แบบไหน |

**Pre-check:** หา event candidate ไม่เจอเลย → **ห้ามเดา** ให้ตอบว่า feature นี้ไม่ต้องประกาศ พร้อมเหตุผล

---

## 🎤 Interview — 3 คำถาม (ถามครั้งเดียวจบ · เสนอ default เสมอ)

ถ้าผู้ prompt ตอบไว้แล้วในบรีฟ/แชท → **ข้ามคำถามนั้น**

### Q1 — event อะไรบ้างที่ "จบแล้วมีผล"?
เสนอจาก state machine: transition ที่เป็นปลายทาง (posted / approved / closed / cancelled / reversed / changed)
> ⚠️ ไม่ใช่ทุก transition = event — `draft → pending` ไม่มีผลทางธุรกิจ อย่าประกาศ

infer: ดู `03_LOGIC` §state + `05_RULES` ข้อที่มีผลข้างเคียง

### Q2 — ★ แต่ละ event กระทบท่อไหน? (คำถามหลักของ skill นี้)
เสนอ mapping แล้วให้ยืนยัน โดยยึด §Trigger Rule ด้านบน
> ⚠️ ตรวจ 3 ข้อนี้ทุกครั้งก่อนตอบ:
> 1. อยากใส่ **OC** ไหม → **ห้าม** ถ้า event นี้ไม่ได้มาจาก Operation Process (OP เป็นเจ้าของท่อ OC เจ้าเดียว)
> 2. อยากใส่ **DC** เพราะมีการอนุมัติไหม → **ห้าม** DOA engine ยิงให้แล้ว · ใส่ DC ได้เฉพาะ **terminal decision** ที่ไม่ใช่การเซ็นอนุมัติ
> 3. **SC** → ห้ามใส่ทุกกรณี (สงวนไว้ · OQ-C3 ยังไม่เคาะ)

### Q3 — มูลค่าเป็นชนิดไหน (เฉพาะ event ที่ยิง EC)?
| kind | ความหมาย | ตัวอย่าง |
|---|---|---|
| `actual` | เกิดจริงแล้ว มีเอกสารรองรับ | AP Invoice · Payment |
| `estimated` | ผูกพันแล้วแต่ยังไม่จ่ายจริง | PO commitment · งบโปรโมชัน |
| `avoided` | ประหยัดได้เพราะหยุด/ยกเลิก | ยกเลิก QT · Prospect lost |

infer: มีเอกสารการเงินรองรับ = `actual` · commit แล้วรอจ่าย = `estimated` · เป็นการหยุด = `avoided`
> ถ้า EC มาจากเวลา/แรงงาน แต่ยังไม่มี Rate Card → ระบุ `basis: declared` (qty-only) **ห้ามใส่ตัวเลขเงิน**

---

## 📤 Output — `CSQ_BRIEF_[F-xxx].md`

ไฟล์เดียวต่อ feature · วางในโฟลเดอร์ FRD Pack · ใช้ template ที่ `references/brief-template.md`
ต้องมีครบ 6 ส่วน:

| § | ส่วน | เนื้อหา |
|---|---|---|
| 1 | Identity | profile_id (`CSQ-XX`), feature_code, module, กลุ่ม A/B/C, version |
| 2 | **Declared Events** | ตาราง: event_id · trigger point (อ้าง FRD §) · ท่อที่ยิง · เงื่อนไข · payload fields |
| 3 | **ท่อที่ไม่ประกาศ (และเหตุผล)** | ต้องระบุชัดว่า OC/DC-เอกสาร มาอัตโนมัติ · ท่ออื่นที่ไม่เกี่ยว = no-effect |
| 4 | Payload Contract | field ที่ต้องส่งเข้ามาใน envelope + ชนิด + มาจาก entity ไหน + Restricted ต้อง mask ตัวไหน |
| 5 | Register Checklist | สิ่งที่ต้องผ่านก่อน deploy จะ register สำเร็จ |
| 6 | Open Questions | ที่ยังไม่เคาะ + ใครต้องตอบ |

**กฎการเขียน**
- `event_id` = `{feature_prefix}.{verb ที่จบแล้ว}` เช่น `doc.approved`, `sow.closed`, `master.changed`, `log.downtime` — ยึดคำใน contract ห้ามคิดคำใหม่ถ้ามีของเดิม
- ทุก event ต้องมี **trigger point ที่อ้าง FRD ได้จริง** (`03_LOGIC §x.x` / `05_RULES BR-xx`) — เขียนลอย ๆ = FAIL
- ทุก payload field ต้อง **มีอยู่จริงใน 04_DB** ของ feature — แต่งฟิลด์ใหม่ = FAIL
- ค่าที่ skill เสนอเอง (ยังไม่ยืนยัน) → ติด `[DEFAULT — รอยืนยัน]`

---

## 📦 Batch Mode (backfill feature ที่พัฒนาไปแล้ว)

ใช้เมื่อ user สั่ง "รัน backfill" / ชี้ไฟล์ `CSQ_BACKFILL_REGISTER.md`

1. อ่านตารางกลุ่ม A / B / C ในไฟล์ backfill
2. **กลุ่ม B (SecC on sensitive change)** — pattern เดียวกันทั้งกลุ่ม → gen ต่อเนื่องได้เร็ว
   แต่ยังต้องเปิด FRD/HTML ของ feature นั้นเพื่อยืนยันชื่อ field จริง (ห้าม gen จากชื่อ feature อย่างเดียว)
3. **กลุ่ม A / C** — เจาะรายตัว มี event หลายแบบ ต้องอ่าน state machine
4. ออกไฟล์ทีละใบ `CSQ_BRIEF_[code].md` + สรุปท้ายงานเป็นตาราง: `feature · events · ท่อ · สถานะ (พร้อม register / ติด OQ)`
5. **ห้าม truncate** — ถ้าเกิน ~10 ใบต่อรอบ ให้ทำเป็นชุด ๆ แล้วบอกว่าทำถึงไหน

> feature ที่ยังไม่มี FRD (เอกสารไม่ครบ) → ออกใบไม่ได้ ให้ลงตาราง "ติดเอกสาร" แทน ห้ามเดา payload

---

## 🔌 FRD Injection (Sync Read โดย frd-generator-v6)

**1. §05_RULES ต้องมีหัวข้อ "ผลกระทบ 7C (CSQ)"** ชี้ไป `CSQ_BRIEF_[F-xxx].md` + business rule:

| BR | เนื้อหา |
|---|---|
| BR-CSQ-01 | ทุก event ที่ประกาศไว้ ต้องยิงเข้า Engine ผ่าน `POST /csq/events` ตาม Event Envelope — ห้ามเขียนผลรายท่อลง table ของ feature เอง |
| BR-CSQ-02 | envelope ต้องมี `idempotency_key` ที่ unique ต่อ (feature, ref, action) — กันยิงซ้ำตอน retry |
| BR-CSQ-03 | payload ห้ามพก field ชั้น Restricted ดิบ — mask ที่ producer ก่อนส่ง |
| BR-CSQ-04 | การกลับรายการของ feature ต้องส่ง event ที่มี `reversal_of` ชี้ event เดิม — ห้ามลบ/แก้ผลเดิม |
| BR-CSQ-05 | feature ไม่ประกาศ/ไม่คำนวณ ท่อ OC และ DC ระดับเอกสาร (มาจาก OP และ DOA engine) |

**2. ข้อห้ามเด็ดขาด (Iron Rule)**
- ❌ ห้ามคำนวณมูลค่า EC/AC/FC ใน feature (เช่น `cost = minutes * 5`) — **ENG-CSQ-02 เป็นเจ้าของการตีมูลค่า**
- ❌ ห้ามสร้าง column เก็บผลรายท่อใน table ของ feature (`is_ec_triggered` ฯลฯ) — ผลอยู่ที่ `T_csq_stamp`
- ❌ ห้ามเขียน rule แบบ "ถ้าเกิน X บาทให้ถือว่ากระทบงบ" ลง feature — นั่นคือเงื่อนไขใน profile
- ✅ เขียนแทนว่า: *"เมื่อ [transition] สำเร็จ ระบบส่ง event `[id]` เข้า Consequence Engine พร้อม payload ตาม CSQ_BRIEF — การประเมินผลรายท่อเป็นหน้าที่ของ Engine"*
- ✅ จุดที่ยังต่อ engine ไม่ได้ → `// TODO: ENG-CSQ emit`

**3. 02_API ต้องมี** — section Cross-Module ระบุ event ที่ feature นี้ปล่อยออก (producer contract) ตาม Envelope ของ F-CSQ-01 §2.3

---

## 🎨 HTML Injection (Sync Read โดย html-generator-v9)

**1. ต้องมีบนหน้าจอ (เท่านี้พอ — ไม่ต้องมากกว่านี้)**
| ส่วน | รายละเอียด |
|---|---|
| ไม่มี UI ประเมินผล | prototype **ห้าม**วาดการ์ดผล 7 ท่อในหน้า feature — นั่นเป็นหน้าที่ของ 7C Engine / หน้า Consequence |
| ลิงก์ดูผล (optional) | ถ้าจำเป็น ใส่ลิงก์ "ดูผลกระทบ" ชี้ไปหน้า Consequence ของท่อนั้น พร้อม `// TODO: ENG-CSQ` |
| mock emit | คอมเมนต์จุดที่ต้อง emit ตอน action สำเร็จ |

**2. mock pattern ที่อนุญาต**
```js
// TODO: ENG-CSQ emit — ดู CSQ_BRIEF_[F-xxx].md
function emitConsequence(eventId, ref, payload){
  // ส่งเข้า POST /csq/events (Envelope) — prototype ไม่ประเมินผลเอง
}
```
- ❌ ห้าม `const PIPES_HIT = ['ec','ac']` ในไฟล์ feature — การตัดสินว่าท่อไหนโดน เป็นของ Engine

---

## ✅ Quality Gate (ก่อนส่ง CSQ_BRIEF)

| # | เช็ค | FAIL ถ้า |
|---|---|---|
| G1 | ไม่มี event ไหนประกาศท่อ `oc` | เจอ `oc` (OP เป็นเจ้าของ — register จะ reject 422) |
| G2 | ไม่มี event ไหนประกาศ `dc` เพราะการอนุมัติ | DC ที่มาจาก approve/sign (DOA เจ้าของ) |
| G3 | ไม่มี event ไหนประกาศ `sc` | เจอ `sc` (สงวนไว้) |
| G4 | ทุก event มี trigger point อ้าง FRD § ได้ | trigger เขียนลอย ๆ |
| G5 | ทุก payload field มีจริงใน 04_DB | แต่งฟิลด์ใหม่ |
| G6 | event ที่ยิง EC ระบุ `kind` (actual/estimated/avoided) ครบ | ขาด kind |
| G7 | EC จากเวลา/แรงงานที่ยังไม่มี Rate Card ระบุ `basis: declared` | ใส่จำนวนเงินที่คำนวณเอง |
| G8 | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` ครบ | เนียนใส่เป็นค่าจริง |
| G9 | `event_id` ไม่ชนกับ catalog เดิมโดยความหมายซ้อน | ตั้งชื่อใหม่ทั้งที่มีของเดิม |

**FAIL ข้อไหนก็ตาม → แก้ก่อน ห้ามส่ง** (G1-G3 คือกฎที่ระบบ enforce จริงตอน register — ปล่อยผ่าน = deploy พัง)

---

## 📚 References

| ไฟล์ | เนื้อหา |
|---|---|
| `references/csq-contract.md` | Master ที่ห้ามแต่งเอง — 7 ท่อ + นิยาม, trigger_status 4 ค่า, kind 3 ค่า, event vocabulary, Envelope schema, รายการ feature ที่ไม่ต้องประกาศ |
| `references/brief-template.md` | Template ของ CSQ_BRIEF 6 ส่วน + ตัวอย่างกรอกจริง 2 เคส (กลุ่ม A และ B) |

**อ่าน reference ก่อนเขียนเสมอ** — ห้ามตอบจากความจำเรื่องชื่อท่อ / ค่า enum / คำ event

---

## 🚫 ห้ามทำ

1. ห้าม register จริงแทน deploy pipeline — skill นี้ออก**ใบประกาศ**เท่านั้น
2. ห้ามแก้ไฟล์ `F-CSQ-01_Consequence_Engine.html` หรือ FRD Pack ของ Engine
3. ห้ามยัดใบประกาศเข้า feature ที่ไม่มีผลกระทบเฉพาะทาง (read model / dashboard / master ธรรมดา)
4. ห้ามคำนวณมูลค่าเงินเองในใบประกาศ — ประกาศแค่ว่า "ตีมูลค่าจากอะไร" (`basis`)
5. ห้ามประกาศ OC / DC-เอกสาร / SC ซ้ำ (ข้อนี้ระบบ reject จริง ไม่ใช่แค่กฎบนกระดาษ)

---

## 📌 หลังส่ง CSQ_BRIEF — งานที่คนต้องทำต่อ

- [ ] วางไฟล์ใน FRD Pack ของ feature (ไปกับ dev package ก้อนเดียว)
- [ ] dev wire `emit` ที่ transition จริง + ใส่ `idempotency_key`
- [ ] deploy → ตรวจว่าแถวใน **Profile Registry** ของ 7C Engine เปลี่ยนเป็น **เชื่อมแล้ว**
- [ ] ตรวจ Event Log ว่า event แรกเข้ามาแล้วประทับผลถูกท่อ (ไม่ค้าง "ยังไม่ประเมิน")
- [ ] อัพเดต `FEATURE_REGISTRY.md` + แจ้งพี่เบิร์ดอัพ Google Sheet
