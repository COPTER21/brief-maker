# HTML UI Brief — F-CUST-CL-001 Customer Credit Limit

## 0. Document control
| Item | Value |
|---|---|
| HTML source | `01_HTML/f-credit-limit.html` |
| FRD pair | `FRD_Pack/` |
| UI status | AS-BUILT; PM/BA approved prototype |
| Route | `#/credit-limits` |

## 1. Design tokens AS-BUILT

Anchor: `:root` (HTML lines 13–14). Typography variables range `--fs-11` to `--fs-20`; semantic colors use `--c-*`; shell sizes use `--sidebar-w` and `--shell-h`. Use the source file, not this document, as authority for token values.

| z token | Layer / anchor |
|---|---|
| `--z-toast:80` | `.toast-wrap` |
| `--z-modal:60` | `.modal-backdrop`, `.dd-panel` |
| `--z-drawer:51` | `.drawer` |
| `--z-backdrop:50` | `.drawer-backdrop` |
| `--z-dropdown:30` | `.topbar`, portal dropdown |
| `--z-shell:20` | `.sidebar` |
| `--z-sticky:10` | sticky support layer |

## 2. Route map

| Route | Default / behavior | Anchor |
|---|---|---|
| `#/credit-limits` | default route; closing drawer replaces history to this route | `DOMContentLoaded`, `hashchange`, `closeDrawer()` |

Only one hash route exists. Detail/change/confirm are overlays, not routes.

## 3. Layout shell

Fixed sidebar (`.sidebar`) and sticky `.topbar` contain the list workspace. `#page-content .page-fill` is replaced by `renderListOnly()` without losing `#credit-search` focus/caret. The table is inside its own panel; filters are not wrapped in an extra border container.

## 4. Page anatomy

### P-01 List

`#page-content` → head bar → list body → `#credit-search`, filter controls, sortable table, empty result. Row action opens detail via `openDrawer(...)` / `renderDrawer()`.

### P-02 Detail drawer

`.drawer-backdrop` + `#tdrawer.drawer` → header/customer state → tab bar → overview / AR / audit / `สายอนุมัติ (DOA)` → state-specific footer. Anchor functions: `renderDrawer()`, `acctState()`, `creditState()`.

### P-03 Change drawer

Change mode inside `#tdrawer`; numeric requested limit and reason feed `refreshChgFoot()`. `submitChange()` creates draft; `sendForApproval(id)` moves it to pending.

### P-04 Confirmation modal

`#modalBackdrop.modal-backdrop` / `#modalCard.modal` is reused for reject, hold, unhold. `renderModal()` provides exact contextual copy and disabled confirmation until reason is present.

## 5. Component inventory

| Component | Anchor | States actually rendered |
|---|---|---|
| Account pill | `acctState(c)` | `รอส่งอนุมัติ`, `รออนุมัติ`, `ระงับเครดิต`, `ปกติ` |
| Credit utilization | `creditState(c)`, `creditPct(c)` | normal, near-full, over, cash |
| Request submit | change footer / `refreshChgFoot()` | visually disabled/valid; no loading/error state in prototype |
| Approval timeline | `.appr-tl`, `.appr-step`, `.appr-dot`, `.appr-person` | pass, current, waiting, rejected; line segment ends between dots |
| Search | `#credit-search`, `renderListOnly()` | focused sequential typing retained; empty result |
| Reason textarea | `#rej-go`, `#hold-go` | confirm disabled until trimmed value; placeholder is in §9 |

Hover/focus visual details follow source CSS; loading state is not present in the prototype.

## 6. Overlay registry

| Overlay | Open | Close / dismiss | z | Anchor |
|---|---|---|---:|---|
| Detail/change drawer | row/action | Esc, backdrop, close; change closes to view according to handler | 51 | `.drawer`, `closeDrawer()` |
| Reject modal | `openReject(id)` | Esc, backdrop, cancel | 60 | `#modalBackdrop`, `closeModal()` |
| Hold/unhold modal | `openHold(id)` | Esc, backdrop, cancel | 60 | `renderModal()` |
| Toast | `showToast(msg,kind)` | auto removes after handler timeout | 80 | `#toastWrap` |
| Dropdown portal | combobox behavior | click choice / outside behavior in source | 30 | `.dd-panel.is-portal` |
| Map tooltip | map hover behavior | pointer-events none; disappears with its source interaction | 20 | `.map-tip` |

