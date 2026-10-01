# 00_OVERVIEW — F-WH-PUTAWAY · จัดเก็บเข้าที่ (Putaway)

## §0.1 Document Control

| ช่อง | ค่า |
|---|---|
| Feature | `F-WH-PUTAWAY` · Putaway — จัดเก็บเข้าที่ (fid **F081**) |
| Module | Warehouse (คลังสินค้า) |
| Wave / Lane | **W3Q** ลำดับ 1 · pack `CUBE-LANE-W3-LITE` |
| Registry (F081) | `arch = master` · `dec = csq` · `wave = W3Q` · **`auto = lite`** → Mode B |
| Architecture | **master/console — ไม่ใช่เอกสารธุรกรรม · ห้าม Pattern Q** |
| FRD Variant | **FULL** (00…07 + INDEX) — เหตุผล §0.1.1 |
| Input | `02_BRD/BRD_F-WH-PUTAWAY.md` (**APPROVED** C01–C23 23/23) · `02_BRD/PREBRIEF_F-WH-PUTAWAY.md` · `02_BRD/FUNCTION_CHECKLIST_F-WH-PUTAWAY.md` (44 FN) · `01_HTML/F-WH-PUTAWAY.html` (**ผ่าน 7R re-gate**) · `03_FRD/CSQ_BRIEF_F-WH-PUTAWAY-001.md` · `HANDOFF.md` §3/§5 |
| Mode | **HTML-first · Phase 1.5 = Recognize & Validate** (สกัด pattern จากจอจริง ไม่ตัดสิน layout ใหม่) |
| Lane Mode | **no-ask** — ข้อที่ skill ตัดสินเองติด `[AI-DEFAULT]` (รายการเต็ม §0.13) |
| วันที่ | **2026-09-14** (**ปี ค.ศ. ล้วนทั้งแพ็ก**) |

### Sync Read (v6.1 — ห้าม hardcode)

| อ่านจาก | ใช้ทำอะไร |
|---|---|
| `.agents/skills/html-generator-v9/` (`SKILL.md` · `knowledge/iron-rules.md`) | CI tokens · iron rules · microcopy กลาง · contract ของ BASE-KIT — **ห้ามคัดตัวเลข/สีมาแปะใน FRD** |
| `01_HTML/F-WH-PUTAWAY.html` | route · anatomy · microcopy verbatim · ชื่อฟังก์ชันจริง |
| `01_HTML/_UX_CHECK_REPORT.md` · `_COVERAGE_REPORT.md` | ผล re-gate ที่ FRD ต้องสอดคล้อง |

### §0.1.1 ทำไมเป็น FULL

1. **Permission matrix จริง** — 6 role × 11 action (BRD §4.2) มีแถวที่ต่างกันจริงหลายจุด (กลับรายการ · ปลดล็อกงาน · ล็อกช่อง · แก้ผัง)
2. **Rule engine จริง** — เกณฑ์แนะนำช่องเก็บ = hard filter 5 เงื่อนไข + จัดอันดับ 4 ชั้น + tie-break 3 ชั้น (PREBRIEF §3.5) และ **ลำดับ/น้ำหนักเป็น config** (R07 CONFIGURABLE)
3. **สัญญาข้ามฟีเจอร์** — `Zone`/`Bin`/`location_type`/`Inv_Movement` เป็นของกลางที่ **F-WH-STKADJ และ F-WH-STKTRF ถูกบังคับให้ใช้** (LOCK-08) → ชั้น DB ต้องเขียนละเอียดพอให้สองฟีเจอร์นั้นหยิบไปใช้ได้โดยไม่ต้องเดา

---

## §0.2 Scope

### In Scope (BRD §3.1 · IS-01…IS-13)

