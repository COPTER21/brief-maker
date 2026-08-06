# 07_LOCKED_DECISIONS — F-LOCATION-MASTER-001 · Warehouse & Bin

> LDs + convention deviations + Scope Lock (immutable). Global Engine IDs assigned at CUBIC Registry registration.

---

## §7.0 Scope Lock (imported from BRD §3.4 — IMMUTABLE, R11)

| LOCK | มติ | ผลต่อ pack |
|---|---|---|
| **D1** | Feature id F-LOCATION-MASTER-001, folder `11_Warehouse`, HTML `WarehouseBin.html` | คงทุกที่ |
| **D3** | `branch_id` required soft-ref บน **warehouses เท่านั้น** · **ไม่มี company_id** | 04_DB warehouses.branch_id; Zone/Area/Rack/Location สืบทอดผ่าน warehouse_id |
| **D8** | RBAC role-only · branch = filter/UX (ไม่ใช่ security boundary) | ไม่มี branch-scoped data permission; 5-role perms() |
| **D11/GC#7** | ไม่มี hard delete — node=archive (active children block), location=decommission (stock≠0 block) · append-only audit | WHB-FN-03/09, no DELETE, WORM |
| **D12** | Dual-view List + Hierarchy Tree · Tree = NON-STANDARD approved | 01_UI P-02, LD-01 |
| **D14** | Canonical name "Warehouse & Bin" (TH "คลังและตำแหน่ง") | sidebar/breadcrumb/h1/title |
| **D15** | ถอด role switcher · path shows name (zone/area/rack) + code (WH+location) · **branch ไม่แสดงใน path** (reverse D7 path) · ระดับ 5 = "ตำแหน่ง" | ENG-HIER-PATH, 01_UI §1.1, LD-04/LD-05/LD-10 |

**Drift check:** ไม่มี spec ใน pack ขัด LOCK. ไม่มี scope ใหม่เกิน LOCK. ✅

---

## §7.1 Locked Decisions (LD)

- **LD-01 — Hierarchy Tree = NON-STANDARD approved deviation (D12/AD-2).** Dual-view tree pane + node summary panel. เคารพ + log; ไม่ใช่ standard list pattern. Stakeholder approved (user).
- **LD-02 — Tree rows lack keyboard/arrow-key nav (UX-08).** Known dev-handoff gap; document for accessibility follow-up. Not blocking Phase 1.
- **LD-03 — No hard delete anywhere (GC#7/D11).** node=soft archive, location=soft decommission; referential-safe (active children/stock block). Audit append-only.
- **LD-04 — Role switcher removed (D15, supersedes D13).** Production role มาจาก auth. `perms()`/`ROLES`/`state.role` คงไว้ (logic), UI switcher ถอด.
- **LD-05 — Branch NOT in path (D15).** Reverses "branch in full_path" portion of D7. Branch ยังเป็น warehouse field (D3) + List column/filter (D7).
- **LD-06 — RBAC role-only, no branch-scoped permission (D8).** Branch-scoped = ฝาก Permission Matrix (Policy & Security) system-wide, future.
- **LD-07 — No DOA / approval workflow.** Master data — RBAC only; SoD via del=Manager/Admin.
- **LD-08 — SPA view-switch, no hash route.** Views = `state.view`/`state.drawer.view`/`state.modal.type` (not URL). Dev binds state-driven rendering, not hash routing.
- **LD-09 — Pill palette = sanctioned CI extension (D10).** status = color-code (CUBE variants); type = icon+label ไม่ color-code. ไม่นับเป็น drift.
- **LD-10 — Dead `.role-switch` CSS + `setRole()`/`syncRoleChip()` = non-feature dead code (D15).** Do NOT implement as feature; safe to strip in production build.
- **LD-11 — Global Engine IDs at CUBIC Registry.** ENG-HIER-PATH, ENG-BULK-PLAN = scope-local codes now; global id assigned at registration.
- **LD-12 — Branch/Geo master = mock endpoints Phase 1 (AD-1/AD-6).** Real Company/Geo master integration = Phase 2 (OQ-1/OQ-2).
- **LD-13 — BR-018 applyTypeDefaults DEFERRED Phase 3 (AD-3).** Schema-ready contract only; not implemented; confirm map at OQ-3.

## §7.2 Convention Deviations
- Node APIs level-parameterized (`/nodes/:level`) instead of 4 separate resource paths — mirrors single `submitNode` in HTML; documented for consistency.
- "route" in 01_UI = state/view identifier (SPA), not HTTP route (LD-08).
- NON-STANDARD tree pattern (LD-01) — approved, not a v7 standard pattern.
