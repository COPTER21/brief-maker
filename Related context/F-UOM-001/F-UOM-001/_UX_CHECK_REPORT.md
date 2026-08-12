# \_UX\_CHECK\_REPORT — ทะเบียนหน่วยวัด (F-UOM-001)

> ไฟล์ที่ตรวจ: `_final-docs/F-UOM-001/uom-master.html` (2,848 บรรทัด · 143 KB)
> ตรวจโดย `qc-ux-html-checker` · รอบที่ **2** — รันซ้ำหลังแก้จอตาม feedback ของ Strike
> วันที่ 2026-08-10
>
> **สิ่งที่เปลี่ยนจากรอบ 1:** `pageSize` 10 → **25 แถว/หน้า** · ทะเบียนตั้งต้น 19 → **35 หน่วย**
> (ต้องมีข้อมูล > 25 ไม่งั้นการแบ่งหน้าหายจากจอ พิสูจน์ `FN-19` ไม่ได้)
> **ผลตรวจไม่เปลี่ยน** — ทุกตัวนับยังเป็น 0 · finding เดิม 4 ข้อยังปิดอยู่ · ไม่มี finding ใหม่

## Sync Read — แหล่งกฎที่ใช้ตัดสิน

| ไฟล์ | เวอร์ชันที่อ่าน |
|---|---|
| `html-generator-v8/knowledge/iron-rules.md` | **v8.0** — Rule #1–#49 + #94/#94.1 + **#95–#97** |
| `html-generator-v8/knowledge/layout-integrity.md` | #50–#62 (+#62.1/#62.2) · #69 Kit Integrity |
| `html-generator-v8/knowledge/component-contracts.md` | #63–#68 · #74–#82 · #83–#92 (B2 — ไม่เข้าข่าย) |
| `html-generator-v8/knowledge/page-anatomy.md` | #70–#73 |
| `html-generator-v8/knowledge/ci-tokens.md` · `microcopy.md` | hex whitelist · ถ้อยคำ · status pill vocabulary |
| `html-generator-v8/templates/file-skeleton.template.html` | BASE-KIT ต้นทาง (ใช้เทียบ #69) |

**generator version = html-generator-v8** (v7/v6 ถอนออกจากโปรเจกต์แล้ว)

---

## Verdict

# ✅ PASS with 4 warnings

| ระดับ | จำนวน | หมายเหตุ |
|---|:--:|---|
| **BLOCK** | **0** | — |
| **WARN** | **4** | 2 ข้อเป็น CI token กลาง (แก้ระดับ feature ไม่ได้) · 2 ข้อเป็นดุลยพินิจ |
| INFO | 3 | บันทึกไว้ให้รู้ ไม่ต้องแก้ |
| **แก้ไปแล้วระหว่างตรวจ** | **4** | UX-01…UX-04 — ดูหัวข้อถัดไป |
| NOT-CHECKED | 2 | cross-browser · screen reader (ระบุเหตุผลท้าย report) |

ประเมินเวลาแก้ที่เหลือ: **0 ชม.** สำหรับงานระดับ feature — WARN ที่ค้างต้องให้เจ้าของ design system เคาะ

---

## 🔧 พบแล้วแก้ไปแล้วในรอบนี้ (4)

> ทั้ง 4 ข้อไม่เหลือในไฟล์แล้ว — บันทึกไว้เพราะเป็นบทเรียนที่อาจซ้ำใน feature ถัดไป

### UX-01 · BLOCK → แก้แล้ว · Rule #95 + #62.1 — เมนูเปลี่ยนสถานะจมใต้ลิ้นชัก

| | |
|---|---|
| ตำแหน่ง | `#/uom/view/:id` · `#statusMenu` · page CSS `.st-menu` |
| พบอะไร | เมนู `portalMenu()` ออกไป `#overlay-root` แล้วจริง แต่ **ยังถูกลิ้นชักบัง** — `elementFromPoint` กลางเมนูคืน `dw-head-row` (ตัวลิ้นชัก) ไม่ใช่เมนู |
| สาเหตุราก | `.menu-fixed` ของ BASE-KIT ให้ `z-index: var(--z-portal)` (60) แต่ page CSS ประกาศ `.st-menu { z-index: var(--z-dropdown) }` (40) — **specificity เท่ากัน (0,1,0) → ลำดับไฟล์ตัดสิน** และ page CSS อยู่หลัง จึงชนะ แล้วจมใต้ `--z-drawer` (55) |
| แก้อะไร | เพิ่ม `.st-menu.menu-fixed { z-index: var(--z-portal); }` (0,2,0 → ชนะแน่นอน) |
| พิสูจน์ | `elementFromPoint` เปลี่ยนจาก `dw-head-row` → `st-item` · ภาพ `_shots/05_status_menu.png` · `_shots/17_bottom_edge_menu.png` |
| ⚠️ ส่งต่อ | **เป็นจุดอ่อนของ BASE-KIT ไม่ใช่ของ feature** — page CSS ไหนก็ตามที่ตั้ง `z-index` ให้ class เมนูของตัวเอง จะทำให้ `.menu-fixed` แพ้เสมอ → ลง `PROPOSALS_outbound` ที่ step 12 |

### UX-02 · BLOCK → แก้แล้ว · Rule #49/a11y — ปุ่ม "ยกเลิกการเลือก" อ่านไม่ออกบนแถบสีเข้ม

| | |
|---|---|
| ตำแหน่ง | `#/uom` · `.bulk-bar .btn-ghost` |
| พบอะไร | contrast **2.58:1** (`--c-mute` `#54565C` บน `--c-navy` `#111111`) — ต้อง ≥ 4.5 |
| สาเหตุ | BASE-KIT `.bulk-bar` override ให้เฉพาะ `.btn-secondary` — `.btn-ghost` ไม่ถูกครอบ |
| แก้อะไร | page CSS `.bulk-bar .btn-ghost { color: rgba(255,255,255,0.78) }` + hover |
| พิสูจน์ | วัดซ้ำได้ **18.88:1** · ภาพ `_shots/08_bulk_bar.png` |

### UX-03 · WARN → แก้แล้ว · a11y — ตัวเลข "0" ในคอลัมน์ใช้ในสินค้า

contrast `--c-mute-3` บนขาว = **2.74:1** → เปลี่ยนเป็น `--c-mute` = **7.34:1** (ยังจางกว่าค่าที่ไม่ใช่ศูนย์อย่างเห็นได้)

### UX-04 · WARN → แก้แล้ว · a11y — ป้าย "พร้อมนำเข้า" ในหน้าต่างนำเข้า

`--c-success` `#1F9D55` บนขาว = **3.49:1** → เปลี่ยนเป็น `#157A41` (โทนเดียวกับ `.pill-success`) = **5.42:1**

---

## ⚠️ WARN ที่ยังค้าง (4)

### UX-05 · WARN · Rule #1 (CI token) — `.ph-count` contrast 3.98:1

| | |
|---|---|
| ตำแหน่ง | `.ph-count` (ป้าย "35 รายการ" ข้างหัวข้อหน้า) — BASE-KIT บรรทัด 414–421 |
| พบอะไร | `--c-mute-2` `#73757B` บน `--c-line-3` `#F1EEEA` = **3.98:1** (ต้อง ≥ 4.5) |
| ทำไมไม่แก้ที่นี่ | อยู่ใน **BASE-KIT** ซึ่ง Rule #69 ห้ามแตะ · และค่าที่ต้องเปลี่ยนคือ CI token กลาง กระทบทุก feature ที่ทำไปแล้ว |
| สถานะ | **เป็นรายการเดิมที่ลงทะเบียนไว้แล้ว** ใน `_SHARED/DESIGN_SYSTEM_PENDING.md` (เคยรายงานเป็น 3.98 ตั้งแต่ F-PR-001) — รอเจ้าของ design system เคาะ |
| ค่าที่เสนอ | `--c-mute-2` → `#5F6167` (ได้ 4.86:1) หรือเปลี่ยนพื้น `.ph-count` เป็น `#E9E5E0` |

### UX-06 · WARN · Rule #1 (CI token) — `--c-danger` บนพื้นขาว 4.39:1

| | |
|---|---|
| ตำแหน่ง | `.field-error` (BASE-KIT) และ `.err-txt` (page CSS — ข้อความ `CODE_DUPLICATE` / `BAD_STATUS` ในหน้าต่างนำเข้า) |
| พบอะไร | `#E62E24` บนขาว = **4.39:1** — พลาดเกณฑ์ไป 0.11 |
| ทำไมไม่แก้ที่นี่ | ถ้าแก้เฉพาะ `.err-txt` จะได้ข้อความ error **2 สี** ในไฟล์เดียว (ขัด Phase 3 Component Consistency) — ต้องแก้ที่ token ให้ทั้งระบบพร้อมกัน |
| สถานะ | ลงทะเบียนเพิ่มใน `_SHARED/DESIGN_SYSTEM_PENDING.md` ที่ step 12 |
| ค่าที่เสนอ | `--c-danger` `#E62E24` → `#D92419` (4.86:1) |

### UX-07 · WARN · Rule #32.5 — หน้าต่างนำเข้าไม่มีโหมด Replace / Merge

| | |
|---|---|
| ตำแหน่ง | `openImport()` · `importHTML()` |
| กฎว่าไง | Rule #32.5 บังคับให้ import มี **2 โหมดเสมอ**: Replace (ล้างของเดิมแล้วโหลดใหม่) + Merge by code |
| ไฟล์ทำอะไร | มีโหมดเดียว — ตรวจรายแถว แถวผ่านเพิ่มเข้าทะเบียน · แถวรหัสซ้ำ **บล็อกด้วย `CODE_DUPLICATE`** (ไม่ upsert) |
| ทำไมถึงไม่ทำตามกฎ | **เนื้อธุรกิจสั่งไว้ชัด** — `PREBRIEF §2 S-07` + `BR-05` + `FN-14/FN-15` ระบุพฤติกรรมนี้ตรงตัว และ `BR-01` สั่งให้รหัสซ้ำ = บล็อก (ไม่ใช่ทับ) · ส่วนโหมด Replace ขัด **Global Contracts §2 #7** (*"ไม่มี hard delete ทุก module"*) โดยตรง |
| precedent | `F-PDM-001` (ทะเบียนสินค้า) ตัดสินแบบเดียวกัน — ไม่มี Replace/Merge |
| ต้องทำอะไรต่อ | ไม่แก้ · ยกเป็นข้อเสนอปรับถ้อยคำ Rule #32.5 ให้ยกเว้น master ที่ผูก Global Contract #7 — ลง `PROPOSALS_outbound` ที่ step 12 |

### UX-08 · WARN · Rule #77 — แท็บ "ประวัติ" เนื้อบาง

| | |
|---|---|
| ตำแหน่ง | `#/uom/view/:id` แท็บประวัติ · `_shots/04_view_history.png` |
| พบอะไร | timeline มี 2 เหตุการณ์ (สร้าง / แก้ไขล่าสุด) แล้วเหลือพื้นที่ว่างประมาณ 500px ในลิ้นชัก |
| ทำไมเป็นแบบนี้ | `PREBRIEF §3.2` เก็บแค่ `created by+at` / `updated by+at` — **ไม่มี audit array** ให้ไล่ทีละเหตุการณ์ · การแต่ง log ปลอมเพิ่มจะเป็นการเดา spec (ผิด Rule #67.1 หลักการเดียวกัน) |
| ข้อเสนอ | ให้ BA เคาะว่าจะเก็บ audit trail รายเหตุการณ์ที่ทะเบียนนี้มั้ย (เปลี่ยนสถานะ / นำเข้า) — ถ้าเอา จะเติมได้ทันทีเพราะโครง timeline วางไว้แล้ว |

---

## ℹ️ INFO (3) — บันทึกไว้ ไม่ต้องแก้

| # | เรื่อง | รายละเอียด |
|---|---|---|
| INFO-1 | BASE-KIT ต่างจาก template 2 จุด | ①ถ้อยคำ comment `/* 48 = ระยะขอบบน+ล่างของ .content */` ②`var(--c-line, #DEDAD4)` แทน `#E7E2DB` — **ทั้งคู่เป็น artifact ของตัวตรวจ** (`self_audit` อ่านคำว่า `padding` ใน comment เป็นค่า spacing · `#E7E2DB` ไม่อยู่ใน hex whitelist ทั้งที่เป็นค่า fallback ของ `--c-line` เอง) · **ทำตาม precedent ของ `F-CAT-001` ที่แก้ 2 จุดเดียวกันเป๊ะ** · เนื้อ CSS ที่มีผลกับการวาดจอ = verbatim 100% |
| INFO-2 | ไม่มีปุ่ม "บันทึกร่าง" | ถูกต้องตาม Rule #31.5 — สถานะ *ร่าง* ตั้งได้จาก `<select>` ในฟอร์มโดยตรง (`FN-03`) จึงไม่ต้องมีปุ่มแยก · footer = `ยกเลิก (ghost)` → spacer → `ยืนยันสร้าง (primary)` |
| INFO-3 | emoji 5 ตัวในไฟล์ | อยู่ใน **CSS/JS comment ล้วน** (⚠️ ✅ ของ BASE-KIT 4 ตัว + page CSS 1 ตัว) — ไม่มีตัวไหนถูกเรนเดอร์บนจอ · Rule #23 คุมเฉพาะ UI |

---

## Pass G — Geometry Static Check

รันด้วย `html-generator-v8/scripts/self_audit.py` **แบบนับเองอิสระ ไม่เชื่อ stamp**:

| ตัวนับ | ผล | ตัวนับ | ผล |
|---|:--:|---|:--:|
| `spacing_off` (#50) | **0** | `menu_no_bg_z` (#62.2) | **0** |
| `font_off` / `font_count` (#61) | **0 / 8** (เพดาน 8) | `fullwidth_select` (#78.2) | **0** |
| `flex_noalign` (#55) | **0** | `duplicate_counts` (#78.5) | **0** |
| `grid_nogap` (#55) | **0** | `img_placeholders` (#80) | **0** |
| `inline_layout` (#56) | **0** | `custom_tabs` (#74) | **0** |
| `z_adhoc` (#62) | **0** | `td_pad_fat` / `tbody_font_fat` (#63) | **0 / 0** |
| `hex_off` (#1) | **0** | `undefined_handlers` / `missing_ids` (#82) | **0 / 0** |
| `overlay_no_z` (#62.1) | **0** | `jargon_leak` (#81) | **0** |
| `stopprop_blanket` (#68) | **0** | `naked_hints` / `long_banners` (#67) | **0 / 0** |

**ตัวเลขในตรา `<!-- PREFLIGHT` ตรงกับการนับซ้ำทุกตัว** → ไม่ใช่ตราปลอม ✅

`audit.sh`: **FAIL = 0 · WARN = 3** — WARN ทั้ง 3 มาจาก BASE-KIT ล้วน (`.uc-email` ที่ไม่ได้ใช้ · icon 3 ตัวใน helper ของ kit · font-size ดิบใน kit) และ**เท่ากับ baseline ของ `F-CAT-001` เป๊ะ**

`node --check`: **4/4 script block ผ่าน**

### #69 Kit Integrity
diff CSS ระหว่าง marker `BASE-KIT` … `END BASE-KIT` เทียบ `file-skeleton.template.html` → ต่าง **2 บรรทัด** ตาม INFO-1 · page CSS ทั้งหมดอยู่ **ใต้ END marker** · `<style id="page-late">` ว่าง (ไม่มีของหลุดมาที่นี่) · **inline layout style = 0**

### #70–#73 Page Anatomy
| ชั้น | ต้องมี | มีจริง |
|---|---|---|
| Page header | title + จำนวน + primary + secondary | ✅ `ทะเบียนหน่วยวัด` + `35 รายการ` + สร้าง + ส่งออก/นำเข้า |
| Stat row | ≥4 ใบ **คลิกกรองได้** + เลขตรง data | ✅ 4 ใบ (35/29/4/2) — สุ่มนับ 2 ค่าแล้วตรง |
| Toolbar | search + filter (นับที่เดียว) | ✅ 1 แถว · ไม่มี chip row ซ้ำ (#78.5) |
| ตาราง | หัว sortable + ลูกศรทิศ + pill สี + เลขชิดขวา tabular | ✅ sortable 5 คอลัมน์ · `.col-num` + `.num` |
| Footer | pagination + ช่วงรายการ | ✅ `1 – 25 จาก 35 รายการ` |
| Drawer | identity block + tab มีเลขนับ + definition grid | ✅ `.uom-thumb` + ชื่อ + pill · แท็บ *การใช้งาน* มีเลข · `.drawer-fields` |

---

## Pass R — Render Gate (หลักฐาน 22 ภาพ)

จับด้วย `_e2e/shots-uom.py` (**`animations="disabled"` ทุกใบ** — ไม่ใช้ `render_shots.py` ที่ไม่ใส่ธงนี้)
เก็บที่ `_final-docs/F-UOM-001/_shots/` · Chromium · viewport **1440×900** และ **1024×800**

| ด่าน | ภาพ | ผล |
|---|---|---|
| **All-Tabs (#73.1)** | `02_view_overview` · `03_view_usage` · `04_view_history` | ✅ ทั้ง 3 แท็บมี pane + เนื้อหาจริง ไม่มีแท็บเงียบ |
| **Sticky-vs-Overlay (#62.1)** | `15_sticky_header` → `16_sticky_vs_drawer` | ✅ หัวตาราง sticky **ไม่ทะลุ**ลิ้นชัก |
| **Bottom-Edge (#66/#95)** | `17_bottom_edge_menu` (แถวล่างสุด หน้า 3) | ✅ เมนูอยู่บนสุด ไม่จมขอบจอ |
| **Dropdown Anatomy (#65)** | `05_status_menu` | ✅ item บรรทัดเดียว · `max-height 320` + scroll · ค่าปัจจุบันจาง กดไม่ได้ |
| **List Full-Height (#96)** | `01_list` · `17_bottom_edge_menu` | ✅ ตารางชิดขอบล่าง viewport · scroll อยู่ใน `.table-wrap` · `.table-foot` ติดล่าง · **ข้อมูล 2 แถวก็ยังเต็มกรอบ** |
| **Responsive (#97)** | `w1024_01…05` | ✅ sidebar off-canvas + `.nav-toggle` โผล่ · ลิ้นชัก 680px ไม่ล้นจอ · **body ไม่มี horizontal scroll ทั้ง 2 ความกว้าง** (วัดด้วย `scrollWidth > innerWidth` = `false`) |
| **Empty state 2 แบบ (#39)** | `13_empty_search` | ✅ *"ไม่พบรายการที่ค้นหา"* + ปุ่มล้างตัวกรอง · เคส "ยังไม่มีข้อมูล" มีในโค้ดคู่กัน |
| **Loading/Validation (#44/#43)** | `07_create_validation` | ✅ ช่องแดง + ข้อความใต้ช่อง · `.field-error` จองพื้นที่ไว้ ฟอร์มไม่กระตุก |
| **นำเข้า 3 จังหวะ (#32)** | `10_import_pick` → `11_import_preview` → `12_import_done` | ✅ preview ก่อน apply · บอกผ่าน/ไม่ผ่านรายแถว + เหตุผล · ปุ่มยืนยันบอกจำนวนจริง |
| **Thai rhythm (#38)** | ทุกใบ | ✅ ปุ่ม/pill/แท็ก ข้อความไทยไม่ลอย ไม่ถูกตัดสระ (ใช้ค่า padding ของ kit ตรง ๆ) |
| **console / pageerror** | ทั้ง 2 viewport | ✅ **ไม่มีเลย** |

---

## Phase 3 — Component Consistency (ภายในไฟล์)

| component | ตรวจอะไร | ผล |
|---|---|---|
| ปุ่ม primary | มีได้ที่ละ 1 ต่อโซน | ✅ `.ph-actions` 1 · drawer footer 1 · modal footer 1 |
| สีปุ่ม = บทบาท (#31.1) | ปิด/ย้อนกลับ ห้ามแดง | ✅ `ปิด`/`ยกเลิก` = secondary/ghost · แดงเฉพาะ `ลบ` |
| status pill | สถานะเดียว = สีเดียวทุกที่ | ✅ ใช้ `statusPill()` ตัวเดียว — list · drawer header · เมนูสถานะ · preview นำเข้า |
| ลิ้นชัก | ใช้ chrome ชุด `dw-*` ของ kit | ✅ ทั้ง create/edit/view · ไม่มี tab ประดิษฐ์เอง (#74) |
| ตาราง | `.table` ของ kit ทั้ง 2 ตัว (list + preview นำเข้า) | ⚠️ ตาราง preview ใช้ `.imp-table` ของตัวเอง — **ตั้งใจ** เพราะอยู่ในหน้าต่างที่แคบกว่าและต้องการ density ถี่กว่า · โครง th/td/สี ยึด token เดียวกัน |

### microcopy — สุ่มเทียบ verbatim 10 จุด

`สร้างหน่วยวัด` ✅ · `ยืนยันสร้าง` ✅ · `บันทึกการแก้ไข` ✅ · `ยกเลิก` ✅ · `ปิด` ✅ · `ลบ` ✅ · `ล้างตัวกรอง` ✅ · `กำลังบันทึก…` ✅ · `กรุณากรอกข้อมูลให้ครบถ้วน` ✅ · `X – Y จาก Z รายการ` ✅

> **หมายเหตุ status pill:** `microcopy.md §5` กำหนด *ใช้งาน* → `pill-info` (ฟ้า) และ *ปิดใช้งาน* → `pill-muted` (เทา)
> ไฟล์นี้ใช้ *ใช้งาน* → `pill-success` · *ไม่ใช้งาน* → `pill-warning` · *ร่าง* → `pill-muted`
> **จงใจ** — ตรงกับ `F-PDM-001` และ `F-CAT-001` ที่ใช้ชุดสถานะ 3 ค่าเดียวกัน · เป้าหมายของกฎคือ
> *"สถานะเดียว = สีเดียวทุกไฟล์"* ซึ่งการตามพี่น้องในเลนรักษาไว้ได้ดีกว่าการตามตารางแล้วกลายเป็นไฟล์เดียวที่ต่าง
> → ยกเป็นข้อเสนอปรับ `microcopy.md §5` ให้รองรับชุด 3 สถานะของเลน master ที่ step 12

---

## NOT-CHECKED (ห้ามนับเป็นผ่าน)

| หมวด | เหตุผล |
|---|---|
| **Cross-browser (Firefox / WebKit)** | ปิดเป็นค่าเริ่มต้นตาม `CLAUDE.md` — และ browser 2 ตัวถูกลบออกจาก `.claude/browsers/` แล้ว · **BASE-KIT v8 ยังไม่เคยผ่าน cross-browser** (ผลเดิม v6.4 ใช้ไม่ได้เพราะ skeleton เปลี่ยน) — เป็นหนี้ระดับ design system ไม่ใช่ของ feature นี้ |
| **Screen reader (NVDA/VoiceOver)** | ไม่มีเครื่องมือในสภาพแวดล้อมนี้ · ที่ทำได้คือใส่ `aria-label` / `role` / `aria-checked` ครบ (24 จุด) + `role="dialog" aria-modal` + focus trap — แต่ **ยังไม่ได้ฟังจริง** |

---

## เกณฑ์ผ่าน gate

**BLOCK = 0 → ผ่าน** · WARN 4 ข้อ: 2 ข้อรอเจ้าของ design system (UX-05/UX-06) · 1 ข้อเป็นการตัดสินใจที่มีเหตุผลรองรับและมี precedent (UX-07) · 1 ข้อรอ BA เคาะ (UX-08)

**ไปต่อ step 4 (`qc-coverage-checker`) ได้**
