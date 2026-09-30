# _UX_CHECK_REPORT — F-WH-GRN · GRN รับของ (ขั้น 7R re-gate)

> เลน WF-01 · Mode B (Phase A pack · `auto: lite`) · skill `qc-ux-html-checker`
> ไฟล์ที่ตรวจ `01_HTML/F-WH-GRN.html` · วันที่ตรวจ 2026-09-14
> registry F079 · arch **Q-document** · dec **ntf · csq · doccfg · pdfdoc** (ไม่มี doa) · wave W3

## 0. ทำไมต้อง re-gate (ห้ามใช้รายงานเดิม)

`feature-pack-workflow.md §7R.3` บังคับให้รัน gate ใหม่บนไฟล์ที่ vibe แล้ว **ห้ามใช้รายงานใน `0_DIRECTION/`/`1_HTML/` แทน** — และรอบนี้มีหลักฐานรูปธรรมว่ารายงานต้นน้ำใช้แทนไม่ได้จริง:

| หลักฐาน | รายงานต้นน้ำ | ไฟล์จริงที่ส่งมา |
|---|---|---|
| ขนาดไฟล์ | `_UX_CHECK_REPORT.md` + `_TECH_CHECK.md` เขียนตรงกันว่า **3,366 บรรทัด** · 225,923 bytes | **3,372 บรรทัด** · 225,923 bytes |
| PREFLIGHT stamp (ท้ายไฟล์) | `inline-layout=0 spacing-off=0 hex-off=0` | จริง `inline_layout` 58–149 · `spacing_off` 2 · `hex_off` 1 |

→ ไฟล์ถูกแก้หลังรายงานถูกเขียน · **stamp เขียนค่าที่ไม่ตรงกับไฟล์** (ไม่ยกเป็น BLOCK ตามแนวเดียวกับ F-PUR-PO แต่ถือว่า stamp เชื่อไม่ได้)

## 1. เครื่องมือที่รันเอง (ไม่รับค่าจากต้นน้ำ)

| เครื่องมือ | ผล |
|---|---|
| `html-generator-v9/scripts/audit.sh` | **FAIL=0 · WARN=3** |
| `html-generator-v9/scripts/self_audit.py` | FAIL 9 หมวด — ตรวจรายหมวดแล้ว **เป็น false positive ที่พิสูจน์แล้วทั้งหมด** (§4) |
| `qc-ux-html-checker/scripts/static_scan.py` | `doc_archetype.is_document=true` · ตัวชี้วัด Pattern Q ครบ (§2) |
| `node --check` ทุก `<script>` | **OK 4/4** |
| CSS brace balance ทุก `<style>` | **depth=0 ทุกบล็อก** (หลังแก้ — ดู §3 BLOCK-1) |
| Playwright runtime | console error **0** · pageerror **0** |

## 2. สัญญา archetype (Iron Rules) — ตรวจกับ `iron-rules.md` ตัวอักษรต่อตัวอักษร ไม่เทียบกับรายงานต้นน้ำ

| สัญญา | กติกา | ไฟล์จริง | ผล |
|---|---|---|---|
| Rule #100 wizard steps | `เลือกแหล่งที่มา · ข้อมูลหลัก[เอกสาร] · รายการสินค้า · เอกสารแนบ · ตรวจสอบและยืนยัน` | `เลือกแหล่งที่มา · ข้อมูลหลักใบรับของ · รายการสินค้า · เอกสารแนบ · ตรวจสอบและยืนยัน` | ✅ ตรง |
| Rule #101 view tabs | `รายละเอียด › [domain ≤2] › PDF Preview › ลายเซ็น › ประวัติ` | `detail · qc · pdf · sign · history` = `รายละเอียด · ตรวจคุณภาพ · PDF Preview · ลายเซ็น · ประวัติ` | ✅ ตรง |
| Rule #101 เอกสารแนบ | ห้ามเป็นแท็บแยก — ต้องเป็น section ใน รายละเอียด | `attach_in_detail=true` | ✅ |
| Rule #99 B2 v2 คอลัมน์ | `26 / — / 64 / 92 / 92 / 78 / 72 / 104 / 54` | `26 / — / 64 / 92 / 92 / 78 / 72 / 104 / 54` (9 ช่อง) | ✅ ตรงเป๊ะ |
| Rule #99 ฟังก์ชัน B2 | `calcLineVat` `migrateLine` `totals` `taxBadgeV` | มีครบ (`vat_segmented_3=true`) | ✅ |
| Rule #99 drawer `.wide` | 1290 | **920 → 1290 หลังแก้ BLOCK-1** | ✅ หลังแก้ |
| HANDOFF §3.3 ปี ค.ศ. ล้วน | ห้ามปน พ.ศ. แม้จุดเดียว | innerText ทุกสถานะ: ค.ศ. 31 ครั้ง · **พ.ศ. 0 ครั้ง** | ✅ |
| HANDOFF §3.4 ไม่มี DOA | ห้ามมีปุ่มอนุมัติ/สายอนุมัติ | ลายเซ็น = ผู้รับของ + ผู้ตรวจคุณภาพ · ไม่มี slot อนุมัติ · ไม่มี `DOA_BRIEF` | ✅ ไม่มี DIVERGENCE |

