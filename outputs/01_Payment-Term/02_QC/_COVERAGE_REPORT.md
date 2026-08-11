# Coverage Report · Payment Term (F-PAY)

> Skill: **qc-coverage-checker** · Round 1 (HTML prototype vs scope baseline)
> Target (source of truth): `outputs/01_Payment-Term/01_HTML/f-payterm.html` (1483 lines)
> Baseline (no `workflow_graph.json` for this feature — repo fallback convention):
> - Function Checklist `FUNCTION_CHECKLIST_F-PAY_Payment-Term.md` (FN-01..20, FN-26..29, FN-40, FN-90, FN-92)
> - PREBRIEF `PREBRIEF_F-PAY_Payment-Term.md` (BR-01..10, S-01..10, Edges §9, decided-OUT S-10/FN-40)
> - Central Plan `CENTRAL_PLAN_CORE_ERP.md` (Payment Terms → PO / AR Inv / AP Inv `[config]`)
> Date: 2026-08-10 · CHECK-ONLY (no HTML edits) · every ✓ cites HTML line evidence

---

## Verdict: **WARN**

No block-severity rule/edge/exception is uncovered — every FN has a real, wired UI hook and every block-rule fires in `submitTerm()`. WARN is raised for **1 source-contradiction (PR in `use_in`)** plus **2 minor UI gaps** (per-option type description; off-canvas sidebar has no reveal control). None are build defects that block dev.

**Counts**
- FN: **26 / 26** functional covered (FN-01 covered with a minor sub-gap) + FN-40 absence-check = clean 5/6, 1 tension
- BR: **10 / 10** reflected/enforced (BR-09 = absence, honored)
- Edges out: **4 / 4** in-scope groups covered/representable + 1 future edge (partner master) declared-not-built = NOT-CHECKED (out of this feature)
- Central Plan `[config]` edges: **3 / 3** representable via `use_in` (→ PO, → AR Inv, → AP Inv)
- Exception paths: **7 / 7** present
- Backend-only hooks: **3** noted (not UI gaps)

---

## 1. FN Coverage Matrix

