# 00_OVERVIEW — F-AGM-004 Crop Management

> Pack STANDARD (7 ไฟล์) · Refactor Wave · constraint mode (invariants.md 🔒)

## §0.1 Feature
| Field | Value |
|---|---|
| ID | F-AGM-004 · Crop Management (การจัดการรอบปลูก) |
| Module | AGM · WKN |
| Upstream | F-AGM-002 Quota + F-AGM-003 Plot (double read-only) · ETCD/Survey external |
| Route | `#/crops` (list) · `#/crops/:crop_id` (Landing drawer) · create/edit/csv = overlay |
| CI | CUBE Warm Light |

## §0.11 Scope Lock (BRD §3.4)
LOCK-01..13 — สรุป: capability 100% · canonical 5-state · **double-binding (quota→plot) read-only** · snapshot read-only · **edit verified→waiting** · quota/plot immutable on edit · verify/reject (reject reason บังคับ) เดี่ยว+bulk · **remaining=total−ΣETCD ติดลบได้+badge** · ETCD/Survey read-only fail-soft · CSV partial · soft cancel/delete+reason · optimistic+idempotency+audit · year 2500-2600/month 1-12/tons≥0

## §0.12 Coverage Manifest
| Story | Layer | Test |
|---|---|---|
| US-01 create double-bind | 01_UI OV-01 · API-02/13/14 · FN-01/04/11/12 | AC-01..08 |
| US-02 quota/plot invalid | API-13/14 · FN-11/12 | AC-02b/02c |
| US-03 CSV | OV-05 · API-09 · FN-09 | AC-14..17 |
| US-04 landing tabs | P-02 · API-04/15/16 | AC-24..26 |
| US-05/06 verify/reject | OV-03 · API-07 · FN-06 | AC-18..20 |
| US-07 bulk | OV-03 · API-08 · FN-07 | AC-21..23 |
| US-08 edit → waiting | OV-02 · API-05 · FN-03 | AC-11..13 |
| US-09 cancel/delete | OV-04 · API-11 · FN-08 | AC-27..28 |
| US-10 search/export/remaining | P-01 · API-01/17 · FN-05/13 | AC-09/10/29 |
> Coverage 10/10 · FN-01..13 · API-01..17 ✅

## §0.13 Variant = STANDARD (7 files)

## §0.14 Cross-Module Summary
Crop อ่าน Quota (verified,exact) + Plot (owner+verified) ผ่าน ENG-EXT-QP · อ่าน ETCD/Survey ผ่าน ENG-EXT-ES (fail-soft) · store quota_id/plot_id + snapshot · **ไม่มี write-back** · downstream สัญญาส่งอ้อย (future) อ่าน crop verified
