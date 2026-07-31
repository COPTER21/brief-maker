# INDEX — F-PURCH-CFG-001 ตั้งค่าการจัดซื้อ (Purchase Configuration) (FRD Pack v5.1, FULL)

> **Generator:** frd-generator-v5 (v5.1) · **Source:** BRD-PURCH-CFG-001 (APPROVED) + P2P Cheat Sheet · **Status:** APPROVED

---

## §I.1 Pack Files
| File | Audience | Content |
|---|---|---|
| 00_OVERVIEW.md | All | Doc Control + Scope + Roles + Dependencies + 5 Open Q + D-Class |
| 01_UI.md | FE | 1 page · 2 tabs · Flow Preview + payment checklist + numbering + boundary/locked |
| 02_API.md | BE | 8 APIs (6 read + 2 PUT) + internal doc-number issue |
| 03_LOGIC.md | BE | 10 Functions + ENG-DOCNUM-01 (NEW) + external refs + Trace |
| 04_DB.md | DBA | 3 new tables + 3 read external + D-Class |
| 05_RULES.md | BE/QA | 12 Business Rules + 6 Validation + 6 Edge + Errors |
| 06_TESTS.md | QA | 11 FR Acceptance (incl numbering atomic) + DoD |
| 07_LOCKED_DECISIONS.md | All | 8 feature LDs + D01–D15 + Governance |
| INDEX.md | All | นี่ |

## §I.2 Quick Navigation
- **ทำไมไม่มี cost center/รหัสงบ ใน PR** → 07_LOCKED LD-03 (มากับ UNLK · บังคับที่ Budget Config)
- **payment types มาจากไหน** → 07_LOCKED LD-02 + 03_LOGIC FN-10 (Payment Term · inherit→PO)
- **เลขเอกสารไม่ซ้ำยังไง** → 03_LOGIC ENG-DOCNUM-01 (atomic FOR UPDATE) + 06_TESTS FR-08
- **Direct Payment อยู่ไหน** → 07_LOCKED LD-05 (AP Invoice / Finance)
- **PR/PO อ่าน config ยังไง** → 02_API API-06 (effective config) + 03_LOGIC FN-07

## §I.3 Consistency Summary
- **Entities:** NEW 3 (T_purchase_config, T_doc_numbering, T_purchase_config_log) · READ Payment Term / Budget Config / Vendor Price List
- **Engine:** NEW ENG-DOCNUM-01 (reusable) · external: DOA / Payment Term / Budget Config (read)
- **Mutations:** API-02 (config) + API-04 (numbering) → validate → persist → audit (R8)
- **Boundaries locked:** release-ref→Budget · approval→DOA · payment term→Finance · GRN→Inventory · Direct Payment→Finance · payment types ดึงจาก Payment Term