| # | ขอบเขต | ลงที่ |
|---|---|---|
| IS-01 | คิวงานค้างจัดเก็บ สร้างอัตโนมัติจากใบรับของที่บันทึกแล้ว เฉพาะบรรทัดที่ผ่าน QC | `03_LOGIC` FN-01 · `02_API` API-01 |
| IS-02 | **สัญญากลางของ location** — คลัง › โซน › ช่องเก็บ + ประเภท 5 ชนิด | `04_DB` §4.2 · §4.7 |
| IS-03 | เกณฑ์แนะนำช่องเก็บ (กรอง 5 + จัดอันดับ 4 + tie-break) พร้อมเหตุผล | `03_LOGIC` §3.2 `ENG-PUT-SUGGEST` |
| IS-04 | เลือกช่องเก็บเอง (override) ทุกเมื่อ · ฝืนเกณฑ์ต้องระบุเหตุผล | `03_LOGIC` FN-12/FN-13 · `05_RULES` R10/R11 |
| IS-05 | ยืนยันจัดเก็บ → รายการเคลื่อนไหวต่อท้ายอย่างเดียว → เด้งงานถัดไป | `03_LOGIC` FN-15/FN-16 · `02_API` API-08 |
| IS-06 | เก็บบางส่วน + แบ่งเก็บหลายช่องในครั้งเดียว | `05_RULES` R12/R14 |
| IS-07 | ความจุช่องเก็บ = เกณฑ์แนะนำ (เกินได้ เตือน + เหตุผล) | `05_RULES` R15 |
| IS-08 | ของกักกันแยกคิว · เก็บได้เฉพาะช่องกักกัน | `05_RULES` R04 |
| IS-09 | การถือครองงาน (รับ/คืน/ปลดล็อก) | `03_LOGIC` FN-05..FN-08 |
| IS-10 | มุมมองผังช่องเก็บ + ล็อก/ปลดล็อกช่อง | `01_UI` §1.5 · `02_API` API-10..12 |
| IS-11 | มุมมองประวัติ + กลับรายการจัดเก็บ | `01_UI` §1.6 · `03_LOGIC` FN-18 |
| IS-12 | ผู้จัดเก็บเป็นคนจริง | `05_RULES` R24 |
| IS-13 | ประกาศผลกระทบ 7C 2 เหตุการณ์ | `05_RULES` §5.5 · `CSQ_BRIEF` |

### Out of Scope (ตัดสินแล้ว — ห้ามทำ · BRD §3.2)

| # | ไม่ทำ | เจ้าของจริง |
|---|---|---|
| OS-01 | เอกสาร / เลขรัน / ไฟล์พิมพ์ / ลายเซ็น | — (ไม่ใช่เอกสาร · LOCK-01/02) |
| OS-02 | สายอนุมัติ (DOA) | — (ไม่มีโดยเจตนา) |
| OS-03 | แจ้งเตือนอัตโนมัติ | ENG-NOTIFY (chip ไม่มี `ntf`) |
| OS-04 | ปรับยอดคงเหลือด้วยมือ | **F-WH-STKADJ** |
| OS-05 | ย้ายของหลังเก็บแล้ว / ข้ามคลัง | **F-WH-STKTRF** |
| OS-06 | คืนของผู้ขาย | **F-PUR-RTV** (ปิดแล้ว) |
| OS-07 | ล็อต/ซีเรียล · พาเลท · cross-dock · slotting · เส้นทางเดิน | backlog W4+ |
| OS-08 | ยิงบาร์โค้ด / RF จริง | W4 (`OQ-PUT-09`) |
| OS-09 | Putaway จากแหล่งที่ไม่ใช่ใบรับของ | F-WH-STKADJ |
| OS-10 | ลงบัญชีจริง | GL/JE · W5 (`TODO: JE posting`) |

---

## §0.3 Roles

| Role | ทำอะไรได้ (สรุป) | อ้าง |
|---|---|---|
| **เจ้าหน้าที่คลัง** (`WH_OPERATOR`) | ดูคิวคลังตัวเอง · รับ/คืนงาน · เลือก/override ช่อง · ยืนยันจัดเก็บ | BRD §4.2 |
| **หัวหน้าคลัง** (`WH_SUPERVISOR`) | ทุกอย่างของเจ้าหน้าที่ (ทุกคลัง) + **ปลดล็อกงานคนอื่น** + **กลับรายการจัดเก็บ** + ล็อก/ปลดล็อกช่อง | BRD §4.2 |
| **ผู้ดูแลผังคลัง** (`WH_LAYOUT_ADMIN`) | แก้ผัง location · ความจุ · หมวดที่โซนรับ · ล็อก/ปลดล็อกช่อง — **ทำที่ F008 ไม่ใช่ที่นี่** | BRD §4.2 |
| **ผู้ตรวจคุณภาพ** (`QC_INSPECTOR`) | อ่านคิวกักกันอย่างเดียว | BRD §4.2 |
| **จัดซื้อ / บัญชี** (`PROC_VIEWER` · `FIN_VIEWER`) | ดูยอดคงเหลือราย bin + ประวัติ (อ่านอย่างเดียว) | BRD §4.2 |
| **ผู้ดูแลระบบ** (`SYS_ADMIN`) | ดูทุกอย่าง · **ลบไม่ได้เหมือนกัน** | BRD §4.2 |

