# PREBRIEF · Cycle Count + ABC
## Defaults/OQ
OQ-ABC-01 default monetary VALUE cumulative70/20/10, cadence A1/B3/C6 months. W4 §2 value×frequency capability is optional policy basis `[ASSUMED]` because it conflicts with §3 monetary default; owner Warehouse Product Owner. ABC class uses cumulative share **before** item, indivisible items may overshoot; ties stable itemCode. Frequency may prioritize due items within class. OQ-ST-02 absent in source: blind count `[ASSUMED]` counter server projection excludes expected/value/variance even after submission; reviewer unlocks comparison only after submitted. Month-end clamp, 90-day frequency window and no auto-recount threshold `[ASSUMED]` owner Warehouse Product Owner.

| S | Trigger/data | Observable result |
|---|---|---|
| S-01 | values40,30,20,10 default | A,A,B,C; shares40/30/20/10; counts2/1/1 |
| S-02 | X value100 freq1, Y value50 freq4 | default X before Y; optional weighted basis Y score200 before X100; previous policy/plan snapshot intact |
| S-03 | tie scores30,30,20,20 codes01–04 | A,A,A,B; actual A80%,B20%,C0; stable repeat |
| S-04 | total value0, config40/40/20, invalid70/25/10 | all C without NaN; changed config can reclassify40,30,20,10 to A,B,B,C; invalid sum rejected |
| S-05 | last accepted review Jan31 2026 | A due Feb28, B Apr30, C Jul31; existing plan due unchanged on new policy |
| S-06 | assigned counter expected12, blank/zero | expected/value/variance absent in counter UI/API/export; blank blocked, zero accepted; reviewer sees delta−12 after submit |
| S-07 | expected100 counted100 | submit creates no StockAdj; reviewer accept reason closes zero delta; onHand100 unchanged |
| S-08 | expected100 counted104 | reviewer sees +4; dispatch disabled before review; accept+reason then one mock StockAdj payload/ack, onHand100/movement unchanged |
| S-09 | first97, reviewer recount, second99 | old attempt locked, new counter form blank/blind; reviewer accepts latest delta−1, payload uses 99 not97 |
| S-10 | conversion 1box=12pcs snapshot, expected24pcs,count3box | reviewer sees36pcs/+12; later conversion to10 does not rewrite; duplicate dispatch same ref, unassigned user denied by production contract |

No actual W3 Stock Adjustment adjustment, approval or posting is in scope. Every screen console/master. User-access and movement persistence require production verification; HTML fixture is not security proof.
