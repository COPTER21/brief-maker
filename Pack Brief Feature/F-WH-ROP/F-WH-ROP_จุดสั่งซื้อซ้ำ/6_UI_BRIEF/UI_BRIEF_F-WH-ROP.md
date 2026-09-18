# UI Brief · F-WH-ROP จุดสั่งซื้อซ้ำ

## 0. Control and source pairing
**AS-BUILT source:** `1_HTML/F-WH-ROP.html` at `_lane/HTML_FREEZE_SHA256.txt` (final after S3 rerun); anchors below derive from authored `_lane_tools/build.py` shell and `_lane_tools/rop_inject.js` injected domain code without rereading generated HTML. **Pair:** FRD 01_UI, 02_API, 03_LOGIC, 05_RULES. Visual rendering NOT-CHECKED (Playwright unavailable); this is a source/behavior extraction, not screenshot certification.

## 1. Tokens and layer map
CSS `:root`: `--bg #FAF8F5`, `--ink #111111`, `--muted #73757B`, `--line #DEDAD4`, `--red #FF3B30`, `--orange #FF9A1F`, `--white #FFFFFF`, `--good #157A41`. Font stack in `HTML_CSS`: Satoshi, Noto Sans Thai, sans-serif. Layer order: `.combo-menu` `--z-dropdown:10` (absolute within `.field`); `.backdrop` `--z-backdrop:50` fixed; `.drawer` `--z-drawer:60` fixed right; `.toast` `--z-toast:70` fixed lower right. Scroll: `.table-wrap` overflow auto, sticky `.tbl th`; `.dw-body` overflow auto. No custom per-feature palette token.

## 2. Route map
`route()` reads `location.hash`, defaults to `#/records`, and only accepts `records`, `history`, `settings`; unknown route falls back to records. `hashchange` re-renders. `tabs()` maps these to **นโยบายเติมสินค้า**, **คำแนะนำเติม**, **ประวัติ** directly below `.page-head`. A tab change does not post any transaction. `render()` keeps `#mainPanel` visible and `#secondaryPanel` hidden on each route.

## 3. Shell
`.sidebar` Warehouse navigation, `.topbar` sample user, `.content`, `.page-head` heading and `.ph-actions`, then `.tabs`, `#stats`, `#mainPanel`. The right side of page-head holds route actions: `เพิ่มนโยบาย` on records; `ตรวจคู่สินค้า×คลัง` and `คำนวณใหม่` on history; export on records/settings. No page-head tab controls on right. Stats are derived in `stats()` from `ropLatestPolicies`, `ropSuggestions` and `ropEvents`.

## 4. Page anatomy
| Route | Regions and anchors | Behavior |
|---|---|---|
| `#/records` | `#mainPanel .toolbar>.search-box`, `#thead/#tbody`, `#tableFoot`, `.ph-actions` | `ropRows` maps latest policy per pair; rows open `openView`, drawer shows policy/version and `ropEditSelected`; create/edit uses `ropOpenPolicy` |
| `#/history` | same list shell and filters; `.ph-actions` recompute/check | `ropSuggestions` derives availability/min/max/qty; row opens suggestion drawer, PR/NC buttons conditional; `ropOpenCheck` shows missing policy explicitly |
| `#/settings` | same list shell and filters | `ropEvents` append-only rows; `openView` shows event ref/time and historical policy version/date when `policy.saved` |

All three lists use `fillFilters` and `renderTableOnly`; search spans rendered row values, type/status filters derive from current rows, header click toggles sort, footer shows visible/total, `#empty` shows filtered empty state. No invented totals.

## 5. Component inventory and states
| Component | Anchor / handler | Present states |
|---|---|---|
| policy master picker | `#ropItem`, `#ropWarehouse`, `.combo-menu`, `.combo-option`, `ropFilterPicker`, `ropChoosePicker` | closed/focus open/filtered/selected; outside click closes; no async loading shown |
| policy inputs | `#ropMin/#ropMax/#ropSafety/#ropEffective/#ropNcRule`, `ropSaveFromDrawer`, `ropValidate` | blank/valid/error, HTML date input, disabled state none |
| suggestion row | `ropEvaluatePair`, `ropRows`, `openView` | below/equal/above; positive qty PR button; NC button when ruleRef; missing pair check |
| status pill | `.pill`, `.pill.pending`, `renderTableOnly` | **มีผล** vs **รอมีผล**; no other policy state |
| list | `#thead/#tbody/#empty/#tableFoot`, `renderTableOnly` | loaded, filtered, empty; no loader in local synchronous demo |
| toast | `#toast`, `toast()` | message shown then hides after 2600ms |

## 6. Overlay registry
| Overlay | Anchor / positioning | Open/close rules |
|---|---|---|
| drawer | `#drawer`, `.drawer`, `showDrawer`, `closeDrawer`; fixed right, width min(920px,100vw) | opens policy/check/view; close button, Cancel, backdrop and Esc close; no unsaved-change prompt in demo |
| backdrop | `#backdrop`, `.backdrop` fixed | click closes drawer |
| picker menu | `.combo-menu` absolute in `.field` | input/focus filters; option selection closes; document outside-click closes; no backdrop |
| toast | `#toast` fixed | `toast()` times out, no manual dismiss |

No modal/stepper/Pattern Q overlay exists. DOM `document.addEventListener('keydown')` handles Esc only when drawer open; picker outside-click document handler is in `rop_inject.js`. No multi-overlay Esc chain, drag or scroll lock is implemented. `showDrawer` focuses first editable input after a short timeout; focus restoration to opener is not present.

