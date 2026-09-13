# Check Methods — map facts → rules → severity

หลักการ: **script ให้ facts, iron-rules.md (Sync Read สด) ให้กฎ, Claude ตัดสิน**
ตารางนี้บอก "วิธีตัดสิน" — เลขกฎอ้างอิง v3.13 ถ้าไฟล์กฎเปลี่ยนเลข ให้ยึดไฟล์กฎ

## หมวด Mechanical (จาก static_scan.py)

| Fact | วิธีตัดสิน | Severity |
|---|---|---|
| `hex_colors` | เทียบ whitelist จาก ci-tokens.md — hex นอกลิสต์ = violation (ยกเว้นใน comment/สี rgba ที่กฎอนุญาต) รายงาน hex + count + first_line | BLOCK |
| `font_families` | ทุกค่าต้องอยู่ใน stack ที่กฎกำหนด (Satoshi/Noto Sans Thai/system) | BLOCK |
| `px_watchlist.540px` | > 0 = drawer legacy (Rule #11) — ระบุทุกจุด | BLOCK |
| `px_watchlist.920px/680px/440px` | ถ้ามี drawer/modal แต่ไม่พบค่ามาตรฐานเลย → สงสัยผิด spec ไปเปิดดูจุดจริง | BLOCK ถ้าผิดจริง |
| `px_watchlist.232px/52px` | มี sidebar/shell แต่ค่าไม่ตรง → Rule #3/#4 | BLOCK |
| `lucide_icon_count` = 0 / `fontawesome` = true / `emoji.count` > 0 | Rule #5 (emoji เช็คบริบท — ในเนื้อหา mock data บางแบบอนุโลม, ใน UI chrome ไม่ได้) | BLOCK/WARN ตามบริบท |
| `hash_routes` ว่าง หรือ `hashchange_listener` = false | SPA ต้อง hash routing | BLOCK |
| `escape_handler` = false ทั้งที่มี drawer/modal | Esc chain หาย | BLOCK |
| `drawer_translate` = false ทั้งที่มี drawer | Rule #12 animation | WARN |
| `scrollbar_width_px` ≠ 5 หรือไม่มี | iron rule minimal scrollbar 5px | WARN |
| `localStorage_or_session` = true | ห้ามใช้ (fail ใน runtime เป้าหมาย) | BLOCK |
| `external_scripts` | อนุญาตเฉพาะ CDN ที่ v6 ระบุ (lucide, fonts, tailwind ถ้า template ใช้) — นอกนั้นถาม | WARN |
| `inline_style_attr_count` สูงผิดปกติ (>~30) | สัญญาณ style หลุด token system → สุ่มเปิดดู | WARN |

## หมวด Heuristic (Claude อ่านโค้ดเอง — script ช่วยชี้เป้าด้วย markers)

| ตรวจ | สัญญาณจาก script | วิธีตรวจจริง |
|---|---|---|
| Empty state (Rule #39) | `markers.empty_state` = 0 แต่ `count_table` > 0 | เปิดดูทุก list: มี empty ครบ (icon+ข้อความ+CTA ตาม microcopy) มั้ย |
| Loading/Submitting (#44) | `markers.loading` = 0 แต่มี form | ปุ่ม submit มี state กดแล้วมั้ย, list โหลดมี skeleton มั้ย |
| Disabled ถูกจังหวะ (#45) | `markers.disabled` | ปุ่มที่ไม่ควรกดได้ตอนไหน disabled จริงมั้ย |
| Destructive confirm | `markers.confirm_modal` = 0 แต่มีปุ่มลบ | action ลบ/ยกเลิก ต้องผ่าน modal 440px |
| Layout stability (#35) | — | toggle/expand แล้ว element อื่นกระโดดมั้ย (อ่าน css/js) |
| Button symmetry (#36) | — | คู่ปุ่ม primary/secondary ขนาด-ลำดับตรง pattern มั้ย |
| Thai rhythm + microcopy (#38) | — | เทียบถ้อยคำกับ microcopy.md — ปุ่ม, empty, error, placeholder |
| List UX (#40-42) | — | cell atomicity, คลิก row = view, long list มี pagination/virtual |

## หมวด Component Consistency (ภายในไฟล์)

วิธีตรวจ: grep class ของ component หลัก (btn, badge, drawer, card, table, filter)
→ ดูว่ามีนิยามซ้ำที่ค่าต่างกันมั้ย / มีการ style ตรงจุดเดียวแบบ one-off มั้ย
ตัดสินโดยเทียบ component-catalog-ref.md ว่าแบบไหนคือมาตรฐาน → อีกแบบคือของต้องแก้

## กติกา NOT-CHECKED

กฎที่ต้องเห็น rendering จริง (เช่น ความรู้สึก spacing บางกรณี, contrast บนจอจริง)
→ ใส่หมวด NOT-CHECKED พร้อมเหตุผล + วิธีให้ user เช็คเองใน 1 บรรทัด
ห้ามเดาผลแล้วนับเป็นผ่าน

## v9 facts (2026-08-25) — map fact → rule

| Fact (static_scan) | ตีความ | verdict |
|---|---|---|
| `px_watchlist.1290px` > 0 แต่ไม่มี `.drawer-panel.wide` | 1290 ใช้ได้เฉพาะ B2/Q wide drawer | BLOCK #11 |
| `select_big` > 0 หรือ `select_big_template` > 0 (select ที่ map จาก master) | ต้องเป็น search combobox | WARN #102 (BLOCK ถ้าเป็น master คน/สินค้า/คู่ค้า) |
| `combobox_count` > 0 แต่ `combo_person_option` = 0 ทั้งที่มี field คน | option คนไม่มี avatar/ตำแหน่ง | BLOCK #102 |
| `overlay_root` = false หรือ `portal_menu` = false ทั้งที่มี dropdown ในตาราง/drawer | เมนูจะจมใต้ overflow | BLOCK #95 |
| `page_fill` = false ในไฟล์ที่มีหน้า list | ตารางไม่ชิดขอบล่าง | WARN #96 |
| `render_table_only` = false ทั้งที่มี filter/sort | re-render ทั้งหน้า → กระโดด | WARN #103 |
| `body_minwidth_768` = false / `scrollbar_gutter_stable` = false | responsive/stability | WARN #97 / #35 |
| `td_multi_pill` > 0 | ซ้อนข้อมูลคนละตัวใน cell | BLOCK #103/#40 (ยกเว้น pill ของแถม+ชื่อสินค้า = WARN) |
| `doc_archetype.is_document` = true → ทุกช่องใน `doc_archetype` ต้อง true · `wizard_steps` = 5 ชื่อล็อก (ตัด "รายการสินค้า" ได้ถ้าไม่มี line items) · `view_tabs` เริ่ม detail ลง pdf/sign/history ท้าย ไม่มี attach · `line_tbl_widths` = [26,64,92,92,78,72,104,54] | Pass D | BLOCK #98–#101 |
| `preflight_stamp` = null | ไม่มี pre-flight | BLOCK #60 |
| `planner_archetype` = true | ตรวจตาม patterns/P (cal-grid · pool-card · plan-row · cap-track · seg-control · mbar ถ้าเป็นทีม) | ตามหัวข้อ |
