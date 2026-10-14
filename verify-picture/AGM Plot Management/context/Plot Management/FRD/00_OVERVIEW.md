# 00_OVERVIEW — F-AGM-003 Plot Management

> **Pack STANDARD (7 ไฟล์)** · Refactor Wave · constraint mode (invariants.md 🔒)
> Audience: ทีม dev/QA · Source of truth: BRD APPROVED + invariants LOCKED + legacy code

## §0.1 Feature
| Field | Value |
|---|---|
| ID | F-AGM-003 · Plot Management (จัดการแปลงที่ดิน) |
| Module | AGM · WKN |
| Upstream | F-AGM-002 Quota (read-only) · F-AGM-001 Farmer (indirect) |
| Route | `#/plots` (list) · `#/plots/:plot_code` (detail drawer) · create/edit/import/verify = overlay |
| CI | CUBE Warm Light (html-generator-v6) |

## §0.11 Scope Lock (จาก BRD §3.4 — inherited)
LOCK-01..12 (ดู BRD §3.4) — สรุป: capability legacy 100% · 3-state machine · **quota binding บังคับ (read-only)** · address 5-field+province · **shapefile mandatory** · 1:N · edit ไม่เปลี่ยน status · verify confirm+fail reason · bulk fail เหตุผลเดียว · soft/hard delete · CSV partial success · optimistic lock+idempotency+audit · deed unique

## §0.12 Coverage Manifest (กัน requirement หล่น)
| Story | Layer coverage | Test |
|---|---|---|
| US-01 create + quota bind | 01_UI OV-01 · 02_API API-02/13 · 03_LOGIC FN-01/04/11 · 04_DB T_plot | AC-01..08 |
| US-02 quota not found | 01_UI · API-13 · FN-11 | AC-02b |
| US-03 CSV import | OV-05 · API-09/10 · FN-09 | AC-14..17 |
| US-04 detail 3-tab | P-02 · API-04/12 | AC-24..25 |
| US-05 verify single | OV-03 · API-07 · FN-06 | AC-18..20 |
| US-06 bulk verify | OV-03 · API-08 · FN-07 | AC-21..23 |
| US-07 edit no-status-change | OV-02 · API-05 · FN-03 | AC-11..13 |
| US-08 soft/hard delete | OV-04 · API-11 · FN-08 | AC-26..27 |
| US-09 search/filter/sort/export | P-01 · API-01/14 · FN-05 | AC-09/10/28 |
| US-10 audit log | P-02 tab3 · API-12 | AC-25 |
> Coverage: 10/10 stories · FN-01..12 · API-01..14 ✅

## §0.13 Variant = STANDARD (7 files)
00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS

## §0.14 Cross-Module Summary
Plot อ่าน Quota (search + farmer snapshot) ผ่าน ENG-EXT-Q01 · store quota_id · **ไม่มี write-back** · downstream (future) สัญญาส่งอ้อย อ่าน plot verified

## §0.15 EN-PAGE Traceability (authoritative page-fn ↔ CUBE artifacts) — G2
> map page-function ทางการ (EN-PAGE-0001-00046..00052 + SFN-CF-*) → artifact ในชุดนี้ (own P-/OV-/API-/FN numbering เป็น CUBE adaptation — คงไว้)

| Authoritative EN-PAGE (page fn) | SFN-CF-* (sub-fn) | Page/Overlay | API | FN |
|---|---|---|---|---|
| EN-PAGE-0001-00046 Create Plot | SER-00039 · VAL-00041 · CRE-00042 | OV-01 Create | API-02/03/13 | FN-01,04,11,12,10 |
| EN-PAGE-0001-00047 Import CSV | UPL-00043 · VAL-00044 · CRE-00045 | OV-05 Import | API-09/10 | FN-09 (→04,01,10) |
| EN-PAGE-0001-00048 View Plot Detail | VIEW-00046 | P-02 Detail | API-04/12 | FN-10 (hist) |
| EN-PAGE-0001-00049 Edit Plot | UPT-00047 | OV-02 Edit | API-05 | FN-03,04,12,10 |
| EN-PAGE-0001-00050 Verify (Single/Bulk) | UPT-00048 | OV-03 Verify | API-07/08 | FN-06,07,10 |
| EN-PAGE-0001-00051 Delete Plot | DEL-00049 | OV-04 Delete | API-11 | FN-08,10 |
| EN-PAGE-0001-00052 Search/Filter/Export | SER-00050 · GEN-00051 | P-01 List | API-01/14 | FN-05 |

## Revision
| วันที่ | รายละเอียด |
|---|---|
| 2026-07-23 | อัปเดตตาม authoritative: CSV shapefile_url บังคับ (13 คอลัมน์), EN-PAGE ID mapping, wizard 5 ขั้น, Export executable, coord 6 ทศนิยม |
