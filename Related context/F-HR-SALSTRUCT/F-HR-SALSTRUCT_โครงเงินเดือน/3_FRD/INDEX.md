# INDEX — FRD F-HR-SALSTRUCT · Salary Structure (โครงเงินเดือน)

> Pack Variant: **FULL** (9 files + INDEX) · FRD v1.0 · 2026-08-28 · Lane Mode v2
> **ไม่มี `PRINT_SPEC.md` โดยเจตนา** — feature นี้ไม่มีท่อ `pdfdoc` (ไม่มีเอกสารที่คนถือ/พิมพ์) · ดู `00_OVERVIEW §0.1`

## 📂 Pack Contents

| ไฟล์ | ใครอ่าน | สาระ |
|---|---|---|
| `00_OVERVIEW.md` | ทุกคน | scope · dependencies · **§0.12 Coverage Manifest (65 FN · 55 story · 24 BR)** · **§0.13 Published Rate Surface** · §0.14 invariant P-1′…P-9′ · §0.15 soft-reference read model |
| `01_UI.md` | FE | Layout Decision Log · 6 หน้า · journey · empty state · ข้อความบนจอ |
| `02_API.md` | BE | 27 endpoint · common concerns · **§2.X Cross-Module Contract** · trace ไป logic |
| `03_LOGIC.md` | BE | 55 function · 6 engine (**3 engine candidate ใหม่**) · trace table + self-check |
| `04_DB.md` | DBA / BE | 9 ตาราง · classification ทุกคอลัมน์ · retention · performance |
| `05_RULES.md` | BE / QA | BR-01…BR-24 · state machine 3 ชุด · VR-01…VR-22 · edge case 32 · error catalog · Security Bible |
| `06_TESTS.md` | QA | AC 59 · CT 5 · DoD · **§6.10 expected text verbatim** |
| `07_LOCKED_DECISIONS.md` | ทุกคน | **§7.0 Scope Lock (immutable)** · LD-01…LD-06 · OQ 30 ข้อ · tradeoff |
| `UI_BRIEF_โครงเงินเดือน.md` | FE / BA | สรุปหน้าจอจาก HTML จริง + Drift Log (S7) |
| `INDEX.md` | ทุกคน | ไฟล์นี้ |

## 🔍 Quick Nav by Question

**"ผม FE dev — เริ่มอ่านที่ไหน?"** → `01_UI §1.0` (Layout Decision Log) → `§1.2` ต่อหน้า → `§1.6` ข้อความ → `02_API §2.2` เฉพาะ endpoint ที่หน้าคุณเรียก
**"ผม BE dev — จะสร้าง endpoint"** → `02_API §2.2` → `03_LOGIC §3.1` (ฟังก์ชันที่ต้องมี) → `05_RULES §5.1` (กติกาที่ต้องบังคับ) → `04_DB §4.2`
**"ผม DBA"** → `04_DB` ทั้งไฟล์ · จุดที่ต้องระวัง = EXCLUDE constraint (§4.2) + trigger กัน UPDATE/DELETE + classification (§4.6)
**"ผม QA"** → `06_TESTS §6.1` (AC) → `§6.9` (cross-module) → `§6.10` (ข้อความ verbatim) → `05_RULES §5.5` (edge case)
**"ผม PM — มี risk อะไรค้าง?"** → `07_LOCKED §7.3` (OQ 30 ข้อ) · เร่งด่วนที่สุด = **OQ-STD-11** (group `legal_minimum`) กับ **OQ-SS-01** (นอกกระบอก)
**"ผม Architect — engine candidate ตัวไหน?"** → `03_LOGIC §3.2`: **ENG-EFFDATE-01** `effective-window-resolver` · **ENG-SALBAND-01** `salary-band-position-calculator` · **ENG-RECUR-01** `recurring-item-terminator` (ทั้งสามเป็น NEW candidate)
**"ผมทำ feature ปลายทาง (Payroll / Manpower / หนังสือรับรอง / Employee Movement)"** → อ่าน **`00_OVERVIEW §0.13` ทั้งหัวข้อ** แล้วยก §0.13.2 + §0.13.4 + §0.14.1 ไปใส่ใน FRD ของคุณ

## 🔗 Cross-Reference Tables

### Page → API
| Page | API ที่เรียก |
|---|---|
| P-01 ระดับ/กระบอก | API-01 · 02 · 03 · 04 · 05 · 06 · 07 · 08 |
| P-02 องค์ประกอบ | API-10 · 11 · 12 |
| P-03 อัตราพนักงาน | API-13 · 14 · 15 · 16 · 17 |
| P-04 รายการประจำ | API-18 · 19 · 20 |
| P-05 ทะเบียนการใช้งาน | API-21 · 22 · 23 |
| P-06 เทียบเวอร์ชัน | API-09 |
| (ไม่มีหน้าจอ · service เท่านั้น) | **API-24 · API-25 · API-26 · API-27** |