## 7. Interaction spec

- Esc chain is exact: `state.modal.open` → close modal; otherwise drawer/change logic → `closeDrawer()` (keydown handler, HTML line 1080).
- `submitChange()` validates a resolved tier and shows `วงเงินเกินเพดานที่ DOA ตั้งไว้ — ตั้งช่วงเพิ่มที่หน้า DOA` on failure.
- `sendForApproval()` is a distinct action after draft: it changes status to pending and shows `ส่งอนุมัติแล้ว — รออนุมัติขั้น 1`.
- Search uses `renderListOnly()` which captures active focus and selection then restores both after DOM replacement.
- History/hash close behavior is in `hashchange` and `closeDrawer()`.

## 8. State-driven UI matrix

| State | Pill | Available footer/action | Source |
|---|---|---|---|
| draft | `รอส่งอนุมัติ` | `ส่งอนุมัติ` when validation passes | `acctState`, `sendForApproval` |
| pending_approval | `รออนุมัติ` | approve/reject only to authorized current signer in production | `approveStep`, `openReject` |
| approved | no pending request | revised profile reflects new limit | `approveStep` |
| rejected | request closed | current limit remains | `confirmReject` |
| hold | `ระงับเครดิต` | `ปลดระงับเครดิต` | `confirmHold` |
| cash | `เงินสด` | change request can set first credit limit | `creditState` |

## 9. Microcopy (verbatim)

| Context | Text |
|---|---|
| draft toast | `บันทึกคำขอแล้ว — พร้อมส่งอนุมัติ` |
| send toast | `ส่งอนุมัติแล้ว — รออนุมัติขั้น 1` |
| final approval toast | `อนุมัติครบสาย — วงเงินใหม่ {amount} บาท` |
| reject toast | `บันทึกไม่อนุมัติแล้ว — วงเงินคงเดิม` |
| review toast | `บันทึกการทบทวนเครดิตแล้ว` |
| reject placeholder | `เช่น ประวัติชำระล่าช้า / เกินนโยบายความเสี่ยง` |
| hold placeholder | `เช่น ค้างชำระเกินกำหนด 2 งวด` |
| unhold placeholder | `เช่น เคลียร์ยอดค้างครบแล้ว` |

## 10. Data binding & backend anchors

`CREDITS` and transaction arrays are mock data. `DOA_APPROVER_DIRECTORY` is explicitly a mock resolved display payload: production resolves `doa_entry_ref`/role steps from DOA and names/identity from My Profile. Pair frontend actions with API-01..10 in `FRD_Pack/02_API.md`; never bind the mock tier logic as backend policy.

## 11. Traceability & drift log

| Brief | FRD | HTML anchor |
|---|---|---|
| list/search/filter | 01_UI P-01; API-01 | `renderListOnly()`, `#credit-search` |
| change draft/send | API-03/API-04; Rules BR-DOA | `submitChange()`, `sendForApproval()` |
| approval/reject | API-05/API-06 | `approveStep()`, `openReject()` |
| hold/unhold/review | API-07..09 | `openHold()`, `reviewCredit()` |
| timeline | 01_UI P-02 | `.appr-tl`, `.appr-dot`, `.appr-person` |

Drift: none found in supported UI behavior. The HTML mock shows all approver actions for flow demonstration; FRD requires server-side current-role authorization in production.

## 12. Diff from previous version

No prior approved HTML version was supplied. The current AS-BUILT includes the PM/BA-confirmed `draft → pending_approval` distinction and corrected approval-timeline segment geometry.

## 13. 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)

— ไม่มีข้อเสนอเพิ่มเติม; this brief intentionally records the approved prototype only.
