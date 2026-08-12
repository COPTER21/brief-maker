# Coverage Report — F-BOM-001 · Bill of Materials (รอบ 2: FRD + Tests vs Business Scope)

- วันที่: 2026-08-12 · WF-01 Step 6 · skill: `qc-coverage-checker` (รอบ 2)
- Artifacts: `outputs/05_BOM/01_HTML/f-bom.html`, `outputs/05_BOM/04_FRD/FRD_F-BOM_Pack/`, `06_TESTS.md`
- Available contract: `Pack Brief Feature/5. BOM/FUNCTION_CHECKLIST_F-BOM_Bill-of-Materials.md`, `PREBRIEF_F-BOM_Bill-of-Materials.md`, BRD §3.4/§7/§9/§10/§12.1
- Formal `workflow_graph.json` / `NODE_BRIEF F-BOM`: **ไม่พบข้อมูลในบทสนทนาและไม่พบใน workspace**; report นี้จึงตรวจ continuity เทียบ declared Function Checklist/Prebrief เดิม โดยไม่เพิ่ม ERP rule เอง
- Checklist: FN-01..23 + FN-90 · edges in 2/out 2 · FN-30 provisional 3 · FN-40 scope guards 8

## Verdict: 🟡 WARN

**Substantive coverage: PASS** — FN 24/24, edges 4/4, BR 15/15, VR 8/8, confirmed edge cases 10/10 และ scope guards 8/8 มี FRD+TC evidence.  
**Governance warning:** formal graph/NODE_BRIEF ไม่มี จึงไม่สามารถรับรองว่า available checklist ตรงกับ graph revision ล่าสุดได้; ไม่มี block-rule/edge จาก contract ที่มีอยู่หายไป.

## Coverage Matrix — Function Checklist

| Item | HTML | FRD | TC | Evidence |
|---|---|---|---|---|
| FN-01 wizard 2 steps | ✓ | ✓ | ✓ | HTML `renderForm()` · `01_UI.md` §1.3 · AC-01/02 |
| FN-02 FG master combobox | ✓ | ✓ | ✓ | HTML `#fgCombo`/`renderFgOpts()` · `01_UI.md` §1.3/1.7 · TC-BR-03 |
| FN-03 header fields/default | ✓ | ✓ | ✓ | HTML `#f-ver/#f-name/#f-outqty` · `01_UI.md` §1.3 · TC-VR-02/03, TC-BR-02 |
| FN-04 component portal | ✓ | ✓ | ✓ | HTML `#lnCombo-*` · `01_UI.md` §1.3/1.7 · AC-07 |
| FN-05 qty/UoM/scrap/remove | ✓ | ✓ | ✓ | HTML line editor · `01_UI.md` §1.3 · TC-BR-06/14 |
| FN-06 live cost rollup/read-only cost | ✓ | ✓ | ✓ | HTML `lineCost()/bomCost()` · `03_LOGIC.md` ENG-01 · TC-BR-07/09 |
| FN-07 draft/active + null approval fields | ✓ | ✓ | ✓ | HTML `saveForm()` · `02_API.md` §2.2/API-02 · AC-02, TC-SCOPE-01 |
| FN-08 one default per FG | ✓ | ✓ | ✓ | HTML default-clear path · `03_LOGIC.md` FN-08 + DB partial index · AC-03/TC-EC-01 |
| FN-09 sibling versions clickable | ✓ | ✓ | ✓ | HTML `others.map(...navTo('bom/view/${x.id}'))` · `01_UI.md` §1.4 · AC-04 |
| FN-10 edit used BOM | ✓ | ✓ | ✓ | HTML edit has no `used` guard · `03_LOGIC.md` FN-04 · AC-05/TC-BR-12 |
| FN-11 parent/name validation | ✓ | ✓ | ✓ | HTML `saveForm()` · `05_RULES.md` VR-01/03 · TC-VR-01/03 |
| FN-12 version validation | ✓ | ✓ | ✓ | HTML blank/duplicate checks · `05_RULES.md` VR-02a/b · TC-VR-02a/b |
| FN-13 line/qty validation | ✓ | ✓ | ✓ | HTML `validateLines()` · `05_RULES.md` VR-04/05 · TC-VR-04/05 |
| FN-14 duplicate/self component | ✓ | ✓ | ✓ | HTML `validateLines()` · `05_RULES.md` VR-06/07 · TC-VR-06/07 |
| FN-15 component→UoM cascade | ✓ | ✓ | ✓ | HTML `selectLineItem()/uomsForItem()` · `01_UI.md` §1.3 · AC-07/TC-EC-05 |
| FN-16 stats/filter/search/sort composed | ✓ | ✓ | ✓ | HTML `filtered()/quickFilter()/sortBy()` · `01_UI.md` §1.2 · AC-10/list integration test |
| FN-17 single status all directions | ✓ | ✓ | ✓ | HTML `setStatus()` · `05_RULES.md` §5.2 · AC-08/TC-BR-08 |
| FN-18 bulk status/select states | ✓ | ✓ | ✓ | HTML `bulkSetStatus()/toggleSelAll()` · API-05/FN-06 · TC-CC-02/TC-BULK-01 |
| FN-19 guarded bulk delete | ✓ | ✓ | ✓ | HTML `openBulkDelete()/confirmBulkDelete()` · API-06/FN-07 · AC-09/TC-EC-07 |
| FN-20 product image/fallback | ✓ | ✓ | ✓ | HTML `prodAvatar()` · `01_UI.md` §1.2/1.3 · UI regression requirement §6.4 |
| FN-21 overlay portal | ✓ | ✓ | ✓ | HTML `#suggest-portal/placeSuggest()` · `01_UI.md` §1.7 · AC-07 UI path |
| FN-22 sticky/responsive/Esc/scroll | ✓ | ✓ | ✓ | HTML sticky styles/Esc chain · `01_UI.md` §1.7/1.8 · UI regression requirement §6.4 |
| FN-23 Warm Light/font/SVG icons | ✓ | ✓ | ✓ | HTML tokens/`renderIcons()` · `00_OVERVIEW.md` §0.6 sync v8 · visual regression requirement §6.4 |
| FN-90 record delete always confirms | ✓ | ✓ | ✓ | HTML only bulk-confirm record delete · `01_UI.md` §1.2 · AC-09 |