### API → Logic
ดูตารางเต็มที่ `02_API §2.4` และ `03_LOGIC §3.3` — สรุป: ทุก mutation API มี ≥1 function/engine · ไม่มี orphan

### API → DB
| API | ตารางที่แตะ |
|---|---|
| API-01…09 | `T_ss_grade` · `T_ss_band_version` · `T_ss_cfg_ref` |
| API-10…12 | `T_ss_pay_component` |
| API-13…17 | `T_ss_comp_record` · `T_ss_recurring_item` · `T_ss_change_reason` · `T_ss_cfg_ref` |
| API-18…20 | `T_ss_recurring_item` |
| API-21…23 · 27 | `T_ss_consumer_usage` · `T_ss_cfg_ref` |
| API-24 · 25 | อ่านทุกตารางหลัก (read-only) + อัปเดต `last_read_at` |
| API-26 | `T_ss_comp_record` · `T_ss_idempotency` |

### Engine ↔ Feature
| Engine | สถานะ | ใครใช้ต่อได้ |
|---|---|---|
| `effective-window-resolver` (ENG-EFFDATE-01) | **NEW candidate** | HR Configuration · Employee Movement · Shift & Roster · Welfare |
| `salary-band-position-calculator` (ENG-SALBAND-01) | **NEW candidate** | Employee Movement · Manpower Planning · Performance |
| `recurring-item-terminator` (ENG-RECUR-01) | **NEW candidate** | Welfare · Expense Claim · Payroll |
| `csq-event-emitter` (ENG-CSQ-01) | EXISTING | ทุก feature |
| `data-masking-resolver` (ENG-MASK-01) | EXISTING (Policy Center) | ทุก feature ที่มีข้อมูล Restricted |
| `hr-config-resolver` (ENG-HRCFG-01) | EXISTING (F-HR-CONFIG) | เรียกผ่าน HTTP เท่านั้น |

## 🚨 R8 Verification Matrix

| ตรวจ | ผล |
|---|---|
| ทุก mutation API มี ≥1 Function/Engine | ✅ (17 mutation endpoint) |
| ทุก Function ใน §3.1 ถูก trace ≥1 API/scheduler | ✅ (55/55) |
| ทุก Engine ถูกเรียกผ่าน Function หรือ API | ✅ (6/6) |
| ไม่มี orphan Function/Engine | ✅ |
| ไม่มี Engine ที่อ้างคำศัพท์ HTTP | ✅ |
| feature ไม่ bypass API ไปเรียก engine ของ feature อื่น | ✅ (`ENG-HRCFG-01` ผ่าน HTTP เท่านั้น) |
| ไม่มี "createX/updateX" แอบอยู่ใน 02_API | ✅ (02_API เป็น HTTP layer ล้วน) |
| ไม่มีการคำนวณ pure แอบอยู่ใน 02_API | ✅ (compa-ratio อยู่ที่ ENG-SALBAND-01) |

## 📊 Pack Statistics

| รายการ | จำนวน |
|---|---|
| หน้าจอ | 6 (5 route + 1 drawer) |
| Endpoint | 27 (17 mutation · 10 read) |
| Function | 55 |
| Engine | 6 (3 ใหม่ · 3 มีอยู่แล้ว) |
| ตาราง | 9 |
| Business Rules | 24 |
| Validation Rules | 22 |
| Edge Cases | 32 (☑15 · ☐17) |
| Acceptance Criteria | 59 + 5 cross-module |
| Error codes | 23 |
| CSQ events | 10 (EC · SecC) |
| FN coverage | **65/65** |
| Open Questions | 30 |
| Scope drift | **0** |

## 🎯 Reading Order Recommendation

**อ่านครั้งแรก (ทุกบทบาท):** `00_OVERVIEW §0.3` scope → `§0.13` published surface → `07_LOCKED §7.0` scope lock → `05_RULES §5.1` BR
**Onboarding dev ใหม่:** 00 → 01 → 04 → 02 → 03 → 05 → 06
**Architect review:** `03_LOGIC §3.2` (engine candidate) → `02_API §2.X` (cross-module) → `00_OVERVIEW §0.13`/`§0.14` (สัญญาที่ feature อื่นจะยึด) → `07_LOCKED §7.4` tradeoff

## Coverage Manifest Pointer ⭐
`00_OVERVIEW §0.12` — Stories 55/55 · **FN 65/65** · BR 24/24 · Scenario 47/47 · Edge 32/32 · Functions Cut 15/15 · **หล่น 0**
