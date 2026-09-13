# CHANGELOG — html-generator v9.0 (2026-08-25)

**แทน html-generator-v8** — base v8 ทั้งหมดคงเดิม (kit / tokens / Rules #1–#97) + ล็อก "แบบประกอบ" ของเอกสารธุรกรรม
จากไฟล์ที่ user craft + vibe แล้ว 3 ไฟล์: `f-sales-order.html`, `op-action-plan.html`, `team-plan.html`

## เพิ่ม
| สิ่งที่เพิ่ม | ที่อยู่ |
|---|---|
| **Pattern Q — Transaction Document Archetype** (list / wizard 5 steps / view tabs / PDF / sign / DOA modals) | `patterns/Q_transaction-document-archetype.md` |
| **Pattern P — Day Planner / Team Scheduler** | `patterns/P_day-planner-scheduler.md` |
| **Iron Rules #98 Document Archetype Lock · #99 Line Editor v2 Lock · #100 Wizard Step Contract · #101 View Tab Contract** | `knowledge/iron-rules.md` Group 20 |
| canonical เอกสาร + JS/CSS verbatim bundles | `references/document-archetype/` (`_SOURCE_so-reference.html`, `line-editor-v2.js.txt`, `doc-create-wizard.js.txt`, `doc-view-drawer.js.txt`, `doc-approval-modals.js.txt`, `doc-archetype.css.html`) |
| canonical planner | `references/planner/` |
| audit `doc_archetype` section (25 checks — ทริกเกอร์เมื่อไฟล์มี `vat_mode`/`renderSignTab`/`line-tbl`) | `scripts/audit.sh` |
| Phase 5 Check **G2** | `SKILL.md` |

## เปลี่ยน (BREAKING)
- **B2 canonical ย้ายจาก PR reference (v7/v8) → SO reference (v9)**: grid compact `.line-tbl` 26/—/64/92/92/78/72/104/54 ·
  lean 1-line advanced row · free-row ของแถม · discount engine (%/฿ + ท้ายบิล segmented + คูปอง) · totals 8 บรรทัด · `updateLine` focus-preserve
  → ไฟล์ที่ gen จาก v8 B2 จะ FAIL audit `doc_archetype` (ต้อง migrate ถ้าจะ re-gen)
- เอกสารแนบ = section ใน tab รายละเอียด — ห้ามเป็น tab แยก
- Pattern G/H/I ยังอยู่เป็นชิ้นส่วน แต่สำหรับเอกสารธุรกรรมต้องประกอบตาม Q เท่านั้น

## ไม่เปลี่ยน
- CSS var names / kit / skeleton / shell / Rules #1–#97 / patterns A–O
- `references/drawer-standard/` ยังอยู่ (legacy เทียบ + master-combobox canonical Rule #94)
