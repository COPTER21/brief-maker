# 00_OVERVIEW — F-AGM-006 Survey Management

> Pack STANDARD (7 ไฟล์) · Refactor Wave · constraint mode (invariants.md 🔒) · T3 code-derived

## §0.1 Feature
| Field | Value |
|---|---|
| ID | F-AGM-006 · Survey Management (จัดการแบบสำรวจ) |
| Module | AGM · WKN |
| Upstream | F-AGM-002/003/004 (read cascade) · feeds Crop survey tab |
| Route | `#/surveys` (list) · `#/surveys/:survey_id` (detail drawer) · create/edit/csv = overlay |
| CI | CUBE Warm Light |

## §0.11 Scope Lock (BRD §3.4)
LOCK-01..11 — สรุป: capability 100% · canonical 5-state · **cascade (quota→plot→crop)** · agronomic fields · **photos 4 หมวด** · verify/reject (reject reason บังคับ) เดี่ยว+bulk · edit verified→waiting · CSV partial · soft cancel/delete · optimistic+idempotency+audit · feeds Crop survey tab

## §0.12 Coverage Manifest
| Story | Layer | Test |
|---|---|---|
| US-01 create cascade | 01_UI OV-01 · API-02/13/14 · FN-01/04/11 | AC-01..09 |
| US-02 cascade invalid | API-13/14 · FN-11 | AC-02b |
| US-03 CSV | OV-05 · API-09 · FN-09 | AC-14..17 |
| US-04 detail tabs | P-02 · API-04 | AC-24..25 |
| US-05/06 verify/reject | OV-03 · API-07 · FN-06 | AC-18..20 |
| US-07 bulk | OV-03 · API-08 · FN-07 | AC-21..23 |
| US-08 edit → waiting | OV-02 · API-05 · FN-03 | AC-11..13 |
| US-09 cancel/delete | OV-04 · API-11 · FN-08 | AC-26..27 |
| US-10 search/export | P-01 · API-01/15 · FN-05 | AC-10/28 |
> Coverage 10/10 · FN-01..11 · API-01..15 ✅

## §0.13 Variant = STANDARD (7 files)

## §0.14 Cross-Module Summary
Survey อ่าน Quota→Plot→Crop (cascade) ผ่าน ENG-EXT-AGM · survey verified feeds Crop F-AGM-004 (แท็บสำรวจ — Crop pull-read) · **ไม่มี write-back**
