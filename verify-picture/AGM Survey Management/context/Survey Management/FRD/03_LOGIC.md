# 03_LOGIC — F-AGM-006 Survey Management

> R8: mutation API → ≥1 Function · no HTTP ใน function

## §3.1 Functions
| FN | Name | Purpose | Calls | Invoked by |
|---|---|---|---|---|
| FN-01 | `createSurvey` | cascade + validate | FN-04,11,10 | API-02 |
| FN-03 | `updateSurvey` | แก้ไข + optimistic · **verified→waiting** (LOCK-07) · cascade immutable | FN-04,10 | API-05 |
| FN-04 | `validateSurveyData` | validation (VR-01..06) | ENG-EXT-AGM | FN-01/03/09 |
| FN-05 | `buildSurveyListQuery` | list + filter status/year + sort + page | — | API-01 |
| FN-06 | `verifyRejectSurvey` | verify/reject เดี่ยว + state machine · reject reason บังคับ | FN-10 | API-07, FN-07 |
| FN-07 | `bulkVerifyReject` | orchestrate กลุ่ม · skip non-waiting · shared reason · partial | FN-06,10 | API-08 |
| FN-08 | `cancelDeleteSurvey` | cancel/delete soft + reason + audit | FN-10 | API-11 |
| FN-09 | `importSurveyCsv` | CSV per-row · cascade+field · idempotent · ทุกแถว waiting | FN-04,01,10 | API-09 |
| FN-10 | `recordSurveyHistory` | append-only audit | — | FN-01/03/06/07/08/09 |
| FN-11 | `resolveCascade` ⭐ | read quota→plots→crops (verified) + snapshot | ENG-EXT-AGM | FN-01, API-13/14 |

## §3.2 Engines
- **ENG-EXT-AGM** `survey-source-connector` [NEW read-only] ⭐ — read quota/plot/crop cascade · wrap F-AGM-002/003/004 · **read-only** · used FN-11
- **ENG-EXT-01** `csv-import-framework` [EXISTING] — FN-09

## §3.3 API ↔ Logic Trace (R8)
| API | Functions | Engines |
|---|---|---|
| API-01 | FN-05 | — |
| API-02 | FN-01,04,11,10 | AGM |
| API-05 | FN-03,04,10 | — |
| API-07 | FN-06,10 | — |
| API-08 | FN-07(→06),10 | — |
| API-09 | FN-09(→04,01),10 | 01, AGM |
| API-11 | FN-08,10 | — |
| API-13/14 | FN-11 | AGM |
> mutation (02/05/07/08/09/11) มี ≥1 FN + FN-10 ✅ · cascade FN-11 read-only ✅

## §3.5 Locked Decisions
- LOCK-03: cascade FN-11 (read quota/plot/crop)
- LOCK-07: FN-03 verified→waiting
- LOCK-10: optimistic + idempotency + FN-10 audit
