# FUNCTION_CHECKLIST · F-WH-QHOLD

`WF` source/HTML behavior at S3; `DEV` production contract and `QA` execution remain open. A check is not proof of live DOA/GRN/NC/CSQ. Each FN maps to S and BR for gate/TC.

| FN | Capability / observable result | Trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-01 | list/search/filter stock slices, held/ATP stats from data | S-01,S-10 / BR-03 | [ ] | [ ] | [ ] |
| FN-02 | select Item/Warehouse/location/lot soft refs, origin/reason/source | S-01,S-07 / BR-01 | [ ] | [ ] | [ ] |
| FN-03 | load DOA policy required slots and eligible actual people; validate choices | S-01,S-09 / BR-02 | [ ] | [ ] | [ ] |
| FN-04 | request partial hold with validation/pending quarantine | S-01,S-07 / BR-03,05,06 | [ ] | [ ] | [ ] |
| FN-05 | approve/reject hold via external mock event/idempotency | S-02,S-03 / BR-04,07 | [ ] | [ ] | [ ] |
| FN-06 | request partial release; reserve held without freeing ATP | S-04,S-05,S-06,S-08 / BR-05,06 | [ ] | [ ] | [ ] |
| FN-07 | approve/reject release via external mock event/idempotency | S-04,S-05,S-08 / BR-04,07 | [ ] | [ ] | [ ] |
| FN-08 | guard concurrent/stale/duplicate request and decision | S-02,S-06,S-08,S-09 / BR-05,07 | [ ] | [ ] | [ ] |
| FN-09 | read pending queue/history append-only, distinct source refs | S-02..S-10 / BR-04,08 | [ ] | [ ] | [ ] |
| FN-10 | validate sell/transfer availability contract only, no transaction | S-10 / BR-03,08 | [ ] | [ ] | [ ] |
