# INDEX — FRD Pack · ทะเบียนหน่วยวัด (F-UOM-001)

| | |
|---|---|
| **FRD ID** | `FRD-F-UOM-001` |
| **Pack Variant** | **STANDARD (8 ไฟล์ + INDEX)** |
| **Upstream** | `BRD_uom-master.md` v1.0 — ✅ **APPROVED** (AI Review 27/28 · 0 ไม่ผ่าน) |
| **HTML ตัวจริง** | `_final-docs/F-UOM-001/uom-master.html` |
| **Version** | 1.0 · 2026-08-10 |

## ไฟล์ในแพ็ก

| ไฟล์ | ชั้น | ตอบคำถามอะไร |
|---|---|---|
| [`00_OVERVIEW.md`](00_OVERVIEW.md) | — | ขอบเขต · variant · traceability · สัญญาข้ามเอกสาร · Open Questions |
| [`01_UI.md`](01_UI.md) | Presentation | route · โครงหน้าจอ · component ที่ใช้ · สถานะของจอ · microcopy |
| [`02_API.md`](02_API.md) | Interface | endpoint · request/response · error code · **§2.9 สัญญาข้ามเอกสาร** |
| [`03_LOGIC.md`](03_LOGIC.md) | Application | ตรรกะฝั่ง server · ลำดับการทำงาน · Logic Placement Matrix |
| [`04_DB.md`](04_DB.md) | Data | ตาราง · คอลัมน์ · index · seed · Data Classification |
| [`05_RULES.md`](05_RULES.md) | Cross-cutting | กติกาธุรกิจ · validation · การจัดการข้อผิดพลาด |
| [`06_TESTS.md`](06_TESTS.md) | QA | เงื่อนไขการทดสอบ · trace กลับกติกา · DoD |
| [`07_LOCKED_DECISIONS.md`](07_LOCKED_DECISIONS.md) | Governance | **มติที่ล็อกแล้ว — feature อื่นต้องยึดตาม** |

## ลำดับการอ่านที่แนะนำ

| ผู้อ่าน | อ่านอะไรก่อน |
|---|---|
| Dev ฝั่งหน้าจอ | `01_UI` → `02_API` → `05_RULES` |
| Dev ฝั่งหลังบ้าน | `04_DB` → `03_LOGIC` → `02_API` → `05_RULES` |
| QA | `06_TESTS` → `05_RULES` → `01_UI` |
| **ทีมที่ทำ feature อื่นที่อ้างถึงทะเบียนนี้** | **`07_LOCKED_DECISIONS` → `02_API §2.9`** |

## Sync Read (แหล่งกฎหน้าตา — ห้าม hardcode ค่าเอง)

`.claude/skills/html-generator-v8/` — `knowledge/iron-rules.md` · `ci-tokens.md` · `microcopy.md` · `component-contracts.md` · `layout-integrity.md` · `page-anatomy.md`
