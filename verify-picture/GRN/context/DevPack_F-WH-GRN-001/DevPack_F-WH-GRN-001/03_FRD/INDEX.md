# INDEX — FRD Pack F-WH-GRN · GRN รับของ (FULL · 9 files + INDEX)

## Quick Nav

| ไฟล์ | ใครอ่าน | สาระ |
|---|---|---|
| [`00_OVERVIEW.md`](00_OVERVIEW.md) | ทุกคน | Document control · scope · roles · **Coverage Manifest §0.12** · **Open Questions §0.13** |
| [`01_UI.md`](01_UI.md) | FE dev | **Layout Decision Log §1.0** (13 หน้า) · anatomy · components · z-index contract |
| [`02_API.md`](02_API.md) | BE dev (HTTP) | 12 endpoints · error catalog · idempotency · **Cross-Module Contract §2.7** |
| [`03_LOGIC.md`](03_LOGIC.md) | BE dev (business) | 15 Functions · **4 Engines** · **Trace Table §3.3** |
| [`04_DB.md`](04_DB.md) | DBA / BE dev | 5 tables · **Data Classification §4.6** · soft-ref contract · indexes |
| [`05_RULES.md`](05_RULES.md) | BE dev + QA | BR-01..24 · VR01..16 · state transitions · E-01..E-18 · **CF-01..06** |
| [`06_TESTS.md`](06_TESTS.md) | QA | AT-01..94 · config · permission · **cross-module §6.9** · DoD |
| [`07_LOCKED_DECISIONS.md`](07_LOCKED_DECISIONS.md) | ทุกคน | **LOCK-01..07** · HANDOFF §3 ครบ 7 ข้อ · **LD-01..09** |
| ใบประกาศ | dev + ผู้ตั้งค่าระบบ | `NTF_BRIEF` · `CSQ_BRIEF` · `DOCCFG_BRIEF` · `print-spec-grn` |

## Function Trace (API → Logic → DB)

| API | Functions | Engines | Tables |
|---|---|---|---|
| API-01 `GET /grn` | FN-01, FN-08, FN-14 | — | header, line |
| API-02 `GET /grn/{id}` | FN-08, FN-09, FN-14 | — | ทุกตาราง |
| API-03 `GET /grn/selectable-pos` | FN-02 | — | (PO ภายนอก) |
| API-04 `POST /grn` | FN-03 | — | header, line, audit |
| API-05 `PUT /grn/{id}` | FN-04, FN-05, FN-08, FN-10 | ENG-GRN-01, ENG-GRN-02 | header, line, audit |
| API-06 `POST .../refresh-from-po` | FN-06, FN-05 | ENG-GRN-02 | line, audit |
| **API-07 `POST .../post`** ★ | FN-11, FN-05, FN-08, FN-09, FN-10 | ENG-DOC-NUM, ENG-GRN-01..04, ENG-NOTIFY, ENG-CSQ | header, line, movement, audit + **PO ภายนอก** |
| **API-08 `POST .../reverse`** ★ | FN-13 | ENG-GRN-03, ENG-GRN-04, ENG-NOTIFY, ENG-CSQ | header, movement, audit + **PO ภายนอก** |
| API-09 `POST .../discard` | FN-12 | — | header, audit |
| API-10 attachments | — | — | attachment, audit |
| API-11 `GET .../print` | FN-15, FN-08 | — | header, line |
| API-12 `GET /grn/check-dn` | FN-07 | — | header |

## ★ FN-xx map — สองชุดที่ชนกัน (อย่าสับสน · LD-08)

| ชุด | รหัส | ความหมาย | อยู่ที่ |
|---|---|---|---|
| **ธุรกิจ** | `FN-01..FN-39` · `FN-90..FN-94` (44 ข้อ) | ฟังก์ชันที่ QA/BA ติ๊กตรวจ | `02_BRD/FUNCTION_CHECKLIST_F-WH-GRN.md` · `01_HTML/_COVERAGE_REPORT.md` |
| **โค้ด** | `F-WH-GRN-FN-01..FN-15` | ฟังก์ชันชั้น logic ที่ dev เขียน | `03_LOGIC §3.1` |

ตัวอย่างที่ชนกันชัด: **FN-07** ธุรกิจ = "คงเหลือหลังใบนี้อัพเดตสด" · **FN-07** โค้ด = `checkDuplicateDeliveryNote`

## Engines

| Engine | เจ้าของ | ใช้โดย |
|---|---|---|
| `ENG-GRN-01` grn-qc-engine | **F-WH-GRN** | F080 RTV (วางแผน) |
| `ENG-GRN-02` receipt-tolerance-engine | **F-WH-GRN** | F095 AP 3-way (วางแผน) |
| `ENG-GRN-03` stock-movement-engine | **F-WH-GRN** | F081 Putaway · F080 RTV (วางแผน) |
| `ENG-GRN-04` po-receipt-sync-engine | **F-WH-GRN** | — (ทางเดียวที่เขียน `PO.received`) |
| `ENG-DOC-NUM` · `ENG-NOTIFY` · `ENG-CSQ` | กลาง | เรียกใช้ผ่านใบประกาศใน `03_FRD/` |

## Traceability chain

```
PREBRIEF (OB · S · BR)  →  BRD (R · VR · E · CF · DR · IS · OS)  →  FRD
   └─ FUNCTION_CHECKLIST 44 FN ──────────────► 01_HTML/_COVERAGE_REPORT.md (รอบ 1 + รอบ 2)
                                  BR-01..24 ─► 05_RULES §5.1 ─► 06_TESTS AT-xx
                                  VR01..16  ─► 05_RULES §5.2 ─► 02_API §2.5 error catalog
                                  E-01..18  ─► 05_RULES §5.4 ─► 06_TESTS
                                  CF-01..06 ─► 05_RULES §5.6 ─► 06_TESTS §6.2
                                  IS/OS     ─► 02_API §2.7   ─► 06_TESTS §6.9
                                  LOCK-01..07 + HANDOFF §3 ──► 07_LOCKED §7.0/§7.1
```

## Phase 3.5 Verification — สรุปผล

| Section | ผล |
|---|---|
| A · Pack completeness (9 + INDEX) | ✅ |
| B · Mutation API contracts ครบ | ✅ 7/7 |
| C · R8 logic traceability (ไม่มี orphan) | ✅ |
| D · API ↔ DB linkage | ✅ |
| E · UI ↔ API cross-reference | ✅ |
| F · Engine iron rules (pure · ไม่มีศัพท์ HTTP) | ✅ 4/4 |
| G · Logic placement compliance | ✅ |
| H · Security Bible (P1 Standard Transaction · 12 controls) | ✅ |
| I · Convention compliance | ✅ (deviation 1 ข้อ บันทึกที่ `07_LOCKED §7.3`) |
| J · R10 Data Classification | ✅ ไม่มี Public · ไม่มี Restricted |
| K · R13 Coverage Manifest | ✅ ไม่มี requirement หล่น |
| L · R11/R12 Scope Lock + Value Stream | ✅ LOCK 7 ข้อ + HANDOFF §3 7 ข้อ ยกครบ |
| **M · R14 HTML Alignment** | ✅ 13 หน้า = 13 หน้า · route ตรง · pattern ตรง · expected text verbatim |

**Verdict: ✅ ผ่านทุก section**