> **ไม่มี role "ผู้อนุมัติ Putaway" โดยเจตนา** (LOCK-02) · **ไม่มีใครมีสิทธิ์ลบ** (BRD §4.2 แถวสุดท้าย)
> matrix เต็มระดับ API อยู่ที่ `02_API` §2.8 · เคสทดสอบสิทธิ์อยู่ที่ `06_TESTS` §6.2

---

## §0.4 Dependencies

| ทิศ | คู่ | สัญญา | สถานะ |
|---|---|---|---|
| **เข้า** | **F-WH-GRN (F079)** | คิวเกิดจากบรรทัดที่ `posted` + ผ่าน QC · ส่ง GRN no. + line no. + item + qty + source location | ✅ ปิดแล้ว (soft-ref) |
| เข้า | **ทะเบียนคลัง/โซน/ช่องเก็บ (F008)** | อ่านผัง + ประเภท + ความจุ + หมวดที่โซนรับ + allow mixed + สถานะล็อก | ⚠️ **ต้องขยาย schema** — ดู `04_DB` §4.7 |
| เข้า | ทะเบียนสินค้า (F010) · หน่วยนับ · ทะเบียนพนักงาน | อ้างอิงแบบหลวม nullable | ✅ |
| เข้า | **NC rules** (config กลาง) | `aging_warn_hours` · `soft_lock_minutes` · `reversal_window_days` | ⚠️ ค่ายังรอเคาะ (CF-05/06/07) |
| **ออก** | **`Inv_Movement` (ของกลางโมดูลคลัง)** | append-only + คู่ reversal | 🆕 **feature นี้เป็นคนตั้ง** |
| **ออก** | **`Bin_Stock` (projection)** | ยอดราย (bin, item) คำนวณจาก movement | 🆕 **feature นี้เป็นคนตั้ง** |
| **ออก** | **F-WH-STKADJ (F082)** | ใช้สัญญา location + ยอดราย bin · เป็นเจ้าของประเภท `damage` | ⏳ ยังไม่ทำ · **LOCK-08** |
| **ออก** | **F-WH-STKTRF (F083)** | ใช้สัญญาเดียวกัน · เป็นเจ้าของประเภท `in-transit` ที่ feature นี้จองไว้ | ⏳ ยังไม่ทำ · **LOCK-08** |
| ออก | F-PUR-RTV (F080) | ของกักกันออกทางเดียวคือคืนผู้ขาย | ✅ ปิดแล้ว · mock ในรอบนี้ |
| ออก | **ENG-CSQ (F-CSQ-01)** | 2 event (`putaway_forced_override` · `putaway_reversed`) | ✅ ผ่านใบประกาศ |
| ออก | GL / JE (W5) | **ไม่กระทบมูลค่ารวม** — mock `TODO: JE posting` | ⏳ W5 |
| **ไม่มีเส้น** | DOA (F-DLG-001) · ENG-NOTIFY · F-DOCCFG · thai-doc-pdf-generator | **โดยเจตนา** (LOCK-02) | ❌ |

---

## §0.7.1 Data Classification — ระดับสูงสุดที่ feature แตะ

| ระดับ | มีในฟีเจอร์นี้ไหม | ตัวอย่าง field |
|---|---|---|
| **D0 Public** | ✅ | รหัสโซน · รหัสช่องเก็บ · ชื่อโซน |
| **D1 Internal** | ✅ **(ระดับสูงสุดของ feature)** | จำนวนคงเหลือราย bin · เลขใบรับของ · หมวดสินค้า · เหตุผล override · ประวัติการเคลื่อนไหว |
| **D2 Confidential** | ⬜ **ไม่มี** | — ไม่มีราคา ไม่มีมูลค่า ไม่มีเงื่อนไขการค้า |
| **D3 Restricted / PII** | ⬜ **ไม่มี** | ชื่อ+ตำแหน่ง+แผนกของพนักงานเป็นข้อมูลองค์กร ไม่ใช่ PII (ไม่มีเบอร์/อีเมล/เลขบัตร) |

**ระดับสูงสุด = D1** → บังคับใช้ตาม `04_DB` §4.6 · Security Preset **P1 (ยกระดับบางส่วน)** ตาม BRD §16.1
ที่ยกระดับ: **ห้ามลบ/ห้ามแก้ย้อนหลัง** และ **ระบุตัวตนผู้ทำรายการ** ให้เท่าเอกสารธุรกรรม เพราะแตะยอดสินทรัพย์จริง

