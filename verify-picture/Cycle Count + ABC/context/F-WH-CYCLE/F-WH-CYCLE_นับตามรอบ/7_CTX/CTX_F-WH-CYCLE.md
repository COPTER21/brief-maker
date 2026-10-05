# Developer Context Pack · F-WH-CYCLE นับตามรอบ
W4B FULL · AI100 no-vibe. Source FRD 00–08, BRD, frozen HTML and 47-case TC. Developer can start now.

Build order: Inventory value/frequency/UoM snapshots→effective ABC policy resolver by asOf/version/class→plan due/assigned counter→server-redacted blind API/export→immutable count attempts→review/recount→reviewed nonzero W3-LITE StockAdj mock outbox/idempotent ack→append-only history/CSQ owner review→UI and tests. Default monetary value70/20/10; optional weighted basis `[ASSUMED]`. 90-day frequency window, cumulative-before/tie/zero C/month-end `[ASSUMED]` Warehouse Product Owner. OQ-ST-02 exact detail absent: counter expected/value/variance must be absent server-side before and after submit/recount `[ASSUMED]`, owner Warehouse Product Owner.

FRD API-01–09 and data model in 04_DB are proposed production contracts, not implemented endpoints. Counter cannot force reviewer view or bypass via ABC value/export; RLS/assignment/reviewer authorization server-side. Latest accepted attempt alone gives delta=countedBase−expectedBase. StockAdj F082 W3-LITE returns mock acknowledgement/reference only; never actual adjustment approval/posting or stock movement change. CSQ draft candidate requires owner classification before registration. No DOA/NTF chip.

Evidence: isolated domain13/13, v9 static audit FAIL0/WARN2, FRD gate A–M, 47 exact QA cases with 17 sys/mock-only. Browser render/click/export/print, production data security, W3 and CSQ integration NOT-CHECKED. Frozen HTML SHA in gate evidence. Any HTML edit requires S3a–c and html-to-frd-sync. W3 mock payload owner StockAdj; Item/UoM source owner Inventory/Item; CSQ event/profile owner CSQ Engine.

Post-freeze correction: future Oct01 policy saved while current Sep14 list remains old; Sep20 plan uses old class A and Oct02 plan uses new class B (ITEM-102 fixture). SHA and drift report in gate evidence.
