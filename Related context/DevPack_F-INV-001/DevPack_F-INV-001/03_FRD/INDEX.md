# INDEX — F-INV-001 Stock by Location FRD Pack

> Cross-reference + Function Trace + Quick Nav. Variant: **FULL** (9 files + INDEX).

---

## Quick Nav

| File | Purpose |
|---|---|
| [00_OVERVIEW.md](./00_OVERVIEW.md) | Scope, variant decision, roles, dependencies, 6 Open Questions, Coverage Manifest |
| [01_UI.md](./01_UI.md) | Layout Decision Log, routes, pages, drawers, modals |
| [02_API.md](./02_API.md) | 17 API contracts + cross-module contract |
| [03_LOGIC.md](./03_LOGIC.md) | 27 Functions + 3 Engines + API↔Logic trace |
| [04_DB.md](./04_DB.md) | 6 owned tables + field dictionary + data classification |
| [05_RULES.md](./05_RULES.md) | BR-01..11 + edge cases + error catalog |
| [06_TESTS.md](./06_TESTS.md) | 17+ acceptance criteria with verbatim on-screen text |
| [07_LOCKED_DECISIONS.md](./07_LOCKED_DECISIONS.md) | LD-01 (modal deviation), LD-02 (G-01 non-resolution) |

---

## Function Checklist (FN-01..23, FN-30, FN-40) → FRD Cross-Reference

| FN | Checklist description | 03_LOGIC | 01_UI | 02_API | 05_RULES | 06_TESTS |
|---|---|---|---|---|---|---|
| FN-01 | Stat 4 ใบ | FN-01 buildStockQuery | P-02 | API-02 | — | AC-01 |
| FN-02 | ตาราง 1 สินค้า 1 แถว | FN-04 aggregateByProduct | P-02 | API-02 | BR-04 | AC-01 |
| FN-03 | กรอง SV ทุกจุด | FN-03 isStockable | P-02/P-05 | API-02/API-08 | BR-02 | AC-01/AC-06 |
| FN-04 | สถานะสั้น 3 ค่า | FN-04 (inline classify) | P-02 | API-02 | BR-06 | AC-01/AC-07/AC-08 |
| FN-05 | รหัส 2 ชุด | FN-05 buildProductCodeChips | D-01/D-02 | API-03/API-04 | BR-01 | AC-01 |
| FN-06 | Tabs บนสุด + route refresh-safe | FN-21 syncRouteToState | D-01 | API-03 | — | AC-02 |
| FN-07 | ภาพรวม 3 ใบฐาน+note+conv+detail | FN-06/FN-07 | D-01/D-02 | API-04 | — | AC-02 |
| FN-08 | ตำแหน่งจัดเก็บ ตาราง | FN-08 resolveLocationUom | D-01/D-02 | API-07 | BR-03 | AC-02 |
| FN-09 | Low stock badge+stat+note | FN-09 checkLowStock | P-02/D-01 | API-02/API-03 | BR-05 | AC-07 |
| FN-10 | การเคลื่อนไหว merge+@ตำแหน่ง | FN-10 mergeProductMovements | D-01 | API-06 | — | AC-02 |
| FN-11 | การ์ดต่อตำแหน่ง+utilization | FN-11 computeLocationUtilization | P-03 | API-05 | — | AC-03 |
| FN-12 | Loc drawer ตามหน่วย loc+ฐานกำกับ+เจาะ balance | FN-12 getLocationContents | D-03 | API-05 | BR-03 | AC-03 |
| FN-13 | Modal grid v8 B2 | FN-14 renderAdjustmentLine | P-05 | API-08 | — | AC-05 |
| FN-14 | เหตุผลบังคับ+หมายเหตุ+เพิ่ม/ลบบรรทัด | FN-18 submitAdjustmentBatch | P-05 | API-08 | — | AC-05 |
| FN-15 | Validation ต่อบรรทัด live | FN-15 validateAdjustmentLine | P-05 | API-08 | BR-08 | AC-10/AC-11 |
| FN-16 | คงเหลือ live | FN-16 computeAdjustmentPreview | P-05 | — | — | AC-09 |
| FN-17 | เพิ่มเข้าตำแหน่งว่าง | FN-17 detectNewBalanceLine | P-05 | API-08 | BR-07 | AC-09 |
| FN-18 | บันทึก RAW+ADJ doc+movement+toast | FN-18 submitAdjustmentBatch | P-05 | API-08 | BR-09 | AC-05/AC-12 |
| FN-19 | RBAC | FN-19 canAdjust | all mutation entry points | API-08/11/14/15/16 | BR-10 | AC-13 |
| FN-20 | Overlay Portal+Esc chain | FN-20 manageOverlayPortal | §1.4 | — | — | AC-15 |
| FN-21 | #67.1 ไม่มี hint | — (verified absent) | §1.0 | — | — | — |
| FN-22 | ค้นหา+ซ่อน0+sort+pagination | FN-22 applyListFilters | P-02 | API-02 | — | AC-04 |
| FN-23 | Break/Pack picker กรอง SV+lock+movement แยก | FN-23..26 | P-04 | API-11/12/13/14/15/16 | BR-11 | AC-14/AC-14b |
| FN-30 | Edge (pid,loc) unique/neg EC-07/bucketsFor/stat ไม่ hardcode | ENG-INV-01 | — | — | §5.2, PR-9 | AC-08 |
| FN-40 | Gate (build/test infra) | N/A — infra, not business logic | — | — | — | — |

---

## Engine Registry (candidates, pending CUBIC registration)

| Engine | Category | Used by |
|---|---|---|
| ENG-INV-01 unit-conversion-engine | inventory-calculation | F-INV-001 (all quantity displays) |
| ENG-INV-02 adjustment-ceiling-engine | inventory-validation | F-INV-001 (Manual Adjustment) |
| ENG-INV-03 stock-audit-log-engine | compliance/audit | F-INV-001 (Manual Adjustment) |

---

## Open Questions Summary (see `00_OVERVIEW.md §0.8` for full detail)

| ID | One-line | Blocking |
|---|---|---|
| OQ-INV-01 | DOA threshold for high-value adjustments | NO |
| OQ-INV-02 | `min_stock` per-item vs per-item-per-warehouse | NO |
| OQ-INV-03 | Who/when may change a location's UoM | NO |
| OQ-INV-04 | Negative-stock reconciliation ownership + Sales-side block | **YES for go-live** |
| OQ-INV-05 | Low-stock → downstream action (notify/auto-PR/report) | NO |
| OQ-INV-06 | Costing/valuation (G-01) — keep and spec, or strip from HTML | **YES before dev sign-off** |

---

## Coverage Manifest Result (from `00_OVERVIEW.md §0.12`)

**OB 12/12 ✅ · Scenarios 14/14 ✅ · Functions 25/26 landed (FN-40 = infra, N/A) ✅ · OQ 6/6 tracked ✅**

Nothing silently dropped. One specification conflict (G-01) discovered in the ground-truth
artifact was tracked as OQ-INV-06 + LD-02, not resolved unilaterally by this FRD pass.