**DIVERGENCE check (§7R.4):** ไม่พบ surface ที่ registry ไม่ได้ประกาศ — ไม่มีสายอนุมัติ/ปุ่มอนุมัติ · เลขรันมาจากศูนย์ตั้งค่าเอกสาร · แบบพิมพ์ตรงกับชิป `pdfdoc` · **ไม่ต้องส่งกลับ BA**

## 3. สิ่งที่ตรวจเจอจริง + แก้แล้ว (4 จุด — ไฟล์ไม่ byte-identical กับ `input/` อีกต่อไป)

### BLOCK-1 · CSS ตายเงียบ 64 selector เพราะ `@keyframes` ไม่ปิดวงเล็บ ★ ร้ายแรงที่สุดของรอบนี้

`@keyframes line-expand-slide` และ `line-collapse-slide` **ขาด `to {}` และขาดปีกกาปิดทั้งคู่** → parser กลืนกฎที่เหลือทั้งบล็อกตั้งแต่ L1471 ถึงท้าย `<style>` (L1591)

- วัดด้วย CSSOM: style block ที่ 2 parse ได้ **45 กฎ จากที่ควรได้ 108** — หายไป **63 กฎ / 64 selector**
- surface ที่ตายรวม **สิ่งที่ Pattern Q บังคับ**: `.a4` + `.a4 table/th/td` (PDF Preview) · `.tl` `.tl-i` (timeline ลายเซ็น) · `.note` `.note.warn/.danger/.ok` (แบนเนอร์ทุกใบ) · `.hard-warn` (กติกาเพดานรับเกิน) · `.field.is-error` `.field-error` `.field-help` (การแจ้ง error ของฟอร์ม) · `.combo-pop` (Rule #94 master combobox) · `.upload-zone` (step 4) · `.line-expand-panel` (แถวขยาย B2) · `.emp-chip` `.slot-row` · `.drawer-panel.wide`
- อาการบนจอ: `.a4` ไม่มีพื้นขาว/ไม่มี padding → ใบ PDF เป็นบล็อกเทาคอลัมน์เบียด · `.note` `display:block` ไม่มีพื้นหลัง · ลิ้นชัก wizard กว้าง 920 แทน 1290
- **ทำไม gate เดิมไม่เจอ:** `audit.sh`/`self_audit.py`/`static_scan.py` เป็น regex ล้วน **ไม่ได้ parse CSS** · `node --check` ดูเฉพาะ JS · console error = 0 เพราะ CSS ที่ parse ไม่ผ่านไม่ throw
- **แก้:** ปิด `@keyframes` ทั้งสองให้ถูก พร้อมเติม `to {}` ตามชื่อ animation
- **ยืนยันหลังแก้:** กฎ 45 → **108** · `.note` = `flex · padding 10px 12px · radius 8px` · `.a4` = `background #fff · padding 36px 40px` · wizard drawer = **1290px** · หลักฐาน `_shots/13_view_pdf.png`

> **เช็คที่ต้องเพิ่มเข้าทุก pack:** `re.sub(r'/\*.*?\*/','',css)` แล้วนับ `{` − `}` ของทุก `<style>` ต้อง = 0 · และเทียบจำนวนกฎที่ CSSOM parse ได้กับจำนวน selector ในซอร์ส

### BLOCK-2 · Iron Rule #81 — marker `FWD-WIRE:` รั่วขึ้นจอผู้ใช้ (ครั้งที่ 3 ของรูปแบบนี้)

ต้นน้ำเปลี่ยน `TODO` → `FWD-WIRE` เพื่อเลี่ยง `audit.sh` Rule #24 (บันทึกไว้เองใน `_TECH_CHECK.md §4`) แต่ marker **ยังอยู่ใน template string ที่ render**

- ซอร์ส 13 จุด · เป็นคอมเมนต์ปลอดภัย 6 จุด · **render ขึ้นจอจริง 7 บรรทัด = 8 instance**
- สถานะที่เห็นได้: wizard ขั้น 3 (1) · **wizard ขั้น 5 (4 จุด รวม `ENG-DOC-NUM` · `putaway handoff (W3Q)`)** · view รายละเอียด (1) · view รายละเอียดเคสมีของไม่ผ่านตรวจ (2) · view ตรวจคุณภาพ (1) · ใบที่กลับรายการ (1)
- `self_audit.jargon_leak = 0` — **จับไม่ได้** (regex รู้จักแค่ `E-\d{3}|GR-…|bucket model|self-slice`) · จับได้จาก sweep `innerText` 17 สถานะ
- **แก้:** ถอด `· FWD-WIRE: …` ออกจากข้อความที่ผู้ใช้เห็น แล้ว **ย้าย trace ไปเป็นคอมเมนต์ในซอร์ส** 4 จุด (ledger ของ HANDOFF §4.3 ไม่หาย · `FWD-WIRE` ในซอร์สยังนับได้ครบ)
- **ยืนยันหลังแก้:** sweep `innerText` 17 สถานะ → **0 hit ทุกคำ** (`FWD-WIRE` `ENG-*` `JE posting` `RTV handoff` `putaway handoff` `W3Q` `(W5)`)

### BLOCK-3 · toast จมใต้ลิ้นชัก (`--z-*` ถูกใช้แต่ไม่ได้ประกาศ — ครั้งที่ 3 ของบั๊ก BASE-KIT v6.4)

- `var(--z-shell|--z-sticky|--z-dropdown|--z-backdrop|--z-drawer|--z-toast)` ถูกใช้ **12 จุด** แต่ `:root` ประกาศ **0 ตัว** → `getComputedStyle` คืน `(EMPTY)` ทั้ง 6 · overlay ทุกชั้น computed เป็น `z-index:auto`
- ไฟล์นี้มี overlay portal ของตัวเอง (`#overlay-root` z70 · `.overlay-wrap` z70) ซึ่งรับหน้าที่ชั้นซ้อนแทน — **แต่ `#toast` ไม่ได้อยู่ใน portal** จึงจมทุกครั้งที่มีลิ้นชัก/โมดัลเปิด
- **พิสูจน์บนเส้นทางผู้ใช้จริง:** wizard ขั้น 1 → กดใบสั่งซื้อที่เลือกไม่ได้ → toast *"เลือกไม่ได้ — ถูกปิดใบก่อนรับครบ (short-close)"* ขึ้นจริง (`is-visible`) แต่ `elementFromPoint` กลางตัว toast คืน element ของลิ้นชัก · `reachesUser: false` → **ผู้ใช้ไม่เห็นเหตุผลเลย** (บนหน้าลิสต์ที่ไม่มี overlay toast ปกติดี)
- **แก้:** ประกาศ 6 token ใน `:root` ตามชั้นจริงของไฟล์ (`sticky 20 · shell 30 · dropdown 40 · backdrop 50 · drawer 51 · toast 90` — toast 90 > row-menu 80 > overlay 70) + `body:has(#overlay-root .overlay-wrap) .toast{bottom:96px}` กันทับปุ่มใน footer ลิ้นชัก (บทเรียน F-SALES-TA)
- **ยืนยันหลังแก้:** `--z-toast=90` · เส้นทางเดิม `reachesUser: **true**` · `hitsFooterBtn: false`

### BLOCK-4 · เมนูของแถวไม่ flip ขึ้นบน — กดรายการสุดท้ายไม่ได้

- `openRowMenu()` สร้าง popover เอง (`document.body.appendChild` · `position:fixed`) แล้ว clamp เฉพาะ `left` **ไม่ clamp/flip `top`**
- แถวสุดท้ายของลิสต์: เมนูล้นขอบล่าง **49px** ทั้งที่ความสูง 900 และ 768 → ปุ่มล่างสุด (`กลับรายการ` / `ทิ้งร่าง` = action อันตราย) `elementFromPoint` ไม่คืนตัวเอง = **กดไม่ได้**
- `self_audit.menu_no_flip = 0` — **จับไม่ได้** เพราะครอบเฉพาะเมนูของ kit (`.menu-fixed`)
- **แก้:** วัด `offsetHeight` หลัง append แล้ว flip ขึ้นบนเมื่อชนขอบล่าง + clamp ในกรอบจอ
- **ยืนยันหลังแก้:** `overflowBottom=0 · overflowTop=0 · lastItemClickable=true` ทั้ง 900 และ 768 · หลักฐาน `_shots/19_FIX_rowmenu_flip_up.png`

## 4. self_audit FAIL ที่พิสูจน์แล้วว่าเป็น false positive (ไม่แก้ — ห้ามดัดโค้ดเพื่อหลบ regex)

| หมวด | ค่า | หลักฐานที่วัดเอง |
|---|---|---|
| `inline_layout` | 149 | นับด้วย regex เดียวกันกับ golden reference `_SOURCE_so-reference.html` = **139 · ไฟล์เรา 58** (สะอาดกว่า 2.4×) → WARN ตามแนว F-PUR-PO |
| `long_banners` | 9 | วัด `innerText` ทุกสถานะ → ยาว >120 จริงเหลือ **3 ข้อความ** (125 · 131 · 142) ดู §5 |
| `naked_hints` | 2 | เปิด wizard ขั้น 2 วัดจริง — `.field-help` **ทั้ง 6 ตัวมี `.lbl` กำกับครบ** ความยาว 33–58 ตัวอักษร |
| `fullwidth_select` | 5 | วัดจริง: 4 ตัวเป็น `<select>` ตัวกรองบนแถบกรอง กว้าง 172px ใน container 1158px = **ตั้งใจไม่เต็มความกว้าง** · อีกตัวคือ `<select>` หน่วยในตารางกรอกรายการ (B2 บังคับ) |
| `missing_ids` | 8 | `post-modal` `reason-modal` `row-menu` `ss-*` = id ที่สร้างตอน runtime ทั้งหมด |
| `custom_tabs` | 2 | ลิ้นชักเป็น overlay portal ของ Pattern Q ใช้ `.tab` ของตัวเอง ไม่ใช่ `.drawer-tabs` ของ kit |
| `stopprop_blanket` | 1 | `e.stopPropagation()` ตัวเดียวใน `openRowMenu` — จำเป็นเพื่อไม่ให้ row click เปิดลิ้นชัก |
| `spacing_off` | 2 | `1180` = breakpoint ของ Rule #97 · `52` = `--shell-h` |
| `hex_off` | 1 | `#E7E2DB` 1 จุด (เส้นคั่น) — นอกชุด token แต่อยู่ในโทน warm light เดิม |

## 5. WARN ที่เหลือไว้ (บันทึกอย่างเดียว — ยกเข้า `07_LOCKED` + README)

| # | เรื่อง | เหตุผลที่ไม่แก้ |
|---|---|---|
| W-01 | `Prototype · W3P` ที่แถบข้าง | scaffolding ของต้นแบบ — ให้ถอดก่อน production |
| W-02 | `(NC rules)` ใน field-help ของ "วันที่รับจริง" | ชื่อกติกาภายในที่ผู้ใช้งานจริงก็เรียกแบบนี้ — เสนอให้ BA ทบทวนถ้อยคำ |
| W-03 | ข้อความยาว >120 เหลือ 3 จุด (125 แบนเนอร์ของไม่ผ่านตรวจ · 131 การ์ดลายเซ็น "ไม่มีสายอนุมัติ" · 142 แบนเนอร์กลับรายการ) | เป็นข้อความอธิบายที่จำเป็น · ลดลงจากเดิมแล้วหลังถอด `FWD-WIRE` |
| W-04 | dead CSS ที่เหลือหลังแก้ BLOCK-1 | เกือบทั้งหมดเป็นชั้น drawer/toast ของ BASE-KIT ที่ไฟล์ไม่ได้ใช้ (ใช้ overlay portal แทน) · สแกน dead CSS เชื่อ 100% ไม่ได้ (มี `classList` 29 จุด + ต่อชื่อคลาส 11 จุด) |
| W-05 | `audit.sh` WARN 3 | Rule #21 `<i data-lucide>` ไม่มี `w-/h-` 3 จุด · Rule #40 `.uc-email` sub-line · hardcoded font-size — ทั้งหมดมาจาก BASE-KIT verbatim |
| W-06 | PREFLIGHT stamp ท้ายไฟล์เขียนค่าที่ไม่ตรงกับไฟล์ | ไม่แก้ stamp (เป็นของต้นน้ำ) — บันทึกว่าเชื่อไม่ได้ |

## 6. Responsive (วัดเป็นตาราง ไม่ใช่จุดเดียว)

`documentElement.scrollWidth` เทียบ `innerWidth`

| 1600 | 1440 | 1280 | 1180 | 1024 | 900 | 768 |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | **0** |

**ล้นแนวนอน 0 ทุกความกว้างรวม 768** — ผ่านครบ (เทียบ F-PUR-PO ที่ 768 ล้น) · หลักฐาน `_shots/20_list_1024.png` · `_shots/21_list_768.png`

## 7. หลักฐานภาพ (ถ่ายใหม่ทั้งชุดหลังแก้ · ภาพก่อนแก้ลบทิ้งแล้ว)

`CAPTURE VERIFY — OK 18 · SKIP 0 · FAIL 0` (pre-verify ทุก container ด้วย `getBoundingClientRect()` ว่า `w>0 && h>0` ก่อนถ่าย) · **md5 ซ้ำ 0 ไฟล์**

| ไฟล์ | สิ่งที่เป็นหลักฐาน |
|---|---|
| `_shots/01_list.png` | ลิสต์ + ตัวกรอง + สถานะเอกสาร |
| `_shots/02_wizard_s1_source.png` | ขั้น 1 เลือกแหล่งที่มา — tile 2 ช่อง (ช่องที่ 2 ปิด) + ใบสั่งซื้อที่เลือกไม่ได้ |
| `_shots/03_wizard_s2_master.png` | ขั้น 2 ข้อมูลหลักใบรับของ — 11 field + combobox #94 |
| `_shots/08_wizard_s4_attach.png` | ขั้น 4 เอกสารแนบ — `.upload-zone` (หลักฐานการแก้ BLOCK-1) |
| `_shots/09_wizard_s5_review.png` | ขั้น 5 ตรวจสอบและยืนยัน — จุดที่เคยรั่ว `FWD-WIRE` 4 จุด ตอนนี้สะอาด |
| `_shots/04_wizard_s3_lines.png` · `_shots/05_line_expand_qc.png` | ตาราง B2 v2 9 คอลัมน์ + แถวขยาย VAT/QC |
| `_shots/11_view_detail.png` | แท็บรายละเอียด — ลำดับ section ตาม Rule #101 |
| `_shots/14_view_sign.png` | แท็บลายเซ็น — ผู้รับของ/ผู้ตรวจ/ผู้ส่ง **ไม่มีปุ่มอนุมัติ** (LOCK-04) |
| `_shots/15_view_history.png` | แท็บประวัติ — ไทม์ไลน์ต่อท้ายอย่างเดียว |
| `_shots/12_view_qc.png` · `_shots/17_view_reject_detail.png` | เส้นทางของไม่ผ่านตรวจ → โซนกักของ |
| `_shots/13_view_pdf.png` | `.a4` เป็นกระดาษขาว + 3 ช่องลงชื่อ (หลักฐานการแก้ BLOCK-1) |
| `_shots/16_view_reversed.png` | ใบที่กลับรายการ |
| `_shots/18_FIX_toast_above_drawer.png` | toast ลอยเหนือลิ้นชัก (หลักฐานการแก้ BLOCK-3) |
| `_shots/19_FIX_rowmenu_flip_up.png` | เมนูแถวสุดท้าย flip ขึ้นบน (หลักฐานการแก้ BLOCK-4) |
| `_shots/20_list_1024.png` · `_shots/21_list_768.png` | responsive |

## 8. VERDICT

**PASS** — หลังแก้ 4 จุด (BLOCK-1..4) · WARN 6 ข้อบันทึกไว้ ไม่มีข้อไหนกันการส่งต่อ

- ก่อนแก้ verdict คือ **BLOCK** (BLOCK-1 ทำให้ surface ที่ Pattern Q บังคับ — PDF/timeline/แบนเนอร์/error ของฟอร์ม — ไม่มีสไตล์เลย)
- ไฟล์ใน pack **ไม่ byte-identical** กับ `input/09142026-grn/1_HTML/F-WH-GRN.html` อีกต่อไป (3,372 → 3,400 บรรทัด) — บันทึกไว้ที่ `03_FRD/07_LOCKED_DECISIONS.md` และ README เพื่อไม่ให้ใครภายหลัง `cmp` แล้วสรุปว่า pack ผิด