## Coverage Matrix — Rules, Edges and Exceptions

| Item | HTML | FRD | TC | Evidence |
|---|---|---|---|---|
| BR-01..15 | UI/backend split | ✓ | ✓ | `05_RULES.md` §5.1 has every row · `06_TESTS.md` TC-BR-01..15 |
| VR-01..08 | ✓ except server-only recheck | ✓ | ✓ | `01_UI.md` §1.6 · `05_RULES.md` §5.4 · TC-VR-01..08 |
| EC-01..10 | ✓/N/A-UI by case | ✓ | ✓ | `05_RULES.md` §5.5 · TC-EC-01..10 |
| Item Master → BOM | ✓ | ✓ | ✓ | HTML FG/component/cost mocks · API §2.X/FN-05 · XT-04/06 |
| UoM Master → BOM | ✓ | ✓ | ✓ | HTML `uomsForItem()` · API §2.X/FN-05 · AC-07/XT-06 |
| BOM → Production/MO | declared hook | ✓ | ✓ | HTML `used` guard/placeholder · API-07/FN-09 · XT-01..03 |
| BOM → Costing | ✓ rollup | ✓ | ✓ | HTML `bomCost()` · ENG-01/API §2.X · XT-04/05 |
| FN-30 cost 0/null | ✓ pass-through | ✓ provisional | ✓ | BR-09/AID-03 · TC-EC-08 |
| FN-30 scrap 100 | ✓ pass-through | ✓ provisional | ✓ | BR-14/AID-04 · TC-EC-09 |
| FN-30 master deactivation | ✓ pass-through | ✓ provisional policy | ✓ | BR-15/AID-05 · TC-EC-10 |
| FN-40 guards (8) | ✓ absent | ✓ locked out | ✓ | `00_OVERVIEW.md` §0.11 · TC-SCOPE-01..04 + TC-BR-02/05/13 |

## Gaps

ไม่พบ substantive gap จาก contract ที่มีอยู่.

## Warnings / NOT-CHECKED

- `workflow_graph.json` หรือ `NODE_BRIEF F-BOM` — NOT-CHECKED เพราะไม่พบไฟล์; หากมี graph revision ภายหลังต้อง rerun report นี้ด้วย `coverage_checklist.py`.
- OQ-BOM-01/04/06/07/08 ยังเป็น provisional/open ตาม `00_OVERVIEW.md` §0.10; tests ตรวจ propagation ของ default แล้ว แต่ stakeholder decision ยังไม่ปิด.

## Diff จากรอบ 1

- ปิดแล้ว: FN-09 — actual HTML ปัจจุบัน render sibling versions และเรียก `navTo('bom/view/${x.id}')`.
- ปิดแล้ว: FRD/API/logic/test contracts สำหรับ Production/MO และ Costing downstream.
- ใหม่: formal graph/NODE_BRIEF absence ถูกบันทึกเป็น governance warning; ไม่ใช่ evidence ว่า business behavior ขาด.
