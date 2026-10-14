# 03_LOGIC — F-AGM-005 Contract Management

> R8: mutation API → ≥1 Function · no HTTP ใน function

## §3.1 Functions
| FN | Name | Purpose | Calls | Invoked by |
|---|---|---|---|---|
| FN-01 | `createContract` | build-path + aggregate + **write crop license='contracted'** | FN-04,11,12,10 | API-02 |
| FN-03 | `updateContract` | แก้ไข type-specific/attachments + optimistic (quota/plots/crops immutable) | FN-04,10 | API-05 |
| FN-04 | `validateContractData` | validation (VR-01..05) + crop verified + license≠contracted | ENG-EXT-AGM | FN-01/03 |
| FN-05 | `buildContractListQuery` | list + filter status/type + sort + page | — | API-01 |
| FN-06 | `approveRejectContract` | approve/reject เดี่ยว + state machine · reject reason บังคับ · **reject → FN-12 revert license** | FN-12,10 | API-07/08, FN-07 |
| FN-07 | `bulkApproveReject` | orchestrate กลุ่ม · skip non-waiting · shared reject reason · partial | FN-06,10 | API-09 |
| FN-08 | `deleteContract` | ลบ + attachments + audit · (soft OQ-CT4) | FN-10 | API-11 |
| FN-10 | `recordContractHistory` | append-only audit (create/approve/reject/delete + bulk + license write) | — | FN-01/03/06/07/08/12 |
| FN-11 | `resolveContractItems` ⭐ | read quota + plots(verified) + crops(verified, license≠contracted) + aggregate tons | ENG-EXT-AGM | FN-01, API-13/14 |
| FN-12 | `writeCropLicense` ⭐ cross-module WRITE | PATCH crop.license_status (contracted/none) + sync external | ENG-EXT-AGM | FN-01(contracted), FN-06(reject→none) |

## §3.2 Engines
- **ENG-EXT-AGM** `agm-chain-connector` [NEW] ⭐ — (read) quota/plot/crop verified + (write) crop.license_status · wrap F-AGM-002/003/004 API · **มี write-back** (ต่างจาก Crop/Plot read-only) · used FN-11/12
- **ENG-EXT-01** `csv-import-framework` / export [EXISTING]

## §3.3 API ↔ Logic Trace (R8)
| API | Functions | Engines |
|---|---|---|
| API-01 | FN-05 | — |
| API-02 | FN-01,04,11,12,10 | AGM |
| API-05 | FN-03,04,10 | AGM |
| API-07 | FN-06,10 | — |
| API-08 | FN-06,12,10 | AGM |
| API-09 | FN-07(→06,12),10 | AGM |
| API-11 | FN-08,10 | — |
| API-13 | FN-11 | AGM |
| API-14 | FN-11 | AGM |
> mutation (02/05/07/08/09/11) มี ≥1 FN + FN-10 ✅ · **write-back FN-12** (create contracted / reject none) ✅

## §3.5 Locked Decisions
- LOCK-03: build-path FN-11 (read quota/plots/crops verified)
- LOCK-07: FN-12 write crop license (contracted/none) + sync
- LOCK-08: FN-04 กัน crop license=contracted เลือกซ้ำ
- LOCK-10: optimistic + idempotency + FN-10 audit
