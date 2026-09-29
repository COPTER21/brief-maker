# HTML UI Brief · F-WH-LOT · ล็อต-ซีเรียล

## 0. Document control
AS-BUILT of frozen `../1_HTML/F-WH-LOT.html`, paired with `../3_FRD/`; authored HTML source is `_lane_tools/build.py` plus `_lane_tools/lot_inject.js`. Browser visual render NOT-CHECKED. Console/master only.

## 1. Design tokens and z-index
| Anchor | AS-BUILT value |
|---|---|
| `:root` | `--bg:#FAF8F5`, `--ink:#111111`, `--muted:#73757B`, `--line:#DEDAD4`, `--red:#FF3B30`, `--orange:#FF9A1F`, `--white:#FFFFFF`, `--good:#157A41` |
| `html,body` | Satoshi, Noto Sans Thai fallback; scrollbar 5px |
| `.panel / .btn` | radius 10px / 8px |
| `--z-toast / --z-drawer / --z-backdrop / --z-dropdown` | 70 / 60 / 50 / 10; `.tbl th` local z=1 |

## 2. Route map
| Hash | Page and render anchor |
|---|---|
| `#/records` default/fallback | `route()` → `render()` → `#mainPanel`, `renderTableOnly()` |
| `#/history` | selected-lot movement trace `#secondaryPanel`, `lotTrace()` |
| `#/settings` | per-item policy/recommendation `#secondaryPanel`, `lotSaveSetting()`/`lotRecommend()` |
`hashchange` invokes `route()`; known hashes survive refresh in the client; unknown hash falls back to records.

## 3. Shell
`.app` horizontal flex; `.sidebar` 232px dark; `.topbar` 56px; `.content` padding 28px, 16px under 1024px, 12px under 767px. Sidebar compacts to 58px then hides under 767px. `.page-head` contains title left, `ส่งออก` and `สร้างรายการ` right; `.tabs` follows directly below; `.stats` follows tabs. `.topbar .demo` displays DEMO.

## 4. Page anatomy
| Page | Region → component | Handler |
|---|---|---|
| Records | `.page-head` → `.tabs` → `#stats` → `#mainPanel .toolbar > .search-box` + `#typeFilter`/`#statusFilter` → `.table-wrap .tbl` + `#empty` → `#tableFoot` | `tabs`, `stats`, `fillFilters`, `renderTableOnly` |
| History | `#secondaryPanel .page-section` → `#traceLot` → movement `.tbl` → `#movementDetail` or `.empty` | `lotSelect`, `lotTrace`, `lotShowMovement` |
| Settings | `#lotItemPick`/`#settingsMenu` → `#lotTracking`/`#lotExpiryFlag` → action buttons → `#lotRecommendation` | `lotFilterSettings`, `lotSettingsChoose`, `lotSaveSetting`, `lotRecommend`, `lotOpenNC` |
| Create drawer | `#drawerBody`: `#f1` item combobox, `#f0` lot, conditional `#f2` serial and `#f3` expiry; `#drawerFooter` | `openCreate`, `lotChooseItem`, `validate`, `saveRecord` |
| View drawer | `#drawerBody .kv` + selected identity `lotTrace()` | `openView`, `domainView` |

## 5. Component states
| Component | AS-BUILT states |
|---|---|
| `.tab` | muted default / `.is-active` red underline |
| `.toolbar > .search-box .input` | blank, focus red border, query filtered rows; `#typeFilter`/`#statusFilter` options built from current rows |
| `.tbl`, `#empty`, `#tableFoot` | sortable rows / empty state / visible and total count |
| `.pill` | green default; `.pending` orange when label contains `รอ`; LOT snapshot status `พร้อมใช้`, `กักอยู่`, `หมดอายุ` |
| `#settingsMenu`, `#lotMenu` | searchable item buttons; selection hides menu; create menu outside click closes |
| `#lotSerialWrap`, `#lotExpiryWrap` | selected item's tracking/expiry controls visibility; `#e0..#e3` field errors |
| `#saveBtn` | normal / disabled with `กำลังบันทึก…` for 300ms local save; validation keeps drawer open |
| `#lotRecommendation` | ranked candidate table / `ไม่มีล็อตที่พร้อมใช้`; no reserve action |
| `#movementDetail` | blank until movement click, then actual source/from/to/previous/next refs; read-only |
No pagination, server-loading state, config-audit list, or permission-controlled shell is implemented in prototype.

## 6. Overlay registry
| Overlay | Open/close | Position/z | Dismiss |
|---|---|---|---|
| `#drawer` + `#backdrop` | `showDrawer`/`closeDrawer` | fixed right width `min(920px,100vw)` z60/50 | close button, cancel, backdrop, Escape; no scroll lock |
| `#toast` | `toast(s)` | fixed bottom right z70 | auto-hides after 2600ms |
| `.combo-menu` | item input/search; option select | absolute within `.field`, z10 | selection; create-menu outside click |
No modal, nested drawer, drag/zoom, or PDF surface.

