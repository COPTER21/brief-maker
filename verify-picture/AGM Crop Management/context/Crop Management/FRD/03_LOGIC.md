# 03_LOGIC — F-AGM-004 Crop Management

> R8: ทุก mutation API → ≥1 Function · no HTTP ใน function

## §3.1 Functions
| FN | Name | Purpose | Calls | Invoked by |
|---|---|---|---|---|
| FN-01 | `createCrop` | สร้าง (double-bind) | FN-04,11,12,13,10 | API-02 |
| FN-03 | `updateCrop` | แก้ไข + optimistic · **verified→waiting** (LOCK-05) · quota/plot immutable | FN-04,10 | API-05 |
| FN-04 | `validateCropData` | validation รวม (VR-01..08) | ENG-EXT-QP | FN-01/03/09 |
| FN-05 | `buildCropListQuery` | list query + filter + remaining badge + ตัด cancelled/deleted default | FN-13 | API-01 |
| FN-06 | `verifyRejectCrop` | verify/reject เดี่ยว + state machine · reject reason บังคับ | FN-10 | API-07, FN-07 |
| FN-07 | `bulkVerifyReject` | orchestrate กลุ่ม · skip non-waiting · shared reject reason · partial | FN-06,10 | API-08 |
| FN-08 | `cancelDeleteCrop` | cancel/delete soft + reason + audit | FN-10 | API-11 |
| FN-09 | `importCropCsv` | CSV per-row · quota/plot verified check + field · idempotent · ทุกแถว waiting | FN-04,01,10 | API-09 |
| FN-10 | `recordCropHistory` | append-only audit (create/edit/verify/reject/cancel/delete + bulk count) | — | FN-01/03/06/07/08/09 |
| FN-11 | `resolveQuota` ⭐ | quota exact + verified → farmer snapshot | ENG-EXT-QP | FN-01, API-13 |
| FN-12 | `resolvePlot` ⭐ | plot ของเจ้าของ quota + verified → address/size snapshot | ENG-EXT-QP | FN-01, API-14 |
| FN-13 | `computeRemaining` ⭐ | remaining = total_tons − ΣETCD (fail-soft) · negative flag | ENG-EXT-ES | FN-05, API-04/15 |

## §3.2 Engines
- **ENG-EXT-QP** `crop-source-connector` [NEW read-only] ⭐ — (a) quota exact+verified, (b) plots ของเจ้าของ+verified · wrap F-AGM-002/003 API · **read-only** · used FN-11/12
- **ENG-EXT-ES** `etcd-survey-reader` [NEW read-only] ⭐ — ETCD bookings + Survey · **fail-soft** (external down → null+flag, ไม่ block) · used FN-13, API-15/16
- **ENG-EXT-01** `csv-import-framework` [EXISTING] — FN-09

## §3.3 API ↔ Logic Trace (R8)
| API | Functions | Engines |
|---|---|---|
| API-01 | FN-05,13 | ENG-EXT-ES |
| API-02 | FN-01,04,11,12,13,10 | QP, ES |
| API-04 | FN-13 | ES |
| API-05 | FN-03,04,10 | — |
| API-07 | FN-06,10 | — |
| API-08 | FN-07(→06),10 | — |
| API-09 | FN-09(→04,01),10 | 01, QP |
| API-11 | FN-08,10 | — |
| API-13 | FN-11 | QP |
| API-14 | FN-12 | QP |
| API-15/16 | FN-13 | ES |
| API-17 | FN-05 | — |
> mutation (02/05/07/08/09/11) มี ≥1 FN + FN-10 ✅ · double cross-module FN-11/12 read-only ✅ · FN-13 fail-soft ✅

## §3.5 Locked Decisions
- LOCK-03: double-binding FN-11/12 read-only
- LOCK-05: FN-03 verified→waiting (Crop-specific)
- LOCK-08: FN-13 remaining compute (negative allowed)
- LOCK-09: ENG-EXT-ES fail-soft
- LOCK-12: optimistic + idempotency + FN-10 audit
