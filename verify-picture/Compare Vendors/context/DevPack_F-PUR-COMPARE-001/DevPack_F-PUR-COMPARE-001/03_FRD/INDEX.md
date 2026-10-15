# FRD Pack — F-PUR-COMPARE-001 · เทียบราคาผู้ขาย

**ขนาด pack:** STANDARD · **มาตรฐาน:** FRD v6.1 (SOW3.3) · **HTML-first**
**วันที่:** 2026-09-13 · **module:** Purchase (จัดซื้อ) · **registry:** F073 · `arch: master` · `dec: ["csq"]` · `wave: W2`

## Source of truth ตามลำดับความสำคัญ
1. **LOCK** — `02_BRD/BRD_F-PUR-COMPARE.md §3.4` + `HANDOFF.md §3` → ดู [`07_LOCKED_DECISIONS.md`](07_LOCKED_DECISIONS.md)
2. **BRD** (APPROVED 23/23) — เจตนาเชิงธุรกิจ
3. **HTML** `01_HTML/CompareVendors.html` — หน้าจอจริง (สกัด pattern จากที่นี่ ห้ามแต่งเพิ่ม)

## ไฟล์ใน pack

| ไฟล์ | เนื้อหา |
| --- | --- |
| [`00_OVERVIEW.md`](00_OVERVIEW.md) | ขอบเขต · archetype · สิ่งที่ไม่ทำและเหตุผล · Coverage Manifest |
| [`01_UI.md`](01_UI.md) | โครงหน้าจอ · Layout Decision Log · state matrix · microcopy |
| [`02_API.md`](02_API.md) | endpoint · payload · error catalog |
| [`03_LOGIC.md`](03_LOGIC.md) | สูตรคำนวณ · state machine · trigger point ของ 7C |
| [`04_DB.md`](04_DB.md) | 5 ตาราง · index · กติกาเพิ่มอย่างเดียว |
| [`05_RULES.md`](05_RULES.md) | BR-01..10 · V-01..07 · C-01..08 · EC-01..09 |
| [`06_TESTS.md`](06_TESTS.md) | เมทริกซ์ทดสอบ + traceability |
| [`07_LOCKED_DECISIONS.md`](07_LOCKED_DECISIONS.md) | LD-01..12 — สิ่งที่ห้ามเปลี่ยนโดยไม่กลับไปหา BA |
| [`HTML_UI_BRIEF_F-PUR-COMPARE-001.md`](HTML_UI_BRIEF_F-PUR-COMPARE-001.md) | บรีฟ UI สกัดจาก HTML 1:1 สำหรับ FE |
| [`CSQ_BRIEF_F-PUR-COMPARE-001.md`](CSQ_BRIEF_F-PUR-COMPARE-001.md) | ใบประกาศ 7C (จาก Phase A — ไม่แก้) |

## ใบประกาศที่ **ไม่** ทำ และเหตุผล
| ชิป | ทำไหม | เหตุผล |
| --- | --- | --- |
| ⚖ `doa` | ❌ | ฟีเจอร์นี้ไม่มีการอนุมัติ — การยืนยันผลเป็นการกระทำเชิงปฏิบัติงาน (BR-07 · LD-02) |
| 🔔 `ntf` | ❌ | ไม่ประกาศ event แจ้งเตือน — registry ชิปมีแค่ `csq` |
| `doccfg` | ❌ | `round_id` ไม่ใช่เลขที่เอกสาร ไม่ผ่านเครื่องออกเลขกลาง (LD-03) |
| 📄 `pdfdoc` | ❌ | ไม่มีแบบพิมพ์ (BR-07) |
> ทั้ง 4 ข้อ **ตั้งใจไม่ทำ ไม่ใช่ตกหล่น** — ถ้ามีใครเพิ่มเข้ามา = DIVERGENCE ต้องกลับไปที่ BA
