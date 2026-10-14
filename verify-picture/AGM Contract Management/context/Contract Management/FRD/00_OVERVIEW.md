# 00_OVERVIEW — F-AGM-005 Contract Management

> Pack STANDARD (7 ไฟล์) · Refactor Wave · constraint mode (invariants.md 🔒) · T3 code-derived

## §0.1 Feature
| Field | Value |
|---|---|
| ID | F-AGM-005 · Contract Management (จัดการสัญญาส่งอ้อย) |
| Module | AGM · WKN |
| Upstream | F-AGM-002/003/004 (read) · **write-back crop license** ⭐ |
| Route | `#/contracts` (list) · `#/contracts/:contract_id` (detail drawer) · create/edit = overlay |
| CI | CUBE Warm Light |

## §0.11 Scope Lock (BRD §3.4)
LOCK-01..10 — สรุป: capability 100% · 3-state · **build path (quota→plots→crops verified→type)** · **5 contract types** · aggregate tons · approve/reject (reject reason บังคับ) เดี่ยว+bulk · **write-back crop license (contracted/none)** · 1 crop:1 active contract · delete+attachments · optimistic+idempotency+audit

## §0.12 Coverage Manifest
| Story | Layer | Test |
|---|---|---|
| US-01 create build-path + write-back | 01_UI OV-01 · API-02/13/14 · FN-01/11/12 | AC-01..09 |
| US-02 quota/crop invalid | API-13/14 · FN-11 | AC-02b |
| US-03 detail tabs | P-02 · API-04 | AC-19..20 |
| US-04 approve | OV-03 · API-07 · FN-06 | AC-13..14 |
| US-05 reject + revert license | OV-03 · API-08 · FN-06/12 | AC-15..16 |
| US-06 bulk | OV-03 · API-09 · FN-07 | AC-17..18 |
| US-07 edit | OV-02 · API-05 · FN-03 | AC-11..12 |
| US-08 delete | OV-04 · API-11 · FN-08 | AC-21..22 |
| US-09 search/export | P-01 · API-01/15 · FN-05 | AC-10/23 |
> Coverage 9/9 · FN-01..12 · API-01..15 ✅

## §0.13 Variant = STANDARD (7 files)

## §0.14 Cross-Module Summary
Contract อ่าน Quota/Plot/Crop (verified) ผ่าน ENG-EXT-AGM · **เขียน crop.license_status (contracted/none)** ผ่าน crop-license-writer · downstream การส่งอ้อยเข้าโรงงาน (future) อ่าน contract verified
