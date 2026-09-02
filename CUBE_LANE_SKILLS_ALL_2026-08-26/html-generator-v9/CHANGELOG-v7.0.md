# html-generator-v7 — v7.0 (Consolidated Release)

**ธีม: Pattern B2 (Document Line Editor) + Iron Rule #94 (Master Combobox)**

## v7.0 คืออะไร
**v6 ทั้ง skill (ทุก pattern A-O, knowledge, references, scripts, templates) + การเปลี่ยนแปลง
ด้านล่างนี้ — เป็น standalone skill ใหม่ ติดตั้งชื่อ `html-generator-v7` แทน v6 ได้เลย**
`_SOURCE_pr-reference.html` เดิมยังอยู่ครบ (Pattern C/G อ้างอิง) — B2 มี reference ของตัวเอง

## ไฟล์ใหม่ (5)
| ไฟล์ | คืออะไร |
|---|---|
| `patterns/B2_document-line-editor.md` | Pattern B2 เต็ม — grid contract 8 คอลัมน์, VAT engine, totals order, hard control hook, reuse map PR/PO/QT/SO/GRN/INV/CN/RTV, QC #83–#92 |
| `references/drawer-standard/_SOURCE_line-editor-reference.html` | reference ทำงานเต็ม (จาก F-PR-001) — CI Warm Light, multi-UoM, budget hard control, item combobox keyboard nav ครบ |
| `references/drawer-standard/line-editor.css.html` | CSS ที่ B2 ต้องมี (verbatim) |
| `references/drawer-standard/line-editor.js.txt` | JS 23 top-level defs (verbatim, node --check ผ่าน) |
| `references/drawer-standard/master-combobox.js.txt` | canonical master combobox (Rule #94) — ตัวอย่าง = combobox "ผู้ขอ" |

## ไฟล์แก้ (6)
| ไฟล์ | แก้อะไร |
|---|---|
| `SKILL.md` | เพิ่มแถว B2 ในตาราง pattern selection + ตารางไฟล์ · เพิ่ม mandate B2 + Rule #94 ใน Pattern B Override · เพิ่ม v6.11 ใน version history |
| `knowledge/iron-rules.md` | Rule #11 เพิ่มข้อยกเว้น `.drawer-panel.wide` 1290px (B2 เท่านั้น) · **Group 18 / Rule #94 ใหม่: Master-Backed Field = Search Combobox เสมอ** + checklist item |
| `knowledge/component-contracts.md` | เพิ่ม **Rule #83–#92 Document Line Editor Contract** (ตาราง verdict BLOCK/WARN สำหรับ qc-ux Sync Read) |
| `patterns/B_create-edit-drawer-wizard.md` | line-item use case ชี้ไป B2 (บังคับ) |
| `patterns/E_compact-table-expandable.md` | โน้ตหัวไฟล์: ใน line-editor context → B2 เป็นเจ้าของ contract |
| `patterns/F_configurable-modifier.md` | โน้ตหัวไฟล์: เดียวกัน |

## กฎใหม่สรุป

**Rule #94 (BREAKING)** — field ที่อ้าง master (product / customer / vendor /
employee / dept / position / branch / BR / project / GL) ต้องเป็น search combobox
pattern เดียวกันเสมอ: state `{query,open,highlight}` · handlers ครบชุด · keyboard
↑↓/Enter/Esc (Esc ปิด list ก่อน — Esc chain) · focus เปิด list ทันที · item 2 บรรทัด
ตาม #65 · ปิดครบ 4 ทาง · drop-up ตาม #66 · empty state ในเมนู
ยกเว้น: enum สั้นที่ไม่ใช่ master และ UoM scoped ต่อสินค้า

**Rule #83–#92** — line editor contract (grid / totals reconcile / VAT exclusive /
ฐาน WHT ก่อน VAT / expand ทีละแถว / `.num` / UoM cascade ราคา / hard control
disable ปุ่มจริง / keyboard nav / แถวว่างบล็อก next)

## การแก้ใน reference (นอกเหนือจาก CI convert)
1. **CI:** Navy → Warm Light ครบ 0 residual (token + inline + เงา + ฟอนต์ Inter→Satoshi)
2. **Drawer width:** คืน base 920/680 + ประกาศ `.wide` 1290 แยก (เอกสาร B2 opt-in)
3. **ปิด OQ-B2-01:** เพิ่ม `onItemKey` + `closeItemSuggest` + highlight ใน suggest
   popover + drop-up (Rule #66) ให้ item combobox — contract ตรงกับ BR/emp/vendor แล้ว
4. `.pill.draft` slate rgba เก่า → #73757B · `.btn-success:hover` #00876F → #E08800

## งานต่อ (นอก skill นี้)
- **qc-ux-html-checker:** Sync Read #83–#92 + #94 จาก component-contracts/iron-rules
  ได้เลย (ไม่ต้องแก้ qc-ux เอง ตามหลัก Sync Read) — แต่ควรเพิ่มขั้น render:
  reconcile totals (#84), UoM cascade (#89), hard control disable (#90), keyboard (#91)
  เข้า `scripts/render_shots.py`
- **html-ui-brief:** เพิ่ม section "Line Editor Contract" สกัด 8 คอลัมน์ + สูตร +
  totals order ให้ dev ทำ backend ตรงสูตรตั้งแต่รอบแรก
- **cube-master-knowledge:** ลง Smart Code / registry ของ B2 + Rule #94

## หมายเหตุ audit
`scripts/audit.sh` กับ `_SOURCE_line-editor-reference.html` ให้ FAIL 1 (Rule #25 —
`lucide.createIcons()` ตรง) เป็น **false positive**: บรรทัดที่จับอยู่ *ข้างใน*
`renderIcons()` เอง — pattern เดียวกับ `_SOURCE_pr-reference.html` ที่เป็นมาตรฐานเดิม
WARN ที่เหลือ (#35/#49 scrollbar, #44 loader, #47 stepper กลาง) เป็นมรดกจากไฟล์
reference รุ่น pre-v6.1 skeleton — ไม่กระทบ contract ของ B2 ที่ lock ไว้
