# FUNCTION_CHECKLIST · F-WH-ROP

`WF` to be checked against actual HTML handlers at S3; `DEV`/`QA` remain implementation/release tasks.

| FN | Capability / result | Trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-01 | list/filter/sort Item×Warehouse policies and data-derived counts | S-01,S-06,S-08 / BR-01 | [x] | [ ] | [ ] |
| FN-02 | create/edit versioned Min/Max/Safety/Lead Time/ADU window/Pack Size policy; validate bounds | S-01,S-02,S-07 / BR-01,BR-02,BR-03 | [x] | [ ] | [ ] |
| FN-03 | resolve effective policy for exact Item×Warehouse/date | S-06,S-07,S-08 / BR-01,BR-02 | [x] | [ ] | [ ] |
| FN-04 | read ATP and movement history from F009, subtract On-Order, calculate ADU/Lead Time quantity and round to purchase Pack Size | S-03,S-04,S-05,S-09 / BR-04,BR-05 | [x] | [ ] | [ ] |
| FN-05 | show replenishment suggestions and empty/no-policy state | S-03..S-09 / BR-04 | [x] | [ ] | [ ] |
| FN-06 | emit `reorder_point.triggered` through Notification with idempotent replay | S-12 / BR-06 | [x] | [ ] | [ ] |
| FN-07 | automatically create one editable PR Draft per warehouse per evaluation round; never auto-submit to DOA | S-10,S-11 / BR-07,BR-08 | [x] | [ ] | [ ] |
| FN-08 | append policy/suggestion/notification/PR Draft events and read history without mutation | S-07,S-13 / BR-08 | [x] | [ ] | [ ] |
