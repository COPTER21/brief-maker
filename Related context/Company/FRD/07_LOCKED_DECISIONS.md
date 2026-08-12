# 07_LOCKED_DECISIONS — F-ORG-001

## Locked Decisions
| ID | Decision | Rationale |
|---|---|---|
| LD-01 | Module เดียว 1 FRD pack (5 entity) ไม่แตก 5 pack | เป็น SPA โมดูลเดียว, BRD เดียว (BRD-ORG-001); ลด overhead |
| LD-02 | Variant = FULL | multi-engine 3 + has-state + has-entity |
| LD-03 | Detail = landing page (ไม่ใช่ view-drawer-tabbed) | BRD §14.6 deviation (user-requested) — FRD ไม่ override (R2) |
| LD-04 | Org chart = custom tree extension | BRD §14.6 — มาตรฐานไม่มี org-chart |
| LD-05 | Engine IDs scope-local (F-ORG-ENG-01..03) | Global ENG-NNN assign ตอน register CUBIC Registry |
| LD-06 | position ผูก dept+division พร้อมกันได้ (matrix) — แสดง dept ก่อน | BR-04; precedence รอยืนยัน (OQ-2) |
| LD-07 | salary_min/max = Restricted | CUBE 4.0 Data Classification; wire Restricted Resources (OQ-1) |
| LD-08 | approval = Pre-DOA (field + TODO) ไม่ hardcode | DOA engine กลาง (F-PC-DOA-01) — Phase 2 |
| LD-09 | โลโก้บริษัทเก็บเป็น `logo_url` (Object Storage ref; prototype ใช้ dataURL) — Classification Confidential; ชนิด/ขนาดจาก Config File ไม่ hardcode | BRD v1.1 §6.1/§14 (BR-14); storage ยืนยัน OQ |

## Convention Deviations
- ไม่มี — ใช้ convention มาตรฐาน (F-ORG-API/FN-NN, kebab-case engine, snake_case field, UPPER_SNAKE error)

## Layout Reference
SSOT = html-generator-v3 v3.9 (33 Iron Rules). Templates: list-view(A), create/edit-drawer-wizard(B) 540, modal-confirmation(D), modal .is-lg(#32 CSV), landing page(dev), org-chart(ext). CI lock: Navy/Primary/Teal.
