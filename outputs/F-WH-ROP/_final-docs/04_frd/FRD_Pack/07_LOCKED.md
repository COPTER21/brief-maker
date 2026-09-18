# 07 LOCKED DECISIONS · F-WH-ROP

| Lock | Decision |
|---|---|
| LOCK-01 | policy granularity is Item×Warehouse, not bin |
| LOCK-02 | ATP is F009 final value; hold/reserved never subtracted again |
| LOCK-03 | ROP and qty formulas match approved HTML (§03 FN-04) |
| LOCK-04 | daily 06:00 and movement triggers are production anchors; UI button is manual |
| LOCK-05 | PR is real F072 Draft, grouped per warehouse/run, never auto-submitted |
| LOCK-06 | vendor does not split Draft; final selection happens downstream |
| LOCK-07 | NTF event is `reorder_point.triggered` and central service owns delivery |
| LOCK-08 | CSQ declares only `master.changed` to SecC; threshold and PR candidates are excluded |
| LOCK-09 | F072 owns PR lifecycle; origin refs preserve ROP traceability |
| LOCK-10 | no DOA/DOCCFG declaration or printable output for F085 |