## 7. Interactions and keyboard
`route()` is hash-driven. `showDrawer()` focuses the first writable input after 30ms. Escape closes an open drawer; backdrop click also closes. `lotChooseItem()` resolves per-item config and toggles conditional fields. `validate()` writes `#e*` errors; failed save leaves data unchanged. Accepted `saveRecord()` appends identity and local audit event, with a local replay key. `lotSaveSetting()` updates selected item; `lotRecommend()` reads candidates without stock mutation. No keyboard scan capture here.

## 8. State-driven matrix
| Source state | UI result |
|---|---|
| `tracking=none` | create validation rejects |
| `tracking=lot`, `expiryEnabled=true` | `#f3` visible and required |
| `tracking=serial` | `#f2` visible/required; duplicate same-item serial rejected |
| expired, fully held, zero available | omitted by `eligibleLots()` |
| expiry-enabled item | expiry, receipt date, lot code order |
| non-expiry item | receipt date, lot code order |
| selected lot with/without movement | exact movement rows/detail or empty state |
| open/closed drawer | `open` classes on drawer/backdrop or absent |

## 9. Microcopy verbatim
Buttons/labels: `ส่งออก`, `สร้างรายการ`, `ล็อต`, `ซีเรียล`, `วันหมดอายุ`, `สินค้า`, `รูปแบบติดตาม`, `บังคับวันหมดอายุ`, `บันทึกการตั้งค่า`, `แนะนำล็อต`, `เปิดกฎแจ้งเตือน`, `บันทึก`, `ยกเลิก`, `ปิด`, `ทุกสถานะ`, `ทุกประเภท`.
Errors/toasts: `เลือกสินค้า`, `เปิดวันหมดอายุต้องติดตามล็อตหรือซีเรียล`, `กรอกรหัสล็อต`, `กรอกซีเรียล`, `กรอกวันหมดอายุ`, `ซีเรียลนี้ถูกใช้แล้ว`, `สินค้านี้ไม่ได้เปิดติดตามล็อตหรือซีเรียล`, `ตรวจสอบข้อมูลที่กรอก`, `รายการนี้ส่งแล้ว`, `บันทึกแล้ว`, `บันทึกการตั้งค่าแล้ว`, `กฎแจ้งเตือนเปิดในระบบกลาง`, `ส่งออกแล้ว`.
Empty/loading: `ไม่พบรายการที่ตรงกับตัวกรอง`, `ยังไม่มีการเคลื่อนไหวของล็อตนี้`, `ไม่มีล็อตที่พร้อมใช้`, `กำลังบันทึก…`.

## 10. Data binding and backend anchors
| Prototype | Production FRD |
|---|---|
| `lotItems`, `lotRows`, `state.rows` | API-01/02 identities; API-03 item policy; Item/Warehouse soft refs |
| `eligibleLots()` | API-04 read-only availability adapter; BR-04..06 |
| `lotMovements`, `lotTrace`, `lotShowMovement` | API-05 W3-LITE movement read mock, no posting |
| `state.history.unshift` | FN-07 append + API-06 audit read; prototype lacks config-audit list |
| `lotOpenNC()` toast | API-X2 NC external mock; no delivery |
| CSQ `master.changed` | declaration/prod adapter only; no 7C stamp in prototype |

## 11. Three-way trace and drift
| Brief | FRD | HTML |
|---|---|---|
| §4 Records/Create | P-01/P-04; API-01/02 | `#mainPanel`, `#drawer`, `saveRecord` |
| §4 History | P-02; API-05 | `#traceLot`, `lotTrace`, `lotShowMovement` |
| §4 Settings | P-03; API-03/04/X2 | `#lotItemPick`, `lotSaveSetting`, `lotRecommend`, `lotOpenNC` |
| §6 Audit read | API-06/FN-08 | FRD-only: no config-audit list in prototype |
Drift: FRD server role checks, effective/versioned policy, tenant scope, persistent idempotency, audit read, NC destination and CSQ event are production contracts. HTML is local demonstration; no browser visual verification.

## 12. Diff
Initial frozen issue. Generic S3 candidate was repaired before freeze with per-item settings, conditional fields, FEFO/FIFO ranking and selected movement refs. No postfreeze HTML edit.

## 13. ข้อเสนอ (ไม่ใช่ AS-BUILT)
Warehouse Product Owner should decide whether production needs visible config audit. UI QA must perform browser visual acceptance before release.

## Demo-only elements
`.topbar .demo` shows `DEMO` beside sample user; there is no persona switcher. Production identity/permissions come from central User Access.