---

## §0.10 ใบประกาศตามชิป — ออก 1 ใบ ตาม `dec = csq`

| ชิป | ใบ | สถานะ | เหตุผล |
|---|---|---|---|
| ◆ `csq` | `CSQ_BRIEF_F-WH-PUTAWAY-001.md` | ✅ **ออก** (รับจาก `5_DECLARATIONS/` ของต้นน้ำ) | มี 2 event ที่ไม่มีใครในระบบนับอยู่ |
| ⚖ `doa` | — | ❌ **ไม่ออก โดยเจตนา** | Putaway ไม่มีสายอนุมัติเลย — เป็นงาน execution · registry ไม่ติดชิป · **LD-01** |
| 🔔 `ntf` | — | ❌ **ไม่ออก โดยเจตนา** | registry ไม่ติดชิป `ntf` รอบนี้ · ถ้าอนาคตต้องเตือน "งานค้างเกินเกณฑ์" ให้ประกาศที่ ENG-NOTIFY ห้าม hardcode · **LD-01** |
| `doccfg` | — | ❌ **ไม่ออก โดยเจตนา** | **ไม่ใช่เอกสาร ไม่มีเลขรัน** — `PT-<seq>` เป็นรหัสภายในเพื่อ trace เท่านั้น · **LD-02** |
| 📄 `pdfdoc` | — | ❌ **ไม่ออก โดยเจตนา** | ไม่มีใบพิมพ์ · `static_scan.a4 = false` · **LD-01** |

> **เขียนไว้ให้ชัดว่าไม่ใช่การตกหล่น** — 4 ใบที่ไม่ออกมีเหตุผลรายใบและถูกตราไว้ที่ `07_LOCKED_DECISIONS` LD-01/LD-02
> `_COVERAGE_REPORT.md` §5 ยืนยันเชิงกล: detect = chip → **ไม่มี DIVERGENCE**

### §0.10.1 หมายเหตุสำคัญเรื่อง `csq` — สิ่งที่ **ไม่** ประกาศก็สำคัญเท่ากัน

`CSQ_BRIEF §3` ประกาศชัดว่า **ไม่** ยิงท่อ OC · DC · SC · SecC · AC · FC และ **ไม่ยิง EC ของการจัดเก็บปกติ**
เหตุผลหลัก: **มูลค่าของก้อนสินค้าถูก `grn_posted` ประกาศ EC ไปแล้ว** — putaway แค่เปลี่ยน location → ยิงอีก = **นับซ้ำทั้งก้อน**
→ ขัดกับ `PREBRIEF §2 S-01`/`§6.2` ที่เขียนว่ามี `csq putaway.confirmed` → **ตัดสินที่ `07_LOCKED` LD-04** (ยึด CSQ_BRIEF) + เปิด OQ ให้ BA แก้ถ้อยคำ

---

## §0.11 Scope Lock (นำเข้าจาก BRD §3.4 + HANDOFF §3 — immutable · R11)

ยกครบทุกข้อไปที่ **`07_LOCKED_DECISIONS.md` §7.0 (LOCK-01..08) และ §7.1 (L1..L10)** — ที่นี่สรุปเฉพาะข้อที่กระทบการเขียนโค้ดโดยตรง:

