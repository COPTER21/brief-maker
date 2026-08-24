# 06_TESTS — F-WH-DN Delivery Note

## §6.1 Acceptance matrix

| AT | Scenario | Expected visible/system outcome | Trace |
|---|---|---|---|
| AT-01 | open `#/list` | tabs “รอออกใบส่งของ” / “ใบส่งของ” and eligible packs | US-01, BR-01 |
| AT-02 | select compatible packs | “ออกใบส่งของ” available; summary totals correct | BR-02 |
| AT-03 | select incompatible pack | incompatible row disabled/confirm blocked | EC-01 |
| AT-04 | confirm reference create | draft created, packs leave queue, no GI | BR-03 |
| AT-05 | assignee search “วิภาวี” | employee result only; no manual option | BR-20 |
| AT-06 | vehicle search “1123” | matching plate; can select | US-02 |
| AT-07 | choose “กรอกเลขรถเอง” blank/save | validation then saved plate | BR-20 |
| AT-08 | driver search name/phone | matching driver result | US-02 |
| AT-09 | choose “กรอกคนขนส่งเอง” | first/last/phone required and preserved | BR-20 |
| AT-10 | over-capacity vehicle | warning visible, flow remains allowed | BR-05 |
| AT-11 | mark ready missing required | inline errors; status unchanged | BR-04 |
| AT-12 | dispatch 3PL without tracking | “กรอกเลขติดตามพัสดุก่อนส่งมอบขนส่ง” | BR-06 |
| AT-13 | dispatch valid reference | in transit + GI/source/audit/outbox once | BR-08 |
| AT-14 | update tracking | next stage only; notification event queued | BR-07 |
| AT-15 | first failed delivery | UI/history says “ครั้งที่ 1” | BR-12, EC-03 |
| AT-16 | reschedule failed | status ready; attempts preserved | lifecycle |
| AT-17 | POD blank receiver | “ระบุชื่อผู้รับสินค้า” | BR-09 |
| AT-18 | rejected qty no reason | blocked at affected line | BR-09 |
| AT-19 | POD full accept | delivered; shipped/source result and audit correct | BR-10/11 |
| AT-20 | POD partial | partial; return_in; backorder/close-short choice | BR-10/11 |
| AT-21 | return all from failed | reason required; reverse GI; packs back queue | BR-13 |
| AT-22 | cancel before dispatch | no reverse; packs back queue | BR-13 |
| AT-23 | cancel after dispatch | reverse succeeds before packs return | BR-13 |
| AT-24 | sales source transition | SO issued/shipped/returned/status recalculated | BR-14 |
| AT-25 | partial choose backorder | retry work event once | FN-14 |
| AT-26 | partial choose close-short | SO/AR event once, no automatic Credit Note | OOS |
| AT-27 | duplicate destructive retry | no duplicate reverse/queue/event | EC-11 |
| AT-28 | select `PACK-2026-0460 / TR-2026-0012` | header/list shows `WH-01 → WH-02` | US-06 |
| AT-29 | dispatch Transfer DN | transfer event + inventory movement; no SO write | BR-15 |
| AT-30 | return/cancel Transfer DN | transfer reversal contract; no SO write | XT-04 |
| AT-31 | click “สร้างแบบ Manual” | independent manual form opens | US-07 |
| AT-32 | create Manual DN | manual record/audit only; no pack/GI/source sync | BR-18 |
| AT-33 | Manual status blank reason | “กรุณาระบุเหตุผล”; unchanged | BR-19 |
| AT-34 | change Manual through several statuses | each state/reason appears in history | BR-19 |
| AT-35 | Manual choose in_transit/delivered | no automatic GI or source event | BR-18 |
| AT-36 | non-draft Reference drawer | delivery fields read-only per state | BR-16 |
| AT-37 | document tab before/after POD | checkbox before; accepted/rejected result after | A4 |
| AT-38 | history tab | append-only chronological events | BR-17 |
| AT-39 | refresh `#/view/...` prototype | route returns list and drawer is absent | EC-02 |
| AT-40 | unauthorized mutation | hidden/disabled UI and backend 403 | permissions |

## §6.2 Negative/permission

- mixed customer/address/source, already-bound pack, invalid phone, blank plate, non-employee assignee
- stale version, repeated idempotency key with different payload, wrong state, excessive rejected qty/media
- driver operates another assignee’s record; viewer calls mutation directly; cross-tenant ID
- Manual payload attempts source refs/GI flag; Transfer path attempts SO update

## §6.3 State and transaction assertions

Every transition asserts prior/new state, one audit event, expected outbox records, version increment and no partial side effects. Failed integration must roll back or leave committed state with retriable outbox exactly as defined in `03_LOGIC §3.4`.

## §6.7 Confirmed edge coverage

EC-01→AT-03; EC-02→AT-39; EC-03→AT-15; EC-04→AT-21; EC-05→AT-22/23; EC-06→AT-28..30; EC-07→AT-33; EC-08→AT-07/09; EC-09→AT-37.

## §6.8 AI-default engineering coverage

EC-10 concurrency→409/reload; EC-11 idempotency→AT-27; EC-12 inactive master→confirm/dispatch validation; EC-13 downstream/outbox retry; EC-14 injected partial movement failure→full rollback.

## §6.9 Cross-module tests

| XT | Test |
|---|---|
| XT-01 Packing | create binds once; return/cancel restores once; duplicate retries are safe |
| XT-02 Inventory | dispatch issue; partial return_in; return/cancel issue_reverse; reconciliation hash matches |
| XT-03 Sales | SO-only counters/status; partial/close-short/reversal recalculate correctly |
| XT-04 Transfer | from/to and transfer events; SO adapter is never invoked |
| XT-05 AR | delivered/partial/close-short emits billing request once; no automatic Credit Note |
| XT-06 Document | number comes from engine; immutable; snapshot policy read centrally |
| XT-07 Notification | declared business events include DN ref; failure queued; no hardcoded channel |

## §6.10 Microcopy note

Browser/UI tests use verbatim anchors from the approved HTML, including “ออกใบส่งของ”, “สร้างแบบ Manual”, “ยืนยันออกรถ · ตัดสต๊อก”, “อัปเดตสถานะ Manual”, “กรุณาระบุเหตุผล” and “ใบแพ็คกลับเข้าคิวรอออกใบส่งของ”.

## §6.11 DoD

- all 40 AT cases pass; every BR/EC/LOCK and XT has evidence
- API→Function/Engine trace has no orphan; data classification complete
- Reference/Manual isolation proven with integration spies/events
- A4 sample and browser prototype remain accessible with zero console errors