| FN | Requirement | HTML | Evidence (line / selector / fn) |
|---|---|---|---|
| FN-01 | Type combobox 7 values, description per option, fields change by type | ⚠✓ | `PT_TYPES` 7 types L768–776; type `searchDropdown('type',...,'onTypeChange')` L1267; `onTypeChange` swaps fields L1071–1082. **Sub-gap:** `typeOpts` passes only `label` (L1156) — no 2-line desc in dropdown per §3.1 |
| FN-02 | Credit: N days (>0) + due basis 3 + trigger locked "ทันที" | ✓ | credit fields L1181–1185; `trigLock:true` L774 → lock badge L1164–1165; `DUE_BASIS` 3 values L810–814; net_days>0 validate L1117 |
| FN-03 | Credit early-pay discount (% + days), optional | ✓ | `discountFields` L1171–1173, help "optional", not required |
| FN-04 | Deposit method 3 (%/fixed/manual); manual → value empty | ✓ | `DEPOSIT_METHOD` L792; `onDepMethodPick` manual→`deposit_value=''` L1084; valField hidden when manual L1190 |
| FN-05 | Deposit remaining timing 3 + trigger default "หลังชำระมัดจำ" | ✓ | `REMAINING_TIMING` 3 L793; deposit `trigDefault:'after_deposit'` L771 (= หลังชำระมัดจำ L780) |
| FN-06 | Installment add/remove + % + due_type + desc, live % total (✓ at 100) | ✓ | `addInst` L1093, `removeInst` disabled ≤2 L1094/1212; live `onInstPct` L1095; `.inst-total is-ok/is-warn` L1226 |
| FN-07 | Partial: no fixed schedule, summary "จ่ายตามรับจริง" | ✓ | `termSummary` partial L921; partial fields L1198–1200 (per-round credit optional) |
| FN-08 | Direct: expense cat 3, no trigger, use_in AP Inv + PV | ✓ | `EXPENSE_CAT` 3 L795; `noTrigger:true` L775 → triggerField='' L1163; disables PR/PO/QUO/SO L1080/809; mock DIRECT-UTIL use_in `[ap_invoice,payment_voucher]` L832 |
| FN-09 | Prepay trigger "หลังชำระเต็มจำนวน"; Postpay N≥0 (0=immediate) | ✓ | full_prepay `trigDefault:'after_full'` L769; postpay net_days field "0 = ทันที" L1178 |
| FN-10 | use_in 8 docs grouped buy/sell, ≥1 | ✓ | `USE_IN_DOCS` 8 L798–807 grouped ฝั่งซื้อ/ฝั่งขาย; `useInChecks` L1237–1248; ≥1 validate L1119 |
| FN-11 | Status 3 values from create (default active) | ✓ | status `<select>` active/inactive/draft L1284–1288, default active |
| FN-12 | No field-help under fields (hint stripped) | ✓ | `fieldBlock` renders `${help?``:''}` — help arg discarded L1364 |
| FN-13 | Default 1-per-type (old drops) + block non-active + list star | ✓ | `toggleDefault` L1090; block if !active L1128; unset old default L1129; list star L1007 |
| FN-14 | code dup / name empty / use_in empty / credit ≤0 → block + toast | ✓ | `submitTerm` L1104–1119 |
| FN-15 | Deposit % 0 or >100 → block | ✓ | >100 L1115; >0 L1125 |
| FN-16 | Installment <2 or ≠100% → block; discount days ≥ net → block | ✓ | L1110–1112; discount L1121–1122 |
| FN-17 | Edit all fields even used>0 | ✓ | `openDrawer('edit')` L1055 + `submitTerm` edit L1130–1132; no used>0 lock (intentional, OQ-PAY-05) |
| FN-18 | View header status menu 3, all directions, current disabled | ✓ | status menu L1329–1331 (current `disabled`); `setStatusFromMenu` L1048 |
| FN-19 | Bulk bar set 3 statuses + deselect; selected rows highlighted | ✓ | bulkbar L958–965; `tr.is-sel` L575 + `renderRow` sel class L1005 |
| FN-20 | Bulk delete: confirm delete/skip count; used>0 skipped; btn disabled if none | ✓ | `bulkDoDelete` skip used>0 L1039–1045; modal count + `${delN?'':'disabled'}` L1372–1381 |
| FN-26 | Stat 4 cards filter + toggle-off; type filter combobox combined | ✓ | 4 `statBtn` L951–956; `quickFilter` toggle-off L1022–1026; `onFilterTypePick` L1049; combined filter L930–934 |
| FN-27 | Table in `.tbl-scroll`, sticky thead, card flush bottom (#96) | ✓ | `.tbl-scroll` sticky thead L65–66; content full-height L61–62; table wrapped L982 |
| FN-28 | Iron Rule #29 scroll preservation (3 layers) | ✓ | `_keepScroll` content/tbl-scroll/drawer-body L1425–1433; `render()` wraps L1435; `renderFormKeepScroll` L1062–1069 |
| FN-29 | 768–1180 sidebar off-canvas; CI Warm Light; Esc chain | ⚠✓ | media query sidebar translateX L68–74; Warm Light tokens L14–40; Esc chain sdd→modal→drawer L1456–1460. **Gap:** `.sidebar.is-open` style exists (L70) but **no button/JS toggles it** — off-canvas sidebar cannot be reopened on narrow viewport (`.nav-toggle` L67 is dead). Status/user menus not in Esc chain |
| FN-90 | Delete always via confirm | ✓ | `bulkAskDelete`→`openModal('bulk-delete')` L1038; no direct delete path |
| FN-92 | Validate all fields before save + termSummary matches data | ✓ | `submitTerm` L1101–1137; `termSummary` L914–924 used in list L1010 + view L1340 |

---

## 2. BR Coverage Matrix

| BR | Rule | HTML | Evidence |
|---|---|---|---|
| BR-01 | code unique | ✓ | dup check `submitTerm` L1106–1107 (import path N/A — no CSV) |
| BR-02 | credit net_days>0; postpay ≥0 | ✓ | credit>0 L1117; `onFormNum` `Math.max(0,...)` L1060 |
| BR-03 | deposit % >0 and ≤100 | ✓ | >100 L1115; >0 L1125 |
| BR-04 | installment ≥2 + total 100% | ✓ | L1110–1112 |
| BR-05 | discount_days >0 and < net_days | ✓ | L1121–1122 |
| BR-06 | use_in ≥1; Quotation sell-side only | ✓ | ≥1 L1119; `quotation` only in ฝั่งขาย group L804; no buy-side quotation exists |
| BR-07 | default 1-per-type + must be active | ✓ | L1128–1129 |
| BR-08 | used>0 not deletable (bulk skip); edit still allowed | ✓ | skip used>0 L1040; no edit lock |
| BR-09 | No CSV import/export | ✓ (absent) | CSS removed L442; import section emptied L1402–1410; toolbar has only "เพิ่มเงื่อนไข" L972 |
| BR-10 | Downstream picks active only; Credit trigger always immediate | ✓ | Credit `trigLock` L774; inactive "ซ่อนจากการเลือกใหม่" L954; archive desc "เลือกใน PO/Invoice ใหม่ไม่ได้" L1385 (actual downstream filtering is edge/backend) |

---

## 3. Edge Coverage (§9 + Central Plan `[config]`)

| Edge out | HTML representation | Evidence |
|---|---|---|
| → PO / SO (+ QUO sell) | `use_in` picker: po, so, quotation | `USE_IN_DOCS` L800/803/804; checkbox grid L1237–1248 |
| → AP/AR Invoice · PV / Receipt | `use_in`: ap_invoice, ar_invoice, payment_voucher, receipt | L801/805/802/806 |
| → Warehouse / GRN / Ship | Trigger field (immediate/after_deposit/after_full) + grn-trigger display | `TRIGGERS` L778–782; trigger dropdown L1167 / lock badge L1165; resolver = ENG-PT-02 **backend** |
| → Accounting / GL | Config inputs feed backend (deposit method, installment schedule, discount) | inputs present; journal split / deposit VAT / cash-discount = **backend** BACKEND comment L762–767 |
| → Customer / Vendor master default | **NOT-CHECKED** — OQ-PAY-03 edge declared, not built (added with partner master) | §9 / OB-3④; not in this feature scope |
| **Central Plan → PO `[config]`** | use_in po | ✓ representable |
| **Central Plan → AR Invoice `[config]`** | use_in ar_invoice | ✓ representable |
| **Central Plan → AP Invoice `[config]`** | use_in ap_invoice | ✓ representable |

---

## 4. Exception Paths

| Path | HTML | Evidence |
|---|---|---|
| code duplicate | ✓ | L1106–1107 + toast L1126 |
| credit ≤ 0 | ✓ | L1117 |
| deposit % = 0 / > 100 | ✓ | L1125 / L1115 |
| installment < 2 | ✓ | L1110 |
| installment ≠ 100% | ✓ | L1111–1112 |
| discount days ≥ net_days | ✓ | L1121–1122 |
| use_in empty | ✓ | L1119 |
| bulk delete used>0 skip | ✓ | L1040 + skip count toast L1044 |

---

## 5. Scope-Creep / Decided-OUT (must be ABSENT — FN-40 / S-10)

| Decided-OUT item | Result | Evidence |
|---|---|---|
| CSV import/export UI | ✅ ABSENT | CSS removed L442; import fn block emptied L1402–1410; no import button in toolbar L971–973 |
| Buy-side Quotation | ✅ ABSENT | `quotation` only exists in ฝั่งขาย (S2C) group L804; no buy-side quotation option |
| **Payment term at PR** | ⚠ **TENSION** | `USE_IN_DOCS.pr` IS a selectable use_in doc L799 (group ฝั่งซื้อ); footers name PR L994/L1355. **Contradiction:** OB-2 + FN-10 + task prompt declare PR as one of the 8 use_in docs, but LD-01 / FN-40 say "payment term at PR ห้ามมี". Source docs disagree — team must reconcile (OB-2 vs LD-01). Not a build defect; not scope creep introduced during vibe. |
| Editable Credit trigger | ✅ ABSENT | Credit `trigLock:true` L774 → renders lock badge, no editable dropdown L1164–1165 |
| >1 early-pay discount tier | ✅ ABSENT | single `discount_pct` + `discount_days` only L1171–1173; no tier repeater |
| Single-row delete / archive-reactivate in row | ✅ ABSENT | `renderRow` row-actions = edit button only L1013–1015; delete only via bulk |
| Approval chain / DOA UI | ✅ ABSENT | no approval UI; DOA placeholder null (approver_role/approved_by/approved_at/approval_chain) L1134 |

---

## 6. Golden Rules

| Rule | Result | Evidence |
|---|---|---|
| Soft-reference (snapshot, no cascade) | ✓ | edit updates master only, no cascade; archive desc "เอกสารเดิม...ยังคงอยู่" L1385; used>0 editable (snapshot) L1130–1132 (data behavior mostly backend, reflected in UI) |
| DOA placeholder null (no approval UI) | ✓ | 4 fields null on create L1134; no approval UI anywhere |
| No NOTIF emit | ✓ | `toggleNotif` is empty no-op L843; no emit on create/edit/status/delete |

---

## 7. Backend-only hooks (NOT UI gaps)

| Hook | Note |
|---|---|
| Installment journal split (ENG-PT-01) | BACKEND comment L763 — UI captures schedule; split is engine work |
| payment-trigger-resolver (ENG-PT-02) | UI has trigger field; resolution at downstream doc = backend |
| Deposit VAT invoice at point of receipt | BACKEND comment L764 — Tax Code + GL Posting Setup integration |

---

## 8. Gaps List (by severity)

| # | Sev | Gap | Where to fix |
|---|---|---|---|
| G1 | WARN | **PR in `use_in` vs LD-01/FN-40 decided-OUT** — HTML allows ticking Purchase Requisition as a payment-term doc, but LD-01/FN-40 say PR carries no payment term. Source contradiction (OB-2/FN-10 include PR; LD-01 excludes). | Reconcile in brief first (PM/BA): confirm whether PR is a valid `use_in` doc. If OUT → remove `pr` from `USE_IN_DOCS` L799 + footers L994/L1355. If IN → strike the FN-40/LD-01 line. **Do not edit HTML until brief is settled.** |
| G2 | WARN | **FN-01 dropdown lacks per-option description** — §3.1 wants a 2-line sub in the type dropdown; `typeOpts` passes only `label` (L1156). `PT_TYPES.hint`/`panelInfo` exist but unused in the option list. | HTML: enrich `typeOpts` + `sddOptsHtml` to render `sub`; or accept as descoped (record decision). Borderline UX. |
| G3 | INFO | **FN-29 off-canvas sidebar has no reveal control** — `.sidebar.is-open` (L70) exists but no hamburger button/JS toggles it; `.nav-toggle` (L67) is dead CSS. On 768–1180 the sidebar cannot be reopened. Status/user menus not in Esc chain. | Add nav-toggle button in shell-bar + toggle fn. Primarily qc-ux-html-checker territory. |

---

## Summary

Payment Term HTML is a **substantively complete master/config prototype**: all 26 functional FNs have wired UI hooks, all 10 BRs are reflected/enforced, all 7 exception paths validate with toasts, all in-scope edges are representable (Central Plan → PO/AR/AP all covered via `use_in`), and 5 of 6 decided-OUT items are correctly absent. Golden rules (soft-ref snapshot, DOA null, no NOTIF) are honored. Verdict **WARN**, driven by the PR-in-`use_in` source contradiction (G1) that needs a brief-level decision, plus two minor UI items (G2/G3). No BLOCK-severity gap — safe to proceed to FRD pack once G1 is reconciled.

---

# ✅ GATE RESOLUTION (2026-08-10)

- **G1 (PR contradiction) — CLOSED:** PM/BA ตัดสิน **"ถอด PR"** — payment term ไม่ผูกที่ PR (ตาม LD-01/FN-40 LOCK + ERP standard) · ลบ `pr` จาก USE_IN_DOCS + DP_DISABLED_DOCS · use_in = **7 เอกสาร** · sync caption 2 จุด · ไม่มี mock ใดอ้าง PR (zero data impact) · OQ-PAY-08 ปิด
- **G2 — FIXED:** type dropdown แสดงคำอธิบายสั้นต่อ option แล้ว (`typeOpts` ส่ง `sub:v.hint` + `.sdd-opt-main/.sdd-opt-sub`)
- **G3 — FIXED:** เพิ่มปุ่ม hamburger (`.nav-toggle`) เรียก `toggleSidebar()` + Esc ปิด sidebar · fix specificity (`.shell-bar .nav-toggle`) กัน icon-btn override · desktop ซ่อน / ≤1180 แสดง (render-verified)
- audit.sh FAIL=0 · render-verified clean (list + create drawer)

**Coverage หลังแก้:** FN 26/26 · BR 10/10 · edges 4/4 · scope-creep สะอาด 6/6 (PR ไม่ใช่ tension แล้ว) · **verdict → PASS**