| Lock | ผลผูกพันกับ dev |
|---|---|
| **LOCK-01 / L1** | ห้าม Pattern Q — ไม่มี wizard · ไม่มี view-drawer แท็บเอกสาร · ไม่มี PDF/ลายเซ็น/เลขที่เอกสาร/สายอนุมัติ |
| **LOCK-02 / L2** | Declarations = `csq` เท่านั้น |
| **L3** | `PT-<seq>` **ห้ามทำเป็นเลขที่ใบ ห้ามผูก doccfg** |
| **LOCK-03 / L4** | รายการเคลื่อนไหวต่อท้ายอย่างเดียว — **ไม่มี endpoint update/delete** (DR-05) |
| **L5** | **§3.0 LOCATION MODEL** ห้ามนิยามใหม่ — F-WH-STKADJ / F-WH-STKTRF ต้องใช้ชุดนี้ |
| **LOCK-07 / L6** | `in-transit` และ `damage` — Putaway **ห้ามเขียนทั้งขาเข้าและขาออก** |
| **LOCK-06 / L7** | ของกักกันออกได้ทางเดียวคือใบคืนผู้ขาย |
| **LOCK-04** | Master ทุกตัว = soft-ref ไม่ผูก FK · nullable |
| **LOCK-05 / L8** | ปี **ค.ศ. ล้วน** ทุกจุด + CI CUBE Warm Light + sidebar ตาม module map |
| **L9** | BASE-KIT ใน HTML verbatim (Rule #69) |
| **L10** | ผู้ทำรายการเป็นคนจริง ห้าม role ID |

---

## §0.12 Coverage Manifest (R13) — ทุก requirement มีที่ลง

### §0.12.1 User Stories (BRD §7 · S-01…S-20)

| Story | ลงที่ | AT |
|---|---|---|
| S-01 เปิดแล้วเห็นคิวทันที | `01_UI` §1.3 · `03_LOGIC` FN-01 | AT-01 |
| S-02 รู้ว่างานมาจากใบรับของไหน | `01_UI` §1.4 หัวงาน · `02_API` API-02 | AT-02 |
| S-03 ได้ข้อเสนอช่องเก็บทันที | `03_LOGIC` §3.2 `ENG-PUT-SUGGEST` | AT-03 |
| S-04 เลือกช่องอื่นได้เสมอ | `03_LOGIC` FN-12 · `05_RULES` R10 | AT-06 |
| S-05 รู้ว่าครั้งไหนฝืนเกณฑ์ | `03_LOGIC` FN-13 · `01_UI` §1.6 filter | AT-07, AT-18 |
| S-06 เก็บบางส่วนได้ | `03_LOGIC` FN-15 · `05_RULES` R14 | AT-09 |
| S-07 แบ่งเก็บหลายช่อง | `03_LOGIC` FN-15/FN-16 | AT-10 |
| S-08 กันเก็บเกินยอด | `03_LOGIC` FN-14 · `05_RULES` R12/R13 | AT-11, AT-12 |
| S-09 ของกักกันไม่หลุด | `03_LOGIC` FN-10 (F-1) · `05_RULES` R04 | AT-13 |
| S-10 ล็อกช่องที่ใช้ไม่ได้ | `03_LOGIC` FN-19/FN-20 | AT-19, AT-20 |
| S-11 จองงานกันทำซ้ำ | `03_LOGIC` FN-05 · `05_RULES` R18 | AT-14 |
| S-12 ปลดงานในมือคนอื่น | `03_LOGIC` FN-07 | AT-16 |
| S-13 กลับรายการที่เก็บผิดช่อง | `03_LOGIC` FN-18 · `05_RULES` R17 | AT-21, AT-22 |
| S-14 ไม่มีใครลบประวัติได้ | `04_DB` §4.2 `t_inv_movement` · `05_RULES` R16 | AT-23 |
| S-15 เห็นยอดคงเหลือแต่ละช่อง | `03_LOGIC` FN-17 · `02_API` API-09 | AT-24 |
| S-16 รู้ทันทีเมื่อไม่มีช่องเหมาะสม | `03_LOGIC` FN-09 ขั้นที่ 4 · `05_RULES` R09 | AT-05 |
| S-17 เห็นงานค้างนานผิดปกติ | `03_LOGIC` FN-04/FN-23 · `05_RULES` R20 | AT-25 |
| S-18 รู้ว่าหมวดไหนยังไม่มีโซน | `03_LOGIC` FN-11 (R4 fallback) | AT-04 |
| S-19 ได้โครง location ใช้ต่อได้ | `04_DB` §4.7 · `01_UI` §1.5 | AT-26 |
| S-20 การจัดเก็บไม่เปลี่ยนมูลค่าคลัง | `05_RULES` §5.5 · `01_UI` §1.4 แถบยืนยัน | AT-27 |

### §0.12.2 Business Rules (BRD §9.1 R01–R25) → `05_RULES` §5.1 — **ครบ 25/25**
### §0.12.3 Validation (BRD §9.2 VR01–VR14) → `05_RULES` §5.2 — **ครบ 14/14**
### §0.12.4 Edge Cases (BRD §10.1 EC-01..15 ยืนยันแล้ว · §10.2 EC-16..21 รอยืนยัน) → `05_RULES` §5.3

### §0.12.5 ★★ ตาราง map รหัสที่ชนกัน — **อ่านก่อนใช้ทุกครั้ง**

รหัส 3 ตระกูลนี้ใช้ตัวอักษรซ้ำกันแต่ **เป็นคนละชุด** — อย่า rename ข้ามไฟล์

| รหัส | ในเอกสารไหน | หมายถึงอะไร | จำนวน |
|---|---|---|---|
| **`S-01`…`S-28`** | **PREBRIEF §2** | **Scenario** (happy / alt / exception / ไม่รองรับ) | 28 |
| **`S-01`…`S-20`** | **BRD §7** | **User Story** | 20 |
| `BR-01`…`BR-25` | PREBRIEF §4 | Business Rule | 25 |
| `R01`…`R25` | BRD §9.1 | Business Rule — **ตรงกับ `BR-xx` 1:1 ทุกข้อ** (BR-01↔R01 … BR-25↔R25) | 25 |
| **`FN-01`…`FN-94`** | **FUNCTION_CHECKLIST** | **ฟังก์ชันเชิงธุรกิจ** (สิ่งที่ผู้ใช้ต้องทำได้) — เลขไม่ต่อเนื่อง | 44 |
| **`F-WH-PUTAWAY-FN-01`…`-25`** | **`03_LOGIC` §3.1** | **ฟังก์ชันชั้นโค้ด** — **คนละชุดกับข้างบน** | 25 |
| `SC-01`…`SC-14` | BRD §14.6 | Screen Inventory | 14 |
| `G-01`…`G-11` | BASELINE §5 | Gap เทียบ ERP มาตรฐาน | 11 |
| `AT-xx` · `PT-xx` · `XT-xx` | `06_TESTS` | Acceptance / Permission / Cross-module test | — |

> ⚠️ **กับดักที่ต้องระวังที่สุด: `S-xx` ชนกัน 2 ความหมาย** (PREBRIEF scenario 28 ตัว vs BRD story 20 ตัว)
> ในแพ็กนี้: **`01_UI` / `05_RULES` / `06_TESTS` §6.10 อ้าง PREBRIEF scenario** · **`00_OVERVIEW` §0.12.1 และ `06_TESTS` §6.1 อ้าง BRD story**
> ทุกครั้งที่อ้าง `S-xx` จะเขียนกำกับว่า `(PREBRIEF)` หรือ `(BRD story)` เสมอ
> **ข้อเสนอให้ BA:** เปลี่ยน prefix ที่ต้นทางเป็น `SC-xx` (scenario) กับ `US-xx` (user story) ในรอบหน้า

### §0.12.6 Scenario coverage — PREBRIEF S-01…S-28 → `06_TESTS` §6.10 (**ครบ 28/28**)
### §0.12.7 FUNCTION_CHECKLIST FN → AT map → `06_TESTS` §6.12 (**ครบ 44/44**)

---

## §0.13 Open Questions

### จาก BRD §15 + PREBRIEF §10 — เจ้าภาพหลัก **Strike**

| # | ประเด็น | สถานะ | เจ้าภาพ | ผลถ้าเปลี่ยน |
|---|---|---|---|---|
| `OQ-GRN-01` | ของ QC ไม่ผ่าน = โซนกักกัน · ออกทางเดียวคือคืนผู้ขาย | **[ASSUMED] ใช้ค่าตั้งต้นแล้ว** | Strike | R04 · FN-10 (F-1) เปลี่ยนทั้งชุด |
| `OQ-TRF-01` | ย้ายข้ามสาขาผ่าน `in-transit` — Putaway จองประเภทไว้ ไม่เขียน | **[ASSUMED]** | Strike + เจ้าของ F-WH-STKTRF | R05 · `04_DB` §4.7 enum |
| `OQ-PUT-01` | override ต้องกรอกเหตุผลทุกกรณีไหม | **[ASSUMED]** เฉพาะเมื่อฝืนเกณฑ์ | Strike | R11 (WARNING) · FN-13 |
| `OQ-PUT-02` | ความจุเป็นกฎหรือเกณฑ์แนะนำ | **[ASSUMED]** เกณฑ์แนะนำ | Strike | R15 (WARNING) · ถ้าเปลี่ยนเป็นกฎ → FN-14 ต้องบล็อก |
| `OQ-PUT-03` | ถือครองงานได้กี่นาทีก่อนคืนคิวอัตโนมัติ | **[ASSUMED]** มีกลไก · ค่าอยู่ NC rules | Strike | R18 · **FN-08 ยังไม่ implement — ดู LD-05** |
| `OQ-PUT-04` | ใครกลับรายการได้ · ย้อนได้กี่วัน · ถ้าของถูกย้าย/เบิกไปแล้ว · กลับครบแล้วใบรับของกลับรายการได้อีกไหม | **รอเคาะ** | Strike (คู่กับ `OQ-GRN-04`) | R17 · FN-18 · FN-22 |
| `OQ-PUT-05` | เจ้าของ config ผังคลัง — กลางหรือรายคลัง | **รอเคาะ** | Strike + เจ้าของ F008 | `04_DB` §4.7 ownership |
| `OQ-PUT-06` | เกณฑ์งานค้างกี่ชั่วโมงถือว่าเสี่ยง | **รอเคาะ** | Strike | CF-05 · FN-04 |
| `OQ-PUT-07` | โซนกักกันเป็นโซนหรือช่องพิเศษ | **ตัดสินชั่วคราว** = โซน | Strike | `04_DB` §4.2 |
| `OQ-PUT-08` | ข้ามเขตตีมูลค่าต้องลงบัญชีไหม | **ตัดสินชั่วคราว** = ไม่กระทบ | Strike + เจ้าของ GL (W5) | §5.5 · `CSQ-Q3` |
| `OQ-PUT-09` | รองรับยิงบาร์โค้ดเมื่อไหร่ | backlog | Strike | OS-08 |
| `CSQ-Q1` | ควรมี event "จัดเก็บสำเร็จ" แบบ value-neutral ไหม | **รอเคาะ** | เจ้าของ F-CSQ-01 | §5.5 · **LD-04** |
| `CSQ-Q2` | Rate Card ของงานย้ายซ้ำ ใครเป็นเจ้าของ | **รอเคาะ** | เจ้าของ ENG-CSQ-02 + Strike | ทั้ง 2 event ยังเป็น `basis: declared` |
| `CSQ-Q3` | putaway ข้าม valuation area ต้องยิง AC ไหม | **รอเคาะ** | เจ้าของ GL (W5) | คู่กับ `OQ-PUT-08` |
| `CSQ-Q4` | aging งานค้างควรเป็น event 7C หรือแค่ KPI | **ตัดสินชั่วคราว** = KPI + NC rules | เจ้าของ F-CSQ-01 + Strike | §5.5 |
| `CSQ-Q5` | กันยิง EC ซ้ำกับ F-WH-STKTRF | **รอเคาะ** | เจ้าของ F-WH-STKTRF + F-CSQ-01 | §5.5 |

### ★ OQ ใหม่ที่เปิดในเลนนี้ (Phase B)

| # | ประเด็น | ที่มา | เจ้าภาพ |
|---|---|---|---|
| **`OQ-PUT-10`** | **PREBRIEF §2/§6.2 เขียนว่ามี event `putaway.confirmed` แต่ `CSQ_BRIEF §2/§3` ห้ามประกาศ** — ต้องแก้ถ้อยคำฝั่ง PREBRIEF ให้ตรง (เลนนี้ยึด CSQ_BRIEF · **LD-04**) | `_COVERAGE_REPORT` §1.2 | Strike + เจ้าของ F-CSQ-01 |
| **`OQ-PUT-11`** | **ชุด mock ให้ `PT-0011` ถือครองโดย `u-anucha` ซึ่งเป็นผู้ใช้ปัจจุบันเอง** → scenario S-15 (PREBRIEF) และ FN-21(a)(b) เดินไม่ถึงในต้นแบบ · ข้อเสนอ: เปลี่ยนผู้ถือเป็น `u-somchai` | `_COVERAGE_REPORT` §1.1 | Strike (BA lane) |
| **`OQ-PUT-12`** | `PREBRIEF §8` `PT-0005` ตั้งใจให้เป็นตัวอย่าง override ข้ามหมวด แต่เกณฑ์ R1 จับได้ก่อน — ต้องแก้ mock spec ให้ตรงพฤติกรรมจริง | `_COVERAGE_R1` §6 (ต้นน้ำแจ้ง) · ยืนยันแล้ว | Strike (BA lane) |

### OQ ของเลนอื่นที่ **ไม่ใช่ของฟีเจอร์นี้** (ระบุไว้กันเข้าใจว่าตกหล่น)

| # | อยู่ที่ไหน | ทำไมไม่ใช่ของเรา |
|---|---|---|
| `OQ-PO-01` | ใบสั่งซื้อ / ใบรับของ | เรื่องเปอร์เซ็นต์รับเกิน — ตัดสินที่ต้นทาง Putaway รับจำนวนที่ผ่าน QC มาใช้ตรง ๆ |
| `OQ-STK-01` | ใบปรับยอดสต๊อก (F082) | เรื่องเหตุผลการปรับยอด + สายอนุมัติตามมูลค่า — **Putaway ไม่ปรับยอดและไม่มีสายอนุมัติ** |

> ระบุไว้ตาม `PREBRIEF §13.4` — **ไม่ได้ตกหล่น แต่ไม่ใช่ขอบเขตของฟีเจอร์นี้**

### Edge Cases ที่ยังไม่ confirm (BRD §10.2 EC-16..EC-21) — **ไม่ได้เขียนเป็น spec**
รายการเต็มอยู่ที่ `05_RULES` §5.3.3 — **dev ห้าม implement จนกว่าจะ confirm**

### `[AI-DEFAULT]` ที่ skill ตัดสินเองในรอบนี้ (Lane Mode — ไม่ถาม)

| # | เรื่อง | ค่าที่ใช้ | เหตุผล |
|---|---|---|---|
| AD-01 | ชื่อ endpoint + รูปแบบ REST | `/warehouse/putaway/*` · `/warehouse/bins/*` · `/inventory/movements/*` | ตามแบบแผนของแพ็กก่อนหน้าในโมดูล |
| AD-02 | รหัส error | `E-PUT-xxx` (feature) · `E-WHBIN-xxx` (ผัง) · `E-INVMV-xxx` (movement) | แยกตามเจ้าของตาราง |
| AD-03 | ชื่อตาราง | `t_wh_zone` · `t_wh_bin` · `t_putaway_task` · `t_inv_movement` · `t_putaway_audit` + view `v_bin_stock` | ตาม convention `t_<module>_<entity>` |
| AD-04 | กลไก concurrency ตอนยืนยัน | optimistic lock ด้วย `task_version` + idempotency key ต่อ (task, bin, action) | DR-09 บังคับให้ key มี bin |
| AD-05 | `Bin_Stock` เป็น materialized view ที่ refresh ในทรานแซกชันเดียวกับ movement | — | DR-06 ห้ามมีตารางยอดที่แก้มือได้ แต่ต้องอ่านเร็ว (SLA ≤1s) |
| AD-06 | soft lock timeout ทำที่ **ฝั่งเซิร์ฟเวอร์** (scheduled sweep + lazy check ตอนอ่านคิว) ไม่ใช่ timer ฝั่งจอ | — | ต้นแบบ in-memory ทำ timer ที่มีความหมายไม่ได้ · **LD-05** |
| AD-07 | ประวัติเก็บถาวร ไม่มี archive/purge | — | LOCK-03 append-only · ยังไม่มีนโยบายเก็บรักษา |

---

## §0.14 หมายเหตุ Mode B — สิ่งที่เลนนี้ทำกับ HTML

| | |
|---|---|
| ขั้น 1–8 | **ทำมาแล้วจากต้นน้ำ** (BA lane · `feature-lane-runner 2.4.1r`) — S3a/S3b/S3c PASS · BRD APPROVED 23/23 |
| เลนนี้เริ่มที่ | **ขั้น 7R re-gate** → Phase B (FRD → UI Brief → TC → TL;DR → Pack) |
| re-gate ใช้ skill อะไร | HANDOFF §6 อ้าง `html-review-fix-order` ซึ่งเป็น skill ของ BA lane **ไม่มีใน repo นี้** → ใช้ `qc-ux-html-checker` + `qc-coverage-checker` ทำหน้าที่แทน (บันทึกไว้ที่ `07_LOCKED` §7.3) |
| **HTML ถูกแก้ไหม** | **ใช่ — 2 บรรทัด** (2561 · 2584) ถอด marker `FWD-WIRE:` ออกจากข้อความที่ผู้ใช้เห็น (Iron Rule #81) · อนุมัติโดยผู้ใช้ 2026-09-14 · **ไม่ byte-identical กับ `input/09142026-putaway/1_HTML/` อีกต่อไป** · **LD-03** |
| gate หลังแก้ | `audit.sh` FAIL=0 · `self_audit` เท่าเดิม (baseline skeleton 4 ตัว) · `node --check` OK · console/pageerror = 0 · jargon sweep 13 สถานะ = 0 hit |
| ภาพหลักฐาน | **20 ใบ ถ่ายใหม่ทั้งหมดหลังแก้** — ชุดก่อนแก้ถูกลบทิ้ง (md5 ซ้ำ = 0) |

**สิ่งที่ยังไม่ได้ทำในเลนนี้:** BA sign-off ของ OQ ที่รอเคาะ · การส่งขึ้น OPS · การอัปเดต `st` ใน registry
