# UI Brief · F-WH-QHOLD กักคุณภาพ
2026-09-14 · source: frozen QHold authored shell/overlay, BRD §14, FRD 01_UI, RIF and PREBRIEF. HTML SHA in `_lane/HTML_FREEZE_SHA256.txt`. This brief documents the current artifact and production design; visual render NOT-CHECKED.

## 1. Intent
Warehouse maker identifies an existing stock slice and requests a partial quarantine/release. Reviewer reads pending/history and DOA decides externally. Held and pending held stay onHand but leave ATP; pending release never frees ATP. No wizard, sale/transfer, GRN posting or stock adjustment.

## 2. Information architecture
ERP shell Warehouse module. Tabs directly below page-head: รายการกัก `#/records`, รออนุมัติ `#/history`, ประวัติ `#/settings`. Top-right page-head action เพิ่มการกัก on list; export only where shown. All list tabs use canonical `.toolbar>.search-box` plus status filter, data-derived footer. No hint/banner. No extra parent navigation.

## 3. Screen 1 — รายการกัก
Columns: สินค้า, คลัง, ล็อต/ตำแหน่ง, On-hand, กักมีผล, รอกัก, ATP, สถานะ. Four stats from current slices: ตำแหน่งสินค้า, กักมีผล, รอกัก, ATP พร้อมใช้. Search and status filter operate on visible rows. Empty result has explicit empty state. Click row opens view drawer, with onHand/reservedSales/activeHeld/pendingHeld/ATP/holdable/releasable.

## 4. Request drawer
Open by เพิ่มการกัก or row ขอกัก/ขอปล่อยกัก. Searchable picker selects an existing Item/Warehouse/lot/location slice snapshot. Enter จำนวน, ที่มา (`พบปัญหาภายหลัง` or `ตรวจรับ GRN QC`), อ้างอิงต้นทาง, เหตุผล. GRN QC requires a mock source reference; later issue permits null source. Quantity finite positive and Item/UoM precision, never exceeds holdable/releasable. Save becomes `requested`; cancel leaves stock/request/event unchanged. Inline errors remain in drawer and do not close it.

## 5. DOA real-person slot picker
Selecting slice and amount loads effective policy for action/warehouse/qty. Required slots `ผู้ตรวจคุณภาพ` and `ผู้รับรองคลัง` are fixture examples only; production policy may differ. Each searchable person choice displays initials avatar, actual name, position and department. Missing/ineligible people block submission. Selected person references and display snapshots persist on request. Do not substitute role codes or hardcode managerial hierarchy.

## 6. Screen 2 — รออนุมัติ
Pending queue columns request, kind, item/lot, qty, selected people, time, status. Click request shows qty/refs/people and read-only state. Production user waits for external DOA event. Local orange DEMO action can simulate approve/reject for testing only; it is not an authorization path.

## 7. Screen 3 — ประวัติ
Append-only rows: event, request, item/lot, qty, source, time, status. Event drawer shows actor/time/source. No edit/delete. Search may narrow by request/source; audit must remain scoped to tenant/warehouse in production.

## 8. Availability check
Slice view drawer has ตรวจจำนวนขาย/ย้ายที่ใช้ได้. Enter qty and read allowed/denied plus available. For fixture held30/onHand100/reserved10, available60: qty61 denied, qty60 contract-valid. This does not create sale/transfer or change ledger/balance.

## 9. States and copy
`requested` hold: รอกัก grows, ATP falls, active held unchanged. Approved hold: pending→active, ATP unchanged. Rejected hold: pending clears, ATP restores. Requested release: pending release reserves active held, ATP unchanged. Approved release: active held falls once, ATP grows once. Rejected release: pending reservation clears, active held/ATP unchanged. Success toast `ส่งคำขอรออนุมัติแล้ว`; DEMO decision toast identifies simulation. Never say a live DOA approval happened.

## 10. Design system
v9 red/orange ERP shell and shared spacing, typography, drawer/table components. DEMO chip orange, visible next to simulated policy/decision controls. Canonical toolbar filter copied, not custom class. Tabs under header, action top-right. Large list scrolls horizontally; specific responsive/visual behavior still requires browser inspection.

## 11. Demo-only elements
`data-demo="doa-policy"` policy/person fixture and `data-demo="doa-decision"` simulated decision buttons, each with visible DEMO badge. They are harness controls, documented in FRD 01_UI. Production UI/API cannot call adapter-only decision endpoint from a user session. No persona switcher.

## 12. Accessibility and errors
Inputs have visible labels; picker must be keyboard searchable and report no match; errors adjacent to invalid action, focus restoration after drawer. Screen reader, keyboard-only, 1280px/narrow viewport and print views are NOT-CHECKED because browser/capture unavailable. Production must test these before release. Ref/policy unavailable must not silently submit.

## 13. Handoff and validation
Developer starts from FRD 00–08; preserve QHold `qhRequest`/`qhDecide` behavior, move concurrency and access control server-side, wire DOA/Inventory/NC/CSQ only after owner-reviewed contract. QA uses 45-case Markdown and exact QA HTML; 14 sys/mock cases need a harness. Isolated arithmetic/decision test 13/13 and static v9 audit FAIL0; no claim of actual browser or downstream pass. `[ASSUMED]` pending hold timing owner Warehouse Product Owner, DOA policy/SoD owner DOA/Security, UoM owner Inventory/Item.