## 7. Interaction sequence
`ropOpenPolicy` builds the create/edit drawer. `ropSaveFromDrawer` rejects blank numeric cells before Number conversion; `ropValidate` enforces finite ordered nonnegative numeric values and real calendar date; `ropSavePolicy` validates scoped master codes, appends version and `policy.saved` event. Cancel/close does not save. `ropRecompute` derives current suggestions and appends one evaluation event per pair/version/snapshot key. `ropOpenCheck` + `ropCheckPair` exposes NO_POLICY or missing stock without inventing threshold. In suggestion drawer, `ropSendPR` displays a mock ack/replay/error; `ropSendNC` displays candidate rule ref and expressly says it is not delivery.

## 8. State-driven UI matrix
| Data condition | List/drawer text | Action |
|---|---|---|
| current policy | **มีผล** | view/edit version |
| future policy | **รอมีผล** | view/edit creates another version |
| available<min | **ต่ำกว่าจุด**, positive qty | PR mock, NC candidate if ruleRef |
| available=min | **เท่าจุด**, positive qty `[ASSUMED]` | PR mock, NC candidate if ruleRef |
| available>min | **สูงกว่าจุด**, qty0 | no PR; NC candidate if ruleRef |
| no policy | **ยังไม่มีนโยบาย** | no recommendation |
| no snapshot | **ไม่มีข้อมูลคงเหลือ** | no recommendation |
| mock PR unavailable | **ปลายทาง PR ยังไม่พร้อม** | no ack |
| replay | **รายการนี้ส่งแล้ว** / **คำขอเดิม** | same local ack/event |

## 9. Microcopy (verbatim from authored source)
Buttons/labels: **เพิ่มนโยบาย**, **แก้นโยบาย**, **บันทึก**, **ยกเลิก**, **ตรวจคู่สินค้า×คลัง**, **ตรวจนโยบาย**, **คำนวณใหม่**, **แนะนำเปิด PR**, **ส่งตัวเลือกให้กฎ NC**, **ขั้นต่ำ**, **สูงสุด**, **Stock ปลอดภัย**, **วันที่เริ่มใช้**, **กฎแจ้งเตือน NC**. Messages: **กรอกตัวเลขให้ครบ**, **ต้องเป็น 0 ≤ safety ≤ min ≤ max**, **กรอกวันที่เริ่มใช้**, **เลือกสินค้าและคลังจากรายการ**, **บันทึกนโยบายแล้ว**, **คำนวณใหม่แล้ว**, **ยังไม่มีนโยบาย**, **ไม่มีข้อมูลคงเหลือ**, **ปลายทาง PR ยังไม่พร้อม**, **ไม่ใช่ผลการแจ้งเตือน**, **ไม่พบรายการที่ตรงกับตัวกรอง**. Dynamic mock refs and quantities must come from data, not fixed copy.

## 10. Data binding / backend anchors
`ropItems`/`ropWarehouses` fixtures → proposed API-07 master options. `ropPolicies`/`ropSavePolicy`/`ropPolicyActive` → API-01/02 and FN-01–03. `ropSnapshots`/`ropEvaluatePair`/`ropSuggestions` → API-03 and FN-04/05. `ropPreparePR` → API-04/FN-06 mock; `ropNcCandidate` → API-05/FN-07 mock; `ropEvents` → API-06/FN-08. `ropRows`/`renderTableOnly` → FN-09 UI. Local demo uses in-memory state and `Date()`; production service must enforce tenant access, decimal, optimistic version, snapshot freshness and durable idempotency independently.

## 11. Traceability and drift
| Brief | FRD | HTML/source anchor |
|---|---|---|
| §2–4 routes/shell | 01_UI; BRD §14 | `route`, `tabs`, `.page-head`, `render` |
| §5–7 policy | API-01/02; FN-01–03; R-01–03 | `ropOpenPolicy`, `ropSaveFromDrawer`, `ropSavePolicy` |
| §8 suggestion | API-03; FN-04/05; R-04/05 | `ropEvaluatePair`, `ropSuggestions`, `openView` |
| §8 mock | API-04/05; FN-06/07; R-06–08 | `ropPreparePR`, `ropNcCandidate`, `ropSendPR/NC` |
| §4 history | API-06; FN-08 | `ropEvents`, `ropRows`, `openView` |

**Drift log:** no route/visible action mismatch after S3 correction and first FRD authoring. FRD production requirements (server permission, decimal persistence, stale snapshot, CSQ/NTF emit) are FRD-only by design and NOT-CHECKED locally; they are not hidden HTML features. The pre-document strict calendar-date patch and rerun are recorded in `_lane/HTML_DRIFT_SYNC.md`. Mock/soft-link boundaries retained.

## 12. Diff from prior version
No prior delivered UI Brief. One pre-document HTML revision tightened date validation; current hash is authoritative. No post-FRD HTML mutation.

## 13. Demo-only elements and proposals
The topbar text **ผู้ใช้งานตัวอย่าง** with **DEMO** badge is sample identity only; no persona switcher exists and it never changes data or permission. No other demo-only control is used. Proposal (not AS-BUILT): before production, add visible snapshot freshness and access-denied states only after owner decision and a new HTML/FRD sync cycle. Do not treat this proposal as implemented scope.
