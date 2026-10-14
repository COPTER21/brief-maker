# 03_LOGIC — F-AGM-003 Plot Management

> R8: ทุก mutation API → ≥1 Function · Iron rule: no HTTP ใน function

## §3.1 Functions
| FN | Name | Purpose | Calls | Invoked by |
|---|---|---|---|---|
| FN-01 | `createPlot` | สร้างแปลง ผูก quota | FN-04, FN-11, FN-10, ENG-EXT-02 | API-02 |
| FN-02 | (reserved import row → FN-09) | — | — | — |
| FN-03 | `updatePlot` | แก้ไข + optimistic lock · **ไม่เปลี่ยน status** (LOCK-07) | FN-04, FN-10 | API-05 |
| FN-04 | `validatePlotData` | validation รวมศูนย์ (VR-01..07,10) | ENG-EXT-02 | FN-01/03/09, API-03 |
| FN-05 | `buildPlotListQuery` | list query 5-field search + filter status/province + sort + page + ตัด is_deleted | — | API-01 |
| FN-06 | `verifyPlot` | verify เดี่ยว + state machine + reason(fail) + optimistic | FN-10 | API-07, FN-07 |
| FN-07 | `bulkVerifyPlots` | orchestrate กลุ่ม · shared fail_reason · partial result | FN-06, FN-10 | API-08 |
| FN-08 | `deletePlot` | soft/hard + reason + audit | FN-10 | API-11 |
| FN-09 | `importPlotCsv` | CSV wizard commit · file/row validate · partial success · ทุกแถว waiting | FN-04, FN-01, FN-10 | API-09 |
| FN-10 | `recordPlotHistory` | append-only audit (create/edit/verify/delete/import + bulk count) | — | FN-01/03/06/07/08/09 |
| FN-11 | `resolveQuotaBinding` ⭐ cross-module | ตรวจ+ผูก quota (read farmer snapshot) ก่อนสร้าง | ENG-EXT-Q01 | FN-01, API-13 |
| FN-12 | `checkDeedUnique` | deed_number unique (exclude self) | — | FN-04 |

## §3.2 Engines
- **ENG-EXT-02** `m01-address-hierarchy` [EXISTING] — cascade จังหวัด/อำเภอ/ตำบล + postal · used FN-01/03/04/09
- **ENG-EXT-Q01** `quota-plot-connector` [NEW — read-only adapter] ⭐ — (a) search quota (verified), (b) get farmer snapshot · wrap F-AGM-002 API (`GET quota-search`, `GET :id/farmer-snapshot`) · **read-only** (ไม่มี write) · used FN-11
- **ENG-EXT-01** `csv-import-framework` [EXISTING] — used FN-09

## §3.3 API ↔ Logic Trace (R8)
| API | Functions | Engines |
|---|---|---|
| API-01 | FN-05 | — |
| API-02 | FN-01,04,11,10,12 | ENG-EXT-02, Q01 |
| API-03 | FN-04 | ENG-EXT-02 |
| API-05 | FN-03,04,10,12 | ENG-EXT-02 |
| API-06 | FN-12 | — |
| API-07 | FN-06,10 | — |
| API-08 | FN-07(→06),10 | — |
| API-09 | FN-09(→04,01),10 | ENG-EXT-01,02 |
| API-11 | FN-08,10 | — |
| API-13 | FN-11 | ENG-EXT-Q01 |
| API-14 | FN-05 | — |
> ทุก mutation (02/05/07/08/09/11) มี ≥1 FN + FN-10 ✅ · cross-module FN-11 read-only ✅

## §3.5 Locked Decisions
- LOCK-03: quota binding FN-11 (read-only, ไม่ write-back)
- LOCK-07: FN-03 ไม่แตะ verify_status
- LOCK-11: optimistic version + idempotency ทุก mutation · FN-10 audit
- OQ-P4: FN-12 deed dup → reject
